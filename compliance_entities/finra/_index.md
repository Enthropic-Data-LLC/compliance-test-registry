# FINRA — Financial Industry Regulatory Authority Broker-Dealer Rules

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** FINRA rules applicable to FINRA-member broker-dealers and their associated persons; covers supervisory systems, books and records, trading practices, customer protection, and cybersecurity obligations
**Authority:** FINRA (self-regulatory organization); rules approved by SEC; enforcement: FINRA Department of Enforcement + SEC
**Enforcing context:** All FINRA-member firms (broker-dealers registered with SEC); associated persons (registered representatives, principals)
**Key rulebooks:** FINRA Rules (4000 series — capital; 4500 series — books and records; 3000 series — supervision); NASD Conduct Rules (carried over); Regulatory Notices

---

## Summary

| Metric | Count |
|---|---|
| Primary rule series | 5 (3000-series: supervision; 4000-series: financial; 4500-series: records; 2000-series: conduct; 1000-series: membership) |
| Books and records retention categories | Multiple (3/6/7 year retention tiers) |
| Sections parsed (individual files) | 1 (broker-dealer-supervision-records.md — WSPs, off-channel comms, books and records retention, WORM, customer protection reserve, registration filings, AML) |
| Fully automated (DETERMINISTIC) | Moderate — retention timelines; registration requirements; notice filing deadlines |
| Partial automation (PARAMETERIZED) | Dominant — supervisory system adequacy; suitability determinations |
| Human-determination required (CONTESTED) | High — supervisory reasonableness; best interest determinations |
| Open assumptions | 0 |

---

## Scoping pre-condition

```python
def is_finra_member() -> bool:
    """
    True if entity is a FINRA-member broker-dealer (SEC-registered under Section 15
    of the Securities Exchange Act of 1934). Includes:
    - Full-service broker-dealers
    - Introducing and clearing firms
    - Investment banks (underwriting activities)
    Does NOT include: investment advisers (RIA-only), exchanges, banks (unless
    also broker-dealer registered).
    """
```

---

## Supervision — Rule 3110 (core obligation)

### Written Supervisory Procedures (WSPs) — DETERMINISTIC

| Requirement | Confidence | Notes |
|---|---|---|
| Written supervisory procedures established | DETERMINISTIC | WSPs must be written; reviewed and updated |
| WSPs reasonably designed to achieve compliance | CONTESTED | Adequacy is a regulatory judgment |
| OSJ (Office of Supervisory Jurisdiction) designation | DETERMINISTIC | Each OSJ identified; registered principal designated |
| Principal supervisor for each type of business | DETERMINISTIC | Named supervisory principal per product line |
| Annual review of supervisory systems | DETERMINISTIC | Annual review documented |
| Review of transactions and correspondence | PARAMETERIZED | Frequency and methodology org-defined |

### Supervisory review of electronic communications — Rule 3110(b)

| Requirement | Confidence | Notes |
|---|---|---|
| Review of electronic correspondence | PARAMETERIZED | Risk-based review; methodology documented |
| Business-related communications on personal devices | PARAMETERIZED | Requires documented policy; monitoring capability |
| Off-channel communication prohibition or surveillance | DETERMINISTIC — firms must either prohibit or capture | SEC enforcement trend: off-channel comm = books and records violation |

---

## Books and records — Rules 4510–4530 (DETERMINISTIC retention)

| Record type | Retention | Rule |
|---|---|---|
| Blotters and ledgers | 6 years (3 years in accessible place) | Rule 4510, SEA Rule 17a-3 |
| Customer account records | 6 years | Rule 4510, SEA Rule 17a-3 |
| Order tickets | 3 years | SEA Rule 17a-3(a)(6) |
| Electronic communications (business-related) | 3 years | Rule 4511 |
| Written supervisory procedures | 3 years after superseded | Rule 4110 |
| Customer complaints | 4 years | Rule 4530 |
| Licensing and registration records | 3 years after termination | — |
| Trade confirmations | 3 years | SEA Rule 17a-3 |

**WORM (Write Once Read Many) requirement:** Electronic records must be stored in non-erasable, non-rewritable format for required retention period (Rule 4511).

---

## Customer protection — Rule 4311 / SEA Rule 15c3-3

| Requirement | Confidence | Notes |
|---|---|---|
| Customer fully-paid securities in good control | DETERMINISTIC | Segregation of customer assets |
| Reserve formula computation | DETERMINISTIC — weekly | Free credit balance calculation every week |
| Reserve deposit in special account | DETERMINISTIC — next business day | Reserve must be deposited promptly |
| PAB (Proprietary Accounts of Broker-dealers) account | DETERMINISTIC | Separate PAB reserve calculation |

---

## Regulatory Notices — cybersecurity (DETERMINISTIC obligations)

### Regulatory Notice 21-18, 11-26, 15-37 guidance

| Obligation | Confidence | Notes |
|---|---|---|
| Cybersecurity risk management program | PARAMETERIZED — no bright-line rule; but expected | Annual review documented |
| Customer identity verification (AML/KYC) | DETERMINISTIC — Rule 3310 BSA/AML program | Written AML program; annual testing |
| Incident notification to FINRA | PARAMETERIZED — for events affecting operations | Prompt notification of material events |
| Cybersecurity training | PARAMETERIZED | Annual training recommended |

---

## Form U4 / U5 — registration and termination (DETERMINISTIC timelines)

| Event | Filing deadline | Form |
|---|---|---|
| New registration | Before person engages in business | Form U4 |
| Material change to U4 | Within 30 days | Form U4 amendment |
| Statutory disqualification event | Prompt (within 30 days) | Form U4 |
| Termination of registration | Within 30 days | Form U5 |
| Termination for cause — internal investigation | Within 30 days of conclusion | Form U5 (amended) |

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Rule |
|---|---|---|
| Electronic records retention | 3 years minimum | Rule 4511 |
| General books and records | 6 years | SEA Rule 17a-4 |
| Reserve formula computation | Weekly | SEA Rule 15c3-3 |
| Annual supervisory review | Once per year | Rule 3110 |
| Form U5 filing | 30 days after termination | Rule 1010 |
| WORM electronic storage | Required format for all required records | Rule 4511 |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Books and records | FINRA Rules 4510–4530, SEC SEA Rule 17a-3/17a-4, CFTC 1.31 | Same record retention infrastructure; different time requirements by record type |
| AML/BSA | FINRA Rule 3310, BSA/FinCEN, OFAC SDN screening | Same AML program; FINRA Rule 3310 = BSA compliance |
| Supervisory procedures | FINRA Rule 3110, SEC Reg BI (best interest), MSRB G-27 | WSPs must address Reg BI and suitability obligations |
| Cybersecurity | FINRA RN 21-18, SEC Cybersecurity Rules 2023, NYDFS §500 | NYC-based BD: NYDFS §500 applies; SEC 8-K for material incidents |
| Off-channel communications | FINRA Rule 4511, SEC Order 2022 (off-channel enforcement wave), CFTC parallel actions | SEC/CFTC/FINRA coordinated enforcement; same WhatsApp/Signal issue |
