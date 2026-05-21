# NERC Non-CIP — COM, TOP: Communications Protocols and Transmission Operations

**Registry path:** `/regulation-registry/NERC-OPS/COM-TOP/`
**Standards:** COM-002-4 (operating personnel communications protocols), TOP-001-4 (transmission operations)
**Last parsed:** 2026-05-21
**Overall confidence:** HIGH — COM-002 three-part communication and TOP-001 IROL/SOL authority obligations are DETERMINISTIC; both carry significant enforcement history and NERC Violation Risk Factor (VRF) of Medium or higher
**Applicable entities:** COM-002: RC, TOP, BA, GOP (issuer role); all operating entities receiving directives (receiver role) | TOP-001: Transmission Operators (TOP) and Reliability Coordinators (RC)

---

## Scope Pre-Conditions

```python
@pytest.fixture(autouse=True)
def require_bes_registered_entity(entity_scope: dict):
    registered_functions = entity_scope.get("registered_nerc_functions", [])
    if not registered_functions:
        pytest.skip("Entity has no registered NERC functional roles — tests not applicable")

def is_com002_issuer(entity_scope: dict) -> bool:
    issuer_roles = {"RC", "TOP", "BA", "GOP"}
    return bool(issuer_roles & set(entity_scope.get("registered_nerc_functions", [])))

def is_top_entity(entity_scope: dict) -> bool:
    return "TOP" in entity_scope.get("registered_nerc_functions", [])
```

---

## COM-002-4 — Operating Personnel Communications Protocols (DETERMINISTIC)

### Source excerpts

> **R3.** Each Issuer, when issuing a verbal or written directive in real-time operations to operate or change the operation of a BES Element or other Real-Time operational directives, shall require the recipient of the directive to repeat, restate, or rephrase the directive, and confirm that the repeated, restated, or rephrased directive was correct, or reissue the directive.
>
> **R4.** Each Receiver, upon receiving a verbal or written directive in real-time operations to operate or change the operation of a BES Element, shall repeat, restate, or rephrase the directive to the issuer and receive confirmation that the repeated, restated, or rephrased directive was correct before acting on the directive.

### Three-part communication protocol

COM-002-4 mandates three-part communication (issuer → receiver → confirmation) for all real-time operating directives. This is one of the most consistently cited NERC violations; failure is often due to habit or time pressure rather than ignorance of the requirement.

| Step | Actor | Required action | Classification |
|---|---|---|---|
| 1 — Issue | Issuer (RC/TOP/BA/GOP) | Issues directive verbally or in writing | DETERMINISTIC |
| 2 — Repeat-back | Receiver | Repeats, restates, or rephrases the directive back to issuer | DETERMINISTIC |
| 3 — Confirmation | Issuer | Confirms repeat-back was correct, or re-issues directive with correction | DETERMINISTIC |

**Critical: No action before confirmation.** The Receiver must NOT act on the directive until Step 3 confirmation is received.

### Directive vs. information exchange distinction

| Communication type | COM-002 applies? | Classification |
|---|---|---|
| Direct order to operate a BES Element (open/close breaker, adjust MW, shed load) | Yes — three-part required | DETERMINISTIC |
| Request for status information ("what is the MW output of unit 2?") | No — informational only | DETERMINISTIC |
| Announcement of a condition ("we have a fault on line 345") | No — informational only | DETERMINISTIC |
| Request to take an action on a BES Element ("reduce unit 3 to 200 MW") | Yes — three-part required | DETERMINISTIC |
| Transmission of pre-agreed switching order package | Yes — confirmation of receipt and intent to execute required | DETERMINISTIC |

**Assumption (ASSUME-NERC-COM-001):** Three-part communication compliance: (1) "directive" under COM-002 is any real-time communication instructing another entity's operating personnel to take an action that changes the state or output of a BES Element — includes MW redispatch, switching operations, load shedding, voltage schedule changes, and generation curtailment; (2) "real-time operations" means any communication outside of pre-planned and pre-approved switching procedures that have not yet been initiated; (3) a single complete failure of three-part communication (issuer acts after no repeat-back, or receiver acts without confirmation) constitutes a violation — no minimum frequency threshold; (4) for written directives: the written confirmation that the directive was received and understood satisfies the repeat-back requirement; (5) voice logging systems are the primary compliance evidence — voice logs retained per entity records policy (typically 90 days minimum); operating logs are secondary evidence; (6) three-part communication required for intra-company directives from RC to TOP, TOP to substation, and GOP to plant operator — not limited to inter-entity communications.

### Applicable entity roles

| Entity | Role in COM-002 | Requirement |
|---|---|---|
| Reliability Coordinator (RC) | Issuer (when directing TOPs/BAs) | Must use three-part; must confirm repeat-back |
| Transmission Operator (TOP) | Issuer (when directing substations/operators) or Receiver (when receiving from RC) | Three-part in both roles |
| Balancing Authority (BA) | Issuer (when directing generation dispatch) or Receiver | Three-part in both roles |
| Generator Operator (GOP) | Receiver (when receiving dispatch instructions from BA/TOP) | Must repeat-back; must receive confirmation before executing |

**Overall: DETERMINISTIC → Pattern 1**

---

### Test specifications — COM-002-4

```yaml
spec_id: NERC-COM-002-001
framework: NERC Reliability Standard COM-002-4
section: R3 (Issuer), R4 (Receiver)
confidence: HIGH
patterns_used:
  - Pattern 1 (DETERMINISTIC)
  - Pattern 2 (assumption-based)
scope_gate: is_nerc_registered_entity with COM-002 applicable role
assumptions:
  - ASSUME-NERC-COM-001  # Directive definition, real-time operations, voice log evidence
applicable_functions:
  issuer: [RC, TOP, BA, GOP]
  receiver: [TOP, BA, GO, GOP, any entity receiving real-time directives]
```

```python
import pytest
from datetime import datetime
from typing import Optional


@pytest.fixture(autouse=True)
def require_com002_applicable_entity(entity_scope: dict):
    applicable_roles = {"RC", "TOP", "BA", "GOP"}
    registered = set(entity_scope.get("registered_nerc_functions", []))
    if not (applicable_roles & registered):
        pytest.skip("Entity has no COM-002 applicable functional role — tests not applicable")


@pytest.mark.assumption(
    id="ASSUME-NERC-COM-001",
    description="Directive definition; three-part steps; voice log as primary evidence; written directive confirmation acceptable",
    approved_by="Compliance Officer",
    review_date="2026-05-21"
)
class TestCOM002ThreePartCommunication:

    def test_operating_procedure_requires_three_part_communication(self, operating_procedures: dict):
        """Written operating procedures must explicitly require three-part communication for all directives."""
        comm_section = operating_procedures.get("communications_protocol_section")
        assert comm_section, "Operating procedures have no communications protocol section"
        assert comm_section.get("three_part_communication_required"), (
            "Operating procedures do not explicitly require three-part communication for directives"
        )

    def test_voice_logging_system_is_operational(self, voice_logging_system: dict):
        """A voice logging system must be operational for real-time operations communications."""
        assert voice_logging_system.get("operational"), (
            "Voice logging system is not operational — COM-002 compliance evidence cannot be generated"
        )
        assert voice_logging_system.get("covers_operating_positions"), (
            "Voice logging does not cover all required operating positions"
        )

    def test_voice_log_retention_meets_minimum(self, voice_logging_system: dict):
        """Voice logs must be retained for the entity's compliance evidence retention period."""
        retention_days = voice_logging_system.get("retention_days")
        assert retention_days is not None, "Voice log retention period not documented"
        assert retention_days >= 90, (
            f"Voice log retention is {retention_days} days — minimum 90 days expected for COM-002 evidence"
        )

    def test_directive_log_entries_have_three_parts(self, directive_log_entry: dict):
        """Each logged directive must evidence all three COM-002-4 steps."""
        directive_id = directive_log_entry.get("directive_id")
        assert directive_log_entry.get("directive_issued_time"), (
            f"Directive {directive_id}: no directive issuance time recorded"
        )
        assert directive_log_entry.get("repeat_back_received"), (
            f"Directive {directive_id}: no repeat-back received recorded"
        )
        assert directive_log_entry.get("issuer_confirmed_correct"), (
            f"Directive {directive_id}: no issuer confirmation of correct repeat-back recorded"
        )

    def test_receiver_did_not_act_before_confirmation(self, directive_log_entry: dict):
        """Receiver must not execute the directive before receiving issuer confirmation."""
        action_time = directive_log_entry.get("action_executed_time")
        confirmation_time = directive_log_entry.get("issuer_confirmation_time")
        if not action_time or not confirmation_time:
            pytest.skip("Action and/or confirmation timestamps not available in log entry")
        if isinstance(action_time, str):
            action_time = datetime.fromisoformat(action_time)
        if isinstance(confirmation_time, str):
            confirmation_time = datetime.fromisoformat(confirmation_time)
        assert action_time >= confirmation_time, (
            f"Directive {directive_log_entry.get('directive_id')}: action executed at {action_time} "
            f"BEFORE issuer confirmation at {confirmation_time} — COM-002 R4 violation"
        )

    def test_operator_training_includes_three_part_communication(self, operator_training_record: dict):
        """Operator training must include COM-002 three-part communication protocol."""
        training_topics = operator_training_record.get("training_topics_covered", [])
        three_part_trained = any(
            "three-part" in topic.lower() or "com-002" in topic.lower() or
            "communications protocol" in topic.lower()
            for topic in training_topics
        )
        assert three_part_trained, (
            f"Operator {operator_training_record.get('operator_id')}: training records do not show "
            "three-part communication / COM-002 training"
        )
```

---

## TOP-001-4 — Transmission Operations (DETERMINISTIC for authority; PARAMETERIZED for SOL/IROL limits)

### Source excerpts

> **R1.** Each Transmission Operator shall operate to protect the reliability of the transmission system within its Transmission Operator Area, even if such operation may adversely affect the transmission system outside its area.
>
> **R3.** Each Transmission Operator shall comply with the reliability directives of its Reliability Coordinator, unless doing so would violate safety, equipment, regulatory, or statutory requirements, or unless the Transmission Operator has a reasonable basis to believe the directive would violate an applicable reliability standard.
>
> **R13.** Each Transmission Operator shall not knowingly violate an IROL or take an action that would knowingly result in an IROL violation.

### IROL vs. SOL framework

| Limit type | Definition | Consequence of violation | Classification |
|---|---|---|---|
| System Operating Limit (SOL) | Thermal, voltage, or stability limit established for the transmission system — may be violated temporarily with corrective action underway | Must initiate corrective action immediately; resolve within timeframe specified by RC | PARAMETERIZED (corrective action timeframe varies) |
| Interconnection Reliability Operating Limit (IROL) | SOL that, if violated, could lead to instability, separation, or cascading — NERC defines IROLs | Must not exceed IROL; if violated, must take immediate corrective action within specified time limit | DETERMINISTIC (no-exceed) |

### TOP-001 key obligations

| Requirement | Classification | Pattern |
|---|---|---|
| Comply with RC reliability directives | DETERMINISTIC — binary: complied or did not | Pattern 1 |
| Operate within IROLs — do not knowingly violate | DETERMINISTIC — no-exceed obligation | Pattern 1 |
| Initiate corrective action upon SOL violation | DETERMINISTIC for initiation; PARAMETERIZED for time-to-resolve | Pattern 2 |
| Written operating procedures for IROLs and SOLs within TOP area | DETERMINISTIC (existence) | Pattern 1 |
| Notify RC within specified timeframe when SOL exceeded or projected to exceed | DETERMINISTIC (notification obligation) | Pattern 1 |
| Maintain real-time monitoring capability for all IROLs within area | DETERMINISTIC (capability existence) | Pattern 1 |

**Assumption (ASSUME-NERC-TOP-001):** TOP-001 compliance is demonstrated when: (1) written list of all IROLs and SOLs applicable to the TOP area is maintained and updated when NERC or RC revises limits; (2) for each IROL, a documented corrective action procedure exists specifying the actions the TOP will take to return within limits — procedure tested through operating exercises or simulations; (3) real-time monitoring system provides continuous visibility of all IROL-relevant flows and voltages; alarm activated when loading approaches IROL (pre-IROL alert at operator-defined threshold, typically 90–95% of IROL); (4) RC directives received through normal operating channels are logged, acknowledged, and executed unless the limited exception applies (safety, equipment, regulatory, statutory, or defensible reliability standard conflict) — if exception invoked, TOP documents basis and notifies RC immediately; (5) when SOL is exceeded, notification to RC is made as soon as practicable — "as soon as practicable" interpreted as within 1 operating hour per NERC Operating Procedures; (6) TOP-001 R13 IROL no-exceed is the hardest bright-line obligation in transmission operations — knowing violation carries the highest VRF (High) in NERC's violation severity matrix.

### IROL notification timing

| Event | Required notification | Classification |
|---|---|---|
| SOL exceeded (actual) | Notify RC as soon as practicable | DETERMINISTIC |
| SOL projected to be exceeded within 30 minutes | Notify RC and initiate corrective action | DETERMINISTIC |
| IROL exceeded (actual) | Immediate RC notification; immediate corrective action | DETERMINISTIC |
| IROL projected to be exceeded | Immediate RC notification; corrective action before IROL is reached | DETERMINISTIC |

**Overall: DETERMINISTIC for IROL no-exceed and RC directive compliance → Pattern 1; PARAMETERIZED for corrective action timeframes and SOL procedure adequacy → Pattern 2**

---

### Test specifications — TOP-001-4

```yaml
spec_id: NERC-TOP-001-001
framework: NERC Reliability Standard TOP-001-4
sections:
  - R1 (operate to protect reliability)
  - R3 (comply with RC directives)
  - R13 (IROL no-exceed)
confidence: HIGH (IROL/directive obligations) / MEDIUM (SOL corrective action)
patterns_used:
  - Pattern 1 (DETERMINISTIC)
  - Pattern 2 (assumption-based)
scope_gate: registered_nerc_function includes TOP
assumptions:
  - ASSUME-NERC-TOP-001
```

```python
@pytest.fixture(autouse=True)
def require_top_registration(entity_scope: dict):
    if "TOP" not in entity_scope.get("registered_nerc_functions", []):
        pytest.skip("Entity is not a registered Transmission Operator — TOP-001 not applicable")


@pytest.mark.assumption(
    id="ASSUME-NERC-TOP-001",
    description="IROL/SOL list maintenance; corrective action procedures; RC directive logging; SOL notification within 1 operating hour",
    approved_by="Compliance Officer",
    review_date="2026-05-21"
)
class TestTOP001TransmissionOperations:

    def test_irol_list_is_documented(self, top_operating_data: dict):
        """TOP must have a documented list of all IROLs applicable to its area."""
        irol_list = top_operating_data.get("irol_list")
        assert irol_list, "No documented IROL list found for TOP area"
        assert top_operating_data.get("irol_list_review_date"), (
            "IROL list has no documented review date — must be kept current with NERC/RC revisions"
        )

    def test_sol_list_is_documented(self, top_operating_data: dict):
        """TOP must have a documented list of all SOLs applicable to its area."""
        sol_list = top_operating_data.get("sol_list")
        assert sol_list, "No documented SOL list found for TOP area"

    def test_irol_corrective_action_procedures_exist(self, top_operating_data: dict):
        """Written corrective action procedures must exist for each IROL."""
        irol_list = top_operating_data.get("irol_list", [])
        for irol in irol_list:
            assert irol.get("corrective_action_procedure_id"), (
                f"IROL '{irol.get('irol_id')}': no corrective action procedure documented"
            )

    def test_irol_monitoring_alarm_configured(self, top_operating_data: dict):
        """Real-time monitoring system must have pre-IROL alert configured for each IROL."""
        irol_list = top_operating_data.get("irol_list", [])
        for irol in irol_list:
            assert irol.get("monitoring_alarm_configured"), (
                f"IROL '{irol.get('irol_id')}': no real-time monitoring alarm configured"
            )

    def test_no_irol_violations_unmitigated(self, irol_event_log: list):
        """Any IROL violation must have an immediate corrective action logged."""
        for event in irol_event_log:
            if event.get("irol_violated"):
                assert event.get("corrective_action_initiated"), (
                    f"IROL violation event {event.get('event_id')} has no corrective action logged"
                )
                assert event.get("rc_notified"), (
                    f"IROL violation event {event.get('event_id')}: no RC notification logged"
                )

    def test_rc_directives_are_logged(self, rc_directive_log: list):
        """All RC directives received must be logged."""
        for directive in rc_directive_log:
            assert directive.get("received_time"), (
                f"RC directive {directive.get('directive_id')} has no received timestamp"
            )
            assert directive.get("disposition") in {"executed", "exception_invoked"}, (
                f"RC directive {directive.get('directive_id')}: disposition must be 'executed' or "
                "'exception_invoked', got '{directive.get('disposition')}'"
            )

    def test_rc_directive_exception_has_documented_basis(self, rc_directive_log: list):
        """Any RC directive not executed must have a documented exception basis."""
        for directive in rc_directive_log:
            if directive.get("disposition") == "exception_invoked":
                assert directive.get("exception_basis"), (
                    f"RC directive {directive.get('directive_id')}: exception invoked but no basis documented"
                )
                valid_bases = {"safety", "equipment", "regulatory", "statutory", "reliability_standard_conflict"}
                assert directive.get("exception_category") in valid_bases, (
                    f"RC directive {directive.get('directive_id')}: exception category "
                    f"'{directive.get('exception_category')}' is not a valid TOP-001 R3 exception"
                )

    def test_sol_exceedance_notification_timeliness(self, sol_event: dict):
        """SOL exceedances must be notified to RC as soon as practicable (≤1 operating hour)."""
        if not sol_event.get("sol_exceeded"):
            pytest.skip("No SOL exceedance in this event — not applicable")
        aware_time = sol_event.get("awareness_time")
        notification_time = sol_event.get("rc_notification_time")
        if not aware_time or not notification_time:
            pytest.skip("Timestamps not available for SOL notification timeliness check")
        if isinstance(aware_time, str):
            aware_time = datetime.fromisoformat(aware_time)
        if isinstance(notification_time, str):
            notification_time = datetime.fromisoformat(notification_time)
        elapsed_minutes = (notification_time - aware_time).total_seconds() / 60
        assert elapsed_minutes <= 60, (
            f"SOL exceedance event {sol_event.get('event_id')}: RC notification took {elapsed_minutes:.1f} "
            "minutes (threshold: ≤60 minutes / 1 operating hour)"
        )
```

---

## Assumption registry (this file)

| ID | Standard | Summary | Review date |
|---|---|---|---|
| ASSUME-NERC-COM-001 | COM-002-4 | Three-part communication: directive definition, steps, voice log as primary evidence, written confirmation acceptable, intra-company scope | 2026-05-21 |
| ASSUME-NERC-TOP-001 | TOP-001-4 | IROL/SOL list currency, corrective action procedures per IROL, SOL notification within 1 operating hour, RC directive exception documentation | 2026-05-21 |

---

## Cross-references

- **COM-002 → TOP-001:** TOP-to-substation directives are subject to COM-002 three-part communication; TOP-001 RC directive compliance requires the same three-part protocol for RC-to-TOP directives
- **COM-002 → EOP-004:** Emergency directives during BES events must use three-part communication even under time pressure — COM-002 has no emergency exception
- **TOP-001 R3 → IRO-001-5:** The RC authority to issue reliability directives is established in IRO-001-5; TOP-001 R3 is the corresponding compliance obligation on the receiver side
- **TOP-001 R13 → FAC-008-3:** IROL values are derived from facility ratings; an incorrect FAC-008 rating methodology can produce an incorrect IROL — indirect compliance dependency
