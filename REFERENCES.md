# Pinned research references

Ethereum specifications and research posts evolve. This file records the versions used for the August 11, 2026 RFC revision. The prose links to canonical pages for readability; protocol claims should be checked against these pins.

## Specifications

| Source | Version used | Relevance |
|---|---|---|
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

## Project provenance

- [Original variable-retention gist](https://gist.github.com/bonklek/2eb406003118bd1e29476e54cc18a0c7).
- [Radio Free Ethereum](https://github.com/bonklek/eth-radio) and [BlobMail](https://github.com/bonklek/blobmail) — experimental public-media and encrypted-message application evidence.
- Repository revision history records the subsequent question-oriented decomposition and adversarial edits.
