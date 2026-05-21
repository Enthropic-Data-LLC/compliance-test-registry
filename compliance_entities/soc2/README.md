# SOC 2 — Trust Services Criteria

**Authority:** American Institute of CPAs (AICPA); attestation by licensed CPA firms
**Scope:** Service organizations; criteria applicable to Security (CC series, mandatory), Availability (A1), Confidentiality (C1), Processing Integrity (PI1), and Privacy (P series, optional)

This directory contains the RDF registry for SOC 2 Trust Services Criteria (2017 edition with 2022 points of focus updates).

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — 64 CC/A/C/PI/P criteria mapped | ✅ |
| [`cc1-cc2-cc3-cc4-governance-risk.md`](./cc1-cc2-cc3-cc4-governance-risk.md) | CC1 (COSO environment), CC2 (communications), CC3 (risk assessment), CC4 (monitoring) | ✅ |
| [`cc6-logical-physical-access.md`](./cc6-logical-physical-access.md) | CC6 — Logical and physical access controls (provisioning, MFA, encryption, physical security) | ✅ |
| [`cc7-system-operations.md`](./cc7-system-operations.md) | CC7 — System operations (vulnerability management, anomaly detection, incident response) | ✅ |
| [`cc8-cc5-change-control-activities.md`](./cc8-cc5-change-control-activities.md) | CC8 (change management), CC5 (control activities) | ✅ |
| [`cc9-c1-pi1-additional-criteria.md`](./cc9-c1-pi1-additional-criteria.md) | CC9 (risk mitigation), C1 (confidentiality), PI1 (processing integrity) | ✅ |
| [`a1-availability.md`](./a1-availability.md) | A1 — Availability criteria (RTO/RPO commitments, capacity, disaster recovery) | ✅ |
| [`p-series-privacy.md`](./p-series-privacy.md) | P1 (notice — 8 elements, delivery, material change update), P2 (consent mechanisms, withdrawal), P3 (collection limitation, sensitive opt-in), P4 (use limitation, retention, disposal), P5 (subject access response, correction), P6 (disclosure basis, third-party contracts, breach notification), P7 (data quality), P8 (monitoring, complaints, incident log, annual attestation) | ✅ |

## Key DETERMINISTIC thresholds (Privacy criteria)

| Obligation | Threshold | Criterion |
|---|---|---|
| Privacy notice update after material change | 30 days | P1.3 |
| Personal information used only for stated purposes | Binary — undisclosed purpose = violation | P4.1 |
| Third-party disclosures must match privacy notice | Binary — undisclosed recipient = violation | P6.1 |
| Disposal log required fields | 4 fields — all must be present | P4.3 |
| Privacy complaint response | 30 days | P8.1 |
| Annual data quality review | 365 days max | P7.1 |
| Annual privacy program review | 365 days max | P8.1 |
| Consent withdrawal honored | Processing must cease | P2.2 |

## Parse status: Complete — Security (CC) criteria, Availability (A1), Confidentiality (C1), Processing Integrity (PI1), and Privacy (P1–P8) fully parsed; 25 assumptions recorded
