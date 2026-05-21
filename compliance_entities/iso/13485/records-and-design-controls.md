# ISO 13485:2016 — Records and Design Controls

**Framework:** ISO 13485:2016
**Clauses:** 4.2, 5.3–5.6, 6.2, 7.2.1, 7.2.2, 7.3.1–7.3.9, 7.4, 7.5.1, 7.5.5–7.5.9, 7.6, 8.2.1–8.2.4, 8.2.6, 8.3, 8.5.2–8.5.3
**Confidence:** DETERMINISTIC-dominant (documentation system + design control + CAPA records)
**Last parsed:** 2026-05-21
**Applies to:** Medical device manufacturers, component suppliers, distributors, and service providers involved in the design, development, production, storage, distribution, installation, or servicing of medical devices
**Trigger:** Regulatory requirement in many major markets — EU MDR/IVDR references ISO 13485; FDA QMSR (21 CFR 820) aligns to ISO 13485:2016; Health Canada, TGA (Australia), PMDA (Japan) recognize ISO 13485 certification; customer requirement in device supply chains
**Jurisdiction:** Global — ISO standard; certification recognized by regulatory bodies in EU, Canada, Australia, Japan, and many other markets; FDA accepts ISO 13485 certification for QMSR compliance determination
**Not applicable to:** Non-medical-device manufacturers; software products not meeting the medical device definition under MDR/IVDR or FDA; purely research/investigational devices not entering commercial distribution

---

## Scope pre-condition

```python
def requires_iso13485(entity_profile: dict) -> bool:
    """
    True if organization is a medical device manufacturer, contract manufacturer,
    sterilization provider, or supplier required by customer to hold ISO 13485 certification.
    """
    return entity_profile.get("iso13485_in_scope", False)
```

---

## Constants

```python
# Record retention (4.2.5) — the binding minimum
ISO13485_RECORD_RETENTION_MIN_YEARS = 2
ISO13485_RECORD_RETENTION_DEVICE_LIFETIME_BUFFER_YEARS = 2
# Effective minimum: max(2 years, device_expected_lifetime + 2 years)
# For implantable devices with 10-year expected lifetime: min retention = 12 years

# Calibration
ISO13485_CALIBRATION_TRACEABLE_STANDARD_REQUIRED = True

# CAPA — effectiveness review must be performed before closure
ISO13485_CAPA_EFFECTIVENESS_REVIEW_REQUIRED = True

# Complaint handling
ISO13485_COMPLAINT_INVESTIGATION_REQUIRED = True
ISO13485_REGULATORY_REPORTING_DETERMINATION_REQUIRED = True
```

---

## Clause 4.2 — Documentation Requirements

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | QMS documentation system for medical device manufacturer | DETERMINISTIC |
| Condition | ISO 13485 certification in scope | DETERMINISTIC |
| Obligation | Quality manual; documented procedures (required procedures enumerated); medical device file (technical file) per device type; records legible, identifiable, retrievable; retention ≥2 years or device lifetime + 2 years | DETERMINISTIC |
| Evidence | Quality manual; procedure list; device file index; retention schedule showing minimum retention periods | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
import pytest
from datetime import date

@pytest.fixture(autouse=True)
def iso13485_scope(entity_profile: dict):
    if not entity_profile.get("iso13485_in_scope", False):
        pytest.skip("ISO 13485 not in scope")

class TestClause4_2_Documentation:
    """Clause 4.2 — Documentation requirements: quality manual, procedures, device file, records."""

    def test_quality_manual_exists(self, controls_evidence: dict):
        docs = controls_evidence.get("iso13485_documentation", {})
        assert docs.get("quality_manual_exists", False), (
            "Quality manual must exist including scope, exclusions, procedures or references, "
            "and process interaction description (ISO 13485 §4.2.2)"
        )

    def test_medical_device_file_maintained_per_device(self, controls_evidence: dict):
        devices = controls_evidence.get("iso13485_device_types", [])
        missing_device_file = [
            d for d in devices
            if not d.get("device_file_maintained", False)
        ]
        assert not missing_device_file, (
            f"Medical device file (technical file) must be maintained for each device type "
            f"demonstrating conformity to requirements (ISO 13485 §4.2.3). "
            f"Missing: {[d['device_id'] for d in missing_device_file]}"
        )

    def test_record_retention_meets_minimum(self, controls_evidence: dict, entity_profile: dict):
        docs = controls_evidence.get("iso13485_documentation", {})
        retention_years = docs.get("record_retention_years", 0)
        device_lifetime_years = entity_profile.get("device_expected_lifetime_years", 0)
        required_retention = max(
            ISO13485_RECORD_RETENTION_MIN_YEARS,
            device_lifetime_years + ISO13485_RECORD_RETENTION_DEVICE_LIFETIME_BUFFER_YEARS
        )
        assert retention_years >= required_retention, (
            f"Record retention must be ≥{ISO13485_RECORD_RETENTION_MIN_YEARS} years or "
            f"≥ device lifetime + {ISO13485_RECORD_RETENTION_DEVICE_LIFETIME_BUFFER_YEARS} years, "
            f"whichever is greater. Required: {required_retention} years; "
            f"Configured: {retention_years} years (ISO 13485 §4.2.5)"
        )

    def test_document_control_procedure_exists(self, controls_evidence: dict):
        docs = controls_evidence.get("iso13485_documentation", {})
        assert docs.get("document_control_procedure_exists", False), (
            "Documented procedure for document control must exist (ISO 13485 §4.2.4)"
        )

    def test_records_control_procedure_exists(self, controls_evidence: dict):
        docs = controls_evidence.get("iso13485_documentation", {})
        assert docs.get("records_control_procedure_exists", False), (
            "Documented procedure for records control must exist (ISO 13485 §4.2.5)"
        )
```

---

## Clause 7.3 — Design and Development Controls

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Design and development activities for medical devices | DETERMINISTIC |
| Condition | Organization performs design and/or development activities | DETERMINISTIC |
| Obligation | Design plan documented; inputs/outputs/reviews/verification/validation/transfer/changes all documented with records; Design History File (DHF) maintained | DETERMINISTIC |
| Evidence | Design plan; design inputs record; design outputs record; design review records with attendees; verification/validation records; DHF index; design change records | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause7_3_DesignControl:
    """Clause 7.3 — Design and development: complete design control record trail."""

    def test_design_plan_documented(self, controls_evidence: dict, entity_profile: dict):
        if not entity_profile.get("performs_design_development", True):
            pytest.skip("Design and development excluded from scope with documented justification")
        design = controls_evidence.get("iso13485_design_control", {})
        assert design.get("design_plan_documented", False), (
            "Design and development plan must be documented with stages, review/verification/"
            "validation activities, and responsibilities (ISO 13485 §7.3.1)"
        )

    def test_design_inputs_documented(self, controls_evidence: dict, entity_profile: dict):
        if not entity_profile.get("performs_design_development", True):
            pytest.skip("Design and development excluded from scope")
        design = controls_evidence.get("iso13485_design_control", {})
        assert design.get("design_inputs_documented", False), (
            "Design inputs must be documented and include functional/performance requirements, "
            "applicable regulatory requirements, and risk management outputs (ISO 13485 §7.3.2)"
        )

    def test_design_outputs_documented(self, controls_evidence: dict, entity_profile: dict):
        if not entity_profile.get("performs_design_development", True):
            pytest.skip("Design and development excluded from scope")
        design = controls_evidence.get("iso13485_design_control", {})
        assert design.get("design_outputs_documented", False), (
            "Design outputs must be documented, meet inputs, and be approved before release "
            "(ISO 13485 §7.3.3)"
        )

    def test_design_review_records_exist(self, controls_evidence: dict, entity_profile: dict):
        if not entity_profile.get("performs_design_development", True):
            pytest.skip("Design and development excluded from scope")
        design = controls_evidence.get("iso13485_design_control", {})
        assert design.get("design_review_records_exist", False), (
            "Design review records must exist for each design review stage with participants "
            "identified (ISO 13485 §7.3.4)"
        )

    def test_design_verification_records_exist(self, controls_evidence: dict, entity_profile: dict):
        if not entity_profile.get("performs_design_development", True):
            pytest.skip("Design and development excluded from scope")
        design = controls_evidence.get("iso13485_design_control", {})
        assert design.get("verification_records_exist", False), (
            "Design verification records must demonstrate outputs meet inputs "
            "(ISO 13485 §7.3.5)"
        )

    def test_design_validation_records_exist(self, controls_evidence: dict, entity_profile: dict):
        if not entity_profile.get("performs_design_development", True):
            pytest.skip("Design and development excluded from scope")
        design = controls_evidence.get("iso13485_design_control", {})
        assert design.get("validation_records_exist", False), (
            "Design validation records must exist; validation must be completed before delivery "
            "(ISO 13485 §7.3.6)"
        )

    def test_design_transfer_verified(self, controls_evidence: dict, entity_profile: dict):
        if not entity_profile.get("performs_design_development", True):
            pytest.skip("Design and development excluded from scope")
        design = controls_evidence.get("iso13485_design_control", {})
        assert design.get("design_transfer_verified", False), (
            "Design transfer must be verified — design outputs must be confirmed suitable "
            "for manufacturing before becoming production specification (ISO 13485 §7.3.7)"
        )

    def test_design_change_records_exist(self, controls_evidence: dict, entity_profile: dict):
        if not entity_profile.get("performs_design_development", True):
            pytest.skip("Design and development excluded from scope")
        design = controls_evidence.get("iso13485_design_control", {})
        design_changes = controls_evidence.get("iso13485_design_changes", [])
        if not design_changes:
            return
        unrecorded_changes = [
            c for c in design_changes
            if not c.get("change_record_exists", False)
        ]
        assert not unrecorded_changes, (
            f"All design changes must be identified, reviewed, verified, validated, and "
            f"approved before implementation with records retained (ISO 13485 §7.3.8). "
            f"Unrecorded: {[c['change_id'] for c in unrecorded_changes]}"
        )

    def test_design_history_file_maintained(self, controls_evidence: dict, entity_profile: dict):
        if not entity_profile.get("performs_design_development", True):
            pytest.skip("Design and development excluded from scope")
        devices = controls_evidence.get("iso13485_device_types", [])
        no_dhf = [
            d for d in devices
            if not d.get("dhf_maintained", False)
        ]
        assert not no_dhf, (
            f"Design History File (DHF) must be maintained for each device type "
            f"demonstrating QMS compliance (ISO 13485 §7.3.9). "
            f"Missing DHF: {[d['device_id'] for d in no_dhf]}"
        )
```

---

## Clause 7.4 — Supplier Controls

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Externally provided materials, components, and services affecting device conformity | DETERMINISTIC |
| Condition | External purchasing activity exists | DETERMINISTIC |
| Obligation | Supplier evaluation criteria defined; suppliers evaluated and selected based on criteria; evaluation records retained; purchasing documents specify requirements; incoming inspection/verification records retained | DETERMINISTIC |
| Evidence | Approved supplier list with evaluation status; supplier evaluation records; purchase orders with requirements; incoming inspection records | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause7_4_SupplierControls:
    """Clause 7.4 — Supplier controls: evaluation, records, purchasing documents."""

    def test_supplier_evaluation_criteria_defined(self, controls_evidence: dict):
        suppliers = controls_evidence.get("iso13485_supplier_management", {})
        assert suppliers.get("evaluation_criteria_defined", False), (
            "Supplier evaluation and selection criteria must be defined (ISO 13485 §7.4.1)"
        )

    def test_supplier_evaluation_records_retained(self, controls_evidence: dict):
        suppliers = controls_evidence.get("iso13485_supplier_management", {})
        assert suppliers.get("evaluation_records_retained", False), (
            "Supplier evaluation records must be retained (ISO 13485 §7.4.1)"
        )

    def test_purchase_orders_specify_requirements(self, controls_evidence: dict):
        recent_pos = controls_evidence.get("iso13485_recent_purchase_orders", [])
        missing_requirements = [
            po for po in recent_pos
            if not po.get("requirements_specified", False)
        ]
        assert not missing_requirements, (
            f"Purchase orders must specify device/component requirements before release "
            f"to supplier (ISO 13485 §7.4.2). Missing: {[po['po_id'] for po in missing_requirements]}"
        )
```

---

## Clause 7.6 — Calibration

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Monitoring and measuring equipment used to verify device conformity | DETERMINISTIC |
| Condition | Monitoring or measuring equipment exists in scope | DETERMINISTIC |
| Obligation | Calibrated against traceable standards; calibration records retained; calibration status identified (label/tag); protected from invalidating adjustments; software validated | DETERMINISTIC |
| Evidence | Calibration records with standard reference, date, result, next due date; calibration status on each instrument | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause7_6_Calibration:
    """Clause 7.6 — Calibration: traceable calibration records for M&M equipment."""

    def test_calibration_records_exist(self, controls_evidence: dict):
        instruments = controls_evidence.get("iso13485_measurement_equipment", [])
        uncalibrated = [
            i for i in instruments
            if i.get("calibration_required", True)
            and not i.get("calibration_record_exists", False)
        ]
        assert not uncalibrated, (
            f"Calibration records must exist for all monitoring and measuring equipment. "
            f"Missing: {[i['instrument_id'] for i in uncalibrated]}"
        )

    def test_calibration_traceable_to_international_standards(self, controls_evidence: dict):
        instruments = controls_evidence.get("iso13485_measurement_equipment", [])
        not_traceable = [
            i for i in instruments
            if i.get("calibration_required", True)
            and not i.get("traceable_to_national_or_international_standard", False)
        ]
        assert not not_traceable, (
            f"Calibration must be traceable to national or international measurement standards. "
            f"Not traceable: {[i['instrument_id'] for i in not_traceable]}"
        )

    def test_calibration_status_identified_on_equipment(self, controls_evidence: dict):
        instruments = controls_evidence.get("iso13485_measurement_equipment", [])
        no_status_label = [
            i for i in instruments
            if i.get("calibration_required", True)
            and not i.get("calibration_status_labeled", False)
        ]
        assert not no_status_label, (
            f"Calibration status must be identified on measuring equipment or in records. "
            f"Missing status label: {[i['instrument_id'] for i in no_status_label]}"
        )
```

---

## Clause 8.2.2 — Complaint Handling

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Complaints about medical devices from customers, regulators, or post-market sources | DETERMINISTIC |
| Condition | Complaint received about a device | DETERMINISTIC |
| Obligation | Documented complaint handling procedure; all complaints recorded; investigation performed; regulatory reporting determination made; records retained | DETERMINISTIC |
| Evidence | Complaint log; complaint investigation records; regulatory reporting determination records per complaint | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause8_2_2_ComplaintHandling:
    """Clause 8.2.2 — Complaint handling: documented procedure, records, regulatory determination."""

    def test_complaint_handling_procedure_exists(self, controls_evidence: dict):
        complaints = controls_evidence.get("iso13485_complaint_handling", {})
        assert complaints.get("documented_procedure_exists", False), (
            "Documented complaint handling procedure must exist (ISO 13485 §8.2.2)"
        )

    def test_all_complaints_recorded(self, controls_evidence: dict):
        complaints = controls_evidence.get("iso13485_complaint_handling", {})
        assert complaints.get("complaint_log_maintained", False), (
            "All complaints must be recorded — complaint log must be maintained "
            "(ISO 13485 §8.2.2)"
        )

    def test_regulatory_reporting_determination_made_per_complaint(
        self, controls_evidence: dict
    ):
        complaint_records = controls_evidence.get("iso13485_complaint_records", [])
        no_determination = [
            c for c in complaint_records
            if not c.get("regulatory_reporting_determination_made", False)
        ]
        assert not no_determination, (
            f"Regulatory reporting determination must be made for each complaint. "
            f"Missing determination: {[c['complaint_id'] for c in no_determination]}"
        )

    def test_complaint_investigations_documented(self, controls_evidence: dict):
        complaint_records = controls_evidence.get("iso13485_complaint_records", [])
        no_investigation = [
            c for c in complaint_records
            if not c.get("investigation_performed", False)
            and not c.get("no_investigation_justified", False)
        ]
        assert not no_investigation, (
            f"Complaint investigations must be performed and documented (or justified if "
            f"no investigation needed). Missing: {[c['complaint_id'] for c in no_investigation]}"
        )
```

---

## Clause 8.3 — Control of Nonconforming Product

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Medical devices that do not conform to requirements | DETERMINISTIC |
| Condition | Nonconformance detected before or after delivery | DETERMINISTIC |
| Obligation | Documented procedure; identification, documentation, segregation, evaluation, and disposition; notification to customers and regulators where required; rework documented and assessed | DETERMINISTIC |
| Evidence | Nonconformance procedure; NC records with disposition; customer/regulatory notification records; rework records | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause8_3_NonconformingProduct:
    """Clause 8.3 — Nonconforming product: documented procedure, disposition, notifications."""

    def test_nc_control_procedure_exists(self, controls_evidence: dict):
        nc = controls_evidence.get("iso13485_nonconforming_product", {})
        assert nc.get("documented_procedure_exists", False), (
            "Documented procedure for control of nonconforming product must exist "
            "(ISO 13485 §8.3.1)"
        )

    def test_nc_disposition_documented(self, controls_evidence: dict):
        nc_records = controls_evidence.get("iso13485_nc_records", [])
        no_disposition = [
            r for r in nc_records
            if not r.get("disposition_documented", False)
        ]
        assert not no_disposition, (
            f"Disposition must be documented for all nonconforming products. "
            f"Missing: {[r['nc_id'] for r in no_disposition]}"
        )

    def test_post_delivery_nc_has_regulatory_reporting_determination(
        self, controls_evidence: dict
    ):
        nc_records = controls_evidence.get("iso13485_nc_records", [])
        post_delivery_ncs = [r for r in nc_records if r.get("detected_after_delivery", False)]
        no_determination = [
            r for r in post_delivery_ncs
            if not r.get("regulatory_reporting_determination_made", False)
        ]
        assert not no_determination, (
            f"Post-delivery nonconformities must have regulatory reporting determination "
            f"(ISO 13485 §8.3.3). Missing: {[r['nc_id'] for r in no_determination]}"
        )
```

---

## Clause 8.5.2 — Corrective Action (CAPA)

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | CAPA system for medical device QMS | DETERMINISTIC |
| Condition | Nonconformity or adverse trend identified | DETERMINISTIC |
| Obligation | Documented CAPA procedure; root cause analysis performed; corrective actions do not adversely affect ability to meet regulatory requirements; effectiveness reviewed; records retained | DETERMINISTIC |
| Evidence | CAPA procedure; CAPA log; root cause records; effectiveness review records; closure documentation | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause8_5_2_CorrectiveAction:
    """Clause 8.5.2 — Corrective action: documented procedure, root cause, effectiveness review."""

    def test_capa_procedure_exists(self, controls_evidence: dict):
        capa = controls_evidence.get("iso13485_capa", {})
        assert capa.get("documented_procedure_exists", False), (
            "Documented corrective action procedure must exist (ISO 13485 §8.5.2)"
        )

    def test_capa_records_retained(self, controls_evidence: dict):
        capa = controls_evidence.get("iso13485_capa", {})
        assert capa.get("records_retained", False), (
            "CAPA records must be retained (ISO 13485 §8.5.2)"
        )

    def test_open_capas_have_root_cause(self, controls_evidence: dict):
        capas = controls_evidence.get("iso13485_open_capas", [])
        no_rca = [
            c for c in capas
            if not c.get("root_cause_documented", False)
            and not c.get("root_cause_in_progress", False)
        ]
        assert not no_rca, (
            f"Root cause analysis must be performed for all CAPAs. "
            f"Missing: {[c['capa_id'] for c in no_rca]}"
        )

    def test_closed_capas_have_effectiveness_review(self, controls_evidence: dict):
        closed_capas = controls_evidence.get("iso13485_closed_capas", [])
        no_effectiveness = [
            c for c in closed_capas
            if not c.get("effectiveness_reviewed", False)
        ]
        assert not no_effectiveness, (
            f"Effectiveness of corrective actions must be reviewed before closure "
            f"(ISO 13485 §8.5.2). Missing: {[c['capa_id'] for c in no_effectiveness]}"
        )

    def test_preventive_action_procedure_exists(self, controls_evidence: dict):
        capa = controls_evidence.get("iso13485_capa", {})
        assert capa.get("preventive_action_procedure_exists", False), (
            "Documented preventive action procedure must exist (ISO 13485 §8.5.3)"
        )
```

---

## Open assumptions

*(No assumptions recorded for this file — all requirements are DETERMINISTIC record existence checks)*

---

## Cross-standard notes

**FDA 21 CFR Part 820 / QMSR:** The records required by ISO 13485 §4.2.5 (device file), §7.3.9 (DHF), §8.2.2 (complaint records), and §8.5.2 (CAPA records) are substantially equivalent to FDA QMSR requirements. A single record structure can satisfy both regulatory systems when designed to meet the more demanding of the two.

**EU MDR Annex II:** ISO 13485 §7.3.9 DHF maps to EU MDR Annex II Technical Documentation. The DHF must include all documentation required by Annex II §6.1 (device description, labeling, design/manufacturing information, conformity assessment decisions).

**ISO 14971:** ISO 13485 §7.1 and §7.3.2 both require risk management per ISO 14971. The risk management file is a prerequisite document for completing design inputs and must be cross-referenced in the DHF.
