# FINRA Broker-Dealer Rules — Supervision, Records, and Customer Protection

**Framework:** FINRA Rules 3110 (supervision), 4510–4530 (books and records), 4311 / SEA Rule 15c3-3 (customer protection), Rule 3310 (AML/BSA), Rule 1010 (registration)
**Clauses:** Rule 3110(a)–(d) (WSPs, annual review, OSJ, principal supervision); Rule 4511 (WORM storage); SEA Rule 17a-3/17a-4 (records retention); SEA Rule 15c3-3 (reserve formula); Rule 3310 (AML program)
**Confidence:** DETERMINISTIC-dominant (retention periods, WSP existence, annual supervisory review, reserve formula weekly, Form U4/U5 30-day deadline, WORM format); PARAMETERIZED (WSP adequacy, supervisory system design, off-channel monitoring sufficiency); CONTESTED (reasonableness of supervisory system — examiner judgment)
**Last parsed:** 2026-05-21
**Applies to:** FINRA-member broker-dealers registered with the SEC under Section 15 of the Securities Exchange Act of 1934; their associated persons (registered representatives, principals, and other individuals subject to FINRA jurisdiction)
**Trigger:** SEC registration as a broker-dealer requires FINRA membership (mandatory for US broker-dealers); FINRA membership agreement subjects firms and their registered persons to FINRA rules
**Jurisdiction:** United States; enforced by FINRA Department of Enforcement; SEC has oversight authority over FINRA as an SRO
**Not applicable to:** Investment advisers registered with the SEC or states (RIA-only, not broker-dealers); commodities futures brokers (CFTC/NFA regulated instead); securities exchanges; banks not also registered as broker-dealers; foreign broker-dealers operating only outside the US

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def finra_scope(entity_profile: dict):
    if not entity_profile.get("finra_member_broker_dealer", False):
        pytest.skip("FINRA rules not applicable — not a FINRA-member broker-dealer")
```

---

## Constants

```python
from datetime import date, timedelta

# Books and records retention periods
FINRA_ELECTRONIC_RECORDS_RETENTION_YEARS = 3
FINRA_GENERAL_RECORDS_RETENTION_YEARS = 6     # Blotters, ledgers, customer accounts
FINRA_CUSTOMER_COMPLAINTS_RETENTION_YEARS = 4
FINRA_ORDER_TICKETS_RETENTION_YEARS = 3
FINRA_WSP_RETENTION_YEARS_AFTER_SUPERSEDED = 3

# Registration and supervisory timelines
FINRA_U4_U5_MATERIAL_CHANGE_FILING_DAYS = 30
FINRA_ANNUAL_SUPERVISORY_REVIEW_INTERVAL_MONTHS = 12

# Customer protection reserve formula
FINRA_RESERVE_FORMULA_FREQUENCY = "weekly"

# Off-channel communications — required records coverage
FINRA_BUSINESS_COMMUNICATION_CHANNELS_REQUIRING_CAPTURE = frozenset({
    "email",
    "text_sms",
    "instant_messaging",
    "social_media_business_use",
})
```

---

## Written Supervisory Procedures (Rule 3110)

**Overall: DETERMINISTIC (WSPs exist, annual review, OSJ designated) + CONTESTED (reasonableness)**

```python
class TestWrittenSupervisoryProcedures:
    """Rule 3110 — WSPs established, maintained, and updated; annual review documented; OSJ designated."""

    def test_written_supervisory_procedures_exist(self, controls_evidence: dict):
        finra = controls_evidence.get("finra", {})
        assert finra.get("written_supervisory_procedures_exist", False), (
            "Written supervisory procedures (WSPs) must be established and "
            "maintained — this is the foundational Rule 3110 requirement and "
            "the first document requested in any FINRA examination "
            "(FINRA Rule 3110(a))"
        )

    def test_wsps_cover_all_lines_of_business(self, controls_evidence: dict):
        finra = controls_evidence.get("finra", {})
        assert finra.get("wsps_cover_all_product_lines_and_business_activities", False), (
            "WSPs must address supervision of all business lines, product types, "
            "and associated persons — gaps in coverage are a common FINRA finding "
            "(FINRA Rule 3110(b))"
        )

    def test_annual_supervisory_review_documented(
        self, controls_evidence: dict, reference_date: date
    ):
        finra = controls_evidence.get("finra", {})
        last_review = finra.get("annual_supervisory_review_last_completed")
        assert last_review is not None, (
            "Annual review of the supervisory system must be conducted; "
            "no completion date on record (FINRA Rule 3110(a))"
        )
        cutoff = reference_date - timedelta(
            days=FINRA_ANNUAL_SUPERVISORY_REVIEW_INTERVAL_MONTHS * 30
        )
        assert last_review >= cutoff, (
            f"Annual supervisory review must be completed within the past 12 months. "
            f"Last completed: {last_review} (FINRA Rule 3110(a))"
        )

    def test_osj_offices_designated_with_registered_principals(
        self, controls_evidence: dict
    ):
        finra = controls_evidence.get("finra", {})
        assert finra.get("osj_offices_designated_with_registered_principals", False), (
            "Each Office of Supervisory Jurisdiction (OSJ) must be designated "
            "and supervised by a registered principal "
            "(FINRA Rule 3110(d))"
        )

    def test_named_supervisory_principal_per_product_line(
        self, controls_evidence: dict
    ):
        finra = controls_evidence.get("finra", {})
        assert finra.get("named_supervisory_principal_per_product_line", False), (
            "A named supervisory principal must be designated for each type of "
            "business conducted — generic 'compliance department' designation "
            "is insufficient (FINRA Rule 3110(b))"
        )
```

---

## Electronic Communications Supervision (Rule 3110(b))

**Overall: DETERMINISTIC (policy exists; off-channel either prohibited or captured) + PARAMETERIZED (review methodology)**

```python
class TestElectronicCommunicationSupervision:
    """Rule 3110(b) + Rule 4511 — Business communications captured or prohibited; review process documented."""

    def test_electronic_communication_review_policy_exists(
        self, controls_evidence: dict
    ):
        finra = controls_evidence.get("finra", {})
        assert finra.get("electronic_communication_review_policy_exists", False), (
            "A documented policy for review of electronic business communications "
            "must exist, including review frequency and methodology "
            "(FINRA Rule 3110(b))"
        )

    def test_off_channel_communications_prohibited_or_captured(
        self, controls_evidence: dict
    ):
        finra = controls_evidence.get("finra", {})
        assert (
            finra.get("off_channel_communications_prohibited", False)
            or finra.get("off_channel_communications_captured_and_archived", False)
        ), (
            "Off-channel communications (personal devices, WhatsApp, iMessage, "
            "Signal) used for business must either be formally prohibited by policy "
            "and enforced, OR captured and archived — SEC/FINRA enforcement wave "
            "2022–2024 resulted in >$2B in penalties for off-channel failures "
            "(FINRA Rule 4511; SEC Order releases)"
        )

    def test_personal_device_business_use_policy_documented(
        self, controls_evidence: dict
    ):
        finra = controls_evidence.get("finra", {})
        assert finra.get("personal_device_business_use_policy_documented", False), (
            "A documented policy governing use of personal devices for business "
            "communication must exist — either a prohibition policy with attestations "
            "or a BYOD capture policy (FINRA Rule 3110(b))"
        )
```

---

## Books and Records Retention (Rules 4510–4530 / SEA Rule 17a-4)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestBooksAndRecordsRetention:
    """Rules 4510–4530 + SEA Rule 17a-4 — Minimum retention periods by record type; WORM format for electronic records."""

    def test_electronic_records_retained_minimum_3_years(self, controls_evidence: dict):
        finra = controls_evidence.get("finra", {})
        retention_years = finra.get("electronic_records_retention_years", 0)
        assert retention_years >= FINRA_ELECTRONIC_RECORDS_RETENTION_YEARS, (
            f"Electronic business records (email, IM, SMS) must be retained for at "
            f"least {FINRA_ELECTRONIC_RECORDS_RETENTION_YEARS} years. "
            f"Current retention: {retention_years} years "
            f"(FINRA Rule 4511 + SEA Rule 17a-4)"
        )

    def test_general_books_and_records_retained_6_years(self, controls_evidence: dict):
        finra = controls_evidence.get("finra", {})
        retention_years = finra.get("general_books_records_retention_years", 0)
        assert retention_years >= FINRA_GENERAL_RECORDS_RETENTION_YEARS, (
            f"Blotters, ledgers, and customer account records must be retained for "
            f"at least {FINRA_GENERAL_RECORDS_RETENTION_YEARS} years. "
            f"Current retention: {retention_years} years "
            f"(SEA Rule 17a-3/17a-4)"
        )

    def test_customer_complaints_retained_4_years(self, controls_evidence: dict):
        finra = controls_evidence.get("finra", {})
        retention_years = finra.get("customer_complaints_retention_years", 0)
        assert retention_years >= FINRA_CUSTOMER_COMPLAINTS_RETENTION_YEARS, (
            f"Customer complaint records must be retained for at least "
            f"{FINRA_CUSTOMER_COMPLAINTS_RETENTION_YEARS} years. "
            f"Current retention: {retention_years} years "
            f"(FINRA Rule 4530)"
        )

    def test_superseded_wsps_retained_3_years(self, controls_evidence: dict):
        finra = controls_evidence.get("finra", {})
        assert finra.get("superseded_wsps_retained_per_rule_4110", False), (
            "Superseded versions of Written Supervisory Procedures must be retained "
            f"for {FINRA_WSP_RETENTION_YEARS_AFTER_SUPERSEDED} years after supersession "
            f"(FINRA Rule 4110)"
        )

    def test_worm_format_used_for_electronic_records(self, controls_evidence: dict):
        finra = controls_evidence.get("finra", {})
        assert finra.get("electronic_records_stored_in_worm_format", False), (
            "All required electronic records must be stored in non-erasable, "
            "non-rewritable (WORM) format for the full required retention period — "
            "mutable storage does not satisfy Rule 4511 requirements "
            "(FINRA Rule 4511)"
        )

    def test_third_party_custodian_arrangement_if_using_cloud_worm(
        self, controls_evidence: dict
    ):
        finra = controls_evidence.get("finra", {})
        if not finra.get("using_third_party_worm_storage", False):
            return
        assert finra.get("third_party_custodian_arrangement_executed", False), (
            "When using third-party cloud WORM storage, a third-party custodian "
            "arrangement (or equivalent SEC/FINRA-approved arrangement) must be "
            "in place (FINRA Rule 4511 + SEA Rule 17a-4(f)(3)(vii))"
        )
```

---

## Customer Protection Reserve (SEA Rule 15c3-3)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestCustomerProtectionReserve:
    """SEA Rule 15c3-3 — Weekly reserve formula; deposit next business day; fully-paid securities in good control."""

    def test_reserve_formula_computed_weekly(self, controls_evidence: dict):
        finra = controls_evidence.get("finra", {})
        assert finra.get("reserve_formula_computed_weekly", False), (
            "The customer protection reserve formula (SEA Rule 15c3-3(e)) must be "
            "computed weekly — less frequent computation is a violation "
            "(SEA Rule 15c3-3)"
        )

    def test_reserve_deposit_made_next_business_day(self, controls_evidence: dict):
        finra = controls_evidence.get("finra", {})
        assert finra.get("reserve_deposit_made_by_next_business_day", False), (
            "Reserve funds must be deposited in the Special Reserve Bank Account "
            "by the next business day after computation "
            "(SEA Rule 15c3-3(e)(1))"
        )

    def test_customer_fully_paid_securities_in_good_control(
        self, controls_evidence: dict
    ):
        finra = controls_evidence.get("finra", {})
        assert finra.get("customer_fully_paid_securities_in_good_control_locations", False), (
            "Customer fully-paid and excess margin securities must be maintained "
            "in good control locations (SEA Rule 15c3-3(d)) — improper use of "
            "customer securities is a serious violation "
            "(SEA Rule 15c3-3)"
        )
```

---

## Form U4 / U5 Registration Filings (Rule 1010 / Form U4)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestRegistrationFilings:
    """Rule 1010 — U4 amendments within 30 days of material change; U5 within 30 days of termination."""

    def test_form_u4_amendments_filed_within_30_days(self, controls_evidence: dict):
        u4_events = controls_evidence.get("finra_u4_events", [])
        late = [
            e for e in u4_events
            if e.get("days_to_file", 0) > FINRA_U4_U5_MATERIAL_CHANGE_FILING_DAYS
        ]
        assert not late, (
            f"Form U4 amendments for material changes must be filed within "
            f"{FINRA_U4_U5_MATERIAL_CHANGE_FILING_DAYS} days of the triggering event. "
            f"Late filings: {[e['event_id'] for e in late]} "
            f"(FINRA Rule 1010)"
        )

    def test_form_u5_filed_within_30_days_of_termination(
        self, controls_evidence: dict
    ):
        terminations = controls_evidence.get("finra_terminations", [])
        late = [
            t for t in terminations
            if t.get("days_to_file_u5", 0) > FINRA_U4_U5_MATERIAL_CHANGE_FILING_DAYS
        ]
        assert not late, (
            f"Form U5 must be filed within {FINRA_U4_U5_MATERIAL_CHANGE_FILING_DAYS} "
            f"days of a registered person's termination. "
            f"Late filings: {[t['person_id'] for t in late]} "
            f"(FINRA Rule 1010)"
        )
```

---

## AML / BSA Program (FINRA Rule 3310)

**Overall: DETERMINISTIC (program existence, annual testing, SAR program) + PARAMETERIZED (adequacy)**

```python
class TestAMLBSAProgram:
    """Rule 3310 — Written AML program; independent testing annually; designated AML compliance officer; SAR filing."""

    def test_written_aml_program_exists(self, controls_evidence: dict):
        finra = controls_evidence.get("finra", {})
        assert finra.get("written_aml_program_exists", False), (
            "A written Anti-Money Laundering program must exist that complies "
            "with the Bank Secrecy Act and FINRA Rule 3310"
        )

    def test_aml_compliance_officer_designated(self, controls_evidence: dict):
        finra = controls_evidence.get("finra", {})
        assert finra.get("aml_compliance_officer_designated", False), (
            "A designated AML compliance officer responsible for implementing "
            "and monitoring the AML program must be named "
            "(FINRA Rule 3310(a))"
        )

    def test_independent_aml_testing_conducted_annually(
        self, controls_evidence: dict, reference_date: date
    ):
        finra = controls_evidence.get("finra", {})
        last_test = finra.get("aml_independent_testing_last_completed")
        assert last_test is not None, (
            "Independent testing (audit) of the AML program must be conducted; "
            "no completion date on record (FINRA Rule 3310(c))"
        )
        cutoff = reference_date - timedelta(
            days=FINRA_ANNUAL_SUPERVISORY_REVIEW_INTERVAL_MONTHS * 30
        )
        assert last_test >= cutoff, (
            f"AML program must be independently tested at least annually. "
            f"Last tested: {last_test} (FINRA Rule 3310(c))"
        )

    def test_sar_filing_process_documented(self, controls_evidence: dict):
        finra = controls_evidence.get("finra", {})
        assert finra.get("sar_filing_process_documented", False), (
            "A documented process for Suspicious Activity Report (SAR) filing "
            "must exist, including escalation, review, and recordkeeping procedures "
            "(FINRA Rule 3310 + 31 CFR §1023.320)"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|

*(No open assumptions — FINRA requirements tested here are binary DETERMINISTIC obligations: WSPs exist, records retained for minimum periods, WORM format, reserve formula weekly, U4/U5 within 30 days. WSP adequacy and supervisory reasonableness are CONTESTED, excluded from machine-testable assertions.)*
