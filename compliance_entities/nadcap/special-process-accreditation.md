# NADCAP — Special Process Accreditation Controls

**Framework:** NADCAP (AC7000 series checklists — PRI / IAQG subscriber-driven)
**Commodities:** Heat Treatment (AC7102), NDT (AC7004+), Welding (AC7110 series), Chemical Processing (AC7108/AC7115), Electronics (AC7120 series)
**Confidence:** DETERMINISTIC-dominant (specification compliance, operator qualification currency, calibration currency, job traveler completeness, NCR closure)
**Last parsed:** 2026-05-21

---

## Scope pre-condition

```python
@pytest.fixture(autouse=True)
def nadcap_scope(entity_profile: dict):
    """Skip unless organization performs NADCAP-scope special processes for aerospace customers."""
    if not entity_profile.get("nadcap_in_scope", False):
        pytest.skip("NADCAP not in scope")
```

---

## Constants

```python
# Certification renewal period — all IPC/NADCAP operator certs
NADCAP_OPERATOR_CERT_MAX_MONTHS = 24  # 2-year recertification cycle for most commodities

# Heat treatment — AMS 2750 calibration requirements
NADCAP_TUS_MAX_INTERVAL_DAYS = 180   # temperature uniformity survey; varies by AMS 2750 class
NADCAP_SAT_MAX_INTERVAL_DAYS = 92    # system accuracy test (quarterly typical)

# NDT — technician certification per NAS 410 / EN 4179
NADCAP_NDT_CERTIFICATION_STANDARDS = frozenset({
    "NAS_410",
    "EN_4179",
    "ASNT_SNT_TC_1A",  # employer-based alternative — verify customer acceptance
})
NADCAP_NDT_CERTIFICATION_MAX_YEARS = 5  # Level II/III renewal; per NAS 410 §10

# Welding — WPS/PQR standards
NADCAP_WELDING_PROCEDURE_STANDARDS = frozenset({
    "AWS_D1.1",
    "AWS_D17.1",    # aerospace welding
    "ASME_IX",      # pressure equipment
    "AMS_2680",     # electron beam welding
    "AMS_2681",     # laser beam welding
})

# NADCAP accreditation duration
NADCAP_STANDARD_ACCREDITATION_MONTHS = 12
NADCAP_EXTENDED_ACCREDITATION_MONTHS = 18   # merit-based; zero major findings required
```

---

## Common Elements (All Commodities)

**Overall: DETERMINISTIC — Pattern 1**

```python
import pytest
from datetime import date, timedelta

class TestNADCAPCommonElements:
    """Common across all NADCAP commodities: spec compliance, calibration, qualifications, job records."""

    def test_applicable_customer_specifications_at_current_revision(
        self, controls_evidence: dict
    ):
        nadcap = controls_evidence.get("nadcap_common", {})
        specs = controls_evidence.get("nadcap_specifications", [])
        outdated = [s for s in specs if not s.get("at_current_revision", False)]
        assert not outdated, (
            f"All customer and industry specifications invoked on purchase orders must be "
            f"at the current revision at time of use (NADCAP AC7000 series — common). "
            f"Outdated: {[s['spec_id'] for s in outdated]}"
        )

    def test_process_equipment_calibrations_current(
        self, controls_evidence: dict, reference_date: date
    ):
        equipment = controls_evidence.get("nadcap_process_equipment", [])
        expired = [
            e for e in equipment
            if e.get("calibration_due_date") is not None
            and e["calibration_due_date"] < reference_date
        ]
        assert not expired, (
            f"All process equipment must have current calibration at time of audit/use. "
            f"Expired calibrations: {[e['equipment_id'] for e in expired]} "
            f"(NADCAP AC7000 series — common)"
        )

    def test_operator_qualifications_current(
        self, controls_evidence: dict, reference_date: date
    ):
        operators = controls_evidence.get("nadcap_operators", [])
        expired_qual = [
            o for o in operators
            if o.get("qualification_expiry_date") is not None
            and o["qualification_expiry_date"] < reference_date
        ]
        assert not expired_qual, (
            f"All operators must have current qualifications for their assigned process. "
            f"Expired qualifications: {[o['operator_id'] for o in expired_qual]} "
            f"(NADCAP AC7000 series — common)"
        )

    def test_job_travelers_complete_for_audited_jobs(
        self, controls_evidence: dict
    ):
        job_travelers = controls_evidence.get("nadcap_job_travelers", [])
        incomplete = [
            jt for jt in job_travelers
            if not jt.get("all_required_entries_present", False)
        ]
        assert not incomplete, (
            f"Job travelers must have all required entries completed for each job "
            f"processed under NADCAP scope (NADCAP common — AC7000 series). "
            f"Incomplete: {[jt['job_id'] for jt in incomplete]}"
        )

    def test_material_certifications_traceable_to_each_job(
        self, controls_evidence: dict
    ):
        job_travelers = controls_evidence.get("nadcap_job_travelers", [])
        no_material_cert = [
            jt for jt in job_travelers
            if not jt.get("material_certification_traceable", False)
        ]
        assert not no_material_cert, (
            f"Raw material certifications must be traceable to each job/lot "
            f"(NADCAP common — AC7000 series). "
            f"Missing traceability: {[jt['job_id'] for jt in no_material_cert]}"
        )

    def test_nonconformances_documented_and_dispositioned(
        self, controls_evidence: dict
    ):
        ncrs = controls_evidence.get("nadcap_nonconformances", [])
        open_ncrs = [
            ncr for ncr in ncrs
            if not ncr.get("dispositioned", False)
        ]
        assert not open_ncrs, (
            f"All nonconformances must be documented and dispositioned "
            f"(NADCAP common). Open NCRs: {[ncr['ncr_id'] for ncr in open_ncrs]}"
        )

    def test_prior_nadcap_ncrs_closed_before_renewal(
        self, controls_evidence: dict
    ):
        prior_audit_ncrs = controls_evidence.get("nadcap_prior_audit_findings", [])
        unclosed = [
            f for f in prior_audit_ncrs
            if not f.get("closed_and_accepted_by_pri", False)
        ]
        assert not unclosed, (
            f"All findings from prior NADCAP audit must be closed and accepted by PRI "
            f"before accreditation renewal (NADCAP merit system). "
            f"Unclosed: {[f['finding_id'] for f in unclosed]}"
        )

    def test_accreditation_certificates_current(
        self, controls_evidence: dict, reference_date: date
    ):
        accreditations = controls_evidence.get("nadcap_accreditations", [])
        expired_accred = [
            a for a in accreditations
            if a.get("expiry_date") is not None
            and a["expiry_date"] < reference_date
        ]
        assert not expired_accred, (
            f"NADCAP accreditation certificates must be current for all commodity scopes "
            f"being performed (NADCAP). "
            f"Expired: {[a['commodity'] for a in expired_accred]}"
        )
```

---

## Heat Treatment (AC7102 / AMS 2750)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestNADCAPHeatTreatment:
    """AC7102 — Furnace TUS and SAT at AMS 2750 required intervals; load records complete."""

    def test_temperature_uniformity_surveys_current(
        self, controls_evidence: dict, reference_date: date
    ):
        furnaces = controls_evidence.get("nadcap_ht_furnaces", [])
        tus_overdue = [
            f for f in furnaces
            if f.get("last_tus_date") is not None
            and f["last_tus_date"] + timedelta(days=NADCAP_TUS_MAX_INTERVAL_DAYS) < reference_date
        ]
        assert not tus_overdue, (
            f"Temperature Uniformity Surveys (TUS) must be performed at AMS 2750 required "
            f"intervals (≤{NADCAP_TUS_MAX_INTERVAL_DAYS} days typical). "
            f"Overdue furnaces: {[f['furnace_id'] for f in tus_overdue]} "
            f"(NADCAP AC7102 / AMS 2750)"
        )

    def test_system_accuracy_tests_current(
        self, controls_evidence: dict, reference_date: date
    ):
        furnaces = controls_evidence.get("nadcap_ht_furnaces", [])
        sat_overdue = [
            f for f in furnaces
            if f.get("last_sat_date") is not None
            and f["last_sat_date"] + timedelta(days=NADCAP_SAT_MAX_INTERVAL_DAYS) < reference_date
        ]
        assert not sat_overdue, (
            f"System Accuracy Tests (SAT) must be performed at required intervals "
            f"(≤{NADCAP_SAT_MAX_INTERVAL_DAYS} days / quarterly typical per AMS 2750). "
            f"Overdue: {[f['furnace_id'] for f in sat_overdue]} "
            f"(NADCAP AC7102 / AMS 2750)"
        )

    def test_heat_treat_load_records_complete(self, controls_evidence: dict):
        loads = controls_evidence.get("nadcap_ht_loads", [])
        incomplete_records = [
            load for load in loads
            if not load.get("load_record_complete", False)
        ]
        assert not incomplete_records, (
            f"Each heat treatment load must have complete records including: furnace ID, "
            f"load number, parts processed, process parameters, operator signature "
            f"(NADCAP AC7102). Incomplete: {[load['load_id'] for load in incomplete_records]}"
        )

    def test_process_charts_retained_for_each_load(self, controls_evidence: dict):
        loads = controls_evidence.get("nadcap_ht_loads", [])
        no_charts = [
            load for load in loads
            if not load.get("process_chart_retained", False)
        ]
        assert not no_charts, (
            f"Time-temperature charts or electronic records must be retained for every "
            f"heat treat load (NADCAP AC7102). "
            f"Missing: {[load['load_id'] for load in no_charts]}"
        )
```

---

## NDT — Non-Destructive Testing (AC7004 series)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestNADCAPNDT:
    """AC7004 — NDT technician certification; technique sheets; reference standards current."""

    def test_ndt_technicians_certified_per_approved_standard(
        self, controls_evidence: dict
    ):
        technicians = controls_evidence.get("nadcap_ndt_technicians", [])
        noncompliant = [
            t for t in technicians
            if t.get("certification_standard") not in NADCAP_NDT_CERTIFICATION_STANDARDS
        ]
        assert not noncompliant, (
            f"NDT technicians must be certified per NAS 410, EN 4179, or customer-approved "
            f"equivalent (NADCAP AC7004). Non-compliant: "
            f"{[t['technician_id'] for t in noncompliant]}"
        )

    def test_ndt_technician_certifications_current(
        self, controls_evidence: dict, reference_date: date
    ):
        technicians = controls_evidence.get("nadcap_ndt_technicians", [])
        expired = [
            t for t in technicians
            if t.get("certification_expiry_date") is not None
            and t["certification_expiry_date"] < reference_date
        ]
        assert not expired, (
            f"NDT technician certifications must be current — max {NADCAP_NDT_CERTIFICATION_MAX_YEARS} "
            f"years per NAS 410 §10 (NADCAP AC7004). "
            f"Expired: {[t['technician_id'] for t in expired]}"
        )

    def test_written_technique_sheets_approved(self, controls_evidence: dict):
        techniques = controls_evidence.get("nadcap_ndt_techniques", [])
        not_approved = [t for t in techniques if not t.get("written_procedure_approved", False)]
        assert not not_approved, (
            f"Written NDT technique sheets/procedures must be approved by Level III or "
            f"designated authority before use (NADCAP AC7004). "
            f"Not approved: {[t['technique_id'] for t in not_approved]}"
        )

    def test_reference_standards_and_calibration_blocks_traceable(
        self, controls_evidence: dict
    ):
        ref_standards = controls_evidence.get("nadcap_ndt_reference_standards", [])
        not_traceable = [
            s for s in ref_standards
            if not s.get("traceable_to_national_standard", False)
        ]
        assert not not_traceable, (
            f"NDT reference standards and calibration blocks must be traceable to "
            f"national/international standards (NADCAP AC7004). "
            f"Not traceable: {[s['standard_id'] for s in not_traceable]}"
        )

    def test_level_certification_matches_task_performed(
        self, controls_evidence: dict
    ):
        ndt_jobs = controls_evidence.get("nadcap_ndt_jobs", [])
        wrong_level = [
            j for j in ndt_jobs
            if not j.get("technician_level_sufficient_for_task", False)
        ]
        assert not wrong_level, (
            f"NDT technician must hold certification level adequate for the task performed "
            f"(e.g., Level II for production testing per NAS 410). "
            f"Level mismatch: {[j['job_id'] for j in wrong_level]} (NADCAP AC7004)"
        )
```

---

## Welding (AC7110 series)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestNADCAPWelding:
    """AC7110 — WPS/PQR documented; welders qualified per applicable standard; filler certs traceable."""

    def test_welding_procedure_specifications_approved(
        self, controls_evidence: dict
    ):
        wpss = controls_evidence.get("nadcap_welding_procedures", [])
        not_approved = [w for w in wpss if not w.get("wps_approved", False)]
        assert not not_approved, (
            f"Welding Procedure Specifications (WPS) must be approved and supported by "
            f"Procedure Qualification Records (PQR) (NADCAP AC7110). "
            f"Not approved: {[w['wps_id'] for w in not_approved]}"
        )

    def test_welder_qualifications_current(
        self, controls_evidence: dict, reference_date: date
    ):
        welders = controls_evidence.get("nadcap_welders", [])
        expired = [
            w for w in welders
            if w.get("qualification_expiry_date") is not None
            and w["qualification_expiry_date"] < reference_date
        ]
        assert not expired, (
            f"Welder qualifications must be current per applicable standard (AWS D17.1, "
            f"ASME IX, etc.) (NADCAP AC7110). "
            f"Expired: {[w['welder_id'] for w in expired]}"
        )

    def test_filler_material_certifications_traceable_to_each_weld(
        self, controls_evidence: dict
    ):
        weld_jobs = controls_evidence.get("nadcap_weld_jobs", [])
        no_filler_cert = [
            j for j in weld_jobs
            if not j.get("filler_material_cert_traceable", False)
        ]
        assert not no_filler_cert, (
            f"Filler material certifications must be traceable to each welded assembly "
            f"(NADCAP AC7110). Missing: {[j['job_id'] for j in no_filler_cert]}"
        )
```

---

## Chemical Processing (AC7108 / AC7115)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestNADCAPChemicalProcessing:
    """AC7108/AC7115 — Bath chemistry recorded at required frequency; process sequence per spec."""

    def test_bath_chemistry_analyzed_at_required_frequency(
        self, controls_evidence: dict
    ):
        baths = controls_evidence.get("nadcap_chem_baths", [])
        analysis_overdue = [
            b for b in baths
            if not b.get("chemistry_analyzed_at_required_frequency", False)
        ]
        assert not analysis_overdue, (
            f"Chemical bath chemistry must be analyzed at the frequency specified in the "
            f"process specification (NADCAP AC7108/AC7115). "
            f"Overdue analysis: {[b['bath_id'] for b in analysis_overdue]}"
        )

    def test_bath_chemistry_results_within_process_limits(
        self, controls_evidence: dict
    ):
        baths = controls_evidence.get("nadcap_chem_baths", [])
        out_of_range = [
            b for b in baths
            if not b.get("current_chemistry_within_process_limits", True)
        ]
        assert not out_of_range, (
            f"Chemical bath chemistry must be within process limits defined by the "
            f"specification at time of processing (NADCAP AC7108/AC7115). "
            f"Out of range: {[b['bath_id'] for b in out_of_range]}"
        )

    def test_process_sequence_followed_per_specification(
        self, controls_evidence: dict
    ):
        chem_jobs = controls_evidence.get("nadcap_chem_jobs", [])
        sequence_violations = [
            j for j in chem_jobs
            if not j.get("process_sequence_followed", False)
        ]
        assert not sequence_violations, (
            f"Chemical processing sequence (pre-clean, etch, rinse, conversion coat, etc.) "
            f"must match the approved process specification sequence "
            f"(NADCAP AC7108/AC7115). Violations: {[j['job_id'] for j in sequence_violations]}"
        )

    def test_solution_analysis_records_retained_per_batch(
        self, controls_evidence: dict
    ):
        baths = controls_evidence.get("nadcap_chem_baths", [])
        no_records = [b for b in baths if not b.get("analysis_records_retained", False)]
        assert not no_records, (
            f"Solution analysis records must be retained for traceability to each "
            f"processed lot (NADCAP AC7108/AC7115). "
            f"Missing: {[b['bath_id'] for b in no_records]}"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|

*(No open assumptions — NADCAP checklist requirements are prescriptive and DETERMINISTIC)*
