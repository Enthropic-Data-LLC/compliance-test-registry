# NRC 10 CFR 73.54 — Nuclear Power Reactor Cybersecurity

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Cybersecurity programs for nuclear power reactor licensees (commercial power reactors licensed under 10 CFR Part 50 or Part 52); protects digital computer and communication systems and networks associated with safety systems, security systems, emergency preparedness systems, and support systems
**Authority:** U.S. Nuclear Regulatory Commission (NRC)
**Enforcing context:** All nuclear power reactor licensees; Rule effective March 2009; implementation per licensee schedule negotiated with NRC
**Related:** 10 CFR 73.77 (cybersecurity incidents and reporting); RG 5.71 (Cyber Security Programs for Nuclear Facilities — primary guidance document)
**Inspection:** Periodic NRC inspections per Inspection Procedure 71130.10

---

## Summary

| Metric | Count |
|---|---|
| Protected asset categories | 4 (Safety / Security / Emergency preparedness / Support) |
| Critical Digital Assets (CDAs) identified by licensee | Site-specific |
| Cybersecurity controls source | NIST SP 800-53 r4 (referenced by RG 5.71) |
| Sections parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | Moderate — isolation requirements; reporting deadlines; plan elements |
| Partial automation (PARAMETERIZED) | Dominant — CDA identification methodology; security control selection |
| Human-determination required (CONTESTED) | Moderate — CDA boundary determination; defense-in-depth adequacy |
| Open assumptions | 0 |

---

## Scoping pre-condition

```python
def is_nrc_nuclear_power_licensee() -> bool:
    """
    True if entity holds NRC license to operate a nuclear power reactor under
    10 CFR Part 50 or Part 52. Does NOT include:
    - Research reactors (different framework)
    - Fuel cycle facilities (10 CFR 74)
    - Materials licensees
    """
```

---

## Protected systems scope — 4 categories

| Category | Examples | NRC designation |
|---|---|---|
| Safety systems | Reactor protection system, ECCS, containment isolation | Highest protection level |
| Security systems | Access control, intrusion detection, physical security comms | High protection |
| Emergency preparedness systems | Emergency notification, dose assessment | High protection |
| Support systems and equipment | Balance of plant digital systems that could affect above | Determined by analysis |

Systems affecting nuclear safety, security, or emergency preparedness are **Critical Digital Assets (CDAs)** — the foundational scoping determination.

---

## CDA identification — PARAMETERIZED (foundational pre-condition)

```python
def is_cda(system) -> bool:
    """
    True if the digital system could adversely affect the safety, security,
    or emergency preparedness functions. Determination requires:
    1. Consequence analysis — could failure affect protected functions?
    2. Attack vector analysis — could the system be exploited as an attack path?
    Source: RG 5.71 Section 4.1
    """
```

All subsequent controls apply to CDAs. CDA boundary determination is PARAMETERIZED/CONTESTED at the methodology level; specific systems in or out is DETERMINISTIC once methodology is applied.

---

## Defense-in-depth security architecture

10 CFR 73.54 and RG 5.71 require defense-in-depth through security levels:

| Level | Description | Confidence |
|---|---|---|
| Level 4 | Highest security — direct connection to reactor protection/ECCS | DETERMINISTIC isolation required |
| Level 3 | Systems that could affect Level 4 | DETERMINISTIC — one-way data flows only |
| Level 2 | Support systems | PARAMETERIZED controls |
| Level 1 | Business systems with any connectivity | PARAMETERIZED controls |

**Isolation requirements (DETERMINISTIC):**
- No direct connections from Level 4 to lower levels
- Data flows from Level 4 to lower levels: one-way data diodes only
- No wireless connections to Level 4 systems
- No portable media introduction to Level 4 without controlled process

---

## Cybersecurity program — required elements (DETERMINISTIC checklist)

The licensee's cybersecurity plan submitted to NRC must include:

1. Program scope (CDA identification methodology)
2. Cybersecurity controls (mapped to RG 5.71 / NIST 800-53)
3. Change management process
4. Supply chain cybersecurity
5. Incident response capability (10 CFR 73.77)
6. Personnel training and awareness
7. Configuration management
8. Protective strategy (defense-in-depth architecture)
9. Program review and assessment process
10. Reporting to NRC

---

## Incident reporting — DETERMINISTIC deadlines (10 CFR 73.77)

| Event | Reporting Deadline | Recipient |
|---|---|---|
| Cybersecurity event affecting required functions | Within 1 hour | NRC Operations Center (301-816-5100) |
| Cybersecurity event not affecting required functions | Within 8 hours | NRC Operations Center |
| Cybersecurity events (written follow-up) | Within 30 days | NRC (written report) |
| Annual assessment submission | Annually | NRC resident inspector |

---

## Key DETERMINISTIC requirements

| Obligation | Requirement | Source |
|---|---|---|
| Level 4 isolation | No direct connections; data diodes for any data flow | RG 5.71 §4.3.3 |
| No wireless on Level 4 CDAs | Absolutely prohibited | 10 CFR 73.54 / RG 5.71 |
| No portable media (uncontrolled) | Media control process required | RG 5.71 §4.3.3 |
| 1-hour incident reporting (affecting required functions) | 1 hour from discovery | 10 CFR 73.77 |
| Annual program assessment | Once per year | 10 CFR 73.54(e) |
| Cybersecurity plan NRC approval | Required before implementation | 10 CFR 73.54(b) |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Network isolation architecture | NRC 10 CFR 73.54, NERC CIP-005, IEC 62443, TSA SD-02D | Nuclear Level 4 isolation is most stringent in registry |
| Security control framework | NRC 10 CFR 73.54 (via RG 5.71), NIST SP 800-53, NERC CIP | RG 5.71 references NIST 800-53 r4 as control source |
| Incident reporting | NRC 10 CFR 73.77, CISA reporting, TSA SD-01C | Different timelines; 1-hour NRC is tightest in OT sector |
| Change management | NRC 10 CFR 73.54, NERC CIP-010, IEC 62443 | Same change process applied to CDAs |
| Supply chain security | NRC (RG 5.71 §4.5), NERC CIP-013, NIST SP 800-161 | All require vendor cybersecurity assessment |
