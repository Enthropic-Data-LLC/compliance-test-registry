# APPI — Act on the Protection of Personal Information (Japan, 2022 Amendment)

**Framework:** APPI as amended by 2020 Act No. 44 (effective April 2022)
**Clauses:** Art. 17–18 (purpose specification), Art. 20 (sensitive PI consent), Art. 23–26 (security management, employee/subcontractor supervision), Art. 27–29 (third-party provision + opt-out registration + records), Art. 26 (breach notification), Arts. 33–39 (data subject rights)
**Confidence:** DETERMINISTIC-dominant (breach notification deadlines, sensitive PI consent, third-party provision records, DSR response deadlines, opt-out registration); PARAMETERIZED (security management measures scale/content)
**Last parsed:** 2026-05-21
**Applies to:** Business operators handling personal information in Japan; foreign businesses that provide goods or services to persons in Japan or use personal information of persons in Japan — regardless of where the business is located
**Trigger:** Handling personal information of persons in Japan in the course of business; providing goods or services targeting Japan; 2022 amendment removed the 5,000-person threshold — now applies to all business operators handling any personal information
**Jurisdiction:** Japan; extraterritorial reach for foreign businesses targeting Japanese persons; enforced by Personal Information Protection Commission (PPC); sector-specific guidelines from FSA (financial), MHLW (healthcare), METI (general industry)
**Not applicable to:** Government agencies (separate Act on Protection of Personal Information Held by Administrative Organs); purely personal or family use with no commercial purpose; anonymous information that is irreversibly de-identified (outside APPI definition of personal information); academic research with appropriate safeguards (limited exemption)

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def appi_scope(entity_profile: dict):
    if not entity_profile.get("appi_in_scope", False):
        pytest.skip("APPI not in scope")
```

---

## Constants

```python
from datetime import date, timedelta

# Breach notification deadlines (Art. 26 — 2022 amendment)
APPI_BREACH_PPC_INITIAL_REPORT_DAYS = 5      # "promptly" — within approx. 3–5 days
APPI_BREACH_PPC_FINAL_REPORT_DAYS = 30       # full report within 30 days of discovery
# Individual notification: "without delay" — no fixed number of days

# Data subject rights response deadlines (Art. 33)
APPI_DSR_RESPONSE_DAYS = 14  # 2 weeks for disclosure requests

# Third-party provision records
APPI_THIRD_PARTY_PROVISION_RECORD_RETENTION_YEARS = 3
APPI_THIRD_PARTY_RECEIPT_RECORD_RETENTION_YEARS = 1

# Notifiable breach triggers (Art. 26)
APPI_BREACH_NOTIFICATION_REQUIRED_TRIGGERS = frozenset({
    "sensitive_pi_leaked",
    "leak_likely_to_harm_individual_rights_and_interests",
    "fraudulent_access_with_pi_leakage",
    "large_scale_leakage_1000_or_more_individuals",
})
```

---

## Purpose Specification and Notification (Arts. 17–18)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestPurposeSpecification:
    """APPI Art. 17–18 — Purpose of use specified; disclosed at time of collection; change within reasonably expected scope."""

    def test_purpose_of_use_specified_to_extent_possible(
        self, controls_evidence: dict
    ):
        appi = controls_evidence.get("appi", {})
        assert appi.get("purpose_of_use_specified_for_all_pi_categories", False), (
            "The purpose of use of personal information must be specified to the "
            "extent possible for each category of personal information "
            "(APPI Art. 17)"
        )

    def test_purpose_notified_or_publicly_announced_at_collection(
        self, controls_evidence: dict
    ):
        appi = controls_evidence.get("appi", {})
        assert appi.get("purpose_notified_at_or_before_collection", False), (
            "When acquiring personal information, the business operator must promptly "
            "notify the individual of the purpose of use, or publicly announce it in "
            "advance (APPI Art. 18)"
        )

    def test_purpose_change_within_reasonably_expected_scope(
        self, controls_evidence: dict
    ):
        purpose_changes = controls_evidence.get("appi_purpose_changes", [])
        out_of_scope = [
            c for c in purpose_changes
            if not c.get("within_reasonably_expected_scope", False)
            and not c.get("new_consent_obtained", False)
        ]
        assert not out_of_scope, (
            f"Purpose of use may be changed only within a scope reasonably expected "
            f"by the individual; otherwise new consent or notification is required "
            f"(APPI Art. 17(2)). Violations: "
            f"{[c['change_id'] for c in out_of_scope]}"
        )
```

---

## Sensitive Personal Information (Art. 20)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestSensitivePersonalInformation:
    """APPI Art. 20 — Prior opt-in consent required before acquiring sensitive personal information."""

    def test_prior_opt_in_consent_obtained_for_sensitive_pi(
        self, controls_evidence: dict
    ):
        appi = controls_evidence.get("appi", {})
        if not appi.get("sensitive_pi_acquired", False):
            return
        assert appi.get("prior_opt_in_consent_for_sensitive_pi", False), (
            "Prior opt-in consent of the individual must be obtained before acquiring "
            "sensitive personal information (race, creed, social status, medical "
            "history, criminal record, disabilities, etc.) "
            "(APPI Art. 20)"
        )

    def test_sensitive_pi_consent_records_retained(self, controls_evidence: dict):
        appi = controls_evidence.get("appi", {})
        if not appi.get("sensitive_pi_acquired", False):
            return
        assert appi.get("sensitive_pi_consent_records_retained", False), (
            "Records of opt-in consent for sensitive personal information must be "
            "retained to demonstrate compliance (APPI Art. 20)"
        )
```

---

## Security Management Measures (Art. 23)

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestSecurityManagementMeasures:
    """APPI Art. 23 — Security management measures appropriate to scale and nature of PI handling; PPC guidelines applied."""

    @pytest.mark.assumption(
        id="ASSUME-APPI-SECURITY-001",
        description=(
            "Security management measures (安全管理措置) must be appropriate to the "
            "number of individuals whose PI is handled and the nature of the information; "
            "PPC guidelines specify 4 dimensions: organizational, human, physical, and "
            "technical measures; SMEs with <100 individuals may use simplified measures; "
            "adequacy of measures is PARAMETERIZED — documented security policy and "
            "measures existence is DETERMINISTIC"
        ),
        approved_by="privacy_officer",
        review_date="2027-05-21",
    )
    def test_security_management_measures_documented(self, controls_evidence: dict):
        appi = controls_evidence.get("appi", {})
        assert appi.get("security_management_measures_documented", False), (
            "Security management measures (organizational, human, physical, technical) "
            "must be documented and implemented appropriately for the scale and nature "
            "of personal information handling (APPI Art. 23 + PPC guidelines)"
        )

    def test_employee_supervision_implemented(self, controls_evidence: dict):
        appi = controls_evidence.get("appi", {})
        assert appi.get("employee_supervision_measures_documented", False), (
            "Necessary and appropriate supervision must be exercised over employees "
            "who handle personal information (APPI Art. 24)"
        )

    def test_entrustee_subcontractor_supervision_implemented(
        self, controls_evidence: dict
    ):
        appi = controls_evidence.get("appi", {})
        if not appi.get("personal_data_handling_outsourced", False):
            return
        assert appi.get("entrustee_supervision_contractually_required", False), (
            "When entrusting the handling of personal information to a third party, "
            "necessary and appropriate supervision over the entrustee must be exercised, "
            "including contractual security obligations (APPI Art. 25)"
        )
```

---

## Third-Party Provision (Arts. 27–28)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestThirdPartyProvision:
    """APPI Art. 27 — Prior consent required for third-party provision; opt-out provision requires PPC registration."""

    def test_prior_consent_obtained_for_third_party_provision(
        self, controls_evidence: dict
    ):
        provisions = controls_evidence.get("appi_third_party_provisions", [])
        no_consent = [
            p for p in provisions
            if not p.get("prior_consent_obtained", False)
            and not p.get("opt_out_registered_with_ppc", False)
            and not p.get("exception_applies", False)
        ]
        assert not no_consent, (
            f"Personal data must not be provided to a third party without the "
            f"individual's prior consent, unless an opt-out is registered with the "
            f"PPC or a statutory exception applies (APPI Art. 27). "
            f"Violations: {[p['provision_id'] for p in no_consent]}"
        )

    def test_opt_out_provisions_registered_with_ppc_before_first_provision(
        self, controls_evidence: dict
    ):
        provisions = controls_evidence.get("appi_third_party_provisions", [])
        opt_out_provisions = [
            p for p in provisions
            if p.get("opt_out_registered_with_ppc", False)
        ]
        not_pre_registered = [
            p for p in opt_out_provisions
            if not p.get("ppc_registration_before_first_provision", False)
        ]
        assert not not_pre_registered, (
            f"Opt-out third-party provision must be registered with the PPC before "
            f"the first provision occurs (APPI Art. 27(2)). "
            f"Not pre-registered: {[p['provision_id'] for p in not_pre_registered]}"
        )

    def test_sensitive_pi_not_provided_via_opt_out(self, controls_evidence: dict):
        provisions = controls_evidence.get("appi_third_party_provisions", [])
        opt_out_with_sensitive = [
            p for p in provisions
            if p.get("opt_out_registered_with_ppc", False)
            and p.get("includes_sensitive_pi", False)
        ]
        assert not opt_out_with_sensitive, (
            f"Sensitive personal information may not be provided to third parties "
            f"via the opt-out mechanism — prior consent is always required "
            f"(APPI Art. 27(2)). Violations: "
            f"{[p['provision_id'] for p in opt_out_with_sensitive]}"
        )
```

---

## Third-Party Provision Records (Art. 29)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestThirdPartyProvisionRecords:
    """APPI Art. 29 — Provision records (3 years) and receipt records (1 year) maintained."""

    def test_third_party_provision_records_maintained(self, controls_evidence: dict):
        appi = controls_evidence.get("appi", {})
        if not appi.get("personal_data_provided_to_third_parties", False):
            return
        assert appi.get("third_party_provision_records_maintained", False), (
            "Records of third-party provision of personal data must be maintained "
            "(APPI Art. 29(1))"
        )

    def test_third_party_provision_record_retention_period(
        self, controls_evidence: dict
    ):
        provision_records = controls_evidence.get("appi_provision_records", [])
        for record in provision_records:
            retention_years = record.get("retention_years")
            if retention_years is not None:
                assert retention_years >= APPI_THIRD_PARTY_PROVISION_RECORD_RETENTION_YEARS, (
                    f"Third-party provision record '{record['record_id']}' must be "
                    f"retained for at least {APPI_THIRD_PARTY_PROVISION_RECORD_RETENTION_YEARS} "
                    f"years (APPI Art. 29)"
                )

    def test_third_party_receipt_records_maintained(self, controls_evidence: dict):
        appi = controls_evidence.get("appi", {})
        if not appi.get("personal_data_received_from_third_parties", False):
            return
        assert appi.get("third_party_receipt_records_maintained", False), (
            "Records of receipt of personal data from third parties must be "
            "maintained (APPI Art. 30)"
        )

    def test_third_party_receipt_record_retention_period(
        self, controls_evidence: dict
    ):
        receipt_records = controls_evidence.get("appi_receipt_records", [])
        for record in receipt_records:
            retention_years = record.get("retention_years")
            if retention_years is not None:
                assert retention_years >= APPI_THIRD_PARTY_RECEIPT_RECORD_RETENTION_YEARS, (
                    f"Third-party receipt record '{record['record_id']}' must be "
                    f"retained for at least {APPI_THIRD_PARTY_RECEIPT_RECORD_RETENTION_YEARS} "
                    f"year (APPI Art. 30)"
                )
```

---

## Breach Notification (Art. 26 — 2022 Amendment)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestBreachNotification:
    """APPI Art. 26 — PPC notified promptly (3–5 days); final report within 30 days; individuals notified without delay."""

    def test_notifiable_breach_triggers_identified(self, controls_evidence: dict):
        incidents = controls_evidence.get("appi_security_incidents", [])
        for incident in incidents:
            for trigger in APPI_BREACH_NOTIFICATION_REQUIRED_TRIGGERS:
                if incident.get(f"trigger_{trigger}", False):
                    assert incident.get("breach_notification_required_flag", False), (
                        f"Incident '{incident['incident_id']}' meets breach notification "
                        f"trigger '{trigger}' but has not been flagged for PPC notification "
                        f"(APPI Art. 26)"
                    )

    def test_ppc_initial_report_within_5_days_of_discovery(
        self, controls_evidence: dict
    ):
        breaches = controls_evidence.get("appi_notifiable_breaches", [])
        for breach in breaches:
            discovery_date = breach.get("discovery_date")
            initial_report_date = breach.get("ppc_initial_report_date")
            if discovery_date is None or initial_report_date is None:
                continue
            days = (initial_report_date - discovery_date).days
            assert days <= APPI_BREACH_PPC_INITIAL_REPORT_DAYS, (
                f"Breach '{breach['breach_id']}' PPC initial report submitted {days} days "
                f"after discovery, exceeding the {APPI_BREACH_PPC_INITIAL_REPORT_DAYS}-day "
                f"'promptly' requirement (APPI Art. 26)"
            )

    def test_ppc_final_report_within_30_days_of_discovery(
        self, controls_evidence: dict
    ):
        breaches = controls_evidence.get("appi_notifiable_breaches", [])
        for breach in breaches:
            discovery_date = breach.get("discovery_date")
            final_report_date = breach.get("ppc_final_report_date")
            if discovery_date is None or final_report_date is None:
                continue
            days = (final_report_date - discovery_date).days
            assert days <= APPI_BREACH_PPC_FINAL_REPORT_DAYS, (
                f"Breach '{breach['breach_id']}' PPC final report submitted {days} days "
                f"after discovery, exceeding the {APPI_BREACH_PPC_FINAL_REPORT_DAYS}-day "
                f"limit (APPI Art. 26)"
            )

    def test_individuals_notified_without_delay(self, controls_evidence: dict):
        breaches = controls_evidence.get("appi_notifiable_breaches", [])
        not_notified = [
            b for b in breaches
            if not b.get("individuals_notified", False)
        ]
        assert not not_notified, (
            f"Affected individuals must be notified 'without delay' when a notifiable "
            f"breach occurs (APPI Art. 26). Not notified: "
            f"{[b['breach_id'] for b in not_notified]}"
        )
```

---

## Data Subject Rights (Arts. 33–39)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestDataSubjectRights:
    """APPI Arts. 33–39 — Disclosure requests responded to within 2 weeks; correction/cessation without delay."""

    def test_disclosure_requests_responded_within_2_weeks(
        self, controls_evidence: dict
    ):
        dsr_requests = controls_evidence.get("appi_dsr_requests", [])
        disclosure_requests = [
            r for r in dsr_requests
            if r.get("request_type") == "disclosure"
        ]
        for request in disclosure_requests:
            request_date = request.get("request_date")
            response_date = request.get("response_date")
            if request_date is None or response_date is None:
                continue
            days = (response_date - request_date).days
            assert days <= APPI_DSR_RESPONSE_DAYS, (
                f"Disclosure request '{request['request_id']}' responded to in {days} days, "
                f"exceeding the {APPI_DSR_RESPONSE_DAYS}-day limit "
                f"(APPI Art. 33)"
            )

    def test_correction_requests_responded_without_delay(
        self, controls_evidence: dict
    ):
        dsr_requests = controls_evidence.get("appi_dsr_requests", [])
        correction_requests = [
            r for r in dsr_requests
            if r.get("request_type") in ("correction", "addition", "deletion")
        ]
        not_actioned = [
            r for r in correction_requests
            if not r.get("action_taken_without_delay", False)
        ]
        assert not not_actioned, (
            f"Correction, addition, and deletion requests must be responded to "
            f"'without delay' (APPI Art. 34). Not actioned: "
            f"{[r['request_id'] for r in not_actioned]}"
        )

    def test_cessation_of_use_requests_responded_without_delay(
        self, controls_evidence: dict
    ):
        dsr_requests = controls_evidence.get("appi_dsr_requests", [])
        cessation_requests = [
            r for r in dsr_requests
            if r.get("request_type") in ("cessation_of_use", "erasure", "cessation_of_third_party_provision")
        ]
        not_actioned = [
            r for r in cessation_requests
            if not r.get("action_taken_without_delay", False)
        ]
        assert not not_actioned, (
            f"Cessation of use, erasure, and cessation of third-party provision "
            f"requests must be actioned 'without delay' (APPI Arts. 35–36). "
            f"Not actioned: {[r['request_id'] for r in not_actioned]}"
        )

    def test_dsr_mechanism_accessible_to_individuals(self, controls_evidence: dict):
        appi = controls_evidence.get("appi", {})
        assert appi.get("dsr_submission_mechanism_accessible", False), (
            "A mechanism for individuals to submit data subject rights requests "
            "must be accessible and clearly communicated (APPI Arts. 33–39)"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-APPI-SECURITY-001 | Art. 23 | Security management measures adequacy: PARAMETERIZED (scale/nature-dependent); documented security measures existence: DETERMINISTIC | 2027-05-21 |
