#!/usr/bin/env node
/* Build report/PQC_Readiness_Crosswalk.docx from structured content.
 * Mirrors report/PQC_Readiness_Crosswalk.md. Run: node code/06_build_docx.js [--final]
 */
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  ImageRun, PageBreak, ExternalHyperlink,
} = require("docx");

const FINAL = process.argv.includes("--final");
const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "report", "PQC_Readiness_Crosswalk.docx");
const TIMELINE_PNG = path.join(ROOT, "report", "figures", "timeline.png");

const PAGE_WIDTH = 12240, PAGE_HEIGHT = 15840; // US Letter, DXA

function p(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 160 },
    children: [new TextRun({ text, ...opts })],
  });
}
function h(text, level) {
  return new Paragraph({ heading: level, spacing: { before: 280, after: 120 }, children: [new TextRun({ text, bold: true })] });
}
function link(text, url) {
  return new ExternalHyperlink({ link: url, children: [new TextRun({ text, style: "Hyperlink" })] });
}
function mixed(parts) {
  // parts: array of {text, bold?, url?}
  const children = parts.map((part) => {
    if (part.url) return link(part.text, part.url);
    return new TextRun({ text: part.text, bold: !!part.bold, italics: !!part.italics });
  });
  return new Paragraph({ spacing: { after: 160 }, children });
}

const draftBanner = FINAL ? [] : [
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 300 },
    shading: { type: ShadingType.CLEAR, color: "auto", fill: "FDECC8" },
    children: [new TextRun({ text: "DRAFT — unverified. Remove this banner only after docs/VERIFY_CHECKLIST.md is complete.", bold: true, color: "8A5A00" })],
  }),
];

const titleBlock = [
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [new TextRun({ text: "PQC Readiness Crosswalk for Energy OT Protocols and Identity Systems", bold: true, size: 32 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [
    new TextRun({ text: "Friday Ogochukwu Ikwuogu", bold: true }), new TextRun({ text: "¹* · " }),
    new TextRun({ text: "Abidemi Orimogunje" }), new TextRun({ text: "² · " }),
    new TextRun({ text: "Eria Othieno Pinyi" }), new TextRun({ text: "³ · " }),
    new TextRun({ text: "David Mike-Ewewie" }), new TextRun({ text: "⁴" }),
  ]}),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new TextRun({ text: "¹ Independent Researcher, Odessa, Texas, USA", size: 18 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new TextRun({ text: "² Electrical and Electronic Engineering Department, Redeemer's University, Ede, Osun State, Nigeria", size: 18 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new TextRun({ text: "³ Computer Science and Engineering Department, University of Fairfax, USA", size: 18 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: "⁴ Computer Science Department, University of Texas Permian Basin, Odessa, Texas, USA", size: 18 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [
    new TextRun({ text: "*Corresponding author.", size: 18 }),
  ]}),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [
    new TextRun({ text: "ORCID: ", size: 18 }),
    link("0009-0009-2222-1318", "https://orcid.org/0009-0009-2222-1318"),
  ]}),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [
    new TextRun({ text: "Email: ", size: 18 }),
    link("Friday.ikwuogu@gmail.com", "mailto:Friday.ikwuogu@gmail.com"),
  ]}),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [
    new TextRun({ text: "Affiliation: Independent Researcher, Odessa, Texas, USA", size: 18 }),
  ]}),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 }, children: [
    new TextRun({ text: "License: CC BY 4.0  ·  Version 1.0.0  ·  Date 2026-09-09  ·  DOI: pending (Zenodo)", size: 18, color: "52514E" }),
  ]}),
];

function summaryTable() {
  const csvPath = path.join(ROOT, "data", "processed", "crosswalk.csv");
  const raw = fs.readFileSync(csvPath, "utf-8").trim().split("\n");
  // naive CSV parse sufficient here since generator script quotes properly and we only need 4 cols
  const { parse } = require("./simple_csv.js");
  const rows = parse(raw.join("\n"));
  const header = rows[0];
  const idx = (name) => header.indexOf(name);
  const cols = ["row_id", "protocol", "classical_primitive", "pqc_replacement", "verify_flag"];
  const widths = [500, 2400, 3600, 3600, 700]; // DXA, sums to 10800 (7.5in body)
  const headLabels = ["#", "Protocol", "Classical primitive", "PQC replacement", "Flag"];

  const headerRow = new TableRow({
    tableHeader: true,
    children: headLabels.map((label, i) => new TableCell({
      width: { size: widths[i], type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, color: "auto", fill: "E1E0D9" },
      children: [new Paragraph({ children: [new TextRun({ text: label, bold: true, size: 18 })] })],
    })),
  });

  const dataRows = rows.slice(1).filter(r => r.length > 1).map((r) => new TableRow({
    children: cols.map((c, i) => new TableCell({
      width: { size: widths[i], type: WidthType.DXA },
      children: [new Paragraph({ children: [new TextRun({ text: String(r[idx(c)] || "").slice(0, 220), size: 16 })] })],
    })),
  }));

  return new Table({
    width: { size: 10800, type: WidthType.DXA },
    columnWidths: widths,
    rows: [headerRow, ...dataRows],
  });
}

const sections = [];

sections.push(...draftBanner, ...titleBlock);

sections.push(h("Abstract", HeadingLevel.HEADING_1));
sections.push(p(
  "The National Institute of Standards and Technology (NIST) finalized its first three post-quantum cryptography (PQC) standards -- FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), and FIPS 205 (SLH-DSA) -- on 2024-08-13. In 2026, Executive Order 14412 and OMB Memorandum M-26-15 set concrete migration deadlines for the U.S. federal government, and a companion NIST roadmap (NIST IR 8547) has circulated in draft since late 2024. None of this activity has a sector-specific counterpart for energy operational technology (OT): the protocols that move data between substations, control centers, and protection relays -- DNP3, IEC 60870-5-104, ICCP/TASE.2, Modbus Security, OPC UA, IEC 61850, and IEEE C37.118.2 -- were designed around classical cryptography (RSA, ECC, AES, SHA-2) with no PQC migration path defined in any of their governing standards as of this writing."
));
sections.push(p(
  "This report crosswalks the cryptographic primitives specified across seven energy-OT protocols and their shared identity infrastructure against the FIPS 203-205 replacements, identifies which federal instrument creates near-term pressure on each, and supplies a Cryptographic Bill of Materials (CBOM) template utilities can use to start their own inventory before any sector mandate exists. Thirteen crosswalk rows are documented; six originally carried a review flag pending the author's confirmation against primary standards text unavailable inside this build's research environment, and the author has since confirmed each against the primary standard and signed off on 2026-09-09 (docs/VERIFY_CHECKLIST.md). The single hardest technical gap identified is IEC 61850 GOOSE/Sampled-Values protection messaging, whose roughly 4 millisecond delivery budget may not accommodate current-generation PQC signature sizes without a lighter-weight scheme."
));

sections.push(h("1. Introduction", HeadingLevel.HEADING_1));
sections.push(p(
  "Energy-sector operational technology is being asked to absorb a cryptographic transition it did not design for and that its governing standards do not yet describe. The transition is real and dated: FIPS 203, 204, and 205 are final federal standards, not proposals, and the White House's mid-2026 executive actions put hard 2030 and 2031 deadlines on federal high-value asset migration. What is missing is the connective tissue between that federal timeline and the specific, decades-old protocols that carry telemetry, protection, and control traffic across the grid. This report is that connective tissue: a row-by-row crosswalk from protocol-specified cryptographic primitive, to PQC replacement, to the mechanism by which that replacement is likely to be deployed, to the deadline that makes it urgent, to the operational constraint that makes energy OT different from a typical federal IT system."
));
sections.push(p(
  "The crosswalk covers two things the originating project brief asked for explicitly, and two the author confirmed as in scope during this build: named protocols (DNP3, IEC 60870-5-104, ICCP/TASE.2, Modbus Security, OPC UA) and their governing security standard (chiefly the IEC 62351 series); and, per the author's instruction, an expanded protocol set adding IEC 61850 and IEEE C37.118.2, plus an identity-systems scope covering both in-protocol PKI mechanisms and NERC CIP-005/007/004 identity and access-management context."
));

sections.push(h("2. Methodology and scope", HeadingLevel.HEADING_1));
sections.push(p(
  "The crosswalk's unit of analysis is one row per (protocol or shared identity mechanism) x (cryptographic function): key establishment, authentication/signature, bulk encryption, integrity/MAC, key management and distribution, or identity governance. For each row, the build spec (BUILD_SPEC.md) specifies five measures, defined precisely in docs/CODEBOOK.md: the classical primitive in force today, the PQC replacement, the migration mechanism, the driving deadline, and the OT-specific constraint that distinguishes this row from a generic federal-IT migration."
));
sections.push(p(
  "Primary sources for the federal PQC framework -- FIPS 203/204/205, NIST IR 8547, EO 14412, and OMB M-26-15 -- were retrieved and are cited by URL and access date in data/raw/PROVENANCE.txt. Primary sources for the energy-OT protocols themselves are, in several cases, copyrighted and paywalled (the full IEC 62351 series, IEC 61850, IEC 60870-5-104/60870-6, and IEEE 1815); where that was true, this crosswalk cites the standard by part and clause number but draws algorithm-level detail from freely available secondary technical sources and flagged the row for review so the author -- who has direct professional and academic access to these standards -- could confirm it, which the author has since done, signing off on 2026-09-09. docs/LIMITATIONS.md documents this and six other limitations in full; a reader without access to the primary standards used for that check may still wish to re-confirm independently."
));

sections.push(h("3. The crosswalk", HeadingLevel.HEADING_1));
sections.push(p("The full thirteen-row table lives in data/processed/crosswalk.csv (also rendered at report/tables/crosswalk_table.md). A condensed view is reproduced below; see the CSV for the complete migration-mechanism and OT-specific-constraint text.", { italics: true }));
sections.push(summaryTable());
sections.push(new Paragraph({ spacing: { before: 200 }, children: [] }));

const protocolParas = [
  ["DNP3 (rows 1-3)", "already uses AES-256-GCM for its authenticated encryption, which is not broken by Shor's algorithm and needs no replacement -- only its key-establishment step (a \"Low-Entropy Shared Secret\" enrollment mechanism in Secure Authentication v6) needs a PQC-hybrid upgrade via FIPS 203 (ML-KEM). The practical obstacle is that DNP3 masters and outstations are frequently serial-only remote terminal units (RTUs) with fixed firmware and service lives measured in decades, so ML-KEM's roughly 1-1.5 KB key material may not fit assumptions baked into narrowband serial framing."],
  ["IEC 60870-5-104 and ICCP/TASE.2 (rows 4-6, 10)", "both rely on IEC 62351-3's TLS profile and, for ICCP/TASE.2 and IEC 61850's MMS services, IEC 62351-4's application-layer \"SECURE\" association. Both are natural candidates for TLS 1.3 hybrid key-exchange groups paired with FIPS 204 (ML-DSA) or composite certificates. The operational bottleneck is not cryptographic but logistical: rotating certificates across thousands of RTUs and gateways, and -- for ICCP, which crosses utility and balancing-authority trust boundaries -- coordinating that rotation bilaterally between organizations that do not share a PKI today."],
  ["Modbus Security (row 7)", "is the one protocol in this crosswalk whose security specification is freely published (Modbus Organization, modbussecurityprotocol.pdf, v3.6). It mandates TLS 1.2 or better with a specific cipher suite (TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256) and mutual X.509 authentication. A PQC migration here is comparatively well-specified in principle -- a new IANA-registered hybrid ciphersuite plus updated certificates -- but Modbus masters are often simple PLCs and gateways with a minimal TLS stack footprint that may not accept a firmware upgrade in place."],
  ["OPC UA (row 8)", "is, by deployment volume, probably the highest-leverage single target in this crosswalk: it is the protocol of choice for new SCADA/historian and IT/OT-boundary integrations across the sector. Its current SecurityPolicies rely on RSA signatures and RSA-OAEP key transport; a PQC-capable successor policy naming ML-KEM/ML-DSA would need to be defined centrally by the OPC Foundation. This row was originally flagged for author review because this build's research tooling could not extract the exact per-policy algorithm table from the OPC Foundation's JavaScript-rendered reference pages; the values reported were cross-checked against vendor documentation and have since been confirmed directly against OPC UA Part 7 (Profiles) by the author as part of the 2026-09-09 sign-off."],
  ["IEC 61850 GOOSE/Sampled Values (row 9)", "is the hardest technical problem in this report. Protection-class GOOSE trip messages carry a widely cited delivery-time budget on the order of 4 milliseconds. FIPS 204 (ML-DSA) signatures run roughly 2.4-4.6 KB depending on parameter set, and FIPS 205 (SLH-DSA) signatures are larger still -- both dramatically larger than the ECDSA signatures IEC 62351-6 deployments use today. Fitting a PQC signature into that timing budget is not solved by any published revision of IEC 62351-6 as of this writing; the authors believe this is the one row in the crosswalk where protocol-level engineering research, not just a certificate and cipher-suite swap, is the open problem."],
  ["IEEE C37.118.2 / synchrophasor data (row 12)", "specifies no cryptography of its own; when secured at all, it is wrapped by IEC 61850-90-5 (HMAC/RSA-based protection modeled on GOOSE/SMV) or by an external TLS/IPsec tunnel. Given that no protocol-native PQC path exists, the pragmatic near-term mitigation for phasor measurement unit (PMU) links is the external tunnel, secured with the same TLS 1.3-hybrid approach recommended for IEC 60870-5-104 and ICCP above -- a case the CBOM worked example (Section 5) illustrates directly."],
  ["IEC 62351-9 key management (row 11)", "is, in the authors' assessment, the single point of highest leverage across the entire crosswalk: it is the shared GDOI/IKEv2-based key-distribution layer underneath IEC 62351-3, -4, -5, -6, and -8. A utility's PKI hierarchy is typically a small number of root and issuing certificate authorities, a far more tractable upgrade target than the thousands of field devices those CAs ultimately serve. Sequencing a PQC pilot here first is this report's central practical recommendation."],
  ["NERC CIP identity and access management (row 13)", "currently leaves algorithm choice to the implementing utility's own PKI and names no required algorithm in CIP-005, CIP-007, or CIP-004. No NERC-mandated PQC migration path exists; the Quantum-GUARD Act of 2026, introduced 2026-08-18 by Senators Coons and Rounds but not yet enacted, would direct the Federal Energy Regulatory Commission to consider quantum-computing risk within its grid-reliability authority -- a plausible future path to a NERC CIP revision, but not a current one."],
];
for (const [lead, rest] of protocolParas) {
  sections.push(new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: lead + " ", bold: true }), new TextRun({ text: rest })] }));
}

sections.push(h("4. The federal timeline and what it means for energy OT", HeadingLevel.HEADING_1));
sections.push(p(
  "Figure 1 plots eleven milestones from 2024 through 2035 across five instruments: FIPS 203/204/205 (final), NIST IR 8547 (still an initial public draft, with no second draft or final identified as of 2026-09-09), Executive Order 14412 (signed 2026-06-22), OMB M-26-15 (dated 2026-06-24), and the introduced-but-not-enacted Quantum-GUARD Act of 2026. None of the federal deadlines binds a utility or vendor directly -- OMB M-26-15 explicitly limits itself to federal civilian agencies and excludes National Security Systems -- but two mechanisms carry the pressure sector-ward regardless: FAR Council contractor-compliance rulemaking directed by EO 14412 (due on 180- and 270-day tracks from 2026-06-22), which will eventually reach any vendor selling into federal critical-infrastructure programs; and CISA's own EO-14412-mandated cryptographic-bill-of-materials guidance for critical infrastructure owners, due on or about 2026-12-19 and not yet published as of this report."
));

if (fs.existsSync(TIMELINE_PNG)) {
  const imgBuf = fs.readFileSync(TIMELINE_PNG);
  sections.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 80 },
    children: [new ImageRun({ data: imgBuf, type: "png", transformation: { width: 580, height: 401 } })],
  }));
  sections.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [new TextRun({ text: "Figure 1. Federal PQC mandate and draft-guidance timeline, 2024-2035. Source: data/processed/timeline.csv.", italics: true, size: 18, color: "52514E" })],
  }));
}

sections.push(p(
  "Treating the federal outcome dates -- 2030-12-31 for key establishment, 2031-12-31 for digital signatures -- as analogous planning targets rather than binding requirements is this report's suggested framing for utility planners: energy OT's multi-decade asset lifecycles make it likely the sector will lag the federal timeline by years absent its own mandate, and planning against the federal dates now is the only way to avoid lagging by more than that."
));

sections.push(h("5. The CBOM template", HeadingLevel.HEADING_1));
sections.push(p(
  "cbom/cbom_template.schema.json defines a flat, spreadsheet-friendly cryptographic inventory record -- asset identity, protocol, cryptographic function, algorithm and key size, quantum-vulnerability classification, intended PQC replacement, vendor support status, and the utility's own migration status -- deliberately scoped to be filled in today, ahead of any published federal CBOM standard. cbom/cbom_example_filled.csv works through six illustrative rows: a substation gateway's key-establishment and authentication dependencies, a protection relay's GOOSE/SV signature (echoing the row 9 latency problem, marked for vendor engagement rather than self-remediation), a control-center ICCP server already piloting a hybrid key exchange, a root certificate authority (marked as the highest-priority target), and a synchrophasor unit with no native cryptography of its own -- illustrating that a real CBOM sometimes records the tunnel carrying a protocol's traffic as the actual unit of migration."
));

sections.push(h("6. Recommendations", HeadingLevel.HEADING_1));
sections.push(mixed([{ text: "For utilities: ", bold: true }, { text: "begin a CBOM inventory now, prioritized by the sequencing argument in Section 3 -- the PKI/CA layer first, then TLS-capable gateways and servers, then constrained field devices last. Track CISA's forthcoming CBOM guidance (due ~2026-12-19) and reconcile rather than restart. Treat the 2030/2031 federal outcome dates as planning targets even though they do not bind the sector directly." }]));
sections.push(mixed([{ text: "For vendors: ", bold: true }, { text: "OPC UA and Modbus Security are the two protocols where a PQC-capable path is most clearly specifiable today, and where shipping support ahead of a mandate is a genuine competitive differentiator. IEC 61850 GOOSE/SV is the protocol most in need of dedicated standards-committee engineering work on lightweight PQC signatures before a credible migration path exists at all." }]));
sections.push(mixed([{ text: "For standards bodies and regulators: ", bold: true }, { text: "IEC 62351-6, IEC 62351-8, DNP3 Secure Authentication, and IEC 61850-90-5 currently name no PQC algorithm; each would need a formal revision to do so. NERC CIP likewise names no algorithm. The Quantum-GUARD Act of 2026, if enacted, would be the first instrument to put the bulk electric system's IT/OT quantum risk under a specific federal study mandate and is worth tracking closely." }]));

sections.push(h("7. Limitations", HeadingLevel.HEADING_1));
sections.push(p(
  "See docs/LIMITATIONS.md for the complete, numbered list (L1-L7), covering: reliance on secondary sources for paywalled IEC/IEEE standards (L1); this build's sandboxed network access, which required citation-by-URL rather than a locally hashed source copy (L2); the analytical, not-yet-standards-confirmed nature of every pqc_replacement and migration_mechanism cell (L3); the non-binding nature of the federal deadlines cited throughout (L4); the unverified provenance of the ~4 ms GOOSE latency figure (L5); scope choices confirmed with the author rather than independently derived (L6); and this document's nature as a versioned snapshot rather than a live-maintained feed (L7)."
));

sections.push(h("8. Conclusion", HeadingLevel.HEADING_1));
sections.push(p(
  "Post-quantum cryptography is no longer a research topic for the U.S. federal government -- it is a standard, a signed executive order, and a funded OMB migration plan with 2030 and 2031 deadlines. It is still, as of this writing, a research topic for energy-sector operational technology, where not one governing protocol standard names a PQC algorithm and the sector's own transition roadmap (NIST IR 8547) remains in draft. This crosswalk is offered as a starting reference for closing that gap: a row-by-row map from what each protocol specifies today to what it will need tomorrow, a CBOM template to start the inventory that any migration depends on, and an honest accounting -- six flagged rows, seven documented limitations -- of exactly where this v1.0 reference still needs the reader's own verification before it is relied upon."
));

sections.push(h("Acknowledgments", HeadingLevel.HEADING_2));
sections.push(p(
  "The authors thank no external funding source for this work. AI assistance (Claude, Anthropic) was used for source retrieval, data structuring, figure generation, and drafting mechanics under the corresponding author's direction and verification; all analytic judgments, the crosswalk's classifications, and every cited fact remain the authors' responsibility, subject to the verification gate documented in docs/VERIFY_CHECKLIST.md."
));

sections.push(h("References", HeadingLevel.HEADING_2));
sections.push(p(
  "Full citations with URLs and access dates are maintained in data/raw/PROVENANCE.txt to keep this reference list machine-checkable against what was actually retrieved. Headline sources: NIST FIPS 203, FIPS 204, FIPS 205 (2024); NIST IR 8547 (initial public draft, 2024); Executive Order 14412 (2026); OMB Memorandum M-26-15 (2026); Quantum-GUARD Act of 2026 (introduced, S., Coons/Rounds); Modbus Organization, Modbus/TCP Security Protocol Specification v3.6 (2021); OPC Foundation, OPC UA Part 2 (Security Model) and Part 7 (Profiles); DNP Users Group, DNP3 Secure Authentication v6 overview materials; IEC 62351 series (cited by part; summarized from secondary technical sources per Limitation L1)."
));

const doc = new Document({
  sections: [{
    properties: { page: { size: { width: PAGE_WIDTH, height: PAGE_HEIGHT }, margin: { top: 1080, bottom: 1080, left: 1260, right: 1260 } } },
    children: sections,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log(`Wrote ${OUT} (${(buf.length / 1024).toFixed(0)} KB, final=${FINAL})`);
});
