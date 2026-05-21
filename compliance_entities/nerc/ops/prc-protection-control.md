# NERC Non-CIP — PRC: Protection and Control Standards

**Registry path:** `/regulation-registry/NERC-OPS/PRC/`
**Standards:** PRC-005-6, PRC-004-5, PRC-023-4, PRC-024-2
**Last parsed:** 2026-05-21
**Overall confidence:** HIGH for PRC-005-6 (explicit maintenance intervals in Table 1) and PRC-004-5 (120-day evaluation window); MEDIUM for PRC-023-4 and PRC-024-2 (relay settings adequacy is engineering-judgment-based)
**Applicable entities:** Transmission Owners (TO), Generator Owners (GO), Distribution Providers (DP) with protection systems on BES facilities

---

## Applicability Fixture

```python
@pytest.fixture(autouse=True)
def require_bes_protection_system_owner(entity_scope: dict):
    if not entity_scope.get("owns_bes_protection_systems"):
        pytest.skip("Entity does not own BES protection systems — PRC tests not applicable")
```

---

## PRC-005-6 — Protection System Maintenance (HIGH — DETERMINISTIC for intervals)

### Source excerpts

> **R1.** Each Transmission Owner, Generator Owner, and Distribution Provider that owns a protection system shall have a protection system maintenance program (PSMP) that includes the maintenance intervals and maintenance activities for each of the protection system component types listed in Table 1 of PRC-005-6.
>
> **R3.** Each Transmission Owner, Generator Owner, and Distribution Provider shall implement its PSMP such that all components are maintained within the maximum maintenance intervals specified in Table 1 of PRC-005-6.

### Table 1 maximum maintenance intervals — key component types

The following intervals are drawn from PRC-005-6 Table 1. These are **maximum** intervals — entities may maintain more frequently.

#### Table 1a — Components with explicit maximum intervals (flooded lead-acid batteries)

| Activity | Maximum interval |
|---|---|
| Battery visual inspection (terminals, electrolyte level, case condition) | 18 calendar months |
| Battery service test (capacity at normal load) | 18 calendar months |
| Battery performance/modified performance test (capacity at 25°C) | Initial: 18 calendar months; subsequent: 3 calendar years after satisfactory performance test; sooner if 80% of expected life reached |

#### Table 1b — Valve-regulated lead-acid (VRLA/sealed) batteries

| Activity | Maximum interval |
|---|---|
| Battery visual inspection | 18 calendar months |
| Battery impedance or conductance test (per manufacturer) | 18 calendar months |
| Battery service test | 18 calendar months |
| Battery performance/modified performance test | Initial: 18 calendar months; subsequent: 3 calendar years |

#### Table 1 — Protection system components (general)

| Component type | Maximum interval | Notes |
|---|---|---|
| DC supply (battery/charger) | Per Table 1a/1b above | Most DETERMINISTIC element of PRC-005 |
| Protective relay (electromechanical/solid-state, trip function) | 6 calendar years | Includes checking output contacts, trip path |
| Protective relay (microprocessor-based, trip function) | 12 calendar years | Verification may be via self-diagnostics + periodic test |
| Communications systems (for protective relaying) | 6 calendar years | Channel test, end-to-end verification |
| Control circuitry (trip path from relay output to breaker trip coil) | 6 calendar years | Includes wiring, output contacts, auxiliary relays |
| Voltage and current sensing devices (CTs, PTs) | 12 calendar years | Ratio test or calibration check |
| Sudden pressure relays | 6 calendar years | Functional test of trip mechanism |

**Assumption (ASSUME-NERC-PRC-001):** Battery maintenance compliance is demonstrated when: (1) each battery string has documented inspection records within 18 calendar months; (2) service test records within 18 calendar months; (3) initial performance test within 18 months of installation; (4) subsequent performance tests within 3 calendar years of the previous satisfactory test — or sooner if battery has reached 80% of expected life per manufacturer specification; (5) VRLA batteries: impedance/conductance test records within 18 months; (6) test results include pass/fail determination against acceptance criteria; (7) failed batteries trigger corrective action documented in the PSMP.

**Assumption (ASSUME-NERC-PRC-002):** Protection system component maintenance compliance is demonstrated when: (1) each component is mapped to a component type in the PSMP; (2) maintenance activities match or exceed the scope listed in Table 1 for that component type; (3) last maintenance date recorded per component; (4) next scheduled maintenance does not exceed the maximum interval from the last completed maintenance date; (5) where microprocessor relays use self-diagnostics in lieu of periodic trip testing, the self-diagnostic capability is verified to detect the failure modes covered by the periodic test — documented in the PSMP.

**Overall: DETERMINISTIC → Pattern 1 (interval compliance); PARAMETERIZED for self-diagnostic substitution → Pattern 2**

---

## PRC-004-5 — Protection System Misoperation Identification and Correction (DETERMINISTIC)

### Source excerpt

> **R1.** Each Transmission Owner, Generator Owner, and Distribution Provider that owns a protection system that misoperates shall investigate the cause of each misoperation. The investigation shall begin within 120 days of the entity becoming aware that a misoperation has occurred.
>
> **R2.** Each entity that identifies a misoperation shall report the misoperation to its Regional Entity within 120 days of becoming aware of the misoperation.

### Misoperation definition

A **misoperation** is any relay operation that is not the expected, intended response to a fault or abnormal condition. Includes:
- **False trip:** Relay operated when it should not have (breaker opened without cause)
- **Failure to trip:** Relay did not operate when it should have (fault not cleared)
- **Slow operation:** Relay operated, but outside its designed operating time

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Protection system operation that is not the intended response | DETERMINISTIC (trigger) / PARAMETERIZED (definition of "intended") |
| Obligation — investigation | Begin within 120 days of becoming aware | DETERMINISTIC |
| Obligation — reporting | Report to Regional Entity within 120 days of becoming aware | DETERMINISTIC |
| Evidence | Misoperation log with awareness date, investigation start date, RE report date | DETERMINISTIC |

**Assumption (ASSUME-NERC-PRC-003):** Misoperation identification and reporting is compliant when: (1) post-event analysis triggered for every protection system operation — both expected and unexpected; (2) misoperation classification made within the 120-day window; (3) investigation documentation includes: event timeline, relay targets, fault recorder data (if available), cause determination, and corrective action plan; (4) RE report submitted within 120 days using the applicable RE template or OE event reporting form; (5) corrective action tracked to completion with verification test where applicable.

**Overall: DETERMINISTIC → Pattern 1**

---

## PRC-023-4 — Transmission Relay Loadability (PARAMETERIZED)

### Source excerpt

> **R1.** Each Transmission Owner shall verify that its phase protective relay settings do not expose BES elements to an unacceptable risk of the protection system incorrectly operating at loadings up to 150% of the Emergency Rating or the applicable line thermal limit.

### Classification

Relay loadability is PARAMETERIZED because compliance depends on the specific relay characteristics, equipment ratings, and loading profiles — no single universal threshold applies. The 150% Emergency Rating is the test boundary, but whether a relay can withstand loading to that level depends on engineering calculations specific to each relay and line.

**Assumption (ASSUME-NERC-PRC-004):** Relay loadability compliance is demonstrated when: (1) relay settings reviewed when equipment ratings change; (2) for each phase relay: impedance characteristic plotted against applicable load flow conditions up to 150% Emergency Rating; (3) if relay characteristic encroaches on load area, corrective action taken per PRC-023 Table 1 remediation options; (4) relay loadability study documented and retained; (5) annual review of settings versus current equipment ratings.

**Overall: PARAMETERIZED → Pattern 2**

---

## PRC-024-2 — Generator Frequency and Voltage Protective Relay Settings (PARAMETERIZED)

### Source excerpt

> **R1.** Each Generator Owner shall set its generator's frequency protective relays within the no-trip zone in Figure 1 or Table 1 of PRC-024-2.

### No-trip zone (key thresholds from Figure 1)

| Frequency range | Required duration generators must not trip |
|---|---|
| 59.5 Hz to 60.5 Hz | Indefinite (normal operation) |
| 58.5 Hz to 59.5 Hz | ≥ 3 minutes |
| 58.0 Hz to 58.5 Hz | ≥ 30 seconds |
| 57.0 Hz to 58.0 Hz | ≥ 7.5 seconds |
| < 57.0 Hz or > 61.7 Hz | Relay may trip — beyond no-trip zone |

**Overall: PARAMETERIZED for relay setting adequacy → Pattern 2; DETERMINISTIC for no-trip zone boundary → Pattern 1**

---

## Test specifications

### YAML spec — PRC protection and control

```yaml
spec_id: NERC-PRC-001
framework: NERC Non-CIP
category: PRC
standards:
  - PRC-005-6
  - PRC-004-5
  - PRC-023-4
  - PRC-024-2
pattern: 1  # PRC-005 intervals and PRC-004 deadlines; Pattern 2 for relay settings
applicable_entities:
  - Transmission Owner (TO)
  - Generator Owner (GO)
  - Distribution Provider (DP — BES protection systems only)
evidence:
  - protection_system_inventory (component list, types, ownership)
  - psmp_document (program document with maintenance activities and intervals)
  - battery_maintenance_records (inspection, service test, performance test dates)
  - protection_system_maintenance_records (per component, per activity, dates)
  - misoperation_log (event ID, awareness date, investigation start, RE report date, cause, corrective action)
  - relay_loadability_studies (per relay, equipment ratings, impedance plots)
  - generator_relay_settings (frequency relay settings vs. PRC-024 no-trip zone)
```

### Python test file

```python
# tests/nerc_ops/test_prc_protection_control.py
"""
NERC Non-CIP — PRC Protection and Control Standards.

Standards: PRC-005-6, PRC-004-5, PRC-023-4, PRC-024-2
Assumptions: ASSUME-NERC-PRC-001 through ASSUME-NERC-PRC-004
"""
import pytest
from datetime import datetime, timedelta, timezone
from typing import Any

# PRC-005-6 Table 1 maximum intervals
BATTERY_INSPECTION_MAX_MONTHS = 18
BATTERY_SERVICE_TEST_MAX_MONTHS = 18
BATTERY_PERFORMANCE_TEST_INITIAL_MONTHS = 18
BATTERY_PERFORMANCE_TEST_SUBSEQUENT_MONTHS = 36  # 3 calendar years
BATTERY_LIFE_THRESHOLD_PERCENT = 80  # Trigger earlier performance test

ELECTROMECHANICAL_RELAY_MAX_YEARS = 6
MICROPROCESSOR_RELAY_MAX_YEARS = 12
COMMUNICATIONS_MAX_YEARS = 6
CONTROL_CIRCUITRY_MAX_YEARS = 6
SENSING_DEVICE_MAX_YEARS = 12
SUDDEN_PRESSURE_MAX_YEARS = 6

# PRC-004-5
MISOPERATION_EVALUATION_MAX_DAYS = 120
MISOPERATION_RE_REPORT_MAX_DAYS = 120

# PRC-024-2 no-trip zone boundaries (Hz)
NO_TRIP_ZONE = [
    (57.0, 58.0, timedelta(seconds=7.5)),
    (58.0, 58.5, timedelta(seconds=30)),
    (58.5, 59.5, timedelta(minutes=3)),
    (59.5, 61.7, None),  # None = indefinite
]


@pytest.fixture(autouse=True)
def require_bes_protection_owner(entity_scope: dict[str, Any]):
    """Gate: entity must own BES protection systems."""
    if not entity_scope.get("owns_bes_protection_systems"):
        pytest.skip("Entity does not own BES protection systems — PRC tests not applicable")


# ── PRC-005-6: Battery Maintenance ───────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-NERC-PRC-001",
    description="Battery visual inspection ≤18 calendar months; service test ≤18 months",
    approved_by="Protection Engineer",
    review_date="2027-05-21",
)
def test_battery_inspection_within_interval(
    battery_maintenance_records: list[dict[str, Any]],
):
    """PRC-005-6 Table 1a/1b: Battery inspection must occur within 18 calendar months."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=BATTERY_INSPECTION_MAX_MONTHS * 30.44)

    overdue = []
    for battery in battery_maintenance_records:
        last_inspection = battery.get("last_visual_inspection_date")
        if last_inspection is None:
            overdue.append(f"{battery['battery_id']}: no inspection record")
        elif last_inspection < cutoff:
            months_since = (now - last_inspection).days / 30.44
            overdue.append(
                f"{battery['battery_id']}: last inspection {months_since:.1f} months ago "
                f"(max {BATTERY_INSPECTION_MAX_MONTHS} months)"
            )

    assert not overdue, f"Batteries overdue for visual inspection: {overdue}"


@pytest.mark.assumption(
    id="ASSUME-NERC-PRC-001",
    description="Battery performance test: initial ≤18 months; subsequent ≤36 months or sooner at 80% life",
    approved_by="Protection Engineer",
    review_date="2027-05-21",
)
def test_battery_performance_test_within_interval(
    battery_maintenance_records: list[dict[str, Any]],
):
    """PRC-005-6 Table 1a/1b: Battery performance test within maximum intervals."""
    now = datetime.now(timezone.utc)
    overdue = []

    for battery in battery_maintenance_records:
        last_perf_test = battery.get("last_performance_test_date")
        is_initial = not battery.get("initial_performance_test_complete")

        if is_initial:
            max_months = BATTERY_PERFORMANCE_TEST_INITIAL_MONTHS
        else:
            max_months = BATTERY_PERFORMANCE_TEST_SUBSEQUENT_MONTHS
            # Early test required if battery is at 80%+ of expected life
            life_pct = battery.get("life_percentage_used", 0)
            if life_pct >= BATTERY_LIFE_THRESHOLD_PERCENT:
                max_months = BATTERY_INSPECTION_MAX_MONTHS  # Same as inspection cadence

        cutoff = now - timedelta(days=max_months * 30.44)
        if last_perf_test is None:
            overdue.append(f"{battery['battery_id']}: no performance test record (initial required)")
        elif last_perf_test < cutoff:
            months_since = (now - last_perf_test).days / 30.44
            overdue.append(
                f"{battery['battery_id']}: last performance test {months_since:.1f} months ago "
                f"(max {max_months} months)"
            )

    assert not overdue, f"Batteries overdue for performance test: {overdue}"


# ── PRC-005-6: Protection System Component Maintenance ───────────────────────

COMPONENT_MAX_INTERVALS = {
    "electromechanical_relay": timedelta(days=ELECTROMECHANICAL_RELAY_MAX_YEARS * 365),
    "solid_state_relay": timedelta(days=ELECTROMECHANICAL_RELAY_MAX_YEARS * 365),
    "microprocessor_relay": timedelta(days=MICROPROCESSOR_RELAY_MAX_YEARS * 365),
    "communication_system": timedelta(days=COMMUNICATIONS_MAX_YEARS * 365),
    "control_circuitry": timedelta(days=CONTROL_CIRCUITRY_MAX_YEARS * 365),
    "current_transformer": timedelta(days=SENSING_DEVICE_MAX_YEARS * 365),
    "potential_transformer": timedelta(days=SENSING_DEVICE_MAX_YEARS * 365),
    "sudden_pressure_relay": timedelta(days=SUDDEN_PRESSURE_MAX_YEARS * 365),
}


@pytest.mark.assumption(
    id="ASSUME-NERC-PRC-002",
    description="Each protection system component maintained within Table 1 maximum interval",
    approved_by="Protection Engineer",
    review_date="2027-05-21",
)
def test_protection_system_components_maintained_within_interval(
    protection_system_inventory: list[dict[str, Any]],
):
    """PRC-005-6 R3: All protection system components must be maintained within maximum intervals."""
    now = datetime.now(timezone.utc)
    overdue = []

    for component in protection_system_inventory:
        component_type = component.get("component_type", "").lower()
        max_interval = COMPONENT_MAX_INTERVALS.get(component_type)
        if max_interval is None:
            continue  # Unknown type — exclude from automated check

        last_maintenance = component.get("last_maintenance_date")
        if last_maintenance is None:
            overdue.append(
                f"{component['component_id']} ({component_type}): no maintenance record"
            )
        elif last_maintenance < now - max_interval:
            years_since = (now - last_maintenance).days / 365.25
            max_years = max_interval.days / 365.25
            overdue.append(
                f"{component['component_id']} ({component_type}): last maintained "
                f"{years_since:.1f} years ago (max {max_years:.0f} years)"
            )

    assert not overdue, (
        f"Protection system components exceeding PRC-005-6 maximum maintenance intervals: {overdue}"
    )


def test_psmp_document_exists(psmp: dict[str, Any]):
    """PRC-005-6 R1: A written Protection System Maintenance Program must exist."""
    assert psmp.get("exists"), "No Protection System Maintenance Program (PSMP) document found"
    assert psmp.get("includes_component_inventory"), (
        "PSMP must include an inventory of all protection system components"
    )
    assert psmp.get("specifies_maintenance_intervals_by_type"), (
        "PSMP must specify maintenance intervals for each component type"
    )
    assert psmp.get("specifies_maintenance_activities_by_type"), (
        "PSMP must specify maintenance activities for each component type"
    )


# ── PRC-004-5: Misoperation Evaluation ───────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-NERC-PRC-003",
    description="Misoperation investigation started within 120 days; RE report within 120 days",
    approved_by="Protection Engineer",
    review_date="2027-05-21",
)
def test_misoperation_investigations_timely(misoperation_log: list[dict[str, Any]]):
    """PRC-004-5 R1/R2: Misoperation investigation must begin and RE report submitted within 120 days."""
    late = []

    for event in misoperation_log:
        awareness_date = event.get("awareness_date")
        investigation_start = event.get("investigation_start_date")
        re_report_date = event.get("re_report_date")

        if awareness_date is None:
            continue

        if investigation_start is None:
            days_since_awareness = (datetime.now(timezone.utc) - awareness_date).days
            if days_since_awareness > MISOPERATION_EVALUATION_MAX_DAYS:
                late.append(
                    f"{event['event_id']}: no investigation started {days_since_awareness}d "
                    f"after awareness (max {MISOPERATION_EVALUATION_MAX_DAYS}d)"
                )
        else:
            investigation_delay = (investigation_start - awareness_date).days
            if investigation_delay > MISOPERATION_EVALUATION_MAX_DAYS:
                late.append(
                    f"{event['event_id']}: investigation started {investigation_delay}d after awareness"
                )

        if re_report_date is None:
            days_since = (datetime.now(timezone.utc) - awareness_date).days
            if days_since > MISOPERATION_RE_REPORT_MAX_DAYS:
                late.append(
                    f"{event['event_id']}: no RE report filed {days_since}d after awareness "
                    f"(max {MISOPERATION_RE_REPORT_MAX_DAYS}d)"
                )
        else:
            report_delay = (re_report_date - awareness_date).days
            if report_delay > MISOPERATION_RE_REPORT_MAX_DAYS:
                late.append(
                    f"{event['event_id']}: RE report filed {report_delay}d after awareness "
                    f"(max {MISOPERATION_RE_REPORT_MAX_DAYS}d)"
                )

    assert not late, f"PRC-004-5 misoperation evaluation/reporting violations: {late}"


# ── PRC-024-2: Generator Frequency Relay Settings ────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-NERC-PRC-004",
    description="Generator frequency relays set within PRC-024-2 no-trip zone (Figure 1)",
    approved_by="Protection Engineer",
    review_date="2027-05-21",
)
def test_generator_frequency_relay_settings_within_no_trip_zone(
    generator_relay_settings: list[dict[str, Any]],
):
    """PRC-024-2 R1: Generator frequency protective relay settings must be within the no-trip zone."""
    violations = []

    for gen in generator_relay_settings:
        for relay in gen.get("frequency_relays", []):
            trip_freq_hz = relay.get("underfrequency_trip_setpoint_hz")
            trip_time_s = relay.get("trip_time_seconds")
            if trip_freq_hz is None:
                continue

            # Check if trip setpoint is within the no-trip zone
            for low_hz, high_hz, required_duration in NO_TRIP_ZONE:
                if low_hz <= trip_freq_hz < high_hz and required_duration is not None:
                    relay_duration = timedelta(seconds=trip_time_s or 0)
                    if relay_duration < required_duration:
                        violations.append(
                            f"{gen['generator_id']} relay {relay['relay_id']}: "
                            f"trips at {trip_freq_hz}Hz in {trip_time_s}s — "
                            f"PRC-024-2 requires ≥{required_duration.total_seconds()}s in this range"
                        )

    assert not violations, (
        f"Generator frequency relay settings not within PRC-024-2 no-trip zone: {violations}"
    )
```
