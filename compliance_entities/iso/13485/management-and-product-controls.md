# ISO 13485:2016 — Management and Product Controls

**Framework:** ISO 13485:2016
**Clauses:** 4.1, 5.1–5.2, 5.4–5.5, 6.1, 6.3–6.4, 7.1, 7.2.3, 7.5.2–7.5.4, 7.5.10–7.5.11, 8.1, 8.2.5, 8.4
**Confidence:** PARAMETERIZED-dominant (management commitment, operational support clauses)
**Last parsed:** 2026-05-21
**Applies to:** Medical device manufacturers, component suppliers, distributors, and service providers involved in the design, development, production, storage, distribution, installation, or servicing of medical devices
**Trigger:** Regulatory requirement in many major markets — EU MDR/IVDR references ISO 13485; FDA QMSR (21 CFR 820) aligns to ISO 13485:2016; Health Canada, TGA (Australia), PMDA (Japan) recognize ISO 13485 certification; customer requirement in device supply chains
**Jurisdiction:** Global — ISO standard; certification recognized by regulatory bodies in EU, Canada, Australia, Japan, and many other markets; FDA accepts ISO 13485 certification for QMSR compliance determination
**Not applicable to:** Non-medical-device manufacturers; software products not meeting the medical device definition under MDR/IVDR or FDA; purely research/investigational devices not entering commercial distribution

---

## Scope pre-condition

```python
@pytest.fixture(autouse=True)
def iso13485_scope(entity_profile: dict):
    if not entity_profile.get("iso13485_in_scope", False):
        pytest.skip("ISO 13485 not in scope")
```

---

## Domain — Clause 4.1 / 5.1: QMS General and Management Commitment

**Overall: PARAMETERIZED — Pattern 2**

```python
import pytest
from datetime import date

class TestClause4_5_Management:
    """Clauses 4.1, 5.1, 5.2 — QMS requirements and management commitment."""

    @pytest.mark.assumption(
        id="ASSUME-ISO13485-5_1-001",
        description=(
            "Top management commitment to QMS and regulatory requirements evidenced by: "
            "quality policy signed at executive level; quality objectives established at "
            "relevant functions; management review participation with records; resource "
            "allocation decisions traceable to QMS needs; communication of regulatory "
            "compliance importance throughout organization"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_management_commitment_to_regulatory_requirements(
        self, controls_evidence: dict
    ):
        leadership = controls_evidence.get("iso13485_leadership", {})
        assert leadership.get("management_commitment_evidenced", False), (
            "Top management must demonstrate commitment to QMS and regulatory requirements "
            "(ISO 13485 §5.1)"
        )

    @pytest.mark.assumption(
        id="ASSUME-ISO13485-5_2-001",
        description=(
            "Customer requirements and applicable regulatory requirements are determined "
            "and documented; regulatory requirements include: EU MDR/IVDR, FDA 21 CFR "
            "Part 820/QMSR, Health Canada MDR, or other applicable national regulations; "
            "regulatory requirements reviewed when regulations are updated; review documented"
        ),
        approved_by="regulatory_affairs",
        review_date="2027-05-21",
    )
    def test_applicable_regulatory_requirements_identified(self, controls_evidence: dict):
        leadership = controls_evidence.get("iso13485_leadership", {})
        assert leadership.get("applicable_regulations_identified", False), (
            "Applicable regulatory requirements must be determined and documented "
            "(ISO 13485 §5.2)"
        )
```

---

## Domain — Clause 6: Resource Management

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestClause6_Resources:
    """Clause 6 — Resource management: personnel competence, infrastructure, environment."""

    @pytest.mark.assumption(
        id="ASSUME-ISO13485-6_2-001",
        description=(
            "Personnel performing work affecting product quality have competence requirements "
            "defined in job descriptions or competence matrices; competence evaluated based on "
            "education, training, skills, and experience; training effectiveness evaluated "
            "within 90 days of training completion; competence records retained for duration "
            "of employment + minimum record retention period"
        ),
        approved_by="hr_quality",
        review_date="2027-05-21",
    )
    def test_competence_requirements_defined_for_quality_roles(
        self, controls_evidence: dict
    ):
        hr = controls_evidence.get("iso13485_hr", {})
        assert hr.get("competence_requirements_defined", False), (
            "Competence requirements must be defined for personnel affecting product quality "
            "(ISO 13485 §6.2)"
        )

    def test_competence_evidence_retained(self, controls_evidence: dict):
        hr = controls_evidence.get("iso13485_hr", {})
        assert hr.get("competence_records_retained", False), (
            "Evidence of competence (education, training, skills, experience records) "
            "must be retained (ISO 13485 §6.2)"
        )

    @pytest.mark.assumption(
        id="ASSUME-ISO13485-6_4-001",
        description=(
            "Work environment conditions that affect product quality are identified and "
            "controlled; for cleanroom or controlled environment requirements: environmental "
            "monitoring program defined (particulate counts, temperature, humidity, pressure); "
            "personnel health requirements documented; contamination control procedures documented "
            "for products at risk of contamination"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_work_environment_controlled(self, controls_evidence: dict):
        infrastructure = controls_evidence.get("iso13485_infrastructure", {})
        assert infrastructure.get("work_environment_conditions_defined", False), (
            "Work environment conditions affecting product quality must be defined and "
            "controlled (ISO 13485 §6.4.1)"
        )
```

---

## Domain — Clause 7.1: Planning of Product Realization

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestClause7_1_ProductRealizationPlanning:
    """Clause 7.1 — Product realization planning: quality plans and risk management integration."""

    @pytest.mark.assumption(
        id="ASSUME-ISO13485-7_1-001",
        description=(
            "Product realization planning integrates risk management per ISO 14971; "
            "quality plans document: quality objectives, processes, documentation, resources, "
            "verification/validation/monitoring/measurement activities, acceptance criteria, "
            "and required records; risk management plan established for each device type; "
            "risk management file maintained throughout product lifecycle"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_product_realization_plans_integrate_risk_management(
        self, controls_evidence: dict
    ):
        planning = controls_evidence.get("iso13485_product_realization", {})
        assert planning.get("risk_management_integrated", False), (
            "Product realization planning must integrate risk management activities per ISO 14971 "
            "(ISO 13485 §7.1)"
        )

    def test_quality_plans_documented(self, controls_evidence: dict):
        planning = controls_evidence.get("iso13485_product_realization", {})
        assert planning.get("quality_plans_documented", False), (
            "Quality plans must be documented for product realization (ISO 13485 §7.1)"
        )
```

---

## Domain — Clause 7.5: Product Controls (non-record sub-clauses)

### 7.5.2–7.5.4, 7.5.10–7.5.11

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestClause7_5_ProductControls:
    """Clause 7.5 — Production and service provision: cleanliness, servicing, preservation."""

    @pytest.mark.assumption(
        id="ASSUME-ISO13485-7_5_5-001",
        description=(
            "Where organization manufactures sterile devices or products cleaned prior to "
            "sterilization: validated sterilization process per applicable standard (ISO 11135, "
            "ISO 11137, ISO 14937, ISO 17665, or equivalent); validation records retained; "
            "sterilization batch records retained; re-validation criteria defined and documented; "
            "sterile barrier system validation per ISO 11607"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_sterilization_processes_validated(
        self, controls_evidence: dict, entity_profile: dict
    ):
        if not entity_profile.get("manufactures_sterile_devices", False):
            pytest.skip("Organization does not manufacture sterile devices")
        production = controls_evidence.get("iso13485_production", {})
        assert production.get("sterilization_validated", False), (
            "Sterilization processes must be validated before use and revalidated after "
            "changes (ISO 13485 §7.5.5)"
        )

    @pytest.mark.assumption(
        id="ASSUME-ISO13485-7_5_6-001",
        description=(
            "Processes where output conformity cannot be verified by subsequent monitoring "
            "or measurement (special processes) are validated before use; applies typically "
            "to: sterilization, sterile barrier sealing, coating processes, bonding processes; "
            "validation includes: defined protocol, acceptance criteria, equipment qualification, "
            "personnel qualification; revalidation criteria documented"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_special_processes_validated(self, controls_evidence: dict):
        production = controls_evidence.get("iso13485_production", {})
        special_processes = controls_evidence.get("iso13485_special_processes", [])
        if not special_processes:
            return
        unvalidated = [
            p for p in special_processes
            if not p.get("validated", False)
        ]
        assert not unvalidated, (
            f"Special processes (where output cannot be verified by subsequent measurement) "
            f"must be validated (ISO 13485 §7.5.6). "
            f"Unvalidated: {[p['process_id'] for p in unvalidated]}"
        )
```

---

## Domain — Clause 8: Measurement, Analysis, Feedback

### 8.2.1 Feedback System, 8.2.5 Process Monitoring, 8.4 Analysis

**Overall: PARAMETERIZED — Pattern 2**

```python
class TestClause8_Monitoring:
    """Clauses 8.1, 8.2.1, 8.2.5, 8.4 — Feedback, monitoring, and analysis."""

    @pytest.mark.assumption(
        id="ASSUME-ISO13485-8_2_1-001",
        description=(
            "Post-market feedback system collects data from: complaint records, warranty "
            "claims, customer surveys, field service reports, published literature/adverse event "
            "databases, and regulatory post-market surveillance requirements; feedback analyzed "
            "to provide early warning of quality problems; frequency and depth of analysis "
            "commensurate with device risk class; results documented in management review inputs"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_feedback_system_exists(self, controls_evidence: dict):
        feedback = controls_evidence.get("iso13485_post_market_feedback", {})
        assert feedback.get("feedback_system_documented", False), (
            "Feedback system must exist to provide early warning of quality problems "
            "and input into management review (ISO 13485 §8.2.1)"
        )

    @pytest.mark.assumption(
        id="ASSUME-ISO13485-8_4-001",
        description=(
            "Data analysis covers: feedback, process conformity, product conformity, "
            "supplier performance, audit results, customer complaints; analysis method "
            "proportionate to data volume and device risk class; results documented and "
            "included in management review; statistical techniques used where appropriate "
            "for process monitoring and product verification"
        ),
        approved_by="quality_manager",
        review_date="2027-05-21",
    )
    def test_data_analysis_conducted(self, controls_evidence: dict):
        analysis = controls_evidence.get("iso13485_data_analysis", {})
        assert analysis.get("data_analysis_conducted", False), (
            "Appropriate data analysis must be conducted to determine suitability, adequacy, "
            "and effectiveness of the QMS (ISO 13485 §8.4)"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-ISO13485-5_1-001 | Management commitment | Evidenced by policy, review participation, resource allocation, regulatory communication | 2027-05-21 |
| ASSUME-ISO13485-5_2-001 | Regulatory requirements | Applicable regulations identified; reviewed when regulations change | 2027-05-21 |
| ASSUME-ISO13485-6_2-001 | Competence | Job descriptions/matrices; effectiveness evaluated ≤90 days post-training; records retained | 2027-05-21 |
| ASSUME-ISO13485-6_4-001 | Work environment | Environmental monitoring program defined for controlled areas; contamination control documented | 2027-05-21 |
| ASSUME-ISO13485-7_1-001 | Risk management integration | ISO 14971 risk management file maintained per device; integrated in product realization planning | 2027-05-21 |
| ASSUME-ISO13485-7_5_5-001 | Sterilization validation | Sterile device manufacturers: validated per applicable ISO standard; batch records retained | 2027-05-21 |
| ASSUME-ISO13485-7_5_6-001 | Special processes | Validation protocol + acceptance criteria + qualification records for special processes | 2027-05-21 |
| ASSUME-ISO13485-8_2_1-001 | Post-market feedback | Feedback system collects from complaints, field reports, surveillance; included in management review | 2027-05-21 |
| ASSUME-ISO13485-8_4-001 | Data analysis | Covers feedback, conformity, supplier, audits; statistical techniques where appropriate | 2027-05-21 |

---

## Cross-standard notes

**ISO 9001:2015 vs ISO 13485:2016 structural divergence:** ISO 13485 does not adopt the "risk-based thinking" flexibility of ISO 9001:2015 — it retains prescriptive requirements for documented procedures. Approximately 22 documented procedures are required by ISO 13485 vs none mandated by name in ISO 9001:2015. When building an integrated QMS, the ISO 13485 prescriptive requirements define the floor; the ISO 9001:2015 approach layers on top.

**ISO 14971 integration:** All risk management requirements in ISO 13485 (clauses 7.1, 7.3.2, 7.3.6) reference ISO 14971:2019. The risk management file is effectively a prerequisite artifact for the DHF and for design validation evidence. A test suite for ISO 13485 is incomplete without ISO 14971 coverage (see nist/sp800-53 for analogous risk framework pattern).

**EU MDR Art. 10 alignment:** ISO 13485:2016 is the primary standard cited in EU MDR Article 10(9) for QMS requirements. EUDAMED registration and UDI requirements sit outside the QMS but interact with traceability records (§7.5.9) — the UDI serves as the traceability identifier.
