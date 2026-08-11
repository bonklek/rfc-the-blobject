# How does Lean Ethereum change the proposal?

**Status:** Research compatibility note, August 2026

## Short answer

Lean Ethereum does not make variable-retention data availability obsolete. It strengthens the case for defining the service above today's EIP-4844 blob while revealing that a single expiry time may eventually be too narrow.

The emerging direction is not that blobs disappear or that all state becomes interchangeable. It is that more classes of Ethereum data may share sampled, cryptographically committed transport while retaining different access and persistence requirements:

```text
application semantics
        !=
transport representation
        !=
availability lifecycle
```

Lean Data and adjacent proposals increasingly generalize the transport representation. Variable retention parameterizes the lifecycle.

These proposals are at different maturity levels. Lean Ethereum is a long-run personal vision, EIP-8142 is a draft EIP, and the integrated-history and new-state designs are research proposals. They are architectural evidence, not a finalized roadmap bundle.

---

## 1. What changes at the transport layer?

[Lean Ethereum](https://blog.ethereum.org/2025/07/31/lean-ethereum) explicitly describes Lean Data as “blobs 2.0”: post-quantum blobs with granular sizing and a calldata-like developer experience. It does not abolish the separately scalable data layer.

The useful abstraction is therefore not “an EIP-4844 blob with a timer.” It is:

> a lifecycle and enforceable serving requirement over a committed Ethereum data object, independent of its current encoding.

That object might be transported as:

- an EIP-4844 blob;
- a granular Lean Data object;
- an EIP-8142 payload-blob;
- PeerDAS or FullDAS cells;
- a future coded frame or streamed object.

This is consistent with the base proposal's existing requirement that applications not depend on KZG, cell, column, or coding layout details.

---

## 2. What does Block-in-Blobs add?

Draft [EIP-8142: Block-in-Blobs](https://eips.ethereum.org/EIPS/eip-8142) places execution-payload transaction data and block-level access lists into blobs. The motivation is specific: once validators can verify a zkEVM proof without downloading and re-executing the payload, validity no longer implies that the underlying data was made available.

EIP-8142 makes payload-blobs a prefix of the block's blob commitments and otherwise treats them like ordinary blobs for consensus-layer availability and networking. They share blob limits and congestion with type-3 transaction blobs.

This breaks the convenient shorthand “blob data means rollup data.” A common DAS plane may carry at least:

- user or application DA;
- rollup batches;
- protocol-mandated L1 execution history;
- block-level access and update information.

Common transport does not imply common economics. Payload-blobs are protocol-mandated and have no natural per-blob user payer. EIP-8142 treats their inclusion as a protocol cost and leaves explicit protocol-level pricing open. A lifecycle-aware market must therefore distinguish who caused bytes from who funds their physical service.

---

## 3. Why is one expiry time no longer enough?

[Integrated in-protocol distributed history and state storage](https://ethresear.ch/t/integrated-in-protocol-distributed-history-and-state-storage/23522) proposes putting canonical block history into blob-like objects and requiring each client to retain a random sample of every blob it sees.

Its illustrative configuration uses 512-byte samples, roughly a `1/512` share per client, and estimates about 80 GB of annual storage growth per client under aggressive throughput assumptions. Those figures are design examples, not protocol parameters.

The important conceptual change is a permanent sparse-history tail after the ordinary high-confidence availability window:

```text
publication
    |
    v
full-strength availability window
    |
    +-------------------------+
    |                         |
    v                         v
expire entirely       reduced sparse-history tail
    |                         |
    v                         v
external retention    history reconstruction services
```

The general lifecycle can be written as:

```text
L = (T_full, f_tail, T_tail)
```

- `T_full` is the full-strength protocol serving window.
- `f_tail` is the fraction or reduced custody obligation retained afterward.
- `T_tail` is that tail's duration, potentially unbounded for canonical history.

The original lease remains the simplest profile:

```text
L = (T, 0, 0)
```

A permanent sparse tail must not be described as full retrievability forever. It has different reconstruction probability, repair, node-population, and serving assumptions.

### Illustrative profiles

| Data class | Full-strength window | Sparse tail | Likely policy source |
|---|---|---|---|
| Ephemeral application object | short | none | purchaser-selected |
| Rollup batch | security/recovery minimum | optional | protocol bounds plus purchaser choice |
| L1 execution payload | protocol minimum | possibly permanent | protocol-defined |
| Censorship-resistant publication | replication window | optional | purchaser-selected |

The examples show the shape of the design space, not recommended parameter values.

---

## 4. Does this make state another DA lease?

No. [Hyper-scaling state by creating new forms of state](https://ethresear.ch/t/hyper-scaling-state-by-creating-new-forms-of-state/24052) emphasizes a fundamental asymmetry between execution, data, and active state.

Historical data can usually be retrieved asynchronously. Execution-critical active state must support dynamically determined, synchronous reads during block construction. A builder cannot produce a valid block if the necessary current state is unavailable.

The correct implication is:

```text
same transport substrate
        does not imply
same access or lifecycle requirement
```

Temporary and UTXO-like state are sibling ideas because they separate large historical objects from small permanent markers. They still require execution semantics and should not be smuggled into the ordinary DA lease model.

The proposal should distinguish:

1. user and rollup DA, where bounded purchaser-selected retention may apply directly;
2. protocol-mandated L1 data, where the protocol supplies the lifecycle and possibly the payer;
3. temporary execution state, which needs a separate execution-aware design;
4. permanent active state, which remains outside the DA lease abstraction.

---

## 5. What is the stable service abstraction?

The narrow interface remains useful:

```text
DAService(C, B, T)
```

The generalized interface is:

```text
DataService(C, B, L, A)
```

where:

- `C` is the commitment;
- `B` is the logical size;
- `L` is the lifecycle profile;
- `A` is the protocol-recognized access or data class.

This is a conceptual interface, not a proposed wire format.

Application semantics should remain outside consensus. Ethereum need not know whether an object is a message, rollup batch, media file, proof witness, or game event. It needs only enough information to enforce the resource and access obligation.

The lifecycle may be:

- purchaser-selected within protocol bounds;
- inherited from a protocol data class;
- extended by a downstream service after the base obligation ends.

---

## 6. How does lifecycle pricing change?

The base paper separates ingress from protocol-required byte-time. A multi-phase lifecycle adds a third physical obligation:

```text
F_data
=
F_ingress(B)
+
F_full(B, T_full)
+
F_tail(B * f_tail, T_tail)
```

This is bookkeeping, not a finished fee mechanism. In particular:

- an unbounded tail cannot be naively sold as one prepaid infinite lease;
- a universal sparse-history obligation may be protocol-funded rather than purchaser-funded;
- a recurring service mechanism may fit replacement, migration, repair, and sync serving better than a one-time fee;
- scarcity fees do not automatically compensate individual custodians.

If only a fraction enters long-lived history, its first-order growth is:

```text
G_history ~= f_tail * R
```

where `R` is the admitted data rate. This can separate near-term DA throughput from per-node permanent-history growth, but only if the custodian population and reconstruction assumptions remain credible.

Block-in-Blobs adds a payer question. User DA has an obvious transaction payer; protocol-mandated payload data may need an execution-fee allocation or another protocol accounting channel. The mechanism must avoid double charging and cross-resource subsidies.

---

## 7. How do the research directions map to this RFC?

| Research direction | What changes | Effect on variable retention |
|---|---|---|
| Lean Data / “blobs 2.0” | Granular, post-quantum data objects | Strengthens transport neutrality |
| Block-in-Blobs | L1 payload data enters DAS | Adds protocol-defined data classes and payer questions |
| Integrated distributed history | Random long-lived samples | Generalizes expiry into lifecycle profiles |
| Mandatory zkEVM verification | Payload validity no longer implies payload download | Makes an explicit availability and serving requirement more important |
| Temporary or UTXO-like state | New execution-aware persistence classes | Conceptually adjacent but outside ordinary DA leases |
| Extremely Lean Chain | More responsibility and proofs move to participants | Reinforces minimization, but is not itself a DA mechanism |
| Specialized state/history serving | Fewer universal storage duties | Raises resilience, incentives, and retrieval-privacy questions |

---

## 8. What changes in the base proposal?

The base proposal needs five bounded revisions:

1. **Broaden the object, not the title.** Keep “Variable-Retention Data Availability for Ethereum,” but define it over committed Ethereum data rather than today's user-facing blob format.
2. **Preserve the simple mechanism.** `T` remains the conservative first deployment and the `L=(T,0,0)` special case.
3. **Acknowledge inherited lifecycles.** Not every duration is purchaser-selected; canonical L1 data may have protocol-defined near-term and history obligations.
4. **Keep semantic boundaries explicit.** Common DAS transport does not turn active state into ordinary expiring DA.
5. **Treat sparse history as a different service class.** Reduced permanent sampling has different capacity, repair, incentive, and security assumptions from full retention.

These revisions strengthen the paper without making the narrow spot-start mechanism depend on Lean Ethereum, EIP-8142, or permanent distributed history.

---

## 9. What new questions must be answered?

### Representation

- What is the minimum independently committed object under granular Lean Data?
- Can lifecycle metadata attach to a byte range or cell group without coupling unrelated expiries?
- How does it survive a move from KZG to hash-based post-quantum commitments?

### Protocol data

- Should payload-blobs receive the same full-strength window as user blobs?
- Which L1 data belongs in a permanent sparse tail?
- How is protocol-mandated data prioritized during user-DA congestion?
- Who funds its physical service?

### Sparse history

- Is permanent sampling appropriate for canonical L1 history only, or for other classes?
- What node count, overlap, churn, and repair policy keeps reconstruction credible?
- How is historical serving discovered and incentivized?
- How does the protocol distinguish a statistical history tail from a full required-serving service?

### State and retrieval

- Which expired temporary-state objects can reuse the history-serving network?
- Who provides state snapshots and reconstruction data without creating a centralized dependency?
- How are user access patterns protected when retrieval moves to specialized services?

---

## Primary sources

- Justin Drake, [lean Ethereum](https://blog.ethereum.org/2025/07/31/lean-ethereum), July 31, 2025.
- [EIP-8142: Block-in-Blobs](https://eips.ethereum.org/EIPS/eip-8142), draft Core EIP, created January 29, 2026.
- Vitalik Buterin, [Integrated in-protocol distributed history and state storage](https://ethresear.ch/t/integrated-in-protocol-distributed-history-and-state-storage/23522), November 24, 2025.
- Vitalik Buterin, [Hyper-scaling state by creating new forms of state](https://ethresear.ch/t/hyper-scaling-state-by-creating-new-forms-of-state/24052), February 5, 2026.
- Vitalik Buterin, [The Extremely Lean Chain](https://ethresear.ch/t/the-extremely-lean-chain/25369/1), July 6, 2026.
- Wei Han Ng, Carlos Pérez, and the Stateless Consensus team, [The Future of Ethereum's State](https://blog.ethereum.org/2025/12/16/future-of-state), December 16, 2025.
- [EIP-7928: Block-Level Access Lists](https://eips.ethereum.org/EIPS/eip-7928).
- Ali Atiia and Keewoo Lee, [Sharded PIR Design for the Ethereum State](https://ethresear.ch/t/sharded-pir-design-for-the-ethereum-state/24552), March 30, 2026.
