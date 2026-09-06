# Initial audit and proposed improvement programme

Date: 2026-09-06. Historical snapshot of the initial assessment, before specialist review or source edits. The author subsequently approved this plan; see the [completion record](2026-09-06-completion.md) for execution and dispositions.

## Assessment

The RFC has a defensible, narrow accounting thesis, but its research agenda is much broader than the evidence currently supporting implementation. Its main editorial problem is accumulated qualifications and extensions: these protect individual sentences while making the overall proposal harder to evaluate. The next revision should improve the argument's hierarchy and evidence, rather than add features or simply shorten sentences.

**Thesis:** Let purchasers select a blob's required serving duration, bounded by the existing maximum service offered. With the same publications and ingress, shorter durations reduce logical required byte-time. Whether this yields useful physical savings without weakening required service depends on representation, custody, reclamation, and application recovery constraints.

**Argument skeleton:** bundled fixed service → heterogeneous application needs → selectable duration → bounded immediate-start logical stock → representation-specific physical admission → application safety → measured benefit over simpler alternatives. Future markets, operator procurement, private authorization, and generalized data-plane applications are branches.

**Steelman:** The logical inequality is a useful starting point for a bounded experiment: compare fixed and selectable serving horizons under the same workload and custody guarantees.

**Strongest objection:** Reducing contracted byte-time is insufficient justification for protocol complexity. If storage is not the binding constraint, safe application horizons are nearly uniform, or sparse serving and reclamation cost more than they save, the mechanism may offer little practical value. More elaborate markets cannot rescue that missing evidence.

## Prioritized initial findings

These are reconnaissance findings, not a complete security, source, code, or visual audit. P1 denotes a material argument/structure defect; P2 a support or consistency defect; P3 expression or maintenance. No P0 contradiction invalidating the whole proposal has been established.

### 1. P1 — The physical-safety qualification disappears in a downstream summary

At `docs/02-is-variable-retention-safe-for-rollups.md:78`, hard active-stock bounds are said to protect physical safety. In `docs/01-how-are-capacity-and-pricing-managed.md:212`, physical admission correctly requires storage, serving, repair, and I/O bounds. A scalar logical-stock cap does not independently establish those bounds.

**Revision:** Say that the stock cap bounds logical contracted stock; physical safety requires the full admission envelope. Search every summary, caption, and conclusion for the same inference. This matters because readers often carry away the summary rather than its earlier qualifications.

### 2. P1 — The proposal's falsification target shifts between variable and continuous retention

`docs/08-what-remains-to-be-proven.md:5` defines a proposal kill in terms of continuous variable retention. Its simpler-design dominance test would favor two or three maturity classes, which remain purchaser-selected variable retention. Meanwhile `docs/01-how-are-capacity-and-pricing-managed.md:116` leaves the allowed maturity set open, and its deployment alternatives retain classes as a fallback.

**Revision:** Separate rejection of selectable native duration from rejection of arbitrary duration granularity. Name the target of each experiment: fixed horizon versus duration menu; duration menu versus arbitrary epoch choices; 1D representation versus conditional 2D branch. A successful simplification should not be reported as disproving the broader mechanism.

### 3. P2 — Duration and absolute expiry share one symbol

`docs/00-what-is-the-proposal.md:71` calls `T` an expiration, while line 84 defines it as elapsed duration from inclusion. The capacity derivation uses expiry `t+T`; the cold-custody discussion uses remaining duration.

**Revision:** Define total duration, absolute expiry, and remaining duration separately. Carry the convention into formulas, service signatures, captions, and model interfaces. Also align the inclusive horizon at `docs/01-how-are-capacity-and-pricing-managed.md:34` with the implementation's exclusive expiry boundary.

### 4. P2 — The implementation description has drifted from the model

`models/README.md:7` describes an epoch ring. `models/stock.py:131` scans and filters a dictionary of objects. `docs/01-how-are-capacity-and-pricing-managed.md:111` mentions a ring buffer and `retained_bytes`, although the nearby pseudocode uses queues and `obligated_bytes`. The model's `admit_blob` also accepts caller-supplied sizes, while the conservative protocol sketch derives a fixed blob quantity.

**Revision:** Describe the actual abstract model, distinguish it from a protocol-faithful adapter, and align the state vocabulary. Do not introduce a ring buffer merely to make an obsolete description true. State which invariants the tests establish and which interface rules they do not test.

### 5. P2 — Cold-custody results need their assumptions attached to the output

`models/cold_custody.py:22` only constrains replicas to the population size; line 29 assumes independent cell survival. Reproduction: two cells, reconstruction threshold one, one custodian, one replica, failure probability 0.1 produces approximately **0.99** survival. If that sole custodian holds both cells, survival is **0.9**. Independent custodian failures do not imply independent cell failures when assignments overlap.

The discussion in `docs/05-can-this-work-with-peerdas-and-fulldas.md` already acknowledges the simplification. This is an applicability limitation, not a newly discovered proof that the stated abstract formula is wrong.

**Revision:** Label CLI results and `meets_target` as conditional on independent cell-loss events and successful repair. Add a shared-custodian counterexample and distinguish assignment-aware experiments from the existing null model. Audit the phrase “conservative checkpoint approximation”: conservatism needs explicit assumptions or a bound.

### 6. P1 — The reading structure still follows the project's expansion

`README.md:48` explicitly says numerical order is not the recommended argumentative order. The conclusion revisits operator payments, backbone traffic, ephemeral proofs, and forward markets. The opening proposal chapter is approximately 3,950 whitespace-delimited words; the conclusion plus source recap is approximately 1,226. The offered five-minute path is poorly matched to the amount and complexity of material.

**Revision:** Create one canonical short core path with explicit previous/next navigation, a compact mechanism specification, and links to optional branches. Retain existing paths and anchors initially. Reduce the conclusion to what follows, what does not yet follow, and the next decisive experiment. Move its repeated source inventory to the reference apparatus.

### 7. P2 — The central demand and value premises remain research questions

The short-duration motivation is clearly marked illustrative, but it is not yet a workload-derived case for changing Ethereum. `docs/02-is-variable-retention-safe-for-rollups.md` appropriately limits retention elasticity; the pricing simulation explicitly holds arrivals fixed and does not model willingness to pay.

**Revision:** Build a workload table stating the actor, use case, required recovery path, safe duration evidence, alternative service, and physical resource likely to bind. Separate illustrative application scenarios from measured demand. Compare the base mechanism with unchanged service and a small maturity menu before extending markets. Do not present fixed-arrival fee comparisons as evidence of behavioral stabilization.

### 8. P2 — Validation success is narrower than its closing message suggests

`tools/validate-rfc.ps1:8` checks numbered base sections only in chapters 00–09 and appendices. Its link regex checks file existence but discards fragment identifiers; pure fragment links are skipped. Two prohibited phrases are not a semantic claims audit. The command does not regenerate outputs or visually inspect figures.

**Revision:** Report distinct check coverage, explicitly handle extension structure, validate heading targets, and compare generated outputs in a temporary directory. Keep source verification and semantic review separate from mechanical checks. Avoid broad assurances that all “claims” were validated.

### 9. P3 — Repository organization and prose need consolidation rather than wholesale relocation

The `docs/`, `appendices/`, `models/`, and `tools/` split is sensible. The friction comes from two reading orders, mixed numbering systems, two generated-figure locations, and a generically named `RESEARCH_TRACKING.md` that tracks only operator-market questions. `.agents/` is ignored, so the useful argument rubric is local rather than a contributor-visible standard. `docs/01-how-are-capacity-and-pricing-managed.md:202` refers to an “old forward-curve presentation,” requiring knowledge of revision history.

**Revision:** Add a canonical document/output manifest, scope the research tracker accurately, identify generated assets and regeneration commands, and consider a public editorial rubric. Replace revision-history references with self-contained reasoning. Consolidate repeated disclaimers at authoritative definitions while retaining qualifications where a local claim would otherwise mislead. Do not renumber or move cited documents without a link-preservation plan.

## Evidence and limitations

- Ran the documented `tools/validate-rfc.ps1`: passed, including **21 Python tests** and `git diff --check`.
- Inspected the entry point, core mechanism and capacity text, rollup safety, conclusion, kill criteria, reference inventory, model documentation, stock and cold-custody implementations, validator, and repository structure. Other chapters and appendices received structural or targeted inspection, not exhaustive review.
- Confirmed the 4,096-epoch data-column request-window constant against the RFC's [pinned mainnet configuration](https://raw.githubusercontent.com/ethereum/consensus-specs/3cbd26f048237250e3373d4d0a651a647b4c58e1/configs/mainnet.yaml). Inspected the official [PeerDAS EIP](https://eips.ethereum.org/EIPS/eip-7594) and [cell-level delta EIP](https://eips.ethereum.org/EIPS/eip-8136) as source reconnaissance. This is not verification of every present-tense statement or proof of sparse historical-serving compatibility.
- References identify an August 11 research baseline. Full review must distinguish correctness against those pins from changes since that baseline. Age alone does not make a claim false.
- Reproduced the custody counterexample above. No client benchmark, adversarial custody experiment, complete novelty search, external-link sweep, or rendered visual audit has been performed.

## Full audit proposed for approval

All specialist subagents will use **`gpt-6-astra` with `reasoning_effort: low`**, as requested. Run at most three specialists concurrently, leaving the fourth slot for the coordinating agent. Each receives the rubric, explicit files, the thesis and scope boundaries, and a bounded output contract. Specialists audit read-only; the coordinator verifies findings and owns revisions to avoid conflicting edits.

| Wave | Specialist | Assignment and required result |
|---|---|---|
| 1 | Facts and provenance | Verify load-bearing external claims against pinned primary sources; compare current versions separately. Deliver claim-to-source ledger, exact supporting passages, dates, and unsupported or overstated claims. |
| 1 | Mechanism and safety | Audit lease identity, timing, reorgs, custody, pruning, repair, admission, and application recovery. Deliver invariant/dependency map, concrete failure cases, and distinctions between base and branch blockers. |
| 1 | Argument and rhetoric | Reverse-outline the whole proposal; test the thesis, novelty wording, premise order, audience assumptions, and benefit-to-evidence alignment. Deliver a proposed core outline and prioritized moves, cuts, and rewrites. |
| 2 | Models and economics | Check formulas, units, numerical stability, model/text agreement, incentives, and what experiments actually establish. Reproduce meaningful counterexamples and generated numerical outputs in isolation. |
| 2 | Prose and terminology | Review all reader-facing prose for ambiguity, redundancy, overstatement, notation drift, paragraph purpose, and transitions. Deliver a terminology sheet and representative edits after considering the argument findings. |
| 2 | Filesystem and presentation | Audit navigation, anchors, numbering, generated artifacts, contribution workflow, validation coverage, and rendered figures for readability, units, labels, and misleading visual implications. Deliver a minimal organization plan and verified defects. |
| 3 | Independent verification | Use two Astra-low reviewers: one checks technical corrections and evidence; one reads the revised core for coherence and scope. They challenge the coordinator's resolutions and look for regressions. |

Every finding must include an ID, severity, file/line location, minimal evidence or reproduction, consequence, recommended correction, confidence, and support status. Reviewers must identify material they did not inspect and avoid re-reporting acknowledged limitations without explaining the remaining defect. Unresolved disagreements remain visible.

### Improvement sequence after approval

1. Establish a coverage manifest and claim ledger; complete the two discovery waves and reconcile findings before broad rewriting.
2. Correct validity, safety, notation, and model/document inconsistencies first. Preserve the author's thesis where the evidence permits it; record substantive unresolved design choices.
3. Reorganize the core argument and branch navigation while preserving cited paths and anchors. Align the introduction, claims summary, kill criteria, and conclusion.
4. Improve evidence calibration, prior-art comparisons, and experimental decision criteria. Do not invent demand measurements or silently convert speculative choices into settled design.
5. Perform prose and figure revisions, then make the smallest justified filesystem and validation changes.
6. Run documented checks, targeted counterexample tests, isolated artifact regeneration, heading/link validation, and visual QA. Review the diff for equation, unit, citation, and scope regressions.
7. Obtain independent re-audits; repeat bounded correction and verification where material defects remain. Deliver the revised project, finding/disposition ledger, coverage report, validation evidence, and remaining research decisions.

**Completion standard:** Every major claim has a support classification; no known unaddressed validity or structural defect remains without an explicit disposition; the minimal mechanism can be understood without optional markets; model claims match model behavior; the artifacts and links pass their applicable checks. A research question may remain open, but it must have a clearly scoped claim and decision-relevant next test. Audit completion does not establish protocol readiness.

**Approval scope:** Execute this full audit and staged local revisions. No publication, GitHub issue creation, remote changes, or physical/client research programme is included. This sign-off boundary follows the author's request to review the plan after the initial audit.
