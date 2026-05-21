# GDPR — Principles, Lawful Basis, and Special Category Data

**Spec file:** `principles-lawful-basis.md`
**Registry version:** 2026.05
**Last updated:** 2026-05-21
**Applies to:** Any organization — regardless of location — that processes personal data of EU/EEA data subjects by offering goods or services to them or monitoring their behavior within the EU/EEA
**Trigger:** Offering goods or services to EU/EEA persons (Art. 3(2)(a)); monitoring behavior of EU/EEA persons within the EU/EEA (Art. 3(2)(b)); establishment in the EU/EEA (Art. 3(1))
**Jurisdiction:** European Union / EEA; strong extraterritorial reach — applies to non-EU organizations targeting EU persons; enforced by national Data Protection Authorities and the EDPB
**Not applicable to:** Purely personal or household use (Art. 2(2)(c)); national security and law enforcement activities (Directive 2016/680 instead); anonymous data (not 'personal data' within GDPR meaning); deceased persons (in most member states)
**Parent index:** [`_index.md`](./_index.md)
**Regulatory basis:** Regulation (EU) 2016/679 (GDPR) — Articles 5, 6, 9
**Authority:** EU/EEA national supervisory authorities; lead authority per main establishment
**Methodology reference:** EDPB Guidelines 05/2020 (consent); EDPB Guidelines 06/2020 (lawful basis for online services); EDPB Guidelines 2/2019 (Art. 6(1)(b)); WP29/EDPB opinions on special category data

---

## Overview

Art. 5 establishes the seven data protection principles that govern all processing. Art. 6 provides the exhaustive list of lawful bases for processing personal data. Art. 9 extends the regime to special category data, layering additional conditions on top of Art. 6.

**CONTESTED density is high.** The principles ("adequate, relevant and limited", "fair", "accurate") resist automation. The testable surface concentrates on:
- Art. 5(1)(e): storage limitation — retention schedules must exist and be enforced
- Art. 6: lawful basis must be documented before processing begins (DETERMINISTIC for existence; CONTESTED for adequacy)
- Art. 6(1)(a): consent — withdrawal mechanism and records are DETERMINISTIC
- Art. 9: special category data identification and applicable Art. 9(2) condition documentation

---

## Scope pre-condition

```python
import pytest


@pytest.fixture(autouse=True)
def gdpr_scope_check(entity_profile: dict):
    """Skip if entity does not process personal data of EU/EEA data subjects."""
    if not entity_profile.get("processes_eu_subject_data", False):
        pytest.skip(
            "GDPR does not apply — entity does not process personal data of EU/EEA "
            "data subjects (Art. 3 territorial scope not met). Note: Art. 3(2) "
            "extra-territorial scope applies to non-EU controllers/processors that "
            "offer goods/services to EU subjects or monitor their behaviour."
        )
```

---

## ARTICLE 5 — Principles of Processing

### Requirements extracted

**Source:** GDPR Art. 5

| # | Principle | Obligation | Confidence |
|---|-----------|------------|------------|
| 5.1a | Lawfulness, fairness, transparency | Processing must have a lawful basis (Art. 6); must be fair; data subjects must receive required information (Art. 13/14) | PARAMETERIZED (lawful basis) / CONTESTED (fair) |
| 5.1b | Purpose limitation | Data collected for specified, explicit and legitimate purposes; not further processed in incompatible manner | CONTESTED |
| 5.1c | Data minimization | Data adequate, relevant and limited to what is necessary for the purpose | CONTESTED |
| 5.1d | Accuracy | Personal data must be accurate and kept up to date; inaccurate data erased or rectified without delay | PARAMETERIZED |
| 5.1e | Storage limitation | Kept in identifiable form no longer than necessary; retention schedule must exist | PARAMETERIZED — retention schedule existence is testable; appropriateness is CONTESTED |
| 5.1f | Integrity and confidentiality | Appropriate security; protection against unauthorized/unlawful processing and accidental loss | CONTESTED (same as Art. 32) |
| 5.2 | Accountability | Controller must demonstrate compliance with all principles | PARAMETERIZED — accountability documentation existence is testable |

### Tests — Art. 5 principles

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


class TestArt5Principles:
    """Art. 5 — Data protection principles. Pattern 3 for CONTESTED; Pattern 2 for PARAMETERIZED."""

    def test_ropa_documents_retention_schedules(self, controls_evidence: dict):
        """Pattern 2: Art. 5(1)(e) storage limitation — retention schedules must be documented."""
        ropa_entries = controls_evidence.get("ropa_entries", [])
        assert ropa_entries, (
            "No ROPA entries found — Art. 30 requires records of processing; Art. 5(1)(e) "
            "requires retention schedules to be specified."
        )
        entries_without_retention = [
            e for e in ropa_entries
            if not e.get("retention_period_defined", False)
        ]
        assert not entries_without_retention, (
            f"ROPA entries without defined retention periods: "
            f"{[e.get('processing_activity') for e in entries_without_retention]}. "
            "GDPR Art. 5(1)(e) requires retention periods to be specified."
        )

    def test_retention_schedule_enforced(self, controls_evidence: dict, reference_date: date):
        """Pattern 2: storage limitation — data past retention period must be deleted or anonymized."""
        overdue_datasets = controls_evidence.get("datasets_past_retention_period", [])
        assert not overdue_datasets, (
            f"Datasets held past their defined retention period: "
            f"{[d.get('dataset_name') for d in overdue_datasets]}. "
            "GDPR Art. 5(1)(e) prohibits retaining personal data longer than necessary."
        )

    @pytest.mark.assumption(
        id="ASSUME-GDPR-PRIN-001",
        description=(
            "GDPR Art. 5(1)(d) accuracy principle requires personal data to be accurate "
            "and kept up to date where necessary. 'Necessary' is context-dependent: "
            "transactional/historical records may not require update; contact data and "
            "preference data do. The testable surface is: (a) each ROPA entry specifies "
            "whether data requires active accuracy maintenance; (b) for categories marked "
            "'accuracy maintenance required,' an update mechanism exists (e.g., self-service "
            "portal, periodic outreach, third-party data refresh); (c) rectification requests "
            "from data subjects are completed within the DSR deadline (Art. 12(3) — 1 month). "
            "The substantive question of whether a given dataset is 'accurate enough' is "
            "CONTESTED and requires human review."
        ),
        approved_by="DPO",
        review_date="2026-11-01",
    )
    def test_accuracy_maintenance_mechanism_defined(self, controls_evidence: dict):
        """Pattern 2: accuracy principle — categories requiring update must have a mechanism."""
        ropa_entries = controls_evidence.get("ropa_entries", [])
        accuracy_failures = [
            e for e in ropa_entries
            if e.get("requires_accuracy_maintenance", False)
            and not e.get("accuracy_maintenance_mechanism_defined", False)
        ]
        assert not accuracy_failures, (
            f"Processing activities marked as requiring accuracy maintenance but without a "
            f"defined update mechanism: {[e.get('processing_activity') for e in accuracy_failures]}. "
            "GDPR Art. 5(1)(d) requires personal data to be accurate and kept up to date."
        )

    @pytest.mark.human_review_required(
        reason=(
            "GDPR Art. 5(1)(b) purpose limitation — 'further processing in an incompatible manner' "
            "requires a legal and contextual analysis. The EDPB Guidelines on purpose limitation "
            "specify a multi-factor test (link between purposes, context of collection, nature of "
            "data, consequences, safeguards). No automated test can substitute for this analysis. "
            "REQUIRES DPO/Legal review of any new use of data collected for a different original purpose."
        )
    )
    def test_purpose_limitation_compatibility_reviewed(self, controls_evidence: dict):
        """Pattern 3: CONTESTED — purpose limitation compatibility requires human judgment."""
        secondary_uses = controls_evidence.get("secondary_processing_activities", [])
        for use in secondary_uses:
            assert use.get("compatibility_assessment_conducted", False), (
                f"Secondary use of personal data for '{use.get('secondary_purpose')}' "
                f"(originally collected for '{use.get('original_purpose')}') has no "
                "Art. 5(1)(b) compatibility assessment. REQUIRES DPO/Legal review."
            )

    def test_accountability_documentation_exists(self, controls_evidence: dict):
        """Pattern 2: Art. 5(2) accountability — controller must be able to demonstrate compliance."""
        accountability_docs = {
            "ropa_exists": "Records of Processing Activities (Art. 30)",
            "privacy_notices_current": "Privacy notices (Art. 13/14)",
            "dpa_agreements_current": "Data processing agreements (Art. 28)",
            "security_measures_documented": "Technical and organisational measures (Art. 32)",
        }
        for doc_key, doc_name in accountability_docs.items():
            assert controls_evidence.get(doc_key, False), (
                f"Art. 5(2) accountability documentation gap: '{doc_name}' not present. "
                "GDPR Art. 5(2) requires the controller to be able to demonstrate compliance."
            )
```

---

## ARTICLE 6 — Lawful Basis for Processing

### Requirements extracted

**Source:** GDPR Art. 6

| Basis | Identifier | Confidence | Notes |
|-------|-----------|------------|-------|
| Consent | 6(1)(a) | DETERMINISTIC for records/withdrawal; PARAMETERIZED for validity | Consent must be freely given, specific, informed, unambiguous; withdrawal must be easy |
| Contract | 6(1)(b) | PARAMETERIZED | "Necessary" for contract — not merely useful or desirable |
| Legal obligation | 6(1)(c) | DETERMINISTIC | Specific legal obligation must be identified |
| Vital interests | 6(1)(d) | CONTESTED | Emergency use only; DPO review required |
| Public task | 6(1)(e) | CONTESTED | Public authority processing only |
| Legitimate interests | 6(1)(f) | CONTESTED | LIA required; balancing test; cannot override data subject rights |

### Tests — Art. 6 lawful basis

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


VALID_LAWFUL_BASES = {
    "consent_6_1_a",
    "contract_6_1_b",
    "legal_obligation_6_1_c",
    "vital_interests_6_1_d",
    "public_task_6_1_e",
    "legitimate_interests_6_1_f",
}


class TestArt6LawfulBasis:
    """Art. 6 — Every processing activity must have a documented lawful basis."""

    def test_all_processing_has_documented_lawful_basis(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — lawful basis must be documented for every processing activity."""
        ropa_entries = controls_evidence.get("ropa_entries", [])
        assert ropa_entries, "No ROPA entries — cannot verify lawful basis coverage."
        entries_without_basis = [
            e for e in ropa_entries
            if not e.get("lawful_basis")
            or e.get("lawful_basis") not in VALID_LAWFUL_BASES
        ]
        assert not entries_without_basis, (
            f"Processing activities without a valid documented lawful basis: "
            f"{[e.get('processing_activity') for e in entries_without_basis]}. "
            "GDPR Art. 6 requires a lawful basis for every processing activity."
        )

    # --- CONSENT (Art. 6(1)(a)) ---

    def test_consent_records_exist(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — consent must be documented and demonstrable."""
        consent_based_activities = [
            e for e in controls_evidence.get("ropa_entries", [])
            if e.get("lawful_basis") == "consent_6_1_a"
        ]
        for activity in consent_based_activities:
            assert activity.get("consent_record_system_identified", False), (
                f"Processing activity '{activity.get('processing_activity')}' relies on "
                "consent but has no consent record system identified. GDPR Art. 7(1) "
                "requires the controller to demonstrate consent was given."
            )

    def test_consent_withdrawal_mechanism_implemented(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — withdrawal must be as easy as giving consent."""
        consent_based_activities = [
            e for e in controls_evidence.get("ropa_entries", [])
            if e.get("lawful_basis") == "consent_6_1_a"
        ]
        for activity in consent_based_activities:
            assert activity.get("withdrawal_mechanism_implemented", False), (
                f"Processing activity '{activity.get('processing_activity')}' relies on "
                "consent but has no withdrawal mechanism. GDPR Art. 7(3) requires withdrawal "
                "to be as easy as giving consent."
            )

    @pytest.mark.assumption(
        id="ASSUME-GDPR-CONSENT-001",
        description=(
            "GDPR Art. 6(1)(a) and Art. 7 consent requirements: consent must be freely given "
            "(no imbalance of power; no bundling with terms of service), specific (granular by "
            "purpose), informed (linked to Art. 13/14 privacy notice at time of collection), "
            "and unambiguous (affirmative action — pre-ticked boxes are invalid). For children "
            "under 16 (or lower national age: 13–16), parental/guardian consent required per "
            "Art. 8. Consent records must retain: timestamp, subject identifier, mechanism used, "
            "notice version shown, specific purpose(s) consented to. Withdrawal must be logged "
            "with timestamp; processing must cease within the Art. 12(3) response window. "
            "Re-obtaining consent after withdrawal requires a fresh affirmative action."
        ),
        approved_by="DPO",
        review_date="2026-11-01",
    )
    def test_consent_records_complete(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — consent record content requirements are enumerated."""
        REQUIRED_CONSENT_RECORD_FIELDS = {
            "subject_identifier",
            "timestamp",
            "mechanism",
            "notice_version_shown",
            "purposes_consented_to",
        }
        consent_records_sample = controls_evidence.get("consent_records_sample", [])
        for record in consent_records_sample:
            present_fields = set(record.get("fields_present", []))
            missing = REQUIRED_CONSENT_RECORD_FIELDS - present_fields
            assert not missing, (
                f"Consent record {record.get('record_id', 'UNKNOWN')} missing required fields: "
                f"{missing}. GDPR Art. 7(1) and ASSUME-GDPR-CONSENT-001."
            )

    def test_consent_withdrawal_processed_within_deadline(
        self, controls_evidence: dict, reference_date: date
    ):
        """Pattern 1: DETERMINISTIC — processing must cease after withdrawal within Art. 12(3) window."""
        DSR_RESPONSE_DAYS = 30
        pending_withdrawals = controls_evidence.get("consent_withdrawals_pending", [])
        for withdrawal in pending_withdrawals:
            withdrawal_date = withdrawal.get("withdrawal_date")
            if withdrawal_date is None:
                continue
            days_outstanding = (reference_date - withdrawal_date).days
            assert days_outstanding <= DSR_RESPONSE_DAYS, (
                f"Consent withdrawal received {withdrawal_date} for "
                f"'{withdrawal.get('processing_activity')}' has not been actioned after "
                f"{days_outstanding} days. Processing must cease within {DSR_RESPONSE_DAYS} days. "
                "GDPR Art. 7(3) and Art. 12(3)."
            )

    # --- LEGITIMATE INTERESTS (Art. 6(1)(f)) ---

    @pytest.mark.human_review_required(
        reason=(
            "GDPR Art. 6(1)(f) legitimate interests requires a three-part balancing test "
            "(LIA): (1) Is the interest legitimate? (2) Is processing necessary? (3) Do "
            "the controller's interests override the data subject's rights? This test is "
            "inherently CONTESTED — no automated assertion can substitute. A documented "
            "LIA by DPO/Legal is required for every legitimate interests basis reliance. "
            "LIA must be reviewed whenever the processing changes materially."
        )
    )
    def test_legitimate_interests_lia_documented(self, controls_evidence: dict):
        """Pattern 3: CONTESTED — LIA is required for every Art. 6(1)(f) reliance."""
        lia_activities = [
            e for e in controls_evidence.get("ropa_entries", [])
            if e.get("lawful_basis") == "legitimate_interests_6_1_f"
        ]
        for activity in lia_activities:
            assert activity.get("lia_documented", False), (
                f"Processing activity '{activity.get('processing_activity')}' relies on "
                "legitimate interests but has no documented Legitimate Interests Assessment. "
                "GDPR Art. 6(1)(f) — REQUIRES DPO/Legal LIA before processing continues."
            )
```

---

## ARTICLE 9 — Special Category Data

### Requirements extracted

**Source:** GDPR Art. 9

| # | Special category | Art. 9(2) condition required |
|---|-----------------|------------------------------|
| All | Racial/ethnic origin, political opinions, religious/philosophical beliefs, trade union membership, genetic data, biometric data (for ID), health data, sex life/orientation | One of Art. 9(2)(a)–(j) conditions must apply in addition to an Art. 6 lawful basis |

**Art. 9(2) conditions most relevant to commercial/employer contexts:**
- **(a)** Explicit consent (higher standard than Art. 6(1)(a) — must be "explicit")
- **(b)** Employment/social security obligations (under national law)
- **(c)** Vital interests
- **(g)** Substantial public interest
- **(h)** Medical purposes (health professional, proportionality safeguards)
- **(i)** Public health
- **(j)** Archiving/research/statistics

### Tests — Art. 9 special category data

```python
import pytest
from datetime import date


SPECIAL_CATEGORY_TYPES = {
    "racial_ethnic_origin",
    "political_opinions",
    "religious_philosophical_beliefs",
    "trade_union_membership",
    "genetic_data",
    "biometric_data_for_identification",
    "health_data",
    "sex_life_or_sexual_orientation",
}

VALID_ART9_CONDITIONS = {
    "explicit_consent_9_2_a",
    "employment_social_security_9_2_b",
    "vital_interests_9_2_c",
    "non_profit_body_9_2_d",
    "public_data_9_2_e",
    "legal_claims_9_2_f",
    "substantial_public_interest_9_2_g",
    "medical_purposes_9_2_h",
    "public_health_9_2_i",
    "archiving_research_statistics_9_2_j",
}


class TestArt9SpecialCategoryData:
    """Art. 9 — Special category data requires documented Art. 9(2) condition in addition to Art. 6 basis."""

    def test_special_category_data_identified_in_ropa(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — special category data must be identified and flagged in ROPA."""
        ropa_entries = controls_evidence.get("ropa_entries", [])
        data_categories_processed = controls_evidence.get(
            "data_categories_processed_summary", []
        )
        special_categories_processed = [
            c for c in data_categories_processed
            if c.get("category_type") in SPECIAL_CATEGORY_TYPES
        ]
        for category in special_categories_processed:
            assert category.get("flagged_as_special_category_in_ropa", False), (
                f"Data category '{category.get('category_type')}' is a GDPR Art. 9 special "
                "category but is not flagged as such in the ROPA. All special category "
                "processing must be explicitly identified."
            )

    @pytest.mark.assumption(
        id="ASSUME-GDPR-SPEC-001",
        description=(
            "GDPR Art. 9 special category data identification: biometric data is only Art. 9 "
            "special category when processed 'for the purpose of uniquely identifying a natural "
            "person' — photographs/CCTV are NOT special category unless processed through facial "
            "recognition or other biometric identification systems. Health data includes any data "
            "from which health information can be inferred, including fitness tracker data if "
            "linked to an identified person, prescription records, medical appointment attendance. "
            "Genetic data means any data resulting from DNA/RNA analysis. The Art. 9(2) condition "
            "must be documented for each processing activity involving special category data — "
            "the same condition need not apply to all; different activities may rely on different "
            "conditions. Explicit consent (9(2)(a)) has a higher standard than standard consent "
            "(Art. 6(1)(a)) — must be explicit statement, not merely unambiguous act."
        ),
        approved_by="DPO",
        review_date="2026-11-01",
    )
    def test_special_category_processing_has_art9_condition(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — each special category processing activity must document an Art. 9(2) condition."""
        ropa_entries = controls_evidence.get("ropa_entries", [])
        special_category_entries = [
            e for e in ropa_entries
            if e.get("involves_special_category_data", False)
        ]
        for entry in special_category_entries:
            art9_condition = entry.get("art9_condition")
            assert art9_condition is not None, (
                f"Processing activity '{entry.get('processing_activity')}' processes special "
                "category data but has no Art. 9(2) condition documented. Art. 9 prohibits "
                "special category processing without an applicable condition."
            )
            assert art9_condition in VALID_ART9_CONDITIONS, (
                f"Processing activity '{entry.get('processing_activity')}' documents Art. 9 "
                f"condition '{art9_condition}' which is not a valid Art. 9(2) condition."
            )

    def test_explicit_consent_for_art9_2_a(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — Art. 9(2)(a) requires explicit (not just unambiguous) consent."""
        art9_consent_activities = [
            e for e in controls_evidence.get("ropa_entries", [])
            if e.get("art9_condition") == "explicit_consent_9_2_a"
        ]
        for activity in art9_consent_activities:
            assert activity.get("consent_is_explicit_statement", False), (
                f"Processing activity '{activity.get('processing_activity')}' relies on "
                "Art. 9(2)(a) explicit consent but consent mechanism does not require an "
                "explicit statement. Art. 9(2)(a) requires explicit consent — not merely "
                "unambiguous consent as required by Art. 6(1)(a). Pre-ticked boxes and "
                "implicit consent are invalid for Art. 9 processing."
            )

    def test_special_category_enhanced_security(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — special category data warrants enhanced technical measures."""
        special_category_systems = controls_evidence.get("special_category_data_systems", [])
        for system in special_category_systems:
            assert system.get("encryption_at_rest_enabled", False), (
                f"System '{system.get('system_name')}' stores special category data but "
                "lacks at-rest encryption. GDPR Art. 32 + Art. 9 require enhanced measures "
                "for special category data."
            )
            assert system.get("access_restricted_to_need_to_know", False), (
                f"System '{system.get('system_name')}' stores special category data but "
                "does not have need-to-know access restrictions documented."
            )

    @pytest.mark.human_review_required(
        reason=(
            "GDPR Art. 9 processing under Art. 9(2)(g) 'substantial public interest' or "
            "Art. 9(2)(b) 'employment obligations' depends on national law — the specific "
            "Member State law that provides the basis must be identified and documented. "
            "Whether a specific employment data practice constitutes a 'necessary' Art. 9(2)(b) "
            "obligation under the applicable national law requires legal review. "
            "This cannot be automated."
        )
    )
    def test_national_law_basis_for_employment_or_public_interest(
        self, controls_evidence: dict
    ):
        """Pattern 3: CONTESTED — national law basis under Art. 9(2)(b)/(g) requires legal verification."""
        activities_needing_national_law = [
            e for e in controls_evidence.get("ropa_entries", [])
            if e.get("art9_condition") in {
                "employment_social_security_9_2_b",
                "substantial_public_interest_9_2_g",
            }
        ]
        for activity in activities_needing_national_law:
            assert activity.get("national_law_provision_identified", False), (
                f"Processing activity '{activity.get('processing_activity')}' relies on "
                f"Art. 9(2) condition '{activity.get('art9_condition')}' but no specific "
                "national law provision is identified. REQUIRES Legal review to confirm "
                "the national law basis."
            )
```

---

## Open assumption registry

| ID | Article | Description | Review date |
|---|---|---|---|
| ASSUME-GDPR-PRIN-001 | Art. 5(1)(d) | Accuracy maintenance: ROPA specifies whether active update required; mechanism defined for those that do; rectification requests completed within 1 month | 2026-11-01 |
| ASSUME-GDPR-CONSENT-001 | Art. 6(1)(a) | Consent validity: freely given, specific, informed, unambiguous; child age thresholds 13–16 per national law; record fields: subject ID, timestamp, mechanism, notice version, purposes; withdrawal logged and actioned within Art. 12(3) window | 2026-11-01 |
| ASSUME-GDPR-SPEC-001 | Art. 9 | Special category identification: biometric = only when used for identification; health data includes inferred health info; Art. 9(2) condition documented per activity; explicit consent under 9(2)(a) requires explicit statement | 2026-11-01 |
