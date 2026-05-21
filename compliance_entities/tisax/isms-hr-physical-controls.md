# TISAX / VDA ISA 6.0 — ISMS, Human Resources & Physical Security

**Framework:** TISAX (Trusted Information Security Assessment Exchange) / VDA ISA 6.0
**Domains:** 1 (ISMS), 2 (Human Resources), 3 (Physical Security)
**Assessment Levels:** AL1 (self), AL2 (remote audit), AL3 (on-site)
**Confidence:** MEDIUM overall — maturity level scoring + some DETERMINISTIC gates
**Last parsed:** 2026-05-21

---

## Scope pre-condition

```python
def requires_tisax(entity_profile: dict) -> bool:
    """
    True if organization has contractual obligation from automotive OEM requiring
    TISAX label. Triggered by: receiving vehicle project data, handling prototypes,
    processing test/crash data, or pre-series technical information.
    """
    return entity_profile.get("tisax_contractual_obligation", False)

def assessment_level(entity_profile: dict) -> int:
    """
    1 = Normal (self-assessment); 2 = High (remote audit); 3 = Very High (on-site).
    Driven by data sensitivity classification defined by OEM customer.
    """
    return entity_profile.get("tisax_assessment_level", 2)
```

---

## Constants

```python
# VDA ISA maturity level minimums
TISAX_MIN_MATURITY_LEVEL_AL2 = 3        # most controls at AL2
TISAX_MIN_MATURITY_LEVEL_AL3_HIGH = 4   # selected high-risk controls at AL3

# Assessment validity
TISAX_LABEL_VALIDITY_YEARS = 3
TISAX_CAP_REQUIRED_BEFORE_LABEL = True  # corrective action plan for non-conformities

# Domain 2 — HR
TISAX_NDA_REQUIRED_FOR_PROJECT_ACCESS = True

# Domain 3 — Physical
TISAX_VISITOR_ESCORT_REQUIRED = True
```

---

## Domain 1 — Information Security Management System (ISMS)

### 1.1 — IS Management System

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Organization handling automotive project data under TISAX obligation | DETERMINISTIC |
| Condition | TISAX label required by OEM customer | DETERMINISTIC |
| Obligation | Formal ISMS scope document and IS policy defined; management commitment documented | PARAMETERIZED |
| Evidence | ISMS scope document; IS policy; management sign-off; internal audit records | PARAMETERIZED |

**Overall: PARAMETERIZED — Pattern 2**

```python
import pytest
from datetime import date

@pytest.fixture(autouse=True)
def tisax_scope(entity_profile: dict):
    if not entity_profile.get("tisax_contractual_obligation", False):
        pytest.skip("No TISAX contractual obligation — VDA ISA not applicable")

class TestDomain1_ISMS:
    """Domain 1 — ISMS: policies, risk management, audits, management review."""

    @pytest.mark.assumption(
        id="ASSUME-TISAX-1_1-001",
        description=(
            "ISMS scope document explicitly covers automotive project data (vehicle designs, "
            "technical specs, prototype data); IS policy addresses automotive information "
            "classification; management commitment evidenced by signed policy and resource "
            "allocation; reviewed annually"
        ),
        approved_by="CISO",
        review_date="2027-05-21",
    )
    def test_isms_scope_documented(self, controls_evidence: dict):
        isms = controls_evidence.get("tisax_isms", {})
        assert isms.get("scope_documented", False), (
            "ISMS scope document must exist and cover automotive project data"
        )

    def test_is_policy_exists(self, controls_evidence: dict):
        isms = controls_evidence.get("tisax_isms", {})
        assert isms.get("is_policy_exists", False), (
            "Information security policy must exist with management sign-off"
        )

    def test_isms_objectives_documented_and_measurable(self, controls_evidence: dict):
        isms = controls_evidence.get("tisax_isms", {})
        assert isms.get("objectives_measurable", False), (
            "IS objectives must be documented with measurable targets"
        )

    def test_internal_audit_planned_and_executed(self, controls_evidence: dict):
        isms = controls_evidence.get("tisax_isms", {})
        assert isms.get("internal_audit_records", False), (
            "Internal IS audit must be planned and records must exist"
        )

    def test_management_review_records_exist(self, controls_evidence: dict):
        isms = controls_evidence.get("tisax_isms", {})
        assert isms.get("management_review_records", False), (
            "Management review of ISMS must occur regularly with documented records"
        )

    # ── Risk management ───────────────────────────────────────────────────

    @pytest.mark.assumption(
        id="ASSUME-TISAX-1_1-002",
        description=(
            "Risk assessment methodology documented and applied to automotive project data; "
            "risk register maintained with automotive-specific threat scenarios; risk treatment "
            "decisions recorded with residual risk acceptance by management"
        ),
        approved_by="CISO",
        review_date="2027-05-21",
    )
    def test_risk_assessment_methodology_documented(self, controls_evidence: dict):
        risk = controls_evidence.get("tisax_risk_management", {})
        assert risk.get("methodology_documented", False), (
            "Risk assessment methodology must be documented and applied to automotive data"
        )

    def test_risk_register_exists(self, controls_evidence: dict):
        risk = controls_evidence.get("tisax_risk_management", {})
        assert risk.get("risk_register_current", False), (
            "Risk register must exist with current automotive information security risks"
        )

    def test_risk_treatment_decisions_recorded(self, controls_evidence: dict):
        risk = controls_evidence.get("tisax_risk_management", {})
        assert risk.get("treatment_decisions_recorded", False), (
            "Risk treatment decisions must be documented with management acceptance"
        )
```

---

## Domain 2 — Human Resources

### 2.1 — Security Awareness and Training

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | All employees handling automotive project data | DETERMINISTIC |
| Condition | Upon hire and ongoing | DETERMINISTIC |
| Obligation | Security awareness training provided; role-specific training for data handlers; records maintained | PARAMETERIZED |
| Evidence | Training records with completion dates; role-based training content; curriculum review date | PARAMETERIZED |

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestDomain2_HR:
    """Domain 2 — Human Resources: training, NDAs, and screening."""

    @pytest.mark.assumption(
        id="ASSUME-TISAX-2_1-001",
        description=(
            "Security awareness training covers automotive data protection, TISAX obligations, "
            "prototype handling (if AL3), and incident reporting; new employees trained within "
            "30 days of hire; refresher training at minimum annually; records retained for "
            "duration of employment"
        ),
        approved_by="HR_security",
        review_date="2027-05-21",
    )
    def test_security_awareness_training_records_exist(self, controls_evidence: dict):
        training = controls_evidence.get("tisax_training_records", {})
        assert training.get("records_exist", False), (
            "Security awareness training records must exist for TISAX-relevant personnel"
        )

    def test_all_project_data_handlers_trained(self, controls_evidence: dict):
        employees = controls_evidence.get("tisax_project_data_employees", [])
        untrained = [e for e in employees if not e.get("awareness_training_current", False)]
        assert not untrained, (
            f"All employees handling automotive project data must have current awareness training. "
            f"Untrained: {[e['employee_id'] for e in untrained]}"
        )

    # ── Non-disclosure agreements ─────────────────────────────────────────

    def test_ndas_in_place_for_project_data_access(self, controls_evidence: dict):
        employees = controls_evidence.get("tisax_project_data_employees", [])
        no_nda = [e for e in employees if not e.get("nda_signed", False)]
        assert not no_nda, (
            f"NDAs must be signed by all personnel with access to automotive project data. "
            f"Missing NDA: {[e['employee_id'] for e in no_nda]}"
        )

    # ── Screening ─────────────────────────────────────────────────────────

    @pytest.mark.assumption(
        id="ASSUME-TISAX-2_1-002",
        description=(
            "Background check process defined for roles with access to automotive project data; "
            "screening commensurate with data sensitivity (AL2: employment verification + "
            "criminal record; AL3: enhanced screening); completed before granting project access"
        ),
        approved_by="HR_security",
        review_date="2027-05-21",
    )
    def test_screening_process_documented(self, controls_evidence: dict):
        screening = controls_evidence.get("tisax_staff_screening", {})
        assert screening.get("process_documented", False), (
            "Background check / screening process for automotive data roles must be documented"
        )
```

---

## Domain 3 — Physical Security

### 3.1 — Secure Area Definition and Access Control

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Areas where automotive project data or prototypes are processed or stored | DETERMINISTIC |
| Condition | Automotive project data or prototype components present on premises | DETERMINISTIC |
| Obligation | Secure areas defined with clear physical boundary; access restricted to authorized personnel; access events logged | DETERMINISTIC |
| Evidence | Site security plan; access control system records; secure zone definition document | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestDomain3_Physical:
    """Domain 3 — Physical Security: secure areas, access control, visitor management."""

    def test_secure_areas_defined(self, controls_evidence: dict):
        physical = controls_evidence.get("tisax_physical_security", {})
        assert physical.get("secure_areas_defined", False), (
            "Secure areas for automotive project data must be formally defined with documented boundary"
        )

    def test_secure_area_access_restricted(self, controls_evidence: dict):
        physical = controls_evidence.get("tisax_physical_security", {})
        assert physical.get("access_restricted_to_authorized", False), (
            "Access to secure areas must be restricted to authorized personnel only"
        )

    def test_physical_access_events_logged(self, controls_evidence: dict):
        physical = controls_evidence.get("tisax_physical_security", {})
        assert physical.get("access_events_logged", False), (
            "All physical access events to secure areas must be logged"
        )

    # ── Visitor management ────────────────────────────────────────────────

    def test_visitor_management_procedure_exists(self, controls_evidence: dict):
        physical = controls_evidence.get("tisax_physical_security", {})
        assert physical.get("visitor_management_process", False), (
            "Visitor management procedure must exist for secure areas"
        )

    def test_visitors_escorted_in_secure_areas(self, controls_evidence: dict):
        physical = controls_evidence.get("tisax_physical_security", {})
        assert physical.get("visitors_escorted", False) == TISAX_VISITOR_ESCORT_REQUIRED, (
            "Visitors must be escorted within secure areas at all times"
        )

    def test_visitor_records_maintained(self, controls_evidence: dict):
        physical = controls_evidence.get("tisax_physical_security", {})
        assert physical.get("visitor_log_maintained", False), (
            "Visitor log must be maintained with purpose of visit and escort information"
        )

    # ── AL3 — Prototype protection measures ──────────────────────────────

    def test_prototype_protection_measures_at_al3(
        self, controls_evidence: dict, entity_profile: dict
    ):
        al = entity_profile.get("tisax_assessment_level", 2)
        if al < 3:
            pytest.skip("Prototype protection measures only required at AL3")
        proto = controls_evidence.get("tisax_prototype_protection", {})
        assert proto.get("procedures_documented", False), (
            "Written procedures for prototype identification, concealment, and handling "
            "required at AL3"
        )
        assert proto.get("photography_restrictions_documented", False), (
            "Photography and filming restrictions for prototype areas must be documented at AL3"
        )
```

---

## TISAX Assessment Validity Gate

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Organization holding TISAX label | DETERMINISTIC |
| Condition | TISAX label in use for customer contracts | DETERMINISTIC |
| Obligation | TISAX label must be current (within 3-year validity); re-assessment initiated before expiry | DETERMINISTIC |
| Evidence | ENX portal label record with assessment date; re-assessment engagement if approaching expiry | DETERMINISTIC |

```python
class TestTISAXValidity:
    """TISAX label validity: 3-year expiry; CAP required for any non-conformities."""

    def test_tisax_label_current(self, controls_evidence: dict, reference_date: date):
        from datetime import timedelta
        label = controls_evidence.get("tisax_label", {})
        assessment_date = label.get("last_assessment_date")
        assert assessment_date is not None, "TISAX label assessment date must be recorded"
        expiry = assessment_date + timedelta(days=TISAX_LABEL_VALIDITY_YEARS * 365)
        assert reference_date <= expiry, (
            f"TISAX label has expired. Assessment date: {assessment_date}; "
            f"Expiry: {expiry}; Current: {reference_date}"
        )

    @pytest.mark.human_review_required(
        reason=(
            "Adequacy of corrective action plan (CAP) for TISAX non-conformities requires "
            "assessor evaluation — the CAP must address root cause and prevent recurrence, "
            "which cannot be verified programmatically"
        )
    )
    def test_cap_adequacy_for_nonconformities(self, controls_evidence: dict):
        label = controls_evidence.get("tisax_label", {})
        nonconformities = label.get("open_nonconformities", [])
        if not nonconformities:
            return
        for nc in nonconformities:
            assert nc.get("cap_submitted", False), (
                f"Corrective action plan must be submitted for non-conformity {nc['nc_id']} "
                f"before label is issued"
            )
```

---

## Open assumptions

| ID | Control | Summary | Review date |
|---|---|---|---|
| ASSUME-TISAX-1_1-001 | ISMS scope | Scope covers automotive project data; policy signed; annual review | 2027-05-21 |
| ASSUME-TISAX-1_1-002 | Risk management | Risk register current; treatment decisions recorded; management acceptance | 2027-05-21 |
| ASSUME-TISAX-2_1-001 | Training | Training covers TISAX obligations; new employee within 30 days; annual refresh; records retained | 2027-05-21 |
| ASSUME-TISAX-2_1-002 | Screening | Background check commensurate with AL; completed before project data access | 2027-05-21 |
