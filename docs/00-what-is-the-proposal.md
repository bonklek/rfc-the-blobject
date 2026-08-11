# What is the proposal?

## Executive framing

Ethereum has spent years increasing **how much data can be made available at once**. [EIP-4844](https://eips.ethereum.org/EIPS/eip-4844) separated blob data from execution gas. [PeerDAS (EIP-7594)](https://eips.ethereum.org/EIPS/eip-7594) distributes blob custody and sampling. The draft [Blob Streaming proposal (EIP-8256)](https://eips.ethereum.org/EIPS/eip-8256) explores reservable ahead-of-time propagation, while [FullDAS](https://ethresear.ch/t/fulldas-towards-massive-scalability-with-32mb-blocks-and-beyond/19529) points toward much larger distributed DA capacity. One parameter has stayed comparatively rigid: **how long every admitted byte must remain protocol-served**.

This RFC proposes making that serving obligation selectable. Today, ingress and retention are bundled. Two objects that create the same propagation burden receive the same serving horizon even when one application needs only a short replication window and the other needs the full current horizon. Under the proposal, a purchaser chooses a duration `T`, bounded by `T_max`. Setting `T_max` no higher than the current minimum serving horizon preserves today's service as `T=T_max` and can only reduce the logical retained-data obligation for a fixed admitted workload. `T_max` limits what a purchaser may require from the protocol; it neither orders nodes to delete data nor prevents them from serving it longer.

If Ethereum uses the resulting storage savings to admit more data, retained stock becomes scarce in its own right. A lease that starts on admission occupies storage immediately, so a ceiling on active retained stock is enough to bound contracted storage. The harder problems are physical: deriving that ceiling from the custody architecture, reserving headroom for short-duration traffic, charging for required byte-time, and making logical expiry release real resources under DAS coding.

That last problem depends on the representation. With current 1D PeerDAS, cell-level transport may allow sparse historical custody without preserving complete column sidecars. A future cross-row 2D code may instead need two phases: keep the richer code through the hot availability phase, then move still-live objects to sparse row-local custody. If the second-dimensional codeword must survive for the entire serving horizon, the fallback is to place similar maturities in separate coding domains. A forward retained-capacity curve is needed only if Ethereum also sells DA or retention commitments that begin in the future.

The same decomposition has wider uses, but they are not prerequisites for the base mechanism. Applications whose security models permit it gain another way to respond to congestion. Blob Streaming-style ingress rights could be paired with timed retrievability. Objects could pass from a short Ethereum serving window to storage providers, caches, archives, or P2P swarms that provide persistence, routing, privacy, or application-specific behavior.

The central question is:

> **Why should every byte entering Ethereum DA purchase the same amount of future serving?**

The following sections define the mechanism, test its implementation and security assumptions, and then examine the larger data-plane consequences.

---

## 1. Ingress and retention are distinct economic resources

Data availability consumes at least two physically and economically distinct resources.

First, data must enter the network. It must be propagated, encoded, distributed, sampled, verified, and made reconstructably available. This is fundamentally a **flow resource**: bandwidth and real-time processing capacity.

Second, once availability has been established, the network must continue to custody, serve, repair, or re-replicate enough of the data for reconstruction. This is fundamentally a **stock resource**: storage capacity committed through time.

These costs should not necessarily be bundled.

A 100 MB object that needs one epoch of required serving—about 6.4 minutes at current timing—imposes approximately the same initial ingress burden as a 100 MB object that receives the current full 4,096-epoch serving window—about 18.2 days. Their subsequent custody obligations differ by exactly a factor of 4,096.

Conversely, shortening retention cannot eliminate the initial bandwidth requirement. A one-epoch object must still be propagated and made available.

A first-order price decomposition is:

```text
DA price
=
ingress price
+
retention price.
```

Ingress prices the act of making the bytes available. Retention prices Ethereum’s continuing obligation to make those same committed bytes reconstructable.

This distinction becomes increasingly important as DA throughput grows. PeerDAS and FullDAS reduce the amount of total data any particular node must custody, but they do not make retained data free. Blob Streaming can move propagation outside the narrow block-production critical path, but it does not make network bandwidth free. Each scaling improvement changes the resource frontier without eliminating the underlying distinction between flow and stock.

Application semantics, by contrast, should remain outside the DA layer. Ethereum need not know whether bytes represent a rollup batch, encrypted message, game event, video segment, proof witness, or dataset. The protocol should price the resources those objects consume rather than their application type.

---

## 2. Logical service abstraction

The notation below describes a service quantity; it does not imply that current Ethereum sells arbitrary byte lengths. Under EIP-4844, the purchasable unit remains one whole blob of 4,096 field elements: a transaction carries an integer number of blobs and pays `GAS_PER_BLOB` for each one, even when the application leaves part of a blob unused. In the conservative EIP-4844-compatible version of this proposal, every blob commitment therefore has the same protocol-derived accounting size `B_blob`. The purchaser chooses `T`, not `B`.

It is still useful to write the transport-neutral service as:

```text
DAService(C,B,T)
```

meaning:

> Make the protocol-accounted quantity `B` corresponding to commitment `C` available under Ethereum's publication-time DAS rules, and require the assigned custody population to retain and serve enough authenticated data for reconstruction through expiration `T`, under the specified custody assumptions.

For a current blob, `B=B_blob` is derived from the blob type and need not be supplied by the application. A transaction with `n` blobs creates `n` commitment-level obligations, each with fixed quantity `B_blob`; it does not purchase one arbitrary-sized object of quantity `n·B_blob` or pay only for useful bytes. A submission would minimally specify:

- a commitment to the data;
- the requested retention duration or expiration;
- and authorization to consume the required DA capacity.

A future versioned data-object or streaming transport could define other allowed accounting units and carry an explicit size. That would require its own framing, commitment, fee, and physical-accounting rules. It is not supplied by EIP-4844 and is not required for blob-granular variable retention.

Publication timing may eventually become another explicit dimension, particularly under Blob Streaming or future DA markets, but it is not necessary for the core variable-retention mechanism.

The underlying PeerDAS or future FullDAS machinery would establish publication-time availability in the ordinary way. Once availability has been established, the required-serving interval begins. Until expiration, the assigned custody participants remain obligated by the protocol to retain and serve their portions of the data.

After expiration:

> **Ethereum’s protocol-level retention and serving obligation ends.**

This does not imply universal deletion. Custody participants, applications, archives, storage providers, torrent-like swarms, EthStorage, Filecoin, or any interested third party may retain and serve copies indefinitely. Expiration terminates only this lease's protocol requirement that the relevant custody participants continue retaining and serving enough of the data for reconstruction. Continued service after expiry is permitted, but applications cannot rely on it without another enforceable service.

A compact commitment or versioned hash can remain as a durable integrity anchor after the payload itself expires, provided that applications or historical-data infrastructure preserve that anchor. Voluntarily retained copies or previously constructed proofs can then be authenticated against the Ethereum-published object. This should not be confused with a native protocol certificate that the data remained retrievable continuously throughout the entire retention interval; such a certificate would be an additional mechanism.

The protocol abstraction should sit above the present blob encoding:

> **A specified quantity of committed data was reconstructably available under Ethereum’s DA security assumptions, and protocol participants remain obligated to retain and serve sufficient custody data for reconstruction until a specified expiration.**

Applications should not depend on a particular arrangement of EIP-4844 blobs, PeerDAS columns, cells, KZG proofs, two-dimensional erasure coding, or future coding schemes. PeerDAS today, FullDAS later, and potentially a future continuous Danksharding-derived data fabric should all be capable of implementing the same semantic service.


### 2.1 Availability establishment versus retained retrievability

The term **data availability** can obscure two distinct claims.

At publication time, Ethereum must establish that the committed data is available under the relevant DAS rules so that the block or payload can be accepted safely. After publication, the network may also impose a **serving horizon** during which nodes remain obligated to retain and serve the recent data needed for reconstruction.

Under the current PeerDAS networking specification, this second property is concretely expressed as a minimum serving window for data-column sidecars. Variable retention would parameterize that post-publication serving obligation. It would not require consensus to re-attest every slot that an old object is still available.

At enforcement level 1, the mechanism makes the following claim through `T`:

> **the protocol requires the relevant custody participants to retain and serve sufficient data for reconstruction through `T`, under the security assumptions of the custody and sampling design.**

This distinction matters again after expiry. A commitment can authenticate a surviving copy, but a commitment by itself does not prove that the network honored the serving obligation at every moment before expiry. If historical proof of service is desired, it must be designed separately.

Expiry can still leave several durable artifacts: canonical inclusion of the commitment, evidence recorded at publication, openings or copies kept elsewhere, and proofs of computations completed while the bytes were available. The [ephemeral-data proving appendix](../appendices/ephemeral-data-and-proofs.md) distinguishes those claims and works through the pattern `D -> prove f(D)=y -> retain C(D), y, pi`.

The distinction may also permit a **change of physical representation through the object lifecycle**. The representation best suited to proving fresh availability need not be identical to the representation best suited to hundreds or thousands of epochs of historical serving. Section 17 branches between current 1D PeerDAS with cell-level historical custody and a conditional future 2D path that may transition from hot cross-row redundancy to cold row-local custody.

---

### 2.2 Three enforcement levels

“Available through `T`” can refer to three materially different services:

1. **Protocol-required serving.** Honest clients are specified to retain and serve their assigned authenticated data. Failure may affect peer scoring or compliance, but there is no recurring per-object consensus certificate proving that every old object remained reconstructable.
2. **Probabilistically monitored serving.** Custodians or peers are challenged or sampled during the serving interval, producing evidence about continued retrievability.
3. **Cryptoeconomically enforced retention.** A failed custody or service proof can trigger a penalty, loss of collateral, or another consensus-recognized consequence.

Those levels describe the force of enforcement, not what a particular proof establishes. A custody design must also say which claim is being tested:

- **acquisition or processing at a moment:** the assigned participant obtained and processed the data when required;
- **continued possession:** the participant still held the assigned data at one or more later checkpoints;
- **retrievability or service:** the participant returned authenticated data, or enough participants served data for reconstruction, within the required conditions.

Historical “bomb” proofs primarily make it costly to skip acquisition or processing at the tested moment. They do not automatically show that data was continuously possessed or retrievable throughout a lease of duration `T`. Proof of custody can enforce acquisition or possession, but a retention lease requires the protocol to define what must be proven, by whom, how often, and through which lifecycle transitions until expiry.

Current PeerDAS-style semantics most directly support level 1. EIP-7594 assigns deterministic custody, and the Fulu networking specification requires clients to serve recent data-column sidecars over a minimum range. The proposal changes how long that service is required. It does not add a historical proof-of-custody system.

Levels 2 and 3 are compatible extensions, not prerequisites. If either is adopted, the service claim and fee can explicitly name the stronger enforcement level. Older Ethereum proof-of-custody research is relevant prior art for level 3, but is not current PeerDAS behavior and is not yet a design for continuous retention and service.

---

### 2.3 Transport neutrality and lifecycle profiles

The single duration `T` is the conservative base mechanism, not necessarily the final shape of the service. The proposal applies to availability obligations over committed Ethereum data regardless of whether a future protocol exposes EIP-4844 blobs, granular Lean Data objects, payload-blobs, FullDAS cells, or another coded transport.

Research on Block-in-Blobs and integrated distributed history suggests a later generalization from one expiry to a lifecycle profile:

```text
L = (T_full, f_tail, T_tail)
```

where `T_full` is the full-strength serving window and an optional fraction `f_tail` remains under a reduced obligation for `T_tail`. Ordinary expiry remains the special case `L=(T,0,0)`. A permanent sparse-history tail is another possible profile; it is not equivalent to full retrievability forever.

The protocol still need not understand application semantics. It needs only the commitment, its type-derived accounting quantity, the applicable access class, and the lifecycle obligation. A future variable-size object type would also need an explicit size rule. Some profiles may be purchaser-selected; protocol-mandated data such as canonical L1 history would inherit a protocol-defined profile.

[The Lean Ethereum compatibility note](10-how-does-lean-ethereum-change-the-proposal.md) develops this extension and its limits.

### 2.4 A weaker availability service is out of scope

Another design could stop at committee custody or recipient-only delivery:

```text
global publication
    -> bounded committee custody
    -> recipient-specific delivery
```

That service might save more bandwidth, but it would give up the permissionless global-reconstruction semantics of Ethereum DAS. A recipient or favored committee could possess data that an arbitrary sampler or later independent retriever could not obtain. This RFC keeps PeerDAS/FullDAS-style publication semantics and varies only the post-publication serving duration. A weaker packet-delivery primitive may be useful elsewhere, but it is not `DAService(C,B,T)` as defined here.

## 3. Minimum and maximum protocol-required retention

Variable retention should initially be bounded:

```text
T_min ≤ T ≤ T_max.
```

This RFC expresses protocol retention in epochs. At the current 32 slots per epoch and 12 seconds per slot, one epoch is 384 seconds. Power-of-two maturities give implementations and users a compact common vocabulary:

| Epochs | Approximate wall-clock time |
|---:|---:|
| 1 | 6.4 minutes |
| 8 | 51.2 minutes |
| 64 | 6.83 hours |
| 256 | 1.14 days |
| 512 | 2.28 days |
| 1,024 | 4.55 days |
| 2,048 | 9.10 days |
| 4,096 | 18.20 days |

This table is a duration vocabulary, not a proposed allowed set. A concrete protocol can omit any maturity below `T_hot`, expose only a subset such as `256, 512, 1,024, 2,048, 4,096`, or permit every epoch value within the bounds.

A minimum is necessary because “zero-retention” DA cannot literally disappear at publication. The network requires time to disperse data, sample it, establish availability, and allow interested parties a meaningful opportunity to retrieve it.

Highly ephemeral DA therefore means:

> **minimal mandatory retention after availability has been established**

rather than instantaneous deletion.

The precise minimum is a security parameter. If Ethereum claims that data was available, independent parties should have a meaningful opportunity to retrieve and replicate the object before protocol custody is permitted to end.

A maximum protocol-required horizon is important for a different reason. Every accepted lease creates a specified resource obligation through time. A conservative first implementation can set `T_max` no higher than the current PeerDAS minimum serving horizon. It then never lets a purchaser impose a protocol serving obligation for any individual object beyond the duration already required by the existing system. `T_max` is not a pruning deadline: protocol participants may retain and serve the object longer, just as a minimum serving horizon does not require deletion when it ends. Such later service is best-effort unless backed by a separate enforceable service.

If the physical implementation uses the two-phase lifecycle developed in §17, there is also a concrete lower bound imposed by the DAS machinery itself. Let `T_hot` denote the common interval—or protocol-recognizable phase—during which every newly admitted object must remain in the rich availability-establishment representation. Then an independently expiring lease cannot end before that phase:

```text
T_min ≥ T_hot.
```

The cleanest implementation may define the purchaser-selected duration as the required serving interval **after** the mandatory hot phase, or may expose one total expiry while enforcing `T≥ T_hot`. The paper does not assume that `T_hot` must extend to ordinary Ethereum finality; §17 compares concrete transition candidates.

### 3.1 Two deployment regimes

It is useful to distinguish a conservative deployment from a later capacity-unlocking regime.

**Conservative regime.** Ethereum leaves ingress limits unchanged and sets `T_max` no higher than the present minimum serving horizon. The mechanism can reduce the protocol-required retained-data obligation but cannot increase its logical worst case relative to fixed retention. Nodes remain free to retain or serve expired objects voluntarily. In this regime the primary benefits are resource savings, price differentiation, and application flexibility.

**Capacity-unlocking regime.** Ethereum raises ingress throughput because a material share of traffic is expected to choose shorter retention. Active retained stock then becomes an independent safety constraint. Importantly, this still does **not** imply that the spot-start protocol needs a full forward reservation curve. Every accepted lease occupies retained capacity immediately. A hard active-stock ceiling can therefore bound the physical obligation as long as leases begin at admission. Forward capacity accounting becomes necessary when the protocol sells obligations that begin in the future.

### 3.2 Resource-allocation dominance under fixed ingress

The conservative case permits a precise claim.

Let the existing fixed serving horizon be `H`. For an admitted workload with objects `i`, protocol-accounted quantities `B_i`, and publication times `t_i`, define:

```text
S_fixed(t)
=
Σ_i B_i 1[t_i≤ t<t_i+H]
```

and let the variable-retention system choose `T_i≤ H`:

```text
S_var(t)
=
Σ_i B_i 1[t_i≤ t<t_i+T_i].
```

Then, for every `t`,

```text
S_var(t) ≤ S_fixed(t).
```

This inequality does not require continuous sizing. In the EIP-4844-compatible case, every `B_i` is the same fixed `B_blob`; the sum simply counts live blob commitments in byte-equivalent accounting units. The more general notation allows a future transport to define additional discrete object classes without assuming that such a transport already exists.

Every workload admitted under fixed retention can be reproduced exactly by choosing `T_i=H` for every object. Any workload in which at least some objects choose shorter horizons can consume strictly less logical retained capacity during their fixed-only tail intervals.

Thus:

> **Holding ingress and the maximum protocol-required horizon fixed, variable retention weakly dominates fixed retention in logical retained-capacity consumption.**

This is deliberately a **resource-allocation** statement, not a claim of total protocol dominance. Heterogeneous expiry may impose metadata, packing, proof, repair, request, and storage-engine overheads. Those physical implementation costs must be compared against the logical savings before an implementation claim can be made.

---
