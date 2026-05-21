# NIST AI RMF 1.0 — AI Risk Management Framework

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Voluntary framework for managing risks associated with AI systems throughout the AI lifecycle; applicable to any organization developing, deploying, or using AI
**Authority:** NIST (National Institute of Standards and Technology); published January 2023
**Enforcing context:** Voluntary — not a regulation. Becomes effectively mandatory when: cited in federal procurement (EO 14110); adopted by sector-specific regulators (FDA AI guidance, SEC AI disclosures); referenced in contractual requirements; used as EU AI Act implementation guidance
**Companion resources:** NIST AI RMF Playbook; Generative AI Profile (NIST AI 600-1); Trustworthy AI characteristics
**Relationship to other frameworks:** Maps to ISO/IEC 23894, ISO/IEC 42001, EU AI Act, and NIST CSF

---

## Summary

| Metric | Count |
|---|---|
| Core functions | 4 (GOVERN / MAP / MEASURE / MANAGE) |
| Subcategories | ~70 |
| AI trustworthiness characteristics | 7 |
| Sections parsed (individual files) | 2 (govern-map.md + measure-manage.md) |
| Fully automated (DETERMINISTIC) | Low — 1 DETERMINISTIC gate: pre-deployment testing; 1 DETERMINISTIC record: regulatory register |
| Partial automation (PARAMETERIZED) | Dominant |
| Human-determination required (CONTESTED) | Moderate — team diversity adequacy, explainability sufficiency |
| Open assumptions | 22 |

---

## Note on regulatory status

NIST AI RMF is guidance. For test purposes, all requirements are PARAMETERIZED or CONTESTED unless an organization has formally adopted the framework or a binding regulation requires it. The EU AI Act and EO 14110 reference compatible standards — AI RMF serves as a mapping bridge.

---

## 7 AI trustworthiness characteristics

All AI risk management decisions are measured against these properties:

| Characteristic | Description | RDF Confidence |
|---|---|---|
| Valid and reliable | Performs intended function accurately and consistently | PARAMETERIZED |
| Safe | Does not cause harm to people or the environment | PARAMETERIZED/CONTESTED |
| Secure and resilient | Resists adversarial attacks; degrades gracefully | PARAMETERIZED |
| Explainable and interpretable | Decisions understandable by appropriate stakeholders | CONTESTED |
| Privacy-enhanced | Protects personal data and respects privacy | PARAMETERIZED |
| Fair — bias managed | Free from inappropriate bias; equitable outcomes | CONTESTED |
| Accountable and transparent | Responsibility assigned; decisions auditable | PARAMETERIZED |

---

## 4 Core Functions — confidence map

### GOVERN — establish AI risk culture and governance

| Subcategory area | Confidence | Notes |
|---|---|---|
| AI risk management policies established | PARAMETERIZED | Written AI risk management policy |
| Roles and responsibilities for AI risk | PARAMETERIZED | Accountability assigned to named roles |
| Organizational risk tolerance for AI defined | CONTESTED | Risk tolerance is inherently organization-specific |
| Teams include diverse perspectives | CONTESTED | Diversity assessment is subjective |
| Legal/regulatory requirements identified | DETERMINISTIC | Register of applicable AI regulations maintained |
| Processes for third-party AI risks | PARAMETERIZED | Third-party AI assessments |

### MAP — identify and categorize AI risks

| Subcategory area | Confidence | Notes |
|---|---|---|
| AI system context established (intended/unintended uses) | PARAMETERIZED | Use case documentation |
| Potential harms identified | PARAMETERIZED | Harm categories: physical / psychological / financial / societal |
| Impact magnitude and likelihood estimated | CONTESTED | Risk scoring methodology org-defined |
| AI system categorized (risk tier) | PARAMETERIZED | Category determines required controls |
| Data provenance and quality assessed | PARAMETERIZED | Training data documentation |

### MEASURE — analyze and assess AI risks

| Subcategory area | Confidence | Notes |
|---|---|---|
| Evaluation metrics defined for trustworthiness characteristics | PARAMETERIZED | Metrics selection org-defined |
| AI system tested before deployment | DETERMINISTIC | Testing evidence required |
| Bias testing performed | PARAMETERIZED | Demographic performance analysis |
| Explainability/interpretability assessed | CONTESTED | Subjective assessment |
| AI incident reports analyzed | PARAMETERIZED | Incidents tracked; root cause analyzed |

### MANAGE — prioritize and treat AI risks

| Subcategory area | Confidence | Notes |
|---|---|---|
| Risk response plan for identified AI risks | PARAMETERIZED | Accept/mitigate/transfer/avoid decisions documented |
| Residual risks monitored post-deployment | PARAMETERIZED | Monitoring cadence defined |
| AI decommissioning plan | PARAMETERIZED | End-of-life plan for AI systems |
| Incident response for AI-specific scenarios | PARAMETERIZED | AI incident runbooks |
| Risk management processes improved iteratively | PARAMETERIZED | Continuous improvement |

---

## Generative AI Profile (NIST AI 600-1) — selected risks

NIST AI 600-1 extends the AI RMF for generative AI (large language models, image generators, etc.):

| Risk | Description | RDF Confidence |
|---|---|---|
| CBRN information capability | Model assists with weapons of mass destruction | CONTESTED — threshold unclear |
| Confabulation (hallucination) | Plausible but false outputs | PARAMETERIZED — factual verification testing |
| Data privacy | Training on personal data; privacy-invasive outputs | PARAMETERIZED |
| Human-AI configuration | Over-reliance; automation bias | CONTESTED |
| Intellectual property | Copyright infringement in outputs | CONTESTED |
| Obscene/harmful/violent content | Unsafe content generation | PARAMETERIZED — content filter testing |
| Cybersecurity vulnerabilities | Code generation with security flaws | PARAMETERIZED |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| AI risk governance | NIST AI RMF GOVERN, EU AI Act Art. 9, ISO/IEC 42001 | Same governance structure; EU AI Act makes it mandatory for high-risk AI |
| AI testing and validation | NIST AI RMF MEASURE, EU AI Act Annex IV (technical documentation), FDA AI/ML-based SaMD | Same testing methodology |
| Bias and fairness | NIST AI RMF MEASURE, EU AI Act Art. 10 (data governance), EEOC (employment AI) | Different enforcement contexts |
| Incident reporting | NIST AI RMF MANAGE, EU AI Act Art. 73, SEC cybersecurity rules | AI incidents may trigger cybersecurity or regulatory reporting |
| Third-party AI risk | NIST AI RMF GOVERN, EU AI Act Art. 28 (deployer obligations), SOC 2 | Shared vendor assessment infrastructure |
