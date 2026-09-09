# Limitations

Numbered so they can be referenced from `README.md`, the report, and future
verification notes. Written before any conclusions were drafted, per the
build standard, so the report cannot outrun what is listed here.

**L1 — Primary IEC/IEEE standards text was not accessed; secondary sources were used instead.**
IEC 60870-5-104, IEC 60870-6 (ICCP/TASE.2), IEC 61850, and the full IEC 62351
series are copyrighted and sold by IEC/ITEH; IEEE 1815 (DNP3 secure
authentication) is likewise a paid IEEE standard, with the DNP Users Group
restricting the full SAv6 spec to members. This crosswalk cites these
standards by part/clause number but draws algorithm-level detail only from
freely available secondary technical sources (vendor documentation, protocol
organization overview PDFs, academic overview papers, and community technical
references). Six of thirteen crosswalk rows were originally flagged for
review on this basis; the author has since checked each against the primary
standard and signed off on 2026-09-09 — see `docs/VERIFY_CHECKLIST.md` for
the record. A reader without access to the primary standards used for that
check may still wish to re-confirm independently.

**L2 — This build's cloud sandbox could not download nist.gov, whitehouse.gov, or modbus.org directly.**
The sandbox's outbound network policy returned HTTP 403 on direct connection
attempts to these hosts during this build (2026-09-09). All primary-source
content cited from these domains was instead retrieved through the build
session's web-fetch tool, which was not subject to the same block, and is
cited by URL and access date in `data/raw/PROVENANCE.txt` rather than by a
locally vendored, cryptographically hashed copy of the source file. This is a
weaker provenance guarantee than the project's own standard (see
`BUILD_SPEC.md`) calls for, and it is disclosed here rather than silently
worked around.

**L3 — "PQC replacement" and "migration mechanism" columns are analysis, not settled standards.**
As of this build, no IEC 62351 part, no DNP3 SAv6 revision, and no OPC UA
SecurityPolicy has been published naming a specific PQC algorithm. Every cell
in `pqc_replacement` and `migration_mechanism` is the author's reasoned
projection of how the FIPS 203/204/205 algorithms are likely to be integrated,
informed by the general TLS/PKI PQC-migration literature (hybrid key
exchange, composite certificates) rather than by an energy-OT-specific
standard that does not yet exist. This is stated plainly in the crosswalk's
column definitions (`docs/CODEBOOK.md`) and should not be read as an
announced vendor or standards-body roadmap.

**L4 — Federal PQC deadlines (EO 14412, OMB M-26-15) are not binding on the energy sector.**
They bind U.S. federal civilian agencies. This crosswalk uses them as the
best available forward-looking reference points because no energy-sector-
specific PQC mandate exists yet; the Quantum-GUARD Act of 2026, the one
instrument that names the electric grid directly, was introduced but not
enacted as of this build. Any statement in the report that treats a federal
deadline as an energy-sector planning target says so explicitly and should
not be read as a compliance requirement.

**L5 — The GOOSE/SV latency-budget figure (row 9) is a commonly cited industry figure, not a single controlling clause.**
The "~4 ms" protection-class delivery requirement is widely cited in IEC
61850 literature (performance class P1) but was not independently verified
against a purchased copy of IEC 61850-5 during this build. The author should
confirm the exact figure and its applicability before the report cites it as
a hard constraint rather than an illustrative one.

**L6 — Scope choices were made per the author's explicit instruction, not independently derived.**
"Identity systems" in the project title is interpreted to include both
in-protocol PKI mechanisms and NERC CIP-005/007/004 identity and
access-management context; the protocol list was expanded from the five
named in the original project brief to include IEC 61850 and IEEE C37.118.2.
Both choices were confirmed with the author during the build (see the
clarifying-question exchange preceding `BUILD_SPEC.md`) rather than assumed.

**L7 — This is a v1.0 reference crosswalk, not a live-maintained feed.**
Federal PQC guidance is moving quickly (two new instruments — EO 14412 and
M-26-15 — issued within three months of each other in mid-2026, and NIST IR
8547 has been in draft for nearly two years). Anyone relying on this crosswalk
for a decision with real consequences should re-check `data/raw/PROVENANCE.txt`'s
cited URLs for newer versions before acting, not assume this document has
kept pace.
