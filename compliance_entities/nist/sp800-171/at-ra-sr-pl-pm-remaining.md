# NIST SP 800-171 r3 — Remaining Families: AT, RA, SR, PL, PM

**Source:** NIST SP 800-171 Rev 3 (Final, May 2024)
**Coverage:** Awareness & Training (3.2), Risk Assessment (3.11), Supply Chain (3.17),
  Planning (3.18), Program Management (3.x r3 additions)
**Design note:** These families have lower DETERMINISTIC density than AC/IA/AU/CM/SC/SI.
  AT has cadence thresholds. RA has scan frequency. SR and PM are predominantly
  CONTESTED. All tests are gated by the standard CUI scope fixture.

**Applies to:** Non-federal organizations (contractors, universities, research institutions) that process, store, or transmit Controlled Unclassified Information (CUI) in nonfederal information systems under US federal contracts or grants
**Trigger:** Federal contract or grant containing DFARS clause 252.204-7012 (DoD) or equivalent FAR clause; any contract where the government provides or the contractor generates CUI; CMMC Level 2 requires third-party assessment against NIST 800-171
**Jurisdiction:** United States; extraterritorial — applies to foreign companies holding US federal contracts involving CUI; enforced through contract terms and DoD CMMC assessments
**Not applicable to:** Federal agencies (use NIST 800-53 instead); organizations with no federal contracts or grants; commercial transactions not involving CUI; EAR99 technology transfers (separate ITAR/EAR framework)

---

```python
import pytest
from datetime import date, timedelta
from typing import FrozenSet, Optional

# ── AT — Awareness and Training ───────────────────────────────────────────────

# 3.2.1: Security awareness training frequency
AT_AWARENESS_TRAINING_MONTHS = 12          # annual minimum; role-based as needed
AT_NEW_USER_TRAINING_DAYS = 30             # before or within 30 days of initial CUI access

# 3.2.2: Role-based training — roles that require additional training
AT_ROLES_REQUIRING_SPECIALIZED_TRAINING: FrozenSet[str] = frozenset({
    "system_administrator",
    "security_engineer",
    "incident_responder",
    "software_developer",
    "privileged_user",
    "cui_handler",
})
AT_ROLE_BASED_TRAINING_MONTHS = 12        # role-based training refreshed annually

# 3.2.3: Insider threat awareness — must be included in awareness training
AT_INSIDER_THREAT_COVERED_REQUIRED = True

# ── RA — Risk Assessment ──────────────────────────────────────────────────────

# 3.11.1: Risk assessment — must be conducted; methodology documented
RA_ASSESSMENT_MONTHS = 36                  # triennial or when significant change (standard practice)
RA_VULNERABILITY_SCAN_MONTHS = 3          # quarterly scans (800-171A assessment objective)
RA_INTERNET_FACING_SCAN_MONTHS = 1        # monthly for internet-accessible systems
RA_CRITICAL_REMEDIATION_DAYS = 30         # CVSS ≥9.0
RA_HIGH_REMEDIATION_DAYS = 90             # CVSS 7.0–8.9

# 3.11.3: Remediate vulnerabilities — track open findings, prioritize by risk
RA_VULN_TRACKING_SYSTEM_REQUIRED = True

# ── SR — Supply Chain Risk Management ─────────────────────────────────────────

# 3.17.1: Supply chain risk management plan
SR_PLAN_REQUIRED = True
SR_PLAN_REVIEW_MONTHS = 12                # annual review
SR_CRITICAL_SUPPLIER_REVIEW_MONTHS = 12  # annual supplier assessment

# 3.17.2: Component authenticity — hardware/software from authorized sources
SR_COMPONENT_AUTHENTICITY_REQUIRED = True

# 3.17.3: Prevent counterfeit components
SR_ANTI_COUNTERFEIT_MEASURES = frozenset({
    "purchase_from_authorized_distributors",
    "component_inspection_upon_receipt",
    "component_provenance_documentation",
})

# 3.17.4: Notify of supply chain incidents
SR_INCIDENT_NOTIFY_REQUIRED = True

# ── PL — Planning ─────────────────────────────────────────────────────────────

# 3.18.1: System Security Plan (SSP)
PL_SSP_REQUIRED = True
PL_SSP_REVIEW_MONTHS = 12                 # reviewed and updated at least annually

# SSP required sections (per NIST 800-171A assessment objectives)
PL_SSP_REQUIRED_SECTIONS: FrozenSet[str] = frozenset({
    "system_description",
    "system_boundary",
    "cui_flows",
    "security_requirements_implementation_status",
    "interconnections_and_dependencies",
    "roles_and_responsibilities",
    "assessment_and_authorization_dates",
})

# ── PM — Program Management (r3 additions) ────────────────────────────────────

# r3 added PM requirements for senior leadership accountability
PM_SENIOR_OFFICIAL_DESIGNATED = True      # named individual accountable for CUI security
PM_PROGRAM_PLAN_REQUIRED = True           # documented security program plan
PM_RESOURCE_ALLOCATION_DOCUMENTED = True  # budget/resources for security requirements

# ── Scope fixture ─────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def cui_scope_check(entity_profile: dict):
    """Skip if system does not process, store, or transmit CUI."""
    if not entity_profile.get("system_processes_cui", False):
        pytest.skip("System does not process CUI — 800-171 not applicable")


# ═══════════════════════════════════════════════════════════════════════════════
# AWARENESS AND TRAINING (AT)
# ═══════════════════════════════════════════════════════════════════════════════

class TestAT321SecurityAwarenessTraining:
    """3.2.1: Ensure all individuals with CUI access receive awareness training."""

    def test_annual_awareness_training_completed(
        self, controls_evidence: dict, reference_date: date
    ):
        """DETERMINISTIC: all CUI-access personnel must complete training within 12 months."""
        users_without_training = [
            u for u in controls_evidence.get("user_training_records", [])
            if u.get("has_cui_access", False)
            and (
                not u.get("last_training_date")
                or (reference_date - u["last_training_date"]).days >
                   AT_AWARENESS_TRAINING_MONTHS * 30
            )
        ]
        assert not users_without_training, (
            f"AT 3.2.1: {len(users_without_training)} user(s) with CUI access lack current "
            f"(≤{AT_AWARENESS_TRAINING_MONTHS} months) security awareness training: "
            f"{[u.get('user_id') for u in users_without_training[:10]]}."
        )

    def test_new_user_training_completed_timely(self, controls_evidence: dict):
        """DETERMINISTIC: new users must complete training before or within 30 days of CUI access."""
        late_onboards = [
            u for u in controls_evidence.get("recent_onboarding_records", [])
            if u.get("days_to_training_completion", 0) > AT_NEW_USER_TRAINING_DAYS
        ]
        assert not late_onboards, (
            f"AT 3.2.1: {len(late_onboards)} new user(s) did not complete security awareness "
            f"training within {AT_NEW_USER_TRAINING_DAYS} days of CUI access: "
            f"{[u.get('user_id') for u in late_onboards]}."
        )


class TestAT322RoleBasedTraining:
    """3.2.2: Provide role-based training for personnel with security responsibilities."""

    @pytest.mark.assumption(
        id="ASSUME-800171-AT-001",
        description=(
            "AT 3.2.2: role-based training required annually for 6 identified high-risk roles "
            "(sysadmin, security engineer, IR, dev, privileged user, CUI handler). "
            "Training content adequacy is PARAMETERIZED."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_role_based_training_completed_for_required_roles(
        self, controls_evidence: dict, reference_date: date
    ):
        """PARAMETERIZED: role-based training completed within 12 months for all required roles."""
        roles_without_training = [
            r for r in controls_evidence.get("role_based_training_records", [])
            if r.get("role", "").lower() in AT_ROLES_REQUIRING_SPECIALIZED_TRAINING
            and (
                not r.get("last_training_date")
                or (reference_date - r["last_training_date"]).days >
                   AT_ROLE_BASED_TRAINING_MONTHS * 30
            )
        ]
        assert not roles_without_training, (
            f"AT 3.2.2: role-based training overdue for {len(roles_without_training)} "
            f"role assignment(s): "
            f"{[(r.get('user_id'), r.get('role')) for r in roles_without_training[:10]]}."
        )


class TestAT323InsiderThreatAwareness:
    """3.2.3: Include insider threat awareness in security awareness training."""

    def test_insider_threat_covered_in_training(self, controls_evidence: dict):
        """DETERMINISTIC: security awareness training must include insider threat content."""
        training_content = set(
            controls_evidence.get("awareness_training_topics_covered", [])
        )
        assert "insider_threat" in training_content, (
            "AT 3.2.3: insider threat awareness not included in security awareness training content."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# RISK ASSESSMENT (RA)
# ═══════════════════════════════════════════════════════════════════════════════

class TestRA3111RiskAssessment:
    """3.11.1: Periodically assess the risk to organizational operations from CUI system operation."""

    @pytest.mark.assumption(
        id="ASSUME-800171-RA-001",
        description=(
            "RA 3.11.1: risk assessment conducted at least every 36 months or after significant "
            "system changes. Assessment must document threat sources, likelihood, impact, and risk. "
            "Risk methodology acceptability is CONTESTED — assessor-evaluated."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_risk_assessment_conducted_within_36_months(
        self, controls_evidence: dict, reference_date: date
    ):
        """PARAMETERIZED: risk assessment must be current (within 36 months or last significant change)."""
        last_ra = controls_evidence.get("last_risk_assessment_date")
        if not last_ra:
            pytest.fail("RA 3.11.1: no risk assessment date documented.")
        months_since = (reference_date.year - last_ra.year) * 12 + \
                       (reference_date.month - last_ra.month)
        assert months_since <= RA_ASSESSMENT_MONTHS, (
            f"RA 3.11.1: last risk assessment {months_since} months ago; must be ≤{RA_ASSESSMENT_MONTHS} months."
        )

    @pytest.mark.human_review_required(
        reason=(
            "RA 3.11.1: risk assessment methodology adequacy is CONTESTED. "
            "Methodology must document threat sources, likelihood, impact, and risk level, "
            "but what constitutes 'adequate' methodology is assessed by the DoD contracting "
            "officer or CMMC assessor — not determinable by automated test."
        )
    )
    def test_risk_assessment_methodology_adequacy(self, controls_evidence: dict):
        """CONTESTED: risk assessment methodology must be documented and meet assessor criteria."""
        assert controls_evidence.get("risk_assessment_methodology_documented", False), (
            "RA 3.11.1: risk assessment methodology not documented in SSP."
        )


class TestRA3112VulnerabilityScanning:
    """3.11.2: Scan for vulnerabilities in the system and applications periodically."""

    @pytest.mark.assumption(
        id="ASSUME-800171-RA-002",
        description=(
            "RA 3.11.2: quarterly scans (every 90 days) for general systems; monthly for "
            "internet-facing systems. Critical (CVSS≥9.0) remediated ≤30 days; "
            "high (7.0–8.9) ≤90 days. Scan must be authenticated."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_vulnerability_scan_cadence(
        self, controls_evidence: dict, reference_date: date
    ):
        """PARAMETERIZED: vulnerability scans must occur at least quarterly."""
        last_scan = controls_evidence.get("last_vulnerability_scan_date")
        if not last_scan:
            pytest.fail("RA 3.11.2: no vulnerability scan date documented.")
        months_since = (reference_date.year - last_scan.year) * 12 + \
                       (reference_date.month - last_scan.month)
        assert months_since <= RA_VULNERABILITY_SCAN_MONTHS, (
            f"RA 3.11.2: last vulnerability scan {months_since} months ago; "
            f"must scan ≤{RA_VULNERABILITY_SCAN_MONTHS} months."
        )

    def test_internet_facing_scan_monthly(
        self, controls_evidence: dict, reference_date: date
    ):
        """DETERMINISTIC: internet-facing systems must be scanned monthly."""
        has_internet_facing = controls_evidence.get("has_internet_facing_systems", False)
        if not has_internet_facing:
            pytest.skip("No internet-facing CUI systems — monthly scan not applicable")
        last_scan = controls_evidence.get("last_internet_facing_scan_date")
        if not last_scan:
            pytest.fail("RA 3.11.2: no internet-facing scan date documented.")
        months_since = (reference_date.year - last_scan.year) * 12 + \
                       (reference_date.month - last_scan.month)
        assert months_since <= RA_INTERNET_FACING_SCAN_MONTHS, (
            f"RA 3.11.2: last internet-facing scan {months_since} months ago; "
            f"must scan ≤{RA_INTERNET_FACING_SCAN_MONTHS} month."
        )

    def test_no_overdue_critical_vulnerabilities(
        self, controls_evidence: dict, reference_date: date
    ):
        """DETERMINISTIC: critical vulnerabilities (CVSS ≥9.0) must be remediated within 30 days."""
        overdue = [
            v for v in controls_evidence.get("open_vulnerabilities", [])
            if v.get("cvss_score", 0) >= 9.0
            and (reference_date - v["first_detected"]).days > RA_CRITICAL_REMEDIATION_DAYS
        ]
        assert not overdue, (
            f"RA 3.11.2: {len(overdue)} critical vulnerability/ies unpatched beyond "
            f"{RA_CRITICAL_REMEDIATION_DAYS}-day SLA: "
            f"{[v.get('cve_id', v.get('title')) for v in overdue]}."
        )

    def test_no_overdue_high_vulnerabilities(
        self, controls_evidence: dict, reference_date: date
    ):
        """DETERMINISTIC: high vulnerabilities (CVSS 7.0–8.9) must be remediated within 90 days."""
        overdue = [
            v for v in controls_evidence.get("open_vulnerabilities", [])
            if 7.0 <= v.get("cvss_score", 0) < 9.0
            and (reference_date - v["first_detected"]).days > RA_HIGH_REMEDIATION_DAYS
        ]
        assert not overdue, (
            f"RA 3.11.2: {len(overdue)} high-severity vulnerability/ies unpatched beyond "
            f"{RA_HIGH_REMEDIATION_DAYS}-day SLA."
        )


class TestRA3113RemediateVulnerabilities:
    """3.11.3: Remediate vulnerabilities in accordance with risk assessments."""

    def test_vulnerability_tracking_system_exists(self, controls_evidence: dict):
        """DETERMINISTIC: an active vulnerability tracking system must be in use."""
        assert controls_evidence.get("vulnerability_tracking_system_in_use", False), (
            "RA 3.11.3: no vulnerability tracking system documented — cannot demonstrate "
            "risk-based remediation prioritization."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SUPPLY CHAIN RISK MANAGEMENT (SR)
# ═══════════════════════════════════════════════════════════════════════════════

class TestSR3171SupplyChainRiskManagementPlan:
    """3.17.1: Establish and maintain a supply chain risk management (SCRM) plan."""

    def test_scrm_plan_documented(self, controls_evidence: dict):
        """DETERMINISTIC: a documented SCRM plan must exist."""
        assert controls_evidence.get("scrm_plan_documented", False), (
            "SR 3.17.1: no supply chain risk management plan documented."
        )

    def test_scrm_plan_reviewed_annually(
        self, controls_evidence: dict, reference_date: date
    ):
        """DETERMINISTIC: SCRM plan must be reviewed within 12 months."""
        last_review = controls_evidence.get("scrm_plan_last_review_date")
        if not last_review:
            pytest.fail("SR 3.17.1: SCRM plan review date not documented.")
        months_since = (reference_date.year - last_review.year) * 12 + \
                       (reference_date.month - last_review.month)
        assert months_since <= SR_PLAN_REVIEW_MONTHS, (
            f"SR 3.17.1: SCRM plan last reviewed {months_since} months ago; "
            f"must review ≤{SR_PLAN_REVIEW_MONTHS} months."
        )

    @pytest.mark.human_review_required(
        reason=(
            "SR 3.17.1: SCRM plan content adequacy is CONTESTED. "
            "The plan must address critical components, supplier vetting, and incident response, "
            "but what constitutes 'adequate' supply chain controls is evaluated by the "
            "CMMC assessor or DoD contracting officer and cannot be reduced to an automated assertion."
        )
    )
    def test_scrm_plan_content_adequacy(self, controls_evidence: dict):
        """CONTESTED: SCRM plan must address critical component identification, supplier vetting, and SCR incident response."""
        has_required_sections = all([
            controls_evidence.get("scrm_identifies_critical_components", False),
            controls_evidence.get("scrm_documents_supplier_vetting_criteria", False),
            controls_evidence.get("scrm_includes_incident_response", False),
        ])
        assert has_required_sections, (
            "SR 3.17.1: SCRM plan is missing one or more required sections "
            "(critical components, supplier vetting criteria, SC incident response)."
        )


class TestSR3172ComponentAuthenticity:
    """3.17.2: Employ safeguards to ensure authenticity of components delivered to the organization."""

    @pytest.mark.assumption(
        id="ASSUME-800171-SR-001",
        description=(
            "SR 3.17.2: component authenticity safeguards require purchase from authorized "
            "distributors and receipt inspection. Adequacy of counterfeit prevention measures "
            "is PARAMETERIZED — specific controls must be documented in the SCRM plan."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_component_authenticity_safeguards_documented(self, controls_evidence: dict):
        """PARAMETERIZED: anti-counterfeit safeguards must be documented in the SCRM plan."""
        safeguards = set(controls_evidence.get("component_authenticity_safeguards_in_use", []))
        if not safeguards:
            pytest.fail(
                "SR 3.17.2: no component authenticity safeguards documented. "
                f"Must include safeguards from: {SR_ANTI_COUNTERFEIT_MEASURES}."
            )

    def test_components_from_authorized_sources(self, controls_evidence: dict):
        """DETERMINISTIC: ICT components must be acquired from authorized/trusted sources."""
        assert controls_evidence.get("ict_components_sourced_from_authorized_distributors", False), (
            "SR 3.17.2: no documentation that ICT components are sourced from authorized distributors."
        )


class TestSR3173PreventCounterfeit:
    """3.17.3: Employ safeguards to prevent counterfeit components entering the supply chain."""

    def test_receipt_inspection_process_exists(self, controls_evidence: dict):
        """DETERMINISTIC: a documented component inspection process must exist for received ICT items."""
        assert controls_evidence.get("ict_component_inspection_on_receipt_documented", False), (
            "SR 3.17.3: no documented inspection process for ICT components received from suppliers."
        )


class TestSR3174SupplyChainIncidentNotification:
    """3.17.4: Respond to and report supply chain incidents."""

    @pytest.mark.human_review_required(
        reason=(
            "SR 3.17.4: supply chain incident response adequacy is CONTESTED. "
            "The process must document notification recipients, timelines, and remediation steps, "
            "but the determination that a supply chain event constitutes a 'reportable incident' "
            "and that the response was adequate is assessor-evaluated."
        )
    )
    def test_scrm_incident_response_process_exists(self, controls_evidence: dict):
        """CONTESTED: a supply chain incident response process must be documented."""
        assert controls_evidence.get("scrm_incident_response_process_documented", False), (
            "SR 3.17.4: no supply chain incident response process documented."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# PLANNING (PL)
# ═══════════════════════════════════════════════════════════════════════════════

class TestPL3181SystemSecurityPlan:
    """3.18.1: Develop, document, and periodically update system security plans (SSPs)."""

    def test_ssp_documented(self, controls_evidence: dict):
        """DETERMINISTIC: an SSP must be documented for the CUI system."""
        assert controls_evidence.get("ssp_documented", False), (
            "PL 3.18.1: no System Security Plan (SSP) documented for this CUI system."
        )

    def test_ssp_contains_required_sections(self, controls_evidence: dict):
        """DETERMINISTIC: SSP must contain all required sections per 800-171A."""
        ssp_sections = set(controls_evidence.get("ssp_sections_present", []))
        missing = PL_SSP_REQUIRED_SECTIONS - ssp_sections
        assert not missing, (
            f"PL 3.18.1: SSP missing required sections: {missing}."
        )

    @pytest.mark.assumption(
        id="ASSUME-800171-PL-001",
        description=(
            "PL 3.18.1: SSP reviewed and updated at least annually or after significant changes. "
            "SSP completeness ('describes how security requirements are met') is PARAMETERIZED — "
            "an assessor determines whether implementation descriptions are sufficient."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_ssp_reviewed_annually(
        self, controls_evidence: dict, reference_date: date
    ):
        """PARAMETERIZED: SSP must be reviewed within 12 months."""
        last_review = controls_evidence.get("ssp_last_review_date")
        if not last_review:
            pytest.fail("PL 3.18.1: SSP has no recorded review date.")
        months_since = (reference_date.year - last_review.year) * 12 + \
                       (reference_date.month - last_review.month)
        assert months_since <= PL_SSP_REVIEW_MONTHS, (
            f"PL 3.18.1: SSP last reviewed {months_since} months ago; "
            f"must review ≤{PL_SSP_REVIEW_MONTHS} months."
        )

    @pytest.mark.human_review_required(
        reason=(
            "PL 3.18.1: SSP completeness is CONTESTED. The requirement to 'describe how security "
            "requirements are met or planned to be met' is an assessor judgment — the level of "
            "implementation detail required cannot be verified by automated inspection of "
            "evidence metadata alone."
        )
    )
    def test_ssp_describes_requirement_implementation(self, controls_evidence: dict):
        """CONTESTED: SSP must describe how each security requirement is met or planned to be met."""
        assert controls_evidence.get("ssp_describes_implementation_for_all_requirements", False), (
            "PL 3.18.1: SSP does not document implementation status for all 800-171 requirements."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# PROGRAM MANAGEMENT (PM — r3 additions)
# ═══════════════════════════════════════════════════════════════════════════════

class TestPMSeniorLeadershipAccountability:
    """r3 additions: Program management requirements for senior leadership accountability."""

    def test_senior_official_designated(self, controls_evidence: dict):
        """DETERMINISTIC: a named senior official must be accountable for CUI security."""
        assert controls_evidence.get("senior_official_for_cui_security_designated", False), (
            "PM (r3): no senior official designated as accountable for CUI security program."
        )

    @pytest.mark.human_review_required(
        reason=(
            "PM (r3): program management sufficiency is CONTESTED. Whether the senior official "
            "has adequate authority, the program plan is sufficiently resourced, and security "
            "activities are appropriately coordinated are all management-maturity judgments "
            "that require assessor evaluation — not reducible to evidence field checks."
        )
    )
    def test_security_program_plan_adequacy(self, controls_evidence: dict):
        """CONTESTED: a documented security program plan with resource allocation must exist."""
        has_plan = controls_evidence.get("security_program_plan_documented", False)
        has_resources = controls_evidence.get("security_resources_budgeted", False)
        assert has_plan and has_resources, (
            "PM (r3): security program plan not documented or security resource allocation "
            "not documented."
        )
```

---

## Assumption registry

| ID | Family/Req | Summary | Review date |
|---|---|---|---|
| ASSUME-800171-AT-001 | AT 3.2.2 | Role-based training annually for 6 required roles; training content adequacy is PARAMETERIZED | 2026-05-21 |
| ASSUME-800171-RA-001 | RA 3.11.1 | Risk assessment: triennial (≤36 months) or after significant change; methodology adequacy is CONTESTED | 2026-05-21 |
| ASSUME-800171-RA-002 | RA 3.11.2 | Vuln scans: quarterly for all; monthly for internet-facing; critical ≤30d, high ≤90d; authenticated scans required | 2026-05-21 |
| ASSUME-800171-SR-001 | SR 3.17.2 | Component authenticity: purchase from authorized distributors; receipt inspection; adequacy PARAMETERIZED | 2026-05-21 |
| ASSUME-800171-PL-001 | PL 3.18.1 | SSP annual review; contains 7 required sections; completeness is CONTESTED (assessor-evaluated) | 2026-05-21 |

## Contested items

| Item | Req | Reason |
|---|---|---|
| Risk assessment methodology adequacy | RA 3.11.1 | Methodology sufficiency is assessed by DoD CO or CMMC assessor; no objective bright-line |
| SCRM plan content adequacy | SR 3.17.1 | Supply chain control depth is assessor-evaluated; NIST 800-161 provides criteria but not thresholds |
| Supply chain incident response adequacy | SR 3.17.4 | Determination of what constitutes reportable SC incident is judgment-based |
| SSP completeness | PL 3.18.1 | Level of implementation detail required is assessor-evaluated |
| PM program sufficiency | PM (r3) | Program maturity (authority, resourcing, coordination) requires management-level assessment |

## Parse status: Complete — all 17 families parsed (AC, AT, AU, CA, CM, IA, IR, MA, MP, PE, PL, PM, PS, RA, SC, SI, SR); ~117 requirements covered
