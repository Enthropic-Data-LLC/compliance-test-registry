# SOC 2 TSC 2017 — A1: Availability Criteria

**Registry path:** `/regulation-registry/SOC2/A1/`
**Version:** AICPA TSC 2017 (2022 points of focus updates)
**Last parsed:** 2026-05-20
**Overall confidence:** MEDIUM — backup frequency and restore test cadence have DETERMINISTIC thresholds with assumptions; capacity management thresholds are PARAMETERIZED (org-defined)
**3 criteria: A1.1–A1.3**
**Optional trust service category — only in scope when service organization commits to availability SLAs**

---

## Scope summary

The Availability criteria apply when the service organization has made availability commitments to customers (SLAs, uptime guarantees). They address capacity planning, environmental protection, and recovery testing. Availability criteria have strong alignment with ISO 27001 A.5.29–5.30 (business continuity) and NIST 800-53 CP (Contingency Planning).

The most testable element is recovery: backup existence is DETERMINISTIC, and restore test cadence is DETERMINISTIC with an assumption. Capacity management thresholds (A1.1) are organization-defined and therefore PARAMETERIZED. Environmental threats (A1.2) are DETERMINISTIC for control existence but PARAMETERIZED for adequacy.

---

## A1.1 — Capacity Management (PARAMETERIZED)

### Source excerpt

> The entity maintains, monitors, and evaluates current processing capacity and use of system components (infrastructure, data, and software) to manage capacity demand and to enable the implementation of additional capacity to help meet its objectives.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Capacity monitoring deployed; capacity thresholds defined; alerts generated when thresholds exceeded; capacity planning process documented | DETERMINISTIC (monitoring existence) / PARAMETERIZED (thresholds) |
| Evidence | `capacity_monitoring.deployed == true`; `capacity_thresholds.documented == true`; `capacity_alerts.configured == true`; capacity planning records | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-SOC2-A1-001):** Capacity management is adequate when: (1) resource utilization monitored for all system components in SOC 2 boundary: CPU, memory, disk, network; (2) alert thresholds configured: warning at 80% sustained, critical at 90% sustained (or lower if based on performance testing); (3) capacity planning review performed at least annually or when significant service growth anticipated; (4) capacity incidents (sustained threshold breach) trigger review and remediation within defined SLA; (5) metrics reviewed against availability commitments — capacity must support committed SLA even under peak load.

**Overall: PARAMETERIZED → Pattern 2; monitoring existence → Pattern 1**

---

## A1.2 — Environmental Threats, Backup, and Recovery (MEDIUM)

### Source excerpt

> The entity authorizes, designs, develops or acquires, implements, operates, approves, maintains, and monitors environmental protections, software, data back-up processes, and recovery infrastructure to meet its objectives.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Environmental protections in place (UPS, fire suppression, HVAC); backup process documented and operating; backup data protected; recovery infrastructure maintained | DETERMINISTIC (backup existence) / PARAMETERIZED (adequacy) |
| Evidence | `backup_policy.documented == true`; `backup_records.last_run_date` ≤ 24 hours; `backup_records.offsite_or_cloud == true`; `environmental_controls.ups_deployed == true` | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-SOC2-A1-002):** Backup and environmental protection are adequate when: (1) backup frequency: daily incremental minimum; weekly full minimum; (2) backup storage: offsite or geographically separate cloud region; (3) backup encryption: backups containing sensitive data encrypted at rest; (4) backup retention: minimum 30 days standard; 90 days for customer data depending on contractual commitments; (5) environmental controls: UPS with ≥ 30-minute runtime; temperature/humidity monitoring; fire suppression in data center; (6) backup integrity verified (automated checksum or periodic manual test).

**Cross-reference:** Aligns with ISO 27001 ASSUME-ISO-A8-006 (backup adequacy) and ISO 27001 A.7.11 (supporting utilities).

**Overall: DETERMINISTIC for backup existence → Pattern 1; PARAMETERIZED for adequacy → Pattern 2**

---

## A1.3 — Recovery Testing (MEDIUM)

### Source excerpt

> The entity tests recovery plan procedures supporting system availability to meet its objectives.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | At planned intervals | DETERMINISTIC (existence of tests) |
| Obligation | Recovery plan tested; RTO and RPO objectives validated against actual recovery times; test results documented; gaps addressed | DETERMINISTIC (cadence) / PARAMETERIZED (adequacy) |
| Evidence | `recovery_test_records.most_recent_date`; `recovery_test_records.rto_achieved == true`; `recovery_test_records.rpo_achieved == true`; gap remediation records | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-SOC2-A1-003):** Recovery testing is adequate when: (1) full system restore test conducted at least annually; (2) data restore tested at least quarterly to verify backup integrity and completeness; (3) test results document: date, scope, actual RTO achieved, actual RPO achieved, data completeness; (4) if actual RTO/RPO exceeds committed objectives: remediation plan in place and tracked; (5) test environment is representative of production (not tested only against development data); (6) customers notified of material changes to recovery capabilities.

**Overall: DETERMINISTIC for test existence and annual cadence → Pattern 1; PARAMETERIZED for RTO/RPO adequacy → Pattern 2**

---

## YAML specifications

### `a1_availability.yaml`

```yaml
regulation_id: SOC2-TSC2017-A1
section: "SOC 2 TSC 2017 — A1: Availability"
r_or_a: Additional (in scope when availability commitments made)
source_text: >
  The entity maintains, monitors, and evaluates current processing capacity and
  use of system components; implements environmental protections and backup processes;
  and tests recovery plan procedures to meet its availability objectives.

extracted_elements:
  subject: "All systems in SOC 2 boundary with availability commitments"
  condition: "Availability category selected; ongoing with quarterly backup test and annual restore test"
  obligation: "Capacity monitored; backups current and offsite; restore test annual; RTO/RPO met"
  evidence: "capacity_monitoring_records, backup_records, recovery_test_records"

ambiguity_classification:
  subject: PARAMETERIZED
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-SOC2-A1-002
    assumption_text: >
      Backup: daily incremental; weekly full; offsite/cloud; encrypted; ≥30-day retention;
      integrity verified. Environmental: UPS ≥30 min; temp/humidity monitoring; fire suppression.
    assumed_by: "ISMS Manager"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
  - assumption_id: ASSUME-SOC2-A1-003
    assumption_text: >
      Recovery testing: annual full restore; quarterly data restore; RTO/RPO documented;
      gaps have remediation plan; production-representative test environment.
    assumed_by: "ISMS Manager"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
test_confidence: MEDIUM
generated_test: "tests/soc2/test_a1_availability.py"
```

---

## Generated tests

### `tests/soc2/test_a1_availability.py`

```python
"""
SOC 2 TSC 2017 — A1: Availability
Confidence: MEDIUM — backup and restore test cadences are DETERMINISTIC with assumptions;
capacity management thresholds are org-defined
"""
import pytest
from datetime import date

BACKUP_MAX_AGE_HOURS = 24
RESTORE_TEST_MAX_DAYS = 365
DATA_RESTORE_TEST_MAX_DAYS = 90
CAPACITY_WARNING_THRESHOLD_PCT = 80


@pytest.mark.assumption(
    id="ASSUME-SOC2-A1-002",
    description=(
        "Backup: daily incremental min; weekly full; offsite/cloud; encrypted; "
        "≥30-day retention; integrity verified."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_backups_current_and_offsite(backup_records):
    """A1.2 — Backups must run daily and be stored offsite or in separate cloud region."""
    today = date.today()
    soc2_backups = [r for r in backup_records if r.get("in_soc2_boundary")]
    assert soc2_backups, (
        "NONCONFORMITY (A1.2): No backup records found for SOC 2 boundary systems"
    )
    violations = []
    for r in soc2_backups:
        last_run = r.get("last_successful_backup_date")
        if last_run is None:
            violations.append(f"{r['system_id']}: no successful backup on record")
        elif (today - last_run).days > 1:
            violations.append(
                f"{r['system_id']}: last backup {(today - last_run).days} day(s) ago"
            )
        if not r.get("offsite_copy") and not r.get("separate_cloud_region"):
            violations.append(
                f"{r['system_id']}: backup not stored offsite or in separate region"
            )
    assert not violations, (
        f"NONCONFORMITY (A1.2): {len(violations)} backup issue(s):\n"
        + "\n".join(violations)
    )


@pytest.mark.assumption(
    id="ASSUME-SOC2-A1-003",
    description=(
        "Recovery testing: annual full restore; quarterly data restore test; "
        "RTO/RPO documented and met; production-representative test environment."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_annual_restore_test_performed(recovery_test_records):
    """A1.3 — Full system restore tested at least annually."""
    today = date.today()
    full_restore_tests = [
        r for r in recovery_test_records
        if r.get("test_type") == "full_restore"
        and r.get("in_soc2_boundary")
    ]
    if not full_restore_tests:
        assert False, (
            "NONCONFORMITY (A1.3): No full restore test records found — "
            "annual restore testing is required"
        )
    latest = max(full_restore_tests, key=lambda r: r["test_date"])
    days_since = (today - latest["test_date"]).days
    assert days_since <= RESTORE_TEST_MAX_DAYS, (
        f"NONCONFORMITY (A1.3): Full restore last tested {days_since} days ago "
        f"(max {RESTORE_TEST_MAX_DAYS})"
    )


def test_quarterly_data_restore_test_performed(recovery_test_records):
    """A1.3 — Data restore tested at least quarterly to verify backup integrity."""
    today = date.today()
    data_restore_tests = [
        r for r in recovery_test_records
        if r.get("test_type") in ("data_restore", "backup_integrity")
        and r.get("in_soc2_boundary")
    ]
    if not data_restore_tests:
        assert False, (
            "NONCONFORMITY (A1.3): No data restore/backup integrity test records found — "
            "quarterly testing is required"
        )
    latest = max(data_restore_tests, key=lambda r: r["test_date"])
    days_since = (today - latest["test_date"]).days
    assert days_since <= DATA_RESTORE_TEST_MAX_DAYS, (
        f"NONCONFORMITY (A1.3): Data restore last tested {days_since} days ago "
        f"(max {DATA_RESTORE_TEST_MAX_DAYS})"
    )


def test_restore_test_met_rto_rpo_objectives(recovery_test_records):
    """A1.3 — Most recent restore test must have met RTO and RPO objectives."""
    soc2_full = [
        r for r in recovery_test_records
        if r.get("test_type") == "full_restore"
        and r.get("in_soc2_boundary")
        and r.get("rto_target_minutes")
    ]
    if not soc2_full:
        pytest.skip("No full restore records with RTO targets available")
    latest = max(soc2_full, key=lambda r: r["test_date"])
    if not latest.get("rto_achieved"):
        assert False, (
            f"NONCONFORMITY (A1.3): Most recent restore test ({latest['test_date']}) "
            f"did not achieve RTO target of {latest.get('rto_target_minutes')} minutes"
        )
    if not latest.get("rpo_achieved"):
        assert False, (
            f"NONCONFORMITY (A1.3): Most recent restore test ({latest['test_date']}) "
            f"did not achieve RPO target"
        )


def test_capacity_monitoring_deployed(capacity_monitoring_records):
    """A1.1 — Capacity monitoring must be deployed for all SOC 2 boundary systems."""
    soc2_systems = [r for r in capacity_monitoring_records if r.get("in_soc2_boundary")]
    assert soc2_systems, (
        "NONCONFORMITY (A1.1): No capacity monitoring records for SOC 2 boundary systems"
    )
    no_monitoring = [r for r in soc2_systems if not r.get("monitoring_deployed")]
    assert not no_monitoring, (
        f"NONCONFORMITY (A1.1): {len(no_monitoring)} system(s) without capacity "
        f"monitoring: {[r['system_id'] for r in no_monitoring]}"
    )
```

---

## Notes for the registry

- **A1 opt-in scope management:** Availability criteria only apply when selected by the service organization. Before any A1 test executes, the system boundary fixture must confirm that Availability is an in-scope trust service category. Tests that fire against out-of-scope categories should run in informational mode only.
- **RTO/RPO and availability SLA consistency:** A common audit finding is that the documented RTO/RPO objectives are not aligned with the availability SLA promised to customers. If the SLA promises 99.9% uptime, the RTO must be short enough to achieve that in the worst-case scenario. The test `test_restore_test_met_rto_rpo_objectives` verifies this alignment indirectly (if RTO is too long to meet the SLA, the test will expose the gap).
- **A1.2 and A.7.11 alignment:** The SOC 2 A1.2 environmental protection requirement overlaps entirely with ISO 27001 A.7.11 (Supporting Utilities). Organizations can use the same UPS test records and environmental monitoring data for both. The fixture `infrastructure_records` used in ISO 27001 tests and `backup_records` used here should share the same underlying data source.
- **A1.3 quarterly backup test frequency:** The quarterly data restore test (ASSUME-SOC2-A1-003) is more frequent than the annual full restore. Quarterly backup tests verify integrity throughout the year — a backup that hasn't been tested since the last full restore could be silently corrupted for 11 months. This frequency aligns with PCI DSS Req 3 (data integrity) expectations.
