# FedRAMP — Federal Risk and Authorization Management Program

**Authority:** FedRAMP Program Management Office (PMO); CISA; OMB; enforced by federal agencies
**Scope:** Cloud Service Providers (CSPs) offering cloud services to U.S. federal agencies; Moderate and High baselines most common; Low baseline for public data only

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — Moderate/High baseline families mapped, 10 open assumptions | ✅ |
| [`conmon-and-overlays.md`](./conmon-and-overlays.md) | FedRAMP-specific overlays: ConMon (monthly scans), IR-6 (1-hour US-CERT), SC-13 (FIPS 140-2/3), IA-2(12) (PIV), CONUS data residency, 3PAO annual assessment | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Control |
|---|---|---|
| Monthly vulnerability scanning | Every 30 days (OS/infra) | RA-5 overlay |
| Incident reporting to US-CERT | Within 1 hour | IR-6 overlay |
| Critical vulnerability remediation (CVSS ≥9.0) | Within 30 days | CA-5 overlay |
| Annual 3PAO assessment | Every 12 months | CA-2/CA-8 |
| Significant change notification to agency | Within 30 days | CM-3 overlay |

## Parse status: Partial — ConMon and key overlays parsed; remaining Moderate baseline families (AC, CP, MP, PS, SA) pending
