# ISO 14001:2015 — Environmental Management System

**Framework:** ISO 14001:2015 (Annex SL — harmonized with ISO 9001, ISO 45001, ISO 27001)
**Clauses:** §5.2 (environmental policy), §6.1.1 (environmental aspects), §6.1.2 (compliance obligations), §6.2 (environmental objectives), §7.2 (competence), §8.2 (emergency preparedness), §9.1.2 (compliance evaluation), §9.2 (internal audit), §9.3 (management review), §10.2 (nonconformity and corrective action)
**Confidence:** DETERMINISTIC-dominant (policy, compliance register, objectives, competence, audit, management review, CAPA, compliance evaluation); PARAMETERIZED/CONTESTED (environmental aspects significance determination)
**Last parsed:** 2026-05-21

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def iso_14001_scope(entity_profile: dict):
    if not entity_profile.get("iso_14001_in_scope", False):
        pytest.skip("ISO 14001 not in scope")
```

---

## Constants

```python
from datetime import date

# Required commitments in environmental policy (§5.2)
ISO_14001_ENVIRONMENTAL_POLICY_REQUIRED_COMMITMENTS = frozenset({
    "protect_the_environment",
    "fulfil_compliance_obligations",
    "continual_improvement_of_ems",
})

# Required inputs to management review (§9.3)
ISO_14001_MANAGEMENT_REVIEW_REQUIRED_INPUTS = frozenset({
    "status_of_previous_review_actions",
    "changes_in_external_internal_issues",
    "extent_of_environmental_objectives_achieved",
    "environmental_performance_information",
    "adequacy_of_resources",
    "communications_from_interested_parties",
    "compliance_obligations_fulfilment",
    "nonconformities_and_corrective_actions",
    "opportunities_for_improvement",
})

# Required documented information — minimum retained records
ISO_14001_REQUIRED_DOCUMENTED_INFORMATION = frozenset({
    "ems_scope",
    "environmental_policy",
    "environmental_aspects_register",
    "compliance_obligations_register",
    "evidence_of_environmental_objectives",
    "competence_evidence",
    "internal_audit_program",
    "audit_results",
    "management_review_records",
    "nonconformity_and_corrective_action_records",
    "monitoring_and_measurement_results",
    "compliance_evaluation_results",
})
```

---

## Environmental Policy (§5.2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestEnvironmentalPolicy:
    """ISO 14001 §5.2 — Written environmental policy with required commitments; available to interested parties."""

    def test_environmental_policy_exists_and_is_documented(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("environmental_policy_documented", False), (
            "A documented environmental policy must exist and be maintained "
            "(ISO 14001:2015 §5.2)"
        )

    def test_environmental_policy_contains_required_commitments(
        self, controls_evidence: dict
    ):
        ems = controls_evidence.get("iso_14001", {})
        present = set(ems.get("environmental_policy_commitments_present", []))
        missing = ISO_14001_ENVIRONMENTAL_POLICY_REQUIRED_COMMITMENTS - present
        assert not missing, (
            f"Environmental policy must include all required commitments. Missing: {missing} "
            f"(ISO 14001:2015 §5.2(a)–(c))"
        )

    def test_environmental_policy_available_to_interested_parties(
        self, controls_evidence: dict
    ):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("environmental_policy_publicly_available", False), (
            "Environmental policy must be available to interested parties "
            "(ISO 14001:2015 §5.2)"
        )
```

---

## Environmental Aspects and Significance (§6.1.1)

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestEnvironmentalAspects:
    """ISO 14001 §6.1.1 — Environmental aspects identified using life cycle perspective; significance criteria documented."""

    @pytest.mark.assumption(
        id="ASSUME-14001-ASPECTS-001",
        description=(
            "Environmental aspects significance methodology is organization-defined: "
            "criteria (scale of impact, severity, frequency, legal profile, stakeholder "
            "concern, etc.) are set by the organization; adequacy of criteria is "
            "PARAMETERIZED — existence of documented aspects register and significance "
            "criteria is DETERMINISTIC"
        ),
        approved_by="ems_manager",
        review_date="2027-05-21",
    )
    def test_environmental_aspects_register_exists(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("environmental_aspects_register_exists", False), (
            "An environmental aspects register (identifying aspects, associated impacts, "
            "and significance determination) must exist "
            "(ISO 14001:2015 §6.1.1)"
        )

    def test_aspects_identified_using_life_cycle_perspective(
        self, controls_evidence: dict
    ):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("life_cycle_perspective_applied", False), (
            "Environmental aspects must be identified considering a life cycle perspective "
            "(upstream to downstream activities, not just on-site operations) "
            "(ISO 14001:2015 §6.1.1)"
        )

    def test_significance_criteria_documented(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("significance_criteria_documented", False), (
            "Criteria for determining significance of environmental aspects must be "
            "documented (ISO 14001:2015 §6.1.1)"
        )
```

---

## Compliance Obligations Register (§6.1.2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestComplianceObligationsRegister:
    """ISO 14001 §6.1.2 — Written register of environmental legal and other compliance obligations; kept current."""

    def test_compliance_obligations_register_exists(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("compliance_obligations_register_exists", False), (
            "A register of applicable environmental legal and other compliance "
            "obligations must exist (ISO 14001:2015 §6.1.2)"
        )

    def test_compliance_register_is_current(
        self, controls_evidence: dict, reference_date: date
    ):
        ems = controls_evidence.get("iso_14001", {})
        last_reviewed = ems.get("compliance_register_last_reviewed")
        assert last_reviewed is not None, (
            "Compliance obligations register must have a documented last-review date "
            "(ISO 14001:2015 §6.1.2)"
        )
        assert last_reviewed >= reference_date.replace(year=reference_date.year - 1), (
            f"Compliance obligations register must be reviewed at least annually. "
            f"Last reviewed: {last_reviewed} (ISO 14001:2015 §6.1.2)"
        )

    def test_environmental_permits_and_conditions_included(
        self, controls_evidence: dict
    ):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("permits_and_conditions_in_register", False), (
            "Environmental permits, licenses, and their conditions must be identified "
            "in the compliance obligations register (ISO 14001:2015 §6.1.2)"
        )
```

---

## Environmental Objectives (§6.2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestEnvironmentalObjectives:
    """ISO 14001 §6.2 — Documented, measurable environmental objectives; monitored; consistent with policy."""

    def test_environmental_objectives_documented(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("environmental_objectives_documented", False), (
            "Environmental objectives must be documented "
            "(ISO 14001:2015 §6.2.1)"
        )

    def test_environmental_objectives_are_measurable(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("environmental_objectives_measurable", False), (
            "Environmental objectives must be measurable (where practicable) "
            "(ISO 14001:2015 §6.2.1)"
        )

    def test_environmental_objective_progress_monitored(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("objective_progress_monitored_and_communicated", False), (
            "Progress toward environmental objectives must be monitored "
            "(ISO 14001:2015 §6.2.2)"
        )
```

---

## Emergency Preparedness and Response (§8.2)

**Overall: DETERMINISTIC (plan exists and is tested) — Pattern 1**

```python
class TestEmergencyPreparedness:
    """ISO 14001 §8.2 — Emergency preparedness plan for environmental emergencies; tested at intervals."""

    def test_emergency_preparedness_plan_exists(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("emergency_preparedness_plan_documented", False), (
            "A documented emergency preparedness and response plan addressing "
            "potential environmental emergencies must exist "
            "(ISO 14001:2015 §8.2)"
        )

    def test_emergency_response_plan_tested_at_planned_intervals(
        self, controls_evidence: dict
    ):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("emergency_plan_tested_at_planned_intervals", False), (
            "The emergency preparedness and response plan must be tested periodically "
            "where practicable (ISO 14001:2015 §8.2)"
        )
```

---

## Compliance Evaluation (§9.1.2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestComplianceEvaluation:
    """ISO 14001 §9.1.2 — Compliance with environmental legal and other obligations evaluated at planned intervals; records retained."""

    def test_compliance_evaluation_conducted_at_planned_intervals(
        self, controls_evidence: dict
    ):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("compliance_evaluation_conducted", False), (
            "Compliance with environmental compliance obligations must be evaluated "
            "at planned intervals (ISO 14001:2015 §9.1.2)"
        )

    def test_compliance_evaluation_records_retained(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("compliance_evaluation_records_retained", False), (
            "Records of compliance evaluation results must be retained "
            "(ISO 14001:2015 §9.1.2)"
        )
```

---

## Internal Audit (§9.2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestInternalAudit:
    """ISO 14001 §9.2 — Planned EMS audit program; auditor independence; records retained."""

    def test_internal_audit_program_exists(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("internal_audit_program_documented", False), (
            "A documented internal audit program for the EMS must exist "
            "(ISO 14001:2015 §9.2.2)"
        )

    def test_auditors_are_independent_of_audited_activity(self, controls_evidence: dict):
        audit_records = controls_evidence.get("iso_14001_audit_records", [])
        not_independent = [
            r for r in audit_records
            if not r.get("auditor_independent_of_audited_activity", False)
        ]
        assert not not_independent, (
            f"EMS auditors must not audit their own work "
            f"(ISO 14001:2015 §9.2.2). Independence violation: "
            f"{[r['audit_id'] for r in not_independent]}"
        )

    def test_audit_records_retained(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("audit_records_retained", False), (
            "Internal audit records must be retained as evidence of the audit "
            "program and results (ISO 14001:2015 §9.2.2)"
        )
```

---

## Management Review (§9.3)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestManagementReview:
    """ISO 14001 §9.3 — Management review at planned intervals; required inputs; records retained."""

    def test_management_review_conducted_at_planned_intervals(
        self, controls_evidence: dict
    ):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("management_review_conducted", False), (
            "Top management must review the EMS at planned intervals "
            "(ISO 14001:2015 §9.3)"
        )

    def test_management_review_includes_required_inputs(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_14001", {})
        present = set(ems.get("management_review_inputs_present", []))
        missing = ISO_14001_MANAGEMENT_REVIEW_REQUIRED_INPUTS - present
        assert not missing, (
            f"Management review must consider all required inputs. Missing: {missing} "
            f"(ISO 14001:2015 §9.3)"
        )

    def test_management_review_records_retained(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("management_review_records_retained", False), (
            "Records of management review must be retained "
            "(ISO 14001:2015 §9.3)"
        )
```

---

## Nonconformity and Corrective Action (§10.2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestNonconformityAndCorrectiveAction:
    """ISO 14001 §10.2 — NCs reacted to; root cause; CAPA implemented; effectiveness reviewed; records retained."""

    def test_nonconformities_reacted_to_immediately(self, controls_evidence: dict):
        ncs = controls_evidence.get("iso_14001_nonconformities", [])
        not_reacted = [
            nc for nc in ncs
            if not nc.get("immediate_action_taken", False)
        ]
        assert not not_reacted, (
            f"Immediate action must be taken to control and correct nonconformities "
            f"(ISO 14001:2015 §10.2). Not reacted to: "
            f"{[nc['nc_id'] for nc in not_reacted]}"
        )

    def test_root_cause_determined_for_nonconformities(self, controls_evidence: dict):
        ncs = controls_evidence.get("iso_14001_nonconformities", [])
        no_root_cause = [
            nc for nc in ncs
            if not nc.get("root_cause_determined", False)
        ]
        assert not no_root_cause, (
            f"Root cause must be determined for all nonconformities "
            f"(ISO 14001:2015 §10.2). Missing root cause: "
            f"{[nc['nc_id'] for nc in no_root_cause]}"
        )

    def test_corrective_action_effectiveness_reviewed(self, controls_evidence: dict):
        ncs = controls_evidence.get("iso_14001_nonconformities", [])
        closed_without_review = [
            nc for nc in ncs
            if nc.get("closed", False)
            and not nc.get("effectiveness_of_corrective_action_reviewed", False)
        ]
        assert not closed_without_review, (
            f"Effectiveness of corrective action must be reviewed before closure "
            f"(ISO 14001:2015 §10.2). Closed without review: "
            f"{[nc['nc_id'] for nc in closed_without_review]}"
        )

    def test_corrective_action_records_retained(self, controls_evidence: dict):
        ems = controls_evidence.get("iso_14001", {})
        assert ems.get("nc_and_corrective_action_records_retained", False), (
            "Records of nonconformities and corrective actions must be retained "
            "(ISO 14001:2015 §10.2)"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-14001-ASPECTS-001 | §6.1.1 | Environmental aspects significance methodology: PARAMETERIZED (adequacy); documented register and significance criteria existence: DETERMINISTIC | 2027-05-21 |
