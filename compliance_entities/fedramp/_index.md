# FedRAMP — Federal Risk and Authorization Management Program

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** FedRAMP Rev 5 baselines (Low / Moderate / High); continuous monitoring requirements
**Authority:** FedRAMP PMO / GSA; NIST SP 800-53 r5 (underlying control catalog)
**Enforcing context:** Cloud Service Providers (CSPs) seeking authorization to operate with federal agencies; required for all cloud services used by federal agencies per FedRAMP Authorization Act (2022)
**Note:** FedRAMP controls are a tailored subset of NIST 800-53 r5 with FedRAMP-specific parameter values and additional requirements. The 800-53 registry entry is the parent; this registry documents FedRAMP-specific overlays only.

---

## Summary

| Metric | Count |
|---|---|
| Impact baselines | 3 (Low, Moderate, High) |
| Low baseline controls | ~125 |
| Moderate baseline controls | ~325 |
| High baseline controls | ~421 |
| FedRAMP-specific additional requirements | ~40+ (overlays on top of 800-53 r5) |
| Controls parsed (individual files) | 2 (conmon-and-overlays.md + account-contingency-media.md — RA-5, CA-5/7, CM-3, IR-6, SC-13, IA-2(12), PE/CONUS, CA-2, CA-8, SR, AC-2/6/12/17, CP-2/3/4/6/9/10, MP-6/7, PS-3/4/5/6) |
| Open assumptions | 19 (ASSUME-FEDRAMP-001–010 + AC-001–002, CP-001–004, MP-001, PS-001–002) |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Authorization pathway — pre-condition structure

| Pathway | Description | Who uses it |
|---|---|---|
| **Agency ATO** | Individual agency grants Authority to Operate for their use | CSPs serving one or a few agencies |
| **JAB P-ATO** | Joint Authorization Board grants Provisional ATO for government-wide reuse | Large CSPs serving multiple agencies; most rigorous |
| **FedRAMP Tailored (LI-SaaS)** | Simplified path for low-impact SaaS | Low-impact SaaS with no sensitive data |
| **Program ATO** | Agency-specific authorization not reused across government | Older model; deprecated in favor of reuse |

Authorization type determines assessment rigor and 3PAO involvement:
- JAB P-ATO: 3PAO required; FedRAMP PMO review
- Agency ATO: 3PAO recommended (required for Moderate+); agency reviews
- LI-SaaS: Self-attestation with agency review

---

## FedRAMP-specific overlays (delta from NIST 800-53 r5)

These are requirements that FedRAMP adds or tightens beyond the 800-53 baseline. Each generates test cases independent of the 800-53 parent.

| Overlay | 800-53 Parent | FedRAMP requirement | Confidence |
|---|---|---|---|
| Continuous monitoring scan frequency | RA-5 | Monthly OS/infrastructure scans; annual application scans | DETERMINISTIC |
| Monthly vulnerability report | RA-5 | CSP must submit monthly ConMon report to agency/JAB | DETERMINISTIC |
| POA&M management | CA-5 | All open findings tracked in FedRAMP POA&M template; monthly updates | DETERMINISTIC |
| Significant change notification | CM-3 | Notify agency/JAB within 30 days of significant change | DETERMINISTIC |
| FIPS 140-2/3 cryptography | SC-13 | Validated cryptographic modules required (FIPS 140-2 minimum) | DETERMINISTIC |
| Federal personal identity verification (PIV) | IA-2(12) | PIV credential support required for Moderate+ | DETERMINISTIC |
| 3PAO annual assessment | CA-2 | Annual assessment by accredited 3PAO | DETERMINISTIC |
| Incident reporting (US-CERT) | IR-6 | Report to US-CERT within 1 hour of discovering incident | DETERMINISTIC |
| Continuous monitoring plan | CA-7 | Formal ConMon plan required; reviewed annually | PARAMETERIZED |
| Data center location | Various | Data must reside in U.S. (CONUS) for Moderate+; exceptions require agency approval | DETERMINISTIC |
| Penetration testing | CA-8 | Annual penetration test by 3PAO; includes network, application, and OS layers | DETERMINISTIC |
| Supply chain (SCRM) | SR-1 through SR-11 | SCRM plan required; High baseline adds enhanced supplier screening | PARAMETERIZED |
| Insider threat program | PS-8 (overlay) | Formal insider threat program required for High | PARAMETERIZED |

---

## Per-baseline confidence map

### Moderate baseline (most common)

| Control family | Controls (approx.) | Confidence projection | FedRAMP overlay notes |
|---|---|---|---|
| AC | 25 | HIGH–MEDIUM | FedRAMP tightens AC-2 (account management) — audit within 30 days of employee departure |
| AU | 12 | HIGH | Monthly log submission to agency; FedRAMP log template |
| CA | 9 | MEDIUM–HIGH | 3PAO annual assessment (DETERMINISTIC); ConMon plan (PARAMETERIZED) |
| CM | 11 | HIGH | Monthly CM reports; FIPS-validated tools |
| CP | 10 | MEDIUM | RTO/RPO documented; annual DR test |
| IA | 12 | HIGH | PIV support required; FIPS 140-2/3 authenticators |
| IR | 8 | HIGH | 1-hour US-CERT reporting (DETERMINISTIC) |
| MA | 6 | MEDIUM | Remote maintenance via approved channels |
| MP | 7 | MEDIUM | FIPS-validated sanitization |
| PE | 11 | HIGH | U.S.-only data center (DETERMINISTIC for Moderate) |
| PL | 5 | PARAMETERIZED | SSP completeness per FedRAMP template |
| PS | 8 | MEDIUM | Background investigations commensurate with impact level |
| RA | 7 | HIGH | Monthly vulnerability scans (DETERMINISTIC) |
| SA | 18 | MEDIUM | Supply chain overlay; developer security testing |
| SC | 44 | HIGH–MEDIUM | FIPS 140-2/3 required; TLS 1.2 minimum |
| SI | 17 | HIGH | Monthly patch report; AV daily updates |
| SR | 12 | CONTESTED | SCRM plan adequacy |

---

## Continuous monitoring (ConMon) requirements — primary DETERMINISTIC surface

ConMon is where FedRAMP has the most automatable obligations:

| Activity | Frequency | Threshold | Confidence |
|---|---|---|---|
| OS/infrastructure vulnerability scan | Monthly | All in-scope systems | DETERMINISTIC |
| Web application scan | Annual (at minimum) | All web apps in boundary | DETERMINISTIC |
| Database scan | Annual (at minimum) | All databases in boundary | DETERMINISTIC |
| POA&M update | Monthly | All open findings | DETERMINISTIC |
| Significant change notification | Within 30 days | Any significant system change | DETERMINISTIC |
| Incident report to US-CERT | Within 1 hour | Confirmed incidents | DETERMINISTIC |
| Annual 3PAO assessment | Annual | Full control set | DETERMINISTIC |
| Annual penetration test | Annual | Network + application layers | DETERMINISTIC |
| CSP monthly ConMon report | Monthly | Submitted to agency/JAB | DETERMINISTIC |

---

## FedRAMP authorization status — DETERMINISTIC test

CSP authorization status is publicly verifiable via the FedRAMP Marketplace (marketplace.fedramp.gov):
- `Authorized` — current ATO/P-ATO in effect
- `In Process` — active authorization in progress
- `Ready` — FedRAMP Ready designation

For agency procurement, checking FedRAMP Marketplace status before contract award is a DETERMINISTIC gate.

---

## Open assumption registry

| ID | Control | Summary | Review date |
|---|---|---|---|
| ASSUME-FEDRAMP-001 | RA-5 overlay | OS/infra scans: monthly (≤30 days); authenticated; web app/DB: annually; all boundary systems in scope | 2026-05-20 |
| ASSUME-FEDRAMP-002 | CA-7 | ConMon plan: monitoring activities and frequencies; roles; reporting format; POA&M trigger; reviewed annually | 2026-05-20 |
| ASSUME-FEDRAMP-003 | CA-5 overlay | POA&M: FedRAMP template; all findings tracked; monthly submission; critical (CVSS≥9.0) ≤30-day remediation; no overdue items without deviation | 2026-05-20 |
| ASSUME-FEDRAMP-004 | CM-3 overlay | Significant change: notify agency AO ≤30 days; classify at intake; security impact analysis; control re-assessment triggered | 2026-05-20 |
| ASSUME-FEDRAMP-005 | IR-6 overlay | US-CERT: ≤1 hour from confirmed incident; FedRAMP PMO and agency AO also notified; all confirmed incident types; preliminary reports acceptable | 2026-05-20 |
| ASSUME-FEDRAMP-006 | SC-13 overlay | FIPS: all crypto modules CMVP-active; prohibited protocols (SSL/TLS≤1.1) and ciphers (RC4, DES, MD5-MAC) disabled; TLS 1.2 minimum | 2026-05-20 |
| ASSUME-FEDRAMP-007 | IA-2(12) | PIV: Moderate/High must accept PIV; OCSP/CRL revocation checked; fallback auth documented and controlled | 2026-05-20 |
| ASSUME-FEDRAMP-008 | PE CONUS overlay | CONUS: Moderate/High all storage and backup regions within CONUS; CDN must geo-restrict; exceptions require agency written approval | 2026-05-20 |
| ASSUME-FEDRAMP-009 | CA-2 + CA-8 | 3PAO: FedRAMP-recognized; SAR ≤365 days; pentest ≤365 days; scope: network + application + OS; prior findings re-tested | 2026-05-20 |
| ASSUME-FEDRAMP-010 | SR SCRM overlay | SCRM: critical suppliers identified; screening criteria documented; records current; reviewed annually; High: NIST 800-161 enhanced screening | 2026-05-20 |
| ASSUME-FEDRAMP-AC-001 | AC-2 overlay | Privileged account review: semi-annual at Moderate/High; departed-user access audit within 30 days | 2026-05-21 |
| ASSUME-FEDRAMP-AC-002 | AC-12 overlay | Session termination (not just lock) ≤30 min for network sessions at Moderate/High | 2026-05-21 |
| ASSUME-FEDRAMP-CP-001 | CP-3 | Training frequency: annual at Moderate; semi-annual (6 months) at High; role-based for continuity personnel | 2026-05-21 |
| ASSUME-FEDRAMP-CP-002 | CP-4 | Testing frequency: annual; High requires functional test (not tabletop-only); must demonstrate RTO | 2026-05-21 |
| ASSUME-FEDRAMP-CP-003 | CP-6 | Alternate storage geographic separation ≥25 miles; both primary and alternate must be CONUS | 2026-05-21 |
| ASSUME-FEDRAMP-CP-004 | CP-9 | Daily user data backups; weekly system-level; offsite; encrypted with FIPS-validated crypto; annual restoration test | 2026-05-21 |
| ASSUME-FEDRAMP-MP-001 | MP-6 overlay | NIST 800-88 required; FIPS-validated tools at Moderate/High; disposal records ≥3 years; physical destruction for High when purge infeasible | 2026-05-21 |
| ASSUME-FEDRAMP-PS-001 | PS-3 overlay | Investigation levels: Low=NACI; Moderate=MBI/NACI; High=BI; reinvestigation every 5 years; complete before CUI access | 2026-05-21 |
| ASSUME-FEDRAMP-PS-002 | PS-5 overlay | Access re-evaluated within 5 business days of transfer; excess prior-role access revoked | 2026-05-21 |

---

## Contested items pending resolution

| Item | Control | Reason | Resolution path |
|---|---|---|---|
| ConMon plan adequacy | CA-7 | "Adequate" monitoring activities and frequencies are assessor-evaluated; plan content sufficiency is judgment-based | 3PAO review; ISSO/ISSM attestation |
| Significant change classification | CM-3 | Boundary cases (e.g., auth policy changes, minor architecture updates) may or may not be "significant" — no objective bright-line | ISSO classification rationale documented; agency AO concurrence for borderline cases |
| Supplier screening adequacy | SR SCRM | Vendor risk assessment depth and ICT supply chain control sufficiency are assessor-evaluated; High baseline follows NIST 800-161 which provides criteria but not absolute thresholds | 3PAO review; SCRM plan against 800-161 criteria |
| CONUS CDN edge caching | PE overlay | Whether CDN edge caching of federal data outside CONUS constitutes a violation when the CDN provider is FedRAMP authorized is agency-specific | Agency AO determination; legal review; typically resolve via CDN boundary exclusion or geo-restriction |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| NIST 800-53 controls | FedRAMP, FISMA, NIST 800-53 registry | FedRAMP IS NIST 800-53 + overlays; the 800-53 registry is the parent. FedRAMP test fixtures extend 800-53 fixtures with tighter parameter values |
| System Security Plan (SSP) | FedRAMP (FedRAMP SSP template), NIST 800-53 PL-2, NIST 800-171 | FedRAMP requires a specific SSP template that is more detailed than the 800-171 SSP; cannot be shared directly but control content can be extracted |
| Vulnerability scan reports | FedRAMP RA ConMon, PCI DSS Req 11, SOC 2 CC7.1 | FedRAMP monthly frequency is the most demanding; design to FedRAMP ConMon to satisfy all |
| Incident response | FedRAMP IR (1-hour US-CERT report), HIPAA (60-day), GDPR (72-hour) | FedRAMP's 1-hour reporting is for US-CERT; GDPR/HIPAA report to different authorities. These run in parallel, not as alternatives |
| FIPS 140-2/3 cryptography | FedRAMP SC-13, CMMC Level 2+ (FIPS required), NIST 800-53 SC-13 | FIPS validation is required for all three; one validated module library satisfies all |
| POA&M management | FedRAMP CA-5, CMMC (POA&M allowed for up to 20% of practices), NIST 800-53 CA-5 | Different POA&M templates; separate tracking required. FedRAMP POA&M has the strictest format and monthly submission requirement |

---

## CI/CD gate configuration

Standard three-tier gate (see NERC CIP registry). FedRAMP-specific constraints:

- **Authorization status:** `fedramp_authorization_status` fixture checks Marketplace; tests are enforcing only for Authorized systems.
- **ConMon deadline tracking:** Monthly scan and report deadlines tracked as time-bounded tests; Pattern 2 failure when deadline is within 5 business days.
- **FIPS module validation:** SC-13 test queries NIST CMVP database for module validation status; expired or revoked validation triggers Pattern 2.
- **Significant change tracker:** All system changes classified at intake; significant changes trigger 30-day notification countdown.
- **3PAO assessment validity:** Annual assessment date tracked; > 12 months since last assessment triggers Pattern 3 block.

---

## Specification file status

| File | Contents | Assumptions | Confidence | Status |
|---|---|---|---|---|
| `conmon-and-overlays.md` | RA-5 (ConMon scans), CA-7 (ConMon plan), CA-5 (POA&M), CM-3 (sig. change), IR-6 (US-CERT 1h), SC-13 (FIPS), IA-2(12) (PIV), PE/CONUS, CA-2+CA-8 (3PAO+pentest), SR (SCRM) | ASSUME-FEDRAMP-001–010 | HIGH (ConMon, IR-6, FIPS, PIV, CONUS, 3PAO/pentest) / MEDIUM (ConMon plan) / CONTESTED (SCRM) | ✅ Parsed |
| `account-contingency-media.md` | AC (account review cadences, FIPS remote access, privileged account separation, session termination), CP (contingency plan 7 elements, training, testing, alternate storage 25mi separation, daily backups, RTO/RPO), MP (NIST 800-88 sanitization, FIPS tools, 3yr disposal records), PS (investigation levels per baseline, 4h account disable, 5-day transfer review, annual access agreements) | ASSUME-FEDRAMP-AC-001–002, CP-001–004, MP-001, PS-001–002 | HIGH (PS-4, CP-4 test, MP-6 method) / MEDIUM (CP training, PS investigation level) | ✅ Parsed |
| *(Remaining Moderate overlay families)* | AU, CM, IA, MA, PL, SA — FedRAMP parameter deltas from 800-53 r5 | TBD | MEDIUM | 🔲 Pending |
| *(High-only enhancements)* | IA-3, PE enhancements, PS insider threat, SR 800-161 enhanced SCRM | TBD | MEDIUM | 🔲 Pending |

---

## Remaining parse priority

| Priority | Area | Notes |
|---|---|---|
| ~~1~~ | ~~AC family~~ | ✅ Complete — `account-contingency-media.md` |
| ~~2~~ | ~~CP family~~ | ✅ Complete — `account-contingency-media.md` |
| ~~3~~ | ~~MP-6 (FIPS sanitization)~~ | ✅ Complete — `account-contingency-media.md` |
| ~~4~~ | ~~PS~~ | ✅ Complete — `account-contingency-media.md` |
| 5 | AU/CM/IA/SC/SI FedRAMP parameter deltas | Monthly log submission, FIPS-validated tool overlay, PIV details |
| 6 | SA (Moderate) | Developer security testing; supply chain overlay |
| 7 | High-only enhancements | Insider threat program; enhanced SCRM (SR); additional IA controls |
