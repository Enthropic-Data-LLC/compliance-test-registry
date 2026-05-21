# NIST SP 800-53 r5 — Maintenance, Media Protection, Physical/Environmental Protection, Personnel Security

**Source:** NIST SP 800-53 Rev 5 + 800-53B baselines
**Coverage:** MA (6 base), MP (8 base), PE (20 base), PS (9 base)
**Baseline tags:** `[L]` Low, `[M]` Moderate, `[H]` High

**Applies to:** US federal agencies and their information systems (mandatory under FISMA); federal contractors and cloud service providers seeking FedRAMP authorization; state and local governments and critical infrastructure (by voluntary adoption or contract)
**Trigger:** Federal Information Security Modernization Act (FISMA) — mandatory for all federal agencies; FedRAMP authorization process; federal contract or grant requirement citing NIST 800-53; OMB Circular A-130
**Jurisdiction:** United States federal government (mandatory); widely adopted internationally as a comprehensive control framework
**Not applicable to:** Private sector organizations not under federal contract (unless voluntarily adopted); non-federal systems outside FISMA scope; CMMC Level 1/2 contractors (use NIST 800-171, which is derived from 800-53 but has 110 requirements vs. 1000+)

---

```python
import pytest
from datetime import date, timedelta
from typing import FrozenSet

# ── MA — Maintenance ──────────────────────────────────────────────────────────

# MA-2: Controlled maintenance — scheduled and documented
MA2_MAINTENANCE_RECORD_REQUIRED = True

# MA-3: Maintenance tools — must be authorized
MA3_TOOL_APPROVAL_REQUIRED = True

# MA-4: Nonlocal (remote) maintenance — FIPS-validated crypto + MFA + session logging
MA4_FIPS_CRYPTO_REQUIRED = True
MA4_MFA_REQUIRED = True                 # Moderate/High
MA4_SESSION_LOGGING_REQUIRED = True
MA4_APPROVED_PROTOCOLS = frozenset({"ssh_v2", "tls_1.2", "tls_1.3", "ipsec_ikev2"})
MA4_PROHIBITED_PROTOCOLS = frozenset({"telnet", "http", "ftp", "rsh", "vnc_unencrypted"})

# MA-5: Maintenance personnel — cleared or escorted
MA5_ESCORT_REQUIRED_UNCLEARED = True    # uncleared personnel must be escorted during maintenance

# MA-6: Timely maintenance — ODP-defined availability requirement
MA6_CRITICAL_SPARE_PARTS_DOCUMENTED = True  # Moderate/High

# ── MP — Media Protection ─────────────────────────────────────────────────────

# MP-2: Media access
MP2_ACCESS_CONTROL_DOCUMENTED = True

# MP-3: Media marking — CUI/classification marking
MP3_MARKING_REQUIRED = True
MP3_EXEMPT_FROM_MARKING: FrozenSet[str] = frozenset({
    "mass_produced_commercial_off_the_shelf",
    "non_removable_internal_media_in_controlled_environment",
})

# MP-5: Media transport
MP5_TRANSPORT_ENCRYPTION_REQUIRED = True   # Moderate/High — FIPS-validated crypto
MP5_COURIER_AUTHORIZATION_REQUIRED = True  # designated courier or tracked shipping

# MP-6: Media sanitization — NIST 800-88
MP6_ACCEPTABLE_METHODS = frozenset({
    "nist_800-88_clear", "nist_800-88_purge", "nist_800-88_destroy",
    "dod_5220_22-m", "physical_destruction",
})
MP6_PROHIBITED_METHODS = frozenset({
    "delete_only", "reformat_only", "quick_format",
    "degauss_flash_media",              # degaussing ineffective for SSD/Flash
})
MP6_DISPOSAL_LOG_REQUIRED = True
MP6_LOG_RETENTION_YEARS = 3

# MP-7: Media use — restrict removable media at Moderate/High
MP7_REMOVABLE_MEDIA_RESTRICTED = True
MP7_EXCEPTIONS_REQUIRE_APPROVAL = True

# ── PE — Physical and Environmental Protection ────────────────────────────────

# PE-2: Physical access authorizations
PE2_ACCESS_LIST_MAINTAINED = True
PE2_ACCESS_LIST_REVIEW_MONTHS = 12      # annual review [M]; 6 months [H]
PE2_HIGH_REVIEW_MONTHS = 6

# PE-3: Physical access control — locks, badge readers, guards
PE3_PHYSICAL_ACCESS_CONTROLS_REQUIRED = True
PE3_ENTRY_EXIT_AUDIT_REQUIRED = True    # Moderate/High

# PE-6: Monitoring physical access
PE6_MONITORING_IN_PLACE = True         # Moderate/High
PE6_INTRUSION_ALARMS_DOCUMENTED = True

# PE-8: Visitor access records
PE8_VISITOR_LOG_REQUIRED = True
PE8_LOG_RETENTION_YEARS = 2            # 800-53B default [M][H]; many orgs use 3yr

# PE-13/14/15: Environmental controls
PE13_FIRE_SUPPRESSION_DOCUMENTED = True  # fire detection + suppression
PE14_HVAC_DOCUMENTED = True              # temperature/humidity controls
PE15_WATER_DAMAGE_DOCUMENTED = True      # water damage protection (shutoff valves)

# PE-17: Alternate work site — Moderate/High
PE17_ALT_WORKSITE_CONTROLS_DOCUMENTED = True

# ── PS — Personnel Security ────────────────────────────────────────────────────

# PS-2: Position risk designation
PS2_RISK_DESIGNATION_REQUIRED = True   # all positions with system access
PS2_REVIEW_MONTHS = 36                 # every 3 years or when responsibilities change

# PS-3: Personnel screening — commensurate with position risk
PS3_SCREENING_REQUIRED_BEFORE_ACCESS = True
PS3_RESCREENING_HIGH_RISK_YEARS = 5

# PS-4: Personnel termination — same-day/immediate
PS4_ACCOUNT_DISABLE_HOURS = 8          # ODP: 800-53B suggests same-day; often ≤8h
PS4_CREDENTIAL_REVOKE_HOURS = 8

# PS-5: Personnel transfer — access re-evaluated
PS5_ACCESS_REVIEW_DAYS = 5

# PS-6: Access agreements — signed before access; renewed annually
PS6_SIGNED_BEFORE_ACCESS = True
PS6_RENEWAL_MONTHS = 12

# PS-7: Third-party personnel security — same requirements for contractors
PS7_THIRD_PARTY_REQUIREMENTS_DOCUMENTED = True
PS7_THIRD_PARTY_MONITORING_REQUIRED = True  # Moderate/High

# PS-8: Personnel sanctions — formal process for violations
PS8_SANCTIONS_PROCESS_DOCUMENTED = True

# ── Scope fixture ──────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def fisma_scope_check(entity_profile: dict):
    if not entity_profile.get("subject_to_fisma_or_fedramp", False):
        pytest.skip("System not subject to FISMA/FedRAMP — 800-53 not applicable")


@pytest.fixture
def impact_level(entity_profile: dict) -> str:
    level = entity_profile.get("fips199_impact_level", "").lower()
    if level not in {"low", "moderate", "high"}:
        pytest.skip("FIPS 199 impact level not categorized")
    return level


@pytest.fixture
def odp_values(entity_profile: dict) -> dict:
    odps = entity_profile.get("odp_values", {})
    if not odps:
        pytest.skip("ODP values not documented")
    return odps


# ═══════════════════════════════════════════════════════════════════════════════
# MAINTENANCE (MA)
# ═══════════════════════════════════════════════════════════════════════════════

class TestMA2ControlledMaintenance:
    """MA-2: Controlled Maintenance — all baselines [L][M][H]"""

    def test_maintenance_records_maintained(self, controls_evidence: dict):
        """DETERMINISTIC: maintenance activities must be documented."""
        assert controls_evidence.get("maintenance_records_maintained", False), (
            "MA-2: no maintenance records maintained."
        )

    def test_maintenance_includes_required_fields(self, controls_evidence: dict):
        """DETERMINISTIC: maintenance records must capture date, description, and personnel."""
        required = {"maintenance_date", "description_of_work", "personnel_name"}
        captured = set(controls_evidence.get("maintenance_record_fields", []))
        missing = required - captured
        assert not missing, (
            f"MA-2: maintenance records missing required fields: {missing}."
        )


class TestMA4NonlocalMaintenance:
    """MA-4: Nonlocal Maintenance — Moderate/High [M][H]"""

    def test_remote_maintenance_uses_approved_protocols(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: remote maintenance must use approved encrypted protocols."""
        if impact_level == "low":
            pytest.skip("MA-4 encrypted remote maintenance applies at Moderate/High")
        protocols = set(controls_evidence.get("remote_maintenance_protocols_in_use", []))
        if not protocols:
            pytest.skip("No remote maintenance in use")
        prohibited = protocols & MA4_PROHIBITED_PROTOCOLS
        assert not prohibited, (
            f"MA-4: prohibited remote maintenance protocols in use: {prohibited}."
        )

    def test_remote_maintenance_requires_mfa(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: remote maintenance sessions must require MFA."""
        if impact_level == "low":
            pytest.skip("MA-4 MFA requirement applies at Moderate/High")
        assert controls_evidence.get("remote_maintenance_requires_mfa", False), (
            "MA-4: MFA not required for remote maintenance sessions."
        )

    def test_remote_maintenance_sessions_logged(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: remote maintenance sessions must be logged."""
        if impact_level == "low":
            pytest.skip("MA-4 session logging applies at Moderate/High")
        assert controls_evidence.get("remote_maintenance_sessions_logged", False), (
            "MA-4: remote maintenance sessions are not logged."
        )

    def test_remote_maintenance_fips_validated_crypto(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: FIPS 140-2/3 validated crypto required for remote maintenance channels."""
        if impact_level == "low":
            pytest.skip("MA-4 FIPS crypto applies at Moderate/High")
        assert controls_evidence.get("remote_maintenance_fips_validated_crypto", False), (
            "MA-4: remote maintenance channels do not use FIPS 140-2/3 validated cryptographic modules."
        )


class TestMA5MaintenancePersonnel:
    """MA-5: Maintenance Personnel — all baselines [L][M][H]"""

    def test_maintenance_personnel_authorized_or_escorted(self, controls_evidence: dict):
        """DETERMINISTIC: uncleared maintenance personnel must be escorted during maintenance."""
        assert controls_evidence.get(
            "uncleared_maintenance_personnel_escorted_or_authorized", False
        ), (
            "MA-5: no documented process for escorting uncleared maintenance personnel."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# MEDIA PROTECTION (MP)
# ═══════════════════════════════════════════════════════════════════════════════

class TestMP3MediaMarking:
    """MP-3: Media Marking — Moderate/High [M][H]"""

    def test_removable_media_marked_with_distribution_limitations(
        self, controls_evidence: dict, impact_level
    ):
        """DETERMINISTIC: removable media containing sensitive data must be marked."""
        if impact_level == "low":
            pytest.skip("MP-3 formal marking applies at Moderate/High")
        assert controls_evidence.get("removable_media_marked_appropriately", False), (
            "MP-3: removable media containing sensitive/CUI data is not marked with "
            "handling and distribution limitations."
        )


class TestMP5MediaTransport:
    """MP-5: Media Transport — Moderate/High [M][H]"""

    def test_media_transport_encrypted(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: media containing sensitive data must be encrypted during transport."""
        if impact_level == "low":
            pytest.skip("MP-5 transport encryption applies at Moderate/High")
        assert controls_evidence.get("media_encrypted_during_transport", False), (
            "MP-5: media containing sensitive data is not encrypted during physical transport."
        )

    def test_media_transport_uses_authorized_courier(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: transport of sensitive media must use designated couriers or tracked shipping."""
        if impact_level == "low":
            pytest.skip("MP-5 courier authorization applies at Moderate/High")
        assert controls_evidence.get("media_transport_uses_authorized_courier", False), (
            "MP-5: sensitive media transport does not use designated couriers or tracked/secured shipping."
        )


class TestMP6MediaSanitization:
    """MP-6: Media Sanitization — all baselines [L][M][H]"""

    def test_sanitization_method_nist_800_88_compliant(self, controls_evidence: dict):
        """DETERMINISTIC: media sanitization must use NIST 800-88 methods."""
        methods_used = set(controls_evidence.get("media_sanitization_methods_in_use", []))
        if not methods_used:
            pytest.skip("No media sanitization events recorded")
        prohibited = methods_used & MP6_PROHIBITED_METHODS
        assert not prohibited, (
            f"MP-6: prohibited sanitization methods in use: {prohibited}. "
            f"Use NIST 800-88 clear/purge/destroy."
        )

    @pytest.mark.assumption(
        id="ASSUME-800053-MP-001",
        description=(
            "MP-6: NIST 800-88 clear/purge/destroy required; disposal logs retained ≥3 years; "
            "degauss alone is insufficient for flash/SSD media. Physical destruction required "
            "when purge is technically infeasible."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_disposal_logs_retained(self, controls_evidence: dict):
        """PARAMETERIZED: media disposal logs must be retained for ≥3 years."""
        retention_years = controls_evidence.get("media_disposal_log_retention_years", 0)
        assert retention_years >= MP6_LOG_RETENTION_YEARS, (
            f"MP-6: disposal log retention {retention_years}yr < required {MP6_LOG_RETENTION_YEARS}yr."
        )


class TestMP7MediaUse:
    """MP-7: Media Use — Moderate/High [M][H]"""

    def test_removable_media_restricted(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: use of removable media must be restricted and authorized."""
        if impact_level == "low":
            pytest.skip("MP-7 restriction applies at Moderate/High")
        assert controls_evidence.get("removable_media_restricted_to_authorized_use", False), (
            "MP-7: removable media use not restricted to authorized users and purposes."
        )

    def test_removable_media_exceptions_approved(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: exceptions to removable media restrictions require documented approval."""
        if impact_level == "low":
            pytest.skip("MP-7 exception approval applies at Moderate/High")
        assert controls_evidence.get("removable_media_exception_process_documented", False), (
            "MP-7: no process for approving exceptions to removable media restrictions."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# PHYSICAL AND ENVIRONMENTAL PROTECTION (PE)
# ═══════════════════════════════════════════════════════════════════════════════

class TestPE2PhysicalAccessAuthorizations:
    """PE-2: Physical Access Authorizations — all baselines [L][M][H]"""

    def test_physical_access_list_maintained(self, controls_evidence: dict):
        """DETERMINISTIC: a list of authorized individuals with physical access must be maintained."""
        assert controls_evidence.get("physical_access_list_maintained", False), (
            "PE-2: no list of authorized individuals for physical access maintained."
        )

    @pytest.mark.assumption(
        id="ASSUME-800053-PE-001",
        description=(
            "PE-2 review frequency ODP: annual (12 months) at Moderate; semi-annual (6 months) at High. "
            "Access removed immediately on role change or personnel action."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_physical_access_list_reviewed_within_interval(
        self, controls_evidence: dict, reference_date: date, odp_values: dict, impact_level
    ):
        """PARAMETERIZED: physical access list must be reviewed within ODP interval."""
        max_months = (PE2_HIGH_REVIEW_MONTHS if impact_level == "high"
                      else odp_values.get("pe2_review_months", PE2_ACCESS_LIST_REVIEW_MONTHS))
        last_review = controls_evidence.get("physical_access_list_last_review_date")
        if not last_review:
            pytest.fail("PE-2: physical access list has no review date documented.")
        months_since = (reference_date.year - last_review.year) * 12 + \
                       (reference_date.month - last_review.month)
        assert months_since <= max_months, (
            f"PE-2: access list last reviewed {months_since} months ago; "
            f"ODP requires ≤{max_months} months for {impact_level}."
        )


class TestPE3PhysicalAccessControl:
    """PE-3: Physical Access Control — all baselines [L][M][H]"""

    def test_physical_access_controls_implemented(self, controls_evidence: dict):
        """DETERMINISTIC: physical access controls (locks, badge readers, or guards) must be in place."""
        assert controls_evidence.get("physical_access_controls_implemented", False), (
            "PE-3: no physical access controls documented at facility/data center entry points."
        )

    def test_entry_exit_logged_moderate_high(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: entry/exit audit logs must be maintained at Moderate/High."""
        if impact_level == "low":
            pytest.skip("PE-3 entry/exit audit applies at Moderate/High")
        assert controls_evidence.get("physical_entry_exit_logged", False), (
            "PE-3: physical entry/exit events not logged at Moderate/High."
        )


class TestPE6MonitoringPhysicalAccess:
    """PE-6: Monitoring Physical Access — Moderate/High [M][H]"""

    def test_physical_monitoring_systems_in_place(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: physical monitoring systems (CCTV, intrusion detection) required."""
        if impact_level == "low":
            pytest.skip("PE-6 monitoring applies at Moderate/High")
        assert controls_evidence.get("physical_monitoring_systems_deployed", False), (
            "PE-6: no physical monitoring systems (CCTV/intrusion detection) documented."
        )


class TestPE8VisitorAccessRecords:
    """PE-8: Visitor Access Records — Moderate/High [M][H]"""

    def test_visitor_log_maintained(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: visitor access must be logged."""
        if impact_level == "low":
            pytest.skip("PE-8 visitor log applies at Moderate/High")
        assert controls_evidence.get("visitor_access_log_maintained", False), (
            "PE-8: visitor access log not maintained."
        )

    @pytest.mark.assumption(
        id="ASSUME-800053-PE-002",
        description=(
            "PE-8 visitor log retention ODP: 2 years per 800-53B Moderate default. "
            "Many organizations retain 3 years for alignment with FedRAMP/CMMC; "
            "2-year minimum is the 800-53 floor."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_visitor_log_retention(self, controls_evidence: dict, impact_level):
        """PARAMETERIZED: visitor logs retained for ≥2 years (800-53B default ODP)."""
        if impact_level == "low":
            pytest.skip("PE-8 retention applies at Moderate/High")
        retention_years = controls_evidence.get("visitor_log_retention_years", 0)
        assert retention_years >= PE8_LOG_RETENTION_YEARS, (
            f"PE-8: visitor log retention {retention_years}yr < required {PE8_LOG_RETENTION_YEARS}yr."
        )


class TestPE13FireProtection:
    """PE-13: Fire Protection — all baselines [L][M][H]"""

    def test_fire_detection_and_suppression_documented(self, controls_evidence: dict):
        """DETERMINISTIC: fire detection and suppression systems must be in place and documented."""
        assert controls_evidence.get("fire_detection_and_suppression_documented", False), (
            "PE-13: no fire detection/suppression systems documented at facility."
        )


class TestPE14TemperatureHumidityControls:
    """PE-14: Environmental Controls — all baselines [L][M][H]"""

    def test_environmental_controls_documented(self, controls_evidence: dict):
        """DETERMINISTIC: temperature/humidity controls must be documented."""
        assert controls_evidence.get("temperature_humidity_controls_documented", False), (
            "PE-14: no temperature/humidity (HVAC) controls documented for IT facility."
        )


class TestPE15WaterDamageProtection:
    """PE-15: Water Damage Protection — all baselines [L][M][H]"""

    def test_water_damage_protection_documented(self, controls_evidence: dict):
        """DETERMINISTIC: water damage protection (shutoff valves, drainage) must be documented."""
        assert controls_evidence.get("water_damage_protection_documented", False), (
            "PE-15: no water damage protection measures documented for IT facility."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# PERSONNEL SECURITY (PS)
# ═══════════════════════════════════════════════════════════════════════════════

class TestPS2PositionRiskDesignation:
    """PS-2: Position Risk Designation — all baselines [L][M][H]"""

    def test_position_risk_designations_assigned(self, controls_evidence: dict):
        """DETERMINISTIC: risk designations (high/moderate/low risk) must be assigned to all positions."""
        assert controls_evidence.get("position_risk_designations_documented", False), (
            "PS-2: position risk designations not assigned to organizational roles."
        )


class TestPS3PersonnelScreening:
    """PS-3: Personnel Screening — all baselines [L][M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-PS-001",
        description=(
            "PS-3 screening criteria ODP: screening criteria must be 'commensurate with risk' — "
            "determined by the organization based on position risk designation. "
            "What constitutes adequate screening is PARAMETERIZED by position risk level "
            "and is ultimately an assessor judgment for borderline cases."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_screening_conducted_before_access(self, controls_evidence: dict):
        """PARAMETERIZED: personnel must be screened before accessing the system."""
        assert controls_evidence.get("screening_conducted_before_system_access", False), (
            "PS-3: no process documented ensuring personnel are screened prior to system access."
        )

    def test_screening_commensurate_with_risk_documented(self, controls_evidence: dict):
        """PARAMETERIZED: screening criteria must be documented and tied to position risk level."""
        assert controls_evidence.get("screening_criteria_documented_by_risk_level", False), (
            "PS-3: screening criteria not documented per position risk designation."
        )


class TestPS4PersonnelTermination:
    """PS-4: Personnel Termination — all baselines [L][M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-PS-002",
        description=(
            "PS-4 termination ODP: 800-53B suggests same-day (0 days) for privileged accounts; "
            "within 8 hours as common practice. Credential revocation and account disable "
            "must happen concurrently — not sequentially."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_accounts_disabled_timely_on_termination(self, controls_evidence: dict, odp_values: dict):
        """PARAMETERIZED: accounts disabled within ODP hours of confirmed termination."""
        max_hours = odp_values.get("ps4_account_disable_hours", PS4_ACCOUNT_DISABLE_HOURS)
        violations = [
            t for t in controls_evidence.get("recent_terminations", [])
            if t.get("hours_to_account_disable", 0) > max_hours
        ]
        assert not violations, (
            f"PS-4: {len(violations)} termination(s) where account was not disabled within "
            f"{max_hours}h: {[v.get('user_id') for v in violations]}."
        )

    def test_exit_interview_or_briefing_conducted(self, controls_evidence: dict):
        """DETERMINISTIC: termination must include a security briefing/reminder of obligations."""
        assert controls_evidence.get("exit_security_briefing_process_documented", False), (
            "PS-4: no documented process for exit security briefing or return of organizational assets."
        )


class TestPS5PersonnelTransfer:
    """PS-5: Personnel Transfer — all baselines [L][M][H]"""

    def test_access_reviewed_within_days_of_transfer(self, controls_evidence: dict, odp_values: dict):
        """DETERMINISTIC: access must be reviewed and updated within ODP days of transfer."""
        max_days = odp_values.get("ps5_access_review_days", PS5_ACCESS_REVIEW_DAYS)
        late = [
            t for t in controls_evidence.get("recent_transfers", [])
            if t.get("days_to_access_review", 0) > max_days
        ]
        assert not late, (
            f"PS-5: {len(late)} transfer(s) where access review took >{max_days}d: "
            f"{[t.get('user_id') for t in late]}."
        )


class TestPS6AccessAgreements:
    """PS-6: Access Agreements — all baselines [L][M][H]"""

    def test_access_agreements_signed_before_access(self, controls_evidence: dict):
        """DETERMINISTIC: access agreements must be signed before system access is granted."""
        unsigned = [
            u for u in controls_evidence.get("personnel_onboarding_records", [])
            if not u.get("access_agreement_signed_before_access", False)
        ]
        assert not unsigned, (
            f"PS-6: {len(unsigned)} personnel granted access without signed access agreement."
        )

    def test_access_agreements_renewed_annually(
        self, controls_evidence: dict, reference_date: date
    ):
        """DETERMINISTIC: access agreements must be renewed within 12 months."""
        overdue = [
            u for u in controls_evidence.get("all_personnel_records", [])
            if (reference_date - u.get("access_agreement_signed_date", date.min)).days >
               PS6_RENEWAL_MONTHS * 31
        ]
        assert not overdue, (
            f"PS-6: {len(overdue)} access agreement(s) not renewed within {PS6_RENEWAL_MONTHS} months."
        )


class TestPS7ThirdPartyPersonnelSecurity:
    """PS-7: Third-Party Personnel Security — all baselines [L][M][H]"""

    def test_third_party_security_requirements_documented(self, controls_evidence: dict):
        """DETERMINISTIC: security requirements for third-party personnel must be documented."""
        assert controls_evidence.get("third_party_personnel_security_requirements_documented", False), (
            "PS-7: security requirements for third-party/contractor personnel not documented."
        )

    def test_third_party_compliance_monitored(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: third-party compliance with security requirements must be monitored."""
        if impact_level == "low":
            pytest.skip("PS-7 active monitoring applies at Moderate/High")
        assert controls_evidence.get("third_party_security_compliance_monitored", False), (
            "PS-7: third-party compliance with security requirements not actively monitored."
        )


class TestPS8PersonnelSanctions:
    """PS-8: Personnel Sanctions — all baselines [L][M][H]"""

    def test_sanctions_process_documented(self, controls_evidence: dict):
        """DETERMINISTIC: a formal sanctions process must exist for security policy violations."""
        assert controls_evidence.get("personnel_sanctions_process_documented", False), (
            "PS-8: no documented formal sanctions process for personnel who violate security policies."
        )
```

---

## Assumption registry

| ID | Family/Control | Summary | Review date |
|---|---|---|---|
| ASSUME-800053-MP-001 | MP-6 | NIST 800-88 required; disposal logs ≥3 years; degauss alone insufficient for flash/SSD | 2026-05-21 |
| ASSUME-800053-PE-001 | PE-2 | Access list review ODP: annual at Moderate; semi-annual at High; immediate removal on role change | 2026-05-21 |
| ASSUME-800053-PE-002 | PE-8 | Visitor log retention ODP: 2 years per 800-53B Moderate default | 2026-05-21 |
| ASSUME-800053-PS-001 | PS-3 | Screening criteria commensurate with risk; documented by position risk level; adequacy PARAMETERIZED | 2026-05-21 |
| ASSUME-800053-PS-002 | PS-4 | Termination ODP: account disable ≤8 hours; concurrent credential revocation; same-day for privileged | 2026-05-21 |

## Parse status: Partial — MA, MP, PE, PS added; MA, MP, PE, PS, AU, AC, IA, CM, SC, SI, CP, IR, CA = 13 of 20 families parsed
