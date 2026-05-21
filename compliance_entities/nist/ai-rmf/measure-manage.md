# NIST AI RMF 1.0 — MEASURE and MANAGE Functions

**Framework:** NIST AI Risk Management Framework (AI RMF) 1.0
**Functions:** MEASURE (1.1–4.2), MANAGE (1.1–4.3)
**Confidence:** DETERMINISTIC gate (testing before deployment) + PARAMETERIZED + CONTESTED
**Last parsed:** 2026-05-21

---

## Scope pre-condition

```python
@pytest.fixture(autouse=True)
def ai_rmf_scope(entity_profile: dict):
    if not entity_profile.get("ai_rmf_in_scope", False):
        pytest.skip("NIST AI RMF not in scope")
```

---

## Constants

```python
# MEASURE — testing is the one DETERMINISTIC gate in AI RMF
AI_RMF_PRE_DEPLOYMENT_TESTING_REQUIRED = True

# MANAGE — monitoring and incident response
AI_RMF_INCIDENT_LOG_REQUIRED = True
AI_RMF_HIGH_RISK_MONITORING_INTERVAL_DAYS = 90  # org-ODP; ASSUME-AIRF-MNG2-001
```

---

## MEASURE — Analyze and Assess AI Risks

### MEASURE 1 — Evaluation Criteria and Metrics

**Overall: PARAMETERIZED — Pattern 2**

```python
import pytest
from datetime import date, timedelta

class TestMEASURE_1_EvaluationCriteria:
    """MEASURE 1 — Evaluation metrics defined for AI trustworthiness characteristics."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-MSR1-001",
        description=(
            "Evaluation metrics are defined for each AI trustworthiness characteristic "
            "applicable to the AI system; at minimum: accuracy/performance metrics for "
            "valid-and-reliable; safety metrics (harm rate, refusal rate for high-risk outputs); "
            "security metrics (adversarial robustness); bias metrics (demographic parity, "
            "equalized odds, or equivalent); explainability metrics where applicable; "
            "metrics selection documented with rationale; metrics reviewed when system changes"
        ),
        approved_by="AI_system_owner",
        review_date="2027-05-21",
    )
    def test_evaluation_metrics_defined_per_ai_system(self, controls_evidence: dict):
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        no_metrics = [
            s for s in ai_systems
            if not s.get("evaluation_metrics_defined", False)
        ]
        assert not no_metrics, (
            f"Evaluation metrics must be defined for each AI system's applicable "
            f"trustworthiness characteristics (NIST AI RMF MEASURE 1.1). "
            f"Missing: {[s['system_id'] for s in no_metrics]}"
        )
```

---

### MEASURE 2 — AI System Testing (DETERMINISTIC gate)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestMEASURE_2_Testing:
    """MEASURE 2 — AI system tested before deployment; bias and security testing performed."""

    def test_ai_systems_tested_before_deployment(self, controls_evidence: dict):
        """DETERMINISTIC: AI testing evidence is required before deployment. No exceptions."""
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        deployed_untested = [
            s for s in ai_systems
            if s.get("deployed", False)
            and not s.get("pre_deployment_testing_completed", False)
        ]
        assert not deployed_untested, (
            f"AI systems must be tested before deployment — testing evidence required. "
            f"Deployed without testing: {[s['system_id'] for s in deployed_untested]}"
        )

    def test_ai_testing_evidence_retained(self, controls_evidence: dict):
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        deployed_systems = [s for s in ai_systems if s.get("deployed", False)]
        missing_evidence = [
            s for s in deployed_systems
            if not s.get("testing_evidence_retained", False)
        ]
        assert not missing_evidence, (
            f"Testing evidence must be retained for deployed AI systems. "
            f"Missing: {[s['system_id'] for s in missing_evidence]}"
        )

    @pytest.mark.assumption(
        id="ASSUME-AIRF-MSR2-001",
        description=(
            "Pre-deployment testing covers: functional performance against defined metrics; "
            "bias testing across relevant demographic subgroups (for systems affecting people); "
            "adversarial/security testing proportionate to risk tier; explainability validation "
            "where the characteristic is required; test datasets are independent of training "
            "data; test results reviewed against acceptance criteria before deployment approval"
        ),
        approved_by="AI_system_owner",
        review_date="2027-05-21",
    )
    def test_bias_testing_performed_for_people_affecting_systems(
        self, controls_evidence: dict
    ):
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        people_affecting = [s for s in ai_systems if s.get("affects_people", False)]
        no_bias_test = [
            s for s in people_affecting
            if not s.get("bias_testing_performed", False)
        ]
        assert not no_bias_test, (
            f"Bias testing must be performed for AI systems affecting people. "
            f"(NIST AI RMF MEASURE 2.5). "
            f"Missing: {[s['system_id'] for s in no_bias_test]}"
        )

    @pytest.mark.assumption(
        id="ASSUME-AIRF-MSR2-002",
        description=(
            "For high-risk AI systems (as defined by org risk tier): adversarial robustness "
            "testing performed (prompt injection, model extraction, evasion attacks for GenAI); "
            "security testing scope defined by risk tier; security testing results reviewed by "
            "AI security specialist before deployment approval; red-team evaluation for highest "
            "risk tier systems per NIST AI 600-1 recommendations"
        ),
        approved_by="CISO_or_AI_governance_lead",
        review_date="2027-05-21",
    )
    def test_security_testing_performed_for_high_risk_ai(
        self, controls_evidence: dict
    ):
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        high_risk = [s for s in ai_systems if s.get("risk_tier") in ("high", "critical")]
        no_security_test = [
            s for s in high_risk
            if not s.get("security_testing_performed", False)
        ]
        assert not no_security_test, (
            f"Security/adversarial testing must be performed for high-risk AI systems "
            f"(NIST AI RMF MEASURE 2.6). "
            f"Missing: {[s['system_id'] for s in no_security_test]}"
        )
```

---

### MEASURE 3 — Explainability and Interpretability

**Overall: CONTESTED — Pattern 3**

```python
class TestMEASURE_3_Explainability:
    """MEASURE 3 — Explainability and interpretability assessed where required."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-MSR3-001",
        description=(
            "For AI systems where explainability is a required trustworthiness characteristic: "
            "explainability requirement is defined (who needs to understand, at what level, "
            "for what purpose); technical approach to explainability documented (LIME, SHAP, "
            "attention maps, rule extraction, or equivalent); note: what constitutes "
            "sufficient explainability is application-specific and cannot be automated"
        ),
        approved_by="AI_system_owner",
        review_date="2027-05-21",
    )
    @pytest.mark.human_review_required(
        reason=(
            "Whether an AI system provides adequate explainability/interpretability "
            "cannot be automatically determined — sufficiency depends on the decision "
            "context, the audience (affected individuals, auditors, regulators), and "
            "whether the explanation enables meaningful understanding of the AI's behavior; "
            "requires qualified human assessment of the explanation quality"
        )
    )
    def test_explainability_requirement_defined_where_applicable(
        self, controls_evidence: dict
    ):
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        explainability_required = [
            s for s in ai_systems if s.get("explainability_required", False)
        ]
        missing_approach = [
            s for s in explainability_required
            if not s.get("explainability_approach_documented", False)
        ]
        assert not missing_approach, (
            f"Explainability approach must be documented for AI systems where explainability "
            f"is required (NIST AI RMF MEASURE 3.1). "
            f"Missing: {[s['system_id'] for s in missing_approach]}"
        )
```

---

### MEASURE 4 — AI Risk Measurement Results

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestMEASURE_4_RiskMeasurementResults:
    """MEASURE 4 — AI incident reports analyzed; risk measurement results documented."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-MSR4-001",
        description=(
            "AI incidents and near-misses are tracked in an incident log; incidents are "
            "analyzed for root cause; root cause analysis results used to update risk "
            "assessments and improve AI risk management processes; incident log reviewed "
            "at minimum quarterly; patterns analyzed at management review; for generative "
            "AI: confabulation incidents and harmful output incidents tracked separately"
        ),
        approved_by="AI_system_owner",
        review_date="2027-05-21",
    )
    def test_ai_incident_log_maintained(self, controls_evidence: dict):
        measure = controls_evidence.get("ai_rmf_measure", {})
        assert measure.get("ai_incident_log_exists", False), (
            "AI incident log must be maintained and incidents analyzed (NIST AI RMF MEASURE 4.1)"
        )
```

---

## MANAGE — Prioritize and Treat AI Risks

### MANAGE 1 — Risk Response Plans

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestMANAGE_1_RiskResponse:
    """MANAGE 1 — Risk response plans documented for identified AI risks."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-MNG1-001",
        description=(
            "Risk response decisions (accept/mitigate/transfer/avoid) are documented for "
            "each identified AI risk; risk acceptance requires explicit approval at the "
            "appropriate authority level (authority level defined by risk tier); mitigation "
            "measures documented with expected residual risk; transfer documented with "
            "third-party risk assessment; risk response decisions reviewed when risk landscape "
            "changes"
        ),
        approved_by="AI_system_owner",
        review_date="2027-05-21",
    )
    def test_risk_response_decisions_documented(self, controls_evidence: dict):
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        no_response_plan = [
            s for s in ai_systems
            if s.get("risk_assessment_completed", False)
            and not s.get("risk_response_documented", False)
        ]
        assert not no_response_plan, (
            f"Risk response decisions must be documented for AI systems with completed "
            f"risk assessments (NIST AI RMF MANAGE 1.1). "
            f"Missing: {[s['system_id'] for s in no_response_plan]}"
        )
```

---

### MANAGE 2 — Post-Deployment Monitoring

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestMANAGE_2_Monitoring:
    """MANAGE 2 — Residual risks monitored post-deployment."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-MNG2-001",
        description=(
            "Post-deployment monitoring program is established for all deployed AI systems; "
            "monitoring metrics align with pre-deployment evaluation metrics; monitoring "
            "frequency proportionate to risk tier: high-risk AI systems monitored at least "
            "quarterly (≤90 days); monitoring covers: performance drift, bias drift, "
            "unexpected output patterns, user feedback signals; monitoring results reviewed "
            "and actioned; monitoring records retained"
        ),
        approved_by="AI_system_owner",
        review_date="2027-05-21",
    )
    def test_post_deployment_monitoring_established(self, controls_evidence: dict):
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        deployed = [s for s in ai_systems if s.get("deployed", False)]
        no_monitoring = [
            s for s in deployed
            if not s.get("monitoring_program_documented", False)
        ]
        assert not no_monitoring, (
            f"Post-deployment monitoring must be established for all deployed AI systems "
            f"(NIST AI RMF MANAGE 2.2). "
            f"Missing: {[s['system_id'] for s in no_monitoring]}"
        )

    def test_high_risk_ai_monitoring_within_interval(
        self, controls_evidence: dict, reference_date: date
    ):
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        high_risk_deployed = [
            s for s in ai_systems
            if s.get("deployed", False)
            and s.get("risk_tier") in ("high", "critical")
        ]
        overdue = [
            s for s in high_risk_deployed
            if s.get("last_monitoring_review_date") is not None
            and s["last_monitoring_review_date"] < reference_date - timedelta(
                days=AI_RMF_HIGH_RISK_MONITORING_INTERVAL_DAYS
            )
        ]
        assert not overdue, (
            f"High-risk AI systems must be monitored at least every "
            f"{AI_RMF_HIGH_RISK_MONITORING_INTERVAL_DAYS} days. "
            f"Overdue: {[s['system_id'] for s in overdue]}"
        )
```

---

### MANAGE 3 — Decommissioning and End-of-Life

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestMANAGE_3_Decommissioning:
    """MANAGE 3 — AI decommissioning plans exist; end-of-life managed."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-MNG3-001",
        description=(
            "Decommissioning plan exists for each deployed AI system and is reviewed "
            "annually; plan covers: notification to affected users/stakeholders, data "
            "retention/deletion per applicable data governance policy, model artifact "
            "archiving, documentation handover; for high-risk AI: decommissioning approved "
            "by AI governance lead"
        ),
        approved_by="AI_system_owner",
        review_date="2027-05-21",
    )
    def test_ai_decommissioning_plan_exists(self, controls_evidence: dict):
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        deployed = [s for s in ai_systems if s.get("deployed", False)]
        no_decom_plan = [
            s for s in deployed
            if not s.get("decommissioning_plan_exists", False)
        ]
        assert not no_decom_plan, (
            f"Decommissioning plan must exist for each deployed AI system "
            f"(NIST AI RMF MANAGE 3.2). "
            f"Missing: {[s['system_id'] for s in no_decom_plan]}"
        )
```

---

### MANAGE 4 — AI Incident Response

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestMANAGE_4_IncidentResponse:
    """MANAGE 4 — AI incident response procedures defined; AI-specific runbooks exist."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-MNG4-001",
        description=(
            "AI incident response procedures exist addressing AI-specific scenarios: "
            "model drift causing harmful outputs, adversarial attack on AI system, "
            "bias incident causing discriminatory outcomes, AI system producing CBRN or "
            "otherwise dangerous content (NIST AI 600-1); IRP integrates with existing "
            "cybersecurity incident response plan; communication procedures cover: "
            "internal escalation, regulatory notification (where required), user notification; "
            "IRP tested at minimum annually via tabletop exercise"
        ),
        approved_by="CISO_or_AI_governance_lead",
        review_date="2027-05-21",
    )
    def test_ai_incident_response_procedures_exist(self, controls_evidence: dict):
        manage = controls_evidence.get("ai_rmf_manage", {})
        assert manage.get("ai_irp_documented", False), (
            "AI-specific incident response procedures must be documented "
            "(NIST AI RMF MANAGE 4.1)"
        )

    @pytest.mark.assumption(
        id="ASSUME-AIRF-MNG4-002",
        description=(
            "For generative AI systems (NIST AI 600-1 scope): incident response addresses "
            "confabulation incidents causing material harm, harmful content generation "
            "incidents, CBRN uplift incidents, intellectual property infringement incidents; "
            "incidents reported to the NIST AI Incident Database or equivalent where "
            "applicable; incident severity classification criteria documented for GenAI-specific "
            "risk categories"
        ),
        approved_by="CISO_or_AI_governance_lead",
        review_date="2027-05-21",
    )
    def test_generative_ai_incident_scenarios_addressed(
        self, controls_evidence: dict, entity_profile: dict
    ):
        if not entity_profile.get("uses_generative_ai", False):
            pytest.skip("Organization does not use generative AI systems")
        manage = controls_evidence.get("ai_rmf_manage", {})
        assert manage.get("genai_incident_scenarios_documented", False), (
            "Generative AI incident scenarios (confabulation, harmful content, CBRN) must "
            "be addressed in AI incident response procedures (NIST AI 600-1)"
        )
```

---

## Generative AI Profile (NIST AI 600-1) — Content Safety Gate

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestGenerativeAI_ContentSafety:
    """NIST AI 600-1 — Generative AI content safety controls."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-GENAI-001",
        description=(
            "Generative AI systems have content filtering or safety controls to prevent "
            "generation of: CBRN-relevant information providing uplift for weapons development, "
            "CSAM, content designed to facilitate mass violence; content filter testing "
            "performed before deployment using standard adversarial prompt datasets; "
            "filter bypass rate documented; acceptable bypass rate threshold defined "
            "based on use case and risk tier; filter performance monitored post-deployment"
        ),
        approved_by="CISO_or_AI_governance_lead",
        review_date="2027-05-21",
    )
    def test_generative_ai_content_safety_controls_tested(
        self, controls_evidence: dict, entity_profile: dict
    ):
        if not entity_profile.get("uses_generative_ai", False):
            pytest.skip("Organization does not use generative AI systems")
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        genai_systems = [s for s in ai_systems if s.get("is_generative_ai", False)]
        no_content_safety = [
            s for s in genai_systems
            if not s.get("content_safety_controls_tested", False)
        ]
        assert not no_content_safety, (
            f"Generative AI systems must have content safety controls tested before deployment "
            f"(NIST AI 600-1). Missing: {[s['system_id'] for s in no_content_safety]}"
        )
```

---

## Open assumptions

| ID | Function | Summary | Review date |
|---|---|---|---|
| ASSUME-AIRF-MSR1-001 | MEASURE 1.1 | Evaluation metrics defined per trustworthiness characteristic; reviewed on changes | 2027-05-21 |
| ASSUME-AIRF-MSR2-001 | MEASURE 2 | Pre-deployment testing: performance, bias, adversarial, explainability; independent test data | 2027-05-21 |
| ASSUME-AIRF-MSR2-002 | MEASURE 2.6 | High-risk AI: adversarial robustness testing; red-team for highest tier | 2027-05-21 |
| ASSUME-AIRF-MSR3-001 | MEASURE 3.1 (CONTESTED) | Explainability approach documented where required; adequacy requires human review | 2027-05-21 |
| ASSUME-AIRF-MSR4-001 | MEASURE 4.1 | AI incident log; root cause analysis; quarterly review; GenAI: confabulation/harmful output tracked | 2027-05-21 |
| ASSUME-AIRF-MNG1-001 | MANAGE 1.1 | Risk response decisions documented; authority level defined by risk tier | 2027-05-21 |
| ASSUME-AIRF-MNG2-001 | MANAGE 2.2 | Monitoring program; high-risk ≤90-day interval; performance + bias drift; records retained | 2027-05-21 |
| ASSUME-AIRF-MNG3-001 | MANAGE 3.2 | Decommissioning plan: user notification, data deletion, model archiving | 2027-05-21 |
| ASSUME-AIRF-MNG4-001 | MANAGE 4.1 | AI IRP: model drift, adversarial attack, bias incident scenarios; annual tabletop test | 2027-05-21 |
| ASSUME-AIRF-MNG4-002 | MANAGE 4.1 (GenAI) | GenAI IRP: confabulation, harmful content, CBRN, IP infringement scenarios | 2027-05-21 |
| ASSUME-AIRF-GENAI-001 | AI 600-1 | Content filter testing before deployment; bypass rate documented; post-deployment monitoring | 2027-05-21 |

---

## Cross-standard notes

**EU AI Act Art. 9 (risk management) ↔ MEASURE/MANAGE:** Pre-deployment testing (MEASURE 2) maps directly to EU AI Act Art. 9(6) — mandatory for high-risk AI systems under Annex III. The DETERMINISTIC testing gate in MEASURE 2 satisfies both frameworks. EU AI Act additionally requires conformity assessment procedures and technical documentation (Annex IV) which are analogous to AI RMF GOVERN/MAP artifacts.

**FDA AI/ML-based SaMD ↔ MEASURE 2:** FDA's predetermined change control plan (PCCP) and performance monitoring requirements align with MANAGE 2 post-deployment monitoring. Pre-market testing of AI/ML-based SaMD maps to MEASURE 2 pre-deployment testing gate.

**SOC 2 vendor assessment ↔ GOVERN 6:** GOVERN 6 third-party AI risk assessment shares infrastructure with SOC 2 Type II vendor reviews — organizations with a vendor assessment program can extend it to include AI-specific risk criteria.
