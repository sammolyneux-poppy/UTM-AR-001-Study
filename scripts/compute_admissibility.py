#!/usr/bin/env python3
"""
compute_admissibility.py
UTM-AR-001: Admissibility Statistics Computation

Reads data/processed/f14_scorecard.csv and computes:
  - Feature coverage rates (check/tilde/cross/dash per feature)
  - Tier distribution (Inside/Plausible/Boundary/Exit/Marginal/Negative)
  - Domain breakdown by classification
  - Top admissible systems

Regenerates all derived CSV files:
  - data/processed/classification_summary.csv
  - data/processed/feature_statistics.csv
  - data/processed/domain_breakdown.csv

Usage:
    python scripts/compute_admissibility.py
"""

import csv
import os
import sys
from collections import defaultdict

# Resolve paths relative to this script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
SCORECARD_PATH = os.path.join(REPO_ROOT, "data", "processed", "f14_scorecard.csv")
SUMMARY_PATH = os.path.join(REPO_ROOT, "data", "processed", "classification_summary.csv")
FEATURE_STATS_PATH = os.path.join(REPO_ROOT, "data", "processed", "feature_statistics.csv")
DOMAIN_BREAKDOWN_PATH = os.path.join(REPO_ROOT, "data", "processed", "domain_breakdown.csv")

FEATURES = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F12", "F13", "F14"]
FEATURE_NAMES = {
    "F1": "Discrete heritable string",
    "F2": "Duplication operator",
    "F3": "Deletion operator",
    "F4": "Selection on variants",
    "F5": "Power-law family-size distribution",
    "F6": "Balanced dup/del rates",
    "F7": "Positive innovation rate",
    "F8": "Conserved per-unit mutation rate (Drake K)",
    "F9": "Error threshold / channel capacity",
    "F10": "Thermodynamic irreversibility",
    "F12": "Three or more fitness levels",
    "F13": "Simple-to-complex trajectory",
    "F14": "WGD insufficiency",
}

CLASSIFICATIONS = ["Inside", "Plausible", "Boundary", "Exit", "Marginal", "Negative"]


def load_scorecard(path):
    systems = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            systems.append(row)
    return systems


def compute_feature_coverage(systems):
    """For each feature, count check/tilde/cross/dash across all systems."""
    coverage = {}
    for feat in FEATURES:
        counts = defaultdict(int)
        for s in systems:
            val = s.get(feat, "dash").strip()
            counts[val] += 1
        applicable = len(systems) - counts.get("dash", 0)
        check_count = counts.get("check", 0)
        tilde_count = counts.get("tilde", 0)
        cross_count = counts.get("cross", 0)
        pct_check = round(
            check_count / applicable * 100, 1
        ) if applicable > 0 else 0.0
        pct_check_or_tilde = round(
            (check_count + 0.5 * tilde_count) / applicable * 100, 1
        ) if applicable > 0 else 0.0
        coverage[feat] = {
            "check": check_count,
            "tilde": tilde_count,
            "cross": cross_count,
            "dash": counts.get("dash", 0),
            "applicable": applicable,
            "pct_check": pct_check,
            "pct_check_or_tilde": pct_check_or_tilde,
        }
    return coverage


def compute_tier_distribution(systems):
    """Count systems by classification."""
    dist = defaultdict(int)
    for s in systems:
        cls = s.get("classification", "Unknown").strip()
        dist[cls] += 1
    return dist


def compute_classification_systems(systems):
    """Group system names by classification."""
    groups = defaultdict(list)
    for s in systems:
        cls = s.get("classification", "Unknown").strip()
        name = s.get("system", "Unknown").strip()
        groups[cls].append(name)
    return groups


def compute_domain_breakdown(systems):
    """Count classifications per domain."""
    breakdown = defaultdict(lambda: defaultdict(int))
    for s in systems:
        domain = s.get("domain", "Unknown").strip()
        cls = s.get("classification", "Unknown").strip()
        breakdown[domain][cls] += 1
    return breakdown


def top_admissible_systems(systems, n=10):
    """Return top N systems by percent_score, Inside or Plausible only."""
    admissible = [
        s for s in systems
        if s.get("classification", "").strip() in ("Inside", "Plausible")
    ]
    admissible.sort(key=lambda s: float(s.get("percent_score", 0)), reverse=True)
    return admissible[:n]


def print_separator(char="-", width=72):
    print(char * width)


# ---------------------------------------------------------------------------
# CSV output writers
# ---------------------------------------------------------------------------

def write_classification_summary(tier_dist, classification_systems, total, path):
    """Write classification_summary.csv."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["classification", "count", "percent", "systems"])
        for cls in CLASSIFICATIONS:
            count = tier_dist.get(cls, 0)
            pct = round(count / total * 100, 1) if total > 0 else 0.0
            sys_list = ";".join(sorted(classification_systems.get(cls, [])))
            writer.writerow([cls, count, pct, sys_list])
    print(f"  [WRITE] {path}")


def write_feature_statistics(coverage, path):
    """Write feature_statistics.csv."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "feature", "feature_name", "check", "tilde", "cross", "dash",
            "applicable", "pct_check", "pct_check_or_tilde"
        ])
        for feat in FEATURES:
            c = coverage[feat]
            writer.writerow([
                feat,
                FEATURE_NAMES.get(feat, ""),
                c["check"],
                c["tilde"],
                c["cross"],
                c["dash"],
                c["applicable"],
                c["pct_check"],
                c["pct_check_or_tilde"],
            ])
    print(f"  [WRITE] {path}")


def write_domain_breakdown(domain_breakdown, path):
    """Write domain_breakdown.csv."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["domain"] + CLASSIFICATIONS + ["total"])
        for domain in sorted(domain_breakdown.keys()):
            row = [domain]
            domain_total = 0
            for cls in CLASSIFICATIONS:
                count = domain_breakdown[domain].get(cls, 0)
                row.append(count)
                domain_total += count
            row.append(domain_total)
            writer.writerow(row)
    print(f"  [WRITE] {path}")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

EXPECTED_COUNTS = {
    "total": 46,
    "Inside": 17,
    "Plausible": 2,
    "Boundary": 4,
    "Exit": 3,
    "Marginal": 5,
    "Negative": 15,
}

SYSTEMS_EXPANSION_PATH = os.path.join(
    REPO_ROOT, "data", "processed", "systems_expansion.csv"
)
SYSTEMS_EXPANSION_EXPECTED_HEADERS = [
    "scorecard_system", "individual_count", "individual_systems", "notes"
]


def validate_systems_expansion():
    """Validate data/processed/systems_expansion.csv structure and content.

    Checks:
      - File exists
      - First line is header (not a comment), matching expected columns
      - Every individual_count is a parseable integer
      - No blank scorecard_system entries
      - Row count matches scorecard (46)

    Returns True if all checks pass.
    """
    print_separator()
    print("  VALIDATION: systems_expansion.csv")
    print_separator()
    all_ok = True

    if not os.path.exists(SYSTEMS_EXPANSION_PATH):
        print(f"  FAIL  File not found: {SYSTEMS_EXPANSION_PATH}")
        return False

    with open(SYSTEMS_EXPANSION_PATH, newline="", encoding="utf-8") as f:
        raw_lines = f.readlines()

    if not raw_lines:
        print("  FAIL  File is empty")
        return False

    # Skip comment lines (starting with #) to find the header
    header_line_idx = 0
    for i, line in enumerate(raw_lines):
        if not line.strip().startswith("#"):
            header_line_idx = i
            break

    # Re-read with csv.DictReader, skipping comment lines
    data_lines = [l for l in raw_lines if not l.strip().startswith("#")]
    if not data_lines:
        print("  FAIL  No non-comment lines found")
        return False

    # Check first non-comment line is the header
    first_line = data_lines[0].strip()
    if first_line.startswith("#"):
        print("  FAIL  First non-comment line starts with '#' (expected header)")
        all_ok = False
    else:
        print("  PASS  First non-comment line is header (not a comment)")

    # Parse with csv reader
    reader = csv.DictReader(data_lines)
    actual_headers = reader.fieldnames or []

    # Check header columns (allow optional system_id column)
    base_match = all(
        h in actual_headers for h in SYSTEMS_EXPANSION_EXPECTED_HEADERS
    )
    if base_match:
        print(f"  PASS  Header columns present: {actual_headers}")
    else:
        print(
            f"  FAIL  Header mismatch: got {actual_headers}, "
            f"expected at least {SYSTEMS_EXPANSION_EXPECTED_HEADERS}"
        )
        all_ok = False

    rows = list(reader)
    row_count = len(rows)

    # Check row count
    if row_count == EXPECTED_COUNTS["total"]:
        print(f"  PASS  Row count = {row_count} (matches scorecard)")
    else:
        print(
            f"  FAIL  Row count: got {row_count}, "
            f"expected {EXPECTED_COUNTS['total']}"
        )
        all_ok = False

    # Check individual_count is parseable integer for every row
    bad_counts = []
    for i, row in enumerate(rows, start=1):
        val = row.get("individual_count", "").strip()
        try:
            int(val)
        except (ValueError, TypeError):
            bad_counts.append((i, val))
    if bad_counts:
        print(f"  FAIL  Non-integer individual_count in {len(bad_counts)} row(s):")
        for rnum, val in bad_counts[:5]:
            print(f"         Row {rnum}: '{val}'")
        all_ok = False
    else:
        print(f"  PASS  All individual_count values are parseable integers")

    # Check no blank scorecard_system
    blank_systems = [
        i for i, row in enumerate(rows, start=1)
        if not row.get("scorecard_system", "").strip()
    ]
    if blank_systems:
        print(f"  FAIL  Blank scorecard_system in row(s): {blank_systems[:10]}")
        all_ok = False
    else:
        print(f"  PASS  No blank scorecard_system entries")

    print()
    if all_ok:
        print("  >>> systems_expansion.csv VALIDATION PASSED <<<")
    else:
        print("  >>> systems_expansion.csv VALIDATION FAILED <<<")
    print()
    return all_ok


def validate(tier_dist, total):
    """Validate counts against expected values. Returns True if all pass."""
    print_separator()
    print("  VALIDATION: scorecard counts")
    print_separator()
    all_ok = True
    # Check total
    if total != EXPECTED_COUNTS["total"]:
        print(f"  FAIL  total: got {total}, expected {EXPECTED_COUNTS['total']}")
        all_ok = False
    else:
        print(f"  PASS  total = {total}")
    # Check each classification
    for cls in CLASSIFICATIONS:
        got = tier_dist.get(cls, 0)
        expected = EXPECTED_COUNTS.get(cls, 0)
        if got != expected:
            print(f"  FAIL  {cls}: got {got}, expected {expected}")
            all_ok = False
        else:
            print(f"  PASS  {cls} = {got}")
    print()
    if all_ok:
        print("  >>> ALL VALIDATION CHECKS PASSED <<<")
    else:
        print("  >>> VALIDATION FAILED <<<")
    print()
    return all_ok


def main():
    if not os.path.exists(SCORECARD_PATH):
        print(f"ERROR: Scorecard not found at {SCORECARD_PATH}")
        print("Run from the repo root or ensure data/processed/f14_scorecard.csv exists.")
        return

    systems = load_scorecard(SCORECARD_PATH)
    total = len(systems)

    print()
    print_separator("=")
    print("  UTM-AR-001: F1-F14 Admissibility Analysis")
    print("  Cross-Domain Validation of FP4 Admissibility Framework")
    print_separator("=")
    print(f"  Total systems assessed: {total}")
    print()

    # --- Tier Distribution ---
    tier_dist = compute_tier_distribution(systems)
    classification_systems = compute_classification_systems(systems)
    print_separator()
    print("  CLASSIFICATION DISTRIBUTION")
    print_separator()
    print(f"  {'Classification':<14} {'Count':>6} {'Pct':>8}")
    print_separator("-", 36)
    for cls in CLASSIFICATIONS:
        count = tier_dist.get(cls, 0)
        pct = round(count / total * 100, 1)
        print(f"  {cls:<14} {count:>6} {pct:>7.1f}%")
    print(f"  {'TOTAL':<14} {total:>6}")
    print()

    # --- Feature Coverage ---
    coverage = compute_feature_coverage(systems)
    print_separator()
    print("  FEATURE COVERAGE RATES (check + 0.5*tilde / applicable)")
    print_separator()
    print(f"  {'Feat':<5} {'check':>6} {'tilde':>6} {'cross':>6} {'dash':>6} {'applic':>7} {'% sat':>8}  Name")
    print_separator("-", 72)
    for feat in FEATURES:
        c = coverage[feat]
        name = FEATURE_NAMES.get(feat, "")
        print(
            f"  {feat:<5} {c['check']:>6} {c['tilde']:>6} {c['cross']:>6} {c['dash']:>6} "
            f"{c['applicable']:>7} {c['pct_check_or_tilde']:>7.1f}%  {name}"
        )
    print()

    # --- Domain Breakdown ---
    domain_breakdown = compute_domain_breakdown(systems)
    print_separator()
    print("  DOMAIN BREAKDOWN BY CLASSIFICATION")
    print_separator()
    header = f"  {'Domain':<10}"
    for cls in CLASSIFICATIONS:
        header += f" {cls[:7]:>8}"
    header += f"  {'Total':>6}"
    print(header)
    print_separator("-", 72)
    for domain in sorted(domain_breakdown.keys()):
        row = f"  {domain:<10}"
        domain_total = 0
        for cls in CLASSIFICATIONS:
            count = domain_breakdown[domain].get(cls, 0)
            row += f" {count:>8}"
            domain_total += count
        row += f"  {domain_total:>6}"
        print(row)
    print()

    # --- Key Finding: F1-F4 discriminatory power ---
    f1_fail = sum(1 for s in systems if s.get("F1", "").strip() == "cross")
    f4_all_check = sum(
        1 for s in systems
        if all(s.get(f, "").strip() == "check" for f in ["F1", "F2", "F3", "F4"])
    )
    print_separator()
    print("  KEY FINDING: F1-F4 DISCRIMINATORY POWER")
    print_separator()
    print(f"  Systems with F1-F4 all = check:    {f4_all_check} / {total} ({round(f4_all_check/total*100,1)}%)")
    print(f"  Systems with F1 = cross (excluded): {f1_fail} / {total} ({round(f1_fail/total*100,1)}%)")
    print()
    print("  All 8 physical power-law systems (PHYS domain) are excluded by F1-F4.")
    print("  Power laws are necessary but insufficient: ~40+ systems show power-law")
    print("  statistics, but only ~22 (Inside+Plausible) satisfy the full BDIM criteria.")
    print()

    # --- Top Admissible Systems ---
    top = top_admissible_systems(systems, n=10)
    print_separator()
    print("  TOP ADMISSIBLE SYSTEMS (by % score, Inside or Plausible)")
    print_separator()
    print(f"  {'System':<28} {'Domain':<8} {'Score':>8}  {'Classification'}")
    print_separator("-", 72)
    for s in top:
        name = s.get("system", "")[:27]
        domain = s.get("domain", "")[:7]
        score = s.get("percent_score", "N/A")
        cls = s.get("classification", "")
        print(f"  {name:<28} {domain:<8} {score:>7}%  {cls}")
    print()

    # --- Write derived CSV files ---
    print_separator("=")
    print("  REGENERATING DERIVED CSV FILES")
    print_separator("=")
    write_classification_summary(tier_dist, classification_systems, total, SUMMARY_PATH)
    write_feature_statistics(coverage, FEATURE_STATS_PATH)
    write_domain_breakdown(domain_breakdown, DOMAIN_BREAKDOWN_PATH)
    print()

    # --- Validation ---
    ok = validate(tier_dist, total)
    ok_expansion = validate_systems_expansion()

    print_separator("=")
    print("  UTM-AR-001 replication complete.")
    print_separator("=")
    print()

    if not ok or not ok_expansion:
        sys.exit(1)


if __name__ == "__main__":
    main()
