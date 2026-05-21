# LGPD — Lei Geral de Proteção de Dados (Brazil)

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Processing of personal data of individuals located in Brazil, regardless of where the processing organization is located; applies when the processing occurs in Brazil, when the processing purpose is to offer goods/services to individuals in Brazil, or when the personal data was collected in Brazil
**Authority:** Autoridade Nacional de Proteção de Dados (ANPD) — National Data Protection Authority
**Current legislation:** Law No. 13,709/2018 (LGPD) as amended; partially effective September 2020; penalty provisions effective August 2021
**Maximum fine:** BRL 50 million (≈ USD 10M) per violation or 2% of Brazil revenue, capped at BRL 50M per violation

---

## Summary

| Metric | Count |
|---|---|
| Legal bases for processing | 10 |
| Data subject rights | 9 |
| Special categories (sensitive data) | 8 types |
| Sections parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | Moderate — legal basis documentation; consent requirements; DPO designation |
| Partial automation (PARAMETERIZED) | Dominant — data mapping; proportionality; security measures |
| Human-determination required (CONTESTED) | Moderate — legitimate interest balancing test |
| Open assumptions | 0 |

---

## Scoping pre-condition

```python
def in_lgpd_scope(processing_activity) -> bool:
    """
    True if ANY of:
    1. Processing occurs in Brazil (even by foreign entity)
    2. Purpose is offering goods/services to Brazil data subjects
    3. Personal data was collected in Brazil
    Exemptions: purely personal/non-economic; journalistic/artistic/academic (with conditions);
    public security/national defense; criminal investigation.
    """
```

---

## 10 legal bases for processing — confidence map

| Legal basis | Art. | Confidence | Notes |
|---|---|---|---|
| Consent | 7(I) | DETERMINISTIC — consent must be explicit, informed, purpose-specific | Withdrawal right must exist |
| Contract performance | 7(V) | PARAMETERIZED | Necessary for contract with data subject |
| Legal obligation | 7(II) | PARAMETERIZED | Compliance with legal or regulatory obligation |
| Public policy / government body | 7(III) | PARAMETERIZED | Government entities only |
| Research (public interest) | 7(IV) | PARAMETERIZED | Anonymization where possible |
| Vital interests | 7(VIII) | PARAMETERIZED | Protection of life/physical safety |
| Legitimate interest | 7(IX) | CONTESTED | Balancing test — controller's interest vs. data subject's rights |
| Credit protection | 7(X) | PARAMETERIZED | Financial sector specific |
| Regular exercise of rights | 7(VI) | PARAMETERIZED | Judicial/administrative/arbitration proceedings |
| Health/sanitation (healthcare only) | 7(VII) → Art. 11 | PARAMETERIZED | Healthcare providers; combined with sensitive data provisions |

---

## Sensitive data — Art. 11 (stricter requirements)

| Sensitive data category | Confidence |
|---|---|
| Racial or ethnic origin | DETERMINISTIC — explicit consent or specific legal bases only |
| Religious belief | DETERMINISTIC |
| Political opinion | DETERMINISTIC |
| Union membership | DETERMINISTIC |
| Health or sex life | DETERMINISTIC |
| Genetic or biometric data | DETERMINISTIC |
| Children's data | DETERMINISTIC — parental/guardian consent required |

---

## Data subject rights — DETERMINISTIC obligations

| Right | Response obligation | Confidence |
|---|---|---|
| Confirmation of existence of processing | Immediately or at next interaction | DETERMINISTIC |
| Access to data | Within 15 days of request | DETERMINISTIC |
| Correction of inaccurate data | PARAMETERIZED | Without undue delay |
| Anonymization, blocking, or deletion | PARAMETERIZED — depends on legal basis | |
| Portability | PARAMETERIZED | Via ANPD regulation |
| Deletion of data processed with consent | Upon withdrawal of consent | DETERMINISTIC |
| Information about sharing with third parties | On request | DETERMINISTIC |
| Refusal of automated processing (profiling) | On request | DETERMINISTIC |
| Revocation of consent | At any time | DETERMINISTIC |

**Key DETERMINISTIC deadline:** Access request = within **15 days** (stricter than GDPR 30-day rule).

---

## Data Officer (DPO equivalent) — Art. 41

| Requirement | Confidence | Notes |
|---|---|---|
| DPO appointment | DETERMINISTIC — controllers must designate a DPO | Processors: ANPD may require |
| DPO identity publicly available | DETERMINISTIC | Name and contact published |
| DPO activities | PARAMETERIZED | Receives complaints, provides guidance, cooperates with ANPD |

---

## Breach notification — Art. 48

| Requirement | Timing | Confidence |
|---|---|---|
| Notify ANPD | "Reasonable time" — ANPD regulation specifies 3 business days | DETERMINISTIC (per ANPD resolution) |
| Notify affected data subjects | When incident may cause relevant harm | PARAMETERIZED (harm threshold) |

---

## International data transfers — Art. 33

| Transfer mechanism | Confidence | Notes |
|---|---|---|
| Transfer to country with adequate level of protection (ANPD-recognized) | DETERMINISTIC | ANPD-issued adequacy list |
| Standard contractual clauses (model clauses issued by ANPD) | DETERMINISTIC — ANPD template | |
| Binding corporate rules | PARAMETERIZED — ANPD approval required | |
| Specific consent for transfer | DETERMINISTIC — explicit, informed | |
| Contract necessity | PARAMETERIZED | Transfer necessary for contract performance |

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Article |
|---|---|---|
| Access request response | 15 days | Art. 19 |
| Breach notification to ANPD | 3 business days (per ANPD resolution) | Art. 48 |
| DPO designation | Mandatory for all controllers | Art. 41 |
| Consent withdrawal right | Must be as easy as consent was given | Art. 8 |
| Children's data — parental consent | Required | Art. 14 |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Data subject rights | LGPD, EU GDPR, CCPA, PIPEDA | LGPD 15-day access deadline < GDPR 30-day |
| Legal basis documentation | LGPD, EU GDPR Art. 6 | Similar structure; 10 LGPD bases vs. 6 GDPR bases |
| Sensitive data handling | LGPD Art. 11, EU GDPR Art. 9 | Similar categories; LGPD includes children's data in sensitive |
| DPO appointment | LGPD Art. 41, EU GDPR Art. 37 | Both mandatory for applicable orgs |
| International transfers | LGPD Art. 33, EU GDPR Art. 44 | Different adequacy lists; similar mechanisms |
