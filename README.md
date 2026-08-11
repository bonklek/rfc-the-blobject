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

The conservative proposal lets a purchaser choose a bounded protocol-required duration no longer than today's minimum serving horizon. That bound limits the obligation a purchaser can impose; it does not require nodes to delete or stop serving data afterward. The broader thesis combines timed bandwidth, timed retrievability, and downstream persistence into a generalized Ethereum data plane.

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

### Appendix

- [How could RetentionNotes work?](appendices/retention-notes.md)
- [What do illustrative retention frontiers look like?](appendices/illustrative-numerics.md)

## Suggested reading paths

- **Five-minute overview:** this README, then the [conclusion](docs/09-what-is-the-conclusion.md).
- **Protocol design:** proposal → capacity and pricing → PeerDAS/FullDAS compatibility → Lean Ethereum compatibility → open questions.
- **Applications and markets:** rollup safety → future markets → post-Ethereum retention → generalized data plane.

## Central claims

1. Under fixed ingress and a maximum protocol-required horizon no longer than today's minimum serving horizon, variable retention weakly reduces the logical retained-data obligation without requiring pruning afterward.
2. Current PeerDAS-style semantics are **protocol-required retrievability under custody assumptions**, not a recurring proof that every historical object remained available.
3. Immediate-start leases can use deterministic active-stock accounting; a forward capacity curve becomes necessary only for future-starting commitments, while physical admission must respect a resource vector.
4. Physical expiry is representation-dependent: 1D cell-level custody is the first prototype path, while hot-2D/cold-1D is one conditional branch rather than the assumed roadmap.
5. A single duration is the conservative special case of a broader lifecycle profile, and downstream systems may extend persistence after Ethereum's required-serving window ends.

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
- [Pinned references](REFERENCES.md)
- Kill questions: [2D parity lifetime](https://github.com/bonklek/rfc-the-blobject/issues/2), [row authentication](https://github.com/bonklek/rfc-the-blobject/issues/3), and [cold-custody survivability](https://github.com/bonklek/rfc-the-blobject/issues/4)

Run the repository checks with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/validate-rfc.ps1
```

## Citation and license

Citation metadata is provided in [`CITATION.cff`](CITATION.cff). This work is released under the [Viral Public License](LICENSE).
