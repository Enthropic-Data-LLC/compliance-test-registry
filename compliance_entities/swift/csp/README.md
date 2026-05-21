# SWIFT Customer Security Programme (CSP) — CSCF v2025

**Authority:** SWIFT (Society for Worldwide Interbank Financial Telecommunication)
**Scope:** All SWIFT users connecting to the SWIFT network; 25 mandatory + 6 advisory controls

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — control confidence map, annual attestation gate, 10 assumptions | ✅ |
| [`secure-environment-controls.md`](./secure-environment-controls.md) | Objectives 1+2 — Restrict Internet Access + Segregate Critical Systems: Controls 1.1 (secure zone isolation), 1.2 (patch SLAs 3/6 months), 1.3 (virtualisation hardening), 2.1 (dedicated operator PCs), 2.2 (internal data flows), 2.3A (operator PC patches), 2.5A (back-office data flows), 2.7A (quarterly vuln scanning) | ✅ |
| [`access-credential-controls.md`](./access-credential-controls.md) | Objectives 3+4 — Credentials + Access Management: Controls 3.1 (password policy min 8/12 chars, 90-day rotation), 3.2 (MFA all operators), 3.3 (physical Secure Zone), 4.1 (password hashing/transmission), 4.2 (HSM/PAM for privileged creds), 4.3A (staff screening), 4.4 (HSM signing keys), 5.1 (least-privilege, annual review), 5.2 (session timeout 15min, encrypted), 5.3A (SWIFT role separation of duties) | ✅ |
| [`detect-respond-controls.md`](./detect-respond-controls.md) | Objectives 5+6 — Detect + Respond: Controls 6.1 (IDS/IPS), 6.2 (FIM on SWIFT software), 6.3 (DAM on SWIFT databases), 6.4 (log retention 12 months), 7.1 (IRP with SWIFT scenarios), 7.3A (annual pentest), annual KYC-SA attestation gate | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Control |
|---|---|---|
| Critical patch application | ≤90 days (3 months) from release | 1.2, 2.3A |
| Other patch application | ≤180 days (6 months) from release | 1.2, 2.3A |
| Quarterly vulnerability scanning | ≤90 days between scans | 2.7A |
| Minimum password length (standard) | 8 characters | 3.1 |
| Minimum password length (privileged) | 12 characters | 3.1 |
| Password rotation | ≤90 days | 3.1 |
| MFA for SWIFT operators | Required; hardware token or equivalent; no SMS/voice | 3.2 |
| Session inactivity timeout | ≤15 minutes | 5.2 |
| SWIFT transaction log retention | ≥365 days (12 months) | 6.4 |
| Annual penetration test | ≤12 months between engagements | 7.3A |
| IRP test | Annual | 7.1 |
| Annual self-attestation deadline | December 31 | KYC-SA |

## Parse status: Complete — all 25 mandatory controls parsed; 3 spec files; 10 assumptions recorded
