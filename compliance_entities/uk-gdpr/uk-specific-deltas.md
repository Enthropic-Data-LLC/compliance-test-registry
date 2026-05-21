# UK GDPR + DPA 2018 — UK-Specific Deltas
## UK GDPR (retained EU GDPR as amended) + Data Protection Act 2018

**Design note:** UK GDPR is substantially identical to EU GDPR. This spec file covers **only the UK-specific departures** from EU GDPR. For all obligations with identical treatment (lawful basis, consent, privacy notices Art. 13/14, DSRs Art. 15–22, DPIA Art. 35, DPA Art. 28, breach notification timelines Art. 33/34), refer to the EU GDPR spec files in `compliance_entities/gdpr/`. Run UK GDPR tests in addition to — not instead of — EU GDPR tests when an organization processes both EU and UK personal data.

**Applies to:** Organizations established in the UK that process personal data; organizations outside the UK that process personal data of UK residents in connection with offering goods/services to them or monitoring their behavior in the UK
**Trigger:** UK establishment (any office, branch, or other stable arrangement in the UK); offering goods or services to UK persons; monitoring behavior of UK persons within the UK; applies post-Brexit under the retained EU GDPR (UK GDPR) + Data Protection Act 2018
**Jurisdiction:** United Kingdom (England, Scotland, Wales, Northern Ireland); extraterritorial reach — applies to non-UK organizations targeting UK persons; enforced by the Information Commissioner's Office (ICO)
**Not applicable to:** Processing exclusively for national security or defense purposes (separate legislation); law enforcement processing (Part 3 of the Data Protection Act 2018 instead); intelligence services; purely personal or household use; deceased persons (generally)

---

## RDF extraction

### ICO registration

```
Subject:    UK data controller
Condition:  Organization processes personal data in the UK (most organizations)
Obligation: Register with the ICO and pay annual fee before processing
Evidence:   ICO register entry; fee payment receipt; correct tier classification
```

### UK international transfers

```
Subject:    UK controller or processor
Condition:  Transfer of personal data to a country without a UK adequacy regulation
Obligation: Use a UK-approved transfer mechanism (UK IDTA or UK Addendum to EU SCCs)
Evidence:   Executed UK IDTA / UK Addendum for each transfer relationship to non-adequate countries
```

---

## Constants

```python
from datetime import date, timedelta

# ICO registration tiers (DPA 2018 / Data Protection (Charges and Information) Regulations 2018)
ICO_TIER_1_FEE = 40    # Micro-organisations (≤10 staff AND ≤£632,000 turnover)
ICO_TIER_2_FEE = 60    # Small/medium (≤250 staff AND ≤£36M turnover, if not Tier 1)
ICO_TIER_3_FEE = 2900  # All other controllers (large organisations)

# Age of consent for information society services (DPA 2018 §9)
UK_AGE_OF_CONSENT_ISS = 13   # NB: EU GDPR default is 16; EU member states can lower to 13

# Breach notification
BREACH_ICO_HOURS = 72        # Art. 33 UK GDPR — same deadline as EU GDPR; recipient is ICO

# SAR response (same as EU GDPR Art. 15)
SAR_INITIAL_DAYS    = 30
SAR_EXTENSION_DAYS  = 60     # Total = 90 days with extension

# ICO registration renewal — annual
ICO_REGISTRATION_RENEWAL_MONTHS = 12

# UK IDTA / UK Addendum — current version
UK_IDTA_VERSION = "B1.0"     # ICO-approved template, effective March 2022
UK_ADDENDUM_VERSION = "1.0"  # UK Addendum to EU SCCs, effective March 2022
```

---

## Scope pre-condition fixture

```python
import pytest

@pytest.fixture(autouse=True)
def uk_gdpr_scope_check(entity_profile: dict):
    """Skip UK GDPR tests if entity does not process UK personal data."""
    if not entity_profile.get("processes_uk_personal_data", False):
        pytest.skip("Entity does not process UK personal data — UK GDPR does not apply")
```

---

## ICO Registration (DPA 2018 / Fee Regulations)

### Registration existence — current (Pattern 1 — DETERMINISTIC)

```python
def test_ico_registration_is_current(
    controls_evidence: dict,
    reference_date: date,
):
    """
    DPA 2018 s.108: Most UK data controllers must register with the ICO and
    pay an annual fee. Failure to register is a criminal offence.
    Registration existence and currency are DETERMINISTIC binary checks.
    """
    ico_reg = controls_evidence.get("ico_registration", {})
    assert ico_reg, (
        "No ICO registration record found. UK data controllers must register with the "
        "ICO before processing personal data."
    )
    assert ico_reg.get("registration_number"), "ICO registration lacks a registration number"
    assert ico_reg.get("expiry_date"), "ICO registration lacks an expiry date"

    expiry = date.fromisoformat(str(ico_reg["expiry_date"]))
    assert expiry >= reference_date, (
        f"ICO registration expired on {expiry}. Current date: {reference_date}. "
        "Renewal must be completed before expiry to avoid a criminal offence."
    )


def test_ico_registration_renewal_not_lapsing_soon(
    controls_evidence: dict,
    reference_date: date,
):
    """Warn if ICO registration expires within 30 days — renewal must be timely."""
    ico_reg = controls_evidence.get("ico_registration", {})
    if not ico_reg or not ico_reg.get("expiry_date"):
        pytest.skip("No ICO registration data in evidence")

    expiry = date.fromisoformat(str(ico_reg["expiry_date"]))
    days_remaining = (expiry - reference_date).days
    assert days_remaining > 30, (
        f"ICO registration expires in {days_remaining} days ({expiry}). "
        "Renew immediately — processing without a valid registration is a criminal offence."
    )
```

### ICO registration tier classification (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-UK-GDPR-REG-001",
    description=(
        "ICO registration tier is determined by the organization's annual turnover and "
        "headcount as defined in the Data Protection (Charges and Information) Regulations "
        "2018; we treat the organization's self-classification as the baseline and flag "
        "for DPO / Finance review if classification has not been reviewed in the past year."
    ),
    approved_by="DPO",
    review_date="2027-05",
)
def test_ico_tier_classification_reviewed_annually(
    controls_evidence: dict,
    reference_date: date,
):
    """
    ICO registration tier (1/2/3) determines the annual fee. Tier depends on
    staff count and annual turnover — must be reviewed when these change.
    """
    ico_reg = controls_evidence.get("ico_registration", {})
    if not ico_reg:
        pytest.skip("No ICO registration in evidence")

    tier_review = ico_reg.get("tier_classification_review", {})
    assert tier_review, "ICO tier classification has never been reviewed"
    assert tier_review.get("reviewed_by"), "ICO tier review lacks reviewer identity"

    review_date_val = tier_review.get("review_date")
    assert review_date_val, "ICO tier review lacks a review date"
    review_age = (reference_date - date.fromisoformat(str(review_date_val))).days / 30.44
    assert review_age <= ICO_REGISTRATION_RENEWAL_MONTHS, (
        f"ICO tier classification last reviewed {review_age:.0f} months ago "
        f"(threshold: {ICO_REGISTRATION_RENEWAL_MONTHS} months)"
    )
```

---

## Age of Consent for Information Society Services (DPA 2018 §9)

### Minimum age = 13 (Pattern 1 — DETERMINISTIC)

```python
def test_age_gate_minimum_is_13_for_information_society_services(
    controls_evidence: dict,
    entity_profile: dict,
):
    """
    DPA 2018 §9: Age of consent for information society services in the UK is 13.
    EU GDPR default is 16 (member states may lower to 13; UK has done so via DPA 2018).
    ASSUME-UK-GDPR-AGE-001: when serving both UK and EU users, the applicable minimum
    for EU users is governed by each member state's implementing legislation (typically
    13–16 depending on country); separate age verification logic may be required.
    """
    if not entity_profile.get("offers_information_society_services_to_uk_under_18s", False):
        pytest.skip("Entity does not offer ISS to under-18s in UK — age gate not required")

    age_gate = controls_evidence.get("age_verification", {})
    assert age_gate, "No age verification mechanism found for information society services"

    uk_min_age = age_gate.get("uk_minimum_age")
    assert uk_min_age is not None, "UK minimum age not configured in age verification system"
    assert uk_min_age >= UK_AGE_OF_CONSENT_ISS, (
        f"UK age gate minimum is {uk_min_age}, which is below the DPA 2018 §9 "
        f"minimum of {UK_AGE_OF_CONSENT_ISS}"
    )
    assert age_gate.get("verification_mechanism"), (
        "Age verification mechanism must be described — not merely a self-declaration "
        "tick-box for high-risk services"
    )
```

---

## Breach Notification to ICO (Art. 33 UK GDPR)

### 72-hour notification to ICO (Pattern 1 — DETERMINISTIC)

```python
def test_personal_data_breach_reported_to_ico_within_72_hours(
    controls_evidence: dict,
    reference_date: date,
):
    """
    Art. 33 UK GDPR: Personal data breaches must be reported to the ICO within
    72 hours of becoming aware. Unlike EU GDPR (which goes to the lead SA in the
    member state of establishment), UK GDPR always goes to the ICO — the sole
    UK supervisory authority (no one-stop-shop mechanism).
    If operating in both UK and EU: separate notifications to ICO and the relevant
    EU lead SA may both be required simultaneously.
    """
    breach = controls_evidence.get("personal_data_breach", {})
    if not breach:
        pytest.skip("No personal data breach in evidence — test not applicable")
    if not breach.get("notification_required", True):
        pytest.skip("Breach determined not to require notification (risk assessment on file)")

    awareness_dt = breach.get("awareness_datetime")
    assert awareness_dt, "Breach record lacks an awareness datetime"
    from datetime import datetime
    if isinstance(awareness_dt, str):
        awareness_dt = datetime.fromisoformat(awareness_dt)

    ico_notification = controls_evidence.get("ico_breach_notification", {})
    assert ico_notification, (
        "No ICO breach notification found. Art. 33 UK GDPR requires notification "
        "to the ICO within 72 hours of becoming aware."
    )

    notification_dt = ico_notification.get("submission_datetime")
    assert notification_dt, "ICO notification lacks a submission datetime"
    if isinstance(notification_dt, str):
        notification_dt = datetime.fromisoformat(notification_dt)

    hours_elapsed = (notification_dt - awareness_dt).total_seconds() / 3600
    assert hours_elapsed <= BREACH_ICO_HOURS, (
        f"ICO breach notification submitted {hours_elapsed:.1f} hours after awareness "
        f"(threshold: {BREACH_ICO_HOURS} hours)"
    )


def test_dual_regulator_breach_notification_when_uk_and_eu_both_apply(
    controls_evidence: dict,
    entity_profile: dict,
):
    """
    When an organization processes both UK and EU personal data, a breach may
    require separate notifications: Art. 33 UK GDPR → ICO (72h) AND
    Art. 33 EU GDPR → lead EU supervisory authority (72h).
    Both tracks must be documented independently.
    """
    if not (entity_profile.get("processes_uk_personal_data", False) and
            entity_profile.get("processes_eu_personal_data", False)):
        pytest.skip("Entity does not process both UK and EU personal data — dual notification not required")

    breach = controls_evidence.get("personal_data_breach", {})
    if not breach or not breach.get("notification_required", True):
        pytest.skip("No notifiable breach in evidence")

    ico_notification = controls_evidence.get("ico_breach_notification", {})
    eu_sa_notification = controls_evidence.get("eu_lead_sa_breach_notification", {})

    assert ico_notification, "Dual-regulator breach: ICO notification missing"
    assert eu_sa_notification, (
        "Dual-regulator breach: EU lead SA notification missing. "
        "UK GDPR ICO notification does not satisfy EU GDPR Art. 33 obligation."
    )
```

---

## International Transfers (Art. 44–49 UK GDPR)

### UK IDTA / UK Addendum required for non-adequate countries (Pattern 1 — DETERMINISTIC)

```python
def test_international_transfers_use_uk_approved_mechanism(
    controls_evidence: dict,
):
    """
    Art. 46 UK GDPR: Transfers to non-adequate countries require a UK-approved
    safeguard. ASSUME-UK-GDPR-TRANSFER-001:
    - UK IDTA (B1.0) is the standard UK controller-to-processor transfer mechanism
    - UK Addendum to EU SCCs (v1.0) is acceptable for organizations using EU SCCs
    - EU SCCs ALONE do not satisfy UK GDPR transfer requirements
    NOTE: UK adequacy list is distinct from EU adequacy list — EU adequacy ≠ UK adequacy.
    """
    transfers = controls_evidence.get("international_data_transfers", [])
    if not transfers:
        pytest.skip("No international data transfers recorded — transfer mechanism test not applicable")

    violations = []
    for transfer in transfers:
        dest_country = transfer.get("destination_country")
        uk_adequate = transfer.get("uk_adequacy_regulation", False)
        if uk_adequate:
            continue  # adequacy regulation in place — no safeguard required

        mechanism = transfer.get("transfer_mechanism", "")
        valid_mechanisms = {
            "uk_idta",
            "uk_addendum_to_eu_sccs",
            "uk_bcr",
            "derogation_art49",
        }
        if mechanism not in valid_mechanisms:
            violations.append({
                "destination": dest_country,
                "mechanism_found": mechanism,
                "issue": (
                    "No valid UK transfer mechanism. EU SCCs alone are insufficient — "
                    "UK IDTA or UK Addendum to EU SCCs is required."
                ),
            })

    assert not violations, (
        f"International transfer mechanism violations: "
        + "; ".join(f"{v['destination']}: {v['issue']}" for v in violations)
    )


@pytest.mark.assumption(
    id="ASSUME-UK-GDPR-TRANSFER-001",
    description=(
        "UK IDTA template (ICO B1.0, March 2022) is the authoritative transfer mechanism "
        "for UK controllers; EU SCCs alone are not sufficient for UK data transfers; "
        "UK Addendum to EU SCCs (v1.0) is acceptable for dual UK/EU scenarios; "
        "UK adequacy list is maintained by the Secretary of State — distinct from EC adequacy."
    ),
    approved_by="DPO",
    review_date="2027-05",
)
def test_uk_adequacy_list_consulted_before_transfer(
    controls_evidence: dict,
):
    """
    Transfers to EU/EEA countries are covered by the UK's EU adequacy regulations.
    Other adequacy determinations are UK-specific and must be verified separately.
    """
    transfers = controls_evidence.get("international_data_transfers", [])
    if not transfers:
        pytest.skip("No international data transfers in evidence")

    adequacy_assessed = [t for t in transfers if t.get("uk_adequacy_assessment_date")]
    transfer_count = len(transfers)
    assessed_count = len(adequacy_assessed)

    assert assessed_count == transfer_count, (
        f"Only {assessed_count}/{transfer_count} transfer relationships have a UK adequacy "
        "assessment on file. All transfers must be assessed against the UK adequacy list "
        "(which is separate from the EU adequacy list)."
    )
```

---

## UK vs EU GDPR — operational coexistence

### Separate records of processing for UK and EU (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-UK-GDPR-ROPA-001",
    description=(
        "Organizations processing both UK and EU personal data may maintain a single "
        "combined ROPA if it clearly distinguishes UK and EU processing activities, "
        "controllers, and applicable legal bases. A single undifferentiated ROPA is "
        "acceptable if the organization operates only in the UK."
    ),
    approved_by="DPO",
    review_date="2027-05",
)
def test_ropa_distinguishes_uk_and_eu_processing_when_dual_regulator(
    controls_evidence: dict,
    entity_profile: dict,
):
    """
    Art. 30 UK GDPR: Records of processing activities required. When processing
    both UK and EU data, the ROPA must distinguish the two to enable separate
    legal basis and transfer mechanism tracking.
    """
    if not (entity_profile.get("processes_uk_personal_data", False) and
            entity_profile.get("processes_eu_personal_data", False)):
        pytest.skip("Not a dual-regulator — UK/EU ROPA separation not required")

    ropa = controls_evidence.get("records_of_processing_activities", {})
    assert ropa, "No ROPA found in evidence"
    assert ropa.get("uk_eu_distinguished", False), (
        "ROPA does not distinguish UK vs EU processing activities. "
        "A dual-regulator organization must track jurisdiction-specific legal bases "
        "and transfer mechanisms separately."
    )
```

---

## Open assumptions

| ID | Assumption | Pattern | Approved | Review |
|---|---|---|---|---|
| ASSUME-UK-GDPR-REG-001 | ICO registration tier classification is self-assessed; DPO must review annually or upon material change to headcount / turnover | 2 | Pending | 2027-05 |
| ASSUME-UK-GDPR-TRANSFER-001 | UK IDTA (B1.0) is the standard transfer mechanism; EU SCCs alone insufficient; UK adequacy list is distinct from EC adequacy — must be verified separately | 1 | Pending | 2027-05 |
| ASSUME-UK-GDPR-AGE-001 | DPA 2018 §9 sets UK age of consent for ISS at 13; when serving both UK and EU users, member state-specific age minimums (13–16) may differ and require separate logic | 1 | Pending | 2027-05 |
| ASSUME-UK-GDPR-ROPA-001 | A single combined ROPA may cover both UK and EU if it distinguishes the two; undifferentiated ROPA is acceptable for UK-only processors | 2 | Pending | 2027-05 |
