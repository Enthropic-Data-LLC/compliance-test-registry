# Requirement 6 — Develop and Maintain Secure Systems and Software

**Registry path:** `/regulation-registry/PCI-DSS/Req-6/`
**Version:** PCI DSS v4.0 (mandatory since March 31, 2025)
**Last parsed:** 2026-05-20
**Overall confidence:** MEDIUM — patch SLAs are DETERMINISTIC; criticality classification and secure coding adequacy are PARAMETERIZED
**R = Required**

---

## Scope summary

Req 6 covers two distinct domains: (1) patch management for commercial and open-source software, and (2) secure software development lifecycle (SDLC) for bespoke/custom code. The patch SLAs (1 month critical, 3 months non-critical) are DETERMINISTIC. Secure coding standards and vulnerability classification are PARAMETERIZED because the regulation references "industry best practices" without mandating specific tools or methodologies.

v4.0 added significant SDLC requirements including mandatory developer training, code review for bespoke software, and WAF requirements for public-facing web applications.

---

## 6.3.3 — Patch Management SLAs (R — DETERMINISTIC)

### Source excerpt

> *6.3.3 — All system components are protected from known vulnerabilities by installing applicable security patches/updates as follows: Critical or high-security patches/updates are installed within one month of release. All applicable security patches/updates are installed within three months of release.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All CDE system components | DETERMINISTIC |
| Condition | Security patch or update released | DETERMINISTIC |
| Obligation | Critical/high patches installed ≤ 30 days from release; all other security patches ≤ 90 days | DETERMINISTIC |
| Evidence | `patch_records.patch_id`, `patch_records.release_date`, `patch_records.install_date`; gap ≤ 30 or 90 days based on `criticality` | DETERMINISTIC |

**Assumption (ASSUME-6-001):** Patch criticality classification: "critical" and "high" are defined by the vendor or the CVSS base score — CVSS ≥ 7.0 is treated as "high or critical" (30-day SLA); CVSS < 7.0 is "non-critical" (90-day SLA). Where vendor severity ratings and CVSS scores conflict, the stricter (shorter SLA) classification governs. Zero-day patches are critical by definition regardless of CVSS score.

**Overall: DETERMINISTIC for timing → Pattern 1; PARAMETERIZED for criticality classification → Pattern 2**

---

## 6.2.2 — Secure Coding Training (R — DETERMINISTIC)

### Source excerpt

> *6.2.2 — Software development personnel working on bespoke and custom software are trained at least once every 12 months as follows: On preventing common software vulnerabilities. Relevant to their development languages and environments. On current threats and vulnerabilities applicable to the entity's technology.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All software developers working on in-scope bespoke/custom code | DETERMINISTIC |
| Condition | Personnel write code for CDE-related software | DETERMINISTIC |
| Obligation | Secure coding training completed ≤ 365 days; covers relevant languages and current vulnerabilities | DETERMINISTIC |
| Evidence | `training_records.employee_id`; `training_records.training_date`; `training_type == "secure_coding"`; gap ≤ 365 days | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 6.3.2 — Software Inventory (R — DETERMINISTIC)

### Source excerpt

> *6.3.2 — An inventory of bespoke and custom software, and third-party software components incorporated into bespoke and custom software is maintained to facilitate vulnerability and patch management.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All bespoke/custom software and embedded third-party libraries in CDE | DETERMINISTIC |
| Condition | CDE software component exists | DETERMINISTIC |
| Obligation | Software inventory (SBOM or equivalent) maintained; includes all third-party dependencies | DETERMINISTIC |
| Evidence | `software_inventory.component_name`, `software_inventory.version`, `software_inventory.cde_system`; inventory current | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 6.4.1 — Web Application Protection (R — PARAMETERIZED)

### Source excerpt

> *6.4.1 — For public-facing web applications, new threats and vulnerabilities are addressed on an ongoing basis and these applications are protected against known attacks by applying either of the following methods: Reviewing public-facing web applications via manual or automated application vulnerability security assessment tools or methods, at least once every 12 months or after any significant changes, and with all vulnerabilities corrected. Installing an automated technical solution that continuously detects and prevents web-based attacks, with an alert generated, at a minimum, for the following attack types: cross-site scripting (XSS), injection flaws, malicious file execution, improper system/object reference, cross-site request forgery (CSRF), information leakage and improper error handling, broken authentication and session management.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All public-facing web applications processing or accessing CHD | DETERMINISTIC |
| Condition | Web application is public-facing and in scope | DETERMINISTIC |
| Obligation | Either: (a) annual DAST/manual assessment with all vulnerabilities corrected; OR (b) WAF deployed covering the 7 required attack types | PARAMETERIZED (approach selection) |
| Evidence | `web_app_assessment_records.last_assessment_date` ≤ 365 days AND `vulnerabilities_corrected == true`, OR `waf_config.deployed == true` with all 7 categories configured | PARAMETERIZED |

**Assumption (ASSUME-6-002):** WAF deployment is adequate when: (1) deployed inline (not just monitoring mode); (2) blocks/alerts on all 7 required attack categories per 6.4.1; (3) rules updated at least monthly; (4) false positive review process documented. Monitoring-only WAF mode does not satisfy the "continuously detects and prevents" language.

**Overall: PARAMETERIZED → Pattern 2**

---

## YAML specifications

### `req6_patch_slas.yaml`

```yaml
regulation_id: PCI-DSS-v4.0-6.3.3
section: "PCI DSS v4.0 — Patch Management SLAs"
r_or_a: Required
source_text: >
  Critical/high patches installed within one month of release.
  All applicable security patches installed within three months of release.

extracted_elements:
  subject: "All CDE system components"
  condition: "Security patch released"
  obligation: "Critical/high ≤ 30 days; non-critical ≤ 90 days"
  evidence: "patch_records: patch_id, release_date, install_date, criticality"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: PARAMETERIZED

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-6-001
    assumption_text: >
      Criticality classification: CVSS >= 7.0 = high/critical (30-day SLA);
      CVSS < 7.0 = non-critical (90-day SLA). Stricter classification governs
      when vendor and CVSS conflict. Zero-days are always critical.
    assumed_by: "IT Security Officer"
    approved_by: "Compliance Officer"
    date: "2026-05-20"
    review_frequency_days: 365
    cryptographic_hash: "sha256:pending-ci"
test_confidence: HIGH
generated_test: "tests/req6/test_6_3_patch_management.py"
```

---

## Generated tests

### `tests/req6/test_6_3_patch_management.py`

```python
"""
PCI DSS v4.0 Req 6.3 — Patch Management
Confidence: HIGH for timing; MEDIUM for criticality classification
"""
import pytest
from datetime import date

CRITICAL_HIGH_PATCH_MAX_DAYS = 30
NONCRITICAL_PATCH_MAX_DAYS = 90
CVSS_HIGH_CRITICAL_THRESHOLD = 7.0


def test_critical_patches_installed_within_30_days(patch_records):
    """6.3.3 — Critical/high patches installed within 1 month of release."""
    violations = []
    for patch in patch_records:
        if not patch.get("in_cde"):
            continue
        criticality = patch.get("criticality", "").lower()
        cvss = patch.get("cvss_score", 0)
        is_critical_or_high = (
            criticality in ("critical", "high")
            or cvss >= CVSS_HIGH_CRITICAL_THRESHOLD
        )
        if not is_critical_or_high:
            continue
        release_date = patch.get("release_date")
        install_date = patch.get("install_date")
        if not install_date:
            violations.append(
                f"Patch {patch['patch_id']} on {patch['system_id']}: "
                f"not installed (critical/high, released {release_date})"
            )
            continue
        days = (install_date - release_date).days
        if days > CRITICAL_HIGH_PATCH_MAX_DAYS:
            violations.append(
                f"Patch {patch['patch_id']} on {patch['system_id']}: "
                f"installed {days} days after release (max {CRITICAL_HIGH_PATCH_MAX_DAYS})"
            )
    assert not violations, (
        f"VIOLATION (6.3.3): {len(violations)} critical/high patch(es) not installed "
        f"within 30 days:\n" + "\n".join(violations)
    )


def test_noncritical_patches_installed_within_90_days(patch_records):
    """6.3.3 — All applicable security patches installed within 3 months."""
    violations = []
    for patch in patch_records:
        if not patch.get("in_cde") or not patch.get("security_patch"):
            continue
        cvss = patch.get("cvss_score", 0)
        criticality = patch.get("criticality", "").lower()
        is_critical_or_high = (
            criticality in ("critical", "high") or cvss >= CVSS_HIGH_CRITICAL_THRESHOLD
        )
        if is_critical_or_high:
            continue  # covered by critical test
        install_date = patch.get("install_date")
        release_date = patch.get("release_date")
        if not install_date:
            today = date.today()
            days_unpatched = (today - release_date).days
            if days_unpatched > NONCRITICAL_PATCH_MAX_DAYS:
                violations.append(
                    f"Patch {patch['patch_id']} on {patch['system_id']}: "
                    f"not installed, {days_unpatched} days since release"
                )
            continue
        days = (install_date - release_date).days
        if days > NONCRITICAL_PATCH_MAX_DAYS:
            violations.append(
                f"Patch {patch['patch_id']} on {patch['system_id']}: "
                f"installed {days} days after release (max {NONCRITICAL_PATCH_MAX_DAYS})"
            )
    assert not violations, (
        f"VIOLATION (6.3.3): {len(violations)} non-critical patch(es) not installed "
        f"within 90 days:\n" + "\n".join(violations)
    )


def test_developer_secure_coding_training_current(training_records, developer_roster):
    """6.2.2 — All CDE developers trained in secure coding within past 12 months."""
    today = date.today()
    trained_ids = {
        r["employee_id"] for r in training_records
        if r.get("training_type") == "secure_coding"
        and (today - r["training_date"]).days <= 365
    }
    violations = [
        d for d in developer_roster
        if d.get("works_on_cde_code") and d["employee_id"] not in trained_ids
    ]
    assert not violations, (
        f"VIOLATION (6.2.2): {len(violations)} developer(s) without current secure "
        f"coding training:\n"
        + "\n".join(
            f"  {d['employee_id']}: {d.get('name')}" for d in violations
        )
    )


def test_software_inventory_exists_for_cde_components(software_inventory, cde_systems):
    """6.3.2 — Software inventory (SBOM) must exist for all CDE software components."""
    inventoried_systems = {i["cde_system_id"] for i in software_inventory}
    violations = [
        s for s in cde_systems
        if s["system_id"] not in inventoried_systems
    ]
    assert not violations, (
        f"VIOLATION (6.3.2): {len(violations)} CDE system(s) without software "
        f"inventory: {[s['system_id'] for s in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-6-002",
    description=(
        "WAF adequate: inline (not monitoring-only); all 7 attack categories; "
        "rules updated monthly; false positive review documented."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_public_facing_web_apps_have_waf_or_assessment(web_app_records):
    """6.4.1 — Public-facing web apps must have WAF or annual assessment."""
    today = date.today()
    violations = []
    for app in web_app_records:
        if not app.get("public_facing") or not app.get("in_scope"):
            continue
        has_waf = app.get("waf_deployed") and app.get("waf_mode") == "blocking"
        last_assessment = app.get("last_security_assessment_date")
        has_current_assessment = (
            last_assessment and (today - last_assessment).days <= 365
            and app.get("assessment_vulnerabilities_corrected")
        )
        if not has_waf and not has_current_assessment:
            violations.append(
                f"App {app['app_id']}: no WAF in blocking mode and no current "
                f"annual security assessment"
            )
    assert not violations, (
        f"VIOLATION (6.4.1): {len(violations)} public-facing web app(s) without "
        f"required protection:\n" + "\n".join(violations)
    )
```

---

## Notes for the registry

- **Patch SLA measurement:** The clock starts at the vendor's public release date, not the date your vulnerability scanner detected it. For CVEs, use the NVD published date. Organizations that rely on scanner detection lag behind this clock — subscribe to vendor security advisories directly.
- **Software inventory (SBOM) is new in v4.0:** v3.2.1 did not require a formal software bill of materials. v4.0 Req 6.3.2 requires tracking all bespoke software and third-party components (libraries, frameworks, SDKs). This enables correlation with vulnerability feeds (NVD, OSV) to identify which systems are affected when new CVEs are published.
- **WAF blocking mode requirement:** 6.4.1 requires "continuously detects and prevents" — monitoring-only WAF does not satisfy "prevents." The WAF must be in inline/blocking mode for production. Testing/learning mode should not be a permanent state for production systems.
- **Developer training specificity:** 6.2.2 requires training "relevant to their development languages and environments." Generic cybersecurity awareness training does not satisfy this — OWASP Top 10 training specific to the languages used (Java, Python, JavaScript, etc.) is the expected minimum. Training must be dated within the past 12 months.
- **Custom vs. commercial software distinction:** Req 6 SDLC requirements (6.2.x) apply only to bespoke/custom software written by or for the organization. Commercial off-the-shelf (COTS) software is covered by patch management (6.3.3) but not by secure coding requirements. The boundary matters for test scope.
