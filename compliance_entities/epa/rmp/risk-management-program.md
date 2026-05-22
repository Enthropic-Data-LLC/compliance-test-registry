# EPA RMP — Risk Management Program (40 CFR Part 68)

**Framework:** Clean Air Act §112(r)(7) — 40 CFR Part 68 (Risk Management Program)
**Clauses:** §68.10 (program determination — Programs 1/2/3); §68.25 (worst-case release scenario); §68.36 (5-year accident history); §68.12 (Program 1 requirements); §68.48–68.96 (Program 2/3 prevention programs); §68.95 (emergency response program); §68.150–68.185 (RMP submission requirements — initial, resubmission, revision); §68.195 (accident reporting)
**Confidence:** DETERMINISTIC-dominant (TQ threshold determination; Program tier determination; RMP 5-year resubmission; 3-year accident history update; 5-year accident history content; immediate notification for releases with offsite impacts; worst-case scenario parameters per §68.22); PARAMETERIZED (consequence modeling methodology; PHA methodology and findings); CONTESTED (worst-case scenario safeguard crediting; worst-case release quantity selection)
**Last parsed:** 2026-05-21
**Applies to:** Facilities that have a regulated substance (77 toxic, 63 flammable) present in any single process at or above its threshold quantity (TQ) listed in 40 CFR Part 68 Appendix A or §68.115
**Trigger:** A regulated substance present in a single process at or above its TQ; approximately 12,500 facilities subject to RMP in the US; Program tier determined by accident history, public receptor proximity, and NAICS code
**Jurisdiction:** United States; EPA enforces; state and local agencies may have companion programs (California CUPA/Cal OES); RMP plans publicly available via EPA's RMP*Info database
**Not applicable to:** Processes with regulated substances below their TQs; naturally occurring substances at their naturally occurring concentrations; transportation of substances; retail facilities (agricultural retailers exempt below specific thresholds); Program 1 facilities with no public receptors in endpoint zone and no accidents in 5 years have significantly simplified requirements

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def rmp_scope(entity_profile: dict):
    if not entity_profile.get("subject_to_rmp", False):
        pytest.skip(
            "EPA RMP (40 CFR Part 68) does not apply — no regulated substance is "
            "present at or above its threshold quantity in any single process."
        )

@pytest.fixture
def program_2_or_3_scope(entity_profile: dict):
    program = entity_profile.get("rmp_program_level")
    if program not in (2, 3):
        pytest.skip("This requirement applies to Program 2 and 3 only.")

@pytest.fixture
def program_3_scope(entity_profile: dict):
    if entity_profile.get("rmp_program_level") != 3:
        pytest.skip("This requirement applies to Program 3 only.")
```

---

## Constants

```python
from typing import FrozenSet

# ── RMP submission and update timelines ───────────────────────────────────────

RMP_INITIAL_SUBMISSION_DAYS_BEFORE_OPERATION = 1   # Must have RMP before operating with TQ
RMP_RESUBMISSION_YEARS = 5                          # 5-year resubmission requirement
RMP_ACCIDENT_HISTORY_YEARS = 5                      # Must cover 5 years
RMP_REVISION_AFTER_ACCIDENTAL_RELEASE_DAYS = 6 * 30  # 6 months after qualifying accident

# ── Accident reporting ────────────────────────────────────────────────────────

RMP_ACCIDENT_NOTIFICATION_HOURS = 8  # Within 8 hours via NRC if release causes death/injury/shelter-in-place

# ── Worst-case release scenario — meteorological conditions (§68.22) ──────────

# These are DETERMINISTIC parameter requirements from EPA's model rule
WCS_WIND_SPEED_MPS = 1.5      # 1.5 m/s wind speed for toxic releases
WCS_STABILITY_CLASS = "F"     # Pasquill F stability class (most stable)
WCS_TEMPERATURE_CELSIUS = 25  # 25°C ambient temperature

# ── RMP required elements (5 sections) ───────────────────────────────────────

RMP_REQUIRED_SECTIONS: FrozenSet[str] = frozenset({
    "registration",
    "hazard_assessment",
    "prevention_program",
    "emergency_response_program",
    "five_year_accident_history",
})

# ── 5-year accident history required content ──────────────────────────────────

ACCIDENT_HISTORY_REQUIRED_FIELDS: FrozenSet[str] = frozenset({
    "date_and_time",
    "chemical_name",
    "quantity_released_pounds",
    "release_duration_minutes",
    "release_event_type",
    "weather_conditions",
    "deaths_injuries_evacuations",
    "property_damage",
    "offsite_impacts",
    "initiating_event",
    "contributing_factors",
    "offsite_responders_notified",
    "changes_introduced_to_prevent_reoccurrence",
})
```

---

## TestProgramDetermination

```python
class TestProgramDetermination:
    """40 CFR §68.10 — RMP Program level determination: binary DETERMINISTIC criteria."""

    def test_program_1_eligibility_correctly_assessed(self, entity_profile: dict):
        """§68.10(b): Program 1 requires (1) worst-case release would NOT reach public receptors,
        (2) no accidents in last 5 years, (3) coordination with LEPC for emergency response."""
        program = entity_profile.get("rmp_program_level")
        if program != 1:
            pytest.skip("Program 1 eligibility check applies to Program 1 facilities only")
        p1_criteria = entity_profile.get("program_1_eligibility", {})
        assert p1_criteria.get("wcs_no_public_receptor_in_endpoint") is True, \
            "Program 1: worst-case release endpoint must not reach public receptors — §68.10(b)(1)"
        assert p1_criteria.get("no_accidents_in_5_years") is True, \
            "Program 1: no accidents with offsite impacts in past 5 years — §68.10(b)(2)"
        assert p1_criteria.get("lepc_coordination") is True, \
            "Program 1: must coordinate emergency response with LEPC — §68.10(b)(3)"

    def test_program_3_correctly_assigned_for_osha_psm_processes(self, entity_profile: dict):
        """§68.10(d): Any process subject to OSHA PSM (29 CFR 1910.119) must be in Program 3."""
        for process in entity_profile.get("rmp_covered_processes", []):
            if process.get("subject_to_osha_psm") is True:
                assert process.get("rmp_program_level") == 3, (
                    f"Process '{process.get('id', 'unknown')}' is subject to OSHA PSM "
                    f"and must be in RMP Program 3 — 40 CFR §68.10(d)"
                )
```

---

## TestHazardAssessment

```python
class TestHazardAssessment:
    """40 CFR §§68.25–68.42 — Hazard assessment: worst-case and alternative release scenarios."""

    def test_worst_case_scenario_documented_for_each_process(self, program_2_or_3_scope, entity_profile: dict):
        """§68.25: Each Program 2/3 process requires a worst-case release scenario."""
        for process in entity_profile.get("rmp_covered_processes", []):
            if process.get("rmp_program_level") in (2, 3):
                assert process.get("worst_case_scenario_documented") is True, (
                    f"No worst-case release scenario for process '{process.get('id', 'unknown')}' "
                    f"— 40 CFR §68.25"
                )

    def test_wcs_uses_passive_mitigation_only(self, program_2_or_3_scope, entity_profile: dict):
        """§68.25(a): Worst-case scenario must assume passive mitigation only
        (no active mitigation credits — no emergency response, no sprinkler systems)."""
        for process in entity_profile.get("rmp_covered_processes", []):
            wcs = process.get("worst_case_scenario", {})
            if wcs:
                assert wcs.get("uses_passive_mitigation_only") is True, (
                    f"Worst-case scenario for process '{process.get('id', 'unknown')}' "
                    f"uses active mitigation — §68.25(a) allows only passive mitigation"
                )

    def test_wcs_meteorological_conditions_correct(self, program_2_or_3_scope, entity_profile: dict):
        """§68.22: Worst-case toxic release scenarios must use 1.5 m/s wind speed,
        F stability class, 25°C temperature (or local meteorological data if more stringent)."""
        for process in entity_profile.get("rmp_covered_processes", []):
            wcs = process.get("worst_case_scenario", {})
            if wcs and wcs.get("substance_type") == "toxic":
                wind = wcs.get("wind_speed_mps")
                stability = wcs.get("stability_class")
                assert wind is not None and wind <= WCS_WIND_SPEED_MPS, (
                    f"WCS for '{process.get('id', 'unknown')}': wind speed {wind} m/s "
                    f"exceeds §68.22 requirement of {WCS_WIND_SPEED_MPS} m/s"
                )
                assert stability == WCS_STABILITY_CLASS, (
                    f"WCS for '{process.get('id', 'unknown')}': stability class '{stability}' "
                    f"must be F per §68.22"
                )

    def test_alternative_release_scenario_documented(self, program_2_or_3_scope, entity_profile: dict):
        """§68.28: Alternative release scenario required for each Program 2/3 process."""
        for process in entity_profile.get("rmp_covered_processes", []):
            if process.get("rmp_program_level") in (2, 3):
                assert process.get("alternative_release_scenario_documented") is True, (
                    f"No alternative release scenario for process '{process.get('id', 'unknown')}' "
                    f"— 40 CFR §68.28"
                )
```

---

## TestFiveYearAccidentHistory

```python
class TestFiveYearAccidentHistory:
    """40 CFR §68.36 — 5-year accident history: required for all Programs."""

    def test_accident_history_covers_5_years(self, entity_profile: dict):
        """§68.36: RMP must include accident history for the 5 years preceding submission."""
        accident_history = entity_profile.get("rmp_accident_history", {})
        assert accident_history.get("covers_5_years") is True, \
            "RMP accident history must cover at least 5 years — 40 CFR §68.36"

    def test_each_qualifying_accident_has_required_fields(self, entity_profile: dict):
        """§68.42: Each accident in the history must include required data elements."""
        for accident in entity_profile.get("rmp_accidents", []):
            reported_fields = frozenset(accident.get("reported_fields", []))
            missing = ACCIDENT_HISTORY_REQUIRED_FIELDS - reported_fields
            assert not missing, (
                f"Accident '{accident.get('id', 'unknown')}' missing required history "
                f"fields: {sorted(missing)} — 40 CFR §68.42"
            )
```

---

## TestRMPSubmission

```python
class TestRMPSubmission:
    """40 CFR §§68.150–68.185 — RMP submission, resubmission, and updates."""

    def test_rmp_submitted_before_operation(self, entity_profile: dict):
        """§68.150: RMP must be submitted to EPA before operating a covered process."""
        rmp = entity_profile.get("rmp_submission", {})
        assert rmp.get("submitted") is True, \
            "No RMP submitted — required before operating a covered process (40 CFR §68.150)"

    def test_rmp_resubmitted_within_5_years(self, entity_profile: dict):
        """§68.190(b): RMP must be resubmitted at least every 5 years."""
        from datetime import date
        from dateutil.relativedelta import relativedelta
        rmp = entity_profile.get("rmp_submission", {})
        last_submission = rmp.get("last_submission_date")
        assert last_submission is not None, "RMP submission date not recorded"
        cutoff = date.today() - relativedelta(years=RMP_RESUBMISSION_YEARS)
        assert last_submission >= cutoff, (
            f"RMP resubmission overdue: last submission {last_submission}, "
            f"must be within {RMP_RESUBMISSION_YEARS} years — 40 CFR §68.190(b)"
        )

    def test_rmp_has_all_required_sections(self, entity_profile: dict):
        """§68.150: RMP must contain all 5 required sections."""
        rmp = entity_profile.get("rmp_submission", {})
        rmp_sections = frozenset(rmp.get("sections_present", []))
        missing = RMP_REQUIRED_SECTIONS - rmp_sections
        assert not missing, (
            f"RMP missing required sections: {sorted(missing)} — 40 CFR §68.150"
        )

    def test_rmp_revised_after_accidental_release(self, entity_profile: dict):
        """§68.190(c): RMP must be revised within 6 months after an accidental release
        that results in deaths, injuries, significant property damage, or evacuation."""
        from datetime import date
        from dateutil.relativedelta import relativedelta
        for accident in entity_profile.get("qualifying_rmp_accidents", []):
            accident_date = accident.get("date")
            revision_date = accident.get("rmp_revision_date")
            if accident_date:
                assert revision_date is not None, (
                    f"No RMP revision after qualifying accident on {accident_date} — "
                    f"40 CFR §68.190(c) requires revision within 6 months"
                )
                deadline = accident_date + relativedelta(months=6)
                assert revision_date <= deadline, (
                    f"RMP revision after accident on {accident_date} was {revision_date}, "
                    f"after the 6-month deadline {deadline} — 40 CFR §68.190(c)"
                )
```

---

## TestEmergencyResponseProgram

```python
class TestEmergencyResponseProgram:
    """40 CFR §68.95 — Emergency response program: written plan with required elements."""

    def test_emergency_response_plan_exists(self, program_2_or_3_scope, entity_profile: dict):
        """§68.95: Facilities with employees who will respond to accidental releases must have
        a written emergency response program."""
        erp = entity_profile.get("emergency_response_program", {})
        assert erp.get("written_plan_exists") is True, \
            "No written emergency response program — 40 CFR §68.95"

    def test_erp_coordinated_with_lepc(self, entity_profile: dict):
        """§68.95(c): Emergency response program must be coordinated with LEPC."""
        erp = entity_profile.get("emergency_response_program", {})
        assert erp.get("lepc_coordination_documented") is True, \
            "Emergency response program not coordinated with LEPC — 40 CFR §68.95(c)"

    def test_emergency_response_training_conducted(self, program_2_or_3_scope, entity_profile: dict):
        """§68.95(b): Employees responding to releases must be trained in the ERP."""
        for employee in entity_profile.get("emergency_response_employees", []):
            assert employee.get("erp_training_completed") is True, (
                f"Emergency responder '{employee.get('name', 'unknown')}' "
                f"has not completed ERP training — 40 CFR §68.95(b)"
            )
```
