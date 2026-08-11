"""Illustrative bounded controller for DA service-procurement prices.

This model is deliberately non-normative. It exposes one feedback equation for
simulation; it does not solve capacity qualification, Sybil resistance, market
power, or protocol parameter selection.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import inf, isfinite


@dataclass(frozen=True)
class ControllerParameters:
    """Bounds for one posted-price update."""

    kappa: float
    max_step: float
    floor: float = 0.0
    ceiling: float = inf

    def validate(self) -> None:
        if not isfinite(self.kappa) or self.kappa < 0:
            raise ValueError("kappa must be finite and non-negative")
        if not isfinite(self.max_step) or not 0 <= self.max_step <= 1:
            raise ValueError("max_step must be finite and between zero and one")
        if not isfinite(self.floor) or self.floor < 0:
            raise ValueError("floor must be finite and non-negative")
        if self.ceiling != inf and not isfinite(self.ceiling):
            raise ValueError("ceiling must be finite or positive infinity")
        if self.ceiling < self.floor:
            raise ValueError("ceiling must be at least floor")


def update_posted_price(
    price: float,
    qualified_supply: float,
    target_supply: float,
    parameters: ControllerParameters,
) -> float:
    """Return one bounded update of the illustrative posted price.

    The unbounded multiplier is
    ``1 + kappa * (target_supply - qualified_supply) / target_supply``.
    ``max_step`` bounds its movement around one before the absolute floor and
    ceiling are applied.
    """

    parameters.validate()
    if not isfinite(price) or price < 0:
        raise ValueError("price must be finite and non-negative")
    if not isfinite(qualified_supply) or qualified_supply < 0:
        raise ValueError("qualified_supply must be finite and non-negative")
    if not isfinite(target_supply) or target_supply <= 0:
        raise ValueError("target_supply must be finite and positive")

    shortage_fraction = (target_supply - qualified_supply) / target_supply
    raw_multiplier = 1 + parameters.kappa * shortage_fraction
    bounded_multiplier = min(
        1 + parameters.max_step,
        max(1 - parameters.max_step, raw_multiplier),
    )
    candidate = price * bounded_multiplier
    return min(parameters.ceiling, max(parameters.floor, candidate))
