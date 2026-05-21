# SOC 2 TSC 2017 — CC6: Logical and Physical Access Controls

**Registry path:** `/regulation-registry/SOC2/CC6/`
**Version:** AICPA TSC 2017 (2022 points of focus updates)
**Last parsed:** 2026-05-20
**Applies to:** Service organizations (SaaS, cloud providers, data centers, managed-service providers) whose services are relevant to user-entity controls
**Trigger:** Customer contract requirement; investor due-diligence; voluntary for competitive positioning; required when customers request a SOC 2 Type I or Type II report from their auditor
**Jurisdiction:** United States (AICPA Trust Services Criteria); widely accepted internationally as equivalent to ISO 27001 attestation
**Not applicable to:** Internal IT departments; organizations that do not provide services to other companies; product companies without a service component
**Overall confidence:** HIGH — CC6 has the highest DETERMINISTIC density of any SOC 2 series; access provisioning, authentication thresholds, session timeout, TLS version, and AV deployment are all directly testable
**8 criteria: CC6.1–CC6.8**

---

## Scope summary

CC6 covers logical and physical access controls and is always in scope for any SOC 2 engagement (Security is the mandatory Trust Service Category). CC6 has the tightest alignment with PCI DSS Req 7–8 and ISO 27001 A.5.15–5.18/A.8.2–8.5. The 2022 points-of-focus updates added explicit references to multi-factor authentication, encryption in transit, and zero-trust principles, but the base criteria language remains from the 2017 edition.

CC6.1–CC6.3 and CC6.5 form the identity lifecycle cluster (provisioning, authentication, access removal). CC6.6–CC6.7 address boundary and transmission security. CC6.4 and CC6.8 address physical access and malware protection respectively.

---

## CC6.1 — Logical Access Security Software, Infrastructure, and Architectures (HIGH)

### Source excerpt

> The entity implements logical access security software, infrastructure, and architectures over protected information assets to protect them from security events to meet the entity's objectives related to availability, confidentiality, and privacy.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All information assets within SOC 2 system boundary | DETERMINISTIC |
| Obligation | Logical access controls implemented; least-privilege enforced; access authorized through formal process; access reviewed periodically | DETERMINISTIC (existence) / PARAMETERIZED (adequacy) |
| Evidence | `access_provisioning_records.authorization_documented`; `user_roles.least_privilege_applied == true`; `access_review_records.review_date` | DETERMINISTIC + PARAMETERIZED |

**Points of focus (2022):** Restricts logical access; identifies and authenticates users; considers network segmentation; manages points of access; authenticates external users; implements multi-factor authentication; authorizes access to security-sensitive data and functions.

**Assumption (ASSUME-SOC2-CC6-001):** Logical access controls are adequate when: (1) all user access is provisioned through a formal request-and-approval workflow with documented authorization; (2) access rights are based on least-privilege/need-to-know; (3) privileged access is assigned separately from standard user access; (4) access reviews conducted at least semi-annually for privileged users, annually for standard users; (5) MFA enforced for remote access and access to systems handling confidential data.

**Overall: DETERMINISTIC for access provisioning existence → Pattern 1; PARAMETERIZED for adequacy → Pattern 2**

---

## CC6.2 — User Authentication (HIGH)

### Source excerpt

> Prior to issuing system credentials and granting system access, the entity registers and authorizes new internal and external users whose access is administered by the entity.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All users of in-scope systems | DETERMINISTIC |
| Condition | Before system access is granted | DETERMINISTIC |
| Obligation | Identity verified before credentials issued; authorization documented; unique credentials per user; no shared accounts | DETERMINISTIC |
| Evidence | `user_account_records.identity_verified_before_access == true`; `user_accounts.shared_account_exists == false` | DETERMINISTIC |

**Assumption (ASSUME-SOC2-CC6-002):** Authentication controls are adequate when: (1) minimum password length ≥ 12 characters; (2) account lockout after ≤ 10 consecutive failed attempts; (3) idle session timeout ≤ 15 minutes for CDE systems and ≤ 30 minutes for other systems; (4) MFA required for all remote access, all privileged access, and all access to confidential data; (5) shared or generic accounts prohibited except for documented emergency break-glass procedures with individual accountability maintained through additional logging.

**Overall: DETERMINISTIC for unique IDs and pre-authorization → Pattern 1; PARAMETERIZED for threshold values → Pattern 2**

---

## CC6.3 — Access Authorization Removal — New Users and Departing Users (HIGH)

### Source excerpt

> The entity removes access to protected information assets when appropriate.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | Departing employees, contractors, and users with changed roles | DETERMINISTIC |
| Condition | On termination, role change, or other triggering event | DETERMINISTIC |
| Obligation | Access removed promptly; offboarding checklist completed; access removal verified | DETERMINISTIC |
| Evidence | `offboarding_records.access_revoked == true`; `offboarding_records.revocation_date` ≤ employment end date; no active accounts for terminated personnel | DETERMINISTIC |

**Assumption (ASSUME-SOC2-CC6-003):** Access removal is adequate when: (1) involuntary termination: access revoked same business day (for critical roles — same hour); (2) voluntary termination: access revoked by last working day at latest; (3) role change: excess access removed within 5 business days; (4) contractor/vendor: access expires with contract end date; (5) access removal verified — not just provisioning ticket closed but actual account status confirmed inactive; (6) quarterly review of all active accounts against current employee/contractor roster.

**Overall: DETERMINISTIC for access removal completeness → Pattern 1; PARAMETERIZED for timing → Pattern 2**

---

## CC6.4 — Physical Access Controls (MEDIUM)

### Source excerpt

> The entity restricts physical access to facilities and protected information assets to authorized personnel.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All facilities housing in-scope systems | DETERMINISTIC |
| Obligation | Physical access restricted; access controlled and logged; visitor procedures in place; physical access reviews conducted | DETERMINISTIC (existence) / PARAMETERIZED (coverage) |
| Evidence | `physical_access_logs.exists == true`; `access_control_system.badge_or_equivalent == true`; visitor logs | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-SOC2-CC6-004):** Physical access controls are adequate when: (1) all areas housing systems in SOC 2 scope require badge/key access, with access limited to authorized personnel; (2) access logs record entrant identity, date, and time; (3) visitor access requires escort; (4) physical access authorizations reviewed at least annually and immediately on termination; (5) data center/server room access separately controlled from general office access with restricted authorization list.

**Overall: PARAMETERIZED → Pattern 2; access log existence → Pattern 1**

---

## CC6.5 — Logical Access Removal (HIGH)

### Source excerpt

> The entity discontinues logical access to protected information assets when appropriate, including timely removal of access of individuals and teams from the entity's information assets.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Logical access removed upon termination; access removed within approved timeframe; removal verified; periodic user access reviews performed | DETERMINISTIC |
| Evidence | `terminated_users_with_active_accounts == []`; `access_review_records.last_review_date` within 6 months for privileged; annual for standard | DETERMINISTIC + PARAMETERIZED |

**Note:** CC6.5 is substantively identical to CC6.3 with the additional specification of periodic review. Both share ASSUME-SOC2-CC6-003 for timing. The distinction: CC6.3 addresses the individual deprovisioning event; CC6.5 addresses the detective control (periodic review catching missed deprovisionings).

**Overall: DETERMINISTIC → Pattern 1**

---

## CC6.6 — Boundary Protection Against External Threats (HIGH)

### Source excerpt

> The entity implements controls to prevent or detect and act upon the introduction of unauthorized or malicious software.

*Note: CC6.6 addresses logical network boundary protection; CC6.8 addresses malware specifically.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Network boundary controls implemented; inbound/outbound traffic restricted; intrusion detection or prevention system deployed; network segmentation applied | DETERMINISTIC (boundary controls existence) / PARAMETERIZED (rule adequacy) |
| Evidence | `network_security_controls.firewall_deployed == true`; `ids_ips.deployed == true`; network segmentation documented | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-SOC2-CC6-005):** Boundary protection is adequate when: (1) firewall or equivalent NSC deployed at all external ingress/egress points; (2) default deny-all inbound rule with explicit allowlist for required services; (3) DMZ architecture separates public-facing services from internal systems; (4) firewall rules reviewed at least semi-annually (aligns with PCI DSS Req 1.2.2 and ISO 27001 A.8.20); (5) IDS/IPS or equivalent monitoring deployed; (6) network segmentation isolates in-scope systems from non-scoped components.

**Overall: DETERMINISTIC for firewall existence → Pattern 1; PARAMETERIZED for rule adequacy → Pattern 2**

---

## CC6.7 — Data Transmission Protection (HIGH)

### Source excerpt

> The entity restricts the transmission, movement, and removal of information to authorized internal and external users and processes, and protects it during transmission, movement, or removal to meet the entity's objectives.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Confidential and sensitive data encrypted in transit; TLS 1.2 or higher enforced; weak cipher suites prohibited; transmission integrity protected | DETERMINISTIC |
| Evidence | `tls_configs.min_version >= "TLS_1_2"`; `prohibited_protocols.ssl_tls_10_11 == disabled`; AEAD cipher suites configured | DETERMINISTIC |

**Assumption (ASSUME-SOC2-CC6-006):** Transmission protection is adequate when: (1) TLS 1.2 minimum for all external communications; TLS 1.3 preferred; (2) SSL 3.0, TLS 1.0, TLS 1.1 disabled; (3) only AEAD cipher suites permitted (AES-GCM, CHACHA20-POLY1305); NULL, EXPORT, anon, RC4, DES, 3DES prohibited; (4) certificate validity checked; expired certificates = immediate finding; (5) internal system-to-system communication handling confidential data also encrypted. Aligns with PCI DSS ASSUME-4-001 and ISO 27001 ASSUME-ISO-A8-008.

**Overall: DETERMINISTIC → Pattern 1**

---

## CC6.8 — Prevention or Detection of Unauthorized Software (HIGH)

### Source excerpt

> The entity implements controls to prevent or detect and act upon the introduction of unauthorized or malicious software to meet the entity's objectives related to confidentiality, privacy and availability.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Malware protection deployed; definitions current; unauthorized software prevented or detected; endpoint controls in place | DETERMINISTIC (AV deployment) / PARAMETERIZED (coverage scope) |
| Evidence | `antivirus.deployed_on_all_applicable_systems == true`; `av_definitions.last_updated` ≤ 24 hours; `software_control.unauthorized_software_blocked or detected` | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-SOC2-CC6-007):** Anti-malware controls are adequate when: (1) AV/EDR deployed on all systems within SOC 2 boundary that run general-purpose operating systems; (2) definition updates automatic; currency ≤ 24 hours; (3) real-time on-access scanning enabled; (4) users cannot disable AV; (5) software allowlisting or application control for high-risk systems; (6) exceptions documented with compensating controls (equivalent to PCI DSS ASSUME-5-001 for non-general-purpose systems). Aligns with ISO 27001 ASSUME-ISO-A8-003.

**Overall: DETERMINISTIC for AV deployment and currency → Pattern 1; PARAMETERIZED for coverage scope → Pattern 2**

---

## YAML specifications

### `cc6_access_controls.yaml`

```yaml
regulation_id: SOC2-TSC2017-CC6
section: "SOC 2 TSC 2017 — CC6: Logical and Physical Access Controls"
r_or_a: Required
source_text: >
  The entity implements logical access security software, infrastructure, and
  architectures over protected information assets to protect them from security
  events to meet the entity's objectives.

extracted_elements:
  subject: "All systems and information assets within SOC 2 system boundary"
  condition: "System is within SOC 2 boundary; component_in_system_boundary() == true"
  obligation: "Access controlled; MFA enforced; TLS 1.2+; AV deployed; access reviews conducted"
  evidence: "access_records, auth_configs, tls_configs, av_status, offboarding_records"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: PARAMETERIZED
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-SOC2-CC6-001
    assumption_text: >
      Access provisioning: formal request-and-approval workflow; least-privilege;
      separate privileged accounts; semi-annual privileged review; annual standard review.
    assumed_by: "ISMS Manager"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
  - assumption_id: ASSUME-SOC2-CC6-002
    assumption_text: >
      Auth: ≥12 chars; lockout ≤10 attempts; idle timeout ≤15 min (CDE) / ≤30 min (other);
      MFA for remote/privileged/confidential access.
    assumed_by: "ISMS Manager"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
  - assumption_id: ASSUME-SOC2-CC6-003
    assumption_text: >
      Access removal: involuntary = same day; voluntary = last working day; role change ≤5 days;
      contractor = contract end; verified not just ticketed; quarterly roster review.
    assumed_by: "ISMS Manager"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
test_confidence: HIGH
generated_test: "tests/soc2/test_cc6_access_controls.py"
```

---

## Generated tests

### `tests/soc2/test_cc6_access_controls.py`

```python
"""
SOC 2 TSC 2017 — CC6: Logical and Physical Access Controls
Confidence: HIGH for CC6.2, CC6.3, CC6.5, CC6.7, CC6.8; MEDIUM for CC6.4
"""
import pytest
from datetime import date

PASSWORD_MIN_LENGTH = 12
MAX_FAILED_ATTEMPTS = 10
SESSION_TIMEOUT_SENSITIVE_MINUTES = 15
SESSION_TIMEOUT_STANDARD_MINUTES = 30
ACCESS_REVIEW_PRIVILEGED_MAX_DAYS = 180
ACCESS_REVIEW_STANDARD_MAX_DAYS = 365
TLS_MINIMUM_VERSION = "TLS_1_2"
AV_DEFINITION_MAX_AGE_HOURS = 24


def test_no_shared_accounts(user_accounts):
    """CC6.2 — Shared accounts prohibited (except documented break-glass)."""
    shared = [
        a for a in user_accounts
        if a.get("is_shared")
        and not a.get("break_glass_documented")
    ]
    assert not shared, (
        f"NONCONFORMITY (CC6.2): {len(shared)} shared account(s) without documented "
        f"break-glass authorization: {[a['account_id'] for a in shared]}"
    )


@pytest.mark.assumption(
    id="ASSUME-SOC2-CC6-002",
    description="Auth: ≥12 chars; lockout ≤10; idle timeout ≤15 min (sensitive) / ≤30 min (other); MFA for remote/privileged",
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_password_policy_minimum_thresholds(auth_system_configs):
    """CC6.2 — Password and authentication configuration must meet minimum thresholds."""
    violations = []
    for cfg in auth_system_configs:
        if not cfg.get("in_soc2_boundary"):
            continue
        issues = []
        if cfg.get("min_password_length", 0) < PASSWORD_MIN_LENGTH:
            issues.append(
                f"min length {cfg.get('min_password_length')} < {PASSWORD_MIN_LENGTH}"
            )
        if cfg.get("max_failed_attempts", 9999) > MAX_FAILED_ATTEMPTS:
            issues.append(
                f"lockout threshold {cfg.get('max_failed_attempts')} > {MAX_FAILED_ATTEMPTS}"
            )
        timeout = cfg.get("session_timeout_minutes", 9999)
        threshold = (
            SESSION_TIMEOUT_SENSITIVE_MINUTES
            if cfg.get("handles_confidential_data")
            else SESSION_TIMEOUT_STANDARD_MINUTES
        )
        if timeout > threshold:
            issues.append(f"session timeout {timeout} min > {threshold}")
        if issues:
            violations.append(f"System {cfg['system_id']}: {'; '.join(issues)}")
    assert not violations, (
        f"NONCONFORMITY (CC6.2): {len(violations)} system(s) not meeting authentication "
        f"thresholds:\n" + "\n".join(violations)
    )


def test_mfa_enforced_for_remote_and_privileged_access(user_accounts):
    """CC6.2 — MFA required for remote access and privileged accounts."""
    violations = [
        a for a in user_accounts
        if a.get("in_soc2_boundary")
        and (a.get("is_privileged") or a.get("has_remote_access"))
        and not a.get("mfa_enrolled")
    ]
    assert not violations, (
        f"NONCONFORMITY (CC6.2): {len(violations)} privileged/remote-access account(s) "
        f"without MFA: {[a['account_id'] for a in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-SOC2-CC6-003",
    description="Involuntary termination = same-day revocation; voluntary = last working day; verified not just ticketed",
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_no_active_accounts_for_terminated_personnel(user_accounts, terminated_personnel):
    """CC6.3/CC6.5 — Terminated personnel must have no active accounts."""
    terminated_ids = {p["employee_id"] for p in terminated_personnel}
    violations = [
        a for a in user_accounts
        if a.get("employee_id") in terminated_ids
        and a.get("account_status") == "active"
    ]
    assert not violations, (
        f"NONCONFORMITY (CC6.3/CC6.5): {len(violations)} active account(s) belonging "
        f"to terminated personnel: {[a['account_id'] for a in violations]}"
    )


def test_privileged_access_reviewed_within_6_months(access_review_records):
    """CC6.1/CC6.5 — Privileged access reviewed at least every 6 months."""
    today = date.today()
    privileged_reviews = [
        r for r in access_review_records
        if r.get("access_type") == "privileged"
    ]
    if not privileged_reviews:
        assert False, (
            "NONCONFORMITY (CC6.1): No privileged access review records found"
        )
    latest = max(privileged_reviews, key=lambda r: r["review_date"])
    days_since = (today - latest["review_date"]).days
    assert days_since <= ACCESS_REVIEW_PRIVILEGED_MAX_DAYS, (
        f"NONCONFORMITY (CC6.1): Privileged access last reviewed {days_since} days ago "
        f"(max {ACCESS_REVIEW_PRIVILEGED_MAX_DAYS})"
    )


def test_tls_minimum_version_enforced(tls_endpoint_configs):
    """CC6.7 — TLS 1.2 minimum on all in-scope external endpoints."""
    PROHIBITED_PROTOCOLS = {"SSL_3_0", "TLS_1_0", "TLS_1_1", "SSL_2_0"}
    violations = []
    for cfg in tls_endpoint_configs:
        if not cfg.get("in_soc2_boundary"):
            continue
        enabled = set(cfg.get("enabled_protocols", []))
        prohibited_enabled = enabled & PROHIBITED_PROTOCOLS
        if prohibited_enabled:
            violations.append(
                f"Endpoint {cfg['endpoint_id']}: prohibited protocols enabled: "
                f"{prohibited_enabled}"
            )
    assert not violations, (
        f"NONCONFORMITY (CC6.7): {len(violations)} endpoint(s) with prohibited TLS "
        f"versions:\n" + "\n".join(violations)
    )


@pytest.mark.assumption(
    id="ASSUME-SOC2-CC6-006",
    description="TLS 1.2+ min; AEAD only; NULL/EXPORT/RC4/DES/3DES prohibited; internal confidential comms also encrypted",
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_weak_cipher_suites_disabled(tls_endpoint_configs):
    """CC6.7 — Weak cipher suites must be disabled on all in-scope endpoints."""
    PROHIBITED_CIPHERS = {
        "NULL", "EXPORT", "ADH", "AECDH", "RC4", "DES", "3DES",
        "RC2", "MD5", "ANON"
    }
    violations = []
    for cfg in tls_endpoint_configs:
        if not cfg.get("in_soc2_boundary"):
            continue
        enabled_ciphers = set(cfg.get("enabled_cipher_suites", []))
        prohibited = {
            c for c in enabled_ciphers
            if any(p in c.upper() for p in PROHIBITED_CIPHERS)
        }
        if prohibited:
            violations.append(
                f"Endpoint {cfg['endpoint_id']}: prohibited ciphers: {prohibited}"
            )
    assert not violations, (
        f"NONCONFORMITY (CC6.7): {len(violations)} endpoint(s) with weak cipher "
        f"suites:\n" + "\n".join(violations)
    )


@pytest.mark.assumption(
    id="ASSUME-SOC2-CC6-007",
    description="AV on all general-purpose OS in boundary; 24-hour definition currency; real-time scanning; users cannot disable",
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_antivirus_deployed_and_current(endpoint_security_status):
    """CC6.8 — AV/EDR must be deployed and definitions current (≤24 hours)."""
    today = date.today()
    violations = []
    for endpoint in endpoint_security_status:
        if not endpoint.get("in_soc2_boundary") or not endpoint.get("general_purpose_os"):
            continue
        if not endpoint.get("av_deployed"):
            violations.append(f"{endpoint['asset_id']}: no AV deployed")
            continue
        last_update = endpoint.get("av_definition_update_date")
        if last_update is None:
            violations.append(f"{endpoint['asset_id']}: no AV definition update date recorded")
        elif (today - last_update).days > 1:
            violations.append(
                f"{endpoint['asset_id']}: AV definitions {(today - last_update).days} "
                f"day(s) old (max 1)"
            )
    assert not violations, (
        f"NONCONFORMITY (CC6.8): {len(violations)} endpoint(s) with AV issues:\n"
        + "\n".join(violations)
    )


def test_physical_access_logs_exist_for_soc2_facilities(physical_access_records):
    """CC6.4 — Physical access to SOC 2 system facilities must be logged."""
    soc2_logs = [
        r for r in physical_access_records
        if r.get("facility_in_soc2_boundary")
    ]
    assert soc2_logs, (
        "NONCONFORMITY (CC6.4): No physical access logs found for facilities within "
        "SOC 2 system boundary"
    )
```

---

## Notes for the registry

- **CC6.3 vs. CC6.5 distinction:** CC6.3 is the preventive control (formal deprovisioning on trigger events); CC6.5 is the detective control (periodic reviews catching missed deprovisionings). A single SOC 2 engagement tests both: event-driven revocations for the period under review AND evidence of periodic user access reviews.
- **MFA as a 2022 points-of-focus emphasis:** The 2022 points-of-focus update explicitly called out MFA as a key mechanism for CC6.1 and CC6.2. Before this update, MFA was implied; after it, auditors specifically look for MFA evidence for remote access and privileged accounts.
- **CC6.6 vs. PCI DSS NSC alignment:** The SOC 2 CC6.6 firewall review requirement is less prescriptive than PCI DSS Req 1.2.2 (explicit 6-month review). ASSUME-SOC2-CC6-005 borrows the PCI threshold to make the test DETERMINISTIC. Organizations subject to both can use one semi-annual review to satisfy both.
- **CC6.7 and internal traffic:** The CC6.7 criteria addresses "transmission" broadly, which includes internal system-to-system communication. Many organizations secure external traffic but transmit internal data unencrypted. ASSUME-SOC2-CC6-006 extends the requirement to internal confidential data transmission.
- **Period evidence for Type II:** For a 12-month Type II engagement, access review records must span the full audit period. A single access review done at the end of the period does not satisfy CC6.1 or CC6.5 for the earlier months. Evidence should show access reviews were performed throughout the period.
