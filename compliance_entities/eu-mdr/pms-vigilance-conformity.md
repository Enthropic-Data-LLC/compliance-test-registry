# EU MDR / IVDR — Post-Market Surveillance, Vigilance, and Conformity Assessment

**Framework:** EU MDR 2017/745 (and IVDR 2017/746 by analogy)
**Clauses:** Articles 83–92 (PMS/PSUR/PMCF), Articles 87–89 (vigilance/serious incidents), Annex IX (conformity assessment pathway), Annex X (EU type examination), Article 61 + Annex XIV (clinical evaluation)
**Parent:** EU MDR Annex I (GSPR), ISO 14971, ISO 13485
**Confidence:** DETERMINISTIC-dominant (PMS plan existence, PSUR cadence, serious incident 15/30-day deadline, conformity assessment pathway selection)
**Last parsed:** 2026-05-21
**Applies to:** Legal manufacturers placing medical devices on the EU market; authorized representatives (for non-EU manufacturers); importers and distributors involved in the EU supply chain for medical devices classified under EU MDR Regulation 2017/745
**Trigger:** Placing a medical device (as defined in MDR Art. 2) on the EU market or putting it into service in the EU; applies regardless of manufacturer location — non-EU manufacturers must appoint an EU authorized representative
**Jurisdiction:** European Union; extraterritorial for non-EU manufacturers exporting to EU market; enforcement by national Competent Authorities and Notified Bodies
**Not applicable to:** In vitro diagnostic medical devices (Regulation 2017/746 IVDR applies instead); custom-made devices (Article 52 modified pathway); devices in clinical investigation only (Article 62 clinical investigation rules); devices for export outside EU with no EU market placement

---

## Scope pre-condition

```python
@pytest.fixture(autouse=True)
def eu_mdr_scope(entity_profile: dict):
    if not entity_profile.get("eu_mdr_in_scope", False):
        pytest.skip("EU MDR 2017/745 not in scope")
```

---

## Constants

```python
from datetime import timedelta

# PMS — Article 83
EU_MDR_PMS_PLAN_REQUIRED = True
EU_MDR_PMS_REPORT_REQUIRED_CLASS_I = True
EU_MDR_PSUR_REQUIRED_CLASSES = frozenset({"IIa", "IIb", "III"})

# PSUR update frequency — Article 86
EU_MDR_PSUR_MAX_INTERVAL_CLASS_III_IIB_DAYS = 365   # Class IIb + III: annual
EU_MDR_PSUR_MAX_INTERVAL_CLASS_IIA_DAYS = 730       # Class IIa: every 2 years

# Serious incident reporting deadlines — Article 87
EU_MDR_SERIOUS_INCIDENT_REPORT_DAYS_LIFE_THREATENING = 15
EU_MDR_SERIOUS_INCIDENT_REPORT_DAYS_OTHER = 30
EU_MDR_UNANTICIPATED_SERIOUS_DEVICE_PROBLEM_DAYS = 10  # §87(3) — imminent risk

# FSCA (Field Safety Corrective Action) — Article 88
EU_MDR_FSCA_NOTIFICATION_REQUIRED = True

# Conformity assessment by device class
EU_MDR_CLASS_I = "I"
EU_MDR_CLASS_IIA = "IIa"
EU_MDR_CLASS_IIB = "IIb"
EU_MDR_CLASS_III = "III"

# Clinical evaluation — Article 61 + Annex XIV
EU_MDR_CLINICAL_EVALUATION_REQUIRED_ALL_CLASSES = True
EU_MDR_CLINICAL_EVALUATION_REPORT_REQUIRED = True
EU_MDR_PMCF_PLAN_REQUIRED = True  # Post-Market Clinical Follow-up plan
```

---

## Articles 83–86 — Post-Market Surveillance (PMS)

**Overall: DETERMINISTIC — Pattern 1**

```python
import pytest
from datetime import date

class TestPostMarketSurveillance:
    """Articles 83–86 — PMS plan + PMS report (Class I) or PSUR (Class IIa/IIb/III)."""

    def test_pms_plan_exists_for_each_device(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        missing_pms = [p for p in programs if not p.get("pms_plan_exists", False)]
        assert not missing_pms, (
            f"Post-Market Surveillance (PMS) plan must exist for each device type "
            f"(EU MDR 2017/745 Article 84). "
            f"Missing: {[p['device_id'] for p in missing_pms]}"
        )

    def test_pms_plan_includes_proactive_data_collection(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        no_data_sources = [
            p for p in programs
            if p.get("pms_plan_exists", False)
            and not p.get("pms_plan_includes_proactive_data_sources", False)
        ]
        assert not no_data_sources, (
            f"PMS plan must include proactive data collection methods: literature review, "
            f"complaint analysis, vigilance data, registry data, clinical follow-up "
            f"(EU MDR 2017/745 Article 84). "
            f"Missing: {[p['device_id'] for p in no_data_sources]}"
        )

    def test_class_i_devices_have_pms_report(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        class_i = [p for p in programs if p.get("device_class") == EU_MDR_CLASS_I]
        no_pms_report = [
            p for p in class_i
            if not p.get("pms_report_exists", False)
        ]
        assert not no_pms_report, (
            f"Class I devices must have a PMS Report (separate from PSUR) "
            f"(EU MDR 2017/745 Article 85). "
            f"Missing: {[p['device_id'] for p in no_pms_report]}"
        )

    def test_psur_exists_for_class_iia_iib_iii(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        higher_class = [
            p for p in programs
            if p.get("device_class") in EU_MDR_PSUR_REQUIRED_CLASSES
        ]
        no_psur = [p for p in higher_class if not p.get("psur_exists", False)]
        assert not no_psur, (
            f"Class IIa, IIb, and III devices must have a Periodic Safety Update Report "
            f"(PSUR) (EU MDR 2017/745 Article 86). "
            f"Missing: {[p['device_id'] for p in no_psur]}"
        )

    def test_psur_updated_within_required_interval(
        self, controls_evidence: dict, reference_date: date
    ):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        for program in programs:
            if not program.get("psur_exists", False):
                continue
            device_class = program.get("device_class")
            last_updated = program.get("psur_last_updated_date")
            if last_updated is None:
                continue

            if device_class in (EU_MDR_CLASS_IIB, EU_MDR_CLASS_III):
                max_days = EU_MDR_PSUR_MAX_INTERVAL_CLASS_III_IIB_DAYS
            elif device_class == EU_MDR_CLASS_IIA:
                max_days = EU_MDR_PSUR_MAX_INTERVAL_CLASS_IIA_DAYS
            else:
                continue

            overdue = last_updated + timedelta(days=max_days) < reference_date
            assert not overdue, (
                f"PSUR for device '{program['device_id']}' (Class {device_class}) is overdue. "
                f"Last updated: {last_updated}; max interval: {max_days} days "
                f"(EU MDR 2017/745 Article 86)"
            )

    def test_pmcf_plan_exists_for_higher_risk_devices(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        higher_class = [
            p for p in programs
            if p.get("device_class") in (EU_MDR_CLASS_IIB, EU_MDR_CLASS_III)
        ]
        no_pmcf = [p for p in higher_class if not p.get("pmcf_plan_exists", False)]
        assert not no_pmcf, (
            f"Class IIb and Class III devices must have a Post-Market Clinical Follow-up "
            f"(PMCF) plan (EU MDR 2017/745 Article 83 + Annex XIV Part B). "
            f"Missing: {[p['device_id'] for p in no_pmcf]}"
        )
```

---

## Articles 87–89 — Vigilance (Serious Incident Reporting)

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestVigilance:
    """Articles 87–89 — Serious incidents reported to competent authority within required timeframe."""

    def test_serious_incidents_have_initial_report_within_deadline(
        self, controls_evidence: dict
    ):
        incidents = controls_evidence.get("eu_mdr_vigilance_incidents", [])
        for incident in incidents:
            if not incident.get("is_reportable_serious_incident", False):
                continue
            date_became_aware = incident.get("date_became_aware")
            date_initial_report = incident.get("date_initial_report_sent")
            if date_became_aware is None:
                continue

            is_life_threatening = incident.get("life_threatening_or_death", False)
            deadline_days = (
                EU_MDR_SERIOUS_INCIDENT_REPORT_DAYS_LIFE_THREATENING
                if is_life_threatening
                else EU_MDR_SERIOUS_INCIDENT_REPORT_DAYS_OTHER
            )

            deadline = date_became_aware + timedelta(days=deadline_days)
            late = (
                date_initial_report is None
                or date_initial_report > deadline
            )
            assert not late, (
                f"Serious incident '{incident['incident_id']}' initial report must be "
                f"submitted to competent authority within {deadline_days} calendar days "
                f"of becoming aware (EU MDR 2017/745 Article 87(1)). "
                f"Aware: {date_became_aware}; Deadline: {deadline}; "
                f"Reported: {date_initial_report}"
            )

    def test_unanticipated_serious_device_problems_reported_within_10_days(
        self, controls_evidence: dict
    ):
        incidents = controls_evidence.get("eu_mdr_vigilance_incidents", [])
        unanticipated = [
            i for i in incidents
            if i.get("unanticipated_serious_device_problem", False)
        ]
        for incident in unanticipated:
            date_became_aware = incident.get("date_became_aware")
            date_initial_report = incident.get("date_initial_report_sent")
            if date_became_aware is None:
                continue
            deadline = date_became_aware + timedelta(
                days=EU_MDR_UNANTICIPATED_SERIOUS_DEVICE_PROBLEM_DAYS
            )
            late = date_initial_report is None or date_initial_report > deadline
            assert not late, (
                f"Unanticipated serious device problem '{incident['incident_id']}' "
                f"must be reported within {EU_MDR_UNANTICIPATED_SERIOUS_DEVICE_PROBLEM_DAYS} "
                f"calendar days (EU MDR 2017/745 Article 87(3)). "
                f"Aware: {date_became_aware}; Deadline: {deadline}; "
                f"Reported: {date_initial_report}"
            )

    def test_fsca_notification_sent_before_or_concurrent_with_action(
        self, controls_evidence: dict
    ):
        fscas = controls_evidence.get("eu_mdr_field_safety_corrective_actions", [])
        not_notified = [
            f for f in fscas
            if not f.get("competent_authority_notified", False)
        ]
        assert not not_notified, (
            f"Field Safety Corrective Actions (FSCA) must be notified to competent "
            f"authorities before or simultaneously with the action (EU MDR Art. 88). "
            f"Not notified: {[f['fsca_id'] for f in not_notified]}"
        )

    def test_fsca_field_safety_notice_issued(self, controls_evidence: dict):
        fscas = controls_evidence.get("eu_mdr_field_safety_corrective_actions", [])
        no_fsn = [f for f in fscas if not f.get("field_safety_notice_issued", False)]
        assert not no_fsn, (
            f"Each FSCA must be accompanied by a Field Safety Notice (FSN) communicated "
            f"to affected users/customers (EU MDR 2017/745 Article 88(5)). "
            f"Missing FSN: {[f['fsca_id'] for f in no_fsn]}"
        )
```

---

## Article 61 + Annex XIV — Clinical Evaluation

**Overall: DETERMINISTIC (CER exists) + PARAMETERIZED (clinical data adequacy)**

```python
class TestClinicalEvaluation:
    """Article 61 — Clinical evaluation required for all devices; CER must be on file."""

    def test_clinical_evaluation_report_exists(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        missing_cer = [p for p in programs if not p.get("cer_exists", False)]
        assert not missing_cer, (
            f"Clinical Evaluation Report (CER) required for all device classes "
            f"(EU MDR 2017/745 Article 61). Missing: {[p['device_id'] for p in missing_cer]}"
        )

    def test_cer_kept_current_with_pms_data(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        stale_cer = [
            p for p in programs
            if p.get("cer_exists", False)
            and not p.get("cer_updated_with_pms_data", False)
        ]
        assert not stale_cer, (
            f"CER must be updated with post-market surveillance data throughout the "
            f"device lifecycle (EU MDR 2017/745 Article 61(11)). "
            f"Stale: {[p['device_id'] for p in stale_cer]}"
        )

    @pytest.mark.assumption(
        id="ASSUME-EUMDR-CER-001",
        description=(
            "Clinical data adequacy: sufficient clinical evidence includes direct clinical "
            "investigation data, literature on equivalent device, or clinical data from "
            "predecessor device; equivalence claim requires technical/biological/clinical "
            "equivalence demonstrated; for Class III and implantables, equivalence alone "
            "may not suffice — clinical investigation may be mandatory; adequacy of the "
            "clinical evidence is a Notified Body judgment and is PARAMETERIZED"
        ),
        approved_by="clinical_affairs_manager",
        review_date="2027-05-21",
    )
    def test_cer_documents_clinical_data_sources(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        no_data_sources = [
            p for p in programs
            if p.get("cer_exists", False)
            and not p.get("cer_documents_clinical_data_sources", False)
        ]
        assert not no_data_sources, (
            f"CER must document and appraise clinical data sources: clinical investigations, "
            f"literature review, equivalent device data (EU MDR Annex XIV Part A). "
            f"Missing: {[p['device_id'] for p in no_data_sources]}"
        )
```

---

## Annex IX / X — Conformity Assessment Pathway

**Overall: DETERMINISTIC — Pattern 1**

```python
class TestConformityAssessmentPathway:
    """Annex IX / X — Conformity assessment pathway appropriate for device class; NB certificate current."""

    def test_notified_body_involved_where_required(self, controls_evidence: dict):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        requires_nb = [
            p for p in programs
            if p.get("device_class") in {EU_MDR_CLASS_IIA, EU_MDR_CLASS_IIB, EU_MDR_CLASS_III}
        ]
        no_nb = [
            p for p in requires_nb
            if not p.get("notified_body_certificate_exists", False)
        ]
        assert not no_nb, (
            f"Class IIa, IIb, and III devices require Notified Body involvement in "
            f"conformity assessment (EU MDR 2017/745 Annex IX/X). "
            f"Missing NB certificate: {[p['device_id'] for p in no_nb]}"
        )

    def test_notified_body_certificates_not_expired(
        self, controls_evidence: dict, reference_date: date
    ):
        programs = controls_evidence.get("eu_mdr_production_programs", [])
        for program in programs:
            cert_expiry = program.get("nb_certificate_expiry_date")
            if cert_expiry is None:
                continue
            assert cert_expiry >= reference_date, (
                f"Notified Body certificate for device '{program['device_id']}' expired "
                f"on {cert_expiry}. CE marking requires a valid NB certificate "
                f"(EU MDR 2017/745 Article 55)"
            )

    def test_qms_certificate_covers_all_placed_device_types(
        self, controls_evidence: dict
    ):
        eu_mdr_qms = controls_evidence.get("eu_mdr_qms_certification", {})
        assert eu_mdr_qms.get("qms_certificate_scope_covers_all_device_types", False), (
            "QMS certificate (Annex IX Chapter I) must cover all device types placed on "
            "the EU market under that QMS (EU MDR 2017/745 Annex IX §2.2)"
        )
```

---

## Open assumptions

| ID | Clause | Summary | Review date |
|---|---|---|---|
| ASSUME-EUMDR-GSPR-001 | Annex I | GSPR adequacy: harmonised standard compliance is PARAMETERIZED; checklist existence is DETERMINISTIC | 2027-05-21 |
| ASSUME-EUMDR-CER-001 | Article 61 | Clinical evidence adequacy: existence of CER is DETERMINISTIC; adequacy is Notified Body judgment (PARAMETERIZED) | 2027-05-21 |
