# Next steps (what v2.0 should add)

1. **Reconcile against CISA's CBOM guidance** once published (due ~2026-12-19
   under EO 14412). The current `cbom/cbom_template.schema.json` is an
   author-designed starting point, not aligned to any published federal CBOM
   schema, because none existed as of this build.
2. **Confirm NIST IR 8547's final status.** If a second draft or final
   version has issued, re-derive the timeline and any deprecation-date
   language from it rather than the initial public draft.
3. ~~Close the six review-flagged gaps with direct access to the paywalled
   primary standards (IEC 62351 series, IEEE 1815, IEC 61850-90-5, OPC UA
   Part 7) rather than secondary sources.~~ Done as of the 2026-09-09
   verification sign-off (`docs/VERIFY_CHECKLIST.md`); v2.0 should still
   re-check each if the underlying standard is revised.
4. **Add a vendor-support matrix.** This version documents what the
   standards specify; it does not yet document which specific SCADA/RTU/relay
   vendors have shipped or committed to PQC support. That is a natural v2.0
   addition once vendor roadmaps are public enough to cite.
5. **Track the Quantum-GUARD Act of 2026** through committee and floor votes;
   if enacted, add its resulting FERC/DOE deliverables as new timeline rows
   with real (not projected) dates.
6. **Pilot the CBOM template** against a real (anonymized) utility asset
   inventory to find fields that are missing or unused in practice, per the
   worked example's own caveat that six illustrative rows are not a validated
   sample.
7. **Add a machine-readable crosswalk-to-CBOM link** (a `driving_deadline_ref`
   join already exists in the CBOM schema against `timeline.csv`'s
   `event_id`; a similar join against `crosswalk.csv`'s `row_id` would let a
   filled CBOM auto-flag which crosswalk row governs each asset).
