"""Render dependency-free SVG charts from normalized spot-model CSV output."""

from __future__ import annotations

import argparse
import csv
import html
from pathlib import Path


SERIES = (
    ("shared_byte_time", "Shared byte-time", "#2563eb"),
    ("term_premium", "Term premium", "#d97706"),
    ("five_maturity_lanes", "Five maturity lanes", "#059669"),
)

SCENARIO_LABELS = {
    "steady": "Steady",
    "long_front_load": "Long front-load",
    "correlated_maximum": "Correlated maximum",
    "adversarial_occupation": "Adversarial occupation",
    "maturity_fragmentation": "Maturity fragmentation",
    "expiry_cliff": "Expiry cliff",
}


def _svg_start(title: str, description: str, width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f"<title id=\"title\">{html.escape(title)}</title>",
        f"<desc id=\"desc\">{html.escape(description)}</desc>",
        "<style>text{font-family:system-ui,sans-serif;fill:#111827}"
        ".axis{stroke:#6b7280;stroke-width:1}.grid{stroke:#e5e7eb;stroke-width:1}"
        ".label{font-size:12px}.small{font-size:11px}.title{font-size:18px;font-weight:600}"
        ".legend{font-size:12px}</style>",
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text class="title" x="64" y="28">{html.escape(title)}</text>',
    ]


def _legend(parts: list[str], x: int, y: int) -> None:
    cursor = x
    for _, label, color in SERIES:
        parts.append(f'<rect x="{cursor}" y="{y - 10}" width="12" height="12" fill="{color}"/>')
        parts.append(f'<text class="legend" x="{cursor + 17}" y="{y}">{label}</text>')
        cursor += 175


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def render_grouped_bars(
    rows: list[dict[str, str]],
    *,
    metric: str,
    title: str,
    y_label: str,
    output: Path,
    percent: bool = False,
    reference: float | None = None,
) -> None:
    width, height = 1_080, 480
    left, right, top, bottom = 72, 24, 72, 110
    plot_w, plot_h = width - left - right, height - top - bottom
    values = [float(row[metric]) for row in rows]
    y_max = max(max(values) * 1.15, reference or 0, 0.01)
    if reference == 1.0:
        y_max = max(y_max, 1.35)
    scenarios = list(SCENARIO_LABELS)
    group_w = plot_w / len(scenarios)
    bar_w = group_w * 0.2
    parts = _svg_start(title, f"Grouped comparison of {y_label} across synthetic RFC stress scenarios.", width, height)
    _legend(parts, left, 52)

    for step in range(6):
        value = y_max * step / 5
        y = top + plot_h - value / y_max * plot_h
        parts.append(f'<line class="grid" x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}"/>')
        label = f"{value:.0%}" if percent else f"{value:.2f}"
        parts.append(f'<text class="small" text-anchor="end" x="{left - 8}" y="{y + 4:.1f}">{label}</text>')

    if reference is not None:
        y = top + plot_h - reference / y_max * plot_h
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" stroke="#111827" stroke-dasharray="5 4"/>')
        parts.append(f'<text class="small" x="{left + plot_w - 4}" y="{y - 5:.1f}" text-anchor="end">coverage = 1</text>')

    lookup = {(row["scenario"], row["mechanism"]): float(row[metric]) for row in rows}
    for s_index, scenario in enumerate(scenarios):
        center = left + group_w * (s_index + 0.5)
        for m_index, (mechanism, _, color) in enumerate(SERIES):
            value = lookup[(scenario, mechanism)]
            x = center + (m_index - 1) * bar_w - bar_w / 2
            y = top + plot_h - value / y_max * plot_h
            bar_h = top + plot_h - y
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" fill="{color}"/>')
            label = f"{value:.0%}" if percent else f"{value:.2f}"
            parts.append(f'<text class="small" text-anchor="middle" x="{x + bar_w / 2:.1f}" y="{max(top + 11, y - 5):.1f}">{label}</text>')
        parts.append(f'<text class="small" text-anchor="middle" x="{center:.1f}" y="{top + plot_h + 20}">{SCENARIO_LABELS[scenario]}</text>')

    parts.append(f'<line class="axis" x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}"/>')
    parts.append(f'<text class="label" text-anchor="middle" transform="translate(18 {top + plot_h / 2}) rotate(-90)">{html.escape(y_label)}</text>')
    parts.append("</svg>")
    output.write_text("\n".join(parts), encoding="utf-8")


def render_occupancy(rows: list[dict[str, str]], output: Path) -> None:
    selected = ("long_front_load", "adversarial_occupation", "expiry_cliff")
    width, height = 1_080, 770
    left, right, top = 72, 24, 78
    panel_h, gap = 190, 42
    plot_w = width - left - right
    parts = _svg_start(
        "Active stock under three stress cases",
        "Active retained stock over epochs for shared byte-time, term-premium, and five partitioned maturity lanes.",
        width,
        height,
    )
    _legend(parts, left, 52)

    for panel, scenario in enumerate(selected):
        y0 = top + panel * (panel_h + gap)
        subset = [row for row in rows if row["scenario"] == scenario]
        x_max = max(int(row["epoch"]) for row in subset)
        parts.append(f'<text class="label" x="{left}" y="{y0 - 8}">{SCENARIO_LABELS[scenario]}</text>')
        for step in range(5):
            value = 1_000 * step / 4
            y = y0 + panel_h - value / 1_000 * panel_h
            parts.append(f'<line class="grid" x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}"/>')
            parts.append(f'<text class="small" text-anchor="end" x="{left - 8}" y="{y + 4:.1f}">{value:.0f}</text>')
        for mechanism, _, color in SERIES:
            series = sorted(
                (row for row in subset if row["mechanism"] == mechanism),
                key=lambda row: int(row["epoch"]),
            )
            points = []
            for row in series:
                x = left + int(row["epoch"]) / x_max * plot_w
                y = y0 + panel_h - float(row["occupancy"]) / 1_000 * panel_h
                points.append(f"{x:.1f},{y:.1f}")
            dash = ' stroke-dasharray="7 4"' if mechanism == "term_premium" else ""
            parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2"{dash} points="{" ".join(points)}"/>')
        parts.append(f'<line class="axis" x1="{left}" y1="{y0 + panel_h}" x2="{left + plot_w}" y2="{y0 + panel_h}"/>')
        for step in range(5):
            epoch = x_max * step / 4
            x = left + plot_w * step / 4
            parts.append(f'<text class="small" text-anchor="middle" x="{x:.1f}" y="{y0 + panel_h + 18}">{epoch:.0f}</text>')
        parts.append(f'<text class="small" text-anchor="middle" x="{left + plot_w / 2}" y="{y0 + panel_h + 34}">Epoch</text>')

    parts.append(f'<text class="label" text-anchor="middle" transform="translate(18 {height / 2}) rotate(-90)">Active stock (normalized capacity units)</text>')
    parts.append("</svg>")
    output.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=Path("models/output"))
    parser.add_argument("--output-dir", type=Path, default=Path("models/output"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary = _read_csv(args.input_dir / "spot-summary.csv")
    timeseries = _read_csv(args.input_dir / "spot-timeseries.csv")
    render_grouped_bars(
        summary,
        metric="rejection_rate",
        title="Admission failures under normalized stress",
        y_label="Rejected requested bytes",
        output=args.output_dir / "rejection-rate.svg",
        percent=True,
    )
    render_grouped_bars(
        summary,
        metric="charge_coverage",
        title="Upfront charge versus realized scarcity",
        y_label="Charge / ex-post scarcity benchmark",
        output=args.output_dir / "charge-coverage.svg",
        reference=1.0,
    )
    render_occupancy(timeseries, args.output_dir / "stress-occupancy.svg")
    for name in ("rejection-rate.svg", "charge-coverage.svg", "stress-occupancy.svg"):
        print(args.output_dir / name)


if __name__ == "__main__":
    main()
