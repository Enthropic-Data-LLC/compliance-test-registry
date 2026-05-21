# NERC INT / IRO / VAR — Interchange, Reliability Coordination, and Reactive Power

**Spec file:** `int-iro-var-coordination.md`
**Registry version:** 2026.05
**Last updated:** 2026-05-21
**Parent index:** [`_index.md`](./_index.md)
**Standards covered:**
- INT-006-4 — Evaluation of Interchange Transactions
- INT-009-2 — Implementation of Interchange
- IRO-001-5 — Reliability Coordination: Responsibilities and Authorities
- IRO-014-3 — Operationally Planning Assessments
- VAR-001-5 — Voltage and Reactive Control
- VAR-002-4.1 — Generator Operation for Maintaining Network Voltage Schedules
**Authority:** North American Electric Reliability Corporation (NERC); enforced by Regional Entities under FERC oversight

---

## Overview

These three standard families govern the coordination spine of the bulk electric system:

- **INT:** How interchange (energy transfer) transactions between balancing authorities are evaluated, tagged, and implemented. E-tagging is the transaction record — deviation from it is the primary enforcement flashpoint.
- **IRO:** How the Reliability Coordinator exercises authority over TOPs and BAs. The RC's directive authority and TOPs/BAs' obligation to comply are the DETERMINISTIC core.
- **VAR:** How generators and operators maintain reactive power and voltage. The AVR (automatic voltage regulator) operating mode obligation and the 2-calendar-day notification window for out-of-service AVR are the primary DETERMINISTIC requirements.

---

## Scope pre-condition

```python
import pytest

APPLICABLE_ENTITY_TYPES = {
    "INT-006-4": {"RC", "BA", "TOP", "TO"},
    "INT-009-2": {"BA", "GOP"},
    "IRO-001-5": {"RC", "TOP", "BA"},
    "IRO-014-3": {"RC"},
    "VAR-001-5": {"TO", "TOP", "BA", "GO", "GOP", "RC"},
    "VAR-002-4.1": {"GOP"},
}


@pytest.fixture(autouse=True)
def nerc_int_iro_var_scope_check(entity_profile: dict, request):
    """Skip test if entity is not registered as an applicable functional entity for this standard."""
    entity_type = entity_profile.get("functional_entity_type")
    standard_id = getattr(request, "param", None) or request.node.get_closest_marker(
        "standard"
    )
    if standard_id is None:
        return  # No standard marker; let test run

    applicable = APPLICABLE_ENTITY_TYPES.get(str(standard_id), set())
    if entity_type not in applicable:
        pytest.skip(
            f"Standard {standard_id} does not apply to functional entity type "
            f"'{entity_type}'; applicable: {sorted(applicable)}"
        )
```

---

## INT-006-4 — Evaluation of Interchange Transactions

### Requirements extracted

**Source:** NERC Standard INT-006-4; applicable to RC, BA, TOP (varies by requirement)

| # | Requirement | Subject | Obligation | Evidence |
|---|------------|---------|------------|---------|
| R1 | Curtailment basis must follow NERC curtailment priority | RC/BA/TOP | When curtailment of interchange is required for reliability, entities must apply curtailment in the order specified by INT-006-4 Attachment 1 (reliability reason first, then economic/other) | Curtailment action log; reason code recorded per curtailment |
| R2 | Evaluation of proposed interchange | RC/BA | Must evaluate the reliability impact of each proposed interchange transaction on the BES; notify tagging entities of constraints | Interchange evaluation records; constraint notifications |
| R3 | Coordination with adjacent entities | RC/BA | When an interchange transaction would create an SOL or IROL exceedance, notify the RC and curtail per priority order | Constraint notification records |

### Tests — interchange curtailment priority

```python
import pytest

# INT-006-4 Attachment 1: Curtailment priority order
# Priority 1 (curtail first): transactions causing IROL exceedances
# Priority 2: transactions causing SOL exceedances
# Priority 3: transactions based on other reliability reasons
# Priority 4 (curtail last): economic/market-based reasons
CURTAILMENT_PRIORITY_ORDER = {
    "IROL_exceedance": 1,
    "SOL_exceedance": 2,
    "other_reliability": 3,
    "economic": 4,
}


class TestINT006Curtailment:
    """Pattern 2: PARAMETERIZED — curtailment applicability requires reliability assessment."""

    @pytest.mark.assumption(
        id="ASSUME-NERC-INT-001",
        description=(
            "INT-006-4 curtailment priority: when reliability-based curtailment is required, "
            "entities must apply the INT-006-4 Attachment 1 priority order — IROL transactions "
            "curtailed first, then SOL transactions, then other reliability, then economic. "
            "Curtailing an economic-priority transaction before a reliability-priority transaction "
            "when both must be curtailed is a violation. Each curtailment action must document "
            "the reliability basis (reason code) in the e-tagging system or equivalent record."
        ),
        approved_by="Operations / Reliability Coordinator",
        review_date="2026-05-21",
    )
    def test_curtailment_priority_order_followed(self, curtailment_event: dict):
        curtailed_transactions = curtailment_event.get("curtailed_transactions", [])
        remaining_transactions = curtailment_event.get("remaining_transactions_not_curtailed", [])

        # Find the highest priority of what was curtailed and lowest priority of what was not
        curtailed_priorities = [
            CURTAILMENT_PRIORITY_ORDER.get(t.get("reason_code"), 99)
            for t in curtailed_transactions
        ]
        remaining_priorities = [
            CURTAILMENT_PRIORITY_ORDER.get(t.get("reason_code"), 99)
            for t in remaining_transactions
        ]

        if not curtailed_priorities or not remaining_priorities:
            pytest.skip("Insufficient curtailment data to evaluate priority order")

        # The lowest priority curtailed should not be lower than the highest priority remaining
        # (i.e., don't curtail economic while leaving IROL transactions untouched)
        min_curtailed_priority = min(curtailed_priorities)  # Lower = higher priority
        max_remaining_priority = max(remaining_priorities)  # Higher = lower priority

        assert min_curtailed_priority <= max_remaining_priority, (
            f"Curtailment event '{curtailment_event.get('event_id')}': "
            f"transactions with lower reliability priority (priority {max_remaining_priority}) "
            "were NOT curtailed while higher-priority reliability transactions "
            f"(priority {min_curtailed_priority}) WERE curtailed — "
            "INT-006-4 Attachment 1 requires curtailment in reliability priority order"
        )

    def test_curtailment_reason_code_documented(self, curtailment_event: dict):
        for txn in curtailment_event.get("curtailed_transactions", []):
            txn_id = txn.get("e_tag_id")
            reason_code = txn.get("reason_code")
            assert reason_code is not None, (
                f"Curtailed transaction '{txn_id}': no reason code documented — "
                "INT-006-4 requires documenting the reliability basis for each curtailment action; "
                "undocumented curtailments cannot be evaluated for priority compliance"
            )
            assert reason_code in CURTAILMENT_PRIORITY_ORDER, (
                f"Curtailed transaction '{txn_id}': reason code '{reason_code}' is not a "
                f"recognized INT-006-4 priority category; valid codes: "
                f"{list(CURTAILMENT_PRIORITY_ORDER.keys())}"
            )
```

---

## INT-009-2 — Implementation of Interchange

### Requirements extracted

**Source:** NERC Standard INT-009-2; applicable to BA, GOP

| # | Requirement | Subject | Threshold | Evidence |
|---|------------|---------|-----------|---------|
| R1 | No unauthorized interchange | BA | BA shall not allow interchange to occur without an approved e-tag | E-tag system records; actual flows vs. e-tagged flows |
| R2 | E-tag deviation tolerance — GOP | GOP | Generator operator shall operate the generator to match the approved e-tag schedule within ±10 MW or ±1.5% of the e-tagged MW (whichever is greater) for any clock-hour; deviations beyond tolerance are unauthorized | E-tag deviation reports; metered generation vs. e-tagged schedule per hour |
| R3 | Unauthorized interchange curtailment | BA | Upon discovery of unauthorized interchange, BA shall take immediate corrective action to curtail or obtain approval | Corrective action log; e-tag submission after discovery |

### DETERMINISTIC thresholds

| Obligation | Threshold | Source |
|---|---|---|
| E-tag deviation tolerance (GOP) | ±10 MW or ±1.5% of e-tagged MW per hour, whichever is greater | INT-009-2 R2 |
| Unauthorized interchange — corrective action | Immediately upon discovery | INT-009-2 R3 |

### Tests — interchange implementation compliance

```python
import pytest


class TestINT009Implementation:
    """Pattern 1: DETERMINISTIC — ±10 MW / ±1.5% deviation tolerance is a fixed threshold."""

    @pytest.mark.assumption(
        id="ASSUME-NERC-INT-002",
        description=(
            "INT-009-2 e-tag deviation tolerance: GOP must operate within ±10 MW or ±1.5% "
            "of the approved e-tagged MW, whichever is greater, for each clock-hour interval. "
            "The 'whichever is greater' clause means small generators (with small e-tag MW) "
            "get a ±10 MW floor. Large generators (>667 MW e-tagged) use the ±1.5% calculation "
            "since 1.5% × 667 = 10 MW. Deviation is measured from the approved e-tag schedule "
            "as of the operating hour — not the original scheduled value (adjustments mid-hour "
            "update the reference). Unauthorized interchange (no approved e-tag) is a categorical "
            "violation regardless of quantity."
        ),
        approved_by="Operations Manager",
        review_date="2026-05-21",
    )
    def test_gop_e_tag_deviation_within_tolerance(self, e_tag_deviation_record: dict):
        e_tagged_mw = e_tag_deviation_record.get("e_tagged_mw", 0.0)
        actual_mw = e_tag_deviation_record.get("actual_mw_for_hour", 0.0)
        clock_hour = e_tag_deviation_record.get("clock_hour")
        generator_id = e_tag_deviation_record.get("generator_id")
        e_tag_id = e_tag_deviation_record.get("e_tag_id")

        # Tolerance: greater of ±10 MW or ±1.5% of e-tagged MW
        tolerance_mw = max(10.0, abs(e_tagged_mw) * 0.015)
        deviation_mw = abs(actual_mw - e_tagged_mw)

        assert deviation_mw <= tolerance_mw, (
            f"Generator '{generator_id}', e-tag '{e_tag_id}', hour {clock_hour}: "
            f"deviation {deviation_mw:.1f} MW from e-tagged schedule {e_tagged_mw:.1f} MW "
            f"(actual: {actual_mw:.1f} MW) — exceeds INT-009-2 tolerance of "
            f"{tolerance_mw:.1f} MW (max of 10 MW or 1.5% of e-tagged MW); "
            "deviation beyond tolerance constitutes unauthorized interchange"
        )

    def test_no_interchange_flows_without_approved_e_tag(self, interchange_flow_record: dict):
        ba_id = interchange_flow_record.get("balancing_authority_id")
        measured_flow_mw = interchange_flow_record.get("measured_interchange_mw", 0.0)
        approved_e_tag_exists = interchange_flow_record.get("approved_e_tag_on_file", False)

        # A non-zero flow without an approved e-tag is unauthorized interchange
        if abs(measured_flow_mw) > 1.0:  # 1 MW threshold to ignore meter noise
            assert approved_e_tag_exists, (
                f"BA '{ba_id}': measured interchange flow of {measured_flow_mw:.1f} MW "
                "with no approved e-tag on record — INT-009-2 R1 prohibits interchange "
                "without an approved e-tag; unauthorized interchange must be curtailed "
                "immediately upon discovery"
            )
```

---

## IRO-001-5 — Reliability Coordination: Responsibilities and Authorities

### Requirements extracted

**Source:** NERC Standard IRO-001-5; applicable to RC, TOP, BA

| # | Requirement | Subject | Obligation | Evidence |
|---|------------|---------|------------|---------|
| R1 | RC directive authority documented | RC | RC shall have documented authority to direct TOPs and BAs within its area to take actions required to preserve reliability | RC authority documentation; NERC functional registration |
| R2 | TOP/BA must comply with RC directives | TOP, BA | Each TOP and BA within an RC's area shall comply with RC directives (exceptions for immediate safety risks under certain conditions; must notify RC of non-compliance basis) | Directive compliance log; non-compliance documentation |
| R3 | Non-compliance notification | TOP/BA | If a TOP or BA cannot comply with an RC directive, it shall immediately notify the RC of the reason for non-compliance | Non-compliance notification records |
| R4 | RC coordination with adjacent RCs | RC | RC shall coordinate reliability issues affecting multiple RC areas | Inter-RC coordination log |

### Tests — IRO-001 authority and compliance

```python
import pytest


class TestIRO001RCAuthority:
    """Pattern 1/2: directive compliance is DETERMINISTIC; authority adequacy is PARAMETERIZED."""

    @pytest.mark.assumption(
        id="ASSUME-NERC-IRO-001",
        description=(
            "IRO-001-5 RC directive authority: the RC has authority to direct TOPs and BAs "
            "to take specific reliability actions. TOPs and BAs must comply — they cannot "
            "refuse an RC directive except when compliance would create an immediate safety risk "
            "to personnel or the public (a very narrow exception). If a TOP or BA cannot comply, "
            "it must IMMEDIATELY notify the RC of the reason; the notification must precede or "
            "simultaneously accompany the non-compliance decision. The RC directive authority "
            "is separate from the COM-002-4 three-part communication requirement — directives "
            "under IRO-001 still require three-part communication under COM-002."
        ),
        approved_by="Operations / Reliability Coordinator",
        review_date="2026-05-21",
    )
    def test_rc_directive_compliance_documented(self, rc_directive_record: dict):
        directive_id = rc_directive_record.get("directive_id")
        directive_recipient = rc_directive_record.get("recipient_entity_id")
        action_confirmed = rc_directive_record.get("recipient_confirmed_compliance", False)
        non_compliance_notified = rc_directive_record.get("non_compliance_notification_sent", False)

        compliance_or_notified = action_confirmed or non_compliance_notified
        assert compliance_or_notified, (
            f"RC directive '{directive_id}' to entity '{directive_recipient}': neither "
            "compliance confirmation NOR non-compliance notification on record — "
            "IRO-001-5 R2 requires the recipient to either comply with the directive or "
            "IMMEDIATELY notify the RC of the reason for non-compliance; absence of either "
            "response constitutes a violation of IRO-001-5 R2"
        )

    def test_non_compliance_has_documented_basis(self, rc_directive_record: dict):
        if not rc_directive_record.get("non_compliance_notification_sent", False):
            pytest.skip("Entity complied with directive — no non-compliance basis needed")

        non_compliance_reason = rc_directive_record.get("non_compliance_reason")
        assert non_compliance_reason is not None, (
            f"RC directive '{rc_directive_record.get('directive_id')}': non-compliance "
            "notification sent but no documented reason — IRO-001-5 R3 requires the entity "
            "to state the reason for non-compliance when notifying the RC; undocumented "
            "non-compliance is a violation of both R2 and R3"
        )

    def test_rc_authority_documentation_exists(self, rc_program: dict):
        authority_doc = rc_program.get("directive_authority_documentation")
        assert authority_doc is not None, (
            "IRO-001-5 R1: RC has no documented authority to direct TOPs and BAs — "
            "the RC must maintain documentation of its authority within its reliability "
            "coordination area; authority documentation is reviewed in NERC audits"
        )
```

---

## IRO-014-3 — Operationally Planning Assessments (Next-Day Reliability)

### Requirements extracted

**Source:** NERC Standard IRO-014-3; applicable to RC

| # | Requirement | Subject | Obligation | Evidence |
|---|------------|---------|------------|---------|
| R1 | Daily next-day reliability assessment | RC | RC shall conduct a next-day (T+12 to T+36 hour) operational planning assessment at least once per day | Next-day assessment records; daily timing log |
| R2 | Assessment scope — SOL/IROL | RC | Assessment must include evaluation for SOL and IROL exceedances under next-day conditions | Assessment records with SOL/IROL evaluation |
| R3 | Notification of identified problems | RC | When next-day assessment identifies a reliability problem, RC shall notify affected TOPs and BAs before the operating period begins | Problem notification records; timing of notification vs. operating period |
| R4 | Assessment information sources | RC | RC shall use adequate, reliable, and current data for next-day assessments | Data source documentation; data currency validation |

### DETERMINISTIC thresholds

| Obligation | Threshold | Source |
|---|---|---|
| Next-day OPA frequency | At least once per operating day | IRO-014-3 R1 |
| OPA notification to TOPs/BAs | Before the start of the affected operating period | IRO-014-3 R3 |

### Tests — next-day operational planning assessment

```python
import pytest
from datetime import date, timedelta


class TestIRO014OperationalPlanningAssessment:
    """Pattern 1/2: daily cadence is DETERMINISTIC; assessment adequacy is PARAMETERIZED."""

    @pytest.mark.assumption(
        id="ASSUME-NERC-IRO-002",
        description=(
            "IRO-014-3 next-day OPA: the RC must conduct at least one operational planning "
            "assessment per operating day for the next-day operating horizon (typically "
            "T+12 to T+36 hours). The assessment must evaluate SOL and IROL exceedances "
            "under anticipated next-day system conditions. If the OPA identifies a reliability "
            "problem (e.g., a projected SOL exceedance), the RC must notify affected TOPs "
            "and BAs before the operating period begins — notification after the operating "
            "period starts is not timely compliance. Assessment results must be documented "
            "and retained per NERC evidence retention requirements."
        ),
        approved_by="RC Operations",
        review_date="2026-05-21",
    )
    def test_next_day_opa_conducted_each_operating_day(self, rc_opa_log: dict):
        operating_dates = rc_opa_log.get("operating_dates_in_period", [])
        opa_dates = set(rc_opa_log.get("opa_conducted_dates", []))

        days_missing_opa = [d for d in operating_dates if d not in opa_dates]
        assert not days_missing_opa, (
            f"RC operational planning assessment (OPA) not conducted on: {days_missing_opa} — "
            "IRO-014-3 R1 requires an OPA at least once per operating day; "
            "missing OPAs are among the most commonly cited IRO-014 violations"
        )

    def test_opa_includes_sol_irol_evaluation(self, opa_record: dict):
        sol_evaluated = opa_record.get("sol_exceedance_evaluated", False)
        irol_evaluated = opa_record.get("irol_exceedance_evaluated", False)

        assert sol_evaluated, (
            f"OPA for {opa_record.get('assessment_date')}: SOL exceedance evaluation "
            "not documented — IRO-014-3 R2 requires the OPA to include assessment for "
            "potential SOL exceedances in the next-day operating period"
        )
        assert irol_evaluated, (
            f"OPA for {opa_record.get('assessment_date')}: IROL exceedance evaluation "
            "not documented — IRO-014-3 R2 requires IROL evaluation in each OPA"
        )

    def test_opa_notifications_issued_before_operating_period(self, opa_record: dict):
        problems_identified = opa_record.get("reliability_problems_identified", [])
        if not problems_identified:
            return  # No problems found — no notifications required

        operating_period_start = opa_record.get("operating_period_start_time")
        for problem in problems_identified:
            notification_time = problem.get("notification_sent_to_top_ba_time")
            assert notification_time is not None, (
                f"OPA {opa_record.get('assessment_date')}: reliability problem "
                f"'{problem.get('problem_description')}' identified but no notification "
                "sent to TOP/BA — IRO-014-3 R3 requires notifying affected TOPs and BAs "
                "when the OPA identifies a reliability problem"
            )
            if operating_period_start is not None:
                assert notification_time <= operating_period_start, (
                    f"OPA {opa_record.get('assessment_date')}: problem notification sent "
                    f"at {notification_time} — AFTER operating period start "
                    f"{operating_period_start} — notification must be issued BEFORE "
                    "the affected operating period begins"
                )
```

---

## VAR-001-5 — Voltage and Reactive Control

### Requirements extracted

**Source:** NERC Standard VAR-001-5; applicable to TO, TOP, BA, GO, GOP, RC

| # | Requirement | Subject | Obligation | Evidence |
|---|------------|---------|------------|---------|
| R1 | Voltage schedule maintenance | TOP | Shall maintain transmission voltage within the RC-approved voltage schedule | Voltage schedule compliance log; exceedance records |
| R2 | Reactive resource coordination | RC/TOP | RC shall establish voltage schedules; TOP shall coordinate reactive resources to maintain the schedule | RC voltage schedule document; TOP coordination records |
| R3 | Reactive support directives | GO/GOP | When directed by the TOP or RC to provide reactive support (Mvar), GO/GOP shall do so within the capability of the generator | Reactive support log; directive compliance |
| R4 | Voltage deviation — notification | TOP/BA | If voltage deviation cannot be corrected within the operating period, notify the RC | Voltage deviation notification records |

### Tests — VAR-001 voltage schedule compliance

```python
import pytest


class TestVAR001VoltageControl:
    """Pattern 2: PARAMETERIZED — voltage schedule adequacy requires engineering judgment."""

    @pytest.mark.assumption(
        id="ASSUME-NERC-VAR-001",
        description=(
            "VAR-001-5 voltage schedule: the RC establishes voltage schedules for key buses "
            "on the transmission system. TOPs must maintain transmission voltage within those "
            "schedules and coordinate reactive resources (generators, capacitors, reactors, "
            "SVCs) to do so. When a TOP cannot maintain the voltage schedule without exceeding "
            "thermal limits or stability margins, the TOP notifies the RC. The RC may then "
            "revise the voltage schedule or direct additional reactive support from adjacent "
            "entities. Voltage schedule is an operational target — deviation for reliability "
            "reasons (e.g., to avoid an overload) is permissible with RC coordination and "
            "documentation."
        ),
        approved_by="Operations / Reliability Coordinator",
        review_date="2026-05-21",
    )
    def test_voltage_schedule_exists_from_rc(self, top_operating_data: dict):
        voltage_schedule_document = top_operating_data.get("rc_approved_voltage_schedule_reference")
        assert voltage_schedule_document is not None, (
            "VAR-001-5 R2: No RC-approved voltage schedule on record — the RC must establish "
            "voltage schedules for key transmission buses; absence of a voltage schedule "
            "prevents TOP from demonstrating compliance with the voltage maintenance obligation"
        )

    def test_reactive_support_directive_complied_with(self, reactive_directive_record: dict):
        directive_id = reactive_directive_record.get("directive_id")
        entity_id = reactive_directive_record.get("recipient_entity_id")
        compliance_confirmed = reactive_directive_record.get("reactive_support_provided", False)
        within_capability = reactive_directive_record.get("within_generator_capability", True)

        if not within_capability:
            pytest.skip("Directive was beyond generator capability — non-compliance basis exists")

        assert compliance_confirmed, (
            f"Reactive support directive '{directive_id}' to '{entity_id}': reactive support "
            "not provided — VAR-001-5 R3 requires GO/GOP to provide reactive support when "
            "directed by the TOP or RC, within the generator's capability"
        )

    def test_voltage_deviation_reported_to_rc_when_not_correctable(self, voltage_event: dict):
        deviation_corrected = voltage_event.get("deviation_corrected_in_operating_period", True)
        if deviation_corrected:
            return  # Corrected — no notification required

        rc_notified = voltage_event.get("rc_notified_of_uncorrectable_deviation", False)
        assert rc_notified, (
            f"Voltage deviation event '{voltage_event.get('event_id')}': voltage schedule "
            "deviation could not be corrected within the operating period but RC was NOT "
            "notified — VAR-001-5 R4 requires notifying the RC when voltage cannot be "
            "maintained within the schedule"
        )
```

---

## VAR-002-4.1 — Generator Operation for Maintaining Network Voltage Schedules

### Requirements extracted

**Source:** NERC Standard VAR-002-4.1; applicable to GOP

| # | Requirement | Subject | Threshold | Evidence |
|---|------------|---------|-----------|---------|
| R1 | AVR in automatic mode | GOP | Generator shall operate in automatic voltage regulator (AVR) mode at all times, unless: (a) equipment failure requires manual, (b) TOP directs manual, (c) pre-planned testing | AVR mode records; operating log; exceptions documented |
| R2 | Notification of AVR out-of-service | GOP | When AVR is taken out of service for maintenance, the GOP shall notify the TOP within 2 calendar days | Notification records; date of notification vs. date AVR taken out of service |
| R3 | Voltage tolerance in manual mode | GOP | When operating in manual (non-AVR) mode, GOP shall maintain voltage within ±5% of the scheduled voltage or the high/low limits established by the TOP | Manual mode voltage log; ±5% band compliance |
| R4 | Compliance with TOP voltage schedule | GOP | GOP shall operate in accordance with the voltage schedule or directives from the TOP | Dispatch/voltage schedule compliance records |

### DETERMINISTIC thresholds

| Obligation | Threshold | Source |
|---|---|---|
| AVR operating mode | Automatic (default); manual only for equipment failure, TOP directive, or testing | VAR-002-4.1 R1 |
| AVR out-of-service notification to TOP | Within 2 calendar days of taking AVR out of service | VAR-002-4.1 R2 |
| Voltage tolerance in manual mode | Within ±5% of scheduled voltage | VAR-002-4.1 R3 |

### Tests — generator AVR and voltage compliance

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta

AVR_OUT_OF_SERVICE_NOTIFICATION_DAYS = 2   # Calendar days
MANUAL_MODE_VOLTAGE_TOLERANCE_FRACTION = 0.05  # ±5%

AVR_ACCEPTABLE_MANUAL_REASONS = {
    "equipment_failure",
    "top_directive",
    "pre_planned_testing",
}


class TestVAR002GeneratorVoltage:
    """Pattern 1: DETERMINISTIC — 2-calendar-day notification and ±5% tolerance are fixed."""

    @pytest.mark.assumption(
        id="ASSUME-NERC-VAR-002",
        description=(
            "VAR-002-4.1 AVR requirements: generators default to operating in automatic "
            "voltage regulator (AVR) mode. Manual (non-AVR) operation is only permitted for: "
            "(1) AVR equipment failure requiring manual operation, (2) TOP directive to operate "
            "manually, or (3) pre-planned testing. When the AVR is taken out of service for "
            "maintenance, the GOP must notify the TOP within 2 calendar days (not business days — "
            "calendar days). While in manual mode, the generator must maintain terminal voltage "
            "within ±5% of the scheduled voltage point. The TOP may establish tighter band limits "
            "which take precedence over the ±5% default."
        ),
        approved_by="Operations Manager / Plant Manager",
        review_date="2026-05-21",
    )
    def test_avr_manual_mode_has_valid_basis(self, generator_operating_record: dict):
        avr_mode = generator_operating_record.get("avr_mode")
        generator_id = generator_operating_record.get("generator_id")
        operating_hour = generator_operating_record.get("operating_hour")

        if avr_mode != "manual":
            return  # AVR in automatic — no issue

        manual_mode_reason = generator_operating_record.get("manual_mode_reason")
        assert manual_mode_reason in AVR_ACCEPTABLE_MANUAL_REASONS, (
            f"Generator '{generator_id}', hour {operating_hour}: AVR is in manual mode "
            f"with reason '{manual_mode_reason}' — not a recognized VAR-002-4.1 acceptable "
            f"reason; valid reasons: {sorted(AVR_ACCEPTABLE_MANUAL_REASONS)}. "
            "Unauthorized manual AVR operation is a VAR-002-4.1 R1 violation."
        )

    def test_avr_out_of_service_notification_within_2_days(self, avr_maintenance_record: dict):
        generator_id = avr_maintenance_record.get("generator_id")
        avr_oos_date = avr_maintenance_record.get("avr_taken_out_of_service_date")
        top_notification_date = avr_maintenance_record.get("top_notification_date")

        if avr_oos_date is None:
            pytest.skip("AVR out-of-service date not recorded")

        assert top_notification_date is not None, (
            f"Generator '{generator_id}': AVR taken out of service on {avr_oos_date} "
            "but no TOP notification on record — VAR-002-4.1 R2 requires notifying the TOP "
            f"within {AVR_OUT_OF_SERVICE_NOTIFICATION_DAYS} calendar days of taking the AVR "
            "out of service for maintenance"
        )

        days_elapsed = (top_notification_date - avr_oos_date).days
        assert days_elapsed <= AVR_OUT_OF_SERVICE_NOTIFICATION_DAYS, (
            f"Generator '{generator_id}': AVR taken out of service {avr_oos_date}, "
            f"TOP notified {top_notification_date} ({days_elapsed} calendar days later) — "
            f"VAR-002-4.1 R2 requires notification within "
            f"{AVR_OUT_OF_SERVICE_NOTIFICATION_DAYS} calendar days; "
            f"{days_elapsed - AVR_OUT_OF_SERVICE_NOTIFICATION_DAYS} day(s) late"
        )

    def test_generator_voltage_within_5pct_in_manual_mode(self, generator_operating_record: dict):
        if generator_operating_record.get("avr_mode") != "manual":
            pytest.skip("Generator is in AVR automatic mode — manual voltage test not applicable")

        generator_id = generator_operating_record.get("generator_id")
        scheduled_voltage_pu = generator_operating_record.get("scheduled_voltage_pu")
        actual_voltage_pu = generator_operating_record.get("actual_terminal_voltage_pu")
        top_defined_voltage_band = generator_operating_record.get("top_defined_voltage_band_pu")

        if scheduled_voltage_pu is None or actual_voltage_pu is None:
            pytest.skip("Voltage reference or measurement not recorded")

        # Use TOP-defined band if tighter than ±5%
        if top_defined_voltage_band is not None:
            tolerance_pu = top_defined_voltage_band
        else:
            tolerance_pu = scheduled_voltage_pu * MANUAL_MODE_VOLTAGE_TOLERANCE_FRACTION

        deviation_pu = abs(actual_voltage_pu - scheduled_voltage_pu)
        assert deviation_pu <= tolerance_pu, (
            f"Generator '{generator_id}' (manual AVR mode): terminal voltage "
            f"{actual_voltage_pu:.4f} pu deviates {deviation_pu:.4f} pu from scheduled "
            f"{scheduled_voltage_pu:.4f} pu — exceeds VAR-002-4.1 R3 tolerance of "
            f"±{tolerance_pu:.4f} pu (±{MANUAL_MODE_VOLTAGE_TOLERANCE_FRACTION:.0%} of scheduled)"
        )
```

---

## Open assumptions

| ID | Section | Summary | Review date |
|---|---|---|---|
| ASSUME-NERC-INT-001 | INT-006-4 | Curtailment priority order per Attachment 1: IROL (1) → SOL (2) → other reliability (3) → economic (4); reason code must be documented per curtailment action | 2026-05-21 |
| ASSUME-NERC-INT-002 | INT-009-2 | E-tag deviation tolerance: ±10 MW or ±1.5% of e-tagged MW per clock-hour, whichever is greater; unauthorized interchange must be curtailed immediately upon discovery | 2026-05-21 |
| ASSUME-NERC-IRO-001 | IRO-001-5 | RC directive authority: TOPs and BAs must comply or IMMEDIATELY notify RC with reason; non-compliance without notification is a violation; safety exception is narrow and must be documented | 2026-05-21 |
| ASSUME-NERC-IRO-002 | IRO-014-3 | Next-day OPA: at least once per operating day; must include SOL/IROL evaluation; problem notification must reach affected TOPs/BAs before the operating period begins | 2026-05-21 |
| ASSUME-NERC-VAR-001 | VAR-001-5 | RC establishes voltage schedules; TOP maintains within schedule; deviation for reliability reasons permissible with RC coordination and documentation; uncorrectable deviations must be reported to RC | 2026-05-21 |
| ASSUME-NERC-VAR-002 | VAR-002-4.1 | AVR automatic mode default; manual only for equipment failure, TOP directive, or testing; 2 calendar days for TOP notification of AVR out-of-service; ±5% voltage tolerance in manual mode (TOP limits override) | 2026-05-21 |

---

## Contested items

| Item | Reason | Resolution path |
|---|---|---|
| INT-006-4 curtailment priority determination | Whether a given transaction falls into "IROL exceedance" vs. "SOL exceedance" vs. "other reliability" priority requires real-time reliability assessment and may not be obvious in fast-moving operational events | RC real-time reliability assessment; documented in pre-curtailment event logs |
| IRO-014-3 OPA adequacy | Whether the next-day assessment adequately captures all potential SOL/IROL exceedances depends on the quality and completeness of the state estimator data and next-day load/generation forecast | RC data quality program; post-event review when forecast missed a constraint |
| VAR-001-5 voltage schedule feasibility | Whether maintaining the RC voltage schedule is possible given current network topology and reactive resource availability requires real-time engineering judgment; TOPs may legitimately deviate with RC coordination | RC/TOP coordination with documented basis |

---

## Cross-standard dependencies

| Artifact | Dependencies |
|---|---|
| RC directive to TOP/BA (IRO-001-5) | COM-002-4 — all RC directives must use three-part communication (issuer/receiver/repeat-back) regardless of the urgency; IRO-001 compliance and COM-002 compliance are concurrent obligations |
| E-tag deviations exceeding tolerance (INT-009-2) | EOP-004-4 — significant energy imbalance events may trigger EOP-004 event reporting; threshold depends on magnitude and reliability impact |
| Generator reactive output (VAR-001-5/VAR-002-4.1) | MOD-025-2 — generator reactive capability verified in P-Q test; VAR compliance depends on MOD-025 verification showing the generator can actually provide the reactive support being dispatched |
| AVR out-of-service (VAR-002-4.1) | TOP-001-4 — if AVR outage creates a reliability constraint, TOP must notify RC per TOP-001 SOL/IROL notification requirements |
| Next-day OPA findings (IRO-014-3) | TOP-001-4 / TOP-002-4 — when OPA identifies next-day constraint, it feeds into TOP operational planning (TOP-002) and the TOP's obligation to manage within SOLs (TOP-001) |
