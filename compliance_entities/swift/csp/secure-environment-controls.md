# SWIFT CSP — Secure Environment Controls (Objectives 1 & 2)

**Framework:** SWIFT Customer Security Programme (CSP) — CSCF v2025
**Controls:** 1.1, 1.2, 1.3, 2.1, 2.2, 2.3A, 2.5A, 2.7A
**Objective:** Restrict Internet Access + Segregate Critical Systems
**Confidence:** HIGH (1.1, 1.2, 2.1, 2.3A, 2.7A) / MEDIUM (1.3, 2.2, 2.5A)
**Last parsed:** 2026-05-21
**Applies to:** All SWIFT member institutions with a direct connection to the SWIFT network — banks, broker-dealers, fund managers, custodians, and other financial institutions using SWIFT for financial messaging; service bureaus providing SWIFT connectivity on behalf of member institutions
**Trigger:** SWIFT network connectivity (live connection) — all connected institutions must self-attest annually against the Customer Security Controls Framework (CSCF) mandatory controls; self-attestation is required in the KYC Registry; non-attestation results in escalation to counterparties and supervisors
**Jurisdiction:** Global — SWIFT is an international cooperative headquartered in Belgium; CSCF applies to all member institutions worldwide regardless of jurisdiction
**Not applicable to:** Correspondent banking relationships where a non-SWIFT institution accesses SWIFT only through a SWIFT-connected correspondent (the downstream institution must comply, not the non-SWIFT upstream); entities that have disconnected from SWIFT

---

## Scope pre-condition

These tests are enforcing only when the entity is a SWIFT user (has a BIC and connects
to the SWIFT network). All test classes apply this pre-condition via autouse fixture.

---

## Constants

```python
# Patch SLAs (Controls 1.2 and 2.3A)
SWIFT_CRITICAL_PATCH_DAYS = 90     # 3 months from release date
SWIFT_OTHER_PATCH_DAYS = 180       # 6 months from release date

# Vulnerability scanning cadence (Control 2.7A)
SWIFT_VULN_SCAN_INTERVAL_DAYS = 90  # quarterly — must not exceed this gap
```

---

## Control 1.1 — SWIFT Environment Protection

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | SWIFT secure zone and the systems within it | DETERMINISTIC |
| Condition | Organization connects to SWIFT network | DETERMINISTIC |
| Obligation | Secure zone isolated from general IT environment and internet; no direct internet routing to/from secure zone systems | DETERMINISTIC |
| Evidence | Network architecture diagram; firewall rule export showing no direct internet route; zone boundary enforcement | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
import pytest
from datetime import date

@pytest.fixture(autouse=True)
def swift_scope(entity_profile: dict):
    if not entity_profile.get("is_swift_user", False):
        pytest.skip("Entity is not a SWIFT user — CSCF not applicable")

class TestControl1_1:
    """1.1 — SWIFT Environment Protection: Secure Zone isolation."""

    def test_secure_zone_defined(self, controls_evidence: dict):
        zone = controls_evidence.get("swift_secure_zone", {})
        assert zone.get("defined", False), (
            "SWIFT secure zone must be formally defined with documented boundary"
        )

    def test_no_direct_internet_routing(self, controls_evidence: dict):
        zone = controls_evidence.get("swift_secure_zone", {})
        assert not zone.get("direct_internet_route", True), (
            "No direct internet routing to/from SWIFT secure zone systems permitted"
        )

    def test_secure_zone_isolated_from_general_it(self, controls_evidence: dict):
        zone = controls_evidence.get("swift_secure_zone", {})
        assert zone.get("isolated_from_general_it", False), (
            "SWIFT secure zone must be isolated from general IT environment via firewall"
        )

    def test_network_architecture_documented(self, controls_evidence: dict):
        docs = controls_evidence.get("network_architecture_docs", {})
        assert docs.get("swift_zone_diagram_current", False), (
            "Current network architecture diagram showing SWIFT zone boundary required"
        )
```

---

## Control 1.2 — Security Updates (SWIFT Infrastructure)

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | All systems within the SWIFT secure zone | DETERMINISTIC |
| Condition | Security update / patch released by vendor | DETERMINISTIC |
| Obligation | Critical patches applied within 3 months; other patches within 6 months | DETERMINISTIC |
| Evidence | Patch status report for all in-scope systems; release date vs. applied date | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestControl1_2:
    """1.2 — Security Updates: patch SLAs for SWIFT secure zone systems."""

    def test_no_overdue_critical_patches(self, controls_evidence: dict, reference_date: date):
        patches = controls_evidence.get("swift_zone_patch_status", [])
        overdue = [
            p for p in patches
            if p.get("severity") == "critical"
            and (reference_date - p["release_date"]).days > SWIFT_CRITICAL_PATCH_DAYS
            and not p.get("applied", False)
        ]
        assert not overdue, (
            f"Critical patches must be applied within {SWIFT_CRITICAL_PATCH_DAYS} days of release. "
            f"Overdue: {[p['patch_id'] for p in overdue]}"
        )

    def test_no_overdue_other_patches(self, controls_evidence: dict, reference_date: date):
        patches = controls_evidence.get("swift_zone_patch_status", [])
        overdue = [
            p for p in patches
            if p.get("severity") != "critical"
            and (reference_date - p["release_date"]).days > SWIFT_OTHER_PATCH_DAYS
            and not p.get("applied", False)
        ]
        assert not overdue, (
            f"Non-critical patches must be applied within {SWIFT_OTHER_PATCH_DAYS} days of release. "
            f"Overdue: {[p['patch_id'] for p in overdue]}"
        )

    def test_patch_inventory_covers_all_zone_systems(self, controls_evidence: dict):
        zone_systems = controls_evidence.get("swift_zone_systems", [])
        patched_systems = {
            p["system_id"]
            for p in controls_evidence.get("swift_zone_patch_status", [])
        }
        uncovered = [s for s in zone_systems if s not in patched_systems]
        assert not uncovered, (
            f"Patch tracking must cover all SWIFT zone systems. "
            f"Missing coverage: {uncovered}"
        )
```

---

## Control 1.3 — Virtualisation Platform Security

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Hypervisor and virtualisation platform hosting SWIFT secure zone | DETERMINISTIC |
| Condition | Secure zone hosted on virtualised infrastructure | DETERMINISTIC |
| Obligation | Hypervisor hardened per vendor security guidelines; configuration documented | PARAMETERIZED |
| Evidence | Hardening benchmark applied; configuration baseline documented; deviations justified | PARAMETERIZED |

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestControl1_3:
    """1.3 — Virtualisation Platform Security: hypervisor hardening."""

    @pytest.mark.assumption(
        id="ASSUME-SWIFT-1_3-001",
        description=(
            "Acceptable hardening benchmark for SWIFT zone hypervisor: vendor security guide "
            "or CIS Benchmark for the relevant hypervisor platform; deviations documented with "
            "compensating control justification"
        ),
        approved_by="ISSO",
        review_date="2027-05-21",
    )
    def test_hypervisor_hardening_applied(self, controls_evidence: dict, odp_values: dict):
        if not odp_values.get("swift_virtualisation_in_scope"):
            pytest.skip("Virtualisation not in SWIFT zone scope")
        virt = controls_evidence.get("swift_virtualisation", {})
        assert virt.get("hardening_benchmark_applied"), (
            "Hypervisor must be hardened per documented vendor or CIS benchmark"
        )
        assert virt.get("hardening_benchmark_name"), (
            "Hardening benchmark name must be recorded"
        )
```

---

## Control 2.1 — Operator PC Security

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | PCs used to operate SWIFT messaging interface | DETERMINISTIC |
| Condition | Organization uses operator PCs to access SWIFT | DETERMINISTIC |
| Obligation | Dedicated operator PCs for SWIFT use; general internet browsing prohibited; OS hardened | DETERMINISTIC |
| Evidence | PC inventory with SWIFT-operator designation; internet browsing restriction evidence (proxy/firewall block); hardening baseline | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestControl2_1:
    """2.1 — Operator PC Security: dedicated and hardened SWIFT operator workstations."""

    def test_dedicated_operator_pcs_exist(self, controls_evidence: dict):
        pcs = controls_evidence.get("swift_operator_pcs", [])
        assert pcs, "SWIFT operator PC inventory must be non-empty"

    def test_operator_pcs_dedicated(self, controls_evidence: dict):
        pcs = controls_evidence.get("swift_operator_pcs", [])
        non_dedicated = [pc for pc in pcs if not pc.get("dedicated_swift_only", False)]
        assert not non_dedicated, (
            f"All SWIFT operator PCs must be dedicated to SWIFT use only. "
            f"Non-dedicated: {[pc['pc_id'] for pc in non_dedicated]}"
        )

    def test_internet_browsing_restricted_on_operator_pcs(self, controls_evidence: dict):
        pcs = controls_evidence.get("swift_operator_pcs", [])
        unrestricted = [
            pc for pc in pcs if not pc.get("internet_browsing_blocked", False)
        ]
        assert not unrestricted, (
            f"General internet browsing must be blocked on SWIFT operator PCs. "
            f"Unrestricted: {[pc['pc_id'] for pc in unrestricted]}"
        )

    def test_operator_pcs_hardened(self, controls_evidence: dict):
        pcs = controls_evidence.get("swift_operator_pcs", [])
        unhardened = [pc for pc in pcs if not pc.get("hardening_applied", False)]
        assert not unhardened, (
            f"SWIFT operator PCs must have OS hardening applied. "
            f"Unhardened: {[pc['pc_id'] for pc in unhardened]}"
        )
```

---

## Control 2.2 — Internal Data Flow Security

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Network traffic between SWIFT secure zone and other internal zones | DETERMINISTIC |
| Condition | Data flows between zones exist | DETERMINISTIC |
| Obligation | Inbound/outbound flows between SWIFT secure zone and other zones filtered and documented | PARAMETERIZED |
| Evidence | Data flow diagram; firewall ruleset; documented allowed flows; deny-by-default posture | PARAMETERIZED |

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestControl2_2:
    """2.2 — Internal Data Flow Security: zone-to-zone traffic filtering."""

    @pytest.mark.assumption(
        id="ASSUME-SWIFT-2_2-001",
        description=(
            "Internal data flows between SWIFT secure zone and back-office / general IT zones "
            "are documented in a data flow diagram; firewall rules implement deny-by-default "
            "with explicit permit rules for each documented flow; rules reviewed annually"
        ),
        approved_by="network_security_team",
        review_date="2027-05-21",
    )
    def test_data_flow_diagram_current(self, controls_evidence: dict):
        dfd = controls_evidence.get("swift_data_flow_diagram", {})
        assert dfd.get("exists", False), (
            "Documented data flow diagram for SWIFT zone traffic required"
        )

    def test_deny_by_default_between_zones(self, controls_evidence: dict):
        fw = controls_evidence.get("swift_zone_firewall_config", {})
        assert fw.get("deny_by_default", False), (
            "SWIFT zone firewall must implement deny-by-default posture with explicit permits"
        )
```

---

## Control 2.3A — Security Updates (Operator PCs)

**Element extraction:**

Identical patch SLA obligation to Control 1.2, applied to SWIFT operator PCs.

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestControl2_3A:
    """2.3A — Security Updates (Operator PCs): same SLAs as 1.2, applied to operator PCs."""

    def test_no_overdue_critical_patches_operator_pcs(
        self, controls_evidence: dict, reference_date: date
    ):
        patches = controls_evidence.get("operator_pc_patch_status", [])
        overdue = [
            p for p in patches
            if p.get("severity") == "critical"
            and (reference_date - p["release_date"]).days > SWIFT_CRITICAL_PATCH_DAYS
            and not p.get("applied", False)
        ]
        assert not overdue, (
            f"Critical patches must be applied within {SWIFT_CRITICAL_PATCH_DAYS} days on "
            f"SWIFT operator PCs. Overdue: {[p['patch_id'] for p in overdue]}"
        )

    def test_no_overdue_other_patches_operator_pcs(
        self, controls_evidence: dict, reference_date: date
    ):
        patches = controls_evidence.get("operator_pc_patch_status", [])
        overdue = [
            p for p in patches
            if p.get("severity") != "critical"
            and (reference_date - p["release_date"]).days > SWIFT_OTHER_PATCH_DAYS
            and not p.get("applied", False)
        ]
        assert not overdue, (
            f"Non-critical patches must be applied within {SWIFT_OTHER_PATCH_DAYS} days on "
            f"SWIFT operator PCs. Overdue: {[p['patch_id'] for p in overdue]}"
        )
```

---

## Control 2.5A — Back-Office Data Flow Security

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Data flows between SWIFT messaging interface and back-office systems | DETERMINISTIC |
| Condition | Back-office systems (payment processors, core banking) connect to SWIFT zone | DETERMINISTIC |
| Obligation | All data flows from SWIFT zone to back-office enforced via firewall; no unauthorised channels | PARAMETERIZED |
| Evidence | Back-office flow documentation; firewall rules for each approved channel | PARAMETERIZED |

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestControl2_5A:
    """2.5A — Back-Office Data Flow Security: firewall-enforced SWIFT-to-back-office flows."""

    @pytest.mark.assumption(
        id="ASSUME-SWIFT-2_5A-001",
        description=(
            "All data flows between the SWIFT messaging zone and back-office systems "
            "(payment processors, core banking, treasury) are documented and enforced via "
            "firewall; each approved channel has an explicit firewall permit rule; "
            "undocumented flows are blocked by default"
        ),
        approved_by="network_security_team",
        review_date="2027-05-21",
    )
    def test_back_office_flows_documented(self, controls_evidence: dict):
        bo = controls_evidence.get("swift_back_office_flows", {})
        assert bo.get("documented", False), (
            "Back-office data flows to/from SWIFT zone must be documented"
        )

    def test_back_office_flows_firewall_enforced(self, controls_evidence: dict):
        bo = controls_evidence.get("swift_back_office_flows", {})
        assert bo.get("firewall_enforced", False), (
            "All back-office flows must be enforced via firewall with explicit permit rules"
        )
```

---

## Control 2.7A — Vulnerability Scanning

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | All systems within the SWIFT secure zone | DETERMINISTIC |
| Condition | Always (ongoing obligation) | DETERMINISTIC |
| Obligation | Internal vulnerability scanning performed at least quarterly | DETERMINISTIC |
| Evidence | Scan reports with timestamps showing ≤90-day cadence; all zone systems in scope | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestControl2_7A:
    """2.7A — Vulnerability Scanning: quarterly internal scans of SWIFT zone."""

    def test_vulnerability_scan_cadence(self, controls_evidence: dict, reference_date: date):
        last_scan = controls_evidence.get("swift_zone_last_vuln_scan_date")
        assert last_scan is not None, "Vulnerability scan date must be recorded"
        days_since = (reference_date - last_scan).days
        assert days_since <= SWIFT_VULN_SCAN_INTERVAL_DAYS, (
            f"SWIFT zone vulnerability scan must occur within {SWIFT_VULN_SCAN_INTERVAL_DAYS} days. "
            f"Days since last scan: {days_since}"
        )

    def test_vulnerability_scan_covers_all_zone_systems(self, controls_evidence: dict):
        zone_systems = set(controls_evidence.get("swift_zone_systems", []))
        scanned_systems = set(controls_evidence.get("swift_zone_last_scan_scope", []))
        unscanned = zone_systems - scanned_systems
        assert not unscanned, (
            f"All SWIFT zone systems must be in vulnerability scan scope. "
            f"Missing: {unscanned}"
        )
```

---

## Open assumptions

| ID | Control | Summary | Review date |
|---|---|---|---|
| ASSUME-SWIFT-1_3-001 | 1.3 | Acceptable hypervisor hardening benchmark: vendor guide or CIS Benchmark; deviations documented | 2027-05-21 |
| ASSUME-SWIFT-2_2-001 | 2.2 | Internal data flows documented in diagram; deny-by-default firewall posture; annual rule review | 2027-05-21 |
| ASSUME-SWIFT-2_5A-001 | 2.5A | Back-office flows documented; each channel has explicit firewall permit rule | 2027-05-21 |
