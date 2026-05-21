# RoHS / REACH — EU Chemical Restriction Regulations

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** RoHS: restriction of hazardous substances in electrical and electronic equipment (EEE) placed on the EU market; REACH: registration, evaluation, authorization and restriction of chemicals for substances manufactured or imported into the EU ≥1 tonne/year
**Authority:** European Commission; enforced by national market surveillance authorities; ECHA (European Chemicals Agency) administers REACH
**Current editions:** RoHS 3 (Directive 2011/65/EU as amended by 2015/863/EU — adds 4 phthalates); REACH (Regulation (EC) No 1907/2006)
**Extraterritorial reach:** Both apply to products placed on the EU market — affect non-EU manufacturers exporting to EU

---

## Summary

| Metric | Count |
|---|---|
| RoHS restricted substances | 10 (6 original + 4 phthalates added 2019) |
| REACH SVHC (candidate list substances) | 240+ (updated biannually) |
| REACH threshold for SVHC notification | 0.1% w/w in articles |
| REACH registration threshold | ≥ 1 tonne/year manufactured/imported |
| Sections parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | High — substance threshold comparisons; documentation checklist |
| Partial automation (PARAMETERIZED) | Moderate — supply chain data collection |
| Human-determination required (CONTESTED) | Low — thresholds are bright-line |
| Open assumptions | 0 |

---

## RoHS — restricted substances and thresholds (DETERMINISTIC)

All 10 substances must be below the maximum concentration value (MCV) in homogeneous materials:

| Substance | Maximum concentration (w/w) |
|---|---|
| Lead (Pb) | 0.1% |
| Mercury (Hg) | 0.1% |
| Cadmium (Cd) | 0.01% |
| Hexavalent chromium (Cr VI) | 0.1% |
| Polybrominated biphenyls (PBB) | 0.1% |
| Polybrominated diphenyl ethers (PBDE) | 0.1% |
| Bis(2-ethylhexyl) phthalate (DEHP) | 0.1% |
| Benzyl butyl phthalate (BBP) | 0.1% |
| Dibutyl phthalate (DBP) | 0.1% |
| Diisobutyl phthalate (DIBP) | 0.1% |

All thresholds are DETERMINISTIC — exceedance = non-compliance; no ambiguity.

### RoHS compliance documentation (DETERMINISTIC checklist)

| Document | Required for |
|---|---|
| Technical documentation (test reports or material declarations) | All EEE placed on EU market |
| EU Declaration of Conformity | Required before CE marking |
| CE marking | Required on product/packaging |
| Authorized representative (for non-EU manufacturers) | Required |
| Importer declaration | Required for EU importers |

---

## RoHS exemptions

Specific applications are exempt from certain substance restrictions. Exemptions are listed in Annex III (EEE) and Annex IV (medical devices/monitoring). Each exemption has an expiry date subject to renewal.

**Exemption management is DETERMINISTIC** — exemption must be:
- Numbered (Annex III or IV entry)
- Currently valid (not expired)
- Applicable to the product category

---

## REACH — key obligations

### Substance registration (manufacturers/importers ≥ 1 t/year)

| Obligation | Threshold | Confidence |
|---|---|---|
| Registration with ECHA | ≥ 1 tonne/year per substance | DETERMINISTIC |
| Chemical safety report | ≥ 10 tonnes/year for substances meeting hazard criteria | DETERMINISTIC |
| Registration number valid | Before placing substance on market | DETERMINISTIC |

### SVHC in articles — notification and communication duty

| Obligation | Threshold | Confidence |
|---|---|---|
| SVHC presence disclosure to customers | > 0.1% w/w in article | DETERMINISTIC |
| SVHC presence notification to ECHA (article notification) | > 0.1% w/w AND > 1 tonne/year placed on market | DETERMINISTIC |
| SVHC candidate list check | Biannual ECHA update | DETERMINISTIC schedule |

**SVHC candidate list** is updated by ECHA twice per year. Systems must re-check all products against new additions within a defined period (typically within 6 months of list update — DETERMINISTIC schedule).

### REACH SVHC — 0.1% calculation basis

The 0.1% threshold applies to:
- Each article as a whole (not homogeneous material, unlike RoHS)
- Per SVHC substance
- Per article

### Substances of Very High Concern (SVHC) authorization

Use of substances requiring authorization (Annex XIV) requires:
- ECHA authorization application before "sunset date"
- Use after sunset date without authorization = non-compliance (DETERMINISTIC)

---

## Supply chain information flow — DETERMINISTIC requirements

| Flow | Requirement | Confidence |
|---|---|---|
| Material declarations from suppliers | Required for RoHS and REACH compliance | DETERMINISTIC — no data = non-compliant |
| Full Materials Declaration (FMD) or RoHS Declaration | Per IEC 62474 or equivalent | PARAMETERIZED format; DETERMINISTIC requirement |
| IMDS (Automotive Material Data System) | Required for automotive supply chain | DETERMINISTIC for automotive OEM suppliers |
| SVHC above 0.1% — customer notification | Must inform customer "sufficient information to allow safe use" | DETERMINISTIC |

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Regulation |
|---|---|---|
| Lead (and other RoHS substances) | 0.1% w/w in homogeneous material | RoHS Annex II |
| Cadmium | 0.01% w/w in homogeneous material | RoHS Annex II |
| SVHC disclosure to customers | > 0.1% w/w in article | REACH Art. 33 |
| SVHC notification to ECHA | > 0.1% w/w AND > 1 t/year | REACH Art. 7(2) |
| REACH registration | ≥ 1 tonne/year | REACH Art. 6 |
| Authorized substance — sunset date compliance | Before sunset date | REACH Art. 56 |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Material declarations | RoHS, REACH, ISO 14001 §8.1, IATF 16949 | Same supplier material data collection |
| CE marking documentation | RoHS, EU MDR, Machinery Directive, Low Voltage Directive | Single technical file per product |
| Chemical management | REACH, ISO 14001 (aspects/impacts), OSHA 1910.1200 (HazCom) | Same chemical inventory |
| SVHC tracking | REACH, California Prop 65, TSCA (US equivalent) | Different substance lists; similar disclosure model |
| Supply chain transparency | RoHS/REACH, IATF 16949 supplier management, AS9100 §8.4 | Same supplier data portal |
