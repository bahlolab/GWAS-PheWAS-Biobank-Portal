#!/usr/bin/env python3
"""
update_readme.py

Splices the auto-generated tables (docs/_portal_table.md and
docs/_feature_matrix.md) into README.md between marker comments, and
inserts the current portal count and last-updated date.

Run scripts/generate_tables.py first, then this script, whenever
data/portals.json changes.

Usage:
    python scripts/update_readme.py
"""

import datetime
import json
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
README = os.path.join(ROOT, "README.md")
DOCS_DIR = os.path.join(ROOT, "docs")
PORTALS_JSON = os.path.join(ROOT, "data", "portals.json")

MARKERS = [
    ("PORTAL_TABLE", "_portal_table.md"),
    ("FEATURE_MATRIX", "_feature_matrix.md"),
]


def splice(content: str, marker: str, replacement: str) -> str:
    pattern = re.compile(
        rf"(<!-- {marker}_START -->)(.*?)(<!-- {marker}_END -->)", re.DOTALL
    )
    new_block = f"\\g<1>\n{replacement}\n\\g<3>"
    if not pattern.search(content):
        raise ValueError(f"Markers for {marker} not found in README.md")
    return pattern.sub(lambda m: m.group(1) + "\n" + replacement + "\n" + m.group(3), content)


def main():
    with open(README, encoding="utf-8") as f:
        content = f.read()

    for marker, filename in MARKERS:
        path = os.path.join(DOCS_DIR, filename)
        with open(path, encoding="utf-8") as f:
            block = f.read().strip()
        content = splice(content, marker, block)

    with open(PORTALS_JSON, encoding="utf-8") as f:
        portals = json.load(f)

    content = re.sub(
        r"(<!-- PORTAL_COUNT_START -->)(.*?)(<!-- PORTAL_COUNT_END -->)",
        rf"\g<1>{len(portals)}\g<3>",
        content,
        flags=re.DOTALL,
    )
    today = datetime.date.today().isoformat()
    content = re.sub(
        r"(<!-- LAST_UPDATED_START -->)(.*?)(<!-- LAST_UPDATED_END -->)",
        rf"\g<1>{today}\3",
        content,
        flags=re.DOTALL,
    )

    with open(README, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"README.md updated: {len(portals)} portals, last updated {today}")


if __name__ == "__main__":
    main()
