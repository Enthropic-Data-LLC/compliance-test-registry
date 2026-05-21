# ITAR / EAR — Parameterized Controls: License Requirements, Deemed Export, TCP, Training

**Registry path:** `/regulation-registry/ITAR-EAR/Parameterized-Controls/`
**Regulations:** ITAR (22 CFR 120–130), EAR (15 CFR 730–774)
**Last parsed:** 2026-05-20
**Applies to:** Any person or entity — US or foreign — that manufactures, exports, re-exports, transfers, or brokers: ITAR — defense articles and services on the US Munitions List (USML); EAR — dual-use items on the Commerce Control List (CCL). Includes 'deemed exports' (sharing controlled technology with foreign nationals in the US)
**Trigger:** Manufacturing, exporting, re-exporting, transferring, or brokering items on USML or CCL; employing or hosting foreign nationals with access to USML/CCL technology ('deemed export'); receiving technical data from a US person subject to ITAR/EAR
**Jurisdiction:** United States extraterritorial — applies globally to US-origin items, technology, and software; enforced by DDTC (State, ITAR) and BIS (Commerce, EAR)
**Not applicable to:** Purely domestic transfers with no export or foreign-national access; EAR99 items with no applicable export control classification number; publicly available information (EAR §734.3(b)(3)); fundamental research (EAR §734.8); news media activities
**Overall confidence:** MEDIUM (PARAMETERIZED); classification inputs are CONTESTED and must be human-attested before downstream tests are meaningful
**Covers:** License requirement matrix (EAR §742, ITAR §123), deemed export (EAR §734, ITAR §125.2), technology control plan (TCP), export control training records

---

## Pre-Condition: Classification Fixture

**All tests in this file depend on prior classification.** The classification fixture must be attested by a qualified export control expert (export counsel or ECO) before these tests transition from informational to enforcing mode.

```python
@pytest.fixture(autouse=True)
def require_current_classification(item_classification: dict, export_control_config: dict):
    if not export_control_config.get("export_control_program_active"):
        pytest.skip("Export control program not active — tests informational only")
    if not item_classification.get("classification_current"):
        pytest.skip(
            "Item classification is not current or has not been attested by qualified export counsel — "
            "downstream tests cannot run in enforcing mode"
        )
```

---

## EAR §740–742 / ITAR §123 — License Requirement Determination (PARAMETERIZED)

### Source excerpts

> **EAR §742:** Export license requirements are driven by the combination of: ECCN classification, reason for control (anti-terrorism, national security, nuclear non-proliferation, etc.), destination country, end-use, and end-user.
>
> **ITAR §123.1:** Any person who intends to export a defense article must obtain the prior written approval of the Directorate of Defense Trade Controls except as otherwise exempted.

### License requirement matrix (EAR — illustrative)

| ECCN category | Destination | License required? | Exception availability |
|---|---|---|---|
| EAR99 (not on CCL) | Non-embargoed | Generally No License Required (NLR) | N/A |
| 5E002 (encryption) | Most countries | License or ENC exception | ENC exception available for commercial products |
| 3E001 (microelectronics tech) | AT / CB / NS destinations | License required | LVS / TSR may apply for low-value items |
| Any ECCN | Embargoed countries (Iran, Cuba, etc.) | License required; generally not approved | Humanitarian exceptions only |
| Any item | Entity List party | License required; presumption of denial | License exception may be unavailable |

**Assumption (ASSUME-ITAR-004):** License requirement determination is adequate when: (1) ECCN is attested by a qualified reviewer (not self-classification for sensitive items); (2) license determination documented for each unique ECCN + destination + end-use + end-user combination; (3) license exceptions documented with: exception symbol (e.g., ENC, LVS, TSR, GOV), eligibility criteria met, and per-exception record keeping; (4) NLR determinations documented — "no license required" is an affirmative determination, not an absence of records; (5) license determinations reviewed when: ECCN changes, destination country restrictions change, or end-use changes.

**Overall: PARAMETERIZED → Pattern 2**

---

## EAR §734.13 / ITAR §125.2 — Deemed Export (PARAMETERIZED)

### Source excerpts

> **EAR §734.13:** Deemed export: the release of technology or source code subject to the EAR to a foreign national. Such release is "deemed" to be an export to the home country of the foreign national.
>
> **ITAR §125.2:** The export of technical data includes the oral, visual, or documentary disclosure of technical data to a foreign person, whether in the United States or abroad, except as provided in §125.4.

### Deemed export decision matrix

| Scenario | EAR treatment | ITAR treatment |
|---|---|---|
| Foreign national employee accesses EAR-controlled technology (not EAR99) | Deemed export to home country — may require license | — |
| Foreign national employee accesses ITAR-controlled technical data | Deemed export — requires license or government approval | ITAR §125.2 |
| Foreign national contractor in facility with controlled technology | Same as employee | Same as employee |
| Dual-national U.S. citizen | EAR: no deemed export (U.S. person); ITAR: no deemed export | No deemed export |
| Technology is "publicly available" | §734.7 "publicly available" exception may apply | §125.4(b)(13) "public domain" exception |
| Technology disclosed in university fundamental research | EAR fundamental research exclusion (§734.8) | ITAR fundamental research exclusion (§125.4(b)(3)) |

**Assumption (ASSUME-ITAR-005):** Deemed export compliance is adequate when: (1) all foreign nationals with access to controlled technology are identified in the deemed export log; (2) for each foreign national: ECCN of accessible technology and home country used to determine if license is required; (3) visa type considered — immigrant visa (LPR/green card) holders treated as U.S. persons for EAR; non-immigrant visa holders are foreign nationals; (4) exceptions documented: publicly available (§734.7), fundamental research (§734.8), publicly available ITAR (§125.4); (5) deemed export licenses or Technology Control Plan (TCP) access restrictions applied for unlicensed foreign nationals; (6) deemed export records retained 5 years.

**Overall: PARAMETERIZED → Pattern 2**

---

## Technology Control Plan (TCP) — PARAMETERIZED

### Source context

A Technology Control Plan is the primary facility-level document for preventing unauthorized access to ITAR/EAR controlled technology. It is required for all facilities with foreign national personnel or visitors who might encounter controlled technology.

### TCP required elements

| Element | Applicability | Classification |
|---|---|---|
| Scope: controlled technology and items covered | All facilities with TCP | DETERMINISTIC (existence) |
| Physical access controls (restricted areas, locks, badging) | Facilities with ITAR | PARAMETERIZED (adequacy) |
| Electronic access controls (file permissions, VPN, BYOD) | All facilities | PARAMETERIZED (adequacy) |
| Foreign national access procedures (visitor logs, escorting) | Facilities with foreign nationals | DETERMINISTIC (existence) |
| Employee training requirements (initial + annual) | All TCP facilities | DETERMINISTIC (existence) |
| Incident reporting procedure | All TCP facilities | DETERMINISTIC (existence) |
| TCP custodian designation | All facilities | DETERMINISTIC |
| Review and update schedule (minimum annual) | All facilities | DETERMINISTIC |
| DDTC registration number and USML categories covered | ITAR facilities | DETERMINISTIC |

**Assumption (ASSUME-ITAR-006):** Technology Control Plan is adequate when: (1) TCP is current (reviewed within last 12 months); (2) TCP covers all ITAR/EAR controlled technology and items at the facility; (3) foreign national access procedures documented — written authorization required for each foreign national before access; (4) physical and electronic access controls described and implemented; (5) TCP custodian designated by name and title; (6) TCP training completed by all personnel with access to controlled technology; (7) TCP reviewed when: foreign national population changes, controlled technology changes, or facility changes.

**TCP adequacy is PARAMETERIZED — whether the described controls are sufficient for the specific threat model is an ECO/legal judgment call, not fully automatable.**

**Overall: PARAMETERIZED → Pattern 2; adequacy determination → Pattern 3**

---

## Export Control Training Records (PARAMETERIZED)

### Source context

Both ITAR and EAR require exporters to maintain an effective compliance program, which courts and enforcement agencies consistently interpret to require regular employee training. Training records are key due diligence evidence.

**Assumption (ASSUME-ITAR-007):** Export control training is adequate when: (1) all personnel with export control responsibilities have completed initial training upon hire/role assignment; (2) annual refresher training completed; (3) training covers: classification basics, license requirements, denied party screening, deemed export, red flag recognition, violation reporting; (4) training completion records retained per §762 / §122.5 (5 years); (5) training content updated when regulations change materially (e.g., new entity list designations, regulation amendments).

**Overall: PARAMETERIZED → Pattern 2**

---

## Test specifications

### YAML spec — ITAR/EAR parameterized controls

```yaml
spec_id: ITAR-EAR-PARAM-001
framework: ITAR / EAR
regulations:
  - EAR §734 (deemed export scope)
  - EAR §740–742 (license exceptions and requirements)
  - ITAR §123 (export licenses)
  - ITAR §125.2 (deemed export)
pattern: 2  # Primary; Pattern 3 for adequacy determinations
controls:
  - License requirement determination
  - Deemed export
  - Technology control plan
  - Export control training
subject: Any U.S. person engaged in export of controlled items, technology, or services
pre_conditions:
  - export_control_program_active == true
  - item_classification_current == true  # Expert-attested classification required
obligations:
  - License determination: documented for each ECCN + destination + end-use + end-user combination
  - NLR/exception: affirmatively documented — not absence of records
  - Deemed export: foreign national access log; license or TCP restriction in place
  - TCP: current (≤12 months); all required elements present; custodian designated
  - Training: initial + annual; all export control personnel; 5-year records
evidence:
  - item_classification (ECCN, USML category, classification date, classified by)
  - license_determination_records (per-transaction ECCN + destination + end-use matrix)
  - foreign_national_log (name, nationality, visa type, accessible technology, license/exception basis)
  - tcp_document (version, review date, custodian, scope)
  - training_records (employee name, role, training date, content version, completion status)
```

### Python test file

```python
# tests/itar_ear/test_itar_ear_parameterized.py
"""
ITAR / EAR Parameterized Controls: License Requirements, Deemed Export, TCP, Training.

Controls: EAR §734, §740-742; ITAR §123, §125.2
Assumptions: ASSUME-ITAR-004 through ASSUME-ITAR-007
"""
import pytest
from datetime import datetime, timedelta, timezone
from typing import Any

TCP_REVIEW_MAX_DAYS = 365
TRAINING_MAX_DAYS = 365


@pytest.fixture(autouse=True)
def require_current_classification(
    item_classification: dict[str, Any],
    export_control_config: dict[str, Any],
):
    """Gate: classification must be expert-attested and current before enforcing mode."""
    if not export_control_config.get("export_control_program_active"):
        pytest.skip("Export control program not active — tests informational only")
    if not item_classification.get("classification_current"):
        pytest.skip(
            "Item classification is not current or not attested by qualified export counsel — "
            "downstream tests informational only"
        )


# ── License Requirement Determination ───────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-ITAR-004",
    description="License determination documented for each ECCN + destination + end-use combination",
    approved_by="Export Compliance Officer",
    review_date="2027-05-20",
)
def test_all_transactions_have_license_determination(
    transaction_records: list[dict[str, Any]],
):
    """EAR §742 / ITAR §123: Each controlled technology transaction must have a license determination."""
    missing_determination = []

    for tx in transaction_records:
        if not tx.get("involves_controlled_technology"):
            continue
        license_determination = tx.get("license_determination")
        if license_determination is None:
            missing_determination.append(tx["transaction_id"])
            continue
        # NLR must be affirmative — "no license required" is not an absence
        determination_type = license_determination.get("type")
        assert determination_type in {
            "license_approved", "nslr", "exception", "nlr", "no_ecl_jurisdiction"
        }, (
            f"Transaction {tx['transaction_id']}: unrecognized license determination type "
            f"{determination_type!r}"
        )

    assert not missing_determination, (
        f"Transactions with no license determination recorded: {missing_determination}"
    )


@pytest.mark.assumption(
    id="ASSUME-ITAR-004",
    description="License exception determinations document the exception basis and eligibility criteria",
    approved_by="Export Compliance Officer",
    review_date="2027-05-20",
)
def test_license_exception_records_complete(
    transaction_records: list[dict[str, Any]],
):
    """EAR §740: License exception records must document exception symbol and eligibility criteria."""
    incomplete = []

    for tx in transaction_records:
        ld = tx.get("license_determination", {})
        if ld.get("type") != "exception":
            continue
        if not ld.get("exception_symbol"):
            incomplete.append(f"{tx['transaction_id']}: missing exception symbol (e.g., ENC, LVS, TSR)")
        if not ld.get("eligibility_criteria_documented"):
            incomplete.append(f"{tx['transaction_id']}: exception eligibility criteria not documented")

    assert not incomplete, (
        f"License exception records incomplete: {incomplete}"
    )


# ── Deemed Export ────────────────────────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-ITAR-005",
    description="All foreign nationals with access to controlled tech identified; license or TCP restriction in place",
    approved_by="Export Compliance Officer",
    review_date="2027-05-20",
)
def test_foreign_national_access_controlled(foreign_national_log: list[dict[str, Any]]):
    """EAR §734.13 / ITAR §125.2: Foreign nationals accessing controlled technology must be logged and managed."""
    uncovered = []

    for person in foreign_national_log:
        if person.get("us_person"):
            continue  # U.S. persons not subject to deemed export
        if person.get("immigrant_visa_holder"):
            continue  # LPR/green card treated as U.S. person for EAR (ITAR has separate rules)

        has_license = person.get("deemed_export_license_number")
        has_exception = person.get("exception_basis")  # e.g., publicly available, fundamental research
        has_tcp_restriction = person.get("tcp_access_restricted_to_non_controlled")

        if not any([has_license, has_exception, has_tcp_restriction]):
            uncovered.append(
                f"{person['name']!r} ({person.get('nationality', 'unknown')}): "
                f"no license, exception, or TCP restriction documented"
            )

    assert not uncovered, (
        f"Foreign nationals with access to controlled technology without license, exception, or TCP restriction: "
        f"{uncovered}"
    )


# ── Technology Control Plan ──────────────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-ITAR-006",
    description="TCP current (≤12 months); all required elements present; custodian designated",
    approved_by="Export Compliance Officer",
    review_date="2027-05-20",
)
def test_tcp_exists_and_current(tcp_document: dict[str, Any]):
    """TCP: Technology Control Plan must exist, be current, and contain all required elements."""
    now = datetime.now(timezone.utc)

    assert tcp_document.get("exists"), "Technology Control Plan (TCP) document not found"

    last_review = tcp_document.get("last_review_date")
    assert last_review is not None, "TCP has no review date"
    assert last_review >= now - timedelta(days=TCP_REVIEW_MAX_DAYS), (
        f"TCP not reviewed within last year: last review {last_review.date()}"
    )

    required_elements = {
        "scope_documented",
        "physical_access_controls",
        "electronic_access_controls",
        "foreign_national_access_procedures",
        "training_requirements",
        "incident_reporting_procedure",
        "custodian_designated",
    }
    missing_elements = required_elements - set(
        k for k, v in tcp_document.items() if v
    )
    assert not missing_elements, (
        f"TCP missing required elements: {missing_elements}"
    )


@pytest.mark.human_review_required(
    reason=(
        "TCP physical and electronic access control adequacy is a judgment call — whether the "
        "described controls are sufficient for the facility's specific threat model requires "
        "review by a qualified Export Compliance Officer or export counsel. "
        "Action: ECO annual TCP review and attestation required."
    )
)
@pytest.mark.assumption(
    id="ASSUME-ITAR-006",
    description="TCP adequacy requires human review — whether controls are sufficient is ECO-evaluated",
    approved_by="Export Compliance Officer",
    review_date="2027-05-20",
)
def test_tcp_adequacy_reviewed_by_eco(tcp_document: dict[str, Any]):
    """TCP: Adequacy of access controls requires ECO annual attestation — surfaced for human review."""
    eco_attestation = tcp_document.get("eco_adequacy_attestation")
    assert eco_attestation is not None, (
        "TCP requires annual ECO adequacy attestation — not yet recorded"
    )

    now = datetime.now(timezone.utc)
    attestation_date = eco_attestation.get("attestation_date")
    assert attestation_date is not None, "ECO attestation has no date"
    assert attestation_date >= now - timedelta(days=TCP_REVIEW_MAX_DAYS), (
        f"ECO TCP adequacy attestation is older than 1 year: {attestation_date.date()}"
    )


# ── Export Control Training ──────────────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-ITAR-007",
    description="All export control personnel have completed initial and annual training; records retained 5 years",
    approved_by="Export Compliance Officer",
    review_date="2027-05-20",
)
def test_export_control_training_current(training_records: list[dict[str, Any]]):
    """ITAR/EAR compliance program: all personnel with export responsibilities must have current training."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=TRAINING_MAX_DAYS)

    overdue_training = []
    for record in training_records:
        if not record.get("has_export_responsibilities"):
            continue
        last_training = record.get("last_export_training_date")
        if last_training is None:
            overdue_training.append(f"{record['employee_id']}: no export control training on record")
        elif last_training < cutoff:
            overdue_training.append(
                f"{record['employee_id']}: last training {last_training.date()} "
                f"(more than {TRAINING_MAX_DAYS} days ago)"
            )

    assert not overdue_training, (
        f"Personnel with overdue export control training: {overdue_training}"
    )
```

---

## Open assumption registry (this file)

| ID | Domain | Summary | Review date |
|---|---|---|---|
| ASSUME-ITAR-004 | License requirement | Determination documented per ECCN + destination + end-use + end-user; NLR/exception affirmative; exceptions include symbol and eligibility criteria | 2026-05-20 |
| ASSUME-ITAR-005 | Deemed export | Foreign national log maintained; visa type considered; license, exception basis, or TCP restriction for each unlicensed access; records retained 5 years | 2026-05-20 |
| ASSUME-ITAR-006 | TCP | TCP current (≤12 months); all required elements present; custodian designated; ECO annual adequacy attestation | 2026-05-20 |
| ASSUME-ITAR-007 | Training | Initial + annual training for all export personnel; covers classification, licensing, screening, deemed export, red flags; records retained 5 years | 2026-05-20 |
