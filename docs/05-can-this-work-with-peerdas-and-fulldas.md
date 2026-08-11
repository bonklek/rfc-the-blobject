# Can this work with PeerDAS and FullDAS?

## 17. FullDAS, distributed-storage leverage, and heterogeneous expiry

Future DAS improvements can move the throughput-retention frontier outward. If FullDAS or successors increase the ratio

```text
(logical protected data) / (local physical storage),
```

then the effective retained-stock envelope `K_safe` can increase. Conversely, increasing ingress without increasing distributed-storage leverage shortens the retention horizon that can be supplied universally.

This complementarity is straightforward. The physical compatibility question is not.

The important adversarial finding is that **heterogeneous expiry creates representation-dependent problems**. Variable retention does not depend on two-dimensional FullDAS becoming Ethereum's chosen path.

```text
Current 1D PeerDAS
    |
    +-- 1D + cell-level transport
    |      -> sparse per-row/cell historical custody
    |      -> no cross-row parity to preserve
    |
    +-- possible future 2D DAS
           -> cross-row parity coupling
           -> hot-2D / cold-1D transition hypothesis
           -> OR maturity-aligned coding domains
```

The 1D branch is the first implementation target. The 2D branch is a compatibility investigation, not the assumed Ethereum roadmap.

### 17.1 Problem A: PeerDAS column packaging

In PeerDAS, each blob is horizontally erasure-coded into cells, while a column collects the same cell index across all blob rows in the block. Current Fulu request/response semantics serve `DataColumnSidecar` objects by block and column.

Schematically:

```text
                column j
Blob A             A_j
Blob B             B_j
Blob C             C_j
Blob D             D_j
```

Suppose A requests 8 epochs—about 51.2 minutes—while B and D request the full 4,096-epoch horizon—about 18.2 days. After A expires, the desired historical state is effectively:

```text
column j:
    [expired A_j]
    B_j
    C_j
    D_j
```

The present whole-column serving abstraction is awkward for this sparse state. Retaining the original complete sidecar until the longest constituent expiry gives short-lived objects the physical lifetime of their longest-lived neighbor. Sparse or cell-level historical serving can plausibly remove this **packaging** coupling.

Draft [EIP-8136](https://eips.ethereum.org/EIPS/eip-8136) is important evidence for this branch. It lets PeerDAS peers exchange missing cells rather than retransmitting complete columns and is designed as a backwards-compatible networking optimization. It does **not** specify sparse historical storage or heterogeneous expiry, but it establishes that independently transmissible cells are already an active protocol direction.

The current [1D-versus-2D DAS analysis](https://ethresear.ch/t/revisiting-secure-das-in-one-and-two-dimensions/22762) also shows that 1D PeerDAS can support partial row reconstruction when paired with cell-level messaging and row-oriented reconstruction flows. That design has practical and security tradeoffs, but it keeps 1D with smaller cells as a viable path rather than a temporary stop on an inevitable move to 2D.

This problem is serious for an implementation built directly on current sidecars, but it does not by itself require changing the blob's row-local encoding.

### 17.2 Problem B: FullDAS cross-row coding

Proposed FullDAS designs go further. Blobs remain row-like objects, but a second erasure-code dimension can be applied vertically across rows to create additional redundancy and permit availability amplification, row/column repair, and cell-level pipelining.

A simplified picture is:

```text
                 horizontal encoding →

Blob A      A0 A1 A2 A3 | A4 A5 A6 A7
Blob B      B0 B1 B2 B3 | B4 B5 B6 B7
Blob C      C0 C1 C2 C3 | C4 C5 C6 C7
Blob D      D0 D1 D2 D3 | D4 D5 D6 D7
            --------------------------------
2D parity   P0 P1 P2 P3 | P4 P5 P6 P7
            Q0 Q1 Q2 Q3 | Q4 Q5 Q6 Q7
            ...
```

The lower rows are schematic: the important property is that second-dimensional coded cells can depend on cells from **multiple logical blob rows**.

This creates a deeper coupling than whole-column packaging. If A expires while B, C, and D remain live, deleting A's row does not necessarily free all coded information that mathematically depended on A. Recomputing the vertical parity without A would create a new codeword and can require new commitments, proofs, indexing, custody assignments, or transition rules.

Cell-level networking alone therefore does not solve this problem.

The critical question is:

> **Must the cross-object coding structure used for fresh availability amplification persist for the whole serving horizon?**

If yes, fine-grained physical expiry becomes difficult. If no, there is a cleaner design family.

### 17.3 The 2D compatibility branch: hot dense DAS → cold sparse row-local custody

If Ethereum adopts a cross-row 2D code, one candidate is a two-phase lifecycle. This section is deliberately conditional on that representation.

#### Phase 1 — row-local preparation

Each logical blob retains an independent commitment and an independently reconstructable horizontal encoding before any cross-row FullDAS coding is applied.

```text
Blob A -> commitment C_A -> horizontally encoded row A
Blob B -> commitment C_B -> horizontally encoded row B
Blob C -> commitment C_C -> horizontally encoded row C
```

The key condition is that the row-local representation can later authenticate and reconstruct its blob without depending permanently on second-dimensional parity.

#### Phase 2 — hot FullDAS composition and availability establishment

Many rows are assembled into the richer DAS object. The protocol adds whatever second-dimensional redundancy, cross-forwarding, sampling, and rapid repair the live FullDAS design requires.

All objects participate normally during this phase regardless of their eventual retention duration. No object may expire before the common hot phase ends.

Let the end of this phase be `T_hot_end`, or its duration be summarized as `T_hot`.

#### Candidate transition events

`T_hot` is a kill parameter, not a placeholder to be resolved later. At least three transition designs should be prototyped:

| Candidate | Transition condition | Benefit | Primary risk |
|---|---|---|---|
| A. Local acceptance plus fixed delay | A node completes its ordinary DA checks, then waits a protocol-fixed safety interval | Earliest transition; preserves very short-lived applications | Different nodes may transition with incomplete common knowledge; unsafe if late repair still depends on 2D redundancy |
| B. Network availability signal | A committee, aggregate, or protocol-recognized signal confirms the hot phase is complete | Shared transition point without necessarily waiting for finality | Introduces new signaling, withholding, and fork-choice interactions |
| C. Finality | The containing block finalizes | Simple, globally recognizable boundary | Makes `T_hot` long enough to weaken 1–8-epoch use cases (~6.4–51.2 minutes) and increases hot working storage |

Candidate A is useful only if local transition disagreement cannot weaken fresh DA. Candidate B must define who signals and what the signal proves. Candidate C is the conservative fallback, not an assumption. The models therefore accept `T_hot` as an explicit input rather than hiding it inside total retention.

#### Phase 3 — hot-to-cold transition

At a protocol-recognizable point where the richer availability-amplification representation is no longer required for **fresh** DA security, the system transitions:

```text
dense availability-establishment representation
                    |
                    v
          fresh DA established
                    |
                    v
     drop 2D-only shared redundancy
                    |
                    v
   retain independently committed row cells
```

The attractive property is what **does not** happen:

- the surviving logical blob does not change;
- its original commitment does not change;
- neighboring live blobs do not need to be re-encoded merely because another blob expires;
- the cold representation can become sparse as individual leases end.

For current PeerDAS, there is no equivalent second-dimensional parity to discard; the analogous transition would principally replace dense whole-column historical serving with a sparse cell-oriented interface.

#### Phase 4 — cold duration-specific custody

Cold custody remains distributed. It does **not** imply that one node stores an entire blob.

A custody group can hold row-local cells from many live blobs:

```text
Custody group 0:
    A0
    B0
    C0
    D0

Custody group 1:
    A1
    B1
    C1
    D1
```

When A expires:

```text
Custody group 0:
    [delete A0]
    B0
    C0
    D0
```

No live blob is re-encoded and no surviving commitment changes.

A client retrieving C later requests enough independently verifiable cells from C's row, reconstructs C, and verifies the result against `C_C`.

This is the intended graceful-expiry property.

### 17.4 Cold custody is a formal security problem

Dropping second-dimensional redundancy gives up some of the machinery that makes fresh FullDAS attractive.

During the hot phase, missing data can benefit from rapid local row/column repair and availability amplification. During cold retention, a missing cell may instead require:

1. collecting enough surviving cells from the same blob row;
2. reconstructing the row or blob;
3. regenerating the missing cell;
4. regenerating or validating whatever proof the eventual design requires;
5. handing the repaired cell to a replacement custodian.

That can be slower and more bandwidth-intensive.

The proposal relies on a latency asymmetry:

> **fresh availability must be established in seconds; historical repair for an object with tens to thousands of epochs remaining may tolerate multiple slots or even an epoch.**

This turns retention into a security problem distinct from initial DAS.

```text
HOT QUESTION:
Was the freshly proposed data made available quickly enough
for safe block/payload acceptance?

COLD QUESTION:
Has this particular still-live object remained reconstructable
through its protocol-required serving horizon?
```

The cold layer therefore needs its own survivability requirement. Let:

- `m` be the number of horizontal cells in the cold row;
- `k` be the number required for reconstruction;
- `n` be the eligible custodian population;
- `c` be the independent replicas assigned per cell;
- `q` be the per-custodian offline or adversarial probability within one repair interval;
- `Δ_repair` be the repair cadence in epochs;
- `T` be the remaining required-serving duration in epochs;
- `p_max` be the maximum tolerated lease-failure probability.

The protocol target is:

```text
P[row remains reconstructable at every checkpoint through T]
>=
1 - p_max.
```

Under a deliberately simple independent-failure model, one cell is lost within an interval with probability `q^c`. The probability that at least `k` of `m` cells survive that interval is:

```text
P_row
=
Σ[j=k..m] choose(m,j) · (1-q^c)^j · (q^c)^(m-j).
```

With repair restoring the target multiplicity every `Δ_repair`, a conservative checkpoint approximation over `N=ceil(T/Δ_repair)` intervals is:

```text
P_lease ≈ P_row^N.
```

In this null model, `n` constrains assignment feasibility only through `c≤n`; independence makes the remaining expression insensitive to the size of the unused population. That simplification is itself a warning. A real design must derive assignment overlap and adversarial concentration from `n` rather than treating replicas as automatically independent.

This is a null model, not a security proof. Real failures are correlated; an adaptive adversary may target custody assignments; repair itself can fail or leak assignments; and “online” is not identical to “will serve.” A deployable model must replace `q` with explicit honest, offline, adversarial, and network-partition processes and must account for handoff overlap.

Candidate mechanisms include replication, multi-custodian assignment, randomized service challenges, health estimation, reconstruct-and-repair, custody reassignment, and overlap during handoff. Level-2 monitoring or level-3 penalties from §2.2 can strengthen compliance but do not replace the reconstruction calculation.

[The cold-custody model](../models/cold_custody.py) evaluates this null model and reports whether a parameter set meets `p_max`.

### 17.5 Physical and hardware consequences

The hot/cold split creates two naturally different workloads.

**Hot availability tier**

- sustained write bandwidth;
- high network throughput;
- coding and proof work;
- rapid repair;
- low latency;
- potentially high-endurance or memory-heavy working storage.

**Cold retention tier**

- storage capacity;
- historical serving;
- expiry indexing;
- lower-rate reconstruct-and-repair;
- custody handoff;
- potentially cheaper capacity-oriented storage.

This is why the physical capacity derivation in §6 separates `γ_hot` from `γ_cold`. Even if short-lived traffic creates little long-run resident stock, it can still impose extreme **write churn** and hot-path bandwidth. Variable retention does not make that burden disappear.

The same operator population could provide both tiers, or a future protocol could permit a custody handoff between differently provisioned participants. The latter would require additional authorization, incentive, and failure semantics and should not be assumed by the base proposal.

### 17.6 Five conditions for the hot/cold design

The paper should treat this design as a falsifiable compatibility hypothesis, not as a solved construction.

**Condition 1 — row-local reconstructability survives independently.**

Each logical blob must retain an independently committed horizontal representation sufficient to reconstruct the blob without the shared second dimension.

**Condition 2 — second-dimensional parity is transient.**

The FullDAS security model must not require the original dense cross-row codeword to remain available for the full historical serving horizon.

**Condition 3 — a clean transition point exists.**

There must be a protocol-recognizable event after which dropping hot-only redundancy does not weaken fork choice or fresh DA security. Ordinary Ethereum finality should not be assumed unless the actual design requires it; waiting for finality could make very short leases substantially less useful.

**Condition 4 — cold row repair is affordable.**

At realistic churn and failure rates, reconstruction and repair from surviving row-local cells must not consume enough bandwidth or compute to erase the storage benefit.

**Condition 5 — sparse historical serving is practical.**

The networking and proof interfaces must permit still-live cells to be requested and verified after neighboring logical objects expire without recreating obsolete dense sidecars.

These reduce to three principal kill questions, tracked as repository issues:

> **[A](https://github.com/bonklek/rfc-the-blobject/issues/2). Does FullDAS require the second-dimensional coded representation for the entire serving horizon, or mainly for fresh dispersal, sampling, and availability amplification?**

> **[B](https://github.com/bonklek/rfc-the-blobject/issues/3). Can the independently committed horizontal row remain a sufficient authenticated reconstruction object after that second dimension is discarded?**

> **[C](https://github.com/bonklek/rfc-the-blobject/issues/4). Is row-local cold repair cheap and robust enough to maintain long leases without keeping the richer 2D code alive?**

A negative answer to A or B would severely weaken this design family. A negative answer to C may still permit short or medium retention but undermine long cold leases.

### 17.7 Fallback: maturity-aware coding domains

If the hot-to-cold transition fails, the strongest fallback is to avoid mixing radically different maturities inside a persistent coded object.

Objects can be grouped into separate coding domains:

```text
frame A -> 1–8 epochs (~6.4–51.2 minutes)
frame B -> 16–64 epochs (~1.71–6.83 hours)
frame C -> 256–2,048 epochs (~1.14–9.10 days)
frame D -> 4,096 epochs (~18.20 days; full horizon)
```

This lets an entire physical codeword expire coherently. It also reintroduces discrete classes, packing fragmentation, and lane-allocation problems.

The tradeoff is therefore sharp:

- **Hot/cold lifecycle:** one large heterogeneous hot DAS domain, continuous logical leases, sparse cold expiry, but a new cold repair/security mechanism.
- **Maturity-aware domains:** simpler physical expiry and preservation of the dense codeword, but discrete classes and fragmented capacity.

### 17.8 The operational-dominance test and deployment order

The weak-dominance result in §3 remains necessary but insufficient. Let `G` be the logical byte-time saved by shorter leases and `O` the physical overhead introduced by sparse serving, metadata, proof handling, repair, and transition machinery. Variable retention is operationally beneficial only when realized physical savings exceed `O`.

The revised deployment order is therefore:

1. preserve a general duration-oriented **service abstraction**;
2. prototype 1D cell-level historical serving against present PeerDAS to isolate the packaging problem;
3. measure row-local cold repair under realistic custody churn;
4. only if a concrete 2D design is pursued, prototype each `T_hot` transition candidate and the hot-2D/cold-1D transition;
5. if any representation-specific kill question fails, fall back to maturity-aligned coding domains;
6. only then decide whether continuous expiry or a small number of physical maturities is justified.

The implementation dependency is now explicit:

> **Application retention semantics should not be forced to equal the lifetime of the physical representation optimized for fresh DAS—but the protocol must prove that those two lifetimes can actually be separated.**

---
