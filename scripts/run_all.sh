#!/usr/bin/env bash
# run_all.sh — UTM-AR-001 Complete Replication Script
# Usage: bash scripts/run_all.sh  (from repo root)
#    or: cd scripts && bash run_all.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo "======================================================================"
echo "  UTM-AR-001: UTM Admissible Regions Study — Replication"
echo "======================================================================"
echo ""

# Verify Python 3 is available
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is required but not found in PATH."
    echo "Install Python 3.9+ from https://python.org and retry."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo "  Python: $PYTHON_VERSION"
echo "  Repo root: $REPO_ROOT"
echo ""

# Run admissibility computation
echo "  Running: compute_admissibility.py ..."
echo ""
python3 "$SCRIPT_DIR/compute_admissibility.py"

echo ""
echo "  Verifying output files..."
echo ""

# Verify all expected output files exist
EXPECTED_FILES=(
    "$REPO_ROOT/data/processed/classification_summary.csv"
    "$REPO_ROOT/data/processed/feature_statistics.csv"
    "$REPO_ROOT/data/processed/domain_breakdown.csv"
)

ALL_OK=true
for f in "${EXPECTED_FILES[@]}"; do
    if [ -f "$f" ]; then
        echo "  ✓ $(basename "$f")"
    else
        echo "  ✗ MISSING: $(basename "$f")"
        ALL_OK=false
    fi
done

echo ""
if ! $ALL_OK; then
    echo "WARNING: Some output files are missing. Check script output above."
    exit 1
fi

# Run document-sync validation
echo "  Running: validate_docs.py ..."
echo ""
python3 "$SCRIPT_DIR/validate_docs.py"

echo ""
echo "======================================================================"
echo "  UTM-AR-001 replication complete. All outputs verified."
echo "======================================================================"
