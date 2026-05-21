# COPPA — Children's Online Privacy Protection Act

**Framework:** COPPA Rule, 16 CFR Part 312 (2013 amendments)
**Clauses:** §312.4 (privacy notice), §312.5 (verifiable parental consent), §312.6 (parental rights), §312.7 (confidentiality and disclosure), §312.8 (data security), §312.10 (retention and deletion), §312.11 (safe harbor programs)
**Confidence:** DETERMINISTIC-dominant (notice elements, consent requirements, parental rights, retention, security obligations); PARAMETERIZED/CONTESTED ("directed to children" scope determination, mixed-audience classification)
**Last parsed:** 2026-05-21
**Applies to:** Operators of commercial websites, online services, and mobile apps (1) directed to children under 13, OR (2) with actual knowledge they are collecting personal information from children under 13
**Trigger:** Site or service 'directed to children' (determined by content, advertising, music, animated characters, celebrities appealing to children, etc.); OR actual knowledge of under-13 users through age gate failures, user self-disclosure, or parent notifications
**Jurisdiction:** United States; extraterritorial reach — applies to foreign operators targeting US children; enforced by FTC under 16 CFR Part 312
**Not applicable to:** Non-commercial websites and services; general audience services with no child-directed content and no actual knowledge of under-13 users; educational institutions using the school-authority exception; services exclusively for persons 13 and older with credible age verification

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def coppa_scope(entity_profile: dict):
    if not entity_profile.get("coppa_operator", False):
        pytest.skip("COPPA not applicable — not a COPPA-covered operator")
```

---

## Constants

```python
from datetime import date

# §312.4(c) — required elements in the online privacy notice
COPPA_PRIVACY_NOTICE_REQUIRED_ELEMENTS = frozenset({
    "name_address_phone_email_of_all_operators",
    "types_of_personal_information_collected_from_children",
    "how_personal_information_is_used",
    "third_party_disclosure_description_and_categories",
    "parental_right_to_review_pi",
    "parental_right_to_delete_pi",
    "parental_right_to_refuse_further_collection",
    "parent_can_consent_without_allowing_third_party_disclosure",
})

# FTC-approved verifiable parental consent methods (§312.5(b))
COPPA_APPROVED_VPC_METHODS = frozenset({
    "signed_form_mail_or_fax",
    "credit_debit_card_transaction_with_notification",
    "toll_free_phone_call_with_trained_personnel",
    "video_conference",
    "government_id_with_verification",
    "email_plus_limited_to_internal_use_only",
})

# §312.10 — operators may not retain PI longer than reasonably necessary
# No fixed number of days — retention limitation is purpose-based (DETERMINISTIC obligation; period is PARAMETERIZED)
```

---

## Scope Determination — "Directed to Children" (§312.2)

**Overall: CONTESTED/PARAMETERIZED — Pattern 2/3**

```python
class TestCOPPAScopeDetermination:
    """COPPA §312.2 — Operator classification as 'directed to children' must be documented; mixed-audience age-screen."""

    @pytest.mark.assumption(
        id="ASSUME-COPPA-SCOPE-001",
        description=(
            "The 'directed to children' classification is a multi-factor FTC analysis: "
            "subject matter, visual content, music, animated characters, celebrities popular "
            "with children, age of intended audience, whether child-oriented activities are "
            "offered, and age composition of actual user base; for mixed-audience sites the "
            "operator may age-screen and apply COPPA only to under-13 segment; adequacy of "
            "the classification analysis is PARAMETERIZED — documentation of the analysis "
            "and classification decision is DETERMINISTIC"
        ),
        approved_by="privacy_counsel",
        review_date="2027-05-21",
    )
    def test_coppa_scope_classification_documented(self, controls_evidence: dict):
        coppa = controls_evidence.get("coppa", {})
        assert coppa.get("scope_classification_documented", False), (
            "The determination of whether the service is 'directed to children' or "
            "whether the operator has 'actual knowledge' of under-13 users must be "
            "documented (COPPA Rule §312.2 + FTC guidance)"
        )

    def test_mixed_audience_sites_implement_age_screen(self, controls_evidence: dict):
        coppa = controls_evidence.get("coppa", {})
        if not coppa.get("mixed_audience_site", False):
            return
        assert coppa.get("age_screen_mechanism_in_place", False), (
            "Mixed-audience sites must implement a neutral age screen to identify "
            "under-13 users and apply COPPA only to that segment (FTC guidance / §312.2)"
        )
```

---

## Online Privacy Notice (§312.4)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestPrivacyNotice:
    """COPPA §312.4 — Online privacy notice posted; all 8 required elements present; direct notice to parent."""

    def test_online_privacy_notice_posted_on_service(self, controls_evidence: dict):
        coppa = controls_evidence.get("coppa", {})
        assert coppa.get("online_privacy_notice_posted", False), (
            "A clear and understandable online privacy notice must be posted on the "
            "homepage and at each area of the site where personal information is "
            "collected from children (COPPA Rule §312.4(a))"
        )

    def test_privacy_notice_contains_all_required_elements(
        self, controls_evidence: dict
    ):
        coppa = controls_evidence.get("coppa", {})
        present = set(coppa.get("privacy_notice_elements_present", []))
        missing = COPPA_PRIVACY_NOTICE_REQUIRED_ELEMENTS - present
        assert not missing, (
            f"Online privacy notice is missing required elements: {missing} "
            f"(COPPA Rule §312.4(c))"
        )

    def test_direct_notice_sent_to_parent_before_collection(
        self, controls_evidence: dict
    ):
        coppa = controls_evidence.get("coppa", {})
        assert coppa.get("direct_notice_to_parent_mechanism_in_place", False), (
            "Before collecting personal information from a child, the operator must "
            "send a direct notice to the child's parent (COPPA Rule §312.4(b))"
        )

    def test_direct_notice_contains_required_content(self, controls_evidence: dict):
        coppa = controls_evidence.get("coppa", {})
        assert coppa.get("direct_notice_content_complete", False), (
            "Direct notice to parent must describe: what PI is collected, how it is "
            "used, and whether it is disclosed to third parties, and provide the "
            "operator's contact information (COPPA Rule §312.4(b))"
        )
```

---

## Verifiable Parental Consent (§312.5)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestVerifiableParentalConsent:
    """COPPA §312.5 — VPC obtained before any PI collection, use, or disclosure; method is FTC-approved."""

    def test_verifiable_parental_consent_obtained_before_collection(
        self, controls_evidence: dict
    ):
        coppa = controls_evidence.get("coppa", {})
        assert coppa.get("vpc_obtained_before_collection", False), (
            "Verifiable parental consent must be obtained before any collection, "
            "use, or disclosure of personal information from a child under 13 "
            "(COPPA Rule §312.5(a))"
        )

    def test_vpc_method_is_ftc_approved(self, controls_evidence: dict):
        coppa = controls_evidence.get("coppa", {})
        vpc_method = coppa.get("vpc_method_used")
        assert vpc_method in COPPA_APPROVED_VPC_METHODS, (
            f"VPC method '{vpc_method}' is not an FTC-approved consent method. "
            f"Approved methods: {COPPA_APPROVED_VPC_METHODS} "
            f"(COPPA Rule §312.5(b))"
        )

    def test_vpc_records_retained(self, controls_evidence: dict):
        coppa = controls_evidence.get("coppa", {})
        assert coppa.get("vpc_records_retained", False), (
            "Records of verifiable parental consent must be retained to demonstrate "
            "compliance (COPPA Rule §312.5)"
        )

    def test_no_collection_before_vpc_for_existing_child_users(
        self, controls_evidence: dict
    ):
        child_accounts = controls_evidence.get("coppa_child_accounts", [])
        no_consent = [
            a for a in child_accounts
            if not a.get("vpc_obtained", False)
            and a.get("pi_collected", False)
        ]
        assert not no_consent, (
            f"PI must not be collected from child accounts without verifiable "
            f"parental consent (COPPA Rule §312.5). Accounts without consent: "
            f"{[a['account_id'] for a in no_consent]}"
        )
```

---

## Parental Rights (§312.6)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestParentalRights:
    """COPPA §312.6 — Mechanisms for parents to review, delete PI, and opt out of future collection."""

    def test_parental_right_to_review_pi_implemented(self, controls_evidence: dict):
        coppa = controls_evidence.get("coppa", {})
        assert coppa.get("parental_review_mechanism_in_place", False), (
            "Operators must provide parents with the ability to review personal "
            "information collected from their child (COPPA Rule §312.6(a)(2))"
        )

    def test_parental_right_to_delete_pi_implemented(self, controls_evidence: dict):
        coppa = controls_evidence.get("coppa", {})
        assert coppa.get("parental_deletion_mechanism_in_place", False), (
            "Operators must provide parents with the ability to refuse further "
            "collection and require deletion of their child's personal information "
            "(COPPA Rule §312.6(a)(2))"
        )

    def test_parental_requests_for_deletion_honored(self, controls_evidence: dict):
        deletion_requests = controls_evidence.get("coppa_parental_deletion_requests", [])
        not_honored = [
            r for r in deletion_requests
            if not r.get("deletion_completed", False)
        ]
        assert not not_honored, (
            f"Parental requests for deletion of child PI must be honored "
            f"(COPPA Rule §312.6). Not completed: "
            f"{[r['request_id'] for r in not_honored]}"
        )

    def test_operator_does_not_require_excess_information(
        self, controls_evidence: dict
    ):
        coppa = controls_evidence.get("coppa", {})
        assert not coppa.get("requires_more_pi_than_reasonably_necessary", False), (
            "Operators may not require children to disclose more personal information "
            "than is reasonably necessary to participate in the activity "
            "(COPPA Rule §312.7)"
        )
```

---

## Data Security (§312.8)

**Overall: DETERMINISTIC (written procedures exist); PARAMETERIZED (adequacy)**

```python
class TestDataSecurity:
    """COPPA §312.8 — Reasonable written security procedures for PI collected from children."""

    def test_written_security_procedures_exist(self, controls_evidence: dict):
        coppa = controls_evidence.get("coppa", {})
        assert coppa.get("written_security_procedures_exist", False), (
            "Operators must establish and maintain reasonable procedures to protect "
            "the confidentiality, security, and integrity of personal information "
            "collected from children; security procedures must be written "
            "(COPPA Rule §312.8)"
        )

    def test_third_party_service_providers_with_child_pi_have_security_obligations(
        self, controls_evidence: dict
    ):
        coppa = controls_evidence.get("coppa", {})
        assert coppa.get("third_party_service_providers_contractually_bound", False), (
            "Third-party service providers that receive children's PI must be "
            "contractually bound to provide comparable security protections "
            "(COPPA Rule §312.8)"
        )
```

---

## Retention and Deletion (§312.10)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestRetentionAndDeletion:
    """COPPA §312.10 — PI retained only as long as necessary for purpose; deleted securely thereafter."""

    def test_retention_period_defined_per_purpose(self, controls_evidence: dict):
        coppa = controls_evidence.get("coppa", {})
        assert coppa.get("retention_periods_defined_for_child_pi", False), (
            "Operators must retain personal information collected from children only "
            "as long as is reasonably necessary to fulfill the purpose for which the "
            "information was collected (COPPA Rule §312.10)"
        )

    def test_pi_deleted_when_no_longer_necessary(self, controls_evidence: dict):
        coppa = controls_evidence.get("coppa", {})
        assert coppa.get("deletion_process_for_expired_child_pi_in_place", False), (
            "A process must exist to delete children's PI when it is no longer "
            "necessary (COPPA Rule §312.10) — deletion must render PI unreadable "
            "and unrecoverable"
        )
```

---

## COPPA Safe Harbor (§312.11) — optional

```python
class TestCOPPASafeHarbor:
    """COPPA §312.11 — If relying on FTC-approved safe harbor program, membership must be current and annual review passed."""

    @pytest.fixture(autouse=True)
    def safe_harbor_scope(self, entity_profile: dict):
        if not entity_profile.get("coppa_safe_harbor_member", False):
            pytest.skip("Not relying on COPPA safe harbor program")

    def test_safe_harbor_membership_is_current(
        self, controls_evidence: dict, reference_date: date
    ):
        coppa = controls_evidence.get("coppa", {})
        membership_expiry = coppa.get("safe_harbor_membership_expiry")
        assert membership_expiry is not None and membership_expiry >= reference_date, (
            f"COPPA safe harbor program membership must be current. "
            f"Expiry: {membership_expiry} (COPPA Rule §312.11)"
        )

    def test_safe_harbor_annual_review_passed(self, controls_evidence: dict):
        coppa = controls_evidence.get("coppa", {})
        assert coppa.get("safe_harbor_annual_review_passed", False), (
            "Annual review by the FTC-approved safe harbor program must have been "
            "passed (COPPA Rule §312.11)"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-COPPA-SCOPE-001 | §312.2 | "Directed to children" classification is a multi-factor FTC analysis: PARAMETERIZED (adequacy); documentation of classification decision: DETERMINISTIC | 2027-05-21 |
