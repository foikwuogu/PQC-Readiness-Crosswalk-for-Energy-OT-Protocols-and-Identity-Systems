# Codebook

## `data/processed/crosswalk.csv`

| Column | Definition | Source / transformation |
|---|---|---|
| `row_id` | Row identifier, referenced from `docs/VERIFY_CHECKLIST.md`, `BUILD_SPEC.md`, and the report. | Assigned sequentially. |
| `protocol` | The energy-OT protocol or shared standard this row describes. | As named in the build spec's scope. |
| `security_standard` | The specific standard/part/version defining the cryptographic mechanism. | Cited from the source in `source_id`. |
| `crypto_function` | The cryptographic role: authentication, bulk encryption/integrity, key establishment/enrollment, key distribution, application authentication (+access control), message integrity + authentication, transport signature + key exchange, or identity governance. | Assigned by the author/build to match the unit of analysis in `BUILD_SPEC.md`. |
| `classical_primitive` | The algorithm(s) specified or commonly deployed today. | Extracted from the cited source; where a source gives a range of vendor practice rather than a fixed mandate, this is noted in the cell text. |
| `pqc_replacement` | The FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), or FIPS 205 (SLH-DSA) primitive expected to replace or hybridize with the classical one. | Author's analysis, informed by NIST IR 8547 (draft) and general PQC-migration literature (TLS 1.3 hybrid key exchange, composite certificates). |
| `migration_mechanism` | How the swap is expected to land in practice. | Author's analysis. |
| `driving_deadline` | Which mandate, draft, or bill creates the pressure, and its date. | Cross-referenced against `data/processed/timeline.csv`. |
| `ot_specific_constraint` | Why energy OT differs from generic federal IT for this row. | Author's analysis, grounded in publicly documented OT characteristics (serial/narrowband links, fixed-firmware legacy devices, multi-decade asset life, real-time/latency budgets). |
| `verify_flag` | Records the review history for a row. Six rows originally carried a review tag where an algorithm/parameter detail could not be confirmed from a directly machine-readable primary source inside this build's sandbox (see `docs/LIMITATIONS.md`, L2); those six now read "verified 2026-09-09 (author sign-off)" following the author's check against the primary standard. Empty otherwise. | Set during the build; updated by the author during the verification gate (see `docs/VERIFY_CHECKLIST.md`). |
| `source_id` | Foreign key into `data/raw/PROVENANCE.txt`. | — |

## `data/processed/timeline.csv`

| Column | Definition |
|---|---|
| `event_id` | Sequential identifier. |
| `date` | ISO 8601 date, or a bare year for a multi-year phase target. A `~` prefix marks a computed/approximate date (e.g., "180 days from X"). |
| `instrument` | The legal or guidance instrument (EO, OMB memo, FIPS, NIST IR, a bill). |
| `milestone` | What the instrument requires or establishes at this date. |
| `binding_scope` | Who the instrument legally binds. |
| `energy_ot_relevance` | Why this federal-scope (mostly) instrument matters to energy OT even where it does not bind utilities directly. |
| `status_as_of_2026-09-09` | The instrument's status as of the build date — final/in force, draft, introduced-not-enacted, not yet published, or scheduled/future. Re-check before relying on this column past the build date. |

## `cbom/cbom_template.schema.json` and `cbom/cbom_example_filled.csv`

See the `description` field on each property in the JSON Schema — every CBOM
field is documented inline there rather than duplicated here, so the schema
stays the single source of truth. `cbom/cbom_example_filled.csv` shows six
worked rows across a substation gateway, a protection relay, a control-center
ICCP server, a root CA, and a synchrophasor unit, chosen to include an easy
case, a hard case (the GOOSE/SV relay, echoing crosswalk row 9), and a case
with no protocol-native algorithm at all (the PMU, echoing crosswalk row 12).

## `report/stats.json`

Every field is computed directly from `crosswalk.csv` and `timeline.csv` by
`code/02_build_stats.py` — see that script for the exact computation behind
each key. No number in `README.md` or the technical report is typed by hand;
all are interpolated from this file.
