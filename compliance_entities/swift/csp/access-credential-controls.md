# SWIFT CSP — Access & Credential Controls (Objectives 3 & 4)

**Framework:** SWIFT Customer Security Programme (CSP) — CSCF v2025
**Controls:** 3.1, 3.2, 3.3, 4.1, 4.2, 4.3A, 4.4, 5.1, 5.2, 5.3A
**Objective:** Prevent Compromise of Credentials + Manage Identities and Segregate Privileges
**Confidence:** HIGH (3.1, 3.2, 4.1, 4.4, 5.1, 5.2) / MEDIUM (3.3, 4.2, 4.3A, 5.3A)
**Last parsed:** 2026-05-21
**Applies to:** All SWIFT member institutions with a direct connection to the SWIFT network — banks, broker-dealers, fund managers, custodians, and other financial institutions using SWIFT for financial messaging; service bureaus providing SWIFT connectivity on behalf of member institutions
**Trigger:** SWIFT network connectivity (live connection) — all connected institutions must self-attest annually against the Customer Security Controls Framework (CSCF) mandatory controls; self-attestation is required in the KYC Registry; non-attestation results in escalation to counterparties and supervisors
**Jurisdiction:** Global — SWIFT is an international cooperative headquartered in Belgium; CSCF applies to all member institutions worldwide regardless of jurisdiction
**Not applicable to:** Correspondent banking relationships where a non-SWIFT institution accesses SWIFT only through a SWIFT-connected correspondent (the downstream institution must comply, not the non-SWIFT upstream); entities that have disconnected from SWIFT

---

## Constants

```python
# Control 3.1 — Password policy
SWIFT_MIN_PASSWORD_LENGTH = 8
SWIFT_MIN_PRIVILEGED_PASSWORD_LENGTH = 12
SWIFT_PASSWORD_MAX_AGE_DAYS = 90
SWIFT_PASSWORD_HISTORY_COUNT = 5
SWIFT_PROHIBITED_PASSWORD_HASH_ALGORITHMS = frozenset({"md5", "sha1", "ntlm_md4"})

# Control 5.1 — Access review
SWIFT_ACCESS_REVIEW_MONTHS = 12

# Control 5.2 — Session protection
SWIFT_SESSION_TIMEOUT_MINUTES = 15
```

---

## Control 3.1 — Password Policy

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | All accounts accessing SWIFT infrastructure | DETERMINISTIC |
| Condition | Password-based authentication in use | DETERMINISTIC |
| Obligation | Minimum length 8 chars (12 for privileged); complexity enforced; 90-day rotation; no reuse within history count | DETERMINISTIC |
| Evidence | Password policy document; identity system configuration showing enforcement; privileged account config | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
import pytest
from datetime import date

@pytest.fixture(autouse=True)
def swift_scope(entity_profile: dict):
    if not entity_profile.get("is_swift_user", False):
        pytest.skip("Entity is not a SWIFT user — CSCF not applicable")

class TestControl3_1:
    """3.1 — Password Policy: enforced on all SWIFT accounts."""

    def test_minimum_password_length_standard_accounts(self, controls_evidence: dict):
        policy = controls_evidence.get("swift_password_policy", {})
        min_len = policy.get("min_length", 0)
        assert min_len >= SWIFT_MIN_PASSWORD_LENGTH, (
            f"SWIFT password policy minimum length must be ≥{SWIFT_MIN_PASSWORD_LENGTH}. "
            f"Current: {min_len}"
        )

    def test_minimum_password_length_privileged_accounts(self, controls_evidence: dict):
        policy = controls_evidence.get("swift_privileged_password_policy", {})
        min_len = policy.get("min_length", 0)
        assert min_len >= SWIFT_MIN_PRIVILEGED_PASSWORD_LENGTH, (
            f"Privileged SWIFT account password minimum length must be "
            f"≥{SWIFT_MIN_PRIVILEGED_PASSWORD_LENGTH}. Current: {min_len}"
        )

    def test_password_complexity_enforced(self, controls_evidence: dict):
        policy = controls_evidence.get("swift_password_policy", {})
        assert policy.get("complexity_enforced", False), (
            "Password complexity (mixed case, numbers, special characters) must be enforced"
        )

    def test_password_max_age(self, controls_evidence: dict):
        policy = controls_evidence.get("swift_password_policy", {})
        max_age = policy.get("max_age_days", 9999)
        assert max_age <= SWIFT_PASSWORD_MAX_AGE_DAYS, (
            f"Password maximum age must be ≤{SWIFT_PASSWORD_MAX_AGE_DAYS} days. "
            f"Current: {max_age}"
        )

    def test_password_history_enforced(self, controls_evidence: dict):
        policy = controls_evidence.get("swift_password_policy", {})
        history = policy.get("history_count", 0)
        assert history >= SWIFT_PASSWORD_HISTORY_COUNT, (
            f"Password history must prevent reuse of last {SWIFT_PASSWORD_HISTORY_COUNT} "
            f"passwords. Current: {history}"
        )

    def test_password_storage_algorithm_not_prohibited(self, controls_evidence: dict):
        identity_systems = controls_evidence.get("swift_identity_systems", [])
        for sys in identity_systems:
            algo = sys.get("password_hash_algorithm", "").lower()
            assert algo not in SWIFT_PROHIBITED_PASSWORD_HASH_ALGORITHMS, (
                f"System {sys.get('system_id')} uses prohibited hash algorithm '{algo}'"
            )
```

---

## Control 3.2 — Multi-Factor Authentication

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | All operators and administrators accessing SWIFT infrastructure | DETERMINISTIC |
| Condition | Access to SWIFT messaging interface, SWIFT operator PCs, or SWIFT zone systems | DETERMINISTIC |
| Obligation | MFA required for all operators; hardware token or equivalent; cannot be bypassed | DETERMINISTIC |
| Evidence | MFA enrollment records for all operator accounts; authentication system config showing MFA enforcement; no bypass accounts | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestControl3_2:
    """3.2 — Multi-Factor Authentication: mandatory for all SWIFT operators."""

    def test_all_swift_operator_accounts_have_mfa(self, controls_evidence: dict):
        operators = controls_evidence.get("swift_operator_accounts", [])
        no_mfa = [a for a in operators if not a.get("mfa_enrolled", False)]
        assert not no_mfa, (
            f"MFA must be enrolled for all SWIFT operator accounts. "
            f"Missing MFA: {[a['account_id'] for a in no_mfa]}"
        )

    def test_no_mfa_bypass_for_swift_access(self, controls_evidence: dict):
        operators = controls_evidence.get("swift_operator_accounts", [])
        bypassed = [a for a in operators if a.get("mfa_bypass_enabled", False)]
        assert not bypassed, (
            f"MFA bypass must not be enabled for any SWIFT operator account. "
            f"Bypassed: {[a['account_id'] for a in bypassed]}"
        )

    def test_mfa_type_is_hardware_or_approved_equivalent(self, controls_evidence: dict):
        operators = controls_evidence.get("swift_operator_accounts", [])
        prohibited_mfa_types = {"sms_otp", "voice_call", "email_otp"}
        weak_mfa = [
            a for a in operators
            if a.get("mfa_type", "").lower() in prohibited_mfa_types
        ]
        assert not weak_mfa, (
            f"SWIFT MFA must use hardware token, TOTP authenticator app, or equivalent. "
            f"Weak MFA types: {[(a['account_id'], a['mfa_type']) for a in weak_mfa]}"
        )
```

---

## Control 3.3 — Physically Secure Environment

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | SWIFT secure zone physical location | DETERMINISTIC |
| Condition | SWIFT secure zone systems hosted in physical premises | DETERMINISTIC |
| Obligation | Physical access to SWIFT secure zone restricted and logged; unauthorized access prevented | PARAMETERIZED |
| Evidence | Access control system records; visitor log; secure zone physical boundary description | PARAMETERIZED |

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestControl3_3:
    """3.3 — Physically Secure Environment: physical access controls for SWIFT zone."""

    @pytest.mark.assumption(
        id="ASSUME-SWIFT-3_3-001",
        description=(
            "SWIFT secure zone physical access is restricted to authorized personnel only; "
            "electronic or physical access controls (badge readers, locks) in place; "
            "all access events logged; visitors require escort"
        ),
        approved_by="physical_security_team",
        review_date="2027-05-21",
    )
    def test_physical_access_controls_exist(self, controls_evidence: dict):
        physical = controls_evidence.get("swift_zone_physical_security", {})
        assert physical.get("access_control_in_place", False), (
            "Physical access controls must be in place for SWIFT secure zone"
        )

    def test_physical_access_logged(self, controls_evidence: dict):
        physical = controls_evidence.get("swift_zone_physical_security", {})
        assert physical.get("access_logging_enabled", False), (
            "Physical access to SWIFT secure zone must be logged"
        )
```

---

## Control 4.1 — Password Storage and Transmission

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Passwords for SWIFT system accounts and operator accounts | DETERMINISTIC |
| Condition | Passwords stored or transmitted by SWIFT zone systems | DETERMINISTIC |
| Obligation | Passwords stored using strong one-way hashing (SHA-256+ or bcrypt/scrypt/Argon2); transmitted only over encrypted channels | DETERMINISTIC |
| Evidence | Identity system configuration; password storage algorithm; TLS enforcement on authentication endpoints | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
SWIFT_APPROVED_HASH_ALGORITHMS = frozenset({
    "bcrypt", "scrypt", "argon2", "pbkdf2_sha256", "pbkdf2_sha512",
    "sha256", "sha512",
})

class TestControl4_1:
    """4.1 — Password Storage and Transmission: strong hashing and encrypted channels."""

    def test_passwords_stored_with_approved_algorithm(self, controls_evidence: dict):
        identity_systems = controls_evidence.get("swift_identity_systems", [])
        for sys in identity_systems:
            algo = sys.get("password_hash_algorithm", "").lower()
            assert algo in SWIFT_APPROVED_HASH_ALGORITHMS, (
                f"System {sys.get('system_id')} uses non-approved hash algorithm '{algo}'. "
                f"Approved: {sorted(SWIFT_APPROVED_HASH_ALGORITHMS)}"
            )

    def test_passwords_transmitted_only_over_encrypted_channels(self, controls_evidence: dict):
        auth_endpoints = controls_evidence.get("swift_auth_endpoints", [])
        plaintext = [ep for ep in auth_endpoints if not ep.get("tls_enforced", False)]
        assert not plaintext, (
            f"All SWIFT authentication endpoints must enforce TLS. "
            f"Unencrypted: {[ep['endpoint_id'] for ep in plaintext]}"
        )
```

---

## Control 4.2 — Physical and Logical Password Storage (System/Service Accounts)

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Privileged system/service account credentials for SWIFT components | DETERMINISTIC |
| Condition | System/service accounts exist within SWIFT zone | DETERMINISTIC |
| Obligation | High-value credentials protected by hardware token, HSM, or privileged access management (PAM) vault | PARAMETERIZED |
| Evidence | PAM system inventory; HSM usage records; credential vault configuration | PARAMETERIZED |

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestControl4_2:
    """4.2 — Physical and Logical Password Storage: hardware-protected credentials."""

    @pytest.mark.assumption(
        id="ASSUME-SWIFT-4_2-001",
        description=(
            "Privileged SWIFT system/service account credentials are stored in a PAM vault, "
            "HSM, or equivalent hardware-protected store; plaintext credential storage in "
            "scripts, config files, or environment variables is prohibited"
        ),
        approved_by="identity_security_team",
        review_date="2027-05-21",
    )
    def test_privileged_credentials_in_vault_or_hsm(self, controls_evidence: dict):
        creds = controls_evidence.get("swift_privileged_credentials", {})
        assert creds.get("protected_storage", False), (
            "Privileged SWIFT credentials must be stored in PAM vault or HSM"
        )

    def test_no_plaintext_credentials_in_config(self, controls_evidence: dict):
        creds = controls_evidence.get("swift_privileged_credentials", {})
        assert not creds.get("plaintext_in_config", True), (
            "Plaintext credentials must not appear in SWIFT zone config files or scripts"
        )
```

---

## Control 4.3A — Staff Screening

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Staff with access to SWIFT infrastructure | DETERMINISTIC |
| Condition | Hiring or onboarding to SWIFT-operator role | DETERMINISTIC |
| Obligation | Background check process completed before granting SWIFT access | PARAMETERIZED |
| Evidence | HR background check records; access grant date vs. clearance date for SWIFT accounts | PARAMETERIZED |

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestControl4_3A:
    """4.3A — Staff Screening: background checks before SWIFT access granted."""

    @pytest.mark.assumption(
        id="ASSUME-SWIFT-4_3A-001",
        description=(
            "Background check process defined and documented for SWIFT operator roles; "
            "check completed prior to granting SWIFT zone access; records retained for "
            "duration of employment + 3 years"
        ),
        approved_by="hr_security_team",
        review_date="2027-05-21",
    )
    def test_background_check_process_exists(self, controls_evidence: dict):
        screening = controls_evidence.get("swift_staff_screening", {})
        assert screening.get("process_documented", False), (
            "Background check process for SWIFT operator roles must be documented"
        )

    def test_swift_access_not_granted_before_screening(self, controls_evidence: dict):
        operators = controls_evidence.get("swift_operator_accounts", [])
        premature = [
            a for a in operators
            if a.get("access_granted_date") is not None
            and a.get("background_check_completion_date") is None
        ]
        assert not premature, (
            f"SWIFT access must not be granted before background check completion. "
            f"Premature access: {[a['account_id'] for a in premature]}"
        )
```

---

## Control 4.4 — Token Management (Signing Keys)

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Cryptographic keys used for SWIFT message signing | DETERMINISTIC |
| Condition | SWIFT message authentication uses signing keys | DETERMINISTIC |
| Obligation | Signing keys generated and stored in HSM or equivalent hardware security device | DETERMINISTIC |
| Evidence | HSM inventory; key generation records; key never exists in software-only form | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestControl4_4:
    """4.4 — Token Management: HSM-protected SWIFT signing keys."""

    def test_signing_keys_in_hsm(self, controls_evidence: dict):
        keys = controls_evidence.get("swift_signing_keys", [])
        software_only = [k for k in keys if not k.get("hsm_protected", False)]
        assert not software_only, (
            f"All SWIFT signing keys must be generated and stored in HSM. "
            f"Software-only keys: {[k['key_id'] for k in software_only]}"
        )

    def test_hsm_inventory_documented(self, controls_evidence: dict):
        hsm = controls_evidence.get("swift_hsm_inventory", [])
        assert hsm, "HSM inventory for SWIFT signing key protection must be non-empty"
```

---

## Control 5.1 — Logical Access Control

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | All accounts with access to SWIFT zone systems | DETERMINISTIC |
| Condition | Always (ongoing obligation) | DETERMINISTIC |
| Obligation | Least-privilege access enforced; access reviewed at least annually; unused accounts disabled | DETERMINISTIC |
| Evidence | Access review records with completion date; disabled/removed accounts list; privilege inventory | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestControl5_1:
    """5.1 — Logical Access Control: least-privilege and annual review."""

    def test_access_review_completed_within_12_months(
        self, controls_evidence: dict, reference_date: date
    ):
        from datetime import timedelta
        last_review = controls_evidence.get("swift_access_review_date")
        assert last_review is not None, "SWIFT access review must have a recorded completion date"
        cutoff = reference_date - timedelta(days=SWIFT_ACCESS_REVIEW_MONTHS * 30)
        assert last_review >= cutoff, (
            f"SWIFT access review must occur within {SWIFT_ACCESS_REVIEW_MONTHS} months. "
            f"Last review: {last_review} — exceeds cutoff: {cutoff}"
        )

    def test_no_excessive_privileges_on_swift_accounts(self, controls_evidence: dict):
        accounts = controls_evidence.get("swift_zone_accounts", [])
        over_privileged = [
            a for a in accounts
            if a.get("access_justified_and_documented", None) is False
        ]
        assert not over_privileged, (
            f"All SWIFT account privileges must be justified and documented. "
            f"Unjustified: {[a['account_id'] for a in over_privileged]}"
        )

    def test_no_dormant_swift_accounts(
        self, controls_evidence: dict, reference_date: date
    ):
        from datetime import timedelta
        accounts = controls_evidence.get("swift_zone_accounts", [])
        dormant_threshold = timedelta(days=90)
        dormant = [
            a for a in accounts
            if a.get("last_used_date") is not None
            and (reference_date - a["last_used_date"]) > dormant_threshold
            and not a.get("disabled", False)
        ]
        assert not dormant, (
            f"Dormant SWIFT accounts (unused >90 days) must be disabled. "
            f"Active dormant accounts: {[a['account_id'] for a in dormant]}"
        )
```

---

## Control 5.2 — Session Protection

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Interactive sessions on SWIFT zone systems and operator PCs | DETERMINISTIC |
| Condition | User session established to SWIFT infrastructure | DETERMINISTIC |
| Obligation | Session terminated after inactivity; all sessions encrypted end-to-end | DETERMINISTIC |
| Evidence | Session timeout configuration; TLS/SSH enforcement for all remote sessions; no cleartext sessions | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestControl5_2:
    """5.2 — Session Protection: timeout and encrypted sessions."""

    def test_session_timeout_configured(self, controls_evidence: dict):
        session = controls_evidence.get("swift_session_config", {})
        timeout = session.get("inactivity_timeout_minutes", 9999)
        assert timeout <= SWIFT_SESSION_TIMEOUT_MINUTES, (
            f"SWIFT session inactivity timeout must be ≤{SWIFT_SESSION_TIMEOUT_MINUTES} min. "
            f"Current: {timeout}"
        )

    def test_no_cleartext_remote_sessions(self, controls_evidence: dict):
        sessions = controls_evidence.get("swift_remote_session_protocols", [])
        cleartext = [s for s in sessions if s.get("protocol", "").lower() in {"telnet", "ftp", "rsh", "rlogin"}]
        assert not cleartext, (
            f"Cleartext remote sessions prohibited on SWIFT zone. "
            f"Found: {[(s['system_id'], s['protocol']) for s in cleartext]}"
        )

    def test_all_remote_sessions_encrypted(self, controls_evidence: dict):
        sessions = controls_evidence.get("swift_remote_session_protocols", [])
        unencrypted = [s for s in sessions if not s.get("encrypted", False)]
        assert not unencrypted, (
            f"All remote sessions to SWIFT zone must be encrypted. "
            f"Unencrypted: {[s['system_id'] for s in unencrypted]}"
        )
```

---

## Control 5.3A — Security Roles

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | SWIFT operational roles (business submitter, business authorizer, security officer) | DETERMINISTIC |
| Condition | Multiple SWIFT operators exist | DETERMINISTIC |
| Obligation | Separation of duties enforced for SWIFT roles; same person cannot both initiate and authorize transactions | PARAMETERIZED |
| Evidence | Role assignment matrix; access control configuration showing role separation | PARAMETERIZED |

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestControl5_3A:
    """5.3A — Security Roles: SWIFT transaction separation of duties."""

    @pytest.mark.assumption(
        id="ASSUME-SWIFT-5_3A-001",
        description=(
            "SWIFT operational roles (submitter, authorizer, security officer, operator) "
            "are documented and assigned to different individuals; no single person can "
            "both initiate and authorize SWIFT transactions; role matrix reviewed annually"
        ),
        approved_by="security_officer",
        review_date="2027-05-21",
    )
    def test_transaction_initiator_and_authorizer_are_separate(self, controls_evidence: dict):
        roles = controls_evidence.get("swift_role_assignments", [])
        dual_role = [
            r for r in roles
            if "submitter" in r.get("roles", []) and "authorizer" in r.get("roles", [])
        ]
        assert not dual_role, (
            f"No person may hold both SWIFT submitter and authorizer roles. "
            f"Dual-role accounts: {[r['account_id'] for r in dual_role]}"
        )

    def test_security_officer_role_not_combined_with_operator(self, controls_evidence: dict):
        roles = controls_evidence.get("swift_role_assignments", [])
        conflict = [
            r for r in roles
            if "security_officer" in r.get("roles", [])
            and any(op in r.get("roles", []) for op in ["submitter", "authorizer", "operator"])
        ]
        assert not conflict, (
            f"SWIFT security officer role must be separate from operator roles. "
            f"Conflicts: {[r['account_id'] for r in conflict]}"
        )
```

---

## Open assumptions

| ID | Control | Summary | Review date |
|---|---|---|---|
| ASSUME-SWIFT-3_3-001 | 3.3 | Physical access restricted to authorized personnel; badge/lock controls; all access logged; visitors escorted | 2027-05-21 |
| ASSUME-SWIFT-4_2-001 | 4.2 | Privileged SWIFT credentials in PAM vault or HSM; no plaintext in config files or scripts | 2027-05-21 |
| ASSUME-SWIFT-4_3A-001 | 4.3A | Background check process documented; check completed before SWIFT access granted; records retained | 2027-05-21 |
| ASSUME-SWIFT-5_3A-001 | 5.3A | SWIFT submitter/authorizer/security officer roles assigned to different individuals; role matrix reviewed annually | 2027-05-21 |
