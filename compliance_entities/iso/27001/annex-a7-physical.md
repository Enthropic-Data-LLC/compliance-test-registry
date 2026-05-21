# ISO/IEC 27001:2022 — Annex A Theme 3: Physical Controls (A.7.x)

**Registry path:** `/regulation-registry/ISO-27001/Annex-A7/`
**Version:** ISO/IEC 27001:2022
**Last parsed:** 2026-05-20
**Applies to:** Any organization seeking ISO/IEC 27001 certification for its Information Security Management System (ISMS); scope is organization-defined (can be a department, product line, or whole entity)
**Trigger:** Voluntary certification; customer or procurement requirement (especially in EU, UK, financial services); NIS2 Directive in EU references ISO 27001 as an acceptable framework; organizational risk management decision
**Jurisdiction:** Global — ISO/IEC international standard recognized worldwide; certifying bodies accredited per ISO/IEC 17021-1
**Not applicable to:** Mandatory compliance in isolation — ISO 27001 is a voluntary standard with no direct regulatory enforcement; certification applies only to the defined ISMS scope; does not replace sector-specific mandatory frameworks (HIPAA, PCI DSS, GLBA, etc.)
**Overall confidence:** MEDIUM overall — A.7.7 (clear desk/screen) and A.7.11 (supporting utilities) have DETERMINISTIC elements; most physical controls are PARAMETERIZED because physical environment adequacy requires on-site assessment
**14 controls: A.7.1–A.7.14**

---

## Scope summary

Theme 3 (Physical Controls) was reorganized from ISO 27001:2013 Clause A.11 (Physical and Environmental Security). The 2022 edition introduced A.7.4 (Physical Security Monitoring) as a new standalone control — previously implied under physical entry controls. A.7.9 (Security of Assets Off-Premises) was elevated from 2013 guidance to a standalone control, reflecting the proliferation of remote work and mobile assets.

Physical controls present a fundamental documentation-versus-reality challenge: paper compliance (policies, procedures) can be assessed programmatically, but the adequacy of the physical implementation — perimeter strength, CCTV coverage, badge reader placement — requires on-site evaluation. Tests in this section primarily verify that documentation and records exist; physical adequacy is CONTESTED territory requiring auditor walkthrough.

---

## A.7.1 — Physical Security Perimeters (MEDIUM)

### Source excerpt

> Security perimeters shall be defined and used to protect areas that contain information and other associated assets.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All areas containing information assets within ISMS scope | DETERMINISTIC |
| Obligation | Physical security perimeters defined and documented; perimeter controls implemented commensurate with risk | DETERMINISTIC (existence) / PARAMETERIZED (adequacy) |
| Evidence | `physical_security_policy.perimeters_defined == true`; perimeter control implementation records; security areas documented with boundaries | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-A7-001):** Physical security perimeters are adequate when: (1) security areas are documented with defined boundaries; (2) entry points to security areas are controlled and logged; (3) walls, locked doors, or equivalent barriers exist between public areas and areas containing sensitive information; (4) the organization's own risk assessment determines the tier of perimeter controls (single locked door may suffice for low-risk; mantrap, CCTV, and security desk required for high-risk); (5) server rooms and areas housing core IT infrastructure are within a defined secure perimeter with access restricted to authorized personnel only.

**Overall: PARAMETERIZED for adequacy → Pattern 2; DETERMINISTIC for existence of documentation → Pattern 1**

---

## A.7.2 — Physical Entry (MEDIUM)

### Source excerpt

> Secure areas shall be protected by appropriate entry controls and access points.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Entry controls restrict access to secure areas to authorized personnel only; access attempts logged; tailgating controls in place for high-sensitivity areas | PARAMETERIZED |
| Evidence | `physical_access_control.entry_log_exists == true`; `access_authorization_records`; entry events logged with identity and timestamp | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-A7-002):** Physical entry controls are adequate when: (1) all secure areas have access logs recording who entered and when; (2) access authorizations are maintained and reviewed at least annually (or immediately upon role change or termination); (3) terminated personnel's physical access credentials are revoked on the same schedule as logical access (ASSUME-ISO-A6-004: involuntary — same day; voluntary — last day); (4) visitor access to secure areas requires escort by authorized personnel; (5) server rooms require at minimum locked door with key/badge, logged access.

**Overall: PARAMETERIZED → Pattern 2; access log existence → Pattern 1**

---

## A.7.3 — Securing Offices, Rooms, and Facilities (PARAMETERIZED)

### Source excerpt

> Physical security for offices, rooms and facilities shall be designed and implemented.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Office security design documented and implemented; offices containing sensitive processing protected against unauthorized access | PARAMETERIZED |
| Evidence | `facility_security_assessment.completed == true`; security measures documented per location | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## A.7.4 — Physical Security Monitoring *(new in 2022)* (PARAMETERIZED)

### Source excerpt

> Premises shall be continually monitored for unauthorized physical access.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Monitoring system in place for unauthorized physical access; monitoring covers sensitive areas; alerts reviewed promptly | PARAMETERIZED |
| Evidence | `physical_monitoring.system_deployed == true`; CCTV or equivalent covering secure area entry points; monitoring alert procedures documented | PARAMETERIZED |

**Assumption (ASSUME-ISO-A7-003):** Physical monitoring is adequate when: (1) CCTV or equivalent monitoring covers all entry points to secure areas (server room, data center, areas with sensitive information); (2) monitoring footage/alerts are reviewed — automated intrusion detection alerts reviewed immediately; recorded footage retained for at least 30 days (90 days for high-security); (3) monitoring system itself is protected from tampering; (4) areas with sensitive information have monitoring that cannot be bypassed or easily disabled by a single individual.

**Overall: PARAMETERIZED → Pattern 2**

---

## A.7.5 — Protecting Against Physical and Environmental Threats (PARAMETERIZED)

### Source excerpt

> Protection against physical and environmental threats, such as natural disasters, malicious attack or accidents shall be designed and applied to secure areas.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Physical and environmental threats identified; protection measures implemented commensurate with threat level | PARAMETERIZED |
| Evidence | `environmental_threat_assessment.completed == true`; protection measures documented (fire suppression, flood detection, temperature/humidity monitoring) | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## A.7.6 — Working in Secure Areas (MEDIUM)

### Source excerpt

> Security measures for working in secure areas shall be designed and applied.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Procedures for working in secure areas documented; need-to-know enforced; unsupervised working in secure areas restricted | PARAMETERIZED |
| Evidence | `secure_area_working_procedures.documented == true`; procedure awareness training records | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## A.7.7 — Clear Desk and Clear Screen (DETERMINISTIC for policy existence)

### Source excerpt

> Clear desk rules for papers and removable storage media and clear screen rules for information processing facilities shall be defined and appropriately enforced.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Clear desk policy documented and communicated; clear screen policy documented; enforcement mechanism in place | DETERMINISTIC (policy existence) / PARAMETERIZED (enforcement adequacy) |
| Evidence | `clear_desk_policy.documented == true`; `screen_lock_auto_timeout_configured == true`; session timeout ≤ org-defined threshold (ASSUME-ISO-A5-004: ≤ 30 minutes) | DETERMINISTIC |

**Assumption (ASSUME-ISO-A7-004):** Clear desk/screen policy is adequate when: (1) clear desk policy requires removal of sensitive materials from workstations when unattended; (2) screens auto-lock after ≤ 30 minutes of inactivity (consistent with ASSUME-ISO-A5-004); (3) physical keys or card-access locks for cabinets storing sensitive printed materials; (4) policy communicated to all workers within ISMS scope; (5) removable media not left unattended in workstations. Enforcement: periodic spot checks or clean desk audits documented.

**Overall: DETERMINISTIC for policy and screen lock existence → Pattern 1; PARAMETERIZED for enforcement → Pattern 2**

---

## A.7.8 — Equipment Siting and Protection (PARAMETERIZED)

### Source excerpt

> Equipment shall be sited and protected to reduce the risks from physical and environmental threats, and from unauthorized access.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Equipment placement considers physical and environmental threats; sensitive equipment not in publicly accessible areas | PARAMETERIZED |
| Evidence | `equipment_placement_policy.documented == true`; servers not accessible to public; UPS and environmental monitoring in place | PARAMETERIZED |

**Overall: PARAMETERIZED → Pattern 2**

---

## A.7.9 — Security of Assets Off-Premises *(elevated to standalone in 2022)* (PARAMETERIZED)

### Source excerpt

> Off-site assets shall be protected, taking into account the different risks of working outside the organization's premises.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Off-premises asset security policy documented; assets tracked when taken off-site; appropriate controls for mobile/remote use | PARAMETERIZED |
| Evidence | `off_premises_asset_policy.documented == true`; asset tracking or declaration records for equipment taken off-site | PARAMETERIZED |

**Assumption (ASSUME-ISO-A7-005):** Off-premises asset security is adequate when: (1) policy exists governing use of organizational assets outside organizational premises; (2) assets taken off-site are recorded or declared (asset loan register); (3) portable devices (laptops, USB drives) require encryption when used or stored off-premises; (4) loss or theft of off-premises assets must be reported immediately as an IS event; (5) assets not authorized for off-premises use (e.g., physical backup media) have technical or procedural controls preventing removal from secure areas. Aligns with ASSUME-ISO-A6-005 (remote working controls).

**Overall: PARAMETERIZED → Pattern 2**

---

## A.7.10 — Storage Media (MEDIUM)

### Source excerpt

> Storage media shall be managed through their life cycle of acquisition, use, transportation and disposal in accordance with the organization's classification scheme and handling requirements.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Storage media lifecycle managed; transportation protected; disposal uses secure sanitization methods | PARAMETERIZED (lifecycle) / DETERMINISTIC (disposal method existence) |
| Evidence | `media_handling_policy.documented == true`; `media_disposal_records.sanitization_method_documented`; secure transport records for sensitive media | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-A7-006):** Storage media controls are adequate when: (1) media containing sensitive/classified information is labeled per classification scheme; (2) physical transport of removable media uses tamper-evident packaging or encrypted media only; (3) disposal: overwrite (≥ 3 passes DoD 5220.22-M or equivalent), degaussing, physical destruction (shredding to ≤ 2mm particles or incineration) — see HIPAA A.310 disposal alignment and PCI DSS 9.4.6; (4) disposal certificates documented for all media destroyed; (5) media inventory tracked so all media is accounted for.

**Overall: PARAMETERIZED for lifecycle → Pattern 2; DETERMINISTIC for disposal documentation → Pattern 1**

---

## A.7.11 — Supporting Utilities (DETERMINISTIC for existence)

### Source excerpt

> Information processing facilities shall be protected from power failures and other disruptions caused by failures in supporting utilities.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | UPS in place for critical systems; generator or equivalent for prolonged outages; temperature and humidity monitoring; redundant utilities where risk warrants | DETERMINISTIC (UPS existence for critical systems) / PARAMETERIZED (capacity adequacy) |
| Evidence | `ups_deployed_on_critical_systems == true`; `temperature_monitoring.deployed == true`; UPS test records; generator test records | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-A7-007):** Supporting utility controls are adequate when: (1) UPS provides at minimum 30-minute runtime for controlled shutdown of critical systems (or longer if RPO requires); (2) UPS tested under load at least annually; (3) temperature in server rooms maintained between 18°C–27°C (64°F–81°F) with automated alerting outside range; (4) humidity maintained 45–65% RH; (5) environmental monitoring alerts route to on-call personnel 24/7; (6) generator capacity and fuel supply sufficient for RTO if extended power outage is in threat model.

**Overall: DETERMINISTIC for UPS and temperature monitoring existence → Pattern 1; PARAMETERIZED for capacity → Pattern 2**

---

## A.7.12 — Cabling Security (DETERMINISTIC for existence of controls)

### Source excerpt

> Cables carrying power or data shall be protected from interception, interference or damage.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Power and data cables protected; cable runs documented; cables in publicly accessible areas protected from interference | DETERMINISTIC (documentation existence) / PARAMETERIZED (adequacy of protection) |
| Evidence | `cable_routing_documented == true`; cable runs in raised floors, conduits, or equivalent; cable labeling in place | DETERMINISTIC + PARAMETERIZED |

**Overall: PARAMETERIZED for adequacy → Pattern 2; DETERMINISTIC for documentation → Pattern 1**

---

## A.7.13 — Equipment Maintenance (MEDIUM)

### Source excerpt

> Equipment shall be maintained correctly to ensure continued availability and integrity of information.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | Equipment maintenance performed per manufacturer schedule; maintenance records kept; maintenance by authorized personnel only | PARAMETERIZED |
| Evidence | `equipment_maintenance_records.exists == true`; maintenance performed within vendor-recommended intervals; vendor or authorized maintainer identity logged | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-A7-008):** Equipment maintenance is adequate when: (1) scheduled maintenance performed per manufacturer specifications or industry standards; (2) maintenance records document: asset ID, date, maintenance performed, technician identity; (3) maintenance access by third-party vendors is supervised or access is limited to the specific equipment requiring maintenance; (4) data storage media removed or sanitized before equipment goes to external maintenance.

**Overall: PARAMETERIZED → Pattern 2**

---

## A.7.14 — Secure Disposal or Re-Use of Equipment (MEDIUM)

### Source excerpt

> Items of equipment containing storage media shall be verified to ensure that any sensitive data and licensed software has been removed or securely overwritten prior to disposal or re-use.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Obligation | All equipment with storage media verified sanitized before disposal or re-use; sanitization method documented; certificates issued | DETERMINISTIC (existence of sanitization check) / PARAMETERIZED (method adequacy) |
| Evidence | `equipment_disposal_checklist.sanitization_verified == true`; `disposal_certificate.exists == true`; sanitization method documented per ASSUME-ISO-A7-006 | DETERMINISTIC + PARAMETERIZED |

**Assumption (ASSUME-ISO-A7-009):** Equipment disposal is adequate when: (1) all storage media (HDD, SSD, flash) verified sanitized before disposal — media overwrite (NIST SP 800-88 Clear or Purge), degaussing, or physical destruction; (2) SSD-specific: overwrite alone is insufficient due to wear-leveling; physical destruction or ATA Secure Erase / vendor sanitization tool required; (3) disposal certificate documents: asset ID, sanitization method, date, responsible party; (4) certificate retained for at least the period until the next information security audit; (5) "re-use within organization" does not skip sanitization if the equipment moves to a lower-trust environment.

**Cross-reference:** Aligns with HIPAA §164.310(d)(2)(i) (Media Disposal — Required); PCI DSS Req 9.4.6 (hard-copy CHD destruction); ASSUME-ISO-A7-006 (media disposal methods).

**Overall: DETERMINISTIC for sanitization check existence → Pattern 1; PARAMETERIZED for method adequacy → Pattern 2**

---

## YAML specifications

### `a7_equipment_disposal.yaml`

```yaml
regulation_id: ISO-27001-2022-A.7.14
section: "ISO 27001:2022 Annex A — Secure Disposal or Re-Use of Equipment"
r_or_a: Required
source_text: >
  Items of equipment containing storage media shall be verified to ensure
  that any sensitive data and licensed software has been removed or securely
  overwritten prior to disposal or re-use.

extracted_elements:
  subject: "All equipment within ISMS scope with storage media"
  condition: "Equipment scheduled for disposal or re-use"
  obligation: "Sanitization verified; method documented; certificate issued"
  evidence: "equipment_disposal_records: asset_id, sanitization_method, date, certificate"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-ISO-A7-009
    assumption_text: >
      NIST SP 800-88 Clear/Purge for HDD; physical destruction or ATA Secure Erase
      for SSD; disposal certificate retained until next audit; sanitization required
      even for internal re-use to lower-trust environments.
    assumed_by: "ISMS Manager"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
    cryptographic_hash: "sha256:pending-ci"
test_confidence: HIGH
generated_test: "tests/iso27001/test_a7_physical.py"
```

### `a7_supporting_utilities.yaml`

```yaml
regulation_id: ISO-27001-2022-A.7.11
section: "ISO 27001:2022 Annex A — Supporting Utilities"
r_or_a: Required
source_text: >
  Information processing facilities shall be protected from power failures
  and other disruptions caused by failures in supporting utilities.

extracted_elements:
  subject: "Critical information processing facilities"
  condition: "UPS and environmental monitoring present"
  obligation: "UPS deployed; temperature monitoring deployed; tests conducted"
  evidence: "infrastructure_records: ups_deployed, temp_monitoring, test_dates"

ambiguity_classification:
  subject: PARAMETERIZED
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-ISO-A7-007
    assumption_text: >
      UPS: min 30-min runtime; annual load test; temperature 18–27°C; humidity 45–65% RH;
      automated alerting; 24/7 on-call routing.
    assumed_by: "ISMS Manager"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
    cryptographic_hash: "sha256:pending-ci"
test_confidence: HIGH
generated_test: "tests/iso27001/test_a7_physical.py"
```

---

## Generated tests

### `tests/iso27001/test_a7_physical.py`

```python
"""
ISO 27001:2022 Annex A Theme 3 — Physical Controls
Confidence: HIGH for A.7.7 and A.7.14 (existence checks); MEDIUM for others
"""
import pytest
from datetime import date

SCREEN_LOCK_MAX_MINUTES = 30
UPS_TEST_MAX_DAYS = 365
MEDIA_DISPOSAL_CERT_REQUIRED = True


def test_clear_screen_timeout_configured(auth_system_configs):
    """A.7.7 — Screen lock must activate within 30 minutes for all ISMS-scope systems."""
    violations = []
    for cfg in auth_system_configs:
        if not cfg.get("in_isms_scope"):
            continue
        timeout = cfg.get("session_timeout_minutes")
        if timeout is None or timeout > SCREEN_LOCK_MAX_MINUTES:
            violations.append(
                f"System {cfg['system_id']}: session timeout "
                f"{timeout} min (max {SCREEN_LOCK_MAX_MINUTES})"
            )
    assert not violations, (
        f"NONCONFORMITY (A.7.7): {len(violations)} system(s) with screen lock "
        f"exceeding {SCREEN_LOCK_MAX_MINUTES} minutes:\n" + "\n".join(violations)
    )


def test_clear_desk_policy_exists(physical_security_policies):
    """A.7.7 — Clear desk policy must be documented."""
    clear_desk = [
        p for p in physical_security_policies
        if p.get("policy_type") == "clear_desk"
    ]
    assert clear_desk, (
        "NONCONFORMITY (A.7.7): No clear desk policy found — clear desk/screen "
        "policy is required for all ISMS-scope workplaces"
    )
    latest = max(clear_desk, key=lambda p: p.get("last_reviewed_date", date.min))
    assert latest.get("communicated_to_all_staff"), (
        "NONCONFORMITY (A.7.7): Clear desk policy not confirmed communicated to all staff"
    )


@pytest.mark.assumption(
    id="ASSUME-ISO-A7-007",
    description=(
        "UPS: min 30-min runtime; annual load test; temperature 18–27°C; "
        "humidity 45–65% RH; automated alerting."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_ups_deployed_on_critical_systems(infrastructure_records):
    """A.7.11 — UPS must be deployed on all critical information processing facilities."""
    critical = [r for r in infrastructure_records if r.get("is_critical_processing")]
    if not critical:
        pytest.skip("No critical processing facilities in infrastructure records")
    no_ups = [r for r in critical if not r.get("ups_deployed")]
    assert not no_ups, (
        f"NONCONFORMITY (A.7.11): {len(no_ups)} critical system(s) without UPS: "
        f"{[r['asset_id'] for r in no_ups]}"
    )


def test_ups_tested_within_12_months(infrastructure_records):
    """A.7.11 — UPS load tests must be conducted annually."""
    today = date.today()
    violations = []
    for r in infrastructure_records:
        if not r.get("ups_deployed"):
            continue
        last_test = r.get("ups_last_test_date")
        if last_test is None:
            violations.append(f"{r['asset_id']}: no UPS test on record")
        elif (today - last_test).days > UPS_TEST_MAX_DAYS:
            violations.append(
                f"{r['asset_id']}: UPS last tested {(today - last_test).days} days ago"
            )
    assert not violations, (
        f"NONCONFORMITY (A.7.11): {len(violations)} UPS(es) overdue for testing:\n"
        + "\n".join(violations)
    )


def test_temperature_monitoring_deployed(infrastructure_records):
    """A.7.11 — Temperature monitoring required in server rooms."""
    server_rooms = [
        r for r in infrastructure_records
        if r.get("location_type") == "server_room"
    ]
    if not server_rooms:
        pytest.skip("No server rooms in infrastructure records")
    no_temp_monitor = [
        r for r in server_rooms
        if not r.get("temperature_monitoring_deployed")
    ]
    assert not no_temp_monitor, (
        f"NONCONFORMITY (A.7.11): {len(no_temp_monitor)} server room(s) without "
        f"temperature monitoring: {[r['asset_id'] for r in no_temp_monitor]}"
    )


@pytest.mark.assumption(
    id="ASSUME-ISO-A7-009",
    description=(
        "Disposal: NIST SP 800-88 Clear/Purge for HDD; physical destruction or "
        "ATA Secure Erase for SSD; certificate retained until next audit."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_equipment_disposal_has_sanitization_certificate(equipment_disposal_records):
    """A.7.14 — All disposed equipment must have documented sanitization."""
    violations = [
        r for r in equipment_disposal_records
        if not r.get("sanitization_verified")
        or not r.get("disposal_certificate_issued")
    ]
    assert not violations, (
        f"NONCONFORMITY (A.7.14): {len(violations)} equipment disposal record(s) "
        f"without verified sanitization or certificate: "
        f"{[r.get('asset_id') for r in violations]}"
    )


def test_equipment_disposal_method_documented(equipment_disposal_records):
    """A.7.14 — Sanitization method must be explicitly documented for each disposal."""
    violations = [
        r for r in equipment_disposal_records
        if not r.get("sanitization_method")
    ]
    assert not violations, (
        f"NONCONFORMITY (A.7.14): {len(violations)} disposal record(s) without "
        f"documented sanitization method: {[r.get('asset_id') for r in violations]}"
    )


def test_physical_access_logs_exist(physical_access_records):
    """A.7.2 — Physical access to secure areas must be logged."""
    secure_area_logs = [
        r for r in physical_access_records
        if r.get("area_type") in ("server_room", "secure_area", "data_center")
    ]
    assert secure_area_logs, (
        "NONCONFORMITY (A.7.2): No physical access logs found for secure areas — "
        "logged entry control is required for all secure areas"
    )


def test_physical_access_revoked_on_termination(offboarding_records, physical_access_records):
    """A.7.2 — Physical access must be revoked on termination (consistent with A.6.5)."""
    terminated_ids = {
        r["employee_id"] for r in offboarding_records
    }
    active_physical_access = {
        r["employee_id"] for r in physical_access_records
        if r.get("access_status") == "active"
    }
    violations = terminated_ids & active_physical_access
    assert not violations, (
        f"NONCONFORMITY (A.7.2/A.6.5): {len(violations)} terminated personnel "
        f"still have active physical access records: {violations}"
    )
```

---

## Notes for the registry

- **Physical assessment limitation:** The tests above verify documentation and records exist. Physical adequacy — whether the door is sturdy enough, whether CCTV actually covers blind spots, whether the server room truly prevents tailgating — requires on-site assessment by a qualified auditor. All physical tests are Pattern 1 or Pattern 2; none provide assurance equivalent to a physical inspection.
- **A.7.4 (physical monitoring) — new 2022:** Prior to 2022, physical monitoring was expected but not explicitly required as a standalone control. A.7.4 formalizes the requirement for continuous monitoring of premises. Organizations that previously treated CCTV as optional should assess their implementation against A.7.4 explicitly.
- **A.7.9 (off-premises) — elevated 2022:** A.7.9 was elevated from 2013 guidance text to a standalone control, reflecting the normalization of remote work. Organizations with significant remote workforces need explicit off-premises asset controls — tracking, encryption requirements, loss reporting — not just a general remote working policy (A.6.7).
- **A.7.14 SSD disposal gap:** Standard magnetic overwrite tools do not reliably sanitize SSDs due to wear-leveling and over-provisioning. NIST SP 800-88 explicitly distinguishes between Clear (overwrite, sufficient for HDD) and Purge (ATA Secure Erase or equivalent, required for flash storage). Many organizations' disposal procedures predate SSD adoption and may incorrectly apply HDD methods to SSD assets.
- **A.7.11 vs. SOC 2 Availability (A1):** Supporting utilities controls overlap with SOC 2 Availability criteria. Organizations pursuing both certifications can use a single infrastructure evidence set (UPS tests, temperature logs, environmental alerts) to satisfy both, but the SOC 2 evidence must be scoped to the systems relevant to service commitments.
- **Physical access revocation cross-reference:** A.7.2 (physical entry) and A.6.5 (termination) both address access revocation. The test `test_physical_access_revoked_on_termination` enforces both controls. ASSUME-ISO-A6-004 (same-day for involuntary, last day for voluntary) applies to both logical and physical access.
