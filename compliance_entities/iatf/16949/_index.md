# IATF 16949:2016 — Automotive Quality Management System

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Quality management system requirements for automotive production and relevant service part organizations
**Authority:** International Automotive Task Force (IATF) — consortium of OEMs (BMW, Stellantis, Ford, GM, Volkswagen, Renault, Daimler) and their trade associations (AIAG, ANFIA, FIEV, SMMT, VDA)
**Enforcing context:** Tier 1, Tier 2, and Tier N suppliers to IATF subscribing OEMs; certification required as a condition of supply for most automotive production programs; enforced through OEM supplier qualification requirements
**Current edition:** IATF 16949:2016 (supersedes ISO/TS 16949:2009)
**Parent standard:** ISO 9001:2015 (IATF 16949 is a supplement; both must be satisfied simultaneously)

---

## Summary

| Metric | Count |
|---|---|
| Additional clauses beyond ISO 9001 | ~100 supplemental requirements embedded in or added to ISO 9001 clause structure |
| Customer-specific requirements (CSRs) | Per OEM — BMW, Ford, GM, Stellantis, VW, etc. publish separate CSRs that layer on top of IATF 16949 |
| AIAG Core Tools | 5 (APQP, PPAP, FMEA, MSA, SPC) — referenced throughout IATF 16949 |
| Requirements parsed (individual files) | 2 (ppap-and-product-controls.md + supplier-and-problem-solving.md — all major DETERMINISTIC clauses covered) |
| Fully automated (DETERMINISTIC) | Moderate — PPAP document completeness, control plan elements, gage R&R acceptance thresholds |
| Partial automation (PARAMETERIZED) | Dominant — core tool methodology adequacy |
| Human-determination required (CONTESTED) | Moderate — risk-based analysis in FMEA, customer-specific requirement interpretation |
| Open assumptions | 3 |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## IATF 16949 + ISO 9001 relationship

IATF 16949 does not stand alone. Each clause maps to ISO 9001:2015:
- ISO 9001 base clause → IATF 16949 supplemental requirements for that clause
- Both must be audited and certified simultaneously by an IATF-approved certification body (CB)
- ISO 9001-only certification does NOT satisfy IATF 16949 requirements

---

## AIAG Core Tools — the foundation of automotive QMS

IATF 16949 explicitly requires use of the AIAG core tools (or equivalent OEM-specific methodology). These are the primary PARAMETERIZED obligations:

| Tool | Abbreviation | When required | Purpose |
|---|---|---|---|
| Advanced Product Quality Planning | APQP | New product launch | Structured product development process; 5 phases with defined deliverables |
| Production Part Approval Process | PPAP | Before serial production | Supplier must submit evidence package demonstrating process capability before shipment |
| Failure Mode and Effects Analysis | FMEA | Design (DFMEA) and process (PFMEA) | Risk analysis of potential failure modes; RPN or AP (per AIAG-VDA FMEA 1st ed.) calculation |
| Measurement System Analysis | MSA | All measurement systems used for control | Gage R&R studies; Gauge Calibration; Measurement Uncertainty |
| Statistical Process Control | SPC | Production monitoring of special characteristics | Capability indices (Cpk ≥ 1.67 for special characteristics per most OEM CSRs) |

---

## Per-clause confidence map (IATF-specific additions to ISO 9001)

### Clause 4 — Context (IATF additions)

| Addition | Confidence | Notes |
|---|---|---|
| 4.3.1 Determining the scope — manufacturing site | DETERMINISTIC | Each manufacturing site must be independently certified; no site exclusions |
| 4.3.2 Customer-specific requirements | DETERMINISTIC | CSRs must be identified and included in QMS scope |

### Clause 5 — Leadership (IATF additions)

| Addition | Confidence | Notes |
|---|---|---|
| 5.1.1.1 Corporate responsibility | PARAMETERIZED | Corporate quality policy; quality objectives at top management |
| 5.1.1.2 Process effectiveness and efficiency | PARAMETERIZED | Top management review of performance indicators |
| 5.3.1 Organizational roles, responsibilities — supplemental | PARAMETERIZED | Customer-designated quality liaison; warranty claim analysis responsibility |

### Clause 6 — Planning (IATF additions)

| Addition | Confidence | Notes |
|---|---|---|
| 6.1.2.1 Risk analysis | PARAMETERIZED | Lessons learned considered; product safety considered |
| 6.1.2.3 Contingency plans | DETERMINISTIC | Written contingency plans for supply disruption; key manufacturing processes; utility outages; natural disasters |
| 6.2.2.1 Quality objectives and planning — supplemental | PARAMETERIZED | Customer performance metrics tracked |

### Clause 7 — Support (IATF additions)

| Addition | Confidence | Notes |
|---|---|---|
| 7.1.3.1 Plant, facility, and equipment planning | PARAMETERIZED | Multidisciplinary approach to plant layout; OEE (Overall Equipment Effectiveness) consideration |
| 7.1.4 Work environment supplement | PARAMETERIZED | Contamination control for product and process |
| 7.1.5.1 Measurement system analysis (MSA) | DETERMINISTIC | MSA studies required for all measurement systems used for control plan characteristics |
| 7.1.5.2 Calibration/verification records | DETERMINISTIC | Records of all calibration activities; traceable to national standards |
| 7.2.1 Competence — supplemental | DETERMINISTIC | On-the-job training for any new or modified responsibilities; records retained |
| 7.2.2 Competence — on-the-job training | PARAMETERIZED | Training effectiveness evaluated |
| 7.2.3 Internal auditor competency | DETERMINISTIC | Internal auditors must be qualified; product/process audit training required |
| 7.2.4 Second-party auditor competency | DETERMINISTIC | Supplier auditors must meet competency criteria |

### Clause 8 — Operation (IATF additions — highest DETERMINISTIC density)

| Addition | Confidence | Notes |
|---|---|---|
| 8.1.1 Operational planning and control — supplemental | DETERMINISTIC | Manufacturing feasibility assessment for each new program |
| 8.1.2 Confidentiality | PARAMETERIZED | Customer-designated confidential products/projects protected |
| 8.2.3.1 Review of requirements — supplemental | DETERMINISTIC | Manufacturing feasibility confirmed before acceptance |
| 8.3.2.1 Design and development planning — supplemental | DETERMINISTIC | Multidisciplinary team (MDT) required; APQP process required |
| 8.3.3.1 Product design inputs | DETERMINISTIC | Product design inputs include customer requirements, special characteristics, DFMEA, manufacturing feasibility |
| 8.3.3.2 Manufacturing process design input | DETERMINISTIC | Process design inputs include product special characteristics, manufacturing capability, manufacturing feasibility |
| 8.3.4.1 Monitoring of design and development | PARAMETERIZED | APQP milestone reviews |
| 8.3.4.2 Design and development validation — supplemental | DETERMINISTIC | Program approval before series production (PPAP or equivalent) |
| 8.3.5.1 Design and development outputs — supplemental | DETERMINISTIC | Design outputs include DFMEA, manufacturing process flow diagram, PFMEA, control plan, work instructions |
| 8.3.6.1 Design and development changes — supplemental | DETERMINISTIC | Customer change notification required for specified change types |
| 8.4.1.1 General — supplemental | DETERMINISTIC | Written supplier quality management system development process; 100% IATF 16949 preferred for Tier 2+; second-party audits required for non-certified Tier 2 suppliers |
| 8.4.1.2 Supplier selection process | PARAMETERIZED | Supplier selection criteria |
| 8.4.1.3 Customer-directed sources (directed buy) | PARAMETERIZED | Control of customer-directed suppliers |
| 8.4.2.1 Type and extent of control — supplemental | DETERMINISTIC | Supplier performance monitoring; supplier quality metrics tracked |
| 8.4.2.2 Statutory and regulatory requirements | DETERMINISTIC | Supplier required to flow down statutory/regulatory requirements |
| 8.4.2.3 Supplier quality management system development | DETERMINISTIC | Second-party audit or third-party certification required |
| 8.4.2.4 Supplier monitoring | DETERMINISTIC | Delivery performance (PPM), quality performance (PPM), IATF certification status monitored |
| 8.4.2.5 Supplier development | PARAMETERIZED | Supplier improvement process |
| 8.5.1.1 Control plan | DETERMINISTIC | Control plans required for prototype, pre-launch, and production phases; must reference all special characteristics; signed by customer if required by CSR |
| 8.5.1.2 Standardized work | DETERMINISTIC | Work instructions at each production station; operator instructions accessible |
| 8.5.1.3 Verification of job setups | DETERMINISTIC | First-off/last-off verification; records retained |
| 8.5.1.4 Verification after shutdown | PARAMETERIZED | Post-shutdown verification process |
| 8.5.1.5 Total productive maintenance | PARAMETERIZED | Documented TPM system; OEE tracked |
| 8.5.1.6 Management of production tooling | DETERMINISTIC | Tooling inventory; maintenance; replacement planning |
| 8.5.2.1 Identification and traceability — supplemental | DETERMINISTIC | Traceability throughout production; unique identification where required by CSR |
| 8.5.4.1 Preservation — supplemental | PARAMETERIZED | Inventory management; obsolescence management |
| 8.5.5.1 Service agreement with customer | PARAMETERIZED | Service agreement scope |
| 8.5.6.1 Production process changes — supplemental | DETERMINISTIC | Customer notification/approval before implementing specified change types |
| 8.5.6.1.1 Temporary change of process controls | DETERMINISTIC | Temporary changes documented; approved; reverted on defined date |
| 8.6.1 Release of products and services — supplemental | DETERMINISTIC | No production delivery without approved PPAP (or equivalent) |
| 8.6.2 Layout inspection and functional testing | DETERMINISTIC | Layout inspection per drawing at defined frequency (typically annual); records retained |
| 8.6.3 Appearance items | PARAMETERIZED | Appearance master samples maintained where applicable |
| 8.6.4 Verification and acceptance of conformance of externally provided products | DETERMINISTIC | Incoming inspection or alternative evidence of supplier conformance |
| 8.6.5 Statutory and regulatory conformity | DETERMINISTIC | All products meet applicable statutory and regulatory requirements |
| 8.6.6 Acceptance criteria | DETERMINISTIC | Acceptance criteria clearly defined; approved by customer for attribute sampling |
| 8.7.1.1 Customer notification | DETERMINISTIC | Customer notified of nonconforming product shipped |
| 8.7.1.2 Customer waiver | DETERMINISTIC | Customer waiver/deviation required before shipping known nonconforming product |
| 8.7.1.3 Control of nonconforming product — supplemental | DETERMINISTIC | Nonconforming product identified, segregated, and controlled |
| 8.7.1.4 Customer-owned nonconforming product | DETERMINISTIC | Customer-owned nonconforming product handled per customer requirements |
| 8.7.1.5 Control of suspect product | DETERMINISTIC | Suspect product controlled same as nonconforming |
| 8.7.1.6 Non-conforming product disposition | DETERMINISTIC | Reworked product re-inspected; records retained |
| 8.7.1.7 Nonconforming product on customer direction | PARAMETERIZED | Customer-directed use of nonconforming product documented |

### Clause 9 — Performance Evaluation (IATF additions)

| Addition | Confidence | Notes |
|---|---|---|
| 9.1.1.1 Monitoring and measurement of manufacturing processes | DETERMINISTIC | Process capability studies required for special characteristics; Cpk/Ppk tracked |
| 9.1.1.2 Statistical tools | PARAMETERIZED | Statistical tools appropriate for product/process |
| 9.1.1.3 Application of SPC | DETERMINISTIC | SPC applied to special characteristics; Cpk ≥ 1.67 (or per CSR) |
| 9.1.2.1 Customer satisfaction — supplemental | DETERMINISTIC | Customer PPM, warranty, field returns, customer scorecards monitored |
| 9.2.2.1 Internal audit program | DETERMINISTIC | Annual internal audit program; QMS audit, manufacturing process audit, product audit — all required; audit coverage of all processes, all shifts |
| 9.3.2.1 Management review inputs — supplemental | DETERMINISTIC | Mandatory additional inputs including customer portal data, warranty, field returns, lessons learned |

### Clause 10 — Improvement (IATF additions)

| Addition | Confidence | Notes |
|---|---|---|
| 10.2.3 Problem solving | DETERMINISTIC | Structured problem solving (8D or equivalent) required; root cause analysis |
| 10.2.4 Error-proofing (poka-yoke) | DETERMINISTIC | Error-proofing devices in control plan tested at defined frequency; records retained |
| 10.2.5 Warranty management system | DETERMINISTIC | Warranty analysis process; No Trouble Found (NTF) analysis |
| 10.2.6 Customer complaints and field failure test analysis | DETERMINISTIC | Customer complaint response; field failure analysis; test records retained |
| 10.3.1 Continual improvement — supplemental | PARAMETERIZED | Documented continual improvement process for manufacturing |

---

## PPAP — Production Part Approval Process (key DETERMINISTIC checklist)

PPAP is a formal submission proving a supplier can produce product meeting customer requirements at stated production rates. The 18 PPAP elements:

| # | Element | Confidence |
|---|---|---|
| 1 | Design Records | DETERMINISTIC |
| 2 | Authorized Engineering Change Documents | DETERMINISTIC |
| 3 | Customer Engineering Approval | DETERMINISTIC |
| 4 | Design FMEA | DETERMINISTIC |
| 5 | Process Flow Diagram | DETERMINISTIC |
| 6 | Process FMEA | DETERMINISTIC |
| 7 | Control Plan | DETERMINISTIC |
| 8 | Measurement System Analysis Studies (MSA) | DETERMINISTIC |
| 9 | Dimensional Results | DETERMINISTIC |
| 10 | Records of Material/Performance Test Results | DETERMINISTIC |
| 11 | Initial Process Studies (SPC/Cpk) | DETERMINISTIC |
| 12 | Qualified Laboratory Documentation | DETERMINISTIC |
| 13 | Appearance Approval Report (AAR) | DETERMINISTIC (if appearance item) |
| 14 | Sample Production Parts | DETERMINISTIC |
| 15 | Master Sample | DETERMINISTIC |
| 16 | Checking Aids | DETERMINISTIC |
| 17 | Customer-Specific Requirements | DETERMINISTIC |
| 18 | Part Submission Warrant (PSW) | DETERMINISTIC |

PPAP level (1–5) determines which elements must be submitted to the customer vs. retained on-site.

---

## Open assumption registry

| ID | File | Clause | Summary | Review date |
|---|---|---|---|---|
| ASSUME-IATF-MSA-001 | ppap-and-product-controls.md | 7.1.5.1 | MSA acceptance: %R&R ≤10% acceptable, ≤30% marginal; ndc ≥5; kappa ≥0.75 attribute | 2027-05-21 |
| ASSUME-IATF-SUPP-001 | supplier-and-problem-solving.md | 8.4.2.5 | Supplier development: targets defined; at-risk suppliers escalated; thresholds in SQM | 2027-05-21 |
| ASSUME-IATF-MGMT-001 | supplier-and-problem-solving.md | 9.3.2.1 | Management review: all IATF inputs incl. customer portal, warranty, field returns, NPI lessons | 2027-05-21 |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| ISO 9001 QMS base | IATF 16949 (parent), AS9100 (parent for aerospace), ISO 13485 (parent for medical devices) | Same underlying management system; sector-specific additions layered on top |
| FMEA | IATF 16949 §8.3.3, AS9100 (risk management), EU MDR Annex I §3 (risk management) | All require risk analysis; AIAG-VDA FMEA 1st edition is the current automotive methodology |
| Control plan | IATF 16949 §8.5.1.1, AS9100 (first article inspection) | Control plan format is automotive-specific; AS9100 first article achieves similar traceability |
| Calibration records | IATF 16949 §7.1.5.2, ISO 9001 §7.1.5.2, AS9100 §7.1.5.2 | Identical requirements across all three |
| CAPA | IATF 16949 §10.2, ISO 9001 §10.2, AS9100 §10.2 | IATF requires structured problem solving (8D); AS9100 requires root cause analysis with verification |
| Supplier qualification | IATF 16949 §8.4.1–8.4.2, AS9100 §8.4, ISO 13485 §7.4 | All require approved supplier lists with evaluation records |
