# IEC 62304:2006+AMD1:2015 — Medical Device Software Lifecycle Processes

**Authority:** IEC
**Scope:** Software that is a medical device (SaMD) or embedded in a medical device; required by EU MDR Annex I §17; recognized by FDA; required by ISO 13485 §7.3

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — 9 clauses, Class A/B/C confidence map, traceability requirements, SOUP, SDP 9-element checklist | ✅ |
| [`software-development-controls.md`](./software-development-controls.md) | Clauses 4 (general, SOUP, safety class), 5 (SDP 9 elements, requirements, architecture B/C, unit testing B/C, integration B/C, system testing all, release), 8 (config management, versioning, baselines, change control, traceability gate) | ✅ |
| [`maintenance-risk-problem-resolution.md`](./maintenance-risk-problem-resolution.md) | Clause 6 (maintenance plan, impact analysis, safety reclassification, regression testing), 7 (hazard identification B/C, risk control implementation + verification, change hazard assessment), 9 (problem reports, root cause, safety impact, change control, trend analysis B/C, resolution verification B/C) | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Class scope | Clause |
|---|---|---|
| Software development plan (9 elements) | A/B/C | 5.1 |
| Software requirements documented | A/B/C | 5.2 |
| Architectural design documented | B/C only | 5.3 |
| Unit testing/verification required | B/C (A waivable with justification) | 5.5 |
| Integration testing records | B/C only | 5.6 |
| System testing records | A/B/C | 5.7 |
| Release authorization documented | A/B/C | 5.8 |
| All software items uniquely versioned | A/B/C | 8.1 |
| SOUP components documented | A/B/C | 8.1.2 |
| Maintenance plan for released software | A/B/C | 6.1 |
| Impact analysis for each modification | A/B/C | 6.2 |
| Safety class re-evaluated on modification | A/B/C | 6.2 |
| Problem reports for all software problems | A/B/C | 9.1 |
| Safety impact per problem report | A/B/C | 9.2 |
| Hazard-contributing software items identified | B/C only | 7.1 |
| Risk control verification in risk file | B/C only | 7.3 |

## Assumption count

| File | Assumptions |
|---|---|
| software-development-controls.md | 1 (traceability matrix) |
| maintenance-risk-problem-resolution.md | 0 (all DETERMINISTIC) |
| **Total** | **1** |

## Parse status: Complete — 2 spec files; 1 assumption; DETERMINISTIC-dominant; Class B/C gating throughout
