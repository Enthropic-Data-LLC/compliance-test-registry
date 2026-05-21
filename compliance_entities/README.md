# Compliance Entities Registry

This directory contains one subdirectory per regulatory framework. Each entry is an independent registry built using the [Regulatory Decomposition Framework (RDF)](../guiding_docs/regulatory-decomposition-framework.md).

## How to navigate

Each framework directory contains:

| File | Purpose |
|---|---|
| `_index.md` | Registry index — confidence map, open assumptions, contested items, cross-standard dependencies |
| `*.md` spec files | Parsed requirements with YAML specs and Python test stubs |
| `README.md` | This navigation file |

## Frameworks by category

### Privacy and Data Protection
| Directory | Framework | Parse depth |
|---|---|---|
| [`gdpr/`](./gdpr/) | EU GDPR (General Data Protection Regulation) | Partial — core articles parsed |
| [`uk-gdpr/`](./uk-gdpr/) | UK GDPR + Data Protection Act 2018 | Index only |
| [`hipaa/`](./hipaa/) | HIPAA Security Rule (45 CFR Parts 164.308/310/312/314/316) | Deep — 5 spec files |
| [`ccpa-cpra/`](./ccpa-cpra/) | California CCPA / CPRA | Index only |
| [`pipeda/`](./pipeda/) | Canada PIPEDA / Privacy Act | Index only |
| [`lgpd/`](./lgpd/) | Brazil LGPD | Index only |
| [`appi/`](./appi/) | Japan APPI | Index only |
| [`coppa/`](./coppa/) | US COPPA (children's privacy) | Index only |

### Cybersecurity and Information Security
| Directory | Framework | Parse depth |
|---|---|---|
| [`iso/27001/`](./iso/27001/) | ISO/IEC 27001:2022 | Deep — 5 spec files (Annex A controls) |
| [`soc2/`](./soc2/) | SOC 2 Trust Services Criteria | Deep — 6 spec files |
| [`nist/sp800-171/`](./nist/sp800-171/) | NIST SP 800-171 Rev 2 (CUI protection) | Partial — 3 spec files |
| [`nist/sp800-53/`](./nist/sp800-53/) | NIST SP 800-53 Rev 5 | Index only |
| [`nist/csf2/`](./nist/csf2/) | NIST Cybersecurity Framework 2.0 | Index only |
| [`cmmc/`](./cmmc/) | CMMC 2.0 (DoD supply chain) | Partial — Level 1/2 practices parsed |
| [`fedramp/`](./fedramp/) | FedRAMP (US government cloud) | Partial — ConMon and overlays parsed |
| [`nydfs/500/`](./nydfs/500/) | NY DFS 23 NYCRR 500 | Index only |
| [`swift/csp/`](./swift/csp/) | SWIFT Customer Security Programme | Index only |
| [`tisax/`](./tisax/) | TISAX (automotive supply chain) | Index only |
| [`glba/`](./glba/) | GLBA / FTC Safeguards Rule | Index only |
| [`ffiec/`](./ffiec/) | FFIEC IT Examination Handbooks | Index only |

### Payment Card and Financial
| Directory | Framework | Parse depth |
|---|---|---|
| [`pci-dss/`](./pci-dss/) | PCI DSS v4.0 | Deep — 12 requirement spec files |
| [`sox/`](./sox/) | SOX IT General Controls | Index only |
| [`psd2/`](./psd2/) | EU PSD2 / Strong Customer Authentication | Index only |
| [`finra/`](./finra/) | FINRA broker-dealer rules | Index only |
| [`sec/cybersecurity/`](./sec/cybersecurity/) | SEC Cybersecurity Rules | Index only |
| [`basel/`](./basel/) | Basel III / BCBS 239 | Index only |

### Defense, Export Control, and Government
| Directory | Framework | Parse depth |
|---|---|---|
| [`itar-ear/`](./itar-ear/) | ITAR (22 CFR 120-130) + EAR (15 CFR 730-774) | Deep — 2 spec files (deterministic + parameterized) |
| [`fedramp/`](./fedramp/) | FedRAMP | Partial |
| [`cmmc/`](./cmmc/) | CMMC 2.0 | Partial |
| [`tsa/pipeline/`](./tsa/pipeline/) | TSA Pipeline Cybersecurity Directives | Index only |

### Energy and Critical Infrastructure
| Directory | Framework | Parse depth |
|---|---|---|
| [`nerc/ops/`](./nerc/ops/) | NERC Reliability Standards (non-CIP) | Deep — 5 spec files |
| [`nerc/cip/`](./nerc/cip/) | NERC CIP-002–CIP-015 | Parsed — CIP-002 through CIP-013 |
| [`nrc/10cfr50/`](./nrc/10cfr50/) | NRC 10 CFR Part 50 (nuclear power) | Deep — 3 spec files |
| [`nrc/10cfr73/`](./nrc/10cfr73/) | NRC 10 CFR Part 73 (nuclear security/cyber) | Index only |
| [`nist/sp800-82/`](./nist/sp800-82/) | NIST SP 800-82 (OT/ICS security) | Index only |

### Healthcare and Life Sciences
| Directory | Framework | Parse depth |
|---|---|---|
| [`fda/21cfr11/`](./fda/21cfr11/) | FDA 21 CFR Part 11 (electronic records) | Deep — 2 spec files |
| [`fda/21cfr210-211/`](./fda/21cfr210-211/) | FDA 21 CFR Parts 210/211 (GMP drug) | Index only |
| [`fda/fsma/`](./fda/fsma/) | FDA FSMA (food safety) | Index only |
| [`fda/qmsr/`](./fda/qmsr/) | FDA QMSR / 21 CFR Part 820 (medical devices) | Index only |
| [`iso/13485/`](./iso/13485/) | ISO 13485 (medical device QMS) | Index only |
| [`iso/14971/`](./iso/14971/) | ISO 14971 (medical device risk management) | Index only |
| [`iec/62304/`](./iec/62304/) | IEC 62304 (medical device software) | Index only |
| [`eu-mdr/`](./eu-mdr/) | EU MDR / IVDR (EU medical devices) | Index only |

### Quality Management and Manufacturing
| Directory | Framework | Parse depth |
|---|---|---|
| [`iso/9001/`](./iso/9001/) | ISO 9001:2015 | Index only |
| [`as9100/`](./as9100/) | AS9100 Rev D (aerospace QMS) | Index only |
| [`iatf/16949/`](./iatf/16949/) | IATF 16949 (automotive QMS) | Index only |
| [`nadcap/`](./nadcap/) | NADCAP (aerospace special processes) | Index only |
| [`iso/22000/`](./iso/22000/) | ISO 22000 (food safety management) | Index only |
| [`ipc/`](./ipc/) | IPC-A-610 / J-STD-001 (electronics assembly) | Index only |
| [`iso/45001/`](./iso/45001/) | ISO 45001 (occupational health and safety) | Index only |
| [`iso/50001/`](./iso/50001/) | ISO 50001 (energy management) | Index only |
| [`iso/14001/`](./iso/14001/) | ISO 14001 (environmental management) | Index only |

### Environmental
| Directory | Framework | Parse depth |
|---|---|---|
| [`epa/clean-air-act/`](./epa/clean-air-act/) | EPA Clean Air Act (CAA) | Index only |
| [`epa/npdes/`](./epa/npdes/) | EPA NPDES (water discharge permits) | Index only |
| [`epa/rcra/`](./epa/rcra/) | EPA RCRA (hazardous waste) | Index only |
| [`epa/rmp/`](./epa/rmp/) | EPA RMP (risk management programs) | Index only |
| [`epa/epcra/`](./epa/epcra/) | EPA EPCRA (emergency planning + community right-to-know) | Index only |
| [`rohs-reach/`](./rohs-reach/) | EU RoHS + REACH (chemical restrictions) | Index only |
| [`osha/1910/`](./osha/1910/) | OSHA 29 CFR 1910 (general industry) | Deep — 10 spec files |
| [`osha/1926/`](./osha/1926/) | OSHA 29 CFR 1926 (construction) | Partial — 3 spec files |

### International and Emerging
| Directory | Framework | Parse depth |
|---|---|---|
| [`eu-ai-act/`](./eu-ai-act/) | EU AI Act (Regulation 2024/1689) | Index only |
| [`nist/ai-rmf/`](./nist/ai-rmf/) | NIST AI Risk Management Framework | Index only |
| [`dora/`](./dora/) | EU DORA (digital operational resilience) | Index only |
| [`iec/62443/`](./iec/62443/) | IEC 62443 (OT/ICS security) | Index only |
| [`api/q1/`](./api/q1/) | API Q1/Q2 (oil and gas QMS) | Index only |
| [`wcag/`](./wcag/) | WCAG 2.2 / Section 508 (accessibility) | Index only |
