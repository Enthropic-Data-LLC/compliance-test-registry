# ISO/IEC 27001:2022 — Information Security Management System

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Mandatory clauses 4–10 + Annex A (93 controls across 4 themes)
**Authority:** International Organization for Standardization (ISO) / International Electrotechnical Commission (IEC)
**Enforcing context:** Third-party certification (accredited certification body); contractual requirements; regulatory recognition (GDPR, NIS2 in EU; various national frameworks)
**Current edition:** ISO/IEC 27001:2022 (supersedes 2013 edition; transition deadline Oct 31 2025)

---

## Summary

| Metric | Count |
|---|---|
| Mandatory clauses | 7 (Clauses 4–10) |
| Annex A themes | 4 |
| Annex A controls | 93 (reduced from 114 in 2013 edition; 11 new controls added) |
| Controls parsed (individual files) | 5 (clauses-4-10, A.5.x, A.6.x, A.7.x, A.8.x — all themes complete) |
| Fully automated (DETERMINISTIC) | Low overall — but A.5.17, A.8.5, A.8.7, A.8.13, A.8.15, A.7.7, A.7.11, A.7.14 have HIGH-confidence DETERMINISTIC tests |
| Partial automation (PARAMETERIZED) | Dominant mode |
| Human-determination required (CONTESTED) | Significant (risk treatment, SoA justification, ISMS scope, supplier adequacy) |
| Unresolvable | Minimal |
| Open assumptions | 29 (ASSUME-ISO-001–005, ASSUME-ISO-A5-001–007, ASSUME-ISO-A6-001–005, ASSUME-ISO-A7-001–009, ASSUME-ISO-A8-001–008) |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Mandatory clauses — confidence map

| Clause | Title | Confidence | PARAMETERIZED surface | CONTESTED surface |
|---|---|---|---|---|
| 4 | Context of the organization | PARAMETERIZED | Interested parties scope; internal/external issue identification adequacy | — |
| 5 | Leadership | PARAMETERIZED | Policy adequacy; management review evidence | — |
| 6 | Planning | CONTESTED | Risk treatment option selection (6.1.3); SoA completeness (6.1.3d) | Risk acceptance criteria; residual risk acceptability |
| 7 | Support | PARAMETERIZED | Competence adequacy; awareness program scope; documented information sufficiency | — |
| 8 | Operation | PARAMETERIZED | Risk treatment plan implementation completeness | — |
| 9 | Performance evaluation | MEDIUM | Internal audit scope (9.2); monitoring metrics selection | Management review adequacy |
| 10 | Improvement | PARAMETERIZED | Nonconformity root cause analysis adequacy; corrective action sufficiency | — |

---

## Annex A — per-theme confidence map

### Theme 1: Organizational controls (37 controls — A.5.x)

| Control | Title | Confidence | Notes |
|---|---|---|---|
| A.5.1 | Information security policies | PARAMETERIZED | Policy review frequency (annual minimum) is DETERMINISTIC; content adequacy is PARAMETERIZED |
| A.5.2 | Information security roles | PARAMETERIZED | Role existence is DETERMINISTIC; adequacy of separation of duties is PARAMETERIZED |
| A.5.3 | Segregation of duties | PARAMETERIZED | Conflict of interest scope | — |
| A.5.4 | Management responsibilities | PARAMETERIZED | Communication of policy to staff | — |
| A.5.5 | Contact with authorities | PARAMETERIZED | Frequency and scope of authority contacts | — |
| A.5.6 | Contact with special interest groups | PARAMETERIZED | — | — |
| A.5.7 | Threat intelligence *(new in 2022)* | PARAMETERIZED | Timeliness and source quality | — |
| A.5.8 | Information security in project management | PARAMETERIZED | Project classification threshold | — |
| A.5.9 | Inventory of information and assets | MEDIUM | Asset completeness determination is PARAMETERIZED | — |
| A.5.10 | Acceptable use of assets | PARAMETERIZED | Policy completeness | — |
| A.5.11 | Return of assets | DETERMINISTIC | Binary: returned or not at termination | — |
| A.5.12 | Classification of information | PARAMETERIZED | Classification scheme adequacy | — |
| A.5.13 | Labelling of information | PARAMETERIZED | Label completeness | — |
| A.5.14 | Information transfer | PARAMETERIZED | Agreement content adequacy | — |
| A.5.15 | Access control | MEDIUM | Rule definition adequacy | — |
| A.5.16 | Identity management | MEDIUM | Identity lifecycle completeness | — |
| A.5.17 | Authentication information | HIGH | Password complexity and storage requirements are mostly DETERMINISTIC | — |
| A.5.18 | Access rights | MEDIUM | Review frequency is PARAMETERIZED (org-defined) | — |
| A.5.19 | Information security in supplier relationships | CONTESTED | Supplier assessment adequacy | — |
| A.5.20 | Addressing IS in supplier agreements | PARAMETERIZED | Clause content adequacy | — |
| A.5.21 | Managing IS in ICT supply chain *(new 2022)* | CONTESTED | Supply chain risk coverage | — |
| A.5.22 | Monitoring, review, change of supplier services | PARAMETERIZED | Review frequency | — |
| A.5.23 | Information security for cloud use *(new 2022)* | PARAMETERIZED | Cloud-specific control scope | — |
| A.5.24 | IS incident management planning | PARAMETERIZED | Plan completeness | — |
| A.5.25 | Assessment and decision on IS events | PARAMETERIZED | Classification criteria | — |
| A.5.26 | Response to IS incidents | MEDIUM | Response completeness | — |
| A.5.27 | Learning from IS incidents | PARAMETERIZED | Lesson incorporation evidence | — |
| A.5.28 | Collection of evidence | PARAMETERIZED | Chain of custody adequacy | — |
| A.5.29 | IS during disruption | PARAMETERIZED | Continuity plan adequacy | — |
| A.5.30 | ICT readiness for business continuity *(new 2022)* | PARAMETERIZED | RTO/RPO achievability | — |
| A.5.31 | Legal, statutory, regulatory compliance | CONTESTED | Regulatory inventory completeness | — |
| A.5.32 | Intellectual property rights | PARAMETERIZED | License tracking completeness | — |
| A.5.33 | Protection of records | MEDIUM | Retention schedule completeness | — |
| A.5.34 | Privacy/PII protection | CONTESTED | Overlaps with GDPR; "appropriate" standard | — |
| A.5.35 | Independent review of IS | MEDIUM | Audit independence and frequency | — |
| A.5.36 | Compliance with policies and standards | MEDIUM | Compliance check frequency | — |
| A.5.37 | Documented operating procedures | PARAMETERIZED | Completeness criteria | — |

### Theme 2: People controls (8 controls — A.6.x)

| Control | Title | Confidence | Notes |
|---|---|---|---|
| A.6.1 | Screening | PARAMETERIZED | Screening criteria "commensurate with risk and regulations" |
| A.6.2 | Terms and conditions of employment | MEDIUM | IS clause completeness |
| A.6.3 | IS awareness, education, training | PARAMETERIZED | Training frequency and content adequacy |
| A.6.4 | Disciplinary process | PARAMETERIZED | Process adequacy |
| A.6.5 | Responsibilities after termination | MEDIUM | Obligation communication evidence |
| A.6.6 | Confidentiality/NDA agreements | MEDIUM | Agreement content adequacy |
| A.6.7 | Remote working *(new 2022)* | PARAMETERIZED | Remote working controls adequacy |
| A.6.8 | IS event reporting | MEDIUM | Reporting channel availability and awareness |

### Theme 3: Physical controls (14 controls — A.7.x)

| Control | Title | Confidence | Notes |
|---|---|---|---|
| A.7.1 | Physical security perimeters | MEDIUM | Boundary definition adequacy |
| A.7.2 | Physical entry | MEDIUM | Control method adequacy |
| A.7.3 | Securing offices, rooms, facilities | PARAMETERIZED | Threat-based adequacy |
| A.7.4 | Physical security monitoring *(new 2022)* | PARAMETERIZED | Coverage adequacy |
| A.7.5 | Protecting against physical/environmental threats | PARAMETERIZED | Threat coverage |
| A.7.6 | Working in secure areas | MEDIUM | Procedure adequacy |
| A.7.7 | Clear desk and screen | DETERMINISTIC | Binary observable control |
| A.7.8 | Equipment siting and protection | PARAMETERIZED | Threat-based adequacy |
| A.7.9 | Security of assets off-premises *(new 2022)* | PARAMETERIZED | Off-premises control scope |
| A.7.10 | Storage media | PARAMETERIZED | Sanitization method adequacy |
| A.7.11 | Supporting utilities | DETERMINISTIC | UPS, generator, redundancy — measurable |
| A.7.12 | Cabling security | DETERMINISTIC | Physical cable labeling and routing |
| A.7.13 | Equipment maintenance | MEDIUM | Maintenance record completeness |
| A.7.14 | Secure disposal or re-use of equipment | MEDIUM | Sanitization method adequacy |

### Theme 4: Technological controls (34 controls — A.8.x)

| Control | Title | Confidence | Notes |
|---|---|---|---|
| A.8.1 | User endpoint devices | MEDIUM | Endpoint policy completeness |
| A.8.2 | Privileged access rights | HIGH | Privileged account inventory is DETERMINISTIC; usage review is PARAMETERIZED |
| A.8.3 | Information access restriction | MEDIUM | Access rule completeness |
| A.8.4 | Access to source code | MEDIUM | Access control completeness |
| A.8.5 | Secure authentication | HIGH | MFA, session timeout, lockout thresholds are DETERMINISTIC |
| A.8.6 | Capacity management | PARAMETERIZED | Threshold definition is org-defined |
| A.8.7 | Protection against malware | HIGH | AV currency and scan frequency are DETERMINISTIC |
| A.8.8 | Management of technical vulnerabilities | MEDIUM | Patch cadence is PARAMETERIZED (org-defined window) |
| A.8.9 | Configuration management *(new 2022)* | HIGH | Baseline existence and drift detection are DETERMINISTIC |
| A.8.10 | Information deletion *(new 2022)* | MEDIUM | Deletion verification method |
| A.8.11 | Data masking *(new 2022)* | PARAMETERIZED | Masking method adequacy |
| A.8.12 | Data leakage prevention *(new 2022)* | PARAMETERIZED | DLP scope and coverage |
| A.8.13 | Information backup | HIGH | Backup frequency and restore testing cadence are DETERMINISTIC |
| A.8.14 | Redundancy of info processing facilities | PARAMETERIZED | Redundancy adequacy |
| A.8.15 | Logging | HIGH | Log content, retention, and integrity protection are DETERMINISTIC |
| A.8.16 | Monitoring activities *(new 2022)* | PARAMETERIZED | Monitoring coverage |
| A.8.17 | Clock synchronisation | DETERMINISTIC | NTP source and drift tolerance are measurable |
| A.8.18 | Use of privileged utility programs | MEDIUM | Authorization and log completeness |
| A.8.19 | Installation of software on operational systems | MEDIUM | Authorization process completeness |
| A.8.20 | Networks security | MEDIUM | Segmentation adequacy |
| A.8.21 | Security of network services | PARAMETERIZED | Service agreement content |
| A.8.22 | Segregation of networks | MEDIUM | Segmentation boundary adequacy |
| A.8.23 | Web filtering *(new 2022)* | MEDIUM | Filter category coverage |
| A.8.24 | Use of cryptography | MEDIUM | Algorithm selection adequacy |
| A.8.25 | Secure development lifecycle | PARAMETERIZED | SDL completeness |
| A.8.26 | Application security requirements | PARAMETERIZED | Requirements completeness |
| A.8.27 | Secure system architecture and engineering | PARAMETERIZED | Principle coverage |
| A.8.28 | Secure coding *(new 2022)* | PARAMETERIZED | Coding standard adequacy |
| A.8.29 | Security testing in dev and acceptance | PARAMETERIZED | Test scope adequacy |
| A.8.30 | Outsourced development | PARAMETERIZED | Contract clause adequacy |
| A.8.31 | Separation of dev, test, production | DETERMINISTIC | Binary: separated or not |
| A.8.32 | Change management | MEDIUM | Change process completeness |
| A.8.33 | Test information | MEDIUM | Test data anonymization adequacy |
| A.8.34 | Protection of IS during audit testing | PARAMETERIZED | Test impact controls |

---

## Statement of Applicability (SoA) — the central evidence artifact

The SoA is mandatory (Clause 6.1.3d) and declares:
- Which Annex A controls are included
- Justification for inclusion (risk treatment result)
- Justification for exclusion (with rationale)
- Implementation status

The SoA is the primary evidence artifact for certification. All 93 controls must be addressed. Exclusions require documented justification; unexplained exclusions are a major nonconformity.

---

## Open assumption registry

| ID | Control | Summary | Review date |
|---|---|---|---|
| ASSUME-ISO-001 | Clause 4 | Context analysis adequate: external/internal issues documented; interested parties ≥6 categories; ISMS scope with exclusion rationale | 2026-05-20 |
| ASSUME-ISO-002 | Clause 5 | IS policy adequate: top-management approval; objectives; compliance commitment; annual review; communicated to all workers | 2026-05-20 |
| ASSUME-ISO-003 | Clause 7 | IS awareness adequate: annual minimum; all workers (not just IT/security); phishing, policies, consequences, incident reporting | 2026-05-20 |
| ASSUME-ISO-004 | Clause 9.2 | Internal audit: annual full ISMS scope; higher-risk areas more frequent; auditors competent and independent; NCs formally tracked | 2026-05-20 |
| ASSUME-ISO-005 | Clause 10 | Corrective action: NC documented; root cause (5-Whys/fishbone/equivalent); action plan with owner and due date; effectiveness verified | 2026-05-20 |
| ASSUME-ISO-A5-001 | A.5.1 | IS policy review: annually minimum; triggered by significant org/operational/threat changes; "reviewed" = actively examined, not version-bumped | 2026-05-20 |
| ASSUME-ISO-A5-002 | A.5.9 | Asset inventory adequate: all ISMS-scope assets identified; each has owner; classified by sensitivity; reviewed annually | 2026-05-20 |
| ASSUME-ISO-A5-003 | A.5.15 | Access rights review: semi-annual for privileged; annual for standard; triggered on role change, absence, termination, incident | 2026-05-20 |
| ASSUME-ISO-A5-004 | A.5.17 | Auth thresholds: min 12 chars; last 5 prohibited; lockout after 10 attempts; session timeout ≤ 30 min | 2026-05-20 |
| ASSUME-ISO-A5-005 | A.5.20 | Supplier agreement IS clauses: scope of access; security controls; incident notification; right to audit; return/destruction; regulatory compliance | 2026-05-20 |
| ASSUME-ISO-A5-006 | A.5.24–5.28 | IRP adequate: roles + escalation + response procedures + evidence preservation; severity classification; regulatory notification timed; annual exercise | 2026-05-20 |
| ASSUME-ISO-A5-007 | A.5.29–5.30 | BCM: RTO/RPO per BIA; tested annually; ICT recovery demonstrated, not just documented | 2026-05-20 |
| ASSUME-ISO-A6-001 | A.6.1 | Screening: identity + employment history + reference minimum; extended checks (criminal, financial) for sensitive-access roles where legally permitted | 2026-05-20 |
| ASSUME-ISO-A6-002 | A.6.2 | Employment IS terms: IS policy reference; NDA; data protection; acceptable use; IP assignment; reporting obligation; consequences of breach | 2026-05-20 |
| ASSUME-ISO-A6-003 | A.6.3 | IS awareness: annual minimum; new employees before sensitive access; covers phishing, incident reporting, password hygiene, policies, consequences | 2026-05-20 |
| ASSUME-ISO-A6-004 | A.6.5 | Access revocation: involuntary termination = same-day; voluntary = last day at latest; post-employment NDA enforceable | 2026-05-20 |
| ASSUME-ISO-A6-005 | A.6.7 | Remote working: approved encrypted channel (VPN/ZTNA); endpoint MDM + AV + disk encryption + screen lock; home workspace physical guidance | 2026-05-20 |
| ASSUME-ISO-A7-001 | A.7.1 | Physical perimeters adequate: security areas documented; entry points controlled; walls/locked doors; server rooms restricted to authorized personnel only | 2026-05-20 |
| ASSUME-ISO-A7-002 | A.7.2 | Physical entry: access logs exist; authorizations reviewed annually; terminated personnel revoked per ASSUME-ISO-A6-004; visitors escorted | 2026-05-20 |
| ASSUME-ISO-A7-003 | A.7.4 | Physical monitoring: CCTV covers secure area entry points; footage retained ≥ 30 days (90 for high-security); monitoring protected from tampering | 2026-05-20 |
| ASSUME-ISO-A7-004 | A.7.7 | Clear desk/screen: sensitive material cleared when unattended; screen lock ≤ 30 min; cabinets locked; removable media not left in workstations | 2026-05-20 |
| ASSUME-ISO-A7-005 | A.7.9 | Off-premises assets: policy exists; asset loan register; portable devices encrypted; loss/theft reported immediately; removal controls for unauthorized assets | 2026-05-20 |
| ASSUME-ISO-A7-006 | A.7.10 | Storage media: labeled per classification; transport = tamper-evident or encrypted; disposal = ≥3-pass overwrite or degauss or physical destruction; certificates documented | 2026-05-20 |
| ASSUME-ISO-A7-007 | A.7.11 | Supporting utilities: UPS ≥ 30-min runtime; annual load test; temperature 18–27°C; humidity 45–65% RH; automated alerting 24/7 | 2026-05-20 |
| ASSUME-ISO-A7-008 | A.7.13 | Equipment maintenance: per manufacturer spec; records document asset ID + date + work + technician; third-party supervised; media removed before external maintenance | 2026-05-20 |
| ASSUME-ISO-A7-009 | A.7.14 | Equipment disposal: NIST SP 800-88 Clear/Purge for HDD; physical destruction or ATA Secure Erase for SSD; certificate retained until next audit | 2026-05-20 |
| ASSUME-ISO-A8-001 | A.8.2 | Privileged access review: semi-annual for privileged accounts; just-in-time access preferred; privilege escalation logged | 2026-05-20 |
| ASSUME-ISO-A8-002 | A.8.5 | Secure auth: min 12 chars; last 5 prohibited; lockout 10 attempts; MFA for sensitive/remote/privileged; session timeout ≤ 30 min | 2026-05-20 |
| ASSUME-ISO-A8-003 | A.8.7 | Malware: AV on all applicable systems; automatic definition updates; real-time scanning; 24-hour definition currency | 2026-05-20 |
| ASSUME-ISO-A8-004 | A.8.8 | Vulnerability management: CVSS ≥ 7.0 = 30-day remediation SLA; CVSS < 7.0 = 90-day; critical/internet-exposed systems scanned monthly | 2026-05-20 |
| ASSUME-ISO-A8-005 | A.8.9 | Configuration management: CIS Benchmarks Level 1 minimum; automated drift detection; deviations approved and documented | 2026-05-20 |
| ASSUME-ISO-A8-006 | A.8.13 | Backup: daily incremental; weekly full; offsite or cloud copy; restore test ≥ quarterly; RTO/RPO targets met in last test | 2026-05-20 |
| ASSUME-ISO-A8-007 | A.8.15 | Logging: 12-month retention; 3-month immediate access; daily review critical/CHD systems; log integrity protection (write-once/SIEM) | 2026-05-20 |
| ASSUME-ISO-A8-008 | A.8.24 | Cryptography: AES-128/256 for symmetric; RSA-2048+/ECC-256+ for asymmetric; SHA-256+ for hashing; TLS 1.2+; key rotation ≥ annually | 2026-05-20 |

---

## Contested items pending resolution

| Item | Clause/Control | Reason | Resolution path |
|---|---|---|---|
| Risk assessment methodology adequacy | Clause 6.1.2 | ISO 27001 does not prescribe a methodology; auditor evaluates consistency and completeness | ISMS Manager + Compliance Officer document chosen methodology; auditor sign-off at Stage 2 |
| Risk acceptance criteria | Clause 6.1.2 | Residual risk acceptability is a management judgment; cannot be validated by test | Top management sign-off on risk appetite statement |
| Supplier assessment adequacy | A.5.19 | Tiering methodology, assessment depth, and contractual clause adequacy are auditor-evaluated | QSA/ISMS auditor review of supplier risk methodology at annual internal audit |
| ICT supply chain risk (SCRM) | A.5.21 | Software component vetting, SBOM, hardware provenance: adequacy is context-dependent | ISMS Manager review against NIST SP 800-161 guidance; document scope and rationale |
| Legal/regulatory inventory completeness | A.5.31 | Organization must identify all applicable requirements; completeness is auditor-evaluated | Legal counsel review + annual regulatory scan documented |
| PII protection adequacy | A.5.34 | "Appropriate" standard overlaps with GDPR; cross-framework determination required | GDPR registry alignment; DPO sign-off where applicable |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Risk assessment | ISO 27001 Clause 6, NIST 800-53 RA, 800-171 RA | ISO methodology is not specified; organization must define and consistently apply. Can use NIST methodology to satisfy all three. |
| Access control records | ISO 27001 A.5.15–5.18/A.8.2–8.5, NIST 800-53 AC, 800-171 AC | Same IAM system evidence; format requirements differ |
| Audit logs | ISO 27001 A.8.15, NIST 800-53 AU, SOC 2 CC7 | Log content and retention are independently specified; design once to satisfy all |
| Supplier agreements | ISO 27001 A.5.19–5.22, SOC 2 CC9, GDPR Art. 28 DPA | Data processing agreements (DPA) under GDPR can be embedded in the same supplier agreement template |
| Incident management | ISO 27001 A.5.24–5.28, NIST 800-53 IR, SOC 2 CC7 | Incident classification, response, and evidence collection overlap across all three |
| Business continuity | ISO 27001 A.5.29–5.30, SOC 2 A1 (Availability), NIST 800-53 CP | RTO/RPO objectives documented in ISO 27001 can directly supply SOC 2 and NIST CP evidence |

---

## CI/CD gate configuration

Standard three-tier gate (see NERC CIP registry). ISO 27001-specific constraints:

- **SoA version tracking:** SoA document hash tracked in registry; any change triggers re-review of affected tests.
- **Annual management review:** A time-bounded test verifies management review completion within 12 months.
- **Certification validity:** External certification dates tracked; expiry within 30 days triggers Pattern 3 gate.
- **Internal audit cadence:** ISO 27001 Clause 9.2 requires planned intervals; test verifies last audit date is within org-defined interval.

---

## Specification file status

| File | Contents | Assumptions | Confidence | Status |
|---|---|---|---|---|
| `clauses-4-10-isms-mandatory.md` | Mandatory ISMS requirements — Clauses 4–10; SoA (Clause 6.1.3d); internal audit and management review cadences | ASSUME-ISO-001–005 | MEDIUM | ✅ Parsed |
| `annex-a5-organizational.md` | Theme 1: Organizational Controls — 37 controls (A.5.1–A.5.36 selected high-value); A.5.17 auth thresholds; A.5.20 supplier agreements | ASSUME-ISO-A5-001–007 | MEDIUM | ✅ Parsed |
| `annex-a6-people.md` | Theme 2: People Controls — all 8 controls (A.6.1–A.6.8); training cadence; access revocation; NDA; remote working | ASSUME-ISO-A6-001–005 | MEDIUM | ✅ Parsed |
| `annex-a7-physical.md` | Theme 3: Physical Controls — all 14 controls (A.7.1–A.7.14); clear desk/screen; supporting utilities; equipment disposal | ASSUME-ISO-A7-001–009 | MEDIUM | ✅ Parsed |
| `annex-a8-technological.md` | Theme 4: Technological Controls — 34 controls (A.8.1–A.8.34 selected high-value); auth, malware, backup, logging, crypto, configuration | ASSUME-ISO-A8-001–008 | MEDIUM–HIGH | ✅ Parsed |
