#!/usr/bin/env python3
"""Build report/figures/timeline.png from data/processed/timeline.csv.

Palette per the dataviz skill's reference instance (categorical slots, fixed
order, chart chrome). Pass --final to remove the DRAFT stamp (only after the
verification gate passes).
"""
import argparse
import csv
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parents[1]
timeline_path = ROOT / "data" / "processed" / "timeline.csv"
out_path = ROOT / "report" / "figures" / "timeline.png"

# dataviz skill reference palette (light mode)
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"
SURFACE = "#fcfcfb"
SLOT_BLUE = "#2a78d6"     # in force / final
SLOT_ORANGE = "#eb6834"   # not yet published / due
SLOT_AQUA = "#1baf7a"     # scheduled (future)
SLOT_YELLOW = "#eda100"   # draft
SLOT_VIOLET = "#4a3aa7"   # pending legislation

STATUS_COLOR = {
    "Final / in force": SLOT_BLUE,
    "In force": SLOT_BLUE,
    "Draft (initial public draft); comment period closed 2025-01-10, no second draft or final observed as of this build": SLOT_YELLOW,
    "Not yet published as of 2026-09-09 (due date has not arrived)": SLOT_ORANGE,
    "Introduced; not enacted -- track for status changes before citing as current": SLOT_VIOLET,
    "Projected from draft; re-confirm against final IR 8547 before relying on specific dates": SLOT_YELLOW,
    "Scheduled (future)": SLOT_AQUA,
}
LEGEND = [
    ("In force / final", SLOT_BLUE),
    ("Draft / projected from draft", SLOT_YELLOW),
    ("Guidance not yet published", SLOT_ORANGE),
    ("Pending legislation", SLOT_VIOLET),
    ("Scheduled (future)", SLOT_AQUA),
]


def parse_date(s):
    s = s.lstrip("~")
    parts = s.split("-")
    if len(parts) == 1:
        return date(int(parts[0]), 6, 1)
    if len(parts) == 2:
        return date(int(parts[0]), int(parts[1]), 1)
    return date(int(parts[0]), int(parts[1]), int(parts[2]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--final", action="store_true", help="remove DRAFT stamp")
    args = ap.parse_args()

    with open(timeline_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    rows.sort(key=lambda r: parse_date(r["date"]))
    dates = [parse_date(r["date"]) for r in rows]
    labels = [f"{r['instrument']}\n{r['milestone'][:58]}{'...' if len(r['milestone'])>58 else ''}" for r in rows]
    colors = [STATUS_COLOR.get(r["status_as_of_2026-09-09"], INK_MUTED) for r in rows]

    fig, ax = plt.subplots(figsize=(12, 8.3), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    y_positions = list(range(len(rows)))
    ax.hlines(y_positions, [dates[0]] * len(rows), dates, color=GRIDLINE, linewidth=1, zorder=1)
    ax.scatter(dates, y_positions, color=colors, s=90, zorder=3, edgecolors=SURFACE, linewidths=1.5)

    for y, d, r in zip(y_positions, dates, rows):
        ax.text(mdates.date2num(d) + 25, y, f"  {r['date']}  —  {r['instrument']}",
                 va="center", ha="left", fontsize=9, color=INK_PRIMARY)

    ax.set_yticks(y_positions)
    ax.set_yticklabels([])
    ax.tick_params(axis="y", left=False)
    ax.set_ylim(len(rows) + 0.6, -1.8)
    ax.set_xlim(dates[0] - (dates[-1] - dates[0]) * 0.02, dates[-1] + (dates[-1] - dates[0]) * 0.34)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color(BASELINE)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.tick_params(axis="x", colors=INK_SECONDARY, labelsize=10)
    ax.grid(axis="x", color=GRIDLINE, linewidth=0.8, zorder=0)

    fig.suptitle("Federal PQC mandate and draft-guidance timeline, 2024–2035",
                  fontsize=14, color=INK_PRIMARY, x=0.01, ha="left", fontweight="bold", y=0.99)
    fig.text(0.01, 0.955, "Vintage: sources accessed 2026-09-09 — see data/processed/timeline.csv",
              fontsize=8.5, color=INK_MUTED, ha="left")

    handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c, markersize=9, label=lbl)
               for lbl, c in LEGEND]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, -0.06), ncol=3,
              frameon=False, fontsize=8.5, labelcolor=INK_SECONDARY)

    if not args.final:
        ax.text(0.5, 0.5, "DRAFT", transform=ax.transAxes, fontsize=60, color=INK_MUTED,
                alpha=0.15, ha="center", va="center", rotation=30, zorder=0)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(rect=[0, 0.03, 1, 0.93])
    fig.savefig(out_path, facecolor=SURFACE, bbox_inches="tight")
    print(f"Wrote {out_path} (final={args.final})")


if __name__ == "__main__":
    main()
