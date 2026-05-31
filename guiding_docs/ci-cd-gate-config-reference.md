# CI/CD Gate Configuration Reference

**Document version:** 2026.05
**Last updated:** 2026-05-20
**Purpose:** Operational reference for configuring Pattern 1/2/3 compliance test gates in a CI/CD pipeline. Covers pytest configuration, gate behavior per pattern, failure routing, staleness enforcement, and example pipeline YAML for GitHub Actions and GitLab CI.

---

## Gate Behavior by Pattern

### Pattern 1 — Direct Assertion (DETERMINISTIC)

**Claim:** "This system is compliant with [requirement] as of this test run."

**Gate behavior:**
- Pass → green gate; no action required
- Fail → **pipeline BLOCKS**; route to Engineering; must be remediated before merge

**When to use:** Requirement has a specific, unambiguous threshold (e.g., "MFA required for all admin accounts," "patch must be applied within 30 days," "audit log retained for 12 months").

```python
# Pattern 1 example
def test_pci_req8_mfa_admin_accounts(live_assets):
    """PCI DSS Req 8.4.2 — MFA required for all non-console admin access to CDE."""
    admin_accounts = [a for a in live_assets.accounts if a.has_cde_admin_access]
    violations = [a for a in admin_accounts if not a.mfa_enabled]
    assert len(violations) == 0, (
        f"PCI DSS Req 8.4.2 FAIL: {len(violations)} admin accounts without MFA: "
        f"{[a.username for a in violations]}"
    )
```

---

### Pattern 2 — Parameterized Assertion (PARAMETERIZED)

**Claim:** "This system is compliant with [requirement] given assumption [ASSUME-XXX-YYY], approved on [date]."

**Gate behavior:**
- Pass (assumption ACTIVE + not stale) → green gate
- Pass (assumption ACTIVE but approaching expiry within 30 days) → yellow warning in CI output; no block
- Fail due to stale assumption → **pipeline BLOCKS**; route to Compliance team for assumption re-approval; Engineering cannot resolve alone
- Fail due to condition not met → **pipeline BLOCKS**; route to Engineering + notify Compliance (assumption may need revision too)

```python
# Pattern 2 example
import pytest

@pytest.mark.assumption(
    id="ASSUME-HIPAA-001",
    text="Organization treats encryption at rest as required for all ePHI systems.",
    approved_by="CISO",
    approval_date="2026-01-15",
    review_due_date="2027-01-15",
)
def test_hipaa_encryption_at_rest(live_assets, assumption_registry):
    """HIPAA §164.312(a)(2)(iv) — Encryption of ePHI at rest (Addressable)."""
    assumption_registry.validate("ASSUME-HIPAA-001")  # raises if stale or invalid
    ephi_systems = [s for s in live_assets.systems if s.processes_ephi]
    violations = [s for s in ephi_systems if not s.encryption_at_rest_enabled]
    assert len(violations) == 0, (
        f"HIPAA §164.312(a)(2)(iv) FAIL: {len(violations)} ePHI systems without "
        f"encryption at rest: {[s.name for s in violations]}"
    )
```

---

### Pattern 3 — Human Determination (CONTESTED)

**Claim:** "A qualified human has determined compliance with [requirement] as of [date], and that determination is current."

**Gate behavior:**
- Pass (human determination exists + not stale) → green gate
- Fail (no determination) → **pipeline BLOCKS**; **pages Compliance Officer**; Engineering cannot resolve
- Fail (determination stale) → **pipeline BLOCKS**; **pages Compliance Officer** with expiry notice
- Note: Pattern 3 tests NEVER evaluate compliance itself — only that a valid human determination exists

```python
# Pattern 3 example
def test_hipaa_minimum_necessary_determination(determination_registry):
    """
    HIPAA §164.502(b) — Minimum Necessary Standard.
    CONTESTED: 'minimum necessary' determination is organization-defined.
    This test verifies that a qualified Compliance Officer has made and documented
    the determination — it does not evaluate whether the determination is correct.
    """
    determination = determination_registry.get(
        framework="hipaa",
        section="164.502(b)",
        determination_type="minimum_necessary_standard"
    )
    assert determination is not None, (
        "HIPAA §164.502(b) BLOCKED: No Compliance Officer determination for "
        "minimum necessary standard. A qualified human must document this determination "
        "before this gate can pass."
    )
    assert not determination.is_stale(), (
        f"HIPAA §164.502(b) BLOCKED: Minimum necessary determination expired "
        f"{determination.expiry_date}. Compliance Officer review required."
    )
    assert determination.approver_is_qualified(), (
        f"HIPAA §164.502(b) BLOCKED: Determination was approved by "
        f"'{determination.approved_by}' but this control requires Compliance Officer "
        f"or Legal Counsel approval."
    )
```

---

## pytest Configuration

### conftest.py — fixtures

```python
# conftest.py
import pytest
from datetime import date
from compliance_fixtures import (
    LiveAssets,
    AssumptionRegistry,
    DeterminationRegistry,
)

@pytest.fixture(scope="session")
def live_assets():
    """Returns a LiveAssets object connected to your CMDB/asset database."""
    return LiveAssets.from_config("config/assets.yaml")

@pytest.fixture(scope="session")
def assumption_registry():
    """Returns an AssumptionRegistry loaded from all _index.md assumption blocks."""
    return AssumptionRegistry.from_directory("compliance_entities/")

@pytest.fixture(scope="session")
def determination_registry():
    """Returns a DeterminationRegistry connected to your GRC workflow system."""
    return DeterminationRegistry.from_config("config/determinations.yaml")
```

### pytest.ini

```ini
[pytest]
markers =
    assumption: Pattern 2 test — parameterized by a documented assumption
    determination: Pattern 3 test — requires human determination
    pattern1: DETERMINISTIC direct assertion
    pattern2: PARAMETERIZED assertion with assumption
    pattern3: CONTESTED human-surfacing test
    framework_hipaa: HIPAA Security Rule tests
    framework_pci: PCI DSS tests
    framework_nerc_cip: NERC CIP tests
    # ... one marker per framework

addopts =
    --tb=short
    --strict-markers
    -v
```

### Running subsets by framework

```bash
# All HIPAA tests
pytest -m framework_hipaa

# Only DETERMINISTIC (Pattern 1) tests
pytest -m pattern1

# All tests except CONTESTED (Pattern 3) — for automated pipeline only
pytest -m "not pattern3"

# Single framework + pattern
pytest -m "framework_pci and pattern1"
```

---

## Failure Routing Matrix

| Test | Failure type | Route to | Block pipeline? | Notification |
|---|---|---|---|---|
| Pattern 1 | Condition not met | Engineering | **YES** | Ticket in bug tracker |
| Pattern 2 | Condition not met | Engineering + Compliance (FYI) | **YES** | Ticket in bug tracker |
| Pattern 2 | Stale assumption | Compliance Officer ONLY | **YES** | Email + Slack to Compliance |
| Pattern 2 | Hash mismatch (assumption tampered) | Security + Compliance | **YES** | Immediate Slack alert |
| Pattern 3 | No human determination | Compliance Officer ONLY | **YES** | Page Compliance Officer |
| Pattern 3 | Stale determination | Compliance Officer ONLY | **YES** | Email + calendar reminder |
| Pattern 3 | Wrong approver role | Compliance Officer ONLY | **YES** | Email to Compliance |

---

## GitHub Actions Pipeline Example

```yaml
# .github/workflows/compliance.yml
name: Compliance Test Suite

on:
  push:
    branches: [main, develop]
  schedule:
    - cron: '0 6 * * *'      # daily at 6 AM — catches staleness even without code changes
  workflow_dispatch:

jobs:
  compliance-pattern1:
    name: "Pattern 1 — DETERMINISTIC gates"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run Pattern 1 tests
        run: pytest -m pattern1 --junitxml=results/pattern1.xml
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: pattern1-results
          path: results/pattern1.xml

  compliance-pattern2:
    name: "Pattern 2 — PARAMETERIZED gates (with assumption validation)"
    runs-on: ubuntu-latest
    needs: compliance-pattern1
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run Pattern 2 tests
        run: pytest -m pattern2 --junitxml=results/pattern2.xml
      - name: Check assumption staleness
        run: python tools/check_assumption_staleness.py --warn-days 30
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: pattern2-results
          path: results/pattern2.xml

  compliance-pattern3:
    name: "Pattern 3 — CONTESTED (human determination required)"
    runs-on: ubuntu-latest
    needs: compliance-pattern2
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run Pattern 3 tests
        run: pytest -m pattern3 --junitxml=results/pattern3.xml
      - name: Notify compliance officer on failure
        if: failure()
        uses: 8398a7/action-slack@v3
        with:
          status: failure
          text: "COMPLIANCE GATE BLOCKED: Pattern 3 test failed — Compliance Officer review required. See run: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.COMPLIANCE_SLACK_WEBHOOK }}
```

---

## Staleness Check Tool

```python
# tools/check_assumption_staleness.py
"""
Scans all _index.md files for assumption blocks and reports those
approaching or past their review_due_date.
"""
import argparse
import sys
from datetime import date, timedelta
from pathlib import Path
import re

def check_staleness(warn_days: int = 30) -> int:
    """Returns exit code: 0 = all current, 1 = warnings, 2 = stale (pipeline should fail)."""
    today = date.today()
    warn_threshold = today + timedelta(days=warn_days)
    
    failures = []
    warnings = []
    
    for index_file in Path("compliance_entities").rglob("_index.md"):
        content = index_file.read_text()
        # Extract review_due_date fields from assumption blocks
        for match in re.finditer(r"review_due_date:\s*['\"]?(\d{4}-\d{2}-\d{2})['\"]?", content):
            due = date.fromisoformat(match.group(1))
            assume_id_match = re.search(r"id:\s*['\"]?(ASSUME-[\w-]+)['\"]?", 
                                         content[:match.start()])
            assume_id = assume_id_match.group(1) if assume_id_match else "UNKNOWN"
            
            if due < today:
                failures.append(f"STALE: {assume_id} in {index_file} — due {due} ({(today - due).days} days overdue)")
            elif due <= warn_threshold:
                warnings.append(f"WARNING: {assume_id} in {index_file} — due {due} ({(due - today).days} days remaining)")
    
    for w in warnings:
        print(w)
    for f in failures:
        print(f)
    
    if failures:
        return 2
    elif warnings:
        return 1
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--warn-days", type=int, default=30)
    args = parser.parse_args()
    sys.exit(check_staleness(args.warn_days))
```

---

## Determination Registry Schema

Pattern 3 tests query a determination registry. Minimum schema:

```yaml
# config/determinations.yaml
determinations:
  - id: "DET-HIPAA-502b-001"
    framework: "hipaa"
    section: "164.502(b)"
    determination_type: "minimum_necessary_standard"
    determination_text: |
      [Compliance Officer's determination of minimum necessary standard
      for all use cases at this organization.]
    approved_by: "Chief Compliance Officer"
    approver_role: "compliance_officer"
    approval_date: "2026-03-01"
    review_frequency_days: 365
    review_due_date: "2027-03-01"
    status: "ACTIVE"
```

The `approver_role` field is validated against a role hierarchy so that Pattern 3 tests can enforce that the right level of authority made the determination.
