# Native Windows verification support

These two small helpers are included in the review package separately from
the repository patch. `OfflineReplay.lean` is the adapter used with the pinned
Comparator. It imports the upstream statement comparison and axiom-audit
implementations, then performs fresh Lean kernel replay and the quotient
postcheck. It provides no operating-system sandbox.

Required pins:

- Lean `4.34.1` (`5045d0056413266e57c625dcd7c365b10e377c52`)
- Comparator `d03acab154d269c06e60e4de7e4cc85deebff94b`
- lean4export `076e8e57707e813375e8f9da8bf989799ace9680`

To build the adapter, place `OfflineReplay.lean` in a checkout of the pinned
Comparator and add this executable target to its `lakefile.toml`:

```toml
[[lean_exe]]
name = "offline-replay"
root = "OfflineReplay"
```

Retain a manifest resolving lean4export to the exact pin above, then run
`lake build offline-replay` using the native Lean 4.34.1 toolchain on `PATH`.
The upstream Comparator's `lean-toolchain` requests 4.34.0; this development
route deliberately uses 4.34.1 to match the exported proof. Ensure `lake` and
`lean` resolve to that native distribution, rather than an Elan shim selecting
4.34.0. The supplied integration receipt records the
hashes of the already-built exporter and adapter actually used. The package
does not include their binaries or dependency caches.

After building the Family 003 targets, invoke the portable helper with the
locations of those tools (replace the example paths):

```sh
python verification/verify_windows.py --project checkout/lean --exporter tools/lean4export.exe --driver tools/offline-replay.exe --output verification-run
```

The output directory must not already exist. The helper obtains the search
path from the assignments printed by `lake env` in the selected checkout,
exports fixture and solution
separately, and writes `receipt.json`. It also retains the large raw proof
exports locally for replay. These streams are intentionally outside the PR.

The tested Windows Lake child launch omitted `LEAN_PATH`. Reading the reported
assignments and passing them through Python preserves Lake's own search paths.
The helper requires the project library to be present and rejects package
paths outside the selected checkout. The separate integration smoke file is
checked with `lake build ComparatorChallenges.Family003IntegrationSmoke` after
temporarily placing it under `lean/ComparatorChallenges/`.

Passing this route establishes the recorded comparison, axiom and Lean-kernel
checks. It does not establish Linux Landrun/Landlock isolation or an independent
kernel check. Building the adapter afresh on another machine is a separate
prerequisite; the integration run uses the previously pinned native binary.
