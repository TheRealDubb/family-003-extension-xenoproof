# Reproduce the Family 003 extension

Base the patch on `openai/math` commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The repository's `lean/lean-toolchain`
pins Lean `4.34.1`; its unchanged manifest pins Mathlib to
`d13f23b723b8a846827a245b89c10fc7d3f11612`.

## Apply and build

Place `family-003-rational-bound.patch` in the parent directory of a clean
checkout at that commit. Run these commands from the checkout:

```sh
git apply --check ../family-003-rational-bound.patch
git apply ../family-003-rational-bound.patch
cd lean
lake build OAI.BelowSevenEighthsTight.AssemblyExtension.PublicBoundary ComparatorChallenges.FrontierTightPublicBoundary
```

Prerequisites are Git and the pinned Lean/Lake toolchain on `PATH`, plus the
pinned dependency checkouts and their official Lean 4.34.1 compatibility
patches. For a new dependency installation, the repository documents
`lake update` in `lean/patches/README.md`. This package does not change the
toolchain, Lake configuration, dependency revisions or official patches.

The tested Windows checkout uses local Git settings `core.autocrlf=false`
and `core.longpaths=true`. These preserve LF source files and allow the
repository's nested paths under Windows.

The two explicit targets compile the public theorem and the independent
statement fixture with their dependencies. They do not build unrelated
repository families. The fixture deliberately contains `sorry` placeholders
for comparison; the solution proofs do not depend on `sorryAx`. Fixture and
solution are separate modules declaring the same public theorem names.

## Clean-checkout test scope

The readiness test uses a second fresh copy of the pinned Git tree, applies
the actual patch, and runs the exact `lake build` command above. Pinned
dependency caches and original Family 003 artifacts are copied independently
to avoid an unrelated dependency bootstrap. No new extension or new fixture
artifact is present before the build. This is a clean source/patch integration
test with a trusted baseline cache, not a cache-free bootstrap or a test of
dependency downloads. The final readiness report records the actual outcome.

Use `LEAN_NUM_THREADS=1` if limiting resource use on Windows. This changes
parallelism, not the build target or proof. The test invokes the pinned
`lake` executable through `PATH`, without custom module setup files or import
maps for the extension.

## Statement and proof verification

Configuration: `lean/ComparatorChallenges/FrontierTightPublicBoundary.json`.
It checks the three public nonvanishing theorems and the two exact strict
boundary comparisons. The axiom allowlist is exactly:

```text
propext
Classical.choice
Quot.sound
```

Comparator pin: `d03acab154d269c06e60e4de7e4cc85deebff94b`.
lean4export pin: `076e8e57707e813375e8f9da8bf989799ace9680`.
The path-free `lean/docs/003-verification.json` binds the verified source
lineage and records statement comparison, axiom audit, full dependency kernel
replay and quotient postcheck. Large export streams and caches are excluded
from the PR.

The existing and integration verification route is native Windows development
mode. It uses the upstream comparison and axiom-audit implementation with a
native adapter for fresh Lean kernel replay and the quotient postcheck.
Linux Landrun/Landlock production sandbox verification has not been reproduced.
The repository's production comparator instructions are a separate Linux
workflow; their success is not asserted by this package.

The full mathematical scope is the public Lean types, including the original
finite-order Hecke family and pole exclusions. Formal compilation of these
types is distinct from an independent audit of their correspondence with
the manuscripts.
