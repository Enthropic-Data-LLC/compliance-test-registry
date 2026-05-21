# SOX — Sarbanes-Oxley Act (IT General Controls)

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** IT General Controls (ITGCs) underlying Section 404 (ICFR) and Section 302 (CEO/CFO certification)
**Authority:** U.S. Securities and Exchange Commission (SEC); PCAOB (auditing standards)
**Enforcing context:** All companies publicly traded on U.S. exchanges; accelerated filers require external auditor attestation of ICFR under §404(b); non-accelerated filers require management assessment only
**Note:** This registry covers the IT control surface only. Accounting/financial controls are out of scope. Methodology reference: COSO 2013 Internal Control Framework + PCAOB AS 2201.

---

## Summary

| Metric | Count |
|---|---|
| Applicable sections (IT-relevant) | §302, §404, §409 |
| ITGC domains | 4 (Access, Change Management, Computer Operations, Data Center) |
| Individual ITGCs | Varies by organization; typically 60–120 in a Moderate scope |
| Controls parsed (individual files) | 1 (`itgc-access-change-operations.md` — Logical Access, Change Management, Computer Operations, Deficiency Tracking) |
| Fully automated (DETERMINISTIC) | Moderate — access provisioning/deprovisioning cadence, change ticket existence, backup completion |
| Partial automation (PARAMETERIZED) | Significant — "appropriate" segregation of duties, review frequency |
| Human-determination required (CONTESTED) | Moderate — key control identification, materiality, scope |
| Open assumptions | 9 (ASSUME-SOX-ACCESS-001–004, ASSUME-SOX-CHANGE-001–002, ASSUME-SOX-OPS-001–002, ASSUME-SOX-DEF-001) |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## ITGC domain architecture

SOX IT compliance is not organized by statute but by the four IT General Control domains recognized by PCAOB AS 2201 and COSO. Automated system-level controls (application controls) that directly support financial reporting are additionally in scope.

| ITGC Domain | Description | Confidence projection |
|---|---|---|
| **Logical Access Controls** | User provisioning, privilege management, access reviews, terminated user removal, privileged account monitoring | HIGH–MEDIUM — most requirements have DETERMINISTIC thresholds (access review frequency, termination timeline) |
| **Change Management** | SDLC, change authorization, segregation of development/test/production, emergency change procedures | MEDIUM — change ticket existence is DETERMINISTIC; testing adequacy is PARAMETERIZED |
| **Computer Operations** | Batch job scheduling, backup/recovery, incident management, data center operations | HIGH–MEDIUM — backup completion is DETERMINISTIC; job failure investigation is PARAMETERIZED |
| **Physical and Environmental** | Data center access, CCTV, environmental monitoring | MEDIUM — badge log existence is DETERMINISTIC; coverage adequacy is PARAMETERIZED |

---

## Per-domain confidence map

### Logical Access Controls (highest audit frequency)

| Control | Description | Confidence | Notes |
|---|---|---|---|
| User access provisioning | Access granted only with authorized request | DETERMINISTIC | Ticket/approval exists before access grant |
| User access deprovisioning | Access removed upon termination or role change | DETERMINISTIC | Termination-to-revocation gap: typically ≤ 1 business day for privileged; ≤ 5 days for standard |
| Periodic access review | Access rights reviewed on defined cadence | PARAMETERIZED | Cadence is org-defined (quarterly or semi-annual is typical); completion is DETERMINISTIC |
| Segregation of duties (SoD) | Conflicting roles not combined in one user | PARAMETERIZED | SoD conflict matrix is org-defined; enforcement is DETERMINISTIC once matrix exists |
| Privileged access management | Admin/root accounts inventoried and monitored | MEDIUM | Inventory existence is DETERMINISTIC; monitoring adequacy is PARAMETERIZED |
| Service/shared account controls | Shared accounts prohibited or controlled | DETERMINISTIC | Existence of shared accounts without compensating controls = finding |
| Password policy enforcement | Password policy applied by system | DETERMINISTIC | Technical enforcement is binary |
| Remote access controls | VPN/MFA required for remote financial system access | DETERMINISTIC | MFA enforcement is binary |

### Change Management

| Control | Description | Confidence | Notes |
|---|---|---|---|
| Change authorization | Approved change ticket required before production change | DETERMINISTIC | Ticket with approval precedes change |
| Development/test/production separation | Three environments separated; no direct production access by developers | DETERMINISTIC | Environment separation is binary; access controls are DETERMINISTIC |
| Change testing | Changes tested in non-production before deployment | PARAMETERIZED | Test evidence must exist; adequacy of testing is PARAMETERIZED |
| Emergency change procedure | Emergency changes documented and approved retrospectively | PARAMETERIZED | Process existence is DETERMINISTIC; retrospective approval completeness is PARAMETERIZED |
| Change log completeness | All production changes captured in change management system | PARAMETERIZED | Sampling-based audit procedure |

### Computer Operations

| Control | Description | Confidence | Notes |
|---|---|---|---|
| Backup completion monitoring | Scheduled backups completed; failures investigated | DETERMINISTIC | Backup job completion log is DETERMINISTIC; investigation of failures is PARAMETERIZED |
| Backup restoration testing | Restore tests performed on defined cadence | PARAMETERIZED | Test cadence is org-defined; completion is DETERMINISTIC |
| Batch job monitoring | Scheduled batch jobs complete; failures investigated | DETERMINISTIC | Job completion log; failure investigation process |
| Incident/problem management | Incidents recorded, prioritized, resolved | PARAMETERIZED | Ticket existence is DETERMINISTIC; resolution timeliness is org-defined |
| Availability monitoring | Uptime and performance of financial systems monitored | PARAMETERIZED | Monitoring existence is DETERMINISTIC; threshold adequacy is PARAMETERIZED |

---

## Application controls (in-scope for §404)

Application controls are automated controls embedded in financial applications (ERP, GL, consolidation tools) that directly prevent or detect misstatements. They depend on ITGCs being effective.

| Control type | Examples | Confidence |
|---|---|---|
| Input validation | Field format checks, range checks on journal entries | DETERMINISTIC |
| Completeness checks | Record counts, hash totals | DETERMINISTIC |
| Authorization controls | Approval workflow enforcement in financial system | DETERMINISTIC |
| Interface controls | Automated reconciliation between systems | DETERMINISTIC — count/amount match is binary |
| Report generation | Accurate extraction of financial data for reporting | PARAMETERIZED |

---

## §302 — CEO/CFO Certification requirements

Each quarterly/annual filing, CEO and CFO must certify:
- They reviewed the filing
- No material misstatements
- Internal controls over financial reporting (ICFR) are designed and operating effectively
- They disclosed to the audit committee and auditors all significant ICFR deficiencies and material weaknesses

**RDF treatment:** §302 is PARAMETERIZED — the certification process is DETERMINISTIC (it exists or it doesn't), but the underlying ICFR assessment that supports it is PARAMETERIZED/CONTESTED.

---

## §404 — ICFR assessment requirements

| Party | Requirement | Threshold |
|---|---|---|
| Management | Annual written assessment of ICFR effectiveness | All accelerated filers and large accelerated filers |
| External auditor | Attestation on management's ICFR assessment | Large accelerated filers and accelerated filers only (§404(b)) |
| Non-accelerated filers | Management assessment only; no auditor attestation | Public float < $75M |

**Material weakness** — the key DETERMINISTIC threshold: A deficiency in ICFR such that there is a reasonable possibility that a material misstatement will not be prevented or detected. If management identifies a material weakness, the annual report must state ICFR is NOT effective.

---

## DEFICIENCY CLASSIFICATION — reference table

| Classification | Definition | Disclosure requirement | CI gate impact |
|---|---|---|---|
| Control deficiency | A control does not operate as intended | Internal remediation tracking; no public disclosure required | Pattern 2 — engineering remediation |
| Significant deficiency | A control deficiency (or combination) that is less severe than a material weakness but important enough to merit audit committee attention | Communicate to audit committee and auditors | Pattern 3 — Compliance Officer notification |
| Material weakness | A deficiency (or combination) that creates a reasonable possibility of material misstatement | Must disclose publicly in §404 report | IMMEDIATE BLOCK — board/audit committee notification required |

---

## Key DETERMINISTIC thresholds

| Obligation | Threshold | Domain |
|---|---|---|
| Privileged account deprovisioning | ≤1 business day from termination | Logical Access |
| Standard account deprovisioning | ≤5 business days from termination | Logical Access |
| Role-change excess access removal | ≤10 business days from role change | Logical Access |
| Privileged access review cadence | Every 3 calendar months | Logical Access |
| Standard access review cadence | Every 12 calendar months | Logical Access |
| Access review exception remediation | Within 30 days of review completion | Logical Access |
| SoD matrix review | At least once per 12 calendar months | Logical Access |
| Emergency change retrospective approval | Within 5 business days | Change Management |
| Backup failure investigation | Within 1 business day | Computer Operations |
| Backup restoration test | At least once per 12 calendar months | Computer Operations |
| Audit log retention | 7 years (§802 / PCAOB AS 2301) | Computer Operations |

---

## Open assumption registry

| ID | Domain | Description | Review date |
|---|---|---|---|
| ASSUME-SOX-ACCESS-001 | Provisioning | Approval before access grant; approver ≠ requestor; approved roles must match provisioned roles | 2026-05-21 |
| ASSUME-SOX-ACCESS-002 | Deprovisioning | Privileged: ≤1 business day from termination; standard: ≤5 business days; role change excess: ≤10 business days | 2026-05-21 |
| ASSUME-SOX-ACCESS-003 | Access review | Quarterly for privileged; annual for standard; exceptions remediated within 30 days | 2026-05-21 |
| ASSUME-SOX-ACCESS-004 | SoD | Matrix reviewed annually; active conflicts require approved compensating control or management exception | 2026-05-21 |
| ASSUME-SOX-CHANGE-001 | Change authorization | Approval before deployment; developer ≠ deployer ≠ approver; test evidence required; emergency retro within 5 days | 2026-05-21 |
| ASSUME-SOX-CHANGE-002 | Environment separation | Three environments required; developers lack production write access | 2026-05-21 |
| ASSUME-SOX-OPS-001 | Backup monitoring | Failures investigated within 1 business day; annual restoration test; completion logs required | 2026-05-21 |
| ASSUME-SOX-OPS-002 | Audit log retention | 7-year retention (§802 / PCAOB); tamper-evident or write-once storage | 2026-05-21 |
| ASSUME-SOX-DEF-001 | Deficiency tracking | All deficiencies have remediation plan with target date; MW classification requires management + auditor agreement | 2026-05-21 |

---

## Contested items pending resolution

*(None recorded yet)*

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Access provisioning/deprovisioning | SOX ITGCs, SOC 2 CC6, ISO 27001 A.5.18, HIPAA §164.312(a) | Same IAM evidence; SOX auditors will sample provisioning tickets from the same system |
| Change management records | SOX ITGCs, SOC 2 CC8, ISO 27001 A.8.32, PCI DSS Req 6 | Change tickets satisfy all four; PCI adds development security testing requirement |
| Backup records | SOX Computer Operations, SOC 2 A1.2, ISO 27001 A.8.13, HIPAA §164.308(a)(7) | Backup completion logs and restore test evidence shared across all |
| Privileged access monitoring | SOX ITGCs, PCI DSS Req 7–8, FedRAMP AC, CMMC AC | Admin account activity logs are the shared evidence artifact |
| Audit logs | SOX (general record retention), SOC 2 CC7, PCI DSS Req 10 | SOX does not specify log retention explicitly; 7-year document retention under §802 applies to audit workpapers |

---

## CI/CD gate configuration

Standard three-tier gate (see NERC CIP registry). SOX-specific constraints:

- **Scope determination:** ITGC tests run only for systems identified as "key systems" supporting financial reporting. Scope changes require audit committee notification.
- **Deficiency classification tracker:** Any Pattern 1/2/3 failure is classified against the deficiency taxonomy (deficiency / significant deficiency / material weakness) by the ITGC owner before the next quarterly certification.
- **Termination-to-revocation clock:** Deprovisioning timer starts at `employee_terminated_at`; Pattern 1 failure if privileged access not revoked within 1 business day.
- **SoD conflict detection:** SoD matrix must be current (< 6 months since last review). Access combinations flagged by the matrix generate Pattern 2 failures requiring owner attestation.

---

## Roadmap — individual ITGC file parse priority

| Priority | Domain | Control | Notes |
|---|---|---|---|
| 1 | Logical Access | User provisioning/deprovisioning | ✅ Parsed — `itgc-access-change-operations.md` §1.1–1.2 |
| 2 | Logical Access | Privileged access management | ✅ Parsed — `itgc-access-change-operations.md` §1.2 |
| 3 | Logical Access | Periodic access review | ✅ Parsed — `itgc-access-change-operations.md` §1.3 |
| 4 | Change Management | Authorization (approval before production) | ✅ Parsed — `itgc-access-change-operations.md` §2.1 |
| 5 | Change Management | Dev/test/production separation | ✅ Parsed — `itgc-access-change-operations.md` §2.2 |
| 6 | Computer Operations | Backup monitoring | ✅ Parsed — `itgc-access-change-operations.md` §3.1 |
| 7 | Computer Operations | Backup restoration testing | ✅ Parsed — `itgc-access-change-operations.md` §3.1 |
| 8 | Logical Access | Segregation of duties | ✅ Parsed — `itgc-access-change-operations.md` §1.4 |
| 9 | Change Management | Emergency change | ✅ Parsed — `itgc-access-change-operations.md` §2.1 |
| 10 | Physical | Data center access | MEDIUM confidence — pending |
