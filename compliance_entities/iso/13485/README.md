# ISO 13485:2016 — Medical Devices Quality Management System

**Authority:** ISO
**Scope:** Medical device manufacturers; required for EU MDR/IVDR CE marking; reference for FDA QMSR; recognized by Health Canada, TGA, ANVISA

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — 8 clauses, confidence map, 14 required records, cross-standard dependencies (FDA QMSR, EU MDR, ISO 14971) | ✅ |
| [`records-and-design-controls.md`](./records-and-design-controls.md) | DETERMINISTIC gates: 4.2 documentation system (quality manual, device file, record retention 2yr/lifetime+2yr), 7.3 design control (plan/inputs/outputs/reviews/V&V/transfer/changes/DHF), 7.4 supplier controls, 7.6 calibration, 8.2.2 complaint handling, 8.3 NC product, 8.5.2–8.5.3 CAPA | ✅ |
| [`management-and-product-controls.md`](./management-and-product-controls.md) | PARAMETERIZED: 4.1/5.1–5.2 management commitment + regulatory requirements identification, 6.2/6.4 competence + work environment, 7.1 product realization planning (ISO 14971 integration), 7.5.5/7.5.6 sterilization/special process validation, 8.2.1 post-market feedback, 8.4 data analysis | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Clause |
|---|---|---|
| Record retention minimum | max(2 years, device lifetime + 2 years) | 4.2.5 |
| Quality manual | Required; must include scope, exclusions, process interaction | 4.2.2 |
| Medical device file | One per device type | 4.2.3 |
| Design History File (DHF) | One per device type; full design control trail | 7.3.9 |
| Calibration traceability | Traceable to national/international standards | 7.6 |
| Complaint regulatory reporting determination | Required per complaint | 8.2.2 |
| CAPA effectiveness review | Required before CA closure | 8.5.2 |
| Documented procedures | ~22 explicitly required (vs zero mandated by name in ISO 9001:2015) | Various |

## Assumption count

| File | Assumptions |
|---|---|
| records-and-design-controls.md | 0 (all DETERMINISTIC) |
| management-and-product-controls.md | 9 |
| **Total** | **9** |

## Parse status: Complete — 2 spec files; 9 assumptions; records-focused file is fully DETERMINISTIC
