# Requirement 8 — Identify Users and Authenticate Access to System Components

**Registry path:** `/regulation-registry/PCI-DSS/Req-8/`
**Version:** PCI DSS v4.0 (mandatory since March 31, 2025)
**Last parsed:** 2026-05-20
**Applies to:** Any organization that stores, processes, or transmits payment card data — merchants of all levels, payment processors, acquirers, issuers, and service providers in the card payment ecosystem
**Trigger:** Participation in the card payment ecosystem; card brand contracts (Visa, Mastercard, Amex, Discover, UnionPay); acquiring bank contractual requirement; SAQ level determined by annual transaction volume
**Jurisdiction:** Global — enforced by card brands (Visa/Mastercard/Amex/Discover) and acquiring banks; no geographic restriction
**Not applicable to:** Organizations that never handle cardholder data and fully outsource all card processing to a PCI-DSS-compliant third party; SAQ A merchants processing only redirected card transactions
**Overall confidence:** HIGH — all authentication thresholds are DETERMINISTIC; MFA replay-resistance method is PARAMETERIZED
**R = Required**

---

## Scope summary

Req 8 is the identity and authentication pillar of PCI DSS v4.0. It has the highest DETERMINISTIC density of any requirement — password length, lockout threshold, session timeout, MFA scope, and service account rotation are all stated as explicit numbers. The only PARAMETERIZED surface is MFA implementation method (must be "not susceptible to replay attacks" — method selection requires a documented rationale).

The most significant v4.0 change: **MFA is now required for ALL CDE access** (8.4.2), not just non-console administrative access as in v3.2.1.

---

## 8.2 — User Identification (R — DETERMINISTIC)

### Source excerpt

> *8.2.1 — All users are assigned a unique ID before allowing them to access system components or cardholder data.*
> *8.2.6 — Inactive user accounts are removed or disabled within 90 days of inactivity.*
> *8.2.8 — If a user session has been idle for more than 15 minutes, the user is required to re-authenticate.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All users with access to CDE systems or CHD | DETERMINISTIC |
| Condition | Any access to system components or cardholder data | DETERMINISTIC |
| Obligation | Unique user ID per individual; no unauthorized shared accounts; 90-day inactivity deactivation; session timeout ≤ 15 minutes | DETERMINISTIC |
| Evidence | `user_accounts.user_id` unique; `inactive_threshold_days <= 90`; `session_idle_timeout_minutes <= 15` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 8.3 — Authentication Factors (R — DETERMINISTIC)

### Source excerpt

> *8.3.4 — Invalid authentication attempts are limited by locking out the user ID after not more than 10 attempts. The lockout must be for a minimum duration of 30 minutes or until the user's identity is confirmed.*
> *8.3.6 — If passwords/passphrases are used: minimum length of at least 12 characters (or 8 characters if the system does not support 12). Contain both numeric and alphabetic characters.*
> *8.3.7 — Individuals are not allowed to submit a new password/passphrase that is the same as any of the last four passwords/passphrases used.*
> *8.3.9 — Service account passwords changed at least every 12 months or at a frequency defined by a targeted risk analysis.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All user and service accounts in CDE | DETERMINISTIC |
| Condition | Password-based authentication in use | DETERMINISTIC |
| Obligation | Lockout ≤ 10 failed attempts; lockout ≥ 30 min; min 12 chars (8 if system limitation); alphanumeric; last 4 prohibited; service account rotation ≤ 365 days | DETERMINISTIC |
| Evidence | `auth_config.max_failed_attempts <= 10`; `lockout_duration_minutes >= 30`; `min_password_length >= 12`; `password_history >= 4`; `service_account_rotation_days <= 365` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 8.4 — Multi-Factor Authentication (R — DETERMINISTIC existence; PARAMETERIZED method)

### Source excerpt

> *8.4.2 — MFA is implemented for all access into the CDE.*
> *8.4.3 — MFA systems are configured as follows: The MFA system is not susceptible to replay attacks. MFA systems cannot be bypassed by any users, including administrative users.*

### Element extraction — existence

| Element | Value | Classification |
|---|---|---|
| Subject | All users accessing any CDE system | DETERMINISTIC |
| Condition | Any CDE access | DETERMINISTIC |
| Obligation | MFA enabled for ALL CDE access; cannot be bypassed by any user | DETERMINISTIC |
| Evidence | `cde_system.mfa_enabled == true`; `mfa_bypass_controls_implemented == true` | DETERMINISTIC |

### Element extraction — replay resistance

| Element | Value | Classification |
|---|---|---|
| Obligation | MFA method not susceptible to replay attacks | PARAMETERIZED |
| Evidence | MFA implementation review; method is FIDO2/WebAuthn, TOTP/HOTP, hardware token, or push with device binding | PARAMETERIZED |

**Assumption (ASSUME-8-001):** Acceptable replay-resistant MFA methods: FIDO2/WebAuthn (hardware key or platform authenticator), TOTP/HOTP (codes expire after use), hardware token with non-replayable challenge, push notification with device binding and user presence check. SMS OTP is susceptible to SIM-swapping and SS7 attacks — while v4.0 does not explicitly prohibit it, Req 8.4.3 "not susceptible to replay attacks" creates risk under QSA scrutiny. Flag SMS OTP for compliance review.

**Overall: DETERMINISTIC for existence → Pattern 1; PARAMETERIZED for method → Pattern 2**

---

## 8.6 — Application and System Account Passwords (R — DETERMINISTIC + PARAMETERIZED)

### Source excerpt

> *8.6.2 — Passwords/passphrases for application and system accounts that can be used for interactive login are not hard-coded in scripts, applications, or configuration/property files and are changed periodically.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All application and system accounts capable of interactive login | DETERMINISTIC |
| Condition | Account has a password | DETERMINISTIC |
| Obligation | No hard-coded passwords in scripts/code/config; passwords changed periodically | PARAMETERIZED (period not stated in 8.6.2; 8.3.9 provides 12-month for service accounts) |
| Evidence | Static analysis: no hardcoded credentials; `service_account.password_source != "hardcoded"` | DETERMINISTIC for prohibition; PARAMETERIZED for period |

**Assumption (ASSUME-8-002):** "Changed periodically" per 8.6.2 is satisfied by annual rotation (consistent with 8.3.9) or by a secrets management system with automatic rotation ≤ 90 days. Hard-coded credentials in source control, config files, or build artifacts are a Pattern 1 block regardless of rotation cadence.

**Overall: DETERMINISTIC for hard-coding prohibition → Pattern 1; PARAMETERIZED for rotation period → Pattern 2**

---

## YAML specifications

### `req8_unique_id.yaml`

```yaml
regulation_id: PCI-DSS-v4.0-8.2.1
section: "PCI DSS v4.0 — Unique User Identification"
r_or_a: Required
source_text: >
  All users are assigned a unique ID before allowing them to access
  system components or cardholder data.

extracted_elements:
  subject: "All users with CDE access"
  condition: "Any access to system components or CHD"
  obligation: "Unique user ID per individual; no unauthorized shared accounts"
  evidence: "user_accounts.user_id: unique; account_type != shared"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log: []
test_confidence: HIGH
generated_test: "tests/req8/test_8_2_user_identification.py"
```

### `req8_auth_factors.yaml`

```yaml
regulation_id: PCI-DSS-v4.0-8.3
section: "PCI DSS v4.0 — Authentication Factor Requirements"
r_or_a: Required
source_text: >
  Lockout after max 10 failed attempts; duration ≥ 30 min. Passwords:
  min 12 chars; alphanumeric; last 4 prohibited.

extracted_elements:
  subject: "All user accounts in CDE"
  condition: "Password-based authentication in use"
  obligation: "All four password thresholds met simultaneously"
  evidence: "auth_config: max_failed_attempts, lockout_duration_minutes,
             min_password_length, password_history"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log: []
test_confidence: HIGH
generated_test: "tests/req8/test_8_3_authentication.py"
```

### `req8_mfa.yaml`

```yaml
regulation_id: PCI-DSS-v4.0-8.4.2
section: "PCI DSS v4.0 — MFA for All CDE Access"
r_or_a: Required
source_text: >
  MFA is implemented for all access into the CDE.

extracted_elements:
  subject: "All users accessing any CDE system"
  condition: "Any CDE access attempt"
  obligation: "MFA enabled; not susceptible to replay; cannot be bypassed"
  evidence: "cde_system: mfa_enabled=true; mfa_bypass_controls_implemented=true"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-8-001
    assumption_text: >
      SMS OTP may not satisfy replay-resistance per 8.4.3 (SIM-swap/SS7 risk).
      Acceptable: FIDO2/WebAuthn, TOTP/HOTP, hardware token, push with device binding.
    assumed_by: "IT Security Officer"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
    cryptographic_hash: "sha256:pending-ci"
test_confidence: HIGH
generated_test: "tests/req8/test_8_4_mfa.py"
```

---

## Generated tests

### `tests/req8/test_8_2_user_identification.py`

```python
"""
PCI DSS v4.0 Req 8.2 — User Identification
Confidence: HIGH | Human Review: NOT REQUIRED
"""
from datetime import date

INACTIVITY_DEACTIVATION_DAYS = 90
SESSION_TIMEOUT_MINUTES = 15


def test_all_cde_users_have_unique_id(cde_user_accounts):
    user_ids = [u["user_id"] for u in cde_user_accounts]
    duplicates = {uid for uid in user_ids if user_ids.count(uid) > 1}
    assert not duplicates, (
        f"VIOLATION (8.2.1): {len(duplicates)} duplicate user ID(s) in CDE: {duplicates}"
    )


def test_no_shared_accounts_without_exception(cde_user_accounts):
    unauthorized_shared = [
        u for u in cde_user_accounts
        if u.get("account_type") == "shared"
        and not u.get("exception_documented")
    ]
    assert not unauthorized_shared, (
        f"VIOLATION (8.2.2): {len(unauthorized_shared)} shared account(s) without "
        f"documented exception: {[u['user_id'] for u in unauthorized_shared]}"
    )


def test_inactive_accounts_deactivated_within_90_days(cde_user_accounts):
    today = date.today()
    violations = []
    for user in cde_user_accounts:
        if user.get("status") == "disabled":
            continue
        last_active = user.get("last_active_date")
        if not last_active:
            violations.append(f"User {user['user_id']}: no last_active_date")
            continue
        days_inactive = (today - last_active).days
        if days_inactive > INACTIVITY_DEACTIVATION_DAYS:
            violations.append(
                f"User {user['user_id']}: inactive {days_inactive} days "
                f"(max {INACTIVITY_DEACTIVATION_DAYS})"
            )
    assert not violations, (
        f"VIOLATION (8.2.6): {len(violations)} active account(s) exceed inactivity "
        f"threshold:\n" + "\n".join(violations)
    )


def test_session_timeout_at_most_15_minutes(cde_system_configs):
    violations = [
        s for s in cde_system_configs
        if s.get("session_idle_timeout_minutes", 9999) > SESSION_TIMEOUT_MINUTES
    ]
    assert not violations, (
        f"VIOLATION (8.2.8): {len(violations)} CDE system(s) idle timeout > 15 min:\n"
        + "\n".join(
            f"  {s['system_id']}: {s.get('session_idle_timeout_minutes')} min"
            for s in violations
        )
    )
```

### `tests/req8/test_8_3_authentication.py`

```python
"""
PCI DSS v4.0 Req 8.3 — Authentication Factor Security
Confidence: HIGH | Human Review: NOT REQUIRED
"""
from datetime import date

PASSWORD_MIN_LENGTH = 12
PASSWORD_MIN_LENGTH_SYSTEM_LIMITED = 8
PASSWORD_HISTORY_COUNT = 4
MAX_FAILED_ATTEMPTS = 10
LOCKOUT_MIN_DURATION_MINUTES = 30
SERVICE_ACCOUNT_MAX_ROTATION_DAYS = 365


def test_password_minimum_length(auth_system_configs):
    violations = []
    for cfg in auth_system_configs:
        min_len = cfg.get("min_password_length", 0)
        system_limited = cfg.get("system_limitation_documented", False)
        required_min = PASSWORD_MIN_LENGTH_SYSTEM_LIMITED if system_limited else PASSWORD_MIN_LENGTH
        if min_len < required_min:
            violations.append(
                f"System {cfg['system_id']}: min length {min_len} < {required_min}"
            )
    assert not violations, (
        f"VIOLATION (8.3.6): {len(violations)} system(s) with insufficient password "
        f"length:\n" + "\n".join(violations)
    )


def test_password_requires_alphanumeric(auth_system_configs):
    violations = [
        s for s in auth_system_configs
        if not s.get("requires_numeric") or not s.get("requires_alpha")
    ]
    assert not violations, (
        f"VIOLATION (8.3.6): {len(violations)} system(s) without alphanumeric "
        f"requirement: {[s['system_id'] for s in violations]}"
    )


def test_password_history_enforced(auth_system_configs):
    violations = [
        s for s in auth_system_configs
        if s.get("password_history_count", 0) < PASSWORD_HISTORY_COUNT
    ]
    assert not violations, (
        f"VIOLATION (8.3.7): {len(violations)} system(s) with password history < "
        f"{PASSWORD_HISTORY_COUNT}: {[s['system_id'] for s in violations]}"
    )


def test_account_lockout_threshold(auth_system_configs):
    violations = [
        s for s in auth_system_configs
        if s.get("max_failed_attempts", 9999) > MAX_FAILED_ATTEMPTS
    ]
    assert not violations, (
        f"VIOLATION (8.3.4): {len(violations)} system(s) allow more than "
        f"{MAX_FAILED_ATTEMPTS} failed attempts: "
        f"{[(s['system_id'], s.get('max_failed_attempts')) for s in violations]}"
    )


def test_lockout_duration(auth_system_configs):
    violations = [
        s for s in auth_system_configs
        if not s.get("lockout_requires_admin_reset")
        and s.get("lockout_duration_minutes", 0) < LOCKOUT_MIN_DURATION_MINUTES
    ]
    assert not violations, (
        f"VIOLATION (8.3.4): {len(violations)} system(s) lockout duration < "
        f"{LOCKOUT_MIN_DURATION_MINUTES} min and no admin-reset: "
        f"{[(s['system_id'], s.get('lockout_duration_minutes')) for s in violations]}"
    )


def test_service_account_password_rotation(service_account_records):
    today = date.today()
    violations = []
    for acct in service_account_records:
        last_rotated = acct.get("password_last_rotated_date")
        if not last_rotated:
            violations.append(f"{acct['account_id']}: no rotation date on record")
            continue
        days = (today - last_rotated).days
        if days > SERVICE_ACCOUNT_MAX_ROTATION_DAYS:
            violations.append(
                f"{acct['account_id']}: last rotated {days} days ago "
                f"(max {SERVICE_ACCOUNT_MAX_ROTATION_DAYS})"
            )
    assert not violations, (
        f"VIOLATION (8.3.9): {len(violations)} service account(s) overdue for "
        f"password rotation:\n" + "\n".join(violations)
    )
```

### `tests/req8/test_8_4_mfa.py`

```python
"""
PCI DSS v4.0 Req 8.4 — Multi-Factor Authentication
Confidence: HIGH | Human Review: ASSUMPTION REQUIRED (ASSUME-8-001) for replay-resistance
"""
import pytest


def test_mfa_enabled_for_all_cde_access(cde_system_configs):
    """8.4.2 — MFA required for ALL CDE access (v4.0 expanded scope)."""
    violations = [
        s for s in cde_system_configs
        if s.get("in_cde") and not s.get("mfa_enabled")
    ]
    assert not violations, (
        f"VIOLATION (8.4.2): {len(violations)} CDE system(s) without MFA: "
        f"{[s['system_id'] for s in violations]}"
    )


def test_mfa_cannot_be_bypassed(cde_system_configs):
    violations = [
        s for s in cde_system_configs
        if s.get("in_cde") and s.get("mfa_enabled")
        and not s.get("mfa_bypass_controls_implemented")
    ]
    assert not violations, (
        f"VIOLATION (8.4.3): {len(violations)} CDE system(s) where MFA bypass "
        f"is uncontrolled: {[s['system_id'] for s in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-8-001",
    description=(
        "SMS OTP may not satisfy replay-resistance per 8.4.3. "
        "Flag for QSA review. Acceptable: FIDO2, TOTP/HOTP, hardware token, "
        "push with device binding."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_no_sms_otp_without_qsa_approval(mfa_implementations):
    sms_without_review = [
        m for m in mfa_implementations
        if m.get("method") == "sms_otp"
        and not m.get("qsa_replay_resistance_approved")
    ]
    if sms_without_review:
        import warnings
        warnings.warn(
            f"{len(sms_without_review)} system(s) using SMS OTP without QSA "
            f"replay-resistance approval (8.4.3): "
            f"{[m['system_id'] for m in sms_without_review]}"
        )


def test_no_hardcoded_service_account_passwords(service_account_records):
    """8.6.2 — Service account passwords must not be hard-coded."""
    hardcoded = [
        r for r in service_account_records
        if r.get("password_source") == "hardcoded"
    ]
    assert not hardcoded, (
        f"VIOLATION (8.6.2): {len(hardcoded)} service account(s) with hard-coded "
        f"passwords: {[r['account_id'] for r in hardcoded]}"
    )
```

---

## Notes for the registry

- **v4.0 MFA scope expansion:** In v3.2.1, MFA was required only for non-console administrative access. v4.0 Req 8.4.2 requires MFA for ALL CDE access — every user, every system. This is the highest-impact v4.0 change for Req 8.
- **SMS OTP:** Not explicitly prohibited but 8.4.3 "not susceptible to replay attacks" creates QSA risk for SMS due to SIM-swapping and SS7 vulnerabilities. FIDO2/WebAuthn or TOTP is strongly recommended for new implementations.
- **Admin-reset vs. timed lockout:** Either satisfies 8.3.4 — an account requiring admin reset to unlock is an alternative to a 30-minute timed lockout, not a replacement.
- **Shared accounts exception scope:** 8.2.2 permits shared/generic accounts only when: use is necessary, authorized by management, time-limited, and individual authentication precedes use. Application service accounts shared across processes (not users) fall under 8.6 instead.
- **Password system limitations:** The "8 characters if system limitation" in 8.3.6 is a carve-out for legacy systems that cannot be configured for 12+ character passwords. The limitation must be documented. New system deployments should always target 12+ characters.
