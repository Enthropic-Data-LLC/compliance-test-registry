# DORA — EU Digital Operational Resilience Act (2022/2554)

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** All 5 pillars: ICT risk management, incident classification/reporting, resilience testing, third-party risk management, information sharing
**Authority:** Joint Committee of European Supervisory Authorities (EBA, EIOPA, ESMA); national competent authorities per member state
**Enforcing context:** All EU/EEA financial entities: banks, investment firms, insurance companies, pension funds, payment institutions, e-money institutions, crypto-asset service providers (CASPs), central counterparties, trade repositories — and their critical ICT third-party service providers (CTPPs)
**In force:** January 17, 2025 (all requirements effective; no phase-in)

---

## Summary

| Metric | Count |
|---|---|
| Pillars | 5 |
| Total articles | 64 |
| Technically testable article clusters | ~30 |
| Articles parsed (individual files) | 0 (index only; individual article files pending) |
| Fully automated (DETERMINISTIC) | Moderate — incident reporting timelines are DETERMINISTIC; RTO/RPO once documented |
| Partial automation (PARAMETERIZED) | Dominant |
| Human-determination required (CONTESTED) | Significant — "major incident" determination, TLPT scope |
| Open assumptions | 0 |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Proportionality — critical pre-condition

DORA applies proportionality: smaller and less complex entities ("simplified ICT risk management framework" entities) face reduced requirements. Significant institutions face enhanced requirements including Threat-Led Penetration Testing (TLPT).

| Tier | Criteria | Key simplifications |
|---|---|---|
| Standard | Most covered entities | Full requirements |
| Simplified | Small/non-interconnected entities per Art. 16 | Simplified ICT risk framework; no TLPT required |
| Significant (TLPT required) | Identified by competent authority based on systemic importance | TLPT every 3 years; enhanced CTPP oversight |

---

## Pillar 1 — ICT Risk Management (Articles 5–16)

| Article | Requirement | Confidence | Notes |
|---|---|---|---|
| 5 | ICT risk management framework — governance | PARAMETERIZED | Board/management body approval and oversight; roles and responsibilities |
| 6 | ICT risk management framework — content | PARAMETERIZED | Comprehensive written ICT risk management framework |
| 7 | ICT systems, protocols, tools | PARAMETERIZED | Adequate and up-to-date ICT systems; continuous monitoring; documented asset register |
| 8 | Identification | PARAMETERIZED | Complete asset inventory; classification of criticality |
| 9 | Protection and prevention | MEDIUM | Policies covering IAM, change management, patch management, data classification |
| 10 | Detection | PARAMETERIZED | Continuous monitoring mechanisms; anomaly detection |
| 11 | Response and recovery | PARAMETERIZED | Written BCP/DRP; defined RTO/RPO |
| 12 | Backup, restoration, recovery | DETERMINISTIC | RTO/RPO defined and achievable; backup testing at least annually; geographic separation |
| 13 | Learning and evolving | PARAMETERIZED | Post-incident review process; threat intelligence integration |
| 14 | Communication | PARAMETERIZED | Internal and external communication plans for ICT incidents and crises |
| 15 | Integrated ICT risk management framework | PARAMETERIZED | Integration with overall enterprise risk framework |
| 16 | Simplified framework (smaller entities) | PARAMETERIZED | Applies to Art. 16 entities only |

---

## Pillar 2 — ICT Incident Classification and Reporting (Articles 17–23)

This is the highest DETERMINISTIC density pillar.

| Article | Requirement | Confidence | Notes |
|---|---|---|---|
| 17 | ICT incident classification | PARAMETERIZED | Classification criteria: duration, geographic spread, data loss, criticality of affected services, economic impact |
| 18 | Classification of major ICT incidents | PARAMETERIZED | Mandatory criteria: 5 dimensions (per RTS 2024/1515) — number of clients, transactions, geographic spread, data loss, criticality rating, reputational impact, economic impact |
| 19 | Reporting of major ICT incidents | DETERMINISTIC | **Initial notification: within 4 hours** of classification as major AND no later than 24 hours from awareness; **Intermediate report: within 72 hours** of initial notification; **Final report: within 1 month** of incident resolution |
| 20 | Harmonized reporting content | PARAMETERIZED | Report templates issued by ESAs per RTS |
| 21 | Voluntary reporting of significant cyber threats | PARAMETERIZED | Not mandatory; competent authority may provide feedback |
| 22 | Centralized reporting hub | Informational | Member state option to create single reporting hub |
| 23 | Reporting by payment service providers | DETERMINISTIC | Additional PSD2-related reporting for PSPs; does not replace Art. 19 reports |

### DORA incident reporting timeline — DETERMINISTIC reference

| Report | Trigger | Deadline |
|---|---|---|
| Initial notification | Awareness of a potential major ICT incident | ≤ 4 hours after classification as major; ≤ 24 hours from awareness |
| Intermediate report | Following initial notification | ≤ 72 hours from initial notification |
| Final report | After full remediation | ≤ 1 month from submission of intermediate report |

---

## Pillar 3 — Digital Operational Resilience Testing (Articles 24–27)

| Article | Requirement | Confidence | Notes |
|---|---|---|---|
| 24 | General requirements for testing | PARAMETERIZED | Proportionate testing program; all ICT systems and applications |
| 25 | Testing of ICT tools and systems | PARAMETERIZED | Annual basic testing (vulnerability assessments, network security assessments, gap analyses, reviews of controls, penetration testing) |
| 26 | Advanced testing — TLPT | DETERMINISTIC | Threat-Led Penetration Testing every **3 years** for significant entities identified by competent authority; scoped by TIBER-EU framework |
| 27 | Requirements for testers | PARAMETERIZED | External testers required for TLPT; internal testers allowed for basic testing |

---

## Pillar 4 — ICT Third-Party Risk Management (Articles 28–44)

| Article | Requirement | Confidence | Notes |
|---|---|---|---|
| 28 | General principles | PARAMETERIZED | Written TPSP risk management policy; due diligence requirements |
| 29 | Pre-contractual assessment | PARAMETERIZED | Risk assessment before contracting with ICT service providers |
| 30 | Key contractual requirements | PARAMETERIZED | 12 mandatory elements in ICT service contracts (Art. 30(2)) |
| 31 | Critical ICT third-party service providers (CTPPs) | DETERMINISTIC | ESA designation of CTPPs; designated CTPPs subject to EU-level oversight |
| 32 | Oversight framework for CTPPs | DETERMINISTIC | Lead overseer assigned; CTPP must cooperate with oversight activities |
| 33–44 | CTPP oversight activities | PARAMETERIZED/CONTESTED | Investigation powers, recommendations, penalties |

### Art. 30(2) — mandatory ICT contract elements (DETERMINISTIC checklist)

All contracts with ICT service providers supporting critical or important functions must include:
1. Clear description of functions and services
2. Location(s) of data processing
3. Provisions on availability, authenticity, integrity, and confidentiality
4. Access, recovery, return, and destruction of data at termination
5. Service level descriptions and quantitative/qualitative performance targets
6. Relevant provisions for notice and remediation of ICT incidents
7. Cooperation with competent authorities and resolution authorities
8. Termination rights and exit strategies
9. Audit rights (for financial entity and competent authority)
10. Business continuity plans
11. Participation in ICT security awareness training
12. Provisions supporting sub-contracting of critical functions

---

## Pillar 5 — Information Sharing (Articles 45–47)

| Article | Requirement | Confidence | Notes |
|---|---|---|---|
| 45 | Voluntary information sharing arrangements | PARAMETERIZED | Not mandatory; financial entities may participate in threat intelligence sharing |
| 46 | Terms of participation | PARAMETERIZED | Confidentiality, data protection compliance |
| 47 | Role of ESAs | Informational | ESA coordination role |

---

## Open assumption registry

*(No assumptions recorded — individual article files not yet written)*

---

## Contested items pending resolution

| ID | Article | Issue | Status |
|---|---|---|---|
| CONTEST-DORA-001 | Art. 17–18 | "Major incident" classification — 5-dimension criteria require quantitative thresholds per RTS; thresholds vary by entity type | Pending entity-type-specific RTS implementation; Pattern 3 gate in place until entity determines applicable thresholds |
| CONTEST-DORA-002 | Art. 28 | "Critical or important function" determination — which services to classify triggers full Art. 28–30 requirements | Pattern 3 gate; requires senior management determination |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| ICT incident reporting timeline | DORA Art. 19 (4h/72h/1mo), GDPR Art. 33 (72h to DPA), NY DFS §500.17 (72h) | DORA and NY DFS have a 72-hour intermediate report deadline; GDPR is to a different authority. Same IRP infrastructure; different notification targets |
| Business continuity / RTO/RPO | DORA Art. 11–12, ISO 22301 (BCM), SOC 2 A1, NIST 800-53 CP | DORA requires documented and achievable RTO/RPO; shared BCP/DRP artifact |
| Third-party contracts | DORA Art. 30, GDPR Art. 28 DPA, GLBA §314.4(f), SOC 2 CC9.2 | DORA Art. 30 mandatory elements are the most specific; a combined contract template addressing all frameworks is feasible |
| Penetration testing | DORA Art. 25–26, NY DFS §500.05, PCI DSS Req 11.4, GLBA §314.4(g) | DORA TLPT (TIBER-EU) is more rigorous than standard pentests; but annual basic pentest satisfies other frameworks |
| Asset inventory | DORA Art. 8, ISO 27001 A.5.9, NIST 800-53 CM-8 | Single asset inventory satisfies all three if it includes criticality classification required by DORA |
| ICT risk management | DORA Art. 5–15, ISO 27001 Clause 6, NIST 800-53 RA, FFIEC IT Handbooks | DORA requires Board-level approval; same risk assessment artifact can be structured to satisfy all frameworks |

---

## CI/CD gate configuration

Standard three-tier gate (see NERC CIP registry). DORA-specific constraints:

- **Major incident classification trigger:** A time-stamped `incident_aware_at` field starts the 24-hour/4-hour clocks simultaneously. Pattern 1 failure if initial report not dispatched within threshold.
- **CTPP register currency:** Art. 28 register of ICT third-party arrangements must be kept current. New contracts trigger mandatory Art. 29 pre-assessment gate.
- **Contract element completeness:** Art. 30(2) 12-element checklist is a DETERMINISTIC gate on all new ICT contracts for critical/important functions.
- **TLPT cycle:** For designated significant entities, TLPT every 3 years tracked as a time-bounded Pattern 2 test.
- **RTO/RPO achievability:** Backup restoration test records must demonstrate that documented RTO/RPO objectives were achieved. Failure triggers Pattern 2.

---

## Roadmap — individual article file parse priority

| Priority | Article(s) | Notes |
|---|---|---|
| 1 | Art. 19 (incident reporting timelines) | Highest DETERMINISTIC density; 4h/72h/1mo thresholds are immediately automatable |
| 2 | Art. 30(2) (contract mandatory elements) | DETERMINISTIC 12-element checklist |
| 3 | Art. 12 (backup and recovery) | RTO/RPO achievability — DETERMINISTIC once objectives documented |
| 4 | Art. 17–18 (incident classification) | PARAMETERIZED; classification criteria per entity-specific RTS |
| 5 | Art. 28–29 (TPSP due diligence) | PARAMETERIZED; pre-assessment process |
| 6 | Art. 25 (basic resilience testing) | Annual testing cadence — DETERMINISTIC |
| 7 | Art. 26 (TLPT) | 3-year cadence — DETERMINISTIC for significant entities |
| 8 | Art. 7–8 (asset inventory + protection) | PARAMETERIZED |
| 9 | Art. 5–6 (ICT risk framework governance) | PARAMETERIZED; Pattern 3 for board approval gate |
| 10 | Art. 11 (BCP/DRP) | PARAMETERIZED; existence is DETERMINISTIC |
