# NERC CIP — Critical Infrastructure Protection Standards

**Authority:** NERC; enforced by Regional Entities under FERC oversight
**Scope:** Responsible Entities owning or operating BES Cyber Systems (BCS) classified as High, Medium, or Low impact

## Contents

| File | Standard | Coverage | Status |
|---|---|---|---|
| [`_index.md`](./_index.md) | CIP-002–015 | Registry index — 14 standards, 25 assumptions, cross-dependencies, CI gate config | ✅ |
| [`CIP-002-5.1a.md`](./CIP-002-5.1a.md) | CIP-002-5.1a | BES Cyber System categorization (High/Medium/Low impact) | ✅ |
| [`CIP-003-9.md`](./CIP-003-9.md) | CIP-003-9 | Security management controls; policies; Low impact requirements | ✅ |
| [`CIP-004-7.md`](./CIP-004-7.md) | CIP-004-7 | Personnel and training (annual training, PRA, access management) | ✅ |
| [`CIP-005-7.md`](./CIP-005-7.md) | CIP-005-7 | Electronic security perimeters (ESP, EAP, interactive remote access) | ✅ |
| [`CIP-006-6.md`](./CIP-006-6.md) | CIP-006-6 | Physical security (PACS, visitor logs, physical access controls) | ✅ |
| [`CIP-007-6.md`](./CIP-007-6.md) | CIP-007-6 | System security management (ports/services, patch management, malware, AAA) | ✅ |
| [`CIP-008-6.md`](./CIP-008-6.md) | CIP-008-6 | Incident reporting and response planning (1-hr Reportable notification, 15-mo test, 90-day update) | ✅ |
| [`CIP-009-6.md`](./CIP-009-6.md) | CIP-009-6 | Recovery plans (15-month plan test, 36-month operational exercise, 90-day update) | ✅ |
| [`CIP-010-4.md`](./CIP-010-4.md) | CIP-010-4 | Configuration change management (5-element baseline, 30-day update, 35-day monitoring, VA cadences, TCA/RM) | ✅ |
| [`CIP-011-3.md`](./CIP-011-3.md) | CIP-011-3 | Information protection (BCSI classification, at-rest/in-transit encryption, reuse/disposal per NIST 800-88) | ✅ |
| [`CIP-012-2.md`](./CIP-012-2.md) | CIP-012-2 | Control center communications (IPsec/TLS protection; enforcement 2026-07-01; all impact levels) | ✅ |
| [`CIP-013-2.md`](./CIP-013-2.md) | CIP-013-2 | Supply chain risk management (6 R1.2 procurement topics, 15-month plan review) | ✅ |
| [`CIP-014-3.md`](./CIP-014-3.md) | CIP-014-3 | Physical security of transmission (R1 30/60-month cadence, R2/R6 third-party 90-day window, R3 7-day notification, R5 CONTESTED) | ✅ |
| [`CIP-015-1.md`](./CIP-015-1.md) | CIP-015-1 | Internal network security monitoring (INSM; H impact enforcement 2028-10-01; anomaly detection, retention floors, BCSI data protection) | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Standard |
|---|---|---|
| Reportable incident notification to E-ISAC/CISA | Within 1 hour of determination | CIP-008-6 R4 |
| AttemptedCompromise notification | By end of next calendar day | CIP-008-6 R4 |
| Incident/recovery plan test | At least every 15 calendar months | CIP-008-6 R2 / CIP-009-6 R2 |
| Recovery operational exercise | At least every 36 calendar months | CIP-009-6 R2.3 |
| Post-test/post-incident plan update | Within 90 calendar days | CIP-008-6 R3 / CIP-009-6 R3 |
| Baseline update after change | Within 30 calendar days | CIP-010-4 R1.3 |
| Configuration monitoring (H impact) | At least every 35 calendar days | CIP-010-4 R2 |
| Vulnerability assessment (paper or active) | At least every 15 calendar months | CIP-010-4 R3.1 |
| Active vulnerability assessment (H impact) | At least every 36 calendar months | CIP-010-4 R3.2 |
| SCRM plan review and approval | At least every 15 calendar months | CIP-013-2 R3 |
| CIP-014 R1 risk assessment (TO) | At least every 30 calendar months | CIP-014-3 R1 |
| CIP-014 R1 risk assessment (TOP with CC) | At least every 60 calendar months | CIP-014-3 R1 |
| R2/R6 third-party review | Within 90 calendar days of trigger | CIP-014-3 R2, R6 |
| R3 notification to operating TOP | Within 7 calendar days | CIP-014-3 R3 |

## Parse status: Complete — all 14 CIP standards (CIP-002 through CIP-015) parsed; 25 assumptions recorded; 2 pre-enforcement standards in informational mode (CIP-012-2: 2026-07-01; CIP-015-1: 2028-10-01)
