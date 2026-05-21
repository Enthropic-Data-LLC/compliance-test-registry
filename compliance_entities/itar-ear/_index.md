# ITAR / EAR — U.S. Export Control Regulations

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** ITAR (22 CFR Parts 120–130) and EAR (15 CFR Parts 730–774)
**Authorities:** U.S. Department of State / DDTC (ITAR); U.S. Department of Commerce / BIS (EAR)
**Enforcing context:** All U.S. persons and companies exporting or re-exporting defense articles, defense services, dual-use items, or related technology; deemed exports (foreign national access); cloud services hosting controlled data

---

## Summary

| Metric | Count |
|---|---|
| Regulatory bodies | 2 (DDTC + BIS) |
| Control lists | 2 (USML + CCL/ECCN) |
| Compliance domains parsed (individual files) | 2 (deterministic-controls.md — screening, record-keeping, registration; parameterized-controls.md — license req., deemed export, TCP, training) |
| Fully automated (DETERMINISTIC) | Low — classification and licensing are inherently PARAMETERIZED/CONTESTED |
| Partial automation (PARAMETERIZED) | Dominant mode |
| Human-determination required (CONTESTED) | Significant (classification, licensing, deemed export scope) |
| Unresolvable | Minimal (case-specific regulatory guidance resolves most edge cases) |
| Open assumptions | 7 (ASSUME-ITAR-001–007) |
| Stale reviews | 0 |
| Pending external escalations | 0 |

---

## Regulatory architecture

### ITAR — International Traffic in Arms Regulations (22 CFR 120–130)

Controls **defense articles** (items on the U.S. Munitions List — USML) and **defense services**.

| Part | Subject | Confidence projection |
|---|---|---|
| 120 | Definitions; purpose | PARAMETERIZED — "defense article," "defense service," "U.S. person" definitions have edge cases |
| 121 | USML — the control list | PARAMETERIZED — USML categories I–XXI; catch-all Category XXI is CONTESTED |
| 122 | Registration of manufacturers/exporters | DETERMINISTIC — binary registration status |
| 123 | Export licenses (defense articles) | PARAMETERIZED — license requirement is DETERMINISTIC per classification; license sufficiency is CONTESTED |
| 124 | Manufacturing licenses and technical assistance agreements | CONTESTED — scope of "defense services" rendered under agreements |
| 125 | Export licenses (technical data + software) | PARAMETERIZED — "export" of data includes deemed export; "publicly available" exemption is PARAMETERIZED |
| 126 | General policies; exemptions | PARAMETERIZED — 126.3 (emergency exemption), 126.4 (for U.S. government) have bounded scope |
| 127 | Violations; penalties | DETERMINISTIC — penalties are statutory |
| 129 | Brokering | PARAMETERIZED — "brokering activities" definition has edge cases |
| 130 | Political contributions and fees | DETERMINISTIC — disclosure thresholds are stated |

### EAR — Export Administration Regulations (15 CFR 730–774)

Controls **dual-use items** on the Commerce Control List (CCL) by ECCN (Export Control Classification Number).

| Part | Subject | Confidence projection |
|---|---|---|
| 730 | General information | Informational |
| 734 | Scope; jurisdiction determination | CONTESTED — EAR/ITAR jurisdiction line (especially for software and technology) is frequently contested |
| 736 | General prohibitions | DETERMINISTIC — 10 general prohibitions are enumerable |
| 738 | CCL overview | Informational |
| 740 | License exceptions | PARAMETERIZED — exception eligibility is condition-based (e.g., ENC for encryption items) |
| 742 | Control policy / licensing requirements | PARAMETERIZED — reason-for-control + destination + end-use + end-user matrix |
| 744 | End-user and end-use controls | CONTESTED — "knows or has reason to know" standard; red-flag list application |
| 746 | Embargoes | DETERMINISTIC — embargoed destinations are enumerable lists |
| 748 | Applications for licenses | PARAMETERIZED — license application content requirements |
| 750 | License reviews | CONTESTED — BIS review factors are policy-based |
| 762 | Record-keeping | DETERMINISTIC — 5-year retention period is bright-line |
| 764 | Violations and penalties | DETERMINISTIC — statutory penalty schedule |
| 772 | Definitions | PARAMETERIZED — "export," "technology," "software" have contested edge cases |
| 774 | CCL / ECCN schedule | PARAMETERIZED — ECCN assignment requires technical review |

---

## Compliance test domains

Unlike standards-based frameworks, ITAR/EAR compliance is organized around decision points rather than numbered requirements. Each domain below corresponds to a class of compliance test.

| Domain | Description | Confidence | Primary test type |
|---|---|---|---|
| **Item classification** | Is the item on the USML or CCL/ECCN? | PARAMETERIZED / CONTESTED | Human-determination gate (Pattern 3) — classification must be attested by a qualified expert and documented in a Commodity Jurisdiction (CJ) or self-classification record |
| **Jurisdiction determination** | Is this item subject to ITAR or EAR? | CONTESTED | Pattern 3 — EAR/ITAR line disputes are common; CJ request from DDTC resolves |
| **License requirement** | Does this transaction require a license or does a license exception apply? | PARAMETERIZED | Pattern 2 — license matrix (item + destination + end-use + end-user) is rule-based but requires classification as input |
| **Denied parties screening** | Is any party to the transaction on a restricted party list (SDN, DPL, Entity List, etc.)? | DETERMINISTIC | Pattern 1 — binary lookup against official government lists; API-based automated check is achievable |
| **Deemed export** | Does disclosure of controlled technology to a foreign national in the U.S. constitute an export? | PARAMETERIZED | Pattern 2 — nationality + item ECCN/USML category matrix; "publicly available" exception is PARAMETERIZED |
| **Record-keeping** | Are required records maintained for the statutory retention period? | DETERMINISTIC | Pattern 1 — 5-year retention (EAR §762); 5-year retention (ITAR §122.5) |
| **Registration status** | Is the entity registered with DDTC (ITAR §122)? | DETERMINISTIC | Pattern 1 — active registration status check |
| **License validity** | Is a required license current, applicable to this transaction, and within authorized quantities/dates? | PARAMETERIZED | Pattern 2 — license scope review |
| **Technology control plan (TCP)** | Is a TCP in place and current for facilities with ITAR/EAR obligations? | PARAMETERIZED | Pattern 2 — plan existence is DETERMINISTIC; adequacy is PARAMETERIZED |
| **Training records** | Do personnel with export responsibilities have current training documentation? | PARAMETERIZED | Pattern 2 — completion is DETERMINISTIC; content adequacy is PARAMETERIZED |

---

## Critical ambiguity: the EAR/ITAR jurisdiction line

The single most CONTESTED determination in U.S. export control is whether an item is subject to ITAR or EAR. This boundary:

- Depends on item design intent, not just function
- Is adjudicated by DDTC via Commodity Jurisdiction (CJ) requests — the only binding determination
- Cannot be automated; must be a named-expert determination with documented rationale and periodic review

All downstream compliance tests (license requirement, deemed export, etc.) depend on this determination. **The jurisdiction classification is the root fixture for all ITAR/EAR tests.**

---

## Denied party screening — the primary DETERMINISTIC automation target

This domain is the most amenable to full Pattern 1 automation:

| List | Authority | Check method |
|---|---|---|
| Specially Designated Nationals (SDN) | Treasury / OFAC | OFAC SDN API |
| Denied Persons List (DPL) | BIS / Commerce | BIS consolidated screening tool |
| Entity List | BIS / Commerce | BIS consolidated screening tool |
| Unverified List | BIS / Commerce | BIS consolidated screening tool |
| Debarred List | DDTC / State | DDTC debarred list |
| Nonproliferation Sanctions | State | Multiple State Dept. lists |

A single consolidated screening API call at transaction time satisfies all six lists.

---

## Open assumption registry

| ID | Domain | Summary | Review date |
|---|---|---|---|
| ASSUME-ITAR-001 | Denied party screening | CSL checked within 24h; screening before transaction; fuzzy name matching; confirmed matches halt transaction; screening log retained 5 years | 2026-05-20 |
| ASSUME-ITAR-002 | Record-keeping | All record types maintained; 5-year retention from latest trigger; electronic format acceptable; destruction schedule enforced | 2026-05-20 |
| ASSUME-ITAR-003 | DDTC registration | Active registration; expiration current; renewal ≥60 days in advance; material changes reported within 60 days | 2026-05-20 |
| ASSUME-ITAR-004 | License requirement | Determination per ECCN + destination + end-use + end-user; NLR affirmative; exception symbol and eligibility documented | 2026-05-20 |
| ASSUME-ITAR-005 | Deemed export | Foreign national log; visa type considered (LPR = U.S. person for EAR); license, exception, or TCP restriction per access; records 5 years | 2026-05-20 |
| ASSUME-ITAR-006 | Technology control plan | TCP current (≤12 months); all required elements; custodian designated; ECO annual adequacy attestation | 2026-05-20 |
| ASSUME-ITAR-007 | Training | Initial + annual for all export personnel; covers classification, licensing, screening, deemed export; records 5 years | 2026-05-20 |

---

## Contested items pending resolution

| Item | Domain | Reason | Resolution path |
|---|---|---|---|
| EAR/ITAR jurisdiction determination | Jurisdiction | EAR/ITAR line for ITAR-pedigree items modified for commercial use is the most frequently contested determination in export control | CJ request to DDTC; Pattern 3 gate in place until resolved |
| "Publicly available" exception scope | EAR §734.7 / ITAR §125.4 | Whether open-source software with encryption components qualifies for publicly available exception — BIS advisory opinions vary | BIS advisory opinion; export counsel determination; Pattern 3 gate |
| TCP access control adequacy | TCP | Whether physical and electronic controls described in a TCP are "sufficient" — no objective threshold; ECO-evaluated | ECO annual attestation; Pattern 3 gate |
| Deemed export — dual nationals | Deemed export | U.S. dual national LPR: treated as U.S. person for EAR; ITAR rule is different (focuses on foreign citizenship regardless of LPR status) — the delta creates compliance complexity | Export counsel determination per ITAR §120.15 and per-employee analysis |
| License application review outcome | BIS §750 review | Whether a submitted license application will be approved is a policy-based BIS determination — not predictable | BIS license review; Pattern 3 holding state during review |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Technology control plan (TCP) | ITAR, EAR, CMMC (for CUI involving controlled technology) | TCP is the primary access control document for export-controlled technology; overlaps with CMMC physical/access controls |
| Denied party screening | ITAR, EAR, OFAC sanctions | Same underlying data sources; recommend single screening service shared across all three |
| Training records | ITAR, EAR, CMMC AT domain | Export control training records can be co-maintained with CMMC/800-171 awareness training records |
| Record-keeping | ITAR §122.5, EAR §762, CMMC AU | 5-year retention aligns with CMMC audit log requirements |

---

## CI/CD gate configuration

ITAR/EAR does not map cleanly to the standard three-tier gate because the test target is a **transaction** (not a system state). Recommended gate model:

- **Pre-transaction gate:** Denied party screening (Pattern 1) runs automatically against all parties before any controlled technology disclosure or shipment.
- **Classification gate:** Item jurisdiction and classification must have a current, expert-attested determination on file (Pattern 3). Stale determinations (> 1 year or after item modification) block.
- **License gate:** License matrix check (Pattern 2) runs per-transaction using the attested classification. Exceptions must be documented.
- **Post-transaction:** Record created and retained; audit trail satisfies §762 and §122.5 retention requirements.

---

## Specification file status

| File | Contents | Assumptions | Confidence | Status |
|---|---|---|---|---|
| `deterministic-controls.md` | Denied party screening (EAR §744, ITAR §127), record-keeping (EAR §762, ITAR §122.5), DDTC registration (ITAR §122) | ASSUME-ITAR-001–003 | HIGH | ✅ Parsed |
| `parameterized-controls.md` | License requirement (EAR §742, ITAR §123), deemed export (EAR §734, ITAR §125.2), technology control plan, training records | ASSUME-ITAR-004–007 | MEDIUM | ✅ Parsed |
| *(Item classification — ECCN)* | EAR ECCN self-classification workflow; CCL review; ECCN validity testing | TBD | PARAMETERIZED | 🔲 Pending |
| *(Item classification — USML)* | ITAR USML category testing; CJ request workflow; USML vs. CCL jurisdiction gate | TBD | CONTESTED | 🔲 Pending |

---

## Remaining parse priority

| Priority | Domain | Notes |
|---|---|---|
| 1 | ECCN item classification workflow | PARAMETERIZED; required as input for license matrix; requires technical review procedure |
| 2 | USML classification + CJ workflow | CONTESTED; root fixture for all ITAR tests; CJ request integration |
| 3 | Jurisdiction determination (EAR vs. ITAR) | CONTESTED; highest complexity; last to parse after classification workflow established |
