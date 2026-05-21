# EPA Clean Air Act — Title V Operating Permits / NSPS / NESHAP / CAM

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Air emissions from stationary sources; Title V operating permits for major sources; New Source Performance Standards (NSPS); National Emission Standards for Hazardous Air Pollutants (NESHAP); Compliance Assurance Monitoring (CAM); Prevention of Significant Deterioration (PSD) for new/modified major sources
**Authority:** U.S. Environmental Protection Agency (EPA); State Implementation Plans (SIPs); delegated to state/local air agencies
**Key regulations:** 40 CFR Part 70 (Title V operating permits); 40 CFR Part 60 (NSPS); 40 CFR Parts 61/63 (NESHAP/MACT); 40 CFR Part 64 (CAM); 40 CFR Parts 51/52 (NAAQS/SIP)

---

## Summary

| Metric | Count |
|---|---|
| NAAQS criteria pollutants | 6 (PM2.5, PM10, O3, NO2, SO2, CO, Pb) |
| Title V major source thresholds | 2 (100 tpy general; 10–50 tpy for HAPs) |
| CAP 40 CFR Part 60 subparts | 100+ source categories |
| Sections parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | Moderate — permit condition compliance; emission limits; reporting deadlines |
| Partial automation (PARAMETERIZED) | Dominant — source-specific emission limits from permit |
| Human-determination required (CONTESTED) | Moderate — emissions calculation methodology |
| Open assumptions | 0 |

---

## Scoping pre-conditions

```python
def is_title_v_major_source(facility) -> bool:
    """
    True if facility emits (or has potential to emit) at or above:
    - 100 tpy for any criteria pollutant (general)
    - 10 tpy of a single HAP OR 25 tpy of combined HAPs
    - Lower thresholds apply in nonattainment areas (varies by pollutant and area designation)
    Note: Potential to emit (PTE) is calculated at max physical capacity, not actual emissions.
    """

def subject_to_nsps(source) -> bool:
    """True if source is in a listed source category AND commenced construction,
    modification, or reconstruction after the applicability date for that subpart."""

def subject_to_mact(source) -> bool:
    """True if source is a major source (or area source) in a MACT-regulated source category."""
```

---

## Title V Operating Permits — 40 CFR Part 70

### Permit required elements (DETERMINISTIC checklist)

A Title V permit must include:
1. Emission limitations and standards for each regulated air pollutant
2. Operational requirements and limitations
3. Compliance schedule (if not currently in compliance)
4. Monitoring and related record-keeping requirements
5. Reporting requirements (at minimum semi-annual)
6. Compliance certification (annual) by responsible official
7. Permit shield (confirmation that compliance = compliance with all applicable requirements)

### Key permit timelines — DETERMINISTIC

| Milestone | Deadline |
|---|---|
| Application for new major source | Before commencing construction |
| Permit renewal application | ≥ 6 months before permit expiration |
| Title V permit term | Maximum 5 years |
| Permit deviation report | Prompt: within 2 business days of deviation (verbal); written within 10 days |
| Semi-annual compliance certification | Every 6 months (or more frequently per permit) |
| Annual compliance certification | Once per year; submitted to EPA + state |

---

## New Source Performance Standards (NSPS) — 40 CFR Part 60

NSPS set emission limits for specific source categories (e.g., fossil fuel-fired boilers, petroleum refineries, cement plants). Applicable subpart determined by source category + construction/modification date.

| Obligation | Confidence | Notes |
|---|---|---|
| Emission limit compliance | DETERMINISTIC — permit-specific emission limits | Limit is DETERMINISTIC; measurement methodology is PARAMETERIZED |
| Initial performance test | DETERMINISTIC — required within 60 days of initial startup | Method 9 (opacity), Method 5 (PM), etc. |
| Continuous monitoring (if required by subpart) | DETERMINISTIC — continuous opacity or CEM (CEMS) data | |
| Excess emission reports | DETERMINISTIC — quarterly or semi-annual per subpart | Must be submitted to state agency |

---

## NESHAP / MACT Standards — 40 CFR Parts 61/63

Maximum Achievable Control Technology (MACT) standards for Hazardous Air Pollutant (HAP) sources:

| Obligation | Confidence | Notes |
|---|---|---|
| MACT compliance — emission limit or work practice | DETERMINISTIC — binary per standard | Source either meets MACT floor or doesn't |
| Initial notification | DETERMINISTIC — within 120 days of applicability | |
| Initial compliance demonstration | DETERMINISTIC — within compliance date per subpart | Performance test or design evaluation |
| Ongoing compliance monitoring | PARAMETERIZED — method specified per subpart | |
| Periodic reports (semi-annual or annual) | DETERMINISTIC — schedule per subpart | |

---

## Compliance Assurance Monitoring (CAM) — 40 CFR Part 64

CAM applies to Title V sources with control devices where emissions could exceed major source thresholds without the control device:

| Requirement | Confidence | Notes |
|---|---|---|
| CAM plan submitted with permit application | DETERMINISTIC | Must include approved monitoring approach |
| Indicator monitoring per CAM plan | DETERMINISTIC | Monitoring as specified in approved CAM plan |
| Exceedance reporting | DETERMINISTIC | Deviations from CAM indicator ranges reported |

---

## Greenhouse Gas Reporting — 40 CFR Part 98

Separate from Title V; applies to facilities emitting ≥ 25,000 metric tons CO2e/year:

| Requirement | Deadline | Confidence |
|---|---|---|
| Annual GHG report submission | March 31 of following year | DETERMINISTIC |
| Report to EPA e-GGRT system | Online submission | DETERMINISTIC |
| Source category applicability | > 25,000 mtCO2e/year | DETERMINISTIC threshold |

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Regulation |
|---|---|---|
| Title V major source (criteria pollutants) | 100 tpy potential to emit | 40 CFR §70.2 |
| Title V major source (single HAP) | 10 tpy | 40 CFR §70.2 |
| Title V major source (combined HAPs) | 25 tpy | 40 CFR §70.2 |
| Title V permit term | 5 years maximum | 40 CFR §70.6(a)(2) |
| Annual compliance certification | Once per year | 40 CFR §70.6(c)(5) |
| Permit deviation verbal notification | 2 business days | 40 CFR §70.6(a)(3) |
| GHG reporting threshold | 25,000 mtCO2e/year | 40 CFR §98.2(a) |
| GHG report deadline | March 31 | 40 CFR §98.3(b) |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Environmental permit portfolio | CAA Title V, RCRA Part 270 (TSD), NPDES | Single facility environmental permit manager |
| Emission inventory | CAA Title V, EPCRA §313 TRI, GHG reporting | Same source-level emission data; different pollutant lists |
| Stack testing / CEMS data | CAA NSPS/MACT, Title V compliance | Performance test records; CEMS data retention (2 years minimum) |
| Emergency generators | CAA §60 Subpart IIII/JJJJ (RICE NESHAP), Title V (if major source) | Backup generator emission limits and operating hour limits |
| ISO 14001 compliance obligations | CAA permits, ISO 14001 §6.1.2 legal register | Air permit conditions are compliance obligations in EMS |
