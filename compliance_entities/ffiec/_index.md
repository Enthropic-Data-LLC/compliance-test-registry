# FFIEC IT Examination Handbooks

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** FFIEC IT Examination Handbook series — the authoritative examination framework for IT and cybersecurity at federally regulated U.S. financial institutions
**Authority:** Federal Financial Institutions Examination Council (FFIEC) — joint body of OCC, FDIC, Federal Reserve, NCUA, CFPB, and State Liaison Committee
**Enforcing context:** Banks, credit unions, savings associations, and their service providers (TSPs) subject to federal examination by FFIEC member agencies. Examiners use these handbooks as the basis for IT safety-and-soundness examinations.
**Note:** FFIEC handbooks are examination guidance, not regulations. However, findings result in MRAs (Matters Requiring Attention) and MRIAs (Matters Requiring Immediate Attention) that carry the practical force of law. Non-remediation leads to enforcement actions.

---

## Summary

| Metric | Count |
|---|---|
| Active handbooks | 12 |
| Examination domains | 6 core (Information Security, Management, Development and Acquisition, Operations, Business Continuity, Audit) + specialized (Retail Payments, Wholesale Payments, E-Banking, etc.) |
| Controls parsed (individual files) | 1 (information-security-examination.md — IS governance, risk assessment, access controls, patch management, vuln scanning, pentest, logging, IRP, TSP management, BCP) |
| Fully automated (DETERMINISTIC) | Moderate — patch cadence, log retention, MFA presence, BCP test frequency |
| Partial automation (PARAMETERIZED) | Dominant — "adequate," "appropriate," "commensurate with risk" appear throughout |
| Human-determination required (CONTESTED) | Significant — examiner judgment is central to the framework |
| Open assumptions | 0 |

| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Handbook inventory

| Handbook | Version | Primary scope |
|---|---|---|
| **Information Security** | 2016 (updated 2019) | The primary cybersecurity handbook; highest exam frequency |
| **Management** | 2015 | IT governance, strategic planning, risk management, vendor management |
| **Development and Acquisition** | 2012 (being updated) | SDLC, project management, software acquisition |
| **Operations** | 2004 (being updated) | Computer operations, production management, capacity planning |
| **Business Continuity Management** | 2019 | BCP/DRP, resilience, testing |
| **Audit** | 2003 (being updated) | IT audit function, independence, coverage |
| **Retail Payment Systems** | 2016 | ACH, card payments, check processing |
| **Wholesale Payment Systems** | 2012 | Wire transfer, Fedwire, CHIPS |
| **E-Banking** | 2003 (outdated; superseded by IS handbook in practice) | Internet banking, authentication |
| **Supervision of Technology Service Providers (TSP)** | 2012 | Third-party IT service providers |
| **Architecture, Infrastructure, and Operations (AIO)** | 2024 (new) | Replaces Operations handbook; cloud, virtualization, modern infrastructure |
| **Cybersecurity Assessment Tool (CAT)** | 2015 (supplemental) | Self-assessment mapping to NIST CSF; not a handbook but widely used |

---

## Information Security Handbook — per-domain confidence map

The Information Security handbook is the primary exam vehicle. It covers five work program areas:

### 1. Information Security Program Governance

| Control | Confidence | Notes |
|---|---|---|
| Board/senior management oversight | PARAMETERIZED | Board approves IS program and receives regular reports; frequency is org-defined (at least annual) |
| Written IS policy | DETERMINISTIC | Written policy must exist; last review date tracked |
| Risk management integration | PARAMETERIZED | IS risk integrated into enterprise risk management |
| IS roles and responsibilities | PARAMETERIZED | CISO or equivalent; reporting structure |
| IS program scope | PARAMETERIZED | All systems, networks, and data processing |

### 2. Information Security Risk Assessment

| Control | Confidence | Notes |
|---|---|---|
| Written risk assessment | DETERMINISTIC | Written document must exist |
| Threat and vulnerability identification | PARAMETERIZED | Methodology adequacy |
| Risk measurement | PARAMETERIZED | Likelihood and impact assessment method |
| Periodic update | PARAMETERIZED | "Regularly" and upon significant change — org-defined interval |

### 3. Information Security Controls

| Control | Confidence | Notes |
|---|---|---|
| Access control — unique IDs | DETERMINISTIC | No shared accounts for privileged access |
| Multi-factor authentication | DETERMINISTIC | Required for remote access; internet-facing systems; privileged accounts |
| Patch management | MEDIUM | Critical patches within defined SLA (examiner looks for ≤ 30 days for critical) |
| Encryption in transit | DETERMINISTIC | Sensitive data in transit must be encrypted; TLS version verified |
| Encryption at rest | PARAMETERIZED | Required for sensitive data; method must be appropriate |
| Logging and monitoring | MEDIUM | Logs retained "adequate" period (examiner benchmark: 12 months online, 2 years total) |
| Antimalware | DETERMINISTIC | Deployed on all applicable systems; definitions current |
| Vulnerability scanning | DETERMINISTIC | Internal and external scans on defined frequency; examiners expect ≥ quarterly |
| Penetration testing | DETERMINISTIC | Annual penetration test (internal and external); scope includes network and applications |
| Incident response | PARAMETERIZED | Written IRP; tested annually; examiners expect tabletop at minimum |

### 4. Security Monitoring and Testing

| Control | Confidence | Notes |
|---|---|---|
| Security event monitoring | PARAMETERIZED | 24/7 or SLA-covered monitoring; coverage scope |
| Log review | PARAMETERIZED | Automated or manual log review process; frequency |
| Penetration test results remediation | PARAMETERIZED | Findings remediated within defined SLA |
| Vulnerability remediation | MEDIUM | Critical findings remediated within 30 days (examiner expectation) |

### 5. Third-Party/Vendor Management (Technology Service Providers)

| Control | Confidence | Notes |
|---|---|---|
| TSP due diligence | PARAMETERIZED | Risk-based due diligence before contracting |
| TSP contracts | PARAMETERIZED | Contracts include security requirements, audit rights, incident notification, BCP |
| TSP ongoing monitoring | PARAMETERIZED | Annual review of SOC 2 reports or equivalent |
| TSP inventory | DETERMINISTIC | Written inventory of all TSPs with access to systems/data |
| Concentration risk | PARAMETERIZED | Dependency on single TSP for critical functions |

---

## Business Continuity Management Handbook — per-domain confidence map

| Domain | Control | Confidence | Notes |
|---|---|---|---|
| BCP governance | Board approval of BCP | DETERMINISTIC | Board-approved BCP required |
| Business impact analysis | Written BIA | DETERMINISTIC | Written BIA must exist; updated annually or after significant change |
| BCP content | Recovery strategies for critical business functions | PARAMETERIZED | Adequacy of recovery strategies |
| RTO/RPO | Defined and achievable RTO/RPO | DETERMINISTIC | Objectives must be documented; achieved in testing |
| Testing | Annual BCP test | DETERMINISTIC | At least annual; examiners expect full test (failover or tabletop + component tests) |
| Testing | Test documentation | DETERMINISTIC | Written test results and remediation plans |
| Crisis communications | Internal and external communication plan | PARAMETERIZED | Plan completeness |
| Data backup | Offsite backup | DETERMINISTIC | Offsite (geographically separate) backup required for critical data |

---

## Cybersecurity Assessment Tool (CAT)

The CAT maps inherent risk profile (5 levels) to cybersecurity maturity (5 levels across 5 domains). Examiners use it as a discussion framework but it is not a checklist.

| Inherent risk tier | Description |
|---|---|
| Least | Simple IT environment; minimal online banking; no critical infrastructure |
| Minimal | Basic online banking; standard payment processing |
| Moderate | Multiple channels; growing complexity |
| Significant | Large institution; complex interconnections; critical infrastructure |
| Most | Systemically important; global operations |

Maturity levels: Baseline → Evolving → Intermediate → Advanced → Innovative

**RDF treatment:** CAT is primarily a Pattern 3 framework — maturity levels are CONTESTED (examiner-determined). Individual controls within each domain have DETERMINISTIC and PARAMETERIZED components that can be extracted independently.

---

## Examiner-expected benchmarks (de facto DETERMINISTIC thresholds)

While the FFIEC handbooks rarely state bright-line numbers, experienced examiners apply consistent expectations. These function as PARAMETERIZED assumptions:

| Control | Examiner benchmark | Source |
|---|---|---|
| Critical patch remediation | ≤ 30 days | Information Security handbook practice |
| Vulnerability scan frequency | At least quarterly (internal); quarterly external ASV | Information Security handbook |
| Penetration test | At least annual; scope: network + application layers | Information Security handbook |
| Log retention | 12 months immediately accessible; 2 years total | Information Security handbook |
| BCP test | Annual full test (failover or tabletop) | BCM handbook |
| Risk assessment update | At least annual or upon material change | Information Security handbook |
| Vendor SOC 2 review | Annual; critical vendors reviewed by qualified staff | TSP handbook |

---

## Open assumption registry

*(No assumptions recorded — individual handbook section files not yet written)*

---

## Contested items pending resolution

| ID | Area | Issue | Status |
|---|---|---|---|
| CONTEST-FFIEC-001 | CAT maturity | Maturity level determination is examiner-dependent and institution-negotiated; no bright-line threshold | Pattern 3 gate; requires Compliance Officer/CIO attestation |
| CONTEST-FFIEC-002 | IS program adequacy | "Commensurate with risk" standard is examiner-evaluated; no audit checklist | Pattern 3 gate |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Penetration testing | FFIEC IS, NY DFS §500.05, GLBA §314.4(g), PCI DSS Req 11.4 | Single annual pentest satisfies all four if scope is correct |
| Patch management | FFIEC IS (30-day examiner benchmark), PCI DSS Req 6 (30-day critical), NIST 800-53 SI-2 | Align to PCI DSS 30-day critical threshold to satisfy FFIEC expectation and PCI requirement |
| BCP/DRP | FFIEC BCM, DORA Art. 11–12, SOC 2 A1, NIST 800-53 CP | Annual test with documented RTO/RPO satisfies all |
| Vendor management | FFIEC TSP handbook, GLBA §314.4(f), DORA Art. 28–30, SOC 2 CC9.2 | Single vendor management program; DORA Art. 30(2) has the most specific contract requirements |
| MFA | FFIEC IS, NY DFS §500.12, GLBA §314.4(c)(5), PCI DSS Req 8 | All require MFA for remote access and privileged accounts; same technical implementation |
| Log retention | FFIEC (12mo/2yr benchmark), NY DFS §500.06 (6 years), PCI DSS Req 10 (12mo/3mo-immediate) | NY DFS 6-year is the binding requirement for dual-regulated entities; FFIEC 12-month is an examiner expectation only |
