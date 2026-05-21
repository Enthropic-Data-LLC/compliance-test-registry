"""
Minimal data model for the Compliance Test Case Registry.

Design principles:
- Every model is a pure value object (no ORM, no DB dependency).
- Models validate structure; they do not encode business logic.
- The markdown spec files remain the authoritative human-readable source of truth;
  these models are the machine-readable layer on top.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field


class AmbiguityTier(str, Enum):
    """Four-tier classification from the Regulatory Decomposition Framework."""
    DETERMINISTIC = "DETERMINISTIC"
    PARAMETERIZED = "PARAMETERIZED"
    CONTESTED = "CONTESTED"
    UNRESOLVABLE = "UNRESOLVABLE"


class ImpactLevel(str, Enum):
    """FIPS 199 / NIST impact baselines. Used as a dimension on all thresholds."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class ControlRelationship(str, Enum):
    """
    Describes the alias control's obligation relative to the canonical control.

    ``subset``   — alias ⊂ canonical (alias is weaker; satisfying canonical satisfies alias)
    ``superset`` — alias ⊃ canonical (alias is stricter; satisfying alias satisfies canonical)
    ``exact``    — alias ≡ canonical (satisfying either satisfies the other)
    ``overlap``  — partial overlap (neither direction guarantees satisfaction)
    """
    SUBSET = "subset"
    SUPERSET = "superset"
    EXACT = "exact"
    OVERLAP = "overlap"


class Threshold(BaseModel):
    """A single DETERMINISTIC numeric or enumerable obligation from a control."""
    label: str
    value: Union[int, float, str, list[str]]
    unit: Optional[str] = None
    baselines: list[ImpactLevel] = Field(default_factory=list)


class ODPEntry(BaseModel):
    """An Organization-Defined Parameter with its 800-53B default value."""
    key: str
    description: str
    baseline_value: Union[int, float, str, list[str]]
    baselines: list[ImpactLevel]
    source: str  # e.g. "NIST 800-53B default"


class Assumption(BaseModel):
    """
    A PARAMETERIZED assumption that must be approved before its test becomes enforcing.
    Corresponds to entries in each framework's _index.md assumption registry.
    """
    id: str           # e.g. "ASSUME-800171-SC-001"
    control_id: str
    framework_id: str
    summary: str
    review_date: date


class TestCase(BaseModel):
    """One test case derived from a single regulatory obligation."""
    id: str
    control_id: str
    framework_id: str
    tier: AmbiguityTier
    description: str
    baselines: list[ImpactLevel]
    required_odp_keys: list[str] = Field(default_factory=list)
    assumption_ids: list[str] = Field(default_factory=list)


class Control(BaseModel):
    """A single control within a framework, with its thresholds."""
    id: str          # e.g. "AC-7"
    family: str      # e.g. "AC"
    title: str
    framework_id: str
    baselines: list[ImpactLevel]
    thresholds: list[Threshold] = Field(default_factory=list)


class Framework(BaseModel):
    """Top-level framework descriptor."""
    id: str          # e.g. "nist-800-53-r5"
    name: str
    version: str
    authority: str


class ControlAlias(BaseModel):
    """
    One cross-framework control equivalence entry (a single row in the thesaurus).

    ``relationship`` describes the alias relative to the canonical:
    - subset:    alias is weaker; satisfying canonical satisfies alias
    - superset:  alias is stricter; satisfying alias satisfies canonical
    - exact:     satisfying either satisfies the other
    - overlap:   partial; neither direction guaranteed
    """
    canonical_framework: str
    canonical_id: str
    alias_framework: str
    alias_id: str
    relationship: ControlRelationship
    baselines: list[ImpactLevel]
    notes: str = ""


class ArtifactCluster(BaseModel):
    """
    A shared evidence artifact that satisfies multiple controls across frameworks.
    Corresponds to the clusters in guiding_docs/cross-framework-dependency-map.md.
    """
    id: str           # e.g. "incident-response-plan"
    name: str
    build_to: str     # "Build to: <framework> <section>" — the most demanding spec
    controls: list[dict]  # [{framework_id, control_id, obligation_summary}]


class EvidenceArtifact(BaseModel):
    """
    A specific evidence item produced by a system under test.
    ``satisfies`` uses "<framework_id>:<control_id>" notation, e.g. "nist-800-53-r5:SC-13".
    """
    id: str
    artifact_type: str   # e.g. "scan_report", "policy_document", "config_export"
    description: str
    satisfies: list[str]
