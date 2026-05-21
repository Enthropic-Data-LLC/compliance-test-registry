# NY DFS 23 NYCRR 500 — Cybersecurity Program Specification

**Spec file:** `cybersecurity-program.md`
**Registry version:** 2026.05
**Last updated:** 2026-05-21
**Applies to:** Any entity operating under a license, registration, charter, certificate, permit, or similar authorization under New York Banking Law, Insurance Law, or Financial Services Law — including state-chartered banks, insurance companies, licensed lenders, mortgage servicers, money transmitters, virtual currency businesses, and others regulated by NYDFS
**Trigger:** DFS license, registration, or authorization in New York; foreign banking organizations with a New York branch or agency; any entity required to obtain a DFS license to conduct financial services business in New York State
**Jurisdiction:** New York State, USA; NYDFS enforces §23 NYCRR Part 500; one of the most prescriptive US state cybersecurity regulations — frequently used as a model by other states
**Not applicable to:** Entities with fewer than 10 employees, less than $5M in gross revenue, and less than $10M in year-end total assets (limited exemption under §500.19); federal credit unions (federally chartered, not DFS licensed); entities exclusively regulated by federal banking agencies without DFS licensing
**Parent index:** [`_index.md`](./_index.md)
**Regulatory basis:** 23 NYCRR Part 500 (as amended November 1, 2023 — Second Amendment)
**Authority:** New York State Department of Financial Services (NY DFS)
**Methodology reference:** NIST CSF; CIS Controls v8; NYDFS examination procedures

---

## Overview

NY DFS 23 NYCRR 500 is one of the most technically prescriptive financial cybersecurity regulations in the U.S. Unlike sector-agnostic frameworks (NIST CSF), 500 sets hard numeric thresholds: 72-hour breach notification, 6-year audit trail retention, mandatory MFA for specific access types, and annual certification filed directly with the superintendent.

The Second Amendment (Nov 2023) added Class A enhanced requirements and tightened existing MFA/encryption mandates. Phase-in for most Second Amendment requirements completed by November 2025.

**DETERMINISTIC density is very high.** Most core controls have binary or time-bounded obligations with no interpretation latitude.

---

## Scope pre-condition

```python
import pytest


@pytest.fixture(autouse=True)
def nydfs500_scope_check(entity_profile: dict):
    """Skip if entity does not hold a NY DFS license, registration, charter, or certificate."""
    if not entity_profile.get("nydfs_licensed_entity", False):
        pytest.skip(
            "NY DFS 23 NYCRR 500 does not apply — entity does not hold a NY DFS license, "
            "registration, charter, certificate, or BitLicense. Covered entity types include "
            "banks, insurance companies, mortgage companies, money transmitters, and virtual "
            "currency businesses licensed under NY Financial Services Law."
        )
```

### Exemption pre-filter

```python
def get_nydfs500_exemption_status(entity_profile: dict) -> dict:
    """
    Determine NY DFS 500 exemption status.
    All three limited-exemption criteria must be met simultaneously.
    Class A status is additive — applies additional requirements on top of full compliance.

    Returns dict with keys: limited_exempt, class_a, full_scope
    """
    employees = entity_profile.get("employee_count_global", 0)
    gross_revenue_usd = entity_profile.get("gross_revenue_usd_3yr_avg", 0)
    year_end_assets_usd = entity_profile.get("year_end_assets_usd", 0)
    consolidated_assets_usd = entity_profile.get("consolidated_assets_usd", 0)

    limited_exempt = (
        employees < 10
        and gross_revenue_usd < 5_000_000
        and year_end_assets_usd < 10_000_000
    )

    class_a = (
        consolidated_assets_usd > 20_000_000_000
        or employees > 2_000
    )

    return {
        "limited_exempt": limited_exempt,
        "class_a": class_a,
        "full_scope": not limited_exempt,
    }
```

---

## SECTION §500.04 — Chief Information Security Officer (CISO)

### Requirements extracted

**Source:** 23 NYCRR §500.04

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 504.1 | CISO designation | At all times | A qualified CISO must be designated, either in-house or via qualified third party | Written designation; CISO name in board records |
| 504.2 | CISO annual report to board | At least once per calendar year | CISO must report to the board (or equivalent governing body) on the cybersecurity program | Board minutes or written report with date; agenda item showing CISO presentation |
| 504.3 | CISO report content | With each report | Report must cover: material cybersecurity risks, assessment of program, significant cybersecurity events, planned changes | Report document with required sections |

### Tests — CISO

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


class TestCISORequirements:
    """§500.04 — CISO designation and annual board reporting."""

    def test_ciso_designated(self, entity_profile: dict, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — CISO must exist."""
        assert controls_evidence.get("ciso_designated_name") is not None, (
            "No CISO designated — 23 NYCRR §500.04(a) requires a qualified CISO. "
            "Third-party CISO arrangements are permitted if contractually documented."
        )

    @pytest.mark.assumption(
        id="ASSUME-NYDFS500-CISO-001",
        description=(
            "NY DFS §500.04(b) requires the CISO to report to the board of directors (or "
            "equivalent governing body for entities without a formal board) at least annually. "
            "The report must include: (1) overall status of the cybersecurity program and "
            "compliance with the regulation; (2) material cybersecurity risks to the covered "
            "entity; (3) actions taken and actions proposed to be taken. The 'at least annually' "
            "cadence is interpreted as once per 12 calendar months from last report date, not "
            "once per calendar year — a report in January and the next in December of the same "
            "year does not satisfy the requirement for the following year if the next report "
            "occurs in March. DFS examiners check board minutes for CISO agenda items."
        ),
        approved_by="CISO / Board Secretary",
        review_date="2026-11-01",
    )
    def test_ciso_annual_board_report(
        self,
        entity_profile: dict,
        controls_evidence: dict,
        reference_date: date,
    ):
        """Pattern 2: PARAMETERIZED — annual cadence is DETERMINISTIC; report content adequacy is PARAMETERIZED."""
        CISO_REPORT_MAX_INTERVAL_MONTHS = 12

        last_report_date = controls_evidence.get("ciso_last_board_report_date")
        assert last_report_date is not None, (
            "No CISO board report date found — §500.04(b) requires annual CISO reporting to the board."
        )

        cutoff = reference_date - relativedelta(months=CISO_REPORT_MAX_INTERVAL_MONTHS)
        assert last_report_date >= cutoff, (
            f"CISO board report is overdue: last report was {last_report_date}, "
            f"which is more than {CISO_REPORT_MAX_INTERVAL_MONTHS} months before {reference_date}. "
            "23 NYCRR §500.04(b) requires at least annual board reporting."
        )

    def test_ciso_report_required_content(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — content requirements are enumerated but adequacy is judgment."""
        required_topics = {
            "cybersecurity_program_status",
            "material_risks_identified",
            "significant_events_in_period",
        }
        report_sections = set(controls_evidence.get("ciso_report_topics_covered", []))
        missing = required_topics - report_sections
        assert not missing, (
            f"CISO board report missing required content areas: {missing}. "
            "23 NYCRR §500.04(b) requires status of program, material risks, and events."
        )
```

---

## SECTION §500.05 — Penetration Testing and Vulnerability Assessment

### Requirements extracted

**Source:** 23 NYCRR §500.05

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 505.1 | Annual penetration test | At least annually | All covered entities must conduct an annual penetration test of information systems | Pentest report with date, scope, methodology, findings, remediation plan |
| 505.2 | Bi-annual vulnerability assessment (Class A) | Every 6 months | Class A companies must conduct vulnerability assessments at least every 6 months | VA report with date, scanner tool, scope, findings |
| 505.3 | Risk-based vulnerability assessment (standard) | Annually or as needed per risk assessment | Standard entities must conduct periodic vulnerability assessments per their risk-based methodology | Assessment records; risk assessment driving frequency |
| 505.4 | Remediation of findings | Per risk-based timeline | Critical/high findings from pentest or VA must have documented remediation plans with target dates | Remediation tracker tied to pentest/VA findings |

### Tests — penetration testing

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


PENTEST_MAX_INTERVAL_MONTHS = 12
VA_MAX_INTERVAL_MONTHS_CLASS_A = 6


class TestPenetrationTesting:
    """§500.05 — Annual penetration testing; Class A bi-annual vulnerability assessment."""

    @pytest.mark.assumption(
        id="ASSUME-NYDFS500-PENTEST-001",
        description=(
            "NY DFS §500.05(a) requires annual penetration testing. The 'annual' requirement "
            "is interpreted as at least once per 12 calendar months from the last test completion "
            "date (not calendar year). The test must cover both network-level and application-level "
            "testing. DFS examination guidance indicates the test must be conducted by qualified "
            "personnel — internal or third-party. For Class A companies, an annual pentest is "
            "required in addition to (not instead of) bi-annual vulnerability assessments per "
            "§500.05(b)(2). Scope must include all systems in the cybersecurity scope, not merely "
            "a subset. Partial-scope tests generate a finding."
        ),
        approved_by="CISO",
        review_date="2026-11-01",
    )
    def test_annual_penetration_test(
        self,
        controls_evidence: dict,
        entity_profile: dict,
        reference_date: date,
    ):
        """Pattern 2: PARAMETERIZED — annual cadence is DETERMINISTIC; scope adequacy is PARAMETERIZED."""
        last_pentest_date = controls_evidence.get("last_penetration_test_date")
        assert last_pentest_date is not None, (
            "No penetration test date found — 23 NYCRR §500.05 requires at least annual pentesting."
        )
        cutoff = reference_date - relativedelta(months=PENTEST_MAX_INTERVAL_MONTHS)
        assert last_pentest_date >= cutoff, (
            f"Penetration test overdue: last test {last_pentest_date} is more than "
            f"{PENTEST_MAX_INTERVAL_MONTHS} months before {reference_date}. "
            "23 NYCRR §500.05 requires at least annual penetration testing."
        )

    def test_class_a_biannual_va(
        self,
        controls_evidence: dict,
        entity_profile: dict,
        reference_date: date,
    ):
        """Pattern 1: DETERMINISTIC — Class A bi-annual VA is a hard threshold."""
        exemption = get_nydfs500_exemption_status(entity_profile)
        if not exemption["class_a"]:
            pytest.skip("Entity is not Class A — bi-annual VA requirement does not apply.")

        last_va_date = controls_evidence.get("last_vulnerability_assessment_date")
        assert last_va_date is not None, (
            "No vulnerability assessment date found — Class A entities must conduct bi-annual "
            "vulnerability assessments per 23 NYCRR §500.05(b)(2)."
        )
        cutoff = reference_date - relativedelta(months=VA_MAX_INTERVAL_MONTHS_CLASS_A)
        assert last_va_date >= cutoff, (
            f"Vulnerability assessment overdue for Class A entity: last VA {last_va_date} "
            f"is more than {VA_MAX_INTERVAL_MONTHS_CLASS_A} months before {reference_date}. "
            "23 NYCRR §500.05(b)(2) requires bi-annual vulnerability assessments for Class A companies."
        )

    def test_pentest_findings_remediation_plan(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — finding existence is DETERMINISTIC; remediation plan is required."""
        findings = controls_evidence.get("pentest_open_critical_high_findings", [])
        for finding in findings:
            assert finding.get("remediation_plan_exists", False), (
                f"Pentest finding {finding.get('id', 'UNKNOWN')} has no remediation plan. "
                "23 NYCRR §500.05 requires findings to be addressed based on risk."
            )
            assert finding.get("target_remediation_date") is not None, (
                f"Pentest finding {finding.get('id', 'UNKNOWN')} has no target remediation date."
            )
```

---

## SECTION §500.06 — Audit Trail

### Requirements extracted

**Source:** 23 NYCRR §500.06

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 506.1 | Audit trail — critical systems | Continuously | Audit trail for all activity on critical systems (login/logout, admin actions, data access, config changes) | Log management system; critical system inventory; sample log output |
| 506.2 | Audit trail retention | At all times | Audit records must be retained for 6 years | Retention policy document; log storage configuration; oldest log date |
| 506.3 | Audit trail integrity | At all times | Audit records must be protected against alteration and unauthorized access | Write-once/WORM storage or equivalent; integrity monitoring |
| 506.4 | Financial system transaction trail | Continuously | Separate audit trail designed to detect and respond to cybersecurity events that have a reasonable likelihood of materially affecting the normal operation of the covered entity | Audit trail policy covering financial transaction reconstruction |

### Tests — audit trail

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


AUDIT_TRAIL_RETENTION_YEARS = 6


class TestAuditTrail:
    """§500.06 — 6-year audit trail retention and integrity."""

    def test_audit_trail_retention_policy_duration(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — 6-year retention is a hard requirement."""
        policy_retention_years = controls_evidence.get("audit_log_retention_policy_years")
        assert policy_retention_years is not None, (
            "No audit log retention policy found — §500.06 requires a documented audit trail "
            "with defined retention period."
        )
        assert policy_retention_years >= AUDIT_TRAIL_RETENTION_YEARS, (
            f"Audit trail retention policy specifies {policy_retention_years} years but "
            f"23 NYCRR §500.06 requires at least {AUDIT_TRAIL_RETENTION_YEARS} years."
        )

    def test_audit_trail_oldest_log_date(
        self, controls_evidence: dict, reference_date: date
    ):
        """Pattern 1: DETERMINISTIC — actual oldest log must be ≥6 years old."""
        oldest_log_date = controls_evidence.get("audit_log_oldest_date")
        assert oldest_log_date is not None, (
            "Cannot determine oldest available audit log date — §500.06 requires 6-year retention."
        )
        required_oldest = reference_date - relativedelta(years=AUDIT_TRAIL_RETENTION_YEARS)
        assert oldest_log_date <= required_oldest, (
            f"Oldest audit log is {oldest_log_date}, but 6-year retention requires logs back to "
            f"{required_oldest}. Logs predating {required_oldest} are missing. "
            "23 NYCRR §500.06 requires 6-year audit trail retention."
        )

    def test_critical_systems_audit_trail_coverage(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — critical system definition is org-defined; coverage completeness is required."""
        critical_systems = controls_evidence.get("critical_systems_inventory", [])
        assert critical_systems, (
            "No critical systems inventory — §500.06 requires audit trails for critical systems. "
            "Critical systems must be defined in the cybersecurity program per §500.02."
        )
        systems_without_audit_trail = [
            s for s in critical_systems if not s.get("audit_trail_enabled", False)
        ]
        assert not systems_without_audit_trail, (
            f"Critical systems without audit trail: {[s.get('name') for s in systems_without_audit_trail]}. "
            "23 NYCRR §500.06 requires audit trail coverage for all critical systems."
        )

    @pytest.mark.assumption(
        id="ASSUME-NYDFS500-AUDIT-001",
        description=(
            "NY DFS §500.06 requires audit trail records be protected from alteration and "
            "preserved for 6 years. 'Protected from alteration' is interpreted to require "
            "either: (a) WORM/write-once storage (e.g., AWS S3 Object Lock, immutable blob "
            "storage, optical WORM); (b) cryptographic integrity protection (HMAC chain); or "
            "(c) access controls that prevent modification by any operational user including "
            "system administrators, enforced at the storage layer. DFS examiners request "
            "evidence that audit logs cannot be modified by the same administrators who can "
            "modify the systems being logged — separation between log writer and log storage "
            "admin is expected."
        ),
        approved_by="CISO",
        review_date="2026-11-01",
    )
    def test_audit_trail_integrity_protection(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — 'protected from alteration' requires one of several accepted mechanisms."""
        integrity_mechanism = controls_evidence.get("audit_log_integrity_mechanism")
        accepted_mechanisms = {
            "worm_storage",
            "s3_object_lock",
            "immutable_blob",
            "cryptographic_hash_chain",
            "separated_log_storage_admin",
        }
        assert integrity_mechanism in accepted_mechanisms, (
            f"Audit log integrity mechanism '{integrity_mechanism}' is not in accepted list "
            f"{accepted_mechanisms}. 23 NYCRR §500.06 requires audit trail protection from alteration."
        )
```

---

## SECTION §500.07 — Access Privileges and Management

### Requirements extracted

**Source:** 23 NYCRR §500.07

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 507.1 | Least privilege | At all times | Access privileges must be limited to the minimum necessary to perform job functions | Access provisioning tickets; role definitions; periodic review results |
| 507.2 | Annual access review | At least annually | Access rights to critical systems must be reviewed at least annually | Access review report with date, reviewer, systems covered, actions taken |
| 507.3 | Privileged access controls | At all times | Privileged accounts must be managed — limit number, monitor, periodically review | PAM inventory; privileged account review records |
| 507.4 | Terminated user removal | Promptly | Access must be revoked promptly upon termination | Termination-to-revocation log; HR system integration |

### Tests — access privileges

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


ACCESS_REVIEW_MAX_INTERVAL_MONTHS = 12


class TestAccessPrivileges:
    """§500.07 — Least privilege, annual access review, privileged account controls."""

    def test_critical_system_access_review_cadence(
        self,
        controls_evidence: dict,
        reference_date: date,
    ):
        """Pattern 1: DETERMINISTIC — annual access review is a hard threshold."""
        last_access_review_date = controls_evidence.get("last_critical_system_access_review_date")
        assert last_access_review_date is not None, (
            "No access review date found — §500.07(a)(3) requires at least annual review "
            "of access rights to critical systems."
        )
        cutoff = reference_date - relativedelta(months=ACCESS_REVIEW_MAX_INTERVAL_MONTHS)
        assert last_access_review_date >= cutoff, (
            f"Access review overdue: last review {last_access_review_date} is more than "
            f"{ACCESS_REVIEW_MAX_INTERVAL_MONTHS} months before {reference_date}. "
            "23 NYCRR §500.07(a)(3) requires at least annual access review."
        )

    def test_no_terminated_user_active_access(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — terminated users with active access is a hard finding."""
        terminated_with_access = controls_evidence.get("terminated_users_with_active_access", [])
        assert not terminated_with_access, (
            f"Terminated users with active access to covered systems: "
            f"{[u.get('username') for u in terminated_with_access]}. "
            "23 NYCRR §500.07 requires prompt revocation upon termination."
        )
```

---

## SECTION §500.12 — Multi-Factor Authentication (MFA)

### Requirements extracted

**Source:** 23 NYCRR §500.12

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 512.1 | MFA — remote access | Any remote access to the internal network | MFA required for all remote network access | VPN/remote access logs; MFA enforcement configuration; no remote access path without MFA |
| 512.2 | MFA — privileged accounts | Any privileged account access | MFA required for all privileged accounts accessing covered systems | IAM configuration; privileged account login evidence; no privileged access path without MFA |
| 512.3 | MFA — external-facing web services | Web-based services accessible by external users | MFA required for all web-based services that provide external user access to covered systems | Web application authentication config; external login audit logs |
| 512.4 | MFA alternatives (CISO exception) | Only with CISO approval and compensating controls | Alternative authentication controls may substitute for MFA only if approved by CISO in writing | CISO exception documentation; compensating controls evidence |

### Tests — MFA

```python
import pytest


class TestMultiFactorAuthentication:
    """§500.12 — MFA for remote access, privileged accounts, and external-facing web services."""

    def test_remote_access_mfa_enforced(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — MFA for all remote access is binary."""
        remote_access_paths = controls_evidence.get("remote_access_paths", [])
        assert remote_access_paths, (
            "No remote access path inventory — §500.12 requires MFA for all remote access. "
            "An inventory of remote access paths is required to demonstrate coverage."
        )
        paths_without_mfa = [
            p for p in remote_access_paths
            if not p.get("mfa_enforced", False) and not p.get("ciso_exception_documented", False)
        ]
        assert not paths_without_mfa, (
            f"Remote access paths without MFA and without documented CISO exception: "
            f"{[p.get('name') for p in paths_without_mfa]}. "
            "23 NYCRR §500.12(a) requires MFA for all remote network access."
        )

    def test_privileged_account_mfa_enforced(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — MFA for all privileged accounts is binary."""
        privileged_accounts = controls_evidence.get("privileged_accounts_inventory", [])
        assert privileged_accounts, (
            "No privileged account inventory — §500.12 requires MFA for all privileged accounts. "
            "A privileged account inventory is required."
        )
        privileged_without_mfa = [
            a for a in privileged_accounts
            if not a.get("mfa_enabled", False) and not a.get("ciso_exception_documented", False)
        ]
        assert not privileged_without_mfa, (
            f"Privileged accounts without MFA: {[a.get('username') for a in privileged_without_mfa]}. "
            "23 NYCRR §500.12(a) requires MFA for all privileged accounts on covered systems."
        )

    def test_external_web_services_mfa_enforced(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — MFA for all external web services with user access is binary."""
        external_web_services = controls_evidence.get("external_web_services", [])
        services_without_mfa = [
            s for s in external_web_services
            if s.get("has_external_user_access", False)
            and not s.get("mfa_enforced", False)
            and not s.get("ciso_exception_documented", False)
        ]
        assert not services_without_mfa, (
            f"External web services with user access but without MFA: "
            f"{[s.get('name') for s in services_without_mfa]}. "
            "23 NYCRR §500.12(b) requires MFA for all web-based services accessible by external users."
        )

    @pytest.mark.assumption(
        id="ASSUME-NYDFS500-MFA-001",
        description=(
            "NY DFS §500.12 was significantly tightened by the Second Amendment (Nov 2023). "
            "The current rule requires MFA for: (a) all remote access to internal networks, "
            "(b) all privileged accounts, (c) all web-based services with external user access. "
            "The prior CISO-waiver provision (pre-amendment) is now restricted — a CISO "
            "exception requires written documentation of the specific alternative control and "
            "annual CISO review. 'Privileged account' is not defined in 500 text; DFS "
            "examination guidance aligns with NIST SP 800-53 definition: any account with "
            "elevated access rights beyond a standard user, including service accounts with "
            "administrative access. Legacy application accounts that cannot support MFA may "
            "qualify for CISO exception only with compensating controls (IP restriction, "
            "privileged access workstation, session recording)."
        ),
        approved_by="CISO",
        review_date="2026-11-01",
    )
    def test_ciso_mfa_exception_documented(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — CISO exception must be written and current."""
        exceptions = controls_evidence.get("mfa_ciso_exceptions", [])
        for exc in exceptions:
            assert exc.get("ciso_signature_date") is not None, (
                f"MFA CISO exception for '{exc.get('system')}' has no CISO signature date. "
                "23 NYCRR §500.12 exceptions require written CISO approval."
            )
            assert exc.get("compensating_controls"), (
                f"MFA CISO exception for '{exc.get('system')}' has no compensating controls documented. "
                "CISO exceptions must describe the alternative controls in place."
            )
```

---

## SECTION §500.15 — Encryption of Nonpublic Information (NPI)

### Requirements extracted

**Source:** 23 NYCRR §500.15

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 515.1 | NPI encryption in transit | Any transmission of NPI | NPI must be encrypted in transit | TLS configuration; certificate inventory; protocol version audits; no plaintext NPI transmission paths |
| 515.2 | NPI encryption at rest | NPI stored on any covered system | NPI must be encrypted at rest OR CISO must review/approve compensating controls annually | Encryption-at-rest configuration; CISO review records if compensating controls used |
| 515.3 | CISO annual review — at-rest compensating controls | If compensating controls used in lieu of encryption at rest | CISO must conduct and document annual review of at-rest compensating controls | CISO annual review document with date; compensating control description |

### Tests — encryption

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


TRANSIT_MINIMUM_TLS_VERSION = 1.2
TRANSIT_PREFERRED_TLS_VERSION = 1.3
AT_REST_CISO_REVIEW_MAX_MONTHS = 12


class TestEncryption:
    """§500.15 — NPI encryption in transit (mandatory) and at rest (mandatory or CISO-reviewed compensating controls)."""

    def test_npi_encryption_in_transit_no_plaintext_paths(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — any plaintext NPI transmission path is a hard finding."""
        transmission_paths = controls_evidence.get("npi_transmission_paths", [])
        assert transmission_paths, (
            "No NPI transmission path inventory — §500.15(a) requires NPI to be encrypted in "
            "transit. An inventory of all NPI transmission paths is required."
        )
        plaintext_paths = [
            p for p in transmission_paths
            if p.get("protocol", "").upper() in {"HTTP", "FTP", "TELNET", "SMTP_CLEARTEXT"}
            and not p.get("tunneled_via_vpn", False)
        ]
        assert not plaintext_paths, (
            f"NPI transmitted over cleartext protocols: {[p.get('name') for p in plaintext_paths]}. "
            "23 NYCRR §500.15(a) requires all NPI to be encrypted in transit."
        )

    def test_npi_encryption_in_transit_tls_version(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — TLS 1.0 and 1.1 are deprecated; minimum TLS 1.2."""
        tls_endpoints = controls_evidence.get("tls_endpoint_configs", [])
        weak_tls_endpoints = [
            ep for ep in tls_endpoints
            if ep.get("minimum_tls_version", 0) < TRANSIT_MINIMUM_TLS_VERSION
        ]
        assert not weak_tls_endpoints, (
            f"Endpoints with TLS version below {TRANSIT_MINIMUM_TLS_VERSION}: "
            f"{[ep.get('name') for ep in weak_tls_endpoints]}. "
            "23 NYCRR §500.15 requires strong encryption; TLS 1.0/1.1 are deprecated."
        )

    @pytest.mark.assumption(
        id="ASSUME-NYDFS500-ENC-001",
        description=(
            "NY DFS §500.15(b) requires NPI encryption at rest 'to the extent feasible.' "
            "Where encryption at rest is not feasible, the CISO must review and approve "
            "alternative compensating controls on an annual basis. DFS examination guidance "
            "treats 'not feasible' narrowly — legacy systems with no encryption capability "
            "qualify; performance concerns alone do not. The compensating control must be "
            "documented, risk-rated, and tied to a remediation/migration plan. Systems that "
            "can support encryption at rest but have not implemented it, without a CISO "
            "exception, are a direct §500.15(b) finding. Acceptable at-rest encryption: "
            "AES-128 minimum (AES-256 preferred); database-level TDE; filesystem encryption "
            "(BitLocker, dm-crypt); application-layer encryption. Key management must prevent "
            "the same administrator from accessing both data and encryption keys."
        ),
        approved_by="CISO",
        review_date="2026-11-01",
    )
    def test_npi_at_rest_encryption_or_ciso_exception(
        self, controls_evidence: dict, reference_date: date
    ):
        """Pattern 2: PARAMETERIZED — encryption at rest is required or CISO must annually review compensating controls."""
        npi_storage_systems = controls_evidence.get("npi_storage_systems", [])
        for system in npi_storage_systems:
            has_encryption = system.get("encryption_at_rest_enabled", False)
            has_ciso_exception = system.get("ciso_exception_at_rest", False)
            ciso_review_date = system.get("ciso_exception_review_date")

            if not has_encryption and not has_ciso_exception:
                pytest.fail(
                    f"NPI storage system '{system.get('name')}' has no encryption at rest and no "
                    "CISO exception. 23 NYCRR §500.15(b) requires encryption at rest or documented "
                    "CISO review of compensating controls."
                )
            if not has_encryption and has_ciso_exception:
                assert ciso_review_date is not None, (
                    f"System '{system.get('name')}' has a CISO at-rest exception but no review date. "
                    "§500.15(b) requires CISO to conduct annual reviews of compensating controls."
                )
                cutoff = reference_date - relativedelta(months=AT_REST_CISO_REVIEW_MAX_MONTHS)
                assert ciso_review_date >= cutoff, (
                    f"CISO at-rest exception for '{system.get('name')}' was last reviewed "
                    f"{ciso_review_date} — more than 12 months ago. Annual CISO review required."
                )
```

---

## SECTION §500.17 — Notices to Superintendent (72-hour Reporting)

### Requirements extracted

**Source:** 23 NYCRR §500.17

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 517.1 | 72-hour cybersecurity event notification | Upon determining a reportable cybersecurity event occurred | Notice must be provided to superintendent within 72 hours of determination | Notification record; timestamps of determination and notification |
| 517.2 | Notification threshold — third-party impact | Event at a third-party service provider | If third party has a cybersecurity event that affects the covered entity's covered systems or NPI, 72-hour clock applies | TPSP incident notification records |
| 517.3 | Annual certification | By April 15 each year | File annual certification of compliance with 23 NYCRR 500 with the superintendent | DFS online portal submission confirmation; submission date |
| 517.4 | Material deficiency disclosure | With annual certification | Known material deficiencies in compliance must be disclosed in the annual certification | Deficiency disclosure section of certification; remediation plan |

### Tests — notification and certification

```python
import pytest
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


NOTIFICATION_WINDOW_HOURS = 72
ANNUAL_CERTIFICATION_MONTH = 4   # April
ANNUAL_CERTIFICATION_DAY = 15    # April 15


class TestNotificationAndCertification:
    """§500.17 — 72-hour breach notification and annual certification."""

    @pytest.mark.assumption(
        id="ASSUME-NYDFS500-NOTIF-001",
        description=(
            "NY DFS §500.17(a) requires notification within 72 hours of a covered entity "
            "'reasonably believing' that a cybersecurity event meeting notification criteria "
            "has occurred. The 72-hour clock begins at the moment of determination, not at "
            "the moment of initial detection. Reportable events include: (1) any event "
            "requiring notice to a government body or self-regulatory organization under "
            "any law; (2) events with a reasonable likelihood of materially harming any "
            "material part of normal operations; (3) unauthorized access to privileged "
            "accounts; (4) deployment of ransomware in material portions of the information "
            "system. DFS requires notifications even if the event was contained before "
            "material harm occurred. The 72 hours is a maximum — earlier notification is "
            "expected when facts are clear. Initial notice can be preliminary; supplement "
            "with follow-on report within 90 days."
        ),
        approved_by="CISO / Legal",
        review_date="2026-11-01",
    )
    def test_past_incidents_notified_within_72_hours(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — notification threshold determination is PARAMETERIZED; timing once determined is DETERMINISTIC."""
        reportable_incidents = controls_evidence.get("reportable_cybersecurity_incidents", [])
        for incident in reportable_incidents:
            determination_time = incident.get("determination_timestamp")
            notification_time = incident.get("dfs_notification_timestamp")

            if determination_time is None:
                continue  # No determination means 72-hour clock not started

            assert notification_time is not None, (
                f"Incident {incident.get('id', 'UNKNOWN')}: DFS was not notified after threshold "
                "determination. 23 NYCRR §500.17(a) requires notification within 72 hours."
            )

            hours_elapsed = (notification_time - determination_time).total_seconds() / 3600
            assert hours_elapsed <= NOTIFICATION_WINDOW_HOURS, (
                f"Incident {incident.get('id', 'UNKNOWN')}: DFS notified {hours_elapsed:.1f} hours "
                f"after threshold determination. 23 NYCRR §500.17(a) requires notification within "
                f"{NOTIFICATION_WINDOW_HOURS} hours."
            )

    def test_annual_certification_filed(
        self, controls_evidence: dict, reference_date: date
    ):
        """Pattern 1: DETERMINISTIC — annual certification filing has a fixed deadline."""
        current_year = reference_date.year
        certification_due = date(current_year, ANNUAL_CERTIFICATION_MONTH, ANNUAL_CERTIFICATION_DAY)

        if reference_date < certification_due:
            # Check previous year's certification if we haven't reached this year's deadline yet
            cert_year = current_year - 1
        else:
            cert_year = current_year

        last_cert_date = controls_evidence.get("dfs_annual_certification_date")
        assert last_cert_date is not None, (
            f"No DFS annual certification record found. "
            "23 NYCRR §500.17(b) requires annual certification filed with the superintendent."
        )

        expected_cert_by = date(cert_year, ANNUAL_CERTIFICATION_MONTH, ANNUAL_CERTIFICATION_DAY)
        assert last_cert_date.year == cert_year, (
            f"Annual certification for {cert_year} not found. Last certification was {last_cert_date}. "
            f"23 NYCRR §500.17(b) requires annual certification by April 15 of each year."
        )
        assert last_cert_date <= expected_cert_by, (
            f"Annual certification for {cert_year} was filed {last_cert_date}, after the April 15 deadline. "
            "23 NYCRR §500.17(b) requires certification by April 15."
        )

    def test_annual_certification_deficiency_disclosure(self, controls_evidence: dict):
        """Pattern 3: CONTESTED — completeness of deficiency disclosure is human judgment."""
        known_deficiencies = controls_evidence.get("known_compliance_deficiencies", [])
        certification_disclosures = controls_evidence.get(
            "certification_disclosed_deficiencies", []
        )
        undisclosed = [
            d for d in known_deficiencies
            if d.get("id") not in {cd.get("id") for cd in certification_disclosures}
        ]
        if undisclosed:
            pytest.fail(
                f"Known compliance deficiencies not disclosed in annual certification: "
                f"{[d.get('description') for d in undisclosed]}. "
                "23 NYCRR §500.17(b) requires disclosure of identified areas of non-compliance. "
                "REQUIRES HUMAN REVIEW: deficiency classification must be confirmed by CISO/Legal "
                "before determining disclosure obligation."
            )
```

---

## SECTION §500.17(b) annual certification — Class A additional requirements

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


class TestClassARequirements:
    """Class A enhanced requirements — companies > $20B assets or > 2,000 employees."""

    def test_class_a_independent_audit(
        self, controls_evidence: dict, entity_profile: dict, reference_date: date
    ):
        """Pattern 1: DETERMINISTIC — Class A annual independent audit is required."""
        exemption = get_nydfs500_exemption_status(entity_profile)
        if not exemption["class_a"]:
            pytest.skip("Entity is not Class A — independent audit requirement does not apply.")

        last_audit_date = controls_evidence.get("class_a_independent_audit_date")
        assert last_audit_date is not None, (
            "No independent cybersecurity audit record — Class A entities must conduct an annual "
            "independent audit of the cybersecurity program per 23 NYCRR §500.02(g)."
        )
        cutoff = reference_date - relativedelta(months=12)
        assert last_audit_date >= cutoff, (
            f"Class A independent audit overdue: last audit {last_audit_date} is more than "
            f"12 months before {reference_date}."
        )

    def test_class_a_edr_deployed(self, controls_evidence: dict, entity_profile: dict):
        """Pattern 1: DETERMINISTIC — Class A EDR deployment is binary."""
        exemption = get_nydfs500_exemption_status(entity_profile)
        if not exemption["class_a"]:
            pytest.skip("Entity is not Class A — EDR requirement does not apply.")

        endpoints = controls_evidence.get("endpoint_inventory", [])
        endpoints_without_edr = [
            ep for ep in endpoints
            if ep.get("covered_system_endpoint", False)
            and not ep.get("edr_installed", False)
        ]
        assert not endpoints_without_edr, (
            f"Covered system endpoints without EDR: {[ep.get('hostname') for ep in endpoints_without_edr]}. "
            "Class A entities must deploy endpoint detection and response (EDR) solutions "
            "per 23 NYCRR §500.14(b)(2) (Class A enhanced requirements)."
        )

    @pytest.mark.assumption(
        id="ASSUME-NYDFS500-CLASSA-001",
        description=(
            "NY DFS Class A thresholds (>$20B consolidated assets OR >2,000 employees globally) "
            "apply on a consolidated basis. For insurance holding companies, the consolidated "
            "asset test includes all affiliates. The 2,000-employee threshold is global headcount "
            "including part-time employees and contractors — DFS examination guidance has not "
            "published a precise definition, but erring toward inclusion is the safer posture. "
            "Foreign banking organizations (FBOs) with NY branches apply the thresholds to the "
            "NY branch's portion plus the global organization as applicable. Class A status must "
            "be re-evaluated annually as assets and headcount change."
        ),
        approved_by="CISO / Legal / Finance",
        review_date="2026-11-01",
    )
    def test_class_a_status_current(
        self, controls_evidence: dict, reference_date: date
    ):
        """Pattern 2: PARAMETERIZED — Class A determination must be current."""
        last_class_a_determination_date = controls_evidence.get("class_a_status_determination_date")
        if last_class_a_determination_date is None:
            pytest.skip("No Class A determination on file — entity may not be subject to 500.")
        cutoff = reference_date - relativedelta(months=12)
        assert last_class_a_determination_date >= cutoff, (
            f"Class A status determination is outdated: last review {last_class_a_determination_date} "
            "is more than 12 months ago. Class A eligibility must be re-evaluated annually."
        )
```

---

## SECTION §500.14 — Training and Monitoring

### Requirements extracted

**Source:** 23 NYCRR §500.14

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 514.1 | Annual cybersecurity training | At least once per calendar year | All covered individuals must receive cybersecurity awareness training annually | Training completion records; date; scope of covered individuals |
| 514.2 | Anomalous activity monitoring | Continuously | Monitoring of authorized users for anomalous behavior that could indicate unauthorized access | SIEM or equivalent; alert configuration; anomaly detection rules |

### Tests — training

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


TRAINING_MAX_INTERVAL_MONTHS = 12


class TestTrainingAndMonitoring:
    """§500.14 — Annual cybersecurity training and anomalous activity monitoring."""

    def test_annual_cybersecurity_training_completion(
        self, controls_evidence: dict, reference_date: date
    ):
        """Pattern 1: DETERMINISTIC — annual training is required for all covered individuals."""
        training_completion_rate = controls_evidence.get("cybersecurity_training_completion_rate")
        last_training_date = controls_evidence.get("last_cybersecurity_training_date")

        assert last_training_date is not None, (
            "No cybersecurity training record — §500.14(a) requires annual training for "
            "all covered individuals."
        )
        cutoff = reference_date - relativedelta(months=TRAINING_MAX_INTERVAL_MONTHS)
        assert last_training_date >= cutoff, (
            f"Cybersecurity training last conducted {last_training_date}, more than "
            f"{TRAINING_MAX_INTERVAL_MONTHS} months before {reference_date}. "
            "23 NYCRR §500.14(a) requires annual training."
        )

    @pytest.mark.assumption(
        id="ASSUME-NYDFS500-TRAIN-001",
        description=(
            "NY DFS §500.14(a) requires cybersecurity awareness training 'at least annually' "
            "for all covered individuals. 'Covered individuals' means employees, contractors, "
            "and agents who have access to covered systems or NPI. DFS examiners focus on "
            "completion rates — 100% completion is expected; anything below 90% generates "
            "examination comments. Training must be specific to the organization's actual "
            "threat landscape and policies — generic vendor-provided content without "
            "organizational customization has drawn DFS criticism. Training records must be "
            "retained as audit evidence. Social engineering simulations (phishing tests) "
            "are encouraged but do not substitute for formal training."
        ),
        approved_by="CISO / HR",
        review_date="2026-11-01",
    )
    def test_training_covers_all_covered_individuals(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — training must cover all covered individuals (contractors, agents)."""
        total_covered = controls_evidence.get("total_covered_individuals_count", 0)
        trained_count = controls_evidence.get("trained_individuals_count", 0)
        assert total_covered > 0, "No covered individual count — cannot verify training coverage."

        completion_rate = trained_count / total_covered if total_covered else 0
        assert completion_rate >= 1.0, (
            f"Cybersecurity training completion rate is {completion_rate:.0%} "
            f"({trained_count}/{total_covered}). "
            "23 NYCRR §500.14(a) requires all covered individuals to receive training annually."
        )
```

---

## Open assumption registry

| ID | Domain | Description | Review date |
|---|---|---|---|
| ASSUME-NYDFS500-CISO-001 | CISO / §500.04 | Annual board report cadence (12-month rolling, not calendar year); report content must include program status, material risks, events | 2026-11-01 |
| ASSUME-NYDFS500-PENTEST-001 | Penetration Testing / §500.05 | Annual pentest scope must cover all in-scope systems; internal or third-party; Class A: additive bi-annual VA requirement | 2026-11-01 |
| ASSUME-NYDFS500-AUDIT-001 | Audit Trail / §500.06 | Protection from alteration requires WORM, crypto chain, or separated log-storage admin; same admin cannot modify logs and covered systems | 2026-11-01 |
| ASSUME-NYDFS500-MFA-001 | MFA / §500.12 | Second Amendment tightened MFA; CISO exception now requires annual review + compensating controls; service accounts with admin access are privileged accounts | 2026-11-01 |
| ASSUME-NYDFS500-ENC-001 | Encryption / §500.15 | "Not feasible" for at-rest is narrow; performance alone insufficient; acceptable mechanisms include AES-128+ TDE, filesystem encryption; key separation required | 2026-11-01 |
| ASSUME-NYDFS500-NOTIF-001 | Notification / §500.17 | 72-hour clock starts at determination, not detection; unauthorized privileged account access and ransomware are per-se reportable; preliminary notice acceptable | 2026-11-01 |
| ASSUME-NYDFS500-CLASSA-001 | Class A / §500.02(g) | Consolidated basis for asset test; global headcount including contractors; re-evaluated annually; FBO treatment applies to NY branch + global org | 2026-11-01 |
| ASSUME-NYDFS500-TRAIN-001 | Training / §500.14 | All covered individuals including contractors; 100% completion expected; generic content insufficient; phishing simulation does not substitute | 2026-11-01 |
