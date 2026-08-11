"""Deterministic active-stock model with slot-derived lease expiry.

This is a non-normative executable companion to docs/01. It models logical
bytes only. Service expiry and conservative capacity reclamation are separate;
a production design must also check every physical resource-vector component.
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from typing import Iterable


SECONDS_PER_SLOT = 12
SLOTS_PER_EPOCH = 32
SECONDS_PER_EPOCH = SECONDS_PER_SLOT * SLOTS_PER_EPOCH


@dataclass(frozen=True)
class DataObjectMeta:
    object_id: str
    commitment: str
    size: int
    inclusion_slot: int
    expiry_slot: int
    reclaim_after_slot: int
    service_profile_id: str = "peerdas-level1-v1"
    enforcement_level: str = "PROTOCOL_REQUIRED"


@dataclass(frozen=True)
class Snapshot:
    current_slot: int
    retained_bytes: int
    accounted_bytes: int
    next_object_ordinal: int
    objects: tuple[DataObjectMeta, ...]


class ProtocolState:
    def __init__(
        self,
        *,
        capacity_bytes: int,
        min_retention_epochs: int,
        max_retention_epochs: int,
        allowed_retention_epochs: Iterable[int] | None = None,
        reclamation_grace_slots: int = 0,
    ) -> None:
        if capacity_bytes <= 0:
            raise ValueError("capacity_bytes must be positive")
        if not 0 < min_retention_epochs <= max_retention_epochs:
            raise ValueError("invalid retention bounds")
        if reclamation_grace_slots < 0:
            raise ValueError("reclamation_grace_slots must be non-negative")

        self.capacity_bytes = capacity_bytes
        self.min_retention_epochs = min_retention_epochs
        self.max_retention_epochs = max_retention_epochs
        self.allowed_retention_epochs = (
            frozenset(allowed_retention_epochs)
            if allowed_retention_epochs is not None
            else None
        )
        self.reclamation_grace_slots = reclamation_grace_slots
        self.current_slot = 0
        self.retained_bytes = 0
        self.accounted_bytes = 0
        self._next_object_ordinal = 0
        self.objects: dict[str, DataObjectMeta] = {}

    @property
    def current_epoch(self) -> int:
        return self.current_slot // SLOTS_PER_EPOCH

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
        blob_index: int = 0,
        service_profile_id: str = "peerdas-level1-v1",
    ) -> DataObjectMeta:
        if not commitment:
            raise ValueError("commitment must be non-empty")
        if blob_index < 0:
            raise ValueError("blob_index must be non-negative")
        if size <= 0:
            raise ValueError("size must be positive")
        if not service_profile_id:
            raise ValueError("service_profile_id must be non-empty")
        self._validate_duration(retention_epochs)
        if self.accounted_bytes + size > self.capacity_bytes:
            raise ValueError("active retained-stock capacity exceeded")

        inclusion_slot = self.current_slot
        expiry_slot = inclusion_slot + retention_epochs * SLOTS_PER_EPOCH
        reclaim_after_slot = expiry_slot + self.reclamation_grace_slots
        object_id = (
            f"slot:{inclusion_slot}:ordinal:{self._next_object_ordinal}:"
            f"blob:{blob_index}:commitment:{commitment}"
        )
        self._next_object_ordinal += 1

        meta = DataObjectMeta(
            object_id=object_id,
            commitment=commitment,
            size=size,
            inclusion_slot=inclusion_slot,
            expiry_slot=expiry_slot,
            reclaim_after_slot=reclaim_after_slot,
            service_profile_id=service_profile_id,
        )
        self.retained_bytes += size
        self.accounted_bytes += size
        self.objects[object_id] = meta
        return meta

    def advance_to_slot(self, slot: int) -> None:
        if slot < self.current_slot:
            raise ValueError("use restore() for a reorganization")

        self.current_slot = slot
        self.retained_bytes = sum(
            meta.size for meta in self.objects.values() if slot < meta.expiry_slot
        )
        self.accounted_bytes = sum(
            meta.size
            for meta in self.objects.values()
            if slot < meta.reclaim_after_slot
        )
        self.objects = {
            object_id: meta
            for object_id, meta in self.objects.items()
            if slot < meta.reclaim_after_slot
        }

    def advance_to(self, epoch: int) -> None:
        """Advance to an epoch boundary; retained for the original model API."""
        if epoch < self.current_epoch:
            raise ValueError("use restore() for a reorganization")
        self.advance_to_slot(epoch * SLOTS_PER_EPOCH)

    def snapshot(self) -> Snapshot:
        return Snapshot(
            current_slot=self.current_slot,
            retained_bytes=self.retained_bytes,
            accounted_bytes=self.accounted_bytes,
            next_object_ordinal=self._next_object_ordinal,
            objects=tuple(copy.deepcopy(tuple(self.objects.values()))),
        )

    def restore(self, snapshot: Snapshot) -> None:
        self.current_slot = snapshot.current_slot
        self.retained_bytes = snapshot.retained_bytes
        self.accounted_bytes = snapshot.accounted_bytes
        self._next_object_ordinal = snapshot.next_object_ordinal
        self.objects = {item.object_id: item for item in copy.deepcopy(snapshot.objects)}


def frontier(capacity_bytes: int, duration_epochs: float) -> float:
    """Return steady-state bytes per second for capacity/epoch duration."""
    if capacity_bytes <= 0 or duration_epochs <= 0:
        raise ValueError("capacity and duration must be positive")
    return capacity_bytes / (duration_epochs * SECONDS_PER_EPOCH)


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
    frontier_parser.add_argument("--durations-epochs", type=int, nargs="+", required=True)
    args = parser.parse_args()

    if args.command == "frontier":
        capacity_bytes = int(args.capacity_tib * 2**40)
        for duration in args.durations_epochs:
            days = duration * SECONDS_PER_EPOCH / 86_400
            print(
                f"{duration:,} epochs (~{days:.3g} days)\t"
                f"{_format_rate(frontier(capacity_bytes, duration))}"
            )


if __name__ == "__main__":
    main()
