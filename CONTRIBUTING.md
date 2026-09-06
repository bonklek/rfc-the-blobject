# Contributing to RFC: The Blobject

This repository is a request for comment. Contributions should sharpen, test, or falsify the proposal.

## Useful contributions

- identify a broken assumption or counterexample;
- add closer prior art with a precise comparison;
- quantify a capacity, pricing, custody, repair, or liveness claim;
- document an L2 security requirement that constrains retention;
- prototype the hot-dense to cold-sparse lifecycle against a concrete DAS design;
- turn an open question into a reproducible simulation or experiment.

## Opening an issue

State the affected document and section, the claim being challenged, the evidence or reasoning, and the smallest proposed next step. Distinguish established behavior from draft mechanisms and original hypotheses.

## Proposing text

Keep the existing section numbering stable where possible. Prefer narrow pull requests with links to primary sources. Mark speculative claims clearly, and do not describe a draft EIP or research proposal as deployed behavior.

When a claim depends on a changing Ethereum specification, add or update its commit pin in `REFERENCES.md`. Record a dated current-source check separately from the pinned research baseline. Models should use only the Python standard library unless a dependency materially improves falsifiability, and should include meaningful tests under `models/test_*.py`.

Express Ethereum protocol and retention durations in epochs first, with wall-clock time as a parenthetical approximation based on the current 32-slot, 12-second-slot timing. Prefer power-of-two example maturities such as `256, 512, 1,024, 2,048, 4,096`. Preserve native wall-clock units for external protocols, but include their Ethereum-epoch equivalent when making a comparison.

## Argument and terminology

Classify consequential claims as established facts, derivations, proposed mechanisms, conditional branches, illustrative results, or open hypotheses. Keep the conditions close to the claim. Logical retained stock is not measured physical occupancy; publication-time availability is not recipient delivery or a proof of continuous service. Fees, hard admission bounds, and payments to providers serve different purposes.

Use `s` for inclusion/start, `T` for elapsed duration, `e=s+T` for expiry, and `τ` for lookahead from current time `t`. Use consistent units and half-open service intervals. The exact legacy serving boundary remains a deployment question, not a property proven by the elapsed-duration toy.

Read proposed changes in dependency order: definition, accounting, representation, application recovery, constraints, evidence, conclusion. Preserve source paths and section anchors; append new structure or navigation rather than silently breaking citations. A shorter paragraph is not an improvement if it hides a required premise.

## Generated artifacts and checks

Python 3.10 or later runs the dependency-free models and checkers. The PowerShell wrapper also requires PowerShell and ripgrep (`rg`) on PATH. Edit model/renderer sources rather than hand-editing CSV or SVG output.

| Outputs | Source command |
|---|---|
| Five explanatory SVGs in `docs/assets/figures/` | `python tools/render-rfc-figures.py` |
| Two scenario CSVs in `models/output/` | `python models/spot_simulation.py --output-dir models/output` |
| Three scenario SVGs in `models/output/` | `python models/render_charts.py` |

After regenerating affected output, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/validate-rfc.ps1
```

This checks base numbering, all chapter slots, local paths and heading targets, fences, two narrow phrase guards, model/tool tests, generated-file consistency, and diff whitespace. The artifact check regenerates in a temporary directory and compares text with normalized line endings. `--output-dir` on the figure renderer supports isolated output as well.

Mechanically valid text can still be false or misleading. Verify changed claims against primary sources, review their implications in context, and inspect rendered figures for cropping, readable labels, correct units, and visible assumptions. The Markdown checker supports the inline-link/ATX-heading conventions used here; it is not a complete Markdown or external-link validator.
