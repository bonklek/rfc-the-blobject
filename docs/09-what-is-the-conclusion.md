# What is the conclusion?

## 23. Conclusion

Ethereum currently bundles immediate blob ingress with one protocol serving horizon. This RFC separates them. The conservative deployment sets `T_max` equal to today's minimum serving horizon, so that duration remains selectable while the design preserves the other relevant DA guarantees. With ingress fixed and every selected `T` no greater than that current horizon, variable retention can only reduce **logical protocol-required retained-capacity consumption**; shorter-lived objects consume less required byte-time. `T_max` limits the obligation a purchaser may impose, but it neither requires pruning at expiry nor prevents voluntary service afterward.

The proposal changes time, not audience. Global availability, designated custody, and recipient delivery are different guarantees. The Blobject would retain Ethereum's permissionless DAS reconstruction semantics, require distributed custody to support them through `T`, and leave recipient acknowledgements or committee-only packet delivery to separate application services.

A spot-start lease consumes retained capacity as soon as it is accepted. Deterministic active-stock accounting can therefore bound contracted obligations without a maturity-dependent forward hard-cap curve. Admission still has to respect the full `K_safe_vector`, not storage alone. An `H_min` reserve can stop long leases from pre-consuming a short-duration lane, although it cannot stop an attacker from flooding that lane directly. Pricing allocates byte-time only after those safety bounds have been enforced.

The lease is attached to a canonical blob publication rather than treating its content commitment as a unique identity. Its total duration runs from inclusion slot to slot-derived expiry, includes any mandatory hot phase, and remains governed by the versioned service profile under which it was admitted. Service may end before conservative admission accounting credits the physical capacity back; reclamation lag and backlog are part of the safety envelope.

The main risk is physical rather than logical. Expiring an obligation in protocol state does not necessarily release storage or repair capacity in the DAS representation. Current PeerDAS has a column-packaging problem. A cross-row 2D FullDAS design would add a deeper problem because shared parity may depend on blobs with different expirations.

The first prototype should therefore test current 1D PeerDAS with cell-level transport, which has no cross-row parity to preserve, and determine whether sparse historical serving releases enough physical capacity to justify its overhead. If Ethereum later adopts a 2D code, one option is to keep the richer code through a hot phase and then retain independently committed row-local cells. If that transition is not safe or economical, a small number of maturity-aligned coding domains remains the fallback.

Hardware imposes a separate limit. Shorter retention lowers resident stock but not the write stream created by a fixed ingress rate. At sufficiently high throughput, duration-aware placement, wear balancing, and fractional custody pools may broaden the operator set. If Ethereum pays those operators directly, the scarcity burn should remain separate from `q_write · B + q_retention · B · T` service payments. Posted procurement prices should move gradually, and concentrated or insufficient supply should lower the safe DA target rather than push payments beyond a service-price ceiling.

Network conservation is equally unforgiving. Coding and replication multiply the global stream, so operator count times sustainable per-node bandwidth must cover the expanded traffic. At backbone scale, today's 128 KiB object and per-cell proof surface produces extreme object and proof counts. A credible design would need multiplexed continuous frames, not a simple multiplication of today's blobs.

Expiry can still leave durable knowledge. Ethereum may retain a commitment while an application retains `y` and a proof that `f(D)=y`, even after the large witness `D` leaves protocol service. The proof establishes a claim about the committed data; it does not establish continuous historical availability, and a late node cannot repeat sampling against bytes that no longer exist.

Rollups can shorten their Ethereum serving horizon only when their proving, recovery, watcher, and archival systems can absorb the change without unacceptable new trust assumptions. The proposal offers graceful degradation; it does not manufacture retention elasticity where none exists.

Forward retained-capacity accounting becomes necessary when Ethereum sells ingress or retention obligations that begin in the future. Blob Streaming-style tickets can supply a delivery date, variable retention can supply a maturity, and the protocol must then bound occupancy over intervals that are not yet visible in active stock.

Together, these pieces describe a resource with two dimensions:

```text
bandwidth × availability through time.
```

The base mechanism remains narrow even though the surrounding research agenda is expansive. Short serving windows could hand committed objects to competing persistence networks. Transferable future rights introduce settlement and privacy questions. Specialized systems could provide routing, indexing, privacy, and long-term storage, while Ethereum provides scarce admission, integrity, and bounded protocol-required retrievability under explicit custody assumptions. None of those extensions is required for the spot-start mechanism: choose a serving duration, account for the resulting active stock, and test whether expiry releases real physical resources.

---

## Research status and implementation anchors

This working draft now distinguishes established mechanisms, current drafts, adjacent systems, and proposed extensions:

- **[EIP-4844](https://eips.ethereum.org/EIPS/eip-4844)** — blob transactions, KZG commitments/versioned hashes, and the original blob resource.
- **[EIP-7594 / PeerDAS](https://eips.ethereum.org/EIPS/eip-7594)** — current column-based DA sampling and custody ([Fulu networking specification](https://github.com/ethereum/consensus-specs/blob/master/specs/fulu/p2p-interface.md); [design discussion](https://github.com/ethereum/consensus-specs/issues/3652)). The mainnet Fulu configuration sets `MIN_EPOCHS_FOR_DATA_COLUMN_SIDECARS_REQUESTS` to 4,096 epochs, or about 18.2 days at current slot timing; current P2P rules require clients to keep and serve recent data-column sidecars over at least that window.
- **[EIP-8256 / Blob Streaming (draft)](https://eips.ethereum.org/EIPS/eip-8256)** ([discussion](https://ethereum-magicians.org/t/eip-8256-blob-streaming/28586)) — non-refundable AOT tickets for future propagation capacity, separate JIT/AOT limits, `JIT_RESERVED`, owner-based mempool allowance, and BLS-authenticated AOT propagation. It does not itself provide variable retention, ticket transferability, or mandatory inclusion.
- **[EIP-4444](https://eips.ethereum.org/EIPS/eip-4444)** ([discussion](https://ethereum-magicians.org/t/eip-4444-bound-historical-data-in-execution-clients/7450)) — fixed expiry of historical execution-layer P2P serving, relevant prior art for separating protocol verification from indefinite historical service.
- **[Optimism](https://docs.optimism.io/op-stack/fault-proofs/explainer) and [Arbitrum](https://docs.arbitrum.io/nitro-whitepaper.pdf) fault-proof documentation** — current challenge windows around one week (roughly 1,440–1,575 Ethereum epochs at current timing), relevant to realistic lower bounds and additional archival assumptions for optimistic rollups.
- **[Celestia retrievability/pruning](https://docs.celestia.org/learn/celestia-101/retrievability/)** — fixed recent sampling/pruning window with longer persistence delegated elsewhere, adjacent to the DA-versus-history distinction.
- **[Filecoin](https://docs.filecoin.io/storage-providers/filecoin-economics/storage-proving)** — explicit-duration, provider-backed storage deals and spacetime economics, prior art for pricing persistence through time rather than for Ethereum DA itself.
- **[EthStorage](https://docs.ethstorage.io/readme/how-ethstorage-works)** — Ethereum-oriented downstream storage with provider retrieval and storage proofs, concrete evidence for the wholesale-availability / downstream-retention handoff.
- **[FullDAS](https://ethresear.ch/t/fulldas-towards-massive-scalability-with-32mb-blocks-and-beyond/19529) / [FullDASv2](https://ethresear.ch/t/accelerating-blob-scaling-with-fulldasv2-with-getblobs-mempool-encoding-and-possibly-rlc/22477) research** — proposed two-dimensional erasure-code DA designs with cell-level messaging, blobs as rows, cross-cutting columns, and row/column repair or availability amplification. [Secure 1D/2D DAS analysis](https://ethresear.ch/t/revisiting-secure-das-in-one-and-two-dimensions/22762) and [cell-level dissemination research](https://ethresear.ch/t/gossipsubs-partial-messages-extension-and-cell-level-dissemination/23017) provide additional context. These mechanisms motivate both sides of §17: sparse cells help with packaging, while cross-row coding creates the deeper expiry-coupling problem. The paper's hot-dense/cold-sparse lifecycle is a proposed compatibility hypothesis, not an established FullDAS feature.

No source above is claimed to implement the complete proposal. The novelty claim is the particular decomposition and composition described in §21.10.

---
