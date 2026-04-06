# FP4 Admissible Region Table — Master Reference

**Date:** 2026-04-03 (Robustness Phase 2)
**Proof state:** 61 files, 0 sorry, 13 active axioms + 3 BI criteria

## Admissible Regions for All Empirical Specifications

| ID | Parameter | R_formal (admissible) | R_empirical (measured) | Sensitivity | Status |
|----|-----------|----------------------|----------------------|-------------|--------|
| E1 | RecursiveMutation ops | Any system with deletion + duplication | All DNA-based organisms (Ohno 1970) | Non-monotone | ✅ CORRECT |
| E2 | Genome encoding | Any finite alphabet | {A,C,G,T} 4-symbol → 2 bits/nt | Non-monotone | ✅ CORRECT |
| E3 | validTrajectory | Any step-reachable sequence | All evolutionary lineages | Definitional | ✅ CORRECT |
| E4 | NaturalisticAES | pop ≥ 2, any non-trivial fitness | All populations with selection | Proof-engineering | ✅ CORRECT |
| E5 | Selection g ≠ [] | Non-empty genome, genuine fitness ineq | All viable organisms | Minimal guard | ✅ CORRECT |
| E6 | Unbounded genome | No global length cap | Class universality | Standard | ✅ CORRECT |
| E7 | IsParetoTail α > 1 | α ∈ (1, +∞) | α ∈ [1.5, 3.0] (Karev 2002) | Sharp at α = 1 | ✅ CORRECT |
| E8 | IsBalanced | Unrestricted (implied by linearity) | N/A | Redundant | ⚠️ REDUNDANT |
| E9 | IsLinearBDIM | Affine rates, positive coefficients | BDIM organisms at steady state | **SHARP** | ✅ ESSENTIAL |
| E10 | IsBalancedOrganism K | K ∈ (0, +∞) | K ∈ [1.2, 4.8] (Lynch & Conery 2000) | Not consumed | ✅ RELAXED P2 |
| E11 | innov_rate | (0, +∞) | [10^-11, 10^-8] per gene/gen | Not consumed | ✅ RELAXED P2 |
| E12 | Drake K | (0, +∞) | K ≈ 2.5-10 (Drake 1991) | Not consumed | ✅ RELAXED P2 |
| E13 | AtChannelCapacity | Unrestricted (type guard only) | DNA microbes at error threshold | Inert | ⚠️ INERT |
| E14 | aesChannelCapacity | N/A (proved theorem) | N * ln 2 nats | Mathematical truth | ✅ PROVED |
| E15 | Landauer principle | dissipated > 0, ΔS > 0 | 30-100× above minimum | Near-maximal | ✅ ROBUST |
| E16 | Replication energy | energy_per_bit > ln 2 | 20-50 kBT/bp (Phillips 2012) | 30-70× margin | ✅ ROBUST |
| E17 | Fitness landscape | N/A (relocated to BI) | Szendro 2013: 50-75% | ORPHANED → BI | ✅ RELOCATED P2 |
| E18 | 3 fitness levels | N/A (relocated to BI) | Part of E17 | ORPHANED → BI | ✅ RELOCATED P2 |
| E19 | Complexity trajectory | N/A (relocated to BI) | Szathmáry 1995 | ORPHANED → BI | ✅ RELOCATED P2 |
| E20 | WGD diversity | N/A (relocated to BI) | Guards E19 | ORPHANED → BI | ✅ RELOCATED P2 |
| E21 | geneFamilyCount | N/A (supports E19 in BI) | Proxy measure | Moot | ✅ IN BI |
| E22 | indel_size_bounded | N/A (retired) | ≤ 50 bp (Denver 2004) | Dead axiom | ✅ RETIRED P2 |
| E23 | indelRateLinearWithTime | Finite support of stationary dist | Denver 2004 rates | Slightly over-spec | ✅ ~CORRECT |
| E24 | dup_rate = 0 | {0} exactly | Phase transition | **SHARP** | ✅ ESSENTIAL |
| E25 | Asexual scope | Structural (single-parent) | Lower bound on power | Structural | ✅ CORRECT |
| E26 | Cambrian constants | N/A (archived) | Historical context only | Retired | ✅ ARCHIVED |

## Summary Statistics

| Category | Count | Description |
|----------|-------|-------------|
| Correctly specified | 8 | E1-E6, E23, E25 — structural/definitional |
| Genuinely essential (sharp) | 3 | E7 (α>1), E9 (linearity), E24 (dup=0) |
| Maximally robust | 2 | E15, E16 (Landauer — 30-100× margin) |
| Proved theorem | 1 | E14 (aesChannelCapacity) |
| Relaxed to maximal region | 3 | E10, E11, E12 (K>0 or >0) |
| Relocated to BI | 4 | E17-E20 (orphaned → BiologicalInstantiation) |
| Retired/archived | 3 | E22 (dead), E26 (archived), E21 (moot) |
| Redundant/inert | 2 | E8 (redundant), E13 (inert) |

## Publication Framing

> FP4 does not depend on exact point estimates from present-day biology. The computability spine requires zero empirical parameters. The power-law arm requires only structural conditions (linear BDIM rates with positive innovation) — no specific numerical values. The thermodynamic arm requires only a directional inequality with a 30-100× empirical safety margin. The formal results apply to any evolutionary or innovation system whose parameters lie within the formally characterized admissible regions documented above.
