# Requirement 2 — Apply Secure Configurations to All System Components

**Registry path:** `/regulation-registry/PCI-DSS/Req-2/`
**Version:** PCI DSS v4.0 (mandatory since March 31, 2025)
**Last parsed:** 2026-05-20
**Overall confidence:** HIGH — vendor default prohibition and non-console encryption are DETERMINISTIC; hardening standard selection is PARAMETERIZED
**R = Required**

---

## Scope summary

Req 2 mandates that all CDE system components be deployed in a securely configured state: no vendor defaults, unnecessary functionality removed, and all non-console administrative access encrypted. The term "vendor defaults" covers default passwords, SNMP community strings, SSIDs, and default accounts. The DETERMINISTIC prohibition on vendor defaults is the most-cited Req 2 finding. Configuration standard adequacy (which hardening benchmark to use) is PARAMETERIZED.

---

## 2.2.2 — No Vendor Default Accounts or Passwords (R — DETERMINISTIC)

### Source excerpt

> *2.2.2 — Vendor default accounts are managed as follows: If the vendor default account(s) will be used, the default password is changed per Requirement 8.3.6. If the vendor default account(s) will not be used, the account is removed or disabled.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All CDE system components | DETERMINISTIC |
| Condition | Component has vendor-provided default accounts or credentials | DETERMINISTIC |
| Obligation | Default accounts either: (a) changed password per Req 8.3.6, or (b) removed/disabled | DETERMINISTIC |
| Evidence | `system_config.default_accounts_managed == true`; no default credential in `credential_audit` scan | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 2.2.3 — Unnecessary Functionality Removed (R — PARAMETERIZED)

### Source excerpt

> *2.2.3 — All unnecessary functionality is removed, as follows: All unnecessary functionality is removed from system components, including but not limited to functions, scripts, drivers, features, subsystems, file systems, and unnecessary web servers.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All CDE system components | DETERMINISTIC |
| Condition | Component has been deployed | PARAMETERIZED |
| Obligation | Unnecessary services, ports, protocols, daemons, and software removed; only required functionality present | PARAMETERIZED |
| Evidence | Configuration baseline review; running services list against approved list; open port scan vs. approved ports | PARAMETERIZED |

**Assumption (ASSUME-2-001):** Unnecessary functionality is adequately removed when: (1) an approved services/ports/protocols list exists for each system class; (2) running services are compared against the approved list quarterly or after system changes; (3) any service not on the approved list is disabled or has a documented exception with business justification. Common findings: Telnet, FTP, unencrypted HTTP admin interfaces, default SNMP communities, sample/demo applications on web servers.

**Overall: PARAMETERIZED → Pattern 2**

---

## 2.2.7 — Non-Console Administrative Access Encrypted (R — DETERMINISTIC)

### Source excerpt

> *2.2.7 — All non-console administrative access is encrypted using strong cryptography.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All non-console administrative access to CDE systems | DETERMINISTIC |
| Condition | Administrative access is via network (non-console) | DETERMINISTIC |
| Obligation | Encrypted using strong cryptography (TLS 1.2+ or SSH with strong ciphers); Telnet, HTTP, FTP, and unencrypted SNMP prohibited | DETERMINISTIC |
| Evidence | `admin_access_config.protocol` must not be Telnet, HTTP, FTP, or SNMPv1/v2c; `encryption_protocol` is SSH or TLS 1.2+ | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 2.3 — Wireless Environments Secured (R — DETERMINISTIC)

### Source excerpt

> *2.3.1 — For wireless environments connected to the CDE or transmitting account data, all wireless vendor defaults are changed at installation, including but not limited to default wireless encryption keys, passwords, and SNMP community strings.*
> *2.3.2 — For wireless environments connected to the CDE or transmitting account data, wireless encryption keys are changed as follows: Whenever personnel with knowledge of the key leave the company or the role for which the knowledge was required. Whenever a key is suspected of or known to be compromised.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All wireless networks connected to CDE or transmitting account data | DETERMINISTIC |
| Condition | Wireless network exists in scope | DETERMINISTIC |
| Obligation | All wireless vendor defaults changed at installation; encryption keys changed when personnel with knowledge depart | DETERMINISTIC |
| Evidence | `wireless_config.default_credentials_changed == true`; `wireless_key_rotation_log.trigger` includes personnel departure | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## YAML specifications

### `req2_vendor_defaults.yaml`

```yaml
regulation_id: PCI-DSS-v4.0-2.2.2
section: "PCI DSS v4.0 — Vendor Default Account Management"
r_or_a: Required
source_text: >
  Vendor default accounts managed: default password changed or account removed/disabled.

extracted_elements:
  subject: "All CDE system components with vendor default accounts"
  condition: "Component has vendor-provided default credentials"
  obligation: "Default password changed per 8.3.6 OR account removed/disabled"
  evidence: "system_config.default_accounts_managed; no default credential in scan"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log: []
test_confidence: HIGH
generated_test: "tests/req2/test_2_2_secure_config.py"
```

---

## Generated tests

### `tests/req2/test_2_2_secure_config.py`

```python
"""
PCI DSS v4.0 Req 2.2 — Secure System Configuration
Confidence: HIGH for defaults/encryption; MEDIUM for hardening adequacy
"""
import pytest

PROHIBITED_ADMIN_PROTOCOLS = {"telnet", "http", "ftp", "snmpv1", "snmpv2c"}


def test_no_vendor_default_credentials(credential_audit_results):
    """2.2.2 — No vendor default credentials in use on CDE systems."""
    violations = [
        r for r in credential_audit_results
        if r.get("is_vendor_default") and r.get("in_cde")
    ]
    assert not violations, (
        f"VIOLATION (2.2.2): {len(violations)} CDE system(s) using vendor default "
        f"credentials:\n"
        + "\n".join(
            f"  {r['system_id']}: {r.get('account_id')} ({r.get('credential_type')})"
            for r in violations
        )
    )


def test_non_console_admin_access_encrypted(admin_access_configs):
    """2.2.7 — All non-console admin access must use strong encryption."""
    violations = [
        c for c in admin_access_configs
        if c.get("in_cde")
        and not c.get("is_console_access")
        and c.get("protocol", "").lower() in PROHIBITED_ADMIN_PROTOCOLS
    ]
    assert not violations, (
        f"VIOLATION (2.2.7): {len(violations)} non-console admin access configuration(s) "
        f"using unencrypted protocol:\n"
        + "\n".join(
            f"  {c['system_id']}: {c.get('protocol')}" for c in violations
        )
    )


def test_wireless_vendor_defaults_changed(wireless_configs):
    """2.3.1 — Wireless vendor defaults must be changed at installation."""
    violations = [
        w for w in wireless_configs
        if w.get("connected_to_cde")
        and not w.get("default_credentials_changed")
    ]
    assert not violations, (
        f"VIOLATION (2.3.1): {len(violations)} CDE-connected wireless network(s) with "
        f"unchanged vendor defaults: {[w['ssid'] for w in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-2-001",
    description=(
        "Unnecessary functionality: approved services/ports list per system class; "
        "running services compared quarterly; exceptions documented with justification."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_running_services_match_approved_list(system_service_audits):
    """2.2.3 — Only approved services should be running on CDE systems."""
    violations = []
    for audit in system_service_audits:
        if not audit.get("in_cde"):
            continue
        unapproved = [
            svc for svc in audit.get("running_services", [])
            if svc not in audit.get("approved_services", [])
            and not audit.get("exception_documented", {}).get(svc)
        ]
        if unapproved:
            violations.append(
                f"{audit['system_id']}: unapproved running services: {unapproved}"
            )
    assert not violations, (
        f"VIOLATION (2.2.3): {len(violations)} CDE system(s) with unapproved services "
        f"running:\n" + "\n".join(violations)
    )
```

---

## Notes for the registry

- **Default credentials are still the #1 entry vector:** Vendor default passwords on network devices, databases, web application servers, and IoT devices remain the most exploited misconfiguration in breach investigations. The test for default credentials should include: network device management interfaces, database superuser accounts (sa, root, postgres), web application admin accounts (admin/admin), and SNMP community strings.
- **Hardening benchmarks:** PCI DSS does not specify which hardening standard to use; CIS Benchmarks (Center for Internet Security) are the most commonly accepted by QSAs for Windows, Linux, Docker, Kubernetes, and major cloud platforms. DISA STIGs are acceptable for federal or defense environments. The chosen benchmark should be documented in the configuration management policy.
- **SSH hardening:** Even though SSH satisfies 2.2.7 (encrypted non-console access), the SSH configuration itself should be hardened: disable root login, disable password authentication (use keys or certificates), disable weak ciphers and MACs, limit source IPs where possible.
- **SNMPv1/v2c prohibition:** SNMPv1 and SNMPv2c transmit community strings in plaintext, making them equivalent to clear-text administrative access. 2.2.7 requires encrypted admin access, which SNMPv1/v2c violates. SNMPv3 with authPriv mode satisfies the encryption requirement.
- **Containers and cloud images:** Base container images and cloud AMIs frequently include default accounts, unnecessary services, and insecure default configurations. Include container base image review and cloud launch template review in the configuration hardening process.
