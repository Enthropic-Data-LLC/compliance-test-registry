# HIPAA Security Rule — 45 CFR Part 164 Subpart C

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Administrative, physical, and technical safeguards for electronic Protected Health Information (ePHI)
**Authority:** U.S. Department of Health and Human Services (HHS) / Office for Civil Rights (OCR)
**Enforcing context:** Covered entities (health plans, healthcare clearinghouses, healthcare providers); business associates (BAs) under HITECH Act; subcontractors of BAs
**Note:** HIPAA Privacy Rule (45 CFR Part 164 Subpart E) is out of scope here; this registry covers the Security Rule only

---

## Summary

| Metric | Count |
|---|---|
| Safeguard categories | 3 (Administrative, Physical, Technical) + Organizational + Documentation |
| Standards (top-level) | 18 |
| Implementation specifications | ~40 (Required or Addressable) |
| Specifications parsed (individual files) | 5 (164.308, 164.310, 164.312, 164.314, 164.316) |
| Fully automated (DETERMINISTIC) | Low-moderate — many specifications are "addressable" and methodology-dependent |
| Partial automation (PARAMETERIZED) | Dominant |
| Human-determination required (CONTESTED) | Significant (risk analysis, addressable specification substitution) |
| Unresolvable | Minimal |
| Open assumptions | 23 |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Required vs. Addressable — the critical distinction

HIPAA Security Rule implementation specifications are either **Required** or **Addressable**:

| Type | Obligation |
|---|---|
| **Required** | Must be implemented exactly as stated |
| **Addressable** | Must be implemented if reasonable and appropriate; if not, must (1) document why it is not reasonable/appropriate AND (2) implement an equivalent alternative measure |

> **Common misconception:** "Addressable" does NOT mean optional. Failure to implement or document substitution is a violation. The addressable designation adds a PARAMETERIZED layer — the "reasonable and appropriate" determination is the obligation.

---

## Per-standard confidence map

### §164.308 — Administrative Safeguards

| Standard | Implementation Spec | R/A | Confidence | Notes |
|---|---|---|---|---|
| (a)(1) Security management process | Risk analysis | R | CONTESTED | Risk methodology not specified; adequacy is auditor-evaluated |
| | Risk management | R | CONTESTED | Risk response strategy adequacy |
| | Sanction policy | R | MEDIUM | Policy existence is DETERMINISTIC; content adequacy is PARAMETERIZED |
| | Information system activity review | R | MEDIUM | Review frequency — org-defined; completeness is PARAMETERIZED |
| (a)(2) Assigned security responsibility | — | R | DETERMINISTIC | Named HIPAA Security Officer must be designated; binary |
| (a)(3) Workforce security | Authorization and/or supervision | A | PARAMETERIZED | Scope of access authorization process |
| | Workforce clearance procedure | A | PARAMETERIZED | Screening criteria adequacy |
| | Termination procedures | A | MEDIUM | Offboarding completeness |
| (a)(4) Information access management | Isolating healthcare clearinghouse functions | R | DETERMINISTIC | Binary: clearinghouses must separate PHI from other data |
| | Access authorization | A | PARAMETERIZED | Authorization process adequacy |
| | Access establishment and modification | A | PARAMETERIZED | Provisioning process completeness |
| (a)(5) Security awareness and training | Security reminders | A | PARAMETERIZED | Reminder frequency and content |
| | Protection from malicious software | A | MEDIUM | AV deployment — DETERMINISTIC existence; update cadence — PARAMETERIZED |
| | Log-in monitoring | A | MEDIUM | Monitoring frequency |
| | Password management | A | MEDIUM | Password policy content |
| (a)(6) Security incident procedures | Response and reporting | R | PARAMETERIZED | Incident definition scope; response capability adequacy |
| (a)(7) Contingency plan | Data backup plan | R | MEDIUM | Backup existence is DETERMINISTIC; adequacy is PARAMETERIZED |
| | Disaster recovery plan | R | PARAMETERIZED | Plan completeness and testing |
| | Emergency mode operation plan | R | PARAMETERIZED | Plan completeness |
| | Testing and revision procedures | A | PARAMETERIZED | Test frequency and scope |
| | Applications and data criticality analysis | A | PARAMETERIZED | Criticality assessment methodology |
| (a)(8) Evaluation | — | R | PARAMETERIZED | Evaluation scope and frequency (no stated interval) |

### §164.310 — Physical Safeguards

| Standard | Implementation Spec | R/A | Confidence | Notes |
|---|---|---|---|---|
| (a)(1) Facility access controls | Contingency operations | A | PARAMETERIZED | Facility access during emergency |
| | Facility security plan | A | PARAMETERIZED | Plan completeness |
| | Access control and validation | A | PARAMETERIZED | Access control method adequacy |
| | Maintenance records | A | MEDIUM | Maintenance log existence is DETERMINISTIC; content is PARAMETERIZED |
| (b) Workstation use | — | R | PARAMETERIZED | Workstation use policy adequacy |
| (c) Workstation security | — | R | PARAMETERIZED | Physical safeguard method |
| (d) Device and media controls | Disposal | R | PARAMETERIZED | Sanitization method — method not specified |
| | Media re-use | R | MEDIUM | Re-use sanitization process |
| | Accountability | A | MEDIUM | Media tracking log completeness |
| | Data backup and storage | A | MEDIUM | Backup adequacy |

### §164.312 — Technical Safeguards

| Standard | Implementation Spec | R/A | Confidence | Notes |
|---|---|---|---|---|
| (a)(1) Access control | Unique user identification | R | DETERMINISTIC | Shared accounts prohibited; binary |
| | Emergency access procedure | R | PARAMETERIZED | Emergency access mechanism adequacy |
| | Automatic logoff | A | MEDIUM | Session timeout — value is org-defined; existence is DETERMINISTIC |
| | Encryption and decryption | A | PARAMETERIZED | Encryption is **addressable** — HHS does not mandate a specific algorithm; NIST guidelines are the reference |
| (b) Audit controls | — | R | MEDIUM | Log content and retention — no explicit retention period in rule; 6-year documentation retention applies via §164.316 |
| (c) Integrity | Authentication of ePHI | A | MEDIUM | Integrity mechanism method |
| (d) Authentication (person/entity) | — | R | MEDIUM | Authentication mechanism — method not specified |
| (e)(1) Transmission security | Integrity controls | A | MEDIUM | Transmission integrity method |
| | Encryption | A | PARAMETERIZED | Encryption is **addressable** — not required; but OCR breach investigations scrutinize absent encryption heavily |

> **Critical note on encryption:** Encryption is addressable under both §164.312(a) and §164.312(e). However, the HITECH Act created a "safe harbor" for breaches involving properly encrypted data — if encryption is absent and a breach occurs, the covered entity faces mandatory notification and potential penalty. This creates strong de facto pressure to encrypt even though it is technically addressable.

### §164.314 — Organizational Requirements

| Standard | Implementation Spec | R/A | Confidence | Notes |
|---|---|---|---|---|
| (a)(1) Business associate contracts | — | R | DETERMINISTIC | BAA required with every BA; existence is binary |
| (a)(2)(i) BAA required elements | — | R | PARAMETERIZED | Contract clause completeness |
| (b)(1) Group health plan requirements | — | R | Applicable to health plans only | Plan document amendment requirements |

### §164.316 — Policies and Procedures + Documentation

| Standard | Implementation Spec | R/A | Confidence | Notes |
|---|---|---|---|---|
| (a) Policies and procedures | — | R | PARAMETERIZED | Policy coverage and content adequacy |
| (b)(1) Documentation | — | R | DETERMINISTIC | 6-year documentation retention period is bright-line |
| (b)(2) Updates | — | R | PARAMETERIZED | Policy update cadence — no stated interval; must reflect current practices |

---

## Key DETERMINISTIC thresholds

| Control | Threshold | Section |
|---|---|---|
| Security Officer designation | Named individual required | §164.308(a)(2) |
| Unique user ID | No shared accounts for ePHI access | §164.312(a)(2)(i) |
| Business Associate Agreement | Required before PHI disclosure to BA | §164.314(a)(1) |
| Documentation retention | 6 years from creation or last effective date | §164.316(b)(2) |
| Breach notification (Privacy Rule overlap) | 60 days from discovery | §164.404 (Privacy Rule) |

---

## HITECH Act interactions

The HITECH Act (2009) strengthened HIPAA enforcement and added:
- Direct liability for Business Associates (not just CEs)
- Tiered penalty structure ($100–$1.9M per violation category per year)
- Breach notification requirements (now in §164.400–164.414)
- Encryption safe harbor for breaches

---

## Open assumption registry

| ID | Section | Summary | Review date |
|---|---|---|---|
| ASSUME-308-001 | §164.308(a)(1)(ii)(C) | Sanction policy adequate: tiered, graduated, written, never waived | 2026-05-20 |
| ASSUME-308-002 | §164.308(a)(1)(ii)(D) | Activity review: daily for privileged users, weekly for all users | 2026-05-20 |
| ASSUME-308-003 | §164.308(a)(3)(ii)(C) | Termination: involuntary = same-day; voluntary = by last day of employment | 2026-05-20 |
| ASSUME-308-004 | §164.308(a)(5)(ii)(B) | Malware protection: AV on all endpoints/servers/email gateways; update ≤ 24 hours | 2026-05-20 |
| ASSUME-308-005 | §164.308(a)(5)(ii)(D) | Passwords: min 12 chars; last 5 prohibited; max 90 days or MFA; complexity required | 2026-05-20 |
| ASSUME-308-006 | §164.308(a)(6)(ii) | Incident response: log within 24h; IRP tested annually; post-incident review within 30 days for significant events | 2026-05-20 |
| ASSUME-308-007 | §164.308(a)(7)(ii)(A) | Backup: RPO ≤ 24h; encrypted copies off-site; restore test quarterly; air-gapped copy for ransomware | 2026-05-20 |
| ASSUME-308-008 | §164.308(a)(8) | Evaluation: annual at minimum; triggered on significant change | 2026-05-20 |
| ASSUME-310-001 | §164.310(a)(1) | Facility access: authorized list reviewed quarterly; events logged with identity/timestamp; log reviewed monthly | 2026-05-20 |
| ASSUME-310-002 | §164.310(a)(2)(iv) | "Physical components related to security" = locks, card readers, alarm systems, server room doors, CCTV | 2026-05-20 |
| ASSUME-310-003 | §164.310(b) | Workstation use policy: permitted activities; screen positioning; clean desk; auto screen lock | 2026-05-20 |
| ASSUME-310-004 | §164.310(c) | Physical safeguards: privacy screens in public areas; auto-lock ≤ 15 min; cable locks or locked storage for portables | 2026-05-20 |
| ASSUME-310-005 | §164.310(d)(2)(i) | Sanitization: NIST SP 800-88 Clear/Purge/Destroy; DoD 5220.22-M; cryptographic erase; physical destruction; certificate of destruction required for vendor disposal | 2026-05-20 |
| ASSUME-312-001 | §164.312(a)(2)(ii) | Emergency access: break-glass procedure documented; tested annually; access logged; minimum number of emergency accounts | 2026-05-20 |
| ASSUME-312-002 | §164.312(a)(2)(iii) | Session timeout: ≤ 15 min public/semi-public areas; ≤ 30 min controlled areas | 2026-05-20 |
| ASSUME-312-003 | §164.312(a)(2)(iv) | Encryption at rest: AES-128 or AES-256; FIPS 140-2 or FIPS 140-3 validated; RC4/DES/3DES not acceptable | 2026-05-20 |
| ASSUME-312-004 | §164.312(b) | Audit controls: 6-year retention; tamper-evident/write-once storage; weekly review for high-risk systems, monthly for all others | 2026-05-20 |
| ASSUME-312-005 | §164.312(c)(2) | Integrity mechanism: SHA-256 or stronger; SHA-1 not acceptable for new implementations | 2026-05-20 |
| ASSUME-312-006 | §164.312(d) | Authentication: MFA required for internet-facing ePHI access; SMS OTP not acceptable for new implementations | 2026-05-20 |
| ASSUME-312-007 | §164.312(e)(2)(ii) | Transmission encryption: TLS 1.2+; TLS 1.3 preferred; AEAD cipher suites; no RC4/DES/3DES/NULL/EXPORT/anon | 2026-05-20 |
| ASSUME-314-001 | §164.314(a)(2) | BAA content-complete: all 8 required clauses present; breach reporting ≤ 60 days (30 recommended); return/destroy clause specifies method and written confirmation | 2026-05-20 |
| ASSUME-316-001 | §164.316(a) | Policy adequate: org-specific (not template); defines roles/responsibilities; sufficient detail for workforce; consistent with actual practice; approved by Security Officer | 2026-05-20 |
| ASSUME-316-002 | §164.316(b)(2)(iii) | Periodic review = annual at minimum; triggered reviews on: new ePHI system, significant change, workforce change, breach, regulatory change, audit finding | 2026-05-20 |

---

## Contested items pending resolution

| ID | Section | Contested element | Reason | Resolution path |
|---|---|---|---|---|
| CONTEST-308-001 | §164.308(a)(1)(ii)(A) | Risk analysis methodology adequacy | Regulation does not define methodology; OCR evaluates on a facts-and-circumstances basis; no safe harbor for any specific tool or approach | Pattern 3: surface to QSA/auditor; document methodology and rationale; NIST SP 800-30 is the recommended reference |
| CONTEST-308-002 | §164.308(a)(1)(ii)(B) | Risk management strategy adequacy | Risk response sufficiency is auditor-evaluated; no threshold for "reasonable and appropriate" risk reduction | Pattern 3: surface to Security Officer; document risk acceptance rationale for each accepted risk above threshold |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Risk analysis | HIPAA §164.308(a)(1), NIST 800-53 RA-3, ISO 27001 Clause 6 | HHS recommends NIST SP 800-30 methodology for HIPAA risk analysis; using 800-53 RA-3 satisfies HIPAA risk analysis if documented |
| Audit logs | HIPAA §164.312(b), SOC 2 CC7, PCI DSS Req 10 | HIPAA has no explicit retention period in the Security Rule; 6-year documentation retention (§164.316) is often applied. PCI 12-month retention is stricter — design to PCI if both apply |
| Access control records | HIPAA §164.312(a), SOC 2 CC6, PCI DSS Req 7–8, NIST 800-53 AC | HIPAA prohibits shared IDs (DETERMINISTIC); PCI has tighter password thresholds — design to PCI if both apply |
| Business associate agreements | HIPAA §164.314, GDPR Art. 28 DPA, ISO 27001 A.5.19 | A combined data processing/BA agreement template can satisfy HIPAA and GDPR simultaneously |
| Encryption | HIPAA §164.312(a)+(e) (addressable), PCI DSS Req 3+4 (required), NIST 800-53 SC-8+SC-28 | PCI mandates encryption; using PCI-grade encryption exceeds HIPAA addressable requirement |
| Incident response | HIPAA §164.308(a)(6), SOC 2 CC7.3, NIST 800-53 IR | Response plan content requirements differ; single IRP with framework-specific annexes is recommended |

---

## CI/CD gate configuration

Standard three-tier gate (see NERC CIP registry). HIPAA-specific constraints:

- **ePHI scope fixture:** All tests gated by `system_handles_ephi()` — must be attested before tests are enforcing.
- **BA relationship tracker:** §164.314 test checks that all vendors with ePHI access have a current, signed BAA on file. Missing or expired BAA triggers Pattern 3 block.
- **Addressable specification tracker:** For each addressable specification marked "not implemented," a substitution rationale must be on file. Absence of rationale triggers Pattern 2 failure.
- **Risk analysis recency:** No stated interval, but OCR guidance and case law suggest at least annual or upon significant environmental change. Test flags if last risk analysis is > 12 months old.

---

## Specification file status

| Section | File | Status | Assumptions | Contested items |
|---|---|---|---|---|
| §164.308 — Administrative Safeguards | `164.308-administrative-safeguards.md` | ✅ Parsed | 8 (ASSUME-308-001 through -008) | 2 (risk analysis, risk management) |
| §164.310 — Physical Safeguards | `164.310-physical-safeguards.md` | ✅ Parsed | 5 (ASSUME-310-001 through -005) | 0 |
| §164.312 — Technical Safeguards | `164.312-technical-safeguards.md` | ✅ Parsed | 7 (ASSUME-312-001 through -007) | 0 |
| §164.314 — Organizational Requirements | `164.314-organizational-requirements.md` | ✅ Parsed | 1 (ASSUME-314-001) | 0 |
| §164.316 — Policies and Documentation | `164.316-policies-documentation.md` | ✅ Parsed | 2 (ASSUME-316-001 through -002) | 0 |
