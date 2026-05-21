# RoHS 3 / REACH — EU Chemical Restriction Compliance

**Framework:** RoHS 3 (Directive 2011/65/EU as amended by 2015/863/EU) + REACH (Regulation (EC) No 1907/2006)
**Clauses:** RoHS Art. 4 (substance restrictions), Art. 7 (CE marking), Art. 8 (technical documentation), Annex II (substance thresholds); REACH Art. 6/7 (registration), Art. 31/33 (SVHC communication), Art. 56 (authorization), Annex XIV (authorized substances)
**Confidence:** DETERMINISTIC throughout — substance thresholds are bright-line; documentation requirements are enumerable; sunset dates are calendar-based
**Last parsed:** 2026-05-21
**Applies to:** RoHS: manufacturers, importers, and distributors placing electrical and electronic equipment (EEE) on the EU market. REACH: any company that manufactures, imports, or uses chemical substances in the EU above threshold quantities, or places articles containing SVHCs on the EU market
**Trigger:** RoHS: placing EEE on the EU market — applies to virtually all consumer and industrial electronics sold in the EU. REACH: manufacturing/importing ≥ 1 tonne/year of a substance in the EU; supplying articles containing SVHCs > 0.1% by weight
**Jurisdiction:** European Union; extraterritorial for non-EU manufacturers — products must comply before entering EU market; enforced by national market surveillance authorities
**Not applicable to:** RoHS: military/defense equipment (Art. 2(3)(b)); large fixed industrial installations; implantable active medical devices; space equipment; some specific product categories in Annex II. REACH: substances used solely in national defense; radioactive substances (Euratom); certain polymers (registration exemption); waste (regulated separately under WFD)

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def rohs_reach_scope(entity_profile: dict):
    in_scope = (
        entity_profile.get("rohs_in_scope", False)
        or entity_profile.get("reach_in_scope", False)
    )
    if not in_scope:
        pytest.skip("RoHS/REACH not in scope")
```

---

## Constants

```python
from datetime import date, timedelta

# RoHS Annex II — restricted substances and maximum concentration values (% w/w in homogeneous material)
ROHS_RESTRICTED_SUBSTANCES_MCV = {
    "lead_pb":                                   0.10,
    "mercury_hg":                                0.10,
    "cadmium_cd":                                0.01,
    "hexavalent_chromium_cr6":                   0.10,
    "polybrominated_biphenyls_pbb":              0.10,
    "polybrominated_diphenyl_ethers_pbde":       0.10,
    "bis_2_ethylhexyl_phthalate_dehp":           0.10,
    "benzyl_butyl_phthalate_bbp":                0.10,
    "dibutyl_phthalate_dbp":                     0.10,
    "diisobutyl_phthalate_dibp":                 0.10,
}

# RoHS compliance documentation required elements
ROHS_COMPLIANCE_DOCUMENTATION_REQUIRED = frozenset({
    "technical_documentation_or_material_declarations",
    "eu_declaration_of_conformity",
    "ce_marking_applied_to_product_or_packaging",
})

# Non-EU manufacturers must also have:
ROHS_NON_EU_MANUFACTURER_ADDITIONAL_REQUIRED = frozenset({
    "authorised_representative_eu_designated",
})

# REACH thresholds
REACH_SVHC_ARTICLE_THRESHOLD_PERCENT = 0.1    # >0.1% w/w in article triggers disclosure
REACH_SVHC_ECHA_NOTIFICATION_THRESHOLD_TONNES = 1.0  # >1 t/year placed on market triggers ECHA notification
REACH_REGISTRATION_THRESHOLD_TONNES = 1.0     # ≥1 t/year substance manufactured/imported

# SVHC candidate list update interval — ECHA updates twice per year
# Systems must be re-checked within this window after each update
REACH_SVHC_LIST_RECHECK_MONTHS = 6

# REACH authorization sunset: use of Annex XIV substance after its sunset date without authorization = non-compliance
```

---

## RoHS — Substance Threshold Compliance (Art. 4 + Annex II)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestRoHSSubstanceThresholds:
    """RoHS Art. 4 + Annex II — All 10 restricted substances below MCV in every homogeneous material."""

    @pytest.fixture(autouse=True)
    def rohs_scope(self, entity_profile: dict):
        if not entity_profile.get("rohs_in_scope", False):
            pytest.skip("RoHS not in scope")

    def test_all_rohs_substances_below_mcv_in_homogeneous_materials(
        self, controls_evidence: dict
    ):
        materials = controls_evidence.get("rohs_homogeneous_materials", [])
        for material in materials:
            substance_data = material.get("substance_concentrations_percent_ww", {})
            for substance, mcv in ROHS_RESTRICTED_SUBSTANCES_MCV.items():
                measured = substance_data.get(substance)
                if measured is None:
                    continue
                assert measured <= mcv, (
                    f"Material '{material['material_id']}': substance '{substance}' "
                    f"concentration {measured}% w/w exceeds RoHS MCV of {mcv}% w/w "
                    f"(RoHS Directive 2011/65/EU Annex II)"
                )

    def test_rohs_substance_test_data_or_material_declarations_available(
        self, controls_evidence: dict
    ):
        products = controls_evidence.get("rohs_products", [])
        no_data = [
            p for p in products
            if not p.get("substance_test_data_or_declaration_available", False)
        ]
        assert not no_data, (
            f"Test reports or material declarations (per IEC 62474 or equivalent) "
            f"must be available for all EEE placed on the EU market. "
            f"Missing: {[p['product_id'] for p in no_data]} "
            f"(RoHS Art. 7 + 8)"
        )
```

---

## RoHS — Exemption Management (Art. 5 + Annex III/IV)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestRoHSExemptionManagement:
    """RoHS Art. 5 — Exemptions claimed are numbered, valid (not expired), and applicable to the product category."""

    @pytest.fixture(autouse=True)
    def rohs_scope(self, entity_profile: dict):
        if not entity_profile.get("rohs_in_scope", False):
            pytest.skip("RoHS not in scope")

    def test_all_claimed_exemptions_are_valid(
        self, controls_evidence: dict, reference_date: date
    ):
        exemptions = controls_evidence.get("rohs_claimed_exemptions", [])
        for exemption in exemptions:
            expiry = exemption.get("exemption_expiry_date")
            assert expiry is None or expiry >= reference_date, (
                f"RoHS exemption '{exemption['exemption_number']}' claimed for product "
                f"'{exemption['product_id']}' has expired. Expiry: {expiry} "
                f"(RoHS Art. 5 — exemptions must be renewed before expiry)"
            )

    def test_claimed_exemptions_are_applicable_to_product_category(
        self, controls_evidence: dict
    ):
        exemptions = controls_evidence.get("rohs_claimed_exemptions", [])
        not_applicable = [
            e for e in exemptions
            if not e.get("exemption_applicable_to_product_category", False)
        ]
        assert not not_applicable, (
            f"RoHS exemptions claimed must be applicable to the product category "
            f"(Annex III for EEE; Annex IV for medical devices and monitoring). "
            f"Inapplicable: {[e['exemption_number'] for e in not_applicable]} "
            f"(RoHS Art. 5)"
        )
```

---

## RoHS — EU Declaration of Conformity and CE Marking (Art. 7 + 13)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestRoHSDeclarationAndCEMarking:
    """RoHS Art. 7/13 — EU DoC with required elements; CE marking on product or packaging; authorised rep for non-EU manufacturers."""

    @pytest.fixture(autouse=True)
    def rohs_scope(self, entity_profile: dict):
        if not entity_profile.get("rohs_in_scope", False):
            pytest.skip("RoHS not in scope")

    def test_eu_declaration_of_conformity_exists_for_all_eee(
        self, controls_evidence: dict
    ):
        products = controls_evidence.get("rohs_products", [])
        no_doc = [
            p for p in products
            if not p.get("eu_declaration_of_conformity_exists", False)
        ]
        assert not no_doc, (
            f"An EU Declaration of Conformity (DoC) must exist for all EEE placed on "
            f"the EU market. Missing: {[p['product_id'] for p in no_doc]} "
            f"(RoHS Art. 7(1))"
        )

    def test_ce_marking_applied_to_all_eee(self, controls_evidence: dict):
        products = controls_evidence.get("rohs_products", [])
        no_ce = [
            p for p in products
            if not p.get("ce_marking_applied", False)
        ]
        assert not no_ce, (
            f"CE marking must be affixed to all EEE before placing on the EU market. "
            f"Missing: {[p['product_id'] for p in no_ce]} (RoHS Art. 13)"
        )

    def test_non_eu_manufacturers_have_authorised_representative(
        self, controls_evidence: dict, entity_profile: dict
    ):
        if entity_profile.get("manufacturer_established_in_eu", True):
            return
        rohs = controls_evidence.get("rohs_compliance", {})
        assert rohs.get("authorised_representative_eu_designated", False), (
            "Non-EU manufacturers must designate an authorised representative "
            "established in the EU before placing EEE on the EU market "
            "(RoHS Art. 8)"
        )
```

---

## REACH — SVHC Identification and Customer Notification (Art. 33)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestREACHSVHCNotification:
    """REACH Art. 33 — SVHCs >0.1% w/w in article disclosed to customers and consumers on request."""

    @pytest.fixture(autouse=True)
    def reach_scope(self, entity_profile: dict):
        if not entity_profile.get("reach_in_scope", False):
            pytest.skip("REACH not in scope")

    def test_svhc_screening_against_candidate_list_conducted(
        self, controls_evidence: dict, reference_date: date
    ):
        reach = controls_evidence.get("reach_compliance", {})
        last_svhc_check = reach.get("svhc_candidate_list_last_checked")
        assert last_svhc_check is not None, (
            "Products must be screened against the ECHA SVHC Candidate List. "
            "No screening date recorded (REACH Art. 33)"
        )
        cutoff = reference_date - timedelta(days=REACH_SVHC_LIST_RECHECK_MONTHS * 30)
        assert last_svhc_check >= cutoff, (
            f"SVHC candidate list check must be repeated after each ECHA update "
            f"(biannual). Last checked: {last_svhc_check} "
            f"(REACH Art. 33)"
        )

    def test_svhc_above_threshold_disclosed_to_customers(
        self, controls_evidence: dict
    ):
        articles = controls_evidence.get("reach_articles", [])
        svhc_articles = [
            a for a in articles
            if a.get("svhc_concentration_percent_ww", 0) > REACH_SVHC_ARTICLE_THRESHOLD_PERCENT
        ]
        not_disclosed = [
            a for a in svhc_articles
            if not a.get("svhc_disclosed_to_customers", False)
        ]
        assert not not_disclosed, (
            f"SVHCs present above {REACH_SVHC_ARTICLE_THRESHOLD_PERCENT}% w/w in an "
            f"article must be communicated to customers 'sufficient to allow safe use' "
            f"(REACH Art. 33(1)). Not disclosed: "
            f"{[a['article_id'] for a in not_disclosed]}"
        )

    def test_svhc_above_threshold_disclosed_to_consumers_on_request(
        self, controls_evidence: dict
    ):
        reach = controls_evidence.get("reach_compliance", {})
        articles = controls_evidence.get("reach_articles", [])
        has_svhc_articles = any(
            a.get("svhc_concentration_percent_ww", 0) > REACH_SVHC_ARTICLE_THRESHOLD_PERCENT
            for a in articles
        )
        if not has_svhc_articles:
            return
        assert reach.get("svhc_consumer_disclosure_process_in_place", False), (
            "A process must exist to disclose SVHC presence to consumers within 45 days "
            "of request (REACH Art. 33(2))"
        )
```

---

## REACH — SVHC Article Notification to ECHA (Art. 7(2))

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestREACHSVHCECHANotification:
    """REACH Art. 7(2) — SVHC in articles >0.1% w/w AND >1 tonne/year notified to ECHA."""

    @pytest.fixture(autouse=True)
    def reach_scope(self, entity_profile: dict):
        if not entity_profile.get("reach_in_scope", False):
            pytest.skip("REACH not in scope")

    def test_svhc_echa_notification_made_when_thresholds_met(
        self, controls_evidence: dict
    ):
        articles = controls_evidence.get("reach_articles", [])
        notification_required = [
            a for a in articles
            if a.get("svhc_concentration_percent_ww", 0) > REACH_SVHC_ARTICLE_THRESHOLD_PERCENT
            and a.get("annual_volume_tonnes", 0) > REACH_SVHC_ECHA_NOTIFICATION_THRESHOLD_TONNES
        ]
        not_notified = [
            a for a in notification_required
            if not a.get("svhc_echa_notification_made", False)
        ]
        assert not not_notified, (
            f"SVHC present >0.1% w/w in articles placed on market in quantities "
            f">1 tonne/year must be notified to ECHA (REACH Art. 7(2)). "
            f"Not notified: {[a['article_id'] for a in not_notified]}"
        )
```

---

## REACH — Substance Registration (Art. 6)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestREACHSubstanceRegistration:
    """REACH Art. 6 — Substances manufactured or imported ≥1 tonne/year must be registered with ECHA; registration number current."""

    @pytest.fixture(autouse=True)
    def reach_scope(self, entity_profile: dict):
        if not entity_profile.get("reach_in_scope", False):
            pytest.skip("REACH not in scope")

    def test_all_registrable_substances_have_current_registration(
        self, controls_evidence: dict
    ):
        substances = controls_evidence.get("reach_substances", [])
        registrable = [
            s for s in substances
            if s.get("annual_volume_tonnes", 0) >= REACH_REGISTRATION_THRESHOLD_TONNES
            and not s.get("registration_exempt", False)
        ]
        not_registered = [
            s for s in registrable
            if not s.get("echa_registration_number_current", False)
        ]
        assert not not_registered, (
            f"Substances manufactured or imported ≥{REACH_REGISTRATION_THRESHOLD_TONNES} "
            f"tonne/year must be registered with ECHA before being placed on the market "
            f"(REACH Art. 6). Not registered: "
            f"{[s['substance_id'] for s in not_registered]}"
        )
```

---

## REACH — Authorized Substance Sunset Date Compliance (Art. 56 + Annex XIV)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestREACHAuthorizationSunsetDates:
    """REACH Art. 56 — No Annex XIV substances used after their sunset date without a valid authorization."""

    @pytest.fixture(autouse=True)
    def reach_scope(self, entity_profile: dict):
        if not entity_profile.get("reach_in_scope", False):
            pytest.skip("REACH not in scope")

    def test_no_annex_xiv_substance_used_after_sunset_without_authorization(
        self, controls_evidence: dict, reference_date: date
    ):
        substances = controls_evidence.get("reach_annex_xiv_substances", [])
        for substance in substances:
            sunset_date = substance.get("sunset_date")
            has_authorization = substance.get("reach_authorization_granted", False)
            if sunset_date and reference_date > sunset_date and not has_authorization:
                assert False, (
                    f"Substance '{substance['substance_id']}' (Annex XIV) has passed its "
                    f"sunset date ({sunset_date}) and is being used without a valid REACH "
                    f"authorization. Use after sunset date without authorization is prohibited "
                    f"(REACH Art. 56)"
                )
```

---

## Supply Chain Material Declarations

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestSupplyChainMaterialDeclarations:
    """RoHS/REACH — Supplier material declarations collected for all substance-impacting components."""

    def test_material_declarations_collected_from_all_applicable_suppliers(
        self, controls_evidence: dict
    ):
        suppliers = controls_evidence.get("rohs_reach_suppliers", [])
        no_declaration = [
            s for s in suppliers
            if s.get("supplies_eee_components", False)
            and not s.get("material_declaration_on_file", False)
        ]
        assert not no_declaration, (
            f"Material declarations (IEC 62474 or equivalent RoHS/REACH declarations) "
            f"must be obtained from all suppliers of EEE components. Missing: "
            f"{[s['supplier_id'] for s in no_declaration]} "
            f"(RoHS Art. 4 + REACH Art. 33 supply chain obligations)"
        )

    def test_material_declarations_reviewed_for_currency(
        self, controls_evidence: dict, reference_date: date
    ):
        suppliers = controls_evidence.get("rohs_reach_suppliers", [])
        stale_declarations = [
            s for s in suppliers
            if s.get("material_declaration_on_file", False)
            and s.get("declaration_date") is not None
            and s["declaration_date"] < reference_date.replace(year=reference_date.year - 3)
        ]
        assert not stale_declarations, (
            f"Material declarations older than 3 years should be re-requested, "
            f"especially after ECHA SVHC list updates. Stale declarations: "
            f"{[s['supplier_id'] for s in stale_declarations]}"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|

*(No open assumptions — RoHS substance thresholds, REACH notification thresholds, and sunset dates are all bright-line DETERMINISTIC criteria)*
