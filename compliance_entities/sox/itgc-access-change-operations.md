# SOX — IT General Controls: Access, Change Management, and Computer Operations

**Spec file:** `itgc-access-change-operations.md`
**Registry version:** 2026.05
**Last updated:** 2026-05-21
**Applies to:** SEC-registered publicly traded companies — US domestic issuers and foreign private issuers (FPIs) listed on US stock exchanges; external auditors registered with the PCAOB; public accounting firms auditing SEC registrants
**Trigger:** SEC registration under the Securities Exchange Act of 1934 (ongoing reporting) or Securities Act of 1933 (initial registration/IPO triggers SOX); listing on NYSE, NASDAQ, or other US national securities exchange; PCAOB registration required for auditors of SEC registrants
**Jurisdiction:** United States; extraterritorial — FPIs listed on US exchanges must comply (though with some modified SOX requirements, e.g., management assessment only, no auditor attestation for smaller FPIs); PCAOB registered audit firms worldwide
**Not applicable to:** Private companies (no SEC registration); non-profit and government organizations; foreign companies not listed on US exchanges and not registered with the SEC; de-listed companies (SOX Section 404 compliance obligation ends); SEC registrants that are non-accelerated filers (limited Section 404(b) exemptions)
**Parent index:** [`_index.md`](./_index.md)
**Regulatory basis:** Sarbanes-Oxley Act §302, §404; PCAOB AS 2201; COSO 2013 Internal Control Framework
**Authority:** SEC; PCAOB; external auditors
**Methodology reference:** PCAOB AS 2201 (ICFR attestation); COSO 2013; ISACA COBIT 2019

---

## Overview

SOX IT General Controls (ITGCs) are not specified by statute — they are the IT controls that auditors (internal and external) rely on to determine that application-level financial reporting controls are operating effectively. ITGCs provide the foundation: if ITGCs are ineffective, application controls relying on them are considered unreliable, potentially resulting in expanded substantive testing or a material weakness finding.

The four ITGC domains: **Logical Access**, **Change Management**, **Computer Operations**, and **Physical/Environmental**. This spec file covers the first three — the highest audit activity domains.

**DETERMINISTIC density is high in access and change management.** Termination-to-revocation timing, approval-before-change evidence, and backup completion are binary/threshold controls with no interpretation required.

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def sox_scope_check(entity_profile: dict):
    """Skip if entity is not a U.S. public company or is not in-scope for ITGC testing."""
    if not entity_profile.get("sec_reporting_company", False):
        pytest.skip(
            "SOX §404 ITGCs do not apply — entity is not a U.S. SEC-reporting company "
            "(not listed on a U.S. exchange or exempt)"
        )
    if not entity_profile.get("system_in_itgc_scope", False):
        pytest.skip(
            "System is not designated as a key system supporting financial reporting — "
            "ITGC testing applies only to systems identified in the SOX scope inventory"
        )
```

---

## DOMAIN 1 — Logical Access Controls

### Section 1.1 — User Provisioning (DETERMINISTIC)

#### Requirements extracted

**Source:** PCAOB AS 2201 ¶28–¶31; COSO CC6.2

| # | Control | Condition | Obligation | Evidence |
|---|---------|-----------|------------|---------|
| 1.1.1 | Access grant authorization | Before access is provisioned to any financial system | Written approval from access owner (manager or system owner) must exist before access is provisioned | Access provisioning ticket with approver name, date, and access level; ticket date precedes provisioning date |
| 1.1.2 | Access consistent with role | At provisioning | Access provisioned must match the role/function requested and approved; no excess permissions beyond request | Provisioning ticket role vs. actual permissions granted comparison |
| 1.1.3 | New hire onboarding access | Within first day of employment for standard users; within 4 hours for emergency access | Access provisioned only after HR confirms employment start; no access provisioned before start date | Provisioning ticket date vs. HR system start date |

#### Tests — provisioning

```python
import pytest
from datetime import date


class TestUserProvisioning:
    """Pattern 1: DETERMINISTIC — approval before access is a binary requirement."""

    @pytest.mark.assumption(
        id="ASSUME-SOX-ACCESS-001",
        description=(
            "SOX provisioning evidence: external auditors sample provisioning tickets to "
            "verify: (1) an approved request exists, (2) the approval predates provisioning, "
            "(3) access granted matches what was approved. The approval authority must be "
            "documented (typically line manager or system/data owner, not IT helpdesk). "
            "Self-approval (requestor = approver) is a segregation of duties violation. "
            "Provisioning within the same ticket as the approval is acceptable if timestamps "
            "confirm approval preceded provisioning."
        ),
        approved_by="IT Controls / Internal Audit",
        review_date="2026-05-21",
    )
    def test_access_provisioning_has_prior_approval(self, provisioning_record: dict):
        ticket_id = provisioning_record.get("ticket_id")
        approval_date = provisioning_record.get("approval_date")
        provisioning_date = provisioning_record.get("provisioning_date")
        approver = provisioning_record.get("approver_id")
        requestor = provisioning_record.get("requestor_id")

        assert approval_date is not None, (
            f"Provisioning ticket '{ticket_id}': no approval date recorded — "
            "SOX ITGC requires documented approval before access is granted; "
            "absence of approval evidence is a control deficiency that auditors will cite"
        )
        assert approver != requestor, (
            f"Provisioning ticket '{ticket_id}': approver ({approver}) is the same as "
            "the requestor ({requestor}) — self-approval violates segregation of duties "
            "and is a SOX ITGC finding; access requests must be approved by an independent party"
        )
        assert approval_date <= provisioning_date, (
            f"Provisioning ticket '{ticket_id}': access provisioned on {provisioning_date} "
            f"BEFORE approval on {approval_date} — access must not be granted prior to approval; "
            "retroactive approvals are a control exception requiring separate documentation"
        )

    def test_access_granted_matches_approved_scope(self, provisioning_record: dict):
        approved_roles = set(provisioning_record.get("approved_roles", []))
        provisioned_roles = set(provisioning_record.get("provisioned_roles", []))
        ticket_id = provisioning_record.get("ticket_id")

        excess_roles = provisioned_roles - approved_roles
        assert not excess_roles, (
            f"Provisioning ticket '{ticket_id}': roles provisioned include "
            f"{sorted(excess_roles)} which were NOT in the approved request — "
            "over-provisioning (granting more than approved) is a SOX ITGC finding "
            "indicating the provisioning control is not operating effectively"
        )
```

### Section 1.2 — User Deprovisioning (DETERMINISTIC)

#### Requirements extracted

**Source:** PCAOB AS 2201; COSO CC6.2; industry practice (PCAOB inspection findings)

| # | Control | Threshold | Evidence |
|---|---------|-----------|---------|
| 1.2.1 | Privileged account revocation on termination | ≤ 1 business day from HR termination date | Ticket timestamp showing privileged access removed; HR termination date from HRIS |
| 1.2.2 | Standard access revocation on termination | ≤ 5 business days from HR termination date | Access revocation ticket; HRIS termination date comparison |
| 1.2.3 | Role transfer on job change | ≤ 10 business days from role change effective date | Access modification ticket; HR role change date |

#### DETERMINISTIC thresholds

| Event | Privileged access | Standard access |
|---|---|---|
| Termination | ≤ 1 business day | ≤ 5 business days |
| Role change (excess access removed) | ≤ 1 business day | ≤ 10 business days |

#### Tests — deprovisioning

```python
import pytest
from datetime import date

PRIVILEGED_TERMINATION_MAX_BUSINESS_DAYS = 1
STANDARD_TERMINATION_MAX_BUSINESS_DAYS = 5
ROLE_CHANGE_MAX_BUSINESS_DAYS = 10


def business_days_between(start: date, end: date) -> int:
    """Count business days between two dates (Mon–Fri, no holidays)."""
    from datetime import timedelta
    days = 0
    current = start
    while current < end:
        current += timedelta(days=1)
        if current.weekday() < 5:  # Monday=0, Friday=4
            days += 1
    return days


class TestUserDeprovisioning:
    """Pattern 1: DETERMINISTIC — termination-to-revocation timing is a hard threshold."""

    @pytest.mark.assumption(
        id="ASSUME-SOX-ACCESS-002",
        description=(
            "SOX deprovisioning thresholds: external auditors universally test terminated "
            "user access as a high-risk logical access control. The 1 business day threshold "
            "for privileged access and 5 business days for standard access are industry-standard "
            "benchmarks recognized by PCAOB; they are not codified in statute. 'Terminated' "
            "means the HR record shows a separation date; the clock starts on that date, not "
            "the last day worked. Accounts still active after these thresholds constitute a "
            "deficiency; a pattern of late revocations without compensating controls typically "
            "rises to a significant deficiency."
        ),
        approved_by="IT Controls / Internal Audit",
        review_date="2026-05-21",
    )
    def test_privileged_access_revoked_within_1_business_day_of_termination(
        self, termination_record: dict
    ):
        user_id = termination_record.get("user_id")
        termination_date = termination_record.get("termination_date")
        privileged_revocation_date = termination_record.get("privileged_access_revocation_date")
        had_privileged_access = termination_record.get("had_privileged_access", False)

        if not had_privileged_access:
            pytest.skip("User did not have privileged access — test not applicable")

        assert privileged_revocation_date is not None, (
            f"User '{user_id}': terminated on {termination_date} but no privileged access "
            "revocation date recorded — privileged account access must be revoked within "
            f"{PRIVILEGED_TERMINATION_MAX_BUSINESS_DAYS} business day(s) of termination; "
            "active privileged accounts for terminated users is a HIGH-severity SOX finding"
        )

        days_elapsed = business_days_between(termination_date, privileged_revocation_date)
        assert days_elapsed <= PRIVILEGED_TERMINATION_MAX_BUSINESS_DAYS, (
            f"User '{user_id}': privileged access revoked {days_elapsed} business day(s) "
            f"after termination — exceeds {PRIVILEGED_TERMINATION_MAX_BUSINESS_DAYS} business "
            "day threshold; active privileged accounts for terminated users is the most "
            "consistently cited SOX ITGC finding in PCAOB inspection reports"
        )

    def test_standard_access_revoked_within_5_business_days_of_termination(
        self, termination_record: dict
    ):
        user_id = termination_record.get("user_id")
        termination_date = termination_record.get("termination_date")
        standard_revocation_date = termination_record.get("standard_access_revocation_date")

        assert standard_revocation_date is not None, (
            f"User '{user_id}': terminated on {termination_date} but no standard access "
            f"revocation recorded — standard access must be revoked within "
            f"{STANDARD_TERMINATION_MAX_BUSINESS_DAYS} business days of termination"
        )

        days_elapsed = business_days_between(termination_date, standard_revocation_date)
        assert days_elapsed <= STANDARD_TERMINATION_MAX_BUSINESS_DAYS, (
            f"User '{user_id}': standard access revoked {days_elapsed} business day(s) "
            f"after termination — exceeds {STANDARD_TERMINATION_MAX_BUSINESS_DAYS} business "
            "day threshold"
        )
```

### Section 1.3 — Periodic User Access Review (PARAMETERIZED)

#### Requirements extracted

| # | Control | Threshold | Evidence |
|---|---------|-----------|---------|
| 1.3.1 | User access review completed | At least annually (quarterly for privileged access) | Access review completion record; sign-off by access owner; date |
| 1.3.2 | Exceptions remediated | Within 30 days of access review completion | Remediation ticket; access modification date vs. review completion date |
| 1.3.3 | All in-scope systems reviewed | Per review cycle | System coverage report; no systems skipped without documented basis |

#### Tests — periodic access review

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta

STANDARD_REVIEW_INTERVAL_MONTHS = 12   # at least annually
PRIVILEGED_REVIEW_INTERVAL_MONTHS = 3  # quarterly for privileged
ACCESS_REVIEW_REMEDIATION_DAYS = 30


class TestPeriodicAccessReview:
    """Pattern 2: PARAMETERIZED — review cadence is org-defined; completion is DETERMINISTIC."""

    @pytest.mark.assumption(
        id="ASSUME-SOX-ACCESS-003",
        description=(
            "SOX access review cadence: SOX does not mandate a specific review frequency; "
            "auditors assess whether the cadence is appropriate given risk. Industry standard "
            "recognized by PCAOB is: quarterly for privileged/admin accounts, annually for "
            "standard user accounts. The completion of the review (owner sign-off) and "
            "remediation of exceptions within 30 days are DETERMINISTIC. A review completed "
            "late or with exceptions unresolved is a control deficiency."
        ),
        approved_by="IT Controls / Internal Audit",
        review_date="2026-05-21",
    )
    def test_standard_access_review_not_overdue(self, access_review_record: dict):
        system_id = access_review_record.get("system_id")
        review_type = access_review_record.get("review_type", "standard")
        last_review_date = access_review_record.get("last_completed_review_date")

        if review_type == "privileged":
            pytest.skip("Handled by privileged access review test")

        assert last_review_date is not None, (
            f"System '{system_id}': no annual access review on record — "
            "SOX ITGC requires periodic access reviews; absence of review evidence "
            "is a control deficiency"
        )

        due_date = last_review_date + relativedelta(months=STANDARD_REVIEW_INTERVAL_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"System '{system_id}': annual access review overdue — "
            f"last review: {last_review_date}, due: {due_date}, today: {today}"
        )

    def test_privileged_access_review_quarterly_not_overdue(self, access_review_record: dict):
        system_id = access_review_record.get("system_id")
        review_type = access_review_record.get("review_type", "standard")
        last_review_date = access_review_record.get("last_completed_review_date")

        if review_type != "privileged":
            pytest.skip("This test applies to privileged access reviews only")

        assert last_review_date is not None, (
            f"System '{system_id}': no quarterly privileged access review on record"
        )

        due_date = last_review_date + relativedelta(months=PRIVILEGED_REVIEW_INTERVAL_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"System '{system_id}': quarterly privileged access review overdue — "
            f"last review: {last_review_date}, due: {due_date}, today: {today}"
        )

    def test_access_review_exceptions_remediated_within_30_days(self, access_review_record: dict):
        review_completion_date = access_review_record.get("review_completion_date")
        exceptions = access_review_record.get("exceptions_identified", [])

        for exception in exceptions:
            exc_id = exception.get("exception_id")
            remediation_date = exception.get("remediation_date")
            is_open = exception.get("still_open", False)

            assert not is_open, (
                f"Access review exception '{exc_id}': still open — exceptions identified "
                "in access reviews must be remediated; unresolved exceptions indicate the "
                "review control is not operating effectively"
            )

            if review_completion_date and remediation_date:
                days_to_remediate = (remediation_date - review_completion_date).days
                assert days_to_remediate <= ACCESS_REVIEW_REMEDIATION_DAYS, (
                    f"Access review exception '{exc_id}': remediated {days_to_remediate} days "
                    f"after review completion — exceeds {ACCESS_REVIEW_REMEDIATION_DAYS}-day "
                    "target; slow remediation of access exceptions is a SOX ITGC finding"
                )
```

### Section 1.4 — Segregation of Duties (PARAMETERIZED)

```python
import pytest


class TestSegregationOfDuties:
    """Pattern 2: PARAMETERIZED — SoD matrix is org-defined; enforcement is DETERMINISTIC."""

    @pytest.mark.assumption(
        id="ASSUME-SOX-ACCESS-004",
        description=(
            "SOX SoD: the SoD conflict matrix defines incompatible role combinations. "
            "Common financial system SoD conflicts: create vendor + approve payments; "
            "initiate journal entry + approve journal entry; purchase order creation + "
            "invoice approval + payment. The matrix must be current (reviewed at least "
            "annually by management). Automated SoD conflict detection in ERP systems "
            "(Oracle, SAP, etc.) generates the evidence. Exceptions to SoD conflicts must "
            "be documented with compensating controls reviewed and approved by management."
        ),
        approved_by="IT Controls / Controller / Internal Audit",
        review_date="2026-05-21",
    )
    def test_sod_matrix_current(self, sod_program: dict):
        last_matrix_review = sod_program.get("last_matrix_review_date")
        from datetime import date
        from dateutil.relativedelta import relativedelta

        assert last_matrix_review is not None, (
            "No SoD conflict matrix review on record — SOX ITGC requires a documented "
            "SoD conflict matrix reviewed at least annually by management"
        )

        due_date = last_matrix_review + relativedelta(months=12)
        assert date.today() <= due_date, (
            f"SoD conflict matrix overdue for annual review — "
            f"last review: {last_matrix_review}, due: {due_date}"
        )

    def test_active_sod_conflicts_have_approved_compensating_controls(
        self, user_access_profile: dict
    ):
        user_id = user_access_profile.get("user_id")
        sod_conflicts = user_access_profile.get("sod_conflicts_detected", [])

        for conflict in sod_conflicts:
            conflict_id = conflict.get("conflict_id")
            has_compensating_control = conflict.get("compensating_control_approved", False)
            has_management_exception = conflict.get("management_exception_approved", False)

            assert has_compensating_control or has_management_exception, (
                f"User '{user_id}': active SoD conflict '{conflict_id}' "
                f"({conflict.get('conflict_description', 'unknown')}) has no approved "
                "compensating control or management exception — active unmitigated SoD "
                "conflicts are control deficiencies that may rise to significant deficiency "
                "depending on the financial reporting impact of the conflicting roles"
            )
```

---

## DOMAIN 2 — Change Management Controls

### Section 2.1 — Change Authorization (DETERMINISTIC)

#### Requirements extracted

| # | Control | Threshold | Evidence |
|---|---------|-----------|---------|
| 2.1.1 | Approved change ticket before production deployment | Before any production change | Change management ticket with approver sign-off; ticket timestamp precedes deployment |
| 2.1.2 | Approved change ticket includes testing evidence | Before promotion to production | Test results or test sign-off documented in or linked to change ticket |
| 2.1.3 | Developer cannot deploy to production independently | All production deployments | Deployment is performed by person other than developer (or by automated pipeline with separation controls) |

```python
import pytest


class TestChangeAuthorization:
    """Pattern 1: DETERMINISTIC — approval before production change is absolute."""

    @pytest.mark.assumption(
        id="ASSUME-SOX-CHANGE-001",
        description=(
            "SOX change management: external auditors test change management by sampling "
            "production changes and verifying: (1) approved change ticket exists, (2) "
            "approval predates deployment, (3) testing evidence exists, (4) developer did "
            "not deploy their own code to production. The 'developer cannot deploy own code' "
            "requirement is a segregation of duties control that external auditors test with "
            "high frequency. Automated deployment pipelines (CI/CD) satisfy this if the "
            "pipeline enforces separation (developer cannot approve their own PR and trigger "
            "deployment without a second person approving). Emergency changes require "
            "retrospective approval within 1–5 business days per most control frameworks."
        ),
        approved_by="IT Controls / Change Advisory Board",
        review_date="2026-05-21",
    )
    def test_production_change_has_prior_approval(self, change_record: dict):
        change_id = change_record.get("change_id")
        approval_date = change_record.get("approval_date")
        deployment_date = change_record.get("production_deployment_date")
        is_emergency = change_record.get("is_emergency_change", False)

        if is_emergency:
            pytest.skip("Emergency changes handled by separate emergency change test")

        assert approval_date is not None, (
            f"Change '{change_id}': no approval date recorded — SOX ITGC requires "
            "documented approval before any production deployment"
        )
        assert approval_date <= deployment_date, (
            f"Change '{change_id}': deployment on {deployment_date} occurred BEFORE "
            f"approval on {approval_date} — all production changes must be approved "
            "before deployment; this is the most commonly tested SOX change management control"
        )

    def test_change_has_test_evidence(self, change_record: dict):
        change_id = change_record.get("change_id")
        test_evidence_reference = change_record.get("test_evidence_reference")

        assert test_evidence_reference is not None, (
            f"Change '{change_id}': no test evidence documented — SOX ITGC requires "
            "evidence that changes were tested in a non-production environment before "
            "deployment; absence of testing documentation is a change management deficiency"
        )

    def test_developer_did_not_deploy_own_code_to_production(self, change_record: dict):
        change_id = change_record.get("change_id")
        developer_id = change_record.get("developer_id")
        deployer_id = change_record.get("production_deployer_id")
        approver_id = change_record.get("approver_id")

        assert deployer_id != developer_id, (
            f"Change '{change_id}': developer '{developer_id}' deployed their own code "
            "to production — SOX ITGC segregation of duties requires that the developer "
            "and the production deployer are different individuals; developer self-deployment "
            "is a significant deficiency in most SOX programs"
        )
        assert approver_id != developer_id, (
            f"Change '{change_id}': developer '{developer_id}' also approved their own "
            "change (approver: {approver_id}) — self-approval violates SOD for change management"
        )

    def test_emergency_change_has_retrospective_approval(self, change_record: dict):
        if not change_record.get("is_emergency_change", False):
            pytest.skip("Not an emergency change")

        change_id = change_record.get("change_id")
        deployment_date = change_record.get("production_deployment_date")
        retrospective_approval_date = change_record.get("retrospective_approval_date")

        assert retrospective_approval_date is not None, (
            f"Emergency change '{change_id}': no retrospective approval on record — "
            "emergency changes must have retrospective documentation and approval after "
            "the fact; emergency changes without any approval evidence are a finding"
        )

        if deployment_date:
            days_to_retro = (retrospective_approval_date - deployment_date).days
            assert days_to_retro <= 5, (
                f"Emergency change '{change_id}': retrospective approval obtained "
                f"{days_to_retro} days after deployment — should be within 5 business days"
            )
```

### Section 2.2 — Development/Test/Production Separation (DETERMINISTIC)

```python
import pytest


class TestEnvironmentSeparation:
    """Pattern 1: DETERMINISTIC — three-environment separation is binary."""

    @pytest.mark.assumption(
        id="ASSUME-SOX-CHANGE-002",
        description=(
            "SOX environment separation: three distinct environments are required — "
            "development, test/QA, and production. 'Separation' means: (1) separate "
            "physical or logical infrastructure, (2) developers do not have write/deploy "
            "access to production, (3) production data is not used in non-production "
            "environments without masking (data privacy overlap with other frameworks). "
            "In cloud/SaaS environments, environment separation is demonstrated by separate "
            "accounts, subscriptions, or namespaces with separate access controls."
        ),
        approved_by="IT Controls / Infrastructure",
        review_date="2026-05-21",
    )
    def test_three_environments_exist(self, itgc_scope: dict):
        environments = itgc_scope.get("defined_environments", [])
        required = {"development", "test", "production"}
        missing = required - {e.get("name", "").lower() for e in environments}
        assert not missing, (
            f"Missing required environments: {sorted(missing)} — SOX ITGC requires "
            "three distinct environments (development, test/QA, production); "
            "absence of environment separation is a significant deficiency"
        )

    def test_developers_lack_production_write_access(self, developer_access_review: dict):
        for developer in developer_access_review.get("developers", []):
            dev_id = developer.get("user_id")
            prod_write_roles = developer.get("production_write_roles", [])
            has_approved_exception = developer.get("production_access_exception_approved", False)

            if not has_approved_exception:
                assert not prod_write_roles, (
                    f"Developer '{dev_id}' has production write/deploy roles: "
                    f"{prod_write_roles} without an approved exception — "
                    "developers must not have write access to production systems; "
                    "this is a foundational SOX change management segregation of duties control"
                )
```

---

## DOMAIN 3 — Computer Operations Controls

### Section 3.1 — Backup Monitoring (DETERMINISTIC)

#### Requirements extracted

| # | Control | Threshold | Evidence |
|---|---------|-----------|---------|
| 3.1.1 | Financial system backup completes daily | All scheduled backup jobs complete successfully | Backup job completion log; failure count = 0 or failures investigated and resolved |
| 3.1.2 | Backup failures investigated | Within 1 business day of failure | Incident/ticket for each backup failure; root cause documented |
| 3.1.3 | Backup restoration test | At least annually (quarterly is better practice) | Restoration test record; data integrity confirmed |

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta

BACKUP_RESTORATION_TEST_INTERVAL_MONTHS = 12


class TestBackupMonitoring:
    """Pattern 1: DETERMINISTIC — backup completion is binary; investigation is required."""

    @pytest.mark.assumption(
        id="ASSUME-SOX-OPS-001",
        description=(
            "SOX backup monitoring: auditors verify that backup jobs for financial systems "
            "complete successfully and that failures are promptly investigated. The existence "
            "of backup completion logs and documented investigation for failures are the "
            "evidence artifacts. Backup restoration testing demonstrates that backups are "
            "usable — completion alone is insufficient evidence of recoverability. Annual "
            "restoration testing is the minimum; critical financial systems should test quarterly."
        ),
        approved_by="IT Operations / IT Controls",
        review_date="2026-05-21",
    )
    def test_no_unresolved_backup_failures_in_period(self, backup_monitoring_report: dict):
        system_id = backup_monitoring_report.get("system_id")
        unresolved_failures = [
            f for f in backup_monitoring_report.get("backup_failures", [])
            if not f.get("investigation_completed", False)
        ]

        assert not unresolved_failures, (
            f"System '{system_id}': {len(unresolved_failures)} backup failure(s) with no "
            "documented investigation — SOX ITGC requires that all backup failures for "
            "financial systems are investigated and root cause documented; unresolved failures "
            "indicate the computer operations monitoring control is not operating effectively"
        )

    def test_backup_restoration_test_not_overdue(self, backup_monitoring_report: dict):
        system_id = backup_monitoring_report.get("system_id")
        last_restoration_test = backup_monitoring_report.get("last_restoration_test_date")

        assert last_restoration_test is not None, (
            f"System '{system_id}': no backup restoration test on record — "
            "SOX ITGC requires periodic restoration testing to demonstrate that backups "
            "are usable; a backup that cannot be restored provides no recovery assurance"
        )

        due_date = last_restoration_test + relativedelta(months=BACKUP_RESTORATION_TEST_INTERVAL_MONTHS)
        today = date.today()
        assert today <= due_date, (
            f"System '{system_id}': annual backup restoration test overdue — "
            f"last test: {last_restoration_test}, due: {due_date}, today: {today}"
        )
```

### Section 3.2 — Audit Log Integrity (DETERMINISTIC)

```python
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta

SOX_LOG_RETENTION_YEARS = 7  # §802 document retention; PCAOB workpaper retention is 7 years


class TestAuditLogIntegrity:
    """Pattern 1: DETERMINISTIC — log existence and retention are binary."""

    @pytest.mark.assumption(
        id="ASSUME-SOX-OPS-002",
        description=(
            "SOX audit log requirements: SOX §802 mandates retention of audit workpapers "
            "for 7 years. While SOX does not explicitly mandate system-level log retention, "
            "PCAOB AS 2201 requires auditors to test that evidence supporting ICFR is "
            "available. In practice, financial system logs are retained for 7 years to support "
            "potential litigation, restatement investigations, or regulatory examinations. "
            "Log integrity (no deletion/modification) is required — logs stored in write-once "
            "or tamper-evident storage satisfy this requirement."
        ),
        approved_by="IT Controls / Legal / Internal Audit",
        review_date="2026-05-21",
    )
    def test_financial_system_audit_logs_retained_7_years(self, log_retention_record: dict):
        system_id = log_retention_record.get("system_id")
        retention_years = log_retention_record.get("configured_retention_years", 0)

        assert retention_years >= SOX_LOG_RETENTION_YEARS, (
            f"System '{system_id}': audit log retention configured for {retention_years} years — "
            f"SOX §802 / PCAOB workpaper retention requires {SOX_LOG_RETENTION_YEARS} years; "
            "insufficient retention means evidence supporting ICFR may not be available for "
            "auditor review or litigation/restatement purposes"
        )

    def test_audit_logs_tamper_evident(self, log_retention_record: dict):
        system_id = log_retention_record.get("system_id")
        tamper_evident = log_retention_record.get("logs_tamper_evident_or_write_once", False)
        assert tamper_evident, (
            f"System '{system_id}': audit logs are not stored in a tamper-evident or "
            "write-once medium — SOX ITGC requires that audit logs cannot be modified or "
            "deleted without detection; logs that can be altered by privileged users without "
            "a separate record undermine the reliability of the audit evidence"
        )
```

---

## DOMAIN 4 — Material Weakness and Deficiency Tracking

```python
import pytest


DEFICIENCY_LEVELS = ("control_deficiency", "significant_deficiency", "material_weakness")


class TestDeficiencyTracking:
    """Pattern 2/3: PARAMETERIZED/CONTESTED — classification requires auditor judgment."""

    @pytest.mark.assumption(
        id="ASSUME-SOX-DEF-001",
        description=(
            "SOX deficiency classification: control deficiencies identified through ITGC "
            "testing must be assessed for potential escalation to significant deficiency or "
            "material weakness. The classification is judgment-based: a material weakness "
            "exists if there is a reasonable possibility that a material misstatement would "
            "not be prevented or detected. 'Reasonable possibility' = more than remote "
            "(PCAOB AS 2201 ¶10). Aggregation of multiple control deficiencies can rise to "
            "a significant deficiency or material weakness even if each individual deficiency "
            "is minor. Classification must be reviewed by management and external auditors."
        ),
        approved_by="Controller / CFO / External Audit",
        review_date="2026-05-21",
    )
    def test_all_identified_deficiencies_have_remediation_plan(self, deficiency_log: dict):
        for deficiency in deficiency_log.get("open_deficiencies", []):
            def_id = deficiency.get("deficiency_id")
            remediation_plan = deficiency.get("remediation_plan")
            target_date = deficiency.get("remediation_target_date")

            assert remediation_plan is not None, (
                f"Deficiency '{def_id}': no remediation plan documented — all identified "
                "SOX ITGC deficiencies must have a written remediation plan with responsible "
                "owner and target completion date"
            )
            assert target_date is not None, (
                f"Deficiency '{def_id}': remediation plan exists but no target date — "
                "remediation plans without target dates are not actionable and will be "
                "cited by external auditors as a management of deficiencies finding"
            )

    @pytest.mark.human_review_required(
        reason=(
            "Material weakness determination: whether a control deficiency (or combination "
            "of deficiencies) rises to a material weakness requires judgment about the "
            "magnitude of potential misstatement and the likelihood that it would not be "
            "prevented or detected by other controls. This requires the Controller, CFO, "
            "and external auditors to assess collectively. No automated test can make this "
            "determination — it is a professional judgment with significant consequences "
            "(public disclosure required for material weaknesses)."
        )
    )
    def test_material_weakness_determination_reviewed_by_management_and_auditors(
        self, deficiency_log: dict
    ):
        potential_mw = [
            d for d in deficiency_log.get("open_deficiencies", [])
            if d.get("classification") in ("significant_deficiency", "material_weakness")
        ]

        for deficiency in potential_mw:
            def_id = deficiency.get("deficiency_id")
            classification = deficiency.get("classification")
            management_reviewed = deficiency.get("management_classification_reviewed", False)
            auditor_reviewed = deficiency.get("external_auditor_reviewed", False)

            assert management_reviewed, (
                f"Deficiency '{def_id}' classified as '{classification}': no management "
                "review of classification on record — significant deficiencies and material "
                "weaknesses must be reviewed and agreed by management before disclosure"
            )
            if classification == "material_weakness":
                assert auditor_reviewed, (
                    f"Deficiency '{def_id}' classified as material weakness: no external "
                    "auditor review on record — material weakness classifications require "
                    "agreement with external auditors as part of §404(b) attestation"
                )
```

---

## Open assumptions

| ID | Section | Summary | Review date |
|---|---|---|---|
| ASSUME-SOX-ACCESS-001 | Provisioning | Approval before access grant; approver ≠ requestor; approved roles must match provisioned roles | 2026-05-21 |
| ASSUME-SOX-ACCESS-002 | Deprovisioning | Privileged: ≤1 business day from termination; standard: ≤5 business days; role change excess: ≤10 business days | 2026-05-21 |
| ASSUME-SOX-ACCESS-003 | Access review | Quarterly for privileged; annual for standard; exceptions remediated within 30 days | 2026-05-21 |
| ASSUME-SOX-ACCESS-004 | SoD | Matrix reviewed annually; active conflicts require approved compensating control or management exception | 2026-05-21 |
| ASSUME-SOX-CHANGE-001 | Change authorization | Approval before deployment; developer ≠ deployer ≠ approver; test evidence required; emergency retro within 5 days | 2026-05-21 |
| ASSUME-SOX-CHANGE-002 | Environment separation | Three environments required; developers lack production write access | 2026-05-21 |
| ASSUME-SOX-OPS-001 | Backup monitoring | Failures investigated within 1 business day; annual restoration test; completion logs required | 2026-05-21 |
| ASSUME-SOX-OPS-002 | Audit log retention | 7-year retention (§802 / PCAOB); tamper-evident or write-once storage | 2026-05-21 |
| ASSUME-SOX-DEF-001 | Deficiency tracking | All deficiencies have remediation plan with target date; MW classification requires management + auditor agreement | 2026-05-21 |

---

## Contested items

| Item | Reason | Resolution path |
|---|---|---|
| Material weakness vs. significant deficiency classification | "Reasonable possibility" and "material" are professional judgment standards; PCAOB has enforcement history showing disagreements | Controller, CFO, and external auditor collective judgment; documentation of aggregation analysis |
| SoD conflict materiality | Whether a specific role combination constitutes a SoD conflict depends on the financial process and compensating controls — there is no universal matrix | Management-approved SoD conflict matrix reviewed annually by Controller; external auditor concurrence |
| Scope determination (key systems) | Whether a system "supports financial reporting" requires judgment about the flow of financial data; scope that is too narrow creates risk of audit exceptions | Annual scope reassessment by management; external auditor agreement on scope |

---

## Cross-standard dependencies

| Artifact | Dependencies |
|---|---|
| Access provisioning tickets | SOC 2 CC6.2, ISO 27001 A.5.18, HIPAA §164.312(a) — same IAM tickets support all frameworks |
| Change management tickets | SOC 2 CC8, PCI DSS Req 6, ISO 27001 A.8.32 — same change tickets used for all framework testing |
| Backup completion logs | SOC 2 A1.2, HIPAA §164.308(a)(7), ISO 27001 A.8.13 — same backup logs used for all frameworks |
| Audit log retention | NY DFS §500.06 (6 years), PCI DSS Req 10 (12 months), SOX §802 (7 years workpapers) — SOX is the longest retention requirement for financial sector |
