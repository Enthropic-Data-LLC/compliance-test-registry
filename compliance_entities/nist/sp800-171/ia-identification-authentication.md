# NIST SP 800-171 r3 — Family IA: Identification and Authentication

**Registry path:** `/regulation-registry/NIST-SP800-171/IA/`
**Version:** NIST SP 800-171 Rev 3 (May 2024)
**Last parsed:** 2026-05-20
**Applies to:** Non-federal organizations (contractors, universities, research institutions) that process, store, or transmit Controlled Unclassified Information (CUI) in nonfederal information systems under US federal contracts or grants
**Trigger:** Federal contract or grant containing DFARS clause 252.204-7012 (DoD) or equivalent FAR clause; any contract where the government provides or the contractor generates CUI; CMMC Level 2 requires third-party assessment against NIST 800-171
**Jurisdiction:** United States; extraterritorial — applies to foreign companies holding US federal contracts involving CUI; enforced through contract terms and DoD CMMC assessments
**Not applicable to:** Federal agencies (use NIST 800-53 instead); organizations with no federal contracts or grants; commercial transactions not involving CUI; EAR99 technology transfers (separate ITAR/EAR framework)
**Overall confidence:** HIGH — MFA (3.5.3), password minimums (3.5.7), authenticator management (3.5.8–3.5.10), and re-authentication (3.5.4) are all DETERMINISTIC with measurable thresholds; non-organizational users (3.5.6) and device authentication (3.5.5) are PARAMETERIZED
**12 requirements: 3.5.1–3.5.12**

---

## Scope summary

The IA family covers identification and authentication for users (organizational and non-organizational) and devices. It is the tightest family in 800-171 from an automation standpoint: most requirements specify measurable control existence (MFA, password length, re-authentication timing). The FIPS 140-2/3 requirement (3.5.10) makes cryptographic module validation a binary check where evidence exists.

IA maps directly to: CMMC Level 2 IA domain; PCI DSS Req 8 (authentication); ISO 27001 A.5.17 and A.8.5.

---

## 3.5.1 — Identification (HIGH)

### Source text

> Identify system users, processes acting on behalf of users, and devices.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | All users, processes, and devices with system access assigned unique identifiers; identification maintained | DETERMINISTIC |
| Evidence | `user_account_records.unique_identifiers == true`; no anonymous or shared accounts in CUI systems; service accounts individually named | DETERMINISTIC |

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.5.2 — Authentication (HIGH)

### Source text

> Authenticate (or verify) the identities of users, processes, or devices, as a prerequisite to allowing access to organizational systems.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Authentication required before granting access; authentication mechanism in place for all access to CUI systems | DETERMINISTIC |
| Evidence | `auth_config.authentication_required_before_access == true`; no unauthenticated access paths to CUI | DETERMINISTIC |

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.5.3 — Multi-Factor Authentication (HIGH)

### Source text

> Use multi-factor authentication for local and network access to privileged accounts and for network access to non-privileged accounts.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | Privileged accounts (all access); non-privileged accounts (network access) | DETERMINISTIC |
| Obligation | MFA required for privileged account access (local and network); MFA required for network access to all accounts | DETERMINISTIC |
| Evidence | `mfa_enrollment_records.privileged_accounts == 100%`; `mfa_enrollment_records.network_access_accounts == 100%` | DETERMINISTIC |

**Assumption (ASSUME-800171-IA-001):** MFA is adequate when: (1) FIPS 140-2/3 validated authenticators used (hardware token, PIV/CAC card, TOTP with validated app); (2) SMS OTP does not satisfy requirement for CUI systems due to NIST SP 800-63B deprecation of SMS-based OTP for high assurance; (3) MFA cannot be bypassed via recovery codes without separate authentication factor; (4) phishing-resistant MFA (FIDO2, PIV) preferred for privileged accounts; (5) applies to all authentication mechanisms including VPN, remote desktop, web portals, and API access.

**Cross-reference:** Aligns with PCI DSS Req 8.4 (MFA expansion) and CMMC Level 2 IA.3.083.

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.5.4 — Replay-Resistant Authentication (HIGH)

### Source text

> Employ replay-resistant authentication mechanisms for network access to privileged and non-privileged accounts.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Authentication mechanisms for network access are replay-resistant | DETERMINISTIC |
| Evidence | `auth_mechanisms.replay_resistant == true`; no password-only network access to CUI systems | DETERMINISTIC |

**Assumption (ASSUME-800171-IA-002):** Authentication is replay-resistant when: (1) Kerberos, TLS client certificates, FIDO2/WebAuthn, or PIV/CAC used — these are inherently replay-resistant; (2) password-only authentication over network does NOT satisfy this requirement (passwords can be replayed from capture); (3) TOTP (HOTP with time window) is replay-resistant within the OTP validity window; (4) challenge-response protocols acceptable if based on approved algorithms.

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.5.5 — Identifier Management — Non-Reuse (HIGH)

### Source text

> Identify and authenticate organizational users, devices, and processes to access the system, and prevent the reuse of identifiers for a defined period.

*Note: Per NIST SP 800-171A, this covers identifier lifecycle management including non-reuse.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Identifiers (usernames, account IDs) managed throughout lifecycle; identifiers not reused for defined period after deactivation | PARAMETERIZED (reuse period) |
| Evidence | `identity_management.disabled_accounts_not_reused_within_period`; account lifecycle records | PARAMETERIZED |

**Assumption (ASSUME-800171-IA-003):** Identifier non-reuse period: deactivated user identifiers not reused for minimum 90 days. Service/process account identifiers not reused for minimum 12 months. Device identifiers follow same timeline as user identifiers for the device class.

**Overall: PARAMETERIZED → Pattern 2**

---

## 3.5.6 — Authentication for Non-Organizational Users (MEDIUM)

### Source text

> Authenticate (or verify) the identities of non-organizational users.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Non-organizational users (contractors, partners, public-facing service consumers) authenticated before accessing systems | PARAMETERIZED |
| Evidence | `external_user_auth.mechanism_documented`; external user provisioning process documented | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## 3.5.7 — Password Complexity and Length (HIGH)

### Source text

> Enforce a minimum password complexity and change requirements for passwords.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Minimum password length enforced; complexity requirements applied; password change on first login and when compromised | DETERMINISTIC |
| Evidence | `password_policy.min_length >= 8` (NIST minimum with complexity) or `>= 15` (NIST recommended without complexity) | DETERMINISTIC |

**Assumption (ASSUME-800171-IA-004):** Password policy is adequate when following NIST SP 800-63B guidance: (1) minimum 8 characters with complexity requirements (uppercase, lowercase, digit, special character), OR minimum 15 characters without complexity requirements (length alone); (2) password changed on first use of system-assigned password; (3) password changed when compromise suspected or confirmed; (4) passwords checked against known-breached password lists on creation/change; (5) maximum password age ≤ 365 days, OR no maximum age when MFA is enforced (NIST SP 800-63B deprecates periodic password rotation in favor of breach-triggered rotation).

**Note:** NIST SP 800-63B (2017) explicitly discourages arbitrary periodic password rotation in favor of breach-triggered rotation when MFA is in place. Some DoD contracts still require periodic rotation — the SSP should document which policy is applied.

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.5.8 — Password Prohibition — Dictionary Words (HIGH)

### Source text

> Prohibit password reuse for a specified number of generations.

*Note: r3 maps 3.5.8 to prohibiting common/dictionary passwords and password reuse.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Password reuse prohibited for defined number of generations; dictionary/common passwords rejected | DETERMINISTIC |
| Evidence | `password_policy.history_count >= 5`; `password_policy.dictionary_check == true` | DETERMINISTIC |

**Assumption (ASSUME-800171-IA-005):** Password reuse prohibition: minimum 5 prior passwords prohibited (consistent with PCI DSS Req 8.3.7 and ISO 27001 ASSUME-ISO-A5-004). Dictionary/common password check: known-breached passwords and common password patterns (e.g., "Password1!") rejected.

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.5.9 — Temporary Password Management (HIGH)

### Source text

> Allow temporary passwords with an immediate change requirement.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Temporary/one-time passwords enforced to change on first use; temporary passwords have limited validity period | DETERMINISTIC |
| Evidence | `auth_config.temp_password_requires_change_on_first_use == true`; temporary password validity ≤ 24 hours | DETERMINISTIC |

**Assumption (ASSUME-800171-IA-006):** Temporary passwords are managed adequately when: (1) first-use change required immediately — system enforces the change, not just recommends it; (2) temporary password validity period ≤ 24 hours; expired if unused; (3) temporary passwords never sent unencrypted (no HTTP, unencrypted email where avoidable — encrypted email or secure channel preferred); (4) applies to all system-generated and administrator-assigned temporary credentials.

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.5.10 — Cryptographically-Protected Passwords (HIGH)

### Source text

> Store and transmit only cryptographically-protected passwords.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Passwords never stored in plaintext; passwords hashed with approved algorithm; transmission encrypted | DETERMINISTIC |
| Evidence | `password_storage.algorithm` ∈ {bcrypt, scrypt, Argon2, PBKDF2-SHA256}; plaintext passwords not stored anywhere in the system | DETERMINISTIC |

**Assumption (ASSUME-800171-IA-007):** Cryptographic password protection is adequate when: (1) passwords stored using adaptive hash with salt: bcrypt (cost ≥ 10), scrypt, Argon2id, or PBKDF2-SHA256 (iterations ≥ 310,000); (2) MD5, SHA-1, SHA-256 without salt are NOT acceptable for password storage (one-way but not adaptive); (3) password transmission never in plaintext — TLS 1.2+ required; (4) FIPS 140-2/3 validated cryptographic module used for password hashing on systems requiring FIPS compliance.

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.5.11 — Obscure Authenticator Feedback (HIGH)

### Source text

> Obscure feedback of authentication information.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Password/authenticator not displayed in plaintext during entry | DETERMINISTIC |
| Evidence | `ui_config.password_input_masked == true`; no application logging of password values; no credential in URLs | DETERMINISTIC |

**Overall: DETERMINISTIC → Pattern 1**

---

## 3.5.12 — Authenticator Management (HIGH)

### Source text

> Manage system authenticators for users and devices.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Authenticator lifecycle managed: initial issuance, protection in use, periodic refresh, revocation | PARAMETERIZED |
| Evidence | `authenticator_management_policy.documented`; hardware token inventory; periodic credential rotation records | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## YAML specifications

### `ia_identification_authentication.yaml`

```yaml
regulation_id: NIST-SP800-171-r3-IA
section: "NIST SP 800-171 r3 — Family IA: Identification and Authentication"
r_or_a: Required
source_text: >
  Identify and authenticate users, processes, and devices; use MFA for privileged
  and network access; protect password storage with approved cryptography; prohibit
  reuse and enforce complexity; replay-resistant authentication required.

extracted_elements:
  subject: "All users, processes, and devices with CUI system access"
  condition: "system_processes_cui() == true"
  obligation: >
    Unique IDs; authentication required; MFA for privileged (all) and standard (network);
    min 8 chars (with complexity) or 15 chars (without); history ≥5; adaptive hash for storage;
    session lock ≤15 min; replay-resistant authentication
  evidence: >
    user_accounts, mfa_enrollment_records, auth_configs, password_policy,
    password_storage_config

ambiguity_classification:
  subject: DETERMINISTIC
  condition: PARAMETERIZED
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-800171-IA-001
    assumption_text: >
      MFA: FIPS 140-2/3 validated authenticators; SMS OTP insufficient;
      FIDO2/PIV preferred for privileged; applies to all network auth paths.
    assumed_by: "System Owner"
    approved_by: "ISSO"
    date: "2026-05-20"
    review_frequency_days: 365
  - assumption_id: ASSUME-800171-IA-004
    assumption_text: >
      Password: min 8 chars + complexity, OR min 15 chars; breach-triggered rotation;
      checked against known-breached lists; max 365 days or no max with MFA.
    assumed_by: "System Owner"
    approved_by: "ISSO"
    date: "2026-05-20"
    review_frequency_days: 365
  - assumption_id: ASSUME-800171-IA-007
    assumption_text: >
      Password hashing: bcrypt ≥10, scrypt, Argon2id, or PBKDF2-SHA256 ≥310k iterations;
      MD5/SHA-1/unsalted-SHA-256 not acceptable; FIPS 140-2/3 module for FIPS-required systems.
    assumed_by: "System Owner"
    approved_by: "ISSO"
    date: "2026-05-20"
    review_frequency_days: 365
test_confidence: HIGH
generated_test: "tests/nist_sp800171/test_ia_identification_authentication.py"
```

---

## Generated tests

### `tests/nist_sp800171/test_ia_identification_authentication.py`

```python
"""
NIST SP 800-171 r3 — Family IA: Identification and Authentication
Confidence: HIGH for 3.5.1–3.5.4, 3.5.7–3.5.11
Pre-condition: system_processes_cui() fixture must return True
"""
import pytest

PASSWORD_MIN_LENGTH_WITH_COMPLEXITY = 8
PASSWORD_MIN_LENGTH_WITHOUT_COMPLEXITY = 15
PASSWORD_HISTORY_MIN = 5
TEMP_PASSWORD_MAX_VALIDITY_HOURS = 24

UNACCEPTABLE_HASH_ALGORITHMS = {"md5", "sha1", "sha256_unsalted", "plaintext"}
ACCEPTABLE_HASH_ALGORITHMS = {"bcrypt", "scrypt", "argon2", "argon2id", "pbkdf2_sha256"}


@pytest.fixture(autouse=True)
def require_cui_scope(system_scope):
    if not system_scope.get("processes_cui"):
        pytest.skip("System not attested as processing CUI")


def test_all_cui_users_have_unique_identifiers(user_accounts):
    """3.5.1 — All users accessing CUI systems must have unique identifiers."""
    violations = [
        a for a in user_accounts
        if a.get("in_cui_enclave")
        and not a.get("unique_identifier")
    ]
    assert not violations, (
        f"NONCONFORMITY (3.5.1): {len(violations)} account(s) without unique identifier: "
        f"{[a['account_id'] for a in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-800171-IA-001",
    description=(
        "MFA: FIPS 140-2/3 validated; SMS OTP insufficient; FIDO2/PIV preferred "
        "for privileged; applies to all network auth paths."
    ),
    approved_by="ISSO",
    review_date="2026-05-20",
)
def test_mfa_enrolled_for_all_privileged_accounts(user_accounts):
    """3.5.3 — MFA required for all privileged account access (local and network)."""
    violations = [
        a for a in user_accounts
        if a.get("in_cui_enclave")
        and a.get("is_privileged")
        and not a.get("mfa_enrolled")
    ]
    assert not violations, (
        f"NONCONFORMITY (3.5.3): {len(violations)} privileged CUI-enclave account(s) "
        f"without MFA: {[a['account_id'] for a in violations]}"
    )


def test_mfa_enrolled_for_all_network_access_accounts(user_accounts):
    """3.5.3 — MFA required for network access to all accounts (privileged and non-privileged)."""
    violations = [
        a for a in user_accounts
        if a.get("in_cui_enclave")
        and a.get("has_network_access")
        and not a.get("mfa_enrolled")
    ]
    assert not violations, (
        f"NONCONFORMITY (3.5.3): {len(violations)} CUI-enclave network-access account(s) "
        f"without MFA: {[a['account_id'] for a in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-800171-IA-004",
    description="Password: min 8+complexity or 15 chars; breach-triggered; checked against known-breached lists",
    approved_by="ISSO",
    review_date="2026-05-20",
)
def test_password_length_policy_configured(auth_system_configs):
    """3.5.7 — Password minimum length must be configured."""
    violations = []
    for cfg in auth_system_configs:
        if not cfg.get("in_cui_enclave"):
            continue
        min_length = cfg.get("min_password_length", 0)
        has_complexity = cfg.get("complexity_requirements_enabled", False)
        threshold = (
            PASSWORD_MIN_LENGTH_WITH_COMPLEXITY
            if has_complexity
            else PASSWORD_MIN_LENGTH_WITHOUT_COMPLEXITY
        )
        if min_length < threshold:
            violations.append(
                f"System {cfg['system_id']}: min length {min_length} < {threshold} "
                f"({'with' if has_complexity else 'without'} complexity)"
            )
    assert not violations, (
        f"NONCONFORMITY (3.5.7): {len(violations)} CUI system(s) with insufficient "
        f"password length:\n" + "\n".join(violations)
    )


@pytest.mark.assumption(
    id="ASSUME-800171-IA-005",
    description="Password history ≥5 prior passwords prohibited; common/dictionary passwords rejected",
    approved_by="ISSO",
    review_date="2026-05-20",
)
def test_password_history_configured(auth_system_configs):
    """3.5.8 — Password reuse prohibited for at least 5 prior passwords."""
    violations = [
        cfg for cfg in auth_system_configs
        if cfg.get("in_cui_enclave")
        and cfg.get("password_history_count", 0) < PASSWORD_HISTORY_MIN
    ]
    assert not violations, (
        f"NONCONFORMITY (3.5.8): {len(violations)} CUI system(s) with insufficient "
        f"password history: {[c['system_id'] for c in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-800171-IA-007",
    description="Password hashing: bcrypt ≥10, scrypt, Argon2id, or PBKDF2-SHA256 ≥310k iterations; MD5/SHA-1 unacceptable",
    approved_by="ISSO",
    review_date="2026-05-20",
)
def test_passwords_stored_with_approved_hash(password_storage_configs):
    """3.5.10 — Passwords must be stored using approved adaptive hash algorithm."""
    violations = []
    for cfg in password_storage_configs:
        if not cfg.get("in_cui_enclave"):
            continue
        algo = cfg.get("hash_algorithm", "").lower()
        if algo in UNACCEPTABLE_HASH_ALGORITHMS:
            violations.append(
                f"System {cfg['system_id']}: unacceptable hash algorithm '{algo}'"
            )
        elif algo not in ACCEPTABLE_HASH_ALGORITHMS:
            violations.append(
                f"System {cfg['system_id']}: unknown/undocumented hash algorithm '{algo}'"
            )
    assert not violations, (
        f"NONCONFORMITY (3.5.10): {len(violations)} CUI system(s) using unacceptable "
        f"password storage:\n" + "\n".join(violations)
    )


def test_temp_passwords_require_immediate_change(auth_system_configs):
    """3.5.9 — Temporary passwords must require change on first use."""
    violations = [
        cfg for cfg in auth_system_configs
        if cfg.get("in_cui_enclave")
        and not cfg.get("temp_password_change_required_on_first_use")
    ]
    assert not violations, (
        f"NONCONFORMITY (3.5.9): {len(violations)} CUI system(s) not enforcing "
        f"first-use change for temporary passwords: "
        f"{[c['system_id'] for c in violations]}"
    )
```

---

## Notes for the registry

- **3.5.3 MFA — local vs. network distinction:** 800-171 r3 requires MFA for privileged accounts on *all* access (local AND network); for non-privileged accounts, MFA is required for network access only. Local non-privileged access (physical terminal in a secured area) may not require MFA depending on the system's SSP. However, most organizations apply MFA universally to avoid complexity.
- **FIPS 140-2/3 and MFA authenticators:** DoD contractor systems handling CUI must use FIPS 140-2/3 validated cryptographic modules. This applies to the MFA authenticator software and the authentication protocol. SMS OTP is excluded not just because of its known weaknesses but because SMS transmission is not FIPS-validated. TOTP apps that use FIPS-validated crypto modules are acceptable.
- **Password length guidance evolution:** NIST SP 800-63B (2017) introduced length-over-complexity as the recommended approach and deprecated mandatory periodic rotation in favor of breach-triggered rotation. 800-171 r3 aligns with this guidance. Organizations should document whether they follow the 8+complexity or 15-without-complexity path in their SSP. CMMC assessors will accept either.
- **3.5.10 adaptive hashing requirement:** MD5 and SHA-1 for password storage are explicitly prohibited — they are computationally fast and trivially crackable with GPU-based attacks. Even SHA-256 without salt and iteration count is unacceptable. The minimum acceptable algorithms are modern adaptive hash functions (bcrypt, scrypt, Argon2id, or PBKDF2 with high iteration count). This is tested by `test_passwords_stored_with_approved_hash`.
- **Mapping to CMMC Level 2:** All 12 IA requirements map to CMMC Level 2 IA domain. IA.3.083 (MFA) is the most commonly assessed and failed requirement in CMMC Level 2 assessments, particularly for remote access to non-privileged accounts (the r3 expansion from r2 which only required MFA for privileged).
