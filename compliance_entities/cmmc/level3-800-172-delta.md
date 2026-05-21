# CMMC Level 3 — Enhanced Security Requirements (NIST SP 800-172 Delta)
## 24 practices added above NIST SP 800-171 r2 baseline

**Basis:** NIST SP 800-172 Rev 1 (Feb 2021) — Enhanced Security Requirements for Protecting CUI
**CMMC level:** Level 3 (Expert) — assessed by DCSA-led government assessors; triennial
**Prerequisite:** Level 2 (all 110 NIST 800-171 r2 practices) must be met before Level 3 delta applies
**DoD applicability:** Programs designated by DoD for Level 3 based on criticality and CUI sensitivity

**Applies to:** Defense contractors and subcontractors handling Controlled Unclassified Information (CUI) or Federal Contract Information (FCI) under Department of Defense (DoD) contracts and subcontracts
**Trigger:** DoD contract or subcontract containing DFARS clause 252.204-7012 (CUI) or 252.204-7021 (CMMC); prime contractors must flow down CMMC requirements to all subcontractors handling CUI; CMMC Level determined by CUI type and sensitivity
**Jurisdiction:** United States Department of Defense supply chain; applies to US companies and foreign companies holding DoD contracts
**Not applicable to:** Commercial-only companies with no DoD contracts or subcontracts; DoD contracts not involving CUI or FCI (though basic contractor ethics and safeguarding under FAR 52.204-21 still apply); non-defense government contractors (civilian agencies use FISMA/800-171 directly without CMMC framework)

---

## RDF extraction

```
Subject:    DoD contractor with Level 3 contract designation
Condition:  System boundary contains CUI for a high-priority program designated by DoD
Obligation: Implement 24 enhanced practices from NIST 800-172 in addition to all 800-171 r2 requirements
Evidence:   Level 3 SSP documenting all 134 practices; DCSA assessment results; POA&M for any gaps
```

---

## Constants

```python
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# Assessment cadence
LEVEL3_ASSESSMENT_YEARS   = 3    # triennial DCSA-led government assessment
ANNUAL_AFFIRMATION_MONTHS = 12   # annual senior official affirmation (same as Level 1/2)

# Penetration testing cadence (CA.L3)
ADVERSARIAL_PENTEST_MONTHS = 12  # ASSUME-CMMC-L3-CA-001: annual adversarial pentest minimum

# Threat intelligence feed currency (SA.L3)
THREAT_INTEL_FEED_DAYS = 7       # ASSUME-CMMC-L3-SA-001: feeds updated at least weekly

# Threat model review cadence
THREAT_MODEL_REVIEW_MONTHS = 12

# SOC monitoring coverage
SOC_COVERAGE_HOURS_PER_DAY = 24  # 24x7 coverage required for CA.L3

# Backup resilience (RE.L3)
BACKUP_RESILIENCE_TEST_MONTHS = 6   # ASSUME-CMMC-L3-RE-001: semi-annual for Level 3

# Supply chain risk assessment cadence (SR.L3)
SUPPLY_CHAIN_ASSESSMENT_MONTHS = 12

# FIPS validation — SC.L3-3.13.10e
ACCEPTED_FIPS_MODULES = frozenset({
    "aes-256",
    "aes-128",
    "sha-256",
    "sha-384",
    "sha-512",
    "ecdh-p256",
    "ecdh-p384",
    "rsa-2048",
    "rsa-3072",
    "rsa-4096",
})
```

---

## Scope pre-condition fixtures

```python
import pytest

@pytest.fixture(autouse=True)
def cmmc_level3_scope_check(entity_profile: dict):
    """Skip Level 3 delta tests if entity is not under a Level 3 contract designation."""
    if entity_profile.get("cmmc_required_level", 0) < 3:
        pytest.skip(
            "Entity is not designated for CMMC Level 3 — enhanced 800-172 practices not required"
        )

@pytest.fixture(autouse=True)
def cmmc_level2_baseline_met(controls_evidence: dict):
    """Level 3 delta only applies when Level 2 (800-171) baseline is met."""
    sprs = controls_evidence.get("cmmc_sprs_score", {})
    if sprs and sprs.get("current_score", 110) < 110:
        pytest.skip(
            "Level 2 baseline not fully met (SPRS < 110) — Level 3 delta assessment "
            "requires full Level 2 compliance first"
        )
```

---

## AC — Access Control (+2 Level 3 practices)

### AC.L3-3.1.2e — Dynamic access control for CUI (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-CMMC-L3-AC-001",
    description=(
        "Dynamic access control (AC.L3-3.1.2e) requires context-aware, real-time "
        "access decisions for CUI based on factors such as user role, device posture, "
        "network location, and time of day. The specific attributes and decision logic "
        "are org-defined; adequacy is Pattern 2 requiring ISSO review."
    ),
    approved_by="ISSO",
    review_date="2027-01",
)
def test_ac_dynamic_access_control_implemented(
    controls_evidence: dict,
):
    """
    AC.L3-3.1.2e: Employ dynamic access control approaches for CUI that allow
    access decisions to be conditioned on dynamic and context-based information.
    """
    ac = controls_evidence.get("cmmc_access_control", {})
    dynamic_ac = ac.get("dynamic_access_control", {}) if ac else {}
    assert dynamic_ac, (
        "AC.L3-3.1.2e: No dynamic access control implementation found. "
        "Static role-based access control alone does not satisfy this requirement."
    )
    assert dynamic_ac.get("context_attributes_defined"), (
        "Dynamic access control lacks documented context attributes (device posture, "
        "location, time, risk score, etc.)"
    )
    assert dynamic_ac.get("decision_engine"), (
        "No access decision engine documented for dynamic/context-based evaluation"
    )


### AC.L3-3.1.3e — Control CUI on mobile and remote access devices (Pattern 1 — DETERMINISTIC)

```python
def test_ac_cui_mobile_device_controls_enforced(
    controls_evidence: dict,
):
    """
    AC.L3-3.1.3e: Control CUI processed or stored on mobile devices. MDM/MAM
    policy must prevent unauthorized CUI access on unmanaged or non-compliant devices.
    """
    ac = controls_evidence.get("cmmc_access_control", {})
    mobile = ac.get("mobile_device_cui_controls", {}) if ac else {}
    assert mobile, "AC.L3-3.1.3e: No mobile device CUI controls documented"
    assert mobile.get("mdm_or_mam_enforced", False), (
        "AC.L3-3.1.3e: MDM/MAM policy not enforced for CUI access on mobile devices"
    )
    assert mobile.get("unmanaged_device_access_blocked", False), (
        "AC.L3-3.1.3e: Unmanaged/non-compliant devices are not blocked from CUI access"
    )
    assert mobile.get("remote_wipe_capability", False), (
        "AC.L3-3.1.3e: Remote wipe capability not configured for mobile devices with CUI access"
    )
```

---

## AT — Awareness and Training (+1 Level 3 practice)

### AT.L3-3.2.1e — Insider threat awareness training (Pattern 1 — DETERMINISTIC)

```python
def test_at_insider_threat_awareness_training_completed(
    controls_evidence: dict,
    reference_date: date,
):
    """
    AT.L3-3.2.1e: Provide security awareness training on recognizing and reporting
    potential indicators of insider threat. Must be included in the annual security
    awareness training program.
    """
    training = controls_evidence.get("cmmc_awareness_training", {})
    insider_threat_training = training.get("insider_threat_module", {}) if training else {}
    assert insider_threat_training, (
        "AT.L3-3.2.1e: No insider threat awareness training module found. "
        "Level 3 requires explicit insider threat recognition and reporting training."
    )
    last_delivery = insider_threat_training.get("last_delivery_date")
    assert last_delivery, "Insider threat training module lacks a last delivery date"
    age = (reference_date - date.fromisoformat(str(last_delivery))).days / 30.44
    assert age <= 12, (
        f"Insider threat training last delivered {age:.0f} months ago (threshold: 12 months)"
    )
    completion_rate = insider_threat_training.get("completion_rate_percent", 0)
    assert completion_rate >= 95, (
        f"Insider threat training completion rate {completion_rate}% below 95% threshold"
    )
```

---

## CM — Configuration Management (+2 Level 3 practices)

### CM.L3-3.4.1e — Deny-by-exception (allowlisting) policy for software execution (Pattern 1 — DETERMINISTIC)

```python
def test_cm_deny_by_exception_software_policy_enforced(
    controls_evidence: dict,
):
    """
    CM.L3-3.4.1e: Employ a deny-by-exception policy for software execution on
    systems that process CUI. Default = deny; only explicitly approved software
    is permitted to execute. This supersedes the Level 2 "block known bad" approach.
    """
    cm = controls_evidence.get("cmmc_configuration_management", {})
    allowlisting = cm.get("software_allowlisting", {}) if cm else {}
    assert allowlisting, (
        "CM.L3-3.4.1e: No software allowlisting configuration found. "
        "Level 3 requires deny-by-exception (allowlisting), not deny-by-known-bad (blacklisting)."
    )
    assert allowlisting.get("default_deny_enforced", False), (
        "CM.L3-3.4.1e: Default-deny policy not enforced. "
        "All unapproved software must be blocked by default."
    )
    assert allowlisting.get("approved_software_list_exists", False), (
        "No approved software list (allowlist) found — required for deny-by-exception enforcement"
    )
    assert allowlisting.get("enforcement_tool"), (
        "No enforcement tool documented (e.g., AppLocker, WDAC, Carbon Black, etc.)"
    )


### CM.L3-3.4.2e — Application allowlisting on CUI systems (Pattern 1 — DETERMINISTIC)

```python
def test_cm_application_allowlisting_covers_all_cui_systems(
    controls_evidence: dict,
):
    """
    CM.L3-3.4.2e: Employ application allowlisting policies and procedures on
    all systems that process CUI. Coverage must be comprehensive — partial
    deployment does not satisfy the requirement.
    """
    cm = controls_evidence.get("cmmc_configuration_management", {})
    allowlisting = cm.get("software_allowlisting", {}) if cm else {}
    if not allowlisting:
        pytest.skip("No allowlisting configuration in evidence")

    coverage_percent = allowlisting.get("cui_system_coverage_percent", 0)
    assert coverage_percent >= 100, (
        f"CM.L3-3.4.2e: Application allowlisting covers {coverage_percent}% of CUI systems. "
        "100% coverage is required — partial deployment does not satisfy Level 3."
    )
```

---

## IA — Identification and Authentication (+1 Level 3 practice)

### IA.L3-3.5.3e — Replay-resistant authentication (Pattern 1 — DETERMINISTIC)

```python
def test_ia_replay_resistant_authentication_for_cui_systems(
    controls_evidence: dict,
):
    """
    IA.L3-3.5.3e: Employ replay-resistant authentication mechanisms for network
    access to privileged and non-privileged accounts on CUI systems.
    Kerberos, FIDO2, smart card/PIV, and TLS mutual authentication with
    session tokens satisfy this. Password-only authentication does not.
    """
    ia = controls_evidence.get("cmmc_ia", {})
    replay_resistant = ia.get("replay_resistant_auth", {}) if ia else {}
    assert replay_resistant, (
        "IA.L3-3.5.3e: No replay-resistant authentication mechanism documented. "
        "Standard password authentication is susceptible to replay attacks and does "
        "not satisfy this Level 3 requirement."
    )
    assert replay_resistant.get("mechanism_in_use"), (
        "Replay-resistant auth mechanism not identified (Kerberos, FIDO2, PIV/CAC, etc.)"
    )
    accepted_mechanisms = frozenset({
        "kerberos", "fido2", "piv_cac", "tls_mutual_auth", "totp_with_session_binding",
    })
    mechanism = replay_resistant.get("mechanism_in_use", "").lower()
    assert any(m in mechanism for m in accepted_mechanisms) or replay_resistant.get("mechanism_validated", False), (
        f"IA.L3-3.5.3e: Mechanism '{mechanism}' not recognized as replay-resistant. "
        "Provide validation evidence if using an alternative mechanism."
    )
```

---

## IR — Incident Response (+2 Level 3 practices)

### IR.L3-3.6.1e — Security Operations Center capability (Pattern 1 — DETERMINISTIC)

```python
def test_ir_security_operations_center_operational(
    controls_evidence: dict,
):
    """
    IR.L3-3.6.1e: Establish an operational capability to centrally monitor
    system events. A SOC (internal or contracted) with 24x7 monitoring is
    required for Level 3 CUI environments.
    ASSUME-CMMC-L3-CA-001: 24x7 coverage is required; coverage hours < 24
    constitute a gap.
    """
    ir = controls_evidence.get("cmmc_incident_response", {})
    soc = ir.get("soc", {}) if ir else {}
    assert soc, (
        "IR.L3-3.6.1e: No SOC capability documented. Level 3 requires a centralized "
        "security monitoring capability (internal SOC or contracted MSSP)."
    )
    assert soc.get("coverage_hours_per_day", 0) >= SOC_COVERAGE_HOURS_PER_DAY, (
        f"IR.L3-3.6.1e: SOC coverage is {soc.get('coverage_hours_per_day')} hours/day; "
        f"Level 3 requires {SOC_COVERAGE_HOURS_PER_DAY}x7 coverage"
    )
    assert soc.get("siem_in_use"), (
        "IR.L3-3.6.1e: No SIEM platform documented — required for centralized event monitoring"
    )


### IR.L3-3.6.2e — Track and manage incidents through resolution (Pattern 2 — PARAMETERIZED)

```python
def test_ir_incident_tracking_system_in_use(
    controls_evidence: dict,
):
    """
    IR.L3-3.6.2e: Track and manage ICT incidents through resolution.
    A ticketing/case management system integrated with incident response
    is required; ad hoc tracking (email, spreadsheets) does not satisfy Level 3.
    """
    ir = controls_evidence.get("cmmc_incident_response", {})
    tracking = ir.get("incident_tracking_system", {}) if ir else {}
    assert tracking, "IR.L3-3.6.2e: No incident tracking system documented"
    assert tracking.get("system_name"), "Incident tracking system lacks identification"
    assert tracking.get("integrated_with_soc", False), (
        "IR.L3-3.6.2e: Incident tracking system not integrated with SOC/monitoring capability"
    )
    assert tracking.get("closure_requires_root_cause", False), (
        "IR.L3-3.6.2e: Incident closure process does not require root cause analysis — "
        "Level 3 requires tracking through full resolution including lessons learned"
    )
```

---

## RM — Risk Management (+3 Level 3 practices)

### RM.L3-3.11.1e — Threat-informed risk assessment (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-CMMC-L3-RM-001",
    description=(
        "Threat-informed risk assessment (RM.L3-3.11.1e) requires integrating current "
        "threat intelligence into the risk assessment methodology. Annual refresh is the "
        "minimum cadence; threat model must reference adversary TTPs relevant to the "
        "organization's mission and CUI holdings."
    ),
    approved_by="ISSO",
    review_date="2027-01",
)
def test_rm_threat_informed_risk_assessment_current(
    controls_evidence: dict,
    reference_date: date,
):
    """
    RM.L3-3.11.1e: Employ threat intelligence to inform risk assessments periodically
    and when new threats are identified. Risk assessment must reference specific threat
    actors and TTPs relevant to the organization's CUI environment.
    """
    rm = controls_evidence.get("cmmc_risk_management", {})
    risk_assessment = rm.get("risk_assessment", {}) if rm else {}
    assert risk_assessment, "RM.L3-3.11.1e: No risk assessment found in evidence"

    threat_informed = risk_assessment.get("threat_informed", {})
    assert threat_informed, (
        "RM.L3-3.11.1e: Risk assessment is not threat-informed. "
        "Level 3 requires current threat intelligence (adversary TTPs) to be incorporated."
    )
    assert threat_informed.get("threat_actors_referenced"), "Risk assessment lacks threat actor analysis"
    assert threat_informed.get("ttps_referenced"), "Risk assessment lacks TTP analysis"

    last_update = risk_assessment.get("last_updated")
    assert last_update, "Risk assessment lacks a last-updated date"
    age = (reference_date - date.fromisoformat(str(last_update))).days / 30.44
    assert age <= THREAT_MODEL_REVIEW_MONTHS, (
        f"Threat-informed risk assessment last updated {age:.0f} months ago "
        f"(threshold: {THREAT_MODEL_REVIEW_MONTHS} months)"
    )


### RM.L3-3.11.2e — Threat hunting (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-CMMC-L3-RM-001",
    description="See above.",
    approved_by="ISSO",
    review_date="2027-01",
)
def test_rm_threat_hunting_program_active(
    controls_evidence: dict,
    reference_date: date,
):
    """
    RM.L3-3.11.2e: Employ a process for proactively hunting for threats within
    the CUI environment. Threat hunting goes beyond reactive monitoring; it
    presupposes breach and actively searches for indicators of compromise.
    """
    rm = controls_evidence.get("cmmc_risk_management", {})
    threat_hunting = rm.get("threat_hunting", {}) if rm else {}
    assert threat_hunting, (
        "RM.L3-3.11.2e: No threat hunting program documented. "
        "Level 3 requires proactive threat hunting beyond reactive SIEM monitoring."
    )
    assert threat_hunting.get("methodology_documented"), "Threat hunting methodology not documented"
    last_hunt = threat_hunting.get("last_hunt_date")
    assert last_hunt, "No threat hunting activities recorded"
    age = (reference_date - date.fromisoformat(str(last_hunt))).days / 30.44
    assert age <= 3, (
        f"Last threat hunt {age:.0f} months ago — quarterly cadence required at Level 3"
    )


### RM.L3-3.11.3e — Supply chain risk assessment (Pattern 2 — PARAMETERIZED)

```python
def test_rm_supply_chain_risk_assessment_for_critical_acquisitions(
    controls_evidence: dict,
    reference_date: date,
):
    """
    RM.L3-3.11.3e: Assess supply chain risks associated with critical acquisitions
    and employ countermeasures to reduce risk. Critical acquisitions include
    hardware, software, and services that process or protect CUI.
    """
    rm = controls_evidence.get("cmmc_risk_management", {})
    scrm = rm.get("supply_chain_risk_assessment", {}) if rm else {}
    assert scrm, "RM.L3-3.11.3e: No supply chain risk assessment program found"
    assert scrm.get("critical_acquisitions_identified"), (
        "Critical acquisitions not identified — required for supply chain risk assessment scope"
    )
    last_assessment = scrm.get("last_assessment_date")
    assert last_assessment, "Supply chain risk assessment lacks a last assessment date"
    age = (reference_date - date.fromisoformat(str(last_assessment))).days / 30.44
    assert age <= SUPPLY_CHAIN_ASSESSMENT_MONTHS, (
        f"Supply chain risk assessment {age:.0f} months old "
        f"(threshold: {SUPPLY_CHAIN_ASSESSMENT_MONTHS} months)"
    )
```

---

## CA — Security Assessment (+3 Level 3 practices)

### CA.L3-3.12.1e — Ongoing/continuous security control monitoring (Pattern 1 — DETERMINISTIC)

```python
def test_ca_continuous_security_control_monitoring(
    controls_evidence: dict,
    reference_date: date,
):
    """
    CA.L3-3.12.1e: Employ automated mechanisms to monitor security controls
    on an ongoing basis. Periodic (annual) assessments alone do not satisfy
    Level 3 — continuous automated monitoring is required.
    """
    ca = controls_evidence.get("cmmc_security_assessment", {})
    continuous_mon = ca.get("continuous_monitoring", {}) if ca else {}
    assert continuous_mon, (
        "CA.L3-3.12.1e: No continuous security control monitoring program found. "
        "Annual assessments alone do not satisfy Level 3."
    )
    assert continuous_mon.get("automated_tool"), "No automated monitoring tool documented"
    assert continuous_mon.get("monitoring_frequency") in (
        "continuous", "daily", "near-real-time"
    ), (
        "CA.L3-3.12.1e: Monitoring frequency must be continuous/near-real-time, "
        f"not '{continuous_mon.get('monitoring_frequency')}'"
    )


### CA.L3-3.12.4e — Adversarial penetration testing (Pattern 1 — DETERMINISTIC cadence)

```python
def test_ca_adversarial_penetration_testing_current(
    controls_evidence: dict,
    reference_date: date,
):
    """
    CA.L3-3.12.4e: Conduct penetration testing leveraging adversarial tactics,
    techniques, and procedures (TTPs) — not just vulnerability scanning.
    ASSUME-CMMC-L3-CA-001: annual adversarial pentest minimum at Level 3.
    Red team exercises satisfy this requirement.
    """
    ca = controls_evidence.get("cmmc_security_assessment", {})
    pentest = ca.get("adversarial_penetration_test", {}) if ca else {}
    assert pentest, (
        "CA.L3-3.12.4e: No adversarial penetration test found. "
        "Vulnerability scanning alone does not satisfy Level 3 — adversarial TTPs required."
    )
    last_test = pentest.get("last_completion_date")
    assert last_test, "Adversarial pentest lacks a completion date"
    age = (reference_date - date.fromisoformat(str(last_test))).days / 30.44
    assert age <= ADVERSARIAL_PENTEST_MONTHS, (
        f"Adversarial pentest last completed {age:.0f} months ago "
        f"(threshold: {ADVERSARIAL_PENTEST_MONTHS} months)"
    )
    assert pentest.get("ttp_framework_used"), (
        "CA.L3-3.12.4e: Pentest methodology must reference an adversarial TTP framework "
        "(e.g., MITRE ATT&CK) — standard pentest methodology does not satisfy Level 3"
    )
    assert pentest.get("report_shared_with_senior_officials", False), (
        "CA.L3-3.12.4e: Pentest results must be provided to senior officials — "
        "no evidence of senior official report distribution found"
    )
```

---

## SA — Situational Awareness (+2 Level 3 practices)

### SA.L3-3.15.3e — Threat intelligence from external sources (Pattern 1 — DETERMINISTIC)

```python
def test_sa_threat_intelligence_feeds_active_and_current(
    controls_evidence: dict,
    reference_date: date,
):
    """
    SA.L3-3.15.3e: Receive threat intelligence from ISACs, US-CERT, or other
    information sharing organizations. Feeds must be integrated into monitoring.
    ASSUME-CMMC-L3-SA-001: feeds must be updated at least weekly.
    """
    sa = controls_evidence.get("cmmc_situational_awareness", {})
    threat_intel = sa.get("threat_intelligence_feeds", {}) if sa else {}
    assert threat_intel, (
        "SA.L3-3.15.3e: No threat intelligence feeds documented. "
        "Level 3 requires receiving threat intel from ISACs or equivalent sources."
    )
    feeds = threat_intel.get("active_feeds", [])
    assert feeds, "No active threat intelligence feeds listed"

    last_update = threat_intel.get("last_feed_update_date")
    assert last_update, "Threat intel feeds lack a last-updated date"
    age_days = (reference_date - date.fromisoformat(str(last_update))).days
    assert age_days <= THREAT_INTEL_FEED_DAYS, (
        f"Threat intel feeds last updated {age_days} days ago "
        f"(threshold: {THREAT_INTEL_FEED_DAYS} days)"
    )
    assert threat_intel.get("integrated_with_siem", False), (
        "SA.L3-3.15.3e: Threat intelligence feeds not integrated with SIEM for automated correlation"
    )


### SA.L3-3.15.4e — Threat models developed and maintained (Pattern 2 — PARAMETERIZED)

```python
def test_sa_threat_model_documented_and_current(
    controls_evidence: dict,
    reference_date: date,
):
    """
    SA.L3-3.15.4e: Develop and maintain threat models to identify adversary
    goals, capabilities, and TTPs relevant to the organization's CUI environment.
    Threat model must be reviewed annually and after significant changes.
    """
    sa = controls_evidence.get("cmmc_situational_awareness", {})
    threat_model = sa.get("threat_model", {}) if sa else {}
    assert threat_model, "SA.L3-3.15.4e: No threat model documented"
    assert threat_model.get("adversary_goals_documented"), "Threat model lacks adversary goals analysis"
    assert threat_model.get("ttps_documented"), "Threat model lacks TTP documentation"

    last_review = threat_model.get("last_review_date")
    assert last_review, "Threat model lacks a review date"
    age = (reference_date - date.fromisoformat(str(last_review))).days / 30.44
    assert age <= THREAT_MODEL_REVIEW_MONTHS, (
        f"Threat model last reviewed {age:.0f} months ago "
        f"(threshold: {THREAT_MODEL_REVIEW_MONTHS} months)"
    )
```

---

## SC — System and Communications Protection (+2 Level 3 practices)

### SC.L3-3.13.10e — FIPS-validated cryptography for CUI (Pattern 1 — DETERMINISTIC)

```python
def test_sc_fips_validated_cryptography_for_cui(
    controls_evidence: dict,
):
    """
    SC.L3-3.13.10e: Employ FIPS-validated cryptography when used to protect
    the confidentiality of CUI. FIPS 140-2 or 140-3 validated modules required.
    Non-FIPS cryptographic implementations do not satisfy Level 3, regardless
    of algorithm strength.
    """
    sc = controls_evidence.get("cmmc_sc", {})
    crypto = sc.get("cryptographic_implementations", []) if sc else []
    assert crypto, "SC.L3-3.13.10e: No cryptographic implementation documentation found"

    violations = []
    for impl in crypto:
        if not impl.get("protects_cui", False):
            continue
        if not impl.get("fips_validated", False):
            violations.append({
                "name": impl.get("implementation_name", "unnamed"),
                "algorithm": impl.get("algorithm"),
                "issue": "not FIPS-validated — FIPS 140-2/140-3 module required for CUI protection",
            })

    assert not violations, (
        "SC.L3-3.13.10e: Cryptographic implementations protecting CUI without FIPS validation: "
        + "; ".join(f"{v['name']} ({v['algorithm']})" for v in violations)
    )


### SC.L3-3.13.4e — Software-defined networking / managed interfaces for CUI (Pattern 2 — PARAMETERIZED)

```python
def test_sc_managed_interfaces_control_cui_flows(
    controls_evidence: dict,
):
    """
    SC.L3-3.13.4e: Establish and manage interfaces for processing CUI. All
    external and internal CUI communication channels must be managed through
    explicitly defined interfaces with access controls.
    """
    sc = controls_evidence.get("cmmc_sc", {})
    managed_interfaces = sc.get("managed_interfaces", {}) if sc else {}
    assert managed_interfaces, (
        "SC.L3-3.13.4e: No managed interface documentation found for CUI communication channels"
    )
    assert managed_interfaces.get("external_interfaces_documented"), (
        "External CUI communication interfaces not documented"
    )
    assert managed_interfaces.get("internal_interfaces_documented"), (
        "Internal CUI communication interfaces not documented"
    )
    assert managed_interfaces.get("unauthorized_flows_blocked", False), (
        "SC.L3-3.13.4e: No mechanism to block unauthorized CUI communication flows documented"
    )
```

---

## SI — System and Information Integrity (+2 Level 3 practices)

### SI.L3-3.14.1e — Threat indicator correlation and application (Pattern 2 — PARAMETERIZED)

```python
def test_si_threat_indicators_applied_to_monitoring(
    controls_evidence: dict,
):
    """
    SI.L3-3.14.1e: Use threat indicator information relevant to the systems
    and information being protected. IOCs from threat intel feeds must be
    operationalized in detection systems (SIEM, EDR, IDS/IPS).
    """
    si = controls_evidence.get("cmmc_si", {})
    threat_indicators = si.get("threat_indicator_integration", {}) if si else {}
    assert threat_indicators, (
        "SI.L3-3.14.1e: No threat indicator integration documented. "
        "Level 3 requires operationalizing IOCs from threat intel feeds in detection tools."
    )
    assert threat_indicators.get("ioc_feed_integrated"), "No IOC feed integrated with detection tools"
    assert threat_indicators.get("automated_ioc_blocking", False), (
        "SI.L3-3.14.1e: IOCs not automatically applied to blocking rules — manual-only detection "
        "does not satisfy the Level 3 operationalization requirement"
    )


### SI.L3-3.14.3e — Advanced malware / APT detection (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-CMMC-L3-SI-001",
    description=(
        "Advanced APT detection (SI.L3-3.14.3e) requires tools beyond signature-based "
        "antivirus: behavioral analysis, EDR with threat hunting capability, or equivalent. "
        "Adequacy of the chosen solution is Pattern 2 — ISSO must review annually."
    ),
    approved_by="ISSO",
    review_date="2027-01",
)
def test_si_advanced_malware_and_apt_detection_deployed(
    controls_evidence: dict,
):
    """
    SI.L3-3.14.3e: Apply advanced techniques to detect and protect against
    advanced persistent threats, including behavioral analytics and endpoint
    detection and response (EDR) capabilities.
    """
    si = controls_evidence.get("cmmc_si", {})
    advanced_detection = si.get("advanced_malware_protection", {}) if si else {}
    assert advanced_detection, (
        "SI.L3-3.14.3e: No advanced malware / APT detection capability documented. "
        "Signature-based antivirus alone does not satisfy Level 3."
    )
    assert advanced_detection.get("behavioral_analysis", False), (
        "SI.L3-3.14.3e: No behavioral analysis capability — required for APT detection"
    )
    assert advanced_detection.get("edr_deployed", False), (
        "SI.L3-3.14.3e: No EDR solution deployed on CUI systems"
    )
```

---

## SR — Supply Chain Risk Management (+2 Level 3 practices)

### SR.L3-3.17.1e — Supply chain risk management plan (Pattern 1 — DETERMINISTIC)

```python
def test_sr_scrm_plan_documented_and_current(
    controls_evidence: dict,
    reference_date: date,
):
    """
    SR.L3-3.17.1e: Develop and maintain a supply chain risk management plan
    that identifies and addresses supply chain risks for critical acquisitions.
    Plan must be reviewed annually.
    """
    sr = controls_evidence.get("cmmc_supply_chain", {})
    scrm_plan = sr.get("scrm_plan", {}) if sr else {}
    assert scrm_plan, "SR.L3-3.17.1e: No supply chain risk management plan found"
    assert scrm_plan.get("plan_document"), "SCRM plan document reference missing"
    assert scrm_plan.get("critical_suppliers_listed"), "SCRM plan does not list critical suppliers"

    last_review = scrm_plan.get("last_review_date")
    assert last_review, "SCRM plan lacks a review date"
    age = (reference_date - date.fromisoformat(str(last_review))).days / 30.44
    assert age <= SUPPLY_CHAIN_ASSESSMENT_MONTHS, (
        f"SCRM plan last reviewed {age:.0f} months ago "
        f"(threshold: {SUPPLY_CHAIN_ASSESSMENT_MONTHS} months)"
    )


### SR.L3-3.17.2e — Supply chain component vulnerability assessment (Pattern 2 — PARAMETERIZED)

```python
def test_sr_supply_chain_components_assessed_for_vulnerabilities(
    controls_evidence: dict,
):
    """
    SR.L3-3.17.2e: Assess supply chain components (hardware, software, services)
    for vulnerabilities and implement countermeasures. Vendor SBOMs (Software
    Bill of Materials) provide visibility into software supply chain components.
    """
    sr = controls_evidence.get("cmmc_supply_chain", {})
    component_assessment = sr.get("component_vulnerability_assessment", {}) if sr else {}
    assert component_assessment, (
        "SR.L3-3.17.2e: No supply chain component vulnerability assessment program found"
    )
    assert component_assessment.get("sbom_or_component_inventory"), (
        "No SBOM or component inventory for critical software components — "
        "required for supply chain vulnerability visibility"
    )
    assert component_assessment.get("vulnerability_monitoring_active", False), (
        "SR.L3-3.17.2e: No active vulnerability monitoring for supply chain components"
    )
```

---

## Open assumptions

| ID | Assumption | Pattern | Approved | Review |
|---|---|---|---|---|
| ASSUME-CMMC-L3-AC-001 | Dynamic access control (AC.L3-3.1.2e) context attributes and decision logic are org-defined; specific implementation is Pattern 2 requiring ISSO review; adequacy is assessed by DCSA assessors during triennial assessment | 2 | Pending | 2027-01 |
| ASSUME-CMMC-L3-CA-001 | Adversarial pentest (CA.L3-3.12.4e) requires annual minimum cadence; SOC coverage is 24x7; both are DETERMINISTIC once the program is established | 1 | Pending | 2027-01 |
| ASSUME-CMMC-L3-RM-001 | Threat-informed risk assessment annual refresh; threat hunting quarterly; both must reference specific adversary TTPs; adequacy of TTP coverage is Pattern 2 | 2 | Pending | 2027-01 |
| ASSUME-CMMC-L3-SA-001 | Threat intel feeds updated at least weekly (7-day threshold); integration with SIEM for automated correlation is required; adequacy of correlation rules is Pattern 2 | 1 | Pending | 2027-01 |
| ASSUME-CMMC-L3-SI-001 | Advanced malware/APT protection requires behavioral analysis + EDR; signature-based antivirus alone fails Level 3; adequacy of the specific solution is Pattern 2 | 2 | Pending | 2027-01 |
| ASSUME-CMMC-L3-RE-001 | Backup resilience testing at Level 3 follows a semi-annual cadence (6 months) rather than the annual cadence of Level 2; the RE.L3 practice requires "regular" comprehensive and resilient backups | 1 | Pending | 2027-01 |
