# EPA RCRA — Hazardous Waste Generator Requirements

**Framework:** Resource Conservation and Recovery Act (42 U.S.C. §6901 et seq.) — 40 CFR Parts 261–262; 40 CFR Part 264/265 (TSD); 40 CFR Part 268 (LDR)
**Clauses:** §261.3 (hazardous waste identification); §261.5 (VSQG); §262.10–262.210 (generator requirements — accumulation, manifests, preparedness, training); §262.17 (LQG emergency coordinator); §268 (land disposal restrictions)
**Confidence:** DETERMINISTIC-dominant (generator category thresholds; accumulation time limits; manifest required fields; contingency plan required elements; training frequency; LDR notification); PARAMETERIZED (waste characterization methodology; TCLP applicability); CONTESTED (listed waste applicability; mixture rule; derived-from rule)
**Last parsed:** 2026-05-21
**Applies to:** Any facility that generates, transports, treats, stores, or disposes of hazardous waste as defined in 40 CFR Part 261; generator requirements (Part 262) apply to any facility generating hazardous waste in any quantity; VSQG, SQG, and LQG categories have different regulatory burdens
**Trigger:** Generation of hazardous waste — any solid waste that is either listed (F, K, P, U lists) or exhibits a characteristic (ignitability, corrosivity, reactivity, toxicity); monthly quantity generated determines category; category assessed monthly
**Jurisdiction:** United States federal; enforced by EPA or authorized state programs (most states have RCRA authorization); authorized state programs may have requirements stricter than federal baseline
**Not applicable to:** Household hazardous waste; agricultural waste used on the land where it was generated; mining and mineral processing overburden; coal combustion residues managed in surface impoundments (subject to 40 CFR Part 257); radioactive waste (NRC regulated)

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def rcra_scope(entity_profile: dict):
    if not entity_profile.get("generates_hazardous_waste", False):
        pytest.skip(
            "RCRA hazardous waste generator requirements (40 CFR Part 262) do not apply — "
            "facility generates no hazardous waste as defined in 40 CFR Part 261."
        )
```

---

## Constants

```python
from typing import FrozenSet

# ── Generator category thresholds (40 CFR §262.13) ────────────────────────────

RCRA_LQG_THRESHOLD_KG_PER_MONTH = 1000
RCRA_SQG_LOWER_THRESHOLD_KG_PER_MONTH = 100
RCRA_VSQG_UPPER_THRESHOLD_KG_PER_MONTH = 100   # exclusive — < 100 kg

# ── Accumulation time limits ───────────────────────────────────────────────────

RCRA_LQG_ACCUMULATION_DAYS = 90
RCRA_SQG_ACCUMULATION_DAYS = 270
RCRA_SQG_QUANTITY_LIMIT_KG = 6000

# ── Characteristic waste thresholds (40 CFR §261.21–261.24) ───────────────────

RCRA_IGNITABILITY_FLASH_POINT_CELSIUS = 60       # D001: flash point < 60°C for liquids
RCRA_CORROSIVITY_PH_LOW = 2                      # D002: pH ≤ 2
RCRA_CORROSIVITY_PH_HIGH = 12.5                  # D002: pH ≥ 12.5

# ── Manifest required information (40 CFR §262.20) ────────────────────────────

RCRA_MANIFEST_REQUIRED_FIELDS: FrozenSet[str] = frozenset({
    "generator_epa_id_number",
    "generator_name_and_address",
    "transporter_1_epa_id",
    "designated_facility_epa_id",
    "designated_facility_name_and_address",
    "waste_description_and_proper_shipping_name",
    "epa_waste_code",
    "dot_hazard_class",
    "quantity_and_units",
    "emergency_response_phone_number",
    "generator_certification_signature",
    "manifest_tracking_number",
})

# ── LQG contingency plan required elements (40 CFR §262.262) ─────────────────

LQG_CONTINGENCY_PLAN_REQUIRED_ELEMENTS: FrozenSet[str] = frozenset({
    "emergency_coordinator_designation_and_24hr_contact",
    "list_of_emergency_equipment",
    "evacuation_plan",
    "arrangements_with_local_emergency_responders",
    "list_of_all_hazardous_wastes_onsite",
    "description_of_emergency_procedures",
})

# ── LQG training requirements (40 CFR §262.17(a)(7)) ─────────────────────────

LQG_INITIAL_TRAINING_BEFORE_WORKING_UNSUPERVISED = True
LQG_ANNUAL_TRAINING_REVIEW_REQUIRED = True
```

---

## TestGeneratorCategoryDetermination

```python
class TestGeneratorCategoryDetermination:
    """40 CFR §262.13 — Generator category determined monthly by quantity generated."""

    def test_generator_category_correctly_determined(self, entity_profile: dict):
        """§262.13: Generator category (LQG/SQG/VSQG) must be determined monthly
        based on total hazardous waste generated in the calendar month."""
        monthly_kg = entity_profile.get("monthly_hazardous_waste_kg", 0)
        reported_category = entity_profile.get("generator_category")
        if monthly_kg >= RCRA_LQG_THRESHOLD_KG_PER_MONTH:
            expected = "LQG"
        elif monthly_kg >= RCRA_SQG_LOWER_THRESHOLD_KG_PER_MONTH:
            expected = "SQG"
        else:
            expected = "VSQG"
        assert reported_category == expected, (
            f"Generator category '{reported_category}' does not match "
            f"quantity-based determination '{expected}' for {monthly_kg} kg/month — "
            f"40 CFR §262.13"
        )

    def test_category_reassessment_is_monthly(self, entity_profile: dict):
        """§262.13(b): Category must be reassessed each calendar month."""
        assert entity_profile.get("monthly_category_reassessment_documented") is True, \
            "Generator category reassessment not documented monthly — 40 CFR §262.13(b)"
```

---

## TestAccumulationTimeLimits

```python
class TestAccumulationTimeLimits:
    """40 CFR §262.17 (LQG), §262.16 (SQG) — Accumulation time limits."""

    def test_lqg_accumulation_within_90_days(self, entity_profile: dict):
        """§262.17(a): LQG facilities must ship all hazardous waste off-site within 90 days
        of start of accumulation."""
        if entity_profile.get("generator_category") != "LQG":
            pytest.skip("90-day accumulation limit applies to LQG only")
        from datetime import date
        for container in entity_profile.get("onsite_hazardous_waste_containers", []):
            start = container.get("accumulation_start_date")
            if start is None:
                continue
            age_days = (date.today() - start).days
            assert age_days <= RCRA_LQG_ACCUMULATION_DAYS, (
                f"Container '{container.get('id', 'unknown')}' has been accumulating for "
                f"{age_days} days, exceeding the 90-day LQG limit — 40 CFR §262.17(a)"
            )

    def test_sqg_accumulation_within_270_days(self, entity_profile: dict):
        """§262.16(b): SQG facilities must ship hazardous waste off-site within 270 days
        and may not accumulate more than 6,000 kg."""
        if entity_profile.get("generator_category") != "SQG":
            pytest.skip("270-day accumulation limit applies to SQG only")
        from datetime import date
        total_kg = 0
        for container in entity_profile.get("onsite_hazardous_waste_containers", []):
            start = container.get("accumulation_start_date")
            if start:
                age_days = (date.today() - start).days
                assert age_days <= RCRA_SQG_ACCUMULATION_DAYS, (
                    f"Container '{container.get('id', 'unknown')}' has been accumulating for "
                    f"{age_days} days, exceeding the 270-day SQG limit — 40 CFR §262.16(b)"
                )
            total_kg += container.get("quantity_kg", 0)
        assert total_kg <= RCRA_SQG_QUANTITY_LIMIT_KG, (
            f"SQG total on-site quantity {total_kg} kg exceeds 6,000 kg limit — "
            f"40 CFR §262.16(b)"
        )
```

---

## TestCharacteristicWasteIdentification

```python
class TestCharacteristicWasteIdentification:
    """40 CFR §§261.21–261.24 — Characteristic hazardous waste thresholds (D001–D043)."""

    def test_d001_ignitability_threshold(self, entity_profile: dict):
        """§261.21: Liquid waste with flash point < 60°C is D001 ignitable hazardous waste."""
        for waste in entity_profile.get("waste_streams", []):
            if waste.get("waste_type") == "liquid" and waste.get("flash_point_celsius") is not None:
                fp = waste["flash_point_celsius"]
                is_classified_d001 = waste.get("waste_codes", []) and "D001" in waste["waste_codes"]
                if fp < RCRA_IGNITABILITY_FLASH_POINT_CELSIUS:
                    assert is_classified_d001, (
                        f"Waste stream '{waste.get('id', 'unknown')}' with flash point {fp}°C "
                        f"must be classified as D001 ignitable hazardous waste — 40 CFR §261.21"
                    )

    def test_d002_corrosivity_threshold(self, entity_profile: dict):
        """§261.22: Aqueous waste with pH ≤ 2 or ≥ 12.5 is D002 corrosive hazardous waste."""
        for waste in entity_profile.get("waste_streams", []):
            if waste.get("waste_type") == "aqueous" and waste.get("ph") is not None:
                ph = waste["ph"]
                is_classified_d002 = waste.get("waste_codes", []) and "D002" in waste["waste_codes"]
                if ph <= RCRA_CORROSIVITY_PH_LOW or ph >= RCRA_CORROSIVITY_PH_HIGH:
                    assert is_classified_d002, (
                        f"Waste stream '{waste.get('id', 'unknown')}' with pH {ph} must be "
                        f"classified as D002 corrosive hazardous waste — 40 CFR §261.22"
                    )
```

---

## TestManifestRequirements

```python
class TestManifestRequirements:
    """40 CFR §262.20 — Hazardous waste manifest: required fields and retention."""

    def test_manifest_used_for_all_offsite_shipments(self, entity_profile: dict):
        """§262.20(a): Manifest required before transporting hazardous waste off-site."""
        if entity_profile.get("generator_category") == "VSQG":
            pytest.skip("VSQGs are not required to use a manifest (40 CFR §262.14(c))")
        for shipment in entity_profile.get("hazardous_waste_shipments", []):
            assert shipment.get("manifest_completed") is True, (
                f"Shipment '{shipment.get('id', 'unknown')}' to "
                f"'{shipment.get('destination', 'unknown')}' has no manifest — "
                f"40 CFR §262.20(a)"
            )

    def test_manifest_has_all_required_fields(self, entity_profile: dict):
        """§262.20: All required manifest fields must be completed."""
        if entity_profile.get("generator_category") == "VSQG":
            pytest.skip("VSQGs do not use manifests")
        for shipment in entity_profile.get("hazardous_waste_shipments", []):
            manifest = shipment.get("manifest", {})
            present = frozenset(k for k, v in manifest.items() if v)
            missing = RCRA_MANIFEST_REQUIRED_FIELDS - present
            assert not missing, (
                f"Manifest for shipment '{shipment.get('id', 'unknown')}' missing "
                f"required fields: {sorted(missing)} — 40 CFR §262.20"
            )

    def test_exception_report_if_return_copy_not_received(self, entity_profile: dict):
        """§262.42: If signed return copy not received within 35 days (LQG) or 60 days (SQG),
        exception report must be filed with EPA."""
        from datetime import date, timedelta
        category = entity_profile.get("generator_category")
        if category == "VSQG":
            pytest.skip("VSQGs do not use manifests")
        deadline_days = 35 if category == "LQG" else 60
        for shipment in entity_profile.get("hazardous_waste_shipments", []):
            shipped_date = shipment.get("shipped_date")
            return_received = shipment.get("return_copy_received")
            if shipped_date and not return_received:
                days_elapsed = (date.today() - shipped_date).days
                if days_elapsed > deadline_days:
                    assert shipment.get("exception_report_filed") is True, (
                        f"Return copy not received {days_elapsed} days after shipment "
                        f"'{shipment.get('id', 'unknown')}' — exception report required "
                        f"after {deadline_days} days — 40 CFR §262.42"
                    )
```

---

## TestLQGContingencyPlan

```python
class TestLQGContingencyPlan:
    """40 CFR §§262.262–262.264 — LQG contingency plan and emergency coordinator."""

    def test_contingency_plan_exists_and_is_written(self, entity_profile: dict):
        """§262.262: LQG must have a written contingency plan."""
        if entity_profile.get("generator_category") != "LQG":
            pytest.skip("Contingency plan requirement (§262.262) applies to LQG only")
        assert entity_profile.get("contingency_plan", {}).get("written_and_current") is True, \
            "LQG must have a written, current contingency plan — 40 CFR §262.262"

    def test_contingency_plan_has_required_elements(self, entity_profile: dict):
        """§262.262: Contingency plan must contain all required elements."""
        if entity_profile.get("generator_category") != "LQG":
            pytest.skip("Applies to LQG only")
        plan_elements = frozenset(entity_profile.get("contingency_plan", {}).get("elements", []))
        missing = LQG_CONTINGENCY_PLAN_REQUIRED_ELEMENTS - plan_elements
        assert not missing, (
            f"Contingency plan missing required elements: {sorted(missing)} — "
            f"40 CFR §262.262"
        )

    def test_emergency_coordinator_designated_24hr(self, entity_profile: dict):
        """§262.17(a)(6): LQG must have a designated emergency coordinator available 24/7."""
        if entity_profile.get("generator_category") != "LQG":
            pytest.skip("Applies to LQG only")
        ec = entity_profile.get("emergency_coordinator", {})
        assert ec.get("designated") is True, \
            "No emergency coordinator designated — 40 CFR §262.17(a)(6)"
        assert ec.get("available_24_hours") is True, \
            "Emergency coordinator must be available 24 hours/day — 40 CFR §262.17(a)(6)"
```

---

## TestPersonnelTraining

```python
class TestPersonnelTraining:
    """40 CFR §262.17(a)(7) — LQG personnel training requirements."""

    def test_lqg_initial_training_completed_before_unsupervised_work(self, entity_profile: dict):
        """§262.17(a)(7): LQG employees must complete initial training before working
        with hazardous waste without supervision."""
        if entity_profile.get("generator_category") != "LQG":
            pytest.skip("Training requirement (§262.17(a)(7)) applies to LQG only")
        for employee in entity_profile.get("hazardous_waste_employees", []):
            assert employee.get("initial_training_completed_before_unsupervised") is True, (
                f"Employee '{employee.get('name', 'unknown')}' has not completed initial "
                f"training before working with hazardous waste — 40 CFR §262.17(a)(7)"
            )

    def test_lqg_annual_training_review(self, entity_profile: dict):
        """§262.17(a)(7): Training must be reviewed annually."""
        if entity_profile.get("generator_category") != "LQG":
            pytest.skip("Applies to LQG only")
        from datetime import date
        from dateutil.relativedelta import relativedelta
        one_year_ago = date.today() - relativedelta(years=1)
        for employee in entity_profile.get("hazardous_waste_employees", []):
            last_training = employee.get("last_annual_training_date")
            assert last_training is not None, (
                f"No annual training record for '{employee.get('name', 'unknown')}' — "
                f"40 CFR §262.17(a)(7)"
            )
            assert last_training >= one_year_ago, (
                f"Annual training overdue for '{employee.get('name', 'unknown')}': "
                f"last training {last_training}, must be within 1 year — 40 CFR §262.17(a)(7)"
            )

    def test_training_records_retained_three_years(self, entity_profile: dict):
        """§262.17(a)(7)(v): Training records must be retained for 3 years."""
        if entity_profile.get("generator_category") != "LQG":
            pytest.skip("Applies to LQG only")
        assert entity_profile.get("training_record_retention_years", 0) >= 3, \
            "Training records must be retained for 3 years — 40 CFR §262.17(a)(7)(v)"
```

---

## TestLandDisposalRestrictions

```python
class TestLandDisposalRestrictions:
    """40 CFR Part 268 — Land Disposal Restrictions (LDR): notification with each shipment."""

    def test_ldr_notification_accompanies_shipment(self, entity_profile: dict):
        """§268.7: Generator must include an LDR notification/certification with
        each shipment of hazardous waste to a treatment or disposal facility."""
        if entity_profile.get("generator_category") == "VSQG":
            pytest.skip("LDR notification may not apply to VSQGs")
        for shipment in entity_profile.get("hazardous_waste_shipments", []):
            if shipment.get("destination_type") in ("treatment", "disposal"):
                assert shipment.get("ldr_notification_included") is True, (
                    f"Shipment '{shipment.get('id', 'unknown')}' to treatment/disposal "
                    f"facility lacks LDR notification — 40 CFR §268.7"
                )
```
