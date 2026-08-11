# What is the proposal?

## Executive framing

Ethereum’s DA roadmap has principally scaled **how much data can be made available at once**. [EIP-4844](https://eips.ethereum.org/EIPS/eip-4844) separated blob data from execution gas; [PeerDAS (EIP-7594)](https://eips.ethereum.org/EIPS/eip-7594) distributes blob custody and sampling; the draft [Blob Streaming proposal (EIP-8256)](https://eips.ethereum.org/EIPS/eip-8256) explores reservable ahead-of-time propagation; and [FullDAS](https://ethresear.ch/t/fulldas-towards-massive-scalability-with-32mb-blocks-and-beyond/19529) points toward much larger distributed DA capacity. One dimension remains comparatively rigid: **how long every admitted byte must remain protocol-served**.

This paper asks whether that temporal obligation should itself become a parameter of the DA service. The argument proceeds in three layers.

**First, a conservative resource-allocation claim.** Today, ingress and retention are bundled: bytes that impose the same immediate propagation burden receive the same serving horizon even when their applications value persistence very differently. Letting a purchaser choose a bounded duration `T`, with `T_max` no longer than the current minimum serving horizon, can only weakly reduce the logical retained-data obligation for a fixed admitted workload. The existing fixed-retention service remains available as the special case `T=T_max`. Here, `T_max` limits only the protocol serving obligation a purchaser may impose; it is not a mandatory deletion time or a prohibition on longer voluntary service. Short-lived traffic can purchase less byte-time without changing its initial DA burden.

**Second, a scaling claim.** If Ethereum eventually uses those savings to raise ingress throughput, retained stock becomes a distinct scarce resource. The narrow spot-start mechanism does not require a full forward-capacity market: every lease begins occupying storage immediately, so an active-stock ceiling is enough to preserve physical safety. The difficult questions are instead how to derive that ceiling from the custody architecture, how much headroom to reserve for minimum-liveness traffic, how to price guaranteed byte-time, and how to make logical expiry produce real physical savings under DAS coding.

The leading compatibility hypothesis is now a **two-phase representation lifecycle**. Fresh data can use the rich representation optimized for rapid availability establishment; after that hot phase, still-live objects can transition to a cheaper sparse representation organized around independently committed blob rows/cells. Under current PeerDAS this principally addresses the dense column-sidecar packaging problem. Under proposed two-dimensional FullDAS designs it would additionally require that cross-row parity used for availability amplification be disposable after the hot phase. This “hot dense DAS → cold sparse row-local custody” design is plausible but unresolved; if the second-dimensional codeword must persist for the whole serving horizon, quantized maturity-aligned coding domains remain the fallback. A full forward retained-capacity curve becomes necessary only when Ethereum also sells **future-starting** DA or retention commitments.

**Third, an architectural claim.** Variable retention gives applications an additional degradation margin under congestion where their security model permits it. Combined with Blob Streaming-style future ingress rights, the same decomposition yields a market in timed bandwidth and timed retrievability. Short Ethereum guarantees can then hand objects to competing downstream storage providers, caches, archives, or P2P swarms. Ethereum becomes a wholesale availability and integrity substrate while specialized systems provide persistence, routing, privacy, and application semantics.

The narrow proposal does not depend on accepting that broader endpoint. Its central question is simply:

> **Why should every byte entering Ethereum DA purchase the same amount of future serving?**

The rest of the paper first establishes the conservative mechanism, then attacks its implementation and security assumptions, and only afterward follows the decomposition toward the larger data-plane thesis.

---

## 1. Ingress and retention are distinct economic resources

Data availability consumes at least two physically and economically distinct resources.

First, data must enter the network. It must be propagated, encoded, distributed, sampled, verified, and made reconstructably available. This is fundamentally a **flow resource**: bandwidth and real-time processing capacity.

Second, once availability has been established, the network must continue to custody, serve, repair, or re-replicate enough of the data for reconstruction. This is fundamentally a **stock resource**: storage capacity committed through time.

These costs should not necessarily be bundled.

A 100 MB object that needs to remain available for five minutes imposes approximately the same initial ingress burden as a 100 MB object that needs to remain available for two weeks. Their subsequent custody obligations, however, differ by roughly four orders of magnitude.

Conversely, shortening retention cannot eliminate the initial bandwidth requirement. A one-minute object must still be propagated and made available.

The natural first-order decomposition is therefore:

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

Under this model, an application would request something approximately like:

```text
DAService(C,B,T)
```

meaning:

> Make `B` bytes corresponding to commitment `C` reconstructably available under Ethereum’s DA security assumptions and guarantee their availability through expiration `T`.

A submission would minimally specify:

- a commitment to the data;
- its size;
- the requested retention duration or expiration;
- and authorization to consume the required DA capacity.

Publication timing may eventually become another explicit dimension, particularly under Blob Streaming or future DA markets, but it is not necessary for the core variable-retention mechanism.

The underlying PeerDAS or future FullDAS machinery would establish availability in the ordinary way. Once availability has been established, the guaranteed-retention interval begins. Until expiration, the appropriate custody participants remain obligated to retain and serve their assigned portions of the data.

After expiration:

> **Ethereum’s protocol-level retention and serving obligation ends.**

This does not imply universal deletion. Custody participants, applications, archives, storage providers, torrent-like swarms, EthStorage, Filecoin, or any interested third party may retain and serve copies indefinitely. Expiration terminates only this lease's protocol requirement that the relevant custody participants continue retaining and serving enough of the data for reconstruction. Continued service after expiry is permitted, but applications cannot rely on it without another guarantee.

A compact commitment or versioned hash can remain as a durable integrity anchor after the payload itself expires, provided that applications or historical-data infrastructure preserve that anchor. Voluntarily retained copies or previously constructed proofs can then be authenticated against the Ethereum-published object. This should not be confused with a native protocol certificate that the data remained retrievable continuously throughout the entire retention interval; such a certificate would be an additional mechanism.

The stable protocol abstraction should therefore sit above the present blob encoding:

> **A specified quantity of committed data was reconstructably available under Ethereum’s DA security assumptions, and protocol participants remain obligated to retain and serve sufficient custody data for reconstruction until a specified expiration.**

Applications should not depend on a particular arrangement of EIP-4844 blobs, PeerDAS columns, cells, KZG proofs, two-dimensional erasure coding, or future coding schemes. PeerDAS today, FullDAS later, and potentially a future continuous Danksharding-derived data fabric should all be capable of implementing the same semantic service.


### 2.1 Availability establishment versus retained retrievability

The term **data availability** can obscure two distinct claims.

At publication time, Ethereum must establish that the committed data is available under the relevant DAS rules so that the block or payload can be accepted safely. After publication, the network may also impose a **serving horizon** during which nodes remain obligated to retain and serve the recent data needed for reconstruction.

Under the current PeerDAS networking specification, this second property is concretely expressed as a minimum serving window for data-column sidecars. Variable retention would parameterize that post-publication serving obligation. It would not require consensus to re-attest every slot that an old object is still available.

Accordingly, throughout this paper, a guarantee “through `T`” should be read as:

> **the protocol requires the relevant custody participants to retain and serve sufficient data for reconstruction through `T`, under the security assumptions of the custody and sampling design.**

This distinction matters again after expiry. A commitment can authenticate a surviving copy, but a commitment by itself does not prove that the network honored the serving obligation at every moment before expiry. If historical proof of service is desired, it must be designed separately.

The distinction may also permit a **change of physical representation through the object lifecycle**. The representation best suited to proving fresh availability need not be identical to the representation best suited to days of historical serving. Section 17 develops the leading hypothesis: use dense DAS redundancy during the hot availability-establishment phase, then retain still-live objects through sparse row-local custody that can expire independently.

---

### 2.2 Transport neutrality and lifecycle profiles

The single duration `T` is the conservative base mechanism, not necessarily the final shape of the service. The proposal applies to availability obligations over committed Ethereum data regardless of whether a future protocol exposes EIP-4844 blobs, granular Lean Data objects, payload-blobs, FullDAS cells, or another coded transport.

Research on Block-in-Blobs and integrated distributed history suggests a later generalization from one expiry to a lifecycle profile:

```text
L = (T_full, f_tail, T_tail)
```

where `T_full` is the full-strength serving window and an optional fraction `f_tail` remains under a reduced obligation for `T_tail`. Ordinary expiry remains the special case `L=(T,0,0)`. A permanent sparse-history tail is another possible profile; it is not equivalent to full retrievability forever.

The protocol still need not understand application semantics. It needs only the commitment, size, applicable access class, and lifecycle obligation. Some profiles may be purchaser-selected; protocol-mandated data such as canonical L1 history would inherit a protocol-defined profile.

[The Lean Ethereum compatibility note](10-how-does-lean-ethereum-change-the-proposal.md) develops this extension and its limits.

## 3. Minimum and maximum guaranteed retention

Variable retention should initially be bounded:

```text
T_min ≤ T ≤ T_max.
```

A minimum is necessary because “zero-retention” DA cannot literally disappear at publication. The network requires time to disperse data, sample it, establish availability, and allow interested parties a meaningful opportunity to retrieve it.

Highly ephemeral DA therefore means:

> **minimal mandatory retention after availability has been established**

rather than instantaneous deletion.

The precise minimum is a security parameter. If Ethereum claims that data was available, independent parties should have a meaningful opportunity to retrieve and replicate the object before protocol custody is permitted to end.

A maximum guaranteed horizon is important for a different reason. Every guaranteed lease is a promise about resource consumption through time. A conservative first implementation can set `T_max` no higher than the current PeerDAS minimum serving horizon. It then never lets a purchaser impose a protocol serving obligation for any individual object beyond the duration already required by the existing system. `T_max` is not a pruning deadline: protocol participants may retain and serve the object longer, just as a minimum serving horizon does not require deletion when it ends. Such later service is best-effort unless backed by a separate guarantee.

If the physical implementation uses the two-phase lifecycle developed in §17, there is also a concrete lower bound imposed by the DAS machinery itself. Let `T_hot` denote the common interval—or protocol-recognizable phase—during which every newly admitted object must remain in the rich availability-establishment representation. Then an independently expiring lease cannot end before that phase:

```text
T_min ≥ T_hot.
```

The cleanest implementation may define the purchaser-selected duration as the guaranteed serving interval **after** the mandatory hot phase, or may expose one total expiry while enforcing `T≥ T_hot`. The paper does not assume that `T_hot` must extend to ordinary Ethereum finality; whether the hot-to-cold transition can occur substantially earlier is one of the principal compatibility questions.

### 3.1 Two deployment regimes

It is useful to distinguish a conservative deployment from a later capacity-unlocking regime.

**Conservative regime.** Ethereum leaves ingress limits unchanged and sets `T_max` no higher than the present minimum serving horizon. The mechanism can reduce the guaranteed retained-data obligation but cannot increase its logical worst case relative to fixed retention. Nodes remain free to retain or serve expired objects voluntarily. In this regime the primary benefits are resource savings, price differentiation, and application flexibility.

**Capacity-unlocking regime.** Ethereum raises ingress throughput because a material share of traffic is expected to choose shorter retention. Active retained stock then becomes an independent safety constraint. Importantly, this still does **not** imply that the spot-start protocol needs a full forward reservation curve. Every accepted lease occupies retained capacity immediately. A hard active-stock ceiling can therefore bound the physical obligation as long as leases begin at admission. Forward capacity accounting becomes necessary when the protocol sells obligations that begin in the future.

### 3.2 Resource-allocation dominance under fixed ingress

The conservative case permits a precise claim.

Let the existing fixed serving horizon be `H`. For an admitted workload with objects `i`, sizes `B_i`, and publication times `t_i`, define:

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

Every workload admitted under fixed retention can be reproduced exactly by choosing `T_i=H` for every object. Any workload in which at least some objects choose shorter horizons can consume strictly less logical retained capacity during their fixed-only tail intervals.

Thus:

> **Holding ingress and the maximum guaranteed horizon fixed, variable retention weakly dominates fixed retention in logical retained-capacity consumption.**

This is deliberately a **resource-allocation** statement, not a claim of total protocol dominance. Heterogeneous expiry may impose metadata, packing, proof, repair, request, and storage-engine overheads. Those physical implementation costs must be compared against the logical savings before an implementation claim can be made.

---
