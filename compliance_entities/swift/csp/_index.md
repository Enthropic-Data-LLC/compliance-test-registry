# SWIFT Customer Security Programme (CSP) — CSCF v2025

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** All SWIFT users (financial institutions, corporates, service bureaux) connecting to the SWIFT network; covers security controls protecting the local SWIFT infrastructure
**Authority:** SWIFT (Society for Worldwide Interbank Financial Telecommunication)
**Enforcing context:** Contractual obligation for all SWIFT connectivity; annual self-attestation mandatory; results shared with correspondents and regulators via KYC Security Attestation (KYC-SA) application
**Current version:** CSCF v2025 (Customer Security Controls Framework)

---

## Summary

| Metric | Count |
|---|---|
| Mandatory controls | 25 |
| Advisory controls | 6 |
| Control families | 3 (Secure your Environment / Know and Limit Access / Detect and Respond) |
| Sections parsed (individual files) | 3 (secure-environment-controls.md + access-credential-controls.md + detect-respond-controls.md) |
| Fully automated (DETERMINISTIC) | HIGH — 1.1, 1.2, 2.1, 2.3A, 2.7A, 3.1, 3.2, 4.1, 4.4, 5.1, 5.2, 6.2, 6.3, 6.4, 7.1, 7.3A, attestation gate |
| Partial automation (PARAMETERIZED) | MEDIUM — 1.3, 2.2, 2.5A, 3.3, 4.2, 4.3A, 5.3A, 6.1 |
| Human-determination required (CONTESTED) | Low |
| Open assumptions | 10 (ASSUME-SWIFT-1_3-001, 2_2-001, 2_5A-001, 3_3-001, 4_2-001, 4_3A-001, 5_3A-001, 6_1-001, plus 2 pending attestation) |

---

## Scoping pre-condition

```python
def is_swift_user() -> bool:
    """
    True if the organization has a SWIFT BIC and connects to the SWIFT network
    via any connectivity type (A1, A2, A3, A4, B).
    Source: SWIFT connectivity agreement + BIC registration.
    """
```

All CSCF controls are enforcing only when `is_swift_user()` returns True.

---

## CSCF architecture — 3 principles, 3 objectives

| Principle | Objective | Focus |
|---|---|---|
| Secure your Environment | 1. Restrict Internet Access | Mandatory network isolation |
| | 2. Segregate Critical Systems | Secure Zone architecture |
| Know and Limit Access | 3. Prevent Compromise of Credentials | MFA, privilege management |
| | 4. Manage Identities and Segregate Privileges | IAM controls |
| Detect and Respond | 5. Detect Anomalous Activity | Logging, anomaly detection |
| | 6. Plan for Incident Response and Information Sharing | IR, SWIFT ISACs |

---

## Per-control confidence map (mandatory controls only)

### Objective 1 — Restrict Internet Access

| Control | ID | Confidence | Notes |
|---|---|---|---|
| SWIFT environment protection | 1.1 | DETERMINISTIC | Mandatory Secure Zone isolation; no direct internet routing |
| Security updates | 1.2 | DETERMINISTIC | Patching within 3 months of release for critical; 6 months for other |
| Virtualisation platform security | 1.3 | PARAMETERIZED | Hardening per vendor guidelines |

### Objective 2 — Segregate Critical Systems

| Control | ID | Confidence | Notes |
|---|---|---|---|
| Operator PC security | 2.1 | DETERMINISTIC | Dedicated operator PCs; no general internet browsing |
| Internal data flow security | 2.2 | PARAMETERIZED | Traffic filtering between zones documented |
| Security updates (operator PC) | 2.3A | DETERMINISTIC | Same 3-month/6-month patching cadence as 1.2 |
| Back-office data flow security | 2.5A | PARAMETERIZED | Firewall-enforced data flow documentation |
| Vulnerability scanning | 2.7A | DETERMINISTIC | Internal vulnerability scanning at least quarterly |

### Objective 3 — Prevent Compromise of Credentials

| Control | ID | Confidence | Notes |
|---|---|---|---|
| Password policy | 3.1 | DETERMINISTIC | Min length, complexity, rotation — SWIFT specifies thresholds |
| Multi-factor authentication | 3.2 | DETERMINISTIC | MFA mandatory for all operators accessing SWIFT infrastructure |
| Physically secure environment | 3.3 | PARAMETERIZED | Physical access controls to Secure Zone |

### Objective 4 — Manage Identities and Segregate Privileges

| Control | ID | Confidence | Notes |
|---|---|---|---|
| Password storage and transmission | 4.1 | DETERMINISTIC | Passwords hashed or encrypted at rest/in-transit |
| Physical and logical password storage | 4.2 | PARAMETERIZED | Hardware token or equivalent for system accounts |
| Staff screening | 4.3A | PARAMETERIZED | Background check process documented |
| Token management | 4.4 | DETERMINISTIC | HSMs or equivalent for signing keys |
| Logical access control | 5.1 | DETERMINISTIC | Least-privilege; access reviewed at least annually |
| Session protection | 5.2 | DETERMINISTIC | Session termination after inactivity; encrypted sessions |
| Security roles | 5.3A | PARAMETERIZED | Separation of duties documented for SWIFT roles |

### Objective 5 — Detect Anomalous Activity

| Control | ID | Confidence | Notes |
|---|---|---|---|
| Intrusion detection | 6.1 | PARAMETERIZED | IDS/IPS or equivalent monitoring |
| Software integrity check | 6.2 | DETERMINISTIC | File integrity monitoring on SWIFT components |
| Database integrity | 6.3 | DETERMINISTIC | DB activity monitoring for critical SWIFT databases |
| Log preservation | 6.4 | DETERMINISTIC | 12-month minimum retention for SWIFT transaction logs |
| Cyber incident response planning | 7.1 | DETERMINISTIC | Written IR plan addressing SWIFT-specific scenarios |
| Penetration testing | 7.3A | DETERMINISTIC | Annual penetration test of SWIFT infrastructure |

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Control |
|---|---|---|
| Critical patch application | Within 3 months of release | 1.2, 2.3A |
| Other patch application | Within 6 months of release | 1.2, 2.3A |
| Vulnerability scanning | Quarterly (minimum) | 2.7A |
| SWIFT transaction log retention | 12 months minimum | 6.4 |
| Annual penetration test | Once per calendar year | 7.3A |
| Access review | At least annually | 5.1 |
| Annual self-attestation | By end of calendar year | CSP Program |

---

## Annual attestation — DETERMINISTIC gate

SWIFT users must complete and submit the annual self-attestation via the KYC-SA application by the program deadline (typically December 31 of the attestation year).

| Attestation element | Status | Confidence |
|---|---|---|
| All mandatory controls attested | Pass/Fail binary | DETERMINISTIC |
| Attestation submitted before deadline | Calendar date gate | DETERMINISTIC |
| Independent assessment (recommended) | Engagement record | PARAMETERIZED |
| Correspondent access to attestation results | Published via KYC-SA | DETERMINISTIC |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| MFA enforcement | SWIFT CSP 3.2, NIST 800-53 IA-2, PCI DSS Req 8, NYDFS §500.12 | Same MFA infrastructure |
| Vulnerability scanning program | SWIFT CSP 2.7A, PCI DSS Req 11, NIST 800-53 RA-5, DORA Art. 25 | Same scanner + schedule |
| Penetration testing | SWIFT CSP 7.3A, PCI DSS Req 11.4, DORA Art. 26 | Same pentest engagement |
| Log retention | SWIFT CSP 6.4, NYDFS §500.06, SOX ITGC, GLBA Safeguards | 12-month SWIFT < 6-year NYDFS — NYDFS controls |
| Incident response plan | SWIFT CSP 7.1, NIST 800-53 IR-8, DORA Art. 18, FFIEC BCP | Single IR plan with SWIFT-specific annex |
