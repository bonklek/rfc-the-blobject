"""Independent-failure null model for cold row custody."""

from __future__ import annotations

import argparse
import json
import math


def interval_survival_probability(
    *,
    cells: int,
    reconstruction_threshold: int,
    custodian_population: int,
    replicas: int,
    failure_probability: float,
) -> float:
    if not 0 < reconstruction_threshold <= cells:
        raise ValueError("threshold must be in [1, cells]")
    if replicas <= 0:
        raise ValueError("replicas must be positive")
    if custodian_population <= 0 or replicas > custodian_population:
        raise ValueError("replicas must not exceed the custodian population")
    if not 0 <= failure_probability <= 1:
        raise ValueError("failure_probability must be in [0, 1]")

    cell_loss = failure_probability**replicas
    cell_survival = 1 - cell_loss
    return sum(
        math.comb(cells, surviving)
        * cell_survival**surviving
        * cell_loss ** (cells - surviving)
        for surviving in range(reconstruction_threshold, cells + 1)
    )


def lease_survival_probability(
    *,
    cells: int,
    reconstruction_threshold: int,
    custodian_population: int,
    replicas: int,
    failure_probability: float,
    duration: float,
    repair_interval: float,
) -> float:
    if duration <= 0 or repair_interval <= 0:
        raise ValueError("duration and repair_interval must be positive")
    checkpoints = math.ceil(duration / repair_interval)
    interval = interval_survival_probability(
        cells=cells,
        reconstruction_threshold=reconstruction_threshold,
        custodian_population=custodian_population,
        replicas=replicas,
        failure_probability=failure_probability,
    )
    return interval**checkpoints


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
        survival = lease_survival_probability(
            cells=cells,
            reconstruction_threshold=reconstruction_threshold,
            custodian_population=custodian_population,
            replicas=replicas,
            failure_probability=failure_probability,
            duration=duration,
            repair_interval=repair_interval,
        )
        if survival >= 1 - p_max:
            return replicas
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells", type=int, required=True)
    parser.add_argument("--threshold", type=int, required=True)
    parser.add_argument("--custodians", type=int, required=True)
    parser.add_argument("--replicas", type=int, required=True)
    parser.add_argument("--failure-probability", type=float, required=True)
    parser.add_argument("--duration", type=float, required=True)
    parser.add_argument("--repair-interval", type=float, required=True)
    parser.add_argument("--p-max", type=float, default=1e-6)
    args = parser.parse_args()
    survival = lease_survival_probability(
        cells=args.cells,
        reconstruction_threshold=args.threshold,
        custodian_population=args.custodians,
        replicas=args.replicas,
        failure_probability=args.failure_probability,
        duration=args.duration,
        repair_interval=args.repair_interval,
    )
    print(
        json.dumps(
            {
                "lease_survival_probability": survival,
                "lease_failure_probability": 1 - survival,
                "meets_target": survival >= 1 - args.p_max,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
