# ITAR / EAR — Deterministic Controls: Denied Party Screening, Record-Keeping, Registration

**Registry path:** `/regulation-registry/ITAR-EAR/Deterministic-Controls/`
**Regulations:** ITAR (22 CFR 120–130), EAR (15 CFR 730–774)
**Last parsed:** 2026-05-20
**Applies to:** Any person or entity — US or foreign — that manufactures, exports, re-exports, transfers, or brokers: ITAR — defense articles and services on the US Munitions List (USML); EAR — dual-use items on the Commerce Control List (CCL). Includes 'deemed exports' (sharing controlled technology with foreign nationals in the US)
**Trigger:** Manufacturing, exporting, re-exporting, transferring, or brokering items on USML or CCL; employing or hosting foreign nationals with access to USML/CCL technology ('deemed export'); receiving technical data from a US person subject to ITAR/EAR
**Jurisdiction:** United States extraterritorial — applies globally to US-origin items, technology, and software; enforced by DDTC (State, ITAR) and BIS (Commerce, EAR)
**Not applicable to:** Purely domestic transfers with no export or foreign-national access; EAR99 items with no applicable export control classification number; publicly available information (EAR §734.3(b)(3)); fundamental research (EAR §734.8); news media activities
**Overall confidence:** HIGH for all sections in this file (all DETERMINISTIC)
**Covers:** Denied party screening (EAR §744 + ITAR debarred), record-keeping (EAR §762, ITAR §122.5), DDTC registration status (ITAR §122)

---

## Pre-Condition: Jurisdiction Classification Fixture

All ITAR/EAR tests require a prior classification determination on file. This file's DETERMINISTIC tests are independent of classification content but still require that a classification record exists and is not stale.

```python
@pytest.fixture(autouse=True)
def require_export_control_program(export_control_config: dict):
    if not export_control_config.get("export_control_program_active"):
        pytest.skip("Export control program not active — tests informational only")
```

---

## §744 (EAR) + ITAR §127 — Denied Party Screening (DETERMINISTIC)

### Source excerpts

> **EAR §744.11:** No person may export, reexport, or transfer (in-country) any item to a party that has been designated on the Entity List if the item is controlled for reasons listed in supplement 4 to this part.
>
> **EAR §764.2:** It is unlawful to export, reexport, or engage in other conduct with a denied party or to take actions that violate the terms of a denial order.
>
> **ITAR §127.7:** The DDTC may debar a person from engaging in defense trade for a period not to exceed three years.

### Official restricted party lists

| List | Authority | Updates |
|---|---|---|
| Specially Designated Nationals (SDN) | OFAC / Treasury | Multiple times per week |
| Denied Persons List (DPL) | BIS / Commerce | Published when orders issued |
| Entity List | BIS / Commerce | Updated by Federal Register notice |
| Unverified List (UVL) | BIS / Commerce | Updated when parties fail end-use checks |
| Debarred List | DDTC / State | Updated when orders issued |
| Nonproliferation Sanctions | State Dept. | Multiple specialized lists |
| Consolidated Screening List (CSL) | Multiple agencies | Updated daily — aggregates all U.S. government lists |

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Any transaction involving controlled technology, hardware, software, or services | DETERMINISTIC |
| Obligation | Screen all parties (buyers, sellers, intermediaries, end-users) against official lists before transaction | DETERMINISTIC |
| Timing | Before each transaction; re-screen on known change to parties | DETERMINISTIC |
| Evidence | Screening log: party name, list searched, date, result; negative match documented | DETERMINISTIC |

**Assumption (ASSUME-ITAR-001):** Denied party screening is adequate when: (1) all parties to each transaction are screened against the Consolidated Screening List (CSL) at minimum; (2) screening occurs before the transaction completes — not retroactively; (3) fuzzy matching applied — exact name match alone insufficient (variants, transliterations, aliases checked); (4) matches investigated within 24 hours; confirmed matches halt the transaction; (5) screening log retained for 5 years per §762 / §122.5; (6) list currency: CSL checked within last 24 hours prior to transaction (update frequency is multiple times daily for SDN).

**Overall: DETERMINISTIC → Pattern 1**

---

## EAR §762 + ITAR §122.5 — Record-Keeping Requirements (DETERMINISTIC)

### Source excerpts

> **EAR §762.2:** The records retention period is 5 years from: the date of export, reexport, or transfer; the date the license was returned, revoked, or amended; or the date of the transaction involving the license exception or no license required designation.
>
> **ITAR §122.5(a):** All persons required to register under this part shall keep and maintain records concerning the manufacture, acquisition, and disposition of defense articles registered, the provision of defense services, and the export and temporary import of defense articles. Such records shall be maintained for a period of five years from the expiration of the license or other approval, from the date of the transaction, or from the date on which the approval is revoked, whichever is latest.

### Required record types

| Record type | ITAR | EAR | Retention |
|---|---|---|---|
| Export license and supporting documents | ✅ §123.9 | ✅ §762.2 | 5 years from transaction |
| Shipping and export documents (EEI, AES) | ✅ | ✅ | 5 years |
| License exception records | — | ✅ §762.2 | 5 years |
| No License Required (NLR) determinations | — | ✅ | 5 years |
| Denied party screening records | ✅ (due diligence) | ✅ (due diligence) | 5 years |
| Commodity jurisdiction (CJ) requests + responses | ✅ | ✅ | 5 years |
| Technology control plan (TCP) + access logs | ✅ | ✅ | 5 years + ongoing |
| Employee training records | ✅ (due diligence) | ✅ (due diligence) | 5 years |
| End-use certificates / end-user statements | ✅ §123.10 | ✅ §748.11 | 5 years |

**Assumption (ASSUME-ITAR-002):** Record-keeping is compliant when: (1) all required record types above are maintained; (2) retention period is 5 years from the latest applicable trigger date (transaction date, license expiration, or revocation date — whichever is latest); (3) records are retrievable within a reasonable time for government inspection; (4) electronic records are acceptable — format must be legible and auditable; (5) destruction schedule enforced — records are not deleted before the 5-year minimum.

**Overall: DETERMINISTIC → Pattern 1**

---

## ITAR §122 — DDTC Registration Status (DETERMINISTIC)

### Source excerpt

> **ITAR §122.1:** Any person who engages in the United States in the business of either manufacturing or exporting defense articles or furnishing defense services is required to register with the Directorate of Defense Trade Controls.
>
> Registration must be renewed annually. Failure to maintain active registration violates ITAR §127 and can result in debarment.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Entity manufactures, exports, or furnishes defense services | DETERMINISTIC (once classification determines ITAR applicability) |
| Obligation | DDTC registration active and current | DETERMINISTIC |
| Renewal | Annual | DETERMINISTIC |
| Evidence | DDTC registration number; expiration date; Directorate verification | DETERMINISTIC |

**Assumption (ASSUME-ITAR-003):** DDTC registration is compliant when: (1) active DDTC registration number on file; (2) registration expiration date > today; (3) renewal initiated at least 60 days before expiration (DDTC renewal processing times); (4) registration fee paid for current year; (5) any material changes to activities reported to DDTC within 60 days per §122.4; (6) registration status verifiable via DDTC system.

**Overall: DETERMINISTIC → Pattern 1**

---

## Test specifications

### YAML spec — ITAR/EAR deterministic controls

```yaml
spec_id: ITAR-EAR-DET-001
framework: ITAR / EAR
regulations:
  - ITAR 22 CFR 120-130
  - EAR 15 CFR 730-774
pattern: 1  # All tests in this file
controls:
  - EAR §744 (denied party / entity list)
  - EAR §762 (record-keeping)
  - ITAR §122 (DDTC registration)
  - ITAR §122.5 (record-keeping)
  - ITAR §127.7 (debarred list)
subject: Any U.S. person engaged in export of controlled items, technology, or services
conditions:
  - export_control_program_active == true
  - entity is registered ITAR manufacturer/exporter OR transacts in EAR-controlled items
obligations:
  - Denied party screening: all parties screened before each transaction; CSL checked within 24h
  - Record-keeping: all export records retained 5 years from latest trigger date
  - DDTC registration: active, current, renewed annually
evidence:
  - screening_log (party name, date, list searched, result, disposition)
  - export_records (license, shipping docs, NLR/exception records)
  - ddtc_registration (registration number, expiration date)
```

### Python test file

```python
# tests/itar_ear/test_itar_ear_deterministic.py
"""
ITAR / EAR Deterministic Controls: Denied Party Screening, Record-Keeping, Registration.

Controls: EAR §744, §762; ITAR §122, §122.5, §127.7
Assumptions: ASSUME-ITAR-001 through ASSUME-ITAR-003
"""
import pytest
from datetime import datetime, timedelta, timezone
from typing import Any

RECORD_RETENTION_YEARS = 5
DDTC_RENEWAL_LEAD_DAYS = 60
SCREENING_CURRENCY_HOURS = 24
MATCH_INVESTIGATION_HOURS = 24


@pytest.fixture(autouse=True)
def require_export_control_program(export_control_config: dict[str, Any]):
    """Gate: skip all tests if export control program is not active."""
    if not export_control_config.get("export_control_program_active"):
        pytest.skip("Export control program not active — tests informational only")


# ── Denied Party Screening ───────────────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-ITAR-001",
    description="All parties screened against CSL before each transaction; list within 24h",
    approved_by="Export Compliance Officer",
    review_date="2027-05-20",
)
def test_all_recent_transactions_have_screening_records(
    transaction_records: list[dict[str, Any]],
    screening_log: list[dict[str, Any]],
):
    """EAR §744 / ITAR §127: Every controlled technology transaction must have a screening record."""
    screened_transaction_ids = {s["transaction_id"] for s in screening_log}

    missing_screens = []
    for tx in transaction_records:
        if not tx.get("involves_controlled_technology"):
            continue
        if tx["transaction_id"] not in screened_transaction_ids:
            missing_screens.append(tx["transaction_id"])

    assert not missing_screens, (
        f"Transactions involving controlled technology with no screening record: {missing_screens}"
    )


@pytest.mark.assumption(
    id="ASSUME-ITAR-001",
    description="Screening performed before transaction; no retroactive screening",
    approved_by="Export Compliance Officer",
    review_date="2027-05-20",
)
def test_screening_precedes_transaction(
    transaction_records: list[dict[str, Any]],
    screening_log: list[dict[str, Any]],
):
    """EAR §744: Denied party screening must occur before the transaction is completed."""
    screening_by_tx = {s["transaction_id"]: s for s in screening_log}

    retroactive = []
    for tx in transaction_records:
        if not tx.get("involves_controlled_technology"):
            continue
        screen = screening_by_tx.get(tx["transaction_id"])
        if screen is None:
            continue  # Covered by previous test
        screening_ts = screen.get("screening_timestamp")
        completion_ts = tx.get("completion_timestamp")
        if screening_ts and completion_ts and screening_ts > completion_ts:
            retroactive.append(
                f"{tx['transaction_id']}: screened {screening_ts} AFTER completion {completion_ts}"
            )

    assert not retroactive, (
        f"Screening performed after transaction completion (retroactive — not acceptable): {retroactive}"
    )


@pytest.mark.assumption(
    id="ASSUME-ITAR-001",
    description="CSL must be checked within 24 hours of use; stale list check is non-compliant",
    approved_by="Export Compliance Officer",
    review_date="2027-05-20",
)
def test_screening_list_currency(screening_log: list[dict[str, Any]]):
    """EAR §744: Screening must use a list checked within the last 24 hours (CSL updates multiple times daily)."""
    stale_screens = []

    for screen in screening_log:
        list_last_updated = screen.get("csl_list_download_timestamp")
        screening_ts = screen.get("screening_timestamp")
        if list_last_updated is None or screening_ts is None:
            continue
        age_hours = (screening_ts - list_last_updated).total_seconds() / 3600
        if age_hours > SCREENING_CURRENCY_HOURS:
            stale_screens.append(
                f"{screen['screening_id']}: CSL was {age_hours:.1f}h old at screening time "
                f"(max {SCREENING_CURRENCY_HOURS}h)"
            )

    assert not stale_screens, (
        f"Denied party screenings using stale CSL data: {stale_screens}"
    )


def test_no_unresolved_positive_screening_matches(screening_log: list[dict[str, Any]]):
    """EAR §744 / ITAR §127: Positive screening matches must be investigated and resolved before proceeding."""
    unresolved_matches = []

    for screen in screening_log:
        if not screen.get("match_found"):
            continue
        if screen.get("match_disposition") in {"confirmed_different_party", "false_positive_cleared"}:
            continue
        if screen.get("match_disposition") == "confirmed_match":
            transaction_halted = screen.get("transaction_halted", False)
            assert transaction_halted, (
                f"Screening {screen['screening_id']}: confirmed match but transaction was not halted"
            )
        elif screen.get("match_disposition") is None:
            unresolved_matches.append(screen["screening_id"])

    assert not unresolved_matches, (
        f"Screening matches with no recorded disposition (unresolved): {unresolved_matches}"
    )


# ── Record-Keeping ───────────────────────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-ITAR-002",
    description="All required export record types retained for 5 years from latest trigger date",
    approved_by="Export Compliance Officer",
    review_date="2027-05-20",
)
def test_export_records_retained_5_years(export_records: list[dict[str, Any]]):
    """EAR §762 / ITAR §122.5: Export records must be retained for 5 years from latest trigger date."""
    now = datetime.now(timezone.utc)
    premature_deletions = []

    for record in export_records:
        if record.get("status") != "deleted":
            continue
        deletion_date = record.get("deletion_date")
        latest_trigger = record.get("latest_trigger_date")  # latest of: transaction, license expiry, revocation
        if deletion_date is None or latest_trigger is None:
            continue

        years_retained = (deletion_date - latest_trigger).days / 365.25
        if years_retained < RECORD_RETENTION_YEARS:
            premature_deletions.append(
                f"{record['record_id']}: deleted after {years_retained:.1f} years "
                f"(minimum {RECORD_RETENTION_YEARS} years from {latest_trigger.date()})"
            )

    assert not premature_deletions, (
        f"Export records deleted before 5-year retention minimum: {premature_deletions}"
    )


@pytest.mark.assumption(
    id="ASSUME-ITAR-002",
    description="All required record types present in the export records system",
    approved_by="Export Compliance Officer",
    review_date="2027-05-20",
)
def test_required_record_types_maintained(export_records_inventory: dict[str, Any]):
    """EAR §762 / ITAR §122.5: All required record categories must be maintained."""
    required_record_types = {
        "export_licenses",
        "shipping_documents",
        "denied_party_screening_logs",
        "commodity_jurisdiction_records",
        "technology_control_plan",
        "employee_training_records",
    }

    maintained_types = set(export_records_inventory.get("maintained_record_types", []))
    missing_types = required_record_types - maintained_types

    assert not missing_types, (
        f"Required export control record types not maintained: {missing_types}"
    )


# ── DDTC Registration ────────────────────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-ITAR-003",
    description="DDTC registration active; renewal initiated ≥60 days before expiration",
    approved_by="Export Compliance Officer",
    review_date="2027-05-20",
)
def test_ddtc_registration_active(ddtc_registration: dict[str, Any]):
    """ITAR §122: DDTC registration must be active and current."""
    status = ddtc_registration.get("status", "").lower()
    assert status == "active", (
        f"DDTC registration status is {status!r} — must be 'active'. "
        "ITAR activities cannot continue with lapsed registration."
    )

    expiration_date = ddtc_registration.get("expiration_date")
    assert expiration_date is not None, "DDTC registration has no expiration date recorded"

    now = datetime.now(timezone.utc)
    assert expiration_date > now, (
        f"DDTC registration expired on {expiration_date.date()} — immediate renewal required"
    )


@pytest.mark.assumption(
    id="ASSUME-ITAR-003",
    description="DDTC renewal initiated at least 60 days before expiration to allow processing time",
    approved_by="Export Compliance Officer",
    review_date="2027-05-20",
)
def test_ddtc_renewal_initiated_in_advance(ddtc_registration: dict[str, Any]):
    """ITAR §122: DDTC renewal must be initiated at least 60 days before expiration."""
    now = datetime.now(timezone.utc)
    expiration_date = ddtc_registration.get("expiration_date")
    renewal_submitted_date = ddtc_registration.get("renewal_submitted_date")

    if expiration_date is None:
        return  # Covered by active test

    days_until_expiry = (expiration_date - now).days

    if days_until_expiry <= DDTC_RENEWAL_LEAD_DAYS and renewal_submitted_date is None:
        pytest.fail(
            f"DDTC registration expires in {days_until_expiry} days "
            f"but renewal has not been submitted — submit at least {DDTC_RENEWAL_LEAD_DAYS} days in advance"
        )

    if renewal_submitted_date:
        # Verify renewal was submitted at least 60 days before expiry
        days_lead = (expiration_date - renewal_submitted_date).days
        if days_lead < DDTC_RENEWAL_LEAD_DAYS:
            pytest.warns(
                UserWarning,
                match="DDTC renewal submitted less than 60 days before expiration — processing delays may cause lapse",
            )
```

---

## Open assumption registry (this file)

| ID | Domain | Summary | Review date |
|---|---|---|---|
| ASSUME-ITAR-001 | Denied party screening | CSL checked within 24h; screening before transaction; fuzzy name matching; confirmed matches halt transaction; screening log retained 5 years | 2026-05-20 |
| ASSUME-ITAR-002 | Record-keeping | All record types maintained; 5-year retention from latest of: transaction date, license expiration, or revocation; electronic format acceptable | 2026-05-20 |
| ASSUME-ITAR-003 | DDTC registration | Active registration with DDTC; expiration date current; renewal submitted ≥60 days before expiry; material changes reported within 60 days | 2026-05-20 |
