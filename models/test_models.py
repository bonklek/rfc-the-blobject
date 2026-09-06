import unittest

from cold_custody import interval_failure_probability, lease_failure_probability, lease_survival_probability, minimum_replicas
from decimal import Decimal, localcontext
import math
import contextlib
import io
import json
from unittest.mock import patch
from cold_custody import main as custody_main
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
    def test_partial_horizon_cannot_claim_future_admissions_or_full_coverage(self) -> None:
        for arrivals, horizon in (([Arrival(5, 1, 1)], 0), ([Arrival(0, 1, 10)], 2)):
            with self.subTest(horizon=horizon), self.assertRaises(ValueError):
                simulate("truncated", arrivals, Mechanism("shared", "byte_time"), horizon=horizon)

    def test_default_horizon_covers_long_shared_lease(self) -> None:
        result, series = simulate("long", [Arrival(0, 1, 5000)], Mechanism("shared", "byte_time"))
        self.assertEqual(series[-1]["occupancy"], 0)
        self.assertGreaterEqual(series[-1]["epoch"], 5000)
        self.assertAlmostEqual(result.realized_scarcity, 5000 / .999)

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
    def test_cli_uses_same_target_precision_as_replica_selection(self) -> None:
        args = ["cold_custody.py", "--cells", "1", "--threshold", "1", "--custodians", "10",
                "--replicas", "1", "--failure-probability", ".02", "--duration-epochs", "27",
                "--repair-interval-epochs", "1", "--p-max", ".4204324735203474"]
        output = io.StringIO()
        with patch("sys.argv", args), contextlib.redirect_stdout(output):
            custody_main()
        self.assertFalse(json.loads(output.getvalue())["meets_target_under_null_model"])
        self.assertEqual(minimum_replicas(cells=1, reconstruction_threshold=1,
                         custodian_population=10, failure_probability=.02,
                         duration=27, repair_interval=1, p_max=.4204324735203474), 2)

    def test_exact_target_boundary_is_accepted(self) -> None:
        self.assertEqual(minimum_replicas(cells=1, reconstruction_threshold=1,
                         custodian_population=10, failure_probability=.1,
                         duration=1, repair_interval=1, p_max=.1), 1)

    def test_interval_underflow_does_not_hide_accumulated_risk(self) -> None:
        kwargs = dict(cells=1, reconstruction_threshold=1, custodian_population=10,
                      failure_probability=1e-200, duration=1e300, repair_interval=1)
        self.assertAlmostEqual(lease_failure_probability(**kwargs, replicas=2) / 1e-100, 1)
        self.assertEqual(minimum_replicas(**kwargs, p_max=1e-150), 3)

    def test_tiny_risk_target_uses_failure_not_rounded_survival(self) -> None:
        self.assertEqual(minimum_replicas(cells=1, reconstruction_threshold=1,
                         custodian_population=10, failure_probability=1e-10,
                         duration=1, repair_interval=1, p_max=1e-25), 3)

    def test_failure_tail_matches_high_precision_reference(self) -> None:
        with localcontext() as ctx:
            ctx.prec = 110
            q = Decimal("0.01")
            interval = sum(Decimal(math.comb(128, j)) * (1-q)**j * q**(128-j)
                           for j in range(64))
            expected = float(1 - (1 - interval)**512)
        actual = lease_failure_probability(cells=128, reconstruction_threshold=64,
                     custodian_population=10000, replicas=2, failure_probability=.1,
                     duration=4096, repair_interval=8)
        self.assertAlmostEqual(actual / expected, 1, places=10)

    def test_failure_endpoints_and_shared_custodian_counterexample(self) -> None:
        kwargs = dict(cells=2, reconstruction_threshold=1, custodian_population=1, replicas=1)
        self.assertEqual(interval_failure_probability(**kwargs, failure_probability=0), 0)
        self.assertEqual(interval_failure_probability(**kwargs, failure_probability=1), 1)
        independent = interval_failure_probability(**kwargs, failure_probability=.1)
        self.assertAlmostEqual(independent, .01)
        self.assertLess(independent, .1)  # Sole holder failure loses both cells together.

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
