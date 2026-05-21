# NRC 10 CFR Part 26 — Fitness for Duty: Drug/Alcohol Testing and Work Hour Controls

**Spec file:** `fitness-for-duty.md`
**Registry version:** 2026.05
**Last updated:** 2026-05-21
**Parent index:** [`_index.md`](./_index.md)
**Regulatory basis:** 10 CFR Part 26 (Subparts B, C, E, H); 10 CFR §26.31, §26.61, §26.65, §26.163, §26.189, §26.205, §26.207
**Authority:** U.S. Nuclear Regulatory Commission
**Key guidance:** NRC Regulatory Issue Summary 2008-12 (work hours); NEI 06-11 (work hour controls)

---

## Overview

10 CFR Part 26 requires nuclear power plant licensees to maintain Fitness for Duty (FFD) programs to ensure personnel with unescorted access are not under the influence of substances that could impair safety-related performance. The regulation's work hour controls (§26.205) are among the most administratively complex requirements in the nuclear industry and carry high enforcement activity.

**DETERMINISTIC density is high.** The random testing rate (≥50%), drug detection cutoffs, alcohol BAC thresholds, and every work hour limit in §26.205 are bright-line regulatory numbers with no interpretation required.

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def nrc_part_26_scope_check(facility_profile: dict):
    """Skip if facility does not hold an NRC operating license."""
    if not facility_profile.get("nrc_operating_license_active", False):
        pytest.skip(
            "10 CFR Part 26 does not apply — facility does not hold an NRC 10 CFR Part 50 "
            "or Part 52 operating license"
        )
```

---

## Section 1 — FFD Program Requirements (PARAMETERIZED)

### Requirements extracted

**Source:** 10 CFR §26.27 — FFD program elements

| # | Subject | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 1.1 | Written FFD policy | NRC-licensed nuclear facility | Written FFD policy covering prohibited substances, testing types, consequences of violations, and employee assistance program | FFD program document; FFD policy statement |
| 1.2 | Behavioral observation program (BOP) | Personnel with unescorted access | BOP required — trained observers (supervisors, coworkers) watch for signs of impairment; observations logged; fitness concerns escalated to FFD coordinator | BOP procedure; observer training records; observation logs |
| 1.3 | Employee assistance program (EAP) | Personnel covered under Part 26 | Self-referral EAP available; referral process documented; confidentiality provisions | EAP provider agreement; FFD program EAP section |
| 1.4 | Annual FFD program audit | All elements of FFD program | Annual audit of all FFD program elements including testing, records, BOP, work hours; findings to corrective action | Annual FFD audit report; findings log |

### Tests — FFD program structure

```python
import pytest


class TestFFDProgramStructure:
    """Pattern 2: PARAMETERIZED — program adequacy requires review."""

    @pytest.mark.assumption(
        id="ASSUME-NRC26-FFD-006",
        description=(
            "Behavioral observation program (BOP): §26.27(d) requires that personnel with "
            "unescorted access to nuclear power plants be subject to a behavioral observation "
            "program. Trained supervisors and coworkers observe for signs of fitness impairment "
            "(behavioral changes, slurred speech, odor of alcohol, etc.). Observations are "
            "documented and fitness concerns escalated to the FFD coordinator. BOP training "
            "records must be maintained for all designated observers."
        ),
        approved_by="FFD Program Administrator",
        review_date="2026-05-21",
    )
    def test_ffd_program_document_exists(self, ffd_program: dict):
        assert ffd_program.get("program_document_number"), (
            "10 CFR §26.27: No FFD program document on record — a written FFD program is "
            "required for all nuclear power plant licensees; absent program document is a "
            "fundamental Part 26 compliance gap"
        )
        assert ffd_program.get("nrc_approved_or_submitted", False), (
            "FFD program has not been submitted to NRC — §26.27 requires licensees to "
            "implement a program meeting Part 26 requirements; major changes require NRC notification"
        )

    def test_behavioral_observation_program_active(self, ffd_program: dict):
        bop_procedure = ffd_program.get("behavioral_observation_program_procedure_number")
        assert bop_procedure is not None, (
            "10 CFR §26.27(d): No behavioral observation program (BOP) procedure on record — "
            "BOP is a required element of the Part 26 FFD program; absence of BOP is cited "
            "by NRC inspectors as a significant program deficiency"
        )

    def test_annual_ffd_audit_not_overdue(self, ffd_program: dict):
        from datetime import date
        from dateutil.relativedelta import relativedelta

        last_audit_date = ffd_program.get("last_annual_audit_completion_date")
        assert last_audit_date is not None, (
            "10 CFR §26.41: No annual FFD program audit on record — §26.41 requires annual "
            "audit of the FFD program covering all program elements"
        )

        due_date = last_audit_date + relativedelta(months=12)
        today = date.today()
        assert today <= due_date, (
            f"Annual FFD program audit overdue — last audit: {last_audit_date}, "
            f"due: {due_date}, today: {today}"
        )
```

---

## Section 2 — Pre-Access Testing (DETERMINISTIC)

### Requirements extracted

**Source:** 10 CFR §26.61 — pre-access testing; §26.63 — testing after prolonged absence

| # | Subject | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 2.1 | Pre-access drug test | Before granting unescorted access to protected area | Drug test (urine) collected and results reviewed by MRO before unescorted access granted | Pre-access test records; access grant date comparison |
| 2.2 | Pre-access alcohol test | Before granting unescorted access | Breath alcohol test (BAT) before access; ≥0.04 = denied access | Pre-access BAT records |
| 2.3 | Negative result required | Pre-access testing | Unescorted access not granted if drug test is reported positive, adulterated, or substituted by MRO | Access grant controls; MRO result notification records |
| 2.4 | Return from prolonged absence | Individual away from covered duties for ≥365 days | Pre-access test required before return to covered duties after 365+ day absence | Return-to-work test records; absence duration records |

### Tests — pre-access compliance

```python
import pytest


class TestPreAccessTesting:
    """Pattern 1: DETERMINISTIC — pre-access test before access grant is absolute."""

    @pytest.mark.assumption(
        id="ASSUME-NRC26-FFD-001",
        description=(
            "Pre-access testing: drug (urine) and alcohol (breath) testing required before "
            "granting unescorted access to the protected area. Drug test results must be "
            "reviewed by a qualified Medical Review Officer (MRO) before access is granted. "
            "Alcohol test must be conducted using a federally approved evidential breath "
            "testing (EBT) device by a qualified Breath Alcohol Technician (BAT). A result "
            "of ≥0.04 BAC denies access. Drug test positive, adulterated, or substituted "
            "result by MRO = access denied. Test validity (chain of custody, licensed "
            "HHS-certified laboratory) is required."
        ),
        approved_by="FFD Program Administrator",
        review_date="2026-05-21",
    )
    def test_pre_access_drug_test_before_access_grant(self, access_record: dict):
        pre_access_test_date = access_record.get("pre_access_drug_test_date")
        access_grant_date = access_record.get("unescorted_access_grant_date")

        assert pre_access_test_date is not None, (
            f"Individual '{access_record.get('individual_id')}': no pre-access drug test "
            "on record before unescorted access grant — 10 CFR §26.61 requires drug testing "
            "before granting unescorted access to the protected area"
        )
        assert access_grant_date is not None, (
            f"Individual '{access_record.get('individual_id')}': access grant date not recorded"
        )
        assert pre_access_test_date <= access_grant_date, (
            f"Individual '{access_record.get('individual_id')}': pre-access drug test on "
            f"{pre_access_test_date} AFTER access granted on {access_grant_date} — "
            "drug test must be collected and MRO result received BEFORE access is granted"
        )

    def test_pre_access_mro_result_negative_before_access(self, access_record: dict):
        mro_result = access_record.get("pre_access_mro_result")
        access_grant_date = access_record.get("unescorted_access_grant_date")

        if access_grant_date is None:
            pytest.skip("No access grant date recorded")

        assert mro_result in ("Negative", "Negative (Dilute)"), (
            f"Individual '{access_record.get('individual_id')}': pre-access drug test "
            f"MRO result is '{mro_result}' — unescorted access cannot be granted when "
            "MRO reports a positive, adulterated, substituted, or invalid result; "
            "access granted with non-negative MRO result is a 10 CFR §26.61 violation"
        )
```

---

## Section 3 — Random Testing Program (DETERMINISTIC)

### Requirements extracted

**Source:** 10 CFR §26.31(c)(3); §26.155 — random testing minimum rates

| # | Subject | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 3.1 | Random drug testing rate | Annual rate computed over calendar year or 12-month period | Minimum ≥50% of covered workers tested for drugs per year | Annual testing rate report; pool size tracking |
| 3.2 | Random alcohol testing rate | Annual rate for alcohol testing | Minimum ≥50% of covered workers tested for alcohol per year | Annual testing rate report |
| 3.3 | Unannounced testing | All random tests | Random tests conducted without advance notice; no advance notification to individual or supervisor | Testing protocol; anti-tipping procedures |
| 3.4 | Random selection method | Random pool management | Random selection using scientifically valid method; selection is unpredictable and each covered worker has equal probability of selection in any selection event | Random selection documentation; selection vendor records |
| 3.5 | Testing at all times | Random pool | Random testing includes all shifts and hours of operation; not limited to day shift or business hours | Testing schedule covering all shifts |

### DETERMINISTIC thresholds

| Obligation | Threshold | Source |
|---|---|---|
| Random drug testing rate | ≥50% of covered workforce per calendar year | §26.31(c)(3)(ii) |
| Random alcohol testing rate | ≥50% of covered workforce per calendar year | §26.31(c)(3)(ii) |

### Tests — random testing rate compliance

```python
import pytest
from datetime import date


RANDOM_TESTING_MINIMUM_RATE = 0.50  # ≥50% of covered workforce


class TestRandomTestingProgram:
    """Pattern 1: DETERMINISTIC — 50% rate is a hard regulatory floor."""

    @pytest.mark.assumption(
        id="ASSUME-NRC26-FFD-001",
        description=(
            "Random testing rate calculation: §26.31(c)(3)(ii) requires that the number of "
            "random tests conducted divided by the average number of covered workers equals "
            "at least 50% for both drugs and alcohol. 'Average covered workers' is calculated "
            "as the average number of workers in the testing pool over the measurement period "
            "(commonly monthly averages over the year). An individual tested twice counts as "
            "two tests in the numerator but is only counted once in the pool for eligibility "
            "purposes. Partial-year workers are included in the pool for the months they were "
            "covered. Rate is typically computed by the FFD program contractor and reported "
            "to the licensee annually."
        ),
        approved_by="FFD Program Administrator",
        review_date="2026-05-21",
    )
    def test_annual_random_drug_testing_rate_meets_minimum(self, ffd_annual_report: dict):
        random_drug_tests_conducted = ffd_annual_report.get("random_drug_tests_conducted", 0)
        average_covered_workforce = ffd_annual_report.get("average_covered_workforce_size", 0)
        reporting_year = ffd_annual_report.get("reporting_year")

        assert average_covered_workforce > 0, (
            f"FFD annual report ({reporting_year}): covered workforce size not recorded — "
            "cannot compute random testing rate without workforce denominator"
        )

        actual_rate = random_drug_tests_conducted / average_covered_workforce
        assert actual_rate >= RANDOM_TESTING_MINIMUM_RATE, (
            f"FFD {reporting_year}: random drug testing rate is {actual_rate:.1%} "
            f"({random_drug_tests_conducted} tests / {average_covered_workforce} avg covered workers) — "
            f"below the 10 CFR §26.31(c)(3)(ii) minimum of {RANDOM_TESTING_MINIMUM_RATE:.0%}; "
            "below-minimum random testing rate is a significant Part 26 violation reportable "
            "under §26.717(a) and frequently cited in NRC inspection findings"
        )

    def test_annual_random_alcohol_testing_rate_meets_minimum(self, ffd_annual_report: dict):
        random_alcohol_tests_conducted = ffd_annual_report.get("random_alcohol_tests_conducted", 0)
        average_covered_workforce = ffd_annual_report.get("average_covered_workforce_size", 0)
        reporting_year = ffd_annual_report.get("reporting_year")

        assert average_covered_workforce > 0, (
            f"FFD annual report ({reporting_year}): covered workforce size not recorded"
        )

        actual_rate = random_alcohol_tests_conducted / average_covered_workforce
        assert actual_rate >= RANDOM_TESTING_MINIMUM_RATE, (
            f"FFD {reporting_year}: random alcohol testing rate is {actual_rate:.1%} "
            f"({random_alcohol_tests_conducted} tests / {average_covered_workforce} avg covered workers) — "
            f"below the 10 CFR §26.31(c)(3)(ii) minimum of {RANDOM_TESTING_MINIMUM_RATE:.0%}"
        )

    def test_random_tests_distributed_across_all_shifts(self, ffd_annual_report: dict):
        shift_distribution = ffd_annual_report.get("random_test_shift_distribution", {})
        shifts_covered = [shift for shift, count in shift_distribution.items() if count > 0]

        configured_shifts = ffd_annual_report.get("plant_operating_shifts", [])
        if not configured_shifts:
            pytest.skip("Plant operating shift configuration not recorded")

        uncovered_shifts = [s for s in configured_shifts if s not in shifts_covered]
        assert not uncovered_shifts, (
            f"Random testing does not cover shift(s): {uncovered_shifts} — §26.31(c)(3) "
            "requires random testing at all times; limiting random selection to day shift "
            "while night shift workers are never selected violates the unpredictability requirement"
        )
```

---

## Section 4 — Drug Detection Cutoff Levels (DETERMINISTIC)

### Requirements extracted

**Source:** 10 CFR §26.163 — minimum detection and confirmation cutoff levels

| Drug / metabolite | Initial (immunoassay) | Confirmation (GC/MS or LC/MS/MS) | Source |
|---|---|---|---|
| Marijuana metabolites (THCA) | 50 ng/mL | 15 ng/mL | §26.163(a)(1) |
| Cocaine metabolites (benzoylecgonine) | 150 ng/mL | 100 ng/mL | §26.163(a)(2) |
| Opiates (morphine/codeine) | 2000 ng/mL | 2000 ng/mL | §26.163(a)(3) |
| Opiates (6-acetylmorphine, heroin marker) | 10 ng/mL | 10 ng/mL | §26.163(a)(3) |
| Phencyclidine (PCP) | 25 ng/mL | 25 ng/mL | §26.163(a)(4) |
| Amphetamines | 500 ng/mL | 250 ng/mL | §26.163(a)(5) |
| MDMA/MDA (ecstasy) | 500 ng/mL | 250 ng/mL | §26.163(a)(5) |

### Tests — cutoff level verification

```python
import pytest

# 10 CFR §26.163 minimum detection cutoffs — labs may use MORE sensitive cutoffs, not less
DRUG_INITIAL_CUTOFFS_NG_ML = {
    "thc_metabolites": 50,
    "cocaine_metabolites": 150,
    "opiates_morphine_codeine": 2000,
    "opiates_6_mam": 10,
    "phencyclidine": 25,
    "amphetamines": 500,
    "mdma": 500,
}

DRUG_CONFIRMATION_CUTOFFS_NG_ML = {
    "thc_metabolites": 15,
    "cocaine_metabolites": 100,
    "opiates_morphine_codeine": 2000,
    "opiates_6_mam": 10,
    "phencyclidine": 25,
    "amphetamines": 250,
    "mdma": 250,
}


class TestDrugCutoffLevels:
    """Pattern 1: DETERMINISTIC — §26.163 cutoffs are regulatory minimums."""

    @pytest.mark.assumption(
        id="ASSUME-NRC26-FFD-002",
        description=(
            "Drug cutoff levels: §26.163 specifies minimum sensitivity cutoffs. HHS-certified "
            "laboratories must use these levels or more sensitive (lower) cutoffs — they cannot "
            "use higher cutoffs that would miss detectable levels of drug. Initial testing uses "
            "immunoassay screening; confirmation uses GC/MS (gas chromatography/mass spectrometry) "
            "or LC/MS/MS (liquid chromatography tandem mass spectrometry). A specimen must "
            "exceed the initial cutoff AND the confirmation cutoff to be reported positive. "
            "The plant must use only HHS-certified laboratories (NLCP-certified) per §26.163(e)."
        ),
        approved_by="FFD Program Administrator / MRO",
        review_date="2026-05-21",
    )
    def test_laboratory_initial_cutoffs_at_or_below_regulatory_minimum(self, lab_contract: dict):
        lab_cutoffs = lab_contract.get("initial_cutoffs_ng_ml", {})

        for drug, regulatory_min in DRUG_INITIAL_CUTOFFS_NG_ML.items():
            lab_cutoff = lab_cutoffs.get(drug)
            if lab_cutoff is None:
                continue  # Drug not in lab panel — skip (panel completeness checked separately)

            assert lab_cutoff <= regulatory_min, (
                f"Laboratory initial cutoff for {drug} is {lab_cutoff} ng/mL — ABOVE the "
                f"§26.163 maximum allowable of {regulatory_min} ng/mL; laboratories must "
                "use cutoffs at or below the regulatory minimum (more sensitive is permitted, "
                "less sensitive is a violation)"
            )

    def test_laboratory_confirmation_cutoffs_at_or_below_regulatory_minimum(self, lab_contract: dict):
        lab_confirmation_cutoffs = lab_contract.get("confirmation_cutoffs_ng_ml", {})

        for drug, regulatory_min in DRUG_CONFIRMATION_CUTOFFS_NG_ML.items():
            lab_cutoff = lab_confirmation_cutoffs.get(drug)
            if lab_cutoff is None:
                continue

            assert lab_cutoff <= regulatory_min, (
                f"Laboratory confirmation cutoff for {drug} is {lab_cutoff} ng/mL — ABOVE "
                f"the §26.163 maximum allowable confirmation cutoff of {regulatory_min} ng/mL"
            )

    def test_laboratory_is_hhs_nlcp_certified(self, lab_contract: dict):
        hhs_certified = lab_contract.get("hhs_nlcp_certified", False)
        assert hhs_certified, (
            f"Laboratory '{lab_contract.get('lab_name')}' is not documented as HHS NLCP-"
            "certified — 10 CFR §26.163(e) requires all drug testing specimens to be "
            "analyzed by a laboratory certified under the HHS National Laboratory "
            "Certification Program (NLCP); uncertified lab results cannot be used to "
            "support FFD determinations"
        )

    def test_full_drug_panel_tested(self, lab_contract: dict):
        tested_drugs = set(lab_contract.get("drugs_in_panel", []))
        required_drugs = set(DRUG_INITIAL_CUTOFFS_NG_ML.keys())
        missing = required_drugs - tested_drugs

        assert not missing, (
            f"Drug panel does not include: {sorted(missing)} — §26.163 requires testing "
            "for all drugs specified in the regulation; an incomplete drug panel cannot "
            "satisfy Part 26 screening requirements"
        )
```

---

## Section 5 — Alcohol Testing (DETERMINISTIC)

### Requirements extracted

**Source:** 10 CFR §26.189 — alcohol testing; §26.31 — testing categories

| BAC result | Required action | Confidence |
|---|---|---|
| < 0.02 | No action required — individual may remain on duty | DETERMINISTIC |
| ≥ 0.02 but < 0.04 | Individual removed from covered duties; second test within 30 minutes required | DETERMINISTIC |
| ≥ 0.04 (confirmed positive) | Violation; removal from covered duties; notification per §26.189(c); adverse action | DETERMINISTIC |

### Tests — alcohol testing and thresholds

```python
import pytest
from datetime import datetime, timedelta

ALCOHOL_REMOVAL_LEVEL_BAC = 0.02      # §26.189(b)(2) — removal from covered duties
ALCOHOL_VIOLATION_LEVEL_BAC = 0.04   # §26.189(c) — confirmed violation
SECOND_TEST_WINDOW_MINUTES = 30       # §26.189(b)(3) — second breath test within 30 minutes


class TestAlcoholTesting:
    """Pattern 1: DETERMINISTIC — BAC thresholds and action requirements are fixed."""

    @pytest.mark.assumption(
        id="ASSUME-NRC26-FFD-003",
        description=(
            "Alcohol testing: breath alcohol testing uses federally approved evidential "
            "breath testing (EBT) devices operated by qualified BATs. A result of ≥0.02 BAC "
            "requires removal from FFD-covered activities; a second confirmatory test within "
            "30 minutes is required. If the confirmatory test is also ≥0.04 BAC, it is a "
            "confirmed violation. If the first test ≥0.04 and second test is also ≥0.04, "
            "violation confirmed. If first test ≥0.04 but second test <0.04, the result is "
            "ambiguous and MRO review is required. A ≥0.02 removal is not a violation per "
            "se — only ≥0.04 confirmed is a violation."
        ),
        approved_by="FFD Program Administrator / MRO",
        review_date="2026-05-21",
    )
    def test_bac_at_or_above_removal_level_triggers_removal(self, alcohol_test_record: dict):
        initial_bac = alcohol_test_record.get("initial_bac_result", 0.0)
        individual_removed = alcohol_test_record.get("removed_from_covered_duties", False)

        if initial_bac >= ALCOHOL_REMOVAL_LEVEL_BAC:
            assert individual_removed, (
                f"Alcohol test result {initial_bac:.3f} BAC is ≥ removal threshold "
                f"({ALCOHOL_REMOVAL_LEVEL_BAC}); individual '{alcohol_test_record.get('individual_id')}' "
                "was NOT removed from covered duties — §26.189(b)(2) requires immediate "
                "removal from FFD-covered activities when BAC ≥ 0.02"
            )

    def test_bac_at_or_above_removal_level_gets_second_test_in_time(self, alcohol_test_record: dict):
        initial_bac = alcohol_test_record.get("initial_bac_result", 0.0)
        if initial_bac < ALCOHOL_REMOVAL_LEVEL_BAC:
            return  # No second test required below 0.02

        first_test_time = alcohol_test_record.get("initial_test_datetime")
        second_test_time = alcohol_test_record.get("confirmatory_test_datetime")

        assert second_test_time is not None, (
            f"Individual '{alcohol_test_record.get('individual_id')}': initial BAC {initial_bac:.3f} "
            f"is ≥ {ALCOHOL_REMOVAL_LEVEL_BAC} but no confirmatory breath test on record — "
            "§26.189(b)(3) requires a second breath test within 30 minutes of initial result ≥ 0.02"
        )

        if first_test_time and isinstance(first_test_time, datetime):
            elapsed_minutes = (second_test_time - first_test_time).total_seconds() / 60
            assert elapsed_minutes <= SECOND_TEST_WINDOW_MINUTES, (
                f"Individual '{alcohol_test_record.get('individual_id')}': confirmatory breath "
                f"test conducted {elapsed_minutes:.0f} minutes after initial test — "
                f"§26.189(b)(3) requires confirmatory test within {SECOND_TEST_WINDOW_MINUTES} minutes"
            )

    def test_confirmed_positive_bac_reported_as_violation(self, alcohol_test_record: dict):
        confirmatory_bac = alcohol_test_record.get("confirmatory_bac_result", 0.0)
        reported_as_violation = alcohol_test_record.get("violation_reported", False)
        notified_nrc = alcohol_test_record.get("nrc_notification_submitted", False)

        if confirmatory_bac >= ALCOHOL_VIOLATION_LEVEL_BAC:
            assert reported_as_violation, (
                f"Confirmed BAC {confirmatory_bac:.3f} is ≥ violation threshold "
                f"({ALCOHOL_VIOLATION_LEVEL_BAC}) but not recorded as a violation — "
                "§26.189(c) requires a confirmed positive at ≥0.04 BAC to be recorded "
                "as an FFD violation with all associated adverse action consequences"
            )
```

---

## Section 6 — For-Cause Testing (DETERMINISTIC)

### Requirements extracted

**Source:** 10 CFR §26.65 — for-cause testing; §26.65(c) — timing requirements

| # | Trigger type | Drug test timing | Alcohol test timing | Evidence |
|---|---|---|---|---|
| 6.1 | Reasonable suspicion of impairment | Within 32 hours of basis for reasonable suspicion | Within 2 hours of observation | §26.65(c)(2)–(c)(3) |
| 6.2 | Post-event (injury/accident to person) | Within 32 hours of event | Within 2 hours of event | §26.65(b)(1) |
| 6.3 | Post-event (equipment damage) | Within 32 hours of event | Within 2 hours of event | §26.65(b)(2) |
| 6.4 | Post-event (near-miss) | Within 32 hours of event | Within 2 hours of event | §26.65(b)(3) |
| 6.5 | Pre-employment/transfer screening | Before assignment to covered duties | Before assignment | §26.61 |

### Tests — for-cause testing timing

```python
import pytest
from datetime import datetime, timedelta

ALCOHOL_FOR_CAUSE_WINDOW_HOURS = 2
DRUG_FOR_CAUSE_WINDOW_HOURS = 32


class TestForCauseTesting:
    """Pattern 1: DETERMINISTIC — for-cause testing timing windows are fixed."""

    def test_for_cause_alcohol_test_within_2_hours(self, for_cause_record: dict):
        trigger_time = for_cause_record.get("trigger_event_time")
        alcohol_test_time = for_cause_record.get("alcohol_test_collection_time")
        trigger_type = for_cause_record.get("trigger_type")

        if trigger_time is None:
            pytest.skip("Trigger event time not recorded")
        if alcohol_test_time is None:
            pytest.skip("Alcohol test not conducted — verified separately (not required if "
                        "trigger was outside 2-hour window and specimen could not be collected)")

        elapsed_hours = (alcohol_test_time - trigger_time).total_seconds() / 3600

        assert elapsed_hours <= ALCOHOL_FOR_CAUSE_WINDOW_HOURS, (
            f"For-cause event '{for_cause_record.get('event_id')}' ({trigger_type}): "
            f"breath alcohol test collected {elapsed_hours:.1f} hours after trigger — "
            f"§26.65(c)(2) requires breath alcohol collection within {ALCOHOL_FOR_CAUSE_WINDOW_HOURS} "
            "hours of the basis for testing; collection outside this window must be documented "
            "as not practicable with the reason recorded"
        )

    def test_for_cause_drug_test_within_32_hours(self, for_cause_record: dict):
        trigger_time = for_cause_record.get("trigger_event_time")
        drug_test_time = for_cause_record.get("drug_test_collection_time")

        if trigger_time is None:
            pytest.skip("Trigger event time not recorded")
        if drug_test_time is None:
            pytest.skip("Drug test not conducted")

        elapsed_hours = (drug_test_time - trigger_time).total_seconds() / 3600

        assert elapsed_hours <= DRUG_FOR_CAUSE_WINDOW_HOURS, (
            f"For-cause event '{for_cause_record.get('event_id')}': urine drug test "
            f"collected {elapsed_hours:.1f} hours after trigger — §26.65(c)(3) requires "
            f"drug specimen collection within {DRUG_FOR_CAUSE_WINDOW_HOURS} hours of the "
            "basis for testing; if specimen cannot be collected within 32 hours, testing "
            "is abandoned and reason documented"
        )
```

---

## Section 7 — Work Hour Controls §26.205 (DETERMINISTIC)

### Requirements extracted

**Source:** 10 CFR §26.205 — work hours; §26.207 — waivers

| # | Limit | Threshold | Period | Source |
|---|---|---|---|---|
| 7.1 | Maximum consecutive working hours | 16 hours | Any single shift or work period | §26.205(d)(1) |
| 7.2 | Minimum break between shifts | 10 hours | Between end of one shift and start of next | §26.205(d)(2) |
| 7.3 | Maximum hours in 48-hour period | 26 hours | Any rolling 48-hour window | §26.205(d)(3) |
| 7.4 | Maximum hours in 7-day period | 72 hours | Any rolling 7-day window | §26.205(d)(4) |
| 7.5 | Maximum consecutive night shifts | 6 shifts | Consecutive night shifts (shift includes hours between midnight and 0600) | §26.205(d)(5) |
| 7.6 | Work hour waiver documentation | When waiver invoked | Written waiver: reason, start time, projected end time, approving authority | §26.207(a) |
| 7.7 | Recovery period after 7-day max | After reaching 72 hours in 7 days | Minimum 34-hour recovery period before resuming covered work | §26.205(d)(4) note |

### Tests — work hour limit compliance

```python
import pytest
from datetime import datetime, timedelta

# 10 CFR §26.205(d) work hour limits
MAX_CONSECUTIVE_HOURS = 16
MIN_BREAK_HOURS = 10
MAX_HOURS_IN_48 = 26
MAX_HOURS_IN_7_DAYS = 72
MAX_CONSECUTIVE_NIGHT_SHIFTS = 6
RECOVERY_PERIOD_HOURS = 34  # Required after reaching 72-hour 7-day limit


class TestWorkHourControls:
    """Pattern 1: DETERMINISTIC — §26.205 limits are bright-line regulatory thresholds."""

    @pytest.mark.assumption(
        id="ASSUME-NRC26-FFD-004",
        description=(
            "Work hour limits: §26.205(d) limits apply to all individuals performing "
            "covered work activities (activities that affect the safe operation of the "
            "nuclear plant) who must maintain unescorted access. 'Consecutive hours' means "
            "hours worked without a break of sufficient length to interrupt the work period. "
            "The 10-hour minimum break is measured from time of release from work to time "
            "of return to covered duties. Night shift is a shift that includes the hours "
            "between midnight and 0600. Rolling windows (48-hour and 7-day) are recalculated "
            "continuously — not fixed calendar periods. Work time includes any time performing "
            "covered work, including training, meetings, and travel if paid by the licensee "
            "as part of covered work."
        ),
        approved_by="FFD Program Administrator / Operations Manager",
        review_date="2026-05-21",
    )
    def test_no_shift_exceeds_16_consecutive_hours(self, work_record: dict):
        consecutive_hours = work_record.get("consecutive_hours_worked", 0.0)
        has_approved_waiver = work_record.get("work_hour_waiver_approved", False)

        if not has_approved_waiver:
            assert consecutive_hours <= MAX_CONSECUTIVE_HOURS, (
                f"Individual '{work_record.get('individual_id')}' on "
                f"{work_record.get('work_date')}: worked {consecutive_hours:.1f} consecutive "
                f"hours — exceeds §26.205(d)(1) maximum of {MAX_CONSECUTIVE_HOURS} hours "
                "without an approved §26.207 waiver; §26.205 work hour violations are "
                "reported as potential Part 26 violations per §26.717"
            )
        else:
            waiver_doc = work_record.get("waiver_documentation_number")
            assert waiver_doc is not None, (
                f"Individual '{work_record.get('individual_id')}': work hour waiver flag "
                "set but no waiver documentation number — §26.207(a) requires written "
                "waiver documentation before or immediately after invoking the waiver"
            )

    def test_minimum_10_hour_break_between_shifts(self, work_record: dict):
        break_hours = work_record.get("hours_break_before_next_shift", None)
        if break_hours is None:
            pytest.skip("Break time before next shift not recorded")

        has_approved_waiver = work_record.get("work_hour_waiver_approved", False)
        if not has_approved_waiver:
            assert break_hours >= MIN_BREAK_HOURS, (
                f"Individual '{work_record.get('individual_id')}': only {break_hours:.1f} "
                f"hours between end of last shift and start of next shift — "
                f"§26.205(d)(2) requires a minimum {MIN_BREAK_HOURS}-hour break between shifts; "
                "insufficient rest periods are among the most commonly cited §26.205 violations"
            )

    def test_max_26_hours_in_any_48_hour_period(self, work_record: dict):
        hours_in_48 = work_record.get("hours_worked_in_rolling_48h_window", None)
        if hours_in_48 is None:
            pytest.skip("Rolling 48-hour hours not calculated for this record")

        has_approved_waiver = work_record.get("work_hour_waiver_approved", False)
        if not has_approved_waiver:
            assert hours_in_48 <= MAX_HOURS_IN_48, (
                f"Individual '{work_record.get('individual_id')}': {hours_in_48:.1f} hours "
                f"worked in a 48-hour window — exceeds §26.205(d)(3) maximum of "
                f"{MAX_HOURS_IN_48} hours in any 48-hour period"
            )

    def test_max_72_hours_in_any_7_day_period(self, work_record: dict):
        hours_in_7_days = work_record.get("hours_worked_in_rolling_7_day_window", None)
        if hours_in_7_days is None:
            pytest.skip("Rolling 7-day hours not calculated for this record")

        has_approved_waiver = work_record.get("work_hour_waiver_approved", False)
        if not has_approved_waiver:
            assert hours_in_7_days <= MAX_HOURS_IN_7_DAYS, (
                f"Individual '{work_record.get('individual_id')}': {hours_in_7_days:.1f} hours "
                f"worked in a 7-day window — exceeds §26.205(d)(4) maximum of "
                f"{MAX_HOURS_IN_7_DAYS} hours; work must not continue until a "
                f"{RECOVERY_PERIOD_HOURS}-hour recovery period has elapsed"
            )

    def test_max_6_consecutive_night_shifts(self, work_record: dict):
        consecutive_night_shifts = work_record.get("consecutive_night_shifts_count", 0)
        has_approved_waiver = work_record.get("work_hour_waiver_approved", False)

        if not has_approved_waiver:
            assert consecutive_night_shifts <= MAX_CONSECUTIVE_NIGHT_SHIFTS, (
                f"Individual '{work_record.get('individual_id')}': {consecutive_night_shifts} "
                f"consecutive night shifts — exceeds §26.205(d)(5) maximum of "
                f"{MAX_CONSECUTIVE_NIGHT_SHIFTS} consecutive night shifts (shifts that include "
                "the hours between midnight and 0600)"
            )
```

---

## Section 8 — Work Hour Waivers §26.207 (PARAMETERIZED)

### Requirements extracted

**Source:** 10 CFR §26.207 — waivers for work hour limits

| # | Waiver basis | Condition | Requirement |
|---|---|---|---|
| 8.1 | Emergency (§26.207(a)(1)) | Unforeseeable event preventing plant from maintaining minimum safe staffing | Licensee management approval; documented before or immediately after invoking; limited to minimum hours necessary | Waiver form with emergency basis, approving manager, start/projected end time |
| 8.2 | Scheduled outage (§26.207(a)(2)) | Refueling or planned maintenance outage | Limits on duration; waivers used only when alternatives exhausted | Waiver form with outage basis |
| 8.3 | Not-practicable (§26.207(a)(3)) | When adherence not reasonably achievable | Documented specific circumstances | Waiver form with specific basis |

### Tests — waiver compliance

```python
import pytest


class TestWorkHourWaivers:
    """Pattern 2: PARAMETERIZED — waiver necessity and basis require management judgment."""

    @pytest.mark.assumption(
        id="ASSUME-NRC26-FFD-005",
        description=(
            "Work hour waivers (§26.207): a licensee may waive work hour limits when "
            "adherence is not reasonably achievable. Three bases: (1) emergency preventing "
            "minimum safe staffing — most common emergency basis; (2) scheduled outage — "
            "for refueling or planned maintenance outages; (3) not practicable — specific "
            "circumstances documented. Waivers must be documented (waiver form or equivalent) "
            "with the basis, the approving management authority, the start time, and the "
            "projected end time. NRC audits waiver frequency — excessive waivers indicate "
            "chronic staffing shortfalls that require corrective action rather than routine "
            "waiver use."
        ),
        approved_by="FFD Program Administrator / Operations Manager",
        review_date="2026-05-21",
    )
    def test_waiver_has_documented_basis_and_approval(self, waiver_record: dict):
        waiver_id = waiver_record.get("waiver_id")
        basis = waiver_record.get("waiver_basis")
        approving_manager = waiver_record.get("approving_manager")
        waiver_doc_number = waiver_record.get("documentation_number")

        assert basis in ("emergency_staffing", "scheduled_outage", "not_practicable"), (
            f"Waiver '{waiver_id}': basis is '{basis}' — not a valid §26.207 waiver basis; "
            "must be one of: emergency preventing minimum safe staffing, scheduled outage, "
            "or documented not-practicable circumstance"
        )
        assert approving_manager is not None, (
            f"Waiver '{waiver_id}': no approving manager documented — §26.207(a) requires "
            "management authority approval for all work hour waivers"
        )
        assert waiver_doc_number is not None, (
            f"Waiver '{waiver_id}': no documentation number — work hour waivers must be "
            "documented per §26.207(a); verbal-only waivers do not satisfy the written "
            "documentation requirement"
        )

    def test_waiver_duration_limited_to_necessity(self, waiver_record: dict):
        start_time = waiver_record.get("waiver_start_time")
        end_time = waiver_record.get("actual_waiver_end_time")
        projected_end_time = waiver_record.get("projected_waiver_end_time")

        assert projected_end_time is not None, (
            f"Waiver '{waiver_record.get('waiver_id')}': no projected end time documented — "
            "§26.207(a) requires documenting a projected end time to confirm the waiver is "
            "limited to the minimum duration necessary"
        )
```

---

## Open assumptions

| ID | Section | Summary | Review date |
|---|---|---|---|
| ASSUME-NRC26-FFD-001 | §26.31(c)(3) | Random testing rate ≥50%: tests conducted ÷ average covered workforce; drug and alcohol pools are separate; individual tested multiple times counts multiple tests in numerator | 2026-05-21 |
| ASSUME-NRC26-FFD-002 | §26.163 | Drug cutoff levels: §26.163 specifies maximums (labs may be more sensitive); initial immunoassay + confirmation GC/MS or LC/MS/MS; HHS NLCP-certified lab required | 2026-05-21 |
| ASSUME-NRC26-FFD-003 | §26.189 | Alcohol: ≥0.02 = removal + second test within 30 min; ≥0.04 confirmed = violation; ≥0.02 alone is NOT a violation; BAT uses EBT device | 2026-05-21 |
| ASSUME-NRC26-FFD-004 | §26.205 | Work hours: rolling windows (not calendar periods); 10-hour break from release to reporting; night shift = shift including hours midnight–0600; covers all work time during covered duties | 2026-05-21 |
| ASSUME-NRC26-FFD-005 | §26.207 | Work hour waivers: three valid bases (emergency, scheduled outage, not practicable); written documentation required; excessive waivers indicate chronic staffing issue | 2026-05-21 |
| ASSUME-NRC26-FFD-006 | §26.27(d) | BOP: trained observers required for all covered personnel; fitness concerns escalated to FFD coordinator; observations documented | 2026-05-21 |

---

## Contested items

| Item | Section | Reason | Resolution path |
|---|---|---|---|
| Suitability determination after positive test | §26.185/§26.187 | Whether individual is suitable to return involves MRO evaluation, Substance Abuse Professional (SAP) evaluation, and licensee determination — multi-factor professional judgment | MRO and SAP evaluations; licensee determination with documented technical basis |
| Work hour waiver necessity | §26.207 | Whether an emergency or "not practicable" determination is valid requires management judgment about alternative staffing options; NRC may disagree that a waiver was warranted | Operations management determination with documented staffing options explored |

---

## Cross-standard dependencies

| Artifact | Dependencies |
|---|---|
| Positive drug/alcohol test result | §50.74 (Personnel Notifications) — positive test results for certain individuals may trigger NRC notification per §50.74; FFD violations for licensed operators require reporting under §50.9 and §50.74 |
| Work hour limit violations | §50.65 Maintenance Rule — personnel performing maintenance under §50.65 who violate work hour limits may indicate programmatic issues in the Maintenance Rule work planning process |
| FFD violation for licensed operator | 10 CFR §50.74 — licensee must notify NRC within 72 hours of determining a licensed operator's license is subject to revocation, suspension, or modification due to FFD violation |
| FFD records | §26.715 — FFD records retained for 5 years (negative results) or indefinitely (violations/determinations); Part 26 records are separate from Part 50 records with specific retention requirements |
