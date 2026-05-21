#!/usr/bin/env python3
"""
Insert **Applies to / Trigger / Jurisdiction / Not applicable to** meta block
into every spec .md file (not _index.md, not README.md).

The block is inserted immediately after the **Last parsed:** line in the
existing header. If a file already contains '**Applies to:**' the file is
skipped (idempotent).

Run: python3 scripts/add_applicability.py  (from repo root)
"""

import re
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).parent.parent
ENTITIES  = REPO_ROOT / "compliance_entities"

# ---------------------------------------------------------------------------
# Applicability metadata — keyed on path prefix relative to compliance_entities/
# Each value is a 4-tuple: (applies_to, trigger, jurisdiction, not_applicable_to)
# ---------------------------------------------------------------------------

META: dict[str, tuple[str, str, str, str]] = {

    # ── SOC 2 ────────────────────────────────────────────────────────────────
    "soc2": (
        "Service organizations (SaaS, cloud providers, data centers, managed-service providers) whose services are relevant to user-entity controls",
        "Customer contract requirement; investor due-diligence; voluntary for competitive positioning; required when customers request a SOC 2 Type I or Type II report from their auditor",
        "United States (AICPA Trust Services Criteria); widely accepted internationally as equivalent to ISO 27001 attestation",
        "Internal IT departments; organizations that do not provide services to other companies; product companies without a service component",
    ),

    # ── PCI DSS ──────────────────────────────────────────────────────────────
    "pci-dss": (
        "Any organization that stores, processes, or transmits payment card data — merchants of all levels, payment processors, acquirers, issuers, and service providers in the card payment ecosystem",
        "Participation in the card payment ecosystem; card brand contracts (Visa, Mastercard, Amex, Discover, UnionPay); acquiring bank contractual requirement; SAQ level determined by annual transaction volume",
        "Global — enforced by card brands (Visa/Mastercard/Amex/Discover) and acquiring banks; no geographic restriction",
        "Organizations that never handle cardholder data and fully outsource all card processing to a PCI-DSS-compliant third party; SAQ A merchants processing only redirected card transactions",
    ),

    # ── HIPAA ────────────────────────────────────────────────────────────────
    "hipaa": (
        "Covered entities (healthcare providers who transmit health information electronically, health plans, healthcare clearinghouses) and their business associates who create, receive, maintain, or transmit PHI on behalf of a covered entity",
        "Creation, receipt, maintenance, or transmission of Protected Health Information (PHI) in connection with a covered function; business associate agreements (BAAs) flow down requirements to subcontractors",
        "United States; extraterritorial reach for foreign entities handling PHI of US patients or providing services to US covered entities",
        "Life insurers outside healthcare coverage; employers' employment records; education records covered by FERPA; de-identified data meeting Safe Harbor or Expert Determination standard; purely personal health records with no commercial healthcare function",
    ),

    # ── GDPR ─────────────────────────────────────────────────────────────────
    "gdpr": (
        "Any organization — regardless of location — that processes personal data of EU/EEA data subjects by offering goods or services to them or monitoring their behavior within the EU/EEA",
        "Offering goods or services to EU/EEA persons (Art. 3(2)(a)); monitoring behavior of EU/EEA persons within the EU/EEA (Art. 3(2)(b)); establishment in the EU/EEA (Art. 3(1))",
        "European Union / EEA; strong extraterritorial reach — applies to non-EU organizations targeting EU persons; enforced by national Data Protection Authorities and the EDPB",
        "Purely personal or household use (Art. 2(2)(c)); national security and law enforcement activities (Directive 2016/680 instead); anonymous data (not 'personal data' within GDPR meaning); deceased persons (in most member states)",
    ),

    # ── CCPA/CPRA ────────────────────────────────────────────────────────────
    "ccpa-cpra": (
        "For-profit businesses doing business in California that collect personal information from California consumers and meet at least one threshold: (1) annual gross revenue > $25M; (2) buy/sell/receive/share PI of ≥ 100,000 consumers or households per year; (3) derive ≥ 50% of annual revenue from selling or sharing consumer PI",
        "Any of the three thresholds above combined with doing business in California or with California consumers; extraterritorial reach — applies to businesses anywhere if they have California consumer relationships",
        "California, USA; applies wherever the business is located if California consumers are involved",
        "Non-profit organizations; government agencies; small businesses below all three thresholds; purely B2B data (partially exempt under CPRA through 2026); employee personal information collected in an employment context (limited exemption, under review)",
    ),

    # ── LGPD ─────────────────────────────────────────────────────────────────
    "lgpd": (
        "Any natural or legal person (public or private sector) that processes personal data: (1) in Brazil; (2) where the purpose of processing is to offer or provide goods/services to individuals in Brazil; or (3) where personal data from Brazil is processed",
        "Any of the three territorial nexus points above — broad extraterritorial scope similar to GDPR; applies to foreign organizations targeting Brazilian persons",
        "Brazil; extraterritorial reach via Art. 3 for organizations outside Brazil that process data of Brazilian residents",
        "Personal or family use with no commercial purpose; journalistic, artistic, academic, or security research with legal safeguards; government processing for national security or criminal investigation purposes",
    ),

    # ── ITAR / EAR ───────────────────────────────────────────────────────────
    "itar-ear": (
        "Any person or entity — US or foreign — that manufactures, exports, re-exports, transfers, or brokers: ITAR — defense articles and services on the US Munitions List (USML); EAR — dual-use items on the Commerce Control List (CCL). Includes 'deemed exports' (sharing controlled technology with foreign nationals in the US)",
        "Manufacturing, exporting, re-exporting, transferring, or brokering items on USML or CCL; employing or hosting foreign nationals with access to USML/CCL technology ('deemed export'); receiving technical data from a US person subject to ITAR/EAR",
        "United States extraterritorial — applies globally to US-origin items, technology, and software; enforced by DDTC (State, ITAR) and BIS (Commerce, EAR)",
        "Purely domestic transfers with no export or foreign-national access; EAR99 items with no applicable export control classification number; publicly available information (EAR §734.3(b)(3)); fundamental research (EAR §734.8); news media activities",
    ),

    # ── ISO 27001 ────────────────────────────────────────────────────────────
    "iso/27001": (
        "Any organization seeking ISO/IEC 27001 certification for its Information Security Management System (ISMS); scope is organization-defined (can be a department, product line, or whole entity)",
        "Voluntary certification; customer or procurement requirement (especially in EU, UK, financial services); NIS2 Directive in EU references ISO 27001 as an acceptable framework; organizational risk management decision",
        "Global — ISO/IEC international standard recognized worldwide; certifying bodies accredited per ISO/IEC 17021-1",
        "Mandatory compliance in isolation — ISO 27001 is a voluntary standard with no direct regulatory enforcement; certification applies only to the defined ISMS scope; does not replace sector-specific mandatory frameworks (HIPAA, PCI DSS, GLBA, etc.)",
    ),

    # ── FedRAMP ──────────────────────────────────────────────────────────────
    "fedramp": (
        "Cloud service providers (CSPs) offering cloud services to US federal agencies; SaaS, PaaS, and IaaS providers seeking FedRAMP Authorization to Operate (ATO)",
        "US federal agency contract or procurement requiring FedRAMP-authorized cloud services; FISMA requires federal agencies to use FedRAMP-authorized cloud offerings; federal CIO Council memo",
        "United States federal government; CSPs may be located anywhere globally but must meet US federal requirements",
        "On-premises federal IT systems (governed by FISMA/NIST 800-53 directly without FedRAMP process); commercial-only cloud products with no federal customers; cloud services offered exclusively to state/local government (StateRAMP is the counterpart)",
    ),

    # ── CMMC ─────────────────────────────────────────────────────────────────
    "cmmc": (
        "Defense contractors and subcontractors handling Controlled Unclassified Information (CUI) or Federal Contract Information (FCI) under Department of Defense (DoD) contracts and subcontracts",
        "DoD contract or subcontract containing DFARS clause 252.204-7012 (CUI) or 252.204-7021 (CMMC); prime contractors must flow down CMMC requirements to all subcontractors handling CUI; CMMC Level determined by CUI type and sensitivity",
        "United States Department of Defense supply chain; applies to US companies and foreign companies holding DoD contracts",
        "Commercial-only companies with no DoD contracts or subcontracts; DoD contracts not involving CUI or FCI (though basic contractor ethics and safeguarding under FAR 52.204-21 still apply); non-defense government contractors (civilian agencies use FISMA/800-171 directly without CMMC framework)",
    ),

    # ── NIST SP 800-53 ───────────────────────────────────────────────────────
    "nist/sp800-53": (
        "US federal agencies and their information systems (mandatory under FISMA); federal contractors and cloud service providers seeking FedRAMP authorization; state and local governments and critical infrastructure (by voluntary adoption or contract)",
        "Federal Information Security Modernization Act (FISMA) — mandatory for all federal agencies; FedRAMP authorization process; federal contract or grant requirement citing NIST 800-53; OMB Circular A-130",
        "United States federal government (mandatory); widely adopted internationally as a comprehensive control framework",
        "Private sector organizations not under federal contract (unless voluntarily adopted); non-federal systems outside FISMA scope; CMMC Level 1/2 contractors (use NIST 800-171, which is derived from 800-53 but has 110 requirements vs. 1000+)",
    ),

    # ── NIST SP 800-171 ──────────────────────────────────────────────────────
    "nist/sp800-171": (
        "Non-federal organizations (contractors, universities, research institutions) that process, store, or transmit Controlled Unclassified Information (CUI) in nonfederal information systems under US federal contracts or grants",
        "Federal contract or grant containing DFARS clause 252.204-7012 (DoD) or equivalent FAR clause; any contract where the government provides or the contractor generates CUI; CMMC Level 2 requires third-party assessment against NIST 800-171",
        "United States; extraterritorial — applies to foreign companies holding US federal contracts involving CUI; enforced through contract terms and DoD CMMC assessments",
        "Federal agencies (use NIST 800-53 instead); organizations with no federal contracts or grants; commercial transactions not involving CUI; EAR99 technology transfers (separate ITAR/EAR framework)",
    ),

    # ── NIST CSF 2.0 ─────────────────────────────────────────────────────────
    "nist/csf2": (
        "Any organization seeking a voluntary, risk-based cybersecurity framework — originally US critical infrastructure, now broadly adopted across all sectors and internationally",
        "Voluntary adoption; referenced in US executive orders (EO 13636, EO 14028) for critical infrastructure and federal contractors; cited in FFIEC examination guidance, TSA directives, and CISA advisories; international government adoption (UK NCSC, Australian ACSC)",
        "US origin; internationally adopted — referenced by ENISA (EU), NCSC (UK), ACSC (Australia), and others as equivalent or mapping framework",
        "Mandatory compliance in isolation — CSF 2.0 is voluntary guidance; serves as a mapping language to mandatory frameworks (NIST 800-53, ISO 27001, PCI DSS, etc.) rather than as an independent regulatory requirement",
    ),

    # ── NIST AI RMF ──────────────────────────────────────────────────────────
    "nist/ai-rmf": (
        "Any organization developing, deploying, procuring, or using AI systems; federal agencies and their contractors per US Executive Order 14110 (2023); organizations seeking to align with EU AI Act risk management requirements",
        "Voluntary adoption; US EO 14110 requires federal agencies to apply AI RMF for high-impact AI; EU AI Act Annex IV references NIST AI RMF as an aligned standard; organizational AI governance decision",
        "US origin; internationally aligned — NIST coordinated AI RMF with ISO/IEC 42001 (AI Management System) and EU AI Act technical standards",
        "Mandatory compliance in isolation — AI RMF 1.0 is voluntary guidance; no direct penalty for non-adoption except under EO 14110 for federal agencies; does not replace sector-specific AI regulations (EU AI Act, FDA AI/ML guidance, etc.)",
    ),

    # ── NERC CIP ─────────────────────────────────────────────────────────────
    "nerc/cip": (
        "Bulk Electric System (BES) owners, operators, and users in North America registered with NERC as a functional entity (Generator Owner/Operator, Transmission Owner/Operator, Balancing Authority, Reliability Coordinator, etc.) that own or operate BES Cyber Systems",
        "NERC registration as a functional entity + ownership/operation of BES Cyber Systems classified as High, Medium, or Low Impact per CIP-002; BES threshold: generation ≥ 20 MW, transmission ≥ 100 kV generally",
        "North America — United States, Canada, and portions of Mexico; enforced by NERC and eight Regional Entities (WECC, SERC, MRO, RFC, NPCC, FRCC, TRE, SPP RE); FERC oversees NERC in the US",
        "Distribution-only utilities operating below the BES voltage threshold; behind-the-meter generation below 20 MW; entities not registered with NERC; natural gas pipeline operators (TSA SD-02D instead); water utilities (AWIA instead)",
    ),

    # ── NERC Operations ──────────────────────────────────────────────────────
    "nerc/ops": (
        "Bulk Electric System registered entities whose functional registration makes them subject to specific operational reliability standards — Transmission Operators, Balancing Authorities, Generator Operators, Reliability Coordinators, and others per NERC functional model",
        "NERC registration as one or more functional entities per the NERC Functional Model; specific standards apply based on functional registration (e.g., COM-001 applies to Transmission Operators and Balancing Authorities but not Generator Owners)",
        "Same as NERC CIP — North America BES; enforced by NERC Regional Entities and FERC",
        "Same as NERC CIP — distribution-only utilities, behind-the-meter generation, unregistered entities; specific standards have applicability sections listing which functional entities are subject",
    ),

    # ── IEC 62443 ────────────────────────────────────────────────────────────
    "iec/62443": (
        "Three roles across the industrial automation and control system (IACS) lifecycle: asset owners (operators of OT/ICS systems), product suppliers (manufacturers of IACS components), and system integrators (designing/deploying IACS solutions) across all industrial sectors",
        "Customer/procurement contractual requirement (increasingly standard in oil and gas, energy, water, manufacturing supply chains); regulatory reference (NIS2 Directive in EU, NERC CIP, NRC guidance); voluntary adoption for OT security program maturity",
        "Global — IEC international standard; widely referenced by EU NIS2 Directive implementing acts, US CISA advisories, and sector-specific regulators",
        "Pure IT environments (ISO 27001 is the counterpart); consumer IoT outside industrial automation context (ETSI EN 303 645 applies instead); IEC 62443 does not replace sector-specific regulations (NERC CIP for BES, NRC for nuclear, TSA for pipelines)",
    ),

    # ── ISO 13485 ────────────────────────────────────────────────────────────
    "iso/13485": (
        "Medical device manufacturers, component suppliers, distributors, and service providers involved in the design, development, production, storage, distribution, installation, or servicing of medical devices",
        "Regulatory requirement in many major markets — EU MDR/IVDR references ISO 13485; FDA QMSR (21 CFR 820) aligns to ISO 13485:2016; Health Canada, TGA (Australia), PMDA (Japan) recognize ISO 13485 certification; customer requirement in device supply chains",
        "Global — ISO standard; certification recognized by regulatory bodies in EU, Canada, Australia, Japan, and many other markets; FDA accepts ISO 13485 certification for QMSR compliance determination",
        "Non-medical-device manufacturers; software products not meeting the medical device definition under MDR/IVDR or FDA; purely research/investigational devices not entering commercial distribution",
    ),

    # ── ISO 14971 ────────────────────────────────────────────────────────────
    "iso/14971": (
        "Medical device manufacturers responsible for risk management throughout the device lifecycle — design, development, production, post-market surveillance",
        "Required by EU MDR Annex I General Safety and Performance Requirements (GSPRs); FDA guidance on device risk management references ISO 14971; ISO 13485 Clause 7.1 requires a risk management process; harmonized standard in EU, Canada, Australia, Japan",
        "Global — harmonized with EU MDR Essential Requirements, referenced by FDA, Health Canada, TGA, PMDA, and most major medical device regulatory frameworks worldwide",
        "Non-medical-device products (ISO 31000 is the general enterprise risk management standard); IVD devices (IEC 62366 usability + ISO 14971 risk management both apply); food/drug products not classified as devices",
    ),

    # ── EU MDR ───────────────────────────────────────────────────────────────
    "eu-mdr": (
        "Legal manufacturers placing medical devices on the EU market; authorized representatives (for non-EU manufacturers); importers and distributors involved in the EU supply chain for medical devices classified under EU MDR Regulation 2017/745",
        "Placing a medical device (as defined in MDR Art. 2) on the EU market or putting it into service in the EU; applies regardless of manufacturer location — non-EU manufacturers must appoint an EU authorized representative",
        "European Union; extraterritorial for non-EU manufacturers exporting to EU market; enforcement by national Competent Authorities and Notified Bodies",
        "In vitro diagnostic medical devices (Regulation 2017/746 IVDR applies instead); custom-made devices (Article 52 modified pathway); devices in clinical investigation only (Article 62 clinical investigation rules); devices for export outside EU with no EU market placement",
    ),

    # ── FDA 21 CFR Part 11 ───────────────────────────────────────────────────
    "fda/21cfr11": (
        "Any FDA-regulated organization (pharmaceutical, biotechnology, medical device, food, cosmetics, tobacco) that uses electronic records and/or electronic signatures in operations where FDA predicate rules require records or signatures",
        "Use of electronic records in lieu of paper records required by FDA predicate regulations (21 CFR 211 for pharma, 21 CFR 820/QMSR for devices, 21 CFR 123 for seafood HACCP, etc.); use of electronic signatures on records subject to FDA requirements",
        "United States; extraterritorial — applies to foreign manufacturers producing products for US distribution where electronic systems support FDA-regulated records",
        "Electronic systems used purely internally with no FDA-required record function; non-FDA-regulated industries; paper-based systems (Part 11 does not apply); purely research data not submitted to FDA and not required by predicate rule",
    ),

    # ── FDA 21 CFR 210/211 ───────────────────────────────────────────────────
    "fda/21cfr210-211": (
        "Manufacturers of finished pharmaceutical drug products (human and veterinary) distributed in US interstate commerce; contract manufacturing organizations (CMOs) producing drugs for US-market distribution; API manufacturers to the extent their processes become part of finished dosage forms",
        "Manufacturing finished drug products for introduction into US interstate commerce; FDA establishment registration under 21 CFR 207 triggers cGMP applicability; applies to domestic and foreign drug manufacturers exporting to the US",
        "United States; strong extraterritorial reach — FDA inspects and can refuse admission of drug products from non-compliant foreign facilities",
        "Investigational drugs in Phase 1 clinical trials (modified cGMP under 21 CFR 312); bulk API (covered under 21 CFR 211 Subpart B primarily for in-process controls); veterinary biologics (USDA); blood products (21 CFR 606); tissue/cellular products (21 CFR 1271)",
    ),

    # ── FDA QMSR ─────────────────────────────────────────────────────────────
    "fda/qmsr": (
        "Manufacturers of medical devices for the US market — Class I, II, and III device manufacturers and specification developers; component manufacturers whose components become part of a finished medical device",
        "Manufacturing or specification development for medical devices requiring FDA establishment registration under 21 CFR 807; QMSR (21 CFR 820) applies to finished device manufacturers; effective date February 2026 (aligning to ISO 13485:2016)",
        "United States; extraterritorial — applies to foreign device manufacturers with devices distributed in the US",
        "Devices for export only (21 CFR 801.58); HCT/Ps regulated under 21 CFR 1271; combination products (additional requirements under 21 CFR 3 and 4); investigational devices in IDE studies (modified requirements)",
    ),

    # ── IATF 16949 ───────────────────────────────────────────────────────────
    "iatf/16949": (
        "Automotive parts manufacturers and their direct and sub-tier suppliers providing production parts, accessories, or service parts to automotive original equipment manufacturers (OEMs)",
        "Customer requirement from automotive OEMs (Ford, GM, Stellantis, BMW, VW Group, Toyota, Honda, etc.) mandating IATF 16949 certification for supply chain qualification; required for PPAP (Production Part Approval Process) submission to most OEMs",
        "Global — IATF (International Automotive Task Force) standard; recognized by all major automotive OEMs worldwide through their customer-specific requirements (CSRs)",
        "Non-automotive manufacturing; automotive distributors or dealers without manufacturing; service-only companies; aftermarket software and electronics not in direct OEM supply chain; companies supplying raw materials only (e.g., steel mills) rather than processed parts",
    ),

    # ── AS9100 ───────────────────────────────────────────────────────────────
    "as9100": (
        "Aviation, space, and defense (AS&D) manufacturers and their supply chains — Tier 1 and Tier 2 suppliers to aerospace OEMs providing parts, assemblies, or services for aircraft, spacecraft, or defense systems",
        "Customer requirement from aerospace OEMs (Boeing, Airbus, Lockheed Martin, Raytheon, Northrop Grumman, etc.) or prime contractors mandating AS9100 Rev D certification; required for NADCAP special process accreditation; FAR/DFARS supply chain flow-down",
        "Global — IAQG (International Aerospace Quality Group) standard with regional bodies: AAQG (Americas), EAQG (Europe), JIAQG (Asia-Pacific)",
        "Non-aerospace manufacturers; MRO organizations (AS9110 applies instead); design-only organizations (AS9100 scope applies differently); companies providing services to aerospace without making parts (may use AS9100 or AS9120 for distributors)",
    ),

    # ── API Q1 ───────────────────────────────────────────────────────────────
    "api/q1": (
        "Manufacturers of oil and gas equipment and service companies seeking the API Monogram license or Q1 certification; suppliers to oil and gas operators requiring API Q1 as a supply chain qualification",
        "API Monogram license requirement — organizations must hold Q1 certification to use the API Monogram on qualifying products; customer contract requirement from oil and gas operators; required for API-licensed products (wellheads, valves, drilling equipment, etc.)",
        "Global — API (American Petroleum Institute) standard; internationally recognized in oil and gas industry globally",
        "Upstream oil and gas operators (they impose the requirement on suppliers but do not self-certify); non-oil-and-gas manufacturers; service companies not supplying equipment or processes to the oil and gas sector",
    ),

    # ── NADCAP ───────────────────────────────────────────────────────────────
    "nadcap": (
        "Suppliers performing special processes for aerospace and defense prime contractors — heat treatment, non-destructive testing (NDT), welding, chemical processing, coatings, electronics manufacturing, composites, and other NADCAP commodity categories",
        "Customer requirement from aerospace prime contractors (Boeing, Airbus, Lockheed Martin, Northrop Grumman, Raytheon, etc.) mandating NADCAP accreditation for specific commodity categories; AS9100 quality management system is a prerequisite; accreditation managed by PRI (Performance Review Institute)",
        "Global — PRI (Performance Review Institute) manages NADCAP; accepted by all major aerospace primes worldwide through NADCAP subscriber agreements",
        "Non-special-process manufacturing; general machining or fabrication not in a NADCAP commodity category; suppliers not in aerospace/defense supply chains; design-only engineering firms without manufacturing operations",
    ),

    # ── IPC-A-610 ────────────────────────────────────────────────────────────
    "ipc": (
        "Electronics assembly manufacturers, contract electronics manufacturers (CEMs), and their inspection personnel for acceptability of electronic assemblies; customers specifying acceptance criteria for PCB assemblies",
        "Customer contract requirement — widely used as the default reference standard for electronics assembly quality; military and defense contracts citing IPC-A-610 as the acceptance standard; IPC Certified IPC Specialist (CIS) and CIS-I programs for inspection personnel",
        "Global — IPC (Association Connecting Electronics Industries) standard; universally recognized in electronics manufacturing across North America, Europe, and Asia",
        "Bare PCB fabrication (IPC-6012 or IPC-A-600 applies instead); component-level manufacturing; non-electronic assembly manufacturing; RF/microwave assemblies (IPC-7711/7721 for rework)",
    ),

    # ── IEC 62304 ────────────────────────────────────────────────────────────
    "iec/62304": (
        "Medical device manufacturers that incorporate software as part of a medical device (embedded, standalone Software as a Medical Device (SaMD), or software controlling a device); IVD manufacturers with software components",
        "Required by EU MDR/IVDR for software-containing devices; FDA's software-related guidance documents reference IEC 62304 as the recognized standard; ISO 13485 design controls (Clause 7.3) require a software development process for devices with software",
        "Global — harmonized with EU MDR/IVDR, referenced by FDA, Health Canada, TGA, PMDA, and most major medical device regulatory frameworks",
        "Software with no medical purpose (wellness apps, administrative hospital software); off-the-shelf general-purpose software used in healthcare settings but not classified as a device; pure hardware medical devices with no software component",
    ),

    # ── ISO 9001 ─────────────────────────────────────────────────────────────
    "iso/9001": (
        "Any organization in any sector seeking ISO 9001 certification for its Quality Management System; required in many supply chains as a baseline QMS qualification",
        "Customer or procurement contract requirement; voluntary certification for competitive positioning; foundation standard upon which sector-specific QMS standards are built (AS9100, IATF 16949, ISO 13485 all incorporate ISO 9001)",
        "Global — ISO international standard; certification bodies accredited per ISO/IEC 17021-1",
        "No mandatory requirement in any major jurisdiction — ISO 9001 is a voluntary standard; sector-specific QMS standards (AS9100, IATF 16949, ISO 13485) supersede ISO 9001 certification scope in their respective sectors",
    ),

    # ── ISO 45001 ────────────────────────────────────────────────────────────
    "iso/45001": (
        "Any organization seeking to implement or certify an Occupational Health and Safety Management System (OHSMS); required in some supply chains (construction, mining, manufacturing, oil and gas) as a contractor qualification criterion",
        "Voluntary certification; contractual requirement in construction, oil and gas, and manufacturing supply chains; government procurement requirement in some countries; organizational OHS risk management decision; replaces OHSAS 18001 (retired 2021)",
        "Global — ISO international standard; recognized in all major markets",
        "ISO 45001 does not replace mandatory OHS regulations — OSHA standards (29 CFR 1910, 1926) in the US and equivalent national regulations impose binding requirements independent of ISO 45001 certification; ISO 45001 is the management system framework, not the regulatory floor",
    ),

    # ── ISO 14001 ────────────────────────────────────────────────────────────
    "iso/14001": (
        "Any organization seeking to implement or certify an Environmental Management System (EMS); required in some government procurement processes and supply chains with environmental performance criteria",
        "Voluntary certification; EU/UK government procurement criteria; customer requirement in automotive (IATF 16949 references), aerospace, and chemical supply chains; organizational environmental risk management decision",
        "Global — ISO international standard",
        "ISO 14001 does not replace mandatory environmental regulations — EPA regulations (Clean Air Act, RCRA, Clean Water Act) and equivalent national laws impose binding requirements independent of ISO 14001 certification; ISO 14001 is a management system framework, not regulatory compliance",
    ),

    # ── ISO 50001 ────────────────────────────────────────────────────────────
    "iso/50001": (
        "Any organization seeking to implement an Energy Management System (EnMS); large enterprises in the EU that may use ISO 50001 certification as an alternative to mandatory energy audits under the EU Energy Efficiency Directive (EED)",
        "Voluntary certification; EU Energy Efficiency Directive Article 8 — large enterprises (> 250 employees or > €50M turnover and > €43M balance sheet) can use ISO 50001 certified EnMS in lieu of mandatory quadrennial energy audit; customer/government procurement requirement in some jurisdictions",
        "Global — ISO international standard; particularly relevant in EU where EED creates regulatory driver",
        "Small and medium enterprises below EU EED large-enterprise thresholds (SMEs are not subject to mandatory energy audit obligations, so ISO 50001 has no regulatory driver for them unless voluntarily adopted); organizations where energy costs are immaterial to operations",
    ),

    # ── RoHS / REACH ─────────────────────────────────────────────────────────
    "rohs-reach": (
        "RoHS: manufacturers, importers, and distributors placing electrical and electronic equipment (EEE) on the EU market. REACH: any company that manufactures, imports, or uses chemical substances in the EU above threshold quantities, or places articles containing SVHCs on the EU market",
        "RoHS: placing EEE on the EU market — applies to virtually all consumer and industrial electronics sold in the EU. REACH: manufacturing/importing ≥ 1 tonne/year of a substance in the EU; supplying articles containing SVHCs > 0.1% by weight",
        "European Union; extraterritorial for non-EU manufacturers — products must comply before entering EU market; enforced by national market surveillance authorities",
        "RoHS: military/defense equipment (Art. 2(3)(b)); large fixed industrial installations; implantable active medical devices; space equipment; some specific product categories in Annex II. REACH: substances used solely in national defense; radioactive substances (Euratom); certain polymers (registration exemption); waste (regulated separately under WFD)",
    ),

    # ── COPPA ────────────────────────────────────────────────────────────────
    "coppa": (
        "Operators of commercial websites, online services, and mobile apps (1) directed to children under 13, OR (2) with actual knowledge they are collecting personal information from children under 13",
        "Site or service 'directed to children' (determined by content, advertising, music, animated characters, celebrities appealing to children, etc.); OR actual knowledge of under-13 users through age gate failures, user self-disclosure, or parent notifications",
        "United States; extraterritorial reach — applies to foreign operators targeting US children; enforced by FTC under 16 CFR Part 312",
        "Non-commercial websites and services; general audience services with no child-directed content and no actual knowledge of under-13 users; educational institutions using the school-authority exception; services exclusively for persons 13 and older with credible age verification",
    ),

    # ── PIPEDA / Law 25 ──────────────────────────────────────────────────────
    "pipeda": (
        "Private-sector organizations that collect, use, or disclose personal information in the course of commercial activities in Canada; foreign organizations collecting personal information from Canadian residents; Quebec Law 25 additionally covers organizations doing business in Quebec",
        "Commercial activity in Canada involving personal information of individuals; collecting data from Canadian residents; Quebec Law 25 triggers: any private-sector organization 'doing business' in Quebec — includes foreign organizations with Quebec customers",
        "Canada federal (PIPEDA); Quebec (Law 25 / Act 25 amending the Act respecting the protection of personal information in the private sector, phased implementation 2022–2023); Alberta and BC have substantially similar provincial laws",
        "Federal government institutions (Privacy Act 1985 applies instead); employee personal information in non-federally-regulated workplaces in provinces with substantially similar legislation (BC, AB, QC); purely personal/family use; non-commercial activities of non-profit organizations in some contexts",
    ),

    # ── APPI ─────────────────────────────────────────────────────────────────
    "appi": (
        "Business operators handling personal information in Japan; foreign businesses that provide goods or services to persons in Japan or use personal information of persons in Japan — regardless of where the business is located",
        "Handling personal information of persons in Japan in the course of business; providing goods or services targeting Japan; 2022 amendment removed the 5,000-person threshold — now applies to all business operators handling any personal information",
        "Japan; extraterritorial reach for foreign businesses targeting Japanese persons; enforced by Personal Information Protection Commission (PPC); sector-specific guidelines from FSA (financial), MHLW (healthcare), METI (general industry)",
        "Government agencies (separate Act on Protection of Personal Information Held by Administrative Organs); purely personal or family use with no commercial purpose; anonymous information that is irreversibly de-identified (outside APPI definition of personal information); academic research with appropriate safeguards (limited exemption)",
    ),

    # ── NIST SP 800-82 ───────────────────────────────────────────────────────
    "nist/sp800-82": (
        "Any organization operating Operational Technology (OT), Industrial Control Systems (ICS), SCADA, DCS, PLC, or RTU systems that: (1) adopts SP 800-82 by organizational policy; (2) is subject to a binding directive referencing SP 800-82 (TSA SD-02D, NRC RG 5.71, CISA advisories); or (3) requires it by contract",
        "Policy adoption for OT security program; TSA Security Directive SD-02D (pipeline operators) references SP 800-82 practices; NRC RG 5.71 references NIST 800-53 (which SP 800-82 tailors for OT); federal/DoD contracts requiring NIST OT security standards; CISA critical infrastructure advisories",
        "US origin; internationally referenced — ENISA, NCSC (UK), and national CERTs worldwide align OT guidance to SP 800-82 and IEC 62443",
        "As a standalone mandatory requirement — SP 800-82 is NIST guidance, not a regulation; it becomes effectively mandatory only when incorporated by reference into a binding regulatory directive or contract; does not replace NERC CIP (electric), TSA SD-02D (pipeline), or NRC 10 CFR 73.54 (nuclear)",
    ),

    # ── TSA Pipeline ─────────────────────────────────────────────────────────
    "tsa/pipeline": (
        "Owners and operators of hazardous liquid pipelines, natural gas transmission pipelines, and liquefied natural gas (LNG) facilities that TSA has specifically designated in writing as critical infrastructure",
        "TSA written designation letter — TSA applies risk-based criteria (throughput volume, geographic significance, strategic interconnectedness) to designate specific pipeline operators; designation is company-specific and confidential; not all pipeline operators receive designation",
        "United States; enforced by TSA under 49 U.S.C. §114(l)(2); CISA coordinates cyber incident notification receipt",
        "Non-designated pipeline operators (TSA has not issued a designation letter); highway and motor carrier operations (separate TSA cybersecurity directives SD-02-2021 and SD-01-2021); water and wastewater utilities (EPA AWIA instead); electric utilities (NERC CIP instead); natural gas distribution (local distribution companies at distribution level)",
    ),

    # ── NRC 10 CFR 73.54 ─────────────────────────────────────────────────────
    "nrc/10cfr73": (
        "Commercial nuclear power reactor licensees holding operating licenses under 10 CFR Part 50 or combined licenses under 10 CFR Part 52; rule applies to all digital computer and communication systems and networks associated with safety, security, emergency preparedness, and support systems (Critical Digital Assets — CDAs)",
        "NRC license to operate a commercial nuclear power reactor in the United States; rule effective March 27, 2009; implementation schedules negotiated per licensee; ongoing compliance verified through NRC inspection procedure IP 71130.10",
        "United States; enforced by the U.S. Nuclear Regulatory Commission (NRC) through routine inspections and enforcement actions",
        "Research and test reactors (different regulatory framework); nuclear fuel cycle facilities (10 CFR Part 74); nuclear materials licensees (Agreement State regulation in many cases); decommissioned reactors (modified applicability); non-power reactor licensees",
    ),

    # ── FFIEC ────────────────────────────────────────────────────────────────
    "ffiec": (
        "Federally regulated US financial institutions — national banks (OCC), federal savings associations (OCC), state member banks (Federal Reserve), bank holding companies (Federal Reserve), state nonmember banks (FDIC), federal credit unions (NCUA); and their technology service providers (TSPs) examined through their institutional clients",
        "Federal charter or federal deposit insurance triggering examination by an FFIEC member agency (OCC, FDIC, Federal Reserve, NCUA, CFPB); examination benchmarks apply during IT Safety-and-Soundness examinations; findings result in MRAs/MRIAs that carry practical enforcement force",
        "United States; FFIEC handbooks are the examination framework for federally regulated institutions; state-chartered non-member banks are examined by state authorities but commonly use FFIEC guidance as the reference standard",
        "State-chartered non-member banks not subject to federal examination (though FFIEC guidance is widely referenced); non-bank financial institutions not regulated by FFIEC member agencies; insurance companies (state regulated); fintech companies not holding a federal banking charter or deposit insurance",
    ),

    # ── FINRA ────────────────────────────────────────────────────────────────
    "finra": (
        "FINRA-member broker-dealers registered with the SEC under Section 15 of the Securities Exchange Act of 1934; their associated persons (registered representatives, principals, and other individuals subject to FINRA jurisdiction)",
        "SEC registration as a broker-dealer requires FINRA membership (mandatory for US broker-dealers); FINRA membership agreement subjects firms and their registered persons to FINRA rules",
        "United States; enforced by FINRA Department of Enforcement; SEC has oversight authority over FINRA as an SRO",
        "Investment advisers registered with the SEC or states (RIA-only, not broker-dealers); commodities futures brokers (CFTC/NFA regulated instead); securities exchanges; banks not also registered as broker-dealers; foreign broker-dealers operating only outside the US",
    ),

    # ── Basel III / BCBS 239 ─────────────────────────────────────────────────
    "basel": (
        "Internationally active banks subject to Basel III capital requirements under national implementation rules; G-SIBs (globally systemically important banks on the FSB annual list) for mandatory BCBS 239 compliance; D-SIBs by national regulator direction",
        "National regulator designation as 'internationally active bank' triggering Basel III final rule; FSB annual G-SIB list (published each November) for BCBS 239 mandatory compliance; implemented via Fed/OCC/FDIC final rules (US), CRR/CRD (EU), PRA rules (UK)",
        "Global — enforced through national banking regulators; US: Federal Reserve/OCC/FDIC; EU: ECB/EBA/national competent authorities; UK: PRA; Switzerland: FINMA",
        "Community banks and smaller non-internationally-active institutions (national regulators apply simplified capital frameworks, e.g., US Community Bank Leverage Ratio); non-bank financial institutions; insurance companies (Solvency II for EU insurers); broker-dealers (net capital rule instead of Basel III)",
    ),

    # ── PSD2 ─────────────────────────────────────────────────────────────────
    "psd2": (
        "Payment service providers (PSPs) licensed in the EU/EEA: credit institutions, e-money institutions, payment institutions, account information service providers (AISPs), payment initiation service providers (PISPs); account-servicing payment service providers (ASPSPs) additionally subject to open banking API requirements",
        "EU/EEA PSP license from a national competent authority; offering payment services to EU/EEA residents; non-EU PSPs targeting EU customers must obtain authorization in an EU/EEA member state",
        "European Union / EEA; national competent authorities (NCAs) enforce PSD2; EBA provides technical standards and guidelines; PSD3 / PSR proposed package (2023) pending adoption as of 2026",
        "Purely intra-group payment transactions between affiliated entities; limited network instruments (e.g., single-retailer gift cards, limited-use prepaid instruments); technical service providers that do not at any time enter into possession of funds; purely commercial agent arrangements where agent acts exclusively for payer or payee",
    ),

    # ── SOX ──────────────────────────────────────────────────────────────────
    "sox": (
        "SEC-registered publicly traded companies — US domestic issuers and foreign private issuers (FPIs) listed on US stock exchanges; external auditors registered with the PCAOB; public accounting firms auditing SEC registrants",
        "SEC registration under the Securities Exchange Act of 1934 (ongoing reporting) or Securities Act of 1933 (initial registration/IPO triggers SOX); listing on NYSE, NASDAQ, or other US national securities exchange; PCAOB registration required for auditors of SEC registrants",
        "United States; extraterritorial — FPIs listed on US exchanges must comply (though with some modified SOX requirements, e.g., management assessment only, no auditor attestation for smaller FPIs); PCAOB registered audit firms worldwide",
        "Private companies (no SEC registration); non-profit and government organizations; foreign companies not listed on US exchanges and not registered with the SEC; de-listed companies (SOX Section 404 compliance obligation ends); SEC registrants that are non-accelerated filers (limited Section 404(b) exemptions)",
    ),

    # ── GLBA ─────────────────────────────────────────────────────────────────
    "glba": (
        "Financial institutions subject to FTC or federal banking regulator jurisdiction that engage in 'financial activities' and collect nonpublic personal information (NPI) from consumers — including banks, insurance companies, securities firms, mortgage brokers, tax preparers, auto dealers with financing, and non-bank financial services",
        "Being a 'financial institution' under GLBA §6809(3) engaged in financial activities as defined in the Bank Holding Company Act §4(k); scope is broad and includes many non-traditional financial service providers; FTC Safeguards Rule enforcement for non-bank financial institutions",
        "United States; FTC enforces for non-bank financial institutions; federal banking regulators (OCC, FDIC, Federal Reserve) enforce for banks; SEC and CFTC for broker-dealers and investment advisers in their respective jurisdictions",
        "Non-financial businesses with no offering of financial products or services; consumers acting in personal capacity; financial institutions solely in the business of providing financial services to businesses (not retail consumers); government agencies",
    ),

    # ── NYDFS 500 ────────────────────────────────────────────────────────────
    "nydfs/500": (
        "Any entity operating under a license, registration, charter, certificate, permit, or similar authorization under New York Banking Law, Insurance Law, or Financial Services Law — including state-chartered banks, insurance companies, licensed lenders, mortgage servicers, money transmitters, virtual currency businesses, and others regulated by NYDFS",
        "DFS license, registration, or authorization in New York; foreign banking organizations with a New York branch or agency; any entity required to obtain a DFS license to conduct financial services business in New York State",
        "New York State, USA; NYDFS enforces §23 NYCRR Part 500; one of the most prescriptive US state cybersecurity regulations — frequently used as a model by other states",
        "Entities with fewer than 10 employees, less than $5M in gross revenue, and less than $10M in year-end total assets (limited exemption under §500.19); federal credit unions (federally chartered, not DFS licensed); entities exclusively regulated by federal banking agencies without DFS licensing",
    ),

    # ── SEC Cybersecurity ────────────────────────────────────────────────────
    "sec/cybersecurity": (
        "SEC-registered public companies — domestic issuers required to file on Forms 10-K and 8-K; foreign private issuers required to file equivalent disclosures on Form 20-F and Form 6-K",
        "SEC registration under the Securities Exchange Act of 1934; material cybersecurity incident triggers 8-K/6-K disclosure within 4 business days of materiality determination; annual 10-K/20-F requires cybersecurity risk management, strategy, and governance disclosures",
        "United States; SEC enforcement; foreign private issuers have modified disclosure obligations (6-K instead of 8-K, 20-F instead of 10-K) but are subject to equivalent cybersecurity disclosure requirements",
        "Private companies (no SEC reporting obligation); smaller reporting companies below SEC thresholds (received extended compliance timelines); government-sponsored enterprises; non-profit organizations",
    ),

    # ── SWIFT CSP ────────────────────────────────────────────────────────────
    "swift/csp": (
        "All SWIFT member institutions with a direct connection to the SWIFT network — banks, broker-dealers, fund managers, custodians, and other financial institutions using SWIFT for financial messaging; service bureaus providing SWIFT connectivity on behalf of member institutions",
        "SWIFT network connectivity (live connection) — all connected institutions must self-attest annually against the Customer Security Controls Framework (CSCF) mandatory controls; self-attestation is required in the KYC Registry; non-attestation results in escalation to counterparties and supervisors",
        "Global — SWIFT is an international cooperative headquartered in Belgium; CSCF applies to all member institutions worldwide regardless of jurisdiction",
        "Correspondent banking relationships where a non-SWIFT institution accesses SWIFT only through a SWIFT-connected correspondent (the downstream institution must comply, not the non-SWIFT upstream); entities that have disconnected from SWIFT",
    ),

    # ── TISAX ────────────────────────────────────────────────────────────────
    "tisax": (
        "Automotive supply chain companies that exchange sensitive information with participating automotive OEMs (VW Group, BMW, Mercedes-Benz, Porsche, etc.) — including suppliers handling vehicle data, prototype/pre-series vehicle information, personal data in automotive context, or classified OEM intellectual property",
        "OEM contractual requirement specifying TISAX assessment with a defined Assessment Level (AL1, AL2, or AL3 based on data sensitivity); TISAX is required for suppliers exchanging information above the sensitivity threshold defined in the VDA ISA questionnaire",
        "Global — ENX Association manages the TISAX program; primarily European OEMs require it but assessment results shared across all ENX participants worldwide",
        "Non-automotive companies; automotive suppliers that do not exchange sensitive data above the TISAX trigger threshold with OEM TISAX participants; pure service companies with no intellectual property or vehicle data handling",
    ),

    # ── DORA ─────────────────────────────────────────────────────────────────
    "dora": (
        "Financial entities in the EU: credit institutions, payment institutions, e-money institutions, investment firms, insurance/reinsurance undertakings, crypto-asset service providers, central counterparties, and others listed in DORA Art. 2(1); and their critical ICT third-party service providers (CTPPs)",
        "EU financial sector license or authorization; providing ICT services to EU financial entities above the materiality threshold for critical/important functions; applicable from January 17, 2025",
        "European Union; enforced by national competent authorities (ECB/EBA for banks, ESMA for investment firms, EIOPA for insurance); ESAs oversee CTPP oversight framework",
        "Microenterprises (< 10 employees, < €2M balance sheet/turnover) — simplified DORA regime; non-financial EU entities (unless providing ICT services to financial entities as a CTPP); non-EU financial entities with no EU nexus; ICT intragroup arrangements (partially modified treatment)",
    ),

    # ── UK GDPR ──────────────────────────────────────────────────────────────
    "uk-gdpr": (
        "Organizations established in the UK that process personal data; organizations outside the UK that process personal data of UK residents in connection with offering goods/services to them or monitoring their behavior in the UK",
        "UK establishment (any office, branch, or other stable arrangement in the UK); offering goods or services to UK persons; monitoring behavior of UK persons within the UK; applies post-Brexit under the retained EU GDPR (UK GDPR) + Data Protection Act 2018",
        "United Kingdom (England, Scotland, Wales, Northern Ireland); extraterritorial reach — applies to non-UK organizations targeting UK persons; enforced by the Information Commissioner's Office (ICO)",
        "Processing exclusively for national security or defense purposes (separate legislation); law enforcement processing (Part 3 of the Data Protection Act 2018 instead); intelligence services; purely personal or household use; deceased persons (generally)",
    ),

    # ── NRC 10 CFR 50 ────────────────────────────────────────────────────────
    "nrc/10cfr50": (
        "Commercial nuclear power plant licensees holding operating licenses (OL) or combined licenses (COL) under 10 CFR Part 50 or Part 52; construction permit holders; nuclear power plant applicants during the licensing process",
        "NRC license to operate or construct a commercial nuclear power plant in the United States; Appendix B (QA) applies from earliest design phases; event reporting, maintenance rule, fire protection, and ISI/IST requirements apply throughout the operating license period",
        "United States; enforced by the U.S. Nuclear Regulatory Commission through routine inspections, resident inspectors, and enforcement actions including Notices of Violation, Confirmatory Action Letters, and civil penalties",
        "Research and test reactors (10 CFR Part 50 applies partially but with different technical requirements); non-power utilization facilities; fuel cycle facilities (10 CFR Part 70); nuclear materials licensees; decommissioned reactors (10 CFR Part 50 Subpart E DECON/SAFSTOR requirements differ)",
    ),

    # ── NRC 10 CFR 26 ────────────────────────────────────────────────────────
    "nrc/10cfr26": (
        "Nuclear power plant licensees and their contractors and vendors whose employees perform safety-sensitive duties at nuclear power facilities — reactor operators, maintenance personnel, security personnel, and other individuals subject to fitness-for-duty (FFD) programs",
        "NRC license to operate a nuclear power plant; applies to all individuals who are granted or who seek unescorted access to a protected area or who perform safety-sensitive duties at a licensed facility; contractors and vendors must comply via licensee FFD programs",
        "United States; enforced by the U.S. Nuclear Regulatory Commission",
        "Individuals working only in administrative or business areas without unescorted access to protected areas; non-nuclear industrial workplaces; research reactors (limited applicability); fuel cycle facilities (different NRC rules apply)",
    ),

    # ── OSHA 1910 ────────────────────────────────────────────────────────────
    "osha/1910": (
        "General industry employers in the United States with one or more employees — covers virtually all private-sector general industry operations including manufacturing, warehousing, retail, service industries, and healthcare; specific standards apply based on the industry activities conducted",
        "Employing workers in general industry operations in the US; OSHA jurisdiction covers all private-sector employers in states under Federal OSHA; specific standards triggered by specific hazards or processes (PSM requires covered processes above threshold quantities; HAZWOPER triggered by hazardous waste operations; confined space requires permit-required spaces, etc.)",
        "United States federal — enforced by OSHA (Occupational Safety and Health Administration) under the OSH Act of 1970; 22 states and 2 territories operate OSHA-approved State Plans covering public and/or private sector workers",
        "Construction industry (29 CFR 1926 applies instead); agriculture (29 CFR 1928); maritime (29 CFR 1915 ship repairing, 1917 marine terminals, 1918 longshoring); self-employed individuals with no employees; federal government agencies (Executive Order 12196 covers federal workers separately); public-sector employees in states without State Plan coverage",
    ),

    # ── OSHA 1926 ────────────────────────────────────────────────────────────
    "osha/1926": (
        "Construction industry employers and contractors in the United States with one or more employees performing construction, alteration, demolition, or repair work — applies to general contractors, subcontractors, and specialty trade contractors",
        "Employing workers who perform construction work as defined in 29 CFR 1910.12 — construction, alteration, or repair including painting and decorating; applies to the entire construction site and all employers at the site; owner-controlled insurance programs (OCIPs) require contractor compliance",
        "United States federal — same OSHA jurisdiction as 29 CFR 1910; State Plan states apply their equivalent construction safety standards",
        "General industry operations at completed facilities (29 CFR 1910 applies instead); design/engineering firms with no field construction workers; homeowners performing personal home improvement work without employees; shipbuilding and repair (29 CFR 1915 applies instead)",
    ),

}

# Some files are in subdirectories that match more specific keys — resolve by
# finding the most-specific matching prefix.
def get_meta(path: pathlib.Path) -> tuple[str, str, str, str] | None:
    rel = path.relative_to(ENTITIES)
    parts = rel.parts[:-1]  # strip filename
    # Try progressively shorter prefixes (most-specific first)
    for length in range(len(parts), 0, -1):
        key = "/".join(parts[:length])
        if key in META:
            return META[key]
    return None


MD_BLOCK_TEMPLATE = """\
**Applies to:** {applies_to}
**Trigger:** {trigger}
**Jurisdiction:** {jurisdiction}
**Not applicable to:** {not_applicable_to}"""

PY_BLOCK_TEMPLATE = """\
# Applies to: {applies_to}
# Trigger: {trigger}
# Jurisdiction: {jurisdiction}
# Not applicable to: {not_applicable_to}"""

LAST_PARSED_RE  = re.compile(r"(\*\*Last parsed:\*\* .+)")
LAST_UPDATED_RE = re.compile(r"(\*\*Last updated:\*\* .+)")

# Matches the last line of a leading Python-comment header block (before first import/blank line
# that leads into code). We anchor on the blank line that separates comments from imports.
_COMMENT_HEADER_RE = re.compile(r"((?:^#[^\n]*\n)+)(\nimport |\nimport\t)", re.MULTILINE)


def process_file(path: pathlib.Path) -> str:
    text = path.read_text(encoding="utf-8")
    if "**Applies to:**" in text or "# Applies to:" in text:
        return "skip"

    meta = get_meta(path)
    if meta is None:
        return "no-meta"

    applies_to, trigger, jurisdiction, not_applicable = meta

    # 1. Try **Last parsed:** (new-style markdown headers)
    md_block = MD_BLOCK_TEMPLATE.format(
        applies_to=applies_to, trigger=trigger,
        jurisdiction=jurisdiction, not_applicable_to=not_applicable,
    )
    new_text, n = LAST_PARSED_RE.subn(r"\1\n" + md_block, text, count=1)
    if n:
        path.write_text(new_text, encoding="utf-8")
        return "updated"

    # 2. Try **Last updated:** (older markdown-header style)
    new_text, n = LAST_UPDATED_RE.subn(r"\1\n" + md_block, text, count=1)
    if n:
        path.write_text(new_text, encoding="utf-8")
        return "updated"

    # 3. Python-comment-only header — insert comment block before first `import`
    py_block = PY_BLOCK_TEMPLATE.format(
        applies_to=applies_to, trigger=trigger,
        jurisdiction=jurisdiction, not_applicable_to=not_applicable,
    )
    m = _COMMENT_HEADER_RE.search(text)
    if m:
        # Insert the py_block (with a leading blank-ish separator) at end of comment block
        insert_pos = m.start(2)  # position of the "\nimport" part
        new_text = text[:insert_pos] + "\n#\n" + py_block + text[insert_pos:]
        path.write_text(new_text, encoding="utf-8")
        return "updated"

    # 4. Markdown files with a first `---` section separator (after header fields)
    #    Insert the md_block on the line just before the `---`.
    hr_m = re.search(r"\n(---\n)", text)
    if hr_m:
        insert_pos = hr_m.start(1)  # insert at the `---` line start
        new_text = text[:insert_pos] + md_block + "\n\n" + text[insert_pos:]
        path.write_text(new_text, encoding="utf-8")
        return "updated"

    return "no-last-parsed"


def main():
    spec_files = [
        p for p in ENTITIES.rglob("*.md")
        if p.name not in ("_index.md", "README.md")
    ]
    spec_files.sort()

    counts = {"updated": 0, "skip": 0, "no-meta": 0, "no-last-parsed": 0}
    for f in spec_files:
        result = process_file(f)
        counts[result] += 1
        if result not in ("updated", "skip"):
            print(f"  {result:20s}  {f.relative_to(REPO_ROOT)}")

    print(f"\nDone — updated: {counts['updated']}  "
          f"already done: {counts['skip']}  "
          f"no meta: {counts['no-meta']}  "
          f"no last-parsed: {counts['no-last-parsed']}")


if __name__ == "__main__":
    main()
