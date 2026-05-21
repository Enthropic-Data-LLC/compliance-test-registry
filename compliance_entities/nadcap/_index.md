# NADCAP — National Aerospace and Defense Contractors Accreditation Program

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Special processes in aerospace and defense manufacturing — heat treatment, welding, chemical processing, non-destructive testing (NDT), composites, coatings, electronics, and materials testing
**Authority:** Performance Review Institute (PRI) on behalf of Nadcap Subscribers (Boeing, Lockheed Martin, Raytheon, Airbus, GE Aviation, Pratt & Whitney, etc.)
**Enforcing context:** Required by prime contractors (subscribers) as a condition of sourcing; applies to both OEM and MRO suppliers performing NADCAP-scope special processes
**Structure:** Each special process has its own Aerospace Quality System (AQS) checklist; AC7000 series; audits performed by PRI-trained commodity teams
**Relationship to AS9100:** NADCAP does not replace AS9100; special process accreditation is in addition to QMS certification

---

## Summary

| Metric | Count |
|---|---|
| NADCAP commodities (special process categories) | ~20 |
| Audit checklist series | AC7000 series (AC7004 = NDT, AC7102 = heat treat, AC7108 = welding, AC7115 = chem processing, etc.) |
| Accreditation body | Performance Review Institute (PRI) |
| Validity period | 12 or 18 months (based on merit system score) |
| Sections parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | High — process specification compliance; record completeness; equipment calibration |
| Partial automation (PARAMETERIZED) | Moderate — process qualification methodology |
| Human-determination required (CONTESTED) | Low — NADCAP checklists are prescriptive |
| Open assumptions | 0 |

---

## Scoping pre-condition

```python
def performs_nadcap_commodity() -> bool:
    """
    True if organization performs any of the following special processes
    on behalf of aerospace/defense customers:
    - Chemical processing (etching, plating, anodizing, conversion coatings)
    - Heat treatment
    - Non-destructive testing (NDT/NDE)
    - Welding and brazing
    - Composites
    - Coatings (thermal spray, paint, adhesive bonding)
    - Fluid distribution systems (tubing, hose)
    - Electronics (solder, conformal coat, wire harness — AC7120 series)
    - Metallic materials testing
    - Non-metallic materials testing
    """

def customer_requires_nadcap() -> bool:
    """True if purchase order or supplier manual from aerospace customer specifies NADCAP."""
```

---

## NADCAP audit structure — common elements (DETERMINISTIC)

All NADCAP commodity audits share a common structure:

| Element | Confidence | Notes |
|---|---|---|
| Written process specification compliance | DETERMINISTIC | Supplier must demonstrate compliance with applicable customer/industry spec |
| Process operator qualification records | DETERMINISTIC | Operators qualified per applicable spec (e.g., AWS D1.1 for welding) |
| Equipment calibration records | DETERMINISTIC | All process equipment calibrated; current calibration certificates |
| Process control records (job travelers) | DETERMINISTIC | Each job/lot has accompanying process control documentation |
| Material certifications | DETERMINISTIC | Raw material certs traceable to each job |
| Nonconformance records | DETERMINISTIC | All NCs documented and dispositioned |
| Customer drawing/specification revision control | DETERMINISTIC | Current revision of all customer specs in use |

---

## Selected commodity-specific requirements

### Heat Treatment (AC7102)
- Furnace calibration: TUS (Temperature Uniformity Survey) at defined intervals — DETERMINISTIC
- SAT (System Accuracy Test): Per AMS 2750 — frequency is DETERMINISTIC
- Atmosphere controls: Documented and recorded — PARAMETERIZED
- Load tracking: Each load traceable to process parameters — DETERMINISTIC

### Non-Destructive Testing — NDT (AC7004 + level-specific checklists)
- NDT technician certification: Per NAS 410, EN 4179, or ASNT SNT-TC-1A — DETERMINISTIC
- Level of certification required per method (PT/MT/UT/RT/ET): DETERMINISTIC per customer spec
- Reference standards/calibration blocks: Current and traceable — DETERMINISTIC
- Technique sheets/written procedures: Approved per applicable standard — DETERMINISTIC

### Welding (AC7110 series)
- Welder qualification per AWS/ASME/AMS — DETERMINISTIC records required
- WPS (Welding Procedure Specification) and PQR (Procedure Qualification Record) — DETERMINISTIC
- Filler material certification and traceability — DETERMINISTIC

### Chemical Processing (AC7108 / AC7115)
- Bath chemistry controls: Process range documented; frequency of analysis defined — DETERMINISTIC
- Rinsing and process sequence: Per specification — DETERMINISTIC
- Solution records: Each bath analysis result retained — DETERMINISTIC

---

## Merit system — accreditation duration (DETERMINISTIC)

NADCAP uses a merit system to extend accreditation for high performers:

| Finding level | Impact |
|---|---|
| Major finding (NCR) | Audit extension required; may suspend accreditation |
| Minor finding | Must be closed before accreditation renewed |
| Zero major findings (consecutive audits) | Eligible for extended accreditation (18 months) |
| Multiple major findings | Increased surveillance; potential probation |

---

## Key DETERMINISTIC requirements (common across commodities)

| Obligation | Requirement |
|---|---|
| Customer specification compliance | Must demonstrate compliance with all invoked specs |
| Equipment calibration currency | No expired calibrations at time of audit |
| Operator/technician qualification currency | No expired qualifications |
| Job traveler completeness | All required entries present for audited jobs |
| Corrective action closure | All prior NCRs closed before renewal |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Special process records | NADCAP, AS9100 §8.5.1.2 (special processes), ISO 9001 §8.5 | AS9100 requires special processes be validated; NADCAP is the validation evidence |
| Operator qualification records | NADCAP, AWS D1.1, ASME Section IX, NAS 410 | Same qualification records — industry standard certs |
| Calibration records | NADCAP, ISO 9001 §7.1.5, IATF 16949 | Same calibration management system |
| Material certifications | NADCAP, AS9100 §8.4, DFARS (counterfeit part) | Same material traceability |
| Customer specification management | NADCAP, AS9100 §8.3, IATF 16949 | Drawing/spec revision control shared |
