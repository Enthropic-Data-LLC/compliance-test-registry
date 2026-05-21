# PIPEDA / Canada's Privacy Act — Personal Information Protection and Electronic Documents Act

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Collection, use, and disclosure of personal information in the course of commercial activities; applies to private-sector organizations across Canada, and to federal works, undertakings, and businesses
**Authority:** Office of the Privacy Commissioner of Canada (OPC); provincial privacy laws declared substantially similar may apply instead in QC, AB, BC for provincially regulated activities
**Current legislation:** PIPEDA (S.C. 2000, c. 5) as amended; Law 25 (Quebec) substantially similar + stricter; Alberta PIPA, British Columbia PIPA — substantially similar
**Upcoming reform:** Bill C-27 (Consumer Privacy Protection Act — CPPA) — proposes to replace PIPEDA; as of 2026 not yet in force
**Note:** Quebec Law 25 (Bill 64) modernized Quebec privacy law significantly (2022–2023 phase-in) — Quebec organizations should reference Law 25 as primary, PIPEDA as federal floor

---

## Summary

| Metric | Count |
|---|---|
| PIPEDA principles | 10 (Fair Information Principles — Schedule 1) |
| OPC enforcement | Investigations + recommendations (no direct fining power under PIPEDA — courts only) |
| Law 25 maximum fine | CAD $25M or 4% global turnover |
| PIPEDA breach notification trigger | Real risk of significant harm (RROSH) |
| Sections parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | Moderate — breach notification; consent elements; record retention |
| Partial automation (PARAMETERIZED) | Dominant — consent adequacy; safeguards appropriateness |
| Human-determination required (CONTESTED) | Moderate — "real risk of significant harm" determination |
| Open assumptions | 0 |

---

## 10 Fair Information Principles (Schedule 1) — confidence map

| Principle | Requirement | Confidence |
|---|---|---|
| 1. Accountability | Designated privacy officer; policies implemented | DETERMINISTIC existence |
| 2. Identifying purposes | Purposes identified before or at collection | DETERMINISTIC |
| 3. Consent | Meaningful consent before collection | PARAMETERIZED |
| 4. Limiting collection | Only information necessary to stated purposes | PARAMETERIZED |
| 5. Limiting use, disclosure, retention | Used only for identified purposes; not retained beyond need | PARAMETERIZED |
| 6. Accuracy | Information accurate, complete, up-to-date | PARAMETERIZED |
| 7. Safeguards | Security appropriate to sensitivity of information | PARAMETERIZED |
| 8. Openness | Privacy policies made available to individuals | DETERMINISTIC |
| 9. Individual access | Access to own information; correction rights | DETERMINISTIC — response obligation |
| 10. Challenging compliance | Process to receive and respond to complaints | DETERMINISTIC existence |

---

## Breach of security safeguards reporting (PIPEDA §10.1)

### Reporting trigger — CONTESTED/PARAMETERIZED

"Real risk of significant harm" (RROSH) analysis — factors:
- Sensitivity of the personal information
- Probability that the personal information has been, is being, or will be misused
- Whether a malicious act caused the breach

### Notification obligations (DETERMINISTIC timelines)

| Notification | Timing | Recipient |
|---|---|---|
| OPC report | "As soon as feasible" after determining RROSH exists | OPC |
| Affected individual notification | "As soon as feasible" | Each affected individual |
| Other organizations (where notification might reduce harm) | Where applicable | Other entities |

Note: "As soon as feasible" is not a defined number of hours/days — less prescriptive than GDPR 72-hour rule.

### Breach records (DETERMINISTIC)

| Obligation | Requirement |
|---|---|
| Record of every breach (regardless of RROSH) | Must be maintained |
| Record retention | 24 months from date of breach |
| OPC access to records | On request |

---

## Quebec Law 25 — key additions beyond PIPEDA

Quebec Law 25 (Privacy in the Private Sector Act) modernized Quebec privacy law significantly:

| Requirement | Deadline | Confidence |
|---|---|---|
| Privacy impact assessment (PIA) — "Technology project with PI" | Before project completion | DETERMINISTIC |
| Privacy by default | New systems and products | DETERMINISTIC |
| Breach notification to Commission d'accès à l'information (CAI) | Without delay; 72 hours in practice | DETERMINISTIC |
| Individual breach notification | Without delay if serious risk | DETERMINISTIC |
| Data portability right | By September 2023 | DETERMINISTIC |
| Right to de-indexing (search engine erasure) | On request | PARAMETERIZED |
| Privacy officer designation | Mandatory; name published on website | DETERMINISTIC |
| Consent: explicit for sensitive PI | Separate explicit consent required | DETERMINISTIC |

---

## Access request — DETERMINISTIC timelines

| Jurisdiction | Deadline |
|---|---|
| PIPEDA | 30 days (extendable 30 days with notice) |
| Quebec Law 25 | 30 days |
| Alberta PIPA | 45 days (extendable 30 days) |
| BC PIPA | 30 days (extendable 30 days) |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Consent framework | PIPEDA Schedule 1 P3, GDPR Art. 7, CCPA (opt-out model) | Different consent models — PIPEDA = opt-in for sensitive |
| Privacy notice | PIPEDA P8 (openness), GDPR Art. 13, CCPA | Different required elements |
| Breach notification | PIPEDA §10.1, GDPR Art. 33 (72h), Quebec Law 25 | PIPEDA "as soon as feasible" < GDPR 72h precision |
| Individual access rights | PIPEDA P9, GDPR Art. 15, CCPA §1798.100 | 30-day PIPEDA ≈ GDPR 1-month; CCPA 45 days |
| Privacy officer | PIPEDA P1, GDPR Art. 37 (DPO), Quebec Law 25 | Different triggers for mandatory DPO/privacy officer |
