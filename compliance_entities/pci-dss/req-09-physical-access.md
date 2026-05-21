# Requirement 9 — Restrict Physical Access to Cardholder Data

**Registry path:** `/regulation-registry/PCI-DSS/Req-9/`
**Version:** PCI DSS v4.0 (mandatory since March 31, 2025)
**Last parsed:** 2026-05-20
**Overall confidence:** MEDIUM — visitor log retention and media inventory cadence are DETERMINISTIC; badge system and CCTV adequacy are PARAMETERIZED
**R = Required**

---

## Scope summary

Req 9 addresses physical security for CDE facilities, media, and point-of-interaction (POI) devices. It has fewer DETERMINISTIC thresholds than most other requirements — the specified thresholds are visitor log retention (3 months), media inventory review cadence (annual), and POI inspection interval (≤ 3 months for unattended high-risk devices). Physical safeguard adequacy (badge system type, CCTV coverage) is PARAMETERIZED because PCI DSS does not specify lock types, camera resolution, or badge technologies.

---

## 9.2.1 — Appropriate Facility Entry Controls (R — PARAMETERIZED)

### Source excerpt

> *9.2.1 — Appropriate facility entry controls are in place to restrict physical access to systems in the CDE. Entry controls are in place to restrict access to any physically isolated legacy systems that store, process, or transmit cardholder data.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All CDE facilities and server rooms | DETERMINISTIC |
| Condition | Facility houses CDE systems | PARAMETERIZED |
| Obligation | Physical access controls restrict entry to authorized personnel; controls appropriate to the risk | PARAMETERIZED |
| Evidence | `facility_access_config.access_mechanism`; authorized personnel list; access log review | PARAMETERIZED |

**Assumption (ASSUME-9-001):** Physical entry controls are adequate when: (1) access mechanism is documented (key card, PIN, biometric, or locked door with key inventory); (2) authorized personnel list is maintained and reviewed at least quarterly; (3) access events are logged with individual identity and timestamp; (4) logs are reviewed monthly; (5) unauthorized access attempts trigger an alert or investigation.

**Overall: PARAMETERIZED → Pattern 2**

---

## 9.2.2 — Physical Access Logs (R — DETERMINISTIC)

### Source excerpt

> *9.2.2 — Physical access to the CDE is monitored to detect and respond to physical access attempts. Logs of all physical access to the CDE are retained for at least three months.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All physical access to CDE facilities | DETERMINISTIC |
| Condition | Access event occurs | DETERMINISTIC |
| Obligation | Access logged with date, time, and individual identity; logs retained ≥ 3 months | DETERMINISTIC |
| Evidence | `physical_access_logs.retention_months >= 3`; log entries include `timestamp`, `individual_id` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 9.3.4 — Visitor Logs (R — DETERMINISTIC)

### Source excerpt

> *9.3.4 — A visitor log is used to maintain a physical audit trail of visitor activity. The visitor log contains the visitor's name, the firm represented, and the on-site personnel authorizing physical access. The log is kept for at least three months.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All visitors to CDE areas | DETERMINISTIC |
| Condition | Visitor accesses CDE area | DETERMINISTIC |
| Obligation | Visitor log maintained with name, firm, authorizing personnel; retained ≥ 3 months | DETERMINISTIC |
| Evidence | `visitor_log.retention_months >= 3`; entries include `visitor_name`, `firm`, `authorizing_personnel` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 9.4.5 — Electronic Media Inventory (R — DETERMINISTIC)

### Source excerpt

> *9.4.5 — Inventory logs of all electronic media with cardholder data are maintained.*
> *9.4.5.1 — Inventory logs are reviewed at least once every 12 months.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All electronic media storing CHD | DETERMINISTIC |
| Condition | Electronic media exists with CHD | DETERMINISTIC |
| Obligation | Inventory maintained; inventory reviewed ≤ 365 days | DETERMINISTIC |
| Evidence | `media_inventory.exists == true`; `media_inventory.last_review_date` ≤ 365 days | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 9.4.6 — Destruction of Hard-Copy CHD (R — DETERMINISTIC)

### Source excerpt

> *9.4.6 — Hard-copy materials with cardholder data are destroyed when no longer needed for business or legal reasons, as follows: Materials are cross-cut shredded, incinerated, or pulped so that cardholder data cannot be reconstructed.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All printed/hard-copy materials containing CHD | DETERMINISTIC |
| Condition | Hard-copy CHD no longer needed | DETERMINISTIC |
| Obligation | Destroyed by cross-cut shred, incineration, or pulping — not strip shredding | DETERMINISTIC |
| Evidence | `media_destruction_policy.method` is "cross_cut_shred", "incinerate", or "pulp" (NOT "strip_shred") | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 9.5.1.2 — POI Device Inspection (R — DETERMINISTIC for interval; PARAMETERIZED for method)

### Source excerpt

> *9.5.1.2 — POI device surfaces are periodically inspected to detect tampering and substitution. The inspection frequency is defined in the entity's targeted risk analysis and considers the following: The location of the device. Whether the device is attended or unattended. The incidence of attacks in the area.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All POI (point-of-interaction) devices | DETERMINISTIC |
| Condition | POI device in use | DETERMINISTIC |
| Obligation | Periodic visual inspection; frequency set by risk analysis; unattended high-risk devices inspected ≤ quarterly (best practice, frequently required by QSAs) | PARAMETERIZED |
| Evidence | `poi_inspection_records.device_id`; `poi_inspection_records.inspection_date`; risk-analysis-defined frequency | PARAMETERIZED |

**Assumption (ASSUME-9-002):** POI inspection frequency is adequate when: high-risk unattended locations (fuel pumps, ATMs, outdoor kiosks) are inspected at least monthly; low-risk attended indoor locations (checkout counters with staff present) are inspected at least quarterly. Inspection records must document the device ID, inspector identity, date, and outcome. Personnel must be trained to recognize skimming device characteristics.

**Overall: PARAMETERIZED → Pattern 2**

---

## YAML specifications

### `req9_physical_logs.yaml`

```yaml
regulation_id: PCI-DSS-v4.0-9.2.2
section: "PCI DSS v4.0 — Physical Access Log Retention"
r_or_a: Required
source_text: >
  Logs of all physical access to the CDE are retained for at least three months.

extracted_elements:
  subject: "Physical access logs for CDE facilities"
  condition: "CDE facility access event"
  obligation: "Log retained ≥ 3 months; entries include timestamp and individual identity"
  evidence: "physical_access_logs: retention_months >= 3, entries have timestamp + individual_id"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log: []
test_confidence: HIGH
generated_test: "tests/req9/test_9_2_physical_access.py"
```

---

## Generated tests

### `tests/req9/test_9_2_physical_access.py`

```python
"""
PCI DSS v4.0 Req 9.2 / 9.3 / 9.4 / 9.5 — Physical Access Controls
Confidence: HIGH for log retention and media cadence; MEDIUM for facility/POI controls
"""
import pytest
from datetime import date

PHYSICAL_LOG_MIN_RETENTION_MONTHS = 3
VISITOR_LOG_MIN_RETENTION_MONTHS = 3
MEDIA_INVENTORY_MAX_REVIEW_DAYS = 365


def test_physical_access_logs_retained_3_months(physical_access_log_configs):
    """9.2.2 — Physical access logs retained at least 3 months."""
    violations = [
        c for c in physical_access_log_configs
        if c.get("retention_months", 0) < PHYSICAL_LOG_MIN_RETENTION_MONTHS
    ]
    assert not violations, (
        f"VIOLATION (9.2.2): {len(violations)} CDE facility/facilities with physical "
        f"access log retention < 3 months: "
        f"{[(c['facility_id'], c.get('retention_months')) for c in violations]}"
    )


def test_physical_log_entries_have_identity_and_timestamp(physical_access_log_sample):
    """9.2.2 — Log entries must identify the individual and timestamp."""
    violations = [
        entry for entry in physical_access_log_sample
        if not entry.get("individual_id") or not entry.get("timestamp")
    ]
    assert not violations, (
        f"VIOLATION (9.2.2): {len(violations)} physical access log entry/entries "
        f"missing individual identity or timestamp"
    )


def test_visitor_logs_retained_3_months(visitor_log_configs):
    """9.3.4 — Visitor logs retained at least 3 months."""
    violations = [
        c for c in visitor_log_configs
        if c.get("retention_months", 0) < VISITOR_LOG_MIN_RETENTION_MONTHS
    ]
    assert not violations, (
        f"VIOLATION (9.3.4): {len(violations)} facility/facilities with visitor log "
        f"retention < 3 months: "
        f"{[(c['facility_id'], c.get('retention_months')) for c in violations]}"
    )


def test_visitor_log_entries_complete(visitor_log_sample):
    """9.3.4 — Visitor log entries must include name, firm, and authorizing personnel."""
    violations = [
        entry for entry in visitor_log_sample
        if not entry.get("visitor_name")
        or not entry.get("authorizing_personnel")
    ]
    assert not violations, (
        f"VIOLATION (9.3.4): {len(violations)} visitor log entry/entries missing "
        f"required fields (name, authorizing personnel)"
    )


def test_chd_media_inventory_reviewed_annually(media_inventory_records):
    """9.4.5.1 — CHD media inventory reviewed at least annually."""
    today = date.today()
    violations = []
    for record in media_inventory_records:
        last_review = record.get("last_review_date")
        if not last_review:
            violations.append(f"{record.get('inventory_id', '?')}: no review date")
            continue
        days = (today - last_review).days
        if days > MEDIA_INVENTORY_MAX_REVIEW_DAYS:
            violations.append(
                f"{record['inventory_id']}: last reviewed {days} days ago "
                f"(max {MEDIA_INVENTORY_MAX_REVIEW_DAYS})"
            )
    assert not violations, (
        f"VIOLATION (9.4.5.1): {len(violations)} CHD media inventory/inventories "
        f"not reviewed annually:\n" + "\n".join(violations)
    )


def test_hardcopy_chd_destruction_method_acceptable(media_destruction_policies):
    """9.4.6 — Hard-copy CHD must be cross-cut shredded, incinerated, or pulped."""
    acceptable_methods = {"cross_cut_shred", "incinerate", "pulp"}
    violations = [
        p for p in media_destruction_policies
        if p.get("media_type") == "hard_copy"
        and p.get("destruction_method") not in acceptable_methods
    ]
    assert not violations, (
        f"VIOLATION (9.4.6): {len(violations)} hard-copy destruction policy/policies "
        f"using unacceptable method (strip-shred not allowed): "
        f"{[(p['policy_id'], p.get('destruction_method')) for p in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-9-001",
    description=(
        "Facility entry controls adequate: documented mechanism; authorized list "
        "reviewed quarterly; events logged with identity/timestamp; logs reviewed "
        "monthly; unauthorized attempts investigated."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_cde_facilities_have_access_controls(cde_facilities, facility_access_configs):
    controlled_ids = {c["facility_id"] for c in facility_access_configs}
    violations = [
        f for f in cde_facilities
        if f["facility_id"] not in controlled_ids
    ]
    assert not violations, (
        f"VIOLATION (9.2.1): {len(violations)} CDE facility/facilities with no "
        f"access control record: {[f['facility_id'] for f in violations]}"
    )
```

---

## Notes for the registry

- **Strip shredding is explicitly prohibited:** 9.4.6 requires cross-cut (confetti) or micro-cut shredding, incineration, or pulping. Strip-cut shredding, which produces long strips that can be reconstructed, does not satisfy the requirement.
- **Visitor badges that are distinguishable:** 9.3.3 requires that visitor identification be visually distinguishable from employee badges. The most common implementation is a badge of a different color that says "VISITOR" in large text with an expiration time. Visitors should surrender the badge upon departure — lanyards that must be returned enforce this.
- **POI device anti-skimming program:** Many organizations focus on back-office CDE security and underinvest in POI device security. Fuel pump skimming attacks are among the highest-volume CHD theft vectors. Physical seals (tamper-evident tape or security labels with serial numbers) on POI device covers, combined with a formal inspection checklist and personnel training, are best practice.
- **Electronic media destruction (9.4.7):** Electronic media (hard drives, SSDs, USB drives, tapes) must be destroyed in a manner that makes CHD unrecoverable — NIST SP 800-88 methods (Clear, Purge, Destroy) apply. For outsourced destruction, a certificate of destruction from the vendor is required.
- **Cloud and virtual environments:** Req 9 physical controls apply to physical infrastructure. For cloud-hosted CDE components, the physical security obligations fall on the cloud provider (verified via their SOC 2 Type II or PCI Attestation of Compliance report, obtained under NDA). The entity's obligation is to verify those controls exist via third-party assessment documentation.
