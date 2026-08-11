# How do future resource markets work?

## 10. Future ingress and future-starting retention

A right to consume DA bandwidth at a particular future time is a perishable network resource.

The abstract claim is:

> The holder may inject `B` bytes into Ethereum DA around future time `T`.

This is distinct from a cash-settled derivative on future blob prices. The object contemplated here is **physical delivery of the network resource itself**.

Blob Streaming provides a concrete adjacent design. The current draft EIP-8256 uses non-refundable tickets tied to future target slots to authorize bounded AOT propagation, while reserving separate JIT capacity. Transferable claims, variable lookahead, and a general secondary market remain extensions beyond that draft.

Once future ingress exists, future retention becomes a genuine reservation problem too. A claim sold today for publication at `T` and retention `R` creates no active retained stock today, but it does create an obligation over the future interval:

```text
[T,T+R].
```

The complete service is therefore:

```text
DAService(B,T,R),
```

meaning:

> Make `B` bytes reconstructably available around time `T`, then require sufficient custody data to be retained and served through `T+R`.

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
- `H_min` preserves the chosen minimum-liveness reserve;
- `H_uncertainty(τ)` is an optional additional reserve against forecast error, future parameter changes, correlated demand, or long-horizon uncertainty.

The protocol then requires:

```text
S_t(τ) ≤ C_t(τ)
     ∀ τ.
```

This gives the earlier abstract `C(τ)` a concrete interpretation. A declining allocable envelope at distant maturities is **not a physical law**. It arises only if the protocol intentionally increases uncertainty/headroom reserves with lookahead.

A future retention fee can then depend on the scarcity created along the purchased interval:

```text
F_ret^(forward)(B,T,R)
=
B · ∫_T^(T+R)
 p((S_t(τ)) / (C_t(τ))) dτ.
```

This is where forward occupancy pricing is structurally justified: unlike a spot-start lease, a future-starting contract can consume capacity later without consuming it now.

### 10.2 Reservation attacks

A forward market introduces attacks absent from the narrow spot mechanism:

- cheap distant capacity can be accumulated before demand appears;
- holders can strategically fail to exercise ingress rights;
- future ingress and retention positions can be combined to crowd out a target interval;
- transferable rights can concentrate despite dispersed primary issuance;
- forecasts of `K_safe` can become stale before delivery.

Possible defenses include non-refundable reservations, bounded lookahead, increasing uncertainty reserves, position limits only where Sybil-resistant identity exists, auctions, and release of unused capacity near delivery. None is assumed solved here.

The resulting market has two forward dimensions:

**Future ingress:** how scarce will admission bandwidth be around `T`?

**Future retention:** how scarce will custody be over `[T,T+R]`?

Blob Streaming supplies a potential **delivery date**. Variable retention supplies a **maturity**.

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

A generalized market could therefore go one step further and separate:

```text
financial ownership
```

from:

```text
operational delivery authorization.
```

Economic ownership could trade through a primary or secondary market.

Near physical settlement, the current holder could assign or authorize a publication credential valid for the relevant DA resource window.

This supports:

- delegation;
- hot/cold key separation;
- operational key rotation;
- treasury versus networking-key separation;
- transfer of DA rights without transfer of operational signing keys.

It may also simplify pooled capacity markets.

The main technical question is how Ethereum’s execution-layer and consensus-layer admission mechanisms recognize the right after settlement while retaining cheap anti-DoS validation. Under the current EIP-8256 draft, EL mempool propagation is explicitly gated by `blob_allowance(sender)` derived from ticket ownership, while the CL validates AOT propagation using the registered BLS key. Transferability or late binding therefore requires a replacement or indirection for the owner-based allowance rule, or a cleaner separation between the availability event and the eventual application transaction.

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

Variable retention creates the last category explicitly.

A two-minute object may resemble messaging, streaming, or real-time coordination.

A fourteen-day object may resemble rollup or archival data.

Even if the payload is encrypted, the payer is hidden, and network ingress is mixed, size, timing, and retention maturity can leak application information.

Privacy-sensitive applications may therefore use:

- standardized maturity intervals;
- padded lease durations;
- pooled capacity;
- shielded ownership domains;
- mixed or delayed settlement;
- common size classes.

These privacy layers remain conceptually independent.

Encrypting payloads does not hide funding.

Hiding funding does not hide IP origin.

A mixnet does not hide that the user purchased an unusual fourteen-day, 40 MB lease.

The DA layer need not interpret any of these semantics. It only needs to enforce scarce resource allocation and availability.

---

## 13. Censorship-resistant replication windows after inclusion

Variable retention also creates a useful primitive for censorship-resistant dissemination **after the data has actually been admitted and made available**.

Some applications care intensely about a strong publication path and a guaranteed replication opportunity but do not need Ethereum itself to retain the data indefinitely. Variable retention strengthens the second property; it does not, by itself, solve transaction inclusion censorship. This distinction is especially important for Blob Streaming: the current EIP-8256 draft explicitly leaves mandatory inclusion of AOT blob transactions to future work.

Consider a document, dataset, software artifact, media stream, or other object whose primary security objective is to become widely replicable once released.

The publisher can purchase:

```text
strong Ethereum ingress
+
short guaranteed retention.
```

Once Ethereum establishes availability, a guaranteed replication window begins.

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

Ethereum therefore need not become a permanent-storage network to provide a powerful censorship-resistance property once inclusion and availability establishment have occurred.

It can provide the protocol serving guarantee:

> **For the next `R`, these exact committed bytes are reconstructably available under Ethereum’s DA security assumptions.**

If `R` is long enough for independent replication, indefinite persistence can bootstrap elsewhere.

This produces a clean division of labor:

**Ethereum DA**

provides economically secured availability after inclusion and a guaranteed replication opportunity; censorship resistance of the admission path depends on the surrounding inclusion mechanism.

**Persistent storage systems**

provide longer-term storage and retrieval.

**Privacy systems**

hide payer identity, network origin, application metadata, or recipients where desired.

A durably preserved commitment or versioned hash can preserve attribution to the originally published object even after Ethereum’s custody obligation ends. Because Ethereum is separately moving toward bounded historical serving, the persistence of that compact anchor should be specified rather than assumed.

---
