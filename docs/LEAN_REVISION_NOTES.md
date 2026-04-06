# Lean Axiom Revision Notes

**Generated during:** FP4 Cross-Domain Validation Report revision v2.0 → v2.1
**Date:** 2026-04-04
**Priority ordering:** HIGH items first, then advisory notes

---

## LEAN-REVISION-E10 (REQUIRED)

**Source:** R3 (E10 K-Balance Section Expansion)
**Priority:** HIGH
**File:** `FractalGenesis/GeneFamilyProcess.lean:290-296`
**Current:** `IsBalancedOrganism K ≤ 5` (no timescale qualifier)

**Required change:** Add doc-string specifying evolutionary-steady-state scope:

```lean
/--
  K is defined as the evolutionary-steady-state dup/del ratio
  (≥10⁴ generations). Instantaneous K values from MA experiments
  or adaptive amplification episodes (e.g., Nilsson et al. 2005
  Salmonella K≈150; Reams & Roth 2015 amplification-divergence
  intermediates) may exceed this bound transiently without
  violating the predicate.

  The steady-state scope is justified by the Karev attractor
  (Karev et al. 2002, 2004): in a BDIM with μ > λ, the
  stationary genome size distribution has finite mean, and
  transient K≫5 states are driven off-attractor by strong
  selection and return as selection relaxes.

  All MA-line steady-state measurements across 6+ organisms
  give K < 3.0 (see FP4 Validation Report v2.1, Section 8.2).
-/
```

**Rationale:** Section 8.2 of the validation report now includes a three-part analysis (8.2.1 Timescale Problem, 8.2.2 Reams & Roth, 8.2.3 Karev Attractor) that depends on the predicate being explicitly scoped to evolutionary steady state. Without this doc-string, a reader of the Lean code could reasonably interpret `IsBalancedOrganism K ≤ 5` as applying to instantaneous measurements, which would be falsified by the Nilsson (2005) Salmonella data.

**Cross-references:** Report Section 8.2.1, 8.2.2, 8.2.3

---

## LEAN-REVISION-E17 (ADVISORY)

**Source:** R1 (F11 Orphaned-Status Resolution)
**Priority:** MEDIUM (documentation only, no proof impact)
**File:** `FractalGenesis/BiologicalInstantiations.lean` (location of `bio_landscapes_monotone`)
**Current:** Axiom `bio_landscapes_monotone` present in axiom register, status ORPHANED

**Advisory note:** No code change required. The axiom remains in the formal architecture but is documented as orphaned. The v2.1 validation report excludes F11 from the scoring formula (Option A), using a 13-feature denominator.

Suggested doc-string addition:
```lean
-- ORPHANED AXIOM (v2.1): bio_landscapes_monotone is retained in the
-- axiom register for future proof versions but is NOT consumed by any
-- active proof step. It does not contribute to the headline theorem
-- biological_evolution_is_utm. Empirical support is documented in
-- FP4 Validation Report v2.1 Section 8 (F11) as a supplementary annotation.
```

---

## LEAN-REVISION-E7-BOUNDARY (ADVISORY)

**Source:** R6 (LANG Mechanistic Treatment)
**Priority:** LOW (documentation only)
**File:** `FractalGenesis/BDIMProperties.lean` (location of `IsParetoTail`)
**Current:** `IsParetoTail` requires α > 1 (strict inequality)

**Advisory note:** Natural language Zipf's law has α ≈ 1.0, which sits at the formal SHARP boundary. The strict inequality correctly excludes Zipf at α = 1.0. This is by design, not a defect. Linguistic systems are correctly classified as Boundary.

Suggested doc-string addition:
```lean
-- NOTE (v2.1): The strict inequality α > 1 is intentional.
-- Systems with α = 1.0 (Zipf's law, city sizes) are at the
-- formal boundary and are correctly classified as Boundary, not Inside.
```

---

*Notes collected 2026-04-04. Only LEAN-REVISION-E10 requires a code change; all others are advisory documentation notes.*
