# NIST SP 800-53 r5 — Security and Privacy Controls for Information Systems

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Full control catalog; Low / Moderate / High impact baselines
**Authority:** National Institute of Standards and Technology (NIST)
**Enforcing context:** FISMA (federal systems); FedRAMP baseline (cloud); CMMC reference; widely adopted for non-federal voluntary use

---

## Summary

| Metric | Count |
|---|---|
| Control families | 20 |
| Total catalog controls + enhancements | ~1,007 |
| Low baseline | ~156 controls |
| Moderate baseline | ~323 controls |
| High baseline | ~421 controls |
| Controls parsed (individual files) | 5 (all 20 families — AU, AC, IA, CM, SC, SI, CP, IR, CA, MA, MP, PE, PS, RA, SA, SR, PL, PM, AT, PT) |
| Fully automated (DETERMINISTIC) | HIGH — AU-3, SC-8/13/28, SI-3, IA-2, AC-17/18, CP-4 (High), IR-4/8, CA-5/7, MA-4, MP-6 (method), PE-3/13/14/15, PS-4/6, RA-5 (scan cadence), PM-10 (ATO validity), AT-2 (new employee), PT-5 (notice at collection) |
| Partial automation (PARAMETERIZED) | Moderate — all ODP-bounded tests (retention, cadence, lockout, session, patch SLAs, training, testing, backup, pentest, review intervals), PL-8 architecture, AT-3 role training, PT-7 sensitive PII protections |
| Human-determination required (CONTESTED) | RA-3 (risk methodology), SA-8/11 (engineering/testing adequacy), SR-2 (SCRM plan content), CP-7 (alternate site equivalency), PL-2 (SSP completeness), PM-9 (risk strategy), PT-2 (legal authority sufficiency) |
| Unresolvable | Minimal |
| Open assumptions | 29 (ASSUME-800053-AU-001–002, AC-001–002, IA-001, CM-001, SI-001, CP-001–004, IR-001–003, CA-001–004, MP-001, PE-001–002, PS-001–002, RA-001–002, SA-001–002, SR-001, PL-001–002, AT-001–003, PT-001) |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Per-family confidence map

| Family | Abbrev | Controls (catalog) | Confidence projection | PARAMETERIZED surface | CONTESTED surface |
|---|---|---|---|---|---|
| Access Control | AC | 25 base | HIGH–MEDIUM | AC-4 info flow enforcement method; AC-14 permitted actions without ID | — |
| Awareness and Training | AT | 6 base | MEDIUM | AT-2 training content adequacy; AT-4 records retention | — |
| Audit and Accountability | AU | 16 base | HIGH | AU-9 log protection method; AU-11 retention period | — |
| Assessment, Authorization, Monitoring | CA | 9 base | MEDIUM | CA-2 assessment scope; CA-7 continuous monitoring frequency | CA-3 information exchange agreements |
| Configuration Management | CM | 14 base | HIGH | CM-4 impact analysis method | — |
| Contingency Planning | CP | 13 base | MEDIUM | CP-2 plan adequacy; CP-7 alternate site equivalency | — |
| Identification and Authentication | IA | 13 base | HIGH | IA-5 password complexity below deterministic threshold | — |
| Incident Response | IR | 10 base | MEDIUM | IR-4 response capability; IR-5 incident tracking scope | — |
| Maintenance | MA | 6 base | MEDIUM | MA-3 maintenance tools authorization | — |
| Media Protection | MP | 8 base | MEDIUM | MP-6 sanitization method adequacy | — |
| Physical and Environmental Protection | PE | 20 base | HIGH–MEDIUM | PE-3 physical access control method | — |
| Planning | PL | 11 base | PARAMETERIZED | PL-2 SSP completeness; PL-8 security architecture adequacy | — |
| Program Management | PM | 32 base | CONTESTED | PM-2 senior information security officer authority; PM-9 risk strategy | PM-14 testing/evaluation strategy |
| Personnel Security | PS | 9 base | MEDIUM | PS-3 personnel screening criteria | — |
| Personally Identifiable Information Processing and Transparency | PT | 8 base | MEDIUM–CONTESTED | PT-2 authority to process PII | PT-3 purpose specification adequacy |
| Risk Assessment | RA | 10 base | CONTESTED | RA-3 risk determination methodology | RA-7 risk response adequacy |
| System and Services Acquisition | SA | 23 base | MEDIUM–CONTESTED | SA-8 security engineering principles | SA-11 developer testing adequacy |
| System and Communications Protection | SC | 51 base | HIGH–MEDIUM | SC-8 transmission confidentiality method; SC-28 protection at rest method | — |
| System and Information Integrity | SI | 23 base | HIGH–MEDIUM | SI-2 flaw remediation timeline (org-defined) | — |
| Supply Chain Risk Management | SR | 12 base | CONTESTED | SR-3 supply chain controls; SR-11 component authenticity | SR-6 supplier assessments |

---

## Baseline scoping

The impact baseline determines which controls are required. Before any test can be enforcing:

1. System must be categorized per FIPS 199 (confidentiality/integrity/availability impact levels)
2. Baseline selected: Low / Moderate / High (or tailored)
3. Organization-defined parameters (ODPs) must be documented — most PARAMETERIZED surfaces arise from ODPs

**Organization-Defined Parameters (ODPs):** 800-53 r5 has hundreds of ODPs (frequency values, time thresholds, scope boundaries). Each ODP must be recorded in the System Security Plan before the test that uses it can assert a deterministic value. The ODP log is treated as the assumption registry for this framework.

---

## Specification file status

| File | Contents | Assumptions | Confidence | Status |
|---|---|---|---|---|
| `core-technical-controls.md` | AU (record content, retention, review), AC (account management, lockout, session lock, remote/wireless), IA (MFA, password policy, hash storage), CM (baseline, hardening, least functionality, change control), SC (TLS, FIPS, at-rest encryption, key management), SI (patch SLAs, AV, monitoring, integrity verification) | ASSUME-800053-AU-001–002, AC-001–002, IA-001, CM-001, SI-001 | HIGH–MEDIUM | ✅ Parsed |
| `contingency-incident-assessment.md` | CP (plan 8 elements, annual review, training, High functional test, alternate storage/processing, daily backups, RTO/RPO), IR (training/test cadence, 6-phase handling, tracking, reporting ≤1h ODP, IRP annual review), CA (triennial assessment, POA&M quarterly + SLAs, monthly ConMon scans, annual pentest) | ASSUME-800053-CP-001–004, IR-001–003, CA-001–004 | HIGH–MEDIUM | ✅ Parsed |
| `maintenance-media-physical-personnel.md` | MA (controlled maintenance records, remote maintenance FIPS+MFA+logging, uncleared personnel escorted), MP (media marking, transport encryption, NIST 800-88 sanitization, removable media restriction), PE (access list annual/semi-annual review, entry/exit logging, monitoring systems, visitor log 2yr, fire/HVAC/water), PS (position risk designation, screening before access, termination ≤8h, transfer ≤5d, access agreements annual, 3rd-party monitoring, sanctions) | ASSUME-800053-MP-001, PE-001–002, PS-001–002 | HIGH–MEDIUM | ✅ Parsed |
| `risk-acquisition-supply-chain.md` | RA (FIPS 199 categorization, risk assessment triennial + 5 required elements, monthly authenticated vuln scans, critical ≤30d SLA), SA (security requirements in contracts, engineering principles, external services inventory annual review, developer SCM, developer security testing), SR (SCRM plan annual review, critical suppliers identified, component authenticity, component disposal) | ASSUME-800053-RA-001–002, SA-001–002, SR-001 | MEDIUM (cadence) / CONTESTED (methodology/adequacy) | ✅ Parsed |
| `planning-program-training-privacy.md` | PL (SSP 8 sections, annual review, security architecture M/H), PM (CISO designated, risk management strategy, valid ATO ≤3yr), AT (annual awareness training all personnel, new employee ≤30 days, 6 required topics, semi-annual role training at High, 3yr record retention), PT (legal authority for PII, purpose documented, privacy notice required content, sensitive PII heightened protections) | ASSUME-800053-PL-001–002, AT-001–003, PT-001 | MEDIUM (AT cadence) / CONTESTED (PL-2/PM-9/PT-2) | ✅ Parsed |

---

## Open assumption registry

| ID | Family/Control | Summary | Review date |
|---|---|---|---|
| ASSUME-800053-AU-001 | AU-11 | Online retention 90d; archive 3yr (Moderate/High) per 800-53B; ODP must be documented in SSP | 2026-05-21 |
| ASSUME-800053-AU-002 | AU-6 | Review frequency ODP: ≤7 days (weekly) for Moderate per 800-53B default | 2026-05-21 |
| ASSUME-800053-AC-001 | AC-7 | Lockout threshold ≤3 attempts; lockout duration ≥30 min; 800-53B Moderate defaults | 2026-05-21 |
| ASSUME-800053-AC-002 | AC-11 | Session lock ≤15-min inactivity; pattern-hiding required; 800-53B Moderate default | 2026-05-21 |
| ASSUME-800053-IA-001 | IA-5(1) | Password length ≥8 (complexity) or ≥15 (no complexity); history 24; max 60d lifetime; no expiry if breach-monitoring active | 2026-05-21 |
| ASSUME-800053-CM-001 | CM-6 | DISA STIGs or CIS Benchmarks satisfy configuration settings requirement; deviations require ISSO-approved exception | 2026-05-21 |
| ASSUME-800053-SI-001 | SI-2 | Patch SLAs: KEV=14d, Critical=30d, High=90d, Medium=180d, Low=365d per 800-53B and CISA BOD 22-01 | 2026-05-21 |
| ASSUME-800053-CP-001 | CP-2 | Contingency plan review ODP: annual (12 months) per 800-53B Moderate default | 2026-05-21 |
| ASSUME-800053-CP-002 | CP-3 | Training frequency ODP: annual at Moderate; semi-annual at High | 2026-05-21 |
| ASSUME-800053-CP-003 | CP-4 | Test frequency ODP: annual; High requires functional or full-interruption test | 2026-05-21 |
| ASSUME-800053-CP-004 | CP-9 | Backup frequency ODPs: daily user-level, weekly system-level; annual restoration test; offsite copies | 2026-05-21 |
| ASSUME-800053-IR-001 | IR-2 | IR training ODP: annual at Moderate; semi-annual at High; role-based for IR personnel | 2026-05-21 |
| ASSUME-800053-IR-002 | IR-3 | IR test ODP: annual at Moderate; semi-annual at High; tabletop or functional acceptable | 2026-05-21 |
| ASSUME-800053-IR-003 | IR-6 | Reporting ODP: within 1 hour of confirmed incident; reporting authority documented in SSP | 2026-05-21 |
| ASSUME-800053-CA-001 | CA-2 | Assessment frequency ODP: triennial (36 months) for Moderate/High; annual recommended for High | 2026-05-21 |
| ASSUME-800053-CA-002 | CA-5 | POA&M SLAs: critical ≤30d, high ≤90d; quarterly update; no overdue without approved exception | 2026-05-21 |
| ASSUME-800053-CA-003 | CA-7 | ConMon ODP: monthly OS/infra scans; ConMon strategy documented and reviewed annually | 2026-05-21 |
| ASSUME-800053-CA-004 | CA-8 | Pentest ODP: annual at High; org-defined at Moderate; network + application + OS layers | 2026-05-21 |
| ASSUME-800053-MP-001 | MP-6 | NIST 800-88 required; disposal logs ≥3 years; degauss alone insufficient for flash/SSD | 2026-05-21 |
| ASSUME-800053-PE-001 | PE-2 | Access list review ODP: annual at Moderate; semi-annual at High; immediate removal on role change | 2026-05-21 |
| ASSUME-800053-PE-002 | PE-8 | Visitor log retention ODP: 2 years per 800-53B Moderate default | 2026-05-21 |
| ASSUME-800053-PS-001 | PS-3 | Screening criteria commensurate with risk; documented by position risk level; adequacy PARAMETERIZED | 2026-05-21 |
| ASSUME-800053-PS-002 | PS-4 | Termination ODP: account disable ≤8 hours; concurrent credential revocation; same-day for privileged | 2026-05-21 |
| ASSUME-800053-RA-001 | RA-3 | Risk assessment frequency ODP: triennial (36 months); must document 5 required elements; methodology adequacy CONTESTED | 2026-05-21 |
| ASSUME-800053-RA-002 | RA-5 | Scan frequency ODP: monthly at Moderate/High; quarterly at Low; authenticated scans required at M/H | 2026-05-21 |
| ASSUME-800053-SA-001 | SA-8 | Security engineering principles ODP: documented selection from NIST 800-160 or equivalent; application adequacy PARAMETERIZED | 2026-05-21 |
| ASSUME-800053-SA-002 | SA-11 | Developer security testing ODP: plan documented; test results reviewed; coverage adequacy CONTESTED | 2026-05-21 |
| ASSUME-800053-SR-001 | SR-3 | Supplier controls ODP: vetting criteria documented in SCRM plan; control sufficiency PARAMETERIZED | 2026-05-21 |
| ASSUME-800053-PL-001 | PL-2 | SSP review ODP: annual; 8 required sections; completeness of implementation descriptions CONTESTED | 2026-05-21 |
| ASSUME-800053-PL-002 | PL-8 | Security architecture ODP: documented and reviewed annually at Moderate/High; alignment adequacy PARAMETERIZED | 2026-05-21 |
| ASSUME-800053-AT-001 | AT-2 | Training frequency ODP: annual; new personnel ≤30 days; 6 required topic areas | 2026-05-21 |
| ASSUME-800053-AT-002 | AT-3 | Role-based training ODP: annual at Moderate; semi-annual at High; 7 designated roles | 2026-05-21 |
| ASSUME-800053-AT-003 | AT-4 | Training record retention ODP: 3 years per 800-53B default | 2026-05-21 |
| ASSUME-800053-PT-001 | PT-7 | Sensitive PII heightened protections: 8 sensitive categories; encryption + access controls + minimization; adequacy PARAMETERIZED | 2026-05-21 |

---

## Contested items pending resolution

*(None recorded yet)*

---

## Cross-standard dependencies

| Shared artifact | Standards | Notes |
|---|---|---|
| System Security Plan | 800-53 PL-2, 800-171 PL, FedRAMP SSP template, FISMA | 800-53 is the superset; 800-171 SSP is a subset; FedRAMP uses its own SSP template built on 800-53 |
| Continuous monitoring strategy | 800-53 CA-7, FedRAMP ConMon, FISMA annual reporting | FedRAMP imposes specific scan frequencies on top of org-defined values |
| Incident response plan | 800-53 IR-8, 800-171 IR, FedRAMP IR | Content requirements largely identical; differ on reporting recipients and timelines |
| Supply chain risk management | 800-53 SR, 800-161 (supply chain risk management supplement), 800-171 SR | 800-53 SR family maps to CMMC SR domain; 800-161 provides detailed SCRM guidance |
| Audit/logging artifacts | 800-53 AU, FedRAMP AU requirements, FISMA | FedRAMP adds SIEM and SOC integration requirements on top of 800-53 AU |
| Privacy controls | 800-53 PT + PL-8, GDPR Art. 25/32, HIPAA §164.312 | 800-53 r5 integrated privacy into the control catalog; PT family maps to GDPR data subject rights and HIPAA technical safeguards |

---

## CI/CD gate configuration

Standard three-tier gate (see NERC CIP registry). Additional constraints:

- **ODP fixture:** Every PARAMETERIZED test requires a corresponding ODP record in the SSP. Tests that reference undefined ODPs block as CONTESTED until the ODP is documented and approved.
- **Baseline fixture:** All tests are tagged with their applicable baseline tier (L/M/H). Tests for controls not in the selected baseline run in informational mode only.
- **Annual review gate:** CA-7 continuous monitoring and CA-2 assessment tests check that the last full assessment date is within the org-defined assessment interval.

---

## Roadmap — individual control file parse priority

Recommended parse order based on DETERMINISTIC density and cross-framework reuse value:

| Priority | Family | Rationale |
|---|---|---|
| ~~1~~ | ~~AU~~ | ✅ Complete — `core-technical-controls.md` |
| ~~2~~ | ~~AC~~ | ✅ Complete — `core-technical-controls.md` |
| ~~3~~ | ~~IA~~ | ✅ Complete — `core-technical-controls.md` |
| ~~4~~ | ~~CM~~ | ✅ Complete — `core-technical-controls.md` |
| ~~5~~ | ~~SC~~ | ✅ Complete — `core-technical-controls.md` |
| ~~6~~ | ~~SI~~ | ✅ Complete — `core-technical-controls.md` |
| ~~7~~ | ~~CP~~ | ✅ Complete — `contingency-incident-assessment.md` |
| ~~8~~ | ~~IR~~ | ✅ Complete — `contingency-incident-assessment.md` |
| ~~9~~ | ~~CA~~ | ✅ Complete — `contingency-incident-assessment.md` |
| ~~10~~ | ~~MA, MP, PE, PS~~ | ✅ Complete — `maintenance-media-physical-personnel.md` |
| ~~11~~ | ~~RA, SA, SR~~ | ✅ Complete — `risk-acquisition-supply-chain.md` |
| ~~12~~ | ~~PL, PM, AT, PT~~ | ✅ Complete — `planning-program-training-privacy.md` |

---

## Watch list

| Item | Status | Impact |
|---|---|---|
| NIST 800-53B r5 (baselines) | Current | Tailoring guidance; ODP defaults for Low/Moderate/High baselines |
| NIST 800-53A r5 (assessment procedures) | Current | Companion assessment guide; test cases should align to 800-53A assessment objectives |
| NIST 800-161 r1 (SCRM) | Current | Supplements SR family with detailed supply chain risk management practices |
| NIST AI RMF 1.0 (AI-specific risk controls) | Published 2023 | Emerging overlap with AI-enabled system compliance; not yet integrated into 800-53 baselines |
