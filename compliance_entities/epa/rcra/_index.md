# EPA RCRA — Resource Conservation and Recovery Act (Hazardous Waste)

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Generation, transportation, treatment, storage, and disposal of hazardous waste; 40 CFR Parts 260–272; also covers used oil (Part 279) and universal waste (Part 273)
**Authority:** U.S. Environmental Protection Agency (EPA); delegated to authorized state programs in most states
**Enforcing context:** Any facility generating, transporting, treating, storing, or disposing of hazardous waste; generator category (LQG/SQG/VSQG) determines applicable requirements
**Key subparts:** Part 260 (definitions), Part 261 (identification), Part 262 (generators), Part 263 (transporters), Part 264/265 (TSD facilities), Part 268 (land disposal restrictions), Part 270 (permits)

---

## Summary

| Metric | Count |
|---|---|
| Generator categories | 3 (LQG / SQG / VSQG) |
| Primary DETERMINISTIC thresholds | Monthly generation quantity + on-site accumulation limits |
| Sections parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | High — generator category thresholds; storage time limits; manifest elements |
| Partial automation (PARAMETERIZED) | Moderate — waste characterization methodology |
| Human-determination required (CONTESTED) | Moderate — TCLP/characteristic determinations; listed waste applicability |
| Open assumptions | 0 |

---

## Generator category — foundational DETERMINISTIC pre-condition

Generator status is determined monthly by quantity of hazardous waste generated:

| Category | Monthly generation | Accumulation time limit | On-site storage limit |
|---|---|---|---|
| **LQG** (Large Quantity Generator) | ≥ 1,000 kg/month | 90 days | No quantity limit (within 90 days) |
| **SQG** (Small Quantity Generator) | 100–999 kg/month | 270 days | 6,000 kg |
| **VSQG** (Very Small Quantity Generator) | < 100 kg/month (< 1 kg acutely hazardous) | None (must send off-site) | 1,000 kg |

Category thresholds are DETERMINISTIC — breach = immediate reclassification upward and loss of generator-category accumulation time.

```python
def generator_category(monthly_kg: float) -> str:
    if monthly_kg >= 1000:
        return "LQG"
    elif monthly_kg >= 100:
        return "SQG"
    else:
        return "VSQG"
```

---

## Hazardous waste identification — confidence map

### Listed wastes (F, K, P, U lists)

| List | Description | Confidence |
|---|---|---|
| F-list | Wastes from nonspecific sources (spent solvents, electroplating) | DETERMINISTIC — specific waste codes |
| K-list | Wastes from specific industry sources | DETERMINISTIC — specific SIC codes + waste types |
| P-list | Acutely hazardous discarded commercial chemical products | DETERMINISTIC — specific chemical codes |
| U-list | Toxic discarded commercial chemical products | DETERMINISTIC — specific chemical codes |

### Characteristic wastes (D codes)

| Characteristic | Test | Threshold | Confidence |
|---|---|---|---|
| D001 — Ignitability | Flash point test | Flash point < 60°C (140°F) for liquids | DETERMINISTIC |
| D002 — Corrosivity | pH or corrosion rate | pH ≤ 2 or ≥ 12.5 | DETERMINISTIC |
| D003 — Reactivity | Expert/lab determination | Explosive, reacts violently with water, etc. | PARAMETERIZED/CONTESTED |
| D004–D043 — Toxicity | TCLP test | Exceeds regulatory level for specific compounds | DETERMINISTIC (threshold); PARAMETERIZED (TCLP application) |

---

## Generator requirements — DETERMINISTIC obligations by category

### LQG requirements

| Requirement | Deadline / Limit | Confidence |
|---|---|---|
| Accumulation time limit | 90 days from start of accumulation | DETERMINISTIC |
| Emergency coordinator — 24/7 | Immediate designation | DETERMINISTIC |
| Contingency plan | Written; submitted to local authorities | DETERMINISTIC |
| Personnel training | Initial + annual refresher; records retained 3 years | DETERMINISTIC |
| Biennial report | February 28 of even years | DETERMINISTIC |
| Pre-transport labeling | Before leaving facility | DETERMINISTIC |
| Manifest (EPA Form 8700-22) | Required for all off-site shipments | DETERMINISTIC |

### SQG requirements

| Requirement | Deadline / Limit | Confidence |
|---|---|---|
| Accumulation time limit | 270 days | DETERMINISTIC |
| Emergency coordinator | At least one per facility | DETERMINISTIC |
| Basic emergency procedures | Written; posted | DETERMINISTIC |
| Personnel training | Initial training required | DETERMINISTIC |
| Manifest | Required for all off-site shipments | DETERMINISTIC |

### VSQG requirements

| Requirement | Requirement | Confidence |
|---|---|---|
| Maximum on-site accumulation | 1,000 kg total | DETERMINISTIC |
| Must send to LQG, TSD facility, or reclaimer | Consolidated or direct shipment | DETERMINISTIC |
| Manifest | Not required (VSQG exception) | DETERMINISTIC exemption |

---

## Uniform Hazardous Waste Manifest — required elements (DETERMINISTIC)

40 CFR Part 262 Subpart B — manifest must include:
1. Generator name, address, and EPA ID number
2. Transporter name(s) and EPA ID number(s)
3. Designated facility name, address, and EPA ID
4. DOT description of waste (proper shipping name, hazard class, ID number)
5. Quantity (containers, type, volume/weight)
6. Special handling instructions
7. Certification signature (generator)
8. Transporter acknowledgment signature
9. Facility acknowledgment signature

Missing manifest elements = regulatory violation (DETERMINISTIC).

---

## Storage area requirements (satellite accumulation / central accumulation)

| Requirement | Confidence | Notes |
|---|---|---|
| Container labeling: "Hazardous Waste" + contents + hazards | DETERMINISTIC | Must be labeled from first drop of waste |
| Container in good condition; compatible with waste | DETERMINISTIC | |
| Container closed (except when adding waste) | DETERMINISTIC | |
| Weekly inspection of storage areas (LQG) | DETERMINISTIC | Written inspection log |
| Satellite accumulation: at/near point of generation; ≤ 55 gal | DETERMINISTIC | Separate limits for acutely hazardous |

---

## Land disposal restrictions (LDR) — 40 CFR Part 268

Most hazardous wastes are prohibited from land disposal unless treated to meet LDR treatment standards. LDR notification required with each shipment.

| Requirement | Confidence |
|---|---|
| LDR treatment standard met before land disposal | DETERMINISTIC — specific concentration standards by waste code |
| LDR notification/certification with manifest | DETERMINISTIC — required for each shipment |
| One-time notification for wastewater treated on-site | DETERMINISTIC |

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | CFR Reference |
|---|---|---|
| LQG accumulation limit | 90 days | 40 CFR §262.17 |
| SQG accumulation limit | 270 days | 40 CFR §262.16 |
| VSQG on-site quantity limit | 1,000 kg total | 40 CFR §262.14 |
| D002 corrosivity (pH) | ≤ 2 or ≥ 12.5 | 40 CFR §261.22 |
| D001 ignitability flash point | < 60°C (liquids) | 40 CFR §261.21 |
| Biennial report deadline | February 28 (even years) | 40 CFR §262.41 |
| Personnel training records retention | 3 years | 40 CFR §262.16/17 |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Chemical inventory | RCRA, EPCRA §311/312 (Tier II), OSHA 1910.1200 (HazCom), REACH | Same chemical inventory system |
| Emergency response plan | RCRA contingency plan (LQG), EPCRA §303 LEPC plan, OSHA PSM §119, EPA RMP Part 68 | Same emergency response infrastructure |
| Waste manifest | RCRA Part 262, DOT 49 CFR (hazmat shipping) | Manifest is also a DOT shipping paper |
| Training records | RCRA §262.16/17, OSHA 1910.1200 (HazCom training), ISO 14001 §7.2 | Same training management system |
| Environmental permit | RCRA Part 270 (TSD permit), Clean Air Act Title V, NPDES | Facility environmental permit portfolio |
