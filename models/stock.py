"""Deterministic active-stock and expiry-ring model.

This is a non-normative executable companion to docs/01. It intentionally
models logical bytes only; a production design must check every component of
the physical resource vector.
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from typing import Iterable


FAR_FUTURE_EPOCH = -1


@dataclass
class Bucket:
    epoch: int = FAR_FUTURE_EPOCH
    bytes: int = 0


@dataclass(frozen=True)
class DataObjectMeta:
    commitment: str
    size: int
    expiry_epoch: int
    enforcement_level: str = "PROTOCOL_REQUIRED"


@dataclass(frozen=True)
class Snapshot:
    current_epoch: int
    retained_bytes: int
    expiry_queue: tuple[Bucket, ...]
    objects: tuple[DataObjectMeta, ...]


class ProtocolState:
    def __init__(
        self,
        *,
        capacity_bytes: int,
        min_retention_epochs: int,
        max_retention_epochs: int,
        allowed_retention_epochs: Iterable[int] | None = None,
    ) -> None:
        if capacity_bytes <= 0:
            raise ValueError("capacity_bytes must be positive")
        if not 0 < min_retention_epochs <= max_retention_epochs:
            raise ValueError("invalid retention bounds")

        self.capacity_bytes = capacity_bytes
        self.min_retention_epochs = min_retention_epochs
        self.max_retention_epochs = max_retention_epochs
        self.allowed_retention_epochs = (
            frozenset(allowed_retention_epochs)
            if allowed_retention_epochs is not None
            else None
        )
        self.current_epoch = 0
        self.retained_bytes = 0
        self.expiry_queue = [Bucket() for _ in range(max_retention_epochs + 1)]
        self.objects: dict[str, DataObjectMeta] = {}

    def _validate_duration(self, retention_epochs: int) -> None:
        if not self.min_retention_epochs <= retention_epochs <= self.max_retention_epochs:
            raise ValueError("retention duration outside protocol bounds")
        if (
            self.allowed_retention_epochs is not None
            and retention_epochs not in self.allowed_retention_epochs
        ):
            raise ValueError("retention duration is not an allowed maturity")

    def admit_blob(
        self,
        *,
        commitment: str,
        size: int,
        retention_epochs: int,
    ) -> DataObjectMeta:
        if not commitment or commitment in self.objects:
            raise ValueError("commitment must be non-empty and unique on this branch")
        if size <= 0:
            raise ValueError("size must be positive")
        self._validate_duration(retention_epochs)
        if self.retained_bytes + size > self.capacity_bytes:
            raise ValueError("active retained-stock capacity exceeded")

        expiry_epoch = self.current_epoch + retention_epochs
        index = expiry_epoch % len(self.expiry_queue)
        bucket = self.expiry_queue[index]
        if bucket.epoch not in (FAR_FUTURE_EPOCH, expiry_epoch):
            raise AssertionError("expiry ring collision")

        bucket.epoch = expiry_epoch
        bucket.bytes += size
        self.retained_bytes += size
        meta = DataObjectMeta(commitment, size, expiry_epoch)
        self.objects[commitment] = meta
        return meta

    def advance_to(self, epoch: int) -> None:
        if epoch < self.current_epoch:
            raise ValueError("use restore() for a reorganization")

        for next_epoch in range(self.current_epoch + 1, epoch + 1):
            index = next_epoch % len(self.expiry_queue)
            bucket = self.expiry_queue[index]
            if bucket.epoch == next_epoch:
                self.retained_bytes -= bucket.bytes
                expired = [
                    commitment
                    for commitment, meta in self.objects.items()
                    if meta.expiry_epoch == next_epoch
                ]
                for commitment in expired:
                    del self.objects[commitment]
                self.expiry_queue[index] = Bucket()
            self.current_epoch = next_epoch

    def snapshot(self) -> Snapshot:
        return Snapshot(
            current_epoch=self.current_epoch,
            retained_bytes=self.retained_bytes,
            expiry_queue=tuple(copy.deepcopy(self.expiry_queue)),
            objects=tuple(self.objects.values()),
        )

    def restore(self, snapshot: Snapshot) -> None:
        self.current_epoch = snapshot.current_epoch
        self.retained_bytes = snapshot.retained_bytes
        self.expiry_queue = list(copy.deepcopy(snapshot.expiry_queue))
        self.objects = {item.commitment: item for item in snapshot.objects}


def frontier(capacity_bytes: int, duration_hours: float) -> float:
    """Return steady-state bytes per second for capacity/duration."""
    if capacity_bytes <= 0 or duration_hours <= 0:
        raise ValueError("capacity and duration must be positive")
    return capacity_bytes / (duration_hours * 3600)


def _format_rate(bytes_per_second: float) -> str:
    units = ((2**30, "GiB/s"), (2**20, "MiB/s"), (2**10, "KiB/s"))
    for divisor, suffix in units:
        if bytes_per_second >= divisor:
            return f"{bytes_per_second / divisor:.3g} {suffix}"
    return f"{bytes_per_second:.3g} B/s"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    frontier_parser = subparsers.add_parser("frontier")
    frontier_parser.add_argument("--capacity-tib", type=float, required=True)
    frontier_parser.add_argument(
        "--durations-hours", type=float, nargs="+", required=True
    )
    args = parser.parse_args()

    if args.command == "frontier":
        capacity_bytes = int(args.capacity_tib * 2**40)
        for duration in args.durations_hours:
            print(f"{duration:g} hours\t{_format_rate(frontier(capacity_bytes, duration))}")


if __name__ == "__main__":
    main()
