# NRC 10 CFR Part 50 — Event Reporting: §50.72 and §50.73

**Registry path:** `/regulation-registry/NRC/10CFR50/EventReporting/`
**Regulation:** 10 CFR §50.72 (immediate notification), §50.73 (Licensee Event Reports)
**Last parsed:** 2026-05-21
**Applies to:** Commercial nuclear power plant licensees holding operating licenses (OL) or combined licenses (COL) under 10 CFR Part 50 or Part 52; construction permit holders; nuclear power plant applicants during the licensing process
**Trigger:** NRC license to operate or construct a commercial nuclear power plant in the United States; Appendix B (QA) applies from earliest design phases; event reporting, maintenance rule, fire protection, and ISI/IST requirements apply throughout the operating license period
**Jurisdiction:** United States; enforced by the U.S. Nuclear Regulatory Commission through routine inspections, resident inspectors, and enforcement actions including Notices of Violation, Confirmatory Action Letters, and civil penalties
**Not applicable to:** Research and test reactors (10 CFR Part 50 applies partially but with different technical requirements); non-power utilization facilities; fuel cycle facilities (10 CFR Part 70); nuclear materials licensees; decommissioned reactors (10 CFR Part 50 Subpart E DECON/SAFSTOR requirements differ)
**Overall confidence:** HIGH — all primary obligations have bright-line time thresholds; awareness determination is the only PARAMETERIZED element
**Covers:** §50.72(a) emergency class notifications (1 hour); §50.72(b)(2) 4-hour notifications; §50.72(b)(3) 8-hour notifications; §50.72(b)(4) 24-hour notifications; §50.73 Licensee Event Reports (60 days)

---

## Scope Pre-Condition

```python
@pytest.fixture(autouse=True)
def require_nrc_licensed_reactor(facility_scope: dict):
    if not facility_scope.get("is_nrc_licensed_nuclear_facility"):
        pytest.skip("Facility is not an NRC-licensed nuclear reactor — tests not applicable")
```

---

## §50.72(a) — Emergency Class Notification (DETERMINISTIC — 1 hour)

### Source excerpt

> **§50.72(a)(1):** Each nuclear power reactor licensee shall notify the NRC Operations Center as soon as practical and in all cases within one hour after the declaration of any of the following emergency classes as specified in the emergency plan:
> Emergency Class: (i) General Emergency; (ii) Site Area Emergency; (iii) Alert; (iv) Notification of Unusual Event.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Any emergency class is declared per the approved Emergency Plan | DETERMINISTIC |
| Obligation | Notify NRC Operations Center within 1 hour of declaration | DETERMINISTIC |
| Recipients | NRC Operations Center (primary); applicable state and local authorities per Emergency Plan | DETERMINISTIC |
| Method | Emergency Notification System (ENS) telephone; backup: commercial telephone | DETERMINISTIC |
| Evidence | Emergency declaration log; ENS notification timestamp | DETERMINISTIC |

### Emergency class definitions (per 10 CFR 50 Appendix E)

| Class | Activation threshold (summary) | Example initiating events |
|---|---|---|
| **Notification of Unusual Event (NOUE)** | Events that indicate potential degradation of safety — no immediate threat | Loss of communications, minor fire, security threat |
| **Alert** | Actual or potential substantial degradation of plant safety | Reactor trip with complications, site boundary radiation approaching limit |
| **Site Area Emergency (SAE)** | Actual or likely major failures of plant safety functions | Loss of cooling to reactor core, uncontrolled radiation release on-site |
| **General Emergency (GE)** | Actual or imminent substantial core damage | Core damage, radiation release off-site requiring protective action |

**Assumption (ASSUME-NRC50-EVTRPT-001):** Emergency class notification is compliant when: (1) notification made to NRC Operations Center within 1 hour of declaration — clock starts at declaration, not at initiating event; (2) notification made via ENS hotline (1-301-816-5100 primary); (3) notification content includes: plant name, reactor unit, emergency class, initiating event, plant status, meteorological conditions (for Site Area and General Emergency), protective actions taken or planned; (4) state and local emergency response organizations (EROs) notified per the approved Emergency Plan; (5) notification log entry created with actual ENS call time.

**Overall: DETERMINISTIC → Pattern 1**

---

## §50.72(b)(2) — 4-Hour Notifications (DETERMINISTIC)

### Source excerpt

> **§50.72(b)(2):** The licensee shall notify the NRC Operations Center within 4 hours of the occurrence of any of the following:
> (i) A reactor trip that was not caused by normal test or surveillance activities;
> (ii) Actuation of any of the safety systems...when the actuation is not the result of normal test or surveillance;
> (iii) [Various other listed conditions including loss of safety function]

### Key 4-hour reportable conditions

| Condition | Classification |
|---|---|
| Reactor trip (non-test) | DETERMINISTIC — binary: trip occurred or not |
| ECCS actuation (non-test) | DETERMINISTIC |
| Reactor Protection System (RPS) actuation resulting in reactor trip | DETERMINISTIC |
| Loss of safety function affecting emergency core cooling | DETERMINISTIC |
| Offsite notification required per §50.72(a) if not already covered | DETERMINISTIC |
| Exceeding any technical specification action level requiring a plant shutdown or power reduction | DETERMINISTIC |

**Assumption (ASSUME-NRC50-EVTRPT-002):** 4-hour notification compliance: (1) clock starts when the licensee becomes aware — defined as when the Shift Manager or equivalent licensed individual has knowledge of the reportable condition; (2) conditions in §50.72(b)(2)(i)–(xi) evaluated within each operating shift; (3) 4-hour notification call to NRC Operations Center with: condition description, time of occurrence, time of awareness, current plant status; (4) supplemental information provided as it becomes available; (5) Technical Specification surveillance-triggered trips are excluded from 4-hour reporting but must still be evaluated for §50.73 LER applicability.

**Overall: DETERMINISTIC → Pattern 1**

---

## §50.72(b)(3) — 8-Hour Notifications (DETERMINISTIC)

### Source excerpt

> **§50.72(b)(3):** The licensee shall notify the NRC Operations Center within 8 hours of discovery of:
> Any event or condition that resulted in the nuclear power plant being in an unanalyzed condition that significantly compromised plant safety, or...

### Key 8-hour reportable conditions

| Condition | Notes |
|---|---|
| Unanalyzed condition significantly compromising plant safety | Requires engineering evaluation — discovery-to-reporting triggers 8-hour clock |
| Degraded or non-conforming condition that does not meet 4-hour criteria | Engineering review typically required |
| Entry into Technical Specification LCO action condition where required action is not completed within the completion time | Condition-dependent |

**Overall: DETERMINISTIC for clock → Pattern 1; PARAMETERIZED for "unanalyzed condition" determination → Pattern 2**

---

## §50.73 — Licensee Event Report (DETERMINISTIC — 60 days)

### Source excerpt

> **§50.73(a)(1):** The licensee shall submit a Licensee Event Report (LER) for any event of the type described in paragraph (a)(2) of this section within 60 days after the discovery of the event.
>
> **§50.73(a)(2):** A licensee shall report each of the following: (i) Any event that required the activation of the Emergency Response Organization (ERO)... (ii) Any operation or condition which was prohibited by the plant's Technical Specifications...

### §50.73(a)(2) LER-triggering conditions (summary)

| Condition | Classification |
|---|---|
| Operation prohibited by Technical Specifications | DETERMINISTIC (TS violation is binary) |
| A Safety System Actuation (not test or surveillance) | DETERMINISTIC |
| An event that could have prevented fulfillment of a safety function | PARAMETERIZED |
| A common cause failure or personnel error that directly affects safety | PARAMETERIZED |
| Exceeding a safety limit | DETERMINISTIC |
| An event where NRC was notified under §50.72 | DETERMINISTIC (all §50.72 events generate LERs) |

### LER content requirements (§50.73(b))

| Required element | Classification |
|---|---|
| Facility and unit identification | DETERMINISTIC |
| Event date and discovery date | DETERMINISTIC |
| Event description (chronological) | PARAMETERIZED |
| Cause of event | PARAMETERIZED (root cause) |
| Assessment of safety significance | PARAMETERIZED |
| Corrective actions taken | PARAMETERIZED |
| Previous similar events (3-year lookback) | PARAMETERIZED |
| Signature of senior plant official | DETERMINISTIC |

**Assumption (ASSUME-NRC50-EVTRPT-003):** LER compliance is demonstrated when: (1) LER submitted within 60 days of discovery — discovery is when the Shift Manager or Plant Nuclear Safety Officer has knowledge sufficient to make a reportability determination; (2) LER submitted via NRC's document management system (ADAMS) in required format (NUREG-1022 guidance); (3) if original LER was incomplete, supplement submitted within 30 days; (4) all §50.72 notifications result in a corresponding LER unless the 4-hour/8-hour condition resolves without a §50.73 triggering event; (5) LER tracking system captures: discovery date, 60-day due date, submission date, ADAMS accession number.

**Assumption (ASSUME-NRC50-EVTRPT-004):** Discovery timing: the NRC defines "discovery" in Inspection Procedure 92703 as the time when the licensee's responsible personnel have sufficient knowledge of the facts to make a reportability determination. This is not necessarily when the event occurred. It is also not extended by the duration of an engineering evaluation — the obligation to report exists once the facts are sufficiently known, even if root cause is incomplete.

**Overall: DETERMINISTIC for 60-day deadline → Pattern 1; PARAMETERIZED for "discovery" determination → Pattern 2**

---

## Test specifications

### YAML spec — NRC event reporting

```yaml
spec_id: NRC-50-EVTRPT-001
framework: NRC 10 CFR Part 50
sections:
  - §50.72(a) (emergency class, 1 hour)
  - §50.72(b)(2) (4-hour notifications)
  - §50.72(b)(3) (8-hour notifications)
  - §50.73 (LER, 60 days)
pattern: 1  # Primary; Pattern 2 for discovery determination
applicable: NRC-licensed nuclear power reactor licensees
evidence:
  - emergency_log (declaration timestamp, ENS call timestamp, class, initiating event)
  - nrc_notifications_log (event ID, condition type, awareness time, notification time, content)
  - ler_tracking_system (event ID, discovery date, 60-day due, submission date, ADAMS number, supplement status)
```

### Python test file

```python
# tests/nrc_10cfr50/test_event_reporting.py
"""
NRC 10 CFR Part 50 — §50.72 and §50.73 Event Reporting Tests.

Sections: §50.72(a), §50.72(b)(2), §50.72(b)(3), §50.73
Assumptions: ASSUME-NRC50-EVTRPT-001 through ASSUME-NRC50-EVTRPT-004
"""
import pytest
from datetime import datetime, timedelta, timezone
from typing import Any

EMERGENCY_CLASS_NOTIFY_MAX_SECONDS = 3600        # 1 hour
FOUR_HOUR_NOTIFY_MAX_SECONDS = 4 * 3600
EIGHT_HOUR_NOTIFY_MAX_SECONDS = 8 * 3600
LER_SUBMISSION_MAX_DAYS = 60
LER_SUPPLEMENT_MAX_DAYS = 30

EMERGENCY_CLASSES = {"notification_of_unusual_event", "alert", "site_area_emergency", "general_emergency"}
FOUR_HOUR_CONDITIONS = {
    "reactor_trip_non_test",
    "eccs_actuation_non_test",
    "rps_actuation_non_test",
    "loss_of_safety_function",
    "technical_specification_action_level_shutdown",
}


@pytest.fixture(autouse=True)
def require_nrc_licensed_reactor(facility_scope: dict[str, Any]):
    """Gate: tests apply only to NRC-licensed nuclear power reactors."""
    if not facility_scope.get("is_nrc_licensed_nuclear_facility"):
        pytest.skip("Facility is not an NRC-licensed nuclear reactor — tests not applicable")


# ── §50.72(a): Emergency Class Notifications ──────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-NRC50-EVTRPT-001",
    description="Emergency class notifications to NRC Operations Center within 1 hour of declaration",
    approved_by="Shift Manager / Emergency Response Organization",
    review_date="2027-05-21",
)
def test_emergency_class_notifications_within_1_hour(emergency_log: list[dict[str, Any]]):
    """§50.72(a): Emergency class declarations must be reported to NRC within 1 hour."""
    late_notifications = []

    for event in emergency_log:
        if event.get("emergency_class", "").lower() not in EMERGENCY_CLASSES:
            continue

        declaration_ts = event.get("declaration_timestamp")
        ens_call_ts = event.get("nrc_ens_notification_timestamp")

        if declaration_ts is None:
            continue
        if ens_call_ts is None:
            elapsed = (datetime.now(timezone.utc) - declaration_ts).total_seconds()
            if elapsed > EMERGENCY_CLASS_NOTIFY_MAX_SECONDS:
                late_notifications.append(
                    f"{event['event_id']} ({event.get('emergency_class')}): "
                    f"no NRC notification recorded {elapsed / 3600:.1f}h after declaration"
                )
        else:
            elapsed = (ens_call_ts - declaration_ts).total_seconds()
            if elapsed > EMERGENCY_CLASS_NOTIFY_MAX_SECONDS:
                late_notifications.append(
                    f"{event['event_id']} ({event.get('emergency_class')}): "
                    f"NRC notified {elapsed / 60:.1f} min after declaration "
                    f"(max {EMERGENCY_CLASS_NOTIFY_MAX_SECONDS / 60:.0f} min)"
                )

    assert not late_notifications, (
        f"§50.72(a) emergency class notification timing violations: {late_notifications}"
    )


# ── §50.72(b)(2): 4-Hour Notifications ────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-NRC50-EVTRPT-002",
    description="4-hour notification conditions: clock starts at awareness; includes reactor trips, ECCS actuations",
    approved_by="Shift Manager",
    review_date="2027-05-21",
)
def test_four_hour_notifications_within_4_hours(
    nrc_notifications_log: list[dict[str, Any]],
):
    """§50.72(b)(2): 4-hour reportable conditions must be notified to NRC within 4 hours of awareness."""
    late = []

    for record in nrc_notifications_log:
        if record.get("notification_type") not in {"four_hour", "section_50_72_b_2"}:
            continue
        condition = record.get("condition_type", "")
        if condition not in FOUR_HOUR_CONDITIONS and not record.get("manually_classified_4hr"):
            continue

        awareness_ts = record.get("awareness_timestamp")
        notification_ts = record.get("nrc_notification_timestamp")

        if awareness_ts is None:
            continue
        if notification_ts is None:
            elapsed = (datetime.now(timezone.utc) - awareness_ts).total_seconds()
            if elapsed > FOUR_HOUR_NOTIFY_MAX_SECONDS:
                late.append(
                    f"{record['event_id']}: no notification {elapsed / 3600:.1f}h after awareness "
                    f"(max 4h)"
                )
        else:
            elapsed = (notification_ts - awareness_ts).total_seconds()
            if elapsed > FOUR_HOUR_NOTIFY_MAX_SECONDS:
                late.append(
                    f"{record['event_id']}: notified {elapsed / 3600:.1f}h after awareness (max 4h)"
                )

    assert not late, f"§50.72(b)(2) 4-hour notification timing violations: {late}"


# ── §50.73: Licensee Event Reports ────────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-NRC50-EVTRPT-003",
    description="LER submitted within 60 days of discovery; supplemented within 30 days if incomplete",
    approved_by="Licensing Manager",
    review_date="2027-05-21",
)
def test_ler_submitted_within_60_days(ler_tracking: list[dict[str, Any]]):
    """§50.73(a)(1): Licensee Event Reports must be submitted within 60 days of discovery."""
    late = []

    for ler in ler_tracking:
        discovery_date = ler.get("discovery_date")
        submission_date = ler.get("submission_date")

        if discovery_date is None:
            continue
        if submission_date is None:
            days_since = (datetime.now(timezone.utc) - discovery_date).days
            if days_since > LER_SUBMISSION_MAX_DAYS:
                late.append(
                    f"LER {ler.get('event_id', '?')}: not submitted {days_since}d after discovery "
                    f"(max {LER_SUBMISSION_MAX_DAYS}d)"
                )
        else:
            days_elapsed = (submission_date - discovery_date).days
            if days_elapsed > LER_SUBMISSION_MAX_DAYS:
                late.append(
                    f"LER {ler.get('event_id', '?')}: submitted {days_elapsed}d after discovery "
                    f"(max {LER_SUBMISSION_MAX_DAYS}d)"
                )

    assert not late, f"§50.73 LER submission timing violations: {late}"


@pytest.mark.assumption(
    id="ASSUME-NRC50-EVTRPT-003",
    description="Supplemental LERs submitted within 30 days when original was incomplete",
    approved_by="Licensing Manager",
    review_date="2027-05-21",
)
def test_ler_supplements_within_30_days(ler_tracking: list[dict[str, Any]]):
    """§50.73: Supplemental LERs must be submitted within 30 days of the original LER."""
    late_supplements = []

    for ler in ler_tracking:
        if not ler.get("supplement_required"):
            continue
        original_submission = ler.get("submission_date")
        supplement_date = ler.get("supplement_submission_date")

        if original_submission is None:
            continue
        if supplement_date is None:
            days_since = (datetime.now(timezone.utc) - original_submission).days
            if days_since > LER_SUPPLEMENT_MAX_DAYS:
                late_supplements.append(
                    f"LER {ler.get('event_id', '?')}: supplement required but not submitted "
                    f"{days_since}d after original (max {LER_SUPPLEMENT_MAX_DAYS}d)"
                )
        else:
            days_elapsed = (supplement_date - original_submission).days
            if days_elapsed > LER_SUPPLEMENT_MAX_DAYS:
                late_supplements.append(
                    f"LER {ler.get('event_id', '?')}: supplement {days_elapsed}d after original "
                    f"(max {LER_SUPPLEMENT_MAX_DAYS}d)"
                )

    assert not late_supplements, f"§50.73 LER supplement timing violations: {late_supplements}"


def test_all_50_72_notifications_have_ler_evaluated(
    nrc_notifications_log: list[dict[str, Any]],
    ler_tracking: list[dict[str, Any]],
):
    """§50.73: Every §50.72 notification must be evaluated for §50.73 LER reportability."""
    ler_events = {ler.get("source_event_id") for ler in ler_tracking}
    missing_ler_eval = []

    for notification in nrc_notifications_log:
        event_id = notification.get("event_id")
        if event_id in ler_events:
            continue
        if notification.get("ler_reportability_evaluated"):
            continue
        if notification.get("ler_not_required_documented"):
            continue
        missing_ler_eval.append(
            f"{event_id}: §50.72 notification with no §50.73 LER evaluation documented"
        )

    assert not missing_ler_eval, (
        f"§50.72 notifications without documented §50.73 LER reportability evaluation: "
        f"{missing_ler_eval}"
    )
```
