# Pinned research references

Ethereum specifications and research posts evolve. This file records the versions used for the August 11, 2026 RFC revision. The prose links to canonical pages for readability; protocol claims should be checked against these pins.

## Specifications

| Source | Version used | Relevance |
|---|---|---|
| [EIP-7594: PeerDAS](https://github.com/ethereum/EIPs/blob/eda011bdbfa08f9002df103c8143937a643c677a/EIPS/eip-7594.md) | `eda011b` — 2026-02-03 | Deterministic custody, 1D cells, publication-time sampling |
| [EIP-8136: Cell-Level Deltas](https://github.com/ethereum/EIPs/blob/49beda901dcf3747ed4b91f853a333595fb2cbc4/EIPS/eip-8136.md) | `49beda9` — 2026-02-28 | Backwards-compatible missing-cell transport |
| [EIP-8256: Blob Streaming](https://github.com/ethereum/EIPs/blob/bdc1d099649eefb8790b76f912e25487757f5f4e/EIPS/eip-8256.md) | `bdc1d09` — 2026-06-11 | AOT/JIT capacity and `JIT_RESERVED` comparison |
| [EIP-8142: Block-in-Blobs](https://github.com/ethereum/EIPs/blob/750d967cd231dc69c3ad018886a5b30e834257b2/EIPS/eip-8142.md) | `750d967` — 2026-06-30 | Protocol-mandated payload blobs and fee-accounting questions |
| [Fulu P2P interface](https://github.com/ethereum/consensus-specs/blob/5366cb59eb39e4ec1d6c468a79cceb626c14c048/specs/fulu/p2p-interface.md) | `5366cb5` — 2026-08-05 | Minimum data-column serving range and request semantics |
| [Mainnet configuration](https://github.com/ethereum/consensus-specs/blob/3cbd26f048237250e3373d4d0a651a647b4c58e1/configs/mainnet.yaml) | `3cbd26f` — 2026-08-03 | `MIN_EPOCHS_FOR_DATA_COLUMN_SIDECARS_REQUESTS = 4096` |

## Research posts

These sources do not expose immutable revisions in the same way as Git commits. They were accessed on August 11, 2026.

- [Revisiting Secure DAS in One and Two Dimensions](https://ethresear.ch/t/revisiting-secure-das-in-one-and-two-dimensions/22762) — partial reconstruction and 1D/2D tradeoffs.
- [A 0.001 bit proof of custody](https://ethresear.ch/t/a-0-001-bit-proof-of-custody/7409) — historical custody-proof and slashing design.
- [FullDAS](https://ethresear.ch/t/fulldas-towards-massive-scalability-with-32mb-blocks-and-beyond/19529) and [FullDASv2](https://ethresear.ch/t/accelerating-blob-scaling-with-fulldasv2-with-getblobs-mempool-encoding-and-possibly-rlc/22477) — candidate 2D architectures, not settled protocol direction.
- [Cell-level dissemination](https://ethresear.ch/t/gossipsubs-partial-messages-extension-and-cell-level-dissemination/23017) — independently transmissible cells.
- [Integrated in-protocol distributed history and state storage](https://ethresear.ch/t/integrated-in-protocol-distributed-history-and-state-storage/23522) — permanent sparse-history samples.
- [Hyper-scaling state by creating new forms of state](https://ethresear.ch/t/hyper-scaling-state-by-creating-new-forms-of-state/24052) — temporary and UTXO-like state classes.
- [The Extremely Lean Chain](https://ethresear.ch/t/the-extremely-lean-chain/25369/1) — proof-backed responsibility separation in consensus state.

## Project provenance

- [Original variable-retention gist](https://gist.github.com/bonklek/2eb406003118bd1e29476e54cc18a0c7).
- Repository revision history records the subsequent question-oriented decomposition and adversarial edits.
