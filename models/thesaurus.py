"""
Thesaurus loader and query interface.

Reads data/thesaurus.yml and exposes two query methods:

    thesaurus.aliases_for(framework, control_id)
        → all ControlAlias entries where the control appears on either side

    thesaurus.satisfies(source_framework, source_control,
                        target_framework, target_control,
                        at_level=None)
        → True if satisfying source_control provably satisfies target_control

Satisfaction logic (follows from ControlRelationship semantics):
    canonical → alias:  True when relationship is SUBSET or EXACT
                        (canonical is stricter or equal; covering canonical covers alias)
    alias → canonical:  True when relationship is SUPERSET or EXACT
                        (alias is stricter; covering alias covers canonical)
    overlap:            False in both directions (partial coverage only)
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

from .core import ControlAlias, ControlRelationship, ImpactLevel

_DEFAULT_PATH = Path(__file__).parent.parent / "data" / "thesaurus.yml"


class Thesaurus:
    def __init__(self, path: Path = _DEFAULT_PATH) -> None:
        with open(path) as f:
            raw = yaml.safe_load(f)
        canonical_fw = raw["canonical_framework"]
        self._entries: list[ControlAlias] = []
        for entry in raw.get("entries", []):
            for alias in entry.get("aliases", []):
                self._entries.append(
                    ControlAlias(
                        canonical_framework=canonical_fw,
                        canonical_id=entry["canonical_id"],
                        alias_framework=alias["framework"],
                        alias_id=alias["control_id"],
                        relationship=ControlRelationship(alias["relationship"]),
                        baselines=[ImpactLevel(b) for b in alias.get("baselines", [])],
                        notes=alias.get("notes", "").strip(),
                    )
                )

    @property
    def entries(self) -> list[ControlAlias]:
        return list(self._entries)

    def aliases_for(self, framework: str, control_id: str) -> list[ControlAlias]:
        """Return all entries where this control appears as canonical or alias."""
        return [
            e for e in self._entries
            if (e.canonical_framework == framework and e.canonical_id == control_id)
            or (e.alias_framework == framework and e.alias_id == control_id)
        ]

    def satisfies(
        self,
        source_framework: str,
        source_control: str,
        target_framework: str,
        target_control: str,
        at_level: Optional[ImpactLevel] = None,
    ) -> bool:
        """
        Return True if satisfying source provably satisfies target per the thesaurus.

        Pass ``at_level`` to restrict the check to a specific impact baseline.
        """
        for e in self._entries:
            if at_level is not None and at_level not in e.baselines:
                continue

            # source is canonical, target is alias
            if (
                e.canonical_framework == source_framework
                and e.canonical_id == source_control
                and e.alias_framework == target_framework
                and e.alias_id == target_control
            ):
                # canonical is stricter (subset) or equal → satisfying canonical covers alias
                return e.relationship in (ControlRelationship.SUBSET, ControlRelationship.EXACT)

            # source is alias, target is canonical
            if (
                e.alias_framework == source_framework
                and e.alias_id == source_control
                and e.canonical_framework == target_framework
                and e.canonical_id == target_control
            ):
                # alias is stricter (superset) or equal → satisfying alias covers canonical
                return e.relationship in (ControlRelationship.SUPERSET, ControlRelationship.EXACT)

        return False

    def coverage_for(
        self,
        framework: str,
        control_id: str,
        at_level: Optional[ImpactLevel] = None,
    ) -> list[tuple[str, str]]:
        """
        Return all (framework, control_id) pairs that are provably satisfied
        when ``control_id`` in ``framework`` is satisfied.
        """
        results: list[tuple[str, str]] = []
        for e in self._entries:
            if at_level is not None and at_level not in e.baselines:
                continue

            # this control is canonical → check if it covers its aliases
            if e.canonical_framework == framework and e.canonical_id == control_id:
                if e.relationship in (ControlRelationship.SUBSET, ControlRelationship.EXACT):
                    results.append((e.alias_framework, e.alias_id))

            # this control is alias → check if it covers the canonical
            if e.alias_framework == framework and e.alias_id == control_id:
                if e.relationship in (ControlRelationship.SUPERSET, ControlRelationship.EXACT):
                    results.append((e.canonical_framework, e.canonical_id))

        return results
