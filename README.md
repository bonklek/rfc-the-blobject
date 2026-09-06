# The Blobject

**A research proposal for choosing how long Ethereum must keep published data retrievable.**

Ethereum already lets applications publish data that the network temporarily stores and serves. The Blobject asks whether the purchaser should also choose the length of that service. A rollup might need a long recovery window; a media segment or a prover's input might need only enough time to be copied and processed. Giving both the same required lifetime may waste storage, provided shorter service is actually safe and cheaper to implement.

This repository contains an RFC, worked examples, and executable models. **It is a research proposal, not an implemented Ethereum feature.** The accounting result follows from explicit assumptions; useful physical savings, safe minimum durations, and an implementation remain to be demonstrated.

**Author:** Bonkle K · **Status:** working draft / request for comment

## What would change?

Ethereum's *data availability* service lets participants obtain enough authenticated pieces to reconstruct published data. A *blob* is the fixed-size data object purchased through the current interface. The network checks availability when it is published; assigned nodes then have a continuing duty to keep and serve their pieces.

The current PeerDAS configuration uses a minimum recent-serving range of **4,096 epochs, approximately 18.2 days**. An epoch is 32 slots, or about 6.4 minutes at 12 seconds per slot. The request rule includes both endpoint epochs, so this is a nominal horizon rather than an exact countdown from each publication. [Specification and boundary details](docs/00-what-is-the-proposal.md#3-minimum-and-maximum-protocol-required-retention).

The proposal separates two costs:

| Resource | What the network does | Effect of a shorter lease |
|---|---|---|
| **Publication, or ingress** | Propagates, encodes, verifies, and samples fresh data | The initial work remains |
| **Retention** | Keeps and serves enough authenticated data for later reconstruction | The required service ends earlier |

A purchaser would pay for publication plus the selected retention obligation. The exact fee mechanism is open. An accepted prepaid lease would retain its promised end time even if prices later rise.

The conservative design keeps today's publication limits and a full-service option, whose exact expiry must be mapped to the existing serving rule. Shorter choices must meet Ethereum's recovery requirements and the application's needs. A small menu of durations may suffice; arbitrary epoch choices are an alternative to test. [Service definition](docs/00-what-is-the-proposal.md#2-logical-service-abstraction) · [Pricing alternatives](docs/01-how-are-capacity-and-pricing-managed.md#5-pricing-protocol-required-byte-time).

## One blob, from publication to expiry

1. **Choose a duration.** The application buys whole blobs. Each publication receives its own lease; publishing identical content twice creates two obligations. Items packed into one blob share its lifetime.
2. **Check admission.** The new obligation must fit both the logical stock limit and physical limits for storage, serving, repair, and I/O. Payment cannot bypass those limits.
3. **Establish availability.** Publication uses the relevant sampling and custody rules. The clock starts at inclusion and includes the initial availability work.
4. **Keep serving.** Assigned nodes must serve their pieces until expiry under the lease's service rules. The base design relies on protocol duties and custody assumptions; it does not add repeated proofs of continuous service.
5. **End the duty and reclaim capacity.** Expiry ends the requirement. Physical storage may become reusable later, so admission accounting must allow for reclamation delay. Nodes and archives may keep copies voluntarily.

A commitment—a cryptographic identifier against which data can be checked—can authenticate a surviving copy. It cannot recover missing bytes or prove that the network served them throughout the lease. A recipient's acknowledgement is also a different claim from availability to the wider network. [State-transition sketch](docs/01-how-are-capacity-and-pricing-managed.md#41-non-normative-protocol-state-sketch) · [Guarantees and enforcement](docs/00-what-is-the-proposal.md#21-availability-establishment-versus-retained-retrievability).

## What does the arithmetic prove?

For the **same blobs published at the same times**, ending some obligations earlier cannot increase the amount of data still owed later. An illustrative 8-epoch lease, about 51 minutes, requires **1/512 of the byte-time** of a 4,096-epoch elapsed lease. Eight epochs is not an established safe minimum, and this ratio is neither a fee discount nor a measured storage saving.

Leases that start immediately are straightforward to count: each adds to active stock on admission and leaves it at expiry. Already accepted obligations can only shrink as time passes. Future-starting commitments need additional accounting because their load is not yet present. [Logical derivation](docs/00-what-is-the-proposal.md#32-resource-allocation-dominance-under-fixed-ingress) · [Capacity accounting](docs/01-how-are-capacity-and-pricing-managed.md#4-flow-and-active-retained-stock).

The strongest objection is practical: **removing a requirement saves little if it was not the expensive part, or if implementing its removal costs more than it saves.** Shorter retention does not reduce initial network traffic or writes. Raising throughput on the strength of expected short leases requires a separate physical capacity case.

## The main implementation obstacle

Ethereum serves encoded pieces and packages, not independent files with deletion timers. In current **PeerDAS**, a column-sidecar package contains pieces from multiple blobs in a block. If one blob expires earlier, preserving the complete package can preserve its bytes anyway. The first experiment is to test whether nodes can efficiently store and serve only the still-required cells while keeping reconstruction and recovery safe.

Cell-level transport research makes that direction plausible, but does not implement historical expiry. A possible future **two-dimensional FullDAS** design adds shared redundancy across blobs: deleting one blob can affect the coding structure supporting others. Transitioning to independently reconstructable retained rows is a research branch; grouping compatible expirations into separate coding domains is an alternative. [PeerDAS and FullDAS analysis](docs/05-can-this-work-with-peerdas-and-fulldas.md).

Both paths must account for failed nodes, repairs, historical requests, pruning backlogs, hardware limits, and network traffic. A logical stock cap alone is insufficient. [Hardware constraints](docs/11-how-do-hardware-and-da-operator-markets-scale.md) · [Network scale arithmetic](appendices/backbone-scale-limits.md).

## Which applications could use shorter service?

The question is when someone must still be able to recover the data, not merely when its publisher stops caring about it.

- **Rollups:** challengers, users, and new nodes may need data after execution or proving. A challenge-period length alone does not determine a safe lease. Shorter native service can introduce reliance on watchers or archives that acquired the bytes in time. [Rollup safety](docs/02-is-variable-retention-safe-for-rollups.md).
- **Computation and proofs:** a prover could fetch a large input, retain it locally, and later publish a compact result and proof. Native service may end before proving finishes if a suitable recovery path remains. [Ephemeral data and proofs](appendices/ephemeral-data-and-proofs.md).
- **Media, messaging, and storage bootstrapping:** a replication window might suffice for some workflows, followed by application-specific delivery or persistence. The two selected application case studies are **Blobcast**, for stream acquisition and archive handoff, and **BlobMail**, for offline-message delivery and expiry recovery. Their implementations provide experimental starting points; they do not yet establish demand or safe short durations. [Applications and evidence](docs/06-what-does-a-generalized-data-plane-enable.md) · [Concrete experiments](audits/application-use-case-review.md).

External storage can continue serving data after Ethereum's duty ends. It cannot itself shorten that native duty. A handoff must happen before expiry and carries the receiving system's own assumptions. [Persistence and handoffs](docs/04-what-happens-after-ethereum-retention-ends.md).

## What else does the project explore?

These extensions explain the broader design space; the base experiment does not depend on them.

| Direction | Question it explores |
|---|---|
| [Future resource markets](docs/03-how-do-future-resource-markets-work.md) | Can future publication and retention be reserved and transferred without overselling or implying guaranteed inclusion? |
| [Private authorization](appendices/private-aot-authorization.md) | Can private ownership activate a public temporary key while preserving cheap spam rejection and bounded gossip use? |
| [RetentionNotes](appendices/retention-notes.md) | Can downstream storage end on an acknowledgement or cancellation, and who controls termination? |
| [Lean Ethereum and history](docs/10-how-does-lean-ethereum-change-the-proposal.md) | How would protocol payloads or permanent sparse history change lifecycle and payment rules? |
| [Operator procurement](docs/11-how-do-hardware-and-da-operator-markets-scale.md#4-separate-scarcity-from-hardware-service) | If specialized providers were paid, how should qualified service, failure, market power, and replacement capacity be handled? |
| [Early surrender and replacement](appendices/active-lease-surrender-and-novation.md) | Who may end a lease early, and when can its physical capacity safely support another object? |

Pricing storage by duration and separating recent availability from long-term persistence have substantial prior art. The claimed contribution is their particular application to purchaser-selected Ethereum serving obligations and representation-aware accounting. [Prior art](docs/07-what-is-the-prior-art-and-novelty.md) · [Sources and verification dates](REFERENCES.md).

## What would make the proposal worth pursuing?

Compare **unchanged service, a small duration menu, and arbitrary epoch choices** under the same workload, recovery guarantees, and hardware assumptions. Measure storage reclaimed alongside metadata, writes, requests, repairs, and failure behavior. Establish which real applications can safely use shorter windows and whether the savings matter economically.

The models cover logical stock, illustrative prices, fixed-arrival allocation scenarios, independent-loss custody, and a provider-price controller. They expose counterexamples and make calculations reproducible. They do not establish demand, network security, hardware performance, or a stable market. [Models and results](models/README.md) · [Workload evidence needed](docs/08-what-remains-to-be-proven.md#workload-evidence-plan).

If shorter service yields no meaningful net benefit or applications cannot use it safely, narrow or abandon the proposal. If a small menu captures the value, prefer it. Failure of an optional 2D or market branch need not reject the base mechanism. [Tests and deployment gates](docs/08-what-remains-to-be-proven.md) · [Conclusion](docs/09-what-is-the-conclusion.md).

## Read, reproduce, or contribute

The core reading order is [definition](docs/00-what-is-the-proposal.md) → [accounting](docs/01-how-are-capacity-and-pricing-managed.md) → [physical feasibility](docs/05-can-this-work-with-peerdas-and-fulldas.md) → [application safety](docs/02-is-variable-retention-safe-for-rollups.md) → [constraints](docs/11-how-do-hardware-and-da-operator-markets-scale.md) → [prior art](docs/07-what-is-the-prior-art-and-novelty.md) → [tests](docs/08-what-remains-to-be-proven.md) → [conclusion](docs/09-what-is-the-conclusion.md).

Chapters live in `docs/`, worked extensions in `appendices/`, experiments in `models/`, and validation/generation tools in `tools/`. Existing paths and section numbers are retained for citations. [Document and artifact map](docs/document-map.md) · [Audit findings and dispositions](audits/2026-09-06-completion.md).

With Python, PowerShell, and ripgrep installed, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/validate-rfc.ps1
```

Useful contributions include counterexamples, closer prior art, measured constraints, and reproducible tests that could change the design decision. [Contribution and regeneration guide](CONTRIBUTING.md) · [Operator-market research questions](RESEARCH_TRACKING.md).

Citation metadata is in [CITATION.cff](CITATION.cff). This work uses the [Viral Public License](LICENSE).
