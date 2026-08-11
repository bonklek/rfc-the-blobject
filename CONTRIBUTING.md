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

When a claim depends on a changing Ethereum specification, add or update its commit pin in `REFERENCES.md`. Models should use only the Python standard library unless a dependency materially improves falsifiability, and should include tests under `models/test_models.py`.
