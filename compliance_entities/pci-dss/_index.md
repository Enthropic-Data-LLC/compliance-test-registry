# PCI DSS v4.0 — Payment Card Industry Data Security Standard

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** All 12 requirements; ~400 individual requirements; Cardholder Data Environment (CDE) and connected systems
**Authority:** PCI Security Standards Council (PCI SSC)
**Enforcing context:** Card brand mandates (Visa, Mastercard, Amex, Discover, JCB); acquiring bank contractual requirements; merchant and service provider agreements
**Current version:** v4.0 (mandatory since March 31 2025; v3.2.1 retired)

---

## Summary

| Metric | Count |
|---|---|
| Requirements (top-level) | 12 |
| Individual requirements | ~400 |
| Requirements parsed (individual files) | 12 (req-01 through req-12 — all requirements) |
| Fully automated (DETERMINISTIC) | High — PCI DSS is the most prescriptive framework in this registry |
| Partial automation (PARAMETERIZED) | Moderate (customized implementation approach adds PARAMETERIZED surface) |
| Human-determination required (CONTESTED) | Low |
| Unresolvable | Minimal |
| Open assumptions | 18 |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Compliance approach — critical pre-condition

v4.0 introduced two compliance approaches that determine test confidence:

| Approach | Description | Confidence impact |
|---|---|---|
| **Defined** | Follow the standard exactly as written — prescriptive controls | DETERMINISTIC dominant; thresholds are stated explicitly |
| **Customized** | Demonstrate the intent of a requirement is met through alternative controls | CONTESTED — QSA determination required; not automatable |

The registry tracks per-requirement which approach is in use. Customized implementation requirements are flagged as CONTESTED and require Pattern 3 tests with QSA sign-off.

---

## CDE scoping — pre-condition to all tests

PCI DSS applies to the Cardholder Data Environment (CDE) and all systems connected to it. CDE scope must be formally defined before any test is enforcing:

| Scoping decision | Classification | Notes |
|---|---|---|
| Is CHD/SAD stored/processed/transmitted here? | PARAMETERIZED | Data flow diagram required; CHD presence must be attested |
| Is this system connected to the CDE? | PARAMETERIZED | Network diagram required; connectivity analysis required |
| Is a system "out of scope"? | CONTESTED | Adequate isolation must be demonstrated to QSA |

**Network segmentation** can reduce scope. Segmentation effectiveness is CONTESTED — must be validated annually by penetration testing.

---

## Per-requirement confidence map

| Req | Title | Confidence | DETERMINISTIC highlights | PARAMETERIZED surface | CONTESTED surface |
|---|---|---|---|---|---|
| 1 | Network security controls | HIGH | Firewall rule review at least every 6 months; inbound/outbound rule restrictions | Rule sufficiency; DMZ adequacy | — |
| 2 | Secure configurations | HIGH | No vendor defaults (passwords, SNMP strings); system inventory completeness | Hardening standard selection | — |
| 3 | Protect stored account data | HIGH | PAN masked to first 6/last 4 digits; PAN encrypted with strong cryptography; SAD not stored after authorization | Encryption key strength if non-AES (any key ≥ 128-bit is DETERMINISTIC) | — |
| 4 | Data transmission protection | HIGH | TLS 1.2 minimum (TLS 1.1 and below prohibited); TLS 1.3 strongly recommended; no WEP/early TLS | Certificate validity | — |
| 5 | Malware protection | HIGH | AV deployed on all applicable systems; AV definitions current (24-hour update); daily scan or continuous | Scan scope for "not commonly affected" systems | — |
| 6 | Secure systems and software | MEDIUM | Critical patches within 1 month; non-critical within 3 months; change control process | Patch criticality classification | — |
| 7 | Restrict access | HIGH | Need-to-know access; default deny all; access review at least every 6 months | Access review scope | — |
| 8 | Identify and authenticate | HIGH | Unique IDs for all users; MFA for all non-console admin access and all remote access; passwords ≥ 12 chars (or 8+ if system limits); lockout after max 10 failed attempts; session timeout ≤ 15 min idle | — | — |
| 9 | Physical access controls | MEDIUM | Visitor logs; badge system; media destruction certificates | CCTV coverage adequacy | — |
| 10 | Log all access | HIGH | Log all admin actions; log all access to audit trails; 12-month retention; 3-month immediate access; time sync (NTP) | — | — |
| 11 | Test security | HIGH | Internal/external vulnerability scans quarterly; ASV scans for external; penetration test at least annually; network and application layer included; segmentation test at least annually (or every 6 months for service providers) | Pentest scope adequacy | — |
| 12 | Policies and programs | MEDIUM | Security policy reviewed annually; targeted risk analysis for each customized control; security awareness training at least annually | Policy content adequacy | — |

---

## Key DETERMINISTIC thresholds (reference table)

These are bright-line values that Pattern 1 tests can assert directly:

| Control | Threshold | Requirement |
|---|---|---|
| Minimum TLS version | TLS 1.2 (TLS 1.1 and SSL prohibited) | Req 4.2.1 |
| Password minimum length | 12 characters (8 if system limitation) | Req 8.3.6 |
| Account lockout threshold | After maximum 10 invalid attempts | Req 8.3.4 |
| Idle session timeout | ≤ 15 minutes | Req 8.2.8 |
| Service account password change | At least every 12 months | Req 8.3.9 |
| PAN masking | First 6 / last 4 digits displayed maximum | Req 3.3.1.1 |
| Firewall rule review | Every 6 months | Req 1.2.2 |
| Access rights review | Every 6 months | Req 7.2.4 |
| Critical patch SLA | Within 1 month of release | Req 6.3.3 |
| Non-critical patch SLA | Within 3 months of release | Req 6.3.3 |
| Log retention total | 12 months | Req 10.7 |
| Log immediate access | 3 months | Req 10.7 |
| External vulnerability scan | Quarterly | Req 11.3.2 |
| Penetration test | At least annually | Req 11.4.3 |
| Annual security policy review | Every 12 months | Req 12.2 |
| Awareness training | At least annually | Req 12.6 |

---

## SAQ applicability

Self-Assessment Questionnaire (SAQ) type determines which requirements apply to smaller merchants:

| SAQ | Merchant type | Applicable requirements |
|---|---|---|
| SAQ A | Card-not-present; all CHD functions fully outsourced | Reduced subset; no system-level controls required |
| SAQ A-EP | E-commerce; third-party payment page | Broader subset including Req 6, 11 |
| SAQ B | Imprint machines or standalone dial-up terminals | Limited scope |
| SAQ B-IP | Standalone IP-connected terminals | Limited scope |
| SAQ C | POS systems with payment application; internet connection | Most requirements except some Req 1 items |
| SAQ D | All other merchants; all service providers | Full requirements (all 12) |

For the registry, SAQ scope is tracked as a pre-condition filter on each test. Tests that do not apply to the merchant's SAQ type run in informational mode only.

---

## Open assumption registry

| ID | Requirement | Summary | Review date |
|---|---|---|---|
| ASSUME-1-001 | Req 1 | NSC rule "necessary": documented business justification; least-privilege for traffic; reviewed in last 6-month cycle | 2026-05-20 |
| ASSUME-2-001 | Req 2 | Unnecessary functionality: approved services/ports list; running services compared quarterly; exceptions documented | 2026-05-20 |
| ASSUME-3-001 | Req 3 | Strong crypto for PAN: AES-128/256 FIPS 140-2/3; HMAC-SHA256 for hashing; MD5/SHA-1 not acceptable; DEK rotation ≥ annually | 2026-05-20 |
| ASSUME-3-002 | Req 3 | KEK split knowledge/dual control: HSM M-of-N or key management system requiring two individuals | 2026-05-20 |
| ASSUME-4-001 | Req 4 | Acceptable ciphers: AEAD only (AES-GCM, CHACHA20-POLY1305); NULL/EXPORT/anon/RC4/DES/3DES prohibited | 2026-05-20 |
| ASSUME-5-001 | Req 5 | "Not commonly affected" exemption: non-general-purpose OS; no user-installed software; cannot execute untrusted code; annual rationale | 2026-05-20 |
| ASSUME-5-002 | Req 5 | Anti-phishing adequate: email gateway with SPF/DKIM/DMARC + annual training + simulated phishing program | 2026-05-20 |
| ASSUME-6-001 | Req 6 | Patch criticality: CVSS ≥ 7.0 = high/critical (30-day SLA); CVSS < 7.0 = non-critical (90-day SLA); zero-days always critical | 2026-05-20 |
| ASSUME-6-002 | Req 6 | WAF adequate: inline/blocking mode; all 7 attack categories; rules updated monthly; false positive review documented | 2026-05-20 |
| ASSUME-7-001 | Req 7 | Least privilege: RBAC model with documented role entitlements; elevated privileges separate role; role definitions reviewed annually | 2026-05-20 |
| ASSUME-8-001 | Req 8 | MFA replay-resistance: SMS OTP may not satisfy 8.4.3; acceptable = FIDO2, TOTP/HOTP, hardware token, push with device binding | 2026-05-20 |
| ASSUME-8-002 | Req 8 | Service account "changed periodically": annual rotation or automated rotation ≤ 90 days via secrets management | 2026-05-20 |
| ASSUME-9-001 | Req 9 | Facility entry controls: authorized list quarterly; events logged with identity/timestamp; logs reviewed monthly | 2026-05-20 |
| ASSUME-9-002 | Req 9 | POI inspection: high-risk unattended ≤ monthly; attended indoor ≤ quarterly; records document device ID, inspector, date | 2026-05-20 |
| ASSUME-10-001 | Req 10 | Non-critical log review "periodically": weekly minimum; monthly acceptable for very low-risk systems with justification | 2026-05-20 |
| ASSUME-10-002 | Req 10 | Critical control failure "promptly": alert ≤ 15 min; incident ticket ≤ 1 hour; remediation or compensating control ≤ 4 hours | 2026-05-20 |
| ASSUME-11-001 | Req 11 | Pentest scope adequate: CDE network + application layer (OWASP Top 10); segmentation validation; qualified = OSCP/CEH/GPEN or documented equivalent | 2026-05-20 |
| ASSUME-12-001 | Req 12 | IRP adequate: defined roles; escalation procedures; containment/recovery; card brand procedures; forensic preservation; tested annually | 2026-05-20 |

---

## Contested items pending resolution

*(None — PCI DSS v4.0 defined approach has no contested items. Customized approach requirements are flagged as CONTESTED per implementation; see CI/CD gate configuration.)*

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Vulnerability scanning | PCI DSS Req 11, SOC 2 CC7.1, ISO 27001 A.8.8, NIST 800-53 RA-5 | Quarterly ASV scan for PCI; SOC 2/ISO have audit-defined frequency. A single scan program satisfies all if frequency ≥ quarterly |
| Penetration testing | PCI DSS Req 11.4, SOC 2 CC7 (points of focus), ISO 27001 A.8.29 | PCI requires annual with specific scope; other frameworks are less prescriptive |
| Access control records | PCI DSS Req 7–8, HIPAA §164.312(a), SOC 2 CC6, NIST 800-53 AC | IAM system evidence reused across all; PCI has the tightest DETERMINISTIC thresholds |
| Audit logs | PCI DSS Req 10, HIPAA §164.312(b), SOC 2 CC7, NIST 800-53 AU | PCI 12-month / 3-month-immediate retention is the most specific; design to PCI to satisfy others |
| Encryption in transit | PCI DSS Req 4, HIPAA §164.312(e), NIST 800-53 SC-8, ISO 27001 A.8.24 | TLS 1.2+ satisfies all frameworks |
| Patch management | PCI DSS Req 6.3.3 (1-month critical SLA), HIPAA SI, NIST 800-53 SI-2 | PCI has the tightest critical patch SLA; design to PCI satisfies others |

---

## CI/CD gate configuration

Standard three-tier gate (see NERC CIP registry). PCI-specific constraints:

- **CDE scope fixture:** All tests are gated by `in_cde()` or `connected_to_cde()` fixture. Scope changes require re-review.
- **SAQ filter:** Tests not applicable to the entity's SAQ type run in informational mode.
- **Customized approach flag:** Any requirement using customized implementation is demoted to Pattern 3 automatically; QSA sign-off required before test is enforcing.
- **Date-bounded tests:** All time-threshold tests (quarterly scans, annual pentest, 6-month access reviews) emit Pattern 2 failures when the deadline is within 30 days of expiry.

---

## Requirement file status

| Requirement | File | Status | Assumptions | Confidence |
|---|---|---|---|---|
| Req 1 — Network Security Controls | `req-01-network-security.md` | ✅ Parsed | ASSUME-1-001 | HIGH |
| Req 2 — Secure Configurations | `req-02-secure-config.md` | ✅ Parsed | ASSUME-2-001 | HIGH |
| Req 3 — Stored Account Data | `req-03-stored-account-data.md` | ✅ Parsed | ASSUME-3-001, ASSUME-3-002 | HIGH |
| Req 4 — Transmission Security | `req-04-transmission-security.md` | ✅ Parsed | ASSUME-4-001 | HIGH |
| Req 5 — Malware Protection | `req-05-malware-protection.md` | ✅ Parsed | ASSUME-5-001, ASSUME-5-002 | HIGH |
| Req 6 — Secure Systems and Software | `req-06-secure-systems.md` | ✅ Parsed | ASSUME-6-001, ASSUME-6-002 | MEDIUM |
| Req 7 — Restrict Access | `req-07-restrict-access.md` | ✅ Parsed | ASSUME-7-001 | HIGH |
| Req 8 — Authentication | `req-08-authentication.md` | ✅ Parsed | ASSUME-8-001, ASSUME-8-002 | HIGH |
| Req 9 — Physical Access | `req-09-physical-access.md` | ✅ Parsed | ASSUME-9-001, ASSUME-9-002 | MEDIUM |
| Req 10 — Logging | `req-10-logging.md` | ✅ Parsed | ASSUME-10-001, ASSUME-10-002 | HIGH |
| Req 11 — Security Testing | `req-11-security-testing.md` | ✅ Parsed | ASSUME-11-001 | HIGH |
| Req 12 — Policies and Programs | `req-12-policies.md` | ✅ Parsed | ASSUME-12-001 | MEDIUM |
