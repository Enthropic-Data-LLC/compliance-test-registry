# SEC Cybersecurity Rules — Incident Disclosure & Annual Report Obligations
## 17 CFR Parts 229 (S-K Item 106), 249 (Form 8-K Item 1.05)

**Effective:** December 15 2023 (large accelerated filers); June 15 2024 (all others)
**Authority:** U.S. Securities and Exchange Commission
**Scope:** All SEC-registered public companies; foreign private issuers with FPI modifications

---

## RDF extraction

### Form 8-K Item 1.05 — Material cybersecurity incident disclosure

```
Subject:    SEC-registered public company
Condition:  Company determines a cybersecurity incident is material
Obligation: File Form 8-K Item 1.05 within 4 business days of determination
Evidence:   8-K filing timestamp in EDGAR; materiality determination documentation with date
```

### S-K Item 106(b) — Annual risk management disclosure

```
Subject:    SEC-registered public company
Condition:  Annual report (Form 10-K / 20-F) filing
Obligation: Disclose cybersecurity risk management process elements (binary presence)
Evidence:   10-K/20-F filing with Item 106(b) section containing all required disclosures
```

### S-K Item 106(c) — Annual governance disclosure

```
Subject:    SEC-registered public company
Condition:  Annual report (Form 10-K / 20-F) filing
Obligation: Disclose board oversight and management role in cybersecurity risk management
Evidence:   10-K/20-F filing with Item 106(c) section; board committee charter or minutes
```

---

## Constants

```python
from datetime import date, timedelta

# Form 8-K Item 1.05
INCIDENT_DISCLOSURE_BUSINESS_DAYS = 4      # from materiality determination
DOJ_INITIAL_DELAY_DAYS            = 60     # national security / public safety delay
DOJ_EXTENSION_DELAY_DAYS          = 60     # additional extension upon renewed notice
MAX_DOJ_TOTAL_DELAY_DAYS          = 120    # 60 + 60 max per Item 1.05(c)

# Regulation S-K Item 106(b) — required disclosure elements (binary presence checklist)
ITEM_106B_REQUIRED_DISCLOSURES = frozenset({
    "risk_assessment_process_described",
    "erm_integration_described",
    "third_party_assessors_disclosed",
    "third_party_service_provider_risk_oversight_described",
    "prior_incident_material_impact_disclosed",
})

# Regulation S-K Item 106(c) — required governance disclosures (binary presence checklist)
ITEM_106C_REQUIRED_DISCLOSURES = frozenset({
    "board_oversight_body_identified",
    "board_oversight_frequency_described",
    "management_roles_identified",
    "management_expertise_described",
    "incident_reporting_to_management_described",
})

# 8-K required disclosure elements — Item 1.05(a)
ITEM_105A_REQUIRED_ELEMENTS = frozenset({
    "incident_nature",
    "incident_scope",
    "incident_timing",
    "material_impact_or_likely_impact",
})


def add_business_days(start: date, n: int) -> date:
    """Return date n business days (Mon–Fri, US federal holidays excluded) after start."""
    US_FEDERAL_HOLIDAYS = _load_federal_holidays(start.year)
    current = start
    count = 0
    while count < n:
        current += timedelta(days=1)
        if current.weekday() < 5 and current not in US_FEDERAL_HOLIDAYS:
            count += 1
    return current


def _load_federal_holidays(year: int) -> frozenset:
    """Approximate US federal holidays for a given year (ASSUME-SEC-DISC-001)."""
    from dateutil.relativedelta import relativedelta, MO
    import calendar
    jan_1  = date(year, 1, 1)
    mlk    = date(year, 1, 1) + relativedelta(weekday=MO(+3))   # 3rd Monday Jan
    pres   = date(year, 2, 1) + relativedelta(weekday=MO(+3))   # 3rd Monday Feb
    mem    = date(year, 5, 31) + relativedelta(weekday=MO(-1))  # last Monday May
    june19 = date(year, 6, 19)
    july4  = date(year, 7, 4)
    labor  = date(year, 9, 1) + relativedelta(weekday=MO(+1))   # 1st Monday Sep
    col    = date(year, 10, 1) + relativedelta(weekday=MO(+2))  # 2nd Monday Oct
    vet    = date(year, 11, 11)
    thanks = date(year, 11, 1) + relativedelta(weekday=MO(+4)) + timedelta(days=3)  # Thanksgiving Thu
    xmas   = date(year, 12, 25)
    return frozenset({jan_1, mlk, pres, mem, june19, july4, labor, col, vet, thanks, xmas})
```

---

## Scope pre-condition fixture

```python
import pytest

@pytest.fixture(autouse=True)
def sec_registrant_scope_check(entity_profile: dict):
    """Skip all SEC cybersecurity rule tests if entity is not an SEC registrant."""
    if not entity_profile.get("sec_registered", False):
        pytest.skip("Entity is not an SEC-registered public company — SEC cybersecurity rules do not apply")
    if not entity_profile.get("sec_effective_date_reached", True):
        pytest.skip("SEC cybersecurity rules not yet effective for this filer category")
```

---

## Form 8-K Item 1.05 — Material Cybersecurity Incident Disclosure

### Materiality determination gate (Pattern 3 — CONTESTED)

```python
@pytest.mark.human_review_required(
    reason=(
        "Materiality determination follows TSC Industries v. Northway: substantial likelihood "
        "that a reasonable investor would consider the information important. No bright-line "
        "threshold — requires named executive/legal sign-off. Pattern 3 gate: the 4-business-day "
        "clock does NOT start until materiality is formally determined and dated. "
        "ASSUME-SEC-MAT-001: discovery date alone does not start the clock."
    )
)
def test_materiality_determination_is_documented(
    controls_evidence: dict,
    reference_date: date,
):
    """
    Verify a cybersecurity incident materiality determination was documented with:
    - Named decision-maker (CEO / CFO / CISO / legal counsel)
    - Date of determination
    - Rationale referencing material impact factors
    """
    incident = controls_evidence.get("cybersecurity_incident", {})
    if not incident:
        pytest.skip("No cybersecurity incident in evidence — test not applicable")

    determination = incident.get("materiality_determination", {})
    assert determination, "No materiality determination record found for incident"
    assert determination.get("determination_date"), "Materiality determination lacks a date"
    assert determination.get("decision_maker"), "Materiality determination lacks a named decision-maker"
    assert determination.get("rationale"), "Materiality determination lacks documented rationale"

    if incident.get("determined_material", False) is False:
        pytest.skip("Incident determined not material — 8-K filing obligation does not arise")
```

### 4-business-day filing deadline (Pattern 1 — DETERMINISTIC)

```python
def test_form_8k_filed_within_four_business_days(
    controls_evidence: dict,
    reference_date: date,
):
    """
    Form 8-K Item 1.05 must be filed within 4 business days of the materiality
    determination date. ASSUME-SEC-DISC-001: business days = Mon–Fri excluding
    US federal holidays, consistent with SEC business day conventions.
    """
    incident = controls_evidence.get("cybersecurity_incident", {})
    if not incident or not incident.get("determined_material", False):
        pytest.skip("No material cybersecurity incident in evidence")

    determination_date = incident["materiality_determination"]["determination_date"]
    if isinstance(determination_date, str):
        from datetime import datetime
        determination_date = datetime.fromisoformat(determination_date).date()

    deadline = add_business_days(determination_date, INCIDENT_DISCLOSURE_BUSINESS_DAYS)

    doj_delay = incident.get("doj_delay_invoked", False)
    if doj_delay:
        # DOJ must notify SEC; registrant must have documentation (ASSUME-SEC-DOJ-001)
        doj_notification = incident.get("doj_notification_to_sec", {})
        assert doj_notification, (
            "DOJ delay invoked but no DOJ-to-SEC notification documentation found. "
            "Item 1.05(c) requires DOJ — not the registrant — to notify the SEC."
        )
        doj_notice_date = doj_notification["notice_date"]
        if isinstance(doj_notice_date, str):
            from datetime import datetime
            doj_notice_date = datetime.fromisoformat(doj_notice_date).date()
        delay_days = incident.get("doj_delay_days_granted", DOJ_INITIAL_DELAY_DAYS)
        assert delay_days <= MAX_DOJ_TOTAL_DELAY_DAYS, (
            f"DOJ delay of {delay_days} days exceeds statutory maximum of "
            f"{MAX_DOJ_TOTAL_DELAY_DAYS} days (60 + 60)"
        )
        deadline = doj_notice_date + timedelta(days=delay_days)

    filing = controls_evidence.get("form_8k_item_105", {})
    assert filing, "No Form 8-K Item 1.05 filing found in evidence"

    filing_date = filing.get("edgar_filing_date")
    assert filing_date, "Form 8-K filing lacks EDGAR filing date"
    if isinstance(filing_date, str):
        from datetime import datetime
        filing_date = datetime.fromisoformat(filing_date).date()

    assert filing_date <= deadline, (
        f"Form 8-K filed on {filing_date}, which is after the {INCIDENT_DISCLOSURE_BUSINESS_DAYS}-"
        f"business-day deadline of {deadline} (determination: {determination_date})"
    )
```

### 8-K required disclosure elements — content checklist (Pattern 1 — DETERMINISTIC)

```python
def test_form_8k_contains_required_disclosure_elements(
    controls_evidence: dict,
):
    """
    Item 1.05(a): 8-K must contain all required elements to the extent known at
    filing time. Missing elements must be disclosed in an amended 8-K (8-K/A)
    when information becomes available. ASSUME-SEC-AMD-001: amended 8-K timing
    is "as soon as practicable" — Pattern 2 for the amendment deadline.
    """
    incident = controls_evidence.get("cybersecurity_incident", {})
    if not incident or not incident.get("determined_material", False):
        pytest.skip("No material cybersecurity incident in evidence")

    filing = controls_evidence.get("form_8k_item_105", {})
    assert filing, "No Form 8-K Item 1.05 filing found in evidence"

    disclosed_elements = frozenset(filing.get("disclosed_elements", []))
    elements_known_at_filing = frozenset(filing.get("elements_known_at_filing", list(ITEM_105A_REQUIRED_ELEMENTS)))

    # Only elements that were known at time of filing are required in initial 8-K
    required_at_filing = ITEM_105A_REQUIRED_ELEMENTS & elements_known_at_filing
    missing = required_at_filing - disclosed_elements

    assert not missing, (
        f"Form 8-K Item 1.05 is missing required disclosures that were known at filing: {missing}. "
        "Elements not yet determined may be omitted from initial 8-K but require an amended 8-K/A "
        "when the information becomes available."
    )
```

### Amended 8-K when material information later determined (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-SEC-AMD-001",
    description=(
        "Amended 8-K/A timeline: the SEC rule says 'as soon as practicable' when previously "
        "omitted material information becomes available. No bright-line days specified. "
        "We treat this as Pattern 2 — Privacy/Legal Officer must review and set a documented "
        "target date upon each information-availability event."
    ),
    approved_by="Compliance Officer",
    review_date="2027-05",
)
def test_amended_8k_filed_when_omitted_information_available(
    controls_evidence: dict,
    reference_date: date,
):
    """
    If the initial 8-K omitted required elements because they were not yet known,
    an amended 8-K/A must be filed when that information becomes available.
    """
    incident = controls_evidence.get("cybersecurity_incident", {})
    if not incident or not incident.get("determined_material", False):
        pytest.skip("No material cybersecurity incident in evidence")

    filing = controls_evidence.get("form_8k_item_105", {})
    if not filing:
        pytest.skip("No 8-K filing in evidence")

    elements_known_at_filing = frozenset(filing.get("elements_known_at_filing", list(ITEM_105A_REQUIRED_ELEMENTS)))
    omitted_at_filing = ITEM_105A_REQUIRED_ELEMENTS - elements_known_at_filing
    if not omitted_at_filing:
        pytest.skip("No elements were omitted from initial 8-K — amendment not required")

    amendment = controls_evidence.get("form_8k_amendment", {})
    assert amendment, (
        f"Elements {omitted_at_filing} were omitted from initial 8-K. "
        "An amended 8-K/A is required once this information becomes available. "
        "No amendment found in evidence."
    )
    assert amendment.get("edgar_filing_date"), "8-K/A amendment lacks EDGAR filing date"
    assert amendment.get("covered_elements"), "8-K/A amendment does not specify which elements it covers"

    missing_in_amendment = omitted_at_filing - frozenset(amendment.get("covered_elements", []))
    assert not missing_in_amendment, (
        f"8-K/A amendment does not address all omitted elements: {missing_in_amendment}"
    )
```

---

## S-K Item 106(b) — Annual Risk Management & Strategy Disclosure

### Required elements presence check (Pattern 1 — DETERMINISTIC)

```python
def test_annual_report_item_106b_contains_all_required_disclosures(
    controls_evidence: dict,
):
    """
    S-K Item 106(b): annual report must contain all required risk management
    and strategy disclosures. Each element is a binary presence check.
    ASSUME-SEC-106-001: presence is DETERMINISTIC; adequacy of substance is Pattern 2.
    """
    annual_report = controls_evidence.get("annual_report_cybersecurity", {})
    assert annual_report, "No annual report cybersecurity disclosures found in evidence"

    item_106b = annual_report.get("item_106b", {})
    assert item_106b, "No Item 106(b) section found in annual report evidence"

    disclosed = frozenset(item_106b.get("disclosed_elements", []))
    missing = ITEM_106B_REQUIRED_DISCLOSURES - disclosed

    assert not missing, (
        f"Annual report Item 106(b) is missing required disclosure elements: {missing}. "
        "All five elements must be present; their substantive adequacy is assessed under "
        "ASSUME-SEC-106-001 (Pattern 2)."
    )
```

### Risk management process integration (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-SEC-106-001",
    description=(
        "S-K Item 106 required disclosure elements are treated as a DETERMINISTIC presence "
        "checklist; adequacy of the substance of each disclosure (e.g., whether the described "
        "risk management process is genuinely integrated into ERM) is Pattern 2 — requires "
        "Disclosure Committee / legal counsel review."
    ),
    approved_by="Disclosure Committee",
    review_date="2027-05",
)
def test_risk_management_process_integration_adequacy(
    entity_profile: dict,
    controls_evidence: dict,
):
    """
    Item 106(b) requires disclosure of whether the cybersecurity risk management
    process is integrated into the overall enterprise risk management framework.
    Adequacy of integration (not merely its disclosure) is assessed by the
    Disclosure Committee.
    """
    annual_report = controls_evidence.get("annual_report_cybersecurity", {})
    item_106b = annual_report.get("item_106b", {}) if annual_report else {}

    erm_integration = item_106b.get("erm_integration_review", {})
    assert erm_integration, (
        "No ERM integration review documented for Item 106(b) substantive adequacy assessment. "
        "Disclosure Committee must review and approve the disclosed ERM integration description."
    )
    assert erm_integration.get("reviewed_by"), "ERM integration review lacks reviewer identity"
    assert erm_integration.get("review_date"), "ERM integration review lacks review date"
    assert erm_integration.get("approved", False), (
        "ERM integration description has not been approved by Disclosure Committee"
    )
```

### Third-party risk management disclosure (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-SEC-106-001",
    description="See above — substantive adequacy is Pattern 2.",
    approved_by="Disclosure Committee",
    review_date="2027-05",
)
def test_third_party_service_provider_risk_oversight_disclosed(
    controls_evidence: dict,
):
    """
    Item 106(b): disclosure of whether the company has a process to oversee and
    identify material cybersecurity risks associated with third-party service providers.
    Binary presence is DETERMINISTIC; adequacy of the described process is Pattern 2.
    """
    annual_report = controls_evidence.get("annual_report_cybersecurity", {})
    item_106b = annual_report.get("item_106b", {}) if annual_report else {}

    tprm_disclosure = item_106b.get("third_party_risk_oversight_description")
    assert tprm_disclosure, (
        "Item 106(b) lacks a third-party service provider risk oversight disclosure. "
        "This is a required element regardless of whether a formal TPRM program exists — "
        "if no process exists, that must be disclosed."
    )
```

---

## S-K Item 106(c) — Annual Governance Disclosure

### Required governance elements presence check (Pattern 1 — DETERMINISTIC)

```python
def test_annual_report_item_106c_contains_all_required_disclosures(
    controls_evidence: dict,
):
    """
    S-K Item 106(c): annual report must identify the board body overseeing cybersecurity
    risk, describe management's role, and describe incident escalation to management.
    Binary presence check for each element.
    """
    annual_report = controls_evidence.get("annual_report_cybersecurity", {})
    assert annual_report, "No annual report cybersecurity disclosures found in evidence"

    item_106c = annual_report.get("item_106c", {})
    assert item_106c, "No Item 106(c) section found in annual report evidence"

    disclosed = frozenset(item_106c.get("disclosed_elements", []))
    missing = ITEM_106C_REQUIRED_DISCLOSURES - disclosed

    assert not missing, (
        f"Annual report Item 106(c) is missing required governance disclosure elements: {missing}."
    )
```

### Board cybersecurity oversight body identified (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-SEC-106-001",
    description="See above — substantive adequacy is Pattern 2.",
    approved_by="Disclosure Committee",
    review_date="2027-05",
)
def test_board_cybersecurity_oversight_body_and_frequency(
    controls_evidence: dict,
):
    """
    Item 106(c): the registrant must identify which board body (full board, audit committee,
    risk committee) oversees cybersecurity and how frequently it receives cybersecurity
    updates. Both body identity and frequency must be disclosed.
    """
    annual_report = controls_evidence.get("annual_report_cybersecurity", {})
    item_106c = annual_report.get("item_106c", {}) if annual_report else {}

    board_oversight = item_106c.get("board_oversight", {})
    assert board_oversight, "No board cybersecurity oversight disclosure found in Item 106(c)"
    assert board_oversight.get("oversight_body"), "Board oversight body not identified (e.g., audit committee)"
    assert board_oversight.get("update_frequency"), "Board update frequency not disclosed"
    assert board_oversight.get("update_mechanism"), "Mechanism by which board is informed not described"
```

### Management expertise disclosure (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-SEC-106-001",
    description="See above — substantive adequacy is Pattern 2.",
    approved_by="Disclosure Committee",
    review_date="2027-05",
)
def test_management_cybersecurity_expertise_described(
    controls_evidence: dict,
):
    """
    Item 106(c): management positions responsible for cybersecurity risk must be
    identified, and their relevant expertise described. CISO, CTO, or other roles
    may satisfy this; adequacy of expertise description is Pattern 2.
    """
    annual_report = controls_evidence.get("annual_report_cybersecurity", {})
    item_106c = annual_report.get("item_106c", {}) if annual_report else {}

    mgmt_roles = item_106c.get("management_cybersecurity_roles", [])
    assert mgmt_roles, (
        "Item 106(c) requires identification of management positions responsible for "
        "cybersecurity risk management. No management roles found in disclosure evidence."
    )
    for role in mgmt_roles:
        assert role.get("title"), "Management role lacks a title"
        assert role.get("expertise_description"), (
            f"Management role '{role.get('title')}' lacks expertise description. "
            "Item 106(c) requires disclosure of relevant expertise or experience in cybersecurity."
        )
```

---

## Multi-framework notification coordination (Pattern 1 — DETERMINISTIC)

```python
def test_parallel_notification_deadlines_tracked(
    controls_evidence: dict,
    entity_profile: dict,
    reference_date: date,
):
    """
    When a cybersecurity incident is material, multiple notification obligations
    may run in parallel. Each applicable deadline must be tracked separately.
    The SEC 4-business-day clock is the tightest US obligation for public companies.
    """
    incident = controls_evidence.get("cybersecurity_incident", {})
    if not incident or not incident.get("determined_material", False):
        pytest.skip("No material cybersecurity incident in evidence")

    notification_tracker = controls_evidence.get("notification_tracker", {})
    assert notification_tracker, (
        "No parallel notification tracker found. Material cybersecurity incidents must "
        "track all applicable notification obligations simultaneously."
    )

    # Verify SEC 8-K is in the tracker
    assert "sec_8k" in notification_tracker, "SEC 8-K notification track missing from tracker"

    # Verify other applicable frameworks are tracked
    applicable_frameworks = []
    if entity_profile.get("ny_dfs_covered_entity", False):
        applicable_frameworks.append("nydfs_72hr")
    if entity_profile.get("hipaa_covered_entity", False):
        applicable_frameworks.append("hipaa_breach_60day")
    if entity_profile.get("gdpr_in_scope", False):
        applicable_frameworks.append("gdpr_72hr")
    if entity_profile.get("dora_in_scope", False):
        applicable_frameworks.append("dora_4hr_initial")

    for framework in applicable_frameworks:
        assert framework in notification_tracker, (
            f"Required notification track '{framework}' missing from parallel tracker. "
            "All applicable frameworks must be tracked independently."
        )

    # Verify SEC track has a filed or scheduled date
    sec_track = notification_tracker["sec_8k"]
    assert sec_track.get("status") in ("filed", "scheduled"), (
        "SEC 8-K track has no filed or scheduled date"
    )
```

---

## Foreign Private Issuer (FPI) modifications

```python
@pytest.fixture(autouse=True)
def fpi_form_check(entity_profile: dict):
    """Tag FPI registrants so tests can select the correct form (6-K vs 8-K, 20-F vs 10-K)."""
    entity_profile.setdefault("is_fpi", False)


def test_fpi_uses_correct_form_for_material_incident(
    controls_evidence: dict,
    entity_profile: dict,
):
    """
    FPIs must disclose material incidents on Form 6-K (not 8-K) within the same
    4-business-day deadline from materiality determination. Annual disclosures
    go on Form 20-F Item 16K instead of Form 10-K Item 106.
    """
    if not entity_profile.get("is_fpi", False):
        pytest.skip("Entity is not a foreign private issuer — FPI form requirements do not apply")

    incident = controls_evidence.get("cybersecurity_incident", {})
    if not incident or not incident.get("determined_material", False):
        pytest.skip("No material cybersecurity incident in evidence")

    filing = controls_evidence.get("form_6k_cybersecurity", {})
    assert filing, (
        "FPI with material cybersecurity incident must file Form 6-K (not 8-K). "
        "No Form 6-K cybersecurity filing found in evidence."
    )

    filing_date = filing.get("edgar_filing_date")
    assert filing_date, "Form 6-K filing lacks EDGAR filing date"
    if isinstance(filing_date, str):
        from datetime import datetime
        filing_date = datetime.fromisoformat(filing_date).date()

    determination_date = incident["materiality_determination"]["determination_date"]
    if isinstance(determination_date, str):
        from datetime import datetime
        determination_date = datetime.fromisoformat(determination_date).date()

    deadline = add_business_days(determination_date, INCIDENT_DISCLOSURE_BUSINESS_DAYS)
    assert filing_date <= deadline, (
        f"Form 6-K filed {filing_date} after {INCIDENT_DISCLOSURE_BUSINESS_DAYS}-business-day "
        f"deadline of {deadline}"
    )
```

---

## Open assumptions

| ID | Assumption | Pattern | Approved | Review |
|---|---|---|---|---|
| ASSUME-SEC-DISC-001 | "Business days" for the 4-day clock = Mon–Fri excluding US federal holidays, consistent with SEC business day conventions throughout the federal securities laws | 1 | Pending | 2027-05 |
| ASSUME-SEC-MAT-001 | The 4-business-day clock starts at the formal materiality determination date; discovery date alone does not start the clock; companies may take a reasonable time to investigate before determining materiality, but cannot delay the determination process indefinitely | 3 | Pending | 2027-05 |
| ASSUME-SEC-DOJ-001 | DOJ delay exception requires DOJ — not the registrant — to notify the SEC; registrant must have documented evidence of DOJ notification with the notice date; without this documentation the standard deadline applies | 1 | Pending | 2027-05 |
| ASSUME-SEC-AMD-001 | Amended 8-K/A timing is "as soon as practicable" — no bright-line days specified in the rule; treated as Pattern 2 requiring Disclosure Committee review and a documented target date for each information-availability event | 2 | Pending | 2027-05 |
| ASSUME-SEC-106-001 | S-K Item 106 required disclosure elements are a DETERMINISTIC presence checklist; adequacy of the substance of each disclosure is Pattern 2 requiring Disclosure Committee / legal counsel review and approval before the annual report is filed | 2 | Pending | 2027-05 |
