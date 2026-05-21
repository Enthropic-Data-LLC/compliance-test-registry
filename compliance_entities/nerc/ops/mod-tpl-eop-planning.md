# NERC Non-CIP — MOD, TPL, EOP: Generator Verification, Transmission Planning, Emergency Operations

**Registry path:** `/regulation-registry/NERC-OPS/MOD-TPL-EOP/`
**Standards:** MOD-025-2 (generator real/reactive capability verification), TPL-001-5 (transmission planning performance), EOP-005-3 (system restoration from blackstart resources), EOP-008-2 (loss of control center functionality)
**Last parsed:** 2026-05-21
**Overall confidence:** MEDIUM — MOD-025 reverification cadence (5-year) and EOP-005 blackstart test cycle (3-year) are DETERMINISTIC; TPL-001 P-event category definitions are enumerable but adequacy is CONTESTED; EOP-008 backup control center capability is PARAMETERIZED
**Applicable entities:** MOD-025: Generator Owners (GO); TPL-001: Transmission Planners (TP), Planning Coordinators (PC); EOP-005: RC (procedures), GO/GOP (blackstart resources); EOP-008: RC, TOP, BA

---

## Scope Pre-Conditions

```python
@pytest.fixture(autouse=True)
def require_bes_registered_entity(entity_scope: dict):
    registered_functions = entity_scope.get("registered_nerc_functions", [])
    if not registered_functions:
        pytest.skip("Entity has no registered NERC functional roles — tests not applicable")

def is_generator_owner(entity_scope: dict) -> bool:
    return "GO" in entity_scope.get("registered_nerc_functions", [])

def is_transmission_planner_or_pc(entity_scope: dict) -> bool:
    return bool({"TP", "PC"} & set(entity_scope.get("registered_nerc_functions", [])))

def has_blackstart_resource(entity_scope: dict) -> bool:
    return entity_scope.get("has_blackstart_resources", False)
```

---

## MOD-025-2 — Generator Real and Reactive Power Capability Verification (PARAMETERIZED with DETERMINISTIC cadence)

### Source excerpt

> **R1.** Each Generator Owner shall verify the Real and Reactive Power capability of each of its applicable generating units at the higher of the following: (1) within the first 6 months after the unit enters commercial operation; (2) within 6 months of a significant plant modification.
>
> **R2.** Each Generator Owner shall reverify the Real and Reactive Power capability of each of its applicable generating units at least once every 60 calendar months.

### Verification cadence

| Trigger | Deadline | Classification |
|---|---|---|
| Initial: new unit enters commercial operation | Within 6 months | DETERMINISTIC |
| Initial: significant plant modification | Within 6 months of modification | DETERMINISTIC (trigger-based) |
| Reverification | Every 60 calendar months (5 years) from last verification | DETERMINISTIC |
| Significant modification definition | GO-determined; documented; modification affecting P or Q capability | PARAMETERIZED |

### Verification method

MOD-025 allows two methods for capability verification:

| Method | Description | Applicable to |
|---|---|---|
| Method 1 — Testing | Measure real and reactive output at several operating points during normal operation or dedicated test | All generating unit types |
| Method 2 — Engineering analysis | Calculate P-Q capability from design parameters and nameplate data (allowed for certain unit types) | Units where testing is impractical |

**Assumption (ASSUME-NERC-MOD-001):** MOD-025 verification compliance: (1) "significant plant modification" includes changes to generator windings, excitation system, power factor correction capacitors, step-up transformer, or control systems that could change P or Q capability; routine maintenance and minor control adjustments are not significant modifications; (2) verification using Method 1 (testing) is preferred — test data includes MW and MVAR readings at multiple voltage and MW operating points covering the full P-Q capability diagram; (3) Method 2 (engineering analysis) must be supported by design data and software modeling; the generator model used must be the same model submitted under MOD-026/027; (4) the 60-month reverification clock starts at the date of the most recent verification (not the original commercial operation date); (5) verification report includes: unit ID, date of test or analysis, methodology used, P-Q capability table or curve, any deviations from nameplate data, and engineer signature; (6) entities with units in extended cold shutdown may request a NERC waiver from the 60-month requirement — waiver request must be submitted before the interval expires.

**Overall: DETERMINISTIC for 6-month initial and 60-month reverification clocks → Pattern 1; PARAMETERIZED for "significant modification" determination → Pattern 2; PARAMETERIZED for verification method adequacy → Pattern 2**

---

### Test specifications — MOD-025-2

```yaml
spec_id: NERC-MOD-025-001
framework: NERC Reliability Standard MOD-025-2
sections:
  - R1 (initial verification within 6 months)
  - R2 (reverification every 60 months)
confidence: HIGH (cadence) / MEDIUM (method adequacy)
patterns_used:
  - Pattern 1 (DETERMINISTIC)
  - Pattern 2 (assumption-based)
scope_gate: registered_nerc_function includes GO
assumptions:
  - ASSUME-NERC-MOD-001
```

```python
import pytest
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


@pytest.fixture(autouse=True)
def require_generator_owner(entity_scope: dict):
    if "GO" not in entity_scope.get("registered_nerc_functions", []):
        pytest.skip("Entity is not a registered Generator Owner — MOD-025 not applicable")


@pytest.mark.assumption(
    id="ASSUME-NERC-MOD-001",
    description="MOD-025: significant modification definition, 60-month reverification clock from last test, verification report required elements, waiver path",
    approved_by="Compliance Officer",
    review_date="2026-05-21"
)
class TestMOD025GeneratorVerification:

    def test_initial_verification_within_six_months_of_commercial_operation(self, generating_unit: dict):
        """Each generating unit must have its initial P-Q verification within 6 months of commercial operation."""
        commercial_op_date = generating_unit.get("commercial_operation_date")
        if not commercial_op_date:
            pytest.skip("Commercial operation date not available")
        if isinstance(commercial_op_date, str):
            commercial_op_date = datetime.fromisoformat(commercial_op_date)
        initial_verification_date = generating_unit.get("initial_mod025_verification_date")
        assert initial_verification_date is not None, (
            f"Unit {generating_unit.get('unit_id')}: no initial MOD-025 verification on record"
        )
        if isinstance(initial_verification_date, str):
            initial_verification_date = datetime.fromisoformat(initial_verification_date)
        deadline = commercial_op_date + relativedelta(months=6)
        assert initial_verification_date <= deadline, (
            f"Unit {generating_unit.get('unit_id')}: initial MOD-025 verification date "
            f"{initial_verification_date.date()} exceeds 6-month deadline {deadline.date()}"
        )

    def test_reverification_not_overdue(self, generating_unit: dict):
        """Generator P-Q capability reverification must not be more than 60 months since last verification."""
        last_verification = generating_unit.get("last_mod025_verification_date")
        assert last_verification is not None, (
            f"Unit {generating_unit.get('unit_id')}: no MOD-025 verification date on record"
        )
        if isinstance(last_verification, str):
            last_verification = datetime.fromisoformat(last_verification)
        next_due = last_verification + relativedelta(months=60)
        assert datetime.now() <= next_due, (
            f"Unit {generating_unit.get('unit_id')}: MOD-025 reverification overdue since {next_due.date()} "
            f"(last verified {last_verification.date()}, 60-month interval)"
        )

    def test_reverification_approaching_alert(self, generating_unit: dict):
        """Flag units within 90 days of reverification deadline for planning purposes."""
        last_verification = generating_unit.get("last_mod025_verification_date")
        if not last_verification:
            pytest.skip("No last verification date — covered by overdue test")
        if isinstance(last_verification, str):
            last_verification = datetime.fromisoformat(last_verification)
        next_due = last_verification + relativedelta(months=60)
        days_remaining = (next_due - datetime.now()).days
        if 0 < days_remaining <= 90:
            pytest.warns(
                UserWarning,
                match=f"Unit {generating_unit.get('unit_id')}: MOD-025 reverification due in {days_remaining} days"
            )

    def test_verification_report_has_required_elements(self, mod025_verification_report: dict):
        """Verification report must contain all required elements."""
        required_fields = [
            "unit_id",
            "verification_date",
            "methodology",  # Method 1 (testing) or Method 2 (engineering analysis)
            "pq_capability_data",  # curve or table of P-Q values
            "engineer_signature",
        ]
        missing = [f for f in required_fields if not mod025_verification_report.get(f)]
        assert not missing, (
            f"MOD-025 verification report for unit {mod025_verification_report.get('unit_id')} "
            f"missing required elements: {missing}"
        )
```

---

## TPL-001-5 — Transmission System Planning Performance Requirements (PARAMETERIZED — P-event categories enumerable)

### Source excerpt

> **R1.** Each Transmission Planner (TP) and Planning Coordinator (PC) shall each perform an annual Steady-State and Stability Assessment.
>
> **R2.** The steady-state and stability assessments shall evaluate the following planning events... [P0 through P7 categories defined]

### P-event planning categories

TPL-001-5 defines seven planning event categories (P0–P7) representing different levels of contingency stress. Each must be evaluated annually for thermal, voltage, and stability performance.

| Category | Description | Expected performance |
|---|---|---|
| P0 | No contingency (normal system) | No violations — system must meet all performance requirements under normal conditions |
| P1 | Single contingency — loss of one BES element | No uncontrolled loss of load; no thermal/voltage violations outside post-contingency limits |
| P2 | Single contingency — loss of two or more elements operated as one (e.g., bus fault) | Limited loss of load permissible; no cascading |
| P3 | Multiple contingency — loss of two or more BES elements | Limited loss of load permissible; no cascading; corrective actions may be relied upon |
| P4 | Extreme event — loss of largest generating unit(s) + common structure failure | Extreme event performance criteria apply |
| P5 | Delayed clearing — fault not cleared in normal protection zone time | Stability may be impaired; no widespread cascading |
| P6 | Two overlapping singles — independent P1 events occurring simultaneously | Limited impact permissible |
| P7 | Common structure — shared tower or right-of-way elements | Performance criteria depend on specific design |

**Element extraction**

| Element | Value | Classification |
|---|---|---|
| Condition | TP or PC registered function | DETERMINISTIC |
| Obligation | Annual steady-state AND stability assessment | DETERMINISTIC (annual cadence) |
| Obligation | Assess all seven P-event categories | DETERMINISTIC (enumerable) |
| Adequacy of results | Whether violations found are acceptable under TPL-001 criteria | PARAMETERIZED |
| Corrective action plan | Required if violations found; adequacy is engineering judgment | PARAMETERIZED |
| Reporting | Results shared with RC and TO on request | DETERMINISTIC |

**Assumption (ASSUME-NERC-TPL-001):** TPL-001 planning compliance: (1) "annual" means the assessment must be completed and documented each calendar year — no gap year is permitted; (2) the base case used for the assessment must represent the near-term (≤10 year) transmission planning horizon with forecast load and committed generation; (3) P0 violations must be corrected before they occur — there are no acceptable P0 violations in a compliant system; (4) for P1–P7 violations: the entity must either implement a corrective action plan (new facilities, operational limits, or demand response) or document why the violation is acceptable under TPL-001 performance criteria (limited circumstances); (5) "stability assessment" means transient stability simulation — steady-state alone is insufficient; (6) results must be retained as compliance evidence — NERC audit expectation: last 3 annual assessment packages retained.

**Overall: DETERMINISTIC for annual cadence and P-event coverage → Pattern 1; PARAMETERIZED for violations acceptability and corrective action adequacy → Pattern 2; CONTESTED for P3+ extreme event acceptability → Pattern 3**

---

### Test specifications — TPL-001-5

```yaml
spec_id: NERC-TPL-001-001
framework: NERC Reliability Standard TPL-001-5
sections:
  - R1 (annual steady-state + stability assessment)
  - R2 (P0–P7 planning event evaluation)
confidence: HIGH (annual cadence) / MEDIUM (P-event adequacy) / CONTESTED (extreme event acceptability)
patterns_used:
  - Pattern 1 (DETERMINISTIC)
  - Pattern 2 (assumption-based)
  - Pattern 3 (human review for extreme event acceptability)
scope_gate: registered_nerc_function includes TP or PC
assumptions:
  - ASSUME-NERC-TPL-001
```

```python
REQUIRED_P_EVENT_CATEGORIES = {"P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7"}


@pytest.fixture(autouse=True)
def require_transmission_planner_or_pc(entity_scope: dict):
    tpl_roles = {"TP", "PC"}
    registered = set(entity_scope.get("registered_nerc_functions", []))
    if not (tpl_roles & registered):
        pytest.skip("Entity is not a TP or PC — TPL-001 not applicable")


@pytest.mark.assumption(
    id="ASSUME-NERC-TPL-001",
    description="Annual assessment deadline, near-term base case, P0 violations unacceptable, stability simulation required, 3-year retention",
    approved_by="Compliance Officer",
    review_date="2026-05-21"
)
class TestTPL001TransmissionPlanning:

    def test_annual_assessment_completed_current_year(self, tpl_assessment_registry: dict):
        """Annual TPL-001 assessment must be completed and documented each calendar year."""
        current_year = datetime.now().year
        current_year_assessment = tpl_assessment_registry.get(current_year)
        # Allow prior year if current year just started (Q1 grace)
        if current_year_assessment is None and datetime.now().month <= 3:
            prior_year_assessment = tpl_assessment_registry.get(current_year - 1)
            assert prior_year_assessment and prior_year_assessment.get("completed"), (
                f"No TPL-001 annual assessment for {current_year - 1} or {current_year}"
            )
        else:
            assert current_year_assessment and current_year_assessment.get("completed"), (
                f"Annual TPL-001 assessment for {current_year} not complete"
            )

    def test_assessment_covers_all_p_event_categories(self, tpl_annual_assessment: dict):
        """Annual assessment must evaluate all P0–P7 planning event categories."""
        assessed_categories = set(tpl_annual_assessment.get("p_event_categories_evaluated", []))
        missing = REQUIRED_P_EVENT_CATEGORIES - assessed_categories
        assert not missing, (
            f"TPL-001 assessment does not cover P-event categories: {missing}"
        )

    def test_assessment_includes_stability_simulation(self, tpl_annual_assessment: dict):
        """Annual assessment must include transient stability simulation, not steady-state only."""
        assert tpl_annual_assessment.get("stability_simulation_performed"), (
            "TPL-001 assessment does not include transient stability simulation — steady-state only is insufficient"
        )

    def test_p0_violations_not_present(self, tpl_annual_assessment: dict):
        """P0 (normal system) violations must not exist in a compliant transmission system."""
        p0_violations = tpl_annual_assessment.get("p0_violations", [])
        assert not p0_violations, (
            f"TPL-001 assessment found {len(p0_violations)} P0 violations — "
            "no P0 violations are acceptable: {p0_violations}"
        )

    def test_violations_have_corrective_action_plans(self, tpl_annual_assessment: dict):
        """Any planning violations (P1–P7) must have associated corrective action plans."""
        all_violations = []
        for p_cat in ["P1", "P2", "P3", "P4", "P5", "P6", "P7"]:
            violations = tpl_annual_assessment.get(f"{p_cat.lower()}_violations", [])
            all_violations.extend(violations)
        for violation in all_violations:
            if not violation.get("acceptable_per_tpl001_criteria"):
                assert violation.get("corrective_action_plan_id"), (
                    f"TPL-001 {violation.get('category')} violation '{violation.get('violation_id')}': "
                    "no corrective action plan and not documented as acceptable under TPL-001 criteria"
                )

    @pytest.mark.human_review_required(
        reason="Acceptability of P3–P7 extreme event violations under TPL-001-5 performance criteria is "
               "an engineering and regulatory judgment requiring Transmission Planner and Planning Coordinator "
               "sign-off. Extreme event acceptability criteria involve probabilistic and consequence assessments "
               "that cannot be reduced to a deterministic rule. Pattern 3: surface for human determination."
    )
    def test_extreme_event_violation_acceptability(self, tpl_annual_assessment: dict):
        """[HUMAN REVIEW] P3–P7 violation acceptability cannot be determined algorithmically."""
        extreme_violations = []
        for p_cat in ["P3", "P4", "P5", "P6", "P7"]:
            violations = tpl_annual_assessment.get(f"{p_cat.lower()}_violations", [])
            extreme_violations.extend(v for v in violations if v.get("acceptable_per_tpl001_criteria"))
        if not extreme_violations:
            pytest.skip("No P3–P7 violations marked as acceptable — human review not triggered")
        for violation in extreme_violations:
            assert violation.get("acceptability_review_by"), (
                f"Violation {violation.get('violation_id')} is claimed acceptable under TPL-001 criteria "
                "but has no documented TP/PC engineer sign-off"
            )
```

---

## EOP-005-3 — System Restoration from Blackstart Resources (PARAMETERIZED with DETERMINISTIC test interval)

### Source excerpt

> **R13.** Each Generator Owner with a BES blackstart generating unit shall ensure each of its BES blackstart generating units is tested in accordance with the test schedule in the entity's Restoration Plan, but no less than once every 36 calendar months.
>
> **R12.** Each Generator Owner with a BES blackstart generating unit shall provide its Reliability Coordinator with the results of its blackstart test upon request.

### Blackstart test requirements

| Requirement | Value | Classification |
|---|---|---|
| Test interval | Maximum 36 calendar months (3 years) between tests | DETERMINISTIC |
| Test types | Full start (from zero), partial (load-rejected), or coordinated — entity's Restoration Plan specifies | PARAMETERIZED (plan adequacy) |
| Documentation | Start time, end time, MW and MVAR output, any deviations from expected performance | DETERMINISTIC (content required) |
| Deviation handling | Deviations documented; corrective actions taken | PARAMETERIZED |
| Restoration plan integration | Test schedule documented in Restoration Plan | DETERMINISTIC (existence) |

**Assumption (ASSUME-NERC-EOP-001):** Blackstart test compliance: (1) the 36-month interval is measured from the date of the previous successful test; a failed test does not restart the clock — the interval runs from the last successful test; (2) a "successful" test is one where the blackstart unit started from zero (or load-rejected state) and demonstrated ability to energize its designated cranking path or provide start power to another unit; (3) partial (load-rejected) tests are acceptable where a full blackstart start from zero is operationally impractical — the test must still demonstrate isolation capability and governor/excitation response; (4) test results must be retained for at least one complete test cycle (36 months) plus an additional 6 months for NERC audit availability — effectively 42 months minimum; (5) if a test fails, a follow-up retest must be performed after corrective action; the entity notifies its RC of the test result and any failure; (6) for units under extended maintenance outage: test requirement is triggered on return to service — unit must be tested before being designated as available for blackstart operations.

**Overall: DETERMINISTIC for 36-month test interval → Pattern 1; PARAMETERIZED for test type and corrective action adequacy → Pattern 2**

---

## EOP-008-2 — Loss of Control Center Functionality (PARAMETERIZED)

### Source excerpt

> **R1.** Each Reliability Coordinator, Transmission Operator, and Balancing Authority shall have a documented plan to continue the reliability functions necessary to operate the BES in the event of a loss of control center functionality.
>
> **R2.** Each [applicable entity] shall exercise its loss of control center functionality plan in conjunction with its reliability coordinator at least once every 60 calendar months.

### Backup control center requirements

| Requirement | Value | Classification |
|---|---|---|
| Documented backup plan | Written plan for continued BES operations if primary control center is lost | DETERMINISTIC (existence) |
| Backup control center designation | Specific location with communications and monitoring capability | DETERMINISTIC (designation required) |
| Exercise cadence | At least once every 60 calendar months (5 years) | DETERMINISTIC |
| Exercise coordination | With RC; must demonstrate actual capability | PARAMETERIZED (scope of demonstration) |
| Plan content | Required: backup location, activation process, key contacts, capability description | PARAMETERIZED (adequacy) |

**Assumption (ASSUME-NERC-EOP-002):** EOP-008 compliance: (1) the backup control center must have: voice communications to neighboring TOPs/BAs/RC, SCADA or equivalent monitoring of the BES, and access to operating procedures; (2) the 60-month exercise interval starts from the last documented exercise; (3) exercises must demonstrate actual operational capability — a tabletop only is not sufficient; actual use of backup SCADA and backup communications must be tested; (4) plan must be updated within 6 months of any material change to the primary or backup control center; (5) if the backup control center is a third-party facility (e.g., a regional coordination center), a written agreement establishing availability must be in place and reviewed annually; (6) plans must be retained for at least one exercise cycle + 6 months.

**Overall: DETERMINISTIC for plan existence and 60-month exercise cadence → Pattern 1; PARAMETERIZED for plan adequacy and exercise scope → Pattern 2**

---

### Test specifications — EOP-005-3 and EOP-008-2

```yaml
spec_id: NERC-EOP-005-008-001
framework: NERC Reliability Standards EOP-005-3, EOP-008-2
sections:
  - EOP-005-3 R13 (blackstart test ≤36 months)
  - EOP-008-2 R1 (backup plan existence)
  - EOP-008-2 R2 (exercise ≤60 months)
confidence: HIGH (test/exercise intervals) / MEDIUM (plan adequacy)
patterns_used:
  - Pattern 1 (DETERMINISTIC)
  - Pattern 2 (assumption-based)
scope_gate:
  EOP-005: registered_nerc_function includes GO and has_blackstart_resources
  EOP-008: registered_nerc_function includes RC, TOP, or BA
assumptions:
  - ASSUME-NERC-EOP-001  # Blackstart: 36-month from last successful test, partial test acceptable
  - ASSUME-NERC-EOP-002  # Backup: actual demonstration required, 60-month exercise, agreement for third-party
```

```python
from dateutil.relativedelta import relativedelta


# ---------------------------------------------------------------------------
# EOP-005-3 Blackstart Tests
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def require_blackstart_resource(entity_scope: dict):
    if "GO" not in entity_scope.get("registered_nerc_functions", []) or \
       not entity_scope.get("has_blackstart_resources", False):
        pytest.skip("Entity is not a GO with blackstart resources — EOP-005 R13 not applicable")


@pytest.mark.assumption(
    id="ASSUME-NERC-EOP-001",
    description="36-month interval from last successful test; partial (load-rejected) acceptable; deviations documented; 42-month retention",
    approved_by="Compliance Officer",
    review_date="2026-05-21"
)
class TestEOP005BlackstartTesting:

    def test_blackstart_test_schedule_in_restoration_plan(self, restoration_plan: dict):
        """Blackstart test schedule must be documented in the Restoration Plan."""
        assert restoration_plan.get("blackstart_test_schedule"), (
            "Restoration Plan has no documented blackstart test schedule — EOP-005 R13 requires it"
        )

    def test_blackstart_unit_test_not_overdue(self, blackstart_unit: dict):
        """Blackstart generating unit must be tested at least once every 36 calendar months."""
        last_successful_test = blackstart_unit.get("last_successful_blackstart_test_date")
        assert last_successful_test is not None, (
            f"Blackstart unit {blackstart_unit.get('unit_id')}: no test date on record"
        )
        if isinstance(last_successful_test, str):
            last_successful_test = datetime.fromisoformat(last_successful_test)
        next_due = last_successful_test + relativedelta(months=36)
        assert datetime.now() <= next_due, (
            f"Blackstart unit {blackstart_unit.get('unit_id')}: test overdue since {next_due.date()} "
            f"(last successful test {last_successful_test.date()}, 36-month interval)"
        )

    def test_blackstart_test_report_has_required_elements(self, blackstart_test_report: dict):
        """Blackstart test report must document start time, end time, output, and deviations."""
        unit_id = blackstart_test_report.get("unit_id")
        assert blackstart_test_report.get("test_start_time"), f"Unit {unit_id}: no test start time"
        assert blackstart_test_report.get("test_end_time"), f"Unit {unit_id}: no test end time"
        assert blackstart_test_report.get("mw_output_achieved") is not None, (
            f"Unit {unit_id}: no MW output documented"
        )
        assert blackstart_test_report.get("test_result") in {"successful", "partial", "failed"}, (
            f"Unit {unit_id}: test result must be 'successful', 'partial', or 'failed'"
        )
        # Deviations field must exist (even if empty list means no deviations)
        assert "deviations" in blackstart_test_report, f"Unit {unit_id}: no deviations field in test report"

    def test_test_failure_has_corrective_action(self, blackstart_test_report: dict):
        """A failed blackstart test must have a documented corrective action."""
        if blackstart_test_report.get("test_result") == "successful":
            pytest.skip("Test was successful — corrective action not required")
        if blackstart_test_report.get("test_result") == "partial":
            pytest.skip("Partial test — corrective action required only if deviations found")
        # Failed test
        assert blackstart_test_report.get("corrective_action_plan_id"), (
            f"Blackstart test for unit {blackstart_test_report.get('unit_id')} failed but no corrective action plan"
        )


# ---------------------------------------------------------------------------
# EOP-008-2 Backup Control Center
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def require_eop008_applicable_entity(entity_scope: dict):
    eop_roles = {"RC", "TOP", "BA"}
    registered = set(entity_scope.get("registered_nerc_functions", []))
    if not (eop_roles & registered):
        pytest.skip("Entity does not have RC, TOP, or BA registration — EOP-008 not applicable")


@pytest.mark.assumption(
    id="ASSUME-NERC-EOP-002",
    description="Backup control center: actual operational demonstration required (not tabletop only), 60-month from last exercise, third-party agreement annual review",
    approved_by="Compliance Officer",
    review_date="2026-05-21"
)
class TestEOP008BackupControlCenter:

    def test_backup_control_center_plan_exists(self, eop008_plan: dict):
        """A documented loss of control center functionality plan must exist."""
        assert eop008_plan.get("plan_document_id"), "No EOP-008 loss of control center functionality plan"
        assert eop008_plan.get("backup_location"), "EOP-008 plan has no designated backup control center location"

    def test_backup_plan_has_required_elements(self, eop008_plan: dict):
        """EOP-008 plan must contain all required elements."""
        required_elements = [
            "backup_location",
            "activation_process",
            "key_contacts",
            "communications_capability_description",
            "monitoring_capability_description",
        ]
        missing = [e for e in required_elements if not eop008_plan.get(e)]
        assert not missing, f"EOP-008 plan missing required elements: {missing}"

    def test_backup_center_exercise_not_overdue(self, eop008_plan: dict):
        """Backup control center exercise must be completed at least once every 60 calendar months."""
        last_exercise = eop008_plan.get("last_exercise_date")
        assert last_exercise is not None, "No EOP-008 backup control center exercise on record"
        if isinstance(last_exercise, str):
            last_exercise = datetime.fromisoformat(last_exercise)
        next_due = last_exercise + relativedelta(months=60)
        assert datetime.now() <= next_due, (
            f"EOP-008 backup control center exercise overdue since {next_due.date()} "
            f"(last exercise {last_exercise.date()}, 60-month interval)"
        )

    def test_exercise_included_actual_operational_demonstration(self, eop008_exercise_record: dict):
        """EOP-008 exercise must demonstrate actual operational capability, not tabletop only."""
        assert eop008_exercise_record.get("actual_scada_or_monitoring_tested"), (
            f"EOP-008 exercise {eop008_exercise_record.get('exercise_id')}: no actual SCADA/monitoring "
            "demonstration — tabletop exercise alone does not satisfy EOP-008 R2"
        )
        assert eop008_exercise_record.get("actual_communications_tested"), (
            f"EOP-008 exercise {eop008_exercise_record.get('exercise_id')}: no actual communications "
            "demonstration documented"
        )

    def test_third_party_backup_agreement_reviewed_annually(self, eop008_plan: dict):
        """If backup control center is a third-party facility, written agreement must be reviewed annually."""
        if not eop008_plan.get("backup_is_third_party", False):
            pytest.skip("Backup control center is not a third-party facility — not applicable")
        last_review = eop008_plan.get("third_party_agreement_review_date")
        assert last_review, "Third-party backup agreement has no documented review date"
        if isinstance(last_review, str):
            last_review = datetime.fromisoformat(last_review)
        days_since = (datetime.now() - last_review).days
        assert days_since <= 365, (
            f"Third-party backup control center agreement last reviewed {last_review.date()} "
            f"({days_since} days ago) — annual review required"
        )
```

---

## Assumption registry (this file)

| ID | Standard | Summary | Review date |
|---|---|---|---|
| ASSUME-NERC-MOD-001 | MOD-025-2 | Generator P-Q verification: significant modification definition, 60-month from last test, verification report required elements, cold shutdown waiver path | 2026-05-21 |
| ASSUME-NERC-TPL-001 | TPL-001-5 | Annual planning assessment: calendar year deadline, near-term base case, P0 unacceptable, stability simulation required, 3-year retention | 2026-05-21 |
| ASSUME-NERC-EOP-001 | EOP-005-3 | Blackstart test: 36-month from last successful test, partial (load-rejected) acceptable, failed test triggers retest, 42-month records retention | 2026-05-21 |
| ASSUME-NERC-EOP-002 | EOP-008-2 | Backup control center: actual operational demonstration required, 60-month exercise, third-party agreement reviewed annually | 2026-05-21 |

---

## Cross-references

- **MOD-025 → MOD-026/027:** The P-Q capability data produced by MOD-025 verification must be consistent with the generator model data submitted under MOD-026 (excitation) and MOD-027 (governor) — a discrepancy between verified capability and model parameters requires model update
- **MOD-025 → FAC-008-3:** Generator real power capability is a component of facility ratings; FAC-008 ratings must reflect MOD-025 verified capability, not just nameplate
- **TPL-001 → FAC-008:** Transmission planning studies (TPL-001) use facility ratings (FAC-008) as inputs; inconsistent or outdated ratings invalidate planning study conclusions
- **EOP-005 blackstart test → EOP-004:** A blackstart test failure that results in a loss of reliability capability may be an EOP-004 reportable event — evaluate for BES loss of load ≥300 MW or equipment damage criteria
- **EOP-008 backup center → CIP-006:** Physical security of backup control centers is addressed in CIP-006 (Physical Security); both standards must be satisfied simultaneously — a backup center that cannot achieve CIP compliance is not a compliant backup
