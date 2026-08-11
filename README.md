# RFC: The Blobject

> Variable-retention data availability for Ethereum: decoupling bandwidth, storage, and time.

**Status:** Working draft / request for comment

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

The conservative proposal lets a purchaser choose a bounded duration without exceeding today's maximum serving horizon. The broader thesis combines timed bandwidth, timed retrievability, and downstream persistence into a generalized Ethereum data plane.

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

### Appendix

- [How could RetentionNotes work?](appendices/retention-notes.md)

## Suggested reading paths

- **Five-minute overview:** this README, then the [conclusion](docs/09-what-is-the-conclusion.md).
- **Protocol design:** proposal → capacity and pricing → PeerDAS/FullDAS compatibility → open questions.
- **Applications and markets:** rollup safety → future markets → post-Ethereum retention → generalized data plane.

## Central claims

1. Under fixed ingress and a maximum horizon no longer than today's, variable retention weakly reduces the logical retained-data obligation.
2. Immediate-start leases can be bounded by an active retained-stock ceiling; a forward capacity curve becomes necessary only for future-starting commitments.
3. Logical expiry creates physical savings only if the DAS representation permits independently expiring custody.
4. The leading compatibility hypothesis is a hot dense DAS phase followed by cold sparse row-local custody.
5. Ethereum can provide bounded availability and integrity while competing downstream systems provide longer persistence and application-specific services.

## How to comment

Open an issue with a concrete objection, missing prior art, counterexample, implementation constraint, or falsifiable experiment. The highest-value feedback is evidence that narrows or invalidates a claim.

## Repository layout

```text
.
├── README.md
├── docs/          # The RFC, split into question-focused sections
├── appendices/    # Worked constructions outside the base proposal
└── tools/         # Reproducible gist-to-repository import tooling
```

The numbered sections inside each document retain the original paper's numbering so citations and discussion remain stable.
