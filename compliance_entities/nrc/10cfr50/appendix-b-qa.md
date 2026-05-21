# NRC 10 CFR Part 50 — Appendix B: Quality Assurance Criteria

**Registry path:** `/regulation-registry/NRC/10CFR50/AppendixB/`
**Regulation:** 10 CFR Part 50 Appendix B — Quality Assurance Criteria for Nuclear Power Plants and Fuel Reprocessing Plants
**Last parsed:** 2026-05-21
**Applies to:** Commercial nuclear power plant licensees holding operating licenses (OL) or combined licenses (COL) under 10 CFR Part 50 or Part 52; construction permit holders; nuclear power plant applicants during the licensing process
**Trigger:** NRC license to operate or construct a commercial nuclear power plant in the United States; Appendix B (QA) applies from earliest design phases; event reporting, maintenance rule, fire protection, and ISI/IST requirements apply throughout the operating license period
**Jurisdiction:** United States; enforced by the U.S. Nuclear Regulatory Commission through routine inspections, resident inspectors, and enforcement actions including Notices of Violation, Confirmatory Action Letters, and civil penalties
**Not applicable to:** Research and test reactors (10 CFR Part 50 applies partially but with different technical requirements); non-power utilization facilities; fuel cycle facilities (10 CFR Part 70); nuclear materials licensees; decommissioned reactors (10 CFR Part 50 Subpart E DECON/SAFSTOR requirements differ)
**Overall confidence:** MEDIUM — three criteria have DETERMINISTIC thresholds (XII calibration, XVII retention, XVIII audit cadence); remaining 15 criteria are PARAMETERIZED (adequacy determinations require QA expert evaluation)
**Covers:** All 18 QA Criteria; primary automation targets are Criteria XII (M&TE calibration), XVII (records retention), and XVIII (audit cadence)

---

## Scope Pre-Condition

```python
@pytest.fixture(autouse=True)
def require_nrc_licensed_reactor(facility_scope: dict):
    if not facility_scope.get("is_nrc_licensed_nuclear_facility"):
        pytest.skip("Facility is not an NRC-licensed nuclear reactor — tests not applicable")
```

---

## Appendix B Overview — 18 Criteria

| Criterion | Title | Confidence | Primary automation target |
|---|---|---|---|
| I | Organization | PARAMETERIZED | QA function independence check |
| II | QA Program | PARAMETERIZED | Written QA program existence |
| III | Design Control | PARAMETERIZED | Design verification method documented |
| IV | Procurement Document Control | PARAMETERIZED | QA requirements flow-down to suppliers |
| V | Instructions, Procedures, Drawings | PARAMETERIZED | Activity-specific written procedures exist |
| VI | Document Control | PARAMETERIZED | Document control system existence |
| VII | Control of Purchased Material, Equipment, and Services | PARAMETERIZED | Supplier QA evaluation records |
| VIII | Identification and Control of Materials, Parts, and Components | PARAMETERIZED | Traceability from fabrication to installation |
| IX | Control of Special Processes | PARAMETERIZED | Special process qualification records |
| X | Inspection | PARAMETERIZED | Inspection program existence; independence |
| XI | Test Control | PARAMETERIZED | Test procedure and results documentation |
| **XII** | **Control of Measuring and Test Equipment** | **DETERMINISTIC (calibration intervals)** | **Calibration currency and NIST traceability** |
| XIII | Handling, Storage, Shipping, Preservation | PARAMETERIZED | Handling procedures for safety-related items |
| XIV | Inspection, Test, and Operating Status | PARAMETERIZED | Status marking system existence |
| XV | Nonconforming Materials, Parts, or Components | PARAMETERIZED | CAP entry timeliness (24-hour) |
| XVI | Corrective Action | PARAMETERIZED | Root cause for SCAQs; recurrence prevention |
| **XVII** | **Quality Assurance Records** | **DETERMINISTIC (lifetime retention)** | **Records retained for life of facility** |
| **XVIII** | **Audits** | **DETERMINISTIC (cadence)** | **Annual internal; 2-year supplier audit** |

---

## Criterion XII — Control of Measuring and Test Equipment (DETERMINISTIC)

### Source excerpt

> **Appendix B, Criterion XII:** Measures shall be established to assure that tools, gauges, instruments, and other measuring and testing devices used in activities affecting quality are properly controlled, calibrated, and adjusted at specified periods to maintain accuracy within necessary limits.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | M&TE used in safety-related activities | DETERMINISTIC |
| Obligation | Calibrated at specified intervals; calibration traceable to national standards | DETERMINISTIC |
| Obligation | Out-of-tolerance instruments trigger impact evaluation | DETERMINISTIC |
| Evidence | Calibration record per instrument (ID, standard used, as-found/as-left values, next-due date) | DETERMINISTIC |
| Standard | Traceable to NIST (National Institute of Standards and Technology) | DETERMINISTIC |

### Calibration interval requirements

| M&TE category | Interval basis | Classification |
|---|---|---|
| Safety-related instruments | Established based on use frequency and instrument stability; documented in calibration program | PARAMETERIZED (interval adequacy) |
| Instruments with manufacturer-specified interval | Follow manufacturer interval unless facility-documented basis for deviation | PARAMETERIZED |
| Out-of-tolerance on as-found check | Immediately removed from service; impact evaluation initiated; previous measurements using instrument evaluated for validity | DETERMINISTIC (trigger is binary) |
| Calibration standard traceability | Direct or indirect traceability to NIST via calibration hierarchy documented | DETERMINISTIC |

**Assumption (ASSUME-NRC50-QA-002):** M&TE calibration is compliant when: (1) each safety-related instrument has a documented calibration interval established in the calibration program; (2) calibration interval is based on use frequency, past calibration history, and manufacturer recommendations — documented technical justification required; (3) calibration records for each instrument capture: instrument ID, calibration date, calibration standards used, as-found values, as-left values (after adjustment), next calibration due date, calibrating technician ID; (4) all calibration standards are traceable to NIST via an unbroken chain of comparisons; (5) any instrument found out-of-tolerance on as-found check: (a) immediately tagged out of service, (b) impact evaluation performed on all activities/measurements that used the instrument since last valid calibration, (c) impact evaluation results documented and dispositioned through the CAP; (6) electronic calibration management systems must protect calibration records from modification (audit trail required).

**Overall: DETERMINISTIC for calibration traceability and out-of-tolerance triggers → Pattern 1; PARAMETERIZED for interval adequacy → Pattern 2**

---

## Criterion XVII — Quality Assurance Records (DETERMINISTIC — lifetime retention)

### Source excerpt

> **Appendix B, Criterion XVII:** Sufficient records shall be maintained to furnish evidence of activities affecting quality. The records shall include at least the following: Operating logs and the results of reviews, inspections, tests, audits, monitoring of work performance, and materials analyses. Records shall be identifiable and retrievable. Retention times of records shall be at least equal to the life of the part or component or, for structure and system records, at least the life of the plant.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Any activity affecting quality generates a record | DETERMINISTIC |
| Obligation | Records retained for at least the life of the associated part/component/structure/system | DETERMINISTIC |
| Minimum retention | Life of the plant; NRC guidance: minimum 5 years after permanent shutdown for most records | DETERMINISTIC |
| Condition | Records must be identifiable and retrievable | DETERMINISTIC |
| Obligation | Vital records (original design, FSAR, licensing basis) protected against fire, flood, theft | DETERMINISTIC |
| Evidence | Records management program; vital records protection documentation | DETERMINISTIC |

### Records retention requirements

| Record type | Retention | Classification |
|---|---|---|
| Design records (drawings, calculations, specifications) | Life of plant | DETERMINISTIC |
| Inspection and test records | Life of associated component/structure | DETERMINISTIC |
| Operating logs | Life of plant (minimum 5 years post-shutdown) | DETERMINISTIC |
| Audit records | Life of plant | DETERMINISTIC |
| Training and qualification records | Life of plant (individual personnel records: duration of employment + 5 years) | DETERMINISTIC |
| Calibration records | Life of associated instrument | DETERMINISTIC |

**Assumption (ASSUME-NRC50-QA-005):** QA records compliance: (1) records management program defines record types, retention periods, location, and custodian; (2) vital records (licensing basis documents, design calculations for safety-related structures/systems/components) stored in protected off-site location or fireproof vault; (3) electronic records acceptable with: access controls, audit trail, backup/recovery procedures, and media obsolescence management plan; (4) records retrievable within a reasonable time (NRC inspection expectation: 24–48 hours for most records); (5) following permanent shutdown, all records retained for minimum 5 years per 10 CFR 50.75(g) — decommissioning records retained until NRC license termination; (6) records must be legible, complete, and include sufficient information to reconstruct the activity.

**Overall: DETERMINISTIC → Pattern 1**

---

## Criterion XVIII — Audits (DETERMINISTIC — cadence)

### Source excerpt

> **Appendix B, Criterion XVIII:** A comprehensive system of planned and periodic audits shall be carried out to verify compliance with all aspects of the quality assurance program and to determine the effectiveness of the program. Audits shall be performed in accordance with written procedures or checklists by appropriately trained personnel not having direct responsibilities in the areas being audited. Audit results shall be documented and reviewed by management having responsibility in the area audited. Follow-up action, including re-audit of deficient areas, shall be taken where indicated.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | QA program exists | DETERMINISTIC |
| Obligation | Comprehensive system of planned and periodic audits | DETERMINISTIC |
| Internal audit cadence | At least annually for all elements of the QA program | DETERMINISTIC |
| Supplier audit cadence | NRC guidance and industry practice: at least every 2 years for qualified suppliers | DETERMINISTIC |
| Independence | Auditors must not have direct responsibility in the area being audited | DETERMINISTIC |
| Evidence | Written audit procedures; audit findings; management response; CAP entries for findings; follow-up closure | DETERMINISTIC |

### Audit program requirements

| Requirement | Value | Classification |
|---|---|---|
| Annual QA program audit coverage | 100% of QA program elements over a rolling annual cycle | DETERMINISTIC |
| Auditor qualification | Trained and qualified per written qualification program; Lead Auditor must meet written criteria | DETERMINISTIC |
| Independence of auditors | Not employed in the area being audited; organizational separation documented | DETERMINISTIC |
| Management review | Audit results reviewed by management with responsibility for area audited | DETERMINISTIC |
| CAP entry for findings | All audit findings entered into Corrective Action Program | DETERMINISTIC |
| Follow-up/re-audit | Required where deficiencies identified; closure verified before closing audit finding | DETERMINISTIC |
| Supplier audits | Commercial-grade dedication suppliers audited against QA requirements; 2-year cycle minimum | DETERMINISTIC (cadence) / PARAMETERIZED (scope adequacy) |

**Assumption (ASSUME-NRC50-QA-001):** Audit compliance is demonstrated when: (1) annual audit plan documents which QA program elements will be audited and when — all 18 criteria must be covered within each annual cycle or with documented coverage schedule; (2) each audit conducted by personnel with no direct responsibility for the work area: this means the auditor is not the supervisor, procedure writer, or direct practitioner of the process being audited — organizational independence documented per the QA program; (3) all audit findings entered into CAP within 5 business days of audit close-out meeting; (4) corrective actions for audit findings tracked to closure with verification; (5) for supplier audits: minimum 2-year cycle for suppliers on the Approved Suppliers List (ASL); audit scope covers quality plan adequacy, procedure compliance, and records completeness; (6) audit records retained per Criterion XVII (life of plant).

**Overall: DETERMINISTIC for audit cadence → Pattern 1; PARAMETERIZED for audit scope adequacy → Pattern 2**

---

## Criterion XV — Nonconforming Materials, Parts, or Components (PARAMETERIZED with DETERMINISTIC trigger)

### Source excerpt

> **Appendix B, Criterion XV:** Measures shall be established to control materials, parts, or components which do not conform to requirements in order to prevent their inadvertent use or installation. These measures shall include, as appropriate, procedures for identification, documentation, segregation, disposition, and notification to affected organizations. Nonconforming items shall be reviewed and accepted, rejected, repaired, or reworked in accordance with documented procedures.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Item identified as not conforming to requirements | DETERMINISTIC (binary: nonconforming or not) |
| Obligation | Document and segregate nonconforming item to prevent inadvertent use | DETERMINISTIC |
| Obligation | Enter into CAP — NRC and industry guidance: within 24 hours of identification | PARAMETERIZED (24h industry expectation) |
| Disposition options | Use-as-is, rework, repair, reject/scrap — each requires documented justification | PARAMETERIZED |
| Use-as-is disposition | Requires documented technical justification by qualified engineer; QA review | PARAMETERIZED (engineering judgment) |
| Rework/repair disposition | Must return item to fully conforming condition per applicable code/specification | PARAMETERIZED |

### Nonconformance disposition requirements

| Disposition | Requirements | Classification |
|---|---|---|
| Use-as-is | Written technical justification; QA concurrence; no adverse effect on safety function documented | PARAMETERIZED |
| Rework | Re-inspected/re-tested after rework to original acceptance criteria | DETERMINISTIC (reinspect required) |
| Repair | Repair procedure qualified; ASME Code repair for pressure-retaining items | PARAMETERIZED (code compliance) |
| Reject/Scrap | Physically marked or destroyed to prevent inadvertent use; controlled disposal | DETERMINISTIC |

**Assumption (ASSUME-NRC50-QA-003):** Nonconformance compliance: (1) nonconforming item identified by tag, label, or physical segregation immediately upon identification — item physically separated from conforming stock wherever practicable; (2) CAP entry created within 24 hours of identification (NRC inspection expectation per NUREG-1600 and INPO AP-913); (3) disposition documented with technical justification by a qualified engineer — disposition authority level (supervisor, engineer, QA manager) defined in QA program; (4) use-as-is dispositions for safety-related items require review and concurrence by QA; (5) significant conditions adverse to quality (SCAQs — nonconformances with potential to affect safety function) escalated to Criterion XVI corrective action process including root cause analysis; (6) trend analysis of nonconformances performed at least quarterly to identify systemic issues.

**Overall: PARAMETERIZED → Pattern 2**

---

## Criterion XVI — Corrective Action (PARAMETERIZED — root cause for SCAQs)

### Source excerpt

> **Appendix B, Criterion XVI:** Measures shall be established to assure that conditions adverse to quality, such as failures, malfunctions, deficiencies, deviations, defective material and equipment, and nonconformances are promptly identified and corrected. In the case of significant conditions adverse to quality, the measures shall assure that the cause of the condition is determined and corrective action taken to preclude repetition.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Condition adverse to quality (CAQ) identified | DETERMINISTIC (binary: CAQ exists or not) |
| Obligation | Prompt identification and correction | PARAMETERIZED ("prompt" = situational) |
| Significant CAQ (SCAQ) | Must determine cause; must preclude repetition | PARAMETERIZED (root cause determination) |
| SCAQ identification | Requires documented criteria in QA program for distinguishing CAQ from SCAQ | PARAMETERIZED |
| Root cause analysis | Required for all SCAQs; method documented | PARAMETERIZED (methodology adequacy) |
| Corrective action verification | Effectiveness of corrective action must be verified | PARAMETERIZED |

### SCAQ vs. CAQ distinction

| Tier | Description | Required response |
|---|---|---|
| Condition Adverse to Quality (CAQ) | Any departure from requirements | Document, correct, close |
| Significant Condition Adverse to Quality (SCAQ) | Could affect safety function; systemic; recurring; precursor to more serious event | Document, correct, root cause analysis, corrective action to preclude repetition, effectiveness review |

**Assumption (ASSUME-NRC50-QA-004):** Corrective action compliance: (1) written criteria in the QA program define what constitutes an SCAQ — criteria must be defensible against NRC inspection scrutiny; (2) root cause analysis (RCA) performed for all SCAQs using a documented methodology (e.g., HPES, ORPS trending, cause-and-effect analysis, or equivalent); (3) corrective actions documented with: action description, responsible individual, due date, and completion criteria; (4) corrective action effectiveness review performed after implementation — typically after 6–12 months or after next performance opportunity; (5) CAP database maintained with status of all open CARs; overdue corrective actions flagged and escalated to management; (6) trending performed at least quarterly — significant trends treated as SCAQs in their own right; (7) NRC performance indicator: corrective action closure timeliness tracked; SCAQs root cause analysis completed within 45 days unless extended with documented justification.

**Overall: PARAMETERIZED → Pattern 2; SCAQ determination requires human judgment → Pattern 3 for adequacy evaluation**

---

## Criteria I–XI and XIII–XIV (PARAMETERIZED overview)

The following criteria are PARAMETERIZED — they require QA auditor or subject matter expert evaluation. They are included for completeness; individual specification files are not created for PARAMETERIZED-only criteria without DETERMINISTIC sub-elements.

| Criterion | Automation surface | Pattern |
|---|---|---|
| I — Organization | QA organization chart exists; QA reports to management with sufficient authority (written function description) | Pattern 2 |
| II — QA Program | Written QA Program document exists; approved by senior management; covers all 18 criteria | Pattern 2 |
| III — Design Control | Design verification method (independent review, alternate calculation, or testing) documented for each safety-related design | Pattern 2 |
| IV — Procurement Document Control | Purchase orders for safety-related items include QA requirements or reference approved QA plan | Pattern 2 |
| V — Instructions, Procedures, Drawings | Written procedures required for all activities affecting quality; procedure approval documented | Pattern 2 |
| VI — Document Control | Document control system prevents use of superseded documents; change authorization process exists | Pattern 2 |
| VII — Control of Purchased Material, Equipment, and Services | Supplier qualification records (audit reports, surveys, or source verification) on file for each ASL supplier | Pattern 2 |
| VIII — ID and Control of Materials, Parts, Components | Traceability from material test report to installed component documented; no unmarked safety-related items | Pattern 2 |
| IX — Control of Special Processes | Qualification records for each special process (welding, NDE, heat treatment) and each qualified practitioner | Pattern 2 |
| X — Inspection | Inspection program covers all safety-related activities; inspectors do not inspect own work | Pattern 2 |
| XI — Test Control | Test procedures specify acceptance criteria before testing; test results reviewed by qualified individual | Pattern 2 |
| XIII — Handling, Storage, Shipping | Written handling/storage procedures for safety-related items; shelf-life controls for age-sensitive items | Pattern 2 |
| XIV — Inspection, Test, and Operating Status | Status tags/stamps/markings prevent use of uninspected or failed items; controlled hold/accept system | Pattern 2 |

---

## Test specifications

### YAML spec — Appendix B QA (DETERMINISTIC criteria)

```yaml
spec_id: NRC-50-APPB-001
framework: NRC 10 CFR Part 50
sections:
  - Appendix B Criterion XII (M&TE calibration)
  - Appendix B Criterion XVII (QA records retention)
  - Appendix B Criterion XVIII (audit cadence)
  - Appendix B Criterion XV (nonconformance CAP entry)
confidence: MIXED
  criterion_xii: HIGH
  criterion_xvii: HIGH
  criterion_xviii: HIGH
  criterion_xv: MEDIUM
patterns_used:
  - Pattern 1 (DETERMINISTIC assertions)
  - Pattern 2 (assumption-based assertions)
scope_gate: is_nrc_licensed_nuclear_facility
assumptions:
  - ASSUME-NRC50-QA-001  # Audit: independence, coverage, cadence
  - ASSUME-NRC50-QA-002  # M&TE: calibration intervals, NIST traceability, out-of-tolerance triggers
  - ASSUME-NRC50-QA-003  # Nonconformances: CAP entry 24h, disposition, SCAQ escalation
  - ASSUME-NRC50-QA-004  # Corrective action: SCAQ criteria, RCA, effectiveness review
  - ASSUME-NRC50-QA-005  # Records: lifetime retention, vital records protection, retrievability
```

### Python tests — `tests/nrc_10cfr50/test_appendix_b_qa.py`

```python
import pytest
from datetime import datetime, timedelta
from typing import Optional

# ---------------------------------------------------------------------------
# Scope gate
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def require_nrc_licensed_reactor(facility_scope: dict):
    if not facility_scope.get("is_nrc_licensed_nuclear_facility"):
        pytest.skip("Facility is not an NRC-licensed nuclear reactor — tests not applicable")


# ---------------------------------------------------------------------------
# Criterion XII — M&TE Calibration (Pattern 1 + Pattern 2)
# ---------------------------------------------------------------------------

@pytest.mark.assumption(
    id="ASSUME-NRC50-QA-002",
    description="M&TE calibration: intervals documented, NIST traceability, out-of-tolerance triggers impact evaluation",
    approved_by="QA Manager",
    review_date="2026-05-21"
)
class TestCriterionXII:

    def test_mte_calibration_record_has_required_fields(self, mte_record: dict):
        """Each M&TE calibration record must have all required fields."""
        required_fields = [
            "instrument_id",
            "calibration_date",
            "calibration_standard_id",
            "as_found_values",
            "as_left_values",
            "next_calibration_due",
            "calibrating_technician_id",
        ]
        missing = [f for f in required_fields if not mte_record.get(f)]
        assert not missing, f"M&TE record {mte_record.get('instrument_id')} missing fields: {missing}"

    def test_mte_calibration_is_current(self, mte_record: dict):
        """M&TE used in safety-related activities must not be past calibration due date."""
        due = mte_record.get("next_calibration_due")
        assert due is not None, f"No calibration due date for {mte_record.get('instrument_id')}"
        if isinstance(due, str):
            due = datetime.fromisoformat(due)
        assert due >= datetime.now(), (
            f"M&TE {mte_record.get('instrument_id')} calibration overdue since {due.date()}"
        )

    def test_mte_calibration_standard_is_nist_traceable(self, mte_record: dict, calibration_standards_db: dict):
        """Calibration standard used must have documented NIST traceability."""
        std_id = mte_record.get("calibration_standard_id")
        assert std_id in calibration_standards_db, f"Calibration standard {std_id} not in standards database"
        std = calibration_standards_db[std_id]
        assert std.get("nist_traceable"), (
            f"Calibration standard {std_id} does not have documented NIST traceability"
        )
        # Traceability chain must not be expired
        cert_expiry = std.get("certificate_expiry")
        if cert_expiry:
            if isinstance(cert_expiry, str):
                cert_expiry = datetime.fromisoformat(cert_expiry)
            assert cert_expiry >= datetime.now(), (
                f"NIST traceability certificate for standard {std_id} expired {cert_expiry.date()}"
            )

    def test_out_of_tolerance_triggers_impact_evaluation(self, mte_record: dict):
        """M&TE found out-of-tolerance on as-found check must have a CAP entry and impact evaluation."""
        if not mte_record.get("out_of_tolerance_on_as_found"):
            pytest.skip("Instrument was within tolerance on as-found check — not applicable")
        assert mte_record.get("cap_entry_id"), (
            f"M&TE {mte_record.get('instrument_id')} was out-of-tolerance but has no CAP entry"
        )
        assert mte_record.get("impact_evaluation_complete"), (
            f"M&TE {mte_record.get('instrument_id')} out-of-tolerance but impact evaluation not completed"
        )

    def test_mte_interval_has_documented_basis(self, mte_calibration_program: dict, instrument_id: str):
        """Each M&TE must have a documented basis for its calibration interval."""
        instrument = mte_calibration_program.get(instrument_id)
        assert instrument is not None, f"Instrument {instrument_id} not found in calibration program"
        assert instrument.get("interval_basis"), (
            f"Instrument {instrument_id} calibration interval has no documented technical basis"
        )


# ---------------------------------------------------------------------------
# Criterion XVII — QA Records Retention (Pattern 1)
# ---------------------------------------------------------------------------

class TestCriterionXVII:

    def test_qa_records_program_exists(self, qa_records_program: dict):
        """A written QA records management program must exist."""
        assert qa_records_program.get("program_document_id"), "No QA records management program document"
        assert qa_records_program.get("approved_by"), "QA records program has no management approval"

    def test_design_records_retention_meets_lifetime_requirement(self, qa_records_program: dict):
        """Safety-related design records must be retained for the life of the plant."""
        design_retention = qa_records_program.get("design_records_retention")
        assert design_retention == "life_of_plant" or design_retention == "lifetime", (
            f"Design records retention is '{design_retention}', expected 'life_of_plant'"
        )

    def test_vital_records_have_protected_storage(self, qa_records_program: dict):
        """Vital records (licensing basis, design records) must have protected off-site or fire-rated storage."""
        assert qa_records_program.get("vital_records_protection"), (
            "QA program has no vital records protection documentation"
        )
        protection = qa_records_program["vital_records_protection"]
        has_offsite = protection.get("offsite_location") or protection.get("fireproof_vault")
        assert has_offsite, "Vital records have no off-site storage or fireproof vault protection"

    @pytest.mark.assumption(
        id="ASSUME-NRC50-QA-005",
        description="QA records: lifetime retention, vital records protection, electronic records acceptable with integrity controls",
        approved_by="QA Manager",
        review_date="2026-05-21"
    )
    def test_electronic_records_have_integrity_controls(self, qa_records_program: dict):
        """If electronic records are used, audit trail and backup/recovery must be documented."""
        uses_electronic = qa_records_program.get("uses_electronic_records", False)
        if not uses_electronic:
            pytest.skip("Facility does not use electronic QA records — not applicable")
        e_controls = qa_records_program.get("electronic_records_controls", {})
        assert e_controls.get("audit_trail_enabled"), "Electronic QA records system lacks audit trail"
        assert e_controls.get("backup_procedure_id"), "Electronic QA records system lacks backup procedure"
        assert e_controls.get("media_obsolescence_plan"), (
            "Electronic QA records system has no media obsolescence management plan"
        )

    def test_records_are_retrievable(self, qa_records_program: dict):
        """QA records must be identifiable and retrievable."""
        assert qa_records_program.get("records_index_or_search_system"), (
            "No records index or search system documented — retrievability cannot be assured"
        )


# ---------------------------------------------------------------------------
# Criterion XVIII — Audits (Pattern 1 + Pattern 2)
# ---------------------------------------------------------------------------

@pytest.mark.assumption(
    id="ASSUME-NRC50-QA-001",
    description="Audits: annual coverage of all QA program elements, auditor independence, findings to CAP, 2-year supplier cycle",
    approved_by="QA Manager",
    review_date="2026-05-21"
)
class TestCriterionXVIII:

    def test_annual_audit_plan_covers_all_criteria(self, annual_audit_plan: dict):
        """Annual audit plan must document coverage of all 18 Appendix B criteria."""
        covered_criteria = set(annual_audit_plan.get("criteria_covered", []))
        all_criteria = set(range(1, 19))  # Criteria I–XVIII (1–18)
        missing = all_criteria - covered_criteria
        assert not missing, (
            f"Annual audit plan does not cover Appendix B Criteria: {sorted(missing)}"
        )

    def test_annual_audit_cycle_not_overdue(self, annual_audit_plan: dict):
        """Annual QA program audit must be completed within each calendar year."""
        last_annual = annual_audit_plan.get("last_annual_completion_date")
        assert last_annual is not None, "No annual QA audit completion date recorded"
        if isinstance(last_annual, str):
            last_annual = datetime.fromisoformat(last_annual)
        days_since = (datetime.now() - last_annual).days
        assert days_since <= 365, (
            f"Annual QA audit overdue: last completed {last_annual.date()} ({days_since} days ago)"
        )

    def test_auditors_are_independent(self, audit_report: dict):
        """Auditors must not have direct responsibility in the area being audited."""
        assert audit_report.get("auditor_independence_documented"), (
            f"Audit {audit_report.get('audit_id')} does not document auditor independence"
        )
        # If auditor org unit is provided, verify it differs from auditee org unit
        auditor_org = audit_report.get("auditor_org_unit")
        auditee_org = audit_report.get("auditee_org_unit")
        if auditor_org and auditee_org:
            assert auditor_org != auditee_org, (
                f"Audit {audit_report.get('audit_id')}: auditor org unit matches auditee org unit — "
                "independence not demonstrated"
            )

    def test_audit_findings_entered_in_cap(self, audit_report: dict):
        """All audit findings must be entered into the Corrective Action Program."""
        findings = audit_report.get("findings", [])
        for finding in findings:
            assert finding.get("cap_entry_id"), (
                f"Audit finding '{finding.get('finding_id')}' in audit {audit_report.get('audit_id')} "
                "has no CAP entry"
            )

    def test_supplier_audit_cadence_two_year_maximum(self, supplier_audit_record: dict):
        """Approved Suppliers List suppliers must be audited at least every 2 years."""
        last_audit_date = supplier_audit_record.get("last_audit_date")
        assert last_audit_date is not None, (
            f"Supplier {supplier_audit_record.get('supplier_id')} has no audit date on record"
        )
        if isinstance(last_audit_date, str):
            last_audit_date = datetime.fromisoformat(last_audit_date)
        days_since = (datetime.now() - last_audit_date).days
        two_years_days = 365 * 2
        assert days_since <= two_years_days, (
            f"Supplier {supplier_audit_record.get('supplier_id')} audit overdue: "
            f"last audited {last_audit_date.date()} ({days_since} days ago, limit {two_years_days})"
        )

    def test_audit_management_review_documented(self, audit_report: dict):
        """Audit results must be reviewed by management responsible for the area audited."""
        assert audit_report.get("management_review_date"), (
            f"Audit {audit_report.get('audit_id')} has no documented management review"
        )
        assert audit_report.get("management_reviewer_id"), (
            f"Audit {audit_report.get('audit_id')} management review has no reviewer ID"
        )


# ---------------------------------------------------------------------------
# Criterion XV — Nonconformances (Pattern 2)
# ---------------------------------------------------------------------------

@pytest.mark.assumption(
    id="ASSUME-NRC50-QA-003",
    description="Nonconformances: CAP entry within 24 hours, physical segregation, SCAQ escalation to Criterion XVI",
    approved_by="QA Manager",
    review_date="2026-05-21"
)
class TestCriterionXV:

    def test_nonconforming_item_has_cap_entry(self, nonconformance_record: dict):
        """Every nonconforming item must have a CAP entry."""
        assert nonconformance_record.get("cap_entry_id"), (
            f"Nonconformance {nonconformance_record.get('ncr_id')} has no CAP entry"
        )

    def test_nonconformance_cap_entry_within_24_hours(self, nonconformance_record: dict):
        """CAP entry should be created within 24 hours of nonconformance identification."""
        identified_at = nonconformance_record.get("identified_at")
        cap_created_at = nonconformance_record.get("cap_entry_created_at")
        if not identified_at or not cap_created_at:
            pytest.skip("Missing timestamp data — cannot evaluate CAP timeliness")
        if isinstance(identified_at, str):
            identified_at = datetime.fromisoformat(identified_at)
        if isinstance(cap_created_at, str):
            cap_created_at = datetime.fromisoformat(cap_created_at)
        elapsed_hours = (cap_created_at - identified_at).total_seconds() / 3600
        assert elapsed_hours <= 24, (
            f"NCR {nonconformance_record.get('ncr_id')}: CAP entry created {elapsed_hours:.1f} hours after "
            "identification (threshold: 24 hours)"
        )

    def test_nonconforming_item_is_segregated(self, nonconformance_record: dict):
        """Nonconforming item must be tagged or segregated to prevent inadvertent use."""
        assert nonconformance_record.get("segregation_action"), (
            f"NCR {nonconformance_record.get('ncr_id')}: no segregation action documented"
        )

    def test_nonconformance_has_disposition(self, nonconformance_record: dict):
        """Nonconforming item must have a documented disposition."""
        valid_dispositions = {"use_as_is", "rework", "repair", "reject", "scrap"}
        disposition = nonconformance_record.get("disposition")
        assert disposition in valid_dispositions, (
            f"NCR {nonconformance_record.get('ncr_id')}: disposition '{disposition}' not valid. "
            f"Must be one of: {valid_dispositions}"
        )
        assert nonconformance_record.get("disposition_justification"), (
            f"NCR {nonconformance_record.get('ncr_id')}: disposition '{disposition}' has no technical justification"
        )

    def test_use_as_is_has_qa_concurrence(self, nonconformance_record: dict):
        """Use-as-is disposition for safety-related items requires QA concurrence."""
        if nonconformance_record.get("disposition") != "use_as_is":
            pytest.skip("Disposition is not use-as-is — not applicable")
        if not nonconformance_record.get("safety_related", False):
            pytest.skip("Item is not safety-related — QA concurrence not required")
        assert nonconformance_record.get("qa_concurrence_id"), (
            f"NCR {nonconformance_record.get('ncr_id')}: use-as-is for safety-related item lacks QA concurrence"
        )

    def test_scaq_escalated_to_criterion_xvi(self, nonconformance_record: dict):
        """Items meeting SCAQ criteria must be escalated to Criterion XVI corrective action process."""
        if not nonconformance_record.get("is_scaq", False):
            pytest.skip("Nonconformance is not classified as SCAQ — not applicable")
        assert nonconformance_record.get("corrective_action_report_id"), (
            f"NCR {nonconformance_record.get('ncr_id')} is classified as SCAQ but has no Criterion XVI "
            "Corrective Action Report"
        )


# ---------------------------------------------------------------------------
# Criterion XVI — Corrective Action (Pattern 2 + Pattern 3)
# ---------------------------------------------------------------------------

@pytest.mark.assumption(
    id="ASSUME-NRC50-QA-004",
    description="Corrective action: documented SCAQ criteria, RCA for SCAQs, corrective action tracking and effectiveness review",
    approved_by="QA Manager",
    review_date="2026-05-21"
)
class TestCriterionXVI:

    def test_scaq_criteria_documented_in_qa_program(self, qa_program: dict):
        """QA program must contain written criteria defining what constitutes an SCAQ."""
        assert qa_program.get("scaq_criteria_section"), (
            "QA program has no written SCAQ determination criteria section"
        )

    def test_scaq_has_root_cause_analysis(self, corrective_action_report: dict):
        """Significant Conditions Adverse to Quality (SCAQs) must have a root cause analysis."""
        if not corrective_action_report.get("is_scaq", False):
            pytest.skip("Corrective action report is not for an SCAQ — not applicable")
        assert corrective_action_report.get("root_cause_analysis_complete"), (
            f"CAR {corrective_action_report.get('car_id')} is SCAQ but root cause analysis is not complete"
        )
        assert corrective_action_report.get("root_cause_analysis_method"), (
            f"CAR {corrective_action_report.get('car_id')}: no RCA method documented"
        )

    def test_scaq_has_recurrence_prevention_action(self, corrective_action_report: dict):
        """SCAQs must have documented corrective action designed to preclude repetition."""
        if not corrective_action_report.get("is_scaq", False):
            pytest.skip("CAR is not for an SCAQ — not applicable")
        assert corrective_action_report.get("recurrence_prevention_action"), (
            f"CAR {corrective_action_report.get('car_id')}: SCAQ has no recurrence prevention action"
        )

    def test_corrective_actions_have_due_dates(self, corrective_action_report: dict):
        """All corrective actions must have assigned responsible individuals and due dates."""
        actions = corrective_action_report.get("corrective_actions", [])
        for action in actions:
            assert action.get("responsible_individual"), (
                f"CAR {corrective_action_report.get('car_id')}, action '{action.get('action_id')}': "
                "no responsible individual assigned"
            )
            assert action.get("due_date"), (
                f"CAR {corrective_action_report.get('car_id')}, action '{action.get('action_id')}': no due date"
            )

    def test_scaq_rca_completed_within_45_days(self, corrective_action_report: dict):
        """SCAQ root cause analysis should be completed within 45 days unless extended with documented justification."""
        if not corrective_action_report.get("is_scaq", False):
            pytest.skip("Not an SCAQ — not applicable")
        identified_at = corrective_action_report.get("identified_at")
        rca_completed_at = corrective_action_report.get("rca_completed_at")
        extension_approved = corrective_action_report.get("rca_extension_approved", False)
        if not identified_at or not rca_completed_at:
            pytest.skip("Missing timestamp data for RCA timeliness evaluation")
        if isinstance(identified_at, str):
            identified_at = datetime.fromisoformat(identified_at)
        if isinstance(rca_completed_at, str):
            rca_completed_at = datetime.fromisoformat(rca_completed_at)
        elapsed_days = (rca_completed_at - identified_at).days
        if elapsed_days > 45 and not extension_approved:
            pytest.fail(
                f"CAR {corrective_action_report.get('car_id')}: SCAQ RCA took {elapsed_days} days "
                "(NRC expectation: ≤45 days unless extended with documented justification)"
            )

    @pytest.mark.human_review_required(
        reason="Adequacy of corrective action to preclude repetition of SCAQ is an engineering and "
               "QA judgment determination — requires QA manager and corrective action review board "
               "sign-off per ASSUME-NRC50-QA-004. Pattern 3: surface for human determination."
    )
    def test_scaq_corrective_action_adequacy(self, corrective_action_report: dict):
        """[HUMAN REVIEW] SCAQ corrective action adequacy cannot be determined algorithmically."""
        if not corrective_action_report.get("is_scaq", False):
            pytest.skip("Not an SCAQ — not applicable")
        # Verify human review is recorded
        assert corrective_action_report.get("adequacy_review_by"), (
            f"CAR {corrective_action_report.get('car_id')}: SCAQ corrective action has no documented "
            "adequacy review sign-off — QA manager or CARB review required"
        )
```

---

## Assumption registry (this file)

| ID | Criterion | Summary | Review date |
|---|---|---|---|
| ASSUME-NRC50-QA-001 | Criterion XVIII | Internal QA audits: annually, covering all 18 criteria; auditors independent; findings to CAP; 2-year supplier cycle | 2026-05-21 |
| ASSUME-NRC50-QA-002 | Criterion XII | M&TE calibration: intervals documented with basis; NIST traceability; out-of-tolerance instruments removed + impact evaluation | 2026-05-21 |
| ASSUME-NRC50-QA-003 | Criterion XV | Nonconformances: CAP entry within 24 hours; physical segregation; SCAQ escalated to Criterion XVI; use-as-is requires QA concurrence | 2026-05-21 |
| ASSUME-NRC50-QA-004 | Criterion XVI | Corrective actions: written SCAQ criteria; RCA for SCAQs; recurrence prevention; effectiveness review; RCA within 45 days | 2026-05-21 |
| ASSUME-NRC50-QA-005 | Criterion XVII | QA records: retained for life of facility; vital records in protected storage; electronic records require audit trail + backup | 2026-05-21 |

---

## Cross-references

- **Criterion XII → event-reporting.md:** Out-of-tolerance M&TE used in post-event surveillance may affect reportability determination (§50.72/§50.73)
- **Criterion XV + XVI → 10 CFR Part 50 §50.65:** CAP nonconformances may trigger Maintenance Rule (a)(1) categorization for affected SSCs
- **Criterion XVI → 10 CFR Part 50 §50.73:** SCAQs identified through the CAP may independently trigger LER reportability under §50.73(a)(2)
- **Criterion XVII → ISO 9001 §7.5:** QA records retention requirements are more stringent than ISO 9001 (life of plant vs. minimum period to be determined by organization)
- **Criterion XVIII → 10 CFR Part 50 §50.54(a):** Failure to implement the QA audit program is a direct §50.54(a) violation — significant enforcement history
