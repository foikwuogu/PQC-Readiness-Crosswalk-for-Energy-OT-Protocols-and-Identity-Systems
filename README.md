# PQC Readiness Crosswalk for Energy OT Protocols and Identity Systems

**Status:** Verified, v1.0 (author sign-off 2026-09-09) | **Maintainer:** Friday Ogochukwu Ikwuogu, [ORCID 0009-0009-2222-1318](https://orcid.org/0009-0009-2222-1318) | **License:** code [MIT](LICENSE), data/docs [CC BY 4.0](LICENSE-CC-BY-4.0)

A structured, standards-aligned reference for utilities, vendors, and regulators
planning the transition to post-quantum cryptography (PQC) in energy-sector
operational technology (OT). It answers one question for each protocol and
identity mechanism in scope: **which cryptographic primitives does it specify
today, what FIPS 203/204/205 primitive replaces or hybridizes with each one,
and what federal deadline, draft standard, or pending bill creates the
pressure to move?** It also ships a Cryptographic Bill of Materials (CBOM)
template so an operator can start inventorying its own cryptographic
dependencies before any sector-specific mandate exists.

Protocols covered: **DNP3, IEC 60870-5-104, ICCP/TASE.2, Modbus Security, OPC
UA, IEC 61850 (GOOSE/Sampled Values and MMS), IEEE C37.118.2 (synchrophasor)**,
plus the shared **IEC 62351-9 key-management layer** and **NERC CIP
identity/access-management** context that surrounds all of them.

## What is here

```
AUTHORS.json           single source of author/collaborator identity (see docs/CODEBOOK.md)
BUILD_SPEC.md           the one-page spec this build followed
CITATION.cff            machine-readable citation
LICENSE                 MIT (code)
LICENSE-CC-BY-4.0       CC BY 4.0 (data, CBOM template, documents)
code/                   numbered scripts, run in order (see below)
data/raw/               PROVENANCE.txt — every source cited, with URL and access date
data/processed/         crosswalk.csv, timeline.csv, qa_report.txt
cbom/                   CBOM JSON Schema, a blank CSV template, and a worked example
report/                 stats.json, figures/, and the technical report (Markdown + DOCX)
docs/                   CODEBOOK, LIMITATIONS, VERIFY_CHECKLIST, NEXT_STEPS
```

## Run it

```
pip install -r requirements.txt
npm install docx     # only needed to rebuild the .docx report
python code/00_generate_crosswalk_csv.py   # writes data/processed/crosswalk.csv
python code/01_generate_timeline_csv.py    # writes data/processed/timeline.csv
python code/02_build_stats.py              # writes report/stats.json
python code/03_qa.py                       # writes data/processed/qa_report.txt
python code/04_figures.py --final          # writes report/figures/timeline.png (pass --final for the release-ready version; omit it for a watermarked working copy)
python code/05_render_tables.py            # writes report/tables/crosswalk_table.md
node code/06_build_docx.js --final         # writes report/PQC_Readiness_Crosswalk.docx (pass --final for the release-ready version; omit it for a watermarked working copy)

# Once docs/VERIFY_CHECKLIST.md is complete and signed off:
python code/04_figures.py --final
node code/06_build_docx.js --final
python /path/to/open-project-build/scripts/publish_gate.py .   # must exit 0 before publishing
```

A stranger should be able to run these five commands from this README alone
and reproduce everything under `data/processed/` and `report/` exactly.

## Sources

See `data/raw/PROVENANCE.txt` for the full list with URLs and access dates.
Headline sources: NIST FIPS 203/204/205 (final, 2024-08-13); NIST IR 8547
(initial public draft, 2024-11-12 — **still a draft**, not final, as of this
release); Executive Order 14412 (2026-06-22); OMB Memorandum M-26-15
(2026-06-24); the Quantum-GUARD Act of 2026 (introduced 2026-08-18, not
enacted); the Modbus/TCP Security Protocol Specification v3.6 (freely
published); and secondary technical summaries of the IEC 62351 series, DNP3
Secure Authentication v6, OPC UA security profiles, and IEC 61850-90-5/IEEE
C37.118.2, since the primary IEC/IEEE standards text is copyrighted and
paywalled (see `docs/LIMITATIONS.md`, item L1).

## Headline numbers (from `report/stats.json`)

Thirteen crosswalk rows span ten named protocols/standards and twelve
cryptographic functions. Six of the thirteen rows (46%) originally carried a
review flag because an algorithm-parameter detail could not be confirmed from
a directly machine-readable primary source inside this build's sandbox; the
author has since checked each against the primary standard and signed off on
2026-09-09 — see `docs/VERIFY_CHECKLIST.md` for the record. NIST IR 8547, the roadmap every federal PQC plan
is told to align with, remains an initial public draft with no second draft
or final identified as of 2026-09-09. CISA's cryptographic-bill-of-materials
guidance for critical infrastructure, due under EO 14412 around 2026-12-19,
had not yet been published as of this build. The single hardest technical gap
identified is row 9: IEC 61850 GOOSE/Sampled-Values protection messages carry
a roughly 4 ms delivery budget that current-generation FIPS 204/205 signature
sizes may not fit without a lighter-weight scheme.

## Limitations

See `docs/LIMITATIONS.md` before using or citing anything here — in
particular, the paywalled-standards limitation (L1) and the sandbox
network-access limitation (L2) that shaped how sources were cited.

## Citation

See `CITATION.cff`. DOI: pending first Zenodo release.
