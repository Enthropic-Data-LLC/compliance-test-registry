# GDPR — Data Subject Rights & Privacy by Design
# Articles 17, 20, 21, 25
#
# Pattern guide:
#   Pattern 1 — direct assert — DETERMINISTIC obligations (binary or threshold-based)
#   Pattern 2 — @pytest.mark.assumption(...) — PARAMETERIZED (org-defined, methodology-dependent)
#   Pattern 3 — @pytest.mark.human_review_required(...) — CONTESTED (requires human judgment)
#
# New assumptions introduced in this file:
#   ASSUME-GDPR-ERASURE-001  Art. 17 — Technical erasure scope and third-party notification
#   ASSUME-GDPR-PORT-001     Art. 20 — Portable format acceptability and direct-transfer feasibility
#   ASSUME-GDPR-OBJ-001      Art. 21 — Objection processing; compelling grounds documentation
#   ASSUME-GDPR-PBD-001      Art. 25 — Privacy by design measures and annual DPO attestation

#
# Applies to: Any organization — regardless of location — that processes personal data of EU/EEA data subjects by offering goods or services to them or monitoring their behavior within the EU/EEA
# Trigger: Offering goods or services to EU/EEA persons (Art. 3(2)(a)); monitoring behavior of EU/EEA persons within the EU/EEA (Art. 3(2)(b)); establishment in the EU/EEA (Art. 3(1))
# Jurisdiction: European Union / EEA; strong extraterritorial reach — applies to non-EU organizations targeting EU persons; enforced by national Data Protection Authorities and the EDPB
# Not applicable to: Purely personal or household use (Art. 2(2)(c)); national security and law enforcement activities (Directive 2016/680 instead); anonymous data (not 'personal data' within GDPR meaning); deceased persons (in most member states)
import pytest
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


# ---------------------------------------------------------------------------
# Scope pre-condition
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def gdpr_scope_check(entity_profile: dict):
    """Skip all tests in this module when GDPR does not apply."""
    if not entity_profile.get("processes_eu_subject_data", False):
        pytest.skip(
            "GDPR (Regulation (EU) 2016/679) does not apply — "
            "entity_profile['processes_eu_subject_data'] is False or absent. "
            "Art. 3 extra-territorial scope: applies to targeting EU/EEA data subjects "
            "regardless of controller/processor location."
        )


# ---------------------------------------------------------------------------
# Shared constants
# ---------------------------------------------------------------------------

DSR_RESPONSE_DAYS = 30          # Art. 12(3) — calendar days from receipt
DSR_EXTENSION_DAYS = 90         # Art. 12(3) — maximum including extension
DIRECT_MARKETING_CESSATION = 0  # Art. 21(3) — object to marketing → must stop immediately


# ===========================================================================
# ARTICLE 17 — Right to Erasure ("Right to be Forgotten")
# ===========================================================================

# DETERMINISTIC grounds for erasure (Art. 17(1)):
#   (a) data no longer necessary for the purpose collected/processed
#   (b) data subject withdraws consent (no other legal basis)
#   (c) data subject objects under Art. 21 and no overriding legitimate grounds
#   (d) personal data processed unlawfully
#   (e) erasure required to comply with legal obligation (EU/Member State law)
#   (f) data collected in relation to child aged under 16 for information society services
#
# Exceptions (Art. 17(3)) — erasure does NOT apply when processing is necessary for:
#   (a) exercising freedom of expression/information
#   (b) compliance with a legal obligation / public interest task
#   (c) public health grounds (Art. 9(2)(h)(i))
#   (d) archiving in public interest, scientific/historical research, statistics
#   (e) establishment, exercise, or defence of legal claims

VALID_ERASURE_GROUNDS = {
    "no_longer_necessary_17_1_a",
    "consent_withdrawn_17_1_b",
    "objection_upheld_17_1_c",
    "unlawful_processing_17_1_d",
    "legal_obligation_17_1_e",
    "child_data_online_service_17_1_f",
}

ERASURE_EXCEPTION_GROUNDS = {
    "freedom_of_expression_17_3_a",
    "legal_obligation_compliance_17_3_b",
    "public_health_17_3_c",
    "archiving_research_statistics_17_3_d",
    "legal_claims_17_3_e",
}


class TestArticle17RightToErasure:
    """Art. 17 — Right to Erasure."""

    # -----------------------------------------------------------------------
    # Art. 17(1) — Erasure request handling: response within Art. 12 deadline
    # -----------------------------------------------------------------------

    def test_erasure_requests_responded_within_deadline(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        Art. 12(3): erasure requests (and all DSRs) must be responded to within
        1 calendar month (30 days) of receipt. Extension to 90 days requires notice
        within the initial 30-day window.
        """
        erasure_log = controls_evidence.get("erasure_request_log", [])

        overdue = []
        for req in erasure_log:
            received = req.get("received_date")
            responded = req.get("responded_date")
            extension_notified = req.get("extension_notice_sent_date")

            if not received:
                continue

            deadline_standard = received + relativedelta(days=DSR_RESPONSE_DAYS)
            deadline_extended = received + relativedelta(days=DSR_EXTENSION_DAYS)

            if responded is None:
                # Unanswered: check if still within initial window
                if reference_date > deadline_standard and extension_notified is None:
                    overdue.append({
                        "request_id": req.get("request_id"),
                        "received": received,
                        "deadline": deadline_standard,
                        "status": "no_response_no_extension",
                    })
            else:
                # Extension path: extension notice must arrive within 30 days
                if extension_notified:
                    assert extension_notified <= deadline_standard, (
                        f"Erasure request {req.get('request_id')}: extension notice "
                        f"sent {extension_notified} is after 30-day deadline {deadline_standard}"
                    )
                    assert responded <= deadline_extended, (
                        f"Erasure request {req.get('request_id')}: extended response "
                        f"{responded} is after 90-day outer deadline {deadline_extended}"
                    )
                else:
                    assert responded <= deadline_standard, (
                        f"Erasure request {req.get('request_id')}: response {responded} "
                        f"is after 30-day deadline {deadline_standard} with no extension notice"
                    )

        assert not overdue, (
            f"Art. 17 / Art. 12(3): {len(overdue)} erasure request(s) are overdue "
            f"with no response and no extension notice: {overdue}"
        )

    # -----------------------------------------------------------------------
    # Art. 17(1) — Documented outcome: granted, denied (with exception ground), or partial
    # -----------------------------------------------------------------------

    def test_erasure_requests_have_documented_outcome(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        Every erasure request must have a documented outcome. Denials must cite
        an Art. 17(3) exception ground. Without a documented outcome the request
        is treated as open and overdue.
        """
        erasure_log = controls_evidence.get("erasure_request_log", [])

        for req in erasure_log:
            req_id = req.get("request_id", "unknown")
            outcome = req.get("outcome")

            assert outcome in ("granted", "denied", "partial", "withdrawn_by_subject"), (
                f"Erasure request {req_id}: outcome '{outcome}' is not one of "
                "granted / denied / partial / withdrawn_by_subject"
            )

            if outcome == "denied":
                exception_ground = req.get("exception_ground")
                assert exception_ground in ERASURE_EXCEPTION_GROUNDS, (
                    f"Erasure request {req_id} denied but exception ground "
                    f"'{exception_ground}' is not a valid Art. 17(3) ground. "
                    f"Valid grounds: {ERASURE_EXCEPTION_GROUNDS}"
                )

    # -----------------------------------------------------------------------
    # Art. 17(2) — Third-party notification obligation
    # -----------------------------------------------------------------------

    @pytest.mark.assumption(
        id="ASSUME-GDPR-ERASURE-001",
        description=(
            "Art. 17(2): where data has been made public, controller must take reasonable "
            "steps to inform other controllers processing the data of the erasure request. "
            "'Reasonable steps' is PARAMETERIZED — assessed on volume, accessibility, "
            "and cost. Assumption: erasure propagation covers: downstream processors, "
            "CDN/caching layers, search index operators, backup media (within scheduled "
            "backup purge cycle). Third-party notification sent within the same 30-day "
            "response window as the primary erasure."
        ),
        approved_by="DPO",
        review_date="2026-11-01",
    )
    def test_erasure_propagation_to_third_parties(self, controls_evidence: dict):
        """
        Pattern 2 — PARAMETERIZED.
        Art. 17(2): when data has been made public, erasure obligation extends to
        other controllers. Verify that the erasure procedure documents which downstream
        systems were notified and confirms propagation (or documents why not necessary).
        """
        erasure_log = controls_evidence.get("erasure_request_log", [])

        for req in erasure_log:
            if req.get("outcome") != "granted":
                continue
            req_id = req.get("request_id", "unknown")

            publicly_disclosed = req.get("data_was_publicly_disclosed", False)
            if not publicly_disclosed:
                continue

            propagation_record = req.get("third_party_propagation")
            assert propagation_record is not None, (
                f"Erasure request {req_id}: data was publicly disclosed but "
                "no third_party_propagation record exists. Art. 17(2) requires "
                "reasonable steps to notify other controllers."
            )

            notified_systems = propagation_record.get("systems_notified", [])
            not_applicable_reason = propagation_record.get("not_applicable_reason")

            assert notified_systems or not_applicable_reason, (
                f"Erasure request {req_id}: third_party_propagation has neither "
                "systems_notified nor not_applicable_reason — documentation incomplete."
            )

    # -----------------------------------------------------------------------
    # Art. 17(1) — Technical erasure scope: primary systems
    # -----------------------------------------------------------------------

    @pytest.mark.assumption(
        id="ASSUME-GDPR-ERASURE-001",
        description=(
            "Technical erasure scope — covers primary databases, application caches, "
            "search indexes, backup media (within scheduled retention window), "
            "and audit-log pseudonymization. Erasure procedure documented in WISP/DPA. "
            "Backups: not required for immediate overwrite but must be excluded from "
            "restore paths (marked for purge at next backup cycle)."
        ),
        approved_by="DPO",
        review_date="2026-11-01",
    )
    def test_technical_erasure_procedure_defined(self, controls_evidence: dict):
        """
        Pattern 2 — PARAMETERIZED.
        Erasure procedure must document which systems are in scope, handling of
        backup media, treatment of audit logs (pseudonymization or erasure),
        and verification step confirming data is no longer accessible.
        """
        erasure_procedure = controls_evidence.get("erasure_technical_procedure")

        assert erasure_procedure is not None, (
            "Art. 17: No erasure_technical_procedure documented. "
            "A written erasure procedure covering in-scope systems is required."
        )

        required_sections = {
            "primary_database_erasure",
            "cache_and_index_erasure",
            "backup_handling",
            "audit_log_treatment",
            "verification_step",
        }
        documented_sections = set(erasure_procedure.get("sections_covered", []))
        missing = required_sections - documented_sections

        assert not missing, (
            f"Art. 17 erasure procedure is missing sections: {missing}. "
            "Procedure must address all in-scope system layers."
        )


# ===========================================================================
# ARTICLE 20 — Right to Data Portability
# ===========================================================================

# Art. 20 applies only when:
#   (a) the lawful basis is consent (Art. 6(1)(a)) OR contract (Art. 6(1)(b)); AND
#   (b) processing is carried out by automated means
#
# Art. 20(2): direct transmission between controllers "where technically feasible"
# Art. 20(4): shall not adversely affect the rights of others

PORTABILITY_ELIGIBLE_BASES = {"consent_6_1_a", "contract_6_1_b"}

ACCEPTED_PORTABLE_FORMATS = {
    "json",
    "csv",
    "xml",
    "parquet",
}


class TestArticle20DataPortability:
    """Art. 20 — Right to Data Portability."""

    # -----------------------------------------------------------------------
    # Art. 20(1) — Portability requests resolved in machine-readable format
    # -----------------------------------------------------------------------

    def test_portability_requests_responded_within_deadline(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        Art. 12(3) applies to portability requests — same 30-day deadline as erasure.
        """
        portability_log = controls_evidence.get("portability_request_log", [])

        overdue = []
        for req in portability_log:
            received = req.get("received_date")
            responded = req.get("responded_date")
            extension_notified = req.get("extension_notice_sent_date")

            if not received:
                continue

            deadline_standard = received + relativedelta(days=DSR_RESPONSE_DAYS)
            deadline_extended = received + relativedelta(days=DSR_EXTENSION_DAYS)

            if responded is None:
                if reference_date > deadline_standard and extension_notified is None:
                    overdue.append(req.get("request_id"))
            else:
                if extension_notified:
                    assert extension_notified <= deadline_standard
                    assert responded <= deadline_extended
                else:
                    assert responded <= deadline_standard, (
                        f"Portability request {req.get('request_id')}: response "
                        f"{responded} exceeds 30-day deadline {deadline_standard}"
                    )

        assert not overdue, (
            f"Art. 20 / Art. 12(3): {len(overdue)} portability request(s) overdue: {overdue}"
        )

    def test_portability_format_is_machine_readable(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        Art. 20(1): data must be provided in a structured, commonly used,
        machine-readable format. Non-machine-readable formats (PDF of printed data,
        HTML page screenshots) fail this requirement.
        """
        portability_log = controls_evidence.get("portability_request_log", [])

        for req in portability_log:
            if req.get("outcome") != "granted":
                continue
            req_id = req.get("request_id", "unknown")
            fmt = req.get("export_format", "").lower()

            assert fmt in ACCEPTED_PORTABLE_FORMATS, (
                f"Portability request {req_id}: export format '{fmt}' is not in "
                f"the accepted machine-readable formats: {ACCEPTED_PORTABLE_FORMATS}. "
                "Art. 20(1) requires structured, commonly used, machine-readable format."
            )

    def test_portability_only_applied_to_eligible_processing(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        Art. 20 applies only to processing based on consent or contract (Art. 6(1)(a/b))
        carried out by automated means. Portability requests for data processed on
        other bases (e.g., legal obligation, legitimate interests) must be declined
        with an explanation — not silently refused.
        """
        portability_log = controls_evidence.get("portability_request_log", [])

        for req in portability_log:
            req_id = req.get("request_id", "unknown")
            outcome = req.get("outcome")

            if outcome == "denied":
                denial_reason = req.get("denial_reason")
                assert denial_reason is not None, (
                    f"Portability request {req_id} denied without documented reason. "
                    "Art. 12(4) requires notifying the data subject of reasons for refusal."
                )

            if outcome == "granted":
                lawful_basis = req.get("processing_lawful_basis")
                assert lawful_basis in PORTABILITY_ELIGIBLE_BASES, (
                    f"Portability request {req_id} granted but lawful basis '{lawful_basis}' "
                    "is not consent or contract — Art. 20 does not apply to this basis."
                )

    # -----------------------------------------------------------------------
    # Art. 20(2) — Direct controller-to-controller transfer
    # -----------------------------------------------------------------------

    @pytest.mark.assumption(
        id="ASSUME-GDPR-PORT-001",
        description=(
            "Art. 20(2): direct controller-to-controller transmission required 'where technically feasible.' "
            "'Technically feasible' is PARAMETERIZED — assessed by engineering team on a per-request basis. "
            "Standard: if the receiving controller provides a documented API endpoint or standard import "
            "capability (e.g., SFTP, REST), direct transfer is feasible. "
            "Determination documented per request; DPO reviews cases where feasibility is disputed."
        ),
        approved_by="DPO",
        review_date="2026-11-01",
    )
    def test_direct_transfer_feasibility_assessed(self, controls_evidence: dict):
        """
        Pattern 2 — PARAMETERIZED.
        When a data subject requests direct transmission to another controller,
        the procedure must document whether direct transfer is technically feasible
        and the rationale for the decision.
        """
        portability_log = controls_evidence.get("portability_request_log", [])

        for req in portability_log:
            if not req.get("direct_transfer_requested", False):
                continue
            req_id = req.get("request_id", "unknown")

            feasibility_assessment = req.get("direct_transfer_feasibility_assessment")
            assert feasibility_assessment is not None, (
                f"Portability request {req_id}: direct transfer was requested but no "
                "feasibility assessment is documented. Art. 20(2) requires assessment."
            )

            assert "feasible" in feasibility_assessment and "rationale" in feasibility_assessment, (
                f"Portability request {req_id}: feasibility assessment must contain "
                "'feasible' (bool) and 'rationale' fields."
            )


# ===========================================================================
# ARTICLE 21 — Right to Object
# ===========================================================================

# Art. 21(1): object to processing based on Art. 6(1)(e) or (f) — controller must
#   cease UNLESS it can demonstrate compelling legitimate grounds overriding
#   the data subject's interests, rights, and freedoms, OR for legal claims.
#
# Art. 21(2): object to processing for direct marketing purposes — ABSOLUTE right.
#   No compelling grounds override. Processing MUST cease immediately.
#
# Art. 21(5): object may be exercised by automated means alongside information society service use.


class TestArticle21RightToObject:
    """Art. 21 — Right to Object."""

    # -----------------------------------------------------------------------
    # Art. 21(2) — Direct marketing objection: absolute, immediate cessation
    # -----------------------------------------------------------------------

    def test_direct_marketing_objection_ceases_processing(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 1 — DETERMINISTIC.
        Art. 21(2)/(3): objection to direct marketing processing is absolute —
        the right is not subject to balancing against the controller's interests.
        Processing for direct marketing MUST cease immediately upon receipt.
        Tolerance: same processing day (DIRECT_MARKETING_CESSATION = 0 days).
        """
        objection_log = controls_evidence.get("objection_request_log", [])

        violations = []
        for req in objection_log:
            if req.get("processing_purpose") != "direct_marketing":
                continue

            req_id = req.get("request_id", "unknown")
            received = req.get("received_date")
            processing_ceased_date = req.get("processing_ceased_date")
            still_processing = req.get("direct_marketing_still_active_after_objection", False)

            if still_processing:
                violations.append({
                    "request_id": req_id,
                    "received": received,
                    "issue": "direct_marketing_still_active",
                })
                continue

            if received and processing_ceased_date:
                assert processing_ceased_date <= received + relativedelta(days=1), (
                    f"Objection {req_id}: direct marketing did not cease within 1 day "
                    f"of receiving objection. Received: {received}, ceased: {processing_ceased_date}. "
                    "Art. 21(3): objection to direct marketing must be complied with immediately."
                )

        assert not violations, (
            f"Art. 21(2)/(3): {len(violations)} direct marketing objection(s) not honoured: {violations}"
        )

    def test_direct_marketing_objection_not_overridden(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        Art. 21(2): no competing-interests override is available for direct marketing objections.
        A documented override attempt for direct marketing is a per se violation.
        """
        objection_log = controls_evidence.get("objection_request_log", [])

        for req in objection_log:
            if req.get("processing_purpose") != "direct_marketing":
                continue
            req_id = req.get("request_id", "unknown")

            compelling_grounds_invoked = req.get("compelling_legitimate_grounds_invoked", False)
            assert not compelling_grounds_invoked, (
                f"Objection {req_id}: compelling legitimate grounds were invoked to override "
                "a direct marketing objection. Art. 21(2) is absolute — no override is permitted "
                "for direct marketing regardless of legitimate interests."
            )

    # -----------------------------------------------------------------------
    # Art. 21(1) — Legitimate-interests / public-task objection: balancing required
    # -----------------------------------------------------------------------

    @pytest.mark.assumption(
        id="ASSUME-GDPR-OBJ-001",
        description=(
            "Art. 21(1): objection to processing on Art. 6(1)(e)/(f) grounds requires the controller "
            "to either (a) cease processing or (b) demonstrate compelling legitimate grounds overriding "
            "the data subject's interests. 'Compelling' is not defined — assessed case-by-case. "
            "Assumption: compelling grounds assessment must be documented, reviewed by DPO/Legal, "
            "and communicated to the data subject within the Art. 12(3) 30-day window. "
            "Legal claims exception (Art. 21(1) in fine) must cite specific proceedings."
        ),
        approved_by="DPO",
        review_date="2026-11-01",
    )
    def test_legitimate_interests_objection_has_documented_assessment(
        self, controls_evidence: dict
    ):
        """
        Pattern 2 — PARAMETERIZED.
        Art. 21(1): when an objection to legitimate-interests processing is received,
        the controller must either cease or document compelling grounds. That assessment
        must be documented with DPO/Legal review.
        """
        objection_log = controls_evidence.get("objection_request_log", [])

        for req in objection_log:
            purpose = req.get("processing_purpose")
            lawful_basis = req.get("processing_lawful_basis")

            if purpose == "direct_marketing":
                continue
            if lawful_basis not in ("public_task_6_1_e", "legitimate_interests_6_1_f"):
                continue

            req_id = req.get("request_id", "unknown")
            outcome = req.get("outcome")

            assert outcome in ("granted_ceased_processing", "denied_compelling_grounds"), (
                f"Objection {req_id}: outcome '{outcome}' is not valid. Must be either "
                "'granted_ceased_processing' or 'denied_compelling_grounds'."
            )

            if outcome == "denied_compelling_grounds":
                assessment = req.get("compelling_grounds_assessment")
                assert assessment is not None, (
                    f"Objection {req_id}: processing was continued after Art. 21(1) objection "
                    "but no compelling_grounds_assessment is documented."
                )
                reviewer = assessment.get("reviewed_by")
                assert reviewer in ("DPO", "Legal", "DPO_and_Legal"), (
                    f"Objection {req_id}: compelling grounds assessment reviewed by '{reviewer}' — "
                    "must be reviewed by DPO or Legal."
                )

    # -----------------------------------------------------------------------
    # Art. 21(1) — Objection to processing for research/statistics: narrower exception
    # -----------------------------------------------------------------------

    @pytest.mark.human_review_required(
        reason=(
            "Art. 21(6): right to object to processing for scientific/historical research "
            "or statistical purposes may be overridden only where processing is necessary "
            "for public interest tasks. Whether a given research purpose qualifies as a "
            "'public interest task' sufficient to override the objection requires legal "
            "and institutional analysis; no algorithmic resolution is available. "
            "Required: DPO + institutional review board (IRB) documented rationale per case."
        )
    )
    def test_research_processing_objection_override_is_justified(
        self, controls_evidence: dict
    ):
        """
        Pattern 3 — CONTESTED.
        Art. 21(6): objections to research/statistics processing may be overridden
        for public interest — but the public interest determination is not automatable.
        """
        objection_log = controls_evidence.get("objection_request_log", [])

        research_overrides = [
            req for req in objection_log
            if req.get("processing_purpose") in ("scientific_research", "historical_research", "statistics")
            and req.get("outcome") == "denied_compelling_grounds"
        ]

        if not research_overrides:
            pytest.skip("No research/statistics objection overrides present — test not applicable.")

        for req in research_overrides:
            req_id = req.get("request_id", "unknown")
            irb_review = req.get("irb_review_documented", False)
            dpo_sign_off = req.get("dpo_sign_off", False)

            assert irb_review and dpo_sign_off, (
                f"Research objection override {req_id}: requires both IRB review "
                f"(present: {irb_review}) and DPO sign-off (present: {dpo_sign_off}). "
                "Art. 21(6) override requires public interest justification at institutional level."
            )


# ===========================================================================
# ARTICLE 25 — Data Protection by Design and by Default
# ===========================================================================

# Art. 25(1): at time of determination AND at time of processing, implement appropriate
#   technical and organisational measures (data minimization, pseudonymization) designed
#   to implement data protection principles (Art. 5) efficiently.
#
# Art. 25(2): by default, only personal data necessary for each specific purpose processed.
#   Applies to: amount collected, extent of processing, storage period, accessibility.
#
# Art. 25(3): certification per Art. 42 can demonstrate compliance (optional).
#
# Art. 25 is CONTESTED: "appropriate" and "state of the art" have no bright-line definitions.
# Pattern 3 is the primary test type. Pattern 2 is used for specific implementation assumptions.


class TestArticle25DataProtectionByDesign:
    """Art. 25 — Data Protection by Design and by Default."""

    # -----------------------------------------------------------------------
    # Art. 25(2) — Data minimization: by-default configuration
    # -----------------------------------------------------------------------

    @pytest.mark.assumption(
        id="ASSUME-GDPR-PBD-001",
        description=(
            "Art. 25(2): by default, only personal data necessary for each specific purpose "
            "is processed. Implementation assumption: (1) systems default to minimum fields "
            "required for stated purpose — no opt-in needed to limit collection; "
            "(2) retention defaults are set to minimum, not maximum; "
            "(3) system documentation (architecture review record) confirms privacy-by-default "
            "settings at launch and after material change; "
            "(4) DPO attests annually that privacy-by-design principles are embedded in SDLC."
        ),
        approved_by="DPO",
        review_date="2026-11-01",
    )
    def test_privacy_by_default_settings_documented(self, controls_evidence: dict):
        """
        Pattern 2 — PARAMETERIZED.
        Art. 25(2): by-default configuration must be documented at system level.
        Verify that a privacy-by-default configuration record exists for each
        system processing personal data, and that it covers data volume, retention,
        and accessibility defaults.
        """
        systems_inventory = controls_evidence.get("systems_processing_personal_data", [])

        for system in systems_inventory:
            system_id = system.get("system_id", "unknown")
            pbd_record = system.get("privacy_by_default_configuration")

            assert pbd_record is not None, (
                f"System '{system_id}': no privacy_by_default_configuration record. "
                "Art. 25(2) requires by-default settings to be documented."
            )

            required_fields = {
                "minimum_data_collected_confirmed",
                "retention_default_is_minimum",
                "accessibility_default",
                "last_reviewed_date",
                "reviewed_by",
            }
            present_fields = set(pbd_record.keys())
            missing = required_fields - present_fields

            assert not missing, (
                f"System '{system_id}' privacy-by-default record is missing fields: {missing}"
            )

            assert pbd_record.get("minimum_data_collected_confirmed") is True, (
                f"System '{system_id}': minimum_data_collected_confirmed is not True. "
                "Art. 25(2): only data necessary for the specific purpose should be collected."
            )

            assert pbd_record.get("retention_default_is_minimum") is True, (
                f"System '{system_id}': retention_default_is_minimum is not True. "
                "Art. 25(2): default retention must be minimum, not maximum."
            )

    # -----------------------------------------------------------------------
    # Art. 25(1) — SDLC integration: privacy review at design stage
    # -----------------------------------------------------------------------

    @pytest.mark.assumption(
        id="ASSUME-GDPR-PBD-001",
        description=(
            "Art. 25(1): privacy-by-design measures must be considered 'at the time of "
            "determination of the means for processing AND at the time of processing itself.' "
            "SDLC integration assumption: each new system or material change to an existing "
            "system involving personal data must have a Privacy Design Review (PDR) conducted "
            "before deployment. PDR documents: data flows, data minimization decisions, "
            "pseudonymization opportunities, access control design, and DPO consultation outcome."
        ),
        approved_by="DPO",
        review_date="2026-11-01",
    )
    def test_privacy_design_review_conducted_for_new_systems(
        self, controls_evidence: dict
    ):
        """
        Pattern 2 — PARAMETERIZED.
        Art. 25(1): privacy-by-design must be integrated at design time.
        For each system added or materially changed in the review period,
        a Privacy Design Review (PDR) must be documented before deployment.
        """
        new_or_changed_systems = controls_evidence.get(
            "new_or_materially_changed_systems", []
        )

        for system in new_or_changed_systems:
            system_id = system.get("system_id", "unknown")
            deployment_date = system.get("deployment_date")
            pdr = system.get("privacy_design_review")

            assert pdr is not None, (
                f"System '{system_id}' deployed {deployment_date} without a documented "
                "Privacy Design Review. Art. 25(1) requires privacy-by-design at design stage."
            )

            required_pdr_elements = {
                "data_flow_documented",
                "data_minimization_decisions",
                "pseudonymization_considered",
                "access_control_design",
                "dpo_consulted",
            }
            present_elements = set(pdr.get("elements_covered", []))
            missing = required_pdr_elements - present_elements

            assert not missing, (
                f"System '{system_id}' Privacy Design Review is incomplete — "
                f"missing elements: {missing}"
            )

            pdr_date = pdr.get("completed_date")
            if deployment_date and pdr_date:
                assert pdr_date <= deployment_date, (
                    f"System '{system_id}': Privacy Design Review ({pdr_date}) was "
                    f"completed AFTER deployment ({deployment_date}). Art. 25(1) requires "
                    "privacy measures at design time, not post-deployment."
                )

    # -----------------------------------------------------------------------
    # Art. 25(1) — Annual DPO attestation of privacy-by-design programme
    # -----------------------------------------------------------------------

    @pytest.mark.human_review_required(
        reason=(
            "Art. 25(1): 'appropriate technical and organisational measures' is CONTESTED — "
            "no bright-line definition of 'appropriate' or 'state of the art.' "
            "Whether the implemented privacy-by-design programme is 'appropriate' to the "
            "nature and risk of the processing is a judgment requiring DPO expertise and "
            "ongoing monitoring of supervisory authority guidance and enforcement decisions. "
            "Required: annual DPO attestation that the privacy-by-design programme meets "
            "'state of the art' standard for this organization's processing profile."
        )
    )
    def test_privacy_by_design_programme_adequacy_attested(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 3 — CONTESTED.
        Art. 25(1): 'appropriate' measures require annual human attestation.
        No automated test can determine whether the technical measures are
        'state of the art' given the nature and risk of the processing.
        """
        pbd_attestation = controls_evidence.get("privacy_by_design_annual_attestation")

        assert pbd_attestation is not None, (
            "Art. 25(1): No privacy_by_design_annual_attestation found. "
            "Annual DPO attestation of programme adequacy is required."
        )

        attestation_date = pbd_attestation.get("attestation_date")
        attested_by = pbd_attestation.get("attested_by")
        scope_covered = pbd_attestation.get("scope_covered", [])

        assert attested_by == "DPO" or "DPO" in str(attested_by), (
            f"Art. 25 attestation signed by '{attested_by}' — must be attested by the DPO."
        )

        assert attestation_date is not None, (
            "Art. 25 attestation: attestation_date is missing."
        )

        max_attestation_age_days = 365
        assert (reference_date - attestation_date).days <= max_attestation_age_days, (
            f"Art. 25 privacy-by-design attestation dated {attestation_date} is more than "
            f"{max_attestation_age_days} days old (reference date: {reference_date}). "
            "Annual re-attestation required."
        )

        assert scope_covered, (
            "Art. 25 attestation: scope_covered is empty — attestation must list "
            "the systems or processing activities reviewed."
        )

    # -----------------------------------------------------------------------
    # Art. 25(2) — Accessibility default: personal data not publicly accessible by default
    # -----------------------------------------------------------------------

    def test_personal_data_not_publicly_accessible_by_default(
        self, controls_evidence: dict
    ):
        """
        Pattern 1 — DETERMINISTIC.
        Art. 25(2): personal data shall not be made accessible without individual's
        intervention to an indefinite number of persons by default.
        New user accounts and data exports must default to private/restricted.
        """
        systems_inventory = controls_evidence.get("systems_processing_personal_data", [])

        violations = []
        for system in systems_inventory:
            system_id = system.get("system_id", "unknown")
            pbd_record = system.get("privacy_by_default_configuration", {})

            default_accessibility = pbd_record.get("accessibility_default", "unknown")

            if default_accessibility in ("public", "world_readable", "open"):
                violations.append({
                    "system_id": system_id,
                    "accessibility_default": default_accessibility,
                })

        assert not violations, (
            f"Art. 25(2): {len(violations)} system(s) have personal data accessible "
            f"publicly by default: {violations}. Default must be private/restricted."
        )
