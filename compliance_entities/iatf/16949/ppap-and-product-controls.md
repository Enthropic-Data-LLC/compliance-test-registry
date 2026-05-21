# IATF 16949:2016 — PPAP and Product Controls

**Framework:** IATF 16949:2016
**Clauses:** 8.3 (design), 8.5.1 (production controls), 8.6 (release), 8.7 (NC product), 9.1.1, 10.2.4–10.2.6
**Parent:** ISO 9001:2015 (see iso/9001 registry); all ISO 9001 requirements apply simultaneously
**Confidence:** DETERMINISTIC-dominant (PPAP 18 elements, control plan, SPC, error-proofing, customer notification)
**Last parsed:** 2026-05-21

---

## Scope pre-condition

```python
def requires_iatf16949(entity_profile: dict) -> bool:
    """
    True if organization is a Tier 1/2/N supplier to an IATF subscribing OEM,
    or has contractual obligation requiring IATF 16949 certification.
    """
    return entity_profile.get("iatf16949_in_scope", False)
```

---

## Constants

```python
# PPAP — 18 required elements (AIAG PPAP 4th ed. / IATF §8.3.4.2)
IATF_PPAP_REQUIRED_ELEMENTS = frozenset({
    "design_records",
    "authorized_engineering_change_documents",
    "customer_engineering_approval",
    "design_fmea",
    "process_flow_diagram",
    "process_fmea",
    "control_plan",
    "measurement_system_analysis",
    "dimensional_results",
    "material_performance_test_results",
    "initial_process_studies",
    "qualified_laboratory_documentation",
    "appearance_approval_report",        # only if appearance item
    "sample_production_parts",
    "master_sample",
    "checking_aids",
    "customer_specific_requirements",
    "part_submission_warrant",
})
IATF_PPAP_ELEMENTS_CONDITIONAL = frozenset({"appearance_approval_report"})

# SPC — process capability requirements
IATF_CPK_SPECIAL_CHARACTERISTICS_MINIMUM = 1.67  # per most OEM CSRs; verify against actual CSR
IATF_PPK_INITIAL_PROCESS_STUDY_MINIMUM = 1.67    # initial capability before Cpk

# Control plan phases
IATF_CONTROL_PLAN_PHASES = frozenset({"prototype", "pre_launch", "production"})

# Layout inspection frequency — §8.6.2
IATF_LAYOUT_INSPECTION_MAX_MONTHS = 12  # typically annual; verify against CSR

# Error-proofing test frequency — §10.2.4 (defined in control plan)
IATF_ERROR_PROOFING_TEST_REQUIRED = True
```

---

## PPAP Gate (§8.3.4.2 / §8.6.1) — DETERMINISTIC

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Production parts for automotive serial production | DETERMINISTIC |
| Condition | Before first shipment of production parts to customer | DETERMINISTIC |
| Obligation | PPAP submission (at applicable level) containing all required elements; customer approval (PSW signed) before production delivery | DETERMINISTIC |
| Evidence | PPAP package with all 18 elements (minus conditional); signed Part Submission Warrant (PSW) | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
import pytest
from datetime import date, timedelta

@pytest.fixture(autouse=True)
def iatf16949_scope(entity_profile: dict):
    if not entity_profile.get("iatf16949_in_scope", False):
        pytest.skip("IATF 16949 not in scope")

class TestPPAP:
    """PPAP — Production Part Approval Process: 18 elements; customer approval before delivery."""

    def test_ppap_submitted_before_production_delivery(self, controls_evidence: dict):
        programs = controls_evidence.get("iatf16949_production_programs", [])
        no_ppap = [
            p for p in programs
            if p.get("in_production", False)
            and not p.get("ppap_submitted", False)
        ]
        assert not no_ppap, (
            f"PPAP must be submitted and approved before production delivery "
            f"(IATF 16949 §8.6.1). Missing: {[p['program_id'] for p in no_ppap]}"
        )

    def test_ppap_contains_required_elements(self, controls_evidence: dict):
        programs = controls_evidence.get("iatf16949_production_programs", [])
        for program in programs:
            if not program.get("ppap_submitted", False):
                continue
            is_appearance_item = program.get("is_appearance_item", False)
            required = IATF_PPAP_REQUIRED_ELEMENTS.copy()
            if not is_appearance_item:
                required -= IATF_PPAP_ELEMENTS_CONDITIONAL
            present = set(program.get("ppap_elements_present", []))
            missing = required - present
            assert not missing, (
                f"PPAP for program '{program['program_id']}' is missing required elements: "
                f"{missing} (IATF 16949 §8.3.4.2)"
            )

    def test_part_submission_warrant_customer_approved(self, controls_evidence: dict):
        programs = controls_evidence.get("iatf16949_production_programs", [])
        no_psw_approval = [
            p for p in programs
            if p.get("ppap_submitted", False)
            and not p.get("psw_customer_approved", False)
        ]
        assert not no_psw_approval, (
            f"Part Submission Warrant (PSW) must be customer-approved before production "
            f"delivery (IATF 16949 §8.6.1). "
            f"Missing PSW approval: {[p['program_id'] for p in no_psw_approval]}"
        )
```

---

## Control Plans (§8.5.1.1) — DETERMINISTIC

```python
class TestControlPlans:
    """§8.5.1.1 — Control plans: required for all three phases; reference special characteristics."""

    def test_control_plans_exist_for_all_phases(self, controls_evidence: dict):
        programs = controls_evidence.get("iatf16949_production_programs", [])
        for program in programs:
            for phase in IATF_CONTROL_PLAN_PHASES:
                if not program.get(f"{phase}_phase_applicable", True):
                    continue
                has_cp = program.get(f"{phase}_control_plan_exists", False)
                assert has_cp, (
                    f"Control plan required for {phase} phase of program "
                    f"'{program['program_id']}' (IATF 16949 §8.5.1.1)"
                )

    def test_control_plans_reference_special_characteristics(
        self, controls_evidence: dict
    ):
        programs = controls_evidence.get("iatf16949_production_programs", [])
        missing_sc = [
            p for p in programs
            if p.get("has_special_characteristics", True)
            and not p.get("control_plan_references_special_chars", False)
        ]
        assert not missing_sc, (
            f"Control plans must reference all special characteristics "
            f"(IATF 16949 §8.5.1.1). Missing: {[p['program_id'] for p in missing_sc]}"
        )

    def test_work_instructions_at_production_stations(self, controls_evidence: dict):
        stations = controls_evidence.get("iatf16949_production_stations", [])
        no_wi = [s for s in stations if not s.get("work_instruction_accessible", False)]
        assert not no_wi, (
            f"Work instructions must be accessible at each production station "
            f"(IATF 16949 §8.5.1.2). Missing: {[s['station_id'] for s in no_wi]}"
        )
```

---

## SPC and Special Characteristics (§9.1.1.3) — DETERMINISTIC

```python
class TestSPCAndSpecialCharacteristics:
    """§9.1.1.3 — SPC applied to special characteristics; Cpk ≥ 1.67 (or per CSR)."""

    def test_spc_applied_to_special_characteristics(self, controls_evidence: dict):
        special_chars = controls_evidence.get("iatf16949_special_characteristics", [])
        no_spc = [sc for sc in special_chars if not sc.get("spc_applied", False)]
        assert not no_spc, (
            f"SPC must be applied to all special characteristics (IATF 16949 §9.1.1.3). "
            f"Missing SPC: {[sc['characteristic_id'] for sc in no_spc]}"
        )

    def test_cpk_meets_minimum_for_special_characteristics(
        self, controls_evidence: dict, entity_profile: dict
    ):
        cpk_minimum = entity_profile.get(
            "cpk_minimum_special_chars", IATF_CPK_SPECIAL_CHARACTERISTICS_MINIMUM
        )
        special_chars = controls_evidence.get("iatf16949_special_characteristics", [])
        below_cpk = [
            sc for sc in special_chars
            if sc.get("spc_applied", False)
            and sc.get("current_cpk") is not None
            and sc["current_cpk"] < cpk_minimum
        ]
        assert not below_cpk, (
            f"Special characteristics must achieve Cpk ≥ {cpk_minimum} "
            f"(IATF 16949 §9.1.1.3 / OEM CSR). "
            f"Below minimum: "
            f"{[(sc['characteristic_id'], sc['current_cpk']) for sc in below_cpk]}"
        )

    def test_process_capability_studies_performed(self, controls_evidence: dict):
        programs = controls_evidence.get("iatf16949_production_programs", [])
        no_capability = [
            p for p in programs
            if p.get("has_special_characteristics", True)
            and not p.get("initial_process_study_performed", False)
        ]
        assert not no_capability, (
            f"Initial process capability studies (Ppk/Cpk) required for special "
            f"characteristics (IATF 16949 §9.1.1.1). "
            f"Missing: {[p['program_id'] for p in no_capability]}"
        )
```

---

## MSA (§7.1.5.1) and Calibration — DETERMINISTIC

```python
class TestMSAAndCalibration:
    """§7.1.5.1 — MSA required for all control plan measurement systems."""

    def test_msa_performed_for_control_plan_measurement_systems(
        self, controls_evidence: dict
    ):
        measurement_systems = controls_evidence.get(
            "iatf16949_measurement_systems", []
        )
        control_plan_systems = [
            m for m in measurement_systems
            if m.get("in_control_plan", True)
        ]
        no_msa = [m for m in control_plan_systems if not m.get("msa_performed", False)]
        assert not no_msa, (
            f"MSA (Gage R&R or equivalent) must be performed for all measurement "
            f"systems used for control plan characteristics (IATF 16949 §7.1.5.1). "
            f"Missing MSA: {[m['measurement_system_id'] for m in no_msa]}"
        )

    @pytest.mark.assumption(
        id="ASSUME-IATF-MSA-001",
        description=(
            "MSA acceptance criteria defined in quality plan or CSR; typical criteria: "
            "Gage R&R %Contribution ≤ 10% (acceptable), 10–30% (marginal — management "
            "decision required), >30% (not acceptable); number of distinct categories (ndc) "
            "≥ 5 for variable gauges; attribute MSA: kappa ≥ 0.75; criteria aligned to "
            "AIAG MSA 4th edition; CSR may specify stricter criteria"
        ),
        approved_by="quality_engineer",
        review_date="2027-05-21",
    )
    def test_msa_results_meet_acceptance_criteria(self, controls_evidence: dict):
        measurement_systems = controls_evidence.get(
            "iatf16949_measurement_systems", []
        )
        failed_msa = [
            m for m in measurement_systems
            if m.get("msa_performed", False)
            and not m.get("msa_acceptable", False)
            and not m.get("msa_marginal_management_approved", False)
        ]
        assert not failed_msa, (
            f"MSA results must meet acceptance criteria; unacceptable gages must be "
            f"addressed before use in production measurement (IATF 16949 §7.1.5.1). "
            f"Failing: {[m['measurement_system_id'] for m in failed_msa]}"
        )
```

---

## Layout Inspection and First-Off Verification (§8.6.2 / §8.5.1.3)

```python
class TestLayoutAndFirstOff:
    """§8.6.2 — Layout inspection at defined frequency; §8.5.1.3 — first-off/last-off."""

    def test_layout_inspection_performed_at_required_interval(
        self, controls_evidence: dict, reference_date: date
    ):
        programs = controls_evidence.get("iatf16949_production_programs", [])
        overdue = [
            p for p in programs
            if p.get("in_production", False)
            and p.get("last_layout_inspection_date") is not None
            and p["last_layout_inspection_date"] < reference_date - timedelta(
                days=IATF_LAYOUT_INSPECTION_MAX_MONTHS * 30
            )
        ]
        assert not overdue, (
            f"Layout inspection must be performed at defined frequency "
            f"(≤{IATF_LAYOUT_INSPECTION_MAX_MONTHS} months per §8.6.2). "
            f"Overdue: {[p['program_id'] for p in overdue]}"
        )

    def test_first_off_verification_records_retained(self, controls_evidence: dict):
        programs = controls_evidence.get("iatf16949_production_programs", [])
        no_first_off = [
            p for p in programs
            if p.get("in_production", False)
            and not p.get("first_off_verification_records_retained", False)
        ]
        assert not no_first_off, (
            f"First-off (and last-off where required) verification records must be "
            f"retained (IATF 16949 §8.5.1.3). Missing: {[p['program_id'] for p in no_first_off]}"
        )
```

---

## Error-Proofing (§10.2.4) and Tooling Inventory (§8.5.1.6)

```python
class TestErrorProofingAndTooling:
    """§10.2.4 — Error-proofing devices tested at defined frequency; §8.5.1.6 — tooling inventory."""

    def test_error_proofing_devices_tested_at_defined_frequency(
        self, controls_evidence: dict
    ):
        error_proofing_devices = controls_evidence.get(
            "iatf16949_error_proofing_devices", []
        )
        not_tested = [
            d for d in error_proofing_devices
            if not d.get("tested_at_defined_frequency", False)
        ]
        assert not not_tested, (
            f"Error-proofing (poka-yoke) devices must be tested at the frequency defined "
            f"in the control plan (IATF 16949 §10.2.4). "
            f"Not tested: {[d['device_id'] for d in not_tested]}"
        )

    def test_error_proofing_test_records_retained(self, controls_evidence: dict):
        ep = controls_evidence.get("iatf16949_error_proofing", {})
        assert ep.get("test_records_retained", False), (
            "Error-proofing test records must be retained (IATF 16949 §10.2.4)"
        )

    def test_tooling_inventory_maintained(self, controls_evidence: dict):
        tooling = controls_evidence.get("iatf16949_tooling", {})
        assert tooling.get("inventory_maintained", False), (
            "Production tooling inventory must be maintained with maintenance and "
            "replacement records (IATF 16949 §8.5.1.6)"
        )
```

---

## Customer Notification for Nonconforming Product (§8.7.1.1 / §8.7.1.2)

```python
class TestCustomerNotificationForNC:
    """§8.7.1.1/1.2 — Customer notification and waiver for nonconforming product."""

    def test_customer_notified_of_nonconforming_shipped_product(
        self, controls_evidence: dict
    ):
        shipped_nc = controls_evidence.get("iatf16949_shipped_nonconforming", [])
        not_notified = [
            s for s in shipped_nc
            if not s.get("customer_notified", False)
        ]
        assert not not_notified, (
            f"Customer must be notified when nonconforming product has been shipped "
            f"(IATF 16949 §8.7.1.1). Not notified: {[s['ncr_id'] for s in not_notified]}"
        )

    def test_customer_waiver_obtained_before_shipping_known_nc(
        self, controls_evidence: dict
    ):
        planned_nc_shipments = controls_evidence.get(
            "iatf16949_planned_nc_shipments", []
        )
        no_waiver = [
            s for s in planned_nc_shipments
            if not s.get("customer_waiver_obtained", False)
        ]
        assert not no_waiver, (
            f"Customer deviation/waiver must be obtained before shipping known nonconforming "
            f"product (IATF 16949 §8.7.1.2). Missing: {[s['shipment_id'] for s in no_waiver]}"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-IATF-MSA-001 | 7.1.5.1 | MSA acceptance: %R&R ≤10% acceptable, ≤30% marginal; ndc ≥5; kappa ≥0.75 attribute | 2027-05-21 |
