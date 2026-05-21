# NERC Non-CIP — FAC, EOP, NUC: Facility Ratings, Vegetation, Event Reporting, Nuclear Interface

**Registry path:** `/regulation-registry/NERC-OPS/FAC-EOP-NUC/`
**Standards:** FAC-003-4 (vegetation management), FAC-008-3 (facility ratings), EOP-004-4 (event reporting), NUC-001-4 (nuclear interface)
**Last parsed:** 2026-05-21
**Applies to:** Bulk Electric System registered entities whose functional registration makes them subject to specific operational reliability standards — Transmission Operators, Balancing Authorities, Generator Operators, Reliability Coordinators, and others per NERC functional model
**Trigger:** NERC registration as one or more functional entities per the NERC Functional Model; specific standards apply based on functional registration (e.g., COM-001 applies to Transmission Operators and Balancing Authorities but not Generator Owners)
**Jurisdiction:** Same as NERC CIP — North America BES; enforced by NERC Regional Entities and FERC
**Not applicable to:** Same as NERC CIP — distribution-only utilities, behind-the-meter generation, unregistered entities; specific standards have applicability sections listing which functional entities are subject
**Overall confidence:** HIGH for FAC-003 vegetation patrol cadence and EOP-004 reporting timelines; MEDIUM for FAC-008 ratings methodology; PARAMETERIZED for NUC-001 interface agreement adequacy
**Applicable entities:** FAC-003: Transmission Owners (lines ≥200kV + select lower voltage); FAC-008: TO/GO; EOP-004: RC/TOP/BA/GO/GOP/TO/DP (per Table 1); NUC-001: TO/TOP/BA/RC and nuclear plant GO/GOP

---

## FAC-003-4 — Transmission Vegetation Management (HIGH — DETERMINISTIC for patrol cadence)

### Source excerpts

> **R1.** Each Transmission Owner shall manage vegetation to prevent encroachment into the MVCD of its applicable transmission lines, consistent with its documented maintenance strategy, work methods, and control techniques.
>
> **R2.** Each Transmission Owner shall complete a patrol of each of its applicable transmission lines at least once per calendar year to observe vegetation conditions.

### MVCD — Minimum Vegetation Clearance Distance

The MVCD is the air-insulation distance required between energized conductors and vegetation, calculated per IEEE Standard 516 and adjusted for altitude. **No vegetation may enter the MVCD at any time.** MVCD encroachment is a Sustained Encroachment and constitutes a violation regardless of whether a fault occurs.

| Nominal voltage (line-to-line) | MVCD (sea level, approx.) |
|---|---|
| 115 kV | 1.07 m (3.5 ft) |
| 230 kV | 1.77 m (5.8 ft) |
| 345 kV | 2.49 m (8.2 ft) |
| 500 kV | 3.51 m (11.5 ft) |
| 765 kV | 4.83 m (15.9 ft) |

> Altitude correction: add approximately 3% per 300 m (1,000 ft) above sea level.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Transmission Owner operates applicable transmission lines | DETERMINISTIC |
| Obligation — MVCD | No vegetation enters MVCD at any time | DETERMINISTIC (binary: encroachment or not) |
| Obligation — patrol | At least one patrol per calendar year | DETERMINISTIC |
| Obligation — strategy | Written maintenance strategy covering work methods, inspection intervals, and control techniques | PARAMETERIZED |
| Evidence | Patrol records with date, line segment, and observed conditions; vegetation maintenance records | DETERMINISTIC |

**Assumption (ASSUME-NERC-FAC-001):** FAC-003 vegetation management compliance is demonstrated when: (1) one patrol per calendar year per applicable line is completed by December 31 — "calendar year" = January 1 through December 31; (2) patrol records document: date, line segment identifier, inspector, and observations (including any vegetation found approaching or within MVCD); (3) any encroachment found during patrol triggers immediate corrective action — work order issued with target completion date; (4) the written vegetation maintenance strategy identifies the applicable line list, inspection frequency rationale, and work method descriptions; (5) strategy reviewed when applicable transmission line list changes or regulatory guidance changes.

**Overall: DETERMINISTIC for annual patrol → Pattern 1; PARAMETERIZED for strategy adequacy → Pattern 2**

---

## FAC-008-3 — Facility Ratings (DETERMINISTIC for existence; PARAMETERIZED for methodology)

### Source excerpt

> **R1.** Each Generator Owner and Transmission Owner shall have a documented Facility Ratings Methodology for its solely and jointly owned Facilities that establishes how Facility Ratings are determined.
>
> **R3.** Each Generator Owner and Transmission Owner shall provide its Facility Ratings to the Transmission Planner, Planning Coordinator, Transmission Operator, and Balancing Authority as requested.

### Required methodology elements

| Element | Classification |
|---|---|
| Identifies equipment types subject to ratings | DETERMINISTIC (existence) |
| Defines how each equipment type's thermal limit is determined | PARAMETERIZED (methodology adequacy) |
| Specifies season/ambient temperature assumptions | PARAMETERIZED |
| Addresses abnormal system conditions (emergency ratings) | PARAMETERIZED |
| Defines how ratings are updated when equipment changes | DETERMINISTIC (process existence) |

**Assumption (ASSUME-NERC-FAC-002):** Facility Ratings Methodology is compliant when: (1) written methodology document exists and covers all owned BES facilities; (2) methodology identifies the limiting component for each facility type (e.g., conductor, transformer, breaker, bus); (3) normal, emergency, and short-term emergency ratings are defined for each applicable facility; (4) ambient temperature assumptions documented (seasonal ratings where applicable); (5) methodology updated when equipment is replaced or ratings are recalculated; (6) actual ratings used in SCADA/EMS match the methodology-derived values — spot check required.

**Overall: DETERMINISTIC for existence → Pattern 1; PARAMETERIZED for methodology adequacy → Pattern 2**

---

## EOP-004-4 — Event Reporting (HIGH — DETERMINISTIC timelines)

### Source excerpt

> **R1.** Each applicable entity shall have documented event reporting procedures that include notification to the Electric Reliability Organization (ERO) and Regional Entity (RE).
>
> **R2.** Each applicable entity shall report each applicable event in accordance with its event reporting procedures, within the timeframes identified in EOP-004-4 Table 1.

### EOP-004-4 Table 1 — Reportable Events (selected high-priority categories)

| Event category | Reporting threshold | Initial notification | Written report |
|---|---|---|---|
| **BES loss of load** | Uncontrolled loss of ≥ 300 MW from a single BES element failure | Within 1 hour (oral to NERC) | Within 24 hours |
| **Voltage deviation** | Unplanned voltage ≥ ±10% of nominal for ≥ 3 consecutive minutes | Within 1 hour (oral) | Within 24 hours |
| **Unexpected frequency deviation** | Frequency outside 59.95–60.05 Hz for > 1 minute (60 Hz systems) | Within 1 hour (oral) | Within 24 hours |
| **Damage to power system equipment** | Damage requiring removal for ≥ 24 hours | Within 24 hours | Within 24 hours |
| **Uncontrolled separation** | Uncontrolled separation of the BES from portions of the interconnection | Within 1 hour (oral) | Within 24 hours |
| **Islanding** | Unintentional loss of synchronism of generation with the BES | Within 1 hour (oral) | Within 24 hours |
| **Fired upon / physical attack** | Physical attack on a BES facility, or notification of credible threat | Within 1 hour (oral) | Within 24 hours |
| **Critical infrastructure protection** | Events with significant cybersecurity impact — coordinate with CIP | Per EOP-004 + CIP requirements | 24 hours |
| **Generator tripped unexpectedly** | Generator ≥ 200 MW tripped unexpectedly | Within 24 hours | Within 24 hours |
| **Transmission line trip** | BES transmission line trip resulting in voltage violation | Within 24 hours | Within 24 hours |

> **"Aware" = the time when the responsible entity or its operating personnel have knowledge of the event.** Clock starts at awareness, not at event occurrence.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | An event matching EOP-004-4 Table 1 category and threshold occurs | DETERMINISTIC (threshold-based) |
| Obligation — initial oral | Notify NERC and RE within 1 hour for Category 1 events | DETERMINISTIC |
| Obligation — written report | Submit written report within 24 hours for most events | DETERMINISTIC |
| Evidence | Event log with awareness timestamp; NERC notification timestamp; OE report submission confirmation | DETERMINISTIC |

**Assumption (ASSUME-NERC-EOP-001):** EOP-004 event reporting is compliant when: (1) documented event reporting procedures exist and identify all Table 1 event categories applicable to the entity's functional roles; (2) awareness timestamp recorded at the time operating personnel first become aware — not retroactively; (3) initial oral notification to NERC Reliability Coordinator (via NERC's 24/7 emergency line) and RE within the timeframe for the event category; (4) written report (NERC OE event analysis system or equivalent form) submitted within 24 hours with: event description, date/time, location, cause (if known), impact, and corrective actions; (5) all events logged even if they ultimately do not meet reporting thresholds — threshold determination documented.

**Overall: DETERMINISTIC → Pattern 1**

---

## NUC-001-4 — Nuclear Plant Interface Coordination (DETERMINISTIC for agreement existence and annual review)

### Source excerpt

> **R1.** Each Nuclear Plant Generator Owner (NUC-GO) shall provide its Transmission Operator (TOP) and Reliability Coordinator (RC) with facility data and documentation necessary to coordinate the connection of the nuclear plant with the BES.
>
> **R3.** Each NUC-GO and its associated TOP, BA, and RC shall jointly review and agree upon the nuclear plant Interface Coordination Document (ICD) at least once per calendar year.

### Interface Coordination Document required elements

| Element | Classification |
|---|---|
| Nuclear plant operator contact information and notification procedures | DETERMINISTIC |
| Transmission grid conditions that could affect nuclear safety systems | PARAMETERIZED |
| Voltage and frequency operating ranges that nuclear plant relies on | DETERMINISTIC |
| Actions required of TOP/BA/RC during nuclear emergencies | PARAMETERIZED |
| Coordination procedures for planned outages affecting nuclear safety | PARAMETERIZED |
| Real-time data exchange requirements | DETERMINISTIC |

**Overall: DETERMINISTIC for ICD existence and annual review → Pattern 1; PARAMETERIZED for content adequacy → Pattern 2**

---

## Test specifications

### YAML spec — FAC, EOP, NUC operations

```yaml
spec_id: NERC-FAC-EOP-001
framework: NERC Non-CIP
category: FAC / EOP / NUC
standards:
  - FAC-003-4
  - FAC-008-3
  - EOP-004-4
  - NUC-001-4
pattern: 1  # Primary for FAC-003 patrol and EOP-004 timelines; Pattern 2 for methodology
evidence:
  - vegetation_patrol_records (line ID, patrol date, inspector, observations)
  - vegetation_maintenance_strategy (document, last review date)
  - facility_ratings_methodology (document, equipment list, ambient assumptions)
  - facility_ratings_current (ratings in SCADA/EMS vs methodology-derived)
  - event_log (event ID, awareness timestamp, category, notification timestamps)
  - eop_procedures (document, Table 1 event categories covered)
  - nuc_interface_coordination_documents (ICD per nuclear plant, last review date, signatories)
```

### Python test file

```python
# tests/nerc_ops/test_fac_eop_operations.py
"""
NERC Non-CIP — FAC-003, FAC-008, EOP-004, NUC-001.

Standards: FAC-003-4, FAC-008-3, EOP-004-4, NUC-001-4
Assumptions: ASSUME-NERC-FAC-001, ASSUME-NERC-FAC-002, ASSUME-NERC-EOP-001, ASSUME-NERC-EOP-002
"""
import pytest
from datetime import datetime, timedelta, timezone
from typing import Any

EOP004_CATEGORY1_NOTIFY_MAX_SECONDS = 3600   # 1 hour oral notification
EOP004_WRITTEN_REPORT_MAX_HOURS = 24
NUC001_ANNUAL_REVIEW_MAX_DAYS = 365


@pytest.fixture(autouse=True)
def require_applicable_entity(entity_scope: dict[str, Any]):
    """Gate: tests only apply to entities with applicable functional roles."""
    if not entity_scope.get("has_nerc_reliability_function"):
        pytest.skip("Entity has no applicable NERC functional role — tests informational only")


# ── FAC-003-4: Vegetation Patrol ─────────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-NERC-FAC-001",
    description="Annual vegetation patrol: once per calendar year (by Dec 31) for all applicable lines",
    approved_by="Vegetation Management Program Lead",
    review_date="2027-05-21",
)
def test_annual_vegetation_patrol_completed_this_year(
    vegetation_patrol_records: list[dict[str, Any]],
    applicable_transmission_lines: list[dict[str, Any]],
    entity_scope: dict[str, Any],
):
    """FAC-003-4 R2: At least one patrol per calendar year per applicable transmission line."""
    if not entity_scope.get("is_transmission_owner_fac003_applicable"):
        pytest.skip("Entity is not subject to FAC-003-4")

    current_year = datetime.now(timezone.utc).year
    lines_patrolled_this_year = {
        r["line_segment_id"]
        for r in vegetation_patrol_records
        if r.get("patrol_date", datetime.min.replace(tzinfo=timezone.utc)).year == current_year
    }

    unpatrolled = [
        line["line_segment_id"]
        for line in applicable_transmission_lines
        if line["line_segment_id"] not in lines_patrolled_this_year
    ]

    assert not unpatrolled, (
        f"Applicable transmission lines with no vegetation patrol in {current_year}: {unpatrolled}"
    )


def test_no_vegetation_mvcd_encroachments_unresolved(
    vegetation_patrol_records: list[dict[str, Any]],
):
    """FAC-003-4 R1: Any MVCD encroachment identified must have an open corrective action."""
    unresolved = []

    for record in vegetation_patrol_records:
        if not record.get("mvcd_encroachment_observed"):
            continue
        if not record.get("corrective_action_initiated"):
            unresolved.append(
                f"Line {record['line_segment_id']} on {record.get('patrol_date', '?')}: "
                "MVCD encroachment observed but no corrective action initiated"
            )

    assert not unresolved, (
        f"MVCD encroachments without corrective action: {unresolved}"
    )


# ── FAC-008-3: Facility Ratings ───────────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-NERC-FAC-002",
    description="Written ratings methodology exists; covers all BES facilities; seasonal assumptions documented",
    approved_by="Ratings Engineer",
    review_date="2027-05-21",
)
def test_facility_ratings_methodology_exists(
    facility_ratings_methodology: dict[str, Any],
    entity_scope: dict[str, Any],
):
    """FAC-008-3 R1: Documented Facility Ratings Methodology required for all owned BES facilities."""
    if not entity_scope.get("is_to_or_go_with_bes_facilities"):
        pytest.skip("Entity is not a TO/GO with BES facilities — FAC-008 not applicable")

    assert facility_ratings_methodology.get("exists"), (
        "No Facility Ratings Methodology document found — FAC-008-3 R1 requires written methodology"
    )
    required_elements = {
        "equipment_types_identified",
        "thermal_limit_determination_method",
        "ambient_temperature_assumptions",
        "emergency_rating_definition",
        "rating_update_process",
    }
    missing = required_elements - {
        k for k, v in facility_ratings_methodology.items() if v
    }
    assert not missing, (
        f"Facility Ratings Methodology missing required elements: {missing}"
    )


# ── EOP-004-4: Event Reporting ────────────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-NERC-EOP-001",
    description="Category 1 events: oral notification within 1 hour; written report within 24 hours",
    approved_by="Compliance Manager",
    review_date="2027-05-21",
)
def test_eop004_category1_oral_notification_timely(
    event_log: list[dict[str, Any]],
):
    """EOP-004-4 R2: Category 1 events require oral notification to NERC within 1 hour of awareness."""
    late_notifications = []

    for event in event_log:
        if event.get("eop004_category") != 1:
            continue

        awareness_ts = event.get("awareness_timestamp")
        oral_notify_ts = event.get("nerc_oral_notification_timestamp")

        if awareness_ts is None:
            continue
        if oral_notify_ts is None:
            elapsed = (datetime.now(timezone.utc) - awareness_ts).total_seconds()
            if elapsed > EOP004_CATEGORY1_NOTIFY_MAX_SECONDS:
                late_notifications.append(
                    f"{event['event_id']}: no oral notification recorded "
                    f"{elapsed / 3600:.1f}h after awareness"
                )
        else:
            elapsed = (oral_notify_ts - awareness_ts).total_seconds()
            if elapsed > EOP004_CATEGORY1_NOTIFY_MAX_SECONDS:
                late_notifications.append(
                    f"{event['event_id']}: oral notification {elapsed / 60:.1f} min after awareness "
                    f"(max {EOP004_CATEGORY1_NOTIFY_MAX_SECONDS / 60:.0f} min)"
                )

    assert not late_notifications, (
        f"EOP-004-4 Category 1 oral notification violations: {late_notifications}"
    )


@pytest.mark.assumption(
    id="ASSUME-NERC-EOP-001",
    description="All applicable events: written report submitted within 24 hours",
    approved_by="Compliance Manager",
    review_date="2027-05-21",
)
def test_eop004_written_report_submitted_within_24_hours(
    event_log: list[dict[str, Any]],
):
    """EOP-004-4 R2: Written event reports must be submitted within 24 hours for all Table 1 events."""
    late_reports = []

    for event in event_log:
        if not event.get("eop004_reportable"):
            continue

        awareness_ts = event.get("awareness_timestamp")
        written_report_ts = event.get("written_report_submission_timestamp")

        if awareness_ts is None:
            continue

        if written_report_ts is None:
            hours_since = (datetime.now(timezone.utc) - awareness_ts).total_seconds() / 3600
            if hours_since > EOP004_WRITTEN_REPORT_MAX_HOURS:
                late_reports.append(
                    f"{event['event_id']}: no written report submitted "
                    f"{hours_since:.1f}h after awareness"
                )
        else:
            hours_elapsed = (written_report_ts - awareness_ts).total_seconds() / 3600
            if hours_elapsed > EOP004_WRITTEN_REPORT_MAX_HOURS:
                late_reports.append(
                    f"{event['event_id']}: written report submitted {hours_elapsed:.1f}h after awareness "
                    f"(max {EOP004_WRITTEN_REPORT_MAX_HOURS}h)"
                )

    assert not late_reports, (
        f"EOP-004-4 written report timing violations: {late_reports}"
    )


def test_eop_reporting_procedures_cover_all_applicable_categories(
    eop_procedures: dict[str, Any],
    entity_scope: dict[str, Any],
):
    """EOP-004-4 R1: EOP procedures must cover all Table 1 event categories applicable to the entity."""
    applicable_categories = entity_scope.get("eop004_applicable_categories", [])
    covered_categories = set(eop_procedures.get("covered_event_categories", []))

    missing = set(applicable_categories) - covered_categories
    assert not missing, (
        f"EOP-004-4 event reporting procedures do not cover applicable categories: {missing}"
    )


# ── NUC-001-4: Nuclear Interface ──────────────────────────────────────────────

def test_nuc001_interface_coordination_documents_current(
    nuc_interface_coordination_documents: list[dict[str, Any]],
    entity_scope: dict[str, Any],
):
    """NUC-001-4 R3: Interface Coordination Documents must be jointly reviewed annually."""
    if not entity_scope.get("has_nuclear_plant_interface_obligation"):
        pytest.skip("Entity has no NUC-001-4 obligation")

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=NUC001_ANNUAL_REVIEW_MAX_DAYS)

    overdue = []
    for icd in nuc_interface_coordination_documents:
        last_review = icd.get("last_joint_review_date")
        if last_review is None:
            overdue.append(f"{icd['nuclear_plant_id']}: no joint review on record")
        elif last_review < cutoff:
            days_since = (now - last_review).days
            overdue.append(
                f"{icd['nuclear_plant_id']}: ICD joint review {days_since}d ago "
                f"(max {NUC001_ANNUAL_REVIEW_MAX_DAYS}d)"
            )

    assert not overdue, (
        f"NUC-001-4 Interface Coordination Documents not reviewed within last year: {overdue}"
    )
```
