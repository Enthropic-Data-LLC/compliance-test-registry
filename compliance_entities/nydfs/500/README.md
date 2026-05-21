# NY DFS 23 NYCRR 500 — Cybersecurity Requirements for Financial Services Companies

See [`_index.md`](./_index.md) for the registry index, confidence map, and open assumptions.

## Contents

| File | Sections covered | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — 21 sections, confidence map, Class A thresholds, cross-standard dependencies | ✅ |
| [`cybersecurity-program.md`](./cybersecurity-program.md) | §500.04 (CISO/board report), §500.05 (pentest/VA), §500.06 (6-year audit trail), §500.07 (access review), §500.12 (MFA), §500.14 (training), §500.15 (encryption), §500.17 (72hr notification + annual certification), Class A requirements | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Section |
|---|---|---|
| Cybersecurity event notification | Within 72 hours of determination | §500.17(a) |
| Audit trail retention | 6 years | §500.06 |
| MFA — remote access | Required (all paths) | §500.12(a) |
| MFA — privileged accounts | Required (all accounts) | §500.12(a) |
| MFA — external web services | Required (all with external users) | §500.12(b) |
| NPI encryption in transit | Mandatory | §500.15(a) |
| NPI encryption at rest | Mandatory or CISO annual review of compensating controls | §500.15(b) |
| Penetration test | At least annually | §500.05 |
| Class A vulnerability assessment | Every 6 months | §500.05(b)(2) |
| CISO board report | At least annually | §500.04(b) |
| Access review | At least annually | §500.07(a)(3) |
| Annual certification | Filed with DFS by April 15 | §500.17(b) |
| Annual cybersecurity training | At least annually | §500.14(a) |

**Parse status:** 1 spec file — §500.04, 500.05, 500.06, 500.07, 500.12, 500.14, 500.15, 500.17 parsed; 8 assumptions recorded
