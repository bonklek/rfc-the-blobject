# What is the conclusion?

## 23. Conclusion

The adversarial pass leaves the core hypothesis intact but simplifies its mechanism.

Fixed blob retention bundles immediate ingress with one protocol serving horizon. Under fixed ingress and `T_max` no greater than that horizon, variable retention weakly dominates fixed retention in **logical retained-capacity consumption**: the fixed service remains available as a special case, while shorter-lived objects consume less byte-time.

The narrow spot-start system does not require a maturity-dependent forward hard-cap curve. Every lease begins consuming retained capacity immediately, so a physically derived active-stock ceiling `K_safe` is sufficient to bound already-contracted storage obligations. A separate reserve `H_min` can preserve a chosen minimum-liveness lane against long-lease crowd-out. Prices then allocate guaranteed byte-time below those safety bounds.

This simplification also clarifies the real implementation risk. Logical savings do not automatically become physical savings under DAS. Current PeerDAS creates a column-packaging problem; proposed two-dimensional FullDAS designs can create a deeper cross-row coding problem because shared parity may depend on blobs with different expirations.

The leading compatibility hypothesis is therefore a two-phase representation lifecycle: preserve the rich DAS code only through the hot fresh-availability phase, then discard hot-only shared redundancy and retain independently committed row-local cells under sparse duration-specific custody. If that transition is compatible with FullDAS security, continuous logical retention can survive without maturity-homogeneous hot frames. If it is not, a small number of maturity-aligned coding domains becomes the conservative fallback.

The L2 resilience claim also survives only conditionally. Applications gain graceful degradation to the extent that proving, recovery, watcher, and archival architectures permit a shorter Ethereum serving horizon without introducing unacceptable trust assumptions.

The forward retained-capacity curve reappears at the point where it is genuinely needed: when Ethereum sells future-starting ingress and retention obligations. Blob Streaming-style tickets then supply a plausible future delivery date; variable retention supplies a maturity; and the protocol must bound occupancy over future intervals that are not yet represented in active stock.

The broader thesis consequently becomes more, not less, coherent:

```text
bandwidth × availability through time.
```

Short base guarantees can hand committed objects to competing persistence networks. Transferable future rights raise settlement and privacy questions. Specialized systems can provide routing, indexing, privacy, and long-term storage while Ethereum supplies scarce admission, integrity, and bounded protocol-secured retrievability.

The scope remains intentionally expansive. The adversarial result is that the expansion no longer needs to be carried by an unnecessarily elaborate narrow mechanism.

---

## Research status and implementation anchors

This working draft now distinguishes established mechanisms, current drafts, adjacent systems, and proposed extensions:

- **[EIP-4844](https://eips.ethereum.org/EIPS/eip-4844)** — blob transactions, KZG commitments/versioned hashes, and the original blob resource.
- **[EIP-7594 / PeerDAS](https://eips.ethereum.org/EIPS/eip-7594)** — current column-based DA sampling and custody ([Fulu networking specification](https://github.com/ethereum/consensus-specs/blob/master/specs/fulu/p2p-interface.md); [design discussion](https://github.com/ethereum/consensus-specs/issues/3652)). The mainnet Fulu configuration sets `MIN_EPOCHS_FOR_DATA_COLUMN_SIDECARS_REQUESTS` to 4096 epochs; current P2P rules require clients to keep and serve recent data-column sidecars over that window.
- **[EIP-8256 / Blob Streaming (draft)](https://eips.ethereum.org/EIPS/eip-8256)** ([discussion](https://ethereum-magicians.org/t/eip-8256-blob-streaming/28586)) — non-refundable AOT tickets for future propagation capacity, separate JIT/AOT limits, `JIT_RESERVED`, owner-based mempool allowance, and BLS-authenticated AOT propagation. It does not itself provide variable retention, ticket transferability, or mandatory inclusion.
- **[EIP-4444](https://eips.ethereum.org/EIPS/eip-4444)** ([discussion](https://ethereum-magicians.org/t/eip-4444-bound-historical-data-in-execution-clients/7450)) — fixed expiry of historical execution-layer P2P serving, relevant prior art for separating protocol verification from indefinite historical service.
- **[Optimism](https://docs.optimism.io/op-stack/fault-proofs/explainer) and [Arbitrum](https://docs.arbitrum.io/nitro-whitepaper.pdf) fault-proof documentation** — current challenge windows around one week, relevant to realistic lower bounds and additional archival assumptions for optimistic rollups.
- **[Celestia retrievability/pruning](https://docs.celestia.org/learn/celestia-101/retrievability/)** — fixed recent sampling/pruning window with longer persistence delegated elsewhere, adjacent to the DA-versus-history distinction.
- **[Filecoin](https://docs.filecoin.io/storage-providers/filecoin-economics/storage-proving)** — explicit-duration, provider-backed storage deals and spacetime economics, prior art for pricing persistence through time rather than for Ethereum DA itself.
- **[EthStorage](https://docs.ethstorage.io/readme/how-ethstorage-works)** — Ethereum-oriented downstream storage with provider retrieval and storage proofs, concrete evidence for the wholesale-availability / downstream-retention handoff.
- **[FullDAS](https://ethresear.ch/t/fulldas-towards-massive-scalability-with-32mb-blocks-and-beyond/19529) / [FullDASv2](https://ethresear.ch/t/accelerating-blob-scaling-with-fulldasv2-with-getblobs-mempool-encoding-and-possibly-rlc/22477) research** — proposed two-dimensional erasure-code DA designs with cell-level messaging, blobs as rows, cross-cutting columns, and row/column repair or availability amplification. [Secure 1D/2D DAS analysis](https://ethresear.ch/t/revisiting-secure-das-in-one-and-two-dimensions/22762) and [cell-level dissemination research](https://ethresear.ch/t/gossipsubs-partial-messages-extension-and-cell-level-dissemination/23017) provide additional context. These mechanisms motivate both sides of §17: sparse cells help with packaging, while cross-row coding creates the deeper expiry-coupling problem. The paper's hot-dense/cold-sparse lifecycle is a proposed compatibility hypothesis, not an established FullDAS feature.

No source above is claimed to implement the complete proposal. The novelty claim is the particular decomposition and composition described in §21.7.

---
