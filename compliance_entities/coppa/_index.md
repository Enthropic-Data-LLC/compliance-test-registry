# COPPA — Children's Online Privacy Protection Act

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Collection, use, and disclosure of personal information from children under 13 by operators of commercial websites and online services directed to children, or operators with actual knowledge they are collecting personal information from children under 13
**Authority:** Federal Trade Commission (FTC); Rule: 16 CFR Part 312 (COPPA Rule)
**Enforcing context:** Operators of websites, apps, games, or online services (1) directed to children under 13, OR (2) with actual knowledge of collecting PI from children under 13
**Current rule:** COPPA Rule as amended 2013; FTC proposed significant 2024 amendments (not yet finalized as of 2026)
**Maximum penalty:** Up to $51,744 per violation per day (adjusted for inflation; 2023 rate)

---

## Summary

| Metric | Count |
|---|---|
| Core operator obligations | 6 |
| Privacy notice required elements | 8 |
| Verifiable parental consent methods | 6+ (FTC-approved methods) |
| Sections parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | High — operator obligations, consent elements, notice elements are checklists |
| Partial automation (PARAMETERIZED) | Moderate — "directed to children" determination |
| Human-determination required (CONTESTED) | Moderate — mixed-audience site classification |
| Open assumptions | 0 |

---

## Scoping pre-condition

```python
def is_coppa_operator(service) -> bool:
    """
    True if EITHER:
    1. Service is "directed to children under 13" — determined by:
       - Subject matter, visual content, music, celebrities popular with children,
         animated characters, child-oriented activities, age of users in ads
    2. Operator has "actual knowledge" that users are under 13
    
    Mixed-audience sites: if service targets both children and adults,
    operator may age-screen and apply COPPA only to under-13 segment.
    FTC "directed to children" is CONTESTED — factors-based analysis.
    """
```

---

## 6 core operator obligations (DETERMINISTIC checklist)

| Obligation | Requirement | Confidence |
|---|---|---|
| 1. Privacy notice — online | Clear, understandable privacy notice posted on website/service | DETERMINISTIC |
| 2. Privacy notice — direct | Direct notice to parent before collecting PI from child | DETERMINISTIC |
| 3. Verifiable parental consent | Obtain verifiable parental consent before collecting, using, or disclosing PI | DETERMINISTIC |
| 4. Parental rights | Provide parents with ability to review, delete child's PI, and opt-out of future collection | DETERMINISTIC |
| 5. PI from child kept confidential and secure | Reasonable procedures to protect confidentiality, security, and integrity | DETERMINISTIC existence |
| 6. Retention and deletion | Retain PI only as long as necessary; deletion upon parent request | DETERMINISTIC |

---

## Privacy notice — required elements (DETERMINISTIC checklist)

The online privacy notice must clearly state:
1. Name, address, phone number, and email of all operators collecting PI through the site
2. What personal information is collected from children
3. How the PI is used
4. Whether PI is disclosed to third parties; categories of third parties
5. Parental rights: review, delete, refuse further collection/use
6. Contact information for parents to exercise rights
7. That operator will not require more PI than reasonably necessary
8. That parent can consent to collection and use without consenting to third-party disclosure

---

## Verifiable parental consent — approved methods

FTC recognizes multiple consent methods. Method must be reasonably calculated to ensure the person providing consent is the parent:

| Method | Confidence | Notes |
|---|---|---|
| Signed consent form (mail/fax) | DETERMINISTIC — accepted | Slow; high friction |
| Credit/debit card transaction + notification | DETERMINISTIC — accepted | Must be a real transaction |
| Toll-free phone call (trained personnel) | DETERMINISTIC — accepted | Live conversation with parent |
| Video conference | DETERMINISTIC — accepted | Identity verification |
| Photo ID + verification | DETERMINISTIC — accepted | Manual review |
| "Email plus" (for internal uses only; low-risk disclosure) | DETERMINISTIC — limited use | Only where PI not disclosed to third parties |

---

## Exceptions to verifiable parental consent

| Exception | Description | Confidence |
|---|---|---|
| Online contact information — one-time response | Email collected only to respond to one-time request; not retained | DETERMINISTIC — narrow scope |
| Online contact information — parent notification | Collected to notify parent of child's activity; no retention | DETERMINISTIC |
| Child safety — online contact for child safety organizations | PARAMETERIZED |  |
| Schools (educational context) | School may consent on behalf of parents for educational purposes | PARAMETERIZED |

---

## COPPA Safe Harbor programs

FTC has approved industry self-regulatory programs (safe harbors) operated by trade associations. Membership confers presumption of compliance:

| Program | Confidence |
|---|---|
| Membership in FTC-approved safe harbor program | DETERMINISTIC — membership current and valid |
| Annual review by safe harbor program | DETERMINISTIC — passed review |

---

## Key DETERMINISTIC thresholds

| Obligation | Requirement | Rule reference |
|---|---|---|
| Verifiable parental consent | Required before any PI collection from under-13 | §312.5 |
| Privacy notice required elements | 8 elements must be present | §312.4(c) |
| Parental right to review | Must be provided | §312.6 |
| Parental right to delete | Must be provided | §312.6 |
| Retention limitation | Retain only as long as necessary for purpose | §312.10 |
| Data security | Reasonable procedures required (written) | §312.8 |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Children's privacy | COPPA (US under-13), UK GDPR Age Appropriate Design Code (under-18), EU GDPR Art. 8 (under-16 or member state age), LGPD Art. 14 | Different age thresholds; US most restrictive at 13 |
| Privacy notice | COPPA §312.4, EU GDPR Art. 13, CCPA §1798.100 | COPPA-specific elements differ from adult privacy notices |
| Parental consent | COPPA, FERPA (school records), HIPAA (minor patients) | Different contexts; same parent consent concept |
| Data security | COPPA §312.8, COPPA FTC Act §5 (unfair practices), GLBA Safeguards | "Reasonable security" standard across FTC-enforced frameworks |
| Third-party data sharing | COPPA §312.5(b), CCPA (sale of minors' PI), EU GDPR | COPPA requires parental consent for third-party disclosure |
