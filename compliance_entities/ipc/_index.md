# IPC-A-610 / J-STD-001 — Electronics Assembly Acceptability Standards

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Acceptability criteria for electronic assemblies (IPC-A-610) and requirements for soldering of electrical and electronic assemblies (J-STD-001); applicable to PCB assembly, surface mount technology (SMT), through-hole soldering, and related processes
**Authority:** IPC (Association Connecting Electronics Industries); standards developed by industry consensus committees
**Enforcing context:** Contractual requirement in electronics manufacturing purchase orders; required by aerospace (IPC-A-610 Class 3 or AS Space Addendum), defense (MIL-specs reference), and medical device manufacturing; NADCAP electronics commodity references IPC
**Current editions:** IPC-A-610 Rev H (2020); J-STD-001 Rev H (2020); IPC-7711/7721 (rework/repair)
**Certification:** IPC-A-610 CIS (Certified IPC Specialist) and CQE (Certified Quality Engineer) for inspectors and trainers

---

## Summary

| Metric | Count |
|---|---|
| Product classes | 3 (Class 1 / Class 2 / Class 3) |
| Major defect categories (IPC-A-610) | ~20 inspection categories |
| Sections parsed (individual files) | 1 (electronics-assembly-acceptability.md — TH solder, SMT, placement, certifications, process controls, rework) |
| Fully automated (DETERMINISTIC) | High — class-based acceptability criteria are binary pass/fail |
| Partial automation (PARAMETERIZED) | Low-Moderate — process parameters |
| Human-determination required (CONTESTED) | Low — standard provides photographic acceptance criteria |
| Open assumptions | 0 |

---

## Product class — foundational scoping pre-condition

| Class | Applications | Requirement level |
|---|---|---|
| Class 1 | General electronics — consumer products, toys | Minimum — functional operation is the criterion |
| Class 2 | Dedicated service — computers, telecom, business equipment | Intermediate — extended life expected; some environment stress |
| Class 3 | High reliability — aerospace, military, medical, life-support | Maximum — continuous high performance; no compromise |

**Class is customer-specified in the contract or purchase order.** All acceptance criteria below are class-dependent. This is DETERMINISTIC once class is established.

---

## IPC-A-610 — selected acceptability criteria (DETERMINISTIC by class)

### Solder connections — through-hole

| Criterion | Class 1 | Class 2 | Class 3 |
|---|---|---|---|
| Minimum solder fill (barrel fill) | 25% | 75% | 75% |
| Wetting | Acceptable with conditions | Full wetting | Full wetting |
| Protrusion length minimum | 0.5mm | 0.5mm | 1.5mm |

All above are DETERMINISTIC pass/fail — measured against physical sample.

### Solder connections — surface mount (SMT)

| Criterion | Class 1 | Class 2 | Class 3 |
|---|---|---|---|
| Minimum side overhang | 50% of component pad | 50% | 25% |
| Minimum end-cap coverage (chip components) | 50% | 75% | 75% |
| Solder bridging | Acceptable if functional | Defect | Defect |

### Component placement

| Defect | Class 1 | Class 2 | Class 3 |
|---|---|---|---|
| Lifted component (one end raised) | Acceptable with conditions | Defect | Defect |
| Rotational misalignment >15° | Acceptable | Defect | Defect |
| Missing component | Defect | Defect | Defect |

---

## J-STD-001 — soldering process requirements

| Requirement | Confidence | Notes |
|---|---|---|
| Operator certification | DETERMINISTIC — operators must be trained and certified | Per IPC-J-STD-001 or equivalent |
| Solder alloy specification | DETERMINISTIC — must match purchase order requirement | Lead-free or leaded as specified |
| Flux type specification | DETERMINISTIC — flux type per IPC classification (ROL0, ROL1, etc.) | No-clean vs. water-wash must match process |
| Soldering iron tip temperature control | PARAMETERIZED — temperature range per assembly type | Within process limits |
| ESD precautions | DETERMINISTIC — ESD-safe handling for class 2/3 | ANSI/ESD S20.20 compliance |
| Rework and repair | DETERMINISTIC — only per IPC-7711/7721 procedures | Unauthorized rework is a defect |

---

## IPC certification requirements — DETERMINISTIC

| Role | Certification | Renewal |
|---|---|---|
| IPC-A-610 Inspector (CIS) | IPC Certified IPC Specialist | Every 2 years |
| IPC-A-610 Trainer (CIT) | IPC Certified IPC Trainer | Every 2 years |
| J-STD-001 Soldering Specialist | IPC/WHMA-A-620 or J-STD-001 CIS | Every 2 years |
| Master Instructor | IPC Master Instructor (MI) | Every 2 years |

Expired certifications = inspectors cannot perform acceptance inspection for class 2/3.

---

## Defect classification — DETERMINISTIC taxonomy

| Condition | Definition | Action required |
|---|---|---|
| Defect | Does not meet requirements; must be reworked, repaired, or scrapped | Mandatory corrective action |
| Process Indicator | Not a defect; may indicate a process control opportunity | Process investigation at organization's discretion |
| Acceptable | Meets the requirements | No action |

**There is no "conditional" acceptance in Class 3** — an item either meets requirements or is a defect.

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Operator qualification records | IPC J-STD-001, NADCAP (AC7120), AS9100 §7.2 | Same training records; NADCAP audits IPC certification currency |
| ESD controls | IPC-A-610, ANSI/ESD S20.20, MIL-STD-1686 | Same ESD program; IPC references ANSI/ESD |
| Rework/repair records | IPC-A-610, IPC-7711/7721, AS9100 §8.7 (nonconforming outputs) | Rework documented as nonconformity disposition |
| Product class definition | IPC-A-610 class, AS9100 (key characteristics), ITAR (defense articles) | Class 3 common for defense and medical |
| Inspection records | IPC-A-610, AS9100 §8.6, ISO 9001 §8.6 | First article inspection includes IPC criteria |
