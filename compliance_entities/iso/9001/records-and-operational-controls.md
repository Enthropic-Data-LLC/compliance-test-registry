# ISO 9001:2015 — Records and Operational Controls

**Framework:** ISO 9001:2015
**Clauses:** 6.2, 7.1.5.2, 7.2, 7.5, 8.2.3, 8.2.4, 8.5.6, 8.6, 8.7, 9.2, 9.3, 10.2
**Confidence:** DETERMINISTIC-dominant (record existence and operational gates)
**Last parsed:** 2026-05-21

---

## Scope pre-condition

```python
def requires_iso9001(entity_profile: dict) -> bool:
    """
    True if organization has ISO 9001 certification, is seeking certification,
    or has a contractual obligation requiring conformance.
    """
    return entity_profile.get("iso9001_in_scope", False)
```

---

## Constants

```python
# Audit and review recency
ISO9001_INTERNAL_AUDIT_MAX_MONTHS = 12
ISO9001_MANAGEMENT_REVIEW_MAX_MONTHS = 12

# Record retention — ISO 9001 does not specify a minimum; organization must define
# The constants below represent org-ODP values used in assumption text
ISO9001_RECORD_RETENTION_YEARS_ODP = 3  # ASSUME-ISO9001-7_5-001: org-defined
```

---

## Clause 6.2 — Quality Objectives

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Organization with QMS in scope | DETERMINISTIC |
| Condition | ISO 9001 certification scope active | DETERMINISTIC |
| Obligation | Quality objectives documented; measurable; monitored; communicated; updated | DETERMINISTIC |
| Evidence | Quality objectives document with measurable targets; status records | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
import pytest
from datetime import date, timedelta

@pytest.fixture(autouse=True)
def iso9001_scope(entity_profile: dict):
    if not entity_profile.get("iso9001_in_scope", False):
        pytest.skip("ISO 9001 not in scope")

class TestClause6_2_QualityObjectives:
    """Clause 6.2 — Quality objectives: documented, measurable, monitored."""

    def test_quality_objectives_documented(self, controls_evidence: dict):
        qms = controls_evidence.get("iso9001_quality_objectives", {})
        assert qms.get("objectives_documented", False), (
            "Quality objectives must be documented (ISO 9001 §6.2)"
        )

    def test_quality_objectives_measurable(self, controls_evidence: dict):
        qms = controls_evidence.get("iso9001_quality_objectives", {})
        assert qms.get("objectives_measurable", False), (
            "Quality objectives must be measurable (ISO 9001 §6.2.1(b))"
        )

    def test_quality_objectives_monitored(self, controls_evidence: dict):
        qms = controls_evidence.get("iso9001_quality_objectives", {})
        assert qms.get("objectives_monitored", False), (
            "Quality objectives must be monitored (ISO 9001 §6.2.1(c))"
        )

    def test_quality_objectives_communicated(self, controls_evidence: dict):
        qms = controls_evidence.get("iso9001_quality_objectives", {})
        assert qms.get("objectives_communicated", False), (
            "Quality objectives must be communicated (ISO 9001 §6.2.1(e))"
        )
```

---

## Clause 7.1.5.2 — Measurement Traceability

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Measurement instruments used to verify product/service conformity | DETERMINISTIC |
| Condition | Traceability required by the organization or considered an essential part of providing confidence in valid measurement results | DETERMINISTIC |
| Obligation | Calibrated against traceable standards; calibration records retained; calibration status visible; protected from damage | DETERMINISTIC |
| Evidence | Calibration records with standard used, date, result, and next calibration due date | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause7_1_5_2_Calibration:
    """Clause 7.1.5.2 — Measurement traceability: calibration records for M&M equipment."""

    def test_calibration_records_exist(self, controls_evidence: dict):
        instruments = controls_evidence.get("iso9001_measurement_instruments", [])
        uncalibrated = [
            i for i in instruments
            if i.get("calibration_required", True)
            and not i.get("calibration_record_exists", False)
        ]
        assert not uncalibrated, (
            f"Calibration records must exist for all measurement instruments where traceability "
            f"is required. Missing records for: {[i['instrument_id'] for i in uncalibrated]}"
        )

    def test_calibration_traceable_to_standards(self, controls_evidence: dict):
        instruments = controls_evidence.get("iso9001_measurement_instruments", [])
        not_traceable = [
            i for i in instruments
            if i.get("calibration_required", True)
            and not i.get("traceable_to_national_standard", False)
        ]
        assert not not_traceable, (
            f"Calibration must be traceable to national or international measurement standards. "
            f"Not traceable: {[i['instrument_id'] for i in not_traceable]}"
        )

    def test_calibration_currency(self, controls_evidence: dict, reference_date: date):
        instruments = controls_evidence.get("iso9001_measurement_instruments", [])
        overdue = [
            i for i in instruments
            if i.get("calibration_required", True)
            and i.get("next_calibration_due") is not None
            and i["next_calibration_due"] < reference_date
        ]
        assert not overdue, (
            f"Calibration overdue for instruments: {[i['instrument_id'] for i in overdue]}"
        )
```

---

## Clause 7.2 — Competence

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Persons doing work under QMS that affects quality performance | DETERMINISTIC |
| Condition | Personnel affect conformity of products/services to requirements | DETERMINISTIC |
| Obligation | Competence requirements defined; evidence of competence retained; actions taken when competence not achieved; effectiveness of actions evaluated | DETERMINISTIC |
| Evidence | Competence records (education, training, skills, experience); training completion records; gap analysis and remediation records | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause7_2_Competence:
    """Clause 7.2 — Competence: requirements defined; evidence retained."""

    def test_competence_requirements_defined(self, controls_evidence: dict):
        competence = controls_evidence.get("iso9001_competence", {})
        assert competence.get("requirements_defined_for_quality_roles", False), (
            "Competence requirements must be defined for persons whose work affects quality "
            "performance (ISO 9001 §7.2(a))"
        )

    def test_competence_evidence_retained(self, controls_evidence: dict):
        personnel = controls_evidence.get("iso9001_quality_personnel", [])
        missing_evidence = [
            p for p in personnel
            if not p.get("competence_evidence_retained", False)
        ]
        assert not missing_evidence, (
            f"Evidence of competence must be retained for quality personnel. "
            f"Missing: {[p['person_id'] for p in missing_evidence]}"
        )
```

---

## Clause 7.5 — Documented Information

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Documented information required by ISO 9001 and determined necessary by the organization | DETERMINISTIC |
| Condition | QMS in scope | DETERMINISTIC |
| Obligation | Documents controlled (approval, review, current version); records legible, identifiable, retrievable; retention period defined | DETERMINISTIC |
| Evidence | Document control procedure; document register; record retention schedule | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause7_5_DocumentedInformation:
    """Clause 7.5 — Documented information: document control and record management."""

    def test_document_control_procedure_exists(self, controls_evidence: dict):
        di = controls_evidence.get("iso9001_documented_information", {})
        assert di.get("document_control_procedure_exists", False), (
            "Document control procedure must exist (ISO 9001 §7.5.2)"
        )

    def test_records_retention_period_defined(self, controls_evidence: dict):
        di = controls_evidence.get("iso9001_documented_information", {})
        assert di.get("retention_periods_defined", False), (
            "Retention periods must be defined for all required QMS records (ISO 9001 §7.5.3.2(g))"
        )

    def test_quality_policy_documented(self, controls_evidence: dict):
        di = controls_evidence.get("iso9001_documented_information", {})
        assert di.get("quality_policy_documented", False), (
            "Quality policy must be maintained as documented information (ISO 9001 §5.2.2)"
        )

    def test_qms_scope_documented(self, controls_evidence: dict):
        di = controls_evidence.get("iso9001_documented_information", {})
        assert di.get("qms_scope_documented", False), (
            "QMS scope must be available as documented information (ISO 9001 §4.3)"
        )
```

---

## Clause 8.6 — Release of Products and Services

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Products and services ready for release to customer | DETERMINISTIC |
| Condition | Planned arrangements for product/service release completed | DETERMINISTIC |
| Obligation | Evidence of conformity with acceptance criteria retained; records identify person authorizing release | DETERMINISTIC |
| Evidence | Release records with: product/service identifier, acceptance criteria met, date, authorizing person identity | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause8_6_Release:
    """Clause 8.6 — Release: conformity evidence and authorization records."""

    def test_release_records_retained(self, controls_evidence: dict):
        release = controls_evidence.get("iso9001_release_records", {})
        assert release.get("records_retained", False), (
            "Records of product/service release must be retained including evidence of conformity "
            "with acceptance criteria (ISO 9001 §8.6)"
        )

    def test_release_records_include_authorizing_person(self, controls_evidence: dict):
        recent_releases = controls_evidence.get("iso9001_recent_releases", [])
        missing_auth = [
            r for r in recent_releases
            if not r.get("authorizing_person_identified", False)
        ]
        assert not missing_auth, (
            f"Release records must identify the person authorizing release. "
            f"Missing authorization identity: {[r['release_id'] for r in missing_auth]}"
        )

    def test_no_unauthorized_releases(self, controls_evidence: dict):
        recent_releases = controls_evidence.get("iso9001_recent_releases", [])
        unauthorized = [
            r for r in recent_releases
            if not r.get("acceptance_criteria_met", False)
            and not r.get("concession_authorized", False)
        ]
        assert not unauthorized, (
            f"Products/services must not be released unless acceptance criteria are met "
            f"(or concession authorized). Unauthorized releases: {[r['release_id'] for r in unauthorized]}"
        )
```

---

## Clause 8.7 — Control of Nonconforming Outputs

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Outputs (products/services) that do not conform to requirements | DETERMINISTIC |
| Condition | Nonconformity detected during production or service provision | DETERMINISTIC |
| Obligation | Nonconforming outputs identified; controlled to prevent unintended use or delivery; corrective action; records of disposition retained | DETERMINISTIC |
| Evidence | Nonconformance reports (NCRs); disposition records; corrective action reference; re-inspection records where applicable | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause8_7_NonconformingOutputs:
    """Clause 8.7 — Control of nonconforming outputs: identification, control, records."""

    def test_nonconforming_output_procedure_exists(self, controls_evidence: dict):
        nc = controls_evidence.get("iso9001_nonconforming_output_control", {})
        assert nc.get("procedure_exists", False), (
            "Procedure for controlling nonconforming outputs must exist (ISO 9001 §8.7)"
        )

    def test_nonconformance_records_retained(self, controls_evidence: dict):
        nc = controls_evidence.get("iso9001_nonconforming_output_control", {})
        assert nc.get("ncr_records_retained", False), (
            "Records describing the nonconformity, actions taken, concessions, and authorizing "
            "person must be retained (ISO 9001 §8.7.2)"
        )

    def test_no_nonconforming_outputs_released_without_authorization(
        self, controls_evidence: dict
    ):
        ncrs = controls_evidence.get("iso9001_nonconformance_reports", [])
        released_without_concession = [
            r for r in ncrs
            if r.get("disposition") == "released"
            and not r.get("concession_authorized", False)
        ]
        assert not released_without_concession, (
            f"Nonconforming outputs must not be released without authorized concession. "
            f"Unauthorized releases: {[r['ncr_id'] for r in released_without_concession]}"
        )

    def test_nonconforming_output_disposition_documented(self, controls_evidence: dict):
        ncrs = controls_evidence.get("iso9001_nonconformance_reports", [])
        no_disposition = [
            r for r in ncrs
            if not r.get("disposition_documented", False)
        ]
        assert not no_disposition, (
            f"Disposition must be documented for all nonconforming outputs. "
            f"Missing disposition: {[r['ncr_id'] for r in no_disposition]}"
        )
```

---

## Clause 9.2 — Internal Audit

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | QMS internal audit program | DETERMINISTIC |
| Condition | QMS in scope | DETERMINISTIC |
| Obligation | Audit program planned considering importance of processes and results of previous audits; audit criteria and scope defined; auditors selected to ensure objectivity; results reported to relevant management; records retained | DETERMINISTIC |
| Evidence | Audit program; individual audit reports; corrective action records; evidence of auditor independence | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause9_2_InternalAudit:
    """Clause 9.2 — Internal audit: planned program, records, independence."""

    def test_audit_program_exists(self, controls_evidence: dict):
        audit = controls_evidence.get("iso9001_internal_audit", {})
        assert audit.get("program_documented", False), (
            "Internal audit program must be documented (ISO 9001 §9.2.2(a))"
        )

    def test_audit_conducted_within_interval(
        self, controls_evidence: dict, reference_date: date
    ):
        audit = controls_evidence.get("iso9001_internal_audit", {})
        last_audit = audit.get("last_audit_completion_date")
        assert last_audit is not None, (
            "Last internal audit completion date must be recorded"
        )
        cutoff = reference_date - timedelta(days=ISO9001_INTERNAL_AUDIT_MAX_MONTHS * 30)
        assert last_audit >= cutoff, (
            f"Internal audit must be conducted at planned intervals (≤{ISO9001_INTERNAL_AUDIT_MAX_MONTHS} "
            f"months). Last audit: {last_audit}; cutoff: {cutoff}"
        )

    def test_audit_results_documented(self, controls_evidence: dict):
        audit = controls_evidence.get("iso9001_internal_audit", {})
        assert audit.get("audit_results_documented", False), (
            "Audit results must be retained as documented information (ISO 9001 §9.2.2(f))"
        )

    def test_auditor_independence_maintained(self, controls_evidence: dict):
        audit = controls_evidence.get("iso9001_internal_audit", {})
        assert audit.get("auditor_independence_documented", False), (
            "Auditors must not audit their own work — independence must be ensured "
            "(ISO 9001 §9.2.2(d))"
        )
```

---

## Clause 9.3 — Management Review

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Top management review of the QMS | DETERMINISTIC |
| Condition | QMS in scope | DETERMINISTIC |
| Obligation | Planned management reviews at defined intervals; specified inputs reviewed; outputs include decisions on improvement actions, resource needs, QMS changes; records retained | DETERMINISTIC |
| Evidence | Management review meeting records; attendees; inputs addressed; decisions and action items | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause9_3_ManagementReview:
    """Clause 9.3 — Management review: planned, documented, with defined inputs/outputs."""

    def test_management_review_conducted_within_interval(
        self, controls_evidence: dict, reference_date: date
    ):
        mgmt_review = controls_evidence.get("iso9001_management_review", {})
        last_review = mgmt_review.get("last_review_date")
        assert last_review is not None, "Last management review date must be recorded"
        cutoff = reference_date - timedelta(days=ISO9001_MANAGEMENT_REVIEW_MAX_MONTHS * 30)
        assert last_review >= cutoff, (
            f"Management review must occur at planned intervals "
            f"(≤{ISO9001_MANAGEMENT_REVIEW_MAX_MONTHS} months). "
            f"Last review: {last_review}; cutoff: {cutoff}"
        )

    def test_management_review_records_retained(self, controls_evidence: dict):
        mgmt_review = controls_evidence.get("iso9001_management_review", {})
        assert mgmt_review.get("records_retained", False), (
            "Management review results must be retained as documented information "
            "(ISO 9001 §9.3.3)"
        )

    def test_management_review_outputs_include_improvement_decisions(
        self, controls_evidence: dict
    ):
        mgmt_review = controls_evidence.get("iso9001_management_review", {})
        assert mgmt_review.get("improvement_decisions_documented", False), (
            "Management review outputs must include any decisions and actions related to "
            "improvement opportunities (ISO 9001 §9.3.3(b))"
        )
```

---

## Clause 10.2 — Nonconformity and Corrective Action

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Nonconformities discovered in the QMS or product/service | DETERMINISTIC |
| Condition | Nonconformity occurs | DETERMINISTIC |
| Obligation | Nonconformity reacted to (correction + consequences); root cause determined; corrective action implemented; effectiveness reviewed; QMS updated if necessary; records retained | DETERMINISTIC |
| Evidence | Corrective action records with: nonconformity description, action taken, root cause, effectiveness evaluation, closure date | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause10_2_CorrectiveAction:
    """Clause 10.2 — Nonconformity and corrective action: records retained; root cause documented."""

    def test_corrective_action_records_retained(self, controls_evidence: dict):
        capa = controls_evidence.get("iso9001_corrective_actions", {})
        assert capa.get("records_retained", False), (
            "Records of nonconformities and corrective actions must be retained "
            "(ISO 9001 §10.2.2)"
        )

    def test_open_nonconformities_have_root_cause(self, controls_evidence: dict):
        ncrs = controls_evidence.get("iso9001_open_nonconformities", [])
        no_root_cause = [
            n for n in ncrs
            if not n.get("root_cause_documented", False)
            and not n.get("root_cause_in_progress", False)
        ]
        assert not no_root_cause, (
            f"Root cause must be documented for all nonconformities. "
            f"Missing root cause: {[n['ncr_id'] for n in no_root_cause]}"
        )

    def test_closed_corrective_actions_have_effectiveness_review(
        self, controls_evidence: dict
    ):
        closed_cas = controls_evidence.get("iso9001_closed_corrective_actions", [])
        no_effectiveness = [
            c for c in closed_cas
            if not c.get("effectiveness_reviewed", False)
        ]
        assert not no_effectiveness, (
            f"Effectiveness of corrective actions must be reviewed before closure "
            "(ISO 9001 §10.2.1(f)). Missing effectiveness review: "
            f"{[c['ca_id'] for c in no_effectiveness]}"
        )
```

---

## Clause 8.5.6 — Control of Changes (Production/Service Provision)

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Changes to production and service provision processes | DETERMINISTIC |
| Condition | Change to a process supporting product/service production | DETERMINISTIC |
| Obligation | Changes reviewed; necessary actions taken to maintain conformity; records of change review and authorization retained | DETERMINISTIC |
| Evidence | Engineering change records; change authorization records; revision history | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestClause8_5_6_ChangeControl:
    """Clause 8.5.6 — Control of changes to production/service provision."""

    def test_change_control_records_retained(self, controls_evidence: dict):
        changes = controls_evidence.get("iso9001_process_changes", {})
        assert changes.get("records_retained", False), (
            "Records of changes to production/service provision processes must be retained "
            "(ISO 9001 §8.5.6)"
        )

    def test_production_changes_reviewed_before_implementation(
        self, controls_evidence: dict
    ):
        recent_changes = controls_evidence.get("iso9001_recent_process_changes", [])
        not_reviewed = [
            c for c in recent_changes
            if not c.get("reviewed_before_implementation", False)
        ]
        assert not not_reviewed, (
            f"Changes to production/service provision must be reviewed before implementation. "
            f"Not reviewed: {[c['change_id'] for c in not_reviewed]}"
        )
```

---

## Open assumptions

*(No assumptions recorded for this file — all requirements are DETERMINISTIC record existence checks)*

---

## Cross-standard notes

**ISO 13485 §8.3/8.5:** ISO 13485 adds more prescriptive requirements on top of the 8.7/10.2 baseline — complaint handling, regulatory reporting determination, CAPA formalization with effectiveness trending. The record structure is the same; 13485 requires more fields.

**IATF 16949:** Adds automotive-specific NC handling including customer notification timelines and containment actions (D0-D3 of 8D methodology). The 9001 §8.7/10.2 record is the foundation.

**AS9100:** Adds First Article Inspection (FAI) records as a type of release record (8.6 extension).
