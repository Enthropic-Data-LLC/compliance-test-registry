# NERC CIP Registry Manifest

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** CIP-002 through CIP-015 (complete suite)

---

## Summary

| Metric | Count |
|---|---|
| Standards parsed | 14 |
| Total requirements parsed | 41 (R-level) |
| Fully automated (DETERMINISTIC) | 18 |
| Partial automation (PARAMETERIZED) | 20 |
| Human-determination required (CONTESTED) | 3 |
| Unresolvable | 0 |
| Open assumptions | 22 |
| Stale reviews | 0 (registry is new) |
| Pending external escalations | 0 |
| Pre-enforcement standards (informational mode) | 2 (CIP-012-2, CIP-015-1) |

---

## Per-standard confidence map

| Standard | Version | Effective | Overall confidence | PARAMETERIZED reqs | CONTESTED reqs |
|---|---|---|---|---|---|
| CIP-002 | 5.1a | Current | HIGH | — | — |
| CIP-003 | 9 | 2026-04-01 | MEDIUM | R2 (Att. 1 Sec 3, Sec 6) | — |
| CIP-004 | 7 | Current | HIGH for R1–R3, R5; MEDIUM for R4 | R4 | — |
| CIP-005 | 7 | Current | MEDIUM | R1.3, R1.5, R3 | — |
| CIP-006 | 6 | Current | HIGH | R1.10 only | — |
| CIP-007 | 6 | Current | LOW for R2; MEDIUM for R1, R3, R5; HIGH for R4 | R1, R3, R5 | R2 |
| CIP-008 | 6 | Current | HIGH for R1–R3; MEDIUM for R4 | R4 (determination) | — |
| CIP-009 | 6 | Current | HIGH | — | — |
| CIP-010 | 4 | Current | MEDIUM | R3 (scope), R4 (TCA/RM) | — |
| CIP-011 | 3 | Current | MEDIUM | R1, R2 (sanitization method) | — |
| CIP-012 | 2 | **2026-07-01** | MEDIUM | R1 (mitigation method) | — |
| CIP-013 | 2 | Current (since 2022-10-01) | MEDIUM | R1 (depth), R2 (impl) | — |
| CIP-014 | 3 | Current | LOW for R5; MEDIUM for R1, R2, R4, R6 | R1, R2, R4 | R5 |
| CIP-015 | 1 | **2028-10-01 (H), ~2030-10-01 (M w/ ERC)** | MEDIUM | R1, R2, R3 | — |

---

## Open assumption registry

All assumptions require annual re-approval. Cryptographic hashes are populated on commit by the CI pipeline; placeholders shown below.

| ID | Standard | Topic | Approved by | Next review |
|---|---|---|---|---|
| ASSUME-003-001 | CIP-003-9 | "Necessary" LERC communications | Compliance Officer | 2027-04-01 |
| ASSUME-003-002 | CIP-003-9 | Vendor session disable capability | Compliance Officer | 2027-04-01 |
| ASSUME-004-001 | CIP-004-7 | "Need" for access authorization | Compliance Officer | 2027-01-15 |
| ASSUME-005-001 | CIP-005-7 | "Needed" ESP traffic | Compliance Officer | 2027-01-15 |
| ASSUME-005-002 | CIP-005-7 | Vendor session detect/disable | Compliance Officer | 2027-01-15 |
| ASSUME-006-001 | CIP-006-6 | "Equally effective" cable protection | Compliance Officer | 2027-01-15 |
| ASSUME-007-001 | CIP-007-6 | "Technically feasible" for patching | Compliance Officer | 2027-01-15 |
| ASSUME-007-002 | CIP-007-6 | Mitigation plan adequacy | Compliance Officer | 2027-01-15 |
| ASSUME-007-003 | CIP-007-6 | Password policy TFE exemption | Compliance Officer | 2027-01-15 |
| ASSUME-008-001 | CIP-008-6 | Incident "determination" timestamp | Compliance Officer | 2027-01-15 |
| ASSUME-010-001 | CIP-010-4 | TCA pre-connect scan adequacy | Compliance Officer | 2027-01-15 |
| ASSUME-011-001 | CIP-011-3 | BCSI presumed categories | Compliance Officer | 2027-01-15 |
| ASSUME-011-002 | CIP-011-3 | BCSI at-rest/in-transit protection | Compliance Officer | 2027-01-15 |
| ASSUME-011-003 | CIP-011-3 | Sanitization method | Compliance Officer | 2027-01-15 |
| ASSUME-012-001 | CIP-012-2 | Link mitigation method | Compliance Officer | 2027-05-15 |
| ASSUME-012-002 | CIP-012-2 | Control Center boundary inheritance | Compliance Officer | 2027-05-15 |
| ASSUME-013-001 | CIP-013-2 | R1.2 topic "addressed" definition | Compliance Officer | 2027-01-15 |
| ASSUME-013-002 | CIP-013-2 | Procurement in-scope determination | Compliance Officer | 2027-01-15 |
| ASSUME-014-001 | CIP-014-3 | Risk assessment methodology acceptability | Compliance Officer | 2027-01-15 |
| ASSUME-014-002 | CIP-014-3 | "Unaffiliated" third party definition | General Counsel | 2027-01-15 |
| ASSUME-014-003 | CIP-014-3 | Six-function plan coverage | Compliance Officer | 2027-01-15 |
| ASSUME-015-001 | CIP-015-1 | "Anomalous" definition | Compliance Officer | 2027-05-15 |
| ASSUME-015-002 | CIP-015-1 | Collection coverage adequacy | Compliance Officer | 2027-05-15 |
| ASSUME-015-003 | CIP-015-1 | Retention floors | Compliance Officer | 2027-05-15 |
| ASSUME-015-004 | CIP-015-1 | Data protection (chains to ASSUME-011-001) | Compliance Officer | 2027-05-15 |

---

## Contested items pending external resolution

| ID | Standard | Issue | Status |
|---|---|---|---|
| CONTEST-007-R2 | CIP-007-6 R2 | Mitigation plan adequacy varies by Regional Entity | Pattern 3 (human-surfacing) test in place; awaiting industry-wide guidance |
| CONTEST-014-R5 | CIP-014-3 R5 | "Designed collectively" adequacy of physical security measures | Pattern 3 test verifies Compliance Officer attestation; substance is auditor-determined |

---

## Pre-enforcement standards (informational mode)

| Standard | Enforcement begins | CI gate behavior |
|---|---|---|
| CIP-012-2 | 2026-07-01 (all impact levels) | `test_CIP012_v2_enforcement_window` skips assertions until date; switch to hard-fail on 2026-07-01 |
| CIP-015-1 | 2028-10-01 (H) / ~2030-10-01 (M w/ ERC) | `_in_force_for` helper gates per-asset; informational dark-launch until per-asset enforcement date |

---

## Cross-standard dependencies

The decomposition surfaces several places where the same evidence artifact satisfies multiple standards. Avoid duplicate test logic by sharing the underlying fixtures:

| Shared artifact | Standards | Notes |
|---|---|---|
| Vendor remote access session log | CIP-003-9 §6, CIP-005-7 R3, CIP-013-2 R1.2 (topic 6) | Single log; three test surfaces (Low / H/M operational / procurement) |
| Personnel access authorization | CIP-004-7 R4, CIP-006-6 R1 (PSP entry), CIP-011-3 R1 (BCSI access), CIP-015-1 R3 (INSM data access) | Same authorization workflow; CIP-004 governs cadence, others govern scope |
| Baseline configuration | CIP-010-4 R1, CIP-007-6 R1 (ports), CIP-007-6 R2 (patches) | CIP-010 is authoritative; CIP-007 tests consume the baseline data |
| Recovery / IR test record | CIP-009-6 R2, CIP-008-6 R2 | Distinct plans, but often exercised in a combined drill |
| BCSI handling controls | CIP-011-3 R1, CIP-015-1 R3 | INSM data IS BCSI; ASSUME-015-004 explicitly chains to ASSUME-011-001 |
| Software integrity verification | CIP-010-4 R1.6, CIP-013-2 R1.2 (topic 5) | CIP-013 = procurement-time process; CIP-010 = baseline-change-time technical |
| Control Center inventory | CIP-002-5.1a R1.1, CIP-012-2 R1, CIP-014-3 R5 | One inventory feeds three different scoping logics |

---

## CI/CD gate configuration

The test pipeline should be configured so that:

- **All Pattern 1 tests must PASS** on every commit to the asset inventory schema.
- **Any Pattern 2 test FAIL** routes to the engineering on-call for the asset owner; the open assumption is included in the alert payload.
- **Any Pattern 3 test FAIL** blocks the pipeline and pages the named Compliance Officer; the human determination must be refreshed before the change merges.
- **Stale-assumption detection** runs nightly; any assumption past `review_frequency_days` days creates a Pattern 3-equivalent block on all tests that depend on it.
- **Pre-enforcement standards** (CIP-012-2 until 2026-07-01; CIP-015-1 per phased dates) run in informational mode: results logged to the dashboard but not failing the pipeline. Switch to hard-fail on the enforcement date.

---

## Watch list (filed but not yet effective)

| Item | Status | Impact |
|---|---|---|
| CIP-002-8 | Filed with FERC; enforcement TBD | Tightens Control Center categorization with quantified scoring; `attachment_1_matches()` helper needs versioned dispatch ahead of enforcement |
| CIP-015-1 EACMS/PACS scope expansion | NERC Project 2025-02; target ~2026-09-01 | Will likely produce CIP-015-2 within ~2 years; INSM architecture should be designed to accommodate without rework |
| FERC Order 918/919 (CIP virtualization + low-impact controls + Control Center redefinition) | Approved 2026-03-19; 24-36 month implementation windows | Will produce new versions of multiple standards. Affects CIP-002, CIP-003, CIP-005, CIP-007, CIP-012 scoping (Control Center definition change) |
