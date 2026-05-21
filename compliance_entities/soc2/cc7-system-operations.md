# SOC 2 TSC 2017 — CC7: System Operations

**Registry path:** `/regulation-registry/SOC2/CC7/`
**Version:** AICPA TSC 2017 (2022 points of focus updates)
**Last parsed:** 2026-05-20
**Overall confidence:** HIGH for CC7.1 (vulnerability management scan cadence); MEDIUM for CC7.2–CC7.4 (monitoring, incident response, and recovery completeness are PARAMETERIZED)
**5 criteria: CC7.1–CC7.5**

---

## Scope summary

CC7 covers ongoing monitoring of system operations — detecting vulnerabilities, identifying anomalies, responding to incidents, and recovering from them. CC7 has the strongest cross-framework alignment of any SOC 2 series: CC7.1 maps to PCI DSS Req 11 (quarterly scans), ISO 27001 A.8.8 (vulnerability management), and NIST 800-53 RA-5/SI-2; CC7.3–CC7.4 map to ISO 27001 A.5.24–5.28 (incident management).

CC7.1 is DETERMINISTIC: vulnerability scan cadence is a measurable frequency threshold that tests can assert directly. CC7.2–CC7.5 are PARAMETERIZED because monitoring coverage, alert rule quality, and response plan completeness require human evaluation.

---

## CC7.1 — Vulnerability Management (HIGH)

### Source excerpt

> To meet its objectives, the entity uses detection and monitoring procedures to identify (1) changes to configurations that result in the introduction of new vulnerabilities, and (2) susceptibilities to newly discovered vulnerabilities.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All systems within SOC 2 system boundary | DETERMINISTIC |
| Condition | Ongoing; triggered by configuration changes and new vulnerability disclosures | DETERMINISTIC |
| Obligation | Vulnerability scans performed regularly; high/critical vulnerabilities remediated within defined SLA; patch management process in place | DETERMINISTIC (scan frequency) / PARAMETERIZED (remediation SLA) |
| Evidence | `vulnerability_scan_records.most_recent_date`; `scan_frequency` ≤ 90 days; `critical_vulnerabilities.open_count == 0` or within SLA | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-SOC2-CC7-001):** Vulnerability management is adequate when: (1) internal vulnerability scans performed at least quarterly; (2) external-facing systems scanned by qualified external scanner at least quarterly; (3) critical vulnerabilities (CVSS ≥ 9.0) remediated within 30 days; high vulnerabilities (CVSS 7.0–8.9) remediated within 60 days; (4) scan results reviewed and acted upon; exception process with documented risk acceptance for vulnerabilities that cannot be remediated within SLA; (5) new vulnerability disclosures (CISA KEV, vendor advisories) reviewed within 72 hours; (6) configuration changes trigger re-scan of affected systems within 30 days.

**Cross-reference:** Aligns with PCI DSS Req 11.3.1 (internal quarterly), 11.3.2 (external quarterly); ISO 27001 ASSUME-ISO-A8-004; NIST 800-53 RA-5.

**Overall: DETERMINISTIC for scan cadence → Pattern 1; PARAMETERIZED for SLA adequacy → Pattern 2**

---

## CC7.2 — Anomaly Detection and Monitoring (MEDIUM)

### Source excerpt

> The entity monitors system components and the operation of those controls on an ongoing basis to identify potential security events and assess the effectiveness of controls.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Monitoring tools deployed; anomaly detection rules configured; alerts generated for security-relevant events; alerts reviewed | DETERMINISTIC (monitoring tool existence) / PARAMETERIZED (coverage and rule quality) |
| Evidence | `siem_or_monitoring_tool.deployed == true`; `monitoring_rules.count > 0`; `alert_review_records.exists == true` | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-SOC2-CC7-002):** System monitoring is adequate when: (1) centralized log aggregation (SIEM or equivalent) deployed covering all systems in SOC 2 boundary; (2) alert rules cover at minimum: failed login attempts (≥ 5 consecutive), privilege escalation, large data exports, access outside business hours, configuration changes to security controls; (3) critical alerts reviewed within 15 minutes; standard security alerts reviewed within 24 hours; (4) log integrity protected (write-once storage or SIEM ingestion with tamper detection); (5) monitoring coverage reviewed and updated at least annually.

**Overall: DETERMINISTIC for tool existence → Pattern 1; PARAMETERIZED for alert rule coverage → Pattern 2**

---

## CC7.3 — Security Incident Response (MEDIUM)

### Source excerpt

> The entity evaluates security events to determine whether they could or have resulted in a failure of the entity to meet its objectives (security incidents) and, if so, takes actions to prevent or address such failures.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Incident response plan documented; events triaged and classified; incidents declared and responded to; response time SLA defined | DETERMINISTIC (plan existence) / PARAMETERIZED (plan adequacy) |
| Evidence | `incident_response_plan.documented == true`; `incident_records.classification_documented`; `incident_records.response_time` within SLA | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-SOC2-CC7-003):** Incident response is adequate when: (1) IRP documented with roles, responsibilities, escalation paths, and communication procedures; (2) severity classification scheme defined (P1/P2/P3 or equivalent); (3) P1 incidents (critical — customer impact) response SLA ≤ 1 hour; (4) incidents tracked in a ticketing system with timeline, actions taken, and communications logged; (5) subservice organizations and customers notified of material incidents within contractually committed or legally required timeframe (GDPR: 72 hours to supervisory authority; SOC 2 customer commitment: per SLA); (6) IRP tested at least annually via tabletop exercise.

**Cross-reference:** Aligns with ISO 27001 ASSUME-ISO-A5-006 (IRP adequacy); PCI DSS ASSUME-12-001; HIPAA §164.308(a)(6)(ii) (Security Incident Procedures).

**Overall: DETERMINISTIC for IRP existence → Pattern 1; PARAMETERIZED for plan adequacy → Pattern 2**

---

## CC7.4 — Incident Response and Recovery (MEDIUM)

### Source excerpt

> The entity responds to identified security incidents by executing a defined incident response program and recovering from the incident.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Incident response executed per documented procedures; containment, eradication, and recovery performed; root cause identified; post-incident review conducted | PARAMETERIZED |
| Evidence | `incident_records.containment_documented`; `incident_records.root_cause_documented`; `post_incident_review_records.exists` | PARAMETERIZED |

**Assumption (ASSUME-SOC2-CC7-004):** Incident response and recovery are adequate when: (1) incident record documents: detection date/time, declaration date/time, containment steps, eradication steps, recovery steps, customer communication timeline; (2) root cause analysis performed for all P1 and P2 incidents; (3) post-incident review conducted within 5 business days for major incidents; lessons learned communicated and tracked; (4) incident triggers review of the relevant control(s) that failed or were bypassed; (5) recovery activities validated — system functionality confirmed before returning to production; (6) customer notification content and timing documented in incident record for evidence.

**Overall: PARAMETERIZED → Pattern 2**

---

## CC7.5 — Identification of Threats — Monitoring for Relevant Security Events (PARAMETERIZED)

### Source excerpt

> The entity identifies, develops, and implements activities to prevent or detect and act upon security events from vulnerabilities or threats that could result in unauthorized or inappropriate access.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Threat intelligence gathered; monitoring updated for new threats; threat indicators integrated into detection | PARAMETERIZED |
| Evidence | `threat_intelligence_program.documented == true`; monitoring rules updated based on new threat intelligence; evidence of threat feed subscription or equivalent | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## YAML specifications

### `cc7_system_operations.yaml`

```yaml
regulation_id: SOC2-TSC2017-CC7
section: "SOC 2 TSC 2017 — CC7: System Operations"
r_or_a: Required
source_text: >
  The entity monitors system components and the operation of those controls on an
  ongoing basis to identify potential security events and assess the effectiveness
  of controls.

extracted_elements:
  subject: "All systems within SOC 2 boundary"
  condition: "Ongoing; quarterly minimum for vulnerability scans"
  obligation: "Quarterly vuln scans; monitoring deployed; IRP documented and tested; incidents tracked"
  evidence: "vuln_scan_records, monitoring_tool_status, incident_records, irp_documentation"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-SOC2-CC7-001
    assumption_text: >
      Vuln scans: quarterly internal and external; critical (CVSS ≥9.0) remediated ≤30 days;
      high (CVSS 7.0–8.9) ≤60 days; exception process for exceptions; KEV review ≤72 hours.
    assumed_by: "ISMS Manager"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
  - assumption_id: ASSUME-SOC2-CC7-003
    assumption_text: >
      IRP adequate: documented with roles + escalation + comms; severity classification;
      P1 response ≤1 hour; incidents tracked; customers notified per SLA/regulation; annual tabletop.
    assumed_by: "ISMS Manager"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
test_confidence: HIGH
generated_test: "tests/soc2/test_cc7_system_operations.py"
```

---

## Generated tests

### `tests/soc2/test_cc7_system_operations.py`

```python
"""
SOC 2 TSC 2017 — CC7: System Operations
Confidence: HIGH for CC7.1 scan cadence; MEDIUM for CC7.2–CC7.4
"""
import pytest
from datetime import date

VULN_SCAN_MAX_DAYS = 90
CRITICAL_VULN_REMEDIATION_DAYS = 30
HIGH_VULN_REMEDIATION_DAYS = 60
IRP_TEST_MAX_DAYS = 365


@pytest.mark.assumption(
    id="ASSUME-SOC2-CC7-001",
    description=(
        "Quarterly scans; critical CVSS≥9.0 remediated ≤30 days; high CVSS 7.0–8.9 ≤60 days; "
        "exception process for remediation delays."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_vulnerability_scans_within_90_days(vulnerability_scan_records):
    """CC7.1 — Internal and external vulnerability scans performed at least quarterly."""
    today = date.today()
    for scan_type in ("internal", "external"):
        scans = [
            r for r in vulnerability_scan_records
            if r.get("scan_type") == scan_type
            and r.get("in_soc2_boundary")
        ]
        if not scans:
            assert False, (
                f"NONCONFORMITY (CC7.1): No {scan_type} vulnerability scan records "
                f"found for SOC 2 boundary systems"
            )
        latest = max(scans, key=lambda r: r["scan_date"])
        days_since = (today - latest["scan_date"]).days
        assert days_since <= VULN_SCAN_MAX_DAYS, (
            f"NONCONFORMITY (CC7.1): {scan_type.capitalize()} vulnerability scan last "
            f"conducted {days_since} days ago (max {VULN_SCAN_MAX_DAYS})"
        )


def test_critical_vulnerabilities_remediated_within_sla(vulnerability_findings):
    """CC7.1 — Critical vulnerabilities (CVSS ≥ 9.0) remediated within 30 days."""
    today = date.today()
    violations = []
    for finding in vulnerability_findings:
        if not finding.get("in_soc2_boundary"):
            continue
        cvss = finding.get("cvss_score", 0)
        if cvss < 9.0:
            continue
        if finding.get("remediated"):
            continue
        if finding.get("risk_accepted") and finding.get("risk_acceptance_rationale"):
            continue
        days_open = (today - finding["discovery_date"]).days
        if days_open > CRITICAL_VULN_REMEDIATION_DAYS:
            violations.append(
                f"CVE {finding.get('cve_id', 'unknown')} on {finding['asset_id']}: "
                f"CVSS {cvss}, open {days_open} days (max {CRITICAL_VULN_REMEDIATION_DAYS})"
            )
    assert not violations, (
        f"NONCONFORMITY (CC7.1): {len(violations)} critical vulnerability/ies exceeding "
        f"remediation SLA:\n" + "\n".join(violations)
    )


def test_high_vulnerabilities_remediated_within_sla(vulnerability_findings):
    """CC7.1 — High vulnerabilities (CVSS 7.0–8.9) remediated within 60 days."""
    today = date.today()
    violations = []
    for finding in vulnerability_findings:
        if not finding.get("in_soc2_boundary"):
            continue
        cvss = finding.get("cvss_score", 0)
        if not (7.0 <= cvss < 9.0):
            continue
        if finding.get("remediated"):
            continue
        if finding.get("risk_accepted") and finding.get("risk_acceptance_rationale"):
            continue
        days_open = (today - finding["discovery_date"]).days
        if days_open > HIGH_VULN_REMEDIATION_DAYS:
            violations.append(
                f"CVE {finding.get('cve_id', 'unknown')} on {finding['asset_id']}: "
                f"CVSS {cvss}, open {days_open} days (max {HIGH_VULN_REMEDIATION_DAYS})"
            )
    assert not violations, (
        f"NONCONFORMITY (CC7.1): {len(violations)} high vulnerability/ies exceeding "
        f"remediation SLA:\n" + "\n".join(violations)
    )


def test_siem_or_monitoring_deployed(monitoring_system_status):
    """CC7.2 — Centralized monitoring/SIEM must be deployed for SOC 2 boundary systems."""
    soc2_monitoring = [
        m for m in monitoring_system_status
        if m.get("covers_soc2_boundary")
    ]
    assert soc2_monitoring, (
        "NONCONFORMITY (CC7.2): No centralized monitoring or SIEM deployed covering "
        "SOC 2 boundary systems"
    )
    all_active = all(m.get("status") == "active" for m in soc2_monitoring)
    assert all_active, (
        "NONCONFORMITY (CC7.2): One or more monitoring systems covering SOC 2 boundary "
        "are not in 'active' status"
    )


@pytest.mark.assumption(
    id="ASSUME-SOC2-CC7-003",
    description=(
        "IRP documented with roles, escalation, comms; P1 response ≤1 hour; "
        "incidents tracked; customer notification per SLA; annual tabletop."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_incident_response_plan_exists_and_current(incident_response_plan_records):
    """CC7.3 — Incident response plan must be documented and tested annually."""
    today = date.today()
    assert incident_response_plan_records, (
        "NONCONFORMITY (CC7.3): No incident response plan found — IRP is required"
    )
    latest = max(
        incident_response_plan_records,
        key=lambda r: r.get("last_reviewed_date", date.min)
    )
    days_since_review = (today - latest["last_reviewed_date"]).days
    assert days_since_review <= IRP_TEST_MAX_DAYS, (
        f"NONCONFORMITY (CC7.3): IRP last reviewed {days_since_review} days ago "
        f"(max {IRP_TEST_MAX_DAYS})"
    )
    days_since_test = (today - latest.get("last_test_date", date.min)).days
    assert days_since_test <= IRP_TEST_MAX_DAYS, (
        f"NONCONFORMITY (CC7.3): IRP last tested {days_since_test} days ago "
        f"(max {IRP_TEST_MAX_DAYS}) — annual tabletop exercise required"
    )


def test_incidents_have_documented_response(incident_records):
    """CC7.4 — All declared security incidents must have documented response records."""
    violations = [
        r for r in incident_records
        if r.get("declared")
        and not r.get("response_steps_documented")
    ]
    assert not violations, (
        f"NONCONFORMITY (CC7.4): {len(violations)} incident(s) declared but without "
        f"documented response steps: {[r.get('incident_id') for r in violations]}"
    )


def test_major_incidents_have_post_incident_review(incident_records):
    """CC7.4 — Major incidents (P1/P2) must have post-incident review."""
    violations = [
        r for r in incident_records
        if r.get("severity") in ("P1", "P2", "critical", "high")
        and not r.get("post_incident_review_completed")
    ]
    assert not violations, (
        f"NONCONFORMITY (CC7.4): {len(violations)} major incident(s) without "
        f"post-incident review: {[r.get('incident_id') for r in violations]}"
    )
```

---

## Notes for the registry

- **CC7.1 scan cadence vs. PCI DSS alignment:** SOC 2 CC7.1 does not explicitly state "quarterly" — that is ASSUME-SOC2-CC7-001, derived from PCI DSS Req 11.3.1/11.3.2 as the industry standard. SOC 2 auditors universally accept quarterly as meeting "ongoing." Organizations subject to both PCI and SOC 2 satisfy both with a single quarterly scan program.
- **CC7.2 monitoring coverage gap:** SOC 2 CC7.2 is frequently an observation point in Type II audits because organizations focus on perimeter alerting (firewall, IDS) but fail to cover internal threats (insider movement, unusual access patterns, large data transfers). ASSUME-SOC2-CC7-002 explicitly includes internal anomaly detection scenarios.
- **CC7.3 customer notification obligation:** SOC 2 customer notification timing is determined by contractual commitments in the service organization's agreements, not by TSC directly. However, the 72-hour GDPR window is the most binding external requirement for EU-customer-facing services. ASSUME-SOC2-CC7-003 references both contractual and regulatory timeframes.
- **CC7.4 and the evidence trail:** Type II auditors sample incident records for the full audit period to verify that the IRP was actually followed, not just that it exists. Organizations should ensure incident tickets capture: detection timestamp, declaration timestamp, each response step with timestamp and responsible party, customer communication records, and PIR completion date.
- **CC7.1 vs. NIST 800-53 RA-5 cadence:** NIST 800-53 RA-5 does not specify a scan frequency — it defers to organization-defined values. SOC 2 CC7.1 (with ASSUME-SOC2-CC7-001) is more specific than NIST in this registry. Using quarterly satisfies both.
