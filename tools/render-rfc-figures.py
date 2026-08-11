"""Render the RFC's explanatory figures as dependency-free SVG files."""

from __future__ import annotations

import html
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "assets" / "figures"

INK = "#172033"
MUTED = "#667085"
GRID = "#d8dee9"
BLUE = "#2563eb"
ORANGE = "#d97706"
GREEN = "#059669"
PURPLE = "#7c3aed"
PINK = "#db2777"
PALE_BLUE = "#dbeafe"
PALE_ORANGE = "#ffedd5"
PALE_GREEN = "#dcfce7"
PALE_PURPLE = "#ede9fe"
PALE_PINK = "#fce7f3"


def start_svg(title: str, description: str, width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(title)}</title>',
        f'<desc id="desc">{html.escape(description)}</desc>',
        "<style>",
        f"text{{font-family:Inter,system-ui,sans-serif;fill:{INK}}}",
        ".title{font-size:22px;font-weight:600}.subtitle{font-size:13px}",
        ".label{font-size:13px}.small{font-size:12px}.tiny{font-size:11px}",
        f".muted{{fill:{MUTED}}}.axis{{stroke:{INK};stroke-width:1}}",
        f".grid{{stroke:{GRID};stroke-width:1}}.frame{{fill:#fff;stroke:{GRID}}}",
        "</style>",
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text class="title" x="32" y="34">{html.escape(title)}</text>',
        f'<text class="subtitle muted" x="32" y="56">{html.escape(description)}</text>',
    ]


def finish_svg(parts: list[str], output: Path) -> None:
    parts.append("</svg>")
    output.write_text("\n".join(parts) + "\n", encoding="utf-8")


def polyline(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def subscripted(symbol: str, *, sub_size: int = 10) -> str:
    if "_" not in symbol:
        return html.escape(symbol)
    base, suffix = symbol.split("_", 1)
    return f'{html.escape(base)}<tspan baseline-shift="sub" font-size="{sub_size}">{html.escape(suffix)}</tspan>'


def render_frontier() -> None:
    width, height = 1200, 520
    parts = start_svg(
        "Figure 1 — Throughput–retention frontier",
        "The same 64 TiB first-order frontier with logarithmic and linear y-axes; x is linear in both panels.",
        width,
        height,
    )
    legend_y = 84
    for x, color, label, dash in (
        (34, BLUE, "Hard frontier S/T", ""),
        (220, ORANGE, "Two-thirds operating target", ' stroke-dasharray="7 5"'),
        (472, PURPLE, "Headroom", ""),
    ):
        if label == "Headroom":
            parts.append(f'<rect x="{x}" y="{legend_y - 10}" width="20" height="10" fill="{PALE_PURPLE}"/>')
        else:
            parts.append(f'<line x1="{x}" y1="{legend_y - 5}" x2="{x + 22}" y2="{legend_y - 5}" stroke="{color}" stroke-width="3"{dash}/>')
        parts.append(f'<text class="small" x="{x + 29}" y="{legend_y}">{label}</text>')

    duration_max = 4096 * 32 * 12 / 86400
    capacity_mib = 64 * 1024 * 1024
    panels = ((44, "A. Logarithmic y-axis", True), (620, "B. Linear y-axis", False))
    plot_top, plot_w, plot_h = 130, 520, 300
    for left, panel_title, logarithmic in panels:
        parts.append(f'<text class="label" x="{left}" y="112" font-weight="600">{panel_title}</text>')
        note = "Preserves relative separation across the range." if logarithmic else "Makes the two-thirds ratio visually literal."
        parts.append(f'<text class="small muted" x="{left + 190}" y="112">{note}</text>')
        parts.append(f'<rect class="frame" x="{left}" y="{plot_top}" width="{plot_w}" height="{plot_h}"/>')

        def x_pos(days: float) -> float:
            return left + (days - 1) / (duration_max - 1) * plot_w

        def hard(days: float) -> float:
            return capacity_mib / (days * 86400)

        if logarithmic:
            y_min, y_max = 20.0, 900.0

            def y_pos(value: float) -> float:
                ratio = (math.log(value) - math.log(y_min)) / (math.log(y_max) - math.log(y_min))
                return plot_top + plot_h * (1 - ratio)

            y_ticks = (20, 50, 100, 200, 500, 800)
        else:
            y_min, y_max = 0.0, 820.0

            def y_pos(value: float) -> float:
                return plot_top + plot_h * (1 - (value - y_min) / (y_max - y_min))

            y_ticks = (0, 200, 400, 600, 800)

        for tick in y_ticks:
            y = y_pos(tick)
            parts.append(f'<line class="grid" x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}"/>')
            parts.append(f'<text class="tiny" x="{left - 9}" y="{y + 4:.1f}" text-anchor="end">{tick}</text>')
        for day in (1, 4, 7, 10, 13, 16, duration_max):
            x = x_pos(day)
            label = "18.2" if day == duration_max else str(day)
            parts.append(f'<line class="axis" x1="{x:.1f}" y1="{plot_top + plot_h}" x2="{x:.1f}" y2="{plot_top + plot_h + 5}"/>')
            parts.append(f'<text class="tiny" x="{x:.1f}" y="{plot_top + plot_h + 20}" text-anchor="middle">{label}</text>')

        data = []
        target = []
        for index in range(141):
            days = 1 + (duration_max - 1) * index / 140
            frontier = hard(days)
            data.append((x_pos(days), y_pos(frontier)))
            target.append((x_pos(days), y_pos(frontier * 2 / 3)))
        area = data + list(reversed(target))
        parts.append(f'<polygon points="{polyline(area)}" fill="{PALE_PURPLE}"/>')
        parts.append(f'<polyline points="{polyline(data)}" fill="none" stroke="{BLUE}" stroke-width="3"/>')
        parts.append(f'<polyline points="{polyline(target)}" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-dasharray="7 5"/>')
        edge_x = x_pos(duration_max)
        parts.append(f'<line x1="{edge_x:.1f}" y1="{plot_top}" x2="{edge_x:.1f}" y2="{plot_top + plot_h}" stroke="{PURPLE}" stroke-width="2"/>')
        parts.append(f'<text class="tiny" x="{edge_x - 7:.1f}" y="{plot_top + 17}" text-anchor="end">4096 epochs</text>')
        parts.append(f'<text class="small" x="{left + plot_w / 2}" y="{plot_top + plot_h + 43}" text-anchor="middle">Required-serving duration (days)</text>')
        parts.append(f'<text class="small" transform="translate({left - 35} {plot_top + plot_h / 2}) rotate(-90)" text-anchor="middle">Sustainable ingress (MiB/s)</text>')

    parts.append(f'<text class="small muted" x="32" y="500">The one-hour frontier is 18.2 GiB/s and is intentionally outside both panels.</text>')
    finish_svg(parts, OUTPUT / "figure-01-throughput-retention-frontier.svg")


def render_fixed_tail() -> None:
    width, height = 1200, 430
    parts = start_svg(
        "Figure 3 — A shorter lease removes only the fixed-system tail",
        "One fixed-size blob, identical publication burden, and two protocol serving policies.",
        width,
        height,
    )
    left, right, top, plot_h = 245, 48, 112, 210
    plot_w = width - left - right
    horizon, chosen = 18.2, 7.2

    def x_pos(days: float) -> float:
        return left + days / horizon * plot_w

    rows = (("Fixed retention", 145, horizon), ("Variable retention", 245, chosen))
    parts.append(f'<rect class="frame" x="{left}" y="{top}" width="{plot_w}" height="{plot_h}"/>')
    for label, y, duration in rows:
        parts.append(f'<text class="label" x="{left - 18}" y="{y + 21}" text-anchor="end">{label}</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{x_pos(duration) - left:.1f}" height="42" fill="{PALE_BLUE}" stroke="{BLUE}"/>')
        parts.append(f'<line x1="{left}" y1="{y - 8}" x2="{left}" y2="{y + 50}" stroke="{INK}" stroke-width="3"/>')
    parts.append(f'<rect x="{x_pos(chosen):.1f}" y="245" width="{x_pos(horizon) - x_pos(chosen):.1f}" height="42" fill="{PALE_PURPLE}" stroke="{PURPLE}" stroke-dasharray="7 5"/>')
    parts.append(f'<text class="label" x="{(x_pos(chosen) + x_pos(horizon)) / 2:.1f}" y="271" text-anchor="middle">fixed-only tail removed</text>')
    parts.append(f'<text class="small" x="{left}" y="128">same fixed-blob ingress and availability-establishment burden</text>')
    parts.append(f'<text class="small" x="{x_pos(chosen):.1f}" y="232" text-anchor="middle">chosen T</text>')
    parts.append(f'<text class="small" x="{x_pos(horizon):.1f}" y="132" text-anchor="end">H = 4096 epochs</text>')
    parts.append(f'<line class="axis" x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}"/>')
    for day in (0, 4, 8, 12, 16, horizon):
        x = x_pos(day)
        label = "18.2" if day == horizon else str(day)
        parts.append(f'<line class="axis" x1="{x:.1f}" y1="{top + plot_h}" x2="{x:.1f}" y2="{top + plot_h + 5}"/>')
        parts.append(f'<text class="tiny" x="{x:.1f}" y="{top + plot_h + 21}" text-anchor="middle">{label}</text>')
    parts.append(f'<text class="small" x="{left + plot_w / 2}" y="{top + plot_h + 48}" text-anchor="middle">Time since publication (days)</text>')
    parts.append(f'<text class="small muted" x="32" y="407">The saving is logical retained byte-time; physical implementation overhead is evaluated separately.</text>')
    finish_svg(parts, OUTPUT / "figure-03-fixed-system-tail.svg")


def render_application_lifecycle() -> None:
    width, height = 1200, 610
    parts = start_svg(
        "Figure 5 — Application examples across the data lifecycle",
        "All objects pass through mandatory hot availability; selected cold custody and external continuation differ by use case.",
        width,
        height,
    )
    left, right, top, bottom = 300, 38, 130, 65
    plot_w, plot_h = width - left - right, height - top - bottom
    hot, ethereum_end, external_start = 0.14, 0.80, 0.57

    def x_pos(value: float) -> float:
        return left + value * plot_w

    parts.append(f'<rect x="{left}" y="{top}" width="{hot * plot_w:.1f}" height="{plot_h}" fill="{PALE_BLUE}"/>')
    parts.append(f'<rect x="{x_pos(hot):.1f}" y="{top}" width="{(ethereum_end - hot) * plot_w:.1f}" height="{plot_h}" fill="{PALE_ORANGE}"/>')
    parts.append(f'<rect x="{x_pos(external_start):.1f}" y="{top}" width="{(1 - external_start) * plot_w:.1f}" height="{plot_h}" fill="{PALE_PURPLE}" fill-opacity="0.65"/>')
    parts.append(f'<rect class="frame" x="{left}" y="{top}" width="{plot_w}" height="{plot_h}" fill="none"/>')
    parts.append(f'<text class="label" x="{x_pos(hot / 2):.1f}" y="105" text-anchor="middle" font-weight="600">hot DAS</text>')
    parts.append(f'<text class="label" x="{x_pos((hot + ethereum_end) / 2):.1f}" y="105" text-anchor="middle" font-weight="600">Ethereum cold custody</text>')
    parts.append(f'<text class="label" x="{x_pos((external_start + 1) / 2):.1f}" y="84" text-anchor="middle" font-weight="600">external services may overlap</text>')

    rows = (
        ("Live-stream segment", "minimum replication opportunity", hot, False, ""),
        ("Communication", "recipient retrieval window", 0.31, False, ""),
        ("Game or social event", "recovery and synchronization", 0.46, False, ""),
        ("Public artifact or dataset", "window for mirrors to acquire", 0.62, True, "mirror or archive"),
        ("Rollup or L2 data posting", "full protocol serving horizon", ethereum_end, True, "optional L2 archive"),
    )
    row_gap, bar_h = 76, 34
    colors = (GREEN, ORANGE, PINK, GREEN, PURPLE)
    pale = (PALE_GREEN, PALE_ORANGE, PALE_PINK, PALE_GREEN, PALE_PURPLE)
    for index, (label, detail, end, continuation, continuation_label) in enumerate(rows):
        y = top + 38 + index * row_gap
        parts.append(f'<text class="label" x="{left - 18}" y="{y + 9}" text-anchor="end">{html.escape(label)}</text>')
        parts.append(f'<text class="tiny muted" x="{left - 18}" y="{y + 26}" text-anchor="end">{html.escape(detail)}</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{hot * plot_w:.1f}" height="{bar_h}" fill="{PALE_BLUE}" stroke="{BLUE}"/>')
        if end > hot:
            parts.append(f'<rect x="{x_pos(hot):.1f}" y="{y}" width="{(end - hot) * plot_w:.1f}" height="{bar_h}" fill="{pale[index]}" stroke="{colors[index]}"/>')
        parts.append(f'<line x1="{x_pos(end):.1f}" y1="{y - 5}" x2="{x_pos(end):.1f}" y2="{y + bar_h + 5}" stroke="{INK}" stroke-width="2"/>')
        if continuation:
            start = x_pos(max(hot, end - 0.035))
            parts.append(f'<line x1="{start:.1f}" y1="{y + bar_h / 2:.1f}" x2="{x_pos(1):.1f}" y2="{y + bar_h / 2:.1f}" stroke="{PURPLE}" stroke-width="5" stroke-dasharray="9 7"/>')
            parts.append(f'<text class="tiny" x="{x_pos(1) - 6:.1f}" y="{y + 9}" text-anchor="end">{html.escape(continuation_label)}</text>')
    parts.append(f'<line x1="{x_pos(hot):.1f}" y1="{top}" x2="{x_pos(hot):.1f}" y2="{top + plot_h}" stroke="{BLUE}" stroke-dasharray="6 5"/>')
    parts.append(f'<line x1="{x_pos(ethereum_end):.1f}" y1="{top}" x2="{x_pos(ethereum_end):.1f}" y2="{top + plot_h}" stroke="{PURPLE}" stroke-width="2"/>')
    parts.append(f'<text class="small" x="{x_pos(ethereum_end) - 8:.1f}" y="{top + 18}" text-anchor="end">4096 epochs</text>')
    parts.append(f'<text class="small" x="{left + plot_w / 2}" y="{height - 23}" text-anchor="middle">Conceptual lifecycle →</text>')
    finish_svg(parts, OUTPUT / "figure-05-application-lifecycle.svg")


def render_storage_model() -> None:
    width, height = 1200, 590
    parts = start_svg(
        "Figure 6 — Storage-side derivation of a proposed retention limit",
        "RFC research model; schematic and not to scale; these are not existing Ethereum protocol counters.",
        width,
        height,
    )
    left, bar_y, bar_w, bar_h = 52, 118, 1096, 118
    parts.append(f'<text class="label" x="{left}" y="99"><tspan font-weight="600">{subscripted("M_budget")}</tspan> — chosen local storage envelope in physical bytes per node</text>')
    segments = (
        (0.00, 0.23, PALE_BLUE, BLUE, "M_hot", "hot working set"),
        (0.23, 0.39, PALE_ORANGE, ORANGE, "M_repair", "repair storage slack"),
        (0.39, 0.53, PALE_GREEN, GREEN, "M_metadata", "commitments, proofs, expiry records"),
        (0.53, 1.00, PALE_PURPLE, PURPLE, "remaining physical bytes", "available to cold retention"),
    )
    for start, end, fill, stroke, label, detail in segments:
        x = left + start * bar_w
        segment_w = (end - start) * bar_w
        parts.append(f'<rect x="{x:.1f}" y="{bar_y}" width="{segment_w:.1f}" height="{bar_h}" fill="{fill}" stroke="{stroke}"/>')
        parts.append(f'<text class="label" x="{x + segment_w / 2:.1f}" y="{bar_y + 50}" text-anchor="middle" font-weight="600">{subscripted(label)}</text>')
        if label == "M_metadata":
            parts.append(f'<text class="tiny muted" x="{x + segment_w / 2:.1f}" y="{bar_y + 70}" text-anchor="middle"><tspan x="{x + segment_w / 2:.1f}">commitments, proofs,</tspan><tspan x="{x + segment_w / 2:.1f}" dy="16">expiry records</tspan></text>')
        else:
            parts.append(f'<text class="tiny muted" x="{x + segment_w / 2:.1f}" y="{bar_y + 73}" text-anchor="middle">{detail}</text>')

    formula_y = 316
    parts.append(f'<text x="52" y="{formula_y}" font-size="21" font-weight="600">{subscripted("K_storage", sub_size=13)} ≲</text>')
    numerator = f'{subscripted("M_budget")} − {subscripted("M_hot")} − {subscripted("M_repair")} − {subscripted("M_metadata")}'
    parts.append(f'<text class="label" x="360" y="{formula_y - 13}" text-anchor="middle">{numerator}</text>')
    parts.append(f'<line x1="190" y1="{formula_y - 4}" x2="530" y2="{formula_y - 4}" stroke="{INK}"/>')
    parts.append(f'<text class="label" x="360" y="{formula_y + 22}" text-anchor="middle">{subscripted("γ_cold")}</text>')
    parts.append(f'<text class="small muted" x="592" y="{formula_y - 13}">{subscripted("γ_cold")} maps one logical retained byte to its local physical</text>')
    parts.append(f'<text class="small muted" x="592" y="{formula_y + 7}">storage footprint under the chosen custody representation.</text>')

    gate_y = 402
    parts.append(f'<line class="grid" x1="52" y1="{gate_y - 35}" x2="1148" y2="{gate_y - 35}"/>')
    parts.append(f'<text class="label" x="52" y="{gate_y - 10}" font-weight="600">Storage is only one admission constraint</text>')
    gates = (
        (52, BLUE, "K_storage", "resident bytes"),
        (248, ORANGE, "K_serve", "historical serving bandwidth"),
        (444, GREEN, "K_repair", "repair bandwidth"),
        (640, PINK, "K_I/O", "write and expiry churn"),
    )
    for x, color, label, detail in gates:
        parts.append(f'<text class="label" x="{x + 72}" y="{gate_y + 25}" text-anchor="middle" font-weight="600">{subscripted(label)}</text>')
        parts.append(f'<text class="tiny muted" x="{x + 72}" y="{gate_y + 46}" text-anchor="middle">{detail}</text>')
        parts.append(f'<line x1="{x}" y1="{gate_y + 64}" x2="{x + 144}" y2="{gate_y + 64}" stroke="{color}" stroke-width="4"/>')
    parts.append(f'<text x="824" y="{gate_y + 43}" font-size="22">→</text>')
    parts.append(f'<text class="label" x="1000" y="{gate_y + 25}" text-anchor="middle" font-weight="600">admission decision</text>')
    parts.append(f'<text class="tiny muted" x="1000" y="{gate_y + 46}" text-anchor="middle">must remain inside every resource bound</text>')
    parts.append(f'<line x1="884" y1="{gate_y + 64}" x2="1116" y2="{gate_y + 64}" stroke="{INK}" stroke-width="4"/>')
    parts.append(f'<text class="small muted" x="52" y="555">{subscripted("K_storage")} is the storage-derived component; the full safe envelope also includes serving, repair, and I/O limits.</text>')
    finish_svg(parts, OUTPUT / "figure-06-storage-admission-model.svg")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    render_frontier()
    render_fixed_tail()
    render_application_lifecycle()
    render_storage_model()
    for path in sorted(OUTPUT.glob("figure-*.svg")):
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
