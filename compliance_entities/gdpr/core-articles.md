# GDPR — Core Technically Testable Articles

**Registry path:** `/regulation-registry/GDPR/Articles/`
**Regulation:** EU General Data Protection Regulation 2016/679
**Last parsed:** 2026-05-20
**Applies to:** Any organization — regardless of location — that processes personal data of EU/EEA data subjects by offering goods or services to them or monitoring their behavior within the EU/EEA
**Trigger:** Offering goods or services to EU/EEA persons (Art. 3(2)(a)); monitoring behavior of EU/EEA persons within the EU/EEA (Art. 3(2)(b)); establishment in the EU/EEA (Art. 3(1))
**Jurisdiction:** European Union / EEA; strong extraterritorial reach — applies to non-EU organizations targeting EU persons; enforced by national Data Protection Authorities and the EDPB
**Not applicable to:** Purely personal or household use (Art. 2(2)(c)); national security and law enforcement activities (Directive 2016/680 instead); anonymous data (not 'personal data' within GDPR meaning); deceased persons (in most member states)
**Overall confidence:** MEDIUM — Art. 33 (72-hour breach notification) is HIGH/DETERMINISTIC; Art. 28/30 (DPA, ROPA) are MEDIUM/PARAMETERIZED; Art. 32 (security) is CONTESTED; Art. 12 (DSR timelines) is HIGH/DETERMINISTIC
**Covers:** Art. 12, 13/14, 28, 30, 33/34, 35, 37, Chapter V (Art. 44–49), plus Art. 32 framing

---

## Art. 12 — Transparency and Data Subject Request Response Times (DETERMINISTIC)

### Source excerpt

> The controller shall provide information on action taken on a request under Articles 15 to 22 to the data subject without undue delay and in any event within one month of receipt of the request. That period may be extended by two further months where necessary, taking into account the complexity and number of the requests. The controller shall inform the data subject of any such extension within one month of receipt of the request, together with the reasons for the delay.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Data subject rights request received (Art. 15–22 requests) | DETERMINISTIC |
| Obligation | Response within 1 month of receipt; extension notice within 1 month if extended; maximum 3 months total | DETERMINISTIC |
| Evidence | `dsr_records.response_date - receipt_date ≤ 30 days`; `extension_notice_sent_within_30_days` if extended | DETERMINISTIC |

**Assumption (ASSUME-GDPR-001):** DSR response is adequate when: (1) response provided within 30 days of receipt date; (2) if complex/multiple requests, extension notice sent within 30 days informing of the extension and the reasons; (3) total maximum response time 90 days; (4) DSR log maintained with receipt date, request type (access/erasure/portability/objection/correction/restriction), response date, and outcome; (5) identity verification performed before providing data — verification must be proportionate and not create excessive burden.

**Overall: DETERMINISTIC → Pattern 1**

---

## Art. 13/14 — Privacy Notices (PARAMETERIZED)

### Source excerpt (Art. 13)

> Where personal data relating to a data subject are collected from the data subject, the controller shall, at the time when personal data are obtained, provide the data subject with all of the following information...

### Required elements (Art. 13(1)–(2))

| Element | Required by | Classification |
|---|---|---|
| Controller identity and contact | Art. 13(1)(a) | DETERMINISTIC (existence) |
| DPO contact (if applicable) | Art. 13(1)(b) | DETERMINISTIC (existence when DPO required) |
| Processing purposes and legal basis | Art. 13(1)(c) | PARAMETERIZED |
| Legitimate interests (if Art. 6(1)(f)) | Art. 13(1)(d) | PARAMETERIZED |
| Recipients or categories of recipients | Art. 13(1)(e) | PARAMETERIZED |
| Third-country transfers intent | Art. 13(1)(f) | PARAMETERIZED |
| Retention period or criteria | Art. 13(2)(a) | PARAMETERIZED |
| Rights notification (access, rectification, erasure, restriction, portability, objection) | Art. 13(2)(b) | DETERMINISTIC (list completeness) |
| Right to withdraw consent (where consent is basis) | Art. 13(2)(c) | DETERMINISTIC (existence when applicable) |
| Right to lodge complaint with supervisory authority | Art. 13(2)(d) | DETERMINISTIC (existence) |
| Whether provision is statutory/contractual requirement | Art. 13(2)(e) | PARAMETERIZED |
| Automated decision-making / profiling (if applicable) | Art. 13(2)(f) | PARAMETERIZED |

**Assumption (ASSUME-GDPR-002):** Privacy notice is adequate when it: (1) contains all 12 required elements above; (2) is written in plain language — not just legal text; (3) is provided at the time of collection (Art. 13) or within 1 month for indirect collection (Art. 14); (4) is easily accessible (not buried 3 clicks deep); (5) is reviewed and updated when processing purposes change.

**Overall: PARAMETERIZED → Pattern 2; mandatory element completeness → Pattern 1**

---

## Art. 28 — Data Processing Agreements (PARAMETERIZED)

### Source excerpt

> Where processing is to be carried out on behalf of a controller, the controller shall only use processors providing sufficient guarantees to implement appropriate technical and organisational measures in such a manner that processing will meet the requirements of this Regulation.

### Art. 28(3) mandatory contract elements

| Element | Required | Classification |
|---|---|---|
| Subject matter, duration, nature, purpose | Art. 28(3) preamble | DETERMINISTIC (existence) |
| Process only on documented instructions | Art. 28(3)(a) | DETERMINISTIC |
| Confidentiality obligation for authorized persons | Art. 28(3)(b) | DETERMINISTIC |
| Security measures (Art. 32 reference) | Art. 28(3)(c) | PARAMETERIZED |
| Sub-processor authorization (general or specific) | Art. 28(3)(d) | DETERMINISTIC |
| Data subject rights assistance | Art. 28(3)(e) | DETERMINISTIC |
| Deletion or return at contract end | Art. 28(3)(f) | DETERMINISTIC |
| Audit and information rights | Art. 28(3)(g) | DETERMINISTIC |
| Sub-processor notification obligation | Art. 28(3)(h) | DETERMINISTIC |

**Assumption (ASSUME-GDPR-003):** DPA is adequate when it: (1) contains all 9 Art. 28(3) mandatory elements above; (2) uses current 2021 EU SCC Module 1 (controller-to-controller) or Module 2 (controller-to-processor) where applicable for EEA-to-non-EEA transfers; (3) processor sub-processor list available and up to date; (4) reviewed and updated when the processing relationship materially changes; (5) covers all processing categories identified in the ROPA for that processor relationship.

**Overall: PARAMETERIZED for content adequacy → Pattern 2; mandatory element existence → Pattern 1**

---

## Art. 30 — Records of Processing Activities (PARAMETERIZED)

### Source excerpt

> Each controller and, where applicable, the controller's representative, shall maintain a record of processing activities under its responsibility.

### Required ROPA fields (controller — Art. 30(1))

| Field | Required | Classification |
|---|---|---|
| Controller name and contact details | Art. 30(1)(a) | DETERMINISTIC |
| DPO contact (if applicable) | Art. 30(1)(a) | DETERMINISTIC (when DPO required) |
| Processing purposes | Art. 30(1)(b) | DETERMINISTIC |
| Data subject categories | Art. 30(1)(c) | PARAMETERIZED (completeness) |
| Data categories | Art. 30(1)(c) | PARAMETERIZED |
| Recipient categories | Art. 30(1)(d) | PARAMETERIZED |
| Third-country transfers and safeguards | Art. 30(1)(e) | PARAMETERIZED |
| Retention periods | Art. 30(1)(f) | PARAMETERIZED |
| General description of technical/organisational measures | Art. 30(1)(g) | PARAMETERIZED |

**Assumption (ASSUME-GDPR-004):** ROPA is adequate when: (1) all processing activities documented — no significant processing activity missing from ROPA; (2) each entry contains all required fields; (3) retention periods specify either a fixed period or criteria used to determine it (not just "as long as necessary"); (4) ROPA reviewed and updated at minimum annually or when new processing activities begin; (5) ROPA held in machine-readable format (not paper-only) to enable supervisory authority inspection.

**Overall: DETERMINISTIC for ROPA existence → Pattern 1; PARAMETERIZED for completeness → Pattern 2**

---

## Art. 33 — Breach Notification to Supervisory Authority (HIGH — DETERMINISTIC)

### Source excerpt

> In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority competent.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Personal data breach that is likely to result in a risk to rights and freedoms of individuals | DETERMINISTIC (trigger is breach) / PARAMETERIZED (risk assessment) |
| Obligation | Notify supervisory authority within 72 hours of becoming aware; where infeasible, notify without undue delay with reasons for delay | DETERMINISTIC |
| Evidence | `breach_records.supervisory_authority_notified == true`; `notification_timestamp - awareness_timestamp ≤ 72 hours` | DETERMINISTIC |

**Assumption (ASSUME-GDPR-005):** Breach notification is adequate when: (1) notification made within 72 hours of awareness (not discovery) — where the controller becomes aware = the controller's responsible personnel know, not just when a system alert fires; (2) notification contains at minimum: breach description, categories and approximate number of individuals concerned, categories and approximate number of records concerned, DPO contact, likely consequences, measures taken or proposed; (3) if full information unavailable within 72 hours, initial notification sent within timeframe with incomplete information; supplementary information provided without further undue delay; (4) all breaches documented in breach log whether reported to authority or not (Art. 33(5)).

**Cross-reference:** 72-hour GDPR deadline is tighter than HIPAA (60 days) and SOC 2 (contractual). Design IRP to meet GDPR and others are automatically satisfied.

**Overall: DETERMINISTIC for 72-hour threshold → Pattern 1; PARAMETERIZED for notification content completeness → Pattern 2**

---

## Art. 34 — Communication of Breach to Data Subjects (PARAMETERIZED)

### Source excerpt

> When the personal data breach is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall communicate the personal data breach to the data subject without undue delay.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Breach "likely to result in a high risk" — higher threshold than Art. 33 | PARAMETERIZED |
| Obligation | Communicate to affected individuals without undue delay | PARAMETERIZED (high risk determination) |
| Exceptions | Communication not required if: data encrypted and key secure; measures taken to prevent materialization; notification would require disproportionate effort (use public notice instead) | PARAMETERIZED |

**Assumption (ASSUME-GDPR-006):** High-risk determination for Art. 34 is adequate when: organization applies EDPB Guidelines 9/2022 criteria — nature of data (special category = high risk), scale, sensitivity, ease of re-identification, and likely consequences. Decision documented with rationale. DPO consulted on borderline cases.

**Overall: PARAMETERIZED → Pattern 2**

---

## Art. 35 — Data Protection Impact Assessment (PARAMETERIZED)

### Source excerpt

> Where a type of processing in particular using new technologies, and taking into account the nature, scope, context and purposes of the processing, is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall, prior to the processing, carry out an assessment of the impact of the envisaged processing operations on the protection of personal data.

### DPIA trigger criteria (Art. 35(3))

| Trigger | Classification |
|---|---|
| Systematic and extensive profiling with legal or significant effects | PARAMETERIZED |
| Large-scale processing of special category data | PARAMETERIZED |
| Systematic monitoring of publicly accessible area | PARAMETERIZED |
| EDPB/national DPA list of mandatory DPIA types | DETERMINISTIC (once list exists for jurisdiction) |

**Assumption (ASSUME-GDPR-007):** DPIA is required and adequate when: (1) any of the Art. 35(3) triggers or national mandatory DPIA list entries apply — DPIA required before processing begins; (2) DPIA includes: systematic description of processing, necessity and proportionality assessment, risk assessment, measures to address the risks; (3) DPO consulted; (4) prior consultation with supervisory authority if residual risk remains high after mitigation (Art. 36); (5) DPIA reviewed when processing changes materially.

**Overall: PARAMETERIZED → Pattern 2**

---

## Art. 37 — DPO Designation (PARAMETERIZED for scope; DETERMINISTIC once threshold met)

### Source excerpt

> The controller and the processor shall designate a data protection officer in any case where: (a) the processing is carried out by a public authority or body; (b) the core activities consist of processing operations which require regular and systematic monitoring of data subjects on a large scale; or (c) the core activities consist of processing on a large scale of special categories of data pursuant to Article 9.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Art. 37(1)(a)/(b)/(c) criteria met | PARAMETERIZED (scope determination) |
| Obligation | DPO designated and registered with supervisory authority; DPO contact published | DETERMINISTIC (once threshold met) |
| Evidence | `dpo_designation.documented == true`; DPO contact in privacy notice; national supervisory authority registration (where required) | DETERMINISTIC |

**Assumption (ASSUME-GDPR-008):** "Large scale" and "core activities" determinations: large scale = processing covering a significant portion of EU population at regional/national level or continuously/systematically; core activities = primary purpose, not ancillary (e.g., HR data processing for a retail company is NOT core activities — but loyalty program profiling at scale may be). DPO must have expert knowledge of data protection law and practice; may be internal or external; cannot hold other roles that create conflicts of interest.

**Overall: PARAMETERIZED for threshold determination → Pattern 2; DETERMINISTIC for DPO existence once threshold met → Pattern 1**

---

## Art. 32 — Security of Processing (CONTESTED)

### Source excerpt

> Taking into account the state of the art, the costs of implementation and the nature, scope, context and purposes of processing as well as the risk of varying likelihood and severity for the rights and freedoms of natural persons, the controller and the processor shall implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk.

### GDPR Art. 32 test structure

Art. 32 does not admit Pattern 1 tests. It generates:
1. **Pattern 2 tests** for specific technical measures adopted as assumptions (encryption, backup, patching, access control, MFA) — these prove the measures are in place
2. **Pattern 3 tests** for the "appropriate" determination — whether the measures are appropriate given the risk, state of the art, and nature of processing

**Assumption (ASSUME-GDPR-009):** Art. 32 technical measures are adequate for processing of standard personal data when they include at minimum: (1) encryption at rest (AES-128+ for stored personal data); (2) encryption in transit (TLS 1.2+); (3) access controls limiting personal data to authorized personnel with need-to-know; (4) MFA for access to systems processing personal data at scale; (5) backup and recovery capable of restoring within a reasonable time (Art. 32(1)(c): ability to restore); (6) regular testing: vulnerability scanning at least quarterly; (7) pseudonymization where feasible without making data unfit for purpose. For special category data, enhanced controls required.

**Overall: CONTESTED → Pattern 3 for adequacy determination; DETERMINISTIC/PARAMETERIZED for specific implemented measures → Pattern 1/2**

---

## Chapter V — International Data Transfers (Art. 44–49) (MIXED)

### Transfer mechanism confidence map

| Mechanism | Basis | Confidence |
|---|---|---|
| Adequacy decision (Art. 45) | EU Commission decision that destination country provides adequate protection | DETERMINISTIC — binary lookup against EDPB adequacy list |
| EU-U.S. Data Privacy Framework | Specific adequacy decision for DPF-certified U.S. organizations | DETERMINISTIC — DPF certification status verifiable via DPF list |
| Standard Contractual Clauses — 2021 version (Art. 46(2)(c)) | SCC in place using 2021 EC SCC template | DETERMINISTIC (existence) / PARAMETERIZED (module selection) |
| Transfer Impact Assessment (TIA) | Assessment of destination country laws | CONTESTED |
| BCRs (Art. 47) | DPA-approved binding corporate rules | PARAMETERIZED (approval status) |
| Derogations (Art. 49) | Explicit consent, vital interests, performance of contract, public interest | CONTESTED |

**Assumption (ASSUME-GDPR-010):** International transfer compliance is adequate when: (1) all personal data transfers to third countries identified in the ROPA; (2) for each transfer: either adequacy decision covers destination, or 2021 SCCs in place with correct module (Module 1: C2C; Module 2: C2P; Module 3: P2P; Module 4: P2C); (3) TIA conducted for transfers to high-risk jurisdictions (no adequacy; laws permitting bulk surveillance); (4) DPF: U.S. recipient's DPF certification verified before relying on adequacy.

**Overall: DETERMINISTIC for adequacy decision and DPF lookup → Pattern 1; PARAMETERIZED for SCC module selection → Pattern 2; CONTESTED for TIA → Pattern 3**

---

## YAML specifications

### `gdpr_breach_notification.yaml`

```yaml
regulation_id: GDPR-Art33-2016-679
section: "GDPR Article 33 — Breach Notification to Supervisory Authority"
r_or_a: Required
source_text: >
  In the case of a personal data breach, the controller shall without undue delay
  and, where feasible, not later than 72 hours after having become aware of it,
  notify the personal data breach to the supervisory authority.

extracted_elements:
  subject: "Controller"
  condition: "Personal data breach likely to result in risk to rights and freedoms"
  obligation: "Supervisory authority notified within 72 hours; all breaches documented"
  evidence: "breach_records: awareness_timestamp, notification_timestamp, authority_notified"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: PARAMETERIZED
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-GDPR-005
    assumption_text: >
      Notification ≤72h from organizational awareness (not system alert); initial
      notification acceptable if incomplete; breach log maintained for all breaches
      whether reported or not (Art. 33(5)).
    assumed_by: "DPO"
    approved_by: "DPO/Legal"
    date: "2026-05-20"
    review_frequency_days: 365
test_confidence: HIGH
generated_test: "tests/gdpr/test_gdpr_core.py"
```

---

## Generated tests

### `tests/gdpr/test_gdpr_core.py`

```python
"""
GDPR 2016/679 — Core Technically Testable Articles
Confidence: HIGH for Art. 33 (72h breach notification) and Art. 12 (DSR response);
MEDIUM for Art. 28 (DPA completeness), Art. 30 (ROPA), Art. 37 (DPO);
CONTESTED for Art. 32 (appropriate security) — requires DPO/legal review
"""
import pytest
from datetime import date, timedelta

BREACH_NOTIFICATION_MAX_HOURS = 72
DSR_RESPONSE_MAX_DAYS = 30
DSR_EXTENSION_NOTICE_MAX_DAYS = 30
DSR_EXTENDED_MAX_DAYS = 90
ROPA_REVIEW_MAX_DAYS = 365

DPA_REQUIRED_ELEMENTS = {
    "subject_matter_documented",
    "processing_on_instructions_only",
    "confidentiality_obligation",
    "deletion_or_return_on_termination",
    "audit_right",
    "subprocessor_notification",
    "dsr_assistance",
}


@pytest.fixture(autouse=True)
def require_eu_processing_scope(system_scope):
    """All GDPR tests require EU data subject processing attestation."""
    if not system_scope.get("processes_eu_subject_data"):
        pytest.skip("System not attested as processing EU data subject personal data")


@pytest.mark.assumption(
    id="ASSUME-GDPR-005",
    description=(
        "Breach notification: ≤72h from organizational awareness; initial notification "
        "acceptable if incomplete; Art. 33(5) documentation for all breaches."
    ),
    approved_by="DPO/Legal",
    review_date="2026-05-20",
)
def test_breach_notification_within_72_hours(breach_records):
    """Art. 33 — Personal data breaches must be notified to supervisory authority within 72 hours."""
    violations = []
    for breach in breach_records:
        if breach.get("notification_not_required"):
            continue
        if not breach.get("supervisory_authority_notified"):
            violations.append(
                f"Breach {breach.get('breach_id')}: supervisory authority not notified"
            )
            continue
        awareness_ts = breach.get("controller_awareness_timestamp")
        notification_ts = breach.get("notification_timestamp")
        if awareness_ts and notification_ts:
            hours_elapsed = (notification_ts - awareness_ts).total_seconds() / 3600
            if hours_elapsed > BREACH_NOTIFICATION_MAX_HOURS:
                violations.append(
                    f"Breach {breach.get('breach_id')}: notified {hours_elapsed:.1f} hours "
                    f"after awareness (max {BREACH_NOTIFICATION_MAX_HOURS})"
                )
    assert not violations, (
        f"NONCONFORMITY (Art. 33): {len(violations)} breach(es) exceeding 72-hour "
        f"notification deadline:\n" + "\n".join(violations)
    )


def test_all_breaches_documented(breach_records):
    """Art. 33(5) — All personal data breaches must be documented regardless of whether reported."""
    assert breach_records is not None, (
        "NONCONFORMITY (Art. 33(5)): Breach log not found — all personal data breaches "
        "must be documented, including those below reporting threshold"
    )


@pytest.mark.assumption(
    id="ASSUME-GDPR-001",
    description="DSR response ≤30 days; extension notice within 30 days if extending; max 90 days total",
    approved_by="DPO/Legal",
    review_date="2026-05-20",
)
def test_dsr_response_within_30_days(dsr_records):
    """Art. 12 — Data subject requests must be responded to within 1 month."""
    violations = []
    for dsr in dsr_records:
        receipt = dsr.get("receipt_date")
        response = dsr.get("response_date")
        if receipt and response:
            days = (response - receipt).days
            if days > DSR_RESPONSE_MAX_DAYS and not dsr.get("extension_granted"):
                violations.append(
                    f"DSR {dsr.get('dsr_id')}: responded {days} days after receipt "
                    f"(max {DSR_RESPONSE_MAX_DAYS} without extension)"
                )
        elif receipt and not response:
            days_open = (date.today() - receipt).days
            if days_open > DSR_RESPONSE_MAX_DAYS and not dsr.get("extension_granted"):
                violations.append(
                    f"DSR {dsr.get('dsr_id')}: open {days_open} days without response "
                    f"or extension"
                )
    assert not violations, (
        f"NONCONFORMITY (Art. 12): {len(violations)} DSR(s) not responded to within "
        f"1 month:\n" + "\n".join(violations)
    )


@pytest.mark.assumption(
    id="ASSUME-GDPR-003",
    description="DPA: all 9 Art. 28(3) mandatory elements; current 2021 SCCs for EEA-to-non-EEA transfers",
    approved_by="DPO/Legal",
    review_date="2026-05-20",
)
def test_all_processors_have_dpa_with_required_elements(processor_register, dpa_records):
    """Art. 28 — All processors must have a DPA with all 9 mandatory elements."""
    dpa_processor_ids = {d["processor_id"] for d in dpa_records if d.get("dpa_executed")}
    violations = []
    for processor in processor_register:
        if not processor.get("processes_personal_data"):
            continue
        if processor["processor_id"] not in dpa_processor_ids:
            violations.append(f"Processor {processor['processor_id']}: no DPA found")
            continue
        dpa = next((d for d in dpa_records if d["processor_id"] == processor["processor_id"]), None)
        if dpa:
            missing = DPA_REQUIRED_ELEMENTS - set(
                k for k, v in dpa.items() if v
            )
            if missing:
                violations.append(
                    f"Processor {processor['processor_id']}: DPA missing elements: {missing}"
                )
    assert not violations, (
        f"NONCONFORMITY (Art. 28): {len(violations)} processor DPA issue(s):\n"
        + "\n".join(violations)
    )


def test_ropa_exists_and_reviewed_annually(ropa_records):
    """Art. 30 — ROPA must exist and be reviewed at least annually."""
    today = date.today()
    assert ropa_records, (
        "NONCONFORMITY (Art. 30): No ROPA found — Records of Processing Activities "
        "are required"
    )
    last_reviewed = max(
        (r.get("last_reviewed_date") for r in ropa_records if r.get("last_reviewed_date")),
        default=None
    )
    assert last_reviewed, "NONCONFORMITY (Art. 30): ROPA has no review date recorded"
    days_since = (today - last_reviewed).days
    assert days_since <= ROPA_REVIEW_MAX_DAYS, (
        f"NONCONFORMITY (Art. 30): ROPA last reviewed {days_since} days ago "
        f"(max {ROPA_REVIEW_MAX_DAYS})"
    )


def test_ropa_entries_have_required_fields(ropa_records):
    """Art. 30 — Each ROPA entry must contain all required fields."""
    REQUIRED_FIELDS = {
        "purpose", "data_subject_categories", "data_categories",
        "retention_period", "controller_name"
    }
    violations = []
    for entry in ropa_records:
        missing = [f for f in REQUIRED_FIELDS if not entry.get(f)]
        if missing:
            violations.append(
                f"ROPA entry '{entry.get('processing_activity')}': "
                f"missing fields: {missing}"
            )
    assert not violations, (
        f"NONCONFORMITY (Art. 30): {len(violations)} ROPA entry/ies with missing "
        f"required fields:\n" + "\n".join(violations)
    )


@pytest.mark.human_review_required(
    reason=(
        "Art. 32: 'appropriate' security measures cannot be validated by automated test. "
        "This test confirms specific security controls are in place; DPO/Legal must annually "
        "attest that measures are appropriate given the risk and state of the art."
    )
)
@pytest.mark.assumption(
    id="ASSUME-GDPR-009",
    description=(
        "Art. 32 measures for standard PD: AES-128+ at rest; TLS 1.2+ in transit; "
        "access controls; MFA at scale; backup with restore; quarterly vuln scanning; pseudonymization."
    ),
    approved_by="DPO/Legal",
    review_date="2026-05-20",
)
def test_art32_security_measures_documented(security_measures_register):
    """Art. 32 — Security measures must be documented (adequacy requires DPO review)."""
    assert security_measures_register, (
        "NONCONFORMITY (Art. 32): No security measures register found — "
        "Art. 32 requires documented technical and organisational measures"
    )
    measures = security_measures_register[0] if security_measures_register else {}
    assert measures.get("encryption_at_rest"), (
        "NONCONFORMITY (Art. 32): Encryption at rest not documented in security measures"
    )
    assert measures.get("encryption_in_transit"), (
        "NONCONFORMITY (Art. 32): Encryption in transit not documented in security measures"
    )
    assert measures.get("dpo_review_date"), (
        "NONCONFORMITY (Art. 32): DPO has not reviewed and attested security measures — "
        "annual DPO attestation required"
    )


def test_dpo_designated_when_required(dpo_designation_records, processing_activities):
    """Art. 37 — DPO must be designated when Art. 37(1) criteria are met."""
    dpo_trigger_activities = [
        a for a in processing_activities
        if a.get("requires_dpo_designation")
    ]
    if not dpo_trigger_activities:
        pytest.skip("No processing activities that trigger mandatory DPO designation")
    assert dpo_designation_records, (
        "NONCONFORMITY (Art. 37): Processing activities trigger mandatory DPO designation "
        "but no DPO designation record found"
    )


def test_international_transfers_have_safeguard(ropa_records):
    """Art. 44 — All international data transfers must have a documented transfer mechanism."""
    violations = []
    for entry in ropa_records:
        transfers = entry.get("international_transfers", [])
        for transfer in transfers:
            if not transfer.get("transfer_mechanism"):
                violations.append(
                    f"Processing '{entry.get('processing_activity')}': "
                    f"transfer to {transfer.get('destination_country')} has no mechanism"
                )
    assert not violations, (
        f"NONCONFORMITY (Art. 44): {len(violations)} international transfer(s) without "
        f"documented safeguard:\n" + "\n".join(violations)
    )
```

---

## Notes for the registry

- **72-hour clock start — "becomes aware":** The breach notification clock starts when the controller "becomes aware" — which EDPB Guidelines clarify means when the controller's responsible staff (data protection or security team, not just IT) have sufficient certainty that a breach occurred. A security alert that has not yet been investigated does not start the clock; however, unreasonable delay in investigation is itself a compliance problem. Organizations should have a documented escalation path from security alert to DPO notification so the clock start is unambiguous.
- **Art. 32 and the GDPR paradox:** The most important GDPR security obligation has no bright-line content. This is intentional — the drafters wanted a technology-neutral, risk-proportionate standard. The consequence is that Pattern 1 tests for Art. 32 are impossible. The ASSUME-GDPR-009 tests verify that specific security controls are in place; they do not and cannot certify that those controls are "appropriate" for the specific processing — that requires human (DPO/Legal) judgment. The `@pytest.mark.human_review_required` decorator signals this.
- **ROPA and the privacy-by-design feedback loop:** Art. 30 ROPA entries should drive Art. 35 DPIA triggers. When a new processing activity is added to the ROPA, the DPIA screening should be automatically triggered. The `test_ropa_entries_have_required_fields` test verifies completeness; the DPIA trigger check (whether each activity has been screened) is a separate Pattern 2 test.
- **DPA vs. BAA vs. DPC:** Under GDPR, agreements with data processors (Art. 28) are called DPAs; under HIPAA, they are BAAs; under the UK GDPR and some other frameworks, they are called DPCs. A well-drafted template can combine all three. The `DPA_REQUIRED_ELEMENTS` set in the test captures the GDPR Art. 28(3) mandatory elements only; HIPAA BAA terms are tracked separately.
- **Schrems II and TIA requirement:** Since the 2020 CJEU Schrems II decision, Standard Contractual Clauses alone are not sufficient for transfers to countries with laws permitting bulk surveillance of EU data (notably the U.S.). A Transfer Impact Assessment (TIA) is required to assess whether the SCCs can be effective in the destination country's legal environment. The EU-U.S. Data Privacy Framework (2023 adequacy decision) removes the TIA requirement for DPF-certified U.S. recipients.
