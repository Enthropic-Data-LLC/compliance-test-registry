# NRC 10 CFR 73.54 — Nuclear Power Reactor Cybersecurity

**Framework:** 10 CFR 73.54 (Cybersecurity Programs for Nuclear Power Reactors) + 10 CFR 73.77 (Cybersecurity Event Notifications); RG 5.71 (Cyber Security Programs for Nuclear Facilities — primary guidance)
**Clauses:** §73.54(b) (cybersecurity plan NRC approval), §73.54(c) (cybersecurity controls), §73.54(d) (defense-in-depth), §73.54(e) (annual assessment), §73.77 (incident reporting — 1-hour/8-hour/30-day); RG 5.71 §4.3.3 (Level 4 isolation requirements)
**Confidence:** DETERMINISTIC-dominant (Level 4 isolation, wireless prohibition, media control, incident reporting deadlines, annual assessment, plan approval); PARAMETERIZED (CDA identification methodology, security control adequacy)
**Last parsed:** 2026-05-21
**Applies to:** Commercial nuclear power reactor licensees holding operating licenses under 10 CFR Part 50 or combined licenses under 10 CFR Part 52; rule applies to all digital computer and communication systems and networks associated with safety, security, emergency preparedness, and support systems (Critical Digital Assets — CDAs)
**Trigger:** NRC license to operate a commercial nuclear power reactor in the United States; rule effective March 27, 2009; implementation schedules negotiated per licensee; ongoing compliance verified through NRC inspection procedure IP 71130.10
**Jurisdiction:** United States; enforced by the U.S. Nuclear Regulatory Commission (NRC) through routine inspections and enforcement actions
**Not applicable to:** Research and test reactors (different regulatory framework); nuclear fuel cycle facilities (10 CFR Part 74); nuclear materials licensees (Agreement State regulation in many cases); decommissioned reactors (modified applicability); non-power reactor licensees

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def nrc_10cfr73_scope(entity_profile: dict):
    if not entity_profile.get("nrc_nuclear_power_reactor_licensee", False):
        pytest.skip("10 CFR 73.54 not applicable — not an NRC nuclear power reactor licensee")
```

---

## Constants

```python
from datetime import date, timedelta

# 10 CFR 73.77 — incident reporting deadlines
NRC_INCIDENT_AFFECTING_REQUIRED_FUNCTIONS_HOURS = 1
NRC_INCIDENT_NOT_AFFECTING_REQUIRED_FUNCTIONS_HOURS = 8
NRC_INCIDENT_WRITTEN_REPORT_DAYS = 30

# Annual assessment interval
NRC_ANNUAL_ASSESSMENT_INTERVAL_MONTHS = 12

# Required elements in NRC-approved cybersecurity plan (§73.54(b) + RG 5.71)
NRC_CYBERSECURITY_PLAN_REQUIRED_ELEMENTS = frozenset({
    "program_scope_cda_identification_methodology",
    "cybersecurity_controls_mapped_to_rg571",
    "change_management_process",
    "supply_chain_cybersecurity",
    "incident_response_capability",
    "personnel_training_and_awareness",
    "configuration_management",
    "protective_strategy_defense_in_depth",
    "program_review_and_assessment_process",
    "reporting_to_nrc",
})

# 4 protected asset categories
NRC_PROTECTED_ASSET_CATEGORIES = frozenset({
    "safety_systems",                  # Reactor protection, ECCS, containment isolation
    "security_systems",                # Physical access control, intrusion detection
    "emergency_preparedness_systems",  # Emergency notification, dose assessment
    "support_systems",                 # Balance of plant systems that affect above
})
```

---

## Critical Digital Asset (CDA) Identification (§73.54(b) + RG 5.71 §4.1)

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestCDAIdentification:
    """§73.54(b) + RG 5.71 §4.1 — CDAs identified using documented consequence and attack vector analysis."""

    @pytest.mark.assumption(
        id="ASSUME-NRC-CDA-001",
        description=(
            "CDA identification requires consequence analysis (could failure affect "
            "safety, security, or emergency preparedness functions?) and attack vector "
            "analysis (could the system be exploited as a pathway to protected functions?); "
            "methodology must be NRC-approved; once the methodology is applied, specific "
            "systems IN or OUT is DETERMINISTIC; adequacy of methodology is PARAMETERIZED "
            "and subject to NRC inspection under IP 71130.10"
        ),
        approved_by="nuclear_cybersecurity_manager",
        review_date="2027-05-21",
    )
    def test_cda_identification_methodology_nrc_approved(
        self, controls_evidence: dict
    ):
        nrc = controls_evidence.get("nrc_10cfr73", {})
        assert nrc.get("cda_identification_methodology_nrc_approved", False), (
            "The CDA identification methodology must be included in the NRC-approved "
            "cybersecurity plan and applied consistently across all 4 protected "
            "asset categories (10 CFR 73.54(b) + RG 5.71 §4.1)"
        )

    def test_all_four_protected_categories_assessed_for_cdas(
        self, controls_evidence: dict
    ):
        nrc = controls_evidence.get("nrc_10cfr73", {})
        categories_assessed = set(nrc.get("protected_categories_assessed_for_cdas", []))
        missing = NRC_PROTECTED_ASSET_CATEGORIES - categories_assessed
        assert not missing, (
            f"CDA identification must cover all 4 protected asset categories. "
            f"Missing: {missing} (10 CFR 73.54(b) + RG 5.71)"
        )

    def test_cda_list_documented_and_current(self, controls_evidence: dict):
        nrc = controls_evidence.get("nrc_10cfr73", {})
        assert nrc.get("cda_list_documented_and_maintained_current", False), (
            "The list of identified CDAs must be documented and kept current — "
            "changes to plant digital systems must trigger a CDA re-assessment "
            "(10 CFR 73.54 + RG 5.71 §4.1)"
        )
```

---

## NRC-Approved Cybersecurity Plan (§73.54(b))

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestCybersecurityPlanApproval:
    """§73.54(b) — Cybersecurity plan submitted to and approved by NRC; all 10 required elements present."""

    def test_cybersecurity_plan_nrc_approved(self, controls_evidence: dict):
        nrc = controls_evidence.get("nrc_10cfr73", {})
        assert nrc.get("cybersecurity_plan_nrc_approved", False), (
            "The licensee's cybersecurity plan must be submitted to the NRC and "
            "receive NRC approval before full implementation "
            "(10 CFR 73.54(b))"
        )

    def test_cybersecurity_plan_contains_all_required_elements(
        self, controls_evidence: dict
    ):
        nrc = controls_evidence.get("nrc_10cfr73", {})
        present = set(nrc.get("cybersecurity_plan_elements_present", []))
        missing = NRC_CYBERSECURITY_PLAN_REQUIRED_ELEMENTS - present
        assert not missing, (
            f"NRC-approved cybersecurity plan is missing required elements: "
            f"{missing} (10 CFR 73.54(b) + RG 5.71)"
        )

    def test_cybersecurity_plan_updated_for_significant_changes(
        self, controls_evidence: dict
    ):
        nrc = controls_evidence.get("nrc_10cfr73", {})
        assert nrc.get("plan_update_process_for_significant_changes_documented", False), (
            "A process must exist to evaluate proposed plant changes for impact on "
            "the cybersecurity program and update the plan accordingly "
            "(10 CFR 73.54 + RG 5.71 change management)"
        )
```

---

## Level 4 Defense-in-Depth Isolation (§73.54(d) + RG 5.71 §4.3.3)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestLevel4Isolation:
    """RG 5.71 §4.3.3 — Level 4 CDAs (safety systems) have no direct connections to lower security levels; data diodes only; no wireless."""

    def test_no_direct_connections_from_level_4_to_lower_levels(
        self, controls_evidence: dict
    ):
        nrc = controls_evidence.get("nrc_10cfr73", {})
        assert not nrc.get("direct_connections_exist_from_level4_to_lower", False), (
            "No direct connections from Level 4 (highest security — reactor protection, "
            "ECCS, containment isolation) to Level 3 or lower are permitted. "
            "Any data flow from Level 4 must use a one-way data diode "
            "(10 CFR 73.54 + RG 5.71 §4.3.3)"
        )

    def test_data_flows_from_level_4_use_one_way_data_diodes(
        self, controls_evidence: dict
    ):
        nrc = controls_evidence.get("nrc_10cfr73", {})
        if not nrc.get("level4_outbound_data_flows_exist", False):
            return
        assert nrc.get("level4_outbound_flows_use_data_diodes_only", False), (
            "Any outbound data flows from Level 4 CDAs must use hardware-enforced "
            "one-way data diodes — bidirectional network connections are prohibited "
            "(RG 5.71 §4.3.3)"
        )

    def test_no_wireless_connections_to_level_4_cdas(self, controls_evidence: dict):
        nrc = controls_evidence.get("nrc_10cfr73", {})
        assert not nrc.get("wireless_connections_to_level4_exist", False), (
            "Wireless connections to Level 4 CDAs (safety systems) are absolutely "
            "prohibited — this includes WiFi, Bluetooth, and cellular "
            "(10 CFR 73.54 + RG 5.71 §4.3.3)"
        )

    def test_level_4_cdas_physically_protected(self, controls_evidence: dict):
        nrc = controls_evidence.get("nrc_10cfr73", {})
        assert nrc.get("level4_cda_physical_access_controlled", False), (
            "Physical access to Level 4 CDA systems and their network connections "
            "must be controlled and logged (RG 5.71 §4.3.3 + PE-3)"
        )
```

---

## Portable Media Control (RG 5.71 §4.3.3)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestPortableMediaControl:
    """RG 5.71 §4.3.3 — No uncontrolled portable media introduction to Level 4 CDAs; controlled process required."""

    def test_portable_media_control_process_documented(self, controls_evidence: dict):
        nrc = controls_evidence.get("nrc_10cfr73", {})
        assert nrc.get("portable_media_control_process_documented", False), (
            "A documented portable media control process must exist for any media "
            "(USB drives, laptops, maintenance tools) introduced to CDA environments "
            "(RG 5.71 §4.3.3)"
        )

    def test_portable_media_scanned_and_authorized_before_cda_connection(
        self, controls_evidence: dict
    ):
        media_events = controls_evidence.get("nrc_portable_media_events", [])
        not_scanned = [
            e for e in media_events
            if not e.get("scanned_and_authorized_before_connection", False)
        ]
        assert not not_scanned, (
            f"Portable media must be scanned for malware and formally authorized "
            f"before connection to any CDA (RG 5.71 §4.3.3). "
            f"Not scanned: {[e['event_id'] for e in not_scanned]}"
        )
```

---

## Incident Reporting (10 CFR 73.77)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestIncidentReporting:
    """10 CFR 73.77 — 1-hour notification (affecting required functions); 8-hour (not affecting); 30-day written report."""

    def test_incidents_affecting_required_functions_reported_within_1_hour(
        self, controls_evidence: dict
    ):
        incidents = controls_evidence.get("nrc_cybersecurity_events", [])
        affecting_required = [
            i for i in incidents
            if i.get("affects_required_functions", False)
        ]
        for incident in affecting_required:
            discovery_dt = incident.get("discovery_datetime")
            nrc_notify_dt = incident.get("nrc_operations_center_notify_datetime")
            if discovery_dt is None or nrc_notify_dt is None:
                continue
            hours = (nrc_notify_dt - discovery_dt).total_seconds() / 3600
            assert hours <= NRC_INCIDENT_AFFECTING_REQUIRED_FUNCTIONS_HOURS, (
                f"Cybersecurity event '{incident['event_id']}' affecting required "
                f"functions was reported in {hours:.2f} hours, exceeding the "
                f"{NRC_INCIDENT_AFFECTING_REQUIRED_FUNCTIONS_HOURS}-hour limit "
                f"(10 CFR 73.77). NRC Operations Center: 301-816-5100"
            )

    def test_incidents_not_affecting_required_functions_reported_within_8_hours(
        self, controls_evidence: dict
    ):
        incidents = controls_evidence.get("nrc_cybersecurity_events", [])
        not_affecting_required = [
            i for i in incidents
            if not i.get("affects_required_functions", False)
            and i.get("reportable_event", False)
        ]
        for incident in not_affecting_required:
            discovery_dt = incident.get("discovery_datetime")
            nrc_notify_dt = incident.get("nrc_operations_center_notify_datetime")
            if discovery_dt is None or nrc_notify_dt is None:
                continue
            hours = (nrc_notify_dt - discovery_dt).total_seconds() / 3600
            assert hours <= NRC_INCIDENT_NOT_AFFECTING_REQUIRED_FUNCTIONS_HOURS, (
                f"Cybersecurity event '{incident['event_id']}' not affecting required "
                f"functions was reported in {hours:.2f} hours, exceeding the "
                f"{NRC_INCIDENT_NOT_AFFECTING_REQUIRED_FUNCTIONS_HOURS}-hour limit "
                f"(10 CFR 73.77)"
            )

    def test_written_follow_up_report_submitted_within_30_days(
        self, controls_evidence: dict
    ):
        incidents = controls_evidence.get("nrc_cybersecurity_events", [])
        reportable = [i for i in incidents if i.get("reportable_event", False)]
        for incident in reportable:
            discovery_dt = incident.get("discovery_datetime")
            written_report_date = incident.get("nrc_written_report_date")
            if discovery_dt is None or written_report_date is None:
                continue
            days = (written_report_date - discovery_dt).days
            assert days <= NRC_INCIDENT_WRITTEN_REPORT_DAYS, (
                f"Written follow-up report for event '{incident['event_id']}' submitted "
                f"{days} days after discovery, exceeding the "
                f"{NRC_INCIDENT_WRITTEN_REPORT_DAYS}-day limit (10 CFR 73.77)"
            )
```

---

## Annual Program Assessment (§73.54(e))

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestAnnualProgramAssessment:
    """§73.54(e) — Annual cybersecurity program assessment conducted; results submitted to NRC resident inspector."""

    def test_annual_assessment_conducted(
        self, controls_evidence: dict, reference_date: date
    ):
        nrc = controls_evidence.get("nrc_10cfr73", {})
        last_assessment = nrc.get("annual_assessment_last_completed")
        assert last_assessment is not None, (
            "Annual cybersecurity program assessment has not been conducted — "
            "no completion date on record (10 CFR 73.54(e))"
        )
        cutoff = reference_date - timedelta(
            days=NRC_ANNUAL_ASSESSMENT_INTERVAL_MONTHS * 30
        )
        assert last_assessment >= cutoff, (
            f"Annual cybersecurity program assessment must be completed within the "
            f"past {NRC_ANNUAL_ASSESSMENT_INTERVAL_MONTHS} months. "
            f"Last completed: {last_assessment} (10 CFR 73.54(e))"
        )

    def test_annual_assessment_results_provided_to_nrc_resident_inspector(
        self, controls_evidence: dict
    ):
        nrc = controls_evidence.get("nrc_10cfr73", {})
        assert nrc.get("annual_assessment_results_provided_to_nrc", False), (
            "Annual cybersecurity program assessment results must be provided to "
            "the NRC resident inspector (10 CFR 73.54(e))"
        )
```

---

## Personnel Training (§73.54(c) + RG 5.71)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestPersonnelTraining:
    """§73.54(c) + RG 5.71 — Cybersecurity training for all personnel with CDA access; records retained."""

    def test_cybersecurity_training_program_for_cda_personnel_exists(
        self, controls_evidence: dict
    ):
        nrc = controls_evidence.get("nrc_10cfr73", {})
        assert nrc.get("cybersecurity_training_program_for_cda_personnel_exists", False), (
            "A cybersecurity training and awareness program must exist for all "
            "personnel with access to CDAs or the ability to affect CDA security "
            "(10 CFR 73.54(c) + RG 5.71)"
        )

    def test_all_cda_personnel_have_current_training_records(
        self, controls_evidence: dict
    ):
        personnel = controls_evidence.get("nrc_cda_personnel", [])
        no_training = [
            p for p in personnel
            if not p.get("cybersecurity_training_current", False)
        ]
        assert not no_training, (
            f"All personnel with CDA access must have current cybersecurity training "
            f"records (10 CFR 73.54(c) + RG 5.71). "
            f"Missing training: {[p['personnel_id'] for p in no_training]}"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-NRC-CDA-001 | §73.54(b) / RG 5.71 §4.1 | CDA identification methodology adequacy: PARAMETERIZED (NRC-reviewed); specific system CDA status once methodology applied: DETERMINISTIC | 2027-05-21 |
