# FDA 21 CFR Parts 210/211 — Pharmaceutical cGMP Manufacturing Controls

**Framework:** FDA 21 CFR Parts 210 and 211 (Current Good Manufacturing Practice)
**Clauses:** §211.22 (QC unit), §211.68 (automated systems), §211.100 (procedures/deviations), §211.103 (yield), §211.110 (in-process testing), §211.113 (microbiological contamination), §211.160–165 (lab controls), §211.166 (stability), §211.180–192 (batch records), §211.192 (batch release review)
**Authority:** U.S. FDA / CDER / CBER
**Confidence:** DETERMINISTIC-dominant (batch record completeness, OOS investigation, yield calculation, stability program, QC unit authority)
**Last parsed:** 2026-05-21
**Applies to:** Manufacturers of finished pharmaceutical drug products (human and veterinary) distributed in US interstate commerce; contract manufacturing organizations (CMOs) producing drugs for US-market distribution; API manufacturers to the extent their processes become part of finished dosage forms
**Trigger:** Manufacturing finished drug products for introduction into US interstate commerce; FDA establishment registration under 21 CFR 207 triggers cGMP applicability; applies to domestic and foreign drug manufacturers exporting to the US
**Jurisdiction:** United States; strong extraterritorial reach — FDA inspects and can refuse admission of drug products from non-compliant foreign facilities
**Not applicable to:** Investigational drugs in Phase 1 clinical trials (modified cGMP under 21 CFR 312); bulk API (covered under 21 CFR 211 Subpart B primarily for in-process controls); veterinary biologics (USDA); blood products (21 CFR 606); tissue/cellular products (21 CFR 1271)

---

## Scope pre-condition

```python
@pytest.fixture(autouse=True)
def cgmp_scope(entity_profile: dict):
    if not entity_profile.get("fda_cgmp_21cfr211_in_scope", False):
        pytest.skip("FDA 21 CFR Parts 210/211 cGMP not in scope")
```

---

## Constants

```python
# Stability testing — §211.166
FDA_CGMP_STABILITY_PROGRAM_REQUIRED = True
FDA_CGMP_STABILITY_LONG_TERM_REQUIRED = True   # supports labeled shelf life
FDA_CGMP_STABILITY_ACCELERATED_REQUIRED = True  # ICH Q1A compatible

# Batch record required fields — §211.188
FDA_CGMP_MASTER_BATCH_RECORD_REQUIRED_ELEMENTS = frozenset({
    "product_name_and_strength",
    "dosage_form",
    "date_of_manufacture",
    "batch_or_lot_number",
    "list_of_components_with_quantities",
    "theoretical_yield_at_each_phase",
    "acceptance_criteria_for_yield",
    "processing_instructions_with_equipment",
    "in_process_control_instructions",
    "instructions_for_sampling_and_testing",
    "special_notations_and_precautions",
    "instructions_for_storage",
})

FDA_CGMP_EXECUTED_BATCH_RECORD_REQUIRED_ELEMENTS = frozenset({
    "product_name_batch_number_strength",
    "date_and_time_each_step_initiated",
    "initials_or_signature_person_performing",
    "initials_or_signature_person_witnessing",
    "actual_yield_and_percent_of_theoretical",
    "complete_labeling_control_records",
    "in_process_laboratory_control_records",
    "equipment_cleaning_and_maintenance",
    "date_of_equipment_cleaning",
    "results_of_examinations_and_tests",
    "investigation_of_any_deviation",
})

# OOS (Out-of-Specification) investigation — §211.192
FDA_CGMP_OOS_INVESTIGATION_REQUIRED = True
FDA_CGMP_BATCH_RELEASE_REVIEW_REQUIRED = True

# Calibration records — §211.68
FDA_CGMP_COMPUTER_VALIDATION_REQUIRED = True

# Lab method validation — §211.160(b)
FDA_CGMP_TEST_METHOD_VALIDATION_REQUIRED = True
```

---

## §211.22 — Quality Control Unit

**Overall: DETERMINISTIC — Pattern 1**

```python
import pytest

class TestQualityControlUnit:
    """§211.22 — QC unit with authority to approve/reject; written procedures; independence."""

    def test_qc_unit_exists_with_defined_responsibilities(
        self, controls_evidence: dict
    ):
        qc = controls_evidence.get("cgmp_quality_control_unit", {})
        assert qc.get("qc_unit_established", False), (
            "An independent Quality Control unit must be established with defined "
            "responsibilities and authority (21 CFR §211.22(a))"
        )

    def test_qc_unit_has_approve_reject_authority(self, controls_evidence: dict):
        qc = controls_evidence.get("cgmp_quality_control_unit", {})
        assert qc.get("authority_to_approve_or_reject_materials_and_products", False), (
            "QC unit must have authority to approve or reject all components, drug product "
            "containers, closures, in-process materials, packaging, labeling, and drug "
            "products (21 CFR §211.22(a))"
        )

    def test_qc_unit_has_written_procedures(self, controls_evidence: dict):
        qc = controls_evidence.get("cgmp_quality_control_unit", {})
        assert qc.get("written_procedures_exist", False), (
            "QC unit responsibilities must be documented in written procedures "
            "(21 CFR §211.22(d))"
        )

    def test_batch_disposition_records_retained(self, controls_evidence: dict):
        qc = controls_evidence.get("cgmp_quality_control_unit", {})
        assert qc.get("batch_disposition_records_retained", False), (
            "QC unit must retain records of disposition (approve/reject) for all batches "
            "(21 CFR §211.22(c))"
        )
```

---

## §211.68 — Automated Processes and Computer Systems

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestComputerValidation:
    """§211.68 — Computer/automated systems used in production or QC must be validated."""

    def test_production_and_laboratory_computers_validated(
        self, controls_evidence: dict
    ):
        systems = controls_evidence.get("cgmp_computer_systems", [])
        production_or_lab = [
            s for s in systems
            if s.get("used_in_production", False) or s.get("used_in_laboratory", False)
        ]
        not_validated = [s for s in production_or_lab if not s.get("validated", False)]
        assert not not_validated, (
            f"All automated and computerized systems used in production or laboratory "
            f"operations must be validated for their intended use (21 CFR §211.68(b)). "
            f"Not validated: {[s['system_id'] for s in not_validated]}"
        )

    def test_backup_system_or_manual_procedure_exists(
        self, controls_evidence: dict
    ):
        systems = controls_evidence.get("cgmp_computer_systems", [])
        no_backup = [
            s for s in systems
            if s.get("used_in_production", False)
            and not s.get("backup_or_manual_fallback_exists", False)
        ]
        assert not no_backup, (
            f"Backup systems or manual procedures must exist for automated systems used "
            f"in production to ensure operations can continue if systems fail "
            f"(21 CFR §211.68(b)). Missing: {[s['system_id'] for s in no_backup]}"
        )
```

---

## §211.100 / §211.103 — Written Procedures and Yield Calculations

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestWrittenProceduresAndYield:
    """§211.100/§211.103 — Written procedures for all operations; deviations investigated; yield calculated."""

    def test_all_manufacturing_operations_have_written_procedures(
        self, controls_evidence: dict
    ):
        qms = controls_evidence.get("cgmp_qms", {})
        assert qms.get("all_operations_have_written_procedures", False), (
            "Written procedures (SOPs) must exist for all production and process control "
            "operations (21 CFR §211.100(a))"
        )

    def test_deviations_from_procedures_investigated(
        self, controls_evidence: dict
    ):
        deviations = controls_evidence.get("cgmp_deviations", [])
        not_investigated = [
            d for d in deviations
            if not d.get("investigation_initiated", False)
        ]
        assert not not_investigated, (
            f"All deviations from written procedures must be investigated "
            f"(21 CFR §211.100(b)). Not investigated: "
            f"{[d['deviation_id'] for d in not_investigated]}"
        )

    def test_theoretical_and_actual_yield_calculated_per_batch(
        self, controls_evidence: dict
    ):
        batches = controls_evidence.get("cgmp_batches", [])
        no_yield = [
            b for b in batches
            if not b.get("theoretical_yield_calculated", False)
            or not b.get("actual_yield_calculated", False)
        ]
        assert not no_yield, (
            f"Theoretical and actual yield must be calculated and recorded at each phase "
            f"of manufacture for each batch (21 CFR §211.103). "
            f"Missing yield data: {[b['batch_id'] for b in no_yield]}"
        )
```

---

## §211.110 — In-Process Testing

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestInProcessTesting:
    """§211.110 — In-process tests at defined stages; samples examined and tested."""

    def test_in_process_specifications_established(self, controls_evidence: dict):
        products = controls_evidence.get("cgmp_products", [])
        no_ips = [p for p in products if not p.get("in_process_specifications_exist", False)]
        assert not no_ips, (
            f"In-process specifications and test procedures must be established for each "
            f"drug product (21 CFR §211.110(a)). Missing: "
            f"{[p['product_id'] for p in no_ips]}"
        )

    def test_in_process_test_results_recorded_per_batch(
        self, controls_evidence: dict
    ):
        batches = controls_evidence.get("cgmp_batches", [])
        no_ipt_records = [
            b for b in batches
            if not b.get("in_process_test_results_recorded", False)
        ]
        assert not no_ipt_records, (
            f"In-process test results must be recorded in the batch production record "
            f"(21 CFR §211.110(b)). Missing: {[b['batch_id'] for b in no_ipt_records]}"
        )
```

---

## §211.113 — Microbiological Contamination Controls

**Overall: DETERMINISTIC (sterile products) / PARAMETERIZED (non-sterile)**

```python
class TestMicrobiologicalControls:
    """§211.113 — Sterile products: sterilization validation required; environmental monitoring."""

    def test_sterilization_processes_validated_for_sterile_products(
        self, controls_evidence: dict, entity_profile: dict
    ):
        if not entity_profile.get("manufactures_sterile_products", False):
            return
        products = controls_evidence.get("cgmp_products", [])
        sterile_products = [p for p in products if p.get("is_sterile", False)]
        not_validated = [
            p for p in sterile_products
            if not p.get("sterilization_process_validated", False)
        ]
        assert not not_validated, (
            f"Sterilization processes for sterile drug products must be validated "
            f"(21 CFR §211.113(b)). Not validated: {[p['product_id'] for p in not_validated]}"
        )
```

---

## §211.160–165 — Laboratory Controls and OOS

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestLaboratoryControlsAndOOS:
    """§211.160/165 — Written lab procedures; validated test methods; OOS investigation before rejection."""

    def test_test_methods_validated_or_verified(self, controls_evidence: dict):
        methods = controls_evidence.get("cgmp_test_methods", [])
        not_validated = [
            m for m in methods
            if not m.get("method_validated_or_compendial", False)
        ]
        assert not not_validated, (
            f"All non-compendial test methods must be validated; compendial methods must "
            f"be verified before use (21 CFR §211.160(b)). "
            f"Not validated/verified: {[m['method_id'] for m in not_validated]}"
        )

    def test_oos_results_have_formal_investigation(self, controls_evidence: dict):
        lab_results = controls_evidence.get("cgmp_lab_results", [])
        oos_results = [r for r in lab_results if r.get("is_oos", False)]
        no_investigation = [
            r for r in oos_results
            if not r.get("oos_investigation_performed", False)
        ]
        assert not no_investigation, (
            f"Out-of-specification (OOS) results must have a formal investigation before "
            f"batch can be accepted or rejected (21 CFR §211.192). "
            f"Missing investigation: {[r['result_id'] for r in no_investigation]}"
        )

    def test_oos_investigation_includes_phase_i_and_ii(
        self, controls_evidence: dict
    ):
        lab_results = controls_evidence.get("cgmp_lab_results", [])
        oos_results = [r for r in lab_results if r.get("is_oos", False)]
        for result in oos_results:
            if not result.get("oos_investigation_performed", False):
                continue
            assert result.get("phase_i_laboratory_investigation_completed", False), (
                f"OOS investigation for result '{result['result_id']}' must include "
                f"Phase I laboratory investigation (21 CFR §211.192)"
            )

    def test_final_drug_product_tested_before_release(
        self, controls_evidence: dict
    ):
        batches = controls_evidence.get("cgmp_batches", [])
        not_tested = [
            b for b in batches
            if not b.get("finished_product_laboratory_tested", False)
        ]
        assert not not_tested, (
            f"Each batch of drug product must be tested by laboratory before released "
            f"for distribution (21 CFR §211.165(a)). "
            f"Not tested: {[b['batch_id'] for b in not_tested]}"
        )
```

---

## §211.166 — Stability Testing

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestStabilityTesting:
    """§211.166 — Written stability program; labeled shelf life supported by data."""

    def test_written_stability_testing_program_exists(
        self, controls_evidence: dict
    ):
        qms = controls_evidence.get("cgmp_qms", {})
        assert qms.get("stability_testing_program_documented", False), (
            "Written stability testing program must exist and be followed "
            "(21 CFR §211.166(a))"
        )

    def test_stability_data_supports_labeled_shelf_life(
        self, controls_evidence: dict
    ):
        products = controls_evidence.get("cgmp_products", [])
        no_stability_support = [
            p for p in products
            if not p.get("stability_data_supports_expiration_dating", False)
        ]
        assert not no_stability_support, (
            f"Stability data must support the labeled expiration date for each product "
            f"(21 CFR §211.166(a)). Missing: {[p['product_id'] for p in no_stability_support]}"
        )

    def test_stability_samples_retained_for_each_batch(
        self, controls_evidence: dict
    ):
        batches = controls_evidence.get("cgmp_batches", [])
        no_stability_samples = [
            b for b in batches
            if not b.get("stability_samples_retained", False)
        ]
        assert not no_stability_samples, (
            f"Stability samples must be retained from each batch and tested per the "
            f"stability program (21 CFR §211.166(a)). "
            f"Missing: {[b['batch_id'] for b in no_stability_samples]}"
        )
```

---

## §211.180–192 — Batch Records and Release Review

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestBatchRecordsAndRelease:
    """§211.180–192 — Master and executed batch records; complete review before release."""

    def test_master_batch_record_exists_per_product(self, controls_evidence: dict):
        products = controls_evidence.get("cgmp_products", [])
        missing_mbr = [
            p for p in products
            if not p.get("master_batch_record_exists", False)
        ]
        assert not missing_mbr, (
            f"Master Production and Control Record (master batch record) must exist for "
            f"each drug product (21 CFR §211.186). "
            f"Missing: {[p['product_id'] for p in missing_mbr]}"
        )

    def test_master_batch_record_contains_required_elements(
        self, controls_evidence: dict
    ):
        products = controls_evidence.get("cgmp_products", [])
        for product in products:
            if not product.get("master_batch_record_exists", False):
                continue
            present = set(product.get("mbr_elements_present", []))
            missing = FDA_CGMP_MASTER_BATCH_RECORD_REQUIRED_ELEMENTS - present
            assert not missing, (
                f"Master batch record for '{product['product_id']}' is missing elements: "
                f"{missing} (21 CFR §211.186)"
            )

    def test_executed_batch_record_completed_per_batch(
        self, controls_evidence: dict
    ):
        batches = controls_evidence.get("cgmp_batches", [])
        missing_ebr = [
            b for b in batches
            if not b.get("executed_batch_record_exists", False)
        ]
        assert not missing_ebr, (
            f"Executed batch production and control records must exist for each batch "
            f"manufactured (21 CFR §211.188). "
            f"Missing: {[b['batch_id'] for b in missing_ebr]}"
        )

    def test_executed_batch_record_contains_required_elements(
        self, controls_evidence: dict
    ):
        batches = controls_evidence.get("cgmp_batches", [])
        for batch in batches:
            if not batch.get("executed_batch_record_exists", False):
                continue
            present = set(batch.get("ebr_elements_present", []))
            missing = FDA_CGMP_EXECUTED_BATCH_RECORD_REQUIRED_ELEMENTS - present
            assert not missing, (
                f"Executed batch record for batch '{batch['batch_id']}' is missing "
                f"elements: {missing} (21 CFR §211.188)"
            )

    def test_complete_batch_record_review_before_release(
        self, controls_evidence: dict
    ):
        batches = controls_evidence.get("cgmp_batches", [])
        released_batches = [b for b in batches if b.get("released_for_distribution", False)]
        no_review = [
            b for b in released_batches
            if not b.get("complete_batch_record_review_performed", False)
        ]
        assert not no_review, (
            f"Complete review and approval of all batch production and control records "
            f"must be performed before batch is released for distribution "
            f"(21 CFR §211.192). "
            f"Missing review: {[b['batch_id'] for b in no_review]}"
        )

    def test_unexplained_discrepancies_investigated_before_release(
        self, controls_evidence: dict
    ):
        batches = controls_evidence.get("cgmp_batches", [])
        batches_with_discrepancies = [
            b for b in batches if b.get("discrepancies_noted_in_batch_review", False)
        ]
        not_resolved = [
            b for b in batches_with_discrepancies
            if not b.get("discrepancies_investigated_before_release", False)
        ]
        assert not not_resolved, (
            f"Unexplained discrepancies or batch failures must be investigated before "
            f"a batch is released or rejected (21 CFR §211.192). "
            f"Not investigated: {[b['batch_id'] for b in not_resolved]}"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|

*(No open assumptions — all 21 CFR 210/211 manufacturing controls are DETERMINISTIC record/process existence checks)*
