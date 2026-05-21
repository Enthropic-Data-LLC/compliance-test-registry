# FDA 21 CFR Part 820 / QMSR — Quality Management System Regulation for Medical Devices

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** 21 CFR Part 820 as amended by the Quality Management System Regulation (QMSR) final rule, effective February 2026
**Authority:** U.S. Food and Drug Administration (FDA) / CDRH, CBER
**Enforcing context:** Manufacturers of finished medical devices and components sold in the U.S.; applies to domestic and foreign device manufacturers
**Current version:** QMSR final rule published Feb 2, 2024; effective February 2, 2026 — aligns 21 CFR Part 820 to ISO 13485:2016 and incorporates it by reference
**Note:** The QMSR replaces the legacy Quality System Regulation (QSR). The primary regulatory text now explicitly incorporates ISO 13485:2016. Manufacturers must comply with ISO 13485 PLUS the additional FDA-specific requirements in §820.

---

## Summary

| Metric | Count |
|---|---|
| Primary incorporated standard | ISO 13485:2016 (fully incorporated by reference) |
| FDA-specific additions to ISO 13485 | ~15 supplemental requirements |
| Sections in 21 CFR Part 820 | ~20 (reduced from legacy QSR) |
| Sections parsed (individual files) | 0 (index only; individual section files pending) |
| Note on scope | ISO 13485 registry (see iso/13485/) covers the base requirements; this registry documents FDA-specific QMSR deltas only |
| Open assumptions | 0 |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## QMSR architecture — ISO 13485 + FDA deltas

The QMSR adopts a two-layer structure:

| Layer | Source | Description |
|---|---|---|
| Base QMS requirements | ISO 13485:2016 | Fully incorporated by reference; all ISO 13485 requirements apply |
| FDA-specific requirements | 21 CFR Part 820 §§820.1–820.400 | Additional U.S.-specific obligations; primarily complaint/MDR handling and records access |

Manufacturers who already have ISO 13485 certification have a strong foundation. The compliance delta is the FDA-specific layer.

---

## FDA-specific QMSR requirements (delta from ISO 13485)

### §820.1 — Scope, intent, and applicability

| Requirement | Confidence | Notes |
|---|---|---|
| Applies to finished device manufacturers, not component manufacturers (unless components sold as finished devices) | DETERMINISTIC | Scope determination is binary once device classification confirmed |
| Single quality system covering all facilities | PARAMETERIZED | Multi-site scope determination |

### §820.3 — Definitions

Key FDA-specific definitions that differ from or supplement ISO 13485:
- **Design History File (DHF):** Compilation of records describing the design history of a finished device
- **Device Master Record (DMR):** Compilation of records containing the procedures and specifications for a finished device
- **Device History Record (DHR):** Compilation of records for each manufactured batch/lot
- **Quality System Record (QSR):** All requirements not related to a specific device type

### §820.30 — Design Controls

| Sub-section | Requirement | Confidence | Notes |
|---|---|---|---|
| (a) General | Design controls apply to Class II and III devices; Class I only if automated or life-sustaining | DETERMINISTIC | Device class determines applicability |
| (b) Design and development planning | DETERMINISTIC | Design plan documents activities, responsibilities, interfaces; updated as design evolves |
| (c) Design input | DETERMINISTIC | Requirements documented; incomplete/ambiguous/conflicting requirements resolved; records retained |
| (d) Design output | DETERMINISTIC | Outputs meet design inputs; reference acceptance criteria; identify essential design outputs; approved before release |
| (e) Design review | DETERMINISTIC | Formal reviews at defined stages; participants include independent reviewer; records retained |
| (f) Design verification | DETERMINISTIC | Verification performed; methods documented; records retained |
| (g) Design validation | DETERMINISTIC | Validation under defined operating conditions; simulated or actual use conditions; includes software validation; records retained |
| (h) Design transfer | DETERMINISTIC | Device design correctly translated to production specifications; records retained |
| (i) Design changes | DETERMINISTIC | Changes identified, reviewed, approved before implementation; records retained |
| (j) Design History File | DETERMINISTIC | DHF maintained for each device; contains or references records demonstrating design was developed per design plan |

### §820.50 — Purchasing Controls

| Sub-section | Requirement | Confidence | Notes |
|---|---|---|---|
| (a) Evaluation of suppliers | DETERMINISTIC | Potential suppliers evaluated; approved supplier list maintained; evaluation criteria defined |
| (b) Purchasing data | DETERMINISTIC | Purchase orders specify applicable requirements; reviewed and approved before release |

### §820.70 — Production and Process Controls

| Sub-section | Requirement | Confidence | Notes |
|---|---|---|---|
| (a) General | DETERMINISTIC | Written procedures for production processes; deviations documented |
| (b) Environmental control | PARAMETERIZED | Environmental specifications established where environmental conditions could adversely affect product quality |
| (c) Personnel | PARAMETERIZED | Personnel in contact with product or product environment have health, cleanliness, and clothing requirements |
| (d) Contamination control | PARAMETERIZED | Contamination control procedures |
| (e) Buildings | PARAMETERIZED | Buildings adequate for operations |
| (f) Equipment | DETERMINISTIC | Equipment maintained in satisfactory condition; preventive maintenance schedule; records retained |
| (g) Automated processes | DETERMINISTIC | Computer software used in production/QS validated per intended use; validation documented; changes controlled |
| (h) Manufacturing material | PARAMETERIZED | Manufacturing materials that could affect device quality controlled |
| (i) Nonconforming product | DETERMINISTIC | Procedures to control nonconforming product; identification, documentation, evaluation, segregation, disposition |

### §820.72 — Inspection, Measuring, and Test Equipment

| Requirement | Confidence | Notes |
|---|---|---|
| Calibrated on scheduled basis | DETERMINISTIC | Calibration frequency defined |
| Calibrated against nationally recognized standards | DETERMINISTIC | Traceable calibration required |
| Calibration records retained | DETERMINISTIC | Records include device ID, calibration date, next calibration date, calibration results |
| Out-of-calibration actions documented | DETERMINISTIC | Impact assessment when equipment found out of calibration |

### §820.80 — Receiving, In-Process, and Finished Device Acceptance

| Sub-section | Requirement | Confidence | Notes |
|---|---|---|---|
| (a) General | DETERMINISTIC | Acceptance activities specified; records of acceptance retained |
| (b) Receiving acceptance | DETERMINISTIC | Incoming components and devices accepted per defined procedures; records retained |
| (c) In-process acceptance | DETERMINISTIC | In-process acceptance activities performed at defined stages; records retained |
| (d) Final acceptance | DETERMINISTIC | Finished device tested/examined per established procedures; all acceptance criteria met before release |
| (e) Acceptance records | DETERMINISTIC | Traceable to the person performing acceptance; date; quantity accepted/rejected |

### §820.100 — Corrective and Preventive Action (CAPA)

| Sub-section | Requirement | Confidence | Notes |
|---|---|---|---|
| (a) Procedures | DETERMINISTIC | Written CAPA procedure |
| (a)(1) | Analyze data to identify existing and potential causes of nonconforming product | DETERMINISTIC | Data sources: processes, work operations, concessions, quality audit reports, service records, complaints, returns |
| (a)(2) | Investigate the cause | DETERMINISTIC | Root cause investigation documented |
| (a)(3) | Identify the action needed | DETERMINISTIC | Corrective/preventive action identified |
| (a)(4) | Verify/validate the action | DETERMINISTIC | Effectiveness verification before implementation |
| (a)(5) | Implement and record changes | DETERMINISTIC | Changes implemented in methods and procedures; records retained |
| (a)(6) | Disseminate information | DETERMINISTIC | Relevant information disseminated to affected personnel |
| (a)(7) | Submit for management review | DETERMINISTIC | CAPA submitted for management review |
| (b) Records | DETERMINISTIC | All CAPA activities documented |

### §820.120 — Device Labeling

| Sub-section | Requirement | Confidence | Notes |
|---|---|---|---|
| (a) Label integrity | DETERMINISTIC | Labels legible and affixed during use; lot/batch number on labels |
| (b) Labeling inspection | DETERMINISTIC | Labeling inspected for accuracy; records retained |
| (c) Labeling storage | DETERMINISTIC | Labels stored to prevent mix-ups |
| (d) Labeling operations | DETERMINISTIC | Labeling operations prevent mix-ups; line clearance; reconciliation |
| (e) Control number | DETERMINISTIC | Control number on labeling if traceability required |

### §820.160 — Distribution

| Requirement | Confidence | Notes |
|---|---|---|
| Distribution records | DETERMINISTIC | Name and address of consignee; device description; quantity; date shipped; control number |
| Outdated/deteriorated devices not distributed | DETERMINISTIC | Only devices meeting acceptance criteria distributed |

### §820.180 — General Requirements for Records

| Requirement | Confidence | Notes |
|---|---|---|
| Retention period: 2 years from device release OR useful life of device (whichever is greater) | DETERMINISTIC | Minimum 2-year retention; implantable devices: useful life may be decades |
| Records available for FDA inspection | DETERMINISTIC | Accessible to FDA investigator; confidentiality maintained for trade secrets |

### §820.198 — Complaint Files

| Sub-section | Requirement | Confidence | Notes |
|---|---|---|---|
| (a) Complaint handling procedures | DETERMINISTIC | Written procedures; designated complaint handling unit |
| (b) Oral complaints | DETERMINISTIC | Oral complaints documented upon receipt |
| (c) Review complaints | DETERMINISTIC | All complaints reviewed and evaluated; determine if MDR reportable |
| (d)–(f) Investigation records | DETERMINISTIC | Records include: device name, date complaint received, unique device identifier, complainant name/address, nature of complaint, dates/results of investigation, corrective action, reply to complainant |

### §820.200 — Servicing (where applicable)

| Requirement | Confidence | Notes |
|---|---|---|
| Written servicing procedures | DETERMINISTIC | Where servicing is a specified requirement |
| Service records | DETERMINISTIC | Service reports; analysis of service reports for trends |

---

## MDR (Medical Device Reporting) linkage — §820.198(c)

Every complaint must be evaluated to determine if it is an MDR-reportable event under 21 CFR Part 803:
- Death: **30 calendar days** from becoming aware
- Serious injury: **30 calendar days** from becoming aware
- Malfunction that could cause or contribute to serious injury/death: **30 calendar days**
- Baseline reports: required for manufacturers of certain device types

**RDF treatment:** MDR reportability determination is PARAMETERIZED; the 30-day reporting deadline is DETERMINISTIC once a reportable event is identified.

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Design History File (DHF) | FDA QMSR §820.30(j), ISO 13485 §7.3.9, EU MDR Annex II | Same underlying design records; format requirements differ slightly |
| CAPA records | FDA QMSR §820.100, ISO 13485 §8.5.2–8.5.3, EU MDR Article 10(9) | FDA QMSR §820.100 is the most prescriptive with 7 explicit elements |
| Complaint handling + MDR | FDA QMSR §820.198 + 21 CFR Part 803, ISO 13485 §8.2.2–8.2.3, EU MDR Article 87 | Same complaint record; different regulatory reporting thresholds |
| Calibration records | FDA QMSR §820.72, ISO 13485 §7.6, ISO 9001 §7.1.5.2 | Identical requirements |
| Supplier controls | FDA QMSR §820.50, ISO 13485 §7.4, EU MDR Article 10(2) | Same approved supplier list; same evaluation records |
