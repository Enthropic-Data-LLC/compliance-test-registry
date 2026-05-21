# Requirement 7 — Restrict Access to System Components and Cardholder Data by Business Need to Know

**Registry path:** `/regulation-registry/PCI-DSS/Req-7/`
**Version:** PCI DSS v4.0 (mandatory since March 31, 2025)
**Last parsed:** 2026-05-20
**Applies to:** Any organization that stores, processes, or transmits payment card data — merchants of all levels, payment processors, acquirers, issuers, and service providers in the card payment ecosystem
**Trigger:** Participation in the card payment ecosystem; card brand contracts (Visa, Mastercard, Amex, Discover, UnionPay); acquiring bank contractual requirement; SAQ level determined by annual transaction volume
**Jurisdiction:** Global — enforced by card brands (Visa/Mastercard/Amex/Discover) and acquiring banks; no geographic restriction
**Not applicable to:** Organizations that never handle cardholder data and fully outsource all card processing to a PCI-DSS-compliant third party; SAQ A merchants processing only redirected card transactions
**Overall confidence:** HIGH — 6-month access review cadence and default-deny are DETERMINISTIC; need-to-know scope definition is PARAMETERIZED
**R = Required**

---

## Scope summary

Req 7 is the access control restriction requirement. Its core principle is least privilege: users and systems receive only the access necessary for their defined job function. Two DETERMINISTIC anchors dominate: the 6-month access rights review cadence and the default-deny access control posture. The PARAMETERIZED surface is the "business need to know" determination — defining what each role legitimately needs is an organization-specific judgment.

---

## 7.2.1 — Least Privilege (R — PARAMETERIZED)

### Source excerpt

> *7.2.1 — An access control model is defined and includes granting of access as follows: Appropriate access depending on the entity's business and access needs. Access to system components and data resources that is based on users' job classification and functions. The least privileges necessary to perform job functions.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All users and system processes accessing CDE | DETERMINISTIC |
| Condition | Access is granted to any CDE system or data | PARAMETERIZED |
| Obligation | Access limited to minimum required for job function; access control model documented | PARAMETERIZED |
| Evidence | `access_control_model.documented == true`; role definitions with associated access levels | PARAMETERIZED |

**Assumption (ASSUME-7-001):** Least privilege is adequately implemented when: (1) a role-based access control (RBAC) model is defined with distinct roles for each job function; (2) each role has documented access entitlements at the system and data level; (3) users are assigned roles, not individual permissions; (4) elevated privileges (admin, root, DBA) are separate roles with additional approval requirements; (5) role definitions are reviewed annually or when job functions change.

**Overall: PARAMETERIZED → Pattern 2**

---

## 7.2.4 — Access Rights Review (R — DETERMINISTIC)

### Source excerpt

> *7.2.4 — All user accounts and related access privileges are reviewed at least once every six months to confirm that access and privileges are appropriate and that those that are no longer appropriate are removed.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All user accounts with CDE access | DETERMINISTIC |
| Condition | Account exists and has CDE access | DETERMINISTIC |
| Obligation | Formal access review ≤ 180 days; inappropriate access removed as a result | DETERMINISTIC |
| Evidence | `access_review_records.review_date`; `access_review_records.accounts_reviewed_count`; `inappropriate_access_removed == true` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 7.2.5 — Application and System Account Access Review (R — DETERMINISTIC)

### Source excerpt

> *7.2.5.1 — All access by application and system accounts and related access privileges are reviewed at least once every six months to confirm that access and privileges are appropriate.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All application and system accounts with CDE access | DETERMINISTIC |
| Condition | Service/application account exists with CDE access | DETERMINISTIC |
| Obligation | Service account access review ≤ 180 days | DETERMINISTIC |
| Evidence | `service_account_review_records.review_date`; `review_interval_days <= 180` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 7.3.3 — Default Deny (R — DETERMINISTIC)

### Source excerpt

> *7.3.3 — Access control systems are set to "deny-all" by default.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All access control systems governing CDE access | DETERMINISTIC |
| Condition | Access control system in use | DETERMINISTIC |
| Obligation | Default posture is deny-all; access is explicitly granted, never implicitly inherited | DETERMINISTIC |
| Evidence | `access_control_config.default_policy == "deny"` for all CDE systems | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## YAML specifications

### `req7_access_review.yaml`

```yaml
regulation_id: PCI-DSS-v4.0-7.2.4
section: "PCI DSS v4.0 — Access Rights Review"
r_or_a: Required
source_text: >
  All user accounts and related access privileges are reviewed at least
  once every six months to confirm access and privileges are appropriate.

extracted_elements:
  subject: "All user accounts with CDE access"
  condition: "Account exists with CDE access"
  obligation: "Formal access review ≤ 180 days; inappropriate access removed"
  evidence: "access_review_records: review_date, accounts_reviewed, inappropriate_removed"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log: []
test_confidence: HIGH
generated_test: "tests/req7/test_7_2_access_review.py"
```

---

## Generated tests

### `tests/req7/test_7_2_access_review.py`

```python
"""
PCI DSS v4.0 Req 7.2 — Access Rights Review
Confidence: HIGH for cadence; MEDIUM for scope definition
"""
import pytest
from datetime import date

ACCESS_REVIEW_MAX_DAYS = 180


def test_user_access_reviewed_within_6_months(access_review_records):
    """7.2.4 — All user accounts reviewed at least every 6 months."""
    today = date.today()
    user_reviews = [r for r in access_review_records if r.get("review_type") == "user"]
    if not user_reviews:
        assert False, (
            "VIOLATION (7.2.4): No user access review records found — "
            "semi-annual review is required"
        )
    latest = max(user_reviews, key=lambda r: r["review_date"])
    days_since = (today - latest["review_date"]).days
    assert days_since <= ACCESS_REVIEW_MAX_DAYS, (
        f"VIOLATION (7.2.4): Last user access review was {days_since} days ago "
        f"(max {ACCESS_REVIEW_MAX_DAYS})"
    )


def test_service_account_access_reviewed_within_6_months(access_review_records):
    """7.2.5.1 — All service/application accounts reviewed at least every 6 months."""
    today = date.today()
    svc_reviews = [
        r for r in access_review_records
        if r.get("review_type") == "service_account"
    ]
    if not svc_reviews:
        assert False, (
            "VIOLATION (7.2.5.1): No service account access review records found"
        )
    latest = max(svc_reviews, key=lambda r: r["review_date"])
    days_since = (today - latest["review_date"]).days
    assert days_since <= ACCESS_REVIEW_MAX_DAYS, (
        f"VIOLATION (7.2.5.1): Last service account review was {days_since} days ago "
        f"(max {ACCESS_REVIEW_MAX_DAYS})"
    )


def test_inappropriate_access_removed_after_review(access_review_records):
    violations = [
        r for r in access_review_records
        if r.get("inappropriate_access_found")
        and not r.get("inappropriate_access_removed")
    ]
    assert not violations, (
        f"VIOLATION (7.2.4): {len(violations)} access review(s) identified inappropriate "
        f"access that was not removed: "
        f"{[r.get('review_id') for r in violations]}"
    )


def test_default_deny_on_all_cde_systems(cde_access_control_configs):
    """7.3.3 — Default policy must be deny-all on all CDE access controls."""
    violations = [
        c for c in cde_access_control_configs
        if c.get("in_cde") and c.get("default_policy") != "deny"
    ]
    assert not violations, (
        f"VIOLATION (7.3.3): {len(violations)} CDE system(s) without default-deny "
        f"access control policy: "
        f"{[(c['system_id'], c.get('default_policy')) for c in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-7-001",
    description=(
        "Least privilege: RBAC model with documented role entitlements; "
        "elevated privileges require separate role + additional approval; "
        "role definitions reviewed annually."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_access_control_model_documented(access_control_model):
    assert access_control_model, (
        "VIOLATION (7.2.1): No access control model documentation found — "
        "RBAC model with role definitions is required"
    )
    assert access_control_model.get("roles_defined"), (
        "VIOLATION (7.2.1): Access control model exists but no roles are defined"
    )
    assert access_control_model.get("default_access_is_deny"), (
        "VIOLATION (7.3.3): Access control model default is not deny"
    )
```

---

## Notes for the registry

- **6-month review vs. continuous:** The 7.2.4 requirement mandates a formal, documented review every 6 months. Continuous automated access monitoring (PAM tools, SIEM alerts) does not replace the formal review — it supplements it. QSAs will look for a dated, documented review record showing accounts were examined and inappropriate access was removed.
- **Service accounts in access reviews:** 7.2.5.1 (service account review) is frequently overlooked. Application and system accounts accumulate excessive privileges over time — they should be included in the 6-month access review cycle, not just user accounts.
- **Default deny in practice:** For firewall rules, "default deny" means the last rule in the ruleset is "deny all." For application RBAC, "default deny" means new users start with zero access and permissions are explicitly granted. The test should verify both network-layer and application-layer default deny configurations.
- **CHD query access (7.2.6):** A specific v4.0 requirement restricts user access to CHD query repositories (e.g., ability to run ad-hoc SQL queries against a table containing PANs). Only users with a documented, authorized need should have this access, and all query access should be logged.
- **Cross-reference with Req 8:** Req 7 defines what access is granted; Req 8 defines how that access is authenticated. A gap in either breaks the control chain — a user might be properly restricted in Req 7 but still able to use a shared credential to exceed their authorized access if Req 8 shared-account controls are absent.
