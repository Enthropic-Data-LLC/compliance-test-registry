# Assumption Registry — Template and Field Reference

**Document version:** 2026.05
**Last updated:** 2026-05-20
**Purpose:** Standardizes the structure and approval workflow for PARAMETERIZED assumptions across all frameworks in the Compliance Test Case Registry. Every PARAMETERIZED test has at least one assumption entry in its framework's `_index.md` — this document defines the fields, approval workflow, and staleness enforcement rules.

---

## Why Assumptions Are First-Class Objects

A PARAMETERIZED test passes or fails based on data *given a documented assumption*. Without the assumption, the test makes no claim at all. The assumption is therefore load-bearing — as load-bearing as the test code itself.

If the assumption is wrong (the regulatory interpretation changed, the organization's scope changed, the risk tolerance was revised), the test produces the right answer to the wrong question. This is worse than no test at all, because it creates false confidence.

The assumption registry exists to prevent assumption rot: the slow drift between what the assumption says and what is actually true.

---

## Assumption File Structure

Each assumption is a block in the framework's `_index.md` assumption registry section, OR an individual YAML file in a future `assumptions/` directory. The YAML structure is canonical:

```yaml
assumption:
  id: "ASSUME-{FRAMEWORK}-{NUMBER}"          # e.g., ASSUME-HIPAA-001
  framework: "{framework-path}"              # e.g., "hipaa" or "nist/sp800-171"
  regulation_ref: "{section reference}"      # e.g., "45 CFR §164.312(a)(2)(iv)"
  requirement: |
    One-sentence description of the requirement this assumption serves.
    Quoted from the regulation where possible.
  assumption_text: |
    The specific interpretation, scope decision, or parameter value this
    assumption establishes. This is the human judgment that Pattern 2 tests
    are conditioned on.
  classification: "PARAMETERIZED"            # Always PARAMETERIZED for this registry
  rationale: |
    Why this interpretation was chosen. What alternatives were considered.
    What regulatory guidance, enforcement history, or legal opinion supports it.
  constraints: |
    Conditions under which this assumption would be WRONG and must be revised.
    e.g., "Assumption invalid if organization processes > X records" or
    "Assumption invalid if OCR issues clarifying guidance on this point."
  approved_by: "{name or role}"              # e.g., "CISO" or "Legal Counsel"
  approval_date: "YYYY-MM-DD"
  review_frequency_days: {integer}           # 365 for annual; 180 for semi-annual
  review_due_date: "YYYY-MM-DD"             # approval_date + review_frequency_days
  hash: "{sha256 of assumption_text}"        # Content hash — detects silent edits
  status: "ACTIVE"                           # ACTIVE | UNDER_REVIEW | SUPERSEDED | REJECTED
  superseded_by: null                        # ID of replacement assumption if SUPERSEDED
  related_tests:
    - "{test_id_1}"                          # IDs of Pattern 2 tests that use this assumption
    - "{test_id_2}"
```

---

## Field Reference

### Required fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique identifier. Format: `ASSUME-{FRAMEWORK}-{3-digit number}`. Examples: `ASSUME-HIPAA-001`, `ASSUME-800171-042` |
| `framework` | string | Directory path from `compliance_entities/` root. Matches the `_index.md` parent directory |
| `regulation_ref` | string | Specific section being interpreted: CFR citation, ISO clause number, standard section |
| `requirement` | string | The regulatory requirement text this assumption addresses. Quote the source where possible |
| `assumption_text` | string | The assumption itself — the human judgment that Pattern 2 tests are conditioned on |
| `approved_by` | string | Named individual or role who approved this assumption |
| `approval_date` | date | ISO 8601 date of most recent approval |
| `review_frequency_days` | integer | How many days between required reviews |
| `review_due_date` | date | Computed: approval_date + review_frequency_days |
| `status` | enum | ACTIVE, UNDER_REVIEW, SUPERSEDED, REJECTED |

### Recommended fields

| Field | Type | Description |
|---|---|---|
| `rationale` | string | Justification for the chosen interpretation |
| `constraints` | string | Conditions that would invalidate this assumption |
| `hash` | string | SHA-256 of `assumption_text` content — CI detects tampering |
| `related_tests` | list | Test IDs that depend on this assumption |
| `superseded_by` | string | If SUPERSEDED, the ID of the replacement |

---

## Staleness Enforcement Rules

The CI/CD pipeline enforces the following:

### Rule 1: Expired review = test failure

```python
def assumption_is_stale(assumption) -> bool:
    return date.today() > assumption.review_due_date

# In CI: Pattern 2 test using a stale assumption → FAIL with message:
# "ASSUMPTION STALE: ASSUME-HIPAA-001 review due 2025-03-15, today is 2025-07-01.
#  Compliance claim suspended until assumption is re-approved."
```

### Rule 2: Hash mismatch = test failure

If `assumption_text` was edited without updating `approval_date` and `hash`, the CI pipeline treats the assumption as invalid:

```python
def assumption_hash_valid(assumption) -> bool:
    return hashlib.sha256(assumption.assumption_text.encode()).hexdigest() == assumption.hash
```

### Rule 3: UNDER_REVIEW status = test warning (not failure)

An assumption in UNDER_REVIEW status generates a CI warning but does not fail the pipeline. This allows review to proceed without blocking deployments. The window is bounded:

```python
UNDER_REVIEW_GRACE_PERIOD_DAYS = 30  # After 30 days in UNDER_REVIEW, escalates to failure
```

### Rule 4: REJECTED assumption = test blocked

A REJECTED assumption means the interpretation was found to be incorrect. All Pattern 2 tests using it are blocked until a replacement ACTIVE assumption is created.

---

## Review Workflow

### Standard annual review

1. CI generates staleness warning 30 days before `review_due_date`
2. Assigned reviewer (from `approved_by` field) re-evaluates the assumption
3. If unchanged: update `approval_date` to today; recompute `review_due_date`; recompute `hash`; commit
4. If changed: draft new `assumption_text`; update all fields; change `status` of old to `SUPERSEDED`; set `superseded_by` to new ID

### Triggered review (regulatory change)

When a regulation changes:
1. Search assumption registry for all `regulation_ref` values matching the changed regulation
2. Set status to `UNDER_REVIEW` for all matching assumptions
3. Legal/compliance reviews each within 30 days
4. Approve (no change), revise, or reject

### Approval authority by assumption type

| Assumption type | Minimum approval authority |
|---|---|
| Scope definition (who is in scope) | CISO + Legal Counsel |
| Technical interpretation (how to implement a control) | CISO or designated SME |
| Risk acceptance (acceptable residual risk level) | Executive sponsor + CISO |
| Regulatory interpretation (what the regulation means) | Legal Counsel |
| Compensating control acceptance | CISO + auditor concurrence |

---

## Standard Review Frequencies by Framework

| Framework cluster | Recommended review frequency | Rationale |
|---|---|---|
| NIST 800-171 / CMMC | 365 days | Annual SPRS score resubmission |
| HIPAA / GDPR / CCPA | 365 days | Annual privacy program review |
| PCI DSS | 365 days | Annual SAQ or QSA assessment |
| NERC CIP | 365 days | Annual internal audit |
| OSHA / EPA | 180 days | Regulatory change frequency |
| ISO 27001 / SOC 2 | 365 days | Annual audit cycle |
| ITAR / EAR | 365 days + triggered by Commerce/State guidance | Export control classification is high-stakes |
| EU AI Act | 180 days | Rapidly evolving implementing regulations |

---

## Example Assumptions

### ASSUME-HIPAA-001

```yaml
assumption:
  id: "ASSUME-HIPAA-001"
  framework: "hipaa"
  regulation_ref: "45 CFR §164.312(a)(2)(iv)"
  requirement: |
    Implement a mechanism to encrypt and decrypt electronic protected health
    information. (Addressable — required unless alternative equivalent measure
    is implemented.)
  assumption_text: |
    Organization treats encryption of ePHI at rest as REQUIRED (not optional
    despite Addressable designation) for all systems in scope. No alternative
    equivalent measure is asserted. AES-256 or equivalent is the minimum standard.
  rationale: |
    OCR enforcement pattern treats lack of encryption as a significant risk factor
    in breach investigations. No documented case where 'no encryption' was accepted
    as an equivalent alternative. Risk of breach settlement outweighs implementation cost.
  constraints: |
    Assumption would need revision if organization acquires a legacy system where
    encryption is technically infeasible — in that case, compensating controls
    (network isolation, enhanced monitoring) should be documented separately.
  approved_by: "CISO"
  approval_date: "2026-01-15"
  review_frequency_days: 365
  review_due_date: "2027-01-15"
  status: "ACTIVE"
  superseded_by: null
  related_tests: ["test_hipaa_312_a2iv_encryption_at_rest"]
```

### ASSUME-CUI-001

```yaml
assumption:
  id: "ASSUME-CUI-001"
  framework: "nist/sp800-171"
  regulation_ref: "NIST SP 800-171 §3.1.1 / CUI Registry"
  requirement: |
    Limit information system access to authorized users, processes acting on
    behalf of authorized users, and devices (including other information systems).
  assumption_text: |
    CUI boundary for this organization is defined as: all systems processing
    technical data subject to distribution statements B–F and all export-controlled
    technical data. Business systems (HR, finance, marketing) are OUT of CUI boundary
    unless they store or process documents containing CUI.
  rationale: |
    NIST SP 800-171A and DCSA guidance allow organizations to define CUI boundary
    based on data flow analysis. This boundary was established via data flow
    assessment completed 2025-11-01 by ISSO with Program Manager concurrence.
  constraints: |
    Boundary must be re-evaluated if organization takes on new contracts with
    different CUI categories, if data flows change (new integration with business
    systems), or if DCSA assessment identifies boundary gaps.
  approved_by: "ISSO + Program Manager"
  approval_date: "2025-11-01"
  review_frequency_days: 365
  review_due_date: "2026-11-01"
  status: "ACTIVE"
  superseded_by: null
  related_tests: ["test_cui_boundary_access_control", "test_cui_system_inventory"]
```
