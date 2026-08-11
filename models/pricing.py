"""Competing retention-accounting benchmarks.

None of these functions is a recommended fee mechanism. They make the pricing
hypotheses in docs/01 comparable without coupling the RFC's resource claim to
one formula.
"""

from __future__ import annotations

import argparse
import json
import math


DEFAULT_MATURITIES = (256.0, 512.0, 1_024.0, 2_048.0, 4_096.0)
DEFAULT_REFERENCE_DURATION = 1_024.0


def utilization_price(utilization: float, base_price: float) -> float:
    if not 0 <= utilization < 1:
        raise ValueError("utilization must be in [0, 1)")
    return base_price / (1 - utilization)


def null_byte_time(
    *, size: float, duration: float, utilization: float, base_price: float
) -> float:
    return size * duration * utilization_price(utilization, base_price)


def convex_duration(
    *,
    size: float,
    duration: float,
    utilization: float,
    base_price: float,
    reference_duration: float,
    exponent: float = 1.5,
) -> float:
    if reference_duration <= 0 or exponent < 1:
        raise ValueError("invalid convex-duration parameters")
    premium = max(1.0, (duration / reference_duration) ** (exponent - 1))
    return null_byte_time(
        size=size,
        duration=duration,
        utilization=utilization,
        base_price=base_price,
    ) * premium


def quantized_maturity(
    *,
    size: float,
    duration: float,
    utilization: float,
    base_price: float,
    maturities: tuple[float, ...],
) -> float:
    maturity = next((item for item in sorted(maturities) if item >= duration), None)
    if maturity is None:
        raise ValueError("duration exceeds the longest maturity")
    return null_byte_time(
        size=size,
        duration=maturity,
        utilization=utilization,
        base_price=base_price,
    )


def expected_scarcity(
    *,
    size: float,
    duration: float,
    utilization: float,
    base_price: float,
    expected_utilization_at_expiry: float,
) -> float:
    current = utilization_price(utilization, base_price)
    future = utilization_price(expected_utilization_at_expiry, base_price)
    average_price = (current + future) / 2
    return size * duration * average_price


def auction_reserve_proxy(
    *, size: float, duration: float, reserve_price_per_byte_time: float
) -> float:
    """Reserve-price floor only; a real auction determines the clearing price."""
    return size * duration * reserve_price_per_byte_time


def compare(
    *,
    size: float,
    duration: float,
    utilization: float,
    base_price: float,
    reference_duration: float = DEFAULT_REFERENCE_DURATION,
    maturities: tuple[float, ...] = DEFAULT_MATURITIES,
    expected_utilization_at_expiry: float | None = None,
) -> dict[str, float]:
    if expected_utilization_at_expiry is None:
        expected_utilization_at_expiry = utilization
    return {
        "null_byte_time": null_byte_time(
            size=size,
            duration=duration,
            utilization=utilization,
            base_price=base_price,
        ),
        "convex_duration": convex_duration(
            size=size,
            duration=duration,
            utilization=utilization,
            base_price=base_price,
            reference_duration=reference_duration,
        ),
        "quantized_maturity": quantized_maturity(
            size=size,
            duration=duration,
            utilization=utilization,
            base_price=base_price,
            maturities=maturities,
        ),
        "expected_scarcity": expected_scarcity(
            size=size,
            duration=duration,
            utilization=utilization,
            base_price=base_price,
            expected_utilization_at_expiry=expected_utilization_at_expiry,
        ),
        "auction_reserve_proxy": auction_reserve_proxy(
            size=size,
            duration=duration,
            reserve_price_per_byte_time=base_price,
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=float, required=True)
    parser.add_argument("--duration-epochs", dest="duration", type=float, required=True)
    parser.add_argument("--utilization", type=float, required=True)
    parser.add_argument("--base-price", type=float, default=1.0)
    parser.add_argument(
        "--reference-duration-epochs",
        dest="reference_duration",
        type=float,
        default=DEFAULT_REFERENCE_DURATION,
    )
    parser.add_argument(
        "--maturities-epochs",
        dest="maturities",
        type=float,
        nargs="+",
        default=DEFAULT_MATURITIES,
    )
    parser.add_argument(
        "--expected-utilization-at-expiry",
        type=float,
        default=None,
    )
    args = parser.parse_args()
    numeric = [
        value
        for value in vars(args).values()
        if value is not None and not isinstance(value, (list, tuple))
    ]
    numeric.extend(args.maturities)
    if not all(math.isfinite(value) for value in numeric):
        raise ValueError("all inputs must be finite")
    arguments = vars(args)
    arguments["maturities"] = tuple(arguments["maturities"])
    print(json.dumps(compare(**arguments), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
