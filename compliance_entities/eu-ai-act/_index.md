# EU AI Act — Regulation (EU) 2024/1689

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** All AI systems placed on or put into service in the EU market; extra-territorial application similar to GDPR
**Authority:** European AI Office (EAIO); national competent authorities per member state; notified bodies for high-risk AI conformity assessment
**Enforcing context:** Providers (developers), deployers (users), importers, and distributors of AI systems affecting EU persons
**In force:** August 1 2024; phased enforcement: GPAI rules Aug 2025; High-risk AI (Annex I) Aug 2026; High-risk AI (Annex III) Aug 2026; full enforcement Aug 2027

---

## Summary

| Metric | Count |
|---|---|
| Risk tiers | 4 (Unacceptable / High / Limited / Minimal) |
| Prohibited practices (Article 5) | 8 |
| High-risk AI categories (Annex III) | 8 + Annex I (safety components) |
| GPAI model tiers | 2 (general-purpose / systemic risk GPAI) |
| Articles | 113 + 13 Annexes |
| Articles parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | Low–moderate — prohibited use list, registration in EU database, conformity assessment pathway |
| Partial automation (PARAMETERIZED) | Dominant |
| Human-determination required (CONTESTED) | Significant — high-risk classification, fundamental rights impact assessment |
| Open assumptions | 0 |

---

## Risk classification — pre-condition to all tests

AI Act obligations are tier-dependent. Classification is the root fixture.

| Tier | Definition | Obligations |
|---|---|---|
| **Unacceptable risk** | Art. 5 — 8 prohibited practices | Complete ban; no compliance path |
| **High risk — Annex I** | Safety components of products already governed by EU harmonisation legislation (medical devices, machinery, vehicles, etc.) | Full conformity assessment; technical documentation; human oversight; registration |
| **High risk — Annex III** | AI in 8 sensitive domains (biometrics, critical infrastructure, education, employment, essential services, law enforcement, migration, justice) | Same as Annex I |
| **Limited risk** | AI with specific transparency obligations (chatbots, emotion recognition, deepfakes) | Disclosure to users |
| **Minimal/no risk** | All other AI (spam filters, recommendation engines, most enterprise AI) | No mandatory obligations; voluntary codes of practice |
| **GPAI models** | General-purpose AI models (LLMs, foundation models) | Transparency, copyright documentation; systemic-risk models: adversarial testing, incident reporting |

---

## Prohibited practices (Article 5) — DETERMINISTIC

These are absolute prohibitions; no balancing test:

| Prohibition | Description |
|---|---|
| Art. 5(1)(a) | Subliminal manipulation of behavior causing harm |
| Art. 5(1)(b) | Exploiting vulnerabilities of specific groups (age, disability) |
| Art. 5(1)(c) | Social scoring by public authorities |
| Art. 5(1)(d) | Real-time remote biometric identification in public spaces by law enforcement (with narrow exceptions) |
| Art. 5(1)(e) | Emotion recognition in workplace/education (with exceptions for safety/medical) |
| Art. 5(1)(f) | Biometric categorization based on sensitive characteristics (race, political, religion, etc.) |
| Art. 5(1)(g) | Untargeted facial image scraping for recognition databases |
| Art. 5(1)(h) | AI to predict criminal recidivism based on protected characteristics |

**RDF treatment:** Each prohibition generates a Pattern 1 binary test: does this AI system perform this function? If yes — immediate escalation; prohibited.

---

## High-risk AI (Annex III) — 8 domains

| Domain | Examples | Confidence |
|---|---|---|
| 1. Biometrics | Remote biometric ID systems; emotion recognition; biometric categorization | PARAMETERIZED — scope boundaries |
| 2. Critical infrastructure | AI managing water, gas, electricity, transport networks | PARAMETERIZED |
| 3. Education/training | AI determining admission, exam scores, educational assessment | PARAMETERIZED |
| 4. Employment | AI for recruitment, CV screening, job assignment, performance monitoring, dismissal | PARAMETERIZED |
| 5. Essential services | AI for creditworthiness, insurance risk, emergency dispatch | PARAMETERIZED |
| 6. Law enforcement | AI for individual risk assessment, lie detection, crime prediction, evidence analysis | PARAMETERIZED |
| 7. Migration/asylum/border | AI for visa/asylum assessment, border control | PARAMETERIZED |
| 8. Justice/democracy | AI for legal research, judicial decisions, electoral processes | PARAMETERIZED |

---

## High-risk AI obligations — confidence map

| Obligation | Article | Confidence | Notes |
|---|---|---|---|
| Risk management system | Art. 9 | PARAMETERIZED | Continuous iterative risk management process throughout lifecycle |
| Data governance | Art. 10 | PARAMETERIZED | Training data relevance, representativeness, freedom from errors; bias monitoring |
| Technical documentation | Art. 11 + Annex IV | DETERMINISTIC | Must exist before market placement; 8 required sections per Annex IV |
| Record keeping / logging | Art. 12 | DETERMINISTIC | Automatic logging capability required; logs retained by deployer |
| Transparency to deployers | Art. 13 | PARAMETERIZED | Instructions for use; capabilities and limitations; intended purpose |
| Human oversight | Art. 14 | PARAMETERIZED | Humans able to understand, monitor, intervene, override system |
| Accuracy, robustness, cybersecurity | Art. 15 | PARAMETERIZED | Appropriate levels of accuracy; resilience to errors; adversarial robustness |
| Quality management system | Art. 17 | PARAMETERIZED | QMS covering all development/deployment phases |
| Technical documentation retention | Art. 18 | DETERMINISTIC | 10 years after last placement on market |
| Logging retention (deployer) | Art. 19 | DETERMINISTIC | Deployer retains logs for at least 6 months |
| Conformity assessment | Art. 43 | DETERMINISTIC | Self-assessment or third-party per Annex VI/VII; CE marking |
| EU database registration | Art. 49 | DETERMINISTIC | Registration in EU AI Act database before placement |
| Post-market monitoring | Art. 72 | PARAMETERIZED | PMS plan; incident reporting; SSCP updates |
| Serious incident reporting | Art. 73 | DETERMINISTIC | Report to national authority within 15 days (death/serious health) or 3 months (other) |
| Fundamental rights impact assessment (FRIA) | Art. 27 | CONTESTED | Deployers in sensitive domains; methodology not specified |

---

## GPAI model obligations (Title VIII, Articles 51–56)

| Tier | Threshold | Obligations |
|---|---|---|
| General GPAI | All GPAI models | Technical documentation; copyright compliance (training data transparency); comply with AI Office requests |
| Systemic-risk GPAI | Trained with > 10^25 FLOPs (approx. GPT-4 scale and above) | All GPAI obligations + adversarial testing; incident reporting to AI Office; cybersecurity measures; energy efficiency |

**Systemic-risk incident reporting:** Report to AI Office without undue delay; serious incidents defined as significant harm to persons, infrastructure, public services.

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Article |
|---|---|---|
| Technical documentation retention | 10 years from last market placement | Art. 18 |
| Deployer log retention | Minimum 6 months | Art. 19 |
| Serious incident — death/serious harm | Report within 15 calendar days | Art. 73 |
| Serious incident — other | Report within 3 months | Art. 73 |
| EU database registration | Before placement on market | Art. 49 |
| Conformity assessment before CE marking | Before market placement | Art. 43 |
| GPAI systemic risk threshold | > 10^25 training FLOPs | Art. 51 |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Risk management | EU AI Act Art. 9, ISO 14971 (medical device AI), NIST AI RMF | Converging methodologies; ISO 14971 principles applicable to AI in medical devices |
| Technical documentation | EU AI Act Annex IV, EU MDR Annex II, FDA AI/ML guidance | AI systems embedded in medical devices must satisfy both EU AI Act and EU MDR documentation |
| Cybersecurity | EU AI Act Art. 15, EU CRA (Cyber Resilience Act), ISO 27001 A.8 | High-risk AI must meet cybersecurity requirements; CRA applies if AI embedded in product |
| Data governance | EU AI Act Art. 10, GDPR Art. 5 (data minimization/accuracy), ISO 27001 A.5.12 | Training data governance overlaps with GDPR personal data requirements |
| Incident reporting | EU AI Act Art. 73, EU MDR Art. 87, DORA Art. 19 | Different recipients; same IRP infrastructure |

---

## Roadmap — parse priority

1. Art. 5 (Prohibited practices) — DETERMINISTIC; highest enforcement risk
2. Art. 49 (EU database registration) — DETERMINISTIC binary gate
3. Annex IV (Technical documentation) — DETERMINISTIC checklist
4. Art. 73 (Incident reporting timelines) — DETERMINISTIC deadlines
5. Art. 43 (Conformity assessment pathway) — DETERMINISTIC by risk tier
6. Art. 12/19 (Logging requirements) — DETERMINISTIC retention periods
7. Art. 9 (Risk management) — PARAMETERIZED; Pattern 2 dominant
8. Art. 14 (Human oversight) — PARAMETERIZED
9. Art. 27 (FRIA) — CONTESTED; Pattern 3 dominant
