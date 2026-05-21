# IEC 62304:2006+AMD1:2015 — Maintenance, Risk Management, and Problem Resolution

**Framework:** IEC 62304:2006+AMD1:2015
**Clauses:** 6 (Maintenance), 7 (Risk Management), 9 (Problem Resolution)
**Confidence:** DETERMINISTIC-dominant; Class B/C requirements distinguished from Class A
**Last parsed:** 2026-05-21
**Applies to:** Medical device manufacturers that incorporate software as part of a medical device (embedded, standalone Software as a Medical Device (SaMD), or software controlling a device); IVD manufacturers with software components
**Trigger:** Required by EU MDR/IVDR for software-containing devices; FDA's software-related guidance documents reference IEC 62304 as the recognized standard; ISO 13485 design controls (Clause 7.3) require a software development process for devices with software
**Jurisdiction:** Global — harmonized with EU MDR/IVDR, referenced by FDA, Health Canada, TGA, PMDA, and most major medical device regulatory frameworks
**Not applicable to:** Software with no medical purpose (wellness apps, administrative hospital software); off-the-shelf general-purpose software used in healthcare settings but not classified as a device; pure hardware medical devices with no software component

---

## Scope pre-condition

```python
@pytest.fixture(autouse=True)
def iec62304_scope(entity_profile: dict):
    if not entity_profile.get("iec62304_in_scope", False):
        pytest.skip("IEC 62304 not in scope")
```

---

## Constants

```python
from compliance_entities.iec._62304_constants import (
    IEC62304_CLASS_A, IEC62304_CLASS_B, IEC62304_CLASS_C,
)
```

---

## Clause 6 — Software Maintenance Process

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Changes to released medical device software | DETERMINISTIC |
| Condition | All safety classes (A, B, C) | DETERMINISTIC |
| Obligation | Software maintenance plan written; impact analysis performed for all modifications; safety impact determines whether re-classification required; modifications follow development process; regression testing performed | DETERMINISTIC |
| Evidence | Software maintenance plan; modification impact analysis records; regression test records; re-classification records where safety class changed | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
import pytest
from datetime import date

class TestClause6_Maintenance:
    """Clause 6 — Software maintenance process: plan, impact analysis, modification control."""

    def test_software_maintenance_plan_exists(self, controls_evidence: dict):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        released = [sw for sw in sw_items if sw.get("released", False)]
        no_maintenance_plan = [
            sw for sw in released
            if not sw.get("software_maintenance_plan_exists", False)
        ]
        assert not no_maintenance_plan, (
            f"Software maintenance plan must exist for all released medical device software "
            f"(IEC 62304 §6.1). Missing: {[sw['software_id'] for sw in no_maintenance_plan]}"
        )

    def test_modifications_have_impact_analysis(self, controls_evidence: dict):
        modifications = controls_evidence.get("iec62304_modifications", [])
        no_impact_analysis = [
            m for m in modifications
            if not m.get("impact_analysis_performed", False)
        ]
        assert not no_impact_analysis, (
            f"Impact analysis must be performed for all software modifications to released "
            f"software (IEC 62304 §6.2). "
            f"Missing: {[m['modification_id'] for m in no_impact_analysis]}"
        )

    def test_impact_analysis_includes_safety_impact(self, controls_evidence: dict):
        modifications = controls_evidence.get("iec62304_modifications", [])
        no_safety_assessment = [
            m for m in modifications
            if m.get("impact_analysis_performed", False)
            and not m.get("safety_impact_assessed", False)
        ]
        assert not no_safety_assessment, (
            f"Impact analysis must include assessment of whether modification affects "
            f"safety classification (IEC 62304 §6.2). "
            f"Missing safety assessment: {[m['modification_id'] for m in no_safety_assessment]}"
        )

    def test_safety_class_upgraded_when_modification_increases_risk(
        self, controls_evidence: dict
    ):
        modifications = controls_evidence.get("iec62304_modifications", [])
        requires_reclassification = [
            m for m in modifications
            if m.get("safety_impact_increases_risk", False)
            and not m.get("safety_class_reclassified", False)
        ]
        assert not requires_reclassification, (
            f"Safety class must be re-evaluated and upgraded when modification increases "
            f"risk (IEC 62304 §6.2). Not reclassified: "
            f"{[m['modification_id'] for m in requires_reclassification]}"
        )

    def test_modifications_follow_development_process(self, controls_evidence: dict):
        modifications = controls_evidence.get("iec62304_modifications", [])
        bypassed_process = [
            m for m in modifications
            if not m.get("development_process_followed", False)
        ]
        assert not bypassed_process, (
            f"Modifications to released software must follow the software development process "
            f"(IEC 62304 §6.3). Process bypassed: "
            f"{[m['modification_id'] for m in bypassed_process]}"
        )

    def test_regression_testing_performed_for_modifications(
        self, controls_evidence: dict
    ):
        modifications = controls_evidence.get("iec62304_modifications", [])
        no_regression = [
            m for m in modifications
            if not m.get("regression_testing_performed", False)
        ]
        assert not no_regression, (
            f"Regression testing must be performed after software modification "
            f"(IEC 62304 §6.3). Missing: {[m['modification_id'] for m in no_regression]}"
        )
```

---

## Clause 7 — Software Risk Management

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Software items that could contribute to hazardous situations | DETERMINISTIC |
| Condition | Class B and C software only (Class A has no risk contribution by definition) | DETERMINISTIC |
| Obligation | All software items that could contribute to hazards identified; risk control measures implemented in software; verification of risk controls performed and recorded; changes to existing software assessed for new hazards | DETERMINISTIC |
| Evidence | Software hazard identification records; risk control implementation records; risk control verification records; change impact on hazards documented | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1 (Class B/C)**

```python
class TestClause7_SoftwareRiskManagement:
    """Clause 7 — Software risk management: hazards, controls, verification (Class B/C)."""

    def test_software_items_contributing_to_hazards_identified(
        self, controls_evidence: dict
    ):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        class_b_c = [
            sw for sw in sw_items
            if sw.get("safety_class") in (IEC62304_CLASS_B, IEC62304_CLASS_C)
        ]
        no_hazard_identification = [
            sw for sw in class_b_c
            if not sw.get("hazard_contributing_items_identified", False)
        ]
        assert not no_hazard_identification, (
            f"Software items that could contribute to hazardous situations must be identified "
            f"for Class B/C software (IEC 62304 §7.1). "
            f"Missing: {[sw['software_id'] for sw in no_hazard_identification]}"
        )

    def test_risk_controls_implemented_in_software(self, controls_evidence: dict):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        class_b_c = [
            sw for sw in sw_items
            if sw.get("safety_class") in (IEC62304_CLASS_B, IEC62304_CLASS_C)
        ]
        no_risk_controls = [
            sw for sw in class_b_c
            if sw.get("has_software_risk_controls", True)
            and not sw.get("risk_controls_implemented", False)
        ]
        assert not no_risk_controls, (
            f"Risk control measures implemented in software must be documented for "
            f"Class B/C software (IEC 62304 §7.2). "
            f"Missing: {[sw['software_id'] for sw in no_risk_controls]}"
        )

    def test_risk_control_verification_evidence_in_risk_management_file(
        self, controls_evidence: dict
    ):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        class_b_c = [
            sw for sw in sw_items
            if sw.get("safety_class") in (IEC62304_CLASS_B, IEC62304_CLASS_C)
        ]
        no_verification = [
            sw for sw in class_b_c
            if sw.get("has_software_risk_controls", True)
            and not sw.get("risk_control_verification_in_risk_file", False)
        ]
        assert not no_verification, (
            f"Risk control verification evidence must be in the risk management file "
            f"(IEC 62304 §7.3). Missing: {[sw['software_id'] for sw in no_verification]}"
        )

    def test_changes_assessed_for_new_hazards(self, controls_evidence: dict):
        modifications = controls_evidence.get("iec62304_modifications", [])
        class_b_c_mods = [
            m for m in modifications
            if m.get("software_safety_class") in (IEC62304_CLASS_B, IEC62304_CLASS_C)
        ]
        no_hazard_assessment = [
            m for m in class_b_c_mods
            if not m.get("new_hazard_assessment_performed", False)
        ]
        assert not no_hazard_assessment, (
            f"Changes to Class B/C software must be assessed for introduction of new hazards "
            f"(IEC 62304 §7.4). Missing: {[m['modification_id'] for m in no_hazard_assessment]}"
        )
```

---

## Clause 9 — Software Problem Resolution Process

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Software problems (defects, failures, unexpected behaviors) in medical device software | DETERMINISTIC |
| Condition | All safety classes (A, B, C) | DETERMINISTIC |
| Obligation | All problems documented in problem reports; root cause analyzed; safety impact of problem determined; resolution follows change control; records retained; trends analyzed (B/C) | DETERMINISTIC |
| Evidence | Problem/defect tracking records; root cause analysis records; safety impact determination per problem; change records for each resolution | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause9_ProblemResolution:
    """Clause 9 — Problem resolution: all problems documented; root cause; safety impact; records."""

    def test_problem_reports_maintained(self, controls_evidence: dict):
        pr = controls_evidence.get("iec62304_problem_resolution", {})
        assert pr.get("problem_tracking_system_exists", False), (
            "Problem tracking system must exist; all software problems documented in "
            "problem reports (IEC 62304 §9.1)"
        )

    def test_all_problems_investigated(self, controls_evidence: dict):
        problem_reports = controls_evidence.get("iec62304_problem_reports", [])
        not_investigated = [
            p for p in problem_reports
            if not p.get("investigation_performed", False)
            and not p.get("deferred_with_justification", False)
        ]
        assert not not_investigated, (
            f"All software problem reports must be investigated (IEC 62304 §9.2). "
            f"Not investigated: {[p['pr_id'] for p in not_investigated]}"
        )

    def test_safety_impact_determined_per_problem(self, controls_evidence: dict):
        problem_reports = controls_evidence.get("iec62304_problem_reports", [])
        no_safety_determination = [
            p for p in problem_reports
            if not p.get("safety_impact_determined", False)
        ]
        assert not no_safety_determination, (
            f"Safety impact must be determined for each software problem report "
            f"(IEC 62304 §9.2). Missing: {[p['pr_id'] for p in no_safety_determination]}"
        )

    def test_problem_resolutions_follow_change_control(self, controls_evidence: dict):
        problem_reports = controls_evidence.get("iec62304_problem_reports", [])
        resolved = [p for p in problem_reports if p.get("resolved", False)]
        no_change_control = [
            p for p in resolved
            if not p.get("resolution_follows_change_control", False)
        ]
        assert not no_change_control, (
            f"Problem resolutions must use the change control process (IEC 62304 §9.4). "
            f"Bypassed: {[p['pr_id'] for p in no_change_control]}"
        )

    def test_problem_records_retained(self, controls_evidence: dict):
        pr = controls_evidence.get("iec62304_problem_resolution", {})
        assert pr.get("problem_records_retained", False), (
            "All problem reports and resolution records must be retained (IEC 62304 §9.5)"
        )

    def test_problem_trend_analysis_performed_for_class_b_c(
        self, controls_evidence: dict, entity_profile: dict
    ):
        has_class_b_c = any(
            sw.get("safety_class") in (IEC62304_CLASS_B, IEC62304_CLASS_C)
            for sw in controls_evidence.get("iec62304_software_items", [])
        )
        if not has_class_b_c:
            pytest.skip("No Class B or C software items in scope")
        pr = controls_evidence.get("iec62304_problem_resolution", {})
        assert pr.get("trend_analysis_performed", False), (
            "Trend analysis of software problems must be performed for Class B/C software "
            "to identify systemic issues (IEC 62304 §9.6)"
        )

    def test_problem_resolutions_verified_for_class_b_c(self, controls_evidence: dict):
        problem_reports = controls_evidence.get("iec62304_problem_reports", [])
        class_b_c_resolved = [
            p for p in problem_reports
            if p.get("resolved", False)
            and p.get("software_safety_class") in (IEC62304_CLASS_B, IEC62304_CLASS_C)
        ]
        not_verified = [
            p for p in class_b_c_resolved
            if not p.get("resolution_verified", False)
        ]
        assert not not_verified, (
            f"Software problem resolutions must be verified for Class B/C software "
            f"(IEC 62304 §9.7). Not verified: {[p['pr_id'] for p in not_verified]}"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| *(no additional assumptions — all requirements are DETERMINISTIC)* | | | |

---

## Cross-standard notes

**ISO 13485 §8.2.2 (complaint handling) ↔ IEC 62304 §9 (problem resolution):** Software problem reports involving deployed devices may constitute complaints under ISO 13485. The IEC 62304 problem tracking system should be configured to trigger the ISO 13485 complaint handling process when: (1) a software problem occurred in a distributed device, (2) caused or could have caused patient harm or device malfunction, or (3) is a reportable event under applicable regulations.

**ISO 14971 risk file ↔ IEC 62304 §7:** The IEC 62304 §7 risk control records are inputs to the ISO 14971 risk management file. The risk management file must reference the IEC 62304 §7 verification evidence for all software-implemented risk controls. A complete medical device software compliance package must demonstrate this bidirectional link.

**FDA QMSR / MDR post-market surveillance ↔ IEC 62304 §6+9:** Maintenance modifications and post-market problem resolutions that affect safety may require FDA 510(k)/PMA supplement or EU MDR vigilance reporting. The §6 impact analysis and §9 safety impact determination are the triggering mechanism for these regulatory obligations — ensure both are connected to the regulatory reporting pipeline.
