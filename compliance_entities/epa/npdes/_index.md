# EPA Clean Water Act — NPDES / SPCC / Stormwater

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Discharge of pollutants to waters of the United States (NPDES); oil spill prevention for aboveground/underground oil storage (SPCC); industrial stormwater discharges; dredge and fill permits (Section 404)
**Authority:** U.S. Environmental Protection Agency (EPA); Army Corps of Engineers (§404); delegated to state agencies for NPDES in most states
**Key regulations:** 40 CFR Part 122 (NPDES permit program), 40 CFR Part 112 (SPCC), 40 CFR Part 117 (reportable quantities — §311), 40 CFR Part 136 (test methods)
**Related:** CWA §402 (NPDES), §311 (oil/hazardous substance discharge), §404 (dredge/fill), §316 (thermal discharge)

---

## Summary

| Metric | Count |
|---|---|
| NPDES permit types | 3 (individual / general / stormwater multi-sector) |
| SPCC applicability thresholds | 2 (aboveground capacity / underground capacity) |
| Effluent limit types | 2 (technology-based / water quality-based) |
| Sections parsed (individual files) | 1 (see README for coverage) |
| Fully automated (DETERMINISTIC) | Moderate — permit effluent limits; SPCC quantity thresholds; reporting deadlines |
| Partial automation (PARAMETERIZED) | Dominant — permit conditions are facility-specific |
| Human-determination required (CONTESTED) | Low — thresholds are bright-line |
| Open assumptions | 0 |

---

## NPDES — scoping pre-condition

```python
def requires_npdes_permit(discharge) -> bool:
    """
    True if facility discharges any pollutant from a point source to
    'waters of the United States' (WOTUS). This includes:
    - Process wastewater discharges
    - Cooling water discharges
    - Stormwater from industrial activities (Phase I/II)
    - Concentrated Animal Feeding Operations (CAFOs)
    Note: 'Waters of the United States' definition has been subject to
    litigation/rulemaking — CONTESTED at boundary; DETERMINISTIC for
    clear navigable waters.
    """
```

---

## NPDES permit — compliance obligations

### Effluent limits — DETERMINISTIC (permit-specific values)

Each NPDES permit contains specific numeric effluent limits:

| Limit type | Confidence | Notes |
|---|---|---|
| Daily maximum concentration limit | DETERMINISTIC — any single day exceedance = violation | e.g., "pH shall not exceed 9.0 SU" |
| Monthly average limit | DETERMINISTIC — average of all samples in calendar month | More common metric |
| Weekly average limit | DETERMINISTIC — average within 7-day period | Less common |
| Mass-based limit (lbs/day) | DETERMINISTIC — calculated from flow × concentration | |

**Any exceedance of a permit effluent limit is a DETERMINISTIC violation** regardless of cause.

### Monitoring and reporting — DETERMINISTIC deadlines

| Requirement | Deadline | Confidence |
|---|---|---|
| Discharge Monitoring Report (DMR) | Monthly or quarterly per permit; due within 28 days of period end | DETERMINISTIC |
| Annual report (if required by permit) | Per permit schedule | DETERMINISTIC |
| Noncompliance notification (verbal) | Within 24 hours of discovery | DETERMINISTIC |
| Noncompliance written report | Within 5 days of verbal notification | DETERMINISTIC |
| Bypass/upset notification | Within 24 hours of discovery | DETERMINISTIC |

### Stormwater — Multi-Sector General Permit (MSGP)

| Requirement | Confidence | Notes |
|---|---|---|
| SWPPP (Stormwater Pollution Prevention Plan) | DETERMINISTIC — must exist and be site-specific | |
| Annual comprehensive site inspection | DETERMINISTIC — once per year; documented | |
| Quarterly visual assessment | DETERMINISTIC — every 3 months; log maintained | |
| Benchmark monitoring (if required by sector) | DETERMINISTIC — frequency per permit | |
| No-Exposure Certification (NEC) | DETERMINISTIC — available if all industrial materials/activities under cover | |

---

## SPCC — Spill Prevention, Control, and Countermeasure Plan (40 CFR Part 112)

### Applicability thresholds — DETERMINISTIC

| Facility type | Threshold for SPCC applicability |
|---|---|
| Non-transportation aboveground oil storage | Total aboveground capacity > 1,320 gallons (in containers ≥ 55 gal) OR any single aboveground container > 660 gallons |
| Underground oil storage | Total underground capacity > 42,000 gallons |
| Farms | Aboveground capacity > 1,320 gallons (qualified facilities) |

No threshold = No SPCC obligation. Threshold comparison is DETERMINISTIC.

### SPCC plan — required elements (DETERMINISTIC checklist)

For Tier II (Qualified Facility — PE certification required):
1. Facility name, address, owner/operator
2. Description of facility and oil storage
3. Secondary containment requirements and design
4. Procedures for oil transfers and inspections
5. Personnel training program
6. Security measures (lighting, fencing, etc.)
7. Tank inspection schedule
8. Spill response procedures
9. Contacts for regulatory notifications
10. Certification by Professional Engineer (PE)

### SPCC inspection requirements — DETERMINISTIC

| Inspection type | Frequency | Confidence |
|---|---|---|
| Regular facility inspections | Monthly (visual) — operator-defined interval | DETERMINISTIC existence |
| Bulk storage container inspection | Monthly | DETERMINISTIC |
| Transfer equipment inspection | Per operating procedure | PARAMETERIZED |
| PE review and amendment | At least every 5 years | DETERMINISTIC |

---

## CWA §311 — Oil and Hazardous Substance Discharge Reporting (DETERMINISTIC)

| Discharge type | Report to | Timing |
|---|---|---|
| Oil discharge ≥ reportable quantity to navigable waters | NRC (1-800-424-8802) | Immediately |
| Hazardous substance discharge ≥ RQ | NRC | Immediately |
| Sheen on water (any quantity) | NRC | Immediately |

**Reportable quantities:** 40 CFR Part 110 (oil); 40 CFR Part 117 (CWA hazardous substances). Oil = any discharge that causes a sheen.

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Regulation |
|---|---|---|
| SPCC applicability (aboveground) | > 1,320 gallons total (or > 660 in single container) | 40 CFR §112.1 |
| SPCC applicability (underground) | > 42,000 gallons | 40 CFR §112.1 |
| SPCC PE review | Every 5 years | 40 CFR §112.5 |
| DMR submission | Within 28 days of monitoring period end | 40 CFR §122.41(l)(4) |
| Noncompliance verbal notification | Within 24 hours | 40 CFR §122.41(l)(6) |
| Oil sheen reporting | Immediately | 40 CFR Part 110 |
| Annual stormwater site inspection | Once per calendar year | MSGP §4.1 |
| Quarterly stormwater visual | Once per quarter | MSGP §3.2 |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Spill response plan | SPCC (40 CFR Part 112), RCRA contingency plan, EPA RMP emergency response, EPCRA §302 | Single emergency response document with regulatory appendices |
| Chemical inventory | NPDES (wastewater characterization), EPCRA §311/312 (Tier II), RCRA | Same chemical management system |
| Environmental monitoring data | NPDES DMRs, EPCRA §313 TRI, ISO 14001 §9.1 performance evaluation | Same environmental monitoring infrastructure |
| Secondary containment | SPCC, RCRA Part 264/265 (TSD containment), ISO 14001 §8.2 emergency preparedness | Same engineering controls |
| Compliance obligations register | NPDES permit conditions, ISO 14001 §6.1.2, ISO 45001 §6.1.3 | Permit conditions = compliance obligations in EMS |
