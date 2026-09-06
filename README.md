# The Blobject

**Temporary data as a general-purpose Ethereum resource.**

Blobs give Ethereum a way to make data available without putting all of that data into permanent contract storage. Their familiar role is to carry rollup batches. The Blobject starts from a broader reading of that capability: Ethereum can provide a shared publication window for any application that needs others to acquire authenticated data.

This RFC develops that idea by making the length of the window selectable. A publisher would pay to distribute data and choose how long Ethereum must keep it retrievable. Public media, encrypted messages, computation inputs, and rollup batches could each buy a duration suited to their lifecycle. Readers could use the data, copy it into longer-term storage, or turn it into a compact result that outlives the original publication.

The proposal connects that change to a broader architecture of publication, computation, communication, and persistence. This repository contains the argument, service design, worked examples, and executable models.

**Author:** Bonkle K · **Status:** working draft / request for comment

## What blobs are today

Ethereum introduced blobs through EIP-4844 to give rollups a dedicated data-publication resource with its own fee market. A blob is a fixed-size encoded data object carried alongside a transaction. The transaction references its content through a cryptographic commitment; the network distributes and temporarily serves the data. Applications retrieve the bytes and check them against that commitment. [EIP-4844](https://eips.ethereum.org/EIPS/eip-4844).

A rollup executes transactions in its own system and publishes batches so other participants can reconstruct and verify its activity. In that setting, a blob is naturally understood as a rollup's data container. The familiar question becomes how many batches Ethereum can carry, and how cheaply.

The underlying format is more general. Ethereum's virtual machine does not directly read the blob's full contents: execution has access to commitment-derived identifiers, while applications retrieve the payload separately. The publisher supplies the application's encoding and meaning. This separation lets Ethereum establish availability for data that other systems interpret and process. [Execution and blob data](https://eips.ethereum.org/EIPS/eip-4844#blob-non-accessibility).

In this RFC's baseline, the recent-serving horizon is nominally 4,096 epochs, approximately 18.2 days. An *epoch* is about 6.4 minutes. After the required service ends, applications and storage providers can continue keeping their own copies. [Current service and exact timing rules](docs/00-what-is-the-proposal.md#3-minimum-and-maximum-protocol-required-retention).

## The larger idea inside that mechanism

A rollup needs other people to obtain data it published. So does a broadcaster, an encrypted messaging application, a prover distributing working inputs, or a publisher seeding an archive. Their consumers do different things with the bytes, but they share a publication problem: make a particular object available for others to acquire and authenticate.

**The useful abstraction is a window of shared access to committed data.** A commitment gives the object a verifiable identity. Ethereum supplies publication and protocol-required availability. Application software supplies meaning: which bytes are a song, which ciphertext belongs in a mailbox, which inputs feed a computation, and which objects an archive should preserve.

That reading expands what blob capacity can be used to build. A browser can reconstruct and play a media segment. A recipient can retrieve a batch and decrypt a message. A prover can acquire an input, perform work, and publish a proof tied to the same committed object. A storage network can acquire a verified copy and continue serving it. Draft [ERC-8180, Blob Authenticated Messaging](https://eips.ethereum.org/EIPS/eip-8180), already explores application messaging over blobs; the broader application interpretation does not depend on variable retention being implemented first.

The architectural consequence is that Ethereum can anchor activity whose bulk data and processing live across many systems. Contracts handle the state and settlement that require shared execution. Blobs carry temporary working data. Applications perform computation and delivery. Storage networks preserve what deserves a longer life. These parts compose through commitments, proofs, and explicit handoffs. [The generalized data-plane argument](docs/06-what-does-a-generalized-data-plane-enable.md#20-why-the-scope-matters).

## Why the lifetime should become a choice

Once blobs are understood through these different uses, time becomes a first-class resource. A live stream's delivery window, an offline recipient's retrieval window, and a rollup's recovery window can have very different lengths. Giving every publication the same serving period ties those different needs to one storage obligation.

The Blobject's organizing principle is to **purchase the strength and duration of service the application needs**. Data can be valuable because it is available at the right time: long enough to be heard, copied, processed, challenged, or preserved elsewhere. Its role in the base network can finish while its consequences continue. A downloaded message can remain in an inbox; a proof can remain verifiable; an archive can keep serving a recording.

Making duration selectable would let these lifecycles be expressed directly in the resource purchase. Applications would choose a permitted window, and the network would account for both publication and the resulting storage obligation. The same idea underlies the RFC's discussion of more specialized forms of state: different uses call for different persistence and access guarantees. [Resource-strength principle and its lineage](docs/06-what-does-a-generalized-data-plane-enable.md#202-a-broader-resource-strength-principle).

## What an application would buy

The proposed service turns that philosophy into a publication with three parts:

| Part | What it means for the application |
|---|---|
| **Committed data** | A cryptographic commitment identifies the content and lets readers check the data they retrieve |
| **Publication** | The network distributes the data and establishes its availability under Ethereum's sampling rules |
| **A serving period** | Assigned nodes must retain and serve enough authenticated pieces for reconstruction until a specified expiry |

The RFC writes this as `DAService(C,B,T)`: commitment `C`, protocol-accounted quantity `B`, and duration `T`. In the version built around today's blob interface, applications purchase whole blobs and choose their duration. Small items can share a blob and its lifetime; larger application objects can span multiple blobs.

The purchaser selects a duration within the protocol's permitted range. The initial design would retain a full-service option and add shorter choices. The permitted minimum must cover Ethereum's own recovery needs; the application selects enough time for its readers and recovery paths. [Service definition and duration bounds](docs/00-what-is-the-proposal.md).

## What this makes available to applications

The common capability is a **shared publication and retrieval window**. During that window, an application's readers, relays, provers, or storage providers can acquire the committed bytes. The application determines what happens next.

| Application | What travels through the data service | How the application uses the window |
|---|---|---|
| **Live media and broadcast** | Media segments and associated application metadata | Listeners acquire segments for playback; caches and archives acquire copies for replay |
| **Encrypted messaging** | Batches of encrypted messages | Recipients discover batches, retrieve them, and decrypt their messages into a local inbox |
| **Computation and proofs** | Inputs, witnesses, or intermediate working data | A prover acquires the material, performs the computation, and publishes a compact result and proof |
| **Rollups** | Transaction batches and data needed to reconstruct state | Users, challengers, and nodes retrieve what they need for execution, verification, and recovery |
| **Persistent publication** | Objects destined for mirrors or storage networks | Independent providers acquire and verify copies before taking over longer-term service |

Ethereum would account for quantity and duration across these uses. Applications would supply their own formats, encryption, discovery, delivery behavior, and persistence arrangements. Encrypted bytes can use the same availability service as public bytes; recipients decrypt them with application-held keys.

This also gives large temporary inputs a role alongside compact durable state. An application could publish a dataset, let an off-chain process compute over it, and retain the resulting commitment, state update, or proof on Ethereum. The data's acquisition window and the result's useful life can be different. [Application space](docs/06-what-does-a-generalized-data-plane-enable.md) · [Temporary data and proofs](appendices/ephemeral-data-and-proofs.md).

### The two application case studies

**Blobcast / Radio Free Ethereum** provides the media example. Its prototype combines a publishing contract, media tools, and a browser tuner. Under the proposed service, a publisher would choose a window covering listener acquisition, late joins, and retries. A listener that has acquired a segment can play its local copy; an archive that acquires it can serve later replays. These are separate stages whose timing can be measured.

**BlobMail** provides the asynchronous example. Its experimental Sepolia client encrypts messages, publishes batches, discovers them through on-chain events, and verifies retrieved data before local decryption. Its relevant clock includes the time a recipient spends offline. The case study follows a message from publication through discovery and acquisition into the recipient's stored inbox, including recovery when an older batch has become unavailable.

These implementations are the starting points for the project's application experiments. [Case-study evidence and experiment plans](audits/application-use-case-review.md).

## How an object moves through the system

An individual publication creates a timed obligation, called a **lease** in the RFC. Its lifecycle is:

1. **Prepare and select.** The application packs its content into blobs, produces the commitments, selects a duration, and authorizes payment. Each published blob receives its own lease.
2. **Distribute and check capacity.** The data is encoded into pieces and distributed. The protocol checks that the publication fits its ingress and retention budgets.
3. **Accept and start the lease.** Block acceptance checks availability through the applicable data availability sampling rules. Canonical inclusion identifies the lease and anchors its clock, with expiry equal to inclusion time plus the selected duration. The duration includes any required initial availability phase.
4. **Retrieve and use.** Assigned custody nodes keep and serve their pieces. Applications obtain enough authenticated pieces to reconstruct the data, then play, decrypt, compute over, or copy it. Custody rules also govern maintaining the data as nodes fail or assignments change.
5. **Expire and hand off.** At expiry, Ethereum's required service for that lease ends. Capacity returns to use as the storage implementation reclaims it. Copies already held by applications, caches, or storage providers can continue serving their own purposes.

```text
Publisher prepares data and chooses a duration
                    |
                    v
       Ethereum publication and inclusion
                    |
                    v
       Required network serving window
          /             |             \
         v              v              v
   Reader acquires  Prover acquires  Archive acquires
   a local copy     working inputs   a verified copy
         |              |              |
         v              v              v
   Playback or      Computation      Continued
   decryption      and result       retrieval
```

Expiry changes who is required to provide service. It leaves applications free to keep their copies. A retained commitment lets a later reader authenticate a surviving copy. Applications that need longer-term retrieval would arrange an overlapping handoff: the next provider acquires and verifies the object while Ethereum's serving window is still open. [Lease accounting](docs/01-how-are-capacity-and-pricing-managed.md#41-non-normative-protocol-state-sketch) · [Persistence and handoffs](docs/04-what-happens-after-ethereum-retention-ends.md).

## How capacity and payment work

Publishing data consumes network resources in two ways. **Ingress** is the flow of new data through propagation, encoding, verification, and sampling. **Retention** is the stock of data the network continues to hold and serve over time. The proposed price separates these:

```text
publication price + retention price
```

Retention can be accounted for in **byte-time**: quantity multiplied by required duration. Holding the same quantity for half as long creates half the contracted byte-time. This is the resource distinction that lets a short-lived publication and a long-lived publication buy different amounts of service.

At any moment, the protocol can sum the quantities of all unexpired leases to calculate its active retained stock. A new lease occupies capacity immediately; its expiry releases the obligation. Admission limits bound both new publication and outstanding retention, with physical budgets for storage, serving traffic, repair, and I/O. Prices allocate demand within those limits. An accepted prepaid lease keeps its promised end time as prices change.

The intended benefit is to match storage obligations to the time applications need them. At a fixed publication rate, shorter durations reduce outstanding obligations. How much physical capacity becomes reusable depends on the representation and storage machinery described next. [Capacity accounting and pricing alternatives](docs/01-how-are-capacity-and-pricing-managed.md).

## How Ethereum would store and serve it

Ethereum distributes custody so that each participating node can hold a portion of the overall data. **PeerDAS** is the current approach to distributing and sampling these pieces. Nodes handle encoded cells, grouped into packages called column sidecars, which can contain pieces from several blobs published in one block.

Variable retention would give those pieces lifetimes derived from their blobs' leases. The implementation explored here would track which cells remain required, serve those cells with the information needed to authenticate them, and reclaim expired cells. Its storage and request formats would need to support that selective service efficiently. The protocol would also track live duties through recovery, reassignment, and repair.

The RFC separately explores a possible future **two-dimensional FullDAS** representation. This adds redundancy across blobs as well as within them. One proposed lifecycle uses the richer representation during initial availability, then keeps independently reconstructable rows for the remainder of their leases. Another approach groups objects with compatible expirations into shared coding structures. These are alternative implementation paths for the timed service. [PeerDAS and FullDAS design](docs/05-can-this-work-with-peerdas-and-fulldas.md) · [Hardware and operator capacity](docs/11-how-do-hardware-and-da-operator-markets-scale.md).

## The broader service and market design

Selectable duration is the base mechanism. The RFC also develops extensions that connect timed availability to publication scheduling, privacy, and longer-term storage:

| Extension | How it would work and what it would enable |
|---|---|
| **[Future publication and retention](docs/03-how-do-future-resource-markets-work.md)** | Reserve capacity for a later start time and a chosen serving period. Accounting would track overlapping future obligations, allowing applications to plan resource use ahead of publication |
| **[Private capacity authorization](appendices/private-aot-authorization.md)** | Acquire or transfer a capacity right privately, then activate a temporary public publication key. This explores separating the payer from the operational publisher while giving peers a cheap authorization check |
| **[Downstream retention agreements](appendices/retention-notes.md)** | Add storage arrangements whose duration follows application conditions, such as an authorized acknowledgement or cancellation. These would govern the provider's subsequent service |
| **[Early surrender and replacement](appendices/active-lease-surrender-and-novation.md)** | Allow an authorized holder to end an eligible lease early and return usable capacity for another publication, with explicit rules for beneficiaries and reclamation |
| **[Specialized storage operators](docs/11-how-do-hardware-and-da-operator-markets-scale.md#4-separate-scarcity-from-hardware-service)** | Explore how qualified operators could be paid for writes, retention, and service, and how capacity could be maintained through provider replacement |
| **[Lean Ethereum and sparse history](docs/10-how-does-lean-ethereum-change-the-proposal.md)** | Examine how timed payload availability could fit alongside other state and history designs, including permanent sparse records that anchor data retained elsewhere |

Together, these directions describe a network in which Ethereum supplies publication, authenticated data, bounded serving duties, and settlement, while applications and specialized networks provide routing, privacy, playback, computation, and persistence. [Generalized data-plane architecture](docs/06-what-does-a-generalized-data-plane-enable.md#20-why-the-scope-matters) · [Prior art and lineage](docs/07-what-is-the-prior-art-and-novelty.md).

## Which existing ideas this brings together

The proposal draws together several recognizable strands of Ethereum work. This map shows what each contributes and how it is used here; the [detailed source-to-design review](docs/07-what-is-the-prior-art-and-novelty.md#210-source-to-design-map) links the forum discussions and separates the base mechanism from optional extensions.

| Existing work | What the Blobject combines with it |
|---|---|
| **[New forms of state](https://ethresear.ch/t/hyper-scaling-state-by-creating-new-forms-of-state/24052)** | The principle of choosing persistence and access guarantees for the use case becomes a choice of required serving duration for published data |
| **[EIP-4844 blobs](https://eips.ethereum.org/EIPS/eip-4844) and [EIP-7594 PeerDAS](https://eips.ethereum.org/EIPS/eip-7594)** | Committed blob publication and distributed custody form the base; this RFC adds a purchaser-selected expiry and accounting for the resulting obligation |
| **[EIP-8136 cell deltas](https://eips.ethereum.org/EIPS/eip-8136), [EIP-8371 RowDAS](https://eips.ethereum.org/EIPS/eip-8371), and [1D/2D DAS research](https://ethresear.ch/t/revisiting-secure-das-in-one-and-two-dimensions/22762)** | Cell transport and row reconstruction inform selective historical serving. The proposed addition is tracking, serving, and reclaiming cells with different expiry times |
| **[FullDAS](https://ethresear.ch/t/fulldas-towards-massive-scalability-with-32mb-blocks-and-beyond/19529) and [FullDASv2](https://ethresear.ch/t/accelerating-blob-scaling-with-fulldasv2-with-getblobs-mempool-encoding-and-possibly-rlc/22477)** | Their richer coding structures motivate an optional transition from initial shared redundancy to retained rows with individual lifetimes |
| **[EIP-8256 Blob Streaming](https://eips.ethereum.org/EIPS/eip-8256) and [in-protocol gas futures](https://ethresear.ch/t/on-in-protocol-gas-futures/23698)** | Ahead-of-time propagation and future resource rights are paired with a serving duration and accounting for overlapping future leases |
| **[ERC-8179 Blob Space Segments](https://eips.ethereum.org/EIPS/eip-8179) and [ERC-8180 Blob Authenticated Messaging](https://eips.ethereum.org/EIPS/eip-8180)** | Application multiplexing and messaging make the general-purpose blob interpretation concrete; Blobcast and BlobMail supply the selected experimental workflows |
| **[EIP-8142 Block-in-Blobs](https://eips.ethereum.org/EIPS/eip-8142) and [distributed history/state research](https://ethresear.ch/t/integrated-in-protocol-distributed-history-and-state-storage/23522)** | The optional Lean/history analysis examines how protocol payloads, temporary availability, and permanent sparse records would be accounted for alongside application publications |

The wider review also connects [distributed publication and EIP-8070 Sparse Blobpool](docs/07-what-is-the-prior-art-and-novelty.md#216-fulldas-two-dimensional-coding-and-cell-level-transport), [storage markets and handoffs](docs/07-what-is-the-prior-art-and-novelty.md#214-downstream-retention-ethstorage), and [historical custody proposals](docs/07-what-is-the-prior-art-and-novelty.md#219-proofs-of-custody-and-retention-enforcement) to their respective design branches.

[Wikipethia](https://github.com/JossDuff/wikipethia), the Ethereum research corpus shared during the review, helped locate RowDAS, a retained-history custody discussion, and distinctions between propagation tickets and retention leases. The review cites the original EIPs and forum posts for those ideas. [Discovery record and specific additions](audits/wikipethia-review.md) · [Versioned references](REFERENCES.md).

## Research status

The Blobject is a proposal, not an implemented Ethereum feature. The models establish logical accounting results and explore illustrative allocation, custody, and pricing scenarios. Safe minimum durations, physical resource savings, application demand, and the economics of deployment remain to be measured. Blobcast and BlobMail supply concrete experimental workflows, not evidence that selectable retention is already deployed.

The next evaluation compares unchanged service, a small menu of durations, and arbitrary epoch choices under the same workload and recovery requirements. The detailed chapters cover rollup safety, exact serving boundaries, storage reclamation, failure recovery, and the separate requirements of each extension. [Research questions and experiments](docs/08-what-remains-to-be-proven.md) · [Rollup recovery requirements](docs/02-is-variable-retention-safe-for-rollups.md) · [Sources and verification dates](REFERENCES.md).

## Explore the repository

The [document map](docs/document-map.md) provides chapter-by-chapter navigation. The main components are:

| Location | Contents |
|---|---|
| [Proposal chapters](docs/00-what-is-the-proposal.md) | Service definition, resource accounting, implementation, applications, and extensions |
| [Worked appendices](appendices/illustrative-numerics.md) | Numerical examples and deeper treatments of proving, persistence, privacy, and markets |
| [Models](models/README.md) | Executable accounting and scenario models, tests, charts, and regeneration instructions |
| [Audit record](audits/2026-09-06-completion.md) | Findings, revisions, evidence review, and verification results |

With Python, PowerShell, and ripgrep installed, run the repository checks:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/validate-rfc.ps1
```

[Contribution and regeneration guide](CONTRIBUTING.md) · [Operator-market research questions](RESEARCH_TRACKING.md) · [Citation metadata](CITATION.cff) · [Viral Public License](LICENSE).
