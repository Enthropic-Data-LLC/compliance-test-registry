# NIST CSF 2.0 — Cybersecurity Framework

**Authority:** National Institute of Standards and Technology (NIST)
**Scope:** Six Functions (GV-Govern, ID-Identify, PR-Protect, DE-Detect, RS-Respond, RC-Recover); 22 categories; 106 subcategories
**Version:** CSF 2.0 (February 2024) — adds Govern function; supersedes CSF 1.1

See [`_index.md`](./_index.md) for the full registry index, confidence map, and open assumptions.

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — function/category confidence map, cross-framework mapping table, Tier/Profile framework | ✅ |
| [`function-profiles-subcategories.md`](./function-profiles-subcategories.md) | Profile gap framework; GV (OC, RM, SC); ID (AM, RA); PR (AA, AT, DS, PS, IR); DE (CM, vulnerability scanning); RS (MA, CO); RC (RP) | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Subcategory |
|---|---|---|
| Privileged access review | At least quarterly (3 months) | PR.AA-05 |
| Standard access review | At least annually | PR.AA-05 |
| Asset inventory reconciliation | At least annually | ID.AM-01/02 |
| Awareness training completion | At least annually; ≥95% completion rate | PR.AT-01 |
| Patch: CISA KEV | 14 days | PR.PS-02 |
| Patch: Critical (non-KEV, CVSS 9.0+) | 30 days | PR.PS-02 |
| Patch: High (CVSS 7.0–8.9) | 60 days | PR.PS-02 |
| Patch: Medium (CVSS 4.0–6.9) | 90 days | PR.PS-02 |
| Vulnerability scanning | At least monthly | DE.CM-08 |
| IRP review | At least annually | RS.MA-01 |
| IRP test (tabletop/simulation) | At least annually | RS.MA-01 |
| Recovery plan test | At least annually | RC.RP-01 |
| Risk assessment refresh | At least annually | ID.RA-01 |
| Log retention | At least 90 days | DE.CM-01 |

## Cross-framework mapping (primary)

| CSF Subcategory | NIST 800-53 | ISO 27001 | SOC 2 | PCI DSS |
|---|---|---|---|---|
| PR.AA-03 (MFA) | IA-2(1)(2) | A.8.5 | CC6.1 | Req 8.4 |
| PR.PS-02 (Patching) | SI-2, RA-5 | A.8.8 | CC7.1 | Req 11.3 |
| PR.DS-01 (Encryption at rest) | SC-28 | A.8.24 | CC6.7 | Req 3.5 |
| DE.CM-01 (Monitoring) | CA-7 | A.8.16 | CC7.2 | Req 10.6 |
| RS.CO-02 (Incident reporting) | IR-6 | A.5.25 | CC7.3 | Req 12.10 |
| RC.RP-01 (Recovery plan) | CP-10 | A.5.29 | A1.3 | Req 12.10 |

## Parse status: Complete — all 22 categories parsed; 6 assumptions recorded
