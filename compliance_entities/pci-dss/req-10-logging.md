# Requirement 10 — Log and Monitor All Access to System Components and Cardholder Data

**Registry path:** `/regulation-registry/PCI-DSS/Req-10/`
**Version:** PCI DSS v4.0 (mandatory since March 31, 2025)
**Last parsed:** 2026-05-20
**Overall confidence:** HIGH — retention thresholds and required log fields are DETERMINISTIC; review frequency is DETERMINISTIC with a PARAMETERIZED exception for non-critical systems
**R = Required**

---

## Scope summary

Req 10 is the audit logging and monitoring requirement. It has the most cross-framework reuse value of any PCI DSS requirement — the 12-month/3-month retention thresholds are the tightest stated retention requirements in the registry and design to them satisfies HIPAA, SOC 2, and NIST simultaneously.

v4.0 added Req 10.7 (critical security control failure detection) and strengthened daily log review requirements with 10.4.1.1 (automated mechanisms required for daily review).

---

## 10.2 — Audit Log Content (R — DETERMINISTIC)

### Source excerpt

> *10.2.1 — Audit logs are enabled and active for all system components, and include all individual user access to cardholder data; all actions taken by any individual with root or administrative privileges; access to all audit trails; invalid logical access attempts; use of and changes to identification and authentication mechanisms; initialization, stopping, or pausing of the audit logs; creation and deletion of system-level objects.*

> *10.3.1 — Read access to audit log files is limited to those with a job-related need. Audit log files, including those for external-facing technologies, are promptly backed up to a secure, central internal log server or other media that is difficult to alter.*

> *10.3.1.1 — Audit log files are protected to prevent modifications by individuals.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All CDE system components | DETERMINISTIC |
| Condition | Log-generating system is in scope | DETERMINISTIC |
| Obligation | Logs enabled and active; capture all 7 event categories in 10.2.1; tamper-evident storage | DETERMINISTIC |
| Evidence | `system_log_config.logging_enabled == true`; log content review against 7-category checklist; `log_storage.tamper_evident == true` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 10.3 — Required Log Entry Fields (R — DETERMINISTIC)

### Source excerpt

> *10.3.2 — Audit log entries contain at least the following: user identification; type of event; date and time; success or failure indication; origination of event; identity or name of affected data, system component, resource, or service.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | Every audit log entry in CDE | DETERMINISTIC |
| Condition | Log entry is generated | DETERMINISTIC |
| Obligation | Entry contains all 6 required fields | DETERMINISTIC |
| Evidence | Log schema: `user_id`, `event_type`, `timestamp`, `success_failure`, `source_ip_or_origin`, `affected_resource` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 10.4 — Log Review (R — DETERMINISTIC for critical systems; PARAMETERIZED for others)

### Source excerpt

> *10.4.1 — The following audit logs are reviewed at least once daily: All security events. Logs of all system components that store, process, or transmit CHD and/or SAD. Logs of all critical system components. Logs of all servers and system components that perform security functions.*
> *10.4.1.1 — Automated mechanisms are used to perform audit log reviews.*
> *10.4.2 — Logs of all other system components are reviewed periodically.*

### Element extraction — daily review (critical systems)

| Element | Value | Classification |
|---|---|---|
| Subject | Security events, CHD/SAD system logs, critical system logs, security function logs | DETERMINISTIC |
| Condition | System is in scope | DETERMINISTIC |
| Obligation | Logs reviewed daily; review performed using automated mechanism | DETERMINISTIC |
| Evidence | `log_review_config.frequency == "daily"` for all critical systems; `automated_review_tool` documented | DETERMINISTIC |

### Element extraction — periodic review (non-critical systems)

| Element | Value | Classification |
|---|---|---|
| Subject | All other in-scope system components | DETERMINISTIC |
| Condition | System is in scope but not classified as critical | PARAMETERIZED |
| Obligation | Reviewed "periodically" — interval not specified | PARAMETERIZED |
| Evidence | `log_review_config.review_interval`; documented review schedule | PARAMETERIZED |

**Assumption (ASSUME-10-001):** "Periodically" for non-critical system log review is satisfied by at least weekly review. Monthly review may satisfy QSA expectations for very low-risk, non-CHD systems if documented with risk justification.

**Overall: DETERMINISTIC for daily critical review → Pattern 1; PARAMETERIZED for non-critical cadence → Pattern 2**

---

## 10.5 — Log Retention (R — DETERMINISTIC)

### Source excerpt

> *10.5.1 — Retain audit log history for at least 12 months, with at least the most recent three months available for immediate analysis.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All audit logs for CDE systems | DETERMINISTIC |
| Condition | Log has been generated | DETERMINISTIC |
| Obligation | Total retention ≥ 12 months; immediate access ≥ 3 months | DETERMINISTIC |
| Evidence | `log_retention_config.total_months >= 12`; `log_retention_config.immediate_access_months >= 3` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 10.6 — Time Synchronization (R — DETERMINISTIC)

### Source excerpt

> *10.6.1 — System clocks and time are synchronized using time-synchronization technology. Time data is protected. Time synchronization settings are consistent across all system components.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All CDE system components | DETERMINISTIC |
| Condition | System is in scope | DETERMINISTIC |
| Obligation | NTP (or equivalent) configured; time data integrity protected; consistent time source | DETERMINISTIC |
| Evidence | `ntp_config.enabled == true`; `ntp_config.server` consistent across all CDE systems; `ntp_access_controls` documented | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 10.7 — Critical Security Control Failure Detection (R — PARAMETERIZED)

### Source excerpt

> *10.7.2 — Failures of critical security controls are detected, alerted, and addressed promptly. The critical security controls include: Network security controls; IDS/IPS; Change detection mechanisms; Anti-malware solutions; Physical access controls; Logical access controls; Audit logging mechanisms; Segmentation controls.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All critical security controls listed in 10.7.2 | DETERMINISTIC |
| Condition | A critical control experiences a failure | PARAMETERIZED (failure definition) |
| Obligation | Failure detected; alert generated; addressed "promptly" | PARAMETERIZED |
| Evidence | `security_control_monitoring.control_type`, `failure_alert_configured == true`, `mean_time_to_alert` documented | PARAMETERIZED |

**Assumption (ASSUME-10-002):** "Promptly" for critical security control failure response is satisfied when: alert is generated within 15 minutes of failure detection; incident ticket opened within 1 hour; remediation or compensating control activated within 4 hours. Automated failure detection via SIEM or equivalent is required under 10.4.1.1 (which also covers security event monitoring).

**Overall: PARAMETERIZED → Pattern 2**

---

## YAML specifications

### `req10_retention.yaml`

```yaml
regulation_id: PCI-DSS-v4.0-10.5.1
section: "PCI DSS v4.0 — Audit Log Retention"
r_or_a: Required
source_text: >
  Retain audit log history for at least 12 months, with at least the most
  recent three months available for immediate analysis.

extracted_elements:
  subject: "All audit logs for CDE systems"
  condition: "Log has been generated"
  obligation: "Total retention ≥ 12 months; ≥ 3 months immediate access"
  evidence: "log_retention_config: total_months >= 12, immediate_access_months >= 3"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log: []
test_confidence: HIGH
generated_test: "tests/req10/test_10_5_retention.py"
```

---

## Generated tests

### `tests/req10/test_10_2_log_coverage.py`

```python
"""
PCI DSS v4.0 Req 10.2 — Audit Log Coverage and Content
Confidence: HIGH | Human Review: NOT REQUIRED
"""

REQUIRED_LOG_FIELDS = {
    "user_id",
    "event_type",
    "timestamp",
    "success_failure",
    "source_origin",
    "affected_resource",
}

REQUIRED_EVENT_CATEGORIES = {
    "user_access_to_chd",
    "admin_and_root_actions",
    "access_to_audit_trails",
    "invalid_access_attempts",
    "auth_mechanism_changes",
    "audit_log_start_stop_pause",
    "system_object_creation_deletion",
}


def test_logging_enabled_on_all_cde_systems(cde_system_configs):
    violations = [
        s for s in cde_system_configs
        if s.get("in_cde") and not s.get("logging_enabled")
    ]
    assert not violations, (
        f"VIOLATION (10.2.1): {len(violations)} CDE system(s) with logging disabled: "
        f"{[s['system_id'] for s in violations]}"
    )


def test_log_captures_all_required_event_categories(log_configuration_reviews):
    violations = []
    for review in log_configuration_reviews:
        captured = set(review.get("event_categories_captured", []))
        missing = REQUIRED_EVENT_CATEGORIES - captured
        if missing:
            violations.append(
                f"System {review['system_id']}: missing event categories {missing}"
            )
    assert not violations, (
        f"VIOLATION (10.2.1): {len(violations)} system(s) missing required event "
        f"categories:\n" + "\n".join(violations)
    )


def test_log_entries_contain_required_fields(log_schema_reviews):
    violations = []
    for review in log_schema_reviews:
        present = set(review.get("fields_present", []))
        missing = REQUIRED_LOG_FIELDS - present
        if missing:
            violations.append(
                f"System {review['system_id']}: missing log fields {missing}"
            )
    assert not violations, (
        f"VIOLATION (10.3.2): {len(violations)} system(s) with incomplete log entry "
        f"schema:\n" + "\n".join(violations)
    )


def test_audit_logs_tamper_evident(log_storage_configs):
    violations = [
        s for s in log_storage_configs
        if not s.get("tamper_evident") and not s.get("write_once")
    ]
    assert not violations, (
        f"VIOLATION (10.3.3): {len(violations)} log storage configuration(s) without "
        f"tamper-evident or write-once protection: "
        f"{[s['system_id'] for s in violations]}"
    )
```

### `tests/req10/test_10_4_log_review.py`

```python
"""
PCI DSS v4.0 Req 10.4 — Log Review Cadence
Confidence: HIGH for daily review; MEDIUM for non-critical cadence
"""
import pytest
from datetime import date

DAILY_REVIEW_MAX_GAP_DAYS = 1
NONCRITICAL_REVIEW_MAX_GAP_DAYS = 7  # ASSUME-10-001: weekly minimum


def test_critical_systems_reviewed_daily(log_review_records, cde_system_configs):
    today = date.today()
    critical_system_ids = {
        s["system_id"] for s in cde_system_configs
        if s.get("critical_system") or s.get("stores_chd") or s.get("security_function")
    }
    violations = []
    review_map = {r["system_id"]: r for r in log_review_records}
    for sys_id in critical_system_ids:
        review = review_map.get(sys_id)
        if not review:
            violations.append(f"{sys_id}: no log review record")
            continue
        last_review = review.get("last_review_date")
        if not last_review:
            violations.append(f"{sys_id}: no review date recorded")
            continue
        gap = (today - last_review).days
        if gap > DAILY_REVIEW_MAX_GAP_DAYS:
            violations.append(f"{sys_id}: last reviewed {gap} days ago (max 1)")
    assert not violations, (
        f"VIOLATION (10.4.1): {len(violations)} critical system log(s) not reviewed "
        f"within 24 hours:\n" + "\n".join(violations)
    )


def test_critical_systems_use_automated_review(log_review_records, cde_system_configs):
    critical_ids = {
        s["system_id"] for s in cde_system_configs
        if s.get("critical_system") or s.get("stores_chd")
    }
    review_map = {r["system_id"]: r for r in log_review_records}
    violations = [
        sid for sid in critical_ids
        if not review_map.get(sid, {}).get("automated_review")
    ]
    assert not violations, (
        f"VIOLATION (10.4.1.1): {len(violations)} critical system(s) without automated "
        f"log review mechanism: {violations}"
    )


@pytest.mark.assumption(
    id="ASSUME-10-001",
    description="Non-critical system log review: weekly minimum satisfies 'periodically'",
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_noncritical_systems_reviewed_periodically(log_review_records, cde_system_configs):
    today = date.today()
    noncritical_ids = {
        s["system_id"] for s in cde_system_configs
        if s.get("in_cde") and not s.get("critical_system") and not s.get("stores_chd")
    }
    review_map = {r["system_id"]: r for r in log_review_records}
    violations = []
    for sid in noncritical_ids:
        review = review_map.get(sid)
        if not review or not review.get("last_review_date"):
            violations.append(f"{sid}: no review record")
            continue
        gap = (today - review["last_review_date"]).days
        if gap > NONCRITICAL_REVIEW_MAX_GAP_DAYS:
            violations.append(f"{sid}: last reviewed {gap} days ago (max {NONCRITICAL_REVIEW_MAX_GAP_DAYS})")
    assert not violations, (
        f"VIOLATION (10.4.2): {len(violations)} non-critical system log(s) overdue "
        f"for review:\n" + "\n".join(violations)
    )
```

### `tests/req10/test_10_5_retention.py`

```python
"""
PCI DSS v4.0 Req 10.5 — Log Retention
Confidence: HIGH | Human Review: NOT REQUIRED
"""

LOG_TOTAL_RETENTION_MONTHS = 12
LOG_IMMEDIATE_ACCESS_MONTHS = 3


def test_log_total_retention_at_least_12_months(log_retention_configs):
    violations = [
        c for c in log_retention_configs
        if c.get("total_retention_months", 0) < LOG_TOTAL_RETENTION_MONTHS
    ]
    assert not violations, (
        f"VIOLATION (10.5.1): {len(violations)} log storage configuration(s) with "
        f"retention < 12 months: "
        f"{[(c['system_id'], c.get('total_retention_months')) for c in violations]}"
    )


def test_log_immediate_access_at_least_3_months(log_retention_configs):
    violations = [
        c for c in log_retention_configs
        if c.get("immediate_access_months", 0) < LOG_IMMEDIATE_ACCESS_MONTHS
    ]
    assert not violations, (
        f"VIOLATION (10.5.1): {len(violations)} system(s) with immediate-access log "
        f"period < 3 months: "
        f"{[(c['system_id'], c.get('immediate_access_months')) for c in violations]}"
    )


def test_ntp_configured_on_all_cde_systems(cde_system_configs):
    violations = [
        s for s in cde_system_configs
        if s.get("in_cde") and not s.get("ntp_configured")
    ]
    assert not violations, (
        f"VIOLATION (10.6.1): {len(violations)} CDE system(s) without NTP configured: "
        f"{[s['system_id'] for s in violations]}"
    )
```

---

## Notes for the registry

- **Cross-framework reuse:** PCI DSS 12-month/3-month retention is stricter than HIPAA (no stated retention for audit logs in Security Rule — only 6-year documentation retention applies via §164.316). If a system is in scope for both PCI and HIPAA, design to PCI's 12-month requirement to satisfy both.
- **Automated review requirement (10.4.1.1):** v4.0 added this as a formal requirement for daily-reviewed systems. Manual log review is insufficient for critical systems — a SIEM, log aggregation platform, or automated alerting system must be in place.
- **Log integrity:** Logs stored on the same system they monitor can be altered by a compromised system. 10.3.3 requires backup to a separate, difficult-to-alter location. A write-once SIEM or a separate syslog server with restricted write access satisfies this.
- **Time sync protection:** 10.6.1 requires that time data be "protected" — typically meaning only designated time servers can update system time, and time configuration changes are themselves logged and alerted.
- **10.7 is new in v4.0:** The critical security control failure detection requirement did not exist in v3.2.1. Organizations upgrading from v3.2.1 need to add monitoring for control failures, not just security events.
