# AS9100 Rev D — Aerospace Quality Management System

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Quality management system requirements for aviation, space, and defense organizations
**Authority:** International Aerospace Quality Group (IAQG) — consortium of OEMs (Boeing, Airbus, Lockheed Martin, Raytheon, GE Aerospace, Rolls-Royce, etc.) and their trade associations (AAQG, EAQG, APAQG)
**Enforcing context:** Suppliers to major aerospace/defense OEMs and primes; required for NADCAP certification programs; mandated by AS9100 subscribing OEMs as a condition of supply; required for FAA/EASA Part 21 production approval holders in many cases
**Current edition:** AS9100 Rev D (2016, aligned to ISO 9001:2015)
**Parent standard:** ISO 9001:2015 (AS9100 is a supplement; both must be satisfied simultaneously)
**Note:** The AS91XX series includes: AS9100 (manufacturers), AS9110 (maintenance/MRO), AS9120 (distributors). This registry covers AS9100.

---

## Summary

| Metric | Count |
|---|---|
| Additional requirements beyond ISO 9001 | ~100 supplemental requirements |
| Aerospace-specific domains | Key characteristics, FOD prevention, first article inspection, counterfeit part control, human factors |
| Customer-specific requirements | Per OEM/prime — Boeing D6-82479, Airbus AP2026, Lockheed Martin, etc. |
| Requirements parsed (individual files) | 0 (index only; individual clause files pending) |
| Fully automated (DETERMINISTIC) | Moderate — FAI completeness, counterfeit part controls, FOD inspection records |
| Partial automation (PARAMETERIZED) | Dominant — risk management adequacy, key characteristic identification |
| Human-determination required (CONTESTED) | Moderate — key characteristic scope, airworthiness impact assessment |
| Open assumptions | 0 |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Aerospace-specific concepts

### Key Characteristics (KCs)

A **Key Characteristic** is a feature of a material, process, or part whose variation has a significant influence on product fit, performance, service life, or producibility.

- KCs designated by customer drawing, specification, or mutual agreement
- KCs must be identified in control plans, FMEAs, work instructions
- KCs require statistical process control or 100% inspection at production
- KC identification is PARAMETERIZED; KC monitoring once identified is DETERMINISTIC

### Foreign Object Damage/Debris (FOD) Prevention

FOD refers to any substance, debris, or article that is alien to the vehicle, system, or assembly that could potentially cause damage. FOD in aerospace causes catastrophic failures.

- Written FOD prevention program required
- FOD inspections at defined stages; records retained
- FOD training for all production personnel

### First Article Inspection (FAI)

FAI is a physical and functional inspection of the first production item (or first item after design/process change) to verify all engineering, design, and specification requirements are met.

- AS9102 defines the FAI procedure
- Required for new parts, re-sourced parts, and after significant process changes
- Three forms: Part Number Accountability (Form 1), Product Accountability — Material/Test Results (Form 2), Characteristic Accountability/Verification (Form 3)
- FAI records retained for part life

### Counterfeit Part Prevention

Counterfeit parts are those that have been fraudulently misrepresented as to their identity or origin. Counterfeit electronic parts are a significant risk in aerospace supply chains.

- Written counterfeit parts prevention process required
- Approved supplier list controls
- Suspect/counterfeit parts segregated, documented, reported
- Traceability of parts to original manufacturer

---

## Per-clause confidence map (AS9100-specific additions to ISO 9001)

### Clause 4 — Context

| Addition | Confidence | Notes |
|---|---|---|
| 4.1 — Organizational knowledge includes safety issues | PARAMETERIZED | Safety lessons learned considered in context analysis |
| 4.4.1 — QMS includes product/service safety | DETERMINISTIC | Product safety explicitly identified as a QMS requirement |

### Clause 5 — Leadership

| Addition | Confidence | Notes |
|---|---|---|
| 5.1.1(h) — Top management communicates importance of ethics | PARAMETERIZED | Ethics policy; reporting of concerns |
| 5.1.1(i) — Top management establishes safety culture | PARAMETERIZED | Safety culture evidenced in management behavior |
| 5.3(e)–(f) — Roles for product safety and FOD | DETERMINISTIC | Named responsibility for product safety and FOD prevention |

### Clause 6 — Planning

| Addition | Confidence | Notes |
|---|---|---|
| 6.1.1(c) — Consider statutory/regulatory compliance in risks | DETERMINISTIC | FAA/EASA/DCSA regulatory requirements explicitly in scope |
| 6.1.2.1 — Risk management process | PARAMETERIZED | Documented risk management plan; risk identification, assessment, treatment, monitoring |
| 6.1.2.3 — Configuration management | DETERMINISTIC | Configuration management plan required; changes controlled and traceable |
| 6.1.2.4 — Product safety | DETERMINISTIC | Processes to promote and maintain safety culture; training; safety issues escalated to customer/regulator |

### Clause 7 — Support

| Addition | Confidence | Notes |
|---|---|---|
| 7.1.3.1 — Awareness of contribution to safety | PARAMETERIZED | Personnel aware of contribution to product safety |
| 7.1.4 — Product and process verification resources | PARAMETERIZED | Verification resources commensurate with risk |
| 7.1.5.1 — Control of calibration/measuring equipment | DETERMINISTIC | Same as ISO 9001; records retained; traceable |
| 7.2(e)–(f) — Human factors, ethics awareness | PARAMETERIZED | Human factors training; awareness of consequences of nonconformance |
| 7.5.1 — Documentation includes key characteristics | DETERMINISTIC | Work instructions reference key characteristics |

### Clause 8 — Operation

| Addition | Confidence | Notes |
|---|---|---|
| 8.1.1 — Operational risk management | PARAMETERIZED | Risks assessed and mitigated at operational level |
| 8.1.2 — Configuration management | DETERMINISTIC | All products under configuration control; configuration documentation controlled; change authorization |
| 8.1.3 — Product safety | DETERMINISTIC | Classification of characteristics for safety-critical items; training on safety implications |
| 8.1.4 — Prevention of counterfeit parts | DETERMINISTIC | Written counterfeit prevention process; approved suppliers; suspect/counterfeit part reporting |
| 8.2.3.1 — Review of requirements — supplemental | DETERMINISTIC | Ability to meet requirements confirmed; risks assessed |
| 8.3.2.1 — Design and development planning | DETERMINISTIC | Multidisciplinary approach; risk and configuration management integrated |
| 8.3.3.1 — Product design inputs | DETERMINISTIC | Design inputs include: regulatory requirements, product safety, risk analysis outputs, key characteristics, FMEAs |
| 8.3.4.1 — Monitoring of design and development | DETERMINISTIC | Design reviews; verification of design objectives; risk review |
| 8.3.4.3 — Special requirements, critical items, key characteristics | DETERMINISTIC | Identification and flow-down of special requirements; key characteristics identified in design outputs |
| 8.3.5.1 — Design and development outputs — supplemental | DETERMINISTIC | Design outputs include: key characteristics, product definition, airworthiness data |
| 8.3.6.1 — Design changes — supplemental | DETERMINISTIC | Airworthiness impact of changes assessed; customer/regulator notification for significant changes |
| 8.4.1 — Control of external providers | DETERMINISTIC | Approved supplier list; supplier evaluation includes product safety consideration |
| 8.4.2.1 — External provider process controls | DETERMINISTIC | Flow-down of all applicable requirements including key characteristics, special requirements |
| 8.4.3.1 — Purchasing information — supplemental | DETERMINISTIC | Purchase orders specify: design/manufacturing requirements, key characteristics, special process requirements, configuration |
| 8.5.1.1 — Control plan (implied via key characteristics) | DETERMINISTIC | Control plans reference all key characteristics; inspection and test at defined frequencies |
| 8.5.1.2 — Work instructions | DETERMINISTIC | Work instructions for all processes affecting product conformance; reference key characteristics |
| 8.5.2 — Identification and traceability | DETERMINISTIC | Traceability to original manufacturer for all safety-critical parts; lot traceability |
| 8.5.4 — Preservation | PARAMETERIZED | Preservation per applicable specifications (shelf life, storage conditions, ESD protection) |
| 8.5.5 — Post-delivery activities | PARAMETERIZED | Field service; customer feedback; warranty |
| 8.5.6 — Control of changes | DETERMINISTIC | Change impact on airworthiness assessed; customer notification per contract |
| 8.6.1 — Release of products and services — supplemental | DETERMINISTIC | First article inspection required before production release |
| 8.6.2 — First article inspection | DETERMINISTIC | FAI per AS9102 required for new/changed products; all 3 forms completed and retained |
| 8.7.1 — Control of nonconforming outputs — supplemental | DETERMINISTIC | Safety implication assessed; customer/regulatory reporting for product safety nonconformances |
| 8.7.3 — Nonconforming output disposition | DETERMINISTIC | Disposition authority defined; use-as-is requires engineering justification; scrap documented |

### Clause 9 — Performance Evaluation

| Addition | Confidence | Notes |
|---|---|---|
| 9.1.1.1 — Monitoring of manufacturing processes | DETERMINISTIC | Key characteristics monitored per control plan; SPC or 100% inspection |
| 9.2.2.1 — Internal audit program | DETERMINISTIC | Annual audit program; product audits, process audits, QMS audits — all required; all shifts covered |
| 9.3.2.1 — Management review inputs — supplemental | DETERMINISTIC | Mandatory inputs include: customer scorecard data, safety-related issues, configuration changes, regulatory updates |

### Clause 10 — Improvement

| Addition | Confidence | Notes |
|---|---|---|
| 10.2.1(f)–(g) — CAPA — supplemental | DETERMINISTIC | Root cause analysis required; verification of effectiveness; escalation for safety-related NCRs |
| 10.2.2 — CAPA records | DETERMINISTIC | Records retained for part life or as defined |
| 10.3.1 — Continual improvement | PARAMETERIZED | Documented continual improvement process |

---

## FAI (First Article Inspection) — AS9102 checklist structure

| Form | Contents | Confidence |
|---|---|---|
| Form 1 — Part Number Accountability | Part number, revision, drawing approval, design documentation | DETERMINISTIC |
| Form 2 — Product Accountability (Materials/Test Results) | Raw material certifications, process approvals, test reports, special process certs | DETERMINISTIC |
| Form 3 — Characteristic Accountability/Verification | All dimensional characteristics on drawing measured and recorded; key characteristics identified | DETERMINISTIC |

FAI completion and approval is a DETERMINISTIC gate before production shipment.

---

## Open assumption registry

*(No assumptions recorded — individual clause files not yet written)*

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| ISO 9001 QMS base | AS9100 (parent), IATF 16949 (automotive equivalent), ISO 13485 (medical device equivalent) | Same underlying management system; sector-specific additions layered on top |
| First Article Inspection | AS9100 §8.6.2, IATF 16949 §8.6.1 (PPAP equivalent), FDA QMSR §820.80 (device acceptance) | AS9102 FAI is the most formally structured; PPAP achieves the same purpose for automotive |
| Key characteristics | AS9100 §8.3.3.1, IATF 16949 (special characteristics), ISO 13485 §7.3.2 (essential requirements) | Different terminology; same risk-based critical attribute concept |
| Counterfeit part control | AS9100 §8.1.4, DFARS 252.246-7007 (DoD counterfeit parts rule), SAE AS5553 | AS9100 requires a process; DFARS makes it mandatory for DoD contractors; SAE AS5553 defines the detailed process |
| Configuration management | AS9100 §8.1.2, IATF 16949 §8.5.6.1 (process change control), DO-178C/DO-254 (software/hardware) | Configuration control is universal; AS9100 is the most explicit about configuration management as a standalone process |
| CAPA with safety escalation | AS9100 §10.2, FAA/EASA airworthiness reporting, EU MDR vigilance | AS9100 requires safety-related NCRs to be escalated; FAA/EASA have specific reportable event criteria |
| Calibration | AS9100 §7.1.5, ISO 9001 §7.1.5, IATF 16949 §7.1.5, ISO 13485 §7.6 | Identical requirements |
