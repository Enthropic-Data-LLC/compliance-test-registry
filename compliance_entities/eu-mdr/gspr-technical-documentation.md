# EU MDR / IVDR — GSPR and Technical Documentation

**Framework:** EU MDR 2017/745 (and IVDR 2017/746 by analogy)
**Clauses:** Annex I (GSPR), Annex II (Technical Documentation), Article 9 (DoC), Article 10 (manufacturer obligations), Article 11 (AR), Article 27 (UDI), Article 55 (CE marking)
**Parent:** ISO 13485 (QMS), ISO 14971 (risk management), IEC 62304 (software)
**Confidence:** DETERMINISTIC-dominant (GSPR checklist, tech doc elements, DoC 19 elements, UDI registration, AR requirement for non-EU manufacturers)
**Last parsed:** 2026-05-21
**Applies to:** Legal manufacturers placing medical devices on the EU market; authorized representatives (for non-EU manufacturers); importers and distributors involved in the EU supply chain for medical devices classified under EU MDR Regulation 2017/745
**Trigger:** Placing a medical device (as defined in MDR Art. 2) on the EU market or putting it into service in the EU; applies regardless of manufacturer location — non-EU manufacturers must appoint an EU authorized representative
**Jurisdiction:** European Union; extraterritorial for non-EU manufacturers exporting to EU market; enforcement by national Competent Authorities and Notified Bodies
**Not applicable to:** In vitro diagnostic medical devices (Regulation 2017/746 IVDR applies instead); custom-made devices (Article 52 modified pathway); devices in clinical investigation only (Article 62 clinical investigation rules); devices for export outside EU with no EU market placement

---

## Scope pre-condition

```python
@pytest.fixture(autouse=True)
def eu_mdr_scope(entity_profile: dict):
    """Skip if device not placed on EU/EEA market."""
    if not entity_profile.get("eu_mdr_in_scope", False):
        pytest.skip("EU MDR 2017/745 not in scope")
```

---

## Constants

```python
# Device class thresholds — determines conformity assessment pathway
EU_MDR_CLASS_I = "I"
EU_MDR_CLASS_IIA = "IIa"
EU_MDR_CLASS_IIB = "IIb"
EU_MDR_CLASS_III = "III"

# Classes requiring Notified Body involvement
EU_MDR_CLASSES_REQUIRING_NOTIFIED_BODY = frozenset({
    EU_MDR_CLASS_IIA, EU_MDR_CLASS_IIB, EU_MDR_CLASS_III
})

# EU Declaration of Conformity — 19 mandatory elements (Article 19)
EU_MDR_DOC_REQUIRED_ELEMENTS = frozenset({
    "name_and_address_of_manufacturer",
    "name_and_address_of_authorized_representative",   # if non-EU manufacturer
    "statement_of_sole_responsibility",
    "device_name_product_code_catalogue_number",
    "basic_udi_di",
    "risk_class",
    "applicable_annexes_conformity_assessment",
    "reference_to_harmonised_standards_applied",
    "reference_to_common_specifications_applied",
    "notified_body_name_address_number",               # where applicable
    "notified_body_certificate_number",                # where applicable
    "statement_of_conformity_with_mdr",
    "place_and_date_of_issue",
    "name_and_signature_of_authorised_signatory",
})
EU_MDR_DOC_CONDITIONAL_ELEMENTS = frozenset({
    "name_and_address_of_authorized_representative",   # only non-EU manufacturers
    "notified_body_name_address_number",               # only where NB involved
    "notified_body_certificate_number",                # only where NB involved
})

# Technical Documentation — Annex II Part A (required for all devices)
EU_MDR_TECH_DOC_PART_A_ELEMENTS = frozenset({
    "device_description_and_specification",
    "reference_to_previous_device_generations",
    "reference_to_similar_devices",
    "labeling_specimens",
    "design_and_manufacturing_information",
    "general_safety_performance_requirements",         # GSPR checklist with §1–23
    "benefit_risk_analysis_risk_management",           # ISO 14971 risk file
    "product_verification_validation",                 # V&V protocols and reports
})

# Software version and IEC 62304 class — required in tech doc Annex II §6.2
EU_MDR_SOFTWARE_DOCUMENTATION_REQUIRED = True

# UDI required on label — Article 27
EU_MDR_UDI_LABEL_REQUIRED = True
EU_MDR_UDI_EUDAMED_REGISTRATION_REQUIRED = True

# IVDR classes for reference
EU_IVDR_CLASS_A = "A"
EU_IVDR_CLASS_B = "B"
EU_IVDR_CLASS_C = "C"
EU_IVDR_CLASS_D = "D"
```

---

## Annex I GSPR — General Safety and Performance Requirements

**Overall: DETERMINISTIC (checklist) + PARAMETERIZED (adequacy)**

```python
import pytest

class TestGSPRChecklist:
    """Annex I — GSPR: device must meet all applicable general safety and performance requirements."""

    def test_gspr_assessment_completed_for_device(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        no_gspr = [p for p in programs if not p.get("gspr_assessment_completed", False)]
        assert not no_gspr, (
            f"GSPR assessment (Annex I §1–23) must be completed for each device type "
            f"(EU MDR 2017/745 Annex I). Missing: {[p['device_id'] for p in no_gspr]}"
        )

    def test_gspr_assessment_references_applicable_standards(
        self, controls_evidence: dict
    ):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        no_standards_ref = [
            p for p in programs
            if p.get("gspr_assessment_completed", False)
            and not p.get("gspr_references_harmonised_or_cs", False)
        ]
        assert not no_standards_ref, (
            f"GSPR assessment must reference applicable harmonised standards or common "
            f"specifications to demonstrate conformity (EU MDR Annex I / Recital 22). "
            f"Missing references: {[p['device_id'] for p in no_standards_ref]}"
        )

    @pytest.mark.assumption(
        id="ASSUME-EUMDR-GSPR-001",
        description=(
            "GSPR adequacy determination: each applicable GSPR clause requires documented "
            "evidence (harmonised standard, CS, or alternative means); non-applicable clauses "
            "require a documented justification; adequacy of 'state of the art' compliance "
            "is a Notified Body judgment for Class IIa+ devices — the existence of the GSPR "
            "checklist is DETERMINISTIC; its adequacy is PARAMETERIZED"
        ),
        approved_by="regulatory_affairs_manager",
        review_date="2027-05-21",
    )
    def test_gspr_non_applicable_clauses_justified(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        missing_justification = [
            p for p in programs
            if p.get("gspr_assessment_completed", False)
            and not p.get("gspr_non_applicable_clauses_justified", False)
        ]
        assert not missing_justification, (
            f"Non-applicable GSPR clauses must have documented justification in the tech doc "
            f"(EU MDR 2017/745 Annex I). Missing: {[p['device_id'] for p in missing_justification]}"
        )

    def test_risk_management_integrated_in_gspr(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        no_risk_mgmt = [
            p for p in programs
            if p.get("gspr_assessment_completed", False)
            and not p.get("gspr_references_iso14971_risk_file", False)
        ]
        assert not no_risk_mgmt, (
            f"GSPR §2/3 requires risk management per ISO 14971 to be referenced in the "
            f"GSPR assessment (EU MDR Annex I §2). Missing: {[p['device_id'] for p in no_risk_mgmt]}"
        )

    def test_software_gspr_references_iec62304_class(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        software_devices = [p for p in programs if p.get("contains_software", False)]
        missing_sw_classification = [
            p for p in software_devices
            if not p.get("software_iec62304_class_documented", False)
        ]
        assert not missing_sw_classification, (
            f"Devices containing software must have IEC 62304 safety class documented "
            f"in the GSPR assessment (EU MDR Annex I §17). "
            f"Missing: {[p['device_id'] for p in missing_sw_classification]}"
        )
```

---

## Annex II — Technical Documentation

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestTechnicalDocumentation:
    """Annex II — Technical documentation: Part A elements required for all devices."""

    def test_technical_documentation_exists_for_each_device(
        self, controls_evidence: dict
    ):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        missing_td = [p for p in programs if not p.get("technical_documentation_exists", False)]
        assert not missing_td, (
            f"Technical documentation (Annex II) must exist for each device type placed on "
            f"the EU market (EU MDR 2017/745 Article 10(4)). "
            f"Missing: {[p['device_id'] for p in missing_td]}"
        )

    def test_technical_documentation_contains_required_part_a_elements(
        self, controls_evidence: dict
    ):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        for program in programs:
            if not program.get("technical_documentation_exists", False):
                continue
            present = set(program.get("tech_doc_elements_present", []))
            missing = EU_MDR_TECH_DOC_PART_A_ELEMENTS - present
            assert not missing, (
                f"Technical documentation for device '{program['device_id']}' is missing "
                f"Annex II Part A required elements: {missing} "
                f"(EU MDR 2017/745 Annex II)"
            )

    def test_technical_documentation_kept_up_to_date(
        self, controls_evidence: dict
    ):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        stale_td = [
            p for p in programs
            if p.get("technical_documentation_exists", False)
            and not p.get("technical_documentation_kept_current", False)
        ]
        assert not stale_td, (
            f"Technical documentation must be kept up to date throughout the device lifecycle "
            f"(EU MDR 2017/745 Article 10(4)). "
            f"Stale: {[p['device_id'] for p in stale_td]}"
        )

    def test_class_iib_iii_tech_doc_includes_part_b(
        self, controls_evidence: dict
    ):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        high_class_devices = [
            p for p in programs
            if p.get("device_class") in (EU_MDR_CLASS_IIB, EU_MDR_CLASS_III)
        ]
        missing_part_b = [
            p for p in high_class_devices
            if p.get("technical_documentation_exists", False)
            and not p.get("tech_doc_part_b_exists", False)
        ]
        assert not missing_part_b, (
            f"Class IIb and Class III devices require Technical Documentation Part B "
            f"(EU MDR 2017/745 Annex II Part B). Missing: "
            f"{[p['device_id'] for p in missing_part_b]}"
        )
```

---

## Article 19 — EU Declaration of Conformity (DoC)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestDeclarationOfConformity:
    """Article 19 — DoC: 14 mandatory elements (some conditional on class/origin)."""

    def test_doc_exists_for_each_ce_marked_device(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        ce_marked = [p for p in programs if p.get("ce_marked", False)]
        missing_doc = [p for p in ce_marked if not p.get("doc_exists", False)]
        assert not missing_doc, (
            f"EU Declaration of Conformity must exist for each CE-marked device "
            f"(EU MDR 2017/745 Article 19). Missing: {[p['device_id'] for p in missing_doc]}"
        )

    def test_doc_contains_required_unconditional_elements(
        self, controls_evidence: dict
    ):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        for program in programs:
            if not program.get("doc_exists", False):
                continue
            is_non_eu = not program.get("manufacturer_is_eu_based", True)
            nb_involved = program.get("device_class") in EU_MDR_CLASSES_REQUIRING_NOTIFIED_BODY

            required = EU_MDR_DOC_REQUIRED_ELEMENTS.copy()
            if not is_non_eu:
                required -= {"name_and_address_of_authorized_representative"}
            if not nb_involved:
                required -= {
                    "notified_body_name_address_number",
                    "notified_body_certificate_number",
                }

            present = set(program.get("doc_elements_present", []))
            missing = required - present
            assert not missing, (
                f"DoC for device '{program['device_id']}' is missing required elements: "
                f"{missing} (EU MDR 2017/745 Article 19)"
            )
```

---

## Article 11 — Authorized Representative

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestAuthorizedRepresentative:
    """Article 11 — Non-EU manufacturers must designate an EU Authorized Representative."""

    def test_non_eu_manufacturer_has_authorized_representative(
        self, controls_evidence: dict, entity_profile: dict
    ):
        if entity_profile.get("manufacturer_is_eu_based", True):
            return  # EU-based manufacturers exempt
        eu_presence = controls_evidence.get("eu_mdr_eu_presence", {})
        assert eu_presence.get("authorized_representative_designated", False), (
            "Non-EU manufacturers placing devices on the EU market must designate an EU "
            "Authorized Representative (EU MDR 2017/745 Article 11)"
        )
        assert eu_presence.get("authorized_representative_written_mandate_exists", False), (
            "AR mandate must be a written agreement defining the AR's obligations "
            "(EU MDR 2017/745 Article 11(3))"
        )
```

---

## Article 27 — Unique Device Identification (UDI)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestUDI:
    """Article 27 — UDI: carrier on label; registration in EUDAMED."""

    def test_udi_carrier_on_device_label(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        missing_udi = [p for p in programs if not p.get("udi_carrier_on_label", False)]
        assert not missing_udi, (
            f"UDI carrier (Basic UDI-DI + UDI-DI + UDI-PI as applicable) must appear on "
            f"the device label (EU MDR 2017/745 Article 27 + Annex VI). "
            f"Missing UDI: {[p['device_id'] for p in missing_udi]}"
        )

    def test_device_registered_in_eudamed(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        not_registered = [
            p for p in programs
            if not p.get("eudamed_registration_complete", False)
        ]
        assert not not_registered, (
            f"All devices placed on the EU market must be registered in EUDAMED "
            f"(EU MDR 2017/745 Article 27 + Article 29). "
            f"Not registered: {[p['device_id'] for p in not_registered]}"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-EUMDR-GSPR-001 | Annex I | GSPR adequacy: harmonised standard compliance is PARAMETERIZED; checklist existence is DETERMINISTIC | 2027-05-21 |
