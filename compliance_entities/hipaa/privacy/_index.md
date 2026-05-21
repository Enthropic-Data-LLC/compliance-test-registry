# HIPAA Privacy Rule — 45 CFR Part 164 Subpart E

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Uses and disclosures of Protected Health Information (PHI); individual rights; notice of privacy practices; minimum necessary standard
**Authority:** U.S. Department of Health and Human Services (HHS) / Office for Civil Rights (OCR)
**Enforcing context:** Covered entities (health plans, healthcare clearinghouses, healthcare providers who transmit PHI electronically); business associates
**Note:** This registry covers the Privacy Rule only. The Security Rule (ePHI technical/administrative/physical safeguards) is in the sibling entry at `hipaa/_index.md`. The Privacy Rule governs PHI in ALL forms (paper, oral, electronic); the Security Rule governs ePHI only.

---

## Summary

| Metric | Count |
|---|---|
| Core sections | ~15 |
| Individual rights | 6 |
| Sections parsed (individual files) | 2 (uses-disclosures-authorization.md — §§164.502, 164.508, 164.512, 164.514; individual-rights-breach.md — §§164.404–414, 164.520, 164.522, 164.524, 164.526, 164.528) |
| Fully automated (DETERMINISTIC) | Moderate — notice deadlines, access response timelines, authorization elements, breach notification |
| Partial automation (PARAMETERIZED) | Dominant — minimum necessary determination, TPO scope, NPP acknowledgment |
| Human-determination required (CONTESTED) | Moderate — minimum necessary, public interest exceptions |
| Open assumptions | 9 (ASSUME-HIPAA-PRIV-BA-001, MINNEC-001, AUTH-001, DEID-001, NPP-001, ACCESS-001, AMEND-001, ACCT-001, BREACH-001) |

---

## Permitted uses and disclosures (§164.502) — the central framework

PHI may only be used or disclosed for:
1. **Treatment, Payment, Healthcare Operations (TPO)** — PARAMETERIZED; scope of each is defined but broad
2. **With individual authorization** — DETERMINISTIC checklist of required authorization elements
3. **Incidental to permitted use** — PARAMETERIZED; reasonable safeguards required
4. **Limited dataset** — DETERMINISTIC; specific identifiers removed
5. **Public interest activities** — 12 categories; PARAMETERIZED/CONTESTED

Any other use or disclosure requires a HIPAA-compliant authorization.

---

## Per-section confidence map

### §164.502 — Uses and Disclosures

| Requirement | Confidence | Notes |
|---|---|---|
| Minimum necessary standard (§164.502(b)) | PARAMETERIZED | Only the minimum necessary PHI to accomplish the purpose; "minimum necessary" determination is org-defined |
| Business associate agreement before disclosure | DETERMINISTIC | BAA required before disclosing PHI to BA; binary |
| Verification of identity/authority before disclosure | PARAMETERIZED | Reasonable verification before disclosing to requestors |

### §164.508 — Authorizations

When authorization is required, it must contain all required elements:

| Element | Confidence |
|---|---|
| Description of the information to be used/disclosed | DETERMINISTIC |
| Name/class of persons authorized to make use/disclosure | DETERMINISTIC |
| Name/class of persons to whom disclosure may be made | DETERMINISTIC |
| Description of each purpose | DETERMINISTIC |
| Expiration date or expiration event | DETERMINISTIC |
| Individual's signature and date | DETERMINISTIC |
| Written right to revoke | DETERMINISTIC |
| Ability/inability to condition treatment/payment on authorization | DETERMINISTIC |
| Potential for re-disclosure | DETERMINISTIC |

**Authorization completeness is DETERMINISTIC** — all 9 elements must be present.

### §164.512 — Uses and Disclosures Without Authorization (Public Interest)

12 categories including: public health activities, abuse/neglect reporting, health oversight, judicial proceedings, law enforcement, decedents, organ donation, research, serious threat, specialized government functions, workers' compensation.

Each category has specific conditions. Most are PARAMETERIZED (conditions that must be met); some have DETERMINISTIC gating conditions (e.g., court order is binary).

### §164.514 — De-identification

Two methods to de-identify PHI (removing it from Privacy Rule scope):

| Method | Description | Confidence |
|---|---|---|
| Expert determination | Qualified statistician certifies very small re-identification risk | PARAMETERIZED |
| Safe Harbor | Remove all 18 specified identifiers | DETERMINISTIC — 18-element checklist |

**Safe Harbor 18 identifiers** (DETERMINISTIC checklist — all must be removed/generalized):
Names, geographic subdivisions smaller than state (except first 3 digits of ZIP if population > 20,000), dates (except year) for individuals ≥ 90, phone numbers, fax numbers, email addresses, SSN, medical record numbers, health plan beneficiary numbers, account numbers, certificate/license numbers, VINs, device identifiers, web URLs, IP addresses, biometric identifiers, full-face photos, any other unique identifying numbers/codes.

---

## Individual rights — confidence map

| Right | Section | Response deadline | Confidence | Notes |
|---|---|---|---|---|
| Right of access (to PHI) | §164.524 | 30 days (extendable 30 days with notice) | DETERMINISTIC | Clock starts at receipt of request; fee limits apply |
| Right to request amendment | §164.526 | 60 days (extendable 30 days) | DETERMINISTIC | Denial permitted; denial must be written with reason |
| Right to an accounting of disclosures | §164.528 | 60 days (extendable 30 days) | DETERMINISTIC | 6-year lookback for most disclosures |
| Right to request restrictions | §164.522 | Must respond to request | PARAMETERIZED | CE not required to agree unless: payment-only, patient pays out-of-pocket in full |
| Right to request confidential communications | §164.522(b) | Reasonable request must be accommodated | PARAMETERIZED | Cannot require explanation of reason |
| Right to notification of breach | §164.404 | 60 calendar days from discovery | DETERMINISTIC | Notification to individual; notice of media for > 500 in jurisdiction |

---

## Notice of Privacy Practices (NPP) — §164.520

| Requirement | Confidence | Notes |
|---|---|---|
| NPP must be provided | DETERMINISTIC | Provided at first service delivery; posted prominently in facility; on website |
| NPP required elements | DETERMINISTIC | Header required verbatim; description of uses/disclosures; individual rights; CE duties; effective date; contact for complaints |
| Acknowledgment of receipt | DETERMINISTIC | Must make good-faith effort to obtain written acknowledgment from patients |
| NPP update | DETERMINISTIC | Updated NPP distributed within 60 days of material change |

---

## Breach notification (§164.400–164.414)

| Notification | Deadline | Recipient |
|---|---|---|
| Individual notification | 60 calendar days from discovery | Each affected individual |
| Media notification (>500 in state/jurisdiction) | 60 calendar days from discovery | Prominent media outlet in affected jurisdiction |
| HHS notification (>500) | 60 calendar days from discovery | HHS Secretary |
| HHS notification (<500) | Annual log; submitted to HHS no later than 60 days after end of calendar year | HHS Secretary |

**Discovery date:** The date the CE or BA knew or by exercising reasonable diligence would have known of the breach.

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Section |
|---|---|---|
| Individual access response | 30 days (+ 30 extension with notice) | §164.524 |
| Amendment response | 60 days (+ 30 extension with notice) | §164.526 |
| Accounting of disclosures response | 60 days (+ 30 extension with notice) | §164.528 |
| Individual breach notification | 60 days from discovery | §164.404 |
| Media breach notification (>500) | 60 days from discovery | §164.406 |
| HHS breach notification (>500) | 60 days from discovery | §164.408 |
| HHS breach notification (<500) | Annual; 60 days after calendar year end | §164.408 |
| NPP update distribution | 60 days after material change | §164.520(b)(3) |
| Authorization elements | 9 required elements — all must be present | §164.508(c) |
| Safe Harbor de-identification | 18 identifiers must be removed | §164.514(b)(2) |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Breach notification | HIPAA Privacy Rule §164.404, HIPAA Security Rule (for ePHI), GDPR Art. 33–34, SEC 8-K | Different deadlines and recipients; same IRP infrastructure |
| Authorization form | HIPAA Privacy Rule §164.508, FDA 21 CFR Part 50 (research informed consent) | Medical research combining treatment and research may require both HIPAA authorization and 21 CFR Part 50 consent |
| Business associate agreements | HIPAA Privacy Rule + Security Rule §164.314, GDPR Art. 28 DPA | BAA required for PHI; DPA required for EU personal data; combined template feasible |
| De-identification | HIPAA §164.514, GDPR Art. 4(5) pseudonymization, CCPA personal information definition | Safe Harbor de-identification removes data from HIPAA scope; may not remove it from GDPR/CCPA scope |
| Notice of Privacy Practices | HIPAA §164.520, GDPR Art. 13 privacy notice, CCPA §1798.100 privacy policy | All require privacy notices; different required elements; layered notice approach can address all |

---

## Open assumption registry

| ID | Section | Summary | Review date |
|---|---|---|---|
| ASSUME-HIPAA-PRIV-BA-001 | §164.504(e)(2) | Privacy Rule BAA must include 8 elements: permitted uses, prohibition on non-permitted use, appropriate safeguards, breach reporting obligation (60 days/30 recommended), subcontractor compliance, individual rights pass-through, PHI availability for individual rights, return/destroy at termination | 2026-11-01 |
| ASSUME-HIPAA-PRIV-MINNEC-001 | §164.502(b) | Minimum necessary: role-based access profiles define minimum PHI per job function; reviewed annually by Privacy Officer; routine requests have standard protocols; non-routine reviewed individually; exceptions: treatment by treating providers, individual's own requests, authorizations, HHS oversight | 2026-11-01 |
| ASSUME-HIPAA-PRIV-AUTH-001 | §164.508 | Authorization form: all 9 elements on single form; psychotherapy notes on separate form (§164.508(a)(2)); marketing authorizations disclose financial remuneration; expiration event must be specific; reviewed and approved by Privacy Officer | 2026-11-01 |
| ASSUME-HIPAA-PRIV-DEID-001 | §164.514(b)(1) | Expert determination: certified by qualified statistician (MS+ in statistics/biostatistics); written certification attached to dataset; certification expires after 24 months or on dataset augmentation; re-identification risk < 9% per NIST SP 800-188 guidance | 2026-11-01 |
| ASSUME-HIPAA-PRIV-NPP-001 | §164.520 | NPP: 7 required elements including verbatim header; good-faith acknowledgment effort required; patient refusal must be documented; direct treatment providers provide at first service; health plans at enrollment and every 3 years | 2026-11-01 |
| ASSUME-HIPAA-PRIV-ACCESS-001 | §164.524 | Access fees: cost-based only (labor + supplies + postage); no search/retrieval fees; ePHI in electronic format requested by individual must be provided electronically; reviewable denials require second review by uninvolved licensed professional | 2026-11-01 |
| ASSUME-HIPAA-PRIV-AMEND-001 | §164.526 | Amendment: accepted amendments propagated to identified recipients within 30 days; disclosure accounting (§164.528) used to identify recipients; statement of disagreement included in future disclosures of affected PHI | 2026-11-01 |
| ASSUME-HIPAA-PRIV-ACCT-001 | §164.528 | Accounting log fields: date, recipient name/address, PHI description, purpose or copy of request; accountable disclosures exclude TPO/authorization/incidental/limited dataset/national security/correctional/workforce; repeated disclosures of same type: first entry + frequency description is sufficient | 2026-11-01 |
| ASSUME-HIPAA-PRIV-BREACH-001 | §164.404 | Unsecured PHI: PHI not encrypted per NIST SP 800-111 or destroyed; 4-factor low-probability assessment required for every potential breach; if low probability cannot be established, incident is a breach; Privacy Officer reviews all assessments | 2026-11-01 |

---

## Specification file status

| File | Coverage | Assumptions | Status |
|---|---|---|---|
| `uses-disclosures-authorization.md` | §164.502 (BAA required, minimum necessary, disclosure basis), §164.508 (9-element authorization, conditioned treatment prohibition, revocation), §164.512 (public interest categories), §164.514 (Safe Harbor 18 identifiers, ZIP code compliance, expert determination, limited dataset DUA) | ASSUME-HIPAA-PRIV-BA-001, MINNEC-001, AUTH-001, DEID-001 | ✅ Parsed |
| `individual-rights-breach.md` | §164.520 (NPP elements, verbatim header, acknowledgment, 60-day update), §164.522 (OOP restriction mandatory, agreed restrictions honored), §164.524 (30-day access, ePHI electronic format, reviewable denials), §164.526 (60-day amendment, written denials, propagation), §164.528 (60-day accounting, 6-year lookback, log fields), §164.404–414 (individual/media/HHS notification deadlines, annual HHS log, 4-factor harm assessment) | ASSUME-HIPAA-PRIV-NPP-001, ACCESS-001, AMEND-001, ACCT-001, BREACH-001 | ✅ Parsed |

## Parse status: Complete — §§164.502, 164.508, 164.512, 164.514, 164.520, 164.522, 164.524, 164.526, 164.528, 164.404–414 parsed; 9 assumptions recorded
