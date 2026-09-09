#!/usr/bin/env python3
"""Render data/processed/crosswalk.csv as a formatted Markdown table at
report/tables/crosswalk_table.md, so the report can reference one file
instead of duplicating the CSV by hand."""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
src = ROOT / "data" / "processed" / "crosswalk.csv"
out = ROOT / "report" / "tables" / "crosswalk_table.md"

COLS = ["row_id", "protocol", "security_standard", "crypto_function",
        "classical_primitive", "pqc_replacement", "driving_deadline", "verify_flag"]
HEADERS = ["#", "Protocol", "Security standard", "Crypto function",
           "Classical primitive", "PQC replacement", "Driving deadline", "Flag"]


def main():
    with open(src, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    lines = ["| " + " | ".join(HEADERS) + " |",
             "|" + "---|" * len(HEADERS)]
    for r in rows:
        cells = [r[c].replace("|", "/").replace("\n", " ") for c in COLS]
        lines.append("| " + " | ".join(cells) + " |")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "# Crosswalk table (full detail in data/processed/crosswalk.csv)\n\n"
        + "\n".join(lines) + "\n"
    )
    print(f"Wrote {out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
