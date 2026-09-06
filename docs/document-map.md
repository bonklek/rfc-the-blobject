# Document and artifact map

The [README](../README.md) is the complete project overview. Chapters retain their original filenames and section anchors for citations; their numeric order records the older paper organization. Follow this dependency order for the core argument:

| Order | Chapter | Role |
|---|---|---|
| 1 | [00 — Proposal](00-what-is-the-proposal.md) | Service, scope, clock, bounds, logical comparison |
| 2 | [01 — Capacity and pricing](01-how-are-capacity-and-pricing-managed.md) | State sketch, physical admission, fee hypotheses |
| 3 | [05 — PeerDAS and FullDAS](05-can-this-work-with-peerdas-and-fulldas.md) | First prototype and conditional coding branch |
| 4 | [02 — Rollups](02-is-variable-retention-safe-for-rollups.md) | Application recovery and conditional elasticity |
| 5 | [11 — Hardware and operators](11-how-do-hardware-and-da-operator-markets-scale.md) | Physical constraints first; optional pools/payments afterward |
| 6 | [07 — Prior art](07-what-is-the-prior-art-and-novelty.md) | Contribution boundaries and related mechanisms |
| 7 | [08 — Open questions](08-what-remains-to-be-proven.md) | Evidence plan, proposal/branch tests, deployment gates |
| 8 | [09 — Conclusion](09-what-is-the-conclusion.md) | What follows and the decisive next experiment |

Optional chapters cover [03 — futures](03-how-do-future-resource-markets-work.md), [04 — persistence](04-what-happens-after-ethereum-retention-ends.md), [06 — applications](06-what-does-a-generalized-data-plane-enable.md), and [10 — Lean/history](10-how-does-lean-ethereum-change-the-proposal.md).

## Worked material

| Appendix | Purpose |
|---|---|
| [RetentionNotes](../appendices/retention-notes.md) | Downstream acknowledgement/cancellation authority |
| [Illustrative numerics](../appendices/illustrative-numerics.md) | Storage-only throughput/retention arithmetic |
| [Operator economics](../appendices/illustrative-operator-economics.md) | Invented payment schedule and controller comparison |
| [Backbone limits](../appendices/backbone-scale-limits.md) | Network, framing, object/proof-count constraints |
| [Ephemeral proofs](../appendices/ephemeral-data-and-proofs.md) | Durable proof claims and witness recovery |
| [Private AOT](../appendices/private-aot-authorization.md) | Canonical authorization versus local gossip checks |
| [Surrender and novation](../appendices/active-lease-surrender-and-novation.md) | Beneficiary authority, reclaim credit, replacement overlap |

## Provenance and generated artifacts

[REFERENCES](../REFERENCES.md) records source versions and verification; [models](../models/README.md) document executable support; [operator questions](../RESEARCH_TRACKING.md) are local research entries, not published GitHub issues. [Audits](../audits/2026-09-06-completion.md) record reviewed evidence, corrections, and remaining limits.

`tools/render-rfc-figures.py` generates explanatory figures 01, 02, 03, 05, and 06 in `docs/assets/figures/`. The numbering preserves the existing figure references; there is no current Figure 4. `models/spot_simulation.py` generates two CSVs and `models/render_charts.py` generates three corresponding SVGs in `models/output/`. This separation distinguishes explanation from simulation output. [Commands and checks](../CONTRIBUTING.md#generated-artifacts-and-checks).
