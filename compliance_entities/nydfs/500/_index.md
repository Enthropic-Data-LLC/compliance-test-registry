# NY DFS 23 NYCRR 500 — Cybersecurity Requirements for Financial Services Companies

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Full regulation as amended November 2023 (Second Amendment)
**Authority:** New York State Department of Financial Services (NY DFS)
**Enforcing context:** All entities holding a NY DFS license, registration, charter, or certificate — includes insurance companies, banks, mortgage companies, money transmitters, virtual currency businesses licensed under BitLicense, and foreign banks with NY branches
**Current version:** 23 NYCRR 500 with Second Amendment (effective Nov 1 2023; most new requirements phased in through Nov 2025)

---

## Summary

| Metric | Count |
|---|---|
| Sections | 23 (§500.00–§500.22) |
| Requirements parsed (individual files) | 1 (`cybersecurity-program.md` — §§500.04, 500.05, 500.06, 500.07, 500.12, 500.14, 500.15, 500.17, Class A) |
| Fully automated (DETERMINISTIC) | High — NY DFS is among the most technically prescriptive financial cybersecurity regulations |
| Partial automation (PARAMETERIZED) | Moderate |
| Human-determination required (CONTESTED) | Low–Moderate |
| Open assumptions | 8 (ASSUME-NYDFS500-CISO-001, PENTEST-001, AUDIT-001, MFA-001, ENC-001, NOTIF-001, CLASSA-001, TRAIN-001) |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Exemptions — critical pre-condition

| Exemption | Criteria | Scope reduction |
|---|---|---|
| Limited exemption | < 10 employees + < $5M gross revenue + < $10M year-end assets (all three) | Exempt from §§500.04, 500.05, 500.06, 500.08, 500.10, 500.12, 500.14, 500.15 |
| Captive insurance company | No direct NY customers; no employees | Exempt from most requirements |
| Class A company (enhanced) | > $20B consolidated assets OR > 2,000 employees (global) | Subject to ADDITIONAL requirements: annual pentest, bi-annual vulnerability assessment, independent audit |

Exemption status is a DETERMINISTIC pre-condition filter on all tests.

---

## Per-section confidence map

| Section | Title | Confidence | PARAMETERIZED surface | CONTESTED surface |
|---|---|---|---|---|
| §500.02 | Cybersecurity program | PARAMETERIZED | Program adequacy based on risk assessment | — |
| §500.03 | Cybersecurity policy | PARAMETERIZED | Policy completeness (14 required topic areas) | — |
| §500.04 | CISO | DETERMINISTIC | Named CISO required; reports at least annually to board | — |
| §500.05 | Penetration testing | DETERMINISTIC | Annual pentest (Class A: annual pentest + bi-annual vuln assessment) | — |
| §500.06 | Audit trail | DETERMINISTIC | 6-year retention; activity on critical systems | — |
| §500.07 | Access privileges | HIGH | Least privilege; MFA; review at least annually | Review scope |
| §500.08 | Application security | PARAMETERIZED | Written procedures for application security in SDLC | — |
| §500.09 | Risk assessment | PARAMETERIZED | Annual written risk assessment; methodology is org-defined | — |
| §500.10 | Cybersecurity personnel | PARAMETERIZED | Qualified personnel/service providers; training | — |
| §500.11 | Third-party service provider security | PARAMETERIZED | Written TPSP security policy; contract requirements | — |
| §500.12 | Multi-factor authentication | DETERMINISTIC | MFA required for all remote access; all privileged accounts; all web-based services with external users |
| §500.13 | Data retention limitations | PARAMETERIZED | Policies to dispose of NPI after no longer needed | — |
| §500.14 | Training and monitoring | PARAMETERIZED | Annual training; monitoring of authorized users for anomalous activity | — |
| §500.15 | Encryption | DETERMINISTIC | NPI encrypted in transit; NPI encrypted at rest (or compensating controls with annual CISO review) | — |
| §500.16 | Incident response plan | PARAMETERIZED | Written IRP with 6 required elements | — |
| §500.17 | Notices to superintendent | DETERMINISTIC | 72-hour notification for "cybersecurity events" meeting threshold |
| §500.19 | Exemptions | DETERMINISTIC | Exemption status determination and annual notice |
| §500.20 | Enforcement | Statutory | — | — |
| §500.21 | Effective dates and phase-in | DETERMINISTIC | Phase-in schedule tracked by requirement |

---

## Key DETERMINISTIC thresholds

| Requirement | Threshold | Section |
|---|---|---|
| Cybersecurity event notification | 72 hours from determination that a reportable event occurred | §500.17(a) |
| CISO board reporting | At least annually | §500.04(b) |
| Penetration testing | At least annually (Class A: annually + bi-annual vuln assessment) | §500.05 |
| Audit trail retention | 6 years | §500.06 |
| MFA — remote access | Required for all remote network access | §500.12(a) |
| MFA — privileged accounts | Required for all privileged accounts | §500.12(a) |
| MFA — external web services | Required for all web-based services with external user access | §500.12(b) |
| Encryption in transit | Required for all NPI in transit | §500.15(a) |
| Encryption at rest | Required or CISO-reviewed compensating controls | §500.15(b) |
| Access review | At least annually | §500.07(a)(3) |
| Annual certification | Annual Board certification of compliance filed with DFS | §500.17(b) |
| Annual cybersecurity training | At least annually | §500.14(a) |

---

## Class A enhanced requirements

Companies with > $20B consolidated assets OR > 2,000 employees face additional requirements:

| Requirement | Threshold | Notes |
|---|---|---|
| Annual penetration test | At least annually (same as standard) | Must also include bi-annual vulnerability assessment |
| Bi-annual vulnerability assessment | Every 6 months | Independent of pentest |
| Independent audit | Annual audit of cybersecurity program | Must be independent and include external party |
| Privileged access management | Formal PAM program required | In addition to standard MFA requirement |
| Endpoint detection and response | EDR solution required | Covers all endpoints |
| CISO attestation | CISO must attest to penetration test results | In addition to standard board reporting |

---

## §500.17 — Cybersecurity event reporting scope

Not all incidents require DFS notification. Reporting is triggered when a "cybersecurity event" meets ANY of:
- Notice to any government body or self-regulatory organization required under other applicable laws
- Event has a reasonable likelihood of materially harming any material part of normal operations
- Unauthorized access to privileged accounts
- Deployment of ransomware in material part of the information system

| Decision | Classification | Notes |
|---|---|---|
| Did a cybersecurity event occur? | DETERMINISTIC | Binary at point of detection |
| Does it meet notification threshold? | PARAMETERIZED | "Reasonable likelihood" and "material" are judgment calls |
| 72-hour clock start | DETERMINISTIC | Clock starts at determination that threshold is met |

---

## Annual Board Certification

All covered entities must file an annual certification with DFS by April 15 (or February 15 — confirm current DFS deadline) attesting that the cybersecurity program complies with the regulation.

| Decision | Classification | Notes |
|---|---|---|
| Certification filed on time | DETERMINISTIC | Binary; due date is fixed |
| Supporting documentation complete | PARAMETERIZED | Evidence package completeness |
| Identified deficiencies disclosed | DETERMINISTIC | Known deficiencies must be disclosed |

---

## Open assumption registry

| ID | Domain | Description | Review date |
|---|---|---|---|
| ASSUME-NYDFS500-CISO-001 | CISO / §500.04 | Annual board report cadence is 12-month rolling; must include program status, material risks, events | 2026-11-01 |
| ASSUME-NYDFS500-PENTEST-001 | Penetration Testing / §500.05 | Annual pentest must cover all in-scope systems; Class A bi-annual VA is additive | 2026-11-01 |
| ASSUME-NYDFS500-AUDIT-001 | Audit Trail / §500.06 | Protection from alteration = WORM or crypto chain or separated log-storage admin | 2026-11-01 |
| ASSUME-NYDFS500-MFA-001 | MFA / §500.12 | Second Amendment tightened MFA; CISO exceptions now require annual review + compensating controls | 2026-11-01 |
| ASSUME-NYDFS500-ENC-001 | Encryption / §500.15 | "Not feasible" for at-rest is narrow; performance alone insufficient; key separation required | 2026-11-01 |
| ASSUME-NYDFS500-NOTIF-001 | Notification / §500.17 | 72-hour clock starts at determination; unauthorized privileged access and ransomware are per-se reportable | 2026-11-01 |
| ASSUME-NYDFS500-CLASSA-001 | Class A / §500.02(g) | Consolidated basis; global headcount including contractors; re-evaluated annually | 2026-11-01 |
| ASSUME-NYDFS500-TRAIN-001 | Training / §500.14 | All covered individuals including contractors; 100% completion expected; generic content insufficient | 2026-11-01 |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| MFA | NY DFS §500.12, GLBA §314.4(c)(5), PCI DSS Req 8, NIST 800-53 IA-2 | NY DFS is the most specific (remote + privileged + external web); same technical implementation |
| Penetration testing | NY DFS §500.05, GLBA §314.4(g)(1), PCI DSS Req 11.4, SOC 2 CC7 | Class A: bi-annual vuln scan matches PCI quarterly; annual pentest aligns |
| Encryption | NY DFS §500.15, GLBA §314.4(c)(3), PCI DSS Req 3–4, HIPAA §164.312 | NY DFS requires encryption or documented compensating controls; PCI requires encryption outright |
| 72-hour breach notification | NY DFS §500.17, GDPR Art. 33 (72h), HIPAA (60 days), NY SHIELD Act (expedient/30 days) | Different recipients and thresholds; same incident response infrastructure |
| Audit trail / log retention | NY DFS §500.06 (6 years), PCI DSS Req 10 (12 months), GLBA, SOX (7 years workpapers) | NY DFS 6-year retention is the most demanding standard in this registry for financial sector logs |
| TPSP security policy | NY DFS §500.11, GLBA §314.4(f), SOC 2 CC9.2, ISO 27001 A.5.19 | Single vendor assessment program satisfies all four |
| Annual board/officer reporting | NY DFS §500.04 + certification, GLBA §314.4(k), SOX §302/404 | Different required content; same board presentation can be structured to address all three |
