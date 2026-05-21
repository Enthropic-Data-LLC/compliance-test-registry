# NIST SP 800-171 r3 — Protecting CUI in Nonfederal Systems

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** ~117 security requirements across 17 families (r3, published May 2024)
**Authority:** National Institute of Standards and Technology (NIST)
**Enforcing context:** DFARS 252.204-7012; all DoD contracts handling CUI; CMMC Level 2 baseline

---

## Summary

| Metric | Count |
|---|---|
| Families | 17 |
| Total requirements | ~117 (r3 expanded from 110 in r2) |
| Requirements parsed (individual files) | 3 (AC, IA, AU+CM+SI — 58 of ~117 requirements covered) |
| Fully automated (DETERMINISTIC) | HIGH — AC (lockout, session lock, remote access), IA (MFA, password policy, hash algorithm), AU (log retention, NTP), CM (baseline, change control), SI (AV, vuln scan) |
| Partial automation (PARAMETERIZED) | Moderate — role/need-to-know adequacy, configuration completeness, SLA window adequacy |
| Human-determination required (CONTESTED) | RA (risk methodology), SR (supply chain), PM (program sufficiency) |
| Unresolvable | Minimal |
| Open assumptions | 18 (ASSUME-800171-AC-001–009, IA-001–007, AU-001–003, CM-001–002, SI-001–003) |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## CUI scoping — pre-condition to all tests

All 800-171 requirements apply only to systems that process, store, or transmit **Controlled Unclassified Information (CUI)**. CUI scope determination is a prerequisite and is itself PARAMETERIZED/CONTESTED. All Pattern 1/2/3 tests must be gated by a `system_processes_cui()` fixture that requires human attestation before any test transitions from informational to enforcing mode. System boundary changes trigger re-attestation.

| Scoping decision | Classification | Rationale |
|---|---|---|
| Is this data CUI? | PARAMETERIZED | CUI Registry (nara.gov) defines categories; application to specific data instances requires human determination |
| Is this system in-scope? | PARAMETERIZED | CUI flow documentation and network boundary diagram required as evidence |
| CUI enclave boundary | CONTESTED | DFARS 7012 requires "adequate security"; boundary adequacy is contracting-officer-dependent |

---

## Per-family confidence map

| Family | Abbrev | Req range | Confidence projection | PARAMETERIZED surface | CONTESTED surface |
|---|---|---|---|---|---|
| Access Control | AC | 3.1.1–3.1.22 (22 reqs) | MEDIUM | Remote access method; split tunneling exception | — |
| Awareness and Training | AT | 3.2.1–3.2.3 (3 reqs) | MEDIUM | Role-based training adequacy; insider-threat awareness scope | — |
| Audit and Accountability | AU | 3.3.1–3.3.9 (9 reqs) | HIGH–MEDIUM | Audit review frequency | — |
| Configuration Management | CM | 3.4.1–3.4.9 (9 reqs) | HIGH | Baseline approval process | — |
| Identification and Authentication | IA | 3.5.1–3.5.12 (12 reqs) | HIGH | MFA exception criteria | — |
| Incident Response | IR | 3.6.1–3.6.3 (3 reqs) | MEDIUM | Response capability adequacy; external reporting scope | — |
| Maintenance | MA | 3.7.1–3.7.6 (6 reqs) | MEDIUM | Remote maintenance control method | — |
| Media Protection | MP | 3.8.1–3.8.9 (9 reqs) | MEDIUM | Sanitization method adequacy | — |
| Personnel Security | PS | 3.9.1–3.9.2 (2 reqs) | PARAMETERIZED | Screening criteria "commensurate with risk" | — |
| Physical Protection | PE | 3.10.1–3.10.6 (6 reqs) | HIGH | — | — |
| Risk Assessment | RA | 3.11.1–3.11.3 (3 reqs) | CONTESTED | Risk methodology acceptability | Risk tolerance boundary |
| Security Assessment | CA | 3.12.1–3.12.4 (4 reqs) | MEDIUM | Assessment scope and remediation plan adequacy | — |
| System and Communications Protection | SC | 3.13.1–3.13.16 (16 reqs) | HIGH–MEDIUM | Cryptographic strength adequacy for non-CUI-in-transit edge cases | — |
| System and Information Integrity | SI | 3.14.1–3.14.7 (7 reqs) | MEDIUM | Malicious code response method | — |
| Supply Chain Risk Management | SR | 3.17.1–3.17.4 (4 reqs) | CONTESTED | Vendor risk adequacy | Supply chain controls sufficiency |
| Planning | PL | 3.18.1 (1 req) | PARAMETERIZED | SSP completeness criteria | — |
| Program Management | PM | 3.x (r3 additions) | CONTESTED | Program sufficiency | — |

---

## Open assumption registry

| ID | Family/Req | Summary | Review date |
|---|---|---|---|
| ASSUME-800171-AC-001 | AC 3.1.2 | CUI access: formal role definitions; semi-annual review; no default full-access provisioning | 2026-05-20 |
| ASSUME-800171-AC-002 | AC 3.1.5 | Least privilege: separate privileged accounts; admin accounts not used for non-admin tasks; JIT preferred | 2026-05-20 |
| ASSUME-800171-AC-003 | AC 3.1.8 | Lockout: ≤10 consecutive failed attempts; minimum 30-min lockout duration | 2026-05-20 |
| ASSUME-800171-AC-004 | AC 3.1.9 | Login banners: authorized-use-only statement; monitoring consent; penalties reference | 2026-05-20 |
| ASSUME-800171-AC-005 | AC 3.1.10 | Session lock: ≤15 min inactivity; pattern-hiding (content cleared, not just locked) | 2026-05-20 |
| ASSUME-800171-AC-006 | AC 3.1.12 | Remote access: approved encrypted channel; sessions logged; split tunneling controlled | 2026-05-20 |
| ASSUME-800171-AC-007 | AC 3.1.13 | Cryptographic remote access: TLS 1.2+ or IKEv2/AES; PPTP/L2TP/SSL prohibited; FIPS 140 for federal contractors | 2026-05-20 |
| ASSUME-800171-AC-008 | AC 3.1.16/17 | Wireless: WPA2-Enterprise or WPA3; individual auth; rogue AP detection; guest isolated from CUI network | 2026-05-20 |
| ASSUME-800171-AC-009 | AC 3.1.18/19 | Mobile devices: MDM enrolled; encrypted; remote wipe; BYOD = CUI containerized | 2026-05-20 |
| ASSUME-800171-IA-001 | IA 3.5.3 | MFA: FIPS 140-2/3 validated; SMS OTP insufficient; FIDO2/PIV preferred for privileged | 2026-05-20 |
| ASSUME-800171-IA-002 | IA 3.5.4 | Replay-resistant: Kerberos, TLS cert, FIDO2, PIV, TOTP acceptable; password-only network auth does not satisfy | 2026-05-20 |
| ASSUME-800171-IA-003 | IA 3.5.5 | Identifier non-reuse: user IDs not reused ≥90 days; service accounts ≥12 months | 2026-05-20 |
| ASSUME-800171-IA-004 | IA 3.5.7 | Password: min 8+complexity or 15 chars; breach-triggered rotation; checked against known-breached lists | 2026-05-20 |
| ASSUME-800171-IA-005 | IA 3.5.8 | Password history: ≥5 prior passwords prohibited; common/dictionary passwords rejected | 2026-05-20 |
| ASSUME-800171-IA-006 | IA 3.5.9 | Temporary passwords: first-use change enforced; validity ≤24 hours; not transmitted unencrypted | 2026-05-20 |
| ASSUME-800171-IA-007 | IA 3.5.10 | Password hashing: bcrypt ≥10/scrypt/Argon2id/PBKDF2-SHA256 ≥310k; MD5/SHA-1 unacceptable | 2026-05-20 |
| ASSUME-800171-AU-001 | AU 3.3.1 | Logging: 8 event categories; 90-day online; 12-month archive; integrity protected; required fields | 2026-05-20 |
| ASSUME-800171-AU-002 | AU 3.3.3 | Audit failure alerting: automated ≤15 min; routed to security team; documented as incident | 2026-05-20 |
| ASSUME-800171-AU-003 | AU 3.3.7 | NTP: NIST-traceable source; drift ≤1 sec; all CUI systems synchronized | 2026-05-20 |
| ASSUME-800171-CM-001 | CM 3.4.1 | Config baselines: references DISA STIG or CIS Benchmark; version-controlled; monthly drift comparison | 2026-05-20 |
| ASSUME-800171-CM-002 | CM 3.4.6/7 | Least functionality: all services/ports documented; approved software list; annual review; USB restricted | 2026-05-20 |
| ASSUME-800171-SI-001 | SI 3.14.1 | AV: all general-purpose OS; 24h definitions; real-time scanning; users cannot disable | 2026-05-20 |
| ASSUME-800171-SI-002 | SI 3.14.5 | Scanning: real-time on-access; weekly full scans; external media scanned; exclusions minimized | 2026-05-20 |
| ASSUME-800171-SI-003 | SI 3.14.6 | Vuln mgmt: quarterly scans; critical CVSS≥7.0 ≤30 days; non-critical ≤90 days; internet-facing monthly | 2026-05-20 |

---

## Contested items pending resolution

| Item | Family/Req | Reason | Resolution path |
|---|---|---|---|
| Risk assessment methodology | RA 3.11.1–3.11.2 | Risk methodology and scope adequacy are assessment-officer-evaluated | ISSO documents methodology; DoD CO/assessor review |
| Supply chain risk adequacy | SR 3.17.1–3.17.4 | Vendor assessment depth and ICT supply chain control sufficiency are judgment calls | ISSO documents supplier risk methodology; CMMC assessor review |
| Program management sufficiency | PM (r3 additions) | Program maturity and resource sufficiency are auditor-evaluated | Management review + CMMC assessment |

---

## Specification file status

| File | Contents | Assumptions | Confidence | Status |
|---|---|---|---|---|
| `ac-access-control.md` | AC family — 22 requirements (3.1.1–3.1.22): user/device access, least privilege, remote access, wireless, mobile | ASSUME-800171-AC-001–009 | MEDIUM–HIGH | ✅ Parsed |
| `ia-identification-authentication.md` | IA family — 12 requirements (3.5.1–3.5.12): MFA, password policy, adaptive hash storage, replay resistance | ASSUME-800171-IA-001–007 | HIGH | ✅ Parsed |
| `au-cm-si-core-technical.md` | AU (9 reqs), CM (9 reqs), SI (7 reqs): log retention, NTP, config baselines, AV, vuln scans | ASSUME-800171-AU-001–003, CM-001–002, SI-001–003 | HIGH | ✅ Parsed |
| *(SC, IR, PE, MA, MP, PS, RA, CA, SR, PL)* | Remaining 9 families (~60 requirements) | TBD | MEDIUM | 🔲 Pending |

---

## Cross-standard dependencies

| Shared artifact | Standards | Notes |
|---|---|---|
| System Security Plan (SSP) | 800-171 PL, CMMC Level 2, FedRAMP (if applicable) | 800-171 SSP is the direct scoring input for CMMC Level 2 assessment; FedRAMP uses a different template but shares the same control families |
| Access control / IAM records | 800-171 AC + IA; CMMC AC + IA domains | Same IAM system; different evidence format requirements per framework |
| Incident response plan | 800-171 IR, CMMC IR domain | 800-171 IR.3.098 maps directly to CMMC IR.2.093–IR.3.098 |
| Risk assessment records | 800-171 RA, CMMC RA domain, FedRAMP CA/RA | Single risk methodology must satisfy all applicable frameworks simultaneously |
| Configuration baseline | 800-171 CM, CMMC CM domain | SSP documents baseline; same artifact satisfies both |
| Audit logs | 800-171 AU, CMMC AU domain, FedRAMP AU | Log retention and content requirements align across all three; FedRAMP adds SIEM integration requirement |

---

## CI/CD gate configuration

Standard three-tier gate (see NERC CIP registry). Additional constraint unique to 800-171:

- **CUI scope fixture** must be attested by a named human before any test transitions from informational to enforcing mode.
- System boundary changes trigger re-attestation of all in-scope tests.
- SSP version tracked in registry manifest; any SSP revision increments the registry version and triggers re-review of all PARAMETERIZED tests that cite it as evidence.

---

## Remaining parse priority

| Priority | Family | Req count | Rationale |
|---|---|---|---|
| 1 | SC | 16 | CUI-in-transit encryption requirements are DETERMINISTIC; high CMMC overlap |
| 2 | IR | 3 | Small family; medium confidence; CMMC overlap justifies early parse |
| 3 | PE | 6 | HIGH confidence; physical controls are DETERMINISTIC |
| 4 | RA, SR, MA, MP, PS, CA, PL | varies | CONTESTED/PARAMETERIZED; parse after high-confidence block complete |

---

## Watch list

| Item | Status | Impact |
|---|---|---|
| CMMC Final Rule (32 CFR Part 170) | Effective Dec 2024 | Level 2 uses 800-171 r2 for initial period; DoD roadmap for r3 alignment TBD |
| NIST 800-171A r3 (assessment procedures) | Draft published 2024 | Companion document defining how each requirement is assessed; test cases should align to 800-171A assessment objectives once finalized |
| NIST 800-172 r1 | Final published 2021; input to CMMC Level 3 | 35 enhanced requirements for CUI in high-value assets; cross-reference into CMMC index |
