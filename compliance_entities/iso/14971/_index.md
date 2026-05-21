# ISO 14971:2019 — Risk Management for Medical Devices

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Risk management process applicable throughout the full lifecycle of a medical device — concept, design, development, production, post-production
**Authority:** International Organization for Standardization (ISO) / IEC
**Enforcing context:** Required by ISO 13485 §7.1; required by EU MDR Annex I §3; recognized by FDA as a consensus standard for risk management in 21 CFR Part 820/QMSR; required for IVDR
**Current edition:** ISO 14971:2019 (third edition; supersedes 2007)
**Note:** ISO 14971 is a process standard — it defines the risk management process, not the analysis methods. Methods (FMEA, FTA, HAZOP) are described in ISO/TR 24971:2020 (companion technical report).

---

## Summary

| Metric | Count |
|---|---|
| Clauses | 9 (Clauses 3–9 + Annexes) |
| Process steps | 6 (Context → Risk Analysis → Risk Evaluation → Risk Control → Residual Risk Evaluation → Risk Management Report) |
| Sections parsed (individual files) | 1 (risk-management-process.md — all 9 process steps covered) |
| Fully automated (DETERMINISTIC) | Low — risk management is inherently a human judgment process |
| Partial automation (PARAMETERIZED) | Moderate — completeness of risk file; FMEA documentation |
| Human-determination required (CONTESTED) | High — risk acceptability, benefit-risk determination |
| Open assumptions | 7 |

---

## Risk management process — the 6-step cycle

| Step | Clause | Confidence | Notes |
|---|---|---|---|
| 1. Risk management plan | §4.4 | DETERMINISTIC | Written plan required before beginning; 6 required elements |
| 2. Intended use / foreseeable misuse identification | §5.1 | PARAMETERIZED | Intended use documented; foreseeable misuse identified |
| 3. Hazard identification | §5.2 | PARAMETERIZED | All hazards associated with the device identified; sources include clinical, use environment, maintenance |
| 4. Risk estimation | §5.3 | PARAMETERIZED | Severity and probability of harm estimated for each hazard situation |
| 5. Risk evaluation | §6 | CONTESTED | Is risk acceptable per defined criteria? — CONTESTED because criteria are org-defined and may require clinical/regulatory interpretation |
| 6. Risk control | §7 | PARAMETERIZED | Control options selected; effectiveness verified; residual risks evaluated; new risks introduced by controls evaluated |
| 7. Residual risk evaluation | §8 | CONTESTED | Overall residual risk acceptable? Benefit-risk determination if not |
| 8. Risk management review | §9.1 | DETERMINISTIC | Risk management report required before commercial distribution |
| 9. Post-production information | §10 | PARAMETERIZED | Production/post-production information monitored; risk file updated |

---

## Risk management plan (§4.4) — DETERMINISTIC checklist

The plan must include:
1. Scope — device, lifecycle phases, and activities covered
2. Responsibilities and authorities
3. Risk acceptability criteria (probability + severity; or qualitative matrix)
4. Verification activities
5. Criteria for risk management report review

All 5 elements must be present for the plan to satisfy §4.4.

---

## Risk management file — the central evidence artifact

The risk management file is the collection of documents produced by the risk management process. It is the primary evidence artifact for:
- ISO 13485 certification audits (Clause 7.1)
- EU MDR Notified Body assessment (Annex I §3)
- FDA 510(k) or PMA submissions (recognized standard)
- QMSR design history file (§820.30)

File contents:
- Risk management plan
- Hazard identification outputs
- Risk estimation records
- Risk evaluation records
- Risk control measures and verification evidence
- Overall residual risk evaluation and benefit-risk determination (if applicable)
- Post-production monitoring plan
- Risk management report

---

## Risk acceptability criteria — CONTESTED

ISO 14971:2019 removed the prescriptive ALARP (As Low As Reasonably Practicable) triangular model from the normative body. Organizations must define their own acceptability criteria. The criteria become a PARAMETERIZED assumption documented in the risk management plan.

Common industry approaches (documented as assumptions):
- Qualitative risk matrix (e.g., 3×3 or 5×5 severity × probability)
- Quantitative frequency limits (e.g., probability of harm < 10^-6 per device-year)
- Reference to IEC 60601-1 safety requirements for specific device types
- Regulatory guidance-based criteria (FDA guidance, MEDDEV)

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Risk management file | ISO 14971, ISO 13485 §7.1, EU MDR Annex I §3, FDA QMSR §820.30(g) | Same file; different naming (Risk File / DHF content); all require evidence of hazard identification → control → verification |
| FMEA | ISO 14971 (method per ISO/TR 24971), EU AI Act Art. 9 (for AI-enabled devices), IATF 16949 §8.3.3 | FMEA methodology is shared; medical device FMEA uses ISO/TR 24971; automotive uses AIAG-VDA |
| Post-production monitoring | ISO 14971 §10, ISO 13485 §8.2.1 (feedback), EU MDR Art. 83–86 (PMS/PSUR) | Risk file updated based on post-market data; PMS feeds back into risk management |
| Usability engineering | ISO 14971 (use error hazards), IEC 62366-1 (usability) | IEC 62366-1 usability analysis feeds hazard identification in ISO 14971; both required for EU MDR |
| Software risk | ISO 14971, IEC 62304 (software lifecycle) | Software failure modes are hazards in ISO 14971; IEC 62304 safety classification drives software V&V rigor |
