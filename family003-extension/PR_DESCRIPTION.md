# Strengthen Family 003 to Re(s) > 0.8749570194201

This extends the Family 003 zero-free half-plane from `7/8 = 0.875` to
`8749570194201/10000000000000 = 0.8749570194201`. It retunes exact rational
parameters and certificates through the existing analytic argument, preserving
the original function definitions and pole conventions.

For every complex `s` with `8749570194201/10000000000000 < s.re`, the public
theorems establish:

- `riemannZeta s ≠ 0`, with Mathlib's convention at `s = 1`;
- `DirichletCharacter.LFunction χ s ≠ 0` for every positive modulus and
  character `χ`, assuming `¬ (χ = 1 ∧ s = 1)`;
- `OAI.SevenEighths.HeckeFamily.LFunction χ s ≠ 0` for every original
  `HeckeFamily.Character`, assuming `¬ (χ.residue = 1 ∧ s = 1)`.

The Hecke family is the original finite-order family over the Eisenstein field
`CyclotomicField 3 ℚ`, including the cubic characters. There is no conclusion
on the boundary line and no added analytic-contract hypothesis.

The public module is
`OAI.BelowSevenEighthsTight.AssemblyExtension.PublicBoundary`. Its entrypoints
in namespace `BelowSevenEighthsTight.PublicResults` are
`riemannZeta_ne_zero_of_rational_lt_re`,
`dirichlet_LFunction_ne_zero_of_rational_lt_re`, and
`hecke_LFunction_ne_zero_of_rational_lt_re`.

## Repro

With the pinned toolchain, dependencies and official compatibility patches
provisioned, run from `lean/`:

```sh
lake build OAI.BelowSevenEighthsTight.AssemblyExtension.PublicBoundary ComparatorChallenges.FrontierTightPublicBoundary
```

See `REPRO.md` in the review package for the clean-checkout test and verification
scope. The patch contains 189 proof modules, including the public entrypoint, the independent
statement fixture/configuration, an update to `lean/docs/003.md`, and compact
verification evidence. Exact certificates are Lean source; research reports,
build caches and large export streams are excluded.

## Pins and verification

| Component | Pin |
| --- | --- |
| Source/base | `adc7f1241b42e322a6451854ab7e4b4c146bf78a` |
| Lean | `4.34.1`, commit `5045d0056413266e57c625dcd7c365b10e377c52` |
| Mathlib | `d13f23b723b8a846827a245b89c10fc7d3f11612` |
| Comparator | `d03acab154d269c06e60e4de7e4cc85deebff94b` |
| lean4export | `076e8e57707e813375e8f9da8bf989799ace9680` |

The verified branch passed statement comparison, axiom audit, fresh Lean
kernel replay and quotient postcheck for all five public declarations (the
three nonvanishing statements and two strict numerical comparisons).
The permitted axioms are only `propext`, `Classical.choice`, and `Quot.sound`.
`lean/docs/003-verification.json` records the compact evidence and source hashes.

The proof was compiled and replayed using the native Windows development-mode
route. The Linux Landrun/Landlock production sandbox has **not** been reproduced;
the replay uses Lean's kernel rather than a second independent kernel.

The frozen verified sources remain untouched. In the PR copy, 188 proof modules
are byte-identical; one trailing space was removed from `LowWindowBound.lean`
for repository whitespace checks. No proof terms or hypotheses were changed.
The comparator JSON uses LF line endings with unchanged parsed contents.

This is a local package for human review. No push, published PR or external
contact has been made.

The actual 193-file patch was applied to a separate fresh copy of the pinned
repository and built with the documented Lake command. That checkout also
passed coimport with the original results, fresh statement comparison,
axiom audit, full dependency kernel replay and quotient postcheck. The
test used independently copied original-project and pinned dependency
caches; all new proof and fixture objects were absent before its first build.
