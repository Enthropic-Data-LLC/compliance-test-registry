# DORA — Incident Reporting, Contracts, Resilience Testing, and ICT Risk
## EU Regulation 2022/2554 — Articles 5–29, effective January 17 2025

**Scope:** EU/EEA financial entities (banks, investment firms, insurance, payment institutions, CASPs, CCPs) and critical ICT third-party service providers (CTPPs)

---

## RDF extraction

### Major ICT incident — initial notification

```
Subject:    DORA-covered financial entity
Condition:  ICT incident classified as "major" per Art. 18 criteria
Obligation: Submit initial notification to competent authority within 4 hours of classification
            AND no later than 24 hours after first becoming aware
Evidence:   Incident log with awareness_datetime and classification_datetime;
            competent authority submission record with timestamp
```

### Major ICT incident — intermediate report

```
Subject:    DORA-covered financial entity
Condition:  Initial notification submitted for a major ICT incident
Obligation: Submit intermediate report within 72 hours of initial notification
Evidence:   Intermediate report submission record timestamped ≤72h after initial notification
```

### Major ICT incident — final report

```
Subject:    DORA-covered financial entity
Condition:  Intermediate report submitted; incident fully remediated
Obligation: Submit final report within 1 month of intermediate report submission
Evidence:   Final report submission record; incident closure confirmation
```

---

## Constants

```python
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# Art. 19 — Major ICT incident reporting timelines
INITIAL_NOTIFICATION_FROM_AWARENESS_HOURS   = 24   # hard outer limit
INITIAL_NOTIFICATION_FROM_CLASSIFICATION_HOURS = 4  # binding if classification < 24h from awareness
INTERMEDIATE_REPORT_FROM_INITIAL_HOURS      = 72
FINAL_REPORT_FROM_INTERMEDIATE_MONTHS       = 1

# Art. 25 — Basic resilience testing cadence
BASIC_TESTING_MONTHS = 12    # at least annually (ASSUME-DORA-TEST-001)

# Art. 26 — TLPT (Threat-Led Penetration Testing)
TLPT_CYCLE_YEARS = 3         # every 3 years for significant entities

# Art. 12 — Backup and recovery
BACKUP_TEST_MONTHS = 12      # annual restore test minimum

# Art. 30(2) — Mandatory ICT contract elements (DETERMINISTIC checklist)
ART_30_MANDATORY_ELEMENTS = frozenset({
    "description_of_functions_and_services",
    "data_processing_locations",
    "availability_authenticity_integrity_confidentiality",
    "data_access_recovery_return_destruction_at_termination",
    "service_level_descriptions_and_performance_targets",
    "incident_notice_and_remediation_provisions",
    "cooperation_with_competent_and_resolution_authorities",
    "termination_rights_and_exit_strategy",
    "audit_rights",
    "business_continuity_plans",
    "ict_security_awareness_training",
    "subcontracting_provisions_for_critical_functions",
})

# Art. 5 — ICT risk framework review
ICT_RISK_FRAMEWORK_REVIEW_MONTHS = 12

# Art. 11 — BCP/DRP existence and annual review
BCP_REVIEW_MONTHS = 12

# Art. 28 — Register of ICT third-party arrangements review
TPSP_REGISTER_REVIEW_MONTHS = 12
```

---

## Scope pre-condition fixture

```python
import pytest

@pytest.fixture(autouse=True)
def dora_scope_check(entity_profile: dict):
    """Skip DORA tests if entity is not a DORA-covered financial entity."""
    if not entity_profile.get("dora_covered_entity", False):
        pytest.skip(
            "Entity is not a DORA-covered financial entity "
            "(banks, investment firms, insurance, payment institutions, "
            "crypto-asset service providers, CCPs)"
        )

@pytest.fixture
def is_simplified_entity(entity_profile: dict) -> bool:
    """True if entity qualifies for simplified ICT risk framework per Art. 16."""
    return entity_profile.get("dora_simplified_framework", False)

@pytest.fixture
def is_significant_entity(entity_profile: dict) -> bool:
    """True if entity designated for TLPT by competent authority (Art. 26)."""
    return entity_profile.get("dora_tlpt_designated", False)
```

---

## Pillar 1 — ICT Risk Management Framework (Art. 5–16)

### ICT risk management framework existence (Pattern 1 — DETERMINISTIC)

```python
def test_ict_risk_management_framework_documented(
    controls_evidence: dict,
    is_simplified_entity: bool,
):
    """
    Art. 6: All financial entities must have a comprehensive ICT risk management
    framework. Simplified entities (Art. 16) may use a reduced framework.
    Framework existence is DETERMINISTIC; adequacy is PARAMETERIZED.
    """
    ict_risk = controls_evidence.get("dora_ict_risk_framework", {})
    assert ict_risk, (
        "Art. 6: No ICT risk management framework documentation found. "
        "All DORA-covered financial entities must maintain a written ICT risk management framework."
    )
    assert ict_risk.get("framework_document"), "ICT risk framework document reference missing"
    assert ict_risk.get("board_approved", False), (
        "Art. 5(2): ICT risk management framework must be approved by the management body (board). "
        "No board approval found."
    )
    assert ict_risk.get("board_approval_date"), "Board approval date not recorded"


def test_ict_risk_framework_reviewed_annually(
    controls_evidence: dict,
    reference_date: date,
):
    """
    Art. 6(5): ICT risk management framework reviewed at least annually
    and after major ICT incidents. ASSUME-DORA-TEST-001: annual = 12 months.
    """
    ict_risk = controls_evidence.get("dora_ict_risk_framework", {})
    if not ict_risk:
        pytest.skip("No ICT risk framework in evidence")

    last_review = ict_risk.get("last_review_date")
    assert last_review, "ICT risk framework lacks a last review date"
    age = (reference_date - date.fromisoformat(str(last_review))).days / 30.44
    assert age <= ICT_RISK_FRAMEWORK_REVIEW_MONTHS, (
        f"ICT risk framework last reviewed {age:.0f} months ago "
        f"(threshold: {ICT_RISK_FRAMEWORK_REVIEW_MONTHS} months)"
    )
```

### Asset register with criticality classification (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-DORA-CTPP-001",
    description=(
        "Critical or important function designation (Art. 3(22)) is a management "
        "determination; we treat the entity's documented function register as "
        "authoritative; adequacy of the designation process is Pattern 3 requiring "
        "senior management sign-off."
    ),
    approved_by="CRO",
    review_date="2027-01",
)
def test_asset_register_exists_with_criticality_classification(
    controls_evidence: dict,
    reference_date: date,
):
    """
    Art. 8: Financial entities must identify, classify, and document all ICT assets
    supporting critical or important functions. Criticality classification required.
    """
    ict_risk = controls_evidence.get("dora_ict_risk_framework", {})
    asset_register = ict_risk.get("asset_register", {}) if ict_risk else {}
    assert asset_register, "Art. 8: No ICT asset register found in evidence"
    assert asset_register.get("criticality_classification_applied", False), (
        "Art. 8: Asset register lacks criticality classification for ICT assets "
        "supporting critical or important functions"
    )
    last_update = asset_register.get("last_updated")
    assert last_update, "Asset register lacks a last-updated date"
    age = (reference_date - date.fromisoformat(str(last_update))).days / 30.44
    assert age <= TPSP_REGISTER_REVIEW_MONTHS, (
        f"Asset register last updated {age:.0f} months ago "
        f"(threshold: {TPSP_REGISTER_REVIEW_MONTHS} months)"
    )
```

### Business continuity plan existence (Pattern 1 — DETERMINISTIC)

```python
def test_bcp_drp_documented_and_reviewed_annually(
    controls_evidence: dict,
    reference_date: date,
):
    """
    Art. 11: Financial entities must have documented ICT business continuity
    policies and disaster recovery procedures. BCP/DRP existence is DETERMINISTIC;
    annual review is DETERMINISTIC once the cadence is established.
    """
    bcp = controls_evidence.get("dora_bcp_drp", {})
    assert bcp, "Art. 11: No BCP/DRP documentation found"
    assert bcp.get("bcp_document"), "BCP document reference missing"
    assert bcp.get("drp_document"), "DRP document reference missing"
    assert bcp.get("rto_hours") is not None, "BCP lacks a defined RTO"
    assert bcp.get("rpo_hours") is not None, "BCP lacks a defined RPO"

    last_review = bcp.get("last_review_date")
    assert last_review, "BCP/DRP lacks a last review date"
    age = (reference_date - date.fromisoformat(str(last_review))).days / 30.44
    assert age <= BCP_REVIEW_MONTHS, (
        f"BCP/DRP last reviewed {age:.0f} months ago (threshold: {BCP_REVIEW_MONTHS} months)"
    )
```

### Art. 12 — Backup and recovery (Pattern 1 — DETERMINISTIC)

```python
def test_backup_policy_geographic_separation(
    controls_evidence: dict,
):
    """
    Art. 12(1): Backup systems geographically separate from primary. Backups
    must be stored at a location that would not be simultaneously affected by
    the same incident impacting the primary system.
    """
    bcp = controls_evidence.get("dora_bcp_drp", {})
    backup = bcp.get("backup_configuration", {}) if bcp else {}
    assert backup, "Art. 12: No backup configuration found"
    assert backup.get("geographically_separate", False), (
        "Art. 12(1): Backup systems are not geographically separate from primary — "
        "a single-site incident could simultaneously impact both"
    )


def test_backup_restore_test_annual(
    controls_evidence: dict,
    reference_date: date,
):
    """
    Art. 12(5): Backup restoration must be tested. ASSUME-DORA-BACKUP-001:
    annual test minimum; test must demonstrate recovery within documented RTO.
    """
    bcp = controls_evidence.get("dora_bcp_drp", {})
    backup = bcp.get("backup_configuration", {}) if bcp else {}
    last_test = backup.get("last_restore_test_date") if backup else None
    assert last_test, "Art. 12: No backup restore test has been performed"
    age = (reference_date - date.fromisoformat(str(last_test))).days / 30.44
    assert age <= BACKUP_TEST_MONTHS, (
        f"Backup restore test {age:.0f} months old (threshold: {BACKUP_TEST_MONTHS} months)"
    )

    # Verify the test demonstrated RTO achievement
    rto_hours = bcp.get("rto_hours") if bcp else None
    test_recovery_hours = backup.get("last_test_recovery_hours")
    if rto_hours is not None and test_recovery_hours is not None:
        assert test_recovery_hours <= rto_hours, (
            f"Last restore test recovery time {test_recovery_hours}h exceeded RTO of {rto_hours}h"
        )
```

---

## Pillar 2 — ICT Incident Classification and Reporting (Art. 17–23)

### Major incident classification — Pattern 3 gate (CONTESTED)

```python
@pytest.mark.human_review_required(
    reason=(
        "Art. 17–18: 'Major ICT incident' classification requires assessment against "
        "5 dimensions per RTS 2024/1515 (client impact, transaction impact, geographic "
        "spread, data loss, criticality, reputational impact, economic impact). Thresholds "
        "vary by entity type. ASSUME-DORA-INC-002: classification is a documented "
        "management decision; classification_datetime must be recorded separately from "
        "awareness_datetime. Pattern 3 gate — the 4-hour clock starts from "
        "classification_datetime."
    )
)
def test_major_incident_classification_documented(
    controls_evidence: dict,
):
    """
    Verify that each ICT incident has a documented classification decision with:
    - Named decision-maker
    - Classification datetime (separate from awareness datetime)
    - Assessment against the 5-dimension Art. 18 criteria
    """
    incidents = controls_evidence.get("dora_ict_incidents", [])
    if not incidents:
        pytest.skip("No ICT incidents in evidence")

    violations = []
    for incident in incidents:
        classification = incident.get("classification", {})
        if not classification:
            violations.append(f"Incident '{incident.get('id', 'unknown')}': no classification record")
            continue
        if not classification.get("classification_datetime"):
            violations.append(f"Incident '{incident.get('id', 'unknown')}': missing classification_datetime")
        if not classification.get("decision_maker"):
            violations.append(f"Incident '{incident.get('id', 'unknown')}': classification lacks named decision-maker")
        if not classification.get("art18_criteria_assessed", False):
            violations.append(f"Incident '{incident.get('id', 'unknown')}': Art. 18 criteria not documented")

    assert not violations, f"ICT incident classification deficiencies: {'; '.join(violations)}"
```

### Initial notification — 4 hours from classification / 24 hours from awareness (Pattern 1 — DETERMINISTIC)

```python
def test_major_incident_initial_notification_within_deadlines(
    controls_evidence: dict,
):
    """
    Art. 19(4)(a): Initial notification to competent authority:
    - Within 4 hours of classifying as major (binding if classification < 24h after awareness)
    - No later than 24 hours from first becoming aware of the incident
    ASSUME-DORA-INC-001: both clocks run independently; whichever produces the tighter
    deadline at the time of notification governs the compliance assessment.
    """
    from datetime import datetime

    incidents = controls_evidence.get("dora_ict_incidents", [])
    major_incidents = [i for i in incidents if i.get("classification", {}).get("is_major", False)]
    if not major_incidents:
        pytest.skip("No major ICT incidents in evidence")

    violations = []
    for incident in major_incidents:
        inc_id = incident.get("id", "unknown")
        awareness_dt  = incident.get("awareness_datetime")
        classification = incident.get("classification", {})
        classification_dt = classification.get("classification_datetime")
        initial_notification_dt = incident.get("initial_notification_datetime")

        if not awareness_dt or not classification_dt:
            violations.append(f"Incident {inc_id}: missing awareness_datetime or classification_datetime")
            continue

        if isinstance(awareness_dt, str):
            awareness_dt = datetime.fromisoformat(awareness_dt)
        if isinstance(classification_dt, str):
            classification_dt = datetime.fromisoformat(classification_dt)

        # Deadline 1: 4 hours from classification
        deadline_from_classification = classification_dt + timedelta(hours=INITIAL_NOTIFICATION_FROM_CLASSIFICATION_HOURS)
        # Deadline 2: 24 hours from awareness
        deadline_from_awareness = awareness_dt + timedelta(hours=INITIAL_NOTIFICATION_FROM_AWARENESS_HOURS)
        # Binding deadline is the earlier of the two
        binding_deadline = min(deadline_from_classification, deadline_from_awareness)

        if not initial_notification_dt:
            violations.append(f"Incident {inc_id}: no initial notification submitted")
            continue

        if isinstance(initial_notification_dt, str):
            initial_notification_dt = datetime.fromisoformat(initial_notification_dt)

        if initial_notification_dt > binding_deadline:
            hours_late = (initial_notification_dt - binding_deadline).total_seconds() / 3600
            violations.append(
                f"Incident {inc_id}: initial notification {hours_late:.1f}h late "
                f"(submitted: {initial_notification_dt}, deadline: {binding_deadline})"
            )

    assert not violations, (
        f"Art. 19 initial notification violations: {'; '.join(violations)}"
    )
```

### Intermediate report — 72 hours from initial notification (Pattern 1 — DETERMINISTIC)

```python
def test_major_incident_intermediate_report_within_72_hours(
    controls_evidence: dict,
):
    """
    Art. 19(4)(b): Intermediate report within 72 hours of initial notification.
    If the situation has changed significantly, the intermediate report updates
    the initial notification with current status.
    """
    from datetime import datetime

    incidents = controls_evidence.get("dora_ict_incidents", [])
    major_incidents = [i for i in incidents if i.get("classification", {}).get("is_major", False)]
    if not major_incidents:
        pytest.skip("No major ICT incidents in evidence")

    violations = []
    for incident in major_incidents:
        inc_id = incident.get("id", "unknown")
        initial_dt = incident.get("initial_notification_datetime")
        intermediate_dt = incident.get("intermediate_report_datetime")

        if not initial_dt:
            continue  # already caught by initial notification test

        if isinstance(initial_dt, str):
            initial_dt = datetime.fromisoformat(initial_dt)

        deadline = initial_dt + timedelta(hours=INTERMEDIATE_REPORT_FROM_INITIAL_HOURS)

        if not intermediate_dt:
            # Only a violation if the deadline has passed
            if datetime.utcnow() > deadline:
                violations.append(f"Incident {inc_id}: no intermediate report submitted; deadline was {deadline}")
            continue

        if isinstance(intermediate_dt, str):
            intermediate_dt = datetime.fromisoformat(intermediate_dt)

        if intermediate_dt > deadline:
            hours_late = (intermediate_dt - deadline).total_seconds() / 3600
            violations.append(
                f"Incident {inc_id}: intermediate report {hours_late:.1f}h late "
                f"(deadline: {deadline})"
            )

    assert not violations, f"Art. 19 intermediate report violations: {'; '.join(violations)}"
```

### Final report — 1 month from intermediate report (Pattern 1 — DETERMINISTIC)

```python
def test_major_incident_final_report_within_one_month(
    controls_evidence: dict,
    reference_date: date,
):
    """
    Art. 19(4)(c): Final report within 1 month of intermediate report submission,
    after incident is fully remediated. Clock runs from the intermediate report date.
    """
    incidents = controls_evidence.get("dora_ict_incidents", [])
    major_incidents = [i for i in incidents if i.get("classification", {}).get("is_major", False)]
    if not major_incidents:
        pytest.skip("No major ICT incidents in evidence")

    violations = []
    for incident in major_incidents:
        inc_id = incident.get("id", "unknown")
        intermediate_date_val = incident.get("intermediate_report_date")
        if not intermediate_date_val:
            continue

        intermediate_date = date.fromisoformat(str(intermediate_date_val))
        deadline = intermediate_date + relativedelta(months=FINAL_REPORT_FROM_INTERMEDIATE_MONTHS)

        if incident.get("status") not in ("remediated", "closed"):
            continue  # incident not yet resolved — final report not yet due

        final_report_date_val = incident.get("final_report_date")
        if not final_report_date_val:
            if reference_date > deadline:
                violations.append(
                    f"Incident {inc_id}: incident resolved but no final report submitted; "
                    f"deadline was {deadline}"
                )
            continue

        final_report_date = date.fromisoformat(str(final_report_date_val))
        if final_report_date > deadline:
            violations.append(
                f"Incident {inc_id}: final report submitted {final_report_date} after "
                f"deadline {deadline}"
            )

    assert not violations, f"Art. 19 final report violations: {'; '.join(violations)}"
```

---

## Pillar 3 — Digital Operational Resilience Testing (Art. 24–27)

### Basic resilience testing — annual cadence (Pattern 1 — DETERMINISTIC)

```python
def test_basic_resilience_testing_completed_annually(
    controls_evidence: dict,
    reference_date: date,
):
    """
    Art. 25: Basic resilience testing program covers all ICT systems and applications
    at least annually. Includes: vulnerability assessments, network security assessments,
    gap analyses, reviews of ICT controls, penetration testing.
    ASSUME-DORA-TEST-001: annual = within 12 calendar months of prior test.
    """
    testing = controls_evidence.get("dora_resilience_testing", {})
    assert testing, "Art. 25: No resilience testing program evidence found"

    basic_test = testing.get("basic_testing", {})
    assert basic_test, "Art. 25: No basic resilience testing record found"

    last_test = basic_test.get("last_completion_date")
    assert last_test, "Basic resilience testing lacks a last completion date"
    age = (reference_date - date.fromisoformat(str(last_test))).days / 30.44
    assert age <= BASIC_TESTING_MONTHS, (
        f"Basic resilience testing last completed {age:.0f} months ago "
        f"(threshold: {BASIC_TESTING_MONTHS} months)"
    )

    required_components = frozenset({
        "vulnerability_assessments",
        "network_security_assessments",
        "penetration_testing",
        "ict_control_reviews",
    })
    completed_components = frozenset(basic_test.get("components_completed", []))
    missing = required_components - completed_components
    assert not missing, (
        f"Art. 25: Basic resilience testing missing components: {missing}"
    )


### TLPT — 3-year cadence for significant entities (Pattern 1 — DETERMINISTIC)

```python
def test_tlpt_completed_within_3_year_cycle(
    controls_evidence: dict,
    reference_date: date,
    is_significant_entity: bool,
):
    """
    Art. 26: Threat-Led Penetration Testing (TLPT) required every 3 years for
    entities designated by the competent authority as significant.
    ASSUME-DORA-TLPT-001: 3-year clock resets from TLPT completion date.
    TIBER-EU framework governs scope and methodology.
    """
    if not is_significant_entity:
        pytest.skip("Entity not designated for TLPT by competent authority — Art. 26 not applicable")

    testing = controls_evidence.get("dora_resilience_testing", {})
    tlpt = testing.get("tlpt", {}) if testing else {}
    assert tlpt, (
        "Art. 26: No TLPT record found. Entity is designated as significant and must "
        "complete TLPT every 3 years."
    )

    last_tlpt = tlpt.get("last_completion_date")
    assert last_tlpt, "TLPT lacks a completion date"
    last_tlpt_date = date.fromisoformat(str(last_tlpt))
    next_due = last_tlpt_date + relativedelta(years=TLPT_CYCLE_YEARS)

    assert reference_date <= next_due, (
        f"TLPT last completed {last_tlpt_date}; next due by {next_due}; "
        f"current date {reference_date} is past due"
    )
    assert tlpt.get("competent_authority_confirmation"), (
        "Art. 26(7): TLPT results must be shared with the competent authority; "
        "no confirmation of submission found"
    )
```

---

## Pillar 4 — ICT Third-Party Risk Management (Art. 28–30)

### Register of ICT third-party arrangements (Pattern 1 — DETERMINISTIC)

```python
def test_ict_tpsp_register_exists_and_current(
    controls_evidence: dict,
    reference_date: date,
):
    """
    Art. 28(3): All financial entities must maintain a register of all ICT
    third-party service provider arrangements. Register must be kept current.
    """
    tpsp_register = controls_evidence.get("dora_tpsp_register", {})
    assert tpsp_register, "Art. 28(3): No ICT TPSP register found in evidence"
    assert tpsp_register.get("arrangements"), "TPSP register is empty"

    last_updated = tpsp_register.get("last_updated")
    assert last_updated, "TPSP register lacks a last-updated date"
    age = (reference_date - date.fromisoformat(str(last_updated))).days / 30.44
    assert age <= TPSP_REGISTER_REVIEW_MONTHS, (
        f"TPSP register last updated {age:.0f} months ago "
        f"(threshold: {TPSP_REGISTER_REVIEW_MONTHS} months)"
    )
```

### Pre-contractual assessment for new ICT service providers (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-DORA-CTPP-001",
    description=(
        "Critical or important function designation is a management determination; "
        "adequacy of the designation process is Pattern 3."
    ),
    approved_by="CRO",
    review_date="2027-01",
)
def test_pre_contractual_ict_risk_assessment_performed(
    controls_evidence: dict,
):
    """
    Art. 29: Before engaging an ICT service provider for critical or important
    functions, a pre-contractual ICT risk assessment must be performed.
    """
    tpsp_register = controls_evidence.get("dora_tpsp_register", {})
    arrangements = tpsp_register.get("arrangements", []) if tpsp_register else []

    critical_arrangements = [
        a for a in arrangements
        if a.get("supports_critical_or_important_function", False)
    ]
    if not critical_arrangements:
        pytest.skip("No arrangements for critical/important functions — Art. 29 assessment not triggered")

    missing_assessment = [
        a.get("provider_name", "unnamed")
        for a in critical_arrangements
        if not a.get("pre_contractual_assessment_date")
    ]
    assert not missing_assessment, (
        f"Art. 29: ICT service providers supporting critical/important functions "
        f"without pre-contractual risk assessment: {missing_assessment}"
    )
```

### Art. 30(2) — mandatory contract elements (Pattern 1 — DETERMINISTIC)

```python
def test_ict_contracts_contain_all_art30_mandatory_elements(
    controls_evidence: dict,
):
    """
    Art. 30(2): All contracts with ICT service providers supporting critical or
    important functions must contain 12 mandatory elements.
    DETERMINISTIC: all 12 must be present; absence of any element is a violation.
    """
    tpsp_register = controls_evidence.get("dora_tpsp_register", {})
    arrangements = tpsp_register.get("arrangements", []) if tpsp_register else []

    critical_arrangements = [
        a for a in arrangements
        if a.get("supports_critical_or_important_function", False)
    ]
    if not critical_arrangements:
        pytest.skip("No critical/important function arrangements — Art. 30(2) not triggered")

    violations = []
    for arrangement in critical_arrangements:
        name = arrangement.get("provider_name", "unnamed")
        contract_elements = frozenset(arrangement.get("contract_elements", []))
        missing = ART_30_MANDATORY_ELEMENTS - contract_elements
        if missing:
            violations.append(f"'{name}': missing elements {missing}")

    assert not violations, (
        f"Art. 30(2): ICT contracts missing mandatory elements: {'; '.join(violations)}"
    )
```

---

## Open assumptions

| ID | Assumption | Pattern | Approved | Review |
|---|---|---|---|---|
| ASSUME-DORA-INC-001 | Art. 19 initial notification: both the 4-hour clock (from classification) and the 24-hour clock (from awareness) run independently; the earlier deadline governs; if classification_datetime is within 4h of awareness, the 4-hour clock becomes binding faster | 1 | Pending | 2027-01 |
| ASSUME-DORA-INC-002 | "Classification as major" is a documented management decision; classification_datetime must be a separate timestamp from awareness_datetime; delay of the classification decision beyond 24h of awareness does not extend the initial notification deadline — the 24h awareness clock is a hard outer limit | 1 | Pending | 2027-01 |
| ASSUME-DORA-CTPP-001 | "Critical or important function" designation per Art. 3(22) is a management determination; entity's documented function register is the authoritative source; adequacy of designation criteria is Pattern 3 requiring CRO / senior management sign-off | 3 | Pending | 2027-01 |
| ASSUME-DORA-TLPT-001 | TLPT 3-year cycle resets from the TLPT completion date (not from designation date); TIBER-EU framework governs methodology; competent authority notification required per Art. 26(7) | 1 | Pending | 2027-01 |
| ASSUME-DORA-TEST-001 | "At least annually" for basic resilience testing (Art. 25) = within 12 calendar months of prior test completion date; testing components must include all four required types | 1 | Pending | 2027-01 |
| ASSUME-DORA-BACKUP-001 | RTO/RPO are documented in BCP; "achievable" is demonstrated by annual backup restore test; test must record actual recovery time; failure to meet RTO in the test is a DETERMINISTIC violation | 1 | Pending | 2027-01 |
