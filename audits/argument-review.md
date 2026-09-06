# Argument and rhetoric review

Date: 2026-09-06. Mode: read-only source audit. Reviewed README, all twelve chapters, and all seven appendices. Only this report is written. Read the local argument skill, its Blobject rubric, and the initial audit. No repository AGENTS.md was found. External citations were inspected as argumentative support labels, not independently verified; the provenance specialist owns source correctness. No novelty search or client experiment was performed.

## Thesis, dependency model, and strongest objection

**Defensible thesis:** Ethereum could let each blob publication select a bounded required-serving duration while keeping publication-time availability and the relevant service guarantees fixed. For the same publications and ingress, durations no longer than the existing fixed horizon cannot increase logical required byte-time. Whether this warrants a protocol change depends on safe application minima and measured net physical benefit under an implementable custody and serving representation.

**Argument:** fixed bundled service → heterogeneous useful lifetimes (unmeasured premise) → per-publication bounded duration → immediate-start stock accounting (derived) → representation and physical admission (open implementation) → application recovery floors (conditional suitability) → comparison with unchanged service and a small duration menu (decisive evaluation).

**Steelman:** The accounting result usefully isolates a concrete experiment: compare fixed and selectable duration under matched workloads, service guarantees, hardware targets, and custody assumptions. A positive result need not require arbitrary epoch granularity or a new provider market.

**Strongest objection:** The inequality removes an obligation by definition. It does not show that the obligation was costly, that users can safely relinquish it, or that implementing its removal saves more than it costs. If network/writes bind, safe durations are nearly uniform, or sparse historical serving introduces greater repair/request overhead, the proposal may have little practical value. Elaborate markets cannot supply the missing evidence.

No new whole-proposal P0 invalidity is established. The main defects concern what must be built, what would falsify the thesis, and whether the entry point actually explains the project.

## Prioritized findings

### ARG-01 — P1: README acts as an index before it teaches the mechanism

**Locations:** README.md:28, :46, :73, :80. **Evidence:** two complete reading orders and an appendix inventory precede the central claims; the five-minute path delegates understanding to the conclusion. Terms such as active stock, canonical publication, 1D custody, hot-2D/cold-1D, and forward curves appear in a ten-item claims list without a worked lifecycle. **Consequence:** a technically capable reader unfamiliar with the research history can understand the motivation but cannot explain the proposed state transition or the main feasibility test without opening several long chapters.

**Fix:** make README a self-contained project explanation with contextual hyperlinks at the point of detail. Explain one blob from publication to expiry; distinguish logical savings from physical savings; explain who may safely choose shorter duration; summarize evidence and next experiment. Put one compact grouped document index afterward. Give optional branches one paragraph each at most. Do not solve this by making another overview document or by deleting the useful core qualification. **Confidence:** high. **Support status:** directly observed structure; matches the user's explicit GitHub README requirement.

### ARG-02 — P1: Optional research questions accidentally become base-EIP gates

**Location:** docs/08-what-remains-to-be-proven.md:146; compare §§22.5, 22.7, 22.9, 22.10. **Evidence:** “An implementation EIP should wait until these questions” follows futures, persistence markets, private activation, and surrender alongside core gates. **Consequence:** the closing decision rule contradicts the repeated statement that those extensions are not prerequisites. A reader could reasonably conclude that a base experiment must solve private AOT and novation first.

**Fix:** state that a base implementation requires the applicable accounting, recovery, representation, service, and economic-value gates; each optional branch has additional gates only if selected. A small base/branch/gate table would clarify this more effectively than further disclaimers. **Confidence:** high. **Support status:** direct cross-document inconsistency.

### ARG-03 — P1: Falsification target moves from selectable duration to arbitrary duration

**Locations:** docs/08-what-remains-to-be-proven.md:5 and §22.0; docs/01-how-are-capacity-and-pricing-managed.md:356; docs/00-what-is-the-proposal.md §3. **Evidence:** §3 leaves the allowed duration set open, but the kill criteria define the base as continuous variable retention; two or three classes are a proposal kill although they implement purchaser-selected variable retention. **Consequence:** success of the simplest prototype can be described as failure of the central proposal, while arbitrary granularity receives privileged status before demand is measured.

**Fix:** separate three decisions: fixed versus selectable native duration; small menu versus arbitrary epochs; current 1D path versus conditional 2D lifecycle. Describe classes as a candidate base implementation, not only a defeated-design fallback. Preserve continuous duration as a research option if desired. **Confidence:** high. **Support status:** confirmed initial finding, independently traced across framing and kill criteria.

### ARG-04 — P1: The scalar-to-physical inference survives in summaries

**Locations:** docs/00-what-is-the-proposal.md:273; docs/02-is-variable-retention-safe-for-rollups.md:78; compare docs/01 §6 and docs/05 §17.8. **Evidence:** “bound the physical obligation” and “protect physical safety” are attributed to an active-stock ceiling. **Consequence:** the correct multidimensional qualification disappears exactly where a reader is likely to compress the argument.

**Fix:** use “bounds contracted logical stock”; physical safety depends on the representation-specific admission envelope, service workload, and reclamation margin. Audit the analogous shorthand in docs/01 §5.1, where the stock cap is said to solve the physical-safety job. **Confidence:** high. **Support status:** confirmed initial finding plus an additional opening-chapter occurrence.

### ARG-05 — P2: Benefit conclusions outrun the explicitly illustrative demand evidence

**Locations:** docs/06-what-does-a-generalized-data-plane-enable.md:191; docs/03-how-do-future-resource-markets-work.md:231; docs/06 §19.1. **Evidence:** the application range “expands substantially,” while prototypes establish “design pressure”; variable retention “strengthens” the replication opportunity although its proposed change is shortening or selecting the required horizon. **Consequence:** the main speculative-benefit chapter closes more confidently than its own evidence permits. Existing fixed service already supplies the replication opportunity.

**Fix:** say selectable service could make short-lived workloads more economical if native cost savings reach purchasers; say it lets a publisher purchase a shorter replication window. Add a compact workload/evidence table: actor, raw-data dependency, safe-duration evidence, alternative service, binding physical resource, and what must be measured. Keep the two prototypes as motivation, not validated demand. **Confidence:** high. **Support status:** internal claim/evidence mismatch; no claim that the proposed use cases are infeasible.

### ARG-06 — P2: Fractional pools are introduced as a necessary architectural constraint

**Location:** docs/11-how-do-hardware-and-da-operator-markets-scale.md:14. **Evidence:** the first three listed items are called architectural constraints; the third is “decompose large logical custody duties across fractional operators.” The base may retain current custody operators and unchanged ingress. **Consequence:** an optional supply architecture becomes a hidden premise of the core reading path, which routes readers through this long chapter.

**Fix:** distinguish universal constraints (writes, placement costs, assignment granularity) from optional responses (tiering, fractional pools, separate procurement). Link the core reader directly to hardware constraints and summarize them in the physical chapter; leave pools and procurement in the extension path. **Confidence:** high. **Support status:** scope inference supported by the chapter's own baseline and deployment sequence.

### ARG-07 — P2: Novelty is reasonably hedged but the claimed composition is broader than the demonstrated core

**Locations:** docs/07-what-is-the-prior-art-and-novelty.md:5 and §21.10. **Evidence:** opening novelty combines duration, byte-time pricing, and DAS; the final contribution adds future markets and representation-aware custody. Pricing is not selected, representation compatibility is open, and futures are optional. **Consequence:** a reader may evaluate novelty against a moving bundle rather than the narrow research contribution.

**Fix:** lead with the proposed native service/accounting decomposition; separately label representation compatibility investigations and future-market extensions. Keep the bounded “not aware” formulation and research cutoff. A comparison matrix of native duration selection, pricing basis, current versus proposed enforcement, and network scope would be more useful than a stronger priority claim. **Confidence:** medium-high. **Support status:** rhetorical scope finding; novelty itself remains unverified and must not be asserted or denied by this audit.

### ARG-08 — P2: Conditional compatibility sometimes becomes an architectural promise

**Location:** docs/00-what-is-the-proposal.md:112. **Evidence:** PeerDAS, FullDAS, and a future continuous fabric “should all be capable of implementing the same semantic service”; later sections correctly make this a compatibility hypothesis. **Consequence:** transport neutrality of the interface is mistaken for existence of a compliant implementation across transports.

**Fix:** describe one semantic target against which candidate representations are tested. The interface can remain stable even when a representation fails the target. Also replace the “must simply avoid” wording in docs/06:37 with the actual unresolved distributed-publication obligations already listed in §17.9. **Confidence:** high. **Support status:** internal confidence mismatch.

### ARG-09 — P2: A sufficient proving schedule is presented as a universal necessity

**Location:** appendices/ephemeral-data-and-proofs.md §C.4, especially :113 and the `T_service > T_fetch + T_prove + T_settle + H` condition. **Evidence:** the appendix first requires acquisition and completion before all usable copies expire, then substitutes Ethereum's serving window for the lifetime of those copies. A prover that acquires and retains its own input can finish after Ethereum's duty ends. **Consequence:** the timing floor is stronger than the stated mechanism requires and may understate retention elasticity for a central non-rollup use case.

**Fix:** label the inequality as a conservative application policy when the application requires proof completion/settlement while native reacquisition remains available. The general requirement is acquisition before the relevant service ends and continued access to a usable copy until proving/retries finish; applications may deliberately require independent repeatability longer. Do not claim that fast proving alone removes recovery requirements. **Confidence:** high. **Support status:** deduction from the appendix's own distinction between native service and surviving copies; coordinate technical review before source change.

### ARG-10 — P3: The conclusion and compatibility note retain revision-history scaffolding

**Locations:** docs/09 entire conclusion and research-source recap; docs/10-how-does-lean-ethereum-change-the-proposal.md:242; docs/01 §5.1; docs/04 §16. **Evidence:** conclusion reintroduces detailed operator rates, continuous frames, ephemeral proving, and futures; Lean note says the proposal “needs five bounded revisions,” several already integrated; “old forward-curve presentation” and “former 64 TiB example” require editorial history. **Consequence:** the final takeaway expands again after the proposal has carefully narrowed its core, and readers cannot tell whether the compatibility changes are pending.

**Fix:** conclude in four short movements: what is proposed, what is derived, what remains unproved, next decisive comparison. Link optional implications. Turn historical editing instructions into current compatibility boundaries. Move source recap responsibility to references/prior art rather than maintaining another inventory. **Confidence:** high. **Support status:** directly observed redundancy and temporal ambiguity; do not mass-edit repeated necessary qualifications.

## Major-claim ledger

| Claim / role | Classification | Support and allowed confidence | Disposition / missing check |
|---|---|---|---|
| Current service bundles ingress and fixed minimum serving | Externally established premise | EIP/spec citations, subject to provenance review | Keep with dated baseline; distinguish minimum from deletion deadline |
| Applications may need different native durations | Empirical premise | Scenarios and prototype design pressure | Keep conditional; obtain workload and recovery traces |
| Purchaser selects bounded duration per canonical publication | Proposed design | Service abstraction and state sketch | Keep as base; choose allowed set later |
| Same workload and shorter durations cannot increase logical stock | Deduction | Indicator-sum proof in §3.2 | Keep strong confidence within stated premises |
| Immediate-start contracted occupancy needs no forward curve | Deduction | Already-admitted leases only expire | Keep; future commitments and changing physical envelope have separate accounting |
| Stock cap assures physical safety | Unsupported inference as locally phrased | Conflicts with resource vector and reclamation discussion | Correct ARG-04 |
| Price may be decomposed into ingress and retention | Design choice / economic accounting | Distinct resource use; several pricing candidates | Keep schematic; not estimated market price or a proven controller |
| Short duration can stabilize demand | Behavioral hypothesis | Plausible feedback plus countervailing behaviors | Retain conditional; fixed-arrival models do not test elasticity |
| Sparse 1D historical service can release storage | Compatibility hypothesis | Cell transport precedent and packaging argument | Benchmark; do not imply existing sparse expiry support |
| Hot-2D/cold-1D can preserve guarantees | Conditional compatibility hypothesis | Handoff invariant and five conditions | Keep branch; failure does not reject 1D/selectable duration |
| Independent-cell custody formula meets target | Illustrative null model | Binomial derivation and repeated intervals | Keep conditional; independence/repair labels at point of result; no security certificate |
| Rollup minima differ | Conditional application constraint | Recovery reasoning and challenge-window citations | Keep; payer/user distinction is useful and should remain |
| External storage extends but cannot shorten native duty | Deduction from service boundary | Explicit overlapping handoff | Keep; it can enable an application to choose shorter native duty under new trust assumptions |
| Receipt secret proves intended recipient retrieval | Proposed application condition | Secret possession | Narrow to secret possession; sender also chose secret; not standalone delivery proof |
| Expiry preserves integrity/proved results but not lost data | Deduction under cryptographic assumptions | Commitment/proof semantics | Keep; separate sufficient native-window policy from necessary proving lifetime |
| Backbone throughput follows storage frontier | Illustrative conditional relationship | `R=S/T` and separate conservation bounds | Keep storage-only label; not total throughput capability |
| Fractional pools broaden credible supply | Empirical prediction / optional mechanism | Arithmetic and adjacent sharding precedent | Test independence, coordinator failure, serving and repair; no decentralization inference from identity count |
| Posted procurement can recruit safe supply | Optional control hypothesis | Toy bounded update and candidate qualification | Compare to current duties and alternatives; no oracle claim |
| Public activation preserves useful payer privacy | Speculative extension | ZK/canonical-allowlist sketch with leakage model | Keep branch; assess end-to-end anonymity and validation DoS |
| Early surrender yields tradable credit | Speculative extension | Explicit credit/handoff/authorization conditions | Keep optional; conservative reclaim credit is the real gate |
| Proposed composition is novel | Bounded literature assertion | Adjacent-mechanism review | Separate base contribution from optional synthesis; provenance/novelty uncertainty remains |

## Compact reverse outline and paragraph dispositions

The following is a paragraph-cluster reverse outline. Every section in the supplied corpus was read; adjacent paragraphs advancing the same claim are grouped to keep the outline usable. Equations, lists, tables, and figures belong to the surrounding argumentative unit. This is not a claim that an independent source check or formal proof was done for every paragraph. Roles: P premise/problem; D definition; M mechanism/design; E evidence/derivation; I implication; L limitation; Q question/test. “Keep” preserves role and placement unless a finding above says otherwise.

| Location / paragraph cluster | Role | One-sentence message and what it supports | Support | Disposition |
|---|---|---|---|---|
| README opening through external storage | P/D | Selectable native duration separates flow and stock and composes with external persistence | Proposed thesis and service boundary | Keep, simplify introductory vocabulary |
| README roadmap, stable index, paths | Navigation | Several routes expose the corpus | Links | Consolidate after explanation, ARG-01 |
| README central claims 1–5 | E/M/L | Fixed-workload accounting is narrow and physical realization conditional | Core derivations | Integrate into explanatory narrative |
| README claims 6–10 | I/L | Extensions, write/network constraints, service scope, persistence stay distinct | Linked branches | Compress and link |
| README comment/layout/artifacts/citation | Navigation | Reader can inspect and contribute | Files and commands | Keep compact |
| 00 executive framing paragraphs 1–2 | P/analogy | DA roadmap scales quantity; resource specialization motivates duration | Roadmap and new-state citations | Brief context; avoid assuming roadmap familiarity |
| 00 executive paragraphs 3–6 | M/E/L | Bound duration, illustrate byte-time, then expose stock and representation constraints | Inequality intuition, scenario | Keep; move detailed 2D alternatives later |
| 00 executive remainder | I/transition | Broader applications are optional; core asks why fixed service | Hypothesis | Compress repeated question and branch preview |
| 00 §1 | D/P | Ingress is flow and continued custody is stock; prices may distinguish them | Physical decomposition and equal-size example | Keep; resource distinction does not establish demand |
| 00 §2 opening, API, metadata | D/M | Blob granularity and canonical publication define the lease | EIP baseline, proposed interface | Keep authoritative definitions; duration/expiry notation correction needed |
| 00 §2 expiry and integrity paragraphs | L | Native obligation ends; copies and proofs have separate lifetimes | Service semantics | Keep |
| 00 §2 external-storage bridge | I/L | External persistence complements shorter native service | Handoff reasoning | Keep short; detailed markets stay in 04 |
| 00 §2 transport-neutral paragraphs | M/hypothesis | Stable semantics are the target across representations | Architectural aim | Calibrate ARG-08 |
| 00 §2.1 availability/serving distinction | D/L | Initial DAS and interval obligation are different claims | Current design citation | Keep before enforcement levels |
| 00 §2.1 guarantee table and counterexamples | D/L | Availability, custody and delivery are not synonyms | Logical counterexamples | Keep; particularly useful README summary |
| 00 §2.1 representation bridge | Transition | Fresh and historical representations may differ | Hypothesis | Link to 05 |
| 00 §2.2 | D/L | Base uses required serving; monitoring/penalties need extra mechanisms | Current baseline and proof semantics | Keep but shorten repeated historical-proof warning |
| 00 §2.3 | I | Lifecycle tails generalize the interface | Lean research | Move detailed profile out of minimal mechanism path |
| 00 §2.4 | L | Network-wide availability remains the product | Service definition | Keep concise boundary |
| 00 §3 vocabulary and bounds | D/L | Duration must cover protocol and application floors within maximum | Timing arithmetic and recovery duties | Define once; don't imply one-epoch safety |
| 00 §3 hot phase, slot expiry, finality | M/Q | Clock starts on inclusion; unresolved fork duties require bounded design | Sketch and open constraints | Keep core premises visible |
| 00 §3.1 | D/I | Unchanged-ingress and increased-ingress deployments have different claims | Scope split | Correct physical inference ARG-04 |
| 00 §3.2 | E/L | Indicator sums prove weak logical stock dominance | Explicit derivation | Keep; central proof is appropriately qualified |
| 01 §4 | D/E | Already-admitted immediate-start stock never grows with future horizon | Monotonic expiry argument | Keep; exclude future starts explicitly |
| 01 §4.1 state sketch | M | Admission tracks service end separately from reclaimable capacity | Non-normative pseudocode | Keep; align drifted counter/ring wording |
| 01 §4.1 explanatory paragraphs | D/M/L | Publication identity, EL/CL visibility, profiles, reclamation and reorgs constrain implementation | Invariants | Keep; surrender paragraph can be link-only |
| 01 §4.1 unresolved choices | Q | Exact interfaces and physical conversions remain open | Design inventory | Keep |
| 01 §5 opening and null fee | M | Byte-time pricing is independent of blob granularity | Accounting equation | Keep illustrative label |
| 01 §5 candidates/hot-cold costs | M/I | Price form remains undecided and fresh cost cannot vanish | Candidate formulas | Keep; avoid privileging 2D in base |
| 01 §5 prepaid versus rent/payment | L/alternative | Paid horizon cannot depend on later top-ups; scarcity is separate from rewards | Security semantics | Keep |
| 01 §5.1 | L | Fees cannot create safety or honest admission | Adversarial argument | Fix scalar phrasing; remove revision history |
| 01 §6 vector derivation | M/L | Every physical dimension must fit a chosen hardware envelope | Schematic accounting | Keep authoritative physical premise |
| 01 §6 hot/cold budget paragraphs | M/E | Reserve working/repair/metadata costs before cold capacity | Dimensional model | Keep schematic |
| 01 §6 headroom and attack limits | M/L | Reserve limits long-lease preconsumption but not flooding | Steady-state calculation and adversary | Keep |
| 01 §7 introduction and §7.1 | Alternative | Small maturity classes simplify representation at fragmentation cost | Design tradeoff | Promote to equal candidate, ARG-03 |
| 01 §§7.2–7.3 | Alternative/L | Renewal/rent weakens prepaid continuity absent reservations | Security reasoning | Keep |
| 01 §§7.4–7.5 | M/Q | Sparse 1D and conditional 2D can support finer expiry | Compatibility hypothesis | Avoid continuous-as-default hierarchy |
| 02 §8 first half | L | Selected duration must satisfy beneficiaries' recovery needs | Payer/user distinction and challenge windows | Keep central application gate |
| 02 §8 second half | I/L | Elastic applications can shorten to a genuine floor | Conditional reasoning | Keep conditional; incentives are predictions |
| 02 §9 | I/Q/L | Price feedback may stabilize but strategic demand may defeat it | Behavioral mechanism and counterexamples | Correct summary safety claim |
| 03 §10 | D/M | Future ingress and future retention create delivery-time obligations | AOT precedent and proposed composition | Keep extension label |
| 03 §10.1 | M/E | Future starts need interval occupancy and future envelope | Accounting derivation | Keep; notation needs separate absolute/relative times |
| 03 §10.2 | L/Q | Reservations create strategic concentration and forecast risk | Adversarial cases | Keep |
| 03 §10.3 | M/I | Prepaid propagation capability motivates cheap authorization | Draft baseline and privacy sketch | Keep branch |
| 03 §11 | M/L | Financial ownership can be separated from delivery credentials | Current ticket fields versus proposed indirection | Keep distinction, compress fragments |
| 03 §12 | D/L | Payment, network, application and profile privacy need different mechanisms | Waku precedent and leakage examples | Keep extension; avoid raw-size ambiguity |
| 03 §13 opening and handoff | I/L | Included data can seed external replication | Existing DA plus chosen window | Correct claim of stronger opportunity, ARG-05 |
| 03 §13.1 | D/L | Inclusion, fresh withholding and later service refusal are different failures | Inclusion-list reference and layer reasoning | Keep; cite from application summary |
| 04 §14 opening and comparison | D/I | External service begins by acquiring authenticated bytes before expiry | Service composition | Keep; repetition can shorten |
| 04 §14.1 | E | Existing systems demonstrate adjacent persistence products | Sources | Keep as adjacent evidence |
| 04 §§14.2–14.4 | M/I/L | Centralized, receipt-based and chained promises have distinct trust models | Worked constructions | Keep optional |
| 04 §15 | E/I | Storage-only uniform-duration frontier is inverse in duration | `S/T` model | Link from core capacity; scope market conclusions to binding storage |
| 04 §16 | Navigation | Numerical example is elsewhere | Appendix link | Remove revision-history voice |
| 05 §17 opening/diagram | P/D | Heterogeneous expiry has 1D packaging and conditional 2D coupling problems | Representation distinction | Keep, lead with 1D rather than FullDAS leverage |
| 05 §17.1 | P/E | Whole-column serving ties expired rows to live neighbors | Example, EIP-8136 as adjacent evidence | Keep first implementation obstacle |
| 05 §17.2 | P | Cross-row parity creates deeper coupling | Coding dependency | Keep explicitly conditional |
| 05 §17.3 phases/candidates | M/Q | A hot-to-cold handoff needs independently authenticatable live rows and common transition | Proposed invariant and alternatives | Keep branch; not implementation evidence |
| 05 §17.4 repair/model | M/E/L | Cold repair has distinct latency and survival constraints | Null probability model | Keep caveats attached; 'conservative' needs a bound |
| 05 §17.4 incentives/accountability | L/Q | Online presence and cheap identities do not ensure continued service | Adversarial reasoning | Keep level-1 versus stronger claims distinct |
| 05 §17.5 | I/L | Hot and cold workloads differ without removing writes | Resource decomposition | Keep core hardware summary; link optional operators |
| 05 §17.6 | Q | Five compatibility conditions reduce to three branch-kill questions | Explicit falsifiers | Keep scope boundary |
| 05 §17.7 | Alternative | Maturity cohorts avoid mixed persistent lifetimes | Design tradeoff | Candidate base/fallback, not proposal rejection |
| 05 §17.8 | E/Q | Compare physical vectors and select representation/granularity empirically | Decision rule | Keep as central evaluation framework |
| 05 §17.9 | M/Q | Distributed prepublication might separate builder selection from full upload | Proposed composition and unsolved obligations | Keep extension; no solved centralization claim |
| 06 §18 | I/L | Short duration changes stock, not live throughput costs | Scale arithmetic | Keep illustrative; no roadmap inference |
| 06 §18.1 | M/L | Distributed upload can avoid one bandwidth bottleneck without fixing inclusion power | Adjacent research | Calibrate 'simply', ARG-08 |
| 06 §19 pattern and floors | I/L | Temporary raw inputs may support durable proved outcomes | Computation pattern | Keep; apply ARG-09 timing qualification |
| 06 §19 examples and figure | I | Different applications might select different windows | Scenarios | Keep representative subset; not demand evidence |
| 06 §19.1 | E/L | Two projects motivate non-rollup use at different maturity levels | Prototype references | Keep precise prototype limitations |
| 06 §20 | I/L | Ethereum and overlays can specialize responsibilities | Architecture and bounded analogy | Keep conditional; include admission qualification locally |
| 06 §20.1 | Analogy | Early Ethereum stack offers a historical parallel | History citations | Optional color; low priority for core reader |
| 06 §20.2 | I/L | Resource specialization is a heuristic across distinct services | Comparison table | Keep distinctions, calibrate closing expansion claim |
| 07 §§21–21.4 | E | Fixed expiry, state rent and timed persistence narrow novelty | Prior-art citations | Keep; not source-verified in this pass |
| 07 §§21.5–21.5.1 | E/D | AOT and derivatives have different settlement claims | Prior-art categories | Keep; no invention-of-futures claim |
| 07 §21.6 | E/L | Cell/distributed publication precedents do not establish historical expiry | Source distinctions | Keep |
| 07 §§21.7–21.9 | E/L | Multiplexing, overlays and custody proofs provide adjacent ingredients | Sources and negative scope | Keep; matrix can compress overview |
| 07 §21.10 | Conclusion | Contribution is composition | Bounded literature claim | Narrow base versus branches, ARG-07 |
| 08 §§22–22.0 | Q | Proposal should be attacked by physical value, demand and simpler alternatives | Decision criteria | Split falsification levels, ARG-03 |
| 08 §§22.1–22.1.1 | Q | Capacity/pricing and optional pools have separate empirical unknowns | Research questions | Tag base versus procurement gates |
| 08 §§22.2–22.4 | Q | Granularity, physical realization and application minima decide base value | Concrete falsifiers | Keep as priority queue |
| 08 §§22.5–22.10 | Q | Futures, stronger evidence, persistence, scale, privacy and surrender add gates | Branch questions | Scope each, correct final blanket gate ARG-02 |
| 09 §23 first six paragraphs | Conclusion | State narrow mechanism/accounting and central physical risk | Core synthesis | Keep, compress to four movements |
| 09 §23 remaining paragraphs | I/L | Hardware, scale, proofs, rollups and markets restate the corpus | Earlier branches | Replace with compact branch links |
| 09 research anchors | E/navigation | Repeats reference inventory | Sources | Centralize in reference apparatus |
| 10 short answer/§1 | D/I | Future transports motivate stable semantic interface | Lean research | Keep conditional |
| 10 §2 | I/L | Protocol-generated payloads add data classes and payer problem | Draft EIP | Keep branch |
| 10 §3 | M/L | Sparse tails differ from full retrievability | Research profile and examples | Keep distinction |
| 10 §4 | L | Active state is not ordinary expiring DA | Execution access requirement | Keep |
| 10 §§5–6 | M/Q | General profiles need access classes and recurring tail funding | Schematic interface/accounting | Keep non-normative; consolidate repeated payer paragraphs |
| 10 §7 | Mapping | Research directions affect different dimensions | Source map | Keep |
| 10 §8 | Revision instruction | Five changes are requested of the base text | Editorial history | Convert to present compatibility boundaries |
| 10 §9/sources | Q/E | Representation, funding, reconstruction and privacy remain open | Questions and primary sources | Keep |
| 11 short answer | P/scope | Hardware costs and provider mechanisms concern supply | Architecture | Separate constraints from pools ARG-06 |
| 11 §1 | E/L | Fixed ingress fixes writes even when stock shrinks | Dimensional endurance example | Keep useful physical warning |
| 11 §2 | M/L | Expiry can inform placement and repair without allowing early loss | Scheduling candidates | Keep optional implementations |
| 11 §3 variants/handoffs | M/L | Pools require accountability, independence and overlap | Arithmetic and adjacent precedent | Keep extension |
| 11 §4 | D/M/L | New service rewards differ from current burned fees and require qualification | Baseline plus proposed formula | Keep clear baseline |
| 11 §5 | M/Q | Bounded prices need trustworthy supply data and anti-withholding design | Toy controller and risks | Keep no-oracle statement |
| 11 §6 scenarios | I/E | A possible end-to-end architecture must fund all duties | Conditional architecture and arithmetic | Keep illustrative |
| 11 §§7–8 | Q | Measure ordinary custody before testing pools/rewards | Comparative deployment sequence | Keep; not base prerequisites |
| RetentionNotes A.1 | M | Metered downstream service ends at condition or cap | Contract sketch | Keep optional |
| RetentionNotes A.2 | M/L | A secret permits identity-light acknowledgement but cannot force it | Hash-preimage sketch | Limit evidence to secret possession; sender knows secret |
| RetentionNotes A.3 | L/M | Storage payment does not price recipient attention | Separate mailbox policies | Keep |
| Numerics opening/tables | E | Hypothetical logical capacity gives inverse duration frontier | Dimensional arithmetic | Keep storage-only scope local |
| Numerics conclusion/model command | I/navigation | Horizon changes stock-limited ingress and reserve allocation | Derived frontier | Avoid implying complete physical throughput guarantee |
| Operator economics calibration | E/L | Arbitrary rates scale mechanically with bytes and duration | Arithmetic | Keep artificial labels; no economic sustainability inference |
| Operator economics controller | M/L | A bounded feedback rule changes prices but cannot qualify supply | Toy model | Keep |
| Operator economics comparison | Alternative/Q | Procurement choices expose different games | Mechanism comparison | Keep conditional |
| Backbone B.1 | E/L | Fixed node bandwidth requires shrinking assigned fraction as ingress rises | Lower bound | Keep |
| Backbone B.2 | E/L | Aggregate receiver capacity constrains rate independent of retention | Conservation and examples | Keep receiver-only caveat |
| Backbone B.3 | E/L | Multiplying current blob/proof granularity creates control cost | Arithmetic | Keep stress-test status |
| Backbone B.4 | M | Larger frames and aggregation are possible responses | Architectural inference | Keep candidate, not uniquely necessary solution |
| Backbone B.5 | L | Storage, writes and network must close in one architecture | Combined inequalities | Keep |
| Backbone B.6 | Q | Topology-aware trace replay is next evidence | Measurement specification | Keep |
| Ephemeral C.1–C.2 | D/L | Inclusion, initial DA, surviving content and computation evidence differ | Proof semantics | Keep |
| Ephemeral C.3 | M/I | A commitment-bound proof can outlive its witness | Conditional proof construction | Keep |
| Ephemeral C.4 | L | Proving/retry must have usable input for long enough | Timing model | Distinguish sufficient native schedule from necessity ARG-09 |
| Ephemeral C.5–C.6 | L | Encoding binding and availability evidence remain separate | Cryptographic statement boundaries | Keep |
| Ephemeral C.7–C.8 | L/Q | Expiry is not deletion and outputs may leak | Threat model/questions | Keep |
| Private AOT opening/D.1 | P/E | Prepaid capacity must retain cheap anti-DoS checks | Draft baseline | Keep extension |
| Private AOT D.2 | Alternative/L | Per-gossip ZK checks can expose verification DoS | Attack sketch | Keep |
| Private AOT D.3–D.4 | M | Canonical activation creates a cheap public key check | Proposed state/indirection | Keep; no end-to-end DoS proof |
| Private AOT D.5–D.6 | L/alternative | Timing/denomination and thin liquidity can undermine privacy | Traffic-analysis reasoning | Keep hypothetical economics |
| Private AOT D.7–D.8 | Q/L | Solvency, replay, leakage and race rules remain unresolved | Threat inventory | Keep branch gates |
| Surrender E.1–E.2 | D/L | Surrender, novation and future rights are different optional operations | Definitions | Keep |
| Surrender E.3–E.4 | M/L | Logical end precedes safe, potentially non-additive physical credit | Credit definition and counterexamples | Keep central gate |
| Surrender E.5–E.6 | M/L | Replacement needs overlap and representation-dependent reclaim | Transition sketch | Keep; no future credit financing earlier hot work |
| Surrender E.7 | L | Payment does not authorize destroying beneficiaries' service | Actor analysis | Keep |
| Surrender E.8–E.9 | Alternative/M | Return, residual rights and buyouts have different state requirements | Candidate mechanisms | Keep optional |
| Surrender E.10–E.12 | Q/conclusion | Reject branch without conservative credit, protected rights and bounded overlap | Kill criteria | Keep explicit base/branch boundary |

## Recommended README and core order

README should stand on its own for a technically knowledgeable reader who knows blockchains but not this proposal. Aim for approximately 900–1,300 words of project explanation before maintenance information, not a strict word quota. Each paragraph should contain the hyperlink that answers its likely next technical question.

1. **One-paragraph proposal:** purchasers choose the required serving duration of each blob; existing maximum service remains available; this is research, not implemented Ethereum behavior.
2. **Why duration matters:** current blob service bundles publication work and later serving. Define DA, ingress, retention, and byte-time in familiar language. Give one explicitly illustrative equal-blob comparison; avoid leading with an unsafe hour-scale promise.
3. **What happens to one blob:** purchaser selects allowed duration; canonical publication establishes availability; clients derive lease identity and expiry; custody serves until expiry; physical accounting returns capacity conservatively. Existing blob quantity remains fixed and later voluntary copies are allowed.
4. **What is established versus open:** same-workload logical inequality; representation-specific physical savings still unproved; no ingress/write/network saving follows merely from expiry.
5. **Who could use shorter service:** rollup recovery and proving floors; one ephemeral computation/replication example; external handoff changes the service assumption. Link evidence table rather than promise broad demand.
6. **First experiment and success criteria:** matched fixed versus small-menu versus finer-duration prototype under current 1D PeerDAS; measure storage, requests, repair, I/O, metadata, recovery and workload value. Explain failure/simplification decisions.
7. **How wider project fits:** short descriptions and links for future reservations, persistence/receipts, generalized applications/proofs, Lean lifecycle compatibility, specialized operator procurement, private activation, and optional surrender. State these are branches and do not expand base prerequisites.
8. **Evidence/repository/use:** executable models are accounting/null models; source cutoff and pinned references; one grouped detail index; how to run checks, comment, cite and license.

Canonical core path: README → 00 service/bounds/logical result → 01 admission and pricing distinction → 05 1D physical problem and vector comparison (with concise hardware summary/link) → 02 application minima → 07 narrow prior-art comparison → 08 applicable base tests → short 09 conclusion. Preserve filenames and cited anchors. 11 is a mixed core-constraint/extension chapter: link its hardware subsections, not the whole procurement program as mandatory reading.

## Revision sequence and residual uncertainty

First correct scope and inference defects ARG-02/03/04, then settle the base/branch hierarchy used by README and conclusion. Calibrate demand, compatibility and proving-window language next. Rewrite README once those claims are stable. Remove duplicated source inventories and editorial-history prose last; they are maintenance improvements, not validity fixes.

Preserve the substantial strengths: the fixed-workload inequality, publication-level lease identity, protocol/application floors, expiry/reclamation distinction, enforcement levels, representation branches, beneficiary protection, and explicit null-model labels. Do not repeat acknowledged model limitations as new defects unless an output or summary erases the qualification.

This audit does not establish protocol feasibility, new source facts, novelty priority, application demand, or correct model numerics. Those require the other specialist passes and ultimately actual client/workload research. The paragraph map is grouped for readability, not a paragraph-by-paragraph rewrite mandate.
