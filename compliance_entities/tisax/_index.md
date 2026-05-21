# TISAX — Trusted Information Security Assessment Exchange

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Information security of organizations in the automotive supply chain; primarily German OEMs and Tier 1/2 suppliers; protects vehicle project data, prototypes, and test vehicles
**Authority:** ENX Association (operated on behalf of VDA — German Association of the Automotive Industry)
**Enforcing context:** Contractual requirement from automotive OEMs (BMW, Daimler, Porsche, Volkswagen, and others) — required before receiving sensitive project data; TISAX label shared via ENX portal (not a public certificate)
**Current version:** VDA ISA 6.0 (Information Security Assessment — the underlying catalog); TISAX Process Regulation defines assessment process
**Note:** TISAX is the exchange mechanism; VDA ISA is the assessment catalog. Assessment performed by ENX-approved audit providers.

---

## Summary

| Metric | Count |
|---|---|
| VDA ISA control domains | 6 |
| Assessment levels (AL) | 3 (AL1 self-assessment / AL2 remote audit / AL3 on-site audit) |
| TISAX label types | Multiple (InfoSec / Prototype protection / Confidential data handling) |
| Sections parsed (individual files) | 2 (isms-hr-physical-controls.md + it-supplier-controls.md) |
| Fully automated (DETERMINISTIC) | MEDIUM — secure area access logging, visitor escort, access review, label validity gate |
| Partial automation (PARAMETERIZED) | Dominant — ISMS scope adequacy, risk treatment, crypto config, vuln mgmt, supplier assessment |
| Human-determination required (CONTESTED) | Low — supplier assessment adequacy requires human review |
| Open assumptions | 9 (ASSUME-TISAX-1_1-001/002, 2_1-001/002, 4_1-001/002/003, 5_1-001/002) |

---

## Scoping pre-condition

```python
def requires_tisax() -> bool:
    """
    True if organization has contractual obligation from automotive OEM/customer
    requiring TISAX label. Common triggers:
    - Receiving vehicle project data (CAD files, technical specifications)
    - Handling prototype vehicles or components
    - Processing test data, crash data, or pre-series information
    """

def assessment_level(data_sensitivity) -> int:
    """
    AL1: Normal — internal processes, self-assessment only (no ENX exchange)
    AL2: High — confidential data, remote audit by ENX provider
    AL3: Very high — prototype/test vehicle data, on-site audit
    Returns 1, 2, or 3.
    """
```

---

## VDA ISA 6.0 — 6 control domains

### 1. Information Security Management (ISMS)

| Control area | Confidence | Notes |
|---|---|---|
| IS management system (policies, organization) | DETERMINISTIC | Written ISMS scope and policy |
| Risk management | PARAMETERIZED | Risk assessment methodology and results |
| IS objectives and targets | DETERMINISTIC | Documented and measurable |
| Internal audit | DETERMINISTIC | Planned; records |
| Management review | DETERMINISTIC | Regular review of ISMS; records |

### 2. Human Resources

| Control area | Confidence | Notes |
|---|---|---|
| Security awareness and training | PARAMETERIZED | Training records; role-based content |
| Non-disclosure agreements | DETERMINISTIC | NDAs in place for personnel with access to project data |
| Screening | PARAMETERIZED | Background check process |

### 3. Physical Security

| Control area | Confidence | Notes |
|---|---|---|
| Secure area definition | DETERMINISTIC | Secure zones defined for prototype/confidential work |
| Access control — physical | DETERMINISTIC | Access restricted and logged |
| Visitor management | DETERMINISTIC | Visitor access controlled; escorts |
| Prototype protection measures | DETERMINISTIC (AL3) | Additional controls for prototype vehicles/components (camouflage, photography restrictions) |

### 4. IT / Information Security

| Control area | Confidence | Notes |
|---|---|---|
| Asset management | DETERMINISTIC | Asset inventory with classification |
| Access control — logical | DETERMINISTIC | Least privilege; review cycle |
| Cryptography | PARAMETERIZED | Encryption for confidential automotive data |
| Vulnerability management | PARAMETERIZED | Scanning and patching |
| Logging and monitoring | PARAMETERIZED | Audit logging; retention |
| Incident management | DETERMINISTIC | Written process; response records |

### 5. Supplier and Service Provider Management

| Control area | Confidence | Notes |
|---|---|---|
| Supplier security requirements | PARAMETERIZED | IS requirements flowed down to sub-suppliers |
| Supplier TISAX or equivalent | PARAMETERIZED | Sub-suppliers with access to confidential data must have equivalent IS assessment |

### 6. Prototype and Test Vehicle Protection (AL3 specific)

| Control area | Confidence | Notes |
|---|---|---|
| Prototype handling procedures | DETERMINISTIC | Written procedures for prototype identification, concealment, transportation |
| Photography/filming restrictions | DETERMINISTIC | Prohibitions documented and enforced |
| Event/public appearance security | PARAMETERIZED | Procedures for auto shows, test drives |

---

## Maturity level scoring (VDA ISA)

TISAX uses a 0-5 maturity scale for each control:

| Level | Description | DETERMINISTIC minimum |
|---|---|---|
| 0 | Incomplete — not implemented | Fails |
| 1 | Performed — implemented ad hoc | Below acceptable |
| 2 | Managed — planned, tracked | Minimum for most controls |
| 3 | Established — standardized process | Required for many AL2/AL3 controls |
| 4 | Predictable — quantitatively managed | Required for some critical AL3 controls |
| 5 | Optimizing — continuous improvement | Not typically required |

Target maturity for AL2/AL3 assessments: typically level 3 for all controls, level 4 for selected high-risk controls.

---

## TISAX assessment cycle — DETERMINISTIC timeline

| Milestone | Requirement |
|---|---|
| Initial assessment scope agreement | Before assessment begins |
| Assessment report issued | Within 3 months of final audit date |
| Label validity period | 3 years from assessment date |
| Re-assessment | Required before 3-year expiry |
| Corrective action plan (CAP) for non-conformities | Required before label issued |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| ISMS | TISAX VDA ISA, ISO 27001 | ISO 27001 certification accepted as partial evidence in some TISAX assessments |
| Physical security | TISAX VDA ISA §3, ISO 27001 Annex A (Physical controls) | Same physical access controls |
| Supplier security | TISAX VDA ISA §5, ISO 27001 §A.15, IATF 16949 §7.4 | Automotive supply chain extends IS requirements downstream |
| Incident management | TISAX VDA ISA §4, ISO 27001 §A.16, GDPR Art. 33 | Same incident response infrastructure |
| Non-disclosure | TISAX VDA ISA §2, ITAR §120 (technical data), GDPR Art. 28 | NDAs required across multiple frameworks |
