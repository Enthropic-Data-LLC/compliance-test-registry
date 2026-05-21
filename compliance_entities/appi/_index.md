# APPI — Act on the Protection of Personal Information (Japan)

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Handling of personal information by business operators in Japan; applies to any business operator handling personal information in Japan, including foreign businesses using personal information of Japanese residents
**Authority:** Personal Information Protection Commission (PPC); sector-specific guidelines from FSA (financial), MHLW (healthcare), METI (general industry)
**Current edition:** APPI as amended by 2020 amendment (effective April 2022) — major modernization adding data breach notification, pseudonymized data, right to opt-out from third-party provision via opt-out registration
**Related:** Act on the Use of Numbers to Identify a Specific Individual (My Number Act) — separate handling requirements for social security numbers

---

## Summary

| Metric | Count |
|---|---|
| Personal information categories | 3 (General PI / Sensitive PI / Pseudonymized PI) |
| PPC fine (criminal) | JPY 1M per violation (criminal); administrative: PPC order + publication of non-compliance |
| Data subject rights | 5 core |
| Sections parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | Moderate — breach notification deadline; sensitive data consent; third-party transfer notice |
| Partial automation (PARAMETERIZED) | Dominant — security management measures; purpose limitation |
| Human-determination required (CONTESTED) | Low-Moderate — "leakage likely to harm individual rights" threshold |
| Open assumptions | 0 |

---

## APPI data categories

| Category | Definition | Handling requirements |
|---|---|---|
| General personal information | Information that can identify a specific individual (name, address, DOB, etc.) | Standard APPI requirements |
| Sensitive personal information (要配慮個人情報) | Race, creed, social status, medical history, criminal record, disabilities | Acquisition requires opt-in consent; stricter handling |
| Pseudonymized information (仮名加工情報) | Processed to prevent identification without separate cross-reference | Reduced rights obligations; cannot be disclosed to third parties |
| Anonymized information (匿名加工情報) | Irreversibly de-identified | Not "personal information" — outside APPI scope |

---

## Core obligations — confidence map

### Purpose specification and limitation

| Requirement | Confidence | Notes |
|---|---|---|
| Purpose of use specified | DETERMINISTIC | Purpose specified to the extent possible |
| Purpose publicly disclosed or notified to individual | DETERMINISTIC | At time of collection or immediately after |
| Purpose change | PARAMETERIZED | Only within reasonably expected scope |

### Collection and consent

| Requirement | Confidence | Notes |
|---|---|---|
| Acquisition of sensitive PI | DETERMINISTIC — prior opt-in consent required | No other legal basis |
| Acquisition from third parties | PARAMETERIZED — records required | Record retention: 1 year from acquisition |

### Security management measures (安全管理措置) — Art. 23

| Requirement | Confidence | Notes |
|---|---|---|
| Security management measures appropriate to scale and nature | PARAMETERIZED | PPC guidelines specify organizational, human, physical, technical measures |
| Employee supervision | PARAMETERIZED | Supervision of employees handling PI |
| Subcontractor supervision | PARAMETERIZED | Appropriate supervision of entrustees (processors) |

### Third-party provision — Art. 27

| Requirement | Confidence | Notes |
|---|---|---|
| Prior consent for third-party provision | DETERMINISTIC | Default rule — consent required |
| Opt-out mechanism (general PI only) | DETERMINISTIC | Must register opt-out with PPC before providing without consent |
| Third-party provision records | DETERMINISTIC | Records of provision and receipt; 1-3 year retention |

---

## Breach notification — 2022 amendment (DETERMINISTIC)

| Incident type | Report to PPC | Notify Individuals |
|---|---|---|
| Sensitive PI leaked | Required | Required |
| Leak likely to harm individual rights and interests | Required | Required |
| Fraudulent access (e.g., hacking) with PI leakage | Required | Required |
| Large-scale leakage (1,000+ individuals) | Required | Required |
| PPC report deadline | Within 3–5 days of discovery (promptly) | Without delay |
| PPC final report | Within 30 days of discovery | — |

---

## Data subject rights — DETERMINISTIC response obligations

| Right | Response deadline | Confidence |
|---|---|---|
| Disclosure (access) of retained personal data | Within 2 weeks of request | DETERMINISTIC |
| Correction, addition, deletion | Without delay (within 2 weeks as practice) | DETERMINISTIC |
| Cessation of use / erasure | Without delay | DETERMINISTIC |
| Cessation of third-party provision | Without delay | DETERMINISTIC |
| Third-party provision records disclosure | Within 2 weeks | DETERMINISTIC |

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Article |
|---|---|---|
| Sensitive PI acquisition | Prior opt-in consent required | Art. 20 |
| Third-party provision (default) | Prior consent required | Art. 27 |
| Breach notification to PPC | Within 3–5 days (promptly) | Art. 26 |
| Breach final report to PPC | Within 30 days | Art. 26 |
| DSR response (disclosure) | Within 2 weeks | Art. 33 |
| Opt-out registration before third-party provision | Before first provision | Art. 27(2) |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Privacy notice | APPI (purpose notification), EU GDPR Art. 13, LGPD | Different required elements; layered notice approach feasible |
| Data subject rights | APPI Arts. 33–39, EU GDPR Arts. 15–22, LGPD | 2-week APPI deadline < GDPR 30 days; stricter |
| Breach notification | APPI Art. 26, EU GDPR Art. 33 (72h), LGPD Art. 48 | APPI 3-5 days — less precise than GDPR 72h |
| Third-party processor agreements | APPI Art. 25 (entrustee supervision), EU GDPR Art. 28 DPA | Same supervision requirement; APPI does not require written DPA explicitly |
| Sensitive data | APPI Art. 20, EU GDPR Art. 9 | Similar categories; APPI includes social status and disability |
