# NIST SP 800-82 r3 — OT/ICS Security Program

**Framework:** NIST SP 800-82 Revision 3 (September 2023) — Guide to Operational Technology Security
**Clauses:** §4 (OT security program); §5 (OT-specific tailoring of SP 800-53 controls); §6 (OT network architecture and zone model); AC-2/AC-17/CM-6/IR-6/PE-3/SI-2 (controls applied directly to OT); SC-7 (OT boundary protection)
**Note:** SP 800-82 is guidance, not a regulation. Tests apply when SP 800-82 is adopted by policy, mandated by contract, or referenced by a binding directive (TSA SD-02D, NRC RG 5.71, CISA). All requirements are PARAMETERIZED unless a binding mandate makes them DETERMINISTIC.
**Confidence:** PARAMETERIZED-dominant (program elements, tailoring adequacy); DETERMINISTIC subset (asset inventory existence, architecture documentation, remote access MFA, IRP existence)
**Last parsed:** 2026-05-21
**Applies to:** Any organization operating Operational Technology (OT), Industrial Control Systems (ICS), SCADA, DCS, PLC, or RTU systems that: (1) adopts SP 800-82 by organizational policy; (2) is subject to a binding directive referencing SP 800-82 (TSA SD-02D, NRC RG 5.71, CISA advisories); or (3) requires it by contract
**Trigger:** Policy adoption for OT security program; TSA Security Directive SD-02D (pipeline operators) references SP 800-82 practices; NRC RG 5.71 references NIST 800-53 (which SP 800-82 tailors for OT); federal/DoD contracts requiring NIST OT security standards; CISA critical infrastructure advisories
**Jurisdiction:** US origin; internationally referenced — ENISA, NCSC (UK), and national CERTs worldwide align OT guidance to SP 800-82 and IEC 62443
**Not applicable to:** As a standalone mandatory requirement — SP 800-82 is NIST guidance, not a regulation; it becomes effectively mandatory only when incorporated by reference into a binding regulatory directive or contract; does not replace NERC CIP (electric), TSA SD-02D (pipeline), or NRC 10 CFR 73.54 (nuclear)

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def sp800_82_scope(entity_profile: dict):
    if not entity_profile.get("nist_sp800_82_in_scope", False):
        pytest.skip("NIST SP 800-82 not in scope")
```

---

## Constants

```python
from datetime import date

# OT system types covered by SP 800-82
SP_800_82_OT_SYSTEM_TYPES = frozenset({
    "ics", "scada", "dcs", "plc", "rtu",
    "safety_instrumented_system_sis",
    "hmi", "engineering_workstation", "historian",
})

# Required OT security program elements
SP_800_82_REQUIRED_OT_PROGRAM_ELEMENTS = frozenset({
    "ot_asset_inventory",
    "ot_network_architecture_documentation",
    "ot_specific_incident_response_plan_or_annex",
    "ot_vulnerability_management_procedure",
    "ot_change_management_procedure",
    "ot_remote_access_policy",
    "ot_configuration_baseline_documentation",
    "ot_physical_access_controls",
})

# Purdue / zone model levels — SP 800-82 §6
OT_PURDUE_ZONES = frozenset({
    "enterprise_zone",          # Levels 4–5: business IT, ERP, internet
    "dmz_operations_zone",      # Level 3: historian, patch server, data aggregation
    "supervisory_zone",         # Level 2: SCADA/HMI, engineering stations
    "control_zone",             # Level 1: PLCs, DCS controllers
    "field_zone",               # Level 0: sensors, actuators
})
```

---

## OT Security Program Elements (SP 800-82 §4)

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestOTSecurityProgramElements:
    """SP 800-82 §4 — OT security program elements documented; scope addresses all applicable OT system types."""

    @pytest.mark.assumption(
        id="ASSUME-800-82-PROGRAM-001",
        description=(
            "SP 800-82 program element adequacy is organization-defined and context-dependent "
            "(sector, OT system criticality, legacy technology constraints); "
            "adequacy of each program element is PARAMETERIZED — "
            "existence of documented program elements is DETERMINISTIC when the "
            "standard is adopted or mandated"
        ),
        approved_by="ot_security_manager",
        review_date="2027-05-21",
    )
    def test_ot_security_program_elements_documented(self, controls_evidence: dict):
        ot = controls_evidence.get("nist_sp800_82", {})
        present = set(ot.get("program_elements_documented", []))
        missing = SP_800_82_REQUIRED_OT_PROGRAM_ELEMENTS - present
        assert not missing, (
            f"OT security program must document all required elements. Missing: {missing} "
            f"(NIST SP 800-82 r3 §4)"
        )

    def test_ot_asset_inventory_maintained_separately_from_it(
        self, controls_evidence: dict
    ):
        ot = controls_evidence.get("nist_sp800_82", {})
        assert ot.get("ot_asset_inventory_separate_from_it", False), (
            "OT asset inventory must be maintained separately from the IT asset "
            "inventory and include firmware versions, communication protocols, and "
            "vendor support status (NIST SP 800-82 r3 §4)"
        )

    def test_ot_asset_inventory_includes_firmware_versions(
        self, controls_evidence: dict
    ):
        ot = controls_evidence.get("nist_sp800_82", {})
        assert ot.get("ot_inventory_includes_firmware_versions", False), (
            "OT asset inventory must include firmware versions for all PLCs, DCS "
            "controllers, RTUs, and HMIs (NIST SP 800-82 r3 §4)"
        )
```

---

## OT Network Architecture and Zone Model (SP 800-82 §6)

**Overall: DETERMINISTIC (architecture documented) + PARAMETERIZED (design adequacy)**

```python
class TestOTNetworkArchitecture:
    """SP 800-82 §6 — Zone-based architecture documented; IT/OT separation enforced; data flows documented."""

    def test_ot_network_architecture_documented_with_zones(
        self, controls_evidence: dict
    ):
        ot = controls_evidence.get("nist_sp800_82", {})
        assert ot.get("ot_network_architecture_documented", False), (
            "OT network architecture must be documented, showing all zones, "
            "conduits, and data flows (NIST SP 800-82 r3 §6)"
        )

    def test_ot_it_network_separation_enforced(self, controls_evidence: dict):
        ot = controls_evidence.get("nist_sp800_82", {})
        assert ot.get("ot_it_network_separation_enforced", False), (
            "OT networks must be separated from IT networks; direct connections "
            "between enterprise zone and control zone are prohibited without "
            "compensating controls (NIST SP 800-82 r3 §6 / IEC 62443 zone model)"
        )

    def test_dmz_exists_between_ot_and_it_zones(self, controls_evidence: dict):
        ot = controls_evidence.get("nist_sp800_82", {})
        assert ot.get("dmz_operations_zone_exists", False), (
            "A demilitarized zone (DMZ / Operations Zone) must exist at Level 3 "
            "between the IT enterprise network and the OT supervisory/control zones "
            "to mediate data flows (NIST SP 800-82 r3 §6)"
        )

    def test_firewall_rules_at_zone_boundaries_documented(
        self, controls_evidence: dict
    ):
        ot = controls_evidence.get("nist_sp800_82", {})
        assert ot.get("zone_boundary_firewall_rules_documented", False), (
            "Firewall rule sets at each zone boundary must be documented and reviewed "
            "periodically; default-deny posture required (NIST SP 800-82 r3 §6 / SC-7)"
        )
```

---

## Remote Access to OT Systems (AC-17 OT Tailoring)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestOTRemoteAccess:
    """SP 800-82 r3 AC-17 tailoring — Remote access to OT requires documented authorization, MFA, and session monitoring."""

    def test_remote_access_to_ot_requires_formal_authorization(
        self, controls_evidence: dict
    ):
        ot = controls_evidence.get("nist_sp800_82", {})
        assert ot.get("ot_remote_access_requires_formal_authorization", False), (
            "Remote access to OT systems must require documented authorization "
            "per session or per role, with named approval authority "
            "(NIST SP 800-82 r3 / AC-17)"
        )

    def test_mfa_required_for_all_remote_ot_access(self, controls_evidence: dict):
        ot = controls_evidence.get("nist_sp800_82", {})
        assert ot.get("mfa_required_for_ot_remote_access", False), (
            "Multi-factor authentication (MFA) must be required for all remote "
            "access sessions to OT systems (NIST SP 800-82 r3 / AC-17)"
        )

    def test_remote_ot_sessions_are_monitored_and_logged(
        self, controls_evidence: dict
    ):
        ot = controls_evidence.get("nist_sp800_82", {})
        assert ot.get("remote_ot_sessions_monitored_and_logged", False), (
            "All remote access sessions to OT systems must be monitored and "
            "logged; logs retained for forensic purposes (NIST SP 800-82 r3 / AC-17)"
        )

    def test_vendor_remote_access_controlled_with_just_in_time_model(
        self, controls_evidence: dict
    ):
        ot = controls_evidence.get("nist_sp800_82", {})
        if not ot.get("vendor_remote_access_used", False):
            return
        assert ot.get("vendor_remote_access_just_in_time_or_equivalent", False), (
            "Vendor remote access to OT systems must use a just-in-time or "
            "time-limited model — persistent always-on vendor connections to "
            "OT are prohibited (NIST SP 800-82 r3 / AC-17)"
        )
```

---

## OT Change Management (CM-6 OT Tailoring)

**Overall: DETERMINISTIC (process exists) + PARAMETERIZED (safety impact assessment adequacy)**

```python
class TestOTChangeManagement:
    """SP 800-82 r3 CM-6 tailoring — OT changes tested before production; safety impact assessed; rollback plan required."""

    def test_ot_change_management_process_exists(self, controls_evidence: dict):
        ot = controls_evidence.get("nist_sp800_82", {})
        assert ot.get("ot_change_management_process_documented", False), (
            "A documented change management process specific to OT systems must "
            "exist, separate from or supplementing the IT change process "
            "(NIST SP 800-82 r3 / CM-6)"
        )

    def test_ot_changes_tested_before_production_deployment(
        self, controls_evidence: dict
    ):
        ot_changes = controls_evidence.get("sp800_82_ot_changes", [])
        not_tested = [
            c for c in ot_changes
            if not c.get("tested_in_test_environment_before_production", False)
        ]
        assert not not_tested, (
            f"OT changes must be tested in a representative test or staging "
            f"environment before production deployment "
            f"(NIST SP 800-82 r3 / CM-6). Not tested: "
            f"{[c['change_id'] for c in not_tested]}"
        )

    def test_safety_impact_assessed_for_ot_changes(self, controls_evidence: dict):
        ot_changes = controls_evidence.get("sp800_82_ot_changes", [])
        no_safety_impact = [
            c for c in ot_changes
            if not c.get("safety_impact_assessed", False)
        ]
        assert not no_safety_impact, (
            f"Safety impact must be assessed for all OT changes before "
            f"implementation (NIST SP 800-82 r3 — OT safety/availability priority). "
            f"Missing assessment: {[c['change_id'] for c in no_safety_impact]}"
        )
```

---

## OT Vulnerability Management (SI-2 OT Tailoring)

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestOTVulnerabilityManagement:
    """SP 800-82 r3 SI-2 tailoring — OT patches applied per vendor guidance; active scanning approach appropriate for OT device fragility."""

    @pytest.mark.assumption(
        id="ASSUME-800-82-PATCH-001",
        description=(
            "OT patch timelines are significantly longer than IT: patches must be "
            "tested by the OT vendor before deployment; emergency patching of OT "
            "may require process shutdown; patching during planned maintenance windows "
            "is acceptable; adequacy of patch timing is PARAMETERIZED — documented "
            "patch policy with risk-based timelines is DETERMINISTIC"
        ),
        approved_by="ot_security_manager",
        review_date="2027-05-21",
    )
    def test_ot_vulnerability_management_policy_documented(
        self, controls_evidence: dict
    ):
        ot = controls_evidence.get("nist_sp800_82", {})
        assert ot.get("ot_vulnerability_management_policy_documented", False), (
            "A vulnerability management policy specific to OT systems must exist, "
            "addressing patch scheduling per maintenance windows, vendor coordination, "
            "and compensating controls when patching is not feasible "
            "(NIST SP 800-82 r3 / SI-2)"
        )

    def test_ot_scanning_method_appropriate_for_device_fragility(
        self, controls_evidence: dict
    ):
        ot = controls_evidence.get("nist_sp800_82", {})
        assert ot.get("ot_scanning_uses_ot_safe_methods", False), (
            "Vulnerability scanning of OT devices must use passive monitoring or "
            "OT-safe scanning tools; active IT-style scanning can disrupt or crash "
            "PLCs and field devices (NIST SP 800-82 r3 / RA-5 OT tailoring)"
        )
```

---

## OT Incident Response Plan (IR-6 OT Tailoring)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestOTIncidentResponsePlan:
    """SP 800-82 r3 IR-6 — OT-specific IRP or annex exists; sector-specific reporting requirements included."""

    def test_ot_incident_response_plan_exists(self, controls_evidence: dict):
        ot = controls_evidence.get("nist_sp800_82", {})
        assert ot.get("ot_incident_response_plan_documented", False), (
            "An OT-specific incident response plan or OT annex to the corporate "
            "IRP must exist, with runbooks appropriate for OT environments "
            "(NIST SP 800-82 r3 / IR-6)"
        )

    def test_ot_irp_includes_sector_reporting_requirements(
        self, controls_evidence: dict
    ):
        ot = controls_evidence.get("nist_sp800_82", {})
        assert ot.get("ot_irp_includes_sector_reporting_requirements", False), (
            "OT IRP must include sector-specific reporting obligations "
            "(e.g., TSA SD-01C 24-hour, NRC 1-hour, CISA, NERC CIP-008) "
            "(NIST SP 800-82 r3 / IR-6)"
        )

    def test_ot_irp_addresses_safety_system_failure_scenarios(
        self, controls_evidence: dict
    ):
        ot = controls_evidence.get("nist_sp800_82", {})
        assert ot.get("ot_irp_includes_safety_system_failure_scenarios", False), (
            "OT IRP must include response procedures for scenarios where safety "
            "instrumented systems (SIS) or process safety functions are affected — "
            "safety actions take precedence over cybersecurity containment "
            "(NIST SP 800-82 r3 §4)"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-800-82-PROGRAM-001 | §4 | OT program element adequacy: PARAMETERIZED (sector/risk-dependent); documented program elements existence: DETERMINISTIC | 2027-05-21 |
| ASSUME-800-82-PATCH-001 | §5/SI-2 | OT patch timeline adequacy: PARAMETERIZED (vendor coordination, maintenance windows); documented patch policy existence: DETERMINISTIC | 2027-05-21 |
