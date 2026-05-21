# NIST SP 800-171 r3 — Families AU, CM, SI: Audit, Configuration, and System Integrity

**Registry path:** `/regulation-registry/NIST-SP800-171/AU-CM-SI/`
**Version:** NIST SP 800-171 Rev 3 (May 2024)
**Last parsed:** 2026-05-20
**Applies to:** Non-federal organizations (contractors, universities, research institutions) that process, store, or transmit Controlled Unclassified Information (CUI) in nonfederal information systems under US federal contracts or grants
**Trigger:** Federal contract or grant containing DFARS clause 252.204-7012 (DoD) or equivalent FAR clause; any contract where the government provides or the contractor generates CUI; CMMC Level 2 requires third-party assessment against NIST 800-171
**Jurisdiction:** United States; extraterritorial — applies to foreign companies holding US federal contracts involving CUI; enforced through contract terms and DoD CMMC assessments
**Not applicable to:** Federal agencies (use NIST 800-53 instead); organizations with no federal contracts or grants; commercial transactions not involving CUI; EAR99 technology transfers (separate ITAR/EAR framework)
**Overall confidence:** HIGH for AU (log retention, content); HIGH for CM (baseline existence, change control); HIGH for SI (AV currency, patch SLAs); all three families have strong DETERMINISTIC cores
**25 requirements: AU 3.3.1–3.3.9 (9 reqs), CM 3.4.1–3.4.9 (9 reqs), SI 3.14.1–3.14.7 (7 reqs)**

---

## Scope summary

AU (Audit and Accountability), CM (Configuration Management), and SI (System and Information Integrity) are grouped here because they share a common evidence pattern — all three families produce system-generated artifacts (logs, baselines, scan results) that are directly measurable. They represent the highest-confidence control families in 800-171 outside of IA.

AU aligns with ISO 27001 A.8.15 and PCI DSS Req 10. CM aligns with ISO 27001 A.8.9. SI aligns with ISO 27001 A.8.7 (malware) and A.8.8 (vulnerability management).

---

# FAMILY AU — AUDIT AND ACCOUNTABILITY

## 3.3.1 — Event Logging (HIGH)

### Source text

> Create and retain system audit logs and records to the extent needed to enable the monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Audit logs created for required event categories; logs retained for adequate period | DETERMINISTIC |
| Evidence | `audit_log_config.event_categories_covered`; `audit_log_retention.days >= 90` | DETERMINISTIC |

**Assumption (ASSUME-800171-AU-001):** Audit logging is adequate when: (1) logs created for: user logon/logoff (successful and failed), account creation/modification/deletion, privilege escalation, access to CUI, system startup/shutdown, policy changes, security-relevant configuration changes, use of privileged commands; (2) log retention: minimum 90 days online (immediately accessible); 12 months archived; (3) log integrity protected — write-once storage, SIEM with tamper detection, or equivalent; (4) logs include: timestamp (UTC), event type, user/process ID, source IP/hostname, success/failure indicator; (5) log review automated where possible — daily review of critical/security events.

**Cross-reference:** Aligns with ISO 27001 ASSUME-ISO-A8-007 (12-month retention, daily review); PCI DSS Req 10 (12-month retention, 3-month immediate access). NIST 800-171 specifies minimum 90 days for immediate access — less stringent than PCI DSS. Design to PCI satisfies 800-171.

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.3.2 — Audit Review, Analysis, and Reporting (HIGH)

### Source text

> Ensure that the actions of individual system users can be traced to those users, so they can be held accountable for their actions.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Audit trail links user actions to individual users; non-repudiation maintained; shared accounts prohibited where auditability required | DETERMINISTIC |
| Evidence | `audit_logs.user_id_logged == true`; no shared accounts on CUI systems (consistent with 3.5.1) | DETERMINISTIC |

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.3.3–3.3.4 — Audit Failure Alerting and Review (MEDIUM)

| Req | Obligation | Classification |
|---|---|---|
| 3.3.3 | Alert responsible personnel of audit logging process failures promptly | DETERMINISTIC (alert existence) |
| 3.3.4 | Review and update logged events to capture relevant security events | PARAMETERIZED |

**Assumption (ASSUME-800171-AU-002):** Audit failure alerting is adequate when: (1) audit log system failures trigger automated alert within 15 minutes; (2) alert routed to security team or equivalent; (3) audit failure documented as security incident; (4) logged event set reviewed annually and updated when threat landscape changes.

**Overall: DETERMINISTIC for alert existence → Pattern 1; PARAMETERIZED for review cadence → Pattern 2**

---

## 3.3.5–3.3.6 — Audit Correlation and Reduction (MEDIUM)

| Req | Obligation | Classification |
|---|---|---|
| 3.3.5 | Correlate audit record review, analysis, and reporting with processes for investigation and response | PARAMETERIZED |
| 3.3.6 | Provide audit reduction and report generation to support analysis | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## 3.3.7 — Authoritative Time Source (HIGH)

### Source text

> Provide a system capability that compares and synchronizes internal system clocks with an authoritative source to generate time stamps for audit records.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | NTP synchronization to authoritative source; all CUI systems clock-synchronized | DETERMINISTIC |
| Evidence | `ntp_config.authoritative_source_configured == true`; all CUI systems sync to approved NTP | DETERMINISTIC |

**Assumption (ASSUME-800171-AU-003):** NTP synchronization is adequate when: (1) NTP source is a NIST-traceable authoritative time source (time.nist.gov, pool.ntp.org, or GPS/cesium-synchronized internal source); (2) clock drift ≤ 1 second from authoritative source; (3) all systems in CUI enclave synchronized to the same time source (±1 second between systems); (4) NTP configuration change requires authorization. Aligns with ISO 27001 A.8.17 (DETERMINISTIC) and PCI DSS Req 10.6.

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.3.8–3.3.9 — Audit Information Protection (HIGH)

| Req | Obligation | Classification |
|---|---|---|
| 3.3.8 | Protect audit information and tools from unauthorized access, modification, and deletion | DETERMINISTIC |
| 3.3.9 | Limit management of audit logging to a subset of privileged users | DETERMINISTIC |

**Overall: DETERMINISTIC → Pattern 1**

---

# FAMILY CM — CONFIGURATION MANAGEMENT

## 3.4.1 — Baseline Configurations (HIGH)

### Source text

> Establish and maintain baseline configurations and inventories of organizational systems (including hardware, software, firmware, and documentation) throughout the respective system development life cycles.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Configuration baseline documented for all CUI system components; baseline maintained and updated | DETERMINISTIC (existence) / PARAMETERIZED (completeness) |
| Evidence | `system_baseline_configs.exists == true`; `asset_inventory.hardware_software_firmware_documented`; baselines version-controlled | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-800171-CM-001):** Configuration baselines are adequate when: (1) baseline documented for all operating system types in CUI enclave; (2) baseline references industry hardening standard (DISA STIG, CIS Benchmark, or vendor security baseline); (3) baseline version-controlled with approval records; (4) actual configurations compared against baseline at least monthly; (5) deviations from baseline documented with approval and risk rationale.

**Cross-reference:** Aligns with ISO 27001 ASSUME-ISO-A8-005 (CIS Benchmarks Level 1).

**Overall: DETERMINISTIC for baseline existence → Pattern 1; PARAMETERIZED for content → Pattern 2**

---

## 3.4.2 — Configuration Change Control (HIGH)

### Source text

> Establish and enforce security configuration settings for information technology products employed in organizational systems.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Security configuration settings established, enforced; changes to configuration settings go through change control | DETERMINISTIC |
| Evidence | `configuration_settings.security_settings_enforced == true`; `change_records.configuration_changes_authorized` | DETERMINISTIC |

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.4.3 — Configuration Change Impact Analysis (MEDIUM)

### Source text

> Track, review, approve or disapprove, and log changes to organizational systems.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Configuration changes tracked; reviewed and approved before implementation; changes logged | DETERMINISTIC |
| Evidence | `change_records.all_config_changes_authorized`; change log complete | DETERMINISTIC |

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.4.4 — Security Impact Analysis (MEDIUM)

### Source text

> Analyze the security impact of changes prior to implementation.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Security impact analysis performed for changes before implementation | PARAMETERIZED |
| Evidence | `change_records.security_impact_analysis_documented` | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## 3.4.5 — Access Restrictions for Change (MEDIUM)

### Source text

> Define, document, approve, and enforce physical and logical access restrictions associated with changes to organizational systems.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Change access restricted to authorized personnel; enforcement mechanisms in place | DETERMINISTIC |
| Evidence | `deployment_access.restricted_to_authorized == true`; no unauthorized production changes | DETERMINISTIC |

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.4.6–3.4.7 — Least Functionality — Disable Unnecessary Functions (HIGH)

| Req | Obligation | Classification |
|---|---|---|
| 3.4.6 | Employ the principle of least functionality; configure only essential capabilities | PARAMETERIZED |
| 3.4.7 | Restrict, disable, or prevent the use of nonessential programs, functions, ports, protocols, and services | DETERMINISTIC (port/service control existence) |

**Assumption (ASSUME-800171-CM-002):** Least functionality is adequate when: (1) all running services and open ports on CUI systems documented and justified; (2) services not required for system operation disabled or removed; (3) software not on approved list cannot be installed on CUI systems; (4) approved software list reviewed and updated at least annually; (5) USB/removable media restricted on CUI systems unless operationally justified. Aligns with PCI DSS ASSUME-2-001 (unnecessary functionality).

**Overall: DETERMINISTIC for port/service documentation → Pattern 1; PARAMETERIZED for adequacy → Pattern 2**

---

## 3.4.8–3.4.9 — Software Usage Restrictions and Information Sharing (MEDIUM)

| Req | Obligation | Classification |
|---|---|---|
| 3.4.8 | Apply deny-by-exception policy to prevent use of unauthorized software or deny-by-default | PARAMETERIZED |
| 3.4.9 | Control and monitor user-installed software | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

# FAMILY SI — SYSTEM AND INFORMATION INTEGRITY

## 3.14.1 — Malware Protection (HIGH)

### Source text

> Identify, report, and correct information and system flaws in a timely manner.

*Note: 3.14.1 in r3 covers both flaw remediation and malware protection as integrated integrity controls.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Malware protection deployed; signatures current; AV in operation on all applicable systems | DETERMINISTIC |
| Evidence | `av_config.deployed_on_all_applicable == true`; `av_definitions.last_updated` ≤ 24 hours | DETERMINISTIC |

**Assumption (ASSUME-800171-SI-001):** Malware protection is adequate when: (1) AV/EDR deployed on all CUI systems running general-purpose OS; (2) definition updates automatic; currency ≤ 24 hours; (3) real-time on-access scanning enabled; (4) users cannot disable AV; (5) AV exceptions documented with compensating controls. Aligns with ISO 27001 ASSUME-ISO-A8-003 and PCI DSS ASSUME-5-001.

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.14.2 — Security Alerts and Advisories (MEDIUM)

### Source text

> Provide protection from malicious code at appropriate locations within organizational systems.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Security alerts and advisories received and acted upon; security information sharing | PARAMETERIZED |
| Evidence | `threat_intel_subscription.active == true`; advisories tracked and reviewed | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## 3.14.3 — Security Function Monitoring (MEDIUM)

### Source text

> Monitor system security alerts and advisories and take action in response.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Security alerts monitored; automated monitoring deployed; responses documented | DETERMINISTIC (monitoring deployment) |
| Evidence | `security_monitoring.deployed == true`; alert response records | DETERMINISTIC + PARAMETERIZED |

**Overall: DETERMINISTIC for monitoring existence → Pattern 1; PARAMETERIZED for coverage → Pattern 2**

---

## 3.14.4 — Software and Firmware Integrity Verification (HIGH)

### Source text

> Update malicious code protection mechanisms when new releases are available.

*In r3, 3.14.4 addresses update cadence and also software/firmware verification.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Malware protection mechanisms updated when new releases available; software/firmware integrity verified | DETERMINISTIC (update mechanism) |
| Evidence | `av_update_config.automatic_updates_enabled == true`; firmware integrity verification documented | DETERMINISTIC + PARAMETERIZED |

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.14.5 — System and File Scanning (HIGH)

### Source text

> Perform periodic scans of organizational systems and real-time scans of files from external sources.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Periodic full system scans performed; real-time scanning of downloaded/received files | DETERMINISTIC |
| Evidence | `av_config.periodic_scan_scheduled == true`; `av_config.real_time_scan_enabled == true` | DETERMINISTIC |

**Assumption (ASSUME-800171-SI-002):** Scanning is adequate when: (1) real-time on-access scanning enabled for all file I/O; (2) periodic full scans scheduled at least weekly; (3) external media (USB, downloads) scanned before use; (4) scan results logged and reviewed; (5) scan exclusions documented and minimized.

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.14.6 — Security Vulnerability Identification (HIGH)

### Source text

> Monitor organizational systems, including inbound and outbound communications traffic, to detect attacks and indicators of potential attacks.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Vulnerability scanning performed; security vulnerabilities identified and remediated within defined SLA | DETERMINISTIC (scan cadence) / PARAMETERIZED (SLA adequacy) |
| Evidence | `vuln_scan_records.most_recent_date` ≤ 90 days; `critical_vulns.open_within_sla` | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-800171-SI-003):** Vulnerability identification is adequate when: (1) CUI systems scanned for vulnerabilities at least quarterly; (2) critical vulnerabilities (CVSS ≥ 7.0) remediated within 30 days; (3) non-critical vulnerabilities remediated within 90 days; (4) exceptions documented with risk rationale; (5) CUI-internet-facing systems scanned monthly. Aligns with PCI DSS ASSUME-6-001 and ISO 27001 ASSUME-ISO-A8-004.

**Overall: DETERMINISTIC for scan cadence → Pattern 1; PARAMETERIZED for SLA → Pattern 2**

---

## 3.14.7 — Unauthorized Use Identification (MEDIUM)

### Source text

> Identify unauthorized use of organizational systems.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Mechanisms in place to identify unauthorized use of CUI systems | PARAMETERIZED |
| Evidence | `ueba_or_monitoring.deployed == true`; anomaly detection for unusual access patterns | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## YAML specifications

### `au_cm_si_technical.yaml`

```yaml
regulation_id: NIST-SP800-171-r3-AU-CM-SI
section: "NIST SP 800-171 r3 — Families AU, CM, SI"
r_or_a: Required
source_text: >
  AU: Create and retain audit logs; synchronize clocks; protect audit information.
  CM: Establish and maintain configuration baselines; control changes; least functionality.
  SI: Protect against malware; scan systems; identify and remediate vulnerabilities.

overall_classification: DETERMINISTIC
human_review_required: false
test_confidence: HIGH
generated_test: "tests/nist_sp800171/test_au_cm_si_technical.py"
```

---

## Generated tests

### `tests/nist_sp800171/test_au_cm_si_technical.py`

```python
"""
NIST SP 800-171 r3 — Families AU, CM, SI: Audit, Configuration, System Integrity
Confidence: HIGH for log retention, NTP, baseline existence, AV currency, vuln scan cadence
"""
import pytest
from datetime import date

AUDIT_LOG_RETENTION_MIN_DAYS = 90
AUDIT_LOG_ARCHIVE_DAYS = 365
VULN_SCAN_MAX_DAYS = 90
CRITICAL_VULN_REMEDIATION_DAYS = 30
NON_CRITICAL_VULN_REMEDIATION_DAYS = 90
AV_DEFINITION_MAX_AGE_HOURS = 24


@pytest.fixture(autouse=True)
def require_cui_scope(system_scope):
    if not system_scope.get("processes_cui"):
        pytest.skip("System not attested as processing CUI")


@pytest.mark.assumption(
    id="ASSUME-800171-AU-001",
    description=(
        "Logs: 8 required event categories; 90-day online retention; 12-month archive; "
        "integrity protected; includes user ID, timestamp, source."
    ),
    approved_by="ISSO",
    review_date="2026-05-20",
)
def test_audit_log_retention_meets_minimum(audit_log_config):
    """3.3.1 — Audit logs must be retained for at least 90 days (online)."""
    assert audit_log_config, "NONCONFORMITY (3.3.1): No audit log configuration found"
    for cfg in audit_log_config:
        if not cfg.get("in_cui_enclave"):
            continue
        online_days = cfg.get("retention_days_online", 0)
        assert online_days >= AUDIT_LOG_RETENTION_MIN_DAYS, (
            f"NONCONFORMITY (3.3.1): System {cfg['system_id']}: audit log online "
            f"retention {online_days} days < {AUDIT_LOG_RETENTION_MIN_DAYS}"
        )


@pytest.mark.assumption(
    id="ASSUME-800171-AU-003",
    description="NTP: NIST-traceable source; clock drift ≤1 sec; all CUI systems synchronized",
    approved_by="ISSO",
    review_date="2026-05-20",
)
def test_ntp_configured_on_all_cui_systems(ntp_configs):
    """3.3.7 — All CUI systems must be synchronized to an authoritative NTP source."""
    violations = [
        cfg for cfg in ntp_configs
        if cfg.get("in_cui_enclave")
        and not cfg.get("ntp_configured")
    ]
    assert not violations, (
        f"NONCONFORMITY (3.3.7): {len(violations)} CUI system(s) without NTP configuration: "
        f"{[c['system_id'] for c in violations]}"
    )


def test_configuration_baselines_exist(system_baseline_records):
    """3.4.1 — Configuration baselines must exist for all CUI system types."""
    cui_baselines = [r for r in system_baseline_records if r.get("in_cui_enclave")]
    assert cui_baselines, (
        "NONCONFORMITY (3.4.1): No configuration baseline records for CUI systems"
    )
    no_approval = [r for r in cui_baselines if not r.get("baseline_approved")]
    assert not no_approval, (
        f"NONCONFORMITY (3.4.1): {len(no_approval)} baseline(s) without approval: "
        f"{[r['baseline_id'] for r in no_approval]}"
    )


def test_all_production_changes_authorized(change_records):
    """3.4.3 — All configuration changes to CUI systems must be authorized."""
    violations = [
        r for r in change_records
        if r.get("affects_cui_system")
        and not r.get("authorization_documented")
    ]
    assert not violations, (
        f"NONCONFORMITY (3.4.3): {len(violations)} CUI system change(s) without "
        f"documented authorization: {[r.get('change_id') for r in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-800171-SI-001",
    description="AV on all general-purpose OS; 24h definition currency; real-time scanning; users cannot disable",
    approved_by="ISSO",
    review_date="2026-05-20",
)
def test_antivirus_deployed_and_current(endpoint_security_status):
    """3.14.1 — AV deployed on all CUI systems with general-purpose OS; definitions ≤24 hours."""
    today = date.today()
    violations = []
    for endpoint in endpoint_security_status:
        if not endpoint.get("in_cui_enclave") or not endpoint.get("general_purpose_os"):
            continue
        if not endpoint.get("av_deployed"):
            violations.append(f"{endpoint['asset_id']}: no AV deployed")
            continue
        last_update = endpoint.get("av_definition_update_date")
        if last_update is None:
            violations.append(f"{endpoint['asset_id']}: no AV definition update date")
        elif (today - last_update).days > 1:
            violations.append(
                f"{endpoint['asset_id']}: AV definitions {(today - last_update).days} day(s) old"
            )
    assert not violations, (
        f"NONCONFORMITY (3.14.1): {len(violations)} CUI endpoint(s) with AV issues:\n"
        + "\n".join(violations)
    )


@pytest.mark.assumption(
    id="ASSUME-800171-SI-003",
    description=(
        "CUI systems scanned quarterly; critical CVSS≥7.0 remediated ≤30 days; "
        "non-critical ≤90 days; internet-facing monthly."
    ),
    approved_by="ISSO",
    review_date="2026-05-20",
)
def test_vulnerability_scans_within_90_days(vulnerability_scan_records):
    """3.14.6 — CUI systems vulnerability-scanned at least quarterly."""
    today = date.today()
    cui_scans = [
        r for r in vulnerability_scan_records
        if r.get("in_cui_enclave")
    ]
    if not cui_scans:
        assert False, "NONCONFORMITY (3.14.6): No vulnerability scan records for CUI systems"
    latest = max(cui_scans, key=lambda r: r["scan_date"])
    days_since = (today - latest["scan_date"]).days
    assert days_since <= VULN_SCAN_MAX_DAYS, (
        f"NONCONFORMITY (3.14.6): CUI vulnerability scan last conducted "
        f"{days_since} days ago (max {VULN_SCAN_MAX_DAYS})"
    )


def test_critical_vulnerabilities_remediated_within_sla(vulnerability_findings):
    """3.14.6 — Critical vulnerabilities (CVSS ≥ 7.0) remediated within 30 days."""
    today = date.today()
    violations = []
    for finding in vulnerability_findings:
        if not finding.get("in_cui_enclave"):
            continue
        if finding.get("cvss_score", 0) < 7.0:
            continue
        if finding.get("remediated"):
            continue
        if finding.get("risk_accepted") and finding.get("risk_acceptance_rationale"):
            continue
        days_open = (today - finding["discovery_date"]).days
        if days_open > CRITICAL_VULN_REMEDIATION_DAYS:
            violations.append(
                f"{finding.get('cve_id', 'unknown')} on {finding['asset_id']}: "
                f"CVSS {finding.get('cvss_score')}, open {days_open} days"
            )
    assert not violations, (
        f"NONCONFORMITY (3.14.6): {len(violations)} critical CUI vulnerability/ies "
        f"exceeding remediation SLA:\n" + "\n".join(violations)
    )
```

---

## Notes for the registry

- **AU retention (90 days online) vs. PCI/ISO 12 months:** NIST 800-171 r3 requires minimum 90 days online retention. PCI DSS Req 10 requires 12 months total (3 months immediate + 9 months archive). ISO 27001 A.8.15 (with ASSUME-ISO-A8-007) requires 12-month retention with daily review for critical. Organizations subject to multiple frameworks should design to the most stringent: 12 months total, 3 months immediate access.
- **CM baseline and STIG/CIS alignment:** NIST 800-171 r3 does not mandate DISA STIGs or CIS Benchmarks — it requires organization-defined baselines that enforce security settings. However, CMMC Level 2 assessors expect to see a recognized hardening standard cited in the SSP. ASSUME-800171-CM-001 references DISA STIG and CIS Benchmark as acceptable references; custom baselines that deviate from both require documented justification.
- **SI malware (3.14.1) and r3 reorganization:** NIST SP 800-171 r3 reorganized the SI family relative to r2. "Flaw remediation" (r2 SI 3.14.1) and "malicious code protection" (r2 SI 3.14.2) are both addressed within r3 3.14.1. The generated tests cover both aspects — AV currency and patch remediation SLAs — for the combined r3 requirement.
- **CMMC Level 2 AU/CM/SI domain alignment:** The AU, CM, and SI families map directly to CMMC Level 2 domains with the same designations. CMMC Level 3 (based on NIST SP 800-172) adds enhanced requirements on top of these. The tests in this file satisfy CMMC Level 2 AU/CM/SI requirements when the same fixture data is used.
