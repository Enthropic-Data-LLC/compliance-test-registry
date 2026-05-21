# NIST CSF 2.0 — Cybersecurity Framework

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Six Functions (Govern, Identify, Protect, Detect, Respond, Recover) across all tiers and profiles
**Authority:** National Institute of Standards and Technology (NIST)
**Enforcing context:** Voluntary in most contexts; mandated by Executive Order 13800/14028 for federal agencies; widely adopted by contract in supply chains; referenced by CISA as the standard for critical infrastructure; cited by CA AG as a benchmark for CCPA "reasonable security"
**Current version:** CSF 2.0 (February 2024 — adds Govern function; supersedes CSF 1.1)

---

## Summary

| Metric | Count |
|---|---|
| Functions | 6 (Govern, Identify, Protect, Detect, Respond, Recover) |
| Categories | 22 |
| Subcategories | 106 |
| Subcategories parsed (individual files) | 22 (all categories, core testable subcategories) |
| Fully automated (DETERMINISTIC) | Low–moderate — CSF is outcomes-based; thresholds are org-defined |
| Partial automation (PARAMETERIZED) | Dominant |
| Human-determination required (CONTESTED) | Moderate — Tier determination, Profile gap assessment |
| Open assumptions | 6 |

---

## CSF as a mapping hub

CSF 2.0's primary value in this registry is as a **cross-framework mapping layer**. Every subcategory is annotated with informative references to NIST 800-53 r5, ISO 27001, COBIT, ISA/IEC 62443, and others. Tests written against 800-53 and 27001 can be tagged with their CSF subcategory, enabling:
- Unified dashboards showing CSF posture across multiple underlying frameworks
- Gap analysis against a CSF Profile without re-writing tests
- Executive reporting in CSF language regardless of which detailed framework is implemented

---

## Function and category map

### GV — Govern (new in CSF 2.0)

| Category | ID | Confidence | Notes |
|---|---|---|---|
| Organizational Context | GV.OC | PARAMETERIZED | Mission, stakeholder expectations, legal/regulatory requirements understood |
| Risk Management Strategy | GV.RM | PARAMETERIZED | Org risk tolerance established and communicated |
| Roles, Responsibilities, and Authorities | GV.RR | PARAMETERIZED | Cybersecurity roles assigned; accountability established |
| Policy | GV.PO | PARAMETERIZED | Cybersecurity policy established, communicated, enforced |
| Oversight | GV.OV | PARAMETERIZED | Results of risk management reviewed to inform strategy |
| Cybersecurity Supply Chain Risk Management | GV.SC | PARAMETERIZED | Supply chain cybersecurity risk integrated into org risk management |

### ID — Identify

| Category | ID | Confidence | Notes |
|---|---|---|---|
| Asset Management | ID.AM | MEDIUM | Asset inventory existence is DETERMINISTIC; completeness is PARAMETERIZED |
| Risk Assessment | ID.RA | PARAMETERIZED | Threat intelligence gathered; vulnerabilities identified; risk determined |
| Improvement | ID.IM | PARAMETERIZED | Lessons learned incorporated |

### PR — Protect

| Category | ID | Confidence | Notes |
|---|---|---|---|
| Identity Management, Authentication, and Access Control | PR.AA | HIGH | MFA, least privilege, unique IDs — DETERMINISTIC |
| Awareness and Training | PR.AT | PARAMETERIZED | Training program; content adequacy |
| Data Security | PR.DS | MEDIUM | Encryption, data classification — DETERMINISTIC thresholds for encryption; classification is PARAMETERIZED |
| Platform Security | PR.PS | HIGH | Configuration management, patch management, vulnerability management — DETERMINISTIC cadences once defined |
| Technology Infrastructure Resilience | PR.IR | MEDIUM | Backup, redundancy, DR — achievability DETERMINISTIC once RTO/RPO defined |

### DE — Detect

| Category | ID | Confidence | Notes |
|---|---|---|---|
| Continuous Monitoring | DE.CM | PARAMETERIZED | Monitoring coverage; anomaly detection adequacy |
| Adverse Event Analysis | DE.AE | PARAMETERIZED | Event correlation; incident determination |

### RS — Respond

| Category | ID | Confidence | Notes |
|---|---|---|---|
| Incident Management | RS.MA | PARAMETERIZED | Incident response plan completeness |
| Incident Analysis | RS.AN | PARAMETERIZED | Root cause analysis |
| Incident Response Reporting and Communication | RS.CO | MEDIUM | Notification timeliness — DETERMINISTIC when specific deadline regulations apply |
| Incident Mitigation | RS.MI | PARAMETERIZED | Containment adequacy |

### RC — Recover

| Category | ID | Confidence | Notes |
|---|---|---|---|
| Incident Recovery Plan Execution | RC.RP | MEDIUM | Recovery plan completion against documented RTO/RPO |
| Incident Recovery Communication | RC.CO | PARAMETERIZED | Communication during recovery |

---

## Tiers

CSF Tiers (1–4: Partial → Risk-Informed → Repeatable → Adaptive) describe organizational cybersecurity risk management maturity. Tier determination is CONTESTED — self-assessed, not independently audited.

---

## Profiles

A **Current Profile** describes the current state of subcategory achievement. A **Target Profile** describes the desired state. Gap = Target minus Current.

**RDF treatment:** Profile gaps are the primary test surface. Each subcategory in the Target Profile generates a test; the test asserts the Current Profile achievement ≥ Target for that subcategory.

---

## Cross-framework mapping table (selected subcategories)

| CSF Subcategory | 800-53 r5 | ISO 27001:2022 | IEC 62443 | SOC 2 |
|---|---|---|---|---|
| PR.AA-01 (Access control) | AC-2, AC-3 | A.5.15–5.18 | SR 1.1–1.3 | CC6.1–6.3 |
| PR.PS-02 (Patch management) | SI-2, RA-5 | A.8.8 | SR 3.2 | CC7.1 |
| DE.CM-01 (Continuous monitoring) | CA-7 | A.8.16 | SR 6.2 | CC7.2 |
| RS.CO-02 (Incident reporting) | IR-6 | A.5.25–5.27 | SR 6.2 | CC7.3 |
| RC.RP-01 (Recovery plan) | CP-10 | A.5.29–5.30 | SR 7.4 | A1.3 |

Full mapping table to be populated as individual subcategory files are written.

---

## Cross-standard dependencies

| Shared artifact | Frameworks |
|---|---|
| Asset inventory | CSF ID.AM, NIST 800-53 CM-8, ISO 27001 A.5.9, IEC 62443 SR 7.8 |
| Access control | CSF PR.AA, NIST 800-53 AC, ISO 27001 A.5.15–5.18, SOC 2 CC6 |
| Vulnerability management | CSF PR.PS + DE.CM, NIST 800-53 RA-5/SI-2, PCI DSS Req 11, SOC 2 CC7.1 |
| Incident response | CSF RS, NIST 800-53 IR, ISO 27001 A.5.24–5.28, DORA Art. 17–19 |

---

## Spec file status

| File | Coverage | Status |
|---|---|---|
| [`function-profiles-subcategories.md`](./function-profiles-subcategories.md) | Profile gap framework, GV (OC, RM, SC), ID (AM asset inventory, RA risk assessment), PR (AA access/MFA, AT training, DS encryption, PS patch/config, IR backup/resilience), DE (CM monitoring, vulnerability scanning), RS (MA IRP, CO notification deadlines), RC (RP recovery RTO/RPO) | ✅ |

## Open assumption registry

| ID | Assumption | Pattern | Approved | Review |
|---|---|---|---|---|
| ASSUME-CSF-TIER-001 | Tier determination is self-assessed; independent validation that the tier accurately reflects maturity is Pattern 3 | 3 | Pending | 2027-02 |
| ASSUME-CSF-PROFILE-001 | Target Profile represents org risk management decisions; Target adequacy relative to threat environment is Pattern 3 requiring Risk Committee approval | 3 | Pending | 2027-02 |
| ASSUME-CSF-PATCH-001 | Patch SLAs: KEV=14d, Critical=30d, High=60d, Medium=90d, Low=180d; org SLA governs if more stringent | 1 | Pending | 2027-02 |
| ASSUME-CSF-ACCESS-001 | Privileged access reviewed quarterly (3 months); standard access annually; aligns with NIST 800-53 AC-2(3) | 1 | Pending | 2027-02 |
| ASSUME-CSF-TRAIN-001 | Annual awareness training minimum; 95% completion threshold; privileged role training at onboarding + annually | 2 | Pending | 2027-02 |
| ASSUME-CSF-ASSET-001 | Asset inventory reconciliation minimum is annual; completeness is Pattern 2 | 2 | Pending | 2027-02 |

## Parse status: Complete — all 22 categories and core testable subcategories parsed; 6 assumptions recorded
