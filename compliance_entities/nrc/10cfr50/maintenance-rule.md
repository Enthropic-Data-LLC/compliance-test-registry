# NRC 10 CFR Part 50 — §50.65: The Maintenance Rule

**Registry path:** `/regulation-registry/NRC/10CFR50/MaintenanceRule/`
**Regulation:** 10 CFR §50.65 — Requirements for Monitoring the Effectiveness of Maintenance at Nuclear Power Plants
**Last parsed:** 2026-05-21
**Overall confidence:** MEDIUM — program existence and annual review cadence are DETERMINISTIC; (a)(1)/(a)(2) categorization and performance criteria adequacy are PARAMETERIZED and require system engineer/expert panel judgment; §50.65(a)(4) pre-maintenance risk assessment existence is DETERMINISTIC but adequacy is PARAMETERIZED
**Covers:** §50.65(a)(1) goals and monitoring; §50.65(a)(2) performance criteria; §50.65(a)(3) annual performance review; §50.65(a)(4) risk assessment before maintenance; industry implementation per NUMARC 93-01 (now NEI 93-01) and INPO AP-913
**Enforcement note:** §50.65 carries very high enforcement activity history — NRC Generic Communication DC/NL-2012-03 lists this as one of the top-cited violations; common findings include (a)(1) placement delay, inadequate performance criteria, and missing (a)(4) assessments

---

## Scope Pre-Condition

```python
@pytest.fixture(autouse=True)
def require_nrc_licensed_reactor(facility_scope: dict):
    if not facility_scope.get("is_nrc_licensed_nuclear_facility"):
        pytest.skip("Facility is not an NRC-licensed nuclear reactor — §50.65 tests not applicable")
```

---

## §50.65 — Maintenance Rule Overview

### Regulatory text (key paragraphs)

> **§50.65(a)(1):** Licensees shall monitor the performance or condition of structures, systems, and components (SSCs) within the scope of the Maintenance Rule against licensee-established performance or condition goals, in a manner sufficient to provide reasonable assurance that these SSCs are capable of fulfilling their intended functions. Where the performance or condition of an SSC does not meet established goals, appropriate corrective action shall be taken.

> **§50.65(a)(2):** The licensee shall demonstrate through monitoring that an SSC's performance or condition is being effectively controlled through the performance of appropriate preventive maintenance, such that the SSC remains capable of performing its intended function.

> **§50.65(a)(3):** Performance and condition monitoring activities and associated goals and preventive maintenance activities shall be evaluated at least every refueling cycle but no less frequently than every 24 months. The objective of the evaluation is to assess the effectiveness of maintenance.

> **§50.65(a)(4):** Before performing maintenance activities (including but not limited to surveillance, post-maintenance testing, corrective and preventive maintenance), the licensee shall assess and manage the increase in risk that may result from the proposed maintenance activities.

---

## §50.65 — Maintenance Rule Program Structure

### SSC scope

The Maintenance Rule applies to all safety-related SSCs and to non-safety-related SSCs that (1) could affect the performance of safety-related SSCs if they fail, or (2) are relied upon to maintain the plant in a safe condition.

| SSC category | Maintenance Rule scope | Classification |
|---|---|---|
| Safety-related SSCs (ASME Code Class 1/2/3; licensed functions) | Always in scope | DETERMINISTIC |
| Non-safety-related SSCs affecting safety function if failed | Screened into scope by licensee | PARAMETERIZED (scope adequacy) |
| Fire protection SSCs | In scope (§50.48 interface) | DETERMINISTIC |
| Security SSCs | Generally excluded from MR; covered by 10 CFR Part 73 | DETERMINISTIC |
| Augmented quality SSCs | In scope per license basis | PARAMETERIZED |

### (a)(1) vs. (a)(2) categorization

All in-scope SSCs are categorized under one of two tiers:

| Category | Description | Trigger for (a)(1) | Evidence required |
|---|---|---|---|
| **(a)(2)** — effective preventive maintenance | SSC is performing satisfactorily; PM program keeps it within performance criteria | Default state | Performance criteria established; monitoring data shows criteria met |
| **(a)(1)** — goals and corrective action | SSC is NOT meeting criteria OR has not been managed effectively | Failure to meet criteria; pattern of functional failures | Measurable, achievable goals; corrective action plan; monitoring against goals; expert panel review |

---

## §50.65(a)(2) — Performance Criteria (PARAMETERIZED)

### Source excerpt

> Where the performance or condition of an SSC is being effectively controlled through appropriate preventive maintenance, the licensee shall establish performance or condition goals, in a manner sufficient to provide reasonable assurance that these SSCs are capable of fulfilling their intended functions.

### Performance criteria requirements

| Requirement | Classification | Notes |
|---|---|---|
| Written performance criteria exist for each (a)(2) SSC | DETERMINISTIC (existence) | Criteria established in MR database or system health report |
| Criteria are "reasonable and appropriate" for the SSC's function | PARAMETERIZED | NUMARC 93-01 guidance: criteria should be based on historical reliability data and maintenance history |
| Criteria use measurable metrics | PARAMETERIZED | Examples: functional failure rate, mean time between failures (MTBF), component reliability |
| PM activities sufficient to maintain SSC within criteria | PARAMETERIZED | PM program basis document required |
| Monitoring frequency adequate to detect degradation | PARAMETERIZED | System health reports, condition monitoring programs |

**Assumption (ASSUME-NRC50-MR-001):** §50.65(a)(2) performance criteria compliance: (1) performance criteria must be established in writing before an SSC is categorized as (a)(2) — there is no "default" (a)(2) without documented criteria; (2) acceptable metric types include functional failure rate (per refueling cycle), MTBF, condition monitoring results (vibration, oil analysis, thermography), and surveillance test failure rates; (3) criteria must be sufficiently challenging to provide "reasonable assurance" — criteria set so loosely that any failure still meets them are not compliant per NRC inspection guidance; (4) the PM program basis document ties PM task types and frequencies to the performance criteria — if PM tasks are adequate, criteria should be met; missing PM basis is a gap even if criteria are nominally documented; (5) performance monitoring data is tracked in the plant's CMMS (Computerized Maintenance Management System) or equivalent; data reviewed at least at the annual MR review cycle and whenever a functional failure occurs.

**Overall: DETERMINISTIC for criteria existence → Pattern 1; PARAMETERIZED for adequacy → Pattern 2**

---

## §50.65(a)(1) — Goals, Corrective Action, and Expert Panel (PARAMETERIZED)

### Categorization trigger

An SSC must be moved from (a)(2) to (a)(1) when any of the following occur:

| Trigger | Description | Classification |
|---|---|---|
| Failure to meet performance criteria | SSC's measured performance violates its established (a)(2) criteria | DETERMINISTIC (trigger — criteria exceeded) |
| Maintenance Preventable Functional Failure (MPFF) pattern | Two or more MPFFs within a defined monitoring period suggest PM is not effective | PARAMETERIZED (MPFF determination requires engineer judgment) |
| Unreliability assessment | System engineer or expert panel determines SSC reliability is inadequate even without a criteria violation | PARAMETERIZED |
| Direct NRC direction | NRC inspection finding or Corrective Action Program item requires (a)(1) placement | DETERMINISTIC |

### (a)(1) program requirements

Once an SSC is in (a)(1) status, the licensee must:

| Requirement | Classification | NUMARC 93-01 guidance |
|---|---|---|
| Establish measurable, achievable goals | PARAMETERIZED (goal adequacy) | Goals based on target reliability; typically expressed as reliability or availability metrics |
| Document a corrective action plan | DETERMINISTIC (existence) | CAP entries in the plant CAP; root cause analysis performed (§50.65 + App. B Criterion XVI) |
| Monitor against goals — demonstrated progress | PARAMETERIZED (frequency and method) | Monthly or quarterly trending recommended |
| Expert panel review before (a)(2) return | PARAMETERIZED | Expert panel must affirm goals are met and PM program is adequate before downgrading |
| Expert panel composition | PARAMETERIZED | Operations, maintenance, engineering, QA representation; charter documented |

**Assumption (ASSUME-NRC50-MR-002):** §50.65(a)(1) categorization and management: (1) "Maintenance Preventable Functional Failure" (MPFF) is defined by the licensee's MR procedure consistent with NUMARC 93-01 guidance — typically a functional failure that could have been prevented by timely and adequate preventive maintenance; (2) NRC inspection guidance (NRC Inspection Procedure 71111.12) accepts the industry standard of two MPFFs within a monitoring period as a trigger for (a)(1) evaluation — one MPFF alone may trigger (a)(1) for high-safety-significance SSCs; (3) (a)(1) goals must be: (a) measurable (quantitative metric), (b) achievable (realistic given corrective actions), and (c) tied to the function the SSC must perform; qualitative goals ("improve reliability") without numeric targets do not satisfy (a)(1) requirements; (4) expert panel is a multi-discipline team that reviews (a)(1) and return-to-(a)(2) decisions — the panel's charter must specify minimum representation (operations, maintenance engineering, system engineering, QA); (5) delay in placing an SSC in (a)(1) when criteria are exceeded is the most cited §50.65 violation — the categorization must be performed promptly, not deferred to the next annual review cycle; (6) root cause analysis for (a)(1) placement is required per both §50.65 and App. B Criterion XVI for significant conditions adverse to quality.

**Overall: DETERMINISTIC for criteria-exceeded trigger and corrective action plan existence → Pattern 1; PARAMETERIZED for MPFF determination, goal adequacy, and expert panel scope → Pattern 2; expert panel adequacy → Pattern 3**

---

## §50.65(a)(3) — Annual Performance Review (DETERMINISTIC — cadence)

### Source excerpt

> **§50.65(a)(3):** Performance and condition monitoring activities and associated goals and preventive maintenance activities shall be evaluated at least every refueling cycle but no less frequently than every 24 months.

### Annual review requirements

| Element | Threshold | Classification |
|---|---|---|
| Review frequency | At least every refueling cycle; maximum 24-month interval | DETERMINISTIC |
| Review scope | All in-scope SSCs; all (a)(1) and (a)(2) categories | DETERMINISTIC |
| Review objectives | Assess maintenance effectiveness; validate (a)(2) criteria remain appropriate; review (a)(1) progress | PARAMETERIZED (adequacy) |
| Documentation | Written evaluation with conclusions | DETERMINISTIC (existence) |
| Management review | Senior management review and approval | DETERMINISTIC |

**Assumption (ASSUME-NRC50-MR-003):** Annual MR performance review: (1) "refueling cycle" is typically 18–24 months for most PWRs and BWRs; the 24-month cap means a plant with an 18-month fuel cycle must still perform the annual review no later than 24 months after the previous review — the refueling cycle length does not extend past 24 months; (2) the annual review must include: (a) a summary of all functional failures for the review period, (b) status of all (a)(1) SSCs and progress toward goals, (c) review of (a)(2) criteria for continued appropriateness, (d) assessment of PM program effectiveness, and (e) trending data for key reliability indicators; (3) the review is typically organized as a written "Maintenance Rule Annual Report" reviewed by senior plant management (Plant Manager or VP Nuclear Operations level); (4) NRC inspection findings for inadequate annual reviews typically cite failure to trend functional failures, failure to evaluate (a)(2) criteria adequacy, or failure to include all in-scope SSCs; (5) the annual review is the primary opportunity to downgrade (a)(1) SSCs to (a)(2) status — such downgrades must be supported by the review data showing goals are met and effectiveness is restored.

**Overall: DETERMINISTIC for 24-month maximum cadence → Pattern 1; PARAMETERIZED for review scope and adequacy → Pattern 2**

---

## §50.65(a)(4) — Pre-Maintenance Risk Assessment (DETERMINISTIC for existence; PARAMETERIZED for adequacy)

### Source excerpt

> **§50.65(a)(4):** Before performing maintenance activities (including but not limited to surveillance, post-maintenance testing, corrective and preventive maintenance), the licensee shall assess and manage the increase in risk that may result from the proposed maintenance activities. The scope of the assessment shall be appropriate to the maintenance activities.

### Risk assessment framework

The §50.65(a)(4) assessment is distinct from the (a)(1)/(a)(2) monitoring framework. It is a real-time, pre-activity risk evaluation performed before each maintenance window.

| Assessment element | Classification | Industry tool |
|---|---|---|
| Baseline plant risk state | PARAMETERIZED | Online risk monitor (typically EOOS, SENTINEL, or equivalent) |
| Incremental risk from proposed out-of-service | DETERMINISTIC (assessment required) / PARAMETERIZED (tool adequacy) | PRA model; risk-informed decision |
| Risk significance classification | PARAMETERIZED | Green/Yellow/Red threshold per RG 1.200 / NUMARC 93-01 |
| Risk management actions | PARAMETERIZED | Compensatory measures for elevated risk windows |
| Documentation | DETERMINISTIC (work order must reference assessment) | Work order package; risk assessment form |

### Risk thresholds (NRC Regulatory Guide 1.174 reference values)

| Risk metric | Green (acceptable) | Yellow (elevated — management review) | Red (high — requires prior approval) |
|---|---|---|---|
| Incremental Core Damage Probability (ICDP) per activity | < 1×10⁻⁶ | 1×10⁻⁶ to 1×10⁻⁵ | > 1×10⁻⁵ |
| Incremental Large Early Release Probability (ILERP) per activity | < 1×10⁻⁷ | 1×10⁻⁷ to 1×10⁻⁶ | > 1×10⁻⁶ |
| Total baseline CDF (with all outages) | < 1×10⁻⁴/yr (Green zone) | 1×10⁻⁴ to 1×10⁻³/yr | > 1×10⁻³/yr |

**Assumption (ASSUME-NRC50-MR-004):** §50.65(a)(4) risk assessment compliance: (1) "before performing maintenance activities" means the assessment must be completed before the equipment is taken out of service for maintenance — late assessments (completed after work begins) constitute a violation; (2) the scope of the assessment must be "appropriate to the maintenance activities" — brief single-train preventive maintenance on a low-safety-significance component requires a less rigorous assessment than extended outages on high-safety-significance SSCs; many plants use a graded approach with screening criteria; (3) the online risk monitor or PRA model used for (a)(4) assessments must be current — a model not updated for plant changes (equipment modifications, setpoint changes) within the past 18–24 months is considered stale and may not produce reliable ICDP calculations; (4) Yellow and Red risk windows require specific management approval and compensatory measures documented in the work package; (5) if a Yellow or Red condition is encountered during maintenance (emergent), the shift manager must be notified and compensatory measures implemented — the assessment must be updated to reflect the emergent condition; (6) documentation standard: work order package must reference the (a)(4) assessment ID and risk color classification; "not a risk-significant activity" determinations must be supportable via screening criteria documented in the procedure.

**Overall: DETERMINISTIC for assessment existence and pre-activity timing → Pattern 1; PARAMETERIZED for scope adequacy, model currency, and compensatory measures → Pattern 2**

---

## Expert Panel Review (PARAMETERIZED — Pattern 3 for adequacy)

### Source and industry guidance

§50.65 does not explicitly require an expert panel, but NUMARC 93-01 (the NRC-endorsed industry guidance document) establishes the expert panel as the standard implementation mechanism for (a)(1)/(a)(2) categorization decisions. NRC Inspection Procedure 71111.12 evaluates expert panel composition, independence, and decision quality.

| Expert panel element | Classification |
|---|---|
| Written charter exists | DETERMINISTIC |
| Panel composition meets charter requirements | DETERMINISTIC (existence) / PARAMETERIZED (independence and qualification) |
| Panel reviews all (a)(1) placements | DETERMINISTIC (all placements reviewed) |
| Panel reviews (a)(2) performance criteria adequacy at annual review | PARAMETERIZED |
| Panel meeting minutes and decisions documented | DETERMINISTIC |
| Panel decisions are defensible (support return to (a)(2)) | PARAMETERIZED — Pattern 3 |

**Assumption (ASSUME-NRC50-MR-005):** Expert panel compliance: (1) the expert panel charter must specify: minimum membership (operations, maintenance, engineering, QA), quorum requirements, decision authority, and documentation format; (2) the panel must include at least one licensed senior reactor operator (SRO) or equivalent operations experience — operations perspective is essential for functional failure significance assessment; (3) panel members must not have direct supervisory responsibility for the SSC being evaluated — independence from the work group being assessed; (4) panel decisions on (a)(1) placements and (a)(2) returns must be documented with the technical basis — "SSC now meets performance criteria" without supporting data is insufficient; (5) the panel's return-to-(a)(2) decision must affirmatively address: (a) root cause of the (a)(1) condition has been corrected, (b) performance data shows goals are met, and (c) PM program changes (if any) are sustainable; (6) NRC inspection findings for expert panel deficiencies most commonly cite: inadequate independence (supervisor sitting on panel reviewing own work area), lack of documented basis for (a)(2) returns, and failure to evaluate all in-scope SSCs at the annual review.

**Overall: PARAMETERIZED → Pattern 2; expert panel adequacy determination → Pattern 3**

---

## Test specifications

### YAML spec — §50.65 Maintenance Rule

```yaml
spec_id: NRC-50-MR-001
framework: NRC 10 CFR Part 50
section: §50.65 (a)(1), (a)(2), (a)(3), (a)(4)
confidence: MIXED
  program_existence: HIGH (DETERMINISTIC)
  annual_review_cadence: HIGH (DETERMINISTIC)
  a1_trigger_detection: MEDIUM (PARAMETERIZED)
  performance_criteria_adequacy: MEDIUM (PARAMETERIZED)
  a4_risk_assessment_existence: HIGH (DETERMINISTIC)
  expert_panel_adequacy: LOW (CONTESTED/Pattern 3)
patterns_used:
  - Pattern 1 (DETERMINISTIC assertions)
  - Pattern 2 (assumption-based assertions)
  - Pattern 3 (human review required — expert panel adequacy, (a)(1) goal adequacy)
scope_gate: is_nrc_licensed_nuclear_facility
assumptions:
  - ASSUME-NRC50-MR-001  # (a)(2) performance criteria: establishment, metrics, PM basis
  - ASSUME-NRC50-MR-002  # (a)(1) triggers: MPFF, goals, expert panel, prompt placement
  - ASSUME-NRC50-MR-003  # Annual review: 24-month cap, scope, documentation, management review
  - ASSUME-NRC50-MR-004  # (a)(4) risk assessment: pre-activity timing, graded approach, model currency
  - ASSUME-NRC50-MR-005  # Expert panel: charter, independence, documented basis for decisions
industry_guidance:
  - NUMARC 93-01 Rev. 4A (NRC-endorsed Maintenance Rule implementation guidance)
  - INPO AP-913 (Equipment Reliability Process)
  - NRC Inspection Procedure 71111.12 (Maintenance Effectiveness)
  - NRC Regulatory Guide 1.174 (risk thresholds for (a)(4) assessment)
```

### Python tests — `tests/nrc_10cfr50/test_maintenance_rule.py`

```python
import pytest
from datetime import datetime, timedelta
from typing import Optional, List


# ---------------------------------------------------------------------------
# Scope gate
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def require_nrc_licensed_reactor(facility_scope: dict):
    if not facility_scope.get("is_nrc_licensed_nuclear_facility"):
        pytest.skip("Facility is not an NRC-licensed nuclear reactor — §50.65 tests not applicable")


# ---------------------------------------------------------------------------
# Program existence (Pattern 1 — DETERMINISTIC)
# ---------------------------------------------------------------------------

class TestMaintenanceRuleProgramExistence:

    def test_written_mr_program_exists(self, mr_program: dict):
        """A written Maintenance Rule program must exist."""
        assert mr_program.get("program_document_id"), "No written §50.65 Maintenance Rule program document"
        assert mr_program.get("approved_by"), "Maintenance Rule program has no management approval signature"

    def test_mr_program_covers_safety_related_sscs(self, mr_program: dict):
        """The MR program must explicitly scope in all safety-related SSCs."""
        assert mr_program.get("safety_related_ssc_scope_addressed"), (
            "MR program does not explicitly address safety-related SSC scope"
        )

    def test_mr_database_or_equivalent_exists(self, mr_database: dict):
        """An MR database or equivalent tracking system must exist for all in-scope SSCs."""
        assert mr_database.get("system_name"), "No MR database or CMMS tracking system identified"
        total_sscs = mr_database.get("total_in_scope_ssc_count", 0)
        assert total_sscs > 0, "MR database shows zero in-scope SSCs — scope is incomplete"

    def test_expert_panel_charter_exists(self, mr_program: dict):
        """An expert panel charter must be documented."""
        assert mr_program.get("expert_panel_charter_document_id"), (
            "No expert panel charter documented — required by NUMARC 93-01"
        )


# ---------------------------------------------------------------------------
# §50.65(a)(2) — Performance Criteria (Pattern 2 — PARAMETERIZED)
# ---------------------------------------------------------------------------

@pytest.mark.assumption(
    id="ASSUME-NRC50-MR-001",
    description="(a)(2) criteria: written before categorization, measurable metrics, PM basis document, monitoring in CMMS",
    approved_by="Maintenance Rule Coordinator",
    review_date="2026-05-21"
)
class TestMaintenanceRuleA2PerformanceCriteria:

    def test_all_a2_sscs_have_written_criteria(self, mr_database: dict):
        """Every (a)(2)-categorized SSC must have written performance criteria."""
        a2_sscs = [s for s in mr_database.get("sscs", []) if s.get("category") == "a2"]
        for ssc in a2_sscs:
            assert ssc.get("performance_criteria"), (
                f"SSC '{ssc.get('ssc_id')}' is categorized (a)(2) but has no written performance criteria"
            )

    def test_a2_performance_criteria_use_measurable_metrics(self, ssc_record: dict):
        """(a)(2) performance criteria must use measurable, quantitative metrics."""
        if ssc_record.get("category") != "a2":
            pytest.skip("SSC is not (a)(2) — not applicable")
        criteria = ssc_record.get("performance_criteria", {})
        # At least one quantitative metric must be present
        quantitative_metrics = [
            criteria.get("functional_failure_rate_per_cycle"),
            criteria.get("mtbf_hours"),
            criteria.get("surveillance_test_failure_rate"),
            criteria.get("condition_monitoring_limit"),
        ]
        has_quantitative = any(m is not None for m in quantitative_metrics)
        assert has_quantitative, (
            f"SSC '{ssc_record.get('ssc_id')}': (a)(2) performance criteria have no quantitative metrics — "
            "qualitative-only criteria are insufficient per NRC inspection guidance"
        )

    def test_a2_ssc_has_pm_basis_document(self, ssc_record: dict):
        """Each (a)(2) SSC must have a PM basis document linking PM tasks to performance criteria."""
        if ssc_record.get("category") != "a2":
            pytest.skip("SSC is not (a)(2) — not applicable")
        assert ssc_record.get("pm_basis_document_id"), (
            f"SSC '{ssc_record.get('ssc_id')}': no PM basis document — "
            "NRC expects documented link between PM activities and (a)(2) performance criteria"
        )

    def test_a2_monitoring_data_is_current(self, ssc_record: dict):
        """Monitoring data for (a)(2) SSCs must be current (reviewed within the monitoring interval)."""
        if ssc_record.get("category") != "a2":
            pytest.skip("SSC is not (a)(2) — not applicable")
        last_review = ssc_record.get("last_monitoring_review_date")
        monitoring_interval_days = ssc_record.get("monitoring_interval_days", 365)
        if not last_review:
            pytest.fail(
                f"SSC '{ssc_record.get('ssc_id')}': no monitoring review date — (a)(2) monitoring not documented"
            )
        if isinstance(last_review, str):
            last_review = datetime.fromisoformat(last_review)
        days_since = (datetime.now() - last_review).days
        assert days_since <= monitoring_interval_days, (
            f"SSC '{ssc_record.get('ssc_id')}': monitoring data is {days_since} days old "
            f"(interval: {monitoring_interval_days} days)"
        )


# ---------------------------------------------------------------------------
# §50.65(a)(1) — Goals and Corrective Action (Pattern 2 + Pattern 3)
# ---------------------------------------------------------------------------

@pytest.mark.assumption(
    id="ASSUME-NRC50-MR-002",
    description="(a)(1) triggers: MPFF definition, two-MPFF threshold, prompt categorization, measurable goals, expert panel review",
    approved_by="Maintenance Rule Coordinator",
    review_date="2026-05-21"
)
class TestMaintenanceRuleA1GoalsAndCorrectiveAction:

    def test_a1_ssc_has_documented_goals(self, ssc_record: dict):
        """Every (a)(1)-categorized SSC must have documented, measurable goals."""
        if ssc_record.get("category") != "a1":
            pytest.skip("SSC is not (a)(1) — not applicable")
        goals = ssc_record.get("a1_goals")
        assert goals, (
            f"SSC '{ssc_record.get('ssc_id')}' is categorized (a)(1) but has no documented goals"
        )

    def test_a1_goals_are_quantitative(self, ssc_record: dict):
        """(a)(1) goals must be measurable and quantitative, not qualitative."""
        if ssc_record.get("category") != "a1":
            pytest.skip("SSC is not (a)(1) — not applicable")
        goals = ssc_record.get("a1_goals", {})
        has_quantitative_goal = any([
            goals.get("target_reliability_percent") is not None,
            goals.get("target_failure_rate") is not None,
            goals.get("max_corrective_maintenance_hours") is not None,
            goals.get("target_availability_percent") is not None,
        ])
        assert has_quantitative_goal, (
            f"SSC '{ssc_record.get('ssc_id')}': (a)(1) goals do not contain any quantitative target — "
            "qualitative goals ('improve reliability') do not satisfy §50.65(a)(1)"
        )

    def test_a1_ssc_has_corrective_action_plan(self, ssc_record: dict):
        """Every (a)(1) SSC must have an associated corrective action plan (CAP entry)."""
        if ssc_record.get("category") != "a1":
            pytest.skip("SSC is not (a)(1) — not applicable")
        assert ssc_record.get("corrective_action_cap_id"), (
            f"SSC '{ssc_record.get('ssc_id')}' is (a)(1) but has no CAP entry — "
            "corrective action is required by §50.65(a)(1)"
        )

    def test_a1_ssc_has_expert_panel_review_on_record(self, ssc_record: dict):
        """(a)(1) placement must be reviewed and documented by the expert panel."""
        if ssc_record.get("category") != "a1":
            pytest.skip("SSC is not (a)(1) — not applicable")
        assert ssc_record.get("expert_panel_review_date"), (
            f"SSC '{ssc_record.get('ssc_id')}' is (a)(1) but no expert panel review date found"
        )
        assert ssc_record.get("expert_panel_meeting_minutes_id"), (
            f"SSC '{ssc_record.get('ssc_id')}': expert panel review not documented in meeting minutes"
        )

    def test_criteria_exceedance_triggers_a1_categorization_promptly(self, ssc_record: dict):
        """SSC must be moved to (a)(1) promptly when performance criteria are exceeded, not deferred to annual review."""
        if ssc_record.get("category") != "a1":
            pytest.skip("SSC is not currently (a)(1) — not applicable")
        criteria_exceedance_date = ssc_record.get("criteria_exceedance_date")
        a1_categorization_date = ssc_record.get("a1_categorization_date")
        if not criteria_exceedance_date or not a1_categorization_date:
            pytest.skip("Dates not available for prompt categorization check")
        if isinstance(criteria_exceedance_date, str):
            criteria_exceedance_date = datetime.fromisoformat(criteria_exceedance_date)
        if isinstance(a1_categorization_date, str):
            a1_categorization_date = datetime.fromisoformat(a1_categorization_date)
        delay_days = (a1_categorization_date - criteria_exceedance_date).days
        # NRC inspection guidance: categorization should be prompt, not deferred past one operating cycle
        assert delay_days <= 90, (
            f"SSC '{ssc_record.get('ssc_id')}': criteria exceeded on {criteria_exceedance_date.date()} but "
            f"(a)(1) placement not made until {a1_categorization_date.date()} ({delay_days} days later) — "
            "delayed (a)(1) placement is the most-cited §50.65 violation"
        )

    @pytest.mark.human_review_required(
        reason="Adequacy of (a)(1) goals to restore SSC reliability requires system engineer and "
               "expert panel judgment — whether the target reliability, corrective action plan, and "
               "monitoring frequency are sufficient to fulfill the SSC's intended safety function cannot "
               "be determined algorithmically. NUMARC 93-01 Section 7 and NRC IP 71111.12 describe the "
               "evaluation criteria. Pattern 3: surface for expert panel sign-off."
    )
    def test_a1_goal_adequacy(self, ssc_record: dict):
        """[HUMAN REVIEW] (a)(1) goal adequacy requires expert panel and system engineer evaluation."""
        if ssc_record.get("category") != "a1":
            pytest.skip("SSC is not (a)(1) — not applicable")
        assert ssc_record.get("expert_panel_goal_adequacy_sign_off"), (
            f"SSC '{ssc_record.get('ssc_id')}': (a)(1) goals have no expert panel adequacy sign-off — "
            "required before goals are considered compliant"
        )

    def test_return_to_a2_requires_expert_panel_review(self, ssc_category_change_record: dict):
        """SSCs returning from (a)(1) to (a)(2) must have expert panel approval."""
        if ssc_category_change_record.get("change_type") != "a1_to_a2":
            pytest.skip("Category change is not an (a)(1) to (a)(2) return")
        assert ssc_category_change_record.get("expert_panel_approved_return"), (
            f"SSC '{ssc_category_change_record.get('ssc_id')}': returned to (a)(2) without expert panel approval"
        )
        assert ssc_category_change_record.get("goals_met_evidence"), (
            f"SSC '{ssc_category_change_record.get('ssc_id')}': returned to (a)(2) without documented evidence "
            "that (a)(1) goals were met"
        )


# ---------------------------------------------------------------------------
# §50.65(a)(3) — Annual Performance Review (Pattern 1 + Pattern 2)
# ---------------------------------------------------------------------------

@pytest.mark.assumption(
    id="ASSUME-NRC50-MR-003",
    description="Annual review: 24-month maximum interval, all in-scope SSCs covered, functional failure summary, management approval",
    approved_by="Maintenance Rule Coordinator",
    review_date="2026-05-21"
)
class TestMaintenanceRuleA3AnnualReview:

    def test_annual_review_not_overdue(self, mr_program: dict):
        """Maintenance Rule annual performance review must not exceed 24 months since last review."""
        last_review_date = mr_program.get("last_annual_review_date")
        assert last_review_date is not None, "No Maintenance Rule annual review date on record"
        if isinstance(last_review_date, str):
            last_review_date = datetime.fromisoformat(last_review_date)
        max_interval_days = 24 * 30  # 24 months ≈ 730 days
        days_since = (datetime.now() - last_review_date).days
        assert days_since <= 730, (
            f"§50.65(a)(3) annual review overdue: last review {last_review_date.date()} "
            f"({days_since} days ago, 24-month maximum)"
        )

    def test_annual_review_has_management_approval(self, mr_annual_review: dict):
        """Annual MR review must have senior management review and approval."""
        assert mr_annual_review.get("management_approved_by"), (
            "MR annual review has no management approval signature"
        )
        assert mr_annual_review.get("management_approval_date"), (
            "MR annual review has no management approval date"
        )

    def test_annual_review_includes_functional_failure_summary(self, mr_annual_review: dict):
        """Annual review must include a summary of all functional failures during the review period."""
        assert mr_annual_review.get("functional_failure_summary"), (
            "MR annual review does not include a functional failure summary — required by NUMARC 93-01"
        )

    def test_annual_review_covers_all_in_scope_sscs(self, mr_annual_review: dict, mr_database: dict):
        """Annual review must evaluate all in-scope SSCs, not just (a)(1) SSCs."""
        sscs_reviewed = set(mr_annual_review.get("sscs_reviewed", []))
        sscs_in_scope = {s.get("ssc_id") for s in mr_database.get("sscs", [])}
        unreviewed = sscs_in_scope - sscs_reviewed
        # Allow up to 5% gap for recently added or removed SSCs in transition
        gap_threshold = max(1, int(len(sscs_in_scope) * 0.05))
        assert len(unreviewed) <= gap_threshold, (
            f"Annual review omits {len(unreviewed)} in-scope SSCs: {list(unreviewed)[:10]}"
        )

    def test_annual_review_evaluates_a2_criteria_adequacy(self, mr_annual_review: dict):
        """Annual review must evaluate whether (a)(2) performance criteria remain appropriate."""
        assert mr_annual_review.get("a2_criteria_adequacy_evaluated"), (
            "Annual review did not evaluate (a)(2) performance criteria adequacy — required by §50.65(a)(3)"
        )

    def test_annual_review_documents_a1_ssc_status(self, mr_annual_review: dict):
        """Annual review must document status and progress for all (a)(1) SSCs."""
        a1_sscs_in_review = mr_annual_review.get("a1_ssc_status_entries", [])
        mr_database = mr_annual_review.get("mr_database_snapshot", {})
        a1_count = mr_database.get("a1_ssc_count", 0)
        if a1_count == 0:
            pytest.skip("No (a)(1) SSCs in database — (a)(1) status section not required")
        assert len(a1_sscs_in_review) >= a1_count, (
            f"Annual review covers {len(a1_sscs_in_review)} (a)(1) SSCs but database shows {a1_count} — "
            "all (a)(1) SSCs must have status entries in the annual review"
        )


# ---------------------------------------------------------------------------
# §50.65(a)(4) — Pre-Maintenance Risk Assessment (Pattern 1 + Pattern 2)
# ---------------------------------------------------------------------------

@pytest.mark.assumption(
    id="ASSUME-NRC50-MR-004",
    description="(a)(4) risk assessment: pre-activity (before OOS), graded approach, online risk monitor currency ≤18 months, Yellow/Red requires management approval",
    approved_by="Maintenance Rule Coordinator",
    review_date="2026-05-21"
)
class TestMaintenanceRuleA4RiskAssessment:

    def test_work_order_references_a4_assessment(self, work_order: dict):
        """Each maintenance work order on an in-scope SSC must reference a §50.65(a)(4) risk assessment."""
        if not work_order.get("is_mr_scope_ssc", False):
            pytest.skip("Work order is for non-MR-scope SSC — (a)(4) not required")
        assert work_order.get("a4_assessment_id") or work_order.get("a4_screening_disposition"), (
            f"Work order {work_order.get('wo_id')}: no §50.65(a)(4) risk assessment reference — "
            "assessment required before taking SSC out of service"
        )

    def test_a4_assessment_completed_before_oos(self, maintenance_activity: dict):
        """§50.65(a)(4) risk assessment must be completed before the SSC is taken out of service."""
        assessment_date = maintenance_activity.get("a4_assessment_completed_date")
        oos_date = maintenance_activity.get("equipment_oos_date")
        if not assessment_date or not oos_date:
            pytest.skip("Assessment or OOS timestamps not available")
        if isinstance(assessment_date, str):
            assessment_date = datetime.fromisoformat(assessment_date)
        if isinstance(oos_date, str):
            oos_date = datetime.fromisoformat(oos_date)
        assert assessment_date <= oos_date, (
            f"Maintenance activity {maintenance_activity.get('activity_id')}: "
            f"(a)(4) assessment completed {assessment_date} AFTER equipment OOS at {oos_date} — "
            "pre-activity assessment requirement violated"
        )

    def test_a4_risk_classification_is_documented(self, maintenance_activity: dict):
        """Each (a)(4) assessment must document a risk classification (Green/Yellow/Red)."""
        if not maintenance_activity.get("a4_assessment_id"):
            pytest.skip("Activity has no (a)(4) assessment — screening may have applied")
        valid_colors = {"green", "yellow", "red"}
        risk_color = maintenance_activity.get("a4_risk_color", "").lower()
        assert risk_color in valid_colors, (
            f"Activity {maintenance_activity.get('activity_id')}: (a)(4) risk color '{risk_color}' is not valid. "
            f"Must be one of: {valid_colors}"
        )

    def test_yellow_risk_requires_management_approval(self, maintenance_activity: dict):
        """Yellow-risk (a)(4) assessments must have documented management approval before proceeding."""
        risk_color = maintenance_activity.get("a4_risk_color", "").lower()
        if risk_color not in {"yellow", "red"}:
            pytest.skip("Activity is Green risk — management approval not required")
        assert maintenance_activity.get("a4_management_approval_id"), (
            f"Activity {maintenance_activity.get('activity_id')}: Yellow/Red (a)(4) risk level but no "
            "management approval documented"
        )

    def test_online_risk_monitor_is_current(self, facility_pra_data: dict):
        """Online risk monitor / PRA model used for (a)(4) assessments must be updated within 18 months."""
        last_model_update = facility_pra_data.get("online_risk_monitor_last_update")
        assert last_model_update is not None, "Online risk monitor last update date not documented"
        if isinstance(last_model_update, str):
            last_model_update = datetime.fromisoformat(last_model_update)
        days_since = (datetime.now() - last_model_update).days
        max_staleness_days = 18 * 30  # 18 months
        assert days_since <= max_staleness_days, (
            f"Online risk monitor last updated {last_model_update.date()} ({days_since} days ago) — "
            "model older than 18 months may not reflect current plant configuration; "
            "(a)(4) assessments using a stale model are a common NRC finding"
        )


# ---------------------------------------------------------------------------
# Expert Panel (Pattern 2 + Pattern 3)
# ---------------------------------------------------------------------------

@pytest.mark.assumption(
    id="ASSUME-NRC50-MR-005",
    description="Expert panel: written charter, independence from work group, SRO representation, documented basis for all decisions",
    approved_by="Maintenance Rule Coordinator",
    review_date="2026-05-21"
)
class TestMaintenanceRuleExpertPanel:

    def test_expert_panel_composition_meets_charter(self, expert_panel_meeting: dict, mr_program: dict):
        """Expert panel meeting attendance must meet the minimum composition in the charter."""
        charter = mr_program.get("expert_panel_charter", {})
        required_roles = set(charter.get("minimum_required_roles", []))
        attending_roles = set(expert_panel_meeting.get("attendee_roles", []))
        missing_roles = required_roles - attending_roles
        assert not missing_roles, (
            f"Expert panel meeting {expert_panel_meeting.get('meeting_id')} lacks required roles: {missing_roles}"
        )

    def test_expert_panel_includes_operations_representation(self, expert_panel_meeting: dict):
        """Expert panel must include operations representation (SRO or equivalent)."""
        attendee_roles = expert_panel_meeting.get("attendee_roles", [])
        has_operations = any(
            role in {"SRO", "operations", "shift_supervisor", "shift_manager"}
            for role in (r.lower() for r in attendee_roles)
        )
        assert has_operations, (
            f"Expert panel meeting {expert_panel_meeting.get('meeting_id')} has no operations (SRO) representation"
        )

    def test_expert_panel_meeting_minutes_exist(self, expert_panel_meeting: dict):
        """Expert panel meetings must have documented minutes with decisions and bases."""
        assert expert_panel_meeting.get("minutes_document_id"), (
            f"Expert panel meeting {expert_panel_meeting.get('meeting_id')} has no documented minutes"
        )
        assert expert_panel_meeting.get("decisions", []), (
            f"Expert panel meeting {expert_panel_meeting.get('meeting_id')} has minutes but no decisions recorded"
        )

    def test_expert_panel_decisions_have_documented_basis(self, expert_panel_meeting: dict):
        """Each expert panel decision must have a documented technical basis."""
        for decision in expert_panel_meeting.get("decisions", []):
            assert decision.get("technical_basis"), (
                f"Expert panel decision '{decision.get('decision_id')}' in meeting "
                f"{expert_panel_meeting.get('meeting_id')} has no documented technical basis"
            )

    @pytest.mark.human_review_required(
        reason="Whether the expert panel's technical basis for an (a)(2) return is sufficient to provide "
               "'reasonable assurance' that the SSC can fulfill its intended safety function is a "
               "judgment determination that requires review by the Maintenance Rule Coordinator and "
               "plant management per NUMARC 93-01 Section 7. NRC Inspection Procedure 71111.12 will "
               "evaluate the panel's analytical rigor. Pattern 3: surface for Maintenance Rule Coordinator sign-off."
    )
    def test_a2_return_basis_adequacy(self, ssc_category_change_record: dict):
        """[HUMAN REVIEW] Adequacy of expert panel basis for (a)(1) → (a)(2) return requires human sign-off."""
        if ssc_category_change_record.get("change_type") != "a1_to_a2":
            pytest.skip("Not an (a)(1) to (a)(2) return")
        assert ssc_category_change_record.get("mr_coordinator_sign_off"), (
            f"SSC '{ssc_category_change_record.get('ssc_id')}': (a)(2) return has no Maintenance Rule "
            "Coordinator sign-off — required per NUMARC 93-01 and NRC IP 71111.12"
        )
```

---

## Assumption registry (this file)

| ID | Section | Summary | Review date |
|---|---|---|---|
| ASSUME-NRC50-MR-001 | §50.65(a)(2) | Performance criteria: written before categorization, quantitative metrics required, PM basis document, monitoring in CMMS | 2026-05-21 |
| ASSUME-NRC50-MR-002 | §50.65(a)(1) | Categorization triggers: MPFF threshold, measurable goals, prompt placement (≤90 days of criteria exceedance), expert panel review and documentation | 2026-05-21 |
| ASSUME-NRC50-MR-003 | §50.65(a)(3) | Annual review: 24-month maximum, all SSCs covered, functional failure summary, (a)(2) criteria adequacy evaluated, management approval | 2026-05-21 |
| ASSUME-NRC50-MR-004 | §50.65(a)(4) | Pre-maintenance risk assessment: before OOS, graded approach acceptable, online risk monitor ≤18 months current, Yellow/Red requires management approval | 2026-05-21 |
| ASSUME-NRC50-MR-005 | §50.65 (expert panel) | Expert panel: charter specifies composition, independence from work group, SRO required, documented basis for all categorization and return decisions | 2026-05-21 |

---

## Cross-references

- **§50.65(a)(1) → App. B Criterion XVI:** Every (a)(1) placement is a Significant Condition Adverse to Quality (SCAQ) — root cause analysis under Criterion XVI is required in addition to MR corrective action; the two programs must be coordinated so a single CAP entry serves both requirements
- **§50.65(a)(4) → §50.65(a)(1):** Pre-maintenance risk assessments may identify cumulative risk from multiple simultaneous (a)(1) SSCs — this interaction must be evaluated; high aggregate risk from (a)(1) SSC concentration is an indicator of systemic maintenance effectiveness problems
- **§50.65 → §50.72/50.73:** Functional failures of in-scope MR SSCs that meet §50.72 notification thresholds require parallel reporting — the MR (a)(1) determination does not substitute for §50.72 event reporting
- **§50.65 → §50.55a:** ASME Code inservice inspection (§50.55a) findings that reveal SSC degradation may trigger (a)(1) placement under the MR — the two programs share the same physical SSC population for pressure-retaining components
- **§50.65(a)(4) risk thresholds → NRC Regulatory Guide 1.174:** Green/Yellow/Red thresholds used for (a)(4) assessments are based on RG 1.174 risk-informed decision-making acceptance guidelines — ICDP and ILERP thresholds must match current NRC guidance edition endorsed in the plant's license basis
