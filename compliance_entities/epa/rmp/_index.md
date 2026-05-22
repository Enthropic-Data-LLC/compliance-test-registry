# EPA RMP — Risk Management Program (40 CFR Part 68)

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Prevention and emergency response planning for accidental chemical releases at facilities with regulated substances above threshold quantities; 40 CFR Part 68
**Authority:** U.S. Environmental Protection Agency (EPA); Clean Air Act §112(r)(7)
**Enforcing context:** Facilities that have more than a threshold quantity (TQ) of a regulated substance in a single process; ~12,500 facilities in the US
**Program tiers:** Program 1 (lowest risk), Program 2 (moderate), Program 3 (highest risk — same as OSHA PSM)
**Related:** OSHA PSM (29 CFR 1910.119) — nearly identical requirements for Program 3; they are implemented together

---

## Summary

| Metric | Count |
|---|---|
| Regulated substances (toxic) | 77 |
| Regulated substances (flammable) | 63 |
| RMP Program tiers | 3 |
| Sections parsed (individual files) | 1 (see README for coverage) |
| Fully automated (DETERMINISTIC) | Moderate — TQ thresholds, submission deadlines, 5-year resubmission, incident reporting |
| Partial automation (PARAMETERIZED) | Dominant — consequence analysis methodology, PHA methodology |
| Human-determination required (CONTESTED) | Moderate — worst-case scenario parameters, safeguard crediting |
| Open assumptions | 0 |

---

## Scoping pre-condition — threshold quantity (TQ)

```python
def requires_rmp(process) -> bool:
    """
    True if any single process has a regulated substance present at or above
    the threshold quantity (TQ) listed in 40 CFR Part 68 Appendix A (toxics)
    or §68.115 (flammables).
    TQ examples:
    - Chlorine: 2,500 lbs
    - Anhydrous ammonia: 10,000 lbs
    - Flammable substances: 10,000 lbs
    """
    return any(substance.quantity >= substance.tq for substance in process.regulated_substances)
```

---

## RMP Program determination — DETERMINISTIC

| Program | Criteria | Requirements |
|---|---|---|
| **Program 1** | Worst-case release would not reach public receptors; no accidents in last 5 years; coordinated with LEPC | Simplified analysis; no PHA required; 5-yr accident history |
| **Program 2** | Not eligible for P1; not in P3 | Hazard assessment; prevention program; emergency response |
| **Program 3** | Process subject to OSHA PSM (1910.119) OR NAICS codes listed in §68.10(d) (e.g., petroleum refining, chemical manufacturing) | Full PHA; OSHA PSM-equivalent prevention; emergency response |

Program determination is DETERMINISTIC once TQ and NAICS criteria evaluated.

---

## RMP Plan — 5 required elements (DETERMINISTIC checklist)

An RMP must include:
1. **Registration** — facility information, regulated substances, program tier
2. **Hazard assessment** — worst-case release scenario + alternative release scenario for each Program 2/3 process
3. **Prevention program** — PHA (P3) or simpler analysis (P2); safety information; operating procedures; training; maintenance; incident investigation
4. **Emergency response program** — written plan; coordination with LEPC; training
5. **Five-year accident history** — all accidents involving regulated substances that resulted in deaths, injuries, significant property damage, or offsite impacts

---

## Hazard assessment — scenario requirements (DETERMINISTIC)

| Scenario | Requirement | Confidence |
|---|---|---|
| Worst-case release scenario | Instantaneous release of largest vessel contents; passive mitigation only; meteorological conditions per §68.22 | DETERMINISTIC parameters; PARAMETERIZED consequence modeling |
| Alternative release scenario | More likely release; active and passive mitigation credited | PARAMETERIZED |
| Endpoint distance (toxic) | IDLH, ERPG-2, or AEGL-2 endpoint | DETERMINISTIC endpoint selection |
| Endpoint (flammable) | Overpressure = 1 psi or radiant heat = 1 kW/m² | DETERMINISTIC endpoint |
| Offsite consequence analysis | Public receptor in endpoint zone = Program 1 ineligible | DETERMINISTIC binary |

---

## Program 3 prevention program (= OSHA PSM elements)

| Element | Confidence | Notes |
|---|---|---|
| Process Safety Information (PSI) | DETERMINISTIC — written documentation of chemicals, technology, equipment | |
| Process Hazard Analysis (PHA) | PARAMETERIZED — methodology (HAZOP/What-if/Checklist) documented | Revalidation every 5 years |
| Operating Procedures | DETERMINISTIC — written; reviewed annually | |
| Training | DETERMINISTIC — initial + refresher; records | |
| Contractors | PARAMETERIZED — contractor safety program requirements | |
| Pre-Startup Safety Review (PSSR) | DETERMINISTIC — before startup of new/modified process | |
| Mechanical Integrity | PARAMETERIZED — inspection/testing program for pressure vessels, piping, relief valves | |
| Hot Work Permit | DETERMINISTIC — permit required before hot work on/near process equipment | |
| Management of Change (MOC) | DETERMINISTIC — written MOC procedure; review before change | |
| Incident Investigation | DETERMINISTIC — investigation within 48 hours of incident; 5-year record retention | |
| Emergency Response | DETERMINISTIC — written plan; coordination with LEPC; annual review | |
| Compliance Audits | DETERMINISTIC — every 3 years; certified report | |

---

## RMP submission and resubmission — DETERMINISTIC deadlines

| Trigger | Deadline | Recipient |
|---|---|---|
| New RMP (new regulated process) | Before start of operations | EPA RMP*eSubmit |
| Resubmission — updated RMP | Within 5 years of initial submission OR within 3 years of accident | EPA RMP*eSubmit |
| Resubmission — change in program tier | Within 6 months of change | EPA RMP*eSubmit |
| Resubmission — new regulated substance added above TQ | Within 6 months | EPA RMP*eSubmit |
| Accident report (accidental release) | Within 4 hours of release affecting offsite receptors | NRC + EPA Local Emergency Coordinator |

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Regulation |
|---|---|---|
| RMP required (chlorine example) | ≥ 2,500 lbs in single process | 40 CFR §68.115 / App. A |
| RMP required (anhydrous ammonia) | ≥ 10,000 lbs in single process | 40 CFR §68.115 |
| RMP required (flammables) | ≥ 10,000 lbs in single process | 40 CFR §68.115 |
| RMP 5-year resubmission | Every 5 years | 40 CFR §68.190 |
| Accident history period | 5 years prior to submission | 40 CFR §68.42 |
| Incident investigation initiation | Within 48 hours | 40 CFR §68.81 |
| Compliance audit frequency | Every 3 years | 40 CFR §68.79 |
| Accidental release report (offsite impact) | Within 4 hours | 40 CFR §68.195 |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Process Hazard Analysis | EPA RMP Program 3, OSHA PSM (§1910.119) | Identical requirement — one PHA satisfies both |
| Emergency response plan | EPA RMP §68 Subpart E, RCRA contingency plan, EPCRA §303 | Single emergency response plan |
| Incident investigation | EPA RMP §68.81, OSHA PSM §119(m), ISO 45001 §10.2 | Same investigation process and 5-yr record |
| Management of Change | EPA RMP §68.75, OSHA PSM §119(l), ISO 45001 §8.1.3 | Unified MOC procedure |
| Process Safety Information | EPA RMP §68.65, OSHA PSM §119(d) | Same PSI document package |
| Compliance audit | EPA RMP §68.79 (3-year), OSHA PSM §119(o) (3-year) | Coordinated audit covers both |
