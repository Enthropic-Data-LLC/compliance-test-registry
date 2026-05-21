# Requirement 4 — Protect Cardholder Data with Strong Cryptography During Transmission

**Registry path:** `/regulation-registry/PCI-DSS/Req-4/`
**Version:** PCI DSS v4.0 (mandatory since March 31, 2025)
**Last parsed:** 2026-05-20
**Applies to:** Any organization that stores, processes, or transmits payment card data — merchants of all levels, payment processors, acquirers, issuers, and service providers in the card payment ecosystem
**Trigger:** Participation in the card payment ecosystem; card brand contracts (Visa, Mastercard, Amex, Discover, UnionPay); acquiring bank contractual requirement; SAQ level determined by annual transaction volume
**Jurisdiction:** Global — enforced by card brands (Visa/Mastercard/Amex/Discover) and acquiring banks; no geographic restriction
**Not applicable to:** Organizations that never handle cardholder data and fully outsource all card processing to a PCI-DSS-compliant third party; SAQ A merchants processing only redirected card transactions
**Overall confidence:** HIGH — TLS version prohibition is DETERMINISTIC; certificate management is PARAMETERIZED
**R = Required**

---

## Scope summary

Req 4 is the shortest PCI DSS requirement in terms of test surface but contains one of the most consequential DETERMINISTIC thresholds in the entire standard: the prohibition on SSL and early TLS. TLS 1.2 is the minimum; TLS 1.3 is strongly recommended. The v4.0 addition of a certificate inventory requirement (4.2.1.2) adds a small DETERMINISTIC tracking obligation.

---

## 4.2.1 — Encryption During Transmission (R — DETERMINISTIC)

### Source excerpt

> *4.2.1 — Strong cryptography is used to safeguard PAN during transmission over open, public networks. Trusted keys/certificates are accepted. The protocol in use supports only secure versions or configurations. The encryption strength is appropriate for the encryption methodology in use.*

> *Note: SSL/early TLS is not considered strong cryptography and cannot be used as a security control. Entities must be using a current, secure version (TLS 1.2 or higher) of TLS.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All PAN transmitted over open, public networks | DETERMINISTIC |
| Condition | Transmission channel is open or public (internet, wireless, Bluetooth, GPRS, satellite) | DETERMINISTIC |
| Obligation | TLS 1.2 minimum; SSL/TLS 1.0/TLS 1.1 prohibited; trusted certificates only | DETERMINISTIC |
| Evidence | `tls_config.min_version >= "TLS1.2"`; `disabled_protocols` includes SSL, TLS1.0, TLS1.1; `certificate.trusted == true` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 4.2.1.1 — No Weak Cipher Suites (R — DETERMINISTIC)

### Source excerpt (from Req 4.2.1 sub-requirements)

> *Only trusted keys/certificates are accepted. The protocol in use supports only secure versions or configurations and does not support fallback to, or use of insecure protocols or methods.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | No export-grade, null, anonymous, RC4, DES, or 3DES cipher suites; no SSL fallback; no protocol downgrade | DETERMINISTIC |
| Evidence | TLS configuration scan: `cipher_suites` must not include NULL, EXPORT, anon, RC4, DES, 3DES | DETERMINISTIC |

**Assumption (ASSUME-4-001):** Acceptable cipher suites are those offering authenticated encryption with additional data (AEAD): AES-128-GCM, AES-256-GCM, CHACHA20-POLY1305. TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 and equivalent are the minimum acceptable for TLS 1.2. TLS 1.3 cipher suites are all AEAD and acceptable by definition.

**Overall: DETERMINISTIC → Pattern 1**

---

## 4.2.1.2 — Certificate Inventory (R — DETERMINISTIC)

### Source excerpt

> *4.2.1.2 — An inventory of the entity's trusted keys and certificates used to protect PAN during transmission is maintained.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All TLS certificates protecting PAN in transit | DETERMINISTIC |
| Condition | Certificate is in use for PAN transmission | DETERMINISTIC |
| Obligation | Certificate inventory exists; contains all certificates protecting PAN transmission | DETERMINISTIC |
| Evidence | `certificate_inventory`: `certificate_id`, `common_name`, `issuer`, `expiry_date`, `systems_protected[]` | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 4.2.2 — PAN Transmitted via End-User Messaging (R — DETERMINISTIC)

### Source excerpt

> *4.2.2 — PAN is secured with strong cryptography whenever it is sent via end-user messaging technologies such as e-mail, instant messaging, SMS, or chat.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | PAN sent via email, IM, SMS, or chat | DETERMINISTIC |
| Condition | PAN is being transmitted via a messaging technology | DETERMINISTIC |
| Obligation | PAN encrypted or not transmitted via messaging technologies at all; policy prohibiting unencrypted PAN in messaging | DETERMINISTIC |
| Evidence | `messaging_policy.pan_transmission == "prohibited_or_encrypted"`; DLP scan results | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## YAML specifications

### `req4_tls_version.yaml`

```yaml
regulation_id: PCI-DSS-v4.0-4.2.1
section: "PCI DSS v4.0 — Transmission Encryption"
r_or_a: Required
source_text: >
  Strong cryptography used to safeguard PAN during transmission over open,
  public networks. SSL/early TLS not considered strong cryptography.

extracted_elements:
  subject: "All PAN transmitted over open, public networks"
  condition: "Transmission over internet, wireless, Bluetooth, GPRS, or similar"
  obligation: "TLS 1.2 minimum; SSL/TLS 1.0/1.1 prohibited; trusted certs only"
  evidence: "tls_config: min_version TLS1.2; disabled_protocols includes SSL/TLS1.0/TLS1.1"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-4-001
    assumption_text: >
      Acceptable cipher suites: AEAD only (AES-128-GCM, AES-256-GCM,
      CHACHA20-POLY1305). All TLS 1.3 suites acceptable.
      Prohibited: NULL, EXPORT, anon, RC4, DES, 3DES cipher suites.
    assumed_by: "IT Security Officer"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
    cryptographic_hash: "sha256:pending-ci"
test_confidence: HIGH
generated_test: "tests/req4/test_4_2_transmission.py"
```

---

## Generated tests

### `tests/req4/test_4_2_transmission.py`

```python
"""
PCI DSS v4.0 Req 4.2 — Transmission Security
Confidence: HIGH | Human Review: ASSUMPTION REQUIRED (ASSUME-4-001) for cipher suites
"""
import pytest
from datetime import date

PROHIBITED_PROTOCOLS = {"SSL", "TLS1.0", "TLS1.1", "SSLv2", "SSLv3"}
PROHIBITED_CIPHER_PATTERNS = {"NULL", "EXPORT", "anon", "RC4", "DES", "3DES"}
CERT_EXPIRY_WARNING_DAYS = 30


def test_tls_minimum_version_is_1_2(tls_endpoint_configs):
    """4.2.1 — TLS 1.2 is the minimum allowed version."""
    violations = []
    for ep in tls_endpoint_configs:
        if ep.get("transmits_pan"):
            min_ver = ep.get("min_tls_version", "")
            if min_ver in ("", "SSL", "TLS1.0", "TLS1.1"):
                violations.append(
                    f"Endpoint {ep['endpoint_id']}: min TLS version is '{min_ver}'"
                )
    assert not violations, (
        f"VIOLATION (4.2.1): {len(violations)} PAN endpoint(s) below TLS 1.2:\n"
        + "\n".join(violations)
    )


def test_prohibited_protocols_disabled(tls_endpoint_configs):
    """4.2.1 — SSL and TLS 1.0/1.1 must be disabled on all PAN endpoints."""
    violations = []
    for ep in tls_endpoint_configs:
        if ep.get("transmits_pan"):
            enabled = set(ep.get("enabled_protocols", []))
            prohibited_found = enabled & PROHIBITED_PROTOCOLS
            if prohibited_found:
                violations.append(
                    f"Endpoint {ep['endpoint_id']}: prohibited protocols enabled: "
                    f"{prohibited_found}"
                )
    assert not violations, (
        f"VIOLATION (4.2.1): {len(violations)} endpoint(s) with prohibited protocols:\n"
        + "\n".join(violations)
    )


@pytest.mark.assumption(
    id="ASSUME-4-001",
    description="Only AEAD ciphers acceptable; NULL/EXPORT/anon/RC4/DES/3DES prohibited",
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_no_weak_cipher_suites(tls_endpoint_configs):
    """4.2.1.1 — No weak or prohibited cipher suites."""
    violations = []
    for ep in tls_endpoint_configs:
        if ep.get("transmits_pan"):
            suites = ep.get("enabled_cipher_suites", [])
            weak = [
                s for s in suites
                if any(pat in s.upper() for pat in PROHIBITED_CIPHER_PATTERNS)
            ]
            if weak:
                violations.append(
                    f"Endpoint {ep['endpoint_id']}: weak cipher suites enabled: {weak}"
                )
    assert not violations, (
        f"VIOLATION (4.2.1): {len(violations)} endpoint(s) with prohibited cipher "
        f"suites:\n" + "\n".join(violations)
    )


def test_certificate_inventory_exists(certificate_inventory):
    """4.2.1.2 — Certificate inventory must exist for all PAN-protecting certs."""
    assert certificate_inventory, (
        "VIOLATION (4.2.1.2): Certificate inventory is empty — no certificates recorded "
        "for PAN transmission protection"
    )


def test_certificates_not_expired(certificate_inventory):
    today = date.today()
    violations = []
    for cert in certificate_inventory:
        expiry = cert.get("expiry_date")
        if not expiry:
            violations.append(
                f"Cert {cert.get('certificate_id', '?')}: no expiry date recorded"
            )
            continue
        if expiry < today:
            violations.append(
                f"Cert {cert['certificate_id']}: expired {expiry} (protecting "
                f"{cert.get('systems_protected', [])})"
            )
    assert not violations, (
        f"VIOLATION (4.2.1): {len(violations)} expired certificate(s) in inventory:\n"
        + "\n".join(violations)
    )


def test_certificates_expiry_warning(certificate_inventory):
    today = date.today()
    expiring_soon = [
        cert for cert in certificate_inventory
        if cert.get("expiry_date")
        and 0 < (cert["expiry_date"] - today).days <= CERT_EXPIRY_WARNING_DAYS
    ]
    if expiring_soon:
        import warnings
        warnings.warn(
            f"{len(expiring_soon)} certificate(s) expiring within "
            f"{CERT_EXPIRY_WARNING_DAYS} days: "
            f"{[(c['certificate_id'], str(c['expiry_date'])) for c in expiring_soon]}"
        )


def test_pan_not_in_unencrypted_messaging(messaging_dlp_results):
    """4.2.2 — PAN must not be sent in unencrypted email, SMS, or messaging."""
    violations = [
        r for r in messaging_dlp_results
        if r.get("pan_detected") and not r.get("encrypted")
    ]
    assert not violations, (
        f"VIOLATION (4.2.2): {len(violations)} messaging event(s) containing "
        f"unencrypted PAN:\n"
        + "\n".join(
            f"  {r.get('message_id')}: {r.get('channel')} on {r.get('date')}"
            for r in violations
        )
    )
```

---

## Notes for the registry

- **SSL/TLS prohibition is hard:** There is no exception for SSL or early TLS in PCI DSS v4.0. The carve-out for POI devices with isolation controls was removed. Any endpoint using SSL, TLS 1.0, or TLS 1.1 is a violation.
- **TLS 1.3 recommendation:** While TLS 1.2 is the minimum, PCI SSC strongly recommends TLS 1.3 for new implementations. TLS 1.3 eliminates weak cipher suites by design and is forward-secure by default.
- **Certificate inventory (4.2.1.2) is new in v4.0:** v3.2.1 did not require a formal certificate inventory. Organizations upgrading must create and maintain one. The inventory should include: certificate ID, CN/SAN, issuer, expiry date, systems protected, and rotation responsibility.
- **End-user messaging (4.2.2):** The cleanest compliance path is to prohibit PAN transmission via email/SMS/chat entirely (policy + DLP enforcement) rather than attempting to encrypt messaging in transit. Most messaging systems do not provide user-controlled encryption.
- **Wireless networks:** Req 4.2.1 applies to Wi-Fi transmitting PAN — all wireless PAN traffic must use WPA3 or WPA2-Enterprise with strong encryption. WEP and open networks are prohibited.
