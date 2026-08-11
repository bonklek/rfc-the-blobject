import unittest

from cold_custody import lease_survival_probability, minimum_replicas
from pricing import compare, convex_duration, null_byte_time
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
        self.assertNotIn("orphan", state.objects)

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
