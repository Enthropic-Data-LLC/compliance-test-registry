#!/usr/bin/env python3
"""
Scans all _index.md files for assumption blocks and reports those
approaching or past their review_due_date.

Exit codes:
  0 — all assumptions current
  1 — one or more assumptions approaching expiry (within --warn-days)
  2 — one or more assumptions are stale (past review_due_date); pipeline should fail
"""
import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path


def check_staleness(warn_days: int = 30) -> int:
    today = date.today()
    warn_threshold = today + timedelta(days=warn_days)

    failures = []
    warnings = []

    for index_file in Path("compliance_entities").rglob("_index.md"):
        content = index_file.read_text()
        for match in re.finditer(
            r"review_due_date:\s*['\"]?(\d{4}-\d{2}-\d{2})['\"]?", content
        ):
            due = date.fromisoformat(match.group(1))
            # Walk back to find the nearest assumption id
            prior_text = content[: match.start()]
            assume_id_match = re.search(
                r"id:\s*['\"]?(ASSUME-[\w-]+)['\"]?", prior_text
            )
            assume_id = assume_id_match.group(1) if assume_id_match else "UNKNOWN"

            if due < today:
                days_over = (today - due).days
                failures.append(
                    f"STALE [{index_file}] {assume_id} — "
                    f"due {due} ({days_over} day(s) overdue)"
                )
            elif due <= warn_threshold:
                days_left = (due - today).days
                warnings.append(
                    f"WARNING [{index_file}] {assume_id} — "
                    f"due {due} ({days_left} day(s) remaining)"
                )

    for w in warnings:
        print(w)
    for f in failures:
        print(f, file=sys.stderr)

    if not failures and not warnings:
        print(f"✓ No stale or expiring assumptions found (warn window: {warn_days} days)")

    if failures:
        return 2
    if warnings:
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check assumption staleness")
    parser.add_argument(
        "--warn-days",
        type=int,
        default=30,
        help="Warn when review_due_date is within this many days (default: 30)",
    )
    args = parser.parse_args()
    sys.exit(check_staleness(args.warn_days))
