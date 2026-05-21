# NIST CSF 2.0 — Function Profiles & Subcategory Tests
## NIST Special Publication CSWP 29 (February 2024)

**Scope:** Six Functions — GV (Govern), ID (Identify), PR (Protect), DE (Detect), RS (Respond), RC (Recover)
**Note:** CSF 2.0 is outcomes-based and voluntary. Tests assert Current Profile ≥ Target Profile for each subcategory. DETERMINISTIC tests apply where binary presence or measurable thresholds exist; most subcategories are PARAMETERIZED or CONTESTED.

---

## RDF extraction

### Profile gap (master pattern)

```
Subject:    Any organization that has adopted NIST CSF 2.0
Condition:  Organization has defined a Target Profile
Obligation: Current Profile achievement must meet or exceed Target Profile for each subcategory
Evidence:   Documented Current Profile + Target Profile; gap assessment with remediation plan for gaps
```

---

## Constants

```python
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# Patch management SLAs — ASSUME-CSF-PATCH-001
PATCH_SLA_DAYS = {
    "critical_kev":  14,   # CISA Known Exploited Vulnerabilities catalog
    "critical":      30,   # CVSS 9.0–10.0, not in KEV
    "high":          60,   # CVSS 7.0–8.9
    "medium":        90,   # CVSS 4.0–6.9
    "low":          180,   # CVSS 0.1–3.9
}

# Access review cadences — ASSUME-CSF-ACCESS-001
PRIVILEGED_ACCESS_REVIEW_MONTHS  = 3    # quarterly
STANDARD_ACCESS_REVIEW_MONTHS    = 12   # annual

# Training — ASSUME-CSF-TRAIN-001
AWARENESS_TRAINING_MONTHS = 12          # annual minimum
PRIVILEGED_ROLE_TRAINING_MONTHS = 12    # annual + at onboarding

# Asset review — ASSUME-CSF-ASSET-001
ASSET_INVENTORY_REVIEW_MONTHS = 12      # annual reconciliation minimum

# Risk assessment — annual refresh
RISK_ASSESSMENT_REFRESH_MONTHS = 12

# Incident response plan review
IRP_REVIEW_MONTHS = 12
IRP_TEST_MONTHS   = 12                  # tabletop or simulation annually

# Recovery plan test
RECOVERY_PLAN_TEST_MONTHS = 12

# CSF Target Profile achievement levels (1=partial, 2=risk-informed, 3=repeatable, 4=adaptive)
MIN_TARGET_TIER = 1
MAX_TARGET_TIER = 4
```

---

## Scope pre-condition fixture

```python
import pytest

@pytest.fixture(autouse=True)
def csf_adoption_check(entity_profile: dict):
    """Skip CSF tests if the organization has not adopted NIST CSF 2.0."""
    if not entity_profile.get("csf2_adopted", False):
        pytest.skip("Organization has not adopted NIST CSF 2.0 — CSF tests not applicable")
```

---

## Profile framework

### Target Profile existence (Pattern 1 — DETERMINISTIC)

```python
def test_csf_target_profile_documented(
    controls_evidence: dict,
):
    """An organization adopting CSF 2.0 must document a Target Profile describing
    the desired cybersecurity outcomes for each applicable subcategory."""
    profile = controls_evidence.get("csf_profiles", {})
    assert profile, "No CSF profile documentation found in evidence"
    assert profile.get("target_profile"), "No Target Profile documented"
    assert profile.get("target_profile_date"), "Target Profile lacks a review/approval date"
    target = profile["target_profile"]
    assert len(target) >= 10, (
        f"Target Profile covers only {len(target)} subcategories — a meaningful profile "
        "should address all applicable subcategories across the six functions"
    )
```

### Current Profile vs Target Profile gap (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-CSF-PROFILE-001",
    description=(
        "Target Profile represents the organization's documented risk management decisions. "
        "Tests assert Current ≥ Target for each subcategory. Whether the Target Profile itself "
        "is ambitious enough relative to the organization's threat environment is Pattern 3 — "
        "requires CISO / Risk Committee approval."
    ),
    approved_by="CISO",
    review_date="2027-02",
)
def test_csf_profile_gap_assessed_and_remediation_planned(
    controls_evidence: dict,
    reference_date: date,
):
    """
    For each subcategory where Current Profile < Target Profile, a remediation item
    with owner and target date must exist.
    """
    profile = controls_evidence.get("csf_profiles", {})
    if not profile:
        pytest.skip("No CSF profile documentation in evidence")

    current = profile.get("current_profile", {})
    target  = profile.get("target_profile", {})
    gaps    = {k: (current.get(k, 0), target[k]) for k in target if current.get(k, 0) < target[k]}

    if not gaps:
        return  # no gaps — pass

    remediation = controls_evidence.get("csf_remediation_plan", {})
    assert remediation, (
        f"CSF profile gaps identified in {len(gaps)} subcategories {list(gaps.keys())} "
        "but no remediation plan found in evidence."
    )
    unplanned = [sc for sc in gaps if sc not in remediation]
    assert not unplanned, (
        f"No remediation plan entries for subcategories with gaps: {unplanned}"
    )
    overdue = [
        sc for sc in gaps
        if remediation.get(sc, {}).get("target_date") and
           date.fromisoformat(str(remediation[sc]["target_date"])) < reference_date and
           remediation[sc].get("status") != "completed"
    ]
    assert not overdue, (
        f"Overdue CSF remediation items (target date passed, not completed): {overdue}"
    )
```

---

## GV — Govern

### GV.OC — Organizational Context (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-CSF-PROFILE-001",
    description="GV adequacy is Pattern 2 — Risk Committee must review annually.",
    approved_by="Risk Committee",
    review_date="2027-02",
)
def test_gv_oc_legal_regulatory_requirements_identified(
    controls_evidence: dict,
    reference_date: date,
):
    """
    GV.OC-03: Legal, regulatory, and contractual cybersecurity requirements are
    understood and documented. This is the mapping point for all other frameworks
    in this registry — a gap here means downstream framework tests may be scoped
    incorrectly.
    """
    gv = controls_evidence.get("csf_govern", {})
    legal_reqs = gv.get("legal_regulatory_requirements", {}) if gv else {}
    assert legal_reqs, "GV.OC-03: No legal/regulatory requirements documentation found"
    assert legal_reqs.get("last_review_date"), "Legal/regulatory requirements lack a review date"
    last_review = date.fromisoformat(str(legal_reqs["last_review_date"]))
    age_months = (reference_date - last_review).days / 30.44
    assert age_months <= RISK_ASSESSMENT_REFRESH_MONTHS, (
        f"Legal/regulatory requirements last reviewed {age_months:.0f} months ago "
        f"(threshold: {RISK_ASSESSMENT_REFRESH_MONTHS} months)"
    )
```

### GV.RM — Risk Management Strategy (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-CSF-PROFILE-001",
    description="Risk tolerance is org-defined and Pattern 2.",
    approved_by="Risk Committee",
    review_date="2027-02",
)
def test_gv_rm_risk_tolerance_documented_and_approved(
    controls_evidence: dict,
):
    """GV.RM-02: Risk appetite and tolerance are established, communicated, and
    reviewed by senior leadership."""
    gv = controls_evidence.get("csf_govern", {})
    risk_strategy = gv.get("risk_management_strategy", {}) if gv else {}
    assert risk_strategy, "GV.RM-02: No risk management strategy documentation found"
    assert risk_strategy.get("risk_tolerance_statement"), "Risk tolerance statement not documented"
    assert risk_strategy.get("approved_by"), "Risk tolerance lacks senior leadership approval"
    assert risk_strategy.get("approval_date"), "Risk tolerance approval lacks a date"
```

### GV.SC — Supply Chain Risk Management (Pattern 2 — PARAMETERIZED)

```python
def test_gv_sc_supply_chain_cybersecurity_requirements_in_contracts(
    controls_evidence: dict,
):
    """
    GV.SC-06: Cybersecurity requirements are included in contracts with suppliers
    and third-party service providers. Pattern 2 — adequacy of requirements
    assessed by procurement / legal.
    """
    gv = controls_evidence.get("csf_govern", {})
    sc_program = gv.get("supply_chain_risk_management", {}) if gv else {}
    assert sc_program, "GV.SC: No supply chain risk management program documentation found"
    assert sc_program.get("contract_requirements_defined"), (
        "GV.SC-06: Cybersecurity requirements for supplier contracts not documented"
    )
    assert sc_program.get("critical_suppliers_identified"), (
        "GV.SC-02: Critical suppliers not identified in supply chain program"
    )
```

---

## ID — Identify

### ID.AM — Asset Management (Pattern 1 — DETERMINISTIC for inventory existence)

```python
def test_id_am_asset_inventory_exists_and_is_current(
    controls_evidence: dict,
    reference_date: date,
):
    """
    ID.AM-01/02: Inventories of hardware and software assets are maintained.
    Inventory existence is DETERMINISTIC; completeness is PARAMETERIZED.
    ASSUME-CSF-ASSET-001: annual reconciliation is the minimum cadence.
    """
    id_evidence = controls_evidence.get("csf_identify", {})
    asset_inventory = id_evidence.get("asset_inventory", {}) if id_evidence else {}
    assert asset_inventory, "ID.AM-01: No asset inventory found in evidence"

    hw_inventory = asset_inventory.get("hardware_inventory")
    sw_inventory = asset_inventory.get("software_inventory")
    assert hw_inventory, "ID.AM-01: No hardware asset inventory documented"
    assert sw_inventory, "ID.AM-02: No software asset inventory documented"

    last_review = asset_inventory.get("last_reconciliation_date")
    assert last_review, "Asset inventory lacks a reconciliation date"
    last_review_date = date.fromisoformat(str(last_review))
    age_months = (reference_date - last_review_date).days / 30.44
    assert age_months <= ASSET_INVENTORY_REVIEW_MONTHS, (
        f"Asset inventory last reconciled {age_months:.0f} months ago "
        f"(threshold: {ASSET_INVENTORY_REVIEW_MONTHS} months)"
    )


def test_id_am_network_map_exists(controls_evidence: dict):
    """ID.AM-03/04: Network maps showing communication flows and data flows exist."""
    id_evidence = controls_evidence.get("csf_identify", {})
    asset_inventory = id_evidence.get("asset_inventory", {}) if id_evidence else {}
    assert asset_inventory.get("network_map"), "ID.AM-03: No network map found in evidence"
    assert asset_inventory.get("data_flow_diagram"), "ID.AM-04: No data flow diagram found in evidence"
```

### ID.RA — Risk Assessment (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-CSF-PROFILE-001",
    description="Risk assessment adequacy is Pattern 2 — CISO must review annually.",
    approved_by="CISO",
    review_date="2027-02",
)
def test_id_ra_risk_assessment_current(
    controls_evidence: dict,
    reference_date: date,
):
    """ID.RA-01: Vulnerabilities are identified, analyzed, and managed. Risk
    assessment refreshed at least annually."""
    id_evidence = controls_evidence.get("csf_identify", {})
    risk_assessment = id_evidence.get("risk_assessment", {}) if id_evidence else {}
    assert risk_assessment, "ID.RA: No risk assessment found in evidence"

    last_updated = risk_assessment.get("last_updated")
    assert last_updated, "Risk assessment lacks a last-updated date"
    last_updated_date = date.fromisoformat(str(last_updated))
    age_months = (reference_date - last_updated_date).days / 30.44
    assert age_months <= RISK_ASSESSMENT_REFRESH_MONTHS, (
        f"Risk assessment last updated {age_months:.0f} months ago "
        f"(threshold: {RISK_ASSESSMENT_REFRESH_MONTHS} months)"
    )
    assert risk_assessment.get("threat_intelligence_sources"), (
        "ID.RA-02: No threat intelligence sources documented in risk assessment"
    )
```

---

## PR — Protect

### PR.AA — Identity Management, Authentication, and Access Control

```python
def test_pr_aa_mfa_enforced_for_privileged_and_remote_access(
    controls_evidence: dict,
):
    """
    PR.AA-03: Authentication commensurate with risk — MFA required for all
    privileged accounts and all remote access. DETERMINISTIC: binary check.
    Maps to: NIST 800-53 IA-2(1)(2), ISO 27001 A.8.5, SOC 2 CC6.1.
    """
    pr_evidence = controls_evidence.get("csf_protect", {})
    access_control = pr_evidence.get("access_control", {}) if pr_evidence else {}
    assert access_control, "PR.AA: No access control evidence found"
    assert access_control.get("mfa_privileged_enforced", False), (
        "PR.AA-03: MFA not enforced for privileged accounts"
    )
    assert access_control.get("mfa_remote_access_enforced", False), (
        "PR.AA-03: MFA not enforced for remote access"
    )


def test_pr_aa_privileged_access_reviewed_quarterly(
    controls_evidence: dict,
    reference_date: date,
):
    """
    PR.AA-05: Access is granted, managed, and revoked based on need.
    ASSUME-CSF-ACCESS-001: Privileged access reviewed at least quarterly (3 months).
    Maps to: NIST 800-53 AC-2(3), ISO 27001 A.5.18.
    """
    pr_evidence = controls_evidence.get("csf_protect", {})
    access_control = pr_evidence.get("access_control", {}) if pr_evidence else {}
    privileged_review = access_control.get("privileged_access_last_review")
    assert privileged_review, "PR.AA-05: No privileged access review date found"
    review_date = date.fromisoformat(str(privileged_review))
    age_months = (reference_date - review_date).days / 30.44
    assert age_months <= PRIVILEGED_ACCESS_REVIEW_MONTHS, (
        f"Privileged access review is {age_months:.1f} months old "
        f"(threshold: {PRIVILEGED_ACCESS_REVIEW_MONTHS} months / quarterly)"
    )


def test_pr_aa_standard_access_reviewed_annually(
    controls_evidence: dict,
    reference_date: date,
):
    """
    PR.AA-05: Standard (non-privileged) user access reviewed at least annually.
    Maps to: NIST 800-53 AC-2, ISO 27001 A.5.18.
    """
    pr_evidence = controls_evidence.get("csf_protect", {})
    access_control = pr_evidence.get("access_control", {}) if pr_evidence else {}
    standard_review = access_control.get("standard_access_last_review")
    assert standard_review, "PR.AA-05: No standard access review date found"
    review_date = date.fromisoformat(str(standard_review))
    age_months = (reference_date - review_date).days / 30.44
    assert age_months <= STANDARD_ACCESS_REVIEW_MONTHS, (
        f"Standard access review is {age_months:.1f} months old "
        f"(threshold: {STANDARD_ACCESS_REVIEW_MONTHS} months / annual)"
    )
```

### PR.AT — Awareness and Training (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-CSF-TRAIN-001",
    description=(
        "Annual cybersecurity awareness training is the minimum cadence. "
        "Privileged users receive role-specific training at onboarding and annually. "
        "Training content adequacy is Pattern 2 — CISO / Security team must review."
    ),
    approved_by="CISO",
    review_date="2027-02",
)
def test_pr_at_awareness_training_completed_annually(
    controls_evidence: dict,
    reference_date: date,
):
    """
    PR.AT-01: Personnel receive awareness and training. Annual completion
    rate tracked. Maps to: NIST 800-53 AT-2, ISO 27001 A.6.3.
    """
    pr_evidence = controls_evidence.get("csf_protect", {})
    training = pr_evidence.get("awareness_training", {}) if pr_evidence else {}
    assert training, "PR.AT: No awareness training records found"

    last_training_cycle = training.get("last_cycle_completion_date")
    assert last_training_cycle, "No training completion date found"
    training_date = date.fromisoformat(str(last_training_cycle))
    age_months = (reference_date - training_date).days / 30.44
    assert age_months <= AWARENESS_TRAINING_MONTHS, (
        f"Awareness training last completed {age_months:.0f} months ago "
        f"(threshold: {AWARENESS_TRAINING_MONTHS} months)"
    )
    completion_rate = training.get("completion_rate_percent", 0)
    assert completion_rate >= 95, (
        f"Awareness training completion rate {completion_rate}% is below 95% threshold"
    )
```

### PR.DS — Data Security (Pattern 1 — DETERMINISTIC for encryption; PARAMETERIZED for classification)

```python
def test_pr_ds_data_at_rest_encryption_for_sensitive_data(
    controls_evidence: dict,
):
    """
    PR.DS-01: Data-at-rest is protected. Encryption of sensitive/critical data
    is DETERMINISTIC — binary check. Classification scheme adequacy is PARAMETERIZED.
    Maps to: NIST 800-53 SC-28, ISO 27001 A.8.24, PCI DSS Req 3, SOC 2 CC6.7.
    """
    pr_evidence = controls_evidence.get("csf_protect", {})
    data_security = pr_evidence.get("data_security", {}) if pr_evidence else {}
    assert data_security, "PR.DS: No data security controls evidence found"
    assert data_security.get("sensitive_data_at_rest_encrypted", False), (
        "PR.DS-01: Sensitive data at rest is not encrypted"
    )


def test_pr_ds_data_in_transit_encryption(
    controls_evidence: dict,
):
    """
    PR.DS-02: Data-in-transit is protected. TLS/encryption of data in transit
    is DETERMINISTIC — binary check.
    Maps to: NIST 800-53 SC-8, ISO 27001 A.8.24, PCI DSS Req 4.
    """
    pr_evidence = controls_evidence.get("csf_protect", {})
    data_security = pr_evidence.get("data_security", {}) if pr_evidence else {}
    assert data_security.get("data_in_transit_encrypted", False), (
        "PR.DS-02: Data in transit is not encrypted (TLS required)"
    )
```

### PR.PS — Platform Security (Pattern 1 — DETERMINISTIC for patch SLAs)

```python
def test_pr_ps_configuration_baselines_exist(
    controls_evidence: dict,
):
    """
    PR.PS-01: Configuration management practices are established.
    Hardened baselines exist for servers, endpoints, and network devices.
    Maps to: NIST 800-53 CM-6, ISO 27001 A.8.9, CIS Benchmarks.
    """
    pr_evidence = controls_evidence.get("csf_protect", {})
    platform_security = pr_evidence.get("platform_security", {}) if pr_evidence else {}
    assert platform_security, "PR.PS: No platform security evidence found"
    assert platform_security.get("configuration_baselines_defined", False), (
        "PR.PS-01: No hardened configuration baselines documented"
    )
    baseline_types = frozenset(platform_security.get("baseline_types", []))
    required_types = frozenset({"servers", "endpoints"})
    missing = required_types - baseline_types
    assert not missing, f"PR.PS-01: Missing configuration baselines for: {missing}"


def test_pr_ps_patch_management_within_sla(
    controls_evidence: dict,
    reference_date: date,
):
    """
    PR.PS-02: Software is maintained. Patches applied within defined SLA.
    ASSUME-CSF-PATCH-001: CISA KEV = 14 days; Critical = 30; High = 60; Medium = 90.
    Maps to: NIST 800-53 SI-2, ISO 27001 A.8.8, SOC 2 CC7.1.
    """
    pr_evidence = controls_evidence.get("csf_protect", {})
    platform_security = pr_evidence.get("platform_security", {}) if pr_evidence else {}
    open_vulns = platform_security.get("open_vulnerabilities", [])
    if not open_vulns:
        pytest.skip("No open vulnerabilities in evidence — patch SLA test not applicable")

    violations = []
    for vuln in open_vulns:
        severity = vuln.get("severity", "medium").lower()
        in_kev = vuln.get("in_cisa_kev", False)
        sla_key = "critical_kev" if in_kev else severity
        sla_days = PATCH_SLA_DAYS.get(sla_key, PATCH_SLA_DAYS["medium"])

        identified_date = date.fromisoformat(str(vuln["identified_date"]))
        deadline = identified_date + timedelta(days=sla_days)
        if reference_date > deadline and vuln.get("status") not in ("patched", "mitigated", "accepted"):
            violations.append({
                "cve": vuln.get("cve_id", "unknown"),
                "severity": sla_key,
                "sla_days": sla_days,
                "overdue_days": (reference_date - deadline).days,
            })

    assert not violations, (
        f"PR.PS-02: {len(violations)} vulnerability/patch SLA violations: "
        + ", ".join(f"{v['cve']} ({v['severity']}, {v['overdue_days']}d overdue)" for v in violations)
    )
```

### PR.IR — Technology Infrastructure Resilience (Pattern 1 — DETERMINISTIC against defined RTO/RPO)

```python
def test_pr_ir_backup_exists_and_tested(
    controls_evidence: dict,
    reference_date: date,
):
    """
    PR.IR-04: Adequate resource capacity is ensured. Backups exist and are
    tested. DETERMINISTIC against documented RTO/RPO commitments.
    Maps to: NIST 800-53 CP-9, ISO 27001 A.8.13, SOC 2 A1.2.
    """
    pr_evidence = controls_evidence.get("csf_protect", {})
    resilience = pr_evidence.get("infrastructure_resilience", {}) if pr_evidence else {}
    assert resilience, "PR.IR: No infrastructure resilience evidence found"

    backup = resilience.get("backup", {})
    assert backup, "PR.IR-04: No backup configuration documented"
    assert backup.get("last_backup_date"), "No last backup date recorded"
    assert backup.get("last_restore_test_date"), (
        "PR.IR-04: No backup restore test has been performed — backups must be tested"
    )

    last_test = date.fromisoformat(str(backup["last_restore_test_date"]))
    age_months = (reference_date - last_test).days / 30.44
    assert age_months <= RECOVERY_PLAN_TEST_MONTHS, (
        f"Backup restore test is {age_months:.0f} months old "
        f"(threshold: {RECOVERY_PLAN_TEST_MONTHS} months)"
    )
```

---

## DE — Detect

### DE.CM — Continuous Monitoring (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-CSF-PROFILE-001",
    description="Monitoring coverage adequacy is Pattern 2 — CISO must review.",
    approved_by="CISO",
    review_date="2027-02",
)
def test_de_cm_continuous_monitoring_solution_deployed(
    controls_evidence: dict,
):
    """
    DE.CM-01/06: Networks and personnel activity are monitored. Monitoring
    solution existence is DETERMINISTIC (binary); coverage adequacy is PARAMETERIZED.
    Maps to: NIST 800-53 CA-7, ISO 27001 A.8.16, SOC 2 CC7.2.
    """
    de_evidence = controls_evidence.get("csf_detect", {})
    monitoring = de_evidence.get("continuous_monitoring", {}) if de_evidence else {}
    assert monitoring, "DE.CM: No continuous monitoring evidence found"
    assert monitoring.get("siem_or_monitoring_tool"), (
        "DE.CM-01: No SIEM or monitoring solution deployed"
    )
    assert monitoring.get("network_monitoring_enabled", False), (
        "DE.CM-01: Network traffic monitoring not enabled"
    )
    assert monitoring.get("log_retention_days", 0) >= 90, (
        "DE.CM: Log retention below 90-day minimum — adequate event analysis requires sufficient history"
    )


def test_de_cm_vulnerability_scanning_cadence(
    controls_evidence: dict,
    reference_date: date,
):
    """
    DE.CM-08: Vulnerability scans performed. At minimum: authenticated scans
    of internal systems at least monthly. Maps to: NIST 800-53 RA-5, PCI DSS Req 11.3.
    """
    de_evidence = controls_evidence.get("csf_detect", {})
    monitoring = de_evidence.get("continuous_monitoring", {}) if de_evidence else {}
    last_scan = monitoring.get("last_vulnerability_scan_date")
    assert last_scan, "DE.CM-08: No vulnerability scan date recorded"
    last_scan_date = date.fromisoformat(str(last_scan))
    age_days = (reference_date - last_scan_date).days
    assert age_days <= 31, (
        f"Last vulnerability scan {age_days} days ago — monthly cadence required (≤31 days)"
    )
```

---

## RS — Respond

### RS.MA — Incident Management (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-CSF-PROFILE-001",
    description="IRP completeness and adequacy is Pattern 2.",
    approved_by="CISO",
    review_date="2027-02",
)
def test_rs_ma_incident_response_plan_exists_and_current(
    controls_evidence: dict,
    reference_date: date,
):
    """
    RS.MA-01: Incidents are investigated. IRP must exist, be reviewed annually,
    and be tested (tabletop or simulation) at least annually.
    Maps to: NIST 800-53 IR-8, ISO 27001 A.5.26, SOC 2 CC7.3.
    """
    rs_evidence = controls_evidence.get("csf_respond", {})
    irp = rs_evidence.get("incident_response_plan", {}) if rs_evidence else {}
    assert irp, "RS.MA-01: No incident response plan found in evidence"

    last_review = irp.get("last_review_date")
    assert last_review, "IRP lacks a review date"
    review_age = (reference_date - date.fromisoformat(str(last_review))).days / 30.44
    assert review_age <= IRP_REVIEW_MONTHS, (
        f"IRP last reviewed {review_age:.0f} months ago (threshold: {IRP_REVIEW_MONTHS} months)"
    )

    last_test = irp.get("last_test_date")
    assert last_test, "IRP has never been tested (tabletop or simulation required)"
    test_age = (reference_date - date.fromisoformat(str(last_test))).days / 30.44
    assert test_age <= IRP_TEST_MONTHS, (
        f"IRP last tested {test_age:.0f} months ago (threshold: {IRP_TEST_MONTHS} months)"
    )
```

### RS.CO — Incident Reporting and Communication (Pattern 1 — DETERMINISTIC for regulated deadlines)

```python
def test_rs_co_notification_deadlines_tracked_per_framework(
    controls_evidence: dict,
    entity_profile: dict,
):
    """
    RS.CO-02: Incidents are reported consistent with established criteria.
    When regulatory notification deadlines apply (SEC, HIPAA, GDPR, NYDFS, DORA),
    each deadline is tracked separately. DETERMINISTIC when specific deadlines apply.
    Maps to: NIST 800-53 IR-6, ISO 27001 A.5.25, SOC 2 CC7.3.
    """
    rs_evidence = controls_evidence.get("csf_respond", {})
    comm_plan = rs_evidence.get("incident_communication_plan", {}) if rs_evidence else {}
    assert comm_plan, "RS.CO: No incident communication plan found"

    # Check that known applicable regulatory notification tracks are in the plan
    notification_tracks = frozenset(comm_plan.get("regulatory_notification_tracks", []))
    required_tracks = set()
    if entity_profile.get("sec_registered", False):
        required_tracks.add("sec_8k_4_business_days")
    if entity_profile.get("hipaa_covered_entity", False):
        required_tracks.add("hipaa_breach_60_days")
    if entity_profile.get("gdpr_in_scope", False):
        required_tracks.add("gdpr_72_hours")
    if entity_profile.get("ny_dfs_covered_entity", False):
        required_tracks.add("nydfs_72_hours")
    if entity_profile.get("dora_in_scope", False):
        required_tracks.add("dora_4_hours_initial")

    missing = required_tracks - notification_tracks
    assert not missing, (
        f"RS.CO-02: Incident communication plan is missing regulatory notification "
        f"tracks for applicable frameworks: {missing}"
    )
```

---

## RC — Recover

### RC.RP — Recovery Plan Execution (Pattern 2 — PARAMETERIZED with DETERMINISTIC RTO/RPO check)

```python
@pytest.mark.assumption(
    id="ASSUME-CSF-PROFILE-001",
    description="RTO/RPO commitments are org-defined; tests assert against those commitments.",
    approved_by="CISO",
    review_date="2027-02",
)
def test_rc_rp_recovery_plan_exists_and_rto_rpo_defined(
    controls_evidence: dict,
    reference_date: date,
):
    """
    RC.RP-01: The recovery portion of the incident response plan is executed
    during or after a cybersecurity incident. RTO/RPO must be defined and
    tested annually. Maps to: NIST 800-53 CP-10, ISO 27001 A.5.29–5.30, SOC 2 A1.3.
    """
    rc_evidence = controls_evidence.get("csf_recover", {})
    recovery = rc_evidence.get("recovery_plan", {}) if rc_evidence else {}
    assert recovery, "RC.RP-01: No recovery plan found in evidence"
    assert recovery.get("rto_hours") is not None, "Recovery plan lacks a defined RTO"
    assert recovery.get("rpo_hours") is not None, "Recovery plan lacks a defined RPO"

    last_test = recovery.get("last_test_date")
    assert last_test, "Recovery plan has never been tested"
    test_age = (reference_date - date.fromisoformat(str(last_test))).days / 30.44
    assert test_age <= RECOVERY_PLAN_TEST_MONTHS, (
        f"Recovery plan last tested {test_age:.0f} months ago "
        f"(threshold: {RECOVERY_PLAN_TEST_MONTHS} months)"
    )

    # Verify last tested recovery time met the RTO commitment
    rto_hours = recovery["rto_hours"]
    last_test_recovery_time = recovery.get("last_test_recovery_hours")
    if last_test_recovery_time is not None:
        assert last_test_recovery_time <= rto_hours, (
            f"Last recovery test took {last_test_recovery_time}h, exceeding RTO commitment of {rto_hours}h"
        )
```

---

## Open assumptions

| ID | Assumption | Pattern | Approved | Review |
|---|---|---|---|---|
| ASSUME-CSF-TIER-001 | Tier determination is self-assessed by the organization; we treat the documented self-assessment as the authoritative tier; independent validation that the tier accurately reflects maturity is Pattern 3 — CISO attestation required | 3 | Pending | 2027-02 |
| ASSUME-CSF-PROFILE-001 | Target Profile represents the organization's documented risk management decisions; tests assert Current ≥ Target; whether the Target Profile is ambitious enough relative to the threat environment is Pattern 3 requiring Risk Committee approval | 3 | Pending | 2027-02 |
| ASSUME-CSF-PATCH-001 | Patch SLAs: CISA KEV = 14 days; Critical (non-KEV) = 30 days; High = 60 days; Medium = 90 days; Low = 180 days; when the organization has a documented patch SLA that is more stringent, the org SLA governs | 1 | Pending | 2027-02 |
| ASSUME-CSF-ACCESS-001 | Privileged access review frequency of quarterly (3 months) is the minimum; aligns with NIST 800-53 AC-2(3) recommendation; standard user access reviewed annually | 1 | Pending | 2027-02 |
| ASSUME-CSF-TRAIN-001 | Annual awareness training is the minimum cadence; privileged role-based training at onboarding and annually; 95% completion rate is the minimum threshold | 2 | Pending | 2027-02 |
| ASSUME-CSF-ASSET-001 | Asset inventory reconciliation minimum is annual; more frequent reconciliation is required for high-change environments; completeness assessment (what percentage of assets are captured) is Pattern 2 | 2 | Pending | 2027-02 |
