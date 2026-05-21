# SOC 2 TSC 2017 — CC9, C1, PI1: Risk Mitigation, Confidentiality, Processing Integrity

**Registry path:** `/regulation-registry/SOC2/CC9-C1-PI1/`
**Version:** AICPA TSC 2017 (2022 points of focus updates)
**Last parsed:** 2026-05-20
**Overall confidence:** MEDIUM for C1.2 and PI1 processing checks; CONTESTED for CC9.2 (vendor risk adequacy); PARAMETERIZED for CC9.1 and C1.1
**9 criteria total: CC9.1–CC9.2, C1.1–C1.2, PI1.1–PI1.5**

---

## Scope summary

CC9 (Risk Mitigation) covers residual risk treatment and vendor/third-party management. It is always in scope. C1 (Confidentiality) and PI1 (Processing Integrity) are optional trust service categories selected based on commitments to customers. 

CC9.2 (vendor risk) is CONTESTED because vendor assessment adequacy is auditor-evaluated. C1 is MEDIUM — disposal documentation is DETERMINISTIC; classification criteria are PARAMETERIZED. PI1 processing integrity tests are MEDIUM because input/output validation thresholds are measurable once defined, but "complete, valid, accurate, timely, authorized" standards are organization-defined.

---

## CC9 — Risk Mitigation

### CC9.1 — Risk Mitigation Activities (PARAMETERIZED)

| Element | Value | Classification |
|---|---|---|
| Obligation | Risk treatment decisions documented; residual risk accepted, mitigated, transferred, or avoided; treatment aligned with risk tolerance | PARAMETERIZED |
| Evidence | `risk_register.treatment_documented`; `risk_acceptance_records.signed_by_owner` | PARAMETERIZED |

**Assumption (ASSUME-SOC2-CC9-001):** Risk mitigation is adequate when: (1) all identified risks have a documented treatment decision (accept/mitigate/transfer/avoid); (2) risk acceptance decisions are signed by the risk owner and reviewed against defined risk tolerance criteria; (3) mitigated risks have documented controls and evidence of control operation; (4) transferred risks (e.g., via cyber insurance or contract indemnification) have policy/agreement documentation; (5) residual risk re-evaluated at least annually.

**Overall: PARAMETERIZED → Pattern 2**

---

### CC9.2 — Vendor and Business Partner Risk Management (CONTESTED)

| Element | Value | Classification |
|---|---|---|
| Obligation | Vendor risk assessed before relationship; ongoing monitoring of vendor security posture; vendor agreements include security requirements | CONTESTED |
| Evidence | `vendor_risk_assessments.completed_before_onboarding == true`; `vendor_agreements.security_clauses_present == true`; periodic vendor review records | CONTESTED |

> **CONTESTED reason:** Vendor assessment adequacy is auditor-evaluated. The depth of assessment appropriate for each vendor tier (critical, standard, low-risk) depends on the service, data accessed, and organization's risk profile. SOC 2 pass-through requirements (relying on subservice organization's own SOC 2 report) vs. carve-out method vs. performing direct assessment is a judgment call.

**Assumption (ASSUME-SOC2-CC9-002):** Vendor/third-party risk management is adequate when: (1) all vendors with access to systems or data in SOC 2 boundary categorized by risk tier; (2) critical vendors (access to sensitive data, single points of failure): assessed via SOC 2 report review or equivalent; annual review; (3) standard vendors: security questionnaire + contract clauses; (4) all vendor agreements include: security obligations, breach notification requirement, right to audit; (5) subservice organizations identified in system description with applicable carve-out or inclusive method noted.

**Overall: CONTESTED → Pattern 3; PARAMETERIZED elements → Pattern 2**

---

## C1 — Confidentiality (Optional)

### C1.1 — Identification and Classification of Confidential Information (PARAMETERIZED)

| Element | Value | Classification |
|---|---|---|
| Obligation | Confidential information identified and classified per the entity's commitments; classification criteria defined | PARAMETERIZED |
| Evidence | `data_classification_policy.documented == true`; data inventory includes classification labels; confidential information identified | PARAMETERIZED |

**Assumption (ASSUME-SOC2-C1-001):** Confidential information classification is adequate when: (1) classification policy defines criteria for "confidential" (typically: customer data, financial data, trade secrets, PII, contractually restricted data); (2) all data handling is governed by classification: storage encryption, access restriction, transmission protection, and disposal aligned with classification level; (3) data inventory or catalog identifies confidential information assets and their locations; (4) personnel training covers classification criteria and handling obligations.

**Overall: PARAMETERIZED → Pattern 2**

---

### C1.2 — Disposal of Confidential Information (MEDIUM)

| Element | Value | Classification |
|---|---|---|
| Obligation | Confidential information disposed of when no longer required; disposal meets the entity's confidentiality commitments | DETERMINISTIC (disposal record existence) / PARAMETERIZED (method adequacy) |
| Evidence | `data_disposal_records.method_documented`; `disposal_certificates.exists == true` for physical media | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-SOC2-C1-002):** Confidential information disposal is adequate when: (1) digital records: overwrite or cryptographic erasure when key is destroyed ("crypto shredding"); (2) physical media: NIST SP 800-88 Clear/Purge for HDD; physical destruction or ATA Secure Erase for SSD; (3) paper records: cross-cut shredding (≤ 2mm particles) or incineration; (4) disposal certificates issued for all physical media and paper; (5) disposal triggered at contract end for customer data (or earlier per contract); (6) cloud data: documented deletion request plus provider confirmation. Aligns with ISO 27001 ASSUME-ISO-A7-006 (media disposal) and PCI DSS 9.4.6 (paper disposal).

**Overall: DETERMINISTIC for disposal documentation → Pattern 1; PARAMETERIZED for method → Pattern 2**

---

## PI1 — Processing Integrity (Optional)

### PI1.1–PI1.5 — Complete, Valid, Accurate, Timely, and Authorized Processing (MEDIUM)

The Processing Integrity criteria address whether the system processes data completely, validly, accurately, on time, and with proper authorization. All five sub-criteria share a common element extraction pattern.

| Criterion | Focus | Classification | Notes |
|---|---|---|---|
| PI1.1 | Authorized, complete, accurate, timely input | MEDIUM | Input validation controls are DETERMINISTIC once thresholds defined |
| PI1.2 | Processing delivers required outputs | MEDIUM | Output reconciliation checks are DETERMINISTIC if implemented |
| PI1.3 | Stored data complete and accurate | PARAMETERIZED | Data integrity checks exist; adequacy is org-defined |
| PI1.4 | Outputs distributed correctly and timely | PARAMETERIZED | Distribution log existence is DETERMINISTIC; completeness is PARAMETERIZED |
| PI1.5 | Inputs/outputs monitored for errors and corrections | MEDIUM | Error rate monitoring is DETERMINISTIC if threshold defined |

### Consolidated element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Input validation implemented; processing errors detected and logged; reconciliation controls in place; output delivery verified | DETERMINISTIC (controls existence) / PARAMETERIZED (threshold adequacy) |
| Evidence | `input_validation_controls.implemented == true`; `error_rate_monitoring.deployed == true`; `reconciliation_records.exists == true`; output delivery logs | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-SOC2-PI1-001):** Processing integrity controls are adequate when: (1) input validation rejects malformed, out-of-range, or incomplete data before processing; (2) processing errors are logged and reviewed; error rate thresholds alert when exceeded; (3) reconciliation controls verify that output totals match expected values; (4) output delivery logs capture recipient, timestamp, and success/failure status; (5) data corrections require authorization (no unauthorized modification of processed data); (6) for financial or high-stakes processing: dual-control or supervisory review for high-value transactions.

**Overall: PARAMETERIZED for threshold adequacy → Pattern 2; controls existence → Pattern 1**

---

## YAML specifications

### `cc9_c1_pi1_additional.yaml`

```yaml
regulation_id: SOC2-TSC2017-CC9-C1-PI1
section: "SOC 2 TSC 2017 — CC9, C1, PI1: Risk Mitigation, Confidentiality, Processing Integrity"
r_or_a: >
  CC9: Required. C1, PI1: Additional (in scope when confidentiality/processing integrity
  commitments made to customers).
source_text: >
  CC9: Entity assesses vendor risk and mitigates identified risks.
  C1: Confidential information identified, protected, and disposed of appropriately.
  PI1: Information processed completely, validly, accurately, timely, and with authorization.

overall_classification: PARAMETERIZED
human_review_required: true
test_confidence: MEDIUM
generated_test: "tests/soc2/test_cc9_c1_pi1.py"
```

---

## Generated tests

### `tests/soc2/test_cc9_c1_pi1.py`

```python
"""
SOC 2 TSC 2017 — CC9, C1, PI1: Risk Mitigation, Confidentiality, Processing Integrity
Confidence: MEDIUM — existence checks DETERMINISTIC; adequacy PARAMETERIZED or CONTESTED
"""
import pytest
from datetime import date


def test_risk_register_all_risks_have_treatment(risk_register_entries):
    """CC9.1 — All identified risks must have a documented treatment decision."""
    untreated = [
        r for r in risk_register_entries
        if not r.get("treatment_decision")
    ]
    assert not untreated, (
        f"NONCONFORMITY (CC9.1): {len(untreated)} risk(s) without documented treatment "
        f"decision: {[r.get('risk_id') for r in untreated]}"
    )


def test_accepted_risks_have_owner_signature(risk_register_entries):
    """CC9.1 — Accepted risks must have owner sign-off."""
    violations = [
        r for r in risk_register_entries
        if r.get("treatment_decision") == "accept"
        and not r.get("risk_owner_accepted")
    ]
    assert not violations, (
        f"NONCONFORMITY (CC9.1): {len(violations)} accepted risk(s) without owner sign-off: "
        f"{[r.get('risk_id') for r in violations]}"
    )


@pytest.mark.human_review_required(
    reason=(
        "CC9.2: Vendor assessment adequacy and tier classification require "
        "human evaluation — automated test verifies agreement existence only."
    )
)
@pytest.mark.assumption(
    id="ASSUME-SOC2-CC9-002",
    description=(
        "Critical vendors: SOC 2 review or equivalent annually; standard vendors: "
        "questionnaire + contract clauses; all agreements include security obligations + breach notification."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_critical_vendors_have_security_agreements(vendor_register, vendor_agreements):
    """CC9.2 — Vendors with data/system access must have documented security agreements."""
    agreement_vendor_ids = {
        a["vendor_id"] for a in vendor_agreements
        if a.get("security_clauses_present")
    }
    violations = [
        v for v in vendor_register
        if v.get("has_system_or_data_access")
        and v["vendor_id"] not in agreement_vendor_ids
    ]
    assert not violations, (
        f"NONCONFORMITY (CC9.2): {len(violations)} vendor(s) with data/system access "
        f"but no security agreement clauses: "
        f"{[v['vendor_id'] for v in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-SOC2-C1-002",
    description=(
        "Digital: crypto shredding or overwrite; physical media: NIST SP 800-88; "
        "paper: cross-cut shred; customer data disposed at contract end."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_confidential_data_disposal_documented(data_disposal_records):
    """C1.2 — Disposal of confidential information must be documented."""
    violations = [
        r for r in data_disposal_records
        if r.get("data_classification") in ("confidential", "sensitive", "restricted")
        and not r.get("disposal_method_documented")
    ]
    assert not violations, (
        f"NONCONFORMITY (C1.2): {len(violations)} confidential data disposal record(s) "
        f"without documented method: {[r.get('disposal_id') for r in violations]}"
    )


def test_input_validation_controls_deployed(processing_control_records):
    """PI1.1 — Input validation controls must be deployed for in-scope processing."""
    soc2_processing = [
        r for r in processing_control_records
        if r.get("in_soc2_boundary") and r.get("processes_customer_data")
    ]
    if not soc2_processing:
        pytest.skip("No in-scope processing records")
    no_validation = [
        r for r in soc2_processing
        if not r.get("input_validation_implemented")
    ]
    assert not no_validation, (
        f"NONCONFORMITY (PI1.1): {len(no_validation)} processing component(s) without "
        f"input validation controls: {[r['component_id'] for r in no_validation]}"
    )


def test_processing_errors_monitored(processing_control_records):
    """PI1.5 — Processing errors must be monitored and logged."""
    soc2_processing = [
        r for r in processing_control_records
        if r.get("in_soc2_boundary") and r.get("processes_customer_data")
    ]
    if not soc2_processing:
        pytest.skip("No in-scope processing records")
    no_error_monitoring = [
        r for r in soc2_processing
        if not r.get("error_monitoring_deployed")
    ]
    assert not no_error_monitoring, (
        f"NONCONFORMITY (PI1.5): {len(no_error_monitoring)} processing component(s) "
        f"without error monitoring: {[r['component_id'] for r in no_error_monitoring]}"
    )
```

---

## Notes for the registry

- **CC9.2 subservice organizations vs. vendors:** SOC 2 distinguishes between "vendors" (third parties providing supporting services but not within the system boundary) and "subservice organizations" (third parties that provide system components included in the SOC 2 system description). Subservice organizations must be disclosed in the system description; vendors typically are not. The distinction affects whether their controls are tested or merely assessed.
- **C1 confidentiality and GDPR overlap:** The C1 criteria and GDPR both address confidentiality of personal information, but C1 is broader — it covers any confidential information committed to in customer agreements, not just personal data. Organizations with GDPR obligations can use C1 evidence (data classification, disposal records) to partially satisfy GDPR Article 5 (data minimization, storage limitation) and Article 32 (security).
- **PI1 evidence for financial services:** Processing integrity criteria are most material for financial data processors, payroll providers, and transaction processors. For these organizations, reconciliation records, exception reports, and out-of-balance reports are the primary PI1 evidence artifacts. The `processing_control_records` fixture should map to whatever reconciliation/error reporting system the organization uses.
- **CC9.2 and SOC 2-on-SOC 2:** A common pattern for critical vendor assessment is relying on the vendor's own SOC 2 Type II report. This is the "inclusive" vs. "carve-out" method question. If a vendor's SOC 2 is carve-out, the service organization must address those controls independently. The system description must accurately represent which method applies to each subservice organization.
