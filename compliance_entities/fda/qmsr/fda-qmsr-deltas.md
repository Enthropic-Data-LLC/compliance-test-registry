# FDA QMSR — 21 CFR Part 820 Deltas Over ISO 13485

**Framework:** FDA QMSR (21 CFR Part 820, effective 2026-02-02)
**Clauses:** §820.30 (DHF), §820.70(g) (software validation), §820.72 (calibration/OOC), §820.100 (CAPA 7-step), §820.180 (records/retention), §820.181 (DMR), §820.184 (DHR), §820.198 (complaints/MDR)
**Parent:** ISO 13485:2016 (fully incorporated by reference — all ISO 13485 requirements apply simultaneously)
**Confidence:** DETERMINISTIC-dominant (DHR/DMR/DHF completeness, MDR 30-day deadline, CAPA 7-step, record retention, FDA inspection access, software validation)
**Last parsed:** 2026-05-21
**Applies to:** Manufacturers of medical devices for the US market — Class I, II, and III device manufacturers and specification developers; component manufacturers whose components become part of a finished medical device
**Trigger:** Manufacturing or specification development for medical devices requiring FDA establishment registration under 21 CFR 807; QMSR (21 CFR 820) applies to finished device manufacturers; effective date February 2026 (aligning to ISO 13485:2016)
**Jurisdiction:** United States; extraterritorial — applies to foreign device manufacturers with devices distributed in the US
**Not applicable to:** Devices for export only (21 CFR 801.58); HCT/Ps regulated under 21 CFR 1271; combination products (additional requirements under 21 CFR 3 and 4); investigational devices in IDE studies (modified requirements)

---

## Scope pre-condition

```python
@pytest.fixture(autouse=True)
def fda_qmsr_scope(entity_profile: dict):
    if not entity_profile.get("fda_qmsr_in_scope", False):
        pytest.skip("FDA QMSR (21 CFR Part 820) not in scope")
```

**Note:** This file covers only FDA-specific requirements that supplement ISO 13485:2016. All ISO 13485 tests (see `iso/13485/`) apply simultaneously and are not repeated here.

---

## Constants

```python
# Records retention — §820.180
FDA_QMSR_RECORD_RETENTION_MIN_YEARS = 2
# Effective retention: max(2 years, device useful life) from device release date

# MDR reporting deadline — 21 CFR Part 803
FDA_MDR_DEATH_INJURY_MALFUNCTION_REPORTING_DAYS = 30  # calendar days from awareness
FDA_MDR_BASELINE_REPORT_REQUIRED = True  # for applicable device types

# CAPA — §820.100(a) 7 required steps
FDA_CAPA_REQUIRED_STEPS = frozenset({
    "analyze_data_to_identify_causes",       # (a)(1)
    "investigate_cause",                     # (a)(2)
    "identify_action_needed",                # (a)(3)
    "verify_or_validate_action",             # (a)(4)
    "implement_and_record_changes",          # (a)(5)
    "disseminate_information",               # (a)(6)
    "submit_for_management_review",          # (a)(7)
})

# Complaint record required fields — §820.198(d)–(f)
FDA_COMPLAINT_REQUIRED_FIELDS = frozenset({
    "device_name",
    "date_received",
    "unique_device_identifier_or_control_number",
    "complainant_name",
    "complainant_address",
    "nature_of_complaint",
    "investigation_dates",
    "investigation_results",
    "corrective_action_taken",
    "reply_to_complainant",
    "mdr_determination_documented",
})

# DHR required fields — §820.184
FDA_DHR_REQUIRED_FIELDS = frozenset({
    "dates_of_manufacture",
    "quantity_manufactured",
    "quantity_released_for_distribution",
    "acceptance_records",
    "primary_identification_label",
    "labeling_used_for_each_production_unit",
    "device_identification_and_control_number",
})

# DMR required content — §820.181
FDA_DMR_REQUIRED_CONTENT = frozenset({
    "device_specifications",
    "production_process_specifications",
    "quality_assurance_procedures",
    "packaging_and_labeling_specifications",
    "installation_maintenance_and_servicing_procedures",
})
```

---

## §820.181 — Device Master Record (DMR)

**Overall: DETERMINISTIC — Pattern 1**

```python
import pytest

class TestDeviceMasterRecord:
    """§820.181 — DMR: compilation of procedures and specifications for each device type."""

    def test_dmr_exists_for_each_finished_device_type(self, controls_evidence: dict):
        programs = controls_evidence.get("fda_qmsr_production_programs", [])
        missing_dmr = [p for p in programs if not p.get("dmr_exists", False)]
        assert not missing_dmr, (
            f"Device Master Record (DMR) must exist for each finished device type "
            f"(21 CFR Part 820 §820.181). Missing: {[p['device_type_id'] for p in missing_dmr]}"
        )

    def test_dmr_contains_required_content(self, controls_evidence: dict):
        programs = controls_evidence.get("fda_qmsr_production_programs", [])
        for program in programs:
            if not program.get("dmr_exists", False):
                continue
            present = set(program.get("dmr_content_present", []))
            missing = FDA_DMR_REQUIRED_CONTENT - present
            assert not missing, (
                f"DMR for device '{program['device_type_id']}' is missing required content: "
                f"{missing} (21 CFR Part 820 §820.181)"
            )

    def test_dmr_references_or_includes_dhf(self, controls_evidence: dict):
        programs = controls_evidence.get("fda_qmsr_production_programs", [])
        no_dhf_ref = [
            p for p in programs
            if p.get("dmr_exists", False)
            and not p.get("dmr_references_dhf", False)
        ]
        assert not no_dhf_ref, (
            f"DMR must include or reference the Design History File (DHF) "
            f"(21 CFR Part 820 §§820.181, 820.30(j)). "
            f"Missing DHF reference: {[p['device_type_id'] for p in no_dhf_ref]}"
        )
```

---

## §820.184 — Device History Record (DHR)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestDeviceHistoryRecord:
    """§820.184 — DHR: per-batch/lot record demonstrating the device was manufactured per DMR."""

    def test_dhr_exists_for_each_production_lot(self, controls_evidence: dict):
        production_lots = controls_evidence.get("fda_qmsr_production_lots", [])
        missing_dhr = [lot for lot in production_lots if not lot.get("dhr_exists", False)]
        assert not missing_dhr, (
            f"Device History Record (DHR) must exist for each production lot/batch "
            f"(21 CFR Part 820 §820.184). Missing: {[lot['lot_id'] for lot in missing_dhr]}"
        )

    def test_dhr_contains_required_fields(self, controls_evidence: dict):
        production_lots = controls_evidence.get("fda_qmsr_production_lots", [])
        for lot in production_lots:
            if not lot.get("dhr_exists", False):
                continue
            present = set(lot.get("dhr_fields_present", []))
            missing = FDA_DHR_REQUIRED_FIELDS - present
            assert not missing, (
                f"DHR for lot '{lot['lot_id']}' is missing required fields: "
                f"{missing} (21 CFR Part 820 §820.184)"
            )

    def test_dhr_demonstrates_compliance_with_dmr(self, controls_evidence: dict):
        production_lots = controls_evidence.get("fda_qmsr_production_lots", [])
        no_dmr_compliance = [
            lot for lot in production_lots
            if lot.get("dhr_exists", False)
            and not lot.get("dhr_demonstrates_dmr_compliance", False)
        ]
        assert not no_dmr_compliance, (
            f"DHR must demonstrate the device was manufactured in accordance with the DMR "
            f"(21 CFR Part 820 §820.184). "
            f"Non-compliant lots: {[lot['lot_id'] for lot in no_dmr_compliance]}"
        )
```

---

## §820.30(j) — Design History File (DHF)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestDesignHistoryFile:
    """§820.30(j) — DHF must contain or reference all records required to demonstrate design was developed per the design plan."""

    def test_dhf_exists_for_each_device_type(self, controls_evidence: dict):
        programs = controls_evidence.get("fda_qmsr_production_programs", [])
        missing_dhf = [p for p in programs if not p.get("dhf_exists", False)]
        assert not missing_dhf, (
            f"Design History File (DHF) must be maintained for each device type "
            f"(21 CFR Part 820 §820.30(j)). Missing: {[p['device_type_id'] for p in missing_dhf]}"
        )

    def test_dhf_demonstrates_design_plan_compliance(self, controls_evidence: dict):
        programs = controls_evidence.get("fda_qmsr_production_programs", [])
        incomplete_dhf = [
            p for p in programs
            if p.get("dhf_exists", False)
            and not p.get("dhf_demonstrates_design_plan_compliance", False)
        ]
        assert not incomplete_dhf, (
            f"DHF must contain or reference records sufficient to demonstrate the device was "
            f"developed in accordance with the approved design plan (21 CFR Part 820 §820.30(j)). "
            f"Incomplete: {[p['device_type_id'] for p in incomplete_dhf]}"
        )
```

---

## §820.70(g) — Automated Process Validation (Software Validation)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestSoftwareValidation:
    """§820.70(g) — Computer software used in production or QS must be validated for its intended use."""

    def test_production_and_qs_software_validated(self, controls_evidence: dict):
        software_systems = controls_evidence.get("fda_qmsr_software_systems", [])
        production_or_qs = [
            s for s in software_systems
            if s.get("used_in_production", False) or s.get("used_in_quality_system", False)
        ]
        not_validated = [s for s in production_or_qs if not s.get("validation_performed", False)]
        assert not not_validated, (
            f"All computer software used in production processes or quality system must be "
            f"validated for its intended use before use (21 CFR Part 820 §820.70(g)). "
            f"Not validated: {[s['system_id'] for s in not_validated]}"
        )

    def test_software_validation_records_retained(self, controls_evidence: dict):
        software_systems = controls_evidence.get("fda_qmsr_software_systems", [])
        validated = [s for s in software_systems if s.get("validation_performed", False)]
        no_records = [s for s in validated if not s.get("validation_records_retained", False)]
        assert not no_records, (
            f"Software validation records must be retained (21 CFR Part 820 §820.70(g)). "
            f"Missing records: {[s['system_id'] for s in no_records]}"
        )

    def test_software_changes_trigger_revalidation_or_impact_assessment(
        self, controls_evidence: dict
    ):
        software_changes = controls_evidence.get("fda_qmsr_software_changes", [])
        no_impact = [
            c for c in software_changes
            if not c.get("impact_assessment_performed", False)
            and not c.get("revalidation_performed", False)
        ]
        assert not no_impact, (
            f"Software changes must trigger revalidation or documented impact assessment "
            f"before implementation in production (21 CFR Part 820 §820.70(g)). "
            f"Missing: {[c['change_id'] for c in no_impact]}"
        )
```

---

## §820.72 — Out-of-Calibration Impact Assessment

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestOutOfCalibrationImpactAssessment:
    """§820.72 — Equipment found out of calibration: impact on product quality must be assessed."""

    def test_out_of_calibration_events_have_impact_assessment(
        self, controls_evidence: dict
    ):
        ooc_events = controls_evidence.get("fda_qmsr_out_of_calibration_events", [])
        no_impact_assessment = [
            e for e in ooc_events
            if not e.get("impact_assessment_performed", False)
        ]
        assert not no_impact_assessment, (
            f"Each out-of-calibration event must have a documented impact assessment "
            f"on product quality (21 CFR Part 820 §820.72). "
            f"Missing: {[e['event_id'] for e in no_impact_assessment]}"
        )

    def test_product_affected_by_ooc_equipment_disposition_documented(
        self, controls_evidence: dict
    ):
        ooc_events = controls_evidence.get("fda_qmsr_out_of_calibration_events", [])
        product_impacted = [
            e for e in ooc_events
            if e.get("product_potentially_affected", True)
        ]
        no_disposition = [
            e for e in product_impacted
            if not e.get("affected_product_disposition_documented", False)
        ]
        assert not no_disposition, (
            f"Product potentially affected by out-of-calibration equipment must have "
            f"documented disposition (21 CFR Part 820 §820.72). "
            f"Missing: {[e['event_id'] for e in no_disposition]}"
        )
```

---

## §820.100 — CAPA 7-Step Process

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestCAPA7Step:
    """§820.100 — CAPA procedure must implement all 7 required steps (§820.100(a)(1-7))."""

    def test_capa_procedure_documents_all_required_steps(
        self, controls_evidence: dict
    ):
        capa = controls_evidence.get("fda_qmsr_capa_system", {})
        assert capa.get("written_capa_procedure_exists", False), (
            "Written CAPA procedure required (21 CFR Part 820 §820.100)"
        )
        steps_covered = set(capa.get("procedure_steps_covered", []))
        missing_steps = FDA_CAPA_REQUIRED_STEPS - steps_covered
        assert not missing_steps, (
            f"CAPA procedure must address all 7 required steps (§820.100(a)(1-7)). "
            f"Missing steps: {missing_steps}"
        )

    def test_individual_capas_include_all_required_steps(
        self, controls_evidence: dict
    ):
        capa_records = controls_evidence.get("fda_qmsr_capa_records", [])
        for record in capa_records:
            steps_documented = set(record.get("steps_documented", []))
            missing = FDA_CAPA_REQUIRED_STEPS - steps_documented
            assert not missing, (
                f"CAPA record '{record['capa_id']}' is missing required steps: "
                f"{missing} (21 CFR Part 820 §820.100(a))"
            )

    def test_capa_effectiveness_verified_before_closure(
        self, controls_evidence: dict
    ):
        capa_records = controls_evidence.get("fda_qmsr_capa_records", [])
        closed_capas = [r for r in capa_records if r.get("closed", False)]
        no_effectiveness = [
            r for r in closed_capas
            if not r.get("effectiveness_verified", False)
        ]
        assert not no_effectiveness, (
            f"CAPA effectiveness must be verified before closure "
            f"(21 CFR Part 820 §820.100(a)(4)). "
            f"Missing verification: {[r['capa_id'] for r in no_effectiveness]}"
        )

    def test_capa_submitted_for_management_review(self, controls_evidence: dict):
        capa_records = controls_evidence.get("fda_qmsr_capa_records", [])
        not_reviewed = [
            r for r in capa_records
            if not r.get("submitted_for_management_review", False)
        ]
        assert not not_reviewed, (
            f"CAPA records must be submitted for management review "
            f"(21 CFR Part 820 §820.100(a)(7)). "
            f"Not submitted: {[r['capa_id'] for r in not_reviewed]}"
        )
```

---

## §820.198 — Complaint Files and MDR Determination

**Overall: DETERMINISTIC — Pattern 1**

```python
from datetime import date, timedelta

class TestComplaintFilesAndMDR:
    """§820.198 — Complaint handling; MDR reportability determination per complaint."""

    def test_complaint_records_contain_required_fields(
        self, controls_evidence: dict
    ):
        complaints = controls_evidence.get("fda_qmsr_complaints", [])
        for complaint in complaints:
            present = set(complaint.get("fields_documented", []))
            missing = FDA_COMPLAINT_REQUIRED_FIELDS - present
            assert not missing, (
                f"Complaint '{complaint['complaint_id']}' is missing required fields: "
                f"{missing} (21 CFR Part 820 §820.198(d)–(f))"
            )

    def test_every_complaint_has_mdr_reportability_determination(
        self, controls_evidence: dict
    ):
        complaints = controls_evidence.get("fda_qmsr_complaints", [])
        no_mdr_determination = [
            c for c in complaints
            if not c.get("mdr_determination_documented", False)
        ]
        assert not no_mdr_determination, (
            f"Every complaint must be evaluated and documented for MDR reportability "
            f"(21 CFR Part 820 §820.198(c) / 21 CFR Part 803). "
            f"Missing determination: {[c['complaint_id'] for c in no_mdr_determination]}"
        )

    def test_mdr_reportable_events_reported_within_30_days(
        self, controls_evidence: dict, reference_date: date
    ):
        complaints = controls_evidence.get("fda_qmsr_complaints", [])
        reportable = [
            c for c in complaints
            if c.get("mdr_reportable", False)
            and c.get("date_became_aware") is not None
        ]
        late_reports = [
            c for c in reportable
            if (
                c.get("mdr_submission_date") is None
                or c["mdr_submission_date"] > c["date_became_aware"] + timedelta(
                    days=FDA_MDR_DEATH_INJURY_MALFUNCTION_REPORTING_DAYS
                )
            )
            and c["date_became_aware"] + timedelta(
                days=FDA_MDR_DEATH_INJURY_MALFUNCTION_REPORTING_DAYS
            ) < reference_date
        ]
        assert not late_reports, (
            f"MDR-reportable events (death, serious injury, or malfunction) must be reported "
            f"to FDA within {FDA_MDR_DEATH_INJURY_MALFUNCTION_REPORTING_DAYS} calendar days "
            f"of becoming aware (21 CFR Part 803). "
            f"Late/missing reports: {[c['complaint_id'] for c in late_reports]}"
        )

    def test_oral_complaints_documented_upon_receipt(self, controls_evidence: dict):
        complaint_system = controls_evidence.get("fda_qmsr_complaint_system", {})
        assert complaint_system.get("oral_complaints_documented_on_receipt", False), (
            "Oral complaints must be documented upon receipt "
            "(21 CFR Part 820 §820.198(b))"
        )

    def test_designated_complaint_handling_unit_exists(self, controls_evidence: dict):
        complaint_system = controls_evidence.get("fda_qmsr_complaint_system", {})
        assert complaint_system.get("designated_complaint_unit_defined", False), (
            "A formally designated unit responsible for receiving, reviewing, and evaluating "
            "complaints must be established (21 CFR Part 820 §820.198(a))"
        )
```

---

## §820.180 — Record Retention and FDA Inspection Access

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestRecordRetentionAndFDAAccess:
    """§820.180 — Records: 2-year minimum retention; accessible to FDA investigators."""

    def test_records_retained_for_minimum_period(self, controls_evidence: dict):
        qms = controls_evidence.get("fda_qmsr_qms", {})
        retention_years = qms.get("record_retention_years_configured")
        assert retention_years is not None and retention_years >= FDA_QMSR_RECORD_RETENTION_MIN_YEARS, (
            f"Records must be retained for at least {FDA_QMSR_RECORD_RETENTION_MIN_YEARS} years "
            f"from the date of release, or the expected useful life of the device "
            f"(whichever is longer) (21 CFR Part 820 §820.180). "
            f"Configured: {retention_years} years"
        )

    def test_implantable_device_records_retained_for_device_useful_life(
        self, controls_evidence: dict
    ):
        programs = controls_evidence.get("fda_qmsr_production_programs", [])
        implantable = [p for p in programs if p.get("is_implantable", False)]
        insufficient_retention = [
            p for p in implantable
            if p.get("record_retention_years") is not None
            and p.get("device_useful_life_years") is not None
            and p["record_retention_years"] < p["device_useful_life_years"]
        ]
        assert not insufficient_retention, (
            f"For implantable devices, records must be retained for the useful life of the "
            f"device, which may significantly exceed 2 years "
            f"(21 CFR Part 820 §820.180). "
            f"Insufficient retention: {[p['device_type_id'] for p in insufficient_retention]}"
        )

    def test_records_accessible_for_fda_inspection(self, controls_evidence: dict):
        qms = controls_evidence.get("fda_qmsr_qms", {})
        assert qms.get("records_accessible_for_fda_inspection", False), (
            "All records required by 21 CFR Part 820 must be accessible to FDA investigators "
            "during inspections (21 CFR Part 820 §820.180)"
        )

    def test_records_stored_to_minimize_deterioration(self, controls_evidence: dict):
        qms = controls_evidence.get("fda_qmsr_qms", {})
        assert qms.get("records_stored_to_minimize_deterioration", False), (
            "Records must be stored in a manner that minimizes deterioration and prevents loss "
            "(21 CFR Part 820 §820.180)"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|

*(No open assumptions — all FDA QMSR delta requirements are DETERMINISTIC record/process checks)*
