# NIST SP 800-171 r3 — SC, IR, PE, MA, MP, PS, CA Families
## System Communications Protection, Incident Response, Physical Protection, and Supporting Families

**Source:** NIST SP 800-171 Rev 3 (May 2024); NIST SP 800-171A Rev 3 assessment procedures
**Scope:** CUI systems in nonfederal organizations; all requirements apply only within the CUI system boundary

---

## Constants

```python
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# SC family thresholds
TLS_MINIMUM_VERSION         = "1.2"   # ASSUME-800171-SC-001
FIPS_REQUIRED               = True    # federal contractors: FIPS 140-2/3 validated modules
DNS_SECURITY_REQUIRED       = True    # DNSSEC or equivalent (3.13.12)
SESSION_TERMINATION_MINUTES = 30      # ASSUME-800171-SC-002 — inactivity session termination
NETWORK_SEGREGATION_REQUIRED = True   # CUI systems on separate VLAN/segment (3.13.3)

# IR family thresholds
IR_PLAN_REVIEW_MONTHS       = 12      # annual IRP review (3.6.2)
IR_TEST_MONTHS              = 12      # annual IR exercise/test (3.6.3)
IR_EXTERNAL_REPORTING_HOURS = 72      # report to US-CERT/org contact ≤72h (ASSUME-800171-IR-001)

# PE family thresholds
PHYSICAL_ACCESS_REVIEW_MONTHS = 6     # semi-annual physical access list review (ASSUME-800171-PE-001)
VISITOR_LOG_RETENTION_MONTHS  = 36    # 3-year visitor log retention (ASSUME-800171-PE-002)

# MA family
REMOTE_MAINTENANCE_LOG_REQUIRED = True  # all remote maintenance sessions logged (3.7.5)

# MP family
MEDIA_DISPOSAL_NIST_800_88    = True    # NIST 800-88 sanitization required (3.8.3)

# PS family
PERSONNEL_TERMINATION_DAYS    = 1      # same-day account termination on departure (ASSUME-800171-PS-001)

# CA family
SECURITY_ASSESSMENT_MONTHS    = 36     # triennial full assessment; annual self-assessment (3.12.1)
POAM_CRITICAL_DAYS            = 30     # CVSS≥9.0 or actively exploited — ≤30-day remediation
POAM_HIGH_DAYS                = 90     # CVSS 7.0–8.9 — ≤90-day remediation
```

---

## 3.13 — System and Communications Protection (SC)

### 3.13.1 — Network boundary protection / CUI traffic monitoring (Pattern 1 — DETERMINISTIC)

```python
def test_sc_network_boundary_protection(
    controls_evidence: dict,
):
    """
    3.13.1: Monitor, control, and protect communications at external boundaries
    and key internal boundaries. Firewalls, packet filtering, and IDS/IPS required.
    """
    sc = controls_evidence.get("nist_sc", {})
    boundary = sc.get("network_boundary_protection", {}) if sc else {}
    assert boundary, "3.13.1: No network boundary protection documentation found"
    assert boundary.get("firewall_deployed", False), "3.13.1: No firewall at CUI system boundary"
    assert boundary.get("external_boundary_monitored", False), "3.13.1: External boundary not monitored"
    assert boundary.get("key_internal_boundaries_controlled", False), (
        "3.13.1: Key internal boundaries (e.g., CUI VLAN to guest/corporate) not controlled"
    )
```

### 3.13.2 — Network segmentation (CUI systems isolated) (Pattern 1 — DETERMINISTIC)

```python
def test_sc_cui_network_segmentation(
    controls_evidence: dict,
):
    """
    3.13.2: Employ architectural designs, software development techniques, and
    systems engineering principles promoting security. Minimum: CUI systems on
    dedicated network segment (VLAN) not shared with general IT traffic.
    ASSUME-800171-SC-001: VLAN isolation is the minimum; micro-segmentation preferred.
    """
    sc = controls_evidence.get("nist_sc", {})
    segmentation = sc.get("network_segmentation", {}) if sc else {}
    assert segmentation, "3.13.2: No network segmentation documentation found"
    assert segmentation.get("cui_segment_isolated", False), (
        "3.13.2: CUI systems are not on an isolated network segment. "
        "CUI systems must not share a segment with general-purpose IT or guest networks."
    )
    assert segmentation.get("segment_type"), "Network segmentation type not documented (VLAN, VPC, etc.)"
```

### 3.13.5 — Public-to-internal boundary — DMZ / deny-by-default (Pattern 1 — DETERMINISTIC)

```python
def test_sc_dmz_and_deny_by_default_from_public(
    controls_evidence: dict,
):
    """
    3.13.5: Implement subnetworks for publicly accessible system components
    separated from internal networks. Default-deny inbound from internet to
    CUI systems; only explicitly permitted traffic allowed.
    """
    sc = controls_evidence.get("nist_sc", {})
    dmz = sc.get("dmz_configuration", {}) if sc else {}
    assert dmz, "3.13.5: No DMZ or perimeter segmentation documentation found"
    assert dmz.get("publicly_accessible_components_in_dmz", False), (
        "3.13.5: Publicly accessible components not isolated in DMZ"
    )
    assert dmz.get("default_deny_inbound_to_cui", False), (
        "3.13.5: Default-deny not enforced for inbound internet traffic to CUI systems"
    )
```

### 3.13.6 — Deny-by-exception network communications (Pattern 1 — DETERMINISTIC)

```python
def test_sc_deny_by_exception_network_policy(
    controls_evidence: dict,
):
    """
    3.13.6: Deny network communications traffic by default; allow by exception
    (i.e., deny-all, permit-by-exception). Firewall ruleset must reflect this.
    """
    sc = controls_evidence.get("nist_sc", {})
    fw_policy = sc.get("firewall_policy", {}) if sc else {}
    assert fw_policy, "3.13.6: No firewall policy documentation found"
    assert fw_policy.get("default_deny_all", False), (
        "3.13.6: Firewall does not implement default-deny-all. Implicit permit rules violate 3.13.6."
    )
    assert fw_policy.get("exception_approval_process"), (
        "3.13.6: No documented exception approval process for firewall rule additions"
    )
```

### 3.13.8 — Encryption in transit for CUI (Pattern 1 — DETERMINISTIC)

```python
def test_sc_cui_encrypted_in_transit(
    controls_evidence: dict,
):
    """
    3.13.8: Implement cryptographic mechanisms to prevent unauthorized disclosure
    of CUI during transmission. TLS 1.2+ required; older protocols prohibited.
    ASSUME-800171-SC-001: TLS 1.0, TLS 1.1, SSL prohibited; TLS 1.2 minimum;
    TLS 1.3 preferred; FIPS-validated cipher suites for federal contractors.
    """
    sc = controls_evidence.get("nist_sc", {})
    transit_encryption = sc.get("transmission_encryption", {}) if sc else {}
    assert transit_encryption, "3.13.8: No transmission encryption documentation found"
    assert transit_encryption.get("tls_minimum_version") in ("1.2", "1.3"), (
        f"3.13.8: TLS minimum version is '{transit_encryption.get('tls_minimum_version')}'; "
        f"requires {TLS_MINIMUM_VERSION} or higher"
    )
    prohibited = frozenset(transit_encryption.get("disabled_protocols", []))
    required_disabled = frozenset({"sslv2", "sslv3", "tls1.0", "tls1.1"})
    not_disabled = required_disabled - prohibited
    assert not not_disabled, (
        f"3.13.8: Prohibited protocols not confirmed disabled: {not_disabled}"
    )
    if transit_encryption.get("federal_contractor", False):
        assert transit_encryption.get("fips_cipher_suites", False), (
            "3.13.8: Federal contractor must use FIPS-validated cipher suites"
        )
```

### 3.13.10 — Cryptographic key management (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-800171-SC-003",
    description=(
        "Cryptographic key management (3.13.10) — key generation, distribution, storage, "
        "access, retirement, and destruction must be documented. Adequacy of the key "
        "lifecycle process is Pattern 2 — ISSO review required annually."
    ),
    approved_by="ISSO",
    review_date="2027-01",
)
def test_sc_cryptographic_key_management_documented(
    controls_evidence: dict,
):
    """
    3.13.10: Employ FIPS-validated cryptography when used to protect the
    confidentiality of CUI. Key management lifecycle must be documented.
    """
    sc = controls_evidence.get("nist_sc", {})
    key_mgmt = sc.get("key_management", {}) if sc else {}
    assert key_mgmt, "3.13.10: No cryptographic key management documentation found"
    required_lifecycle_phases = frozenset({
        "key_generation", "key_distribution", "key_storage", "key_retirement", "key_destruction"
    })
    documented_phases = frozenset(key_mgmt.get("documented_lifecycle_phases", []))
    missing = required_lifecycle_phases - documented_phases
    assert not missing, (
        f"3.13.10: Key management lifecycle missing phases: {missing}"
    )
```

### 3.13.11 — FIPS-validated cryptography (Pattern 1 — DETERMINISTIC)

```python
def test_sc_fips_validated_cryptography(
    controls_evidence: dict,
):
    """
    3.13.11: Employ FIPS-validated cryptography when used to protect the
    confidentiality of CUI. Applies to all cryptographic modules in the CUI
    boundary, not just TLS. FIPS 140-2 minimum; FIPS 140-3 preferred.
    """
    sc = controls_evidence.get("nist_sc", {})
    crypto_modules = sc.get("cryptographic_modules", []) if sc else []
    assert crypto_modules, "3.13.11: No cryptographic module inventory found"

    violations = [
        m for m in crypto_modules
        if m.get("protects_cui", False) and not m.get("fips_validated", False)
    ]
    assert not violations, (
        "3.13.11: Cryptographic modules protecting CUI without FIPS validation: "
        + ", ".join(v.get("module_name", "unnamed") for v in violations)
    )
```

### 3.13.12 — Collaborative computing session control (Pattern 1 — DETERMINISTIC)

```python
def test_sc_remote_desktop_collaboration_controls(
    controls_evidence: dict,
):
    """
    3.13.12: Prohibit remote activation of collaborative computing devices and
    provide an indication of use to present users. Screen sharing, remote desktop,
    and video conferencing tools on CUI systems must not allow remote activation
    without explicit user consent.
    """
    sc = controls_evidence.get("nist_sc", {})
    collab = sc.get("collaborative_computing_controls", {}) if sc else {}
    assert collab, "3.13.12: No collaborative computing device controls documented"
    assert collab.get("remote_activation_prohibited", False), (
        "3.13.12: Remote activation of collaborative computing devices not prohibited"
    )
    assert collab.get("in_use_indicator_active", False), (
        "3.13.12: No in-use indicator provided to present users during remote sessions"
    )
```

### 3.13.14 — Session termination on inactivity (Pattern 1 — DETERMINISTIC)

```python
def test_sc_session_terminates_after_inactivity(
    controls_evidence: dict,
):
    """
    3.13.14: Terminate sessions after a defined condition. Inactivity timeout
    required. ASSUME-800171-SC-002: 30-minute inactivity timeout.
    Combined with AC 3.1.10 (session lock after 15 min) — this terminates
    rather than locks the session.
    """
    sc = controls_evidence.get("nist_sc", {})
    session_mgmt = sc.get("session_management", {}) if sc else {}
    timeout = session_mgmt.get("inactivity_termination_minutes", 0) if session_mgmt else 0
    assert timeout > 0, "3.13.14: No inactivity session termination configured"
    assert timeout <= SESSION_TERMINATION_MINUTES, (
        f"3.13.14: Session termination timeout {timeout} min exceeds {SESSION_TERMINATION_MINUTES}-min threshold"
    )
```

### 3.13.15 — Protection of network identifiers (Pattern 2 — PARAMETERIZED)

```python
def test_sc_network_identifier_protection(
    controls_evidence: dict,
):
    """3.13.15: Protect the authenticity of communications sessions."""
    sc = controls_evidence.get("nist_sc", {})
    session_auth = sc.get("session_authenticity", {}) if sc else {}
    assert session_auth, "3.13.15: No session authenticity controls documented"
    assert session_auth.get("mechanism"), (
        "3.13.15: No session authenticity mechanism specified (e.g., TLS session ID, HMAC tokens)"
    )
```

### 3.13.16 — CUI at rest encryption (Pattern 1 — DETERMINISTIC)

```python
def test_sc_cui_encrypted_at_rest(
    controls_evidence: dict,
):
    """
    3.13.16: Protect the confidentiality of CUI at rest.
    Full-disk encryption or file-level encryption required for all CUI storage.
    ASSUME-800171-SC-001: AES-256 preferred; AES-128 minimum; FIPS-validated
    module required for federal contractors.
    """
    sc = controls_evidence.get("nist_sc", {})
    at_rest = sc.get("data_at_rest_encryption", {}) if sc else {}
    assert at_rest, "3.13.16: No data-at-rest encryption documentation found"
    assert at_rest.get("cui_storage_encrypted", False), (
        "3.13.16: CUI data-at-rest is not encrypted"
    )
    algorithm = at_rest.get("encryption_algorithm", "").upper()
    assert "AES" in algorithm, (
        f"3.13.16: Encryption algorithm '{algorithm}' — AES required"
    )
    key_length = at_rest.get("key_length_bits", 0)
    assert key_length >= 128, (
        f"3.13.16: Key length {key_length} bits below 128-bit minimum"
    )
```

---

## 3.6 — Incident Response (IR)

### 3.6.1 — Incident response plan documented and current (Pattern 1 — DETERMINISTIC)

```python
def test_ir_plan_documented_and_reviewed_annually(
    controls_evidence: dict,
    reference_date: date,
):
    """
    3.6.1: Establish an operational incident-handling capability for the CUI
    system. IRP must be documented, reviewed at least annually, and tested.
    """
    ir = controls_evidence.get("nist_ir", {})
    irp = ir.get("incident_response_plan", {}) if ir else {}
    assert irp, "3.6.1: No incident response plan found in evidence"
    assert irp.get("plan_document"), "IRP document reference missing"
    assert irp.get("contacts_current", False), (
        "3.6.1: IRP does not have current contact information for incident handlers"
    )

    last_review = irp.get("last_review_date")
    assert last_review, "IRP lacks a last review date"
    age = (reference_date - date.fromisoformat(str(last_review))).days / 30.44
    assert age <= IR_PLAN_REVIEW_MONTHS, (
        f"3.6.1: IRP last reviewed {age:.0f} months ago (threshold: {IR_PLAN_REVIEW_MONTHS} months)"
    )


def test_ir_external_reporting_capability_documented(
    controls_evidence: dict,
):
    """
    3.6.1: IRP must include capability to report incidents to organizational
    officials and external entities (US-CERT, DoD DIBNet, etc.).
    ASSUME-800171-IR-001: DoD contractors must report to US-CERT/DIBNet within
    72 hours; report to CISA if a critical infrastructure sector.
    """
    ir = controls_evidence.get("nist_ir", {})
    irp = ir.get("incident_response_plan", {}) if ir else {}
    if not irp:
        pytest.skip("No IRP in evidence")
    assert irp.get("external_reporting_contacts"), (
        "3.6.1: IRP lacks external reporting contacts (US-CERT, DoD DIBNet, CISA, etc.)"
    )
    assert irp.get("reporting_thresholds_defined"), (
        "3.6.1: IRP lacks defined thresholds for what constitutes a reportable incident"
    )
```

### 3.6.2 — Incident tracking and management (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-800171-IR-001",
    description=(
        "DoD contractors must report incidents affecting CUI to US-CERT/DIBNet within "
        "72 hours per DFARS 252.204-7012. This is the minimum reporting threshold; "
        "specific contract requirements may impose shorter deadlines."
    ),
    approved_by="ISSO",
    review_date="2027-01",
)
def test_ir_incident_tracking_system_in_use(
    controls_evidence: dict,
):
    """
    3.6.2: Track, document, and report incidents to appropriate officials.
    Ad hoc tracking (email only) is insufficient for CUI systems.
    """
    ir = controls_evidence.get("nist_ir", {})
    tracking = ir.get("incident_tracking", {}) if ir else {}
    assert tracking, "3.6.2: No incident tracking system documented"
    assert tracking.get("system_name"), "3.6.2: Incident tracking tool not identified"
    assert tracking.get("incidents_logged_to_system"), (
        "3.6.2: Incidents are not being logged to the tracking system (evidence of use required)"
    )
```

### 3.6.3 — Incident response testing (Pattern 1 — DETERMINISTIC)

```python
def test_ir_tested_annually(
    controls_evidence: dict,
    reference_date: date,
):
    """
    3.6.3: Test the incident response capability. Annual tabletop exercise or
    simulation required. Test results must be documented.
    """
    ir = controls_evidence.get("nist_ir", {})
    irp = ir.get("incident_response_plan", {}) if ir else {}
    last_test = irp.get("last_test_date") if irp else None
    assert last_test, "3.6.3: Incident response capability has never been tested"
    age = (reference_date - date.fromisoformat(str(last_test))).days / 30.44
    assert age <= IR_TEST_MONTHS, (
        f"3.6.3: IR capability last tested {age:.0f} months ago (threshold: {IR_TEST_MONTHS} months)"
    )
    assert irp.get("last_test_results_documented", False), (
        "3.6.3: IR test results not documented — must record findings and lessons learned"
    )
```

---

## 3.10 — Physical Protection (PE)

### 3.10.1 — Physical access authorizations (Pattern 1 — DETERMINISTIC)

```python
def test_pe_physical_access_list_maintained_and_reviewed(
    controls_evidence: dict,
    reference_date: date,
):
    """
    3.10.1: Limit physical access to CUI systems and facilities to authorized
    individuals. Access authorization list must exist and be reviewed semi-annually.
    ASSUME-800171-PE-001: semi-annual review cycle = 6-month threshold.
    """
    pe = controls_evidence.get("nist_pe", {})
    access_list = pe.get("physical_access_authorization", {}) if pe else {}
    assert access_list, "3.10.1: No physical access authorization list found"
    assert access_list.get("access_list"), "3.10.1: Physical access list is empty"

    last_review = access_list.get("last_review_date")
    assert last_review, "Physical access list lacks a review date"
    age = (reference_date - date.fromisoformat(str(last_review))).days / 30.44
    assert age <= PHYSICAL_ACCESS_REVIEW_MONTHS, (
        f"3.10.1: Physical access list last reviewed {age:.0f} months ago "
        f"(threshold: {PHYSICAL_ACCESS_REVIEW_MONTHS} months)"
    )


def test_pe_physical_access_controls_in_place(
    controls_evidence: dict,
):
    """3.10.1/3.10.2: Physical access controls (badge readers, locks, guards) installed."""
    pe = controls_evidence.get("nist_pe", {})
    physical_controls = pe.get("physical_access_controls", {}) if pe else {}
    assert physical_controls, "3.10.2: No physical access controls documented"
    assert physical_controls.get("entry_control_mechanism"), (
        "3.10.2: No entry control mechanism documented (badge readers, keypads, locks, guards)"
    )
```

### 3.10.3 — Visitor management and escort (Pattern 1 — DETERMINISTIC)

```python
def test_pe_visitors_escorted_and_logged(
    controls_evidence: dict,
):
    """
    3.10.3: Escort visitors and monitor visitor activity. Visitor logs maintained
    for CUI areas. ASSUME-800171-PE-002: 3-year visitor log retention.
    """
    pe = controls_evidence.get("nist_pe", {})
    visitor_mgmt = pe.get("visitor_management", {}) if pe else {}
    assert visitor_mgmt, "3.10.3: No visitor management procedures documented"
    assert visitor_mgmt.get("escort_required", False), (
        "3.10.3: Visitor escort not required in CUI areas"
    )
    assert visitor_mgmt.get("visitor_log_maintained", False), (
        "3.10.3: Visitor log not maintained for CUI areas"
    )
    assert visitor_mgmt.get("log_retention_months", 0) >= VISITOR_LOG_RETENTION_MONTHS, (
        f"3.10.3: Visitor log retention {visitor_mgmt.get('log_retention_months')} months "
        f"below {VISITOR_LOG_RETENTION_MONTHS}-month threshold"
    )
```

### 3.10.6 — CUI-capable device removal and disposal (Pattern 2 — PARAMETERIZED)

```python
def test_pe_alternative_work_site_controls(
    controls_evidence: dict,
    entity_profile: dict,
):
    """
    3.10.6: Enforce safeguarding measures for CUI at alternate work sites
    (e.g., home offices). Remote workers with access to CUI must have
    documented alternative work site controls.
    """
    if not entity_profile.get("has_remote_workers_with_cui_access", False):
        pytest.skip("No remote workers with CUI access — 3.10.6 not applicable")

    pe = controls_evidence.get("nist_pe", {})
    alt_site = pe.get("alternative_work_site_controls", {}) if pe else {}
    assert alt_site, "3.10.6: No alternative work site controls documented"
    assert alt_site.get("policy_documented"), "Alternative work site CUI policy not documented"
    assert alt_site.get("employee_acknowledgement_required"), (
        "3.10.6: Employees with CUI access at alternative sites not required to acknowledge controls"
    )
```

---

## 3.7 — Maintenance (MA)

### 3.7.5 — Remote maintenance controls (Pattern 1 — DETERMINISTIC)

```python
def test_ma_remote_maintenance_monitored_and_authenticated(
    controls_evidence: dict,
    entity_profile: dict,
):
    """
    3.7.5: Require MFA for remote maintenance sessions. Log all remote
    maintenance connections and activities.
    """
    if not entity_profile.get("has_remote_maintenance", False):
        pytest.skip("No remote maintenance performed — 3.7.5 not applicable")

    ma = controls_evidence.get("nist_ma", {})
    remote_ma = ma.get("remote_maintenance", {}) if ma else {}
    assert remote_ma, "3.7.5: No remote maintenance controls documented"
    assert remote_ma.get("mfa_required", False), (
        "3.7.5: MFA not required for remote maintenance sessions"
    )
    assert remote_ma.get("sessions_logged", False), (
        "3.7.5: Remote maintenance sessions are not logged"
    )
    assert remote_ma.get("sessions_terminated_after_use", False), (
        "3.7.5: Remote maintenance sessions are not terminated after use — "
        "persistent maintenance access is not permitted"
    )
```

---

## 3.8 — Media Protection (MP)

### 3.8.1 — Media access control (Pattern 1 — DETERMINISTIC)

```python
def test_mp_access_to_cui_media_controlled(
    controls_evidence: dict,
):
    """
    3.8.1: Protect system media containing CUI, both paper and digital.
    Physical media (hard drives, USB, paper) with CUI must be access-controlled.
    """
    mp = controls_evidence.get("nist_mp", {})
    media_access = mp.get("media_access_control", {}) if mp else {}
    assert media_access, "3.8.1: No CUI media access controls documented"
    assert media_access.get("digital_media_access_controlled", False), (
        "3.8.1: Digital media (drives, USB) containing CUI not access-controlled"
    )
    assert media_access.get("paper_media_controlled", False), (
        "3.8.1: Paper media containing CUI not secured"
    )
```

### 3.8.3 — Media sanitization (NIST 800-88) (Pattern 1 — DETERMINISTIC)

```python
def test_mp_media_sanitized_before_reuse_or_disposal(
    controls_evidence: dict,
):
    """
    3.8.3: Sanitize or destroy system media before disposal or reuse.
    NIST SP 800-88 methods required. DoD 5220.22-M is not recommended
    (superseded by 800-88 for most media types).
    """
    mp = controls_evidence.get("nist_mp", {})
    sanitization = mp.get("media_sanitization", {}) if mp else {}
    assert sanitization, "3.8.3: No media sanitization procedures documented"
    assert sanitization.get("nist_800_88_compliant", False), (
        "3.8.3: Media sanitization does not follow NIST SP 800-88 guidelines"
    )
    accepted_methods = frozenset({
        "clear", "purge", "destroy",
        "cryptographic_erase", "degauss", "shred", "incinerate"
    })
    method = sanitization.get("method_for_digital", "").lower()
    assert any(m in method for m in accepted_methods) or sanitization.get("method_validated", False), (
        f"3.8.3: Sanitization method '{method}' not recognized as 800-88 compliant"
    )


def test_mp_media_disposal_log_maintained(
    controls_evidence: dict,
):
    """3.8.3: Maintain records of media disposal including method, date, and asset."""
    mp = controls_evidence.get("nist_mp", {})
    sanitization = mp.get("media_sanitization", {}) if mp else {}
    assert sanitization.get("disposal_log_maintained", False), (
        "3.8.3: No media disposal log maintained — records required for CUI media"
    )
```

### 3.8.7 — Removable media use control (Pattern 1 — DETERMINISTIC)

```python
def test_mp_removable_media_controlled_on_cui_systems(
    controls_evidence: dict,
):
    """
    3.8.7: Control the use of removable media on CUI system components.
    USB ports should be restricted; only pre-approved media permitted.
    ASSUME-800171-CM-002: USB restricted (see CM family).
    """
    mp = controls_evidence.get("nist_mp", {})
    removable = mp.get("removable_media_control", {}) if mp else {}
    assert removable, "3.8.7: No removable media controls documented"
    assert removable.get("usage_restricted", False), (
        "3.8.7: Removable media use not restricted on CUI systems"
    )
    assert removable.get("restriction_mechanism"), (
        "3.8.7: No technical mechanism restricting removable media "
        "(USB port disabling, endpoint agent, etc.)"
    )
```

---

## 3.9 — Personnel Security (PS)

### 3.9.1 — Screen individuals prior to CUI access (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-800171-PS-001",
    description=(
        "Personnel screening for CUI access must be commensurate with the risk; "
        "DoD contracts typically require NACI or equivalent background investigation; "
        "screening must be completed before CUI access is granted, not after."
    ),
    approved_by="HR / Security Officer",
    review_date="2027-01",
)
def test_ps_personnel_screened_before_cui_access(
    controls_evidence: dict,
):
    """
    3.9.1: Screen individuals prior to authorizing access to CUI.
    Background investigation commensurate with risk required before access.
    """
    ps = controls_evidence.get("nist_ps", {})
    screening = ps.get("personnel_screening", {}) if ps else {}
    assert screening, "3.9.1: No personnel screening program documented"
    assert screening.get("screening_before_access", False), (
        "3.9.1: Personnel screening not confirmed as a pre-condition to CUI access"
    )
    assert screening.get("screening_criteria_documented"), (
        "3.9.1: Personnel screening criteria not documented"
    )
```

### 3.9.2 — Termination and transfer actions (Pattern 1 — DETERMINISTIC)

```python
def test_ps_termination_triggers_immediate_account_revocation(
    controls_evidence: dict,
    reference_date: date,
):
    """
    3.9.2: Protect CUI during and after personnel actions including terminations.
    Account access must be revoked on or before the termination date.
    ASSUME-800171-PS-001: same-day revocation is the target; any open accounts
    after confirmed termination date constitute a violation.
    """
    ps = controls_evidence.get("nist_ps", {})
    termination = ps.get("termination_procedures", {}) if ps else {}
    assert termination, "3.9.2: No termination procedures documented"
    assert termination.get("account_revocation_on_termination", False), (
        "3.9.2: Account revocation on personnel termination not documented as a required step"
    )
    assert termination.get("credential_return_required", False), (
        "3.9.2: Return of credentials (badges, tokens, etc.) not required on termination"
    )

    # Check for open accounts belonging to terminated personnel
    terminated_with_access = termination.get("open_accounts_post_termination", [])
    assert not terminated_with_access, (
        f"3.9.2: {len(terminated_with_access)} terminated personnel still have active accounts: "
        f"{terminated_with_access}"
    )
```

---

## 3.12 — Security Assessment (CA)

### 3.12.1 — Security assessment conducted periodically (Pattern 2 — PARAMETERIZED)

```python
@pytest.mark.assumption(
    id="ASSUME-800171-CA-001",
    description=(
        "3.12.1: Security controls assessed at least triennially (every 3 years) for "
        "CUI systems; annual self-assessments recommended for CMMC alignment; "
        "assessment results documented in a Security Assessment Report (SAR)."
    ),
    approved_by="ISSO",
    review_date="2027-01",
)
def test_ca_security_assessment_current(
    controls_evidence: dict,
    reference_date: date,
):
    """
    3.12.1: Periodically assess security controls. Triennial full assessment minimum.
    Annual self-assessment aligns with CMMC affirmation schedule.
    """
    ca = controls_evidence.get("nist_ca", {})
    assessment = ca.get("security_assessment", {}) if ca else {}
    assert assessment, "3.12.1: No security assessment records found"

    last_assessment = assessment.get("last_assessment_date")
    assert last_assessment, "Security assessment lacks a last assessment date"
    age = (reference_date - date.fromisoformat(str(last_assessment))).days / 30.44
    assert age <= SECURITY_ASSESSMENT_MONTHS, (
        f"3.12.1: Security assessment last conducted {age:.0f} months ago "
        f"(threshold: {SECURITY_ASSESSMENT_MONTHS} months)"
    )
    assert assessment.get("sar_documented", False), (
        "3.12.1: No Security Assessment Report (SAR) found — assessment results must be documented"
    )
```

### 3.12.2 — Plan of Action and Milestones (POA&M) (Pattern 1 — DETERMINISTIC)

```python
def test_ca_poam_maintained_with_no_overdue_critical_items(
    controls_evidence: dict,
    reference_date: date,
):
    """
    3.12.2: Develop and implement plans of action to correct deficiencies.
    No critical (CVSS≥9.0) or actively exploited items may be overdue.
    ASSUME-800171-CA-001: critical ≤30-day; high ≤90-day remediation.
    """
    ca = controls_evidence.get("nist_ca", {})
    poam = ca.get("plan_of_action", {}) if ca else {}
    if not poam:
        pytest.skip("No POA&M in evidence (no known deficiencies)")

    open_items = poam.get("open_items", [])
    violations = []
    for item in open_items:
        severity = item.get("severity", "medium").lower()
        threshold = POAM_CRITICAL_DAYS if severity in ("critical", "kev") else (
            POAM_HIGH_DAYS if severity == "high" else 180
        )
        opened = date.fromisoformat(str(item["opened_date"]))
        deadline = opened + timedelta(days=threshold)
        if reference_date > deadline:
            violations.append({
                "id": item.get("id", "unknown"),
                "severity": severity,
                "overdue_days": (reference_date - deadline).days,
            })

    assert not violations, (
        f"3.12.2: Overdue POA&M items: "
        + ", ".join(f"{v['id']} ({v['severity']}, {v['overdue_days']}d overdue)" for v in violations)
    )
```

### 3.12.4 — System Security Plan (SSP) (Pattern 2 — PARAMETERIZED)

```python
def test_ca_ssp_documented_and_current(
    controls_evidence: dict,
    reference_date: date,
):
    """
    3.12.4: Develop, document, and periodically update a system security plan
    describing system boundaries, operating environment, implemented security
    requirements, and relationships with other systems.
    """
    ca = controls_evidence.get("nist_ca", {})
    ssp = ca.get("system_security_plan", {}) if ca else {}
    assert ssp, "3.12.4: No System Security Plan (SSP) found in evidence"
    assert ssp.get("system_boundary_defined"), "SSP lacks a defined system boundary"
    assert ssp.get("all_requirements_documented"), (
        "3.12.4: SSP does not document implementation status for all 800-171 requirements"
    )
    last_review = ssp.get("last_review_date")
    assert last_review, "SSP lacks a review date"
    age = (reference_date - date.fromisoformat(str(last_review))).days / 30.44
    assert age <= 12, (
        f"3.12.4: SSP last reviewed {age:.0f} months ago — annual review recommended"
    )
```

---

## Open assumptions

| ID | Assumption | Pattern | Approved | Review |
|---|---|---|---|---|
| ASSUME-800171-SC-001 | TLS minimum version 1.2; SSL and TLS ≤1.1 disabled; FIPS-validated cipher suites required for federal contractors; AES-128 minimum at rest; AES-256 preferred; VLAN isolation is the minimum network segmentation | 1 | Pending | 2027-01 |
| ASSUME-800171-SC-002 | Session termination inactivity timeout = 30 minutes; applies to web sessions, remote desktop, and authenticated CLI sessions in the CUI boundary | 1 | Pending | 2027-01 |
| ASSUME-800171-SC-003 | Key management lifecycle must document all 5 phases; adequacy of key generation entropy and storage HSM-level is Pattern 2 | 2 | Pending | 2027-01 |
| ASSUME-800171-IR-001 | DoD contractors report CUI-affecting incidents to US-CERT/DIBNet within 72 hours per DFARS 252.204-7012; report to CISA if critical infrastructure sector; IRP must name specific external reporting contacts | 1 | Pending | 2027-01 |
| ASSUME-800171-PE-001 | Physical access list reviewed semi-annually (6-month threshold); removal of departed/role-changed personnel from access list must be same-day | 1 | Pending | 2027-01 |
| ASSUME-800171-PE-002 | Visitor log retention = 36 months (3 years); logs must include name, affiliation, sponsoring employee, date/time in/out, and areas visited | 1 | Pending | 2027-01 |
| ASSUME-800171-PS-001 | Same-day account revocation on termination; termination procedure includes account revocation, credential return, and CUI access confirmation; screening must be completed before access is granted | 1 | Pending | 2027-01 |
| ASSUME-800171-CA-001 | Triennial full assessment minimum; annual self-assessment for CMMC alignment; critical POA&M items ≤30 days; high ≤90 days; SSP reviewed annually | 1 | Pending | 2027-01 |
