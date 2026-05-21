# PSD2 — Strong Customer Authentication and Open Banking

**Framework:** Directive (EU) 2015/2366 (PSD2) + Commission Delegated Regulation (EU) 2018/389 (RTS on SCA and CSC)
**Clauses:** Art. 4 RTS (SCA minimum factors); Art. 5 RTS (authentication code dynamic linking to amount and payee); Art. 9 RTS (independence of factors); Art. 10–18 RTS (SCA exemptions — low-value contactless, low-value remote, TRA fraud rate gates); Art. 32 RTS (ASPSP dedicated API / 99.5% uptime); Art. 96 PSD2 (incident reporting — 72-hour intermediate report)
**Confidence:** DETERMINISTIC-dominant (SCA 2-factor minimum, dynamic linking requirement, low-value thresholds, TRA fraud rate gates, API 99.5% uptime, 72-hour intermediate report); PARAMETERIZED (factor independence implementation, exemption eligibility logic, consent duration, major incident classification)
**Last parsed:** 2026-05-21

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def psd2_scope(entity_profile: dict):
    if not entity_profile.get("eu_eea_payment_service_provider", False):
        pytest.skip("PSD2 not applicable — not a licensed payment service provider in the EU/EEA")

@pytest.fixture
def aspsp_scope(entity_profile: dict):
    """Additional fixture for ASPSP-only requirements (open banking API)."""
    if not entity_profile.get("aspsp_account_servicing_payment_service_provider", False):
        pytest.skip("ASPSP-only requirement — entity is not an account-servicing PSP")
```

---

## Constants

```python
from decimal import Decimal

# SCA requirements
PSD2_SCA_MIN_FACTORS = 2

# Low-value contactless (POS) exemption thresholds — Art. 10 RTS
PSD2_LOW_VALUE_CONTACTLESS_PER_TRANSACTION_EUR = Decimal("50")
PSD2_LOW_VALUE_CONTACTLESS_CUMULATIVE_EUR = Decimal("150")
PSD2_LOW_VALUE_CONTACTLESS_CONSECUTIVE_LIMIT = 5

# Low-value remote electronic payment exemption thresholds — Art. 16 RTS
PSD2_LOW_VALUE_REMOTE_PER_TRANSACTION_EUR = Decimal("30")
PSD2_LOW_VALUE_REMOTE_CUMULATIVE_EUR = Decimal("100")
PSD2_LOW_VALUE_REMOTE_CONSECUTIVE_LIMIT = 5

# TRA exemption fraud rate thresholds — Art. 18 RTS
PSD2_TRA_EXEMPTION_100_EUR_MAX_FRAUD_RATE_PCT = Decimal("0.13")
PSD2_TRA_EXEMPTION_250_EUR_MAX_FRAUD_RATE_PCT = Decimal("0.06")
PSD2_TRA_EXEMPTION_500_EUR_MAX_FRAUD_RATE_PCT = Decimal("0.01")

# ASPSP API availability
PSD2_API_MINIMUM_UPTIME_PCT = Decimal("99.5")

# Incident reporting
PSD2_INCIDENT_INTERMEDIATE_REPORT_HOURS = 72
PSD2_INCIDENT_FINAL_REPORT_DAYS = 30

# Valid SCA factor categories
PSD2_SCA_FACTOR_CATEGORIES = frozenset({
    "knowledge",    # PIN, password, passphrase
    "possession",   # Hardware token, mobile device, smart card
    "inherence",    # Fingerprint, face, voice, retina
})
```

---

## Strong Customer Authentication — Factor Requirements (Art. 4–9 RTS)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestSCAFactors:
    """Art. 4–9 RTS — SCA requires at least 2 factors from distinct categories; factors must be independent."""

    def test_sca_uses_minimum_two_factors(self, controls_evidence: dict):
        psd2 = controls_evidence.get("psd2", {})
        factor_count = len(set(psd2.get("sca_factor_categories_in_use", [])))
        assert factor_count >= PSD2_SCA_MIN_FACTORS, (
            f"Strong Customer Authentication must use at least {PSD2_SCA_MIN_FACTORS} "
            f"factors from distinct categories (knowledge / possession / inherence). "
            f"Current distinct categories in use: {factor_count} "
            f"(Art. 4 RTS on SCA and CSC)"
        )

    def test_sca_factors_drawn_from_distinct_categories(self, controls_evidence: dict):
        psd2 = controls_evidence.get("psd2", {})
        categories = set(psd2.get("sca_factor_categories_in_use", []))
        invalid = categories - PSD2_SCA_FACTOR_CATEGORIES
        assert not invalid, (
            f"SCA factor categories must be from the defined set "
            f"{PSD2_SCA_FACTOR_CATEGORIES}. "
            f"Unrecognized categories: {invalid} "
            f"(Art. 4 RTS on SCA and CSC)"
        )

    def test_sca_factors_are_independent(self, controls_evidence: dict):
        psd2 = controls_evidence.get("psd2", {})
        assert psd2.get("sca_factors_independence_assessed", False), (
            "SCA factors must be independent — compromise of one factor must not "
            "compromise the other. Independence assessment must be documented "
            "(Art. 9 RTS on SCA and CSC)"
        )

    def test_sca_implemented_for_all_payer_initiated_electronic_payments(
        self, controls_evidence: dict
    ):
        psd2 = controls_evidence.get("psd2", {})
        assert psd2.get("sca_applied_to_all_payer_initiated_payments_unless_exempt", False), (
            "SCA must be applied to all electronic payment transactions initiated "
            "by the payer, unless a specific RTS exemption applies — "
            "blanket SCA bypass without documented exemption is a violation "
            "(Art. 97 PSD2)"
        )
```

---

## Dynamic Linking of Authentication Code (Art. 5 RTS)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestDynamicLinking:
    """Art. 5 RTS — For payment transactions, authentication code must be dynamically linked to specific amount and payee."""

    def test_authentication_code_linked_to_transaction_amount(
        self, controls_evidence: dict
    ):
        psd2 = controls_evidence.get("psd2", {})
        assert psd2.get("authentication_code_dynamically_linked_to_amount", False), (
            "The authentication code for a payment transaction must be dynamically "
            "linked to the specific transaction amount — a generic code that does "
            "not bind the amount is not compliant "
            "(Art. 5(1) RTS on SCA and CSC)"
        )

    def test_authentication_code_linked_to_payee(self, controls_evidence: dict):
        psd2 = controls_evidence.get("psd2", {})
        assert psd2.get("authentication_code_dynamically_linked_to_payee", False), (
            "The authentication code for a payment transaction must be dynamically "
            "linked to the specific payee — a code that does not bind the payee "
            "does not satisfy dynamic linking requirements "
            "(Art. 5(1) RTS on SCA and CSC)"
        )

    def test_altering_amount_or_payee_invalidates_authentication_code(
        self, controls_evidence: dict
    ):
        psd2 = controls_evidence.get("psd2", {})
        assert psd2.get(
            "amount_or_payee_alteration_invalidates_authentication_code", False
        ), (
            "Any alteration of the transaction amount or payee after authentication "
            "code generation must invalidate that code — this is a DETERMINISTIC "
            "technical requirement to prevent man-in-the-browser attacks "
            "(Art. 5(2) RTS on SCA and CSC)"
        )

    def test_transaction_amount_and_payee_displayed_to_payer_before_authentication(
        self, controls_evidence: dict
    ):
        psd2 = controls_evidence.get("psd2", {})
        assert psd2.get(
            "transaction_amount_and_payee_displayed_before_sca_completion", False
        ), (
            "The payer must be shown the transaction amount and payee before "
            "completing SCA — display must be on the authentication device "
            "(Art. 5(3) RTS on SCA and CSC)"
        )
```

---

## Low-Value SCA Exemptions (Art. 10, Art. 16 RTS)

**Overall: DETERMINISTIC thresholds — Pattern 1**

```python
class TestLowValueExemptions:
    """Art. 10 + Art. 16 RTS — Low-value exemptions require per-transaction AND cumulative/consecutive limits not exceeded."""

    def test_contactless_pos_exemption_per_transaction_limit_enforced(
        self, controls_evidence: dict
    ):
        transactions = controls_evidence.get("psd2_contactless_exempt_transactions", [])
        over_limit = [
            t for t in transactions
            if Decimal(str(t.get("amount_eur", 0))) >= PSD2_LOW_VALUE_CONTACTLESS_PER_TRANSACTION_EUR
        ]
        assert not over_limit, (
            f"Contactless POS SCA exemption may only be applied to transactions "
            f"below {PSD2_LOW_VALUE_CONTACTLESS_PER_TRANSACTION_EUR} EUR. "
            f"Over-limit: {[t['transaction_id'] for t in over_limit]} "
            f"(Art. 10(1) RTS on SCA and CSC)"
        )

    def test_contactless_pos_exemption_cumulative_cap_enforced(
        self, controls_evidence: dict
    ):
        sessions = controls_evidence.get("psd2_contactless_exempt_sessions", [])
        over_cumulative = [
            s for s in sessions
            if Decimal(str(s.get("cumulative_eur_since_last_sca", 0))) > PSD2_LOW_VALUE_CONTACTLESS_CUMULATIVE_EUR
        ]
        assert not over_cumulative, (
            f"Contactless POS exemption must be reset when cumulative amount since "
            f"last SCA exceeds {PSD2_LOW_VALUE_CONTACTLESS_CUMULATIVE_EUR} EUR or "
            f"{PSD2_LOW_VALUE_CONTACTLESS_CONSECUTIVE_LIMIT} consecutive exempt transactions. "
            f"Cumulative cap exceeded in sessions: {[s['session_id'] for s in over_cumulative]} "
            f"(Art. 10(2) RTS on SCA and CSC)"
        )

    def test_low_value_remote_exemption_per_transaction_limit_enforced(
        self, controls_evidence: dict
    ):
        transactions = controls_evidence.get("psd2_low_value_remote_exempt_transactions", [])
        over_limit = [
            t for t in transactions
            if Decimal(str(t.get("amount_eur", 0))) >= PSD2_LOW_VALUE_REMOTE_PER_TRANSACTION_EUR
        ]
        assert not over_limit, (
            f"Low-value remote payment SCA exemption may only be applied to "
            f"transactions below {PSD2_LOW_VALUE_REMOTE_PER_TRANSACTION_EUR} EUR. "
            f"Over-limit: {[t['transaction_id'] for t in over_limit]} "
            f"(Art. 16(1) RTS on SCA and CSC)"
        )

    def test_low_value_remote_exemption_cumulative_cap_enforced(
        self, controls_evidence: dict
    ):
        sessions = controls_evidence.get("psd2_low_value_remote_sessions", [])
        over_cumulative = [
            s for s in sessions
            if Decimal(str(s.get("cumulative_eur_since_last_sca", 0))) > PSD2_LOW_VALUE_REMOTE_CUMULATIVE_EUR
        ]
        assert not over_cumulative, (
            f"Low-value remote exemption must be reset when cumulative amount since "
            f"last SCA exceeds {PSD2_LOW_VALUE_REMOTE_CUMULATIVE_EUR} EUR or "
            f"{PSD2_LOW_VALUE_REMOTE_CONSECUTIVE_LIMIT} consecutive exempt transactions. "
            f"Cumulative cap exceeded in sessions: {[s['session_id'] for s in over_cumulative]} "
            f"(Art. 16(2) RTS on SCA and CSC)"
        )
```

---

## Transaction Risk Analysis (TRA) Exemption (Art. 18 RTS)

**Overall: DETERMINISTIC fraud rate gates — Pattern 1**

```python
class TestTransactionRiskAnalysis:
    """Art. 18 RTS — TRA exemption requires PSP fraud rate at or below published thresholds by exemption tier."""

    def test_tra_exemption_for_100_eur_requires_fraud_rate_at_or_below_013_pct(
        self, controls_evidence: dict
    ):
        psd2 = controls_evidence.get("psd2", {})
        if not psd2.get("tra_exemption_applied_for_100_eur_tier", False):
            return
        fraud_rate = psd2.get("psp_fraud_rate_pct_current_quarter")
        if fraud_rate is None:
            return
        assert Decimal(str(fraud_rate)) <= PSD2_TRA_EXEMPTION_100_EUR_MAX_FRAUD_RATE_PCT, (
            f"TRA exemption for transactions up to €100 requires PSP fraud rate "
            f"≤ {PSD2_TRA_EXEMPTION_100_EUR_MAX_FRAUD_RATE_PCT}%. "
            f"Current fraud rate: {fraud_rate}% — TRA exemption at this tier "
            f"must be suspended immediately "
            f"(Art. 18(1)(a) RTS on SCA and CSC)"
        )

    def test_tra_exemption_for_250_eur_requires_fraud_rate_at_or_below_006_pct(
        self, controls_evidence: dict
    ):
        psd2 = controls_evidence.get("psd2", {})
        if not psd2.get("tra_exemption_applied_for_250_eur_tier", False):
            return
        fraud_rate = psd2.get("psp_fraud_rate_pct_current_quarter")
        if fraud_rate is None:
            return
        assert Decimal(str(fraud_rate)) <= PSD2_TRA_EXEMPTION_250_EUR_MAX_FRAUD_RATE_PCT, (
            f"TRA exemption for transactions up to €250 requires PSP fraud rate "
            f"≤ {PSD2_TRA_EXEMPTION_250_EUR_MAX_FRAUD_RATE_PCT}%. "
            f"Current fraud rate: {fraud_rate}% — TRA exemption at this tier "
            f"must be suspended "
            f"(Art. 18(1)(b) RTS on SCA and CSC)"
        )

    def test_tra_exemption_for_500_eur_requires_fraud_rate_at_or_below_001_pct(
        self, controls_evidence: dict
    ):
        psd2 = controls_evidence.get("psd2", {})
        if not psd2.get("tra_exemption_applied_for_500_eur_tier", False):
            return
        fraud_rate = psd2.get("psp_fraud_rate_pct_current_quarter")
        if fraud_rate is None:
            return
        assert Decimal(str(fraud_rate)) <= PSD2_TRA_EXEMPTION_500_EUR_MAX_FRAUD_RATE_PCT, (
            f"TRA exemption for transactions up to €500 requires PSP fraud rate "
            f"≤ {PSD2_TRA_EXEMPTION_500_EUR_MAX_FRAUD_RATE_PCT}%. "
            f"Current fraud rate: {fraud_rate}% — TRA exemption at this tier "
            f"must be suspended "
            f"(Art. 18(1)(c) RTS on SCA and CSC)"
        )

    def test_tra_fraud_rate_calculated_per_rts_methodology(
        self, controls_evidence: dict
    ):
        psd2 = controls_evidence.get("psd2", {})
        if not psd2.get("tra_exemption_in_use", False):
            return
        assert psd2.get("tra_fraud_rate_calculated_per_rts_annex_methodology", False), (
            "PSP fraud rate for TRA exemption must be calculated per the RTS Annex "
            "methodology — value of unauthorized or fraudulent transactions / "
            "total value of transactions in the same category "
            "(Art. 18(2) RTS on SCA and CSC)"
        )
```

---

## ASPSP Open Banking API Requirements (Art. 30–33 RTS)

**Overall: DETERMINISTIC (API must exist, 99.5% uptime, testing environment) + PARAMETERIZED (obstacle-free access)**

```python
class TestASPSPOpenBankingAPI:
    """Art. 30–33 RTS — Dedicated interface for TPPs; 99.5% monthly uptime; testing facility available; no obstacles."""

    def test_dedicated_interface_or_fallback_provided(self, controls_evidence: dict, aspsp_scope):
        psd2 = controls_evidence.get("psd2", {})
        assert (
            psd2.get("dedicated_api_interface_provided", False)
            or psd2.get("modified_customer_interface_fallback_provided", False)
        ), (
            "ASPSPs must provide either a dedicated API interface for TPP access "
            "or, if the dedicated interface does not meet contingency requirements, "
            "a fallback via the modified customer interface "
            "(Art. 30 + Art. 33 RTS on SCA and CSC)"
        )

    def test_api_monthly_uptime_meets_99_5_percent_minimum(
        self, controls_evidence: dict, aspsp_scope
    ):
        api_months = controls_evidence.get("psd2_api_availability", [])
        below_sla = [
            m for m in api_months
            if Decimal(str(m.get("uptime_pct", 100))) < PSD2_API_MINIMUM_UPTIME_PCT
        ]
        assert not below_sla, (
            f"ASPSP dedicated interface must maintain at least "
            f"{PSD2_API_MINIMUM_UPTIME_PCT}% monthly uptime. "
            f"Below-SLA months: {[m['month'] for m in below_sla]} "
            f"(Art. 32(1) RTS on SCA and CSC)"
        )

    def test_tpp_testing_facility_available(self, controls_evidence: dict, aspsp_scope):
        psd2 = controls_evidence.get("psd2", {})
        assert psd2.get("tpp_testing_facility_available", False), (
            "ASPSPs must make a testing facility available to TPPs for testing "
            "connectivity and interface integration before go-live "
            "(Art. 30(5) RTS on SCA and CSC)"
        )

    def test_no_obstacles_imposed_on_tpps(self, controls_evidence: dict, aspsp_scope):
        psd2 = controls_evidence.get("psd2", {})
        assert not psd2.get("obstacles_identified_in_tpp_access", False), (
            "ASPSPs must not impose obstacles on AISPs or PISPs beyond what is "
            "required for SCA — additional authentication steps, redirects without "
            "functional equivalence, and data access restrictions are prohibited "
            "(Art. 32(3) RTS on SCA and CSC)"
        )
```

---

## Incident Reporting (Art. 96 PSD2)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestPSD2IncidentReporting:
    """Art. 96 PSD2 — Major incidents reported to NCA; intermediate report within 72 hours; final within 30 days."""

    def test_major_incident_classification_process_documented(
        self, controls_evidence: dict
    ):
        psd2 = controls_evidence.get("psd2", {})
        assert psd2.get("major_incident_classification_criteria_documented", False), (
            "A documented process for classifying operational or security incidents "
            "as 'major' must exist — criteria based on PSU count affected, "
            "transaction value disrupted, geographic scope, and duration "
            "(EBA Guidelines on major incident reporting under PSD2)"
        )

    def test_intermediate_report_submitted_within_72_hours(
        self, controls_evidence: dict
    ):
        incidents = controls_evidence.get("psd2_major_incidents", [])
        for incident in incidents:
            initial_notify_dt = incident.get("initial_notification_datetime")
            intermediate_report_dt = incident.get("intermediate_report_submitted_datetime")
            if initial_notify_dt is None or intermediate_report_dt is None:
                continue
            hours = (intermediate_report_dt - initial_notify_dt).total_seconds() / 3600
            assert hours <= PSD2_INCIDENT_INTERMEDIATE_REPORT_HOURS, (
                f"Intermediate incident report for '{incident['incident_id']}' submitted "
                f"{hours:.1f} hours after initial notification, exceeding the "
                f"{PSD2_INCIDENT_INTERMEDIATE_REPORT_HOURS}-hour deadline "
                f"(Art. 96(2) PSD2)"
            )

    def test_final_incident_report_submitted_within_30_days(
        self, controls_evidence: dict
    ):
        incidents = controls_evidence.get("psd2_major_incidents", [])
        for incident in incidents:
            if not incident.get("resolved", False):
                continue
            resolution_dt = incident.get("resolution_date")
            final_report_dt = incident.get("final_report_submitted_date")
            if resolution_dt is None or final_report_dt is None:
                continue
            days = (final_report_dt - resolution_dt).days
            assert days <= PSD2_INCIDENT_FINAL_REPORT_DAYS, (
                f"Final incident report for '{incident['incident_id']}' submitted "
                f"{days} days after resolution, exceeding the "
                f"{PSD2_INCIDENT_FINAL_REPORT_DAYS}-day deadline "
                f"(Art. 96(4) PSD2)"
            )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|

*(No open assumptions — SCA factor count, dynamic linking, TRA fraud rate gates, API uptime, and incident timelines are all DETERMINISTIC; exemption eligibility logic and factor independence implementation assessment are PARAMETERIZED but excluded from machine-testable assertions here)*
