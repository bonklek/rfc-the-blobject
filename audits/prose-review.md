# Prose and terminology review

Date: 2026-09-06. Read-only source pass during coordinator revisions; only this report was written. Read the local argument skill and Blobject rubric, the initial audit, and the argument review. This is a bounded supplementary review, not a second full argument audit. README and conclusion rewrites belong to the coordinator.

## Argument and coverage

The defensible thesis remains bounded selectable required-serving duration, a derived logical byte-time reduction at fixed workload, and an open representation-specific test of net physical benefit. Future reservations, sparse-history lifecycles, and downstream cancellation are separate extensions. The strongest objection remains that removing a logical duty need not produce useful physical savings after service and implementation costs.

Reviewed docs/03 and docs/10 closely, the current opening service definition, RetentionNotes, selected numerical/operator/backbone appendix passages, and targeted terminology occurrences across all chapters and seven appendices. Used argument-review.md for the whole-corpus structural map. No external source verification, model execution, or exhaustive line edit was performed. Source edits were in progress: anchors identify the observed snapshot and should be rechecked before applying. Already corrected receipt-secret and acquired-witness qualifications are acknowledged as resolved; no new defect is asserted for those passages.

## Prioritized concrete fixes

### PROSE-01 — P2: Future-time notation changes meaning and shifts the fee interval

**Anchors:** docs/03-how-do-future-resource-markets-work.md:9, :18, :24, :39, :73–77, :95. **Confidence:** high.

The base uses `T` for elapsed duration, but this chapter uses it for an absolute publication time and `R` for duration. More consequentially, `S_t(τ)` is defined at absolute time `t+τ`, while the integral runs from absolute `T` to `T+R`. For nonzero current time, that evaluates the wrong forward interval.

Use future inclusion/start `s`, elapsed duration `T`, expiry `e=s+T`, and lookahead `τ`. Write the obligation as `[s,e)` and the fee integral over `τ` from `s-t` to `e-t`; define `s≥t`. A signature such as `DAService(C,B,s,T)` should explicitly identify the future-start extension. Keep the scalar forward envelope labelled as a logical-stock projection of the physical admission constraints, rather than an independently sufficient physical bound. This is a notation/derivation correction, not a claim that the illustrative fee is a finished market.

### PROSE-02 — P2: Sparse-tail fraction switches between local and system quantities

**Anchors:** docs/10-how-does-lean-ethereum-change-the-proposal.md:94, :187, :200, :217. **Confidence:** high for ambiguity; medium for intended interpretation.

`f_tail` is an unspecified retained fraction. The source discussion concerns a random share per client, `G_history ~= f_tail * R` is then described as per-node growth, and the fee formula applies `f_tail * B` without saying whether it prices one node or total service. Multiple nodes retaining a small fraction each does not mean the system retains that fraction in aggregate.

Define a local share, for example `f_tail,node`, and call the growth `G_history,node`. State that aggregate service depends on population, replication/overlap, coding, repair, and serving. Either scope the operator formula to one qualifying node's duty or leave aggregate `F_tail` as a function of a specified custody profile. The lifecycle API can carry a named tail service profile instead of silently treating a local sample share as a complete security specification.

### PROSE-03 — P2: Downstream shorthand still treats duration as a date

**Anchors:** docs/00-what-is-the-proposal.md:123, :125, :156; appendices/ephemeral-data-and-proofs.md:52, :204. **Confidence:** high.

The opening definition now correctly separates `s`, `T`, and `e`, but later text still says “through `T`.” Use “until expiry `e`” or “for duration `T` from inclusion.” Align interval service evidence with `[s,e)`; avoid a closed right endpoint where the accounting excludes expiry. In private-aot-authorization.md:48, target slot `T` is locally defined and mathematically valid, but `s_target` would reduce cross-document overload. That local rename is lower priority than the forward integral.

### PROSE-04 — P2: General lifecycle wording can imply deletion or a stronger guarantee

**Anchors:** docs/10-how-does-lean-ethereum-change-the-proposal.md:81, :93, :160. **Confidence:** high.

Replace diagram label “expire entirely” with “native serving obligation ends.” Define “full-strength window” as the ordinary required-serving service under the selected custody assumptions, rather than leave it sounding like certified continuous availability. Define `B` as protocol-accounted quantity, including fixed whole-blob accounting in the current-compatible case; “logical size” alone can be read as useful payload length. These are small local repairs that preserve the already sound distinction between sparse history and full retrievability.

### PROSE-05 — P3: The compatibility note mixes current explanation with revision instructions

**Anchors:** docs/10-how-does-lean-ethereum-change-the-proposal.md:7, :19, :205, :222, :242. **Confidence:** high.

Use conditional opening language: “If these research directions advance, more data classes could receive distinct lifecycle policies.” The later status paragraph already qualifies the proposals, but the first sentences are categorical. Replace “The base proposal needs five bounded revisions” with a present-tense compatibility boundary list; these are now properties and extension limits, not instructions to a future editor. Combine the two nearby payer paragraphs in §6: retain the funding alternatives and explicit cross-subsidy warning once. Keep §2's short payer introduction because it explains why Block-in-Blobs matters before pricing.

### PROSE-06 — P3: Surrender example names the wrong marginal quantity

**Anchor:** appendices/active-lease-surrender-and-novation.md:252. **Confidence:** high.

After showing near-zero reclaim credit under persistent shared parity, the paragraph says the object's “marginal physical burden remains close to zero.” A reader may understand this as zero physical cost despite retained shared material. Say “Ending the logical obligation may release almost no physical capacity while the shared codeword remains necessary.” This directly states the inference represented by `κ_A` without requiring a counterfactual definition of marginal burden.

### PROSE-07 — P3: A numerical summary loses its binding-resource scope

**Anchor:** appendices/illustrative-numerics.md, concluding blockquote beginning “The same retained-stock envelope supports radically different ingress rates.” **Confidence:** high.

Use “Under this storage-only steady-state model, the same logical-stock envelope permits different stock-limited ingress rates as mean required duration changes.” The appendix's introductory qualifications are useful; carry the binding-resource scope into its isolated takeaway. The issue is summary precision, not invalid arithmetic.

## Terminology sheet

| Concept | Preferred term / symbol | Boundary to retain |
|---|---|---|
| Canonical lease start | inclusion time `s` | Hot phase begins within total duration; future propagation is not necessarily canonical inclusion |
| Selected service length | elapsed duration `T` | Not an absolute timestamp |
| Lease end | expiry `e=s+T` | Obligation interval `[s,e)`; does not order deletion |
| Future offset | lookahead `τ` at current time `t` | Absolute evaluation time is `t+τ` |
| Throughput | logical ingress rate `R` | Do not reuse for duration in forward markets |
| Quantity | protocol-accounted quantity `B` | Current-compatible case is fixed whole-blob accounting, not useful payload |
| Retained stock | contracted logical stock `S_t` | Not measured physical disk occupancy |
| Reclaim | conservative admission credit `κ` | Not necessarily instantaneous freed bytes or additive across objects |
| Fresh DA | publication-time availability | Does not prove later interval service or inclusion fairness |
| Retention | required serving under custody assumptions | Not recipient delivery, guaranteed deletion, or a recurring consensus certificate |
| Maturity | duration class, or expiry date when explicitly defined | Prefer precise term when a sentence mixes starts and ends |
| Sparse tail | reduced custody service/profile | Specify local versus aggregate fraction and reconstruction assumptions |
| Operator fee | payment for qualified service | Distinct from protocol scarcity price and burned transaction fees |
| Downstream acknowledgement | stated termination authorization | Bearer-secret revelation does not prove recipient retrieval |

## Revision sequence and residual uncertainty

Correct the forward-time equation first, then settle the local/aggregate tail interpretation before editing its formulas. Apply the vocabulary and diagram fixes next; compress repeated payer and editorial-history prose last. The broader argument review already owns the base-versus-continuous-duration hierarchy, overstated benefit language, compatibility claims, and README/conclusion structure, so those are not duplicated here as new findings.

The tail formula needs an explicit interpretation from the design owner; prose alone cannot select a custody population or security profile. No new P0 or whole-proposal P1 defect is established by this supplementary pass. Completion of these edits would improve precision without establishing feasibility, demand, novelty, or physical performance.
