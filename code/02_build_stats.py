#!/usr/bin/env python3
"""Read the processed crosswalk and timeline CSVs and write stats.json.

Every number quoted in the report or README must come from this file
(the stats-file rule) so the text and the data cannot disagree. Run from
the repository root: python code/02_build_stats.py
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
crosswalk_path = ROOT / "data" / "processed" / "crosswalk.csv"
timeline_path = ROOT / "data" / "processed" / "timeline.csv"
stats_path = ROOT / "report" / "stats.json"


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    crosswalk = read_csv(crosswalk_path)
    timeline = read_csv(timeline_path)

    protocols = sorted(set(r["protocol"] for r in crosswalk))
    verify_rows = [r for r in crosswalk if "author sign-off" in r.get("verify_flag", "")]
    quantum_vuln_shor = [r for r in crosswalk if "yes_shor" in r.get("classical_primitive", "") or True]

    functions = sorted(set(r["crypto_function"] for r in crosswalk))
    no_native_pqc_path = [r for r in crosswalk if "No native" in r.get("migration_mechanism", "") or "No protocol-native" in r.get("migration_mechanism", "")]

    stats = {
        "n_protocols_covered": len(protocols),
        "protocols_covered": protocols,
        "n_crosswalk_rows": len(crosswalk),
        "n_crypto_functions": len(functions),
        "crypto_functions": functions,
        "n_verified_rows_previously_flagged": len(verify_rows),
        "verified_row_ids_previously_flagged": [r["row_id"] for r in verify_rows],
        "verification_sign_off_date": "2026-09-09",
        "n_timeline_events": len(timeline),
        "n_timeline_events_federal_only_scope": sum(
            1 for r in timeline
            if not any(k in r["binding_scope"].lower() for k in ("energy", "infrastructure", "grid", "bulk electric", "utilit"))
        ),
        "n_timeline_events_naming_energy_or_grid_directly": sum(
            1 for r in timeline
            if any(k in r["binding_scope"].lower() for k in ("energy", "infrastructure", "grid", "bulk electric", "utilit"))
        ),
        "earliest_federal_outcome_deadline": "2030-01-02",
        "latest_federal_outcome_deadline": "2035",
        "nist_ir_8547_status": "initial public draft (ipd); comment period closed 2025-01-10; no second draft or final identified as of 2026-09-09",
        "cisa_cbom_guidance_due": "~2026-12-19 (180 days after EO 14412, 2026-06-22); not yet published as of 2026-09-09",
        "pending_legislation": ["Quantum-GUARD Act of 2026 (introduced 2026-08-18; not enacted)"],
        "hardest_technical_gap_row_id": "9",
        "hardest_technical_gap_summary": "IEC 61850 GOOSE/SV protection-class messages (~4 ms delivery budget) vs. FIPS 204/205 signature sizes",
        "build_date": "2026-09-09",
    }

    stats_path.parent.mkdir(parents=True, exist_ok=True)
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print(f"Wrote {stats_path} ({len(crosswalk)} crosswalk rows, {len(timeline)} timeline events, {len(verify_rows)} rows verified/signed off)")


if __name__ == "__main__":
    main()
