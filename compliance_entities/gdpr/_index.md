# GDPR — EU General Data Protection Regulation (2016/679)

**Registry version:** 2026.05
**Last updated:** 2026-05-21
**Scope:** Articles governing technical and organizational compliance obligations (Articles 5–6, 13–14, 17, 20, 25, 30, 32–40, Chapter V)
**Authority:** EU / EEA national supervisory authorities (lead authority for cross-border processing determined by main establishment)
**Enforcing context:** Any organization processing personal data of EU/EEA data subjects, regardless of organization location; extra-territorial scope per Article 3
**Note:** This registry focuses on technically testable obligations. Legal interpretation of lawful basis (Art. 6) and legitimate interests (Art. 6(1)(f)) is out of scope for automation.

---

## Summary

| Metric | Count |
|---|---|
| Articles (full regulation) | 99 |
| Articles with technically testable obligations | ~20 (focused scope) |
| Articles parsed (individual files) | 3 (core-articles.md — Art. 12, 13/14, 28, 30, 32, 33/34, 35, 37, Chapter V; principles-lawful-basis.md — Art. 5, 6, 9; data-subject-rights-design.md — Art. 17, 20, 21, 25) |
| Fully automated (DETERMINISTIC) | Low — GDPR heavily favors "appropriate," "reasonable," "proportionate" language |
| Partial automation (PARAMETERIZED) | Moderate (breach notification timelines, DPIA triggers, retention schedules, erasure, portability) |
| Human-determination required (CONTESTED) | Dominant — "appropriate measures" is the central obligation of Art. 32 |
| Unresolvable | Low |
| Open assumptions | 17 (ASSUME-GDPR-001–010; ASSUME-GDPR-PRIN-001, CONSENT-001, SPEC-001; ERASURE-001, PORT-001, OBJ-001, PBD-001) |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Ambiguity character of GDPR

GDPR is the most CONTESTED framework in this registry. The drafters intentionally used technology-neutral, risk-based language throughout. Article 32's "appropriate technical and organisational measures" has no bright-line content. Test confidence across GDPR is therefore lower than other frameworks, with Pattern 3 (human-surfacing tests) dominating.

**However**, a subset of GDPR obligations is DETERMINISTIC:
- The 72-hour breach notification deadline (Art. 33)
- The DPO registration requirement when Art. 37 criteria are met (binary once scope is determined)
- ROPA maintenance requirement (Art. 30) — existence is binary; completeness is PARAMETERIZED
- Data subject request response deadline: 1 month (Art. 12)

---

## Per-article confidence map (technically testable obligations)

| Article | Title | Confidence | PARAMETERIZED surface | CONTESTED surface |
|---|---|---|---|---|
| 5 | Principles of processing | CONTESTED | Accuracy maintenance frequency; data minimization scope | "Adequate, relevant and limited" — no bright-line |
| 6 | Lawful basis | PARAMETERIZED | Basis selection documentation | Legitimate interests (6(1)(f)) balancing test |
| 9 | Special category data | PARAMETERIZED | Special category identification completeness | "Necessary" exemption scope |
| 12 | Transparency / response timelines | DETERMINISTIC | — | — |
| 13 | Privacy notice (data collected directly) | PARAMETERIZED | Notice completeness per required elements | Adequacy of layered notice approach |
| 14 | Privacy notice (data not collected directly) | PARAMETERIZED | Notice completeness; delivery timing | — |
| 17 | Right to erasure | PARAMETERIZED | Technical erasure coverage | Competing rights/obligations exception scope |
| 20 | Right to data portability | PARAMETERIZED | Portable format suitability | "Commonly used" machine-readable format definition |
| 21 | Right to object | PARAMETERIZED | Objection processing coverage | Compelling legitimate grounds determination |
| 25 | Data protection by design and default | CONTESTED | — | "Appropriate" technical measures — no specification |
| 28 | Processor agreements (DPA) | PARAMETERIZED | Contract clause completeness (Art. 28(3) mandatory elements) | — |
| 30 | Records of Processing Activities (ROPA) | PARAMETERIZED | ROPA completeness — all required fields per 30(1)/(2) | — |
| 32 | Security of processing | CONTESTED | — | "Appropriate" technical and organisational measures — central GDPR obligation |
| 33 | Breach notification to supervisory authority | DETERMINISTIC (timeline) / PARAMETERIZED (content) | Notification content completeness | — |
| 34 | Communication of breach to data subjects | PARAMETERIZED | "Likely to result in a high risk" determination | — |
| 35 | Data Protection Impact Assessment (DPIA) | PARAMETERIZED | DPIA trigger criteria; adequacy of assessment | Prior consultation trigger |
| 37 | DPO designation | PARAMETERIZED | Art. 37 threshold criteria ("core activities") | "Core activities" interpretation |
| 44–49 | International transfers (Chapter V) | CONTESTED | SCCs implementation completeness | Adequacy decision reliance; Transfer Impact Assessment adequacy |

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Article |
|---|---|---|
| Breach notification to supervisory authority | 72 hours from discovery (when feasible) | Art. 33(1) |
| Data subject request response | 1 month (extendable by 2 months with notice) | Art. 12(3) |
| ROPA existence | Required for organizations with ≥ 250 employees, or processing is non-occasional, special category, or high-risk | Art. 30(5) |
| Privacy notice timing (direct collection) | At time of collection | Art. 13 |
| Privacy notice timing (indirect collection) | Within 1 month or at first communication | Art. 14(3) |
| Breach documentation | All breaches must be documented (not just reported) | Art. 33(5) |

---

## Article 32 — the core compliance obligation

Article 32 requires "appropriate technical and organisational measures to ensure a level of security appropriate to the risk." It non-exhaustively lists:
- (a) Pseudonymization and encryption
- (b) Ongoing confidentiality, integrity, availability, and resilience
- (c) Ability to restore data after incident
- (d) Regular testing and evaluation

None of these have defined thresholds. The Recitals and EDPB guidance provide examples but not bright-lines.

**RDF treatment:**
- Art. 32 generates no Pattern 1 tests directly
- Implementation choices (e.g., encryption algorithm, backup frequency, pentest cadence) are documented as assumptions and tested via Pattern 2
- The "appropriate" determination itself is a Pattern 3 test requiring DPO/Legal sign-off annually or upon significant processing change

---

## Chapter V — International transfers

Post-Schrems II, the primary transfer mechanisms are:
1. Adequacy decision (Art. 45) — DETERMINISTIC: is the destination country on the EU adequacy list?
2. Standard Contractual Clauses (SCCs, Art. 46(2)(c)) — PARAMETERIZED: SCCs exist and use current 2021 version
3. Binding Corporate Rules (BCRs, Art. 47) — PARAMETERIZED: BCR approval status
4. Transfer Impact Assessment (TIA) — CONTESTED: risk assessment methodology acceptability

The current EU-U.S. Data Privacy Framework (DPF, 2023) is an adequacy decision for DPF-certified U.S. organizations. DPF certification status is DETERMINISTIC (binary lookup).

---

## ROPA — mandatory record structure

The Records of Processing Activities (Art. 30) must contain, for controllers:
- Controller name and contact
- DPO contact (if applicable)
- Processing purposes
- Data subject categories
- Data categories
- Recipient categories
- Third-country transfers
- Retention schedule
- Technical and organisational measure descriptions

Completeness is PARAMETERIZED (each record must have all fields). ROPA existence for qualifying organizations is DETERMINISTIC.

---

## Open assumption registry

| ID | Article | Summary | Review date |
|---|---|---|---|
| ASSUME-GDPR-001 | Art. 12 | DSR response: ≤30 days from receipt; extension notice within 30 days; max 90 days total; log with receipt date, request type, response date, outcome; identity verification proportionate | 2026-05-20 |
| ASSUME-GDPR-002 | Art. 13/14 | Privacy notice: 12 required elements present; plain language; provided at time of collection (Art. 13) or within 1 month for indirect collection (Art. 14); reviewed on processing change | 2026-05-20 |
| ASSUME-GDPR-003 | Art. 28 | DPA: 9 Art. 28(3) mandatory elements present; 2021 EU SCCs where applicable; sub-processor list current; reviewed on material processing change | 2026-05-20 |
| ASSUME-GDPR-004 | Art. 30 | ROPA: all processing activities documented; required fields per 30(1) present per entry; retention periods specific; reviewed annually or on new processing; machine-readable format | 2026-05-20 |
| ASSUME-GDPR-005 | Art. 33 | Breach notification: within 72 hours of controller becoming aware; initial notification with incomplete info acceptable + supplement without undue delay; 5 content elements required; all breaches documented in breach log | 2026-05-20 |
| ASSUME-GDPR-006 | Art. 34 | Art. 34 high-risk determination: EDPB Guidelines 9/2022 criteria applied — nature, scale, sensitivity, re-identification ease, likely consequences; decision documented; DPO consulted on borderline cases | 2026-05-20 |
| ASSUME-GDPR-007 | Art. 35 | DPIA: required for any Art. 35(3) trigger or national mandatory list; includes systematic description, necessity/proportionality, risk assessment, measures; DPO consulted; prior consultation (Art. 36) if residual risk remains high | 2026-05-20 |
| ASSUME-GDPR-008 | Art. 37 | DPO designation: "large scale" = significant portion of EU population / continuous-systematic; "core activities" = primary purpose, not ancillary HR; DPO has expert knowledge; internal or external; no conflict of interest roles | 2026-05-20 |
| ASSUME-GDPR-009 | Art. 32 | Art. 32 technical measures for standard personal data: encryption at rest (AES-128+); TLS 1.2+; access controls; MFA for large-scale processing; backup with restore capability; quarterly vulnerability scanning; pseudonymization where feasible | 2026-05-20 |
| ASSUME-GDPR-010 | Chapter V | International transfers: all transfers in ROPA; adequacy decision or 2021 SCCs with correct module (M1/M2/M3/M4); TIA for high-risk jurisdictions (bulk surveillance risk); DPF: U.S. recipient certification verified | 2026-05-20 |
| ASSUME-GDPR-PRIN-001 | Art. 5 | Accuracy maintenance: accuracy review cadence is org-defined based on data category — minimum annual for high-stakes decisions; near-real-time for transactional data; accuracy metric documented in ROPA per processing activity | 2026-11-01 |
| ASSUME-GDPR-CONSENT-001 | Art. 6 | Consent records required fields: subject_identifier, timestamp, mechanism, notice_version_shown, purposes_consented_to; consent withdrawal processed within 30 days (Art. 12(3)); re-collection required if consent records cannot be verified | 2026-11-01 |
| ASSUME-GDPR-SPEC-001 | Art. 9 | Special category processing: Art. 9(2) condition documented per activity in ROPA alongside Art. 6 lawful basis; biometric data only Art. 9 when used for identification; explicit consent (Art. 9(2)(a)) requires unambiguous affirmative act — no inferred or pre-ticked consent | 2026-11-01 |
| ASSUME-GDPR-ERASURE-001 | Art. 17 | Technical erasure scope covers primary databases, application caches, search indexes, backup media (marked for purge at next backup cycle); third-party notification sent within 30-day response window for publicly disclosed data; audit logs pseudonymized rather than erased | 2026-11-01 |
| ASSUME-GDPR-PORT-001 | Art. 20 | Portable format: JSON/CSV/XML/Parquet accepted; direct controller-to-controller transfer feasible if receiving controller provides documented API or standard import capability; feasibility documented per request with DPO review on disputes | 2026-11-01 |
| ASSUME-GDPR-OBJ-001 | Art. 21 | Direct marketing objection is absolute — no compelling grounds override; LIA objection: compelling grounds assessment documented, DPO/Legal reviewed, communicated within 30 days; research/statistics override requires IRB review + DPO sign-off | 2026-11-01 |
| ASSUME-GDPR-PBD-001 | Art. 25 | Privacy by design: systems default to minimum fields, minimum retention, restricted access; Privacy Design Review (PDR) required before deployment of new or materially changed systems; annual DPO attestation of programme adequacy against 'state of the art' standard | 2026-11-01 |

---

## Contested items pending resolution

| Item | Article | Reason | Resolution path |
|---|---|---|---|
| "Appropriate" security measures | Art. 32 | No EU-wide bright-line; EDPB guidelines provide examples but not thresholds; proportionality to risk is always a judgment call | DPO annual attestation; EDPB guidance review; Pattern 3 gate in place |
| Art. 34 high-risk determination | Art. 34 | "Likely to result in a high risk" — higher threshold than Art. 33 reporting threshold; requires case-by-case judgment | DPO review; EDPB Guidelines 9/2022 applied; documented rationale required |
| Legitimate interests balancing | Art. 6(1)(f) | Legitimate interests assessment (LIA) is a multi-factor test; no objective outcome | DPO/Legal conduct LIA; document outcomes; Pattern 3 gate |
| Art. 49 derogation adequacy | Art. 49 | Derogation for "occasional transfers" lacking SCCs/adequacy — scope of "occasional" undefined; pending EDPB guidance | Pattern 3 gate in place; legal counsel for each invocation |
| Transfer Impact Assessment (TIA) adequacy | Art. 46 | Risk assessment methodology and depth of TIA review is assessor-evaluated; supervisory authority enforcement varies | DPO/Legal conduct TIA; document methodology; Pattern 3 gate |
| "Large scale" and "core activities" | Art. 37 | No numeric thresholds for DPO designation triggers; WP29/EDPB provide guidance but not bright-lines | DPO consultation; document determination rationale per Art. 37 |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Data processing agreements | GDPR Art. 28, HIPAA §164.314 BAA, ISO 27001 A.5.19 | A combined DPA/BAA template satisfies both GDPR and HIPAA for U.S.-EU processing chains |
| Encryption at rest/in transit | GDPR Art. 32 (recital 83), HIPAA §164.312 (addressable), PCI DSS Req 3–4 (required) | PCI-grade encryption exceeds both GDPR and HIPAA requirements |
| Data breach response | GDPR Art. 33 (72h), HIPAA §164.408 (60 days), NIST 800-53 IR-6 | 72-hour GDPR deadline is the tightest; design IRP to meet GDPR and others are satisfied |
| Data inventory / ROPA | GDPR Art. 30, HIPAA addressable §164.308, ISO 27001 A.5.9 | A single unified data inventory can satisfy all three if it contains the required fields for each |
| Vendor assessments | GDPR Art. 28, ISO 27001 A.5.19–5.22, SOC 2 CC9.2 | A single vendor due diligence questionnaire template covers all three |
| Retention schedules | GDPR Art. 5(1)(e) (storage limitation), HIPAA §164.316(b)(2) (6-year), PCI DSS Req 10 (12-month log) | Retention decisions must satisfy the most restrictive applicable requirement per data category |

---

## CI/CD gate configuration

Standard three-tier gate (see NERC CIP registry). GDPR-specific constraints:

- **Processing scope fixture:** All tests gated by `processes_eu_subject_data()` — must be attested before tests are enforcing. Art. 3 extra-territorial scope means many organizations qualify unexpectedly.
- **Lawful basis tracker:** Each processing activity in the ROPA must have a documented lawful basis. Absence triggers Pattern 2 failure.
- **Breach response clock:** 72-hour countdown test starts on `incident_discovered_at` timestamp; Pattern 1 failure if notification not dispatched within threshold.
- **DPF/adequacy check (Chapter V):** For U.S. transfers, DPF certification status is queried via DPF list; absence triggers Pattern 2 requiring SCC or TIA documentation.
- **Art. 32 annual review:** Pattern 3 gate verifies DPO/Legal has reviewed and attested security measures as "appropriate" within the last 12 months.

---

## Specification file status

| File | Contents | Assumptions | Confidence | Status |
|---|---|---|---|---|
| `core-articles.md` | Art. 12 (DSR timelines), 13/14 (privacy notices), 28 (DPA), 30 (ROPA), 32 (security), 33/34 (breach notification), 35 (DPIA), 37 (DPO), Chapter V (international transfers) | ASSUME-GDPR-001–010 | HIGH (Art. 12, 33) / MEDIUM (Art. 28, 30, 37) / LOW (Art. 32, Chapter V) | ✅ Parsed |
| `principles-lawful-basis.md` | Art. 5 (principles — storage limitation, accuracy, purpose limitation, accountability), Art. 6 (lawful basis — consent records/withdrawal, LIA), Art. 9 (special category data — identification, Art. 9(2) conditions, explicit consent, enhanced security) | ASSUME-GDPR-PRIN-001, CONSENT-001, SPEC-001 | HIGH (Art. 6 consent/withdrawal) / MEDIUM (Art. 9) / LOW (Art. 5 — CONTESTED) | ✅ Parsed |
| `data-subject-rights-design.md` | Art. 17 (right to erasure — response deadline, outcome documentation, third-party propagation, technical procedure), Art. 20 (portability — deadline, machine-readable format, direct transfer feasibility), Art. 21 (right to object — direct marketing absolute cessation, LIA objection assessment, research override), Art. 25 (privacy by design/default — by-default configuration, SDLC PDR, annual DPO attestation, accessibility default) | ASSUME-GDPR-ERASURE-001, PORT-001, OBJ-001, PBD-001 | HIGH (Art. 21 direct marketing, Art. 17 deadline) / MEDIUM (Art. 20, Art. 17 erasure scope) / LOW (Art. 25 — CONTESTED) | ✅ Parsed |

---

## Parse status: Complete — all focused-scope articles parsed across 3 spec files (Art. 5, 6, 9, 12, 13/14, 17, 20, 21, 25, 28, 30, 32, 33/34, 35, 37, Chapter V); 17 assumptions recorded
