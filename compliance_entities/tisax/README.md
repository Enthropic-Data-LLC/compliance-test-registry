# TISAX — Trusted Information Security Assessment Exchange / VDA ISA 6.0

**Authority:** ENX Association / VDA (German Association of the Automotive Industry)
**Scope:** Automotive supply chain organizations receiving vehicle project data from OEMs; AL1/AL2/AL3 assessment levels

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — 6 VDA ISA domains, confidence map, AL1/2/3 requirements, 9 assumptions | ✅ |
| [`isms-hr-physical-controls.md`](./isms-hr-physical-controls.md) | Domains 1–3: ISMS (scope, risk management, audit, management review), HR (awareness training, NDAs, screening), Physical Security (secure areas, visitor management, prototype protection at AL3), TISAX label validity gate | ✅ |
| [`it-supplier-controls.md`](./it-supplier-controls.md) | Domains 4–5: IT/InfoSec (asset inventory, least-privilege access, annual review, AES-128+ encryption, TLS 1.2+, vuln management, 90-day log retention, incident management), Supplier Management (IS flow-down contracts, sub-supplier TISAX/equivalent assessment, adequacy review) | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Domain |
|---|---|---|
| Secure area access logging | Required; all events | Domain 3 |
| Visitor escort in secure areas | Required at all times | Domain 3 |
| Access review frequency | Annual (≤12 months) | Domain 4 |
| Minimum encryption at rest | AES-128+ | Domain 4 |
| Minimum log retention | 90 days | Domain 4 |
| TISAX label validity | 3 years from assessment date | Assessment gate |
| CAP before label issued | Required for all non-conformities | Assessment gate |
| Sub-supplier assessment (AL2+) | TISAX label or equivalent for project data access | Domain 5 |

## Parse status: Complete — Domains 1–5 parsed; 2 spec files; 9 assumptions recorded
