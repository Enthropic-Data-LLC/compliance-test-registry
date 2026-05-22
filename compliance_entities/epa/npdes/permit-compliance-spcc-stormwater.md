# EPA Clean Water Act — NPDES Permit Compliance, SPCC, and Stormwater

**Framework:** Clean Water Act (33 U.S.C. §§1251–1387) — 40 CFR Part 122 (NPDES), 40 CFR Part 112 (SPCC), 40 CFR Part 117 (reportable quantities), 40 CFR Part 136 (test methods)
**Clauses:** §402 (NPDES permit program); §122.41 (standard permit conditions — including DMR deadlines, noncompliance notification); §112.3 (SPCC applicability thresholds); §112.7 (SPCC plan requirements); 40 CFR Parts 122/123 (multi-sector general permit / industrial stormwater)
**Confidence:** DETERMINISTIC-dominant (permit effluent limits — any exceedance is a violation; DMR 28-day submission deadline; noncompliance verbal 24-hour / written 5-day notification; SPCC applicability thresholds; annual comprehensive site inspection; quarterly visual stormwater assessment); PARAMETERIZED (permit effluent limit values are permit-specific; monitoring method per effluent guideline); CONTESTED (WOTUS jurisdictional determination; bypass/upset affirmative defense conditions)
**Last parsed:** 2026-05-21
**Applies to:** Any facility discharging pollutants from a point source to waters of the United States requires an NPDES permit; facilities with aboveground oil storage ≥1,320 gallons (or underground ≥42,000 gallons) that could reasonably discharge oil to navigable waters require an SPCC plan; industrial facilities discharging stormwater to waters of the US under Phase I/II MSGP
**Trigger:** Discharge of any pollutant from a point source to WOTUS triggers NPDES permit requirement; oil storage above SPCC thresholds triggers SPCC plan; industrial activity categories subject to stormwater MSGP
**Jurisdiction:** United States; EPA enforces in non-delegated states; most states have NPDES delegation (40 states); Army Corps issues §404 dredge/fill permits
**Not applicable to:** Discharges to publicly owned treatment works (POTW) — regulated by pretreatment standards (40 CFR Part 403); discharges not to WOTUS (to groundwater only, or to isolated waters not WOTUS); SPCC exemption for facilities that cannot reasonably discharge to navigable waters (physical geography); agricultural stormwater discharges (§402(l)(1) exemption)

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def cwa_scope(entity_profile: dict):
    subject = (
        entity_profile.get("has_npdes_permit", False)
        or entity_profile.get("subject_to_spcc", False)
        or entity_profile.get("subject_to_stormwater_msgp", False)
    )
    if not subject:
        pytest.skip(
            "CWA NPDES/SPCC/stormwater requirements do not apply — facility has no NPDES permit, "
            "no SPCC-triggering oil storage, and no industrial stormwater discharge to WOTUS."
        )

@pytest.fixture
def npdes_scope(entity_profile: dict):
    if not entity_profile.get("has_npdes_permit", False):
        pytest.skip("Facility does not have an NPDES permit.")

@pytest.fixture
def spcc_scope(entity_profile: dict):
    if not entity_profile.get("subject_to_spcc", False):
        pytest.skip("SPCC requirements do not apply — oil storage below thresholds.")

@pytest.fixture
def stormwater_scope(entity_profile: dict):
    if not entity_profile.get("subject_to_stormwater_msgp", False):
        pytest.skip("Industrial stormwater MSGP does not apply.")
```

---

## Constants

```python
from typing import FrozenSet

# ── SPCC thresholds (40 CFR §112.1(d)(2)) ────────────────────────────────────

SPCC_ABOVEGROUND_THRESHOLD_GALLONS = 1320   # Any single AST ≥ 660 gal, or aggregate ≥ 1,320 gal
SPCC_UNDERGROUND_THRESHOLD_GALLONS = 42000  # For underground storage tanks

# ── DMR submission deadline ───────────────────────────────────────────────────

NPDES_DMR_SUBMISSION_DAYS_AFTER_PERIOD_END = 28

# ── Noncompliance notification ────────────────────────────────────────────────

NPDES_NONCOMPLIANCE_VERBAL_HOURS = 24
NPDES_NONCOMPLIANCE_WRITTEN_DAYS = 5

# ── SPCC plan amendment timelines (40 CFR §112.5(a)) ─────────────────────────

SPCC_PLAN_AMENDMENT_DAYS_AFTER_CHANGE = 60     # Amendment required within 60 days
SPCC_PE_CERTIFICATION_REQUIRED = True           # PE must certify SPCC plan (certain exemptions for SQF)

# ── SPCC five-year review (40 CFR §112.5(b)) ─────────────────────────────────

SPCC_REVIEW_INTERVAL_YEARS = 5

# ── SPCC drill/inspection frequency ──────────────────────────────────────────

SPCC_SECONDARY_CONTAINMENT_TEST_FREQUENCY = "periodic"   # PARAMETERIZED — frequency per plan

# ── Industrial stormwater MSGP ────────────────────────────────────────────────

STORMWATER_ANNUAL_SITE_INSPECTION_MONTHS = 12
STORMWATER_QUARTERLY_VISUAL_ASSESSMENT_MONTHS = 3

# ── SPCC required plan elements (40 CFR §112.7) ──────────────────────────────

SPCC_REQUIRED_PLAN_ELEMENTS: FrozenSet[str] = frozenset({
    "facility_description_and_oil_storage_locations",
    "discharge_response_procedures",
    "inspection_and_testing_program",
    "personnel_training_and_oil_spill_prevention_briefings",
    "security_provisions",
    "secondary_containment_design",
    "loading_and_unloading_procedures",
    "tank_integrity_testing_program",
    "emergency_contact_information",
})
```

---

## TestNPDESPermitCompliance

```python
class TestNPDESPermitCompliance:
    """40 CFR §122.41 — NPDES permit standard conditions: effluent limits and reporting."""

    def test_no_daily_maximum_exceedances(self, npdes_scope, entity_profile: dict):
        """§122.41(a): Permit holder must comply with all conditions of the permit.
        Any single day exceeding a daily maximum limit is a permit violation."""
        for limit in entity_profile.get("npdes_effluent_limits", []):
            violations = limit.get("daily_maximum_exceedances", [])
            assert not violations, (
                f"NPDES effluent limit for '{limit.get('pollutant', 'unknown')}' at "
                f"outfall '{limit.get('outfall', 'unknown')}': {len(violations)} daily "
                f"maximum exceedance(s) — each is a permit violation (40 CFR §122.41(a))"
            )

    def test_no_monthly_average_exceedances(self, npdes_scope, entity_profile: dict):
        """§122.41(a): Monthly average effluent limits may not be exceeded."""
        for limit in entity_profile.get("npdes_effluent_limits", []):
            monthly_violations = limit.get("monthly_average_exceedances", [])
            assert not monthly_violations, (
                f"NPDES monthly average exceedance(s) for '{limit.get('pollutant', 'unknown')}' "
                f"at outfall '{limit.get('outfall', 'unknown')}' — 40 CFR §122.41(a)"
            )

    def test_dmr_submitted_within_28_days(self, npdes_scope, entity_profile: dict):
        """§122.41(l)(4): Discharge Monitoring Reports (DMRs) must be submitted within
        28 days of the end of the reporting period."""
        from datetime import date
        for dmr in entity_profile.get("discharge_monitoring_reports", []):
            period_end = dmr.get("reporting_period_end")
            submitted = dmr.get("submission_date")
            if period_end:
                assert submitted is not None, (
                    f"DMR for period ending {period_end} not submitted — "
                    f"must be submitted within 28 days (40 CFR §122.41(l)(4))"
                )
                days_to_submit = (submitted - period_end).days
                assert days_to_submit <= NPDES_DMR_SUBMISSION_DAYS_AFTER_PERIOD_END, (
                    f"DMR for period ending {period_end} submitted {days_to_submit} days late — "
                    f"must be within {NPDES_DMR_SUBMISSION_DAYS_AFTER_PERIOD_END} days "
                    f"(40 CFR §122.41(l)(4))"
                )

    def test_noncompliance_verbal_notification_within_24_hours(self, npdes_scope, entity_profile: dict):
        """§122.41(l)(6)(i): Oral notification to EPA/state within 24 hours of becoming
        aware of noncompliance with permit conditions posing serious threat or certain violations."""
        for incident in entity_profile.get("noncompliance_incidents", []):
            if not incident.get("requires_immediate_notification"):
                continue
            detected = incident.get("detected_datetime")
            verbal = incident.get("verbal_notification_datetime")
            if detected and verbal:
                hours = (verbal - detected).total_seconds() / 3600
                assert hours <= NPDES_NONCOMPLIANCE_VERBAL_HOURS, (
                    f"Noncompliance incident '{incident.get('id', 'unknown')}': verbal "
                    f"notification was {hours:.1f} hours after detection — must be within "
                    f"{NPDES_NONCOMPLIANCE_VERBAL_HOURS} hours (40 CFR §122.41(l)(6)(i))"
                )

    def test_noncompliance_written_report_within_5_days(self, npdes_scope, entity_profile: dict):
        """§122.41(l)(6)(ii): Written report within 5 days of verbal notification."""
        for incident in entity_profile.get("noncompliance_incidents", []):
            if not incident.get("requires_immediate_notification"):
                continue
            verbal = incident.get("verbal_notification_date")
            written = incident.get("written_report_date")
            if verbal:
                assert written is not None, (
                    f"No written noncompliance report for incident '{incident.get('id', 'unknown')}' "
                    f"— required within 5 days of verbal notification (§122.41(l)(6)(ii))"
                )
                days = (written - verbal).days
                assert days <= NPDES_NONCOMPLIANCE_WRITTEN_DAYS, (
                    f"Written noncompliance report for '{incident.get('id', 'unknown')}' "
                    f"was {days} days after verbal notification — must be within "
                    f"{NPDES_NONCOMPLIANCE_WRITTEN_DAYS} days (§122.41(l)(6)(ii))"
                )
```

---

## TestSPCCPlan

```python
class TestSPCCPlan:
    """40 CFR Part 112 — Spill Prevention, Control, and Countermeasure (SPCC) plan."""

    def test_spcc_plan_exists(self, spcc_scope, entity_profile: dict):
        """§112.3: Facility with oil storage above SPCC thresholds must have an SPCC plan."""
        assert entity_profile.get("spcc_plan", {}).get("exists") is True, \
            "No SPCC plan found — required for facilities above oil storage thresholds (40 CFR §112.3)"

    def test_spcc_plan_pe_certified(self, spcc_scope, entity_profile: dict):
        """§112.3(d): SPCC plan must be certified by a licensed Professional Engineer (PE).
        Qualified Facility self-certification exemption applies to smaller facilities."""
        plan = entity_profile.get("spcc_plan", {})
        if entity_profile.get("qualified_facility_self_certification_eligible", False):
            assert plan.get("owner_operator_certified") is True, \
                "Qualified Facility SPCC plan must be owner/operator certified — 40 CFR §112.6"
        else:
            assert plan.get("pe_certified") is True, \
                "SPCC plan must be certified by a Professional Engineer — 40 CFR §112.3(d)"

    def test_spcc_plan_has_required_elements(self, spcc_scope, entity_profile: dict):
        """§112.7: SPCC plan must contain all required elements."""
        plan = entity_profile.get("spcc_plan", {})
        plan_elements = frozenset(plan.get("elements_present", []))
        missing = SPCC_REQUIRED_PLAN_ELEMENTS - plan_elements
        assert not missing, (
            f"SPCC plan missing required elements: {sorted(missing)} — 40 CFR §112.7"
        )

    def test_spcc_plan_reviewed_every_5_years(self, spcc_scope, entity_profile: dict):
        """§112.5(b): SPCC plan must be reviewed at least once every 5 years."""
        from datetime import date
        from dateutil.relativedelta import relativedelta
        plan = entity_profile.get("spcc_plan", {})
        last_review = plan.get("last_review_date")
        assert last_review is not None, \
            "No SPCC plan review date recorded — 40 CFR §112.5(b) requires 5-year review"
        cutoff = date.today() - relativedelta(years=SPCC_REVIEW_INTERVAL_YEARS)
        assert last_review >= cutoff, (
            f"SPCC plan review overdue: last review {last_review}, "
            f"must be within {SPCC_REVIEW_INTERVAL_YEARS} years — 40 CFR §112.5(b)"
        )

    def test_spcc_plan_amended_within_60_days_of_change(self, spcc_scope, entity_profile: dict):
        """§112.5(a): SPCC plan must be amended within 60 days of any change that materially
        affects the potential for oil discharge."""
        for change in entity_profile.get("facility_changes_requiring_spcc_amendment", []):
            change_date = change.get("date")
            amendment_date = change.get("spcc_amendment_date")
            if change_date:
                assert amendment_date is not None, (
                    f"No SPCC plan amendment for facility change "
                    f"'{change.get('description', 'unknown')}' on {change_date} — "
                    f"40 CFR §112.5(a)"
                )
                days = (amendment_date - change_date).days
                assert days <= SPCC_PLAN_AMENDMENT_DAYS_AFTER_CHANGE, (
                    f"SPCC plan amendment for change '{change.get('description', 'unknown')}' "
                    f"was {days} days after the change — must be within "
                    f"{SPCC_PLAN_AMENDMENT_DAYS_AFTER_CHANGE} days (40 CFR §112.5(a))"
                )
```

---

## TestIndustrialStormwater

```python
class TestIndustrialStormwater:
    """MSGP — Industrial Stormwater Multi-Sector General Permit: SWPPP and inspections."""

    def test_swppp_exists_and_site_specific(self, stormwater_scope, entity_profile: dict):
        """MSGP §3.1: Stormwater Pollution Prevention Plan (SWPPP) required;
        must be site-specific and current."""
        swppp = entity_profile.get("swppp", {})
        assert swppp.get("exists") is True, \
            "No SWPPP found — required for industrial stormwater discharges under MSGP §3.1"
        assert swppp.get("site_specific") is True, \
            "SWPPP must be site-specific — MSGP §3.1"

    def test_annual_comprehensive_site_inspection_completed(self, stormwater_scope, entity_profile: dict):
        """MSGP §4.1: Comprehensive site inspection required at least annually."""
        from datetime import date
        from dateutil.relativedelta import relativedelta
        last_inspection = entity_profile.get("last_annual_stormwater_inspection")
        assert last_inspection is not None, \
            "No annual comprehensive site inspection recorded — MSGP §4.1"
        cutoff = date.today() - relativedelta(months=STORMWATER_ANNUAL_SITE_INSPECTION_MONTHS)
        assert last_inspection >= cutoff, (
            f"Annual stormwater inspection overdue: last inspection {last_inspection}, "
            f"must be within {STORMWATER_ANNUAL_SITE_INSPECTION_MONTHS} months — MSGP §4.1"
        )

    def test_quarterly_visual_assessments_documented(self, stormwater_scope, entity_profile: dict):
        """MSGP §3.3: Quarterly visual assessments of stormwater discharges required."""
        from datetime import date
        from dateutil.relativedelta import relativedelta
        last_visual = entity_profile.get("last_quarterly_stormwater_visual_assessment")
        assert last_visual is not None, \
            "No quarterly visual assessment record — MSGP §3.3"
        cutoff = date.today() - relativedelta(months=STORMWATER_QUARTERLY_VISUAL_ASSESSMENT_MONTHS)
        assert last_visual >= cutoff, (
            f"Quarterly stormwater visual assessment overdue: last assessment {last_visual}, "
            f"must be within {STORMWATER_QUARTERLY_VISUAL_ASSESSMENT_MONTHS} months — MSGP §3.3"
        )
```
