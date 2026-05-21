# FedRAMP — Federal Risk and Authorization Management Program

**Authority:** FedRAMP Program Management Office (PMO); CISA; OMB; enforced by federal agencies
**Scope:** Cloud Service Providers (CSPs) offering cloud services to U.S. federal agencies; Moderate and High baselines most common; Low baseline for public data only

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — Moderate/High baseline families mapped, 19 open assumptions | ✅ |
| [`conmon-and-overlays.md`](./conmon-and-overlays.md) | FedRAMP-specific overlays: ConMon (monthly scans), IR-6 (1-hour US-CERT), SC-13 (FIPS 140-2/3), IA-2(12) (PIV), CONUS data residency, 3PAO annual assessment, SCRM | ✅ |
| [`account-contingency-media.md`](./account-contingency-media.md) | AC (account review cadences, FIPS remote access, privileged separation, 30-min session termination), CP (contingency plan, annual test, 25-mile alternate storage, daily backups, RTO/RPO), MP (NIST 800-88 sanitization, FIPS tools, 3yr records), PS (investigation levels per baseline, 4h account disable, 5-day transfer review, annual access agreements) | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Control |
|---|---|---|
| Monthly vulnerability scanning | Every 30 days (OS/infra) | RA-5 overlay |
| Incident reporting to US-CERT | Within 1 hour | IR-6 overlay |
| Critical vulnerability remediation (CVSS ≥9.0) | Within 30 days | CA-5 overlay |
| Annual 3PAO assessment | Every 12 months | CA-2/CA-8 |
| Significant change notification to agency | Within 30 days | CM-3 overlay |
| Departed user account disable | Same day (day of termination) | AC-2 overlay |
| Credentials revoked after termination | Within 4 hours | PS-4 overlay |
| Personnel transfer access review | Within 5 business days | PS-5 overlay |
| Contingency plan test | Annual; High requires functional test | CP-4 |
| User data backup | Daily | CP-9 overlay |
| Backup restoration test | Annual | CP-9 overlay |
| Alternate storage site separation | ≥25 miles from primary | CP-6 overlay |
| Media sanitization method | NIST 800-88 clear/purge/destroy; FIPS-validated tools | MP-6 overlay |
| Media disposal record retention | ≥3 years | MP-6 overlay |

## Parse status: Partial — ConMon/overlays + AC/CP/MP/PS parsed (2 spec files); remaining: AU/CM/IA/SC/SI FedRAMP parameter deltas, SA, High-only enhancements pending
