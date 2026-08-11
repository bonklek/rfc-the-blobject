# What is the prior art, and what is novel?

## 21. Prior art and adjacent mechanisms

The dedicated prior-art search did not surface a current Ethereum proposal that combines **user-selected base-protocol DA serving duration, byte-time pricing, and DAS custody** in the form proposed here. It did surface several important neighboring mechanisms that narrow the novelty claim.

### 21.1 Fixed protocol expiry: [EIP-4444](https://eips.ethereum.org/EIPS/eip-4444) and [Celestia](https://docs.celestia.org/learn/celestia-101/retrievability/)

EIP-4444 bounds how long Ethereum execution clients are expected to serve historical block bodies and receipts. It establishes the general principle that consensus verification and indefinite P2P historical serving need not be the same obligation, but its horizon is protocol-wide rather than purchaser-selected or fee-priced.

Celestia similarly distinguishes recent DA/retrievability from long-term history: its light-node sampling/pruning design uses a seven-day sampling window—about 1,575 Ethereum epochs at current timing—with historical persistence delegated to archive infrastructure and rollup-specific mechanisms. This is strong prior art for the **DA-versus-persistence separation**, but not for a market in heterogeneous base-layer serving maturities.

### 21.2 Ethereum state rent and TTL research

Earlier [Ethereum state-rent and state-expiry research](https://ethereum.org/roadmap/statelessness/) explored charging for persistent resource consumption, time-to-live, eviction, and expiry bookkeeping. The analogy is valuable mainly as a warning: making lifetime explicit often moves complexity into indexing, eviction, revival, and adversarial edge cases. State rent concerns consensus state rather than DA custody, so the mechanism is not directly portable.

### 21.3 Timed storage markets: Filecoin

[Filecoin storage deals](https://docs.filecoin.io/storage-providers/filecoin-economics/storage-proving) make duration an explicit contract term and price storage over time. This is direct prior art for treating **spacetime** as an economic resource. The distinction is architectural: Filecoin sells provider-backed persistence, whereas this proposal asks Ethereum’s consensus DA/custody network to expose a bounded serving duration attached to an initial availability event.

### 21.4 Downstream retention: EthStorage

[EthStorage](https://docs.ethstorage.io/readme/how-ethstorage-works) supplies particularly close precedent for the handoff architecture. Its storage providers obtain Ethereum-associated data, retain it, prove storage, and receive contract-mediated rewards. This supports the claim that Ethereum publication can be a common ingestion event for later persistence without implying that EthStorage already implements variable base-protocol retention.

### 21.5 Future bandwidth reservation: Blob Streaming

Draft [EIP-8256](https://eips.ethereum.org/EIPS/eip-8256) ([discussion](https://ethereum-magicians.org/t/eip-8256-blob-streaming/28586)) supplies the closest adjacent mechanism for the **future ingress** half of the broader thesis. Its non-refundable AOT tickets reserve future propagation capacity, its `JIT_RESERVED` parameter preserves near-term capacity against AOT demand, and it separates ticket ownership from the BLS key used to authenticate propagation. It does not provide user-selected retention, transferable ticket markets, or mandatory inclusion.

### 21.6 FullDAS, two-dimensional coding, and cell-level transport

[FullDAS](https://ethresear.ch/t/fulldas-towards-massive-scalability-with-32mb-blocks-and-beyond/19529) and [FullDASv2](https://ethresear.ch/t/accelerating-blob-scaling-with-fulldasv2-with-getblobs-mempool-encoding-and-possibly-rlc/22477) research is directly relevant to the compatibility problem. Current proposals describe a **two-dimensional erasure-code** DAS construct with cell-level messaging, blobs as rows, cross-cutting columns, and in-network row/column repair or availability amplification. Separate [cell-level dissemination work](https://ethresear.ch/t/gossipsubs-partial-messages-extension-and-cell-level-dissemination/23017) likewise explores making independently verifiable cells the propagation unit rather than whole `DataColumnSidecar`s.

Draft [EIP-8136](https://eips.ethereum.org/EIPS/eip-8136) makes this direction concrete for current PeerDAS by allowing peers to exchange missing cells instead of complete columns. It is a backwards-compatible dissemination optimization, not a historical-retention design. The [1D-versus-2D analysis](https://ethresear.ch/t/revisiting-secure-das-in-one-and-two-dimensions/22762) further shows that 1D PeerDAS with cell-level messaging can support partial row reconstruction, keeping 1D as a viable simpler branch.

These mechanisms strengthen the plausibility of sparse serving for the PeerDAS packaging problem while making the deeper 2D issue explicit: second-dimensional coding can couple multiple blob rows into shared redundancy. The hot-2D/cold-1D lifecycle in §17 is **not** established FullDAS behavior; it is this paper's conditional compatibility hypothesis.

### 21.7 Proofs of custody and retention enforcement

Current PeerDAS assigns deterministic custody and specifies a minimum historical serving range, but it does not create a recurring consensus proof that each old object remained retrievable throughout that range.

Earlier Ethereum research on [one-bit and 0.001-bit proofs of custody](https://ethresear.ch/t/a-0-001-bit-proof-of-custody/7409) explored a stronger model: validators commit to data-dependent custody computations and can become slashable when a later reveal shows that they attested without holding the data. Those designs targeted earlier sharding architectures and are not directly portable to PeerDAS. They remain important prior art for distinguishing:

- protocol-required serving;
- probabilistically monitored serving;
- cryptoeconomically enforced retention.

The narrow proposal initially adopts the first level. Any move to challenges, custody bonds, or mass-slashable unavailability faults would be a separate enforcement extension with its own false-positive, correlation, and recovery risks.

### 21.8 Narrow novelty claim

The defensible novelty claim is therefore not “nobody has priced storage duration” or “nobody has separated availability from persistence.” Both have extensive precedent.

The narrower contribution is the composition:

> **treat Ethereum DA as a service with separately accounted ingress and bounded purchaser-selected protocol serving duration; make that duration a deterministic state transition over active retained stock; and extend the same resource decomposition to representation-aware custody and future resource markets.**

That claim should be updated if closer prior art emerges.

---
