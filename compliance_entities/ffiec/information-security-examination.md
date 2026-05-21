# FFIEC IT Examination Handbooks — Information Security & Business Continuity

**Framework:** FFIEC Information Security Handbook (2016/2019 update) + Business Continuity Management Handbook (2019) + TSP Handbook (2012)
**Clauses:** IS Handbook Work Programs 1–5 (governance, risk assessment, controls, monitoring, TSP management); BCM Handbook (BIA, RTO/RPO, annual testing, offsite backup); Rule 3310 (AML) cross-reference
**Confidence:** DETERMINISTIC-dominant (MFA, patch ≤30d, vuln scan ≥quarterly, pentest annual, log retention, BCP annual test, offsite backup, written policies, TSP inventory); PARAMETERIZED (control adequacy, risk assessment methodology, monitoring coverage)
**Last parsed:** 2026-05-21
**Applies to:** Federally regulated US financial institutions — national banks (OCC), federal savings associations (OCC), state member banks (Federal Reserve), bank holding companies (Federal Reserve), state nonmember banks (FDIC), federal credit unions (NCUA); and their technology service providers (TSPs) examined through their institutional clients
**Trigger:** Federal charter or federal deposit insurance triggering examination by an FFIEC member agency (OCC, FDIC, Federal Reserve, NCUA, CFPB); examination benchmarks apply during IT Safety-and-Soundness examinations; findings result in MRAs/MRIAs that carry practical enforcement force
**Jurisdiction:** United States; FFIEC handbooks are the examination framework for federally regulated institutions; state-chartered non-member banks are examined by state authorities but commonly use FFIEC guidance as the reference standard
**Not applicable to:** State-chartered non-member banks not subject to federal examination (though FFIEC guidance is widely referenced); non-bank financial institutions not regulated by FFIEC member agencies; insurance companies (state regulated); fintech companies not holding a federal banking charter or deposit insurance

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def ffiec_scope(entity_profile: dict):
    if not entity_profile.get("ffiec_examined_financial_institution", False):
        pytest.skip("FFIEC IT Examination Handbooks not applicable — not an FFIEC-examined financial institution or TSP")
```

---

## Constants

```python
from datetime import date, timedelta

# Examiner benchmark thresholds — de facto DETERMINISTIC expectations
FFIEC_CRITICAL_PATCH_MAX_DAYS = 30
FFIEC_HIGH_PATCH_MAX_DAYS = 90
FFIEC_VULNERABILITY_SCAN_MAX_INTERVAL_DAYS = 90   # quarterly
FFIEC_PENETRATION_TEST_INTERVAL_MONTHS = 12
FFIEC_LOG_RETENTION_ACCESSIBLE_MONTHS = 12
FFIEC_LOG_RETENTION_TOTAL_MONTHS = 24
FFIEC_RISK_ASSESSMENT_MAX_AGE_MONTHS = 12
FFIEC_BCP_TEST_INTERVAL_MONTHS = 12

# Required elements in written IS policy
FFIEC_IS_POLICY_REQUIRED_ELEMENTS = frozenset({
    "information_security_program_scope",
    "roles_and_responsibilities",
    "risk_assessment_process",
    "access_control_requirements",
    "incident_response_procedures",
    "vendor_management_requirements",
    "training_and_awareness",
    "encryption_requirements",
    "audit_and_logging_requirements",
    "business_continuity_integration",
})

# Required elements in IRP
FFIEC_IRP_REQUIRED_ELEMENTS = frozenset({
    "incident_classification_criteria",
    "roles_and_responsibilities_during_incident",
    "internal_escalation_procedures",
    "external_notification_procedures",
    "evidence_preservation",
    "containment_and_eradication_steps",
    "recovery_procedures",
    "post_incident_review_process",
})

# Required elements in TSP contracts
FFIEC_TSP_CONTRACT_REQUIRED_ELEMENTS = frozenset({
    "security_requirements",
    "audit_rights_or_soc2_provision",
    "incident_notification_obligation",
    "business_continuity_requirements",
    "data_ownership_and_return",
    "right_to_terminate",
})
```

---

## IS Program Governance (IS Handbook Work Program 1)

**Overall: DETERMINISTIC (policy existence) + PARAMETERIZED (adequacy)**

```python
class TestISProgramGovernance:
    """IS Handbook Work Program 1 — Written IS policy; board oversight; named CISO or equivalent; annual review."""

    def test_written_information_security_policy_exists(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("written_information_security_policy_exists", False), (
            "A written information security policy must exist — this is the primary "
            "artifact reviewed during FFIEC IS examination (IS Handbook Work Program 1)"
        )

    def test_is_policy_contains_required_elements(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        present = set(ffiec.get("is_policy_elements_present", []))
        missing = FFIEC_IS_POLICY_REQUIRED_ELEMENTS - present
        assert not missing, (
            f"Written IS policy is missing required elements: {missing} "
            f"(FFIEC IS Handbook Work Program 1)"
        )

    def test_board_or_senior_management_approves_is_program(
        self, controls_evidence: dict
    ):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("board_or_senior_mgmt_approves_is_program", False), (
            "The IS program must be approved by the board of directors or senior "
            "management, with documented evidence of approval "
            "(FFIEC IS Handbook Work Program 1)"
        )

    def test_is_policy_reviewed_within_past_12_months(
        self, controls_evidence: dict, reference_date: date
    ):
        ffiec = controls_evidence.get("ffiec", {})
        last_review = ffiec.get("is_policy_last_review_date")
        assert last_review is not None, (
            "IS policy must have a documented review date "
            "(FFIEC IS Handbook Work Program 1)"
        )
        cutoff = reference_date - timedelta(days=FFIEC_RISK_ASSESSMENT_MAX_AGE_MONTHS * 30)
        assert last_review >= cutoff, (
            f"IS policy must be reviewed at least annually. "
            f"Last reviewed: {last_review} (FFIEC IS Handbook Work Program 1)"
        )

    def test_ciso_or_equivalent_designated(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("ciso_or_equivalent_designated", False), (
            "A CISO or equivalent senior IS officer must be designated with "
            "documented responsibility for the IS program "
            "(FFIEC IS Handbook Work Program 1)"
        )
```

---

## Information Security Risk Assessment (IS Handbook Work Program 2)

**Overall: DETERMINISTIC (written assessment exists, annual update) + PARAMETERIZED (methodology)**

```python
class TestISRiskAssessment:
    """IS Handbook Work Program 2 — Written risk assessment exists; updated at least annually or upon material change."""

    def test_written_risk_assessment_exists(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("written_information_security_risk_assessment_exists", False), (
            "A written information security risk assessment must exist; "
            "examiners verify the document during examination "
            "(FFIEC IS Handbook Work Program 2)"
        )

    def test_risk_assessment_current(
        self, controls_evidence: dict, reference_date: date
    ):
        ffiec = controls_evidence.get("ffiec", {})
        last_assessment = ffiec.get("risk_assessment_last_completed")
        assert last_assessment is not None, (
            "Risk assessment must have a documented completion date "
            "(FFIEC IS Handbook Work Program 2)"
        )
        cutoff = reference_date - timedelta(days=FFIEC_RISK_ASSESSMENT_MAX_AGE_MONTHS * 30)
        assert last_assessment >= cutoff, (
            f"IS risk assessment must be updated at least annually or upon "
            f"significant change. Last completed: {last_assessment} "
            f"(FFIEC IS Handbook Work Program 2)"
        )

    def test_risk_assessment_covers_threats_vulnerabilities_impacts(
        self, controls_evidence: dict
    ):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("risk_assessment_covers_threats_vulnerabilities_impacts", False), (
            "Risk assessment must identify threats, vulnerabilities, and business "
            "impact — not just a control inventory "
            "(FFIEC IS Handbook Work Program 2)"
        )
```

---

## Access Controls (IS Handbook Work Program 3)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestAccessControls:
    """IS Handbook Work Program 3 — Unique IDs; MFA for remote access and privileged accounts; access review."""

    def test_no_shared_accounts_for_privileged_access(
        self, controls_evidence: dict
    ):
        ffiec = controls_evidence.get("ffiec", {})
        assert not ffiec.get("shared_privileged_accounts_in_use", False), (
            "Shared accounts must not be used for privileged access — each "
            "administrator must have an individual account for accountability "
            "(FFIEC IS Handbook Work Program 3)"
        )

    def test_mfa_for_remote_access(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("mfa_enforced_for_remote_access", False), (
            "Multi-factor authentication must be required for all remote access to "
            "institution systems — this is a FFIEC examiner non-negotiable "
            "(FFIEC IS Handbook Work Program 3; Regulatory Notice FIL-50-2019)"
        )

    def test_mfa_for_privileged_accounts(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("mfa_enforced_for_privileged_accounts", False), (
            "Multi-factor authentication must be required for all privileged "
            "accounts, including network and system administrators "
            "(FFIEC IS Handbook Work Program 3)"
        )

    def test_access_reviews_conducted_periodically(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("access_reviews_conducted_periodically", False), (
            "Periodic user access reviews must be conducted to verify that access "
            "rights remain appropriate and terminated employees are removed "
            "(FFIEC IS Handbook Work Program 3)"
        )
```

---

## Patch Management (IS Handbook Work Program 3)

**Overall: DETERMINISTIC — Pattern 1 (with examiner benchmark thresholds)**

```python
class TestPatchManagement:
    """IS Handbook Work Program 3 — Critical patches applied within 30 days; tracked via formal process."""

    def test_patch_management_process_documented(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("patch_management_process_documented", False), (
            "A documented patch management process must exist with defined "
            "timelines for critical, high, and lower severity patches "
            "(FFIEC IS Handbook Work Program 3)"
        )

    def test_critical_patches_applied_within_30_days(self, controls_evidence: dict):
        patches = controls_evidence.get("ffiec_patches", [])
        overdue = [
            p for p in patches
            if p.get("severity") == "critical"
            and p.get("days_to_apply", 0) > FFIEC_CRITICAL_PATCH_MAX_DAYS
        ]
        assert not overdue, (
            f"Critical patches must be applied within {FFIEC_CRITICAL_PATCH_MAX_DAYS} "
            f"days — this is the examiner benchmark threshold. "
            f"Overdue: {[p['patch_id'] for p in overdue]} "
            f"(FFIEC IS Handbook Work Program 3)"
        )

    def test_high_patches_applied_within_90_days(self, controls_evidence: dict):
        patches = controls_evidence.get("ffiec_patches", [])
        overdue = [
            p for p in patches
            if p.get("severity") == "high"
            and p.get("days_to_apply", 0) > FFIEC_HIGH_PATCH_MAX_DAYS
        ]
        assert not overdue, (
            f"High-severity patches must be applied within {FFIEC_HIGH_PATCH_MAX_DAYS} "
            f"days. Overdue: {[p['patch_id'] for p in overdue]} "
            f"(FFIEC IS Handbook Work Program 3)"
        )
```

---

## Vulnerability Scanning and Penetration Testing (IS Handbook Work Program 4)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestVulnerabilityAndPenetrationTesting:
    """IS Handbook Work Program 4 — Quarterly vuln scans; annual pentest (internal + external network + application)."""

    def test_vulnerability_scanning_at_least_quarterly(
        self, controls_evidence: dict, reference_date: date
    ):
        ffiec = controls_evidence.get("ffiec", {})
        last_scan = ffiec.get("last_vulnerability_scan_date")
        assert last_scan is not None, (
            "No vulnerability scan date on record — examiners require evidence "
            "of periodic scanning (FFIEC IS Handbook Work Program 4)"
        )
        cutoff = reference_date - timedelta(days=FFIEC_VULNERABILITY_SCAN_MAX_INTERVAL_DAYS)
        assert last_scan >= cutoff, (
            f"Vulnerability scans must be conducted at least quarterly. "
            f"Last scan: {last_scan} — exceeds {FFIEC_VULNERABILITY_SCAN_MAX_INTERVAL_DAYS}-day "
            f"window (FFIEC IS Handbook Work Program 4)"
        )

    def test_penetration_test_conducted_annually(
        self, controls_evidence: dict, reference_date: date
    ):
        ffiec = controls_evidence.get("ffiec", {})
        last_pentest = ffiec.get("last_penetration_test_date")
        assert last_pentest is not None, (
            "No penetration test date on record — examiners require annual "
            "penetration testing evidence (FFIEC IS Handbook Work Program 4)"
        )
        cutoff = reference_date - timedelta(days=FFIEC_PENETRATION_TEST_INTERVAL_MONTHS * 30)
        assert last_pentest >= cutoff, (
            f"Penetration test must be conducted at least annually. "
            f"Last tested: {last_pentest} (FFIEC IS Handbook Work Program 4)"
        )

    def test_penetration_test_covers_internal_and_external_scope(
        self, controls_evidence: dict
    ):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("pentest_covers_internal_network", False), (
            "Penetration test scope must include internal network testing "
            "(FFIEC IS Handbook Work Program 4)"
        )
        assert ffiec.get("pentest_covers_external_network", False), (
            "Penetration test scope must include external perimeter testing "
            "(FFIEC IS Handbook Work Program 4)"
        )
        assert ffiec.get("pentest_covers_applications", False), (
            "Penetration test scope must include internet-facing and critical "
            "internal applications (FFIEC IS Handbook Work Program 4)"
        )

    def test_pentest_findings_remediated(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("pentest_findings_remediation_tracked", False), (
            "Penetration test findings must be tracked to remediation with "
            "defined timelines — open critical findings require exception approval "
            "(FFIEC IS Handbook Work Program 4)"
        )
```

---

## Logging and Monitoring (IS Handbook Work Program 4)

**Overall: DETERMINISTIC (log retention duration) + PARAMETERIZED (monitoring coverage)**

```python
class TestLoggingAndMonitoring:
    """IS Handbook Work Program 4 — Logs retained 12mo accessible / 24mo total; security event monitoring."""

    def test_security_event_logging_enabled(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("security_event_logging_enabled_on_critical_systems", False), (
            "Security event logging must be enabled on all critical systems including "
            "authentication events, privileged access, and network boundary activity "
            "(FFIEC IS Handbook Work Program 4)"
        )

    def test_log_retention_meets_12_month_accessible_benchmark(
        self, controls_evidence: dict
    ):
        ffiec = controls_evidence.get("ffiec", {})
        accessible_months = ffiec.get("log_retention_accessible_months", 0)
        assert accessible_months >= FFIEC_LOG_RETENTION_ACCESSIBLE_MONTHS, (
            f"Logs must be retained in an immediately accessible state for at least "
            f"{FFIEC_LOG_RETENTION_ACCESSIBLE_MONTHS} months (examiner benchmark). "
            f"Current: {accessible_months} months "
            f"(FFIEC IS Handbook Work Program 4)"
        )

    def test_log_retention_meets_24_month_total_benchmark(
        self, controls_evidence: dict
    ):
        ffiec = controls_evidence.get("ffiec", {})
        total_months = ffiec.get("log_retention_total_months", 0)
        assert total_months >= FFIEC_LOG_RETENTION_TOTAL_MONTHS, (
            f"Total log retention (accessible + archive) must be at least "
            f"{FFIEC_LOG_RETENTION_TOTAL_MONTHS} months (examiner benchmark). "
            f"Current: {total_months} months "
            f"(FFIEC IS Handbook Work Program 4)"
        )
```

---

## Incident Response Plan (IS Handbook Work Program 3)

**Overall: DETERMINISTIC (IRP exists, tested annually) + PARAMETERIZED (adequacy)**

```python
class TestIncidentResponsePlan:
    """IS Handbook Work Program 3 — Written IRP with required elements; tested at least annually."""

    def test_written_irp_exists(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("written_incident_response_plan_exists", False), (
            "A written Incident Response Plan must exist; this is reviewed during "
            "every FFIEC IS examination (IS Handbook Work Program 3)"
        )

    def test_irp_contains_required_elements(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        present = set(ffiec.get("irp_elements_present", []))
        missing = FFIEC_IRP_REQUIRED_ELEMENTS - present
        assert not missing, (
            f"Incident Response Plan is missing required elements: {missing} "
            f"(FFIEC IS Handbook Work Program 3)"
        )

    def test_irp_tested_annually(
        self, controls_evidence: dict, reference_date: date
    ):
        ffiec = controls_evidence.get("ffiec", {})
        last_test = ffiec.get("irp_last_tested_date")
        assert last_test is not None, (
            "IRP must be tested; no test date on record "
            "(FFIEC IS Handbook Work Program 3)"
        )
        cutoff = reference_date - timedelta(days=FFIEC_BCP_TEST_INTERVAL_MONTHS * 30)
        assert last_test >= cutoff, (
            f"IRP must be tested at least annually via tabletop or exercise. "
            f"Last tested: {last_test} (FFIEC IS Handbook Work Program 3)"
        )
```

---

## Third-Party / TSP Management (FFIEC TSP Handbook)

**Overall: DETERMINISTIC (TSP inventory, contract elements) + PARAMETERIZED (due diligence adequacy)**

```python
class TestThirdPartyManagement:
    """FFIEC TSP Handbook — Written TSP inventory; contracts with required elements; annual SOC 2 review."""

    def test_written_tsp_inventory_exists(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("written_tsp_inventory_exists", False), (
            "A written inventory of all technology service providers with access "
            "to institution systems or customer data must exist "
            "(FFIEC TSP Handbook)"
        )

    def test_tsp_contracts_contain_required_elements(self, controls_evidence: dict):
        tsps = controls_evidence.get("ffiec_tsps", [])
        for tsp in tsps:
            if not tsp.get("critical_or_high_risk", False):
                continue
            contract_elements = set(tsp.get("contract_elements_present", []))
            missing = FFIEC_TSP_CONTRACT_REQUIRED_ELEMENTS - contract_elements
            assert not missing, (
                f"TSP '{tsp['tsp_id']}' contract is missing required elements: "
                f"{missing} (FFIEC TSP Handbook)"
            )

    def test_critical_tsps_have_annual_soc2_or_equivalent_review(
        self, controls_evidence: dict, reference_date: date
    ):
        tsps = controls_evidence.get("ffiec_tsps", [])
        for tsp in tsps:
            if not tsp.get("critical_or_high_risk", False):
                continue
            last_review = tsp.get("soc2_or_equivalent_review_date")
            assert last_review is not None, (
                f"Critical TSP '{tsp['tsp_id']}' has no SOC 2 or equivalent "
                f"review on record (FFIEC TSP Handbook)"
            )
            cutoff = reference_date - timedelta(days=FFIEC_RISK_ASSESSMENT_MAX_AGE_MONTHS * 30)
            assert last_review >= cutoff, (
                f"Critical TSP '{tsp['tsp_id']}' SOC 2/equivalent review is "
                f"older than 12 months. Last reviewed: {last_review} "
                f"(FFIEC TSP Handbook)"
            )
```

---

## Business Continuity (FFIEC BCM Handbook 2019)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestBusinessContinuity:
    """FFIEC BCM Handbook 2019 — Board-approved BCP; written BIA; offsite backup; documented RTO/RPO; annual test."""

    def test_board_approved_bcp_exists(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("board_approved_bcp_exists", False), (
            "A Business Continuity Plan must exist and be approved by the board "
            "of directors (FFIEC BCM Handbook 2019)"
        )

    def test_written_bia_exists_and_is_current(
        self, controls_evidence: dict, reference_date: date
    ):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("written_bia_exists", False), (
            "A written Business Impact Analysis must exist "
            "(FFIEC BCM Handbook 2019)"
        )
        last_bia_update = ffiec.get("bia_last_updated")
        if last_bia_update is not None:
            cutoff = reference_date - timedelta(days=FFIEC_RISK_ASSESSMENT_MAX_AGE_MONTHS * 30)
            assert last_bia_update >= cutoff, (
                f"BIA must be updated at least annually or after significant change. "
                f"Last updated: {last_bia_update} (FFIEC BCM Handbook 2019)"
            )

    def test_rto_rpo_defined_for_critical_systems(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("rto_rpo_defined_for_critical_systems", False), (
            "Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO) "
            "must be defined for all critical business functions and systems "
            "(FFIEC BCM Handbook 2019)"
        )

    def test_offsite_backup_exists_for_critical_data(self, controls_evidence: dict):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("offsite_backup_exists_for_critical_data", False), (
            "Offsite (geographically separate) backup must exist for all critical "
            "data — backup co-located with primary site does not satisfy this "
            "requirement (FFIEC BCM Handbook 2019)"
        )

    def test_bcp_tested_annually(
        self, controls_evidence: dict, reference_date: date
    ):
        ffiec = controls_evidence.get("ffiec", {})
        last_test = ffiec.get("bcp_last_full_test_date")
        assert last_test is not None, (
            "BCP must be tested; no test date on record "
            "(FFIEC BCM Handbook 2019)"
        )
        cutoff = reference_date - timedelta(days=FFIEC_BCP_TEST_INTERVAL_MONTHS * 30)
        assert last_test >= cutoff, (
            f"BCP must be tested at least annually. "
            f"Last tested: {last_test} (FFIEC BCM Handbook 2019)"
        )

    def test_bcp_test_results_documented_with_remediation(
        self, controls_evidence: dict
    ):
        ffiec = controls_evidence.get("ffiec", {})
        assert ffiec.get("bcp_test_results_documented_with_remediation_plan", False), (
            "BCP test results must be documented and gaps identified during testing "
            "must have remediation plans (FFIEC BCM Handbook 2019)"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|

*(No open assumptions — all FFIEC spec tests use DETERMINISTIC examiner benchmarks or check the binary existence of required documents; IS program adequacy and monitoring coverage are scoped out as PARAMETERIZED and not asserted here)*
