# NRC 10 CFR Part 26 — Fitness for Duty Programs

**Registry version:** 2026.05
**Last updated:** 2026-05-21
**Scope:** Fitness for duty (FFD) programs for personnel with unescorted access to nuclear power plants; drug and alcohol testing; work hour controls; behavioral observation
**Authority:** U.S. Nuclear Regulatory Commission (NRC)
**Enforcing context:** All NRC-licensed nuclear power reactor licensees; contractors and vendors with unescorted access

---

## Summary

| Metric | Count |
|---|---|
| Key subparts | Subpart A (General), Subpart B (FFD Policy/Program), Subpart C (Testing), Subpart D (Laboratories), Subpart E (Cutoff Levels), Subpart F (MRO), Subpart G (Adverse Actions), Subpart H (Work Hours), Subpart I (Audits/Records) |
| Sections parsed | 1 (fitness-for-duty.md — §26.31 random testing, §26.163 cutoffs, §26.205 work hours, §26.61 pre-access, §26.65 for-cause) |
| Fully automated (DETERMINISTIC) | High — random testing rates, work hour limits, drug/alcohol cutoffs, testing timing windows |
| Partial automation (PARAMETERIZED) | Moderate — behavioral observation program, MRO determination process |
| Human-determination required (CONTESTED) | Low — suitability determinations, waiver decisions |
| Open assumptions | 6 (ASSUME-NRC26-FFD-001–006) |

---

## Per-section confidence map

### §26.31 — Drug and Alcohol Testing Categories (DETERMINISTIC)

| Testing type | Trigger | Timing | Confidence |
|---|---|---|---|
| Pre-access testing | Before granting unescorted access | Before access granted | DETERMINISTIC |
| Random testing — drugs | Random selection; ≥50% of covered workforce per year | Unannounced; no advance notice | DETERMINISTIC (rate) |
| Random testing — alcohol | Random selection; ≥50% of covered workforce per year | Unannounced | DETERMINISTIC (rate) |
| For-cause — behavior/observation | Reasonable suspicion of impairment | Within 2 hours of observation for alcohol; 32 hours for drug | DETERMINISTIC (timing) |
| For-cause — accident/event | After an event meeting §26.65(b) criteria | Within 2 hours for alcohol | DETERMINISTIC (timing) |
| Follow-up testing | After return to covered duties following violation | Unannounced; minimum frequency per MRO plan | PARAMETERIZED |

### §26.163 — Drug Detection Cutoff Levels (DETERMINISTIC)

| Drug | Initial cutoff | Confirmation cutoff |
|---|---|---|
| Marijuana metabolites (THCA) | 50 ng/mL | 15 ng/mL |
| Cocaine metabolites | 150 ng/mL | 100 ng/mL |
| Opiates (morphine/codeine) | 2000 ng/mL | 2000 ng/mL |
| Opiates (6-MAM — heroin marker) | 10 ng/mL | 10 ng/mL |
| Phencyclidine (PCP) | 25 ng/mL | 25 ng/mL |
| Amphetamines (AMPH/METH) | 500 ng/mL | 250 ng/mL |
| MDMA (ecstasy) | 500 ng/mL | 250 ng/mL |
| Alcohol (breath) — removal level | ≥0.02 BAC | N/A |
| Alcohol (breath) — confirmed positive | ≥0.04 BAC | N/A |

### §26.205 — Work Hour Controls (DETERMINISTIC)

| Limit | Threshold | Period |
|---|---|---|
| Maximum consecutive working hours | 16 hours | Any shift |
| Minimum break between shifts | 10 hours | Before next shift |
| Maximum hours in 48-hour period | 26 hours | Any rolling 48-hour window |
| Maximum hours in 7-day period | 72 hours | Any rolling 7-day window |
| Maximum consecutive night shifts | 6 shifts | Night defined as hours including midnight |

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Section |
|---|---|---|
| Random drug testing rate | ≥50% of covered workers per year | §26.31(c)(3)(ii) |
| Random alcohol testing rate | ≥50% of covered workers per year | §26.31(c)(3)(ii) |
| Pre-access testing | Required before first unescorted access grant | §26.61 |
| Behavioral observation — initial certification | Trained BOP observers before unescorted access | §26.27(d) |
| For-cause testing — alcohol (breath) | Within 2 hours of reasonable suspicion or qualifying event | §26.65(c)(2) |
| For-cause testing — drug (urine) | Within 32 hours of qualifying event | §26.65(c)(3) |
| Alcohol removal level | ≥0.02 BAC — removal from covered duties | §26.189(b)(2) |
| Alcohol confirmed positive | ≥0.04 BAC — violation | §26.189(c) |
| Maximum consecutive working hours | 16 hours | §26.205(d)(1) |
| Minimum break between shifts | 10 hours | §26.205(d)(2) |
| Maximum hours in 48-hour period | 26 hours | §26.205(d)(3) |
| Maximum hours in 7-day period | 72 hours | §26.205(d)(4) |
| Maximum consecutive night shifts | 6 shifts | §26.205(d)(5) |
| Annual FFD program audit | Annually | §26.41 |
| Drug testing records retention | 5 years (general); indefinite for violations | §26.715 |

---

## Open assumption registry

| ID | Section | Summary | Review date |
|---|---|---|---|
| ASSUME-NRC26-FFD-001 | §26.31(c)(3) | Random testing rate: ≥50% calculated as number of tests conducted ÷ average covered workforce size; drug and alcohol pools may be separate; tested more than once counts once toward pool eligibility not rate denominator | 2026-05-21 |
| ASSUME-NRC26-FFD-002 | §26.163 | Drug cutoff levels: §26.163 specifies minimum sensitivity; HHS-certified labs must use these as minimum; initial (immunoassay) vs. confirmation (GC/MS or LC/MS/MS) levels distinct | 2026-05-21 |
| ASSUME-NRC26-FFD-003 | §26.189 | Alcohol: ≥0.02 BAC removal from FFD activities (not a violation unless ≥0.04); 0.02 result = second test within 30 minutes; confirmed ≥0.04 = violation, removal, notification; tested individual notified by qualified breath alcohol technician (BAT) | 2026-05-21 |
| ASSUME-NRC26-FFD-004 | §26.205 | Work hour limits: 10-hour minimum break is from release to reporting; consecutive night shifts = night defined as shift that includes hours between midnight and 0600; limits apply to covered individuals performing activities affecting nuclear safety | 2026-05-21 |
| ASSUME-NRC26-FFD-005 | §26.205(f) | Work hour waivers: licensee may grant waivers for work hour limits in emergencies (§26.207); must document reason, duration, and hours; 26.207(a)(1)-(3) specifies valid waiver bases; waivers do not excuse minimum rest requirements unless emergency necessity demonstrated | 2026-05-21 |
| ASSUME-NRC26-FFD-006 | §26.27 | Behavioral observation program (BOP): personnel with unescorted access must be observed by trained supervisors/coworkers; observations logged; fitness concerns escalated to FFD coordinator; BOP is required element of Part 26 program | 2026-05-21 |

---

## Contested items

| Item | Section | Reason |
|---|---|---|
| Suitability determination after positive test | §26.185/§26.187 | Whether an individual is suitable to return to covered duties after FFD violation involves MRO evaluation, SAP recommendation, and licensee determination; multi-factor judgment | 
| Work hour waiver necessity | §26.207 | Whether a waiver is warranted for a specific operational event requires judgment about whether alternative staffing was truly unavailable |

---

## Specification file status

| File | Contents | Status |
|---|---|---|
| `fitness-for-duty.md` | §26.31 random testing rates; §26.61 pre-access; §26.65 for-cause; §26.163 cutoff levels; §26.189 alcohol; §26.205 work hours; §26.207 waivers | ✅ Parsed |

---

## Remaining parse priority

| Priority | Section | Rationale |
|---|---|---|
| 1 | ~~§26.31/§26.163/§26.205 (core FFD)~~ | ✅ Parsed — `fitness-for-duty.md` |
| 2 | §26.41 (audit requirements) + §26.715 (records retention) | Procedural/administrative completeness |
