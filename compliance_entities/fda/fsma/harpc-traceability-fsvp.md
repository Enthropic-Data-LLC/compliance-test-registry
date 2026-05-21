# FDA FSMA — HARPC, Enhanced Traceability, and FSVP

**Framework:** Food Safety Modernization Act (21 U.S.C. §2201 et seq.) — 21 CFR Part 117 (HARPC), 21 CFR Part 204 (Enhanced Traceability), 21 CFR Part 1 Subpart L (FSVP)
**Clauses:** §117.126–§117.180 (Food Safety Plan elements); §117.135 (preventive controls); §117.305 (record retention); §204.210 (traceability retrieval); Part 1 Subpart L (FSVP hazard analysis and supplier verification)
**Confidence:** DETERMINISTIC-dominant (Food Safety Plan required elements; allergen program documentation; 2-year record retention; 24-hour FTL retrieval; FSVP importer of record designation); PARAMETERIZED (hazard characterization; process control critical parameters; supplier verification activity selection); CONTESTED (reasonable foreseeable hazard scope)
**Last parsed:** 2026-05-21
**Applies to:** Domestic and foreign food facilities that manufacture, process, pack, or hold food for human consumption in the US and are required to register under 21 CFR Part 1; US importers of food as FSVP importers; enhanced traceability applies to handlers of foods on the Food Traceability List (FTL)
**Trigger:** FDA facility registration under 21 CFR §1.226; importing food into the US interstate commerce; handling FTL foods at any point in the supply chain (harvesting through retail)
**Jurisdiction:** United States; FDA enforces; foreign facilities exporting to US subject to extraterritorial application; state agencies may have concurrent authority
**Not applicable to:** Farms (except produce farms under Part 112 Produce Safety Rule); retail food establishments; restaurants; non-profit charitable food facilities; fishing vessels; very small businesses (< $1M annual food sales) receive extended timelines and modified requirements; facilities exclusively subject to other FDA rules (seafood HACCP Part 123, juice HACCP Part 120)

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def fsma_scope(entity_profile: dict):
    if not entity_profile.get("fda_registered_food_facility", False):
        pytest.skip(
            "FDA FSMA HARPC (21 CFR Part 117) does not apply — "
            "entity_profile['fda_registered_food_facility'] is False. "
            "Exemptions: farms, retail food establishments, restaurants, "
            "fishing vessels, non-profit charitable facilities."
        )

@pytest.fixture
def fsvp_scope(entity_profile: dict):
    """Additional fixture for FSVP — US importers of food."""
    if not entity_profile.get("fsvp_importer", False):
        pytest.skip("FSVP (21 CFR Part 1 Subpart L) applies only to US importers of food.")

@pytest.fixture
def ftl_scope(entity_profile: dict):
    """Additional fixture for Enhanced Traceability — handlers of FTL foods."""
    if not entity_profile.get("handles_ftl_foods", False):
        pytest.skip(
            "Enhanced Traceability Rule (21 CFR Part 204) applies only to facilities "
            "handling Food Traceability List (FTL) foods."
        )
```

---

## Constants

```python
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from typing import FrozenSet

# ── Record retention (21 CFR §117.305) ────────────────────────────────────────

FSMA_RECORD_RETENTION_YEARS = 2  # All HARPC records — 2 years minimum

# ── Enhanced Traceability (21 CFR §204.210) ───────────────────────────────────

FSMA_FTL_RETRIEVAL_DEADLINE_HOURS = 24  # FDA record request must be fulfilled in 24 hours

# ── Food Safety Plan required elements (21 CFR §117.126) ─────────────────────

HARPC_FOOD_SAFETY_PLAN_REQUIRED_ELEMENTS: FrozenSet[str] = frozenset({
    "written_hazard_analysis",
    "written_preventive_controls",       # for each identified significant hazard
    "written_supply_chain_program",      # if supply chain applied as a control
    "written_recall_plan",
    "monitoring_procedures",
    "corrective_action_procedures",
    "verification_procedures",
    "validation_records",                # for process preventive controls
})

# ── Hazard analysis required categories (21 CFR §117.130) ─────────────────────
# Written hazard analysis must consider all of these categories

HARPC_HAZARD_CATEGORIES_REQUIRED: FrozenSet[str] = frozenset({
    "biological_hazards",               # pathogens
    "chemical_hazards",                 # including radiological
    "physical_hazards",                 # foreign objects
    "economically_motivated_adulteration",  # EMA — new vs. traditional HACCP
    "naturally_occurring_hazards",
    "intentionally_introduced_hazards", # food defense
})

# ── Preventive control types (21 CFR §117.135) ────────────────────────────────

HARPC_PREVENTIVE_CONTROL_TYPES: FrozenSet[str] = frozenset({
    "process_controls",
    "food_allergen_controls",
    "sanitation_controls",
    "supply_chain_controls",
})

# ── Major food allergens (FALCPA as amended by FASTER Act 2021) ───────────────

FSMA_MAJOR_ALLERGENS: FrozenSet[str] = frozenset({
    "milk", "eggs", "fish", "shellfish", "tree_nuts",
    "wheat", "peanuts", "soybeans", "sesame",  # sesame added Jan 1 2023
})

# ── Enhanced Traceability — Critical Tracking Events ──────────────────────────

FTL_CRITICAL_TRACKING_EVENTS: FrozenSet[str] = frozenset({
    "harvesting",
    "cooling",
    "initial_packing",
    "first_land_based_receiving",   # seafood
    "transformation",
    "creation",
    "shipping",
    "receiving",
})

# ── Training record retention (21 CFR §117.4) ────────────────────────────────

FSMA_TRAINING_RECORD_RETENTION_AFTER_DEPARTURE_YEARS = 2
```

---

## TestFoodSafetyPlanElements

```python
class TestFoodSafetyPlanElements:
    """21 CFR §117.126 — Food Safety Plan required written elements."""

    def test_food_safety_plan_exists_and_is_written(self, entity_profile: dict):
        """§117.126(a): Food Safety Plan must exist in written form."""
        fsp = entity_profile.get("food_safety_plan", {})
        assert fsp.get("exists") is True, \
            "No Food Safety Plan found — 21 CFR §117.126 requires a written FSP"
        assert fsp.get("written_format") is True, \
            "Food Safety Plan must be in written (paper or electronic) form"

    def test_food_safety_plan_required_elements_present(self, entity_profile: dict):
        """§117.126(b): All 8 required Food Safety Plan elements must be documented."""
        fsp_elements = frozenset(entity_profile.get("food_safety_plan_elements", []))
        missing = HARPC_FOOD_SAFETY_PLAN_REQUIRED_ELEMENTS - fsp_elements
        assert not missing, (
            f"Food Safety Plan missing required elements: {sorted(missing)} — "
            f"21 CFR §117.126 requires all of: "
            f"{sorted(HARPC_FOOD_SAFETY_PLAN_REQUIRED_ELEMENTS)}"
        )

    def test_qualified_individual_prepared_or_reviewed_fsp(self, entity_profile: dict):
        """§117.126(c): FSP must be prepared by or under oversight of a preventive controls
        qualified individual (PCQI)."""
        fsp = entity_profile.get("food_safety_plan", {})
        assert fsp.get("pcqi_prepared_or_reviewed") is True, \
            "Food Safety Plan must be prepared or reviewed by a PCQI — 21 CFR §117.126(c)"

    def test_food_safety_plan_reanalysis_trigger(self, entity_profile: dict):
        """§117.170: FSP must be reanalyzed at least every 3 years and upon triggers."""
        fsp = entity_profile.get("food_safety_plan", {})
        last_reanalysis = fsp.get("last_reanalysis_date")
        assert last_reanalysis is not None, \
            "No FSP reanalysis date recorded — 21 CFR §117.170 requires periodic reanalysis"
        three_years_ago = date.today() - relativedelta(years=3)
        assert last_reanalysis >= three_years_ago, (
            f"Food Safety Plan reanalysis overdue: last reanalysis {last_reanalysis}, "
            f"must be within 3 years — 21 CFR §117.170"
        )
```

---

## TestHazardAnalysis

```python
class TestHazardAnalysis:
    """21 CFR §117.130 — Written hazard analysis scope."""

    def test_hazard_analysis_exists_and_is_written(self, entity_profile: dict):
        """§117.130(a)(1): Written hazard analysis required."""
        assert entity_profile.get("hazard_analysis", {}).get("written") is True, \
            "No written hazard analysis found — 21 CFR §117.130 is mandatory"

    def test_hazard_categories_all_considered(self, entity_profile: dict):
        """§117.130(b)(1): Hazard analysis must consider known or reasonably foreseeable
        hazards from all required categories."""
        considered = frozenset(entity_profile.get("hazard_categories_considered", []))
        missing = HARPC_HAZARD_CATEGORIES_REQUIRED - considered
        assert not missing, (
            f"Hazard analysis did not consider required categories: {sorted(missing)} — "
            f"21 CFR §117.130(b)(1) requires all hazard categories to be evaluated"
        )

    @pytest.mark.assumption(
        id="ASSUME-FSMA-HARPC-001",
        text="Significant hazard determination is based on severity × likelihood assessment; "
             "'reasonably foreseeable' scope interpreted per facility type and processing history.",
        confidence="PARAMETERIZED",
        approved_by=None,
    )
    def test_significant_hazards_identified(self, entity_profile: dict):
        """§117.130(b)(2): Significant hazards requiring preventive controls must be identified."""
        ha = entity_profile.get("hazard_analysis", {})
        assert ha.get("significant_hazard_determination_documented") is True, \
            "Significant hazard determination not documented — 21 CFR §117.130(b)(2)"
```

---

## TestPreventiveControls

```python
class TestPreventiveControls:
    """21 CFR §117.135 — Preventive controls for significant hazards."""

    def test_allergen_controls_documented(self, entity_profile: dict):
        """§117.135(c)(2): Food allergen controls must be documented if the facility handles
        major food allergens. Documentation requirement is DETERMINISTIC."""
        if not entity_profile.get("handles_major_allergens", False):
            pytest.skip("Facility does not handle major food allergens — allergen controls not required")
        pc = entity_profile.get("preventive_controls", {})
        assert pc.get("allergen_controls_documented") is True, \
            "Allergen preventive controls must be documented — 21 CFR §117.135(c)(2)"

    def test_allergen_program_prevents_cross_contact(self, entity_profile: dict):
        """§117.135(c)(2): Allergen program must address cross-contact prevention."""
        if not entity_profile.get("handles_major_allergens", False):
            pytest.skip("Facility does not handle major food allergens")
        allergen_pc = entity_profile.get("allergen_preventive_controls", {})
        assert allergen_pc.get("cross_contact_prevention_addressed") is True, \
            "Allergen preventive controls must address cross-contact prevention"

    def test_recall_plan_is_written(self, entity_profile: dict):
        """§117.139: Written recall plan required for all facilities with preventive controls."""
        assert entity_profile.get("recall_plan", {}).get("exists_and_written") is True, \
            "Written recall plan required — 21 CFR §117.139"

    @pytest.mark.assumption(
        id="ASSUME-FSMA-HARPC-002",
        text="Process control critical limits (e.g., cooking temperature, pH, water activity) "
             "are facility-specific based on validated hazard control; values accepted as "
             "documented in facility's Food Safety Plan without prescribing specific numbers.",
        confidence="PARAMETERIZED",
        approved_by=None,
    )
    def test_process_controls_have_critical_parameters(self, entity_profile: dict):
        """§117.135(c)(1): Process preventive controls must have defined monitoring
        parameters and critical limits."""
        for control in entity_profile.get("process_preventive_controls", []):
            assert control.get("critical_parameters_defined") is True, (
                f"Process preventive control '{control.get('name', 'unknown')}' "
                f"lacks defined critical parameters — 21 CFR §117.135(c)(1)"
            )
```

---

## TestMonitoringAndVerification

```python
class TestMonitoringAndVerification:
    """21 CFR §§117.145–117.165 — Monitoring, corrective actions, verification."""

    def test_monitoring_procedures_exist_for_each_control(self, entity_profile: dict):
        """§117.145: Monitoring procedures required for each preventive control."""
        controls = entity_profile.get("all_preventive_controls", [])
        for control in controls:
            assert control.get("monitoring_procedure_documented") is True, (
                f"No monitoring procedure for preventive control '{control.get('name', 'unknown')}' "
                f"— 21 CFR §117.145"
            )

    def test_corrective_action_procedures_documented(self, entity_profile: dict):
        """§117.150: Written corrective action procedures required."""
        assert entity_profile.get("corrective_action_procedures_documented") is True, \
            "Corrective action procedures must be documented — 21 CFR §117.150"

    def test_verification_activities_scheduled(self, entity_profile: dict):
        """§117.165: Verification activities must be scheduled and documented."""
        assert entity_profile.get("verification_procedures_documented") is True, \
            "Verification procedures must be documented — 21 CFR §117.165"

    def test_validation_performed_for_process_controls(self, entity_profile: dict):
        """§117.160: Process preventive controls must be validated (evidence that
        control measures, when properly implemented, will effectively control the hazard)."""
        for control in entity_profile.get("process_preventive_controls", []):
            assert control.get("validation_documented") is True, (
                f"Process preventive control '{control.get('name', 'unknown')}' "
                f"lacks validation record — 21 CFR §117.160"
            )
```

---

## TestRecordRetention

```python
class TestRecordRetention:
    """21 CFR §117.305 — 2-year record retention for all HARPC records."""

    RECORD_CATEGORIES = [
        "food_safety_plan",
        "monitoring_records",
        "corrective_action_records",
        "verification_records",
        "training_records",
        "supply_chain_records",
    ]

    def test_all_harpc_record_categories_retained(self, entity_profile: dict):
        """§117.305: All HARPC record categories must be retained for a minimum of 2 years."""
        records = entity_profile.get("harpc_records", {})
        for category in self.RECORD_CATEGORIES:
            assert category in records, \
                f"HARPC record category '{category}' not found — 21 CFR §117.305"
            assert records[category].get("retention_years", 0) >= FSMA_RECORD_RETENTION_YEARS, (
                f"'{category}' retention period {records[category].get('retention_years')} years "
                f"is less than the 2-year minimum — 21 CFR §117.305"
            )

    def test_records_accessible_at_or_near_facility(self, entity_profile: dict):
        """§117.305(c): Records must be kept at or associated with the facility during the
        retention period and be accessible for FDA inspection."""
        assert entity_profile.get("harpc_records_accessible_on_site") is True, \
            "HARPC records must be accessible at or associated with the facility — 21 CFR §117.305(c)"

    def test_training_records_retained_after_employee_departure(self, entity_profile: dict):
        """§117.4(b)(2): Training records must be retained for 2 years after the employee
        leaves the facility."""
        for record in entity_profile.get("departed_employee_training_records", []):
            departure = record.get("departure_date")
            if departure is None:
                continue
            retention_end = departure + relativedelta(years=FSMA_TRAINING_RECORD_RETENTION_AFTER_DEPARTURE_YEARS)
            if date.today() < retention_end:
                assert record.get("retained") is True, (
                    f"Training record for departed employee (departed {departure}) must be "
                    f"retained until {retention_end} — 21 CFR §117.4(b)(2)"
                )
```

---

## TestEnhancedTraceability

```python
class TestEnhancedTraceability:
    """21 CFR Part 204 — Enhanced Traceability (Food Traceability List foods)."""

    def test_traceability_lot_codes_assigned(self, ftl_scope, entity_profile: dict):
        """§204.170: Traceability Lot Codes (TLCs) must be assigned for FTL foods
        at initial packing or first land-based receiving."""
        batches = entity_profile.get("ftl_food_batches", [])
        assert batches, "No FTL food batches found in entity profile"
        for batch in batches:
            assert batch.get("traceability_lot_code") is not None, (
                f"Batch '{batch.get('id', 'unknown')}' of FTL food "
                f"'{batch.get('food_type', 'unknown')}' has no Traceability Lot Code — "
                f"21 CFR §204.170"
            )

    def test_key_data_elements_captured_at_each_cte(self, ftl_scope, entity_profile: dict):
        """§204.210: Key Data Elements (KDEs) must be captured at each Critical Tracking Event."""
        events = entity_profile.get("critical_tracking_events", [])
        for event in events:
            event_type = event.get("event_type")
            assert event_type in FTL_CRITICAL_TRACKING_EVENTS, (
                f"Unknown CTE type '{event_type}'; valid types: {sorted(FTL_CRITICAL_TRACKING_EVENTS)}"
            )
            assert event.get("key_data_elements_captured") is True, (
                f"Key Data Elements not captured at {event_type} event "
                f"for batch '{event.get('tlc', 'unknown')}' — 21 CFR §204.210"
            )

    def test_traceability_records_retrievable_within_24_hours(self, ftl_scope, entity_profile: dict):
        """§204.210: Records must be available to FDA within 24 hours of request."""
        retrieval = entity_profile.get("traceability_record_retrieval", {})
        assert retrieval.get("max_retrieval_hours", float("inf")) <= FSMA_FTL_RETRIEVAL_DEADLINE_HOURS, (
            f"Maximum traceability record retrieval time {retrieval.get('max_retrieval_hours')} hours "
            f"exceeds the 24-hour FDA requirement — 21 CFR §204.210"
        )

    def test_traceability_records_cover_required_cte_types(self, ftl_scope, entity_profile: dict):
        """§204.210: Records must span all applicable CTEs in the facility's supply chain role."""
        facility_ctes = frozenset(entity_profile.get("applicable_cte_types", []))
        captured_ctes = frozenset(entity_profile.get("ctes_with_captured_records", []))
        missing = facility_ctes - captured_ctes
        assert not missing, (
            f"Traceability records missing for applicable CTEs: {sorted(missing)} — "
            f"21 CFR §204.210 requires KDE capture at all applicable CTEs"
        )
```

---

## TestFSVP

```python
class TestFSVP:
    """21 CFR Part 1 Subpart L — Foreign Supplier Verification Program."""

    def test_fsvp_importer_designated(self, fsvp_scope, entity_profile: dict):
        """§1.500: Single US importer of record must be designated as FSVP importer."""
        assert entity_profile.get("fsvp_importer_designated") is True, \
            "No FSVP importer designated — 21 CFR §1.500 requires the US importer of record"

    def test_hazard_analysis_conducted_for_each_imported_food(self, fsvp_scope, entity_profile: dict):
        """§1.504: Written hazard analysis required for each food imported."""
        imported_foods = entity_profile.get("imported_food_products", [])
        assert imported_foods, "No imported food products found in entity profile"
        for food in imported_foods:
            assert food.get("hazard_analysis_conducted") is True, (
                f"No hazard analysis for imported food '{food.get('name', 'unknown')}' "
                f"from supplier '{food.get('supplier', 'unknown')}' — 21 CFR §1.504"
            )

    def test_supplier_verification_activities_performed(self, fsvp_scope, entity_profile: dict):
        """§1.506: Supplier verification activities must be conducted based on hazard analysis."""
        for food in entity_profile.get("imported_food_products", []):
            assert food.get("supplier_verification_activity_type") is not None, (
                f"No supplier verification activity defined for "
                f"'{food.get('name', 'unknown')}' — 21 CFR §1.506"
            )

    def test_fsvp_records_maintained(self, fsvp_scope, entity_profile: dict):
        """§1.512: FSVP records must be maintained at US importer's principal office
        or US port of entry for at least 2 years."""
        fsvp = entity_profile.get("fsvp_records", {})
        assert fsvp.get("location_is_us_office_or_port") is True, \
            "FSVP records must be at US principal office or port of entry — 21 CFR §1.512"
        assert fsvp.get("retention_years", 0) >= FSMA_RECORD_RETENTION_YEARS, (
            f"FSVP record retention {fsvp.get('retention_years')} years is less than "
            f"the 2-year minimum — 21 CFR §1.512"
        )

    @pytest.mark.assumption(
        id="ASSUME-FSMA-FSVP-001",
        text="Supplier verification activity type (on-site audit vs. sampling/testing vs. "
             "record review) is selected based on the hazard analysis and supplier's compliance "
             "history; the specific verification type is parameterized per supplier and food.",
        confidence="PARAMETERIZED",
        approved_by=None,
    )
    def test_high_hazard_suppliers_subject_to_on_site_audit(self, fsvp_scope, entity_profile: dict):
        """§1.506(d): For serious hazards without adequate preventive controls at importer,
        annual on-site audit of supplier required."""
        for food in entity_profile.get("imported_food_products", []):
            if food.get("serious_hazard_no_importer_control") is True:
                assert food.get("annual_onsite_audit_conducted") is True, (
                    f"Food '{food.get('name', 'unknown')}' has serious hazard with no "
                    f"importer-side control — annual on-site supplier audit required (§1.506(d))"
                )
```
