# IATF 16949:2016 — Supplier Management and Problem Solving

**Framework:** IATF 16949:2016
**Clauses:** 4.3.2 (CSRs), 6.1.2.3 (contingency plans), 7.2.3–7.2.4 (auditor competence), 8.4 (supplier management), 10.2.3 (8D), 10.2.5 (warranty), 10.2.6 (field failures), 9.1.2.1, 9.2.2.1, 9.3.2.1
**Parent:** ISO 9001:2015 (all ISO 9001 requirements apply simultaneously)
**Confidence:** DETERMINISTIC-dominant (supplier qualification, 8D, warranty analysis, customer performance, audit program)
**Last parsed:** 2026-05-21
**Applies to:** Automotive parts manufacturers and their direct and sub-tier suppliers providing production parts, accessories, or service parts to automotive original equipment manufacturers (OEMs)
**Trigger:** Customer requirement from automotive OEMs (Ford, GM, Stellantis, BMW, VW Group, Toyota, Honda, etc.) mandating IATF 16949 certification for supply chain qualification; required for PPAP (Production Part Approval Process) submission to most OEMs
**Jurisdiction:** Global — IATF (International Automotive Task Force) standard; recognized by all major automotive OEMs worldwide through their customer-specific requirements (CSRs)
**Not applicable to:** Non-automotive manufacturing; automotive distributors or dealers without manufacturing; service-only companies; aftermarket software and electronics not in direct OEM supply chain; companies supplying raw materials only (e.g., steel mills) rather than processed parts

---

## Scope pre-condition

```python
@pytest.fixture(autouse=True)
def iatf16949_scope(entity_profile: dict):
    if not entity_profile.get("iatf16949_in_scope", False):
        pytest.skip("IATF 16949 not in scope")
```

---

## Constants

```python
# 8D problem solving — §10.2.3
IATF_8D_REQUIRED_DISCIPLINES = frozenset({
    "D0_emergency_response_actions",
    "D1_team_formation",
    "D2_problem_description",
    "D3_interim_containment_actions",
    "D4_root_cause_analysis",
    "D5_permanent_corrective_actions",
    "D6_implementation_and_validation",
    "D7_prevent_recurrence",
    "D8_team_recognition",
})

# Supplier monitoring — §8.4.2.4
IATF_SUPPLIER_MONITORING_REQUIRED_METRICS = frozenset({
    "quality_ppm",
    "delivery_performance",
    "iatf16949_certification_status",
})

# Customer satisfaction monitoring — §9.1.2.1
IATF_CUSTOMER_METRICS_REQUIRED = frozenset({
    "quality_ppm_to_customer",
    "warranty_returns",
    "customer_scorecard_performance",
})

# Internal audit program — §9.2.2.1 (annual; all processes, all shifts)
IATF_AUDIT_TYPES_REQUIRED = frozenset({
    "qms_audit",
    "manufacturing_process_audit",
    "product_audit",
})
```

---

## Clause 4.3.2 — Customer-Specific Requirements (CSRs)

**Overall: DETERMINISTIC — Pattern 1**

```python
import pytest
from datetime import date

class TestCSRs:
    """§4.3.2 — Customer-specific requirements identified and included in QMS."""

    def test_customer_specific_requirements_identified(self, controls_evidence: dict):
        qms = controls_evidence.get("iatf16949_qms", {})
        assert qms.get("customer_specific_requirements_identified", False), (
            "Customer-specific requirements (CSRs) from each OEM customer must be identified "
            "and incorporated into the QMS (IATF 16949 §4.3.2)"
        )

    def test_csr_register_maintained(self, controls_evidence: dict):
        qms = controls_evidence.get("iatf16949_qms", {})
        assert qms.get("csr_register_exists", False), (
            "Register of customer-specific requirements must be maintained and reviewed "
            "when CSRs are updated (IATF 16949 §4.3.2)"
        )
```

---

## Clause 6.1.2.3 — Contingency Plans

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestContingencyPlans:
    """§6.1.2.3 — Written contingency plans for supply disruption."""

    def test_contingency_plans_exist(self, controls_evidence: dict):
        contingency = controls_evidence.get("iatf16949_contingency", {})
        assert contingency.get("contingency_plans_documented", False), (
            "Written contingency plans must exist for production disruption scenarios: "
            "supply disruption, key processes, utility outages, natural disasters "
            "(IATF 16949 §6.1.2.3)"
        )

    def test_contingency_plans_tested(self, controls_evidence: dict):
        contingency = controls_evidence.get("iatf16949_contingency", {})
        assert contingency.get("contingency_plans_tested", False), (
            "Contingency plans must be tested/exercised to verify effectiveness "
            "(IATF 16949 §6.1.2.3)"
        )
```

---

## Clause 7.2.3–7.2.4 — Auditor Competency

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestAuditorCompetency:
    """§7.2.3/7.2.4 — Internal and second-party auditors must meet competency requirements."""

    def test_internal_auditors_qualified(self, controls_evidence: dict):
        auditors = controls_evidence.get("iatf16949_internal_auditors", [])
        unqualified = [a for a in auditors if not a.get("qualified", False)]
        assert not unqualified, (
            f"Internal auditors must be qualified including product/process audit training "
            f"(IATF 16949 §7.2.3). Unqualified: {[a['auditor_id'] for a in unqualified]}"
        )

    def test_supplier_auditors_meet_competency_criteria(self, controls_evidence: dict):
        auditors = controls_evidence.get("iatf16949_supplier_auditors", [])
        unqualified = [a for a in auditors if not a.get("meets_competency_criteria", False)]
        assert not unqualified, (
            f"Second-party (supplier) auditors must meet defined competency criteria "
            f"(IATF 16949 §7.2.4). Unqualified: {[a['auditor_id'] for a in unqualified]}"
        )
```

---

## Clause 8.4 — Supplier Management

**Overall: DETERMINISTIC-dominant — Pattern 1/2**

```python
class TestSupplierManagement:
    """§8.4 — Supplier qualification, monitoring, development, second-party audits."""

    def test_approved_supplier_list_maintained(self, controls_evidence: dict):
        suppliers = controls_evidence.get("iatf16949_supplier_management", {})
        assert suppliers.get("approved_supplier_list_exists", False), (
            "Approved supplier list must be maintained with qualification status "
            "(IATF 16949 §8.4.1)"
        )

    def test_suppliers_monitored_on_required_metrics(self, controls_evidence: dict):
        suppliers_data = controls_evidence.get("iatf16949_suppliers", [])
        for supplier in suppliers_data:
            monitored_metrics = set(supplier.get("monitored_metrics", []))
            missing_metrics = IATF_SUPPLIER_MONITORING_REQUIRED_METRICS - monitored_metrics
            assert not missing_metrics, (
                f"Supplier '{supplier['supplier_id']}' missing required monitoring metrics: "
                f"{missing_metrics} (IATF 16949 §8.4.2.4)"
            )

    def test_non_iatf_certified_suppliers_have_second_party_audit(
        self, controls_evidence: dict
    ):
        suppliers_data = controls_evidence.get("iatf16949_suppliers", [])
        non_certified_tier2 = [
            s for s in suppliers_data
            if not s.get("iatf_certified", False)
            and s.get("receives_production_product_info", True)
        ]
        no_second_party = [
            s for s in non_certified_tier2
            if not s.get("second_party_audit_performed", False)
        ]
        assert not no_second_party, (
            f"Tier 2 suppliers not IATF 16949 certified must have second-party audit "
            f"(IATF 16949 §8.4.2.3). Missing: {[s['supplier_id'] for s in no_second_party]}"
        )

    @pytest.mark.assumption(
        id="ASSUME-IATF-SUPP-001",
        description=(
            "Supplier development plan targets: (1) suppliers below quality/delivery "
            "performance thresholds receive active development; (2) improvement targets "
            "defined with timeline; (3) second-party audits used as development mechanism "
            "for non-certified or poor-performing suppliers; (4) at-risk suppliers escalated "
            "to controlled shipping or provisional status per OEM CSR requirements; "
            "performance thresholds defined in supplier quality manual"
        ),
        approved_by="supplier_quality_manager",
        review_date="2027-05-21",
    )
    def test_supplier_development_process_exists(self, controls_evidence: dict):
        suppliers = controls_evidence.get("iatf16949_supplier_management", {})
        assert suppliers.get("supplier_development_process_exists", False), (
            "Supplier development process must exist for improving poor-performing "
            "suppliers (IATF 16949 §8.4.2.5)"
        )
```

---

## Clause 10.2.3 — 8D Problem Solving

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestProblemSolving8D:
    """§10.2.3 — Structured problem solving (8D) required; all disciplines documented."""

    def test_8d_used_for_structured_problem_solving(self, controls_evidence: dict):
        ps = controls_evidence.get("iatf16949_problem_solving", {})
        assert ps.get("structured_problem_solving_methodology_defined", False), (
            "Structured problem solving methodology (8D or equivalent) must be defined "
            "(IATF 16949 §10.2.3)"
        )

    def test_8d_reports_contain_required_disciplines(self, controls_evidence: dict):
        problem_reports = controls_evidence.get("iatf16949_8d_reports", [])
        for report in problem_reports:
            disciplines_present = set(report.get("disciplines_documented", []))
            missing = IATF_8D_REQUIRED_DISCIPLINES - disciplines_present
            assert not missing, (
                f"8D report '{report['report_id']}' missing required disciplines: "
                f"{missing} (IATF 16949 §10.2.3)"
            )

    def test_interim_containment_documented_in_8d(self, controls_evidence: dict):
        problem_reports = controls_evidence.get("iatf16949_8d_reports", [])
        no_d3 = [
            r for r in problem_reports
            if "D3_interim_containment_actions" not in set(r.get("disciplines_documented", []))
        ]
        assert not no_d3, (
            f"D3 interim containment actions must be documented in 8D reports "
            f"(IATF 16949 §10.2.3). Missing D3: {[r['report_id'] for r in no_d3]}"
        )
```

---

## Clause 10.2.5 — Warranty Management

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestWarrantyManagement:
    """§10.2.5 — Warranty analysis process; NTF analysis performed."""

    def test_warranty_analysis_process_exists(self, controls_evidence: dict):
        warranty = controls_evidence.get("iatf16949_warranty", {})
        assert warranty.get("warranty_analysis_process_documented", False), (
            "Warranty analysis process must exist to analyze returned parts and identify "
            "quality issues (IATF 16949 §10.2.5)"
        )

    def test_ntf_analysis_performed(self, controls_evidence: dict):
        warranty = controls_evidence.get("iatf16949_warranty", {})
        assert warranty.get("ntf_analysis_process_exists", False), (
            "No Trouble Found (NTF) analysis process must exist for warranty returns "
            "where no defect is found (IATF 16949 §10.2.5)"
        )
```

---

## Clause 9.1.2.1 — Customer Satisfaction Monitoring

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestCustomerSatisfaction:
    """§9.1.2.1 — Customer performance metrics (PPM, warranty, scorecard) monitored."""

    def test_required_customer_metrics_monitored(self, controls_evidence: dict):
        cs = controls_evidence.get("iatf16949_customer_satisfaction", {})
        monitored_metrics = set(cs.get("monitored_metrics", []))
        missing = IATF_CUSTOMER_METRICS_REQUIRED - monitored_metrics
        assert not missing, (
            f"Required customer satisfaction metrics must be monitored: {missing} "
            f"(IATF 16949 §9.1.2.1)"
        )

    def test_customer_portal_data_monitored(self, controls_evidence: dict):
        cs = controls_evidence.get("iatf16949_customer_satisfaction", {})
        assert cs.get("customer_portal_data_monitored", False), (
            "Customer portal data (customer scorecards, delivery performance ratings) "
            "must be monitored (IATF 16949 §9.1.2.1)"
        )
```

---

## Clause 9.2.2.1 — Internal Audit Program

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestInternalAuditProgram:
    """§9.2.2.1 — Annual audit program: QMS, process, and product audits; all shifts."""

    def test_annual_audit_program_includes_all_required_audit_types(
        self, controls_evidence: dict
    ):
        audit = controls_evidence.get("iatf16949_internal_audit", {})
        audit_types_in_program = set(audit.get("audit_types_planned", []))
        missing_types = IATF_AUDIT_TYPES_REQUIRED - audit_types_in_program
        assert not missing_types, (
            f"Annual internal audit program must include all audit types: "
            f"{missing_types} (IATF 16949 §9.2.2.1)"
        )

    def test_audit_coverage_includes_all_shifts(self, controls_evidence: dict):
        audit = controls_evidence.get("iatf16949_internal_audit", {})
        assert audit.get("all_shifts_covered", False), (
            "Internal audit program must cover all production shifts "
            "(IATF 16949 §9.2.2.1)"
        )

    def test_manufacturing_process_audit_performed(self, controls_evidence: dict):
        audit = controls_evidence.get("iatf16949_internal_audit", {})
        assert audit.get("manufacturing_process_audit_performed", False), (
            "Manufacturing process audit (process-level audit — not just QMS) must be "
            "performed annually (IATF 16949 §9.2.2.1)"
        )
```

---

## Clause 9.3.2.1 — Management Review — Additional Inputs

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestManagementReviewInputs:
    """§9.3.2.1 — Management review must include automotive-specific inputs."""

    @pytest.mark.assumption(
        id="ASSUME-IATF-MGMT-001",
        description=(
            "Management review inputs include all ISO 9001 §9.3.2 inputs PLUS: "
            "customer portal data, warranty performance, field returns, lessons learned "
            "from new program launches, customer PPM, delivery performance, CSR review; "
            "management review occurs at least annually; records include attendance, "
            "inputs reviewed, decisions, action items with owners and due dates"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_management_review_includes_required_iatf_inputs(
        self, controls_evidence: dict
    ):
        mgmt_review = controls_evidence.get("iatf16949_management_review", {})
        assert mgmt_review.get("automotive_specific_inputs_included", False), (
            "Management review must include IATF-required inputs: customer portal data, "
            "warranty, field returns, lessons learned from new programs "
            "(IATF 16949 §9.3.2.1)"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-IATF-SUPP-001 | 8.4.2.5 | Supplier development: targets defined; at-risk suppliers escalated; thresholds in SQM | 2027-05-21 |
| ASSUME-IATF-MGMT-001 | 9.3.2.1 | Management review: all IATF inputs incl. customer portal, warranty, field returns, NPI lessons | 2027-05-21 |
