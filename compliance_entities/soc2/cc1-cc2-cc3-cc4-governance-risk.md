# SOC 2 TSC 2017 — CC1–CC4: Control Environment, Communication, Risk Assessment, and Monitoring

**Registry path:** `/regulation-registry/SOC2/CC1-CC4/`
**Version:** AICPA TSC 2017 (2022 points of focus updates)
**Last parsed:** 2026-05-20
**Applies to:** Service organizations (SaaS, cloud providers, data centers, managed-service providers) whose services are relevant to user-entity controls
**Trigger:** Customer contract requirement; investor due-diligence; voluntary for competitive positioning; required when customers request a SOC 2 Type I or Type II report from their auditor
**Jurisdiction:** United States (AICPA Trust Services Criteria); widely accepted internationally as equivalent to ISO 27001 attestation
**Not applicable to:** Internal IT departments; organizations that do not provide services to other companies; product companies without a service component
**Overall confidence:** LOW–MEDIUM — CC1 (control environment) is predominantly CONTESTED; CC2 is PARAMETERIZED; CC3.2–CC3.3 (risk assessment and fraud) are CONTESTED; CC4 is PARAMETERIZED
**14 criteria total: CC1.1–CC1.5, CC2.1–CC2.3, CC3.1–CC3.4, CC4.1–CC4.2**

---

## Scope summary

CC1–CC4 map to the COSO Internal Control–Integrated Framework (2013): Control Environment (CC1), Information and Communication (CC2), Risk Assessment (CC3), and Monitoring Activities (CC4). These series are the most challenging to automate because they address governance, culture, and management judgment — all of which require human assessment.

The dominant pattern across CC1–CC4 is Pattern 3 (human review surfacing). Only CC2.3 (system description accuracy), CC3.1 (objective specification), and CC4.2 (deficiency communication) have partial DETERMINISTIC elements with assumptions.

---

## CC1 — Control Environment (CONTESTED)

### CC1.1 — Board Oversight

| Element | Value | Classification |
|---|---|---|
| Obligation | Board of directors (or equivalent) demonstrates oversight of security | CONTESTED |
| Evidence | Board meeting minutes referencing IS oversight; board-level security reporting | CONTESTED |

> **CONTESTED reason:** Board competency determination and the adequacy of governance structure are auditor-evaluated. No measurable threshold exists for "independence" or "oversight effectiveness."

**Overall: CONTESTED → Pattern 3**

---

### CC1.2 — Ethical Values and Independence

| Element | Value | Classification |
|---|---|---|
| Obligation | Ethical values established and communicated; code of conduct exists; independence enforced for oversight roles | CONTESTED |
| Evidence | Code of conduct signed by all personnel; whistleblower mechanism; conflict of interest disclosures | DETERMINISTIC (existence) / CONTESTED (adequacy) |

**Assumption (ASSUME-SOC2-CC1-001):** Code of conduct controls are adequate when: (1) code of conduct documented and available to all personnel; (2) all personnel sign or acknowledge the code of conduct on hire and annually; (3) disciplinary process for code of conduct violations documented; (4) conflict of interest disclosure process documented; (5) anonymous reporting channel (whistleblower line) available.

**Overall: DETERMINISTIC for code of conduct existence → Pattern 1; CONTESTED for governance independence → Pattern 3**

---

### CC1.3 — Management Structure and Accountability

| Element | Value | Classification |
|---|---|---|
| Obligation | Organizational structure documented; reporting lines established; security roles and responsibilities defined | PARAMETERIZED |
| Evidence | `org_chart.security_roles_defined == true`; CISO or equivalent formally designated | PARAMETERIZED + DETERMINISTIC (existence) |

**Assumption (ASSUME-SOC2-CC1-002):** Management structure is adequate when: (1) organizational chart documents reporting lines for security function; (2) CISO or equivalent with security responsibility formally designated; (3) security responsibilities defined for all roles with ISMS impact; (4) security function reports to a level of management appropriate to the size and risk profile of the organization.

**Overall: PARAMETERIZED → Pattern 2; CISO designation → Pattern 1**

---

### CC1.4 — Competence and Development

| Element | Value | Classification |
|---|---|---|
| Obligation | Competence requirements defined for security roles; training program in place; performance evaluations include security responsibilities | PARAMETERIZED |
| Evidence | `role_competency_requirements.documented == true`; `training_records.security_role_training == true` | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

### CC1.5 — Accountability

| Element | Value | Classification |
|---|---|---|
| Obligation | Personnel held accountable for security responsibilities; performance evaluations include security metrics; disciplinary process for security violations | PARAMETERIZED |
| Evidence | `performance_review_records.security_objectives_included == true`; disciplinary records for IS violations | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## CC2 — Communication and Information

### CC2.1 — Information Quality

| Element | Value | Classification |
|---|---|---|
| Obligation | High-quality, relevant information available for decision-making; information flows support control activities | PARAMETERIZED |
| Evidence | `information_quality_processes.documented == true` | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

### CC2.2 — Internal Communication

| Element | Value | Classification |
|---|---|---|
| Obligation | Internal communication supports achievement of objectives; security information communicated to relevant parties | PARAMETERIZED |
| Evidence | `internal_communication_records.security_updates_distributed == true` | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

### CC2.3 — External Communication and System Description (MEDIUM)

| Element | Value | Classification |
|---|---|---|
| Obligation | System description accurately describes the service; system description reflects current state; system boundaries documented | DETERMINISTIC (existence) / PARAMETERIZED (accuracy) |
| Evidence | `system_description.last_reviewed_date` ≤ 365 days; `system_description.boundary_documented == true`; system description reviewed before each audit period | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-SOC2-CC2-001):** System description is accurate when: (1) infrastructure components are accurately listed (no significant components omitted); (2) service commitments and system requirements match what is actually committed in customer agreements; (3) subservice organizations are identified; (4) complementary user entity controls (CUECs) documented and reasonable; (5) reviewed and updated at least annually or when material changes occur.

**Overall: DETERMINISTIC for system description existence and review date → Pattern 1; PARAMETERIZED for accuracy → Pattern 2**

---

## CC3 — Risk Assessment

### CC3.1 — Objective Specification (PARAMETERIZED)

| Element | Value | Classification |
|---|---|---|
| Obligation | Security objectives specified; objectives are specific and measurable; objectives linked to the SOC 2 trust service commitments | PARAMETERIZED |
| Evidence | `security_objectives.documented == true`; objectives linked to trust service criteria | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

### CC3.2 — Risk Identification and Analysis (CONTESTED)

| Element | Value | Classification |
|---|---|---|
| Obligation | Risks identified and analyzed; risk assessment methodology documented; risks evaluated against criteria | CONTESTED |
| Evidence | `risk_assessment_records.exists == true`; `risk_register.populated == true`; methodology documented | CONTESTED |

> **CONTESTED reason:** Risk assessment methodology adequacy and risk completeness are auditor-evaluated judgments. No objective threshold defines "sufficient" risk identification. Pattern 3 test surfaces the assessment for human review.

**Overall: CONTESTED → Pattern 3**

---

### CC3.3 — Fraud Risk (CONTESTED)

| Element | Value | Classification |
|---|---|---|
| Obligation | Fraud risk considered in risk assessment; fraud scenarios appropriate to the entity's operations identified | CONTESTED |
| Evidence | `fraud_risk_assessment.completed == true`; fraud scenarios documented | CONTESTED |

> **CONTESTED reason:** The adequacy of fraud scenario identification depends on the nature of the service organization's business and auditor judgment.

**Overall: CONTESTED → Pattern 3**

---

### CC3.4 — Change Risk Identification (PARAMETERIZED)

| Element | Value | Classification |
|---|---|---|
| Obligation | Changes in business environment, technology, or regulatory requirements trigger re-assessment of affected risks | PARAMETERIZED |
| Evidence | `risk_reassessment_triggers.documented == true`; change events linked to risk reassessments | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## CC4 — Monitoring Activities

### CC4.1 — Ongoing and Separate Evaluations (PARAMETERIZED)

| Element | Value | Classification |
|---|---|---|
| Obligation | Ongoing monitoring of controls; separate evaluations (internal audit, management review) performed; results used to improve controls | PARAMETERIZED |
| Evidence | `monitoring_activities.ongoing_controls_reviewed == true`; internal audit records; management review records | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

### CC4.2 — Communication of Deficiencies (MEDIUM)

| Element | Value | Classification |
|---|---|---|
| Obligation | Control deficiencies identified and communicated to responsible parties; significant deficiencies escalated to appropriate management level | DETERMINISTIC (escalation exists) / PARAMETERIZED (timeliness) |
| Evidence | `deficiency_log.exists == true`; deficiencies communicated to process owners; significant deficiencies documented as escalated to management | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-SOC2-CC4-001):** Deficiency communication is adequate when: (1) control deficiencies (identified from monitoring, audit, or incident review) are logged with owner and due date; (2) significant deficiencies communicated to senior management within 30 days of identification; (3) material weaknesses communicated to the board or equivalent within 60 days; (4) management response to deficiencies documented; (5) remediation tracked to closure.

**Overall: PARAMETERIZED → Pattern 2; deficiency log existence → Pattern 1**

---

## YAML specifications

### `cc1_cc4_governance.yaml`

```yaml
regulation_id: SOC2-TSC2017-CC1-CC4
section: "SOC 2 TSC 2017 — CC1–CC4: Governance, Communication, Risk, Monitoring"
r_or_a: Required
source_text: >
  Entity implements COSO-aligned controls: control environment (CC1), communication (CC2),
  risk assessment (CC3), and monitoring activities (CC4).

extracted_elements:
  subject: "Entity governance, risk management, and monitoring processes"
  condition: "Ongoing; annual review cycles"
  obligation: >
    Code of conduct documented and acknowledged; system description current; risk register
    populated; deficiencies logged and escalated; CISO designated.
  evidence: >
    code_of_conduct_acknowledgments, system_description, risk_register,
    deficiency_log, org_chart

ambiguity_classification:
  subject: PARAMETERIZED
  condition: PARAMETERIZED
  obligation: CONTESTED
  evidence: PARAMETERIZED

overall_classification: PARAMETERIZED
human_review_required: true
test_confidence: MEDIUM
generated_test: "tests/soc2/test_cc1_cc4_governance.py"
```

---

## Generated tests

### `tests/soc2/test_cc1_cc4_governance.py`

```python
"""
SOC 2 TSC 2017 — CC1–CC4: Control Environment, Communication, Risk, Monitoring
Confidence: MEDIUM for existence checks; CONTESTED for adequacy
Human review required for CC1.1, CC3.2, CC3.3
"""
import pytest
from datetime import date

SYSTEM_DESCRIPTION_MAX_AGE_DAYS = 365
DEFICIENCY_ESCALATION_MAX_DAYS = 30


@pytest.mark.assumption(
    id="ASSUME-SOC2-CC1-001",
    description="Code of conduct: documented; signed annually by all staff; whistleblower line available",
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_code_of_conduct_acknowledged_by_all_staff(
    code_of_conduct_records, personnel_roster
):
    """CC1.2 — Code of conduct must be acknowledged by all in-scope personnel."""
    acknowledged_ids = {
        r["employee_id"] for r in code_of_conduct_records
        if r.get("current_acknowledgment")
    }
    violations = [
        p for p in personnel_roster
        if p.get("in_soc2_boundary") and p["employee_id"] not in acknowledged_ids
    ]
    assert not violations, (
        f"NONCONFORMITY (CC1.2): {len(violations)} personnel without current code of "
        f"conduct acknowledgment: {[p['employee_id'] for p in violations]}"
    )


def test_ciso_or_equivalent_designated(security_role_assignments):
    """CC1.3 — CISO or equivalent security responsibility role must be formally designated."""
    ciso_roles = [
        r for r in security_role_assignments
        if r.get("role_type") in ("ciso", "security_lead", "isms_manager", "security_officer")
        and r.get("formally_designated")
    ]
    assert ciso_roles, (
        "NONCONFORMITY (CC1.3): No CISO or equivalent formally designated — a security "
        "responsibility role assignment is required"
    )


def test_system_description_current(system_description_records):
    """CC2.3 — System description must be reviewed within the last 12 months."""
    today = date.today()
    assert system_description_records, (
        "NONCONFORMITY (CC2.3): No system description found — system description is "
        "required for all SOC 2 engagements"
    )
    latest = max(
        system_description_records,
        key=lambda r: r.get("last_reviewed_date", date.min)
    )
    days_since = (today - latest["last_reviewed_date"]).days
    assert days_since <= SYSTEM_DESCRIPTION_MAX_AGE_DAYS, (
        f"NONCONFORMITY (CC2.3): System description last reviewed {days_since} days ago "
        f"(max {SYSTEM_DESCRIPTION_MAX_AGE_DAYS}) — must be current before audit engagement"
    )


@pytest.mark.human_review_required(
    reason=(
        "CC3.2: Risk assessment methodology adequacy and risk completeness "
        "cannot be validated by automated test — auditor evaluation required."
    )
)
def test_risk_register_exists_and_populated(risk_register_entries):
    """CC3.1/CC3.2 — Risk register must exist and be populated (existence only)."""
    assert risk_register_entries, (
        "NONCONFORMITY (CC3.2): Risk register is empty — identified risks are required. "
        "NOTE: Risk completeness requires human review."
    )
    no_owner = [r for r in risk_register_entries if not r.get("risk_owner")]
    assert not no_owner, (
        f"NONCONFORMITY (CC3.2): {len(no_owner)} risk(s) without assigned owner"
    )


def test_deficiencies_logged_and_escalated(deficiency_records):
    """CC4.2 — All control deficiencies must be logged; significant ones escalated."""
    today = date.today()
    violations = []
    for d in deficiency_records:
        if d.get("severity") not in ("significant", "material"):
            continue
        if d.get("management_notified"):
            continue
        days_open = (today - d["identified_date"]).days
        if days_open > DEFICIENCY_ESCALATION_MAX_DAYS:
            violations.append(
                f"Deficiency {d.get('deficiency_id')}: {d['severity']}, "
                f"open {days_open} days without management escalation"
            )
    assert not violations, (
        f"NONCONFORMITY (CC4.2): {len(violations)} significant/material deficiency/ies "
        f"not escalated to management:\n" + "\n".join(violations)
    )
```

---

## Notes for the registry

- **CC1–CC4 and the COSO framework:** SOC 2 CC1–CC4 are direct mappings to COSO Internal Control–Integrated Framework (2013). Organizations that have assessed against COSO for SOX compliance can reuse significant portions of their CC1–CC4 evidence. The SOC 2 engagement is scoped to the service organization's commitments, but the control environment evidence base is the same.
- **CC1.1 board oversight — practical evidence:** For small service organizations without a traditional board, the "equivalent governing body" is typically the founding team or principal leadership. SOC 2 auditors accept a documented leadership oversight structure (e.g., quarterly executive security review with documented minutes) in lieu of a formal board for small organizations.
- **CC3.2 risk assessment — the contested core:** This is the single most CONTESTED criterion in all of SOC 2. The standard does not prescribe a methodology; NIST SP 800-30, ISO 27005, FAIR, and bespoke matrices are all acceptable. The test `test_risk_register_exists_and_populated` verifies existence and ownership only — the Pattern 3 decorator surfaces the adequacy question for human auditor review.
- **System description (CC2.3) as the engagement anchor:** The system description is the foundation of the entire SOC 2 report. Every control is evaluated in the context of the system boundary defined in the description. Stale or inaccurate system descriptions are a major audit finding and can cause the auditor to scope-expand (add more system components) or qualify the report.
- **CC4 and management review overlap with ISO 27001 Clause 9.3:** ISO 27001 Clause 9.3 (Management Review) and SOC 2 CC4.1 (Ongoing Evaluations) both require periodic management review of the control framework. A single annual management review meeting with documented agenda and action items satisfies both criteria.
