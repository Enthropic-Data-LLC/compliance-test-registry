# ISO 45001:2018 — Occupational Health and Safety Management System

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** All clauses 4–10; OH&S management system for prevention of work-related injury, ill health, and promotion of worker well-being
**Authority:** International Organization for Standardization (ISO)
**Enforcing context:** Third-party certification (accredited CB); contractual requirements; replaces OHSAS 18001:2007; complements OSHA 1910/1926 regulatory compliance (provides the management system; OSHA provides the specific technical requirements)
**Current edition:** ISO 45001:2018 (Annex SL — harmonized with ISO 9001, ISO 14001, ISO 27001)

---

## Summary

| Metric | Count |
|---|---|
| Clauses | 7 (Clauses 4–10) |
| Sub-clauses with discrete requirements | ~50 |
| Sub-clauses parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | Low — OH&S management system standard; process-level obligations |
| Partial automation (PARAMETERIZED) | Dominant |
| Human-determination required (CONTESTED) | Moderate — hazard identification methodology, risk acceptability |
| Open assumptions | 0 |

---

## Relationship to OSHA

ISO 45001 is the **management system** layer; OSHA 1910/1926 provides **specific technical requirements** (permissible exposure limits, lockout/tagout procedures, PPE specs, etc.). They are complementary:

| Layer | Standard | Nature |
|---|---|---|
| Management system | ISO 45001 | How you manage OH&S — process, governance, continual improvement |
| Technical requirements | OSHA 1910/1926 | What specific controls are required — bright-line thresholds |
| Evidence | Integrated | ISO 45001 audit verifies the management system; OSHA inspection verifies specific controls |

ISO 45001 §6.1.3 (legal/other requirements) requires identification of applicable OSHA regulations. OSHA compliance is treated as a compliance obligation within the ISO 45001 framework.

---

## Per-clause confidence map

### Clause 4 — Context

| Sub-clause | Requirement | Confidence | Notes |
|---|---|---|---|
| 4.1 | Internal/external issues | PARAMETERIZED | — |
| 4.2 | Needs of workers and other interested parties | PARAMETERIZED | Worker consultation emphasized throughout |
| 4.3 | OH&S MS scope | PARAMETERIZED | Must be documented |
| 4.4 | OH&S MS processes | PARAMETERIZED | — |

### Clause 5 — Leadership and Worker Participation

| Sub-clause | Requirement | Confidence | Notes |
|---|---|---|---|
| 5.1 | Leadership and commitment | PARAMETERIZED | Top management demonstrably accountable for OH&S |
| 5.2 | OH&S policy | DETERMINISTIC | Written policy; commitment to provide safe/healthy working conditions; eliminate hazards; comply with legal requirements; consult workers |
| 5.3 | Organizational roles | PARAMETERIZED | OH&S responsibilities assigned and communicated |
| 5.4 | Consultation and participation of workers | PARAMETERIZED | Workers involved in hazard identification, risk assessment, incident investigation, improvement |

### Clause 6 — Planning

| Sub-clause | Requirement | Confidence | Notes |
|---|---|---|---|
| 6.1.1 | General — risks and opportunities | PARAMETERIZED | OH&S risks and opportunities identified |
| 6.1.2 | Hazard identification and risk assessment | PARAMETERIZED | Proactive and reactive hazard identification; risk assessment methodology org-defined |
| 6.1.3 | Determination of legal/other requirements | DETERMINISTIC | Register of applicable legal requirements maintained; OSHA regulations included |
| 6.1.4 | Planning to address risks/opportunities | PARAMETERIZED | Actions planned and integrated |
| 6.2 | OH&S objectives | DETERMINISTIC | Documented; measurable; monitored; communicated; updated |

### Clause 7 — Support

| Sub-clause | Requirement | Confidence | Notes |
|---|---|---|---|
| 7.1 | Resources | PARAMETERIZED | — |
| 7.2 | Competence | DETERMINISTIC | Competence evidence; training records; records retained |
| 7.3 | Awareness | PARAMETERIZED | Awareness of OH&S policy; contribution to OH&S; consequences of noncompliance |
| 7.4 | Communication | PARAMETERIZED | Internal/external communication; workers consulted on changes |
| 7.5 | Documented information | DETERMINISTIC | Required documented information controlled |

### Clause 8 — Operation

| Sub-clause | Requirement | Confidence | Notes |
|---|---|---|---|
| 8.1.1 | General operational planning and control | PARAMETERIZED | Controls for hazards in hierarchy: eliminate > substitute > engineering > administrative > PPE |
| 8.1.2 | Eliminating hazards and reducing OH&S risks | PARAMETERIZED | Hierarchy of controls applied |
| 8.1.3 | Management of change | DETERMINISTIC | Changes to operations evaluated for OH&S impact before implementation; temporary changes also controlled |
| 8.1.4 | Procurement | PARAMETERIZED | Contractors and outsourced processes controlled; OH&S requirements flow-down |
| 8.2 | Emergency preparedness and response | PARAMETERIZED | Plans for potential emergency situations; tested; workers trained |

### Clause 9 — Performance Evaluation

| Sub-clause | Requirement | Confidence | Notes |
|---|---|---|---|
| 9.1.1 | Monitoring, measurement, analysis, evaluation | PARAMETERIZED | OH&S performance metrics; leading and lagging indicators |
| 9.1.2 | Evaluation of compliance | DETERMINISTIC | Compliance evaluation at planned intervals; records retained |
| 9.2 | Internal audit | DETERMINISTIC | Planned program; independence; records |
| 9.3 | Management review | DETERMINISTIC | Planned intervals; inputs/outputs; records |

### Clause 10 — Improvement

| Sub-clause | Requirement | Confidence | Notes |
|---|---|---|---|
| 10.1 | General | PARAMETERIZED | — |
| 10.2 | Incident, nonconformity, and corrective action | DETERMINISTIC | Incidents investigated; root cause determined; corrective action implemented; effectiveness reviewed; records retained; reported to workers |
| 10.3 | Continual improvement | PARAMETERIZED | — |

---

## Incident investigation — key DETERMINISTIC record

All incidents (including near-misses) must be investigated. Records include:
- Description of incident
- Root cause(s) identified
- Corrective actions taken
- Effectiveness verification
- Communication to workers

OSHA 300/300A/301 logs are a DETERMINISTIC companion record (where OSHA recordkeeping applies).

---

## Cross-standard dependencies

| Shared artifact | Frameworks |
|---|---|
| Management system (Annex SL) | ISO 9001, ISO 14001, ISO 27001 — IMS integration |
| Legal requirements register | ISO 45001 §6.1.3, ISO 14001 §6.1.2, OSHA 1910/1926 | OSHA regulations are the primary compliance obligations in the register |
| Competence records | ISO 45001 §7.2, ISO 9001 §7.2, OSHA training records | Same training management system |
| Incident records | ISO 45001 §10.2, OSHA 300 log, RIDDOR (UK) | ISO 45001 investigation records; OSHA 300 log is the statutory companion |
| Emergency preparedness | ISO 45001 §8.2, ISO 14001 §8.2, OSHA 1910.38 (EAP) | Single emergency plan satisfies all three |
| Internal audit | ISO 45001 §9.2, ISO 9001 §9.2, ISO 14001 §9.2 | Combined IMS audit covers all three |
