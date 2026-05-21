# NIST AI RMF 1.0 — AI Risk Management Framework

**Authority:** NIST (National Institute of Standards and Technology)
**Scope:** Voluntary framework for AI risk management; effectively mandatory under EO 14110 federal procurement, FDA AI/ML-based SaMD, and as EU AI Act implementation guidance
**Companion:** NIST AI 600-1 (Generative AI Profile)

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — 4 functions, 7 trustworthiness characteristics, ~70 subcategories, regulatory status note, cross-standard dependencies | ✅ |
| [`govern-map.md`](./govern-map.md) | GOVERN (1–6): AI risk policy, process, accountability RACI, team diversity (CONTESTED), regulatory register (DETERMINISTIC), third-party AI risk; MAP (1–5): context/intended use, unintended use, harm identification, risk categorization, data provenance | ✅ |
| [`measure-manage.md`](./measure-manage.md) | MEASURE (1–4): evaluation metrics, **pre-deployment testing (DETERMINISTIC gate)**, bias testing, adversarial testing (high-risk), explainability (CONTESTED), incident tracking; MANAGE (1–4): risk response plans, post-deployment monitoring, decommissioning plans, AI IRP; NIST AI 600-1 content safety gate | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Function |
|---|---|---|
| AI regulatory register | Must exist + reviewed ≤12 months | GOVERN 5.1 |
| Pre-deployment testing | Required before any AI system deployment | MEASURE 2 |
| Testing evidence retention | Required for all deployed AI systems | MEASURE 2 |
| High-risk AI monitoring interval | ≤90 days (org-ODP) | MANAGE 2.2 |

## CONTESTED gates (human review required)

| Gate | Function | Reason |
|---|---|---|
| Team diversity adequacy | GOVERN 3.1 | Adequacy is use-case and population specific |
| Explainability/interpretability sufficiency | MEASURE 3.1 | Sufficiency depends on audience and decision context |

## Assumption count

| File | Assumptions |
|---|---|
| govern-map.md | 11 |
| measure-manage.md | 11 |
| **Total** | **22** |

## Parse status: Complete — 2 spec files; 22 assumptions; 1 DETERMINISTIC gate (pre-deployment testing); 2 CONTESTED gates
