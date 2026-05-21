# SWIFT CSP — Detect & Respond Controls (Objectives 5 & 6)

**Framework:** SWIFT Customer Security Programme (CSP) — CSCF v2025
**Controls:** 6.1, 6.2, 6.3, 6.4, 7.1, 7.3A + Annual attestation gate
**Objective:** Detect Anomalous Activity + Plan for Incident Response
**Confidence:** HIGH (6.2, 6.3, 6.4, 7.1, 7.3A, attestation) / MEDIUM (6.1)
**Last parsed:** 2026-05-21

---

## Constants

```python
# Control 6.4 — Log retention
SWIFT_LOG_RETENTION_DAYS = 365       # 12 months minimum

# Control 7.3A — Penetration testing
SWIFT_PENTEST_INTERVAL_MONTHS = 12   # annual

# Annual attestation
SWIFT_ATTESTATION_DEADLINE_MONTH = 12
SWIFT_ATTESTATION_DEADLINE_DAY = 31
```

---

## Control 6.1 — Intrusion Detection

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | SWIFT secure zone network and host perimeter | DETERMINISTIC |
| Condition | Always (ongoing detection obligation) | DETERMINISTIC |
| Obligation | Intrusion detection or prevention system (IDS/IPS) or equivalent monitoring deployed; alerts investigated | PARAMETERIZED |
| Evidence | IDS/IPS system inventory; monitoring scope covering zone; alert investigation records | PARAMETERIZED |

**Overall: PARAMETERIZED — Pattern 2**

```python
import pytest
from datetime import date

@pytest.fixture(autouse=True)
def swift_scope(entity_profile: dict):
    if not entity_profile.get("is_swift_user", False):
        pytest.skip("Entity is not a SWIFT user — CSCF not applicable")

class TestControl6_1:
    """6.1 — Intrusion Detection: IDS/IPS or equivalent coverage of SWIFT zone."""

    @pytest.mark.assumption(
        id="ASSUME-SWIFT-6_1-001",
        description=(
            "IDS/IPS or equivalent monitoring deployed covering SWIFT secure zone network "
            "traffic and host endpoints; alerts are investigated and dispositioned within "
            "a documented SLA; monitoring is continuous (not batch); logs fed to SOC or "
            "SIEM with defined escalation path"
        ),
        approved_by="security_operations",
        review_date="2027-05-21",
    )
    def test_ids_or_equivalent_deployed_for_swift_zone(self, controls_evidence: dict):
        detection = controls_evidence.get("swift_intrusion_detection", {})
        assert detection.get("deployed", False), (
            "IDS/IPS or equivalent anomaly detection must be deployed for SWIFT zone"
        )

    def test_swift_zone_in_detection_scope(self, controls_evidence: dict):
        detection = controls_evidence.get("swift_intrusion_detection", {})
        assert detection.get("swift_zone_covered", False), (
            "IDS/IPS monitoring scope must include all SWIFT secure zone systems"
        )

    def test_alerts_have_investigation_process(self, controls_evidence: dict):
        detection = controls_evidence.get("swift_intrusion_detection", {})
        assert detection.get("alert_investigation_process_documented", False), (
            "IDS/IPS alert investigation and disposition process must be documented"
        )
```

---

## Control 6.2 — Software Integrity Check

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | SWIFT software components (SWIFT messaging interface, Alliance software, connector) | DETERMINISTIC |
| Condition | SWIFT software deployed in the secure zone | DETERMINISTIC |
| Obligation | File integrity monitoring (FIM) applied to SWIFT software components; unauthorized modifications detected and alerted | DETERMINISTIC |
| Evidence | FIM tool inventory; SWIFT component hashes; alert on unauthorized modification | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestControl6_2:
    """6.2 — Software Integrity Check: FIM on SWIFT software components."""

    def test_fim_deployed_on_swift_components(self, controls_evidence: dict):
        fim = controls_evidence.get("swift_fim_config", {})
        assert fim.get("deployed", False), (
            "File integrity monitoring must be deployed for SWIFT software components"
        )

    def test_swift_components_in_fim_scope(self, controls_evidence: dict):
        swift_components = set(controls_evidence.get("swift_software_components", []))
        fim_scope = set(controls_evidence.get("swift_fim_monitored_components", []))
        uncovered = swift_components - fim_scope
        assert not uncovered, (
            f"All SWIFT software components must be in FIM monitoring scope. "
            f"Uncovered: {uncovered}"
        )

    def test_fim_alerts_on_unauthorized_change(self, controls_evidence: dict):
        fim = controls_evidence.get("swift_fim_config", {})
        assert fim.get("alerts_on_modification", False), (
            "FIM must generate alerts on any unauthorized modification to SWIFT components"
        )
```

---

## Control 6.3 — Database Integrity

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | Databases storing SWIFT transaction data and configuration | DETERMINISTIC |
| Condition | SWIFT zone contains databases with transaction or audit records | DETERMINISTIC |
| Obligation | Database activity monitoring (DAM) deployed; unauthorized queries or modifications to critical SWIFT databases detected and alerted | DETERMINISTIC |
| Evidence | DAM tool inventory; monitoring scope covering SWIFT transaction databases; alert records | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestControl6_3:
    """6.3 — Database Integrity: DAM on SWIFT transaction databases."""

    def test_dam_deployed_on_swift_databases(self, controls_evidence: dict):
        dam = controls_evidence.get("swift_dam_config", {})
        assert dam.get("deployed", False), (
            "Database activity monitoring must be deployed for SWIFT transaction databases"
        )

    def test_swift_databases_in_dam_scope(self, controls_evidence: dict):
        swift_dbs = set(controls_evidence.get("swift_critical_databases", []))
        dam_scope = set(controls_evidence.get("swift_dam_monitored_databases", []))
        uncovered = swift_dbs - dam_scope
        assert not uncovered, (
            f"All SWIFT critical databases must be in DAM scope. Uncovered: {uncovered}"
        )

    def test_dam_alerts_on_suspicious_activity(self, controls_evidence: dict):
        dam = controls_evidence.get("swift_dam_config", {})
        assert dam.get("alerts_configured", False), (
            "DAM must generate alerts on suspicious database activity"
        )
```

---

## Control 6.4 — Log Preservation

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | All logs generated by SWIFT infrastructure (transaction logs, authentication logs, admin logs, OS logs) | DETERMINISTIC |
| Condition | Always (ongoing obligation) | DETERMINISTIC |
| Obligation | SWIFT transaction and security logs retained for minimum 12 months; protected from unauthorized modification or deletion | DETERMINISTIC |
| Evidence | Log retention policy; log system configuration showing retention period; log integrity controls | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestControl6_4:
    """6.4 — Log Preservation: 12-month minimum retention for SWIFT logs."""

    def test_log_retention_policy_meets_minimum(self, controls_evidence: dict):
        log_config = controls_evidence.get("swift_log_retention_config", {})
        retention_days = log_config.get("retention_days", 0)
        assert retention_days >= SWIFT_LOG_RETENTION_DAYS, (
            f"SWIFT log retention must be ≥{SWIFT_LOG_RETENTION_DAYS} days (12 months). "
            f"Current: {retention_days}"
        )

    def test_swift_transaction_logs_in_retention_scope(self, controls_evidence: dict):
        log_config = controls_evidence.get("swift_log_retention_config", {})
        required_log_types = {"transaction_logs", "authentication_logs", "admin_logs", "os_logs"}
        covered = set(log_config.get("covered_log_types", []))
        missing = required_log_types - covered
        assert not missing, (
            f"All SWIFT log types must be covered by retention policy. Missing: {missing}"
        )

    def test_logs_protected_from_modification(self, controls_evidence: dict):
        log_config = controls_evidence.get("swift_log_retention_config", {})
        assert log_config.get("integrity_protection_enabled", False), (
            "SWIFT logs must be protected from unauthorized modification or deletion "
            "(write-once, append-only, or SIEM-forwarded)"
        )

    def test_logs_available_within_retention_window(
        self, controls_evidence: dict, reference_date: date
    ):
        from datetime import timedelta
        oldest_log = controls_evidence.get("swift_oldest_available_log_date")
        if oldest_log is None:
            pytest.skip("Log availability date not in evidence — manual verification required")
        required_oldest = reference_date - timedelta(days=SWIFT_LOG_RETENTION_DAYS)
        assert oldest_log <= required_oldest, (
            f"SWIFT logs must be available back to {required_oldest}. "
            f"Oldest available: {oldest_log}"
        )
```

---

## Control 7.1 — Cyber Incident Response Planning

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | SWIFT user organization | DETERMINISTIC |
| Condition | Always (plan must exist pre-incident) | DETERMINISTIC |
| Obligation | Written incident response plan that specifically addresses SWIFT-related cyber incidents (fraud, SWIFT credential compromise, unauthorized transactions) | DETERMINISTIC |
| Evidence | IRP document with SWIFT-specific scenarios; SWIFT contact escalation procedure; annual test record | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
SWIFT_IRP_REQUIRED_ELEMENTS = frozenset({
    "swift_fraud_scenario",
    "swift_credential_compromise_scenario",
    "unauthorized_transaction_scenario",
    "swift_contact_escalation_procedure",
    "roles_and_responsibilities",
    "communication_plan",
})

class TestControl7_1:
    """7.1 — Cyber Incident Response Planning: IRP with SWIFT-specific scenarios."""

    def test_irp_exists(self, controls_evidence: dict):
        irp = controls_evidence.get("swift_irp", {})
        assert irp.get("exists", False), (
            "Written incident response plan must exist"
        )

    def test_irp_contains_required_elements(self, controls_evidence: dict):
        irp = controls_evidence.get("swift_irp", {})
        elements_present = set(irp.get("elements_present", []))
        missing = SWIFT_IRP_REQUIRED_ELEMENTS - elements_present
        assert not missing, (
            f"IRP must contain all required SWIFT-specific elements. Missing: {missing}"
        )

    def test_irp_tested_within_12_months(
        self, controls_evidence: dict, reference_date: date
    ):
        from datetime import timedelta
        irp = controls_evidence.get("swift_irp", {})
        last_test = irp.get("last_test_date")
        assert last_test is not None, "IRP must have a documented test date"
        cutoff = reference_date - timedelta(days=365)
        assert last_test >= cutoff, (
            f"IRP must be tested within 12 months. Last test: {last_test}; cutoff: {cutoff}"
        )

    def test_swift_emergency_contacts_documented(self, controls_evidence: dict):
        irp = controls_evidence.get("swift_irp", {})
        contacts = irp.get("swift_emergency_contacts", [])
        assert contacts, (
            "IRP must include SWIFT emergency contact information (SWIFT ISAC, regional support)"
        )
```

---

## Control 7.3A — Penetration Testing

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | SWIFT infrastructure (secure zone systems, operator PCs, authentication mechanisms) | DETERMINISTIC |
| Condition | Annual obligation | DETERMINISTIC |
| Obligation | Penetration test of SWIFT infrastructure performed at least annually by qualified tester; findings tracked and remediated | DETERMINISTIC |
| Evidence | Pentest engagement contract; pentest report with SWIFT scope; finding remediation records | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestControl7_3A:
    """7.3A — Penetration Testing: annual pentest of SWIFT infrastructure."""

    def test_pentest_completed_within_12_months(
        self, controls_evidence: dict, reference_date: date
    ):
        from datetime import timedelta
        pentest = controls_evidence.get("swift_pentest", {})
        last_pentest = pentest.get("last_completion_date")
        assert last_pentest is not None, "SWIFT penetration test must have a recorded completion date"
        cutoff = reference_date - timedelta(days=SWIFT_PENTEST_INTERVAL_MONTHS * 30)
        assert last_pentest >= cutoff, (
            f"SWIFT pentest must be completed within {SWIFT_PENTEST_INTERVAL_MONTHS} months. "
            f"Last pentest: {last_pentest}; cutoff: {cutoff}"
        )

    def test_pentest_scope_includes_swift_zone(self, controls_evidence: dict):
        pentest = controls_evidence.get("swift_pentest", {})
        scope = set(pentest.get("scope_components", []))
        required_scope = {"swift_zone_network", "swift_messaging_interface", "operator_pcs"}
        missing = required_scope - scope
        assert not missing, (
            f"Pentest scope must include all SWIFT infrastructure components. Missing: {missing}"
        )

    def test_pentest_critical_findings_remediated(self, controls_evidence: dict):
        pentest = controls_evidence.get("swift_pentest", {})
        findings = pentest.get("findings", [])
        open_critical = [
            f for f in findings
            if f.get("severity") == "critical" and not f.get("remediated", False)
        ]
        assert not open_critical, (
            f"All critical pentest findings must be remediated before next attestation. "
            f"Open critical findings: {[f['finding_id'] for f in open_critical]}"
        )
```

---

## Annual Self-Attestation Gate

**Element extraction:**

| Element | Value | Classification |
|---|---|---|
| Subject | SWIFT user organization | DETERMINISTIC |
| Condition | Annual attestation cycle (calendar year) | DETERMINISTIC |
| Obligation | Self-attestation submitted via KYC-SA application by December 31; all 25 mandatory controls attested | DETERMINISTIC |
| Evidence | KYC-SA attestation submission record with submission date; all mandatory controls attested as compliant | DETERMINISTIC |

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestAnnualAttestation:
    """Annual SWIFT self-attestation gate: submitted by Dec 31, all 25 mandatory controls."""

    def test_attestation_submitted_for_current_cycle(self, controls_evidence: dict):
        attestation = controls_evidence.get("swift_kycsa_attestation", {})
        assert attestation.get("submitted", False), (
            "Annual SWIFT self-attestation must be submitted via KYC-SA application"
        )

    def test_attestation_submitted_before_deadline(self, controls_evidence: dict):
        attestation = controls_evidence.get("swift_kycsa_attestation", {})
        submission_date = attestation.get("submission_date")
        assert submission_date is not None, "Attestation submission date must be recorded"
        assert submission_date.month <= SWIFT_ATTESTATION_DEADLINE_MONTH, (
            f"Attestation must be submitted by month {SWIFT_ATTESTATION_DEADLINE_MONTH}. "
            f"Submitted: {submission_date}"
        )

    def test_all_mandatory_controls_attested(self, controls_evidence: dict):
        attestation = controls_evidence.get("swift_kycsa_attestation", {})
        attested_controls = set(attestation.get("attested_control_ids", []))
        mandatory_controls = {
            "1.1", "1.2", "1.3", "2.1", "2.2", "2.3A", "2.5A", "2.7A",
            "3.1", "3.2", "3.3", "4.1", "4.2", "4.3A", "4.4",
            "5.1", "5.2", "5.3A",
            "6.1", "6.2", "6.3", "6.4", "7.1", "7.3A",
        }
        missing = mandatory_controls - attested_controls
        assert not missing, (
            f"All 25 mandatory CSCF controls must be attested. Missing from attestation: {missing}"
        )
```

---

## Open assumptions

| ID | Control | Summary | Review date |
|---|---|---|---|
| ASSUME-SWIFT-6_1-001 | 6.1 | IDS/IPS deployed on SWIFT zone; continuous monitoring; alerts investigated with documented SLA; fed to SOC/SIEM | 2027-05-21 |
