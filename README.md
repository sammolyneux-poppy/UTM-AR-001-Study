# UTM-AR-001: UTM Admissible Regions Study

**Companion to:** "Computational Universality of Recursive Genome Evolution" (FP4 Lean 4 Formal Proof)

## Overview

This repository contains the complete replication package for the UTM-AR-001 admissible regions study — a cross-domain empirical analysis assessing approximately 85 natural and cultural systems against the FP4 proof's F1-F14 admissibility framework.

The FP4 formal proof (`biological_evolution_is_utm`) establishes in Lean 4 that recursive genome mutation operators — specifically, deletion and duplication acting on discrete heritable units under selection — are computationally universal. The proof depends on 14 axioms (8 FORMAL, 2 EMPIRICAL_WELL_CONFIRMED, 3 EMPIRICAL_MEASURED, 1 MODELLING_BRIDGE), zero `sorry` placeholders, and compiles with 0 errors across 62 Lean files.

The admissibility framework operationalizes the proof's sufficient conditions into 13 active empirically testable features (F1-F10, F12-F14). **F11 (accessible fitness landscape) is excluded from admissibility scoring** because the corresponding Lean axiom (`bio_landscapes_monotone`) is currently orphaned — retained as a supplementary annotation only. Admissibility requires scoring on at least 11/13 applicable features for biological systems (Inside classification: >= 78.5% AND F1-F4 all satisfied).

**Version:** 2.1 (incorporates R1-R12 revisions from peer review; see `docs/V2_REVISION_SUMMARY.md`)

## Key Results

| Classification | Count | Key Examples |
|---------------|:-----:|-------------|
| **Inside** (~78.5-100%) | ~20 | E. coli (100%), S. cerevisiae (100%), S. pombe (100%), T/B cell repertoire (100%), H. sapiens (96.2%), Pan-genomes (95.8%), Baby names (94.4%) |
| **Plausible** (57-78%) | ~2 | Cancer somatic evolution (73.1%), Software codebases (81.8%) |
| **Boundary** | ~4 | CPR bacteria (63.6%), DPANN archaea (63.6%), Language (83.3%), Patents |
| **Exit** | ~3 | Buchnera (40.9%), Carsonella (40.9%), N. equitans (40.9%) |
| **Marginal** | ~5 | RNA World (61.1%), PPI networks (55.6%), WWW hyperlinks (33.3%), Neuronal avalanches (16.7%), Cancer epigenomics (44.4%) |
| **Negative** | ~14 | All 8 physical systems, Citations, Income/wealth, Stock returns, Internet AS, RNA viruses, City sizes |

**Headline finding:** The minimal discriminating feature set {F1, F2, F3, F4} — heritable string, duplication operator, deletion operator, and selection — jointly excludes all 8 physical power-law systems (earthquakes, stellar flares, turbulence, galaxy LF, stellar IMF, molecular clouds, sandpile/SOC, rivers) while admitting all confirmed biological and cultural innovation systems. Power laws are necessary but dramatically insufficient: of the ~85 systems surveyed, 40+ exhibit power-law statistics, but only ~22 (Inside + Plausible) satisfy the full BDIM admissibility criteria.

**Notable reclassifications (v2.1):** Scientific citations and income/wealth were reclassified from Inside to Negative based on mechanistic analysis (non-stationarity, Gibrat process without heritable string). CRISPR spacer arrays are introduced as a novel BDIM analog satisfying 11/13 features (84.6%). Endosymbiont genome reductions (Buchnera, Carsonella, N. equitans) confirm predicted BDIM exit when innovation rate approaches zero.

## F1-F14 Framework

Each feature corresponds to one or more formal specifications (E1-E26) in the FP4 proof. F11 is excluded from scoring.

| Feature | Description | Criticality | Formal Spec |
|---------|-------------|-------------|-------------|
| **F1** | Discrete heritable string | Essential | E2, E5 |
| **F2** | Duplication operator | Essential | E1 |
| **F3** | Deletion operator | Essential | E1 |
| **F4** | Selection on variants | Essential | E4, E5 |
| **F5** | Power-law family-size distribution (alpha > 1) | SHARP | E7 |
| **F6** | Balanced duplication/deletion rates | Important | E10 |
| **F7** | Positive innovation rate | Essential | E11 |
| **F8** | Conserved per-unit mutation rate (Drake K) | Supporting | E12 |
| **F9** | Error threshold / channel capacity | Supporting | E13, E14 |
| **F10** | Thermodynamic irreversibility (Landauer) | Universal | E15, E16 |
| **F11** | Accessible fitness landscape | **ORPHANED** | E17 |
| **F12** | Three or more fitness levels | Supporting | E18 |
| **F13** | Simple-to-complex trajectory | Supporting | E19 |
| **F14** | WGD insufficiency | Supporting | E20, E21 |

For full admissible region specifications (R_formal and R_empirical for all E1-E26), see `specs/FP4_AdmissibleRegion_Table.md`.

**Scoring protocol:** Each system x feature is scored check (satisfied with quantitative evidence), tilde (partially or ambiguously satisfied), cross (not satisfied), or dash (not applicable). Admissibility percentage = (check_count + 0.5 * tilde_count) / (applicable features out of 13, excluding F11) * 100.

**F5 standard (v2.1, R2):** All F5 assessments are documented in `data/processed/Table_S1_PowerLaw_Clauset_Audit.csv`. Power-law claims are confirmed only when: (a) Clauset (2009) MLE applied, (b) KS p-value > 0.1, (c) power law outperforms log-normal by DAIC > 2. Systems with Karev BDIM chi-squared fits but no Clauset MLE receive tilde for F5.

## Repository Structure

```
UTM-AR-001-Study/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── docs/
│   ├── UTM_AR_001_Report.md           # Primary report (v2.1, ~1700 lines)
│   ├── UTM_AR_001_Report.docx         # DOCX version with formatting
│   ├── V2_REVISION_SUMMARY.md         # R1-R12 revision change log (v2.0 -> v2.1)
│   ├── LEAN_REVISION_NOTES.md         # Required/advisory Lean code changes
│   └── archive/
│       ├── FP4_Cross_Domain_Validation_Report_v2.md  # Previous report version
│       └── FP4_Empirical_Validation_Master.md        # Original master report
├── data/
│   ├── raw/
│   │   └── systems_catalog.csv        # All ~48 system rows with domain, classification, notes, citations
│   └── processed/
│       ├── f14_scorecard.csv          # Complete F1-F14 scorecard for all systems
│       ├── feature_statistics.csv     # Coverage rates per feature across all systems
│       ├── classification_summary.csv # Counts by domain and classification
│       └── Table_S1_PowerLaw_Clauset_Audit.csv  # F5 Clauset audit (all systems)
├── figures/                           # (Placeholder for generated figures)
├── scripts/
│   ├── compute_admissibility.py       # Admissibility statistics computation
│   └── run_all.sh                     # Complete replication script
└── specs/
    └── FP4_AdmissibleRegion_Table.md  # E1-E26 admissible region specifications
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/sammolyneux-poppy/UTM-AR-001-Study.git
cd UTM-AR-001-Study

# Run the full admissibility computation
bash scripts/run_all.sh

# Or run the Python script directly
python3 scripts/compute_admissibility.py
```

## Dependencies

- Python 3.9+ (standard library only; no additional packages required)

## Nine Universality Domains

Systems are drawn from nine knowledge domains:

| Code | Domain | Example Systems |
|------|--------|----------------|
| **BIO** | Biological / Genetic Evolution | E. coli, S. cerevisiae, H. sapiens, archaea, plants, endosymbionts |
| **CHEM** | Chemical / Prebiotic | RNA World, autocatalytic networks |
| **IMMUNE** | Immune Repertoire | T cell, B cell, CRISPR spacer arrays |
| **LANG** | Language / Text | Natural language (Zipf) |
| **COMP** | Computational / Software | Software codebases, chess openings |
| **ECON** | Economic / Social | Firms, baby names, dog breeds, pottery, patents |
| **PHYS** | Physical | Earthquakes, stellar flares, turbulence, galaxy LF, sandpiles, rivers |
| **INFO** | Information Networks | WWW, citations, PPI networks, Internet AS |
| **NEUR** | Neural / Cognitive | Neuronal avalanches, cancer epigenomics |

## Risk Tier System

Each empirical specification E1-E26 carries a risk tier:

| Risk Tier | Count | Key Examples |
|-----------|:-----:|-------------|
| **LOW** | 18 | E1-E6 (structural/existential claims); E15-E16 (Landauer, 30-100x margin) |
| **MEDIUM** | 6 | E7 (power-law vs. log-normal); E9 (linearity sharpness); E12 (Drake K); E24 (phase transition) |
| **HIGH** | 2 | E10 (K-balance transient violations); E17 (fitness landscape — orphaned) |

## Citation

Molyneux, S. (2026). "Computational Universality of Recursive Genome Evolution." In preparation.

If citing this study specifically:

> Molyneux, S. (2026). UTM-AR-001: UTM Admissible Regions Study — Cross-domain validation of the FP4 admissibility framework across ~85 natural and cultural systems. Companion to "Computational Universality of Recursive Genome Evolution."

## Related

- **TIME-AR-001-Study** (temporal admissible regions): https://github.com/sammolyneux-poppy/TIME-AR-001-Study
- **FP4 Lean 4 Formal Proof:** "Computational Universality of Recursive Genome Evolution" (in preparation)

## License

MIT License — see `LICENSE` file for details.
