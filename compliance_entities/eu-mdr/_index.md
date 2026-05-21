# EU MDR / IVDR — EU Medical Device Regulation and In Vitro Diagnostic Regulation

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** EU MDR (2017/745) and EU IVDR (2017/746) — requirements for medical devices and IVDs placed on the EU/EEA market
**Authority:** European Commission; national competent authorities (Notified Bodies for conformity assessment)
**Enforcing context:** Manufacturers placing medical devices or IVDs on the EU/EEA market; authorized representatives; importers; distributors
**In force:** EU MDR: fully applicable since May 26 2021 (transitional periods extended through 2027/2028 for legacy devices); EU IVDR: applicable since May 26 2022 (transitional periods through 2027/2028 for most IVD classes)

---

## Summary

| Metric | Count |
|---|---|
| Regulations | 2 (MDR + IVDR) |
| MDR articles | 123 + 17 Annexes |
| IVDR articles | 113 + 14 Annexes |
| Technically testable article clusters | ~30 |
| Articles parsed (individual files) | 2 (gspr-technical-documentation.md + pms-vigilance-conformity.md — GSPR, tech doc, DoC, UDI, PMS/PSUR, vigilance deadlines, conformity assessment) |
| Fully automated (DETERMINISTIC) | Low-moderate — classification rules, labeling elements, UDI database registration |
| Partial automation (PARAMETERIZED) | Dominant — "appropriate," "sufficient," "state of the art" throughout |
| Human-determination required (CONTESTED) | Significant — clinical evaluation adequacy, risk/benefit determination |
| Open assumptions | 2 |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Device classification — pre-condition to all MDR tests

MDR classification determines the conformity assessment pathway and the level of Notified Body involvement:

| Class | Risk level | Notified Body required? | Examples |
|---|---|---|---|
| Class I | Low risk | No (unless sterile, measuring, or reusable surgical instrument) | Bandages, wheelchairs, stethoscopes |
| Class I (sterile/measuring/reusable surgical) | Low-moderate | Yes (limited scope) | Sterile syringes, measuring catheters |
| Class IIa | Medium risk | Yes | Hearing aids, contact lenses, ultrasound equipment |
| Class IIb | Medium-high risk | Yes | Ventilators, bone fixation plates, defibrillators |
| Class III | High risk | Yes (full QMS + technical documentation review) | Implantable devices, cardiac stents, cochlear implants |

Classification is determined by applying the 22 classification rules in MDR Annex VIII. Classification is DETERMINISTIC given the correct rule, but rule selection is PARAMETERIZED.

IVDR uses a different 4-class system (A/B/C/D) defined in IVDR Annex VIII.

---

## Per-article confidence map (MDR — key articles)

### Chapter II — Making Available on the Market and Putting into Service (Articles 5–19)

| Article | Requirement | Confidence | Notes |
|---|---|---|---|
| Art. 5 | Placing on market and putting into service | PARAMETERIZED | Device meets all applicable requirements; CE marking required |
| Art. 9 | EU declaration of conformity | DETERMINISTIC | Written DoC required; 10 mandatory elements (Art. 19 list) |
| Art. 10 | General obligations of manufacturers | PARAMETERIZED | 19 sub-obligations; QMS implementation; post-market surveillance; CAPA; clinical evaluation |
| Art. 11 | Authorized representative | DETERMINISTIC | Non-EU manufacturers must designate an EU authorized representative |
| Art. 13 | General obligations of importers | PARAMETERIZED | Import compliance checks |
| Art. 14 | General obligations of distributors | PARAMETERIZED | Distribution compliance checks |

### Chapter III — Identification and Traceability (Articles 24–26)

| Article | Requirement | Confidence | Notes |
|---|---|---|---|
| Art. 24 | Registration of economic operators | DETERMINISTIC | Manufacturers, authorized representatives, and importers must register in EUDAMED before placing device on market |
| Art. 25 | Summary of safety and clinical performance (SSCP) | DETERMINISTIC | Required for Class III and implantable devices; published in EUDAMED |
| Art. 26 | UDI system | DETERMINISTIC | Unique Device Identification system; UDI-DI assigned; UDI-PI on labels; registered in EUDAMED |

### Chapter IV — Notified Bodies (Articles 33–50)

| Article | Requirement | Confidence | Notes |
|---|---|---|---|
| Art. 52 | Conformity assessment procedures | DETERMINISTIC | Class determines applicable Annex IX/X/XI/XIII procedure; Notified Body involvement is DETERMINISTIC by class |

### Chapter V — Classification and Conformity Assessment (Articles 51–60)

| Article | Requirement | Confidence | Notes |
|---|---|---|---|
| Art. 51 | Classification of devices | PARAMETERIZED | Annex VIII rules applied; classification justified in technical documentation |
| Art. 52 | Conformity assessment procedures | DETERMINISTIC | Class III: Annex IX QMS + technical documentation OR Annex X type examination + Annex XI; Class IIb: Annex IX QMS + technical documentation OR Annex X + Annex XI; Class IIa: Annex IX QMS + technical documentation OR various routes; Class I: Annex IV self-declaration |

### Chapter VII — Post-Market Surveillance, Vigilance and Market Surveillance (Articles 83–100)

| Article | Requirement | Confidence | Notes |
|---|---|---|---|
| Art. 83 | Post-market surveillance system | DETERMINISTIC | Written PMS plan required for all devices; continuous PMS process |
| Art. 84 | PMS plan | DETERMINISTIC | PMS plan includes: proactive data collection, complaint analysis, vigilance reporting, trend analysis, FSCA assessment |
| Art. 85 | Post-market surveillance report (Class I) | DETERMINISTIC | PMS report updated when necessary; available to competent authority upon request |
| Art. 86 | Periodic safety update report — PSUR (Class IIa, IIb, III) | DETERMINISTIC | PSUR frequency: Class IIa and IIb: at least every 2 years; Class III: annually |
| Art. 87 | Reporting of serious incidents and FSCAs | DETERMINISTIC | **Serious incident:** 15 calendar days; **Immediate threat to health:** immediately (max 2 days); **Field safety corrective action (FSCA):** immediately |
| Art. 88 | Trend reporting | PARAMETERIZED | Statistical increase in non-serious incidents or expected side effects must be reported |
| Art. 89 | Analysis of serious incidents and FSCAs | PARAMETERIZED | Root cause analysis; FSCA implementation |

### Annex I — General Safety and Performance Requirements (GSPR)

Annex I is the core technical requirement. All devices must meet all applicable GSPRs. The GSPR is the EU MDR counterpart to the FDA's Essential Requirements.

| Chapter | Focus | Confidence | Notes |
|---|---|---|---|
| Ch. I (§§1–9) | General requirements | PARAMETERIZED | Risk management per ISO 14971; state of the art; known/foreseeable risks reduced |
| Ch. II (§§10–22) | Requirements regarding design and manufacture | PARAMETERIZED/DETERMINISTIC | Chemical/physical/biological properties; sterility; measuring; radiation; software (IEC 62304) |
| Ch. III (§§23–24) | Information supplied with device | DETERMINISTIC | Label content requirements (25 mandatory elements per Annex I §23.4) |

### Annex II — Technical Documentation

The Technical Documentation (TD) is the primary compliance artifact. It must include:

| Section | Contents | Confidence |
|---|---|---|
| 1 | Device description and specification (including variants and accessories) | DETERMINISTIC — presence of each element is binary |
| 2 | Information to be supplied by manufacturer | DETERMINISTIC |
| 3 | Design and manufacturing information | DETERMINISTIC |
| 4 | General safety and performance requirements (with GSPR cross-reference) | DETERMINISTIC |
| 5 | Benefit-risk analysis and risk management | PARAMETERIZED |
| 6 | Product verification and validation | DETERMINISTIC |
| **6.1** | Pre-clinical and clinical data | DETERMINISTIC |
| **6.2** | Clinical evaluation (per Annex XIV) | CONTESTED — clinical evidence sufficiency |

### Annex XIV — Clinical Evaluation (Part A and Part B)

| Part | Requirement | Confidence | Notes |
|---|---|---|---|
| Part A | Clinical evaluation plan and report | PARAMETERIZED | CER must follow MEDDEV 2.7/1 rev 4 guidance; clinical evidence sources must be identified and appraised |
| Part B | Post-market clinical follow-up (PMCF) plan | PARAMETERIZED | PMCF plan required; data collection methods defined |

---

## MDR vigilance reporting timelines — DETERMINISTIC

| Event type | Reporting deadline | Recipient |
|---|---|---|
| Serious incident (potentially caused by device) | 15 calendar days from becoming aware | National competent authority |
| Serious incident — immediate threat to public health | 2 calendar days | National competent authority |
| Serious incident — death or unanticipated serious deterioration | 10 calendar days | National competent authority |
| Field Safety Corrective Action (FSCA) | Before action taken (or simultaneously in urgent cases) | National competent authority |
| FSCA communication (Field Safety Notice — FSN) | With competent authority approval or as agreed | Users/customers |

---

## EUDAMED registration — DETERMINISTIC gates

| Obligation | When | Confidence |
|---|---|---|
| Manufacturer/AR/importer registration | Before placing device on market | DETERMINISTIC |
| Device registration (UDI-DI) | Before placing device on market | DETERMINISTIC |
| Certificate upload | When Notified Body certificate issued | DETERMINISTIC |
| SSCP publication | Before placing Class III / implantable devices on market | DETERMINISTIC |
| Serious incident/FSCA reports | Per reporting timelines above | DETERMINISTIC |

---

## Open assumption registry

*(No assumptions recorded — individual article files not yet written)*

---

## Contested items pending resolution

| ID | Article | Issue | Status |
|---|---|---|---|
| CONTEST-MDR-001 | Annex XIV | Clinical evaluation adequacy — "sufficient clinical evidence" has no bright-line threshold; assessed by Notified Body | Pattern 3 gate; requires Notified Body (or clinical expert) sign-off |
| CONTEST-MDR-002 | Annex I §1 | "State of the art" determination — no defined reference; MEDDEV and MDCG guidances provide context but not bright-lines | Pattern 3 gate |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Technical documentation | EU MDR Annex II+III, ISO 13485 §7.3.9 (DHF), FDA QMSR §820.30 (DHF) | Same underlying design records; EU MDR Annex II and III define the EU format; FDA QMSR defines the DHF format — both can be maintained as one set with jurisdiction-specific sections |
| Risk management file | EU MDR Annex I §3 (ISO 14971), ISO 13485 §7.1, FDA QMSR §820.30(g) | ISO 14971:2019 is the shared risk management standard |
| QMS | EU MDR Article 10(9) + Annex IX, ISO 13485, FDA QMSR | EU MDR requires QMS per Annex IX; ISO 13485 certification satisfies the QMS requirement for Notified Body assessment |
| PMS / PSUR / complaint handling | EU MDR Art. 83–89, ISO 13485 §8.2.1–8.2.3, FDA QMSR §820.198 | Same complaint data; different reporting thresholds and authorities |
| CAPA | EU MDR Article 10(9)(d), ISO 13485 §8.5.2, FDA QMSR §820.100 | Same CAPA process; FDA QMSR has the most prescriptive structure |
| Labeling | EU MDR Annex I §23 (25 elements), FDA 21 CFR Part 801, ISO 15223 (symbols) | Separate label reviews for each market; ISO 15223 symbols are recognized by both EU and FDA |
