# ISO 9001:2015 — Management and Process Controls

**Framework:** ISO 9001:2015
**Clauses:** 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 6.1, 6.3, 7.1, 7.3, 7.4, 8.1–8.5, 9.1, 10.1, 10.3
**Confidence:** PARAMETERIZED-dominant (management system + process approach clauses)
**Last parsed:** 2026-05-21

---

## Scope pre-condition

```python
@pytest.fixture(autouse=True)
def iso9001_scope(entity_profile: dict):
    if not entity_profile.get("iso9001_in_scope", False):
        pytest.skip("ISO 9001 not in scope")
```

---

## Domain — Clause 4: Context of the Organization

### 4.1 / 4.2 — Context and Interested Parties

**Overall: PARAMETERIZED — Pattern 2**

```python
import pytest
from datetime import date

class TestClause4_Context:
    """Clauses 4.1–4.4 — Context, interested parties, QMS scope, and process approach."""

    @pytest.mark.assumption(
        id="ASSUME-ISO9001-4_1-001",
        description=(
            "External and internal issues relevant to the organization's purpose and strategic "
            "direction are identified and documented; list reviewed at least annually and at "
            "management review; format is org-defined (SWOT, PESTLE, or equivalent analysis "
            "document acceptable as evidence)"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_internal_external_issues_identified(self, controls_evidence: dict):
        context = controls_evidence.get("iso9001_context", {})
        assert context.get("internal_external_issues_documented", False), (
            "Internal and external issues relevant to the organization's purpose must be "
            "identified and documented (ISO 9001 §4.1)"
        )

    @pytest.mark.assumption(
        id="ASSUME-ISO9001-4_2-001",
        description=(
            "Interested parties and their relevant requirements are identified; at minimum: "
            "customers, regulatory authorities, suppliers, and employees; requirements reviewed "
            "for inclusion in QMS scope; list updated when business context changes"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_interested_parties_identified(self, controls_evidence: dict):
        context = controls_evidence.get("iso9001_context", {})
        assert context.get("interested_parties_documented", False), (
            "Interested parties and their relevant requirements must be determined "
            "(ISO 9001 §4.2)"
        )

    def test_qms_scope_documented(self, controls_evidence: dict):
        context = controls_evidence.get("iso9001_context", {})
        assert context.get("qms_scope_documented", False), (
            "QMS scope must be available as documented information; exclusions from "
            "Clause 8 must be justified (ISO 9001 §4.3)"
        )

    @pytest.mark.assumption(
        id="ASSUME-ISO9001-4_4-001",
        description=(
            "QMS processes identified with inputs, outputs, sequence, interaction, criteria, "
            "resources, responsibilities, risks/opportunities, and performance indicators; "
            "process map or process interaction diagram maintained; processes reviewed when "
            "scope changes"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_qms_processes_defined(self, controls_evidence: dict):
        context = controls_evidence.get("iso9001_context", {})
        assert context.get("qms_processes_documented", False), (
            "QMS processes must be determined and documented with process approach elements "
            "(ISO 9001 §4.4)"
        )
```

---

## Domain — Clause 5: Leadership

### 5.1 / 5.2 / 5.3 — Leadership, Quality Policy, Roles

**Overall: PARAMETERIZED — Pattern 2 (5.2 quality policy has DETERMINISTIC existence check)**

```python
class TestClause5_Leadership:
    """Clauses 5.1–5.3 — Leadership: commitment, quality policy, roles."""

    @pytest.mark.assumption(
        id="ASSUME-ISO9001-5_1-001",
        description=(
            "Top management demonstrates QMS commitment via: quality policy signed at executive "
            "level; management review participation; resource allocation decisions traceable to "
            "quality objectives; communication of quality importance to organization; integration "
            "of QMS requirements into business processes"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_management_commitment_evidenced(self, controls_evidence: dict):
        leadership = controls_evidence.get("iso9001_leadership", {})
        assert leadership.get("management_commitment_evidenced", False), (
            "Top management must demonstrate commitment to the QMS "
            "(ISO 9001 §5.1.1)"
        )

    def test_quality_policy_exists_and_signed(self, controls_evidence: dict):
        leadership = controls_evidence.get("iso9001_leadership", {})
        assert leadership.get("quality_policy_exists", False), (
            "Quality policy must be established as documented information and signed by "
            "top management (ISO 9001 §5.2)"
        )

    def test_quality_policy_communicated(self, controls_evidence: dict):
        leadership = controls_evidence.get("iso9001_leadership", {})
        assert leadership.get("quality_policy_communicated", False), (
            "Quality policy must be communicated within the organization and available "
            "to interested parties (ISO 9001 §5.2.2)"
        )

    def test_qms_roles_and_responsibilities_defined(self, controls_evidence: dict):
        leadership = controls_evidence.get("iso9001_leadership", {})
        assert leadership.get("qms_roles_defined", False), (
            "Roles, responsibilities, and authorities relevant to QMS must be assigned "
            "and communicated (ISO 9001 §5.3)"
        )
```

---

## Domain — Clause 6.1: Risk and Opportunities

**Overall: CONTESTED — Pattern 3**

```python
class TestClause6_1_RiskOpportunities:
    """Clause 6.1 — Risk-based thinking: risks and opportunities identified and addressed."""

    @pytest.mark.assumption(
        id="ASSUME-ISO9001-6_1-001",
        description=(
            "Risks and opportunities related to QMS context and interested parties "
            "are identified; no prescribed methodology — any systematic approach (risk register, "
            "FMEA, SWOT risk section, process-level risk assessment) is acceptable; "
            "actions to address risks are integrated into QMS processes and their effectiveness "
            "is evaluated; risk register or equivalent document reviewed annually"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    @pytest.mark.human_review_required(
        reason=(
            "Risk identification adequacy and action proportionality cannot be automatically "
            "verified — whether identified risks are comprehensive and whether actions are "
            "proportionate to potential impact requires qualified quality management judgment"
        )
    )
    def test_risks_and_opportunities_identified(self, controls_evidence: dict):
        risk = controls_evidence.get("iso9001_risk_management", {})
        assert risk.get("risks_opportunities_documented", False), (
            "Risks and opportunities must be identified and actions planned "
            "(ISO 9001 §6.1)"
        )
```

---

## Domain — Clause 7: Support (non-record sub-clauses)

### 7.1 Resources, 7.3 Awareness, 7.4 Communication

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestClause7_Support:
    """Clause 7 — Support: resources, awareness, communication (excluding record sub-clauses)."""

    @pytest.mark.assumption(
        id="ASSUME-ISO9001-7_3-001",
        description=(
            "Personnel are aware of: quality policy, quality objectives relevant to their work, "
            "their contribution to QMS effectiveness, implications of not conforming to QMS "
            "requirements; awareness verified through orientation records, training completion, "
            "or periodic acknowledgment sign-off"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_personnel_awareness_of_qms(self, controls_evidence: dict):
        support = controls_evidence.get("iso9001_support", {})
        assert support.get("personnel_qms_awareness_evidenced", False), (
            "Personnel must be aware of quality policy, relevant objectives, and implications "
            "of nonconformity (ISO 9001 §7.3)"
        )

    @pytest.mark.assumption(
        id="ASSUME-ISO9001-7_4-001",
        description=(
            "Internal and external communication relevant to QMS is planned: what to "
            "communicate, when, with whom, how, and who communicates; at minimum covers "
            "customer communication (§8.2.1), supplier communication (§8.4.3), and employee "
            "communication on quality matters"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_communication_plan_exists(self, controls_evidence: dict):
        support = controls_evidence.get("iso9001_support", {})
        assert support.get("communication_plan_documented", False), (
            "Internal and external communication plan must exist for QMS-relevant topics "
            "(ISO 9001 §7.4)"
        )
```

---

## Domain — Clause 8: Operation (planning and provision)

### 8.1 Operational Planning, 8.2.1/8.2.2 Customer Requirements, 8.3 Design & Development

**Overall: PARAMETERIZED — Pattern 2 (design records are in records-and-operational-controls.md)**

```python
class TestClause8_Operation:
    """Clauses 8.1–8.5 — Operational controls (planning, customer focus, design, suppliers)."""

    @pytest.mark.assumption(
        id="ASSUME-ISO9001-8_1-001",
        description=(
            "Operational processes are planned and controlled: process criteria established, "
            "controls implemented consistent with criteria, documented information retained "
            "sufficient to demonstrate processes carried out as planned; production/service "
            "process documentation reviewed annually or when significant process changes occur"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_operational_processes_planned_and_controlled(self, controls_evidence: dict):
        ops = controls_evidence.get("iso9001_operations", {})
        assert ops.get("process_criteria_documented", False), (
            "Operational planning and control must include documented process criteria "
            "(ISO 9001 §8.1)"
        )

    @pytest.mark.assumption(
        id="ASSUME-ISO9001-8_4-001",
        description=(
            "Externally provided processes, products, and services are controlled; supplier "
            "evaluation criteria defined; approved supplier list maintained; evaluation results "
            "retained as records; re-evaluation frequency defined based on supplier risk "
            "classification; critical/sole-source suppliers reviewed at minimum annually"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_external_provider_controls_defined(self, controls_evidence: dict):
        suppliers = controls_evidence.get("iso9001_external_providers", {})
        assert suppliers.get("evaluation_criteria_defined", False), (
            "Type and extent of control for external providers must be determined based on "
            "requirements and risk (ISO 9001 §8.4.1)"
        )

    def test_approved_supplier_list_maintained(self, controls_evidence: dict):
        suppliers = controls_evidence.get("iso9001_external_providers", {})
        assert suppliers.get("approved_supplier_list_exists", False), (
            "Approved supplier list or equivalent must be maintained with evaluation status "
            "(ISO 9001 §8.4.1)"
        )
```

---

## Domain — Clause 9.1: Performance Monitoring and Customer Satisfaction

**Overall: PARAMETERIZED / CONTESTED — Pattern 2/3**

```python
class TestClause9_1_Monitoring:
    """Clause 9.1 — Performance evaluation: monitoring, customer satisfaction."""

    @pytest.mark.assumption(
        id="ASSUME-ISO9001-9_1-001",
        description=(
            "Methods for obtaining customer satisfaction data are defined and implemented; "
            "acceptable methods include: customer surveys, complaint rates, on-time delivery "
            "metrics, return/warranty rates, customer feedback forms, or customer scorecards; "
            "results analyzed and included in management review inputs; method reviewed "
            "annually for continued appropriateness"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    @pytest.mark.human_review_required(
        reason=(
            "Adequacy of customer satisfaction monitoring method cannot be automatically "
            "determined — whether the chosen method provides meaningful data on customer "
            "perception depends on the organization's customer relationship model"
        )
    )
    def test_customer_satisfaction_monitored(self, controls_evidence: dict):
        monitoring = controls_evidence.get("iso9001_performance_evaluation", {})
        assert monitoring.get("customer_satisfaction_method_defined", False), (
            "Method for monitoring customer satisfaction must be defined and implemented "
            "(ISO 9001 §9.1.2)"
        )

    @pytest.mark.assumption(
        id="ASSUME-ISO9001-9_1-002",
        description=(
            "Analysis and evaluation of QMS performance data covers: conformity of products "
            "and services, degree of customer satisfaction, QMS process performance, supplier "
            "performance, effectiveness of actions to address risks and opportunities, "
            "improvement opportunities; results feed management review inputs"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_qms_performance_data_analyzed(self, controls_evidence: dict):
        monitoring = controls_evidence.get("iso9001_performance_evaluation", {})
        assert monitoring.get("performance_analysis_conducted", False), (
            "Analysis and evaluation of QMS performance data must be conducted "
            "(ISO 9001 §9.1.3)"
        )
```

---

## Domain — Clause 10.3: Continual Improvement

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestClause10_3_ContinualImprovement:
    """Clause 10.3 — Continual improvement: QMS effectiveness improved over time."""

    @pytest.mark.assumption(
        id="ASSUME-ISO9001-10_3-001",
        description=(
            "Continual improvement activities are planned and tracked; improvement initiatives "
            "are derived from: analysis and evaluation results (§9.1.3), management review "
            "outputs (§9.3.3), corrective actions (§10.2), and any other relevant QMS data; "
            "improvement objectives documented and progress reviewed at management review"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_continual_improvement_activities_planned(self, controls_evidence: dict):
        improvement = controls_evidence.get("iso9001_continual_improvement", {})
        assert improvement.get("improvement_activities_documented", False), (
            "Continual improvement activities must be planned and implemented "
            "(ISO 9001 §10.3)"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-ISO9001-4_1-001 | Context | Internal/external issues documented; reviewed annually; format org-defined | 2027-05-21 |
| ASSUME-ISO9001-4_2-001 | Interested parties | Customers, regulators, suppliers, employees identified; requirements reviewed | 2027-05-21 |
| ASSUME-ISO9001-4_4-001 | QMS processes | Process map/interaction diagram maintained; reviewed on scope changes | 2027-05-21 |
| ASSUME-ISO9001-5_1-001 | Leadership | Top management commitment evidenced by policy, review participation, resource allocation | 2027-05-21 |
| ASSUME-ISO9001-6_1-001 | Risk (CONTESTED) | Risk/opportunity identification; any systematic methodology accepted; annual review | 2027-05-21 |
| ASSUME-ISO9001-7_3-001 | Awareness | Personnel aware of policy, objectives, contribution, NC implications | 2027-05-21 |
| ASSUME-ISO9001-7_4-001 | Communication | Communication plan covers customer, supplier, employee quality topics | 2027-05-21 |
| ASSUME-ISO9001-8_1-001 | Operational planning | Process criteria documented; documented information sufficient to demonstrate control | 2027-05-21 |
| ASSUME-ISO9001-8_4-001 | External providers | Approved supplier list; evaluation criteria defined; critical suppliers reviewed annually | 2027-05-21 |
| ASSUME-ISO9001-9_1-001 | Customer satisfaction (CONTESTED) | Method defined; any systematic approach accepted; results in management review | 2027-05-21 |
| ASSUME-ISO9001-9_1-002 | Performance analysis | Analysis covers conformity, satisfaction, process performance, supplier, risk actions | 2027-05-21 |
| ASSUME-ISO9001-10_3-001 | Continual improvement | Improvement activities derived from analysis + management review outputs | 2027-05-21 |
