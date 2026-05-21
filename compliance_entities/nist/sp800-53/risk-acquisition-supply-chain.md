# NIST SP 800-53 r5 — Risk Assessment, System/Services Acquisition, Supply Chain Risk Management

**Source:** NIST SP 800-53 Rev 5 + 800-53B baselines
**Coverage:** RA (10 base), SA (23 base), SR (12 base)
**Baseline tags:** `[L]` Low, `[M]` Moderate, `[H]` High
**Note:** RA and SR have significant CONTESTED surfaces (methodology/adequacy). SA developer
  security tests are primarily PARAMETERIZED. DETERMINISTIC tests cover presence and cadence.

---

```python
import pytest
from datetime import date, timedelta
from typing import FrozenSet

# ── RA — Risk Assessment ──────────────────────────────────────────────────────

# RA-2: Security categorization — FIPS 199 required before any baseline selection
RA2_FIPS199_CATEGORIZATION_REQUIRED = True

# RA-3: Risk assessment — documented, periodic
RA3_ASSESSMENT_MONTHS = 36              # triennial or after significant change
RA3_REQUIRED_ELEMENTS: FrozenSet[str] = frozenset({
    "threat_sources",
    "threat_events",
    "likelihood_determination",
    "impact_determination",
    "risk_determination",
})

# RA-5: Vulnerability monitoring and scanning
RA5_SCAN_MONTHS = 1                     # monthly [M][H] (800-53B default ODP)
RA5_QUARTERLY_SCAN_MONTHS = 3          # quarterly acceptable for Low
RA5_AUTHENTICATED_SCAN_REQUIRED = True  # Moderate/High: authenticated scans required
RA5_CRITICAL_PATCH_DAYS = 30           # CVSS ≥9.0
RA5_HIGH_PATCH_DAYS = 90               # CVSS 7.0–8.9

# RA-7: Risk response — documented response actions for identified risks
RA7_RISK_RESPONSE_DOCUMENTED = True

# ── SA — System and Services Acquisition ─────────────────────────────────────

# SA-4: Acquisition process — security requirements in contracts
SA4_SECURITY_REQUIREMENTS_IN_CONTRACTS = True

# SA-8: Security and privacy engineering principles
SA8_ENGINEERING_PRINCIPLES_DOCUMENTED = True  # [M][H]

# SA-9: External system services — inventory and requirements
SA9_EXTERNAL_SERVICES_INVENTORY_REQUIRED = True
SA9_REVIEW_MONTHS = 12                  # annual review of external service inventory

# SA-10: Developer configuration management
SA10_CONFIG_MGMT_REQUIRED_FOR_DEV = True  # [M][H]: developers must use SCM/version control

# SA-11: Developer testing and evaluation — Moderate/High
SA11_DEV_TESTING_REQUIRED = True
SA11_REQUIRED_TESTING_TYPES: FrozenSet[str] = frozenset({
    "unit_testing",
    "integration_testing",
    "regression_testing",
    "security_testing",
})
SA11_FLAW_REMEDIATION_PROCESS = True

# SA-15: Development process, standards, and tools
SA15_DEVELOPMENT_PROCESS_DOCUMENTED = True  # [H]

# ── SR — Supply Chain Risk Management ────────────────────────────────────────

# SR-1: Policy and procedures
SR1_SCRM_POLICY_REQUIRED = True

# SR-2: Supply chain risk management plan
SR2_PLAN_REQUIRED = True
SR2_PLAN_REVIEW_MONTHS = 12

# SR-3: Supply chain controls and processes
SR3_CRITICAL_SUPPLIERS_IDENTIFIED = True
SR3_SUPPLIER_VETTING_DOCUMENTED = True

# SR-5: Acquisition strategies and tools
SR5_ACQUISITION_STRATEGY_DOCUMENTED = True

# SR-11: Component authenticity
SR11_AUTHENTICITY_VERIFICATION_REQUIRED = True  # Moderate/High
SR11_ACCEPTABLE_VERIFICATION_METHODS = frozenset({
    "cryptographic_signature_verification",
    "certificate_of_conformance_from_authorized_distributor",
    "bill_of_materials_verification",
    "nist_nsf_hardware_bill_of_materials",
})

# SR-12: Component disposal
SR12_DISPOSAL_DOCUMENTED = True
SR12_CLASSIFIED_COMPONENT_DISPOSAL_REQUIRES_APPROVAL = True

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
# RISK ASSESSMENT (RA)
# ═══════════════════════════════════════════════════════════════════════════════

class TestRA2SecurityCategorization:
    """RA-2: Security Categorization — all baselines [L][M][H]"""

    def test_fips199_categorization_documented(self, controls_evidence: dict):
        """DETERMINISTIC: system must have a documented FIPS 199 security categorization."""
        assert controls_evidence.get("fips199_categorization_documented", False), (
            "RA-2: no FIPS 199 security categorization documented for this system."
        )

    def test_categorization_reviewed_on_significant_change(self, controls_evidence: dict):
        """DETERMINISTIC: categorization must be reviewed when significant system changes occur."""
        assert controls_evidence.get("categorization_review_process_documented", False), (
            "RA-2: no documented process for reviewing FIPS 199 categorization after significant changes."
        )


class TestRA3RiskAssessment:
    """RA-3: Risk Assessment — all baselines [L][M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-RA-001",
        description=(
            "RA-3 assessment frequency ODP: triennial (36 months) per 800-53B Moderate; "
            "also required after significant system changes or incidents. Assessment must "
            "document threat sources, events, likelihood, impact, and risk determination."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_risk_assessment_conducted_within_interval(
        self, controls_evidence: dict, reference_date: date, odp_values: dict
    ):
        """PARAMETERIZED: risk assessment must be current per ODP interval."""
        max_months = odp_values.get("ra3_assessment_months", RA3_ASSESSMENT_MONTHS)
        last_ra = controls_evidence.get("last_risk_assessment_date")
        if not last_ra:
            pytest.fail("RA-3: no risk assessment date documented.")
        months_since = (reference_date.year - last_ra.year) * 12 + \
                       (reference_date.month - last_ra.month)
        assert months_since <= max_months, (
            f"RA-3: last risk assessment {months_since} months ago; "
            f"ODP requires ≤{max_months} months."
        )

    def test_risk_assessment_contains_required_elements(self, controls_evidence: dict):
        """DETERMINISTIC: risk assessment must document all five required elements."""
        present = set(controls_evidence.get("risk_assessment_elements_documented", []))
        missing = RA3_REQUIRED_ELEMENTS - present
        assert not missing, (
            f"RA-3: risk assessment missing required elements: {missing}."
        )

    @pytest.mark.human_review_required(
        reason=(
            "RA-3: risk assessment methodology adequacy is CONTESTED. The 'appropriateness' "
            "of threat sources, event selection, likelihood and impact determination methodology "
            "is an assessor judgment that varies by organization context and cannot be reduced "
            "to automated field checks."
        )
    )
    def test_risk_methodology_adequacy(self, controls_evidence: dict):
        """CONTESTED: risk methodology must be documented and assessor-reviewed."""
        assert controls_evidence.get("risk_assessment_methodology_documented", False), (
            "RA-3: risk assessment methodology not documented."
        )


class TestRA5VulnerabilityScanning:
    """RA-5: Vulnerability Monitoring and Scanning — all baselines [L][M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-RA-002",
        description=(
            "RA-5 scan frequency ODP: monthly for Moderate/High (800-53B default); "
            "quarterly acceptable for Low. Authenticated scans required for Moderate/High. "
            "Results shared with relevant personnel and incorporated into remediation."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_vulnerability_scans_current(
        self, controls_evidence: dict, reference_date: date, odp_values: dict, impact_level
    ):
        """PARAMETERIZED: vulnerability scans must be conducted within ODP interval."""
        if impact_level == "low":
            max_months = odp_values.get("ra5_scan_months_low", RA5_QUARTERLY_SCAN_MONTHS)
        else:
            max_months = odp_values.get("ra5_scan_months", RA5_SCAN_MONTHS)
        last_scan = controls_evidence.get("last_vulnerability_scan_date")
        if not last_scan:
            pytest.fail("RA-5: no vulnerability scan date documented.")
        months_since = (reference_date.year - last_scan.year) * 12 + \
                       (reference_date.month - last_scan.month)
        assert months_since <= max_months, (
            f"RA-5: last scan {months_since} months ago; ODP requires ≤{max_months} month(s) "
            f"for {impact_level}."
        )

    def test_authenticated_scans_used_moderate_high(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: authenticated vulnerability scans required at Moderate/High."""
        if impact_level == "low":
            pytest.skip("RA-5 authenticated scan requirement applies at Moderate/High")
        assert controls_evidence.get("vulnerability_scans_are_authenticated", False), (
            "RA-5: vulnerability scans are not authenticated (required at Moderate/High)."
        )

    def test_no_overdue_critical_vulnerabilities(
        self, controls_evidence: dict, reference_date: date, odp_values: dict
    ):
        """DETERMINISTIC: critical vulnerabilities must be patched within 30 days."""
        sla_days = odp_values.get("ra5_critical_patch_days", RA5_CRITICAL_PATCH_DAYS)
        overdue = [
            v for v in controls_evidence.get("open_vulnerabilities", [])
            if v.get("cvss_score", 0) >= 9.0
            and (reference_date - v["first_detected"]).days > sla_days
        ]
        assert not overdue, (
            f"RA-5: {len(overdue)} critical vulnerability/ies unpatched beyond {sla_days}-day SLA."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM AND SERVICES ACQUISITION (SA)
# ═══════════════════════════════════════════════════════════════════════════════

class TestSA4AcquisitionProcess:
    """SA-4: Acquisition Process — all baselines [L][M][H]"""

    def test_security_requirements_in_contracts(self, controls_evidence: dict):
        """DETERMINISTIC: security requirements must be included in acquisition contracts."""
        assert controls_evidence.get("security_requirements_included_in_contracts", False), (
            "SA-4: security requirements not documented as being included in acquisition contracts."
        )


class TestSA8SecurityEngineeringPrinciples:
    """SA-8: Security and Privacy Engineering Principles — Moderate/High [M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-SA-001",
        description=(
            "SA-8 engineering principles ODP: organization selects from NIST SP 800-160 v1/v2 "
            "or equivalent security engineering principles. Adequacy of selection and application "
            "is PARAMETERIZED — assessor-evaluated for whether principles are actually applied."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_security_engineering_principles_documented(
        self, controls_evidence: dict, impact_level
    ):
        """PARAMETERIZED: security engineering principles must be documented and applied."""
        if impact_level == "low":
            pytest.skip("SA-8 formal engineering principles apply at Moderate/High")
        assert controls_evidence.get("security_engineering_principles_documented", False), (
            "SA-8: no documented security engineering principles (e.g., NIST 800-160 based)."
        )


class TestSA9ExternalSystemServices:
    """SA-9: External System Services — all baselines [L][M][H]"""

    def test_external_services_inventory_maintained(self, controls_evidence: dict):
        """DETERMINISTIC: an inventory of external system services must be maintained."""
        assert controls_evidence.get("external_services_inventory_maintained", False), (
            "SA-9: no inventory of external system services maintained."
        )

    def test_external_services_security_requirements_documented(self, controls_evidence: dict):
        """DETERMINISTIC: security requirements for external services must be documented."""
        assert controls_evidence.get("external_services_security_requirements_documented", False), (
            "SA-9: security requirements for external system services not documented."
        )

    def test_external_services_inventory_reviewed_annually(
        self, controls_evidence: dict, reference_date: date
    ):
        """DETERMINISTIC: external services inventory must be reviewed within 12 months."""
        last_review = controls_evidence.get("external_services_inventory_last_review_date")
        if not last_review:
            pytest.fail("SA-9: external services inventory has no review date.")
        months_since = (reference_date.year - last_review.year) * 12 + \
                       (reference_date.month - last_review.month)
        assert months_since <= SA9_REVIEW_MONTHS, (
            f"SA-9: external services inventory last reviewed {months_since} months ago; "
            f"must review within {SA9_REVIEW_MONTHS} months."
        )


class TestSA10DeveloperConfigurationManagement:
    """SA-10: Developer Configuration Management — Moderate/High [M][H]"""

    def test_developer_configuration_management_required(
        self, controls_evidence: dict, impact_level
    ):
        """DETERMINISTIC: developers must use configuration management (source control)."""
        if impact_level == "low":
            pytest.skip("SA-10 developer CM applies at Moderate/High")
        assert controls_evidence.get("developer_scm_in_use", False), (
            "SA-10: developers not documented as using source code/configuration management."
        )

    def test_developer_change_tracking_documented(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: changes to system/software during development must be tracked."""
        if impact_level == "low":
            pytest.skip("SA-10 change tracking applies at Moderate/High")
        assert controls_evidence.get("developer_change_tracking_documented", False), (
            "SA-10: developer change tracking process not documented."
        )


class TestSA11DeveloperTestingAndEvaluation:
    """SA-11: Developer Testing and Evaluation — Moderate/High [M][H]"""

    @pytest.mark.assumption(
        id="ASSUME-800053-SA-002",
        description=(
            "SA-11 ODP: developer testing must include security testing; test plans and "
            "results available for review. Adequacy of testing depth and coverage is "
            "PARAMETERIZED — what constitutes adequate security testing is assessor-evaluated."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_developer_security_testing_plan_exists(
        self, controls_evidence: dict, impact_level
    ):
        """PARAMETERIZED: developer security testing plan must be documented."""
        if impact_level == "low":
            pytest.skip("SA-11 developer security testing applies at Moderate/High")
        assert controls_evidence.get("developer_security_testing_plan_documented", False), (
            "SA-11: no developer security testing plan documented."
        )

    def test_developer_testing_includes_security_testing(
        self, controls_evidence: dict, impact_level
    ):
        """DETERMINISTIC: developer testing must include security testing activities."""
        if impact_level == "low":
            pytest.skip("SA-11 security testing applies at Moderate/High")
        testing_types = set(controls_evidence.get("developer_testing_types_conducted", []))
        assert "security_testing" in testing_types, (
            "SA-11: developer testing does not include security testing."
        )

    @pytest.mark.human_review_required(
        reason=(
            "SA-11: adequacy of developer security testing coverage and depth is CONTESTED. "
            "What constitutes sufficient security testing (static analysis depth, pen test scope, "
            "coverage thresholds) varies by application risk level and is assessor-evaluated."
        )
    )
    def test_developer_testing_adequacy(self, controls_evidence: dict, impact_level):
        """CONTESTED: developer security testing must be adequate for the system risk level."""
        if impact_level == "low":
            pytest.skip("SA-11 adequacy review applies at Moderate/High")
        assert controls_evidence.get("developer_testing_results_reviewed", False), (
            "SA-11: developer testing results not documented as reviewed by the organization."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SUPPLY CHAIN RISK MANAGEMENT (SR)
# ═══════════════════════════════════════════════════════════════════════════════

class TestSR2SupplyChainRiskManagementPlan:
    """SR-2: Supply Chain Risk Management Plan — Moderate/High [M][H]"""

    def test_scrm_plan_documented(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: a documented SCRM plan must exist at Moderate/High."""
        if impact_level == "low":
            pytest.skip("SR-2 documented SCRM plan applies at Moderate/High")
        assert controls_evidence.get("scrm_plan_documented", False), (
            "SR-2: no supply chain risk management plan documented."
        )

    def test_scrm_plan_reviewed_annually(
        self, controls_evidence: dict, reference_date: date, impact_level
    ):
        """DETERMINISTIC: SCRM plan must be reviewed within 12 months."""
        if impact_level == "low":
            pytest.skip("SR-2 annual review applies at Moderate/High")
        last_review = controls_evidence.get("scrm_plan_last_review_date")
        if not last_review:
            pytest.fail("SR-2: SCRM plan review date not documented.")
        months_since = (reference_date.year - last_review.year) * 12 + \
                       (reference_date.month - last_review.month)
        assert months_since <= SR2_PLAN_REVIEW_MONTHS, (
            f"SR-2: SCRM plan last reviewed {months_since} months ago; must review ≤{SR2_PLAN_REVIEW_MONTHS} months."
        )

    @pytest.mark.human_review_required(
        reason=(
            "SR-2: SCRM plan content adequacy is CONTESTED. What constitutes adequate supply "
            "chain risk identification, assessment, and response for a given organization context "
            "is evaluated by the assessor against NIST SP 800-161 criteria — not objectively "
            "verifiable by automated assertion."
        )
    )
    def test_scrm_plan_content_adequacy(self, controls_evidence: dict, impact_level):
        """CONTESTED: SCRM plan must address identification, assessment, and response for supply chain risks."""
        if impact_level == "low":
            pytest.skip("SR-2 content adequacy check applies at Moderate/High")
        required = {
            "critical_components_identified",
            "supplier_vetting_criteria_documented",
            "supply_chain_incident_response_documented",
        }
        present = {k for k in required if controls_evidence.get(k, False)}
        missing = required - present
        assert not missing, (
            f"SR-2: SCRM plan missing required content areas: {missing}."
        )


class TestSR3SupplyChainControlsAndProcesses:
    """SR-3: Supply Chain Controls and Processes — Moderate/High [M][H]"""

    def test_critical_suppliers_identified(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: critical/high-risk suppliers must be identified and documented."""
        if impact_level == "low":
            pytest.skip("SR-3 critical supplier identification applies at Moderate/High")
        assert controls_evidence.get("critical_suppliers_identified_and_documented", False), (
            "SR-3: critical/high-risk suppliers not identified and documented."
        )

    @pytest.mark.assumption(
        id="ASSUME-800053-SR-001",
        description=(
            "SR-3 supplier controls ODP: controls and processes for managing supply chain risks "
            "from critical suppliers must be documented. Assessment of control sufficiency is "
            "PARAMETERIZED — criteria must be documented in the SCRM plan and reviewed by assessor."
        ),
        approved_by="ISSO",
        review_date="2026-05-21",
    )
    def test_supplier_vetting_process_documented(self, controls_evidence: dict, impact_level):
        """PARAMETERIZED: documented process for vetting critical suppliers must exist."""
        if impact_level == "low":
            pytest.skip("SR-3 supplier vetting applies at Moderate/High")
        assert controls_evidence.get("supplier_vetting_process_documented", False), (
            "SR-3: no documented process for vetting critical/high-risk suppliers."
        )


class TestSR11ComponentAuthenticity:
    """SR-11: Component Authenticity — Moderate/High [M][H]"""

    def test_authenticity_verification_in_place(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: component authenticity must be verified before installation."""
        if impact_level == "low":
            pytest.skip("SR-11 component authenticity applies at Moderate/High")
        assert controls_evidence.get("component_authenticity_verification_in_place", False), (
            "SR-11: no component authenticity verification in place for acquired ICT components."
        )

    def test_components_from_authorized_sources(self, controls_evidence: dict, impact_level):
        """DETERMINISTIC: ICT components must be sourced from authorized/trusted distributors."""
        if impact_level == "low":
            pytest.skip("SR-11 authorized sourcing applies at Moderate/High")
        assert controls_evidence.get("ict_components_from_authorized_distributors", False), (
            "SR-11: ICT components not documented as acquired from authorized distributors."
        )


class TestSR12ComponentDisposal:
    """SR-12: Component Disposal — all baselines [L][M][H]"""

    def test_component_disposal_process_documented(self, controls_evidence: dict):
        """DETERMINISTIC: a documented process for disposing of ICT components must exist."""
        assert controls_evidence.get("component_disposal_process_documented", False), (
            "SR-12: no documented process for secure disposal of ICT components."
        )
```

---

## Assumption registry

| ID | Family/Control | Summary | Review date |
|---|---|---|---|
| ASSUME-800053-RA-001 | RA-3 | Risk assessment frequency ODP: triennial (36 months); must document 5 required elements; methodology adequacy CONTESTED | 2026-05-21 |
| ASSUME-800053-RA-002 | RA-5 | Scan frequency ODP: monthly at Moderate/High; quarterly at Low; authenticated scans required at M/H | 2026-05-21 |
| ASSUME-800053-SA-001 | SA-8 | Security engineering principles ODP: documented selection from NIST 800-160 or equivalent; application adequacy PARAMETERIZED | 2026-05-21 |
| ASSUME-800053-SA-002 | SA-11 | Developer security testing ODP: plan documented; test results reviewed; coverage adequacy CONTESTED | 2026-05-21 |
| ASSUME-800053-SR-001 | SR-3 | Supplier controls ODP: vetting criteria documented in SCRM plan; control sufficiency PARAMETERIZED | 2026-05-21 |

## Parse status: Partial — RA, SA, SR added; 16 of 20 families now parsed (AU, AC, IA, CM, SC, SI, CP, IR, CA, MA, MP, PE, PS, RA, SA, SR)
