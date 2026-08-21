#!/usr/bin/env python3
"""
Scans the registry for documented assumptions and reports those approaching or
past their review due date.

Two assumption formats exist in the registry and both are checked:

  1. YAML assumption blocks in the standard files, e.g.

         - assumption_id: ASSUME-SOC2-CC8-001
           approved_by: "Compliance Officer"
           date: "2026-05-20"
           review_frequency_days: 365

     Due date = ``date`` + ``review_frequency_days``. An explicit
     ``review_due_date`` overrides the computed value when present.

  2. ``@pytest.mark.assumption(...)`` markers in the embedded test code, e.g.

         @pytest.mark.assumption(
             id="ASSUME-800053-AU-002",
             approved_by="ISSO",
             review_date="2026-05-21",
         )

     ``review_date`` is the due date. These markers carry mixed semantics across
     the registry (some hold the authoring date, some a future due date) and some
     are malformed, so by default they are reported as warnings only. Pass
     ``--strict-markers`` to gate on them.

Exit codes:
  0 — all assumptions current
  1 — one or more assumptions approaching expiry (within --warn-days), or
      marker-format problems while not in --strict-markers mode
  2 — one or more gated assumptions are stale (past due); pipeline should fail
"""
import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

REGISTRY = Path("compliance_entities")

# A YAML assumption block: id first, then (in any order) date / frequency / due date.
YAML_BLOCK_RE = re.compile(
    r"assumption_id:\s*['\"]?(?P<id>ASSUME-[\w.-]+)['\"]?(?P<body>.*?)(?=assumption_id:|\Z)",
    re.DOTALL,
)
DATE_RE = re.compile(r"^\s*date:\s*['\"]?(\d{4}-\d{2}-\d{2})['\"]?", re.MULTILINE)
FREQ_RE = re.compile(r"^\s*review_frequency_days:\s*(\d+)", re.MULTILINE)
DUE_RE = re.compile(r"^\s*review_due_date:\s*['\"]?(\d{4}-\d{2}-\d{2})['\"]?", re.MULTILINE)

MARKER_RE = re.compile(
    r"@pytest\.mark\.assumption\((?P<body>.*?)\)\s*\n", re.DOTALL
)
MARKER_ID_RE = re.compile(r"id\s*=\s*['\"]([^'\"]+)['\"]")
MARKER_DATE_RE = re.compile(r"review_date\s*=\s*['\"]([^'\"]+)['\"]")


def _iter_files():
    return sorted(REGISTRY.rglob("*.md"))


def collect_yaml_assumptions():
    """Yield (source, assumption_id, due_date) for every YAML assumption block."""
    for path in _iter_files():
        text = path.read_text()
        for match in YAML_BLOCK_RE.finditer(text):
            body = match.group("body")
            explicit = DUE_RE.search(body)
            if explicit:
                yield path, match.group("id"), date.fromisoformat(explicit.group(1))
                continue
            approved = DATE_RE.search(body)
            freq = FREQ_RE.search(body)
            if approved and freq:
                due = date.fromisoformat(approved.group(1)) + timedelta(
                    days=int(freq.group(1))
                )
                yield path, match.group("id"), due


def collect_marker_assumptions():
    """Yield (source, assumption_id, due_date_or_None, raw_date) for pytest markers."""
    for path in _iter_files():
        text = path.read_text()
        for match in MARKER_RE.finditer(text):
            body = match.group("body")
            id_match = MARKER_ID_RE.search(body)
            date_match = MARKER_DATE_RE.search(body)
            if not date_match:
                continue
            assume_id = id_match.group(1) if id_match else "UNKNOWN"
            raw = date_match.group(1)
            try:
                yield path, assume_id, date.fromisoformat(raw), raw
            except ValueError:
                yield path, assume_id, None, raw


def check_staleness(warn_days: int = 30, strict_markers: bool = False) -> int:
    today = date.today()
    warn_threshold = today + timedelta(days=warn_days)

    failures: list[str] = []
    warnings: list[str] = []
    checked = 0

    for path, assume_id, due in collect_yaml_assumptions():
        checked += 1
        if due < today:
            failures.append(
                f"STALE [{path}] {assume_id} — due {due} ({(today - due).days} day(s) overdue)"
            )
        elif due <= warn_threshold:
            warnings.append(
                f"WARNING [{path}] {assume_id} — due {due} ({(due - today).days} day(s) remaining)"
            )

    marker_stale: list[str] = []
    marker_bad: list[str] = []
    for path, assume_id, due, raw in collect_marker_assumptions():
        checked += 1
        if due is None:
            marker_bad.append(f"MALFORMED [{path}] {assume_id} — review_date={raw!r}")
        elif due < today:
            marker_stale.append(
                f"STALE MARKER [{path}] {assume_id} — review_date {due} "
                f"({(today - due).days} day(s) overdue)"
            )
        elif due <= warn_threshold:
            warnings.append(
                f"WARNING [{path}] {assume_id} — review_date {due} "
                f"({(due - today).days} day(s) remaining)"
            )

    if strict_markers:
        failures.extend(marker_stale)
        failures.extend(marker_bad)
    else:
        if marker_stale:
            warnings.append(
                f"WARNING — {len(marker_stale)} pytest.mark.assumption marker(s) carry a "
                f"review_date in the past. Not gated (see --strict-markers)."
            )
            warnings.extend(f"  {line}" for line in marker_stale[:10])
            if len(marker_stale) > 10:
                warnings.append(f"  ... and {len(marker_stale) - 10} more")
        if marker_bad:
            warnings.append(
                f"WARNING — {len(marker_bad)} marker(s) have an unparseable review_date. "
                f"Not gated (see --strict-markers)."
            )
            warnings.extend(f"  {line}" for line in marker_bad[:10])
            if len(marker_bad) > 10:
                warnings.append(f"  ... and {len(marker_bad) - 10} more")

    # Anti-vacuity guard: a checker that finds nothing to check is broken, not passing.
    if checked == 0:
        print(
            "ERROR: no assumptions found to check. The registry format or this "
            "parser has drifted — treating as a failure rather than a pass.",
            file=sys.stderr,
        )
        return 2

    for w in warnings:
        print(w)
    for f in failures:
        print(f, file=sys.stderr)

    print(f"Checked {checked} assumption(s) across {len(_iter_files())} registry files.")

    if failures:
        return 2
    if warnings:
        return 1
    print(f"✓ No stale or expiring assumptions found (warn window: {warn_days} days)")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check assumption staleness")
    parser.add_argument(
        "--warn-days",
        type=int,
        default=30,
        help="Warn when an assumption is due within this many days (default: 30)",
    )
    parser.add_argument(
        "--strict-markers",
        action="store_true",
        help="Treat overdue/malformed @pytest.mark.assumption review_dates as failures",
    )
    args = parser.parse_args()
    sys.exit(check_staleness(args.warn_days, args.strict_markers))
