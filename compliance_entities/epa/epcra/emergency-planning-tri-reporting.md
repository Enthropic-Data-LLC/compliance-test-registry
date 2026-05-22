# EPA EPCRA / SARA Title III — Emergency Planning and TRI Reporting

**Framework:** Emergency Planning and Community Right-to-Know Act (42 U.S.C. §§11001–11050 / SARA Title III) — 40 CFR Parts 355, 370, 372
**Clauses:** §302 (emergency planning — TPQ notification); §304 (emergency release notification — 15-minute/1-hour reporting); §311/312 (Tier I/II hazardous chemical reporting — March 1); §313 (TRI Form R / Form A — July 1)
**Confidence:** DETERMINISTIC-dominant (TPQ thresholds; reporting deadlines — March 1, July 1; §304 15-minute notification; §311 SDS threshold quantities; §313 employee count and quantity thresholds); PARAMETERIZED (TPQ quantity determination methodology; TRI chemical activity coding)
**Last parsed:** 2026-05-21
**Applies to:** Facilities with extremely hazardous substances (EHS) above threshold planning quantities (§302); facilities required to have SDS under OSHA HazCom with chemicals above §311 thresholds; facilities meeting §313 TRI criteria (≥10 FTE, covered SIC/NAICS, chemical above manufacturing/processing/otherwise-use threshold)
**Trigger:** Any EHS at or above its TPQ triggers §302 planning obligations; OSHA HazCom SDS requirement + quantity thresholds triggers §311/312; ≥10 employees + covered industry + TRI chemical above applicable threshold triggers §313 Form R
**Jurisdiction:** United States federal; EPA enforces §304 release notifications; LEPCs (Local Emergency Planning Committees) receive emergency planning data; state emergency response commissions (SERCs) coordinate
**Not applicable to:** Transportation of hazardous chemicals (§327 transportation exemption for §311/312 and §313 during transport); agricultural operations (§311/312 farm exemption); chemicals at facilities below all applicable thresholds; chemicals not on applicable EHS, OSHA HazCom, or TRI chemical lists

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def epcra_scope(entity_profile: dict):
    if not entity_profile.get("subject_to_any_epcra_section", False):
        pytest.skip(
            "EPCRA / SARA Title III does not apply — facility has no EHS above TPQ, "
            "no OSHA HazCom chemicals above §311 thresholds, and does not meet §313 TRI criteria."
        )
```

---

## Constants

```python
from datetime import date
from typing import FrozenSet

# ── §302 / §304 thresholds ────────────────────────────────────────────────────

# TPQ notification deadline: within 60 days of exceeding TPQ (§302)
EPCRA_302_NOTIFICATION_DAYS = 60

# §304 release notification timelines
EPCRA_304_IMMEDIATE_NOTIFICATION_MINUTES = 15  # If EHS release exceeds reportable quantity
EPCRA_304_WRITTEN_FOLLOW_UP_DAYS = 30          # Written follow-up report to SERC/LEPC

# ── §312 Tier II reporting deadline ───────────────────────────────────────────

EPCRA_312_ANNUAL_REPORT_DEADLINE_MONTH = 3   # March 1
EPCRA_312_ANNUAL_REPORT_DEADLINE_DAY = 1

# ── §313 TRI reporting deadline ───────────────────────────────────────────────

EPCRA_313_FORM_R_DEADLINE_MONTH = 7   # July 1
EPCRA_313_FORM_R_DEADLINE_DAY = 1

# ── §313 TRI eligibility thresholds ───────────────────────────────────────────

EPCRA_313_EMPLOYEE_THRESHOLD = 10
EPCRA_313_MANUFACTURING_THRESHOLD_LBS = 25000
EPCRA_313_PROCESSING_THRESHOLD_LBS = 25000
EPCRA_313_OTHERWISE_USE_THRESHOLD_LBS = 10000

# ── §312 Tier II required data elements ───────────────────────────────────────

TIER_II_REQUIRED_FIELDS: FrozenSet[str] = frozenset({
    "chemical_name_or_common_name",
    "cas_number",
    "maximum_amount_on_site_during_year",
    "average_daily_amount",
    "number_of_days_on_site",
    "storage_location_description",
    "physical_and_health_hazards",
    "storage_codes_and_conditions",
})
```

---

## TestSection302EmergencyPlanning

```python
class TestSection302EmergencyPlanning:
    """EPCRA §302 — Emergency planning notification when EHS present at or above TPQ."""

    def test_serc_and_lepc_notified_within_60_days_of_tpq(self, entity_profile: dict):
        """§302(c): Facilities with EHS at or above TPQ must notify SERC and LEPC
        within 60 days of first reaching or exceeding TPQ."""
        if not entity_profile.get("has_ehs_above_tpq", False):
            pytest.skip("No EHS present at or above TPQ — §302 notification not required")
        notification = entity_profile.get("section_302_notification", {})
        assert notification.get("serc_notified") is True, \
            "SERC not notified of EHS presence — EPCRA §302(c)"
        assert notification.get("lepc_notified") is True, \
            "LEPC not notified of EHS presence — EPCRA §302(c)"
        first_tpq_date = entity_profile.get("date_tpq_first_exceeded")
        if first_tpq_date:
            notified_date = notification.get("notification_date")
            assert notified_date is not None, "Notification date not recorded"
            days_elapsed = (notified_date - first_tpq_date).days
            assert days_elapsed <= EPCRA_302_NOTIFICATION_DAYS, (
                f"§302 notification was {days_elapsed} days after TPQ was exceeded — "
                f"must be within {EPCRA_302_NOTIFICATION_DAYS} days (EPCRA §302(c))"
            )

    def test_emergency_coordinator_designated(self, entity_profile: dict):
        """§303(d): Facility must designate an emergency coordinator and notify LEPC."""
        if not entity_profile.get("has_ehs_above_tpq", False):
            pytest.skip("Applies when EHS present at or above TPQ")
        assert entity_profile.get("emergency_coordinator_designated") is True, \
            "Emergency coordinator not designated — EPCRA §303(d)"

    def test_tpq_change_notification_within_60_days(self, entity_profile: dict):
        """§302(c): If TPQ status changes (new chemical, quantity change), notify LEPC
        within 60 days."""
        for change in entity_profile.get("tpq_status_changes", []):
            change_date = change.get("date")
            notification_date = change.get("lepc_notified_date")
            if change_date and notification_date:
                days = (notification_date - change_date).days
                assert days <= EPCRA_302_NOTIFICATION_DAYS, (
                    f"TPQ change for '{change.get('chemical', 'unknown')}' not reported "
                    f"to LEPC within 60 days ({days} days elapsed) — EPCRA §302(c)"
                )
```

---

## TestSection304EmergencyReleaseNotification

```python
class TestSection304EmergencyReleaseNotification:
    """EPCRA §304 — Immediate emergency notification for EHS releases above reportable quantity."""

    def test_immediate_notification_within_15_minutes(self, entity_profile: dict):
        """§304(b): Facility must immediately notify SERC and LEPC when an EHS (or CERCLA
        hazardous substance) is released in a quantity equal to or greater than the
        reportable quantity (RQ). 'Immediately' interpreted as ~15 minutes."""
        for incident in entity_profile.get("release_incidents", []):
            if not incident.get("above_reportable_quantity"):
                continue
            release_time = incident.get("release_detected_time")
            notification_time = incident.get("emergency_notification_time")
            if release_time and notification_time:
                minutes_elapsed = (notification_time - release_time).total_seconds() / 60
                assert minutes_elapsed <= EPCRA_304_IMMEDIATE_NOTIFICATION_MINUTES, (
                    f"Incident '{incident.get('id', 'unknown')}': emergency notification "
                    f"was {minutes_elapsed:.1f} minutes after detection — "
                    f"§304(b) requires immediate notification (within ~15 minutes)"
                )

    def test_written_follow_up_report_within_30_days(self, entity_profile: dict):
        """§304(c): Written follow-up report must be submitted to SERC and LEPC
        within 30 days of the emergency release."""
        for incident in entity_profile.get("release_incidents", []):
            if not incident.get("above_reportable_quantity"):
                continue
            release_date = incident.get("release_date")
            followup_date = incident.get("written_followup_submitted_date")
            if release_date:
                assert followup_date is not None, (
                    f"No written follow-up report for incident '{incident.get('id', 'unknown')}' "
                    f"— §304(c) requires report within 30 days"
                )
                days_elapsed = (followup_date - release_date).days
                assert days_elapsed <= EPCRA_304_WRITTEN_FOLLOW_UP_DAYS, (
                    f"Written follow-up for incident '{incident.get('id', 'unknown')}' "
                    f"was {days_elapsed} days after release — must be within 30 days (§304(c))"
                )
```

---

## TestSection312TierIIReporting

```python
class TestSection312TierIIReporting:
    """EPCRA §312 — Annual Tier II hazardous chemical inventory report by March 1."""

    def test_tier_ii_submitted_by_march_1(self, entity_profile: dict):
        """§312: Tier II reports must be submitted to SERC, LEPC, and local fire department
        annually by March 1."""
        if not entity_profile.get("subject_to_section_312", False):
            pytest.skip("Facility not subject to §312 — no OSHA HazCom chemicals above thresholds")
        for report_year in entity_profile.get("tier_ii_report_years", []):
            year = report_year.get("year")
            submitted_date = report_year.get("submission_date")
            deadline = date(year, EPCRA_312_ANNUAL_REPORT_DEADLINE_MONTH,
                           EPCRA_312_ANNUAL_REPORT_DEADLINE_DAY)
            assert submitted_date is not None, \
                f"Tier II report for year {year} not submitted — EPCRA §312"
            assert submitted_date <= deadline, (
                f"Tier II report for year {year} submitted {submitted_date}, "
                f"after March 1 deadline {deadline} — EPCRA §312"
            )

    def test_tier_ii_includes_all_required_fields(self, entity_profile: dict):
        """§312: Tier II report must include specific data elements for each hazardous chemical."""
        if not entity_profile.get("subject_to_section_312", False):
            pytest.skip("Applies when subject to §312")
        for chemical in entity_profile.get("tier_ii_chemicals", []):
            reported_fields = frozenset(chemical.get("reported_fields", []))
            missing = TIER_II_REQUIRED_FIELDS - reported_fields
            assert not missing, (
                f"Tier II entry for '{chemical.get('name', 'unknown')}' missing required "
                f"fields: {sorted(missing)} — EPCRA §312"
            )
```

---

## TestSection313TRIReporting

```python
class TestSection313TRIReporting:
    """EPCRA §313 — TRI Form R / Form A annual toxic chemical release inventory by July 1."""

    def test_tri_eligibility_correctly_determined(self, entity_profile: dict):
        """§313(b): TRI reporting required if: ≥10 FTE employees AND covered SIC/NAICS code
        AND manufactures/processes/otherwise uses a listed TRI chemical above threshold."""
        if not entity_profile.get("subject_to_section_313", False):
            pytest.skip("Facility not subject to §313 TRI reporting")
        assert entity_profile.get("employee_count", 0) >= EPCRA_313_EMPLOYEE_THRESHOLD, (
            f"§313 requires ≥{EPCRA_313_EMPLOYEE_THRESHOLD} FTE employees — "
            f"facility has {entity_profile.get('employee_count')} employees"
        )

    def test_form_r_submitted_by_july_1(self, entity_profile: dict):
        """§313: Form R (or Form A for de minimis releases) must be submitted to EPA
        and state by July 1 annually."""
        if not entity_profile.get("subject_to_section_313", False):
            pytest.skip("Applies when subject to §313")
        for report_year in entity_profile.get("tri_report_years", []):
            year = report_year.get("year")
            submitted_date = report_year.get("submission_date")
            deadline = date(year, EPCRA_313_FORM_R_DEADLINE_MONTH,
                           EPCRA_313_FORM_R_DEADLINE_DAY)
            assert submitted_date is not None, \
                f"TRI Form R for year {year} not submitted — EPCRA §313"
            assert submitted_date <= deadline, (
                f"TRI Form R for year {year} submitted {submitted_date}, "
                f"after July 1 deadline {deadline} — EPCRA §313"
            )

    def test_tri_form_r_filed_for_each_eligible_chemical(self, entity_profile: dict):
        """§313: A separate Form R is required for each TRI-listed chemical above
        the applicable activity threshold."""
        if not entity_profile.get("subject_to_section_313", False):
            pytest.skip("Applies when subject to §313")
        for chemical in entity_profile.get("tri_eligible_chemicals", []):
            assert chemical.get("form_r_or_a_filed") is True, (
                f"No Form R/A filed for TRI-eligible chemical "
                f"'{chemical.get('name', 'unknown')}' — EPCRA §313"
            )

    def test_tri_records_retained_three_years(self, entity_profile: dict):
        """§313(h)(2): Facilities must retain TRI records for 3 years."""
        if not entity_profile.get("subject_to_section_313", False):
            pytest.skip("Applies when subject to §313")
        assert entity_profile.get("tri_record_retention_years", 0) >= 3, \
            "TRI records must be retained for 3 years — EPCRA §313(h)(2)"
```
