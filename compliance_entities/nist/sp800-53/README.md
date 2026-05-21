# NIST SP 800-53 r5 — Security and Privacy Controls for Information Systems

**Authority:** NIST; enforced via FISMA for federal systems; FedRAMP baseline; widely referenced for non-federal voluntary adoption
**Scope:** ~1,007 controls and enhancements across 20 families; Low / Moderate / High impact baselines per FIPS 199

See [`_index.md`](./_index.md) for the full registry index, confidence map, ODP framework, and open assumptions.

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — 20-family confidence map, ODP framework, baseline scoping, assumption registry | ✅ |
| [`core-technical-controls.md`](./core-technical-controls.md) | AU (record content, retention 90d/3yr, review cadence), AC (account management, lockout ≤3/30min, session lock ≤15min, remote/wireless protocols), IA (MFA at Moderate/High, password policy ODPs, prohibited hash algorithms), CM (baseline configuration, hardening benchmarks, least functionality, CCB), SC (TLS 1.2+ in transit, FIPS validated crypto, AES-128+ at rest, key management lifecycle), SI (patch SLAs KEV=14d/Critical=30d/High=90d, AV real-time, system monitoring, integrity verification) | ✅ |

## Key DETERMINISTIC thresholds

| Control | Threshold | Baseline |
|---|---|---|
| AU-3: Audit record fields | 6 required fields (event type, timestamp, outcome, subject, object, source) | L/M/H |
| AU-11: Log retention online | ≥90 days immediately accessible | L/M/H |
| AU-11: Archive retention | ≥3 years (Moderate/High) | M/H |
| AC-7: Failed logon lockout | ≤3 attempts → ≥30-min lockout (800-53B default ODPs) | L/M/H |
| AC-11: Session lock | ≤15-min inactivity with content hiding (800-53B default ODP) | M/H |
| AC-17: Remote access protocols | TLS 1.2+, IPsec IKEv2, SSH v2 only; HTTP/Telnet/FTP/SSLv3/TLS 1.0–1.1 prohibited | L/M/H |
| IA-2: MFA | Privileged users at Moderate; all users at High | M/H |
| SC-8: Transmission protocols | TLS 1.2+; cleartext and weak-encryption prohibited; FIPS-validated modules | M/H |
| SC-13: FIPS cryptography | FIPS 140-2 or 140-3 validated modules required | L/M/H |
| SC-28: Encryption at rest | AES-128+ minimum; DES/3DES/RC4/plaintext prohibited | M/H |
| SI-2: CISA KEV patches | ≤14 days from detection | L/M/H |
| SI-2: Critical patches | ≤30 days (CVSS ≥9.0) | L/M/H |
| SI-3: AV definitions | Updated within 24 hours; real-time scanning enabled | L/M/H |

## Parse status: Partial — AU, AC, IA, CM, SC, SI (6 of 20 families) parsed; CP, IR, CA, MA, MP, PE, PS, RA, SA, SR, PL, PM, AT, PT remaining
