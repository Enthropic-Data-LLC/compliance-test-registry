# ISO 45001:2018 — Occupational Health and Safety Management System

**Framework:** ISO 45001:2018 (Annex SL — harmonized with ISO 9001, ISO 14001, ISO 27001)
**Clauses:** §5.2 (OH&S policy), §6.1.2 (hazard identification and risk assessment), §6.1.3 (legal requirements), §6.2 (OH&S objectives), §7.2 (competence), §8.1.3 (management of change), §9.1.2 (compliance evaluation), §9.2 (internal audit), §9.3 (management review), §10.2 (incident investigation + CAPA)
**Confidence:** DETERMINISTIC-dominant (policy, legal register, objectives, incident records, audit program, management review, CAPA); PARAMETERIZED (hazard identification methodology, hierarchy of controls adequacy)
**Last parsed:** 2026-05-21
**Applies to:** Any organization seeking to implement or certify an Occupational Health and Safety Management System (OHSMS); required in some supply chains (construction, mining, manufacturing, oil and gas) as a contractor qualification criterion
**Trigger:** Voluntary certification; contractual requirement in construction, oil and gas, and manufacturing supply chains; government procurement requirement in some countries; organizational OHS risk management decision; replaces OHSAS 18001 (retired 2021)
**Jurisdiction:** Global — ISO international standard; recognized in all major markets
**Not applicable to:** ISO 45001 does not replace mandatory OHS regulations — OSHA standards (29 CFR 1910, 1926) in the US and equivalent national regulations impose binding requirements independent of ISO 45001 certification; ISO 45001 is the management system framework, not the regulatory floor

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def iso_45001_scope(entity_profile: dict):
    if not entity_profile.get("iso_45001_in_scope", False):
        pytest.skip("ISO 45001 not in scope")
```

---

## Constants

```python
from datetime import date

# Required commitments in OH&S policy (§5.2)
ISO_45001_OHS_POLICY_REQUIRED_COMMITMENTS = frozenset({
    "provide_safe_and_healthy_working_conditions",
    "eliminate_hazards_and_reduce_ohs_risks",
    "fulfil_legal_and_other_requirements",
    "consult_and_participate_workers",
    "continual_improvement_of_ohs_ms",
})

# Required inputs to management review (§9.3.2)
ISO_45001_MANAGEMENT_REVIEW_REQUIRED_INPUTS = frozenset({
    "status_of_previous_review_actions",
    "changes_in_external_internal_issues",
    "ohs_performance_and_trends",
    "consultation_and_participation_results",
    "incidents_nonconformities_corrective_actions",
    "monitoring_and_measurement_results",
    "compliance_evaluation_results",
    "legal_requirement_changes",
    "risk_and_opportunity_status",
    "adequacy_of_resources",
    "communication_from_interested_parties",
    "opportunities_for_continual_improvement",
})

# Required fields in incident investigation record (§10.2.1)
ISO_45001_INCIDENT_RECORD_REQUIRED_FIELDS = frozenset({
    "incident_description",
    "root_cause_identified",
    "corrective_actions_determined",
    "effectiveness_of_actions_verified",
    "communicated_to_workers",
    "reported_to_relevant_interested_parties",
})

# Hierarchy of controls (§8.1.2) — order is DETERMINISTIC; adequacy is PARAMETERIZED
ISO_45001_HIERARCHY_OF_CONTROLS = [
    "elimination",
    "substitution",
    "engineering_controls",
    "administrative_controls",
    "ppe",
]
```

---

## OH&S Policy (§5.2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestOHSPolicy:
    """ISO 45001 §5.2 — Written OH&S policy with required commitments; communicated; accessible."""

    def test_ohs_policy_exists_and_is_documented(self, controls_evidence: dict):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("ohs_policy_documented", False), (
            "A documented OH&S policy must exist and be maintained "
            "(ISO 45001:2018 §5.2)"
        )

    def test_ohs_policy_contains_required_commitments(self, controls_evidence: dict):
        ohs = controls_evidence.get("iso_45001", {})
        present = set(ohs.get("ohs_policy_commitments_present", []))
        missing = ISO_45001_OHS_POLICY_REQUIRED_COMMITMENTS - present
        assert not missing, (
            f"OH&S policy must include all required commitments. Missing: {missing} "
            f"(ISO 45001:2018 §5.2(a)–(e))"
        )

    def test_ohs_policy_communicated_to_workers(self, controls_evidence: dict):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("ohs_policy_communicated_to_workers", False), (
            "OH&S policy must be communicated within the organization and be "
            "available to interested parties (ISO 45001:2018 §5.2)"
        )
```

---

## Legal and Other Requirements Register (§6.1.3)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestLegalRequirementsRegister:
    """ISO 45001 §6.1.3 — Register of applicable OH&S legal and other requirements; kept current."""

    def test_legal_requirements_register_exists(self, controls_evidence: dict):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("legal_requirements_register_exists", False), (
            "A register of applicable OH&S legal and other requirements must be "
            "maintained (ISO 45001:2018 §6.1.3)"
        )

    def test_legal_requirements_register_is_current(
        self, controls_evidence: dict, reference_date: date
    ):
        ohs = controls_evidence.get("iso_45001", {})
        last_reviewed = ohs.get("legal_register_last_reviewed")
        assert last_reviewed is not None, (
            "Legal requirements register must have a documented last-review date "
            "(ISO 45001:2018 §6.1.3)"
        )
        assert last_reviewed >= reference_date.replace(year=reference_date.year - 1), (
            f"Legal requirements register must be reviewed at least annually. "
            f"Last reviewed: {last_reviewed} (ISO 45001:2018 §6.1.3)"
        )

    def test_osha_and_applicable_regulations_included_in_register(
        self, controls_evidence: dict
    ):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("applicable_osha_regulations_in_register", False), (
            "Applicable occupational safety regulations (OSHA, local equivalents) "
            "must be identified and included in the legal requirements register "
            "(ISO 45001:2018 §6.1.3)"
        )
```

---

## Hazard Identification and Risk Assessment (§6.1.2)

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestHazardIdentificationAndRiskAssessment:
    """ISO 45001 §6.1.2 — Documented hazard identification and OH&S risk assessment process."""

    @pytest.mark.assumption(
        id="ASSUME-45001-HIRA-001",
        description=(
            "Hazard identification methodology is organization-defined: must cover "
            "routine and non-routine activities, emergencies, contractor activities, "
            "and psychosocial hazards; risk assessment criteria (likelihood × severity) "
            "are org-defined; adequacy of methodology is PARAMETERIZED — existence of "
            "documented process and hazard register is DETERMINISTIC"
        ),
        approved_by="hse_manager",
        review_date="2027-05-21",
    )
    def test_hazard_identification_process_documented(self, controls_evidence: dict):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("hazard_identification_process_documented", False), (
            "A documented process for hazard identification must exist, covering "
            "routine, non-routine, and emergency activities "
            "(ISO 45001:2018 §6.1.2)"
        )

    def test_hazard_register_exists(self, controls_evidence: dict):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("hazard_register_exists", False), (
            "A hazard register (or equivalent documented risk assessment output) "
            "must exist for applicable activities (ISO 45001:2018 §6.1.2)"
        )

    def test_hierarchy_of_controls_applied_to_significant_risks(
        self, controls_evidence: dict
    ):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("hierarchy_of_controls_applied", False), (
            "Controls for identified hazards must follow the hierarchy of controls: "
            f"{ISO_45001_HIERARCHY_OF_CONTROLS} — elimination first, PPE last "
            "(ISO 45001:2018 §8.1.2)"
        )
```

---

## OH&S Objectives (§6.2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestOHSObjectives:
    """ISO 45001 §6.2 — Documented, measurable OH&S objectives; monitored; communicated."""

    def test_ohs_objectives_documented_and_measurable(self, controls_evidence: dict):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("ohs_objectives_documented", False), (
            "OH&S objectives must be documented and be measurable "
            "(ISO 45001:2018 §6.2.1)"
        )

    def test_ohs_objectives_monitored_and_communicated(self, controls_evidence: dict):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("ohs_objectives_monitored", False), (
            "Progress toward OH&S objectives must be monitored and results "
            "communicated (ISO 45001:2018 §6.2.1)"
        )
```

---

## Management of Change (§8.1.3)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestManagementOfChange:
    """ISO 45001 §8.1.3 — OH&S impact of operational changes evaluated before implementation."""

    def test_change_management_process_for_ohs_exists(self, controls_evidence: dict):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("change_management_process_documented", False), (
            "A process for evaluating OH&S impacts of planned changes must exist "
            "(ISO 45001:2018 §8.1.3)"
        )

    def test_planned_changes_evaluated_for_ohs_impact_before_implementation(
        self, controls_evidence: dict
    ):
        changes = controls_evidence.get("iso_45001_changes", [])
        not_evaluated = [
            c for c in changes
            if not c.get("ohs_impact_evaluated_before_implementation", False)
        ]
        assert not not_evaluated, (
            f"Planned changes (process, organizational, equipment) must have OH&S "
            f"impact evaluated before implementation (ISO 45001:2018 §8.1.3). "
            f"Not evaluated: {[c['change_id'] for c in not_evaluated]}"
        )
```

---

## Compliance Evaluation (§9.1.2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestComplianceEvaluation:
    """ISO 45001 §9.1.2 — Periodic evaluation of compliance with legal and other requirements; records retained."""

    def test_compliance_evaluation_conducted_at_planned_intervals(
        self, controls_evidence: dict
    ):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("compliance_evaluation_conducted", False), (
            "Compliance with OH&S legal and other requirements must be evaluated "
            "at planned intervals (ISO 45001:2018 §9.1.2)"
        )

    def test_compliance_evaluation_records_retained(self, controls_evidence: dict):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("compliance_evaluation_records_retained", False), (
            "Records of compliance evaluation results must be retained "
            "(ISO 45001:2018 §9.1.2)"
        )
```

---

## Internal Audit (§9.2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestInternalAudit:
    """ISO 45001 §9.2 — Planned OH&S audit program; auditor independence; records retained."""

    def test_internal_audit_program_exists(self, controls_evidence: dict):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("internal_audit_program_documented", False), (
            "A documented internal audit program for the OH&S management system "
            "must exist (ISO 45001:2018 §9.2.2)"
        )

    def test_auditors_are_independent_of_audited_activity(self, controls_evidence: dict):
        audit_records = controls_evidence.get("iso_45001_audit_records", [])
        not_independent = [
            r for r in audit_records
            if not r.get("auditor_independent_of_audited_activity", False)
        ]
        assert not not_independent, (
            f"Auditors must not audit their own work (ISO 45001:2018 §9.2.2). "
            f"Independence violation: {[r['audit_id'] for r in not_independent]}"
        )

    def test_audit_records_retained(self, controls_evidence: dict):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("audit_records_retained", False), (
            "Internal audit records must be retained as evidence of the audit "
            "program and results (ISO 45001:2018 §9.2.2)"
        )
```

---

## Management Review (§9.3)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestManagementReview:
    """ISO 45001 §9.3 — Management review at planned intervals; required inputs; records retained."""

    def test_management_review_conducted_at_planned_intervals(
        self, controls_evidence: dict
    ):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("management_review_conducted", False), (
            "Top management must review the OH&S management system at planned "
            "intervals (ISO 45001:2018 §9.3)"
        )

    def test_management_review_includes_required_inputs(self, controls_evidence: dict):
        ohs = controls_evidence.get("iso_45001", {})
        present = set(ohs.get("management_review_inputs_present", []))
        missing = ISO_45001_MANAGEMENT_REVIEW_REQUIRED_INPUTS - present
        assert not missing, (
            f"Management review must consider all required inputs. Missing: {missing} "
            f"(ISO 45001:2018 §9.3.2)"
        )

    def test_management_review_records_retained(self, controls_evidence: dict):
        ohs = controls_evidence.get("iso_45001", {})
        assert ohs.get("management_review_records_retained", False), (
            "Records of management review must be retained "
            "(ISO 45001:2018 §9.3)"
        )
```

---

## Incident Investigation and Corrective Action (§10.2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestIncidentInvestigationAndCorrective:
    """ISO 45001 §10.2 — All incidents investigated; root cause; CAPA; effectiveness; worker communication."""

    def test_all_incidents_investigated(self, controls_evidence: dict):
        incidents = controls_evidence.get("iso_45001_incidents", [])
        not_investigated = [
            i for i in incidents
            if not i.get("investigation_completed", False)
        ]
        assert not not_investigated, (
            f"All incidents (including near-misses) must be investigated "
            f"(ISO 45001:2018 §10.2.1). Not investigated: "
            f"{[i['incident_id'] for i in not_investigated]}"
        )

    def test_incident_records_contain_required_fields(self, controls_evidence: dict):
        incidents = controls_evidence.get("iso_45001_incidents", [])
        for incident in incidents:
            if not incident.get("investigation_completed", False):
                continue
            present = set(incident.get("record_fields_present", []))
            missing = ISO_45001_INCIDENT_RECORD_REQUIRED_FIELDS - present
            assert not missing, (
                f"Incident record for '{incident['incident_id']}' is missing required "
                f"fields: {missing} (ISO 45001:2018 §10.2.1)"
            )

    def test_corrective_action_effectiveness_verified_before_closure(
        self, controls_evidence: dict
    ):
        corrective_actions = controls_evidence.get("iso_45001_corrective_actions", [])
        not_verified = [
            ca for ca in corrective_actions
            if ca.get("closed", False)
            and not ca.get("effectiveness_verified_before_closure", False)
        ]
        assert not not_verified, (
            f"Corrective action effectiveness must be verified before closure "
            f"(ISO 45001:2018 §10.2.1(f)). "
            f"Closed without verification: {[ca['ca_id'] for ca in not_verified]}"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-45001-HIRA-001 | §6.1.2 | Hazard identification methodology: PARAMETERIZED (adequacy); documented process and hazard register existence: DETERMINISTIC | 2027-05-21 |
