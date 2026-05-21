# GLBA / FTC Safeguards Rule — Gramm-Leach-Bliley Act

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Financial Privacy Rule (16 CFR Part 313) + Safeguards Rule (16 CFR Part 314, revised June 2023)
**Authority:** Federal Trade Commission (FTC) for non-bank financial institutions; parallel rules enforced by OCC, FDIC, Federal Reserve, NCUA for their regulated institutions (FFIEC context)
**Enforcing context:** "Financial institutions" under FTC jurisdiction: mortgage brokers, payday lenders, auto dealers, tax preparers, financial planners, investment advisors, insurance companies, fintechs, credit reporting agencies — any non-bank entity "significantly engaged" in providing financial products/services
**Note:** Banks, credit unions, and bank holding companies are subject to parallel Interagency Guidelines (enforced by OCC/FDIC/Fed/NCUA) rather than the FTC Safeguards Rule, but the substantive requirements are nearly identical. See FFIEC registry for bank-specific examination framework.

---

## Summary

| Metric | Count |
|---|---|
| Rules covered | 2 (Privacy Rule + Safeguards Rule) |
| Safeguards Rule sections | ~20 substantive requirements |
| Requirements parsed (individual files) | 0 (index only; individual section files pending) |
| Fully automated (DETERMINISTIC) | Moderate — MFA, encryption, penetration testing cadence, board reporting |
| Partial automation (PARAMETERIZED) | Dominant — risk assessment methodology, safeguard adequacy |
| Human-determination required (CONTESTED) | Moderate — "qualified individual" determination, program adequacy |
| Open assumptions | 0 |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Small company exemption — critical pre-condition

Companies with fewer than **5,000 customer records** are exempt from the following Safeguards Rule requirements:
- Annual penetration testing (§314.4(g)(1))
- Vulnerability scanning (§314.4(g)(2))
- Audit log requirements (§314.4(h))

All other Safeguards Rule requirements apply regardless of size. Exemption status is a DETERMINISTIC pre-condition filter on applicable tests.

---

## Privacy Rule (16 CFR Part 313) — confidence map

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| §313.4 | Initial privacy notice | PARAMETERIZED | Notice content adequacy (must include all 9 disclosure elements) |
| §313.5 | Annual privacy notice | DETERMINISTIC | Annual notice required (or exception: no opt-out + no policy changes) |
| §313.6 | Opt-out notice requirements | PARAMETERIZED | Notice clarity and opt-out mechanism adequacy |
| §313.7 | Form of opt-out notice | PARAMETERIZED | Reasonable means to opt out |
| §313.10 | Limits on disclosure | DETERMINISTIC | Cannot share NPI with non-affiliated third parties without opt-out notice + opportunity |
| §313.13 | Limits on reuse/redisclosure | DETERMINISTIC | Recipients of NPI bound by same restrictions |

---

## Safeguards Rule (16 CFR Part 314) — confidence map

### Written Information Security Program (WISP) — §314.3

All covered entities must implement a comprehensive WISP that is appropriate to size and complexity, nature and scope of activities, and sensitivity of customer information.

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| §314.3 | Written WISP required | DETERMINISTIC | Existence of written program is binary |

### Qualified Individual — §314.4(a)

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| §314.4(a) | Designated qualified individual (QI) | DETERMINISTIC | Named individual (or service provider) must be designated as responsible for WISP |
| §314.4(a) | QI qualification | PARAMETERIZED | "Qualified" is not defined; expertise must be sufficient for the program |

### Risk Assessment — §314.4(b)

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| §314.4(b) | Written risk assessment | DETERMINISTIC | Written document must exist |
| §314.4(b)(1) | Criteria for risk evaluation and categorization | PARAMETERIZED | Methodology is org-defined |
| §314.4(b)(2) | Criteria for risk mitigation | PARAMETERIZED | Adequacy of selected safeguards |
| §314.4(b)(3) | Frequency of reassessment | PARAMETERIZED | "Periodically and whenever a material change" — org-defined cadence |

### Safeguards Implementation — §314.4(c)

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| §314.4(c)(1) | Access controls | MEDIUM | Least privilege, MFA for remote access and privileged accounts |
| §314.4(c)(2) | Data inventory | PARAMETERIZED | Identify/classify customer information — completeness criteria |
| §314.4(c)(3) | Encryption | DETERMINISTIC | Customer information must be encrypted in transit AND at rest |
| §314.4(c)(4) | Secure development practices | PARAMETERIZED | SDL adequacy |
| §314.4(c)(5) | Multi-factor authentication | DETERMINISTIC | MFA required for any employee accessing customer information; may use equivalent controls with approval |
| §314.4(c)(6) | Disposal of customer information | PARAMETERIZED | Secure disposal method |
| §314.4(c)(7) | Change management | PARAMETERIZED | Anticipate and evaluate security of changes to operations or business arrangements |
| §314.4(c)(8) | Monitoring and testing | DETERMINISTIC | Continuous monitoring or annual penetration testing + bi-annual vulnerability scanning |

### Penetration Testing and Vulnerability Assessment — §314.4(g)

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| §314.4(g)(1) | Annual penetration test | DETERMINISTIC | Annual pentest required (> 5,000 records only) |
| §314.4(g)(2) | Bi-annual vulnerability scan | DETERMINISTIC | Every 6 months + after material change (> 5,000 records only) |

### Audit Log Requirements — §314.4(h)

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| §314.4(h) | Audit logging | DETERMINISTIC | Monitor and filter audit logs (> 5,000 records only); log must capture activity on systems storing customer information |

### Training — §314.4(d)

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| §314.4(d) | Security awareness training | PARAMETERIZED | Annual training required; content adequacy is PARAMETERIZED |

### Service Provider Oversight — §314.4(f)

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| §314.4(f)(1) | Service provider selection | PARAMETERIZED | Due diligence on service providers with access to customer information |
| §314.4(f)(2) | Service provider contracts | PARAMETERIZED | Contracts must require appropriate safeguards; content adequacy |

### Incident Response Plan — §314.4(i)

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| §314.4(i) | Written incident response plan | DETERMINISTIC | Plan must exist; must address the 8 elements listed in the rule |
| §314.4(i)(1)–(8) | IRP required elements | PARAMETERIZED | 8 elements: goals, internal processes, roles, communications, remediation, documentation, review, notification |

### Board Reporting — §314.4(k)

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| §314.4(k) | Annual report to Board or senior officer | DETERMINISTIC | Annual written report to board (or senior officer if no board) covering WISP status, material risks, safeguard changes, recommendations |

---

## Key DETERMINISTIC thresholds

| Requirement | Threshold | Section |
|---|---|---|
| Encryption in transit | Required for all customer information in transit | §314.4(c)(3) |
| Encryption at rest | Required for all customer information at rest | §314.4(c)(3) |
| MFA | Required for all employees accessing customer information | §314.4(c)(5) |
| Annual penetration test | Required annually (> 5,000 records) | §314.4(g)(1) |
| Vulnerability scanning | Bi-annual (> 5,000 records) | §314.4(g)(2) |
| Annual WISP review | Must be reviewed and updated at least annually | §314.4(j) |
| Annual board report | Annual written report required | §314.4(k) |
| Privacy notice | Annual notice or exception applies | §313.5 |

---

## Open assumption registry

*(No assumptions recorded — individual section files not yet written)*

---

## Contested items pending resolution

*(None recorded yet)*

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Encryption at rest/in transit | GLBA §314.4(c)(3), PCI DSS Req 3–4, HIPAA §164.312 (addressable), NY DFS §500.15 | GLBA mandates encryption (unlike HIPAA which is addressable); align to PCI-grade to satisfy all |
| MFA | GLBA §314.4(c)(5), NY DFS §500.12, PCI DSS Req 8, NIST 800-53 IA | GLBA and NY DFS both mandate MFA; same technical implementation satisfies both |
| Penetration testing | GLBA §314.4(g)(1), NY DFS §500.05, PCI DSS Req 11.4, SOC 2 CC7 | Annual pentest scope and frequency overlap; a single engagement with correct scope satisfies all |
| Incident response plan | GLBA §314.4(i), NY DFS §500.16, HIPAA §164.308(a)(6), GDPR Art. 33 | IRP content elements differ; shared template with framework-specific annexes recommended |
| Service provider management | GLBA §314.4(f), GDPR Art. 28, ISO 27001 A.5.19, SOC 2 CC9.2 | Single vendor assessment and agreement template can satisfy all |
| Board/senior officer reporting | GLBA §314.4(k), NY DFS §500.04 (CISO report), SOX §302/404 | Annual security report to board; same document can satisfy multiple frameworks if it covers required content |
