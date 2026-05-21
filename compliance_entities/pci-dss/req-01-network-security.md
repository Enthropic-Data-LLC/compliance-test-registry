# Requirement 1 — Install and Maintain Network Security Controls

**Registry path:** `/regulation-registry/PCI-DSS/Req-1/`
**Version:** PCI DSS v4.0 (mandatory since March 31, 2025)
**Last parsed:** 2026-05-20
**Overall confidence:** HIGH — 6-month review cadence and default-deny are DETERMINISTIC; rule sufficiency is PARAMETERIZED
**R = Required**

---

## Scope summary

Req 1 governs network security controls (NSCs) — firewalls, routers, switches, and software-defined networking components that enforce traffic restrictions around the CDE. The language changed in v4.0 from "firewalls and routers" to "network security controls" to accommodate cloud, container, and software-defined environments. Two DETERMINISTIC thresholds apply: the 6-month rule review cadence and the inbound/outbound restriction obligation. Rule sufficiency ("are the rules correct?") is PARAMETERIZED.

---

## 1.2.2 — NSC Rule Review (R — DETERMINISTIC)

### Source excerpt

> *1.2.2 — All changes to network connections and to configurations of NSCs are approved and managed in accordance with the change control process defined at Requirement 6.5.1. Network diagrams are updated to reflect changes in accordance with the entity's change control process. Configurations for NSCs are reviewed at least once every six months to confirm they are relevant and effective.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All NSC rule configurations | DETERMINISTIC |
| Condition | NSC exists in the CDE environment | DETERMINISTIC |
| Obligation | NSC rules reviewed ≤ 180 days; review confirmed in writing; irrelevant rules removed | DETERMINISTIC |
| Evidence | `nsc_review_records.review_date`; `nsc_review_records.nsc_id`; review interval ≤ 180 days | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 1.3 — Restrict Traffic To and From CDE (R — DETERMINISTIC + PARAMETERIZED)

### Source excerpt

> *1.3.1 — Inbound traffic to the CDE is restricted to only that which is necessary.*
> *1.3.2 — Outbound traffic from the CDE is restricted to only that which is necessary.*
> *1.3.3 — NSCs are installed between all wireless networks and the CDE, and these NSCs deny or, if traffic is necessary, permit only authorized traffic between the wireless environment and the CDE.*

### Element extraction — inbound/outbound restriction

| Element | Value | Classification |
|---|---|---|
| Subject | All network paths to/from CDE | DETERMINISTIC |
| Condition | Network path exists between CDE and any other segment | DETERMINISTIC |
| Obligation | Inbound AND outbound traffic restricted to authorized flows only; implicit deny-all for everything else | DETERMINISTIC |
| Evidence | `nsc_configs.default_policy == "deny"`; authorized traffic rules documented; no "permit any any" rules | DETERMINISTIC |

### Element extraction — rule sufficiency

| Element | Value | Classification |
|---|---|---|
| Obligation | Rules permit only traffic that is "necessary" for business operations | PARAMETERIZED |
| Evidence | Rule review: each rule has a documented business justification; overly permissive rules identified and remediated | PARAMETERIZED |

**Assumption (ASSUME-1-001):** An NSC rule is "necessary" when: (1) a documented business justification exists identifying the source, destination, port, and protocol; (2) the rule is the minimum required (least-privilege for network traffic); (3) the rule has been reviewed in the most recent 6-month cycle and confirmed still required. Rules without documented justification, rules with source/destination "any," or rules that have not been reviewed in 6 months are considered unnecessary.

**Overall: DETERMINISTIC for policy existence → Pattern 1; PARAMETERIZED for rule sufficiency → Pattern 2**

---

## 1.4.4 — CDE Not Directly Accessible from Untrusted Networks (R — DETERMINISTIC)

### Source excerpt

> *1.4.4 — System components that store cardholder data are not directly accessible from untrusted networks.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All systems that store CHD | DETERMINISTIC |
| Condition | System stores cardholder data | DETERMINISTIC |
| Obligation | No direct path from untrusted network (internet) to CHD-storing system; DMZ or multi-tier architecture required | DETERMINISTIC |
| Evidence | Network diagram review; no rule permitting direct internet → CHD storage system traffic | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 1.4.5 — Internal IP Addresses Not Disclosed (R — DETERMINISTIC)

### Source excerpt

> *1.4.5 — The disclosure of internal IP addresses and routing information is limited to only authorized parties.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | Internal CDE IP address space and routing tables | DETERMINISTIC |
| Condition | Traffic is outbound from CDE toward untrusted networks | DETERMINISTIC |
| Obligation | Internal IPs not disclosed in DNS responses, error messages, or network headers visible externally | DETERMINISTIC |
| Evidence | External DNS does not return RFC1918 addresses; error pages do not disclose internal IPs; NAT configured | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## 1.5.1 — NSCs on Remote-Access Devices (R — DETERMINISTIC)

### Source excerpt

> *1.5.1 — Security policies and operational procedures are in place for managing all NSCs in use. NSCs are installed on any computing devices, including company- and employee-owned devices, that connect to both untrusted networks and the CDE.*

### Element extraction

| Element | Value | Classification |
|---|---|---|
| Subject | All devices (company and BYOD) that connect to both untrusted networks and CDE | DETERMINISTIC |
| Condition | Device can access the internet AND the CDE | DETERMINISTIC |
| Obligation | NSC (host-based firewall or endpoint NAC) installed and active on the device | DETERMINISTIC |
| Evidence | `endpoint_config.host_firewall_active == true` for all dual-network devices | DETERMINISTIC |

**Overall: DETERMINISTIC → Full Automation (Pattern 1)**

---

## YAML specifications

### `req1_rule_review.yaml`

```yaml
regulation_id: PCI-DSS-v4.0-1.2.2
section: "PCI DSS v4.0 — NSC Rule Review Cadence"
r_or_a: Required
source_text: >
  Configurations for NSCs are reviewed at least once every six months to
  confirm they are relevant and effective.

extracted_elements:
  subject: "All NSC configurations in CDE environment"
  condition: "NSC exists in scope"
  obligation: "Review ≤ 180 days; irrelevant rules removed"
  evidence: "nsc_review_records: review_date, nsc_id, rules_removed_count"

ambiguity_classification:
  subject: DETERMINISTIC
  condition: DETERMINISTIC
  obligation: DETERMINISTIC
  evidence: DETERMINISTIC

overall_classification: DETERMINISTIC
human_review_required: false
legal_assumption_log: []
test_confidence: HIGH
generated_test: "tests/req1/test_1_2_nsc_review.py"
```

---

## Generated tests

### `tests/req1/test_1_2_nsc_review.py`

```python
"""
PCI DSS v4.0 Req 1.2 — NSC Review Cadence and Rule Validity
Confidence: HIGH for cadence; MEDIUM for rule justification
"""
import pytest
from datetime import date

NSC_REVIEW_MAX_DAYS = 180


def test_all_nscs_reviewed_within_6_months(nsc_review_records, cde_nsc_inventory):
    """1.2.2 — NSC rules reviewed at least every 6 months."""
    today = date.today()
    reviewed_nsc_ids = {r["nsc_id"] for r in nsc_review_records}
    violations = []
    for nsc in cde_nsc_inventory:
        if nsc["nsc_id"] not in reviewed_nsc_ids:
            violations.append(f"{nsc['nsc_id']}: no review record on file")
            continue
        latest_review = max(
            (r for r in nsc_review_records if r["nsc_id"] == nsc["nsc_id"]),
            key=lambda r: r["review_date"],
        )
        days_since = (today - latest_review["review_date"]).days
        if days_since > NSC_REVIEW_MAX_DAYS:
            violations.append(
                f"{nsc['nsc_id']}: last reviewed {days_since} days ago "
                f"(max {NSC_REVIEW_MAX_DAYS})"
            )
    assert not violations, (
        f"VIOLATION (1.2.2): {len(violations)} NSC(s) not reviewed within 6 months:\n"
        + "\n".join(violations)
    )


def test_no_permit_any_any_rules(nsc_rule_inventory):
    """1.3.1 / 1.3.2 — No overly permissive 'allow any any' rules."""
    violations = [
        r for r in nsc_rule_inventory
        if r.get("source") in ("any", "0.0.0.0/0")
        and r.get("destination") in ("any", "0.0.0.0/0")
        and r.get("action") == "permit"
    ]
    assert not violations, (
        f"VIOLATION (1.3): {len(violations)} NSC rule(s) permit unrestricted traffic "
        f"(source=any, destination=any):\n"
        + "\n".join(
            f"  Rule {r.get('rule_id')} on {r.get('nsc_id')}" for r in violations
        )
    )


def test_default_deny_on_cde_nscs(cde_nsc_inventory):
    """1.3 — All CDE NSCs must have a default-deny policy."""
    violations = [
        n for n in cde_nsc_inventory
        if n.get("default_policy") != "deny"
    ]
    assert not violations, (
        f"VIOLATION (1.3): {len(violations)} CDE NSC(s) without default-deny policy: "
        f"{[(n['nsc_id'], n.get('default_policy')) for n in violations]}"
    )


def test_chd_storage_not_directly_reachable_from_internet(network_topology_review):
    """1.4.4 — Systems storing CHD must not be directly accessible from untrusted networks."""
    violations = [
        r for r in network_topology_review
        if r.get("stores_chd") and r.get("directly_internet_accessible")
    ]
    assert not violations, (
        f"VIOLATION (1.4.4): {len(violations)} CHD-storing system(s) directly "
        f"accessible from the internet: "
        f"{[r['system_id'] for r in violations]}"
    )


@pytest.mark.assumption(
    id="ASSUME-1-001",
    description=(
        "NSC rule 'necessary': documented business justification; least-privilege "
        "for traffic; reviewed in last 6-month cycle. Rules without justification or "
        "reviewed > 6 months ago are unnecessary."
    ),
    approved_by="Compliance Officer",
    review_date="2026-05-20",
)
def test_nsc_rules_have_business_justification(nsc_rule_inventory):
    violations = [
        r for r in nsc_rule_inventory
        if r.get("action") == "permit"
        and not r.get("business_justification_documented")
    ]
    assert not violations, (
        f"VIOLATION (1.3): {len(violations)} permit rule(s) without documented "
        f"business justification:\n"
        + "\n".join(
            f"  Rule {r.get('rule_id')} on {r.get('nsc_id')}: "
            f"{r.get('source')} → {r.get('destination')}:{r.get('port')}"
            for r in violations
        )
    )
```

---

## Notes for the registry

- **v4.0 terminology shift:** v3.2.1 said "firewalls and routers." v4.0 uses "network security controls (NSCs)" — explicitly including cloud security groups, virtual network ACLs, containers' network policies, and software-defined networking constructs. Cloud-native organizations must map their security groups and network policies to this requirement.
- **Network diagram currency:** 1.2.2 implies that network diagrams must be kept current (changes tracked via change control). An outdated diagram is treated as evidence of insufficient control, even if the actual NSC configurations are correct.
- **Outbound traffic restriction:** Many organizations restrict inbound traffic but fail to restrict outbound. 1.3.2 requires outbound from the CDE to be "restricted to only that which is necessary" — this is a common QSA finding. Egress filtering prevents data exfiltration and C2 communication from compromised CDE systems.
- **BYOD and dual-homed devices (1.5.1):** Any device that simultaneously accesses both the internet and the CDE (including split-tunnel VPN configurations) requires an NSC on the device itself. Split-tunnel VPN without host firewall is a common compliance gap.
- **Cloud NSCs:** AWS Security Groups, Azure NSGs, GCP Firewall Rules, and Kubernetes Network Policies all qualify as NSCs under v4.0. They must be included in the 6-month review cycle and documented in the network architecture.
