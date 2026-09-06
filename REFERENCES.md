# Pinned research references

Ethereum specifications and research posts evolve. This file records the versions used for the August 11, 2026 RFC revision. The prose links to canonical pages for readability; protocol claims should be checked against these pins.

For the relationship between sources, read the [source-to-design map](docs/07-what-is-the-prior-art-and-novelty.md#210-source-to-design-map). It identifies the EIPs, ethresear.ch discussions, and Ethereum Magicians venues behind each combination, separates base mechanisms from extensions, and records which findings came through Wikipethia. The [README summary](README.md#which-existing-ideas-this-brings-together) provides a shorter entry point.

## September 6, 2026 verification notes

The August pins below remain the research baseline. The [source-audit ledger](audits/facts-review.md) records a later targeted primary-source check, its coverage, and unresolved verification limits. It is not an exhaustive source or novelty certification.

- The 4,096-epoch constant is supported, but the [pinned Fulu request range](https://github.com/ethereum/consensus-specs/blob/5366cb59eb39e4ec1d6c468a79cceb626c14c048/specs/fulu/p2p-interface.md#datacolumnsidecarsbyrange-v1) is epoch-inclusive. Exact equivalence to elapsed-duration expiry remains a deployment gate.
- [EIP-8136](https://eips.ethereum.org/EIPS/eip-8136) is now **Review**, versus Draft at the February pin. It still does not specify heterogeneous historical expiry. The source-map follow-up also checked **Review** status for [EIP-8070](https://eips.ethereum.org/EIPS/eip-8070) and the EIPs'/ERCs' declared Magicians discussion links. The checked EIP-8256 and EIP-8142 descriptions remain proposal evidence, not deployed-feature claims.
- [OP fault proofs](https://docs.optimism.io/op-stack/fault-proofs/explainer) and the [BoLD technical description](https://docs.arbitrum.io/how-arbitrum-works/bold/bold-technical-deep-dive) support the quoted challenge-period examples. [BoLD's overview](https://docs.arbitrum.io/how-arbitrum-works/bold/gentle-introduction) distinguishes worst-case resolution. These durations alone do not establish a safe native retention window.
- The [Filecoin storage-market specification](https://spec.filecoin.io/systems/filecoin_markets/storage_market/) supplies direct start/end-duration evidence; the older storage-proving URL was unavailable to the source reviewer.
- Prototype descriptions now refer to [poc-blobcast at `8d4924e`](https://github.com/bonklek/poc-blobcast/blob/8d4924edaf7ecad2ddaccb2bd52df08ff24284e3/README.md) and [poc-blobmail at `939b1d8`](https://github.com/bonklek/poc-blobmail/blob/939b1d8a5dc2f9ca230a2a7e9d301923033d877b/README.md). BlobMail's documented Sepolia MVP supersedes the August local-only description. Repository inspection does not verify live acceptance, demand, or production security.
- The pinned EthStorage guide recommends NVMe rather than requiring it. Historical custody-bomb research proves slashable signature conditions rather than a participant's past non-possession. Waku/Swarm privacy and retention comparisons were checked within the narrow scope stated in the source ledger.

## Specifications

| Source | Version used | Relevance |
|---|---|---|
| [EIP-8371: RowDAS](https://github.com/ethereum/EIPs/blob/169a65510927f58bdafdc67e840d53020e7a91ca/EIPS/eip-8371.md) | `169a655` — added to this RFC's sources on 2026-09-06 | Row reconstruction; explicit separation from future historical retrieval and row custody |
| [EIP-7594: PeerDAS](https://github.com/ethereum/EIPs/blob/eda011bdbfa08f9002df103c8143937a643c677a/EIPS/eip-7594.md) | `eda011b` — 2026-02-03 | Deterministic custody, 1D cells, publication-time sampling |
| [EIP-8136: Cell-Level Deltas](https://github.com/ethereum/EIPs/blob/49beda901dcf3747ed4b91f853a333595fb2cbc4/EIPS/eip-8136.md) | `49beda9` — 2026-02-28 | Backwards-compatible missing-cell transport |
| [EIP-8256: Blob Streaming](https://github.com/ethereum/EIPs/blob/bdc1d099649eefb8790b76f912e25487757f5f4e/EIPS/eip-8256.md) | `bdc1d09` — 2026-06-11 | AOT/JIT capacity and `JIT_RESERVED` comparison |
| [EIP-8142: Block-in-Blobs](https://github.com/ethereum/EIPs/blob/750d967cd231dc69c3ad018886a5b30e834257b2/EIPS/eip-8142.md) | `750d967` — 2026-06-30 | Protocol-mandated payload blobs and fee-accounting questions |
| [EIP-8070: Sparse Blobpool](https://github.com/ethereum/EIPs/blob/169a65510927f58bdafdc67e840d53020e7a91ca/EIPS/eip-8070.md) | `169a655` — 2026-08-11 | Custody-aligned sparse blobpool and `getBlobs` retrieval |
| [EIP-7805: FOCIL](https://github.com/ethereum/EIPs/blob/169a65510927f58bdafdc67e840d53020e7a91ca/EIPS/eip-7805.md) | `169a655` — 2026-08-11 | Committee inclusion lists and fork-choice enforcement |
| [EIP-8135: Increase Blob Count](https://github.com/ethereum/EIPs/blob/169a65510927f58bdafdc67e840d53020e7a91ca/EIPS/eip-8135.md) | `169a655` — 2026-08-11 | BPO schedule, including the 14-blob target used as a dated calibration baseline |
| [ERC-8179: Blob Space Segments](https://github.com/ethereum/EIPs/blob/169a65510927f58bdafdc67e840d53020e7a91ca/EIPS/eip-8179.md) | `169a655` — 2026-08-11 | Event-only declarations for application subranges inside blobs |
| [ERC-8180: Blob Authenticated Messaging](https://github.com/ethereum/EIPs/blob/169a65510927f58bdafdc67e840d53020e7a91ca/EIPS/eip-8180.md) | `169a655` — 2026-08-11 | Authenticated non-rollup message batches over blobs |
| [Fulu P2P interface](https://github.com/ethereum/consensus-specs/blob/5366cb59eb39e4ec1d6c468a79cceb626c14c048/specs/fulu/p2p-interface.md) | `5366cb5` — 2026-08-05 | Minimum data-column serving range and request semantics |
| [Fulu polynomial commitments](https://github.com/ethereum/consensus-specs/blob/9d377fd53d029536e57cfda1a4d2c700c59f86bf/specs/fulu/polynomial-commitments-sampling.md) | `9d377fd` — 2025-02-12 | Extended-blob cell and proof-count arithmetic |
| [Mainnet configuration](https://github.com/ethereum/consensus-specs/blob/3cbd26f048237250e3373d4d0a651a647b4c58e1/configs/mainnet.yaml) | `3cbd26f` — 2026-08-03 | `MIN_EPOCHS_FOR_DATA_COLUMN_SIDECARS_REQUESTS = 4096` |

## Research posts

These sources do not expose immutable revisions in the same way as Git commits. They were accessed on August 11, 2026.

- [Revisiting Secure DAS in One and Two Dimensions](https://ethresear.ch/t/revisiting-secure-das-in-one-and-two-dimensions/22762) — partial reconstruction and 1D/2D tradeoffs.
- [A 0.001 bit proof of custody](https://ethresear.ch/t/a-0-001-bit-proof-of-custody/7409) — historical custody-proof and slashing design.
- [Proofs of Custody](https://dankradfeist.de/ethereum/2021/09/30/proofs-of-custody.html) by Dankrad Feist — historical explainer of the “bomb” construction for enforcing acquisition and processing. Its numerical parameters are illustrative, not parameters proposed by this RFC or the current Strawmap.
- [Ethereum L1 Strawmap](https://strawmap.org/) and its [drawing changelog](https://github.com/ethereum/strawmap/issues/6) — evolving roadmap context for renewed proof-of-custody research; placement on the map does not imply a settled construction.
- [FullDAS](https://ethresear.ch/t/fulldas-towards-massive-scalability-with-32mb-blocks-and-beyond/19529) and [FullDASv2](https://ethresear.ch/t/accelerating-blob-scaling-with-fulldasv2-with-getblobs-mempool-encoding-and-possibly-rlc/22477) — candidate 2D architectures, not settled protocol direction.
- [Is Data Available in the EL Mempool?](https://ethresear.ch/t/is-data-available-in-the-el-mempool/22329), [A New Design for DAS and Sharded Blob Mempools](https://ethresear.ch/t/a-new-design-for-das-and-sharded-blob-mempools/22537), and [Blob Notaries](https://ethresear.ch/t/blob-notaries-a-distributed-blob-publishing-design-to-scale-da/22709) — distributed blob acquisition, partial dissemination, and publisher/notary designs that avoid treating one builder as the only synchronous source.
- Julian Ma, [On In-Protocol Gas Futures](https://ethresear.ch/t/on-in-protocol-gas-futures/23698) — protocol-issued, physically settled future blockspace access, building on Vitalik Buterin's gas-futures framing.
- Tamara Tran, [Introducing Ethereum Blobspace Derivatives](https://paragraph.com/@tamaratran/introducing-ethereum-blobspace-derivatives) — cash-settled blob-price derivatives and a physical-delivery research direction.
- Luban/Taiyi, [Luban Unveils Blob Futures](https://paragraph.com/@luban-2/luban-unveils-blob-futures-pre-settle-blobs-on-ethereum) — proposer/underwriter-backed commitments to future blob inclusion and physical settlement.
- [Cell-level dissemination](https://ethresear.ch/t/gossipsubs-partial-messages-extension-and-cell-level-dissemination/23017) — independently transmissible cells.
- [Integrated in-protocol distributed history and state storage](https://ethresear.ch/t/integrated-in-protocol-distributed-history-and-state-storage/23522) — permanent sparse-history samples.
- [Hyper-scaling state by creating new forms of state](https://ethresear.ch/t/hyper-scaling-state-by-creating-new-forms-of-state/24052) — temporary and UTXO-like state classes.
- [The Extremely Lean Chain](https://ethresear.ch/t/the-extremely-lean-chain/25369/1) — proof-backed responsibility separation in consensus state.
- [Waku protocols](https://docs.waku.org/learn/concepts/protocols/) and [content-topic privacy guidance](https://docs.waku.org/learn/concepts/content-topics) — RLN anti-spam and the separation of gossip, request, retrieval, and network privacy.
- [Waku Store configuration](https://docs.waku.org/run-node/config-options) and [Waku FAQ](https://docs.waku.org/learn/faq/) — bounded local message retention with no general guarantee of long-term availability.
- [Swarm postage stamps](https://docs.ethswarm.org/docs/concepts/incentives/postage-stamps/) and [batch purchasing](https://docs.ethswarm.org/docs/develop/tools-and-features/buy-a-stamp-batch/) — prepaid storage value, batch depth, time-dependent depletion, top-ups, and price-sensitive TTL.
- [Codex marketplace specification](https://github.com/logos-storage/logos-storage-spec/blob/f238dd660409ce628f14572991f6c1d8dd71c5d1/specs/marketplace.md) — duration-priced storage requests, provider collateral, and randomized storage-proof requirements during the contract interval.
- EthStorage's [contract deployment template](https://github.com/ethstorage/storage-contracts-v1/blob/513ec70e23a15db828dbd99f03714aada3484ce3/.env.template) (`513ec70` — 2025-08-29) and [storage-provider hardware guide](https://github.com/ethstorage/ethstorage-doc/blob/8ba215431220c1bc8518833a91a5f35c334d513e/storage-provider-guide/tutorials.md) (`8ba2154` — 2026-04-16) — a roughly 512 GiB configured shard and at least 550 GB free storage for one provider shard.
- [Lightning Network paper](https://lightning.network/lightning-network-paper.pdf) — base-layer settlement with high-frequency activity in a specialized network; used only as an architectural analogy.
- [BuilderNet](https://buildernet.org/) and [multi-party block construction](https://ethresear.ch/t/building-towards-multi-party-block-construction/24975) — adjacent distributed and multi-contributor block-building architectures.
- Ethereum Foundation, [Building the decentralized Web 3.0](https://blog.ethereum.org/2014/08/18/building-decentralized-web) and [Swarm alpha public pilot](https://blog.ethereum.org/2016/12/15/swarm-alpha-public-pilot-basics-swarm) — historical Ethereum/Whisper/Swarm composition and the separate `eth`, `shh`, and `bzz` protocol vision.
- [Ethereum networking layer: Whisper](https://ethereum.org/developers/docs/networking-layer/#whisper) and [decentralized storage: Swarm](https://ethereum.org/developers/docs/storage/#swarm) — current documentation of Whisper's deprecation and Swarm as a separate storage system.

## Additional discovery through Wikipethia

The September audit used [Wikipethia](https://github.com/JossDuff/wikipethia) for ten focused hosted-corpus searches and contextual follow-through, then checked consequential original sources. The [query/disposition record](audits/wikipethia-review.md) documents the depth and limits. Discovery through the corpus is not a substitute for specification authority, and a negative search is not a novelty proof.

This pass added RowDAS above, the [2018 custody thread](https://ethresear.ch/t/extending-skin-in-the-game-of-notarization-with-proofs-of-custody/1639/1) and [retained-history reply](https://ethresear.ch/t/extending-skin-in-the-game-of-notarization-with-proofs-of-custody/1639/4), and the [2020 mass-slashing discussion](https://ethresear.ch/t/mass-slashable-unavailability-faults/8129/1). [Variants of Mempool Tickets](https://ethresear.ch/t/variants-of-mempool-tickets/23338/1) is a further terminology comparison: its leases concern propagation permissions, not historical serving of included data.

## Project provenance

- [Radio Free Ethereum](https://github.com/bonklek/eth-radio) and [BlobMail](https://github.com/bonklek/blobmail) — experimental public-media and encrypted-message application evidence.
- Repository revision history records the subsequent question-oriented decomposition and adversarial edits.
