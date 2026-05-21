# PSD2 — EU Payment Services Directive 2 / Strong Customer Authentication

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Payment service providers (PSPs) operating in the EU/EEA; includes banks, e-money institutions, payment institutions, account information service providers (AISPs), and payment initiation service providers (PISPs)
**Authority:** European Banking Authority (EBA); implemented by national competent authorities; primary regulation: Directive (EU) 2015/2366 + RTS on SCA and CSC (Commission Delegated Regulation (EU) 2018/389)
**Enforcing context:** All PSPs processing electronic payments in EU/EEA; SCA requirements apply to payer-facing interactions; open banking API requirements apply to ASPSPs (account-holding PSPs)
**Current edition:** PSD2 (2015/2366); PSD3 and PSR proposed (2023 package — pending adoption as of 2026)

---

## Summary

| Metric | Count |
|---|---|
| Core titles in PSD2 | 4 |
| RTS on SCA — key Articles | ~49 |
| SCA exemptions | 10 categories |
| Sections parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | High — SCA element requirements; authentication code binding; transaction monitoring thresholds |
| Partial automation (PARAMETERIZED) | Moderate — exemption application logic |
| Human-determination required (CONTESTED) | Low — authentication approach design |
| Open assumptions | 0 |

---

## Scoping pre-condition

```python
def is_psd2_psp() -> bool:
    """
    True if entity is a licensed payment service provider operating in EU/EEA.
    PSP types: credit institution, e-money institution, payment institution,
    AISP (Art. 67), PISP (Art. 66), ASPSP (Art. 68).
    """

def transaction_requires_sca(transaction) -> bool:
    """
    True if electronic payment transaction triggered by payer — SCA required
    unless an explicit exemption applies (Art. 10-18 RTS).
    """
```

---

## Strong Customer Authentication (SCA) — DETERMINISTIC requirements

SCA requires **at least 2 independent factors** from:

| Factor Category | Examples | Confidence |
|---|---|---|
| Knowledge (something only the user knows) | PIN, password, passphrase | DETERMINISTIC |
| Possession (something only the user has) | Mobile device, hardware token, smart card | DETERMINISTIC |
| Inherence (something the user is) | Fingerprint, face, voice, retina | DETERMINISTIC |

**Independence requirement:** The factors must be independent — compromise of one must not compromise the other (Art. 9 RTS). This is DETERMINISTIC in principle; implementation assessment is PARAMETERIZED.

### Authentication code binding (Art. 5 RTS) — DETERMINISTIC

For payment transactions, the authentication code must be dynamically linked to:
- The specific amount of the transaction
- The specific payee/recipient

Alteration of amount or payee must invalidate the authentication code. This is a DETERMINISTIC binary check.

---

## SCA exemptions — PARAMETERIZED eligibility, DETERMINISTIC thresholds

| Exemption | Condition | Threshold | Confidence |
|---|---|---|---|
| Low-value contactless (POS) | < €50 per transaction | ≤ €150 cumulative or ≤ 5 consecutive | DETERMINISTIC thresholds |
| Low-value remote electronic | < €30 per transaction | ≤ €100 cumulative or ≤ 5 consecutive | DETERMINISTIC thresholds |
| Unattended transport/parking | Low-risk context | Amount-independent | PARAMETERIZED |
| Trusted beneficiaries | Payer-whitelisted payee | No amount limit | PARAMETERIZED setup |
| Recurring transactions | Same amount, same payee | First transaction requires SCA | DETERMINISTIC first-time rule |
| Corporate payments | Dedicated payment processes + controls | Risk-based | PARAMETERIZED |
| Transaction Risk Analysis (TRA) | Fraud rate below reference threshold | €100/€250/€500 tiers | DETERMINISTIC fraud rate gates |
| Secure corporate payment processes | Assessed as low-risk by PSP | Supervised | PARAMETERIZED |

### TRA fraud rate thresholds (Art. 18 RTS) — DETERMINISTIC

| Exemption up to | Maximum PSP fraud rate |
|---|---|
| €100 | 0.13% |
| €250 | 0.06% |
| €500 | 0.01% |

PSP fraud rate exceeding the applicable threshold = TRA exemption unavailable for that tier. Binary DETERMINISTIC gate.

---

## Open banking (ASPSP obligations)

| Requirement | Confidence | Notes |
|---|---|---|
| Dedicated API interface | DETERMINISTIC | ASPSPs must provide dedicated access interface (or fallback) |
| Availability SLA: 99.5% uptime | DETERMINISTIC | API availability measured monthly |
| API testing facility | DETERMINISTIC | Testing environment made available before go-live |
| No obstacles for TPPs | DETERMINISTIC | Cannot impose additional requirements on AISPs/PISPs beyond SCA |
| Consent duration | PARAMETERIZED | AISP access valid for the duration authorized by PSU |
| Strong authentication for TPP access | DETERMINISTIC | SCA required when PSU first authorizes TPP |

---

## Incident reporting — DETERMINISTIC deadlines

| Notification | Deadline | Recipient |
|---|---|---|
| Initial notification of major incident | Without undue delay after classification | National competent authority |
| Intermediate report | Within 72 hours of initial notification | NCA |
| Final report | Within 1 month of incident resolution | NCA |

**Major incident classification:** Based on number of payment service users affected, transaction value, operational impact, geographic spread, and duration.

---

## Key DETERMINISTIC thresholds summary

| Obligation | Value | Article |
|---|---|---|
| SCA required factors | 2 minimum from distinct categories | Art. 4 RTS |
| Low-value contactless (per transaction) | < €50 | Art. 10 RTS |
| Low-value contactless (cumulative cap) | €150 | Art. 10 RTS |
| Low-value remote (per transaction) | < €30 | Art. 16 RTS |
| Low-value remote (cumulative cap) | €100 | Art. 16 RTS |
| TRA exemption (€500 tier) fraud rate cap | ≤ 0.01% | Art. 18 RTS |
| API uptime SLA | 99.5% monthly | Art. 32 RTS |
| Intermediate incident report | 72 hours | Art. 96 PSD2 |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Authentication infrastructure | PSD2 SCA, NIST 800-63-3 (AAL2/AAL3), FIDO2 | Same authenticator hardware; different assurance level mapping |
| Fraud monitoring | PSD2 TRA (Art. 18), Reg SCI, FFIEC | Same fraud detection system; PSD2 adds mandatory rate thresholds |
| Incident reporting | PSD2 Art. 96, DORA Art. 19 (alignment in progress), GDPR Art. 33 | DORA replaces PSD2 incident reporting for DORA-scope entities by 2025 |
| Open banking API | PSD2 Art. 68, UK Open Banking Standard, FDX (US) | Different API specs; same account access consent model |
| Data minimization | PSD2 Art. 67 (AISP data restriction), GDPR Art. 5 | AISP access limited to account data explicitly requested |
