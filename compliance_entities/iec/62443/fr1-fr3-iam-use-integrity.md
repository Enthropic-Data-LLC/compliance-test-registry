# IEC 62443 — FR1 (IAC), FR2 (Use Control), FR3 (System Integrity)

**Framework:** IEC 62443-3-3:2013 System Security Requirements; 62443-4-2 Component Requirements
**Foundational Requirements:** FR 1 (Identification and Authentication), FR 2 (Use Control), FR 3 (System Integrity)
**System Requirements:** SR 1.1–1.13, SR 2.1–2.12, SR 3.1–3.9
**Confidence:** DETERMINISTIC-dominant once Security Level Target (SL-T) is established
**Last parsed:** 2026-05-21

---

## Scope pre-condition

```python
def requires_iec62443(entity_profile: dict) -> bool:
    """
    True if organization is an asset owner operating Industrial Automation and Control
    Systems (IACS), a system integrator deploying IACS, or a component supplier building
    products for IACS. Note: NERC CIP governs electric utility BES Cyber Systems separately.
    """
    return entity_profile.get("iec62443_in_scope", False)
```

---

## Constants

```python
# Security Level targets — org-defined from 62443-3-2 risk assessment
IEC62443_SL_LEVELS = frozenset({1, 2, 3, 4})

# FR 1 — Authentication
IEC62443_LOGIN_BANNER_REQUIRED_AT_SL = 2        # SR 1.12
IEC62443_LOCKOUT_REQUIRED = True                # SR 1.11 — all SLs
IEC62443_MFA_REQUIRED_AT_SL = 2                 # SR 1.13 (untrusted networks) + enhancement at SL 2+

# FR 2 — Session controls
IEC62443_SESSION_LOCK_REQUIRED_AT_SL = 2        # SR 2.5

# FR 3 — Integrity
IEC62443_MALWARE_PROTECTION_REQUIRED = True     # SR 3.2 — all SLs
IEC62443_AUDIT_LOG_PROTECTION_REQUIRED = True   # SR 3.9 — all SLs
IEC62443_TIMESTAMPS_REQUIRED = True             # SR 2.11 — all SLs

# Password policy (SR 1.7) — org-defined minimums bounded by SL
IEC62443_MIN_PASSWORD_LENGTH_SL1 = 8
IEC62443_MIN_PASSWORD_LENGTH_SL2 = 10
IEC62443_MAX_FAILED_ATTEMPTS_BEFORE_LOCKOUT = 5  # SR 1.11 — org-defined upper bound

# Prohibited authenticator feedback (SR 1.10)
IEC62443_AUTH_FEEDBACK_MUST_NOT_REVEAL_CREDENTIALS = True
```

---

## Zone and conduit pre-condition

Before FR tests run, the zone/conduit architecture must be established and SL-T assigned per zone.

```python
@pytest.fixture(autouse=True)
def iec62443_scope(entity_profile: dict):
    if not entity_profile.get("iec62443_in_scope", False):
        pytest.skip("IEC 62443 not in scope")

def get_zone_sl_target(zone_id: str, controls_evidence: dict) -> int:
    """Returns the SL-T for a given zone from the 62443-3-2 risk assessment."""
    zones = controls_evidence.get("iec62443_zones", [])
    for z in zones:
        if z["zone_id"] == zone_id:
            return z.get("sl_target", 1)
    return 1

class TestZoneConduitArchitecture:
    """62443-3-2 — Zone/conduit model must be defined before SR-level tests."""

    def test_zone_conduit_model_defined(self, controls_evidence: dict):
        assert controls_evidence.get("iec62443_zones"), (
            "Security zones must be defined with SL-T assignments before applying SR tests "
            "(IEC 62443-3-2 §5)"
        )

    def test_all_zones_have_sl_target(self, controls_evidence: dict):
        zones = controls_evidence.get("iec62443_zones", [])
        no_sl_target = [z for z in zones if not z.get("sl_target")]
        assert not no_sl_target, (
            f"All zones must have a Security Level Target (SL-T) from risk assessment. "
            f"Missing: {[z['zone_id'] for z in no_sl_target]}"
        )

    def test_conduits_defined_between_zones(self, controls_evidence: dict):
        assert controls_evidence.get("iec62443_conduits") is not None, (
            "Conduits between zones must be defined and have SL-T assigned "
            "(IEC 62443-3-2 §5)"
        )
```

---

## FR 1 — Identification and Authentication Control (IAC)

### SR 1.1 — Human User Identification and Authentication

**Overall: DETERMINISTIC — Pattern 1**

```python
import pytest

class TestFR1_IAC:
    """FR 1 — IAC: user/device authentication, account management, password policy, lockout."""

    def test_all_iacs_users_have_unique_identifiers(self, controls_evidence: dict):
        accounts = controls_evidence.get("iec62443_user_accounts", [])
        shared_accounts = [a for a in accounts if a.get("is_shared_account", False)]
        assert not shared_accounts, (
            f"All IACS users must have unique identifiers — shared accounts prohibited "
            f"(IEC 62443 SR 1.1). Shared accounts found: {[a['account_id'] for a in shared_accounts]}"
        )

    def test_authentication_required_for_all_iacs_access(self, controls_evidence: dict):
        systems = controls_evidence.get("iec62443_systems", [])
        no_auth = [s for s in systems if not s.get("authentication_required", True)]
        assert not no_auth, (
            f"Authentication must be required for all IACS access (IEC 62443 SR 1.1). "
            f"No auth required: {[s['system_id'] for s in no_auth]}"
        )

    # SR 1.3 — Account Management
    def test_inactive_accounts_disabled_or_removed(self, controls_evidence: dict):
        accounts = controls_evidence.get("iec62443_user_accounts", [])
        active_inactive = [
            a for a in accounts
            if a.get("user_status") == "inactive"
            and a.get("account_status") == "enabled"
        ]
        assert not active_inactive, (
            f"Accounts for inactive users must be disabled or removed (IEC 62443 SR 1.3). "
            f"Active-but-inactive: {[a['account_id'] for a in active_inactive]}"
        )

    # SR 1.4 — Identifier Management
    def test_no_identifier_reuse(self, controls_evidence: dict):
        iam = controls_evidence.get("iec62443_iam", {})
        assert iam.get("identifier_reuse_prevented", False), (
            "Identifiers must not be reused — each user/device has a unique, non-reused ID "
            "(IEC 62443 SR 1.4)"
        )

    # SR 1.5 — Authenticator Management
    def test_password_management_procedure_enforced(self, controls_evidence: dict):
        iam = controls_evidence.get("iec62443_iam", {})
        assert iam.get("password_lifecycle_managed", False), (
            "Authenticators (passwords/tokens/certs) must be managed: strength enforced, "
            "expiry/revocation in place (IEC 62443 SR 1.5)"
        )

    # SR 1.7 — Strength of Password-based Authentication
    def test_password_minimum_length_meets_sl(self, controls_evidence: dict):
        zones = controls_evidence.get("iec62443_zones", [])
        for zone in zones:
            sl_t = zone.get("sl_target", 1)
            min_required = (
                IEC62443_MIN_PASSWORD_LENGTH_SL2
                if sl_t >= 2
                else IEC62443_MIN_PASSWORD_LENGTH_SL1
            )
            configured_min = zone.get("password_minimum_length", 0)
            assert configured_min >= min_required, (
                f"Zone '{zone['zone_id']}' (SL-T {sl_t}): password minimum length "
                f"{configured_min} is below required {min_required} (IEC 62443 SR 1.7)"
            )

    # SR 1.10 — Authenticator Feedback
    def test_authentication_feedback_does_not_reveal_credentials(
        self, controls_evidence: dict
    ):
        iam = controls_evidence.get("iec62443_iam", {})
        assert iam.get("auth_feedback_hides_credentials", False), (
            "Authentication feedback must not reveal credential content — "
            "passwords must not be echoed (IEC 62443 SR 1.10)"
        )

    # SR 1.11 — Unsuccessful Login Attempts
    def test_account_lockout_configured(self, controls_evidence: dict):
        iam = controls_evidence.get("iec62443_iam", {})
        assert iam.get("account_lockout_enabled", False), (
            "Account lockout must be configured after defined number of failed login attempts "
            "(IEC 62443 SR 1.11)"
        )
        max_attempts = iam.get("lockout_threshold_attempts", 999)
        assert max_attempts <= IEC62443_MAX_FAILED_ATTEMPTS_BEFORE_LOCKOUT, (
            f"Lockout threshold {max_attempts} exceeds maximum allowed "
            f"{IEC62443_MAX_FAILED_ATTEMPTS_BEFORE_LOCKOUT} (IEC 62443 SR 1.11)"
        )

    # SR 1.12 — System Use Notification (SL 2+)
    def test_login_banner_present_at_sl2_plus(self, controls_evidence: dict):
        zones = controls_evidence.get("iec62443_zones", [])
        sl2_zones = [z for z in zones if z.get("sl_target", 1) >= IEC62443_LOGIN_BANNER_REQUIRED_AT_SL]
        systems_in_sl2_zones = [
            s for s in controls_evidence.get("iec62443_systems", [])
            if s.get("zone_id") in {z["zone_id"] for z in sl2_zones}
        ]
        no_banner = [s for s in systems_in_sl2_zones if not s.get("login_banner_configured", False)]
        assert not no_banner, (
            f"Login banner (system use notification) required at SL 2+ "
            f"(IEC 62443 SR 1.12). Missing: {[s['system_id'] for s in no_banner]}"
        )
```

---

## FR 2 — Use Control (UC)

### SR 2.1–2.12

**Overall: DETERMINISTIC (session lock, timestamps, audit events, session termination)**

```python
class TestFR2_UseControl:
    """FR 2 — Use control: least privilege, session management, audit logging, timestamps."""

    # SR 2.1 — Authorization Enforcement
    @pytest.mark.assumption(
        id="ASSUME-62443-FR2-001",
        description=(
            "Role-based access control enforced for IACS access; roles defined based on "
            "functional requirements; access rights assigned by role, not individual (except "
            "emergency accounts); least-privilege principle applied — roles have minimum access "
            "required for job function; role assignments reviewed at minimum annually or when "
            "personnel roles change; documentation: RBAC matrix per zone"
        ),
        approved_by="IACS_security_manager",
        review_date="2027-05-21",
    )
    def test_least_privilege_enforced_for_iacs_access(self, controls_evidence: dict):
        uc = controls_evidence.get("iec62443_use_control", {})
        assert uc.get("least_privilege_enforced", False), (
            "Least privilege must be enforced for IACS access — each role has minimum "
            "necessary permissions (IEC 62443 SR 2.1)"
        )

    # SR 2.5 — Session Lock (SL 2+)
    def test_session_lock_configured_at_sl2(self, controls_evidence: dict):
        zones = controls_evidence.get("iec62443_zones", [])
        sl2_zones = [z for z in zones if z.get("sl_target", 1) >= IEC62443_SESSION_LOCK_REQUIRED_AT_SL]
        systems_in_sl2_zones = [
            s for s in controls_evidence.get("iec62443_systems", [])
            if s.get("zone_id") in {z["zone_id"] for z in sl2_zones}
        ]
        no_session_lock = [
            s for s in systems_in_sl2_zones
            if not s.get("session_lock_configured", False)
        ]
        assert not no_session_lock, (
            f"Session lock after inactivity must be configured for SL 2+ systems "
            f"(IEC 62443 SR 2.5). Missing: {[s['system_id'] for s in no_session_lock]}"
        )

    # SR 2.6 — Remote Session Termination
    def test_remote_session_termination_available(self, controls_evidence: dict):
        uc = controls_evidence.get("iec62443_use_control", {})
        assert uc.get("remote_session_termination_available", False), (
            "Ability to terminate remote sessions must be available to authorized personnel "
            "(IEC 62443 SR 2.6)"
        )

    # SR 2.7 — Concurrent Session Control (SL 3+)
    def test_concurrent_sessions_limited_at_sl3(self, controls_evidence: dict):
        zones = controls_evidence.get("iec62443_zones", [])
        sl3_zones = [z for z in zones if z.get("sl_target", 1) >= 3]
        systems_in_sl3 = [
            s for s in controls_evidence.get("iec62443_systems", [])
            if s.get("zone_id") in {z["zone_id"] for z in sl3_zones}
        ]
        no_concurrent_limit = [
            s for s in systems_in_sl3
            if not s.get("concurrent_session_limit_configured", False)
        ]
        assert not no_concurrent_limit, (
            f"Concurrent session limits must be configured at SL 3+ (IEC 62443 SR 2.7). "
            f"Missing: {[s['system_id'] for s in no_concurrent_limit]}"
        )

    # SR 2.8 — Auditable Events
    def test_auditable_events_defined_and_logged(self, controls_evidence: dict):
        uc = controls_evidence.get("iec62443_use_control", {})
        assert uc.get("auditable_events_defined", False), (
            "List of auditable events must be defined and audit logging enabled "
            "(IEC 62443 SR 2.8)"
        )
        assert uc.get("audit_logging_enabled", False), (
            "Audit logging must be enabled for all defined auditable events (IEC 62443 SR 2.8)"
        )

    # SR 2.11 — Timestamps
    def test_timestamps_synchronized_via_ntp(self, controls_evidence: dict):
        uc = controls_evidence.get("iec62443_use_control", {})
        assert uc.get("time_synchronization_configured", False), (
            "Timestamps must be synchronized via NTP or equivalent time source for accurate "
            "audit log correlation (IEC 62443 SR 2.11)"
        )
```

---

## FR 3 — System Integrity (SI)

### SR 3.1–3.9

**Overall: DETERMINISTIC (malware protection, audit log protection, timestamps)**

```python
class TestFR3_SystemIntegrity:
    """FR 3 — System integrity: malware protection, communication integrity, audit protection."""

    # SR 3.2 — Malicious Code Protection
    def test_malware_protection_deployed_on_applicable_systems(
        self, controls_evidence: dict
    ):
        systems = controls_evidence.get("iec62443_systems", [])
        applicable = [
            s for s in systems
            if s.get("malware_protection_applicable", True)
        ]
        no_malware_protection = [
            s for s in applicable
            if not s.get("malware_protection_deployed", False)
        ]
        assert not no_malware_protection, (
            f"Malware protection must be deployed on IACS systems where technically feasible "
            f"(IEC 62443 SR 3.2). Missing: {[s['system_id'] for s in no_malware_protection]}"
        )

    def test_malware_definitions_maintained(self, controls_evidence: dict):
        integrity = controls_evidence.get("iec62443_integrity", {})
        if not integrity.get("malware_protection_in_use", False):
            return
        assert integrity.get("malware_definitions_update_configured", False), (
            "Malware protection definitions/signatures must be kept current "
            "(IEC 62443 SR 3.2)"
        )

    # SR 3.2 — Compensating control where AV not feasible
    @pytest.mark.assumption(
        id="ASSUME-62443-FR3-001",
        description=(
            "For legacy IACS systems where malware protection cannot be installed (PLCs, "
            "legacy SCADA, end-of-life OS): compensating controls documented and implemented; "
            "compensating controls include at minimum: network-level isolation (dedicated zone), "
            "application whitelisting where technically feasible, integrity monitoring of "
            "configuration files from external system; compensating controls reviewed annually "
            "and when system environment changes"
        ),
        approved_by="IACS_security_manager",
        review_date="2027-05-21",
    )
    def test_legacy_systems_without_av_have_compensating_controls(
        self, controls_evidence: dict
    ):
        systems = controls_evidence.get("iec62443_systems", [])
        legacy_no_av = [
            s for s in systems
            if not s.get("malware_protection_applicable", True)
        ]
        missing_compensating = [
            s for s in legacy_no_av
            if not s.get("compensating_controls_documented", False)
        ]
        assert not missing_compensating, (
            f"Compensating controls must be documented for IACS systems where malware "
            f"protection cannot be installed (IEC 62443 SR 3.2 — compensating control). "
            f"Missing: {[s['system_id'] for s in missing_compensating]}"
        )

    # SR 3.9 — Protection of Audit Information
    def test_audit_logs_protected_from_modification(self, controls_evidence: dict):
        integrity = controls_evidence.get("iec62443_integrity", {})
        assert integrity.get("audit_logs_write_protected", False), (
            "Audit logs must be protected from unauthorized modification or deletion "
            "(IEC 62443 SR 3.9)"
        )

    @pytest.mark.assumption(
        id="ASSUME-62443-FR3-002",
        description=(
            "Communication integrity protection implemented proportionate to SL: "
            "SL 1 — checksum or equivalent; SL 2+ — cryptographic message authentication "
            "(HMAC or equivalent) for all communications in security zones; "
            "SL 3+ — cryptographic integrity with authenticated encryption; "
            "legacy industrial protocols without native integrity (Modbus, DNP3 serial): "
            "integrity provided at the network layer via encrypted tunnel or dedicated conduit"
        ),
        approved_by="IACS_security_manager",
        review_date="2027-05-21",
    )
    def test_communication_integrity_protection_configured(
        self, controls_evidence: dict
    ):
        integrity = controls_evidence.get("iec62443_integrity", {})
        assert integrity.get("communication_integrity_configured", False), (
            "Communication integrity protection must be configured (checksums at SL 1, "
            "cryptographic MAC at SL 2+) (IEC 62443 SR 3.1)"
        )
```

---

## Open assumptions

| ID | FR | Summary | Review date |
|---|---|---|---|
| ASSUME-62443-FR2-001 | FR 2 / SR 2.1 | RBAC enforced; roles by function; least privilege; annual review; RBAC matrix per zone | 2027-05-21 |
| ASSUME-62443-FR3-001 | FR 3 / SR 3.2 | Legacy IACS without AV: compensating controls (network isolation, app whitelisting, integrity monitoring) | 2027-05-21 |
| ASSUME-62443-FR3-002 | FR 3 / SR 3.1 | Communication integrity by SL: checksum (SL 1), HMAC (SL 2+), legacy protocols via network layer | 2027-05-21 |

---

## Cross-standard notes

**NERC CIP ↔ IEC 62443 FR1:** NERC CIP CIP-007-6 R5 (account management) and CIP-005-7 (ESP access control) map directly to SR 1.1/1.3/1.11. Electric utilities satisfying CIP-007-6 R5 have strong coverage of FR 1. The key gap is that NERC CIP focuses on BES Cyber Systems; non-BES OT systems require IEC 62443 coverage.

**NIST 800-53 IA family ↔ FR 1:** NIST 800-53 IA-2 (Identification and Authentication), IA-5 (Authenticator Management), and AC-7 (Unsuccessful Login Attempts) map to SR 1.1, 1.5, and 1.11 respectively. See `data/thesaurus.yml` for cross-framework mappings.
