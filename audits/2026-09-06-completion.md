# Audit and revision record — September 6, 2026

Status: audit and staged local revisions complete. Independent technical and reader rechecks closed their actionable findings; remaining implementation questions are explicitly scoped research gates.

The author approved the [initial audit plan](2026-09-06-initial-audit-and-plan.md) and requested a self-contained GitHub README. Six specialist passes used Astra at low reasoning: [facts](facts-review.md), [mechanism](mechanism-review.md), [argument](argument-review.md), [models](models-review.md), [prose](prose-review.md), and [presentation](presentation-review.md). Their reports preserve the reviewed snapshots; finding locations may move in the revised files. The coordinator verified findings and made source changes.

## Checkpoint log

Subsequent reader-facing revisions add [Blobcast and BlobMail case studies](application-use-case-review.md), an explanation-led [project overview](../README.md), and a [source-to-design map](../docs/07-what-is-the-prior-art-and-novelty.md#210-source-to-design-map). The map makes the EIP/forum combinations and Wikipethia's specific discovery contributions explicit; the specialist reports below preserve their original review snapshots.

| Pass | Scope | Defect and revision | Verification / remaining risk |
|---|---|---|---|
| 1 | Initial assessment | Established thesis, nine findings, approved plan | Original 21 tests passed; deeper review needed |
| 2 | Six specialist audits | Source/logic/model/figure counterexamples collected | Reports distinguish base defects, branch defects, and acknowledged research gates |
| 3 | Technical correction | Physical versus logical bounds; legacy boundary; application timelines; receipt authority; gossip state; future coordinates; risk-tail arithmetic | Model regressions pass; complete integration check pending |
| 4 | Structure and prose | README rebuilt; conclusion narrowed; workload plan, notation, navigation and provenance improved | Independent reader review pending |
| 5 | Tooling and presentation | Heading checks; isolated regeneration; visible chart assumptions and layout fixes | Final rendered inspection and integration checks pending |
| 6 | Independent re-audit | Caught and corrected accumulated-risk underflow, exact-boundary rounding, and remaining cross-chapter scope drift | 29 model tests; independent numerical comparison and finding closure recorded in technical verification |
| 7 | User-supplied research lead | Queried Wikipethia at bounded depth; added RowDAS and historical retained-custody provenance | Ten searches plus context and original-source checks; no novelty certification |

Passes 3–5 were subsequently verified: all model/tool checks and isolated regeneration pass; all eight figures pass native CairoSVG inspection. Browser/GitHub rendering was not independently tested; exported typography was made portable after an initial SVG renderer failure.

## Core claim ledger

| Claim | Support type | Allowed conclusion / remaining evidence |
|---|---|---|
| Ethereum requires recent sidecar serving using a 4,096-epoch range | Pinned normative specification; current source check | Correct nominal baseline; exact full-service expiry mapping still open |
| Shorter durations reduce logical required stock at fixed publications | Indicator-function derivation | Logical inequality only; not total physical or economic dominance |
| Immediate starts can be bounded by active stock | Monotone-expiry accounting | Requires fixed envelope and separate physical admission/reclamation checks |
| Sparse 1D history can save resources | Compatibility hypothesis | Prototype and net physical measurements required |
| Shorter service is useful to applications | Conditional empirical prediction | Workload recovery timelines, demand and cost evidence required |
| Chosen prices allocate efficiently or stabilize demand | Candidate mechanism / fixed-arrival examples | No behavioral, equilibrium or welfare result established |
| Cold rows survive a given risk target | Independent-loss null model | Numerical result conditional on independence/full repair; not service security |
| FullDAS transition, tail service, futures, privacy, surrender, procurement work | Optional designs and research branches | Each requires its own interface, safety, incentive and empirical evidence |

## Finding dispositions

Locations in specialist reports describe their review snapshots. The following table records the final disposition, consolidating duplicate reports of the same defect.

| Finding IDs | Disposition |
|---|---|
| Initial 1; M03; ARG-04; reader safety shorthand | Corrected stock/physical safety claims throughout core summaries; separate physical admission remains mandatory |
| Initial 2; ARG-02/03/06; reader granularity | Separated base kills, duration-menu choice, representation branches and optional market gates; fractional pools no longer introduced as required |
| Initial 3; M04; PROSE-01/03 | Standardized start/duration/expiry notation, exclusive endpoints, and forward integration relative to current time |
| Initial 4 | Model README and state sketch now describe dictionary accounting, synthetic sizes/identity, both counters and limits of snapshot restoration |
| Initial 5; M05; MOD-01/02; TV-01/02 and CLI follow-up | Direct failure-tail calculation with Decimal checkpoint composition and consistent target decisions; assumptions visible; exact and high-precision regressions added |
| Initial 6; ARG-01/10 | README teaches the whole project with contextual links; conclusion narrowed; stable-path document map and previous/next navigation added |
| Initial 7; F-03; ARG-05 | Application expansion made conditional; workload/recovery evidence table and matched-comparison plan added |
| Initial 8; PRES-4 | Validator now checks local fragments, all chapter slots, and isolated regenerated artifacts; output reports actual scope; contributor instructions and tool regression tests added |
| Initial 9; PROSE-05/06/07 | Preserved useful directory layout; added provenance map and public editorial conventions; removed revision-history and marginal-capacity ambiguities; storage-only summary qualified |
| F-01 | Nominal 4,096-epoch horizon separated from legacy inclusive boundary; exact full-service mapping explicitly remains a deployment gate |
| F-02 | Rollup challenge-period conversions retained as arithmetic; unsafe implication of a universally sufficient 2,048-epoch class removed; direct BoLD sources added |
| F-04/05/06/07 | Dated EIP status notes; BlobMail/Blobcast descriptions pinned and updated; NVMe recommendation distinguished from requirement; historical slashable-signature claims narrowed |
| M01 | Sender-known secret explicitly permits cancellation and proves no recipient retrieval; downstream chapter corrected too |
| M02 | Canonical activation separated from peer-local quotas/replay history; bandwidth cannot roll back; fork uniqueness and repeated verifier costs qualified |
| M06/M07 | New-admission reductions cannot cancel outstanding service; old-data beneficiary floors and limits of off-protocol matching stated |
| M08; ARG-09 | In-window proving budget labelled sufficient for one policy; acquisition before expiry with retained witnesses permits later completion |
| MOD-03 | Simulator rejects truncated observations and derives enough default time for long billed leases; regression cases cover future arrivals and incomplete coverage |
| MOD-04 | Reserve explicitly measured relative to assigned physical capacity; original arithmetic preserved |
| ARG-07/08; reader novelty/compatibility | Narrow service/accounting contribution separated from extensions; transport neutrality now a target to test, not a universal implementation promise |
| PROSE-02/04; reader tail scope | Local node fraction and recurring payment distinguished from aggregate custody profile; lifecycle labels refer to duty ending rather than deletion |
| PRES-1/2/3/5; Figure 6 follow-up | Duration chart qualifications corrected, clipping removed, phase bands restored, standalone assumptions added, portable variable typography verified |
| W-01/02/03/04 | Added RowDAS and historical custody provenance; recorded mass-slashing and mempool-permission distinctions. Wikipethia is a discovery source, not protocol authority |

No known actionable P0/P1 remains within the reviewed scope. Acknowledged open research is not represented as solved: exact legacy mapping, safe floors, sparse-history interface, physical savings, correlated failures/repair, demand, and optional-market security still need implementation-specific evidence.

## Final validation and evidence

- **29 model tests and 3 documentation-tool tests pass.** New regressions cover numerical tails and boundary decisions, observation horizons, and heading-link failures.
- **10 published generated artifacts match isolated regeneration:** two CSVs and eight SVGs. Figure changes reflect labels/layout; the scenario numerical outputs remain reproducible.
- Local file/heading links, chapters 00–11, base section numbering, fences, narrow phrase guards and `git diff --check` pass.
- All eight final SVGs were rendered and inspected with CairoSVG. Before/final evidence is retained in `visual-qa/`; Figure 6's exporter defect was corrected and rechecked.
- [Technical verification](technical-verification.md) records independent numerical checks and closure. [Reader verification](reader-verification.md) confirms the README's self-contained reader objective and closes cross-chapter residuals.
- [Source audit](facts-review.md) records primary-source verification and limits. [Wikipethia pass](wikipethia-review.md) records ten searches, contextual retrieval, and original-source follow-through.

The revised argument is: selectable duration changes logical duty; physical representations determine whether that change saves resources; application recovery determines whether shorter duty is usable; matched experiments determine whether it warrants implementation. Optional branches neither prove that chain nor block its minimal experiment. The strongest remaining objection is that reducing byte-time may produce too little practical value to justify the complexity.

## Scope limits

No Ethereum client prototype, calibrated demand study, hardware benchmark, live application acceptance run, production cryptographic audit, or exhaustive novelty search was performed. Source checks used primary material and explicitly record failed retrievals and dated observations. No remote publication, issue creation, commit, or push is part of this local revision record.
