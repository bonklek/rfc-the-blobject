# Independent reader verification

Date: 2026-09-06. Read-only re-audit of the revised reader path; only this report was written. Source edits were continuing during review, so locations identify the observed snapshot and must be rechecked before disposition.

## Outcome

The revised README now meets the stated reader objective. A technically knowledgeable non-specialist can identify the proposal, follow a blob from purchase through expiry, distinguish logical byte-time from physical savings, understand the first PeerDAS experiment, recognize application recovery constraints, and find the optional branches without opening another overview. It explicitly distinguishes a research proposal from an implemented feature and explains what the models do and do not demonstrate. The core reading sequence follows the argument dependencies and its navigation matches the document map.

No unresolved P0 or P1 was established in this pass. All five P2 consistency findings below were corrected and independently rechecked on September 6. No remaining important P2 was established by this bounded recheck.

## Original P2 findings — all closed after recheck

1. **Continuous durations still receive a privileged design status.** `docs/01-how-are-capacity-and-pricing-managed.md:356` calls continuous variable retention the semantic target and maturity classes the conservative fallback. This conflicts with the README, conclusion, and revised §22.0, which make a small menu a candidate implementation whose success supports the proposal. Minimal correction: state the target as purchaser-selected duration; compare a small menu and arbitrary epoch choices before selecting granularity. Keep the conditional 2D compatibility branch independent of that choice.

2. **Transport neutrality still sounds like an implementation promise.** `docs/00-what-is-the-proposal.md:112` says PeerDAS, FullDAS, and a future fabric “should all be capable” of implementing the service. The physical chapter correctly treats compatibility as a falsifiable hypothesis. Minimal correction: call this a common semantic target against which each representation is tested, rather than assert that each can implement it.

3. **The tail-payment summary retains the local/aggregate ambiguity repaired in the detailed chapter.** `docs/11-how-do-hardware-and-da-operator-markets-scale.md:328` uses `q_history * f_tail * B * Δt` without identifying one node's duty or an aggregate service profile. `docs/10-how-does-lean-ethereum-change-the-proposal.md:217` now correctly uses node-specific quantities. Minimal correction: mirror that per-node scope and state that aggregate procurement depends on the specified custody population/profile. A local retained share cannot stand for aggregate system service.

4. **The novelty conclusion still expands the contribution bundle.** `docs/07-what-is-the-prior-art-and-novelty.md:91` and its following quotation combine the native service/accounting proposal with representation-aware custody and future markets. The README gives a narrower contribution and treats markets as optional. Minimal correction: put native selected duration and accounting in the contribution sentence; name representation studies and future markets separately as investigations/extensions. This finding does not assert or deny novelty.

5. **One pricing takeaway still attributes safety to an unspecified hard cap.** `docs/01-how-are-capacity-and-pricing-managed.md:188` says “The hard cap supplies safety.” The surrounding resource-vector derivation is correct, but the isolated takeaway invites the scalar-to-physical inference corrected elsewhere. Minimal correction: “Logical stock limits and the physical admission envelope constrain admitted obligations; fees allocate capacity within those bounds.”

## Confirmed corrections and fulfilled promises

- README lifecycle, publication-level lease identity, whole-blob accounting, prepaid expiry, and reclamation delay match the state sketch.
- The nominal 4,096-epoch comparison now flags the inclusive legacy boundary and exact compatibility gate; eight epochs is illustrative, not a certified minimum.
- The fixed-workload stock inequality stays separate from measured physical benefit and increased throughput.
- Rollup safety includes payer/beneficiary differences, acquisition and dispute timelines, and the limitations of challenge-period shortcuts.
- Publication-time availability, continuing protocol duty, recipient delivery, and durable integrity evidence remain distinct in the entry point and core explanation.
- The 1D packaging problem and optional 2D parity transition are separated; cell-level transport is evidence for a direction rather than existing expiry support.
- Revised tests distinguish base deployment gates, granularity choices, and optional branch failures. Workload claims are accompanied by an explicit evidence plan.
- The conclusion now ends on the decisive comparison instead of reopening every extension.
- The forward-market notation now uses start `s`, elapsed `T`, and lookahead integration limits `s-t` to `s+T-t`; the scalar projection is qualified.
- Operator chapter scope now explicitly makes fractional pools and separate payment optional.
- The reference register clearly separates August pins from the targeted September verification pass and does not claim exhaustive source or novelty certification.

## Coverage and uncertainty

Read README; the core chapters 00, 01, 05, 02, 11, 07, 08, and 09; the reference register; document map; argument/prose audit findings; and branch summaries/selected passages in 03, 04, 06, and 10. The initial combined tool read was truncated, so central mechanism and physical/safety sections were reread in smaller outputs. This was a reader/coherence verification, not an exhaustive second source audit, appendix line edit, formal verification, model execution, link checker, or rendered-figure QA. External claims were assessed against the repository's documented evidence scope, not independently recertified. No new user-demand, hardware, security, or novelty evidence was produced.

## Closure recheck

All five corrections were read in the revised source, not inferred from the coordinator report:

- **Finding 1 closed:** docs/01:356 now makes selectable duration the target and explicitly compares a small menu with arbitrary epoch choices; coding-domain alternatives remain representation-dependent.
- **Finding 2 closed:** docs/00:112 now identifies a common semantic target and explicitly denies that transport neutrality establishes safe or economic implementation.
- **Finding 3 closed:** docs/11:328 now scopes the formula to one qualifying node and distinguishes aggregate procurement/security from the local retained fraction.
- **Finding 4 closed:** docs/07:93 now states the native service and deterministic accounting contribution, with physical feasibility, pricing, and market extensions separately qualified.
- **Finding 5 closed:** docs/01:188 now separates the logical stock cap from the physical safe-admission envelope.

The new RowDAS paragraph at docs/05:62 fits the argument: it distinguishes row discovery/reconstruction from custody duties and treats individual historical retrieval as future work. It strengthens a research path without claiming retained service is implemented. This recheck assessed its argumentative scope only; the independent primary-source check belongs to the source-review pass.
