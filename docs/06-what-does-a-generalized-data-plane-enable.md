# What does a generalized Ethereum data plane enable?

## 18. High-throughput ephemeral DA

Ephemeral retention does not reduce the live bandwidth needed to establish availability. Gigabytes per second still have to cross the network, be processed, and become reconstructably available. Nor is it practical to reach that throughput by multiplying today's 128 KiB blob objects into hundreds of thousands or millions of objects per slot.

A high-throughput architecture would likely require:

- larger coded DA frames;
- extensive multiplexing;
- ahead-of-time or continuous propagation;
- increasingly fine distributed custody;
- efficient repair;
- batch or aggregate proof verification;
- consensus periodically certifying availability over a continuous data plane;
- markets for ingress;
- explicit accounting for custody through time.

Applications could still submit small logical messages or objects. The underlying transport would batch them into much larger DA structures.

Variable retention is independent of this transport evolution. Its purpose is to prevent an increase in real-time throughput from automatically causing a proportional increase in mandatory long-term storage.

At one gigabyte per second, for example, a one-epoch raw logical retention window—384 seconds, or about 6.4 minutes—corresponds to roughly 384 GB of currently live data. A 4,096-epoch window—about 18.20 days—corresponds to roughly 1.57 PB. Both cases have the same ingress bandwidth and radically different storage obligations.

This distinction becomes increasingly consequential as Ethereum DA moves from megabytes per second toward hundreds of megabytes or gigabytes per second.

Storage is only one frontier. The [backbone-scale appendix](../appendices/backbone-scale-limits.md) derives the matching per-node and aggregate network bounds. It covers shrinking custody fractions, 10,000-node stress cases, object-count explosion, and current PeerDAS cell-proof arithmetic. Its conclusion is stricter: shorter retention does not relax live network conservation.

### 18.1 High-throughput DA does not require a mega-builder

Execution and MEV may centralize block construction for reasons unrelated to DA dissemination. The dangerous design is one in which the winning PBS builder must ingest, encode, and upload the entire DA frame during the slot. That turns a large synchronous uplink into a prerequisite for competitive block building.

The AOT-plus-FullDAS path in §17.9 draws the boundary differently. The builder selects a manifest of rows that have already been dispersed, while row holders and column networks distribute cells and assemble redundancy. The builder can remain specialized in execution ordering without becoming the sole source of every DA byte.

This does not solve builder centralization. [BuilderNet](https://buildernet.org/) explores collaborative multi-node block building, and [multi-party block construction](https://ethresear.ch/t/building-towards-multi-party-block-construction/24975) explores blocks assembled from several builders' contributions. Both show that “one block” need not mean one indivisible construction process, but both introduce their own trust, coordination, latency, and MEV questions.

The limited conclusion is that variable retention does not itself require one centralized publication path. A high-throughput design still needs a concrete distributed acquisition, propagation, reconstruction, and failure-handling protocol; removing the builder as the sole uplink is a requirement, not a demonstrated solution.

That is a bandwidth claim, not an inclusion-censorship claim. Distributed upload does not force a concentrated PBS builder to select a transaction or blob commitment. The [admission/inclusion analysis in §13.1](03-how-do-future-resource-markets-work.md#131-inclusion-censorship-is-upstream-of-das) separates inclusion censorship, publication-time withholding, and post-inclusion service refusal; a generalized data plane inherits the first problem unless inclusion lists or another robust admission path address it.

---

## 19. Application space

A generalized Ethereum availability market could serve applications whose timing requirements differ sharply.

The most direct non-rollup pattern is **ephemeral working data**: information that must be publicly retrievable long enough to drive a computation or state transition, but need not remain in Ethereum's native service afterward.

```text
temporary authenticated data
        |
        v
Ethereum DA
        |
        v
off-chain computation or proving
        |
        v
succinct result or proof
        |
        v
durable Ethereum state transition
        |
        v
raw working data may leave protocol service
```

Durable state still belongs in the consensus state when later execution must read it synchronously: balances, ownership, commitments, state roots, nullifiers, and settlement outputs are typical examples. Blobs can instead carry temporary orders, bids, game actions, message batches, computation inputs, witnesses, coordination data, or intermediate application state. They do not replace permanent Ethereum state; they can let an application keep only the compact result of work performed over larger temporary inputs.

The selected duration is therefore a deadline for every actor that still needs the raw bytes. An application-specific minimum may need to cover retrieval, computation or proving, result publication or settlement, retries, and a safety margin. The [ephemeral proving appendix](../appendices/ephemeral-data-and-proofs.md#c4-proving-window-requirements) gives the corresponding timing condition. This application requirement is independent of Ethereum's own `T_protocol-min`, and the selected duration must satisfy both.

Examples include:

- rollup DA;
- proof and witness distribution;
- private messaging;
- public authenticated messaging;
- live media;
- broadcast;
- social feeds;
- games;
- oracle and event data;
- agent coordination;
- censorship-resistant publication;
- decentralized-storage bootstrap;
- software distribution;
- arbitrary application data.

The protocol should not encode these as application categories.

Their differences emerge from the protocol-accounted quantity, selected serving duration, and any access, routing, privacy, or enforcement profiles:

```text
B, T, service/access profile
```

A live-media segment might select 8 epochs—about 51.2 minutes—if the eventual protocol minimum and its own delivery requirements permit it. Eight epochs is an illustrative stress case, not a proposed parameter.

A message may purchase enough time for recipient relays to observe it.

A storage bootstrap object may purchase enough time for a persistent P2P network to acquire it.

A rollup may purchase 256–4,096 epochs—about 1.14–18.20 days—subject to its security minimum.

![Five example data uses crossing mandatory hot DAS and choosing different Ethereum cold-custody horizons, with public artifacts and L2 data optionally continuing into external storage.](assets/figures/figure-05-application-lifecycle.svg)

*Figure 5 — Application examples across the data lifecycle.* Every object crosses the common hot-availability phase. Live media may stop at the minimum; communication and interactive data can select intermediate serving windows; public artifacts can give mirrors time to acquire them; and rollup or L2 data posting can select the full 4,096-epoch horizon. External storage may overlap Ethereum custody and continue afterward. These are examples of resource profiles, not application categories recognized by the protocol.

### 19.1 Experimental application evidence

The application case studies selected for this round are **Blobcast (Radio Free Ethereum)** and **BlobMail**. Their implementations provide concrete non-rollup workflows to study. They do not yet demonstrate demand for selectable retention:

- [Radio Free Ethereum](https://github.com/bonklek/poc-blobcast/blob/8d4924edaf7ecad2ddaccb2bd52df08ff24284e3/README.md) is an Ethereum blob-radio prototype with a station contract, publishing tools, and a browser tuner that verifies and plays media segments.
- [BlobMail](https://github.com/bonklek/poc-blobmail/blob/939b1d8a5dc2f9ca230a2a7e9d301923033d877b/README.md) now documents an experimental Sepolia messaging MVP with batch publication and KZG verification. The September source review supersedes the August local-fixture description; it inspected repository evidence, not an independently rerun live acceptance test.

The projects sit at opposite ends of the application surface—public streaming and recipient-private messaging. They illustrate workflows that might use a bounded publication window; neither establishes safe shorter horizons, demand, or cost advantage for this proposal. Their reported functionality does not establish that the proposed protocol or privacy stack is complete.

Their value is that each supplies a different retention experiment:

| Selected case study | Concrete requirement | First experiment |
|---|---|---|
| Radio Free Ethereum / Blobcast | Listeners need segments for initial playback, late joins, and retries; replay and archives may require copies much later | Replay the same publication and listener trace under different simulated serving windows. Measure verified acquisition, interrupted playback, archive dependence, and total storage and traffic |
| BlobMail | A recipient must discover and acquire a batch before its last usable copy disappears; publication does not establish receipt | Sweep recipient offline time and provider outages. Include an unavailable old batch followed by fresh mail, and measure both delivery and cursor recovery |

Blobcast's [availability model](https://github.com/bonklek/poc-blobcast/blob/8d4924edaf7ecad2ddaccb2bd52df08ff24284e3/packages/protocol/availability.mjs) already compares an asset's serving deadline with a required season-end deadline plus margin. Its current profile is not an implementation of purchaser-selected Ethereum retention. BlobMail's [receiver](https://github.com/bonklek/poc-blobmail/blob/939b1d8a5dc2f9ca230a2a7e9d301923033d877b/src/mailbox/receiver.js) fails a refresh without advancing its cursor when a discovered segment cannot be verified. That deliberate verification boundary makes expiry recovery a specific behavior to test: shorter retention must not silently lose mail or prevent progress through later batches.

These projects share an author with this proposal. They can supply implementation fixtures and workload traces, but should not be counted as independent adoption evidence. The [application review and experiment design](../audits/application-use-case-review.md) distinguish inspected source, recorded live results, and measurements still needed.

All of these applications use the same primitive:

> **market-priced, protocol-required retrievability over committed bytes under explicit custody assumptions.**

---

## 20. Why the scope matters

Ethereum should not try to replace BitTorrent, Tor, Filecoin, messaging protocols, CDNs, or the Internet. The proposal assigns Ethereum a narrower role.

Ethereum can supply:

- economic scarcity;
- settlement;
- authenticated commitments;
- admission control;
- censorship-resistant publication;
- distributed availability;
- and eventually markets for those resources through time.

Specialized systems can supply:

- routing;
- privacy;
- discovery;
- indexing;
- long-term persistence;
- retransmission;
- application semantics.

At the level of architecture, this resembles Lightning's relationship to Bitcoin: a base chain supplies scarce settlement and enforceable commitments while a specialized network handles high-frequency behavior. Here the pattern applies to publication and bounded retrievability rather than payment-channel balances. The analogy does not import Lightning's security or privacy properties.

In this architecture, Ethereum serves as a **permissionless economic control plane and availability substrate**. A user purchases a scarce network resource, authenticated bytes enter a globally shared data plane, and DAS establishes publication-time availability. Assigned custodians then serve enough authenticated data for reconstruction for the chosen period. Specialized systems take over afterward, handling routing, privacy, discovery, or persistence.

Ethereum's rollup-oriented DA roadmap may already contain much of the infrastructure needed for a more general economically secured network substrate, even though that was not its original design objective.

### 20.1 A historical rhyme with the early Web3 stack

This endpoint has an Ethereum lineage. The 2014 decentralized-Web framing described a three-part family: Ethereum contracts for logic, Swarm for decentralized storage, and Whisper for decentralized messaging. The 2016 Swarm introduction likewise described separate `eth`, `bzz`, and `shh` protocols intended to compose into a broader Web3 stack.

That integrated stack did not become today's Ethereum architecture. [Whisper is deprecated](https://ethereum.org/developers/docs/networking-layer/#whisper), while [Swarm continues as a separate storage and distribution system](https://ethereum.org/developers/docs/storage/#swarm). The Blobject does not propose restoring either protocol or putting messaging and permanent storage into consensus.

The historical rhyme is functional rather than institutional:

```text
early composition                 emerging composition

Ethereum contracts               Ethereum settlement and commitments
Whisper messaging        ->       privacy/messaging overlays and relays
Swarm storage                     competing downstream persistence systems
                                  PeerDAS/FullDAS bounded availability
```

The newer composition begins with a narrower base-layer promise: economically scarce admission, authenticated publication, and bounded reconstructability. Routing, privacy, delivery, and permanent storage remain plural overlay services. It may recover some ambitions of the early decentralized-Internet stack through explicit markets and interfaces rather than one bundled Ethereum software suite.

### 20.2 A broader resource-strength principle

Variable-retention DA is one instance of a wider design pattern:

| Resource | Stronger form | Specialized or weaker form |
|---|---|---|
| State | permanent synchronously accessible state | temporary, UTXO-like, or separately recoverable state classes |
| Data | one full universal serving horizon | short leases, longer leases, or reduced sparse tails |
| Execution | universal direct re-execution | validity-proved execution under an explicit witness-availability model |

The general principle is:

> **Price and require guarantees according to the semantic strength applications need, rather than silently granting every object the strongest available guarantee.**

This is a research heuristic, not a claim that the rows are interchangeable. Active state must support synchronous execution reads. A validity proof can establish a computation without supplying its witness. DA must provide a permissionless reconstruction path under its sampling and custody assumptions. Specialization is useful only while those semantic boundaries remain explicit.

Variable retention matters because it removes a temporal assumption inherited from the rollup use case.

Shorter native service could make additional applications economical if the savings exceed ingress, custody, and overlay costs. The scale of that demand is unmeasured; neither the application examples nor the fixed-arrival pricing model establish it.

---

[Project overview](../README.md) · [Document map](document-map.md)
