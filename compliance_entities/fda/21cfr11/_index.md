# FDA 21 CFR Part 11 — Electronic Records and Electronic Signatures

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** 21 CFR Part 11 (Subparts A–C); electronic records in closed and open systems; electronic signatures and handwritten signatures executed to electronic records
**Authority:** U.S. Food and Drug Administration (FDA) / CDER, CBER, CDRH
**Enforcing context:** Pharmaceutical, biotech, medical device manufacturers; clinical research organizations; any FDA-regulated industry using electronic records in place of paper records required by FDA regulations (21 CFR Parts 58, 210, 211, 820, etc.)
**Current version:** Final rule 21 CFR Part 11 (1997); 2003 Guidance for Industry reduces enforcement scope for predicate rule records

---

## Summary

| Metric | Count |
|---|---|
| Subparts | 3 (A: General; B: Electronic Records; C: Electronic Signatures) |
| Sections (regulatory requirements) | ~15 |
| Requirements parsed (individual files) | 2 (electronic-records-esig.md — §11.10(b-k), §11.50, §11.70, §11.100, §11.200, §11.300; system-validation.md — §11.10(a)(f)(i)(j), §11.30) |
| Fully automated (DETERMINISTIC) | High — 21 CFR Part 11 is among the most DETERMINISTIC frameworks in this registry |
| Partial automation (PARAMETERIZED) | Moderate (system validation scope; training adequacy) |
| Human-determination required (CONTESTED) | Low (Part 11 scope determination itself is the main CONTESTED area) |
| Unresolvable | Minimal |
| Open assumptions | 13 (ASSUME-21CFR11-001–013) |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Scope determination — critical pre-condition

Part 11 applies only to electronic records that are:
1. **Created, modified, maintained, archived, retrieved, or transmitted** under FDA requirements, AND
2. **Used in lieu of paper records** required by predicate rules (21 CFR 58, 210, 211, 820, etc.)

The 2003 FDA Guidance narrowed enforcement focus to:
- Audit trails (§11.10(e))
- Copy protection (§11.10(b))
- Legacy systems (use risk-based approach)

Predicate rule compliance is the primary obligation; Part 11 is the electronic records overlay.

| Scoping decision | Classification | Notes |
|---|---|---|
| Is this record subject to a predicate rule? | PARAMETERIZED | Regulatory citation mapping required |
| Is this record used in lieu of paper? | DETERMINISTIC | Binary: paper record also maintained (hybrid) vs. paper replaced |
| Is this a closed or open system? | DETERMINISTIC | Network isolation determination |

---

## Per-section confidence map

### Subpart B — Electronic Records

#### §11.10 — Controls for Closed Systems

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| 11.10(a) | System validation | PARAMETERIZED | Validation scope and extent — "appropriate," "consistent with intended use"; GAMP 5 methodology is industry standard assumption |
| 11.10(b) | Accurate and complete copies | DETERMINISTIC | System must produce human-readable and electronic copies on demand; format accuracy is verifiable |
| 11.10(c) | Record protection and archival | DETERMINISTIC | Records must be retrievable throughout retention period; corruption/loss detection required |
| 11.10(d) | Computer access controls | HIGH | Access limited to authorized individuals; unique user ID + password or biometric required |
| 11.10(e) | Audit trail | DETERMINISTIC | Secure, computer-generated, time-stamped audit trail; must record operator ID, date/time, action; cannot be modified or deleted by user; must be retained at least as long as the record itself |
| 11.10(f) | Operational checks | PARAMETERIZED | System checks to enforce sequencing of steps; method not specified |
| 11.10(g) | Authority checks | DETERMINISTIC | System checks user has authority before permitting action; role-based access control is standard implementation |
| 11.10(h) | Device checks | PARAMETERIZED | Input device validity checks; scope of validation |
| 11.10(i) | Personnel qualification | PARAMETERIZED | Training adequacy; documentation of qualifications |
| 11.10(j) | Written policies | PARAMETERIZED | Policy content covering accountability and electronic signature use |
| 11.10(k) | Distribution controls | DETERMINISTIC | Controls ensuring only authorized copies circulate |

#### §11.30 — Controls for Open Systems

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| 11.30 | Open system additional controls | MEDIUM | Includes all §11.10 controls plus: document encryption, digital signatures for records transmitted over open networks |

#### §11.50 — Signature Manifestations

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| 11.50(a) | Signature components displayed | DETERMINISTIC | Electronic signature must display: (1) printed name of signer, (2) date/time signed, (3) meaning of signature (e.g., "approved," "reviewed") |
| 11.50(b) | Signature subject to same controls as records | DETERMINISTIC | Binary: signature stored as part of or linked to the record |

#### §11.70 — Signature/Record Linking

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| 11.70 | Signatures linked to records | DETERMINISTIC | Electronic signatures must be permanently linked to their respective records; link must detect any alteration of either record or signature |

### Subpart C — Electronic Signatures

#### §11.100 — General requirements

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| 11.100(a) | Unique to one individual | DETERMINISTIC | No shared electronic signatures |
| 11.100(b) | Identity verification before first use | DETERMINISTIC | Organization must verify identity before issuing electronic signature authority |
| 11.100(c) | Certification to FDA (non-biometric) | DETERMINISTIC | One-time certification to FDA that electronic signatures are intended to be the legally binding equivalent of handwritten signatures |

#### §11.200 — Electronic signature components and controls

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| 11.200(a)(1) | Non-biometric signatures: two components | DETERMINISTIC | Must use at least two identification components (e.g., ID + password); both must be used for signing in single continuous session |
| 11.200(a)(2) | Non-biometric signatures: different sessions | DETERMINISTIC | If not a single continuous session, all electronic signature components must be used |
| 11.200(a)(3) | Non-biometric: not re-usable or transferable | DETERMINISTIC | Components cannot be borrowed, stolen, or used by anyone other than their rightful owner |
| 11.200(b) | Biometric signatures | DETERMINISTIC | Biometric signatures must be designed to ensure they cannot be used by any other individual |

#### §11.300 — Controls for identification codes/passwords

| Section | Requirement | Confidence | Notes |
|---|---|---|---|
| 11.300(a) | Unique combination | DETERMINISTIC | Unique ID + password combination; periodic ID/password checks |
| 11.300(b) | Revocation | DETERMINISTIC | Passwords revised at established intervals; lost/stolen tokens recalled |
| 11.300(c) | Deactivation after loss | DETERMINISTIC | Immediately deactivate tokens reported lost, stolen, or compromised |
| 11.300(d) | Transaction safeguards | PARAMETERIZED | Safeguards to prevent unauthorized use; detection and reporting of attempts |
| 11.300(e) | Device checks | PARAMETERIZED | Initial and periodic testing of devices used for generating signatures |

---

## Key DETERMINISTIC checkpoints (reference table)

| Requirement | Bright-line test | Section |
|---|---|---|
| Audit trail existence | Computer-generated, timestamped log exists and is non-alterable | §11.10(e) |
| Audit trail retention | Retained at least as long as the associated record | §11.10(e) |
| Unique user IDs | No shared accounts | §11.10(d), §11.100(a) |
| Signature components | Must display: name, date/time, meaning | §11.50(a) |
| Two-component signature | Non-biometric esig requires two components | §11.200(a)(1) |
| Signature/record link | Alteration of either invalidates the link | §11.70 |
| FDA certification | One-time written certification submitted to FDA | §11.100(c) |
| Identity verification | Identity verified before first esig use | §11.100(b) |

---

## System validation — the central PARAMETERIZED obligation

§11.10(a) requires validation "to ensure accuracy, reliability, consistent intended performance, and the ability to discern invalid or altered records." No specific validation methodology is mandated. Industry standard is **GAMP 5** (Good Automated Manufacturing Practice):

| GAMP 5 Category | System type | Validation scope |
|---|---|---|
| Category 1 | Infrastructure software (OS, middleware) | Installation Qualification (IQ) only |
| Category 3 | Non-configured software (e.g., Excel) | IQ + Operational Qualification (OQ) |
| Category 4 | Configured software (e.g., LIMS, ERP) | IQ + OQ + Performance Qualification (PQ) |
| Category 5 | Custom software | Full lifecycle validation; source code review |

GAMP 5 category assignment and validation extent are documented as assumptions and tested via Pattern 2.

---

## Open assumption registry

| ID | Section | Summary | Review date |
|---|---|---|---|
| ASSUME-21CFR11-001 | §11.10(e) | Audit trail: every create/modify/delete; non-alterable; operator ID + timestamp + old value; retained with record; FDA-inspectable export | 2026-05-20 |
| ASSUME-21CFR11-002 | §11.10(d) | Access controls: unique user IDs; role-based; terminated = disabled within 24h; annual review | 2026-05-20 |
| ASSUME-21CFR11-003 | §11.10(b)+(c) | Record copies: human-readable and electronic on demand; archival integrity; retrievable throughout retention; checksum/hash verification | 2026-05-20 |
| ASSUME-21CFR11-004 | §11.50 | Signature manifestations: full name + date/time + meaning from controlled vocabulary; on every human-readable rendering | 2026-05-20 |
| ASSUME-21CFR11-005 | §11.70 | Signature/record link: permanent; alteration detectable; cannot be excised; hash or DB reference to specific record version | 2026-05-20 |
| ASSUME-21CFR11-006 | §11.100 | Uniqueness + FDA cert: unique IDs not reused; identity verified at hire; §11.100(c) certification submitted to FDA and on file | 2026-05-20 |
| ASSUME-21CFR11-007 | §11.200 | Two-component: user ID + password; first signing = both components; session break resets to both; biometric = individual-only | 2026-05-20 |
| ASSUME-21CFR11-008 | §11.300 | Password/token: lockout ≤10 attempts; failed attempts alerted; lost/stolen deactivated within 4h; periodic checks; password history | 2026-05-20 |
| ASSUME-21CFR11-009 | §11.10(a) | GAMP 5: category assigned; IQ/OQ/PQ per category; impact assessment on changes; revalidation when required; packages retained | 2026-05-20 |
| ASSUME-21CFR11-010 | §11.10(f) | Operational checks: critical sequences enforced; risk justification if not; verified in OQ/PQ | 2026-05-20 |
| ASSUME-21CFR11-011 | §11.10(i) | Personnel qualification: role-specific training before access; covers esig meaning and record protection; records retained | 2026-05-20 |
| ASSUME-21CFR11-012 | §11.10(j) | Written policies: Part 11 policy covering 5 required sections; reviewed annually; personnel annual acknowledgment; version-controlled | 2026-05-20 |
| ASSUME-21CFR11-013 | §11.30 | Open systems: all §11.10 controls + TLS 1.2+ in transit; digital signature standard QA/RA-reviewed; transmission path in validation scope | 2026-05-20 |

---

## Contested items pending resolution

| Item | Section | Reason | Resolution path |
|---|---|---|---|
| Part 11 scope determination | §11.10 | Which records are "used in lieu of paper" — hybrid paper+electronic records are partially out of scope; determination requires predicate rule citation mapping | QA/RA determination per system; predicate rule citation table maintained |
| System validation scope ("appropriate") | §11.10(a) | What level of validation is "appropriate" for a given system/risk level — 2003 Guidance allows risk-based approach but does not define bright-line thresholds | QA/RA-led validation risk assessment; Pattern 3 for scope borderline cases |
| §11.30 "appropriate digital signature standard" | §11.30 | No specific digital signature standard named in regulation; X.509/PKI, S/MIME, or other mechanisms may be appropriate depending on context | QA/RA review and attestation; industry guidance (ICH Q9) | 

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Audit trail / logging | 21 CFR Part 11 §11.10(e), HIPAA §164.312(b), SOC 2 CC7, PCI DSS Req 10 | 21 CFR Part 11 has the strictest non-alterability requirement; design audit trail to Part 11 and all others are satisfied |
| Access control / unique IDs | 21 CFR Part 11 §11.10(d), HIPAA §164.312(a)(2)(i), PCI DSS Req 8.2.1 | All three require unique user IDs; no shared accounts. Identical DETERMINISTIC test |
| System validation documentation | 21 CFR Part 11 §11.10(a), ISO 27001 A.8.25 (secure development), SOC 2 CC8 (change management) | Validation documentation satisfies all three if it covers IQ/OQ/PQ and change control |
| Electronic signature policies | 21 CFR Part 11 §11.10(j), ISO 27001 A.5.14 (data in transit) | Signature policy documents the intent of esig as equivalent to handwritten; distinct from data-in-transit policy but can share the same policy framework |
| Record retention | 21 CFR Part 11 §11.10(c), HIPAA §164.316(b)(2) (6 years), PCI DSS Req 10 (12 months for logs) | Record retention per predicate rule; §11.10(c) requires retrievability throughout retention. Retain to the most restrictive applicable predicate rule period |

---

## CI/CD gate configuration

Standard three-tier gate (see NERC CIP registry). 21 CFR Part 11-specific constraints:

- **Scope fixture:** All tests gated by `record_subject_to_predicate_rule()` — mapping between records and regulatory citations is a required pre-condition.
- **Audit trail integrity check (Pattern 1):** Non-alterable log verified by computing hash of audit log table; any unexplained delta triggers immediate failure.
- **Validation status (Pattern 2):** Each system must have a current validation package. Validation packages older than the last significant change trigger Pattern 2 failure.
- **FDA certification tracker (Pattern 1):** One-time §11.100(c) certification must be on file; absence is a DETERMINISTIC failure.
- **esig configuration (Pattern 1):** Two-component signature enforcement is a system configuration check; binary DETERMINISTIC test.

---

## Specification file status

| File | Contents | Assumptions | Confidence | Status |
|---|---|---|---|---|
| `electronic-records-esig.md` | §11.10(b)(c)(d)(e): record copies, archival, access controls, audit trail; §11.50 signature manifestations; §11.70 sig/record linking; §11.100 uniqueness + FDA cert; §11.200 two-component; §11.300 password/token | ASSUME-21CFR11-001–008 | HIGH | ✅ Parsed |
| `system-validation.md` | §11.10(a) system validation (GAMP 5); §11.10(f)(i)(j) operational/training/policy; §11.30 open systems | ASSUME-21CFR11-009–013 | MEDIUM | ✅ Parsed |
| *(§11.10(g)+(k))* | Authority checks and distribution controls | TBD | HIGH | 🔲 Pending |

---

## Remaining parse priority

| Priority | Section | Notes |
|---|---|---|
| 1 | §11.10(g) | Authority checks before permitting operations — DETERMINISTIC; role-based permission check |
| 2 | §11.10(k) | Distribution controls for system documentation — DETERMINISTIC for access control |
| 3 | §11.10(h) | Device checks — PARAMETERIZED; input device validation scope |
