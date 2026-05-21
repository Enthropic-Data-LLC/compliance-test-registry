# ISO/IEC 27001:2022 — Clauses 4–10 (ISMS Mandatory Requirements)

**Registry path:** `/regulation-registry/ISO-27001/Clauses/`
**Version:** ISO/IEC 27001:2022
**Last parsed:** 2026-05-20
**Overall confidence:** MEDIUM — audit and management review cadences are DETERMINISTIC; risk treatment, SoA content, and most process requirements are PARAMETERIZED or CONTESTED
**R = Required (all mandatory clause requirements are non-negotiable for certification)**

---

## Scope summary

Clauses 4–10 are the mandatory framework requirements — every organization seeking ISO/IEC 27001:2022 certification must satisfy all of them. Unlike Annex A (which allows control exclusion via the SoA), mandatory clause requirements cannot be excluded. The dominant mode is PARAMETERIZED because ISO 27001 is a management system standard: it specifies what must be done but almost never specifies how. The certification auditor evaluates whether the organization's approach is fit for purpose given its specific context.

Two DETERMINISTIC thresholds exist: internal audit must be performed (Clause 9.2) and management review must be performed (Clause 9.3) — both at "planned intervals." Annual minimum is the auditor consensus; more frequent is expected for complex organizations.

---

## Clause 4 — Context of the Organization (PARAMETERIZED)

### Source summary

> Determine external and internal issues relevant to the ISMS purpose. Identify interested parties and their requirements. Define ISMS scope. Document the ISMS.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | Organization | DETERMINISTIC |
| Obligation | Context documented; interested parties identified with requirements; ISMS scope defined and documented | PARAMETERIZED |
| Evidence | `isms_documentation.context_analysis_exists == true`; `isms_scope_statement`; `interested_parties_register` | PARAMETERIZED |

**Assumption (ASSUME-ISO-001):** Context analysis is adequate when: (1) external issues list covers legal/regulatory environment, industry threats, market context, and technology landscape; (2) internal issues list covers organizational culture, governance structures, and existing security capabilities; (3) interested parties register includes at minimum: customers, regulators, employees, suppliers, certification body, and board/management; (4) each interested party's relevant requirements are documented; (5) ISMS scope statement specifies included/excluded business units, locations, and asset types with documented rationale for any exclusions.

**Overall: PARAMETERIZED → Pattern 2**

---

## Clause 5 — Leadership (PARAMETERIZED)

### Source summary

> Top management must demonstrate commitment, establish IS policy, assign roles, and ensure integration with business processes.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | Top management | DETERMINISTIC |
| Obligation | IS policy documented, reviewed annually, communicated to all staff; roles and responsibilities assigned; management demonstrates commitment | PARAMETERIZED |
| Evidence | `is_policy.last_reviewed_date` ≤ 365 days; `role_assignments.ciso_or_equivalent`; management review records | PARAMETERIZED |

**Assumption (ASSUME-ISO-002):** IS policy is adequate when it: (1) is approved by top management; (2) states objectives and principles; (3) includes commitment to satisfying applicable IS requirements and to continual improvement; (4) is reviewed and updated at least annually; (5) is communicated to all workers and made available to interested parties as appropriate.

**Overall: PARAMETERIZED → Pattern 2**

---

## Clause 6 — Planning (CONTESTED for risk treatment; DETERMINISTIC for SoA)

### Source summary

> Perform risk assessment with documented methodology. Apply risk treatment. Produce Statement of Applicability. Define IS objectives.

### 6.1.2 — Risk Assessment (CONTESTED)

| Element | Value | Classification |
|---|---|---|
| Obligation | Risk assessment methodology defined and consistently applied; identifies risks to CIA of information assets; produces risk evaluation against defined criteria | CONTESTED |
| Evidence | `risk_assessment_methodology.documented == true`; `risk_register` with identified risks, likelihood/impact, risk owners | CONTESTED |

> **CONTESTED reason:** ISO 27001 does not specify a risk assessment methodology — NIST SP 800-30, ISO 27005, OCTAVE, FAIR, and custom matrices are all acceptable. The auditor evaluates whether the chosen methodology is appropriate and consistently applied, not whether it matches a defined standard. The adequacy of the risk acceptance criteria and the completeness of the asset/threat/vulnerability identification are judgment calls.

### 6.1.3d — Statement of Applicability (R — DETERMINISTIC)

| Element | Value | Classification |
|---|---|---|
| Obligation | SoA documented; addresses all 93 Annex A controls; includes inclusion/exclusion justification and implementation status | DETERMINISTIC |
| Evidence | `soa.total_controls_addressed == 93`; each control has `included == true/false`; exclusions have `justification`; inclusions have `implementation_status` | DETERMINISTIC |

**Overall for Clause 6: CONTESTED for risk treatment → Pattern 3; DETERMINISTIC for SoA control count → Pattern 1**

---

## Clause 7 — Support (PARAMETERIZED)

### Source summary

> Ensure resources, competence, awareness, communication, and documented information for ISMS operation.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All personnel with IS responsibilities | DETERMINISTIC |
| Obligation | Competence determined and evidenced; IS awareness program for all workers; documented information controlled and retained | PARAMETERIZED |
| Evidence | `competence_records.employee_id`; `awareness_training.training_date`; `document_control.version_history` | PARAMETERIZED |

**Assumption (ASSUME-ISO-003):** IS awareness is adequate when all workers (not just IT/security) receive annual IS awareness training covering: applicable IS policies, their role in maintaining IS, consequences of noncompliance, phishing and social engineering recognition, and incident reporting procedures. Frequency: at minimum annually and upon significant threat landscape changes.

**Overall: PARAMETERIZED → Pattern 2**

---

## Clause 8 — Operation (PARAMETERIZED)

### Source summary

> Implement risk treatment plans. Control operational processes. Manage changes. Control outsourced processes.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All ISMS operational processes | DETERMINISTIC |
| Obligation | Risk treatment plans implemented; operational controls in place; changes controlled; outsourced processes managed | PARAMETERIZED |
| Evidence | `risk_treatment_plan.controls_implemented == true`; `change_records`; `outsourcing_agreements.security_requirements_included` | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## Clause 9 — Performance Evaluation (MEDIUM — cadence DETERMINISTIC; content PARAMETERIZED)

### Source summary

> Monitor and measure ISMS performance. Conduct internal audits at planned intervals. Conduct management review at planned intervals.

### 9.2 — Internal Audit (R — DETERMINISTIC for cadence; PARAMETERIZED for scope)

| Element | Value | Classification |
|---|---|---|
| Obligation | Internal audit programme defined; audits performed at planned intervals; audit results reported to management | DETERMINISTIC (interval) / PARAMETERIZED (scope) |
| Evidence | `internal_audit_programme.exists == true`; `audit_records.most_recent_date`; `audit_scope` covers ISMS clauses and Annex A controls | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-004):** Internal audit cadence is adequate when: (1) full ISMS scope is audited at least annually; (2) higher-risk areas are audited more frequently or with greater depth; (3) auditors are competent and independent of the area being audited; (4) nonconformities from audits are formally tracked and corrected.

### 9.3 — Management Review (R — DETERMINISTIC for existence; PARAMETERIZED for content)

| Element | Value | Classification |
|---|---|---|
| Obligation | Management review performed at planned intervals; covers: changes in context, previous review actions, ISMS performance metrics, audit results, risk treatment status, opportunities for improvement | DETERMINISTIC (existence) / PARAMETERIZED (content) |
| Evidence | `management_review_records.most_recent_date` ≤ 365 days; agenda covers all required topics; action items recorded | DETERMINISTIC + PARAMETERIZED |

**Overall for Clause 9: DETERMINISTIC for audit/review existence → Pattern 1; PARAMETERIZED for scope/content → Pattern 2**

---

## Clause 10 — Improvement (PARAMETERIZED)

### Source summary

> Address nonconformities with corrective action. Continually improve ISMS.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Nonconformities documented; root cause analysis performed; corrective actions implemented and verified; ISMS continually improved | PARAMETERIZED |
| Evidence | `nonconformity_log.exists == true`; `corrective_action_records.root_cause_documented`; `corrective_action_records.verified_effective` | PARAMETERIZED |

**Assumption (ASSUME-ISO-005):** Corrective action is adequate when: (1) nonconformity documented with description and date; (2) root cause analysis performed (5-Whys, fishbone, or equivalent); (3) corrective action plan documented with owner and due date; (4) effectiveness of corrective action verified within an agreed timeframe; (5) lessons learned communicated to affected areas.

**Overall: PARAMETERIZED → Pattern 2**

---

## YAML specifications

### `clause9_audit.yaml`

```yaml
regulation_id: ISO-27001-2022-9.2
section: "ISO 27001:2022 — Internal Audit"
r_or_a: Required
source_text: >
  The organization shall conduct internal audits at planned intervals to
  provide information on whether the ISMS conforms to requirements and
  is effectively implemented and maintained.

extracted_elements:
  subject: "ISMS scope"
  condition: "At planned intervals (annual minimum per auditor consensus)"
  obligation: "Internal audit conducted; scope covers full ISMS; results reported; NCs tracked"
  evidence: "internal_audit_records: most_recent_date, scope, nonconformities_raised"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: PARAMETERIZED
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-ISO-004
    assumption_text: >
      Annual audit cadence for full ISMS scope; higher-risk areas more frequent;
      auditors competent and independent; NCs formally tracked and corrected.
    assumed_by: "ISMS Manager"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
    cryptographic_hash: "sha256:pending-ci"
test_confidence: HIGH
generated_test: "tests/iso27001/test_clause9_performance.py"
```

---

## Generated tests

### `tests/iso27001/test_clause6_planning.py`

```python
"""
ISO 27001:2022 Clause 6 — Planning
Confidence: MEDIUM for SoA; CONTESTED for risk treatment
"""
import pytest

REQUIRED_ANNEX_A_CONTROL_COUNT = 93


@pytest.mark.human_review_required(
    reason=(
        "Risk assessment methodology adequacy is auditor-evaluated. "
        "Test confirms documentation exists and risk register is populated; "
        "methodology adequacy requires auditor/ISMS manager review."
    )
)
def test_risk_assessment_documented(risk_assessment_records):
    assert risk_assessment_records, (
        "NONCONFORMITY (6.1.2): No risk assessment records found — risk assessment "
        "is mandatory for ISO 27001 certification"
    )
    assert any(r.get("methodology_documented") for r in risk_assessment_records), (
        "NONCONFORMITY (6.1.2): No risk assessment record has documented methodology — "
        "consistent, documented methodology is required"
    )


def test_risk_register_populated(risk_register_entries):
    assert risk_register_entries, (
        "NONCONFORMITY (6.1.2): Risk register is empty — identified risks required"
    )
    no_owner = [r for r in risk_register_entries if not r.get("risk_owner")]
    assert not no_owner, (
        f"NONCONFORMITY (6.1.2): {len(no_owner)} risk(s) without assigned risk owner"
    )


def test_soa_addresses_all_93_controls(soa_records):
    """6.1.3d — SoA must address all 93 Annex A controls."""
    assert soa_records, (
        "NONCONFORMITY (6.1.3d): No Statement of Applicability found — SoA is mandatory"
    )
    soa = soa_records[0]  # most recent
    control_count = soa.get("total_controls_addressed", 0)
    assert control_count >= REQUIRED_ANNEX_A_CONTROL_COUNT, (
        f"NONCONFORMITY (6.1.3d): SoA addresses {control_count} controls; "
        f"all {REQUIRED_ANNEX_A_CONTROL_COUNT} must be addressed"
    )


def test_soa_exclusions_have_justification(soa_control_entries):
    violations = [
        e for e in soa_control_entries
        if not e.get("included")
        and not e.get("exclusion_justification")
    ]
    assert not violations, (
        f"NONCONFORMITY (6.1.3d): {len(violations)} excluded control(s) without "
        f"justification: {[e['control_id'] for e in violations]}"
    )
```

### `tests/iso27001/test_clause9_performance.py`

```python
"""
ISO 27001:2022 Clause 9 — Performance Evaluation
Confidence: HIGH for existence; MEDIUM for scope adequacy
"""
import pytest
from datetime import date

AUDIT_MAX_INTERVAL_DAYS = 365
MGMT_REVIEW_MAX_INTERVAL_DAYS = 365


@pytest.mark.assumption(
    id="ASSUME-ISO-004",
    description="Annual audit cadence minimum; full ISMS scope; auditors independent",
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_internal_audit_within_12_months(internal_audit_records):
    """9.2 — Internal audit performed at planned intervals (annual minimum)."""
    today = date.today()
    if not internal_audit_records:
        assert False, (
            "NONCONFORMITY (9.2): No internal audit records found"
        )
    latest = max(internal_audit_records, key=lambda r: r["audit_date"])
    days_since = (today - latest["audit_date"]).days
    assert days_since <= AUDIT_MAX_INTERVAL_DAYS, (
        f"NONCONFORMITY (9.2): Last internal audit was {days_since} days ago "
        f"(max {AUDIT_MAX_INTERVAL_DAYS})"
    )


def test_management_review_within_12_months(management_review_records):
    """9.3 — Management review performed at planned intervals (annual minimum)."""
    today = date.today()
    if not management_review_records:
        assert False, (
            "NONCONFORMITY (9.3): No management review records found"
        )
    latest = max(management_review_records, key=lambda r: r["review_date"])
    days_since = (today - latest["review_date"]).days
    assert days_since <= MGMT_REVIEW_MAX_INTERVAL_DAYS, (
        f"NONCONFORMITY (9.3): Last management review was {days_since} days ago "
        f"(max {MGMT_REVIEW_MAX_INTERVAL_DAYS})"
    )


def test_nonconformities_have_corrective_action(nonconformity_records):
    """10.1 — All nonconformities must have documented corrective action."""
    open_without_action = [
        nc for nc in nonconformity_records
        if not nc.get("corrective_action_documented")
        and not nc.get("accepted_risk_rationale")
    ]
    assert not open_without_action, (
        f"NONCONFORMITY (10.1): {len(open_without_action)} nonconformity/ies without "
        f"corrective action or accepted-risk rationale: "
        f"{[nc.get('nc_id') for nc in open_without_action]}"
    )
```

---

## Notes for the registry

- **SoA is the certification pivot point:** The SoA is the single most important document in the ISO 27001 certification process. All 93 controls must be addressed; exclusions need justification tied to the risk assessment results. A poorly documented SoA is a major nonconformity (Stage 2 audit blocker).
- **Risk methodology consistency matters more than methodology choice:** Auditors do not prescribe a methodology but evaluate whether the chosen methodology is: (1) repeatable — same methodology applied each time; (2) comparable — enables comparison of risks across the organization; (3) complete — covers the full ISMS scope. Inconsistent or ad-hoc risk assessment is a major nonconformity.
- **"Planned intervals" for audit and review:** ISO 27001 does not state a specific frequency for internal audit or management review. Annually is the universal auditor expectation for organizations seeking certification. High-risk environments or organizations with significant changes should review more frequently.
- **Clause 6 vs. Annex A distinction:** Clauses 4–10 define the management system requirements. Annex A defines the security controls. You need both — a well-run ISMS (clauses) with inadequate controls (Annex A) or vice versa will not achieve or maintain certification.
- **Transition from 2013 to 2022:** The transition deadline was October 31, 2025. All new certifications and surveillance audits should now be against the 2022 edition. The 11 new controls added in 2022 (A.5.7, A.5.23, A.5.30, A.6.7, A.7.4, A.8.9, A.8.10, A.8.11, A.8.12, A.8.16, A.8.23, A.8.28) must be addressed in the SoA.
