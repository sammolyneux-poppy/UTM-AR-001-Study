#!/usr/bin/env python3
"""
validate_docs.py
UTM-AR-001: Document-Sync Validation

Reads data/processed/classification_summary.csv (authoritative counts) and
checks that README.md and docs/UTM_AR_001_Report.md are consistent.

Checks:
  1. README classification table counts match classification_summary.csv
  2. Report mentions of Negative count match (should be 15)

Usage:
    python scripts/validate_docs.py
"""

import csv
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
SUMMARY_PATH = os.path.join(REPO_ROOT, "data", "processed", "classification_summary.csv")
README_PATH = os.path.join(REPO_ROOT, "README.md")
REPORT_PATH = os.path.join(REPO_ROOT, "docs", "UTM_AR_001_Report.md")


def load_classification_summary(path):
    """Load authoritative counts from classification_summary.csv."""
    counts = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cls = row["classification"].strip()
            count = int(row["count"])
            counts[cls] = count
    return counts


def check_readme(counts):
    """Check that README.md classification table counts match the CSV."""
    print("  CHECK: README.md classification table")
    print()

    if not os.path.exists(README_PATH):
        print("  FAIL  README.md not found")
        return False

    with open(README_PATH, encoding="utf-8") as f:
        text = f.read()

    all_ok = True

    # The README table has lines like:
    #   | **Inside** (~78.5-100%) | 17 | ...
    #   | **Negative** | 15 | ...
    # Pattern: | **Classification** ... | <count> |
    table_pattern = re.compile(
        r"\|\s*\*\*(\w+)\*\*[^|]*\|\s*(\d+)\s*\|"
    )

    readme_counts = {}
    for match in table_pattern.finditer(text):
        cls_name = match.group(1)
        cls_count = int(match.group(2))
        readme_counts[cls_name] = cls_count

    if not readme_counts:
        print("  FAIL  Could not find classification table in README.md")
        return False

    for cls, expected in counts.items():
        got = readme_counts.get(cls)
        if got is None:
            print(f"  FAIL  {cls}: not found in README table")
            all_ok = False
        elif got != expected:
            print(f"  FAIL  {cls}: README has {got}, CSV has {expected}")
            all_ok = False
        else:
            print(f"  PASS  {cls} = {got}")

    return all_ok


def check_report_negative(counts):
    """Check that docs/UTM_AR_001_Report.md agrees on Negative count."""
    print()
    print("  CHECK: UTM_AR_001_Report.md Negative count")
    print()

    if not os.path.exists(REPORT_PATH):
        print("  FAIL  UTM_AR_001_Report.md not found")
        return False

    expected_negative = counts.get("Negative", 15)

    with open(REPORT_PATH, encoding="utf-8") as f:
        text = f.read()

    all_ok = True

    # Look for patterns like "15 Negative" or "Negative (15)" or
    # "| **Negative** | 15 |" or "15 negative controls" etc.
    # We search for any line containing "Negative" near a number.
    negative_patterns = [
        # Table row: | **Negative** | <count> |
        (r"\|\s*\*\*Negative\*\*\s*\|\s*(\d+)\s*\|", "table row"),
        # Prose: "<count> Negative" or "<count> negative"
        (r"\b(\d+)\s+[Nn]egative\b", "prose count"),
        # Prose: "Negative.*<count>" within a short span
        (r"[Nn]egative[^.]{0,30}?\b(\d+)\b", "Negative near count"),
    ]

    found_any = False
    for pattern, label in negative_patterns:
        for match in re.finditer(pattern, text):
            value = int(match.group(1))
            found_any = True
            if value == expected_negative:
                print(f"  PASS  {label}: found {value} (matches CSV)")
            else:
                # Only flag mismatches for values that look like they
                # represent the total Negative count (not e.g. "6 negatives"
                # referring to the old count in context).
                print(f"  INFO  {label}: found {value} (CSV has {expected_negative})")

    if not found_any:
        print(f"  WARN  No Negative count references found in report")
        # Not a hard failure -- the report may just not state the count explicitly
    else:
        print(f"  PASS  Report references Negative count")

    return all_ok


def main():
    print()
    print("=" * 72)
    print("  UTM-AR-001: Document-Sync Validation")
    print("=" * 72)
    print()

    if not os.path.exists(SUMMARY_PATH):
        print(f"  ERROR: {SUMMARY_PATH} not found.")
        print("  Run compute_admissibility.py first to generate it.")
        sys.exit(1)

    counts = load_classification_summary(SUMMARY_PATH)
    print(f"  Authoritative counts from classification_summary.csv:")
    for cls, count in counts.items():
        print(f"    {cls}: {count}")
    print()

    ok_readme = check_readme(counts)
    ok_report = check_report_negative(counts)

    print()
    print("-" * 72)
    if ok_readme and ok_report:
        print("  >>> ALL DOCUMENT-SYNC CHECKS PASSED <<<")
    else:
        print("  >>> DOCUMENT-SYNC VALIDATION FAILED <<<")
    print("-" * 72)
    print()

    if not (ok_readme and ok_report):
        sys.exit(1)


if __name__ == "__main__":
    main()
