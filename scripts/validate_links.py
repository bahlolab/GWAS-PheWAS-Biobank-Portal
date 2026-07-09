#!/usr/bin/env python3
"""
validate_links.py

Checks every portal URL in data/portals.json for reachability and writes a
status report to data/link_status.json (and a human-readable summary to
stdout). Designed to be run locally or from the check-links GitHub Action.

Usage:
    python scripts/validate_links.py [--timeout 15] [--fail-on-broken]

Exit code is non-zero if --fail-on-broken is set and any URL is broken,
which is used by CI to fail the workflow (surfaced via badges/issues rather
than blocking merges by default).
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PORTALS_JSON = os.path.join(DATA_DIR, "portals.json")
STATUS_JSON = os.path.join(DATA_DIR, "link_status.json")

USER_AGENT = (
    "Mozilla/5.0 (compatible; GWAS-Biobank-Portal-Catalog-LinkChecker/1.0; "
    "+https://github.com/)"
)


def check_url(url: str, timeout: int) -> dict:
    """Return a dict describing the reachability of a single URL."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"status": "ok", "http_status": resp.status}
    except urllib.error.HTTPError as e:
        # Some sites (e.g. those blocking HEAD) return 4xx/5xx to HEAD but work with GET.
        if e.code in (403, 405, 501):
            try:
                req_get = urllib.request.Request(
                    url, headers={"User-Agent": USER_AGENT}, method="GET"
                )
                with urllib.request.urlopen(req_get, timeout=timeout) as resp:
                    return {"status": "ok", "http_status": resp.status}
            except Exception as e2:  # noqa: BLE001
                return {"status": "broken", "http_status": None, "error": str(e2)}
        return {"status": "broken", "http_status": e.code, "error": str(e)}
    except Exception as e:  # noqa: BLE001
        return {"status": "broken", "http_status": None, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=15, help="Per-request timeout in seconds")
    parser.add_argument(
        "--fail-on-broken", action="store_true", help="Exit non-zero if any URL is broken"
    )
    parser.add_argument(
        "--sleep", type=float, default=0.5, help="Delay between requests (politeness)"
    )
    args = parser.parse_args()

    with open(PORTALS_JSON, encoding="utf-8") as f:
        portals = json.load(f)

    results = {}
    broken = []

    for p in portals:
        url = p["url"]
        print(f"Checking {p['id']:35s} {url}")
        result = check_url(url, args.timeout)
        result["name"] = p["name"]
        result["url"] = url
        results[p["id"]] = result
        if result["status"] != "ok":
            broken.append((p["id"], url, result.get("error")))
        time.sleep(args.sleep)

    with open(STATUS_JSON, "w", encoding="utf-8") as f:
        json.dump(
            {"checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "results": results},
            f,
            indent=2,
        )

    print("\n=== Summary ===")
    print(f"Total portals checked: {len(portals)}")
    print(f"Broken/unreachable:    {len(broken)}")
    for pid, url, err in broken:
        print(f"  - {pid}: {url} ({err})")

    if args.fail_on_broken and broken:
        sys.exit(1)


if __name__ == "__main__":
    main()
