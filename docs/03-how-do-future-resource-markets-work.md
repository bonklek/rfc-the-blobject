# How do future resource markets work?

## 10. Future ingress and future-starting retention

A future DA reservation is a right to use network bandwidth at a specified time. The right expires if it is not used.

Its basic promise is:

> The holder may inject an allowed protocol-accounted quantity `B` into Ethereum DA around future time `s`.

This is not a cash-settled bet on future blob prices. It is a claim on **physical delivery of the network resource itself**.

`B` is constrained by the transport that issues the right. For an EIP-4844-compatible market it is an integer number of whole blob slots, not an arbitrary useful-payload length. Blob Streaming provides a concrete adjacent design. The current draft EIP-8256 uses non-refundable tickets tied to future target slots to authorize bounded AOT propagation, while reserving separate JIT capacity. Transferable claims, variable lookahead, arbitrary-sized objects, and a general secondary market remain extensions beyond that draft.

Once future ingress exists, future retention becomes a genuine reservation problem too. A claim sold today for publication at `s ≥ t` and duration `T` creates no active retained stock today, but it does create an obligation over the future interval:

```text
[s,s+T).
```

Combining publication and retention gives:

```text
DAService(C,B,s,T),
```

meaning:

> Make `B` bytes reconstructably available at start `s`, then require sufficient custody data to be retained and served until expiry `e=s+T`, under the selected service profile. Here `T` is elapsed duration, consistent with the base service.

### 10.1 The forward retained-stock curve belongs here

Viewed at current time `t`, define:

```text
S_t(τ)
```

as the amount of retained capacity already contracted for future horizon `t+τ`, including both currently active leases and obligations sold for future publication.

Now define a physically derived forward allocable envelope:

```text
C_t(τ)
=
K_safe(t+τ)
-
H_min(t+τ)
-
H_uncertainty(τ).
```

Here:

- `K_safe` is the retained-stock envelope implied by the custody architecture and hardware target;
- `H_min` keeps long leases from pre-consuming the chosen short-duration reserve, without claiming honest-user liveness inside that lane;
- `H_uncertainty(τ)` is an optional additional reserve against forecast error, future parameter changes, correlated demand, or long-horizon uncertainty.

The protocol then requires:

```text
S_t(τ) ≤ C_t(τ)
     ∀ τ.
```

The scalar envelope is a logical-stock projection; future service also needs the physical resource-vector constraints, reclamation margin, and supply commitments through the accepted term. Reducing new admission after supply loss does not cancel sold obligations. Replacement and repair reserves and emergency shortfall handling are unresolved branch requirements.

This defines the abstract `C(τ)`. Nothing physically requires the allocable envelope to decline at distant maturities. It declines only if the protocol deliberately increases uncertainty or headroom reserves with lookahead.

A future retention fee can then depend on the scarcity created along the purchased interval:

```text
F_ret^(forward)(B,s,T;t)
=
B · ∫_(s-t)^(s+T-t)
 p((S_t(τ)) / (C_t(τ))) dτ.
```

Forward occupancy pricing belongs here because a future-starting contract consumes capacity later without appearing in today's active stock.

### 10.2 Reservation attacks

A forward market introduces attacks absent from the narrow spot mechanism:

- cheap distant capacity can be accumulated before demand appears;
- holders can strategically fail to exercise ingress rights;
- future ingress and retention positions can be combined to crowd out a target interval;
- transferable rights can concentrate despite dispersed primary issuance;
- forecasts of `K_safe` can become stale before delivery.

Possible defenses include non-refundable reservations, bounded lookahead, increasing uncertainty reserves, position limits only where Sybil-resistant identity exists, auctions, and release of unused capacity near delivery. None is assumed solved here.

The market prices two future resources:

**Future ingress:** how scarce will admission bandwidth be around `s`?

**Future retention:** how scarce will custody be over `[s,s+T)`?

Blob Streaming supplies a potential **delivery date**. Variable retention supplies a **maturity**.

### 10.3 AOT tickets as prepaid network capabilities

AOT provides more than ordinary fee eligibility. In a conventional mempool, the network can spend bandwidth and validation work on candidate traffic that never lands. Blob Streaming puts payment and bounded authorization before the special propagation path:

```text
PAY FIRST
    -> receive a scarce future propagation capability
    -> bytes may enter AOT gossip
```

Draft EIP-8256 gives the network a bounded, globally agreed set of eligible senders and requires ticket ownership before the corresponding blob data is propagated. An attacker who reserves capacity to waste it pays the same ticket cost as an honest user. In that sense, a ticket is a **prepaid capability to consume one bounded unit of Ethereum DA-network bandwidth**, not merely a claim on a future fee.

That ordering constrains private authorization. If every peer must verify a fresh zero-knowledge ownership proof before rejecting an unknown publisher, privacy recreates a verification-DoS surface. The [private AOT authorization note](../appendices/private-aot-authorization.md) sketches a two-stage alternative: prove private ownership once in canonical state, then use a public ephemeral key that peers can check against a cheap allowlist.

---

## 11. Physical settlement

A financially owned future DA right and the operational credential that eventually exercises it need not be the same thing.

This distinction becomes important if future DA claims are transferable.

Suppose a claim to future capacity changes hands repeatedly before publication.

The final user may be:

- an L2 sequencer;
- a delegated publisher;
- a data-relay service;
- a treasury-controlled agent;
- or some other operational system.

Binding a permanent publication credential when the capacity is first issued becomes unnecessarily restrictive.

The current draft Blob Streaming design already exposes part of this distinction: each ticket record contains both an execution-layer `owner` address and a BLS public key used by the consensus layer to authenticate AOT propagation. But the BLS key is bound when the ticket is purchased, while the execution-layer mempool allowance remains anchored to the owner address. The draft does not itself provide transferable tickets or late-bound delivery credentials.

A generalized market could separate:

```text
financial ownership
```

from:

```text
operational delivery authorization.
```

Economic ownership could trade through a primary or secondary market.

Near physical settlement, the current holder could assign or authorize a publication credential valid for the relevant DA resource window.

That separation permits:

- delegation;
- hot/cold key separation;
- operational key rotation;
- treasury versus networking-key separation;
- transfer of DA rights without transfer of operational signing keys.

It may also simplify pooled capacity markets.

The main technical question is how Ethereum’s execution-layer and consensus-layer admission mechanisms recognize the right after settlement while retaining cheap anti-DoS validation. Under the current EIP-8256 draft, EL mempool propagation is explicitly gated by `blob_allowance(sender)` derived from ticket ownership, while the CL validates AOT propagation using the registered BLS key. Transferability or late binding therefore requires a replacement or indirection for the owner-based allowance rule, or a cleaner separation between the availability event and the eventual application transaction.

One privacy-oriented design uses **private ownership followed by canonical public activation**. The holder spends a shielded credit with an on-chain proof that registers a slot-specific publication key. Peers reject unknown keys with an O(1) lookup before doing expensive payload validation, and reorgs update the allowlist through ordinary canonical state. This still reveals activation timing, capacity class, and operational traffic. Pooling and common denominations would be needed for a useful anonymity set. The construction remains an appendix-level research direction rather than part of the base market.

---

## 12. Privacy boundaries

Separating financial ownership from operational delivery also exposes several distinct privacy questions.

Late-bound delivery credentials do not create privacy by themselves. If ownership transfers remain fully public, a fresh publication key can still be linked through the transparent provenance graph. Economic unlinkability would require ownership to enter a shielded, aggregated, pooled, or otherwise privacy-preserving domain before settlement.

A generalized DA service has at least four relevant privacy dimensions.

### Economic privacy

Who paid for or owned the publication right?

### Network privacy

Which IP address or first-hop peer originated the data?

### Application privacy

Who is communicating, who is the recipient, and what do the bytes mean?

### Service-pattern privacy

What can be inferred merely from the selected network resource profile?

Each dimension needs a different mechanism:

```text
payer -> publication       shielded or pooled settlement
IP -> first peer           mix/onion ingress or a privacy relay
sender -> recipient        application encryption and private retrieval
object -> service profile  padding, common classes, and timing cover
```

[Waku](https://docs.waku.org/learn/concepts/protocols/) provides useful precedent for keeping these layers separate. RLN Relay combines zero-knowledge membership with rate limiting for economic anti-spam. Waku's content-topic guidance also warns that Filter, Store, and Light Push peers can link an IP address to a topic interest. Anonymous admission therefore does not hide network origin, recipient interest, or retrieval behavior by itself.

Gossip has the same boundary. Encryption can hide the payload, and broad GossipSub topics can enlarge the recipient anonymity set, but a peer that receives a new object directly can still learn its first hop. A mixnet, onion route, or unlinkable relay can protect ingress without hiding a distinctive retention purchase or a later targeted fetch.

Variable retention creates the last category explicitly.

A one-epoch object—about 6.4 minutes—may resemble messaging, streaming, or real-time coordination.

A full-horizon 4,096-epoch object—about 18.2 days under current timing—may resemble rollup or archival data.

Even if the payload is encrypted, the payer is hidden, and network ingress is mixed, size, timing, and retention maturity can leak application information.

Privacy-sensitive applications may therefore use:

- standardized maturity intervals;
- padded lease durations;
- pooled capacity;
- shielded ownership domains;
- mixed or delayed settlement;
- common size classes.

These privacy layers are independent. Encrypting a payload does not hide its funding, and hiding the funding does not hide the originating IP address. A mixnet may hide network origin while still revealing that someone purchased an unusual full-horizon 40 MB lease lasting 4,096 epochs—about 18.2 days.

The DA layer need not interpret any of these semantics. It only needs to enforce scarce resource allocation and availability.

---

## 13. Censorship-resistant replication windows after inclusion

Variable retention also creates a useful primitive for censorship-resistant dissemination **after the data has actually been admitted and made available**.

Some applications care intensely about a strong publication path and a protocol-required replication opportunity but do not need Ethereum itself to retain the data indefinitely. Variable retention strengthens the second property; it does not, by itself, solve transaction inclusion censorship. This distinction is especially important for Blob Streaming: the current EIP-8256 draft explicitly leaves mandatory inclusion of AOT blob transactions to future work.

Consider a document, dataset, software artifact, media stream, or other object whose primary security objective is to become widely replicable once released.

The publisher can purchase:

```text
strong Ethereum ingress
+
short protocol-required retention.
```

Once Ethereum establishes publication-time availability, a protocol-required replication window begins.

During that interval, arbitrary parties can retrieve the exact committed bytes and hand them off to:

- torrent-like swarms;
- mirrors;
- archives;
- EthStorage;
- Filecoin;
- application-specific storage networks;
- journalists;
- watchdog organizations;
- or ordinary users.

Ethereum can provide a useful censorship-resistance property after inclusion and availability establishment without becoming a permanent-storage network.

It can provide the protocol serving requirement:

> **For the next `R`, these exact committed bytes are reconstructably available under Ethereum’s DA security assumptions.**

If `R` is long enough for independent replication, indefinite persistence can bootstrap elsewhere.

The responsibilities divide as follows:

**Ethereum DA**

provides publication-time DAS plus a required replication opportunity under the custody assumptions; censorship resistance of the admission path depends on the surrounding inclusion mechanism.

**Persistent storage systems**

provide longer-term storage and retrieval.

**Privacy systems**

hide payer identity, network origin, application metadata, or recipients where desired.

A durably preserved commitment or versioned hash can preserve attribution to the originally published object even after Ethereum’s custody obligation ends. Because Ethereum is separately moving toward bounded historical serving, the persistence of that compact anchor should be specified rather than assumed.

### 13.1 Inclusion censorship is upstream of DAS

“Censorship-resistant publication” contains at least three distinct failure modes:

1. **Admission or inclusion censorship:** a transaction or blob is never selected for a canonical block. PBS builder concentration and proposer behavior sit here. Committee inclusion-list designs such as [FOCIL / EIP-7805](https://eips.ethereum.org/EIPS/eip-7805) address this layer by requiring proposers to respect independently assembled inclusion lists.
2. **Publication-time availability censorship:** a commitment is selected, but enough underlying bytes are withheld that the block should not be treated as available. DAS, dispersal, sampling, and availability fork-choice rules sit here.
3. **Post-inclusion service censorship:** some custodians refuse historical requests after availability was established. Redundant custody, peer selection, repair, and the required-serving window sit here.

Variable retention changes the duration of the third guarantee. It does not solve the first, and DAS principally addresses the second. Likewise, distributed blob publication can remove the winning builder as the only synchronous DA uplink without removing the builder's political power over which transactions or blob commitments enter the block.

The generalized data plane is therefore a censorship-resistant publishing substrate only to the extent that its admission and canonical-inclusion path is itself robust against concentrated builders and proposers. Inclusion lists and related PBS reforms are complementary dependencies, not features supplied by variable retention.

---

[Project overview](../README.md) · [Document map](document-map.md)
