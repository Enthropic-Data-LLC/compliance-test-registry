# TISAX / VDA ISA 6.0 — IT/Information Security & Supplier Management

**Framework:** TISAX (Trusted Information Security Assessment Exchange) / VDA ISA 6.0
**Domains:** 4 (IT / Information Security), 5 (Supplier and Service Provider Management)
**Assessment Levels:** AL1 (self), AL2 (remote audit), AL3 (on-site)
**Confidence:** MEDIUM (Domain 4) / PARAMETERIZED-dominant (Domain 5)
**Last parsed:** 2026-05-21

---

## Constants

```python
# Domain 4 — IT controls
TISAX_ACCESS_REVIEW_MONTHS = 12
TISAX_APPROVED_ENCRYPTION_ALGORITHMS = frozenset({"aes-128", "aes-256", "rsa-2048", "rsa-4096", "ec-p256", "ec-p384"})
TISAX_PROHIBITED_ENCRYPTION = frozenset({"des", "3des", "rc4", "md5"})

# Domain 4 — Logging
TISAX_LOG_RETENTION_DAYS = 90    # minimum; organization ODP may extend

# Domain 5 — Supplier
TISAX_SUB_SUPPLIER_ASSESSMENT_REQUIRED = True  # for sub-suppliers with access to project data
```

---

## Domain 4 — IT / Information Security

### 4.1 — Asset Management

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Information assets (systems, data, applications) handling automotive project data | DETERMINISTIC |
| Condition | Assets exist in scope of automotive project data handling | DETERMINISTIC |
| Obligation | Asset inventory maintained with data classification; automotive project data assets identified and labeled | DETERMINISTIC |
| Evidence | Asset inventory with classification labels; automotive data assets enumerated | DETERMINISTIC |

```python
import pytest
from datetime import date

@pytest.fixture(autouse=True)
def tisax_scope(entity_profile: dict):
    if not entity_profile.get("tisax_contractual_obligation", False):
        pytest.skip("No TISAX contractual obligation — VDA ISA not applicable")

class TestDomain4_IT:
    """Domain 4 — IT/Information Security: assets, access, crypto, vuln mgmt, logging, IR."""

    def test_asset_inventory_exists(self, controls_evidence: dict):
        assets = controls_evidence.get("tisax_asset_inventory", {})
        assert assets.get("exists", False), (
            "Asset inventory must exist covering automotive project data assets"
        )

    def test_automotive_project_data_assets_classified(self, controls_evidence: dict):
        assets = controls_evidence.get("tisax_asset_inventory", {})
        assert assets.get("automotive_data_classified", False), (
            "Assets containing automotive project data must be classified and labeled"
        )

    # ── Logical access control ────────────────────────────────────────────

    def test_access_control_principle_of_least_privilege(self, controls_evidence: dict):
        ac = controls_evidence.get("tisax_access_control", {})
        assert ac.get("least_privilege_enforced", False), (
            "Principle of least privilege must be applied to automotive project data access"
        )

    def test_access_review_within_12_months(
        self, controls_evidence: dict, reference_date: date
    ):
        from datetime import timedelta
        ac = controls_evidence.get("tisax_access_control", {})
        last_review = ac.get("last_access_review_date")
        assert last_review is not None, "Access review must have a documented completion date"
        cutoff = reference_date - timedelta(days=TISAX_ACCESS_REVIEW_MONTHS * 30)
        assert last_review >= cutoff, (
            f"Access review must occur within {TISAX_ACCESS_REVIEW_MONTHS} months. "
            f"Last review: {last_review}; cutoff: {cutoff}"
        )

    # ── Cryptography ──────────────────────────────────────────────────────

    @pytest.mark.assumption(
        id="ASSUME-TISAX-4_1-001",
        description=(
            "Automotive project data (vehicle designs, technical specs, test data classified "
            "as confidential or strictly confidential) encrypted at rest using AES-128+ and "
            "in transit using TLS 1.2+; encryption applies to all storage media (local, cloud, "
            "portable) and all transmission channels including email attachments"
        ),
        approved_by="security_architect",
        review_date="2027-05-21",
    )
    def test_project_data_encrypted_at_rest(self, controls_evidence: dict):
        crypto = controls_evidence.get("tisax_crypto_config", {})
        assert crypto.get("project_data_at_rest_encrypted", False), (
            "Automotive project data classified as confidential must be encrypted at rest"
        )

    def test_encryption_algorithms_approved(self, controls_evidence: dict):
        crypto = controls_evidence.get("tisax_crypto_config", {})
        algorithms_in_use = {a.lower() for a in crypto.get("algorithms_in_use", [])}
        prohibited_in_use = algorithms_in_use & TISAX_PROHIBITED_ENCRYPTION
        assert not prohibited_in_use, (
            f"Prohibited encryption algorithms found in use: {prohibited_in_use}"
        )

    def test_project_data_encrypted_in_transit(self, controls_evidence: dict):
        crypto = controls_evidence.get("tisax_crypto_config", {})
        assert crypto.get("project_data_in_transit_encrypted", False), (
            "Automotive project data must be encrypted in transit (TLS 1.2+)"
        )

    # ── Vulnerability management ──────────────────────────────────────────

    @pytest.mark.assumption(
        id="ASSUME-TISAX-4_1-002",
        description=(
            "Vulnerability scanning performed at least quarterly on systems handling "
            "automotive project data; critical and high findings remediated within "
            "documented SLAs; findings tracked in vulnerability management system"
        ),
        approved_by="security_operations",
        review_date="2027-05-21",
    )
    def test_vulnerability_management_process_documented(self, controls_evidence: dict):
        vuln = controls_evidence.get("tisax_vulnerability_management", {})
        assert vuln.get("process_documented", False), (
            "Vulnerability management process must be documented for TISAX-in-scope systems"
        )

    def test_no_unaddressed_critical_vulnerabilities(self, controls_evidence: dict):
        vuln = controls_evidence.get("tisax_vulnerability_management", {})
        findings = vuln.get("open_findings", [])
        open_critical = [
            f for f in findings
            if f.get("severity") == "critical"
            and not f.get("remediated", False)
            and not f.get("accepted_risk", False)
        ]
        assert not open_critical, (
            f"Critical vulnerabilities on TISAX-in-scope systems must be remediated or risk-accepted. "
            f"Open critical: {[f['finding_id'] for f in open_critical]}"
        )

    # ── Logging and monitoring ────────────────────────────────────────────

    @pytest.mark.assumption(
        id="ASSUME-TISAX-4_1-003",
        description=(
            "Audit logging enabled for all systems handling automotive project data; "
            "logs include authentication events, data access, and privilege use; "
            "retention minimum 90 days; logs reviewed periodically for anomalies"
        ),
        approved_by="security_operations",
        review_date="2027-05-21",
    )
    def test_audit_logging_enabled_on_project_data_systems(self, controls_evidence: dict):
        logging = controls_evidence.get("tisax_logging", {})
        assert logging.get("enabled_on_project_systems", False), (
            "Audit logging must be enabled on all systems handling automotive project data"
        )

    def test_log_retention_meets_minimum(self, controls_evidence: dict):
        logging = controls_evidence.get("tisax_logging", {})
        retention_days = logging.get("retention_days", 0)
        assert retention_days >= TISAX_LOG_RETENTION_DAYS, (
            f"Log retention must be ≥{TISAX_LOG_RETENTION_DAYS} days for TISAX systems. "
            f"Current: {retention_days}"
        )

    # ── Incident management ───────────────────────────────────────────────

    def test_incident_management_process_written(self, controls_evidence: dict):
        ir = controls_evidence.get("tisax_incident_management", {})
        assert ir.get("written_process_exists", False), (
            "Written incident management process must exist covering automotive data incidents"
        )

    def test_incident_records_maintained(self, controls_evidence: dict):
        ir = controls_evidence.get("tisax_incident_management", {})
        assert ir.get("records_maintained", False), (
            "Incident records must be maintained with response actions documented"
        )
```

---

## Domain 5 — Supplier and Service Provider Management

### 5.1 — Supplier Security Requirements

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Sub-suppliers and service providers with access to automotive project data | DETERMINISTIC |
| Condition | Organization shares automotive project data or system access with third parties | DETERMINISTIC |
| Obligation | IS requirements flowed down to sub-suppliers; sub-suppliers with project data access required to have equivalent IS assessment | PARAMETERIZED |
| Evidence | Supplier contracts with IS requirements; supplier assessment records; TISAX label or equivalent from sub-suppliers | PARAMETERIZED |

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestDomain5_Suppliers:
    """Domain 5 — Supplier/Service Provider Management: IS flow-down and assessment."""

    @pytest.mark.assumption(
        id="ASSUME-TISAX-5_1-001",
        description=(
            "IS requirements flow-down contract clause included in all supplier agreements "
            "where the supplier receives automotive project data; sub-suppliers at AL2/AL3 "
            "must hold TISAX label or equivalent VDA ISA assessment; non-IT service providers "
            "(facilities, maintenance) addressed via supplier questionnaire"
        ),
        approved_by="procurement_security",
        review_date="2027-05-21",
    )
    def test_supplier_contracts_include_is_requirements(self, controls_evidence: dict):
        suppliers = controls_evidence.get("tisax_project_data_suppliers", [])
        no_clause = [s for s in suppliers if not s.get("is_requirements_in_contract", False)]
        assert not no_clause, (
            f"IS requirements clause must be included in all supplier contracts where "
            f"automotive project data is shared. Missing: {[s['supplier_id'] for s in no_clause]}"
        )

    def test_project_data_suppliers_have_assessment(self, controls_evidence: dict):
        suppliers = controls_evidence.get("tisax_project_data_suppliers", [])
        al = 2
        if al >= 2:
            unassessed = [
                s for s in suppliers
                if s.get("receives_project_data", False)
                and not s.get("tisax_or_equivalent_assessment", False)
            ]
            assert not unassessed, (
                f"Sub-suppliers receiving automotive project data must hold TISAX label or "
                f"equivalent IS assessment. Unassessed: {[s['supplier_id'] for s in unassessed]}"
            )

    @pytest.mark.assumption(
        id="ASSUME-TISAX-5_1-002",
        description=(
            "Equivalency criteria for non-TISAX supplier assessments: ISO 27001 certification "
            "covering the relevant scope is accepted as equivalent at AL2; AL3 requires TISAX "
            "label specifically; equivalency determination documented and approved by ISSO"
        ),
        approved_by="ISSO",
        review_date="2027-05-21",
    )
    @pytest.mark.human_review_required(
        reason=(
            "Assessment adequacy of sub-supplier IS controls requires qualified review — "
            "whether a supplier's ISO 27001 scope, TISAX label, or questionnaire response "
            "sufficiently covers the automotive data handling use case cannot be automatically "
            "verified; requires human assessor judgment"
        )
    )
    def test_supplier_assessment_adequacy(self, controls_evidence: dict, entity_profile: dict):
        al = entity_profile.get("tisax_assessment_level", 2)
        suppliers = controls_evidence.get("tisax_project_data_suppliers", [])
        for supplier in suppliers:
            if supplier.get("receives_project_data", False):
                has_review = supplier.get("assessment_adequacy_reviewed_by_human", False)
                assert has_review, (
                    f"Supplier {supplier['supplier_id']} assessment adequacy must be reviewed "
                    f"by a qualified person (AL{al} obligation)"
                )
```

---

## Cross-standard notes

**ISO 27001 ↔ TISAX:** ISO 27001 certification covering the same scope is accepted as
partial evidence in TISAX assessments. An ISO 27001 SoA that includes the relevant Annex A
controls and a documented statement of applicability referencing automotive data can reduce
assessment effort at AL2. It does not replace the TISAX assessment process.

**IATF 16949 §7.4 ↔ TISAX Domain 5:** Both require IS requirements to flow down to the
automotive supply chain. A single supplier management framework can satisfy both if it
includes IS assessment criteria alongside quality requirements.

---

## Open assumptions

| ID | Control | Summary | Review date |
|---|---|---|---|
| ASSUME-TISAX-4_1-001 | Cryptography | Project data encrypted at rest (AES-128+) and in transit (TLS 1.2+); applies to all storage and transmission | 2027-05-21 |
| ASSUME-TISAX-4_1-002 | Vulnerability management | Quarterly scanning; critical/high SLAs documented; tracked in vuln system | 2027-05-21 |
| ASSUME-TISAX-4_1-003 | Logging | Logging enabled on project data systems; events: auth + data access + privilege; 90-day retention | 2027-05-21 |
| ASSUME-TISAX-5_1-001 | Supplier flow-down | IS requirements clause in all supplier contracts; sub-suppliers with project data access require assessment | 2027-05-21 |
| ASSUME-TISAX-5_1-002 | Supplier equivalency | ISO 27001 accepted as AL2 equivalent; AL3 requires TISAX label specifically | 2027-05-21 |
