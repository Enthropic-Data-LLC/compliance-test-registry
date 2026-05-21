# 29 CFR 1926 — Construction Industry Registry Index

**Authority:** 29 CFR Part 1926 (OSHA Construction Standards)
**Applicability:** Construction, alteration, and repair work — including painting and decorating
**Last updated:** 2026-05-20

---

## Standards parsed in this registry

| Section | Title | Confidence | File |
|---|---|---|---|
| 1926.451 | Scaffolds — General Requirements | MEDIUM | `1926.451-scaffolds.md` |
| 1926.501/502/503 | Fall Protection — Duty to Have, Criteria, Training | HIGH | `1926.501-fall-protection.md` |
| 1926.651/652 | Excavations — Specific Requirements and Protective Systems | MEDIUM | `1926.651-excavations.md` |

---

## Shared data model fields (1926 common schema)

The tests in this section rely on the following additional fields beyond the 1910 common schema:

```yaml
construction_site:
  site_id: str
  project_name: str
  general_contractor: str
  competent_person: str        # designated competent person for the specific hazard
  site_start_date: date
  site_end_date: date

worker:
  worker_id: str
  employer: str                # subcontractor or GC
  trade: str
  training_records: list[TrainingRecord]

daily_site_inspection:
  site_id: str
  inspection_date: date
  inspected_by: str
  competent_person_qualified: bool
  hazards_found: list[str]
  corrective_actions: list[str]
  workers_removed_from_area: bool   # when imminent danger found

fall_protection_plan:
  site_id: str
  applicable_area: str
  protection_method: str       # guardrail, safety_net, PFAS, warning_line, monitoring
  system_installed_date: date
  inspected_by: str
```

---

## Key construction-specific concepts

**Competent Person:** Someone capable of identifying existing and predictable hazards in the surroundings or working conditions that are unsanitary, hazardous, or dangerous to employees, and who has authorization to take prompt corrective measures. Each standard that uses this term (scaffolds, excavations, fall protection, etc.) imposes specific knowledge requirements for that standard.

**Qualified Person:** Someone who by possession of a recognized degree, certificate, or professional standing, or by extensive knowledge, training, and experience, has successfully demonstrated the ability to solve or resolve problems relating to the subject matter, work, or project.

**Employer responsibility:** In multi-employer construction worksites, the creating, exposing, correcting, and controlling employer doctrine applies. The test suite should accommodate multi-employer scenarios — a subcontractor may be the exposing employer even though the GC created the hazard.
