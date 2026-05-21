# ISO/IEC 27001:2022 — Annex A Theme 4: Technological Controls (A.8.x)

**Registry path:** `/regulation-registry/ISO-27001/Annex-A8/`
**Version:** ISO/IEC 27001:2022
**Last parsed:** 2026-05-20
**Applies to:** Any organization seeking ISO/IEC 27001 certification for its Information Security Management System (ISMS); scope is organization-defined (can be a department, product line, or whole entity)
**Trigger:** Voluntary certification; customer or procurement requirement (especially in EU, UK, financial services); NIS2 Directive in EU references ISO 27001 as an acceptable framework; organizational risk management decision
**Jurisdiction:** Global — ISO/IEC international standard recognized worldwide; certifying bodies accredited per ISO/IEC 17021-1
**Not applicable to:** Mandatory compliance in isolation — ISO 27001 is a voluntary standard with no direct regulatory enforcement; certification applies only to the defined ISMS scope; does not replace sector-specific mandatory frameworks (HIPAA, PCI DSS, GLBA, etc.)
**Overall confidence:** MEDIUM overall — HIGH for A.8.5 (authentication), A.8.7 (malware), A.8.13 (backup), A.8.15 (logging), A.8.17 (NTP); PARAMETERIZED for most others
**34 controls: A.8.1–A.8.34**

---

## Scope summary

Theme 4 contains the 34 technological controls — the highest density of DETERMINISTIC thresholds in Annex A. It covers authentication, privileged access, malware protection, backups, logging, clock synchronization, cryptography, vulnerability management, configuration management, and the full secure development lifecycle. Many controls directly parallel PCI DSS Req 2, 5, 6, 8, and 10; cross-framework evidence reuse is high.

---

## A.8.2 — Privileged Access Rights (MEDIUM)

| Element | Value | Classification |
|---|---|---|
| Obligation | Privileged access rights allocated, reviewed, and revoked through formal authorization; use of generic admin accounts controlled | PARAMETERIZED |
| Evidence | `privileged_account_inventory`; `access_review_records.privileged_scope`; formal approval process | PARAMETERIZED |

**Assumption (ASSUME-ISO-A8-001):** Privileged access management is adequate when: (1) all privileged accounts inventoried with justification and approval; (2) privileged access reviewed at least every 6 months (quarterly for critical systems); (3) privileged access separated from normal user access (no dual-use accounts); (4) privileged session logging enabled; (5) generic admin accounts disabled or used only under break-glass procedures with individual accountability logging.

---

## A.8.5 — Secure Authentication (HIGH)

| Element | Value | Classification |
|---|---|---|
| Obligation | Authentication procedures and technologies based on information access restrictions; passwords meet minimum requirements; MFA for systems handling sensitive information | PARAMETERIZED (method) / DETERMINISTIC (thresholds where stated) |
| Evidence | Auth system configuration review; password policy review | PARAMETERIZED + DETERMINISTIC |

**Assumption (ASSUME-ISO-A8-002):** Authentication is adequate when: (1) passwords are at least 12 characters; (2) last 5 passwords prohibited; (3) automatic lockout after 10 failed attempts; (4) session timeout active for unattended sessions; (5) MFA implemented for all remote access and access to sensitive systems/data. ISO 27001 does not state numeric thresholds — these are derived from ISO 27002:2022 guidance and industry consensus.

---

## A.8.7 — Protection Against Malware (HIGH)

| Element | Value | Classification |
|---|---|---|
| Obligation | Protection against malware implemented and supported by appropriate user awareness; detection, prevention, and recovery controls deployed | DETERMINISTIC (deployment) / PARAMETERIZED (scope definition) |
| Evidence | `av_deployment_records`; `av_config.auto_update_enabled == true`; user awareness training covering malware | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-A8-003):** Malware protection is adequate when: AV/EDR deployed on all endpoints and servers capable of running it; definitions update automatically at least every 24 hours; scheduled or real-time scanning enabled; users trained to recognize and report malware indicators; removable media scanned before use.

---

## A.8.8 — Management of Technical Vulnerabilities (MEDIUM)

| Element | Value | Classification |
|---|---|---|
| Obligation | Technical vulnerabilities timely identified, evaluated, and addressed; vulnerability scanning performed; patches applied | PARAMETERIZED (no explicit SLA in standard) |
| Evidence | `vuln_scan_records.scan_date`; `patch_records.install_date`; vulnerability management policy | PARAMETERIZED |

**Assumption (ASSUME-ISO-A8-004):** Vulnerability management is adequate when: (1) vulnerability scanning performed at least quarterly and after significant changes; (2) critical vulnerabilities (CVSS ≥ 9.0) remediated within 30 days; high vulnerabilities (CVSS 7.0–8.9) within 30 days; medium within 90 days; (3) patch management process documented with defined SLAs; (4) exception process for unpatched systems with compensating controls documented.

> **Note:** ISO 27002:2022 guidance references "timely" but does not set numeric SLAs. The thresholds in ASSUME-ISO-A8-004 align with PCI DSS Req 6.3.3 for organizations subject to both frameworks — using PCI thresholds satisfies ISO when both apply.

---

## A.8.9 — Configuration Management *(new in 2022)* (HIGH)

| Element | Value | Classification |
|---|---|---|
| Obligation | Configurations (including security configurations) of hardware, software, services, and networks documented, implemented, monitored, and reviewed | DETERMINISTIC (existence) / PARAMETERIZED (completeness) |
| Evidence | `configuration_baselines.exists == true`; `configuration_drift_monitoring.enabled == true` | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-A8-005):** Configuration management is adequate when: (1) secure configuration baselines documented for each system class (server OS, network device, container image, cloud instance type); (2) baselines based on recognized hardening guidance (CIS Benchmarks or equivalent); (3) drift from baseline detected and alerted; (4) configuration changes go through change management process; (5) baselines reviewed at least annually or after significant system changes.

---

## A.8.13 — Information Backup (HIGH)

| Element | Value | Classification |
|---|---|---|
| Obligation | Backup copies of information, software, and system images maintained and regularly tested | DETERMINISTIC (existence) / PARAMETERIZED (frequency/test interval) |
| Evidence | `backup_policy.exists == true`; `backup_test_records.last_restore_test_date`; `backup_config.offsite_copy == true` | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-A8-006):** Backup is adequate when: (1) backup frequency aligned with RPO (Recovery Point Objective) defined in BIA; (2) backup copies stored offsite or in a separate cloud region from production; (3) restore test performed at least quarterly to verify backup integrity; (4) backup encryption enabled; (5) backup media access controlled.

---

## A.8.15 — Logging (HIGH)

| Element | Value | Classification |
|---|---|---|
| Obligation | Event logs produced, stored, protected, and analysed; logging activities include user activities, exceptions, faults, and IS events | DETERMINISTIC (log field requirements) / PARAMETERIZED (retention) |
| Evidence | `logging_config.enabled == true`; log schema includes user ID, timestamp, event type, source, outcome; `log_retention_policy` | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-A8-007):** Logging is adequate when: (1) all authentication events logged (success and failure); (2) all privileged account actions logged; (3) access to sensitive data logged; (4) log entries include user identity, timestamp, event type, source, and outcome; (5) logs stored tamper-evidently (separate system or SIEM); (6) logs retained for the period specified in the data retention policy (minimum 12 months for audit purposes, align with PCI DSS if applicable); (7) logs reviewed regularly (critical systems daily, others weekly).

---

## A.8.17 — Clock Synchronisation (DETERMINISTIC)

| Element | Value | Classification |
|---|---|---|
| Obligation | Clocks of all relevant information processing systems synchronised to approved time sources | DETERMINISTIC |
| Evidence | `ntp_config.enabled == true` on all CDE/sensitive systems; `ntp_config.source` consistent; `clock_drift_monitoring` | DETERMINISTIC |

---

## A.8.24 — Use of Cryptography (MEDIUM)

| Element | Value | Classification |
|---|---|---|
| Obligation | Rules on cryptographic use implemented; key management lifecycle addressed | PARAMETERIZED |
| Evidence | `cryptography_policy.exists == true`; algorithm standards documented; key management procedures | PARAMETERIZED |

**Assumption (ASSUME-ISO-A8-008):** Cryptographic use policy is adequate when it specifies: (1) approved algorithms and key lengths (AES-128/256 for symmetric, RSA-2048+ or ECDSA P-256+ for asymmetric, SHA-256+ for hashing); (2) prohibited algorithms (MD5, SHA-1, DES, 3DES, RC4); (3) key management requirements (generation, storage, distribution, rotation, destruction); (4) certificate management for TLS (minimum TLS 1.2, preferred TLS 1.3).

---

## A.8.31 — Separation of Development, Test, and Production (DETERMINISTIC)

| Element | Value | Classification |
|---|---|---|
| Obligation | Development, testing, and production environments separated | DETERMINISTIC |
| Evidence | `environment_separation_config.dev_test_prod_isolated == true`; no production data in dev/test without anonymization | DETERMINISTIC |

---

## YAML specifications

### `a8_logging.yaml`

```yaml
regulation_id: ISO-27001-2022-A.8.15
section: "ISO 27001:2022 Annex A — Logging"
r_or_a: Required
source_text: >
  Event logs that record user activities, exceptions, faults and IS events
  shall be produced, stored, protected and analysed.

extracted_elements:
  subject: "All systems processing information subject to the ISMS"
  condition: "System is in ISMS scope"
  obligation: "Logging enabled; required fields present; logs protected; logs reviewed"
  evidence: "logging_config: enabled, schema fields; log_retention_policy; review_records"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: PARAMETERIZED

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-ISO-A8-007
    assumption_text: >
      Adequate: all auth events logged; privileged actions logged; sensitive data access logged;
      required fields present; tamper-evident storage; 12-month minimum retention;
      daily review for critical systems.
    assumed_by: "ISMS Manager"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
    cryptographic_hash: "sha256:pending-ci"
test_confidence: HIGH
generated_test: "tests/iso27001/test_a8_technological.py"
```

---

## Generated tests

### `tests/iso27001/test_a8_technological.py`

```python
"""
ISO 27001:2022 Annex A Theme 4 — Technological Controls
Confidence: HIGH for A.8.5/A.8.7/A.8.13/A.8.15/A.8.17; MEDIUM/PARAMETERIZED for others
"""
import pytest
from datetime import date

LOG_RETENTION_MIN_MONTHS = 12
BACKUP_RESTORE_TEST_MAX_DAYS = 90
AV_DEFINITION_MAX_AGE_HOURS = 24
PRIVILEGED_ACCESS_REVIEW_MAX_DAYS = 180


def test_ntp_configured_on_all_isms_systems(isms_system_configs):
    """A.8.17 — All ISMS systems must have clock synchronisation configured."""
    violations = [
        s for s in isms_system_configs
        if s.get("in_isms_scope") and not s.get("ntp_configured")
    ]
    assert not violations, (
        f"NONCONFORMITY (A.8.17): {len(violations)} ISMS system(s) without NTP: "
        f"{[s['system_id'] for s in violations]}"
    )


def test_dev_test_prod_environments_separated(environment_configs):
    """A.8.31 — Development, test, and production environments must be separated."""
    violations = [
        e for e in environment_configs
        if not e.get("separated_from_production")
        and e.get("environment_type") in ("development", "test")
    ]
    assert not violations, (
        f"NONCONFORMITY (A.8.31): {len(violations)} dev/test environment(s) not "
        f"separated from production: {[e['environment_id'] for e in violations]}"
    )


def test_logging_enabled_on_isms_systems(isms_system_configs):
    """A.8.15 — Event logging must be enabled on all ISMS-scoped systems."""
    violations = [
        s for s in isms_system_configs
        if s.get("in_isms_scope") and not s.get("logging_enabled")
    ]
    assert not violations, (
        f"NONCONFORMITY (A.8.15): {len(violations)} ISMS system(s) without logging: "
        f"{[s['system_id'] for s in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-ISO-A8-007",
    description=(
        "Adequate logging: auth events, privileged actions, sensitive data access; "
        "required fields; tamper-evident storage; 12-month retention; daily review "
        "for critical systems."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_log_retention_minimum_12_months(log_retention_configs):
    violations = [
        c for c in log_retention_configs
        if c.get("retention_months", 0) < LOG_RETENTION_MIN_MONTHS
    ]
    assert not violations, (
        f"NONCONFORMITY (A.8.15): {len(violations)} log retention configuration(s) "
        f"below 12-month minimum: "
        f"{[(c['system_id'], c.get('retention_months')) for c in violations]}"
    )


def test_av_deployed_and_current(isms_system_configs, av_configs):
    """A.8.7 — Malware protection deployed and definitions current."""
    av_map = {c["system_id"]: c for c in av_configs}
    violations = []
    for system in isms_system_configs:
        if not system.get("in_isms_scope") or system.get("av_exempt"):
            continue
        av = av_map.get(system["system_id"])
        if not av:
            violations.append(f"{system['system_id']}: no AV record")
            continue
        if not av.get("auto_update_enabled"):
            violations.append(f"{system['system_id']}: AV auto-update disabled")
        age_h = av.get("last_definition_update_age_hours", 9999)
        if age_h > AV_DEFINITION_MAX_AGE_HOURS:
            violations.append(
                f"{system['system_id']}: AV definitions {age_h}h old "
                f"(max {AV_DEFINITION_MAX_AGE_HOURS}h)"
            )
    assert not violations, (
        f"NONCONFORMITY (A.8.7): {len(violations)} malware protection issue(s):\n"
        + "\n".join(violations)
    )


@pytest.mark.assumption(
    id="ASSUME-ISO-A8-006",
    description=(
        "Backup adequate: frequency aligned with RPO; offsite/separate region; "
        "restore test ≥ quarterly; encrypted; access controlled."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_backup_restore_test_within_90_days(backup_test_records):
    """A.8.13 — Backup restore test performed at least quarterly."""
    today = date.today()
    if not backup_test_records:
        assert False, (
            "NONCONFORMITY (A.8.13): No backup restore test records found — "
            "restore testing is required to verify backup integrity"
        )
    latest = max(backup_test_records, key=lambda r: r["test_date"])
    days_since = (today - latest["test_date"]).days
    assert days_since <= BACKUP_RESTORE_TEST_MAX_DAYS, (
        f"NONCONFORMITY (A.8.13): Last backup restore test was {days_since} days ago "
        f"(max {BACKUP_RESTORE_TEST_MAX_DAYS})"
    )


@pytest.mark.assumption(
    id="ASSUME-ISO-A8-001",
    description=(
        "Privileged access: inventoried with approval; reviewed ≥ 6-monthly; "
        "separated from normal access; session logging enabled; generic admin disabled."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_privileged_access_reviewed_within_6_months(privileged_access_reviews):
    """A.8.2 — Privileged access reviewed at planned intervals (6 months maximum)."""
    today = date.today()
    if not privileged_access_reviews:
        assert False, (
            "NONCONFORMITY (A.8.2): No privileged access review records found"
        )
    latest = max(privileged_access_reviews, key=lambda r: r["review_date"])
    days_since = (today - latest["review_date"]).days
    assert days_since <= PRIVILEGED_ACCESS_REVIEW_MAX_DAYS, (
        f"NONCONFORMITY (A.8.2): Privileged access last reviewed {days_since} days ago "
        f"(max {PRIVILEGED_ACCESS_REVIEW_MAX_DAYS})"
    )
```

---

## Notes for the registry

- **A.8.9 Configuration Management is new in 2022:** This control did not exist in ISO 27001:2013. It explicitly requires documented secure configuration baselines and drift monitoring. Organizations transitioning from the 2013 edition need to add this control to their SoA and implement configuration baseline management.
- **A.8.7 vs. PCI DSS Req 5:** ISO 27001 A.8.7 has no explicit update frequency requirement. The 24-hour AV definition update threshold is derived from ISO 27002:2022 guidance and PCI DSS Req 5.3.1 cross-framework alignment. Using PCI DSS's explicit threshold is a defensible approach for organizations subject to both frameworks.
- **A.8.15 vs. HIPAA audit controls:** ISO 27001 A.8.15 does not specify a retention period. The 12-month minimum in ASSUME-ISO-A8-007 aligns with PCI DSS Req 10.5.1. For HIPAA-subject organizations, apply the 6-year documentation retention rule; for PCI-subject organizations, apply the 12-month/3-month-immediate rule. Design to the stricter of the two.
- **A.8.24 new controls (2022):** The 2022 edition added A.8.9 (configuration management), A.8.10 (information deletion), A.8.11 (data masking), A.8.12 (data leakage prevention), A.8.16 (monitoring activities), and A.8.28 (secure coding) to the technology theme. All must appear in the SoA.
- **Cross-reference to PCI DSS:** A.8.5 ↔ PCI Req 8; A.8.7 ↔ PCI Req 5; A.8.8 ↔ PCI Req 6 & 11; A.8.9 ↔ PCI Req 2; A.8.13 ↔ HIPAA §164.308(a)(7); A.8.15 ↔ PCI Req 10; A.8.17 ↔ PCI Req 10.6. Single evidence artifacts satisfy all applicable frameworks where alignment exists.
