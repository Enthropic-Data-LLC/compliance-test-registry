# CCPA / CPRA — California Consumer Privacy Act / Privacy Rights Act

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** California Consumer Privacy Act (effective 2020) as amended by California Privacy Rights Act (effective Jan 1 2023); California Privacy Protection Agency (CPPA) enforcement regulations
**Authority:** California Privacy Protection Agency (CPPA) + California Attorney General (AG)
**Enforcing context:** For-profit businesses that: (1) have gross annual revenues > $25M; OR (2) buy, sell, or share personal information of ≥ 100,000 consumers or households; OR (3) derive ≥ 50% of annual revenues from selling or sharing consumers' personal information — AND do business in California or with California consumers
**Note:** This registry covers CCPA/CPRA. For multi-state coverage, see companion state privacy law entries when added. Most state privacy laws (VCDPA, CPA, CTDPA, etc.) are architecturally similar to CPRA.

---

## Summary

| Metric | Count |
|---|---|
| Rights granted to consumers | 11 |
| Business obligation categories | 7 |
| Technically testable obligations | ~25 |
| Obligations parsed (individual files) | 0 (index only; individual section files pending) |
| Fully automated (DETERMINISTIC) | Moderate — response deadlines, opt-out links, data retention schedules |
| Partial automation (PARAMETERIZED) | Dominant — notice adequacy, security "appropriate to risk" |
| Human-determination required (CONTESTED) | Significant — proportionality, "sensitive personal information" scope |
| Open assumptions | 0 |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Applicability threshold — pre-condition to all tests

| Threshold | Test | Classification |
|---|---|---|
| Revenue threshold | Gross annual revenues > $25M | DETERMINISTIC |
| Data volume threshold | Buy/sell/share PI of ≥ 100,000 consumers or households/year | DETERMINISTIC |
| Revenue-from-data threshold | ≥ 50% of annual revenues from selling/sharing PI | DETERMINISTIC |
| California nexus | Does business in California or with California consumers | PARAMETERIZED |

If none of the first three criteria are met, the business is not a "business" under CCPA/CPRA. All tests are gated by `is_covered_business()` fixture.

---

## Consumer rights — confidence map

| Right | Code Section | Response deadline | Confidence | Notes |
|---|---|---|---|---|
| Right to know (categories) | §1798.110 | 45 days (extendable +45) | DETERMINISTIC | Deadline is bright-line; content is PARAMETERIZED |
| Right to know (specific pieces) | §1798.115 | 45 days (extendable +45) | DETERMINISTIC | Same deadline; portability format is PARAMETERIZED |
| Right to delete | §1798.105 | 45 days (extendable +45) | DETERMINISTIC | Deadline is DETERMINISTIC; deletion verification across third parties is PARAMETERIZED |
| Right to correct | §1798.106 | 45 days (extendable +45) | DETERMINISTIC | — |
| Right to opt-out of sale/sharing | §1798.120 | Opt-out must be honored within 15 business days | DETERMINISTIC | "Do Not Sell or Share My Personal Information" link must be present on homepage |
| Right to limit use of sensitive PI | §1798.121 | Opt-out honored within 15 business days | DETERMINISTIC | "Limit the Use of My Sensitive Personal Information" link required |
| Right to non-discrimination | §1798.125 | N/A | PARAMETERIZED | Cannot deny goods/services, charge different price, or provide different quality for exercising rights |
| Right to opt-out of automated decision-making | §1798.185(a)(16) (CPRA) | Per CPPA regulations | CONTESTED | CPPA regulations still developing |
| Right to know about automated decision-making | §1798.185(a)(16) | Per CPPA regulations | CONTESTED | — |
| Right to appeal | Via CPPA complaint | N/A | PARAMETERIZED | Complaint mechanism adequacy |
| Right to access contractor/service provider data | §1798.115(c) | 45 days | PARAMETERIZED | Disclosure of service providers who have PI |

---

## Business obligations — confidence map

### Privacy Notice / Privacy Policy (§1798.100, §1798.130)

| Requirement | Confidence | Notes |
|---|---|---|
| Privacy policy publicly posted | DETERMINISTIC | Binary — URL accessible |
| Privacy policy updated within 12 months | DETERMINISTIC | Last-updated date tracked |
| Policy includes required disclosure elements | PARAMETERIZED | 10+ required elements; completeness is PARAMETERIZED |
| Notice at collection | PARAMETERIZED | At or before point of collection; content adequacy |
| "Do Not Sell or Share" link on homepage | DETERMINISTIC | Binary presence check |
| "Limit Sensitive PI" link on homepage | DETERMINISTIC | Binary presence check (if sensitive PI processed) |

### Data Subject Request (DSR) infrastructure (§1798.130)

| Requirement | Confidence | Notes |
|---|---|---|
| At least two request submission methods | DETERMINISTIC | Must offer ≥ 2 methods (toll-free number + web form minimum) |
| 45-day initial response | DETERMINISTIC | Clock starts on receipt of verifiable consumer request |
| Extension notice | DETERMINISTIC | If using 45-day extension: must notify consumer within initial 45 days |
| Verification process | PARAMETERIZED | Must reasonably verify identity without being "unnecessarily burdensome" |
| Record-keeping (24-month) | DETERMINISTIC | Records of requests and responses retained 24 months |

### Opt-out mechanisms (§1798.120, §1798.135)

| Requirement | Confidence | Notes |
|---|---|---|
| Opt-out honored within 15 business days | DETERMINISTIC | Bright-line threshold |
| Global Privacy Control (GPC) honored | DETERMINISTIC | Must recognize GPC browser signal as valid opt-out (CPPA enforcement priority) |
| Re-sale to third parties restricted post-opt-out | DETERMINISTIC | Third parties notified of opt-out; cannot re-sell for 12 months without new consent |

### Sensitive Personal Information (SPI) (§1798.121)

CPRA created a new category. SPI includes: SSN, DL, financial account credentials, precise geolocation, race/ethnicity/religion, union membership, genetic data, biometric data, health data, sexual orientation/sex life, and contents of personal communications.

| Requirement | Confidence | Notes |
|---|---|---|
| SPI identified in data inventory | PARAMETERIZED | SPI inventory completeness |
| "Limit SPI use" link if SPI used beyond permitted purposes | DETERMINISTIC | Binary link presence if applicable |
| SPI use limited to service delivery | PARAMETERIZED | "Necessary" use scope |

### Data Retention (§1798.100(a)(3))

| Requirement | Confidence | Notes |
|---|---|---|
| Retention periods disclosed in privacy policy | PARAMETERIZED | Policy must state retention period or criteria for each category |
| Retention not longer than reasonably necessary | PARAMETERIZED | "Reasonably necessary" — proportionality determination |
| Retention schedule enforced | PARAMETERIZED | Technical enforcement of stated periods |

### Security (§1798.150 — private right of action)

| Requirement | Confidence | Notes |
|---|---|---|
| Reasonable security procedures | CONTESTED | No bright-line security standard specified; CA AG has pointed to CIS Controls as a reference benchmark |
| Non-encrypted/non-redacted PI exposed in breach | DETERMINISTIC | Triggers private right of action; $100–$750 per consumer per incident |

### Contracts with Service Providers / Contractors / Third Parties (§1798.140)

| Requirement | Confidence | Notes |
|---|---|---|
| Written contract with service providers | DETERMINISTIC | Written contract required before disclosing PI to service providers |
| Contract prohibits unauthorized use | PARAMETERIZED | Required contract terms (7 elements in §1798.140(e)) |
| Annual risk assessments | PARAMETERIZED | Required for processing posing "significant risk" (CPPA regulations define scope) |

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Section |
|---|---|---|
| DSR response deadline | 45 days from receipt (extendable once by 45 days with notice) | §1798.130 |
| Opt-out honoring deadline | 15 business days | §1798.120(b)(2) |
| "Do Not Sell or Share" link | Must be on homepage and in privacy policy | §1798.135(a)(1) |
| GPC signal recognition | Must be honored as a valid opt-out | CPPA regs |
| Privacy policy update | At least every 12 months | §1798.130(a)(5) |
| DSR records retention | 24 months | §1798.185(a)(8) |
| Re-sale restriction after opt-out | 12 months before re-authorization solicitation | §1798.120(c) |
| Breach private right of action | Non-encrypted/non-redacted PI exposed | §1798.150 |

---

## Open assumption registry

*(No assumptions recorded — individual section files not yet written)*

---

## Contested items pending resolution

| ID | Section | Issue | Status |
|---|---|---|---|
| CONTEST-CCPA-001 | §1798.150 | "Reasonable security" — no statutory definition; CA AG points to CIS Controls but no binding standard | Pattern 3 gate; requires Compliance Officer attestation against chosen security framework |
| CONTEST-CCPA-002 | §1798.185(a)(16) | Automated decision-making right — CPPA regulations in development; scope of "significant decisions" not yet finalized | Pattern 3 gate; informational mode until CPPA regulations finalized |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Privacy notice / policy | CCPA/CPRA, GDPR Art. 13–14, GLBA §313.4–5 | Different required elements; a combined layered notice can satisfy all if organized by jurisdiction |
| Data subject request infrastructure | CCPA/CPRA (45 days), GDPR Art. 12 (30 days), HIPAA (30 days for access) | Different deadlines and scope; shared DSR platform with jurisdiction-specific routing |
| Data inventory / records of processing | CCPA/CPRA (categories + retention), GDPR Art. 30 (ROPA), HIPAA addressable | A unified data inventory with jurisdiction-specific fields satisfies all three |
| Opt-out / consent management | CCPA/CPRA, GDPR (consent + legitimate interests withdrawal), GLBA opt-out | Different legal bases; shared consent management platform with jurisdiction-specific logic |
| Service provider contracts | CCPA/CPRA §1798.140, GDPR Art. 28 DPA, HIPAA BAA | Combined contract template; GDPR Art. 28 mandatory elements are the most specific |
| Security (reasonable) | CCPA/CPRA §1798.150, GLBA Safeguards Rule, HIPAA §164.312, ISO 27001 A.5–8 | All use a "reasonable/appropriate" standard; implementing a recognized framework (ISO 27001, CIS Controls) creates a defensible position across all |

---

## State privacy law landscape (companion frameworks — not yet parsed)

As of 2026, 19+ states have enacted GDPR/CPRA-style privacy laws. All share the same architectural pattern (rights-based, consent-based, service provider obligations) with varying thresholds and exemptions:

| State | Law | Effective |
|---|---|---|
| Virginia | VCDPA | Jan 1 2023 |
| Colorado | CPA | Jul 1 2023 |
| Connecticut | CTDPA | Jul 1 2023 |
| Utah | UCPA | Dec 31 2023 |
| Texas | TDPSA | Jul 1 2024 |
| Montana | MCDPA | Oct 1 2024 |
| Oregon | OCPA | Jul 1 2024 |
| Delaware | DPDPA | Jan 1 2025 |
| Iowa | ICDPA | Jan 1 2025 |
| New Hampshire | NHPPA | Jan 1 2025 |
| New Jersey | NJDPA | Jan 15 2025 |
| Nebraska | NDPA | Jan 1 2025 |
| Tennessee | TIPA | Jul 1 2025 |
| Indiana | INCDPA | Jan 1 2026 |
| Kentucky | KCDPA | Jan 1 2026 |
| Maryland | MODPA | Oct 1 2025 |
| Minnesota | MNDPA | Jul 31 2025 |

**Recommendation:** Parse state laws as a delta-from-CPRA model. Most obligations are identical; only threshold differences, exemptions, and cure periods need individual entries.
