# RFC: The Blobject

> Variable-retention data availability for Ethereum: decoupling bandwidth, storage, and time.

**Status:** Working draft / request for comment

**Author:** Bonkle K

**Source:** Restructured from the original [research gist](https://gist.github.com/bonklek/2eb406003118bd1e29476e54cc18a0c7)

## The question

Why should every byte entering Ethereum data availability purchase the same amount of future serving?

Ethereum's DA roadmap principally scales how much data can be made available at once. The Blobject asks whether the duration of the protocol's serving obligation should also become a parameter of the service.

The proposal separates two resources:

```text
DA price = ingress price + retention price
```

- **Ingress** is the flow cost of propagating, encoding, sampling, and establishing availability.
- **Retention** is the stock cost of keeping committed data reconstructable through time.

The proposal lets a purchaser choose how long Ethereum must serve an object, up to today's minimum serving horizon. That upper bound limits the obligation a purchaser can impose. It is not a deletion deadline: nodes may keep and serve the data for as long as they choose. From that basic separation, the RFC also examines markets for future bandwidth, timed retrievability, and downstream persistence.

## Read by question

1. [What is the proposal?](docs/00-what-is-the-proposal.md)
2. [How are capacity and pricing managed?](docs/01-how-are-capacity-and-pricing-managed.md)
3. [Is variable retention safe for rollups?](docs/02-is-variable-retention-safe-for-rollups.md)
4. [How do future resource markets work?](docs/03-how-do-future-resource-markets-work.md)
5. [What happens after Ethereum retention ends?](docs/04-what-happens-after-ethereum-retention-ends.md)
6. [Can this work with PeerDAS and FullDAS?](docs/05-can-this-work-with-peerdas-and-fulldas.md)
7. [What does a generalized Ethereum data plane enable?](docs/06-what-does-a-generalized-data-plane-enable.md)
8. [What is the prior art, and what is novel?](docs/07-what-is-the-prior-art-and-novelty.md)
9. [What remains to be proven?](docs/08-what-remains-to-be-proven.md)
10. [What is the conclusion?](docs/09-what-is-the-conclusion.md)
11. [How does Lean Ethereum change the proposal?](docs/10-how-does-lean-ethereum-change-the-proposal.md)
12. [How do hardware and DA operator markets scale?](docs/11-how-do-hardware-and-da-operator-markets-scale.md)

### Appendix

- [How could RetentionNotes work?](appendices/retention-notes.md)
- [What do illustrative retention frontiers look like?](appendices/illustrative-numerics.md)
- [What do illustrative operator payments and controllers look like?](appendices/illustrative-operator-economics.md)
- [What are the backbone-scale limits?](appendices/backbone-scale-limits.md)
- [What can be proven after ephemeral data expires?](appendices/ephemeral-data-and-proofs.md)
- [How could private AOT authorization remain cheap to validate?](appendices/private-aot-authorization.md)

## Suggested reading paths

- **Five-minute overview:** this README, then the [conclusion](docs/09-what-is-the-conclusion.md).
- **Protocol design:** proposal → capacity and pricing → PeerDAS/FullDAS compatibility → hardware and operator markets → Lean Ethereum compatibility → open questions.
- **Applications and markets:** rollup safety → future markets → post-Ethereum retention → generalized data plane.
- **Physical and proving limits:** hardware/operator markets → backbone-scale limits → ephemeral data and proofs → open questions.

## Central claims

1. With ingress held fixed, allowing shorter serving windows can only reduce the logical retained-data obligation. Nothing in the proposal requires nodes to prune afterward.
2. PeerDAS currently provides **protocol-required retrievability under custody assumptions**. It does not repeatedly prove that every historical object remained available.
3. A lease that starts immediately can be accounted for as active stock. A forward capacity curve is needed only for commitments that start in the future, and physical admission must account for more than storage alone.
4. The conservative EIP-4844 path remains blob-granular: applications buy an integer number of whole blobs, while retention duration is selected per blob commitment. The RFC's `B` is an accounting quantity, not an existing arbitrary-byte purchase interface.
5. Whether logical expiry saves physical resources depends on the representation. The first prototype path is 1D cell-level custody; hot-2D/cold-1D is a conditional branch, not an assumed roadmap.
6. One expiry is the simplest lifecycle. Later designs may add reduced-strength tails, and downstream systems may continue persistence after Ethereum's required-serving window ends.
7. At high throughput, shorter retention reduces resident stock but not the write stream seen by each node. If Ethereum pays specialized hardware providers, scarcity pricing and payment for qualified service should remain separate.
8. Retention does not relax network conservation. Global throughput, coding and replication overhead, operator count, and sustainable per-node bandwidth must fit one consistent architecture.
9. The proposal varies the **duration** of Ethereum's global DA service, not its network scope: custody by a designated population and delivery to one recipient are distinct, narrower claims unless they support permissionless reconstruction under the stated DAS assumptions.

## How to comment

Open an issue with a concrete objection, missing prior art, counterexample, implementation constraint, or falsifiable experiment. The highest-value feedback is evidence that narrows or invalidates a claim.

## Repository layout

```text
.
├── README.md
├── docs/          # The RFC, split into question-focused sections
├── appendices/    # Worked constructions outside the base proposal
├── models/        # Executable stock, pricing, and cold-custody null models
├── REFERENCES.md  # Date- and commit-pinned research inputs
└── tools/         # Repository validation
```

The numbered sections inside each document retain the original paper's numbering so citations and discussion remain stable.

## Research artifacts

- [Toy protocol state and capacity model](docs/01-how-are-capacity-and-pricing-managed.md#41-non-normative-protocol-state-sketch)
- [Executable models](models/README.md)
- [RFC figure renderer](tools/render-rfc-figures.py)
- [Pinned references](REFERENCES.md)
- [Backbone-scale arithmetic](appendices/backbone-scale-limits.md)
- [Ephemeral proving semantics](appendices/ephemeral-data-and-proofs.md)
- [Private AOT authorization sketch](appendices/private-aot-authorization.md)
- [Illustrative operator economics and procurement controller](appendices/illustrative-operator-economics.md)
- [Issue-ready operator-market kill questions](RESEARCH_TRACKING.md)
- Kill questions: [2D parity lifetime](https://github.com/bonklek/rfc-the-blobject/issues/2), [row authentication](https://github.com/bonklek/rfc-the-blobject/issues/3), and [cold-custody survivability](https://github.com/bonklek/rfc-the-blobject/issues/4)

Run the repository checks with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/validate-rfc.ps1
```

## Citation and license

Citation metadata is provided in [`CITATION.cff`](CITATION.cff). This work is released under the [Viral Public License](LICENSE).
