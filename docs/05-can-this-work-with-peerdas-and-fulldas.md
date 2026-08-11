# Can this work with PeerDAS and FullDAS?

## 17. FullDAS, distributed-storage leverage, and heterogeneous expiry

Future DAS improvements can move the throughput-retention frontier outward. If FullDAS or successors increase the ratio

```text
(logical protected data) / (local physical storage),
```

then the effective retained-stock envelope `K_safe` can increase. Conversely, increasing ingress without increasing distributed-storage leverage shortens the retention horizon that can be supplied universally.

This complementarity is straightforward. The physical compatibility question is not.

The important adversarial finding is that **heterogeneous expiry creates two distinct problems**, one already visible in PeerDAS and a deeper one introduced by proposed two-dimensional FullDAS designs.

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

Suppose A requests one hour while B and D request fourteen days. After A expires, the desired historical state is effectively:

```text
column j:
    [expired A_j]
    B_j
    C_j
    D_j
```

The present whole-column serving abstraction is awkward for this sparse state. Retaining the original complete sidecar until the longest constituent expiry gives short-lived objects the physical lifetime of their longest-lived neighbor. Sparse or cell-level historical serving can plausibly remove this **packaging** coupling.

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

### 17.3 Leading compatibility hypothesis: hot dense DAS → cold sparse row-local custody

The current preferred research direction is a two-phase lifecycle.

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

### 17.4 Cold repair is a different security problem

Dropping second-dimensional redundancy gives up some of the machinery that makes fresh FullDAS attractive.

During the hot phase, missing data can benefit from rapid local row/column repair and availability amplification. During cold retention, a missing cell may instead require:

1. collecting enough surviving cells from the same blob row;
2. reconstructing the row or blob;
3. regenerating the missing cell;
4. regenerating or validating whatever proof the eventual design requires;
5. handing the repaired cell to a replacement custodian.

That can be slower and more bandwidth-intensive.

The proposal relies on a latency asymmetry:

> **fresh availability must be established in seconds; historical repair for an object with hours or days remaining may tolerate seconds or minutes.**

This turns retention into a security problem distinct from initial DAS.

```text
HOT QUESTION:
Was the freshly proposed data made available quickly enough
for safe block/payload acceptance?

COLD QUESTION:
Has this particular still-live object remained reconstructable
through its promised serving horizon?
```

The cold layer therefore needs its own survivability policy. Candidate ingredients include replication, multi-custodian assignment, randomized custody or service challenges, health estimation, reconstruct-and-repair, custody reassignment, overlap during handoff, and repair thresholds that depend on remaining lease time.

None is specified here as the final mechanism.

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

These reduce to three principal kill questions:

> **A. Does FullDAS require the second-dimensional coded representation for the entire serving horizon, or mainly for fresh dispersal, sampling, and availability amplification?**

> **B. Can the independently committed horizontal row remain a sufficient authenticated reconstruction object after that second dimension is discarded?**

> **C. Is row-local cold repair cheap and robust enough to maintain long leases without keeping the richer 2D code alive?**

A negative answer to A or B would severely weaken this design family. A negative answer to C may still permit short or medium retention but undermine long cold leases.

### 17.7 Fallback: maturity-aware coding domains

If the hot-to-cold transition fails, the strongest fallback is to avoid mixing radically different maturities inside a persistent coded object.

Objects can be grouped into separate coding domains:

```text
frame A -> minutes
frame B -> hours
frame C -> days
frame D -> full horizon
```

This lets an entire physical codeword expire coherently. It also reintroduces discrete classes, packing fragmentation, and lane-allocation problems.

The tradeoff is therefore sharp:

- **Hot/cold lifecycle:** one large heterogeneous hot DAS domain, continuous logical leases, sparse cold expiry, but a new cold repair/security mechanism.
- **Maturity-aware domains:** simpler physical expiry and preservation of the dense codeword, but discrete classes and fragmented capacity.

### 17.8 The operational-dominance test and deployment order

The weak-dominance result in §3 remains necessary but insufficient. Let `G` be the logical byte-time saved by shorter leases and `O` the physical overhead introduced by sparse serving, metadata, proof handling, repair, and transition machinery. Variable retention is operationally beneficial only when realized physical savings exceed `O`.

The revised deployment order is therefore:

1. preserve a general duration-oriented **service abstraction**;
2. prototype sparse historical serving against present PeerDAS cells to isolate the packaging problem;
3. prototype the hot-to-cold transition against a concrete two-dimensional FullDAS code;
4. measure row-local cold repair under realistic custody churn;
5. if any kill question fails, fall back to maturity-aligned coding domains;
6. only then decide whether continuous expiry or a small number of physical maturities is justified.

The implementation dependency is now explicit:

> **Application retention semantics should not be forced to equal the lifetime of the physical representation optimized for fresh DAS—but the protocol must prove that those two lifetimes can actually be separated.**

---
