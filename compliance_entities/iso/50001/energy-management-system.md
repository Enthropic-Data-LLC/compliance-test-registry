# ISO 50001:2018 — Energy Management System

**Framework:** ISO 50001:2018 (second edition; Annex SL — harmonized with ISO 9001, ISO 14001, ISO 45001)
**Clauses:** §5.2 (energy policy), §5.3 (EnMR designation), §6.2 (energy review — 6 required outputs), §6.3 (energy baseline), §6.4 (EnPIs), §6.5 (energy objectives and targets), §6.6 (action plans), §9.1.2 (compliance evaluation), §9.2 (internal audit), §9.3 (management review), §10.1 (CAPA)
**Confidence:** DETERMINISTIC-dominant (policy, EnMR, all §6 planning artifacts, audit program, management review, CAPA); PARAMETERIZED (SEU criteria, EnPI selection adequacy)
**Last parsed:** 2026-05-21
**Applies to:** Any organization seeking to implement an Energy Management System (EnMS); large enterprises in the EU that may use ISO 50001 certification as an alternative to mandatory energy audits under the EU Energy Efficiency Directive (EED)
**Trigger:** Voluntary certification; EU Energy Efficiency Directive Article 8 — large enterprises (> 250 employees or > €50M turnover and > €43M balance sheet) can use ISO 50001 certified EnMS in lieu of mandatory quadrennial energy audit; customer/government procurement requirement in some jurisdictions
**Jurisdiction:** Global — ISO international standard; particularly relevant in EU where EED creates regulatory driver
**Not applicable to:** Small and medium enterprises below EU EED large-enterprise thresholds (SMEs are not subject to mandatory energy audit obligations, so ISO 50001 has no regulatory driver for them unless voluntarily adopted); organizations where energy costs are immaterial to operations

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def iso_50001_scope(entity_profile: dict):
    if not entity_profile.get("iso_50001_in_scope", False):
        pytest.skip("ISO 50001 not in scope")
```

---

## Constants

```python
from datetime import date

# Required energy review outputs (§6.2) — all 6 must be documented
ISO_50001_ENERGY_REVIEW_REQUIRED_OUTPUTS = frozenset({
    "energy_use_and_consumption_analysis_by_type",
    "significant_energy_uses_identified",
    "variables_affecting_seu_consumption_identified",
    "current_energy_performance_of_seus",
    "future_energy_use_and_consumption_estimated",
    "energy_improvement_opportunities_identified",
})

# Required energy policy commitments (§5.2)
ISO_50001_ENERGY_POLICY_REQUIRED_COMMITMENTS = frozenset({
    "improve_energy_performance",
    "fulfil_applicable_legal_and_other_requirements",
    "support_purchase_of_energy_efficient_products",
    "provide_information_and_resources",
})

# Required elements in action plans (§6.6)
ISO_50001_ACTION_PLAN_REQUIRED_ELEMENTS = frozenset({
    "activities_to_achieve_objective",
    "resources_required",
    "responsible_party",
    "timeframe",
    "method_to_verify_improvement_in_energy_performance",
})

# Required inputs to management review (§9.3.3)
ISO_50001_MANAGEMENT_REVIEW_REQUIRED_INPUTS = frozenset({
    "status_of_previous_review_actions",
    "review_of_energy_policy",
    "energy_performance_including_enpi_results",
    "compliance_obligations_fulfilment",
    "extent_of_energy_objectives_and_targets_achieved",
    "results_of_audits",
    "nonconformities_and_corrective_actions",
    "adequacy_of_resources",
    "opportunities_for_improvement",
})
```

---

## Energy Policy (§5.2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestEnergyPolicy:
    """ISO 50001 §5.2 — Written energy policy with required commitments; communicated throughout organization."""

    def test_energy_policy_exists_and_is_documented(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("energy_policy_documented", False), (
            "A documented energy policy must exist and be maintained "
            "(ISO 50001:2018 §5.2)"
        )

    def test_energy_policy_contains_required_commitments(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        present = set(ems.get("energy_policy_commitments_present", []))
        missing = ISO_50001_ENERGY_POLICY_REQUIRED_COMMITMENTS - present
        assert not missing, (
            f"Energy policy must include all required commitments. Missing: {missing} "
            f"(ISO 50001:2018 §5.2(a)–(d))"
        )

    def test_energy_policy_communicated_throughout_organization(
        self, controls_evidence: dict
    ):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("energy_policy_communicated", False), (
            "Energy policy must be communicated throughout the organization "
            "(ISO 50001:2018 §5.2)"
        )
```

---

## Energy Management Representative (§5.3)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestEnergyManagementRepresentative:
    """ISO 50001 §5.3 — Management representative (EnMR) formally designated; accountable for EnMS."""

    def test_energy_management_representative_designated(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("energy_management_representative_designated", False), (
            "Top management must designate an Energy Management Representative (EnMR) "
            "responsible for the EnMS (ISO 50001:2018 §5.3)"
        )

    def test_energy_management_representative_has_defined_authority(
        self, controls_evidence: dict
    ):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("enm_representative_authority_documented", False), (
            "The EnMR's responsibilities and authority for reporting energy performance "
            "to top management must be documented (ISO 50001:2018 §5.3)"
        )
```

---

## Energy Review (§6.2)

**Overall: DETERMINISTIC — Pattern 1 (all 6 required outputs must be present)**

```python
class TestEnergyReview:
    """ISO 50001 §6.2 — Energy review conducted and documented; all 6 required outputs present."""

    def test_energy_review_conducted_and_documented(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("energy_review_documented", False), (
            "An energy review must be conducted and documented "
            "(ISO 50001:2018 §6.2)"
        )

    def test_energy_review_contains_all_required_outputs(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        present = set(ems.get("energy_review_outputs_present", []))
        missing = ISO_50001_ENERGY_REVIEW_REQUIRED_OUTPUTS - present
        assert not missing, (
            f"Energy review must document all required outputs. Missing: {missing} "
            f"(ISO 50001:2018 §6.2)"
        )

    def test_energy_review_updated_at_defined_intervals(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("energy_review_update_interval_defined", False), (
            "The energy review must be updated at defined intervals and when major "
            "changes in facilities, equipment, or systems occur "
            "(ISO 50001:2018 §6.2)"
        )
```

---

## Energy Baseline (§6.3)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestEnergyBaseline:
    """ISO 50001 §6.3 — Energy baseline established and documented; normalization factors applied; updated when SEUs change."""

    def test_energy_baseline_established_and_documented(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("energy_baseline_established", False), (
            "An energy baseline (EnB) must be established and documented for each "
            "relevant energy type or SEU (ISO 50001:2018 §6.3)"
        )

    def test_energy_baseline_uses_relevant_time_period(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("energy_baseline_time_period_documented", False), (
            "The time period used for the energy baseline must be documented and "
            "appropriate for the energy use being tracked (ISO 50001:2018 §6.3)"
        )

    def test_normalization_factors_applied_where_applicable(
        self, controls_evidence: dict
    ):
        ems = controls_evidence.get("iso_50001", {})
        if ems.get("normalization_factors_applicable", False):
            assert ems.get("normalization_factors_documented", False), (
                "Where variables significantly affect energy performance, normalization "
                "factors must be documented and applied to the energy baseline "
                "(ISO 50001:2018 §6.3)"
            )
```

---

## Energy Performance Indicators (§6.4)

**Overall: DETERMINISTIC (existence and monitoring); PARAMETERIZED (selection adequacy)**

```python
class TestEnergyPerformanceIndicators:
    """ISO 50001 §6.4 — EnPIs selected, documented, and monitored; reviewed for continued appropriateness."""

    @pytest.mark.assumption(
        id="ASSUME-50001-ENPI-001",
        description=(
            "EnPI selection methodology is organization-defined: indicators may be "
            "simple ratios (kWh/unit), regression models, or composite indices; "
            "adequacy of EnPI selection for representing energy performance is "
            "PARAMETERIZED — documented EnPIs and monitoring records is DETERMINISTIC"
        ),
        approved_by="energy_manager",
        review_date="2027-05-21",
    )
    def test_energy_performance_indicators_documented(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("enpi_documented", False), (
            "Energy Performance Indicators (EnPIs) must be documented "
            "(ISO 50001:2018 §6.4)"
        )

    def test_energy_performance_indicators_monitored(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("enpi_monitored_with_records", False), (
            "EnPI values must be monitored and recorded at defined intervals "
            "(ISO 50001:2018 §6.4)"
        )

    def test_enpi_compared_to_energy_baseline(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("enpi_compared_to_energy_baseline", False), (
            "EnPI values must be compared to the energy baseline to demonstrate "
            "energy performance improvement (ISO 50001:2018 §6.4)"
        )
```

---

## Energy Objectives, Targets, and Action Plans (§6.5 / §6.6)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestEnergyObjectivesAndActionPlans:
    """ISO 50001 §6.5/§6.6 — Energy objectives and targets documented, quantified, monitored; action plans complete."""

    def test_energy_objectives_and_targets_documented(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("energy_objectives_and_targets_documented", False), (
            "Energy objectives and associated energy targets must be documented "
            "(ISO 50001:2018 §6.5)"
        )

    def test_energy_objectives_are_quantified(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("energy_objectives_quantified", False), (
            "Energy targets must be quantified and measurable "
            "(ISO 50001:2018 §6.5)"
        )

    def test_action_plans_exist_for_all_energy_objectives(
        self, controls_evidence: dict
    ):
        objectives = controls_evidence.get("iso_50001_energy_objectives", [])
        no_action_plan = [
            o for o in objectives
            if not o.get("action_plan_exists", False)
        ]
        assert not no_action_plan, (
            f"Action plans must exist for each energy objective "
            f"(ISO 50001:2018 §6.6). Missing: {[o['objective_id'] for o in no_action_plan]}"
        )

    def test_action_plans_contain_required_elements(self, controls_evidence: dict):
        action_plans = controls_evidence.get("iso_50001_action_plans", [])
        for plan in action_plans:
            present = set(plan.get("elements_present", []))
            missing = ISO_50001_ACTION_PLAN_REQUIRED_ELEMENTS - present
            assert not missing, (
                f"Action plan '{plan['plan_id']}' is missing required elements: "
                f"{missing} (ISO 50001:2018 §6.6)"
            )
```

---

## Compliance Evaluation (§9.1.2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestComplianceEvaluation:
    """ISO 50001 §9.1.2 — Compliance with energy-related legal requirements evaluated at planned intervals; records retained."""

    def test_compliance_evaluation_conducted(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("compliance_evaluation_conducted", False), (
            "Compliance with energy-related legal and other requirements must be "
            "evaluated at planned intervals (ISO 50001:2018 §9.1.2)"
        )

    def test_compliance_evaluation_records_retained(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("compliance_evaluation_records_retained", False), (
            "Records of compliance evaluation results must be retained "
            "(ISO 50001:2018 §9.1.2)"
        )
```

---

## Internal Audit (§9.2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestInternalAudit:
    """ISO 50001 §9.2 — Planned EnMS audit program; auditor independence; records retained."""

    def test_internal_audit_program_exists(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("internal_audit_program_documented", False), (
            "A documented internal audit program for the EnMS must exist "
            "(ISO 50001:2018 §9.2.2)"
        )

    def test_auditors_are_independent_of_audited_activity(self, controls_evidence: dict):
        audit_records = controls_evidence.get("iso_50001_audit_records", [])
        not_independent = [
            r for r in audit_records
            if not r.get("auditor_independent_of_audited_activity", False)
        ]
        assert not not_independent, (
            f"EnMS auditors must not audit their own work "
            f"(ISO 50001:2018 §9.2.2). Independence violation: "
            f"{[r['audit_id'] for r in not_independent]}"
        )

    def test_audit_records_retained(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("audit_records_retained", False), (
            "Internal audit records must be retained "
            "(ISO 50001:2018 §9.2.2)"
        )
```

---

## Management Review (§9.3)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestManagementReview:
    """ISO 50001 §9.3 — Management review at planned intervals; energy performance improvement assessed; records retained."""

    def test_management_review_conducted_at_planned_intervals(
        self, controls_evidence: dict
    ):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("management_review_conducted", False), (
            "Top management must review the EnMS at planned intervals "
            "(ISO 50001:2018 §9.3)"
        )

    def test_management_review_includes_required_inputs(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        present = set(ems.get("management_review_inputs_present", []))
        missing = ISO_50001_MANAGEMENT_REVIEW_REQUIRED_INPUTS - present
        assert not missing, (
            f"Management review must consider all required inputs. Missing: {missing} "
            f"(ISO 50001:2018 §9.3.3)"
        )

    def test_management_review_records_retained(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("management_review_records_retained", False), (
            "Records of management review must be retained "
            "(ISO 50001:2018 §9.3)"
        )
```

---

## Nonconformity and Corrective Action (§10.1)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestNonconformityAndCorrectiveAction:
    """ISO 50001 §10.1 — NCs investigated; CAPA implemented; effectiveness reviewed; records retained."""

    def test_nonconformities_investigated(self, controls_evidence: dict):
        ncs = controls_evidence.get("iso_50001_nonconformities", [])
        not_investigated = [
            nc for nc in ncs
            if not nc.get("root_cause_investigated", False)
        ]
        assert not not_investigated, (
            f"Root cause must be determined for all nonconformities "
            f"(ISO 50001:2018 §10.1). Not investigated: "
            f"{[nc['nc_id'] for nc in not_investigated]}"
        )

    def test_corrective_action_effectiveness_reviewed(self, controls_evidence: dict):
        ncs = controls_evidence.get("iso_50001_nonconformities", [])
        closed_without_review = [
            nc for nc in ncs
            if nc.get("closed", False)
            and not nc.get("effectiveness_reviewed", False)
        ]
        assert not closed_without_review, (
            f"Effectiveness of corrective action must be reviewed before closure "
            f"(ISO 50001:2018 §10.1). Closed without review: "
            f"{[nc['nc_id'] for nc in closed_without_review]}"
        )

    def test_nc_records_retained(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_50001", {})
        assert ems.get("nc_records_retained", False), (
            "Records of nonconformities and corrective actions must be retained "
            "(ISO 50001:2018 §10.1)"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-50001-ENPI-001 | §6.4 | EnPI selection methodology: PARAMETERIZED (adequacy); documented EnPIs and monitoring records: DETERMINISTIC | 2027-05-21 |
