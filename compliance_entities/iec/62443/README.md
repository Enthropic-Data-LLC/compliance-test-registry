# IEC 62443 — Industrial Automation and Control System (IACS) Security

**Authority:** IEC Technical Committee 65
**Scope:** Asset owners, system integrators, component suppliers across all industrial sectors (manufacturing, oil & gas, utilities, water, transportation, building automation); NERC CIP governs electric utility BES Cyber Systems separately

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — 4 series groups, SL 1–4 framework, 7 foundational requirements, ~110 SRs, zone/conduit model, patch management, NERC CIP relationship | ✅ |
| [`fr1-fr3-iam-use-integrity.md`](./fr1-fr3-iam-use-integrity.md) | FR 1 (SR 1.1–1.13): unique IDs, no shared accounts, lockout, login banner (SL 2+), password length by SL, auth feedback; FR 2 (SR 2.1–2.12): RBAC, session lock (SL 2+), session termination, concurrent sessions (SL 3+), auditable events, timestamps; FR 3 (SR 3.1–3.9): malware protection, compensating controls for legacy, communication integrity, audit log protection | ✅ |
| [`fr4-fr7-confidentiality-availability.md`](./fr4-fr7-confidentiality-availability.md) | FR 4 (SR 4.1–4.3): encryption in transit (SL 2+), at rest (SL 3+), media sanitization; FR 5 (SR 5.1–5.4): zone/conduit architecture, default-deny firewall, DMZ, ruleset documentation; FR 6 (SR 6.1–6.2 + 62443-2-3): log accessibility, monitoring (SL 2+), patch policy, deferred patch compensating controls; FR 7 (SR 7.3–7.8): backup + restore test, config baseline, least functionality, component inventory with versions, emergency power | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | SL scope | SR |
|---|---|---|
| Unique user identifiers — no shared accounts | SL 1+ | SR 1.1 |
| Account lockout after failed attempts | SL 1+ | SR 1.11 |
| Login banner | SL 2+ | SR 1.12 |
| Session lock after inactivity | SL 2+ | SR 2.5 |
| Concurrent session limits | SL 3+ | SR 2.7 |
| Auditable events defined and logged | SL 1+ | SR 2.8 |
| Timestamp synchronization (NTP) | SL 1+ | SR 2.11 |
| Malware protection (or compensating controls) | SL 1+ | SR 3.2 |
| Audit log write-protected | SL 1+ | SR 3.9 |
| Encryption in transit | SL 2+ | SR 4.1 |
| Encryption at rest (sensitive data) | SL 3+ | SR 4.1 |
| Default-deny firewall at zone boundaries | SL 1+ | SR 5.2 |
| IACS configuration backup + restore test | SL 1+ | SR 7.3 |
| Security configuration baseline documented | SL 1+ | SR 7.6 |
| Unused ports/protocols/services disabled | SL 1+ | SR 7.7 |
| Component inventory with software versions | SL 1+ | SR 7.8 |
| Patch management policy | SL 1+ | 62443-2-3 |

## Assumption count

| File | Assumptions |
|---|---|
| fr1-fr3-iam-use-integrity.md | 3 |
| fr4-fr7-confidentiality-availability.md | 5 |
| **Total** | **8** |

## Parse status: Complete — 2 spec files covering all 7 FRs; 8 assumptions; DETERMINISTIC-dominant once SL-T established
