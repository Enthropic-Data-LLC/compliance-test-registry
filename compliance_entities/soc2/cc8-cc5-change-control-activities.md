# SOC 2 TSC 2017 — CC8: Change Management + CC5: Control Activities

**Registry path:** `/regulation-registry/SOC2/CC8-CC5/`
**Version:** AICPA TSC 2017 (2022 points of focus updates)
**Last parsed:** 2026-05-20
**Applies to:** Service organizations (SaaS, cloud providers, data centers, managed-service providers) whose services are relevant to user-entity controls
**Trigger:** Customer contract requirement; investor due-diligence; voluntary for competitive positioning; required when customers request a SOC 2 Type I or Type II report from their auditor
**Jurisdiction:** United States (AICPA Trust Services Criteria); widely accepted internationally as equivalent to ISO 27001 attestation
**Not applicable to:** Internal IT departments; organizations that do not provide services to other companies; product companies without a service component
**Overall confidence:** MEDIUM — CC8.1 change management process existence is DETERMINISTIC; change authorization and testing adequacy is PARAMETERIZED; CC5 policy deployment is DETERMINISTIC for existence, PARAMETERIZED for content
**4 criteria total: CC8.1 + CC5.1–CC5.3**

---

## Scope summary

CC8 (Change Management) has a single criterion — CC8.1 — covering the entire change management lifecycle. It is grouped with CC5 (Control Activities) here because both are process-level controls with moderate DETERMINISTIC content and are frequently assessed together in SOC 2 audits.

CC5 addresses how the entity selects, designs, and deploys control activities. CC5.3 (Policy Deployment) has a DETERMINISTIC element: policies must be documented and communicated. CC5.1–CC5.2 are PARAMETERIZED because control selection adequacy and technology general controls are auditor-evaluated.

---

## CC8.1 — Change Management (MEDIUM)

### Source excerpt

> The entity authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes to infrastructure, data, software, and procedures to meet its objectives.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All changes to in-scope infrastructure, software, data, and procedures | DETERMINISTIC |
| Obligation | Change management process documented; changes authorized and reviewed before implementation; testing performed; emergency change process defined | DETERMINISTIC (process existence) / PARAMETERIZED (adequacy) |
| Evidence | `change_management_policy.documented == true`; `change_records.authorization_documented`; `change_records.testing_completed`; emergency change log | DETERMINISTIC + PARAMETERIZED |

**Points of focus (2022):** Manages changes throughout the system lifecycle; authorizes changes; designs and develops changes; tests system changes; approves system changes; deploys system changes; identifies and evaluates system changes.

**Assumption (ASSUME-SOC2-CC8-001):** Change management is adequate when: (1) all changes to production systems processed through documented change management workflow — no unauthorized direct production changes; (2) changes classified: standard (pre-approved low-risk), normal (requires review and testing), emergency (expedited but post-implementation reviewed); (3) normal changes require: documented change request, impact assessment, test plan, rollback plan, approval by authorized approver (developer cannot approve own changes); (4) emergency changes reviewed for completeness within 5 business days of implementation; (5) change freeze periods (release windows) documented and enforced; (6) separation of duties: developer cannot deploy their own changes to production.

**Overall: DETERMINISTIC for process existence → Pattern 1; PARAMETERIZED for process adequacy → Pattern 2**

---

## CC5.1 — Control Selection and Development (PARAMETERIZED)

### Source excerpt

> The entity selects and develops control activities that contribute to the mitigation of risks to the achievement of objectives to acceptable levels.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Risk-based controls selected; controls designed to address identified risks; preventive, detective, and corrective controls represented | PARAMETERIZED |
| Evidence | `risk_register.controls_mapped == true`; control inventory with risk linkage | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## CC5.2 — Technology Controls (MEDIUM)

### Source excerpt

> The entity also selects and develops general control activities over technology to support the achievement of objectives.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | General IT controls documented and operating: access controls, change management, operations management, IT governance | PARAMETERIZED |
| Evidence | `gitc_assessment.completed == true`; general IT controls tested and operating | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## CC5.3 — Policy Deployment (MEDIUM)

### Source excerpt

> The entity deploys control activities through policies that establish what is expected and procedures that put policies into action.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Policies and procedures documented; communicated to relevant personnel; responsibilities assigned; controls operating as described in policies | DETERMINISTIC (existence) / PARAMETERIZED (adequacy) |
| Evidence | `security_policies.documented == true`; `policy_acknowledgment_records.all_staff_acknowledged == true`; `policy_last_reviewed_date` ≤ 365 days | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-SOC2-CC5-001):** Policy deployment is adequate when: (1) security policies documented and approved by management; (2) policies reviewed and updated at least annually; (3) all in-scope personnel acknowledge policies (signed or tracked acknowledgment); (4) procedures exist for all significant control activities — policy alone is insufficient without operational procedures; (5) policies accessible to all relevant personnel.

**Overall: DETERMINISTIC for policy existence and annual review → Pattern 1; PARAMETERIZED for content adequacy → Pattern 2**

---

## YAML specifications

### `cc8_change_management.yaml`

```yaml
regulation_id: SOC2-TSC2017-CC8.1
section: "SOC 2 TSC 2017 — CC8: Change Management"
r_or_a: Required
source_text: >
  The entity authorizes, designs, develops or acquires, configures, documents, tests,
  approves, and implements changes to infrastructure, data, software, and procedures
  to meet its objectives.

extracted_elements:
  subject: "All production system changes within SOC 2 boundary"
  condition: "Change to production systems"
  obligation: "Authorized; documented; tested; approved before deployment; emergency changes reviewed post-deploy"
  evidence: "change_records: request, authorization, test_result, approval, deployment_date"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-SOC2-CC8-001
    assumption_text: >
      Change process: documented workflow; standard/normal/emergency classification;
      normal = request + impact + test plan + rollback + approval (not self-approved);
      emergency reviewed within 5 days; separation of duties for production deploy.
    assumed_by: "ISMS Manager"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
test_confidence: MEDIUM
generated_test: "tests/soc2/test_cc8_change_management.py"
```

---

## Generated tests

### `tests/soc2/test_cc8_change_management.py`

```python
"""
SOC 2 TSC 2017 — CC8: Change Management + CC5: Control Activities
Confidence: MEDIUM — process existence DETERMINISTIC; adequacy PARAMETERIZED
"""
import pytest
from datetime import date

EMERGENCY_CHANGE_REVIEW_MAX_DAYS = 5
POLICY_REVIEW_MAX_DAYS = 365


@pytest.mark.assumption(
    id="ASSUME-SOC2-CC8-001",
    description=(
        "Change process: documented; normal changes = request + impact + test + rollback + approval; "
        "emergency reviewed ≤5 business days; no self-approval."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_production_changes_have_authorization(change_records):
    """CC8.1 — All production changes must be authorized before deployment."""
    violations = [
        r for r in change_records
        if r.get("affects_production")
        and r.get("change_type") != "emergency"
        and not r.get("authorization_documented")
    ]
    assert not violations, (
        f"NONCONFORMITY (CC8.1): {len(violations)} production change(s) without "
        f"documented authorization: {[r.get('change_id') for r in violations]}"
    )


def test_no_self_approved_changes(change_records):
    """CC8.1 — Developers cannot approve their own production changes (separation of duties)."""
    violations = [
        r for r in change_records
        if r.get("affects_production")
        and r.get("requester_id") == r.get("approver_id")
        and r.get("change_type") != "emergency"
    ]
    assert not violations, (
        f"NONCONFORMITY (CC8.1): {len(violations)} production change(s) self-approved "
        f"(requester == approver): {[r.get('change_id') for r in violations]}"
    )


def test_emergency_changes_reviewed_within_5_days(change_records):
    """CC8.1 — Emergency changes must be reviewed for completeness within 5 business days."""
    today = date.today()
    violations = []
    for r in change_records:
        if r.get("change_type") != "emergency":
            continue
        if r.get("post_implementation_review_completed"):
            continue
        days_since = (today - r["deployment_date"]).days
        if days_since > EMERGENCY_CHANGE_REVIEW_MAX_DAYS:
            violations.append(
                f"Change {r['change_id']}: deployed {days_since} days ago, "
                f"post-implementation review not completed"
            )
    assert not violations, (
        f"NONCONFORMITY (CC8.1): {len(violations)} emergency change(s) without "
        f"timely post-implementation review:\n" + "\n".join(violations)
    )


def test_normal_changes_have_test_evidence(change_records):
    """CC8.1 — Normal changes must have documented test results before deployment."""
    violations = [
        r for r in change_records
        if r.get("affects_production")
        and r.get("change_type") == "normal"
        and not r.get("testing_documented")
    ]
    assert not violations, (
        f"NONCONFORMITY (CC8.1): {len(violations)} normal production change(s) without "
        f"documented test results: {[r.get('change_id') for r in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-SOC2-CC5-001",
    description="Security policies: documented; annual review; all staff acknowledged; procedures for all significant controls",
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_security_policies_reviewed_within_12_months(policy_records):
    """CC5.3 — Security policies must be reviewed at least annually."""
    today = date.today()
    security_policies = [
        p for p in policy_records
        if p.get("in_soc2_boundary")
        and p.get("policy_category") == "security"
    ]
    if not security_policies:
        assert False, "NONCONFORMITY (CC5.3): No security policy records found"
    violations = []
    for policy in security_policies:
        last_reviewed = policy.get("last_reviewed_date")
        if last_reviewed is None:
            violations.append(f"{policy['policy_id']}: no review date recorded")
        elif (today - last_reviewed).days > POLICY_REVIEW_MAX_DAYS:
            violations.append(
                f"{policy['policy_id']}: last reviewed "
                f"{(today - last_reviewed).days} days ago"
            )
    assert not violations, (
        f"NONCONFORMITY (CC5.3): {len(violations)} security policy/ies overdue for review:\n"
        + "\n".join(violations)
    )


def test_all_staff_acknowledged_policies(policy_records, personnel_roster):
    """CC5.3 — All in-scope personnel must have acknowledged current security policies."""
    violations = []
    for policy in policy_records:
        if not policy.get("requires_acknowledgment"):
            continue
        acknowledged_ids = set(policy.get("acknowledged_employee_ids", []))
        for person in personnel_roster:
            if person.get("in_soc2_boundary") and person["employee_id"] not in acknowledged_ids:
                violations.append(
                    f"Policy {policy['policy_id']}: {person['employee_id']} "
                    f"({person.get('name')}) has not acknowledged"
                )
    assert not violations, (
        f"NONCONFORMITY (CC5.3): {len(violations)} policy acknowledgment gap(s):\n"
        + "\n".join(violations[:20])  # Cap display at 20
    )
```

---

## Notes for the registry

- **CC8.1 and DevOps/CI-CD pipelines:** Modern CI/CD pipelines can satisfy CC8.1 if the pipeline enforces authorization gates — e.g., code review approval required before merge, deployment pipeline gates that verify approvals. The evidence is in pull request records and pipeline run logs. The key test is that no code was deployed without review — automated enforcement is acceptable, but the control must be configured and tested.
- **Emergency changes as an audit focus area:** Type II auditors sample emergency changes specifically because they are the most likely bypass point for change management controls. A high volume of emergency changes relative to total changes is itself an observation point — it may indicate the normal change process is too slow, leading teams to misclassify normal changes as emergencies.
- **CC5.3 policy acknowledgment:** Policy acknowledgment tracking is frequently managed via LMS (learning management system) or HR onboarding systems. For Type II audits, the evidence must show acknowledgment was obtained during the audit period — blanket acknowledgments from years prior do not satisfy the ongoing operating effectiveness requirement for the period.
- **CC8 and CC5 relationship to CC6:** CC8.1 and CC5 provide the management control framework that CC6 (access controls) operates within. A Type II auditor will test that: access control policy (CC5.3) is current; access control changes (user provisioning/deprovisioning) go through a documented workflow (CC8.1); and the actual access configurations align with what the policies and workflows prescribe (CC6.1).
