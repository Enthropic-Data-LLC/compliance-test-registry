# TSA Pipeline Cybersecurity Directives — SD-02D and SD-01C

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Critical pipeline (hazardous liquid and natural gas) and LNG facility operators designated by TSA as critical; highway and motor carrier cybersecurity directives also in effect (separate)
**Authority:** Transportation Security Administration (TSA) / DHS; issued under 49 U.S.C. §114(l)(2)
**Enforcing context:** TSA-designated critical pipeline/LNG operators (specific companies notified by TSA — list not public); SD-02D supersedes SD-02C (Oct 2023); SD-01C covers reporting
**Current directive:** SD-02D (October 2023 — performance-based approach) + SD-01C (reporting)

---

## Summary

| Metric | Count |
|---|---|
| Key cybersecurity performance goals | 4 |
| SD-01C reporting categories | 2 (immediate + 24-hour) |
| Core required plans | 3 (Cybersecurity Implementation Plan / Incident Response Plan / Recovery Plan) |
| Sections parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | Moderate — reporting timelines, plan currency, testing frequency |
| Partial automation (PARAMETERIZED) | Dominant — architecture, segmentation design, access control model |
| Human-determination required (CONTESTED) | Low-Moderate — "significant" incident determination |
| Open assumptions | 0 |

---

## Scoping pre-condition

```python
def is_tsa_designated_critical_pipeline() -> bool:
    """
    True if operator has received TSA written designation as critical pipeline facility.
    TSA uses risk criteria including throughput, geographic significance, interconnectedness.
    Not all pipeline operators are designated — only those specifically notified by TSA.
    """
```

---

## SD-02D — 4 cybersecurity performance goals

SD-02D is performance-based (vs. prescriptive SD-02A). Operators demonstrate achieving outcomes rather than implementing specific controls.

### Goal 1: Identify and detect cybersecurity threats

| Requirement | Confidence | Notes |
|---|---|---|
| Asset inventory (OT + IT) | DETERMINISTIC | Documented inventory of IT/OT systems |
| Vulnerability management program | PARAMETERIZED | Regular vulnerability identification and remediation |
| Network monitoring | PARAMETERIZED | Monitoring for anomalous/unauthorized activity |
| Threat intelligence sharing with CISA | PARAMETERIZED | Participation in information sharing |

### Goal 2: Protect against cybersecurity threats

| Requirement | Confidence | Notes |
|---|---|---|
| Network segmentation (OT/IT separation) | DETERMINISTIC | OT networks segmented from IT; documented architecture |
| Access control — least privilege | PARAMETERIZED | Minimum necessary access; privileged account management |
| MFA for remote access to OT systems | DETERMINISTIC | MFA required for remote access to OT/ICS environments |
| Patch and vulnerability remediation | PARAMETERIZED | Risk-based patching timeline |
| Configuration management | PARAMETERIZED | Baseline configurations; change management |

### Goal 3: Respond to and recover from cybersecurity incidents

| Requirement | Confidence | Notes |
|---|---|---|
| Cybersecurity Incident Response Plan | DETERMINISTIC | Written, tested plan — must exist and be current |
| Cybersecurity Recovery Plan | DETERMINISTIC | Written, tested recovery plan — must exist and be current |
| Plan testing — tabletop or exercise | DETERMINISTIC | Annual testing of IRP and Recovery Plan |
| Unaffected backup OT networks/systems | PARAMETERIZED | Backup capability to maintain safe operations |

### Goal 4: Cybersecurity governance

| Requirement | Confidence | Notes |
|---|---|---|
| Cybersecurity Implementation Plan (CIP) | DETERMINISTIC | Submitted to TSA; describes how goals are achieved |
| TSA review and approval | DETERMINISTIC | CIP must be TSA-approved |
| Annual reporting to TSA | DETERMINISTIC | Annual cybersecurity assessment to TSA |
| Senior official designation | DETERMINISTIC | Named Cybersecurity Coordinator (available 24/7) |

---

## SD-01C — Incident reporting (DETERMINISTIC deadlines)

| Incident type | Deadline | Report to |
|---|---|---|
| Cybersecurity incident affecting operational systems | Within 24 hours of identification | CISA (via CISA.gov/reporting or 888-282-0870) |
| All cybersecurity incidents | Within 24 hours | TSA (via designated contact) |
| Immediate notification — confirmed attack on critical systems | Immediately | TSA + CISA |

**Definition of reportable incident:** Unauthorized access to IT/OT systems; malware on OT systems; denial of service affecting pipeline operations; ransomware attack; any incident causing operational disruption.

---

## Cybersecurity Implementation Plan — required contents (DETERMINISTIC checklist)

The CIP submitted to TSA must address:
1. Current state description of OT/IT architecture
2. How each of the 4 performance goals is achieved
3. Gap analysis against performance goals
4. Remediation timeline for gaps
5. Network segmentation documentation
6. Access control architecture
7. Incident response and recovery plan summaries
8. Testing schedule

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Source |
|---|---|---|
| OT/IT network segmentation | Required — architecture must enforce separation | SD-02D Goal 2 |
| MFA for remote OT access | Mandatory — no exceptions | SD-02D Goal 2 |
| Cybersecurity Coordinator availability | 24/7 availability | SD-02D Goal 4 |
| Annual plan testing | Once per year minimum | SD-02D Goal 3 |
| 24-hour incident report | Within 24 hours of identification | SD-01C |
| Cybersecurity Implementation Plan currency | Must be TSA-approved; updated as architecture changes | SD-02D Goal 4 |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| OT/ICS network segmentation | TSA SD-02D, NERC CIP-005, IEC 62443, NIST SP 800-82 | Same zone/conduit model; different regulatory mandates |
| Incident reporting | TSA SD-01C, CISA 6-hour reporting rule (CIRCIA), NERC CIP-008 | CIRCIA will unify reporting requirements post-rulemaking |
| Asset inventory | TSA SD-02D, NERC CIP-002, IEC 62443 | Same OT asset registry |
| Vulnerability management | TSA SD-02D, NERC CIP-007 R2, IEC 62443 | Same patch management program |
| Senior cybersecurity official | TSA Cybersecurity Coordinator, NYDFS §500.04 CISO | Different title; same function |
