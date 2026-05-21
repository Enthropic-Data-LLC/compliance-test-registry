# FDA FSMA — Food Safety Modernization Act (21 U.S.C. §2201 et seq.)

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Domestic and foreign food facilities that manufacture, process, pack, or hold food for human consumption in the United States; separate rules for produce farms, importers, and sanitary transportation
**Authority:** U.S. Food and Drug Administration (FDA) under FSMA (signed January 2011); implementing rules in 21 CFR Parts 1, 11, 16, 106–110, 117, 121, 123, 507, 600
**Enforcing context:** All FDA-registered food facilities; foreign facilities exporting to US; FSVP applies to US importers
**Primary rules:** PCHR (21 CFR Part 117), PCHAF (21 CFR Part 507), Produce Safety Rule (21 CFR Part 112), FSVP (21 CFR Part 1 Subpart L), Sanitary Transportation (21 CFR Part 1 Subpart O), Enhanced Traceability (21 CFR Part 204)

---

## Summary

| Metric | Count |
|---|---|
| FSMA implementing rules | 7 major rules |
| HARPC required elements | 8 (vs. HACCP traditional 7) |
| Enhanced Traceability foods (FTL) | ~16 food categories |
| Sections parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | Moderate — HARPC documentation elements; record retention timelines; traceability retrieval deadline |
| Partial automation (PARAMETERIZED) | Dominant — hazard characterization, supply chain controls |
| Human-determination required (CONTESTED) | High — "reasonably foreseeable" hazard scope |
| Open assumptions | 0 |

---

## Scoping pre-condition

```python
def is_fda_registered_food_facility() -> bool:
    """
    True if facility manufactures, processes, packs, or holds food for
    human consumption in the US and is required to register under 21 CFR Part 1.
    Exemptions: farms, retail food establishments, restaurants, non-profit
    charitable food facilities, fishing vessels.
    """

def is_very_small_business() -> bool:
    """True if food sales < $1M/year averaged over 3 years — modified HARPC applies."""

def is_small_business() -> bool:
    """True if < 500 FTE — reduced compliance timelines applied."""
```

---

## Preventive Controls for Human Food (21 CFR Part 117) — HARPC

HARPC (Hazard Analysis and Risk-Based Preventive Controls) extends HACCP with additional elements:

### Hazard Analysis — required scope (DETERMINISTIC element list)

Written hazard analysis must consider:
1. **Biological hazards** (pathogens)
2. **Chemical hazards** (including radiological)
3. **Physical hazards** (foreign objects)
4. **Economically motivated adulteration** (EMA) — new vs. traditional HACCP
5. **Naturally occurring hazards**
6. **Intentionally introduced hazards** (food defense)

### Preventive Controls — 4 types (DETERMINISTIC taxonomy)

| Control Type | Examples | Confidence |
|---|---|---|
| Process controls | Cooking, pasteurization, pH | PARAMETERIZED — critical parameters org-defined |
| Food allergen controls | Preventing cross-contact, labeling | DETERMINISTIC — allergen program must be documented |
| Sanitation controls | Environmental pathogens, equipment cleaning | PARAMETERIZED |
| Supply chain controls | Approved suppliers, verification activities | PARAMETERIZED |

### Required program elements (DETERMINISTIC checklist)

Food Safety Plan must include:
1. Written hazard analysis
2. Written preventive controls (for each significant hazard)
3. Written supply chain program (if supply chain applied as control)
4. Written recall plan
5. Monitoring procedures
6. Corrective action procedures
7. Verification procedures
8. Validation records (for process controls)

---

## Record retention requirements — DETERMINISTIC

| Record type | Retention period | Notes |
|---|---|---|
| Food Safety Plan | 2 years after plan is superseded | Must be retained at facility |
| Monitoring records | 2 years | During and after production |
| Corrective action records | 2 years | All deviations and CAPAs |
| Verification records | 2 years | Calibration, audit, validation |
| Training records | 2 years after employee leaves | Qualified Individual training |
| Supply chain program records | 2 years | Supplier verification activities |

---

## Enhanced Traceability Rule (21 CFR Part 204) — DETERMINISTIC

Applies to foods on the Food Traceability List (FTL): leafy greens, tomatoes, peppers, cucumbers, melons, tropical tree fruits, herbs, ready-to-eat deli salads, shell eggs, nut butters, fresh-cut fruits and vegetables, finfish, crustaceans, bivalve mollusks, and soft cheeses.

| Requirement | Threshold | Confidence |
|---|---|---|
| Key Data Elements (KDEs) captured at each Critical Tracking Event (CTE) | Mandatory for FTL foods | DETERMINISTIC |
| Traceability Lot Codes (TLCs) assigned and maintained | Mandatory | DETERMINISTIC |
| Records retrievable within 24 hours upon FDA request | 24-hour deadline | DETERMINISTIC |
| Electronic or paper records | Electronic strongly preferred | PARAMETERIZED |

**Critical Tracking Events (CTEs):** Harvesting, cooling, initial packing, first land-based receiving (seafood), transformation, creation, shipping, receiving.

---

## Foreign Supplier Verification Program (FSVP) — 21 CFR Part 1 Subpart L

| Requirement | Confidence | Notes |
|---|---|---|
| Hazard analysis of imported food | DETERMINISTIC — written analysis required | Same HARPC methodology applied to imported goods |
| Supplier verification activities | PARAMETERIZED — activity type depends on hazard | On-site audit, sampling/testing, record review, or combinations |
| Importer of record = FSVP importer | DETERMINISTIC — single responsible party | |
| FSVP records at US port of entry or main US office | DETERMINISTIC — location requirement | |

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Rule |
|---|---|---|
| Food Safety Plan written requirement | Mandatory | 21 CFR §117.126 |
| Recall plan requirement | Mandatory (written) | 21 CFR §117.139 |
| Record retention | 2 years (minimum) | 21 CFR §117.305 |
| FTL traceability record retrieval | Within 24 hours of FDA request | 21 CFR §204.210 |
| Allergen program documentation | Required for all facilities handling major allergens | 21 CFR §117.135(c)(2) |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| HACCP/HARPC | FDA FSMA Part 117, ISO 22000 §8.5, Codex Alimentarius HACCP | HARPC is FSMA's HACCP variant; ISO 22000 also requires hazard analysis |
| Traceability | FDA FSMA Part 204, ISO 22000 §8.10, EU FIC 178/2002 | FSMA 24-hour retrieval is most stringent |
| Allergen controls | FDA FSMA Part 117, EU FIC 1169/2011 (14 allergens) | Different allergen lists (US: 9 major; EU: 14) |
| Supply chain programs | FDA FSMA Part 117 Subpart G, FSVP, ISO 22000 §8.6 | FSVP is importer-specific; FSMA Part 117 applies to domestic manufacturers |
| Recall program | FDA FSMA Part 117, FDA 21 CFR Part 7 (voluntary recall guidance), ISO 22000 §8.9.5 | Recall plan must be written and tested |
