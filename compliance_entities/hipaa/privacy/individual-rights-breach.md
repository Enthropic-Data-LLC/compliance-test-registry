# HIPAA Privacy Rule — Individual Rights and Breach Notification
# 45 CFR §§164.404–414 (Breach Notification), §164.520 (NPP),
#         §164.522 (Restrictions), §164.524 (Access), §164.526 (Amendment),
#         §164.528 (Accounting of Disclosures)
#
# Pattern guide:
#   Pattern 1 — direct assert — DETERMINISTIC obligations
#   Pattern 2 — @pytest.mark.assumption(...) — PARAMETERIZED
#   Pattern 3 — @pytest.mark.human_review_required(...) — CONTESTED
#
# New assumptions introduced in this file:
#   ASSUME-HIPAA-PRIV-NPP-001    §164.520 — NPP required elements; acknowledgment good-faith effort
#   ASSUME-HIPAA-PRIV-ACCESS-001 §164.524 — Access fee limits; ePHI electronic format; denial categories
#   ASSUME-HIPAA-PRIV-AMEND-001  §164.526 — Amendment acceptance; notification to relevant parties
#   ASSUME-HIPAA-PRIV-ACCT-001   §164.528 — Accounting log required fields; 6-year lookback
#   ASSUME-HIPAA-PRIV-BREACH-001 §164.404 — Unsecured PHI determination; 4-factor harm assessment

#
# Applies to: Covered entities (healthcare providers who transmit health information electronically, health plans, healthcare clearinghouses) and their business associates who create, receive, maintain, or transmit PHI on behalf of a covered entity
# Trigger: Creation, receipt, maintenance, or transmission of Protected Health Information (PHI) in connection with a covered function; business associate agreements (BAAs) flow down requirements to subcontractors
# Jurisdiction: United States; extraterritorial reach for foreign entities handling PHI of US patients or providing services to US covered entities
# Not applicable to: Life insurers outside healthcare coverage; employers' employment records; education records covered by FERPA; de-identified data meeting Safe Harbor or Expert Determination standard; purely personal health records with no commercial healthcare function
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


# ---------------------------------------------------------------------------
# Scope pre-condition
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def hipaa_privacy_scope_check(entity_profile: dict):
    is_ce = entity_profile.get("hipaa_covered_entity", False)
    is_ba = entity_profile.get("hipaa_business_associate", False)
    if not (is_ce or is_ba):
        pytest.skip(
            "HIPAA Privacy Rule (45 CFR Part 164 Subpart E) does not apply — "
            "entity is neither a covered entity nor a business associate."
        )


# ---------------------------------------------------------------------------
# Response deadlines (calendar days from receipt of request)
# ---------------------------------------------------------------------------

ACCESS_INITIAL_DAYS = 30       # §164.524(b)(2) — initial response
ACCESS_EXTENSION_DAYS = 60     # §164.524(b)(2)(ii) — one-time 30-day extension → total 60
AMENDMENT_INITIAL_DAYS = 60    # §164.526(b)(2)
AMENDMENT_EXTENSION_DAYS = 90  # §164.526(b)(2)(ii) — one 30-day extension → total 90
ACCOUNTING_INITIAL_DAYS = 60   # §164.528(c)(1)
ACCOUNTING_EXTENSION_DAYS = 90 # §164.528(c)(1) — one 30-day extension → total 90

BREACH_INDIVIDUAL_NOTICE_DAYS = 60   # §164.404(b) — from discovery
BREACH_MEDIA_NOTICE_DAYS = 60        # §164.406 — from discovery; > 500 in state/jurisdiction
BREACH_HHS_LARGE_DAYS = 60           # §164.408(b) — > 500: within 60 days of discovery
# HHS annual log: < 500: maintained throughout year, submitted within 60 days of calendar year end
NPP_UPDATE_DAYS = 60                 # §164.520(b)(3) — after material change

# Accounting lookback
ACCOUNTING_LOOKBACK_YEARS = 6        # §164.528(b)(1)


# ===========================================================================
# §164.520 — Notice of Privacy Practices (NPP)
# ===========================================================================

class TestSection164520NoticeOfPrivacyPractices:
    """§164.520 — Notice of Privacy Practices."""

    # -----------------------------------------------------------------------
    # §164.520(b) — Required elements (selected DETERMINISTIC subset)
    # -----------------------------------------------------------------------

    @pytest.mark.assumption(
        id="ASSUME-HIPAA-PRIV-NPP-001",
        description=(
            "NPP required elements (§164.520(b)): (1) header — verbatim 'THIS NOTICE DESCRIBES HOW "
            "MEDICAL INFORMATION ABOUT YOU MAY BE USED AND DISCLOSED AND HOW YOU CAN GET ACCESS TO "
            "THIS INFORMATION. PLEASE REVIEW IT CAREFULLY.'; (2) description of uses/disclosures "
            "CE is permitted/required to make; (3) separate statement of uses/disclosures requiring "
            "authorization; (4) description of each individual right and how to exercise it; "
            "(5) CE's legal duties: maintain privacy, abide by current NPP, right to change NPP; "
            "(6) how to file complaints with CE and HHS; (7) effective date. "
            "Good-faith effort for acknowledgment: CE must document attempt; no penalty if patient "
            "refuses to sign — must document the refusal."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_npp_contains_required_elements(self, controls_evidence: dict):
        """
        Pattern 2 — PARAMETERIZED.
        §164.520(b): NPP must contain 7 required elements. Content adequacy of descriptions
        is PARAMETERIZED; existence of each element is DETERMINISTIC.
        """
        npp_record = controls_evidence.get("notice_of_privacy_practices")

        assert npp_record is not None, (
            "§164.520: No notice_of_privacy_practices record found. "
            "All covered entities must maintain and provide an NPP."
        )

        required_elements = {
            "verbatim_header_present",
            "description_of_permitted_uses_disclosures",
            "separate_statement_for_authorization_required_uses",
            "individual_rights_description",
            "ce_legal_duties_statement",
            "complaint_procedure_ce_and_hhs",
            "effective_date",
        }

        present = set(npp_record.get("elements_present", []))
        missing = required_elements - present

        assert not missing, (
            f"§164.520(b): NPP is missing required elements: {missing}."
        )

    def test_npp_verbatim_header_present(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        §164.520(b)(1)(i): The NPP header must appear verbatim in prominent placement:
        'THIS NOTICE DESCRIBES HOW MEDICAL INFORMATION ABOUT YOU MAY BE USED AND
        DISCLOSED AND HOW YOU CAN GET ACCESS TO THIS INFORMATION. PLEASE REVIEW IT CAREFULLY.'
        """
        npp_record = controls_evidence.get("notice_of_privacy_practices", {})
        header_verbatim = npp_record.get("verbatim_header_present", False)

        assert header_verbatim is True, (
            "§164.520(b)(1)(i): NPP verbatim header is absent. The exact regulatory header "
            "language must appear prominently on the NPP."
        )

    # -----------------------------------------------------------------------
    # §164.520(c) — Provision to individuals + acknowledgment
    # -----------------------------------------------------------------------

    def test_npp_provided_at_first_service_delivery(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        §164.520(c)(1)(i): Direct treatment providers must provide the NPP no later than
        the date of first service delivery. Emergency situations: as soon as practicable.
        """
        npp_delivery = controls_evidence.get("npp_delivery_procedure")

        assert npp_delivery is not None, (
            "§164.520(c): No npp_delivery_procedure documented. "
            "NPP must be provided at or before first service delivery."
        )

        delivery_trigger = npp_delivery.get("delivery_trigger")
        assert delivery_trigger in (
            "first_service_delivery",
            "at_or_before_first_service",
        ), (
            f"§164.520(c)(1)(i): delivery_trigger '{delivery_trigger}' does not satisfy "
            "the requirement for provision no later than first service delivery."
        )

    def test_acknowledgment_good_faith_effort_documented(
        self, controls_evidence: dict
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.520(c)(2)(ii): CE must make a good-faith effort to obtain written acknowledgment
        of receipt. If acknowledgment is not obtained, CE must document why.
        """
        npp_delivery = controls_evidence.get("npp_delivery_procedure", {})

        acknowledgment_procedure = npp_delivery.get("acknowledgment_procedure")
        assert acknowledgment_procedure is not None, (
            "§164.520(c)(2)(ii): No acknowledgment_procedure documented. CE must describe "
            "how it obtains (or documents inability to obtain) written acknowledgment."
        )

        documents_refusals = acknowledgment_procedure.get(
            "documents_patient_refusal_to_sign", False
        )
        assert documents_refusals is True, (
            "§164.520(c)(2)(ii): Acknowledgment procedure does not document patient refusals. "
            "When acknowledgment cannot be obtained, CE must document the attempt and why "
            "acknowledgment was not obtained."
        )

    # -----------------------------------------------------------------------
    # §164.520(b)(3) — NPP update: 60 days after material change
    # -----------------------------------------------------------------------

    def test_npp_updated_within_60_days_of_material_change(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.520(b)(3)/(c)(1)(i) (health plans) / (c)(2)(iv) (direct treatment providers):
        Material changes to privacy practices must be reflected in an updated NPP
        distributed (or made available) within 60 days of the effective date of the change.
        """
        npp_change_log = controls_evidence.get("npp_material_change_log", [])

        for change in npp_change_log:
            change_id = change.get("change_id", "unknown")
            effective_date = change.get("effective_date")
            npp_updated_date = change.get("npp_updated_and_distributed_date")

            if effective_date is None:
                continue

            deadline = effective_date + relativedelta(days=NPP_UPDATE_DAYS)

            if npp_updated_date is None:
                # Only fail if deadline has passed
                if reference_date > deadline:
                    pytest.fail(
                        f"§164.520(b)(3): Material privacy change '{change_id}' effective "
                        f"{effective_date} — NPP has not been updated. Deadline: {deadline}."
                    )
            else:
                assert npp_updated_date <= deadline, (
                    f"§164.520(b)(3): Material privacy change '{change_id}' effective "
                    f"{effective_date} — NPP not updated until {npp_updated_date}, "
                    f"after 60-day deadline {deadline}."
                )


# ===========================================================================
# §164.522 — Rights to Request Privacy Protection and Restrictions
# ===========================================================================

class TestSection164522Restrictions:
    """§164.522 — Restriction requests and confidential communications."""

    # -----------------------------------------------------------------------
    # §164.522(a)(1)(vi) — Out-of-pocket payment restriction: mandatory
    # -----------------------------------------------------------------------

    def test_out_of_pocket_payment_restriction_is_mandatory(
        self, controls_evidence: dict
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.522(a)(1)(vi) (HITECH): A CE MUST agree to a restriction request when:
          - The disclosure is to a health plan for payment or healthcare operations
          - The item/service was paid for out-of-pocket in full by the individual
        This is the only mandatory restriction under HIPAA. CE cannot deny it.
        """
        restriction_requests = controls_evidence.get("restriction_requests", [])

        violations = []
        for req in restriction_requests:
            req_id = req.get("request_id", "unknown")
            is_oop_payment = req.get("is_out_of_pocket_payment_in_full", False)
            is_health_plan_disclosure = req.get("restriction_against_health_plan", False)
            ce_agreed = req.get("ce_agreed_to_restriction", False)
            ce_denied = req.get("ce_denied_restriction", False)

            if is_oop_payment and is_health_plan_disclosure and ce_denied:
                violations.append(req_id)

        assert not violations, (
            f"§164.522(a)(1)(vi): {len(violations)} mandatory restriction request(s) "
            f"improperly denied: {violations}. When an individual pays out-of-pocket in full, "
            "the CE MUST agree to restrict disclosure to the health plan for payment/operations."
        )

    def test_agreed_restrictions_are_honored(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        §164.522(a)(1)(iii): Once a CE agrees to a restriction, it is bound by it —
        with exceptions for treatment in an emergency or required by law.
        """
        restriction_requests = controls_evidence.get("restriction_requests", [])

        for req in restriction_requests:
            req_id = req.get("request_id", "unknown")
            if not req.get("ce_agreed_to_restriction", False):
                continue

            restriction_violated = req.get("restriction_subsequently_violated", False)
            emergency_exception = req.get("emergency_treatment_exception_documented", False)
            required_by_law = req.get("required_by_law_exception", False)

            if restriction_violated and not (emergency_exception or required_by_law):
                pytest.fail(
                    f"§164.522(a)(1)(iii): Agreed restriction request '{req_id}' was violated "
                    "without a documented emergency treatment or required-by-law exception."
                )


# ===========================================================================
# §164.524 — Access of Individuals to Protected Health Information
# ===========================================================================

class TestSection164524IndividualAccess:
    """§164.524 — Right of access to PHI (inspect and copy)."""

    # -----------------------------------------------------------------------
    # §164.524(b)(2) — 30-day response deadline
    # -----------------------------------------------------------------------

    def test_access_requests_responded_within_deadline(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.524(b)(2): CE must act on an access request no later than 30 days
        after receipt. One 30-day extension (total 60 days) is permitted if
        the records are not maintained onsite — extension notice within 30 days.
        """
        access_log = controls_evidence.get("individual_access_request_log", [])

        overdue = []
        for req in access_log:
            req_id = req.get("request_id", "unknown")
            received = req.get("received_date")
            responded = req.get("responded_date")
            extension_notice = req.get("extension_notice_sent_date")
            offsite_records = req.get("records_not_maintained_onsite", False)

            if not received:
                continue

            deadline_initial = received + relativedelta(days=ACCESS_INITIAL_DAYS)
            deadline_extended = received + relativedelta(days=ACCESS_EXTENSION_DAYS)

            if responded is None:
                if reference_date > deadline_initial and extension_notice is None:
                    overdue.append({"request_id": req_id, "received": received})
                elif extension_notice and reference_date > deadline_extended:
                    overdue.append({
                        "request_id": req_id,
                        "received": received,
                        "issue": "extended_deadline_also_exceeded",
                    })
            else:
                if extension_notice:
                    assert extension_notice <= deadline_initial, (
                        f"Access request {req_id}: extension notice {extension_notice} "
                        f"sent after initial 30-day deadline {deadline_initial}."
                    )
                    assert responded <= deadline_extended, (
                        f"Access request {req_id}: response {responded} after extended "
                        f"60-day deadline {deadline_extended}."
                    )
                    assert offsite_records is True, (
                        f"Access request {req_id}: 30-day extension used but "
                        "records_not_maintained_onsite is not True. Extension only permitted "
                        "for records not maintained or accessible onsite."
                    )
                else:
                    assert responded <= deadline_initial, (
                        f"Access request {req_id}: response {responded} after 30-day "
                        f"deadline {deadline_initial} with no extension notice."
                    )

        assert not overdue, (
            f"§164.524(b)(2): {len(overdue)} access request(s) overdue: {overdue}"
        )

    # -----------------------------------------------------------------------
    # §164.524 (HITECH) — ePHI access in electronic format
    # -----------------------------------------------------------------------

    def test_ephi_access_provided_in_electronic_format_when_requested(
        self, controls_evidence: dict
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.524(c)(2)(ii) (HITECH): If the individual requests ePHI in electronic form
        and the CE maintains the PHI in an EHR, the CE must provide it in the electronic
        form and format requested by the individual, if readily producible. If not readily
        producible in the requested format, CE must provide it in a readable electronic form
        agreed to by CE and individual. CE may not require a written request when CE already
        offers electronic access.
        """
        access_log = controls_evidence.get("individual_access_request_log", [])

        violations = []
        for req in access_log:
            req_id = req.get("request_id", "unknown")
            if req.get("outcome") not in ("granted", "partial"):
                continue

            requested_electronic = req.get("requested_electronic_format", False)
            phi_maintained_in_ehr = req.get("phi_in_ehr", False)

            if not (requested_electronic and phi_maintained_in_ehr):
                continue

            provided_format = req.get("provided_format", "")
            if provided_format in ("paper_only", "hard_copy_only"):
                violations.append({
                    "request_id": req_id,
                    "provided_format": provided_format,
                })

        assert not violations, (
            f"§164.524(c)(2)(ii): {len(violations)} ePHI access request(s) fulfilled in "
            f"paper-only format despite individual requesting electronic format: {violations}."
        )

    @pytest.mark.assumption(
        id="ASSUME-HIPAA-PRIV-ACCESS-001",
        description=(
            "Access fee limits (§164.524(c)(4)): CE may only charge a reasonable, cost-based fee "
            "covering: labor for copying (paper or electronic), supplies for paper copies, "
            "postage. Cannot charge for retrieving/searching, or for maintaining the system. "
            "Flat fees not permitted by OCR 2016 guidance except: 'actual costs' or "
            "'labor + supplies + postage' calculation. "
            "Denial categories (§164.524(a)(2)): unreviewable denials (correctional, research) "
            "and reviewable denials (information compiled in anticipation of litigation, licensed "
            "professional believes access may endanger). Reviewable denials require second review "
            "by licensed professional not involved in original decision."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_access_denial_is_in_permitted_category(self, controls_evidence: dict):
        """
        Pattern 2 — PARAMETERIZED.
        §164.524(a)(2): Denials of access are only permitted in specified categories.
        Non-listed denial reasons are impermissible.
        """
        PERMITTED_DENIAL_CATEGORIES = {
            # Unreviewable
            "correctional_facility_jeopardizes_health_safety",
            "research_with_irb_modification",
            "privacy_act_system_of_records",
            # Reviewable
            "licensed_professional_endanger_life",
            "requested_by_personal_representative_endanger",
            "information_compiled_in_anticipation_of_litigation",
        }

        access_log = controls_evidence.get("individual_access_request_log", [])

        for req in access_log:
            req_id = req.get("request_id", "unknown")
            if req.get("outcome") != "denied":
                continue

            denial_category = req.get("denial_category")
            assert denial_category in PERMITTED_DENIAL_CATEGORIES, (
                f"Access request {req_id}: denial category '{denial_category}' is not a "
                f"permitted §164.524(a)(2) denial ground. Permitted: {PERMITTED_DENIAL_CATEGORIES}"
            )

            # Reviewable denials require second review
            reviewable = {
                "licensed_professional_endanger_life",
                "requested_by_personal_representative_endanger",
                "information_compiled_in_anticipation_of_litigation",
            }
            if denial_category in reviewable:
                second_review = req.get("second_review_by_uninvolved_professional", False)
                assert second_review is True, (
                    f"Access request {req_id}: reviewable denial category '{denial_category}' "
                    "requires a second review by a licensed professional not involved in the "
                    "original decision. §164.524(d)."
                )


# ===========================================================================
# §164.526 — Amendment of Protected Health Information
# ===========================================================================

class TestSection164526Amendment:
    """§164.526 — Individual right to request amendment of PHI."""

    def test_amendment_requests_responded_within_deadline(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.526(b)(2): CE must act on amendment requests within 60 days of receipt.
        One 30-day extension (total 90 days) is permitted with written notice within 60 days.
        """
        amendment_log = controls_evidence.get("amendment_request_log", [])

        overdue = []
        for req in amendment_log:
            req_id = req.get("request_id", "unknown")
            received = req.get("received_date")
            responded = req.get("responded_date")
            extension_notice = req.get("extension_notice_sent_date")

            if not received:
                continue

            deadline_initial = received + relativedelta(days=AMENDMENT_INITIAL_DAYS)
            deadline_extended = received + relativedelta(days=AMENDMENT_EXTENSION_DAYS)

            if responded is None:
                if reference_date > deadline_initial and extension_notice is None:
                    overdue.append(req_id)
            else:
                if extension_notice:
                    assert extension_notice <= deadline_initial
                    assert responded <= deadline_extended
                else:
                    assert responded <= deadline_initial, (
                        f"Amendment request {req_id}: response {responded} after 60-day "
                        f"deadline {deadline_initial}."
                    )

        assert not overdue, (
            f"§164.526(b)(2): {len(overdue)} amendment request(s) overdue: {overdue}"
        )

    def test_amendment_denials_are_written_with_reason(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        §164.526(d)(1): If CE denies an amendment request, the denial must be in writing
        and inform the individual of the basis for the denial, how to submit a written
        statement of disagreement, and how to file a complaint.
        """
        PERMITTED_DENIAL_BASES = {
            "not_created_by_ce",
            "not_part_of_designated_record_set",
            "not_available_for_inspection",
            "accurate_and_complete",
        }

        amendment_log = controls_evidence.get("amendment_request_log", [])

        for req in amendment_log:
            req_id = req.get("request_id", "unknown")
            if req.get("outcome") != "denied":
                continue

            denial_in_writing = req.get("denial_in_writing", False)
            assert denial_in_writing is True, (
                f"Amendment request {req_id}: denial is not documented in writing. "
                "§164.526(d)(1) requires written denial with reason, disagreement rights, "
                "and complaint procedure."
            )

            denial_basis = req.get("denial_basis")
            assert denial_basis in PERMITTED_DENIAL_BASES, (
                f"Amendment request {req_id}: denial basis '{denial_basis}' is not one of "
                f"the four permitted grounds: {PERMITTED_DENIAL_BASES}."
            )

    @pytest.mark.assumption(
        id="ASSUME-HIPAA-PRIV-AMEND-001",
        description=(
            "Amendment notification (§164.526(c)(3)): when CE grants an amendment, it must "
            "make reasonable efforts to inform and provide the amendment to: "
            "(1) persons identified by the individual as needing notification; "
            "(2) persons CE knows have received the PHI and could rely on it to the individual's detriment. "
            "Assumption: CE maintains a disclosure accounting (§164.528) that enables identification "
            "of recipients; amendment notifications sent within 30 days of amendment acceptance; "
            "notifications documented in the amendment record. "
            "Statement of disagreement (§164.526(d)(2)): if accepted, CE must include the statement "
            "in future disclosures of the relevant PHI."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_accepted_amendment_propagated_to_relevant_parties(
        self, controls_evidence: dict
    ):
        """
        Pattern 2 — PARAMETERIZED.
        §164.526(c)(3): when CE grants an amendment, it must notify persons who
        received the PHI and could rely on it to the individual's detriment.
        """
        amendment_log = controls_evidence.get("amendment_request_log", [])

        for req in amendment_log:
            if req.get("outcome") != "granted":
                continue
            req_id = req.get("request_id", "unknown")

            propagation = req.get("amendment_propagation_record")
            assert propagation is not None, (
                f"Amendment request {req_id} was granted but no amendment_propagation_record "
                "exists. §164.526(c)(3) requires notification to relevant recipients."
            )

            notified = propagation.get("notified_parties", [])
            no_prior_disclosures = propagation.get("no_prior_disclosures_requiring_notification", False)

            assert notified or no_prior_disclosures, (
                f"Amendment request {req_id}: propagation record has no notified_parties and "
                "no_prior_disclosures_requiring_notification is not True."
            )


# ===========================================================================
# §164.528 — Accounting of Disclosures
# ===========================================================================

class TestSection164528AccountingOfDisclosures:
    """§164.528 — Individual right to an accounting of disclosures."""

    # -----------------------------------------------------------------------
    # §164.528(c)(1) — 60-day response deadline
    # -----------------------------------------------------------------------

    def test_accounting_requests_responded_within_deadline(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.528(c)(1): CE must act on accounting requests within 60 days.
        One 30-day extension (total 90 days) with written notice within 60 days.
        """
        accounting_log = controls_evidence.get("accounting_request_log", [])

        overdue = []
        for req in accounting_log:
            req_id = req.get("request_id", "unknown")
            received = req.get("received_date")
            responded = req.get("responded_date")
            extension_notice = req.get("extension_notice_sent_date")

            if not received:
                continue

            deadline_initial = received + relativedelta(days=ACCOUNTING_INITIAL_DAYS)
            deadline_extended = received + relativedelta(days=ACCOUNTING_EXTENSION_DAYS)

            if responded is None:
                if reference_date > deadline_initial and extension_notice is None:
                    overdue.append(req_id)
            else:
                if extension_notice:
                    assert extension_notice <= deadline_initial
                    assert responded <= deadline_extended
                else:
                    assert responded <= deadline_initial, (
                        f"Accounting request {req_id}: response {responded} after 60-day "
                        f"deadline {deadline_initial}."
                    )

        assert not overdue, (
            f"§164.528(c)(1): {len(overdue)} accounting request(s) overdue: {overdue}"
        )

    # -----------------------------------------------------------------------
    # §164.528(b)(1) — 6-year lookback and disclosure log required fields
    # -----------------------------------------------------------------------

    def test_disclosure_log_covers_6_year_lookback(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.528(b)(1): The accounting must cover disclosures made in the 6 years
        before the date of the request (not before April 14, 2003).
        CE must maintain a disclosure log covering at least this period.
        """
        disclosure_tracking = controls_evidence.get("phi_disclosure_tracking")

        assert disclosure_tracking is not None, (
            "§164.528: No phi_disclosure_tracking record found. "
            "CE must maintain a log of accountable disclosures for the 6-year lookback."
        )

        log_start_date = disclosure_tracking.get("log_maintained_since")
        assert log_start_date is not None, (
            "§164.528: phi_disclosure_tracking has no log_maintained_since date."
        )

        required_start = reference_date - relativedelta(years=ACCOUNTING_LOOKBACK_YEARS)
        assert log_start_date <= required_start, (
            f"§164.528(b)(1): Disclosure log starts {log_start_date}, but the 6-year lookback "
            f"from {reference_date} requires coverage back to {required_start}."
        )

    @pytest.mark.assumption(
        id="ASSUME-HIPAA-PRIV-ACCT-001",
        description=(
            "Disclosure log required fields (§164.528(b)(2)): each entry must contain: "
            "(1) date of disclosure; (2) name and address of recipient (if known); "
            "(3) brief description of PHI disclosed; (4) brief statement of purpose or "
            "copy of written request. "
            "Accountable disclosures: all disclosures EXCEPT those for TPO, to the individual, "
            "with authorization, incidental to permitted use, as part of a limited dataset, "
            "national security/intelligence, correctional/law enforcement custodians, "
            "or to workforce for CE's activities. "
            "Repeated disclosures of same type (e.g., repeated mandatory public health reports): "
            "first entry + frequency, dates, description of PHI is sufficient."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_disclosure_log_entries_have_required_fields(
        self, controls_evidence: dict
    ):
        """
        Pattern 2 — PARAMETERIZED.
        §164.528(b)(2): Each entry in the accounting disclosure log must contain
        the 4 required fields for each accountable disclosure.
        """
        disclosure_log = controls_evidence.get("phi_disclosure_log", [])

        # Only accountable disclosures need the full entry
        NON_ACCOUNTABLE_BASES = {
            "treatment_payment_operations",
            "individual_request",
            "authorization_on_file",
            "incidental_to_permitted_use",
            "limited_dataset_514e",
            "national_security_intelligence",
            "correctional_law_enforcement_custodians",
            "workforce_ce_activities",
        }

        required_fields = {
            "disclosure_date",
            "recipient_name",
            "phi_description",
            "purpose_or_written_request",
        }

        incomplete = []
        for disc in disclosure_log:
            disc_id = disc.get("disclosure_id", "unknown")
            if disc.get("permissibility_basis") in NON_ACCOUNTABLE_BASES:
                continue  # not accountable, no entry required

            present = set(k for k, v in disc.items() if v is not None)
            missing = required_fields - present

            if missing:
                incomplete.append({"disclosure_id": disc_id, "missing_fields": missing})

        assert not incomplete, (
            f"§164.528(b)(2): {len(incomplete)} accountable disclosure log entries are "
            f"missing required fields: {incomplete}."
        )


# ===========================================================================
# §164.400–414 — Breach Notification
# ===========================================================================

class TestSection164400BreachNotification:
    """§164.400–414 — Notification in case of breach of unsecured PHI."""

    # -----------------------------------------------------------------------
    # §164.404(b) — Individual notification: 60 days from discovery
    # -----------------------------------------------------------------------

    def test_individual_breach_notification_within_60_days(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.404(b): Following discovery of a breach, CE must notify each affected
        individual within 60 calendar days of discovery.
        Discovery date: date CE (or BA acting on its behalf) knew or should have known
        by exercising reasonable diligence.
        """
        breach_log = controls_evidence.get("phi_breach_log", [])

        violations = []
        for breach in breach_log:
            breach_id = breach.get("breach_id", "unknown")
            discovery_date = breach.get("discovery_date")
            is_unsecured_phi = breach.get("involves_unsecured_phi", True)

            if not is_unsecured_phi or not discovery_date:
                continue

            deadline = discovery_date + relativedelta(days=BREACH_INDIVIDUAL_NOTICE_DAYS)
            individual_notice_date = breach.get("individual_notification_date")

            if individual_notice_date is None:
                if reference_date > deadline:
                    violations.append({
                        "breach_id": breach_id,
                        "discovery_date": discovery_date,
                        "deadline": deadline,
                        "issue": "no_notification_deadline_passed",
                    })
            else:
                if individual_notice_date > deadline:
                    violations.append({
                        "breach_id": breach_id,
                        "discovery_date": discovery_date,
                        "notification_date": individual_notice_date,
                        "deadline": deadline,
                        "issue": "notification_late",
                    })

        assert not violations, (
            f"§164.404(b): {len(violations)} breach(es) with individual notification "
            f"violations: {violations}"
        )

    # -----------------------------------------------------------------------
    # §164.406 — Media notification: >500 affected in a state/jurisdiction
    # -----------------------------------------------------------------------

    def test_media_notification_for_large_breaches(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.406: For breaches affecting more than 500 residents of a state or jurisdiction,
        CE must notify prominent media outlets in that jurisdiction within 60 days of discovery.
        """
        breach_log = controls_evidence.get("phi_breach_log", [])

        for breach in breach_log:
            breach_id = breach.get("breach_id", "unknown")
            discovery_date = breach.get("discovery_date")
            if not discovery_date or not breach.get("involves_unsecured_phi", True):
                continue

            affected_by_jurisdiction = breach.get("affected_individuals_by_jurisdiction", {})

            for jurisdiction, count in affected_by_jurisdiction.items():
                if count <= 500:
                    continue

                deadline = discovery_date + relativedelta(days=BREACH_MEDIA_NOTICE_DAYS)
                media_notice_date = breach.get(f"media_notification_date_{jurisdiction}")

                if media_notice_date is None:
                    if reference_date > deadline:
                        pytest.fail(
                            f"§164.406: Breach '{breach_id}' affected {count} individuals "
                            f"in {jurisdiction} — media notification required by {deadline}. "
                            "No media notification recorded."
                        )
                else:
                    assert media_notice_date <= deadline, (
                        f"§164.406: Breach '{breach_id}' — media notification for {jurisdiction} "
                        f"sent {media_notice_date}, after 60-day deadline {deadline}."
                    )

    # -----------------------------------------------------------------------
    # §164.408 — HHS notification
    # -----------------------------------------------------------------------

    def test_hhs_notification_for_large_breaches_within_60_days(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.408(b): For breaches affecting 500 or more individuals, CE must notify
        HHS Secretary contemporaneously (within 60 days of discovery).
        """
        breach_log = controls_evidence.get("phi_breach_log", [])

        for breach in breach_log:
            breach_id = breach.get("breach_id", "unknown")
            discovery_date = breach.get("discovery_date")
            total_affected = breach.get("total_affected_individuals", 0)

            if not discovery_date or not breach.get("involves_unsecured_phi", True):
                continue
            if total_affected < 500:
                continue

            deadline = discovery_date + relativedelta(days=BREACH_HHS_LARGE_DAYS)
            hhs_notice_date = breach.get("hhs_notification_date")

            if hhs_notice_date is None:
                if reference_date > deadline:
                    pytest.fail(
                        f"§164.408(b): Breach '{breach_id}' affected {total_affected} individuals — "
                        f"HHS notification required by {deadline}. No notification recorded."
                    )
            else:
                assert hhs_notice_date <= deadline, (
                    f"§164.408(b): Breach '{breach_id}' HHS notification {hhs_notice_date} "
                    f"is after 60-day deadline {deadline}."
                )

    def test_small_breach_hhs_annual_log_submitted_on_time(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.408(c): For breaches affecting fewer than 500 individuals, CE must log
        the breaches and submit the annual log to HHS no later than 60 days after
        the end of each calendar year (i.e., by March 1 of the following year,
        or February 29 in a leap year — rule states 60 days after calendar year end).
        """
        hhs_annual_logs = controls_evidence.get("hhs_annual_breach_log_submissions", [])

        for log in hhs_annual_logs:
            calendar_year = log.get("calendar_year")
            submission_date = log.get("submission_date")

            if not calendar_year or not submission_date:
                continue

            year_end = date(calendar_year, 12, 31)
            deadline = year_end + relativedelta(days=60)

            assert submission_date <= deadline, (
                f"§164.408(c): HHS annual breach log for calendar year {calendar_year} "
                f"submitted {submission_date}, after 60-day deadline {deadline}."
            )

    # -----------------------------------------------------------------------
    # §164.402 — Unsecured PHI determination (4-factor harm assessment)
    # -----------------------------------------------------------------------

    @pytest.mark.assumption(
        id="ASSUME-HIPAA-PRIV-BREACH-001",
        description=(
            "Unsecured PHI definition (§164.402): PHI that has not been rendered unusable, "
            "unreadable, or indecipherable through encryption (NIST SP 800-111) or destruction. "
            "4-factor low-probability-of-compromise assessment (§164.402(2)): "
            "(1) nature and extent of PHI involved (types and likelihood of re-identification); "
            "(2) who accessed/received the PHI; "
            "(3) whether PHI was actually acquired or viewed; "
            "(4) extent to which risk has been mitigated. "
            "Assumption: if any factor cannot be determined with a low-probability conclusion, "
            "the incident is treated as a breach. Documentation of the 4-factor assessment "
            "is required for every incident that could be a breach — even if ultimately "
            "determined not to be. Privacy Officer must review all assessments."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_breach_determination_documents_4_factor_assessment(
        self, controls_evidence: dict
    ):
        """
        Pattern 2 — PARAMETERIZED.
        §164.402(2): When an incident could constitute a breach, CE must perform a
        4-factor harm assessment to determine whether a low probability of compromise
        exists. If it cannot be determined to be low probability, it is a breach.
        Assessment must be documented regardless of conclusion.
        """
        privacy_incidents = controls_evidence.get("privacy_incident_log", [])

        required_assessment_factors = {
            "nature_and_extent_of_phi",
            "who_accessed_or_received",
            "whether_phi_acquired_or_viewed",
            "risk_mitigation_extent",
        }

        for incident in privacy_incidents:
            incident_id = incident.get("incident_id", "unknown")
            involves_phi = incident.get("potentially_involves_phi", False)

            if not involves_phi:
                continue

            assessment = incident.get("four_factor_harm_assessment")
            assert assessment is not None, (
                f"Privacy incident '{incident_id}': no four_factor_harm_assessment documented. "
                "§164.402(2): every potential PHI incident must have a documented 4-factor "
                "assessment to determine breach status."
            )

            factors_assessed = set(assessment.get("factors_assessed", []))
            missing = required_assessment_factors - factors_assessed

            assert not missing, (
                f"Privacy incident '{incident_id}': 4-factor assessment is missing "
                f"factors: {missing}."
            )

            conclusion = assessment.get("conclusion")
            assert conclusion in ("breach", "not_a_breach_low_probability"), (
                f"Privacy incident '{incident_id}': assessment conclusion '{conclusion}' "
                "is not valid — must be 'breach' or 'not_a_breach_low_probability'."
            )

            reviewer = assessment.get("reviewed_by")
            assert reviewer == "Privacy Officer" or "Privacy Officer" in str(reviewer), (
                f"Privacy incident '{incident_id}': 4-factor assessment reviewed by "
                f"'{reviewer}' — must be reviewed by the Privacy Officer."
            )
