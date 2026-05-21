# Requirement 3 — Protect Stored Account Data

**Registry path:** `/regulation-registry/PCI-DSS/Req-3/`
**Version:** PCI DSS v4.0 (mandatory since March 31, 2025)
**Last parsed:** 2026-05-20
**Applies to:** Any organization that stores, processes, or transmits payment card data — merchants of all levels, payment processors, acquirers, issuers, and service providers in the card payment ecosystem
**Trigger:** Participation in the card payment ecosystem; card brand contracts (Visa, Mastercard, Amex, Discover, UnionPay); acquiring bank contractual requirement; SAQ level determined by annual transaction volume
**Jurisdiction:** Global — enforced by card brands (Visa/Mastercard/Amex/Discover) and acquiring banks; no geographic restriction
**Not applicable to:** Organizations that never handle cardholder data and fully outsource all card processing to a PCI-DSS-compliant third party; SAQ A merchants processing only redirected card transactions
**Overall confidence:** HIGH — PAN masking and SAD prohibition are DETERMINISTIC; key management adequacy is PARAMETERIZED
**R = Required**

---

## Scope summary

Req 3 governs account data at rest. It has two DETERMINISTIC anchors with zero ambiguity: (1) sensitive authentication data (SAD) must not be stored after authorization — full stop, no exceptions; (2) PAN displayed to users must be masked to first 6 / last 4 digits maximum. The PARAMETERIZED surface is key management — the regulation requires strong cryptography for stored PAN but does not mandate a specific algorithm, key length, or key management solution.

Req 3 distinguishes two data categories:
- **Cardholder data (CHD):** PAN, cardholder name, expiration date, service code
- **Sensitive authentication data (SAD):** Full magnetic stripe/chip data (Track 1/2), CVV/CVC/CAV, PIN/PIN blocks

CHD may be stored with proper protection. SAD must never be stored after authorization.

---

## 3.3 — SAD Must Not Be Stored After Authorization (R — DETERMINISTIC)

### Source excerpt

> *3.3.1 — SAD is not retained after authorization. All sensitive authentication data received is rendered unrecoverable upon completion of the authorization process.*
> *3.3.1.1 — The full contents of any track are not retained upon completion of the authorization process.*
> *3.3.1.2 — The card verification code is not retained upon completion of the authorization process.*
> *3.3.1.3 — The personal identification number (PIN) and the PIN block are not retained upon completion of the authorization process.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All systems that receive SAD during payment authorization | DETERMINISTIC |
| Condition | Authorization process has completed | DETERMINISTIC |
| Obligation | Full track data, CVV/CVC, and PIN blocks are not stored anywhere — not in logs, databases, memory dumps, or temporary files | DETERMINISTIC |
| Evidence | `data_discovery_scan.sad_found == false`; `transaction_logs.cvv_present == false`; database schema review | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 3.4 — PAN Display Masking (R — DETERMINISTIC)

### Source excerpt

> *3.4.1 — The PAN is masked when displayed (the BIN and last four digits are the maximum number of digits to be displayed), such that only personnel with a legitimate business need can see more than the BIN and last four digits of the PAN.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | Any display of PAN to users | DETERMINISTIC |
| Condition | PAN is displayed on screen, report, receipt, or print | DETERMINISTIC |
| Obligation | Maximum visible: first 6 digits (BIN) + last 4 digits; all other digits masked | DETERMINISTIC |
| Evidence | `display_configuration.pan_mask_format` = `[first 6]****[last 4]` or equivalent; application code review | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 3.4.2 — Remote Access PAN Copy Controls (R — DETERMINISTIC)

### Source excerpt

> *3.4.2 — When using remote-access technologies, technical controls prevent copy and/or relocation of PAN for all personnel, except for those with documented, explicit authorization and a legitimate, defined business need.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | Remote access sessions to CDE systems | DETERMINISTIC |
| Condition | Personnel connect via RDP, VPN, or similar remote access technology | DETERMINISTIC |
| Obligation | Copy/paste of PAN disabled in remote sessions; exceptions documented and authorized | DETERMINISTIC |
| Evidence | `remote_access_config.clipboard_redirect_disabled == true` or equivalent technical control; exception registry | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 3.5 — PAN Encrypted at Rest (R — DETERMINISTIC existence; PARAMETERIZED strength)

### Source excerpt

> *3.5.1 — Primary account number is secured with strong cryptography wherever it is stored, using any of the following approaches: one-way hashes based on strong cryptography of the entire PAN; truncation; index tokens with the pads being securely stored; strong cryptography with associated key management processes and procedures.*

### Element extraction — encryption existence

| Element | Value | Classification |
|---|---|---|
| Subject | All stored PAN | DETERMINISTIC |
| Condition | PAN exists in a stored medium (database, file, cache, backup) | DETERMINISTIC |
| Obligation | PAN secured by one of: strong crypto, one-way hash, truncation, or index token | DETERMINISTIC |
| Evidence | `pan_storage_config.protection_method` is one of the 4 accepted methods | DETERMINISTIC |

### Element extraction — key management

| Element | Value | Classification |
|---|---|---|
| Obligation | Key management processes and procedures documented; key custodians designated; split knowledge/dual control for key-encrypting keys | PARAMETERIZED |
| Evidence | Key management documentation review; key custodian designation | PARAMETERIZED |

**Assumption (ASSUME-3-001):** "Strong cryptography" for stored PAN is satisfied by: AES-128 or AES-256 with FIPS 140-2 or 140-3 validated modules; RSA-2048 or RSA-4096 for asymmetric key operations. SHA-256 keyed hash (HMAC-SHA256) is acceptable for one-way hashing of PAN. MD5 and SHA-1 are NOT acceptable for new PAN protection implementations. Key rotation: data encryption keys (DEKs) rotated at least annually; key encryption keys (KEKs) rotated when a cryptoperiod expires or when a key custodian leaves.

**Assumption (ASSUME-3-002):** Split knowledge / dual control for key-encrypting keys (KEKs) is satisfied by: HSM with M-of-N access control, or a key management system that requires two separate individuals to perform key operations on KEKs. Automated key management solutions with documented approval workflows may substitute if they prevent single-person access to the plaintext KEK.

**Overall: DETERMINISTIC for protection existence → Pattern 1; PARAMETERIZED for key management → Pattern 2**

---

## YAML specifications

### `req3_sad_prohibition.yaml`

```yaml
regulation_id: PCI-DSS-v4.0-3.3.1
section: "PCI DSS v4.0 — SAD Post-Authorization Storage Prohibition"
r_or_a: Required
source_text: >
  SAD is not retained after authorization. All SAD received is rendered
  unrecoverable upon completion of the authorization process.

extracted_elements:
  subject: "All systems that receive SAD during payment authorization"
  condition: "Authorization process completed"
  obligation: "No track data, CVV/CVC, or PIN stored anywhere after auth"
  evidence: "data_discovery_scan.sad_found=false; transaction_log CVV field empty"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log: []
test_confidence: HIGH
generated_test: "tests/req3/test_3_3_sad_prohibition.py"
```

### `req3_pan_encryption.yaml`

```yaml
regulation_id: PCI-DSS-v4.0-3.5.1
section: "PCI DSS v4.0 — PAN Encryption at Rest"
r_or_a: Required
source_text: >
  Primary account number secured with strong cryptography wherever stored.

extracted_elements:
  subject: "All stored PAN"
  condition: "PAN exists in any stored medium"
  obligation: "Protected by strong crypto, one-way hash, truncation, or index token"
  evidence: "pan_storage_config.protection_method; key_management_documentation"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: PARAMETERIZED

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-3-001
    assumption_text: >
      Strong cryptography: AES-128/256 (FIPS 140-2/3). HMAC-SHA256 for hashing.
      MD5 and SHA-1 not acceptable for new implementations.
      DEK rotation at least annually; KEK rotation on cryptoperiod expiry.
    assumed_by: "IT Security Officer"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
    cryptographic_hash: "sha256:pending-ci"
  - assumption_id: ASSUME-3-002
    assumption_text: >
      Split knowledge/dual control for KEKs: HSM with M-of-N, or key management
      system requiring two individuals for KEK operations.
    assumed_by: "IT Security Officer"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
    cryptographic_hash: "sha256:pending-ci"
test_confidence: HIGH
generated_test: "tests/req3/test_3_5_pan_encryption.py"
```

---

## Generated tests

### `tests/req3/test_3_3_sad_prohibition.py`

```python
"""
PCI DSS v4.0 Req 3.3 — SAD Post-Authorization Storage Prohibition
Confidence: HIGH | Human Review: NOT REQUIRED
"""

SAD_FIELD_PATTERNS = [
    "track1", "track2", "full_track", "magnetic_stripe",
    "cvv", "cvc", "cav", "cvv2", "cvc2",
    "pin_block", "pin",
]


def test_no_sad_in_database_schemas(database_schema_reviews):
    """3.3.1 — SAD must not appear in any database schema."""
    violations = []
    for review in database_schema_reviews:
        sad_fields = [
            col for col in review.get("columns", [])
            if any(pat in col.lower() for pat in SAD_FIELD_PATTERNS)
            and not review.get("pre_auth_only")
        ]
        if sad_fields:
            violations.append(
                f"Database {review['database_id']}: potential SAD fields: {sad_fields}"
            )
    assert not violations, (
        f"VIOLATION (3.3.1): {len(violations)} database(s) with SAD field patterns "
        f"in schema:\n" + "\n".join(violations)
    )


def test_no_sad_in_transaction_logs(transaction_log_samples):
    """3.3.1.2 — CVV/CVC must not appear in transaction logs."""
    violations = [
        r for r in transaction_log_samples
        if r.get("cvv_present") or r.get("full_track_present")
    ]
    assert not violations, (
        f"VIOLATION (3.3.1): {len(violations)} transaction log sample(s) containing "
        f"SAD (CVV or full track data): "
        f"{[r.get('log_entry_id') for r in violations]}"
    )


def test_data_discovery_scan_finds_no_sad(data_discovery_results):
    """3.3.1 — Automated data discovery must confirm no SAD stored post-authorization."""
    violations = [
        r for r in data_discovery_results
        if r.get("sad_detected") and not r.get("pre_auth_buffer_only")
    ]
    assert not violations, (
        f"VIOLATION (3.3.1): {len(violations)} data discovery result(s) found SAD "
        f"in unauthorized locations:\n"
        + "\n".join(
            f"  {r.get('location')}: {r.get('sad_type')}" for r in violations
        )
    )
```

### `tests/req3/test_3_4_pan_masking.py`

```python
"""
PCI DSS v4.0 Req 3.4 — PAN Display Masking
Confidence: HIGH | Human Review: NOT REQUIRED
"""
import re

PAN_MASK_PATTERN = re.compile(r"^\d{6}\*+\d{4}$")


def test_pan_display_masked_to_first_6_last_4(pan_display_configs):
    """3.4.1 — Displayed PAN must show first 6 (BIN) and last 4 digits only."""
    violations = [
        c for c in pan_display_configs
        if not c.get("mask_applied")
        or not PAN_MASK_PATTERN.match(c.get("sample_masked_pan", ""))
    ]
    assert not violations, (
        f"VIOLATION (3.4.1): {len(violations)} display configuration(s) not masking "
        f"PAN to first-6/last-4: "
        f"{[c['display_context'] for c in violations]}"
    )


def test_remote_access_pan_copy_disabled(remote_access_configs):
    """3.4.2 — Copy/paste of PAN must be disabled in remote access sessions."""
    violations = [
        c for c in remote_access_configs
        if c.get("accesses_cde")
        and not c.get("clipboard_redirect_disabled")
        and not c.get("pan_copy_exception_documented")
    ]
    assert not violations, (
        f"VIOLATION (3.4.2): {len(violations)} remote access configuration(s) without "
        f"PAN copy controls: {[c['config_id'] for c in violations]}"
    )
```

### `tests/req3/test_3_5_pan_encryption.py`

```python
"""
PCI DSS v4.0 Req 3.5 — PAN Encryption at Rest
Confidence: HIGH for protection existence; MEDIUM for key management adequacy
"""
import pytest

ACCEPTED_PROTECTION_METHODS = {
    "aes_encryption",
    "one_way_hash",
    "truncation",
    "index_token",
}


def test_all_pan_storage_is_protected(pan_storage_locations):
    """3.5.1 — All stored PAN must be protected by strong cryptography or equivalent."""
    violations = [
        loc for loc in pan_storage_locations
        if loc.get("protection_method") not in ACCEPTED_PROTECTION_METHODS
    ]
    assert not violations, (
        f"VIOLATION (3.5.1): {len(violations)} PAN storage location(s) with "
        f"unacceptable or missing protection method: "
        f"{[(l['storage_id'], l.get('protection_method')) for l in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-3-001",
    description=(
        "Strong crypto: AES-128/256 FIPS 140-2/3. HMAC-SHA256 for hashing. "
        "MD5/SHA-1 not acceptable. DEK rotation ≥ annually."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_encryption_algorithm_is_strong(pan_storage_locations):
    WEAK_ALGORITHMS = {"md5", "sha1", "sha-1", "des", "3des", "rc4"}
    violations = [
        loc for loc in pan_storage_locations
        if loc.get("protection_method") in ("aes_encryption", "one_way_hash")
        and loc.get("algorithm", "").lower() in WEAK_ALGORITHMS
    ]
    assert not violations, (
        f"VIOLATION (3.5.1): {len(violations)} PAN storage location(s) using weak "
        f"algorithm: "
        f"{[(l['storage_id'], l.get('algorithm')) for l in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-3-002",
    description=(
        "KEK split knowledge/dual control: HSM M-of-N or key management system "
        "requiring two individuals for KEK operations."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_key_management_documentation_exists(key_management_records):
    """3.7 — Key management processes must be documented."""
    assert key_management_records, (
        "VIOLATION (3.7): No key management documentation found — required for "
        "all cryptographic key operations protecting PAN."
    )
    violations = [
        r for r in key_management_records
        if not r.get("key_custodians_designated")
    ]
    assert not violations, (
        f"VIOLATION (3.7): {len(violations)} key type(s) without designated "
        f"custodians: {[r['key_type'] for r in violations]}"
    )
```

---

## Notes for the registry

- **SAD prohibition has no exceptions:** Unlike PCI DSS's general "customized approach" flexibility, 3.3.1 is absolute — SAD must not be stored anywhere after authorization, even if encrypted. There is no compliance path for storing encrypted CVV/track data post-authorization.
- **Logs are a common SAD leak:** Verbose application and network logging frequently captures CVV values, full track data, or raw PAN in plaintext. Transaction processing logs should be reviewed specifically for SAD presence as part of any compliance review. Mask/redact at the logging layer, not just at the display layer.
- **Truncation is not the same as encryption:** Truncated PAN (e.g., `****1234`) is an accepted protection method under 3.5.1 but does not allow reconstruction of the full PAN — the truncated form cannot be decrypted back to the full PAN. If the full PAN is needed for business purposes, encryption (not truncation) must be used.
- **Index tokens:** Tokenization using an index (mapping token → real PAN in a separate secure token vault) is accepted under 3.5.1. The token vault itself must be secured per all PCI DSS requirements; the token environment cannot be de-scoped simply by using tokens unless segmentation is effective.
- **Key management (3.6–3.7) complexity:** Key management is the most operationally complex part of Req 3. A Hardware Security Module (HSM) is the clearest path to satisfying key generation, storage, distribution, and destruction requirements. Software key management without HSM requires much more extensive documentation to satisfy QSA review.
