# SOC 2 — Trust Services Criteria (AICPA TSC 2017)

**Registry version:** 2026.05
**Last updated:** 2026-05-21
**Scope:** Common Criteria (CC1–CC9) + additional criteria for Availability (A1), Confidentiality (C1), Processing Integrity (PI1), Privacy (P1–P8)
**Authority:** American Institute of Certified Public Accountants (AICPA)
**Enforcing context:** Service organization audits (Type I: point-in-time; Type II: 6–12 month period); contractual B2B requirements; vendor risk management programs
**Current version:** TSC 2017 (with 2022 points of focus updates)

---

## Summary

| Metric | Count |
|---|---|
| Trust service categories | 5 (Security + 4 additional) |
| Common Criteria (CC) series | 9 series (CC1–CC9), ~50+ individual criteria |
| Additional criteria | A1 (3), C1 (2), PI1 (5), P1–P8 (~20 across privacy) |
| Criteria parsed (individual files) | 6 (CC6, CC7, A1, CC8+CC5, CC9+C1+PI1, P1–P8 Privacy) |
| Fully automated (DETERMINISTIC) | Moderate — CC6 (access controls, TLS, AV) and CC7.1 (vuln scan cadence) are HIGH; A1.2–A1.3 are MEDIUM-HIGH |
| Partial automation (PARAMETERIZED) | Dominant across CC1–CC5, CC8, CC9, A1.1 |
| Human-determination required (CONTESTED) | CC1.1 (board oversight), CC3.2–CC3.3 (risk methodology, fraud), CC9.2 (vendor adequacy) |
| Unresolvable | Minimal |
| Open assumptions | 25 (ASSUME-SOC2-CC6-001–007, CC7-001–004, A1-001–003, CC8-001, CC5-001, CC4-001, CC9-001–002, C1-001–002, PI1-001; P1-001, P2-001, P3-001, P4-001, P5-001, P6-001, P7-001, P8-001) |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Trust service category scope

When engaging for a SOC 2, the service organization selects which categories apply. Security (CC) is always required. Additional categories are opt-in based on customer commitments.

| Category | Required? | Criteria | Typical use case |
|---|---|---|---|
| Security | Always | CC1–CC9 | All SOC 2 engagements |
| Availability | Optional | A1.1–A1.3 | SLA-bound services; uptime commitments |
| Confidentiality | Optional | C1.1–C1.2 | Services handling sensitive client data |
| Processing Integrity | Optional | PI1.1–PI1.5 | Transaction processing; financial data services |
| Privacy | Optional | P1–P8 (~20 criteria) | Services processing personal information |

---

## Common Criteria — per-series confidence map

### CC1: Control Environment (COSO — 5 criteria)

| Series | Focus | Confidence | PARAMETERIZED surface | CONTESTED surface |
|---|---|---|---|---|
| CC1.1 | Board oversight of security | CONTESTED | — | Board competency determination; governance structure adequacy |
| CC1.2 | Ethical values and independence | CONTESTED | — | Independence determination; code of conduct adequacy |
| CC1.3 | Management structure and reporting | PARAMETERIZED | Organizational structure completeness | — |
| CC1.4 | Competence and development | PARAMETERIZED | Competency criteria and training adequacy | — |
| CC1.5 | Accountability | PARAMETERIZED | Performance metrics appropriateness | — |

### CC2: Communication and Information (3 criteria)

| Series | Focus | Confidence | Notes |
|---|---|---|---|
| CC2.1 | Relevant quality information | PARAMETERIZED | Information completeness and timeliness |
| CC2.2 | Internal communication | PARAMETERIZED | Communication adequacy |
| CC2.3 | External communication | PARAMETERIZED | System description accuracy (critical for SOC 2 report boundary) |

### CC3: Risk Assessment (4 criteria)

| Series | Focus | Confidence | Notes |
|---|---|---|---|
| CC3.1 | Objectives specification | PARAMETERIZED | Objective completeness |
| CC3.2 | Risk identification and analysis | CONTESTED | Risk methodology acceptability |
| CC3.3 | Fraud risk | CONTESTED | Fraud scenario completeness |
| CC3.4 | Change risk identification | PARAMETERIZED | Change risk analysis scope |

### CC4: Monitoring Activities (2 criteria)

| Series | Focus | Confidence | Notes |
|---|---|---|---|
| CC4.1 | Ongoing and separate evaluations | PARAMETERIZED | Evaluation frequency and scope |
| CC4.2 | Communication of deficiencies | MEDIUM | Deficiency reporting timeliness |

### CC5: Control Activities (3 criteria)

| Series | Focus | Confidence | Notes |
|---|---|---|---|
| CC5.1 | Control selection and development | PARAMETERIZED | Control coverage adequacy |
| CC5.2 | Technology controls | MEDIUM | General IT control framework adequacy |
| CC5.3 | Policy deployment | PARAMETERIZED | Deployment and adherence evidence |

### CC6: Logical and Physical Access Controls (8 criteria) — HIGH DETERMINISTIC DENSITY

| Series | Focus | Confidence | Notes |
|---|---|---|---|
| CC6.1 | Logical access security | HIGH | Access provisioning process, MFA enforcement, least privilege — DETERMINISTIC checkpoints |
| CC6.2 | User authentication | HIGH | Authentication method, lockout thresholds, session timeout — DETERMINISTIC |
| CC6.3 | Access removal | HIGH | Offboarding timeline — PARAMETERIZED window; completeness is DETERMINISTIC |
| CC6.4 | Physical access | MEDIUM | Physical entry log, badge system — DETERMINISTIC existence; coverage is PARAMETERIZED |
| CC6.5 | Logical access removal | HIGH | Same as CC6.3 — technical revocation is DETERMINISTIC |
| CC6.6 | Boundary protection | HIGH | Firewall rules, network segmentation — DETERMINISTIC existence; rule adequacy is PARAMETERIZED |
| CC6.7 | Data transmission protection | HIGH | TLS version, encryption in transit — DETERMINISTIC thresholds |
| CC6.8 | Malware and unauthorized software | HIGH | AV deployment, file integrity monitoring — DETERMINISTIC |

### CC7: System Operations (5 criteria) — HIGH DETERMINISTIC DENSITY

| Series | Focus | Confidence | Notes |
|---|---|---|---|
| CC7.1 | Vulnerability management | HIGH | Scan frequency (quarterly minimum), CVSS thresholds, patch SLAs — DETERMINISTIC |
| CC7.2 | Anomaly detection and monitoring | MEDIUM | Alert rule coverage — PARAMETERIZED |
| CC7.3 | Security incident response | MEDIUM | Response plan completeness — PARAMETERIZED; response time SLA — DETERMINISTIC |
| CC7.4 | Incident response and recovery | MEDIUM | Containment, eradication, recovery completeness — PARAMETERIZED |
| CC7.5 | Identification of relevant threats | PARAMETERIZED | Threat landscape coverage adequacy |

### CC8: Change Management (1 criterion)

| Series | Focus | Confidence | Notes |
|---|---|---|---|
| CC8.1 | Change management process | MEDIUM | Change authorization and testing completeness — PARAMETERIZED |

### CC9: Risk Mitigation (2 criteria)

| Series | Focus | Confidence | Notes |
|---|---|---|---|
| CC9.1 | Risk mitigation activities | PARAMETERIZED | Mitigation coverage and effectiveness |
| CC9.2 | Vendor/business partner risk management | CONTESTED | Vendor assessment adequacy; SOC 2 pass-through requirements |

---

## Additional criteria — confidence map

### Availability (A1) — 3 criteria

| Criterion | Focus | Confidence | Notes |
|---|---|---|---|
| A1.1 | Availability capacity management | PARAMETERIZED | Capacity threshold definitions (org-defined) |
| A1.2 | Environmental and software threats | MEDIUM | Backup frequency, redundancy — DETERMINISTIC; adequacy — PARAMETERIZED |
| A1.3 | Recovery testing | MEDIUM | Recovery test frequency and RTO achievement — DETERMINISTIC; test scope — PARAMETERIZED |

### Confidentiality (C1) — 2 criteria

| Criterion | Focus | Confidence | Notes |
|---|---|---|---|
| C1.1 | Confidential information identification | PARAMETERIZED | Classification criteria adequacy |
| C1.2 | Confidential information disposal | MEDIUM | Disposal method — PARAMETERIZED; documentation — DETERMINISTIC |

### Processing Integrity (PI1) — 5 criteria

| Criterion | Focus | Confidence | Notes |
|---|---|---|---|
| PI1.1–PI1.5 | Complete, valid, accurate, timely, authorized processing | MEDIUM | Input validation and output verification are DETERMINISTIC; completeness determination is PARAMETERIZED |

### Privacy (P1–P8) — ~20 criteria

| Series | Focus | Confidence | Notes |
|---|---|---|---|
| P1 | Privacy notice | PARAMETERIZED | Notice completeness and accuracy |
| P2 | Choice and consent | CONTESTED | Consent mechanism adequacy; opt-out effectiveness |
| P3 | Collection | PARAMETERIZED | Collection limitation scope |
| P4 | Use, retention, disposal | PARAMETERIZED | Use limitation and retention schedule |
| P5 | Access | MEDIUM | Subject access request fulfillment — timeliness is DETERMINISTIC |
| P6 | Disclosure and notification | MEDIUM | Breach notification timeliness — DETERMINISTIC (if time bound); scope — PARAMETERIZED |
| P7 | Quality | PARAMETERIZED | Data accuracy maintenance |
| P8 | Monitoring and enforcement | PARAMETERIZED | Privacy program enforcement evidence |

---

## Type I vs. Type II distinction

| Type | Period | Evidence basis | CI gate implication |
|---|---|---|---|
| Type I | Point in time (single date) | Controls designed and in place as of the report date | Tests run as of report date; no period evidence required |
| Type II | 6–12 month period | Controls operating effectively throughout the period | Tests must include sampling evidence across the period; log-based tests must cover full period |

Type II is the meaningful commitment for customers. Type I is a design assessment only.

---

## System Description boundary — critical pre-condition

SOC 2 applies only to the services described in the system description (CC2.3). The system boundary determines which components, people, processes, and third parties are in scope. The boundary is a human-attested artifact.

All tests are gated by: `component_in_system_boundary()` — a fixture requiring the system description to be current (< 12 months since last review for Type II).

---

## Open assumption registry

| ID | Criterion | Summary | Review date |
|---|---|---|---|
| ASSUME-SOC2-CC1-001 | CC1.2 | Code of conduct: documented; annual acknowledgment; whistleblower line available | 2026-05-20 |
| ASSUME-SOC2-CC1-002 | CC1.3 | Management structure: CISO designated; security roles defined; reporting lines appropriate to org size | 2026-05-20 |
| ASSUME-SOC2-CC2-001 | CC2.3 | System description: infrastructure accurately listed; commitments match agreements; subservice orgs identified; reviewed annually | 2026-05-20 |
| ASSUME-SOC2-CC4-001 | CC4.2 | Deficiency communication: significant deficiencies ≤30 days to senior management; material weaknesses ≤60 days to board | 2026-05-20 |
| ASSUME-SOC2-CC5-001 | CC5.3 | Policy deployment: documented; annual review; all staff acknowledged; procedures for all significant controls | 2026-05-20 |
| ASSUME-SOC2-CC6-001 | CC6.1 | Logical access: formal request-and-approval workflow; least-privilege; separate privileged accounts; semi-annual privileged review | 2026-05-20 |
| ASSUME-SOC2-CC6-002 | CC6.2 | Auth thresholds: ≥12 chars; lockout ≤10; idle timeout ≤15 min (CDE/confidential) / ≤30 min (other); MFA for remote/privileged | 2026-05-20 |
| ASSUME-SOC2-CC6-003 | CC6.3/CC6.5 | Access removal: involuntary = same day; voluntary = last working day; role change ≤5 days; quarterly roster review | 2026-05-20 |
| ASSUME-SOC2-CC6-004 | CC6.4 | Physical access: badge or key to all SOC 2 areas; access logs; visitors escorted; annual review + immediate on termination | 2026-05-20 |
| ASSUME-SOC2-CC6-005 | CC6.6 | Boundary protection: default deny-all inbound; DMZ architecture; firewall rules reviewed semi-annually; IDS/IPS deployed | 2026-05-20 |
| ASSUME-SOC2-CC6-006 | CC6.7 | Transmission: TLS 1.2+ min; AEAD only; SSL/TLS 1.0/1.1 disabled; internal confidential comms also encrypted | 2026-05-20 |
| ASSUME-SOC2-CC6-007 | CC6.8 | Anti-malware: AV on all general-purpose OS in boundary; 24h definition currency; real-time scanning; users cannot disable | 2026-05-20 |
| ASSUME-SOC2-CC7-001 | CC7.1 | Vuln mgmt: quarterly internal + external scans; critical CVSS≥9.0 ≤30 days; high CVSS 7.0–8.9 ≤60 days; KEV review ≤72 hours | 2026-05-20 |
| ASSUME-SOC2-CC7-002 | CC7.2 | Monitoring: SIEM covering boundary; alert rules for failed logins/privilege escalation/large exports; critical alerts ≤15 min review | 2026-05-20 |
| ASSUME-SOC2-CC7-003 | CC7.3 | IRP: documented; P1 response ≤1 hour; incidents tracked; customer notification per SLA/regulation; annual tabletop test | 2026-05-20 |
| ASSUME-SOC2-CC7-004 | CC7.4 | Incident response/recovery: containment + eradication + recovery documented; RCA for P1/P2; PIR within 5 business days | 2026-05-20 |
| ASSUME-SOC2-CC8-001 | CC8.1 | Change management: documented workflow; normal = request+impact+test+rollback+approval; emergency reviewed ≤5 days; no self-approval | 2026-05-20 |
| ASSUME-SOC2-CC9-001 | CC9.1 | Risk mitigation: all risks have treatment decision; accepted risks have owner sign-off; residual risk re-evaluated annually | 2026-05-20 |
| ASSUME-SOC2-CC9-002 | CC9.2 | Vendor risk: critical vendors assessed via SOC 2 or equivalent annually; all agreements include security obligations + breach notification | 2026-05-20 |
| ASSUME-SOC2-A1-001 | A1.1 | Capacity: CPU/memory/disk/network monitored; warning 80% sustained; capacity planning annual; peak-load tested against SLA | 2026-05-20 |
| ASSUME-SOC2-A1-002 | A1.2 | Backup: daily incremental; weekly full; offsite/cloud; encrypted; ≥30-day retention; integrity verified | 2026-05-20 |
| ASSUME-SOC2-A1-003 | A1.3 | Recovery testing: annual full restore; quarterly data restore; RTO/RPO documented and met; production-representative environment | 2026-05-20 |
| ASSUME-SOC2-C1-001 | C1.1 | Confidential classification: policy defines criteria; data inventory with labels; training covers handling obligations | 2026-05-20 |
| ASSUME-SOC2-C1-002 | C1.2 | Confidential disposal: crypto shredding/overwrite (digital); NIST SP 800-88 (media); cross-cut shred (paper); disposal certs issued | 2026-05-20 |
| ASSUME-SOC2-PI1-001 | PI1.1–PI1.5 | Processing integrity: input validation; error monitoring; reconciliation controls; output delivery logs; corrections require authorization | 2026-05-20 |
| ASSUME-SOC2-P1-001 | P1.2–P1.4 | Privacy notice: 8 required elements; updated within 30 days of material change; third-party privacy commitments communicated via contract before disclosure | 2026-11-01 |
| ASSUME-SOC2-P2-001 | P2.1–P2.2 | Consent: opt-out acceptable for non-sensitive data; opt-in required for sensitive; withdrawal processed within 30 days; annual Privacy Officer attestation of mechanism adequacy | 2026-11-01 |
| ASSUME-SOC2-P3-001 | P3.2 | Sensitive data collection: explicit opt-in required unless legal obligation/vital interests/public task/documented legitimate interests applies | 2026-11-01 |
| ASSUME-SOC2-P4-001 | P4.2–P4.3 | Retention: schedule per category reviewed annually; automated deletion/archival triggers configured; disposal documented (date, category, method, approver); crypto shredding or NIST 800-88 | 2026-11-01 |
| ASSUME-SOC2-P5-001 | P5.1–P5.2 | Access response: 30 days (extendable to 60 with notice); correction acknowledged 10 days; resolved 30 days; denial includes reason + appeal mechanism | 2026-11-01 |
| ASSUME-SOC2-P6-001 | P6.2–P6.7 | Third-party contracts: 5 required terms including use limitation, security, incident notification (72h), no onward transfer, return/destroy; breach notification timeline: 72h for high-risk, 30 days standard | 2026-11-01 |
| ASSUME-SOC2-P7-001 | P7.1 | Data quality: self-service update available; annual quality review; source system refresh cascades to downstream copies; higher-stakes data reviewed more frequently | 2026-11-01 |
| ASSUME-SOC2-P8-001 | P8.1 | Privacy monitoring: annual Privacy Officer review covering 6 areas; complaints responded within 30 days; incident log maintained; material issues escalated to senior management | 2026-11-01 |

---

## Contested items pending resolution

| Item | Criterion | Reason | Resolution path |
|---|---|---|---|
| Board oversight adequacy | CC1.1 | Board competency and governance effectiveness cannot be measured by test | Auditor walkthrough + board meeting minutes review |
| Code of conduct independence | CC1.2 | Independence of oversight roles is auditor judgment | External auditor evaluation |
| Risk assessment methodology | CC3.2 | Methodology adequacy is auditor-evaluated; no prescriptive standard | ISMS Manager documents methodology rationale; auditor sign-off |
| Fraud risk scenario completeness | CC3.3 | Fraud scenario adequacy depends on business context | Management sign-off on fraud risk assessment scope |
| Vendor/subservice assessment depth | CC9.2 | Tiering adequacy, assessment depth, and carve-out vs. inclusive method are judgment calls | QSA/auditor review of vendor risk methodology |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Audit logs | SOC 2 CC7, ISO 27001 A.8.15, NIST 800-53 AU, HIPAA §164.312(b) | Log retention and content; design once to satisfy all four |
| Access control records | SOC 2 CC6, ISO 27001 A.5.15–5.18, NIST 800-53 AC, HIPAA §164.312(a) | IAM provisioning/deprovisioning records satisfy all |
| Vulnerability management | SOC 2 CC7.1, ISO 27001 A.8.8, NIST 800-53 RA-5/SI-2, PCI DSS Req. 11 | Scan frequency and remediation SLAs aligned across frameworks |
| Vendor/third-party management | SOC 2 CC9.2, ISO 27001 A.5.19–5.22, GDPR Art. 28, HIPAA BAA | Single vendor assessment and agreement template can satisfy all four |
| Business continuity / availability | SOC 2 A1, ISO 27001 A.5.29–5.30, NIST 800-53 CP | RTO/RPO testing records shared |
| Privacy / PII | SOC 2 P series, GDPR, HIPAA Privacy Rule | Privacy criteria overlap significantly; combined data inventory and notice satisfy multiple |

---

## CI/CD gate configuration

Standard three-tier gate (see NERC CIP registry). SOC 2-specific constraints:

- **Period evidence accumulation (Type II only):** Log-based tests must track evidence across the full engagement period (typically 12 months). Evidence age gates check that log sources were active throughout.
- **System description currency:** Stale system description (> 12 months without review) triggers Pattern 3 block.
- **Subservice organization reliance:** If CC9.2 relies on subservice organization SOC 2 reports, those reports must be current (< 12 months) and in scope.

---

## Specification file status

| File | Contents | Assumptions | Confidence | Status |
|---|---|---|---|---|
| `cc6-logical-physical-access.md` | CC6.1–CC6.8: access controls, MFA, TLS, AV, boundary protection | ASSUME-SOC2-CC6-001–007 | HIGH | ✅ Parsed |
| `cc7-system-operations.md` | CC7.1–CC7.5: vulnerability management, monitoring, incident response, recovery | ASSUME-SOC2-CC7-001–004 | HIGH | ✅ Parsed |
| `a1-availability.md` | A1.1–A1.3: capacity management, backup, recovery testing | ASSUME-SOC2-A1-001–003 | MEDIUM | ✅ Parsed |
| `cc8-cc5-change-control-activities.md` | CC8.1 change management; CC5.1–CC5.3 control activities and policy deployment | ASSUME-SOC2-CC8-001, CC5-001 | MEDIUM | ✅ Parsed |
| `cc9-c1-pi1-additional-criteria.md` | CC9.1–CC9.2 risk mitigation and vendor risk; C1.1–C1.2 confidentiality; PI1.1–PI1.5 processing integrity | ASSUME-SOC2-CC9-001–002, C1-001–002, PI1-001 | MEDIUM | ✅ Parsed |
| `cc1-cc2-cc3-cc4-governance-risk.md` | CC1.1–CC1.5 control environment; CC2.1–CC2.3 communication; CC3.1–CC3.4 risk assessment; CC4.1–CC4.2 monitoring | ASSUME-SOC2-CC1-001–002, CC2-001, CC4-001 | LOW–MEDIUM | ✅ Parsed |
| `p-series-privacy.md` | P1 (notice — elements, delivery, update), P2 (consent mechanisms, withdrawal), P3 (collection limitation, sensitive data opt-in), P4 (use limitation, retention schedules, disposal), P5 (access response deadline, correction), P6 (disclosure basis, third-party contracts, breach notification), P7 (data quality review), P8 (privacy program monitoring, complaints, incident log, annual attestation) | ASSUME-SOC2-P1-001–P8-001 | MEDIUM (P1, P4, P5) / LOW-MEDIUM (P2, P3, P6, P7, P8) | ✅ Parsed |
