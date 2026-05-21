# NRC 10 CFR §50.48 — Fire Protection Program

**Spec file:** `fire-protection.md`
**Registry version:** 2026.05
**Last updated:** 2026-05-21
**Applies to:** Commercial nuclear power plant licensees holding operating licenses (OL) or combined licenses (COL) under 10 CFR Part 50 or Part 52; construction permit holders; nuclear power plant applicants during the licensing process
**Trigger:** NRC license to operate or construct a commercial nuclear power plant in the United States; Appendix B (QA) applies from earliest design phases; event reporting, maintenance rule, fire protection, and ISI/IST requirements apply throughout the operating license period
**Jurisdiction:** United States; enforced by the U.S. Nuclear Regulatory Commission through routine inspections, resident inspectors, and enforcement actions including Notices of Violation, Confirmatory Action Letters, and civil penalties
**Not applicable to:** Research and test reactors (10 CFR Part 50 applies partially but with different technical requirements); non-power utilization facilities; fuel cycle facilities (10 CFR Part 70); nuclear materials licensees; decommissioned reactors (10 CFR Part 50 Subpart E DECON/SAFSTOR requirements differ)
**Parent index:** [`_index.md`](./_index.md)
**Regulatory basis:** 10 CFR §50.48; 10 CFR Part 50, Appendix R; NFPA 805 (alternative method via §50.48(c))
**Authority:** U.S. Nuclear Regulatory Commission
**Key standards referenced:** NFPA 25 (suppression systems), NFPA 72 (detection/alarm), NFPA 805 (performance-based), NEI 00-01 (fire brigade), NUREG-0800 §9.5.1 (BTP CMEB 9.5-1)

---

## Overview

§50.48 requires nuclear power plants to maintain a fire protection program that protects safety-related structures, systems, and components (SSCs) from fire and provides post-fire safe shutdown capability. Two compliance methods are available:

| Method | Basis | Change path |
|--------|-------|-------------|
| **Appendix R (deterministic)** | 10 CFR 50 Appendix R — prescriptive three-hour fire barriers, fire brigade, suppression/detection, Appendix R safe shutdown analysis | Default method; NRC-approved license basis |
| **NFPA 805 (performance-based)** | §50.48(c) — risk-informed, performance-based; allows plant-specific methods if performance goals are met | Requires NRC license amendment before transition; about 30+ plants have transitioned |

The most-cited §50.48 violations involve: fire barrier integrity (penetration seal deficiencies), hot work fire watch lapses, and fire brigade staffing shortfalls.

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def nrc_50_48_scope_check(facility_profile: dict):
    """Skip if facility does not hold an NRC 10 CFR Part 50 operating license."""
    if not facility_profile.get("nrc_operating_license_active", False):
        pytest.skip(
            "§50.48 does not apply — facility does not hold an NRC 10 CFR Part 50 "
            "or Part 52 operating license"
        )
```

---

## Section 1 — Fire Protection Program Document (DETERMINISTIC)

### Requirements extracted

**Source:** 10 CFR §50.48(b); Appendix R, Section III.A; NRC Inspection Procedure 71111.05T

| # | Subject | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 1.1 | Written fire protection program | NRC-licensed nuclear facility | Shall have a written, NRC-approved fire protection program; program defines fire areas, protection features, suppression/detection, safe shutdown capability, and administrative controls | Fire protection program document; NRC SER approving program |
| 1.2 | Fire hazards analysis | All plant areas | Written fire hazards analysis (FHA) for each fire area; identifies ignition sources, combustible loads, fire protection features, and impact on safe shutdown SSCs | Fire hazards analysis document (or equivalent) |
| 1.3 | Compliance method documented | Either Appendix R or NFPA 805 | Plant fire protection program documents whether compliance is via Appendix R (default) or NFPA 805 §50.48(c) (requires license amendment) | License basis documentation; §50.48(c) license amendment (if NFPA 805) |
| 1.4 | NFPA 805 transition NRC approval | If NFPA 805 method in use | NRC must have approved the §50.48(c) license amendment before plant operates under NFPA 805; operating under NFPA 805 without approval is a violation of §50.48 | NRC license amendment approval; NRC inspection report |

### Tests — program existence and method

```python
import pytest


class TestFireProtectionProgram:
    """Pattern 1/2: DETERMINISTIC existence check; method selection is PARAMETERIZED."""

    @pytest.mark.assumption(
        id="ASSUME-NRC50-FP-001",
        description=(
            "Fire protection program method: Appendix R is the NRC-mandated default for plants "
            "licensed under 10 CFR Part 50 Appendix R. NFPA 805 is the alternative performance-"
            "based method available under §50.48(c) — requires NRC license amendment approval "
            "before transition. About 30+ plants have transitioned to NFPA 805 as of 2024. "
            "Regardless of method, the plant must have an NRC-approved fire protection program "
            "document, a fire hazards analysis, and an approved safe shutdown analysis."
        ),
        approved_by="Fire Protection Engineer / Licensing",
        review_date="2026-05-21",
    )
    def test_fire_protection_program_document_exists(self, fire_protection_program: dict):
        assert fire_protection_program.get("program_document_number"), (
            "§50.48(b): No fire protection program document on record — written NRC-approved "
            "fire protection program is required for all 10 CFR Part 50 licensees"
        )
        assert fire_protection_program.get("nrc_approved", False), (
            "Fire protection program has not been NRC-approved — §50.48 requires NRC approval "
            "of the fire protection program as part of the plant operating license"
        )

    def test_fire_hazards_analysis_exists(self, fire_protection_program: dict):
        fha_document = fire_protection_program.get("fire_hazards_analysis_document_number")
        assert fha_document is not None, (
            "Appendix R §III.A: No fire hazards analysis (FHA) on record — FHA is required to "
            "identify ignition sources, combustible loads, and safe shutdown impact for each "
            "fire area; FHA is the foundational document for the entire fire protection program"
        )

    def test_nfpa_805_requires_nrc_approved_license_amendment(self, fire_protection_program: dict):
        if fire_protection_program.get("compliance_method") != "NFPA 805":
            return  # Appendix R plants: nothing to check here

        amendment_number = fire_protection_program.get("nfpa_805_license_amendment_number")
        nrc_approval_date = fire_protection_program.get("nfpa_805_nrc_approval_date")

        assert amendment_number is not None, (
            "Plant fire protection program indicates NFPA 805 compliance method but no "
            "NRC-approved §50.48(c) license amendment on record — transition to NFPA 805 "
            "requires NRC written approval before implementation"
        )
        assert nrc_approval_date is not None, (
            f"NFPA 805 license amendment {amendment_number} has no documented NRC approval date"
        )
```

---

## Section 2 — Fire Suppression Systems (DETERMINISTIC — NFPA 25)

### Requirements extracted

**Source:** 10 CFR §50.48; Appendix R §III.G; NFPA 25 (2017 or applicable edition adopted by plant)

| # | System type | Inspection interval | Test/maintenance requirement | Evidence |
|---|-------------|--------------------|-----------------------------|---------|
| 2.1 | Wet pipe sprinkler — gauges | Quarterly | Gauge reading within normal range; no physical damage | Inspection records |
| 2.2 | Wet pipe sprinkler — main drain test | Annually | Main drain test — measures pressure to verify supply header not obstructed | Annual main drain test records |
| 2.3 | Wet pipe sprinkler — inspector test connection | Annually | Flow test via inspector test connection; confirms alarm activation | Annual flow test records |
| 2.4 | Sprinkler heads — visual inspection | Annually | No corrosion, paint, physical damage, or obstructions; clearance to deflector maintained | Annual inspection report |
| 2.5 | Sprinkler heads — 50-year replacement or sample test | 50 years (fast-response: 20 years) | Remove sample (min 4 heads per 10,000 installed) for laboratory testing per NFPA 25 5.4.1.2; or replace all heads | 50-year (or 20-year) test/replacement records |
| 2.6 | Dry pipe sprinkler — trip test | Annually | Dry pipe valve trip test to verify automatic operation; accelerator test annually | Annual dry-pipe trip test records |
| 2.7 | Deluge/pre-action system | Annually | Full trip test (operational test per NFPA 25 §8.3); water supply confirmed; nozzle condition | Annual deluge trip test records |
| 2.8 | Halon 1301 / clean agent systems | Annually | Weight/pressure check of agent containers; nozzle inspection; detector functional test | Annual halon/clean agent inspection records |
| 2.9 | CO₂ fixed suppression | Annually | Weight check of CO₂ cylinders; distribution piping inspection; alarm/detector functional test | Annual CO₂ inspection records |
| 2.10 | Standpipe — flow test | Every 5 years | Hydraulic flow test from highest, most remote outlet; pressure and flow must meet design requirements | 5-year standpipe flow test records |
| 2.11 | Fire water supply — flow test (hydrants) | Annually | Hydrant flow test to verify water supply availability; post-test valve position verification | Annual hydrant flow test records |

### DETERMINISTIC thresholds — suppression system testing

| Obligation | Interval | Source |
|---|---|---|
| Wet pipe sprinkler gauge inspection | Quarterly (3 months) | NFPA 25 §5.2.4 |
| Wet pipe main drain test | Annually | NFPA 25 §5.2.5 |
| Wet pipe inspector test connection flow test | Annually | NFPA 25 §5.3.1 |
| Sprinkler head visual inspection | Annually | NFPA 25 §5.4.1.1 |
| Sprinkler head 50-year sample test (standard response) | 50 years from installation | NFPA 25 §5.4.1.2 |
| Sprinkler head 20-year sample test (fast-response) | 20 years from installation | NFPA 25 §5.4.1.2 |
| Dry pipe valve trip test | Annually | NFPA 25 §7.3.1 |
| Deluge/pre-action operational test | Annually | NFPA 25 §8.3.1 |
| Halon/clean agent cylinder weight check | Annually | NFPA 12A / NFPA 2001 |
| Standpipe hydraulic flow test | Every 5 years (60 months) | NFPA 25 §6.3 |
| Fire water supply hydrant flow test | Annually | NFPA 25 §7.3.2 |

### Tests — suppression system interval compliance

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta

# NFPA 25 inspection and test intervals
WET_PIPE_GAUGE_INSPECTION_MONTHS = 3       # quarterly
WET_PIPE_MAIN_DRAIN_TEST_MONTHS = 12       # annual
SPRINKLER_HEAD_VISUAL_MONTHS = 12          # annual
SPRINKLER_HEAD_STANDARD_RESPONSE_YEARS = 50
SPRINKLER_HEAD_FAST_RESPONSE_YEARS = 20
DRY_PIPE_TRIP_TEST_MONTHS = 12            # annual
DELUGE_OPERATIONAL_TEST_MONTHS = 12       # annual
HALON_AGENT_INSPECTION_MONTHS = 12        # annual
STANDPIPE_FLOW_TEST_MONTHS = 60          # 5 years
HYDRANT_FLOW_TEST_MONTHS = 12            # annual


class TestFireSuppressionSystems:
    """Pattern 1: DETERMINISTIC — NFPA 25 inspection intervals are fixed."""

    @pytest.mark.assumption(
        id="ASSUME-NRC50-FP-002",
        description=(
            "NFPA 25 inspection intervals: nuclear plants reference NFPA 25 as the baseline "
            "standard for suppression system inspection, testing, and maintenance. The "
            "applicable edition is typically locked in the plant fire protection program or "
            "technical specifications. Quarterly gauge inspections, annual main drain tests, "
            "and annual inspector's test are the most commonly cited deficiencies in NRC "
            "fire protection inspection findings (NRC IP 71111.05T)."
        ),
        approved_by="Fire Protection Engineer",
        review_date="2026-05-21",
    )
    def test_wet_pipe_sprinkler_gauge_inspection_not_overdue(self, suppression_system_record: dict):
        if suppression_system_record.get("system_type") != "wet_pipe_sprinkler":
            pytest.skip("This test applies to wet pipe sprinkler systems only")

        last_gauge_inspection = suppression_system_record.get("last_gauge_inspection_date")
        assert last_gauge_inspection is not None, (
            f"Suppression system '{suppression_system_record.get('system_id')}': "
            "no quarterly gauge inspection on record — NFPA 25 §5.2.4 requires quarterly "
            "gauge inspection of wet pipe sprinkler systems"
        )

        due_date = last_gauge_inspection + relativedelta(months=WET_PIPE_GAUGE_INSPECTION_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"Wet pipe sprinkler '{suppression_system_record.get('system_id')}': "
            f"quarterly gauge inspection overdue — last: {last_gauge_inspection}, "
            f"due: {due_date}, today: {today}"
        )

    def test_wet_pipe_main_drain_test_not_overdue(self, suppression_system_record: dict):
        if suppression_system_record.get("system_type") != "wet_pipe_sprinkler":
            pytest.skip("This test applies to wet pipe sprinkler systems only")

        last_drain_test = suppression_system_record.get("last_main_drain_test_date")
        assert last_drain_test is not None, (
            f"Wet pipe sprinkler '{suppression_system_record.get('system_id')}': "
            "no annual main drain test on record — NFPA 25 §5.2.5 requires annual main "
            "drain test to verify water supply header is unobstructed"
        )

        due_date = last_drain_test + relativedelta(months=WET_PIPE_MAIN_DRAIN_TEST_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"Wet pipe sprinkler '{suppression_system_record.get('system_id')}': "
            f"annual main drain test overdue — last: {last_drain_test}, due: {due_date}, today: {today}"
        )

    def test_sprinkler_head_visual_inspection_not_overdue(self, suppression_system_record: dict):
        if "sprinkler" not in suppression_system_record.get("system_type", ""):
            pytest.skip("This test applies to sprinkler systems only")

        last_head_inspection = suppression_system_record.get("last_sprinkler_head_inspection_date")
        assert last_head_inspection is not None, (
            f"Sprinkler system '{suppression_system_record.get('system_id')}': "
            "no annual sprinkler head inspection on record — NFPA 25 §5.4.1.1 requires "
            "annual visual inspection of all sprinkler heads for corrosion, paint, damage, "
            "obstructions, and deflector clearance"
        )

        due_date = last_head_inspection + relativedelta(months=SPRINKLER_HEAD_VISUAL_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"Sprinkler system '{suppression_system_record.get('system_id')}': "
            f"annual sprinkler head inspection overdue — last: {last_head_inspection}, "
            f"due: {due_date}, today: {today}"
        )

    def test_sprinkler_heads_within_50_or_20_year_sample_test_window(self, suppression_system_record: dict):
        if "sprinkler" not in suppression_system_record.get("system_type", ""):
            pytest.skip("This test applies to sprinkler systems only")

        installation_year = suppression_system_record.get("sprinkler_heads_installation_year")
        if installation_year is None:
            pytest.skip("Sprinkler head installation year not recorded")

        head_type = suppression_system_record.get("sprinkler_head_type", "standard_response")
        max_years = (
            SPRINKLER_HEAD_FAST_RESPONSE_YEARS
            if head_type == "fast_response"
            else SPRINKLER_HEAD_STANDARD_RESPONSE_YEARS
        )

        installation_date = date(installation_year, 1, 1)
        sample_test_due = installation_date + relativedelta(years=max_years)
        today = date.today()

        last_sample_test = suppression_system_record.get("last_sprinkler_head_sample_test_date")
        heads_replaced = suppression_system_record.get("heads_replaced_at_max_interval", False)

        if today >= sample_test_due:
            assert last_sample_test is not None or heads_replaced, (
                f"Sprinkler system '{suppression_system_record.get('system_id')}': "
                f"{head_type.replace('_', ' ')} heads installed in {installation_year} — "
                f"{max_years}-year laboratory sample test or full replacement required by "
                f"{sample_test_due} per NFPA 25 §5.4.1.2; neither sample test nor replacement "
                "is on record"
            )

    def test_deluge_preaction_operational_test_not_overdue(self, suppression_system_record: dict):
        if suppression_system_record.get("system_type") not in ("deluge", "pre_action"):
            pytest.skip("This test applies to deluge and pre-action systems only")

        last_trip_test = suppression_system_record.get("last_operational_trip_test_date")
        assert last_trip_test is not None, (
            f"Suppression system '{suppression_system_record.get('system_id')}' "
            f"({suppression_system_record.get('system_type')}): "
            "no annual operational trip test on record — NFPA 25 §8.3.1 requires annual "
            "operational test of deluge and pre-action systems"
        )

        due_date = last_trip_test + relativedelta(months=DELUGE_OPERATIONAL_TEST_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"Deluge/pre-action system '{suppression_system_record.get('system_id')}': "
            f"annual operational test overdue — last: {last_trip_test}, due: {due_date}, today: {today}"
        )

    def test_standpipe_flow_test_within_5_year_interval(self, suppression_system_record: dict):
        if suppression_system_record.get("system_type") != "standpipe":
            pytest.skip("This test applies to standpipe systems only")

        last_flow_test = suppression_system_record.get("last_hydraulic_flow_test_date")
        assert last_flow_test is not None, (
            f"Standpipe system '{suppression_system_record.get('system_id')}': "
            "no 5-year hydraulic flow test on record — NFPA 25 §6.3 requires hydraulic "
            "flow testing of standpipe systems every 5 years"
        )

        due_date = last_flow_test + relativedelta(months=STANDPIPE_FLOW_TEST_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"Standpipe system '{suppression_system_record.get('system_id')}': "
            f"5-year hydraulic flow test overdue — last: {last_flow_test}, due: {due_date}, today: {today}"
        )
```

---

## Section 3 — Fire Detection and Alarm Systems (DETERMINISTIC — NFPA 72)

### Requirements extracted

**Source:** 10 CFR §50.48; Appendix R §III.H; NFPA 72 (applicable edition per plant fire protection program)

| # | Device type | Test interval | Test requirement | Evidence |
|---|-------------|--------------|-----------------|---------|
| 3.1 | Smoke detectors (ionization/photoelectric) | Annually | Functional test with smoke/aerosol test agent; sensitivity verification per NFPA 72 | Annual smoke detector test records |
| 3.2 | Heat detectors (fixed temperature) | Annually | Functional test using heat gun; calibration check per NFPA 72 §14.4.4 | Annual heat detector test records |
| 3.3 | Beam smoke detectors | Annually + sensitivity check | Functional test; beam alignment; sensitivity within ±4 dB margin | Annual beam detector test records |
| 3.4 | Manual pull stations | Annually | Functional test — pull station actuates alarm; reset verified | Annual pull station test records |
| 3.5 | Fire alarm control panel (FACP) | Annually | Full functional test: alarm initiation, supervisory signals, trouble signals, notification appliance circuits | Annual FACP functional test records |
| 3.6 | FACP battery — load test | Annually | Battery capacity load test under simulated alarm condition; no less than 24-hour standby + 5-minute alarm | Annual battery load test records |
| 3.7 | FACP battery — inspection | Quarterly | Visual inspection — no corrosion, electrolyte level OK, connections tight | Quarterly battery inspection records |
| 3.8 | Audible/visual notification appliances | Annually | Functional test of horns, strobes, speakers | Annual notification appliance test records |
| 3.9 | Duct smoke detectors | Annually | Functional test with smoke/aerosol; airflow test to verify detector is responsive in duct conditions | Annual duct detector test records |

### Tests — fire detection interval compliance

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta

FIRE_DETECTION_ANNUAL_TEST_MONTHS = 12
FACP_BATTERY_INSPECTION_MONTHS = 3   # quarterly


class TestFireDetectionSystems:
    """Pattern 1: DETERMINISTIC — NFPA 72 testing intervals are fixed."""

    @pytest.mark.assumption(
        id="ASSUME-NRC50-FP-003",
        description=(
            "NFPA 72 fire detection testing: nuclear plants reference NFPA 72 for fire detection "
            "and alarm system inspection, testing, and maintenance. All initiating devices "
            "(smoke detectors, heat detectors, manual pull stations) are tested annually. "
            "FACP battery load testing annually and quarterly visual inspection are required. "
            "Detection testing is tracked in the plant surveillance test program and inspected "
            "by NRC fire protection inspectors under IP 71111.05T."
        ),
        approved_by="Fire Protection Engineer",
        review_date="2026-05-21",
    )
    def test_fire_detector_annual_test_not_overdue(self, fire_detector_record: dict):
        detector_types_annual = {
            "smoke_ionization", "smoke_photoelectric", "smoke_beam",
            "heat_fixed_temperature", "heat_rate_of_rise",
            "manual_pull_station", "duct_smoke_detector",
        }

        detector_type = fire_detector_record.get("detector_type")
        if detector_type not in detector_types_annual:
            pytest.skip(f"Annual test interval not defined for detector type '{detector_type}'")

        last_test_date = fire_detector_record.get("last_annual_test_date")
        assert last_test_date is not None, (
            f"Fire detector '{fire_detector_record.get('detector_id')}' ({detector_type}): "
            "no annual functional test on record — NFPA 72 requires annual testing of all "
            "initiating devices; untested detectors are a common NRC fire protection finding"
        )

        due_date = last_test_date + relativedelta(months=FIRE_DETECTION_ANNUAL_TEST_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"Fire detector '{fire_detector_record.get('detector_id')}' ({detector_type}): "
            f"annual functional test overdue — last: {last_test_date}, due: {due_date}, today: {today}"
        )

    def test_facp_annual_functional_test_not_overdue(self, facp_record: dict):
        last_annual_test = facp_record.get("last_annual_functional_test_date")
        assert last_annual_test is not None, (
            f"Fire alarm control panel '{facp_record.get('facp_id')}': "
            "no annual full functional test on record — NFPA 72 requires annual functional "
            "test of the FACP including all alarm, supervisory, and trouble signal circuits"
        )

        due_date = last_annual_test + relativedelta(months=FIRE_DETECTION_ANNUAL_TEST_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"FACP '{facp_record.get('facp_id')}': annual functional test overdue — "
            f"last: {last_annual_test}, due: {due_date}, today: {today}"
        )

    def test_facp_battery_quarterly_inspection_not_overdue(self, facp_record: dict):
        last_battery_inspection = facp_record.get("last_battery_quarterly_inspection_date")
        assert last_battery_inspection is not None, (
            f"FACP '{facp_record.get('facp_id')}': no quarterly battery inspection on record — "
            "NFPA 72 requires quarterly visual inspection of FACP batteries"
        )

        due_date = last_battery_inspection + relativedelta(months=FACP_BATTERY_INSPECTION_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"FACP '{facp_record.get('facp_id')}': quarterly battery inspection overdue — "
            f"last: {last_battery_inspection}, due: {due_date}, today: {today}"
        )

    def test_facp_battery_annual_load_test_not_overdue(self, facp_record: dict):
        last_load_test = facp_record.get("last_battery_load_test_date")
        assert last_load_test is not None, (
            f"FACP '{facp_record.get('facp_id')}': no annual battery load test on record — "
            "NFPA 72 requires annual battery capacity verification under simulated alarm load; "
            "minimum 24-hour standby plus 5-minute alarm capacity required"
        )

        due_date = last_load_test + relativedelta(months=FIRE_DETECTION_ANNUAL_TEST_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"FACP '{facp_record.get('facp_id')}': annual battery load test overdue — "
            f"last: {last_load_test}, due: {due_date}, today: {today}"
        )
```

---

## Section 4 — Fire Barriers and Penetration Seals (PARAMETERIZED with DETERMINISTIC intervals)

### Requirements extracted

**Source:** Appendix R §III.G.2, §III.L; 10 CFR 50 App. R Section III; NUREG-0800 §9.5.1; NRC IP 71111.05T

| # | Element | Requirement | Confidence |
|---|---------|-------------|-----------|
| 4.1 | Three-hour fire barriers between redundant shutdown divisions | Appendix R §III.G.2.a: fire barriers with 3-hour fire resistance rating separate redundant safe shutdown divisions (Trains A and B) | PARAMETERIZED — barrier adequacy (original rating confirmed vs. as-modified condition) |
| 4.2 | One-hour fire barriers — alternative to suppression | Appendix R §III.G.2.b: alternative to 3-hour barrier: 1-hour barrier + fire detection + manual suppression capability | PARAMETERIZED — combination of features |
| 4.3 | Fire door inspection and functional test | Annual functional test — self-closing doors: close completely, latch, positive latching; smoke seals intact | DETERMINISTIC (annual test interval) |
| 4.4 | Fire door visual inspection | Every 6 months | Check for physical damage, wedging open, door frame gap, seals | DETERMINISTIC (6-month interval) |
| 4.5 | Penetration seal inspection | Annually — visual inspection per qualified fire-stop method; no gaps, voids, or physical damage | DETERMINISTIC (annual interval); adequacy PARAMETERIZED |
| 4.6 | Fire wrap/blanket inspection | Annually | No physical damage, proper attachment, coverage per installation drawing | DETERMINISTIC (annual interval) |

### Tests — fire barrier inspection intervals

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta

FIRE_DOOR_FUNCTIONAL_TEST_MONTHS = 12     # annual
FIRE_DOOR_VISUAL_INSPECTION_MONTHS = 6   # semi-annual
PENETRATION_SEAL_INSPECTION_MONTHS = 12  # annual
FIRE_WRAP_INSPECTION_MONTHS = 12          # annual


class TestFireBarriers:

    @pytest.mark.assumption(
        id="ASSUME-NRC50-FP-004",
        description=(
            "Fire barrier inspection intervals: fire doors require annual functional tests "
            "(self-closing, latching, seal integrity) and semi-annual visual inspections. "
            "Penetration seals and fire wraps require annual visual inspections per the "
            "qualified fire-stop method (UL-listed, tested per ASTM E814 / UL 1479). "
            "Penetration seal deficiencies (unqualified fire-stop materials, gaps, voids) "
            "are the single most frequently cited finding in NRC fire protection inspections — "
            "a plant may have hundreds of seals requiring tracking. Adequacy of fire-stop "
            "materials (correct qualified sealing compound vs. as-installed material) is "
            "PARAMETERIZED and requires engineering judgment."
        ),
        approved_by="Fire Protection Engineer",
        review_date="2026-05-21",
    )
    def test_fire_door_annual_functional_test_not_overdue(self, fire_barrier_record: dict):
        if fire_barrier_record.get("barrier_type") != "fire_door":
            pytest.skip("This test applies to fire doors only")

        last_functional_test = fire_barrier_record.get("last_annual_functional_test_date")
        assert last_functional_test is not None, (
            f"Fire door '{fire_barrier_record.get('door_id')}': no annual functional test "
            "on record — Appendix R §III.G / NRC IP 71111.05T requires annual functional "
            "test: self-closing, positive latching, and seal integrity confirmed"
        )

        due_date = last_functional_test + relativedelta(months=FIRE_DOOR_FUNCTIONAL_TEST_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"Fire door '{fire_barrier_record.get('door_id')}': annual functional test "
            f"overdue — last: {last_functional_test}, due: {due_date}, today: {today}"
        )

    def test_fire_door_semi_annual_visual_inspection_not_overdue(self, fire_barrier_record: dict):
        if fire_barrier_record.get("barrier_type") != "fire_door":
            pytest.skip("This test applies to fire doors only")

        last_visual = fire_barrier_record.get("last_semi_annual_visual_inspection_date")
        assert last_visual is not None, (
            f"Fire door '{fire_barrier_record.get('door_id')}': no semi-annual visual "
            "inspection on record — fire doors shall be visually inspected every 6 months "
            "for physical damage, wedging, frame gaps, and seal condition"
        )

        due_date = last_visual + relativedelta(months=FIRE_DOOR_VISUAL_INSPECTION_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"Fire door '{fire_barrier_record.get('door_id')}': semi-annual visual inspection "
            f"overdue — last: {last_visual}, due: {due_date}, today: {today}"
        )

    def test_penetration_seal_annual_inspection_not_overdue(self, fire_barrier_record: dict):
        if fire_barrier_record.get("barrier_type") != "penetration_seal":
            pytest.skip("This test applies to penetration seals only")

        last_inspection = fire_barrier_record.get("last_annual_inspection_date")
        assert last_inspection is not None, (
            f"Penetration seal '{fire_barrier_record.get('seal_id')}': no annual visual "
            "inspection on record — penetration seal inspections are among the most "
            "frequently cited §50.48 findings; annual inspection required per fire "
            "protection program surveillance procedures"
        )

        due_date = last_inspection + relativedelta(months=PENETRATION_SEAL_INSPECTION_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"Penetration seal '{fire_barrier_record.get('seal_id')}': annual inspection "
            f"overdue — last: {last_inspection}, due: {due_date}, today: {today}"
        )

    @pytest.mark.human_review_required(
        reason=(
            "Fire barrier adequacy — whether a fire barrier provides the required "
            "1-hour or 3-hour fire resistance rating in its as-modified, as-maintained "
            "condition requires fire protection engineer evaluation. Common issues: "
            "(1) repairs using non-qualified fire-stop material, (2) gaps in penetration "
            "seals that reduce effective rating, (3) fire door hardware replaced with "
            "non-listed components. Automated inspection tracks whether an inspection "
            "occurred; it cannot evaluate adequacy of what was found."
        )
    )
    def test_fire_barrier_adequacy_requires_engineering_review(self, fire_barrier_record: dict):
        last_engineering_review = fire_barrier_record.get("last_fire_protection_engineering_review_date")
        assert last_engineering_review is not None, (
            f"Fire barrier '{fire_barrier_record.get('barrier_id')}': no fire protection "
            "engineering review of barrier adequacy on record — each fire barrier must be "
            "verified as providing the required fire resistance rating in its current condition"
        )
```

---

## Section 5 — Hot Work Program (DETERMINISTIC)

### Requirements extracted

**Source:** Appendix R §III.J; plant fire protection program administrative controls; OSHA 29 CFR 1910.252 (reference)

| # | Requirement | Condition | Obligation | Evidence |
|---|-------------|-----------|------------|---------|
| 5.1 | Hot work permit required | All welding, cutting, grinding, brazing, soldering in non-permanent welding shops | Written hot work permit (fire permit) required before any hot work begins; identifies fire watches, precautions, fire extinguisher staging | Hot work permit records; permit log |
| 5.2 | Continuous fire watch during hot work | Hot work in progress | At minimum one continuous fire watch with fire extinguisher present at work location for all duration of hot work operations | Fire watch log; hot work permit (fire watch assignment) |
| 5.3 | Post-hot-work fire watch — welding/cutting | After welding, torch cutting, brazing | Fire watch maintained for minimum 60 minutes after cessation of hot work at the work location; extended to 4 hours if work performed adjacent to combustible structural materials or within 35 ft of combustibles that cannot be removed | Post-hot-work fire watch log |
| 5.4 | Fire watch training | All personnel assigned fire watch duty | Fire watches trained and qualified — recognize fires, operate extinguishers, activate alarm, contact fire brigade | Training records for fire watch designees |
| 5.5 | Combustible material removal or protection | Before hot work begins | Remove all unnecessary combustibles from within 35 feet of hot work; protect combustibles that cannot be removed with flame-resistant blankets | Hot work permit (pre-work inspection checklist) |

### DETERMINISTIC thresholds — hot work

| Obligation | Threshold | Source |
|---|---|---|
| Fire watch — during hot work | Continuous; present at work location | Appendix R §III.J; NFPA 51B |
| Post-hot-work fire watch (welding/cutting) | Minimum 60 minutes | NFPA 51B §5.6.3; plant fire protection program |
| Post-hot-work fire watch — combustible adjacent areas | Minimum 4 hours | NFPA 51B §5.6.3.1; plant fire protection program |
| Combustible clearance radius | 35 feet from hot work | NFPA 51B §5.3 |

### Tests — hot work compliance

```python
import pytest
from datetime import timedelta

POST_HOT_WORK_MINIMUM_FIRE_WATCH_MINUTES = 60
POST_HOT_WORK_ADJACENT_COMBUSTIBLES_FIRE_WATCH_MINUTES = 240  # 4 hours


class TestHotWorkProgram:
    """Pattern 1: DETERMINISTIC — fire watch timing requirements are fixed."""

    @pytest.mark.assumption(
        id="ASSUME-NRC50-FP-005",
        description=(
            "Hot work fire watch: a continuous fire watch is required during all hot work "
            "(welding, torch cutting, grinding that produces sparks, brazing, soldering). "
            "After hot work ceases, fire watch continues for a minimum of 60 minutes. If "
            "hot work was performed adjacent to combustible structural materials, enclosed "
            "areas with combustibles, or within 35 feet of combustibles that cannot be "
            "removed, the post-work fire watch extends to 4 hours. Nuclear plants may have "
            "more conservative site-specific requirements in their fire protection program."
        ),
        approved_by="Fire Protection Engineer",
        review_date="2026-05-21",
    )
    def test_hot_work_permit_issued_before_work(self, hot_work_record: dict):
        permit_issue_time = hot_work_record.get("permit_issue_time")
        work_start_time = hot_work_record.get("work_start_time")

        assert permit_issue_time is not None, (
            f"Hot work event '{hot_work_record.get('permit_number')}': no permit issue time "
            "recorded — hot work permit must be issued before work begins per plant "
            "fire protection program administrative controls (Appendix R §III.J)"
        )

        if work_start_time is not None:
            assert permit_issue_time <= work_start_time, (
                f"Hot work permit '{hot_work_record.get('permit_number')}': permit issued "
                f"at {permit_issue_time} AFTER work started at {work_start_time} — "
                "hot work permit must precede all work operations"
            )

    def test_continuous_fire_watch_present_during_hot_work(self, hot_work_record: dict):
        fire_watch_assigned = hot_work_record.get("fire_watch_assigned", False)
        assert fire_watch_assigned, (
            f"Hot work permit '{hot_work_record.get('permit_number')}': no fire watch "
            "assigned — a continuous fire watch with fire extinguisher is required at the "
            "work location for all hot work operations per Appendix R §III.J"
        )

        fire_watch_qualified = hot_work_record.get("fire_watch_training_current", False)
        assert fire_watch_qualified, (
            f"Hot work permit '{hot_work_record.get('permit_number')}': assigned fire watch "
            f"'{hot_work_record.get('fire_watch_name')}' training is not current — fire "
            "watches must be trained and qualified per plant fire protection program"
        )

    def test_post_hot_work_fire_watch_meets_minimum_duration(self, hot_work_record: dict):
        work_end_time = hot_work_record.get("hot_work_end_time")
        fire_watch_end_time = hot_work_record.get("post_work_fire_watch_end_time")

        if work_end_time is None or fire_watch_end_time is None:
            pytest.skip("Hot work end time or fire watch end time not recorded")

        adjacent_combustibles = hot_work_record.get("adjacent_to_combustible_construction", False)
        required_minutes = (
            POST_HOT_WORK_ADJACENT_COMBUSTIBLES_FIRE_WATCH_MINUTES
            if adjacent_combustibles
            else POST_HOT_WORK_MINIMUM_FIRE_WATCH_MINUTES
        )

        actual_watch_minutes = (fire_watch_end_time - work_end_time).total_seconds() / 60

        assert actual_watch_minutes >= required_minutes, (
            f"Hot work permit '{hot_work_record.get('permit_number')}': post-hot-work fire "
            f"watch lasted {actual_watch_minutes:.0f} minutes — minimum required is "
            f"{required_minutes} minutes "
            f"({'adjacent combustible construction' if adjacent_combustibles else 'standard'}) "
            "per NFPA 51B §5.6.3 and plant fire protection program; "
            "short fire watches are among the most frequently cited §50.48 violations"
        )
```

---

## Section 6 — Fire Brigade (DETERMINISTIC / PARAMETERIZED)

### Requirements extracted

**Source:** 10 CFR 50, Appendix R §III.D; NEI 00-01 (fire brigade guideline)

| # | Requirement | Threshold | Confidence |
|---|-------------|-----------|-----------|
| 6.1 | Fire brigade minimum staffing | Minimum 5 members on-site at all times (shift basis) | DETERMINISTIC |
| 6.2 | Fire brigade leader | Minimum one fire brigade leader on each fire brigade shift team | DETERMINISTIC (existence) |
| 6.3 | Fire brigade training — initial | Before assignment to fire brigade | Training topics: fire behavior, extinguishment techniques, fire brigade duties, self-contained breathing apparatus (SCBA) donning and use, communication procedures | PARAMETERIZED |
| 6.4 | Fire brigade training — refresher | At least annually | Annual refresher training per plant fire brigade manual | DETERMINISTIC (annual interval) |
| 6.5 | Fire brigade drills | Quarterly (at least one announced drill per year) | Minimum quarterly drills per fire brigade team; at least one unannounced drill per year | DETERMINISTIC (quarterly interval) |
| 6.6 | Annual drill — unannounced | Annually | At least one drill per year is unannounced (brigade does not know in advance) | DETERMINISTIC |
| 6.7 | SCBA qualification | At least annually | All brigade members pass SCBA donning qualification (under 60 seconds for full donning) | DETERMINISTIC |

### Tests — fire brigade compliance

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta

FIRE_BRIGADE_MINIMUM_STAFFING = 5
FIRE_BRIGADE_DRILL_INTERVAL_MONTHS = 3    # quarterly
FIRE_BRIGADE_TRAINING_ANNUAL_MONTHS = 12  # annual refresher


class TestFireBrigade:
    """Pattern 1: DETERMINISTIC — Appendix R §III.D staffing and drill requirements are fixed."""

    @pytest.mark.assumption(
        id="ASSUME-NRC50-FP-006",
        description=(
            "Fire brigade requirements per Appendix R §III.D: minimum 5 members on-site "
            "at all times; at least one qualified fire brigade leader per shift team. "
            "Quarterly drills required (at minimum one per shift team per quarter); at least "
            "one unannounced drill per year per shift team per Appendix R §III.D and NEI 00-01. "
            "Annual refresher training required. SCBA qualification annually — industry standard "
            "is donning in 60 seconds or less under test conditions."
        ),
        approved_by="Fire Protection Engineer / Fire Brigade Coordinator",
        review_date="2026-05-21",
    )
    def test_fire_brigade_minimum_shift_staffing(self, fire_brigade_shift_record: dict):
        on_site_count = fire_brigade_shift_record.get("on_site_brigade_members", 0)
        shift_id = fire_brigade_shift_record.get("shift_id")

        assert on_site_count >= FIRE_BRIGADE_MINIMUM_STAFFING, (
            f"Shift '{shift_id}': fire brigade staffing is {on_site_count} members — "
            f"Appendix R §III.D requires a minimum of {FIRE_BRIGADE_MINIMUM_STAFFING} qualified "
            "fire brigade members on-site at all times; staffing shortfall is a reportable "
            "operability condition that may trigger Technical Specification action"
        )

    def test_fire_brigade_leader_present_each_shift(self, fire_brigade_shift_record: dict):
        has_leader = fire_brigade_shift_record.get("qualified_leader_on_site", False)
        shift_id = fire_brigade_shift_record.get("shift_id")

        assert has_leader, (
            f"Shift '{shift_id}': no qualified fire brigade leader on-site — "
            "Appendix R §III.D requires at least one fire brigade leader per on-shift team; "
            "a fire brigade team without a qualified leader cannot meet the fire response "
            "capability requirement"
        )

    def test_fire_brigade_quarterly_drill_not_overdue(self, fire_brigade_team_record: dict):
        team_id = fire_brigade_team_record.get("team_id")
        last_drill_date = fire_brigade_team_record.get("last_drill_date")

        assert last_drill_date is not None, (
            f"Fire brigade team '{team_id}': no drill on record — Appendix R §III.D requires "
            "quarterly fire brigade drills; no drills on record is a significant §50.48 finding"
        )

        due_date = last_drill_date + relativedelta(months=FIRE_BRIGADE_DRILL_INTERVAL_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"Fire brigade team '{team_id}': quarterly drill overdue — "
            f"last drill: {last_drill_date}, due: {due_date}, today: {today} — "
            "Appendix R §III.D requires drills at least quarterly for each fire brigade team"
        )

    def test_fire_brigade_annual_unannounced_drill_completed(self, fire_brigade_team_record: dict):
        team_id = fire_brigade_team_record.get("team_id")
        current_year = date.today().year
        unannounced_drills_this_year = [
            d for d in fire_brigade_team_record.get("drills_this_year", [])
            if not d.get("announced", True)
        ]

        # Only check if we're past Q1 of the year (first opportunity for unannounced drill)
        if date.today().month < 4:
            pytest.skip("Annual unannounced drill check deferred — Q1 not yet complete")

        assert len(unannounced_drills_this_year) >= 1, (
            f"Fire brigade team '{team_id}': no unannounced fire brigade drill in {current_year} — "
            "Appendix R §III.D requires at least one unannounced drill per year for each fire "
            "brigade team; unannounced drills test actual response capability"
        )

    def test_fire_brigade_member_annual_training_current(self, fire_brigade_member_record: dict):
        member_id = fire_brigade_member_record.get("member_id")
        last_annual_training = fire_brigade_member_record.get("last_annual_refresher_training_date")

        assert last_annual_training is not None, (
            f"Fire brigade member '{member_id}': no annual refresher training on record — "
            "Appendix R §III.D requires annual fire brigade refresher training"
        )

        due_date = last_annual_training + relativedelta(months=FIRE_BRIGADE_TRAINING_ANNUAL_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"Fire brigade member '{member_id}': annual training overdue — "
            f"last training: {last_annual_training}, due: {due_date}, today: {today}"
        )
```

---

## Section 7 — Safe Shutdown Capability (CONTESTED / PARAMETERIZED)

### Requirements extracted

**Source:** Appendix R §III.G; NUREG-0800 §9.5.1; RG 1.189

| # | Element | Confidence | Notes |
|---|---------|-----------|-------|
| 7.1 | Post-fire safe shutdown analysis (SSA) written | PARAMETERIZED | SSA documents the shutdown method and SSCs required for each fire area |
| 7.2 | Redundant cold shutdown trains separated by 3-hour barriers | PARAMETERIZED | Physical separation or protection of redundant shutdown trains per Appendix R §III.G.2 |
| 7.3 | Alternative shutdown panel availability | PARAMETERIZED | If main control room lost to fire, alternative shutdown from outside — §III.G.3 |
| 7.4 | Manual operator action feasibility (time and accessibility) | CONTESTED | Whether manual actions are feasible in a post-fire scenario with smoke, limited access — depends on HRA, walk-down validation |
| 7.5 | Fire-induced circuit failure analysis | PARAMETERIZED / CONTESTED | Cable routing analysis for spurious actuation, hot shorts, loss of function — complex systems engineering |
| 7.6 | NFPA 805 performance goal compliance | CONTESTED | Whether current plant configuration meets NFPA 805 performance goals (core damage frequency, large early release frequency limits) requires full PRA model update |

### Tests — safe shutdown program status

```python
import pytest


class TestSafeShutdownCapability:
    """Pattern 2/3: safe shutdown analysis is PARAMETERIZED; operator action feasibility is CONTESTED."""

    @pytest.mark.assumption(
        id="ASSUME-NRC50-FP-007",
        description=(
            "Safe shutdown analysis (SSA): every nuclear plant must have a documented SSA "
            "that identifies the SSCs required for safe shutdown for each fire area. The SSA "
            "demonstrates that fire in any area cannot prevent safe shutdown via at least one "
            "complete shutdown train. Under Appendix R §III.G.2(a), the preferred method is "
            "3-hour fire barriers separating redundant trains; alternative methods (§III.G.2.b/c) "
            "allow 1-hour barriers with suppression/detection or other combinations. The SSA "
            "must be updated for plant design changes per the §50.59 change process."
        ),
        approved_by="Fire Protection Engineer",
        review_date="2026-05-21",
    )
    def test_safe_shutdown_analysis_document_exists(self, fire_protection_program: dict):
        ssa_document = fire_protection_program.get("safe_shutdown_analysis_document_number")
        assert ssa_document is not None, (
            "Appendix R §III.G: No safe shutdown analysis (SSA) document on record — "
            "SSA is required to demonstrate post-fire safe shutdown capability for all "
            "fire areas; absence of SSA is a fundamental §50.48 compliance gap"
        )

    def test_safe_shutdown_analysis_current_with_design_basis(self, fire_protection_program: dict):
        ssa_revision = fire_protection_program.get("ssa_current_revision")
        last_design_change_ssa_review = fire_protection_program.get("last_50_59_ssa_update_date")

        assert ssa_revision is not None, (
            "Safe shutdown analysis: no current revision identified — SSA must be maintained "
            "to reflect current plant design; updates required whenever design changes affect "
            "fire area boundaries, cable routing, or safe shutdown SSC availability"
        )
        assert last_design_change_ssa_review is not None, (
            "Safe shutdown analysis: no record of §50.59 review for design changes affecting "
            "SSA — changes to fire area SSCs must be evaluated for impact on SSA and updated "
            "per §50.59 screening or full evaluation requirements"
        )

    @pytest.mark.human_review_required(
        reason=(
            "Manual operator action feasibility — whether operator actions required for "
            "post-fire safe shutdown are actually feasible (accessible routes, timing, "
            "smoke conditions, equipment operability with fire-induced circuit failures) "
            "requires walk-down validation and Human Reliability Analysis (HRA). NRC has "
            "identified non-feasible manual actions as a significant finding in multiple "
            "fire protection inspections. This determination cannot be made from test data "
            "alone — it requires an on-site engineering evaluation."
        )
    )
    def test_manual_operator_actions_walk_down_validated(self, fire_protection_program: dict):
        walkdown_completed = fire_protection_program.get("operator_actions_walkdown_validated", False)
        assert walkdown_completed, (
            "Appendix R §III.G / NRC IP 71111.05T: No walk-down validation of operator "
            "manual actions for post-fire safe shutdown on record — walk-down validation "
            "is required to verify that manual actions are feasible in terms of route "
            "accessibility, timing, and equipment availability"
        )
        walkdown_date = fire_protection_program.get("operator_actions_walkdown_date")
        assert walkdown_date is not None, (
            "Walk-down validation is recorded but no date is documented — walk-down "
            "date required to assess currency relative to design changes"
        )

    @pytest.mark.human_review_required(
        reason=(
            "Fire-induced circuit failure analysis — whether spurious actuations, hot shorts, "
            "or loss-of-function failures caused by fires affecting cable routing zones could "
            "prevent safe shutdown requires a detailed cable routing analysis and fire-induced "
            "circuit failure analysis (FICFA). This is among the most technically complex "
            "aspects of Appendix R compliance and has been the subject of multiple NRC "
            "Inspection Findings at various plants."
        )
    )
    def test_fire_induced_circuit_failure_analysis_exists(self, fire_protection_program: dict):
        ficfa_document = fire_protection_program.get("fire_induced_circuit_failure_analysis_document")
        assert ficfa_document is not None, (
            "No fire-induced circuit failure analysis (FICFA) document on record — FICFA is "
            "required to evaluate whether fire-induced cable failures could cause spurious "
            "actuations or loss-of-function that prevents safe shutdown; this is a required "
            "element of the Appendix R safe shutdown analysis"
        )
```

---

## Open assumptions

| ID | Section | Summary | Review date |
|---|---|---|---|
| ASSUME-NRC50-FP-001 | §50.48 program | Fire protection method: Appendix R is default; NFPA 805 requires §50.48(c) NRC license amendment before transition | 2026-05-21 |
| ASSUME-NRC50-FP-002 | §50.48 suppression | NFPA 25 inspection intervals: quarterly gauges, annual main drain, annual sprinkler head inspection; 50-year (standard) and 20-year (fast-response) sample tests; 5-year standpipe flow test | 2026-05-21 |
| ASSUME-NRC50-FP-003 | §50.48 detection | NFPA 72 testing: annual functional test of all initiating devices (smoke, heat, pull stations); annual FACP functional test; quarterly battery visual; annual battery load test | 2026-05-21 |
| ASSUME-NRC50-FP-004 | §50.48 barriers | Fire door annual functional test + semi-annual visual; penetration seal annual inspection; seal adequacy (qualified fire-stop material) is PARAMETERIZED | 2026-05-21 |
| ASSUME-NRC50-FP-005 | §50.48 hot work | Post-hot-work fire watch: 60-minute minimum; 4 hours if adjacent to combustible construction; continuous during hot work; 35-foot combustible clearance radius | 2026-05-21 |
| ASSUME-NRC50-FP-006 | §50.48 fire brigade | Appendix R §III.D: minimum 5 members on-site at all times; quarterly drills; 1 unannounced drill per year; annual refresher training; annual SCBA qualification | 2026-05-21 |
| ASSUME-NRC50-FP-007 | §50.48 safe shutdown | SSA required for all fire areas; walk-down validation of manual operator actions required; FICFA required for cable routing zones | 2026-05-21 |

---

## Contested items

| Item | Reason | Resolution path |
|---|---|---|
| Safe shutdown analysis adequacy | Whether the SSA correctly identifies all required SSCs and demonstrates post-fire shutdown capability requires fire protection engineering and nuclear systems engineering judgment | Fire protection engineer evaluation; NRC resident inspector review; inspection findings as feedback |
| Manual operator action feasibility | Post-fire route accessibility, timing, smoke conditions, and equipment availability with fire-induced circuit failures requires HRA walk-down in actual plant conditions | Walk-down by qualified fire protection and licensed operator personnel; HRA documentation |
| Fire barrier equivalency (Appendix R §III.G.2.b/c alternatives) | Whether a 1-hour barrier + suppression/detection combination provides equivalent protection to a 3-hour barrier requires fire modeling or engineering judgment | NRC-approved equivalency evaluation or NRC license amendment |
| NFPA 805 fire risk performance goals | Whether current plant configuration meets NFPA 805 CDF/LERF performance goals (ΔCDFfire ≤ 1×10⁻⁵/yr; ΔLERFfire ≤ 1×10⁻⁶/yr) requires updated fire PRA model | Full fire PRA peer review; NRC review of §50.48(c) license amendment |

---

## Cross-standard dependencies

| Artifact | Dependencies |
|---|---|
| Fire brigade staffing shortfall | §50.72(b)(3) — inability to perform safe shutdown is an 8-hour notification condition; staffing shortfall that impairs fire response capability may require §50.72 notification |
| Hot work permit lapses / missed fire watch | App. B Criterion XVI corrective action — repeated administrative procedure violations require SCAQ root cause analysis |
| Fire protection program changes | §50.59 — changes to the fire protection program (fire areas, SSCs, barriers, detection) must be evaluated under §50.59 to determine if an unreviewed safety question exists |
| Fire suppression system impairments | Technical Specification Limiting Conditions for Operation — fire suppression system outages require TS LCO entry and action time compliance; also tracked under §50.65 Maintenance Rule |
| §50.48(c) NFPA 805 transition | §50.59 — implementing changes necessary for NFPA 805 transition requires §50.59 screening; the license amendment itself addresses most changes but implementation details may require individual §50.59 evaluations |
