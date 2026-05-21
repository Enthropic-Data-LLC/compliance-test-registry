# EPA EPCRA / SARA Title III — Emergency Planning and Community Right-to-Know Act

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Emergency planning for hazardous chemical releases; community right-to-know reporting; toxic chemical release inventory (TRI); applies to facilities with chemicals above threshold planning quantities (TPQs) or reporting thresholds
**Authority:** U.S. Environmental Protection Agency (EPA); Local Emergency Planning Committees (LEPCs); State Emergency Response Commissions (SERCs)
**Key sections:** §301–303 (emergency planning), §304 (emergency notification), §311–312 (hazardous chemical reporting — Tier I/II), §313 (TRI / Form R)
**Related:** CERCLA §103 (continuous release notification); 40 CFR Part 355 (§301–304); 40 CFR Part 370 (§311–312); 40 CFR Part 372 (§313 TRI)

---

## Summary

| Metric | Count |
|---|---|
| EPCRA sections | 4 major reporting sections (301–304, 311–312, 313) |
| Extremely Hazardous Substances (EHS) list | ~355 chemicals with TPQs |
| TRI-listed chemicals | ~800+ chemicals and chemical categories |
| Sections parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | High — quantity thresholds, filing deadlines, notification timelines |
| Partial automation (PARAMETERIZED) | Low — threshold determination |
| Human-determination required (CONTESTED) | Low |
| Open assumptions | 0 |

---

## Scoping pre-conditions by section

```python
def in_scope_epcra_302(facility) -> bool:
    """§302: True if facility has EHS at or above threshold planning quantity (TPQ)."""
    return any(chem.quantity >= chem.tpq for chem in facility.ehs_chemicals)

def in_scope_epcra_311(facility) -> bool:
    """§311/312: True if facility is required to have SDS under OSHA HazCom (1910.1200)
    AND has a hazardous chemical at or above threshold (10,000 lbs generally;
    500 lbs or TPQ, whichever is lower, for EHS)."""

def in_scope_epcra_313(facility) -> bool:
    """§313 TRI: True if facility (1) has ≥10 FTE, AND (2) is in a covered SIC code,
    AND (3) manufactures, processes, or otherwise uses a listed chemical above threshold."""
```

---

## §302 — Emergency Planning Notification (DETERMINISTIC)

| Requirement | Threshold / Deadline | Confidence |
|---|---|---|
| Notify SERC + LEPC of EHS presence | Within 60 days of triggering threshold OR by May 17, 1988 (whichever later) | DETERMINISTIC |
| Designate facility emergency coordinator | Upon notification | DETERMINISTIC |
| Participate in LEPC emergency planning | Ongoing | PARAMETERIZED |
| Notify LEPC of TPQ changes | Within 60 days of change | DETERMINISTIC |

**Threshold Planning Quantities (TPQs):** Chemical-specific; listed in 40 CFR Part 355 Appendix A and B. Range from 1 lb (most toxic EHS) to 10,000 lbs. All DETERMINISTIC — look up chemical, compare inventory.

---

## §304 — Emergency Release Notification (DETERMINISTIC deadlines)

When a release of a CERCLA hazardous substance or EPCRA EHS exceeds the **reportable quantity (RQ):**

| Notification | Timing | Recipient |
|---|---|---|
| Immediate verbal notification | Immediately after discovery | LEPC + SERC (for EHS releases to environment); NRC (for CERCLA hazardous substances) |
| Written follow-up notification | As soon as practicable | LEPC + SERC |

**Reportable quantities:** Substance-specific (1 to 5,000 lbs); listed in 40 CFR Part 302 Table 302.4. DETERMINISTIC — quantity released ≥ RQ = mandatory notification.

**Exemptions:** Federally permitted releases (per NPDES permit, etc.); normal agricultural operations; releases solely within a structure; continuous releases (follow §103 instead).

---

## §311/312 — Tier I / Tier II Inventory Reporting (DETERMINISTIC deadlines)

### Applicability thresholds

| Chemical type | Reporting threshold |
|---|---|
| Hazardous chemicals (non-EHS) | ≥ 10,000 lbs on-site at any one time |
| Extremely Hazardous Substances (EHS) | ≥ 500 lbs OR TPQ, whichever is lower |

### Tier II report — required elements (DETERMINISTIC checklist)

Tier II (annual; supersedes Tier I) must include for each reportable chemical:
1. Chemical name or common name (or trade name if CBI claimed)
2. CAS number
3. Chemical category (pure/mixture) and EHS designation
4. Max and average daily amounts present on-site
5. Number of days on-site
6. Storage locations and codes (indoor/outdoor; above/below grade; etc.)
7. Confidential Business Information (CBI) claimed?
8. Certifying official signature

### Filing deadline — DETERMINISTIC

| Report | Deadline | Recipient |
|---|---|---|
| Tier II | March 1 annually | SERC + LEPC + local fire department |

---

## §313 — Toxic Release Inventory (TRI) / Form R (DETERMINISTIC)

### Applicability thresholds

| Activity | Annual threshold |
|---|---|
| Manufacturing or processing TRI chemical | 25,000 lbs/year |
| Otherwise using TRI chemical | 10,000 lbs/year |
| PBT (Persistent Bioaccumulative Toxic) chemicals | Lower thresholds: 10–100 lbs depending on chemical |
| Dioxin and dioxin-like compounds | 0.1 gram |

### TRI Form R — required reporting elements

| Element | Confidence |
|---|---|
| Quantity released to each environmental medium (air/water/land/underground injection) | DETERMINISTIC — measured or estimated with documented methodology |
| Quantity transferred off-site | DETERMINISTIC |
| Source reduction activities | PARAMETERIZED |
| Pollution prevention activities | PARAMETERIZED |

### Filing deadline — DETERMINISTIC

| Report | Deadline | Recipient |
|---|---|---|
| TRI Form R (or Form A if eligible) | July 1 annually | EPA (electronically via TRI-MEweb) + State |

**Form A (alternate certification):** Available if total annual release + off-site transfers ≤ 500 lbs AND no manufacture/processing/use exceeds reporting threshold by less than 10x. Binary DETERMINISTIC eligibility check.

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Section |
|---|---|---|
| §302 SERC/LEPC notification | EHS ≥ TPQ | §302 |
| §304 emergency notification | Release ≥ RQ to environment | §304 |
| §304 verbal notification timing | Immediately | §304 |
| §312 Tier II filing | March 1 annually | §312 |
| §312 threshold (non-EHS) | ≥ 10,000 lbs | §312 |
| §313 TRI Form R filing | July 1 annually | §313 |
| §313 manufacture/process threshold | 25,000 lbs/year | §313 |
| §313 use threshold | 10,000 lbs/year | §313 |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Chemical inventory / SDS management | EPCRA §311/312, OSHA 1910.1200 (HazCom), RCRA, REACH | One chemical inventory system feeds all |
| Emergency notification | EPCRA §304, RCRA contingency plan (LQG), EPA RMP §68.195, NRC (CERCLA §103) | Same emergency communication infrastructure |
| Release quantities | EPCRA §313 TRI, CERCLA §103, Clean Air Act §112(r) | TRI quantities can trigger other reporting |
| Emergency response plan | EPCRA §303 (LEPC plan), RCRA contingency plan, RMP emergency response (§68 Subpart E) | Single emergency response plan with regulatory appendices |
| Environmental permits | EPCRA (reporting), NPDES (permitted discharges exempt from §304), CAA Title V | Permitted releases exempt from some §304 notifications |
