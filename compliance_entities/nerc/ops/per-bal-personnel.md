# NERC Non-CIP — PER, BAL: Operator Credentials, Training, and Frequency Response

**Registry path:** `/regulation-registry/NERC-OPS/PER-BAL/`
**Standards:** PER-003-2 (operating personnel credentials), PER-005-3 (system personnel training), BAL-003-1 (frequency response and frequency bias setting)
**Last parsed:** 2026-05-21
**Applies to:** Bulk Electric System registered entities whose functional registration makes them subject to specific operational reliability standards — Transmission Operators, Balancing Authorities, Generator Operators, Reliability Coordinators, and others per NERC functional model
**Trigger:** NERC registration as one or more functional entities per the NERC Functional Model; specific standards apply based on functional registration (e.g., COM-001 applies to Transmission Operators and Balancing Authorities but not Generator Owners)
**Jurisdiction:** Same as NERC CIP — North America BES; enforced by NERC Regional Entities and FERC
**Not applicable to:** Same as NERC CIP — distribution-only utilities, behind-the-meter generation, unregistered entities; specific standards have applicability sections listing which functional entities are subject
**Overall confidence:** HIGH — credential currency and BAL-003 FRO compliance are DETERMINISTIC binary checks; training hour counts are DETERMINISTIC; training content adequacy is PARAMETERIZED
**Applicable entities:** PER-003: RC, TOP, BA functional entities (system operators); PER-005: same; BAL-003: Balancing Authorities (BA)

---

## Scope Pre-Conditions

```python
@pytest.fixture(autouse=True)
def require_bes_registered_entity(entity_scope: dict):
    registered_functions = entity_scope.get("registered_nerc_functions", [])
    if not registered_functions:
        pytest.skip("Entity has no registered NERC functional roles — tests not applicable")

def is_per_applicable_entity(entity_scope: dict) -> bool:
    per_roles = {"RC", "TOP", "BA"}
    return bool(per_roles & set(entity_scope.get("registered_nerc_functions", [])))

def is_balancing_authority(entity_scope: dict) -> bool:
    return "BA" in entity_scope.get("registered_nerc_functions", [])
```

---

## PER-003-2 — Operating Personnel Credentials (DETERMINISTIC)

### Source excerpt

> **R1.** Each Reliability Coordinator, Transmission Operator, and Balancing Authority shall ensure that each of its operating personnel performing the functional obligations of the Reliability Coordinator, Transmission Operator, or Balancing Authority, as applicable, holds a valid credential issued by NERC.

### NERC System Operator Certification

NERC administers the System Operator Certification Program. Credentials are role-specific and must be maintained continuously. Operating without a valid credential constitutes a per-occurrence violation.

| Credential | Applicable role | Renewal cycle | Continuing education requirement |
|---|---|---|---|
| Reliability Coordinator (RC) | RC operations personnel | 3 years from issuance | 200 Continuing Education Hours (CEH) per 3-year period |
| Transmission System Operator (TSO) | TOP operations personnel | 3 years | 200 CEH per 3-year period |
| Balancing, Interchange, and Transmission System Operator (BASO) | BA operations personnel | 3 years | 200 CEH per 3-year period |
| Reliability Operator (RO) | RC operations personnel at some entities | 3 years | 200 CEH |

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Individual performs system operator functions for RC/TOP/BA | DETERMINISTIC |
| Obligation | Hold valid NERC-issued credential for the applicable function | DETERMINISTIC |
| Currency | Credential must not be expired — active status in NERC certification database | DETERMINISTIC |
| Renewal trigger | Expires at end of 3-year certification period — renewal requires CEH attestation | DETERMINISTIC |
| Evidence | NERC certification number; expiry date; employer records showing credential on file at time of operations | DETERMINISTIC |

**Assumption (ASSUME-NERC-PER-001):** PER-003 credential compliance: (1) "operating personnel" means any individual who performs the day-to-day real-time control functions of the registered entity's function (e.g., system operator, area operator, energy control center operator) — does not include supervisors who oversee but do not operate; (2) credential is "valid" when: NERC certification database shows active status, expiry date has not passed, and credential is appropriate for the registered function being performed; (3) entities must track credential expiry dates for all operating personnel — a credential expired by even one day during a shift constitutes a violation; (4) the 200 CEH requirement for renewal is tracked and submitted to NERC by the certificant; the employer's obligation is to verify the employee holds a valid credential before allowing operations; (5) for new hires or personnel transitioning roles: credential must be obtained before solo operations are performed — supervised training operations under a qualified certificant are not a violation if properly documented.

**Overall: DETERMINISTIC → Pattern 1**

---

### Test specifications — PER-003-2

```yaml
spec_id: NERC-PER-003-001
framework: NERC Reliability Standard PER-003-2
section: R1 (credential currency)
confidence: HIGH
patterns_used:
  - Pattern 1 (DETERMINISTIC)
  - Pattern 2 (assumption-based)
scope_gate: registered_nerc_function includes RC, TOP, or BA
assumptions:
  - ASSUME-NERC-PER-001
```

```python
import pytest
from datetime import datetime
from typing import Optional


@pytest.fixture(autouse=True)
def require_per003_applicable_entity(entity_scope: dict):
    per_roles = {"RC", "TOP", "BA"}
    registered = set(entity_scope.get("registered_nerc_functions", []))
    if not (per_roles & registered):
        pytest.skip("Entity does not have RC, TOP, or BA registration — PER-003 not applicable")


@pytest.mark.assumption(
    id="ASSUME-NERC-PER-001",
    description="Credential currency: 3-year cycle, 200 CEH renewal requirement, employer verification obligation, new-hire supervised ops carve-out",
    approved_by="Compliance Officer",
    review_date="2026-05-21"
)
class TestPER003Credentials:

    def test_all_operators_have_nerc_credential_on_file(self, operator_roster: list):
        """All operating personnel must have a NERC credential number on file."""
        for operator in operator_roster:
            assert operator.get("nerc_credential_number"), (
                f"Operator {operator.get('operator_id')} has no NERC credential number on file"
            )

    def test_operator_credential_is_not_expired(self, operator: dict):
        """Operator's NERC credential must not be expired."""
        expiry = operator.get("nerc_credential_expiry")
        assert expiry is not None, (
            f"Operator {operator.get('operator_id')}: no credential expiry date on file"
        )
        if isinstance(expiry, str):
            expiry = datetime.fromisoformat(expiry)
        assert expiry >= datetime.now(), (
            f"Operator {operator.get('operator_id')} NERC credential expired {expiry.date()} — "
            "operations after expiry constitute a PER-003 violation"
        )

    def test_operator_credential_matches_registered_function(self, operator: dict, entity_scope: dict):
        """Operator credential type must be appropriate for the entity's registered function."""
        credential_type = operator.get("nerc_credential_type")
        registered_functions = entity_scope.get("registered_nerc_functions", [])
        valid_credential_map = {
            "RC": {"RC", "RO"},
            "TOP": {"TSO", "BASO"},
            "BA": {"BASO"},
        }
        applicable_credentials = set()
        for func in registered_functions:
            applicable_credentials |= valid_credential_map.get(func, set())
        assert credential_type in applicable_credentials, (
            f"Operator {operator.get('operator_id')} holds credential type '{credential_type}' "
            f"but entity functions {registered_functions} require one of: {applicable_credentials}"
        )

    def test_upcoming_credential_expirations_tracked(self, credential_tracking_system: dict):
        """Credential tracking system must alert before expiry to allow renewal."""
        assert credential_tracking_system.get("expiry_alert_configured"), (
            "No credential expiry alert configured — operators may operate with expired credentials"
        )
        alert_days = credential_tracking_system.get("advance_alert_days", 0)
        assert alert_days >= 60, (
            f"Credential expiry alert is only {alert_days} days in advance — "
            "60 days minimum recommended for renewal processing"
        )
```

---

## PER-005-3 — System Personnel Training (DETERMINISTIC for cadence; PARAMETERIZED for content adequacy)

### Source excerpt

> **R1.** Each Reliability Coordinator, Transmission Operator, and Balancing Authority shall have a documented annual training program for its operating personnel that contains the following content areas: (1) system topology; (2) operating processes and procedures; (3) abnormal and emergency operating conditions; (4) key NERC reliability standards applicable to the entity's registered function.
>
> **R2.** Each [applicable entity] shall ensure that each of its operating personnel completes the training specified in R1 at least once per calendar year.

### Training content requirements

| Required content area | Classification | Evidence |
|---|---|---|
| System topology (transmission network, generation, interconnections) | DETERMINISTIC (topic required) | Training curriculum documentation; sign-in sheets or LMS records |
| Operating processes and procedures (normal operations, dispatch protocols) | DETERMINISTIC (topic required) | Training curriculum; procedure walkthrough records |
| Abnormal and emergency operating conditions (contingencies, restoration, IROL response) | DETERMINISTIC (topic required) | Training curriculum; simulator exercise records |
| Key NERC reliability standards for the entity's registered function | DETERMINISTIC (topic required) | Training curriculum; tested knowledge verification |

### Annual training cadence

| Requirement | Threshold | Classification |
|---|---|---|
| Annual training program completion | 100% of operating personnel complete all four content areas each calendar year | DETERMINISTIC |
| Initial training for new operating personnel | Before assumption of unsupervised operating duties | DETERMINISTIC |
| Training program documentation | Written training plan with topics, hours, delivery method, and schedule | DETERMINISTIC |
| Training records retention | Retained for compliance evidence — NERC audit evidence expectation: 3 years minimum | DETERMINISTIC |

**Assumption (ASSUME-NERC-PER-002):** PER-005 training compliance: (1) "once per calendar year" = all four content areas completed by December 31 of each year; (2) training may be delivered as classroom, simulator, computer-based, webinar, or combined — delivery method must be documented; (3) each operator must personally complete the training — proxy completion or records fabrication is a violation; (4) for operating personnel who join mid-year: they must complete training before unsupervised operations, and a pro-rated or accelerated annual training must still be completed in the calendar year of hire; (5) simulator training for abnormal and emergency conditions is not required by the standard but is the industry-standard delivery for NERC certifying exam preparation and annual proficiency — entities should document simulator hours as a best practice; (6) PER-005 training content must be updated when system topology or operating procedures change materially — training delivery does not satisfy R1 if content is significantly out of date.

**Overall: DETERMINISTIC for annual cadence and required topics → Pattern 1; PARAMETERIZED for content adequacy and trainer qualifications → Pattern 2**

---

### Test specifications — PER-005-3

```yaml
spec_id: NERC-PER-005-001
framework: NERC Reliability Standard PER-005-3
sections:
  - R1 (training program content)
  - R2 (annual completion)
confidence: HIGH (cadence, content topics) / MEDIUM (content adequacy)
patterns_used:
  - Pattern 1 (DETERMINISTIC)
  - Pattern 2 (assumption-based)
scope_gate: registered_nerc_function includes RC, TOP, or BA
assumptions:
  - ASSUME-NERC-PER-002
```

```python
@pytest.fixture(autouse=True)
def require_per005_applicable_entity(entity_scope: dict):
    per_roles = {"RC", "TOP", "BA"}
    registered = set(entity_scope.get("registered_nerc_functions", []))
    if not (per_roles & registered):
        pytest.skip("Entity does not have RC, TOP, or BA registration — PER-005 not applicable")


REQUIRED_TRAINING_TOPICS = {
    "system_topology",
    "operating_processes_and_procedures",
    "abnormal_and_emergency_conditions",
    "nerc_reliability_standards",
}


@pytest.mark.assumption(
    id="ASSUME-NERC-PER-002",
    description="Annual training: calendar year deadline Dec 31, all four R1 topics, initial training before unsupervised ops, 3-year records retention",
    approved_by="Compliance Officer",
    review_date="2026-05-21"
)
class TestPER005Training:

    def test_annual_training_program_document_exists(self, training_program: dict):
        """A written annual training program must exist with all required content areas."""
        assert training_program.get("program_document_id"), "No written annual training program document"
        topics = set(training_program.get("content_areas", []))
        missing_topics = REQUIRED_TRAINING_TOPICS - topics
        assert not missing_topics, (
            f"Annual training program missing required PER-005 R1 content areas: {missing_topics}"
        )

    def test_all_operators_complete_annual_training(self, operator_roster: list, training_records: dict):
        """All operating personnel must complete annual training within each calendar year."""
        current_year = datetime.now().year
        for operator in operator_roster:
            op_id = operator.get("operator_id")
            completions = training_records.get(op_id, {}).get(current_year, [])
            completed_topics = {c.get("topic") for c in completions}
            missing = REQUIRED_TRAINING_TOPICS - completed_topics
            if missing:
                pytest.fail(
                    f"Operator {op_id}: annual training incomplete for {current_year}. "
                    f"Missing topics: {missing}"
                )

    def test_training_records_retained_minimum_three_years(self, training_records_policy: dict):
        """Training records must be retained for at least 3 years for NERC audit evidence."""
        retention_years = training_records_policy.get("retention_years")
        assert retention_years is not None, "No training records retention policy documented"
        assert retention_years >= 3, (
            f"Training records retention is {retention_years} years — NERC audit expectation is ≥3 years"
        )

    def test_new_operator_trained_before_unsupervised_operations(self, operator: dict, training_records: dict):
        """New operating personnel must complete initial training before unsupervised operations."""
        first_solo_date = operator.get("first_unsupervised_operations_date")
        if not first_solo_date:
            pytest.skip("Operator has not yet performed unsupervised operations")
        if isinstance(first_solo_date, str):
            first_solo_date = datetime.fromisoformat(first_solo_date)
        op_id = operator.get("operator_id")
        initial_training_records = [
            r for year_records in training_records.get(op_id, {}).values()
            for r in year_records
            if r.get("is_initial_training")
        ]
        assert initial_training_records, (
            f"Operator {op_id}: no initial training record found before unsupervised operations"
        )
        max_training_date = max(
            datetime.fromisoformat(r["completion_date"]) if isinstance(r["completion_date"], str)
            else r["completion_date"]
            for r in initial_training_records
        )
        assert max_training_date <= first_solo_date, (
            f"Operator {op_id}: initial training completed AFTER first unsupervised operations date"
        )
```

---

## BAL-003-1 — Frequency Response Obligation (DETERMINISTIC)

### Source excerpt

> **R1.** Each Balancing Authority (BA) shall provide frequency response no less than its Frequency Response Obligation (FRO).
>
> **R2.** Each BA shall provide NERC with a Frequency Bias Setting that is consistent with its FRO.

### Frequency Response Obligation (FRO) framework

The FRO is NERC's primary mechanism for ensuring the Interconnection has sufficient frequency response to arrest frequency decline following a large generation loss. NERC calculates and publishes each BA's FRO annually through the Frequency Response Initiative.

| Element | Value | Classification |
|---|---|---|
| FRO source | Published annually by NERC; specific MW obligation per BA | DETERMINISTIC — NERC-defined number |
| Measurement period | NERC measures BA frequency response using frequency event data (27-point method per BAL-003 Guidelines) | DETERMINISTIC |
| Obligation | BA must provide at least its FRO MW of frequency response during measured events | DETERMINISTIC (MW threshold binary) |
| Frequency Bias Setting | AGC bias setting must be consistent with FRO — reported to NERC annually | DETERMINISTIC |
| Non-compliance consequence | Corrective action plan required if BA does not meet its FRO | DETERMINISTIC (trigger) / PARAMETERIZED (adequacy of plan) |
| Measurement method | NERC calculates BA response using the 27-point method at least annually | DETERMINISTIC |

### FRO calculation and compliance evidence

| Step | Description | Classification |
|---|---|---|
| FRO publication | NERC publishes each BA's FRO in MW; BA acknowledges receipt | DETERMINISTIC |
| Frequency Bias Setting report | BA reports its AGC bias setting to NERC; setting must be ≥ FRO | DETERMINISTIC |
| Annual measurement | NERC measures BA response using qualifying frequency events; compares to FRO | DETERMINISTIC |
| Non-compliance determination | NERC notifies BA if measured response < FRO | DETERMINISTIC |
| Corrective action plan (CAP) | If non-compliant: BA submits CAP to NERC within specified timeframe | PARAMETERIZED (plan adequacy) |

**Assumption (ASSUME-NERC-BAL-001):** BAL-003 compliance: (1) FRO is the MW value published in NERC's annual Frequency Response Initiative report for the specific BA — BA must retain the NERC-issued FRO notification letter as compliance evidence; (2) Frequency Bias Setting submitted to NERC must be negative (droop-based) and numerically equal to or greater than the FRO in absolute value — a bias setting smaller in magnitude than the FRO is a violation; (3) if NERC's annual measurement shows BA response below FRO: BA must submit a corrective action plan (CAP) addressing the shortfall — typical corrective actions include governor droop settings, reserve obligations, or contractual frequency response resources; (4) entities that are a BA but with minimal generation (net importers) may have an FRO that they cannot self-supply — in these cases the CAP must address procurement of frequency response from other sources; (5) BAL-003 compliance is measured at the Interconnection level using actual frequency disturbance events — the 27-point method averages response across qualifying events in the measurement year; entities with no qualifying events in a given year are typically held harmless.

**Overall: DETERMINISTIC for FRO acknowledgment, bias setting, and CAP trigger → Pattern 1; PARAMETERIZED for CAP adequacy → Pattern 2**

---

### Test specifications — BAL-003-1

```yaml
spec_id: NERC-BAL-003-001
framework: NERC Reliability Standard BAL-003-1
sections:
  - R1 (frequency response obligation)
  - R2 (frequency bias setting)
confidence: HIGH (FRO acknowledgment, bias setting currency) / MEDIUM (CAP adequacy)
patterns_used:
  - Pattern 1 (DETERMINISTIC)
  - Pattern 2 (assumption-based)
scope_gate: registered_nerc_function includes BA
assumptions:
  - ASSUME-NERC-BAL-001
```

```python
@pytest.fixture(autouse=True)
def require_balancing_authority(entity_scope: dict):
    if "BA" not in entity_scope.get("registered_nerc_functions", []):
        pytest.skip("Entity is not a registered Balancing Authority — BAL-003 not applicable")


@pytest.mark.assumption(
    id="ASSUME-NERC-BAL-001",
    description="FRO = NERC-published MW obligation; bias setting ≥ FRO in absolute value; non-compliance triggers CAP; 27-point measurement method",
    approved_by="Compliance Officer",
    review_date="2026-05-21"
)
class TestBAL003FrequencyResponse:

    def test_fro_acknowledgment_letter_on_file(self, bal003_compliance_data: dict):
        """BA must have the NERC-issued FRO notification letter on file as compliance evidence."""
        assert bal003_compliance_data.get("fro_notification_document_id"), (
            "No NERC FRO notification document on file — BAL-003 compliance evidence missing"
        )

    def test_frequency_bias_setting_meets_fro(self, bal003_compliance_data: dict):
        """BA's Frequency Bias Setting must be numerically consistent with (≥) its FRO."""
        fro_mw = bal003_compliance_data.get("fro_mw")
        bias_setting_mw = bal003_compliance_data.get("frequency_bias_setting_mw")
        assert fro_mw is not None, "FRO MW value not documented"
        assert bias_setting_mw is not None, "Frequency Bias Setting not documented"
        # Both values are negative for droop-based response; compare absolute values
        assert abs(bias_setting_mw) >= abs(fro_mw), (
            f"Frequency Bias Setting {bias_setting_mw} MW is less in magnitude than FRO {fro_mw} MW — "
            "BAL-003 R2 violation: bias must be ≥ FRO in absolute value"
        )

    def test_bias_setting_submitted_to_nerc(self, bal003_compliance_data: dict):
        """BA must submit its Frequency Bias Setting to NERC."""
        assert bal003_compliance_data.get("bias_setting_submitted_to_nerc_date"), (
            "No record of Frequency Bias Setting submission to NERC"
        )

    def test_annual_measurement_result_on_file(self, bal003_compliance_data: dict):
        """Annual NERC frequency response measurement result must be retained."""
        assert bal003_compliance_data.get("annual_measurement_year"), (
            "No annual NERC frequency response measurement result on file"
        )
        assert bal003_compliance_data.get("annual_measurement_result_mw") is not None, (
            "Annual measurement result (MW) not recorded"
        )

    def test_non_compliant_measurement_triggers_cap(self, bal003_compliance_data: dict):
        """If annual measurement falls below FRO, a corrective action plan must be on file."""
        fro_mw = bal003_compliance_data.get("fro_mw", 0)
        measured_mw = bal003_compliance_data.get("annual_measurement_result_mw")
        if measured_mw is None:
            pytest.skip("No annual measurement result available")
        if abs(measured_mw) >= abs(fro_mw):
            pytest.skip("Measured frequency response meets FRO — no CAP required")
        # Non-compliant case: must have CAP
        assert bal003_compliance_data.get("corrective_action_plan_id"), (
            f"BA measured frequency response {measured_mw} MW is below FRO {fro_mw} MW — "
            "corrective action plan required but not found"
        )

    def test_bias_setting_consistent_with_current_fro(self, bal003_compliance_data: dict):
        """Frequency Bias Setting report must be for the current FRO reporting year."""
        current_year = datetime.now().year
        submission_date = bal003_compliance_data.get("bias_setting_submitted_to_nerc_date")
        if not submission_date:
            pytest.skip("No submission date available")
        if isinstance(submission_date, str):
            submission_date = datetime.fromisoformat(submission_date)
        submission_year = submission_date.year
        assert submission_year >= current_year - 1, (
            f"Frequency Bias Setting submission is from {submission_year} — "
            f"must be current year ({current_year}) or prior year if FRO not yet published"
        )
```

---

## Assumption registry (this file)

| ID | Standard | Summary | Review date |
|---|---|---|---|
| ASSUME-NERC-PER-001 | PER-003-2 | System operator credentials: 3-year renewal cycle, 200 CEH, employer verification obligation, credential type must match registered function | 2026-05-21 |
| ASSUME-NERC-PER-002 | PER-005-3 | Annual training: calendar year Dec 31 deadline, all four R1 topics required, initial training before unsupervised ops, 3-year records retention | 2026-05-21 |
| ASSUME-NERC-BAL-001 | BAL-003-1 | FRO = NERC-published MW value; bias setting ≥ FRO absolute value; non-compliance triggers CAP; 27-point measurement; no qualifying events = harmless | 2026-05-21 |

---

## Cross-references

- **PER-003 → COM-002-4:** Only credentialed operators (PER-003) should be issuing directives subject to COM-002 three-part communication — uncredentialed operators performing real-time operations creates a dual violation
- **PER-005 → EOP standards:** Abnormal and emergency operations training required by PER-005 R1(3) must cover the entity's own EOP-004, EOP-005, and EOP-008 procedures — training content and operating procedures must stay synchronized
- **BAL-003 → BAL-001/002:** FRO and bias setting are foundational to BAL-001 control performance and BAL-002 disturbance recovery — an inadequate bias setting degrades both
- **PER-003 expiry tracking → CI/CD gate:** Credential expiry dates should be loaded into the compliance tracking system; automated alerts at 60-day and 30-day pre-expiry points prevent inadvertent violations
