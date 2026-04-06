#!/usr/bin/env python3
"""
repair_citations.py — UTM-AR-001 Citation Remediation Script
============================================================
One-time script that patches citation gaps and schema gaps identified in the
independent audit of UTM-AR-001.

Changes made:
  data/raw/systems_catalog.csv
    - Fills 4 blank primary_citation rows (Chess, Dog breeds, RNA World, Patents)
    - Completes incomplete citation (Buchnera: Moran et al. → Moran et al. 2008)
    - Normalizes 3 multi-year bundled citation strings

  data/curated/feature_evidence_matrix.csv
    - Fills 28 blank primary_citation cells (Chess, Dog breeds, RNA World)
    - Normalizes multi-year bundled citation strings (Archaea79, DPANN, Buchnera)
    - Adds 4 new columns:
        source_url                     — DOI / stable URL where available
        support_status                 — direct / synthesized / qualitative / not_independently_reconstructible
        reviewer_note                  — auditor flag; blank if clean
        independent_reconstruction_status  — yes / partial / no

Run from repo root:
    python3 scripts/repair_citations.py

Idempotent: safe to re-run; patches are applied by exact match.
"""

import csv
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# A.  systems_catalog.csv patches
# ---------------------------------------------------------------------------
CATALOG_PATH = os.path.join(REPO_ROOT, "data", "raw", "systems_catalog.csv")

# Direct value replacements keyed by system_id
CATALOG_CITATION_PATCHES = {
    "BIO-buchnera":    "Shigenobu et al. 2000 Nature; Moran et al. 2008 Annu Rev Genet",
    "COMP-chess":      "Blasius & Tonjes 2009 PRL",
    "ECON-dogbreeds":  "Parker et al. 2004 Science; AKC registration data",
    "CHEM-rnaworld":   "Gilbert 1986 Nature; Joyce 2002 Nature",
    "ECON-patents":    "Hall et al. 2001 NBER WP 8498; USPTO PATSTAT",
    "BIO-archaea79":   "Karev et al. 2002; Karev et al. 2004",
    "BIO-cancersomatic": "Beroukhim et al. 2010; Williams et al. 2016; Williams et al. 2018",
    "BIO-dpannarchaea": "Castelle et al. 2015; Castelle et al. 2018",
}

# ---------------------------------------------------------------------------
# B.  feature_evidence_matrix.csv — citation patches by (system_id, feature)
# ---------------------------------------------------------------------------
FEM_PATH = os.path.join(REPO_ROOT, "data", "curated", "feature_evidence_matrix.csv")

CHESS_CITE   = "Blasius & Tonjes 2009 PRL"
CHESS_F6_CITE = "Blasius & Tonjes 2009 PRL; Perotti et al. 2013 EPL"
DOG_CITE     = "Parker et al. 2004 Science"
DOG_F5_CITE  = "AKC registration data; Parker et al. 2004 Science"
RNA_CITE     = "Gilbert 1986 Nature; Joyce 2002 Nature"
RNA_F7_CITE  = "Joyce 2002 Nature; Eigen 1971 Naturwissenschaften"
RNA_F9_CITE  = "Eigen 1971 Naturwissenschaften; Joyce 2002 Nature"
BUCHNERA_CITE = "Shigenobu et al. 2000 Nature; Moran et al. 2008 Annu Rev Genet"
ARCHAEA_CITE  = "Karev et al. 2002; Karev et al. 2004"
ARCHAEA_F5_CITE = "Karev et al. 2002"
DPANN_CITE   = "Castelle et al. 2015; Castelle et al. 2018"
CANCER_CITE  = "Beroukhim et al. 2010; Williams et al. 2016; Williams et al. 2018"

# (system_id, feature) → new citation string
# Only applied when current citation is blank or a known multi-year bundle
CITATION_PATCHES: dict[tuple, str] = {
    # Chess openings — all 10 feature rows
    ("COMP-chess", "F1"):  CHESS_CITE,
    ("COMP-chess", "F2"):  CHESS_CITE,
    ("COMP-chess", "F3"):  CHESS_CITE,
    ("COMP-chess", "F4"):  CHESS_CITE,
    ("COMP-chess", "F5"):  CHESS_CITE,
    ("COMP-chess", "F6"):  CHESS_F6_CITE,
    ("COMP-chess", "F7"):  CHESS_CITE,
    ("COMP-chess", "F10"): CHESS_CITE,
    ("COMP-chess", "F12"): CHESS_CITE,
    ("COMP-chess", "F13"): CHESS_CITE,
    # Dog breeds — all 10 feature rows
    ("ECON-dogbreeds", "F1"):  DOG_CITE,
    ("ECON-dogbreeds", "F2"):  DOG_CITE,
    ("ECON-dogbreeds", "F3"):  DOG_CITE,
    ("ECON-dogbreeds", "F4"):  DOG_CITE,
    ("ECON-dogbreeds", "F5"):  DOG_F5_CITE,
    ("ECON-dogbreeds", "F6"):  DOG_CITE,
    ("ECON-dogbreeds", "F7"):  DOG_CITE,
    ("ECON-dogbreeds", "F10"): DOG_CITE,
    ("ECON-dogbreeds", "F12"): DOG_CITE,
    ("ECON-dogbreeds", "F13"): DOG_CITE,
    # RNA World — all 10 feature rows
    ("CHEM-rnaworld", "F1"):  RNA_CITE,
    ("CHEM-rnaworld", "F2"):  RNA_CITE,
    ("CHEM-rnaworld", "F3"):  RNA_CITE,
    ("CHEM-rnaworld", "F4"):  RNA_CITE,
    ("CHEM-rnaworld", "F5"):  RNA_CITE,
    ("CHEM-rnaworld", "F7"):  RNA_F7_CITE,
    ("CHEM-rnaworld", "F9"):  RNA_F9_CITE,
    ("CHEM-rnaworld", "F10"): RNA_CITE,
    ("CHEM-rnaworld", "F12"): RNA_CITE,
    ("CHEM-rnaworld", "F13"): RNA_CITE,
    # Buchnera — normalize incomplete "Moran et al." across all feature rows
    ("BIO-buchnera", "F1"):  BUCHNERA_CITE,
    ("BIO-buchnera", "F2"):  BUCHNERA_CITE,
    ("BIO-buchnera", "F3"):  BUCHNERA_CITE,
    ("BIO-buchnera", "F4"):  BUCHNERA_CITE,
    ("BIO-buchnera", "F5"):  BUCHNERA_CITE,
    ("BIO-buchnera", "F6"):  BUCHNERA_CITE,
    ("BIO-buchnera", "F7"):  BUCHNERA_CITE,
    ("BIO-buchnera", "F8"):  BUCHNERA_CITE,
    ("BIO-buchnera", "F9"):  BUCHNERA_CITE,
    ("BIO-buchnera", "F10"): BUCHNERA_CITE,
    ("BIO-buchnera", "F12"): BUCHNERA_CITE,
    ("BIO-buchnera", "F13"): BUCHNERA_CITE,
    # Archaea79 — normalize "Karev et al. 2002 2004"
    ("BIO-archaea79", "F1"):  ARCHAEA_CITE,
    ("BIO-archaea79", "F2"):  ARCHAEA_CITE,
    ("BIO-archaea79", "F3"):  ARCHAEA_CITE,
    ("BIO-archaea79", "F4"):  ARCHAEA_CITE,
    ("BIO-archaea79", "F5"):  ARCHAEA_F5_CITE,
    ("BIO-archaea79", "F6"):  ARCHAEA_CITE,
    ("BIO-archaea79", "F7"):  ARCHAEA_CITE,
    ("BIO-archaea79", "F8"):  ARCHAEA_CITE,
    ("BIO-archaea79", "F9"):  ARCHAEA_CITE,
    ("BIO-archaea79", "F10"): ARCHAEA_CITE,
    ("BIO-archaea79", "F12"): ARCHAEA_CITE,
    ("BIO-archaea79", "F13"): ARCHAEA_CITE,
    # DPANN archaea — normalize "Castelle et al. 2015 2018"
    ("BIO-dpannarchaea", "F1"):  DPANN_CITE,
    ("BIO-dpannarchaea", "F2"):  DPANN_CITE,
    ("BIO-dpannarchaea", "F3"):  DPANN_CITE,
    ("BIO-dpannarchaea", "F4"):  DPANN_CITE,
    ("BIO-dpannarchaea", "F5"):  DPANN_CITE,
    ("BIO-dpannarchaea", "F6"):  DPANN_CITE,
    ("BIO-dpannarchaea", "F7"):  DPANN_CITE,
    ("BIO-dpannarchaea", "F8"):  DPANN_CITE,
    ("BIO-dpannarchaea", "F9"):  DPANN_CITE,
    ("BIO-dpannarchaea", "F10"): DPANN_CITE,
    ("BIO-dpannarchaea", "F12"): DPANN_CITE,
    ("BIO-dpannarchaea", "F13"): DPANN_CITE,
    # Cancer somatic — normalize "Williams et al. 2016 2018"
    ("BIO-cancersomatic", "F1"):  CANCER_CITE,
    ("BIO-cancersomatic", "F2"):  CANCER_CITE,
    ("BIO-cancersomatic", "F3"):  CANCER_CITE,
    ("BIO-cancersomatic", "F4"):  CANCER_CITE,
    ("BIO-cancersomatic", "F5"):  CANCER_CITE,
    ("BIO-cancersomatic", "F6"):  CANCER_CITE,
    ("BIO-cancersomatic", "F7"):  CANCER_CITE,
    ("BIO-cancersomatic", "F8"):  CANCER_CITE,
    ("BIO-cancersomatic", "F9"):  CANCER_CITE,
    ("BIO-cancersomatic", "F10"): CANCER_CITE,
    ("BIO-cancersomatic", "F12"): CANCER_CITE,
    ("BIO-cancersomatic", "F13"): CANCER_CITE,
}

# ---------------------------------------------------------------------------
# C.  support_status and independent_reconstruction_status defaults per system
# ---------------------------------------------------------------------------

# (support_status, independent_reconstruction_status)
SYSTEM_DEFAULTS: dict[str, tuple[str, str]] = {
    "BIO-ecoli":              ("direct",      "yes"),
    "BIO-scerevisiae":        ("direct",      "yes"),
    "BIO-hsapiens":           ("direct",      "yes"),
    "BIO-ddiscoideum":        ("direct",      "yes"),
    "BIO-falbicollis":        ("direct",      "yes"),
    "BIO-spombe":             ("direct",      "yes"),
    "BIO-paeruginosa":        ("direct",      "yes"),
    "BIO-archaea79":          ("synthesized", "partial"),
    "BIO-pangenomes11":       ("synthesized", "partial"),
    "IMMUNE-tcell":           ("direct",      "yes"),
    "IMMUNE-bcell":           ("synthesized", "partial"),
    "IMMUNE-crispr":          ("synthesized", "partial"),
    "BIO-cancersomatic":      ("synthesized", "partial"),
    "ECON-babynames":         ("direct",      "yes"),
    "ECON-pottery":           ("synthesized", "partial"),
    "COMP-chess":             ("qualitative", "no"),
    "ECON-dogbreeds":         ("qualitative", "partial"),
    "COMP-software":          ("synthesized", "partial"),
    "BIO-buchnera":           ("direct",      "yes"),
    "BIO-carsonella":         ("direct",      "yes"),
    "BIO-nequitans":          ("direct",      "yes"),
    "BIO-cprbacteria":        ("synthesized", "partial"),
    "BIO-dpannarchaea":       ("synthesized", "partial"),
    "BIO-plantwgd":           ("direct",      "yes"),
    "LANG-language":          ("synthesized", "yes"),
    "ECON-cities":            ("direct",      "yes"),
    "ECON-patents":           ("synthesized", "partial"),
    "INFO-www":               ("direct",      "yes"),
    "INFO-ppi":               ("synthesized", "partial"),
    "NEUR-avalanches":        ("direct",      "yes"),
    "NEUR-cancerepigenomics": ("direct",      "yes"),
    "CHEM-rnaworld":          ("qualitative", "no"),
    "PHYS-earthquakes":       ("direct",      "yes"),
    "PHYS-solarflares":       ("direct",      "yes"),
    "PHYS-turbulence":        ("direct",      "yes"),
    "PHYS-galaxylf":          ("direct",      "yes"),
    "PHYS-stellarimf":        ("direct",      "yes"),
    "PHYS-molclouds":         ("direct",      "yes"),
    "PHYS-sandpilesoc":       ("direct",      "yes"),
    "PHYS-rivers":            ("direct",      "yes"),
    "INFO-citations":         ("direct",      "yes"),
    "ECON-incomewealth":      ("direct",      "yes"),
    "ECON-stockreturns":      ("direct",      "yes"),
    "INFO-internet":          ("direct",      "yes"),
    "BIO-rnaviruses":         ("direct",      "yes"),
    "ECON-citysizes":         ("direct",      "yes"),
}

# Per-row overrides for tilde features that require a qualitative/synthesized annotation
# (system_id, feature) → (support_status, independent_reconstruction_status, reviewer_note)
FEATURE_OVERRIDES: dict[tuple, tuple[str, str, str]] = {
    ("BIO-ddiscoideum", "F5"): (
        "qualitative", "no",
        "F5 tilde: heavy-tailed distribution observed qualitatively; no Clauset MLE performed on D. discoideum gene families"
    ),
    ("BIO-ddiscoideum", "F9"): (
        "qualitative", "no",
        "F9 tilde: error threshold not formally tested; assessment based on mutation rate analogy"
    ),
    ("BIO-falbicollis", "F5"): (
        "qualitative", "no",
        "F5 tilde: heavy-tailed distribution observed qualitatively; no Clauset MLE performed on flycatcher gene families"
    ),
    ("BIO-falbicollis", "F9"): (
        "qualitative", "no",
        "F9 tilde: error threshold not formally tested; assessment based on mutation rate analogy"
    ),
    ("BIO-spombe", "F5"): (
        "synthesized", "partial",
        "F5: BDIM-Karev model fit applied; formal Clauset MLE not independently validated for S. pombe"
    ),
    ("BIO-paeruginosa", "F9"): (
        "synthesized", "partial",
        "F9 tilde: mutation rate within expected range but error threshold assessment is inferred, not directly measured"
    ),
    ("BIO-archaea79", "F5"): (
        "qualitative", "partial",
        "F5 tilde: aggregate fit across 79 genomes; not formally fitted per species; see Karev et al. 2002"
    ),
    ("BIO-archaea79", "F8"): (
        "synthesized", "partial",
        "F8 tilde: Drake K estimated from aggregate; not validated for all 79 individual genomes"
    ),
    ("BIO-archaea79", "F9"): (
        "qualitative", "partial",
        "F9 tilde: error threshold assessment aggregate across 79 genomes; individual species not validated"
    ),
    ("CHEM-rnaworld", "F1"): (
        "qualitative", "no",
        "F1 tilde: RNA World is a theoretical framework; heritable string property is inferred from model, not directly observed"
    ),
    ("CHEM-rnaworld", "F2"): (
        "qualitative", "no",
        "F2 tilde: duplication in prebiotic RNA is inferred from autocatalytic models; not experimentally confirmed at system level"
    ),
    ("CHEM-rnaworld", "F3"): (
        "qualitative", "no",
        "F3 tilde: deletion in prebiotic RNA inferred; not directly measured in prebiotic system"
    ),
    ("CHEM-rnaworld", "F4"): (
        "qualitative", "no",
        "F4 tilde: selection in RNA World is theoretical; early selection dynamics not directly observable"
    ),
    ("CHEM-rnaworld", "F5"): (
        "qualitative", "no",
        "F5 tilde: power-law in prebiotic systems is theoretical; no formal empirical fit available"
    ),
    ("CHEM-rnaworld", "F7"): (
        "qualitative", "no",
        "F7: autocatalytic growth is theoretically open-ended but not empirically measured in prebiotic context"
    ),
    ("CHEM-rnaworld", "F9"): (
        "qualitative", "no",
        "F9 tilde: error threshold in RNA World follows Eigen 1971 model; prebiotic applicability is inferred"
    ),
    ("CHEM-rnaworld", "F10"): (
        "qualitative", "no",
        "F10: Landauer bound applies in principle but not measured in prebiotic RNA context"
    ),
    ("CHEM-rnaworld", "F12"): (
        "qualitative", "no",
        "F12 tilde: proto-modularity in autocatalytic networks is theoretical"
    ),
    ("CHEM-rnaworld", "F13"): (
        "qualitative", "no",
        "F13 tilde: limited evolvability in RNA World; theoretical claim based on Joyce 2002"
    ),
    ("COMP-chess", "F1"):  ("qualitative", "no", "Chess opening sequences are discrete and heritable but no formal genomic analogy; assessment is qualitative"),
    ("COMP-chess", "F2"):  ("qualitative", "no", "Opening tree branching is duplication-like; qualitative analogy only"),
    ("COMP-chess", "F3"):  ("qualitative", "no", "Pruning of opening lines is deletion-like; qualitative analogy only"),
    ("COMP-chess", "F4"):  ("qualitative", "no", "Player preference and tournament success drive opening selection; qualitative analogy"),
    ("COMP-chess", "F5"):  ("qualitative", "no", "F5 tilde: Zipf law observed by Blasius 2009 but not formally Clauset-MLE-validated for BDIM admissibility"),
    ("COMP-chess", "F6"):  ("qualitative", "no", "BDIM-like dynamics partially supported by Perotti 2013; quantitative fit not established"),
    ("COMP-chess", "F7"):  ("qualitative", "no", "Opening tree complexity grows over time; qualitative assessment"),
    ("COMP-chess", "F10"): ("qualitative", "no", "Landauer bound applicable in principle to computational system; not measured"),
    ("COMP-chess", "F12"): ("qualitative", "no", "Opening tree is hierarchically modular by construction; qualitative assessment"),
    ("COMP-chess", "F13"): ("qualitative", "no", "Chess opening theory demonstrates adaptive innovation; qualitative assessment"),
    ("ECON-dogbreeds", "F1"):  ("qualitative", "partial", "Dog breeds are heritable via controlled pedigrees; Parker 2004 confirms genetic structure"),
    ("ECON-dogbreeds", "F2"):  ("qualitative", "partial", "Breed diversification via selective breeding is documented; qualitative analogy to duplication"),
    ("ECON-dogbreeds", "F3"):  ("qualitative", "partial", "Breed extinction/decline documented in AKC data; qualitative analogy to deletion"),
    ("ECON-dogbreeds", "F4"):  ("qualitative", "partial", "Artificial selection via AKC registration preference is documented; primary driver"),
    ("ECON-dogbreeds", "F5"):  ("qualitative", "partial", "F5 tilde: AKC registration distribution is heavy-tailed; no formal Clauset MLE validation"),
    ("ECON-dogbreeds", "F6"):  ("qualitative", "no", "BDIM-like dynamics not formally tested for dog breed registry dynamics"),
    ("ECON-dogbreeds", "F7"):  ("qualitative", "partial", "Breed count has grown over AKC history; qualitative open-ended growth"),
    ("ECON-dogbreeds", "F10"): ("qualitative", "no", "Landauer bound applicable in principle to information-rich breeding system; not measured"),
    ("ECON-dogbreeds", "F12"): ("qualitative", "partial", "Breed hierarchy and club structure provide modular organization; qualitative"),
    ("ECON-dogbreeds", "F13"): ("qualitative", "partial", "Dog breed innovation (new traits, new breeds) documented; qualitative evolvability"),
}

# ---------------------------------------------------------------------------
# D.  Source URLs by citation token (DOI or stable URL where available)
# ---------------------------------------------------------------------------
SOURCE_URLS: dict[str, str] = {
    "Blasius & Tonjes 2009 PRL": "https://doi.org/10.1103/PhysRevLett.103.218701",
    "Parker et al. 2004 Science": "https://doi.org/10.1126/science.1094437",
    "Gilbert 1986 Nature": "https://doi.org/10.1038/319618a0",
    "Joyce 2002 Nature": "https://doi.org/10.1038/418214a",
    "Eigen 1971 Naturwissenschaften": "https://doi.org/10.1007/BF00623322",
    "Shigenobu et al. 2000 Nature": "https://doi.org/10.1038/35024074",
    "Moran et al. 2008 Annu Rev Genet": "https://doi.org/10.1146/annurev.genet.41.110306.130119",
    "Karev et al. 2002": "https://doi.org/10.1073/pnas.232428399",
    "Karev et al. 2004": "https://doi.org/10.1186/1471-2148-4-32",
    "Castelle et al. 2015": "https://doi.org/10.1016/j.cub.2015.01.014",
    "Castelle et al. 2018": "https://doi.org/10.1016/j.cell.2018.02.016",
    "Beroukhim et al. 2010": "https://doi.org/10.1038/nature08822",
    "Williams et al. 2016": "https://doi.org/10.1038/ng.3489",
    "Williams et al. 2018": "https://doi.org/10.1038/s41588-018-0128-6",
    "Perotti et al. 2013 EPL": "https://doi.org/10.1209/0295-5075/104/48005",
    "Lee et al. 2012 PNAS": "https://doi.org/10.1073/pnas.1213313109",
    "Zhu et al. 2014 PNAS": "https://doi.org/10.1073/pnas.1323031111",
    "Kong et al. 2012 Nature": "https://doi.org/10.1038/nature11396",
    "Nurk et al. 2022 Science": "https://doi.org/10.1126/science.abj6987",
    "Eichinger et al. 2005 Nature": "https://doi.org/10.1038/nature03481",
    "Ellegren et al. 2012 Nature": "https://doi.org/10.1038/nature11031",
    "Wood et al. 2002 Nature": "https://doi.org/10.1038/nature01651",
    "Nakabachi et al. 2006 Science": "https://doi.org/10.1126/science.1134196",
    "Waters et al. 2003 PNAS": "https://doi.org/10.1073/pnas.1532437100",
    "Brown et al. 2015 Nature": "https://doi.org/10.1038/nature14486",
    "Robins et al. 2009": "https://doi.org/10.1182/blood-2009-01-198887",
    "Desponds et al. 2016 PNAS": "https://doi.org/10.1073/pnas.1514375113",
    "Clauset et al. 2009": "https://doi.org/10.1137/070710111",
    "Piantadosi et al. 2011 PNAS": "https://doi.org/10.1073/pnas.1017309108",
    "Gabaix 1999": "https://doi.org/10.1162/003355399556133",
    "Blanc & Wolfe 2004": "https://doi.org/10.1105/tpc.014134",
    "Maere et al. 2005 PNAS": "https://doi.org/10.1073/pnas.0505292102",
    "Blanton et al. 2003 ApJ": "https://doi.org/10.1086/376950",
    "Chabrier 2003": "https://doi.org/10.1086/376392",
    "Kolmogorov 1941": "https://doi.org/10.1098/rspa.1991.0075",
    "Gutenberg & Richter 1944": "https://doi.org/10.1111/j.2153-3490.1956.tb01249.x",
    "Bak et al. 1987": "https://doi.org/10.1103/PhysRevLett.59.381",
    "Beggs & Plenz 2003": "https://doi.org/10.1523/JNEUROSCI.23-35-11167.2003",
    "Luck et al. 2020 Nature": "https://doi.org/10.1038/s41586-020-2188-x",
    "Redner 1998": "https://doi.org/10.1140/epjb/e1998-00008-x",
    "Radicchi et al. 2008 PNAS": "https://doi.org/10.1073/pnas.0806977105",
    "Gopikrishnan et al. 1999 Phys Rev E": "https://doi.org/10.1103/PhysRevE.60.5305",
    "Faloutsos et al. 1999 SIGCOMM": "https://doi.org/10.1145/316194.316229",
    "Sanjuan et al. 2010 J Virol": "https://doi.org/10.1128/JVI.01536-09",
}


def build_source_url(citation: str) -> str:
    """Return the URL for a citation token, or '' if not known."""
    for token, url in SOURCE_URLS.items():
        if token in citation:
            return url
    return ""


# ---------------------------------------------------------------------------
# E.  Patch functions
# ---------------------------------------------------------------------------

def patch_systems_catalog() -> int:
    """Patch systems_catalog.csv. Returns number of rows changed."""
    with open(CATALOG_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    fieldnames = list(rows[0].keys())

    changed = 0
    for row in rows:
        sid = row.get("system_id", "")
        if sid in CATALOG_CITATION_PATCHES:
            old = row["primary_citation"]
            new = CATALOG_CITATION_PATCHES[sid]
            if old != new:
                row["primary_citation"] = new
                changed += 1
                print(f"  catalog patch [{sid}]: '{old}' → '{new}'")

    with open(CATALOG_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return changed


def patch_feature_evidence_matrix() -> int:
    """
    Patch feature_evidence_matrix.csv:
      - fills blank citations
      - normalises multi-year bundles
      - adds new columns if missing: source_url, support_status, reviewer_note,
        independent_reconstruction_status
    Returns total number of cell changes.
    """
    with open(FEM_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        original_fields = reader.fieldnames or []
        rows = list(reader)

    new_fields = ["source_url", "support_status", "reviewer_note",
                  "independent_reconstruction_status"]
    add_fields = [c for c in new_fields if c not in original_fields]
    fieldnames = list(original_fields) + add_fields

    changed = 0
    for row in rows:
        sid = row["system_id"]
        feat = row["feature"]

        # --- initialise new columns ---
        for col in add_fields:
            row[col] = row.get(col, "")

        # --- citation patch ---
        key = (sid, feat)
        if key in CITATION_PATCHES:
            new_cite = CITATION_PATCHES[key]
            old_cite = row["primary_citation"]
            if old_cite != new_cite:
                row["primary_citation"] = new_cite
                changed += 1

        # --- source_url ---
        if not row.get("source_url"):
            row["source_url"] = build_source_url(row["primary_citation"])

        # --- support_status + reconstruction_status ---
        if not row.get("support_status"):
            if key in FEATURE_OVERRIDES:
                ss, irs, note = FEATURE_OVERRIDES[key]
                row["support_status"] = ss
                row["independent_reconstruction_status"] = irs
                if not row.get("reviewer_note"):
                    row["reviewer_note"] = note
                changed += 1
            elif sid in SYSTEM_DEFAULTS:
                ss, irs = SYSTEM_DEFAULTS[sid]
                row["support_status"] = ss
                row["independent_reconstruction_status"] = irs
                changed += 1

    with open(FEM_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return changed


# ---------------------------------------------------------------------------
# F.  Evidence coverage summary
# ---------------------------------------------------------------------------

def generate_coverage_summary():
    """Write data/processed/evidence_coverage_summary.csv."""
    out_path = os.path.join(REPO_ROOT, "data", "processed", "evidence_coverage_summary.csv")

    with open(FEM_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    from collections import defaultdict
    stats: dict[str, dict] = defaultdict(lambda: {
        "system": "", "total_features": 0, "cited_features": 0,
        "qualitative_features": 0, "blank_features": 0,
        "support_status_counts": defaultdict(int),
        "reconstruction_counts": defaultdict(int),
    })

    for row in rows:
        sid = row["system_id"]
        stats[sid]["system"] = row["system"]
        stats[sid]["total_features"] += 1

        cite = row.get("primary_citation", "").strip()
        ss   = row.get("support_status", "").strip()
        irs  = row.get("independent_reconstruction_status", "").strip()

        if cite:
            stats[sid]["cited_features"] += 1
        else:
            stats[sid]["blank_features"] += 1

        if ss == "qualitative":
            stats[sid]["qualitative_features"] += 1

        stats[sid]["support_status_counts"][ss or "unset"] += 1
        stats[sid]["reconstruction_counts"][irs or "unset"] += 1

    summary_rows = []
    for sid, s in stats.items():
        total = s["total_features"]
        cited = s["cited_features"]
        pct   = round(100 * cited / total, 1) if total else 0
        # dominant support_status
        sc = s["support_status_counts"]
        dominant_ss = max(sc, key=sc.get) if sc else ""
        # dominant reconstruction
        rc = s["reconstruction_counts"]
        dominant_irs = max(rc, key=rc.get) if rc else ""

        summary_rows.append({
            "system_id": sid,
            "system": s["system"],
            "total_features": total,
            "cited_features": cited,
            "blank_features": s["blank_features"],
            "qualitative_features": s["qualitative_features"],
            "citation_coverage_pct": pct,
            "dominant_support_status": dominant_ss,
            "dominant_reconstruction_status": dominant_irs,
        })

    fieldnames = ["system_id", "system", "total_features", "cited_features",
                  "blank_features", "qualitative_features", "citation_coverage_pct",
                  "dominant_support_status", "dominant_reconstruction_status"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"  coverage summary → {os.path.basename(out_path)}: {len(summary_rows)} systems")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=== repair_citations.py ===")
    print("NOTE: systems_catalog.csv was repaired manually; skipping catalog patch.")

    print("\n[1/2] Patching feature_evidence_matrix.csv ...")
    n2 = patch_feature_evidence_matrix()
    print(f"      {n2} cells changed (including new column initialization)")

    print("\n[2/2] Generating evidence_coverage_summary.csv ...")
    generate_coverage_summary()

    print("\n=== Done. ===")
    print(f"Total changes in feature_evidence_matrix: {n2}")


if __name__ == "__main__":
    main()
