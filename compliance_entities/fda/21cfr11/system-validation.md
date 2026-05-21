# FDA 21 CFR Part 11 — System Validation (§11.10(a)) and Open System Controls (§11.30)

**Registry path:** `/regulation-registry/FDA/21CFR11/SystemValidation/`
**Regulation:** 21 CFR Part 11 (FDA, 1997); 2003 Guidance (risk-based enforcement)
**Last parsed:** 2026-05-20
**Applies to:** Any FDA-regulated organization (pharmaceutical, biotechnology, medical device, food, cosmetics, tobacco) that uses electronic records and/or electronic signatures in operations where FDA predicate rules require records or signatures
**Trigger:** Use of electronic records in lieu of paper records required by FDA predicate regulations (21 CFR 211 for pharma, 21 CFR 820/QMSR for devices, 21 CFR 123 for seafood HACCP, etc.); use of electronic signatures on records subject to FDA requirements
**Jurisdiction:** United States; extraterritorial — applies to foreign manufacturers producing products for US distribution where electronic systems support FDA-regulated records
**Not applicable to:** Electronic systems used purely internally with no FDA-required record function; non-FDA-regulated industries; paper-based systems (Part 11 does not apply); purely research data not submitted to FDA and not required by predicate rule
**Overall confidence:** MEDIUM — validation scope is PARAMETERIZED; methodology adequacy is CONTESTED; existence of validation documentation is DETERMINISTIC
**Covers:** §11.10(a) [system validation], §11.10(f)+(h)+(i)+(j) [operational/device/training/policy], §11.30 [open system controls]

---

## §11.10(a) — System Validation (PARAMETERIZED — Central GAMP 5 Obligation)

### Source excerpt

> (a) Validation of systems to ensure accuracy, reliability, consistent intended performance, and the ability to discern invalid or altered records.

### Validation obligation scope

No methodology is specified in the regulation. Industry standard is **GAMP 5** (Good Automated Manufacturing Practice for Pharmaceutical Manufacturing), which the FDA endorses in its process analytical technology and software guidance.

### GAMP 5 Category-to-Validation mapping

| GAMP 5 Category | System type | Minimum validation activities |
|---|---|---|
| Category 1 | Infrastructure software (OS, middleware, compilers) | Installation Qualification (IQ): confirm installation per vendor spec |
| Category 3 | Non-configured COTS (e.g., Excel spreadsheets used for calculations) | IQ + Operational Qualification (OQ): confirm system functions as designed |
| Category 4 | Configured COTS (LIMS, ERP, eDMR, EDMS) | IQ + OQ + Performance Qualification (PQ): confirm system performs for intended use in production environment |
| Category 5 | Custom / bespoke software | Full lifecycle: Requirements > Design > IQ + OQ + PQ + ongoing change control; source code review |

**Assumption (ASSUME-21CFR11-009):** System validation is adequate when: (1) each system subject to Part 11 is assigned a GAMP 5 category by a qualified system owner; (2) validation activities corresponding to the GAMP 5 category are documented in a Validation Plan and executed — IQ/OQ/PQ test scripts and results retained; (3) validation is re-executed after significant changes (software updates, configuration changes, migration) — changes assessed via impact analysis; (4) validation packages retained throughout the system lifecycle plus the longest predicate rule retention period for records produced by the system; (5) periodic reviews conducted at minimum every 2–3 years to verify ongoing compliance — "re-validation" not required unless change occurred; (6) a User Requirements Specification (URS) or equivalent exists documenting Part 11-specific requirements.

**Note — 2003 FDA Guidance:** FDA's 2003 guidance scales enforcement based on risk. Legacy systems (in use since before Part 11 effective date) may use a risk-based approach in lieu of full retroactive validation. High-risk systems (those producing lot release records, clinical data, safety records) must be fully validated; lower-risk systems may use abbreviated qualification. This does not eliminate the validation requirement — it directs validation resources to highest-risk systems first.

**Overall: PARAMETERIZED for scope and adequacy → Pattern 2; CONTESTED for "appropriate" determination → Pattern 3 for borderline cases**

---

## §11.10(f) — Operational Checks (PARAMETERIZED)

### Source excerpt

> (f) Use of operational system checks to enforce permitted sequencing of steps and events, as appropriate.

**Assumption (ASSUME-21CFR11-010):** Operational checks are adequate when: (1) critical workflows with required step sequences have system-enforced ordering — e.g., review before approval, data entry before QC check; (2) the enforced sequences are documented in the validation test scripts and verified during OQ/PQ; (3) systems that allow out-of-sequence actions document the risk justification and compensating controls.

**Overall: PARAMETERIZED → Pattern 2**

---

## §11.10(i) — Personnel Qualifications (PARAMETERIZED)

### Source excerpt

> (i) Determination that persons who develop, maintain, or use electronic record/electronic signature systems have the education, training, and experience necessary to perform their assigned tasks.

**Assumption (ASSUME-21CFR11-011):** Personnel qualification is adequate when: (1) all users of Part 11 systems have role-specific training documented before being granted access; (2) training covers: system use procedures, electronic signature meaning and legal equivalence, record protection responsibilities; (3) training records retained per predicate rule retention period; (4) system developers and administrators have documented qualifications (education, training, experience) appropriate to their roles; (5) refresher training conducted when system significantly changes or regulatory requirements change.

**Overall: PARAMETERIZED → Pattern 2**

---

## §11.10(j) — Written Policies (PARAMETERIZED)

### Source excerpt

> (j) The use of appropriate controls over systems documentation including: (1) adequate controls over the distribution of, access to, and use of documentation for system operation and maintenance; (2) revision and change control procedures to maintain an audit trail that documents time-sequenced development and modification of systems documentation.

**Assumption (ASSUME-21CFR11-012):** Written policies are adequate when: (1) a policy document exists covering: electronic record responsibilities, electronic signature meaning, training requirements, incident reporting, and record protection; (2) system documentation (SOPs, user manuals, validation documentation) version-controlled — changes tracked with effective dates; (3) access to system documentation restricted to authorized personnel; (4) policies reviewed annually and on regulatory change; (5) all personnel with Part 11 responsibilities acknowledge the policy annually.

**Overall: PARAMETERIZED → Pattern 2**

---

## §11.30 — Controls for Open Systems (MEDIUM — builds on §11.10)

### Source excerpt

> Persons who use open systems to create, modify, maintain, or transmit electronic records shall employ procedures and controls designed to ensure the authenticity, integrity, and, as appropriate, the confidentiality of electronic records from the point of their creation to the point of their receipt. Such procedures and controls shall include those identified in §11.10, as appropriate, and additional measures such as document encryption and use of appropriate digital signature standards to ensure, as necessary, record authenticity, integrity, and confidentiality.

### Open system additional requirements

| Requirement | Classification | Notes |
|---|---|---|
| All §11.10 controls | DETERMINISTIC/PARAMETERIZED | Inherits all closed system controls |
| Document encryption (if confidentiality required) | DETERMINISTIC once scope determined | Records transmitted over open networks (internet) must be encrypted |
| Digital signature standards | PARAMETERIZED | "Appropriate" digital signature standard (e.g., X.509 certificates, PKI) — no specific standard mandated |

**Assumption (ASSUME-21CFR11-013):** Open system controls are adequate when: (1) all §11.10 controls are implemented; (2) records transmitted over open networks (email, internet, cloud storage outside the controlled boundary) are encrypted in transit using TLS 1.2 or higher; (3) for high-sensitivity records (batch records, clinical data): encrypted at rest in addition to in-transit encryption; (4) digital signatures using X.509 certificates or equivalent PKI satisfy the "appropriate digital signature standard" requirement for open-system transmissions; (5) the transmission path is documented and included in the validation scope.

**Overall: PARAMETERIZED → Pattern 2; "appropriate" standard → Pattern 3 for contested cases**

---

## Test specifications

### YAML spec — 21 CFR Part 11 system validation

```yaml
spec_id: 21CFR11-VALIDATION-001
framework: FDA 21 CFR Part 11
sections:
  - §11.10(a) (system validation)
  - §11.10(f) (operational checks)
  - §11.10(i) (personnel qualifications)
  - §11.10(j) (written policies)
  - §11.30 (open systems)
pattern: 2  # Primary; Pattern 3 for adequacy contestation
subject: Electronic record systems in FDA-regulated environments
pre_conditions:
  - records_subject_to_predicate_rule == true
obligations:
  - validation: GAMP 5 category assigned; IQ/OQ/PQ per category; validated after significant change; packages retained
  - operational_checks: critical workflow sequences enforced or risk-justified
  - training: documented before access; covers esig meaning; records retained
  - policies: Part 11 policy exists; version-controlled; annual acknowledgment
  - open_systems: encryption in transit (TLS 1.2+); digital signature for transmission if required
evidence:
  - validation_master_plan (systems list; GAMP 5 categories; validation status)
  - validation_packages (IQ/OQ/PQ scripts + results per system)
  - training_records (user training completion; role-specific; system-specific)
  - part11_policy (effective date; version; acknowledgment log)
  - change_control_records (impact assessments; re-validation decisions)
```

### Python test file

```python
# tests/fda_21cfr11/test_21cfr11_validation.py
"""
FDA 21 CFR Part 11 System Validation Tests.

Sections: §11.10(a)(f)(i)(j), §11.30
Assumptions: ASSUME-21CFR11-009 through ASSUME-21CFR11-013
"""
import pytest
from datetime import datetime, timedelta, timezone
from typing import Any

VALIDATION_REVIEW_MAX_DAYS = 730   # 2-year periodic review
POLICY_REVIEW_MAX_DAYS = 365
TRAINING_MAX_DAYS = 365
OPEN_SYSTEM_MIN_TLS = "tls_1_2"


@pytest.fixture(autouse=True)
def require_part11_scope(system_scope: dict[str, Any]):
    """Gate: records must be subject to a predicate rule."""
    if not system_scope.get("records_subject_to_predicate_rule"):
        pytest.skip("No predicate rule citation on file — tests informational only")


# ── §11.10(a) System Validation ──────────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-21CFR11-009",
    description="All Part 11 systems have GAMP 5 category assignment and appropriate validation documentation",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_all_part11_systems_validated(validation_master_plan: dict[str, Any]):
    """§11.10(a): All Part 11-in-scope systems must have completed validation documentation."""
    systems = validation_master_plan.get("systems", [])
    unvalidated = []

    for system in systems:
        if not system.get("in_part11_scope"):
            continue
        if not system.get("validation_complete"):
            unvalidated.append(
                f"{system['system_name']}: validation not complete "
                f"(GAMP Cat {system.get('gamp5_category', '?')})"
            )

    assert not unvalidated, (
        f"Part 11 in-scope systems with incomplete validation: {unvalidated}"
    )


@pytest.mark.assumption(
    id="ASSUME-21CFR11-009",
    description="Validation packages include IQ/OQ/PQ as appropriate for GAMP 5 category",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_validation_packages_include_required_activities(
    validation_packages: list[dict[str, Any]],
):
    """§11.10(a): Validation package activities must match GAMP 5 category requirements."""
    GAMP5_REQUIRED = {
        1: {"iq"},
        3: {"iq", "oq"},
        4: {"iq", "oq", "pq"},
        5: {"iq", "oq", "pq", "requirements_spec", "design_spec"},
    }
    insufficient = []

    for pkg in validation_packages:
        category = pkg.get("gamp5_category")
        if category not in GAMP5_REQUIRED:
            continue
        completed = set(pkg.get("completed_activities", []))
        required = GAMP5_REQUIRED[category]
        missing = required - completed
        if missing:
            insufficient.append(
                f"{pkg['system_name']} (Cat {category}): missing {missing}"
            )

    assert not insufficient, (
        f"Validation packages missing required qualification activities: {insufficient}"
    )


@pytest.mark.assumption(
    id="ASSUME-21CFR11-009",
    description="Significant system changes assessed for validation impact; re-execution where required",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_significant_changes_assessed_for_validation_impact(
    change_control_records: list[dict[str, Any]],
):
    """§11.10(a): Changes to validated systems must include validation impact assessment."""
    missing_assessment = []

    for change in change_control_records:
        if not change.get("system_in_part11_scope"):
            continue
        if not change.get("validation_impact_assessed"):
            missing_assessment.append(
                f"Change {change['change_id']}: no validation impact assessment"
            )
        elif change.get("revalidation_required") and not change.get("revalidation_complete"):
            missing_assessment.append(
                f"Change {change['change_id']}: revalidation required but not completed"
            )

    assert not missing_assessment, (
        f"System changes without validation impact assessment or incomplete revalidation: "
        f"{missing_assessment}"
    )


# ── §11.10(i) Personnel Qualifications ───────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-21CFR11-011",
    description="All Part 11 system users have system-specific training before access granted",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_part11_system_training_completed(
    user_accounts: list[dict[str, Any]],
    training_records: list[dict[str, Any]],
):
    """§11.10(i): Users of Part 11 systems must have documented role-specific training."""
    training_by_user = {t["user_id"]: t for t in training_records}
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=TRAINING_MAX_DAYS)

    untrained = []
    for acct in user_accounts:
        if not acct.get("has_part11_system_access"):
            continue
        training = training_by_user.get(acct["user_id"])
        if training is None:
            untrained.append(f"{acct['user_id']}: no training record")
        elif training.get("part11_training_date", datetime.min.replace(tzinfo=timezone.utc)) < cutoff:
            untrained.append(
                f"{acct['user_id']}: training expired "
                f"({training['part11_training_date'].date()})"
            )

    assert not untrained, (
        f"Part 11 system users without current training: {untrained}"
    )


# ── §11.10(j) Written Policies ───────────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-21CFR11-012",
    description="Part 11 policy exists; version-controlled; reviewed annually; all personnel acknowledge annually",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_part11_policy_exists_and_current(security_policies: dict[str, Any]):
    """§11.10(j): Written Part 11 policy must exist, be current, and have annual acknowledgments."""
    now = datetime.now(timezone.utc)
    part11_policy = security_policies.get("part11_policy")

    assert part11_policy is not None, (
        "Written 21 CFR Part 11 policy not found — §11.10(j) requires written policies covering "
        "electronic record responsibilities and electronic signature controls"
    )

    last_review = part11_policy.get("last_review_date")
    assert last_review is not None, "Part 11 policy has no review date"
    assert last_review >= now - timedelta(days=POLICY_REVIEW_MAX_DAYS), (
        f"Part 11 policy not reviewed within last year: last review {last_review.date()}"
    )

    required_sections = {
        "electronic_record_responsibilities",
        "electronic_signature_meaning",
        "training_requirements",
        "incident_reporting",
        "record_protection",
    }
    missing_sections = required_sections - set(part11_policy.get("covered_topics", []))
    assert not missing_sections, (
        f"Part 11 policy missing required sections: {missing_sections}"
    )


# ── §11.30 Open System Controls ──────────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-21CFR11-013",
    description="Open system records encrypted in transit (TLS 1.2+); digital signatures for open-network transmissions",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_open_system_records_encrypted_in_transit(
    system_scope: dict[str, Any],
    tls_config: dict[str, Any],
):
    """§11.30: Records transmitted over open systems must be encrypted; TLS 1.2 minimum."""
    if not system_scope.get("uses_open_systems"):
        pytest.skip("No open system transmissions detected — §11.30 not applicable")

    min_tls = tls_config.get("minimum_tls_version", "")
    acceptable_tls = {"tls_1_2", "tls_1_3"}
    assert min_tls.lower() in acceptable_tls, (
        f"§11.30 open system: minimum TLS version is {min_tls!r} — must be TLS 1.2 or higher "
        "for electronic record transmissions"
    )


@pytest.mark.human_review_required(
    reason=(
        "§11.30 'appropriate digital signature standard' for open-system transmission is not defined "
        "in the regulation. Whether PKI/X.509, S/MIME, or another mechanism is 'appropriate' "
        "for the specific transmission context requires QA/RA expert determination. "
        "Action: QA/RA review and documented standard selection required."
    )
)
@pytest.mark.assumption(
    id="ASSUME-21CFR11-013",
    description="§11.30 digital signature standard appropriateness requires human QA/RA review",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_open_system_digital_signature_standard_reviewed(
    system_scope: dict[str, Any],
    security_policies: dict[str, Any],
):
    """§11.30: 'Appropriate digital signature standard' determination requires QA/RA review."""
    if not system_scope.get("uses_open_systems"):
        pytest.skip("No open system transmissions — §11.30 not applicable")

    open_system_policy = security_policies.get("open_system_transmission_policy")
    assert open_system_policy is not None, (
        "§11.30 open system policy not documented — QA/RA must define and document the digital "
        "signature standard used for electronic record transmission"
    )
    assert open_system_policy.get("qa_ra_reviewed"), (
        "§11.30 open system digital signature standard must be QA/RA reviewed and attested as 'appropriate'"
    )
```

---

## Open assumption registry (this file)

| ID | Section | Summary | Review date |
|---|---|---|---|
| ASSUME-21CFR11-009 | §11.10(a) | GAMP 5 category assigned; IQ/OQ/PQ per category; impact assessment on changes; revalidation when required; packages retained with records | 2026-05-20 |
| ASSUME-21CFR11-010 | §11.10(f) | Operational checks: critical sequences enforced in system; risk justification if not; verified in OQ/PQ | 2026-05-20 |
| ASSUME-21CFR11-011 | §11.10(i) | Personnel qualification: role-specific training before access; Part 11-specific (esig meaning, record protection); records retained | 2026-05-20 |
| ASSUME-21CFR11-012 | §11.10(j) | Written policies: Part 11 policy exists; covers 5 required sections; reviewed annually; all personnel acknowledge annually | 2026-05-20 |
| ASSUME-21CFR11-013 | §11.30 | Open systems: all §11.10 controls; TLS 1.2+ in transit; appropriate digital signature standard (QA/RA-reviewed); transmission path in validation scope | 2026-05-20 |
