# UK GDPR + Data Protection Act 2018

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Processing of personal data of data subjects in the UK; applies to controllers and processors established in the UK, and to non-UK entities that offer goods/services to UK data subjects or monitor their behavior
**Authority:** Information Commissioner's Office (ICO); Data Protection Act 2018 (DPA 2018) supplements and modifies UK GDPR post-Brexit; UK GDPR = retained EU GDPR as modified by DPA 2018
**Enforcing context:** Any organization processing UK personal data; DPA 2018 adapts UK GDPR for law enforcement (Part 3) and intelligence services (Part 4)
**Relationship to EU GDPR:** UK GDPR is substantially identical to EU GDPR as of 2018 snapshot; UK has since diverged modestly (adequacy decisions, reform proposals); for test purposes, treat as EU GDPR with UK-specific deltas
**Current status:** EU adequacy decision for UK in force; UK GDPR reform (DPDI Bill) ongoing as of 2026

---

## Summary

| Metric | Count |
|---|---|
| Core articles | ~99 (same structure as EU GDPR) |
| UK-specific departures from EU GDPR | ~15 (DPA 2018 modifications) |
| ICO maximum fine (standard) | £17.5M or 4% global annual turnover (higher of) |
| ICO maximum fine (lower tier) | £8.75M or 2% global annual turnover |
| Sections parsed (individual files) | 1 (UK-specific deltas; EU GDPR base tests apply in full) |
| Fully automated (DETERMINISTIC) | Same as EU GDPR — 72h breach, DSR deadlines, consent elements |
| Partial automation (PARAMETERIZED) | Same as EU GDPR dominant |
| Human-determination required (CONTESTED) | Same as EU GDPR — legitimate interests, adequacy |
| Open assumptions | 4 |

---

## UK vs EU GDPR — key deltas

| Dimension | EU GDPR | UK GDPR | Confidence |
|---|---|---|---|
| Supervisory authority | Lead SA in establishment country | ICO only (UK-centric) | DETERMINISTIC |
| Adequacy decisions | EC-issued | UK Secretary of State-issued | DETERMINISTIC |
| One-stop-shop | Yes (EU-wide) | No UK equivalent — ICO is sole authority | DETERMINISTIC |
| Age of consent for information society services | 16 (or lower by member state, min 13) | 13 (DPA 2018 §9) | DETERMINISTIC |
| Fee regulations | Not in GDPR text | DPA 2018 §12 — ICO can charge nominal fee for complex DSRs | PARAMETERIZED |
| Law enforcement processing | LED Directive | DPA 2018 Part 3 | Out of GDPR scope |
| Research/statistics exemptions | Art. 89 + member state law | Art. 89 + DPA 2018 Sch. 2 | PARAMETERIZED |

---

## Core obligations (mirrors EU GDPR — confidence map abbreviated)

| Obligation | Article | Deadline | Confidence |
|---|---|---|---|
| Lawful basis for processing | Art. 6 UK GDPR | Before processing | PARAMETERIZED |
| Valid consent elements | Art. 7 | Before processing | DETERMINISTIC |
| Privacy notice to data subjects | Art. 13/14 | At time of collection | DETERMINISTIC — required elements |
| Subject Access Request (SAR) | Art. 15 | 1 month (extendable 2 months) | DETERMINISTIC |
| Right to erasure | Art. 17 | Without undue delay | PARAMETERIZED |
| Data breach notification to ICO | Art. 33 | 72 hours from becoming aware | DETERMINISTIC |
| Data breach notification to individuals | Art. 34 | Without undue delay | PARAMETERIZED (risk threshold) |
| DPIA for high-risk processing | Art. 35 | Before processing | DETERMINISTIC existence |
| DPO appointment (applicable organizations) | Art. 37 | Before processing begins | DETERMINISTIC |
| Data Processing Agreement | Art. 28 | Before processor engagement | DETERMINISTIC |
| International transfers | Art. 44–49 | Before transfer | PARAMETERIZED (mechanism) |
| Records of processing activities | Art. 30 | Ongoing | DETERMINISTIC for large/complex orgs |

---

## UK-specific: ICO registration

Most UK data controllers must register with the ICO and pay a registration fee (Tier 1: £40/year for small orgs; Tier 2: £60; Tier 3: £2,900 for large orgs). Failure to register = criminal offence.

| Requirement | Confidence |
|---|---|
| ICO registration current | DETERMINISTIC — binary; fee paid; entry on public register |
| Correct tier classification | PARAMETERIZED — based on turnover and headcount |

---

## UK international transfers — post-Brexit mechanisms

| Transfer mechanism | Confidence | Notes |
|---|---|---|
| UK adequacy regulations (for specific countries) | DETERMINISTIC — list maintained by ICO | EU adequacy ≠ UK adequacy; separate lists |
| UK International Data Transfer Agreement (IDTA) | DETERMINISTIC — correct template | Replaced EU SCCs for UK transfers (2022) |
| UK Addendum to EU SCCs | DETERMINISTIC — addendum attached to EU SCCs | For UK companies using EU SCCs with non-UK transfers |
| Binding Corporate Rules (UK BCRs) | PARAMETERIZED — ICO approval required | Separate UK BCR process from EU |

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Article |
|---|---|---|
| Breach notification to ICO | 72 hours | Art. 33 UK GDPR |
| SAR response | 1 month (+ 2-month extension with notice) | Art. 15 |
| Age of consent (information society services) | 13 years | DPA 2018 §9 |
| ICO registration fee | £40–£2,900/year | DPA 2018 / ICO Fee Regulations |
| UK IDTA / UK Addendum required | Before transfer to non-adequate country | Art. 46 UK GDPR |

---

## Spec file status

| File | Coverage | Status |
|---|---|---|
| [`uk-specific-deltas.md`](./uk-specific-deltas.md) | ICO registration (existence, tier, renewal), age of consent = 13 (DPA 2018 §9), 72-hour breach to ICO, dual-regulator breach notification (UK + EU), UK IDTA / UK Addendum transfer mechanisms, ROPA UK/EU separation | ✅ |

## Open assumption registry

| ID | Assumption | Pattern | Approved | Review |
|---|---|---|---|---|
| ASSUME-UK-GDPR-REG-001 | ICO tier classification self-assessed; DPO must review annually or on material change to headcount/turnover | 2 | Pending | 2027-05 |
| ASSUME-UK-GDPR-TRANSFER-001 | UK IDTA (B1.0) is the standard mechanism; EU SCCs alone insufficient; UK adequacy list is distinct from EC adequacy | 1 | Pending | 2027-05 |
| ASSUME-UK-GDPR-AGE-001 | DPA 2018 §9 sets UK age of consent at 13; when serving both UK and EU users, member state minimums (13–16) may differ | 1 | Pending | 2027-05 |
| ASSUME-UK-GDPR-ROPA-001 | Combined ROPA may cover UK and EU if it distinguishes the two; undifferentiated ROPA is acceptable for UK-only processors | 2 | Pending | 2027-05 |

## Parse status: Complete — UK-specific deltas parsed; run in conjunction with EU GDPR spec files for full coverage; 4 assumptions recorded

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Privacy notice | UK GDPR Art. 13/14, EU GDPR Art. 13/14, CCPA §1798.100 | Separate notices required if serving both UK and EU; separate if serving US |
| Data Processing Agreement | UK GDPR Art. 28, EU GDPR Art. 28, HIPAA BAA | Different templates; UK IDTA ≠ EU SCCs |
| Breach notification | UK GDPR Art. 33 (72h to ICO), EU GDPR Art. 33 (72h to lead SA) | Separate notifications if dual-regulator (UK + EU) |
| DPIA | UK GDPR Art. 35, EU GDPR Art. 35 | Same methodology; separate submission to ICO if required |
| Records of processing | UK GDPR Art. 30, EU GDPR Art. 30 | If operating in both UK and EU, separate records required |
