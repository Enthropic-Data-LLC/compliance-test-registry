# IEC 62304:2006+AMD1:2015 — Medical Device Software Lifecycle Processes

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Software development and maintenance processes for software that is itself a medical device (SaMD) or is embedded in a medical device
**Authority:** International Electrotechnical Commission (IEC)
**Enforcing context:** Required by EU MDR Annex I §17; recognized by FDA as a consensus standard; required by ISO 13485 §7.3 for software development; referenced by IMDRF SaMD guidance
**Current edition:** IEC 62304:2006 Amendment 1:2015

---

## Summary

| Metric | Count |
|---|---|
| Clauses | 9 (Clauses 4–9) |
| Software safety classes | 3 (A, B, C) |
| Processes | 8 (development, maintenance, risk management, configuration management, problem resolution, change management, documentation, QA) |
| Clauses parsed (individual files) | 2 (software-development-controls.md + maintenance-risk-problem-resolution.md) |
| Fully automated (DETERMINISTIC) | High — safety class gates make most requirements binary; SDP 9 elements, SOUP, traceability, problem reports all DETERMINISTIC |
| Partial automation (PARAMETERIZED) | Low — 1 traceability assumption |
| Human-determination required (CONTESTED) | Low — safety class assignment is PARAMETERIZED from ISO 14971 (not CONTESTED) |
| Open assumptions | 1 |

---

## Software safety class — pre-condition to all tests

Safety class drives which IEC 62304 activities are required. Assignment is based on ISO 14971 risk analysis:

| Class | Definition | Consequences of failure |
|---|---|---|
| **Class A** | No injury or damage to health possible | Cannot contribute to hazardous situation |
| **Class B** | Non-serious injury possible | Could contribute to hazardous situation that does not result in serious injury |
| **Class C** | Death or serious injury possible | Could contribute to hazardous situation that results in death or serious injury |

Class assignment is PARAMETERIZED (derived from ISO 14971 risk analysis). Once assigned, required activities are DETERMINISTIC.

---

## Per-clause confidence map

### Clause 4 — General Requirements

| Sub-clause | Requirement | Class | Confidence | Notes |
|---|---|---|---|---|
| 4.1 | Quality management system | A/B/C | DETERMINISTIC | Must have QMS; ISO 13485 satisfies this |
| 4.2 | Risk management | A/B/C | DETERMINISTIC | Risk management per ISO 14971 throughout lifecycle |
| 4.3 | Software safety classification | A/B/C | PARAMETERIZED | Classification determined and documented |
| 4.4 | References between documents | A/B/C | DETERMINISTIC | Traceability maintained |

### Clause 5 — Software Development Process

| Sub-clause | Requirement | Class | Confidence | Notes |
|---|---|---|---|---|
| 5.1 | Software development planning | A/B/C | DETERMINISTIC | Written software development plan required; 9 required elements |
| 5.2 | Software requirements analysis | A/B/C | DETERMINISTIC | Requirements documented; include functional, performance, interface, safety requirements |
| 5.3 | Software architectural design | B/C | DETERMINISTIC | Architecture designed; software items identified; segregation of safety-related items |
| 5.4 | Software detailed design | C | DETERMINISTIC | Detailed design of each software unit |
| 5.5 | Software unit implementation and verification | A/B/C | PARAMETERIZED (A), DETERMINISTIC (B/C) | Class A: accept without unit testing or other verification; Class B/C: unit testing required |
| 5.6 | Software integration and integration testing | B/C | DETERMINISTIC | Integration tested; records retained |
| 5.7 | Software system testing | A/B/C | DETERMINISTIC | System testing per test plan; records retained |
| 5.8 | Software release | A/B/C | DETERMINISTIC | Software version under configuration management; release authorization; accompanying documents |

### Clause 6 — Software Maintenance Process

| Sub-clause | Requirement | Class | Confidence | Notes |
|---|---|---|---|---|
| 6.1 | Establish software maintenance plan | A/B/C | DETERMINISTIC | Written maintenance plan |
| 6.2 | Problem and modification analysis | A/B/C | DETERMINISTIC | Impact analysis; safety impact determination; re-classification if needed |
| 6.3 | Modification implementation | A/B/C | DETERMINISTIC | Follow development process for changes; regression testing |

### Clause 7 — Software Risk Management Process

| Sub-clause | Requirement | Class | Confidence | Notes |
|---|---|---|---|---|
| 7.1 | Analysis of software contributing to hazardous situations | B/C | DETERMINISTIC | All software items that could contribute to hazards identified |
| 7.2 | Risk control measures implemented in software | B/C | DETERMINISTIC | Risk controls implemented and verified |
| 7.3 | Verification of risk control measures | B/C | DETERMINISTIC | Verification evidence in risk management file |
| 7.4 | Risk management of changes to existing software | B/C | DETERMINISTIC | Changes assessed for new hazards |

### Clause 8 — Software Configuration Management Process

| Sub-clause | Requirement | Class | Confidence | Notes |
|---|---|---|---|---|
| 8.1 | Configuration identification | A/B/C | DETERMINISTIC | All software items uniquely identified and versioned |
| 8.2 | Change control | A/B/C | DETERMINISTIC | Changes authorized before implementation; baseline established before testing |
| 8.3 | Configuration status accounting | A/B/C | DETERMINISTIC | Status of all software items tracked |

### Clause 9 — Software Problem Resolution Process

| Sub-clause | Requirement | Class | Confidence | Notes |
|---|---|---|---|---|
| 9.1 | Prepare problem reports | A/B/C | DETERMINISTIC | All problems documented |
| 9.2 | Investigate the problem | A/B/C | DETERMINISTIC | Root cause analysis; impact on safety |
| 9.3 | Advise relevant parties | A/B/C | PARAMETERIZED | Regulatory reporting if applicable |
| 9.4 | Use change control | A/B/C | DETERMINISTIC | Problem resolution follows change control |
| 9.5 | Maintain records | A/B/C | DETERMINISTIC | All problem reports and resolutions retained |
| 9.6 | Analyse problems for trends | B/C | PARAMETERIZED | Trend analysis to identify systemic issues |
| 9.7 | Verify software problem resolution | B/C | DETERMINISTIC | Resolution verified |
| 9.8 | Test documentation contents | B/C | DETERMINISTIC | Test documentation meets defined content requirements |

---

## Software development plan (§5.1) — DETERMINISTIC checklist

The plan must address:
1. Development lifecycle model
2. Standards, methods, tools used
3. Software configuration management plan
4. Problem resolution plan
5. Hardware/software integration plan
6. Software system test plan
7. Risk management activities
8. Regulatory compliance approach
9. Content of documentation to be produced

---

## Traceability requirements

IEC 62304 requires bidirectional traceability from:
- Software requirements → Software architecture → Software detailed design → Software unit tests → System tests
- Safety-related requirements → Risk controls → Verification evidence

Traceability matrix completeness is DETERMINISTIC (all items must be traceable); correctness of the linkages is PARAMETERIZED.

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Software development plan | IEC 62304 §5.1, EU MDR Annex II (tech doc), FDA QMSR §820.30 | Same plan; EU MDR requires it in technical documentation; FDA requires it in DHF |
| Risk management integration | IEC 62304 §7, ISO 14971 | IEC 62304 §7 is the software-specific risk management process that feeds the ISO 14971 risk file |
| Configuration management | IEC 62304 §8, ISO 13485 §4.2.4 (document control), FDA QMSR §820.30(i) | Same version control system; IEC 62304 adds software-specific traceability requirements |
| Problem resolution | IEC 62304 §9, ISO 13485 §8.2.2 (complaints), FDA QMSR §820.198 | Software problem reports may trigger complaint handling if they affect deployed devices |
| SOUP (Software of Unknown Provenance) | IEC 62304 §8.1.2 — must document and evaluate all SOUP/COTS/OSS components | Important for open-source and third-party library use in medical device software |
