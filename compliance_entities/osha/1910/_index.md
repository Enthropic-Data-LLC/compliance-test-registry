# 29 CFR 1910 — General Industry Registry Index

**Authority:** 29 CFR Part 1910 (OSHA General Industry Standards)
**Applicability:** Employers with workers not covered by specific industry-specific OSHA standards (not construction, agriculture, or maritime)
**Last updated:** 2026-05-20

---

## Standards parsed in this registry

| Section | Title | Confidence | File |
|---|---|---|---|
| 1910.38 | Emergency Action Plans | HIGH | `1910.38-eap.md` |
| 1910.119 | Process Safety Management of Highly Hazardous Chemicals | MEDIUM | `1910.119-psm.md` |
| 1910.120 | Hazardous Waste Operations and Emergency Response (HAZWOPER) | MEDIUM | `1910.120-hazwoper.md` |
| 1910.132 | Personal Protective Equipment — General Requirements | MEDIUM | `1910.132-ppe.md` |
| 1910.134 | Respiratory Protection | MEDIUM | `1910.134-respiratory.md` |
| 1910.146 | Permit-Required Confined Spaces | MEDIUM | `1910.146-confined-space.md` |
| 1910.147 | Control of Hazardous Energy (Lockout/Tagout) | HIGH | `1910.147-loto.md` |
| 1910.178 | Powered Industrial Trucks | MEDIUM | `1910.178-powered-industrial-trucks.md` |
| 1910.212 | General Requirements for All Machines (Machine Guarding) | CONTESTED | `1910.212-machine-guarding.md` |
| 1910.1200 | Hazard Communication | HIGH | `1910.1200-hazcom.md` |

---

## Shared data model fields (1910 common schema)

The tests in this section rely on the following shared fields in the safety management database:

```yaml
employee:
  employee_id: str
  job_title: str
  department: str
  hire_date: date
  training_records: list[TrainingRecord]
  medical_clearances: list[MedicalClearance]

training_record:
  standard_id: str          # e.g., "1910.147"
  topic: str
  training_date: date
  trainer: str
  refresher_due: date
  method: str               # classroom, OJT, online, hands-on

written_program:
  standard_id: str
  last_reviewed_date: date
  reviewed_by: str
  approval_signature_hash: str
  version: str

equipment:
  equipment_id: str
  equipment_type: str
  location: str
  last_inspection_date: date
  inspection_by: str
  status: str               # active, LOTO, OOS, decommissioned
```
