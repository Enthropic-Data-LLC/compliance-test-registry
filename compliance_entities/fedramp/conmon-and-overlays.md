# FedRAMP — Continuous Monitoring and Key FedRAMP Overlays

**Registry path:** `/regulation-registry/FedRAMP/ConMon-Overlays/`
**Regulation:** Federal Risk and Authorization Management Program (FedRAMP Rev 5)
**Last parsed:** 2026-05-20
**Applies to:** Cloud service providers (CSPs) offering cloud services to US federal agencies; SaaS, PaaS, and IaaS providers seeking FedRAMP Authorization to Operate (ATO)
**Trigger:** US federal agency contract or procurement requiring FedRAMP-authorized cloud services; FISMA requires federal agencies to use FedRAMP-authorized cloud offerings; federal CIO Council memo
**Jurisdiction:** United States federal government; CSPs may be located anywhere globally but must meet US federal requirements
**Not applicable to:** On-premises federal IT systems (governed by FISMA/NIST 800-53 directly without FedRAMP process); commercial-only cloud products with no federal customers; cloud services offered exclusively to state/local government (StateRAMP is the counterpart)
**Overall confidence:** HIGH for DETERMINISTIC overlays (ConMon cadences, US-CERT reporting, FIPS validation, PIV, CONUS); MEDIUM for PARAMETERIZED (ConMon plan, SCRM plan); CONTESTED for supply chain sufficiency
**Covers:** ConMon requirements (RA-5, CA-7, POA&M/CA-5, significant change CM-3), IR-6 (US-CERT), SC-13 (FIPS), IA-2(12) (PIV), PE data location, CA-2+CA-8 (3PAO + pentest)

---

## FedRAMP Authorization Pre-Condition

All tests in this file apply only to systems within the FedRAMP authorization boundary. The authorization fixture is a prerequisite:

```python
@pytest.fixture(autouse=True)
def require_fedramp_boundary(system_scope):
    if not system_scope.get("fedramp_authorization_active"):
        pytest.skip("System not in FedRAMP authorization boundary — tests informational only")
```

---

## RA-5 (FedRAMP Overlay) — Continuous Monitoring Scan Frequency (DETERMINISTIC)

### Source excerpt

> **FedRAMP RA-5 Additional Requirements:** CSPs must conduct vulnerability scanning of operating systems/infrastructure monthly, web applications annually (at minimum), and databases annually (at minimum). Results submitted to FedRAMP PMO or agency authorizing official per the ConMon plan.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | System is within FedRAMP authorization boundary | DETERMINISTIC |
| Obligation — OS/infrastructure | Vulnerability scan: monthly; all in-scope systems | DETERMINISTIC |
| Obligation — web applications | Vulnerability scan: annually (minimum) | DETERMINISTIC |
| Obligation — databases | Vulnerability scan: annually (minimum) | DETERMINISTIC |
| Evidence | `scan_records.scan_date`; `scan_records.scope` covers all boundary systems; monthly cadence for OS/infra | DETERMINISTIC |

**Assumption (ASSUME-FEDRAMP-001):** FedRAMP ConMon scanning is compliant when: (1) OS/infrastructure scans completed within the last 30 calendar days for all in-scope systems; (2) web application scans completed within the last 365 days for all boundary web applications; (3) database scans completed within the last 365 days; (4) authenticated scans used for OS/infrastructure (unauthenticated scans alone insufficient); (5) scan results include CVSS scores; (6) all findings tracked in the FedRAMP POA&M template; (7) no scan exclusions without documented agency/JAB approval.

**Overall: DETERMINISTIC → Pattern 1**

---

## CA-7 (FedRAMP Overlay) — Continuous Monitoring Plan (PARAMETERIZED)

### Source excerpt

> **FedRAMP CA-7:** CSP must implement a continuous monitoring strategy including defined metrics, frequency of monitoring, assessment of security controls, reporting to authorizing officials, and ongoing authorization.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | System is FedRAMP Moderate or High | PARAMETERIZED |
| Obligation | Written ConMon plan; defines monitoring activities, frequencies, responsible roles, reporting format | PARAMETERIZED |
| Evidence | ConMon plan document; reviewed annually; approved by authorizing official | PARAMETERIZED |

**Assumption (ASSUME-FEDRAMP-002):** ConMon plan is adequate when it: (1) identifies all monitoring activities and their frequencies (matching RA-5 overlay cadences at minimum); (2) names responsible roles (ISSO, ISSM); (3) defines reporting format and distribution (monthly ConMon report to agency/JAB); (4) documents the process for responding to identified vulnerabilities (POA&M creation trigger); (5) reviewed and updated annually or when system boundary changes significantly.

**Overall: PARAMETERIZED → Pattern 2**

---

## CA-5 (FedRAMP Overlay) — POA&M Management (DETERMINISTIC for format/cadence)

### Source excerpt

> **FedRAMP CA-5 Additional Requirements:** All open POA&M items must be tracked in the FedRAMP POA&M template. POA&M must be submitted monthly to the authorizing official. Deviation requests and false positive documentation are required for items closed without remediation.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Any open security finding from assessment, ConMon, or self-assessment | DETERMINISTIC |
| Obligation | POA&M entry created within 30 days of finding identification; submitted monthly | DETERMINISTIC |
| Obligation — items | CVSS-scored; risk-rated; scheduled completion date; milestone progress | DETERMINISTIC (format) / PARAMETERIZED (adequacy of dates) |
| Evidence | POA&M template with all required fields; last submission date ≤ 30 days | DETERMINISTIC |

**Assumption (ASSUME-FEDRAMP-003):** POA&M compliance is adequate when: (1) POA&M uses FedRAMP-provided template (not custom format); (2) all open findings from assessments and ConMon scans have POA&M entries; (3) monthly submission made to authorizing official (agency AO or JAB); (4) scheduled completion dates not exceeded without deviation request approval; (5) items closed as false positives have documented supporting evidence reviewed by ISSO; (6) critical findings (CVSS≥9.0) have scheduled remediation within 30 days.

**Overall: DETERMINISTIC for cadence/format → Pattern 1; PARAMETERIZED for deviation request adequacy → Pattern 2**

---

## CM-3 (FedRAMP Overlay) — Significant Change Notification (DETERMINISTIC)

### Source excerpt

> **FedRAMP CM-3 Additional Requirements:** CSPs must notify the authorizing official within 30 days of any significant change to the information system. FedRAMP defines significant changes as those that materially affect the security posture of the system.

### Significant change criteria (FedRAMP definition)

| Change type | Classification |
|---|---|
| New hardware added to system boundary | Significant |
| New software / services with new ports/protocols | Significant |
| New interconnections to external systems | Significant |
| Changes to cryptographic mechanisms | Significant |
| Changes to authentication mechanisms | Significant |
| Data center / cloud region changes | Significant |
| Changes to network architecture | Significant |
| Changes to access control policy | PARAMETERIZED — may or may not be significant based on scope |

**Assumption (ASSUME-FEDRAMP-004):** Significant change notification is compliant when: (1) change classification occurs at intake using FedRAMP significant change criteria; (2) notification to authorizing official within 30 calendar days of change implementation; (3) change documented with: change description, systems affected, security impact analysis, test results, and rollback plan; (4) significant changes trigger re-assessment of affected controls before or concurrent with implementation; (5) minor changes documented in the change log but do not require agency notification.

**Overall: DETERMINISTIC for 30-day notification cadence → Pattern 1; PARAMETERIZED for significance classification → Pattern 2**

---

## IR-6 (FedRAMP Overlay) — Incident Reporting to US-CERT (DETERMINISTIC — tightest threshold in registry)

### Source excerpt

> **FedRAMP IR-6 Additional Requirements:** CSPs must report incidents to the US-CERT (Cybersecurity and Infrastructure Security Agency / CISA) within one (1) hour of discovery. Incidents are also reported to the FedRAMP PMO and the relevant agency within 1 hour. US-CERT reporting uses the CISA incident reporting format.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Confirmed security incident involving systems within FedRAMP boundary | DETERMINISTIC |
| Obligation | Report to US-CERT within **1 hour** of discovery | DETERMINISTIC |
| Obligation | Report to FedRAMP PMO and agency AO within 1 hour | DETERMINISTIC |
| Evidence | `incident_records.us_cert_notification_timestamp - incident_discovery_timestamp ≤ 3600 seconds` | DETERMINISTIC |
| Note | 1-hour threshold is the tightest DETERMINISTIC gate in this entire registry (GDPR: 72h, HIPAA: 60 days) | — |

**Assumption (ASSUME-FEDRAMP-005):** Incident reporting is compliant when: (1) incident reporting procedures are documented and tested; (2) US-CERT notification occurs within 1 hour of confirming the incident — confirmed means the ISSO/SOC team has validated the event is a real incident (not a false positive); (3) initial report may be preliminary — updated reports follow as analysis progresses; (4) "incident" includes: unauthorized access, denial of service, malicious code, improper usage, and scans/probes against the system boundary; (5) all incidents tracked in incident log with: discovery time, notification time, involved systems, data affected (if any), containment/eradication/recovery actions.

**Cross-reference:** FedRAMP 1-hour US-CERT reporting and GDPR 72-hour supervisory authority reporting run in parallel for systems processing EU personal data — neither supersedes the other. Both clocks run from their respective trigger events.

**Overall: DETERMINISTIC → Pattern 1**

---

## SC-13 (FedRAMP Overlay) — FIPS 140-2/3 Cryptography (DETERMINISTIC)

### Source excerpt

> **FedRAMP SC-13:** CSPs must use cryptographic mechanisms that comply with NIST FIPS 140-2 (or 140-3) standards. All cryptography protecting federal information must use FIPS-validated modules. This applies to encryption at rest, encryption in transit, key management, and authentication.

### FIPS applicability scope

| Use case | Requirement | Classification |
|---|---|---|
| Encryption in transit (TLS) | TLS 1.2+ with FIPS-approved cipher suites | DETERMINISTIC |
| Encryption at rest | FIPS 140-2/3 validated module | DETERMINISTIC |
| Key management | FIPS-validated key derivation / wrapping | DETERMINISTIC |
| VPN / remote access | FIPS-validated IPsec or TLS | DETERMINISTIC |
| Authentication tokens | FIPS 140-2/3 validated (PIV, FIDO2 authenticator) | DETERMINISTIC |
| Hashing (integrity) | SHA-256, SHA-384, SHA-512 (not MD5 or SHA-1) | DETERMINISTIC |
| Random number generation | FIPS-approved DRBG | DETERMINISTIC |

**Assumption (ASSUME-FEDRAMP-006):** FIPS cryptographic compliance is adequate when: (1) all cryptographic modules are listed in the NIST CMVP (Cryptographic Module Validation Program) as validated for the algorithm set in use; (2) validation certificates are not expired or revoked (CMVP validation status is `Active`); (3) TLS configuration uses FIPS-approved cipher suites only (AES-256-GCM, AES-128-GCM, SHA-256/384/512); (4) MD5, RC4, DES, 3DES (TDES ≤112-bit effective), and SSL 2.0/3.0 are explicitly disabled; (5) TLS 1.0 and TLS 1.1 disabled (TLS 1.2 minimum; TLS 1.3 preferred).

**FIPS PROHIBITED cipher suites / protocols:**
```
SSL 2.0, SSL 3.0, TLS 1.0, TLS 1.1
MD5-based cipher suites
RC4 cipher suites
DES / 3DES / TDES (single DES; triple-DES only for legacy interop and only ≤112-bit effective key is prohibited)
Anonymous key exchange (DH_anon, ECDH_anon)
Export-grade cipher suites
```

**Overall: DETERMINISTIC → Pattern 1 (CMVP lookup)**

---

## IA-2(12) — PIV Credential Support (DETERMINISTIC for Moderate+)

### Source excerpt

> **FedRAMP IA-2(12):** The information system accepts and electronically verifies Personal Identity Verification (PIV) credentials from other federal agencies. Required for FedRAMP Moderate and High baselines.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | System is FedRAMP Moderate or High | DETERMINISTIC |
| Obligation | System accepts PIV credentials for authentication | DETERMINISTIC (binary: supported or not) |
| Evidence | PIV authentication tested and documented in SSP; PIV login path available in system | DETERMINISTIC |

**Assumption (ASSUME-FEDRAMP-007):** PIV support is compliant when: (1) system accepts PIV/CAC credentials from at minimum the using agency's identity management system; (2) PIV authentication tested during 3PAO assessment; (3) SSP documents PIV implementation including certificate validation and OCSP/CRL revocation checking; (4) fallback authentication (non-PIV) documented and controlled — not freely selectable by users; (5) FedRAMP Low baseline: PIV recommended but not required; Moderate/High: required.

**Overall: DETERMINISTIC → Pattern 1**

---

## PE (FedRAMP Overlay) — CONUS Data Residency (DETERMINISTIC for Moderate/High)

### Source excerpt

> **FedRAMP Data Residency Requirement:** For FedRAMP Moderate and High systems, all federal data must reside within the continental United States (CONUS) unless a specific exception is approved by the authorizing agency. Data sovereignty is verified during 3PAO assessment.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | System is FedRAMP Moderate or High; processes or stores federal data | DETERMINISTIC |
| Obligation | All federal data (at rest and in transit) located in CONUS data centers | DETERMINISTIC |
| Evidence | System architecture documentation; CSP data center locations listed in SSP; region configuration verified | DETERMINISTIC |
| Exceptions | Out-of-CONUS processing requires agency-specific written approval documented in SSP | DETERMINISTIC (existence check for exceptions) |

**Assumption (ASSUME-FEDRAMP-008):** CONUS data residency is compliant when: (1) all storage regions/availability zones hosting federal data are within the continental United States; (2) backup storage locations are also CONUS; (3) disaster recovery sites are CONUS; (4) CDN caching: federal data must not be cached in non-CONUS edge nodes (geo-restriction required or CDN excluded from CSP boundary); (5) replication: cross-region replication only to CONUS regions; (6) FedRAMP Low: CONUS preferred but exceptions may be approved without formal deviation.

**Overall: DETERMINISTIC → Pattern 1**

---

## CA-2 + CA-8 (FedRAMP Overlays) — Annual 3PAO Assessment and Penetration Testing (DETERMINISTIC)

### Source excerpt

> **FedRAMP CA-2:** CSPs must undergo annual security assessments conducted by a FedRAMP-recognized Third Party Assessment Organization (3PAO). **CA-8:** Penetration testing required annually by the 3PAO; must cover network, application, and OS layers within the authorization boundary.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | System has active FedRAMP authorization | DETERMINISTIC |
| Obligation — assessment | Annual assessment by accredited 3PAO; results in Security Assessment Report (SAR) | DETERMINISTIC |
| Obligation — pentest | Annual penetration test; network + application + OS layers | DETERMINISTIC |
| Obligation — pentest scope | All external-facing interfaces; privileged internal access paths; social engineering optional | DETERMINISTIC for scope (external + application + OS); PARAMETERIZED for methodology |
| Evidence | SAR signed by 3PAO; pentest report within last 365 days | DETERMINISTIC |

**Assumption (ASSUME-FEDRAMP-009):** 3PAO assessment and penetration testing are compliant when: (1) 3PAO is FedRAMP recognized (listed in FedRAMP marketplace); (2) SAR completed within last 12 months; (3) penetration test report within last 12 months; (4) pentest scope includes all external-facing interfaces and all privileged access paths; (5) pentest findings tracked in POA&M; (6) critical/high findings from pentest have POA&M entries with remediation dates; (7) re-testing of prior critical findings included in annual assessment.

**Overall: DETERMINISTIC → Pattern 1**

---

## SR (FedRAMP Overlay) — Supply Chain Risk Management (PARAMETERIZED/CONTESTED)

### Source excerpt

> **FedRAMP SR-1 through SR-11 (High baseline):** CSPs must develop a Supply Chain Risk Management (SCRM) plan addressing ICT supply chain risks, supplier screening, and component provenance. SCRM requirements are enhanced for the High baseline.

**Assumption (ASSUME-FEDRAMP-010):** SCRM plan is adequate when it: (1) identifies critical suppliers and components (hardware, software, cloud sub-services) within the authorization boundary; (2) includes supplier screening criteria and screening records for critical suppliers; (3) documents component provenance tracking process; (4) includes process for responding to supply chain incidents; (5) reviewed and updated annually; (6) FedRAMP High: adds enhanced supplier screening (NIST SP 800-161 reference).

**Overall: PARAMETERIZED for plan existence/content → Pattern 2; CONTESTED for supplier screening adequacy → Pattern 3**

---

## Test specifications

### YAML spec — FedRAMP ConMon and overlays

```yaml
spec_id: FEDRAMP-CONMON-001
framework: FedRAMP
baseline: Moderate  # Most common; High inherits all
pattern: 1          # Primary; Pattern 2 for PARAMETERIZED; Pattern 3 for CONTESTED
controls:
  - RA-5 (FedRAMP overlay)
  - CA-7 (FedRAMP overlay)
  - CA-5 (FedRAMP overlay)
  - CM-3 (FedRAMP overlay)
  - IR-6 (FedRAMP overlay)
  - SC-13 (FedRAMP overlay)
  - IA-2(12)
  - PE (CONUS overlay)
  - CA-2 (FedRAMP overlay)
  - CA-8 (FedRAMP overlay)
subject: FedRAMP CSP (Cloud Service Provider)
conditions:
  - system is within FedRAMP authorization boundary
  - fedramp_authorization_active == true
obligations:
  - OS/infrastructure vuln scans: monthly (≤30 days)
  - Web app scans: annually (≤365 days)
  - Database scans: annually (≤365 days)
  - POA&M: all findings tracked; submitted monthly
  - Significant changes: notified to agency within 30 days
  - Incidents: US-CERT notification within 1 hour
  - FIPS cryptography: validated modules only; approved cipher suites
  - PIV support: Moderate+ must accept PIV credentials
  - CONUS: all federal data at rest and in transit within CONUS
  - 3PAO assessment: annually
  - Penetration testing: annually; network + app + OS scope
evidence:
  - scan_records (system inventory, scan dates, scope)
  - poam (all findings, dates, CVSS scores)
  - change_records (classification, notification dates)
  - incident_records (discovery times, notification times)
  - crypto_inventory (module names, CMVP certificate numbers, status)
  - auth_config (PIV support, authentication methods)
  - infrastructure_config (region/AZ locations)
  - assessment_records (SAR date, 3PAO name, pentest date, scope)
```

### Python test file

```python
# tests/fedramp/test_fedramp_conmon.py
"""
FedRAMP Continuous Monitoring and Key Overlay Tests.

Controls: RA-5 (overlay), CA-7, CA-5, CM-3 (overlay), IR-6 (overlay),
          SC-13, IA-2(12), PE (CONUS), CA-2, CA-8
Framework: FedRAMP Rev 5 (Moderate baseline — also applies to High)
Assumptions: ASSUME-FEDRAMP-001 through ASSUME-FEDRAMP-010
"""
import pytest
from datetime import datetime, timedelta, timezone
from typing import Any

FEDRAMP_BOUNDARY_FIXTURE = "fedramp_authorization_active"

OS_INFRA_SCAN_MAX_DAYS = 30
WEB_APP_SCAN_MAX_DAYS = 365
DATABASE_SCAN_MAX_DAYS = 365
POAM_SUBMISSION_MAX_DAYS = 30
SIGNIFICANT_CHANGE_NOTIFY_MAX_DAYS = 30
USCERT_NOTIFY_MAX_SECONDS = 3600  # 1 hour
ANNUAL_ASSESSMENT_MAX_DAYS = 365
PENTEST_MAX_DAYS = 365
CRITICAL_VULN_REMEDIATION_DAYS = 30
CRITICAL_CVSS_THRESHOLD = 9.0

FIPS_PROHIBITED_PROTOCOLS = {"ssl_2_0", "ssl_3_0", "tls_1_0", "tls_1_1"}
FIPS_PROHIBITED_CIPHERS = {
    "rc4", "des", "3des_56", "export_grade", "anon_dh", "anon_ecdh",
    "md5_mac", "null_cipher",
}
FIPS_REQUIRED_MIN_TLS = "tls_1_2"


@pytest.fixture(autouse=True)
def require_fedramp_boundary(system_scope: dict[str, Any]):
    """Gate: skip all tests unless system is in FedRAMP authorization boundary."""
    if not system_scope.get("fedramp_authorization_active"):
        pytest.skip("System not in FedRAMP authorization boundary — tests informational only")


# ── RA-5 FedRAMP Overlay: Vulnerability Scan Cadence ─────────────────────────

@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-001",
    description="OS/infrastructure scans: monthly (≤30 days); authenticated scans required",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_os_infrastructure_scans_within_30_days(scan_records: dict[str, Any]):
    """RA-5 FedRAMP overlay: OS/infra vulnerability scans must be completed monthly."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=OS_INFRA_SCAN_MAX_DAYS)

    last_os_scan = scan_records.get("os_infrastructure_last_scan_date")
    assert last_os_scan is not None, "No OS/infrastructure scan record found"
    assert last_os_scan >= cutoff, (
        f"OS/infrastructure scan overdue: last scan {last_os_scan.date()}, "
        f"required within {OS_INFRA_SCAN_MAX_DAYS} days"
    )

    # Authenticated scans required (unauthenticated alone insufficient)
    assert scan_records.get("os_infrastructure_authenticated_scan"), (
        "OS/infrastructure scans must use authenticated scanning — unauthenticated alone is insufficient"
    )


@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-001",
    description="Web application scans: annually (≤365 days)",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_web_application_scans_within_365_days(scan_records: dict[str, Any]):
    """RA-5 FedRAMP overlay: Web application scans must be completed annually."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=WEB_APP_SCAN_MAX_DAYS)

    last_web_scan = scan_records.get("web_application_last_scan_date")
    assert last_web_scan is not None, "No web application scan record found"
    assert last_web_scan >= cutoff, (
        f"Web application scan overdue: last scan {last_web_scan.date()}, "
        f"required within {WEB_APP_SCAN_MAX_DAYS} days"
    )


@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-001",
    description="All in-scope systems appear in scan results — no exclusions without approval",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_all_boundary_systems_in_scan_scope(
    scan_records: dict[str, Any],
    system_inventory: list[dict[str, Any]],
):
    """RA-5 FedRAMP overlay: Every in-boundary system must appear in latest scan."""
    scanned_systems = set(scan_records.get("scanned_system_ids", []))
    approved_exclusions = set(scan_records.get("agency_approved_exclusion_ids", []))

    for system in system_inventory:
        sys_id = system["system_id"]
        if sys_id in approved_exclusions:
            continue
        assert sys_id in scanned_systems, (
            f"System {sys_id!r} ({system.get('hostname', 'unknown')}) is in the FedRAMP boundary "
            f"but not included in last vulnerability scan — add to scan scope or obtain agency exclusion approval"
        )


# ── CA-5 FedRAMP Overlay: POA&M Management ──────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-003",
    description="POA&M submitted monthly; all findings tracked; CVSS-rated; completion dates set",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_poam_submitted_within_last_30_days(poam: dict[str, Any]):
    """CA-5 FedRAMP overlay: POA&M must be submitted to authorizing official monthly."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=POAM_SUBMISSION_MAX_DAYS)

    last_submission = poam.get("last_submission_date")
    assert last_submission is not None, "No POA&M submission record found"
    assert last_submission >= cutoff, (
        f"POA&M submission overdue: last submitted {last_submission.date()}, "
        f"must submit within {POAM_SUBMISSION_MAX_DAYS} days"
    )


@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-003",
    description="Critical findings (CVSS≥9.0) scheduled for remediation within 30 days",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_critical_poam_items_have_timely_remediation(poam: dict[str, Any]):
    """CA-5 FedRAMP overlay: Critical findings in POA&M must have ≤30-day scheduled remediation."""
    now = datetime.now(timezone.utc)
    items = poam.get("items", [])

    overdue = []
    for item in items:
        if item.get("cvss_score", 0.0) < CRITICAL_CVSS_THRESHOLD:
            continue
        scheduled = item.get("scheduled_completion_date")
        if scheduled is None or scheduled > now + timedelta(days=CRITICAL_VULN_REMEDIATION_DAYS):
            overdue.append(item["finding_id"])

    assert not overdue, (
        f"Critical POA&M items (CVSS≥{CRITICAL_CVSS_THRESHOLD}) must have scheduled remediation "
        f"within {CRITICAL_VULN_REMEDIATION_DAYS} days: {overdue}"
    )


@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-003",
    description="No POA&M items past their scheduled completion date without deviation request",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_no_overdue_poam_items_without_deviation(poam: dict[str, Any]):
    """CA-5 FedRAMP overlay: Overdue POA&M items must have agency-approved deviation request."""
    now = datetime.now(timezone.utc)
    items = poam.get("items", [])

    unexcused = []
    for item in items:
        scheduled = item.get("scheduled_completion_date")
        has_deviation = item.get("deviation_request_approved", False)
        if scheduled and scheduled < now and not has_deviation:
            unexcused.append(item["finding_id"])

    assert not unexcused, (
        f"POA&M items are past scheduled completion date without approved deviation request: {unexcused}"
    )


# ── CM-3 FedRAMP Overlay: Significant Change Notification ───────────────────

@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-004",
    description="Significant changes notified to agency AO within 30 calendar days",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_significant_changes_notified_within_30_days(change_records: list[dict[str, Any]]):
    """CM-3 FedRAMP overlay: Significant changes must be reported to agency within 30 days."""
    late_notifications = []

    for change in change_records:
        if not change.get("classified_as_significant"):
            continue
        implementation_date = change.get("implementation_date")
        notification_date = change.get("agency_notification_date")

        if implementation_date is None:
            continue
        if notification_date is None:
            late_notifications.append(
                f"{change['change_id']}: significant change not yet notified to agency"
            )
        else:
            days_elapsed = (notification_date - implementation_date).days
            if days_elapsed > SIGNIFICANT_CHANGE_NOTIFY_MAX_DAYS:
                late_notifications.append(
                    f"{change['change_id']}: notified {days_elapsed} days after implementation "
                    f"(max {SIGNIFICANT_CHANGE_NOTIFY_MAX_DAYS})"
                )

    assert not late_notifications, (
        f"Significant changes not notified within {SIGNIFICANT_CHANGE_NOTIFY_MAX_DAYS} days: "
        f"{late_notifications}"
    )


# ── IR-6 FedRAMP Overlay: US-CERT Incident Reporting ────────────────────────

@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-005",
    description="Confirmed incidents reported to US-CERT within 1 hour of discovery",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_incidents_reported_to_uscert_within_1_hour(incident_records: list[dict[str, Any]]):
    """IR-6 FedRAMP overlay: Incidents must be reported to US-CERT within 1 hour of confirmation."""
    late_reports = []

    for incident in incident_records:
        if not incident.get("confirmed_incident"):
            continue  # Unconfirmed events (false positives) do not require US-CERT report

        discovery_ts = incident.get("discovery_timestamp")
        uscert_notify_ts = incident.get("uscert_notification_timestamp")

        if discovery_ts is None:
            continue
        if uscert_notify_ts is None:
            late_reports.append(f"{incident['incident_id']}: no US-CERT notification recorded")
        else:
            elapsed = (uscert_notify_ts - discovery_ts).total_seconds()
            if elapsed > USCERT_NOTIFY_MAX_SECONDS:
                elapsed_minutes = elapsed / 60
                late_reports.append(
                    f"{incident['incident_id']}: US-CERT notified {elapsed_minutes:.1f} min after discovery "
                    f"(max {USCERT_NOTIFY_MAX_SECONDS / 60:.0f} min)"
                )

    assert not late_reports, (
        f"Incidents not reported to US-CERT within {USCERT_NOTIFY_MAX_SECONDS / 3600:.0f} hour: "
        f"{late_reports}"
    )


def test_incident_response_procedures_documented(security_policies: dict[str, Any]):
    """IR-6 FedRAMP overlay: Incident response procedures must be documented and include US-CERT contact."""
    irp = security_policies.get("incident_response_plan")
    assert irp is not None, "Incident Response Plan (IRP) not found in security policies"

    assert irp.get("uscert_reporting_procedure_included"), (
        "IRP must include documented US-CERT reporting procedure"
    )
    assert irp.get("reporting_thresholds_defined"), (
        "IRP must define incident classification thresholds that trigger US-CERT reporting"
    )
    assert irp.get("agency_notification_procedure_included"), (
        "IRP must include agency AO notification procedure"
    )


# ── SC-13 FedRAMP Overlay: FIPS 140-2/3 Cryptography ────────────────────────

@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-006",
    description="All cryptographic modules FIPS 140-2/3 validated (CMVP active); no prohibited protocols",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_fips_validated_crypto_modules(crypto_inventory: list[dict[str, Any]]):
    """SC-13 FedRAMP overlay: All cryptographic modules must have active FIPS 140-2/3 validation."""
    invalid_modules = []

    for module in crypto_inventory:
        cmvp_status = module.get("cmvp_status", "").lower()
        cert_number = module.get("cmvp_certificate_number")

        if cmvp_status != "active":
            invalid_modules.append(
                f"{module['module_name']}: CMVP status={cmvp_status!r} "
                f"(cert #{cert_number}) — must be Active"
            )

    assert not invalid_modules, (
        f"Cryptographic modules without active FIPS validation: {invalid_modules}"
    )


@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-006",
    description="FIPS-prohibited TLS protocols and cipher suites disabled",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_fips_prohibited_protocols_disabled(tls_config: dict[str, Any]):
    """SC-13 FedRAMP overlay: Prohibited TLS protocols and cipher suites must be disabled."""
    enabled_protocols = {p.lower() for p in tls_config.get("enabled_protocols", [])}
    enabled_ciphers = {c.lower() for c in tls_config.get("enabled_ciphers", [])}

    prohibited_protocols_found = enabled_protocols & FIPS_PROHIBITED_PROTOCOLS
    prohibited_ciphers_found = enabled_ciphers & FIPS_PROHIBITED_CIPHERS

    assert not prohibited_protocols_found, (
        f"FIPS-prohibited TLS protocols enabled: {prohibited_protocols_found}"
    )
    assert not prohibited_ciphers_found, (
        f"FIPS-prohibited cipher suites enabled: {prohibited_ciphers_found}"
    )


# ── IA-2(12): PIV Credential Support ────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-007",
    description="Moderate/High baseline: system accepts and validates PIV credentials",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_piv_credential_support(auth_config: dict[str, Any], system_scope: dict[str, Any]):
    """IA-2(12): FedRAMP Moderate/High must accept PIV credentials."""
    baseline = system_scope.get("fedramp_baseline", "low").lower()
    if baseline == "low":
        pytest.skip("PIV support required for Moderate/High only — Low baseline informational")

    assert auth_config.get("piv_authentication_supported"), (
        f"FedRAMP {baseline.capitalize()} baseline requires PIV credential support (IA-2(12))"
    )
    assert auth_config.get("piv_ocsp_crl_revocation_checking"), (
        "PIV implementation must include OCSP or CRL revocation checking"
    )


# ── PE FedRAMP Overlay: CONUS Data Residency ────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-008",
    description="All federal data at rest and in transit resides in CONUS for Moderate/High",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_federal_data_resides_in_conus(
    infrastructure_config: dict[str, Any],
    system_scope: dict[str, Any],
):
    """PE FedRAMP overlay: Moderate/High federal data must reside in CONUS."""
    baseline = system_scope.get("fedramp_baseline", "low").lower()
    if baseline == "low":
        pytest.skip("CONUS requirement applies to Moderate/High — Low baseline informational")

    storage_regions = infrastructure_config.get("storage_regions", [])
    backup_regions = infrastructure_config.get("backup_regions", [])
    all_regions = storage_regions + backup_regions

    non_conus = [r for r in all_regions if not r.get("is_conus")]
    approved_exceptions = [r for r in non_conus if r.get("agency_conus_exception_approved")]
    unapproved = [r for r in non_conus if not r.get("agency_conus_exception_approved")]

    assert not unapproved, (
        f"Federal data regions outside CONUS without agency approval: "
        f"{[r['region_id'] for r in unapproved]}"
    )

    if approved_exceptions:
        pytest.warns(
            UserWarning,
            match="Non-CONUS data residency approved",
        )


# ── CA-2 + CA-8: Annual 3PAO Assessment and Penetration Testing ─────────────

@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-009",
    description="3PAO annual assessment completed within last 365 days by recognized 3PAO",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_annual_3pao_assessment_current(assessment_records: dict[str, Any]):
    """CA-2 FedRAMP overlay: Annual 3PAO security assessment must be within last 365 days."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=ANNUAL_ASSESSMENT_MAX_DAYS)

    last_assessment = assessment_records.get("last_3pao_assessment_date")
    assert last_assessment is not None, "No 3PAO security assessment record found"
    assert last_assessment >= cutoff, (
        f"3PAO annual assessment overdue: last assessment {last_assessment.date()}, "
        f"required within {ANNUAL_ASSESSMENT_MAX_DAYS} days"
    )

    # 3PAO must be FedRAMP-recognized
    assert assessment_records.get("assessor_fedramp_recognized"), (
        "Security assessment must be performed by a FedRAMP-recognized 3PAO"
    )


@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-009",
    description="Annual penetration test completed within last 365 days; scope: network + app + OS",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_annual_penetration_test_current(assessment_records: dict[str, Any]):
    """CA-8 FedRAMP overlay: Annual penetration test must be within last 365 days."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=PENTEST_MAX_DAYS)

    last_pentest = assessment_records.get("last_pentest_date")
    assert last_pentest is not None, "No penetration test record found"
    assert last_pentest >= cutoff, (
        f"Annual penetration test overdue: last pentest {last_pentest.date()}, "
        f"required within {PENTEST_MAX_DAYS} days"
    )

    pentest_scope = set(assessment_records.get("pentest_scope_layers", []))
    required_scope = {"network", "application", "os"}
    missing_scope = required_scope - pentest_scope
    assert not missing_scope, (
        f"Penetration test missing required scope layers: {missing_scope} "
        f"(required: network, application, OS)"
    )


# ── SR FedRAMP Overlay: SCRM Plan ───────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-010",
    description="SCRM plan exists, covers critical suppliers, reviewed annually",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_scrm_plan_exists_and_current(security_policies: dict[str, Any]):
    """SR FedRAMP overlay: Supply Chain Risk Management plan required."""
    scrm_plan = security_policies.get("scrm_plan")
    assert scrm_plan is not None, "Supply Chain Risk Management (SCRM) plan not found"

    now = datetime.now(timezone.utc)
    last_review = scrm_plan.get("last_review_date")
    assert last_review is not None, "SCRM plan has no review date"
    assert last_review >= now - timedelta(days=365), (
        f"SCRM plan not reviewed within last year: last review {last_review.date()}"
    )


@pytest.mark.human_review_required(
    reason=(
        "SCRM supplier screening adequacy is a judgment call — whether supplier vetting depth "
        "is sufficient for FedRAMP High is an assessor-evaluated determination. "
        "Action: 3PAO review of SCRM plan against NIST SP 800-161 criteria required."
    )
)
@pytest.mark.assumption(
    id="ASSUME-FEDRAMP-010",
    description="Critical supplier screening adequacy requires human review",
    approved_by="ISSO",
    review_date="2027-05-20",
)
def test_critical_supplier_screening_adequacy_reviewed(security_policies: dict[str, Any]):
    """SR FedRAMP overlay (High): Critical supplier screening adequacy requires 3PAO/human review."""
    scrm_plan = security_policies.get("scrm_plan")
    assert scrm_plan is not None, "SCRM plan required for supplier screening review"

    # Surface the state for human review
    critical_suppliers = scrm_plan.get("critical_suppliers_identified", False)
    screening_criteria_documented = scrm_plan.get("supplier_screening_criteria_documented", False)
    screening_records_current = scrm_plan.get("supplier_screening_records_current", False)

    assert critical_suppliers, "SCRM plan must identify critical ICT suppliers and components"
    assert screening_criteria_documented, (
        "SCRM plan must document supplier screening criteria — requires human review for adequacy"
    )
    assert screening_records_current, (
        "Supplier screening records must be current — adequacy is 3PAO/assessor-evaluated"
    )
```

---

## Open assumption registry (this file)

| ID | Control | Summary | Review date |
|---|---|---|---|
| ASSUME-FEDRAMP-001 | RA-5 overlay | OS/infra scans: monthly (≤30 days); authenticated; web app/DB: annually; all boundary systems in scope; no unapproved exclusions | 2026-05-20 |
| ASSUME-FEDRAMP-002 | CA-7 | ConMon plan: monitoring activities and frequencies; responsible roles; reporting format; POA&M creation triggers; reviewed annually | 2026-05-20 |
| ASSUME-FEDRAMP-003 | CA-5 overlay | POA&M: FedRAMP template; all findings tracked; monthly submission; critical (CVSS≥9.0) remediation ≤30 days; no overdue items without approved deviation | 2026-05-20 |
| ASSUME-FEDRAMP-004 | CM-3 overlay | Significant change: notify agency AO ≤30 days; classification at intake; security impact analysis; affects control re-assessment | 2026-05-20 |
| ASSUME-FEDRAMP-005 | IR-6 overlay | US-CERT: ≤1 hour from confirmed incident discovery; FedRAMP PMO and agency AO also notified; incident log with timestamps; all confirmed incident types | 2026-05-20 |
| ASSUME-FEDRAMP-006 | SC-13 overlay | FIPS: all crypto modules CMVP-active; prohibited protocols (SSL/TLS≤1.1) and ciphers (RC4, DES, MD5-MAC) disabled; TLS 1.2 minimum | 2026-05-20 |
| ASSUME-FEDRAMP-007 | IA-2(12) | PIV: Moderate/High must accept PIV; OCSP/CRL revocation checked; fallback auth documented | 2026-05-20 |
| ASSUME-FEDRAMP-008 | PE CONUS overlay | CONUS: Moderate/High all storage + backup regions within CONUS; CDN must geo-restrict; exceptions require agency written approval in SSP | 2026-05-20 |
| ASSUME-FEDRAMP-009 | CA-2 + CA-8 | 3PAO: FedRAMP-recognized; SAR ≤365 days; pentest ≤365 days; scope: network + application + OS; prior findings re-tested | 2026-05-20 |
| ASSUME-FEDRAMP-010 | SR SCRM overlay | SCRM: critical suppliers identified; screening criteria documented; records current; reviewed annually; High adds NIST 800-161 enhanced screening | 2026-05-20 |
