# TSA Pipeline Cybersecurity Directives — SD-02D / SD-01C

**Framework:** TSA Security Directive SD-02D (October 2023, performance-based) + SD-01C (incident reporting)
**Clauses:** SD-02D Goal 1 (identify and detect), Goal 2 (protect), Goal 3 (respond and recover), Goal 4 (cybersecurity governance); SD-01C (24-hour incident reporting to CISA + TSA)
**Confidence:** DETERMINISTIC-dominant (Cybersecurity Coordinator 24/7, CIP submitted + TSA-approved, OT/IT network segmentation enforced, MFA for remote OT access, annual plan testing, 24-hour incident reporting, annual assessment); PARAMETERIZED (architecture design adequacy, access control model, vulnerability remediation timelines)
**Last parsed:** 2026-05-21

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def tsa_pipeline_scope(entity_profile: dict):
    if not entity_profile.get("tsa_designated_critical_pipeline_operator", False):
        pytest.skip("TSA pipeline cybersecurity directives not applicable — not a TSA-designated critical pipeline operator")
```

---

## Constants

```python
from datetime import date, timedelta

# SD-01C — incident reporting deadline
TSA_PIPELINE_INCIDENT_REPORT_HOURS = 24

# SD-02D — annual plan testing interval
TSA_PIPELINE_PLAN_TEST_INTERVAL_MONTHS = 12

# Cybersecurity Implementation Plan (CIP) — required elements
TSA_PIPELINE_CIP_REQUIRED_ELEMENTS = frozenset({
    "current_ot_it_architecture_description",
    "how_goal_1_achieved",         # Identify and detect
    "how_goal_2_achieved",         # Protect
    "how_goal_3_achieved",         # Respond and recover
    "how_goal_4_achieved",         # Governance
    "gap_analysis_against_performance_goals",
    "remediation_timeline_for_gaps",
    "network_segmentation_documentation",
    "access_control_architecture",
    "testing_schedule",
})
```

---

## Cybersecurity Coordinator (SD-02D Goal 4)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestCybersecurityCoordinator:
    """SD-02D Goal 4 — Named Cybersecurity Coordinator designated; available 24/7; TSA-notified."""

    def test_cybersecurity_coordinator_designated(self, controls_evidence: dict):
        tsa = controls_evidence.get("tsa_pipeline", {})
        assert tsa.get("cybersecurity_coordinator_designated", False), (
            "A Cybersecurity Coordinator must be designated by the operator "
            "(TSA SD-02D Goal 4)"
        )

    def test_cybersecurity_coordinator_available_24_7(self, controls_evidence: dict):
        tsa = controls_evidence.get("tsa_pipeline", {})
        assert tsa.get("cybersecurity_coordinator_24_7_availability_documented", False), (
            "The Cybersecurity Coordinator must be available 24 hours a day, "
            "7 days a week to TSA and CISA (TSA SD-02D Goal 4)"
        )

    def test_cybersecurity_coordinator_contact_provided_to_tsa(
        self, controls_evidence: dict
    ):
        tsa = controls_evidence.get("tsa_pipeline", {})
        assert tsa.get("cybersecurity_coordinator_contact_provided_to_tsa", False), (
            "Cybersecurity Coordinator contact information must be provided to TSA "
            "and updated when the coordinator changes (TSA SD-02D Goal 4)"
        )
```

---

## Cybersecurity Implementation Plan (SD-02D Goal 4)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestCybersecurityImplementationPlan:
    """SD-02D Goal 4 — CIP submitted to TSA; approved; contains all required elements; updated as architecture changes."""

    def test_cybersecurity_implementation_plan_tsa_approved(
        self, controls_evidence: dict
    ):
        tsa = controls_evidence.get("tsa_pipeline", {})
        assert tsa.get("cip_submitted_and_tsa_approved", False), (
            "The Cybersecurity Implementation Plan (CIP) must be submitted to TSA "
            "and receive TSA approval before implementation (TSA SD-02D Goal 4)"
        )

    def test_cip_contains_all_required_elements(self, controls_evidence: dict):
        tsa = controls_evidence.get("tsa_pipeline", {})
        present = set(tsa.get("cip_elements_present", []))
        missing = TSA_PIPELINE_CIP_REQUIRED_ELEMENTS - present
        assert not missing, (
            f"Cybersecurity Implementation Plan is missing required elements: "
            f"{missing} (TSA SD-02D Goal 4)"
        )

    def test_cip_updated_when_architecture_or_risk_changes(
        self, controls_evidence: dict
    ):
        tsa = controls_evidence.get("tsa_pipeline", {})
        assert tsa.get("cip_update_process_documented", False), (
            "The CIP must be updated and resubmitted to TSA when significant "
            "changes occur to OT/IT architecture or threat landscape "
            "(TSA SD-02D Goal 4)"
        )
```

---

## OT/IT Network Segmentation (SD-02D Goal 2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestNetworkSegmentation:
    """SD-02D Goal 2 — OT networks segmented from IT networks; segmentation architecture documented and enforced."""

    def test_ot_it_network_segmentation_documented_and_enforced(
        self, controls_evidence: dict
    ):
        tsa = controls_evidence.get("tsa_pipeline", {})
        assert tsa.get("ot_it_network_segmentation_documented", False), (
            "OT pipeline control networks must be segmented from IT corporate "
            "networks; segmentation architecture must be documented "
            "(TSA SD-02D Goal 2)"
        )

    def test_no_direct_connections_between_ot_and_enterprise_networks(
        self, controls_evidence: dict
    ):
        tsa = controls_evidence.get("tsa_pipeline", {})
        assert not tsa.get("direct_ot_enterprise_connection_exists", False), (
            "No direct, unmediated connections between OT pipeline control systems "
            "and enterprise IT networks are permitted (TSA SD-02D Goal 2)"
        )

    def test_segmentation_controls_tested_for_effectiveness(
        self, controls_evidence: dict
    ):
        tsa = controls_evidence.get("tsa_pipeline", {})
        assert tsa.get("segmentation_controls_tested", False), (
            "Network segmentation controls must be tested to verify effectiveness — "
            "e.g., penetration testing or firewall rule review "
            "(TSA SD-02D Goal 2)"
        )
```

---

## MFA for Remote OT Access (SD-02D Goal 2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestRemoteAccessMFA:
    """SD-02D Goal 2 — MFA mandatory for all remote access to OT/ICS pipeline systems; no exceptions."""

    def test_mfa_required_for_all_remote_ot_access(self, controls_evidence: dict):
        tsa = controls_evidence.get("tsa_pipeline", {})
        assert tsa.get("mfa_enforced_for_ot_remote_access", False), (
            "Multi-factor authentication must be required for all remote access "
            "to OT/ICS pipeline systems — this is a mandatory SD-02D Goal 2 "
            "performance measure with no exceptions permitted"
        )

    def test_remote_ot_sessions_monitored_and_logged(self, controls_evidence: dict):
        tsa = controls_evidence.get("tsa_pipeline", {})
        assert tsa.get("remote_ot_sessions_monitored_and_logged", False), (
            "Remote access sessions to OT pipeline systems must be monitored and "
            "logged; logs retained to support incident investigation "
            "(TSA SD-02D Goal 2)"
        )
```

---

## Incident Response and Recovery Plans (SD-02D Goal 3)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestIncidentResponseAndRecoveryPlans:
    """SD-02D Goal 3 — Cybersecurity IRP and Recovery Plan documented; tested annually via tabletop or exercise."""

    def test_cybersecurity_incident_response_plan_exists(
        self, controls_evidence: dict
    ):
        tsa = controls_evidence.get("tsa_pipeline", {})
        assert tsa.get("cybersecurity_incident_response_plan_documented", False), (
            "A Cybersecurity Incident Response Plan (CIRP) must be documented "
            "and cover OT pipeline system scenarios (TSA SD-02D Goal 3)"
        )

    def test_cybersecurity_recovery_plan_exists(self, controls_evidence: dict):
        tsa = controls_evidence.get("tsa_pipeline", {})
        assert tsa.get("cybersecurity_recovery_plan_documented", False), (
            "A Cybersecurity Recovery Plan addressing restoration of OT pipeline "
            "systems after a cybersecurity incident must be documented "
            "(TSA SD-02D Goal 3)"
        )

    def test_irp_and_recovery_plan_tested_annually(
        self, controls_evidence: dict, reference_date: date
    ):
        tsa = controls_evidence.get("tsa_pipeline", {})
        last_test = tsa.get("irp_and_recovery_plan_last_tested")
        assert last_test is not None, (
            "Cybersecurity IRP and Recovery Plan must be tested; no test date recorded "
            "(TSA SD-02D Goal 3)"
        )
        cutoff = reference_date - timedelta(days=TSA_PIPELINE_PLAN_TEST_INTERVAL_MONTHS * 30)
        assert last_test >= cutoff, (
            f"Cybersecurity IRP and Recovery Plan must be tested at least annually "
            f"via tabletop exercise or full exercise. Last tested: {last_test} "
            f"(TSA SD-02D Goal 3)"
        )

    def test_unaffected_backup_capability_for_safe_operations(
        self, controls_evidence: dict
    ):
        tsa = controls_evidence.get("tsa_pipeline", {})
        assert tsa.get("backup_ot_capability_for_safe_operations_documented", False), (
            "A backup capability to maintain safe operational control in the event "
            "of OT system compromise must be documented "
            "(TSA SD-02D Goal 3)"
        )
```

---

## Incident Reporting (SD-01C)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestIncidentReporting:
    """SD-01C — Cybersecurity incidents reported to CISA and TSA within 24 hours of identification."""

    def test_incident_reporting_process_documented(self, controls_evidence: dict):
        tsa = controls_evidence.get("tsa_pipeline", {})
        assert tsa.get("incident_reporting_process_documented", False), (
            "A documented process for reporting cybersecurity incidents to CISA "
            "and TSA within 24 hours must exist (TSA SD-01C)"
        )

    def test_cybersecurity_incidents_reported_within_24_hours(
        self, controls_evidence: dict
    ):
        incidents = controls_evidence.get("tsa_pipeline_incidents", [])
        for incident in incidents:
            if not incident.get("reportable", False):
                continue
            identification_date = incident.get("identification_datetime")
            report_date = incident.get("cisa_tsa_report_datetime")
            if identification_date is None or report_date is None:
                continue
            hours = (report_date - identification_date).total_seconds() / 3600
            assert hours <= TSA_PIPELINE_INCIDENT_REPORT_HOURS, (
                f"Incident '{incident['incident_id']}' reported to CISA/TSA in "
                f"{hours:.1f} hours, exceeding the {TSA_PIPELINE_INCIDENT_REPORT_HOURS}-hour "
                f"deadline (TSA SD-01C)"
            )

    def test_cisa_contact_information_in_irp(self, controls_evidence: dict):
        tsa = controls_evidence.get("tsa_pipeline", {})
        assert tsa.get("cisa_reporting_contact_in_irp", False), (
            "CISA reporting contact information (CISA.gov/reporting, 888-282-0870) "
            "must be included in the Cybersecurity Incident Response Plan "
            "(TSA SD-01C)"
        )
```

---

## Annual Cybersecurity Assessment (SD-02D Goal 4)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestAnnualCybersecurityAssessment:
    """SD-02D Goal 4 — Annual cybersecurity assessment submitted to TSA; assesses performance against 4 goals."""

    def test_annual_cybersecurity_assessment_submitted_to_tsa(
        self, controls_evidence: dict, reference_date: date
    ):
        tsa = controls_evidence.get("tsa_pipeline", {})
        last_assessment = tsa.get("annual_assessment_last_submitted_to_tsa")
        assert last_assessment is not None, (
            "Annual cybersecurity assessment to TSA has not been submitted — "
            "no submission date on record (TSA SD-02D Goal 4)"
        )
        cutoff = reference_date - timedelta(days=TSA_PIPELINE_PLAN_TEST_INTERVAL_MONTHS * 30)
        assert last_assessment >= cutoff, (
            f"Annual cybersecurity assessment must be submitted to TSA within the "
            f"past {TSA_PIPELINE_PLAN_TEST_INTERVAL_MONTHS} months. "
            f"Last submitted: {last_assessment} (TSA SD-02D Goal 4)"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|

*(No open assumptions — SD-02D requirements are performance-based binaries: coordinator designated, CIP approved, segmentation enforced, MFA in place, plans tested, incidents reported on time, assessment submitted annually — all DETERMINISTIC)*
