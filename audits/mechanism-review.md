# Mechanism and safety specialist review

Date: 2026-09-06. Read-only review of proposal sources; this report is the only output edited by this specialist. Locations refer to the pre-revision draft. Severity follows the local argument-audit skill: P0 validity, P1 structure/dependency, P2 support/precision, P3 expression. A branch-local P0 does not invalidate the base proposal.

## Thesis, steelman, and objection

The proposed base service attaches a bounded, prepaid serving duration to each canonical blob publication. With publications fixed and every duration bounded by the existing fixed horizon, required logical stock and byte-time cannot increase. A useful implementation additionally needs independently expirable authenticated custody, bounded reclamation and repair, and application recovery floors.

The steelman is a controlled experiment in current 1D PeerDAS: preserve publication-time DAS and the maximum serving choice, alter only post-publication duration, and measure the physical service vector against fixed retention and a small duration menu. The strongest objection remains that a correct logical inequality does not establish useful resource savings or sufficient application elasticity. Futures, paid operators, and private messaging cannot supply that missing evidence.

## Coverage

| Material | Coverage |
|---|---|
| Local skill, blobject rubric, initial audit, README | Read for scope and claim hierarchy |
| docs/00, 01, 02 | Detailed mechanism, lease identity, timing, bounds, EL/CL boundary, reorg and recovery review |
| docs/03, 04 | Detailed futures, settlement, privacy, post-inclusion service, external persistence review |
| docs/05 | Detailed 1D/2D, transition, custody, reconstruction and repair review |
| docs/06 | Application timing, service semantics and conclusion review; no application repository execution |
| docs/07 | Opening prior-art scope inspected; exhaustive novelty/source audit deferred to provenance specialist |
| docs/08, 09 | Deployment gates, kill scope, safety summary and conclusion review |
| docs/10 | Conditional lifecycle, protocol data and sparse-tail review |
| docs/11 | Detailed hardware, pool, handoff, reward, qualification and controller safety passages; no economic numerical reproduction |
| appendices/retention-notes.md | Detailed authorization and claimed receipt semantics |
| appendices/private-aot-authorization.md | Detailed canonical activation, gossip allowance and reorg semantics |
| appendices/active-lease-surrender-and-novation.md | Detailed reclaim, overlap, beneficiary, atomicity and fallback review |
| appendices/ephemeral-data-and-proofs.md | Detailed proof binding, acquisition/proving timing and availability distinction |
| appendices/backbone-scale-limits.md | Conservation, assignment and high-throughput safety argument review |
| appendices/illustrative-numerics.md; illustrative-operator-economics.md | Opening assumptions and claimed scope inspected; numerical/model review delegated elsewhere |
| Models, validator, figures | Not independently executed/rendered; initial audit evidence considered, model specialist owns verification |

## Dependency and invariant map

| Layer | Necessary invariant | Status and decisive check |
|---|---|---|
| Publication identity | Identical commitments in distinct publications produce distinct obligations; deterministic ID without circular block-root dependence | Correctly stated design requirement; container and derivation remain open EIP work |
| Timing | Expiry is inclusion slot plus duration; service holds before exclusive expiry; protocol and application floors include required hot/recovery work | Defined but notation drifts (M04); no safe minimum established |
| Logical admission | Account all live leases and unreclaimed obligations; exclude future starts from the monotonic spot proof | Sound for fixed capacity and stated accounting; physical vector cannot be inferred from scalar stock (M03) |
| Fork state | Restore counters and metadata atomically, without duplicating charges or reclaim credits | Logical requirement stated; snapshots cannot restore deleted payloads or remove physical fork-cache costs |
| Pruning/reclaim | Ending service cannot credit capacity before representation and reclamation permit safe reuse | Explicit research gate; fixed grace is illustrative, not measured proof of backlog safety |
| Service profile | Publication DAS remains unchanged; eligible arbitrary requesters retain a bounded reconstruction path; no upgrade weakens an admitted live profile | Correctly separated from delivery/custody; adversarial load, discovery and request-budget evidence missing by design |
| Custody/repair | Enough authenticated independent pieces survive throughout service and handoffs; repair completes before reconstruction fails | Base 1D deployment gate, with an additional parity handoff gate in 2D; checkpoint null model insufficient (M05) |
| Application recovery | Chosen duration covers the actual recovery path or a completed trustworthy handoff; payer cannot silently weaken beneficiaries' rights | Main text correctly admits trust changes; receipt example violates stronger opening claim (M01) |
| Future starts | Reserve every future occupied interval plus reclamation, transition and flow constraints; transfer cannot duplicate a right | Conceptual forward curve present; coordinate error M04 and capacity-shrink question M06 remain |
| Private activation | Canonical credit spent once; key, domain, slot, capacity bound; public authorization separate from peer-local replay/traffic accounting | Good two-stage idea; canonical/local accounting conflated (M02) |
| Surrender/novation | Authorized old-service cutover; replacement clears fresh DA; overlap funded before credit; no protected old-data floor violated | Mostly explicit; old-object floor and fallback scope need clarification (M07) |
| Operator markets | Accountable service and data survive exits; future reduced admission cannot cancel old accepted service | Handoff text strong; supply-shrink response needs explicit outstanding-obligation guard (M06) |

The canonical argument order should be publication/identity and clock → logical accounting → representation and physical admission → recovery/security floors → experiments. Optional privacy, futures, surrender and procurement should hang from this chain rather than become prerequisites.

## Findings

### M01 — P0, branch-local: acknowledgement secret does not prove recipient retrieval

- **Location:** appendices/retention-notes.md:7, 39–57; docs/04-what-happens-after-ethereum-retention-ends.md:14.3.
- **Evidence:** A.1 says termination occurs when the intended recipient proves retrieval. A.2 has the sender choose `r`, encrypt it for the recipient, and let anyone revealing `r` terminate. The sender already knows `r` and can reveal it before any recipient fetch. The provider or a colluding sender can therefore obtain the termination event without delivery. Even a recipient signature would establish an acknowledgement, not a proof that every byte was read, absent a stronger protocol.
- **Consequence:** The worked construction cannot support recipient-controlled termination or receipt-certified delivery as introduced. The later sentence acknowledging only secret possession is correct, but does not repair the incompatible earlier promise.
- **Correction:** Label this simple construction a bearer-secret cancellation capability and state that sender knowledge permits early cancellation. If recipient authorization is intended, describe an optional recipient-controlled signing key or proof of recipient-secret knowledge, bound to note/object/domain, and explicitly separate authorization from delivery evidence. Do not silently substitute a new cryptographic construction as solved.
- **Confidence/support:** High; direct counterexample from the supplied construction, no external cryptographic assumption needed.

### M02 — P1, branch-local: canonical activation is mixed with peer-local gossip consumption

- **Location:** appendices/private-aot-authorization.md:129–153, 252, 267; docs/03-how-do-future-resource-markets-work.md physical-settlement privacy paragraph.
- **Evidence:** The proposed canonical map contains `remaining_bytes`; peers then decrement allowance for accepted gossip and allegedly roll it back in the same canonical state transition. Two peers can receive different valid objects in different orders without any chain-state difference. Canonical ownership is shared, but these accepted-message histories are not. D.1 already correctly states that gossip does not consume an on-chain ticket bit.
- **Consequence:** The fast path gives an unwarranted impression of globally consistent spent bandwidth and solved reorg handling. A malicious authorized key can equivocate; activation alone neither serializes concurrent gossip nor makes first-seen histories canonical.
- **Correction:** Canonical state should bind an activation ID, chain/domain, target, maximum allowance, key and permitted object-index range. Describe separate bounded peer-local first-valid caches keyed by activation/object/column (or equivalent exact resource unit), authenticated object binding and quotas. Reorg refresh invalidates/reconciles authorization and local caches; it does not roll back actual bandwidth. State unresolved equivocation/concurrent-object semantics and limit “once” to one canonical activation transaction rather than one verifier globally. Replace “unique across forks” with unique on each canonical history, with orphan/reactivation rules.
- **Confidence/support:** High; protocol-state distinction plus primary source verification. Current draft [EIP-8256 P2P Gossip](https://eips.ethereum.org/EIPS/eip-8256#p2p-gossip) accepts only the first valid sidecar for a ticket/column pair; its [reorg handling](https://eips.ethereum.org/EIPS/eip-8256#reorg-handling) refreshes ticket caches. Inspected 2026-09-06; the external draft is evidence for the boundary, not specification of this extension.

### M03 — P1, base argument: scalar-stock proof again becomes physical safety

- **Location:** docs/02-is-variable-retention-safe-for-rollups.md:78; docs/01-how-are-capacity-and-pricing-managed.md:202–208.
- **Evidence:** The rollup summary says hard active-stock bounds protect physical safety. Section 5.1 says the active-stock cap solves enforcement of a physical safety bound. Section 6 correctly requires storage, serving, repair and I/O constraints together.
- **Consequence:** A stream of short leases can satisfy resident-stock capacity while violating writes or service capacity. The local summary removes a premise necessary to its conclusion.
- **Correction:** Say the cap bounds contracted logical stock; resource-vector admission and conservative reclaim protect physical feasibility. Preserve the fixed-ingress logical theorem and the reserve's limited role in separating duration lanes.
- **Confidence/support:** High; internal contradiction of scope, already found in initial audit with a second recurrence identified here.

### M04 — P2, base and futures: time coordinates and expiry endpoints disagree

- **Location:** docs/00-what-is-the-proposal.md:71, 84; docs/01-how-are-capacity-and-pricing-managed.md:34; docs/03-how-do-future-resource-markets-work.md:37–75.
- **Evidence:** `T` is both expiry and duration in chapter 00; spot interval includes `τ=T` although service is `current_slot < expiry_slot`. In chapter 03 `T` is absolute publication time while `S_t(τ)` is stock at `t+τ`; the fee integral runs from `T` to `T+R` using `S_t(τ)`, which prices the interval shifted by current time `t`.
- **Consequence:** Ambiguous endpoints and an actual forward-price coordinate error. For now `t=100`, publication `T=120`, duration 10, the intended horizons are 20–30, not 120–130.
- **Correction:** Use duration `T`, absolute inclusion/start `s`, expiry `e=s+T`, remaining duration `max(0,e-now)`; define occupancy on half-open intervals. Integrate forward horizon from `s-t` to `s+T-t`, or integrate absolute time `u` using `S_t(u-t)` and `C_t(u-t)`.
- **Confidence/support:** High; dimensional and coordinate derivation. No need for new protocol parameters.

### M05 — P2, custody evidence: “conservative” has not been shown for the checkpoint model

- **Location:** docs/05-can-this-work-with-peerdas-and-fulldas.md:17.4, paragraph introducing `P_lease ≈ P_row^N` and model link.
- **Evidence:** The formula assumes independent cell losses plus successful restoration between intervals. Independent custodian failures do not give independent cells if custody sets overlap: two cells with threshold one and one common custodian failing with probability 0.1 survive with probability 0.9, while independent-cell arithmetic produces 0.99. The draft acknowledges correlation and model limitations but still calls the product a conservative checkpoint approximation.
- **Consequence:** A reader can interpret a passing `p_max` result as a lower-bound safety claim. Checkpoint reconstruction alone also does not establish continuous service between checkpoints.
- **Correction:** Remove “conservative” absent a bound; label independent-cell and repair assumptions alongside formula and outputs. State whether loss is monotone within each interval and whether the probability models loss of possession, temporary unavailability or refusal to serve. Add the shared-custodian counterexample as an applicability test, not a claim that the abstract binomial formula is wrong.
- **Confidence/support:** High; algebraic counterexample already reproduced in initial audit. Formal survivability remains an acknowledged deployment gate, not a new finding that the whole proposal fails.

### M06 — P2, procurement/futures branch: reduced admission does not resolve outstanding service after supply loss

- **Location:** docs/11-how-do-hardware-and-da-operator-markets-scale.md:267–274, 366; docs/03-how-do-future-resource-markets-work.md:10.1–10.2.
- **Evidence:** The shortage example lowers safe admission when qualified cold supply falls to 800 TB. If previously admitted obligations already require more than that, rejecting new arrivals does not make those obligations fit. Future rights have the same issue if the forecast envelope falls after sale.
- **Consequence:** “The safe response” reads as a complete recovery rule when it is only a rule for new commitments. It can be mistaken for permission to shrink already prepaid service or redefine `K_safe` around the shortage.
- **Correction:** Explicitly distinguish prospective admission/target reductions from preservation of outstanding leases. List funded replacement/repair reserve, enforceable exit notice, committed supply through accepted terms, and emergency shortfall handling as branch deployment requirements. An unhandled shortage is a service failure under the model, not retroactive cancellation or a safe redefinition of obligations.
- **Confidence/support:** High for the accounting distinction; medium on materiality because the chapter already provides strong handoff and delayed-exit language. A clarifying paragraph is sufficient; no invented bailout or procurement policy needed.

### M07 — P2, surrender branch: clarify old-object floors and what “off protocol” can salvage

- **Location:** appendices/active-lease-surrender-and-novation.md:293–296, 380–390, 415.
- **Evidence:** The minimum inequality is stated for continuing or replacement obligations; a replacement's duration cannot protect beneficiaries who still require the old object's bytes. Elsewhere failures of deterministic reclaim or authorization are said to leave novation “off protocol.” An off-protocol payment cannot authorize early pruning or unsafe native capacity credit, as the appendix itself correctly explains at E.8.
- **Consequence:** These shortcuts weaken an otherwise careful beneficiary/reclaim model.
- **Correction:** For each terminated old lease, test cutover against its immutable earliest authorized end or protected absolute expiry, and require its surrender authority separately; check the new lease's floors independently. Clarify that when native surrender/reclaim is unsafe, only economic rights/payment matching or downstream obligations can move off protocol; the original native lease continues to natural expiry. Do not imply off-protocol matching repairs a broken native transition.
- **Confidence/support:** High for distinction, medium severity; substantially mitigated by existing E.7/E.9 text.

### M08 — P2, proving application: the timing inequality is sufficient for one operating policy, not necessary for the general pattern

- **Location:** appendices/ephemeral-data-and-proofs.md:123–132; docs/06-what-does-a-generalized-data-plane-enable.md selected-duration paragraph.
- **Evidence:** `T_service > T_fetch + T_prove + T_settle + H` is called a minimum operational condition. A prover can acquire a durable local witness before Ethereum expiry and finish later, while keeping that witness through proof settlement. Ethereum's serving duty has ended but the proof pattern still works.
- **Consequence:** The text overstates the native duration needed and blurs the acknowledged distinction between native retention and voluntarily preserved copies. This can understate genuine retention elasticity.
- **Correction:** Label the inequality a sufficient budget when the workflow requires completion within Ethereum's serving window. For workflows that retain a local or external witness, require acquisition before native expiry and preserve a stated recovery path until successful proof/settlement; explain the changed trust/redundancy assumption.
- **Confidence/support:** High; direct scheduling counterexample, no novel cryptographic result required.

## Acknowledged research limitations, not additional defects

- The canonical ID construction, metadata container, fork-state integration and service-profile versioning are explicitly unspecified. These are implementation work, not contradictions. Correct the stale ring-buffer/`retained_bytes` description in chapter 01 while preserving that status.
- A reorg can restore logical counters, not deleted cells. Fork-recovery minimums, orphan-data reserve and finality stalls are already explicitly asked in chapter 00 and 08. Keep these as base deployment gates and add the compact reminder near the reorg sketch; do not report them as wholly omitted.
- Sparse historical serving under current 1D is not established merely by cell messaging. The draft correctly distinguishes that hypothesis from EIP-8136. A negative parity-lifetime result in future 2D does not invalidate 1D.
- The minimum duration is not established, including the illustrative eight-epoch use case. The draft repeatedly states this; reviewers should not claim it recommends that parameter.
- Full reconstruction/security under correlated custody failure remains unproven. The base level-1 experiment does not require inventing a level-3 proof or paid operator market first.
- External archive acceptance needs actual acquisition, authenticated completeness and an application-appropriate continuing retrieval path. Main text generally makes the changed trust boundary explicit; a purchase or promise alone is not a completed handoff.
- Logical dominance assumes the same admitted workload and maximum horizon. It is not proof of larger ingress, market stability, demand or client readiness. The hierarchy of whole-proposal versus duration-granularity kill tests needs correction as already identified in the initial audit.

## Revision sequence and residual uncertainty

1. Correct M01 and M02 without promoting either optional branch to a solved protocol.
2. Repair M03 and M04 throughout summaries and equations; fix state-vocabulary drift near the reorg sketch.
3. Qualify M05 and M08 at formulas and outputs, then add the narrow clarifications M06–M07.
4. Put base deployment gates next to the minimal mechanism and distinguish 1D failure, 2D branch failure, optional-market failure and preference for a small maturity menu.
5. Independently re-read the resulting core and altered appendices. No prototype or source edit was performed by this specialist.

This review does not establish safe service parameters, physical reclaim bounds, an adversarial custody proof, privacy security, source accuracy across every cited system, or production readiness. It establishes that the base accounting thesis survives this mechanism review, with two concrete optional-construction defects and several recoverable scope/precision errors.
