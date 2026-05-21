# IEC 62443 — Industrial Automation and Control System (IACS) Security

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Full IEC 62443 series — cybersecurity for Industrial Automation and Control Systems (IACS) including SCADA, DCS, PLC, safety systems, and their networks
**Authority:** International Electrotechnical Commission (IEC), Technical Committee 65 (TC65)
**Enforcing context:** Asset owners operating IACS; system integrators designing/deploying IACS; component/product suppliers; applies across all industrial sectors (manufacturing, oil & gas, utilities, water/wastewater, transportation, building automation, chemical) — note: NERC CIP covers electric utility IACS separately
**Note:** IEC 62443 is the OT/ICS security counterpart to NIST 800-53 (IT security). NERC CIP is a sector-specific implementation of IACS security concepts for the North American electric grid. Understanding 62443 is foundational to any OT security compliance program.

---

## Summary

| Metric | Count |
|---|---|
| Series parts (current and draft) | 13 |
| Primary addressable audiences | 3 (asset owners, integrators, product/component suppliers) |
| Security levels | 4 (SL 1–4) |
| Foundational requirements (FR) | 7 |
| System requirements (SR) | ~110 |
| Component requirements (CR) | ~90 |
| Requirements parsed (individual files) | 2 (fr1-fr3-iam-use-integrity.md + fr4-fr7-confidentiality-availability.md) — all 7 FRs covered |
| Fully automated (DETERMINISTIC) | High once SL-T established — 16 DETERMINISTIC thresholds across all 7 FRs |
| Partial automation (PARAMETERIZED) | Moderate — RBAC adequacy, monitoring design, crypto selection |
| Human-determination required (CONTESTED) | Low — zone/conduit boundary determination is PARAMETERIZED (not CONTESTED) |
| Open assumptions | 8 |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Series architecture

IEC 62443 is organized into 4 groups:

| Group | Parts | Focus | Audience |
|---|---|---|---|
| **General** | 62443-1-1 (concepts), 62443-1-2 (glossary), 62443-1-3 (metrics), 62443-1-4 (lifecycle) | Foundational concepts and framework | All stakeholders |
| **Policies & Procedures** | 62443-2-1 (IACS security program), 62443-2-2 (operating IACS), 62443-2-3 (patch management), 62443-2-4 (supplier requirements for service providers) | Management and operational requirements | Asset owners, service providers |
| **System** | 62443-3-2 (security risk assessment for system design), 62443-3-3 (system security requirements and security levels) | System-level requirements | Asset owners, integrators |
| **Component** | 62443-4-1 (product development requirements), 62443-4-2 (technical security requirements for IACS components) | Component/product requirements | Product/component suppliers |

---

## Security Level framework — pre-condition to all tests

All requirements in IEC 62443-3-3 and 62443-4-2 are expressed relative to a Security Level (SL):

| Level | Description | Adversary capability |
|---|---|---|
| SL 1 | Protection against casual or coincidental violation | Unskilled attacker; no motivation |
| SL 2 | Protection against intentional violation using simple means | Skilled attacker; low resources; general motivation |
| SL 3 | Protection against intentional violation using sophisticated means | Skilled attacker; moderate resources; IACS-specific motivation |
| SL 4 | Protection against state-sponsored, sophisticated attacks | Nation-state level; unlimited resources; specific motivation |

Three SL concepts exist:
- **SL Target (SL-T):** Desired security level for a zone/conduit — defined by risk assessment
- **SL Capability (SL-C):** Security level a component/system is capable of achieving
- **SL Achieved (SL-A):** Actual security level achieved in the deployed system

Test framework: verify SL-A ≥ SL-T for each zone and conduit.

---

## Foundational Requirements (FR) — the 7-FR structure

All system requirements in 62443-3-3 are organized under 7 Foundational Requirements:

| FR | Name | Abbreviation | Key test themes |
|---|---|---|---|
| FR 1 | Identification and Authentication Control | IAC | User and device authentication; MFA; PKI; account management |
| FR 2 | Use Control | UC | Authorization; least privilege; audit logging |
| FR 3 | System Integrity | SI | Malware protection; integrity verification; patching |
| FR 4 | Data Confidentiality | DC | Encryption at rest and in transit; data classification |
| FR 5 | Restricted Data Flow | RDF | Zone and conduit architecture; firewalls; unidirectional gateways |
| FR 6 | Timely Response to Events | TRE | Audit log management; incident response; alert notification |
| FR 7 | Resource Availability | RA | Denial-of-service protection; backup/recovery; energy management |

---

## 62443-3-3 System Security Requirements — per-FR confidence map

### FR 1 — Identification and Authentication Control

| SR | Requirement | SL scope | Confidence | Notes |
|---|---|---|---|---|
| SR 1.1 | Human user identification and authentication | SL 1–4 | HIGH | Unique IDs; authentication required; MFA at SL 2+ |
| SR 1.2 | Software process and device identification and authentication | SL 1–4 | MEDIUM | Machine/device identity; certificates at SL 3+ |
| SR 1.3 | Account management | SL 1–4 | DETERMINISTIC | Account lifecycle; provisioning/deprovisioning; review cadence (SL 2+: periodic review required) |
| SR 1.4 | Identifier management | SL 1–4 | DETERMINISTIC | Unique identifier per user/device; no reuse |
| SR 1.5 | Authenticator management | SL 1–4 | DETERMINISTIC | Password strength; expiry; revocation |
| SR 1.6 | Wireless access management | SL 1–4 | MEDIUM | SSID management; authentication method |
| SR 1.7 | Strength of password-based authentication | SL 1–4 | DETERMINISTIC | Minimum length, complexity, history — org-defined but bounded by SL |
| SR 1.8 | PKI certificates | SL 3–4 | PARAMETERIZED | Certificate management; CA trust |
| SR 1.9 | Strength of public key-based authentication | SL 3–4 | MEDIUM | Key length; algorithm |
| SR 1.10 | Authenticator feedback | SL 1–4 | DETERMINISTIC | Authentication feedback does not reveal authenticator content |
| SR 1.11 | Unsuccessful login attempts | SL 1–4 | DETERMINISTIC | Lockout after defined failed attempts; lockout duration |
| SR 1.12 | System use notification | SL 2–4 | DETERMINISTIC | Login banner required |
| SR 1.13 | Access via untrusted networks | SL 2–4 | MEDIUM | MFA or additional authentication for untrusted network access |

### FR 2 — Use Control

| SR | Requirement | SL scope | Confidence | Notes |
|---|---|---|---|---|
| SR 2.1 | Authorization enforcement | SL 1–4 | MEDIUM | Least privilege; role-based access control |
| SR 2.2 | Wireless use control | SL 1–4 | MEDIUM | Authorization required for wireless devices |
| SR 2.3 | Use control for portable and mobile devices | SL 1–4 | MEDIUM | Portable device authorization and control |
| SR 2.4 | Mobile code | SL 2–4 | PARAMETERIZED | Mobile code authorization and integrity |
| SR 2.5 | Session lock | SL 2–4 | DETERMINISTIC | Session lock after inactivity period |
| SR 2.6 | Remote session termination | SL 1–4 | DETERMINISTIC | Ability to terminate remote sessions |
| SR 2.7 | Concurrent session control | SL 3–4 | DETERMINISTIC | Limit concurrent sessions per account |
| SR 2.8 | Auditable events | SL 1–4 | DETERMINISTIC | Defined list of auditable events logged |
| SR 2.9 | Audit storage capacity | SL 1–4 | PARAMETERIZED | Adequate capacity to store audit records; overflow handling |
| SR 2.10 | Response to audit processing failures | SL 1–4 | MEDIUM | Alert and response when audit processing fails |
| SR 2.11 | Timestamps | SL 1–4 | DETERMINISTIC | Time synchronization; NTP; timestamp accuracy |
| SR 2.12 | Non-repudiation | SL 3–4 | MEDIUM | Actions cannot be denied; digital signatures |

### FR 3 — System Integrity

| SR | Requirement | SL scope | Confidence | Notes |
|---|---|---|---|---|
| SR 3.1 | Communication integrity | SL 1–4 | MEDIUM | Integrity protection for communication (checksums at SL 1; cryptographic at SL 2+) |
| SR 3.2 | Malicious code protection | SL 1–4 | DETERMINISTIC | Malware protection deployed; definitions maintained |
| SR 3.3 | Security functionality verification | SL 1–4 | PARAMETERIZED | Boot integrity verification; startup self-tests |
| SR 3.4 | Software and information integrity | SL 2–4 | MEDIUM | Change detection; integrity monitoring |
| SR 3.5 | Input validation | SL 1–4 | PARAMETERIZED | Input validation on all external interfaces |
| SR 3.6 | Deterministic output | SL 2–4 | PARAMETERIZED | System behavior deterministic under attack conditions |
| SR 3.7 | Error handling | SL 1–4 | PARAMETERIZED | Error handling does not reveal sensitive information |
| SR 3.8 | Session integrity | SL 1–4 | MEDIUM | Session management integrity |
| SR 3.9 | Protection of audit information | SL 1–4 | DETERMINISTIC | Audit logs protected from unauthorized modification |

### FR 4 — Data Confidentiality

| SR | Requirement | SL scope | Confidence | Notes |
|---|---|---|---|---|
| SR 4.1 | Information confidentiality | SL 2–4 | MEDIUM | Encryption of sensitive data in transit at SL 2+; at rest at SL 3+ |
| SR 4.2 | Information persistence | SL 2–4 | MEDIUM | Data sanitization before media reuse |
| SR 4.3 | Use of cryptography | SL 3–4 | PARAMETERIZED | Cryptographic module strength; algorithm selection |

### FR 5 — Restricted Data Flow

| SR | Requirement | SL scope | Confidence | Notes |
|---|---|---|---|---|
| SR 5.1 | Network segmentation | SL 1–4 | HIGH | Zone and conduit model; firewalls at zone boundaries; architecture is DETERMINISTIC once zones defined |
| SR 5.2 | Zone boundary protection | SL 1–4 | HIGH | Firewall rules; default deny; inbound/outbound restrictions |
| SR 5.3 | General purpose person-to-person communication restriction | SL 3–4 | MEDIUM | Email/messaging restrictions within IACS |
| SR 5.4 | Application partitioning | SL 3–4 | PARAMETERIZED | Separation of IACS from non-IACS applications |

### FR 6 — Timely Response to Events

| SR | Requirement | SL scope | Confidence | Notes |
|---|---|---|---|---|
| SR 6.1 | Audit log accessibility | SL 1–4 | DETERMINISTIC | Audit logs accessible to authorized personnel |
| SR 6.2 | Continuous monitoring | SL 2–4 | PARAMETERIZED | Monitoring for anomalous behavior |

### FR 7 — Resource Availability

| SR | Requirement | SL scope | Confidence | Notes |
|---|---|---|---|---|
| SR 7.1 | Denial of service protection | SL 1–4 | MEDIUM | DoS protection mechanisms |
| SR 7.2 | Resource management | SL 2–4 | PARAMETERIZED | Resource limits; availability of resources under attack |
| SR 7.3 | Control system backup | SL 1–4 | DETERMINISTIC | Backup of control system configurations; backup tested |
| SR 7.4 | Control system recovery and reconstitution | SL 1–4 | PARAMETERIZED | Recovery time objectives defined; tested |
| SR 7.5 | Emergency power | SL 1–4 | DETERMINISTIC | Backup power for critical IACS components |
| SR 7.6 | Network and security configuration settings | SL 1–4 | DETERMINISTIC | Configuration baseline documented; changes controlled |
| SR 7.7 | Least functionality | SL 1–4 | DETERMINISTIC | Disable/remove unused ports, protocols, services |
| SR 7.8 | Control system component inventory | SL 1–4 | DETERMINISTIC | Inventory of all IACS components maintained |

---

## Zone and conduit model (62443-3-2) — the architectural foundation

Before any system-level test, the IACS must be partitioned into **Security Zones** and **Conduits**:
- **Zone:** A grouping of logical or physical assets sharing common security requirements
- **Conduit:** A communication channel between zones; inherits the higher SL of the two connected zones

SL-T for each zone is determined by risk assessment (62443-3-2). Tests verify SL-A ≥ SL-T.

Zone/conduit boundary definition is PARAMETERIZED. Test results are DETERMINISTIC once boundaries are defined.

---

## 62443-2-3 — Patch Management for IACS

| Requirement | Confidence | Notes |
|---|---|---|
| Patch management policy exists | DETERMINISTIC | Written policy required |
| All applicable patches inventoried | DETERMINISTIC | Asset inventory drives patch applicability |
| Patches assessed for IACS applicability | PARAMETERIZED | Impact on operational continuity assessed before applying |
| Patch deployment cadence | PARAMETERIZED | No bright-line timeline (unlike IT frameworks); cadence is risk-based; OT patching windows often annual |
| Compensating controls documented where patching deferred | PARAMETERIZED | Compensating control adequacy |

---

## NERC CIP relationship

NERC CIP (in this registry at `nerc/cip/`) is a mandatory, sector-specific implementation of IACS security for the North American bulk electric system. It shares conceptual roots with IEC 62443 but differs in structure:

| Dimension | NERC CIP | IEC 62443 |
|---|---|---|
| Mandatory? | Yes (regulatory) | No (voluntary/contractual) |
| Sector | Electric utility only | All industrial sectors |
| Risk levels | High/Medium/Low (impact-based) | SL 1–4 |
| Zone model | ESP/PSP | Zone/conduit |
| Patch cadence | 35 days (with TFE) | Risk-based |
| Source | FERC/NERC | IEC TC65 |

For electric utilities, NERC CIP is the binding requirement. IEC 62443 provides deeper technical guidance and is used as a reference for non-BES OT systems.

---

## Open assumption registry

*(No assumptions recorded — individual part files not yet written)*

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Zone/network architecture | IEC 62443-3-2, NERC CIP (ESP/PSP), NIST 800-82 (ICS security guide) | Zone boundaries and firewall rules are the shared artifact; different terminology |
| Patch management policy | IEC 62443-2-3, NERC CIP CIP-007-6, NIST 800-53 SI-2 | OT patch cadence is risk-based (unlike IT frameworks); compensating controls documented for deferred patches |
| Asset inventory | IEC 62443 SR 7.8, NERC CIP CIP-002 (BES Cyber System), NIST 800-53 CM-8 | Same inventory; NERC CIP adds impact classification |
| Account management | IEC 62443 SR 1.3, NERC CIP CIP-004/CIP-007, NIST 800-53 AC-2 | Same IAM records |
| Backup and recovery | IEC 62443 SR 7.3–7.4, NERC CIP CIP-009, NIST 800-53 CP | Same backup records; NERC CIP adds restoration testing cadence |
| Security configuration baseline | IEC 62443 SR 7.6, NERC CIP CIP-010, NIST 800-53 CM-6 | Same baseline artifact; different naming |
