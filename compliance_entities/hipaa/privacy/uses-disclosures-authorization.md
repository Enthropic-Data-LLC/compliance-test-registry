# HIPAA Privacy Rule — Uses, Disclosures, Authorizations, and De-identification
# 45 CFR §§164.502, 164.508, 164.512, 164.514
#
# Scope note: The Privacy Rule governs PHI in ALL forms (paper, oral, electronic).
# The Security Rule (sibling registry) governs ePHI only. Both apply to CEs and BAs.
#
# Pattern guide:
#   Pattern 1 — direct assert — DETERMINISTIC obligations
#   Pattern 2 — @pytest.mark.assumption(...) — PARAMETERIZED
#   Pattern 3 — @pytest.mark.human_review_required(...) — CONTESTED
#
# New assumptions introduced in this file:
#   ASSUME-HIPAA-PRIV-BA-001     §164.502 — BAA required before BA disclosure; Privacy Rule BAA elements
#   ASSUME-HIPAA-PRIV-MINNEC-001 §164.502(b) — Minimum necessary determination methodology
#   ASSUME-HIPAA-PRIV-AUTH-001   §164.508 — Authorization form validation; conditioned treatment rules
#   ASSUME-HIPAA-PRIV-DEID-001   §164.514 — Expert determination methodology and certification

import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


# ---------------------------------------------------------------------------
# Scope pre-condition
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def hipaa_privacy_scope_check(entity_profile: dict):
    """
    HIPAA Privacy Rule applies to covered entities (health plans, healthcare
    clearinghouses, healthcare providers transmitting PHI electronically) and
    their business associates. Skip if neither applies.
    """
    is_ce = entity_profile.get("hipaa_covered_entity", False)
    is_ba = entity_profile.get("hipaa_business_associate", False)
    if not (is_ce or is_ba):
        pytest.skip(
            "HIPAA Privacy Rule (45 CFR Part 164 Subpart E) does not apply — "
            "entity is neither a covered entity nor a business associate."
        )


# ---------------------------------------------------------------------------
# Safe Harbor 18 de-identification identifiers (§164.514(b)(2))
# All 18 must be absent or generalized for data to be considered de-identified.
# ---------------------------------------------------------------------------

SAFE_HARBOR_IDENTIFIERS = frozenset({
    "names",
    "geographic_subdivisions_smaller_than_state",  # except first 3 ZIP digits if pop > 20,000
    "dates_except_year_for_individuals_ge_90",      # dates other than year; all ages ≥ 90 must use "90+"
    "phone_numbers",
    "fax_numbers",
    "email_addresses",
    "social_security_numbers",
    "medical_record_numbers",
    "health_plan_beneficiary_numbers",
    "account_numbers",
    "certificate_or_license_numbers",
    "vehicle_identifiers_and_serial_numbers_including_vin",
    "device_identifiers_and_serial_numbers",
    "web_urls",
    "ip_addresses",
    "biometric_identifiers_including_finger_and_voice_prints",
    "full_face_photographs_and_any_comparable_images",
    "any_other_unique_identifying_numbers_codes_or_characteristics",
})

# Required elements in a valid §164.508 authorization
REQUIRED_AUTHORIZATION_ELEMENTS = frozenset({
    "description_of_information",
    "authorized_persons_making_disclosure",
    "authorized_recipients",
    "purpose_of_each_use_or_disclosure",
    "expiration_date_or_event",
    "individual_signature_and_date",
    "right_to_revoke_statement",
    "ability_to_condition_statement",
    "potential_for_redisclosure_statement",
})


# ===========================================================================
# §164.502 — Uses and Disclosures: General Rules
# ===========================================================================

class TestSection164502UsesAndDisclosures:
    """§164.502 — Permitted uses and disclosures of PHI."""

    # -----------------------------------------------------------------------
    # §164.502(e) — Business Associate Agreement required before disclosure
    # -----------------------------------------------------------------------

    def test_ba_disclosure_requires_baa(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        §164.502(e)(1): A covered entity may not disclose PHI to a business associate
        unless a satisfactory assurance (BAA) is in place. No BAA = impermissible disclosure.
        """
        ba_relationships = controls_evidence.get("business_associate_relationships", [])

        violations = []
        for ba in ba_relationships:
            ba_id = ba.get("ba_id", "unknown")
            receives_phi = ba.get("receives_phi", False)
            baa_on_file = ba.get("baa_on_file", False)
            baa_signed_date = ba.get("baa_signed_date")
            baa_expired = ba.get("baa_expired", False)

            if not receives_phi:
                continue

            if not baa_on_file or baa_signed_date is None or baa_expired:
                violations.append({
                    "ba_id": ba_id,
                    "baa_on_file": baa_on_file,
                    "baa_expired": baa_expired,
                })

        assert not violations, (
            f"§164.502(e): {len(violations)} business associate(s) receive PHI without a "
            f"current, signed BAA: {violations}. PHI disclosure to a BA without a BAA is an "
            "impermissible disclosure."
        )

    @pytest.mark.assumption(
        id="ASSUME-HIPAA-PRIV-BA-001",
        description=(
            "Privacy Rule BAA content (§164.504(e)(2)): BAA must include (1) permitted uses/disclosures "
            "of PHI by BA; (2) prohibition on BA using/disclosing other than permitted or required by law; "
            "(3) requirement to implement appropriate safeguards; (4) requirement to report unauthorized "
            "uses/disclosures and breaches to CE within 60 days (30-day recommended); "
            "(5) requirement for subcontractors to comply; (6) individual rights pass-through; "
            "(7) make PHI available for CE to fulfill individual rights; (8) return/destroy PHI at termination. "
            "All 8 elements must be present — mapped to ASSUME-314-001 for ePHI but this assumption "
            "covers the broader Privacy Rule context including non-electronic PHI."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_baa_contains_required_privacy_elements(self, controls_evidence: dict):
        """
        Pattern 2 — PARAMETERIZED.
        §164.504(e)(2): Privacy Rule BAA must contain 8 required provisions.
        Content completeness check for each BA relationship.
        """
        ba_relationships = controls_evidence.get("business_associate_relationships", [])

        required_baa_elements = {
            "permitted_uses_disclosures_defined",
            "prohibition_on_non_permitted_use",
            "appropriate_safeguards_required",
            "breach_reporting_obligation",
            "subcontractor_compliance_required",
            "individual_rights_pass_through",
            "phi_availability_for_individual_rights",
            "return_or_destroy_at_termination",
        }

        for ba in ba_relationships:
            ba_id = ba.get("ba_id", "unknown")
            if not ba.get("receives_phi", False) or not ba.get("baa_on_file", False):
                continue

            baa_elements = set(ba.get("baa_elements_present", []))
            missing = required_baa_elements - baa_elements

            assert not missing, (
                f"BA '{ba_id}': BAA is missing required Privacy Rule provisions: {missing}. "
                "§164.504(e)(2) requires all 8 elements."
            )

    # -----------------------------------------------------------------------
    # §164.502(b) — Minimum necessary standard
    # -----------------------------------------------------------------------

    @pytest.mark.assumption(
        id="ASSUME-HIPAA-PRIV-MINNEC-001",
        description=(
            "Minimum necessary standard (§164.502(b)): CEs must make reasonable efforts to limit "
            "PHI to the minimum necessary to accomplish the intended purpose. "
            "Implementation assumption: (1) role-based access profiles define the minimum PHI "
            "fields accessible per job function — documented in the access authorization matrix; "
            "(2) access profiles reviewed at least annually by the Privacy Officer; "
            "(3) routine requests (recurring) have standard protocols defining minimum fields; "
            "(4) non-routine requests reviewed individually. "
            "Exceptions: treatment (no minimum necessary restriction for treating providers), "
            "individual's own requests, authorizations, HHS oversight, research with IRB waiver."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_minimum_necessary_profiles_exist(self, controls_evidence: dict):
        """
        Pattern 2 — PARAMETERIZED.
        §164.502(b): minimum necessary implementation requires documented access profiles
        per role defining what PHI fields/categories are accessible for each purpose.
        """
        min_necessary_matrix = controls_evidence.get("minimum_necessary_access_matrix")

        assert min_necessary_matrix is not None, (
            "§164.502(b): No minimum_necessary_access_matrix found. "
            "Privacy Rule requires reasonable efforts to limit PHI to minimum necessary — "
            "role-based PHI access profiles must be documented."
        )

        roles = min_necessary_matrix.get("roles", [])
        assert len(roles) > 0, (
            "§164.502(b): minimum_necessary_access_matrix has no roles defined."
        )

        last_reviewed = min_necessary_matrix.get("last_reviewed_by_privacy_officer")
        assert last_reviewed is not None, (
            "§164.502(b): minimum necessary access matrix has never been reviewed by "
            "the Privacy Officer. Annual review is required."
        )

    @pytest.mark.human_review_required(
        reason=(
            "§164.502(b): The 'minimum necessary' determination for non-routine disclosures "
            "is a case-by-case judgment — no formula produces a binary answer. "
            "Whether a given disclosure included only the minimum necessary PHI requires "
            "assessment of the specific purpose, the recipient's need, and the amount of PHI shared. "
            "Required: Privacy Officer review of non-routine disclosure log on a quarterly basis, "
            "with spot-check assessment of 5–10 disclosures per quarter."
        )
    )
    def test_non_routine_disclosures_reviewed_for_minimum_necessary(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 3 — CONTESTED.
        §164.502(b): minimum necessary determination for non-routine disclosures
        requires individual review — no automated test can substitute.
        """
        non_routine_review = controls_evidence.get(
            "non_routine_disclosure_minimum_necessary_review"
        )

        assert non_routine_review is not None, (
            "§164.502(b): No non_routine_disclosure_minimum_necessary_review found. "
            "Privacy Officer must periodically review non-routine disclosures for "
            "minimum necessary compliance."
        )

        last_review_date = non_routine_review.get("last_review_date")
        assert last_review_date is not None, (
            "Non-routine disclosure minimum-necessary review has no last_review_date."
        )

        max_review_age_days = 92  # quarterly
        assert (reference_date - last_review_date).days <= max_review_age_days, (
            f"§164.502(b): Non-routine disclosure minimum-necessary review is overdue. "
            f"Last review: {last_review_date}. Quarterly review required."
        )


# ===========================================================================
# §164.508 — Authorizations for Uses and Disclosures
# ===========================================================================

class TestSection164508Authorizations:
    """§164.508 — HIPAA-compliant authorizations for uses/disclosures not otherwise permitted."""

    # -----------------------------------------------------------------------
    # §164.508(c) — Required elements: all 9 must be present
    # -----------------------------------------------------------------------

    def test_authorizations_contain_all_required_elements(
        self, controls_evidence: dict
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.508(c): A valid HIPAA authorization must contain all 9 required elements.
        An authorization missing any element is invalid — the use/disclosure it purports
        to authorize is impermissible.
        """
        authorizations = controls_evidence.get("phi_authorizations", [])

        invalid = []
        for auth in authorizations:
            auth_id = auth.get("authorization_id", "unknown")
            present_elements = set(auth.get("elements_present", []))
            missing = REQUIRED_AUTHORIZATION_ELEMENTS - present_elements

            if missing:
                invalid.append({"authorization_id": auth_id, "missing_elements": missing})

        assert not invalid, (
            f"§164.508(c): {len(invalid)} authorization(s) are missing required elements: {invalid}. "
            "An incomplete authorization is invalid — any PHI use/disclosure under it is impermissible."
        )

    # -----------------------------------------------------------------------
    # §164.508(b)(4) — Authorization may not condition treatment/payment/enrollment
    # -----------------------------------------------------------------------

    def test_authorizations_not_used_as_condition_of_treatment(
        self, controls_evidence: dict
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.508(b)(4): A CE may not condition treatment, payment, enrollment, or benefits
        eligibility on the individual's authorization, EXCEPT for:
          - Research-related treatment
          - Health plan enrollment/eligibility for underwriting/risk-rating
        Any non-excepted authorization that was required as a condition is per se invalid.
        """
        authorizations = controls_evidence.get("phi_authorizations", [])

        violations = []
        for auth in authorizations:
            auth_id = auth.get("authorization_id", "unknown")
            conditioned_on_treatment = auth.get("conditioned_on_treatment_or_payment", False)
            is_research_treatment = auth.get("is_research_related_treatment", False)
            is_underwriting = auth.get("is_underwriting_or_eligibility", False)

            # Conditioning is permitted only for the two exception categories
            if conditioned_on_treatment and not (is_research_treatment or is_underwriting):
                violations.append(auth_id)

        assert not violations, (
            f"§164.508(b)(4): {len(violations)} authorization(s) impermissibly conditioned "
            f"on treatment/payment/enrollment: {violations}."
        )

    # -----------------------------------------------------------------------
    # §164.508(b)(5) — Right to revoke: must be honored; procedure must exist
    # -----------------------------------------------------------------------

    def test_authorization_revocations_honored(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        §164.508(b)(5): Individuals may revoke an authorization in writing at any time,
        EXCEPT where the CE has taken action in reliance on the authorization or the
        authorization was obtained as a condition of obtaining insurance coverage.
        Once revoked, no further PHI use/disclosure under that authorization is permitted.
        """
        revocation_log = controls_evidence.get("authorization_revocation_log", [])

        violations = []
        for rev in revocation_log:
            rev_id = rev.get("revocation_id", "unknown")
            revoked_date = rev.get("revocation_received_date")
            phi_used_after_revocation = rev.get("phi_used_or_disclosed_after_revocation", False)
            reliance_exception = rev.get("prior_reliance_exception_documented", False)

            if phi_used_after_revocation and not reliance_exception:
                violations.append({
                    "revocation_id": rev_id,
                    "revoked_date": revoked_date,
                    "issue": "phi_used_post_revocation_no_exception",
                })

        assert not violations, (
            f"§164.508(b)(5): {len(violations)} authorization(s) had PHI used/disclosed "
            f"after revocation without a documented prior-reliance exception: {violations}."
        )

    @pytest.mark.assumption(
        id="ASSUME-HIPAA-PRIV-AUTH-001",
        description=(
            "Authorization form validation: all 9 §164.508(c) elements must appear on a single "
            "form in plain language; authorization and consent may not be combined on the same form "
            "except in limited circumstances; psychotherapy notes require separate authorization "
            "(§164.508(a)(2)) — may not be combined with general PHI authorization; "
            "marketing authorizations that involve financial remuneration must so state (§164.508(a)(3)). "
            "Expiration event: must be specific enough that the individual can determine when it occurs."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_authorization_form_templates_valid(self, controls_evidence: dict):
        """
        Pattern 2 — PARAMETERIZED.
        §164.508: Authorization form templates must be reviewed by the Privacy Officer
        to confirm all required elements are present, psychotherapy notes are
        handled separately, and marketing authorizations disclose financial remuneration.
        """
        auth_form_review = controls_evidence.get("authorization_form_template_review")

        assert auth_form_review is not None, (
            "§164.508: No authorization_form_template_review found. "
            "Authorization form templates must be reviewed and approved by the Privacy Officer."
        )

        reviewed_by = auth_form_review.get("reviewed_by")
        assert reviewed_by in ("Privacy Officer", "Legal", "Privacy Officer and Legal"), (
            f"Authorization form review signed by '{reviewed_by}' — must be Privacy Officer or Legal."
        )

        separate_psychotherapy_form = auth_form_review.get(
            "separate_psychotherapy_notes_authorization", False
        )
        assert separate_psychotherapy_form is True, (
            "§164.508(a)(2): Psychotherapy notes authorization must be on a separate form — "
            "may not be combined with general PHI authorization. "
            "authorization_form_template_review['separate_psychotherapy_notes_authorization'] must be True."
        )


# ===========================================================================
# §164.512 — Uses and Disclosures Without Authorization (Public Interest)
# ===========================================================================

class TestSection164512PublicInterestDisclosures:
    """§164.512 — 12 categories of permitted disclosures without individual authorization."""

    # -----------------------------------------------------------------------
    # §164.512 — All non-authorized disclosures must map to a permitted category
    # -----------------------------------------------------------------------

    def test_all_disclosures_have_documented_basis(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        §164.502(a): PHI may only be used/disclosed as permitted or required by the rule.
        Every disclosure that is not to the individual, for TPO, or under a valid
        authorization must map to one of the §164.512 public interest categories.
        """
        disclosure_log = controls_evidence.get("phi_disclosure_log", [])

        PERMITTED_NON_AUTH_BASES = {
            "treatment_payment_operations",
            "individual_request",
            "authorization_on_file",
            "required_by_law",
            "public_health_512a",
            "abuse_neglect_domestic_violence_512b_512c",
            "health_oversight_512d",
            "judicial_administrative_512e",
            "law_enforcement_512f",
            "decedents_512g",
            "organ_donation_512h",
            "research_512i",
            "serious_threat_512j",
            "specialized_government_512k",
            "workers_compensation_512l",
            "limited_dataset_514e",
            "de_identified_514b",
            "incidental_to_permitted_use",
        }

        undocumented = []
        for disc in disclosure_log:
            disc_id = disc.get("disclosure_id", "unknown")
            basis = disc.get("permissibility_basis")

            if basis is None:
                undocumented.append(disc_id)
            elif basis not in PERMITTED_NON_AUTH_BASES:
                undocumented.append({
                    "disclosure_id": disc_id,
                    "basis": basis,
                    "issue": "unrecognized_basis",
                })

        assert not undocumented, (
            f"§164.502(a): {len(undocumented)} PHI disclosure(s) lack a documented "
            f"permissibility basis: {undocumented}. Every disclosure must map to a "
            "permitted basis under the Privacy Rule."
        )


# ===========================================================================
# §164.514 — De-identification of Protected Health Information
# ===========================================================================

class TestSection164514DeIdentification:
    """§164.514 — Methods for de-identifying PHI and removing it from Privacy Rule scope."""

    # -----------------------------------------------------------------------
    # §164.514(b)(2) — Safe Harbor: all 18 identifiers removed
    # -----------------------------------------------------------------------

    def test_safe_harbor_datasets_have_all_18_identifiers_removed(
        self, controls_evidence: dict
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.514(b)(2): Safe Harbor de-identification requires removal of all 18 specified
        identifier categories. A dataset claiming Safe Harbor de-identification that retains
        any of the 18 identifiers is NOT de-identified and is still PHI.
        """
        safe_harbor_datasets = controls_evidence.get("safe_harbor_deidentified_datasets", [])

        violations = []
        for ds in safe_harbor_datasets:
            ds_id = ds.get("dataset_id", "unknown")
            identifiers_removed = set(ds.get("identifiers_confirmed_removed", []))
            remaining_identifiers = SAFE_HARBOR_IDENTIFIERS - identifiers_removed

            if remaining_identifiers:
                violations.append({
                    "dataset_id": ds_id,
                    "remaining_identifiers": remaining_identifiers,
                })

        assert not violations, (
            f"§164.514(b)(2): {len(violations)} Safe Harbor dataset(s) have not removed "
            f"all 18 required identifiers: {violations}. These datasets remain PHI."
        )

    def test_safe_harbor_zip_codes_compliant(self, controls_evidence: dict):
        """
        Pattern 1 — DETERMINISTIC.
        §164.514(b)(2)(i): Geographic data smaller than state must be removed,
        EXCEPT first three digits of ZIP code may be retained if the geographic
        unit formed has > 20,000 people. If the ZIP prefix covers ≤ 20,000 people,
        it must be changed to '000'. Specific check for ZIP code compliance.
        """
        safe_harbor_datasets = controls_evidence.get("safe_harbor_deidentified_datasets", [])

        for ds in safe_harbor_datasets:
            ds_id = ds.get("dataset_id", "unknown")
            zip_handling = ds.get("zip_code_handling")

            if zip_handling is None:
                continue  # no ZIP data in dataset

            method = zip_handling.get("method")
            assert method in (
                "removed_entirely",
                "first_three_digits_retained_population_verified_gt_20000",
                "converted_to_000_for_small_populations",
                "first_three_only_all_prefixes_population_gt_20000",
            ), (
                f"Safe Harbor dataset '{ds_id}': ZIP code handling method '{method}' does not "
                "satisfy §164.514(b)(2)(i). Must either remove entirely or retain only first "
                "3 digits with population > 20,000 verified."
            )

    # -----------------------------------------------------------------------
    # §164.514(b)(1) — Expert determination method
    # -----------------------------------------------------------------------

    @pytest.mark.assumption(
        id="ASSUME-HIPAA-PRIV-DEID-001",
        description=(
            "Expert determination de-identification (§164.514(b)(1)): a qualified statistician "
            "must certify that the risk of re-identification is very small. "
            "Assumption: 'qualified statistician' means holds at minimum a master's degree in "
            "statistics or biostatistics, or comparable demonstrated expertise. "
            "Certification must be written, signed, and attached to the dataset record. "
            "Certification expires: when the dataset is augmented with additional fields, "
            "when source population changes materially, or at most every 24 months. "
            "Re-identification risk threshold: < 0.09 (9%) per NIST SP 800-188 guidance."
        ),
        approved_by="Privacy Officer",
        review_date="2026-11-01",
    )
    def test_expert_determination_datasets_have_valid_certification(
        self, controls_evidence: dict, reference_date: date
    ):
        """
        Pattern 2 — PARAMETERIZED.
        §164.514(b)(1): Expert determination de-identification requires written
        certification from a qualified statistician. Certification must be current.
        """
        expert_deid_datasets = controls_evidence.get(
            "expert_determination_deidentified_datasets", []
        )

        MAX_CERT_AGE_MONTHS = 24

        for ds in expert_deid_datasets:
            ds_id = ds.get("dataset_id", "unknown")
            cert = ds.get("expert_certification")

            assert cert is not None, (
                f"Expert-determination dataset '{ds_id}': no expert_certification found. "
                "§164.514(b)(1) requires written certification from a qualified statistician."
            )

            cert_date = cert.get("certification_date")
            assert cert_date is not None, (
                f"Expert-determination dataset '{ds_id}': certification has no date."
            )

            age_months = (
                (reference_date.year - cert_date.year) * 12
                + (reference_date.month - cert_date.month)
            )
            assert age_months <= MAX_CERT_AGE_MONTHS, (
                f"Expert-determination dataset '{ds_id}': certification dated {cert_date} "
                f"is {age_months} months old (maximum {MAX_CERT_AGE_MONTHS} months). Recertification required."
            )

            certifier_qualified = cert.get("certifier_is_qualified_statistician", False)
            assert certifier_qualified is True, (
                f"Expert-determination dataset '{ds_id}': certifier qualification not confirmed. "
                "§164.514(b)(1) requires a 'qualified statistician.'"
            )

    # -----------------------------------------------------------------------
    # §164.514(e) — Limited dataset: specific identifiers removed
    # -----------------------------------------------------------------------

    def test_limited_datasets_have_required_identifiers_removed(
        self, controls_evidence: dict
    ):
        """
        Pattern 1 — DETERMINISTIC.
        §164.514(e): A limited dataset removes a subset of identifiers (not all 18)
        and may retain geographic data, dates, and other indirect identifiers.
        Must remove: names, postal address (except town/city, state, ZIP),
        phone, fax, email, SSN, medical record numbers, health plan beneficiary numbers,
        account numbers, certificate/license numbers, VINs, device IDs, URLs, IPs,
        biometric IDs, full-face photos. Must be covered by a data use agreement (DUA).
        """
        LIMITED_DATASET_REMOVED_IDENTIFIERS = {
            "names",
            "postal_address_below_city_state_zip",
            "phone_numbers",
            "fax_numbers",
            "email_addresses",
            "social_security_numbers",
            "medical_record_numbers",
            "health_plan_beneficiary_numbers",
            "account_numbers",
            "certificate_or_license_numbers",
            "vehicle_identifiers_and_serial_numbers_including_vin",
            "device_identifiers_and_serial_numbers",
            "web_urls",
            "ip_addresses",
            "biometric_identifiers_including_finger_and_voice_prints",
            "full_face_photographs_and_any_comparable_images",
        }

        limited_datasets = controls_evidence.get("limited_datasets", [])

        for ds in limited_datasets:
            ds_id = ds.get("dataset_id", "unknown")

            removed = set(ds.get("identifiers_confirmed_removed", []))
            missing = LIMITED_DATASET_REMOVED_IDENTIFIERS - removed
            assert not missing, (
                f"Limited dataset '{ds_id}': required identifiers not removed: {missing}. "
                "§164.514(e)(2) specifies identifiers that must be absent from a limited dataset."
            )

            dua_on_file = ds.get("data_use_agreement_on_file", False)
            assert dua_on_file is True, (
                f"Limited dataset '{ds_id}': no data_use_agreement_on_file. "
                "§164.514(e)(4): limited datasets must be covered by a data use agreement."
            )
