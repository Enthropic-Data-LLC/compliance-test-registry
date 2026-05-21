# NIST AI RMF 1.0 — GOVERN and MAP Functions

**Framework:** NIST AI Risk Management Framework (AI RMF) 1.0
**Functions:** GOVERN (1.1–6.2), MAP (1.1–5.2)
**Confidence:** PARAMETERIZED-dominant with CONTESTED sub-categories; one DETERMINISTIC gate (regulatory register)
**Last parsed:** 2026-05-21
**Applies to:** Any organization developing, deploying, procuring, or using AI systems; federal agencies and their contractors per US Executive Order 14110 (2023); organizations seeking to align with EU AI Act risk management requirements
**Trigger:** Voluntary adoption; US EO 14110 requires federal agencies to apply AI RMF for high-impact AI; EU AI Act Annex IV references NIST AI RMF as an aligned standard; organizational AI governance decision
**Jurisdiction:** US origin; internationally aligned — NIST coordinated AI RMF with ISO/IEC 42001 (AI Management System) and EU AI Act technical standards
**Not applicable to:** Mandatory compliance in isolation — AI RMF 1.0 is voluntary guidance; no direct penalty for non-adoption except under EO 14110 for federal agencies; does not replace sector-specific AI regulations (EU AI Act, FDA AI/ML guidance, etc.)

---

## Scope pre-condition

```python
def requires_ai_rmf(entity_profile: dict) -> bool:
    """
    True if organization:
    - Has formally adopted NIST AI RMF, OR
    - Is subject to federal procurement requirements citing AI RMF (EO 14110 / NIST AI 100-1), OR
    - Is building or deploying AI systems subject to sector-specific AI governance requirements
      (FDA AI/ML-based SaMD, SEC AI disclosures, EU AI Act with AI RMF as implementation guidance)
    """
    return entity_profile.get("ai_rmf_in_scope", False)
```

---

## Constants

```python
# AI RMF does not prescribe numeric thresholds — these are org-ODP values
AI_RMF_REGULATORY_REGISTER_UPDATE_MONTHS = 12  # recommended maximum review interval
AI_RMF_TEST_REQUIRED_BEFORE_DEPLOYMENT = True   # DETERMINISTIC gate
```

---

## GOVERN — Establish AI Risk Culture and Governance

**Overall: PARAMETERIZED (GOVERN 1–4, 6) / DETERMINISTIC (GOVERN 5) — Pattern 2/1**

### GOVERN 1 — Policies, Processes, Procedures, and Practices

```python
import pytest
from datetime import date, timedelta

@pytest.fixture(autouse=True)
def ai_rmf_scope(entity_profile: dict):
    if not entity_profile.get("ai_rmf_in_scope", False):
        pytest.skip("NIST AI RMF not in scope")

class TestGOVERN_1_Policies:
    """GOVERN 1 — AI risk management policies, processes, procedures established."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-GOV1-001",
        description=(
            "AI risk management policy exists covering: purpose and scope of AI use, "
            "roles and responsibilities for AI governance, accountability for AI decisions, "
            "integration of AI risk into enterprise risk management, policy review cycle; "
            "policy signed at C-suite level; communicated to all personnel involved in AI "
            "development or procurement; reviewed at minimum annually"
        ),
        approved_by="CISO_or_AI_governance_lead",
        review_date="2027-05-21",
    )
    def test_ai_risk_management_policy_exists(self, controls_evidence: dict):
        govern = controls_evidence.get("ai_rmf_govern", {})
        assert govern.get("ai_risk_policy_exists", False), (
            "AI risk management policy must be established (NIST AI RMF GOVERN 1.1)"
        )

    @pytest.mark.assumption(
        id="ASSUME-AIRF-GOV1-002",
        description=(
            "AI risk management process is established and documented covering: AI system "
            "lifecycle stages (design, development, deployment, operation, decommission); "
            "integration points with existing enterprise risk management and software development "
            "processes; process reviewed when significant new AI system types are introduced"
        ),
        approved_by="CISO_or_AI_governance_lead",
        review_date="2027-05-21",
    )
    def test_ai_risk_management_process_documented(self, controls_evidence: dict):
        govern = controls_evidence.get("ai_rmf_govern", {})
        assert govern.get("ai_risk_process_documented", False), (
            "AI risk management process must be documented covering the AI lifecycle "
            "(NIST AI RMF GOVERN 1.2)"
        )
```

---

### GOVERN 2 — Accountability Structures

```python
class TestGOVERN_2_Accountability:
    """GOVERN 2 — Accountability for AI risk management assigned to named roles."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-GOV2-001",
        description=(
            "Accountability for AI risk management is assigned to specific organizational "
            "roles; at minimum: AI system owner (accountable for system risk), AI risk officer "
            "or equivalent (accountable for policy), technical lead (accountable for testing); "
            "accountability documented in RACI matrix or equivalent; roles reviewed when "
            "organization structure changes"
        ),
        approved_by="CISO_or_AI_governance_lead",
        review_date="2027-05-21",
    )
    def test_ai_risk_accountability_assigned(self, controls_evidence: dict):
        govern = controls_evidence.get("ai_rmf_govern", {})
        assert govern.get("ai_accountability_roles_defined", False), (
            "Accountability for AI risk management must be assigned to specific roles "
            "(NIST AI RMF GOVERN 2.1)"
        )
```

---

### GOVERN 3 — Workforce Diversity and Organizational Practices

**Overall: CONTESTED — Pattern 3**

```python
class TestGOVERN_3_Diversity:
    """GOVERN 3 — Teams include diverse perspectives; bias risk acknowledged."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-GOV3-001",
        description=(
            "AI development and governance teams include diverse perspectives to reduce "
            "systemic bias risk; at minimum: representation from domain experts, affected "
            "stakeholder groups, and AI ethics/fairness roles; diversity composition documented; "
            "note: the specific diversity dimensions required depend on the AI use case and "
            "cannot be universally prescribed"
        ),
        approved_by="CISO_or_AI_governance_lead",
        review_date="2027-05-21",
    )
    @pytest.mark.human_review_required(
        reason=(
            "Whether team diversity is adequate to identify and mitigate relevant biases "
            "cannot be automatically verified — adequacy depends on the AI use case, affected "
            "populations, and the specific sources of potential bias; requires human assessor "
            "with knowledge of both the AI application domain and bias risk"
        )
    )
    def test_team_diversity_acknowledged(self, controls_evidence: dict):
        govern = controls_evidence.get("ai_rmf_govern", {})
        assert govern.get("team_diversity_considered", False), (
            "AI teams must include diverse perspectives; diversity considerations must be "
            "documented (NIST AI RMF GOVERN 3.1)"
        )
```

---

### GOVERN 4 — Organizational Commitment

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestGOVERN_4_Commitment:
    """GOVERN 4 — Resources and senior leadership commitment to AI risk management."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-GOV4-001",
        description=(
            "Senior leadership demonstrates commitment to trustworthy AI through: "
            "allocated budget for AI risk management activities, documented in operating plan; "
            "executive sponsor identified for AI governance program; AI risk management "
            "included as agenda item in relevant governance meetings at minimum annually"
        ),
        approved_by="CISO_or_AI_governance_lead",
        review_date="2027-05-21",
    )
    def test_senior_leadership_commitment_to_ai_risk(self, controls_evidence: dict):
        govern = controls_evidence.get("ai_rmf_govern", {})
        assert govern.get("senior_leadership_commitment_documented", False), (
            "Organizational commitment to AI risk management must be evidenced "
            "(NIST AI RMF GOVERN 4.1)"
        )
```

---

### GOVERN 5 — Legal and Regulatory Requirements (DETERMINISTIC gate)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestGOVERN_5_LegalRequirements:
    """GOVERN 5 — Legal and regulatory requirements applicable to AI systems identified."""

    def test_applicable_ai_regulations_register_exists(self, controls_evidence: dict):
        govern = controls_evidence.get("ai_rmf_govern", {})
        assert govern.get("ai_regulatory_register_exists", False), (
            "A register of applicable legal and regulatory requirements for AI must exist "
            "(NIST AI RMF GOVERN 5.1)"
        )

    def test_ai_regulatory_register_current(
        self, controls_evidence: dict, reference_date: date
    ):
        govern = controls_evidence.get("ai_rmf_govern", {})
        last_review = govern.get("regulatory_register_last_review")
        assert last_review is not None, "AI regulatory register last review date must be recorded"
        cutoff = reference_date - timedelta(days=AI_RMF_REGULATORY_REGISTER_UPDATE_MONTHS * 30)
        assert last_review >= cutoff, (
            f"AI regulatory register must be reviewed at least every "
            f"{AI_RMF_REGULATORY_REGISTER_UPDATE_MONTHS} months. "
            f"Last review: {last_review}; cutoff: {cutoff}"
        )
```

---

### GOVERN 6 — Third-Party AI Risks

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestGOVERN_6_ThirdPartyAI:
    """GOVERN 6 — Third-party AI risks identified and managed."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-GOV6-001",
        description=(
            "Third-party AI components (purchased models, APIs, AI platforms, pre-trained "
            "models) are assessed for risk prior to deployment; assessment covers: intended "
            "use alignment, bias/fairness disclosures, data provenance, security posture, "
            "vendor accountability; assessment frequency: at procurement + annually for "
            "high-risk AI; third-party AI risk documented in vendor risk register"
        ),
        approved_by="CISO_or_AI_governance_lead",
        review_date="2027-05-21",
    )
    def test_third_party_ai_risk_assessed(self, controls_evidence: dict):
        govern = controls_evidence.get("ai_rmf_govern", {})
        assert govern.get("third_party_ai_risk_process_exists", False), (
            "Process for assessing third-party AI risks must exist and be applied to "
            "externally provided AI components (NIST AI RMF GOVERN 6.1)"
        )
```

---

## MAP — Identify and Categorize AI Risks

**Overall: PARAMETERIZED-dominant with CONTESTED impact scoring**

### MAP 1 — Context Establishment

```python
class TestMAP_1_Context:
    """MAP 1 — AI system context and intended use established."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-MAP1-001",
        description=(
            "AI system context is established before deployment: intended use cases documented; "
            "foreseeable unintended uses identified; user population and affected stakeholders "
            "identified; deployment environment documented; interaction model (human-in-the-loop, "
            "automated, advisory) documented; context documentation updated when system scope "
            "or use cases change"
        ),
        approved_by="AI_system_owner",
        review_date="2027-05-21",
    )
    def test_ai_system_context_documented(self, controls_evidence: dict):
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        missing_context = [
            s for s in ai_systems
            if not s.get("context_documented", False)
        ]
        assert not missing_context, (
            f"Context documentation must exist for each AI system. "
            f"Missing: {[s['system_id'] for s in missing_context]}"
        )

    @pytest.mark.assumption(
        id="ASSUME-AIRF-MAP1-002",
        description=(
            "Foreseeable unintended uses of the AI system are identified through: use case "
            "analysis, adversarial use scenario workshops, review of analogous system failure "
            "modes; unintended uses documented with risk severity; mitigations considered before "
            "deployment; note: comprehensive unintended use identification requires domain "
            "knowledge that cannot be automated"
        ),
        approved_by="AI_system_owner",
        review_date="2027-05-21",
    )
    def test_unintended_uses_identified(self, controls_evidence: dict):
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        missing_unintended_use = [
            s for s in ai_systems
            if not s.get("unintended_uses_documented", False)
        ]
        assert not missing_unintended_use, (
            f"Foreseeable unintended uses must be identified for each AI system. "
            f"Missing: {[s['system_id'] for s in missing_unintended_use]}"
        )
```

---

### MAP 2 — Scientific Basis and Risk Identification

```python
class TestMAP_2_RiskIdentification:
    """MAP 2 — AI risk categories identified; harm types assessed."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-MAP2-001",
        description=(
            "Potential harms from AI system are identified across harm categories: "
            "physical, psychological, financial, societal/reputational; affected individuals "
            "and communities identified; harm likelihood and magnitude estimated using "
            "org-defined risk scoring methodology; harm identification updated when system "
            "capability, deployment context, or population changes"
        ),
        approved_by="AI_system_owner",
        review_date="2027-05-21",
    )
    def test_potential_harms_identified_per_ai_system(self, controls_evidence: dict):
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        missing_harm_assessment = [
            s for s in ai_systems
            if not s.get("harm_identification_documented", False)
        ]
        assert not missing_harm_assessment, (
            f"Potential harms must be identified for each AI system (NIST AI RMF MAP 2.1). "
            f"Missing: {[s['system_id'] for s in missing_harm_assessment]}"
        )
```

---

### MAP 3 — AI Risk Categorization

```python
class TestMAP_3_Categorization:
    """MAP 3 — AI system categorized by risk tier."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-MAP3-001",
        description=(
            "AI systems are categorized into risk tiers based on: potential impact magnitude, "
            "affected population size, level of human oversight, reversibility of harm; "
            "risk tier determines: required testing depth, monitoring frequency, human oversight "
            "requirements, incident escalation thresholds; tier assignment documented and "
            "reviewed at least annually or when system capabilities change significantly"
        ),
        approved_by="CISO_or_AI_governance_lead",
        review_date="2027-05-21",
    )
    def test_ai_systems_categorized_by_risk_tier(self, controls_evidence: dict):
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        uncategorized = [
            s for s in ai_systems
            if not s.get("risk_tier_assigned", False)
        ]
        assert not uncategorized, (
            f"Each AI system must be assigned a risk tier/category. "
            f"Uncategorized: {[s['system_id'] for s in uncategorized]}"
        )
```

---

### MAP 5 — Data Provenance and Quality

```python
class TestMAP_5_DataProvenance:
    """MAP 5 — Data provenance and quality assessed for training and operational data."""

    @pytest.mark.assumption(
        id="ASSUME-AIRF-MAP5-001",
        description=(
            "Training data provenance documented: data sources, collection methods, "
            "known limitations, bias risks; data quality assessment performed including: "
            "completeness, representativeness, labeling accuracy; provenance documentation "
            "retained with model version; for generative AI (NIST AI 600-1): additional "
            "documentation of web-scraped or licensed content and copyright/IP risk assessment"
        ),
        approved_by="AI_data_owner",
        review_date="2027-05-21",
    )
    def test_training_data_provenance_documented(self, controls_evidence: dict):
        ai_systems = controls_evidence.get("ai_rmf_ai_systems", [])
        missing_provenance = [
            s for s in ai_systems
            if s.get("uses_training_data", True)
            and not s.get("training_data_provenance_documented", False)
        ]
        assert not missing_provenance, (
            f"Training data provenance must be documented for AI systems. "
            f"Missing: {[s['system_id'] for s in missing_provenance]}"
        )
```

---

## Open assumptions

| ID | Function | Summary | Review date |
|---|---|---|---|
| ASSUME-AIRF-GOV1-001 | GOVERN 1.1 | AI risk policy; C-suite signed; annual review; communicated to AI personnel | 2027-05-21 |
| ASSUME-AIRF-GOV1-002 | GOVERN 1.2 | AI risk process covers full lifecycle; integrates with ERM | 2027-05-21 |
| ASSUME-AIRF-GOV2-001 | GOVERN 2.1 | Accountability RACI: system owner, risk officer, technical lead | 2027-05-21 |
| ASSUME-AIRF-GOV3-001 | GOVERN 3.1 (CONTESTED) | Team diversity documented; adequacy requires human review | 2027-05-21 |
| ASSUME-AIRF-GOV4-001 | GOVERN 4.1 | Budget allocated; executive sponsor identified; governance meeting agenda | 2027-05-21 |
| ASSUME-AIRF-GOV6-001 | GOVERN 6.1 | Third-party AI assessed at procurement + annually for high-risk | 2027-05-21 |
| ASSUME-AIRF-MAP1-001 | MAP 1.1 | Context doc: intended use, unintended use, user population, deployment env | 2027-05-21 |
| ASSUME-AIRF-MAP1-002 | MAP 1.2 | Unintended uses identified via scenario analysis; mitigations considered | 2027-05-21 |
| ASSUME-AIRF-MAP2-001 | MAP 2.1 | Harm identification: physical/psychological/financial/societal; updated on changes | 2027-05-21 |
| ASSUME-AIRF-MAP3-001 | MAP 3.1 | Risk tier assignment; tier determines testing depth and oversight requirements | 2027-05-21 |
| ASSUME-AIRF-MAP5-001 | MAP 5.1 | Training data provenance: sources, limitations, bias risks; generative AI IP risk | 2027-05-21 |

---

## Cross-standard notes

**EU AI Act alignment:** GOVERN 5 (regulatory register) and MAP 3 (risk categorization) map directly to EU AI Act Article 9 (risk management) and the high-risk AI system classification (Annex III). An organization satisfying NIST AI RMF GOVERN/MAP has completed most of the groundwork for EU AI Act conformity assessment.

**ISO/IEC 42001:2023:** GOVERN function maps to ISO/IEC 42001 Clauses 4–6 (context, leadership, planning). The AI RMF is more prescriptive at the MAP/MEASURE level; ISO/IEC 42001 provides the management system structure. Organizations pursuing certification typically use ISO 42001 as the QMS shell and AI RMF as the risk methodology.
