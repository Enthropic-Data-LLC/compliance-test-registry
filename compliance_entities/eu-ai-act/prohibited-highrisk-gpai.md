# EU AI Act — Prohibited Practices, High-Risk AI Obligations, and GPAI Requirements

**Framework:** Regulation (EU) 2024/1689 (EU AI Act) — in force August 1 2024; phased enforcement
**Clauses:** Art. 5 (prohibited practices — 8 absolute prohibitions); Art. 9 (risk management system); Art. 11 + Annex IV (technical documentation — 8-section checklist); Art. 12/19 (logging requirements — 6-month deployer retention); Art. 13 (transparency to deployers); Art. 14 (human oversight); Art. 17 (quality management system); Art. 18 (documentation retention — 10 years); Art. 27 (fundamental rights impact assessment); Art. 43 (conformity assessment); Art. 49 (EU database registration); Art. 51–56 (GPAI — systemic risk: 10^25 FLOPs threshold); Art. 73 (serious incident reporting — 15 days / 3 months)
**Confidence:** DETERMINISTIC-dominant (8 prohibited practice binary gates; technical documentation 10-year retention; deployer log 6-month retention; serious incident 15-day/3-month reporting; EU database registration before market placement; conformity assessment before CE marking; GPAI systemic-risk 10^25 FLOPs threshold); PARAMETERIZED (risk management system; data governance; human oversight implementation; QMS scope); CONTESTED (high-risk classification for edge cases; fundamental rights impact assessment methodology)
**Last parsed:** 2026-05-21
**Applies to:** AI system providers (developers/deployers placing AI on EU market or putting into service); deployers (using AI systems); importers and distributors of AI in EU; applies regardless of provider's location — non-EU entities placing AI on EU market must comply; GPAI model providers whose models are used in AI systems
**Trigger:** Placing an AI system on the EU market or putting it into service in the EU; offering AI services to EU users; GPAI model training and distribution to downstream integrators; enforcement phased: GPAI Aug 2025, High-risk (Annex I) Aug 2026, full enforcement Aug 2027
**Jurisdiction:** European Union; enforced by European AI Office (for GPAI) and national competent authorities per member state; national market surveillance authorities for product safety aspects; substantial fines: up to €35M or 7% global turnover for prohibited practices; €15M or 3% for other violations
**Not applicable to:** AI systems exclusively for national security, military, or defense purposes (Art. 2(3)); AI systems used by public authorities of third countries for law enforcement/judicial purposes in the context of police cooperation; research and development prototypes not yet on the market; open-source GPAI models (limited exemptions for documentation obligations); purely personal non-professional use

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def eu_ai_act_scope(entity_profile: dict):
    subject = (
        entity_profile.get("places_ai_on_eu_market", False)
        or entity_profile.get("deploys_ai_in_eu", False)
        or entity_profile.get("gpai_model_provider", False)
    )
    if not subject:
        pytest.skip(
            "EU AI Act (Regulation (EU) 2024/1689) does not apply — entity does not place "
            "AI systems on the EU market, deploy AI in the EU, or provide GPAI models."
        )

@pytest.fixture
def high_risk_ai_scope(entity_profile: dict):
    """Applies to providers/deployers of high-risk AI systems (Art. 6, Annex III)."""
    if not entity_profile.get("has_high_risk_ai_system", False):
        pytest.skip(
            "High-risk AI obligations apply only to systems classified as high-risk "
            "under Art. 6 (Annex I safety components) or Art. 6(2) (Annex III domains)."
        )

@pytest.fixture
def gpai_scope(entity_profile: dict):
    """Applies to GPAI model providers (Title VIII, Art. 51-56)."""
    if not entity_profile.get("gpai_model_provider", False):
        pytest.skip("GPAI model obligations apply only to providers of general-purpose AI models.")

@pytest.fixture
def systemic_risk_gpai_scope(entity_profile: dict):
    """Applies to GPAI models with systemic risk designation (> 10^25 FLOPs)."""
    if not entity_profile.get("gpai_systemic_risk_model", False):
        pytest.skip(
            "Systemic-risk GPAI obligations apply only to models trained with > 10^25 FLOPs "
            "or designated by the AI Office."
        )
```

---

## Constants

```python
from typing import FrozenSet
from decimal import Decimal

# ── Art. 5 — Prohibited practices (8 absolute prohibitions) ──────────────────

PROHIBITED_AI_PRACTICES: FrozenSet[str] = frozenset({
    "subliminal_manipulation_causing_harm",                       # Art. 5(1)(a)
    "exploiting_vulnerabilities_of_specific_groups",              # Art. 5(1)(b)
    "social_scoring_by_public_authorities",                       # Art. 5(1)(c)
    "real_time_remote_biometric_identification_law_enforcement",  # Art. 5(1)(d) — narrow exceptions
    "emotion_recognition_workplace_education",                    # Art. 5(1)(e) — safety/medical exceptions
    "biometric_categorization_sensitive_characteristics",         # Art. 5(1)(f)
    "untargeted_facial_image_scraping_for_recognition_database",  # Art. 5(1)(g)
    "criminal_recidivism_prediction_protected_characteristics",   # Art. 5(1)(h)
})

# ── Art. 18 — Technical documentation retention ───────────────────────────────

AI_ACT_TECHNICAL_DOCUMENTATION_RETENTION_YEARS = 10

# ── Art. 19 — Deployer log retention ─────────────────────────────────────────

AI_ACT_DEPLOYER_LOG_RETENTION_MONTHS = 6

# ── Art. 73 — Serious incident reporting ──────────────────────────────────────

AI_ACT_SERIOUS_INCIDENT_DEATH_SERIOUS_HARM_DAYS = 15
AI_ACT_SERIOUS_INCIDENT_OTHER_MONTHS = 3

# ── Art. 51 — GPAI systemic risk threshold ────────────────────────────────────

GPAI_SYSTEMIC_RISK_FLOPS_THRESHOLD = Decimal("1e25")   # > 10^25 FLOPs training compute

# ── Annex IV — Technical documentation required sections ─────────────────────

ANNEX_IV_REQUIRED_SECTIONS: FrozenSet[str] = frozenset({
    "general_description_of_ai_system",
    "detailed_description_elements_and_development_process",
    "monitoring_functioning_controlling_ai_system",
    "description_of_appropriateness_of_performance_metrics",
    "risk_management_system_description",
    "description_of_changes_to_system",
    "list_of_harmonised_standards_applied",
    "eu_declaration_of_conformity",
})
```

---

## TestProhibitedPractices

```python
class TestProhibitedPractices:
    """Art. 5 — 8 absolute prohibited AI practices: binary DETERMINISTIC gates."""

    def test_ai_system_does_not_use_prohibited_technique(self, entity_profile: dict):
        """Art. 5: Any AI system implementing a prohibited practice must not be placed
        on the EU market or put into service. These are absolute prohibitions."""
        for ai_system in entity_profile.get("ai_systems", []):
            system_id = ai_system.get("id", "unknown")
            system_functions = frozenset(ai_system.get("functions", []))
            prohibited_found = system_functions & PROHIBITED_AI_PRACTICES
            assert not prohibited_found, (
                f"AI system '{system_id}' implements prohibited practice(s): "
                f"{sorted(prohibited_found)} — Art. 5 EU AI Act: absolute prohibition"
            )

    def test_no_social_scoring_by_public_authority_ai(self, entity_profile: dict):
        """Art. 5(1)(c): Public authorities may not use AI to evaluate or classify
        natural persons' social behavior for social scoring with detrimental effects."""
        if not entity_profile.get("is_public_authority", False):
            pytest.skip("Social scoring prohibition in Art. 5(1)(c) applies to public authorities")
        for ai_system in entity_profile.get("ai_systems", []):
            assert not ai_system.get("implements_social_scoring", False), (
                f"AI system '{ai_system.get('id', 'unknown')}' implements social scoring — "
                f"prohibited for public authorities under Art. 5(1)(c) EU AI Act"
            )

    def test_no_real_time_rbi_in_public_spaces_without_exception(self, entity_profile: dict):
        """Art. 5(1)(d): Real-time remote biometric identification (RBI) in public spaces
        by law enforcement is prohibited except for narrow specified purposes."""
        if not entity_profile.get("is_law_enforcement_authority", False):
            pytest.skip("Real-time RBI prohibition in Art. 5(1)(d) applies to law enforcement")
        for ai_system in entity_profile.get("ai_systems", []):
            if ai_system.get("implements_real_time_rbi_public_spaces") is True:
                exceptions = entity_profile.get("rbi_authorized_exceptions", [])
                assert exceptions, (
                    f"AI system '{ai_system.get('id', 'unknown')}' uses real-time RBI in "
                    f"public spaces without an authorized exception — Art. 5(1)(d) EU AI Act"
                )
```

---

## TestHighRiskAIObligations

```python
class TestHighRiskAIObligations:
    """Art. 9–17, 43, 49 — High-risk AI system obligations."""

    def test_technical_documentation_exists_before_market_placement(
        self, high_risk_ai_scope, entity_profile: dict
    ):
        """Art. 11 + Annex IV: Technical documentation must be drawn up before placing
        high-risk AI system on the market or putting it into service."""
        for ai_system in entity_profile.get("high_risk_ai_systems", []):
            assert ai_system.get("technical_documentation_exists") is True, (
                f"High-risk AI system '{ai_system.get('id', 'unknown')}' has no technical "
                f"documentation — Art. 11 requires documentation before market placement"
            )

    def test_technical_documentation_contains_all_annex_iv_sections(
        self, high_risk_ai_scope, entity_profile: dict
    ):
        """Annex IV: Technical documentation must include all 8 required sections."""
        for ai_system in entity_profile.get("high_risk_ai_systems", []):
            doc_sections = frozenset(ai_system.get("technical_documentation_sections", []))
            missing = ANNEX_IV_REQUIRED_SECTIONS - doc_sections
            assert not missing, (
                f"Technical documentation for '{ai_system.get('id', 'unknown')}' missing "
                f"Annex IV sections: {sorted(missing)}"
            )

    def test_technical_documentation_retained_10_years(
        self, high_risk_ai_scope, entity_profile: dict
    ):
        """Art. 18: Technical documentation must be retained for 10 years after last
        placement on the market."""
        for ai_system in entity_profile.get("high_risk_ai_systems", []):
            retention_years = ai_system.get("technical_documentation_retention_years", 0)
            assert retention_years >= AI_ACT_TECHNICAL_DOCUMENTATION_RETENTION_YEARS, (
                f"AI system '{ai_system.get('id', 'unknown')}' technical documentation "
                f"retention {retention_years} years is less than the 10-year requirement — "
                f"Art. 18 EU AI Act"
            )

    def test_logging_capability_implemented(self, high_risk_ai_scope, entity_profile: dict):
        """Art. 12: High-risk AI systems must have automatic logging capability."""
        for ai_system in entity_profile.get("high_risk_ai_systems", []):
            assert ai_system.get("automatic_logging_capability") is True, (
                f"High-risk AI system '{ai_system.get('id', 'unknown')}' lacks automatic "
                f"logging capability — Art. 12 EU AI Act"
            )

    def test_deployer_retains_logs_at_least_6_months(
        self, high_risk_ai_scope, entity_profile: dict
    ):
        """Art. 19: Deployers of high-risk AI systems must retain logs for at least 6 months."""
        if not entity_profile.get("is_ai_deployer", False):
            pytest.skip("Log retention obligation in Art. 19 applies to deployers")
        for ai_system in entity_profile.get("high_risk_ai_systems", []):
            log_retention_months = ai_system.get("deployer_log_retention_months", 0)
            assert log_retention_months >= AI_ACT_DEPLOYER_LOG_RETENTION_MONTHS, (
                f"Deployer log retention for '{ai_system.get('id', 'unknown')}' is "
                f"{log_retention_months} months — must be at least "
                f"{AI_ACT_DEPLOYER_LOG_RETENTION_MONTHS} months (Art. 19)"
            )

    def test_conformity_assessment_completed_before_market_placement(
        self, high_risk_ai_scope, entity_profile: dict
    ):
        """Art. 43: High-risk AI system must undergo conformity assessment before CE marking."""
        for ai_system in entity_profile.get("high_risk_ai_systems", []):
            assert ai_system.get("conformity_assessment_completed") is True, (
                f"High-risk AI system '{ai_system.get('id', 'unknown')}' conformity "
                f"assessment not completed — Art. 43 requires assessment before CE marking"
            )

    def test_registered_in_eu_ai_database_before_market_placement(
        self, high_risk_ai_scope, entity_profile: dict
    ):
        """Art. 49: High-risk AI systems must be registered in the EU AI Act database
        before being placed on the market."""
        for ai_system in entity_profile.get("high_risk_ai_systems", []):
            assert ai_system.get("eu_database_registered") is True, (
                f"High-risk AI system '{ai_system.get('id', 'unknown')}' not registered "
                f"in EU AI Act database — Art. 49 requires registration before market placement"
            )

    def test_risk_management_system_implemented(self, high_risk_ai_scope, entity_profile: dict):
        """Art. 9: Continuous risk management system required for high-risk AI throughout lifecycle."""
        for ai_system in entity_profile.get("high_risk_ai_systems", []):
            assert ai_system.get("risk_management_system_documented") is True, (
                f"High-risk AI system '{ai_system.get('id', 'unknown')}' has no risk "
                f"management system — Art. 9 EU AI Act"
            )

    @pytest.mark.assumption(
        id="ASSUME-EUAI-HIGHRISK-001",
        text="Human oversight measures are implemented in a manner appropriate to the AI "
             "system's specific deployment context; the technical and operational means "
             "for human oversight (Art. 14) are accepted as documented in the technical "
             "documentation rather than prescribing specific interface requirements.",
        confidence="PARAMETERIZED",
        approved_by=None,
    )
    def test_human_oversight_measures_implemented(
        self, high_risk_ai_scope, entity_profile: dict
    ):
        """Art. 14: High-risk AI system must have human oversight measures enabling
        humans to understand, monitor, and intervene."""
        for ai_system in entity_profile.get("high_risk_ai_systems", []):
            assert ai_system.get("human_oversight_measures_documented") is True, (
                f"High-risk AI system '{ai_system.get('id', 'unknown')}' lacks documented "
                f"human oversight measures — Art. 14 EU AI Act"
            )
```

---

## TestSeriousIncidentReporting

```python
class TestSeriousIncidentReporting:
    """Art. 73 — Serious incident reporting: DETERMINISTIC deadlines."""

    def test_death_or_serious_harm_incident_reported_within_15_days(self, entity_profile: dict):
        """Art. 73(3): Serious incidents resulting in death or serious harm to health
        must be reported to the national competent authority within 15 calendar days
        of the provider becoming aware."""
        for incident in entity_profile.get("ai_serious_incidents", []):
            if incident.get("severity") not in ("death", "serious_harm_to_health"):
                continue
            awareness_date = incident.get("provider_awareness_date")
            report_date = incident.get("national_authority_report_date")
            if awareness_date:
                assert report_date is not None, (
                    f"Serious AI incident '{incident.get('id', 'unknown')}' (death/serious harm) "
                    f"not reported to national authority — Art. 73(3)"
                )
                days_elapsed = (report_date - awareness_date).days
                assert days_elapsed <= AI_ACT_SERIOUS_INCIDENT_DEATH_SERIOUS_HARM_DAYS, (
                    f"Serious AI incident report '{incident.get('id', 'unknown')}' filed "
                    f"{days_elapsed} days after awareness — must be within "
                    f"{AI_ACT_SERIOUS_INCIDENT_DEATH_SERIOUS_HARM_DAYS} days (Art. 73(3))"
                )

    def test_other_serious_incident_reported_within_3_months(self, entity_profile: dict):
        """Art. 73: Other serious incidents (not death/serious harm) must be reported
        within 3 months of the provider becoming aware."""
        from dateutil.relativedelta import relativedelta
        for incident in entity_profile.get("ai_serious_incidents", []):
            if incident.get("severity") in ("death", "serious_harm_to_health"):
                continue
            awareness_date = incident.get("provider_awareness_date")
            report_date = incident.get("national_authority_report_date")
            if awareness_date:
                assert report_date is not None, (
                    f"Serious AI incident '{incident.get('id', 'unknown')}' not reported — Art. 73"
                )
                deadline = awareness_date + relativedelta(months=AI_ACT_SERIOUS_INCIDENT_OTHER_MONTHS)
                assert report_date <= deadline, (
                    f"Serious AI incident '{incident.get('id', 'unknown')}' reported {report_date}, "
                    f"after the 3-month deadline {deadline} — Art. 73"
                )
```

---

## TestGPAIObligations

```python
class TestGPAIObligations:
    """Art. 51–56 — General-Purpose AI model obligations."""

    def test_gpai_technical_documentation_maintained(self, gpai_scope, entity_profile: dict):
        """Art. 53(1)(a): GPAI model providers must draw up and keep up-to-date technical
        documentation for the model."""
        for model in entity_profile.get("gpai_models", []):
            assert model.get("technical_documentation_current") is True, (
                f"GPAI model '{model.get('id', 'unknown')}' lacks current technical "
                f"documentation — Art. 53(1)(a)"
            )

    def test_gpai_copyright_compliance_documented(self, gpai_scope, entity_profile: dict):
        """Art. 53(1)(c): GPAI providers must make publicly available a sufficiently detailed
        summary of the training data used (copyright compliance documentation)."""
        for model in entity_profile.get("gpai_models", []):
            assert model.get("training_data_summary_published") is True, (
                f"GPAI model '{model.get('id', 'unknown')}' training data summary not "
                f"published — Art. 53(1)(c)"
            )

    def test_systemic_risk_model_correctly_identified(
        self, systemic_risk_gpai_scope, entity_profile: dict
    ):
        """Art. 51: GPAI models trained with > 10^25 FLOPs presumed to have systemic risk."""
        for model in entity_profile.get("gpai_models", []):
            training_flops = model.get("training_compute_flops")
            if training_flops and Decimal(str(training_flops)) > GPAI_SYSTEMIC_RISK_FLOPS_THRESHOLD:
                assert model.get("systemic_risk_designated") is True, (
                    f"GPAI model '{model.get('id', 'unknown')}' trained with {training_flops:.2e} "
                    f"FLOPs (> 10^25) must be designated as systemic-risk — Art. 51"
                )

    def test_systemic_risk_gpai_adversarial_testing_conducted(
        self, systemic_risk_gpai_scope, entity_profile: dict
    ):
        """Art. 55(1)(a): Systemic-risk GPAI providers must perform adversarial testing
        (red-teaming) of the model."""
        for model in entity_profile.get("gpai_models", []):
            if model.get("systemic_risk_designated") is True:
                assert model.get("adversarial_testing_conducted") is True, (
                    f"Systemic-risk GPAI model '{model.get('id', 'unknown')}' adversarial "
                    f"testing not conducted — Art. 55(1)(a)"
                )

    def test_systemic_risk_gpai_incident_reporting_to_ai_office(
        self, systemic_risk_gpai_scope, entity_profile: dict
    ):
        """Art. 55(1)(c): Systemic-risk GPAI providers must report serious incidents
        to the AI Office without undue delay."""
        for incident in entity_profile.get("gpai_serious_incidents", []):
            assert incident.get("reported_to_ai_office") is True, (
                f"Systemic-risk GPAI incident '{incident.get('id', 'unknown')}' not reported "
                f"to AI Office — Art. 55(1)(c)"
            )

    @pytest.mark.human_review_required(
        id="CONTEST-EUAI-HIGHRISK-001",
        question="High-risk classification under Art. 6 + Annex III: whether a specific "
                 "AI application falls within an Annex III domain requires legal/technical "
                 "judgment on the system's actual function and primary purpose.",
        confidence="CONTESTED",
    )
    def test_high_risk_classification_reviewed(self, entity_profile: dict):
        """Art. 6 + Annex III: High-risk classification requires case-by-case assessment
        of the AI system's function within listed domains."""
        for ai_system in entity_profile.get("ai_systems", []):
            if ai_system.get("high_risk_classification_performed") is not True:
                assert False, (
                    f"AI system '{ai_system.get('id', 'unknown')}' has no documented "
                    f"high-risk classification assessment — Art. 6 requires providers "
                    f"to assess whether their system falls under Annex I or Annex III"
                )
```
