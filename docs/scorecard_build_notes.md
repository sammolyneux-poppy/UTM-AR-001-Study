# Scorecard Build Notes

**Study:** UTM-AR-001 — UTM Admissible Regions Study
**Date:** 2026-04-06
**Source file:** `data/processed/f14_scorecard.csv` (46 rows, 13 active features)

---

## 1. Scorecard Construction Methodology

The F1-F14 admissibility scorecard is the primary data product of the UTM-AR-001 study. Each of the 46 rows represents a system (or grouped system aggregate) assessed against 13 active features (F1-F10, F12-F14). F11 (accessible fitness landscape) is excluded from scoring because the corresponding Lean axiom (`bio_landscapes_monotone`) is orphaned in the FP4 proof; it is retained as a supplementary annotation column only.

**Assessment protocol.** Each system x feature cell was scored by expert review of published peer-reviewed literature. The four possible marks are:

| Mark | Meaning | Numeric value |
|------|---------|:-------------:|
| check | Feature satisfied with quantitative evidence and primary citation | 1.0 |
| tilde | Partially or ambiguously satisfied; evidence exists but is incomplete or methodologically contested | 0.5 |
| cross | Feature not satisfied based on available evidence | 0.0 |
| dash | Feature not applicable to this system type | excluded |

**Admissibility formula:**

```
percent_score = (check_count + 0.5 * tilde_count) / applicable_features * 100
```

where `applicable_features` is the count of features scored check, tilde, or cross (i.e., all non-dash features out of the 13 active features). Classification thresholds and the additional requirement that F1-F4 are all satisfied for Inside status are documented in the README and primary report.

**Citation linkage.** Every system row in the scorecard has a corresponding entry in `data/raw/systems_catalog.csv` with domain, sub-domain, classification, notes, and primary citation(s). Per-feature evidence notes are available in `data/curated/feature_evidence_matrix.csv`.

---

## 2. System Selection Criteria

The 46 scorecard rows (~85 individual systems after expansion) were selected to provide broad coverage across domains, taxonomic groups, and expected classification outcomes.

**Biological systems (BIO).** Selected to span major branches of cellular life:
- Bacteria: *E. coli*, *P. aeruginosa*, Pan-genomes (11 spp)
- Archaea: Archaea (79 genomes across 23 species)
- Eukaryotes: *S. cerevisiae*, *S. pombe* (fungi), *H. sapiens*, *F. albicollis* (vertebrates), *D. discoideum* (social amoeba), Plant WGD (polyploidy)
- Endosymbionts: *Buchnera*, *Carsonella*, *N. equitans* (selected as predicted BDIM exit cases)
- Ultra-reduced lineages: CPR bacteria, DPANN archaea (selected as predicted boundary cases)
- Other: Cancer somatic evolution, RNA viruses

**Immune repertoires (IMMUNE).** T cell and B cell repertoires (adaptive immune), CRISPR spacer arrays (prokaryotic adaptive immune) — selected to test whether immune diversification satisfies BDIM criteria independently of germline evolution.

**Physical systems (PHYS).** Eight systems (earthquakes, solar flares, turbulence, galaxy luminosity function, stellar IMF, molecular clouds, sandpile/SOC, rivers) — selected as **negative controls**. These exhibit well-documented power-law statistics but lack heritable information strings, duplication/deletion operators, and selection. They are expected to satisfy F5 (power law) while failing F1-F4.

**Cultural and computational systems (COMP, LANG, ECON).** Baby names, pottery typologies, chess openings, dog breeds, software codebases, language — selected to test whether the BDIM framework extends to non-genetic replicator systems with discrete heritable units and copying/deletion dynamics.

**Economic and information systems (ECON, INFO).** Cities, patents, citations, income/wealth, stock returns, WWW hyperlinks, PPI networks, Internet AS — selected to test boundary conditions and identify systems where power-law statistics arise from non-BDIM mechanisms (e.g., Gibrat multiplicative growth, preferential attachment).

---

## 3. Grouped Rows

Two scorecard rows represent aggregated assessments rather than single systems:

**Archaea (79 genomes).** This row aggregates BDI3 model fits from Karev et al. (2002, 2004) across 79 archaeal genomes spanning 23 species (including *Sulfolobus solfataricus*, *Methanocaldococcus jannaschii*, *Halobacterium salinarum*, *Thermoplasma acidophilum*, *Aeropyrum pernix*, *Pyrococcus horikoshii*, *Pyrococcus furiosus*, and 16 additional species). The assessment reflects aggregate BDIM fit quality: chi-squared goodness-of-fit was confirmed across all 79 genomes, but Clauset MLE was not applied (hence F5 = tilde). F8 and F9 receive tilde due to limited per-species mutation rate data. The full species list is in `data/processed/systems_expansion.csv`.

**Pan-genomes (11 spp).** This row aggregates Heaps' law exponents from Tettelin et al. (2008) and Land et al. (2015) across 11 bacterial species (*E. coli*, *S. aureus*, *S. pneumoniae*, *H. pylori*, *N. meningitidis*, *B. anthracis*, *L. pneumophila*, *C. trachomatis*, *P. aeruginosa*, *M. tuberculosis*, *S. agalactiae*). All 11 species exhibit open pan-genome dynamics (Heaps' law exponents 0.08-0.64), confirming ongoing BDIM innovation. F9 receives tilde because error-threshold analysis has not been performed for all 11 species individually.

Both grouped rows are documented in the systems expansion mapping so that the "46 rows representing ~85 systems" accounting is transparent and auditable.

---

## 4. Expert Curation Rationale

The scorecard is a human-curated expert assessment, not an automatically computed output. This is a deliberate methodological choice, not a limitation.

**Why automated scoring is not feasible.** Several features require qualitative domain expertise that cannot be reduced to a computable metric:

- F1 (discrete heritable string): Determining whether a system transmits discrete, copyable information units requires understanding the system's mechanistic basis — DNA sequences, spacer arrays, cultural memes, or codebases each require domain-specific assessment.
- F6 (balanced duplication/deletion rates): Assessing whether a system maintains approximate K-balance requires interpreting heterogeneous rate measurements across different experimental methodologies.
- F13 (simple-to-complex trajectory): Evaluating evolutionary complexity trajectories requires synthesizing evidence from phylogenetics, paleontology, and comparative genomics.

**Why this is standard practice.** Expert-curated assessment matrices are the established methodology for cross-domain meta-analyses in evolutionary biology, ecology, and systems science. Comparable approaches include:

- Comparative phylogenetic character matrices (Maddison & Maddison, Mesquite)
- Systematic review evidence tables in biomedical meta-analyses (Cochrane methodology)
- Technology readiness level (TRL) assessments in engineering

The key safeguards against subjectivity are: (a) all assessments are backed by cited literature, (b) the scoring protocol is pre-specified and documented, (c) the full per-feature evidence matrix is published alongside the scorecard, and (d) the computation script independently validates internal consistency.

---

## 5. Version History

| Version | Date | Changes |
|---------|------|---------|
| **v1.0** | 2026-03 | Initial 48-system assessment with 14-feature scoring (F1-F14 all active) |
| **v2.0** | 2026-04-01 | Revised to 46 systems. Citations and income/wealth reclassified from Inside to Negative based on mechanistic analysis (Gibrat process, no heritable string). "Cheese" and other legacy entries removed. City sizes added as separate Negative entry. |
| **v2.1** | 2026-04-04 | R1-R12 peer review revisions incorporated. F11 orphaned and excluded from scoring formula. F5 Clauset standard applied uniformly (Table S1 audit created). Six system groups downgraded F5 from check to tilde. All admissibility percentages recomputed on 13-feature denominator. See `docs/V2_REVISION_SUMMARY.md` for full change log. |

---

## Reproducibility

The scorecard can be validated by running:

```bash
python3 scripts/compute_admissibility.py
```

This script reads `data/processed/f14_scorecard.csv`, recomputes all derived statistics (classification counts, feature coverage rates, domain breakdowns), and confirms internal consistency. It does not generate the scorecard itself — that is the product of the literature review documented above.
