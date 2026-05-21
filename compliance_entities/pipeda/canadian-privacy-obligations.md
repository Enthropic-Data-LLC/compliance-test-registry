# PIPEDA / Quebec Law 25 — Canadian Privacy Obligations

**Framework:** PIPEDA (S.C. 2000, c. 5) + Quebec Law 25 (Act respecting the protection of personal information in the private sector, as amended)
**Clauses:** PIPEDA Schedule 1 Principles 1–10 (Fair Information Principles), §10.1 (breach of security safeguards); Quebec Law 25 §§3.2, 12, 25, 63.3, 63.5–63.6 (PIA, privacy by default, breach, portability, de-indexing)
**Confidence:** DETERMINISTIC-dominant (privacy officer designation, breach records, access response deadlines, Law 25 PIA obligation, breach notification timelines); PARAMETERIZED (consent adequacy, safeguards appropriateness); CONTESTED (RROSH determination)
**Last parsed:** 2026-05-21

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def pipeda_scope(entity_profile: dict):
    if not entity_profile.get("pipeda_in_scope", False):
        pytest.skip("PIPEDA not in scope")
```

---

## Constants

```python
from datetime import date, timedelta

# PIPEDA access request response deadline
PIPEDA_ACCESS_REQUEST_MAX_DAYS = 30
PIPEDA_ACCESS_REQUEST_EXTENSION_MAX_DAYS = 30  # with written notice to individual

# Breach records retention (PIPEDA Breach of Security Safeguards Regulations)
PIPEDA_BREACH_RECORD_RETENTION_MONTHS = 24

# Quebec Law 25 breach notification deadline
QUEBEC_LAW25_BREACH_NOTIFICATION_HOURS = 72  # "without delay" interpreted as 72h in practice

# Privacy officer — named person or role responsible for PIPEDA compliance
```

---

## Privacy Officer (Principle 1 — Accountability)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestPrivacyOfficer:
    """PIPEDA Schedule 1 P1 — Designated privacy officer accountable for organization's PIPEDA compliance."""

    def test_privacy_officer_designated(self, controls_evidence: dict):
        pipeda = controls_evidence.get("pipeda", {})
        assert pipeda.get("privacy_officer_designated", False), (
            "An individual must be designated as accountable for the organization's "
            "compliance with PIPEDA — typically a Chief Privacy Officer or Privacy "
            "Officer role (PIPEDA Schedule 1, Principle 1)"
        )

    def test_privacy_policies_and_procedures_implemented(
        self, controls_evidence: dict
    ):
        pipeda = controls_evidence.get("pipeda", {})
        assert pipeda.get("privacy_policies_implemented", False), (
            "The organization must implement policies and practices to give effect to "
            "PIPEDA's principles, including procedures for complaints, training, and "
            "third-party contracts (PIPEDA Schedule 1, Principle 1)"
        )
```

---

## Purpose Identification and Limitation (Principles 2, 5)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestPurposeSpecification:
    """PIPEDA Schedule 1 P2 — Purposes identified before or at collection; P5 — used only for identified purposes."""

    def test_purposes_identified_before_or_at_collection(
        self, controls_evidence: dict
    ):
        pipeda = controls_evidence.get("pipeda", {})
        assert pipeda.get("purposes_documented_for_all_pi_categories", False), (
            "The purposes for which personal information is collected must be "
            "identified before or at the time of collection "
            "(PIPEDA Schedule 1, Principle 2)"
        )

    def test_pi_not_used_for_purposes_beyond_original(
        self, controls_evidence: dict
    ):
        data_uses = controls_evidence.get("pipeda_data_uses", [])
        beyond_purpose = [
            u for u in data_uses
            if not u.get("within_identified_purposes", False)
            and not u.get("new_consent_obtained", False)
        ]
        assert not beyond_purpose, (
            f"Personal information must not be used for purposes beyond those for "
            f"which it was collected, without obtaining new consent "
            f"(PIPEDA Schedule 1, Principle 5). Violations: "
            f"{[u['use_id'] for u in beyond_purpose]}"
        )
```

---

## Consent (Principle 3)

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestConsent:
    """PIPEDA Schedule 1 P3 — Meaningful consent obtained; implied consent only for non-sensitive; explicit for sensitive."""

    @pytest.mark.assumption(
        id="ASSUME-PIPEDA-CONSENT-001",
        description=(
            "Consent adequacy under PIPEDA is context-dependent: express consent "
            "required for sensitive information and for unexpected uses; implied consent "
            "may be sufficient for non-sensitive information in straightforward commercial "
            "contexts; OPC guidance on meaningful consent (2018) requires plain language, "
            "not buried in terms; adequacy of consent mechanism is PARAMETERIZED — "
            "documented consent mechanism existence is DETERMINISTIC"
        ),
        approved_by="privacy_officer",
        review_date="2027-05-21",
    )
    def test_consent_mechanism_documented_for_each_pi_category(
        self, controls_evidence: dict
    ):
        pipeda = controls_evidence.get("pipeda", {})
        assert pipeda.get("consent_mechanism_documented_per_pi_category", False), (
            "The consent mechanism used for each category of personal information "
            "must be documented — express vs. implied and the rationale "
            "(PIPEDA Schedule 1, Principle 3)"
        )

    def test_sensitive_pi_obtains_express_consent(self, controls_evidence: dict):
        pipeda = controls_evidence.get("pipeda", {})
        if not pipeda.get("sensitive_pi_collected", False):
            return
        assert pipeda.get("express_consent_for_sensitive_pi", False), (
            "Sensitive personal information (financial, medical, health, etc.) "
            "requires explicit (express) consent — implied consent is not sufficient "
            "(PIPEDA Schedule 1, Principle 3 + OPC guidance)"
        )
```

---

## Breach Records (PIPEDA §10.1 + Breach Regulations)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestBreachRecords:
    """PIPEDA §10.1 — Every security breach recorded regardless of RROSH; records retained 24 months; available to OPC."""

    def test_breach_log_maintained_for_all_breaches(self, controls_evidence: dict):
        pipeda = controls_evidence.get("pipeda", {})
        assert pipeda.get("breach_log_maintained", False), (
            "A record of every breach of security safeguards must be maintained, "
            "regardless of whether the breach creates a real risk of significant harm "
            "(PIPEDA §10.1 + Breach Regulations §9)"
        )

    def test_breach_records_retained_24_months(self, controls_evidence: dict):
        breach_records = controls_evidence.get("pipeda_breach_records", [])
        for record in breach_records:
            retention_months = record.get("retention_months")
            if retention_months is not None:
                assert retention_months >= PIPEDA_BREACH_RECORD_RETENTION_MONTHS, (
                    f"Breach record '{record['breach_id']}' must be retained for a minimum "
                    f"of {PIPEDA_BREACH_RECORD_RETENTION_MONTHS} months from the date of "
                    f"breach. Configured: {retention_months} months "
                    f"(PIPEDA Breach Regulations §9)"
                )

    def test_breach_records_available_to_opc_on_request(self, controls_evidence: dict):
        pipeda = controls_evidence.get("pipeda", {})
        assert pipeda.get("breach_records_accessible_to_opc", False), (
            "Breach records must be provided to the OPC on request "
            "(PIPEDA §10.1 + Breach Regulations §9)"
        )
```

---

## Breach Notification — RROSH Trigger (PIPEDA §10.1)

**Overall: PARAMETERIZED (trigger) + DETERMINISTIC (notification obligation once triggered)**

```python
class TestBreachNotification:
    """PIPEDA §10.1 — Breaches with RROSH reported to OPC and individuals 'as soon as feasible'."""

    @pytest.mark.assumption(
        id="ASSUME-PIPEDA-RROSH-001",
        description=(
            "The 'real risk of significant harm' (RROSH) determination is a contextual "
            "analysis considering: sensitivity of PI, probability of misuse, whether the "
            "breach involved a malicious actor; the OPC provides a RROSH assessment tool; "
            "adequacy of RROSH assessment is PARAMETERIZED — documented RROSH analysis "
            "for each material breach is DETERMINISTIC"
        ),
        approved_by="privacy_officer",
        review_date="2027-05-21",
    )
    def test_rrosh_assessment_conducted_for_all_material_breaches(
        self, controls_evidence: dict
    ):
        breaches = controls_evidence.get("pipeda_breach_records", [])
        no_rrosh_assessment = [
            b for b in breaches
            if not b.get("rrosh_assessment_conducted", False)
        ]
        assert not no_rrosh_assessment, (
            f"A real risk of significant harm (RROSH) assessment must be conducted "
            f"and documented for each breach of security safeguards "
            f"(PIPEDA §10.1). Missing assessment: "
            f"{[b['breach_id'] for b in no_rrosh_assessment]}"
        )

    def test_opc_notified_for_rrosh_breaches_as_soon_as_feasible(
        self, controls_evidence: dict
    ):
        breaches = controls_evidence.get("pipeda_breach_records", [])
        rrosh_breaches = [b for b in breaches if b.get("rrosh_determined", False)]
        not_reported = [
            b for b in rrosh_breaches
            if not b.get("opc_notified", False)
        ]
        assert not_reported == [], (
            f"Breaches with RROSH must be reported to the OPC 'as soon as feasible' "
            f"(PIPEDA §10.1). Not reported: "
            f"{[b['breach_id'] for b in not_reported]}"
        )

    def test_individuals_notified_for_rrosh_breaches(self, controls_evidence: dict):
        breaches = controls_evidence.get("pipeda_breach_records", [])
        rrosh_breaches = [b for b in breaches if b.get("rrosh_determined", False)]
        not_notified = [
            b for b in rrosh_breaches
            if not b.get("individuals_notified", False)
        ]
        assert not_notified == [], (
            f"Affected individuals must be notified of breaches with RROSH "
            f"'as soon as feasible' (PIPEDA §10.1). Not notified: "
            f"{[b['breach_id'] for b in not_notified]}"
        )
```

---

## Individual Access Rights (Principle 9)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestIndividualAccessRights:
    """PIPEDA Schedule 1 P9 — Access requests responded to within 30 days; correction rights provided."""

    def test_access_requests_responded_to_within_30_days(
        self, controls_evidence: dict, reference_date: date
    ):
        from datetime import timedelta
        access_requests = controls_evidence.get("pipeda_access_requests", [])
        for request in access_requests:
            request_date = request.get("request_date")
            response_date = request.get("response_date")
            extended = request.get("extension_notified", False)
            if request_date is None or response_date is None:
                continue
            max_days = PIPEDA_ACCESS_REQUEST_MAX_DAYS
            if extended:
                max_days += PIPEDA_ACCESS_REQUEST_EXTENSION_MAX_DAYS
            delta = (response_date - request_date).days
            assert delta <= max_days, (
                f"Access request '{request['request_id']}' responded to in {delta} days, "
                f"exceeding the {max_days}-day limit "
                f"(PIPEDA Schedule 1, Principle 9)"
            )

    def test_correction_right_implemented(self, controls_evidence: dict):
        pipeda = controls_evidence.get("pipeda", {})
        assert pipeda.get("correction_right_mechanism_in_place", False), (
            "Individuals must be able to challenge the accuracy and completeness of "
            "their personal information and have it corrected "
            "(PIPEDA Schedule 1, Principle 9)"
        )
```

---

## Quebec Law 25 — Additional Requirements

**Overall: DETERMINISTIC — Pattern 1 (when Quebec scope applies)**

```python
class TestQuebecLaw25:
    """Quebec Law 25 — PIA for technology projects; privacy by default; 72-hour breach notification; privacy officer published."""

    @pytest.fixture(autouse=True)
    def quebec_scope(self, entity_profile: dict):
        if not entity_profile.get("quebec_law25_in_scope", False):
            pytest.skip("Quebec Law 25 not in scope")

    def test_privacy_impact_assessment_conducted_for_technology_projects(
        self, controls_evidence: dict
    ):
        technology_projects = controls_evidence.get("law25_technology_projects", [])
        no_pia = [
            p for p in technology_projects
            if not p.get("privacy_impact_assessment_completed_before_launch", False)
        ]
        assert not no_pia, (
            f"A Privacy Impact Assessment (PIA) must be conducted before any "
            f"technology project involving personal information is completed "
            f"(Quebec Law 25 §3.3). Missing PIA: "
            f"{[p['project_id'] for p in no_pia]}"
        )

    def test_privacy_by_default_implemented_for_new_products_and_services(
        self, controls_evidence: dict
    ):
        law25 = controls_evidence.get("law25", {})
        assert law25.get("privacy_by_default_implemented", False), (
            "Privacy by default must be implemented — only PI necessary for the "
            "purposes must be collected, and only kept for the minimum time required "
            "(Quebec Law 25 §9)"
        )

    def test_cai_notified_within_72_hours_of_confidentiality_incident(
        self, controls_evidence: dict
    ):
        incidents = controls_evidence.get("law25_confidentiality_incidents", [])
        for incident in incidents:
            if not incident.get("serious_risk_of_injury", False):
                continue
            notification_hours = incident.get("cai_notification_hours")
            if notification_hours is not None:
                assert notification_hours <= QUEBEC_LAW25_BREACH_NOTIFICATION_HOURS, (
                    f"Confidentiality incident '{incident['incident_id']}' notified to "
                    f"Commission d'accès à l'information (CAI) in {notification_hours}h, "
                    f"exceeding the {QUEBEC_LAW25_BREACH_NOTIFICATION_HOURS}h requirement "
                    f"(Quebec Law 25 §3.5)"
                )

    def test_privacy_officer_name_published_on_website(self, controls_evidence: dict):
        law25 = controls_evidence.get("law25", {})
        assert law25.get("privacy_officer_name_published_on_website", False), (
            "The name and contact information of the person responsible for the "
            "protection of personal information must be published on the organization's "
            "website (Quebec Law 25 §3.2)"
        )

    def test_explicit_consent_obtained_for_sensitive_personal_information(
        self, controls_evidence: dict
    ):
        law25 = controls_evidence.get("law25", {})
        if not law25.get("sensitive_pi_collected", False):
            return
        assert law25.get("explicit_consent_for_sensitive_pi", False), (
            "Explicit (separate, distinct) consent must be obtained for the collection "
            "of sensitive personal information under Quebec Law 25"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-PIPEDA-CONSENT-001 | P3 | Consent mechanism adequacy: PARAMETERIZED (contextual analysis); documented consent mechanism per PI category: DETERMINISTIC | 2027-05-21 |
| ASSUME-PIPEDA-RROSH-001 | §10.1 | RROSH determination: PARAMETERIZED (multi-factor contextual analysis); documented RROSH assessment for each breach: DETERMINISTIC | 2027-05-21 |
