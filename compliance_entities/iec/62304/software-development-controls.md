# IEC 62304:2006+AMD1:2015 — Software Development and Configuration Management

**Framework:** IEC 62304:2006+AMD1:2015
**Clauses:** 4 (General), 5 (Software Development), 8 (Configuration Management)
**Confidence:** DETERMINISTIC-dominant; class-gated (A/B/C determines required activities)
**Last parsed:** 2026-05-21

---

## Scope pre-condition

```python
def requires_iec62304(entity_profile: dict) -> bool:
    """
    True if organization develops software that is:
    - A medical device (SaMD), or
    - Embedded in or forms part of a medical device
    Required by EU MDR Annex I §17; recognized by FDA; required by ISO 13485 §7.3
    for software development activities.
    """
    return entity_profile.get("iec62304_in_scope", False)
```

---

## Constants

```python
# Software safety class (from ISO 14971 risk analysis — PARAMETERIZED assignment)
IEC62304_CLASS_A = "A"  # No injury possible
IEC62304_CLASS_B = "B"  # Non-serious injury possible
IEC62304_CLASS_C = "C"  # Death or serious injury possible

# Software development plan — 9 required elements (§5.1)
IEC62304_SDP_REQUIRED_ELEMENTS = frozenset({
    "development_lifecycle_model",
    "standards_methods_tools",
    "software_configuration_management_plan",
    "problem_resolution_plan",
    "hardware_software_integration_plan",
    "software_system_test_plan",
    "risk_management_activities",
    "regulatory_compliance_approach",
    "documentation_content_plan",
})

# SOUP (Software of Unknown Provenance) — must be identified and documented
IEC62304_SOUP_DOCUMENTATION_REQUIRED = True
```

---

## Clause 4 — General Requirements

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Software development organization | DETERMINISTIC |
| Condition | Software is medical device or part of medical device | DETERMINISTIC |
| Obligation | QMS in place (ISO 13485 satisfies); risk management per ISO 14971 throughout lifecycle; software safety classification documented | DETERMINISTIC |
| Evidence | QMS documentation reference; risk management file reference; safety class assignment document with rationale | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
import pytest
from datetime import date

@pytest.fixture(autouse=True)
def iec62304_scope(entity_profile: dict):
    if not entity_profile.get("iec62304_in_scope", False):
        pytest.skip("IEC 62304 not in scope")

class TestClause4_General:
    """Clause 4 — General requirements: QMS, risk management, safety classification."""

    def test_software_safety_class_documented(self, controls_evidence: dict):
        for sw in controls_evidence.get("iec62304_software_items", []):
            assert sw.get("safety_class") in (
                IEC62304_CLASS_A, IEC62304_CLASS_B, IEC62304_CLASS_C
            ), (
                f"Software item '{sw.get('software_id')}' must have documented safety class "
                f"A, B, or C based on ISO 14971 risk analysis (IEC 62304 §4.3)"
            )

    def test_safety_class_assignment_has_rationale(self, controls_evidence: dict):
        for sw in controls_evidence.get("iec62304_software_items", []):
            assert sw.get("safety_class_rationale_documented", False), (
                f"Safety class assignment for '{sw.get('software_id')}' must have documented "
                f"rationale linking to ISO 14971 risk analysis (IEC 62304 §4.3)"
            )

    def test_risk_management_integrated_in_development(self, controls_evidence: dict):
        general = controls_evidence.get("iec62304_general", {})
        assert general.get("risk_management_process_referenced", False), (
            "Risk management process per ISO 14971 must be integrated throughout the "
            "software development lifecycle (IEC 62304 §4.2)"
        )

    def test_soup_components_documented(self, controls_evidence: dict):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        for sw in sw_items:
            soup_components = sw.get("soup_components", [])
            undocumented_soup = [
                s for s in soup_components
                if not s.get("documented", False)
            ]
            assert not undocumented_soup, (
                f"All SOUP (Software of Unknown Provenance) components in '{sw.get('software_id')}' "
                f"must be documented including title, manufacturer, and version (IEC 62304 §8.1.2). "
                f"Undocumented: {[s.get('soup_id') for s in undocumented_soup]}"
            )
```

---

## Clause 5 — Software Development Process

### 5.1 — Software Development Plan

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Written software development plan (SDP) | DETERMINISTIC |
| Condition | All safety classes (A, B, C) | DETERMINISTIC |
| Obligation | SDP must exist and address all 9 required elements; updated as software development evolves | DETERMINISTIC |
| Evidence | SDP document with all 9 elements; version history | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause5_1_SoftwareDevelopmentPlan:
    """Clause 5.1 — Software development plan: required for all safety classes."""

    def test_software_development_plan_exists(self, controls_evidence: dict):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        no_sdp = [
            sw for sw in sw_items
            if not sw.get("software_development_plan_exists", False)
        ]
        assert not no_sdp, (
            f"Software development plan must exist for all medical device software. "
            f"Missing SDP: {[sw['software_id'] for sw in no_sdp]}"
        )

    def test_software_development_plan_addresses_required_elements(
        self, controls_evidence: dict
    ):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        for sw in sw_items:
            sdp_elements = set(sw.get("sdp_elements_present", []))
            missing_elements = IEC62304_SDP_REQUIRED_ELEMENTS - sdp_elements
            assert not missing_elements, (
                f"Software development plan for '{sw['software_id']}' is missing required "
                f"elements: {missing_elements} (IEC 62304 §5.1)"
            )
```

---

### 5.2 — Software Requirements Analysis

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Software requirements for medical device software | DETERMINISTIC |
| Condition | All safety classes (A, B, C) | DETERMINISTIC |
| Obligation | Requirements documented; include functional, performance, interface, safety, and security requirements; traced to system requirements | DETERMINISTIC |
| Evidence | Software requirements specification (SRS); traceability to system requirements; requirements review records | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause5_2_SoftwareRequirements:
    """Clause 5.2 — Software requirements analysis: documented and traceable."""

    def test_software_requirements_documented(self, controls_evidence: dict):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        no_srs = [
            sw for sw in sw_items
            if not sw.get("software_requirements_documented", False)
        ]
        assert not no_srs, (
            f"Software requirements must be documented for all medical device software. "
            f"Missing SRS: {[sw['software_id'] for sw in no_srs]}"
        )

    def test_software_requirements_include_safety_requirements(
        self, controls_evidence: dict
    ):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        class_b_c = [
            sw for sw in sw_items
            if sw.get("safety_class") in (IEC62304_CLASS_B, IEC62304_CLASS_C)
        ]
        missing_safety_reqs = [
            sw for sw in class_b_c
            if not sw.get("safety_requirements_in_srs", False)
        ]
        assert not missing_safety_reqs, (
            f"Software requirements must include safety-related requirements for Class B/C "
            f"software. Missing: {[sw['software_id'] for sw in missing_safety_reqs]}"
        )
```

---

### 5.3 — Software Architectural Design (Class B/C only)

**Overall: DETERMINISTIC for Class B/C — Pattern 1**

```python
class TestClause5_3_ArchitecturalDesign:
    """Clause 5.3 — Architectural design: required for Class B and C software."""

    def test_architectural_design_documented_for_class_b_c(
        self, controls_evidence: dict
    ):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        class_b_c = [
            sw for sw in sw_items
            if sw.get("safety_class") in (IEC62304_CLASS_B, IEC62304_CLASS_C)
        ]
        no_arch = [
            sw for sw in class_b_c
            if not sw.get("architectural_design_documented", False)
        ]
        assert not no_arch, (
            f"Architectural design must be documented for Class B/C software items. "
            f"Missing: {[sw['software_id'] for sw in no_arch]}"
        )

    def test_software_items_identified_in_architecture(self, controls_evidence: dict):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        class_b_c = [
            sw for sw in sw_items
            if sw.get("safety_class") in (IEC62304_CLASS_B, IEC62304_CLASS_C)
        ]
        no_item_decomp = [
            sw for sw in class_b_c
            if not sw.get("software_items_decomposed_in_architecture", False)
        ]
        assert not no_item_decomp, (
            f"Software items (components) must be identified in the architectural design "
            f"for Class B/C software (IEC 62304 §5.3). "
            f"Missing decomposition: {[sw['software_id'] for sw in no_item_decomp]}"
        )
```

---

### 5.5 — Software Unit Verification (Class B/C DETERMINISTIC; Class A waivable)

**Overall: DETERMINISTIC for B/C — Pattern 1**

```python
class TestClause5_5_UnitVerification:
    """Clause 5.5 — Unit verification: required for Class B/C; class A may skip with justification."""

    def test_unit_testing_performed_for_class_b_c(self, controls_evidence: dict):
        sw_units = controls_evidence.get("iec62304_software_units", [])
        class_b_c_units = [
            u for u in sw_units
            if u.get("safety_class") in (IEC62304_CLASS_B, IEC62304_CLASS_C)
        ]
        not_unit_tested = [
            u for u in class_b_c_units
            if not u.get("unit_testing_performed", False)
        ]
        assert not not_unit_tested, (
            f"Unit testing/verification is required for Class B and C software units "
            f"(IEC 62304 §5.5). Not tested: {[u['unit_id'] for u in not_unit_tested]}"
        )

    def test_class_a_unit_verification_decision_documented(
        self, controls_evidence: dict
    ):
        sw_units = controls_evidence.get("iec62304_software_units", [])
        class_a_units = [u for u in sw_units if u.get("safety_class") == IEC62304_CLASS_A]
        for unit in class_a_units:
            if not unit.get("unit_testing_performed", False):
                assert unit.get("no_unit_testing_justified", False), (
                    f"Class A unit '{unit['unit_id']}' skipping unit verification must "
                    f"have documented justification (IEC 62304 §5.5)"
                )
```

---

### 5.6 — Integration Testing (Class B/C)

```python
class TestClause5_6_IntegrationTesting:
    """Clause 5.6 — Integration testing: required for Class B/C."""

    def test_integration_testing_records_exist_for_class_b_c(
        self, controls_evidence: dict
    ):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        class_b_c = [
            sw for sw in sw_items
            if sw.get("safety_class") in (IEC62304_CLASS_B, IEC62304_CLASS_C)
        ]
        no_integration_records = [
            sw for sw in class_b_c
            if not sw.get("integration_testing_records_exist", False)
        ]
        assert not no_integration_records, (
            f"Integration testing records must exist for Class B/C software "
            f"(IEC 62304 §5.6). Missing: {[sw['software_id'] for sw in no_integration_records]}"
        )
```

---

### 5.7 — Software System Testing (All Classes)

```python
class TestClause5_7_SystemTesting:
    """Clause 5.7 — Software system testing: required for all safety classes."""

    def test_system_test_plan_exists(self, controls_evidence: dict):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        no_plan = [sw for sw in sw_items if not sw.get("system_test_plan_exists", False)]
        assert not no_plan, (
            f"Software system test plan must exist for all medical device software. "
            f"Missing: {[sw['software_id'] for sw in no_plan]}"
        )

    def test_system_test_records_retained(self, controls_evidence: dict):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        no_records = [
            sw for sw in sw_items
            if not sw.get("system_test_records_retained", False)
        ]
        assert not no_records, (
            f"Software system testing records must be retained (IEC 62304 §5.7). "
            f"Missing: {[sw['software_id'] for sw in no_records]}"
        )
```

---

### 5.8 — Software Release

```python
class TestClause5_8_SoftwareRelease:
    """Clause 5.8 — Software release: version under CM; release authorization documented."""

    def test_released_software_under_configuration_management(
        self, controls_evidence: dict
    ):
        releases = controls_evidence.get("iec62304_software_releases", [])
        not_under_cm = [r for r in releases if not r.get("under_configuration_management", False)]
        assert not not_under_cm, (
            f"All released software versions must be under configuration management. "
            f"Not under CM: {[r['release_id'] for r in not_under_cm]}"
        )

    def test_software_release_authorization_documented(self, controls_evidence: dict):
        releases = controls_evidence.get("iec62304_software_releases", [])
        no_auth = [r for r in releases if not r.get("release_authorization_documented", False)]
        assert not no_auth, (
            f"Software release must be authorized with documented authorization. "
            f"Missing: {[r['release_id'] for r in no_auth]}"
        )

    def test_accompanying_documents_released_with_software(
        self, controls_evidence: dict
    ):
        releases = controls_evidence.get("iec62304_software_releases", [])
        missing_docs = [
            r for r in releases
            if not r.get("accompanying_documents_included", False)
        ]
        assert not missing_docs, (
            f"Accompanying documents (instructions for use, maintenance info) must be "
            f"released with the software (IEC 62304 §5.8). "
            f"Missing: {[r['release_id'] for r in missing_docs]}"
        )
```

---

## Clause 8 — Software Configuration Management

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | All software items and deliverables | DETERMINISTIC |
| Condition | All safety classes (A, B, C) | DETERMINISTIC |
| Obligation | All software items uniquely identified and versioned; changes authorized before implementation; configuration baselines established before testing; status of all items tracked; SOUP documented | DETERMINISTIC |
| Evidence | Version control system records; change control records; configuration baselines; SOUP list | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause8_ConfigurationManagement:
    """Clause 8 — Configuration management: versioning, change control, SOUP inventory."""

    def test_all_software_items_uniquely_versioned(self, controls_evidence: dict):
        cm = controls_evidence.get("iec62304_configuration_management", {})
        assert cm.get("all_items_versioned", False), (
            "All software items must be uniquely identified and versioned "
            "(IEC 62304 §8.1)"
        )

    def test_configuration_baselines_established_before_testing(
        self, controls_evidence: dict
    ):
        cm = controls_evidence.get("iec62304_configuration_management", {})
        assert cm.get("baselines_established_before_testing", False), (
            "Configuration baselines must be established before software testing commences "
            "(IEC 62304 §8.2)"
        )

    def test_change_control_process_followed(self, controls_evidence: dict):
        changes = controls_evidence.get("iec62304_software_changes", [])
        unauthorized_changes = [
            c for c in changes
            if not c.get("change_authorized_before_implementation", False)
        ]
        assert not unauthorized_changes, (
            f"All software changes must be authorized before implementation (IEC 62304 §8.2). "
            f"Unauthorized: {[c['change_id'] for c in unauthorized_changes]}"
        )

    def test_configuration_status_tracked(self, controls_evidence: dict):
        cm = controls_evidence.get("iec62304_configuration_management", {})
        assert cm.get("configuration_status_tracked", False), (
            "Configuration status of all software items must be tracked (IEC 62304 §8.3)"
        )
```

---

## Traceability gate (bidirectional)

```python
class TestTraceability:
    """IEC 62304 bidirectional traceability requirement."""

    @pytest.mark.assumption(
        id="ASSUME-62304-TRACE-001",
        description=(
            "Bidirectional traceability matrix maintained from: software requirements → "
            "architectural design → detailed design (Class C) → software units → unit tests → "
            "integration tests → system tests; safety-related requirements additionally traced "
            "to risk controls → verification evidence in risk management file; traceability "
            "matrix updated when requirements change; completeness verified before software release"
        ),
        approved_by="software_quality_engineer",
        review_date="2027-05-21",
    )
    def test_traceability_matrix_exists(self, controls_evidence: dict):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        no_traceability = [
            sw for sw in sw_items
            if not sw.get("traceability_matrix_exists", False)
        ]
        assert not no_traceability, (
            f"Bidirectional traceability matrix must exist for medical device software. "
            f"Missing: {[sw['software_id'] for sw in no_traceability]}"
        )

    def test_traceability_matrix_complete(self, controls_evidence: dict):
        sw_items = controls_evidence.get("iec62304_software_items", [])
        incomplete = [
            sw for sw in sw_items
            if sw.get("traceability_matrix_exists", False)
            and not sw.get("traceability_matrix_complete", False)
        ]
        assert not incomplete, (
            f"Traceability matrix must be complete — all items traced in both directions. "
            f"Incomplete: {[sw['software_id'] for sw in incomplete]}"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-62304-TRACE-001 | Traceability | Bidirectional: requirements → design → units → tests → verification; safety reqs traced to risk controls | 2027-05-21 |
