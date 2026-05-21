# Requirement 12 — Support Information Security with Organizational Policies and Programs

**Registry path:** `/regulation-registry/PCI-DSS/Req-12/`
**Version:** PCI DSS v4.0 (mandatory since March 31, 2025)
**Last parsed:** 2026-05-20
**Overall confidence:** MEDIUM — annual review cadences are DETERMINISTIC; policy content adequacy is PARAMETERIZED
**R = Required**

---

## Scope summary

Req 12 is the organizational governance requirement — it mandates that compliance obligations be backed by written policies, personnel training, third-party service provider management, and an incident response plan. Most cadence thresholds (annual policy review, annual security training, IRP testing, CDE scope validation) are DETERMINISTIC. Policy content adequacy and incident response plan completeness are PARAMETERIZED.

v4.0 elevated several program elements from best practice to formal requirements, including targeted risk analyses, CISO designation, and quarterly compliance reviews for service providers.

---

## 12.1 — Information Security Policy (R — DETERMINISTIC for cadence; PARAMETERIZED for content)

### Source excerpt

> *12.1.1 — An overall information security policy is established, published, maintained, and disseminated to all relevant personnel and applicable vendors/business partners.*
> *12.1.2 — The information security policy is reviewed at least once every 12 months and is updated as needed to reflect changes to business objectives or the risk environment.*
> *12.1.4 — Responsibility for information security is formally assigned to a Chief Information Security Officer or other information security officer with the knowledge and experience to manage an information security program.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | Information security policy | DETERMINISTIC |
| Condition | Organization is in scope | DETERMINISTIC |
| Obligation | Policy documented and disseminated; reviewed ≤ 12 months; CISO or equivalent formally designated | DETERMINISTIC |
| Evidence | `policy_records.security_policy_review_date` ≤ 365 days; `org_chart.ciso_or_equivalent_designated == true` | DETERMINISTIC |

**Overall: DETERMINISTIC for cadence and CISO → Pattern 1; PARAMETERIZED for content → Pattern 2**

---

## 12.5 — PCI DSS Scope Validation (R — DETERMINISTIC)

### Source excerpt

> *12.5.1 — An inventory of system components that are in scope for PCI DSS, including a description of function/use, is maintained and kept current.*
> *12.5.2 — PCI DSS scope is documented and confirmed by the entity at least once every 12 months and upon significant change to the in-scope environment. At a minimum, the scoping validation includes identifying and confirming the accuracy of all data flows for account data.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | CDE scope inventory and data flows | DETERMINISTIC |
| Condition | PCI DSS assessment year or significant change | DETERMINISTIC |
| Obligation | CDE inventory current; scope formally validated ≤ 365 days; data flow diagrams current | DETERMINISTIC |
| Evidence | `cde_inventory.last_validated_date` ≤ 365 days; `data_flow_diagrams.current == true` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 12.6 — Security Awareness Education (R — DETERMINISTIC)

### Source excerpt

> *12.6.3 — Personnel receive security awareness training upon hire and at least once every 12 months.*
> *12.6.3.1 — Security awareness training includes awareness of threats that could impact the security of the CDE, including but not limited to phishing and related attacks.*
> *12.6.3.2 — Security awareness training includes awareness of the acceptable use policy and that personnel are required to acknowledge at least once every 12 months that they have read and understood the acceptable use policy.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All personnel with CDE access | DETERMINISTIC |
| Condition | Upon hire and annually thereafter | DETERMINISTIC |
| Obligation | Security awareness training ≤ 365 days; covers threats including phishing; includes AUP acknowledgment | DETERMINISTIC |
| Evidence | `training_records.employee_id`; `training_date` ≤ 365 days; `training_type == "security_awareness"`; `aup_acknowledged == true` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 12.8 — Third-Party Service Provider (TPSP) Management (R — DETERMINISTIC)

### Source excerpt

> *12.8.1 — A list of all TPSPs with which account data is shared or that could affect the security of account data is maintained, including a description of the service(s) provided.*
> *12.8.4 — A program is implemented to monitor TPSPs' PCI DSS compliance status at least once every 12 months.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All TPSPs with access to account data or CDE connectivity | DETERMINISTIC |
| Condition | TPSP relationship exists | DETERMINISTIC |
| Obligation | TPSP inventory maintained; PCI DSS compliance monitored ≤ 365 days | DETERMINISTIC |
| Evidence | `tpsp_inventory.exists == true`; `tpsp_compliance_records.last_reviewed_date` ≤ 365 days per TPSP | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 12.10 — Incident Response Plan (R — DETERMINISTIC for existence and cadence; PARAMETERIZED for content)

### Source excerpt

> *12.10.1 — An incident response plan exists and is ready to be activated immediately in the event of a system breach.*
> *12.10.2 — At least once every 12 months, the incident response plan is reviewed and tested, including all elements listed in Requirement 12.10.1.*
> *12.10.3 — Specific personnel are designated to be available on a 24/7 basis to respond to suspected or confirmed security incidents.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | Incident response plan (IRP) | DETERMINISTIC |
| Condition | Organization processes CHD | DETERMINISTIC |
| Obligation | IRP documented; tested ≤ 365 days; 24/7 response personnel designated; card brand procedures referenced | DETERMINISTIC |
| Evidence | `irp_records.exists == true`; `irp_records.last_tested_date` ≤ 365 days; `irp_contacts.24x7_available == true` | DETERMINISTIC |

**Assumption (ASSUME-12-001):** IRP is adequate when it includes: (1) defined roles and responsibilities for incident response team; (2) communication and escalation procedures; (3) containment, eradication, and recovery procedures; (4) reference to card brand incident response procedures (Visa CISP, Mastercard SDP); (5) forensic evidence preservation procedures; (6) criteria for escalating to law enforcement; AND (7) tested via tabletop exercise or simulation at least annually.

**Overall: DETERMINISTIC for cadence → Pattern 1; PARAMETERIZED for content → Pattern 2**

---

## YAML specifications

### `req12_policy_review.yaml`

```yaml
regulation_id: PCI-DSS-v4.0-12.1.2
section: "PCI DSS v4.0 — Information Security Policy Review"
r_or_a: Required
source_text: >
  The information security policy is reviewed at least once every 12 months
  and is updated as needed.

extracted_elements:
  subject: "Overall information security policy"
  condition: "Policy exists"
  obligation: "Reviewed ≤ 12 months"
  evidence: "policy_records.security_policy_review_date within 365 days"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log: []
test_confidence: HIGH
generated_test: "tests/req12/test_12_1_policy.py"
```

---

## Generated tests

### `tests/req12/test_12_1_policy.py`

```python
"""
PCI DSS v4.0 Req 12.1 — Information Security Policy
Confidence: HIGH for cadence; MEDIUM for content adequacy
"""
from datetime import date

POLICY_REVIEW_MAX_DAYS = 365


def test_security_policy_reviewed_within_12_months(policy_records):
    """12.1.2 — Security policy reviewed at least annually."""
    today = date.today()
    security_policies = [
        r for r in policy_records
        if r.get("policy_type") == "information_security"
    ]
    if not security_policies:
        assert False, (
            "VIOLATION (12.1.1): No information security policy on record"
        )
    latest = max(security_policies, key=lambda r: r.get("last_reviewed_date", date.min))
    days_since = (today - latest["last_reviewed_date"]).days
    assert days_since <= POLICY_REVIEW_MAX_DAYS, (
        f"VIOLATION (12.1.2): Security policy last reviewed {days_since} days ago "
        f"(max {POLICY_REVIEW_MAX_DAYS})"
    )


def test_ciso_formally_designated(org_chart):
    """12.1.4 — A CISO or equivalent must be formally designated."""
    assert org_chart.get("ciso_or_equivalent_designated"), (
        "VIOLATION (12.1.4): No CISO or information security officer formally "
        "designated — assignment must be documented in org chart or formal designation record"
    )
```

### `tests/req12/test_12_5_scope.py`

```python
"""
PCI DSS v4.0 Req 12.5 — PCI DSS Scope Validation
Confidence: HIGH | Human Review: NOT REQUIRED
"""
from datetime import date

SCOPE_VALIDATION_MAX_DAYS = 365


def test_cde_scope_validated_within_12_months(scope_validation_records):
    """12.5.2 — PCI DSS scope validated at least annually."""
    today = date.today()
    if not scope_validation_records:
        assert False, (
            "VIOLATION (12.5.2): No PCI DSS scope validation records found"
        )
    latest = max(scope_validation_records, key=lambda r: r["validation_date"])
    days_since = (today - latest["validation_date"]).days
    assert days_since <= SCOPE_VALIDATION_MAX_DAYS, (
        f"VIOLATION (12.5.2): PCI DSS scope last validated {days_since} days ago "
        f"(max {SCOPE_VALIDATION_MAX_DAYS})"
    )


def test_data_flow_diagrams_current(data_flow_diagram_records):
    """12.5.2 — Data flow diagrams must be current."""
    violations = [
        d for d in data_flow_diagram_records
        if not d.get("current")
    ]
    assert not violations, (
        f"VIOLATION (12.5.2): {len(violations)} data flow diagram(s) marked as "
        f"not current: {[d.get('diagram_id') for d in violations]}"
    )
```

### `tests/req12/test_12_6_training.py`

```python
"""
PCI DSS v4.0 Req 12.6 — Security Awareness Training
Confidence: HIGH | Human Review: NOT REQUIRED
"""
from datetime import date

TRAINING_MAX_DAYS = 365


def test_all_cde_personnel_trained_within_12_months(training_records, personnel_roster):
    """12.6.3 — All personnel with CDE access trained within past 12 months."""
    today = date.today()
    trained_ids = {
        r["employee_id"] for r in training_records
        if r.get("training_type") == "security_awareness"
        and (today - r["training_date"]).days <= TRAINING_MAX_DAYS
    }
    violations = [
        p for p in personnel_roster
        if p.get("has_cde_access") and p["employee_id"] not in trained_ids
    ]
    assert not violations, (
        f"VIOLATION (12.6.3): {len(violations)} personnel with CDE access and no "
        f"current security awareness training:\n"
        + "\n".join(
            f"  {p['employee_id']}: {p.get('name')}" for p in violations
        )
    )


def test_training_covers_phishing_and_aup(training_records):
    """12.6.3.1 / 12.6.3.2 — Training must cover phishing threats and AUP acknowledgment."""
    violations = []
    for record in training_records:
        if record.get("training_type") != "security_awareness":
            continue
        if not record.get("covers_phishing"):
            violations.append(
                f"{record['employee_id']}: training on {record['training_date']} "
                f"does not cover phishing"
            )
        if not record.get("aup_acknowledged"):
            violations.append(
                f"{record['employee_id']}: AUP not acknowledged in training"
            )
    assert not violations, (
        f"VIOLATION (12.6.3.1/12.6.3.2): {len(violations)} training record(s) missing "
        f"required content:\n" + "\n".join(violations)
    )
```

### `tests/req12/test_12_10_incident_response.py`

```python
"""
PCI DSS v4.0 Req 12.10 — Incident Response Plan
Confidence: HIGH for cadence; MEDIUM for IRP content adequacy
"""
import pytest
from datetime import date

IRP_TEST_MAX_DAYS = 365


def test_incident_response_plan_exists(irp_records):
    """12.10.1 — IRP must exist and be ready for immediate activation."""
    assert irp_records, (
        "VIOLATION (12.10.1): No incident response plan on record"
    )


def test_irp_tested_within_12_months(irp_records):
    """12.10.2 — IRP must be reviewed and tested at least annually."""
    today = date.today()
    tested_plans = [r for r in irp_records if r.get("last_tested_date")]
    if not tested_plans:
        assert False, (
            "VIOLATION (12.10.2): No IRP test records found — "
            "annual testing is required"
        )
    latest = max(tested_plans, key=lambda r: r["last_tested_date"])
    days_since = (today - latest["last_tested_date"]).days
    assert days_since <= IRP_TEST_MAX_DAYS, (
        f"VIOLATION (12.10.2): IRP last tested {days_since} days ago "
        f"(max {IRP_TEST_MAX_DAYS})"
    )


def test_24x7_incident_response_contacts_designated(irp_records):
    """12.10.3 — Personnel must be designated for 24/7 incident response."""
    violations = [r for r in irp_records if not r.get("contacts_24x7_designated")]
    assert not violations, (
        f"VIOLATION (12.10.3): {len(violations)} IRP(s) without designated 24/7 "
        f"response personnel: {[r.get('plan_id') for r in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-12-001",
    description=(
        "IRP adequate: defined roles; escalation procedures; containment/recovery; "
        "card brand procedures referenced; forensic preservation; tested via "
        "tabletop/simulation annually."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_irp_includes_card_brand_procedures(irp_records):
    violations = [r for r in irp_records if not r.get("card_brand_procedures_referenced")]
    assert not violations, (
        f"VIOLATION (12.10.6): {len(violations)} IRP(s) without reference to card "
        f"brand incident response procedures (Visa CISP, Mastercard SDP): "
        f"{[r.get('plan_id') for r in violations]}"
    )


def test_tpsp_pci_compliance_monitored_annually(tpsp_compliance_records):
    """12.8.4 — All TPSP PCI DSS compliance status reviewed at least annually."""
    today = date.today()
    violations = []
    for record in tpsp_compliance_records:
        last_reviewed = record.get("last_compliance_check_date")
        if not last_reviewed:
            violations.append(f"TPSP {record['tpsp_id']}: no compliance check date")
            continue
        days = (today - last_reviewed).days
        if days > 365:
            violations.append(
                f"TPSP {record['tpsp_id']}: compliance last reviewed {days} days ago"
            )
    assert not violations, (
        f"VIOLATION (12.8.4): {len(violations)} TPSP compliance record(s) not "
        f"reviewed annually:\n" + "\n".join(violations)
    )
```

---

## Notes for the registry

- **Targeted risk analysis (12.3.1):** v4.0 introduced the concept of a "targeted risk analysis" (TRA) for several requirements where the frequency is not a fixed interval but organization-defined. For example, 9.5.1.2 (POI inspection) and 10.4.2 (non-critical log review) allow organization-defined frequencies justified by a TRA. The TRA must be documented, reviewed, and approved. A generic annual risk assessment is not the same as a targeted risk analysis for a specific control.
- **CISO designation vs. job title:** 12.1.4 does not require the title "CISO" — it requires an individual formally assigned responsibility for the information security program with "knowledge and experience." A VP of IT who also owns security may satisfy this if formally designated.
- **Service provider quarterly reviews (12.4.2):** Service providers must perform quarterly reviews to confirm that security controls are operating effectively and personnel are following security policies. This requirement applies only to service providers, not merchants.
- **TPSP vs. subcontractor:** 12.8 addresses TPSPs — vendors who store, process, or transmit account data, or whose services could affect the security of CHD. TPSPs must provide their own PCI DSS Attestation of Compliance (AOC) or Responsibility Matrix. Simple utility vendors with no CHD access are not TPSPs under this definition.
- **IRP card brand procedures:** When a confirmed breach occurs, Visa and Mastercard each have specific reporting procedures (CISP for Visa, SDP for Mastercard). The IRP must reference these programs and include the relevant breach notification contact information. Failure to follow card brand procedures post-breach is itself a compliance violation.
