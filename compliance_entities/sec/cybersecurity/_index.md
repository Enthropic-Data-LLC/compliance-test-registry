# SEC Cybersecurity Rules — 17 CFR Parts 229, 232, 239, 240, 249

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Cybersecurity incident disclosure (Item 1.05 Form 8-K) + Annual cybersecurity risk management disclosure (Item 106 Regulation S-K)
**Authority:** U.S. Securities and Exchange Commission (SEC)
**Enforcing context:** All public companies registered with the SEC (domestic + foreign private issuers with modifications); effective December 15 2023 for large accelerated filers; June 15 2024 for all others
**Note:** These rules operate alongside SOX ITGCs. SOX governs IT controls over financial reporting; SEC cybersecurity rules govern disclosure of material cybersecurity incidents and risk management practices to investors.

---

## Summary

| Metric | Count |
|---|---|
| Rules | 2 (Form 8-K Item 1.05 + Regulation S-K Item 106) |
| Sections parsed (individual files) | 1 |
| Fully automated (DETERMINISTIC) | Moderate — 4-business-day filing deadline, disclosure content checklist |
| Partial automation (PARAMETERIZED) | Moderate — "material" determination |
| Human-determination required (CONTESTED) | Significant — materiality is a legal/business judgment |
| Open assumptions | 5 |

---

## Rule 1 — Form 8-K Item 1.05: Material Cybersecurity Incident Disclosure

### Obligation

Public companies must disclose material cybersecurity incidents on Form 8-K **within 4 business days** of determining that the incident is material.

### Materiality — the central CONTESTED determination

Materiality follows the existing SEC materiality standard (TSC Industries v. Northway): information is material if there is a substantial likelihood that a reasonable investor would consider it important.

No bright-line threshold exists. Factors considered:
- Scope of data compromised
- Financial impact (direct costs, remediation, lost business)
- Operational disruption duration
- Regulatory and legal exposure
- Reputational harm
- Customer/third-party notification obligations triggered

**RDF treatment:** Materiality determination is CONTESTED — it requires a named legal/executive determination and is a Pattern 3 gate. Once materiality is determined, the 4-business-day filing clock is DETERMINISTIC.

### 4-business-day filing clock

| Event | Trigger | Deadline |
|---|---|---|
| Materiality determination | Company determines incident is material | 4 business days from determination |
| Delay exception | DOJ national security/public safety exception | DOJ notifies SEC; can extend up to 60 days + additional 60 days |

**Critical distinction:** The clock starts at **determination**, not at **discovery**. Companies can take reasonable time to investigate before determining materiality, but cannot delay indefinitely.

### Required 8-K disclosures (Item 1.05(a)) — DETERMINISTIC checklist

Each Form 8-K Item 1.05 must include, to the extent known at the time of filing:
1. Nature, scope, and timing of the incident
2. Material impact or reasonably likely material impact on the registrant

**Not required in initial 8-K:**
- Specific technical information that would impede incident response
- Information not yet determined

Amended 8-K required when material information omitted from initial filing becomes available.

---

## Rule 2 — Regulation S-K Item 106: Annual Cybersecurity Disclosure

### Obligation

Annual reports (Form 10-K / 20-F for foreign private issuers) must include disclosures on:

#### Sub-item 106(b) — Cybersecurity Risk Management and Strategy

| Disclosure element | Confidence | Notes |
|---|---|---|
| Whether the company has a process to assess, identify, and manage material cybersecurity risks | DETERMINISTIC | Binary — process exists or it doesn't |
| Whether the process is integrated into overall enterprise risk management | PARAMETERIZED | Integration adequacy |
| Whether the company uses third-party assessors, consultants, auditors, or other third parties in connection with the cybersecurity risk management process | DETERMINISTIC | Binary disclosure |
| Whether the company has cybersecurity risk processes to oversee third-party service provider risks | PARAMETERIZED | Process adequacy |
| Whether previous or current cybersecurity incidents have materially affected strategy, results of operations, or financial condition | DETERMINISTIC | Binary disclosure; if yes, description required |

#### Sub-item 106(c) — Cybersecurity Governance

| Disclosure element | Confidence | Notes |
|---|---|---|
| Board of directors' oversight of cybersecurity risk | PARAMETERIZED | Which board body (committee or full board); how it is informed; how often |
| Management's role in assessing and managing material cybersecurity risks | PARAMETERIZED | Which management positions responsible; relevant expertise; reporting to board |
| Whether and how cybersecurity incidents are reported to management | PARAMETERIZED | Escalation process description |

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Rule |
|---|---|---|
| Material incident 8-K filing | 4 business days from materiality determination | Form 8-K Item 1.05 |
| DOJ delay — national security | Up to 60 days; renewable for additional 60 days | Item 1.05(c) |
| Annual disclosure | Annual report (10-K/20-F) filing deadline | S-K Item 106 |
| Amended 8-K | When previously omitted material information becomes available | Item 1.05 instructions |

---

## Interaction with other incident notification frameworks

Multiple incident notification obligations may apply simultaneously. The SEC 4-business-day clock is the tightest for public companies (excluding DORA's 4-hour initial notification for EU financial entities):

| Framework | Trigger | Deadline | Recipient |
|---|---|---|---|
| SEC 8-K | Material cybersecurity incident determination | 4 business days | SEC (public filing) |
| NY DFS §500.17 | Cybersecurity event meeting threshold | 72 hours | NY DFS Superintendent |
| GDPR Art. 33 | Personal data breach | 72 hours | National DPA |
| HIPAA §164.408 | PHI breach | 60 calendar days | HHS OCR |
| DORA Art. 19 | Major ICT incident classification | 4 hours (initial) | National competent authority |

An organization subject to multiple frameworks must run all applicable notification tracks in parallel.

---

## Foreign Private Issuer (FPI) modifications

FPIs use Form 20-F (annual) and Form 6-K (current reports). Key differences:
- Material incident disclosure on Form 6-K (not 8-K) — same 4-business-day deadline
- Annual disclosure on Form 20-F Item 16K

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Materiality determination process | SEC Cybersecurity Rules, SOX §302/404, SEC MD&A | Same executive sign-off process; cybersecurity materiality is now a board-level governance topic |
| Board cybersecurity oversight | SEC S-K Item 106(c), GLBA §314.4(k), DORA Art. 5 | Annual board reporting now required by all three; same board presentation can address all |
| Incident response plan | SEC 8-K Item 1.05, NY DFS §500.16, HIPAA §164.308(a)(6), GDPR Art. 33 | IRP must include SEC notification workflow; 4-business-day clock tracked from materiality determination |
| Third-party risk management | SEC S-K Item 106(b), SOC 2 CC9.2, GLBA §314.4(f) | Disclosure of TPRM process; same vendor management program |
| Cybersecurity risk management process | SEC S-K Item 106(b), NIST CSF 2.0 GV/ID, SOX ITGCs | NIST CSF language is widely used in 10-K disclosures to describe the risk management process |

---

## Spec file status

| File | Coverage | Status |
|---|---|---|
| [`incident-disclosure-annual-report.md`](./incident-disclosure-annual-report.md) | Form 8-K Item 1.05 (4-business-day clock, DOJ delay, 8-K/A amendment), S-K Item 106(b) (risk management disclosures), S-K Item 106(c) (governance disclosures), multi-framework notification coordination, FPI modifications (Form 6-K / 20-F) | ✅ |

## Open assumption registry

| ID | Assumption | Pattern | Approved | Review |
|---|---|---|---|---|
| ASSUME-SEC-DISC-001 | "Business days" = Mon–Fri excluding US federal holidays, consistent with SEC conventions | 1 | Pending | 2027-05 |
| ASSUME-SEC-MAT-001 | 4-business-day clock starts at formal materiality determination date; discovery alone does not start the clock | 3 | Pending | 2027-05 |
| ASSUME-SEC-DOJ-001 | DOJ delay requires DOJ (not registrant) to notify SEC; registrant must document the DOJ notification | 1 | Pending | 2027-05 |
| ASSUME-SEC-AMD-001 | 8-K/A amendment timing is "as soon as practicable" — Pattern 2; no bright-line days | 2 | Pending | 2027-05 |
| ASSUME-SEC-106-001 | S-K Item 106 element presence is DETERMINISTIC; substantive adequacy is Pattern 2 requiring Disclosure Committee approval | 2 | Pending | 2027-05 |

## Parse status: Complete — Form 8-K Item 1.05, S-K Item 106(b)/(c) parsed; 5 assumptions recorded
