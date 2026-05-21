# PCI DSS v4.0

**Authority:** PCI Security Standards Council (PCI SSC); enforced contractually by card brands (Visa, Mastercard, Amex, Discover, JCB)
**Scope:** Any entity that stores, processes, or transmits cardholder data (CHD) or sensitive authentication data (SAD); applies to merchants, service providers, and their technology environments

This directory contains the RDF registry for PCI DSS v4.0, decomposed across all 12 Requirements with YAML specs and Python test stubs.

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — 285 requirements mapped, confidence map, open assumptions | ✅ |
| [`req-01-network-security.md`](./req-01-network-security.md) | Req 1 — Network security controls (firewall rules, DMZ, deny-all) | ✅ |
| [`req-02-secure-config.md`](./req-02-secure-config.md) | Req 2 — Secure configurations (default passwords, unnecessary services) | ✅ |
| [`req-03-stored-account-data.md`](./req-03-stored-account-data.md) | Req 3 — Stored account data (PAN masking, truncation, SAD prohibition) | ✅ |
| [`req-04-transmission-security.md`](./req-04-transmission-security.md) | Req 4 — Transmission security (TLS 1.2+, prohibited protocols) | ✅ |
| [`req-05-malware-protection.md`](./req-05-malware-protection.md) | Req 5 — Anti-malware (AV on all systems, scan frequency) | ✅ |
| [`req-06-secure-systems.md`](./req-06-secure-systems.md) | Req 6 — Secure systems and software (patching, OWASP Top 10, SDLC) | ✅ |
| [`req-07-restrict-access.md`](./req-07-restrict-access.md) | Req 7 — Restrict access by business need (least privilege, role-based) | ✅ |
| [`req-08-authentication.md`](./req-08-authentication.md) | Req 8 — User identification and authentication (MFA, password policy, shared accounts) | ✅ |
| [`req-09-physical-access.md`](./req-09-physical-access.md) | Req 9 — Physical access controls (visitor logs, media destruction) | ✅ |
| [`req-10-logging.md`](./req-10-logging.md) | Req 10 — Log and monitor all access (audit logs, SIEM, 12-month retention) | ✅ |
| [`req-11-security-testing.md`](./req-11-security-testing.md) | Req 11 — Security testing (quarterly scans, annual penetration test, rogue AP detection) | ✅ |
| [`req-12-policies.md`](./req-12-policies.md) | Req 12 — Policies and programs (annual risk assessment, third-party compliance, incident response) | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Requirement |
|---|---|---|
| Vulnerability scan (ASV) | Quarterly | Req 11.3.2 |
| Internal vulnerability scan | Quarterly; after significant changes | Req 11.3.1 |
| Penetration test — external | At least annually; after significant changes | Req 11.4.3 |
| Penetration test — internal | At least annually | Req 11.4.4 |
| Rogue AP detection | Quarterly physical or automated ongoing | Req 11.2.1 |
| PAN display masking | Maximum 6 digits first / 4 digits last | Req 3.3.1 |
| Audit log retention | 12 months total; 3 months immediately available | Req 10.7 |
| Annual risk assessment | At least once per year | Req 12.3.1 |
| Incident response plan test | At least annually | Req 12.10.2 |

## Parse status: Deep — all 12 Requirements parsed
