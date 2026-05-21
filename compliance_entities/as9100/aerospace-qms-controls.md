# AS9100 Rev D — Aerospace QMS Controls

**Framework:** AS9100 Rev D (2016)
**Clauses:** 6.1.2.3–6.1.2.4, 8.1.2–8.1.4, 8.3.4.3, 8.4.1, 8.5.1.1–8.5.2, 8.5.6–8.5.7, 8.6.2, 8.7.1, 8.7.3, 9.1.1.1
**Parent:** ISO 9001:2015 (all ISO 9001 requirements apply simultaneously — see iso/9001/)
**Confidence:** DETERMINISTIC-dominant (FAI completeness, counterfeit prevention, FOD program, KC controls, configuration management)
**Last parsed:** 2026-05-21
**Applies to:** Aviation, space, and defense (AS&D) manufacturers and their supply chains — Tier 1 and Tier 2 suppliers to aerospace OEMs providing parts, assemblies, or services for aircraft, spacecraft, or defense systems
**Trigger:** Customer requirement from aerospace OEMs (Boeing, Airbus, Lockheed Martin, Raytheon, Northrop Grumman, etc.) or prime contractors mandating AS9100 Rev D certification; required for NADCAP special process accreditation; FAR/DFARS supply chain flow-down
**Jurisdiction:** Global — IAQG (International Aerospace Quality Group) standard with regional bodies: AAQG (Americas), EAQG (Europe), JIAQG (Asia-Pacific)
**Not applicable to:** Non-aerospace manufacturers; MRO organizations (AS9110 applies instead); design-only organizations (AS9100 scope applies differently); companies providing services to aerospace without making parts (may use AS9100 or AS9120 for distributors)

---

## Scope pre-condition

```python
@pytest.fixture(autouse=True)
def as9100_scope(entity_profile: dict):
    if not entity_profile.get("as9100_in_scope", False):
        pytest.skip("AS9100 Rev D not in scope")
```

---

## Constants

```python
# First Article Inspection (FAI) — AS9102 3 forms
AS9100_FAI_REQUIRED_FORMS = frozenset({
    "form1_part_number_accountability",
    "form2_product_accountability",
    "form3_characteristic_accountability",
})

# FAI triggers — any of these require a new FAI
AS9100_FAI_TRIGGERS = frozenset({
    "new_part_number",
    "design_change_affecting_form_fit_function",
    "process_change_affecting_product_characteristics",
    "resourcing_to_different_facility_or_supplier",
    "interruption_of_production_exceeding_defined_period",
})

# FOD prevention program required elements
AS9100_FOD_PROGRAM_REQUIRED_ELEMENTS = frozenset({
    "written_fod_prevention_procedures",
    "fod_training_for_production_personnel",
    "fod_inspection_at_defined_stages",
    "fod_inspection_records_retained",
    "fod_prevention_responsibility_assigned",
})

# Configuration management required elements — §6.1.2.3
AS9100_CONFIG_MGMT_REQUIRED_ELEMENTS = frozenset({
    "configuration_identification",
    "configuration_control",
    "configuration_status_accounting",
    "configuration_audits",
})

# Counterfeit part prevention — §8.1.4
AS9100_COUNTERFEIT_PREVENTION_REQUIRED_ELEMENTS = frozenset({
    "written_counterfeit_prevention_process",
    "approved_supplier_list_enforced",
    "suspect_counterfeit_quarantine_procedure",
    "suspect_counterfeit_reporting_process",
    "traceability_to_original_manufacturer",
})
```

---

## §6.1.2.3 — Configuration Management

**Overall: DETERMINISTIC — Pattern 1**

```python
import pytest

class TestConfigurationManagement:
    """§6.1.2.3 — Configuration management process required across the product lifecycle."""

    def test_configuration_management_plan_exists(self, controls_evidence: dict):
        config = controls_evidence.get("as9100_configuration_management", {})
        assert config.get("configuration_management_process_documented", False), (
            "Configuration management process must be documented and implemented "
            "(AS9100 Rev D §6.1.2.3)"
        )

    def test_configuration_management_covers_required_elements(
        self, controls_evidence: dict
    ):
        config = controls_evidence.get("as9100_configuration_management", {})
        elements_present = set(config.get("elements_implemented", []))
        missing = AS9100_CONFIG_MGMT_REQUIRED_ELEMENTS - elements_present
        assert not missing, (
            f"Configuration management process must include all required elements: "
            f"{missing} (AS9100 Rev D §6.1.2.3)"
        )

    def test_design_changes_require_configuration_authorization(
        self, controls_evidence: dict
    ):
        design_changes = controls_evidence.get("as9100_design_changes", [])
        unauthorized = [
            c for c in design_changes
            if not c.get("configuration_change_authorized", False)
        ]
        assert not unauthorized, (
            f"All changes to configuration items must be authorized before implementation "
            f"(AS9100 Rev D §6.1.2.3). Unauthorized: "
            f"{[c['change_id'] for c in unauthorized]}"
        )
```

---

## §6.1.2.4 — Product Safety

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestProductSafety:
    """§6.1.2.4 — Product safety processes; safety-critical characteristics; reporting obligations."""

    def test_product_safety_responsibility_assigned(self, controls_evidence: dict):
        safety = controls_evidence.get("as9100_product_safety", {})
        assert safety.get("safety_responsibility_assigned", False), (
            "Responsibility for promoting and maintaining product safety culture must be "
            "assigned (AS9100 Rev D §6.1.2.4)"
        )

    def test_safety_critical_characteristics_identified(self, controls_evidence: dict):
        programs = controls_evidence.get("as9100_production_programs", [])
        missing_sc_identification = [
            p for p in programs
            if p.get("has_safety_critical_characteristics", True)
            and not p.get("safety_critical_characteristics_identified", False)
        ]
        assert not missing_sc_identification, (
            f"Safety-critical characteristics must be identified for all applicable programs "
            f"(AS9100 Rev D §6.1.2.4). Missing: "
            f"{[p['program_id'] for p in missing_sc_identification]}"
        )

    def test_product_safety_escapes_reported(self, controls_evidence: dict):
        safety_escapes = controls_evidence.get("as9100_product_safety_escapes", [])
        not_reported = [
            e for e in safety_escapes
            if not e.get("customer_or_regulatory_notification_sent", False)
        ]
        assert not not_reported, (
            f"Product safety escapes (characteristics affecting airworthiness or safety) "
            f"must be reported to customer and/or regulator (AS9100 Rev D §6.1.2.4). "
            f"Not reported: {[e['escape_id'] for e in not_reported]}"
        )
```

---

## §8.1.4 — Prevention of Counterfeit Parts

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestCounterfeitPartPrevention:
    """§8.1.4 — Written counterfeit prevention process; approved sources; suspect part handling."""

    def test_counterfeit_prevention_process_covers_required_elements(
        self, controls_evidence: dict
    ):
        counterfeit = controls_evidence.get("as9100_counterfeit_prevention", {})
        elements_present = set(counterfeit.get("elements_implemented", []))
        missing = AS9100_COUNTERFEIT_PREVENTION_REQUIRED_ELEMENTS - elements_present
        assert not missing, (
            f"Counterfeit prevention process must include all required elements: "
            f"{missing} (AS9100 Rev D §8.1.4)"
        )

    def test_parts_sourced_from_approved_suppliers(self, controls_evidence: dict):
        purchase_orders = controls_evidence.get("as9100_purchase_orders", [])
        unapproved_source = [
            po for po in purchase_orders
            if po.get("is_hardware_or_electronic_component", True)
            and not po.get("supplier_on_approved_list", False)
        ]
        assert not unapproved_source, (
            f"Hardware and electronic components must be sourced from approved suppliers "
            f"to mitigate counterfeit risk (AS9100 Rev D §8.1.4). "
            f"Unapproved: {[po['po_id'] for po in unapproved_source]}"
        )

    def test_suspect_counterfeit_parts_quarantined(self, controls_evidence: dict):
        suspect_parts = controls_evidence.get("as9100_suspect_counterfeit_parts", [])
        not_quarantined = [
            p for p in suspect_parts
            if not p.get("quarantined", False)
        ]
        assert not not_quarantined, (
            f"Suspect counterfeit parts must be quarantined and prevented from use "
            f"(AS9100 Rev D §8.1.4). Not quarantined: "
            f"{[p['part_id'] for p in not_quarantined]}"
        )

    def test_suspect_counterfeit_parts_reported(self, controls_evidence: dict):
        suspect_parts = controls_evidence.get("as9100_suspect_counterfeit_parts", [])
        not_reported = [
            p for p in suspect_parts
            if not p.get("reported_to_customer_or_industry_group", False)
        ]
        assert not not_reported, (
            f"Suspect counterfeit parts must be reported to customer and/or industry "
            f"reporting organizations (AS9100 Rev D §8.1.4). "
            f"Not reported: {[p['part_id'] for p in not_reported]}"
        )
```

---

## §8.3.4.3 — Key Characteristics

**Overall: DETERMINISTIC — Pattern 1/2**

```python
class TestKeyCharacteristics:
    """§8.3.4.3 — Key characteristics: identified in design, controlled in production."""

    @pytest.mark.assumption(
        id="ASSUME-AS9100-KC-001",
        description=(
            "Key characteristic (KC) identification scope: KCs designated by customer "
            "drawing, specification, or mutual agreement; internal KCs designated through "
            "DFMEA/PFMEA analysis where variation significantly impacts fit, performance, "
            "service life, or producibility; KC identification is customer-driven or "
            "organization-determined — the identification process is PARAMETERIZED but "
            "the subsequent controls are DETERMINISTIC"
        ),
        approved_by="quality_engineer",
        review_date="2027-05-21",
    )
    def test_key_characteristics_identified_in_design_outputs(
        self, controls_evidence: dict
    ):
        programs = controls_evidence.get("as9100_production_programs", [])
        missing_kc_identification = [
            p for p in programs
            if p.get("has_key_characteristics", True)
            and not p.get("key_characteristics_in_design_documentation", False)
        ]
        assert not missing_kc_identification, (
            f"Key characteristics must be identified and documented in design outputs "
            f"(AS9100 Rev D §8.3.4.3). Missing: "
            f"{[p['program_id'] for p in missing_kc_identification]}"
        )

    def test_key_characteristics_referenced_in_control_plans(
        self, controls_evidence: dict
    ):
        programs = controls_evidence.get("as9100_production_programs", [])
        missing_kc_in_cp = [
            p for p in programs
            if p.get("has_key_characteristics", True)
            and not p.get("control_plan_references_key_characteristics", False)
        ]
        assert not missing_kc_in_cp, (
            f"Key characteristics must be referenced in control plans with defined "
            f"monitoring/inspection methods (AS9100 Rev D §8.3.4.3). "
            f"Missing: {[p['program_id'] for p in missing_kc_in_cp]}"
        )

    def test_key_characteristics_have_statistical_control_or_100pct_inspection(
        self, controls_evidence: dict
    ):
        key_characteristics = controls_evidence.get("as9100_key_characteristics", [])
        no_control = [
            kc for kc in key_characteristics
            if not kc.get("spc_applied", False)
            and not kc.get("100_percent_inspection_applied", False)
        ]
        assert not no_control, (
            f"Key characteristics must be monitored via SPC or 100% inspection "
            f"(AS9100 Rev D §8.3.4.3). Missing controls: "
            f"{[kc['characteristic_id'] for kc in no_control]}"
        )
```

---

## §8.5.1.1 — FOD Prevention Program

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestFODPrevention:
    """§8.5.1.1 / AS9100 Rev D — FOD prevention: written program; training; inspections."""

    def test_fod_prevention_program_covers_required_elements(
        self, controls_evidence: dict
    ):
        fod = controls_evidence.get("as9100_fod_prevention", {})
        elements_present = set(fod.get("elements_implemented", []))
        missing = AS9100_FOD_PROGRAM_REQUIRED_ELEMENTS - elements_present
        assert not missing, (
            f"FOD prevention program must include all required elements: "
            f"{missing} (AS9100 Rev D — FOD prevention)"
        )

    def test_fod_inspection_records_retained(self, controls_evidence: dict):
        fod = controls_evidence.get("as9100_fod_prevention", {})
        assert fod.get("fod_inspection_records_retained", False), (
            "FOD inspection records at defined manufacturing stages must be retained "
            "(AS9100 Rev D — FOD prevention)"
        )

    def test_fod_training_records_retained(self, controls_evidence: dict):
        fod = controls_evidence.get("as9100_fod_prevention", {})
        assert fod.get("fod_training_records_retained", False), (
            "FOD prevention training records for all production personnel must be retained "
            "(AS9100 Rev D — FOD prevention)"
        )
```

---

## §8.6.2 — First Article Inspection (FAI)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestFirstArticleInspection:
    """§8.6.2 — FAI required per AS9102; all 3 forms completed before production release."""

    def test_fai_performed_before_production_release(self, controls_evidence: dict):
        programs = controls_evidence.get("as9100_production_programs", [])
        no_fai = [
            p for p in programs
            if p.get("fai_required", True)
            and not p.get("fai_completed", False)
        ]
        assert not no_fai, (
            f"First Article Inspection (FAI) per AS9102 must be completed before "
            f"production release (AS9100 Rev D §8.6.2). "
            f"Missing FAI: {[p['program_id'] for p in no_fai]}"
        )

    def test_fai_contains_all_three_forms(self, controls_evidence: dict):
        programs = controls_evidence.get("as9100_production_programs", [])
        for program in programs:
            if not program.get("fai_completed", False):
                continue
            forms_present = set(program.get("fai_forms_completed", []))
            missing_forms = AS9100_FAI_REQUIRED_FORMS - forms_present
            assert not missing_forms, (
                f"FAI for program '{program['program_id']}' must include all 3 AS9102 forms. "
                f"Missing: {missing_forms} (AS9100 Rev D §8.6.2)"
            )

    def test_fai_triggered_for_design_or_process_changes(
        self, controls_evidence: dict
    ):
        change_events = controls_evidence.get("as9100_significant_changes", [])
        fai_required_but_missing = [
            e for e in change_events
            if e.get("fai_trigger_met", False)
            and not e.get("fai_performed", False)
        ]
        assert not fai_required_but_missing, (
            f"FAI must be performed after any change that triggers a new FAI requirement "
            f"(design change affecting F/F/F, process change, resourcing) "
            f"(AS9100 Rev D §8.6.2). Missing FAI: "
            f"{[e['change_id'] for e in fai_required_but_missing]}"
        )

    def test_fai_records_retained_for_part_life(self, controls_evidence: dict):
        programs = controls_evidence.get("as9100_production_programs", [])
        fai_no_retention = [
            p for p in programs
            if p.get("fai_completed", False)
            and not p.get("fai_records_retained", False)
        ]
        assert not fai_no_retention, (
            f"FAI records must be retained for the life of the part "
            f"(AS9100 Rev D §8.6.2). Missing retention: "
            f"{[p['program_id'] for p in fai_no_retention]}"
        )
```

---

## §8.5.2 — Identification and Traceability

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestAerospaceTraceability:
    """§8.5.2 — Traceability to original manufacturer for safety-critical parts; lot traceability."""

    def test_safety_critical_parts_traceable_to_original_manufacturer(
        self, controls_evidence: dict
    ):
        parts = controls_evidence.get("as9100_production_parts", [])
        safety_critical = [p for p in parts if p.get("safety_critical", False)]
        not_traceable = [
            p for p in safety_critical
            if not p.get("traceable_to_original_manufacturer", False)
        ]
        assert not not_traceable, (
            f"Safety-critical parts must be traceable to original manufacturer "
            f"(AS9100 Rev D §8.5.2). Missing traceability: "
            f"{[p['part_id'] for p in not_traceable]}"
        )
```

---

## §8.7.1 / §8.7.3 — Nonconforming Product (Aerospace)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestAerospaceNonconformingProduct:
    """§8.7.1/§8.7.3 — Safety impact assessed; scrap/use-as-is requires engineering auth."""

    def test_safety_implications_assessed_for_nonconformances(
        self, controls_evidence: dict
    ):
        ncrs = controls_evidence.get("as9100_nonconformance_records", [])
        no_safety_assessment = [
            ncr for ncr in ncrs
            if not ncr.get("safety_impact_assessed", False)
        ]
        assert not no_safety_assessment, (
            f"Every nonconformance record must include a safety impact assessment "
            f"(AS9100 Rev D §8.7.1). Missing: {[ncr['ncr_id'] for ncr in no_safety_assessment]}"
        )

    def test_use_as_is_disposition_requires_engineering_authorization(
        self, controls_evidence: dict
    ):
        ncrs = controls_evidence.get("as9100_nonconformance_records", [])
        use_as_is = [ncr for ncr in ncrs if ncr.get("disposition") == "use_as_is"]
        no_auth = [
            ncr for ncr in use_as_is
            if not ncr.get("engineering_authorization_obtained", False)
        ]
        assert not no_auth, (
            f"Use-as-is disposition requires formal engineering authorization "
            f"(AS9100 Rev D §8.7.3). Missing auth: {[ncr['ncr_id'] for ncr in no_auth]}"
        )

    def test_safety_impacting_nonconformances_reported_to_customer(
        self, controls_evidence: dict
    ):
        ncrs = controls_evidence.get("as9100_nonconformance_records", [])
        safety_impacting = [
            ncr for ncr in ncrs
            if ncr.get("safety_impact_assessed", False)
            and ncr.get("safety_impacting", False)
        ]
        not_reported = [
            ncr for ncr in safety_impacting
            if not ncr.get("customer_notified", False)
        ]
        assert not not_reported, (
            f"Nonconformances impacting product safety or airworthiness must be reported "
            f"to customer and/or regulatory authority (AS9100 Rev D §8.7.1). "
            f"Not reported: {[ncr['ncr_id'] for ncr in not_reported]}"
        )
```

---

## §9.1.1.1 — KC Monitoring and SPC

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestKCMonitoringAndSPC:
    """§9.1.1.1 — Key characteristics monitored per control plan; SPC records retained."""

    def test_kc_spc_records_retained(self, controls_evidence: dict):
        key_characteristics = controls_evidence.get("as9100_key_characteristics", [])
        spc_kcs = [kc for kc in key_characteristics if kc.get("spc_applied", False)]
        no_records = [kc for kc in spc_kcs if not kc.get("spc_records_retained", False)]
        assert not no_records, (
            f"SPC records for key characteristics must be retained "
            f"(AS9100 Rev D §9.1.1.1). Missing records: "
            f"{[kc['characteristic_id'] for kc in no_records]}"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-AS9100-KC-001 | 8.3.4.3 | KC identification: customer-driven or FMEA-derived; identification process PARAMETERIZED, controls DETERMINISTIC | 2027-05-21 |
