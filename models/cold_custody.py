"""Null model with independent cell losses, independent intervals, and full repair."""

from __future__ import annotations

import argparse
import json
import math
from decimal import Decimal, localcontext


def _interval_failure_decimal(
    *,
    cells: int,
    reconstruction_threshold: int,
    custodian_population: int,
    replicas: int,
    failure_probability: float,
) -> Decimal:
    if not 0 < reconstruction_threshold <= cells:
        raise ValueError("threshold must be in [1, cells]")
    if replicas <= 0:
        raise ValueError("replicas must be positive")
    if custodian_population <= 0 or replicas > custodian_population:
        raise ValueError("replicas must not exceed the custodian population")
    if not 0 <= failure_probability <= 1:
        raise ValueError("failure_probability must be in [0, 1]")

    cell_loss = Decimal(str(failure_probability))**replicas
    if cell_loss == 0:
        return Decimal(0)
    if cell_loss == 1:
        return Decimal(1)
    # Sum the failure tail directly. Subtracting near-one survival destroys
    # the tiny risks this model compares with p_max. Decimal retains an
    # interval risk below float range until checkpoint amplification.
    result = sum(
        Decimal(math.comb(cells, surviving))
        * (1 - cell_loss)**surviving * cell_loss**(cells - surviving)
        for surviving in range(reconstruction_threshold)
    )
    return min(Decimal(1), result)


def interval_failure_probability(**kwargs: int | float) -> float:
    with localcontext() as ctx:
        ctx.prec = 80
        return float(_interval_failure_decimal(**kwargs))


def interval_survival_probability(**kwargs: int | float) -> float:
    """Compatibility view; near-one survival may round to one. Use failure for risk."""
    return 1 - interval_failure_probability(**kwargs)


def _lease_failure_decimal(
    *,
    cells: int,
    reconstruction_threshold: int,
    custodian_population: int,
    replicas: int,
    failure_probability: float,
    duration: float,
    repair_interval: float,
) -> Decimal:
    if not math.isfinite(duration) or not math.isfinite(repair_interval) or duration <= 0 or repair_interval <= 0:
        raise ValueError("duration and repair_interval must be positive")
    checkpoints = (Decimal(str(duration)) / Decimal(str(repair_interval))).to_integral_value(rounding="ROUND_CEILING")
    interval = _interval_failure_decimal(
        cells=cells,
        reconstruction_threshold=reconstruction_threshold,
        custodian_population=custodian_population,
        replicas=replicas,
        failure_probability=failure_probability,
    )
    if interval == 1:
        return Decimal(1)
    if checkpoints == 1 or interval == 0:
        return interval
    # log1p/expm1 series avoid cancellation in the small tails. Below 1e-30
    # the omitted relative terms are <1e-90, below this 80-digit context.
    tiny = Decimal("1e-30")
    hazard = checkpoints * (interval * (1 + interval/2 + interval**2/3)
                            if interval < tiny else -(1-interval).ln())
    if hazard < tiny:
        return hazard * (1 - hazard/2 + hazard**2/6)
    return 1 - (-hazard).exp()


def lease_failure_probability(**kwargs: int | float) -> float:
    with localcontext() as ctx:
        ctx.prec = 80
        return float(_lease_failure_decimal(**kwargs))


def lease_survival_probability(**kwargs: int | float) -> float:
    """Compatibility view; target decisions must use lease_failure_probability."""
    return 1 - lease_failure_probability(**kwargs)


def minimum_replicas(
    *,
    cells: int,
    reconstruction_threshold: int,
    custodian_population: int,
    failure_probability: float,
    duration: float,
    repair_interval: float,
    p_max: float,
    max_replicas: int = 32,
) -> int | None:
    if not 0 < p_max < 1:
        raise ValueError("p_max must be in (0, 1)")
    for replicas in range(1, min(max_replicas, custodian_population) + 1):
        with localcontext() as ctx:
            ctx.prec = 80
            failure = _lease_failure_decimal(
                cells=cells,
                reconstruction_threshold=reconstruction_threshold,
                custodian_population=custodian_population,
                replicas=replicas,
                failure_probability=failure_probability,
                duration=duration,
                repair_interval=repair_interval,
            )
            if failure <= Decimal(str(p_max)):
                return replicas
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells", type=int, required=True)
    parser.add_argument("--threshold", type=int, required=True)
    parser.add_argument("--custodians", type=int, required=True)
    parser.add_argument("--replicas", type=int, required=True)
    parser.add_argument("--failure-probability", type=float, required=True)
    parser.add_argument("--duration-epochs", dest="duration", type=float, required=True)
    parser.add_argument(
        "--repair-interval-epochs", dest="repair_interval", type=float, required=True
    )
    parser.add_argument("--p-max", type=float, default=1e-6)
    args = parser.parse_args()
    if not 0 < args.p_max < 1:
        parser.error("p-max must be in (0, 1)")
    with localcontext() as ctx:
        ctx.prec = 80
        exact_failure = _lease_failure_decimal(
            cells=args.cells,
            reconstruction_threshold=args.threshold,
            custodian_population=args.custodians,
            replicas=args.replicas,
            failure_probability=args.failure_probability,
            duration=args.duration,
            repair_interval=args.repair_interval,
        )
        meets_target = exact_failure <= Decimal(str(args.p_max))
    failure = float(exact_failure)
    print(
        json.dumps(
            {
                "model": "independent_cell_loss_checkpoint_null",
                "assumptions": ["independent cell losses (no assignment overlap)",
                                "independent intervals", "successful full repair between intervals"],
                "lease_survival_probability": 1 - failure,
                "lease_failure_probability": failure,
                "meets_target_under_null_model": meets_target,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
