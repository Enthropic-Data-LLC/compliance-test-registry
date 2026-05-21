# CCPA / CPRA — Consumer Rights and Business Obligations
# Cal. Civil Code §§1798.100–1798.199 (CCPA as amended by CPRA)
# CPPA Regulations (Cal. Code Regs. tit. 11, §§7000–7305, effective Mar 29 2024)
#
# Pattern guide:
#   Pattern 1 — direct assert — DETERMINISTIC obligations
#   Pattern 2 — @pytest.mark.assumption(...) — PARAMETERIZED
#   Pattern 3 — @pytest.mark.human_review_required(...) — CONTESTED
#
# New assumptions introduced in this file:
#   ASSUME-CCPA-NOTICE-001  §1798.130 — Privacy policy required elements; notice at collection
#   ASSUME-CCPA-DSR-001     §1798.130 — DSR verification; record-keeping format
#   ASSUME-CCPA-OPTOUT-001  §1798.120/135 — GPC implementation; 12-month re-auth restriction
#   ASSUME-CCPA-SPI-001     §1798.121 — SPI inventory; permitted use scope
#   ASSUME-CCPA-SP-001      §1798.140 — Service provider contract 7-element completeness
#   ASSUME-CCPA-SEC-001     §1798.150 — "Reasonable security" — CIS Controls alignment

import pytest
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


# ---------------------------------------------------------------------------
# Scope pre-condition
# ---------------------------------------------------------------------------

def is_covered_business(entity_profile: dict) -> bool:
    """
    §1798.140(d): A "business" under CCPA/CPRA is a for-profit entity that:
      (1) has gross annual revenues > $25M; OR
      (2) buys, sells, or shares PI of ≥ 100,000 consumers or households/year; OR
      (3) derives ≥ 50% of annual revenues from selling or sharing PI
    AND does business in California or with California consumers.
    """
    revenue = entity_profile.get("gross_annual_revenue_usd", 0)
    pi_volume = entity_profile.get("consumers_or_households_pi_volume_annual", 0)
    revenue_pct_from_pi = entity_profile.get("revenue_pct_from_selling_sharing_pi", 0)
    california_nexus = entity_profile.get("does_business_in_california", False)

    meets_threshold = (
        revenue > 25_000_000
        or pi_volume >= 100_000
        or revenue_pct_from_pi >= 50
    )
    return meets_threshold and california_nexus


@pytest.fixture(autouse=True)
def ccpa_scope_check(entity_profile: dict):
    """Skip all tests when entity is not a covered business under CCPA/CPRA."""
    if not is_covered_business(entity_profile):
        pytest.skip(
            "CCPA/CPRA does not apply — entity does not meet covered business thresholds "
            "($25M revenue, 100K consumer records, or 50% revenue from PI sale/sharing) "
            "or has no California nexus."
        )


# ---------------------------------------------------------------------------
# Shared constants
# ---------------------------------------------------------------------------

DSR_INITIAL_DAYS = 45           # §1798.130(a)(2) — calendar days from receipt
DSR_EXTENSION_DAYS = 90         # §1798.130(a)(2) — one 45-day extension → 90 total
OPT_OUT_BUSINESS_DAYS = 15      # §1798.120(b)(2) — business days (not calendar)
RESALE_RESTRICTION_MONTHS = 12  # §1798.120(c) — cannot re-sell/re-share without new consent
PRIVACY_POLICY_UPDATE_MONTHS = 12  # §1798.130(a)(5) — must update at least annually
DSR_RECORD_RETENTION_MONTHS = 24   # §1798.185(a)(8) — 24-month DSR record-keeping


def add_business_days(start: date, n: int) -> date:
    """Add n business days (Mon–Fri) to start date."""
    current = start
    added = 0
    while added < n:
        current += timedelta(days=1)
        if current.weekday() < 5:  # Monday = 0, Friday = 4
            added += 1
    return current


# ---------------------------------------------------------------------------
# Sensitive Personal Information categories (§1798.121 / §1798.140(ae))
# ---------------------------------------------------------------------------

SPI_CATEGORIES = frozenset({
    "social_security_drivers_license_passport",
    "financial_account_credentials",
    "precise_geolocation",
    "race_ethnic_origin_religion_union_membership",
    "personal_communications_contents",
    "genetic_data",
    "biometric_data_for_identification",
    "health_data",
    "sexual_orientation_sex_life",
})

# Permitted SPI uses without a "Limit SPI" opt-out mechanism (§1798.121(a)):
SPI_PERMITTED_PURPOSES = frozenset({
    "performing_services_or_providing_goods_requested",
    "detecting_security_incidents",
    "preventing_fraud",
    "ensuring_safety_physical_integrity",
    "short_term_transient_use",
    "maintaining_quality_or_improving_service",
    "legal_obligation",
    "noncommercial_research_journalism_statistics",
})


# ===========================================================================
# §1798.130 — Privacy Policy and Notice at Collection
# ===========================================================================

class TestPrivacyPolicyAndNotice:
    """§1798.130 — Privacy policy existence, currency, and content."""

    def test_privacy_policy_publicly_posted(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        §1798.130(a)(5): The business must make its privacy policy available in a
        conspicuous manner, at minimum by posting it on the business's website or
        mobile app. Existence of a publicly accessible privacy policy is binary.
        """
        privacy_policy = controls_evidence.get("privacy_policy")
        assert privacy_policy is not None, (
            "§1798.130(a)(5): No privacy_policy record found. "
            "CCPA requires a publicly posted privacy policy."
        )

        publicly_accessible = privacy_policy.get("publicly_accessible", False)
        assert publicly_accessible is True, (
            "§1798.130(a)(5): Privacy policy is not marked publicly_accessible. "
            "Must be posted conspicuously on the website or mobile app."
        )

    def test_privacy_policy_updated_within_12_months(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §1798.130(a)(5)(C): The privacy policy must be updated at least once every 12 months.
        """
        privacy_policy = controls_evidence.get("privacy_policy", {})
        last_updated = privacy_policy.get("last_updated_date")

        assert last_updated is not None, (
            "§1798.130(a)(5): Privacy policy has no last_updated_date. "
            "Annual update is required."
        )

        age_months = (
            (reference_date.year - last_updated.year) * 12
            + (reference_date.month - last_updated.month)
        )
        assert age_months <= PRIVACY_POLICY_UPDATE_MONTHS, (
            f"§1798.130(a)(5)(C): Privacy policy last updated {last_updated} — "
            f"{age_months} months ago (maximum {PRIVACY_POLICY_UPDATE_MONTHS}). "
            "Annual update required."
        )

    @pytest.mark.assumption(
        id="ASSUME-CCPA-NOTICE-001",
        description=(
            "Privacy policy required elements (§1798.130(a)(5)(A)): (1) categories of PI collected; "
            "(2) purposes for collection; (3) categories of PI sold or shared, and categories of "
            "third parties to whom sold/shared; (4) categories of PI disclosed for business purposes "
            "and categories of service providers/contractors receiving it; (5) retention period or "
            "criteria for each category (§1798.100(a)(3)); (6) consumer rights and how to exercise; "
            "(7) 'Do Not Sell or Share' and 'Limit SPI' links/descriptions; (8) contact for requests; "
            "(9) effective date; (10) whether PI is sold to third parties for monetary consideration. "
            "Notice at collection (§1798.100(b)): provided at or before PI collection; "
            "includes categories + purposes; must not use PI for additional purposes without notice + consent."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_privacy_policy_contains_required_elements(self, controls_evidence: dict):
        """
        Pattern 2 — PARAMETERIZED.
        §1798.130(a)(5)(A): Privacy policy must contain 10 required disclosure elements.
        """
        privacy_policy = controls_evidence.get("privacy_policy", {})

        required_elements = {
            "categories_of_pi_collected",
            "purposes_for_collection",
            "categories_sold_or_shared_and_recipients",
            "categories_disclosed_for_business_purposes",
            "retention_periods_or_criteria_per_category",
            "consumer_rights_and_how_to_exercise",
            "opt_out_and_limit_spi_links_or_description",
            "contact_for_requests",
            "effective_date",
            "whether_pi_sold_for_monetary_consideration",
        }

        present = set(privacy_policy.get("elements_present", []))
        missing = required_elements - present

        assert not missing, (
            f"§1798.130(a)(5)(A): Privacy policy is missing required elements: {missing}."
        )

    def test_notice_at_collection_provided(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        §1798.100(b): Businesses must provide a notice at collection at or before
        the point of collection. The notice must identify the categories of PI to be
        collected and the purposes for collection.
        """
        notice_at_collection = controls_evidence.get("notice_at_collection_procedure")

        assert notice_at_collection is not None, (
            "§1798.100(b): No notice_at_collection_procedure documented. "
            "Notice at collection is required at or before point of collection."
        )

        timing = notice_at_collection.get("delivery_timing")
        assert timing in ("at_collection", "before_collection"), (
            f"§1798.100(b): notice delivery_timing '{timing}' does not satisfy "
            "the 'at or before collection' requirement."
        )

        categories_disclosed = notice_at_collection.get("categories_and_purposes_included", False)
        assert categories_disclosed is True, (
            "§1798.100(b): Notice at collection must include PI categories and purposes."
        )


# ===========================================================================
# §1798.130 — DSR Infrastructure and Response
# ===========================================================================

class TestDSRInfrastructure:
    """§1798.130 — DSR submission methods, response timelines, and record-keeping."""

    def test_at_least_two_submission_methods_available(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        §1798.130(a)(1): Businesses must provide consumers with at least two methods
        to submit requests: for online businesses, a website form + toll-free number.
        Businesses without an internet presence: at least one method appropriate to
        the business's interactions with consumers.
        """
        submission_methods = controls_evidence.get("dsr_submission_methods", [])

        assert len(submission_methods) >= 2, (
            f"§1798.130(a)(1): Only {len(submission_methods)} DSR submission method(s) available. "
            "At least 2 methods required (minimum: toll-free number + website form)."
        )

        method_types = {m.get("method_type") for m in submission_methods}
        assert "toll_free_number" in method_types or "website_form" in method_types, (
            "§1798.130(a)(1): Neither toll_free_number nor website_form is among "
            f"the submission methods: {method_types}."
        )

    def test_dsr_responses_within_45_day_deadline(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §1798.130(a)(2): Businesses must respond to verifiable consumer requests within
        45 calendar days of receipt. One 45-day extension is permitted (total 90 days)
        if the business notifies the consumer within the initial 45-day window.
        """
        dsr_log = controls_evidence.get("dsr_log", [])

        overdue = []
        for req in dsr_log:
            req_id = req.get("request_id", "unknown")
            received = req.get("received_date")
            responded = req.get("responded_date")
            extension_notice = req.get("extension_notice_sent_date")

            if not received:
                continue

            deadline_initial = received + relativedelta(days=DSR_INITIAL_DAYS)
            deadline_extended = received + relativedelta(days=DSR_EXTENSION_DAYS)

            if responded is None:
                if extension_notice is None and reference_date > deadline_initial:
                    overdue.append({
                        "request_id": req_id,
                        "received": received,
                        "deadline": deadline_initial,
                    })
                elif extension_notice and reference_date > deadline_extended:
                    overdue.append({
                        "request_id": req_id,
                        "received": received,
                        "issue": "extended_deadline_exceeded",
                    })
            else:
                if extension_notice:
                    assert extension_notice <= deadline_initial, (
                        f"DSR {req_id}: extension notice {extension_notice} sent after "
                        f"initial 45-day deadline {deadline_initial}."
                    )
                    assert responded <= deadline_extended, (
                        f"DSR {req_id}: response {responded} after extended 90-day deadline."
                    )
                else:
                    assert responded <= deadline_initial, (
                        f"DSR {req_id}: response {responded} after 45-day deadline "
                        f"{deadline_initial} with no extension notice."
                    )

        assert not overdue, (
            f"§1798.130(a)(2): {len(overdue)} DSR(s) overdue: {overdue}"
        )

    def test_dsr_records_retained_24_months(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §1798.185(a)(8): Businesses must retain records of consumer requests and
        responses for 24 months. The record must include the type of request,
        date received, date responded, and basis for denial (if applicable).
        """
        dsr_retention = controls_evidence.get("dsr_record_retention")

        assert dsr_retention is not None, (
            "§1798.185(a)(8): No dsr_record_retention record found. "
            "DSR records must be retained for 24 months."
        )

        retention_months = dsr_retention.get("retention_months", 0)
        assert retention_months >= DSR_RECORD_RETENTION_MONTHS, (
            f"§1798.185(a)(8): DSR records retained for {retention_months} months. "
            f"Minimum is {DSR_RECORD_RETENTION_MONTHS} months."
        )

    @pytest.mark.assumption(
        id="ASSUME-CCPA-DSR-001",
        description=(
            "DSR verification (§1798.130(a)(3) + CPPA Regs §7060–7065): verification must be "
            "reasonably designed to verify the consumer's identity without being unnecessarily "
            "burdensome. Tiered approach: low-risk requests (categories of PI) — verify to a "
            "reasonable degree of certainty (1–2 data points); high-risk requests (specific pieces, "
            "deletion, correction) — verify to a higher degree of certainty (3+ data points or "
            "signed declaration under penalty of perjury for household requests). "
            "Cannot deny solely because unable to verify — must inform consumer. "
            "DSR record-keeping fields: request type, received date, verification method used, "
            "response date, outcome, basis for denial. Retention: 24 months from response."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_dsr_records_contain_required_fields(self, controls_evidence: dict):
        """
        Pattern 2 — PARAMETERIZED.
        §1798.185(a)(8) + CPPA Regs: DSR records must contain sufficient fields to
        demonstrate compliance with the request handling obligations.
        """
        dsr_log = controls_evidence.get("dsr_log", [])

        REQUIRED_DSR_FIELDS = {
            "request_type",
            "received_date",
            "responded_date",
            "outcome",
        }

        incomplete = []
        for req in dsr_log:
            req_id = req.get("request_id", "unknown")
            present = set(k for k, v in req.items() if v is not None)
            missing = REQUIRED_DSR_FIELDS - present

            if req.get("outcome") == "denied":
                if "denial_basis" not in req or req.get("denial_basis") is None:
                    missing.add("denial_basis")

            if missing:
                incomplete.append({"request_id": req_id, "missing_fields": missing})

        assert not incomplete, (
            f"§1798.185(a)(8): {len(incomplete)} DSR record(s) missing required fields: {incomplete}."
        )


# ===========================================================================
# §1798.105 / §1798.106 — Right to Delete and Right to Correct
# ===========================================================================

class TestRightToDeleteAndCorrect:
    """§1798.105 (delete) / §1798.106 (correct) — 45-day response deadline."""

    def test_deletion_requests_responded_within_deadline(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §1798.105(c): Business must respond to deletion requests within 45 days.
        If deletion is granted, the business must also notify service providers,
        contractors, and third parties to whom the PI was sold/shared.
        """
        dsr_log = controls_evidence.get("dsr_log", [])
        deletion_requests = [r for r in dsr_log if r.get("request_type") == "deletion"]

        overdue = []
        for req in deletion_requests:
            req_id = req.get("request_id", "unknown")
            received = req.get("received_date")
            responded = req.get("responded_date")
            extension_notice = req.get("extension_notice_sent_date")

            if not received:
                continue

            deadline_initial = received + relativedelta(days=DSR_INITIAL_DAYS)
            deadline_extended = received + relativedelta(days=DSR_EXTENSION_DAYS)

            if responded is None:
                if extension_notice is None and reference_date > deadline_initial:
                    overdue.append(req_id)
            elif extension_notice:
                if responded > deadline_extended:
                    overdue.append(req_id)
            else:
                if responded > deadline_initial:
                    overdue.append(req_id)

        assert not overdue, (
            f"§1798.105: {len(overdue)} deletion request(s) exceeded 45-day deadline: {overdue}"
        )

    def test_granted_deletions_notify_downstream_parties(
        self, controls_evidence: dict
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §1798.105(c)(1): When granting a deletion request, the business must direct
        service providers, contractors, and third parties to delete the consumer's PI.
        """
        dsr_log = controls_evidence.get("dsr_log", [])

        for req in dsr_log:
            if req.get("request_type") != "deletion" or req.get("outcome") != "granted":
                continue
            req_id = req.get("request_id", "unknown")

            downstream_notified = req.get("downstream_parties_notified_of_deletion", False)
            no_downstream = req.get("no_downstream_parties_held_pi", False)

            assert downstream_notified or no_downstream, (
                f"§1798.105(c)(1): Deletion request '{req_id}' was granted but "
                "downstream_parties_notified_of_deletion is False and "
                "no_downstream_parties_held_pi is False. Service providers/contractors "
                "must be directed to delete."
            )

    def test_correction_requests_responded_within_deadline(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §1798.106: Right to correct inaccurate personal information. 45-day response,
        one 45-day extension permitted. If correction is denied, business must inform
        the consumer of the reasons.
        """
        dsr_log = controls_evidence.get("dsr_log", [])
        correction_requests = [r for r in dsr_log if r.get("request_type") == "correction"]

        overdue = []
        for req in correction_requests:
            req_id = req.get("request_id", "unknown")
            received = req.get("received_date")
            responded = req.get("responded_date")
            extension_notice = req.get("extension_notice_sent_date")

            if not received:
                continue

            deadline = received + relativedelta(
                days=DSR_EXTENSION_DAYS if extension_notice else DSR_INITIAL_DAYS
            )

            if responded is None and reference_date > deadline:
                overdue.append(req_id)
            elif responded and responded > deadline:
                overdue.append(req_id)

        assert not overdue, (
            f"§1798.106: {len(overdue)} correction request(s) exceeded 45-day deadline: {overdue}"
        )


# ===========================================================================
# §1798.120 / §1798.135 — Right to Opt-Out of Sale or Sharing
# ===========================================================================

class TestRightToOptOut:
    """§1798.120 / §1798.135 — Opt-out of sale and sharing; GPC signal; homepage link."""

    def test_do_not_sell_or_share_link_on_homepage(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        §1798.135(a)(1): If the business sells or shares personal information, it must
        provide a clear and conspicuous link titled 'Do Not Sell or Share My Personal
        Information' on its homepage and in its privacy policy.
        """
        sells_or_shares_pi = controls_evidence.get(
            "business_sells_or_shares_personal_information", False
        )
        if not sells_or_shares_pi:
            pytest.skip("Business does not sell or share PI — opt-out link not required.")

        homepage_links = controls_evidence.get("homepage_compliance_links", {})
        dns_link = homepage_links.get("do_not_sell_or_share_my_personal_information")

        assert dns_link is not None and dns_link.get("present", False), (
            "§1798.135(a)(1): 'Do Not Sell or Share My Personal Information' link is "
            "absent from the homepage. This link is required when PI is sold or shared."
        )

    def test_opt_out_honored_within_15_business_days(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §1798.120(b)(2): Businesses must comply with opt-out requests within
        15 business days of receipt. Business days = Monday through Friday,
        excluding federal public holidays.
        """
        opt_out_log = controls_evidence.get("opt_out_request_log", [])

        violations = []
        for req in opt_out_log:
            req_id = req.get("request_id", "unknown")
            received = req.get("received_date")
            honored_date = req.get("opt_out_honored_date")
            still_selling = req.get("sale_or_sharing_continues", False)

            if not received:
                continue

            deadline = add_business_days(received, OPT_OUT_BUSINESS_DAYS)

            if still_selling:
                violations.append({
                    "request_id": req_id,
                    "issue": "sale_or_sharing_continues_after_opt_out",
                })
            elif honored_date is None:
                if reference_date > deadline:
                    violations.append({
                        "request_id": req_id,
                        "received": received,
                        "deadline": deadline,
                        "issue": "not_honored_by_deadline",
                    })
            else:
                assert honored_date <= deadline, (
                    f"Opt-out request '{req_id}': honored {honored_date} after "
                    f"15 business-day deadline {deadline}."
                )

        assert not violations, (
            f"§1798.120(b)(2): {len(violations)} opt-out request(s) not honored within "
            f"15 business days: {violations}"
        )

    def test_global_privacy_control_signal_honored(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        CPPA Regulations §7025(b): The Global Privacy Control (GPC) signal
        (Sec-GPC: 1 HTTP header or navigator.globalPrivacyControl = true)
        must be recognized and honored as a valid opt-out of sale and sharing.
        This is an enforcement priority for the CPPA.
        """
        gpc_implementation = controls_evidence.get("gpc_signal_implementation")

        assert gpc_implementation is not None, (
            "CPPA Regs §7025(b): No gpc_signal_implementation record found. "
            "The Global Privacy Control (GPC) signal must be honored as an opt-out."
        )

        gpc_honored = gpc_implementation.get("gpc_signal_recognized_and_honored", False)
        assert gpc_honored is True, (
            "CPPA Regs §7025(b): GPC signal is not recognized or honored. "
            "Sec-GPC: 1 header and navigator.globalPrivacyControl must be treated as "
            "a valid opt-out of sale and sharing."
        )

    @pytest.mark.assumption(
        id="ASSUME-CCPA-OPTOUT-001",
        description=(
            "GPC implementation: must be applied to the browser session in which the signal "
            "is received; must be persisted as an opt-out for that consumer; documented in "
            "privacy policy; no dark patterns to discourage opt-out. "
            "12-month re-authorization restriction (§1798.120(c)): after opt-out, PI may not "
            "be sold or shared (even with the same third party) for 12 months without obtaining "
            "new consent. 'New consent' must be an affirmative opt-in — pre-checked boxes not valid. "
            "Third-party notification: all current third-party buyers/sharers must be notified "
            "of the opt-out within the 15-business-day window."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_resale_restriction_enforced_after_opt_out(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 2 — PARAMETERIZED.
        §1798.120(c): After an opt-out, the business may not sell or share the
        consumer's PI for 12 months without obtaining new opt-in consent.
        """
        opt_out_log = controls_evidence.get("opt_out_request_log", [])

        for req in opt_out_log:
            req_id = req.get("request_id", "unknown")
            honored_date = req.get("opt_out_honored_date")

            if honored_date is None:
                continue

            restriction_end = honored_date + relativedelta(months=RESALE_RESTRICTION_MONTHS)

            # Check whether PI was sold/shared to a new third party during restriction window
            new_sale_during_restriction = req.get("new_sale_during_restriction_period", False)
            new_opt_in_obtained = req.get("new_opt_in_consent_obtained_before_new_sale", False)

            if new_sale_during_restriction and not new_opt_in_obtained:
                pytest.fail(
                    f"§1798.120(c): Consumer opt-out '{req_id}' honored {honored_date} — "
                    f"PI sold/shared again before {restriction_end} without new opt-in consent. "
                    "12-month resale restriction violated."
                )


# ===========================================================================
# §1798.121 — Right to Limit Use of Sensitive Personal Information
# ===========================================================================

class TestSensitivePersonalInformation:
    """§1798.121 — Right to limit use and disclosure of sensitive personal information."""

    def test_limit_spi_link_present_when_applicable(
        self, controls_evidence: dict, entity_profile: dict
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §1798.135(a)(2): If a business uses SPI for purposes other than the permitted
        purposes in §1798.121(a), it must provide a clear and conspicuous link
        'Limit the Use of My Sensitive Personal Information' on its homepage.
        """
        spi_inventory = controls_evidence.get("sensitive_personal_information_inventory", {})
        uses_spi_beyond_permitted = spi_inventory.get("uses_spi_beyond_permitted_purposes", False)

        if not uses_spi_beyond_permitted:
            pytest.skip("Business uses SPI only for permitted purposes — Limit SPI link not required.")

        homepage_links = controls_evidence.get("homepage_compliance_links", {})
        limit_spi_link = homepage_links.get("limit_the_use_of_my_sensitive_personal_information")

        assert limit_spi_link is not None and limit_spi_link.get("present", False), (
            "§1798.135(a)(2): 'Limit the Use of My Sensitive Personal Information' link "
            "is absent from homepage. Required when SPI is used beyond permitted purposes."
        )

    @pytest.mark.assumption(
        id="ASSUME-CCPA-SPI-001",
        description=(
            "SPI inventory (§1798.121): all SPI categories collected must be documented in "
            "the data inventory with: category, purpose, whether used beyond permitted scope, "
            "and whether the Limit SPI mechanism is in place. "
            "Permitted SPI uses (§1798.121(a)) that do not require a Limit SPI opt-out: "
            "service delivery, security/fraud prevention, safety, short-term transient use, "
            "service improvement, legal obligations, non-commercial research/journalism. "
            "SPI opt-out honored within 15 business days (same as sale/sharing opt-out). "
            "SPI limit mechanism must be technically effective — not just UI."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_spi_inventory_complete(self, controls_evidence: dict):
        """
        Pattern 2 — PARAMETERIZED.
        §1798.121: All SPI categories collected must be inventoried and their
        processing purposes documented.
        """
        pi_inventory = controls_evidence.get("personal_information_inventory", {})
        collected_categories = set(
            c.get("category") for c in pi_inventory.get("collection_details", [])
        )
        spi_collected = collected_categories & SPI_CATEGORIES

        if not spi_collected:
            pytest.skip("No SPI categories are collected — SPI tests not applicable.")

        spi_inventory = controls_evidence.get("sensitive_personal_information_inventory")
        assert spi_inventory is not None, (
            "§1798.121: SPI categories are collected but no "
            "sensitive_personal_information_inventory found. "
            "Each SPI category must be documented with processing purpose."
        )

        inventoried_categories = {
            item.get("category") for item in spi_inventory.get("categories", [])
        }
        uninventoried = spi_collected - inventoried_categories

        assert not uninventoried, (
            f"§1798.121: SPI categories collected but not in inventory: {uninventoried}."
        )


# ===========================================================================
# §1798.125 — Non-Discrimination
# ===========================================================================

class TestNonDiscrimination:
    """§1798.125 — Business may not discriminate for exercising CCPA rights."""

    def test_no_price_or_service_differential_for_rights_exercise(
        self, controls_evidence: dict
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §1798.125(a)(1): A business may not deny goods/services, charge different
        prices, or provide a different level or quality of goods/services because a
        consumer exercised a right under CCPA. Confirmed discrimination is per se violation.
        """
        rights_exercise_log = controls_evidence.get("ccpa_rights_exercise_log", [])

        violations = []
        for exercise in rights_exercise_log:
            exercise_id = exercise.get("exercise_id", "unknown")
            service_denied = exercise.get("service_denied_after_rights_exercise", False)
            price_differential = exercise.get("price_differential_applied", False)
            quality_differential = exercise.get("quality_differential_applied", False)

            if service_denied or price_differential or quality_differential:
                violations.append({
                    "exercise_id": exercise_id,
                    "service_denied": service_denied,
                    "price_differential": price_differential,
                    "quality_differential": quality_differential,
                })

        assert not violations, (
            f"§1798.125(a)(1): {len(violations)} instance(s) of discrimination "
            f"following rights exercise: {violations}."
        )


# ===========================================================================
# §1798.140(e) — Service Provider / Contractor Contracts
# ===========================================================================

class TestServiceProviderContracts:
    """§1798.140 — Written contracts with service providers and contractors."""

    def test_service_provider_contracts_exist(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        §1798.140(e): A service provider or contractor relationship requires a written
        contract before disclosing PI. Without a written contract, the recipient is
        a 'third party' and the disclosure may constitute a sale.
        """
        service_providers = controls_evidence.get("service_providers", [])

        violations = []
        for sp in service_providers:
            sp_id = sp.get("sp_id", "unknown")
            receives_pi = sp.get("receives_personal_information", False)
            written_contract = sp.get("written_contract_on_file", False)

            if receives_pi and not written_contract:
                violations.append(sp_id)

        assert not violations, (
            f"§1798.140(e): {len(violations)} service provider(s)/contractor(s) receive "
            f"PI without a written contract: {violations}. Without a written contract, "
            "the relationship may constitute a 'sale' under CCPA."
        )

    @pytest.mark.assumption(
        id="ASSUME-CCPA-SP-001",
        description=(
            "Service provider contract required elements (§1798.140(e)(1–7)): "
            "(1) specifies PI is disclosed only for limited and specified purposes; "
            "(2) obligates SP to comply with CCPA; "
            "(3) grants business right to take reasonable steps to ensure SP uses PI consistently; "
            "(4) requires SP to notify business if it can no longer meet its CCPA obligations; "
            "(5) grants business right to remedy unauthorized use upon notice; "
            "(6) SP and subcontractors must not: sell/share PI, retain/use/disclose beyond scope, "
            "combine PI from multiple sources (outside specific exceptions); "
            "(7) SP must delete or return PI at contract termination. "
            "Annual risk assessment: required for processing activities posing significant risk "
            "per CPPA regulations (still evolving — placeholder test in place)."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_service_provider_contracts_contain_required_terms(
        self, controls_evidence: dict
    ):
        """
        Pattern 2 — PARAMETERIZED.
        §1798.140(e): Service provider contracts must contain 7 required elements.
        """
        REQUIRED_SP_TERMS = {
            "pi_disclosed_for_limited_specified_purposes",
            "sp_obligated_to_comply_with_ccpa",
            "business_right_to_audit_or_verify_compliance",
            "sp_must_notify_business_if_unable_to_comply",
            "business_right_to_remedy_unauthorized_use",
            "sp_prohibited_from_selling_sharing_or_combining_pi",
            "return_or_delete_pi_at_termination",
        }

        service_providers = controls_evidence.get("service_providers", [])

        for sp in service_providers:
            sp_id = sp.get("sp_id", "unknown")
            if not sp.get("receives_personal_information", False):
                continue
            if not sp.get("written_contract_on_file", False):
                continue

            contract_terms = set(sp.get("contract_terms_present", []))
            missing = REQUIRED_SP_TERMS - contract_terms

            assert not missing, (
                f"§1798.140(e): Service provider '{sp_id}' contract is missing "
                f"required terms: {missing}."
            )


# ===========================================================================
# §1798.150 — Security / Private Right of Action
# ===========================================================================

class TestSecurityObligations:
    """§1798.150 — Reasonable security; private right of action for non-encrypted PI breaches."""

    def test_non_encrypted_pi_breach_documented_and_notified(
        self, controls_evidence: dict
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §1798.150(a): When non-encrypted or non-redacted personal information is
        subject to unauthorized access and exfiltration, theft, or disclosure due to
        a business's failure to maintain reasonable security procedures, consumers
        may bring a civil action for $100–$750 per consumer per incident (or actual
        damages if greater). Evidence requirement: document all data breach incidents
        involving non-encrypted/non-redacted PI; breach notifications sent per CA law.
        """
        breach_log = controls_evidence.get("data_breach_log", [])

        for breach in breach_log:
            breach_id = breach.get("breach_id", "unknown")
            involves_non_encrypted_pi = breach.get("involves_non_encrypted_unredacted_pi", False)

            if not involves_non_encrypted_pi:
                continue

            # Breach involving non-encrypted PI must have documented notification
            ca_notification_sent = breach.get("california_breach_notification_sent", False)
            assert ca_notification_sent is True, (
                f"§1798.150 / CA Civil Code §1798.82: Breach '{breach_id}' involves "
                "non-encrypted, non-redacted PI but no California breach notification "
                "was recorded. §1798.82 requires notification without unreasonable delay "
                "and no later than 45 days after discovery."
            )

    @pytest.mark.human_review_required(
        reason=(
            "§1798.150: 'Reasonable security procedures and practices appropriate to the "
            "nature of the information' is CONTESTED — no statutory definition. "
            "The CA AG has cited CIS Controls as a reasonable reference benchmark in "
            "enforcement actions. No court or regulation has designated a binding standard. "
            "Required: annual attestation by CISO/Compliance Officer that the organization's "
            "security program aligns with a recognized framework (CIS Controls, NIST CSF, "
            "ISO 27001) appropriate to the sensitivity of PI processed. "
            "The attestation should document which framework is used and key gaps."
        )
    )
    @pytest.mark.assumption(
        id="ASSUME-CCPA-SEC-001",
        description=(
            "Reasonable security (§1798.150): no prescribed standard. CA AG enforcement "
            "precedent cites CIS Controls. Assumption: organization maintains a security "
            "program aligned with CIS Controls v8 or equivalent recognized framework, "
            "documented annually by CISO. At minimum: encryption for PI at rest and in transit, "
            "access controls, vulnerability management, incident response plan. "
            "Key risk: non-encrypted PI in a breach triggers private right of action — "
            "encryption is the strongest §1798.150 defense."
        ),
        approved_by="CISO",
        review_date="2026-11-01",
    )
    def test_reasonable_security_program_attested(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 3 — CONTESTED.
        §1798.150: Annual CISO attestation that the security program is reasonable
        and aligned with a recognized framework appropriate to PI sensitivity.
        """
        security_attestation = controls_evidence.get("reasonable_security_annual_attestation")

        assert security_attestation is not None, (
            "§1798.150: No reasonable_security_annual_attestation found. "
            "Annual CISO/Compliance Officer attestation of security program adequacy required."
        )

        attestation_date = security_attestation.get("attestation_date")
        attested_by = security_attestation.get("attested_by")
        framework_referenced = security_attestation.get("security_framework_referenced")

        assert attestation_date is not None
        assert (reference_date - attestation_date).days <= 365, (
            f"§1798.150: Security attestation overdue (last: {attestation_date})."
        )
        assert attested_by in ("CISO", "Compliance Officer", "VP Engineering"), (
            f"§1798.150: Attestation signed by '{attested_by}' — expected CISO, "
            "Compliance Officer, or VP Engineering."
        )
        assert framework_referenced is not None, (
            "§1798.150: Attestation does not reference a security framework. "
            "Must cite CIS Controls, NIST CSF, ISO 27001, or equivalent."
        )
