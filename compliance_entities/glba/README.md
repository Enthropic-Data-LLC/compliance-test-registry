# GLBA — Gramm-Leach-Bliley Act / FTC Safeguards Rule

**Authority:** FTC (non-bank financial institutions: 16 CFR Parts 313/314); OCC, FDIC, Federal Reserve, NCUA (bank institutions via parallel rules); revised Safeguards Rule effective June 2023
**Scope:** Financial institutions — banks, credit unions, securities firms, insurance companies, mortgage brokers, tax preparers, auto dealers, and other entities "significantly engaged" in financial activities

See [`_index.md`](./_index.md) for the full registry index, confidence map, and open assumptions.

## Contents

| File | Sections covered | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — Privacy Rule + Safeguards Rule confidence map, DETERMINISTIC thresholds, cross-standard dependencies | ✅ |
| [`safeguards-rule.md`](./safeguards-rule.md) | §314.3 (WISP), §314.4(a) (QI + board report), §314.4(c)(3) (mandatory encryption in transit + at rest), §314.4(c)(5) (MFA all employees), §314.4(g) (annual pentest + bi-annual VA), §314.4(h) (audit logs), §314.4(i) (IRP 8 elements), §314.4(k) (annual board report), §314.15 (FTC breach notification 30-day) | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Section |
|---|---|---|
| Encryption in transit | Mandatory — all customer information | §314.4(c)(3) |
| Encryption at rest | Mandatory — no compensating controls exception | §314.4(c)(3) |
| MFA | All employees accessing customer information | §314.4(c)(5) |
| Annual penetration test | At least annually (> 5,000 records) | §314.4(g)(1) |
| Bi-annual vulnerability scan | Every 6 months + after material change (> 5,000 records) | §314.4(g)(2) |
| WISP annual review | At least annually | §314.4(j) |
| Annual board/senior officer report | At least annually | §314.4(k) |
| FTC breach notification | Within 30 days of discovery (≥ 500 customers) | §314.15 |

**Parse status:** 1 spec file — WISP, QI, encryption, MFA, pentest/VA, audit logs, IRP, breach notification parsed; 6 assumptions recorded
