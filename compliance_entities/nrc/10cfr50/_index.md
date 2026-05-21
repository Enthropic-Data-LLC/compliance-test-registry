# NRC 10 CFR Part 50 — Domestic Licensing of Production and Utilization Facilities

**Registry version:** 2026.05
**Last updated:** 2026-05-21
**Scope:** Commercial nuclear power reactors licensed under 10 CFR Part 50 (construction permits + operating licenses) and Part 52 (combined licenses); primary safety, quality assurance, and operational requirements for nuclear power plants
**Authority:** U.S. Nuclear Regulatory Commission (NRC)
**Enforcing context:** All NRC-licensed nuclear power reactors operating in the United States; approximately 90+ operating reactors at ~55 sites
**Related regulations:** 10 CFR Part 52 (combined licenses), 10 CFR Part 73 (security/cybersecurity), 10 CFR Part 26 (fitness for duty), 10 CFR Part 54 (license renewal)
**Note:** This registry covers Part 50 compliance from an operational/QA/event reporting perspective — not licensing process requirements. Radiological protection (10 CFR Part 20) and security (Part 73) are in separate entries.

---

## Summary

| Metric | Count |
|---|---|
| Key operational/safety sections | ~30 (§50.9, 50.48, 50.54, 50.55a, 50.59, 50.65, 50.72, 50.73, 50.75, and Appendices A/B/J/R/S) |
| Sections parsed (individual files) | 4 (event-reporting.md — §50.72/50.73; appendix-b-qa.md — Appendix B 18 criteria; maintenance-rule.md — §50.65; 50.55a-isi-ist.md — §50.55a ISI/IST) |
| Fully automated (DETERMINISTIC) | Moderate — event reporting timelines (50.72/50.73); maintenance rule metrics (50.65); fire protection equipment testing intervals |
| Partial automation (PARAMETERIZED) | Dominant — QA criterion adequacy (Appendix B), maintenance effectiveness (50.65(a)(1)/(a)(2) categorization), 50.59 screening |
| Human-determination required (CONTESTED) | Significant — "unreviewed safety question" determination (50.59), QA criterion adequacy, corrective action adequacy |
| Open assumptions | 22 (ASSUME-NRC50-EVTRPT-001–004, ASSUME-NRC50-QA-001–005, ASSUME-NRC50-MR-001–005, ASSUME-NRC50-ISI-001–008) |

---

## Per-section confidence map

### §50.72 and §50.73 — Event Reporting (DETERMINISTIC — primary automation target)

| Reporting type | Threshold | Notification window | Confidence |
|---|---|---|---|
| Emergency Classification notification | Emergency, Alert, Site Area Emergency, or General Emergency declared | Within 1 hour | DETERMINISTIC |
| Unusual Event notification | Notification of Unusual Event (NOUE) declared | Within 1 hour | DETERMINISTIC |
| 4-hour notification (§50.72(b)(2)) | Listed abnormal conditions including reactor trip, ECCS actuation, loss of safety function | Within 4 hours | DETERMINISTIC |
| 8-hour notification (§50.72(b)(3)) | Unanalyzed condition that compromises plant safety | Within 8 hours | DETERMINISTIC |
| 24-hour notification (§50.72(b)(4)) | Exercise of enforcement discretion; other specified conditions | Within 24 hours | DETERMINISTIC |
| Licensee Event Report (LER) (§50.73) | Written LER for events meeting §50.73 criteria | Within 60 days | DETERMINISTIC |

### §50.59 — Changes, Tests, and Experiments (CONTESTED/PARAMETERIZED)

| Decision | Classification |
|---|---|
| Does the proposed change require a license amendment? | CONTESTED — 10-criterion evaluation; "unreviewed safety question" determination |
| Is a written 50.59 evaluation required? | PARAMETERIZED — screening vs. full evaluation |
| Does the change require NRC prior approval? | PARAMETERIZED — dependent on 50.59 evaluation outcome |

10 CFR 50.59 is the most CONTESTED section in nuclear plant operations. A negative 50.59 determination (change requires amendment) carries significant regulatory and cost consequences. Evaluations require licensed professional (nuclear engineer, licensed senior reactor operator) judgment.

### §50.65 — Maintenance Rule (PARAMETERIZED — see `maintenance-rule.md`)

| Element | Confidence |
|---|---|
| Written Maintenance Rule program exists | DETERMINISTIC |
| Performance criteria established for SSCs | PARAMETERIZED |
| SSC categorized as (a)(1) or (a)(2) | PARAMETERIZED — functional failure performance triggers |
| (a)(1) goals and monitoring — corrective action plan | PARAMETERIZED |
| (a)(1) prompt categorization (≤90 days of criteria exceedance) | PARAMETERIZED — most-cited §50.65 violation |
| Annual performance review | DETERMINISTIC (24-month maximum cadence) |
| §50.65(a)(4) pre-maintenance risk assessment | DETERMINISTIC (existence required before OOS) |
| Online risk monitor currency | DETERMINISTIC (≤18 months for valid (a)(4)) |
| Expert panel composition and independence | PARAMETERIZED |
| (a)(1) goal adequacy | CONTESTED — Pattern 3 (expert panel sign-off required) |

### Appendix B — Quality Assurance Criteria (PARAMETERIZED — 18 criteria)

| Criterion | Title | Confidence |
|---|---|---|
| I | Organization | PARAMETERIZED |
| II | QA Program | PARAMETERIZED |
| III | Design Control | PARAMETERIZED |
| IV | Procurement Document Control | PARAMETERIZED |
| V | Instructions, Procedures, Drawings | PARAMETERIZED |
| VI | Document Control | PARAMETERIZED |
| VII | Control of Purchased Material, Equipment, and Services | PARAMETERIZED |
| VIII | Identification and Control of Materials, Parts, and Components | PARAMETERIZED |
| IX | Control of Special Processes | PARAMETERIZED |
| X | Inspection | PARAMETERIZED |
| XI | Test Control | PARAMETERIZED |
| XII | Control of Measuring and Test Equipment | DETERMINISTIC (calibration intervals) |
| XIII | Handling, Storage, Shipping, Preservation | PARAMETERIZED |
| XIV | Inspection, Test, and Operating Status | PARAMETERIZED |
| XV | Nonconforming Materials, Parts, or Components | PARAMETERIZED |
| XVI | Corrective Action | PARAMETERIZED |
| XVII | Quality Assurance Records | DETERMINISTIC (retention — lifetime of plant) |
| XVIII | Audits | DETERMINISTIC (annual internal; 2-year supplier audit cadence) |

### §50.48 — Fire Protection (PARAMETERIZED with DETERMINISTIC elements)

| Element | Confidence | Notes |
|---|---|---|
| Written fire protection program | DETERMINISTIC (existence) | Appendix R or NFPA 805 method |
| Fire barrier integrity testing | DETERMINISTIC (interval) | Visual inspection annually; penetration seal testing per qualified method |
| Fire suppression system testing | DETERMINISTIC (interval) | Sprinkler inspection per NFPA 25 |
| Safe shutdown analysis | PARAMETERIZED | Adequacy of shutdown capability after worst-case fire |
| Operator manual action acceptability | PARAMETERIZED | Time and feasibility of manual operator actions |

### §50.55a — Codes and Standards (PARAMETERIZED)

ASME Boiler and Pressure Vessel Code and ASME Code for Operation and Maintenance (OM Code) required for pressure-retaining systems. Inservice inspection (ISI) and inservice testing (IST) program intervals defined by the Code.

| Element | Confidence |
|---|---|
| ISI program implemented per current ASME code edition | PARAMETERIZED |
| IST program implemented per ASME OM Code | PARAMETERIZED |
| 10-year ISI interval — Class 1, 2, 3 components | DETERMINISTIC (interval) |
| ISI/IST results submitted to NRC per §50.55a(q) | PARAMETERIZED |

---

## Key DETERMINISTIC thresholds (cross-section reference)

| Obligation | Threshold | Section |
|---|---|---|
| Emergency class declaration notification | Within 1 hour | §50.72(a) |
| 4-hour notification (reactor trip, ECCS actuation, safety function loss) | Within 4 hours | §50.72(b)(2) |
| 8-hour notification (unanalyzed condition) | Within 8 hours | §50.72(b)(3) |
| Licensee Event Report (LER) submission | Within 60 days of discovery | §50.73 |
| LER supplement (if original incomplete) | Within 30 days of original LER | §50.73 |
| QA records retention | For the life of the facility; minimum 5 years after permanent shutdown | App. B, Criterion XVII |
| Maintenance Rule annual performance review | Every 24 months maximum (every refueling cycle minimum) | §50.65(a)(3) |
| (a)(1) prompt categorization after criteria exceedance | No regulatory bright-line; NRC practice: ≤90 days | §50.65(a)(1) |
| (a)(4) pre-maintenance risk assessment | Before each maintenance activity on in-scope SSCs | §50.65(a)(4) |
| (a)(4) Yellow risk management approval | Required before maintenance proceeds | §50.65(a)(4) / RG 1.174 |
| Online risk monitor (PRA model) currency | ≤18 months since last update for valid (a)(4) assessments | §50.65(a)(4) |
| Internal QA audit | Annually | App. B, Criterion XVIII |
| ISI interval — Class 1 pressure-retaining components | 10-year inspection interval | §50.55a(g) |
| ISI interval extension (no NRC approval) | ≤12 additional months beyond 10 years | §50.55a / ASME XI IWA-2430(d) |
| Class 1 Period 1 inspection target | ~40% of required examinations | ASME XI IWB-2412 |
| Class 1 Period 2 inspection target | ~20% of required examinations | ASME XI IWB-2412 |
| Class 1 Period 3 inspection target | ~40% of required examinations | ASME XI IWB-2412 |
| Group A pump quarterly test interval | 3 months | ASME OM ISTB-3400 |
| Group A pump comprehensive test interval | 24 months | ASME OM ISTB-3400 |
| Group B pump maximum test interval | 120 months (10 years) at cold shutdown | ASME OM ISTB-3400 |
| Pump differential pressure Required Action level | ≥10% decrease from reference | ASME OM Table ISTB-5121-1 |
| Pump vibration Required Action level | ≥6× reference value | ASME OM Table ISTB-5121-1 |
| Category A/B valve quarterly exercise | 3 months (if can test during normal ops) | ASME OM ISTC-3300 |
| Category A/B valve cold-shutdown maximum | 60 months (5 years) | ASME OM ISTC-3510 |
| Safety/relief valve setpoint test interval | 60 months (5 years) | ASME OM ISTC-3600 |
| Safety/relief valve as-left setpoint tolerance | ±1% of nominal setpoint | ASME OM ISTC-3600 |
| Valve stroke time Required Action level | ±100% deviation from reference | ASME OM ISTC-5221-1 |
| SG primary-to-secondary leakage limit | ≤150 gallons/day per steam generator | 10 CFR 50 App. A GDC 14 |
| Fitness for duty testing | Random + cause-based; random rate ≥50% per year for covered workers | 10 CFR Part 26 (cross-reference) |

---

## Open assumption registry

| ID | Section | Summary | Review date |
|---|---|---|---|
| ASSUME-NRC50-EVTRPT-001 | §50.72(a) | Emergency class notifications: "within 1 hour" from declaration, not from event; NRC Operations Center + applicable state and local authorities; phone notification acceptable initially | 2026-05-21 |
| ASSUME-NRC50-EVTRPT-002 | §50.72(b)(2) | 4-hour notifications: clock starts when the licensee becomes aware of the condition; conditions enumerated in §50.72(b)(2)(i)–(xi); reactor trip includes automatic and manual | 2026-05-21 |
| ASSUME-NRC50-EVTRPT-003 | §50.73 | LER: 60-day window from discovery; covers events per §50.73(a)(2) criteria; supplemented within 30 days if original was incomplete; submitted to NRC Document Control | 2026-05-21 |
| ASSUME-NRC50-EVTRPT-004 | §50.72/50.73 | "Discovery": the time when responsible licensed personnel become aware of a reportable condition — same principle as NRC Inspection Procedure 92703 guidance; not when the event occurred | 2026-05-21 |
| ASSUME-NRC50-QA-001 | App. B, Criterion XVIII | Internal QA audits: performed at least annually by personnel not having direct responsibility for the area being audited; audit findings documented and corrective actions tracked | 2026-05-21 |
| ASSUME-NRC50-QA-002 | App. B, Criterion XII | M&TE calibration: calibration intervals established based on use frequency and stability; calibration traceable to NIST standards; out-of-tolerance instruments trigger impact evaluation | 2026-05-21 |
| ASSUME-NRC50-QA-003 | App. B, Criterion XV | Nonconformances: documented in Corrective Action Program (CAP) within 24 hours of identification; dispositioned as use-as-is, rework, repair, reject, or scrap — each with documented justification | 2026-05-21 |
| ASSUME-NRC50-QA-004 | App. B, Criterion XVI | Corrective actions: root cause analysis for significant conditions adverse to quality (SCAQs); corrective action documented, implemented, and verified; recurrence prevention for SCAQs | 2026-05-21 |
| ASSUME-NRC50-QA-005 | App. B, Criterion XVII | QA records: retained for life of facility; vital records protected against fire, flood, and theft; electronic records acceptable with integrity controls | 2026-05-21 |
| ASSUME-NRC50-MR-001 | §50.65(a)(2) | Performance criteria: written before (a)(2) categorization; quantitative metrics required; PM basis document required; monitoring data current | 2026-05-21 |
| ASSUME-NRC50-MR-002 | §50.65(a)(1) | Categorization triggers: MPFF definition, two-MPFF threshold, prompt placement (≤90 days), measurable goals, expert panel review and minutes | 2026-05-21 |
| ASSUME-NRC50-MR-003 | §50.65(a)(3) | Annual review: 24-month maximum, all SSCs covered, functional failure summary, (a)(2) criteria adequacy evaluated, management approval | 2026-05-21 |
| ASSUME-NRC50-MR-004 | §50.65(a)(4) | Pre-maintenance risk assessment: before OOS, graded approach acceptable, risk monitor ≤18 months current, Yellow/Red requires management approval | 2026-05-21 |
| ASSUME-NRC50-MR-005 | §50.65 (expert panel) | Expert panel: charter with composition requirements, independence from work group, SRO representation, documented basis for all decisions | 2026-05-21 |
| ASSUME-NRC50-ISI-001 | §50.55a ISI | ISI program document requirements, code edition applicability (6 months before interval start), ANII approval | 2026-05-21 |
| ASSUME-NRC50-ISI-002 | §50.55a ISI interval | 10-year interval start at commercial operation; 40%/20%/40% period distribution; 12-month extension without NRC approval | 2026-05-21 |
| ASSUME-NRC50-ISI-003 | §50.55a ISI scope | Risk-informed §50.69 alternative to schedule-based examination selection allowed with NRC approval | 2026-05-21 |
| ASSUME-NRC50-ISI-004 | §50.55a IST pumps | Group A (quarterly/2-year) and Group B (cold shutdown max 10 years) classification per plant IST program | 2026-05-21 |
| ASSUME-NRC50-ISI-005 | §50.55a IST pumps | Pump Alert and Required Action levels per ASME OM Table ISTB-5121-1/5221-1; Required Action = inoperable declaration | 2026-05-21 |
| ASSUME-NRC50-ISI-006 | §50.55a IST valves | Category A/B/C classification per IST program; cold-shutdown deferred max 5 years; PRD as-left ±1% | 2026-05-21 |
| ASSUME-NRC50-ISI-007 | §50.55a(z) alternatives | NRC written approval required BEFORE any code departure; hardship (z)(1) or equivalent safety (z)(2) basis | 2026-05-21 |
| ASSUME-NRC50-ISI-008 | §50.55a SG tubes | SG tube repair limit 10% TWA (uniform); mechanism-specific limits from ERAs; leakage ≤150 gpd per SG | 2026-05-21 |

---

## Contested items pending resolution

| Item | Section | Reason | Resolution path |
|---|---|---|---|
| "Unreviewed safety question" determination | §50.59 | 10-criterion evaluation outcome is engineering and legal judgment; NRC enforcement history shows significant variance | Licensed nuclear engineer evaluation; legal review for borderline cases; may require NRC license amendment |
| Corrective action adequacy | App. B, Criterion XVI | Whether a corrective action adequately prevents recurrence is a judgment determination; NRC inspectors evaluate against "reasonable assurance" standard | QA manager and corrective action review board sign-off; NRC inspection findings as feedback |
| Maintenance Rule categorization | §50.65 | Whether an SSC meets (a)(2) performance criteria or must be moved to (a)(1) monitoring involves system engineer judgment | Maintenance Rule expert panel review; documented technical justification |
| Fire barrier equivalency | §50.48 | Whether an alternative fire barrier approach (NFPA 805 risk-informed method) provides "equivalent protection" to deterministic Appendix R is technically contested | Fire protection engineer evaluation; NRC license amendment if departing from Appendix R |

---

## Cross-standard dependencies

| Shared artifact | Regulations | Notes |
|---|---|---|
| Corrective Action Program (CAP) | 10 CFR 50 App. B Criteria XV+XVI, 10 CFR Part 73 (security CAP), ISO 9001 §10.2 | Nuclear CAP is among the most rigorous in any industry; designed to capture and correct all conditions adverse to quality |
| QA records | 10 CFR 50 App. B Criterion XVII, 10 CFR Part 73 records, NERC CIP-007 logging | Retention for plant life is longer than any other framework in this registry |
| Event reporting | 10 CFR 50.72/50.73, NERC EOP-004-4 (NUC-001 interface), NRC 10 CFR 50.72 to NRC Ops Center | Nuclear events may require parallel notification to NRC (§50.72) and NERC via NUC-001 procedures — these run concurrently |
| Test and maintenance records | 10 CFR 50 App. B, NERC PRC-005-6 (for digital protection systems) | Digital I&C protective systems are subject to both NRC QA (surveillance testing, calibration) and NERC PRC-005 maintenance intervals |
| Inservice inspection | §50.55a (ASME Code), NERC facility ratings (FAC-008) | ISI findings may require derating of pressure-retaining components, which must flow to NERC FAC-008 facility ratings |

---

## CI/CD gate configuration

- **Reactor license scope fixture:** All tests gated by `is_nrc_licensed_nuclear_facility()` — never applied to non-nuclear systems.
- **Event reporting countdown (§50.72):** 1-hour, 4-hour, 8-hour countdown timers started on event awareness timestamp; alert at 75% elapsed.
- **LER deadline tracker (§50.73):** 60-day window from discovery; LER management system integration.
- **QA audit cadence (App. B Criterion XVIII):** Annual audit calendar tracked; alert 30 days before annual cycle closes.
- **50.59 evaluation status:** All proposed changes classified at intake; changes without a completed 50.59 screening before implementation trigger Pattern 2 failure.

---

## Specification file status

| File | Contents | Assumptions | Confidence | Status |
|---|---|---|---|---|
| `event-reporting.md` | §50.72 (1h/4h/8h/24h notifications), §50.73 (LER 60-day), emergency class declarations | ASSUME-NRC50-EVTRPT-001–004 | HIGH | ✅ Parsed |
| `appendix-b-qa.md` | All 18 QA criteria (Appendix B); calibration intervals (Crit. XII); audit cadence (Crit. XVIII); CAP (Crit. XV+XVI); records retention (Crit. XVII) | ASSUME-NRC50-QA-001–005 | MEDIUM | ✅ Parsed |
| *(§50.59 changes, tests, experiments)* | 10-criterion evaluation; screening vs. full evaluation; amendment trigger | TBD | CONTESTED | 🔲 Pending |
| `maintenance-rule.md` | §50.65(a)(1) goals/corrective action; (a)(2) performance criteria; (a)(3) annual review; (a)(4) pre-maintenance risk assessment; expert panel | ASSUME-NRC50-MR-001–005 | MEDIUM | ✅ Parsed |
| `50.55a-isi-ist.md` | ISI program document; 10-year interval/period distribution; Class 1–3 exam categories; IST pump Group A/B intervals and acceptance criteria; IST valve intervals; §50.55a(z) alternatives; SG tube integrity | ASSUME-NRC50-ISI-001–008 | MEDIUM | ✅ Parsed |
| *(§50.48 fire protection)* | Fire protection program; barrier testing; Appendix R vs. NFPA 805 | TBD | MEDIUM | 🔲 Pending |

---

## Remaining parse priority

| Priority | Section | Rationale |
|---|---|---|
| 1 | ~~§50.65 (Maintenance Rule)~~ | ✅ Parsed — `maintenance-rule.md` |
| 2 | ~~§50.55a (ISI/IST)~~ | ✅ Parsed — `50.55a-isi-ist.md` |
| 3 | §50.48 (Fire protection) | High enforcement history; Appendix R vs. NFPA 805 decision point important |
| 4 | §50.59 (Changes, tests, experiments) | CONTESTED; most important section for plant modifications; Pattern 3 dominant |
| 5 | 10 CFR Part 26 (Fitness for Duty) | Random testing rate ≥50% is DETERMINISTIC; cross-reference to security |
