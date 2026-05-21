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
| Controls parsed (individual files) | 1 (AU, AC, IA, CM, SC, SI — 6 families, ~65 of ~156 Low baseline controls covered) |
| Fully automated (DETERMINISTIC) | HIGH — AU-3 (record fields), SC-8/13/28 (crypto protocols), SI-3 (AV), IA-2 (MFA presence), AC-17/18 (remote/wireless protocols) |
| Partial automation (PARAMETERIZED) | Moderate — AU-11 (retention ODP), AC-7/11 (lockout/session ODPs), IA-5(1) (password ODPs), SI-2 (patch SLA ODPs), CM-6 (deviation tracking) |
| Human-determination required (CONTESTED) | ODP manifest completeness; CM-6 deviation adequacy; IA-2 MFA method exception justification |
| Unresolvable | Minimal |
| Open assumptions | 7 (ASSUME-800053-AU-001–002, AC-001–002, IA-001, CM-001, SI-001) |
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
| *(CP, IR, CA, MA, MP, PE, PS, RA, SA, SR, PL, PM, AT, PT)* | Remaining 14 families | TBD | MEDIUM–CONTESTED | 🔲 Pending |

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
| 7 | CP | Contingency and backup — MEDIUM confidence; DETERMINISTIC for recovery time objectives if ODP-set |
| 8 | IR | Incident response — aligns with CMMC and FedRAMP IR requirements |
| 9 | CA | Continuous monitoring — FedRAMP overlap justifies early parse |
| 10 | SR | CONTESTED family; critical for supply chain programs |
| 11 | remaining | Parse after core baseline established |

---

## Watch list

| Item | Status | Impact |
|---|---|---|
| NIST 800-53B r5 (baselines) | Current | Tailoring guidance; ODP defaults for Low/Moderate/High baselines |
| NIST 800-53A r5 (assessment procedures) | Current | Companion assessment guide; test cases should align to 800-53A assessment objectives |
| NIST 800-161 r1 (SCRM) | Current | Supplements SR family with detailed supply chain risk management practices |
| NIST AI RMF 1.0 (AI-specific risk controls) | Published 2023 | Emerging overlap with AI-enabled system compliance; not yet integrated into 800-53 baselines |
