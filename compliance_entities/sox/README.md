# SOX — Sarbanes-Oxley Act (IT General Controls)

**Authority:** Public Company Accounting Oversight Board (PCAOB); SEC; external auditors
**Scope:** Public companies with securities listed in the US; Section 404 (ICFR — Internal Control over Financial Reporting) and Section 302 (CEO/CFO certification); IT General Controls (ITGCs) underlying financial reporting systems

See [`_index.md`](./_index.md) for the full registry index, confidence map, and open assumptions.

## Contents

| File | Controls covered | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — 4 ITGC domains, 9 open assumptions, DETERMINISTIC thresholds | ✅ |
| [`itgc-access-change-operations.md`](./itgc-access-change-operations.md) | Logical Access (provisioning, deprovisioning, review, SoD), Change Management (authorization, env separation), Computer Operations (backup, log retention), Deficiency Tracking | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Domain |
|---|---|---|
| Privileged account deprovisioning | ≤1 business day from termination | Logical Access |
| Standard account deprovisioning | ≤5 business days from termination | Logical Access |
| Privileged access review | Every 3 calendar months | Logical Access |
| Standard access review | Every 12 calendar months | Logical Access |
| SoD matrix review | At least once per 12 calendar months | Logical Access |
| Emergency change retrospective approval | Within 5 business days | Change Management |
| Backup restoration test | At least once per 12 calendar months | Computer Operations |
| Audit log retention | 7 years (§802) | Computer Operations |

**Parse status:** 1 spec file — Logical Access, Change Management, Computer Operations, Deficiency Tracking parsed
