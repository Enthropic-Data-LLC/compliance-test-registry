# FDA 21 CFR Part 11 — Electronic Records and Electronic Signatures: Core Requirements

**Registry path:** `/regulation-registry/FDA/21CFR11/ElectronicRecords-ESig/`
**Regulation:** 21 CFR Part 11 (FDA, 1997 final rule; 2003 Guidance reduces enforcement scope)
**Last parsed:** 2026-05-20
**Applies to:** Any FDA-regulated organization (pharmaceutical, biotechnology, medical device, food, cosmetics, tobacco) that uses electronic records and/or electronic signatures in operations where FDA predicate rules require records or signatures
**Trigger:** Use of electronic records in lieu of paper records required by FDA predicate regulations (21 CFR 211 for pharma, 21 CFR 820/QMSR for devices, 21 CFR 123 for seafood HACCP, etc.); use of electronic signatures on records subject to FDA requirements
**Jurisdiction:** United States; extraterritorial — applies to foreign manufacturers producing products for US distribution where electronic systems support FDA-regulated records
**Not applicable to:** Electronic systems used purely internally with no FDA-required record function; non-FDA-regulated industries; paper-based systems (Part 11 does not apply); purely research data not submitted to FDA and not required by predicate rule
**Overall confidence:** HIGH for DETERMINISTIC requirements (audit trail, signature components, two-component enforcement, FDA certification); MEDIUM for PARAMETERIZED (system validation, training)
**Covers:** §11.10(b)–(k) [closed system controls], §11.50 [signature manifestations], §11.70 [signature/record linking], §11.100 [esig uniqueness + FDA cert], §11.200 [two-component signatures], §11.300 [password/token controls]

---

## Scope Pre-Condition

21 CFR Part 11 applies only to electronic records used in lieu of paper records required by predicate rules (21 CFR Parts 58, 210, 211, 820, etc.). The scope fixture gates all tests:

```python
@pytest.fixture(autouse=True)
def require_part11_scope(system_scope: dict):
    if not system_scope.get("records_subject_to_predicate_rule"):
        pytest.skip(
            "Records not subject to Part 11 — no predicate rule citation on file. "
            "Attest predicate rule applicability before tests are enforcing."
        )
```

---

## §11.10(e) — Audit Trail (HIGH — DETERMINISTIC)

### Source excerpt

> (e) Use of secure, computer-generated, time-stamped audit trails to independently record the date and time of operator entries and actions that create, modify, or delete electronic records. Record changes shall not obscure previously recorded information. Such audit trail documentation shall be retained for a period at least as long as that required for the subject electronic records and shall be available for agency review and copying.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Electronic record is created, modified, or deleted | DETERMINISTIC |
| Obligation | Audit trail entry generated automatically at each event | DETERMINISTIC |
| Audit trail properties | Secure; computer-generated; time-stamped; cannot be modified or deleted by users | DETERMINISTIC |
| Required fields | Operator ID; date/time; nature of change (create/modify/delete); previous value preserved | DETERMINISTIC |
| Retention | At least as long as the associated electronic record (per predicate rule) | DETERMINISTIC |
| Availability | Available for FDA inspection and copying on request | DETERMINISTIC |

**Assumption (ASSUME-21CFR11-001):** Audit trail is compliant when: (1) every create, modify, and delete action on a predicate-rule record generates an audit entry automatically — no manual bypass; (2) audit entry contains: operator ID, action timestamp (UTC or timestamped with timezone), action type, record identifier, old value (for modifications), new value; (3) audit trail records are stored separately from the record data and cannot be altered, deleted, or overwritten by regular users — no DELETE permission on audit table; (4) retention period equals or exceeds the predicate rule retention period for the associated record type; (5) audit trail can be exported in human-readable format for FDA inspection within a reasonable time.

**Overall: DETERMINISTIC → Pattern 1**

---

## §11.10(d) — Access Controls (HIGH — DETERMINISTIC)

### Source excerpt

> (d) Limiting system access to authorized individuals.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | System processes electronic records subject to predicate rules | DETERMINISTIC |
| Obligation | Only authorized individuals can access the system | DETERMINISTIC |
| Implementation | Unique user ID + password (§11.200) or biometric for electronic signatures; user account management | DETERMINISTIC |

**Assumption (ASSUME-21CFR11-002):** Access controls are compliant when: (1) every user has a unique user ID — no shared accounts; (2) user access is role-based — users can only access functions appropriate to their job role; (3) account provisioning requires documented authorization (supervisor or system owner approval); (4) terminated employee accounts disabled within 24 hours of departure; (5) periodic access review conducted at minimum annually — unauthorized or excess access revoked; (6) privileged access (admin, configuration changes) is a separate account or separately authorized role.

**Overall: DETERMINISTIC → Pattern 1**

---

## §11.10(b) + (c) — Record Copies and Archival (DETERMINISTIC)

### Source excerpts

> (b) The ability to generate accurate and complete copies of records in both human readable and electronic form suitable for inspection, review, and copying by the agency.
>
> (c) Protection of records to enable their accurate and ready retrieval throughout the records retention period.

**Assumption (ASSUME-21CFR11-003):** Record copy and archival controls are compliant when: (1) system can generate human-readable output (print or display) of any electronic record on demand; (2) system can generate an electronic copy in a transferable format (PDF, XML, or other format accessible without the original application); (3) archived records are protected against accidental deletion, corruption, and ransomware — offline/immutable backup required; (4) records remain retrievable throughout the full retention period — storage media migration performed before media EOL; (5) record integrity verification (checksum/hash) detects silent corruption.

**Overall: DETERMINISTIC → Pattern 1**

---

## §11.50 — Signature Manifestations (DETERMINISTIC)

### Source excerpt

> (a) Signed electronic records shall contain information associated with the signing that clearly indicates all of the following:
> (1) The printed name of the signer;
> (2) The date and time when the signature was executed;
> (3) The meaning (such as review, approval, responsibility, or authorship) associated with the signature.
>
> (b) The items identified in paragraphs (a)(1), (a)(2), and (a)(3) of this section shall be subject to the same controls as for electronic records and shall be included as part of any human readable form of the electronic record (such as electronic display or printout).

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Electronic record carries an electronic signature | DETERMINISTIC |
| Obligation | Signature displays three elements: name, date/time, meaning | DETERMINISTIC |
| Integrity | Signature elements subject to same controls as the record | DETERMINISTIC |

**Assumption (ASSUME-21CFR11-004):** Signature manifestations are compliant when: (1) every electronic signature record contains three elements: printed name of signer (not just username), timestamp (date and time), and meaning (one of: approved, reviewed, authored, verified, or equivalent domain-specific meaning); (2) these three elements appear on any human-readable rendering of the record (print/export); (3) the meaning element is pre-defined and selected from a controlled vocabulary — free-text meaning is not acceptable unless constrained by a controlled list.

**Overall: DETERMINISTIC → Pattern 1**

---

## §11.70 — Signature/Record Linking (DETERMINISTIC)

### Source excerpt

> Electronic signatures and handwritten signatures executed to electronic records shall be linked to their respective electronic records to ensure that the signatures cannot be excised, copied, or otherwise transferred to falsify an electronic record by ordinary means.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Condition | Electronic signature is applied to an electronic record | DETERMINISTIC |
| Obligation | Signature is permanently and inseparably linked to the record; link detects any alteration | DETERMINISTIC |

**Assumption (ASSUME-21CFR11-005):** Signature/record linking is compliant when: (1) the signature record includes a reference to the specific record version it was applied to (foreign key, hash, or document ID + version); (2) any subsequent modification to the record after signature is detectable — either the system prevents post-signature modification entirely, or modification creates a new version requiring a new signature; (3) the link cannot be broken by ordinary means — not stored in an easily-editable user-accessible field; (4) if using cryptographic hash: hash of the signed record is stored with the signature and recomputed to verify link integrity on access.

**Implementation note:** Database-level foreign key link (signature table references record table PK) satisfies the "cannot be excised by ordinary means" requirement for closed enterprise systems. Cryptographic linking via document hash provides stronger protection and is preferred for records transmitted outside the closed system.

**Overall: DETERMINISTIC → Pattern 1**

---

## §11.100 — Electronic Signature General Requirements (DETERMINISTIC)

### Source excerpt

> (a) Each electronic signature shall be unique to one individual and shall not be reused by, or reassigned to, anyone else.
>
> (b) Before an organization establishes, assigns, certifies, or otherwise sanctions an individual's electronic signature, or any element of such electronic signature, the organization shall verify the identity of the individual.
>
> (c)(1) Persons using electronic signatures shall, prior to or at the time of such use, certify to the agency that the electronic signatures in their system, used on or after August 20, 1997, are intended to be the legally binding equivalent of traditional handwritten signatures.
>
> (c)(2) The certification shall be submitted in paper form and signed with a traditional handwritten signature, to the office of the agency...

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Uniqueness | Each esig unique to one individual; not reused or reassigned | DETERMINISTIC |
| Identity verification | Verify identity before granting esig authority | DETERMINISTIC |
| FDA certification | Written certification submitted to FDA (one-time, per organization) | DETERMINISTIC |

**Assumption (ASSUME-21CFR11-006):** §11.100 requirements are compliant when: (1) each user has a unique esig ID that has never been assigned to another user (no re-use); (2) identity verification at hire: performed through employment-level identity check (I-9, government ID, or equivalent) — organization documents verification method; (3) FDA certification: written §11.100(c) certification letter submitted to FDA via certified mail or equivalent and retained on file; (4) re-certification not required unless the original certification is superseded; (5) certification covers all systems in the organization using electronic signatures.

**Overall: DETERMINISTIC → Pattern 1**

---

## §11.200 — Electronic Signature Components (DETERMINISTIC)

### Source excerpt

> (a) Electronic signatures that are not based upon biometrics shall:
> (1) Employ at least two distinct identification components such as an identification code and password.
> (i) When an individual executes a series of signings during a single, continuous period of controlled system access, the first signing shall be executed using all electronic signature components; subsequent signings shall be executed using at least one electronic signature component that is only executable by, and designed to be used only by, the individual.
> (ii) When an individual executes one or more signings not performed during a single period of controlled system access, each signing shall be executed using all electronic signature components.

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Non-biometric signature | Requires at least two identification components (e.g., user ID + password) | DETERMINISTIC |
| Single continuous session | First signing: both components; subsequent signings: at least one component exclusive to the user | DETERMINISTIC |
| New/non-continuous session | Every signing: all components required | DETERMINISTIC |
| Biometric signature | Designed so no other individual can use it | DETERMINISTIC |

**Assumption (ASSUME-21CFR11-007):** Two-component signature enforcement is compliant when: (1) non-biometric electronic signature requires entry of user ID + password (or ID + PIN, or other two-component combination); (2) for a single continuous session: first signature prompts both components; subsequent signatures in the same session may prompt only the password (the exclusive component); (3) session breaks: if the user logs out, navigates away, or the session expires, the next signature requires both components again; (4) the system enforces this — it cannot be bypassed by the user; (5) biometric signature implementation is designed to be individual-specific (fingerprint, iris, signature dynamics).

**Overall: DETERMINISTIC → Pattern 1**

---

## §11.300 — Controls for Identification Codes/Passwords (DETERMINISTIC for existence; PARAMETERIZED for adequacy)

### Source excerpt

> (a) Maintaining the uniqueness of each combined identification code and password, such that no two individuals have the same combination of identification code and password.
>
> (b) Ensuring that identification code and password issuances are periodically checked, recalled, or revised (e.g., to cover such events as password aging, equipment changes, and alterations in job responsibilities).
>
> (c) Following loss management procedures to electronically deauthorize lost, stolen, missing, or otherwise potentially compromised tokens, cards, and other devices that bear or generate identification code or password information, and to issue temporary or permanent replacements using suitable, rigorous controls.
>
> (d) Use of transaction safeguards to prevent unauthorized use of passwords and/or identification codes, and to detect and report in an automated fashion any attempts at their unauthorized use to the system security unit...
>
> (e) Initial and periodic testing of devices...

**Assumption (ASSUME-21CFR11-008):** Password/token controls are compliant when: (1) no two active users share the same user ID + password combination; (2) passwords are periodically verified for currency — password expiration policy in place (review period per organizational policy; 90-day maximum is common industry practice for non-MFA systems); (3) tokens or hardware devices immediately deactivated when reported lost/stolen — deactivation occurs within 4 hours of report; (4) automated account lockout after repeated failed attempts; (5) failed login attempts generate a security alert; (6) password issuance for new employees follows secure distribution (temporary password, first-use change required); (7) password history enforced — users cannot immediately reuse recent passwords.

**Overall: DETERMINISTIC for uniqueness and deactivation → Pattern 1; PARAMETERIZED for password aging adequacy → Pattern 2**

---

## Test specifications

### YAML spec — 21 CFR Part 11 core controls

```yaml
spec_id: 21CFR11-CORE-001
framework: FDA 21 CFR Part 11
pattern: 1  # Primary; Pattern 2 for PARAMETERIZED items
sections:
  - §11.10(b) (record copies)
  - §11.10(c) (archival)
  - §11.10(d) (access controls)
  - §11.10(e) (audit trail)
  - §11.50 (signature manifestations)
  - §11.70 (signature/record linking)
  - §11.100 (uniqueness + FDA certification)
  - §11.200 (two-component signatures)
  - §11.300 (password/token controls)
subject: Electronic records and electronic signatures in FDA-regulated systems
pre_conditions:
  - records_subject_to_predicate_rule == true
obligations:
  - audit_trail: every create/modify/delete logged; non-alterable; retained with record; operator ID + timestamp + old value
  - access_controls: unique user IDs; role-based; terminated = deactivated within 24h; annual review
  - record_copies: human-readable and electronic copy available for FDA inspection
  - archival: records retrievable throughout retention; integrity-verified; offline backup
  - signature_manifestations: name + date/time + meaning on every signed record
  - signature_link: permanent link; alteration detectable; cannot be excised
  - uniqueness: each esig unique to one person; identity verified before grant; FDA certification on file
  - two_component: user ID + password; all components at first signing per session; new session = all components
  - password_controls: unique combinations; periodic checks; immediate deactivation on loss/theft; lockout on failed attempts
evidence:
  - audit_log_config (non-alterable table; write-only; retained with records)
  - user_accounts (unique IDs; no shared accounts; role assignments; deactivation log)
  - esig_records (name + timestamp + meaning fields; link to record version)
  - fda_certification_letter (§11.100(c) letter on file with submission confirmation)
  - esig_workflow_config (two-component enforcement; session handling)
  - password_policy (expiration; history; lockout; complexity)
```

### Python test file

```python
# tests/fda_21cfr11/test_21cfr11_core.py
"""
FDA 21 CFR Part 11 Core Electronic Records and Electronic Signature Tests.

Sections: §11.10(b)(c)(d)(e), §11.50, §11.70, §11.100, §11.200, §11.300
Assumptions: ASSUME-21CFR11-001 through ASSUME-21CFR11-008
"""
import pytest
from datetime import datetime, timedelta, timezone
from typing import Any

TERMINATED_ACCOUNT_DISABLE_HOURS = 24
LOST_TOKEN_DEACTIVATE_HOURS = 4
ACCESS_REVIEW_MAX_DAYS = 365
REQUIRED_SIGNATURE_FIELDS = {"signer_name", "signing_timestamp", "signature_meaning"}
CONTROLLED_MEANING_VOCABULARY = {"approved", "reviewed", "authored", "verified", "released", "rejected"}


@pytest.fixture(autouse=True)
def require_part11_scope(system_scope: dict[str, Any]):
    """Gate: records must be subject to a predicate rule before Part 11 tests are enforcing."""
    if not system_scope.get("records_subject_to_predicate_rule"):
        pytest.skip(
            "No predicate rule citation on file — Part 11 tests informational only. "
            "Attest predicate rule applicability before enforcing."
        )


# ── §11.10(e) Audit Trail ─────────────────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-21CFR11-001",
    description="Audit trail: every create/modify/delete event logged; non-alterable; retained with record",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_audit_trail_configured_non_alterable(audit_log_config: dict[str, Any]):
    """§11.10(e): Audit trail must be secure, computer-generated, and non-alterable by users."""
    assert audit_log_config.get("computer_generated"), (
        "Audit trail must be computer-generated — manual audit entries are not compliant"
    )
    assert not audit_log_config.get("user_delete_permitted"), (
        "Audit trail records must not be deletable by users — Part 11 §11.10(e)"
    )
    assert not audit_log_config.get("user_modify_permitted"), (
        "Audit trail records must not be modifiable by users — Part 11 §11.10(e)"
    )
    assert audit_log_config.get("timestamps_utc_or_timezone_stamped"), (
        "Audit trail timestamps must be UTC or include timezone offset — §11.10(e)"
    )


@pytest.mark.assumption(
    id="ASSUME-21CFR11-001",
    description="Audit entries contain: operator ID, timestamp, action type, record ID, old value",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_audit_entries_contain_required_fields(audit_log_sample: list[dict[str, Any]]):
    """§11.10(e): Each audit entry must contain all required fields."""
    required_fields = {"operator_id", "action_timestamp", "action_type", "record_id"}
    modification_fields = required_fields | {"previous_value"}

    incomplete = []
    for entry in audit_log_sample:
        fields = set(entry.keys())
        if entry.get("action_type") in {"modify", "delete"}:
            missing = modification_fields - fields
        else:
            missing = required_fields - fields
        if missing:
            incomplete.append(f"{entry.get('entry_id', '?')}: missing fields {missing}")

    assert not incomplete, (
        f"Audit entries missing required fields: {incomplete}"
    )


@pytest.mark.assumption(
    id="ASSUME-21CFR11-001",
    description="Audit trail retained at least as long as associated record per predicate rule",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_audit_trail_retention_equals_record_retention(
    retention_policy: dict[str, Any],
):
    """§11.10(e): Audit trail retention must equal or exceed the associated record retention period."""
    record_types = retention_policy.get("record_types", [])
    violations = []

    for rt in record_types:
        record_retention_days = rt.get("record_retention_days", 0)
        audit_retention_days = rt.get("audit_trail_retention_days", 0)
        if audit_retention_days < record_retention_days:
            violations.append(
                f"{rt['record_type']}: audit trail retention ({audit_retention_days}d) < "
                f"record retention ({record_retention_days}d)"
            )

    assert not violations, (
        f"Audit trail retention is shorter than record retention for: {violations}"
    )


# ── §11.10(d) Access Controls ────────────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-21CFR11-002",
    description="Unique user IDs: no shared accounts; terminated accounts disabled within 24h",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_no_shared_user_accounts(user_accounts: list[dict[str, Any]]):
    """§11.10(d) / §11.100(a): Each user must have a unique ID — no shared accounts permitted."""
    shared_accounts = [
        acct for acct in user_accounts
        if acct.get("shared_account") or acct.get("generic_account")
    ]
    # Shared service/system accounts are separate from user accounts
    shared_accounts = [a for a in shared_accounts if not a.get("is_system_account")]

    assert not shared_accounts, (
        f"Shared user accounts found — Part 11 §11.100(a) prohibits shared electronic signatures: "
        f"{[a['username'] for a in shared_accounts]}"
    )


@pytest.mark.assumption(
    id="ASSUME-21CFR11-002",
    description="Terminated employees' accounts disabled within 24 hours of departure",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_terminated_employees_accounts_disabled_timely(
    termination_records: list[dict[str, Any]],
):
    """§11.10(d): Terminated employee accounts must be disabled within 24 hours."""
    late_disables = []

    for record in termination_records:
        termination_date = record.get("termination_date")
        account_disabled_date = record.get("account_disabled_date")
        if termination_date is None:
            continue
        if account_disabled_date is None:
            late_disables.append(f"{record['employee_id']}: account never disabled")
        else:
            hours_elapsed = (account_disabled_date - termination_date).total_seconds() / 3600
            if hours_elapsed > TERMINATED_ACCOUNT_DISABLE_HOURS:
                late_disables.append(
                    f"{record['employee_id']}: account disabled {hours_elapsed:.1f}h after termination "
                    f"(max {TERMINATED_ACCOUNT_DISABLE_HOURS}h)"
                )

    assert not late_disables, (
        f"Terminated employee accounts not disabled within {TERMINATED_ACCOUNT_DISABLE_HOURS}h: "
        f"{late_disables}"
    )


# ── §11.50 Signature Manifestations ─────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-21CFR11-004",
    description="Signed records display: signer name (full), date/time, meaning from controlled vocabulary",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_signature_records_contain_required_manifestation_fields(
    esig_records: list[dict[str, Any]],
):
    """§11.50(a): Every signed record must display signer name, date/time, and meaning."""
    incomplete = []

    for esig in esig_records:
        fields = {k for k, v in esig.items() if v is not None}
        missing = REQUIRED_SIGNATURE_FIELDS - fields
        if missing:
            incomplete.append(f"esig {esig.get('esig_id', '?')}: missing {missing}")
            continue
        # Meaning must be from controlled vocabulary
        meaning = esig.get("signature_meaning", "")
        if meaning.lower() not in CONTROLLED_MEANING_VOCABULARY:
            incomplete.append(
                f"esig {esig.get('esig_id', '?')}: meaning {meaning!r} not in controlled vocabulary "
                f"{CONTROLLED_MEANING_VOCABULARY}"
            )

    assert not incomplete, (
        f"Signature records with incomplete manifestation fields: {incomplete}"
    )


# ── §11.70 Signature/Record Linking ─────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-21CFR11-005",
    description="Signatures are permanently linked to record version; link detects alteration",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_signature_record_links_are_intact(esig_records: list[dict[str, Any]]):
    """§11.70: Electronic signatures must be permanently and detectably linked to their records."""
    broken_links = []

    for esig in esig_records:
        record_ref = esig.get("record_id") or esig.get("record_hash")
        if not record_ref:
            broken_links.append(
                f"esig {esig.get('esig_id', '?')}: no link to a specific record — "
                "§11.70 requires permanent linking"
            )
            continue
        if esig.get("link_integrity_verified") is False:
            broken_links.append(
                f"esig {esig.get('esig_id', '?')}: link integrity check failed — "
                "record or signature may have been altered after signing"
            )

    assert not broken_links, (
        f"Signature/record link integrity failures: {broken_links}"
    )


# ── §11.100 Uniqueness and FDA Certification ─────────────────────────────────

def test_fda_certification_on_file(esig_system_config: dict[str, Any]):
    """§11.100(c): §11.100(c) FDA certification letter must be on file before electronic signatures are used."""
    cert = esig_system_config.get("fda_11100c_certification")
    assert cert is not None, (
        "§11.100(c) FDA certification letter not on file — required before electronic signatures "
        "are used as the legal equivalent of handwritten signatures"
    )
    assert cert.get("submission_confirmed"), (
        "§11.100(c) certification must be submitted to FDA — submission confirmation required"
    )
    assert cert.get("covers_current_systems"), (
        "§11.100(c) certification must cover all systems currently using electronic signatures"
    )


@pytest.mark.assumption(
    id="ASSUME-21CFR11-006",
    description="Identity verified at hire/before esig grant; verification method documented",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_identity_verified_before_esig_granted(user_accounts: list[dict[str, Any]]):
    """§11.100(b): Organization must verify identity before granting electronic signature authority."""
    unverified = [
        acct["user_id"] for acct in user_accounts
        if acct.get("has_esig_authority")
        and not acct.get("identity_verified_at_hire")
    ]

    assert not unverified, (
        f"Users with electronic signature authority without documented identity verification: {unverified}"
    )


# ── §11.200 Two-Component Signature Enforcement ──────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-21CFR11-007",
    description="Non-biometric esig requires two components; first signing per session uses both; re-login resets",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_two_component_signature_enforced(esig_system_config: dict[str, Any]):
    """§11.200(a): Non-biometric electronic signatures must require at least two identification components."""
    esig_type = esig_system_config.get("esig_type", "non_biometric")

    if esig_type == "biometric":
        assert esig_system_config.get("biometric_individual_only_design"), (
            "§11.200(b): Biometric signature must be designed so no other individual can use it"
        )
    else:
        # Non-biometric: two-component required
        assert esig_system_config.get("two_component_required"), (
            "§11.200(a): Non-biometric electronic signature must require two identification components "
            "(e.g., user ID + password)"
        )
        assert esig_system_config.get("first_signing_requires_both_components"), (
            "§11.200(a)(1): First signing in a session must use all components"
        )
        assert esig_system_config.get("session_break_resets_to_both_components"), (
            "§11.200(a)(2): After a session break (logout, timeout), next signing must use all components"
        )


# ── §11.300 Password/Token Controls ─────────────────────────────────────────

@pytest.mark.assumption(
    id="ASSUME-21CFR11-008",
    description="Unique ID+password combinations; lockout on failed attempts; immediate deactivation on loss/theft",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_account_lockout_configured(esig_system_config: dict[str, Any]):
    """§11.300(d): Automated detection and reporting of unauthorized login attempts required."""
    assert esig_system_config.get("account_lockout_enabled"), (
        "§11.300(d): Automated account lockout must be enabled to detect unauthorized use attempts"
    )
    max_attempts = esig_system_config.get("lockout_max_attempts", 0)
    assert 0 < max_attempts <= 10, (
        f"Account lockout after {max_attempts} attempts — should be ≤10 for Part 11 systems"
    )
    assert esig_system_config.get("failed_attempts_alerted_to_security"), (
        "§11.300(d): Failed login attempts must be reported to the system security unit in automated fashion"
    )


@pytest.mark.assumption(
    id="ASSUME-21CFR11-008",
    description="Lost/stolen tokens immediately deactivated — deactivation within 4 hours of report",
    approved_by="QA/RA Lead",
    review_date="2027-05-20",
)
def test_lost_stolen_tokens_deactivated_timely(
    token_loss_records: list[dict[str, Any]],
):
    """§11.300(c): Lost, stolen, or compromised tokens must be deactivated without undue delay."""
    late_deactivations = []

    for record in token_loss_records:
        report_time = record.get("reported_at")
        deactivated_time = record.get("deactivated_at")
        if report_time is None:
            continue
        if deactivated_time is None:
            late_deactivations.append(f"{record['token_id']}: not yet deactivated")
        else:
            hours_elapsed = (deactivated_time - report_time).total_seconds() / 3600
            if hours_elapsed > LOST_TOKEN_DEACTIVATE_HOURS:
                late_deactivations.append(
                    f"{record['token_id']}: deactivated {hours_elapsed:.1f}h after report "
                    f"(max {LOST_TOKEN_DEACTIVATE_HOURS}h)"
                )

    assert not late_deactivations, (
        f"Lost/stolen tokens not deactivated within {LOST_TOKEN_DEACTIVATE_HOURS}h: "
        f"{late_deactivations}"
    )
```

---

## Open assumption registry (this file)

| ID | Section | Summary | Review date |
|---|---|---|---|
| ASSUME-21CFR11-001 | §11.10(e) | Audit trail: every create/modify/delete; non-alterable; operator ID + timestamp + old value; retained with record; FDA-inspectable | 2026-05-20 |
| ASSUME-21CFR11-002 | §11.10(d) | Access controls: unique user IDs; role-based; terminated = disabled within 24h; annual review | 2026-05-20 |
| ASSUME-21CFR11-003 | §11.10(b)+(c) | Record copies: human-readable and electronic on demand; archival integrity; retrievable throughout retention; checksum/hash verification | 2026-05-20 |
| ASSUME-21CFR11-004 | §11.50 | Signature manifestations: full name + date/time + meaning from controlled vocabulary; on every human-readable rendering | 2026-05-20 |
| ASSUME-21CFR11-005 | §11.70 | Signature/record link: permanent; alteration detectable; cannot be excised; hash or DB reference to specific record version | 2026-05-20 |
| ASSUME-21CFR11-006 | §11.100 | Uniqueness + FDA cert: unique IDs not reused; identity verified at hire; §11.100(c) letter submitted to FDA and on file | 2026-05-20 |
| ASSUME-21CFR11-007 | §11.200 | Two-component: user ID + password (or equivalent); first signing = both; session break resets; biometric = individual-only design | 2026-05-20 |
| ASSUME-21CFR11-008 | §11.300 | Password/token: lockout ≤10 attempts; failed attempts alerted to security; lost/stolen deactivated within 4h; periodic password checks | 2026-05-20 |
