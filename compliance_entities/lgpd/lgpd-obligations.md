# LGPD — Lei Geral de Proteção de Dados — Core Obligations
## Law No. 13,709/2018 (as amended); ANPD Resolutions

**Authority:** Autoridade Nacional de Proteção de Dados (ANPD)
**Effective:** September 2020 (general); August 2021 (penalty provisions)
**Scope:** Processing of personal data of individuals located in Brazil

---

## RDF extraction

### Data subject access right

```
Subject:    Any LGPD-covered controller
Condition:  Data subject submits a request to access their personal data
Obligation: Respond within 15 calendar days
Evidence:   Request intake log with receipt date; response record with date; data provided or denial reason
```

### Breach notification to ANPD

```
Subject:    Controller
Condition:  Security incident that may cause relevant harm to data subjects
Obligation: Notify ANPD within 3 business days of becoming aware
Evidence:   Incident awareness log; ANPD notification submission record with date
```

### DPO designation

```
Subject:    All controllers (Art. 41 — mandatory)
Condition:  Processing personal data of Brazilian individuals
Obligation: Designate a DPO and publish their name and contact information
Evidence:   DPO designation record; public-facing DPO contact publication
```

---

## Constants

```python
from datetime import date, timedelta

# Data subject rights — Art. 19
ACCESS_RESPONSE_DAYS      = 15   # LGPD Art. 19 — stricter than GDPR 30-day rule; no extension
CORRECTION_RESPONSE_DAYS  = 15   # Treated symmetrically with access (ASSUME-LGPD-ACCESS-001)

# Breach notification — Art. 48 + ANPD Resolution CD/ANPD/No. 15/2023
BREACH_ANPD_BUSINESS_DAYS = 3    # 3 business days from becoming aware (ASSUME-LGPD-BREACH-001)

# LGPD legal bases — Art. 7
LGPD_LEGAL_BASES = frozenset({
    "consent_7_i",
    "legal_obligation_7_ii",
    "public_policy_7_iii",
    "research_7_iv",
    "contract_performance_7_v",
    "regular_exercise_rights_7_vi",
    "vital_interests_7_viii",       # note: Art. 7 skips VII for general data
    "legitimate_interest_7_ix",
    "credit_protection_7_x",
    # Art. 7(VII) routes to Art. 11 for sensitive data health/sanitation
})

# Sensitive data categories — Art. 11 (stricter requirements; explicit consent or specific bases)
SENSITIVE_DATA_CATEGORIES = frozenset({
    "racial_ethnic_origin",
    "religious_belief",
    "political_opinion",
    "union_membership",
    "health_data",
    "sex_life",
    "genetic_data",
    "biometric_data",
    "childrens_data",               # Art. 14 — parental consent required
})

# Consent requirements — Art. 8
CONSENT_REQUIRED_ATTRIBUTES = frozenset({
    "explicit",
    "informed",
    "purpose_specific",
    "freely_given",
    "withdrawal_as_easy_as_giving",
})


def add_business_days_brazil(start: date, n: int) -> date:
    """Return date n Brazilian business days (Mon–Fri) after start.
    ASSUME-LGPD-BREACH-001: excludes weekends only (national holiday list
    should be maintained by compliance team and substituted for production use).
    """
    current = start
    count = 0
    while count < n:
        current += timedelta(days=1)
        if current.weekday() < 5:
            count += 1
    return current
```

---

## Scope pre-condition fixture

```python
import pytest

@pytest.fixture(autouse=True)
def lgpd_scope_check(entity_profile: dict):
    """Skip LGPD tests if entity does not process personal data in/of Brazil."""
    if not entity_profile.get("lgpd_in_scope", False):
        pytest.skip(
            "LGPD not in scope: entity does not process data in Brazil, "
            "offer goods/services to Brazilian individuals, or collect data in Brazil"
        )
```

---

## Legal Basis for Processing

### Legal basis documented for each processing activity (Pattern 1 — DETERMINISTIC)

```python
def test_legal_basis_documented_for_all_processing_activities(
    controls_evidence: dict,
):
    """
    Art. 7: Every processing activity must have a documented legal basis.
    Existence of documentation is DETERMINISTIC; adequacy of the chosen
    legal basis is PARAMETERIZED (except for consent and legitimate interest).
    """
    data_mapping = controls_evidence.get("lgpd_data_mapping", {})
    assert data_mapping, "No LGPD data mapping (records of processing) found in evidence"

    activities = data_mapping.get("processing_activities", [])
    assert activities, "Data mapping contains no processing activities"

    missing_basis = [
        a["activity_name"] for a in activities
        if not a.get("legal_basis") or a["legal_basis"] not in LGPD_LEGAL_BASES
    ]
    assert not missing_basis, (
        f"Processing activities with missing or invalid LGPD legal basis: {missing_basis}. "
        f"Valid bases: {LGPD_LEGAL_BASES}"
    )
```

### Consent requirements (Pattern 1 — DETERMINISTIC)

```python
def test_consent_meets_lgpd_requirements(
    controls_evidence: dict,
):
    """
    Art. 8: Consent must be explicit, informed, purpose-specific, freely given,
    and withdrawal must be as easy as giving consent. All five attributes required.
    """
    consent_mechanisms = controls_evidence.get("lgpd_consent_mechanisms", [])
    if not consent_mechanisms:
        pytest.skip("No consent-based processing identified — consent tests not applicable")

    violations = []
    for cm in consent_mechanisms:
        name = cm.get("name", "unnamed")
        missing_attrs = CONSENT_REQUIRED_ATTRIBUTES - frozenset(cm.get("attributes", []))
        if missing_attrs:
            violations.append(f"'{name}' missing: {missing_attrs}")

    assert not violations, (
        f"Consent mechanism(s) do not meet Art. 8 requirements: {'; '.join(violations)}"
    )


def test_consent_withdrawal_honored_and_data_deleted(
    controls_evidence: dict,
):
    """
    Art. 8(5): Withdrawal of consent must result in deletion of data processed
    on that basis, unless another legal basis exists. Withdrawal must be as
    easy as granting consent.
    """
    consent_mechanisms = controls_evidence.get("lgpd_consent_mechanisms", [])
    if not consent_mechanisms:
        pytest.skip("No consent-based processing identified")

    for cm in consent_mechanisms:
        assert cm.get("withdrawal_mechanism"), (
            f"Consent mechanism '{cm.get('name', 'unnamed')}' lacks a documented "
            "withdrawal mechanism (Art. 8(5) — withdrawal must be as easy as giving consent)"
        )
        assert cm.get("post_withdrawal_deletion_process"), (
            f"Consent mechanism '{cm.get('name', 'unnamed')}' lacks a post-withdrawal "
            "data deletion process"
        )
```

### Legitimate interest — balancing test (Pattern 3 — CONTESTED)

```python
@pytest.mark.human_review_required(
    reason=(
        "LGPD Art. 7(IX) + Art. 10: Legitimate interest requires a three-part balancing "
        "test — (1) controller's legitimate purpose, (2) necessity and suitability of "
        "processing, (3) data subject's fundamental rights/interests not overriding. "
        "ASSUME-LGPD-LI-001: a written Legitimate Interest Assessment (LIA) signed by "
        "the DPO is required for each processing activity relying on this basis. "
        "This is Pattern 3 — human DPO determination required."
    )
)
def test_legitimate_interest_processing_has_documented_lia(
    controls_evidence: dict,
):
    """
    For each processing activity using legitimate interest as the legal basis,
    a Legitimate Interest Assessment must be documented, signed by the DPO,
    and reviewed at least annually.
    """
    data_mapping = controls_evidence.get("lgpd_data_mapping", {})
    activities = data_mapping.get("processing_activities", []) if data_mapping else []

    li_activities = [
        a for a in activities
        if a.get("legal_basis") == "legitimate_interest_7_ix"
    ]
    if not li_activities:
        pytest.skip("No legitimate interest processing activities — LIA test not applicable")

    for activity in li_activities:
        lia = activity.get("legitimate_interest_assessment")
        assert lia, (
            f"Processing activity '{activity.get('activity_name', 'unnamed')}' uses "
            "legitimate interest but has no Legitimate Interest Assessment (LIA). "
            "Art. 10 requires documented balancing test."
        )
        assert lia.get("signed_by_dpo"), "LIA not signed by DPO"
        assert lia.get("last_review_date"), "LIA lacks a review date"
```

---

## Data Subject Rights

### 15-day access response deadline (Pattern 1 — DETERMINISTIC)

```python
def test_access_request_responded_within_15_days(
    controls_evidence: dict,
    reference_date: date,
):
    """
    Art. 19: Data subject requests for access must be responded to within 15
    calendar days. ASSUME-LGPD-ACCESS-001: no extension mechanism is provided
    in the LGPD (stricter than GDPR 30-day + 2-month extension). If the request
    cannot be fulfilled within 15 days, a partial response with a reason must
    be provided within the deadline.
    """
    dsr_log = controls_evidence.get("lgpd_dsr_log", [])
    if not dsr_log:
        pytest.skip("No DSR log found — access response test not applicable")

    access_requests = [r for r in dsr_log if r.get("request_type") == "access"]
    if not access_requests:
        pytest.skip("No access requests in DSR log")

    violations = []
    for req in access_requests:
        receipt_date = date.fromisoformat(str(req["receipt_date"]))
        deadline = receipt_date + timedelta(days=ACCESS_RESPONSE_DAYS)
        response_date = req.get("response_date")
        if response_date:
            response_date = date.fromisoformat(str(response_date))
            if response_date > deadline:
                violations.append({
                    "request_id": req.get("request_id", "unknown"),
                    "deadline": deadline,
                    "responded": response_date,
                    "overdue_days": (response_date - deadline).days,
                })
        elif reference_date > deadline and req.get("status") not in ("responded", "closed"):
            violations.append({
                "request_id": req.get("request_id", "unknown"),
                "deadline": deadline,
                "responded": None,
                "overdue_days": (reference_date - deadline).days,
            })

    assert not violations, (
        f"LGPD Art. 19: {len(violations)} access request(s) not responded to within "
        f"{ACCESS_RESPONSE_DAYS} calendar days: "
        + ", ".join(f"ID={v['request_id']} ({v['overdue_days']}d overdue)" for v in violations)
    )
```

### Consent withdrawal — deletion of data (Pattern 1 — DETERMINISTIC)

```python
def test_consent_withdrawal_triggers_data_deletion(
    controls_evidence: dict,
    reference_date: date,
):
    """
    Art. 15(I) + Art. 8(5): Upon withdrawal of consent, personal data processed
    on that basis must be deleted unless another legal basis applies.
    Deletion must happen without undue delay — treated as 15 days for consistency
    with the access request deadline (ASSUME-LGPD-ACCESS-001).
    """
    dsr_log = controls_evidence.get("lgpd_dsr_log", [])
    withdrawals = [r for r in dsr_log if r.get("request_type") == "consent_withdrawal"] if dsr_log else []
    if not withdrawals:
        pytest.skip("No consent withdrawal requests in DSR log")

    violations = []
    for req in withdrawals:
        receipt_date = date.fromisoformat(str(req["receipt_date"]))
        deadline = receipt_date + timedelta(days=ACCESS_RESPONSE_DAYS)
        deletion_confirmed = req.get("deletion_confirmed", False)
        alternative_basis = req.get("alternative_legal_basis")

        if alternative_basis:
            continue  # data retained under a different legal basis — acceptable

        if not deletion_confirmed and reference_date > deadline:
            violations.append(req.get("request_id", "unknown"))

    assert not violations, (
        f"Consent withdrawals without confirmed deletion (and no alternative legal basis): {violations}"
    )
```

---

## Sensitive Data (Art. 11)

### Sensitive data processing — explicit consent or specific legal basis (Pattern 1 — DETERMINISTIC)

```python
def test_sensitive_data_has_explicit_consent_or_specific_basis(
    controls_evidence: dict,
):
    """
    Art. 11: Sensitive personal data may only be processed with explicit consent
    or for specific listed purposes (public health, legal obligation, research,
    etc.). Generic consent or legitimate interest CANNOT justify sensitive data
    processing. DETERMINISTIC: each sensitive data category must be mapped to
    an Art. 11-specific legal basis.
    """
    data_mapping = controls_evidence.get("lgpd_data_mapping", {})
    activities = data_mapping.get("processing_activities", []) if data_mapping else []

    VALID_SENSITIVE_BASES = frozenset({
        "explicit_consent_art11_i",
        "legal_obligation_art11_ii_a",
        "shared_data_policy_art11_ii_b",
        "research_art11_ii_c",
        "regular_exercise_rights_art11_ii_d",
        "vital_interests_art11_ii_e",
        "health_sanitation_art11_ii_f",
        "fraud_prevention_art11_ii_g",
    })

    violations = []
    for activity in activities:
        sensitive_categories = frozenset(activity.get("sensitive_data_categories", []))
        if not sensitive_categories:
            continue
        basis = activity.get("sensitive_data_legal_basis")
        if not basis or basis not in VALID_SENSITIVE_BASES:
            violations.append({
                "activity": activity.get("activity_name", "unnamed"),
                "categories": list(sensitive_categories),
                "basis_found": basis,
            })

    assert not violations, (
        f"Sensitive data processing without valid Art. 11 legal basis: "
        + "; ".join(
            f"{v['activity']} (categories: {v['categories']}, basis: {v['basis_found']})"
            for v in violations
        )
    )
```

---

## Children's Data (Art. 14)

### Parental/guardian consent required for children under 18 (Pattern 1 — DETERMINISTIC)

```python
def test_childrens_data_requires_parental_consent(
    controls_evidence: dict,
    entity_profile: dict,
):
    """
    Art. 14: Processing of personal data of children (under 18 in Brazil) requires
    specific parental or legal guardian consent. This is a separate obligation from
    Art. 8 general consent.
    """
    if not entity_profile.get("processes_childrens_data_brazil", False):
        pytest.skip("Entity does not process children's data in Brazil — Art. 14 not applicable")

    childrens_processing = controls_evidence.get("lgpd_childrens_data", {})
    assert childrens_processing, "No children's data processing documentation found"
    assert childrens_processing.get("parental_consent_mechanism"), (
        "Art. 14: No parental/guardian consent mechanism documented for children's data"
    )
    assert childrens_processing.get("age_verification_method"), (
        "Art. 14: No age verification method documented to identify child data subjects"
    )
    assert childrens_processing.get("best_interests_assessment"), (
        "Art. 14(3): Processing must be in the best interests of the child — "
        "no best interests assessment found"
    )
```

---

## DPO Designation (Art. 41)

### DPO mandatory for all controllers (Pattern 1 — DETERMINISTIC)

```python
def test_dpo_designated_and_publicly_identified(
    controls_evidence: dict,
):
    """
    Art. 41: All controllers must designate a DPO (Encarregado de Dados).
    DPO name and contact information must be publicly disclosed.
    Unlike GDPR Art. 37 (which applies only to certain organizations), LGPD
    Art. 41 applies to ALL controllers.
    """
    dpo = controls_evidence.get("lgpd_dpo", {})
    assert dpo, "No DPO designation found. Art. 41 requires ALL controllers to designate a DPO."
    assert dpo.get("name"), "DPO record lacks a name"
    assert dpo.get("contact_email") or dpo.get("contact_channel"), (
        "DPO record lacks contact information. Art. 41 requires publicly disclosed contact."
    )
    assert dpo.get("publicly_published", False), (
        "DPO contact information must be publicly disclosed (e.g., privacy policy page). "
        "Art. 41(1) requires public accessibility."
    )
```

---

## Breach Notification (Art. 48 + ANPD Resolution CD/ANPD/No. 15/2023)

### 3-business-day notification to ANPD (Pattern 1 — DETERMINISTIC)

```python
def test_breach_notified_to_anpd_within_3_business_days(
    controls_evidence: dict,
    reference_date: date,
):
    """
    Art. 48 + ANPD Resolution: Security incidents that may cause relevant harm
    must be reported to the ANPD within 3 business days of becoming aware.
    ASSUME-LGPD-BREACH-001: Brazilian business days = Mon–Fri; national holidays
    excluded (compliance team must maintain holiday calendar).
    """
    incident = controls_evidence.get("lgpd_security_incident", {})
    if not incident:
        pytest.skip("No security incident in evidence — breach notification test not applicable")
    if not incident.get("notification_required", True):
        pytest.skip("Incident determined not to require ANPD notification (harm assessment on file)")

    awareness_date = date.fromisoformat(str(incident["awareness_date"]))
    deadline = add_business_days_brazil(awareness_date, BREACH_ANPD_BUSINESS_DAYS)

    anpd_notification = controls_evidence.get("anpd_breach_notification", {})
    assert anpd_notification, (
        "No ANPD breach notification found. Art. 48 requires notification within "
        f"{BREACH_ANPD_BUSINESS_DAYS} business days of becoming aware."
    )

    submission_date = anpd_notification.get("submission_date")
    assert submission_date, "ANPD notification lacks a submission date"
    submission_date = date.fromisoformat(str(submission_date))

    assert submission_date <= deadline, (
        f"ANPD breach notification submitted on {submission_date}, after the "
        f"{BREACH_ANPD_BUSINESS_DAYS}-business-day deadline of {deadline} "
        f"(awareness: {awareness_date})"
    )


def test_breach_notification_to_affected_data_subjects_when_relevant_harm(
    controls_evidence: dict,
):
    """
    Art. 48(1): When a breach may cause relevant harm to data subjects, they
    must also be notified within a reasonable time. Harm threshold is
    PARAMETERIZED — DPO must conduct harm assessment.
    """
    incident = controls_evidence.get("lgpd_security_incident", {})
    if not incident:
        pytest.skip("No security incident in evidence")

    harm_assessment = incident.get("harm_assessment", {})
    assert harm_assessment, (
        "No harm assessment found for security incident. "
        "Art. 48 requires assessment of whether relevant harm to data subjects may occur."
    )
    assert harm_assessment.get("conducted_by"), "Harm assessment lacks reviewer identity"
    assert harm_assessment.get("assessment_date"), "Harm assessment lacks a date"

    if harm_assessment.get("relevant_harm_likely", False):
        ds_notification = controls_evidence.get("lgpd_ds_breach_notification", {})
        assert ds_notification, (
            "Harm assessment determined relevant harm is likely but no data subject "
            "notification documented. Art. 48(1) requires notification when harm is likely."
        )
```

---

## International Data Transfers (Art. 33)

### ANPD-approved transfer mechanism required (Pattern 1 — DETERMINISTIC)

```python
@pytest.mark.assumption(
    id="ASSUME-LGPD-TRANSFER-001",
    description=(
        "ANPD adequacy list is independent of EU/UK adequacy; ANPD model contractual "
        "clauses (Art. 35(I)) are the standard mechanism; EU SCCs are not directly "
        "usable without ANPD adoption. Adequacy decisions issued under Art. 34 by ANPD."
    ),
    approved_by="DPO",
    review_date="2027-05",
)
def test_international_transfers_use_anpd_approved_mechanism(
    controls_evidence: dict,
):
    """
    Art. 33: International transfers to non-adequate countries require an ANPD-approved
    mechanism. ANPD adequacy list is distinct from EC and ICO adequacy lists.
    """
    transfers = controls_evidence.get("lgpd_international_transfers", [])
    if not transfers:
        pytest.skip("No international data transfers identified — transfer mechanism test not applicable")

    VALID_LGPD_TRANSFER_MECHANISMS = frozenset({
        "anpd_adequacy",
        "anpd_model_clauses",
        "binding_corporate_rules_anpd",
        "explicit_consent_art33_iii",
        "contract_necessity_art33_iv",
        "international_cooperation_art33_v",
        "vital_interests_art33_vi",
        "legal_registry_art33_vii",
    })

    violations = []
    for transfer in transfers:
        mechanism = transfer.get("transfer_mechanism", "")
        if mechanism not in VALID_LGPD_TRANSFER_MECHANISMS:
            violations.append({
                "destination": transfer.get("destination_country"),
                "mechanism_found": mechanism,
            })

    assert not violations, (
        "International transfers using non-ANPD-approved mechanisms: "
        + "; ".join(f"{v['destination']}: {v['mechanism_found']}" for v in violations)
    )
```

---

## Open assumptions

| ID | Assumption | Pattern | Approved | Review |
|---|---|---|---|---|
| ASSUME-LGPD-ACCESS-001 | 15-day access response deadline runs from receipt of request; no extension mechanism in LGPD; if the full response cannot be provided within 15 days, a partial response with reason must be delivered; we apply the same 15-day window to correction requests for consistency | 1 | Pending | 2027-05 |
| ASSUME-LGPD-BREACH-001 | "3 business days" per ANPD Resolution CD/ANPD/No. 15/2023 = Brazilian Mon–Fri excluding national holidays; clock starts at "becoming aware" (awareness_date); compliance team must maintain Brazilian national holiday calendar for production use | 1 | Pending | 2027-05 |
| ASSUME-LGPD-LI-001 | Legitimate interest (Art. 7(IX) + Art. 10) requires a written Legitimate Interest Assessment (LIA) documenting: controller's legitimate purpose, necessity/suitability of processing, and that data subject's fundamental rights do not override; LIA must be signed by the DPO and reviewed annually | 3 | Pending | 2027-05 |
| ASSUME-LGPD-TRANSFER-001 | ANPD adequacy list is independent of EC/ICO adequacy; ANPD model contractual clauses (Art. 35(I)) are the standard transfer mechanism; EU SCCs are not directly usable without ANPD adoption/recognition | 1 | Pending | 2027-05 |
