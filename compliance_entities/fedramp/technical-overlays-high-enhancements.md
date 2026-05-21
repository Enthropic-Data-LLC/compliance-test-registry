# FedRAMP — Technical Overlays (AU/CM/IA/SC/SI) + SA + High-Only Enhancements

**Source:** FedRAMP Rev 5 baselines; parameter deltas from NIST SP 800-53 r5
**Design note:** This file tests FedRAMP-specific parameter overlays for technical families
  and High-only additional requirements. Run the corresponding 800-53 spec files in parallel
  for base control coverage. FedRAMP tightens or supplements — it does not replace.
**Baseline tags:** `[L]` Low, `[M]` Moderate, `[H]` High — gated by `impact_level` fixture.

---

```python
import pytest
from datetime import date, timedelta
from typing import FrozenSet

# ── AU — FedRAMP Audit Overlay ─────────────────────────────────────────────────

# FedRAMP requires monthly log submission to agency/JAB in ConMon reporting
AU_MONTHLY_LOG_SUBMISSION_REQUIRED = True    # [M][H]
AU_LOG_SUBMISSION_DAYS = 30                  # within 30 days of end of month

# FedRAMP standardizes audit log fields beyond 800-53 AU-3
AU_FEDRAMP_REQUIRED_LOG_FIELDS: FrozenSet[str] = frozenset({
    "date_time_utc",
    "event_type",
    "source_ip",
    "user_id",
    "resource_accessed",
    "action_taken",
    "outcome_success_or_failure",
    "session_id",
})

# SIEM integration required at High
AU_SIEM_REQUIRED_HIGH = True

# ── CM — FedRAMP Configuration Management Overlay ─────────────────────────────

# FedRAMP monthly ConMon reports must include CM status
CM_MONTHLY_REPORT_INCLUDES_CM_STATUS = True

# FedRAMP approved tools list — scanning tools must be FedRAMP authorized
CM_SCAN_TOOLS_FEDRAMP_AUTHORIZED = True      # [M][H]

# Significant change process — CM-3 overlay (also in conmon-and-overlays.md)
CM_SIGNIFICANT_CHANGE_NOTIFY_DAYS = 30

# ── IA — FedRAMP Identity and Authentication Overlays ─────────────────────────

# IA-2(12): PIV credential support — Moderate/High
IA2_PIV_SUPPORT_REQUIRED = True              # [M][H]
IA2_PIV_OCSP_OR_CRL_CHECK = True            # revocation checking required
IA2_PIV_ACCEPTABLE_FALLBACK = frozenset({
    "fido2_passkey", "piv_derived_credential", "smartcard_non_piv",
})

# IA-5 FedRAMP password policy overlay
# FedRAMP tightens: min 8 chars, complexity required, max lifetime 60 days [M],
# or passwordless/MFA + no expiry
IA5_MIN_LENGTH = 8
IA5_COMPLEXITY_REQUIRED = True              # [M]
IA5_MAX_LIFETIME_DAYS = 60                  # or no expiry if MFA + breach monitoring
IA5_FIPS_VALIDATED_AUTHENTICATORS = True    # FIPS 140-2/3 validated tokens/smartcards

# IA-8: Identification and authentication for non-organizational users
IA8_FEDRAMP_AUTHORIZED_IDP_REQUIRED = True  # [M][H]: IdP must be FedRAMP authorized
                                              # or equivalently vetted

# ── SC — FedRAMP System and Communications Protection Overlay ─────────────────

# FedRAMP FIPS overlay (from conmon-and-overlays.md; additional SC-8/28 details here)
SC_TLS_MINIMUM_VERSION = "1.2"
SC_PROHIBITED_CIPHERS: FrozenSet[str] = frozenset({
    "rc4", "des", "3des_for_bulk", "export_grade",
    "null_cipher", "md5_hmac",
})
SC_APPROVED_CIPHER_SUITES: FrozenSet[str] = frozenset({
    "tls_aes_256_gcm_sha384",
    "tls_aes_128_gcm_sha256",
    "tls_chacha20_poly1305_sha256",
    "ecdhe_rsa_aes_256_gcm_sha384",
    "ecdhe_rsa_aes_128_gcm_sha256",
})
SC_DNSSec_REQUIRED = True                   # DNSSEC for all DNS queries [M][H]

# SC-28 FedRAMP: all federal data at rest must be encrypted with AES-256 at High
SC28_HIGH_REQUIRES_AES256 = True           # High: AES-256 minimum (not 128)

# ── SI — FedRAMP System and Information Integrity Overlay ─────────────────────

# FedRAMP monthly patch reporting — patch status submitted in ConMon report
SI_MONTHLY_PATCH_REPORT_REQUIRED = True     # [M][H]
SI_PATCH_REPORT_INCLUDES: FrozenSet[str] = frozenset({
    "total_open_vulnerabilities",
    "critical_count_and_oldest_age",
    "high_count_and_oldest_age",
    "remediated_this_month",
    "poa_m_items",
})

# FedRAMP AV definition update frequency
SI_AV_DEFINITION_UPDATE_HOURS = 24          # same as 800-53; FedRAMP confirms this ODP

# ── SA — FedRAMP Services Acquisition Overlay ─────────────────────────────────

# SA-9: External services — FedRAMP requires sub-CSP services to also be FedRAMP authorized
SA9_SUB_SERVICES_FEDRAMP_AUTHORIZED = True  # [M][H]: external IaaS/PaaS must be FedRAMP authorized
                                              # (or equivalently authorized per JAB determination)

# SA-11: Developer security testing — FedRAMP requires code-level security scanning
SA11_SAST_REQUIRED = True                   # static application security testing [H]
SA11_DAST_REQUIRED = True                   # dynamic testing [H]

# SA-15: Development process documented — FedRAMP requires OWASP Top 10 training for devs [H]
SA15_OWASP_TRAINING_REQUIRED_HIGH = True

# ── High-only enhancements ─────────────────────────────────────────────────────

# PS-8 Insider Threat Program — High only
PS8_INSIDER_THREAT_PROGRAM_REQUIRED = True
PS8_REQUIRED_ELEMENTS: FrozenSet[str] = frozenset({
    "user_activity_monitoring",
    "access_anomaly_detection",
    "data_loss_prevention",
    "insider_threat_awareness_training",
    "incident_response_for_insider_threats",
})

# IA-3 Device identification and authentication — High only
IA3_DEVICE_AUTH_REQUIRED_ALL_DEVICES = True  # cryptographic device authentication [H]

# PE-9 Power Equipment and Cabling — High: redundant power
PE9_REDUNDANT_POWER_REQUIRED_HIGH = True

# PE-11/12 Emergency Power — High: generator + UPS
PE11_GENERATOR_REQUIRED_HIGH = True
PE12_UPS_REQUIRED_HIGH = True

# SR SCRM — High: NIST 800-161 enhanced supplier screening
SR_800161_ENHANCED_SCREENING_HIGH = True

# ── Scope fixture ──────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def fedramp_scope_check(entity_profile: dict):
    if not entity_profile.get("fedramp_in_scope", False):
        pytest.skip("System not subject to FedRAMP — overlays not applicable")


@pytest.fixture
def impact_level(entity_profile: dict) -> str:
    level = entity_profile.get("fips199_impact_level", "").lower()
    if level not in {"low", "moderate", "high"}:
        pytest.skip("FIPS 199 impact level not categorized")
    return level


@pytest.fixture
def odp_values(entity_profile: dict) -> dict:
    return entity_profile.get("odp_values", {})


# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT AND ACCOUNTABILITY — FedRAMP Overlay (AU)
# ═══════════════════════════════════════════════════════════════════════════════

class TestAUFedRAMPLogFields:
    """AU FedRAMP overlay: standardized log fields for ConMon reporting."""

    def test_fedramp_log_fields_captured(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: audit records must capture all FedRAMP-required fields."""
        if impact_level == "low":
            pytest.skip("FedRAMP AU field overlay applies at Moderate/High")
        captured = set(controls_evidence.get("audit_record_fields_captured", []))
        missing = AU_FEDRAMP_REQUIRED_LOG_FIELDS - captured
        assert not missing, (
            f"AU (FedRAMP): audit records missing FedRAMP-required fields: {missing}."
        )


class TestAUMonthlyLogSubmission:
    """AU FedRAMP overlay: monthly log submission to agency/JAB."""

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-AU-001",
        description=(
            "FedRAMP AU overlay: monthly log submission to agency AO or JAB within 30 days "
            "of end of reporting month. Submission is part of ConMon report package."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_monthly_log_submission_current(
        self, controls_evidence: dict, reference_date: date, impact_level
    ):
        """PARAMETERIZED: monthly audit log submission must be current."""
        if impact_level == "low":
            pytest.skip("Monthly log submission applies at Moderate/High")
        last_submission = controls_evidence.get("last_conmon_log_submission_date")
        if not last_submission:
            pytest.fail("AU (FedRAMP): no ConMon log submission date documented.")
        days_since = (reference_date - last_submission).days
        assert days_since <= AU_LOG_SUBMISSION_DAYS + 5, (    # 5-day grace for month boundary
            f"AU (FedRAMP): last log submission {days_since}d ago; must submit within "
            f"{AU_LOG_SUBMISSION_DAYS}d of month end."
        )


class TestAUSIEMHighBaseline:
    """AU FedRAMP High overlay: SIEM integration required."""

    def test_siem_integrated_at_high(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: SIEM integration required at High baseline."""
        if impact_level != "high":
            pytest.skip("SIEM integration required at High baseline only")
        assert controls_evidence.get("siem_integrated_and_operational", False), (
            "AU (FedRAMP High): SIEM not integrated for centralized log analysis."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# IDENTIFICATION AND AUTHENTICATION — FedRAMP Overlay (IA)
# ═══════════════════════════════════════════════════════════════════════════════

class TestIA2PIVSupport:
    """IA-2(12) FedRAMP: PIV credential support at Moderate/High."""

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-IA-001",
        description=(
            "IA-2(12) FedRAMP: PIV/CAC credential support required for Moderate/High. "
            "OCSP or CRL revocation checking must be performed. Fallback authentication "
            "is permitted but must be documented and access-controlled."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_piv_support_implemented(self, controls_evidence: dict, impact_level):
        """PARAMETERIZED: PIV credential acceptance must be implemented at Moderate/High."""
        if impact_level == "low":
            pytest.skip("IA-2(12) PIV support applies at Moderate/High")
        assert controls_evidence.get("piv_credential_acceptance_implemented", False), (
            "IA-2(12) (FedRAMP): PIV/CAC credential acceptance not implemented."
        )

    def test_piv_revocation_checking_enabled(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: OCSP or CRL revocation checking must be enabled for PIV."""
        if impact_level == "low":
            pytest.skip("PIV revocation checking applies at Moderate/High")
        assert controls_evidence.get("piv_revocation_checking_enabled", False), (
            "IA-2(12) (FedRAMP): PIV certificate revocation checking (OCSP/CRL) not enabled."
        )


class TestIA5FedRAMPPasswordOverlay:
    """IA-5 FedRAMP password overlay: FIPS-validated authenticators."""

    def test_authenticators_fips_validated(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: hardware authenticators and smartcards must be FIPS 140-2/3 validated."""
        if impact_level == "low":
            pytest.skip("FIPS authenticator validation applies at Moderate/High")
        assert controls_evidence.get("hardware_authenticators_fips_validated", False) or \
               controls_evidence.get("no_hardware_authenticators_in_use", False), (
            "IA-5 (FedRAMP): hardware authenticators not documented as FIPS 140-2/3 validated."
        )


class TestIA8ExternalIdentityProviders:
    """IA-8 FedRAMP: external IdPs must be FedRAMP authorized or equivalently vetted."""

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-IA-002",
        description=(
            "IA-8 FedRAMP overlay: external identity providers used for non-org users must be "
            "FedRAMP authorized or meet equivalent assurance. IdP not on FedRAMP marketplace "
            "requires JAB/agency AO written determination of equivalency."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_external_idp_fedramp_authorized(self, controls_evidence: dict, impact_level):
        """PARAMETERIZED: external IdPs must be FedRAMP authorized or equivalently approved."""
        if impact_level == "low":
            pytest.skip("IA-8 external IdP requirement applies at Moderate/High")
        uses_external_idp = controls_evidence.get("uses_external_identity_provider", False)
        if not uses_external_idp:
            pytest.skip("No external IdP in use — IA-8 FedRAMP overlay not applicable")
        assert controls_evidence.get("external_idp_fedramp_authorized", False) or \
               controls_evidence.get("external_idp_equivalency_approved_by_ao", False), (
            "IA-8 (FedRAMP): external IdP not FedRAMP authorized and no AO equivalency determination."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM AND COMMUNICATIONS PROTECTION — FedRAMP Overlay (SC)
# ═══════════════════════════════════════════════════════════════════════════════

class TestSCFedRAMPCipherSuites:
    """SC FedRAMP overlay: prohibited cipher suites and minimum approved suites."""

    def test_prohibited_cipher_suites_disabled(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: prohibited cipher suites must be disabled."""
        if impact_level == "low":
            pytest.skip("SC cipher suite control applies at Moderate/High")
        ciphers_in_use = set(controls_evidence.get("tls_cipher_suites_in_use", []))
        prohibited = ciphers_in_use & SC_PROHIBITED_CIPHERS
        assert not prohibited, (
            f"SC (FedRAMP): prohibited cipher suites in use: {prohibited}."
        )


class TestSCDNSSec:
    """SC FedRAMP overlay: DNSSEC for all DNS resolution."""

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-SC-001",
        description=(
            "SC FedRAMP overlay: DNSSEC validation required for all DNS queries; "
            "applicable at Moderate/High. DNSSEC signing required for hosted DNS zones."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_dnssec_validation_enabled(self, controls_evidence: dict, impact_level):
        """PARAMETERIZED: DNSSEC validation must be enabled at Moderate/High."""
        if impact_level == "low":
            pytest.skip("DNSSEC applies at Moderate/High")
        assert controls_evidence.get("dnssec_validation_enabled", False), (
            "SC (FedRAMP): DNSSEC validation not enabled for DNS queries."
        )


class TestSC28HighAES256:
    """SC-28 FedRAMP High: AES-256 required (not just AES-128) for data at rest."""

    def test_at_rest_encryption_aes256_at_high(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: High baseline requires AES-256 for federal data at rest."""
        if impact_level != "high":
            pytest.skip("AES-256 at-rest requirement applies at High baseline only")
        algorithm = controls_evidence.get("at_rest_encryption_algorithm", "unknown").lower()
        assert "aes_256" in algorithm or "aes256" in algorithm, (
            "SC-28 (FedRAMP High): at-rest encryption does not meet AES-256 minimum requirement."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM AND INFORMATION INTEGRITY — FedRAMP Overlay (SI)
# ═══════════════════════════════════════════════════════════════════════════════

class TestSIMonthlyPatchReport:
    """SI FedRAMP overlay: monthly patch status report submitted in ConMon package."""

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-SI-001",
        description=(
            "SI FedRAMP overlay: monthly patch report submitted as part of ConMon package. "
            "Must include total open vulns, critical/high counts and ages, remediated this month, "
            "and open POA&M items. Late submission triggers agency/JAB notification."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_monthly_patch_report_current(
        self, controls_evidence: dict, reference_date: date, impact_level
    ):
        """PARAMETERIZED: monthly patch report must be submitted within 30 days."""
        if impact_level == "low":
            pytest.skip("Monthly patch reporting applies at Moderate/High")
        last_report = controls_evidence.get("last_patch_report_submission_date")
        if not last_report:
            pytest.fail("SI (FedRAMP): no monthly patch report submission date documented.")
        days_since = (reference_date - last_report).days
        assert days_since <= 35, (    # 30d + 5d grace for reporting period boundary
            f"SI (FedRAMP): last patch report {days_since}d ago; monthly submission required."
        )

    def test_patch_report_contains_required_elements(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: monthly patch report must include all required data elements."""
        if impact_level == "low":
            pytest.skip("Patch report content check applies at Moderate/High")
        report_elements = set(controls_evidence.get("patch_report_elements_included", []))
        missing = SI_PATCH_REPORT_INCLUDES - report_elements
        assert not missing, (
            f"SI (FedRAMP): monthly patch report missing required elements: {missing}."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM AND SERVICES ACQUISITION — FedRAMP Overlay (SA)
# ═══════════════════════════════════════════════════════════════════════════════

class TestSA9SubServicesFedRAMPAuthorized:
    """SA-9 FedRAMP: external sub-services must be FedRAMP authorized."""

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-SA-001",
        description=(
            "SA-9 FedRAMP overlay: IaaS/PaaS services used by the CSP (sub-services) must "
            "be FedRAMP authorized. Exception requires JAB/agency written determination. "
            "CSP must track authorization status of all sub-services annually."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_sub_services_fedramp_authorized(self, controls_evidence: dict, impact_level):
        """PARAMETERIZED: all external IaaS/PaaS sub-services must be FedRAMP authorized."""
        if impact_level == "low":
            pytest.skip("SA-9 sub-service authorization applies at Moderate/High")
        unauthorized = [
            s for s in controls_evidence.get("external_sub_services", [])
            if not s.get("fedramp_authorized", False)
            and not s.get("ao_equivalency_approval", False)
        ]
        assert not unauthorized, (
            f"SA-9 (FedRAMP): {len(unauthorized)} external sub-service(s) not FedRAMP authorized "
            f"without AO approval: {[s.get('service_name') for s in unauthorized]}."
        )


class TestSA11FedRAMPSASTDASTHigh:
    """SA-11 FedRAMP High: SAST and DAST required for application-layer security testing."""

    def test_sast_conducted_for_high(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: static application security testing required at High."""
        if impact_level != "high":
            pytest.skip("SAST requirement applies at High baseline only")
        assert controls_evidence.get("sast_conducted", False), (
            "SA-11 (FedRAMP High): static application security testing (SAST) not conducted."
        )

    def test_dast_conducted_for_high(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: dynamic application security testing required at High."""
        if impact_level != "high":
            pytest.skip("DAST requirement applies at High baseline only")
        assert controls_evidence.get("dast_conducted", False), (
            "SA-11 (FedRAMP High): dynamic application security testing (DAST) not conducted."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# HIGH-ONLY ENHANCEMENTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPS8InsiderThreatProgramHigh:
    """PS-8 / PM (overlay): Insider Threat Program — High only."""

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-H-001",
        description=(
            "FedRAMP High overlay: formal insider threat program required with user activity "
            "monitoring, anomaly detection, DLP, insider threat awareness training, and "
            "dedicated IR for insider threat incidents. Program adequacy is PARAMETERIZED."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_insider_threat_program_exists(self, controls_evidence: dict, impact_level):
        """PARAMETERIZED: formal insider threat program required at High."""
        if impact_level != "high":
            pytest.skip("Insider threat program required at High baseline only")
        assert controls_evidence.get("insider_threat_program_documented", False), (
            "PS-8 (FedRAMP High): no formal insider threat program documented."
        )

    def test_insider_threat_program_elements(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: insider threat program must contain required elements."""
        if impact_level != "high":
            pytest.skip("Insider threat program elements check applies at High only")
        present = set(controls_evidence.get("insider_threat_program_elements", []))
        missing = PS8_REQUIRED_ELEMENTS - present
        assert not missing, (
            f"PS-8 (FedRAMP High): insider threat program missing elements: {missing}."
        )


class TestIA3DeviceAuthHigh:
    """IA-3 FedRAMP High: cryptographic device identification and authentication."""

    def test_device_authentication_cryptographic(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: all devices must use cryptographic authentication at High."""
        if impact_level != "high":
            pytest.skip("IA-3 cryptographic device auth required at High baseline only")
        assert controls_evidence.get("device_cryptographic_authentication_in_use", False), (
            "IA-3 (FedRAMP High): cryptographic device identification and authentication "
            "not implemented for all system devices."
        )


class TestPERedundantPowerHigh:
    """PE-9/11/12 FedRAMP High: redundant power and emergency power required."""

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-H-002",
        description=(
            "FedRAMP High overlay: PE-9 redundant power distribution paths required; "
            "PE-11 generator required with fuel supply; PE-12 UPS required with adequate "
            "runtime to support graceful shutdown and generator startup."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_redundant_power_at_high(self, controls_evidence: dict, impact_level):
        """PARAMETERIZED: redundant power distribution required at High."""
        if impact_level != "high":
            pytest.skip("Redundant power applies at High baseline only")
        assert controls_evidence.get("redundant_power_paths_documented", False), (
            "PE-9 (FedRAMP High): redundant power distribution paths not documented."
        )

    def test_generator_backup_at_high(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: emergency generator required at High."""
        if impact_level != "high":
            pytest.skip("Generator backup applies at High baseline only")
        assert controls_evidence.get("emergency_generator_in_place", False), (
            "PE-11 (FedRAMP High): emergency generator not documented."
        )

    def test_ups_in_place_at_high(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: UPS required at High."""
        if impact_level != "high":
            pytest.skip("UPS requirement applies at High baseline only")
        assert controls_evidence.get("ups_in_place", False), (
            "PE-12 (FedRAMP High): uninterruptible power supply (UPS) not documented."
        )


class TestSREnhancedSCRMHigh:
    """SR FedRAMP High: NIST 800-161 enhanced supplier screening."""

    @pytest.mark.assumption(
        id="ASSUME-FEDRAMP-H-003",
        description=(
            "FedRAMP High SR overlay: NIST SP 800-161 enhanced supply chain risk management "
            "required. Critical supplier identification must include second-tier suppliers. "
            "Enhanced screening criteria and frequency per 800-161 C-SCRM practices. "
            "Adequacy of enhanced screening is PARAMETERIZED."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_nist_800161_enhanced_scrm_at_high(self, controls_evidence: dict, impact_level):
        """PARAMETERIZED: NIST 800-161 enhanced SCRM required at High."""
        if impact_level != "high":
            pytest.skip("Enhanced SCRM per NIST 800-161 applies at High baseline only")
        assert controls_evidence.get("nist_800161_enhanced_scrm_documented", False), (
            "SR (FedRAMP High): NIST SP 800-161 enhanced supply chain risk management "
            "not documented."
        )

    def test_second_tier_suppliers_assessed_at_high(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: second-tier (sub-supplier) assessment required at High."""
        if impact_level != "high":
            pytest.skip("Second-tier supplier assessment applies at High only")
        assert controls_evidence.get("second_tier_suppliers_identified", False), (
            "SR (FedRAMP High): second-tier (sub-supplier) supply chain risks not assessed."
        )
```

---

## Assumption registry

| ID | Family/Control | Summary | Review date |
|---|---|---|---|
| ASSUME-FEDRAMP-AU-001 | AU overlay | Monthly log submission within 30 days of month end; part of ConMon package | 2026-05-21 |
| ASSUME-FEDRAMP-IA-001 | IA-2(12) overlay | PIV support required M/H; OCSP/CRL revocation check; fallback documented | 2026-05-21 |
| ASSUME-FEDRAMP-IA-002 | IA-8 overlay | External IdPs must be FedRAMP authorized or AO equivalency determination | 2026-05-21 |
| ASSUME-FEDRAMP-SC-001 | SC overlay | DNSSEC validation required M/H; prohibited cipher suites enumerated | 2026-05-21 |
| ASSUME-FEDRAMP-SI-001 | SI overlay | Monthly patch report in ConMon package; 5 required data elements | 2026-05-21 |
| ASSUME-FEDRAMP-SA-001 | SA-9 overlay | External sub-services must be FedRAMP authorized or AO equivalency; tracked annually | 2026-05-21 |
| ASSUME-FEDRAMP-H-001 | PS-8/PM High | Insider threat program with 5 required elements; program adequacy PARAMETERIZED | 2026-05-21 |
| ASSUME-FEDRAMP-H-002 | PE-9/11/12 High | Redundant power + generator + UPS required at High | 2026-05-21 |
| ASSUME-FEDRAMP-H-003 | SR High | NIST 800-161 enhanced SCRM + second-tier supplier assessment at High | 2026-05-21 |

## Parse status: Complete — 3 spec files (conmon-and-overlays.md + account-contingency-media.md + technical-overlays-high-enhancements.md); all Moderate baseline overlays and High-only enhancements parsed; 28 total assumptions
