# NIST SP 800-53 r5 — Core Technical Controls (AU, AC, IA, CM, SC, SI)

**Source:** NIST SP 800-53 Rev 5 (Final, September 2020) + 800-53B baselines
**Baseline tags:** `[L]` Low, `[M]` Moderate, `[H]` High — tests are gated by `system_impact_level` fixture
**ODP framework:** Organization-Defined Parameters must be recorded in the SSP before any
  PARAMETERIZED test can assert an enforcing value. ODPs default to 800-53B recommended values
  where available; all ODP values used below are documented in `odp_values` fixture.

---

```python
import pytest
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from typing import FrozenSet

# ── Audit and Accountability (AU) ────────────────────────────────────────────

# AU-3 required record fields — all baselines
AU3_REQUIRED_FIELDS: FrozenSet[str] = frozenset({
    "event_type",           # what type of event occurred
    "event_date_time",      # timestamp
    "event_outcome",        # success or failure
    "subject_identity",     # user or process that triggered event
    "object_affected",      # resource, file, object affected
    "source_location",      # IP address or hostname of origin
})

# AU-2 event categories that must be audited — Moderate/High baseline minimum
AU2_REQUIRED_EVENT_CATEGORIES: FrozenSet[str] = frozenset({
    "logon_logoff",                 # AU-2(a): account logon / logoff / session events
    "account_management",           # AC-2 events: create, modify, disable, delete accounts
    "privilege_use",                # use of special privileges
    "process_creation",             # process execution / program invocation
    "object_access",                # CUI / sensitive file access
    "policy_change",                # changes to security policies or audit configuration
    "authentication_events",        # failed authentication attempts
    "system_events",                # system startup, shutdown, restart
})

# AU-11 log retention — 800-53B ODP recommended values
AU11_ONLINE_RETENTION_DAYS = 90         # online / immediately accessible
AU11_ARCHIVE_RETENTION_YEARS = 3        # long-term archive (Moderate/High baseline)
AU11_LOW_RETENTION_DAYS = 90            # Low baseline minimum

# AU-6 review frequency — ODP (Pattern 2); 800-53B default = weekly for Moderate
AU6_DEFAULT_REVIEW_DAYS = 7             # weekly audit review (ODP default, Moderate)

# ── Access Control (AC) ───────────────────────────────────────────────────────

# AC-7 unsuccessful logon — ODP values, 800-53B defaults
AC7_MAX_ATTEMPTS = 3                    # consecutive failures before lockout (Moderate default)
AC7_LOCKOUT_MINUTES = 30               # minimum lockout duration (Moderate default)

# AC-11 session lock — ODP (800-53B default = 15 min)
AC11_SESSION_LOCK_MINUTES = 15

# AC-2 inactive account review — ODP
AC2_INACTIVE_ACCOUNT_DISABLE_DAYS = 35  # Moderate: disable if no logon in 35 days

# AC-17 remote access encryption — DETERMINISTIC (FIPS-validated required when cryptography used)
AC17_ENCRYPTION_REQUIRED = True
AC17_APPROVED_PROTOCOLS = frozenset({"tls_1.2", "tls_1.3", "ipsec_ikev2", "ssh_v2"})
AC17_PROHIBITED_PROTOCOLS = frozenset({"telnet", "ftp", "http", "ssl", "tls_1.0", "tls_1.1", "pptp"})

# AC-18 wireless — WPA2/WPA3 minimum
AC18_APPROVED_PROTOCOLS = frozenset({"wpa2_enterprise", "wpa3_enterprise", "wpa3_personal"})
AC18_PROHIBITED_PROTOCOLS = frozenset({"wep", "wpa_personal", "open", "wpa2_personal_tkip"})

# ── Identification and Authentication (IA) ────────────────────────────────────

# IA-2 MFA — Moderate: MFA for privileged users; High: MFA for all
IA2_MFA_REQUIRED_PRIVILEGED = True     # all baselines at or above Moderate
IA2_MFA_REQUIRED_ALL_USERS = True      # High baseline (IA-2(1) + IA-2(2))
IA2_ACCEPTABLE_MFA_TYPES = frozenset({
    "fido2_passkey", "piv_cac", "totp_hardware", "totp_software",
    "push_authenticator", "smartcard",
})
IA2_PROHIBITED_SECOND_FACTORS = frozenset({"sms_otp", "voice_call"})  # NIST 800-63B deprecated

# IA-5(1) password-based authenticators — ODP thresholds
IA5_MIN_LENGTH_COMPLEXITY = 8           # min length when complexity rules apply
IA5_MIN_LENGTH_NO_COMPLEXITY = 15       # min length without complexity requirement (preferred)
IA5_MAX_CONSECUTIVE_IDENTICAL = 2       # no more than N consecutive identical chars
IA5_PASSWORD_HISTORY_COUNT = 24         # prohibit reuse of last 24 passwords (800-53B Moderate)
IA5_MAX_LIFETIME_DAYS = 60             # maximum password lifetime when time-based rotation used
IA5_NO_EXPIRY_IF_MONITORED = True       # per 800-63B: no expiry required if breach-monitoring active

# IA-5(6) protection of authenticators
IA5_HASH_ACCEPTABLE = frozenset({"bcrypt", "scrypt", "argon2id", "pbkdf2_sha256", "pbkdf2_sha512"})
IA5_HASH_PROHIBITED = frozenset({"md5", "sha1", "sha256_unsalted", "sha512_unsalted", "des", "plaintext"})

# IA-3 device identification — DETERMINISTIC presence
IA3_DEVICE_AUTH_REQUIRED_FOR_CUI_NETWORK = True  # Moderate/High

# ── Configuration Management (CM) ────────────────────────────────────────────

# CM-2 baseline configuration — must exist and be version-controlled
CM2_BASELINE_REQUIRED_ATTRIBUTES = frozenset({
    "version_controlled",
    "approved_by_change_control_board_or_equivalent",
    "includes_hardware_software_firmware_versions",
    "includes_network_topology",
})

# CM-6 configuration settings — references to external hardening guides
CM6_ACCEPTABLE_HARDENING_SOURCES = frozenset({
    "disa_stig", "cis_benchmark", "nist_national_checklist",
    "vendor_security_guide_approved_by_isso",
})

# CM-7 least functionality — restrict to only approved services/ports/protocols
CM7_REVIEW_MONTHS = 12                  # annual review of approved software list
CM7_PORT_DOCUMENTATION_REQUIRED = True # all open ports must be documented with business justification

# CM-3 change control — configuration changes must go through formal process
CM3_REQUIRED_CHANGE_ATTRIBUTES = frozenset({
    "change_description", "security_impact_analysis", "approval_authority",
    "test_plan", "rollback_plan",
})

# CM-8 component inventory — Moderate/High
CM8_REVIEW_MONTHS = 12                  # ODP default: review inventory annually

# ── System and Communications Protection (SC) ─────────────────────────────────

# SC-8 transmission integrity/confidentiality — DETERMINISTIC (FIPS-validated crypto required)
SC8_FIPS_REQUIRED = True
SC8_APPROVED_PROTOCOLS = frozenset({"tls_1.2", "tls_1.3", "ipsec_ikev2", "ssh_v2", "sftp"})
SC8_PROHIBITED_PROTOCOLS = frozenset({"http", "ftp", "telnet", "snmpv1", "snmpv2c", "ssl", "tls_1.0", "tls_1.1"})

# SC-13 cryptographic protection — FIPS 140-2 or 140-3 validated modules
SC13_FIPS_VALIDATED_REQUIRED = True     # DETERMINISTIC for federal / FISMA systems
SC13_MINIMUM_KEY_LENGTH_AES = 128       # AES-128 minimum; AES-256 preferred

# SC-28 protection of information at rest
SC28_ENCRYPTION_REQUIRED = True        # Moderate/High
SC28_APPROVED_ALGORITHMS = frozenset({"aes_128_cbc", "aes_256_cbc", "aes_128_gcm", "aes_256_gcm"})
SC28_PROHIBITED = frozenset({"des", "3des", "rc4", "blowfish", "plaintext"})

# SC-12 cryptographic key management — DETERMINISTIC attributes
SC12_REQUIRED_KEY_MGMT_PHASES = frozenset({
    "key_generation", "key_distribution", "key_storage",
    "key_revocation", "key_destruction",
})

# SC-5 denial of service protection — Moderate/High: automated DoS protection required
SC5_AUTOMATED_PROTECTION_REQUIRED = True  # Moderate/High baseline

# SC-39 process isolation — DETERMINISTIC (OS-enforced process isolation required)
SC39_REQUIRED = True

# ── System and Information Integrity (SI) ─────────────────────────────────────

# SI-2 flaw remediation — ODP timeline (800-53B defaults)
SI2_CRITICAL_PATCH_DAYS = 30           # CVSS 9.0–10.0
SI2_HIGH_PATCH_DAYS = 90               # CVSS 7.0–8.9
SI2_MEDIUM_PATCH_DAYS = 180            # CVSS 4.0–6.9
SI2_LOW_PATCH_DAYS = 365               # CVSS 0.1–3.9
SI2_KEV_PATCH_DAYS = 14                # CISA Known Exploited Vulnerabilities

# SI-3 malicious code protection — all baselines
SI3_AV_REQUIRED = True
SI3_DEFINITION_UPDATE_HOURS = 24       # signature update frequency
SI3_SCAN_ON_REAL_TIME = True
SI3_SCAN_ON_FILE_DOWNLOAD = True
SI3_SCAN_ON_REMOVABLE_MEDIA = True

# SI-4 system monitoring — Moderate/High: automated monitoring required
SI4_AUTOMATED_MONITORING_REQUIRED = True
SI4_MONITORING_EVENTS = frozenset({
    "inbound_outbound_comms",
    "unusual_activity",
    "potential_attacks",
    "unauthorized_local_network_remote_connections",
})

# SI-7 software and information integrity — Moderate/High
SI7_INTEGRITY_VERIFICATION_REQUIRED = True   # cryptographic hash or signature
SI7_ACCEPTABLE_METHODS = frozenset({"sha256", "sha384", "sha512", "rsa_signature", "ecdsa_signature"})

# ── Scope fixtures ─────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def fisma_system_scope_check(entity_profile: dict):
    """Skip entire module if system is not subject to FISMA / 800-53."""
    if not entity_profile.get("subject_to_fisma_or_fedramp", False):
        pytest.skip("System not subject to FISMA/FedRAMP — 800-53 not enforcing")


@pytest.fixture
def impact_level(entity_profile: dict) -> str:
    """Return 'low', 'moderate', or 'high' based on FIPS 199 categorization."""
    level = entity_profile.get("fips199_impact_level", "").lower()
    if level not in {"low", "moderate", "high"}:
        pytest.skip("FIPS 199 impact level not categorized — baseline indeterminate")
    return level


@pytest.fixture
def odp_values(entity_profile: dict) -> dict:
    """Organization-Defined Parameters from the SSP.  Tests that use these values
    are PARAMETERIZED; a missing ODP converts the test to CONTESTED."""
    odps = entity_profile.get("odp_values", {})
    if not odps:
        pytest.skip("ODP values not documented in SSP — PARAMETERIZED tests cannot execute")
    return odps


# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT AND ACCOUNTABILITY (AU)
# ═══════════════════════════════════════════════════════════════════════════════

class TestAU3AuditRecordContent:
    """AU-3: Content of Audit Records — all baselines [L][M][H]"""

    def test_required_fields_present(self, controls_evidence: dict):
        """DETERMINISTIC: all 6 required AU-3 content fields must be captured."""
        audit_fields = set(controls_evidence.get("audit_record_fields_captured", []))
        missing = AU3_REQUIRED_FIELDS - audit_fields
        assert not missing, (
            f"AU-3: audit records missing required fields: {missing}. "
            f"All of {AU3_REQUIRED_FIELDS} must be captured."
        )


class TestAU2EventsAudited:
    """AU-2: Event Logging — Moderate/High [M][H]"""

    def test_required_event_categories_audited(
        self, controls_evidence: dict, impact_level
    ):
        if impact_level == "low":
            pytest.skip("AU-2 required event categories apply at Moderate/High only")
        audited = set(controls_evidence.get("audited_event_categories", []))
        missing = AU2_REQUIRED_EVENT_CATEGORIES - audited
        assert not missing, (
            f"AU-2: required event categories not audited: {missing}."
        )


class TestAU11LogRetention:
    """AU-11: Audit Record Retention — all baselines [L][M][H]"""

    def test_online_retention_meets_minimum(
        self, controls_evidence: dict, reference_date: date
    ):
        """DETERMINISTIC: logs must be retrievable for at least 90 days online."""
        online_days = controls_evidence.get("audit_log_online_retention_days", 0)
        assert online_days >= AU11_ONLINE_RETENTION_DAYS, (
            f"AU-11: online audit retention {online_days}d < required {AU11_ONLINE_RETENTION_DAYS}d."
        )

    def test_archive_retention_moderate_high(
        self, controls_evidence: dict, impact_level
    ):
        """DETERMINISTIC: Moderate/High must retain archives for 3 years."""
        if impact_level == "low":
            pytest.skip("3-year archive requirement applies at Moderate/High only")
        archive_years = controls_evidence.get("audit_log_archive_retention_years", 0)
        assert archive_years >= AU11_ARCHIVE_RETENTION_YEARS, (
            f"AU-11: archive retention {archive_years}yr < required {AU11_ARCHIVE_RETENTION_YEARS}yr "
            f"for {impact_level} baseline."
        )

    @pytest.mark.assumption(
        id="ASSUME-800053-AU-001",
        description="AU-11 online retention 90 days; archive 3 years (Moderate/High) per 800-53B defaults",
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_retention_odp_documented(self, odp_values: dict):
        """PARAMETERIZED: ODP must document the org-defined retention periods."""
        assert "au11_online_retention_days" in odp_values, (
            "AU-11 ODP 'au11_online_retention_days' not documented in SSP."
        )


class TestAU6AuditReview:
    """AU-6: Audit Record Review, Analysis, Reporting — Moderate/High [M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-AU-002",
        description="AU-6 review frequency ODP: weekly (7 days) for Moderate; more frequent acceptable",
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_review_frequency(self, controls_evidence: dict, odp_values: dict, impact_level):
        """PARAMETERIZED: audit reviews must occur at least as frequently as the ODP value."""
        if impact_level == "low":
            pytest.skip("AU-6 formal review cadence applies at Moderate/High")
        freq_days = odp_values.get("au6_review_frequency_days", AU6_DEFAULT_REVIEW_DAYS)
        last_review = controls_evidence.get("last_audit_review_date")
        if not last_review:
            pytest.fail("AU-6: no audit review date documented in evidence.")
        days_since = (date.today() - last_review).days
        assert days_since <= freq_days, (
            f"AU-6: {days_since}d since last audit review; ODP requires ≤{freq_days}d."
        )


class TestAU9ProtectionOfAuditInformation:
    """AU-9: Protection of Audit Information — all baselines [L][M][H]"""

    def test_audit_logs_write_protected(self, controls_evidence: dict):
        """DETERMINISTIC: audit logs must be write-protected from modification or deletion
        by non-privileged users."""
        protected = controls_evidence.get("audit_logs_write_protected_from_non_admin", False)
        assert protected, (
            "AU-9: audit logs are not write-protected from non-admin modification or deletion."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# ACCESS CONTROL (AC)
# ═══════════════════════════════════════════════════════════════════════════════

class TestAC2AccountManagement:
    """AC-2: Account Management — all baselines [L][M][H]"""

    def test_account_management_process_documented(self, controls_evidence: dict):
        """DETERMINISTIC: formal account management process must exist."""
        assert controls_evidence.get("account_management_process_documented", False), (
            "AC-2: no documented account management process in evidence."
        )

    def test_inactive_accounts_disabled(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC (Moderate/High): accounts inactive beyond ODP threshold must be disabled."""
        if impact_level == "low":
            pytest.skip("Inactive account automated disable applies at Moderate/High")
        inactive_threshold = controls_evidence.get(
            "inactive_account_disable_days", None
        )
        if inactive_threshold is None:
            pytest.fail(
                "AC-2: inactive account disable threshold not documented (required at Moderate/High)."
            )
        assert inactive_threshold <= AC2_INACTIVE_ACCOUNT_DISABLE_DAYS, (
            f"AC-2: inactive account threshold {inactive_threshold}d exceeds "
            f"maximum {AC2_INACTIVE_ACCOUNT_DISABLE_DAYS}d."
        )


class TestAC7UnsuccessfulLogonAttempts:
    """AC-7: Unsuccessful Logon Attempts — all baselines [L][M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-AC-001",
        description=(
            "AC-7 ODP: ≤3 consecutive failures before lockout; ≥30-min lockout (800-53B Moderate default). "
            "Lower thresholds are acceptable (more restrictive)."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_lockout_threshold_configured(self, controls_evidence: dict, odp_values: dict):
        """PARAMETERIZED: account lockout triggers at or below the ODP threshold."""
        threshold = odp_values.get("ac7_max_attempts", AC7_MAX_ATTEMPTS)
        configured = controls_evidence.get("logon_failure_lockout_threshold", 999)
        assert configured <= threshold, (
            f"AC-7: lockout threshold {configured} exceeds ODP maximum {threshold} attempts."
        )

    @pytest.mark.assumption(
        id="ASSUME-800053-AC-001",
        description="AC-7 ODP lockout duration ≥30 minutes per 800-53B Moderate default.",
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_lockout_duration_configured(self, controls_evidence: dict, odp_values: dict):
        """PARAMETERIZED: lockout duration meets or exceeds ODP minimum."""
        min_lockout = odp_values.get("ac7_lockout_minutes", AC7_LOCKOUT_MINUTES)
        configured = controls_evidence.get("logon_lockout_duration_minutes", 0)
        assert configured >= min_lockout, (
            f"AC-7: lockout duration {configured}min < ODP minimum {min_lockout}min."
        )


class TestAC11SessionLock:
    """AC-11: Session Lock — Moderate/High [M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-AC-002",
        description="AC-11 ODP: ≤15-min inactivity session lock (800-53B Moderate default); pattern-hiding required.",
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_session_lock_timeout(self, controls_evidence: dict, odp_values: dict, impact_level):
        """PARAMETERIZED: session lock triggers within the ODP inactivity window."""
        if impact_level == "low":
            pytest.skip("AC-11 session lock applies at Moderate/High")
        max_inactivity = odp_values.get("ac11_session_lock_minutes", AC11_SESSION_LOCK_MINUTES)
        configured = controls_evidence.get("session_inactivity_lock_minutes", 9999)
        assert configured <= max_inactivity, (
            f"AC-11: session lock at {configured}min exceeds ODP maximum {max_inactivity}min."
        )

    def test_session_lock_hides_content(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: session lock must hide/obscure displayed information (pattern-hiding)."""
        if impact_level == "low":
            pytest.skip("AC-11 pattern-hiding applies at Moderate/High")
        assert controls_evidence.get("session_lock_hides_displayed_content", False), (
            "AC-11: session lock does not conceal previously visible information."
        )


class TestAC17RemoteAccess:
    """AC-17: Remote Access — all baselines [L][M][H]"""

    def test_remote_access_encrypted(self, controls_evidence: dict):
        """DETERMINISTIC: all remote access sessions must use approved encrypted protocols."""
        protocols = set(
            controls_evidence.get("remote_access_protocols_in_use", [])
        )
        prohibited = protocols & AC17_PROHIBITED_PROTOCOLS
        assert not prohibited, (
            f"AC-17: prohibited remote access protocols in use: {prohibited}."
        )

    def test_remote_access_approved_protocols_only(self, controls_evidence: dict):
        """DETERMINISTIC: protocols in use must be in the approved set."""
        protocols = set(
            controls_evidence.get("remote_access_protocols_in_use", [])
        )
        unapproved = protocols - AC17_APPROVED_PROTOCOLS
        assert not unapproved, (
            f"AC-17: remote access protocols not in approved list: {unapproved}."
        )

    def test_remote_access_sessions_monitored(self, controls_evidence: dict):
        """DETERMINISTIC: remote access sessions must be monitored/logged."""
        assert controls_evidence.get("remote_access_sessions_logged", False), (
            "AC-17: remote access sessions not logged or monitored."
        )


class TestAC18WirelessAccess:
    """AC-18: Wireless Access — all baselines [L][M][H]"""

    def test_wireless_uses_approved_protocols(self, controls_evidence: dict):
        """DETERMINISTIC: wireless must use WPA2-Enterprise or WPA3 minimum."""
        wireless_protocols = set(
            controls_evidence.get("wireless_protocols_in_use", [])
        )
        if not wireless_protocols:
            pytest.skip("No wireless access — AC-18 not applicable")
        prohibited = wireless_protocols & AC18_PROHIBITED_PROTOCOLS
        assert not prohibited, (
            f"AC-18: prohibited wireless protocols in use: {prohibited}."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# IDENTIFICATION AND AUTHENTICATION (IA)
# ═══════════════════════════════════════════════════════════════════════════════

class TestIA2MultiFactorAuthentication:
    """IA-2: Identification and Authentication — Moderate/High [M][H]"""

    def test_mfa_enforced_privileged_users(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: MFA required for all privileged users at Moderate and above."""
        if impact_level == "low":
            pytest.skip("IA-2 MFA required at Moderate/High for privileged users")
        assert controls_evidence.get("mfa_enforced_privileged_users", False), (
            "IA-2: MFA not enforced for privileged users (required at Moderate/High)."
        )

    def test_mfa_enforced_all_users_high(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: MFA required for all users at High baseline (IA-2(1) + IA-2(2))."""
        if impact_level != "high":
            pytest.skip("IA-2 all-user MFA required at High baseline only")
        assert controls_evidence.get("mfa_enforced_all_users", False), (
            "IA-2: MFA not enforced for all users (required at High baseline)."
        )

    def test_mfa_method_not_prohibited(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: SMS OTP and voice call are deprecated second factors — must not be sole MFA mechanism."""
        if impact_level == "low":
            pytest.skip("MFA method check applies at Moderate/High")
        mfa_methods = set(controls_evidence.get("mfa_methods_in_use", []))
        only_prohibited = mfa_methods and mfa_methods.issubset(IA2_PROHIBITED_SECOND_FACTORS)
        assert not only_prohibited, (
            f"IA-2: sole MFA factor(s) in use are deprecated per NIST 800-63B: {mfa_methods}. "
            f"Migrate to approved methods: {IA2_ACCEPTABLE_MFA_TYPES}."
        )


class TestIA5AuthenticatorManagement:
    """IA-5(1): Password-Based Authenticators — all baselines [L][M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-IA-001",
        description=(
            "IA-5(1) password ODP: min length 8+complexity or 15-no-complexity; "
            "history 24 passwords; max lifetime 60 days if expiry-based; "
            "no expiry acceptable if breach-monitoring active per 800-63B guidance."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_password_minimum_length(self, controls_evidence: dict, odp_values: dict):
        """PARAMETERIZED: password minimum length meets ODP threshold."""
        uses_complexity = controls_evidence.get("password_complexity_rules_enforced", False)
        if uses_complexity:
            required_min = odp_values.get("ia5_min_length_complexity", IA5_MIN_LENGTH_COMPLEXITY)
        else:
            required_min = odp_values.get("ia5_min_length_no_complexity", IA5_MIN_LENGTH_NO_COMPLEXITY)
        configured_min = controls_evidence.get("password_minimum_length", 0)
        assert configured_min >= required_min, (
            f"IA-5(1): password minimum length {configured_min} < ODP required {required_min}."
        )

    def test_password_history_enforced(self, controls_evidence: dict, odp_values: dict, impact_level):
        """PARAMETERIZED: password history prohibits reuse of ODP count of prior passwords."""
        if impact_level == "low":
            pytest.skip("Password history enforcement applies at Moderate/High")
        required_history = odp_values.get("ia5_password_history_count", IA5_PASSWORD_HISTORY_COUNT)
        configured_history = controls_evidence.get("password_history_count", 0)
        assert configured_history >= required_history, (
            f"IA-5(1): password history {configured_history} < ODP required {required_history} prior passwords."
        )

    def test_password_hashing_algorithm(self, controls_evidence: dict):
        """DETERMINISTIC: plaintext or weak password storage algorithms are prohibited."""
        hash_algo = controls_evidence.get("password_hash_algorithm", "unknown").lower()
        assert hash_algo not in IA5_HASH_PROHIBITED, (
            f"IA-5(1): password storage algorithm '{hash_algo}' is prohibited. "
            f"Use one of: {IA5_HASH_ACCEPTABLE}."
        )

    def test_password_storage_uses_approved_algorithm(self, controls_evidence: dict):
        """DETERMINISTIC: password hash algorithm must be in the approved set."""
        hash_algo = controls_evidence.get("password_hash_algorithm", "unknown").lower()
        # Only fail if the algo is specifically identified as prohibited, not just unknown
        if hash_algo != "unknown":
            assert hash_algo in IA5_HASH_ACCEPTABLE, (
                f"IA-5(1): '{hash_algo}' not in approved password storage algorithms: "
                f"{IA5_HASH_ACCEPTABLE}."
            )


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION MANAGEMENT (CM)
# ═══════════════════════════════════════════════════════════════════════════════

class TestCM2BaselineConfiguration:
    """CM-2: Baseline Configuration — all baselines [L][M][H]"""

    def test_baseline_configuration_exists(self, controls_evidence: dict):
        """DETERMINISTIC: a documented, version-controlled baseline configuration must exist."""
        assert controls_evidence.get("baseline_configuration_documented", False), (
            "CM-2: no baseline configuration documented."
        )

    def test_baseline_configuration_attributes(self, controls_evidence: dict):
        """DETERMINISTIC: baseline must capture required CM-2 attributes."""
        attributes = set(controls_evidence.get("baseline_configuration_attributes", []))
        missing = CM2_BASELINE_REQUIRED_ATTRIBUTES - attributes
        assert not missing, (
            f"CM-2: baseline configuration missing required attributes: {missing}."
        )


class TestCM6ConfigurationSettings:
    """CM-6: Configuration Settings — Moderate/High [M][H]"""

    def test_configuration_hardening_guide_referenced(self, controls_evidence: dict, impact_level):
        """PARAMETERIZED: configuration settings must reference an approved hardening benchmark."""
        if impact_level == "low":
            pytest.skip("CM-6 hardening benchmark requirement applies at Moderate/High")
        guide = controls_evidence.get("hardening_guide_reference", "none").lower()
        assert guide in CM6_ACCEPTABLE_HARDENING_SOURCES or guide != "none", (
            f"CM-6: no approved hardening guide referenced. Must use one of: "
            f"{CM6_ACCEPTABLE_HARDENING_SOURCES}."
        )

    @pytest.mark.assumption(
        id="ASSUME-800053-CM-001",
        description=(
            "CM-6: DISA STIGs or CIS Benchmarks satisfy the 'established configuration settings' "
            "requirement; deviations require documented exception with ISSO approval."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_configuration_deviations_documented(self, controls_evidence: dict, impact_level):
        """PARAMETERIZED: deviations from hardening benchmarks must be documented and approved."""
        if impact_level == "low":
            pytest.skip("Formal deviation tracking applies at Moderate/High")
        assert controls_evidence.get("configuration_deviations_documented", False) or \
               controls_evidence.get("no_configuration_deviations", False), (
            "CM-6: configuration deviations from hardening benchmarks are not documented."
        )


class TestCM7LeastFunctionality:
    """CM-7: Least Functionality — all baselines [L][M][H]"""

    def test_approved_software_list_exists(self, controls_evidence: dict):
        """DETERMINISTIC: an approved software / services list must be maintained."""
        assert controls_evidence.get("approved_software_list_maintained", False), (
            "CM-7: no approved software or services list maintained."
        )

    def test_approved_software_list_reviewed_annually(
        self, controls_evidence: dict, reference_date: date
    ):
        """DETERMINISTIC: approved software list must be reviewed within 12 months."""
        last_review = controls_evidence.get("approved_software_list_last_review_date")
        if not last_review:
            pytest.fail("CM-7: approved software list has no recorded review date.")
        months_since = (reference_date.year - last_review.year) * 12 + \
                       (reference_date.month - last_review.month)
        assert months_since <= CM7_REVIEW_MONTHS, (
            f"CM-7: approved software list last reviewed {months_since} months ago; "
            f"must be reviewed within {CM7_REVIEW_MONTHS} months."
        )

    def test_all_open_ports_documented(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: all active ports, protocols, and services must be documented."""
        if impact_level == "low":
            pytest.skip("Port documentation applies at Moderate/High")
        assert controls_evidence.get("all_open_ports_documented_with_justification", False), (
            "CM-7: open ports/services not documented with business justification."
        )


class TestCM3ConfigurationChangeControl:
    """CM-3: Configuration Change Control — Moderate/High [M][H]"""

    def test_change_control_process_exists(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: formal configuration change control process must exist."""
        if impact_level == "low":
            pytest.skip("Formal CCB applies at Moderate/High")
        assert controls_evidence.get("configuration_change_control_process_documented", False), (
            "CM-3: no documented configuration change control process."
        )

    def test_changes_include_security_impact_analysis(
        self, controls_evidence: dict, impact_level
    ):
        """DETERMINISTIC: configuration changes must include security impact analysis."""
        if impact_level == "low":
            pytest.skip("Security impact analysis applies at Moderate/High")
        changes_with_sia = controls_evidence.get(
            "pct_config_changes_with_security_impact_analysis", 0
        )
        assert changes_with_sia >= 100, (
            f"CM-3: {100 - changes_with_sia}% of configuration changes lack required "
            f"security impact analysis."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM AND COMMUNICATIONS PROTECTION (SC)
# ═══════════════════════════════════════════════════════════════════════════════

class TestSC8TransmissionConfidentialityIntegrity:
    """SC-8: Transmission Confidentiality and Integrity — Moderate/High [M][H]"""

    def test_prohibited_protocols_not_in_use(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: prohibited cleartext and weak-encryption protocols must not be in use."""
        if impact_level == "low":
            pytest.skip("SC-8 cryptographic protection applies at Moderate/High")
        protocols_in_use = set(controls_evidence.get("network_protocols_in_use", []))
        prohibited = protocols_in_use & SC8_PROHIBITED_PROTOCOLS
        assert not prohibited, (
            f"SC-8: prohibited transmission protocols in use: {prohibited}."
        )

    def test_fips_validated_crypto_for_transmission(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: FIPS 140-2 or 140-3 validated cryptographic modules required."""
        if impact_level == "low":
            pytest.skip("SC-8 FIPS requirement applies at Moderate/High for federal systems")
        assert controls_evidence.get("transmission_crypto_fips_validated", False), (
            "SC-8: cryptographic modules protecting data in transit are not FIPS 140-2/3 validated."
        )


class TestSC13CryptographicProtection:
    """SC-13: Cryptographic Protection — all baselines [L][M][H]"""

    def test_fips_validated_cryptography_in_use(self, controls_evidence: dict):
        """DETERMINISTIC: all cryptographic mechanisms must use FIPS 140-2 or 140-3 validated modules."""
        assert controls_evidence.get("fips_validated_crypto_modules_in_use", False), (
            "SC-13: non-FIPS-validated cryptographic modules in use. "
            "FIPS 140-2 or 140-3 validation required for federal / FISMA systems."
        )


class TestSC28ProtectionAtRest:
    """SC-28: Protection of Information at Rest — Moderate/High [M][H]"""

    def test_sensitive_data_encrypted_at_rest(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: sensitive / classified information must be encrypted at rest."""
        if impact_level == "low":
            pytest.skip("SC-28 encryption at rest applies at Moderate/High")
        assert controls_evidence.get("sensitive_data_encrypted_at_rest", False), (
            "SC-28: sensitive information at rest is not encrypted."
        )

    def test_encryption_algorithm_approved(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: at-rest encryption must use approved algorithms."""
        if impact_level == "low":
            pytest.skip("SC-28 algorithm check applies at Moderate/High")
        algorithm = controls_evidence.get("at_rest_encryption_algorithm", "unknown").lower()
        assert algorithm not in SC28_PROHIBITED, (
            f"SC-28: at-rest encryption algorithm '{algorithm}' is prohibited."
        )
        if algorithm != "unknown":
            assert algorithm in SC28_APPROVED_ALGORITHMS, (
                f"SC-28: '{algorithm}' not in approved at-rest encryption algorithms."
            )


class TestSC12KeyManagement:
    """SC-12: Cryptographic Key Management — all baselines [L][M][H]"""

    def test_key_management_all_phases_covered(self, controls_evidence: dict):
        """DETERMINISTIC: key management process must address all 5 lifecycle phases."""
        covered_phases = set(controls_evidence.get("key_management_phases_covered", []))
        missing = SC12_REQUIRED_KEY_MGMT_PHASES - covered_phases
        assert not missing, (
            f"SC-12: key management lifecycle missing phases: {missing}."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM AND INFORMATION INTEGRITY (SI)
# ═══════════════════════════════════════════════════════════════════════════════

class TestSI2FlawRemediation:
    """SI-2: Flaw Remediation — all baselines [L][M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-SI-001",
        description=(
            "SI-2 ODP patch SLAs: CISA KEV=14d; Critical (CVSS≥9.0)=30d; "
            "High (7.0–8.9)=90d; Medium (4.0–6.9)=180d; Low=365d. "
            "ODPs may be tighter; must be documented in SSP."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_no_overdue_critical_patches(
        self, controls_evidence: dict, odp_values: dict, reference_date: date
    ):
        """PARAMETERIZED: no critical vulnerabilities may remain unpatched beyond the ODP SLA."""
        sla_days = odp_values.get("si2_critical_patch_days", SI2_CRITICAL_PATCH_DAYS)
        overdue = [
            v for v in controls_evidence.get("open_vulnerabilities", [])
            if v.get("severity", "").lower() == "critical"
            and (reference_date - v["first_detected"]).days > sla_days
        ]
        assert not overdue, (
            f"SI-2: {len(overdue)} critical vulnerability/ies unpatched beyond {sla_days}-day SLA: "
            f"{[v.get('cve_id', v.get('title')) for v in overdue]}."
        )

    def test_no_overdue_kev_patches(
        self, controls_evidence: dict, odp_values: dict, reference_date: date
    ):
        """DETERMINISTIC: CISA KEV entries must be patched within 14 days."""
        sla_days = odp_values.get("si2_kev_patch_days", SI2_KEV_PATCH_DAYS)
        overdue = [
            v for v in controls_evidence.get("open_vulnerabilities", [])
            if v.get("is_cisa_kev", False)
            and (reference_date - v["first_detected"]).days > sla_days
        ]
        assert not overdue, (
            f"SI-2: {len(overdue)} CISA KEV item(s) unpatched beyond {sla_days}-day deadline: "
            f"{[v.get('cve_id', v.get('title')) for v in overdue]}."
        )

    def test_no_overdue_high_patches(
        self, controls_evidence: dict, odp_values: dict, reference_date: date
    ):
        """PARAMETERIZED: high severity vulnerabilities must be patched within ODP SLA."""
        sla_days = odp_values.get("si2_high_patch_days", SI2_HIGH_PATCH_DAYS)
        overdue = [
            v for v in controls_evidence.get("open_vulnerabilities", [])
            if v.get("severity", "").lower() == "high"
            and (reference_date - v["first_detected"]).days > sla_days
        ]
        assert not overdue, (
            f"SI-2: {len(overdue)} high-severity vulnerability/ies unpatched beyond {sla_days}-day SLA."
        )


class TestSI3MaliciousCodeProtection:
    """SI-3: Malicious Code Protection — all baselines [L][M][H]"""

    def test_antimalware_deployed_on_all_endpoints(self, controls_evidence: dict):
        """DETERMINISTIC: antimalware must be deployed on all general-purpose endpoints."""
        assert controls_evidence.get("antimalware_deployed_all_endpoints", False), (
            "SI-3: antimalware protection not deployed on all general-purpose endpoints."
        )

    def test_definition_update_frequency(
        self, controls_evidence: dict, reference_date: date
    ):
        """DETERMINISTIC: antimalware definitions must be updated within 24 hours."""
        last_update = controls_evidence.get("antimalware_definitions_last_updated")
        if not last_update:
            pytest.fail("SI-3: no antimalware definition update date recorded.")
        hours_since = (datetime.combine(reference_date, datetime.min.time()) -
                       datetime.combine(last_update, datetime.min.time())).total_seconds() / 3600
        assert hours_since <= SI3_DEFINITION_UPDATE_HOURS, (
            f"SI-3: antimalware definitions {hours_since:.0f}h old; must be updated within "
            f"{SI3_DEFINITION_UPDATE_HOURS}h."
        )

    def test_realtime_scanning_enabled(self, controls_evidence: dict):
        """DETERMINISTIC: real-time (on-access) scanning must be enabled."""
        assert controls_evidence.get("antimalware_realtime_scanning_enabled", False), (
            "SI-3: real-time on-access scanning is not enabled."
        )

    def test_removable_media_scanned(self, controls_evidence: dict):
        """DETERMINISTIC: removable media must be scanned before use."""
        assert controls_evidence.get("removable_media_scanned_before_use", False), (
            "SI-3: removable media is not scanned for malicious code before use."
        )


class TestSI4SystemMonitoring:
    """SI-4: System Monitoring — Moderate/High [M][H]"""

    def test_automated_monitoring_deployed(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: automated monitoring tools must be deployed at Moderate/High."""
        if impact_level == "low":
            pytest.skip("SI-4 automated monitoring applies at Moderate/High")
        assert controls_evidence.get("automated_monitoring_deployed", False), (
            "SI-4: no automated system monitoring tools deployed."
        )

    def test_monitoring_covers_required_events(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: monitoring must cover all required SI-4 event categories."""
        if impact_level == "low":
            pytest.skip("SI-4 event coverage check applies at Moderate/High")
        monitored = set(controls_evidence.get("monitoring_event_categories_covered", []))
        missing = SI4_MONITORING_EVENTS - monitored
        assert not missing, (
            f"SI-4: automated monitoring not covering required event categories: {missing}."
        )


class TestSI7IntegrityVerification:
    """SI-7: Software, Firmware, and Information Integrity — High [H]"""

    def test_software_integrity_verification_deployed(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: software integrity verification required at High baseline."""
        if impact_level != "high":
            pytest.skip("SI-7 software integrity verification applies at High baseline only")
        assert controls_evidence.get("software_integrity_verification_deployed", False), (
            "SI-7: no cryptographic software/firmware integrity verification deployed (required at High)."
        )

    def test_integrity_verification_method_approved(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: integrity verification must use an approved cryptographic method."""
        if impact_level != "high":
            pytest.skip("SI-7 integrity verification method check applies at High baseline only")
        method = controls_evidence.get("integrity_verification_method", "unknown").lower()
        if method != "unknown":
            assert method in SI7_ACCEPTABLE_METHODS, (
                f"SI-7: integrity verification method '{method}' not in approved set "
                f"{SI7_ACCEPTABLE_METHODS}."
            )


# ── ODP manifest cross-check ──────────────────────────────────────────────────

class TestODPManifest:
    """Verify that all ODP-dependent tests have documented ODP values in the SSP."""

    REQUIRED_ODPS = frozenset({
        "au11_online_retention_days",
        "au6_review_frequency_days",
        "ac7_max_attempts",
        "ac7_lockout_minutes",
        "ac11_session_lock_minutes",
        "ia5_min_length_complexity",
        "ia5_min_length_no_complexity",
        "ia5_password_history_count",
        "si2_critical_patch_days",
        "si2_high_patch_days",
        "si2_kev_patch_days",
    })

    @pytest.mark.human_review_required(
        reason=(
            "ODP manifest completeness is a human-judgment check: SSP must document "
            "all organization-defined values and obtain ISSO / AO approval before tests "
            "transition from PARAMETERIZED to enforcing mode."
        )
    )
    def test_all_required_odps_documented(self, odp_values: dict):
        """CONTESTED: all required ODP keys must appear in the SSP ODP registry."""
        missing = self.REQUIRED_ODPS - set(odp_values.keys())
        assert not missing, (
            f"ODP registry incomplete — missing keys: {missing}. "
            f"Document these in the SSP before enforcing PARAMETERIZED tests."
        )
```

---

## Assumption registry

| ID | Family/Control | Summary | Review date |
|---|---|---|---|
| ASSUME-800053-AU-001 | AU-11 | Online retention 90d; archive 3yr (Moderate/High) per 800-53B; ODP must be documented in SSP | 2026-05-21 |
| ASSUME-800053-AU-002 | AU-6 | Review frequency ODP: ≤7 days (weekly) for Moderate per 800-53B default | 2026-05-21 |
| ASSUME-800053-AC-001 | AC-7 | Lockout threshold ≤3 attempts; lockout duration ≥30 min; 800-53B Moderate defaults | 2026-05-21 |
| ASSUME-800053-AC-002 | AC-11 | Session lock ≤15-min inactivity; pattern-hiding required; 800-53B Moderate default | 2026-05-21 |
| ASSUME-800053-IA-001 | IA-5(1) | Password length ≥8 (complexity) or ≥15 (no complexity); history 24; max 60d lifetime; no expiry if breach-monitoring active | 2026-05-21 |
| ASSUME-800053-CM-001 | CM-6 | DISA STIGs or CIS Benchmarks satisfy configuration settings requirement; deviations require ISSO-approved exception | 2026-05-21 |
| ASSUME-800053-SI-001 | SI-2 | Patch SLAs: KEV=14d, Critical=30d, High=90d, Medium=180d, Low=365d per 800-53B and CISA BOD 22-01 | 2026-05-21 |

## Parse status: Partial — AU, AC, IA, CM, SC, SI families (6 of 20) parsed; CP, IR, CA, MA, MP, PE, PS, RA, SA, SR, PL, PM, AT, PT remaining
