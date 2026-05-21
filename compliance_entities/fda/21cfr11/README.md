# FDA 21 CFR Part 11 — Electronic Records and Electronic Signatures

**Authority:** U.S. Food and Drug Administration (FDA)
**Scope:** Electronic records and electronic signatures used in lieu of paper records or handwritten signatures in FDA-regulated activities; applies to drug, biologics, medical device, food, and cosmetic manufacturers using computerized systems

## Contents

| File | Coverage | Status |
|---|---|---|
| [`_index.md`](./_index.md) | Registry index — §11.10/11.50/11.70/11.100/11.200/11.300 mapped, 13 open assumptions | ✅ |
| [`electronic-records-esig.md`](./electronic-records-esig.md) | §11.10 controls (audit trail, access, copies), §11.50 signature manifestations, §11.70 signature/record link, §11.100 uniqueness + FDA certification letter, §11.200 two-component signing | ✅ |
| [`system-validation.md`](./system-validation.md) | §11.10(a) GAMP 5 validation (categories 1/3/4/5), §11.10(f) operational checks, §11.10(i) personnel qualification, §11.10(j) written policies, §11.30 open systems | ✅ |

## Key DETERMINISTIC thresholds

| Obligation | Threshold |
|---|---|
| Audit trail | Non-alterable; computer-generated; retained with record |
| Unique user IDs | No reuse of IDs assigned to individuals who have left |
| FDA certification letter (§11.100(c)) | Submitted to FDA before electronic signatures used |
| Two-component signing | User ID + password (or token); both required at first signing |
| Password lockout | After ≤10 failed attempts (industry standard) |
| Lost/stolen authenticator deactivation | Within 4 hours |
| GAMP 5 Category 5 system | Full lifecycle validation; IQ + OQ + PQ required |

## Parse status: Deep — electronic records and system validation both parsed
