# HIPAA Security Rule

**Authority:** U.S. Department of Health and Human Services (HHS), Office for Civil Rights (OCR)
**Regulation:** 45 CFR Parts 160 and 164 (Security Rule: §§164.308, 164.310, 164.312, 164.314, 164.316)
**Scope:** Covered Entities (health plans, healthcare clearinghouses, healthcare providers) and their Business Associates handling ePHI (electronic Protected Health Information)

This directory contains the RDF registry for the HIPAA Security Rule, fully decomposed to DETERMINISTIC/PARAMETERIZED/CONTESTED test patterns with YAML specs and Python test stubs.

## Contents

| File | Coverage | Assumptions | Status |
|---|---|---|---|
| [`_index.md`](./_index.md) | Registry index — all 54 implementation specifications across 5 standards | ASSUME-HIPAA-001–010 | ✅ |
| [`164.308-administrative-safeguards.md`](./164.308-administrative-safeguards.md) | 9 administrative safeguard standards (risk analysis, workforce training, contingency plan, BAA, etc.) | — | ✅ |
| [`164.310-physical-safeguards.md`](./164.310-physical-safeguards.md) | 4 physical safeguard standards (facility access, workstation use, device/media controls) | — | ✅ |
| [`164.312-technical-safeguards.md`](./164.312-technical-safeguards.md) | 5 technical safeguard standards (access control, audit controls, integrity, transmission security) | — | ✅ |
| [`164.314-organizational-requirements.md`](./164.314-organizational-requirements.md) | Business Associate Agreements — required elements, execution timing, subcontractor chain | — | ✅ |
| [`164.316-policies-documentation.md`](./164.316-policies-documentation.md) | Policies and documentation — 6-year retention, review cadence, change documentation | — | ✅ |
| [`privacy/_index.md`](./privacy/_index.md) | Privacy Rule index (45 CFR Part 164, Subpart E) — index only | — | Index only |

## Key DETERMINISTIC thresholds

| Obligation | Threshold |
|---|---|
| Breach notification to HHS | Within 60 days of discovery (breaches affecting <500 individuals: annual log) |
| Breach notification to individuals | Within 60 days of discovery |
| Breach notification to media (≥500 in a state) | Within 60 days, prominent media outlet |
| Documentation retention | 6 years from creation or last effective date |
| Risk analysis | Required before ePHI is created, received, maintained, or transmitted |
| BAA execution | Required before Business Associate accesses ePHI |
| Workforce training | Before workforce member accesses ePHI; annually thereafter (industry standard) |

## Parse status: Deep — all 5 Security Rule standards parsed
