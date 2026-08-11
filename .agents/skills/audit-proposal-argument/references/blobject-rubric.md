# Blobject proposal rubric

Use this rubric only for whole-proposal or cross-section work in this repository.

## Reader contract

The proposal should let a technically sophisticated Ethereum reader answer, in order:

1. What service is currently bundled?
2. Which dimension changes, and which guarantees remain fixed?
3. What is the minimal blob-compatible mechanism?
4. Why is contracted logical capacity bounded?
5. Under what physical representation does expiry release real resources?
6. What safety, recovery, operator, and network constraints remain?
7. Which extensions are optional or future-facing?
8. What must be proven before implementation is credible?

Flag ordering that asks the reader to accept downstream markets or applications before the base mechanism and its constraints are intelligible.

## Non-negotiable distinctions

Audit these terms for stable, non-interchangeable use:

- ingress flow versus retained stock;
- logical obligation versus physical resource consumption;
- publication-time availability versus post-publication serving;
- availability versus custody versus delivery;
- commitment or integrity anchor versus proof of continuous retrievability;
- current PeerDAS behavior versus proposed behavior;
- 1D prototype path versus conditional 2D lifecycle branch;
- spot-start obligation versus future-start commitment;
- safety cap or admission rule versus scarcity price versus operator payment;
- reduced retention versus increased ingress throughput.

## Epistemic labels

Require the prose to make these categories visible:

- **Established:** current EIP, specification, deployed behavior, or cited system.
- **Derived:** conclusion that follows from explicit assumptions or accounting.
- **Proposed:** mechanism or policy introduced by this RFC.
- **Conditional:** branch that matters only under a future architecture.
- **Illustrative:** toy model, numerical example, or non-normative sketch.
- **Open:** unresolved feasibility question, kill criterion, or experiment.
- **Speculative:** application or market enabled only if earlier layers work.

Do not let a citation near a proposed sentence make the proposed mechanism appear established.

## Central argument path

Test this dependency chain:

1. Ethereum bundles ingress with a fixed minimum serving horizon.
2. Applications may value different serving durations.
3. Selecting a duration no greater than today's horizon preserves the current maximum service while reducing logical required byte-time for shorter leases.
4. Active-stock accounting can bound spot-start contracted storage obligations.
5. Safe admission still depends on a multidimensional physical capacity vector.
6. Expiry helps physically only if coding, packaging, repair, and serving representations can release the relevant resources.
7. The conservative prototype therefore needs a representation-specific path under current 1D PeerDAS.
8. Rollups and other applications may use shorter horizons only when their recovery and proving assumptions tolerate them.
9. Future-start commitments, stronger enforcement, downstream persistence, and broader markets are extensions rather than prerequisites.

Flag any step that is absent, stated after dependents, or stronger than its support.

## Repeated high-risk claims

Check every occurrence, not just the canonical definition:

- "can only reduce" must remain scoped to logical protocol-required retained capacity with ingress fixed;
- "preserves today's service" must remain scoped to the permitted maximum duration and unchanged relevant guarantees;
- "available through T" must name the enforcement level and custody assumptions;
- "expiry releases capacity" must not omit representation-dependent physical feasibility;
- "global" or "permissionless" must not collapse into designated custody or named-recipient delivery;
- "proof" must state exactly what event or interval it proves;
- high-throughput claims must respect write-stream and network conservation.

## Cross-document consistency

Compare at minimum:

- README question, central claims, and suggested reading paths;
- `docs/00-*` executive framing and service abstraction;
- capacity/pricing claims in `docs/01-*`;
- safety and recovery claims in `docs/02-*`;
- physical-representation discussion across PeerDAS, FullDAS, hardware, and appendices;
- prior-art and novelty boundaries;
- open questions and kill criteria;
- conclusion language against every earlier qualification.

Treat appendices and executable models as support, not as places to hide premises required by the main argument.

## Completion test

A strong draft should satisfy all of the following:

- A skeptical reader can state the minimal proposal without mentioning optional markets.
- Each central claim has an explicit support type and calibrated confidence.
- The main text exposes every assumption needed to understand feasibility.
- The section order follows argumentative dependency, not research chronology.
- The conclusion introduces no unearned claim and preserves major qualifications.
- Open problems are decision-relevant and paired with a falsifiable check where possible.
- Terminology remains stable across the README, main sections, appendices, and figures.
