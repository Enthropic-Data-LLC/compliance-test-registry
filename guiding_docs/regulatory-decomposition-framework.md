# Regulatory Decomposition Framework (RDF)
### A Methodology for Translating Natural Language Regulations into Executable Test Cases

---

## Overview

The Regulatory Decomposition Framework (RDF) is a systematic methodology for converting ambiguous natural language regulations into deterministic, version-controlled, executable compliance test cases. It is the operational backbone of **Compliance-Driven Development (CDD)** — the application of Test-Driven Development (TDD) principles to regulatory compliance.

**Core premise:** Every regulation can be decomposed into four extractable elements. The degree to which those elements are deterministic defines the automation strategy. Ambiguity is not a blocker — it is a first-class data object to be surfaced, documented, and resolved.

---

## Stage 1: Regulatory Parsing — The 4-Element Extraction

Every regulation, regardless of complexity, contains four extractable structural elements. If any element cannot be extracted, the regulation is flagged as ambiguous before any code is written.

| Element | Question to Answer | Example (NERC CIP-002) |
|---|---|---|
| **Subject** | Who or what does this apply to? | BES Cyber Systems |
| **Condition** | Under what circumstances does the obligation trigger? | Aggregate capacity > 1,500 MW |
| **Obligation** | What must be true when the condition is met? | Classified as Medium Impact |
| **Evidence** | How is compliance demonstrated and verified? | `impact_rating` field in CMDB asset schema |

> **Rule:** If all four elements can be extracted with precision, the regulation is a candidate for full automation. If any element resists extraction, escalate to Stage 2 for ambiguity classification before proceeding.

---

## Stage 2: Ambiguity Classification

Each extracted element is independently scored against a four-tier classification system. The lowest-scoring element determines the overall test confidence level for the regulation.

| Classification | Definition | Engineering Response |
|---|---|---|
| **DETERMINISTIC** | Exact threshold, boolean, or enumerable value. Direct code translation. | Automate fully. No human review required. |
| **PARAMETERIZED** | Qualitative but bounded. Requires a defined assumption to become testable. | Automate with documented assumption. Flag assumption for periodic review. |
| **CONTESTED** | Industry or legal interpretation varies. No consensus on meaning. | Surface via test. Require human determination and cryptographic sign-off. |
| **UNRESOLVABLE** | Genuinely undefined. Cannot be resolved by internal policy. | Escalate to external legal counsel or standards body rulemaking petition. Do not automate. |

### Worked Examples

**Deterministic regulation (CIP-002-R1.1):**

> *"High Impact Rating shall be assigned to each BES Cyber System used by and located at a Control Center performing the functional obligations of a Reliability Coordinator or Balancing Authority."*

| Element | Classification | Rationale |
|---|---|---|
| Subject | DETERMINISTIC | BES Cyber System — defined term |
| Condition | DETERMINISTIC | Control Center + enumerated functional roles |
| Obligation | DETERMINISTIC | High Impact — explicit categorical assignment |
| Evidence | DETERMINISTIC | `impact_rating` field in asset schema |

**Overall: DETERMINISTIC → Full Automation**

---

**Parameterized regulation (CIP-007-R3.1):**

> *"Implement security patches within 35 calendar days of availability, or document compensating measures where patching is not technically feasible."*

| Element | Classification | Rationale |
|---|---|---|
| Subject | DETERMINISTIC | Cyber Assets — defined term |
| Condition | PARAMETERIZED | "Not technically feasible" is subjective |
| Obligation | PARAMETERIZED | "Compensating measures" undefined in standard |
| Evidence | CONTESTED | Industry interpretation varies on adequacy |

**Overall: CONTESTED → Partial Automation with Human Sign-off Required**

---

## Stage 3: Test Case Specification (YAML)

Every parsed regulation produces a structured YAML specification before any code is written. This document is the authoritative source of truth for the test implementation, human assumptions, and audit trail.

### Template: Deterministic Regulation

```yaml
regulation_id: CIP-002-R1.1
revision: 5.1a
source_text: >
  High Impact Rating shall be assigned to each BES Cyber System used by and
  located at a Control Center performing the functional obligations of a
  Reliability Coordinator or Balancing Authority.

extracted_elements:
  subject: "BES Cyber System"
  condition: "is_control_center == true AND functional_role IN
              [Reliability Coordinator, Balancing Authority]"
  obligation: "impact_rating == High"
  evidence: "asset_schema.impact_rating"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log: []
test_confidence: HIGH
generated_test: "tests/CIP-002/test_R1_1.py"
```

### Template: Parameterized / Contested Regulation

```yaml
regulation_id: CIP-007-R3.1
revision: "6"
source_text: >
  Implement security patches within 35 calendar days of availability,
  or document compensating measures where patching is not technically feasible.

extracted_elements:
  subject: "Cyber Assets within ESP"
  condition: "patch_available == true AND technically_feasible == [PARAMETERIZED]"
  obligation: "days_to_apply <= 35 OR compensating_measure_documented == true"
  evidence: "patch_management_record.applied_date, compensating_measure_log"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: PARAMETERIZED
  obligation: PARAMETERIZED
  evidence: CONTESTED

overall_classification: CONTESTED
human_review_required: true
test_confidence: MEDIUM

legal_assumption_log:
  - assumption_id: ASSUME-007-001
    assumption_text: >
      "Technically feasible" is defined as: vendor patch available AND
      validated in isolated test environment AND approved change window exists
      within the 35-day period.
    assumed_by: "Engineering Lead"
    approved_by: "Compliance Officer"
    date: "2025-01-15"
    review_frequency_days: 365
    cryptographic_hash: "sha256:a3f9c2d..."

generated_test: "tests/CIP-007/test_R3_1.py"
```

---

## Stage 4: Code Generation Patterns

Each confidence tier maps to a distinct test implementation pattern. This ensures the test suite is honest about its own certainty.

### Pattern 1: HIGH Confidence — Direct Assertion

Used when all four elements are DETERMINISTIC.

```python
def test_CIP002_R1_high_impact_control_center(live_assets):
    """
    CIP-002-R1.1: Control Centers performing Reliability Coordinator or
    Balancing Authority functions must be classified as High Impact.
    Confidence: HIGH | Human Review: NOT REQUIRED
    """
    high_impact_roles = {"Reliability Coordinator", "Balancing Authority"}

    for asset in live_assets:
        if asset["is_control_center"] and \
           set(asset["functional_roles"]).intersection(high_impact_roles):
            assert asset["impact_rating"] == "High", \
                f"CRITICAL VIOLATION: {asset['asset_id']} performs high-impact " \
                f"functional roles but is not classified HIGH IMPACT."
```

---

### Pattern 2: MEDIUM Confidence — Parameterized Assertion with Documented Assumption

Used when elements are PARAMETERIZED. The assumption is encoded directly and traceable.

```python
@pytest.mark.assumption(
    id="ASSUME-007-001",
    description="Technical feasibility defined as: vendor patch + test env + change window",
    approved_by="Compliance Officer",
    review_date="2025-01-15"
)
def test_CIP007_R3_patch_compliance(asset, patch_record):
    """
    CIP-007-R3.1: Patches must be applied within 35 days, or compensating
    measures documented where technically infeasible.
    Confidence: MEDIUM | Human Review: ASSUMPTION REQUIRED
    """
    if is_technically_feasible(asset, patch_record):
        assert patch_record.days_to_apply <= 35, \
            f"VIOLATION: {asset.id} patch applied in {patch_record.days_to_apply} days. " \
            f"Threshold: 35 days."
    else:
        assert compensating_measure_exists(asset), \
            f"VIOLATION: {asset.id} deemed infeasible but no compensating " \
            f"measure is documented."
```

---

### Pattern 3: LOW / CONTESTED Confidence — Human Surfacing Test

Used when elements are CONTESTED or UNRESOLVABLE. The test does not assert compliance — it asserts that a human determination exists and is current.

```python
@pytest.mark.human_review_required
@pytest.mark.contested(
    regulation="CIP-007-R3.1",
    reason="Industry interpretation varies on compensating measure adequacy"
)
def test_CIP007_R3_feasibility_requires_human_determination(asset):
    """
    This test does not determine compliance. It verifies that a valid,
    current human determination exists and has not become stale.
    Confidence: LOW | Human Review: MANDATORY
    """
    result = get_feasibility_assessment(asset)

    assert result is not None, \
        f"UNRESOLVED: {asset.id} has no feasibility determination on record. " \
        f"Human review required before asset can be considered compliant."

    assert result.reviewed_by is not None, \
        f"INCOMPLETE: {asset.id} feasibility record missing reviewer identity."

    assert result.review_date > (datetime.now() - timedelta(days=365)), \
        f"STALE REVIEW: {asset.id} feasibility determination is older than 12 months. " \
        f"Re-review required. Last reviewed: {result.review_date}"

    assert result.cryptographic_hash is not None, \
        f"INTEGRITY FAILURE: {asset.id} feasibility record lacks cryptographic attestation."
```

---

## Stage 5: Registry Architecture

All parsed regulations, generated tests, and human assumptions live in a structured, version-controlled registry. Every change is a git commit. Every audit is a diff.

```
/regulation-registry/
│
├── NERC-CIP/
│   ├── CIP-002-5.1a/
│   │   ├── R1.yaml                  ← Parsed specification
│   │   ├── R1_test.py               ← Generated test
│   │   └── R1_history.log           ← Assumption change history
│   │
│   ├── CIP-007-6/
│   │   ├── R3.yaml
│   │   ├── R3_test.py
│   │   └── assumptions/
│   │       └── ASSUME-007-001.yaml  ← Signed, dated, hashed assumption
│   │
│   └── _index.yaml                  ← Registry manifest with confidence summary
│
├── GDPR/
│   └── Article-32/
│       └── ...
│
└── _global/
    ├── assumption_registry.yaml     ← All cross-regulation assumptions
    └── contested_log.yaml           ← All CONTESTED items pending resolution
```

### Registry Manifest (`_index.yaml`)

```yaml
registry_version: "2025.01"
last_updated: "2025-01-15T14:32:00Z"

summary:
  total_regulations: 47
  fully_automated: 31         # DETERMINISTIC
  partially_automated: 12     # PARAMETERIZED
  human_required: 4           # CONTESTED
  unresolvable: 0             # UNRESOLVABLE — escalated externally

open_assumptions: 8
stale_reviews: 1
pending_escalations: 0
```

---

## Stage 6: CI/CD Integration

The test suite runs automatically on any change to the asset inventory schema. The pipeline enforces a strict gate before changes are committed to the live compliance record.

```
+---------------------+     +----------------------+     +-----------------------+
| Asset Change Event  | --> | RDF Test Suite       | --> | Result Classification |
| (CMDB / Discovery)  |     | All tiers execute    |     |                       |
+---------------------+     +----------------------+     +-----------------------+
                                                                    |
                              +------------------------------------+|+------------------------------------+
                              |                                    ||                                    |
                    +---------v---------+              +-----------v-----------+          +-------------v-----------+
                    | ALL GREEN         |              | PARAMETERIZED FAILURE |          | CONTESTED / HUMAN FLAG  |
                    | Auto-commit to    |              | Assumption violated.  |          | Block pipeline.         |
                    | compliance record.|              | Engineering review.   |          | Route to named reviewer.|
                    +-------------------+              +-----------------------+          +-------------------------+
```

### Audit Response Protocol

When a regulator requests evidence of compliance, the response is generated directly from the registry:

> *"Regulation CIP-002-R1.1 was parsed as DETERMINISTIC on 2024-11-01 (commit: `sha256:b7f2...`). Asset `SUB-ALPHA-PLC-04` was evaluated against `test_R1_1.py` at commit `sha256:c3a1...` on 2025-01-14T09:17:00Z. Test result: PASS. No human assumptions were required. Full execution log and asset schema snapshot attached."*

---

## Decision Tree: Regulation to Test

```
Regulation received
        |
        v
Extract 4 elements (Subject, Condition, Obligation, Evidence)
        |
        +---> Any element unextractable?
        |           |
        |           YES --> Flag as AMBIGUOUS. Return to regulation author
        |                   for clarification before proceeding.
        |
        v
Classify each element (DETERMINISTIC / PARAMETERIZED / CONTESTED / UNRESOLVABLE)
        |
        +---> Any element UNRESOLVABLE?
        |           |
        |           YES --> Escalate externally. Do not automate.
        |
        +---> Any element CONTESTED?
        |           |
        |           YES --> Pattern 3 (Human Surfacing Test). Require sign-off.
        |
        +---> Any element PARAMETERIZED?
        |           |
        |           YES --> Pattern 2 (Parameterized Assertion). Log assumption.
        |
        v
    All DETERMINISTIC --> Pattern 1 (Direct Assertion). Full automation.
```

---

## Appendix: Confidence Level Reference

| Level | Classification | Test Pattern | Audit Posture |
|---|---|---|---|
| HIGH | All elements DETERMINISTIC | Direct assertion | Fully automated. Cryptographic log sufficient. |
| MEDIUM | Any element PARAMETERIZED | Parameterized assertion | Automated with documented assumption. Assumption requires periodic human re-approval. |
| LOW | Any element CONTESTED | Human surfacing test | Automation verifies human determination exists and is current. Determination itself is manual. |
| NONE | Any element UNRESOLVABLE | No test generated | Escalated to external authority. Manually tracked until resolved. |

---

*Regulatory Decomposition Framework (RDF) v1.0*
*Companion methodology to: Continuous Compliance-Driven Development (CDD)*
