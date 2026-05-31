# Cross-Framework Dependency Map

**Document version:** 2026.05
**Last updated:** 2026-05-20
**Purpose:** Documents shared evidence artifacts, shared controls, and shared infrastructure that satisfy multiple frameworks simultaneously. The primary value is IMS planning: knowing that one investment addresses five frameworks prevents duplicated programs and conflicting implementations.

---

## How to Use This Document

For each shared artifact below:
- **Build once, satisfy many:** Implement the artifact to the most demanding specification among all frameworks that require it. The others are automatically satisfied.
- **Watch for conflicts:** Where two frameworks specify different values for the same artifact (e.g., different log retention periods), the longer/stricter requirement governs.
- **Avoid fragmentation:** Do not create separate breach notification procedures for GDPR, HIPAA, NYDFS, and DORA. One IRP with regulatory-specific annexes is the right architecture.

---

## Artifact Clusters

### 1. Incident Response Plan (IRP)

**Build to:** DORA Art. 18 (most structured template requirement in the registry)

| Framework | Section | Specific obligation |
|---|---|---|
| NIST SP 800-53 | IR-8 | IR plan; roles/responsibilities; escalation |
| NIST CSF 2.0 | RS.RP / RC.RP | Response and recovery planning |
| ISO 27001 | A.5.26 / A.5.24 | Information security incident management |
| HIPAA Security Rule | §164.308(a)(6) | Security incident procedures |
| GDPR | Art. 33–34 | Breach notification procedures |
| UK GDPR | Art. 33–34 | Same as GDPR — 72h to ICO |
| NYDFS Part 500 | §500.16 | IRP required; annual testing |
| DORA | Art. 18 | ICT incident management process — most detailed template |
| PCI DSS | Req 12.10 | Incident response plan with 7 required elements |
| SOC 2 | CC7.3–CC7.5 | Incident response procedures |
| NERC CIP | CIP-008-6 | Cyber Security Incident Response Plans |
| TSA Pipeline | SD-02D Goal 3 | Written IRP; annual testing |
| NIST SP 800-82 | IR-8 (OT tailoring) | OT-specific IRP annex |
| NRC 10 CFR 73 | §73.54(e) | Nuclear cybersecurity incident response |
| ISO 45001 | §10.2 | OH&S incident investigation |
| EPA RMP | §68 Subpart E | Emergency response plan |
| EPCRA | §303 | Emergency planning with LEPC |

**Single-document architecture:** One IRP document with:
- Core structure (roles, escalation, communication tree)
- Regulatory annexes: GDPR/UK GDPR 72h timeline; HIPAA breach assessment; NYDFS notification; DORA classification; NERC CIP EOP; RMP emergency response
- OT-specific runbooks (if OT in scope)

---

### 2. Audit Log Retention

**Build to:** NYDFS Part 500 §500.06 — 6 years (longest in registry)

| Framework | Retention period | Section |
|---|---|---|
| NYDFS Part 500 | **6 years** | §500.06 |
| SWIFT CSP | 12 months | CSP Control 6.4 |
| PCI DSS | 12 months (3 months immediately available) | Req 10.7 |
| HIPAA Security Rule | 6 years (audit logs = required documentation) | §164.316(b)(2) |
| SOX ITGC | 7 years (financial records; audit logs supporting financial systems) | SOX §802 |
| FINRA | 3 years (electronic communications) | Rule 4511 |
| SEC / FINRA | 6 years (most broker-dealer records) | SEA Rule 17a-4 |
| NERC CIP | CIP-007 R5: 90 days rolling; CIP-008: 3 years for incident records | CIP-007-6 |
| GDPR | "No longer than necessary" — operational practice 12–24 months | Art. 5(1)(e) |
| FedRAMP | System-defined per NIST 800-53 AU-11 (3 years typical) | AU-11 |

**Conflict resolution:** When systems are subject to both NYDFS (6yr) and PCI DSS (1yr), retain for 6 years. NYDFS governs. For purely financial broker-dealer systems with no NYDFS applicability, SOX 7yr governs.

---

### 3. Penetration Testing Program

**Build to:** PCI DSS Req 11.4 + NYDFS §500.05 (most prescriptive combination)

| Framework | Frequency | Scope | Section |
|---|---|---|---|
| PCI DSS | Annual + after significant changes | Internal and external; application and network | Req 11.4 |
| NYDFS Part 500 | Annual | External-facing systems minimum | §500.05 |
| SWIFT CSP | Annual | SWIFT infrastructure | Control 7.3A |
| DORA | Threat-led penetration testing (TLPT) for significant firms | 3 years | Art. 26 |
| SOC 2 | No defined frequency; auditor expectation = annual | External; control testing | CC7.1 |
| NERC CIP | No explicit pentest; but vulnerability assessments required | CDE | CIP-007-6 R3 |
| NIST SP 800-53 | CA-8 — frequency per organization policy | System boundary | CA-8 |
| FedRAMP | Annual assessment | Moderate/High baselines | CA-2 / CA-8 |

**Single program:** Annual pentest with defined scope. Add DORA TLPT as a 3-year deep-dive for financial entities. Use results to satisfy all frameworks simultaneously.

---

### 4. Vulnerability Management Program

**Build to:** PCI DSS Req 11.3 (quarterly internal + external scans) as minimum scan cadence

| Framework | Scan frequency | Section |
|---|---|---|
| PCI DSS | Quarterly external ASV scans + quarterly internal | Req 11.3 |
| NYDFS Part 500 | Periodic vulnerability assessment (quarterly interpreted) | §500.05 |
| SWIFT CSP | Quarterly internal vulnerability scanning | Control 2.7A |
| FedRAMP | Monthly scanning (High baseline) | RA-5 |
| NERC CIP | 35-day patching window (high impact) | CIP-007-6 R2 |
| TSA Pipeline | Vulnerability management program | SD-02D Goal 2 |
| ISO 27001 | A.8.8 — management of technical vulnerabilities | — |
| CMMC | RM.L2-3.11.2 — vulnerability scans | §3.11.2 |
| NIST SP 800-53 | RA-5 — frequency per org policy | RA-5 |

**Critical patch windows (DETERMINISTIC — most demanding governs):**
- NERC CIP: 35 days (high impact BES Cyber Systems)
- SWIFT CSP: 3 months (critical patches)
- PCI DSS: 1 month (critical patches per Req 6.3)

---

### 5. MFA Enforcement

**Build to:** NYDFS §500.12 (most prescriptive language — all remote access + privileged access)

| Framework | MFA requirement | Section |
|---|---|---|
| NYDFS Part 500 | All remote access; all privileged access; all external-facing web applications | §500.12 |
| PCI DSS | All remote access; all non-console administrative access to CDE | Req 8.4/8.5 |
| SWIFT CSP | All operators accessing SWIFT infrastructure | Control 3.2 |
| TSA Pipeline SD-02D | MFA for remote access to OT systems | Goal 2 |
| NRC 10 CFR 73 | — (physical/logical combined access control) | RG 5.71 |
| CMMC / 800-171 | IA.L2-3.5.3 — privileged and remote access | §3.5.3 |
| FedRAMP | IA-2(1) — required for Moderate/High baseline | IA-2(1) |
| ISO 27001 | A.8.5 — Secure Authentication | — |
| HIPAA | A.5.16 (Addressable — effectively required) | §164.312(d) |

**Single implementation:** Deploy MFA for (a) all remote access, (b) all privileged/admin access, (c) all external-facing web applications. This satisfies all frameworks. No need for separate MFA scopes per framework.

---

### 6. Data Processing Agreements / Vendor Management

**Build to:** EU GDPR Art. 28 + HIPAA BAA (most detailed required elements)

| Framework | Agreement type | Required before | Section |
|---|---|---|---|
| EU GDPR | Data Processing Agreement (DPA) | Before processor engagement | Art. 28 |
| UK GDPR | DPA (UK template / IDTA addendum) | Before processor engagement | Art. 28 |
| HIPAA | Business Associate Agreement (BAA) | Before disclosing PHI | §164.308(b) |
| LGPD | Data processing agreement | Before processor engagement | Art. 37–38 |
| CCPA | Service Provider contract | Before sharing personal information | §1798.140(ag) |
| ISO 27001 | Supplier security policy + agreements | Supplier onboarding | A.5.19–5.22 |
| PCI DSS | Contractual security obligations | Before engaging service provider | Req 12.8 |
| NERC CIP | Electronic Access Security controls for vendors | CIP-005 / CIP-013 | — |
| NIST 800-171 | CUI flow-down in contracts | Before CUI shared with supplier | §3.1.3 |
| DORA | ICT third-party contract requirements (12-element checklist) | Before ICT service | Art. 30(2) |

**Single vendor assessment framework:** One vendor security questionnaire and contract addendum that covers GDPR DPA fields, HIPAA BAA elements, DORA Art. 30(2) 12 elements, and PCI DSS Req 12.8 requirements. Checked at onboarding; reviewed annually.

---

### 7. CAPA / Corrective Action System

**Build to:** ISO 13485 §8.5.2 (most explicit field requirements in the registry)

| Framework | Section | Scope |
|---|---|---|
| ISO 9001 | §10.2 | General QMS nonconformity |
| ISO 13485 | §8.5.2 | Medical device CAPA — 7 explicit elements |
| ISO 14001 | §10.2 | Environmental nonconformity |
| ISO 45001 | §10.2 | OH&S incident and nonconformity |
| ISO 27001 | §10.1 | ISMS nonconformity |
| PCI DSS | Req 12.10.6 | Security control failures |
| HIPAA | §164.308(a)(8) | Security program review and updates |
| SOX | ITGC control failures | Remediation documentation |
| NERC CIP | CIP-007-6 / CIP-010-4 | BES Cyber System exceptions |
| FDA QMSR | §820.100 | Device CAPA |
| IEC 62304 | §9 | Software problem resolution |

**Single CAPA system:** One tracking system (Kanboard, Jira, etc.) with mandatory fields: description, root cause, corrective action, effectiveness verification, closure date. Map regulatory-specific fields as custom metadata.

---

### 8. Training and Awareness Records

**Build to:** NERC CIP-004-7 (most granular personnel training requirements in the registry)

| Framework | Training type | Records retained | Section |
|---|---|---|---|
| NERC CIP | CIP-004-7 | Role-based; annual; per-person completion; 3 years | CIP-004-7 R2 |
| OSHA 1910.1200 | HazCom training | Initial + annual; all hazardous chemical handlers; duration of employment | §1910.1200(h) |
| RCRA | Hazardous waste handler training | Initial + annual; LQG; 3 years | 40 CFR §262.17 |
| ISO 27001 | A.6.3 | Awareness and training records | — |
| HIPAA | §164.308(a)(5) | Workforce training; periodic; records retained | — |
| PCI DSS | Req 12.6 | Annual security awareness; all personnel | Req 12.6 |
| CMMC / 800-171 | AT.L2 | Security awareness training for all users | §3.2.1 |
| IPC J-STD-001 | Operator certification | Biennial CIS/CIT renewal | — |
| NADCAP | Operator qualification | Currency per commodity; renewal per schedule | — |

**Single training management system:** One LMS with course completion records. Tag each record with applicable frameworks. Expiry-date tracking covers all renewal requirements.

---

### 9. Business Continuity / Recovery Plans

**Build to:** DORA Art. 11 + NIST SP 800-53 CP family (most prescriptive combination)

| Framework | Plan type | Testing frequency | Section |
|---|---|---|---|
| DORA | ICT Business Continuity Policy + BCP | Annual | Art. 11 |
| NIST SP 800-53 | CP-2 (Contingency Plan) | Annual test | CP-2 |
| ISO 22301 | BCMS (related standard — not in this registry) | — | — |
| NERC CIP | CIP-009-6 Recovery Plans | Annual (tabletop or operational) | CIP-009-6 |
| FFIEC | BCP handbook | Annual review + exercise | BCP handbook |
| TSA Pipeline SD-02D | Recovery Plan | Annual test | SD-02D Goal 3 |
| PCI DSS | Req 12.3.4 | — | Req 12.3 |
| FedRAMP | CP-2 / CP-4 (test annually at Moderate/High) | Annual | CP-4 |

---

### 10. Encryption at Rest / In Transit

**Build to:** FIPS 140-2/3 validated modules where US government / FedRAMP required; AES-256 elsewhere

| Framework | At rest | In transit | Section |
|---|---|---|---|
| FedRAMP | FIPS 140-2/3 validated | TLS 1.2+ (TLS 1.3 preferred) | SC-28, SC-8 |
| CMMC / 800-171 | Encrypt CUI at rest | Encrypt CUI in transit | §3.13.8 / §3.13.10 |
| PCI DSS | Strong cryptography (AES-256 / RSA-2048+) | TLS 1.2 minimum | Req 3.5 / Req 4.2 |
| HIPAA | Addressable — effectively required (AES-256) | TLS 1.2+ | §164.312(a)(2)(iv) |
| GDPR | Appropriate technical measures (Art. 32) — AES-256 is safe harbor standard | TLS 1.2+ | Art. 32 |
| NYDFS Part 500 | Encryption of NPI in transit and at rest | TLS 1.2+ | §500.15 |
| ISO 27001 | A.8.24 (cryptography policy) | — | — |

**Single cryptography policy:** One cryptography policy that specifies AES-256 (at rest) and TLS 1.2 minimum / TLS 1.3 preferred (in transit). State FIPS 140-2/3 applicability for FedRAMP/government systems. Satisfies all frameworks.
