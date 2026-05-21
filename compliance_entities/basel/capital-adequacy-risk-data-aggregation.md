# Basel III / BCBS 239 — Capital Adequacy and Risk Data Aggregation

**Framework:** Basel III (CRD IV / CRR + Basel IV finalization effective 2025) + BCBS 239 (Principles for Effective Risk Data Aggregation and Risk Reporting, January 2013)
**Clauses:** Basel III Pillar 1 (minimum capital ratios CET1/Tier1/Total/Leverage); Pillar 2 (ICAAP); Pillar 3 (disclosure — quarterly 45-day deadline); LCR Disclosure Standards (monthly 15-business-day); BCBS 239 Principles 1–14 (P5/P10 DETERMINISTIC; remainder PARAMETERIZED); NSFR (100% minimum)
**Confidence:** DETERMINISTIC (capital ratio thresholds; LCR/NSFR minimums; Pillar 3 publication deadlines; BCBS 239 P5 timeliness; BCBS 239 P10 board reporting quarterly); PARAMETERIZED-dominant (ICAAP, model validation, BCBS 239 data architecture adequacy, stress testing)
**Last parsed:** 2026-05-21

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def basel_scope(entity_profile: dict):
    if not entity_profile.get("internationally_active_bank_or_gsib", False):
        pytest.skip("Basel III / BCBS 239 not applicable — not an internationally active bank or G-SIB")

@pytest.fixture
def gsib_scope(entity_profile: dict):
    """Additional fixture for G-SIB-only requirements (BCBS 239, G-SIB surcharge)."""
    if not entity_profile.get("gsib", False):
        pytest.skip("G-SIB-only requirement — not on FSB G-SIB list")
```

---

## Constants

```python
from datetime import date, timedelta
from decimal import Decimal

# Basel III — minimum capital ratios (Pillar 1)
BASEL3_CET1_MINIMUM_PCT = Decimal("4.5")
BASEL3_CET1_WITH_CONSERVATION_BUFFER_PCT = Decimal("7.0")
BASEL3_TIER1_MINIMUM_PCT = Decimal("6.0")
BASEL3_TIER1_WITH_CONSERVATION_BUFFER_PCT = Decimal("8.5")
BASEL3_TOTAL_CAPITAL_MINIMUM_PCT = Decimal("8.0")
BASEL3_TOTAL_CAPITAL_WITH_BUFFER_PCT = Decimal("10.5")
BASEL3_LEVERAGE_RATIO_MINIMUM_PCT = Decimal("3.0")

# Liquidity requirements
BASEL3_LCR_MINIMUM_PCT = Decimal("100")
BASEL3_NSFR_MINIMUM_PCT = Decimal("100")

# Pillar 3 disclosure deadlines
BASEL3_PILLAR3_QUARTERLY_DISCLOSURE_DAYS = 45     # days after quarter-end
BASEL3_LCR_DISCLOSURE_BUSINESS_DAYS = 15           # business days after month-end
BASEL3_PILLAR3_ANNUAL_WITH_FINANCIAL_STATEMENTS = True

# BCBS 239 reporting frequency
BCBS239_BOARD_RISK_REPORTING_MIN_FREQUENCY = "quarterly"
```

---

## Capital Adequacy Ratios (Basel III Pillar 1)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestCapitalAdequacyRatios:
    """Basel III Pillar 1 — CET1 ≥ 4.5%; Tier 1 ≥ 6%; Total Capital ≥ 8%; conservation buffer maintained."""

    def test_cet1_ratio_meets_minimum(self, controls_evidence: dict):
        basel = controls_evidence.get("basel3", {})
        cet1 = controls_evidence.get("capital_ratios", {}).get("cet1_ratio_pct")
        if cet1 is None:
            return
        assert Decimal(str(cet1)) >= BASEL3_CET1_MINIMUM_PCT, (
            f"CET1 ratio {cet1}% is below the {BASEL3_CET1_MINIMUM_PCT}% minimum. "
            f"Breach triggers automatic Pillar 2 supervisory review "
            f"(Basel III Pillar 1)"
        )

    def test_cet1_with_conservation_buffer(self, controls_evidence: dict):
        cet1 = controls_evidence.get("capital_ratios", {}).get("cet1_ratio_pct")
        if cet1 is None:
            return
        cet1_decimal = Decimal(str(cet1))
        if cet1_decimal < BASEL3_CET1_WITH_CONSERVATION_BUFFER_PCT:
            restrictions = controls_evidence.get("capital_ratios", {}).get(
                "capital_conservation_restrictions_applied", False
            )
            assert restrictions, (
                f"CET1 ratio {cet1}% is below the {BASEL3_CET1_WITH_CONSERVATION_BUFFER_PCT}% "
                f"conservation buffer threshold. Capital distribution restrictions "
                f"(dividends, buybacks, discretionary bonuses) must be applied "
                f"(Basel III Capital Conservation Buffer)"
            )

    def test_tier1_ratio_meets_minimum(self, controls_evidence: dict):
        tier1 = controls_evidence.get("capital_ratios", {}).get("tier1_ratio_pct")
        if tier1 is None:
            return
        assert Decimal(str(tier1)) >= BASEL3_TIER1_MINIMUM_PCT, (
            f"Tier 1 capital ratio {tier1}% is below the {BASEL3_TIER1_MINIMUM_PCT}% minimum "
            f"(Basel III Pillar 1)"
        )

    def test_total_capital_ratio_meets_minimum(self, controls_evidence: dict):
        total = controls_evidence.get("capital_ratios", {}).get("total_capital_ratio_pct")
        if total is None:
            return
        assert Decimal(str(total)) >= BASEL3_TOTAL_CAPITAL_MINIMUM_PCT, (
            f"Total capital ratio {total}% is below the {BASEL3_TOTAL_CAPITAL_MINIMUM_PCT}% minimum "
            f"(Basel III Pillar 1)"
        )

    def test_capital_ratios_calculated_and_reported_on_schedule(
        self, controls_evidence: dict, reference_date: date
    ):
        basel = controls_evidence.get("basel3", {})
        last_calculation = basel.get("capital_ratios_last_calculated")
        assert last_calculation is not None, (
            "Capital ratios must be calculated and documented on a regular schedule; "
            "no calculation date on record"
        )
        # Capital ratios should be calculated at least quarterly
        cutoff = reference_date - timedelta(days=95)
        assert last_calculation >= cutoff, (
            f"Capital ratios must be calculated at least quarterly. "
            f"Last calculated: {last_calculation}"
        )
```

---

## Leverage and Liquidity Ratios (Basel III)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestLeverageAndLiquidityRatios:
    """Basel III — Leverage Ratio ≥ 3%; LCR ≥ 100%; NSFR ≥ 100%."""

    def test_leverage_ratio_meets_minimum(self, controls_evidence: dict):
        leverage = controls_evidence.get("capital_ratios", {}).get("leverage_ratio_pct")
        if leverage is None:
            return
        assert Decimal(str(leverage)) >= BASEL3_LEVERAGE_RATIO_MINIMUM_PCT, (
            f"Leverage ratio (Tier 1 / Total Exposure) {leverage}% is below the "
            f"{BASEL3_LEVERAGE_RATIO_MINIMUM_PCT}% minimum (Basel III Leverage Ratio Framework)"
        )

    def test_lcr_meets_100_percent_minimum(self, controls_evidence: dict):
        lcr = controls_evidence.get("liquidity_ratios", {}).get("lcr_pct")
        if lcr is None:
            return
        assert Decimal(str(lcr)) >= BASEL3_LCR_MINIMUM_PCT, (
            f"Liquidity Coverage Ratio (HQLA / 30-day net cash outflow) {lcr}% "
            f"is below the {BASEL3_LCR_MINIMUM_PCT}% minimum. "
            f"Breach requires immediate supervisory notification "
            f"(Basel III LCR Standard)"
        )

    def test_nsfr_meets_100_percent_minimum(self, controls_evidence: dict):
        nsfr = controls_evidence.get("liquidity_ratios", {}).get("nsfr_pct")
        if nsfr is None:
            return
        assert Decimal(str(nsfr)) >= BASEL3_NSFR_MINIMUM_PCT, (
            f"Net Stable Funding Ratio (ASF / RSF) {nsfr}% is below the "
            f"{BASEL3_NSFR_MINIMUM_PCT}% minimum (Basel III NSFR Standard)"
        )
```

---

## Pillar 3 Public Disclosures (Basel III Pillar 3)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestPillar3Disclosures:
    """Basel III Pillar 3 — Quarterly disclosures within 45 days of quarter-end; LCR disclosure within 15 business days."""

    def test_quarterly_pillar3_disclosures_published_within_45_days(
        self, controls_evidence: dict
    ):
        disclosures = controls_evidence.get("pillar3_disclosures", [])
        late = [
            d for d in disclosures
            if d.get("disclosure_type") == "quarterly"
            and d.get("days_after_quarter_end", 0) > BASEL3_PILLAR3_QUARTERLY_DISCLOSURE_DAYS
        ]
        assert not late, (
            f"Quarterly Pillar 3 disclosures (capital adequacy, RWA, leverage ratio) "
            f"must be published within {BASEL3_PILLAR3_QUARTERLY_DISCLOSURE_DAYS} days "
            f"of quarter-end. Late disclosures: "
            f"{[d['period'] for d in late]} "
            f"(Basel III Pillar 3 Requirements)"
        )

    def test_lcr_disclosure_published_within_15_business_days(
        self, controls_evidence: dict
    ):
        disclosures = controls_evidence.get("pillar3_disclosures", [])
        late_lcr = [
            d for d in disclosures
            if d.get("disclosure_type") == "lcr_monthly"
            and d.get("business_days_after_month_end", 0) > BASEL3_LCR_DISCLOSURE_BUSINESS_DAYS
        ]
        assert not late_lcr, (
            f"Monthly LCR disclosures must be published within "
            f"{BASEL3_LCR_DISCLOSURE_BUSINESS_DAYS} business days of month-end. "
            f"Late: {[d['period'] for d in late_lcr]} "
            f"(Basel III LCR Disclosure Standards)"
        )

    def test_pillar3_disclosures_include_required_templates(
        self, controls_evidence: dict
    ):
        basel = controls_evidence.get("basel3", {})
        assert basel.get("pillar3_disclosures_include_required_templates", False), (
            "Pillar 3 disclosures must include the required standardized templates "
            "(KM1 key metrics, OV1 RWA overview, CC1 capital composition, "
            "LR1 leverage ratio) (Basel III Pillar 3 2018 update)"
        )
```

---

## BCBS 239 — Risk Data Aggregation (G-SIBs)

**Overall: DETERMINISTIC (P5 timeliness, P10 board reporting frequency) + PARAMETERIZED (data architecture adequacy)**

```python
class TestBCBS239DataAggregation:
    """BCBS 239 Principles 3–6 — Risk data accurate, complete, timely, and adaptable; end-of-day delivery as normal mode."""

    @pytest.mark.assumption(
        id="ASSUME-BCBS239-ARCH-001",
        description=(
            "BCBS 239 data architecture adequacy (P1–P4, P6) is supervisory-evaluated: "
            "regulators assess whether integrated data taxonomy, single authoritative "
            "sources, automated reconciliation, and ad-hoc reporting capability "
            "meet the 'accurate and complete' standard; these are PARAMETERIZED "
            "because adequacy depends on data environment complexity and supervisory "
            "judgment; P5 (timeliness: end-of-day normal mode) and P10 (board quarterly) "
            "are DETERMINISTIC binary thresholds"
        ),
        approved_by="chief_risk_officer",
        review_date="2027-05-21",
    )
    def test_risk_data_aggregation_framework_documented(self, controls_evidence: dict):
        bcbs239 = controls_evidence.get("bcbs239", {})
        assert bcbs239.get("risk_data_aggregation_framework_documented", False), (
            "A documented risk data aggregation framework addressing BCBS 239 "
            "Principles 1–14 must exist, with board approval "
            "(BCBS 239 P1)"
        )

    def test_risk_data_delivered_end_of_day_normal_mode(
        self, controls_evidence: dict
    ):
        bcbs239 = controls_evidence.get("bcbs239", {})
        assert bcbs239.get("risk_data_delivered_by_end_of_day_normal_mode", False), (
            "In normal mode, risk data must be aggregated and available by "
            "end-of-business-day — P5 timeliness is a DETERMINISTIC requirement "
            "(BCBS 239 P5)"
        )

    def test_stress_mode_intraday_aggregation_capability_exists(
        self, controls_evidence: dict
    ):
        bcbs239 = controls_evidence.get("bcbs239", {})
        assert bcbs239.get("intraday_aggregation_capability_for_stress_mode", False), (
            "In stress mode, supervisors may require intraday risk data — the "
            "institution must have the capability to produce aggregated risk data "
            "on an intraday basis when required (BCBS 239 P5 + P6)"
        )

    def test_single_authoritative_data_sources_established(
        self, controls_evidence: dict
    ):
        bcbs239 = controls_evidence.get("bcbs239", {})
        assert bcbs239.get("single_authoritative_data_sources_established", False), (
            "Authoritative data sources (golden sources) must be established for "
            "key risk data — conflicting data lineages are a key BCBS 239 finding "
            "(BCBS 239 P2–P3)"
        )
```

---

## BCBS 239 — Risk Reporting Frequency (P10)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestBCBS239RiskReportingFrequency:
    """BCBS 239 P10 — Board-level risk reporting at least quarterly; senior management more frequently."""

    def test_board_receives_risk_reports_at_least_quarterly(
        self, controls_evidence: dict
    ):
        bcbs239 = controls_evidence.get("bcbs239", {})
        assert bcbs239.get("board_receives_risk_reports_quarterly_or_more_frequently", False), (
            "The board of directors must receive risk reports at least quarterly — "
            "this is a DETERMINISTIC requirement under BCBS 239 P10 "
            "(BCBS 239 Principle 10)"
        )

    def test_senior_management_receives_risk_reports_more_frequently(
        self, controls_evidence: dict
    ):
        bcbs239 = controls_evidence.get("bcbs239", {})
        assert bcbs239.get(
            "senior_management_receives_risk_reports_more_frequently_than_board", False
        ), (
            "Senior management must receive risk reports more frequently than "
            "the board — typically monthly or more often for key risk metrics "
            "(BCBS 239 P10)"
        )
```

---

## ICAAP and ILAAP Annual Submission (Basel III Pillar 2)

**Overall: DETERMINISTIC (annual submission) + PARAMETERIZED (adequacy)**

```python
class TestICAAP:
    """Basel III Pillar 2 — ICAAP (and ILAAP) submitted annually to home supervisor; stress testing documented."""

    @pytest.mark.assumption(
        id="ASSUME-BASELI-ICAAP-001",
        description=(
            "ICAAP and ILAAP adequacy (stress scenario selection, capital projection "
            "methodology, internal model validation) is determined by the home "
            "supervisor via SREP — adequacy is PARAMETERIZED/CONTESTED; "
            "the annual submission itself is DETERMINISTIC"
        ),
        approved_by="chief_risk_officer",
        review_date="2027-05-21",
    )
    def test_icaap_submitted_annually(
        self, controls_evidence: dict, reference_date: date
    ):
        basel = controls_evidence.get("basel3", {})
        last_icaap = basel.get("icaap_last_submitted_to_supervisor")
        assert last_icaap is not None, (
            "ICAAP has not been submitted to the home supervisor — "
            "no submission date on record (Basel III Pillar 2)"
        )
        cutoff = reference_date - timedelta(days=366)
        assert last_icaap >= cutoff, (
            f"ICAAP must be submitted annually to the home supervisor. "
            f"Last submitted: {last_icaap} (Basel III Pillar 2)"
        )

    def test_icaap_includes_stress_testing(self, controls_evidence: dict):
        basel = controls_evidence.get("basel3", {})
        assert basel.get("icaap_includes_stress_testing_scenarios", False), (
            "ICAAP must include stress testing across at least one severe but "
            "plausible scenario covering credit, market, and operational risk "
            "(Basel III Pillar 2 / BCBS guidance on stress testing)"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-BCBS239-ARCH-001 | BCBS 239 P1–P4, P6 | Risk data architecture adequacy (single sources, reconciliation, ad-hoc reporting): PARAMETERIZED (supervisory-evaluated); P5 timeliness and P10 frequency: DETERMINISTIC | 2027-05-21 |
| ASSUME-BASELI-ICAAP-001 | Basel III Pillar 2 | ICAAP/ILAAP scenario adequacy: PARAMETERIZED (SREP-determined); annual submission: DETERMINISTIC | 2027-05-21 |
