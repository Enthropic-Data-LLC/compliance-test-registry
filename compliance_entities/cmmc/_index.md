# CMMC 2.0 — Cybersecurity Maturity Model Certification

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** All three levels; 14 domains; ~134 practices at Level 3 maximum
**Authority:** U.S. Department of Defense (DoD) / OUSD(A&S)
**Enforcing context:** DFARS 252.204-7021 (effective Dec 2024); required for DoD contracts handling FCI or CUI
**Regulatory basis:** 32 CFR Part 170 (CMMC Program final rule, Dec 16 2024)

---

## Summary

| Metric | Count |
|---|---|
| Levels | 3 |
| Domains | 14 |
| Level 1 practices | 17 (= FAR 52.204-21 basic safeguarding requirements) |
| Level 2 practices | 110 (= NIST SP 800-171 r2) |
| Level 3 practices | 134 (= 800-171 r2 + 24 selected from NIST 800-172 r1) |
| Practices parsed (individual files) | 1 (Level 1 + Level 2 mapping; practice-level tests in 800-171 family files) |
| Open assumptions | 2 (ASSUME-CMMC-001–002: SPRS scoring, annual affirmation) |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Level architecture

| Level | Scope | Practice source | Assessment method | Cadence |
|---|---|---|---|---|
| Level 1 | Federal Contract Information (FCI) only | FAR 52.204-21 (17 practices) | Annual self-assessment + annual affirmation in SPRS | Annual |
| Level 2 (self) | CUI — less sensitive programs | NIST 800-171 r2 (110 practices) | Triennial self-assessment + annual affirmation in SPRS | Self: annual affirmation; tri: full assessment |
| Level 2 (C3PAO) | CUI — sensitive/critical programs | NIST 800-171 r2 (110 practices) | Triennial C3PAO assessment; annual affirmation | Triennial |
| Level 3 | CUI — highest priority programs | 800-171 r2 + 24 from 800-172 r1 | DCSA-led government assessment | Triennial |

> **Note:** DoD determines which level applies per contract. Level 2 C3PAO or Level 3 requirements appear in the solicitation. Self-assessment vs. third-party is not contractor-elected.

---

## Per-domain confidence map

| Domain | Abbrev | Level 1 | Level 2 | Level 3 delta | PARAMETERIZED surface | CONTESTED surface |
|---|---|---|---|---|---|---|
| Access Control | AC | 2 | 22 | +2 (800-172) | Remote access method; CUI access least privilege | — |
| Asset Management | AM | — | — | +2 (800-172) | Asset inventory completeness | — |
| Audit and Accountability | AU | — | 9 | +1 | Log review frequency | — |
| Awareness and Training | AT | — | 3 | +1 | Training content adequacy | — |
| Configuration Management | CM | — | 9 | +2 | Baseline approval process; blacklisting completeness | — |
| Identification and Authentication | IA | 4 | 11 | +1 | MFA exception handling | — |
| Incident Response | IR | — | 3 | +2 | Response capability adequacy | — |
| Maintenance | MA | — | 6 | — | Remote maintenance controls | — |
| Media Protection | MP | 1 | 9 | — | Sanitization method | — |
| Physical Protection | PE | 2 | 6 | — | — | — |
| Recovery | RE | — | — | +1 | Recovery capability | — |
| Risk Management | RM | — | 3 | +3 | Risk methodology; vulnerability remediation prioritization | Risk tolerance |
| Security Assessment | CA | — | 4 | +3 | Assessment scope; pentesting scope | — |
| Situational Awareness | SA | — | — | +2 | Threat intel timeliness | — |
| System and Communications Protection | SC | — | 16 | +2 | Cryptographic method adequacy | — |
| System and Information Integrity | SI | — | 7 | +2 | Flaw remediation timeline; advanced threat hunting | — |
| Supply Chain Risk Management | SR | — | — | +2 (800-172) | Supplier assessment adequacy | Supply chain controls sufficiency |

> Domain counts above are approximate. Level 1 (17) + Level 2 (110) + Level 3 delta (+24) = 134 Level 3 practices total.

---

## SPRS score — pre-condition to Level 2 self-assessment

All Level 2 self-assessors must calculate and submit a SPRS (Supplier Performance Risk System) score (range: -203 to +110) before contract award. Score = 110 minus points deducted for each unimplemented practice. A score below 110 requires a Plan of Action and Milestones (POA&M) with completion dates.

| SPRS decision | Classification | Notes |
|---|---|---|
| Is a practice implemented? | DETERMINISTIC for most; PARAMETERIZED for "adequacy" practices | Binary for most practices at score calculation time |
| POA&M acceptability | CONTESTED | Contracting officers evaluate POA&M adequacy case-by-case |
| "Not applicable" determination | PARAMETERIZED | Requires documented rationale tied to system scope |

---

## Open assumption registry

| ID | Level/Domain | Summary | Review date |
|---|---|---|---|
| ASSUME-CMMC-001 | Level 2 SPRS | Score: 110 practices assessed against 800-171A; DoD point weights; POA&M ≤180 days; N/A requires rationale | 2026-05-20 |
| ASSUME-CMMC-002 | Levels 1+2 Affirmation | Annual affirmation: Senior Official within 12 months; accurately reflects current status; updated if implementation changed | 2026-05-20 |

---

## Contested items pending resolution

| Item | Level | Reason | Resolution path |
|---|---|---|---|
| POA&M acceptability | Level 2 | Contracting officers evaluate POA&M adequacy case-by-case; no objective threshold | CO review + legal counsel for contract-specific determination |
| "Not applicable" determination | Level 2 | Requires documented rationale; scope exclusion adequacy is assessor-evaluated | ISSO documents rationale in SSP; C3PAO/assessor concurrence required |
| Level 3 program eligibility | Level 3 | DoD program office determines which programs require Level 3; not self-determined | DCSA assessment upon designation |

## Specification file status

| File | Contents | Confidence | Status |
|---|---|---|---|
| `level1-level2-practices.md` | Level 1 (17 FAR 52.204-21 practices); Level 2 domain-to-800-171 mapping; SPRS scoring; annual affirmation | HIGH | ✅ Parsed |
| *(Level 3 — 800-172 delta)* | 24 additional practices from NIST 800-172 r1 | MEDIUM | 🔲 Pending |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| NIST 800-171 SSP | CMMC Level 2, 800-171, FedRAMP (if applicable) | Level 2 C3PAO assessment is scored against the SSP; same document feeds all three frameworks |
| SPRS score | CMMC Level 2 self-assessment, DoD DFARS | SPRS submission is mandatory before contract award; score is derived from SSP and POA&M |
| POA&M | CMMC Levels 2+3, 800-171, FedRAMP | CMMC allows conditional certification with POA&M; FedRAMP ATO can be granted with open POA&M items |
| Audit logs | CMMC AU, 800-171 AU, FedRAMP AU | Consistent log content across all three; CMMC adds SIEM affirmation requirement at Level 3 |
| Risk assessment | CMMC RM, 800-171 RA, FedRAMP RA | Methodology documented in SSP must satisfy all active frameworks |
| Incident response plan | CMMC IR, 800-171 IR | CMMC IR.2.092–IR.3.098 maps 1:1 to 800-171 IR family |

---

## CI/CD gate configuration

Standard three-tier gate (see NERC CIP registry). CMMC-specific constraints:

- **Scope fixture:** System must be categorized (FCI-only or CUI) before level-appropriate tests are selected.
- **SPRS score test:** A synthetic test computes the current SPRS score from the practice implementation matrix and fails if it is below the contract-required floor.
- **POA&M staleness:** Any open POA&M item older than its committed completion date triggers a Pattern 3 gate requiring Compliance Officer attestation.
- **Affirmation cadence:** Annual affirmation deadline tracked as a time-bounded test; fails when `today > last_affirmation_date + 365 days`.

---

## Roadmap — individual practice file parse priority

Parse aligned with 800-171 roadmap since Level 2 = 800-171 r2 exactly:

| Priority | Domain | Notes |
|---|---|---|
| 1 | AC | Highest practice count; Level 1 subset covers 2 basic safeguarding practices |
| 2 | IA | Level 1 covers 4 practices; MFA thresholds are DETERMINISTIC |
| 3 | AU | Fully Level 2+; no Level 1 requirement — important for gap analysis |
| 4 | CM | HIGH confidence; baseline and change control |
| 5 | SC | CUI-in-transit encryption — DETERMINISTIC |
| 6 | SI | Flaw remediation — DETERMINISTIC cadence |
| 7 | Level 3 delta (24 practices) | Parse after Level 2 baseline complete; 800-172 sources |

---

## Watch list

| Item | Status | Impact |
|---|---|---|
| CMMC Level 2 alignment to 800-171 r3 | DoD roadmap TBD | Current Level 2 uses r2 (110 reqs); r3 alignment expected in future rulemaking — will add ~7 new practices |
| CMMC marketplace (C3PAO availability) | Active backlog | Limited certified C3PAOs; assessment scheduling risk for Level 2 C3PAO contracts |
| Conditional CMMC (POA&M window) | Defined in 32 CFR 170 | 180-day POA&M window allowed for up to 20% of practices; practices in the "not met" category for POA&M must be specifically excluded from the SPRS deduction calculation |
| 48 CFR Part 204 (CMMC DFARS rule) | Proposed rule 2023; final rule pending | Contracts clause will embed CMMC level requirement in solicitations |
