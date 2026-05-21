# ISO 13485:2016 — Medical Devices Quality Management System

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** All clauses 4–8; QMS for design, development, production, installation, and servicing of medical devices and related services
**Authority:** International Organization for Standardization (ISO)
**Enforcing context:** Medical device manufacturers worldwide; required for EU MDR/IVDR CE marking; recognized by FDA as a reference for 21 CFR Part 820 (QMSR); required by Health Canada, TGA, ANVISA, and most national regulatory authorities
**Current edition:** ISO 13485:2016 (aligned to but NOT harmonized with ISO 9001:2015 — uses different structure)
**Parent standard:** ISO 9001 (see iso/9001 registry); 13485 is more prescriptive and does not adopt ISO 9001's risk-based thinking flexibility

---

## Summary

| Metric | Count |
|---|---|
| Clauses | 8 (Clauses 1–8) |
| Sub-clauses with discrete requirements | ~80 |
| Sub-clauses parsed (individual files) | 2 (records-and-design-controls.md + management-and-product-controls.md) |
| Fully automated (DETERMINISTIC) | Moderate — DHF/device file, complaint records, CAPA records, calibration, record retention gate |
| Partial automation (PARAMETERIZED) | Dominant |
| Human-determination required (CONTESTED) | Low — risk management method adequacy requires human review (not tested directly) |
| Open assumptions | 9 |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Critical distinction from ISO 9001

ISO 13485 is **not** a subset of ISO 9001:2015. Key differences:
- ISO 13485 retains a prescriptive, documented-procedure approach (ISO 9001:2015 does not require "procedures")
- ISO 13485 does not adopt "risk-based thinking" as a free-form concept — risk management is explicitly required per ISO 14971
- ISO 13485 adds regulatory compliance as an explicit requirement throughout
- ISO 13485 has additional requirements for sterile medical devices, software, and implantable devices

---

## Per-clause confidence map

### Clause 4 — Quality Management System

| Sub-clause | Requirement | Confidence | Notes |
|---|---|---|---|
| 4.1 | General QMS requirements | PARAMETERIZED | Documented QMS; outsourced processes controlled |
| 4.2.1 | Documentation requirements (general) | DETERMINISTIC | Quality manual required; documented procedures; records |
| 4.2.2 | Quality manual | DETERMINISTIC | Must include scope, exclusions, procedures or references, and process interaction description |
| 4.2.3 | Medical device file | DETERMINISTIC | Device file (technical file) maintained for each device type; all documents demonstrating conformity to requirements |
| 4.2.4 | Control of documents | DETERMINISTIC | Document control procedure required; approval, review, changes, external documents, obsolete documents |
| 4.2.5 | Control of records | DETERMINISTIC | Records legible, identifiable, retrievable; retention period defined; minimum 2 years or lifetime of device + 2 years (whichever greater) |

### Clause 5 — Management Responsibility

| Sub-clause | Requirement | Confidence | Notes |
|---|---|---|---|
| 5.1 | Management commitment | PARAMETERIZED | Top management demonstrable commitment to QMS and regulatory requirements |
| 5.2 | Customer focus | PARAMETERIZED | Customer and regulatory requirements determined and met |
| 5.3 | Quality policy | DETERMINISTIC | Written policy; commitment to compliance; objectives framework; reviewed for suitability |
| 5.4.1 | Quality objectives | DETERMINISTIC | Documented quality objectives at relevant functions/levels; measurable |
| 5.4.2 | Quality planning | PARAMETERIZED | QMS integrity maintained during changes |
| 5.5 | Responsibility and authority | DETERMINISTIC | Roles, responsibilities, authorities defined and communicated; management representative designated |
| 5.6 | Management review | DETERMINISTIC | Planned intervals; inputs/outputs defined; records retained |

### Clause 6 — Resource Management

| Sub-clause | Requirement | Confidence | Notes |
|---|---|---|---|
| 6.1 | Provision of resources | PARAMETERIZED | Resources for QMS implementation and regulatory compliance |
| 6.2 | Human resources | DETERMINISTIC | Competence based on education, training, skills, experience; training effectiveness evaluated; records retained |
| 6.3 | Infrastructure | PARAMETERIZED | Buildings, workspace, equipment, services maintained |
| 6.4.1 | Work environment | PARAMETERIZED | Conditions controlled; personnel health and cleanliness requirements defined |
| 6.4.2 | Contamination control | PARAMETERIZED | Arrangements for controlling contaminated or potentially contaminated product |

### Clause 7 — Product Realization

This is the most complex clause and the primary source of DETERMINISTIC requirements unique to 13485.

| Sub-clause | Requirement | Confidence | Notes |
|---|---|---|---|
| 7.1 | Planning of product realization | PARAMETERIZED | Quality plans; risk management integration per ISO 14971 |
| 7.2.1 | Determination of product requirements | DETERMINISTIC | Requirements include performance, regulatory, statutory/regulatory, applicable standards; documented |
| 7.2.2 | Review of product requirements | DETERMINISTIC | Review before commitment; records retained |
| 7.2.3 | Customer communication | PARAMETERIZED | Communication on product info, enquiries, complaints |
| 7.3.1 | Design and development planning | DETERMINISTIC | Design plan documents stages, review/verification/validation activities, responsibilities; updated as design evolves |
| 7.3.2 | Design and development inputs | DETERMINISTIC | Inputs documented and reviewed; include functional/performance requirements, applicable regulatory requirements, risk management outputs, previous design information |
| 7.3.3 | Design and development outputs | DETERMINISTIC | Outputs meet inputs; approved before release; provide manufacturing/servicing information; reference acceptance criteria |
| 7.3.4 | Design and development review | DETERMINISTIC | Reviews at suitable stages; participants include functions concerned with stage; records retained |
| 7.3.5 | Design and development verification | DETERMINISTIC | Verification performed to ensure outputs meet inputs; records retained |
| 7.3.6 | Design and development validation | DETERMINISTIC | Validation before delivery; includes clinical evaluation/usability validation where applicable; records retained |
| 7.3.7 | Transfer to manufacturing | DETERMINISTIC | Design transfer verified that design outputs are suitable for manufacturing before becoming production specification |
| 7.3.8 | Control of design and development changes | DETERMINISTIC | Changes identified, reviewed, verified, validated before implementation; records retained |
| 7.3.9 | Design and development files (DHF) | DETERMINISTIC | Design History File maintained for each device type demonstrating QMS compliance |
| 7.4.1 | Purchasing process | DETERMINISTIC | Supplier evaluation and selection based on criteria; records of evaluation retained |
| 7.4.2 | Purchasing information | DETERMINISTIC | Purchase orders specify requirements; reviewed and approved before release |
| 7.4.3 | Verification of purchased product | DETERMINISTIC | Inspection/verification activities defined; records retained |
| 7.5.1 | Control of production and service provision | DETERMINISTIC | Documented procedures/work instructions where absence would adversely affect quality; monitoring and measurement equipment used; equipment validated; release/delivery/post-delivery activities controlled |
| 7.5.2 | Cleanliness of product | PARAMETERIZED | Product cleanliness requirements documented if product cleaned before sterilization or is supplied sterile |
| 7.5.3.1 | Installation activities | PARAMETERIZED | Installation and verification criteria documented if applicable |
| 7.5.3.2 | Servicing activities | PARAMETERIZED | Service procedures, reference materials, measurement techniques documented if applicable |
| 7.5.4 | Servicing requirements | DETERMINISTIC | Records of servicing activities retained |
| 7.5.5 | Particular requirements for sterile medical devices | DETERMINISTIC | Sterilization processes validated; validated sterilization records retained |
| 7.5.6 | Validation of processes for production and service provision | DETERMINISTIC | Processes where output cannot be verified by subsequent monitoring must be validated; records retained |
| 7.5.7 | Particular requirements for validation of processes for sterilization and sterile barrier systems | DETERMINISTIC | Sterilization validation records retained |
| 7.5.8 | Identification | DETERMINISTIC | Product identified throughout production and service; suitable means of identification used |
| 7.5.9 | Traceability | DETERMINISTIC | Traceability records as required by regulatory requirements; implantable devices: unique identification records retained for defined period |
| 7.5.10 | Customer property | PARAMETERIZED | Customer-provided components identified, verified, protected, safeguarded |
| 7.5.11 | Preservation of product | PARAMETERIZED | Preservation methods documented; storage conditions defined and monitored |
| 7.6 | Control of monitoring and measuring equipment | DETERMINISTIC | Calibration records; calibrated against traceable standards; calibration status visible; protected; software validation |

### Clause 8 — Measurement, Analysis, and Improvement

| Sub-clause | Requirement | Confidence | Notes |
|---|---|---|---|
| 8.1 | General | PARAMETERIZED | Monitoring, measurement, analysis, improvement processes planned and implemented |
| 8.2.1 | Feedback | DETERMINISTIC | Feedback system to provide early warning of quality problems; data included in management review |
| 8.2.2 | Complaint handling | DETERMINISTIC | Documented complaint handling procedure; records of all complaints retained; investigation performed; regulatory reporting determination made |
| 8.2.3 | Reporting to regulatory authorities | DETERMINISTIC | Reportable events reported to relevant regulatory authorities in defined timeframes |
| 8.2.4 | Internal audit | DETERMINISTIC | Planned audit program; auditor independence; corrective actions without undue delay; records retained |
| 8.2.5 | Monitoring and measurement of processes | PARAMETERIZED | Methods to demonstrate process conformity; corrective action when planned results not achieved |
| 8.2.6 | Monitoring and measurement of product | DETERMINISTIC | Evidence of conformity with acceptance criteria documented; records identify person authorizing release |
| 8.3.1 | Control of nonconforming product (general) | DETERMINISTIC | Documented procedure; identification, documentation, segregation, evaluation, and disposition; notification to customers and regulators where required |
| 8.3.2 | Actions in response to nonconforming product detected before delivery | DETERMINISTIC | Disposition documented |
| 8.3.3 | Actions in response to nonconforming product detected after delivery | DETERMINISTIC | Complaint handling and potential field action evaluated; regulatory reporting determination made |
| 8.3.4 | Rework | DETERMINISTIC | Rework documented; effect of rework on product assessed; rework instructions reviewed and approved |
| 8.4 | Analysis of data | PARAMETERIZED | Appropriate data collected and analyzed; feedback, conformity, supplier characteristics, audits |
| 8.5.1 | Improvement — general | PARAMETERIZED | Changes in regulatory requirements; customer feedback; complaints; regulatory reporting; internal audits |
| 8.5.2 | Corrective action | DETERMINISTIC | Documented CAPA procedure; root cause analysis; evidence corrective actions do not adversely affect ability to meet requirements; records retained |
| 8.5.3 | Preventive action | DETERMINISTIC | Documented preventive action procedure; records retained |

---

## Key DETERMINISTIC record requirements

| Record | Sub-clause |
|---|---|
| Design History File (DHF) | 7.3.9 |
| Design inputs/outputs/reviews/verification/validation | 7.3.2–7.3.6 |
| Design transfer verification | 7.3.7 |
| Design change records | 7.3.8 |
| Supplier evaluation records | 7.4.1 |
| Sterilization validation records | 7.5.5, 7.5.7 |
| Process validation records | 7.5.6 |
| Traceability records (implantable devices) | 7.5.9 |
| Calibration records | 7.6 |
| Complaint records | 8.2.2 |
| Regulatory reporting determination records | 8.2.3 |
| Nonconforming product records | 8.3.1 |
| Corrective action records | 8.5.2 |
| Preventive action records | 8.5.3 |

---

## Open assumption registry

See [`management-and-product-controls.md`](./management-and-product-controls.md) for 9 PARAMETERIZED assumptions (ASSUME-ISO13485-5_1-001 through 8_4-001).

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Design History File (DHF) | ISO 13485 §7.3.9, FDA 21 CFR Part 820/QMSR §820.30, EU MDR Annex II Technical Documentation | Same underlying records; different names and format requirements. QMSR DHF + EU MDR Tech Doc are the three primary regulatory targets |
| Risk management file | ISO 13485 §7.1 (risk management per ISO 14971), EU MDR Article 10(2), FDA QMSR §820.30(g) | ISO 14971 risk management file is the shared artifact; each regulatory system has slightly different required inputs |
| Complaint handling | ISO 13485 §8.2.2, FDA 21 CFR Part 820/QMSR §820.198, EU MDR Article 87 (vigilance) | Same complaint records; different regulatory reporting thresholds and timelines |
| CAPA | ISO 13485 §8.5.2–8.5.3, FDA QMSR §820.100, EU MDR Article 10(9) | Same CAPA process; QMSR adds trending requirement |
| Supplier controls | ISO 13485 §7.4, FDA QMSR §820.50, EU MDR Article 10(2) | Same supplier evaluation records; QMSR adds critical supplier designation |
| Calibration records | ISO 13485 §7.6, ISO 9001 §7.1.5.2, FDA 21 CFR Part 820 §820.72 | Same calibration records; traceable to national standards |
