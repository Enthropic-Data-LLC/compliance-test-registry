# ISO/IEC 27001:2022 — Annex A Theme 1: Organizational Controls (A.5.x)

**Registry path:** `/regulation-registry/ISO-27001/Annex-A5/`
**Version:** ISO/IEC 27001:2022
**Last parsed:** 2026-05-20
**Applies to:** Any organization seeking ISO/IEC 27001 certification for its Information Security Management System (ISMS); scope is organization-defined (can be a department, product line, or whole entity)
**Trigger:** Voluntary certification; customer or procurement requirement (especially in EU, UK, financial services); NIS2 Directive in EU references ISO 27001 as an acceptable framework; organizational risk management decision
**Jurisdiction:** Global — ISO/IEC international standard recognized worldwide; certifying bodies accredited per ISO/IEC 17021-1
**Not applicable to:** Mandatory compliance in isolation — ISO 27001 is a voluntary standard with no direct regulatory enforcement; certification applies only to the defined ISMS scope; does not replace sector-specific mandatory frameworks (HIPAA, PCI DSS, GLBA, etc.)
**Overall confidence:** MEDIUM overall — A.5.11 (asset return) and A.5.17 (authentication information) have DETERMINISTIC elements; most organizational controls are PARAMETERIZED; A.5.19–5.22 (supplier controls) and A.5.31 (legal compliance) are CONTESTED
**37 controls: A.5.1–A.5.36**

---

## Scope summary

Theme 1 (Organizational Controls) is the largest Annex A theme with 37 controls covering governance, asset management, access control policy, supplier relationships, incident management, and business continuity. Most controls are PARAMETERIZED — ISO 27001 sets what must be done; how it is done is organization-specific. The highest-confidence sub-areas are A.5.11 (asset return on termination — binary), A.5.17 (password policy — measurable thresholds from 27002 guidance), and A.5.9 (asset inventory — existence is DETERMINISTIC).

---

## A.5.1 — Information Security Policies (PARAMETERIZED)

| Element | Value | Classification |
|---|---|---|
| Obligation | IS policies defined, approved by management, published, and reviewed at regular intervals or when significant changes occur | PARAMETERIZED |
| Evidence | `is_policy.approved_by_management == true`; `is_policy.last_reviewed_date` ≤ 365 days; policy distributed to all relevant parties | PARAMETERIZED |

**Assumption (ASSUME-ISO-A5-001):** Policy review cadence: annually as a minimum; triggered when significant organizational, operational, or threat-landscape changes occur. "Reviewed" means actively examined and updated if necessary — not just version-bumped.

---

## A.5.9 — Inventory of Information and Associated Assets (MEDIUM)

| Element | Value | Classification |
|---|---|---|
| Obligation | Inventory of information and associated assets maintained | DETERMINISTIC (existence) / PARAMETERIZED (completeness) |
| Evidence | `asset_inventory.exists == true`; assets classified; owners assigned | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-A5-002):** Asset inventory is adequate when: (1) all information assets within ISMS scope are identified; (2) each asset has a designated owner; (3) assets are classified by sensitivity; (4) inventory reviewed and updated at least annually or when assets are added, changed, or removed.

---

## A.5.11 — Return of Assets (DETERMINISTIC)

| Element | Value | Classification |
|---|---|---|
| Obligation | All employees and external users return all organizational assets upon termination | DETERMINISTIC |
| Evidence | `offboarding_checklist.assets_returned == true` for all terminated employees | DETERMINISTIC |

---

## A.5.15 — Access Control (MEDIUM)

| Element | Value | Classification |
|---|---|---|
| Obligation | Access control policy defined, documented, reviewed; need-to-know and need-to-use principles applied; access rights reviewed at planned intervals | PARAMETERIZED |
| Evidence | `access_control_policy.exists == true`; access rights review records | PARAMETERIZED |

**Assumption (ASSUME-ISO-A5-003):** Access rights review cadence: at minimum semi-annually for privileged accounts; annually for standard user accounts. Triggered reviews required on: role change, prolonged absence, termination, and security incident.

---

## A.5.17 — Authentication Information (HIGH)

| Element | Value | Classification |
|---|---|---|
| Obligation | Management of authentication information controlled through a formal management process; temporary credentials changed on first login; password quality requirements applied | DETERMINISTIC for measurable thresholds / PARAMETERIZED for process controls |
| Evidence | `password_policy.min_length >= 12`; `password_policy.history_count >= 5`; `auth_config.lockout_after_failed_attempts <= 10`; session timeout configured | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-A5-004):** Authentication policy thresholds (derived from ISO 27002:2022 guidance): minimum password length 12 characters; last 5 passwords prohibited; maximum age 90 days or MFA deployed; lockout after 10 failed attempts; session timeout for unattended sessions ≤ 30 minutes.

---

## A.5.18 — Access Rights (MEDIUM)

| Element | Value | Classification |
|---|---|---|
| Obligation | Provisioning, modification, and deprovisioning of access rights managed through a formal authorization process; reviews at planned intervals | PARAMETERIZED |
| Evidence | `access_request_records.authorization_documented`; `access_review_records.last_review_date` | PARAMETERIZED |

---

## A.5.19 — Information Security in Supplier Relationships (CONTESTED)

| Element | Value | Classification |
|---|---|---|
| Obligation | Processes and procedures defined and implemented to manage IS risks associated with suppliers and partners | CONTESTED |
| Evidence | `supplier_is_policy.exists == true`; supplier risk assessment records | CONTESTED |

> **CONTESTED reason:** "Appropriate" supplier security requirements depend on the sensitivity of information shared and the services provided. The adequacy of supplier assessment methodology, tiering, and contractual clauses is auditor-evaluated.

---

## A.5.20 — Addressing IS in Supplier Agreements (PARAMETERIZED)

| Element | Value | Classification |
|---|---|---|
| Obligation | Relevant IS requirements established and agreed with each supplier that may access, process, store, communicate, or provide IT infrastructure for information | PARAMETERIZED |
| Evidence | `supplier_agreements.security_clauses_present == true`; clause content review | PARAMETERIZED |

**Assumption (ASSUME-ISO-A5-005):** Supplier agreement IS clauses are adequate when they include: (1) scope of access and permitted use; (2) security controls required (aligned with the organization's own ISMS); (3) incident notification obligation; (4) right to audit; (5) data return/destruction on termination; (6) compliance with applicable laws and regulations. For critical suppliers, clauses should additionally include sub-supplier flow-down, personnel background check requirements, and BCM provisions.

---

## A.5.23 — Information Security for Use of Cloud Services *(new in 2022)* (PARAMETERIZED)

| Element | Value | Classification |
|---|---|---|
| Obligation | Processes for acquisition, use, management, and exit from cloud services established, per IS requirements | PARAMETERIZED |
| Evidence | `cloud_security_policy.exists == true`; cloud provider security documentation reviewed; exit strategy documented | PARAMETERIZED |

---

## A.5.24–A.5.28 — Incident Management (MEDIUM)

| Control | Obligation | Classification |
|---|---|---|
| A.5.24 | IS incident management plan documented; roles and responsibilities defined | PARAMETERIZED |
| A.5.25 | IS events assessed to determine if they qualify as incidents | PARAMETERIZED |
| A.5.26 | Incidents responded to according to documented procedures | PARAMETERIZED |
| A.5.27 | Knowledge from incidents used to improve controls | PARAMETERIZED |
| A.5.28 | Evidence from incidents collected, preserved, and maintained | PARAMETERIZED |

**Assumption (ASSUME-ISO-A5-006):** Incident management is adequate when: (1) IRP documented with roles, escalation paths, response procedures, and evidence preservation; (2) incident severity classification scheme defined; (3) incidents logged with timeline, actions taken, and lessons learned; (4) regulatory notification obligations known and timed (e.g., GDPR 72-hour deadline if applicable); (5) annual IRP exercise/tabletop test performed.

---

## A.5.29–A.5.30 — Business Continuity (PARAMETERIZED)

| Control | Obligation | Classification |
|---|---|---|
| A.5.29 | IS continuity requirements determined; IS controls implemented during disruption | PARAMETERIZED |
| A.5.30 (new 2022) | ICT readiness for business continuity planned, implemented, maintained, tested | PARAMETERIZED |

**Assumption (ASSUME-ISO-A5-007):** BCM for IS is adequate when: RTO and RPO objectives defined per business impact analysis; tested at least annually; results used to improve plans; ICT recovery capabilities demonstrated not just documented.

---

## YAML specifications

### `a5_supplier_agreements.yaml`

```yaml
regulation_id: ISO-27001-2022-A.5.20
section: "ISO 27001:2022 Annex A — IS in Supplier Agreements"
r_or_a: Required
source_text: >
  Relevant information security requirements shall be established and agreed
  with each supplier based on the type of supplier relationship.

extracted_elements:
  subject: "All suppliers with access to organizational information or IT infrastructure"
  condition: "Supplier relationship exists with information access"
  obligation: "IS clauses in supplier agreement covering the 6 required areas"
  evidence: "supplier_agreements.security_clauses_present; clause content review"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: PARAMETERIZED
  obligation: PARAMETERIZED
  evidence: PARAMETERIZED

overall_classification: PARAMETERIZED
human_review_required: true
legal_assumption_log:
  - assumption_id: ASSUME-ISO-A5-005
    assumption_text: >
      Adequate clauses: scope of access; required security controls; incident notification;
      right to audit; return/destruction on termination; regulatory compliance.
      Critical suppliers additionally: sub-supplier flow-down, background checks, BCM.
    assumed_by: "ISMS Manager"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
    cryptographic_hash: "sha256:pending-ci"
test_confidence: MEDIUM
generated_test: "tests/iso27001/test_a5_organizational.py"
```

---

## Generated tests

### `tests/iso27001/test_a5_organizational.py`

```python
"""
ISO 27001:2022 Annex A Theme 1 — Organizational Controls
Confidence: HIGH for A.5.11 and A.5.17 thresholds; MEDIUM/PARAMETERIZED for others
"""
import pytest
from datetime import date

POLICY_REVIEW_MAX_DAYS = 365
ACCESS_REVIEW_MAX_DAYS = 180
ASSET_INVENTORY_REVIEW_MAX_DAYS = 365

PASSWORD_MIN_LENGTH = 12
PASSWORD_HISTORY_MIN = 5
MAX_FAILED_ATTEMPTS = 10


def test_assets_returned_on_termination(offboarding_records):
    """A.5.11 — All assets must be returned upon employment termination."""
    violations = [
        r for r in offboarding_records
        if not r.get("assets_returned") and not r.get("asset_return_exception_documented")
    ]
    assert not violations, (
        f"NONCONFORMITY (A.5.11): {len(violations)} offboarding record(s) with "
        f"assets not confirmed returned: {[r.get('employee_id') for r in violations]}"
    )


def test_is_policy_reviewed_within_12_months(policy_records):
    """A.5.1 — IS policy reviewed at least annually."""
    today = date.today()
    is_policies = [p for p in policy_records if p.get("policy_type") == "information_security"]
    if not is_policies:
        assert False, "NONCONFORMITY (A.5.1): No information security policy found"
    latest = max(is_policies, key=lambda p: p.get("last_reviewed_date", date.min))
    days_since = (today - latest["last_reviewed_date"]).days
    assert days_since <= POLICY_REVIEW_MAX_DAYS, (
        f"NONCONFORMITY (A.5.1): IS policy last reviewed {days_since} days ago "
        f"(max {POLICY_REVIEW_MAX_DAYS})"
    )


def test_asset_inventory_exists_with_owners(asset_inventory):
    """A.5.9 — Asset inventory must exist with owners assigned."""
    assert asset_inventory, (
        "NONCONFORMITY (A.5.9): Asset inventory is empty — all ISMS-scoped "
        "assets must be inventoried"
    )
    no_owner = [a for a in asset_inventory if not a.get("asset_owner")]
    assert not no_owner, (
        f"NONCONFORMITY (A.5.9): {len(no_owner)} asset(s) without assigned owner: "
        f"{[a['asset_id'] for a in no_owner]}"
    )


@pytest.mark.assumption(
    id="ASSUME-ISO-A5-004",
    description=(
        "Auth thresholds: min 12 chars; last 5 prohibited; lockout after 10 attempts; "
        "session timeout ≤ 30 min."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_password_policy_meets_minimum_thresholds(auth_system_configs):
    """A.5.17 — Authentication information must meet quality requirements."""
    violations = []
    for cfg in auth_system_configs:
        if not cfg.get("in_isms_scope"):
            continue
        issues = []
        if cfg.get("min_password_length", 0) < PASSWORD_MIN_LENGTH:
            issues.append(
                f"min length {cfg.get('min_password_length')} < {PASSWORD_MIN_LENGTH}"
            )
        if cfg.get("password_history_count", 0) < PASSWORD_HISTORY_MIN:
            issues.append(
                f"history {cfg.get('password_history_count')} < {PASSWORD_HISTORY_MIN}"
            )
        if cfg.get("max_failed_attempts", 9999) > MAX_FAILED_ATTEMPTS:
            issues.append(
                f"lockout threshold {cfg.get('max_failed_attempts')} > {MAX_FAILED_ATTEMPTS}"
            )
        if issues:
            violations.append(f"System {cfg['system_id']}: {'; '.join(issues)}")
    assert not violations, (
        f"NONCONFORMITY (A.5.17): {len(violations)} system(s) not meeting authentication "
        f"quality requirements:\n" + "\n".join(violations)
    )


@pytest.mark.assumption(
    id="ASSUME-ISO-A5-005",
    description=(
        "Supplier agreements: scope; security controls; incident notification; "
        "audit rights; data return/destruction; regulatory compliance."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_all_critical_suppliers_have_is_agreements(supplier_register, supplier_agreements):
    """A.5.20 — All suppliers with information access must have IS agreement clauses."""
    agreement_supplier_ids = {a["supplier_id"] for a in supplier_agreements
                              if a.get("security_clauses_present")}
    violations = [
        s for s in supplier_register
        if s.get("has_information_access")
        and s["supplier_id"] not in agreement_supplier_ids
    ]
    assert not violations, (
        f"NONCONFORMITY (A.5.20): {len(violations)} supplier(s) with information "
        f"access but no IS agreement clauses: "
        f"{[s['supplier_id'] for s in violations]}"
    )
```

---

## Notes for the registry

- **A.5.19–A.5.22 supplier cluster:** The 2022 edition expanded supplier security from two controls (2013: A.15.1 and A.15.2) to four controls, adding A.5.21 (ICT supply chain) and A.5.23 (cloud services). Organizations with complex supply chains need to address all four and ensure the SoA explicitly includes all with implementation status.
- **A.5.21 ICT supply chain (new 2022, CONTESTED):** Supply chain risk management is contested because the adequacy of software component vetting, open-source dependency analysis, and hardware provenance verification is highly context-dependent. ISO 27002:2022 guidance references SCRM practices from NIST SP 800-161 but this is guidance, not a requirement.
- **A.5.23 cloud (new 2022):** This control was added specifically for cloud-hosted ISMS scope. It requires processes for cloud service acquisition, use, management, and exit. The exit strategy requirement (portability, data recovery, encryption key ownership) is often overlooked.
- **A.5.31 legal compliance (CONTESTED):** Legal and regulatory requirements vary by jurisdiction, industry, and data type. The adequacy of the regulatory inventory is auditor-evaluated — organizations must demonstrate they have identified all applicable requirements, not just the obvious ones. Data protection law, sector-specific rules, and contractual obligations all count.
- **A.5.17 vs. PCI DSS Req 8:** The thresholds in ASSUME-ISO-A5-004 align with PCI DSS Req 8.3.6 (12-character minimum, alphanumeric required). Using PCI DSS password policy satisfies ISO 27001 A.5.17 when both frameworks apply.
