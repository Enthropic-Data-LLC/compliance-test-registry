# NIST SP 800-53 r5 — Contingency Planning, Incident Response, Assessment/Authorization/Monitoring

**Source:** NIST SP 800-53 Rev 5 (Final, September 2020) + 800-53B baselines
**Coverage:** CP (13 base controls), IR (10 base controls), CA (9 base controls)
**Baseline tags:** `[L]` Low, `[M]` Moderate, `[H]` High — gated by `impact_level` fixture.
**ODP framework:** ODP values documented in SSP; tests that reference undocumented ODPs
  block as CONTESTED until the ODP is recorded and ISSO-approved.

---

```python
import pytest
from datetime import date, timedelta, datetime
from typing import FrozenSet, Optional

# ── CP — Contingency Planning ──────────────────────────────────────────────────

# CP-2 contingency plan required elements and review cadence
CP2_REQUIRED_PLAN_ELEMENTS: FrozenSet[str] = frozenset({
    "essential_missions_and_business_functions",
    "recovery_objectives_and_priorities",
    "roles_and_responsibilities",
    "contact_information",
    "recovery_procedures",
    "alternate_site_procedures",
    "backup_and_restoration_procedures",
    "poe_activities",                    # plan of action post-event
})
CP2_REVIEW_MONTHS = 12                   # ODP default: annual [M][H]

# CP-3 contingency training frequency
CP3_TRAINING_MONTHS = 12                 # annual [M]; 6 months [H]
CP3_HIGH_TRAINING_MONTHS = 6

# CP-4 contingency plan testing
CP4_TEST_MONTHS = 12                     # annual [M][H]
CP4_HIGH_TEST_TYPE = "functional"        # High: functional or full-interruption test

# CP-6 alternate storage site
CP6_SEPARATION_REQUIRED = True
CP6_ACCESSIBILITY_DOCUMENTED_REQUIRED = True

# CP-7 alternate processing site
CP7_REQUIRED = True                      # Moderate/High
CP7_EQUIVALENT_CAPABILITY_DOCUMENTED = True  # alternate site must have equivalent security

# CP-9 backup
CP9_USER_DATA_BACKUP_DAYS = 1           # daily user-level backups [M][H]
CP9_SYSTEM_LEVEL_BACKUP_DAYS = 7        # weekly system-level [M][H]
CP9_TEST_MONTHS = 12                    # annual restoration test
CP9_BACKUP_COPIES = 3                   # 3-2-1 rule: 3 copies, 2 media types, 1 offsite

# CP-10 recovery / reconstitution
CP10_RTO_RPO_DOCUMENTED = True

# ── IR — Incident Response ─────────────────────────────────────────────────────

# IR-2 incident response training
IR2_TRAINING_MONTHS = 12                # annual [M][H]
IR2_HIGH_TRAINING_MONTHS = 6           # semi-annual for High

# IR-3 incident response testing
IR3_TEST_MONTHS = 12                    # annual [M][H]
IR3_HIGH_TEST_MONTHS = 6               # semi-annual for High

# IR-4 incident handling
IR4_REQUIRED_PROCESS_STEPS: FrozenSet[str] = frozenset({
    "detection",
    "analysis",
    "containment",
    "eradication",
    "recovery",
    "post_incident_activity",
})

# IR-5 incident monitoring — DETERMINISTIC at Moderate/High
IR5_TRACKING_SYSTEM_REQUIRED = True

# IR-6 incident reporting
IR6_REPORT_HOURS = 1                    # report to designated authorities within 1 hour [M][H]
                                        # ODP: organization defines the reporting target
# IR-7 incident response assistance — DETERMINISTIC presence
IR7_SUPPORT_RESOURCE_DESIGNATED = True

# IR-8 incident response plan
IR8_PLAN_REVIEW_MONTHS = 12            # annual review and update

# ── CA — Assessment, Authorization, Continuous Monitoring ─────────────────────

# CA-2 control assessments
CA2_ASSESSMENT_MONTHS = 36             # triennial minimum [M][H]; can be more frequent
CA2_3PAO_REQUIRED_FEDRAMP = True       # FedRAMP-specific; handled in fedramp/ spec

# CA-5 plan of action and milestones (POA&M)
CA5_CRITICAL_REMEDIATION_DAYS = 30     # CVSS ≥9.0 / Critical finding
CA5_HIGH_REMEDIATION_DAYS = 90         # High finding
CA5_UPDATE_MONTHS = 3                  # POA&M reviewed/updated at least quarterly [M][H]

# CA-7 continuous monitoring strategy
CA7_VULN_SCAN_MONTHS = 1              # monthly OS/infrastructure scans [M][H]
CA7_CONMON_PLAN_REVIEW_MONTHS = 12    # annual ConMon strategy review

# CA-8 penetration testing
CA8_TEST_MONTHS = 12                  # annual penetration test [H] (Moderate: per org policy)

# ── Scope fixture ─────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def fisma_scope_check(entity_profile: dict):
    """Skip if system is not subject to FISMA/FedRAMP."""
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
        pytest.skip("ODP values not documented — PARAMETERIZED tests cannot execute")
    return odps


# ═══════════════════════════════════════════════════════════════════════════════
# CONTINGENCY PLANNING (CP)
# ═══════════════════════════════════════════════════════════════════════════════

class TestCP2ContingencyPlan:
    """CP-2: Contingency Plan — Moderate/High [M][H]"""

    def test_contingency_plan_exists(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: a documented contingency plan must exist."""
        if impact_level == "low":
            pytest.skip("CP-2 documented plan required at Moderate/High")
        assert controls_evidence.get("contingency_plan_documented", False), (
            "CP-2: no contingency plan documented."
        )

    def test_contingency_plan_required_elements(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: plan must contain all required CP-2 elements."""
        if impact_level == "low":
            pytest.skip("CP-2 required elements apply at Moderate/High")
        present = set(controls_evidence.get("contingency_plan_elements", []))
        missing = CP2_REQUIRED_PLAN_ELEMENTS - present
        assert not missing, (
            f"CP-2: contingency plan missing required elements: {missing}."
        )

    @pytest.mark.assumption(
        id="ASSUME-800053-CP-001",
        description=(
            "CP-2 review/update: annual (12 months) per 800-53B Moderate default ODP; "
            "also after system changes, incidents, or exercises that expose deficiencies."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_contingency_plan_reviewed_annually(
        self, controls_evidence: dict, reference_date: date, odp_values: dict, impact_level
    ):
        """PARAMETERIZED: contingency plan must be reviewed within the ODP review interval."""
        if impact_level == "low":
            pytest.skip("CP-2 annual review applies at Moderate/High")
        review_months = odp_values.get("cp2_review_months", CP2_REVIEW_MONTHS)
        last_review = controls_evidence.get("contingency_plan_last_review_date")
        if not last_review:
            pytest.fail("CP-2: contingency plan review date not documented.")
        months_since = (reference_date.year - last_review.year) * 12 + \
                       (reference_date.month - last_review.month)
        assert months_since <= review_months, (
            f"CP-2: plan last reviewed {months_since} months ago; ODP requires ≤{review_months} months."
        )


class TestCP3ContingencyTraining:
    """CP-3: Contingency Training — Moderate/High [M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-CP-002",
        description=(
            "CP-3 training frequency ODP: annual for Moderate (800-53B default); "
            "semi-annual (6 months) for High. Role-based for personnel with CP responsibilities."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_contingency_training_current(
        self, controls_evidence: dict, reference_date: date, odp_values: dict, impact_level
    ):
        """PARAMETERIZED: contingency training must occur within ODP frequency."""
        if impact_level == "low":
            pytest.skip("CP-3 formal training applies at Moderate/High")
        max_months = (CP3_HIGH_TRAINING_MONTHS if impact_level == "high"
                      else odp_values.get("cp3_training_months", CP3_TRAINING_MONTHS))
        last_training = controls_evidence.get("contingency_training_last_date")
        if not last_training:
            pytest.fail("CP-3: contingency training date not documented.")
        months_since = (reference_date.year - last_training.year) * 12 + \
                       (reference_date.month - last_training.month)
        assert months_since <= max_months, (
            f"CP-3: last contingency training {months_since} months ago; "
            f"ODP requires ≤{max_months} months for {impact_level}."
        )


class TestCP4ContingencyPlanTesting:
    """CP-4: Contingency Plan Testing — Moderate/High [M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-CP-003",
        description=(
            "CP-4 test type and frequency ODP: annual at Moderate (tabletop acceptable); "
            "High baseline: functional or full-interruption test required annually. "
            "Test must cover all essential mission/business functions."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_contingency_plan_tested_within_interval(
        self, controls_evidence: dict, reference_date: date, odp_values: dict, impact_level
    ):
        """PARAMETERIZED: contingency plan must be tested within ODP interval."""
        if impact_level == "low":
            pytest.skip("CP-4 formal testing applies at Moderate/High")
        test_months = odp_values.get("cp4_test_months", CP4_TEST_MONTHS)
        last_test = controls_evidence.get("contingency_plan_last_test_date")
        if not last_test:
            pytest.fail("CP-4: no contingency plan test has been conducted.")
        months_since = (reference_date.year - last_test.year) * 12 + \
                       (reference_date.month - last_test.month)
        assert months_since <= test_months, (
            f"CP-4: last test {months_since} months ago; ODP requires ≤{test_months} months."
        )

    def test_high_baseline_functional_test(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: High baseline requires a functional (not tabletop-only) test."""
        if impact_level != "high":
            pytest.skip("Functional test requirement applies at High baseline only")
        test_type = controls_evidence.get("contingency_plan_last_test_type", "tabletop").lower()
        assert test_type in {"functional", "full_interruption"}, (
            f"CP-4: High baseline requires functional test; last test type was '{test_type}'."
        )


class TestCP6AlternateStorageSite:
    """CP-6: Alternate Storage Site — Moderate/High [M][H]"""

    def test_alternate_storage_site_established(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: an alternate storage site must be established."""
        if impact_level == "low":
            pytest.skip("CP-6 alternate storage applies at Moderate/High")
        assert controls_evidence.get("alternate_storage_site_established", False), (
            "CP-6: no alternate storage site established."
        )

    def test_alternate_storage_geographically_separated(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: alternate storage must be geographically separated from primary."""
        if impact_level == "low":
            pytest.skip("CP-6 geographic separation applies at Moderate/High")
        assert controls_evidence.get("alternate_storage_geographically_separated", False), (
            "CP-6: alternate storage site is not geographically separated from the primary site."
        )

    def test_alternate_storage_accessibility_documented(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: accessibility to alternate storage during disruption must be documented."""
        if impact_level == "low":
            pytest.skip("CP-6 accessibility documentation applies at Moderate/High")
        assert controls_evidence.get("alternate_storage_accessibility_plan_documented", False), (
            "CP-6: no documented plan for accessing alternate storage site during a disruption."
        )


class TestCP7AlternateProcessingSite:
    """CP-7: Alternate Processing Site — Moderate/High [M][H]"""

    def test_alternate_processing_site_established(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: an alternate processing site must be established at Moderate/High."""
        if impact_level == "low":
            pytest.skip("CP-7 alternate processing applies at Moderate/High")
        assert controls_evidence.get("alternate_processing_site_established", False), (
            "CP-7: no alternate processing site established."
        )

    @pytest.mark.human_review_required(
        reason=(
            "CP-7: whether the alternate processing site provides equivalent security controls "
            "is a human-judgment determination — the alternate site's control environment must "
            "be assessed and documented, but sufficiency is assessor-evaluated."
        )
    )
    def test_alternate_processing_equivalent_security(self, controls_evidence: dict, impact_level):
        """CONTESTED: alternate site security must be equivalent to the primary site."""
        if impact_level == "low":
            pytest.skip("CP-7 equivalent security applies at Moderate/High")
        assert controls_evidence.get("alternate_site_security_equivalence_assessed", False), (
            "CP-7: alternate processing site security has not been assessed for equivalence "
            "to the primary site."
        )


class TestCP9Backups:
    """CP-9: Information System Backup — Moderate/High [M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-CP-004",
        description=(
            "CP-9 backup frequency ODPs: user-level daily; system-level weekly. "
            "Backups must be tested for restorability annually. Backup copies protected "
            "with equivalent or stronger controls than primary system. 3-2-1 rule (3 copies, "
            "2 media types, 1 offsite) is standard practice satisfying CP-9."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_user_data_backup_current(
        self, controls_evidence: dict, reference_date: date, odp_values: dict, impact_level
    ):
        """PARAMETERIZED: user-level data backed up daily."""
        if impact_level == "low":
            pytest.skip("CP-9 daily backup applies at Moderate/High")
        max_days = odp_values.get("cp9_user_backup_days", CP9_USER_DATA_BACKUP_DAYS)
        last_backup = controls_evidence.get("last_user_data_backup_date")
        if not last_backup:
            pytest.fail("CP-9: no user data backup date documented.")
        days_since = (reference_date - last_backup).days
        assert days_since <= max_days, (
            f"CP-9: last user data backup {days_since}d ago; ODP requires ≤{max_days}d."
        )

    def test_backup_restoration_tested_annually(
        self, controls_evidence: dict, reference_date: date, impact_level
    ):
        """DETERMINISTIC: backup restoration must be tested within 12 months."""
        if impact_level == "low":
            pytest.skip("CP-9 restoration test applies at Moderate/High")
        last_test = controls_evidence.get("backup_restoration_last_test_date")
        if not last_test:
            pytest.fail("CP-9: no backup restoration test has been conducted.")
        months_since = (reference_date.year - last_test.year) * 12 + \
                       (reference_date.month - last_test.month)
        assert months_since <= CP9_TEST_MONTHS, (
            f"CP-9: backup restoration last tested {months_since} months ago; "
            f"must test within {CP9_TEST_MONTHS} months."
        )

    def test_backups_stored_offsite(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: backup copies must be stored at an offsite or alternate location."""
        if impact_level == "low":
            pytest.skip("CP-9 offsite storage applies at Moderate/High")
        assert controls_evidence.get("backup_copies_stored_offsite", False), (
            "CP-9: backup copies not stored offsite or at an alternate storage location."
        )


class TestCP10RecoveryReconstitution:
    """CP-10: Information System Recovery and Reconstitution — Moderate/High [M][H]"""

    def test_rto_documented(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: Recovery Time Objective (RTO) must be documented."""
        if impact_level == "low":
            pytest.skip("CP-10 RTO documentation applies at Moderate/High")
        assert controls_evidence.get("rto_documented_in_contingency_plan", False), (
            "CP-10: Recovery Time Objective (RTO) not documented in contingency plan."
        )

    def test_rpo_documented(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: Recovery Point Objective (RPO) must be documented."""
        if impact_level == "low":
            pytest.skip("CP-10 RPO documentation applies at Moderate/High")
        assert controls_evidence.get("rpo_documented_in_contingency_plan", False), (
            "CP-10: Recovery Point Objective (RPO) not documented in contingency plan."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# INCIDENT RESPONSE (IR)
# ═══════════════════════════════════════════════════════════════════════════════

class TestIR2IncidentResponseTraining:
    """IR-2: Incident Response Training — Moderate/High [M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-IR-001",
        description=(
            "IR-2 training frequency ODP: annual for Moderate; semi-annual (6 months) for High. "
            "Training must cover roles and responsibilities, incident handling procedures, "
            "and reporting requirements."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_incident_response_training_current(
        self, controls_evidence: dict, reference_date: date, odp_values: dict, impact_level
    ):
        """PARAMETERIZED: IR training must occur within ODP frequency."""
        if impact_level == "low":
            pytest.skip("IR-2 formal training applies at Moderate/High")
        max_months = (IR2_HIGH_TRAINING_MONTHS if impact_level == "high"
                      else odp_values.get("ir2_training_months", IR2_TRAINING_MONTHS))
        last_training = controls_evidence.get("ir_training_last_date")
        if not last_training:
            pytest.fail("IR-2: no incident response training date documented.")
        months_since = (reference_date.year - last_training.year) * 12 + \
                       (reference_date.month - last_training.month)
        assert months_since <= max_months, (
            f"IR-2: last IR training {months_since} months ago; ODP requires ≤{max_months} months."
        )


class TestIR3IncidentResponseTesting:
    """IR-3: Incident Response Testing — Moderate/High [M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-IR-002",
        description=(
            "IR-3 test frequency ODP: annual for Moderate; semi-annual for High. "
            "Tabletop exercises and functional exercises both satisfy 800-53 IR-3. "
            "Test must exercise detection, analysis, containment, and recovery processes."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_incident_response_tested_within_interval(
        self, controls_evidence: dict, reference_date: date, odp_values: dict, impact_level
    ):
        """PARAMETERIZED: IR plan must be tested within ODP interval."""
        if impact_level == "low":
            pytest.skip("IR-3 formal testing applies at Moderate/High")
        max_months = (IR3_HIGH_TEST_MONTHS if impact_level == "high"
                      else odp_values.get("ir3_test_months", IR3_TEST_MONTHS))
        last_test = controls_evidence.get("ir_plan_last_test_date")
        if not last_test:
            pytest.fail("IR-3: no incident response plan test has been conducted.")
        months_since = (reference_date.year - last_test.year) * 12 + \
                       (reference_date.month - last_test.month)
        assert months_since <= max_months, (
            f"IR-3: last IR test {months_since} months ago; ODP requires ≤{max_months} months."
        )


class TestIR4IncidentHandling:
    """IR-4: Incident Handling — all baselines [L][M][H]"""

    def test_incident_handling_capability_established(self, controls_evidence: dict):
        """DETERMINISTIC: an incident handling capability must be established."""
        assert controls_evidence.get("incident_handling_capability_documented", False), (
            "IR-4: no documented incident handling capability."
        )

    def test_incident_handling_process_covers_required_steps(self, controls_evidence: dict):
        """DETERMINISTIC: incident handling must cover all required process phases."""
        covered = set(controls_evidence.get("incident_handling_process_steps", []))
        missing = IR4_REQUIRED_PROCESS_STEPS - covered
        assert not missing, (
            f"IR-4: incident handling process missing required phases: {missing}."
        )


class TestIR5IncidentMonitoring:
    """IR-5: Incident Monitoring — Moderate/High [M][H]"""

    def test_incident_tracking_system_in_use(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: a system for tracking/documenting incidents must be in use."""
        if impact_level == "low":
            pytest.skip("IR-5 automated tracking applies at Moderate/High")
        assert controls_evidence.get("incident_tracking_system_in_use", False), (
            "IR-5: no incident tracking/documentation system in use."
        )


class TestIR6IncidentReporting:
    """IR-6: Incident Reporting — all baselines [L][M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-IR-003",
        description=(
            "IR-6 reporting ODP: reporting within 1 hour of discovering incident "
            "(800-53B Moderate default for confirmed incidents). "
            "Reporting target (US-CERT, CISA, agency CISO) defined by org ODP. "
            "FedRAMP tightens to US-CERT/FedRAMP PMO notification."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_incident_reporting_target_documented(self, controls_evidence: dict, odp_values: dict):
        """PARAMETERIZED: designated incident reporting authority must be documented in SSP."""
        reporting_authority = odp_values.get("ir6_reporting_authority")
        assert reporting_authority, (
            "IR-6: incident reporting authority not documented as ODP in SSP."
        )

    def test_recent_incidents_reported_timely(self, controls_evidence: dict, odp_values: dict):
        """DETERMINISTIC: incidents must be reported to designated authority within ODP timeframe."""
        max_hours = odp_values.get("ir6_report_hours", IR6_REPORT_HOURS)
        late_incidents = [
            i for i in controls_evidence.get("recent_confirmed_incidents", [])
            if i.get("hours_to_reporting", 0) > max_hours
        ]
        assert not late_incidents, (
            f"IR-6: {len(late_incidents)} incident(s) reported beyond {max_hours}-hour ODP deadline: "
            f"{[i.get('incident_id') for i in late_incidents]}."
        )


class TestIR7IncidentResponseAssistance:
    """IR-7: Incident Response Assistance — all baselines [L][M][H]"""

    def test_incident_support_resource_designated(self, controls_evidence: dict):
        """DETERMINISTIC: an advisory support resource for incident response must be designated."""
        assert controls_evidence.get("ir_support_resource_designated", False), (
            "IR-7: no designated incident response advisory/assistance resource documented."
        )


class TestIR8IncidentResponsePlan:
    """IR-8: Incident Response Plan — all baselines [L][M][H]"""

    def test_incident_response_plan_documented(self, controls_evidence: dict):
        """DETERMINISTIC: a documented incident response plan must exist."""
        assert controls_evidence.get("incident_response_plan_documented", False), (
            "IR-8: no incident response plan documented."
        )

    def test_incident_response_plan_reviewed_annually(
        self, controls_evidence: dict, reference_date: date
    ):
        """DETERMINISTIC: IRP must be reviewed and updated within 12 months."""
        last_review = controls_evidence.get("irp_last_review_date")
        if not last_review:
            pytest.fail("IR-8: no IRP review date documented.")
        months_since = (reference_date.year - last_review.year) * 12 + \
                       (reference_date.month - last_review.month)
        assert months_since <= IR8_PLAN_REVIEW_MONTHS, (
            f"IR-8: IRP last reviewed {months_since} months ago; must review within "
            f"{IR8_PLAN_REVIEW_MONTHS} months."
        )

    def test_irp_distributed_to_relevant_personnel(self, controls_evidence: dict):
        """DETERMINISTIC: IRP must be distributed to personnel with IR responsibilities."""
        assert controls_evidence.get("irp_distributed_to_ir_personnel", False), (
            "IR-8: IRP not documented as distributed to incident response personnel."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# ASSESSMENT, AUTHORIZATION, CONTINUOUS MONITORING (CA)
# ═══════════════════════════════════════════════════════════════════════════════

class TestCA2ControlAssessments:
    """CA-2: Control Assessments — all baselines [L][M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-CA-001",
        description=(
            "CA-2 assessment frequency ODP: triennial (36 months) for Moderate/High "
            "per 800-53B; annual assessments at High are recommended but ODP-bound. "
            "Assessment scope must cover all implemented controls in the security plan."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_control_assessment_current(
        self, controls_evidence: dict, reference_date: date, odp_values: dict
    ):
        """PARAMETERIZED: control assessment must be conducted within ODP interval."""
        assessment_months = odp_values.get("ca2_assessment_months", CA2_ASSESSMENT_MONTHS)
        last_assessment = controls_evidence.get("last_control_assessment_date")
        if not last_assessment:
            pytest.fail("CA-2: no control assessment date documented.")
        months_since = (reference_date.year - last_assessment.year) * 12 + \
                       (reference_date.month - last_assessment.month)
        assert months_since <= assessment_months, (
            f"CA-2: last assessment {months_since} months ago; ODP requires ≤{assessment_months} months."
        )

    def test_assessment_scope_covers_all_implemented_controls(self, controls_evidence: dict):
        """DETERMINISTIC: assessment must cover all controls in the security plan."""
        assert controls_evidence.get("assessment_covers_all_ssp_controls", False), (
            "CA-2: control assessment did not cover all controls documented in the security plan."
        )


class TestCA5PlanOfActionAndMilestones:
    """CA-5: Plan of Action and Milestones (POA&M) — all baselines [L][M][H]"""

    def test_poam_maintained(self, controls_evidence: dict):
        """DETERMINISTIC: a POA&M must be maintained to document remediation activities."""
        assert controls_evidence.get("poam_maintained", False), (
            "CA-5: no Plan of Action and Milestones (POA&M) maintained."
        )

    @pytest.mark.assumption(
        id="ASSUME-800053-CA-002",
        description=(
            "CA-5 POA&M SLAs: critical findings (CVSS≥9.0 or High risk rating) ≤30 days; "
            "high findings ≤90 days. Update cadence: quarterly review minimum. "
            "No overdue items without a documented and approved exception or risk acceptance."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_no_overdue_critical_poam_items(
        self, controls_evidence: dict, reference_date: date, odp_values: dict
    ):
        """PARAMETERIZED: no critical POA&M items past committed completion date."""
        max_days = odp_values.get("ca5_critical_remediation_days", CA5_CRITICAL_REMEDIATION_DAYS)
        overdue = [
            item for item in controls_evidence.get("open_poam_items", [])
            if item.get("severity", "").lower() in {"critical", "high_risk"}
            and item.get("committed_completion_date")
            and (reference_date - item["committed_completion_date"]).days > 0
            and not item.get("exception_approved", False)
        ]
        assert not overdue, (
            f"CA-5: {len(overdue)} critical/high-risk POA&M item(s) past committed "
            f"completion date without approved exception: "
            f"{[i.get('finding_id', i.get('title')) for i in overdue]}."
        )

    def test_poam_updated_quarterly(
        self, controls_evidence: dict, reference_date: date, odp_values: dict
    ):
        """DETERMINISTIC: POA&M must be reviewed and updated at least quarterly."""
        update_months = odp_values.get("ca5_update_months", CA5_UPDATE_MONTHS)
        last_update = controls_evidence.get("poam_last_update_date")
        if not last_update:
            pytest.fail("CA-5: POA&M has no recorded update date.")
        months_since = (reference_date.year - last_update.year) * 12 + \
                       (reference_date.month - last_update.month)
        assert months_since <= update_months, (
            f"CA-5: POA&M last updated {months_since} months ago; must update "
            f"≤{update_months} months."
        )


class TestCA7ContinuousMonitoring:
    """CA-7: Continuous Monitoring — Moderate/High [M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-CA-003",
        description=(
            "CA-7 ConMon ODP: vulnerability scanning monthly for OS/infrastructure; "
            "monitoring events and frequencies must be documented in a ConMon strategy. "
            "FedRAMP tightens this with specific scan frequency requirements "
            "(handled in fedramp/conmon-and-overlays.md)."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_continuous_monitoring_strategy_documented(self, controls_evidence: dict, impact_level):
        """PARAMETERIZED: a continuous monitoring strategy must be documented."""
        if impact_level == "low":
            pytest.skip("CA-7 formal ConMon strategy applies at Moderate/High")
        assert controls_evidence.get("continuous_monitoring_strategy_documented", False), (
            "CA-7: no continuous monitoring strategy documented in security plan."
        )

    def test_vulnerability_scans_monthly(
        self, controls_evidence: dict, reference_date: date, odp_values: dict, impact_level
    ):
        """DETERMINISTIC: OS/infrastructure vulnerability scans at least monthly at Moderate/High."""
        if impact_level == "low":
            pytest.skip("CA-7 monthly scanning applies at Moderate/High")
        max_months = odp_values.get("ca7_vuln_scan_months", CA7_VULN_SCAN_MONTHS)
        last_scan = controls_evidence.get("last_os_infrastructure_scan_date")
        if not last_scan:
            pytest.fail("CA-7: no OS/infrastructure vulnerability scan date documented.")
        months_since = (reference_date.year - last_scan.year) * 12 + \
                       (reference_date.month - last_scan.month)
        assert months_since <= max_months, (
            f"CA-7: last OS/infra scan {months_since} months ago; ODP requires ≤{max_months} month(s)."
        )

    def test_conmon_strategy_reviewed_annually(
        self, controls_evidence: dict, reference_date: date, impact_level
    ):
        """DETERMINISTIC: ConMon strategy must be reviewed within 12 months."""
        if impact_level == "low":
            pytest.skip("CA-7 ConMon strategy review applies at Moderate/High")
        last_review = controls_evidence.get("conmon_strategy_last_review_date")
        if not last_review:
            pytest.fail("CA-7: ConMon strategy review date not documented.")
        months_since = (reference_date.year - last_review.year) * 12 + \
                       (reference_date.month - last_review.month)
        assert months_since <= CA7_CONMON_PLAN_REVIEW_MONTHS, (
            f"CA-7: ConMon strategy last reviewed {months_since} months ago; "
            f"must review within {CA7_CONMON_PLAN_REVIEW_MONTHS} months."
        )


class TestCA8PenetrationTesting:
    """CA-8: Penetration Testing — High [H] (Moderate: per org ODP)"""

    @pytest.mark.assumption(
        id="ASSUME-800053-CA-004",
        description=(
            "CA-8 pentest ODP: annual at High (800-53B default); Moderate: org-defined "
            "frequency (annual recommended). Must cover network, application, and OS layers. "
            "FedRAMP requires 3PAO-conducted test annually for Moderate/High "
            "(handled in fedramp/conmon-and-overlays.md)."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_penetration_test_conducted(
        self, controls_evidence: dict, reference_date: date, odp_values: dict, impact_level
    ):
        """PARAMETERIZED: penetration test must have been conducted within ODP interval."""
        if impact_level == "low":
            pytest.skip("CA-8 penetration testing applies at High; optional at Moderate")
        test_months = odp_values.get("ca8_pentest_months", CA8_TEST_MONTHS)
        last_test = controls_evidence.get("last_penetration_test_date")
        if not last_test:
            pytest.fail(
                f"CA-8: no penetration test conducted (required for {impact_level} baseline)."
            )
        months_since = (reference_date.year - last_test.year) * 12 + \
                       (reference_date.month - last_test.month)
        assert months_since <= test_months, (
            f"CA-8: last pentest {months_since} months ago; ODP requires ≤{test_months} months."
        )

    def test_penetration_test_scope_covers_required_layers(
        self, controls_evidence: dict, impact_level
    ):
        """DETERMINISTIC: pentest must cover network, application, and OS layers."""
        if impact_level == "low":
            pytest.skip("CA-8 scope requirement applies at High")
        pentest_scope = set(controls_evidence.get("last_pentest_scope", []))
        required_layers = {"network", "application", "operating_system"}
        missing_layers = required_layers - pentest_scope
        assert not missing_layers, (
            f"CA-8: last penetration test did not cover required layers: {missing_layers}."
        )
```

---

## Assumption registry

| ID | Family/Control | Summary | Review date |
|---|---|---|---|
| ASSUME-800053-CP-001 | CP-2 | Contingency plan review ODP: annual (12 months) per 800-53B Moderate default | 2026-05-21 |
| ASSUME-800053-CP-002 | CP-3 | Training frequency ODP: annual at Moderate; semi-annual at High | 2026-05-21 |
| ASSUME-800053-CP-003 | CP-4 | Test frequency ODP: annual; High requires functional or full-interruption test | 2026-05-21 |
| ASSUME-800053-CP-004 | CP-9 | Backup frequency ODPs: daily user-level, weekly system-level; annual restoration test; offsite copies | 2026-05-21 |
| ASSUME-800053-IR-001 | IR-2 | IR training ODP: annual at Moderate; semi-annual at High; role-based for IR personnel | 2026-05-21 |
| ASSUME-800053-IR-002 | IR-3 | IR test ODP: annual at Moderate; semi-annual at High; tabletop or functional acceptable | 2026-05-21 |
| ASSUME-800053-IR-003 | IR-6 | Reporting ODP: within 1 hour of confirmed incident; reporting authority documented in SSP | 2026-05-21 |
| ASSUME-800053-CA-001 | CA-2 | Assessment frequency ODP: triennial (36 months) for Moderate/High; annual recommended for High | 2026-05-21 |
| ASSUME-800053-CA-002 | CA-5 | POA&M SLAs: critical ≤30d, high ≤90d; quarterly update; no overdue without approved exception | 2026-05-21 |
| ASSUME-800053-CA-003 | CA-7 | ConMon ODP: monthly OS/infra scans; ConMon strategy documented and reviewed annually | 2026-05-21 |
| ASSUME-800053-CA-004 | CA-8 | Pentest ODP: annual at High; org-defined at Moderate; network + application + OS layers | 2026-05-21 |

## Parse status: Partial — AU, AC, IA, CM, SC, SI, CP, IR, CA parsed (9 of 20 families); MA, MP, PE, PS, PL, RA, SA, SR, AT, PM, PT remaining
