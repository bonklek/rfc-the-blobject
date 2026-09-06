"""Normalized immediate-start retention allocation scenarios.

This model deliberately uses synthetic capacity units and arbitrary fee units.
It tests allocation behavior named by the RFC; it does not estimate Ethereum
parameters, demand, or operator costs.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from pricing import DEFAULT_MATURITIES, convex_duration, null_byte_time, utilization_price


@dataclass(frozen=True)
class Arrival:
    epoch: int
    size: float
    duration: int
    label: str = "ordinary"


@dataclass
class Lease:
    size: float
    expiry: int
    billed_duration: int
    lane: int | None
    charge: float
    realized_scarcity: float = 0.0


@dataclass(frozen=True)
class SimulationResult:
    scenario: str
    mechanism: str
    requested_bytes: float
    admitted_bytes: float
    rejected_bytes: float
    rejection_rate: float
    total_charge: float
    realized_scarcity: float
    charge_coverage: float
    peak_occupancy: float
    stranded_capacity: float
    peak_expiry: float


@dataclass(frozen=True)
class Mechanism:
    name: str
    kind: str
    capacity: float = 1_000.0
    base_price: float = 1.0
    reference_duration: float = 1_024.0
    duration_exponent: float = 1.25
    maturities: tuple[int, ...] = tuple(int(item) for item in DEFAULT_MATURITIES)


def _maturity(duration: int, maturities: tuple[int, ...]) -> int:
    candidate = next((item for item in sorted(maturities) if item >= duration), None)
    if candidate is None:
        raise ValueError("duration exceeds the longest maturity")
    return candidate


def _quote(
    mechanism: Mechanism,
    *,
    size: float,
    requested_duration: int,
    billed_duration: int,
    utilization: float,
) -> float:
    if mechanism.kind == "term_premium":
        return convex_duration(
            size=size,
            duration=billed_duration,
            utilization=utilization,
            base_price=mechanism.base_price,
            reference_duration=mechanism.reference_duration,
            exponent=mechanism.duration_exponent,
        )
    return null_byte_time(
        size=size,
        duration=billed_duration,
        utilization=utilization,
        base_price=mechanism.base_price,
    )


def simulate(
    scenario: str,
    arrivals: Iterable[Arrival],
    mechanism: Mechanism,
    *,
    horizon: int | None = None,
) -> tuple[SimulationResult, list[dict[str, float | int | str]]]:
    events: dict[int, list[Arrival]] = {}
    requested_bytes = 0.0
    last_expiry = 0
    for arrival in arrivals:
        if arrival.epoch < 0 or arrival.duration <= 0 or arrival.size <= 0:
            raise ValueError("arrivals require nonnegative epochs and positive size/duration")
        events.setdefault(arrival.epoch, []).append(arrival)
        requested_bytes += arrival.size
        billed = (_maturity(arrival.duration, mechanism.maturities)
                  if mechanism.kind == "maturity_lanes" else arrival.duration)
        last_expiry = max(last_expiry, arrival.epoch + billed)

    max_arrival = max(events, default=0)
    if horizon is None:
        horizon = max(last_expiry, max_arrival + max(mechanism.maturities) + 1)
    elif horizon < last_expiry:
        raise ValueError("horizon must cover every arrival and full billed lease expiry")

    active: list[Lease] = []
    completed: list[Lease] = []
    rejected_bytes = 0.0
    stranded_capacity = 0.0
    peak_occupancy = 0.0
    peak_expiry = 0.0
    series: list[dict[str, float | int | str]] = []

    lane_capacity = mechanism.capacity / len(mechanism.maturities)

    for epoch in range(horizon + 1):
        expiring = [lease for lease in active if lease.expiry == epoch]
        if expiring:
            peak_expiry = max(peak_expiry, sum(lease.size for lease in expiring))
            completed.extend(expiring)
            active = [lease for lease in active if lease.expiry != epoch]

        rejected_this_epoch = 0.0
        for arrival in events.get(epoch, []):
            lane = None
            billed_duration = arrival.duration
            if mechanism.kind == "maturity_lanes":
                billed_duration = _maturity(arrival.duration, mechanism.maturities)
                lane = billed_duration
                used = sum(item.size for item in active if item.lane == lane)
                available = lane_capacity - used
                utilization = used / lane_capacity
            else:
                used = sum(item.size for item in active)
                available = mechanism.capacity - used
                utilization = used / mechanism.capacity

            if arrival.size > available:
                rejected_bytes += arrival.size
                rejected_this_epoch += arrival.size
                if mechanism.kind == "maturity_lanes":
                    total_used = sum(item.size for item in active)
                    stranded_capacity = max(
                        stranded_capacity, max(0.0, mechanism.capacity - total_used)
                    )
                continue

            charge = _quote(
                mechanism,
                size=arrival.size,
                requested_duration=arrival.duration,
                billed_duration=billed_duration,
                utilization=utilization,
            )
            active.append(
                Lease(
                    size=arrival.size,
                    expiry=epoch + billed_duration,
                    billed_duration=billed_duration,
                    lane=lane,
                    charge=charge,
                )
            )

        total_occupancy = sum(item.size for item in active)
        peak_occupancy = max(peak_occupancy, total_occupancy)

        for lease in active:
            if mechanism.kind == "maturity_lanes":
                lane_used = sum(item.size for item in active if item.lane == lease.lane)
                utilization = lane_used / lane_capacity
            else:
                utilization = total_occupancy / mechanism.capacity
            lease.realized_scarcity += lease.size * utilization_price(
                min(utilization, 0.999_999), mechanism.base_price
            )

        if epoch in events or expiring or epoch % 64 == 0:
            series.append(
                {
                    "scenario": scenario,
                    "mechanism": mechanism.name,
                    "epoch": epoch,
                    "occupancy": total_occupancy,
                    "rejected": rejected_this_epoch,
                    "expired": sum(lease.size for lease in expiring),
                }
            )

    completed.extend(active)
    admitted_bytes = requested_bytes - rejected_bytes
    total_charge = sum(lease.charge for lease in completed)
    realized_scarcity = sum(lease.realized_scarcity for lease in completed)
    coverage = total_charge / realized_scarcity if realized_scarcity else 1.0
    result = SimulationResult(
        scenario=scenario,
        mechanism=mechanism.name,
        requested_bytes=requested_bytes,
        admitted_bytes=admitted_bytes,
        rejected_bytes=rejected_bytes,
        rejection_rate=rejected_bytes / requested_bytes if requested_bytes else 0.0,
        total_charge=total_charge,
        realized_scarcity=realized_scarcity,
        charge_coverage=coverage,
        peak_occupancy=peak_occupancy,
        stranded_capacity=stranded_capacity,
        peak_expiry=peak_expiry,
    )
    return result, series


def _baseline() -> list[Arrival]:
    events: list[Arrival] = []
    for epoch in range(0, 2_048, 64):
        events.extend(
            (
                Arrival(epoch, 18, 256, "elastic-short"),
                Arrival(epoch, 12, 1_024, "elastic-medium"),
                Arrival(epoch, 5, 4_096, "security-constrained"),
            )
        )
    return events


def scenarios() -> dict[str, list[Arrival]]:
    baseline = _baseline()
    front_load = baseline + [Arrival(128, 350, 4_096, "front-loaded-long")]
    correlated = [
        Arrival(item.epoch, item.size, 4_096, "correlated-maximum")
        if 512 <= item.epoch < 1_024
        else item
        for item in baseline
    ]
    occupation = baseline + [
        Arrival(epoch, 100, 4_096, "adversarial") for epoch in range(128, 576, 64)
    ]
    fragmentation = [
        Arrival(epoch, 60, 256, "short-heavy") for epoch in range(0, 2_048, 64)
    ]
    expiry_cliff = baseline + [Arrival(256, 600, 1_024, "expiry-cliff")]
    return {
        "steady": baseline,
        "long_front_load": front_load,
        "correlated_maximum": correlated,
        "adversarial_occupation": occupation,
        "maturity_fragmentation": fragmentation,
        "expiry_cliff": expiry_cliff,
    }


def mechanisms() -> tuple[Mechanism, ...]:
    return (
        Mechanism("shared_byte_time", "byte_time"),
        Mechanism("term_premium", "term_premium"),
        Mechanism("five_maturity_lanes", "maturity_lanes"),
    )


def run_all() -> tuple[list[SimulationResult], list[dict[str, float | int | str]]]:
    results: list[SimulationResult] = []
    series: list[dict[str, float | int | str]] = []
    for scenario, arrivals in scenarios().items():
        for mechanism in mechanisms():
            result, observations = simulate(scenario, arrivals, mechanism)
            results.append(result)
            series.extend(observations)
    return results, series


def write_outputs(output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    results, series = run_all()
    summary_path = output_dir / "spot-summary.csv"
    series_path = output_dir / "spot-timeseries.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(results[0])))
        writer.writeheader()
        writer.writerows(asdict(item) for item in results)
    with series_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(series[0]))
        writer.writeheader()
        writer.writerows(series)
    return summary_path, series_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results, _ = run_all()
    if args.output_dir:
        paths = write_outputs(args.output_dir)
        print("\n".join(str(path) for path in paths))
    elif args.json:
        print(json.dumps([asdict(item) for item in results], indent=2))
    else:
        for item in results:
            print(
                f"{item.scenario:24} {item.mechanism:22} "
                f"reject={item.rejection_rate:6.1%} "
                f"coverage={item.charge_coverage:6.2f} "
                f"peak={item.peak_occupancy:6.1f}"
            )


if __name__ == "__main__":
    main()
