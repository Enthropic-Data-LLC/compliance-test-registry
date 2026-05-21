# Basel III / BCBS 239 — Banking Capital Adequacy and Risk Data Aggregation

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Capital adequacy (Basel III), liquidity coverage, leverage ratios, and risk data aggregation/reporting (BCBS 239) for internationally active banks; implemented through national regulatory frameworks (US: Fed/OCC/FDIC rules; EU: CRR/CRD)
**Authority:** Basel Committee on Banking Supervision (BCBS); enforced by national prudential regulators
**Enforcing context:** Globally systemically important banks (G-SIBs) — BCBS 239 mandatory. Other internationally active banks — capital/liquidity requirements phased by national regulator. Non-bank entities — not directly in scope.
**Current edition:** Basel III finalization (Basel IV) — full implementation 1 January 2025 (US/EU phased)

---

## Summary

| Metric | Count |
|---|---|
| Basel III pillars | 3 (Minimum Capital / Supervisory Review / Market Discipline) |
| BCBS 239 principles | 14 |
| BCBS 239 target population | G-SIBs (mandatory); D-SIBs (comply or explain) |
| Sections parsed (individual files) | 1 (capital-adequacy-risk-data-aggregation.md — CET1/Tier1/Total capital ratios, LCR/NSFR, leverage ratio, Pillar 3 disclosure deadlines, BCBS 239 P5/P10, ICAAP) |
| Fully automated (DETERMINISTIC) | Low-Moderate — ratio thresholds; disclosure deadlines |
| Partial automation (PARAMETERIZED) | Dominant — ICAAP, model validation, stress testing |
| Human-determination required (CONTESTED) | High — internal model approval; materiality determination |
| Open assumptions | 2 |

---

## Scoping pre-conditions

```python
def is_gsib() -> bool:
    """True if institution is on FSB G-SIB list (annual November publication)."""

def is_internationally_active_bank() -> bool:
    """True if institution meets national regulator definition of internationally active."""

def in_scope_for_bcbs239() -> bool:
    """BCBS 239 mandatory for G-SIBs; D-SIBs by national regulator direction."""
    return is_gsib()  # Plus national regulator extension for D-SIBs
```

---

## Basel III — capital adequacy thresholds (DETERMINISTIC)

| Ratio | Minimum | With Conservation Buffer | Notes |
|---|---|---|---|
| Common Equity Tier 1 (CET1) | 4.5% | 7.0% | Breach triggers capital conservation restrictions |
| Tier 1 Capital | 6.0% | 8.5% | — |
| Total Capital | 8.0% | 10.5% | — |
| Countercyclical Buffer | 0–2.5% | Institution-specific | National regulator-set |
| G-SIB Surcharge | 1.0–3.5% | Institution-specific | Based on systemic importance score |
| Leverage Ratio | 3.0% | — | Tier 1 / Total Exposure |
| Liquidity Coverage Ratio (LCR) | 100% | — | HQLA / Net cash outflows (30-day stress) |
| Net Stable Funding Ratio (NSFR) | 100% | — | Available stable funding / Required stable funding |

All ratio minimums are DETERMINISTIC — breach generates automatic supervisory notification.

---

## BCBS 239 — 14 principles confidence map

### Overarching governance

| Principle | Requirement | Confidence | Notes |
|---|---|---|---|
| P1 | Board/senior management oversight of risk data aggregation | PARAMETERIZED | Board-approved framework; evidence of oversight |
| P2 | Data architecture and IT infrastructure | PARAMETERIZED | Integrated data taxonomy; single authoritative data sources |

### Risk data aggregation capabilities

| Principle | Requirement | Confidence | Notes |
|---|---|---|---|
| P3 | Accuracy and integrity | PARAMETERIZED | Automated reconciliation; exception reporting |
| P4 | Completeness | PARAMETERIZED | All material risk positions captured |
| P5 | Timeliness | DETERMINISTIC | Normal mode: end-of-day; stress mode: intraday as required by supervisor |
| P6 | Adaptability | PARAMETERIZED | Ad hoc risk reporting capability within supervisory timelines |

### Risk reporting practices

| Principle | Requirement | Confidence | Notes |
|---|---|---|---|
| P7 | Accuracy | PARAMETERIZED | Reports reconcile to risk aggregation outputs |
| P8 | Comprehensiveness | PARAMETERIZED | All material risks; group-wide and entity view |
| P9 | Clarity and usefulness | CONTESTED | Subjective qualitative assessment by supervisors |
| P10 | Frequency | DETERMINISTIC | Board: quarterly minimum; senior management: more frequent |
| P11 | Distribution | PARAMETERIZED | Appropriate distribution to decision-makers |

### Supervisory review / cross-border

| Principle | Requirement | Confidence | Notes |
|---|---|---|---|
| P12 | Review and evaluation | PARAMETERIZED | Annual self-assessment vs. principles |
| P13 | Remedial actions | PARAMETERIZED | Supervisory-directed remediation plans |
| P14 | Home/host cooperation | PARAMETERIZED | Cross-border data sharing arrangements |

---

## Pillar 3 disclosure — DETERMINISTIC publication deadlines

| Disclosure | Frequency | Deadline | Section |
|---|---|---|---|
| Capital adequacy | Quarterly | Within 45 days of quarter-end | Pillar 3 |
| Risk-weighted assets | Quarterly | Within 45 days | Pillar 3 |
| Leverage ratio | Quarterly | Within 45 days | Pillar 3 |
| LCR | Monthly | Within 15 business days of month-end | LCR Disclosure Standards |
| TLAC (G-SIBs) | Quarterly | Within 45 days | FSB TLAC Standard |
| Annual full disclosure | Annual | With annual financial statements | Pillar 3 |

---

## ICAAP and ILAAP — PARAMETERIZED (supervisory submission)

Internal Capital Adequacy Assessment Process (ICAAP) and Internal Liquidity Adequacy Assessment Process (ILAAP) are the primary PARAMETERIZED artifacts:
- Frequency: Annual submission to home supervisor
- Content: Stress scenarios, capital projections, governance attestation
- Threshold for adequacy: Supervisor-determined (CONTESTED)

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Capital ratio calculation | Basel III, DORA (operational resilience capital), SOX (financial reporting) | Same calculation methodology |
| Data lineage and governance | BCBS 239, GDPR Art. 5 (data accuracy), SEC Reg SCI | Data architecture artifacts reused |
| Stress testing | Basel III (ICAAP), Fed DFAST/CCAR, EBA stress tests | Scenario library can be shared |
| Operational risk | Basel III OpRisk capital, SOX ITGC, DORA Art. 28 | Operational loss events feed capital calculation |
| Disclosure | Pillar 3, SEC 10-K/10-Q, IFRS 7/IFRS 9 | Same financial statements infrastructure |
