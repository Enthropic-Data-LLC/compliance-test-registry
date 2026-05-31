# Compliance Test Case Registry

**Maintainer:** Enthropic LLC — [enthropicdata.com](https://www.enthropicdata.com)
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0) — see [License](#license)
**Status:** Active development — contributions welcome

---

## Disclaimer

> **This registry is provided for informational and educational purposes only. It does not constitute legal advice, regulatory guidance, or a compliance determination of any kind. Nothing in this repository should be relied upon as a substitute for advice from qualified legal counsel, a licensed compliance professional, or an accredited third-party assessor with expertise in the applicable regulation.**
>
> **Accuracy and currency:** Regulations, standards, and enforcement interpretations change. Content in this registry reflects the state of each framework as of its `Last updated` date. The maintainers make no warranty, express or implied, that the content is accurate, complete, or current at the time of your use. You are solely responsible for verifying the applicability and accuracy of any test case, assumption, or interpretation against the authoritative primary source before relying on it.
>
> **No warranty of compliance:** Use of this registry does not guarantee, imply, or establish compliance with any regulation. Passing a test case in this registry does not constitute evidence of regulatory compliance. Compliance determinations require assessment by qualified personnel against the specific facts, systems, and circumstances of your organization.
>
> **AI-assisted content:** Portions of this registry were developed with the assistance of large language model (LLM) AI tools, including Claude (Anthropic), for initial element extraction, ambiguity classification drafts, and test code scaffolding. All AI-generated content was reviewed against primary regulatory source text before inclusion. However, AI tools can and do produce errors, misclassifications, and outdated interpretations. Do not use any content in this registry for compliance purposes without independent human review by a qualified professional.
>
> **Jurisdiction and applicability:** Regulatory requirements vary by jurisdiction, organization type, system scope, contract terms, and applicable law. A requirement classified as DETERMINISTIC in this registry may be PARAMETERIZED or CONTESTED in your specific context. The maintainers assume no liability for compliance failures, regulatory penalties, audit findings, or any other harm arising from use of this registry.
>
> **Use at your own risk.** By using this registry you acknowledge that you have read this disclaimer and agree that Enthropic LLC and its contributors bear no responsibility for any consequences of your reliance on its contents.

---

## What This Is

This repository is a structured, version-controlled library of regulatory compliance test cases built using the **Regulatory Decomposition Framework (RDF)** — a methodology for translating natural language regulations into deterministic, auditable, executable specifications.

Every regulation in this registry has been passed through a four-stage process: parsed into its four extractable elements (Subject, Condition, Obligation, Evidence), classified by ambiguity tier, expressed as a YAML specification, and implemented as a Python test case. The result is a compliance library where every requirement has a known confidence level, every assumption is documented and signed, and every audit response can be generated directly from the version history.

This is not a policy template library. It is an engineering artifact — designed to be executed, not read.

---

## Why We Built This

Compliance work has a structural problem: it lives in Word documents and spreadsheets that rot the moment the regulation changes or the person who wrote them leaves. Controls get checked manually on a schedule that no one follows. Audits produce point-in-time snapshots that are obsolete before the ink dries.

The premise here is that **every regulation can be treated like a software requirement** — broken down, tested automatically, and tracked in version control. The parts that cannot be automated are not glossed over; they are surfaced explicitly as human-determination requirements with documented assumptions, assigned reviewers, and expiry dates.

The specific problem that prompted this work was preparing compliance posture documentation for an internal GRC platform targeting CMMC 2.0, NIST 800-171, and ITAR. As we decomposed those frameworks we realized: (1) the methodology was framework-agnostic, and (2) no publicly available library did this at the precision level we needed. So we built it in the open.

### Foundational design decisions

**Ambiguity is a first-class object.** Most compliance tools hide interpretive uncertainty inside a checkbox. This registry surfaces it explicitly. A PARAMETERIZED test documents what assumption was made, by whom, when, and when it needs to be re-approved. A CONTESTED test refuses to make the determination at all — it only verifies that a qualified human has done so recently.

**Confidence levels are honest.** Every test file states its confidence level at the top. A HIGH confidence test passes or fails based on data. A MEDIUM confidence test passes or fails based on data *given a documented assumption*. A LOW confidence test passes or fails based on whether a human determination exists and is current — it does not determine compliance itself.

**The test suite is the audit trail.** When a regulator asks for evidence, the answer is a git commit hash, a test run timestamp, and the specific assertion that passed. No interpretation required.

**Assumptions have owners and expiry dates.** Every PARAMETERIZED assumption has an `approved_by`, a `date`, and a `review_frequency_days`. The CI pipeline treats stale assumptions as failures. The assumption registry in each `_index.md` is the single source of truth for what human decisions are load-bearing in the test suite.

---

## Start Here: A NERC CIP Example End-to-End

NERC CIP is the most mature part of this registry — 14 standard files, fully DETERMINISTIC across all requirements, and the framework most likely to be familiar to readers from the energy sector. Walking through one requirement end-to-end shows exactly what the registry produces.

**Requirement:** CIP-002-5.1a R2 — every Responsible Entity must review its BES Cyber System categorization and obtain CIP Senior Manager approval at least once every 15 calendar months.

### Step 1: Source text

> *"The Responsible Entity shall: (R2.1) Review the identifications in Requirement R1 and its parts at least once every 15 calendar months, even if it has no identified items in Requirement R1; and (R2.2) Have its CIP Senior Manager or delegate approve the identifications required by Requirement R1 at least once every 15 calendar months."*

### Step 2: Four-element extraction

| Element | Extracted value | Classification |
|---|---|---|
| Subject | Responsible Entity's R1 categorization record | DETERMINISTIC |
| Condition | Elapsed time since last review/approval | DETERMINISTIC |
| Obligation | `days_since_last_review ≤ 457` AND approved by CIP Senior Manager or delegate | DETERMINISTIC |
| Evidence | `categorization_review.last_reviewed_at`, `.approved_by_role`, `.signature_hash` | DETERMINISTIC |

Every element resolves to a bright-line value. No "reasonable," no "adequate," no "as necessary." This makes CIP-002 R2 a textbook Pattern 1 test.

### Step 3: YAML specification

```yaml
regulation_id: CIP-002-R2
revision: 5.1a
source_text: >
  Review the identifications in R1 at least once every 15 calendar months,
  and have the CIP Senior Manager or delegate approve them at the same cadence.
extracted_elements:
  subject: "R1 categorization record"
  condition: "days_since_last_review > 457 OR approval missing"
  obligation: "days_since_last_review <= 457 AND approved_by_cip_senior_manager == true"
  evidence: "categorization_review.last_reviewed_at, .approved_by_role, .signature_hash"
ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC
overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log: []
test_confidence: HIGH
generated_test: "tests/CIP-002/test_R2.py"
```

### Step 4: Generated test (Pattern 1 — Direct Assertion)

```python
"""
CIP-002-5.1a R2 — Annual Review and Approval
Confidence: HIGH | Human Review: NOT REQUIRED
"""
from datetime import datetime, timedelta

REVIEW_WINDOW_DAYS = 457  # 15 calendar months (15 × 30.44 ≈ 457)


def test_CIP002_R2_1_review_cadence(categorization_review):
    """R2.1: R1 identifications reviewed within 15 calendar months."""
    age = datetime.utcnow() - categorization_review.last_reviewed_at
    assert age <= timedelta(days=REVIEW_WINDOW_DAYS), (
        f"VIOLATION: Categorization review is {age.days} days old. "
        f"Threshold: {REVIEW_WINDOW_DAYS} days. "
        f"Last reviewed: {categorization_review.last_reviewed_at.isoformat()}"
    )


def test_CIP002_R2_2_senior_manager_approval(categorization_review):
    """R2.2: Approval by CIP Senior Manager or named delegate."""
    assert categorization_review.approved_by_role in (
        "CIP Senior Manager",
        "CIP Senior Manager Delegate",
    ), (
        f"VIOLATION: Approved by '{categorization_review.approved_by_role}' — "
        f"not an authorized role."
    )
    assert categorization_review.signature_hash, (
        "INTEGRITY FAILURE: Approval lacks signature hash."
    )
    age = datetime.utcnow() - categorization_review.approved_at
    assert age <= timedelta(days=REVIEW_WINDOW_DAYS), (
        f"VIOLATION: Approval is {age.days} days old (threshold {REVIEW_WINDOW_DAYS})."
    )
```

### What a SCAFFOLDED entry looks like by comparison

A SCAFFOLDED entry (e.g., TSA Pipeline SD-02D) covers an entire framework in one file. It has the same structure — source text, element extraction, YAML, test code — but as a single document rather than one file per standard. It's a valid starting point; it captures all the DETERMINISTIC content. It is not the same as 14 files where every requirement has been individually extracted, classified, and tested.

The DECOMPOSED label means each standard in the framework has its own file. The SCAFFOLDED label means the whole framework is in one file. Both are useful. Neither is a placeholder.

---

## Repository Structure

```
compliance_test_cases/
│
├── README.md                          ← this file (grand index + methodology)
├── .gitignore
│
├── guiding_docs/
│   ├── regulatory-decomposition-framework.md   ← RDF methodology
│   ├── assumption-registry-template.md         ← PARAMETERIZED assumption schema + workflow
│   ├── cross-framework-dependency-map.md       ← 10 shared artifact clusters (IMS planning)
│   ├── ci-cd-gate-config-reference.md          ← Pattern 1/2/3 gate config + pipeline YAML
│   └── scoping-fixture-catalog.md              ← All is_in_scope() functions; scoping matrix
│
└── compliance_entities/               ← 59 frameworks across 9 sectors
    │
    ├── [CYBERSECURITY & IT SECURITY]
    ├── nerc/cip/                      ← NERC CIP-002–CIP-015 (FULL — 14 standard files)
    ├── nist/sp800-53/                 ← NIST SP 800-53 r5
    ├── nist/sp800-171/                ← NIST SP 800-171 r3
    ├── nist/csf2/                     ← NIST CSF 2.0
    ├── nist/sp800-82/                 ← NIST SP 800-82 r3 (OT/ICS guide)
    ├── nist/ai-rmf/                   ← NIST AI RMF 1.0
    ├── cmmc/                          ← CMMC 2.0 (3 levels)
    ├── iso/27001/                     ← ISO/IEC 27001:2022 (INDEX+SECTIONS — 4 files)
    ├── fedramp/                       ← FedRAMP
    ├── soc2/                          ← SOC 2 (CC1–CC9 + 4 additional)
    ├── iec/62443/                     ← IEC 62443 (OT/ICS)
    ├── tisax/                         ← TISAX / VDA ISA 6.0 (automotive)
    ├── sec/cybersecurity/             ← SEC Cybersecurity Rules 2023
    ├── swift/csp/                     ← SWIFT CSP / CSCF v2025
    ├── tsa/pipeline/                  ← TSA Pipeline SD-02D
    ├── nrc/10cfr73/                   ← NRC 10 CFR 73.54 (nuclear)
    │
    ├── [PRIVACY & DATA PROTECTION]
    ├── gdpr/                          ← GDPR (EU)
    ├── uk-gdpr/                       ← UK GDPR + DPA 2018
    ├── ccpa-cpra/                     ← CCPA / CPRA (California)
    ├── hipaa/                         ← HIPAA Security Rule (INDEX+SECTIONS — 5 files)
    ├── hipaa/privacy/                 ← HIPAA Privacy Rule (separate from Security Rule)
    ├── coppa/                         ← COPPA (children under 13)
    ├── pipeda/                        ← PIPEDA / Quebec Law 25 (Canada)
    ├── lgpd/                          ← LGPD (Brazil)
    ├── appi/                          ← APPI 2022 amendment (Japan)
    │
    ├── [FINANCIAL SERVICES & BANKING]
    ├── pci-dss/                       ← PCI DSS v4.0 (INDEX+SECTIONS — 12 req files)
    ├── sox/                           ← SOX ITGC (4 domains)
    ├── glba/                          ← GLBA Safeguards Rule
    ├── nydfs/500/                     ← NYDFS Part 500
    ├── dora/                          ← DORA (EU — 5 pillars)
    ├── ffiec/                         ← FFIEC handbooks (12)
    ├── basel/                         ← Basel III / BCBS 239
    ├── psd2/                          ← PSD2 / SCA (EU payments)
    ├── finra/                         ← FINRA broker-dealer rules
    │
    ├── [HEALTHCARE & LIFE SCIENCES]
    ├── fda/21cfr11/                   ← FDA 21 CFR Part 11
    ├── fda/21cfr210-211/              ← FDA cGMP (pharmaceutical)
    ├── fda/qmsr/                      ← FDA QMSR (medical device QMS)
    ├── fda/fsma/                      ← FDA FSMA (food safety)
    ├── iso/13485/                     ← ISO 13485:2016
    ├── eu-mdr/                        ← EU MDR 2017/745 + IVDR
    ├── iso/14971/                     ← ISO 14971:2019 (risk mgmt)
    ├── iec/62304/                     ← IEC 62304 (SW lifecycle)
    │
    ├── [MANUFACTURING & QUALITY]
    ├── iso/9001/                      ← ISO 9001:2015 (QMS foundation)
    ├── iatf/16949/                    ← IATF 16949:2016 (automotive)
    ├── as9100/                        ← AS9100 Rev D (aerospace)
    ├── nadcap/                        ← NADCAP (~20 commodities)
    ├── api/q1/                        ← API Q1/Q2 (oil and gas)
    ├── ipc/                           ← IPC-A-610 / J-STD-001 (electronics)
    │
    ├── [SAFETY & ENVIRONMENT]
    ├── osha/1910/                     ← OSHA 29 CFR 1910 (FULL — 10 standard files)
    ├── osha/1926/                     ← OSHA 29 CFR 1926 (FULL — 3 standard files)
    ├── iso/45001/                     ← ISO 45001:2018 (OH&S)
    ├── iso/14001/                     ← ISO 14001:2015 (EMS)
    ├── iso/50001/                     ← ISO 50001:2018 (EnMS)
    ├── rohs-reach/                    ← RoHS 3 / REACH (EU chemicals)
    │
    ├── [EXPORT CONTROLS]
    ├── itar-ear/                      ← ITAR (22 CFR 120–130) + EAR (15 CFR 730–774)
    │
    ├── [FOOD SAFETY]
    ├── iso/22000/                     ← ISO 22000:2018 / FSSC 22000
    │
    ├── [EPA / ENVIRONMENTAL]
    ├── epa/rcra/                      ← RCRA hazardous waste (LQG/SQG/VSQG — 90/270-day limits)
    ├── epa/epcra/                     ← EPCRA/SARA Title III (Tier II, TRI Form R)
    ├── epa/clean-air-act/             ← Clean Air Act (Title V, NSPS, NESHAP, CAM)
    ├── epa/npdes/                     ← NPDES + SPCC (water discharge + oil spill prevention)
    ├── epa/rmp/                       ← EPA RMP 40 CFR Part 68 (Program 1/2/3)
    │
    └── [EMERGING & SPECIALIZED]
        ├── eu-ai-act/                 ← EU AI Act 2024/1689 (4 risk tiers)
        └── wcag/                     ← WCAG 2.2 / Section 508 (accessibility)
```

### File types

| File | Purpose |
|---|---|
| `_index.md` | Registry manifest: confidence summary, assumption registry, contested item log, cross-standard dependencies, CI gate config, roadmap |
| `<STANDARD>.md` | Full RDF decomposition for a single standard: element extraction tables, YAML specs, Python test code |
| `guiding_docs/regulatory-decomposition-framework.md` | The complete RDF methodology document |

---

## Framework Coverage Status

**Registry version:** 2026.05 — Last updated: 2026-05-20

### Summary statistics

| Metric | Count |
|---|---|
| Total frameworks indexed | 67 |
| Frameworks with multi-file decomposition (DECOMPOSED) | 26 |
| Frameworks with single comprehensive file (SCAFFOLDED) | 41 |
| Individual standard files (beyond `_index.md`) | 151 |
| Guiding documents | 5 |
| Sectors covered | 11 |

Status key: **DECOMPOSED** = index + multiple standard files with control-by-control treatment; **SCAFFOLDED** = index + one comprehensive standard file covering the full framework; **INDEX** = `_index.md` only — individual standard files not yet written

---

### Cybersecurity & IT Security

| Framework | Path | Authority | Scope | Status | Individual files |
|---|---|---|---|---|---|
| NERC CIP (CIP-002–CIP-015) | `nerc/cip/` | NERC / FERC | Electric grid BES cybersecurity | **DECOMPOSED** | 14 standard files |
| NERC Reliability Standards (non-CIP) | `nerc/ops/` | NERC / FERC | BES operations, planning, protection, vegetation mgmt | **DECOMPOSED** | com-top-operations.md, fac-eop-operations.md, int-iro-var-coordination.md, mod-tpl-eop-planning.md, per-bal-personnel.md, prc-protection-control.md |
| NIST SP 800-53 r5 | `nist/sp800-53/` | NIST | Federal IS security controls (~1,007 controls) | **DECOMPOSED** | core-technical-controls.md, contingency-incident-assessment.md, maintenance-media-physical-personnel.md, planning-program-training-privacy.md, risk-acquisition-supply-chain.md |
| NIST SP 800-171 r3 | `nist/sp800-171/` | NIST | CUI protection — 17 families, 110 requirements | **DECOMPOSED** | ac-access-control.md, ia-identification-authentication.md, au-cm-si-core-technical.md, sc-ir-pe-remaining.md, at-ra-sr-pl-pm-remaining.md |
| NIST CSF 2.0 | `nist/csf2/` | NIST | Voluntary cybersecurity framework — 6 functions, 106 subcategories | SCAFFOLDED | function-profiles-subcategories.md |
| NIST SP 800-82 r3 | `nist/sp800-82/` | NIST | OT/ICS security guide — SP 800-53 tailoring for OT | SCAFFOLDED | ot-ics-security-program.md |
| NIST AI RMF 1.0 | `nist/ai-rmf/` | NIST | AI risk management — GOVERN/MAP/MEASURE/MANAGE | **DECOMPOSED** | govern-map.md, measure-manage.md |
| CMMC 2.0 | `cmmc/` | DoD / OUSD(A&S) | Defense contractor cybersecurity — 3 levels | **DECOMPOSED** | level1-level2-practices.md, level3-800-172-delta.md |
| ISO/IEC 27001:2022 | `iso/27001/` | ISO/IEC | ISMS — 93 Annex A controls, 4 themes | **DECOMPOSED** | clauses-4-10-isms-mandatory.md, annex-a5-organizational.md, annex-a6-people.md, annex-a7-physical.md, annex-a8-technological.md |
| FedRAMP | `fedramp/` | OMB / GSA | Cloud service authorization — 800-53 + overlays | **DECOMPOSED** | account-contingency-media.md, technical-overlays-high-enhancements.md, conmon-and-overlays.md |
| SOC 2 | `soc2/` | AICPA | Service org trust criteria — CC1–CC9 + 4 additional | **DECOMPOSED** | cc1-cc2-cc3-cc4-governance-risk.md, cc6-logical-physical-access.md, cc7-system-operations.md, cc8-cc5-change-control-activities.md, cc9-c1-pi1-additional-criteria.md, a1-availability.md, p-series-privacy.md |
| IEC 62443 | `iec/62443/` | IEC | OT/ICS security — 7 FRs, 4 Security Levels, zone/conduit | **DECOMPOSED** | fr1-fr3-iam-use-integrity.md, fr4-fr7-confidentiality-availability.md |
| TISAX / VDA ISA 6.0 | `tisax/` | ENX / VDA | Automotive supply chain information security | **DECOMPOSED** | isms-hr-physical-controls.md, it-supplier-controls.md |
| SEC Cybersecurity Rules 2023 | `sec/cybersecurity/` | SEC | 8-K 4-business-day disclosure + annual risk governance | SCAFFOLDED | incident-disclosure-annual-report.md |
| SWIFT CSP / CSCF v2025 | `swift/csp/` | SWIFT | Financial institution SWIFT infrastructure — 25 mandatory controls | **DECOMPOSED** | secure-environment-controls.md, access-credential-controls.md, detect-respond-controls.md |
| TSA Pipeline Directives SD-02D | `tsa/pipeline/` | TSA / DHS | Critical pipeline OT/IT cybersecurity | SCAFFOLDED | pipeline-cybersecurity-directives.md |
| NRC 10 CFR 73.54 | `nrc/10cfr73/` | NRC | Nuclear power reactor cybersecurity | SCAFFOLDED | nuclear-cybersecurity-program.md |

---

### Privacy & Data Protection

| Framework | Path | Authority | Scope | Status | Individual files |
|---|---|---|---|---|---|
| GDPR | `gdpr/` | EU / DPAs | EU personal data protection — 99 articles | **DECOMPOSED** | principles-lawful-basis.md, core-articles.md, data-subject-rights-design.md |
| UK GDPR + DPA 2018 | `uk-gdpr/` | ICO (UK) | Post-Brexit UK data protection — UK GDPR delta table | SCAFFOLDED | uk-specific-deltas.md |
| CCPA / CPRA | `ccpa-cpra/` | CalAG / CPPA | California consumer privacy — 3 thresholds, GPC signal | SCAFFOLDED | consumer-rights-obligations.md |
| HIPAA Security Rule | `hipaa/` | HHS / OCR | ePHI technical/admin/physical safeguards | **DECOMPOSED** | 164.308-administrative-safeguards.md, 164.310-physical-safeguards.md, 164.312-technical-safeguards.md, 164.314-organizational-requirements.md, 164.316-policies-documentation.md |
| HIPAA Privacy Rule | `hipaa/privacy/` | HHS / OCR | PHI in all forms — 9-element auth checklist, Safe Harbor 18 identifiers | **DECOMPOSED** | uses-disclosures-authorization.md, individual-rights-breach.md |
| COPPA | `coppa/` | FTC | Children's online privacy — under 13, verifiable parental consent | SCAFFOLDED | children-online-privacy.md / 1 assumption |
| PIPEDA / Law 25 | `pipeda/` | OPC (Canada) | Canadian private-sector privacy — 10 Fair Information Principles | SCAFFOLDED | canadian-privacy-obligations.md / 2 assumptions |
| LGPD | `lgpd/` | ANPD (Brazil) | Brazilian personal data protection — 10 legal bases, 15-day DSR | SCAFFOLDED | lgpd-obligations.md |
| APPI (2022 amendment) | `appi/` | PPC (Japan) | Japanese personal data protection — 2-week DSR, 3-5 day breach report | SCAFFOLDED | japanese-personal-data-protection.md / 1 assumption |

---

### Financial Services & Banking

| Framework | Path | Authority | Scope | Status | Individual files |
|---|---|---|---|---|---|
| PCI DSS v4.0 | `pci-dss/` | PCI SSC | Payment card data security — 12 requirements | **DECOMPOSED** | req-01 through req-12 (12 files) |
| SOX ITGC | `sox/` | SEC / PCAOB | Public company financial controls — 4 ITGC domains | SCAFFOLDED | itgc-access-change-operations.md |
| GLBA Safeguards Rule | `glba/` | FTC / OCC | Financial institution customer data — 9 safeguard elements | SCAFFOLDED | safeguards-rule.md |
| NYDFS Part 500 | `nydfs/500/` | NYDFS | NY-licensed financial entity cybersecurity — 6yr log retention | SCAFFOLDED | cybersecurity-program.md |
| DORA | `dora/` | EU / ESAs | EU financial entity digital operational resilience — 5 pillars | SCAFFOLDED | incident-reporting-contracts-resilience.md |
| FFIEC | `ffiec/` | FFIEC | US bank examination benchmarks — 12 handbooks | SCAFFOLDED | information-security-examination.md |
| Basel III / BCBS 239 | `basel/` | BCBS | Capital adequacy ratios + risk data aggregation | SCAFFOLDED | capital-adequacy-risk-data-aggregation.md / 2 assumptions |
| PSD2 / SCA | `psd2/` | EBA (EU) | Payment services strong customer authentication | SCAFFOLDED | strong-customer-authentication.md |
| FINRA Rules | `finra/` | FINRA | Broker-dealer supervision, records, customer protection | SCAFFOLDED | broker-dealer-supervision-records.md |

---

### Healthcare & Life Sciences

| Framework | Path | Authority | Scope | Status | Individual files |
|---|---|---|---|---|---|
| FDA 21 CFR Part 11 | `fda/21cfr11/` | FDA | Electronic records and signatures | **DECOMPOSED** | electronic-records-esig.md, system-validation.md |
| FDA 21 CFR 210/211 cGMP | `fda/21cfr210-211/` | FDA | Pharmaceutical manufacturing good practices | SCAFFOLDED | pharmaceutical-manufacturing-controls.md |
| FDA QMSR | `fda/qmsr/` | FDA | Medical device quality management — ISO 13485 + 15 FDA deltas | SCAFFOLDED | fda-qmsr-deltas.md |
| FDA FSMA | `fda/fsma/` | FDA | Food safety modernization — HARPC, FSVP, FTL traceability | SCAFFOLDED | harpc-traceability-fsvp.md / 3 assumptions |
| ISO 13485:2016 | `iso/13485/` | ISO | Medical device QMS — ~80 sub-clauses | **DECOMPOSED** | records-and-design-controls.md, management-and-product-controls.md |
| EU MDR 2017/745 / IVDR | `eu-mdr/` | EC / notified bodies | EU medical device regulation — 4 device classes | **DECOMPOSED** | gspr-technical-documentation.md, pms-vigilance-conformity.md |
| ISO 14971:2019 | `iso/14971/` | ISO | Medical device risk management — 6-step process | SCAFFOLDED | risk-management-process.md |
| IEC 62304:2006+AMD1 | `iec/62304/` | IEC | Medical device software lifecycle — 3 safety classes | **DECOMPOSED** | software-development-controls.md, maintenance-risk-problem-resolution.md |

---

### Manufacturing & Quality

| Framework | Path | Authority | Scope | Status | Individual files |
|---|---|---|---|---|---|
| ISO 9001:2015 | `iso/9001/` | ISO | General-purpose QMS — foundation for all sector-specific standards | **DECOMPOSED** | records-and-operational-controls.md, management-process-controls.md |
| IATF 16949:2016 | `iatf/16949/` | IATF | Automotive QMS — APQP/PPAP/FMEA/MSA/SPC | **DECOMPOSED** | ppap-and-product-controls.md, supplier-and-problem-solving.md |
| AS9100 Rev D | `as9100/` | SAE / IAQG | Aerospace QMS — FAI, FOD, counterfeit part controls | SCAFFOLDED | aerospace-qms-controls.md |
| NADCAP | `nadcap/` | PRI | Aerospace special process accreditation — ~20 commodities | SCAFFOLDED | special-process-accreditation.md |
| API Q1/Q2 (9th/1st Ed) | `api/q1/` | API | Oil and gas equipment/service QMS + API Monogram | SCAFFOLDED | oilgas-qms-controls.md / 1 assumption |
| IPC-A-610 / J-STD-001 Rev H | `ipc/` | IPC | Electronics assembly acceptability — 3 product classes | SCAFFOLDED | electronics-assembly-acceptability.md |

---

### Safety & Environment

| Framework | Path | Authority | Scope | Status | Individual files |
|---|---|---|---|---|---|
| OSHA 29 CFR 1910 | `osha/1910/` | U.S. DOL / OSHA | General industry safety — 10 most-cited standards | **DECOMPOSED** | 10 standard files |
| OSHA 29 CFR 1926 | `osha/1926/` | U.S. DOL / OSHA | Construction safety — 3 most-cited standards | **DECOMPOSED** | 1926.451-scaffolds.md, 1926.501-fall-protection.md, 1926.651-excavations.md |
| ISO 45001:2018 | `iso/45001/` | ISO | OH&S management system — replaces OHSAS 18001 | SCAFFOLDED | ohs-management-system.md / 1 assumption |
| ISO 14001:2015 | `iso/14001/` | ISO | Environmental management system | SCAFFOLDED | environmental-management-system.md / 1 assumption |
| ISO 50001:2018 | `iso/50001/` | ISO | Energy management system — EnPI, SEU, energy review | SCAFFOLDED | energy-management-system.md / 1 assumption |
| RoHS 3 / REACH | `rohs-reach/` | EC / ECHA | EU chemical restrictions — 10 RoHS substances, SVHC 0.1% | SCAFFOLDED | chemical-restriction-compliance.md |

---

### Export Controls & Trade Compliance

| Framework | Path | Authority | Scope | Status | Individual files |
|---|---|---|---|---|---|
| ITAR / EAR | `itar-ear/` | State Dept / Commerce | U.S. export controls — USML / CCL | **DECOMPOSED** | deterministic-controls.md, parameterized-controls.md |

---

### Food Safety

| Framework | Path | Authority | Scope | Status | Individual files |
|---|---|---|---|---|---|
| ISO 22000:2018 / FSSC 22000 | `iso/22000/` | ISO / FSSC | Food safety management — HACCP + Annex SL | SCAFFOLDED | fsms-haccp-traceability.md / 2 assumptions |
| FDA FSMA | `fda/fsma/` | FDA | *(Also listed under Healthcare — HARPC, FTL 24-hour traceability)* | SCAFFOLDED | harpc-traceability-fsvp.md / 3 assumptions |

---

### EPA / Environmental

| Framework | Path | Authority | Scope | Status | Individual files |
|---|---|---|---|---|---|
| RCRA (40 CFR Parts 260–272) | `epa/rcra/` | EPA | Hazardous waste generation, storage, disposal — LQG/SQG/VSQG tiers | SCAFFOLDED | hazardous-waste-generator.md |
| EPCRA / SARA Title III | `epa/epcra/` | EPA / LEPCs | Emergency planning, community right-to-know, TRI Form R | SCAFFOLDED | emergency-planning-tri-reporting.md |
| Clean Air Act (Title V / NSPS / NESHAP) | `epa/clean-air-act/` | EPA / state agencies | Air emissions — permits, NSPS, MACT, CAM, GHG reporting | SCAFFOLDED | title-v-nsps-neshap.md |
| Clean Water Act / NPDES / SPCC | `epa/npdes/` | EPA / Army Corps | Water discharge permits, oil spill prevention, stormwater | SCAFFOLDED | permit-compliance-spcc-stormwater.md |
| EPA RMP (40 CFR Part 68) | `epa/rmp/` | EPA | Risk Management Program — accidental release prevention; Program 1/2/3 | SCAFFOLDED | risk-management-program.md |

---

### Nuclear Safety & Quality

| Framework | Path | Authority | Scope | Status | Individual files |
|---|---|---|---|---|---|
| NRC 10 CFR Part 50 | `nrc/10cfr50/` | NRC | Nuclear power reactor safety, QA, operations, and event reporting | **DECOMPOSED** | appendix-b-qa.md, event-reporting.md, fire-protection.md, maintenance-rule.md, 50.55a-isi-ist.md, 50.59-changes-tests-experiments.md |
| NRC 10 CFR Part 26 | `nrc/10cfr26/` | NRC | Fitness for duty — drug/alcohol testing, work hour controls, behavioral observation | SCAFFOLDED | fitness-for-duty.md |

---

### Emerging & Specialized

| Framework | Path | Authority | Scope | Status | Individual files |
|---|---|---|---|---|---|
| EU AI Act 2024/1689 | `eu-ai-act/` | EC | AI system risk classification — 4 tiers, prohibited practices | SCAFFOLDED | prohibited-highrisk-gpai.md / 2 assumptions |
| WCAG 2.2 / Section 508 | `wcag/` | W3C / US Access Board | Digital accessibility — POUR principles, 87 success criteria | SCAFFOLDED | wcag22-section508-accessibility.md / 1 assumption |

---

### Guiding Documents

| Document | Path | Purpose |
|---|---|---|
| Regulatory Decomposition Framework | `guiding_docs/regulatory-decomposition-framework.md` | Core RDF methodology — 4-element extraction, confidence classification, test patterns |
| Assumption Registry Template | `guiding_docs/assumption-registry-template.md` | YAML schema, field definitions, approval workflow, and staleness enforcement rules for all PARAMETERIZED assumptions |
| Cross-Framework Dependency Map | `guiding_docs/cross-framework-dependency-map.md` | 10 shared evidence artifact clusters (IRP, log retention, MFA, pentest, etc.) showing how one implementation satisfies multiple frameworks |
| CI/CD Gate Configuration Reference | `guiding_docs/ci-cd-gate-config-reference.md` | Pattern 1/2/3 pytest implementation, failure routing matrix, GitHub Actions pipeline YAML, staleness check tool |
| Scoping Fixture Catalog | `guiding_docs/scoping-fixture-catalog.md` | All `is_in_scope()` pre-condition functions for all 67 frameworks; scoping matrix by organization type |

---

### Parse roadmap — next priority targets

The following frameworks have the highest DETERMINISTIC density and are best candidates for expanding SCAFFOLDED entries into full DECOMPOSED treatment:

| Priority | Framework | Reason |
|---|---|---|
| 1 | PCI DSS v4.0 | 12 requirement `_index.md` files exist; full YAML + test code next |
| 2 | HIPAA Security Rule | 5 section files exist; test code scaffolding next |
| 3 | NIST SP 800-171 r3 | 110 requirements; high CUI program demand; CMMC dependency |
| 4 | GDPR | 72h breach deadline + 9 DSR rights = highest DETERMINISTIC density in privacy cluster |
| 5 | ISO 27001 Annex A | 93 controls; 4 section files exist; SoA generation target |
| 6 | SOX ITGC | Access provisioning/termination timelines; high demand |
| 7 | NYDFS Part 500 | Strictest log retention in registry (6yr); small control set |
| 8 | FDA 21 CFR Part 11 | Audit trail non-alterability; high demand from life sciences orgs |

---

## The Regulatory Decomposition Framework (RDF)

The core methodology is summarized below. The full internal working document (`guiding_docs/regulatory-decomposition-framework.md`) is not distributed with this repository — it is an internal process document maintained by Enthropic LLC and excluded via `.gitignore`. The summary below is sufficient to read and contribute to the registry.

**Every regulation contains four extractable elements:**

| Element | Question |
|---|---|
| **Subject** | Who or what does this apply to? |
| **Condition** | Under what circumstances does the obligation trigger? |
| **Obligation** | What must be true when the condition is met? |
| **Evidence** | How is compliance demonstrated and verified? |

**Each element is independently classified:**

| Classification | Meaning | Engineering response |
|---|---|---|
| `DETERMINISTIC` | Exact threshold, boolean, or enumerable value | Automate fully |
| `PARAMETERIZED` | Bounded but qualitative — requires a defined assumption | Automate with documented assumption; flag for periodic re-approval |
| `CONTESTED` | Industry or legal interpretation varies | Surface via test; require human determination with sign-off |
| `UNRESOLVABLE` | Genuinely undefined | Escalate externally; do not automate |

**The lowest-scoring element sets the test pattern for that regulation:**

- **Pattern 1 (HIGH):** Direct assertion — `assert asset.impact_rating == "High"`
- **Pattern 2 (MEDIUM):** Parameterized assertion with `@pytest.mark.assumption(id=...)` — tests the compliance condition *given* a documented assumption
- **Pattern 3 (LOW/CONTESTED):** Human surfacing — tests that a valid, current human determination exists; does not determine compliance itself

---

## How to Use This Registry

### As a reference

Read the `_index.md` for a framework to understand its overall confidence profile, open assumptions, and cross-standard dependencies before implementing any tests. Read the individual standard files for the full YAML spec and test code.

### As a starting point for a compliance program

1. Identify which frameworks apply to your organization.
2. Read the corresponding `_index.md` files and note all PARAMETERIZED and CONTESTED items.
3. Work through the assumption registry: for each open assumption, have your legal or compliance team approve the stated assumption or substitute their own. Record the approval with a date and signature hash.
4. Deploy the test code against your SMS/CMDB/asset database. Pattern 1 tests run immediately; Pattern 2 tests require your data layer to expose the evidence fields documented in the YAML specs.
5. Wire Pattern 3 tests to your human-review workflow.

### As a contribution target

Every placeholder directory is an open contribution target. The format is defined — apply the RDF to the next standard and submit a pull request. See [Contributing](#contributing).

### Data model assumptions

The Python tests reference a data model (fixtures) that you must implement for your environment. The `_index.md` for each framework documents the required schema fields. The tests use standard pytest fixtures — `live_assets`, `training_records`, `written_programs`, etc. — which you wire to your actual data source (PostgreSQL, SQLite, REST API, etc.) in your `conftest.py`.

No specific ORM or database is required. The tests are pure assertions against Python dicts/objects.

---

## Thought Process: How This Registry Was Built

This section documents the creation methodology for transparency and reproducibility.

### Step 1: Source text acquisition

Regulations were sourced from their authoritative primary sources:
- NERC CIP: NERC.com official standards PDFs
- OSHA: eCFR (ecfr.gov) Title 29
- NIST: NIST CSRC publications (csrc.nist.gov)
- All others: respective issuing authority official publications

No secondary summaries, compliance vendor interpretations, or training materials were used as the primary source. Where interpretive guidance exists (OSHA Letters of Interpretation, NERC enforcement memos), it was used to inform ambiguity classification — but the requirement text itself is always quoted from the primary source.

### Step 2: 4-element extraction

For each requirement (or sub-requirement), the four elements were extracted verbatim from the regulation text. If any element could not be extracted without interpretation, the regulation was flagged as ambiguous before classification began.

The extraction is the most important step. Sloppy extraction — paraphrasing the obligation, abstracting the subject — is how ambiguity gets hidden. Every element table quotes the specific regulatory language it was derived from.

### Step 3: Ambiguity classification

Each element was independently classified against the four-tier system. The key discipline: classification was made based on what the regulation *says*, not what the industry does. If a word like "reasonable," "adequate," "as necessary," or "technically feasible" appears in an obligation element, it is PARAMETERIZED at minimum, not rationalized into DETERMINISTIC because everyone knows what it means.

Words that consistently trigger PARAMETERIZED classification in these frameworks: *reasonable*, *adequate*, *feasible*, *necessary*, *sufficient*, *appropriate*, *substantially*, *timely*.

Words that consistently trigger CONTESTED classification: *commensurate*, *equivalent*, *acceptable*, and any obligation where OSHA enforcement history shows Regional Entity variation.

### Step 4: YAML specification before code

No test code was written until the YAML specification was complete. This discipline prevents the most common failure mode in compliance automation: writing the test to pass the data you have rather than to check the regulation you're subject to.

The YAML spec is the authoritative source of truth. If the test code and the YAML spec disagree, the YAML spec wins.

### Step 5: Test code generation

Test code was written in three distinct patterns corresponding to the confidence level. The patterns are not stylistic choices — they have different epistemological claims:

- Pattern 1 claims: "This system is compliant with [requirement] as of this test run."
- Pattern 2 claims: "This system is compliant with [requirement] given assumption [ASSUME-XXX-YYY], which was approved on [date]."
- Pattern 3 claims: "A qualified human has determined compliance with [requirement] as of [date], and that determination is current."

These are different claims. Conflating them is how compliance programs fail audits they thought they were passing.

---

## Contributing

Contributions are welcome under the terms of the [CC BY 4.0 license](#license).

**Before you start:** Read [`guiding_docs/regulatory-decomposition-framework.md`](guiding_docs/regulatory-decomposition-framework.md) — it defines the 4-element extraction process, ambiguity classification rules, and the three test patterns. Without it, it's difficult to produce a conformant PR. The [`guiding_docs/assumption-registry-template.md`](guiding_docs/assumption-registry-template.md) covers the PARAMETERIZED assumption schema you'll need for any non-DETERMINISTIC elements.

**To add a new standard:**

1. Fork the repository.
2. Locate or create the appropriate `compliance_entities/<framework>/` directory.
3. Create a `_index.md` if it does not exist, following the existing manifests as a template.
4. Create the standard file using the RDF format: source text excerpt, 4-element extraction table, ambiguity classification, YAML spec, Python test code. See the [NERC CIP example above](#start-here-a-nerc-cip-example-end-to-end) for the expected level of detail.
5. Update the `_index.md` manifest to include the new standard in the confidence summary, assumption registry, and per-standard confidence map.
6. Submit a pull request with a description of the regulation decomposed and a note on any CONTESTED or UNRESOLVABLE classifications you identified.

**Standards for contributions:**

- Source text must be quoted verbatim from the primary regulatory source, not paraphrased.
- Every PARAMETERIZED element must have a documented assumption with the fields defined in the RDF methodology.
- Every CONTESTED element must reference a specific reason (inspector-dependent enforcement, conflicting case law, undefined terms without industry consensus, etc.).
- Test code must be syntactically valid Python 3 and use standard pytest conventions.
- Do not rationalize ambiguous elements into DETERMINISTIC — surface the ambiguity. That is the value of this registry.

**To correct an existing decomposition:**

Open an issue with: the regulation ID, the element you believe is misclassified, the primary source text supporting the correction, and the classification you believe is appropriate. For CONTESTED reclassifications, include a reference to the interpretive basis (enforcement memo, court decision, standards body guidance).

---

## License

This work is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, including commercial

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. Attribution must include:
  - The name **Enthropic LLC**
  - A link to **https://www.enthropicdata.com**
  - The repository URL or name: **Compliance Test Case Registry**
  - An indication of any changes made from the original

Full license text: https://creativecommons.org/licenses/by/4.0/

### Attribution example

```
Compliance Test Case Registry
© Enthropic LLC — https://www.enthropicdata.com
Licensed under CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/
[Describe any changes made]
```

### Note on regulatory source text

Quoted regulatory text (CFR, NERC standards, NIST publications, etc.) is reproduced for educational and analytical purposes. Regulations are government works and are not subject to copyright. NERC standards are copyrighted by NERC but are reproduced here in excerpt form for commentary and analysis. ISO standards are copyrighted by ISO; this repository does not reproduce ISO standard text in full — only excerpts sufficient for decomposition under fair use/fair dealing principles.

---

## Contact

**Enthropic LLC**
Website: [https://www.enthropicdata.com](https://www.enthropicdata.com)
Location: Weddington, NC

For questions about this registry, open an issue in this repository. For commercial licensing inquiries or custom regulatory decomposition work, contact us through the website.

---

*Compliance Test Case Registry — built by [Enthropic LLC](https://www.enthropicdata.com)*
