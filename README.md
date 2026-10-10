# Family 003 Extension — Xenoproof

This repository preserves a Lean-verified extension of OpenAI Math Family 003.

The original zero-free half-plane

Re(s) > 7/8 = 0.875

is strengthened to

Re(s) > 0.8749570194201

for the same Riemann zeta, Dirichlet L-function, and finite-order Hecke-family statements, with the original pole conventions.

The result was obtained by retuning and extending the existing analytic proof architecture, then formally reconstructing and verifying the full dependency chain in Lean.

## Verification status

- Full public theorem compiled in Lean 4.34.1
- Statement comparison passed
- Axiom audit passed
- Fresh Lean kernel replay passed
- Quotient postcheck passed
- Permitted axioms: `propext`, `Classical.choice`, `Quot.sound`
- Linux Landrun/Landlock production-sandbox reproduction remains pending

## Repository contents

- `family003-extension/` — formal proof sources
- `verification/` — verification reports and receipts
- `reviews/` — independent audit materials
- `research-history/` — evolution of the bound and failed/retained approaches
- `frontier/` — current Track 2 research beyond the verified bound

- ## What is a Xenoproof?

A **xenoproof** is a mathematically certified proof whose correctness can be verified, but whose full strategy or conceptual explanation is not yet adequately understood by human mathematicians.

The term is meant to distinguish this situation from ordinary computer-assisted mathematics. A proof may be computationally large yet still conceptually transparent. A xenoproof describes a different state: **verification has outrun understanding**.

A related term is:

**Xenotheorem** — a theorem for which the only currently known proof is a xenoproof.

These are not intended as permanent labels. A xenoproof can be studied, reconstructed, simplified, and eventually humanized. A xenotheorem may therefore cease to be a xenotheorem once its proof becomes conceptually understood.

The long-term purpose of this repository is not only to preserve finished proof artifacts, but to preserve the transition:

**candidate result → verification → theorem archaeology → structural reconstruction → human understanding**

That process matters historically. Failed approaches, repaired arguments, formalization discoveries, independent audits, and changes in understanding are part of the mathematical record rather than disposable scaffolding.

## Why this repository preserves the process

This project began as an attempt to understand and stress-test OpenAI Math Family 003. The eventual improvement to

`Re(s) > 0.8749570194201`

emerged through audit, parameter retuning, independent review, formal reconstruction, Lean verification, and repeated attempts to push beyond the resulting frontier.

Accordingly, this repository is intended to preserve both:

- the verified mathematical result;
- the research history showing how the result was discovered, challenged, formalized, and understood.

The goal is to preserve the transition from **mathematical correctness to mathematical understanding**.
