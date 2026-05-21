# GDPR — EU General Data Protection Regulation

**Authority:** European Data Protection Board (EDPB); national supervisory authorities (DPAs) per member state
**Scope:** Processing of personal data of EU/EEA data subjects by controllers and processors established in the EU/EEA, or targeting EU/EEA data subjects from outside

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — Articles mapped, confidence map, 17 open assumptions, CI gate config | ✅ |
| [`core-articles.md`](./core-articles.md) | Art. 12 (DSR timelines), Art. 13/14 (privacy notices), Art. 28 (DPA), Art. 30 (ROPA), Art. 32 (security), Art. 33/34 (breach notification), Art. 35 (DPIA), Art. 37 (DPO), Chapter V (international transfers) | ✅ |
| [`principles-lawful-basis.md`](./principles-lawful-basis.md) | Art. 5 (principles — storage limitation, accuracy, purpose limitation, accountability), Art. 6 (lawful basis — consent records/withdrawal, LIA), Art. 9 (special category data — identification, Art. 9(2) conditions, explicit consent, enhanced security) | ✅ |
| [`data-subject-rights-design.md`](./data-subject-rights-design.md) | Art. 17 (right to erasure — deadline, outcome, third-party propagation, technical procedure), Art. 20 (portability — deadline, machine-readable format, direct transfer), Art. 21 (right to object — direct marketing absolute, LIA objection, research override), Art. 25 (privacy by design/default — by-default config, SDLC review, DPO attestation) | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Article |
|---|---|---|
| Breach notification to supervisory authority | Within 72 hours of becoming aware | Art. 33 |
| DSR response (access, portability, erasure) | Within 1 month; extendable 2 months with notice | Art. 12 |
| Direct marketing objection | Must cease immediately — no override permitted | Art. 21(2)/(3) |
| Consent withdrawal processing | Within 30 days of receipt | Art. 12(3) |
| All processing must have documented lawful basis | Binary — absence is a per se violation | Art. 6 |
| Portability format | Structured, commonly used, machine-readable (JSON/CSV/XML) | Art. 20(1) |
| DPIA prior consultation response from SA | Within 8 weeks (extendable 6 weeks) | Art. 36 |
| Data retention | No longer than necessary for purpose | Art. 5(1)(e) |
| Personal data accessibility default | Must default to private/restricted — not public | Art. 25(2) |

## Parse status: Complete — all focused-scope articles parsed; 3 spec files; 17 assumptions recorded
