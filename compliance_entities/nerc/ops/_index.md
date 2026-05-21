# NERC Reliability Standards (Non-CIP) — Operating and Planning Standards

**Registry version:** 2026.05
**Last updated:** 2026-05-21
**Scope:** NERC enforceable reliability standards excluding CIP-002–CIP-015; covers bulk electric system (BES) operations, planning, protection, vegetation management, and emergency preparedness
**Authority:** North American Electric Reliability Corporation (NERC); enforced by Regional Entities (RE) under FERC oversight (U.S.); NEB oversight (Canada)
**Enforcing context:** Transmission Owners (TO), Transmission Operators (TOP), Balancing Authorities (BA), Reliability Coordinators (RC), Generator Owners (GO), Generator Operators (GOP), Distribution Providers (DP), and Planning Coordinators (PC) — each standard specifies applicable functional entities
**Note:** CIP standards are maintained in `nerc/cip/` — this index covers all non-CIP NERC standards

---

## Summary

| Metric | Count |
|---|---|
| Non-CIP standard categories | 14 (BAL, COM, EOP, FAC, INT, IRO, MOD, NUC, PER, PRC, TOP, TPL, VAR, plus legacy) |
| Enforceable standards (active) | ~90+ individual standards across all categories |
| Standards parsed (individual files) | 5 (prc-protection-control.md; fac-eop-operations.md; com-top-operations.md; per-bal-personnel.md; mod-tpl-eop-planning.md) |
| Fully automated (DETERMINISTIC) | Moderate — maintenance intervals (PRC-005), vegetation patrol (FAC-003), event reporting (EOP-004), three-part communication (COM-002), operator credentials (PER-003), frequency response obligation (BAL-003), blackstart test cycle (EOP-005) |
| Partial automation (PARAMETERIZED) | Dominant — planning event adequacy (TPL-001), model validation (MOD-025), relay coordination (PRC-023), corrective action timeframes (TOP-001) |
| Human-determination required (CONTESTED) | Significant — ratings methodology adequacy (FAC-008), P3–P7 extreme event acceptability (TPL-001), restoration procedure sufficiency (EOP-005) |
| Open assumptions | 17 (ASSUME-NERC-PRC-001–004, FAC-001–002, EOP-001–002, COM-001, TOP-001, PER-001–002, BAL-001, MOD-001, TPL-001, EOP-001–002 planning) |
| Stale reviews | 0 |

---

## Standard categories and confidence map

### BAL — Balancing and Frequency Control

| Standard | Title | Confidence | Key obligation |
|---|---|---|---|
| BAL-001-2 | Real Power Balancing Control Performance | PARAMETERIZED | Control performance criteria (CPS1/CPS2) — compliance period-based |
| BAL-002-3 | Disturbance Control Standard – Balancing Resources | PARAMETERIZED | Recovery to scheduled frequency within 15 minutes |
| BAL-003-1 | Frequency Response and Frequency Bias Setting | DETERMINISTIC | BA frequency response obligation (FRO) in MW — calculated by NERC annually |
| BAL-004-0 | Time Error Correction | PARAMETERIZED | Time error correction process |
| BAL-005-1 | Automatic Generation Control | PARAMETERIZED | AGC frequency deviation criteria |
| BAL-006-2 | Inadvertent Interchange | PARAMETERIZED | Inadvertent interchange accounting |

### COM — Communications

| Standard | Title | Confidence | Key obligation |
|---|---|---|---|
| COM-001-3 | Telecommunications | DETERMINISTIC | Redundant, reliable communications capability for RC/TOP/BA operations |
| COM-002-4 | Operating Personnel Communications Protocols | DETERMINISTIC | Three-part communication (issuer / receiver / repeat-back) for all directives |

### EOP — Emergency Preparedness and Operations

| Standard | Title | Confidence | Key obligation |
|---|---|---|---|
| EOP-004-4 | Event Reporting | DETERMINISTIC | Specific event categories → reporting timelines (1-hour oral / 24-hour written) |
| EOP-005-3 | System Restoration from Blackstart Resources | PARAMETERIZED | Blackstart resources tested every 3 years; procedures validated |
| EOP-006-3 | Reliability Coordinator Procedures During a Transmission Emergency | PARAMETERIZED | RC procedure adequacy |
| EOP-008-2 | Loss of Control Center Functionality | PARAMETERIZED | Backup control center designation and capability |
| EOP-011-3 | Emergency Operations | PARAMETERIZED | BA/TOP/RC emergency operations procedures |

### FAC — Facility Design, Connections, and Maintenance

| Standard | Title | Confidence | Key obligation |
|---|---|---|---|
| FAC-001-3 | Facility Connection Requirements | PARAMETERIZED | TO establishes connection requirements; annual review |
| FAC-002-3 | Facility or Meter Data for the Actual or Proposed Data for Interconnecting Facilities | PARAMETERIZED | Data provided within specified timeframes |
| FAC-003-4 | Transmission Vegetation Management | DETERMINISTIC | Annual patrol; MVCD clearances; 4-year cycle for detailed inspection |
| FAC-008-3 | Facility Ratings | DETERMINISTIC (existence) / PARAMETERIZED (methodology) | Written ratings methodology; ratings consistent with methodology; provided to planning/operations on request |

### INT — Interchange Scheduling and Coordination

| Standard | Title | Confidence | Key obligation |
|---|---|---|---|
| INT-004-3.1 | Dynamic Transfers | PARAMETERIZED | AGC capability verification |
| INT-006-4 | Evaluation of Interchange Transactions | PARAMETERIZED | Curtailment protocol |
| INT-009-2 | Implementation of Interchange | DETERMINISTIC | No unauthorized energy transfers |
| INT-010-2 | Interchange Initiation and Modification for Adjacent Balancing Authorities | PARAMETERIZED | Confirmation protocol |

### IRO — Interconnection Reliability Operations and Coordination

| Standard | Title | Confidence | Key obligation |
|---|---|---|---|
| IRO-001-5 | Reliability Coordination — Responsibilities and Authorities | DETERMINISTIC | RC has authority to issue directives; TOP/BA must comply |
| IRO-002-6 | Reliability Coordination — Monitoring and Analysis | PARAMETERIZED | Monitoring capability for real-time operations |
| IRO-006-5 | Reliability Coordination — System Restoration | PARAMETERIZED | RC system restoration plan |
| IRO-010-2 | Reliability Coordination — Coordination of Real-time Operations | PARAMETERIZED | Information exchange between RCs and TOPs/BAs |
| IRO-014-3 | Operationally Planning Assessments | PARAMETERIZED | Next-day reliability assessments |
| IRO-019-2 | Transmission Relay Loadability | PARAMETERIZED | Coordinate with PRC-023 |

### MOD — Modeling, Data, and Analysis

| Standard | Title | Confidence | Key obligation |
|---|---|---|---|
| MOD-025-2 | Verification of Generator Real and Reactive Power Capability | PARAMETERIZED | Verification testing cadence; initial + 5-year reverification |
| MOD-026-1 | Verification of Models and Data for Generator Excitation Control System | PARAMETERIZED | Dynamic model verification |
| MOD-027-1 | Verification of Models and Data for Turbine/Governor and Load Control | PARAMETERIZED | Dynamic model verification |
| MOD-032-1 | Data for Power System Modeling and Analysis | PARAMETERIZED | Data provided within specified deadlines |
| MOD-033-1 | Steady-State and Dynamic System Model Validation | PARAMETERIZED | Post-disturbance model comparison |

### NUC — Nuclear Plant Interface Requirements

| Standard | Title | Confidence | Key obligation |
|---|---|---|---|
| NUC-001-4 | Nuclear Plant Interface Coordination | DETERMINISTIC | Interface agreements between NUC-GO/GOP and TO/TOP/BA/RC; reviewed annually |

### PER — Personnel Performance, Training, and Qualifications

| Standard | Title | Confidence | Key obligation |
|---|---|---|---|
| PER-003-2 | Operating Personnel Credentials | DETERMINISTIC | System operators must hold valid credentials for their function |
| PER-004-2 | Reliability Coordination — Staffing | PARAMETERIZED | Qualified staff available at RC 24/7 |
| PER-005-3 | System Personnel Training | DETERMINISTIC | Initial and continuing training; minimum training hours documented |
| PER-006-1 | Observing Operator Training | PARAMETERIZED | Annual training observation |

### PRC — Protection and Control

| Standard | Title | Confidence | Key obligation |
|---|---|---|---|
| PRC-001-2 | System Protection Coordination | PARAMETERIZED | Protection system coordination documentation |
| PRC-002-2 | Dynamic Disturbance Monitoring | PARAMETERIZED | Monitoring equipment at specified BES locations |
| PRC-004-5 | Protection System Misoperation Identification and Correction | DETERMINISTIC | Document and evaluate each misoperation within 120 days |
| **PRC-005-6** | **Protection System, Automatic Reclosing, and Sudden Pressure Relaying Maintenance** | **DETERMINISTIC** | **Explicit maximum maintenance intervals per Table 1 component type** |
| PRC-006-5 | Automatic Underfrequency Load Shedding | PARAMETERIZED | UFLS program design and testing |
| PRC-019-2 | Coordination of Generating Unit or Plant Capabilities, Voltage Regulating Controls, and Protection | PARAMETERIZED | Generator and protection coordination |
| PRC-023-4 | Transmission Relay Loadability | PARAMETERIZED | Relay settings must not limit transmission before thermal limits |
| PRC-024-2 | Generator Frequency and Voltage Protective Relay Settings | PARAMETERIZED | Settings within NERC-defined ride-through curves |
| PRC-025-2 | Generator Relay Loadability | PARAMETERIZED | Generator relay settings review |
| PRC-026-1 | Relay Performance During Stable Power Swings | PARAMETERIZED | Relay coordination for power swing conditions |
| PRC-027-1 | Coordination of Protection Systems for Performance During Faults | PARAMETERIZED | Protection coordination study every 5 years |

### TOP — Transmission Operations

| Standard | Title | Confidence | Key obligation |
|---|---|---|---|
| TOP-001-4 | Transmission Operations | DETERMINISTIC | TOP operates within IROLs and SOLs; must not direct actions that violate reliability standards |
| TOP-002-4 | Operations Planning | PARAMETERIZED | Next-day operational analysis |
| TOP-003-4 | Operational Reliability Data | PARAMETERIZED | Data provided to RC within specified timeframes |

### TPL — Transmission Planning

| Standard | Title | Confidence | Key obligation |
|---|---|---|---|
| TPL-001-5 | Transmission System Planning Performance Requirements | PARAMETERIZED | Annual steady-state and stability analysis for P0–P7 planning events |
| TPL-007-4 | Transmission System Planned Performance for Geomagnetic Disturbance Events | PARAMETERIZED | GMD vulnerability assessment |

### VAR — Voltage and Reactive

| Standard | Title | Confidence | Key obligation |
|---|---|---|---|
| VAR-001-5 | Voltage and Reactive Control | PARAMETERIZED | TO/TOP/BA/RC voltage profile maintenance |
| VAR-002-4.1 | Generator Operation for Maintaining Network Voltage Schedules | PARAMETERIZED | Generator reactive capability dispatch |
| VAR-003-1a | Generator Automatic Voltage Regulator (AVR) Maintenance | PARAMETERIZED | AVR in service; excitation system operational |

---

## Key DETERMINISTIC thresholds (cross-standard reference)

| Obligation | Threshold | Standard |
|---|---|---|
| Battery inspection interval | 18 calendar months maximum | PRC-005-6 Table 1a |
| Battery service test interval | 18 calendar months maximum | PRC-005-6 Table 1a |
| Protection system component maintenance | 6 calendar years maximum for most component types | PRC-005-6 Table 1 |
| Microprocessor-based relay (trip function test) | 12 calendar years maximum | PRC-005-6 Table 1-5 |
| Vegetation patrol/inspection (transmission ROW) | Once per calendar year minimum | FAC-003-4 R2 |
| MVCD maintenance clearance | No vegetation entering MVCD at any time | FAC-003-4 R1 |
| Misoperation evaluation and documentation | Within 120 days of identification | PRC-004-5 R2 |
| Event reporting — initial oral notification | Within 1 hour for specified event categories | EOP-004-4 Table 1 |
| Event reporting — written report | Within 24 hours for most event categories | EOP-004-4 Table 1 |
| NUC-001 interface agreement review | Annually | NUC-001-4 R3 |
| System operator credentials | Valid credential required before operating; continuous | PER-003-2 R1 |
| Three-part communication | Required for all directives issued in real time | COM-002-4 R3 |
| System operator credential | Valid NERC credential before solo operations; renewed every 3 years | PER-003-2 R1 |
| Annual operator training | All four PER-005 content areas completed by Dec 31 each year | PER-005-3 R2 |
| Frequency Response Obligation | BA must provide ≥ NERC-published FRO MW during frequency events | BAL-003-1 R1 |
| Frequency Bias Setting | BA AGC bias setting ≥ FRO in absolute value; reported to NERC | BAL-003-1 R2 |
| Generator P-Q reverification | Every 60 calendar months (5 years) from last verification | MOD-025-2 R2 |
| Generator initial P-Q verification | Within 6 months of commercial operation or significant modification | MOD-025-2 R1 |
| Annual transmission planning assessment | P0–P7 event categories; steady-state + stability; by Dec 31 each year | TPL-001-5 R1/R2 |
| Blackstart unit test | At least once every 36 calendar months | EOP-005-3 R13 |
| Backup control center exercise | At least once every 60 calendar months | EOP-008-2 R2 |
| IROL no-exceed | TOP must not knowingly violate an IROL; IROL violation = immediate corrective action | TOP-001-4 R13 |
| SOL exceedance notification | Notify RC as soon as practicable (≤1 operating hour) | TOP-001-4 |

---

## Open assumption registry

| ID | Standard | Summary | Review date |
|---|---|---|---|
| ASSUME-NERC-PRC-001 | PRC-005-6 | Battery maintenance intervals: 18-month inspection/service test; 18-month initial performance test; 3-year subsequent; sealed battery types per Table 1b | 2026-05-21 |
| ASSUME-NERC-PRC-002 | PRC-005-6 | Protection system component intervals: DC supply testing per Table 1a; electromechanical relay trip testing ≤6 years; microprocessor ≤12 years; control circuit ≤12 years | 2026-05-21 |
| ASSUME-NERC-PRC-003 | PRC-004-5 | Misoperation: any relay operation that is not the intended response to a fault or abnormal condition; includes both false trips and failure-to-trip; 120-day evaluation window | 2026-05-21 |
| ASSUME-NERC-PRC-004 | PRC-023-4 | Relay loadability: relay settings reviewed when equipment ratings change; line loading threshold methodology per PRC-023 Table 1; coordination with IRO-019 | 2026-05-21 |
| ASSUME-NERC-FAC-001 | FAC-003-4 | Vegetation patrol: "once per calendar year" = must be completed by Dec 31 of each year; applies to transmission lines at 200kV and above and select lower voltage per applicability | 2026-05-21 |
| ASSUME-NERC-FAC-002 | FAC-008-3 | Facility ratings methodology: written document identifying equipment, rating factors, ambient conditions, and seasonal adjustments; must be consistent with actual ratings in use | 2026-05-21 |
| ASSUME-NERC-EOP-001 | EOP-004-4 | Event categories: Table 1 specifies 18 reportable event types; "aware" = responsible entity or its operating personnel know of the event; oral notification = phone to NERC and RE |2026-05-21 |
| ASSUME-NERC-EOP-002 | EOP-005-3 | Blackstart test: full start or partial (load-rejected) acceptable; 3-year maximum interval; test report with start time, end time, and deviations documented | 2026-05-21 |
| ASSUME-NERC-COM-001 | COM-002-4 | Three-part communication: directive definition, steps, voice log as primary evidence, written confirmation acceptable, intra-company scope | 2026-05-21 |
| ASSUME-NERC-TOP-001 | TOP-001-4 | IROL/SOL list currency, corrective action procedures per IROL, SOL notification within 1 operating hour, RC directive exception documentation | 2026-05-21 |
| ASSUME-NERC-PER-001 | PER-003-2 | System operator credentials: 3-year renewal cycle, 200 CEH, employer verification obligation, credential type must match registered function | 2026-05-21 |
| ASSUME-NERC-PER-002 | PER-005-3 | Annual training: calendar year Dec 31 deadline, all four R1 topics required, initial training before unsupervised ops, 3-year records retention | 2026-05-21 |
| ASSUME-NERC-BAL-001 | BAL-003-1 | FRO = NERC-published MW value; bias setting ≥ FRO absolute value; non-compliance triggers CAP; 27-point measurement; no qualifying events = harmless | 2026-05-21 |
| ASSUME-NERC-MOD-001 | MOD-025-2 | Generator P-Q verification: significant modification definition, 60-month from last test, verification report required elements, cold shutdown waiver path | 2026-05-21 |
| ASSUME-NERC-TPL-001 | TPL-001-5 | Annual planning assessment: calendar year deadline, near-term base case, P0 unacceptable, stability simulation required, 3-year retention | 2026-05-21 |
| ASSUME-NERC-EOP-003 | EOP-005-3 | Blackstart test: 36-month from last successful test (detailed, supersedes EOP-002), partial acceptable, failed triggers retest, 42-month records retention | 2026-05-21 |
| ASSUME-NERC-EOP-004 | EOP-008-2 | Backup control center: actual operational demonstration required (not tabletop), 60-month exercise, third-party agreement reviewed annually | 2026-05-21 |

---

## Contested items pending resolution

| Item | Standard | Reason | Resolution path |
|---|---|---|---|
| Facility ratings methodology adequacy | FAC-008-3 | Whether the methodology is "consistent" with actual ratings is an assessor judgment; no objective methodology standard specified | RE audit review; FAC-008 violation precedent guidance |
| MVCD calculation method | FAC-003-4 | MVCD formula produces different clearances depending on conductor voltage, altitude, and temperature; which temperature/conditions to use for compliance is PARAMETERIZED | Vegetation management plan documents assumptions; RE review |
| "Responsible" for a protection system | PRC-005-6 | When ownership and operations are split between multiple entities, which entity is responsible for maintenance may be CONTESTED | Joint ownership agreement; compliance filing with RE |
| Misoperation — borderline events | PRC-004-5 | Some events are ambiguous: relay operated as designed but design was later found to be incorrect — is this a misoperation? | Event-specific determination; escalate to RE for guidance |
| Model validation deviation threshold | MOD-033-1 | How much deviation between simulated and actual response triggers a model update is not defined numerically | Entity-specific threshold documented in evidence |

---

## Cross-standard dependencies

| Shared artifact | Standards | Notes |
|---|---|---|
| Protection system maintenance records | PRC-005-6, CIP-007-6 (patch mgmt of digital relays) | Digital relays subject to BOTH PRC-005 maintenance intervals AND CIP-007 patch management; the intersection requires careful scope management |
| Facility ratings | FAC-008-3, MOD-032-1, TPL-001-5 | Same ratings used in planning studies and operations; must be consistent across all three uses |
| Nuclear plant interface agreements | NUC-001-4, EOP-004-4, TOP-001-4 | Interface agreements define how nuclear units communicate with grid operators during emergencies; EOP-004 event categories include nuclear-related events |
| Blackstart resources | EOP-005-3, BAL-005-1 (AGC) | Blackstart resources are typically exempt from normal AGC dispatch requirements during restoration |
| Event reporting | EOP-004-4, NERC Bulk Power System (BPS) event logging | EOP-004 report feeds NERC's EOAS (Operating Events Analysis System); same events may require parallel reporting to state PUC or NRC |

---

## CI/CD gate configuration

Standard three-tier gate (see NERC CIP registry for reference). Non-CIP specific constraints:

- **Applicable function fixture:** Each test must verify the entity's registered functional role (TO, TOP, BA, RC, GO, GOP, etc.) before applying standard-specific requirements. A BA is not subject to TOP-002; a GO is not subject to EOP-005 unless it has blackstart resources.
- **Maintenance interval tracking (PRC-005):** Last maintenance date per component per protection system; alert when approaching maximum interval with 60-day lead.
- **Vegetation patrol cadence (FAC-003):** Calendar-year patrol completion tracker; alert when December approaches without documented patrol completion for all applicable line segments.
- **Event reporting deadlines (EOP-004):** Event category classification at intake; 1-hour and 24-hour countdown timers started on event awareness timestamp.
- **NUC-001 annual review:** Interface agreement review due date tracked; failure = DETERMINISTIC after Dec 31 of review year.

---

## Specification file status

| File | Contents | Assumptions | Confidence | Status |
|---|---|---|---|---|
| `prc-protection-control.md` | PRC-005-6 (full Table 1 maintenance intervals), PRC-004-5 (misoperation), PRC-023-4/PRC-024-2 (relay loadability/settings) | ASSUME-NERC-PRC-001–004 | HIGH (PRC-005, PRC-004) / MEDIUM (PRC-023/024) | ✅ Parsed |
| `fac-eop-operations.md` | FAC-003-4 (vegetation management), FAC-008-3 (facility ratings), EOP-004-4 (event reporting), NUC-001-4 (nuclear interface) | ASSUME-NERC-FAC-001–002, EOP-001–002 | HIGH (FAC-003 patrol, EOP-004 timelines) / MEDIUM (FAC-008 methodology) | ✅ Parsed |
| `com-top-operations.md` | COM-002-4 (three-part communication), TOP-001-4 (IROL/SOL no-exceed, RC directive compliance) | ASSUME-NERC-COM-001, TOP-001 | HIGH | ✅ Parsed |
| `per-bal-personnel.md` | PER-003-2 (operator credentials, 3-year NERC cert), PER-005-3 (annual training, 4 content areas), BAL-003-1 (FRO, frequency bias setting) | ASSUME-NERC-PER-001–002, BAL-001 | HIGH | ✅ Parsed |
| `mod-tpl-eop-planning.md` | MOD-025-2 (generator P-Q verification, 60-month), TPL-001-5 (P0–P7 annual planning), EOP-005-3 (blackstart 36-month), EOP-008-2 (backup control center 60-month) | ASSUME-NERC-MOD-001, TPL-001, EOP-003–004 | MEDIUM | ✅ Parsed |
| *(INT, IRO, VAR, EOP-006/011)* | Interchange scheduling, RC coordination, reactive control, emergency procedures | TBD | MEDIUM–PARAMETERIZED | 🔲 Pending |

---

## Remaining parse priority

| Priority | Standard | Rationale |
|---|---|---|
| 1 | ~~COM-002-4 (three-part communication)~~ | ✅ Parsed — `com-top-operations.md` |
| 2 | ~~TOP-001-4 (IROL/SOL authority)~~ | ✅ Parsed — `com-top-operations.md` |
| 3 | ~~PER-003-2 + PER-005-3 (operator credentials + training)~~ | ✅ Parsed — `per-bal-personnel.md` |
| 4 | ~~BAL-003-1 (frequency response obligation)~~ | ✅ Parsed — `per-bal-personnel.md` |
| 5 | ~~MOD-025-2 (generator capability verification)~~ | ✅ Parsed — `mod-tpl-eop-planning.md` |
| 6 | ~~TPL-001-5 (transmission planning)~~ | ✅ Parsed — `mod-tpl-eop-planning.md` |
| 7 | ~~EOP-005-3 + EOP-008-2 (blackstart + backup control center)~~ | ✅ Parsed — `mod-tpl-eop-planning.md` |
| 8 | INT-006-4 + INT-009-2 (interchange scheduling) | DETERMINISTIC no-unauthorized-transfer obligation; lower enforcement frequency |
| 9 | IRO-001-5 + IRO-014-3 (RC authority + operationally planning) | DETERMINISTIC for RC authority; PARAMETERIZED for next-day assessment |
| 10 | VAR-001-5 + VAR-002-4.1 (reactive control) | PARAMETERIZED; reactive dispatch obligations depend on system conditions |
