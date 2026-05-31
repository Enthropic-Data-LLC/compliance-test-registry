# Scoping Fixture Catalog

**Document version:** 2026.05
**Last updated:** 2026-05-20
**Purpose:** Collects all `is_in_scope()` pre-condition functions from every framework `_index.md` into one reference. A developer wiring up multi-framework compliance tests can read this document to understand what scoping attestations must be implemented in `conftest.py` before any framework's tests are enforcing.

---

## How Scoping Fixtures Work

Every framework in this registry has at least one scoping pre-condition — a function that returns `True` if the organization is subject to that framework's requirements. Pattern 1/2/3 tests are **only enforcing when their scoping fixture returns True.**

This prevents a network equipment company from failing HIPAA tests, or a consumer web app from failing NERC CIP tests.

```python
# Conceptual pipeline
def should_run_test(test):
    for fixture in test.scoping_fixtures:
        if not fixture():
            pytest.skip(f"Scoping fixture {fixture.__name__} returned False — not in scope")
    return True
```

In practice, implement scoping fixtures as pytest fixtures that call `pytest.skip()` if scope is not met, or tag tests with scope marks that are filtered at run time.

---

## Implementation Template

```python
# compliance_fixtures/scope.py

class OrganizationScope:
    """
    Single source of truth for all scoping determinations.
    Populated from your organization's profile / configuration file.
    Each attribute must be explicitly set — there is no default 'True'.
    """
    
    def __init__(self, config_path: str):
        self._config = self._load(config_path)
    
    # Each method below corresponds to one framework scoping fixture.
    # Add a comment referencing the _index.md that defines it.
    
    def is_bes_asset_owner(self) -> bool:
        """NERC CIP — owns/operates BES Cyber Systems."""
        return self._config.get("nerc_cip.in_scope", False)
    
    def processes_cui(self) -> bool:
        """NIST SP 800-171 / CMMC — handles Controlled Unclassified Information."""
        return self._config.get("cui.in_scope", False)
    
    # ... etc.
```

---

## Full Catalog

### Cybersecurity & IT Security

```python
def is_bes_asset_owner() -> bool:
    """
    NERC CIP — nerc/cip/_index.md
    True if organization owns or operates Bulk Electric System Cyber Systems (BCS).
    Source: NERC CIP-002-5.1a — responsible entity designation by NERC/RE.
    """

def processes_cui() -> bool:
    """
    NIST SP 800-171 / CMMC — nist/sp800-171/_index.md, cmmc/_index.md
    True if organization handles, stores, or transmits Controlled Unclassified Information
    under a federal contract or agreement.
    Source: DoD contract clause DFARS 252.204-7012.
    """

def is_federal_information_system() -> bool:
    """
    NIST SP 800-53 / FedRAMP — nist/sp800-53/_index.md, fedramp/_index.md
    True if system is operated by or on behalf of a U.S. federal agency,
    OR is a cloud service requiring FedRAMP authorization.
    Source: FISMA (44 U.S.C. §3551); FedRAMP authorization letter.
    """

def in_iso_27001_scope() -> bool:
    """
    ISO 27001 — iso/27001/_index.md
    True if organization has defined an ISMS scope and seeks/maintains ISO 27001 certification.
    Source: ISO 27001 §4.3 — scope is organization-defined.
    Note: Must set to True BEFORE implementing any Annex A controls to establish scope.
    """

def in_pci_cde() -> bool:
    """
    PCI DSS — pci-dss/_index.md
    True for systems within or connected to the Cardholder Data Environment (CDE):
    stores, processes, or transmits cardholder data, OR is connected to such a system.
    Source: PCI DSS v4.0 §1.2.1 scoping guidance.
    """

def is_soc2_service_organization() -> bool:
    """
    SOC 2 — soc2/_index.md
    True if organization provides services to user entities where those services
    are relevant to user entities' internal controls over financial reporting, or
    where security/availability/confidentiality/processing integrity/privacy commitments exist.
    Source: AICPA TSC 2017 §100.
    """

def has_ics_ot_systems() -> bool:
    """
    IEC 62443 / NIST SP 800-82 — iec/62443/_index.md, nist/sp800-82/_index.md
    True if organization operates Industrial Control Systems (ICS), SCADA, DCS,
    PLC, or RTU equipment as part of a production or critical infrastructure process.
    """

def is_swift_user() -> bool:
    """
    SWIFT CSP — swift/csp/_index.md
    True if organization has a SWIFT BIC and connects to the SWIFT network
    via any connectivity type (A1, A2, A3, A4, B).
    Source: SWIFT connectivity agreement + BIC registration.
    """

def is_tsa_designated_critical_pipeline() -> bool:
    """
    TSA Pipeline — tsa/pipeline/_index.md
    True if operator has received TSA written designation as critical pipeline facility.
    Source: TSA SD-02D designation letter (facility-specific).
    """

def is_nrc_nuclear_power_licensee() -> bool:
    """
    NRC 10 CFR 73 — nrc/10cfr73/_index.md
    True if entity holds NRC license to operate a nuclear power reactor
    under 10 CFR Part 50 or Part 52.
    """

def requires_tisax() -> bool:
    """
    TISAX — tisax/_index.md
    True if organization has contractual obligation from automotive OEM requiring TISAX label.
    Source: Purchase order or supplier qualification requirement from OEM.
    """

def is_sec_reporting_company() -> bool:
    """
    SEC Cybersecurity Rules — sec/cybersecurity/_index.md
    True if organization is a reporting company under SEC Exchange Act
    (registered under §12 or required to file under §15(d)).
    Source: SEC registration documentation.
    """
```

---

### Privacy & Data Protection

```python
def processes_eu_personal_data() -> bool:
    """
    GDPR — gdpr/_index.md
    True if organization: (1) is established in EU/EEA, OR (2) processes personal data
    of EU/EEA data subjects in connection with offering goods/services or monitoring behavior.
    Source: GDPR Art. 3.
    """

def processes_uk_personal_data() -> bool:
    """
    UK GDPR — uk-gdpr/_index.md
    True if organization: (1) is established in UK, OR (2) processes personal data
    of UK data subjects in connection with offering goods/services or monitoring behavior.
    Source: UK GDPR Art. 3 (same territorial scope as EU GDPR but UK-specific).
    """

def processes_ephi() -> bool:
    """
    HIPAA Security Rule — hipaa/_index.md
    True if organization is a Covered Entity (CE) or Business Associate (BA) that
    creates, receives, maintains, or transmits electronic Protected Health Information.
    Source: 45 CFR §160.103 (covered entity definition).
    """

def processes_phi_any_form() -> bool:
    """
    HIPAA Privacy Rule — hipaa/privacy/_index.md
    True if organization is a CE or BA that creates, receives, maintains, or transmits
    Protected Health Information in ANY form (electronic, paper, or oral).
    Source: 45 CFR §160.103. Superset of processes_ephi().
    """

def is_coppa_operator() -> bool:
    """
    COPPA — coppa/_index.md
    True if EITHER: (1) service is 'directed to children under 13', OR
    (2) operator has 'actual knowledge' that users include children under 13.
    Source: 16 CFR §312.2.
    Note: 'directed to children' determination may itself require legal review (CONTESTED).
    """

def is_ccpa_covered_business() -> bool:
    """
    CCPA / CPRA — ccpa-cpra/_index.md
    True if for-profit business that: (1) has annual gross revenue > $25M, OR
    (2) buys/sells/receives/shares personal information of ≥ 100,000 consumers/households, OR
    (3) derives ≥ 50% of annual revenue from selling/sharing personal information.
    AND does business in California.
    Source: Cal. Civ. Code §1798.140(d).
    """

def processes_canadian_personal_information() -> bool:
    """
    PIPEDA — pipeda/_index.md
    True if private-sector organization collects, uses, or discloses personal information
    in the course of commercial activities in Canada.
    Source: PIPEDA §4.
    """

def in_scope_lgpd(processing_activity) -> bool:
    """
    LGPD — lgpd/_index.md
    True if processing occurs in Brazil, OR purpose is offering goods/services to
    Brazil data subjects, OR personal data was collected in Brazil.
    Source: LGPD Art. 3.
    """

def processes_japan_personal_information() -> bool:
    """
    APPI — appi/_index.md
    True if organization handles personal information of individuals in Japan.
    Source: APPI Art. 2.
    """
```

---

### Financial Services

```python
def is_finra_member() -> bool:
    """
    FINRA — finra/_index.md
    True if entity is a FINRA-member broker-dealer (SEC-registered under Securities
    Exchange Act §15).
    Source: FINRA membership agreement.
    """

def is_nydfs_covered_entity() -> bool:
    """
    NYDFS Part 500 — nydfs/500/_index.md
    True if entity operates under a license, registration, charter, certificate, permit,
    or accreditation issued by NYDFS.
    Source: 23 NYCRR §500.01(c).
    """

def is_glba_financial_institution() -> bool:
    """
    GLBA — glba/_index.md
    True if entity is a financial institution under GLBA (significantly engaged in
    financial activities) that is subject to FTC Safeguards Rule OR federal banking regulator.
    Source: 15 U.S.C. §6809(3); 16 CFR Part 314 (FTC).
    """

def is_sox_public_company() -> bool:
    """
    SOX — sox/_index.md
    True if entity is a reporting company under SEC Exchange Act (files 10-K/10-Q).
    Also applies to entities that are consolidated subsidiaries of public companies
    where financial systems contribute to consolidated financial statements.
    Source: SOX §302/404 applicability.
    """

def is_dora_financial_entity() -> bool:
    """
    DORA — dora/_index.md
    True if entity is within DORA's scope: credit institutions, payment institutions,
    investment firms, crypto-asset service providers, insurance undertakings, etc.
    operating in EU/EEA.
    Source: DORA Art. 2(1) — enumerated entity types.
    """

def is_psd2_psp() -> bool:
    """
    PSD2 — psd2/_index.md
    True if entity is a licensed payment service provider operating in EU/EEA.
    PSP types: credit institution, e-money institution, payment institution, AISP, PISP, ASPSP.
    Source: PSD2 Art. 1.
    """

def is_gsib() -> bool:
    """
    Basel III / BCBS 239 — basel/_index.md
    True if institution is on FSB G-SIB list (annual November publication).
    Source: FSB annual G-SIB identification methodology.
    """
```

---

### Healthcare & Life Sciences

```python
def is_fda_registered_food_facility() -> bool:
    """
    FDA FSMA — fda/fsma/_index.md
    True if facility manufactures, processes, packs, or holds food for human
    consumption in the US and is required to register under 21 CFR Part 1.
    """

def manufactures_medical_devices() -> bool:
    """
    FDA QMSR / ISO 13485 / EU MDR / ISO 14971 / IEC 62304
    True if organization designs, manufactures, or remanufactures medical devices
    (Class I/II/III or EU Class I/IIa/IIb/III).
    Source: FDA 21 CFR Part 820 §820.3(r); EU MDR Art. 2(1).
    """

def is_fda_21cfr11_system(system) -> bool:
    """
    FDA 21 CFR Part 11 — fda/21cfr11/_index.md
    True if system creates, modifies, maintains, or transmits electronic records
    that the FDA requires to be kept OR that are submitted to FDA.
    Source: 21 CFR §11.2.
    """
```

---

### Manufacturing, Safety & Environment

```python
def is_osha_general_industry() -> bool:
    """
    OSHA 29 CFR 1910 — osha/1910/_index.md
    True for employers in general industry (not construction, maritime, or agriculture).
    All employers with ≥ 1 employee are subject to OSHA.
    Source: OSH Act §5.
    """

def is_osha_construction() -> bool:
    """
    OSHA 29 CFR 1926 — osha/1926/_index.md
    True for employers engaged in construction activities (building, alteration,
    repair, including painting and decorating).
    Source: 29 CFR §1926.32(g).
    """

def generator_category(monthly_kg: float) -> str:
    """
    RCRA — epa/rcra/_index.md
    Returns 'LQG', 'SQG', or 'VSQG' based on monthly hazardous waste generation.
    Source: 40 CFR §262.
    """
    if monthly_kg >= 1000:
        return "LQG"
    elif monthly_kg >= 100:
        return "SQG"
    return "VSQG"

def requires_rmp(process) -> bool:
    """
    EPA RMP — epa/rmp/_index.md
    True if any single process has a regulated substance at or above threshold quantity (TQ).
    Source: 40 CFR Part 68 Appendix A.
    """

def requires_npdes_permit(discharge) -> bool:
    """
    NPDES — epa/npdes/_index.md
    True if facility discharges any pollutant from a point source to
    'waters of the United States'.
    Source: CWA §402; 40 CFR Part 122.
    """

def spcc_applicable(facility) -> bool:
    """
    SPCC — epa/npdes/_index.md
    True if facility has aboveground oil storage > 1,320 gallons total capacity
    (in containers ≥ 55 gal) OR > 42,000 gallons underground.
    Source: 40 CFR §112.1.
    """

def in_scope_epcra_302(facility) -> bool:
    """
    EPCRA §302 — epa/epcra/_index.md
    True if facility has Extremely Hazardous Substance (EHS) at or above
    Threshold Planning Quantity (TPQ).
    Source: 40 CFR Part 355.
    """

def performs_nadcap_commodity() -> bool:
    """
    NADCAP — nadcap/_index.md
    True if organization performs special processes (heat treat, NDT, welding,
    chemical processing, etc.) for aerospace/defense customers who require NADCAP.
    Source: Customer purchase order or supplier qualification requirements.
    """
```

---

## Scoping Matrix — Quick Reference

The following table shows which sectors/org types are in scope for each framework cluster. Use to quickly determine which fixtures to implement for a given organization profile.

| Org type | Frameworks in scope |
|---|---|
| US federal contractor (DoD, CUI) | NIST 800-171, CMMC, ITAR/EAR |
| Cloud service provider (federal) | FedRAMP, NIST 800-53 |
| Electric utility / ISO/RTO participant | NERC CIP |
| Healthcare provider / health plan / BA | HIPAA Security, HIPAA Privacy |
| Payment processor / merchant | PCI DSS |
| NY-licensed financial institution | NYDFS Part 500, GLBA |
| EU financial entity | DORA, PSD2 (if PSP) |
| Public company (SEC registrant) | SOX ITGC, SEC Cybersecurity |
| EU data controller / processor | GDPR |
| California consumer-facing business | CCPA/CPRA, COPPA (if under-13 users) |
| Medical device manufacturer | FDA QMSR, ISO 13485, EU MDR, ISO 14971, IEC 62304 |
| Pharmaceutical manufacturer | FDA 21 CFR 210/211, FDA FSMA (if food-drug) |
| Aerospace manufacturer / supplier | AS9100, NADCAP, ITAR/EAR |
| Automotive manufacturer / supplier | IATF 16949, TISAX |
| Chemical / industrial facility | EPA RMP, EPCRA, RCRA, NPDES/SPCC, OSHA PSM |
| General manufacturing | ISO 9001, ISO 14001, ISO 45001, OSHA 1910 |
| Food manufacturer | ISO 22000, FDA FSMA |
| Oil and gas | API Q1/Q2, EPA RMP, NERC CIP (if power generation) |
| Electronics manufacturer | IPC-A-610, NADCAP (if aerospace customer), RoHS/REACH (if EU market) |
| SWIFT network participant | SWIFT CSP |
| Broker-dealer | FINRA, SOX, SEC Cybersecurity |
| Nuclear power operator | NRC 10 CFR 73, NERC CIP (if grid-connected) |
| Critical pipeline operator | TSA Pipeline Directives |
| Any org — AI systems | EU AI Act (if deploying in EU), NIST AI RMF |
| Any org — web/software | WCAG 2.2 (if public-facing or US federal), COPPA (if under-13 users) |
