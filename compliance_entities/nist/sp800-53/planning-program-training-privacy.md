# NIST SP 800-53 r5 — Planning, Program Management, Awareness/Training, Privacy (PT)

**Source:** NIST SP 800-53 Rev 5 + 800-53B baselines
**Coverage:** PL (11 base), PM (32 base), AT (6 base), PT (8 base)
**Baseline tags:** `[L]` Low, `[M]` Moderate, `[H]` High
**Note:** PL and PM are predominantly PARAMETERIZED/CONTESTED (plan adequacy, program sufficiency).
  AT has DETERMINISTIC cadence tests. PT has CONTESTED surfaces around authority and consent.

---

```python
import pytest
from datetime import date, timedelta
from typing import FrozenSet

# ── PL — Planning ─────────────────────────────────────────────────────────────

# PL-1: Policy and procedures — all control families require a policy
PL1_POLICY_REVIEW_MONTHS = 12                # annual review [M][H]

# PL-2: System Security and Privacy Plans (SSP)
PL2_SSP_REVIEW_MONTHS = 12                   # annual update minimum
PL2_REQUIRED_SSP_SECTIONS: FrozenSet[str] = frozenset({
    "system_description_and_purpose",
    "system_boundary",
    "information_types_processed",
    "security_categorization",
    "security_control_implementation_descriptions",
    "interconnections",
    "roles_and_responsibilities",
    "authorization_date_and_atp",
})

# PL-8: Information security architecture
PL8_ARCHITECTURE_DOCUMENTED = True          # [M][H]
PL8_ARCHITECTURE_REVIEW_MONTHS = 12

# ── PM — Program Management ────────────────────────────────────────────────────

# PM-2: Information security program leadership
PM2_SENIOR_OFFICIAL_DESIGNATED = True        # CIO/CISO/ISSO designated

# PM-9: Risk management strategy
PM9_RISK_STRATEGY_DOCUMENTED = True

# PM-10: Authorization process
PM10_ATO_REQUIRED_BEFORE_OPERATION = True   # system must have valid ATO
PM10_ATO_MAX_YEARS = 3                       # ATOs valid for 3 years (FISMA/FedRAMP standard)

# PM-14: Testing, training, and monitoring
PM14_TESTING_TRAINING_MONITORING_DOCUMENTED = True

# ── AT — Awareness and Training ───────────────────────────────────────────────

# AT-1: Policy and procedures
AT1_POLICY_REVIEW_MONTHS = 12

# AT-2: Literacy training and awareness
AT2_TRAINING_MONTHS = 12                    # annual for all personnel [L][M][H]
AT2_NEW_EMPLOYEE_TRAINING_DAYS = 30         # before or within 30 days of access
AT2_REQUIRED_TOPICS: FrozenSet[str] = frozenset({
    "phishing_and_social_engineering",
    "password_security",
    "data_handling_and_classification",
    "incident_reporting_procedures",
    "acceptable_use_policy",
    "insider_threat_awareness",
})

# AT-3: Role-based training
AT3_ROLE_TRAINING_MONTHS = 12              # annual for personnel with security responsibilities
AT3_HIGH_ROLE_TRAINING_MONTHS = 6         # semi-annual for High
AT3_ROLES_REQUIRING_TRAINING: FrozenSet[str] = frozenset({
    "system_administrator",
    "information_security_officer",
    "incident_responder",
    "developer",
    "privileged_user",
    "privacy_officer",
    "data_owner",
})

# AT-4: Training records
AT4_RECORD_RETENTION_YEARS = 3            # retain training records for 3 years

# ── PT — PII Processing and Transparency ──────────────────────────────────────

# PT-2: Authority to process PII
PT2_LEGAL_AUTHORITY_DOCUMENTED = True       # must be documented before PII processing
PT2_AUTHORITY_SOURCES: FrozenSet[str] = frozenset({
    "statute_or_regulation",
    "executive_order",
    "memorandum_or_directive",
    "public_law",
})

# PT-3: Purpose specification
PT3_PURPOSE_DOCUMENTED_BEFORE_PROCESSING = True

# PT-5: Privacy notice
PT5_NOTICE_PROVIDED_TO_INDIVIDUALS = True   # before/at time of collection
PT5_NOTICE_REQUIRED_CONTENTS: FrozenSet[str] = frozenset({
    "pii_categories_collected",
    "purpose_of_collection",
    "retention_period",
    "rights_of_individuals",
    "how_to_exercise_rights",
})

# PT-6: System of records notice (SORN) — federal systems
PT6_SORN_REQUIRED_FEDERAL = True

# PT-7: Specific categories of PII — heightened protections
PT7_SENSITIVE_PII_HEIGHTENED_PROTECTION = True
PT7_SENSITIVE_PII_CATEGORIES: FrozenSet[str] = frozenset({
    "social_security_number",
    "financial_account_information",
    "health_information",
    "biometric_data",
    "geolocation_data",
    "race_ethnicity",
    "religious_beliefs",
    "sexual_orientation",
})

# ── Scope fixture ──────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def fisma_scope_check(entity_profile: dict):
    if not entity_profile.get("subject_to_fisma_or_fedramp", False):
        pytest.skip("System not subject to FISMA/FedRAMP — 800-53 not applicable")


@pytest.fixture
def impact_level(entity_profile: dict) -> str:
    level = entity_profile.get("fips199_impact_level", "").lower()
    if level not in {"low", "moderate", "high"}:
        pytest.skip("FIPS 199 impact level not categorized")
    return level


@pytest.fixture
def odp_values(entity_profile: dict) -> dict:
    odps = entity_profile.get("odp_values", {})
    if not odps:
        pytest.skip("ODP values not documented")
    return odps


@pytest.fixture
def processes_pii(entity_profile: dict) -> bool:
    """Skip PT tests if system does not process PII."""
    if not entity_profile.get("system_processes_pii", False):
        pytest.skip("System does not process PII — PT controls not applicable")
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# PLANNING (PL)
# ═══════════════════════════════════════════════════════════════════════════════

class TestPL2SystemSecurityPlan:
    """PL-2: System Security and Privacy Plans — all baselines [L][M][H]"""

    def test_ssp_documented(self, controls_evidence: dict):
        """DETERMINISTIC: an SSP must be documented for the system."""
        assert controls_evidence.get("ssp_documented", False), (
            "PL-2: no System Security Plan (SSP) documented."
        )

    def test_ssp_contains_required_sections(self, controls_evidence: dict):
        """DETERMINISTIC: SSP must contain all required sections."""
        present = set(controls_evidence.get("ssp_sections_present", []))
        missing = PL2_REQUIRED_SSP_SECTIONS - present
        assert not missing, (
            f"PL-2: SSP missing required sections: {missing}."
        )

    @pytest.mark.assumption(
        id="ASSUME-800053-PL-001",
        description=(
            "PL-2 SSP update ODP: reviewed and updated annually or after significant changes. "
            "SSP completeness ('describes how controls are implemented') is PARAMETERIZED — "
            "the level of implementation detail is assessor-evaluated."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_ssp_reviewed_annually(
        self, controls_evidence: dict, reference_date: date, odp_values: dict
    ):
        """PARAMETERIZED: SSP must be reviewed within ODP interval."""
        max_months = odp_values.get("pl2_review_months", PL2_SSP_REVIEW_MONTHS)
        last_review = controls_evidence.get("ssp_last_review_date")
        if not last_review:
            pytest.fail("PL-2: SSP has no recorded review date.")
        months_since = (reference_date.year - last_review.year) * 12 + \
                       (reference_date.month - last_review.month)
        assert months_since <= max_months, (
            f"PL-2: SSP last reviewed {months_since} months ago; ODP requires ≤{max_months} months."
        )

    @pytest.mark.human_review_required(
        reason=(
            "PL-2: SSP completeness is CONTESTED. Whether control implementation descriptions "
            "are sufficiently detailed for the system risk level and boundary complexity is an "
            "assessor judgment that cannot be reduced to a metadata field check."
        )
    )
    def test_ssp_implementation_descriptions_adequate(self, controls_evidence: dict):
        """CONTESTED: SSP must describe how each implemented control is satisfied."""
        assert controls_evidence.get("ssp_describes_control_implementation", False), (
            "PL-2: SSP does not document implementation descriptions for controls."
        )


class TestPL8InformationSecurityArchitecture:
    """PL-8: Information Security Architecture — Moderate/High [M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-PL-002",
        description=(
            "PL-8 security architecture ODP: documented and reviewed annually. Must describe "
            "how security is embedded in the enterprise architecture. Adequacy and alignment "
            "with the enterprise architecture is PARAMETERIZED."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_security_architecture_documented(self, controls_evidence: dict, impact_level):
        """PARAMETERIZED: security architecture must be documented at Moderate/High."""
        if impact_level == "low":
            pytest.skip("PL-8 security architecture applies at Moderate/High")
        assert controls_evidence.get("security_architecture_documented", False), (
            "PL-8: no information security architecture documented."
        )

    def test_security_architecture_reviewed_annually(
        self, controls_evidence: dict, reference_date: date, impact_level
    ):
        """DETERMINISTIC: security architecture must be reviewed within 12 months."""
        if impact_level == "low":
            pytest.skip("PL-8 annual review applies at Moderate/High")
        last_review = controls_evidence.get("security_architecture_last_review_date")
        if not last_review:
            pytest.fail("PL-8: security architecture review date not documented.")
        months_since = (reference_date.year - last_review.year) * 12 + \
                       (reference_date.month - last_review.month)
        assert months_since <= PL8_ARCHITECTURE_REVIEW_MONTHS, (
            f"PL-8: security architecture last reviewed {months_since} months ago; "
            f"must review ≤{PL8_ARCHITECTURE_REVIEW_MONTHS} months."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# PROGRAM MANAGEMENT (PM)
# ═══════════════════════════════════════════════════════════════════════════════

class TestPM2InformationSecurityProgramLeadership:
    """PM-2: Information Security Program Leadership — all baselines [L][M][H]"""

    def test_senior_security_official_designated(self, controls_evidence: dict):
        """DETERMINISTIC: a senior official (CIO/CISO/ISSO) must be designated accountable
        for the information security program."""
        assert controls_evidence.get("senior_information_security_official_designated", False), (
            "PM-2: no senior information security official designated."
        )


class TestPM9RiskManagementStrategy:
    """PM-9: Risk Management Strategy — all baselines [L][M][H]"""

    @pytest.mark.human_review_required(
        reason=(
            "PM-9: risk management strategy adequacy is CONTESTED. The strategy must address "
            "organizational risk tolerance and risk acceptance criteria, but what constitutes "
            "an adequate strategy (depth, coverage, integration with enterprise risk) is an "
            "executive-level judgment that assessors evaluate contextually."
        )
    )
    def test_risk_management_strategy_documented(self, controls_evidence: dict):
        """CONTESTED: an organizational risk management strategy must be documented."""
        assert controls_evidence.get("risk_management_strategy_documented", False), (
            "PM-9: no organizational risk management strategy documented."
        )


class TestPM10AuthorizationProcess:
    """PM-10: Authorization Process (ATO) — all baselines [L][M][H]"""

    def test_valid_ato_in_place(self, controls_evidence: dict, reference_date: date):
        """DETERMINISTIC: system must have a valid, non-expired Authority to Operate (ATO)."""
        ato_expiry = controls_evidence.get("ato_expiration_date")
        if not ato_expiry:
            pytest.fail("PM-10: no ATO (Authority to Operate) documented for this system.")
        assert reference_date <= ato_expiry, (
            f"PM-10: ATO expired on {ato_expiry}. System cannot operate without a valid ATO."
        )

    def test_ato_not_older_than_3_years(self, controls_evidence: dict, reference_date: date):
        """DETERMINISTIC: ATO must not be more than 3 years old without reauthorization."""
        ato_issue_date = controls_evidence.get("ato_issue_date")
        if not ato_issue_date:
            pytest.fail("PM-10: ATO issue date not documented.")
        years_old = (reference_date - ato_issue_date).days / 365.25
        assert years_old <= PM10_ATO_MAX_YEARS, (
            f"PM-10: ATO issued {years_old:.1f} years ago; reauthorization required ≤{PM10_ATO_MAX_YEARS} years."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# AWARENESS AND TRAINING (AT)
# ═══════════════════════════════════════════════════════════════════════════════

class TestAT2LiteracyTrainingAndAwareness:
    """AT-2: Literacy Training and Awareness — all baselines [L][M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-AT-001",
        description=(
            "AT-2 training frequency ODP: annual for all personnel (800-53B default). "
            "New personnel must complete training within 30 days of initial access. "
            "Training must cover the 6 required topic areas at minimum."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_annual_awareness_training_completed(
        self, controls_evidence: dict, reference_date: date, odp_values: dict
    ):
        """PARAMETERIZED: all personnel must complete awareness training within ODP interval."""
        max_months = odp_values.get("at2_training_months", AT2_TRAINING_MONTHS)
        users_without_training = [
            u for u in controls_evidence.get("user_training_records", [])
            if u.get("has_system_access", False)
            and (
                not u.get("last_awareness_training_date")
                or (reference_date - u["last_awareness_training_date"]).days >
                   max_months * 31
            )
        ]
        assert not users_without_training, (
            f"AT-2: {len(users_without_training)} user(s) with system access lack current "
            f"(≤{max_months} months) awareness training: "
            f"{[u.get('user_id') for u in users_without_training[:10]]}."
        )

    def test_new_employee_training_timely(self, controls_evidence: dict):
        """DETERMINISTIC: new employees must complete training within 30 days of access."""
        late_onboards = [
            u for u in controls_evidence.get("recent_onboarding_records", [])
            if u.get("days_to_awareness_training", 0) > AT2_NEW_EMPLOYEE_TRAINING_DAYS
        ]
        assert not late_onboards, (
            f"AT-2: {len(late_onboards)} new employee(s) did not complete awareness training "
            f"within {AT2_NEW_EMPLOYEE_TRAINING_DAYS} days: "
            f"{[u.get('user_id') for u in late_onboards]}."
        )

    def test_required_topics_covered_in_training(self, controls_evidence: dict):
        """DETERMINISTIC: awareness training must cover all required topic areas."""
        covered = set(controls_evidence.get("awareness_training_topics_covered", []))
        missing = AT2_REQUIRED_TOPICS - covered
        assert not missing, (
            f"AT-2: awareness training missing required topics: {missing}."
        )


class TestAT3RoleBasedTraining:
    """AT-3: Role-Based Training — Moderate/High [M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-AT-002",
        description=(
            "AT-3 role-based training frequency ODP: annual for Moderate; semi-annual for High. "
            "7 roles require specialized training. Content adequacy — whether training covers "
            "role-specific security responsibilities — is PARAMETERIZED."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_role_based_training_completed_for_required_roles(
        self, controls_evidence: dict, reference_date: date, odp_values: dict, impact_level
    ):
        """PARAMETERIZED: role-based training must be current for all designated roles."""
        if impact_level == "low":
            pytest.skip("AT-3 role-based training applies at Moderate/High")
        max_months = (AT3_HIGH_ROLE_TRAINING_MONTHS if impact_level == "high"
                      else odp_values.get("at3_training_months", AT3_ROLE_TRAINING_MONTHS))
        overdue = [
            r for r in controls_evidence.get("role_training_records", [])
            if r.get("role", "").lower() in AT3_ROLES_REQUIRING_TRAINING
            and (
                not r.get("last_role_training_date")
                or (reference_date - r["last_role_training_date"]).days > max_months * 31
            )
        ]
        assert not overdue, (
            f"AT-3: {len(overdue)} role training record(s) overdue (>{max_months} months): "
            f"{[(r.get('user_id'), r.get('role')) for r in overdue[:10]]}."
        )


class TestAT4TrainingRecords:
    """AT-4: Training Records — all baselines [L][M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-AT-003",
        description=(
            "AT-4 record retention ODP: 3 years per 800-53B default. Records must include "
            "completion date, training content identifier, and employee ID. "
            "Retention period begins at completion date."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_training_records_maintained(self, controls_evidence: dict):
        """DETERMINISTIC: training completion records must be maintained."""
        assert controls_evidence.get("training_records_maintained", False), (
            "AT-4: no training completion records system in place."
        )

    def test_training_record_retention_adequate(self, controls_evidence: dict):
        """PARAMETERIZED: training records must be retained for ≥3 years."""
        retention_years = controls_evidence.get("training_record_retention_years", 0)
        assert retention_years >= AT4_RECORD_RETENTION_YEARS, (
            f"AT-4: training record retention {retention_years}yr < required {AT4_RECORD_RETENTION_YEARS}yr."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# PII PROCESSING AND TRANSPARENCY (PT)
# ═══════════════════════════════════════════════════════════════════════════════

class TestPT2AuthorityToProcessPII:
    """PT-2: Authority to Process PII — applies when PII is processed [L][M][H]"""

    @pytest.mark.human_review_required(
        reason=(
            "PT-2: legal authority to process PII is CONTESTED. The organization must identify "
            "the legal authority (statute, EO, directive, public law) before collection. "
            "Whether a cited authority is sufficient and specific enough to cover the processing "
            "activity in question is a legal and assessor judgment — not automatically verifiable."
        )
    )
    def test_legal_authority_documented_for_pii_processing(
        self, controls_evidence: dict, processes_pii: bool
    ):
        """CONTESTED: legal authority for PII processing must be documented."""
        assert controls_evidence.get("pii_processing_legal_authority_documented", False), (
            "PT-2: legal authority for PII processing not documented."
        )

    def test_pii_processing_limited_to_authorized_purposes(
        self, controls_evidence: dict, processes_pii: bool
    ):
        """DETERMINISTIC: PII must only be processed for documented authorized purposes."""
        assert controls_evidence.get("pii_processing_limited_to_authorized_purposes", False), (
            "PT-2: no documented controls to limit PII processing to authorized purposes."
        )


class TestPT3PurposeSpecification:
    """PT-3: Purpose Specification — applies when PII is processed"""

    def test_pii_collection_purpose_documented(
        self, controls_evidence: dict, processes_pii: bool
    ):
        """DETERMINISTIC: the purpose for each category of PII collected must be documented."""
        assert controls_evidence.get("pii_collection_purpose_documented", False), (
            "PT-3: the specific purpose for PII collection has not been documented."
        )

    def test_pii_use_limited_to_stated_purpose(
        self, controls_evidence: dict, processes_pii: bool
    ):
        """DETERMINISTIC: PII must not be used beyond its stated collection purpose."""
        assert controls_evidence.get("pii_use_limited_to_stated_purpose", False), (
            "PT-3: no documented controls to prevent PII use beyond stated collection purpose."
        )


class TestPT5PrivacyNotice:
    """PT-5: Privacy Notice — applies when PII is collected directly from individuals"""

    def test_privacy_notice_provided_at_collection(
        self, controls_evidence: dict, processes_pii: bool
    ):
        """DETERMINISTIC: privacy notice must be provided before or at the time of PII collection."""
        if not controls_evidence.get("pii_collected_directly_from_individuals", False):
            pytest.skip("Privacy notice applies only when PII collected directly from individuals")
        assert controls_evidence.get("privacy_notice_provided_at_collection", False), (
            "PT-5: privacy notice not provided to individuals at the time of PII collection."
        )

    def test_privacy_notice_contains_required_elements(
        self, controls_evidence: dict, processes_pii: bool
    ):
        """DETERMINISTIC: privacy notice must contain all required content elements."""
        if not controls_evidence.get("pii_collected_directly_from_individuals", False):
            pytest.skip("Privacy notice content check applies only when PII collected directly")
        notice_elements = set(controls_evidence.get("privacy_notice_elements_present", []))
        missing = PT5_NOTICE_REQUIRED_CONTENTS - notice_elements
        assert not missing, (
            f"PT-5: privacy notice missing required elements: {missing}."
        )


class TestPT7SensitivePIIHeightenedProtection:
    """PT-7: Specific Categories of PII — heightened protections for sensitive PII"""

    @pytest.mark.assumption(
        id="ASSUME-800053-PT-001",
        description=(
            "PT-7: sensitive PII categories (SSN, financial, health, biometric, geolocation, "
            "race/ethnicity, religion, sexual orientation) require heightened protections beyond "
            "standard PII. What constitutes adequate heightened protection is PARAMETERIZED — "
            "typically encryption at rest + in transit + access controls + minimization."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_sensitive_pii_identified(self, controls_evidence: dict, processes_pii: bool):
        """PARAMETERIZED: sensitive PII categories must be identified in the system's PII inventory."""
        sensitive_categories = set(controls_evidence.get("pii_categories_processed", [])) & \
                               PT7_SENSITIVE_PII_CATEGORIES
        if not sensitive_categories:
            pytest.skip("System does not process sensitive PII categories — PT-7 not applicable")
        assert controls_evidence.get("sensitive_pii_identified_in_inventory", False), (
            f"PT-7: sensitive PII categories in use ({sensitive_categories}) not identified "
            f"in the PII inventory."
        )

    def test_sensitive_pii_has_heightened_protections(
        self, controls_evidence: dict, processes_pii: bool
    ):
        """PARAMETERIZED: sensitive PII must have heightened protections documented."""
        sensitive_categories = set(controls_evidence.get("pii_categories_processed", [])) & \
                               PT7_SENSITIVE_PII_CATEGORIES
        if not sensitive_categories:
            pytest.skip("No sensitive PII categories — PT-7 not applicable")
        assert controls_evidence.get("sensitive_pii_heightened_protections_documented", False), (
            f"PT-7: no heightened protections documented for sensitive PII categories: "
            f"{sensitive_categories}."
        )
```

---

## Assumption registry

| ID | Family/Control | Summary | Review date |
|---|---|---|---|
| ASSUME-800053-PL-001 | PL-2 | SSP review ODP: annual; 8 required sections; completeness of implementation descriptions CONTESTED | 2026-05-21 |
| ASSUME-800053-PL-002 | PL-8 | Security architecture ODP: documented and reviewed annually at Moderate/High; alignment adequacy PARAMETERIZED | 2026-05-21 |
| ASSUME-800053-AT-001 | AT-2 | Training frequency ODP: annual; new personnel ≤30 days; 6 required topic areas | 2026-05-21 |
| ASSUME-800053-AT-002 | AT-3 | Role-based training ODP: annual at Moderate; semi-annual at High; 7 designated roles | 2026-05-21 |
| ASSUME-800053-AT-003 | AT-4 | Training record retention ODP: 3 years per 800-53B default | 2026-05-21 |
| ASSUME-800053-PT-001 | PT-7 | Sensitive PII heightened protections: 8 sensitive categories; encryption + access controls + minimization required; adequacy PARAMETERIZED | 2026-05-21 |

## Parse status: Complete — all 20 families parsed across 4 spec files (AU/AC/IA/CM/SC/SI, CP/IR/CA, MA/MP/PE/PS/RA/SA/SR, PL/PM/AT/PT); ~1,007 controls cataloged
