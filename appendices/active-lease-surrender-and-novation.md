# Appendix: How could active retention leases be surrendered or novated?

**Status:** Exploratory and non-normative

**Relationship to the base RFC:** Nothing in this appendix is required for variable retention. It asks what may become possible only after Ethereum can represent finite serving obligations, end them safely, and derive conservative physical admission limits.

## E.1 Scope and central question

The base proposal lets a canonical blob publication receive a protocol-required serving duration. This appendix asks a later question:

> **When an active protocol obligation terminates early, under what conditions does that create capacity Ethereum can safely reuse?**

The question comes before market design. A payment between a lease payer and a replacement buyer cannot manufacture physical headroom. Early termination is useful only if the coding, custody, repair, indexing, and storage architecture can turn it into a conservative admission credit.

The appendix therefore does not assume that:

- active leases are transferable or surrenderable;
- the payer controls surrender;
- one surrendered blob releases one blob-equivalent of capacity;
- service termination triggers immediate deletion or compaction;
- reclaimability is visible to consensus;
- a replacement can bypass ordinary ingress;
- builders should procure DA service;
- or a secondary market belongs in the protocol.

The dependency is:

```text
logical expiry can release measurable physical resources
        |
        v
safe reclaim credit can be derived conservatively
        |
        v
early surrender or novation may be protocol-safe
        |
        v
secondary matching may have economic value
```

Failure at any earlier step blocks the steps below it without weakening the base variable-retention proposal.

## E.2 Surrender, transfer, and novation are different

“Resale” hides several different operations.

### Ownership or payment-right transfer

The committed object, expiry, service profile, and custody duty do not change. Only an economic claim or payment recipient changes. This may create little or no DA-level work.

### Early surrender

An authorized party asks Ethereum to end an existing serving obligation before its admitted expiry. No replacement is implied. Any safely reusable capacity returns according to the protocol's admission rules.

### Active novation

An old obligation ends early and a new committed object is admitted through a coordinated transition:

```text
old object A
    -> authorized early termination
    -> replacement object B clears fresh ingress and hot DAS
    -> safe cutover
    -> B continues under its own lease
```

The replacement still consumes ordinary publication bandwidth, coding, sampling, hot writes, and availability-establishment capacity. Retained-stock headroom is not ingress headroom.

### Future-capacity transfer

A right to use capacity later changes holders before exercise. That is a future-starting commitment and requires forward occupancy accounting. It also does not include future ingress unless the contract says so explicitly.

These operations should not share one state transition merely because they can all be described colloquially as lease transfers.

## E.3 Logical service termination versus physical reuse

An object can pass through several states:

```text
LIVE / OBLIGATED
        |
        | natural expiry or authorized early termination
        v
NON-LIVE / NOT OWED
        |
        | bookkeeping, repair cancellation, handoff,
        | compaction, reassignment, or lazy overwrite
        v
SAFELY RECLAIMED / CREDITABLE
```

The first transition ends a service claim. The second determines when physical capacity may support another admitted obligation.

Expiry may require consensus and storage-engine bookkeeping:

- active-stock counter updates;
- expiry-index changes;
- cancellation of future repair;
- scheduler and placement updates;
- reassignment or handoff state changes.

It need not trigger immediate erasure, compaction, or overwrite. Stale authenticated data can remain in place until reuse is economically useful. The distinction is:

```text
expiry bookkeeping work
    !=
physical reclamation work
```

This extends the base RFC's separation between `expiry_slot` and `reclaim_after_slot`. Early surrender needs at least the same conservatism as natural expiry.

## E.4 Time-dependent safe reclaim credit

Let:

- `L` be the current live obligation set;
- `X` be an authorized surrender set contained in `L`;
- `τ` be elapsed time since the surrender or cutover process began.

Define:

```text
κ_X(L, τ)
```

as the maximum additional protocol serving obligation that can be admitted safely at time `τ` **because of** surrender set `X`, after accounting for representation, overlap, repair, reclamation, and every binding component of `K_safe_vector`.

This is not a measurement of empty disk sectors. It is a conservative admission credit expressed in the same logical units used by the retained-stock rule.

The function has four important properties.

### Representation-dependent

`κ_X` depends on erasure coding, packing, custody assignment, repair policy, indexes, storage tiers, and which other objects remain live.

### Time-dependent

Immediately after initiation, the safe value may be zero:

```text
κ_X(L, 0) = 0
```

Later it may increase as duties end, handoffs complete, repair state changes, and physical headroom becomes safely reusable.

### Potentially non-additive

A coding cohort may become discardable only after several members leave:

```text
κ_{A,B}(L, τ)
    >
κ_A(L, τ) + κ_B(L, τ)
```

Individual leases can therefore have little reclaim value even when a compatible cohort has substantial value.

### Potentially non-consensus-observable

Reclaimability may depend on RocksDB or another storage engine, SSD garbage collection, local compaction, operator-specific repair debt, client layout, or hidden failure-domain concentration. Those facts do not automatically form a deterministic consensus input.

This is the primary kill question:

> **Can Ethereum derive a conservative, deterministic reclaim credit from protocol-visible facts rather than unverifiable local implementation state?**

If not, the protocol cannot safely mint admission headroom from early surrender.

### Credit must not be retractable after use

Raw physical headroom can fluctuate after a repair incident or operator failure. A protocol credit cannot. Once a replacement obligation has consumed `κ_X`, later events must not make that admission retrospectively unsafe.

A design must therefore either:

- issue credit only after an irreversible protocol-recognized transition;
- reserve enough margin to survive the modeled adverse events;
- or define a monotonically conservative credited function below measured reclaimability.

## E.5 Atomic transition and overlap reserve

A naive swap is unsafe:

```text
Alice releases A
    -> Bob inserts B
```

Bob's data must first clear the hot DA path while Alice's old obligation may still consume cold capacity. During that interval, both can be physically live and both must be accounted.

A safer sequence is:

```text
authorized surrender intent for A
        |
        v
conditional replacement right for B
        |
        v
B clears ingress and hot DAS
        |
        v
A and B temporarily overlap
        |
        v
handoff / coding / reclamation condition completes
        |
        v
A's protocol obligation terminates
        |
        v
κ_X(L, τ) becomes spendable
```

The overlap requires explicit headroom. Let:

```text
H_novation
```

denote the resource-vector reserve available for safe transition overlap. Admission must remain inside every relevant dimension:

```text
usage_vector
    + hot_obligation(B)
    + overlap_work(A, B)
    <= K_safe_vector
```

`H_novation` is not necessarily a separate consensus pool. It may be implemented as general safety slack, a capped transition lane, or a requirement that the transition wait for naturally free headroom. Whatever the mechanism, Alice's future reclaim credit cannot finance Bob's hot phase before the credit exists.

If B fails publication-time availability or the cutover condition, A's obligation must not silently disappear. The transition either aborts or follows a separately specified recovery rule.

## E.6 Representation-dependent additivity

### Independently reconstructable cold custody

Suppose each live object retains independently authenticated material sufficient for its own reconstruction. Removing `A` then need not weaken `B`, `C`, or `D`. After the relevant delay, reclaim credit may be approximately additive:

```text
κ_A(L, τ) ~= obligation_size(A)
```

This is the physical environment in which object-level early surrender is easiest to reason about.

### Persistent shared parity

Suppose a FullDAS representation retains parity derived across several logical rows. Removing `A` may release little headroom if the shared codeword remains necessary for surviving rows. Then:

```text
κ_A(L, τ) << obligation_size(A)
```

The object may be logically expired while its marginal physical burden remains close to zero.

### Cohort release

If shared structures can disappear only when several members leave, the useful surrender unit may be a coding cohort rather than one blob. Matching becomes combinatorial:

```text
small individual credits
    + compatible surrender set
    -> large cohort credit
```

This can create matching surplus, but it also makes the market less fungible, less predictable, and more dependent on representation details. Market liquidity is therefore endogenous to the coding and custody architecture.

The hot-2D/cold-1D branch in the main RFC matters here for the same reason it matters to ordinary expiry. If shared parity is only temporary availability-establishment scaffolding, the cold representation may permit predictable row-local reclamation. If shared parity persists, active novation may be cohort-based or impractical.

## E.7 Authorization and beneficiary protection

Prepayment does not imply unilateral surrender authority.

The party paying for a lease may be a sequencer or publisher, while other actors rely on continued service:

- challengers;
- bridge users;
- light clients;
- provers;
- future node operators;
- or application users who never controlled the payer key.

A real lease therefore needs a surrender policy distinct from payment authorization. Candidate policies include:

- non-surrenderable leases;
- leases transferable only above an immutable application minimum;
- application-contract approval;
- a dedicated surrender authority assigned at admission;
- multi-party or delayed authorization;
- and protocol-generated duties that cannot be surrendered at all.

At minimum, a surrender transition must satisfy:

```text
new_duration >= max(T_protocol-min, declared_application_min)
```

for every continuing or replacement obligation to which those floors apply. If beneficiaries cannot express or enforce their minimum, payer-directed early termination introduces delegated trust rather than preserving the original application guarantee.

Authorization must also survive key rotation, contract upgrades, reorgs, and changes in the party operating the application. Exact authority mechanics belong in an implementation proposal, but the base invariant is simple: no actor may sell service on which another protected actor is still entitled to rely.

## E.8 Possible market semantics

Early surrender does not imply one unique property-right model.

### Reclaim-and-return

Alice authorizes termination. Bob receives only the replacement term explicitly purchased and safely admitted. Any unused reclaimable capacity returns to the common protocol pool.

This is the simpler baseline because it does not create a new future-starting capacity asset.

### Residual-right model

Bob buys Alice's entire remaining contractual position. If Bob uses only part of the remaining interval, the unused tail becomes a future capacity right.

This is possible, but it imports the forward-occupancy machinery from the future-resource chapter. It must specify:

- future start and expiry;
- whether the right is divisible or transferable;
- future ingress acquisition;
- scheduled turnover or overlap;
- non-exercise and return-to-pool rules;
- and reorg or upgrade behavior.

The residual tail is therefore a design choice, not a consequence of novation.

### Off-protocol buyout

Alice and Bob may settle economically outside consensus while Ethereum exposes only an authorized surrender operation and ordinary admission. This avoids enshrining a matching market, although it does not remove the need for conservative reclaimability and beneficiary protection.

## E.9 Minimal non-normative protocol sketch

The following structure identifies the required state without choosing a market or proof system:

```text
LeaseMeta:
    object_id
    commitment
    expiry_slot
    reclaim_after_slot
    service_profile_id
    representation_domain
    surrender_policy
    surrender_authority
    declared_application_min

SurrenderIntent:
    lease_id
    earliest_cutover_slot
    authorization
    min_compensation          # optional market field
    nonce

ReplacementIntent:
    commitment
    requested_duration
    service_profile_id
    max_total_cost            # optional market field
    deadline
```

A hypothetical joint transition would require:

```text
1. surrender is authorized under LeaseMeta;
2. no protected application or protocol minimum is violated;
3. replacement clears ordinary ingress and hot DAS;
4. old and new obligations fit during transition overlap;
5. a protocol-recognized cutover condition succeeds;
6. reclaim_credit(surrender_set, elapsed_transition_time)
       is deterministic, conservative, and sufficient;
7. storage, serving, repair, I/O, and reclamation limits remain safe;
8. no lease or reclaim credit is duplicated across transfer or reorg;
9. failure before cutover leaves the old obligation intact or invokes
       an explicitly funded recovery rule.
```

The hard problem is item 6. A market interface does not solve it.

## E.10 Kill criteria

Protocol-level active surrender or novation should be rejected or kept off protocol if any of these conditions holds:

1. **Reclaim credit is not consensus-safe.** `κ_X(L, τ)` depends materially on hidden client or operator state and cannot be bounded conservatively from protocol-visible facts.
2. **Credit is not stable after issue.** A credit can be spent and later become unsafe under ordinary modeled repair, churn, or failure.
3. **Overlap cannot be bounded.** Hot admission plus old cold custody creates transition demand that cannot fit a conservative resource-vector reserve.
4. **Surviving data loses recoverability.** Removing `X` weakens still-live objects beyond their service profile unless shared representation is retained.
5. **Authorization cannot protect beneficiaries.** A payer or sequencer can terminate service below another protected actor's declared minimum.
6. **Turnover cannot be accounted.** Incremental reclamation, repair, and handoff work cannot be separated conservatively from ordinary ingress and background operations.
7. **A simpler design dominates.** Natural expiry, non-transferable leases, reclaim-and-return, or an off-protocol buyout captures nearly all value with materially less consensus complexity.

Failure of this appendix does not invalidate variable retention. It means that early termination should remain unavailable, application-specific, or off protocol.

## E.11 Relationship to futures, providers, and PBS

If conservative reclaim credits exist, a matching system could pair authorized surrenderers with replacement demand. A solver or builder may discover surplus from compatible cohorts, scarce overlap headroom, and timing constraints. That surplus is distinct from the protocol scarcity charge and from payment for physical DA service.

The separation should remain:

```text
protocol scarcity price
    != provider compensation
    != solver / builder matching surplus
```

Detailed future-capacity semantics belong in [the future-resource chapter](../docs/03-how-do-future-resource-markets-work.md). Provider qualification, custody accountability, posted procurement, concentration, and vertical-integration risks belong in [the hardware and operator-market chapter](../docs/11-how-do-hardware-and-da-operator-markets-scale.md) and its [illustrative economics appendix](illustrative-operator-economics.md).

Active novation adds two narrow concerns to those analyses:

- cohort-dependent reclaimability can create combinatorial matching value;
- paying for reclamation can reward manufactured churn unless private reward remains below the private cost of circular replacement.

Those concerns justify later simulation. They do not justify making PBS or a provider market part of the base surrender mechanism.

## E.12 Conclusion

Active leases may acquire secondary economic value, but usable reclaim credit is representation-dependent, delayed, potentially non-additive, and possibly unobservable to consensus. If those properties cannot be bounded conservatively, active novation should remain off protocol.

The appendix extends the main RFC's physical question by one step:

```text
logical expiry
    -> predictable physical savings?
    -> tradable reclaim credit?
```

The first arrow is required by variable retention's physical implementation. The second is optional. Ethereum should attempt it only if `κ_X(L, τ)` can be conservative, deterministic, stable after issue, and compatible with beneficiary rights and transition overlap.
