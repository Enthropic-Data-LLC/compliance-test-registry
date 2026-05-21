# FedRAMP — Federal Risk and Authorization Management Program

**Authority:** FedRAMP Program Management Office (PMO); CISA; OMB; enforced by federal agencies
**Scope:** Cloud Service Providers (CSPs) offering cloud services to U.S. federal agencies; Moderate and High baselines most common; Low baseline for public data only

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — Moderate/High baseline families mapped, 28 open assumptions | ✅ |
| [`conmon-and-overlays.md`](./conmon-and-overlays.md) | FedRAMP-specific overlays: ConMon (monthly scans), IR-6 (1-hour US-CERT), SC-13 (FIPS 140-2/3), IA-2(12) (PIV), CONUS data residency, 3PAO annual assessment, SCRM | ✅ |
| [`account-contingency-media.md`](./account-contingency-media.md) | AC (account review cadences, FIPS remote access, privileged separation, 30-min session termination), CP (contingency plan, annual test, 25-mile alternate storage, daily backups, RTO/RPO), MP (NIST 800-88 sanitization, FIPS tools, 3yr records), PS (investigation levels per baseline, 4h account disable, 5-day transfer review, annual access agreements) | ✅ |
| [`technical-overlays-high-enhancements.md`](./technical-overlays-high-enhancements.md) | AU (8 FedRAMP log fields, monthly log submission ≤30d, SIEM at High), IA (PIV OCSP/CRL revocation, FIPS-validated authenticators, external IdP authorization), SC (prohibited ciphers, approved TLS suites, DNSSEC, AES-256 at High), SI (monthly patch report 5-element ConMon package), SA (sub-services FedRAMP authorization, SAST+DAST at High), High-only: PS-8 insider threat (UAM/DLP/IR), IA-3 device auth, PE-9/11/12 redundant power, SR NIST 800-161 enhanced SCRM | ✅ |

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
| FedRAMP log fields required | 8 fields (date_time_utc, event_type, source_ip, user_id, resource_accessed, action_taken, outcome, session_id) | AU overlay |
| Log submission to agency/JAB | Within 30 days | AU overlay |
| SIEM aggregating all logs | Required at High | AU overlay |
| PIV revocation check | OCSP or CRL at every authentication | IA-2 overlay |
| FIPS-validated hardware authenticators | Required at High | IA-5 overlay |
| External IdP authorization | Must be FedRAMP Authorized | IA-8 overlay |
| DNSSEC for authoritative DNS zones | Required at Moderate/High | SC overlay |
| AES-256 minimum encryption | Required at High (AES-128 insufficient) | SC-28 overlay |
| Monthly patch report in ConMon | 5 required elements | SI overlay |
| External sub-service authorization | FedRAMP Authorized or agency AO approved | SA-9 overlay |
| SAST + DAST for custom code | Required at High | SA-11 overlay |
| Insider threat program | Required at High (UAM, anomaly detection, DLP, awareness training, IR playbook) | PS-8 (High) |
| Cryptographic device authentication | Required for all devices at High | IA-3 (High) |
| Redundant power + generator + UPS | Required at High | PE-9/11/12 (High) |
| Second-tier supplier identification | Required at High per NIST 800-161 | SR overlay (High) |

## Parse status: Complete — 3 spec files; all Moderate baseline overlays and High-only enhancements parsed; 28 assumptions recorded
