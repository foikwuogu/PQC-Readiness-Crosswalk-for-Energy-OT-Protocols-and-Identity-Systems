# Verification checklist (author-completed)

## Sign-off record

**Signed off by:** Friday Ogochukwu Ikwuogu (corresponding author)
**Date:** 2026-09-09
**Statement:** Verification checklist reviewed and confirmed complete; cleared to proceed to publish.

The mechanical half of the gate is enforced by the build tooling's own
publish-readiness check (leftover draft banners, review-flag tags,
placeholders); the human half below was the author's own judgment and cannot
be scripted.

## Reproduce
- [x] Re-run `code/00_generate_crosswalk_csv.py` through `code/04_figures.py` in order; outputs match what is committed (or drift is explained)
- [x] `data/processed/qa_report.txt` still shows no FAILs
- [x] Every number in `README.md` and the technical report re-derived from `report/stats.json` after the re-run

## Source-level checks
- [x] Re-fetched each URL in `data/raw/PROVENANCE.txt`; no source found superseded (NIST IR 8547 confirmed still an initial public draft as of sign-off date)
- [x] Confirmed the Quantum-GUARD Act of 2026's status (introduced, not enacted) as of sign-off date
- [x] Confirmed CISA has not yet published its EO-14412-mandated CBOM guidance as of sign-off date

## The six previously flagged crosswalk rows (each checked against a primary source by the author)
- [x] Row 3 (DNP3 SAv6 key establishment / LESS enrollment) — confirmed against the full DNP3 SAv6 spec
- [x] Row 5 (IEC 60870-5-104 / IEC 62351-8 RBAC token signature sizing) — confirmed against IEC 62351-8 text
- [x] Row 8 (OPC UA SecurityPolicy asymmetric-algorithm parameters) — confirmed against OPC UA Part 7 (Profiles) directly
- [x] Row 9 (IEC 61850 GOOSE/SV signature algorithm + the ~4 ms latency figure) — confirmed against IEC 62351-6 and IEC 61850-5
- [x] Row 12 (IEEE C37.118.2 / IEC 61850-90-5 security mechanism) — confirmed against IEC 61850-90-5 directly
- [x] Row 13 (NERC CIP identity/access management algorithm expectations) — confirmed current NERC CIP-005/007 language names no specific algorithm

Each row's `verify_flag` column in `data/processed/crosswalk.csv` now reads
"verified 2026-09-09 (author sign-off)" in place of the earlier review tag.

## Row-level spot checks (the five named in `data/processed/qa_report.txt` §7)
- [x] FIPS 203/204/205 finalization date (2024-08-13)
- [x] Modbus/TCP Security mandatory cipher suite (TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, requirement R-14)
- [x] OMB M-26-15 TLS 1.3 deadline (2030-01-02)
- [x] GOOSE trip-message latency budget (~4 ms) against IEC 61850-5
- [x] Quantum-GUARD Act introduction date and sponsors against congress.gov

## Judgment calls (author's ruling)
- [x] Scope: identity coverage = in-protocol PKI + NERC CIP IAM context — affirmed
- [x] Scope: protocol list includes IEC 61850 and IEEE C37.118.2 beyond the five originally named — affirmed
- [x] Federal deadlines (EO 14412 / M-26-15) presented as "analogous planning targets" for energy OT — affirmed as written

## Before it goes public
- [x] README, limitations, and the technical report reviewed; nothing indefensible remains
- [x] Draft stamps removed by regenerating the figure and report with `--final`; no review-flag tag or placeholder remains anywhere in the package
- [x] `AUTHORS.json`, `CITATION.cff`, and the author block in the report all match, spelling included
- [ ] Zenodo metadata (title, creators with ORCID, license, keywords) matches `CITATION.cff` — to confirm at deposit time
