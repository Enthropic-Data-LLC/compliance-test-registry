# EPA Clean Air Act — Title V Operating Permits / NSPS / NESHAP / CAM

**Framework:** Clean Air Act (42 U.S.C. §§7401–7671q) — 40 CFR Parts 60 (NSPS), 61/63 (NESHAP/MACT), 70 (Title V operating permits), 64 (CAM)
**Clauses:** §70.5 (Title V permit application deadline); §70.6 (permit required elements — 7-element checklist); Part 60 (NSPS — initial performance test within 60 days, excess emission reports); Part 63 (MACT — 120-day initial notification, initial compliance demonstration); §70.6(a)(3) (semi-annual compliance certification); §70.6(c)(1) (annual compliance certification)
**Confidence:** DETERMINISTIC-dominant (7-element permit required content; semi-annual and annual certification deadlines; NSPS 60-day initial performance test; MACT 120-day initial notification; permit deviation reporting 2-day/10-day; permit term 5-year maximum); PARAMETERIZED (emission limits are permit-specific; monitoring methodology per subpart; excess emission causation analysis); CONTESTED (potential to emit determination; Title V applicability at threshold margins)
**Last parsed:** 2026-05-21
**Applies to:** Major stationary sources subject to Title V operating permits (≥100 tpy criteria pollutants, or ≥10 tpy single HAP / ≥25 tpy combined HAPs); sources in categories subject to NSPS (40 CFR Part 60) or NESHAP/MACT standards (40 CFR Parts 61/63); area sources subject to MACT standards for certain HAP categories
**Trigger:** Potential to emit (PTE) at or above Title V major source thresholds; construction/modification/reconstruction of a listed NSPS source category after applicable date; location in a MACT-regulated source category; permit renewal every 5 years
**Jurisdiction:** United States; EPA enforces in non-delegated states; Title V operating permits issued by state/local air agencies under EPA-approved programs; EPA retains oversight and objection authority
**Not applicable to:** Minor sources below Title V thresholds (subject to state minor permit programs instead); area sources below MACT applicability thresholds (unless MACT area source standard issued); emergency generators used exclusively for emergencies (may have RICE NESHAP exemptions); research and development facilities meeting §112(c)(7) requirements

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def clean_air_act_scope(entity_profile: dict):
    subject = (
        entity_profile.get("title_v_major_source", False)
        or entity_profile.get("subject_to_nsps", False)
        or entity_profile.get("subject_to_mact", False)
    )
    if not subject:
        pytest.skip(
            "EPA Clean Air Act operating permit/NSPS/NESHAP requirements do not apply — "
            "facility is not a Title V major source and not in a listed NSPS/MACT category."
        )

@pytest.fixture
def title_v_scope(entity_profile: dict):
    if not entity_profile.get("title_v_major_source", False):
        pytest.skip("Title V operating permit obligations apply only to major sources.")

@pytest.fixture
def nsps_scope(entity_profile: dict):
    if not entity_profile.get("subject_to_nsps", False):
        pytest.skip("NSPS (40 CFR Part 60) requirements apply only to listed source categories.")

@pytest.fixture
def mact_scope(entity_profile: dict):
    if not entity_profile.get("subject_to_mact", False):
        pytest.skip("MACT/NESHAP (40 CFR Part 63) requirements apply only to listed HAP source categories.")
```

---

## Constants

```python
from typing import FrozenSet

# ── Title V permit term ───────────────────────────────────────────────────────

TITLE_V_MAX_PERMIT_TERM_YEARS = 5
TITLE_V_RENEWAL_APPLICATION_MONTHS_BEFORE_EXPIRY = 6

# ── Permit deviation reporting ────────────────────────────────────────────────

TITLE_V_DEVIATION_VERBAL_REPORT_BUSINESS_DAYS = 2
TITLE_V_DEVIATION_WRITTEN_REPORT_DAYS = 10

# ── Compliance certification frequency ────────────────────────────────────────

TITLE_V_SEMI_ANNUAL_CERTIFICATION_MONTHS = 6
TITLE_V_ANNUAL_CERTIFICATION_MONTHS = 12

# ── NSPS ──────────────────────────────────────────────────────────────────────

NSPS_INITIAL_PERFORMANCE_TEST_DAYS_FROM_STARTUP = 60

# ── MACT/NESHAP ───────────────────────────────────────────────────────────────

MACT_INITIAL_NOTIFICATION_DAYS = 120  # After source becomes subject to standard

# ── Title V permit required content (40 CFR §70.6) ───────────────────────────

TITLE_V_PERMIT_REQUIRED_ELEMENTS: FrozenSet[str] = frozenset({
    "emission_limitations_and_standards",
    "operational_requirements_and_limitations",
    "compliance_schedule_if_applicable",
    "monitoring_and_recordkeeping_requirements",
    "reporting_requirements_semi_annual_minimum",
    "annual_compliance_certification_by_responsible_official",
    "permit_shield_confirmation",
})
```

---

## TestTitleVPermit

```python
class TestTitleVPermit:
    """40 CFR Part 70 — Title V operating permit: existence, content, and compliance."""

    def test_title_v_permit_exists(self, title_v_scope, entity_profile: dict):
        """§70.5: Major source must hold a Title V operating permit."""
        permit = entity_profile.get("title_v_permit", {})
        assert permit.get("exists") is True, \
            "No Title V operating permit found — major source must obtain permit (40 CFR §70.5)"

    def test_permit_not_expired(self, title_v_scope, entity_profile: dict):
        """§70.6(a)(2): Title V permit term shall not exceed 5 years."""
        from datetime import date
        from dateutil.relativedelta import relativedelta
        permit = entity_profile.get("title_v_permit", {})
        expiry = permit.get("expiration_date")
        assert expiry is not None, "Title V permit expiration date not recorded"
        assert expiry >= date.today(), \
            f"Title V permit expired on {expiry} — permit must be renewed (40 CFR §70.6(a)(2))"

    def test_renewal_application_submitted_timely(self, title_v_scope, entity_profile: dict):
        """§70.5(a)(1)(iii): Renewal application must be submitted at least 6 months
        before permit expiration."""
        from datetime import date
        from dateutil.relativedelta import relativedelta
        permit = entity_profile.get("title_v_permit", {})
        expiry = permit.get("expiration_date")
        renewal_submitted = permit.get("renewal_application_submitted_date")
        if expiry and (date.today() > expiry - relativedelta(months=8)):
            assert renewal_submitted is not None, \
                f"Title V renewal application must be submitted ≥6 months before expiry {expiry}"
            deadline = expiry - relativedelta(months=TITLE_V_RENEWAL_APPLICATION_MONTHS_BEFORE_EXPIRY)
            assert renewal_submitted <= deadline, (
                f"Renewal application submitted {renewal_submitted} is later than "
                f"the 6-month-before-expiry deadline {deadline} — 40 CFR §70.5(a)(1)(iii)"
            )

    def test_permit_contains_all_required_elements(self, title_v_scope, entity_profile: dict):
        """§70.6: Title V permit must contain all 7 required elements."""
        permit = entity_profile.get("title_v_permit", {})
        permit_elements = frozenset(permit.get("elements_present", []))
        missing = TITLE_V_PERMIT_REQUIRED_ELEMENTS - permit_elements
        assert not missing, (
            f"Title V permit missing required elements: {sorted(missing)} — 40 CFR §70.6"
        )

    def test_semi_annual_compliance_certification_submitted(self, title_v_scope, entity_profile: dict):
        """§70.6(a)(3)(iii)(A): Compliance certification must be submitted at least semi-annually."""
        from datetime import date
        from dateutil.relativedelta import relativedelta
        last_cert = entity_profile.get("last_compliance_certification_date")
        assert last_cert is not None, \
            "No compliance certification on record — 40 CFR §70.6(a)(3)(iii)(A)"
        six_months_ago = date.today() - relativedelta(months=TITLE_V_SEMI_ANNUAL_CERTIFICATION_MONTHS)
        assert last_cert >= six_months_ago, (
            f"Compliance certification overdue: last certification {last_cert}, "
            f"must be within 6 months — 40 CFR §70.6(a)(3)(iii)(A)"
        )

    def test_permit_deviations_reported_timely(self, title_v_scope, entity_profile: dict):
        """§70.6(a)(3)(iii)(B): Permit deviations must be reported — verbal within 2 business days,
        written within 10 days."""
        for deviation in entity_profile.get("permit_deviations", []):
            dev_id = deviation.get("id", "unknown")
            detected = deviation.get("detection_date")
            verbal_date = deviation.get("verbal_report_date")
            written_date = deviation.get("written_report_date")
            if detected:
                if verbal_date:
                    business_days = deviation.get("business_days_to_verbal_report", 0)
                    assert business_days <= TITLE_V_DEVIATION_VERBAL_REPORT_BUSINESS_DAYS, (
                        f"Deviation '{dev_id}' verbal report was {business_days} business days "
                        f"after detection — must be within 2 business days (§70.6(a)(3)(iii)(B))"
                    )
                if written_date:
                    days = (written_date - detected).days
                    assert days <= TITLE_V_DEVIATION_WRITTEN_REPORT_DAYS, (
                        f"Deviation '{dev_id}' written report was {days} days after detection — "
                        f"must be within 10 days (§70.6(a)(3)(iii)(B))"
                    )
```

---

## TestEmissionLimitCompliance

```python
class TestEmissionLimitCompliance:
    """Permit-specific emission limits — any single exceedance is a DETERMINISTIC violation."""

    def test_no_daily_maximum_exceedances(self, entity_profile: dict):
        """Title V permit conditions: daily maximum effluent limits may not be exceeded
        on any single day."""
        for limit in entity_profile.get("emission_limits", []):
            violations = limit.get("daily_maximum_exceedances", [])
            assert not violations, (
                f"Emission limit '{limit.get('pollutant', 'unknown')}' at "
                f"'{limit.get('unit_id', 'unknown')}': {len(violations)} daily maximum "
                f"exceedance(s) — each is a permit violation"
            )

    def test_no_monthly_average_exceedances(self, entity_profile: dict):
        """Title V permit conditions: monthly average emission limits may not be exceeded."""
        for limit in entity_profile.get("emission_limits", []):
            monthly_violations = limit.get("monthly_average_exceedances", [])
            assert not monthly_violations, (
                f"Emission limit '{limit.get('pollutant', 'unknown')}' at "
                f"'{limit.get('unit_id', 'unknown')}': {len(monthly_violations)} monthly "
                f"average exceedance(s) — each is a permit violation"
            )
```

---

## TestNSPS

```python
class TestNSPS:
    """40 CFR Part 60 — New Source Performance Standards."""

    def test_initial_performance_test_within_60_days(self, nsps_scope, entity_profile: dict):
        """40 CFR §60.8: Initial performance test required within 60 days of achieving
        maximum production rate (not later than 180 days after initial startup)."""
        for unit in entity_profile.get("nsps_affected_units", []):
            startup_date = unit.get("initial_startup_date")
            test_date = unit.get("initial_performance_test_date")
            if startup_date:
                assert test_date is not None, (
                    f"NSPS unit '{unit.get('id', 'unknown')}' has no initial performance test — "
                    f"required within 60 days of max production rate (40 CFR §60.8)"
                )

    def test_excess_emission_reports_submitted(self, nsps_scope, entity_profile: dict):
        """40 CFR §60.7(c): Excess emission reports must be submitted quarterly or
        semi-annually per applicable subpart."""
        for report in entity_profile.get("nsps_excess_emission_reports", []):
            assert report.get("submitted") is True, (
                f"NSPS excess emission report for period '{report.get('period', 'unknown')}' "
                f"not submitted — 40 CFR §60.7(c)"
            )
```

---

## TestMACTNESHAP

```python
class TestMACTNESHAP:
    """40 CFR Parts 61/63 — NESHAP / MACT initial notification and compliance."""

    def test_initial_notification_within_120_days(self, mact_scope, entity_profile: dict):
        """40 CFR §63.9(b): Initial notification must be submitted to state agency and EPA
        within 120 days of becoming subject to a MACT standard."""
        for standard in entity_profile.get("applicable_mact_standards", []):
            subject_date = standard.get("date_became_subject")
            notification_date = standard.get("initial_notification_date")
            if subject_date:
                assert notification_date is not None, (
                    f"No initial notification for MACT standard "
                    f"'{standard.get('subpart', 'unknown')}' — 40 CFR §63.9(b)"
                )
                days_elapsed = (notification_date - subject_date).days
                assert days_elapsed <= MACT_INITIAL_NOTIFICATION_DAYS, (
                    f"MACT initial notification for '{standard.get('subpart', 'unknown')}' "
                    f"was {days_elapsed} days after becoming subject — must be within "
                    f"{MACT_INITIAL_NOTIFICATION_DAYS} days (40 CFR §63.9(b))"
                )

    def test_initial_compliance_demonstration_completed(self, mact_scope, entity_profile: dict):
        """40 CFR §63.7: Initial compliance demonstration must be completed by compliance date."""
        for standard in entity_profile.get("applicable_mact_standards", []):
            assert standard.get("initial_compliance_demonstrated") is True, (
                f"Initial compliance demonstration not completed for MACT standard "
                f"'{standard.get('subpart', 'unknown')}' — 40 CFR §63.7"
            )

    def test_periodic_compliance_reports_submitted(self, mact_scope, entity_profile: dict):
        """40 CFR §63.10: Periodic compliance reports must be submitted per subpart schedule."""
        for report in entity_profile.get("mact_compliance_reports", []):
            assert report.get("submitted_on_time") is True, (
                f"MACT compliance report for '{report.get('subpart', 'unknown')}' "
                f"period '{report.get('period', 'unknown')}' not submitted on time — "
                f"40 CFR §63.10"
            )
```
