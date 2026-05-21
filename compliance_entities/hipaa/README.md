# HIPAA — Security Rule + Privacy Rule

**Authority:** U.S. Department of Health and Human Services (HHS), Office for Civil Rights (OCR)
**Regulations:** Security Rule: 45 CFR §§164.308, 164.310, 164.312, 164.314, 164.316 (ePHI only) | Privacy Rule: 45 CFR §§164.500–164.534 (PHI in all forms)
**Scope:** Covered Entities (health plans, healthcare clearinghouses, healthcare providers) and their Business Associates

## Security Rule Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Security Rule registry index — 54 implementation specifications; 23 assumptions | ✅ |
| [`164.308-administrative-safeguards.md`](./164.308-administrative-safeguards.md) | Risk analysis, workforce training, contingency plan, incident response, BAA, evaluation | ✅ |
| [`164.310-physical-safeguards.md`](./164.310-physical-safeguards.md) | Facility access controls, workstation use/security, device and media controls | ✅ |
| [`164.312-technical-safeguards.md`](./164.312-technical-safeguards.md) | Access control, audit controls, integrity, authentication, transmission security | ✅ |
| [`164.314-organizational-requirements.md`](./164.314-organizational-requirements.md) | Business Associate Agreements — required elements, execution timing, subcontractor chain | ✅ |
| [`164.316-policies-documentation.md`](./164.316-policies-documentation.md) | Policies and documentation — 6-year retention, review cadence, change documentation | ✅ |

## Privacy Rule Contents

| File | Coverage | Status |
|---|---|---|
| [`privacy/_index.md`](./privacy/_index.md) | Privacy Rule registry index — confidence map, 15 assumptions | ✅ |
| [`privacy/uses-disclosures-authorization.md`](./privacy/uses-disclosures-authorization.md) | §164.502 (BAA required, minimum necessary), §164.508 (9-element authorization), §164.512 (public interest disclosures), §164.514 (Safe Harbor 18-identifier de-identification, expert determination, limited dataset) | ✅ |
| [`privacy/individual-rights-breach.md`](./privacy/individual-rights-breach.md) | §164.520 (NPP elements + acknowledgment + 60-day update), §164.522 (OOP restriction mandatory, agreed restrictions honored), §164.524 (30-day access), §164.526 (60-day amendment), §164.528 (60-day accounting, 6-year lookback), §164.404–414 (60-day breach notification — individual, media, HHS; 4-factor harm assessment) | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Rule |
|---|---|---|
| Individual breach notification | 60 days from discovery | Privacy §164.404 |
| Media breach notification (> 500 in jurisdiction) | 60 days from discovery | Privacy §164.406 |
| HHS breach notification (≥ 500) | 60 days from discovery | Privacy §164.408 |
| HHS annual breach log (< 500) | 60 days after calendar year end | Privacy §164.408 |
| Individual access response | 30 days (+ 30 extension for offsite records) | Privacy §164.524 |
| Amendment response | 60 days (+ 30 extension) | Privacy §164.526 |
| Accounting of disclosures response | 60 days (+ 30 extension) | Privacy §164.528 |
| Accounting lookback period | 6 years | Privacy §164.528 |
| NPP update after material change | 60 days | Privacy §164.520 |
| Authorization elements | 9 required elements — all must be present | Privacy §164.508 |
| Safe Harbor de-identification | 18 identifiers must all be removed | Privacy §164.514 |
| Mandatory OOP restriction (health plan) | CE must agree — cannot deny | Privacy §164.522 |
| Security documentation retention | 6 years from creation or last effective date | Security §164.316 |
| BAA execution | Required before BA accesses PHI/ePHI | Both |

## Parse status: Complete — Security Rule (5 standards) + Privacy Rule (§§164.502, 164.508, 164.512, 164.514, 164.520, 164.522, 164.524, 164.526, 164.528, 164.404–414) fully parsed
