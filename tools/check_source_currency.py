#!/usr/bin/env python3
"""
Reports drift between the version of each framework this registry ASSERTS and the
version currently published by the issuing authority.

This tool detects drift. It does not edit registry content: a flag here means a human
must read the source and decide what, if anything, changed for our tests.

Check methods (per entry in data/sources.yml):

  ecfr    Query the eCFR versioner API for the latest amendment date across the
          configured parts. Authoritative and precise. Drift = an amendment dated
          after our `asserted_as_of`.
  regex   Fetch the source page and extract a version string. Drift = extracted
          version differs from the one embedded in `asserted`.
  hash    Fetch the source page, reduce it to visible text, and hash it. Drift =
          the hash differs from the stored baseline. Noisy by nature — some pages
          carry banners or timestamps — so treat a hash flag as "go look", not
          "something changed in the regulation".
  manual  Paywalled or no public version marker. Never flags automatically; listed
          in the report so it cannot be forgotten.

Exit codes:
  0 — no drift detected
  1 — drift detected, or one or more sources could not be checked

This tool never exits 2 and is not a merge gate. Regulators reorganise their websites;
that should produce a report, not a red build on an unrelated pull request.
"""
import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path

import yaml

SOURCES = Path("data/sources.yml")
BASELINES = Path("data/source-baselines.json")
USER_AGENT = (
    "compliance-test-registry currency checker "
    "(+https://github.com/Enthropic-Data-LLC/compliance-test-registry)"
)
TIMEOUT = 30
HOST_INTERVAL = 4.0   # seconds between requests to the same host
RETRY_AFTER = 10.0    # seconds to wait before the single retry
RETRY_CODES = {403, 429, 500, 502, 503, 504}

_last_request: dict[str, float] = {}

TAG_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)
STRIP_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


class Result:
    def __init__(self, entry, status, detail):
        self.id = entry["id"]
        self.name = entry["name"]
        self.method = entry["method"]
        self.asserted = str(entry["asserted"])
        self.url = entry.get("url", "")
        self.status = status  # CURRENT | DRIFT | UNKNOWN | MANUAL
        self.detail = detail


def _get(url: str) -> str:
    host = urllib.parse.urlparse(url).netloc
    # Some authorities (iso.org especially) start returning 403 to a burst of
    # requests, so space out consecutive hits on the same host.
    elapsed = time.monotonic() - _last_request.get(host, 0.0)
    if elapsed < HOST_INTERVAL:
        time.sleep(HOST_INTERVAL - elapsed)
    _last_request[host] = time.monotonic()

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def fetch(url: str) -> str:
    """Fetch a URL, retrying once on a throttling-shaped failure."""
    try:
        return _get(url)
    except urllib.error.HTTPError as exc:
        if exc.code not in RETRY_CODES:
            raise
    except (TimeoutError, urllib.error.URLError):
        pass
    time.sleep(RETRY_AFTER)
    return _get(url)


def visible_text(html: str) -> str:
    html = TAG_RE.sub(" ", html)
    return WS_RE.sub(" ", STRIP_RE.sub(" ", html)).strip()


def check_ecfr(entry) -> tuple[str, str]:
    """Latest amendment date across the configured parts, via the eCFR versioner API."""
    asserted_as_of = date.fromisoformat(str(entry["asserted_as_of"]))
    latest: tuple[date, str] | None = None
    for part in entry["parts"]:
        url = (
            f"https://www.ecfr.gov/api/versioner/v1/versions/"
            f"title-{entry['title']}.json?part={part}"
        )
        payload = json.loads(fetch(url))
        for version in payload.get("content_versions", []):
            raw = version.get("amendment_date") or version.get("date")
            if not raw:
                continue
            try:
                amended = date.fromisoformat(raw)
            except ValueError:
                continue
            if latest is None or amended > latest[0]:
                latest = (amended, f"{entry['title']} CFR {version.get('identifier', part)}")
    if latest is None:
        return "UNKNOWN", "eCFR returned no dated versions for the configured parts"
    amended, identifier = latest
    if amended > asserted_as_of:
        days = (amended - asserted_as_of).days
        return (
            "DRIFT",
            f"amended {amended} ({identifier}) — {days} day(s) after our "
            f"{asserted_as_of} review",
        )
    return "CURRENT", f"latest amendment {amended}, before our {asserted_as_of} review"


def check_regex(entry) -> tuple[str, str]:
    text = visible_text(fetch(entry["url"]))
    matches = re.findall(entry["pattern"], text)
    if not matches:
        return "UNKNOWN", "version pattern did not match — page layout may have changed"
    # Highest-sorting match wins: pages often list historical versions alongside current.
    def key(value: str):
        return [int(part) if part.isdigit() else part for part in re.split(r"\D+", value) if part]

    published = max(set(matches), key=key)
    if published in entry["asserted"]:
        return "CURRENT", f"published version {published} matches asserted"
    return "DRIFT", f"published version {published}, registry asserts '{entry['asserted']}'"


def check_hash(entry, baselines: dict, update: bool) -> tuple[str, str]:
    digest = hashlib.sha256(visible_text(fetch(entry["url"])).encode()).hexdigest()
    previous = baselines.get(entry["id"], {}).get("sha256")
    if update or previous is None:
        baselines[entry["id"]] = {
            "sha256": digest,
            "captured": datetime.now().date().isoformat(),
            "url": entry["url"],
        }
        return ("CURRENT", "baseline recorded") if previous is None else ("CURRENT", "baseline updated")
    if digest != previous:
        captured = baselines[entry["id"]].get("captured", "unknown")
        return "DRIFT", f"source page changed since baseline captured {captured}"
    return "CURRENT", "source page unchanged since baseline"


def run(only: str | None, update_baseline: bool) -> int:
    entries = yaml.safe_load(SOURCES.read_text())["sources"]

    # The registry and the source list must not drift apart.
    known = {entry["id"] for entry in entries}
    present = {
        str(path.parent).replace("compliance_entities/", "")
        for path in Path("compliance_entities").rglob("_index.md")
    }
    if present - known:
        print(
            "ERROR: frameworks with no entry in data/sources.yml: "
            + ", ".join(sorted(present - known)),
            file=sys.stderr,
        )
        return 1

    baselines = json.loads(BASELINES.read_text()) if BASELINES.exists() else {}
    results: list[Result] = []

    for entry in entries:
        if only and not entry["id"].startswith(only):
            continue
        try:
            if entry["method"] == "ecfr":
                status, detail = check_ecfr(entry)
            elif entry["method"] == "regex":
                status, detail = check_regex(entry)
            elif entry["method"] == "hash":
                status, detail = check_hash(entry, baselines, update_baseline)
            else:
                status, detail = "MANUAL", entry.get("notes", "human review only").strip()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            status, detail = "UNKNOWN", f"fetch failed: {exc}"
        except (ValueError, KeyError) as exc:
            status, detail = "UNKNOWN", f"could not interpret source: {exc}"
        results.append(Result(entry, status, detail))
        print(f"{status:8} {entry['id']:24} {detail}")

    BASELINES.write_text(json.dumps(baselines, indent=2, sort_keys=True) + "\n")

    drift = [r for r in results if r.status == "DRIFT"]
    unknown = [r for r in results if r.status == "UNKNOWN"]
    manual = [r for r in results if r.status == "MANUAL"]

    print(
        f"\n{len(results)} source(s) checked — {len(drift)} drift, {len(unknown)} "
        f"unknown, {len(manual)} manual-only, "
        f"{len(results) - len(drift) - len(unknown) - len(manual)} current."
    )
    if drift:
        print("\nDrift — a human must read the source and decide what changed:")
        for r in drift:
            print(f"  {r.id}: {r.detail}\n    asserted: {r.asserted}\n    {r.url}")
    if unknown:
        print("\nCould not check:")
        for r in unknown:
            print(f"  {r.id}: {r.detail}")

    return 1 if (drift or unknown) else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check registry currency against published sources")
    parser.add_argument("--only", help="Check only entries whose id starts with this prefix")
    parser.add_argument(
        "--update-baseline",
        action="store_true",
        help="Re-record hash baselines instead of comparing (use after a reviewed update)",
    )
    args = parser.parse_args()
    sys.exit(run(args.only, args.update_baseline))
