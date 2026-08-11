# Appendix: What are the backbone-scale limits?

This appendix tests the network side of high-throughput DA with round numbers. The calculations expose orders of magnitude; they are not proposed Ethereum parameters.

The storage frontier:

```text
R ≈ S / T
```

is necessary but incomplete. No choice of `T` changes the fact that each admitted byte must cross enough independent network and custody paths to establish availability.

---

## B.1 Per-node bandwidth

Let:

- `R` be the global logical ingress rate;
- `e` be network expansion from erasure coding;
- `q` be the effective delivery/replication multiplier across independent custody paths;
- `f` be the fraction of expanded traffic received by one node;
- `b_local` be that node's sustained inbound DA bandwidth.

A first-order local requirement is:

```text
b_local ≳ f · e · q · R.
```

The factors are deliberately separated. Coding can add bytes even before the network sends the same duty to several operators. Repair, gossip duplication, control messages, proofs, retransmission, and burst headroom sit above this lower bound.

For an illustrative `e·q=2` and `f=1/32`:

| Global logical ingress `R` | Approximate local ingress |
|---:|---:|
| 100 MiB/s | 6.25 MiB/s |
| 1 GiB/s | 64 MiB/s |
| 1 TiB/s | 64 GiB/s |

The first two rows may fit increasingly demanding consumer or prosumer systems. The third does not resemble ordinary home-node participation. Short retention would reduce resident storage at every row while leaving these live bandwidth figures unchanged.

PeerDAS itself anticipates reducing the local sample fraction as throughput rises: [EIP-7594](https://eips.ethereum.org/EIPS/eip-7594) describes a current `1/8` local fraction with possible future reductions to `1/16` or `1/32`. The broader principle is unavoidable:

> **If the per-node bandwidth envelope remains fixed while global throughput rises, the fraction assigned to each ordinary node must fall.**

At a local budget `b_max`, the fraction must satisfy approximately:

```text
f ≤ b_max / (e · q · R).
```

For `b_max=100 MiB/s`, `e·q=2`, and `R=1 TiB/s`, this gives:

```text
f ≤ 1 / 20,972.
```

That is no longer a minor parameter adjustment. It demands a much larger effective operator population, a different backbone class, substantially different security analysis, or some combination of the three.

---

## B.2 Aggregate conservation

Distributing work does not make aggregate traffic disappear.

Let:

- `N` be the number of contributing nodes;
- `b` be the sustainable DA bandwidth per node allocated to this duty.

Ignoring topology and duplicate transit, aggregate receive capacity must satisfy at least:

```text
N · b ≳ e · q · R.
```

Equivalently:

```text
N ≳ (e · q · R) / b.
```

This is a conservation bound, not a security proof. It assumes perfectly balanced assignment and counts only receiver capacity. Real dissemination also consumes sender uplink, intermediate forwarding, repair, request serving, and burst margin.

### Ten-thousand-node thought experiment

Suppose `N=10,000` and `e·q=4`.

| Logical ingress | Aggregate expanded delivery | Perfectly balanced average per node |
|---:|---:|---:|
| 100 MiB/s | 400 MiB/s | ~41 KiB/s |
| 1 GiB/s | 4 GiB/s | ~0.42 MiB/s |
| 1 TiB/s | 4 TiB/s | ~419 MiB/s |

The averages hide custody concentration and topology, but the regime change is visible. A terabyte per second consumes hundreds of megabytes per second at every one of 10,000 perfectly balanced recipients before ordinary overhead. A smaller qualified population would require multi-gigabit service from each participant.

Conversely, if nodes can sustainably devote only `100 MiB/s`, the same `R=1 TiB/s`, `e·q=4` workload needs at least approximately:

```text
N ≥ 41,944
```

perfectly utilized receiver-equivalents. Geographic diversity, correlated hosting, sender capacity, and security replication can only raise the practical requirement.

The calculation separates two regimes:

- **gigabytes per second** may be architecturally conceivable with shrinking custody fractions, pre-propagation, large frames, and a broad operator set;
- **terabytes per second** changes the nature and likely the composition of the participating infrastructure.

That conclusion is not a claim that one rate is safe and the other impossible. It says they should not be discussed as points on the same smooth parameter curve.

---

## B.3 Object-count explosion

The present EIP-4844 object is 128 KiB at the protocol-accounting level. If future throughput were represented only by multiplying that object count, then at `R=1 GiB/s` and 12-second slots:

```text
objects per second
=
1 GiB/s / 128 KiB
=
8,192

objects per slot
=
8,192 · 12
=
98,304.
```

At `1 TiB/s`, the same abstraction would require:

```text
8,388,608 objects/s
100,663,296 objects/slot.
```

These are arithmetic extrapolations, not proposed block limits. They omit transaction packaging, commitments, manifests, indices, gossip metadata, and inclusion overhead—the very costs that make the extrapolation unattractive.

### Cell-proof count

Current PeerDAS extends each blob into 128 cells: 8,192 extended field elements divided into 64 field elements per cell under the pinned [Fulu polynomial-commitment specification](https://github.com/ethereum/consensus-specs/blob/9d377fd53d029536e57cfda1a4d2c700c59f86bf/specs/fulu/polynomial-commitments-sampling.md). EIP-7594 requires one cell proof for every extended cell, while permitting batch verification.

If every 128 KiB object at `1 GiB/s` retained this proof granularity, the raw production rate would be:

```text
8,192 blobs/s · 128 cell proofs/blob
=
1,048,576 cell proofs/s.
```

At `1 TiB/s`, it would exceed one billion cell proofs per second.

Batch verification helps verification cost; it does not eliminate proof generation, transport, indexing, memory, or scheduling. Future constructions may change the cell count, proof system, aggregation, or commitment scheme entirely. The calculation is evidence against preserving today's smallest object and per-object control surface unchanged at backbone scale.

---

## B.4 Why large continuous frames follow

The arithmetic motivates a different transport shape:

```text
many small application objects
        |
        v
large ahead-of-time coded frame
        |
        +-- compact manifest of selected logical objects
        +-- batched commitments and proofs
        +-- fine distributed custody below the frame boundary
        +-- continuous or pipelined propagation
```

Applications can retain small logical messages. The network need not represent each message as an independent transaction, gossip topic, proof batch, and retention record.

A backbone-scale design likely needs:

- multiplexed field-element or cell ranges;
- compact manifests and aggregate authentication;
- AOT propagation outside the slot critical path;
- pipelined encoding and proof work;
- cell-level custody and repair;
- common frames large enough to amortize scheduling metadata;
- logical expiry below a physical frame boundary or a hot-to-cold transition;
- congestion and service accounting that does not require one auction per cell.

The AOT-plus-distributed-FullDAS path in §17.9 is one candidate. It is attractive because pre-dispersed holders can supply selected cells directly to column networks while the builder selects only the manifest.

---

## B.5 Storage, writes, and networking must close simultaneously

Three first-order constraints now sit together:

```text
resident stock:
S_local ≈ f_storage · rho · R · T

local writes:
W_local ≈ alpha · f_write · rho · R

local network:
b_local ≳ f_network · e · q · R.
```

The fractions need not be identical. A protocol may use different hot dissemination, cold custody, repair, and sampling populations. That flexibility creates handoff and incentive questions rather than removing the conservation laws.

A proposed throughput is credible only if all of the following close under one consistent operator model:

1. enough sender and receiver bandwidth exists;
2. the assignment fraction produces the desired DAS security;
3. hot writes fit the endurance envelope;
4. retained stock and repair fit the capacity envelope;
5. proof and metadata rates fit the compute and memory envelope;
6. no mandatory participant becomes the synchronous full-frame uplink.

Reducing `T` solves only part of item 4.

---

## B.6 What should be measured

The next useful artifact is a topology-aware simulator or trace replay rather than a larger headline throughput number. It should report:

- logical and expanded bytes per second;
- unique sender uplink and receiver downlink distributions;
- duplicate gossip and retransmission factors;
- proof generation and batch-verification rates;
- per-node assignment, sampling, repair, and historical-serving traffic;
- burst behavior within and across slots;
- the smallest operator population consistent with the target fraction;
- concentration by administrative, hosting, network, geographic, and client domain;
- degradation under correlated node loss and withheld AOT rows.

The decisive question is not “can a datacenter ingest this rate?” It is:

> **Can the chosen population establish and maintain the claimed availability semantics without concentrating the mandatory full data path?**

Until that question is answered, gigabyte- and terabyte-scale examples should remain stress tests rather than roadmap targets.
