# ISO/IEC 27001:2022 — Annex A Theme 2: People Controls (A.6.x)

**Registry path:** `/regulation-registry/ISO-27001/Annex-A6/`
**Version:** ISO/IEC 27001:2022
**Last parsed:** 2026-05-20
**Overall confidence:** MEDIUM — personnel security controls are largely PARAMETERIZED; A.6.3 (training) has a DETERMINISTIC cadence element; A.6.5 (termination) has a DETERMINISTIC existence element
**8 controls: A.6.1–A.6.8**

---

## Scope summary

Theme 2 (People Controls) is the smallest Annex A theme — 8 controls covering the full employee lifecycle from pre-employment screening through termination and post-employment obligations, plus remote working and event reporting. All 8 controls were present in ISO 27001:2013 under Clause A.7 (Human Resource Security); A.6.7 (Remote Working) was reorganized from A.6.2.2 in the 2013 edition into this theme with expanded guidance in 2022.

Most people controls are PARAMETERIZED because they depend on HR processes, employment law, and organizational culture. The DETERMINISTIC elements are: security awareness training existence (binary) and termination procedures existence (binary). Training cadence (annual) and screening scope are PARAMETERIZED with documented assumptions.

---

## A.6.1 — Screening (PARAMETERIZED)

### Source excerpt

> Background verification checks on all candidates for employment shall be carried out prior to joining the organization and on an ongoing basis, taking into consideration applicable laws, regulations and ethics and proportional to the business requirements, the classification of the information to be accessed and the perceived risks.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All new employees and contractors | DETERMINISTIC |
| Condition | Prior to employment commencement; proportional to role access level | PARAMETERIZED |
| Obligation | Background verification performed; scope proportional to information access; compliant with applicable law | PARAMETERIZED |
| Evidence | `screening_records.employee_id`; `screening_scope` matches role risk classification; `legal_compliance_noted` | PARAMETERIZED |

**Assumption (ASSUME-ISO-A6-001):** Screening is adequate when: (1) minimum checks for all employees with ISMS scope access: identity verification, employment history verification, and reference check; (2) extended checks for roles with access to sensitive information: criminal records check (where legally permitted), financial/credit check for finance roles; (3) screening completed before access to sensitive systems is granted; (4) screening documentation retained per local employment law retention requirements; (5) ongoing checks (re-screening) triggered by significant behavioral changes or when roles change to higher-trust access.

**Overall: PARAMETERIZED → Pattern 2**

---

## A.6.2 — Terms and Conditions of Employment (PARAMETERIZED)

### Source excerpt

> Employment contractual agreements shall state the personnel's and the organization's responsibilities for information security.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | IS responsibilities documented in employment contract or supplementary agreement; staff acknowledge IS obligations | DETERMINISTIC (existence) / PARAMETERIZED (content) |
| Evidence | `employment_contracts.is_clause_included == true`; `acknowledgment_records.signed == true` | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-A6-002):** Employment agreement IS terms are adequate when they include: (1) reference to the IS policy and requirement to comply; (2) confidentiality and non-disclosure obligation; (3) data protection and privacy obligations; (4) acceptable use obligations; (5) intellectual property assignment for work product; (6) reporting obligations for IS events and concerns; (7) consequences of breach (disciplinary process reference).

**Overall: PARAMETERIZED → Pattern 2**

---

## A.6.3 — Information Security Awareness, Education, and Training (MEDIUM — cadence DETERMINISTIC)

### Source excerpt

> Personnel of the organization and relevant interested parties shall receive appropriate information security awareness, education and training and regular updates in organizational policies and procedures, as relevant to their job function.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All personnel within ISMS scope | DETERMINISTIC |
| Condition | On hire and at regular intervals thereafter | DETERMINISTIC |
| Obligation | IS awareness training provided upon hire; repeated at regular intervals; job-function-relevant content; policy updates communicated | PARAMETERIZED (content) / DETERMINISTIC (cadence with assumption) |
| Evidence | `training_records.employee_id`; `training_date` within last 365 days; `training_content_relevant == true` | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-A6-003):** IS awareness training cadence: annual for all personnel at minimum; new employees trained before accessing sensitive systems. Content must include: applicable IS policies, role-specific IS responsibilities, phishing and social engineering recognition, password hygiene, incident reporting procedures, and consequences of noncompliance. Security awareness program effectiveness should be measured (e.g., phishing simulation results, quiz scores) and used to improve the program.

**Overall: PARAMETERIZED for content → Pattern 2; DETERMINISTIC for annual cadence with assumption → Pattern 1 once assumption is approved**

---

## A.6.4 — Disciplinary Process (PARAMETERIZED)

### Source excerpt

> A formal and communicated disciplinary process shall be in place to take action against personnel who have committed an information security policy violation.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Disciplinary process for IS violations documented, communicated to all staff; graduated sanctions applicable | DETERMINISTIC (existence) / PARAMETERIZED (adequacy) |
| Evidence | `hr_policies.disciplinary_process_for_is_violations_documented == true`; sanctions are proportionate to violation severity | DETERMINISTIC + PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## A.6.5 — Responsibilities After Termination or Change of Employment (DETERMINISTIC for existence)

### Source excerpt

> Information security responsibilities and duties that remain valid after termination or change of employment shall be defined, communicated to the employee or contractor and enforced.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Post-employment IS obligations defined; communicated before or at termination; access revoked promptly; assets returned | DETERMINISTIC (access revocation and asset return) / PARAMETERIZED (scope of ongoing obligations) |
| Evidence | `offboarding_checklist.access_revoked == true`; `offboarding_checklist.assets_returned == true`; `termination_agreement.confidentiality_confirmed == true` | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-A6-004):** Access revocation timing: involuntary termination — immediate revocation (same day, same hour for sensitive roles); voluntary termination — revocation by last day of employment at latest, earlier where risk warrants. Post-employment obligations include: NDA remains enforceable; return of confidential information; prohibition on unauthorized use of organizational knowledge.

**Overall: DETERMINISTIC for access revocation (binary) → Pattern 1; PARAMETERIZED for post-employment obligation scope → Pattern 2**

---

## A.6.6 — Confidentiality or Non-Disclosure Agreements (PARAMETERIZED)

### Source excerpt

> Requirements for confidentiality or non-disclosure agreements reflecting the organization's needs for the protection of information shall be identified, documented, regularly reviewed, and signed by personnel and other relevant interested parties.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | NDA/confidentiality agreement signed by all personnel and relevant third parties with access to sensitive information | DETERMINISTIC (existence) / PARAMETERIZED (content) |
| Evidence | `nda_records.signed == true` for all in-scope personnel and third parties | DETERMINISTIC |

**Overall: DETERMINISTIC for existence → Pattern 1**

---

## A.6.7 — Remote Working *(reorganized/expanded in 2022)* (PARAMETERIZED)

### Source excerpt

> Security measures shall be implemented when personnel are working remotely to protect information accessed, processed or stored outside the organization's premises.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Remote working security policy documented; technical controls for remote access implemented; physical security at remote locations addressed | PARAMETERIZED |
| Evidence | `remote_working_policy.exists == true`; `vpn_or_zero_trust_config.deployed == true`; home workspace security guidance documented | PARAMETERIZED |

**Assumption (ASSUME-ISO-A6-005):** Remote working controls are adequate when: (1) remote access to organizational systems only via approved, encrypted channel (VPN or zero-trust network access); (2) endpoint device meets minimum security requirements (MDM-enrolled, AV active, disk encryption enabled, screen lock configured); (3) remote workers briefed on home workspace physical security (screen positioning, visitor awareness, clean desk for printed material); (4) remote access logs reviewed; (5) personal device usage on organizational data governed by BYOD policy.

**Overall: PARAMETERIZED → Pattern 2**

---

## A.6.8 — Information Security Event Reporting (PARAMETERIZED)

### Source excerpt

> The organization shall provide a mechanism for personnel to report observed or suspected information security events through appropriate channels in a timely manner.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Reporting mechanism defined and communicated; personnel aware of their obligation to report; reports handled promptly | PARAMETERIZED |
| Evidence | `incident_reporting_channel.documented == true`; `awareness_training.covers_reporting == true`; reporting procedures tested | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## YAML specifications

### `a6_training.yaml`

```yaml
regulation_id: ISO-27001-2022-A.6.3
section: "ISO 27001:2022 Annex A — IS Awareness Training"
r_or_a: Required
source_text: >
  Personnel shall receive appropriate IS awareness, education and training
  and regular updates in organizational policies relevant to their job function.

extracted_elements:
  subject: "All personnel within ISMS scope"
  condition: "On hire and at regular intervals (annual minimum)"
  obligation: "IS awareness training completed; job-function-relevant; covers required topics"
  evidence: "training_records: employee_id, training_date within 365 days, content topics"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: PARAMETERIZED
  obligation: PARAMETERIZED
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-ISO-A6-003
    assumption_text: >
      Annual minimum; new employees before sensitive access. Content: policies,
      role responsibilities, phishing, password hygiene, incident reporting,
      consequences of noncompliance. Effectiveness measured.
    assumed_by: "ISMS Manager"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
    cryptographic_hash: "sha256:pending-ci"
test_confidence: HIGH
generated_test: "tests/iso27001/test_a6_people.py"
```

---

## Generated tests

### `tests/iso27001/test_a6_people.py`

```python
"""
ISO 27001:2022 Annex A Theme 2 — People Controls
Confidence: HIGH for A.6.5 access revocation and A.6.3 training cadence; MEDIUM for others
"""
import pytest
from datetime import date

TRAINING_MAX_DAYS = 365


def test_all_isms_personnel_trained_within_12_months(training_records, personnel_roster):
    """A.6.3 — IS awareness training required for all personnel annually."""
    today = date.today()
    trained_ids = {
        r["employee_id"] for r in training_records
        if r.get("training_type") == "security_awareness"
        and (today - r["training_date"]).days <= TRAINING_MAX_DAYS
    }
    violations = [
        p for p in personnel_roster
        if p.get("in_isms_scope") and p["employee_id"] not in trained_ids
    ]
    assert not violations, (
        f"NONCONFORMITY (A.6.3): {len(violations)} ISMS personnel without current "
        f"IS awareness training:\n"
        + "\n".join(
            f"  {p['employee_id']}: {p.get('name')}" for p in violations
        )
    )


@pytest.mark.assumption(
    id="ASSUME-ISO-A6-003",
    description="Annual minimum training; covers phishing, incident reporting, policies",
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_training_covers_required_topics(training_records):
    required_topics = {"phishing", "incident_reporting", "password_hygiene", "policies"}
    violations = []
    for record in training_records:
        if record.get("training_type") != "security_awareness":
            continue
        covered = set(record.get("topics_covered", []))
        missing = required_topics - covered
        if missing:
            violations.append(
                f"{record['employee_id']} ({record['training_date']}): "
                f"missing topics {missing}"
            )
    assert not violations, (
        f"NONCONFORMITY (A.6.3): {len(violations)} training record(s) missing "
        f"required topics:\n" + "\n".join(violations)
    )


def test_access_revoked_on_termination(offboarding_records):
    """A.6.5 — Access must be revoked upon termination of employment."""
    violations = [
        r for r in offboarding_records
        if not r.get("access_revoked")
    ]
    assert not violations, (
        f"NONCONFORMITY (A.6.5): {len(violations)} offboarding record(s) without "
        f"confirmed access revocation: {[r.get('employee_id') for r in violations]}"
    )


def test_ndas_signed_by_all_isms_personnel(nda_records, personnel_roster):
    """A.6.6 — NDA/confidentiality agreement required for all ISMS-scope personnel."""
    signed_ids = {r["employee_id"] for r in nda_records if r.get("signed")}
    violations = [
        p for p in personnel_roster
        if p.get("in_isms_scope") and p["employee_id"] not in signed_ids
    ]
    assert not violations, (
        f"NONCONFORMITY (A.6.6): {len(violations)} ISMS personnel without signed NDA: "
        f"{[p['employee_id'] for p in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-ISO-A6-005",
    description=(
        "Remote working: approved encrypted channel; endpoint security requirements "
        "(MDM, AV, disk encryption, screen lock); home workspace guidance."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_remote_working_policy_exists(remote_working_policy):
    """A.6.7 — Remote working security policy must be documented."""
    assert remote_working_policy, (
        "NONCONFORMITY (A.6.7): No remote working security policy found"
    )
    assert remote_working_policy.get("approved_access_channel_defined"), (
        "NONCONFORMITY (A.6.7): Remote working policy does not define approved "
        "access channel (VPN or ZTNA)"
    )
```

---

## Notes for the registry

- **A.6.1 screening and employment law:** Background screening requirements vary significantly by jurisdiction. In the EU, criminal records checks are heavily restricted under GDPR and national law; in the US, Fair Credit Reporting Act (FCRA) governs background check processes. The adequacy assumption must acknowledge that screening scope is constrained by what is legally permissible in the jurisdiction of employment.
- **A.6.7 remote working (2022 update):** The 2022 edition formalized remote working controls as a standalone control. The COVID-era proliferation of remote work means most organizations already had informal practices; the 2022 edition requires these to be formally documented and assessed against security requirements.
- **A.6.3 training frequency:** "Regular updates" in A.6.3 does not specify frequency. Annual is the universal auditor expectation. For higher-risk roles (e.g., finance personnel, system administrators, personnel with access to particularly sensitive data), more frequent role-specific training may be expected.
- **A.6.5 vs. HIPAA termination procedures:** A.6.5 and HIPAA §164.308(a)(3)(ii)(C) both address termination-related access revocation. The timing assumption (involuntary = same day; voluntary = last day at latest) aligns ASSUME-ISO-A6-004 with ASSUME-308-003 in the HIPAA registry. Organizations subject to both can use a single termination procedure to satisfy both.
- **Awareness training program as evidence:** The training records should capture not just that training was completed but also the date, content covered, and completion method (in-person, LMS, etc.). A signed acknowledgment of completion is best practice. Some auditors require evidence that training was effective (quiz scores, phishing simulation results), not just completed.
