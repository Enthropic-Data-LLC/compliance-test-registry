# OSHA Registry Manifest

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** 29 CFR 1910 (General Industry) + 29 CFR 1926 (Construction)
**Authority:** Occupational Safety and Health Administration, U.S. Department of Labor

---

## Summary

| Metric | Count |
|---|---|
| Standards parsed | 13 |
| Total requirements parsed | 61 (section-level) |
| Fully automated (DETERMINISTIC) | 22 |
| Partial automation (PARAMETERIZED) | 30 |
| Human-determination required (CONTESTED) | 9 |
| Unresolvable | 0 |
| Open assumptions | 21 |
| Stale reviews | 0 (registry is new) |
| Pending external escalations | 0 |

---

## Per-standard confidence map — 29 CFR 1910 (General Industry)

| Standard | Title | Overall Confidence | PARAMETERIZED | CONTESTED |
|---|---|---|---|---|
| 1910.38 | Emergency Action Plans | HIGH | — | — |
| 1910.119 | Process Safety Management | MEDIUM | (e) PSI completeness, (f) PHA methodology, (m) MOC scope | — |
| 1910.120 | HAZWOPER | MEDIUM | (b) program adequacy, (h) training hours, (i) medical scope | (e) site-specific plan adequacy |
| 1910.132 | PPE — General Requirements | MEDIUM | (d) hazard assessment methodology | — |
| 1910.134 | Respiratory Protection | MEDIUM | (d) selection rationale, (e)(6) physician determinations | — |
| 1910.146 | Permit-Required Confined Spaces | MEDIUM | (c)(5) hazard reclassification, (k) training adequacy | (d)(9) adequate rescue capability |
| 1910.147 | Control of Hazardous Energy (LOTO) | HIGH | (c)(4) annual inspection scope | — |
| 1910.178 | Powered Industrial Trucks | MEDIUM | (l)(3) operator evaluation timing | — |
| 1910.212 | Machine Guarding | CONTESTED | (a)(1) "point of operation" boundary | (a)(1) "other hazardous parts" scope |
| 1910.1200 | Hazard Communication | HIGH | — | — |

---

## Per-standard confidence map — 29 CFR 1926 (Construction)

| Standard | Title | Overall Confidence | PARAMETERIZED | CONTESTED |
|---|---|---|---|---|
| 1926.451 | Scaffolds | MEDIUM | (b)(1) platform gap tolerances, (f)(3) prohibited actions | — |
| 1926.501 | Fall Protection — Duty to Have | HIGH | — | — |
| 1926.651 | Excavations | MEDIUM | (g) atmospheric testing scope, (i)(1) "competent person" determination | (i)(2) hazardous condition remediation |

---

## Open assumption registry

| ID | Standard | Topic | Approved by | Next review |
|---|---|---|---|---|
| ASSUME-119-001 | 1910.119 | Completeness of process safety information (PSI) set | Compliance Officer | 2027-05-20 |
| ASSUME-119-002 | 1910.119 | PHA methodology acceptance criteria | Compliance Officer | 2027-05-20 |
| ASSUME-119-003 | 1910.119 | MOC scope: "replacement in kind" boundary | Compliance Officer | 2027-05-20 |
| ASSUME-120-001 | 1910.120 | Minimum content of site-specific health and safety plan | Compliance Officer | 2027-05-20 |
| ASSUME-120-002 | 1910.120 | HAZWOPER refresher training minimum duration | Compliance Officer | 2027-05-20 |
| ASSUME-120-003 | 1910.120 | Medical surveillance trigger thresholds | Compliance Officer | 2027-05-20 |
| ASSUME-132-001 | 1910.132 | Hazard assessment methodology sufficiency | Compliance Officer | 2027-05-20 |
| ASSUME-134-001 | 1910.134 | "Immediately dangerous to life or health" classification criteria | Compliance Officer | 2027-05-20 |
| ASSUME-134-002 | 1910.134 | Physician/PLHCP determination scope for fitness-for-duty | Compliance Officer | 2027-05-20 |
| ASSUME-146-001 | 1910.146 | Reclassification adequacy: permit-required → non-permit space | Compliance Officer | 2027-05-20 |
| ASSUME-146-002 | 1910.146 | Adequate rescue capability determination | Compliance Officer | 2027-05-20 |
| ASSUME-147-001 | 1910.147 | Annual inspection scope and documentation adequacy | Compliance Officer | 2027-05-20 |
| ASSUME-178-001 | 1910.178 | Operator evaluation interval after observed unsafe operation | Compliance Officer | 2027-05-20 |
| ASSUME-451-001 | 1926.451 | Maximum scaffold platform gap (plank, gap-fill) determination | Compliance Officer | 2027-05-20 |
| ASSUME-451-002 | 1926.451 | "Equivalent protection" for prohibited scaffold actions | Compliance Officer | 2027-05-20 |
| ASSUME-651-001 | 1926.651 | Atmospheric testing frequency in excavations | Compliance Officer | 2027-05-20 |
| ASSUME-651-002 | 1926.651 | Competent person determination criteria | Compliance Officer | 2027-05-20 |
| ASSUME-119-004 | 1910.119 | Compliance audit cycle (3-year) adequacy vs. scope | Compliance Officer | 2027-05-20 |
| ASSUME-120-004 | 1910.120 | Decontamination procedure adequacy | Compliance Officer | 2027-05-20 |
| ASSUME-134-003 | 1910.134 | Fit-test protocol equivalency for novel facepieces | Compliance Officer | 2027-05-20 |
| ASSUME-212-001 | 1910.212 | Point-of-operation guarding method adequacy | Compliance Officer | 2027-05-20 |

---

## Contested items pending external resolution

| ID | Standard | Issue | Status |
|---|---|---|---|
| CONTEST-212-R1 | 1910.212 | OSHA has not defined a bright-line for "other hazardous parts" — citation history is inspection-dependent | Pattern 3 (human-surfacing) test in place |
| CONTEST-146-R1 | 1910.146 | Adequacy of non-entry rescue is evaluated case-by-case; no bright-line criteria exist | Pattern 3 in place; requires competent-person sign-off |

---

## Cross-standard dependencies

| Shared artifact | Standards | Notes |
|---|---|---|
| Written safety program | 1910.119, 1910.120, 1910.146, 1910.147, 1910.134, 1910.1200 | Each standard requires a distinct written program, but they are often maintained as a unified SMS document with standard-specific annexes |
| Employee training records | 1910.119, 1910.120, 1910.132, 1910.134, 1910.146, 1910.147, 1910.178, 1910.1200, 1926.501, 1926.451 | Common training management system; each standard has distinct frequency and content requirements |
| Hazard assessment / JHA | 1910.132, 1910.119 (PHA), 1926.651 (soil classification) | Distinct in scope and method but share the "competent person" concept |
| Medical surveillance records | 1910.120, 1910.134 | HAZWOPER and respiratory programs both require PLHCP-driven medical evaluations; records share a format but trigger conditions differ |
| Competent person designation | 1926.451, 1926.651, 1910.146, 1910.147 | Term appears in all four; definition is consistent across 1926 but 1910 uses "authorized employee" in a narrower sense |

---

## CI/CD gate configuration

Same tier-based gate as NERC CIP registry:

- **Pattern 1 (HIGH):** All must PASS on every change to the safety management system (SMS) data layer.
- **Pattern 2 (MEDIUM):** Any FAIL routes to the Safety Officer responsible for the assumption; assumption YAML included in alert payload.
- **Pattern 3 (CONTESTED):** Pipeline blocks; pages named Compliance Officer. Human determination must be refreshed before change merges.
- **Stale-assumption detection:** Runs nightly; triggers Pattern 3 gate on all dependent tests.

---

## Roadmap (not yet parsed)

| Standard | Title | Priority |
|---|---|---|
| 1910.95 | Occupational Noise Exposure | High — TWA/PEL thresholds are fully DETERMINISTIC; STS provisions are PARAMETERIZED |
| 1910.1000 | Air Contaminants (PEL table) | High — PEL table is DETERMINISTIC; exposure monitoring methodology is PARAMETERIZED |
| 1910.303-305 | Electrical (Wiring Design/Methods) | Medium — largely DETERMINISTIC but NFPA 70 cross-reference creates PARAMETERIZED surface |
| 1910.23 | Ladders | High — most cited after HazCom; height/load requirements are DETERMINISTIC |
| 1910.217 | Mechanical Power Presses | Medium |
| 1926.1053 | Ladders (Construction) | High |
| 1926.1400 | Cranes and Derricks | Medium — load charts are DETERMINISTIC; inspector-judgment provisions are CONTESTED |
| 1926.62 | Lead (Construction) | Medium — AL/PEL DETERMINISTIC; engineering control adequacy PARAMETERIZED |
| 1926.1101 | Asbestos (Construction) | Medium |
