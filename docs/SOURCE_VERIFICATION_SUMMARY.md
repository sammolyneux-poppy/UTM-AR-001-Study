# UTM-AR-001 Source Verification Summary

**Generated:** 2026-04-06
**Study:** UTM-AR-001 — Cross-Domain Admissibility Study
**Version:** v2.2 (citation remediation)

---

## Validation Results

**13/13 checks passed** | **0 failed**

| Check | Result |
|---|---|
| catalog_row_count | ✓ PASS |
| catalog_no_blank_citations | ✓ PASS |
| catalog_no_bundle_citations | ✓ PASS |
| fem_no_blank_citations | ✓ PASS |
| fem_no_hard_fail_status | ✓ PASS |
| fem_no_bundle_citations | ✓ PASS |
| fem_system_ids_valid | ✓ PASS |
| fem_coverage | ✓ PASS |
| source_registry_exists | ✓ PASS |
| coverage_summary_complete | ✓ PASS |
| fem_schema_complete | ✓ PASS |
| fem_source_url_canonical | ✓ PASS |
| fem_source_id_resolves | ✓ PASS |

---

## Evidence Tier Classification

All 46 systems now have 100% citation coverage in `data/curated/feature_evidence_matrix.csv`.
Systems are classified into four evidence tiers based on `dominant_support_status`:

| Evidence Tier | Systems |
|---|---|
| direct | 31 system(s) |
| synthesized | 12 system(s) |
| qualitative | 3 system(s) |

### Tier Definitions

| Tier | Meaning |
|---|---|
| **direct** | All material claims cite peer-reviewed literature directly; independently reconstructible from public data |
| **synthesized** | Core claims cited; some features rely on cross-system inference or database aggregation; partially reconstructible |
| **qualitative** | Expert assessment based on domain knowledge with limited formal citation; not independently reconstructible |
| **not_independently_reconstructible** | Claims are theoretical or from inaccessible sources |

---

## Citation Schema

`feature_evidence_matrix.csv` now includes four evidence quality columns:

| Column | Description |
|---|---|
| `source_url` | DOI or stable URL for primary citation |
| `support_status` | direct / synthesized / qualitative / not_independently_reconstructible |
| `reviewer_note` | Auditor flags; blank if clean |
| `independent_reconstruction_status` | yes / partial / no |

---

## Flagged Rows

The following system+feature combinations carry `qualitative` support_status due to absence of
formal statistical validation (this is expected and documented):

- **D. discoideum** F5, F9 — power law not formally Clauset-MLE-validated
- **F. albicollis** F5, F9 — power law not formally Clauset-MLE-validated
- **Chess openings** all features — qualitative analogy; Blasius & Tönjes 2009 cited for structure
- **Dog breeds** all features — AKC statistics + Parker 2004; no formal BDIM fit
- **RNA World** all features — theoretical framework; Gilbert 1986 + Joyce 2002

**None of these qualitative rows affect the admissibility classification** of their respective
systems. D. discoideum and F. albicollis remain Inside (Tier B, 91.7%) because their tilde
features are not classification-determining.

---

## Source Registry

`data/raw/source_registry.csv` registers 75 unique sources with canonical citations, DOIs,
URLs, source types, and access status.

---

## Re-audit Decision Buckets

| Bucket | Count | Systems |
|---|---|---|
| Fully independently reconstructible | ~25 | BIO core, PHYS, IMMUNE-tcell, ECON-babynames |
| Partially independently reconstructible | ~17 | BIO-archaea79, BIO-cancersomatic, COMP-software, ECON-pottery |
| Curated-synthesis only | 4 | COMP-chess, ECON-dogbreeds, CHEM-rnaworld, ECON-patents |
| Needs reclassification or removal | 0 | None |

