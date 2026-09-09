#!/usr/bin/env python3
"""Generate data/processed/timeline.csv from a Python list of dicts (see
00_generate_crosswalk_csv.py for why: avoids hand-quoting CSV commas)."""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed" / "timeline.csv"

FIELDS = ["event_id", "date", "instrument", "milestone", "binding_scope",
          "energy_ot_relevance", "status_as_of_2026-09-09"]

ROWS = [
    dict(event_id=1, date="2024-08-13", instrument="FIPS 203/204/205",
         milestone="NIST finalizes ML-KEM, ML-DSA, and SLH-DSA as the federal PQC algorithm standards",
         binding_scope="US federal government (all agencies); de facto global reference",
         energy_ot_relevance="Defines the target algorithms every row of the crosswalk migrates toward",
         status="Final / in force"),
    dict(event_id=2, date="2024-11-12", instrument="NIST IR 8547 (ipd)",
         milestone="Initial public draft of the PQC transition roadmap published for comment",
         binding_scope="Guidance (non-binding until finalized)",
         energy_ot_relevance="Names the deprecation timetable federal agencies (and by extension, FAR-covered vendors) will follow; energy OT has no sector-specific annex",
         status="Draft (initial public draft); comment period closed 2025-01-10, no second draft or final observed as of this build"),
    dict(event_id=3, date="2026-06-22", instrument="Executive Order 14412",
         milestone="Directs federal PQC migration; sets 30/90/180/270-day process deadlines and 2030-12-31 / 2031-12-31 outcome deadlines for high-value/high-impact federal systems",
         binding_scope="US federal government; contractor rules to follow via FAR Council",
         energy_ot_relevance="Not directly binding on utilities, but drives CISA critical-infrastructure assistance (via Sector Risk Management Agencies) and eventual contractor/vendor compliance rules that flow into energy-sector procurement",
         status="In force"),
    dict(event_id=4, date="2026-06-24", instrument="OMB M-26-15",
         milestone="Implements EO 14412 for civilian agencies: 120-day migration plan submission, TLS 1.3-or-successor by 2030-01-02, phased migration 2026-2035 (five phases)",
         binding_scope="US federal civilian agencies (explicitly excludes National Security Systems)",
         energy_ot_relevance="Federal-only, but its TLS 1.3 and phase structure is the template utilities and vendors will likely mirror voluntarily; explicitly requires agency plans to align with NIST IR 8547 'or successor document'",
         status="In force"),
    dict(event_id=5, date="~2026-12-19", instrument="CISA CBOM guidance (per EO 14412, 180 days from 2026-06-22)",
         milestone="CISA to release cryptographic bill of materials guidance for critical infrastructure owners",
         binding_scope="Guidance (critical infrastructure, incl. energy)",
         energy_ot_relevance="Directly relevant to this project's CBOM template; template should be reconciled against this guidance once published",
         status="Not yet published as of 2026-09-09 (due date has not arrived)"),
    dict(event_id=6, date="2026-08-18", instrument="Quantum-GUARD Act of 2026 (S., Coons/Rounds)",
         milestone="Would direct FERC to weigh quantum risk in grid-reliability authority, DOE to run a PQC testing environment, and DOE to study quantum risk to bulk-electric-system IT/OT",
         binding_scope="Would be binding on FERC/DOE and indirectly the bulk electric system if enacted",
         energy_ot_relevance="The only proposed instrument in this timeline that names the electric grid specifically",
         status="Introduced; not enacted -- track for status changes before citing as current"),
    dict(event_id=7, date="2027", instrument="NIST IR 8547 (projected) -- early transition phase per draft guidance",
         milestone="Early deprecation warnings for RSA/ECDH at common key sizes begin per draft roadmap language",
         binding_scope="Guidance",
         energy_ot_relevance="Utilities beginning PKI inventory (CBOM) work now will be ahead of any eventual sector mandate",
         status="Projected from draft; re-confirm against final IR 8547 before relying on specific dates"),
    dict(event_id=8, date="2030-01-02", instrument="OMB M-26-15 milestone",
         milestone="Federal systems must support TLS 1.3 or a successor version",
         binding_scope="US federal civilian agencies",
         energy_ot_relevance="Sets the interoperability floor that IEC 62351-3 TLS profiles used by 104/DNP3/ICCP will need to meet to interoperate with upgraded federal/partner endpoints",
         status="Scheduled (future)"),
    dict(event_id=9, date="2030-12-31", instrument="EO 14412 milestone",
         milestone="All federal high-value assets/high-impact systems must complete PQC migration for key establishment",
         binding_scope="US federal government",
         energy_ot_relevance="Analogous target date energy-sector planners can use for their own key-establishment (ML-KEM) migration even though not legally binding on them",
         status="Scheduled (future)"),
    dict(event_id=10, date="2031-12-31", instrument="EO 14412 milestone",
         milestone="All federal high-value assets/high-impact systems must complete PQC migration for digital signatures",
         binding_scope="US federal government",
         energy_ot_relevance="Analogous target date for ML-DSA/SLH-DSA signature migration across substation and control-center PKI",
         status="Scheduled (future)"),
    dict(event_id=11, date="2035", instrument="OMB M-26-15 Phase 5",
         milestone="Full federal PQC migration completion target",
         binding_scope="US federal civilian agencies",
         energy_ot_relevance="Outer bound for a fully PQC-migrated federal reference environment; energy OT, with its longer asset lifecycles, should expect to lag this by years absent a sector-specific mandate",
         status="Scheduled (future)"),
]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(FIELDS)
        for r in ROWS:
            w.writerow([r["event_id"], r["date"], r["instrument"], r["milestone"],
                        r["binding_scope"], r["energy_ot_relevance"], r["status"]])
    print(f"Wrote {OUT} ({len(ROWS)} rows)")


if __name__ == "__main__":
    main()
