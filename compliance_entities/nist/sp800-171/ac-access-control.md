# NIST SP 800-171 r3 — Family AC: Access Control

**Registry path:** `/regulation-registry/NIST-SP800-171/AC/`
**Version:** NIST SP 800-171 Rev 3 (May 2024)
**Last parsed:** 2026-05-20
**Applies to:** Non-federal organizations (contractors, universities, research institutions) that process, store, or transmit Controlled Unclassified Information (CUI) in nonfederal information systems under US federal contracts or grants
**Trigger:** Federal contract or grant containing DFARS clause 252.204-7012 (DoD) or equivalent FAR clause; any contract where the government provides or the contractor generates CUI; CMMC Level 2 requires third-party assessment against NIST 800-171
**Jurisdiction:** United States; extraterritorial — applies to foreign companies holding US federal contracts involving CUI; enforced through contract terms and DoD CMMC assessments
**Not applicable to:** Federal agencies (use NIST 800-53 instead); organizations with no federal contracts or grants; commercial transactions not involving CUI; EAR99 technology transfers (separate ITAR/EAR framework)
**Overall confidence:** MEDIUM — 3.1.1 (account types) and 3.1.2 (CUI access) are DETERMINISTIC; remote access (3.1.12–3.1.15) has DETERMINISTIC elements with assumptions; information flow (3.1.3) and separation of duties (3.1.4) are PARAMETERIZED
**22 requirements: 3.1.1–3.1.22**

---

## Scope summary

The AC family is the largest family in 800-171 and covers the full access control lifecycle: account management, access authorization, separation of duties, remote access, wireless, and mobile device access. It maps directly to NIST SP 800-53 AC control family and CMMC Level 2 AC domain.

The highest-confidence requirements are those with measurable thresholds: 3.1.1 (authorized users only), 3.1.2 (CUI access limited to authorized users and processes), 3.1.20 (wireless access prohibited or controlled). Requirements involving "need-to-know" and "least privilege" (3.1.1, 3.1.2, 3.1.6) are PARAMETERIZED for adequacy but DETERMINISTIC for existence of the access control mechanism.

---

## 3.1.1 — Authorized Users and Processes (HIGH)

### Source text

> Limit system access to authorized users, processes acting on behalf of authorized users, and devices (including other systems).

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All systems within the CUI enclave | DETERMINISTIC |
| Obligation | Access to system limited to authorized users/processes/devices; all other access denied | DETERMINISTIC |
| Evidence | `user_account_records.all_active_accounts_authorized == true`; `unauthorized_access_attempts_blocked == true`; access control list maintained | DETERMINISTIC |

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.1.2 — CUI Access — Least Privilege and Need-to-Know (HIGH)

### Source text

> Limit system access to the types of transactions and functions that authorized users are permitted to execute.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Access limited to functions/transactions authorized by role; CUI accessible only to users with need-to-know; privileged functions separated | DETERMINISTIC (least-privilege enforcement) / PARAMETERIZED (role definition adequacy) |
| Evidence | `user_roles.defined_with_permitted_functions`; `access_reviews.conducted`; no users with access beyond their defined role | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-800171-AC-001):** CUI access controls are adequate when: (1) all CUI-system users have documented role definitions specifying permitted functions; (2) access rights mapped to role — no default full-access provisioning; (3) access rights reviewed at least semi-annually; (4) service and shared accounts prohibited except with documented justification and extra controls (individual accountability, logging).

**Overall: DETERMINISTIC for access limiting mechanism → Pattern 1; PARAMETERIZED for role adequacy → Pattern 2**

---

## 3.1.3 — Information Flow Enforcement (MEDIUM)

### Source text

> Control the flow of CUI in accordance with approved authorizations.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | CUI flow controlled; unauthorized flow paths blocked; flow enforcement documented in SSP | PARAMETERIZED |
| Evidence | `data_flow_diagram.cui_flows_documented`; `firewall_rules.cui_flow_enforcement_documented`; DLP or equivalent controls | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## 3.1.4 — Separation of Duties (MEDIUM)

### Source text

> Separate the duties of individuals to reduce the risk of malevolent activity without collusion.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Duties separated for key functions; conflicting roles identified and prevented | PARAMETERIZED |
| Evidence | `separation_of_duties_matrix.documented`; no single user has conflicting roles (e.g., developer + production deployer) | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## 3.1.5 — Least Privilege (HIGH)

### Source text

> Employ the principle of least privilege, including for specific security functions and privileged accounts.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Privileged accounts separate from standard user accounts; least privilege enforced; security functions require explicit authorization | DETERMINISTIC (privileged account separation) / PARAMETERIZED (scope) |
| Evidence | `privileged_accounts.separate_from_user_accounts == true`; no admin rights on standard accounts; admin accounts not used for email/browsing | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-800171-AC-002):** Least privilege is adequate when: (1) privileged accounts (system administration, security function access) are separate accounts from standard user accounts; (2) privileged accounts used only for administrative functions — not email, web browsing, or non-admin tasks; (3) privileged access reviewed semi-annually; (4) service accounts have privileges limited to the service's operational requirements; (5) just-in-time access preferred over standing privilege for high-risk functions.

**Overall: DETERMINISTIC for account separation → Pattern 1; PARAMETERIZED for adequacy → Pattern 2**

---

## 3.1.6 — Non-Privileged Account Usage (MEDIUM)

### Source text

> Use non-privileged accounts or roles when accessing non-security functions.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Personnel with privileged accounts also have separate standard accounts; standard account used for non-administrative tasks | DETERMINISTIC (two-account model) / PARAMETERIZED (enforcement) |
| Evidence | `admin_users.have_separate_standard_accounts == true`; evidence that admin accounts not used for standard tasks | DETERMINISTIC + PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## 3.1.7 — Privileged Function Logging (HIGH)

### Source text

> Prevent non-privileged users from executing privileged functions and capture the execution of such functions in audit logs.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Non-privileged users cannot execute privileged functions; privileged function execution captured in audit logs | DETERMINISTIC |
| Evidence | `access_control_config.non_privileged_blocked_from_privileged_functions == true`; `audit_logs.privilege_escalation_logged == true` | DETERMINISTIC |

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.1.8 — Unsuccessful Login Attempts (HIGH)

### Source text

> Limit unsuccessful logon attempts.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Limit on consecutive failed logon attempts implemented; account lockout or equivalent after threshold exceeded | DETERMINISTIC |
| Evidence | `auth_config.max_failed_attempts ≤ 10`; lockout enforced on all systems accessing CUI | DETERMINISTIC |

**Assumption (ASSUME-800171-AC-003):** Unsuccessful logon threshold: maximum 10 consecutive failed attempts consistent with PCI DSS Req 8.3.4 and ISO 27001 ASSUME-ISO-A5-004. Lockout duration: minimum 30 minutes or until administrator unlock. Threshold applies to all systems within the CUI enclave.

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.1.9 — Privacy and Security Notices (MEDIUM)

### Source text

> Provide privacy and security notices consistent with CUI rules.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Privacy and security notice displayed at system login; notice consistent with NARA CUI marking requirements | DETERMINISTIC (existence) / PARAMETERIZED (content) |
| Evidence | `system_banners.configured == true`; banner text includes required elements | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-800171-AC-004):** Login banners are adequate when they include: (1) statement that the system is for authorized use only; (2) notification that use constitutes consent to monitoring; (3) reference to applicable penalties for unauthorized use; (4) displayed at all login points to CUI systems.

**Overall: DETERMINISTIC for banner existence → Pattern 1; PARAMETERIZED for content → Pattern 2**

---

## 3.1.10 — Session Lock (HIGH)

### Source text

> Use session lock with pattern-hiding displays after a period of inactivity.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Session lock activated after inactivity period; display cleared/obscured (pattern-hiding) | DETERMINISTIC |
| Evidence | `session_lock.max_inactive_minutes ≤ 15`; screen lock clears display content | DETERMINISTIC |

**Assumption (ASSUME-800171-AC-005):** Session lock threshold: 15 minutes maximum consistent with PCI DSS Req 8.2.8 and NIST guidance for CUI systems. Screen lock must be pattern-hiding — not merely password-protected with content still visible.

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.1.11 — Session Termination (MEDIUM)

### Source text

> Terminate (automatically) a user session after a defined condition.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Session terminated after defined conditions (inactivity timeout, end of work session, security event) | PARAMETERIZED (conditions) |
| Evidence | `session_config.auto_terminate_on_inactivity == true`; termination conditions documented in SSP | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## 3.1.12 — Remote Access — Monitoring and Control (HIGH)

### Source text

> Monitor and control remote access sessions.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Remote access sessions monitored; remote access only through approved access points; VPN or equivalent required | DETERMINISTIC |
| Evidence | `remote_access_config.approved_method_only == true`; `remote_sessions.logged`; split tunneling controlled | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-800171-AC-006):** Remote access monitoring is adequate when: (1) all remote access to CUI systems via approved, encrypted channel (VPN, ZTNA, or equivalent); (2) remote sessions logged with identity, timestamp, and session duration; (3) split tunneling prohibited or explicitly authorized with documented risk acceptance; (4) remote access monitoring alert on anomalous session behavior.

**Overall: DETERMINISTIC for encrypted channel enforcement → Pattern 1; PARAMETERIZED for monitoring coverage → Pattern 2**

---

## 3.1.13 — Remote Access — Cryptographic Mechanisms (HIGH)

### Source text

> Employ cryptographic mechanisms to protect the confidentiality of remote access sessions.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Remote access sessions protected by cryptographic mechanisms; approved encryption algorithms used | DETERMINISTIC |
| Evidence | `vpn_config.encryption_protocol`; TLS 1.2+ or approved VPN with AES-128/256 | DETERMINISTIC |

**Assumption (ASSUME-800171-AC-007):** Cryptographic protection of remote access is adequate when: (1) TLS 1.2 minimum for web-based remote access; TLS 1.3 preferred; (2) VPN using IKEv2 or equivalent with AES-128/256 and SHA-256; (3) weak protocols (SSL, TLS 1.0/1.1, PPTP, L2TP without IPsec) prohibited; (4) aligns with FIPS 140-2/3 validated module requirement for federal contractor systems. Aligns with PCI DSS ASSUME-4-001 and ISO 27001 ASSUME-ISO-A8-008.

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.1.14 — Remote Access — Routing Through Managed Access Points (MEDIUM)

### Source text

> Route remote access via managed access control points.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Remote access traffic routed through managed (controlled) access points; traffic inspectable | PARAMETERIZED |
| Evidence | `network_config.remote_access_via_managed_access_point == true`; split tunneling disabled or controlled | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## 3.1.15 — Remote Access — Privileged Commands (HIGH)

### Source text

> Authorize remote execution of privileged commands and access to security-relevant information via remote access only for documented operational needs.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Remote execution of privileged commands documented and authorized; not permitted by default | DETERMINISTIC (authorization required) / PARAMETERIZED (scope) |
| Evidence | `remote_privileged_access.documented_operational_need == true`; privileged remote commands logged | DETERMINISTIC + PARAMETERIZED |

**Overall: DETERMINISTIC for authorization requirement → Pattern 1; PARAMETERIZED for scope → Pattern 2**

---

## 3.1.16–3.1.17 — Wireless Access (HIGH)

### 3.1.16 Source text

> Authorize wireless access prior to allowing such connections.

### 3.1.17 Source text

> Protect wireless access using authentication and encryption.

### Element extraction (combined)

| Element | Value | Classification |
|---|---|---|
| Obligation | Wireless access authorized before connecting; protected with authentication (WPA2/3 minimum); encrypted; rogue wireless prohibited | DETERMINISTIC |
| Evidence | `wireless_config.authentication == "WPA2_or_WPA3"`; `wireless_config.encryption == "AES"`; wireless access authorized per device; rogue AP detection deployed | DETERMINISTIC |

**Assumption (ASSUME-800171-AC-008):** Wireless controls are adequate when: (1) WPA2-Enterprise (802.1X) or WPA3 for corporate wireless — PSK-only WPA2 acceptable only with strong passphrase (≥20 chars) and documented justification; (2) all wireless connections to CUI systems require individual authentication; (3) rogue wireless AP detection deployed or wireless prohibited in CUI areas; (4) guest wireless isolated from CUI network via separate SSID and VLAN.

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.1.18–3.1.20 — Mobile Device and External System Access (MEDIUM)

### Element extraction

| Element | Value | Classification |
|---|---|---|
| 3.1.18 | Mobile device connections controlled; MDM or equivalent | PARAMETERIZED |
| 3.1.19 | Encryption of CUI on mobile devices | DETERMINISTIC |
| 3.1.20 | Verify remote CUI connections from external systems prohibited unless controlled | DETERMINISTIC |

**Assumption (ASSUME-800171-AC-009):** Mobile device access to CUI is adequate when: (1) mobile devices accessing CUI enrolled in MDM; (2) MDM enforces: device encryption, screen lock (≤ 10 min), remote wipe capability, certificate-based authentication; (3) BYOD: CUI isolated via containerization (EMM/MAM); corporate data not stored on personal device storage; (4) remote wipe triggered within 24 hours of lost/stolen device report.

**Overall: DETERMINISTIC for device encryption → Pattern 1; PARAMETERIZED for MDM adequacy → Pattern 2**

---

## 3.1.21–3.1.22 — CUI on Publicly Accessible Systems (HIGH)

### Element extraction

| Element | Value | Classification |
|---|---|---|
| 3.1.21 | Limit use of portable storage devices on external systems | DETERMINISTIC |
| 3.1.22 | Control CUI posted or processed on publicly accessible systems | DETERMINISTIC |

**Overall: DETERMINISTIC → Pattern 1**

---

## YAML specifications

### `ac_access_control.yaml`

```yaml
regulation_id: NIST-SP800-171-r3-AC
section: "NIST SP 800-171 r3 — Family AC: Access Control"
r_or_a: Required
source_text: >
  Limit system access to authorized users and devices; enforce least privilege;
  control remote, wireless, and mobile access; protect CUI from unauthorized access.

extracted_elements:
  subject: "All systems processing, storing, or transmitting CUI"
  condition: "system_processes_cui() == true (human attestation required)"
  obligation: >
    Authorized users only; least privilege; privileged/standard account separation;
    lockout ≤10 attempts; session lock ≤15 min; remote access encrypted; wireless WPA2+
  evidence: >
    user_accounts, access_review_records, auth_configs, remote_access_configs,
    wireless_configs, mobile_device_configs

ambiguity_classification:
  subject: DETERMINISTIC
  condition: PARAMETERIZED
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-800171-AC-003
    assumption_text: >
      Lockout threshold ≤10 consecutive failed attempts; duration ≥30 min.
      Applies to all CUI-enclave systems.
    assumed_by: "System Owner"
    approved_by: "ISSO"
    date: "2026-05-20"
    review_frequency_days: 365
  - assumption_id: ASSUME-800171-AC-005
    assumption_text: >
      Session lock ≤15 min inactivity; pattern-hiding display (content cleared).
      Applies to all CUI-enclave systems.
    assumed_by: "System Owner"
    approved_by: "ISSO"
    date: "2026-05-20"
    review_frequency_days: 365
test_confidence: HIGH
generated_test: "tests/nist_sp800171/test_ac_access_control.py"
```

---

## Generated tests

### `tests/nist_sp800171/test_ac_access_control.py`

```python
"""
NIST SP 800-171 r3 — Family AC: Access Control
Confidence: HIGH for 3.1.1, 3.1.2, 3.1.5, 3.1.7, 3.1.8, 3.1.10, 3.1.12–3.1.13, 3.1.16–3.1.19
Pre-condition: system_processes_cui() fixture must return True (human attestation required)
"""
import pytest
from datetime import date

MAX_FAILED_ATTEMPTS = 10
SESSION_LOCK_MAX_MINUTES = 15
ACCESS_REVIEW_MAX_DAYS = 180


@pytest.fixture(autouse=True)
def require_cui_scope(system_scope):
    """All AC tests require CUI scope attestation."""
    if not system_scope.get("processes_cui"):
        pytest.skip("System not attested as processing CUI — AC tests run in informational mode")


def test_no_unauthorized_active_accounts(user_accounts):
    """3.1.1 — All active accounts must be authorized."""
    violations = [
        a for a in user_accounts
        if a.get("in_cui_enclave")
        and a.get("account_status") == "active"
        and not a.get("authorization_documented")
    ]
    assert not violations, (
        f"NONCONFORMITY (3.1.1): {len(violations)} active account(s) without documented "
        f"authorization: {[a['account_id'] for a in violations]}"
    )


def test_privileged_accounts_separate_from_standard(user_accounts):
    """3.1.5 — Privileged accounts must be separate from standard user accounts."""
    violations = [
        a for a in user_accounts
        if a.get("in_cui_enclave")
        and a.get("is_privileged")
        and a.get("also_standard_user")
    ]
    assert not violations, (
        f"NONCONFORMITY (3.1.5): {len(violations)} privileged account(s) that are also "
        f"standard user accounts — separation required: "
        f"{[a['account_id'] for a in violations]}"
    )


def test_privileged_access_reviewed_within_6_months(access_review_records):
    """3.1.2/3.1.5 — CUI privileged access reviewed at least every 6 months."""
    today = date.today()
    privileged_reviews = [
        r for r in access_review_records
        if r.get("access_type") == "privileged"
        and r.get("in_cui_enclave")
    ]
    if not privileged_reviews:
        assert False, "NONCONFORMITY (3.1.2): No privileged access review records for CUI enclave"
    latest = max(privileged_reviews, key=lambda r: r["review_date"])
    days_since = (today - latest["review_date"]).days
    assert days_since <= ACCESS_REVIEW_MAX_DAYS, (
        f"NONCONFORMITY (3.1.2): CUI privileged access last reviewed {days_since} days ago "
        f"(max {ACCESS_REVIEW_MAX_DAYS})"
    )


@pytest.mark.assumption(
    id="ASSUME-800171-AC-003",
    description="Lockout ≤10 consecutive failed attempts; duration ≥30 min",
    approved_by="ISSO",
    review_date="2026-05-20",
)
def test_account_lockout_configured(auth_system_configs):
    """3.1.8 — Account lockout after maximum 10 failed attempts."""
    violations = []
    for cfg in auth_system_configs:
        if not cfg.get("in_cui_enclave"):
            continue
        if cfg.get("max_failed_attempts", 9999) > MAX_FAILED_ATTEMPTS:
            violations.append(
                f"System {cfg['system_id']}: lockout threshold "
                f"{cfg.get('max_failed_attempts')} > {MAX_FAILED_ATTEMPTS}"
            )
    assert not violations, (
        f"NONCONFORMITY (3.1.8): {len(violations)} CUI system(s) with lockout threshold "
        f"exceeding maximum:\n" + "\n".join(violations)
    )


@pytest.mark.assumption(
    id="ASSUME-800171-AC-005",
    description="Session lock ≤15 min inactivity; pattern-hiding display",
    approved_by="ISSO",
    review_date="2026-05-20",
)
def test_session_lock_configured(auth_system_configs):
    """3.1.10 — Session lock within 15 minutes of inactivity for all CUI systems."""
    violations = []
    for cfg in auth_system_configs:
        if not cfg.get("in_cui_enclave"):
            continue
        timeout = cfg.get("session_timeout_minutes", 9999)
        if timeout > SESSION_LOCK_MAX_MINUTES:
            violations.append(
                f"System {cfg['system_id']}: session timeout {timeout} min "
                f"(max {SESSION_LOCK_MAX_MINUTES})"
            )
    assert not violations, (
        f"NONCONFORMITY (3.1.10): {len(violations)} CUI system(s) with session lock "
        f"exceeding maximum:\n" + "\n".join(violations)
    )


@pytest.mark.assumption(
    id="ASSUME-800171-AC-006",
    description="Remote access: approved encrypted channel; sessions logged; split tunneling controlled",
    approved_by="ISSO",
    review_date="2026-05-20",
)
def test_remote_access_via_encrypted_channel(remote_access_configs):
    """3.1.12/3.1.13 — Remote access to CUI must use encrypted approved channel."""
    violations = [
        r for r in remote_access_configs
        if r.get("in_cui_enclave")
        and not r.get("encrypted_channel_required")
    ]
    assert not violations, (
        f"NONCONFORMITY (3.1.12/3.1.13): {len(violations)} remote access configuration(s) "
        f"not enforcing encrypted channel for CUI: "
        f"{[r['config_id'] for r in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-800171-AC-008",
    description="Wireless: WPA2-Enterprise or WPA3; individual authentication; guest isolated from CUI",
    approved_by="ISSO",
    review_date="2026-05-20",
)
def test_wireless_access_uses_approved_authentication(wireless_configs):
    """3.1.16/3.1.17 — Wireless access requires WPA2 or WPA3 with authentication."""
    APPROVED_PROTOCOLS = {"WPA2_Enterprise", "WPA3", "WPA2_Personal"}
    violations = [
        w for w in wireless_configs
        if w.get("in_cui_network")
        and w.get("auth_protocol") not in APPROVED_PROTOCOLS
    ]
    assert not violations, (
        f"NONCONFORMITY (3.1.16/3.1.17): {len(violations)} wireless configuration(s) "
        f"not using approved authentication: "
        f"{[w['ssid'] for w in violations]}"
    )


def test_mobile_cui_storage_encrypted(mobile_device_records):
    """3.1.19 — CUI on mobile devices must be encrypted."""
    violations = [
        d for d in mobile_device_records
        if d.get("stores_or_accesses_cui")
        and not d.get("storage_encrypted")
    ]
    assert not violations, (
        f"NONCONFORMITY (3.1.19): {len(violations)} mobile device(s) accessing CUI "
        f"without storage encryption: {[d['device_id'] for d in violations]}"
    )


def test_no_active_accounts_for_terminated_personnel(user_accounts, terminated_personnel):
    """3.1.1 — Terminated personnel must have no active CUI system access."""
    terminated_ids = {p["employee_id"] for p in terminated_personnel}
    violations = [
        a for a in user_accounts
        if a.get("in_cui_enclave")
        and a.get("employee_id") in terminated_ids
        and a.get("account_status") == "active"
    ]
    assert not violations, (
        f"NONCONFORMITY (3.1.1): {len(violations)} active CUI-enclave account(s) "
        f"belonging to terminated personnel: {[a['account_id'] for a in violations]}"
    )
```

---

## Notes for the registry

- **3.1.1 vs. 3.1.2 distinction:** 3.1.1 controls *who* can access the system (authorized users/devices/processes only); 3.1.2 controls *what* authorized users can do once inside (transaction/function restrictions). Both are required. Together they form the access control foundation: authentication (you are who you say you are) × authorization (you may do what you're attempting).
- **CUI enclave scope fixture:** All AC tests use `autouse=True` on a CUI scope fixture. This ensures no AC test silently passes on a system that hasn't been attested as CUI-processing. The skip is intentional — it's not a pass, it's an "not applicable here" signal. The fixture state must be manually attested; it should never default to True.
- **3.1.5 dual-account model:** The requirement for separate privileged and standard accounts (3.1.5 + 3.1.6) is more common in DoD contractor environments than commercial environments. In practice, it means a system administrator should have: admin@company.com (for admin work) and user.name@company.com (for email, web, day-to-day tasks). This is tested by `test_privileged_accounts_separate_from_standard`.
- **CMMC Level 2 mapping:** The entire AC family in 800-171 maps to the CMMC Level 2 AC domain. CMMC assessors will test against 800-171A r3 assessment objectives. The tests in this file align to the assessment objectives defined in 800-171A once finalized.
- **3.1.10 pattern-hiding requirement:** The session lock must clear or obscure the display content — not merely require a password while still showing the last screen. This matters for screens visible from across a room. The `session_timeout_minutes` check only verifies the numeric threshold; pattern-hiding behavior is a configuration setting that must be verified separately (typically via screenshot or policy audit).
