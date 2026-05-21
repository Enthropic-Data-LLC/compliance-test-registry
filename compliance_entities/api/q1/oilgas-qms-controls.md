# API Q1 / Q2 — Oil and Gas QMS Controls

**Framework:** API Q1 9th Edition + API Q2 1st Edition
**Clauses:** Q1 §5.3 (contingency planning), §6.2 (risk assessment), §7.3 (design records), §7.4 (supplier controls), §8 (production/service delivery); Q2 §5 (service agreements), §6 (critical service tools), §8 (wellsite execution)
**Parent:** ISO 9001:2015 (fully incorporated — all ISO 9001 requirements apply simultaneously)
**Confidence:** DETERMINISTIC-dominant (design record completeness, CST calibration, contingency plan, API Monogram marking, service agreement review before execution)
**Last parsed:** 2026-05-21
**Applies to:** Manufacturers of oil and gas equipment and service companies seeking the API Monogram license or Q1 certification; suppliers to oil and gas operators requiring API Q1 as a supply chain qualification
**Trigger:** API Monogram license requirement — organizations must hold Q1 certification to use the API Monogram on qualifying products; customer contract requirement from oil and gas operators; required for API-licensed products (wellheads, valves, drilling equipment, etc.)
**Jurisdiction:** Global — API (American Petroleum Institute) standard; internationally recognized in oil and gas industry globally
**Not applicable to:** Upstream oil and gas operators (they impose the requirement on suppliers but do not self-certify); non-oil-and-gas manufacturers; service companies not supplying equipment or processes to the oil and gas sector

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def api_q1_scope(entity_profile: dict):
    if not entity_profile.get("api_q1_in_scope", False) and not entity_profile.get("api_q2_in_scope", False):
        pytest.skip("API Q1/Q2 not in scope")
```

---

## Constants

```python
# API Q1 — design record required types (§7.3)
API_Q1_DESIGN_RECORD_TYPES = frozenset({
    "design_and_development_plan",
    "design_input_record",
    "design_output_record",
    "design_review_record",
    "design_verification_record",
    "design_validation_record",
    "design_change_record",
})
# design_transfer is PARAMETERIZED — adequacy determination required

# API Monogram — product marking required fields
API_MONOGRAM_MARKING_REQUIRED = frozenset({
    "api_monogram_symbol",
    "specification_number",       # e.g., 6A, 5CT, 11E
    "manufacturer_license_number",
    "date_of_manufacture",
})

# API Q2 — Critical Service Tool (CST) pre-deployment checks
API_Q2_CST_PREDEPLOY_CHECKS = frozenset({
    "inspection_completed",
    "calibration_current",
    "certification_current",
    "pressure_test_current",
})
```

---

## API Q1 — Design Records (§7.3)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestAPIQ1DesignRecords:
    """API Q1 §7.3 — Each design record type must exist as a separate, distinct document."""

    def test_all_required_design_record_types_exist(
        self, controls_evidence: dict
    ):
        products = controls_evidence.get("api_q1_products", [])
        for product in products:
            if not product.get("design_controls_applicable", True):
                continue
            present = set(product.get("design_records_present", []))
            missing = API_Q1_DESIGN_RECORD_TYPES - present
            assert not missing, (
                f"API Q1 requires each design record type to be separately documented "
                f"for product '{product['product_id']}'. Missing: {missing} "
                f"(API Q1 9th Edition §7.3)"
            )

    def test_design_change_records_exist_for_all_changes(
        self, controls_evidence: dict
    ):
        design_changes = controls_evidence.get("api_q1_design_changes", [])
        no_record = [
            c for c in design_changes
            if not c.get("design_change_record_exists", False)
        ]
        assert not no_record, (
            f"Design Change Records must document all changes including review, "
            f"approval, and re-validation status (API Q1 9th Edition §7.3). "
            f"Missing: {[c['change_id'] for c in no_record]}"
        )

    def test_design_validation_performed_under_intended_use_conditions(
        self, controls_evidence: dict
    ):
        products = controls_evidence.get("api_q1_products", [])
        no_validation = [
            p for p in products
            if p.get("design_controls_applicable", True)
            and not p.get("design_validation_under_intended_conditions", False)
        ]
        assert not no_validation, (
            f"Design validation must be performed under simulated or actual intended "
            f"use conditions (API Q1 9th Edition §7.3.5). "
            f"Missing: {[p['product_id'] for p in no_validation]}"
        )
```

---

## API Q1 — Contingency Planning (§5.3)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestAPIQ1ContingencyPlanning:
    """API Q1 §5.3 — Written contingency plan for critical processes; equipment, personnel, supply disruptions."""

    def test_contingency_plan_exists_for_critical_processes(
        self, controls_evidence: dict
    ):
        qms = controls_evidence.get("api_q1_qms", {})
        assert qms.get("contingency_plan_documented", False), (
            "Written contingency plan must exist addressing responses to equipment failure, "
            "key personnel loss, and supply disruptions for critical processes "
            "(API Q1 9th Edition §5.3)"
        )

    def test_critical_processes_identified_in_contingency_plan(
        self, controls_evidence: dict
    ):
        qms = controls_evidence.get("api_q1_qms", {})
        assert qms.get("critical_processes_identified_in_plan", False), (
            "Contingency plan must explicitly identify which processes are considered "
            "critical and the responses for each disruption type "
            "(API Q1 9th Edition §5.3)"
        )
```

---

## API Q1 — Risk Assessment (§6.2)

**Overall: DETERMINISTIC (record exists) + PARAMETERIZED (adequacy)**

```python
class TestAPIQ1RiskAssessment:
    """API Q1 §6.2 — Formal risk assessment documented before product realization."""

    def test_risk_assessment_performed_before_product_realization(
        self, controls_evidence: dict
    ):
        products = controls_evidence.get("api_q1_products", [])
        no_risk_assessment = [
            p for p in products
            if not p.get("risk_assessment_performed", False)
        ]
        assert not no_risk_assessment, (
            f"Formal risk assessment must be performed and documented for each product "
            f"realization process before production (API Q1 9th Edition §6.2). "
            f"Missing: {[p['product_id'] for p in no_risk_assessment]}"
        )

    @pytest.mark.assumption(
        id="ASSUME-APIQ1-RISK-001",
        description=(
            "Risk assessment methodology: organization-defined; must identify hazards, "
            "assess likelihood and consequence for the oil and gas operating environment "
            "(high-pressure, high-temperature, H2S exposure, wellbore integrity); "
            "risk mitigation measures documented; adequacy of methodology is PARAMETERIZED — "
            "existence of the risk assessment record is DETERMINISTIC"
        ),
        approved_by="engineering_manager",
        review_date="2027-05-21",
    )
    def test_risk_mitigation_measures_documented(self, controls_evidence: dict):
        products = controls_evidence.get("api_q1_products", [])
        no_mitigations = [
            p for p in products
            if p.get("risk_assessment_performed", False)
            and not p.get("risk_mitigation_measures_documented", False)
        ]
        assert not no_mitigations, (
            f"Risk assessment must include documented risk mitigation measures "
            f"(API Q1 9th Edition §6.2). Missing: {[p['product_id'] for p in no_mitigations]}"
        )
```

---

## API Q1 — Supplier Controls (§7.4)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestAPIQ1SupplierControls:
    """API Q1 §7.4 — Written supplier selection criteria; evaluation records for all approved suppliers."""

    def test_supplier_selection_criteria_documented(self, controls_evidence: dict):
        qms = controls_evidence.get("api_q1_qms", {})
        assert qms.get("supplier_selection_criteria_documented", False), (
            "Written criteria for supplier selection and evaluation must be documented "
            "(API Q1 9th Edition §7.4.1)"
        )

    def test_approved_suppliers_have_evaluation_records(
        self, controls_evidence: dict
    ):
        suppliers = controls_evidence.get("api_q1_suppliers", [])
        no_eval = [s for s in suppliers if not s.get("evaluation_record_exists", False)]
        assert not no_eval, (
            f"Evaluation records must exist for all approved suppliers "
            f"(API Q1 9th Edition §7.4.1). Missing: {[s['supplier_id'] for s in no_eval]}"
        )
```

---

## API Monogram — Product Marking and License

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestAPIMonogram:
    """API Monogram — product marked per spec; license current; Q1 QMS certification prerequisite."""

    @pytest.fixture(autouse=True)
    def monogram_scope(self, entity_profile: dict):
        if not entity_profile.get("api_monogram_licensee", False):
            pytest.skip("API Monogram not applicable")

    def test_api_monogram_license_current(
        self, controls_evidence: dict, reference_date: date
    ):
        monogram = controls_evidence.get("api_monogram", {})
        license_expiry = monogram.get("license_expiry_date")
        assert license_expiry is not None and license_expiry >= reference_date, (
            f"API Monogram license must be current. "
            f"Expiry: {license_expiry} (API Monogram Program)"
        )

    def test_monogram_marked_products_contain_required_fields(
        self, controls_evidence: dict
    ):
        products = controls_evidence.get("api_q1_products", [])
        monogram_products = [p for p in products if p.get("api_monogram_marked", False)]
        for product in monogram_products:
            present = set(product.get("marking_fields_present", []))
            missing = API_MONOGRAM_MARKING_REQUIRED - present
            assert not missing, (
                f"API Monogram product '{product['product_id']}' is missing required "
                f"marking fields: {missing} (API Monogram Program / API Spec marking requirements)"
            )

    def test_products_comply_with_applicable_api_specification(
        self, controls_evidence: dict
    ):
        products = controls_evidence.get("api_q1_products", [])
        monogram_products = [p for p in products if p.get("api_monogram_marked", False)]
        not_compliant = [
            p for p in monogram_products
            if not p.get("api_spec_compliance_verified", False)
        ]
        assert not not_compliant, (
            f"Monogram-marked products must comply with the applicable API product "
            f"specification (5CT, 6A, 11E, etc.) (API Monogram Program). "
            f"Non-compliant: {[p['product_id'] for p in not_compliant]}"
        )
```

---

## API Q2 — Critical Service Tools (CSTs)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestAPIQ2CriticalServiceTools:
    """API Q2 §6 — CSTs identified; pre-deployment inspection + calibration current; post-use records."""

    @pytest.fixture(autouse=True)
    def q2_scope(self, entity_profile: dict):
        if not entity_profile.get("api_q2_in_scope", False):
            pytest.skip("API Q2 not in scope")

    def test_critical_service_tools_identified(self, controls_evidence: dict):
        q2 = controls_evidence.get("api_q2_operations", {})
        assert q2.get("critical_service_tools_identified", False), (
            "Critical Service Tools (CSTs) must be identified and documented "
            "(API Q2 1st Edition §6)"
        )

    def test_cst_predeploy_checks_completed_before_wellsite(
        self, controls_evidence: dict
    ):
        csts = controls_evidence.get("api_q2_critical_service_tools", [])
        for cst in csts:
            checks_done = set(cst.get("predeploy_checks_completed", []))
            missing = API_Q2_CST_PREDEPLOY_CHECKS - checks_done
            assert not missing, (
                f"CST '{cst['cst_id']}' missing required pre-deployment checks: "
                f"{missing} (API Q2 §6)"
            )

    def test_cst_traceability_maintained(self, controls_evidence: dict):
        csts = controls_evidence.get("api_q2_critical_service_tools", [])
        no_traceability = [
            c for c in csts
            if not c.get("traceability_to_job_maintained", False)
        ]
        assert not no_traceability, (
            f"CST traceability must be maintained from inventory through each wellsite job "
            f"(API Q2 §6). Missing: {[c['cst_id'] for c in no_traceability]}"
        )
```

---

## API Q2 — Service Agreements and Wellsite Execution (§5 / §8)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestAPIQ2ServiceExecution:
    """API Q2 §5/§8 — Service agreement reviewed before execution; wellsite records complete; NCRs reported."""

    @pytest.fixture(autouse=True)
    def q2_scope(self, entity_profile: dict):
        if not entity_profile.get("api_q2_in_scope", False):
            pytest.skip("API Q2 not in scope")

    def test_service_agreement_reviewed_before_execution(
        self, controls_evidence: dict
    ):
        jobs = controls_evidence.get("api_q2_jobs", [])
        no_review = [
            j for j in jobs
            if not j.get("service_agreement_reviewed_before_start", False)
        ]
        assert not no_review, (
            f"Service agreements must be reviewed and accepted before wellsite execution "
            f"begins (API Q2 §5). Missing review: {[j['job_id'] for j in no_review]}"
        )

    def test_service_agreement_documents_scope_and_requirements(
        self, controls_evidence: dict
    ):
        jobs = controls_evidence.get("api_q2_jobs", [])
        missing_scope = [
            j for j in jobs
            if not j.get("service_agreement_documents_scope_requirements", False)
        ]
        assert not missing_scope, (
            f"Service agreement must document scope, technical requirements, and any "
            f"approved deviations (API Q2 §5). Missing: {[j['job_id'] for j in missing_scope]}"
        )

    def test_wellsite_job_records_complete(self, controls_evidence: dict):
        jobs = controls_evidence.get("api_q2_jobs", [])
        incomplete_records = [
            j for j in jobs
            if not j.get("job_record_complete", False)
        ]
        assert not incomplete_records, (
            f"Wellsite job records must be complete including: date, location, services "
            f"performed, personnel, CSTs used, deviations, safety incidents "
            f"(API Q2 §8). Incomplete: {[j['job_id'] for j in incomplete_records]}"
        )

    def test_wellsite_nonconformities_immediately_notified(
        self, controls_evidence: dict
    ):
        wellsite_ncrs = controls_evidence.get("api_q2_wellsite_nonconformities", [])
        not_notified = [
            ncr for ncr in wellsite_ncrs
            if not ncr.get("customer_notified", False)
        ]
        assert not not_notified, (
            f"Nonconformities occurring at the wellsite must result in immediate customer "
            f"notification (API Q2 §8). Not notified: "
            f"{[ncr['ncr_id'] for ncr in not_notified]}"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-APIQ1-RISK-001 | Q1 §6.2 | Risk assessment methodology: PARAMETERIZED (adequacy); existence of risk assessment record: DETERMINISTIC | 2027-05-21 |
