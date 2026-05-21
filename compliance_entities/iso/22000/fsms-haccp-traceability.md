# ISO 22000:2018 — Food Safety Management System: HACCP, Traceability, and FSMS Requirements

**Framework:** ISO 22000:2018 Food Safety Management Systems — Requirements for any organization in the food chain
**Clauses:** Clause 5.2 (food safety policy); Clause 7.2 (competence); Clause 7.5 (documented information); Clause 8.2 (PRPs); Clause 8.3 (traceability); Clause 8.5.4 (Hazard Control Plan — HACCP + OPRPs); Clause 8.8 (verification of HACCP); Clause 9.2 (internal audit); Clause 9.3 (management review); Clause 10.1 (nonconformity and corrective action)
**Confidence:** DETERMINISTIC-dominant (Hazard Control Plan 7-element documentation checklist; 1-step traceability forward and back; internal audit scheduled program; management review records; corrective action records); PARAMETERIZED (hazard analysis content; critical limit values; PRP content; competence criteria); CONTESTED (hazard characterization; OPRP vs. CCP classification)
**Last parsed:** 2026-05-21
**Applies to:** Any organization in the food chain regardless of size or complexity — primary production (farms, dairies, fisheries), food processing, food service, retail, and transport/storage; also feed producers, food contact material manufacturers, food packaging manufacturers, and food equipment/sanitizer suppliers; FSSC 22000 adds sector-specific PRPs on top
**Trigger:** Customer contractual requirement for ISO 22000 or FSSC 22000 certification; GFSI-benchmark scheme acceptance (retailers, foodservice chains); regulatory reference (some national food laws reference ISO 22000 as an accepted FSMS standard); voluntary organizational decision for food safety management system credibility
**Jurisdiction:** Global — ISO international standard; certified by accredited certification bodies; recognized by GFSI and major food retailers and foodservice operators worldwide
**Not applicable to:** Organizations outside the food chain with no food safety impact; organizations producing non-food products; ISO 22000 certification scope is organization-defined and may exclude specific processes or sites

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def iso22000_scope(entity_profile: dict):
    if not entity_profile.get("iso22000_fsms_in_scope", False):
        pytest.skip(
            "ISO 22000:2018 does not apply — entity is not in the food chain "
            "or has not adopted an ISO 22000 FSMS."
        )
```

---

## Constants

```python
from typing import FrozenSet

# ── Hazard Control Plan — required elements per CCP and OPRP ──────────────────
# ISO 22000:2018 §8.5.4 — all 7 elements must be documented for each CCP/OPRP

HACCP_CONTROL_PLAN_REQUIRED_ELEMENTS: FrozenSet[str] = frozenset({
    "food_safety_hazards_controlled",
    "control_measures",
    "critical_limits",           # CCPs; action criteria for OPRPs
    "monitoring_procedures_and_frequency",
    "corrective_actions_when_limits_exceeded",
    "responsibilities_and_authorities",
    "records_of_monitoring",
})

# ── Management review — required inputs (§9.3.2) ──────────────────────────────

MANAGEMENT_REVIEW_REQUIRED_INPUTS: FrozenSet[str] = frozenset({
    "status_of_actions_from_previous_reviews",
    "changes_affecting_fsms",
    "monitoring_and_measurement_results",
    "nonconformity_and_corrective_action_summary",
    "audit_results",
    "external_provider_performance",
    "hazard_control_plan_updates",
    "emergency_situations_or_incidents",
    "continual_improvement_opportunities",
})

# ── Internal audit program — minimum requirements ─────────────────────────────

INTERNAL_AUDIT_REQUIRED_ELEMENTS: FrozenSet[str] = frozenset({
    "audit_schedule_documented",
    "audit_criteria_defined",
    "audit_scope_defined",
    "auditor_competence_independence_ensured",
    "audit_results_reported",
    "corrective_actions_taken_for_findings",
    "records_retained",
})
```

---

## TestFoodSafetyPolicy

```python
class TestFoodSafetyPolicy:
    """ISO 22000:2018 §5.2 — Food safety policy: written, communicated, available."""

    def test_food_safety_policy_documented(self, entity_profile: dict):
        """§5.2.1: Organization must establish a documented food safety policy."""
        policy = entity_profile.get("food_safety_policy", {})
        assert policy.get("documented") is True, \
            "No documented food safety policy — ISO 22000:2018 §5.2.1 requires written policy"

    def test_food_safety_policy_communicated(self, entity_profile: dict):
        """§5.2.2: Policy must be communicated and available within the organization."""
        policy = entity_profile.get("food_safety_policy", {})
        assert policy.get("communicated_to_organization") is True, \
            "Food safety policy not communicated — ISO 22000:2018 §5.2.2"

    def test_food_safety_policy_reviewed_periodically(self, entity_profile: dict):
        """§5.2.2(c): Policy must be reviewed for continuing suitability."""
        policy = entity_profile.get("food_safety_policy", {})
        assert policy.get("periodic_review_scheduled") is True, \
            "Food safety policy review not scheduled — ISO 22000:2018 §5.2.2(c)"
```

---

## TestCompetenceAndTraining

```python
class TestCompetenceAndTraining:
    """ISO 22000:2018 §7.2 — Competence: documented evidence required."""

    def test_competence_records_exist_for_food_safety_roles(self, entity_profile: dict):
        """§7.2: Organization must retain documented information as evidence of competence."""
        roles = entity_profile.get("food_safety_roles", [])
        assert roles, "No food safety roles defined in entity profile"
        for role in roles:
            assert role.get("competence_records_retained") is True, (
                f"No competence records for food safety role '{role.get('title', 'unknown')}' "
                f"— ISO 22000:2018 §7.2"
            )

    def test_food_safety_team_members_competent(self, entity_profile: dict):
        """§8.5.1.1: Food safety team members must have knowledge and experience
        in hazard analysis and HACCP."""
        team = entity_profile.get("food_safety_team", [])
        assert team, "No food safety team members found"
        for member in team:
            assert member.get("haccp_competence_documented") is True, (
                f"Team member '{member.get('name', 'unknown')}' lacks documented "
                f"HACCP/hazard analysis competence — ISO 22000:2018 §8.5.1.1"
            )
```

---

## TestPrerequisitePrograms

```python
class TestPrerequisitePrograms:
    """ISO 22000:2018 §8.2 — Prerequisite programs (PRPs): existence and documentation."""

    def test_prps_established_and_documented(self, entity_profile: dict):
        """§8.2.1: PRPs must be established, implemented, maintained, and documented."""
        assert entity_profile.get("prerequisite_programs", {}).get("documented") is True, \
            "PRPs not documented — ISO 22000:2018 §8.2.1"

    def test_prp_monitoring_records_retained(self, entity_profile: dict):
        """§8.2.4: PRP monitoring must be conducted and records retained."""
        for prp in entity_profile.get("prerequisite_programs", {}).get("list", []):
            assert prp.get("monitoring_records_retained") is True, (
                f"PRP '{prp.get('name', 'unknown')}' has no monitoring records — "
                f"ISO 22000:2018 §8.2.4"
            )

    @pytest.mark.assumption(
        id="ASSUME-ISO22000-PRP-001",
        text="PRP content (e.g., cleaning and disinfection procedures, pest control, "
             "maintenance program, cross-contamination controls) is sector-specific and "
             "defined by ISO/TS 22002 series (sector-specific PRPs) or equivalent "
             "recognized standards; the specific PRP content is accepted as documented.",
        confidence="PARAMETERIZED",
        approved_by=None,
    )
    def test_prp_content_appropriate_for_sector(self, entity_profile: dict):
        """§8.2.1: PRP content must be appropriate to the organization's needs
        and the food safety hazards in the food chain."""
        prp = entity_profile.get("prerequisite_programs", {})
        assert prp.get("sector_appropriateness_assessed") is True, \
            "PRP sector appropriateness not assessed — ISO 22000:2018 §8.2.1"
```

---

## TestTraceability

```python
class TestTraceability:
    """ISO 22000:2018 §8.3 — Traceability: one-step-back and one-step-forward minimum."""

    def test_one_step_back_traceability_exists(self, entity_profile: dict):
        """§8.3: Must be able to identify inputs (raw materials, ingredients, contact materials)
        from their direct supplier."""
        for batch in entity_profile.get("finished_product_batches", []):
            assert batch.get("one_step_back_traceable") is True, (
                f"Batch '{batch.get('id', 'unknown')}' cannot be traced one step back to "
                f"input supplier — ISO 22000:2018 §8.3"
            )

    def test_one_step_forward_traceability_exists(self, entity_profile: dict):
        """§8.3: Must be able to identify where product was dispatched to
        (immediate customer/distributor)."""
        for batch in entity_profile.get("finished_product_batches", []):
            assert batch.get("one_step_forward_traceable") is True, (
                f"Batch '{batch.get('id', 'unknown')}' cannot be traced one step forward "
                f"to customer/distributor — ISO 22000:2018 §8.3"
            )

    def test_lot_batch_linkage_to_ingredients(self, entity_profile: dict):
        """§8.3: Finished product lot/batch must be linkable to ingredient lots used."""
        for batch in entity_profile.get("finished_product_batches", []):
            assert batch.get("ingredient_lot_linkage") is True, (
                f"Batch '{batch.get('id', 'unknown')}' not linked to ingredient lots — "
                f"ISO 22000:2018 §8.3"
            )

    def test_traceability_records_retained(self, entity_profile: dict):
        """§8.3: Traceability records must be retained for a defined period."""
        traceability = entity_profile.get("traceability_system", {})
        assert traceability.get("record_retention_defined") is True, \
            "Traceability record retention period not defined — ISO 22000:2018 §8.3"
```

---

## TestHazardControlPlan

```python
class TestHazardControlPlan:
    """ISO 22000:2018 §8.5.4 — Hazard Control Plan (HACCP + OPRPs): 7-element documentation."""

    def test_hazard_control_plan_documented(self, entity_profile: dict):
        """§8.5.4: Organization must maintain a documented Hazard Control Plan."""
        assert entity_profile.get("hazard_control_plan", {}).get("documented") is True, \
            "No documented Hazard Control Plan — ISO 22000:2018 §8.5.4"

    def test_each_ccp_oprp_has_all_required_elements(self, entity_profile: dict):
        """§8.5.4.1/§8.5.4.2: Each CCP and OPRP in the Hazard Control Plan must document
        all 7 required elements."""
        control_measures = entity_profile.get("hazard_control_plan", {}).get("control_measures", [])
        assert control_measures, "No CCPs or OPRPs found in Hazard Control Plan"
        for cm in control_measures:
            cm_id = cm.get("id", "unknown")
            cm_type = cm.get("type", "CCP/OPRP")
            documented_elements = frozenset(cm.get("documented_elements", []))
            missing = HACCP_CONTROL_PLAN_REQUIRED_ELEMENTS - documented_elements
            assert not missing, (
                f"{cm_type} '{cm_id}' missing required elements: {sorted(missing)} — "
                f"ISO 22000:2018 §8.5.4 requires all 7 elements for each CCP/OPRP"
            )

    def test_ccp_critical_limits_defined(self, entity_profile: dict):
        """§8.5.4.1: CCPs must have defined critical limits (measurable values that distinguish
        acceptable from unacceptable)."""
        ccps = [cm for cm in entity_profile.get("hazard_control_plan", {}).get("control_measures", [])
                if cm.get("type") == "CCP"]
        for ccp in ccps:
            assert ccp.get("critical_limits_defined") is True, (
                f"CCP '{ccp.get('id', 'unknown')}' has no defined critical limits — "
                f"ISO 22000:2018 §8.5.4.1"
            )

    @pytest.mark.assumption(
        id="ASSUME-ISO22000-HACCP-001",
        text="Classification of control measures as CCPs vs. OPRPs is a technical judgment "
             "by the food safety team based on severity of hazard and ability to monitor "
             "and apply corrective action; the classification is accepted as documented in "
             "the Hazard Control Plan.",
        confidence="CONTESTED",
        approved_by=None,
    )
    def test_ccp_oprp_classification_documented(self, entity_profile: dict):
        """§8.5.4: The basis for classifying each control measure as CCP or OPRP
        must be documented."""
        for cm in entity_profile.get("hazard_control_plan", {}).get("control_measures", []):
            assert cm.get("ccp_oprp_classification_documented") is True, (
                f"CCP/OPRP classification not documented for control measure "
                f"'{cm.get('id', 'unknown')}' — ISO 22000:2018 §8.5.4"
            )
```

---

## TestHACCPVerification

```python
class TestHACCPVerification:
    """ISO 22000:2018 §8.8 — Verification of the Hazard Control Plan."""

    def test_haccp_verification_activities_scheduled(self, entity_profile: dict):
        """§8.8.1: Verification activities must be established and implemented
        to confirm that the Hazard Control Plan is effective."""
        verification = entity_profile.get("haccp_verification", {})
        assert verification.get("scheduled_activities_defined") is True, \
            "HACCP verification activities not scheduled — ISO 22000:2018 §8.8.1"

    def test_haccp_verification_records_retained(self, entity_profile: dict):
        """§8.8.1: Records of verification activities must be retained."""
        verification = entity_profile.get("haccp_verification", {})
        assert verification.get("records_retained") is True, \
            "HACCP verification records not retained — ISO 22000:2018 §8.8.1"
```

---

## TestInternalAudit

```python
class TestInternalAudit:
    """ISO 22000:2018 §9.2 — Internal audit: planned program with records."""

    def test_internal_audit_program_documented(self, entity_profile: dict):
        """§9.2.2: Organization must have a documented internal audit program."""
        audit_program = entity_profile.get("internal_audit_program", {})
        assert audit_program.get("documented") is True, \
            "No internal audit program documented — ISO 22000:2018 §9.2.2"

    def test_internal_audit_program_has_required_elements(self, entity_profile: dict):
        """§9.2.2: Internal audit program must include all required elements."""
        program = entity_profile.get("internal_audit_program", {})
        program_elements = frozenset(program.get("elements_present", []))
        missing = INTERNAL_AUDIT_REQUIRED_ELEMENTS - program_elements
        assert not missing, (
            f"Internal audit program missing required elements: {sorted(missing)} — "
            f"ISO 22000:2018 §9.2.2"
        )

    def test_internal_audit_results_retained(self, entity_profile: dict):
        """§9.2.2(f): Audit results must be reported and retained as documented information."""
        audits = entity_profile.get("internal_audits_conducted", [])
        assert audits, "No internal audits conducted or recorded"
        for audit in audits:
            assert audit.get("results_documented") is True, (
                f"Internal audit '{audit.get('id', 'unknown')}' results not documented — "
                f"ISO 22000:2018 §9.2.2(f)"
            )
```

---

## TestManagementReview

```python
class TestManagementReview:
    """ISO 22000:2018 §9.3 — Management review: planned intervals with required inputs."""

    def test_management_review_scheduled(self, entity_profile: dict):
        """§9.3.1: Management review must be conducted at planned intervals."""
        mgmt_review = entity_profile.get("management_review", {})
        assert mgmt_review.get("scheduled_at_planned_intervals") is True, \
            "Management review not scheduled — ISO 22000:2018 §9.3.1"

    def test_management_review_required_inputs_addressed(self, entity_profile: dict):
        """§9.3.2: Management review must include all required input topics."""
        mgmt_review = entity_profile.get("management_review", {})
        addressed_inputs = frozenset(mgmt_review.get("inputs_addressed", []))
        missing = MANAGEMENT_REVIEW_REQUIRED_INPUTS - addressed_inputs
        assert not missing, (
            f"Management review missing required input topics: {sorted(missing)} — "
            f"ISO 22000:2018 §9.3.2"
        )

    def test_management_review_records_retained(self, entity_profile: dict):
        """§9.3.3: Management review outputs and records must be retained."""
        reviews = entity_profile.get("management_reviews_conducted", [])
        assert reviews, "No management review records found"
        for review in reviews:
            assert review.get("records_retained") is True, (
                f"Management review '{review.get('date', 'unknown')}' records not retained — "
                f"ISO 22000:2018 §9.3.3"
            )
```

---

## TestNonconformityAndCorrectiveAction

```python
class TestNonconformityAndCorrectiveAction:
    """ISO 22000:2018 §10.1 — Nonconformity and corrective action: records required."""

    def test_nonconformities_investigated(self, entity_profile: dict):
        """§10.1.1(b): Each nonconformity must be reviewed and investigated."""
        for nc in entity_profile.get("nonconformities", []):
            assert nc.get("investigated") is True, (
                f"Nonconformity '{nc.get('id', 'unknown')}' not investigated — "
                f"ISO 22000:2018 §10.1.1(b)"
            )

    def test_corrective_actions_implemented_for_nonconformities(self, entity_profile: dict):
        """§10.1.1(c): Corrective actions must be taken to eliminate the cause
        of significant nonconformities."""
        for nc in entity_profile.get("nonconformities", []):
            if nc.get("significant") is True:
                assert nc.get("corrective_action_implemented") is True, (
                    f"No corrective action implemented for significant nonconformity "
                    f"'{nc.get('id', 'unknown')}' — ISO 22000:2018 §10.1.1(c)"
                )

    def test_corrective_action_records_retained(self, entity_profile: dict):
        """§10.1.2: Organization must retain documented information of NCs and corrective actions."""
        for nc in entity_profile.get("nonconformities", []):
            assert nc.get("records_retained") is True, (
                f"Records not retained for nonconformity '{nc.get('id', 'unknown')}' — "
                f"ISO 22000:2018 §10.1.2"
            )

    def test_corrective_action_effectiveness_evaluated(self, entity_profile: dict):
        """§10.1.1(e): Effectiveness of corrective actions must be evaluated."""
        for nc in entity_profile.get("nonconformities", []):
            if nc.get("corrective_action_implemented") is True:
                assert nc.get("effectiveness_evaluated") is True, (
                    f"Corrective action effectiveness not evaluated for "
                    f"'{nc.get('id', 'unknown')}' — ISO 22000:2018 §10.1.1(e)"
                )
```
