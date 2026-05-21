# NIST SP 800-82 r3 — Guide to OT Security

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Operational Technology (OT) security — Industrial Control Systems (ICS), SCADA, DCS, PLCs, RTUs, and associated networks across all sectors; not a compliance mandate but primary reference document for OT security programs; referenced by TSA directives, NERC CIP, NRC guidance, and CISA advisories
**Authority:** NIST (National Institute of Standards and Technology); guidance document — not a regulation
**Current edition:** SP 800-82 Revision 3 (September 2023)
**Relationship to 800-53:** SP 800-82 provides OT-specific overlays and tailoring guidance for NIST SP 800-53 controls; the two documents are used together

---

## Summary

| Metric | Count |
|---|---|
| OT system types covered | 6 (ICS/SCADA/DCS/PLC/RTU/Safety Instrumented Systems) |
| Control tailoring categories | 3 (Applies directly / Tailored / Not applicable to OT) |
| SP 800-53 families with OT tailoring | 20 |
| Sections parsed (individual files) | 1 (ot-ics-security-program.md — program elements, zone architecture, remote access, change management, vulnerability management, OT IRP) |
| Fully automated (DETERMINISTIC) | Low — SP 800-82 is guidance, not bright-line requirements; DETERMINISTIC subset: asset inventory existence, architecture documentation, remote access MFA, IRP existence |
| Partial automation (PARAMETERIZED) | Dominant |
| Human-determination required (CONTESTED) | High — OT-specific risk acceptance decisions |
| Open assumptions | 2 |

---

## Note on regulatory status

SP 800-82 is **guidance**, not a regulation. It becomes effectively mandatory when:
- Cited by a binding directive (TSA SD-02D, NRC RG 5.71, CISA advisories)
- Required by contract (DoD procurement, critical infrastructure programs)
- Adopted as policy by the organization

For test purposes, SP 800-82 requirements are PARAMETERIZED assumptions unless a binding mandate references them.

---

## OT vs. IT security — key differences documented in SP 800-82

| Dimension | IT Priority | OT Priority | Test implication |
|---|---|---|---|
| Primary concern | Confidentiality → Integrity → Availability | Availability → Integrity → Confidentiality | CIA triad is inverted — test ordering differs |
| Patch application | Rapid patching | Tested, scheduled, vendor-coordinated patching | Patch timelines are longer and PARAMETERIZED |
| System uptime | High availability desired | Continuous operation often mandatory | Downtime for patching may be unacceptable |
| Testing/scanning | Active scanning routine | Active scanning may disrupt OT devices | Test methodology must account for fragility |

---

## OT architecture reference model (per SP 800-82 §3)

SP 800-82 uses a zone-based model aligned with IEC 62443 Purdue levels:

| Level | Zone | Examples |
|---|---|---|
| Level 4-5 | Enterprise Zone | Business IT, ERP, internet-facing |
| Level 3 | Operations Zone / DMZ | Historian, data aggregation, patch servers |
| Level 2 | Supervisory Zone | SCADA/HMI workstations, engineering stations |
| Level 1 | Control Zone | PLCs, DCS controllers |
| Level 0 | Field Zone | Sensors, actuators |

---

## SP 800-53 tailoring for OT — selected controls

SP 800-82 r3 provides tailoring guidance for applying SP 800-53 Rev 5 to OT. Key tailoring decisions:

### Controls that apply directly (DETERMINISTIC when mandated)

| Control | OT application |
|---|---|
| AC-2 Account Management | OT system accounts managed separately from IT; shared accounts documented |
| AC-17 Remote Access | Remote access to OT requires documented approval, MFA, monitored sessions |
| CM-6 Configuration Settings | Baseline configurations for PLCs/DCS/RTUs documented and enforced |
| IR-6 Incident Reporting | OT incidents reported per sector-specific requirements (NERC CIP, TSA, NRC) |
| PE-3 Physical Access Control | Physical access to control rooms and OT components controlled |
| SI-2 Flaw Remediation | Patches applied per vendor guidance and operational windows |

### Controls tailored for OT (PARAMETERIZED)

| Control | OT tailoring |
|---|---|
| CA-7 Continuous Monitoring | Active scanning may be replaced with passive monitoring for fragile devices |
| RA-5 Vulnerability Scanning | Scanning windows during maintenance; vendor-specific tools required |
| SA-10 Developer Configuration Management | SOUP/COTS component tracking for embedded software |
| SC-7 Boundary Protection | Data diodes, firewalls, and protocol breaks at zone boundaries |

### Controls not applicable or significantly modified for OT

| Control | Reason |
|---|---|
| AC-14 Permitted Actions Without ID | Some OT devices cannot support authentication |
| SC-10 Network Disconnect | Automatic disconnect may cause safety hazards |
| SI-16 Memory Protection | Legacy OT devices lack OS-level memory protection |

---

## OT-specific program requirements (PARAMETERIZED)

| Requirement | Description |
|---|---|
| OT asset inventory | Separate from IT; includes firmware versions, communication protocols |
| Network architecture documentation | Zone diagrams; data flow documentation; firewall rule sets |
| Vendor/integrator management | OT vendor access controls; remote access agreements |
| OT incident response plan | Separate or OT-specific annex to corporate IRP |
| Industrial protocol awareness | Modbus, DNP3, PROFINET, EtherNet/IP — protocol-specific security |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| OT zone architecture | NIST SP 800-82, IEC 62443, NERC CIP-005, TSA SD-02D, NRC 10 CFR 73.54 | SP 800-82 is the reference; others mandate specific zone isolation |
| OT asset inventory | NIST SP 800-82, NERC CIP-002, TSA SD-02D | Same registry; different criticality classification methods |
| Vulnerability management | NIST SP 800-82, NERC CIP-007, TSA SD-02D | SP 800-82 guidance on OT-safe scanning techniques |
| Remote access controls | NIST SP 800-82, NERC CIP-005 R2, TSA SD-02D Goal 2 | Same MFA + session monitoring requirements |
| Incident response | NIST SP 800-82, CISA advisories, NERC CIP-008, NRC 10 CFR 73.77 | IRP with OT-specific runbooks |
