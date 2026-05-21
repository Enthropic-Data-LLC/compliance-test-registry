# IEC 62443 — FR4 (Data Confidentiality), FR5 (Restricted Data Flow), FR6 (Timely Response), FR7 (Resource Availability)

**Framework:** IEC 62443-3-3:2013; 62443-2-1 (IACS Security Program); 62443-2-3 (Patch Management)
**Foundational Requirements:** FR 4 (DC), FR 5 (RDF), FR 6 (TRE), FR 7 (RA)
**System Requirements:** SR 4.1–4.3, SR 5.1–5.4, SR 6.1–6.2, SR 7.1–7.8
**Confidence:** DETERMINISTIC-dominant (zone architecture, backup, config baseline, inventory, patch policy)
**Last parsed:** 2026-05-21
**Applies to:** Three roles across the industrial automation and control system (IACS) lifecycle: asset owners (operators of OT/ICS systems), product suppliers (manufacturers of IACS components), and system integrators (designing/deploying IACS solutions) across all industrial sectors
**Trigger:** Customer/procurement contractual requirement (increasingly standard in oil and gas, energy, water, manufacturing supply chains); regulatory reference (NIS2 Directive in EU, NERC CIP, NRC guidance); voluntary adoption for OT security program maturity
**Jurisdiction:** Global — IEC international standard; widely referenced by EU NIS2 Directive implementing acts, US CISA advisories, and sector-specific regulators
**Not applicable to:** Pure IT environments (ISO 27001 is the counterpart); consumer IoT outside industrial automation context (ETSI EN 303 645 applies instead); IEC 62443 does not replace sector-specific regulations (NERC CIP for BES, NRC for nuclear, TSA for pipelines)

---

## Scope pre-condition

```python
@pytest.fixture(autouse=True)
def iec62443_scope(entity_profile: dict):
    if not entity_profile.get("iec62443_in_scope", False):
        pytest.skip("IEC 62443 not in scope")
```

---

## Constants

```python
# FR 4 — Data Confidentiality
IEC62443_ENCRYPTION_IN_TRANSIT_REQUIRED_AT_SL = 2   # SR 4.1 SL 2+
IEC62443_ENCRYPTION_AT_REST_REQUIRED_AT_SL = 3       # SR 4.1 SL 3+

# FR 7 — Resource Availability
IEC62443_CONTROL_SYSTEM_BACKUP_REQUIRED = True       # SR 7.3 — all SLs
IEC62443_BACKUP_TESTED = True                        # SR 7.3 — backup must be tested
IEC62443_LEAST_FUNCTIONALITY_REQUIRED = True         # SR 7.7 — disable unused ports/protocols
IEC62443_ASSET_INVENTORY_REQUIRED = True             # SR 7.8 — all SLs

# FR 5 — Network segmentation
IEC62443_ZONE_CONDUIT_ARCHITECTURE_REQUIRED = True   # SR 5.1 — all SLs
IEC62443_DEFAULT_DENY_FIREWALL_RULE = True           # SR 5.2 — all SLs
```

---

## FR 4 — Data Confidentiality

### SR 4.1 — Information Confidentiality

**Overall: DETERMINISTIC at SL 2+ — Pattern 1**

```python
import pytest
from datetime import date

class TestFR4_DataConfidentiality:
    """FR 4 — Data confidentiality: encryption in transit (SL 2+) and at rest (SL 3+)."""

    def test_data_encrypted_in_transit_at_sl2(self, controls_evidence: dict):
        zones = controls_evidence.get("iec62443_zones", [])
        sl2_zones = [z for z in zones if z.get("sl_target", 1) >= IEC62443_ENCRYPTION_IN_TRANSIT_REQUIRED_AT_SL]
        conduits_to_sl2 = [
            c for c in controls_evidence.get("iec62443_conduits", [])
            if c.get("connects_to_zone_sl", 1) >= IEC62443_ENCRYPTION_IN_TRANSIT_REQUIRED_AT_SL
        ]
        unencrypted_conduits = [
            c for c in conduits_to_sl2
            if not c.get("traffic_encrypted", False)
            and not c.get("unidirectional_gateway", False)
        ]
        assert not unencrypted_conduits, (
            f"Communications through conduits to SL 2+ zones must be encrypted "
            f"(IEC 62443 SR 4.1). Unencrypted: {[c['conduit_id'] for c in unencrypted_conduits]}"
        )

    def test_sensitive_data_encrypted_at_rest_at_sl3(self, controls_evidence: dict):
        zones = controls_evidence.get("iec62443_zones", [])
        sl3_zones = [z for z in zones if z.get("sl_target", 1) >= IEC62443_ENCRYPTION_AT_REST_REQUIRED_AT_SL]
        sl3_zone_ids = {z["zone_id"] for z in sl3_zones}
        systems_in_sl3 = [
            s for s in controls_evidence.get("iec62443_systems", [])
            if s.get("zone_id") in sl3_zone_ids
            and s.get("stores_sensitive_data", False)
        ]
        not_encrypted_at_rest = [
            s for s in systems_in_sl3
            if not s.get("data_at_rest_encrypted", False)
        ]
        assert not not_encrypted_at_rest, (
            f"Sensitive data at rest in SL 3+ zones must be encrypted (IEC 62443 SR 4.1). "
            f"Missing: {[s['system_id'] for s in not_encrypted_at_rest]}"
        )

    # SR 4.2 — Information Persistence (media sanitization)
    @pytest.mark.assumption(
        id="ASSUME-62443-FR4-001",
        description=(
            "IACS media (hard drives, USB, removable storage) containing sensitive data "
            "sanitized before reuse or disposal; sanitization method proportionate to data "
            "sensitivity and SL: SL 1-2 — overwrite; SL 3-4 — cryptographic erasure or "
            "physical destruction; sanitization records retained; method documented in "
            "media management procedure"
        ),
        approved_by="IACS_security_manager",
        review_date="2027-05-21",
    )
    def test_media_sanitization_procedure_exists(self, controls_evidence: dict):
        dc = controls_evidence.get("iec62443_data_confidentiality", {})
        assert dc.get("media_sanitization_procedure_exists", False), (
            "Media sanitization procedure must exist for IACS media reuse/disposal "
            "(IEC 62443 SR 4.2)"
        )
```

---

## FR 5 — Restricted Data Flow

### SR 5.1 — Network Segmentation / Zone Boundary Protection

**Overall: DETERMINISTIC — Pattern 1 (once zones defined)**

```python
class TestFR5_RestrictedDataFlow:
    """FR 5 — Restricted data flow: zone/conduit architecture, firewall boundary protection."""

    def test_firewall_at_every_zone_boundary(self, controls_evidence: dict):
        zones = controls_evidence.get("iec62443_zones", [])
        conduits = controls_evidence.get("iec62443_conduits", [])
        zone_ids_with_firewall = {
            c.get("protected_zone_id") for c in conduits
            if c.get("firewall_or_boundary_protection_in_place", False)
        }
        for zone in zones:
            assert zone["zone_id"] in zone_ids_with_firewall or zone.get("standalone_isolated_zone", False), (
                f"Zone '{zone['zone_id']}' must have firewall or boundary protection at "
                f"all conduits (IEC 62443 SR 5.1/5.2)"
            )

    def test_default_deny_rule_on_zone_firewalls(self, controls_evidence: dict):
        conduits = controls_evidence.get("iec62443_conduits", [])
        no_default_deny = [
            c for c in conduits
            if c.get("firewall_or_boundary_protection_in_place", False)
            and not c.get("default_deny_rule_configured", False)
        ]
        assert not no_default_deny, (
            f"Firewalls at zone boundaries must have default-deny rule — only explicitly "
            f"permitted traffic allowed (IEC 62443 SR 5.2). "
            f"Missing default deny: {[c['conduit_id'] for c in no_default_deny]}"
        )

    def test_dmz_between_iacs_and_enterprise_network(self, controls_evidence: dict):
        rdf = controls_evidence.get("iec62443_restricted_data_flow", {})
        if not rdf.get("enterprise_network_connectivity_exists", False):
            pytest.skip("No enterprise network connectivity — DMZ not applicable")
        assert rdf.get("dmz_between_iacs_and_enterprise", False), (
            "DMZ or equivalent isolation must exist between IACS network and enterprise "
            "network (IEC 62443 SR 5.1 — zone segmentation principle)"
        )

    @pytest.mark.assumption(
        id="ASSUME-62443-FR5-001",
        description=(
            "Firewall rule sets for each zone boundary are documented with: permit rules "
            "specifying source, destination, port, protocol; business justification for each "
            "permitted rule; rule owner; last review date; rule sets reviewed at minimum "
            "annually and after any architectural change; unused rules removed; any-any rules "
            "prohibited except in explicitly justified cases documented with risk acceptance"
        ),
        approved_by="IACS_security_manager",
        review_date="2027-05-21",
    )
    def test_firewall_ruleset_documented(self, controls_evidence: dict):
        conduits = controls_evidence.get("iec62443_conduits", [])
        firewalled = [c for c in conduits if c.get("firewall_or_boundary_protection_in_place", False)]
        no_ruleset = [c for c in firewalled if not c.get("firewall_ruleset_documented", False)]
        assert not no_ruleset, (
            f"Firewall ruleset must be documented for each zone boundary conduit "
            f"(IEC 62443 SR 5.2). Missing: {[c['conduit_id'] for c in no_ruleset]}"
        )
```

---

## FR 6 — Timely Response to Events

### SR 6.1 — Audit Log Accessibility; 62443-2-3 Patch Management

**Overall: DETERMINISTIC (log accessibility, patch policy)**

```python
class TestFR6_TimelyResponseToEvents:
    """FR 6 — Timely response: audit log accessibility; patch management policy."""

    def test_audit_logs_accessible_to_authorized_personnel(
        self, controls_evidence: dict
    ):
        tre = controls_evidence.get("iec62443_timely_response", {})
        assert tre.get("audit_logs_accessible", False), (
            "Audit logs must be accessible to authorized security personnel for review "
            "(IEC 62443 SR 6.1)"
        )

    @pytest.mark.assumption(
        id="ASSUME-62443-FR6-001",
        description=(
            "Continuous monitoring or periodic security monitoring defined for IACS: "
            "SL 2: periodic review of audit logs (minimum monthly); "
            "SL 3-4: continuous monitoring with alerting on anomalous events; "
            "monitoring scope covers: authentication failures, privilege escalation, "
            "unexpected network flows, configuration changes; "
            "security operations capability defined (internal SOC or managed service)"
        ),
        approved_by="IACS_security_manager",
        review_date="2027-05-21",
    )
    def test_security_monitoring_defined_at_sl2(self, controls_evidence: dict):
        zones = controls_evidence.get("iec62443_zones", [])
        sl2_zones = [z for z in zones if z.get("sl_target", 1) >= 2]
        if not sl2_zones:
            pytest.skip("No SL 2+ zones — continuous monitoring not required")
        tre = controls_evidence.get("iec62443_timely_response", {})
        assert tre.get("security_monitoring_defined", False), (
            "Security monitoring must be defined for SL 2+ zones (IEC 62443 SR 6.2)"
        )

    # 62443-2-3 — Patch Management
    def test_patch_management_policy_exists(self, controls_evidence: dict):
        pm = controls_evidence.get("iec62443_patch_management", {})
        assert pm.get("policy_exists", False), (
            "IACS patch management policy must exist (IEC 62443-2-3)"
        )

    def test_patch_applicability_assessed_before_deployment(
        self, controls_evidence: dict
    ):
        patches = controls_evidence.get("iec62443_patches", [])
        not_assessed = [
            p for p in patches
            if not p.get("applicability_assessed", False)
        ]
        assert not not_assessed, (
            f"Patch applicability to IACS must be assessed before deployment — "
            f"patches must be tested for operational impact (IEC 62443-2-3). "
            f"Not assessed: {[p['patch_id'] for p in not_assessed]}"
        )

    @pytest.mark.assumption(
        id="ASSUME-62443-FR6-002",
        description=(
            "Where critical patches cannot be applied due to operational constraints "
            "(production continuity, vendor qualification requirements, legacy OS): "
            "compensating controls documented and implemented including: network isolation, "
            "enhanced monitoring for exploit indicators, application whitelisting; "
            "deferred patch documented with: risk acceptance, compensating control description, "
            "timeline for patch application at next maintenance window; "
            "deferred patches reviewed at minimum quarterly"
        ),
        approved_by="IACS_security_manager",
        review_date="2027-05-21",
    )
    def test_deferred_patches_have_compensating_controls(
        self, controls_evidence: dict
    ):
        patches = controls_evidence.get("iec62443_patches", [])
        deferred = [
            p for p in patches
            if p.get("deployment_deferred", False)
        ]
        no_compensating = [
            p for p in deferred
            if not p.get("compensating_controls_documented", False)
        ]
        assert not no_compensating, (
            f"Deferred patches must have documented compensating controls and risk acceptance "
            f"(IEC 62443-2-3). Missing: {[p['patch_id'] for p in no_compensating]}"
        )
```

---

## FR 7 — Resource Availability

### SR 7.3 (Backup), SR 7.6 (Config Baseline), SR 7.7 (Least Functionality), SR 7.8 (Inventory)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestFR7_ResourceAvailability:
    """FR 7 — Resource availability: backup, config baseline, least functionality, inventory."""

    # SR 7.3 — Control System Backup
    def test_iacs_configuration_backup_exists(self, controls_evidence: dict):
        ra = controls_evidence.get("iec62443_resource_availability", {})
        assert ra.get("iacs_configuration_backup_exists", False), (
            "Backup of IACS configuration (PLCs, SCADA, DCS, safety systems) must exist "
            "(IEC 62443 SR 7.3)"
        )

    def test_iacs_backup_tested(self, controls_evidence: dict):
        ra = controls_evidence.get("iec62443_resource_availability", {})
        assert ra.get("backup_restore_tested", False), (
            "IACS configuration backup must be tested (restore test) to verify recoverability "
            "(IEC 62443 SR 7.3)"
        )

    def test_backup_stored_offline_or_isolated(self, controls_evidence: dict):
        ra = controls_evidence.get("iec62443_resource_availability", {})
        assert ra.get("backup_stored_offline_or_isolated", False), (
            "IACS backup must be stored offline or in an isolated location to prevent "
            "ransomware propagation (IEC 62443 SR 7.3 principle)"
        )

    # SR 7.5 — Emergency Power
    @pytest.mark.assumption(
        id="ASSUME-62443-FR7-001",
        description=(
            "Backup power (UPS, generator, or battery) exists for critical IACS components "
            "required for safe shutdown or continued operation during power outage; "
            "backup power capacity documented (runtime); tested at minimum annually; "
            "critical components identified by safety/operability assessment; "
            "UPS battery replacement schedule maintained"
        ),
        approved_by="IACS_security_manager",
        review_date="2027-05-21",
    )
    def test_emergency_power_for_critical_iacs_components(
        self, controls_evidence: dict
    ):
        ra = controls_evidence.get("iec62443_resource_availability", {})
        assert ra.get("emergency_power_for_critical_components", False), (
            "Backup power must exist for critical IACS components (IEC 62443 SR 7.5)"
        )

    # SR 7.6 — Network and Security Configuration Settings
    def test_security_configuration_baseline_documented(self, controls_evidence: dict):
        systems = controls_evidence.get("iec62443_systems", [])
        no_baseline = [
            s for s in systems
            if not s.get("security_configuration_baseline_documented", False)
        ]
        assert not no_baseline, (
            f"Security configuration baseline must be documented for each IACS component "
            f"(IEC 62443 SR 7.6). Missing: {[s['system_id'] for s in no_baseline]}"
        )

    def test_configuration_changes_controlled_against_baseline(
        self, controls_evidence: dict
    ):
        ra = controls_evidence.get("iec62443_resource_availability", {})
        assert ra.get("configuration_change_control_process_exists", False), (
            "Configuration changes to IACS must be controlled against documented baseline "
            "(IEC 62443 SR 7.6)"
        )

    # SR 7.7 — Least Functionality
    def test_unused_ports_protocols_services_disabled(self, controls_evidence: dict):
        systems = controls_evidence.get("iec62443_systems", [])
        not_hardened = [
            s for s in systems
            if not s.get("least_functionality_applied", False)
        ]
        assert not not_hardened, (
            f"Unused ports, protocols, and services must be disabled on IACS components "
            f"(IEC 62443 SR 7.7). Not hardened: {[s['system_id'] for s in not_hardened]}"
        )

    # SR 7.8 — Control System Component Inventory
    def test_iacs_component_inventory_maintained(self, controls_evidence: dict):
        ra = controls_evidence.get("iec62443_resource_availability", {})
        assert ra.get("component_inventory_exists", False), (
            "Inventory of all IACS components must be maintained (IEC 62443 SR 7.8)"
        )

    def test_component_inventory_includes_software_versions(
        self, controls_evidence: dict
    ):
        systems = controls_evidence.get("iec62443_systems", [])
        missing_version = [
            s for s in systems
            if not s.get("software_version_in_inventory", False)
        ]
        assert not missing_version, (
            f"Component inventory must include software/firmware versions for all IACS "
            f"components (IEC 62443 SR 7.8 — drives patch applicability). "
            f"Missing: {[s['system_id'] for s in missing_version]}"
        )
```

---

## Open assumptions

| ID | FR | Summary | Review date |
|---|---|---|---|
| ASSUME-62443-FR4-001 | FR 4 / SR 4.2 | Media sanitization by SL: overwrite (SL 1-2), crypto erasure/destruction (SL 3-4); records retained | 2027-05-21 |
| ASSUME-62443-FR5-001 | FR 5 / SR 5.2 | Firewall ruleset documented; business justification per rule; annual review; no any-any | 2027-05-21 |
| ASSUME-62443-FR6-001 | FR 6 / SR 6.2 | Security monitoring: monthly log review (SL 2), continuous alerting (SL 3-4) | 2027-05-21 |
| ASSUME-62443-FR6-002 | FR 6 / 62443-2-3 | Deferred patches: compensating controls + risk acceptance + quarterly review | 2027-05-21 |
| ASSUME-62443-FR7-001 | FR 7 / SR 7.5 | Emergency power: UPS/generator for critical IACS; capacity documented; annual test | 2027-05-21 |

---

## Cross-standard notes

**NERC CIP ↔ FR 7:** NERC CIP CIP-009 (Recovery Plans) maps to SR 7.3 (backup and recovery). CIP-010 (Configuration Change Management) maps to SR 7.6. CIP-007-6 R1 (ports/services) maps to SR 7.7. For electric utilities, NERC CIP satisfies these FRs for BES Cyber Systems; FR 7 coverage fills the gap for non-BES OT assets.

**NIST SP 800-82 ↔ IEC 62443:** NIST 800-82 Rev 3 (Guide to OT Security) is the US government equivalent reference. The zone/conduit architecture (FR 5) aligns with 800-82's ICS network architecture recommendations. Asset inventory (SR 7.8) maps to 800-53 CM-8. Backup (SR 7.3) maps to 800-53 CP-9.

**Patch management reality in OT:** Unlike IT (NIST 800-53 SI-2 recommends patching within 30 days), IEC 62443-2-3 acknowledges that OT patching windows may be annual (planned maintenance outages). The compensating control model (ASSUME-62443-FR6-002) is the primary mechanism for risk management during the patch deferral window — this is the operational pattern in practice.
