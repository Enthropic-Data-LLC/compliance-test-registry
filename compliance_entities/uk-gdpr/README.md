# UK GDPR + Data Protection Act 2018

**Authority:** Information Commissioner's Office (ICO)
**Scope:** Processing of personal data of UK data subjects; applies to controllers and processors established in the UK and to non-UK entities offering goods/services to UK data subjects or monitoring their behavior

See [`_index.md`](./_index.md) for the full registry index, confidence map, and open assumptions.

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — UK vs EU GDPR delta table, international transfer mechanisms, ICO registration, confidence map | ✅ |
| [`uk-specific-deltas.md`](./uk-specific-deltas.md) | ICO registration (existence + tier), age of consent = 13 (DPA 2018 §9), 72-hour breach to ICO, dual-regulator breach notification, UK IDTA / UK Addendum transfer mechanisms, dual-regulator ROPA separation | ✅ |

**Usage:** Run these tests in addition to the EU GDPR spec files (`compliance_entities/gdpr/`) when processing UK personal data. UK GDPR is structurally identical to EU GDPR — the delta file covers only the UK departures. EU GDPR tests cover lawful basis, consent, Art. 13/14 privacy notices, DSRs (Art. 15–22), DPIA (Art. 35), DPA (Art. 28), and the 72-hour breach timeline.

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Article / Section |
|---|---|---|
| Breach notification to ICO | 72 hours from becoming aware | Art. 33 UK GDPR |
| SAR response | 1 month + 2-month extension with notice | Art. 15 UK GDPR |
| Age of consent (ISS) | 13 years minimum | DPA 2018 §9 |
| ICO registration renewal | Annual (12 months) | DPA 2018 / Fee Regulations |
| ICO Tier 1 fee | £40/year (≤10 staff AND ≤£632K turnover) | Fee Regulations |
| ICO Tier 2 fee | £60/year (≤250 staff AND ≤£36M turnover) | Fee Regulations |
| ICO Tier 3 fee | £2,900/year (large organisations) | Fee Regulations |
| UK IDTA version | B1.0 (ICO-approved, March 2022) | Art. 46 UK GDPR |

## Parse status: Complete — UK-specific deltas parsed; EU GDPR base tests apply in full; 4 assumptions recorded
