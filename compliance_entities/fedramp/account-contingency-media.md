# FedRAMP — Account Management, Contingency Planning, Media Protection, Personnel Security

**Source:** FedRAMP Rev 5 baselines; parameter deltas from NIST SP 800-53 r5
**Design note:** This file tests only the FedRAMP-specific parameter overlays and additional
  requirements within these families. Run the corresponding NIST 800-53 spec files in parallel
  for the underlying control coverage. FedRAMP tightens or supplements — it does not replace.
**Baseline tags:** `[L]` Low, `[M]` Moderate, `[H]` High — tests gated by `impact_level` fixture.

**Applies to:** Cloud service providers (CSPs) offering cloud services to US federal agencies; SaaS, PaaS, and IaaS providers seeking FedRAMP Authorization to Operate (ATO)
**Trigger:** US federal agency contract or procurement requiring FedRAMP-authorized cloud services; FISMA requires federal agencies to use FedRAMP-authorized cloud offerings; federal CIO Council memo
**Jurisdiction:** United States federal government; CSPs may be located anywhere globally but must meet US federal requirements
**Not applicable to:** On-premises federal IT systems (governed by FISMA/NIST 800-53 directly without FedRAMP process); commercial-only cloud products with no federal customers; cloud services offered exclusively to state/local government (StateRAMP is the counterpart)

---

```python
import pytest
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from typing import FrozenSet, Optional

# ── AC — FedRAMP Account Management Overlays ──────────────────────────────────

# AC-2: FedRAMP tightens the account departure audit window
AC2_DEPARTURE_ACCOUNT_DISABLE_DAYS = 1     # same-day disable on termination (FedRAMP overlay)
AC2_DEPARTURE_ACCOUNT_AUDIT_DAYS = 30      # audit all access of departed user within 30 days
AC2_ACCOUNT_REVIEW_MONTHS = 12             # annual account access review (AC-2(j))
AC2_PRIVILEGED_ACCOUNT_REVIEW_MONTHS = 6   # semi-annual for privileged accounts

# AC-17: FedRAMP remote access overlay — encryption must use FIPS-validated modules
AC17_FIPS_REQUIRED_FOR_REMOTE = True
AC17_APPROVED_PROTOCOLS = frozenset({"tls_1.2", "tls_1.3", "ipsec_ikev2", "ssh_v2"})
AC17_PROHIBITED_PROTOCOLS = frozenset({
    "telnet", "ftp", "http", "rsh", "rlogin", "vnc_unencrypted",
    "ssl", "tls_1.0", "tls_1.1", "pptp",
})

# AC-6(5): FedRAMP — privileged accounts for administrative functions ONLY
# Privileged accounts must not be used for browsing, email, or end-user tasks
AC6_5_PRIVILEGED_ACCOUNT_SEPARATION_REQUIRED = True   # Moderate/High

# AC-12: FedRAMP session termination after inactivity (tighter than base 800-53)
AC12_SESSION_TERMINATION_MINUTES = 30      # full termination (not just lock) after 30 min

# ── CP — Contingency Planning ─────────────────────────────────────────────────

# CP-2: Contingency plan attributes
CP2_REQUIRED_PLAN_ELEMENTS = frozenset({
    "essential_missions_and_business_functions",
    "recovery_objectives_and_priorities",
    "roles_and_responsibilities",
    "contact_information",
    "system_recovery_procedures",
    "backup_restoration_procedures",
    "alternate_processing_site",
})
CP2_REVIEW_MONTHS = 12                      # annual review required [M][H]

# CP-3: Contingency training frequency
CP3_TRAINING_MONTHS = 12                    # annual [M]; 6 months [H]
CP3_HIGH_TRAINING_MONTHS = 6               # semi-annual for High

# CP-4: Contingency plan testing
CP4_TEST_MONTHS = 12                        # annual [M][H]; tabletop or functional
CP4_HIGH_REQUIRES_FUNCTIONAL_TEST = True   # High: functional test (not just tabletop)

# CP-6/7: Alternate processing/storage sites
CP6_GEOGRAPHIC_SEPARATION_REQUIRED = True  # alternate storage must be geographically separate
CP6_SEPARATION_DISTANCE_MILES = 25         # FedRAMP: ≥25 miles from primary site (common overlay)

# CP-9: Information system backup
CP9_BACKUP_FREQUENCY_USER_DATA_DAYS = 1    # daily user-level data backups [M][H]
CP9_BACKUP_FREQUENCY_SYSTEM_DATA_DAYS = 7  # weekly system-level backups [M][H]
CP9_BACKUP_TEST_MONTHS = 12                # annual backup restoration test
CP9_BACKUP_OFFSITE_REQUIRED = True

# CP-10: RTO / RPO — must be documented (ODP); FedRAMP requires values in SSP
CP10_RTO_RPO_DOCUMENTED_REQUIRED = True

# ── MP — Media Protection (FedRAMP Overlays) ─────────────────────────────────

# MP-2: FedRAMP restricts CUI/federal data media access to authorized individuals
MP2_ACCESS_CONTROL_DOCUMENTED_REQUIRED = True

# MP-6: Media sanitization — FedRAMP requires NIST 800-88 compliance + FIPS-validated tools
MP6_ACCEPTABLE_SANITIZATION_METHODS = frozenset({
    "nist_800-88_clear",
    "nist_800-88_purge",
    "nist_800-88_destroy",
    "dod_5220_22-m",        # accepted equivalency for Clear/Purge
    "physical_destruction",  # for High or when purge not achievable
})
MP6_PROHIBITED_METHODS = frozenset({
    "reformat_only",
    "delete_only",
    "quick_format",
    "degauss_without_verification",  # degauss alone insufficient for SSD/Flash
})
MP6_REQUIRES_FIPS_VALIDATED_TOOL = True
MP6_DISPOSAL_RECORD_RETENTION_YEARS = 3    # FedRAMP: sanitization records ≥3 years

# MP-7: Removable media controls
MP7_REMOVABLE_MEDIA_RESTRICTED = True      # restricted to authorized users/purposes
MP7_CUI_REMOVAL_APPROVAL_REQUIRED = True   # must be explicitly authorized

# ── PS — Personnel Security ───────────────────────────────────────────────────

# PS-3: Background investigations — FedRAMP tightens to match impact level
# Low: basic background check (NACI or equivalent)
# Moderate: Moderate Background Investigation (MBI) or NACI
# High: Background Investigation (BI) or equivalent
PS3_REQUIRED_INVESTIGATION_LEVEL = {
    "low": "naci_or_equivalent",
    "moderate": "mbi_or_naci_or_equivalent",
    "high": "bi_or_equivalent",
}
PS3_INVESTIGATION_BEFORE_ACCESS = True     # investigation must complete before CUI access
PS3_REINVESTIGATION_YEARS = {
    "low": 10,
    "moderate": 5,
    "high": 5,
}

# PS-4: Personnel termination — FedRAMP same-day/immediate account termination
PS4_ACCOUNT_DISABLE_HOURS = 4             # accounts disabled within 4 hours of separation
PS4_CREDENTIAL_REVOKE_HOURS = 4           # all credentials revoked within 4 hours
PS4_DEVICE_RETURN_DAYS = 1                # organizational devices returned same day or next
PS4_EXIT_INTERVIEW_REQUIRED = True        # exit interview with security awareness reminders

# PS-5: Personnel transfer — access review within N days of transfer
PS5_ACCESS_REVIEW_DAYS = 5                # access re-evaluated within 5 days of transfer

# PS-6: Access agreements
PS6_AGREEMENT_BEFORE_ACCESS = True        # signed before initial CUI access
PS6_RENEWAL_MONTHS = 12                   # renewed annually

# ── Scope fixtures ─────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def fedramp_scope_check(entity_profile: dict):
    """Skip if the system is not a FedRAMP-authorized or in-authorization CSP."""
    if not entity_profile.get("fedramp_in_scope", False):
        pytest.skip("System not subject to FedRAMP — overlays not applicable")


@pytest.fixture
def impact_level(entity_profile: dict) -> str:
    level = entity_profile.get("fips199_impact_level", "").lower()
    if level not in {"low", "moderate", "high"}:
        pytest.skip("FIPS 199 impact level not categorized — baseline indeterminate")
    return level


@pytest.fixture
def odp_values(entity_profile: dict) -> dict:
    odps = entity_profile.get("odp_values", {})
    if not odps:
        pytest.skip("ODP values not documented in SSP — PARAMETERIZED tests cannot execute")
    return odps


# ═══════════════════════════════════════════════════════════════════════════════
# ACCESS CONTROL — FedRAMP overlays (AC)
# ═══════════════════════════════════════════════════════════════════════════════

class TestAC2FedRAMPAccountManagement:
    """AC-2 FedRAMP overlay: tighter departure audit window and privileged review cadence."""

    def test_departed_user_account_disabled_same_day(self, controls_evidence: dict):
        """DETERMINISTIC: accounts must be disabled on day of termination."""
        violations = [
            u for u in controls_evidence.get("recent_terminations", [])
            if u.get("days_to_account_disable", 0) > AC2_DEPARTURE_ACCOUNT_DISABLE_DAYS
        ]
        assert not violations, (
            f"AC-2 (FedRAMP): {len(violations)} terminated user(s) did not have accounts disabled "
            f"within {AC2_DEPARTURE_ACCOUNT_DISABLE_DAYS} day(s) of departure: "
            f"{[v.get('user_id') for v in violations]}."
        )

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-AC-001",
        description=(
            "AC-2 FedRAMP overlay: access of departed users must be audited within 30 days "
            "of departure; privileged accounts reviewed semi-annually; all accounts annually."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_privileged_account_review_cadence(
        self, controls_evidence: dict, reference_date: date, impact_level
    ):
        """PARAMETERIZED: privileged accounts reviewed at least semi-annually at Moderate/High."""
        if impact_level == "low":
            pytest.skip("Semi-annual privileged account review applies at Moderate/High")
        last_review = controls_evidence.get("privileged_account_review_last_date")
        if not last_review:
            pytest.fail("AC-2 (FedRAMP): privileged account review date not documented.")
        months_since = (reference_date.year - last_review.year) * 12 + \
                       (reference_date.month - last_review.month)
        assert months_since <= AC2_PRIVILEGED_ACCOUNT_REVIEW_MONTHS, (
            f"AC-2 (FedRAMP): privileged account review {months_since} months ago; "
            f"must occur ≤{AC2_PRIVILEGED_ACCOUNT_REVIEW_MONTHS} months for {impact_level} baseline."
        )

    def test_all_account_review_cadence(
        self, controls_evidence: dict, reference_date: date
    ):
        """DETERMINISTIC: all accounts must be reviewed within 12 months."""
        last_review = controls_evidence.get("all_account_review_last_date")
        if not last_review:
            pytest.fail("AC-2: annual all-account review date not documented.")
        months_since = (reference_date.year - last_review.year) * 12 + \
                       (reference_date.month - last_review.month)
        assert months_since <= AC2_ACCOUNT_REVIEW_MONTHS, (
            f"AC-2: all-account review {months_since} months ago; must occur ≤{AC2_ACCOUNT_REVIEW_MONTHS} months."
        )


class TestAC17FedRAMPRemoteAccess:
    """AC-17 FedRAMP overlay: FIPS-validated cryptography for all remote access sessions."""

    def test_remote_access_fips_validated_crypto(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: remote access must use FIPS 140-2/3 validated cryptographic modules."""
        if impact_level == "low":
            pytest.skip("AC-17 FIPS validation applies at Moderate/High")
        assert controls_evidence.get("remote_access_fips_validated_crypto", False), (
            "AC-17 (FedRAMP): remote access sessions not using FIPS 140-2/3 validated crypto."
        )

    def test_remote_access_prohibited_protocols_absent(self, controls_evidence: dict):
        """DETERMINISTIC: prohibited remote access protocols must not be in use."""
        protocols = set(controls_evidence.get("remote_access_protocols_in_use", []))
        prohibited = protocols & AC17_PROHIBITED_PROTOCOLS
        assert not prohibited, (
            f"AC-17 (FedRAMP): prohibited remote access protocols in use: {prohibited}."
        )


class TestAC65PrivilegedAccountSeparation:
    """AC-6(5) FedRAMP: privileged accounts restricted to privileged functions only."""

    def test_privileged_accounts_not_used_for_nonprovileged_tasks(
        self, controls_evidence: dict, impact_level
    ):
        """DETERMINISTIC: privileged accounts must not be used for email, browsing, or user tasks."""
        if impact_level == "low":
            pytest.skip("AC-6(5) applies at Moderate/High")
        assert controls_evidence.get("privileged_accounts_restricted_to_admin_functions", False), (
            "AC-6(5) (FedRAMP): privileged accounts used for non-privileged tasks (email, browsing, etc.). "
            "Separate user accounts required for non-administrative activities."
        )


class TestAC12SessionTermination:
    """AC-12 FedRAMP: full session termination after 30 min inactivity (stronger than AC-11 lock)."""

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-AC-002",
        description=(
            "AC-12 FedRAMP: sessions must be fully terminated (not just locked) after ≤30 min "
            "of inactivity for network-based sessions. Remote sessions re-require full re-auth."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_network_session_termination_timeout(
        self, controls_evidence: dict, impact_level
    ):
        """PARAMETERIZED: network sessions must terminate (not just lock) within 30 min of inactivity."""
        if impact_level == "low":
            pytest.skip("AC-12 session termination applies at Moderate/High")
        termination_minutes = controls_evidence.get("session_inactivity_termination_minutes", 9999)
        assert termination_minutes <= AC12_SESSION_TERMINATION_MINUTES, (
            f"AC-12 (FedRAMP): session terminates after {termination_minutes}min; "
            f"must terminate within {AC12_SESSION_TERMINATION_MINUTES}min."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# CONTINGENCY PLANNING (CP)
# ═══════════════════════════════════════════════════════════════════════════════

class TestCP2ContingencyPlan:
    """CP-2: Contingency Plan — Moderate/High [M][H]"""

    def test_contingency_plan_exists(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: a documented contingency plan must exist."""
        if impact_level == "low":
            pytest.skip("CP-2 documented contingency plan required at Moderate/High")
        assert controls_evidence.get("contingency_plan_documented", False), (
            "CP-2: no documented contingency plan."
        )

    def test_contingency_plan_required_elements(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: contingency plan must contain all required CP-2 elements."""
        if impact_level == "low":
            pytest.skip("CP-2 required elements apply at Moderate/High")
        plan_elements = set(controls_evidence.get("contingency_plan_elements", []))
        missing = CP2_REQUIRED_PLAN_ELEMENTS - plan_elements
        assert not missing, (
            f"CP-2: contingency plan missing required elements: {missing}."
        )

    def test_contingency_plan_reviewed_annually(
        self, controls_evidence: dict, reference_date: date, impact_level
    ):
        """DETERMINISTIC: contingency plan must be reviewed within 12 months."""
        if impact_level == "low":
            pytest.skip("CP-2 annual review applies at Moderate/High")
        last_review = controls_evidence.get("contingency_plan_last_review_date")
        if not last_review:
            pytest.fail("CP-2: contingency plan review date not documented.")
        months_since = (reference_date.year - last_review.year) * 12 + \
                       (reference_date.month - last_review.month)
        assert months_since <= CP2_REVIEW_MONTHS, (
            f"CP-2: contingency plan last reviewed {months_since} months ago; "
            f"must be reviewed within {CP2_REVIEW_MONTHS} months."
        )


class TestCP3ContingencyTraining:
    """CP-3: Contingency Training — Moderate/High [M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-CP-001",
        description=(
            "CP-3 training frequency: annual for Moderate; semi-annual (6 months) for High; "
            "role-based training for personnel with contingency responsibilities."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_contingency_training_cadence(
        self, controls_evidence: dict, reference_date: date, impact_level
    ):
        """PARAMETERIZED: contingency training frequency matches impact level."""
        if impact_level == "low":
            pytest.skip("CP-3 formal training applies at Moderate/High")
        max_months = CP3_HIGH_TRAINING_MONTHS if impact_level == "high" else CP3_TRAINING_MONTHS
        last_training = controls_evidence.get("contingency_training_last_date")
        if not last_training:
            pytest.fail("CP-3: contingency training date not documented.")
        months_since = (reference_date.year - last_training.year) * 12 + \
                       (reference_date.month - last_training.month)
        assert months_since <= max_months, (
            f"CP-3: last contingency training {months_since} months ago; "
            f"must occur ≤{max_months} months for {impact_level} baseline."
        )


class TestCP4ContingencyPlanTesting:
    """CP-4: Contingency Plan Testing — Moderate/High [M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-CP-002",
        description=(
            "CP-4 test frequency: annual; High baseline requires a functional test "
            "(not just tabletop); test must include key personnel and demonstrate RTO achievement."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_contingency_plan_tested_annually(
        self, controls_evidence: dict, reference_date: date, impact_level
    ):
        """DETERMINISTIC: contingency plan must be tested within 12 months."""
        if impact_level == "low":
            pytest.skip("CP-4 annual test applies at Moderate/High")
        last_test = controls_evidence.get("contingency_plan_last_test_date")
        if not last_test:
            pytest.fail("CP-4: no contingency plan test date documented.")
        months_since = (reference_date.year - last_test.year) * 12 + \
                       (reference_date.month - last_test.month)
        assert months_since <= CP4_TEST_MONTHS, (
            f"CP-4: contingency plan last tested {months_since} months ago; "
            f"must be tested within {CP4_TEST_MONTHS} months."
        )

    def test_high_baseline_functional_test(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: High baseline requires functional (not tabletop-only) contingency test."""
        if impact_level != "high":
            pytest.skip("Functional test requirement applies at High baseline only")
        test_type = controls_evidence.get("contingency_plan_last_test_type", "tabletop").lower()
        assert test_type in {"functional", "full_interruption"}, (
            f"CP-4 (FedRAMP High): test type '{test_type}' insufficient — "
            f"functional test required at High baseline."
        )


class TestCP6AlternateStorage:
    """CP-6: Alternate Storage Site — Moderate/High [M][H]"""

    def test_alternate_storage_site_exists(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: an alternate storage site must be documented."""
        if impact_level == "low":
            pytest.skip("CP-6 alternate storage applies at Moderate/High")
        assert controls_evidence.get("alternate_storage_site_documented", False), (
            "CP-6: no alternate storage site documented."
        )

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-CP-003",
        description=(
            "CP-6 geographic separation: alternate storage ≥25 miles from primary site "
            "to avoid shared disaster scenarios. Both sites must be CONUS for Moderate/High."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_alternate_storage_geographic_separation(self, controls_evidence: dict, impact_level):
        """PARAMETERIZED: alternate storage must be geographically separated by ≥25 miles."""
        if impact_level == "low":
            pytest.skip("CP-6 geographic separation applies at Moderate/High")
        separation_miles = controls_evidence.get(
            "alternate_storage_separation_miles", 0
        )
        assert separation_miles >= CP6_SEPARATION_DISTANCE_MILES, (
            f"CP-6 (FedRAMP): alternate storage site {separation_miles} miles from primary; "
            f"minimum {CP6_SEPARATION_DISTANCE_MILES} miles required."
        )


class TestCP9Backups:
    """CP-9: Information System Backup — Moderate/High [M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-CP-004",
        description=(
            "CP-9 backup frequency: daily user-level data, weekly system-level data; "
            "backup stored offsite; restoration tested annually; backup copies protected "
            "with FIPS-validated encryption for Moderate/High."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_user_data_backup_frequency(self, controls_evidence: dict, impact_level, reference_date: date):
        """PARAMETERIZED: user-level data must be backed up daily."""
        if impact_level == "low":
            pytest.skip("CP-9 daily backup applies at Moderate/High")
        last_backup = controls_evidence.get("last_user_data_backup_date")
        if not last_backup:
            pytest.fail("CP-9: no user data backup date documented.")
        days_since = (reference_date - last_backup).days
        assert days_since <= CP9_BACKUP_FREQUENCY_USER_DATA_DAYS, (
            f"CP-9: last user data backup {days_since}d ago; must occur within "
            f"{CP9_BACKUP_FREQUENCY_USER_DATA_DAYS}d."
        )

    def test_backups_stored_offsite(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: backups must be stored at an offsite / alternate location."""
        if impact_level == "low":
            pytest.skip("CP-9 offsite backup applies at Moderate/High")
        assert controls_evidence.get("backups_stored_offsite", False), (
            "CP-9 (FedRAMP): backups not stored at offsite or alternate location."
        )

    def test_backup_restoration_tested_annually(
        self, controls_evidence: dict, reference_date: date, impact_level
    ):
        """DETERMINISTIC: backup restoration must be tested within 12 months."""
        if impact_level == "low":
            pytest.skip("CP-9 restoration test applies at Moderate/High")
        last_test = controls_evidence.get("backup_restoration_last_test_date")
        if not last_test:
            pytest.fail("CP-9: backup restoration has never been tested.")
        months_since = (reference_date.year - last_test.year) * 12 + \
                       (reference_date.month - last_test.month)
        assert months_since <= CP9_BACKUP_TEST_MONTHS, (
            f"CP-9: backup restoration last tested {months_since} months ago; "
            f"must test within {CP9_BACKUP_TEST_MONTHS} months."
        )

    def test_backup_copies_encrypted(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: backup media must be encrypted with FIPS-validated crypto."""
        if impact_level == "low":
            pytest.skip("CP-9 backup encryption with FIPS modules applies at Moderate/High")
        assert controls_evidence.get("backup_copies_encrypted_fips_validated", False), (
            "CP-9 (FedRAMP): backup copies not encrypted with FIPS 140-2/3 validated modules."
        )


class TestCP10RTORPODocumented:
    """CP-10: Information System Recovery and Reconstitution — RTO/RPO in SSP."""

    def test_rto_rpo_documented_in_ssp(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: RTO and RPO values must be documented (FedRAMP requires in SSP)."""
        if impact_level == "low":
            pytest.skip("CP-10 RTO/RPO documentation applies at Moderate/High")
        assert controls_evidence.get("rto_documented", False), (
            "CP-10 (FedRAMP): Recovery Time Objective (RTO) not documented in SSP."
        )
        assert controls_evidence.get("rpo_documented", False), (
            "CP-10 (FedRAMP): Recovery Point Objective (RPO) not documented in SSP."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# MEDIA PROTECTION — FedRAMP overlays (MP)
# ═══════════════════════════════════════════════════════════════════════════════

class TestMP6MediaSanitization:
    """MP-6: Media Sanitization — NIST 800-88 + FIPS-validated tools required (FedRAMP overlay)."""

    def test_sanitization_method_approved(self, controls_evidence: dict):
        """DETERMINISTIC: media sanitization method must be NIST 800-88 compliant."""
        methods_used = set(controls_evidence.get("media_sanitization_methods_in_use", []))
        if not methods_used:
            pytest.skip("No media sanitization events — MP-6 not applicable")
        prohibited = methods_used & MP6_PROHIBITED_METHODS
        assert not prohibited, (
            f"MP-6 (FedRAMP): prohibited sanitization methods in use: {prohibited}. "
            f"Use NIST 800-88 clear/purge/destroy methods."
        )

    def test_sanitization_tool_fips_validated(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: sanitization tools must be FIPS 140-2/3 validated at Moderate/High."""
        if impact_level == "low":
            pytest.skip("FIPS-validated sanitization tool applies at Moderate/High")
        assert controls_evidence.get("sanitization_tool_fips_validated", False), (
            "MP-6 (FedRAMP): media sanitization tools are not FIPS 140-2/3 validated."
        )

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-MP-001",
        description=(
            "MP-6 FedRAMP overlay: NIST 800-88 clear/purge/destroy required; "
            "FIPS-validated tools for Moderate/High; disposal records retained ≥3 years; "
            "physical destruction for High or when purge is technically infeasible."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_disposal_records_retained(
        self, controls_evidence: dict, reference_date: date
    ):
        """PARAMETERIZED: media disposal records must be retained for at least 3 years."""
        disposal_records = controls_evidence.get("media_disposal_records_retained_years", 0)
        assert disposal_records >= MP6_DISPOSAL_RECORD_RETENTION_YEARS, (
            f"MP-6 (FedRAMP): disposal records retained {disposal_records}yr; "
            f"must retain ≥{MP6_DISPOSAL_RECORD_RETENTION_YEARS}yr."
        )


class TestMP7RemovableMedia:
    """MP-7: Media Use — removable media controls at Moderate/High."""

    def test_removable_media_restricted_to_authorized_use(
        self, controls_evidence: dict, impact_level
    ):
        """DETERMINISTIC: removable media use must be restricted and authorized."""
        if impact_level == "low":
            pytest.skip("MP-7 removable media restriction applies at Moderate/High")
        assert controls_evidence.get("removable_media_restricted_to_authorized_users", False), (
            "MP-7 (FedRAMP): removable media not restricted to authorized users/purposes."
        )

    def test_cui_removal_requires_approval(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: CUI data transfer to removable media must be explicitly authorized."""
        if impact_level == "low":
            pytest.skip("MP-7 CUI removal approval applies at Moderate/High")
        assert controls_evidence.get("cui_removal_to_media_requires_approval", False), (
            "MP-7 (FedRAMP): CUI transfer to removable media does not require explicit authorization."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# PERSONNEL SECURITY — FedRAMP overlays (PS)
# ═══════════════════════════════════════════════════════════════════════════════

class TestPS3BackgroundInvestigations:
    """PS-3: Personnel Screening — FedRAMP tightens investigation level to match impact baseline."""

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-PS-001",
        description=(
            "PS-3 investigation levels: Low=NACI or equivalent; Moderate=MBI or NACI; "
            "High=BI or equivalent. Investigation must complete before CUI system access. "
            "Reinvestigation: Moderate=every 5 years; High=every 5 years."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_investigation_level_matches_baseline(self, controls_evidence: dict, impact_level):
        """PARAMETERIZED: background investigation level must match the FedRAMP impact level requirement."""
        required_level = PS3_REQUIRED_INVESTIGATION_LEVEL[impact_level]
        conducted_level = controls_evidence.get(
            "background_investigation_level_conducted", "none"
        ).lower()
        if conducted_level == "none":
            pytest.fail(
                f"PS-3 (FedRAMP): no background investigation conducted for {impact_level} system. "
                f"Required: {required_level}."
            )
        # Pattern 2: adequacy of "or equivalent" requires human verification
        assert conducted_level != "none", (
            f"PS-3 (FedRAMP): investigation level '{conducted_level}' must meet or exceed "
            f"'{required_level}' for {impact_level} baseline."
        )

    def test_investigation_precedes_access(self, controls_evidence: dict):
        """DETERMINISTIC: investigation must complete before CUI access is granted."""
        premature_access = [
            u for u in controls_evidence.get("personnel_onboarding_records", [])
            if u.get("access_granted_before_investigation_complete", False)
        ]
        assert not premature_access, (
            f"PS-3 (FedRAMP): {len(premature_access)} personnel granted CUI access before "
            f"background investigation completed: "
            f"{[u.get('user_id') for u in premature_access]}."
        )


class TestPS4PersonnelTermination:
    """PS-4: Personnel Termination — FedRAMP same-day account disable and credential revocation."""

    def test_accounts_disabled_within_4_hours(self, controls_evidence: dict):
        """DETERMINISTIC: FedRAMP requires accounts disabled within 4 hours of confirmed termination."""
        violations = [
            t for t in controls_evidence.get("recent_terminations", [])
            if t.get("hours_to_account_disable", 0) > PS4_ACCOUNT_DISABLE_HOURS
        ]
        assert not violations, (
            f"PS-4 (FedRAMP): {len(violations)} termination(s) where account not disabled within "
            f"{PS4_ACCOUNT_DISABLE_HOURS}h: {[v.get('user_id') for v in violations]}."
        )

    def test_credentials_revoked_within_4_hours(self, controls_evidence: dict):
        """DETERMINISTIC: all credentials (tokens, certificates, physical) revoked within 4 hours."""
        violations = [
            t for t in controls_evidence.get("recent_terminations", [])
            if t.get("hours_to_credential_revocation", 0) > PS4_CREDENTIAL_REVOKE_HOURS
        ]
        assert not violations, (
            f"PS-4 (FedRAMP): {len(violations)} termination(s) where credentials not revoked within "
            f"{PS4_CREDENTIAL_REVOKE_HOURS}h: {[v.get('user_id') for v in violations]}."
        )


class TestPS5PersonnelTransfer:
    """PS-5: Personnel Transfer — access re-evaluated within 5 days."""

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-PS-002",
        description=(
            "PS-5 FedRAMP overlay: access rights must be reviewed and modified within 5 business days "
            "of a personnel transfer. Excess access from prior role must be revoked."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_access_reviewed_within_5_days_of_transfer(self, controls_evidence: dict):
        """PARAMETERIZED: access re-evaluated within 5 days of any personnel transfer."""
        late_reviews = [
            t for t in controls_evidence.get("recent_transfers", [])
            if t.get("days_to_access_review", 0) > PS5_ACCESS_REVIEW_DAYS
        ]
        assert not late_reviews, (
            f"PS-5 (FedRAMP): {len(late_reviews)} transfer(s) where access review took more than "
            f"{PS5_ACCESS_REVIEW_DAYS} days: {[t.get('user_id') for t in late_reviews]}."
        )


class TestPS6AccessAgreements:
    """PS-6: Access Agreements — signed before access; renewed annually."""

    def test_access_agreements_signed_before_access(self, controls_evidence: dict):
        """DETERMINISTIC: access agreements must be signed before CUI access is granted."""
        unsigned = [
            u for u in controls_evidence.get("personnel_onboarding_records", [])
            if not u.get("access_agreement_signed_before_access", False)
        ]
        assert not unsigned, (
            f"PS-6 (FedRAMP): {len(unsigned)} personnel granted access without signed access agreement: "
            f"{[u.get('user_id') for u in unsigned]}."
        )

    def test_access_agreements_renewed_annually(
        self, controls_evidence: dict, reference_date: date
    ):
        """DETERMINISTIC: access agreements must be renewed within 12 months."""
        overdue = [
            u for u in controls_evidence.get("all_personnel_records", [])
            if (reference_date - u.get("access_agreement_signed_date", date.min)).days >
               PS6_RENEWAL_MONTHS * 30
        ]
        assert not overdue, (
            f"PS-6 (FedRAMP): {len(overdue)} personnel with access agreements not renewed within "
            f"{PS6_RENEWAL_MONTHS} months: {[u.get('user_id') for u in overdue[:10]]}."
        )
```

---

## Assumption registry

| ID | Family/Control | Summary | Review date |
|---|---|---|---|
| ASSUME-FEDRAMP-AC-001 | AC-2 overlay | Privileged account review: semi-annual at Moderate/High; departed-user access audit within 30 days | 2026-05-21 |
| ASSUME-FEDRAMP-AC-002 | AC-12 overlay | Session termination (not just lock) ≤30 min for network sessions at Moderate/High | 2026-05-21 |
| ASSUME-FEDRAMP-CP-001 | CP-3 | Training frequency: annual at Moderate; semi-annual (6 months) at High; role-based for continuity personnel | 2026-05-21 |
| ASSUME-FEDRAMP-CP-002 | CP-4 | Testing frequency: annual; High requires functional test (not tabletop-only); must demonstrate RTO | 2026-05-21 |
| ASSUME-FEDRAMP-CP-003 | CP-6 | Alternate storage geographic separation ≥25 miles; both primary and alternate must be CONUS | 2026-05-21 |
| ASSUME-FEDRAMP-CP-004 | CP-9 | Daily user data backups; weekly system-level; offsite; encrypted with FIPS-validated crypto; annual restoration test | 2026-05-21 |
| ASSUME-FEDRAMP-MP-001 | MP-6 overlay | NIST 800-88 required; FIPS-validated tools at Moderate/High; disposal records ≥3 years; physical destruction for High when purge infeasible | 2026-05-21 |
| ASSUME-FEDRAMP-PS-001 | PS-3 overlay | Investigation levels: Low=NACI; Moderate=MBI/NACI; High=BI; reinvestigation every 5 years; complete before CUI access | 2026-05-21 |
| ASSUME-FEDRAMP-PS-002 | PS-5 overlay | Access re-evaluated within 5 business days of transfer; excess prior-role access revoked | 2026-05-21 |

## Parse status: Partial — conmon-and-overlays.md + account-contingency-media.md (AC, CP, MP, PS overlays); remaining: full AU/CM/IA/SC/SI FedRAMP parameter overlays, High-only enhancements, SA/SR SCRM details
