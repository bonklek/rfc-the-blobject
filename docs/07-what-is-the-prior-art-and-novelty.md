# What is the prior art, and what is novel?

## 21. Prior art and adjacent mechanisms

As of the research cutoff recorded in [REFERENCES.md](../REFERENCES.md), we are not aware of an Ethereum proposal that combines **user-selected base-protocol DA serving duration, byte-time pricing, and DAS custody** in this form. Several neighboring mechanisms cover parts of the design and narrow what can reasonably be claimed as novel.

### 21.0 Source-to-design map

This map identifies the work being combined and the role of each connection. **Base** means the immediate-start retention mechanism; **branch** means a candidate implementation; **extension** means an additional service or market design; **context** means a precedent or constraint. Source versions and dated checks are recorded in [REFERENCES.md](../REFERENCES.md).

#### Philosophy, publication, and custody

| Sources being drawn in | Borrowed idea | Combination proposed here |
|---|---|---|
| [New forms of state](https://ethresear.ch/t/hyper-scaling-state-by-creating-new-forms-of-state/24052) and the [early decentralized-Web framing](https://blog.ethereum.org/2014/08/18/building-decentralized-web) | Specialized persistence/access guarantees; composing execution, communication, and storage | **Philosophy:** apply resource specialization to the lifetime of DA, then connect publication to application processing and persistence. [Application architecture](06-what-does-a-generalized-data-plane-enable.md#20-why-the-scope-matters) |
| [EIP-4844](https://eips.ethereum.org/EIPS/eip-4844), [EIP-7594](https://eips.ethereum.org/EIPS/eip-7594), and the [pinned Fulu P2P interface](https://github.com/ethereum/consensus-specs/blob/5366cb59eb39e4ec1d6c468a79cceb626c14c048/specs/fulu/p2p-interface.md) | Whole-blob publication, commitments, sampling, distributed custody, and recent historical serving | **Base:** add selected expiry to each publication and account for outstanding obligations. [Service definition](00-what-is-the-proposal.md#2-logical-service-abstraction) and [stock accounting](01-how-are-capacity-and-pricing-managed.md#4-flow-and-active-retained-stock) define this composition |
| [EIP-8136](https://eips.ethereum.org/EIPS/eip-8136) ([Magicians discussion](https://ethereum-magicians.org/t/eip-8136-cell-level-deltas-for-data-column-broadcast/27675)); [Gossipsub cell dissemination](https://ethresear.ch/t/gossipsubs-partial-messages-extension-and-cell-level-dissemination/23017); [EIP-8371 RowDAS](https://eips.ethereum.org/EIPS/eip-8371) ([discussion](https://ethereum-magicians.org/t/eip-8371-rowdas-distributed-blobspace-reconstruction/29320)); [1D/2D DAS analysis](https://ethresear.ch/t/revisiting-secure-das-in-one-and-two-dimensions/22762) | Missing-cell transport and row-level reconstruction | **1D branch:** extend that granularity to historical service after neighboring blobs expire. Expiry indexes, historical custody, repair, and reclamation remain this RFC's implementation work. [§17.1](05-can-this-work-with-peerdas-and-fulldas.md#171-problem-a-peerdas-column-packaging) |
| [FullDAS](https://ethresear.ch/t/fulldas-towards-massive-scalability-with-32mb-blocks-and-beyond/19529) and [FullDASv2](https://ethresear.ch/t/accelerating-blob-scaling-with-fulldasv2-with-getblobs-mempool-encoding-and-possibly-rlc/22477) | Two-dimensional coding, shared redundancy, and reconstruction/repair research | **2D branch:** combine shared initial redundancy with later row-local serving by expiry. That transition is this RFC's hypothesis; grouping similar maturities is its alternative. [Representation analysis](05-can-this-work-with-peerdas-and-fulldas.md) |

#### Publication scheduling and resource rights

| Sources being drawn in | Borrowed idea | Combination proposed here |
|---|---|---|
| [EIP-8070 Sparse Blobpool](https://eips.ethereum.org/EIPS/eip-8070) ([discussion](https://ethereum-magicians.org/t/eip-8070-sparse-blobpool/26023)); [DA in the EL mempool](https://ethresear.ch/t/is-data-available-in-the-el-mempool/22329); [sharded blob mempools](https://ethresear.ch/t/a-new-design-for-das-and-sharded-blob-mempools/22537); [Blob Notaries](https://ethresear.ch/t/blob-notaries-a-distributed-blob-publishing-design-to-scale-da/22709) | Sparse acquisition, multiple data sources, and distributed publication roles | **Publication extension:** combine distributed upload with ahead-of-time capacity and timed custody. These are adjacent or alternative designs informing [§17.9](05-can-this-work-with-peerdas-and-fulldas.md#179-aot-streaming-and-distributed-fulldas-dissemination) |
| [EIP-8256 Blob Streaming](https://eips.ethereum.org/EIPS/eip-8256) ([Magicians discussion](https://ethereum-magicians.org/t/eip-8256-blob-streaming/28586)); Julian Ma's [On In-Protocol Gas Futures](https://ethresear.ch/t/on-in-protocol-gas-futures/23698) | Paid AOT propagation, reserved near-term capacity, and physical future resource access | **Market extension:** pair future ingress with a retention maturity and account for overlapping future obligations. Future retention, transfer/settlement questions, and private activation extend the cited mechanisms. [Chapter 03](03-how-do-future-resource-markets-work.md) |
| [Waku protocols](https://docs.waku.org/learn/concepts/protocols/) and [topic privacy](https://docs.waku.org/learn/concepts/content-topics), alongside EIP-8256 authorization | Separated relay/retrieval roles, anonymous anti-spam techniques, and bounded network permissions | **Privacy extension:** privately held capacity activates a temporary public key for cheap peer authorization. This [activation construction](../appendices/private-aot-authorization.md) is proposed here; the privacy of content, payment, origin, and access patterns remains separately specified |

The 1D branch can be tested on its own. FullDAS and future-market extensions have separate requirements; the map identifies points of composition rather than requiring simultaneous adoption.

#### Applications, persistence, and accountability

| Sources being drawn in | Borrowed idea | Combination proposed here |
|---|---|---|
| [ERC-8179](https://eips.ethereum.org/EIPS/eip-8179) ([Magicians discussion](https://ethereum-magicians.org/t/erc-8179-blob-space-segments-bss/27867)); [ERC-8180](https://eips.ethereum.org/EIPS/eip-8180) ([discussion](https://ethereum-magicians.org/t/erc-8180-blob-authenticated-messaging-bam/27868)) | Application subrange declarations and authenticated-message interfaces | **Application composition:** combine formats and discovery with an acquisition window. [Blobcast and BlobMail](../audits/application-use-case-review.md) are the case studies. Subranges share their containing blob's lease; BlobMail's ciphertext is not claimed to implement the full public BAM stack |
| [Filecoin storage deals](https://spec.filecoin.io/systems/filecoin_markets/storage_market/), [EthStorage](https://docs.ethstorage.io/readme/how-ethstorage-works), [Swarm postage](https://docs.ethswarm.org/docs/concepts/incentives/postage-stamps/), and the [Codex storage marketplace](https://github.com/logos-storage/logos-storage-spec/blob/f238dd660409ce628f14572991f6c1d8dd71c5d1/specs/marketplace.md) | Duration pricing, publication-to-provider ingestion, prepaid retention value, and storage accountability | **Persistence extension and economic precedent:** combine an Ethereum acquisition window with separately contracted later service. [Chapter 04](04-what-happens-after-ethereum-retention-ends.md) and [RetentionNotes](../appendices/retention-notes.md) develop handoff and termination conditions |
| [2018 custody proposal](https://ethresear.ch/t/extending-skin-in-the-game-of-notarization-with-proofs-of-custody/1639/1) and [retained-history reply](https://ethresear.ch/t/extending-skin-in-the-game-of-notarization-with-proofs-of-custody/1639/4); [0.001-bit custody](https://ethresear.ch/t/a-0-001-bit-proof-of-custody/7409); [2020 mass-slashing proposal](https://ethresear.ch/t/mass-slashable-unavailability-faults/8129/1) and [reply](https://ethresear.ch/t/mass-slashable-unavailability-faults/8129/4) | Acquisition incentives, claims over retained history, and distinct slashing/deterrence constructions | **Accountability research:** frame possible stronger enforcement for timed custody. The base uses protocol-required serving; recurring proofs or penalties require a separate design. [§21.9](#219-proofs-of-custody-and-retention-enforcement) preserves the distinctions |
| [EIP-8142 Block-in-Blobs](https://eips.ethereum.org/EIPS/eip-8142) ([discussion](https://ethereum-magicians.org/t/eip-8142-block-in-blobs-bib/27621)); [distributed history/state](https://ethresear.ch/t/integrated-in-protocol-distributed-history-and-state-storage/23522); [The Extremely Lean Chain](https://ethresear.ch/t/the-extremely-lean-chain/25369/1) | Protocol payloads in blobs, permanent sparse history, and proof-backed separation of state responsibilities | **Compatibility extension:** distinguish application leases, mandated payload duties, permanent records, and active state while examining their shared resource accounting. [Chapter 10](10-how-does-lean-ethereum-change-the-proposal.md) |

Other EIPs play narrower roles: **[EIP-4444](https://eips.ethereum.org/EIPS/eip-4444)** is a history-expiry precedent; **[EIP-7805 FOCIL](https://eips.ethereum.org/EIPS/eip-7805)** informs the separate inclusion-censorship discussion; and pinned **[EIP-8135](https://github.com/ethereum/EIPs/blob/169a65510927f58bdafdc67e840d53020e7a91ca/EIPS/eip-8135.md)** supplies a dated throughput calibration. These are context or constraints. Section 21.5.1 separately traces cash-settled derivatives and proposer-backed delivery as market precedents.

#### What Wikipethia contributed

[JossDuff/wikipethia](https://github.com/JossDuff/wikipethia) supplied discovery across Ethereum research and Magicians material. The bounded September pass promoted four findings:

1. **RowDAS:** a closer row-reconstruction reference, including its open historical retrieval and custody interface.
2. **Retained-history custody:** the 2018 storeback reply, clarifying that earlier custody work also considered data retained over time.
3. **Mass-slashing distinctions:** the 2020 original and reply, separating aggregate-slashing claims from modified sampling deterrence.
4. **[Variants of Mempool Tickets](https://ethresear.ch/t/variants-of-mempool-tickets/23338/1):** reusable propagation permissions concern a different resource from post-inclusion retention leases.

The [discovery record](../audits/wikipethia-review.md) contains the ten queries, contextual reads, original-source checks, and unpromoted leads. Technical attribution belongs to the original EIPs and posts. The Magicians links above identify declared discussion venues; mechanism summaries rely on specifications and the reviewed source record, rather than treating discussion as adoption or endorsement.

The base synthesis is **committed blob publication + distributed custody + a selected serving duration + accounting for outstanding obligations**. The map identifies where existing work supplies a building block and where this RFC adds an interface, lifecycle, or market rule.

### 21.1 Fixed protocol expiry: [EIP-4444](https://eips.ethereum.org/EIPS/eip-4444) and [Celestia](https://docs.celestia.org/learn/celestia-101/retrievability/)

EIP-4444 bounds how long Ethereum execution clients are expected to serve historical block bodies and receipts. It establishes the general principle that consensus verification and indefinite P2P historical serving need not be the same obligation, but its horizon is protocol-wide rather than purchaser-selected or fee-priced.

Celestia also separates recent DA/retrievability from long-term history. Its light-node sampling/pruning design uses a seven-day sampling window—about 1,575 Ethereum epochs at current timing—and delegates historical persistence to archive infrastructure and rollup-specific mechanisms. It establishes precedent for the **DA-versus-persistence separation**, but not for a market in heterogeneous base-layer serving maturities.

### 21.2 Ethereum state rent and TTL research

Earlier [Ethereum state-rent and state-expiry research](https://ethereum.org/roadmap/statelessness/) explored charging for persistent resource consumption, time-to-live, eviction, and expiry bookkeeping. The analogy is valuable mainly as a warning: making lifetime explicit often moves complexity into indexing, eviction, revival, and adversarial edge cases. State rent concerns consensus state rather than DA custody, so the mechanism is not directly portable.

### 21.3 Timed storage markets: Filecoin

[Filecoin storage deals](https://spec.filecoin.io/systems/filecoin_markets/storage_market/) make duration an explicit contract term and price storage over time. Filecoin therefore provides direct precedent for treating **spacetime** as an economic resource. Its architecture is different: Filecoin sells provider-backed persistence, whereas this proposal attaches a bounded serving duration to an initial availability event in Ethereum's consensus DA/custody network.

### 21.4 Downstream retention: EthStorage

[EthStorage](https://docs.ethstorage.io/readme/how-ethstorage-works) is close precedent for the handoff architecture. Its storage providers obtain Ethereum-associated data, retain it, prove storage, and receive contract-mediated rewards. Ethereum publication can therefore serve as a common ingestion event for later persistence, although EthStorage does not implement variable base-protocol retention.

Waku Store, Swarm, and Codex expose three other useful points on the retention spectrum. [Waku Store](https://docs.waku.org/run-node/config-options) supports bounded time-, capacity-, or size-based message retention, but Waku explicitly does not promise general long-term availability. [Swarm postage stamps](https://docs.ethswarm.org/docs/concepts/incentives/postage-stamps/) prepay a batch whose storage value depletes through time and can be extended by top-up; this is close economic precedent for prepaid retention value decaying as service is consumed. The pinned [Codex marketplace specification](https://github.com/logos-storage/logos-storage-spec/blob/f238dd660409ce628f14572991f6c1d8dd71c5d1/specs/marketplace.md) names a duration, requires provider collateral, and randomly requires storage proofs during the interval. None supplies Ethereum consensus DA, but together they distinguish temporary caching, prepaid network storage, and accountable duration contracts.

### 21.5 Future bandwidth reservation: Blob Streaming

Draft [EIP-8256](https://eips.ethereum.org/EIPS/eip-8256) ([discussion](https://ethereum-magicians.org/t/eip-8256-blob-streaming/28586)) is the closest adjacent mechanism for **future ingress**. Its non-refundable AOT tickets reserve future propagation capacity, its `JIT_RESERVED` parameter preserves near-term capacity against AOT demand, and it separates ticket ownership from the BLS key used to authenticate propagation. It does not provide user-selected retention, transferable ticket markets, or mandatory inclusion.

#### 21.5.1 Blockspace and blobspace futures

There is a recognizable market lineage adjacent to AOT tickets. Julian Ma's [On In-Protocol Gas Futures](https://ethresear.ch/t/on-in-protocol-gas-futures/23698), motivated by Vitalik Buterin's gas-futures framing, develops protocol-issued access to future blockspace and emphasizes physical rather than merely cash settlement. Tamara Tran's [blobspace derivatives](https://paragraph.com/@tamaratran/introducing-ethereum-blobspace-derivatives) start from cash-settled exposure to the blob base fee while identifying physical delivery as a further research direction. Luban/Taiyi's [blob futures](https://paragraph.com/@luban-2/luban-unveils-blob-futures-pre-settle-blobs-on-ethereum) move toward proposer- or underwriter-backed commitments to include blobs in future slots.

The progression is therefore:

```text
cash-settled price exposure
    -> proposer-backed physical delivery
    -> protocol-native future DA rights.
```

These categories should not be collapsed. A cash-settled derivative hedges price but cannot force publication. A proposer-backed promise adds counterparty and proposer-performance risk. A protocol-native right could reserve ingress capacity, but still requires explicit settlement, expiry, reassignment, and inclusion semantics. The future-resource construction in this RFC combines reserved ingress with a retention maturity; it does not claim invention of blockspace futures.

### 21.6 FullDAS, two-dimensional coding, and cell-level transport

The September follow-up also checked [Draft RowDAS, EIP-8371](https://eips.ethereum.org/EIPS/eip-8371). It develops row reconstruction while leaving historical requests and row-serving obligations to an extension. This is relevant 1D prior art, not an implementation of selectable retention.

[FullDAS](https://ethresear.ch/t/fulldas-towards-massive-scalability-with-32mb-blocks-and-beyond/19529) and [FullDASv2](https://ethresear.ch/t/accelerating-blob-scaling-with-fulldasv2-with-getblobs-mempool-encoding-and-possibly-rlc/22477) research is directly relevant to the compatibility problem. Current proposals describe a **two-dimensional erasure-code** DAS construct with cell-level messaging, blobs as rows, cross-cutting columns, and in-network row/column repair or availability amplification. Separate [cell-level dissemination work](https://ethresear.ch/t/gossipsubs-partial-messages-extension-and-cell-level-dissemination/23017) likewise explores making independently verifiable cells the propagation unit rather than whole `DataColumnSidecar`s.

[EIP-8136](https://eips.ethereum.org/EIPS/eip-8136) makes this direction concrete for current PeerDAS by allowing peers to exchange missing cells instead of complete columns. It is a backwards-compatible dissemination optimization, not a historical-retention design. The [1D-versus-2D analysis](https://ethresear.ch/t/revisiting-secure-das-in-one-and-two-dimensions/22762) further shows that 1D PeerDAS with cell-level messaging can support partial row reconstruction, keeping 1D as a viable simpler branch.

Several distributed-publication proposals strengthen the provenance of the AOT-plus-FullDAS synthesis in §17.9. [Is Data Available in the EL Mempool?](https://ethresear.ch/t/is-data-available-in-the-el-mempool/22329) uses `getBlobs` and a multi-source execution-layer mempool so a builder need not transmit every selected blob by itself. [A New Design for DAS and Sharded Blob Mempools](https://ethresear.ch/t/a-new-design-for-das-and-sharded-blob-mempools/22537) combines partial column dissemination with sharded blob acquisition and distributed block building. [EIP-8070: Sparse Blobpool](https://eips.ethereum.org/EIPS/eip-8070) aligns sparse storage and sampling with custody while retaining `getBlobs` retrieval. [Blob Notaries](https://ethresear.ch/t/blob-notaries-a-distributed-blob-publishing-design-to-scale-da/22709) separates initial validation and distributed blob publication through a notary layer.

The shared question is how to avoid making one proposer or builder the synchronous source of the entire DA payload. These designs make that direction plausible; they do not by themselves establish the representation transition, retention accounting, or security of §17.9.

These mechanisms strengthen the plausibility of sparse serving for the PeerDAS packaging problem while making the deeper 2D issue explicit: second-dimensional coding can couple multiple blob rows into shared redundancy. The hot-2D/cold-1D lifecycle in §17 is **not** established FullDAS behavior; it is this paper's conditional compatibility hypothesis.

### 21.7 Blobspace multiplexing and messaging: ERC-8179 and ERC-8180

Draft [ERC-8179: Blob Space Segments](https://eips.ethereum.org/EIPS/eip-8179) defines an event-only interface that binds a field-element subrange of an EIP-4844 blob to its versioned hash and a content tag. It establishes precedent for application multiplexing inside one blob, but not for variable physical retention. Segment negotiation, construction, and fee splitting remain out of scope.

Draft [ERC-8180: Blob Authenticated Messaging](https://eips.ethereum.org/EIPS/eip-8180) builds on ERC-8179 with interfaces for registered message batches, on-chain decoder discovery, signature registries, and optional message exposure. It treats blobs as a transport for authenticated messages beyond rollups while leaving aggregation, archival, and fee splitting to other layers.

Together, these drafts show that non-rollup blob use is more than a hypothetical. They do not provide duration-aware admission, custody, operator procurement, or network-layer privacy.

### 21.8 P2P privacy and economically constrained overlays

[Waku's protocol family](https://docs.waku.org/learn/concepts/protocols/) separates gossip relay, light push, filtering, storage, and RLN-based rate limiting. RLN Relay is especially relevant because it uses zero-knowledge membership and nullifiers to limit spam without requiring every message to reveal a stable publisher identity. This is precedent for anonymous economic admission above a P2P data plane, not a complete solution for payer, IP-origin, recipient, or access-pattern privacy.

Waku's [content-topic privacy guidance](https://docs.waku.org/learn/concepts/content-topics) makes the remaining leakage concrete. Request/response protocols reveal topic interests to peers, and a narrow topic shrinks the recipient anonymity set. Mix or onion ingress protects the link between an origin IP and its first peer. End-to-end encryption protects content. Shielded payment protects the purchase graph. None of these protections implies the others.

The [Lightning Network paper](https://lightning.network/lightning-network-paper.pdf) supplies a broader analogy: frequent interactions can move to a specialized network while retaining base-layer settlement and enforceability. The comparison here is limited to publication and service. A DA overlay is not a payment channel and does not inherit Lightning's guarantees.

The [private AOT authorization note](../appendices/private-aot-authorization.md) combines these ideas in one candidate design: shield capacity ownership, activate a public ephemeral key with one canonical proof, and let peers reject unknown keys before expensive payload validation. That construction is proposed here; it is not functionality already supplied by Waku, RLN, or EIP-8256.

### 21.9 Proofs of custody and retention enforcement

The [2018 custody proposal](https://ethresear.ch/t/extending-skin-in-the-game-of-notarization-with-proofs-of-custody/1639/1) and [Justin Drake's retained-history extension](https://ethresear.ch/t/extending-skin-in-the-game-of-notarization-with-proofs-of-custody/1639/4) considered repeated claims over a notary's retained data. Historical custody research therefore reaches beyond acquisition at publication. It does not supply this RFC's heterogeneous expiry, repair, reassignment, or permissionless service mechanism.

The [mass-slashable unavailability proposal](https://ethresear.ch/t/mass-slashable-unavailability-faults/8129/1) and [Dankrad Feist's modification](https://ethresear.ch/t/mass-slashable-unavailability-faults/8129/4) also have different claims: deterrence of lazy sampling does not itself guarantee mass slashing after an availability fault. Neither establishes continuous historical serving.

Current PeerDAS assigns deterministic custody and specifies a minimum historical serving range, but it does not create a recurring consensus proof that each old object remained retrievable throughout that range.

Earlier Ethereum research on [one-bit and 0.001-bit proofs of custody](https://ethresear.ch/t/a-0-001-bit-proof-of-custody/7409) explored a stronger model: validators commit to data-dependent custody computations and can become slashable when a later secret reveal exposes a slashable data-dependent attestation, making skipped acquisition or computation risky. Those designs targeted earlier sharding architectures and are not directly portable to PeerDAS. They remain important prior art for distinguishing:

- protocol-required serving;
- probabilistically monitored serving;
- cryptoeconomically enforced retention.

The base proposal initially adopts the first level. Challenges, custody bonds, or mass-slashable unavailability faults would be separate enforcement extensions with their own false-positive, correlation, and recovery risks.

### 21.10 Narrow novelty claim

The novelty claim is not that nobody has priced storage duration or separated availability from persistence. Both have extensive precedent.

The contribution claimed here is their composition:

> **Treat Ethereum DA as a service with separately accounted ingress and bounded purchaser-selected serving duration, represented by deterministic state transitions over active retained stock.**

Physical feasibility and pricing remain questions to test. Representation-aware custody investigations and future resource markets extend the proposed service; they are not demonstrated components of the core contribution.

That claim should be updated if closer prior art emerges.

---

[Project overview](../README.md) · [Document map](document-map.md) · [Previous in core argument](11-how-do-hardware-and-da-operator-markets-scale.md) · [Next in core argument](08-what-remains-to-be-proven.md)
