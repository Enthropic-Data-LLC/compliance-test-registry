# IPC-A-610 / J-STD-001 — Electronics Assembly Acceptability and Soldering

**Framework:** IPC-A-610 Rev H (2020) + J-STD-001 Rev H (2020) + IPC-7711/7721 (rework/repair)
**Clauses:** IPC-A-610 §10–15 (class-based acceptability by category); J-STD-001 §4–6 (solder process requirements)
**Confidence:** DETERMINISTIC-dominant (inspector certification currency, class-based pass/fail criteria, solder bridging defects, barrel fill percentages, operator certification)
**Last parsed:** 2026-05-21
**Applies to:** Electronics assembly manufacturers, contract electronics manufacturers (CEMs), and their inspection personnel for acceptability of electronic assemblies; customers specifying acceptance criteria for PCB assemblies
**Trigger:** Customer contract requirement — widely used as the default reference standard for electronics assembly quality; military and defense contracts citing IPC-A-610 as the acceptance standard; IPC Certified IPC Specialist (CIS) and CIS-I programs for inspection personnel
**Jurisdiction:** Global — IPC (Association Connecting Electronics Industries) standard; universally recognized in electronics manufacturing across North America, Europe, and Asia
**Not applicable to:** Bare PCB fabrication (IPC-6012 or IPC-A-600 applies instead); component-level manufacturing; non-electronic assembly manufacturing; RF/microwave assemblies (IPC-7711/7721 for rework)

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def ipc_scope(entity_profile: dict):
    if not entity_profile.get("ipc_a610_in_scope", False):
        pytest.skip("IPC-A-610 / J-STD-001 not in scope")
```

---

## Constants

```python
# Product class — customer-specified in PO or drawing
IPC_CLASS_1 = 1  # General electronics — consumer
IPC_CLASS_2 = 2  # Dedicated service — business, telecom
IPC_CLASS_3 = 3  # High reliability — aerospace, military, medical

# Through-hole solder — minimum barrel fill by class (IPC-A-610 §8.2.1)
IPC_TH_MIN_BARREL_FILL_CLASS_1 = 25   # percent
IPC_TH_MIN_BARREL_FILL_CLASS_2 = 75   # percent
IPC_TH_MIN_BARREL_FILL_CLASS_3 = 75   # percent

# Through-hole solder — minimum protrusion (clinch leads) by class
IPC_TH_MIN_PROTRUSION_MM_CLASS_1 = 0.5
IPC_TH_MIN_PROTRUSION_MM_CLASS_2 = 0.5
IPC_TH_MIN_PROTRUSION_MM_CLASS_3 = 1.5

# SMT chip component — minimum end-cap solder coverage by class (IPC-A-610 §8.3)
IPC_SMT_MIN_END_CAP_COVERAGE_CLASS_1 = 50   # percent of land width
IPC_SMT_MIN_END_CAP_COVERAGE_CLASS_2 = 75
IPC_SMT_MIN_END_CAP_COVERAGE_CLASS_3 = 75

# SMT — minimum side overhang coverage
IPC_SMT_MIN_SIDE_OVERHANG_CLASS_1 = 50   # percent
IPC_SMT_MIN_SIDE_OVERHANG_CLASS_2 = 50
IPC_SMT_MIN_SIDE_OVERHANG_CLASS_3 = 25

# Solder bridging — class treatment
IPC_BRIDGING_CLASS_2_IS_DEFECT = True
IPC_BRIDGING_CLASS_3_IS_DEFECT = True

# Inspector / operator certification renewal
IPC_CERTIFICATION_MAX_YEARS = 2  # CIS, CIT, J-STD-001 certification — biennial renewal

# Rotational misalignment threshold (degrees) — Class 2/3 defect
IPC_ROTATION_DEFECT_THRESHOLD_DEG = 15

# ESD-sensitive component handling — Classes 2/3
IPC_ESD_CONTROL_REQUIRED_CLASS = 2  # required for Class 2 and higher
```

---

## Product Class Scoping

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestIPCProductClass:
    """Product class must be customer-defined; all acceptance criteria applied to that class."""

    def test_product_class_specified_in_contract_or_drawing(
        self, controls_evidence: dict
    ):
        assemblies = controls_evidence.get("ipc_assemblies", [])
        no_class = [a for a in assemblies if a.get("product_class") is None]
        assert not no_class, (
            f"IPC product class (1, 2, or 3) must be customer-specified in the purchase "
            f"order or drawing for each assembly (IPC-A-610 §1.4). "
            f"Missing class: {[a['assembly_id'] for a in no_class]}"
        )
```

---

## Inspector and Operator Certifications

**Overall: DETERMINISTIC — Pattern 1**

```python
from datetime import date

class TestIPCCertifications:
    """IPC-A-610 CIS/CIT and J-STD-001 certifications must be current; max 2-year renewal."""

    def test_class_2_3_inspectors_hold_valid_ipc_a610_certification(
        self, controls_evidence: dict, reference_date: date
    ):
        inspectors = controls_evidence.get("ipc_inspectors", [])
        class_2_3_inspectors = [
            i for i in inspectors
            if i.get("inspects_class") in (IPC_CLASS_2, IPC_CLASS_3)
        ]
        for inspector in class_2_3_inspectors:
            cert_expiry = inspector.get("ipc_a610_cert_expiry")
            expired = cert_expiry is None or cert_expiry < reference_date
            assert not expired, (
                f"Inspector '{inspector['inspector_id']}' must hold a valid IPC-A-610 "
                f"CIS certification (max {IPC_CERTIFICATION_MAX_YEARS}-year renewal) to "
                f"inspect Class 2/3 assemblies (IPC-A-610 §1.8). "
                f"Expiry: {cert_expiry}"
            )

    def test_soldering_operators_certified_per_j_std_001(
        self, controls_evidence: dict, reference_date: date
    ):
        operators = controls_evidence.get("ipc_solder_operators", [])
        for operator in operators:
            cert_expiry = operator.get("jstd001_cert_expiry")
            expired = cert_expiry is None or cert_expiry < reference_date
            assert not expired, (
                f"Solder operator '{operator['operator_id']}' must hold a current "
                f"J-STD-001 certification (max {IPC_CERTIFICATION_MAX_YEARS}-year renewal). "
                f"Expiry: {cert_expiry} (J-STD-001 §4)"
            )
```

---

## Through-Hole Solder Acceptability (IPC-A-610 §8)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestThroughHoleSolder:
    """IPC-A-610 §8 — Barrel fill and protrusion by product class."""

    def test_through_hole_barrel_fill_meets_class_minimum(
        self, controls_evidence: dict
    ):
        th_joints = controls_evidence.get("ipc_through_hole_joints", [])
        for joint in th_joints:
            product_class = joint.get("product_class", IPC_CLASS_2)
            barrel_fill = joint.get("barrel_fill_percent")
            if barrel_fill is None:
                continue
            if product_class == IPC_CLASS_1:
                minimum = IPC_TH_MIN_BARREL_FILL_CLASS_1
            elif product_class == IPC_CLASS_2:
                minimum = IPC_TH_MIN_BARREL_FILL_CLASS_2
            else:
                minimum = IPC_TH_MIN_BARREL_FILL_CLASS_3

            assert barrel_fill >= minimum, (
                f"Through-hole joint '{joint['joint_id']}' barrel fill {barrel_fill}% "
                f"is below Class {product_class} minimum {minimum}% "
                f"(IPC-A-610 Rev H §8.2)"
            )

    def test_class_3_th_protrusion_meets_minimum(
        self, controls_evidence: dict
    ):
        th_joints = controls_evidence.get("ipc_through_hole_joints", [])
        class_3 = [j for j in th_joints if j.get("product_class") == IPC_CLASS_3]
        below_minimum = [
            j for j in class_3
            if j.get("protrusion_mm") is not None
            and j["protrusion_mm"] < IPC_TH_MIN_PROTRUSION_MM_CLASS_3
        ]
        assert not below_minimum, (
            f"Class 3 through-hole joints must have minimum lead protrusion of "
            f"{IPC_TH_MIN_PROTRUSION_MM_CLASS_3}mm (IPC-A-610 Rev H §8.2). "
            f"Below minimum: {[j['joint_id'] for j in below_minimum]}"
        )
```

---

## SMT Solder Acceptability (IPC-A-610 §8)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestSMTSolder:
    """IPC-A-610 §8 — SMT chip component end-cap coverage; solder bridging is defect for Class 2/3."""

    def test_smt_end_cap_coverage_meets_class_minimum(
        self, controls_evidence: dict
    ):
        smt_joints = controls_evidence.get("ipc_smt_joints", [])
        for joint in smt_joints:
            product_class = joint.get("product_class", IPC_CLASS_2)
            end_cap_coverage = joint.get("end_cap_coverage_percent")
            if end_cap_coverage is None:
                continue
            if product_class == IPC_CLASS_1:
                minimum = IPC_SMT_MIN_END_CAP_COVERAGE_CLASS_1
            else:
                minimum = IPC_SMT_MIN_END_CAP_COVERAGE_CLASS_2  # same for 2 and 3

            assert end_cap_coverage >= minimum, (
                f"SMT chip joint '{joint['joint_id']}' end-cap coverage "
                f"{end_cap_coverage}% is below Class {product_class} minimum {minimum}% "
                f"(IPC-A-610 Rev H §8.3)"
            )

    def test_solder_bridges_are_defects_for_class_2_and_3(
        self, controls_evidence: dict
    ):
        smt_joints = controls_evidence.get("ipc_smt_joints", [])
        bridged_class_2_3 = [
            j for j in smt_joints
            if j.get("solder_bridge_present", False)
            and j.get("product_class", IPC_CLASS_2) >= IPC_CLASS_2
        ]
        assert not bridged_class_2_3, (
            f"Solder bridges are defects for Class 2 and Class 3 assemblies and must "
            f"be reworked or rejected (IPC-A-610 Rev H §8). "
            f"Defective joints: {[j['joint_id'] for j in bridged_class_2_3]}"
        )
```

---

## Component Placement Defects (IPC-A-610 §9)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestComponentPlacement:
    """IPC-A-610 §9 — Missing components, rotation >15°, and lifted leads are class-dependent defects."""

    def test_no_missing_components(self, controls_evidence: dict):
        assemblies = controls_evidence.get("ipc_assemblies", [])
        missing_components = [
            a for a in assemblies
            if a.get("missing_component_present", False)
        ]
        assert not missing_components, (
            f"Missing components are a defect in all product classes "
            f"(IPC-A-610 Rev H §9). Assemblies with missing components: "
            f"{[a['assembly_id'] for a in missing_components]}"
        )

    def test_rotation_misalignment_within_class_limit(
        self, controls_evidence: dict
    ):
        placements = controls_evidence.get("ipc_component_placements", [])
        for placement in placements:
            product_class = placement.get("product_class", IPC_CLASS_2)
            rotation_deg = placement.get("rotation_misalignment_degrees")
            if rotation_deg is None:
                continue
            if product_class >= IPC_CLASS_2:
                assert rotation_deg <= IPC_ROTATION_DEFECT_THRESHOLD_DEG, (
                    f"Component '{placement['placement_id']}' rotational misalignment "
                    f"{rotation_deg}° exceeds Class {product_class} limit of "
                    f"{IPC_ROTATION_DEFECT_THRESHOLD_DEG}° (IPC-A-610 Rev H §9)"
                )

    def test_no_lifted_components_on_class_2_3(self, controls_evidence: dict):
        placements = controls_evidence.get("ipc_component_placements", [])
        lifted_class_2_3 = [
            p for p in placements
            if p.get("component_lifted", False)
            and p.get("product_class", IPC_CLASS_2) >= IPC_CLASS_2
        ]
        assert not lifted_class_2_3, (
            f"Lifted components (one end raised from pad) are defects for Class 2 and 3 "
            f"assemblies (IPC-A-610 Rev H §9). "
            f"Defective: {[p['placement_id'] for p in lifted_class_2_3]}"
        )
```

---

## J-STD-001 — Soldering Process Controls

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestJSTD001ProcessControls:
    """J-STD-001 — Solder alloy matches spec; flux classification matches process; ESD controls present."""

    def test_solder_alloy_matches_purchase_order_requirement(
        self, controls_evidence: dict
    ):
        assemblies = controls_evidence.get("ipc_assemblies", [])
        wrong_alloy = [
            a for a in assemblies
            if not a.get("solder_alloy_matches_requirement", False)
        ]
        assert not wrong_alloy, (
            f"Solder alloy used (lead-free or leaded as required) must match the "
            f"purchase order or drawing requirement (J-STD-001 Rev H §4). "
            f"Mismatched: {[a['assembly_id'] for a in wrong_alloy]}"
        )

    def test_flux_classification_matches_process_design(
        self, controls_evidence: dict
    ):
        assemblies = controls_evidence.get("ipc_assemblies", [])
        flux_mismatch = [
            a for a in assemblies
            if not a.get("flux_classification_matches_process", False)
        ]
        assert not flux_mismatch, (
            f"Flux classification (ROL0, ROL1, REL0, REL1, etc.) must be compatible "
            f"with the process design — no-clean flux used where cleaning is not "
            f"performed (J-STD-001 Rev H §5). Mismatch: "
            f"{[a['assembly_id'] for a in flux_mismatch]}"
        )

    def test_esd_controls_in_place_for_class_2_3(
        self, controls_evidence: dict, entity_profile: dict
    ):
        if entity_profile.get("ipc_max_product_class", IPC_CLASS_1) < IPC_ESD_CONTROL_REQUIRED_CLASS:
            return
        esd = controls_evidence.get("ipc_esd_controls", {})
        assert esd.get("esd_protected_workstation_in_use", False), (
            "ESD-protected workstations (wrist straps, grounded mats, EPA signage) "
            "must be in place for handling Class 2 and Class 3 assemblies "
            "(IPC-A-610 / ANSI/ESD S20.20)"
        )
        assert esd.get("esd_training_records_current", False), (
            "ESD awareness training records must be current for all personnel handling "
            "Class 2/3 assemblies (IPC-A-610 / ANSI/ESD S20.20)"
        )
```

---

## Rework and Repair (IPC-7711/7721)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestReworkAndRepair:
    """Rework and repair must follow IPC-7711/7721 approved procedures; unauthorized rework is a defect."""

    def test_rework_performed_per_ipc_7711_7721(self, controls_evidence: dict):
        rework_records = controls_evidence.get("ipc_rework_records", [])
        not_per_procedure = [
            r for r in rework_records
            if not r.get("performed_per_ipc_7711_7721_procedure", False)
        ]
        assert not not_per_procedure, (
            f"All rework and repair must be performed per approved IPC-7711/7721 "
            f"procedures. Unauthorized rework constitutes a defect "
            f"(IPC-A-610 Rev H / IPC-7711/7721). "
            f"Non-compliant: {[r['rework_id'] for r in not_per_procedure]}"
        )

    def test_rework_re_inspected_after_completion(self, controls_evidence: dict):
        rework_records = controls_evidence.get("ipc_rework_records", [])
        not_reinspected = [
            r for r in rework_records
            if not r.get("re_inspected_after_rework", False)
        ]
        assert not not_reinspected, (
            f"Assemblies must be re-inspected to the applicable class criteria after "
            f"rework is completed (IPC-A-610 Rev H). "
            f"Not re-inspected: {[r['rework_id'] for r in not_reinspected]}"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|

*(No open assumptions — IPC-A-610 acceptability criteria are class-based binary pass/fail — DETERMINISTIC throughout)*
