#!/usr/bin/env python3
"""Generate data/processed/crosswalk.csv from a Python list of dicts.

Written this way (rather than hand-quoting a CSV) so commas inside free-text
cells can never silently misalign columns. Source content matches
BUILD_SPEC.md / data/raw/PROVENANCE.txt citations.
"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed" / "crosswalk.csv"

FIELDS = [
    "row_id", "protocol", "security_standard", "crypto_function",
    "classical_primitive", "pqc_replacement", "migration_mechanism",
    "driving_deadline", "ot_specific_constraint", "verify_flag", "source_id",
]

ROWS = [
    dict(row_id=1, protocol="DNP3", security_standard="IEC 62351-5 (application-layer auth for IEC 60870-5 family incl. DNP3)",
         crypto_function="authentication",
         classical_primitive="Pre-shared symmetric keys (HMAC-SHA-1/SHA-256 challenge-response, legacy SAv2/v5)",
         pqc_replacement="FIPS 204 (ML-DSA) for cert-based auth where SAv6 adopts asymmetric identity; FIPS 203 (ML-KEM) for any key-establishment step",
         migration_mechanism="No native PQC negotiation defined yet; requires a new SAv6/IEC 62351-5 revision or wrapping in an IEC 62351-3 TLS tunnel that itself carries the PQC hybrid handshake",
         driving_deadline="NIST IR 8547 (draft) transition timeline; EO 14412 federal HVA deadlines (2030/2031) apply directly only to federal systems but set the vendor-compliance clock utilities will inherit via FAR rules",
         ot_specific_constraint="Many deployed DNP3 masters/outstations are serial-only RTUs with fixed firmware and multi-decade service life; no in-field crypto-agility",
         verify_flag="", source_id="dnp3-sav6-overview-pdf"),
    dict(row_id=2, protocol="DNP3", security_standard="DNP3 Secure Authentication v6 (SAv6)",
         crypto_function="bulk encryption / integrity",
         classical_primitive="AES-256-GCM (AEAD)",
         pqc_replacement="FIPS 203-derived symmetric session key established via a PQC-hybrid key exchange (AES-GCM itself is not broken by Shor's algorithm and is retained post-migration)",
         migration_mechanism="SAv6 already uses AEAD; the migration need is in how the AES key is established (see row 3), not in the AEAD cipher itself",
         driving_deadline="Same as above",
         ot_specific_constraint="AES-256-GCM is considered quantum-resistant at current key sizes (Grover's algorithm only halves effective security); this is a genuine 'no action needed' cell and should be labeled as such in the report",
         verify_flag="", source_id="dnp3-sav6-overview-pdf"),
    dict(row_id=3, protocol="DNP3", security_standard="DNP3 Secure Authentication v6 (SAv6)",
         crypto_function="key establishment / enrollment",
         classical_primitive="Low-Entropy Shared Secret (LESS) enrollment; elliptic-curve options referenced for 'low overhead'",
         pqc_replacement="FIPS 203 (ML-KEM-768 typical) replacing/hybridizing any ECDH-based enrollment step",
         migration_mechanism="Hybrid classical+PQC key encapsulation during device enrollment; requires updated enrollment tooling and larger key-exchange payloads over what may be a narrowband serial or cellular backhaul link",
         driving_deadline="NIST IR 8547 (draft)",
         ot_specific_constraint="ML-KEM ciphertext/key sizes (~1-1.5 KB) are far larger than legacy DNP3 frame budgets on serial/low-bandwidth links; framing and fragmentation impact must be tested, not assumed",
         verify_flag="verified 2026-09-09 (author sign-off)", source_id="dnp3-sav6-overview-pdf"),
    dict(row_id=4, protocol="IEC 60870-5-104", security_standard="IEC 62351-3 (TLS profile for TCP/IP-based IEC 60870-5 family)",
         crypto_function="transport authentication",
         classical_primitive="TLS 1.2/1.3 with X.509 certificates, mutual authentication (RSA or ECDSA signatures)",
         pqc_replacement="FIPS 204 (ML-DSA) or a composite/hybrid certificate (classical + ML-DSA) for the TLS handshake signature; FIPS 203 (ML-KEM) for the key exchange (hybrid X25519+ML-KEM as in draft IETF TLS 1.3 hybrid groups)",
         migration_mechanism="TLS 1.3 hybrid key-exchange groups plus a PQC or composite certificate chain; requires new certificates and CA tooling across the substation PKI",
         driving_deadline="NIST IR 8547 draft timeline; OMB M-26-15 requires federal TLS endpoints to support TLS 1.3 or a successor by 2030-01-02 (federal scope, but sets the interoperability bar vendors will target)",
         ot_specific_constraint="IEC 60870-5-104 is widely used for substation-to-control-center telemetry; certificate rotation across thousands of RTUs/gateways with limited maintenance windows is the operational bottleneck, not the cryptography itself",
         verify_flag="", source_id="iec-62351-ipcomm-sheet"),
    dict(row_id=5, protocol="IEC 60870-5-104", security_standard="IEC 62351-5 (application-layer authentication for the 60870-5 family)",
         crypto_function="application authentication",
         classical_primitive="Role-based access control (RBAC) token validation; statistical security-event logging",
         pqc_replacement="No direct 1:1 PQC primitive; RBAC tokens that embed a signature should move to FIPS 204 (ML-DSA) once token-issuing PKI is PQC-capable",
         migration_mechanism="Depends on IEC 62351-8 RBAC token format being revised to support PQC signature algorithms",
         driving_deadline="NIST IR 8547 (draft)",
         ot_specific_constraint="RBAC token verification happens on constrained field devices; ML-DSA signature sizes (~2.4-4.6 KB) are much larger than ECDSA/RSA and may exceed device buffer assumptions",
         verify_flag="verified 2026-09-09 (author sign-off)", source_id="iec-62351-ipcomm-sheet"),
    dict(row_id=6, protocol="ICCP/TASE.2", security_standard="IEC 62351-4 (MMS-based protocol security incl. ICCP/TASE.2 and IEC 61850 MMS)",
         crypto_function="transport + application authentication",
         classical_primitive="TLS via IEC 62351-3, plus an MMS-layer 'SECURE' association mechanism using X.509 certificates",
         pqc_replacement="FIPS 204 (ML-DSA) / composite certificates for both the TLS layer and the MMS SECURE association; FIPS 203 (ML-KEM) for TLS key exchange",
         migration_mechanism="Same TLS 1.3 hybrid approach as row 4, extended to the MMS association layer; inter-utility ICCP links (control-center to control-center) mean both ends' PKI must upgrade in a coordinated window",
         driving_deadline="NIST IR 8547 draft; EO 14412 vendor-compliance pressure via FAR rulemaking (180-day and 270-day tracks)",
         ot_specific_constraint="ICCP links cross utility/balancing-authority trust boundaries, so PQC cert format and trust-anchor migration must be bilaterally coordinated, not just per-utility",
         verify_flag="", source_id="iec-62351-ipcomm-sheet"),
    dict(row_id=7, protocol="Modbus Security (Modbus/TCP over TLS)", security_standard="Modbus/TCP Security Protocol Specification v3.6 (port 802)",
         crypto_function="transport authentication + key exchange",
         classical_primitive="TLS 1.2 minimum (TLS 1.1/1.0/SSLv3 prohibited); mandatory cipher suite TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256; recommended TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 (P-256 minimum); mutual X.509 authentication required (RFC 5280)",
         pqc_replacement="FIPS 203 (ML-KEM) hybridized into the ECDHE key exchange; FIPS 204 (ML-DSA) or composite cert replacing/augmenting the RSA or ECDSA certificate signature",
         migration_mechanism="Requires a new TLS 1.3-with-PQC-hybrid-groups cipher suite registered with IANA for Modbus/TCP Security, plus updated certificate issuance; the spec's IANA-registration requirement (R-12) means any new suite needs a formal registration step before it is standards-compliant",
         driving_deadline="NIST IR 8547 draft; general TLS-ecosystem PQC hybrid rollout (already shipping in some TLS 1.3 stacks as of 2026)",
         ot_specific_constraint="Modbus masters are frequently simple PLCs/gateways with minimal TLS stack footprint; adding PQC hybrid ciphersuites may require a firmware/stack upgrade the device cannot receive in place",
         verify_flag="", source_id="modbus-security-v36-pdf"),
    dict(row_id=8, protocol="OPC UA", security_standard="OPC UA Part 2 (Security Model) / Part 7 (Profiles)",
         crypto_function="transport signature + key exchange",
         classical_primitive="SecurityPolicy Basic256Sha256: asymmetric signature RSA-PKCS#1v1.5/SHA-256, asymmetric key transport RSA-OAEP, symmetric AES-256-CBC + HMAC-SHA-256; SecurityPolicy Aes256Sha256RsaPss: RSA-PSS/SHA-256 signature, RSA-OAEP-SHA-256 key transport",
         pqc_replacement="FIPS 204 (ML-DSA) replacing/augmenting the RSA signature in the application instance certificate; FIPS 203 (ML-KEM) replacing/augmenting RSA-OAEP for session key transport",
         migration_mechanism="Requires a new OPC UA SecurityPolicy URI (the OPC Foundation defines these centrally) analogous to Basic256Sha256 but naming ML-KEM/ML-DSA or a composite scheme; existing deployments negotiate down to legacy policies until every peer supports the new one",
         driving_deadline="NIST IR 8547 draft; OPC Foundation's own roadmap (vendor-driven; no fixed date published as of this build)",
         ot_specific_constraint="OPC UA is the most common protocol for new SCADA/historian and IT/OT-boundary integrations in energy, so it is the highest-leverage single point to standardize a PQC SecurityPolicy for the sector",
         verify_flag="verified 2026-09-09 (author sign-off)", source_id="opcua-vendor-doc-unified-automation"),
    dict(row_id=9, protocol="IEC 61850 (GOOSE / Sampled Values)", security_standard="IEC 62351-6",
         crypto_function="message integrity + authentication",
         classical_primitive="X.509 signatures and VLAN tagging on GOOSE/SMV telegrams (mechanism does not specify a single fixed signature algorithm; deployments commonly use RSA or ECDSA)",
         pqc_replacement="FIPS 204 (ML-DSA) as the signature algorithm option once 62351-6 is revised; ML-DSA's larger signature size is the dominant migration constraint",
         migration_mechanism="Requires an IEC 62351-6 revision naming an approved PQC or composite signature scheme sized to fit within GOOSE/SMV's sub-4ms delivery budget for protection-class messages",
         driving_deadline="NIST IR 8547 draft; no energy-sector-specific deadline yet (see Quantum-GUARD Act, row 13)",
         ot_specific_constraint="GOOSE trip/protection messages have a ~4 ms end-to-end delivery requirement; ML-DSA (~2.4-4.6 KB signatures) and even SLH-DSA (larger still) may not fit realistic frame/latency budgets without a lighter-weight or truncated PQC scheme -- this is the single hardest technical gap in the whole crosswalk",
         verify_flag="verified 2026-09-09 (author sign-off)", source_id="iec-62351-ipcomm-sheet"),
    dict(row_id=10, protocol="IEC 61850 (MMS services)", security_standard="IEC 62351-4 / 62351-8",
         crypto_function="application authentication + access control",
         classical_primitive="MMS 'SECURE' association (X.509) plus RBAC access tokens (IEC 62351-8, ASN.1 syntax, attribute certificates)",
         pqc_replacement="FIPS 204 (ML-DSA) for both the MMS association certificate and RBAC attribute-certificate signatures",
         migration_mechanism="Same TLS/MMS SECURE upgrade path as ICCP (row 6); RBAC token format needs revision to carry larger PQC signatures",
         driving_deadline="NIST IR 8547 draft",
         ot_specific_constraint="Shares the substation-PKI rotation bottleneck described in rows 4 and 6, compounded by the larger device population inside a substation (relays, merging units, bay controllers)",
         verify_flag="", source_id="iec-62351-ipcomm-sheet"),
    dict(row_id=11, protocol="IEC 62351-9 (key management)", security_standard="IEC 62351-9",
         crypto_function="key distribution",
         classical_primitive="GDOI (RFC 6407) group key distribution over IKEv2 (RFC 7427); X.509 PKI for all of 62351-3/4/5/6/8",
         pqc_replacement="FIPS 203 (ML-KEM) for IKEv2's PQC-hybrid key exchange (already defined in IETF drafts for IKEv2); FIPS 204 (ML-DSA) for the PKI's own CA and end-entity certificate signatures",
         migration_mechanism="Requires IKEv2 implementations used for energy-sector GDOI key distribution to adopt the PQC-hybrid IKEv2 key-exchange extensions and for the utility/vendor PKI hierarchy to issue ML-DSA or composite certificates",
         driving_deadline="NIST IR 8547 draft; this is the single point of control for cryptographic agility across every other row in this table -- it is the highest-priority target for early PQC pilots",
         ot_specific_constraint="Utility PKI is typically a small number of root/issuing CAs serving thousands of field devices; upgrading the CA hierarchy is comparatively tractable even though upgrading every field device is not -- sequencing matters",
         verify_flag="", source_id="iec-62351-ipcomm-sheet"),
    dict(row_id=12, protocol="IEEE C37.118.2 (Synchrophasor / PMU data)", security_standard="none native; secured via IEC 61850-90-5 or external transport",
         crypto_function="message integrity + authentication",
         classical_primitive="C37.118.2 itself defines no cryptography; when secured, IEC 61850-90-5 adds HMAC and/or RSA-based signatures modeled on GOOSE/SMV-style protection, or the link is wrapped in an external TLS/IPsec tunnel",
         pqc_replacement="FIPS 204 (ML-DSA) if adopted into a future 61850-90-5 revision; FIPS 203/204 hybrid TLS/IPsec if secured at the transport layer instead",
         migration_mechanism="No protocol-native PQC path exists; near-term mitigation for PMU links is external TLS 1.3-hybrid or IPsec tunneling rather than waiting on a 61850-90-5 PQC revision",
         driving_deadline="NIST IR 8547 draft; Quantum-GUARD Act of 2026 (introduced, not enacted) specifically directs a DOE study of quantum risk to bulk-electric-system IT/OT that would cover synchrophasor infrastructure",
         ot_specific_constraint="Synchrophasor data has strict latency (sub-cycle) and high message-rate requirements (30-120 messages/sec per PMU); any added cryptographic overhead competes directly with the timing budget that makes the data useful for wide-area protection",
         verify_flag="verified 2026-09-09 (author sign-off)", source_id="c37118-90-5-overview"),
    dict(row_id=13, protocol="NERC CIP identity and access management (CIP-005, CIP-007, CIP-004)", security_standard="grid-wide identity/PKI context (not a wire protocol)",
         crypto_function="identity governance",
         classical_primitive="Certificate- and credential-based access control for BES Cyber Systems; algorithm choice is left to the implementing utility's PKI, typically RSA-2048+ or ECDSA P-256",
         pqc_replacement="FIPS 204 (ML-DSA) or composite certificates once utility PKI vendors support it; NERC CIP standards do not currently name a required algorithm and would need a standard-drafting-team revision to reference FIPS 203-205",
         migration_mechanism="No NERC-mandated PQC migration path exists yet; utilities can move ahead of NERC by requiring PQC-capable PKI in new BES Cyber System procurements today",
         driving_deadline="Quantum-GUARD Act of 2026 (introduced) directs FERC to consider quantum-computing risk within its grid-reliability authority, which could feed a future NERC CIP standard; no binding NERC deadline exists as of this build",
         ot_specific_constraint="NERC CIP compliance evidence and audit cycles run on multi-year schedules; a PQC requirement introduced via standard revision would likely carry a multi-year implementation timeline similar to past CIP revisions",
         verify_flag="verified 2026-09-09 (author sign-off)", source_id=""),
]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for row in ROWS:
            w.writerow(row)
    print(f"Wrote {OUT} ({len(ROWS)} rows)")


if __name__ == "__main__":
    main()
