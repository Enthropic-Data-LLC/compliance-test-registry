# SOC 2 — Privacy Criteria (P Series)
# AICPA Trust Services Criteria 2017, P1–P8
# Based on Generally Accepted Privacy Principles (GAPP)
#
# Scope note: SOC 2 Privacy criteria are framework-neutral. They require the entity to
# (a) state privacy commitments in a privacy notice, and (b) operate in accordance with
# those commitments. DETERMINISTIC thresholds are therefore driven by the entity's stated
# commitments and applicable law — not by fixed SOC 2 thresholds. The assessor validates
# that practice matches promise.
#
# Pattern guide:
#   Pattern 1 — direct assert — DETERMINISTIC (entity committed to a specific threshold)
#   Pattern 2 — @pytest.mark.assumption(...) — PARAMETERIZED
#   Pattern 3 — @pytest.mark.human_review_required(...) — CONTESTED
#
# New assumptions introduced in this file:
#   ASSUME-SOC2-P1-001   P1 — Privacy notice required elements; material change update trigger
#   ASSUME-SOC2-P2-001   P2 — Consent mechanism adequacy; withdrawal timeline
#   ASSUME-SOC2-P3-001   P3 — Collection limitation; sensitive data explicit consent
#   ASSUME-SOC2-P4-001   P4 — Retention schedule; disposal documentation
#   ASSUME-SOC2-P5-001   P5 — Subject access response timeline; correction procedure
#   ASSUME-SOC2-P6-001   P6 — Third-party privacy contracts; breach notification timeline
#   ASSUME-SOC2-P7-001   P7 — Data accuracy; correction and update mechanism
#   ASSUME-SOC2-P8-001   P8 — Privacy program monitoring; incident handling; annual review

import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


# ---------------------------------------------------------------------------
# Scope pre-condition
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def soc2_privacy_scope_check(entity_profile: dict):
    """
    SOC 2 Privacy criteria (P series) are optional — applicable only when the
    entity has included Privacy in its SOC 2 engagement scope.
    Skip all tests if Privacy criteria are not in scope.
    """
    if not entity_profile.get("soc2_privacy_criteria_in_scope", False):
        pytest.skip(
            "SOC 2 Privacy criteria (P1–P8) are not in scope for this engagement. "
            "Set entity_profile['soc2_privacy_criteria_in_scope'] = True to enable."
        )


@pytest.fixture(autouse=True)
def soc2_system_boundary_check(entity_profile: dict, reference_date: date):
    """
    All SOC 2 criteria require a current system description. Stale system description
    is a block across all criteria (CC2.3 requirement, extends to Privacy criteria).
    """
    system_desc_reviewed = entity_profile.get("system_description_last_reviewed_date")
    if system_desc_reviewed is None:
        pytest.skip("System description has never been reviewed — system boundary undefined.")
    max_age_days = 365
    age = (reference_date - system_desc_reviewed).days
    if age > max_age_days:
        pytest.skip(
            f"System description is {age} days old (last reviewed: {system_desc_reviewed}). "
            "System description must be reviewed within the last 12 months before "
            "SOC 2 Privacy criteria tests are meaningful."
        )


# ---------------------------------------------------------------------------
# Shared constants — derived from entity's stated privacy commitments
# ---------------------------------------------------------------------------

def get_privacy_commitments(entity_profile: dict) -> dict:
    """
    Returns the entity's stated privacy commitments from the privacy notice.
    All DETERMINISTIC thresholds in the P series are commitment-relative.
    """
    return entity_profile.get("privacy_commitments", {})


# ===========================================================================
# P1 — Privacy Notice
# Criteria: P1.1–P1.5
# Entity communicates privacy practices to data subjects before or at collection.
# ===========================================================================

class TestP1PrivacyNotice:
    """P1 — Privacy Notice: entity communicates its privacy practices."""

    def test_privacy_notice_exists_and_is_current(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        P1.1: The entity provides notice about its privacy practices. Existence of a
        current privacy notice is binary. A notice not updated after a material change
        to privacy practices is not current.
        """
        privacy_notice = controls_evidence.get("privacy_notice")
        assert privacy_notice is not None, (
            "P1.1: No privacy_notice record found. A current privacy notice is required "
            "when the Privacy criteria are in scope."
        )

        effective_date = privacy_notice.get("effective_date")
        assert effective_date is not None, "P1.1: Privacy notice has no effective_date."

        # Notice must be newer than the most recent material change
        last_material_change = controls_evidence.get("privacy_notice_last_material_change_date")
        if last_material_change:
            assert effective_date >= last_material_change, (
                f"P1.1: Privacy notice effective {effective_date} predates the last material "
                f"privacy change ({last_material_change}). Notice must be updated after "
                "material changes to privacy practices."
            )

    @pytest.mark.assumption(
        id="ASSUME-SOC2-P1-001",
        description=(
            "Privacy notice required elements (P1.2): notice must contain at minimum — "
            "(1) identity of the entity; (2) categories of personal information collected; "
            "(3) purposes for collection and use; (4) categories of third parties to whom "
            "disclosed; (5) individual rights (access, correction, objection/opt-out); "
            "(6) retention period or criteria; (7) contact for privacy questions/complaints; "
            "(8) effective date of notice. "
            "Material change trigger (P1.3): notice updated and individuals notified within 30 days "
            "of material change to collection, use, disclosure, or retention practices. "
            "Notice provided before or at time of collection (P1.5)."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_privacy_notice_contains_required_elements(self, controls_evidence: dict):
        """
        Pattern 2 — PARAMETERIZED.
        P1.2: Privacy notice must contain 8 required elements. Content adequacy
        of descriptions is PARAMETERIZED; existence of each element is testable.
        """
        privacy_notice = controls_evidence.get("privacy_notice", {})

        required_elements = {
            "entity_identity",
            "categories_of_personal_information_collected",
            "purposes_for_collection_and_use",
            "third_party_disclosure_categories",
            "individual_rights_description",
            "retention_period_or_criteria",
            "privacy_contact_information",
            "notice_effective_date",
        }

        present = set(privacy_notice.get("elements_present", []))
        missing = required_elements - present

        assert not missing, (
            f"P1.2: Privacy notice is missing required elements: {missing}."
        )

    def test_privacy_notice_provided_at_or_before_collection(
        self, controls_evidence: dict
    ):
        """
        Pattern 1 — DETERMINISTIC.
        P1.5: Personal information must not be collected from individuals before providing
        notice. Evidence: collection forms/flows include a notice link/reference; documented
        in privacy notice delivery procedure.
        """
        notice_delivery = controls_evidence.get("privacy_notice_delivery_procedure")

        assert notice_delivery is not None, (
            "P1.5: No privacy_notice_delivery_procedure documented. "
            "Notice must be provided before or at time of personal information collection."
        )

        delivery_timing = notice_delivery.get("delivery_timing")
        assert delivery_timing in ("before_collection", "at_time_of_collection"), (
            f"P1.5: delivery_timing '{delivery_timing}' does not satisfy the requirement "
            "for notice before or at collection."
        )

    def test_privacy_notice_updated_after_material_change(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        P1.3: When privacy practices change materially, the notice must be updated
        and individuals notified within the entity's stated timeline (assumed: 30 days).
        """
        NOTICE_UPDATE_DAYS = 30

        change_log = controls_evidence.get("privacy_notice_material_change_log", [])
        privacy_notice = controls_evidence.get("privacy_notice", {})

        for change in change_log:
            change_id = change.get("change_id", "unknown")
            effective_date = change.get("effective_date")
            notice_updated_date = change.get("notice_updated_date")

            if not effective_date:
                continue

            deadline = effective_date + relativedelta(days=NOTICE_UPDATE_DAYS)

            if notice_updated_date is None:
                if reference_date > deadline:
                    pytest.fail(
                        f"P1.3: Material privacy change '{change_id}' effective {effective_date} — "
                        f"notice not updated. Deadline: {deadline}."
                    )
            else:
                assert notice_updated_date <= deadline, (
                    f"P1.3: Privacy notice for change '{change_id}' updated {notice_updated_date}, "
                    f"after 30-day deadline {deadline}."
                )

    @pytest.mark.assumption(
        id="ASSUME-SOC2-P1-001",
        description=(
            "Third-party privacy commitment communication (P1.4): the entity communicates "
            "privacy commitments to third parties (vendors, partners) who receive personal "
            "information. Communication channel: privacy provisions in contracts or DPAs; "
            "third-party privacy questionnaire for high-risk processors. "
            "Timing: at contract execution or before personal information is shared."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_privacy_commitments_communicated_to_third_parties(
        self, controls_evidence: dict
    ):
        """
        Pattern 2 — PARAMETERIZED.
        P1.4: The entity communicates its privacy commitments to third parties to
        whom personal information is disclosed. Privacy clauses in contracts are the
        primary evidence mechanism.
        """
        third_party_disclosures = controls_evidence.get(
            "third_party_personal_information_disclosures", []
        )

        for tp in third_party_disclosures:
            tp_id = tp.get("third_party_id", "unknown")
            privacy_commitments_communicated = tp.get("privacy_commitments_in_contract", False)
            is_exempt = tp.get("disclosure_to_individual_or_legal", False)

            if is_exempt:
                continue

            assert privacy_commitments_communicated, (
                f"P1.4: Third party '{tp_id}' receives personal information but "
                "privacy_commitments_in_contract is not True. Privacy commitments must "
                "be communicated via contract or DPA before disclosure."
            )


# ===========================================================================
# P2 — Choice and Consent
# Criteria: P2.1, P2.2
# ===========================================================================

class TestP2ChoiceAndConsent:
    """P2 — Choice and Consent: individuals have choice over use of their information."""

    @pytest.mark.assumption(
        id="ASSUME-SOC2-P2-001",
        description=(
            "Consent mechanism adequacy (P2.1): for non-sensitive personal information, "
            "implied consent (opt-out) is acceptable if the purpose is described in the notice. "
            "For sensitive personal information (health, financial, biometric, SSN, precise "
            "geolocation, children's data), explicit opt-in is required. "
            "Withdrawal timeline: consent withdrawal requests processed within 30 days; "
            "processing for the consented purpose ceases upon withdrawal. "
            "Consent withdrawal does not affect processing already completed. "
            "Evidence: consent records with timestamp, mechanism, and purposes consented to."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_consent_mechanism_exists_for_stated_purposes(
        self, controls_evidence: dict
    ):
        """
        Pattern 2 — PARAMETERIZED.
        P2.1: The entity provides individuals with a mechanism to opt out of uses/disclosures
        not required or not for primary purposes. For sensitive data, opt-in mechanism required.
        """
        consent_mechanisms = controls_evidence.get("consent_mechanisms", [])

        assert len(consent_mechanisms) > 0, (
            "P2.1: No consent_mechanisms documented. The entity must provide individuals "
            "with mechanisms to exercise choice over their personal information."
        )

        for mechanism in consent_mechanisms:
            mech_id = mechanism.get("mechanism_id", "unknown")
            data_type = mechanism.get("data_type", "standard")
            mechanism_type = mechanism.get("mechanism_type")

            if data_type == "sensitive":
                assert mechanism_type == "opt_in", (
                    f"P2.1: Consent mechanism '{mech_id}' covers sensitive personal information "
                    f"but uses mechanism_type '{mechanism_type}'. Sensitive data requires opt-in consent."
                )
            else:
                assert mechanism_type in ("opt_in", "opt_out"), (
                    f"P2.1: Consent mechanism '{mech_id}' mechanism_type '{mechanism_type}' "
                    "is not opt_in or opt_out."
                )

    def test_consent_withdrawal_honored(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        P2.2: The entity honors requests to withdraw consent. Once withdrawn, processing
        for the consented purpose must cease. Processing already completed is unaffected.
        """
        WITHDRAWAL_PROCESSING_DAYS = 30

        withdrawal_log = controls_evidence.get("consent_withdrawal_log", [])

        overdue = []
        for req in withdrawal_log:
            req_id = req.get("request_id", "unknown")
            received = req.get("received_date")
            processing_ceased_date = req.get("processing_ceased_date")
            still_processing = req.get("processing_continues_after_withdrawal", False)

            if still_processing:
                overdue.append({"request_id": req_id, "issue": "processing_not_ceased"})
                continue

            if received and processing_ceased_date is None:
                deadline = received + relativedelta(days=WITHDRAWAL_PROCESSING_DAYS)
                if reference_date > deadline:
                    overdue.append({"request_id": req_id, "issue": "no_cessation_date_recorded"})

        assert not overdue, (
            f"P2.2: {len(overdue)} consent withdrawal request(s) not honored: {overdue}"
        )

    @pytest.mark.human_review_required(
        reason=(
            "P2.2: Whether a consent mechanism is 'adequate' given the entity's privacy notice "
            "and applicable law is a judgment call requiring assessment of: the clarity of the "
            "opt-out/opt-in mechanism, accessibility to affected individuals, whether implied "
            "consent is appropriate for the data category and purpose, and whether the mechanism "
            "is technically effective. Required: annual Privacy Officer review of all consent "
            "mechanisms against current privacy notice and applicable regulatory guidance."
        )
    )
    def test_consent_mechanism_adequacy_attested(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 3 — CONTESTED.
        P2.1: Adequacy of consent mechanisms requires annual Privacy Officer attestation.
        Automated tests can verify mechanism existence but not adequacy.
        """
        attestation = controls_evidence.get("consent_mechanism_annual_attestation")

        assert attestation is not None, (
            "P2: No consent_mechanism_annual_attestation found. "
            "Annual Privacy Officer review of consent mechanisms is required."
        )

        attestation_date = attestation.get("attestation_date")
        assert attestation_date is not None
        assert (reference_date - attestation_date).days <= 365, (
            f"P2: Consent mechanism attestation is overdue (last: {attestation_date})."
        )


# ===========================================================================
# P3 — Collection
# Criteria: P3.1, P3.2
# ===========================================================================

class TestP3Collection:
    """P3 — Collection: personal information collected only as described in notice."""

    def test_collection_limited_to_stated_purposes(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        P3.1: Personal information collected is consistent with the entity's privacy notice.
        Any personal information category not described in the notice is an impermissible
        collection.
        """
        privacy_notice = controls_evidence.get("privacy_notice", {})
        notified_categories = set(
            privacy_notice.get("categories_of_personal_information_collected", [])
        )

        actual_collection = controls_evidence.get("personal_information_inventory", {})
        collected_categories = set(actual_collection.get("categories_actually_collected", []))

        undisclosed_categories = collected_categories - notified_categories
        assert not undisclosed_categories, (
            f"P3.1: Personal information categories are collected but not described in the "
            f"privacy notice: {undisclosed_categories}. Collection must match notice."
        )

    @pytest.mark.assumption(
        id="ASSUME-SOC2-P3-001",
        description=(
            "Sensitive personal information collection (P3.2): requires explicit consent before "
            "collection unless an exception applies (legal obligation, vital interests, public task, "
            "legitimate interests proportionate to sensitivity). "
            "Sensitive categories: health/medical, financial account numbers, SSN/government ID, "
            "biometric, precise geolocation, racial/ethnic origin, sexual orientation, children's data. "
            "Evidence: consent records timestamped before collection; data flow diagram confirms "
            "consent gate precedes data storage."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_sensitive_data_collection_has_explicit_consent_or_exception(
        self, controls_evidence: dict
    ):
        """
        Pattern 2 — PARAMETERIZED.
        P3.2: For sensitive categories of personal information, explicit consent or a
        documented exception must exist before collection.
        """
        SENSITIVE_CATEGORIES = {
            "health_medical",
            "financial_account_numbers",
            "government_id_ssn",
            "biometric",
            "precise_geolocation",
            "racial_ethnic_origin",
            "sexual_orientation",
            "children_data_under_13",
        }

        PERMITTED_EXCEPTIONS = {
            "legal_obligation",
            "vital_interests",
            "public_task",
            "legitimate_interests_documented",
            "explicit_consent_on_file",
        }

        actual_collection = controls_evidence.get("personal_information_inventory", {})
        collected_sensitive = [
            item for item in actual_collection.get("collection_details", [])
            if item.get("category") in SENSITIVE_CATEGORIES
        ]

        for item in collected_sensitive:
            item_id = item.get("category", "unknown")
            basis = item.get("collection_basis")

            assert basis in PERMITTED_EXCEPTIONS, (
                f"P3.2: Sensitive personal information '{item_id}' collected but basis "
                f"'{basis}' is not in permitted exceptions: {PERMITTED_EXCEPTIONS}."
            )


# ===========================================================================
# P4 — Use, Retention, and Disposal
# Criteria: P4.1, P4.2, P4.3
# ===========================================================================

class TestP4UseRetentionDisposal:
    """P4 — Personal information used only for stated purposes; retained appropriately; disposed securely."""

    def test_personal_information_used_only_for_stated_purposes(
        self, controls_evidence: dict
    ):
        """
        Pattern 1 — DETERMINISTIC.
        P4.1: Personal information must not be used for purposes not described in the
        privacy notice unless additional consent is obtained or a legal basis applies.
        """
        privacy_notice = controls_evidence.get("privacy_notice", {})
        stated_purposes = set(privacy_notice.get("purposes_for_collection_and_use", []))

        processing_log = controls_evidence.get("personal_information_processing_log", [])

        violations = []
        for activity in processing_log:
            activity_id = activity.get("activity_id", "unknown")
            purpose = activity.get("purpose")
            additional_consent = activity.get("additional_consent_obtained", False)
            legal_basis = activity.get("legal_basis_exception")

            if purpose not in stated_purposes and not additional_consent and not legal_basis:
                violations.append({
                    "activity_id": activity_id,
                    "purpose": purpose,
                })

        assert not violations, (
            f"P4.1: {len(violations)} processing activities use personal information for "
            f"purposes not in the privacy notice without additional consent or legal basis: "
            f"{violations}."
        )

    @pytest.mark.assumption(
        id="ASSUME-SOC2-P4-001",
        description=(
            "Retention schedule (P4.2): each category of personal information has a documented "
            "retention period tied to the business purpose. Retention schedules reviewed annually. "
            "Automated deletion/archival triggers are configured per schedule. "
            "Disposal method (P4.3): digital records — cryptographic erasure or NIST SP 800-88 "
            "Purge/Clear/Destroy as appropriate for media type; paper records — cross-cut shredding "
            "or equivalent; certificates of disposal for high-sensitivity data. "
            "Disposal documented: date, category, method, approver."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_retention_schedules_exist_per_data_category(self, controls_evidence: dict):
        """
        Pattern 2 — PARAMETERIZED.
        P4.2: Retention schedules must be documented per personal information category,
        aligned with the privacy notice, and reviewed annually.
        """
        retention_schedule = controls_evidence.get("personal_information_retention_schedule")

        assert retention_schedule is not None, (
            "P4.2: No personal_information_retention_schedule found. "
            "Retention schedules must be documented per personal information category."
        )

        schedule_entries = retention_schedule.get("entries", [])
        assert len(schedule_entries) > 0, (
            "P4.2: Retention schedule has no entries. Each collected personal information "
            "category must have a documented retention period."
        )

        last_reviewed = retention_schedule.get("last_reviewed_date")
        assert last_reviewed is not None, (
            "P4.2: Retention schedule has no last_reviewed_date. Annual review required."
        )

    def test_disposal_of_personal_information_documented(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        P4.3: When personal information is disposed of, the disposal must be documented.
        Absence of a disposal record for information known to have passed its retention
        period is a gap. Documentation must include: category, date, method, approver.
        """
        disposal_log = controls_evidence.get("personal_information_disposal_log", [])

        REQUIRED_DISPOSAL_FIELDS = {
            "data_category",
            "disposal_date",
            "disposal_method",
            "approved_by",
        }

        incomplete = []
        for entry in disposal_log:
            entry_id = entry.get("disposal_id", "unknown")
            present = set(k for k, v in entry.items() if v is not None)
            missing = REQUIRED_DISPOSAL_FIELDS - present

            if missing:
                incomplete.append({"disposal_id": entry_id, "missing_fields": missing})

        assert not incomplete, (
            f"P4.3: {len(incomplete)} disposal log entries are missing required fields: {incomplete}."
        )


# ===========================================================================
# P5 — Access
# Criteria: P5.1, P5.2
# ===========================================================================

class TestP5Access:
    """P5 — Individuals can access and correct their personal information."""

    @pytest.mark.assumption(
        id="ASSUME-SOC2-P5-001",
        description=(
            "Subject access request response timeline (P5.1): the entity's privacy notice "
            "commits to responding to access requests within 30 days (extendable to 60 days "
            "with notice). This matches GDPR Art. 12 and HIPAA §164.524 for cross-framework "
            "alignment. If the entity's stated commitment differs, use that instead. "
            "Access log must capture: received date, responded date, format provided, "
            "partial/full fulfillment, denial reason if applicable. "
            "Correction procedure (P5.2): acknowledged within 10 days; correction or denial "
            "within 30 days of receipt; denial must include reason and appeal mechanism."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_access_requests_responded_within_committed_timeline(
        self, controls_evidence: dict, entity_profile: dict, reference_date: date
    ):
        """
        Pattern 2 — PARAMETERIZED.
        P5.1: Subject access requests must be responded to within the entity's stated
        commitment (default assumption: 30 days). Pattern 2 because the deadline is
        org-defined; if the entity commits to 30 days it becomes DETERMINISTIC.
        """
        commitments = get_privacy_commitments(entity_profile)
        ACCESS_RESPONSE_DAYS = commitments.get("access_request_response_days", 30)

        access_log = controls_evidence.get("subject_access_request_log", [])

        overdue = []
        for req in access_log:
            req_id = req.get("request_id", "unknown")
            received = req.get("received_date")
            responded = req.get("responded_date")
            extension_notice = req.get("extension_notice_sent_date")

            if not received:
                continue

            deadline = received + relativedelta(days=ACCESS_RESPONSE_DAYS)
            extended_deadline = received + relativedelta(days=ACCESS_RESPONSE_DAYS * 2)

            if responded is None:
                if extension_notice is None and reference_date > deadline:
                    overdue.append(req_id)
            else:
                effective_deadline = extended_deadline if extension_notice else deadline
                if responded > effective_deadline:
                    overdue.append(req_id)

        assert not overdue, (
            f"P5.1: {len(overdue)} subject access request(s) responded outside the "
            f"{ACCESS_RESPONSE_DAYS}-day committed timeline: {overdue}"
        )

    def test_correction_requests_acknowledged_and_resolved(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        P5.2: Individuals must be able to request correction of inaccurate personal information.
        Every correction request must have a documented outcome — corrected or denied with reason.
        """
        correction_log = controls_evidence.get("personal_information_correction_log", [])

        unresolved = []
        for req in correction_log:
            req_id = req.get("request_id", "unknown")
            outcome = req.get("outcome")

            if outcome not in ("corrected", "denied_accurate", "denied_not_held", "withdrawn"):
                if outcome is None:
                    received = req.get("received_date")
                    if received:
                        age = (reference_date - received).days
                        if age > 30:
                            unresolved.append({
                                "request_id": req_id,
                                "age_days": age,
                                "issue": "no_outcome_after_30_days",
                            })

        assert not unresolved, (
            f"P5.2: {len(unresolved)} correction request(s) have no documented outcome "
            f"after 30 days: {unresolved}."
        )


# ===========================================================================
# P6 — Disclosure to Third Parties
# Criteria: P6.1–P6.7
# ===========================================================================

class TestP6DisclosureToThirdParties:
    """P6 — Personal information disclosed only as described; third parties bound by privacy obligations."""

    def test_third_party_disclosures_match_privacy_notice(
        self, controls_evidence: dict
    ):
        """
        Pattern 1 — DETERMINISTIC.
        P6.1: Personal information must not be disclosed to third parties not described
        in the privacy notice unless additional consent is obtained or a legal basis applies.
        """
        privacy_notice = controls_evidence.get("privacy_notice", {})
        disclosed_to_categories = set(
            privacy_notice.get("third_party_disclosure_categories", [])
        )

        actual_disclosures = controls_evidence.get(
            "third_party_personal_information_disclosures", []
        )

        violations = []
        for disc in actual_disclosures:
            disc_id = disc.get("disclosure_id", "unknown")
            recipient_category = disc.get("recipient_category")
            additional_consent = disc.get("additional_consent_obtained", False)
            legal_basis = disc.get("legal_basis_exception")

            if (
                recipient_category not in disclosed_to_categories
                and not additional_consent
                and not legal_basis
            ):
                violations.append({
                    "disclosure_id": disc_id,
                    "recipient_category": recipient_category,
                })

        assert not violations, (
            f"P6.1: {len(violations)} disclosure(s) to third parties not described "
            f"in the privacy notice: {violations}."
        )

    @pytest.mark.assumption(
        id="ASSUME-SOC2-P6-001",
        description=(
            "Third-party privacy contracts (P6.2): all third parties to whom personal information "
            "is disclosed must be contractually bound to equivalent privacy protections. "
            "Contract must include: (1) use limitation to stated purposes; "
            "(2) security measures appropriate to data sensitivity; "
            "(3) privacy incident notification to entity within 72 hours of discovery; "
            "(4) no onward transfer without entity's consent; "
            "(5) return/destroy at contract termination. "
            "Breach notification timeline (P6.6/P6.7): aligned to most restrictive applicable "
            "regulation — default 72 hours from discovery for GDPR-subject data; "
            "60 days for HIPAA PHI. Entity's privacy notice states its commitment to individuals."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_third_party_privacy_contracts_contain_required_terms(
        self, controls_evidence: dict
    ):
        """
        Pattern 2 — PARAMETERIZED.
        P6.2: Third-party recipients of personal information must be contractually bound
        to privacy protections equivalent to the entity's commitments.
        """
        third_party_disclosures = controls_evidence.get(
            "third_party_personal_information_disclosures", []
        )

        REQUIRED_CONTRACT_TERMS = {
            "use_limitation_to_stated_purposes",
            "appropriate_security_measures",
            "incident_notification_to_entity",
            "no_onward_transfer_without_consent",
            "return_or_destroy_at_termination",
        }

        for tp in third_party_disclosures:
            tp_id = tp.get("third_party_id", "unknown")
            is_individual = tp.get("recipient_is_the_individual", False)
            is_legal_requirement = tp.get("disclosure_required_by_law", False)

            if is_individual or is_legal_requirement:
                continue

            contract_terms = set(tp.get("privacy_contract_terms_present", []))
            missing = REQUIRED_CONTRACT_TERMS - contract_terms

            assert not missing, (
                f"P6.2: Third party '{tp_id}' privacy contract is missing terms: {missing}."
            )

    def test_privacy_incident_notification_to_individuals_on_time(
        self, controls_evidence: dict, entity_profile: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC (against entity's stated commitment).
        P6.6/P6.7: When a privacy incident affects personal information, the entity
        must notify affected individuals within its stated commitment timeline.
        Default assumption: 72 hours for high-risk incidents; 30 days for others.
        """
        commitments = get_privacy_commitments(entity_profile)
        HIGH_RISK_NOTIFICATION_HOURS = commitments.get(
            "high_risk_incident_notification_hours", 72
        )
        STANDARD_NOTIFICATION_DAYS = commitments.get(
            "standard_incident_notification_days", 30
        )

        incident_log = controls_evidence.get("privacy_incident_log", [])

        violations = []
        for incident in incident_log:
            incident_id = incident.get("incident_id", "unknown")
            is_high_risk = incident.get("classified_high_risk", False)
            discovery_date = incident.get("discovery_date")
            individual_notification_date = incident.get("individual_notification_date")
            notification_required = incident.get("individual_notification_required", True)

            if not notification_required or not discovery_date:
                continue

            if is_high_risk:
                deadline = discovery_date + relativedelta(
                    hours=HIGH_RISK_NOTIFICATION_HOURS
                )
            else:
                deadline = discovery_date + relativedelta(days=STANDARD_NOTIFICATION_DAYS)

            if individual_notification_date is None:
                if reference_date > deadline.date() if hasattr(deadline, 'date') else deadline:
                    violations.append({
                        "incident_id": incident_id,
                        "discovery_date": discovery_date,
                        "deadline": str(deadline),
                        "issue": "no_notification",
                    })
            else:
                notification_dt = individual_notification_date
                if not is_high_risk:
                    if notification_dt > deadline:
                        violations.append({
                            "incident_id": incident_id,
                            "notification_date": str(notification_dt),
                            "deadline": str(deadline),
                        })

        assert not violations, (
            f"P6.6/P6.7: {len(violations)} privacy incident(s) with notification "
            f"violations: {violations}"
        )


# ===========================================================================
# P7 — Quality
# Criterion: P7.1
# ===========================================================================

class TestP7Quality:
    """P7 — Personal information is accurate, complete, and relevant."""

    @pytest.mark.assumption(
        id="ASSUME-SOC2-P7-001",
        description=(
            "Data quality mechanism (P7.1): the entity must have a mechanism to maintain "
            "personal information as accurate, complete, and relevant for the purpose collected. "
            "Implementation: (1) individuals can update their own information via self-service; "
            "(2) periodic data quality review for non-self-service data (annual at minimum); "
            "(3) source system refresh triggers update of downstream copies; "
            "(4) accuracy review cadence for high-stakes personal information (credit/health/legal) "
            "is more frequent than general data."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_data_quality_mechanism_exists(self, controls_evidence: dict):
        """
        Pattern 2 — PARAMETERIZED.
        P7.1: The entity maintains a mechanism to ensure personal information is accurate,
        complete, and relevant. Mechanism adequacy is PARAMETERIZED.
        """
        quality_mechanism = controls_evidence.get("personal_information_quality_mechanism")

        assert quality_mechanism is not None, (
            "P7.1: No personal_information_quality_mechanism documented. "
            "A mechanism for maintaining data accuracy is required under the Privacy criteria."
        )

        required_fields = {
            "self_service_update_available",
            "periodic_data_quality_review_cadence",
            "last_quality_review_date",
        }
        present = set(quality_mechanism.keys())
        missing = required_fields - present

        assert not missing, (
            f"P7.1: Data quality mechanism is missing fields: {missing}."
        )

    def test_data_quality_review_current(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        P7.1: Data quality review must not be overdue based on the stated cadence.
        Default assumption: annual review.
        """
        quality_mechanism = controls_evidence.get(
            "personal_information_quality_mechanism", {}
        )
        last_review = quality_mechanism.get("last_quality_review_date")

        if last_review is None:
            pytest.fail(
                "P7.1: No last_quality_review_date found. "
                "Annual data quality review is required."
            )

        max_interval_days = 365
        age = (reference_date - last_review).days
        assert age <= max_interval_days, (
            f"P7.1: Data quality review is {age} days old (last: {last_review}). "
            "Annual review required."
        )


# ===========================================================================
# P8 — Monitoring and Enforcement
# Criterion: P8.1
# ===========================================================================

class TestP8MonitoringAndEnforcement:
    """P8 — Privacy program is monitored; incidents handled; program tested annually."""

    @pytest.mark.assumption(
        id="ASSUME-SOC2-P8-001",
        description=(
            "Privacy program monitoring (P8.1): the entity must monitor compliance with its "
            "privacy commitments on an ongoing basis. Implementation: (1) Privacy Officer "
            "conducts annual privacy program review; (2) privacy controls are tested at least "
            "annually as part of the SOC 2 engagement or internal audit; (3) privacy incidents "
            "are tracked in an incident log with root cause analysis for incidents involving "
            "more than 100 individuals or classified as high-risk; (4) privacy complaints "
            "from individuals are tracked and responded to within 30 days; "
            "(5) unresolved material privacy issues escalated to senior management/board."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_privacy_program_annual_review_current(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 2 — PARAMETERIZED.
        P8.1: Privacy Officer must conduct an annual review of the privacy program,
        covering: notice accuracy, consent mechanisms, access rights fulfillment,
        third-party compliance, incident handling, and emerging legal obligations.
        """
        annual_review = controls_evidence.get("privacy_program_annual_review")

        assert annual_review is not None, (
            "P8.1: No privacy_program_annual_review found. "
            "Annual Privacy Officer review of the privacy program is required."
        )

        review_date = annual_review.get("review_date")
        reviewed_by = annual_review.get("reviewed_by")

        assert review_date is not None, "P8.1: Annual review has no review_date."
        assert (reference_date - review_date).days <= 365, (
            f"P8.1: Privacy program annual review is overdue (last: {review_date})."
        )
        assert reviewed_by == "Privacy Officer" or "Privacy Officer" in str(reviewed_by), (
            f"P8.1: Annual review signed by '{reviewed_by}' — must be Privacy Officer."
        )

        required_areas = {
            "notice_accuracy",
            "consent_mechanisms",
            "access_rights_fulfillment",
            "third_party_compliance",
            "incident_handling",
            "emerging_legal_obligations",
        }
        reviewed_areas = set(annual_review.get("areas_reviewed", []))
        missing = required_areas - reviewed_areas

        assert not missing, (
            f"P8.1: Annual privacy review is missing coverage areas: {missing}."
        )

    def test_privacy_complaints_tracked_and_responded(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        P8.1: Privacy complaints from individuals must be tracked and responded to.
        No complaint may go unacknowledged. Default response commitment: 30 days.
        """
        COMPLAINT_RESPONSE_DAYS = 30

        complaint_log = controls_evidence.get("privacy_complaint_log", [])

        unresolved = []
        for complaint in complaint_log:
            c_id = complaint.get("complaint_id", "unknown")
            received = complaint.get("received_date")
            responded = complaint.get("responded_date")
            outcome = complaint.get("outcome")

            if not received:
                continue

            deadline = received + relativedelta(days=COMPLAINT_RESPONSE_DAYS)

            if responded is None and outcome is None:
                if reference_date > deadline:
                    unresolved.append({
                        "complaint_id": c_id,
                        "received": received,
                        "deadline": deadline,
                    })

        assert not unresolved, (
            f"P8.1: {len(unresolved)} privacy complaint(s) have no response or outcome "
            f"after {COMPLAINT_RESPONSE_DAYS} days: {unresolved}"
        )

    def test_privacy_incident_log_maintained(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        P8.1: A privacy incident log must exist and be maintained. Absence of any
        incident log (as opposed to an empty log for a period with no incidents)
        is a control gap.
        """
        incident_log = controls_evidence.get("privacy_incident_log")

        assert incident_log is not None, (
            "P8.1: No privacy_incident_log found (as opposed to an empty list). "
            "A privacy incident log must be maintained even if no incidents occurred "
            "during the period. An empty list is acceptable; a missing key is not."
        )

    @pytest.mark.human_review_required(
        reason=(
            "P8.1: Whether the entity's overall privacy monitoring programme is adequate "
            "to detect and address privacy control failures requires assessment of: "
            "the scope and frequency of monitoring activities, whether monitoring covers "
            "all P1–P7 criteria, whether findings lead to remediation, and whether the "
            "Privacy Officer has the authority and resources to enforce commitments. "
            "Required: annual Privacy Officer attestation and SOC 2 auditor assessment "
            "of monitoring programme design and operating effectiveness."
        )
    )
    def test_privacy_monitoring_programme_adequacy_attested(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 3 — CONTESTED.
        P8.1: Adequacy of the monitoring programme cannot be fully automated.
        Annual auditor walkthrough and Privacy Officer attestation required.
        """
        programme_attestation = controls_evidence.get(
            "privacy_monitoring_programme_attestation"
        )

        assert programme_attestation is not None, (
            "P8.1: No privacy_monitoring_programme_attestation found. "
            "Annual attestation of monitoring programme adequacy is required."
        )

        attestation_date = programme_attestation.get("attestation_date")
        assert attestation_date is not None
        assert (reference_date - attestation_date).days <= 365, (
            f"P8.1: Monitoring programme attestation overdue (last: {attestation_date})."
        )
