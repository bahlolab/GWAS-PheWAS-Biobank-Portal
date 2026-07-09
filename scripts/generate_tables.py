#!/usr/bin/env python3
"""
generate_tables.py

Regenerates the auto-generated Markdown tables that get embedded in
README.md, from the canonical data/portals.json. This keeps README.md,
portals.csv, and portals.json from drifting apart.

Usage:
    python scripts/generate_tables.py

It writes two files into docs/:
    docs/_portal_table.md            (full comparison table)
    docs/_feature_matrix.md          (boolean feature matrix)

These are then included/pasted into README.md between the
<!-- PORTAL_TABLE_START --> / <!-- PORTAL_TABLE_END --> markers
(and the equivalent FEATURE_MATRIX markers) by scripts/update_readme.py.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")
PORTALS_JSON = os.path.join(DATA_DIR, "portals.json")

YES = "✅"
NO = "—"
PARTIAL = "◐"

BOOL_MAP = {"Y": YES, "N": NO, "P": PARTIAL, "U": "❓"}


def fmt(v):
    return BOOL_MAP.get(v, v)


def main():
    with open(PORTALS_JSON, encoding="utf-8") as f:
        portals = json.load(f)

    os.makedirs(DOCS_DIR, exist_ok=True)

    # --- Comparison table -------------------------------------------------
    lines = []
    lines.append("| Portal | Institution | Country | Cohort | Sample Size | Ancestry | Summary Stats | API | Bulk DL |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for p in sorted(portals, key=lambda x: x["name"].lower()):
        lines.append(
            f"| [{p['name']}]({p['url']}) | {p['institution']} | {p['country']} | "
            f"{p['cohort']} | {p['sample_size']} | {p['ancestry']} | "
            f"{fmt(p['summary_stats'])} | {fmt(p['api_available'])} | {fmt(p['bulk_download'])} |"
        )
    with open(os.path.join(DOCS_DIR, "_portal_table.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # --- Feature matrix -----------------------------------------------------
    feature_cols = [
        ("gwas", "GWAS"), ("phewas", "PheWAS"), ("wes", "WES"), ("wgs", "WGS"),
        ("cnv", "CNV"), ("rare_variant", "Rare Var."), ("burden_test", "Burden"),
        ("eqtl", "eQTL"), ("pqtl", "pQTL"), ("twas", "TWAS"),
        ("lab_traits", "Lab"), ("imaging", "Imaging"), ("drug_targets", "Drug Tgt"),
        ("multi_omics", "Multi-omics"),
    ]
    lines = []
    header = "| Portal | " + " | ".join(label for _, label in feature_cols) + " |"
    sep = "|---|" + "|".join(["---"] * len(feature_cols)) + "|"
    lines.append(header)
    lines.append(sep)
    for p in sorted(portals, key=lambda x: x["name"].lower()):
        row = [f"[{p['name']}]({p['url']})"] + [fmt(p[col]) for col, _ in feature_cols]
        lines.append("| " + " | ".join(row) + " |")
    with open(os.path.join(DOCS_DIR, "_feature_matrix.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Regenerated tables for {len(portals)} portals in {DOCS_DIR}/")


if __name__ == "__main__":
    main()
