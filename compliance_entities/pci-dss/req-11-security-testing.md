# Requirement 11 — Test Security of Systems and Networks Regularly

**Registry path:** `/regulation-registry/PCI-DSS/Req-11/`
**Version:** PCI DSS v4.0 (mandatory since March 31, 2025)
**Last parsed:** 2026-05-20
**Applies to:** Any organization that stores, processes, or transmits payment card data — merchants of all levels, payment processors, acquirers, issuers, and service providers in the card payment ecosystem
**Trigger:** Participation in the card payment ecosystem; card brand contracts (Visa, Mastercard, Amex, Discover, UnionPay); acquiring bank contractual requirement; SAQ level determined by annual transaction volume
**Jurisdiction:** Global — enforced by card brands (Visa/Mastercard/Amex/Discover) and acquiring banks; no geographic restriction
**Not applicable to:** Organizations that never handle cardholder data and fully outsource all card processing to a PCI-DSS-compliant third party; SAQ A merchants processing only redirected card transactions
**Overall confidence:** HIGH — scan and test cadences are DETERMINISTIC; scope adequacy is PARAMETERIZED
**R = Required**

---

## Scope summary

Req 11 mandates a continuous testing posture: quarterly vulnerability scans (internal and external), annual penetration tests, weekly file integrity checks, and intrusion detection. All primary cadence thresholds are DETERMINISTIC. The only PARAMETERIZED surface is penetration test scope adequacy — the regulation requires testing at network and application layers but does not define exactly how deep the application testing must go.

v4.0 added Req 11.6.1 (payment page script monitoring) as a new DETERMINISTIC requirement.

---

## 11.3.1 — Internal Vulnerability Scans (R — DETERMINISTIC)

### Source excerpt

> *11.3.1 — Internal vulnerability scans are performed as follows: At least once every three months. High-risk and critical vulnerabilities are resolved. Rescans are performed to confirm that all high-risk and critical vulnerabilities are resolved as defined in the entity's targeted risk analysis, or as defined in Requirement 6.3.1. Scan tool is kept up to date with the latest vulnerability information. After significant changes.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All CDE system components | DETERMINISTIC |
| Condition | Quarterly calendar interval; after significant changes | DETERMINISTIC |
| Obligation | Internal scan completed ≤ 90 days since last; high/critical vulnerabilities remediated; rescan confirms remediation; tool updated | DETERMINISTIC |
| Evidence | `vuln_scan_records.scan_date`; `scan_type == "internal"`; `high_critical_open_count == 0` after rescan | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 11.3.2 — External Vulnerability Scans (R — DETERMINISTIC)

### Source excerpt

> *11.3.2 — External vulnerability scans are performed as follows: At least once every three months. By a PCI SSC Approved Scanning Vendor (ASV). Passing scan results achieved. After significant changes.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All external-facing CDE IP addresses and domains | DETERMINISTIC |
| Condition | Quarterly calendar interval; after significant changes | DETERMINISTIC |
| Obligation | External ASV scan ≤ 90 days; scan result is "Pass"; ASV is on PCI SSC approved list | DETERMINISTIC |
| Evidence | `asv_scan_records.scan_date`; `scan_result == "Pass"`; `scanner_is_approved_asv == true` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 11.4 — Penetration Testing (R — DETERMINISTIC for cadence; PARAMETERIZED for scope)

### Source excerpt

> *11.4.3 — External penetration testing is performed: At least once every 12 months. After any significant upgrade or modification. By a qualified internal resource or qualified third party.*
> *11.4.4 — Exploitable vulnerabilities and security weaknesses found during penetration testing are corrected, and testing is repeated to verify corrections.*
> *11.4.5 — If segmentation is used to isolate the CDE, penetration tests are performed on segmentation controls at least once every 12 months (or every 6 months for service providers).*

### Element extraction — cadence

| Element | Value | Classification |
|---|---|---|
| Subject | CDE perimeter — network and application layers | DETERMINISTIC |
| Condition | Annual calendar interval; after significant changes | DETERMINISTIC |
| Obligation | Internal and external pentest ≤ 365 days; segmentation test ≤ 365 days (≤ 180 for service providers); findings remediated | DETERMINISTIC |
| Evidence | `pentest_records.test_date`; `test_type`; `findings_remediated == true` | DETERMINISTIC |

### Element extraction — scope adequacy

| Element | Value | Classification |
|---|---|---|
| Obligation | Pentest includes network layer and application layer; covers the entire CDE perimeter | PARAMETERIZED |
| Evidence | Pentest scope document reviewed for network and application coverage; confirmation of methodology by qualified tester | PARAMETERIZED |

**Assumption (ASSUME-11-001):** Penetration test scope is adequate when it includes: (1) all CDE-connected network segments and perimeter controls; (2) all externally exposed CDE application components including web application layer testing (OWASP Top 10 coverage); (3) internal network segments within the CDE; (4) segmentation validation confirming out-of-scope systems cannot reach CHD. "Qualified" means OSCP, CEH, GPEN, or demonstrated equivalent experience documented in the pentest report.

**Overall: DETERMINISTIC for cadence → Pattern 1; PARAMETERIZED for scope → Pattern 2**

---

## 11.5.2 — File Integrity Monitoring (R — DETERMINISTIC)

### Source excerpt

> *11.5.2 — A change-detection mechanism (for example, file integrity monitoring tools) is deployed as follows: To alert personnel to unauthorized modification of critical files. To perform critical file comparisons at least once weekly.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | Critical files on CDE systems | DETERMINISTIC |
| Condition | CDE system component is in scope | DETERMINISTIC |
| Obligation | FIM deployed; critical file comparison ≤ 7 days; alerts configured; unauthorized modification triggers alert | DETERMINISTIC |
| Evidence | `fim_config.deployed == true`; `fim_config.comparison_interval_days <= 7`; `fim_config.alert_on_change == true` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 11.6.1 — Payment Page Script Monitoring (R — DETERMINISTIC) [NEW IN v4.0]

### Source excerpt

> *11.6.1 — A change- and tamper-detection mechanism is deployed to alert personnel to unauthorized modification of the payment page as follows: The mechanism is configured to evaluate the HTTP headers and the contents of the payment page received by the consumer browser. The mechanism functions are performed as follows: At least once every seven days; OR Periodically at a frequency defined in the entity's targeted risk analysis.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | Consumer-facing payment page(s) | DETERMINISTIC |
| Condition | Organization hosts or controls a payment page | DETERMINISTIC |
| Obligation | Script/content monitoring deployed for payment page; evaluates HTTP headers and page content as received by browser; alerts on change; ≤ 7 days between checks (or risk-analysis interval) | DETERMINISTIC |
| Evidence | `payment_page_monitoring.deployed == true`; `check_interval_days <= 7`; `monitors_http_headers == true` and `monitors_page_content == true` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## YAML specifications

### `req11_vuln_scans.yaml`

```yaml
regulation_id: PCI-DSS-v4.0-11.3.1-11.3.2
section: "PCI DSS v4.0 — Vulnerability Scanning Cadence"
r_or_a: Required
source_text: >
  Internal scans: at least once every three months; high/critical resolved;
  rescans confirm remediation. External scans: at least once every three months;
  by ASV; passing results required.

extracted_elements:
  subject: "All CDE system components (internal) and external IPs/domains (external)"
  condition: "Quarterly calendar interval; after significant changes"
  obligation: "Scan completed ≤ 90 days; findings remediated; ASV used for external"
  evidence: "vuln_scan_records: scan_date, scan_type, result, open_high_critical_count"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log: []
test_confidence: HIGH
generated_test: "tests/req11/test_11_3_vulnerability_scans.py"
```

---

## Generated tests

### `tests/req11/test_11_3_vulnerability_scans.py`

```python
"""
PCI DSS v4.0 Req 11.3 — Vulnerability Scanning
Confidence: HIGH | Human Review: NOT REQUIRED
"""
from datetime import date

QUARTERLY_MAX_DAYS = 90


def test_internal_vulnerability_scan_within_90_days(vuln_scan_records):
    """11.3.1 — Internal scan must be performed at least quarterly."""
    today = date.today()
    internal_scans = [r for r in vuln_scan_records if r.get("scan_type") == "internal"]
    if not internal_scans:
        assert False, "VIOLATION (11.3.1): No internal vulnerability scan records found"
    latest = max(internal_scans, key=lambda r: r["scan_date"])
    days_since = (today - latest["scan_date"]).days
    assert days_since <= QUARTERLY_MAX_DAYS, (
        f"VIOLATION (11.3.1): Last internal scan was {days_since} days ago "
        f"(max {QUARTERLY_MAX_DAYS})"
    )


def test_external_asv_scan_within_90_days(vuln_scan_records):
    """11.3.2 — External ASV scan must be performed at least quarterly."""
    today = date.today()
    asv_scans = [
        r for r in vuln_scan_records
        if r.get("scan_type") == "external" and r.get("scanner_is_approved_asv")
    ]
    if not asv_scans:
        assert False, (
            "VIOLATION (11.3.2): No external ASV scan records found — "
            "quarterly external scanning by an approved ASV is required"
        )
    latest = max(asv_scans, key=lambda r: r["scan_date"])
    days_since = (today - latest["scan_date"]).days
    assert days_since <= QUARTERLY_MAX_DAYS, (
        f"VIOLATION (11.3.2): Last external ASV scan was {days_since} days ago "
        f"(max {QUARTERLY_MAX_DAYS})"
    )


def test_latest_external_scan_is_passing(vuln_scan_records):
    """11.3.2 — Most recent external ASV scan result must be 'Pass'."""
    asv_scans = [
        r for r in vuln_scan_records
        if r.get("scan_type") == "external" and r.get("scanner_is_approved_asv")
    ]
    if not asv_scans:
        return
    latest = max(asv_scans, key=lambda r: r["scan_date"])
    assert latest.get("scan_result") == "Pass", (
        f"VIOLATION (11.3.2): Most recent ASV scan from {latest['scan_date']} "
        f"did not achieve a passing result — result: {latest.get('scan_result')}"
    )


def test_no_open_high_critical_vulnerabilities(vuln_scan_records):
    """11.3.1.1 — All high-risk and critical vulnerabilities must be remediated."""
    internal_scans = [r for r in vuln_scan_records if r.get("scan_type") == "internal"]
    if not internal_scans:
        return
    latest = max(internal_scans, key=lambda r: r["scan_date"])
    open_count = latest.get("open_high_critical_count", 0)
    assert open_count == 0, (
        f"VIOLATION (11.3.1.1): {open_count} high/critical vulnerability/vulnerabilities "
        f"unresolved from internal scan on {latest['scan_date']}"
    )
```

### `tests/req11/test_11_4_penetration_testing.py`

```python
"""
PCI DSS v4.0 Req 11.4 — Penetration Testing
Confidence: HIGH for cadence; MEDIUM for scope adequacy
"""
import pytest
from datetime import date

ANNUAL_MAX_DAYS = 365
SEGMENTATION_TEST_MAX_DAYS_MERCHANT = 365
SEGMENTATION_TEST_MAX_DAYS_SERVICE_PROVIDER = 180


def test_penetration_test_within_12_months(pentest_records):
    """11.4.3 — Penetration test must be performed at least annually."""
    today = date.today()
    if not pentest_records:
        assert False, "VIOLATION (11.4.3): No penetration test records found"
    latest = max(pentest_records, key=lambda r: r["test_date"])
    days_since = (today - latest["test_date"]).days
    assert days_since <= ANNUAL_MAX_DAYS, (
        f"VIOLATION (11.4.3): Last penetration test was {days_since} days ago "
        f"(max {ANNUAL_MAX_DAYS})"
    )


def test_pentest_findings_remediated(pentest_records):
    """11.4.4 — All exploitable findings from pentest must be corrected and verified."""
    violations = [
        r for r in pentest_records
        if r.get("exploitable_findings_open", 0) > 0
    ]
    assert not violations, (
        f"VIOLATION (11.4.4): {len(violations)} pentest report(s) with unresolved "
        f"exploitable findings: "
        f"{[(r['pentest_id'], r.get('exploitable_findings_open')) for r in violations]}"
    )


def test_segmentation_test_within_required_interval(segmentation_test_records, entity_config):
    """11.4.5 — Segmentation controls tested annually (or 6-monthly for service providers)."""
    if not segmentation_test_records:
        return  # segmentation not used; skip
    today = date.today()
    is_service_provider = entity_config.get("is_service_provider", False)
    max_days = (
        SEGMENTATION_TEST_MAX_DAYS_SERVICE_PROVIDER
        if is_service_provider
        else SEGMENTATION_TEST_MAX_DAYS_MERCHANT
    )
    latest = max(segmentation_test_records, key=lambda r: r["test_date"])
    days_since = (today - latest["test_date"]).days
    assert days_since <= max_days, (
        f"VIOLATION (11.4.5): Last segmentation test was {days_since} days ago "
        f"(max {max_days} for {'service provider' if is_service_provider else 'merchant'})"
    )


@pytest.mark.assumption(
    id="ASSUME-11-001",
    description=(
        "Pentest scope adequate: CDE network + application layer (OWASP Top 10); "
        "segmentation validation included. Qualified = OSCP/CEH/GPEN or documented equivalent."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_pentest_scope_is_adequate(pentest_records):
    if not pentest_records:
        return
    latest = max(pentest_records, key=lambda r: r["test_date"])
    violations = []
    if not latest.get("network_layer_tested"):
        violations.append("Network layer not included in scope")
    if not latest.get("application_layer_tested"):
        violations.append("Application layer not included in scope")
    if not latest.get("tester_qualified"):
        violations.append("Tester qualification not documented")
    assert not violations, (
        f"VIOLATION (11.4.3) — Pentest scope deficiencies in most recent test "
        f"({latest['pentest_id']}): {violations}"
    )
```

### `tests/req11/test_11_5_integrity_monitoring.py`

```python
"""
PCI DSS v4.0 Req 11.5 — File Integrity Monitoring and Payment Page Monitoring
Confidence: HIGH | Human Review: NOT REQUIRED
"""
from datetime import date

FIM_MAX_INTERVAL_DAYS = 7
PAYMENT_PAGE_MAX_CHECK_DAYS = 7


def test_fim_deployed_on_cde_systems(cde_system_configs):
    """11.5.2 — FIM must be deployed on all CDE system components."""
    violations = [
        s for s in cde_system_configs
        if s.get("in_cde") and not s.get("fim_deployed")
    ]
    assert not violations, (
        f"VIOLATION (11.5.2): {len(violations)} CDE system(s) without FIM: "
        f"{[s['system_id'] for s in violations]}"
    )


def test_fim_comparison_interval_weekly(fim_configs):
    violations = [
        c for c in fim_configs
        if c.get("comparison_interval_days", 9999) > FIM_MAX_INTERVAL_DAYS
    ]
    assert not violations, (
        f"VIOLATION (11.5.2): {len(violations)} FIM configuration(s) with comparison "
        f"interval > 7 days: "
        f"{[(c['system_id'], c.get('comparison_interval_days')) for c in violations]}"
    )


def test_payment_page_monitoring_deployed(payment_page_configs):
    """11.6.1 — Payment page change-detection mechanism must be deployed."""
    violations = [
        p for p in payment_page_configs
        if not p.get("monitoring_deployed")
    ]
    assert not violations, (
        f"VIOLATION (11.6.1): {len(violations)} payment page(s) without "
        f"change-detection monitoring: {[p['page_id'] for p in violations]}"
    )


def test_payment_page_monitoring_covers_headers_and_content(payment_page_configs):
    """11.6.1 — Monitoring must cover HTTP headers AND page content."""
    violations = [
        p for p in payment_page_configs
        if p.get("monitoring_deployed")
        and (
            not p.get("monitors_http_headers")
            or not p.get("monitors_page_content")
        )
    ]
    assert not violations, (
        f"VIOLATION (11.6.1): {len(violations)} payment page monitoring configuration(s) "
        f"not covering both HTTP headers and page content: "
        f"{[p['page_id'] for p in violations]}"
    )
```

---

## Notes for the registry

- **ASV requirement for external scans:** Any external-facing CDE IP address must be scanned by a PCI SSC Approved Scanning Vendor — not just any vulnerability scanner. The ASV list is maintained at pcisecuritystandards.org. Using an internal tool or a non-ASV vendor for external scans does not satisfy 11.3.2.
- **Quarterly cadence means calendar quarters, not rolling 90 days:** While the 90-day threshold is testable and practical, the PCI SSC guidance suggests quarterly scans should be performed in each calendar quarter (Q1–Q4). Confirm timing with your QSA.
- **Pentest qualifications:** PCI DSS does not mandate specific certifications but does require "qualified." OSCP, CEH, GPEN, or CREST CRT are commonly cited. The most important factor is that the methodology and tester qualifications are documented in the pentest report — undocumented credentials are treated as unqualified by many QSAs.
- **11.6.1 is new in v4.0 (payment page monitoring):** This requirement targets supply-chain/skimming attacks (Magecart-style). If the organization does not directly control the payment page (e.g., it uses an embedded iframe from a payment provider), the obligation shifts to ensuring the third-party provider has equivalent monitoring in place under the BAA-equivalent agreement.
- **FIM critical file definitions:** "Critical files" are not defined exhaustively in PCI DSS. Typically includes: OS kernel and binaries, configuration files, authentication/authorization files, audit log configuration, web server configuration and application files. FIM tools (Tripwire, AIDE, Wazuh) typically have pre-built profiles; confirm the profile covers web application files in the CDE.
