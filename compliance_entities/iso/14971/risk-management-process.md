# ISO 14971:2019 — Risk Management for Medical Devices

**Framework:** ISO 14971:2019
**Clauses:** 4–10 (all normative clauses)
**Confidence:** DETERMINISTIC gates (plan, report, post-production plan) + PARAMETERIZED (file completeness) + CONTESTED (acceptability, benefit-risk)
**Last parsed:** 2026-05-21
**Applies to:** Medical device manufacturers responsible for risk management throughout the device lifecycle — design, development, production, post-market surveillance
**Trigger:** Required by EU MDR Annex I General Safety and Performance Requirements (GSPRs); FDA guidance on device risk management references ISO 14971; ISO 13485 Clause 7.1 requires a risk management process; harmonized standard in EU, Canada, Australia, Japan
**Jurisdiction:** Global — harmonized with EU MDR Essential Requirements, referenced by FDA, Health Canada, TGA, PMDA, and most major medical device regulatory frameworks worldwide
**Not applicable to:** Non-medical-device products (ISO 31000 is the general enterprise risk management standard); IVD devices (IEC 62366 usability + ISO 14971 risk management both apply); food/drug products not classified as devices

---

## Scope pre-condition

```python
def requires_iso14971(entity_profile: dict) -> bool:
    """
    True if organization develops, manufactures, or markets a medical device.
    Required by: ISO 13485 §7.1; EU MDR Annex I §3; FDA QMSR §820.30(g) (recognized standard).
    """
    return entity_profile.get("iso14971_in_scope", False)
```

---

## Constants

```python
# Risk management plan — §4.4 required elements
ISO14971_PLAN_REQUIRED_ELEMENTS = frozenset({
    "scope_device_and_lifecycle",
    "responsibilities_and_authorities",
    "risk_acceptability_criteria",
    "verification_activities",
    "risk_management_report_review_criteria",
})

# Risk management file — required document types
ISO14971_RISK_FILE_REQUIRED_DOCUMENTS = frozenset({
    "risk_management_plan",
    "hazard_identification_records",
    "risk_estimation_records",
    "risk_evaluation_records",
    "risk_control_records",
    "risk_control_verification_records",
    "residual_risk_evaluation",
    "risk_management_report",
    "post_production_monitoring_plan",
})
```

---

## Clause 4.4 — Risk Management Plan (DETERMINISTIC gate)

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Written risk management plan | DETERMINISTIC |
| Condition | Before beginning risk management activities | DETERMINISTIC |
| Obligation | Plan must include all 5 required elements; reviewed and updated as device design evolves | DETERMINISTIC |
| Evidence | Risk management plan document; version history | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
import pytest
from datetime import date

@pytest.fixture(autouse=True)
def iso14971_scope(entity_profile: dict):
    if not entity_profile.get("iso14971_in_scope", False):
        pytest.skip("ISO 14971 not in scope")

class TestClause4_RiskManagementPlan:
    """Clause 4.4 — Risk management plan: required elements checklist."""

    def test_risk_management_plan_exists(self, controls_evidence: dict):
        devices = controls_evidence.get("iso14971_devices", [])
        no_plan = [d for d in devices if not d.get("risk_management_plan_exists", False)]
        assert not no_plan, (
            f"Risk management plan must exist for each medical device "
            f"(ISO 14971 §4.4). Missing: {[d['device_id'] for d in no_plan]}"
        )

    def test_risk_management_plan_has_required_elements(
        self, controls_evidence: dict
    ):
        devices = controls_evidence.get("iso14971_devices", [])
        for device in devices:
            plan_elements = set(device.get("risk_management_plan_elements", []))
            missing = ISO14971_PLAN_REQUIRED_ELEMENTS - plan_elements
            assert not missing, (
                f"Risk management plan for '{device['device_id']}' is missing required "
                f"elements: {missing} (ISO 14971 §4.4)"
            )

    def test_risk_acceptability_criteria_defined(self, controls_evidence: dict):
        devices = controls_evidence.get("iso14971_devices", [])
        no_criteria = [
            d for d in devices
            if not d.get("risk_acceptability_criteria_defined", False)
        ]
        assert not no_criteria, (
            f"Risk acceptability criteria must be defined in the risk management plan "
            f"before risk evaluation (ISO 14971 §4.4). "
            f"Missing: {[d['device_id'] for d in no_criteria]}"
        )
```

---

## Clauses 5–6 — Hazard Identification and Risk Estimation/Evaluation

### 5.2/5.3 — Hazard Identification and Risk Estimation

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestClause5_HazardIdentification:
    """Clauses 5.2–5.3 — Hazard identification and risk estimation."""

    @pytest.mark.assumption(
        id="ASSUME-14971-HAZID-001",
        description=(
            "Hazard identification systematically considers: intended use and reasonably "
            "foreseeable misuse; device characteristics (energy, materials, software, "
            "biological, environment); clinical context; reasonably foreseeable sequences "
            "of events; method documented (FMEA per ISO/TR 24971, FTA, HAZOP, or equivalent); "
            "hazard identification reviewed and updated when design changes occur, incidents "
            "are identified, or new information becomes available"
        ),
        approved_by="risk_management_team",
        review_date="2027-05-21",
    )
    def test_hazard_identification_documented(self, controls_evidence: dict):
        devices = controls_evidence.get("iso14971_devices", [])
        no_hazid = [
            d for d in devices
            if not d.get("hazard_identification_records_exist", False)
        ]
        assert not no_hazid, (
            f"Hazard identification records must exist for each device "
            f"(ISO 14971 §5.2). Missing: {[d['device_id'] for d in no_hazid]}"
        )

    @pytest.mark.assumption(
        id="ASSUME-14971-HAZID-002",
        description=(
            "Risk estimation performed for each identified hazardous situation: "
            "probability of occurrence of harm estimated using clinical literature, "
            "incident data, similar device data, or expert judgment; severity of harm "
            "estimated on defined scale; estimation documented with rationale; where "
            "probability cannot be estimated, worst-case assumption applied per ISO 14971 §5.3 "
            "and documented"
        ),
        approved_by="risk_management_team",
        review_date="2027-05-21",
    )
    def test_risk_estimation_records_exist(self, controls_evidence: dict):
        devices = controls_evidence.get("iso14971_devices", [])
        no_estimation = [
            d for d in devices
            if not d.get("risk_estimation_records_exist", False)
        ]
        assert not no_estimation, (
            f"Risk estimation records must exist for each device "
            f"(ISO 14971 §5.3). Missing: {[d['device_id'] for d in no_estimation]}"
        )
```

---

### 6 — Risk Evaluation

**Overall: CONTESTED — Pattern 3**

```python
class TestClause6_RiskEvaluation:
    """Clause 6 — Risk evaluation: acceptability determination against defined criteria."""

    @pytest.mark.assumption(
        id="ASSUME-14971-EVAL-001",
        description=(
            "Each risk is evaluated against the risk acceptability criteria defined in the "
            "risk management plan; evaluation outcome: acceptable (no further action) or "
            "not acceptable (requires risk control); if acceptability criteria cannot be met "
            "after applying all practicable risk controls, benefit-risk analysis performed "
            "per §9; evaluation records include the risk estimate, the criteria applied, "
            "and the evaluation outcome for each hazardous situation"
        ),
        approved_by="risk_management_team",
        review_date="2027-05-21",
    )
    @pytest.mark.human_review_required(
        reason=(
            "Whether a risk is acceptable cannot be automatically determined — acceptability "
            "depends on org-defined criteria that may incorporate clinical judgment, regulatory "
            "guidance interpretation, benefit-risk considerations, and state-of-the-art "
            "assessment; requires qualified risk management personnel review"
        )
    )
    def test_risk_evaluation_records_exist_per_hazard(self, controls_evidence: dict):
        devices = controls_evidence.get("iso14971_devices", [])
        no_evaluation = [
            d for d in devices
            if not d.get("risk_evaluation_records_exist", False)
        ]
        assert not no_evaluation, (
            f"Risk evaluation records must exist for each device "
            f"(ISO 14971 §6). Missing: {[d['device_id'] for d in no_evaluation]}"
        )
```

---

## Clause 7 — Risk Control

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestClause7_RiskControl:
    """Clause 7 — Risk control: option selection, implementation, verification, new risks."""

    @pytest.mark.assumption(
        id="ASSUME-14971-CTRL-001",
        description=(
            "Risk control measures selected in priority order per §7.1: (1) inherent safety "
            "by design, (2) protective measures in device or manufacturing process, "
            "(3) information for safety (IFU warnings); lower-priority measures used only "
            "when higher-priority not practicable; rationale for priority selection documented; "
            "risk control measures verified for effectiveness before implementation in "
            "production; new risks introduced by controls evaluated"
        ),
        approved_by="risk_management_team",
        review_date="2027-05-21",
    )
    def test_risk_control_measures_documented(self, controls_evidence: dict):
        devices = controls_evidence.get("iso14971_devices", [])
        no_controls = [
            d for d in devices
            if d.get("has_unacceptable_risks", True)
            and not d.get("risk_control_records_exist", False)
        ]
        assert not no_controls, (
            f"Risk control records must exist for devices with unacceptable risks "
            f"(ISO 14971 §7). Missing: {[d['device_id'] for d in no_controls]}"
        )

    def test_risk_control_verification_records_exist(self, controls_evidence: dict):
        devices = controls_evidence.get("iso14971_devices", [])
        no_verification = [
            d for d in devices
            if d.get("risk_controls_implemented", False)
            and not d.get("risk_control_verification_records_exist", False)
        ]
        assert not no_verification, (
            f"Risk control verification records must exist demonstrating controls "
            f"are implemented and effective (ISO 14971 §7.4). "
            f"Missing: {[d['device_id'] for d in no_verification]}"
        )

    def test_new_risks_from_controls_evaluated(self, controls_evidence: dict):
        devices = controls_evidence.get("iso14971_devices", [])
        no_secondary_risk_eval = [
            d for d in devices
            if d.get("risk_controls_implemented", False)
            and not d.get("new_risks_from_controls_evaluated", False)
        ]
        assert not no_secondary_risk_eval, (
            f"New risks introduced by risk control measures must be identified and "
            f"evaluated (ISO 14971 §7.6). Missing: {[d['device_id'] for d in no_secondary_risk_eval]}"
        )
```

---

## Clause 8 — Residual Risk Evaluation and Benefit-Risk

**Overall: CONTESTED — Pattern 3**

```python
class TestClause8_ResidualRisk:
    """Clause 8 — Residual risk evaluation and benefit-risk determination."""

    @pytest.mark.assumption(
        id="ASSUME-14971-RESID-001",
        description=(
            "Overall residual risk evaluated after all risk control measures applied; "
            "if overall residual risk is not acceptable per defined criteria: benefit-risk "
            "analysis performed using clinical evidence; benefit-risk analysis references "
            "published clinical data, post-market data from similar devices, and regulatory "
            "guidance; benefit-risk determination documented with supporting evidence; "
            "if benefit-risk is negative: device cannot be released — this is a hard stop"
        ),
        approved_by="risk_management_team",
        review_date="2027-05-21",
    )
    @pytest.mark.human_review_required(
        reason=(
            "Overall residual risk acceptability and benefit-risk determination require "
            "clinical judgment — whether the clinical benefits outweigh the residual risks "
            "requires assessment of clinical literature, patient population, available "
            "alternatives, and regulatory context; cannot be automated"
        )
    )
    def test_residual_risk_evaluation_documented(self, controls_evidence: dict):
        devices = controls_evidence.get("iso14971_devices", [])
        no_residual = [
            d for d in devices
            if not d.get("residual_risk_evaluation_documented", False)
        ]
        assert not no_residual, (
            f"Overall residual risk evaluation must be documented (ISO 14971 §8). "
            f"Missing: {[d['device_id'] for d in no_residual]}"
        )
```

---

## Clause 9.1 — Risk Management Report (DETERMINISTIC gate)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause9_1_RiskManagementReport:
    """Clause 9.1 — Risk management report: required before commercial distribution."""

    def test_risk_management_report_exists(self, controls_evidence: dict):
        devices = controls_evidence.get("iso14971_devices", [])
        no_report = [d for d in devices if not d.get("risk_management_report_exists", False)]
        assert not no_report, (
            f"Risk management report must exist and be completed before commercial "
            f"distribution (ISO 14971 §9.1). Missing: {[d['device_id'] for d in no_report]}"
        )

    def test_risk_management_report_references_plan(self, controls_evidence: dict):
        devices = controls_evidence.get("iso14971_devices", [])
        report_without_plan_ref = [
            d for d in devices
            if d.get("risk_management_report_exists", False)
            and not d.get("report_references_risk_plan", False)
        ]
        assert not report_without_plan_ref, (
            f"Risk management report must confirm the risk management plan was implemented "
            f"and overall residual risk is acceptable (ISO 14971 §9.1). "
            f"Missing reference: {[d['device_id'] for d in report_without_plan_ref]}"
        )
```

---

## Clause 10 — Post-Production Information

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestClause10_PostProduction:
    """Clause 10 — Post-production information monitoring and risk file updates."""

    def test_post_production_monitoring_plan_exists(self, controls_evidence: dict):
        devices = controls_evidence.get("iso14971_devices", [])
        no_pms_plan = [
            d for d in devices
            if not d.get("post_production_monitoring_plan_exists", False)
        ]
        assert not no_pms_plan, (
            f"Post-production monitoring plan must exist for each device "
            f"(ISO 14971 §10). Missing: {[d['device_id'] for d in no_pms_plan]}"
        )

    @pytest.mark.assumption(
        id="ASSUME-14971-PMS-001",
        description=(
            "Post-production information sources monitored include: complaint data, MDR/vigilance "
            "reports, published scientific and clinical literature, post-market clinical "
            "follow-up data, service and repair records, similar device adverse events; "
            "monitoring frequency defined in plan; risk file reviewed and updated when "
            "post-production information indicates new hazards, changed probability, or "
            "changed severity; threshold for triggering risk file update documented; "
            "review records retained"
        ),
        approved_by="risk_management_team",
        review_date="2027-05-21",
    )
    def test_risk_file_updated_from_post_production_data(
        self, controls_evidence: dict
    ):
        pms = controls_evidence.get("iso14971_post_production", {})
        assert pms.get("post_production_review_process_exists", False), (
            "Process to review post-production information and update the risk file "
            "must exist (ISO 14971 §10)"
        )
```

---

## Risk management file completeness gate

```python
class TestRiskManagementFileCompleteness:
    """Risk management file: all required document types must be present."""

    @pytest.mark.assumption(
        id="ASSUME-14971-FILE-001",
        description=(
            "Risk management file is a collection (not necessarily a single document); "
            "may be maintained as cross-references to documents in DHF/technical file; "
            "file index maintained showing all required document types and their locations; "
            "file current as of most recent design change; file reviewed before each "
            "regulatory submission and before commercial distribution"
        ),
        approved_by="risk_management_team",
        review_date="2027-05-21",
    )
    def test_risk_management_file_contains_all_required_documents(
        self, controls_evidence: dict
    ):
        devices = controls_evidence.get("iso14971_devices", [])
        for device in devices:
            present_docs = set(device.get("risk_file_document_types_present", []))
            missing_docs = ISO14971_RISK_FILE_REQUIRED_DOCUMENTS - present_docs
            assert not missing_docs, (
                f"Risk management file for '{device['device_id']}' is missing required "
                f"document types: {missing_docs} (ISO 14971)"
            )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-14971-HAZID-001 | 5.2 | Systematic hazard identification method documented; updated on design change | 2027-05-21 |
| ASSUME-14971-HAZID-002 | 5.3 | Risk estimation: probability + severity per defined scale; worst-case when prob unknown | 2027-05-21 |
| ASSUME-14971-EVAL-001 | 6 (CONTESTED) | Risk evaluation against plan criteria; benefit-risk if residual unacceptable | 2027-05-21 |
| ASSUME-14971-CTRL-001 | 7 | Risk control priority order: design → protective measure → IFU; verification before production | 2027-05-21 |
| ASSUME-14971-RESID-001 | 8 (CONTESTED) | Overall residual risk evaluation; benefit-risk with clinical evidence if unacceptable | 2027-05-21 |
| ASSUME-14971-PMS-001 | 10 | PMS sources: complaints, MDR, literature, PMCF; risk file updated when new info | 2027-05-21 |
| ASSUME-14971-FILE-001 | Overall | Risk file index maintained; cross-references to DHF/tech file acceptable | 2027-05-21 |

---

## Cross-standard notes

**IEC 62304 §7 ↔ ISO 14971:** IEC 62304 §7 is the software-specific instantiation of the ISO 14971 process. Software failure modes are hazards; IEC 62304 §7 generates the risk control verification records that must appear in the ISO 14971 risk file. A complete medical device software risk management package must show this bidirectional link.

**EU MDR Annex I §3 ↔ ISO 14971:** EU MDR requires risk management throughout the device lifecycle. ISO 14971 is the harmonized standard; conformity to ISO 14971 creates a presumption of conformity with Annex I §3. The risk management report (§9.1 gate) is required content in the technical documentation under Annex II.
