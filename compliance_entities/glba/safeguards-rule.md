# GLBA — FTC Safeguards Rule Specification (16 CFR Part 314)

**Spec file:** `safeguards-rule.md`
**Registry version:** 2026.05
**Last updated:** 2026-05-21
**Parent index:** [`_index.md`](./_index.md)
**Regulatory basis:** Gramm-Leach-Bliley Act (GLBA) § 501(b); 16 CFR Part 314 (FTC Safeguards Rule, revised effective June 9, 2023)
**Authority:** Federal Trade Commission (FTC) for non-bank financial institutions; parallel enforcement by OCC/FDIC/Federal Reserve/NCUA for banks and credit unions
**Methodology reference:** NIST Cybersecurity Framework; FTC Safeguards Rule Compliance Guide (2023)

---

## Overview

The revised FTC Safeguards Rule (June 2023) transformed GLBA from a principles-based framework into a specific, enumerated set of security requirements closely aligned with NIST CSF and NY DFS 500. Key changes from the prior rule: mandatory encryption (at rest AND in transit, no compensating controls option unlike NY DFS), mandatory MFA for all employees accessing customer information (not just remote/privileged), and specific penetration testing + vulnerability scanning cadences for entities with > 5,000 customer records.

**Notable distinctions from NY DFS 500:**
- GLBA encryption at rest is **mandatory** — no "CISO compensating controls" exception
- MFA applies to **all employees** accessing customer information (NY DFS only requires MFA for remote access, privileged accounts, and external web)
- Pentest/VA obligations are size-gated: only entities with > 5,000 records
- GLBA does not require a 72-hour breach notification to regulators (that obligation runs under separate state laws and the FTC Safeguards Rule § 314.15 for certain data breaches — see below)

---

## Scope pre-condition

```python
import pytest


@pytest.fixture(autouse=True)
def glba_scope_check(entity_profile: dict):
    """Skip if entity is not a non-bank financial institution subject to FTC jurisdiction."""
    if not entity_profile.get("glba_ftc_covered_entity", False):
        pytest.skip(
            "GLBA FTC Safeguards Rule (16 CFR Part 314) does not apply — entity is not a "
            "non-bank financial institution under FTC jurisdiction. Bank entities are subject "
            "to parallel Interagency Guidelines (OCC/FDIC/Fed/NCUA), not this file. "
            "Non-bank covered entities include: mortgage brokers, auto dealers, tax preparers, "
            "financial planners, credit reporting agencies, fintechs significantly engaged in "
            "financial products/services."
        )
```

### Small-company size gate

```python
SMALL_COMPANY_RECORDS_THRESHOLD = 5_000


def is_glba_small_company_exempt(entity_profile: dict) -> bool:
    """
    Entities with fewer than 5,000 customer records are exempt from:
    §314.4(g)(1) annual penetration testing,
    §314.4(g)(2) bi-annual vulnerability scanning,
    §314.4(h) audit log requirements.
    All other Safeguards Rule requirements apply regardless of size.
    """
    customer_records = entity_profile.get("customer_record_count", 0)
    return customer_records < SMALL_COMPANY_RECORDS_THRESHOLD
```

---

## SECTION §314.3 — Written Information Security Program (WISP)

### Requirements extracted

**Source:** 16 CFR §314.3

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 3.1 | WISP existence | At all times | Written Information Security Program (WISP) must exist, appropriate to size, complexity, nature, and customer information sensitivity | Written WISP document; version with effective date; annual review signature |
| 3.2 | WISP appropriateness | At all times | WISP must be commensurate with size, complexity, and nature of activities | Program scope section of WISP; documented rationale for approach |
| 3.3 | WISP annual review and update | At least annually | WISP must be reviewed and updated at least annually and after any material change | Review date; update history; change log |

### Tests — WISP

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


WISP_REVIEW_MAX_INTERVAL_MONTHS = 12


class TestWrittenInformationSecurityProgram:
    """§314.3 — Written WISP existence and annual review."""

    def test_wisp_document_exists(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — WISP must exist as a written document."""
        wisp_document_path = controls_evidence.get("wisp_document_path")
        wisp_effective_date = controls_evidence.get("wisp_effective_date")
        assert wisp_document_path is not None, (
            "No WISP document found — 16 CFR §314.3 requires a written Information Security "
            "Program. The program must be a documented, named policy document, not informal practices."
        )
        assert wisp_effective_date is not None, (
            "WISP has no effective date — §314.3 requires a dated written program."
        )

    def test_wisp_annual_review(
        self, controls_evidence: dict, reference_date: date
    ):
        """Pattern 1: DETERMINISTIC — annual WISP review is a hard threshold."""
        last_wisp_review_date = controls_evidence.get("wisp_last_review_date")
        assert last_wisp_review_date is not None, (
            "No WISP review date found — 16 CFR §314.4(j) requires annual review and update "
            "of the information security program."
        )
        cutoff = reference_date - relativedelta(months=WISP_REVIEW_MAX_INTERVAL_MONTHS)
        assert last_wisp_review_date >= cutoff, (
            f"WISP annual review overdue: last review {last_wisp_review_date} is more than "
            f"{WISP_REVIEW_MAX_INTERVAL_MONTHS} months before {reference_date}. "
            "16 CFR §314.4(j) requires at least annual review."
        )
```

---

## SECTION §314.4(a) — Qualified Individual (QI)

### Requirements extracted

**Source:** 16 CFR §314.4(a)

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 4a.1 | Qualified Individual designation | At all times | A qualified individual (QI) — employee, officer, affiliate, or service provider — must be designated as responsible for the information security program | Written designation; QI name in WISP; role description |
| 4a.2 | QI board reporting | At least annually | QI must report annually to the board of directors or equivalent governing body (or senior officer if no formal board) | Board minutes; written annual report; date |

### Tests — qualified individual

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


QI_REPORT_MAX_INTERVAL_MONTHS = 12


class TestQualifiedIndividual:
    """§314.4(a) — Qualified Individual designation and annual board/senior officer reporting."""

    def test_qualified_individual_designated(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — QI must be named."""
        qi_name = controls_evidence.get("qualified_individual_name")
        assert qi_name is not None, (
            "No Qualified Individual (QI) designated — 16 CFR §314.4(a) requires designation of "
            "a qualified individual responsible for the information security program. "
            "The QI may be an in-house employee/officer or a service provider."
        )

    @pytest.mark.assumption(
        id="ASSUME-GLBA-QI-001",
        description=(
            "16 CFR §314.4(a) requires annual reporting by the Qualified Individual to the "
            "board of directors or equivalent governing body. For entities with no formal board, "
            "the report goes to the 'senior officer' — typically the CEO, COO, or President. "
            "The report must cover: (1) overall status of the information security program and "
            "compliance with Part 314; (2) material matters related to the program, including "
            "risk assessment results, risk management decisions, service provider arrangements, "
            "results of testing, security events or violations, and recommendations for changes. "
            "FTC Safeguards Rule guidance (2023) aligns this requirement closely with the GLBA "
            "Interagency Guidelines and NY DFS §500.04 — the same annual board security briefing "
            "can satisfy all three if it covers the required content areas."
        ),
        approved_by="QI / Board Secretary",
        review_date="2026-11-01",
    )
    def test_qi_annual_board_report(
        self, controls_evidence: dict, reference_date: date
    ):
        """Pattern 2: PARAMETERIZED — annual cadence is DETERMINISTIC; report content adequacy is PARAMETERIZED."""
        last_report_date = controls_evidence.get("qi_last_board_report_date")
        assert last_report_date is not None, (
            "No QI board report date — 16 CFR §314.4(k) requires annual written report to board "
            "or senior officer on the status of the information security program."
        )
        cutoff = reference_date - relativedelta(months=QI_REPORT_MAX_INTERVAL_MONTHS)
        assert last_report_date >= cutoff, (
            f"QI board report overdue: last report {last_report_date} is more than "
            f"{QI_REPORT_MAX_INTERVAL_MONTHS} months before {reference_date}. "
            "16 CFR §314.4(k) requires annual reporting."
        )

    def test_qi_report_required_content(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — required content elements enumerated in §314.4(k)."""
        required_elements = {
            "program_overall_status",
            "risk_assessment_results",
            "risk_management_and_control_decisions",
            "service_provider_arrangements",
            "testing_results",
            "security_events_and_violations",
            "recommendations_for_changes",
        }
        report_elements = set(controls_evidence.get("qi_report_topics_covered", []))
        missing = required_elements - report_elements
        assert not missing, (
            f"QI board report missing required content elements: {missing}. "
            "16 CFR §314.4(k) enumerates required content for the annual security report."
        )
```

---

## SECTION §314.4(c)(3) — Encryption (Mandatory, No Exceptions)

### Requirements extracted

**Source:** 16 CFR §314.4(c)(3)

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 4c3.1 | Encryption in transit | Any transmission of customer information | Customer information must be encrypted in transit | TLS configuration; no cleartext transmission paths |
| 4c3.2 | Encryption at rest | Customer information stored on any system | Customer information must be encrypted at rest | Storage encryption config; database TDE; filesystem encryption |

> **Critical distinction from NY DFS §500.15:** GLBA encryption at rest is **mandatory** — there is no CISO compensating controls exception. The revised 2023 rule removed the flexibility that existed in the prior rule. Any customer information at rest that is not encrypted is a direct §314.4(c)(3) violation.

### Tests — encryption

```python
import pytest


TRANSIT_MINIMUM_TLS_VERSION = 1.2


class TestEncryption:
    """§314.4(c)(3) — Mandatory encryption in transit AND at rest (no compensating controls exception)."""

    def test_customer_info_encryption_in_transit(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — cleartext transmission of customer information is a hard violation."""
        transmission_paths = controls_evidence.get("customer_info_transmission_paths", [])
        assert transmission_paths, (
            "No customer information transmission path inventory — §314.4(c)(3) requires "
            "encryption in transit. An inventory is required to demonstrate coverage."
        )
        cleartext_paths = [
            p for p in transmission_paths
            if p.get("protocol", "").upper() in {"HTTP", "FTP", "TELNET", "SMTP_CLEARTEXT"}
            and not p.get("tunneled_via_vpn", False)
        ]
        assert not cleartext_paths, (
            f"Customer information transmitted over cleartext protocols: "
            f"{[p.get('name') for p in cleartext_paths]}. "
            "16 CFR §314.4(c)(3) requires all customer information to be encrypted in transit."
        )

    def test_customer_info_tls_version(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — TLS version must be 1.2 or higher."""
        tls_endpoints = controls_evidence.get("tls_endpoint_configs", [])
        weak_tls = [
            ep for ep in tls_endpoints
            if ep.get("minimum_tls_version", 0) < TRANSIT_MINIMUM_TLS_VERSION
        ]
        assert not weak_tls, (
            f"Endpoints with TLS below {TRANSIT_MINIMUM_TLS_VERSION}: "
            f"{[ep.get('name') for ep in weak_tls]}. "
            "16 CFR §314.4(c)(3) requires strong encryption; TLS 1.0/1.1 are deprecated."
        )

    @pytest.mark.assumption(
        id="ASSUME-GLBA-ENC-001",
        description=(
            "16 CFR §314.4(c)(3) (revised 2023) requires encryption of customer information "
            "both in transit and at rest. Unlike the NY DFS §500.15(b) rule, there is NO "
            "compensating controls exception for at-rest encryption in the FTC Safeguards Rule. "
            "FTC guidance: 'feasibility' language was removed in the 2023 revision; encryption "
            "at rest is now an absolute requirement. Acceptable at-rest encryption: AES-128 "
            "minimum (AES-256 preferred); database TDE; filesystem-level encryption; "
            "application-layer encryption. Systems that hold customer information in unencrypted "
            "form — including backups, test copies, and development datasets — are in scope. "
            "Masking/tokenization of production data for test environments is a recommended "
            "control. Key management must ensure the encryption keys are not accessible to "
            "the same personnel who can access the customer data."
        ),
        approved_by="QI / CISO",
        review_date="2026-11-01",
    )
    def test_customer_info_encryption_at_rest(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — encryption at rest is mandatory; scope definition (what counts as customer info) is PARAMETERIZED."""
        storage_systems = controls_evidence.get("customer_info_storage_systems", [])
        assert storage_systems, (
            "No customer information storage inventory — §314.4(c)(3) requires encryption at rest. "
            "An inventory of all systems storing customer information is required."
        )
        unencrypted_systems = [
            s for s in storage_systems
            if not s.get("encryption_at_rest_enabled", False)
        ]
        assert not unencrypted_systems, (
            f"Customer information storage systems without encryption at rest: "
            f"{[s.get('name') for s in unencrypted_systems]}. "
            "16 CFR §314.4(c)(3) requires encryption at rest — no compensating controls exception."
        )
```

---

## SECTION §314.4(c)(5) — Multi-Factor Authentication

### Requirements extracted

**Source:** 16 CFR §314.4(c)(5)

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 4c5.1 | MFA for all employees accessing customer information | Any access to customer information | MFA required for all employees who access customer information (not limited to remote access or privileged accounts) | MFA configuration; user access logs; application authentication settings |
| 4c5.2 | Equivalent controls exception | Only with written QI approval | May substitute equivalent technical controls with prior written approval from QI | QI exception documentation; equivalent control description |

> **Key distinction:** GLBA MFA applies to **all employees** who access customer information — broader than NY DFS §500.12 which only requires MFA for remote access, privileged accounts, and external web services.

### Tests — MFA

```python
import pytest


class TestMultiFactorAuthentication:
    """§314.4(c)(5) — MFA for all employees accessing customer information."""

    @pytest.mark.assumption(
        id="ASSUME-GLBA-MFA-001",
        description=(
            "16 CFR §314.4(c)(5) (revised 2023) requires MFA for any individual who accesses "
            "any information system — not just remote access or privileged accounts. This is "
            "broader than NY DFS §500.12. FTC guidance clarifies that on-site users accessing "
            "customer information from a company workstation also require MFA unless QI-approved "
            "equivalent controls are in place. 'Equivalent controls' must be documented and "
            "approved in writing by the QI before deployment. Acceptable equivalents: "
            "biometric + PIN; hardware token; risk-based adaptive authentication with strong "
            "fraud signals. Password-only access for any user to any system that stores or "
            "processes customer information is a direct §314.4(c)(5) violation. "
            "Service accounts without interactive login that access customer data fall in scope "
            "unless they are controlled via certificate-based authentication and cannot be used "
            "interactively — document the technical rationale in the WISP."
        ),
        approved_by="QI",
        review_date="2026-11-01",
    )
    def test_all_customer_info_access_requires_mfa(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — scope (which users/systems) is PARAMETERIZED; MFA enforcement is DETERMINISTIC."""
        access_paths_to_customer_info = controls_evidence.get(
            "customer_info_access_paths", []
        )
        assert access_paths_to_customer_info, (
            "No customer information access path inventory — §314.4(c)(5) requires MFA for "
            "all employees accessing customer information. An access path inventory is required."
        )
        paths_without_mfa = [
            p for p in access_paths_to_customer_info
            if not p.get("mfa_enforced", False) and not p.get("qi_exception_documented", False)
        ]
        assert not paths_without_mfa, (
            f"Customer information access paths without MFA and without QI exception: "
            f"{[p.get('name') for p in paths_without_mfa]}. "
            "16 CFR §314.4(c)(5) requires MFA for all employees accessing customer information."
        )

    def test_qi_mfa_exceptions_documented(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — QI exception must be written and describe equivalent controls."""
        exceptions = controls_evidence.get("mfa_qi_exceptions", [])
        for exc in exceptions:
            assert exc.get("qi_written_approval_date") is not None, (
                f"MFA QI exception for '{exc.get('system')}' lacks written QI approval date. "
                "§314.4(c)(5) requires prior written QI approval for any MFA alternative."
            )
            assert exc.get("equivalent_control_description"), (
                f"MFA QI exception for '{exc.get('system')}' has no equivalent control description. "
                "The alternative technical control must be documented."
            )
```

---

## SECTION §314.4(g) — Penetration Testing and Vulnerability Scanning

### Requirements extracted

**Source:** 16 CFR §314.4(g)(1)–(2)

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 4g.1 | Annual penetration test | Entities with > 5,000 records | Annual penetration test of information systems | Pentest report with date, methodology, scope, findings, remediation |
| 4g.2 | Bi-annual vulnerability scan | Entities with > 5,000 records | Vulnerability assessment every 6 months AND after any material change to operations or business | VA report with date and scope; post-change VA trigger records |

### Tests — penetration testing and vulnerability scanning

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta


PENTEST_MAX_INTERVAL_MONTHS = 12
VA_MAX_INTERVAL_MONTHS = 6


class TestPenetrationTestingAndVA:
    """§314.4(g) — Annual pentest and bi-annual VA (entities with > 5,000 customer records only)."""

    def test_annual_penetration_test(
        self, controls_evidence: dict, entity_profile: dict, reference_date: date
    ):
        """Pattern 1: DETERMINISTIC — annual pentest is a hard threshold for in-scope entities."""
        if is_glba_small_company_exempt(entity_profile):
            pytest.skip(
                "Entity has < 5,000 customer records — §314.4(g)(1) annual penetration test "
                "requirement does not apply."
            )

        last_pentest_date = controls_evidence.get("last_penetration_test_date")
        assert last_pentest_date is not None, (
            "No penetration test date found — 16 CFR §314.4(g)(1) requires annual penetration "
            "testing for entities with > 5,000 customer records."
        )
        cutoff = reference_date - relativedelta(months=PENTEST_MAX_INTERVAL_MONTHS)
        assert last_pentest_date >= cutoff, (
            f"Penetration test overdue: last test {last_pentest_date} is more than "
            f"{PENTEST_MAX_INTERVAL_MONTHS} months before {reference_date}. "
            "16 CFR §314.4(g)(1) requires annual penetration testing."
        )

    @pytest.mark.assumption(
        id="ASSUME-GLBA-PENTEST-001",
        description=(
            "16 CFR §314.4(g) requires annual penetration testing for entities with > 5,000 "
            "customer records. The 5,000-record threshold applies to the total number of customer "
            "records maintained — not accounts or unique customers. FTC guidance has not defined "
            "'record' narrowly; the conservative interpretation counts each individual's financial "
            "information as a record. The pentest must cover all information systems in scope "
            "under the Safeguards Rule — partial scope tests are a finding. Internal or external "
            "testers are both acceptable; credentials must document tester qualifications. "
            "The bi-annual vulnerability assessment must be conducted independently of the annual "
            "pentest — a pentest does not substitute for a vulnerability scan. After any material "
            "change (new system, major acquisition, significant configuration change), a "
            "vulnerability scan must be conducted regardless of the regular 6-month cadence."
        ),
        approved_by="QI",
        review_date="2026-11-01",
    )
    def test_biannual_vulnerability_scan(
        self, controls_evidence: dict, entity_profile: dict, reference_date: date
    ):
        """Pattern 2: PARAMETERIZED — bi-annual cadence is DETERMINISTIC; scope and material-change trigger are PARAMETERIZED."""
        if is_glba_small_company_exempt(entity_profile):
            pytest.skip(
                "Entity has < 5,000 customer records — §314.4(g)(2) bi-annual vulnerability "
                "scan requirement does not apply."
            )

        last_va_date = controls_evidence.get("last_vulnerability_scan_date")
        assert last_va_date is not None, (
            "No vulnerability scan date found — 16 CFR §314.4(g)(2) requires bi-annual "
            "vulnerability scanning for entities with > 5,000 customer records."
        )
        cutoff = reference_date - relativedelta(months=VA_MAX_INTERVAL_MONTHS)
        assert last_va_date >= cutoff, (
            f"Vulnerability scan overdue: last scan {last_va_date} is more than "
            f"{VA_MAX_INTERVAL_MONTHS} months before {reference_date}. "
            "16 CFR §314.4(g)(2) requires bi-annual vulnerability scanning."
        )

    def test_post_material_change_va_conducted(self, controls_evidence: dict, entity_profile: dict):
        """Pattern 2: PARAMETERIZED — material change trigger is binary; what counts as material is PARAMETERIZED."""
        if is_glba_small_company_exempt(entity_profile):
            pytest.skip("Small company exempt from §314.4(g)(2).")

        material_changes = controls_evidence.get("material_changes_without_va", [])
        assert not material_changes, (
            f"Material changes without subsequent vulnerability assessment: "
            f"{[c.get('description') for c in material_changes]}. "
            "16 CFR §314.4(g)(2) requires vulnerability assessment after any material change."
        )
```

---

## SECTION §314.4(h) — Audit Logs

### Requirements extracted

**Source:** 16 CFR §314.4(h)

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 4h.1 | Audit log monitoring | Continuously | Monitor and filter audit logs of every event that could reasonably lead to unauthorized acquisition of customer information | Log management system; alert configuration |
| 4h.2 | Audit log retention | At all times | Retain audit logs as long as necessary for the information security program but minimum as defined in WISP | Log retention policy in WISP; log storage configuration |

### Tests — audit logs

```python
import pytest


class TestAuditLogs:
    """§314.4(h) — Audit log monitoring (entities with > 5,000 customer records)."""

    def test_audit_log_monitoring_enabled(
        self, controls_evidence: dict, entity_profile: dict
    ):
        """Pattern 1: DETERMINISTIC — audit log monitoring is required for in-scope entities."""
        if is_glba_small_company_exempt(entity_profile):
            pytest.skip("Entity has < 5,000 records — §314.4(h) audit log requirement does not apply.")

        log_monitoring_enabled = controls_evidence.get("audit_log_monitoring_enabled", False)
        assert log_monitoring_enabled, (
            "Audit log monitoring is not enabled — 16 CFR §314.4(h) requires monitoring and "
            "filtering of audit logs of every event that could lead to unauthorized acquisition "
            "of customer information."
        )

    @pytest.mark.assumption(
        id="ASSUME-GLBA-AUDIT-001",
        description=(
            "16 CFR §314.4(h) requires monitoring and filtering of audit logs for events that "
            "could reasonably lead to unauthorized acquisition of customer information. "
            "Unlike NY DFS §500.06 which specifies a 6-year retention period, GLBA §314.4(h) "
            "does not specify a retention period — it defers to the WISP. FTC examination "
            "guidance suggests 1–3 years for small/mid-size entities; 3+ years for larger "
            "entities. Cross-framework note: if the entity is also subject to NY DFS (6 years) "
            "or SOX (7 years), the longer retention period applies across all frameworks. "
            "Monitoring scope must include: all systems that store or process customer "
            "information; privileged user activity; authentication events; data exports and "
            "transfers. A SIEM or equivalent log aggregation tool is the standard implementation."
        ),
        approved_by="QI",
        review_date="2026-11-01",
    )
    def test_audit_log_retention_defined_in_wisp(self, controls_evidence: dict, entity_profile: dict):
        """Pattern 2: PARAMETERIZED — retention period is WISP-defined; monitoring scope is PARAMETERIZED."""
        if is_glba_small_company_exempt(entity_profile):
            pytest.skip("Entity has < 5,000 records — §314.4(h) does not apply.")

        log_retention_policy = controls_evidence.get("audit_log_retention_policy_defined_in_wisp", False)
        assert log_retention_policy, (
            "No audit log retention policy in WISP — §314.4(h) requires audit log retention "
            "as specified in the information security program. The WISP must define the retention period."
        )
```

---

## SECTION §314.4(i) — Incident Response Plan

### Requirements extracted

**Source:** 16 CFR §314.4(i)(1)–(8)

| # | Element | Content |
|---|---------|---------|
| IRP-1 | Goals | Defined goals of the incident response plan |
| IRP-2 | Internal processes | Internal process for responding to a security event |
| IRP-3 | Roles and responsibilities | Clear roles and responsibilities in response |
| IRP-4 | Communications and escalation | Internal/external communications and information sharing |
| IRP-5 | Remediation | Requirements for the remediation of any identified weaknesses in information systems |
| IRP-6 | Documentation | Requirements for documentation and reporting regarding security events |
| IRP-7 | Evaluation and revision | Evaluation and revision following a security event |
| IRP-8 | Identification of service providers | Identification of service providers that will be utilized during or after a security event |

### Tests — incident response plan

```python
import pytest


IRP_REQUIRED_ELEMENTS = {
    "goals",
    "internal_processes",
    "roles_and_responsibilities",
    "communications_and_escalation",
    "remediation_requirements",
    "documentation_and_reporting",
    "evaluation_and_revision",
    "service_provider_identification",
}


class TestIncidentResponsePlan:
    """§314.4(i) — Written incident response plan with 8 required elements."""

    def test_irp_exists(self, controls_evidence: dict):
        """Pattern 1: DETERMINISTIC — IRP must exist as a written document."""
        irp_document_path = controls_evidence.get("irp_document_path")
        assert irp_document_path is not None, (
            "No incident response plan document found — 16 CFR §314.4(i) requires a written "
            "incident response plan for safeguarding customer information."
        )

    def test_irp_required_elements_present(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — 8 required elements enumerated in §314.4(i)(1)–(8); completeness is auditable."""
        irp_elements_present = set(controls_evidence.get("irp_elements_present", []))
        missing_elements = IRP_REQUIRED_ELEMENTS - irp_elements_present
        assert not missing_elements, (
            f"Incident response plan missing required elements: {missing_elements}. "
            "16 CFR §314.4(i) requires all 8 elements: goals, internal processes, "
            "roles/responsibilities, communications, remediation, documentation, "
            "evaluation/revision, service provider identification."
        )

    @pytest.mark.human_review_required(
        reason=(
            "16 CFR §314.4(i)(4) requires the IRP to address communications and information "
            "sharing. Determining whether the communications plan is adequate — particularly "
            "whether external notification obligations (state breach laws, FTC §314.15 breach "
            "notification for financial institutions) are properly integrated — requires "
            "Legal and Compliance review. The existence of the IRP element is DETERMINISTIC; "
            "whether the notification triggers and recipient list are current requires human "
            "judgment and legal verification."
        )
    )
    def test_irp_notification_obligations_current(self, controls_evidence: dict):
        """Pattern 3: CONTESTED — IRP notification obligations require human/Legal review."""
        pass
```

---

## SECTION §314.15 — Breach Notification to FTC

### Requirements extracted

**Source:** 16 CFR §314.15 (effective May 13, 2024)

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 15.1 | FTC breach notification | Security breach involving ≥ 500 customers | Notify FTC as soon as possible, no later than 30 days after discovery | FTC notification record; discovery and notification timestamps |
| 15.2 | Notification to affected individuals | As required by applicable state law | State breach notification laws continue to apply (timeframes vary by state) | State notification records per applicable laws |

### Tests — breach notification

```python
import pytest
from datetime import timedelta


FTC_NOTIFICATION_WINDOW_DAYS = 30
GLBA_BREACH_NOTIFICATION_RECORDS_THRESHOLD = 500


class TestBreachNotification:
    """§314.15 — FTC breach notification for breaches involving ≥500 customers (effective May 2024)."""

    @pytest.mark.assumption(
        id="ASSUME-GLBA-NOTIF-001",
        description=(
            "16 CFR §314.15 (effective May 13, 2024) requires FTC notification for breaches "
            "of unencrypted customer information involving 500 or more customers. The 30-day "
            "clock runs from discovery, not from determination of reportability (unlike NY DFS "
            "§500.17 which starts at determination). Notification is made via the FTC's online "
            "reporting platform. Note: this is separate from state breach notification laws — "
            "entities must comply with both. The 30-day FTC window is a maximum; FTC guidance "
            "states 'as soon as possible.' Breaches involving encrypted customer information "
            "where the encryption keys were not compromised do not trigger notification — "
            "reinforcing the §314.4(c)(3) mandatory encryption requirement as a direct "
            "means of eliminating notification obligations."
        ),
        approved_by="QI / Legal",
        review_date="2026-11-01",
    )
    def test_breach_notifications_filed_within_30_days(self, controls_evidence: dict):
        """Pattern 2: PARAMETERIZED — 30-day window is DETERMINISTIC; breach classification is PARAMETERIZED."""
        reportable_breaches = controls_evidence.get("reportable_ftc_breaches", [])
        for breach in reportable_breaches:
            discovery_date = breach.get("discovery_date")
            notification_date = breach.get("ftc_notification_date")
            affected_count = breach.get("affected_customer_count", 0)

            if affected_count < GLBA_BREACH_NOTIFICATION_RECORDS_THRESHOLD:
                continue

            assert discovery_date is not None, (
                f"Breach {breach.get('id', 'UNKNOWN')} has no discovery date."
            )
            assert notification_date is not None, (
                f"Breach {breach.get('id', 'UNKNOWN')}: FTC not notified despite {affected_count} "
                "affected customers (≥500 threshold). §314.15 requires FTC notification."
            )
            days_elapsed = (notification_date - discovery_date).days
            assert days_elapsed <= FTC_NOTIFICATION_WINDOW_DAYS, (
                f"Breach {breach.get('id', 'UNKNOWN')}: FTC notified {days_elapsed} days after "
                f"discovery, exceeding the {FTC_NOTIFICATION_WINDOW_DAYS}-day window. "
                "16 CFR §314.15 requires notification no later than 30 days after discovery."
            )
```

---

## Open assumption registry

| ID | Domain | Description | Review date |
|---|---|---|---|
| ASSUME-GLBA-QI-001 | Qualified Individual / §314.4(a) | Annual board/senior-officer report; required content: program status, risk results, management decisions, service providers, testing, events, recommendations | 2026-11-01 |
| ASSUME-GLBA-ENC-001 | Encryption / §314.4(c)(3) | At-rest encryption is mandatory — 2023 revision removed "feasibility" exception; covers backups, test copies, and dev datasets; key separation required | 2026-11-01 |
| ASSUME-GLBA-MFA-001 | MFA / §314.4(c)(5) | Applies to all employees accessing customer information (not just remote/privileged); QI exception requires written approval + equivalent control description | 2026-11-01 |
| ASSUME-GLBA-PENTEST-001 | Pentest / §314.4(g) | 5,000-record threshold counts individual records; bi-annual VA is independent of annual pentest; post-material-change VA required regardless of regular cadence | 2026-11-01 |
| ASSUME-GLBA-AUDIT-001 | Audit Logs / §314.4(h) | No specified retention period — WISP-defined; cross-framework: NY DFS (6 yr) or SOX (7 yr) prevails if entity is dual-subject; SIEM is standard implementation | 2026-11-01 |
| ASSUME-GLBA-NOTIF-001 | Breach Notification / §314.15 | 30-day FTC notification from discovery (not determination); ≥500 customers threshold; encrypted-data breaches exempt if keys not compromised | 2026-11-01 |
