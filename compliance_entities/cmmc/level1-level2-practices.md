# CMMC 2.0 — Level 1 (FAR 52.204-21) and Level 2 Domain Mapping

**Registry path:** `/regulation-registry/CMMC/Practices/`
**Version:** CMMC 2.0 (32 CFR Part 170, effective Dec 2024)
**Last parsed:** 2026-05-20
**Applies to:** Defense contractors and subcontractors handling Controlled Unclassified Information (CUI) or Federal Contract Information (FCI) under Department of Defense (DoD) contracts and subcontracts
**Trigger:** DoD contract or subcontract containing DFARS clause 252.204-7012 (CUI) or 252.204-7021 (CMMC); prime contractors must flow down CMMC requirements to all subcontractors handling CUI; CMMC Level determined by CUI type and sensitivity
**Jurisdiction:** United States Department of Defense supply chain; applies to US companies and foreign companies holding DoD contracts
**Not applicable to:** Commercial-only companies with no DoD contracts or subcontracts; DoD contracts not involving CUI or FCI (though basic contractor ethics and safeguarding under FAR 52.204-21 still apply); non-defense government contractors (civilian agencies use FISMA/800-171 directly without CMMC framework)
**Overall confidence:** HIGH for Level 1 (17 binary safeguarding practices); MEDIUM for Level 2 mapping (inherits confidence from 800-171 family files); CONTESTED for SPRS scoring and POA&M adequacy
**Level 1: 17 practices | Level 2: 110 practices (= NIST SP 800-171 r2) | Level 3: +24 practices from NIST 800-172**

---

## Scope summary

This file covers:
1. **Level 1 practices** (17 — FAR 52.204-21 basic safeguarding): binary, fully DETERMINISTIC, highest confidence in the registry
2. **Level 2 domain mapping**: CMMC Level 2 maps 1:1 to NIST SP 800-171 r2 (110 practices across 14 domains). The 800-171 family files provide the test specifications; this file provides the CMMC framing, scoring, and assessment context
3. **SPRS score calculation**: synthetic test that computes current score from practice implementation matrix
4. **Annual affirmation**: time-bounded test for CMMC affirmation deadline

**Key distinction:** CMMC Level 2 uses SP 800-171 **r2** (not r3). The 800-171 family files in this registry are written for r3. The difference is ~7 practices added in r3 vs. r2. For CMMC Level 2 purposes, the r2 practice set (110 practices) is the authoritative source; r3 practices beyond r2 are tracked separately as Level 3 candidates.

---

## Level 1 Practices — FAR 52.204-21 (DETERMINISTIC)

All 17 Level 1 practices are directly derived from FAR 52.204-21 basic safeguarding requirements for Federal Contract Information (FCI). They are the minimum baseline for any DoD contractor handling FCI. All are binary (implemented = yes/no).

| Practice ID | Description | Domain | Confidence |
|---|---|---|---|
| AC.L1-3.1.1 | Limit access to authorized users and processes | AC | HIGH (DETERMINISTIC) |
| AC.L1-3.1.2 | Limit access to types of transactions and functions users are permitted to execute | AC | HIGH (DETERMINISTIC) |
| IA.L1-3.5.1 | Identify information system users, processes, and devices | IA | HIGH (DETERMINISTIC) |
| IA.L1-3.5.2 | Authenticate (or verify) the identities of users, processes, or devices | IA | HIGH (DETERMINISTIC) |
| IA.L1-3.5.3 | Use MFA for local and network access to privileged accounts | IA | HIGH (DETERMINISTIC) |
| IA.L1-3.5.4 | Employ replay-resistant authentication for network access | IA | HIGH (DETERMINISTIC) |
| MP.L1-3.8.3 | Sanitize or destroy media before disposal or reuse | MP | HIGH (DETERMINISTIC) |
| PE.L1-3.10.1 | Limit physical access to authorized individuals | PE | HIGH (DETERMINISTIC) |
| PE.L1-3.10.3 | Escort visitors and monitor visitor activity | PE | MEDIUM (PARAMETERIZED) |
| PE.L1-3.10.4 | Maintain audit logs of physical access | PE | HIGH (DETERMINISTIC) |
| PE.L1-3.10.5 | Manage physical access devices | PE | MEDIUM (PARAMETERIZED) |
| SC.L1-3.13.1 | Monitor, control, and protect communications at external boundaries | SC | HIGH (DETERMINISTIC) |
| SC.L1-3.13.5 | Implement subnetworks for publicly accessible system components | SC | HIGH (DETERMINISTIC) |
| SI.L1-3.14.1 | Identify, report, and correct flaws in a timely manner | SI | HIGH (DETERMINISTIC) |
| SI.L1-3.14.2 | Provide protection from malicious code at appropriate locations | SI | HIGH (DETERMINISTIC) |
| SI.L1-3.14.4 | Update malicious code protection mechanisms when new releases are available | SI | HIGH (DETERMINISTIC) |
| SI.L1-3.14.5 | Perform periodic scans and real-time scans of files from external sources | SI | HIGH (DETERMINISTIC) |

---

## Level 2 Domain-to-800-171 Mapping

Level 2 (110 practices) = NIST SP 800-171 r2 exactly. The following table maps CMMC domains to 800-171 family files.

| CMMC Domain | CMMC Practice Range | 800-171 r2 Family | Registry File (r3 basis) | Practices |
|---|---|---|---|---|
| AC | AC.L1-3.1.x, AC.L2-3.1.x | AC (3.1.1–3.1.22) | `ac-access-control.md` | 22 |
| AT | AT.L2-3.2.x | AT (3.2.1–3.2.3) | Pending | 3 |
| AU | AU.L2-3.3.x | AU (3.3.1–3.3.9) | `au-cm-si-core-technical.md` | 9 |
| CM | CM.L2-3.4.x | CM (3.4.1–3.4.9) | `au-cm-si-core-technical.md` | 9 |
| IA | IA.L1/L2-3.5.x | IA (3.5.1–3.5.12) | `ia-identification-authentication.md` | 11 (r2) / 12 (r3) |
| IR | IR.L2-3.6.x | IR (3.6.1–3.6.3) | Pending | 3 |
| MA | MA.L2-3.7.x | MA (3.7.1–3.7.6) | Pending | 6 |
| MP | MP.L1/L2-3.8.x | MP (3.8.1–3.8.9) | Pending | 9 |
| PE | PE.L1/L2-3.10.x | PE (3.10.1–3.10.6) | Pending | 6 |
| RM | RM.L2-3.11.x | RA (3.11.1–3.11.3) | Pending | 3 |
| CA | CA.L2-3.12.x | CA (3.12.1–3.12.4) | Pending | 4 |
| SC | SC.L1/L2-3.13.x | SC (3.13.1–3.13.16) | Pending | 16 |
| SI | SI.L1/L2-3.14.x | SI (3.14.1–3.14.7) | `au-cm-si-core-technical.md` | 7 |
| PS | PS.L2-3.9.x | PS (3.9.1–3.9.2) | Pending | 2 |

> **r2 vs. r3 note:** CMMC Level 2 assessments are scored against 800-171 r2 (110 practices). The test files in this registry reference r3 for the most current guidance; r2 practices are a subset of r3. For CMMC scoring purposes, r2 practice IDs are used; r3 practices beyond r2 are not yet in scope for Level 2.

---

## SPRS Score Calculation

The SPRS score starts at 110 and deducts points for each unimplemented practice. DoD CMMC Program Office assigns a point weight to each practice; total deductible points = 203 (maximum deficit). Score range: -203 to +110.

| Score range | Meaning | Action required |
|---|---|---|
| 110 | All 110 Level 2 practices implemented | No POA&M required |
| 0 to 109 | Some practices not implemented | POA&M required for each unimplemented |
| Below 0 | Significant gaps | POA&M required; contracting officer review |

**Assumption (ASSUME-CMMC-001):** SPRS score is adequately calculated when: (1) each of the 110 Level 2 practices assessed as Met/Not Met against the 800-171 r2 assessment objectives in 800-171A; (2) point deduction applied per DoD's published weighting table; (3) score submitted to SPRS within required timeframe before or after contract award (per DFARS 252.204-7021); (4) open POA&M items documented with completion date ≤ 180 days from assessment; (5) practices marked "Not Applicable" require documented rationale.

---

## Annual Affirmation Requirement

Both Level 1 and Level 2 self-assessors must submit an annual affirmation in SPRS that their implementation remains accurate.

**Assumption (ASSUME-CMMC-002):** Annual affirmation is adequate when: (1) Senior Official (CEO, President, or equivalent) or authorized representative submits affirmation; (2) affirmation submitted within 12 months of last assessment or last affirmation; (3) affirmation accurately reflects current implementation status; (4) if implementation status has changed since last assessment, updated assessment or POA&M submitted before affirmation.

---

## YAML specifications

### `cmmc_level1_level2.yaml`

```yaml
regulation_id: CMMC-2.0-Level1-Level2
section: "CMMC 2.0 — Level 1 (FAR 52.204-21) and Level 2 (NIST 800-171 r2) Practices"
r_or_a: Required
source_text: >
  Level 1: 17 basic safeguarding requirements from FAR 52.204-21.
  Level 2: 110 practices from NIST SP 800-171 r2 across 14 domains.
  Assessment: Annual self-assessment (Level 2 self) or triennial C3PAO (Level 2 C3PAO).
  SPRS score submitted before or concurrent with contract performance.

extracted_elements:
  subject: "All systems handling FCI (Level 1) or CUI (Level 2)"
  condition: "DoD contract requires CMMC Level 1 or Level 2; FCI/CUI handling attested"
  obligation: "All applicable practices implemented; SPRS score current; annual affirmation current"
  evidence: >
    practice_implementation_matrix (per 800-171 family files),
    sprs_submission_records,
    affirmation_records,
    poam_records

ambiguity_classification:
  subject: DETERMINISTIC
  condition: PARAMETERIZED
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log:
  - assumption_id: ASSUME-CMMC-001
    assumption_text: >
      SPRS score: 110 practices assessed against 800-171A objectives; point deductions
      per DoD table; POA&M items have completion date ≤180 days; N/A requires rationale.
    assumed_by: "System Owner"
    approved_by: "Senior Official"
    date: "2026-05-20"
    review_frequency_days: 365
  - assumption_id: ASSUME-CMMC-002
    assumption_text: >
      Annual affirmation: submitted by Senior Official within 12 months; accurately reflects
      current status; updated assessment if implementation changed.
    assumed_by: "System Owner"
    approved_by: "Senior Official"
    date: "2026-05-20"
    review_frequency_days: 365
test_confidence: HIGH
generated_test: "tests/cmmc/test_cmmc_scoring_affirmation.py"
```

---

## Generated tests

### `tests/cmmc/test_cmmc_scoring_affirmation.py`

```python
"""
CMMC 2.0 — Level 1 and Level 2: Scoring, Affirmation, POA&M
Confidence: HIGH for affirmation cadence and POA&M staleness checks
Note: Practice-specific tests are in the 800-171 family test files.
"""
import pytest
from datetime import date

AFFIRMATION_MAX_DAYS = 365
POAM_MAX_OPEN_DAYS = 180
SPRS_MIN_SCORE_LEVEL1 = 110
CMMC_LEVEL2_TOTAL_PRACTICES = 110


@pytest.fixture(autouse=True)
def require_cmmc_scope(system_scope):
    """All CMMC tests require CMMC contract scope attestation."""
    if not system_scope.get("cmmc_contract_applies"):
        pytest.skip("System not under CMMC contract requirement")


@pytest.mark.assumption(
    id="ASSUME-CMMC-002",
    description="Annual affirmation: Senior Official within 12 months; accurately reflects current status",
    approved_by="Senior Official",
    review_date="2026-05-20",
)
def test_sprs_affirmation_current(cmmc_affirmation_records):
    """CMMC — Annual affirmation must be current (within 12 months)."""
    today = date.today()
    if not cmmc_affirmation_records:
        assert False, (
            "NONCONFORMITY (CMMC Affirmation): No SPRS affirmation records found — "
            "annual affirmation is required"
        )
    latest = max(cmmc_affirmation_records, key=lambda r: r["affirmation_date"])
    days_since = (today - latest["affirmation_date"]).days
    assert days_since <= AFFIRMATION_MAX_DAYS, (
        f"NONCONFORMITY (CMMC Affirmation): SPRS affirmation last submitted "
        f"{days_since} days ago (max {AFFIRMATION_MAX_DAYS})"
    )


@pytest.mark.assumption(
    id="ASSUME-CMMC-001",
    description="SPRS: 110 practices; point deductions per DoD table; POA&M ≤180 days; N/A requires rationale",
    approved_by="Senior Official",
    review_date="2026-05-20",
)
def test_poam_items_not_overdue(cmmc_poam_records):
    """CMMC — Open POA&M items must not exceed 180-day completion window."""
    today = date.today()
    violations = []
    for item in cmmc_poam_records:
        if item.get("status") == "closed":
            continue
        completion_date = item.get("planned_completion_date")
        if completion_date and (today - completion_date).days > 0:
            violations.append(
                f"POA&M {item['poam_id']} (Practice {item.get('practice_id')}): "
                f"planned completion {completion_date} is overdue"
            )
        elif item.get("days_open", 0) > POAM_MAX_OPEN_DAYS:
            violations.append(
                f"POA&M {item['poam_id']}: open {item['days_open']} days "
                f"(max {POAM_MAX_OPEN_DAYS})"
            )
    assert not violations, (
        f"NONCONFORMITY (CMMC POA&M): {len(violations)} overdue POA&M item(s):\n"
        + "\n".join(violations)
    )


def test_sprs_score_submitted(cmmc_sprs_records):
    """CMMC — SPRS score must be on file."""
    assert cmmc_sprs_records, (
        "NONCONFORMITY (CMMC SPRS): No SPRS submission records found — "
        "SPRS score submission is required before contract award"
    )
    latest = max(cmmc_sprs_records, key=lambda r: r["submission_date"])
    assert latest.get("score") is not None, (
        "NONCONFORMITY (CMMC SPRS): Latest SPRS submission has no score recorded"
    )


def test_level1_all_17_practices_assessed(practice_implementation_matrix):
    """CMMC Level 1 — All 17 FAR 52.204-21 practices must be assessed."""
    LEVEL1_PRACTICE_IDS = {
        "AC.L1-3.1.1", "AC.L1-3.1.2", "IA.L1-3.5.1", "IA.L1-3.5.2",
        "IA.L1-3.5.3", "IA.L1-3.5.4", "MP.L1-3.8.3",
        "PE.L1-3.10.1", "PE.L1-3.10.3", "PE.L1-3.10.4", "PE.L1-3.10.5",
        "SC.L1-3.13.1", "SC.L1-3.13.5",
        "SI.L1-3.14.1", "SI.L1-3.14.2", "SI.L1-3.14.4", "SI.L1-3.14.5"
    }
    assessed_ids = {p["practice_id"] for p in practice_implementation_matrix}
    missing = LEVEL1_PRACTICE_IDS - assessed_ids
    assert not missing, (
        f"NONCONFORMITY (CMMC Level 1): {len(missing)} Level 1 practice(s) not assessed: "
        f"{missing}"
    )


def test_not_applicable_practices_have_rationale(practice_implementation_matrix):
    """CMMC — Practices marked N/A must have documented rationale."""
    violations = [
        p for p in practice_implementation_matrix
        if p.get("status") == "not_applicable"
        and not p.get("na_rationale")
    ]
    assert not violations, (
        f"NONCONFORMITY (CMMC): {len(violations)} practice(s) marked N/A without "
        f"documented rationale: {[p['practice_id'] for p in violations]}"
    )
```

---

## Notes for the registry

- **CMMC Level 2 uses r2, not r3:** This is a critical distinction. CMMC Level 2 assessment is scored against 800-171 r2 (110 practices). NIST SP 800-171 r3 added ~7 practices and reorganized others. Until DoD updates the CMMC rule to reference r3, Level 2 assessments use r2. The 800-171 family files in this registry use r3 numbering; for CMMC purposes, r2 practice IDs and descriptions should be used in the SSP.
- **C3PAO vs. self-assessment decision:** Whether Level 2 requires a C3PAO (third-party) or allows self-assessment is determined by the DoD program office and specified in the contract solicitation. Contractors cannot self-elect to use C3PAO in lieu of the required method. The CMMC marketplace (CMMC-AB) maintains the list of authorized C3PAOs.
- **SPRS score and contracting risk:** A low SPRS score (below 110) with an open POA&M does not automatically disqualify a contractor — the contracting officer has discretion. However, the SPRS score is publicly visible to government customers and affects source selection scoring. Organizations should treat SPRS score improvement as a business priority, not just a compliance exercise.
- **Level 3 delta (24 practices from 800-172):** Level 3 requires a government-led assessment by DCSA. The 24 additional practices from 800-172 focus on advanced persistent threat (APT) resilience: enhanced security design, threat hunting, deception technology, and advanced incident response. Level 3 is reserved for the highest-priority programs and is not addressed in Level 1/2 test files.
- **Annual affirmation vs. triennial assessment:** Level 2 self-assessors do a full assessment every 3 years but must affirm annually that the implementation status in SPRS remains accurate. If implementation has degraded (e.g., a control was removed), the annual affirmation should not be submitted without updating the SPRS score. False affirmations expose the organization to False Claims Act liability.
