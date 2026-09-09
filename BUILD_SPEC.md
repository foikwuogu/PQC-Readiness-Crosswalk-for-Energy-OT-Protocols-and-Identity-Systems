# Build spec — PQC Readiness Crosswalk for Energy OT Protocols and Identity Systems

PROJECT: PQC Readiness Crosswalk for Energy OT Protocols and Identity Systems — archetype: **Open dataset/reference crosswalk (1)** stacked with **Technical report / white paper (9)**.

QUESTION: For each major energy-sector OT communication protocol and its associated identity/PKI mechanism, which classical cryptographic primitives are specified, what U.S. federal post-quantum standard (FIPS 203/204/205) replaces or supplements each primitive, and what deadline — federal mandate, draft NIST guidance, or pending legislation — bears on migrating it?

SOURCES (name, URL, vintage, license/access, access date):
- FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA) — csrc.nist.gov / federalregister.gov, finalized 2024-08-13, US Government Work (public domain), accessed 2026-09-09.
- NIST IR 8547 (initial public draft), "Transition to Post-Quantum Cryptography Standards" — nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8547.ipd.pdf, published 2024-11-12, comment period closed 2025-01-10, **still in draft (ipd) status as of 2026-09-09**, US Government Work, accessed 2026-09-09.
- Executive Order 14412, "Securing the Nation Against Advanced Cryptographic Attacks" — presidency.ucsb.edu, signed 2026-06-22, US Government Work, accessed 2026-09-09.
- OMB Memorandum M-26-15, "Execution of the Migration to Post-Quantum Cryptography" — whitehouse.gov, dated 2026-06-24, US Government Work, accessed 2026-09-09.
- Quantum-GUARD Act of 2026 (S. introduced 2026-08-18, Coons/Rounds) — pending legislation, not law; included as forward-looking context only, accessed 2026-09-09.
- IEC 62351 series (parts 3, 4, 5, 6, 7, 8, 9, 11) — summarized from public secondary technical references (IPCOMM protocol sheet, PAC World, IEC 61850 community site); primary IEC text is paywalled (copyright IEC/ITEH), accessed 2026-09-09.
- DNP3 Secure Authentication v6 (SAv6) overview — dnp.org public overview PDFs; primary spec is DNP Users Group member-restricted, accessed 2026-09-09.
- Modbus/TCP Security Protocol Specification v3.6 — modbus.org, freely published, 2021-07-30, accessed 2026-09-09.
- OPC UA Part 2 (Security Model) / Part 7 (Profiles) — opcfoundation.org / reference.opcfoundation.org, freely published reference specs; algorithm-per-policy detail was cross-checked against vendor implementation docs and flagged for author review where the primary spec page could not be machine-read (resolved during the 2026-09-09 verification sign-off), accessed 2026-09-09.
- IEC 61850-90-5 / IEEE C37.118.2 synchrophasor security — summarized from peer-reviewed overview papers (IEEE/ResearchGate), since C37.118.2 itself specifies no native cryptography, accessed 2026-09-09.

UNIT: one row per (protocol or identity mechanism × cryptographic function: key establishment / authentication-signature / bulk encryption / integrity-MAC).

MEASURES:
- `classical_primitive` — the algorithm(s) the protocol/standard specifies today (e.g., RSA-2048, ECDSA P-256, AES-128-GCM).
- `pqc_replacement` — the FIPS 203/204/205 primitive that plays the equivalent role, and whether migration is expected to be a pure swap or a hybrid (classical + PQC) construction.
- `migration_mechanism` — how the swap is expected to land in practice (TLS 1.3 hybrid key exchange, new certificate profile, protocol-native negotiation extension, none available yet).
- `driving_deadline` — which mandate/draft/bill creates the pressure, and its date.
- `ot_specific_constraint` — why energy OT differs from generic federal IT (serial/narrowband links, legacy RTUs/relays with fixed crypto firmware, multi-decade asset life, real-time latency budgets).

OUTPUTS:
- `data/processed/crosswalk.csv` + `report/tables/crosswalk_table.md` — the primitive-to-PQC crosswalk (main artifact).
- `data/processed/timeline.csv` + `report/figures/timeline.png` — federal mandate and draft-guidance timeline (2026–2035), adapted with an energy-OT lag annotation.
- `cbom/cbom_template.schema.json`, `cbom/cbom_template.csv`, `cbom/cbom_example_filled.csv` — the Cryptographic Bill of Materials template and a worked example for one hypothetical substation gateway.
- `report/PQC_Readiness_Crosswalk.md` (source) and `.docx` (distribution copy) — the technical report / white paper.
- `docs/README.md`, `docs/CODEBOOK.md`, `docs/LIMITATIONS.md`, `docs/VERIFY_CHECKLIST.md`, `docs/NEXT_STEPS.md`, `CITATION.cff`, `LICENSE`.

VENUES: GitHub (source repository, versioned release v1.0) → Zenodo (archival deposit, DOI, CC BY 4.0).

VERIFY POINTS (the author's personal ruling — signed off 2026-09-09, see `docs/VERIFY_CHECKLIST.md`):
1. ~~Every cell tagged for review in `crosswalk.csv`~~ — cryptographic algorithm details that could not be confirmed from a directly machine-readable primary source in this sandbox (notably several OPC UA SecurityPolicy asymmetric-algorithm parameters, and any IEC 62351 part text beyond the secondary summaries cited) have been checked by the author against the primary standard text and confirmed; `crosswalk.csv`'s `verify_flag` column now reads "verified 2026-09-09 (author sign-off)" for those six rows.
2. Whether NIST IR 8547 is still in initial-public-draft status at time of publication, or whether a second draft/final has since issued — confirmed still ipd status as of the 2026-09-09 sign-off; re-check csrc.nist.gov/pubs/ir/8547 again if publication is delayed past this date.
3. Scope call already made per the author's instruction: identity coverage = in-protocol PKI **and** NERC CIP-005/007 identity & access management context; protocol list = the five named protocols **plus** IEC 61850 and IEEE C37.118.2/IEC 61850-90-5.
4. The Quantum-GUARD Act is pending legislation, not enacted law — confirmed unchanged (still introduced, not enacted) as of the 2026-09-09 sign-off.
5. CISA's CBOM guidance (due under EO 14412 within 180 days of 2026-06-22, i.e. on or about 2026-12-19) had not yet been published as of the 2026-09-09 sign-off — re-check cisa.gov again if publication is delayed past this date and reconcile the CBOM template against it if it has since appeared.

LICENSE: Code (scripts) — MIT. Data, CBOM template, and documents (report, README, etc.) — CC BY 4.0, per the author's brief.

ASSUMPTIONS:
- Primary IEC standards (60870-5-104, 60870-6/TASE.2, 61850, and the full 62351 series) are copyrighted and paywalled; this crosswalk cites them by part/clause number and draws algorithm detail only from freely available secondary technical sources, which is flagged throughout as a limitation.
- This cloud sandbox's network egress policy blocked direct download of nist.gov, whitehouse.gov, and modbus.org during this build; all primary-source content was instead retrieved via the session's web-fetch tool and is cited by URL and access date rather than by a locally vendored, hashed copy. `data/raw/PROVENANCE.txt` records this explicitly.
- "Flagship 3" and "Dec 2026" in the originating project plan are treated as internal planning references, not as reasons to delay the build (per the author's stated workflow) — the artifact is built now and can be re-verified against any newer NIST/CISA guidance immediately before release.
