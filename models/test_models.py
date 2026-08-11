import unittest

from cold_custody import lease_survival_probability, minimum_replicas
from pricing import compare, convex_duration, null_byte_time
from spot_simulation import Arrival, Mechanism, run_all, simulate
from stock import ProtocolState, frontier


class StockModelTests(unittest.TestCase):
    def test_expiry_releases_stock(self) -> None:
        state = ProtocolState(
            capacity_bytes=1_000,
            min_retention_epochs=1,
            max_retention_epochs=8,
        )
        state.admit_blob(commitment="a", size=400, retention_epochs=2)
        self.assertEqual(state.retained_bytes, 400)
        state.advance_to(1)
        self.assertEqual(state.retained_bytes, 400)
        state.advance_to(2)
        self.assertEqual(state.retained_bytes, 0)

    def test_capacity_rejects_admission(self) -> None:
        state = ProtocolState(
            capacity_bytes=100,
            min_retention_epochs=1,
            max_retention_epochs=4,
        )
        state.admit_blob(commitment="a", size=80, retention_epochs=1)
        with self.assertRaises(ValueError):
            state.admit_blob(commitment="b", size=21, retention_epochs=1)

    def test_reorg_restores_fork_state(self) -> None:
        state = ProtocolState(
            capacity_bytes=1_000,
            min_retention_epochs=1,
            max_retention_epochs=8,
        )
        state.admit_blob(commitment="canonical", size=200, retention_epochs=4)
        parent = state.snapshot()
        state.admit_blob(commitment="orphan", size=300, retention_epochs=2)
        state.restore(parent)
        self.assertEqual(state.retained_bytes, 200)
        self.assertFalse(any(meta.commitment == "orphan" for meta in state.objects.values()))

    def test_slot_based_expiry_delivers_full_duration(self) -> None:
        state = ProtocolState(
            capacity_bytes=1_000,
            min_retention_epochs=1,
            max_retention_epochs=8,
        )
        state.advance_to_slot(31)
        meta = state.admit_blob(commitment="late", size=100, retention_epochs=1)
        self.assertEqual(meta.expiry_slot, 63)
        state.advance_to_slot(62)
        self.assertEqual(state.retained_bytes, 100)
        state.advance_to_slot(63)
        self.assertEqual(state.retained_bytes, 0)

    def test_identical_commitments_create_distinct_leases(self) -> None:
        state = ProtocolState(
            capacity_bytes=1_000,
            min_retention_epochs=1,
            max_retention_epochs=8,
        )
        first = state.admit_blob(commitment="same", size=100, retention_epochs=1)
        second = state.admit_blob(commitment="same", size=100, retention_epochs=2)
        self.assertNotEqual(first.object_id, second.object_id)
        self.assertEqual(state.accounted_bytes, 200)

    def test_reclamation_grace_delays_capacity_credit(self) -> None:
        state = ProtocolState(
            capacity_bytes=100,
            min_retention_epochs=1,
            max_retention_epochs=8,
            reclamation_grace_slots=4,
        )
        state.admit_blob(commitment="grace", size=100, retention_epochs=1)
        state.advance_to_slot(32)
        self.assertEqual(state.retained_bytes, 0)
        self.assertEqual(state.accounted_bytes, 100)
        with self.assertRaises(ValueError):
            state.admit_blob(commitment="too-soon", size=1, retention_epochs=1)
        state.advance_to_slot(36)
        self.assertEqual(state.accounted_bytes, 0)

    def test_frontier_geometry(self) -> None:
        self.assertAlmostEqual(frontier(384, 1), 1)


class PricingModelTests(unittest.TestCase):
    def test_convex_premium_is_not_below_null(self) -> None:
        null = null_byte_time(size=10, duration=8, utilization=0.5, base_price=1)
        convex = convex_duration(
            size=10,
            duration=8,
            utilization=0.5,
            base_price=1,
            reference_duration=2,
        )
        self.assertGreater(convex, null)

    def test_comparison_exposes_all_hypotheses(self) -> None:
        result = compare(size=10, duration=8, utilization=0.5, base_price=1)
        self.assertEqual(
            set(result),
            {
                "null_byte_time",
                "convex_duration",
                "quantized_maturity",
                "expected_scarcity",
                "auction_reserve_proxy",
            },
        )

    def test_comparison_uses_fixed_external_maturities(self) -> None:
        result = compare(size=1, duration=300, utilization=0, base_price=1)
        self.assertEqual(result["quantized_maturity"], 512)

    def test_comparison_reference_is_not_derived_from_request(self) -> None:
        short = compare(size=1, duration=256, utilization=0, base_price=1)
        long = compare(size=1, duration=4096, utilization=0, base_price=1)
        self.assertEqual(short["convex_duration"], 256)
        self.assertGreater(long["convex_duration"] / 4096, 1)


class SpotSimulationTests(unittest.TestCase):
    def test_expiry_releases_capacity_for_later_arrival(self) -> None:
        result, _ = simulate(
            "expiry",
            [Arrival(0, 100, 256), Arrival(256, 100, 256)],
            Mechanism("shared", "byte_time", capacity=100),
            horizon=513,
        )
        self.assertEqual(result.rejected_bytes, 0)

    def test_lane_partition_can_strand_capacity(self) -> None:
        result, _ = simulate(
            "fragmentation",
            [Arrival(0, 60, 256)],
            Mechanism(
                "lanes",
                "maturity_lanes",
                capacity=100,
                maturities=(256, 4096),
            ),
            horizon=257,
        )
        self.assertEqual(result.rejected_bytes, 60)
        self.assertGreater(result.stranded_capacity, 0)

    def test_all_normalized_scenarios_run(self) -> None:
        results, series = run_all()
        self.assertEqual(len(results), 18)
        self.assertTrue(series)


class ColdCustodyModelTests(unittest.TestCase):
    def test_more_replicas_improve_survival(self) -> None:
        one = lease_survival_probability(
            cells=8,
            reconstruction_threshold=4,
            custodian_population=100,
            replicas=1,
            failure_probability=0.2,
            duration=10,
            repair_interval=1,
        )
        two = lease_survival_probability(
            cells=8,
            reconstruction_threshold=4,
            custodian_population=100,
            replicas=2,
            failure_probability=0.2,
            duration=10,
            repair_interval=1,
        )
        self.assertGreater(two, one)

    def test_minimum_replicas_meets_target(self) -> None:
        replicas = minimum_replicas(
            cells=16,
            reconstruction_threshold=8,
            custodian_population=100,
            failure_probability=0.25,
            duration=4096,
            repair_interval=8,
            p_max=1e-6,
        )
        self.assertIsNotNone(replicas)


if __name__ == "__main__":
    unittest.main()
