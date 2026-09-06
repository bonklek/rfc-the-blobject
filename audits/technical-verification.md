# Independent post-revision technical verification

Date: 2026-09-06. Scope: technical correction verification against the six specialist review reports, completion record, current changed model/tool code and selected changed mechanism passages. The first-pass findings below preserve their original snapshot; the follow-up closure section records the subsequently verified corrections. No source files were edited by this verifier.

Final status: all actionable technical findings from this verification are closed in the inspected working tree. The research and finite-precision limitations below remain.

## Assessment

The main corrections are sound. The future-price integral now uses lookahead coordinates consistently: at current time 100, start 120, duration 10, it integrates horizons 20 through 30. The half-open service interval excludes expiry. Chapter 10 now distinguishes a node's encoded local fraction from aggregate custody service and uses a full custody profile for aggregate pricing; ten nodes each assigned 0.2 of an object incur two object-equivalents of local duty, not 0.2 aggregate. These fixes resolve M04/PROSE-01 and the central PROSE-02 ambiguity.

The logical-stock versus physical-resource distinction is repaired in chapters 01 and 02. Canonical AOT authorization is separated from peer-local traffic histories; restoring authorization cannot restore bandwidth. The bearer-secret note now explicitly admits sender cancellation and does not certify recipient retrieval. Surrender now protects old-object rights separately and leaves unsafe native surrender unavailable. Supply-loss admission changes do not cancel outstanding duties. Those resolve the concrete M01–M03, M06–M07 counterexamples at the inspected locations. Their deployment questions remain open, appropriately.

## Remaining actionable numerical findings at first verification

### TV-01 — P2: representable lease risk can be lost by interval underflow

Location: models/cold_custody.py, interval_failure_probability and lease_failure_probability (initial snapshot lines 27–28 and 64–78).

Reproduction: call minimum_replicas with cells=1, reconstruction_threshold=1, custodian_population=10, failure_probability=1e-200, duration=1e300, repair_interval=1, p_max=1e-150. It returns 2 and reports zero lease failure for two replicas. Exact two-replica interval risk is about 1e-400 and the lease risk is approximately 1e-100, which is representable and fails the target. Three replicas give approximately 1e-300 and pass. The README's underflow caveat acknowledges unrepresentable probabilities, but does not describe a false pass for a representable final result after checkpoint amplification.

Keep interval risk in log space until checkpoint composition/target comparison, or reject a clearly documented unsupported numerical domain. Test the exact one-cell amplification identity with high precision. This is an extreme-input numerical correctness issue in a null model, not evidence against the proposal or a production safety claim. Confidence high.

### TV-02 — P2: round-trip logarithms reject an exact risk boundary

Location: models/cold_custody.py, interval_failure_probability and minimum_replicas (initial snapshot lines 43 and 105).

Reproduction: cells=1, reconstruction_threshold=1, custodian_population=10, failure_probability=0.1, duration=1, repair_interval=1, p_max=0.1 returns minimum_replicas=2. One replica has failure exactly equal to the supplied failure_probability and should satisfy the inclusive target. The exp(log(p)) round trip yields 0.10000000000000002 and spuriously rejects it. Preserve exact elementary endpoint identities where possible and use a deliberately defined numerical comparison policy; do not add a broad tolerance that can hide materially excessive tiny risk. Confidence high; impact is conservative overprovisioning at the boundary.

Both findings were sent to the coordinator for correction. They refine MOD-01: its original catastrophic cancellation cases are fixed, but complete numerical closure was not yet established by the first verification.

## Tests and old-finding dispositions

- Ran 26 model tests successfully; original one-cell tiny target and published high-precision 128-cell tail now pass. MOD-01's original reproductions are resolved, subject to TV-01/02 above.
- Ran three documentation-tool tests successfully. The checker validates this repository's stated inline-link/ATX-heading subset, not arbitrary Markdown; no material new defect established. Current repository check passed with 33 Markdown files and 168 local links before this report was added.
- MOD-02: CLI and models README explicitly label independent cells, independent intervals and complete repair. The overlapping-holder counterexample is present. Chapter 05 still needed the words “independent intervals” alongside its product formula at the initial verification; sent to coordinator.
- MOD-03: API now rejects both future arrivals outside observation and incomplete lease service; default horizon includes actual billed expiry. The published fixed scenario outputs were never affected by the original issue. Model regressions pass.
- MOD-04: current hardware text defines spare capacity relative to assigned capacity, preserving the intended arithmetic.
- F-01 is handled as an explicitly open exact legacy-range mapping, not a completed implementation: the elapsed-duration toy is no longer claimed to implement it. This is an honest disposition, not proof of a safe full-window parameter.
- Several old prose locations remained in the concurrent snapshot (surrender marginal burden, numerical stock-only takeaway, chapter 10 logical-size shorthand, chapter 01 continuous-target/fallback phrasing); sent to coordinator and reader-verification owner for disposition rather than duplicated as new technical findings.

Full integration regeneration and visual review were being performed by the coordinator. This pass did not independently retrieve external sources, inspect a running Ethereum client, measure hardware, validate application recovery windows, or establish custody security. Those are outside the evidence supplied by these toy models.

## Follow-up verification after Decimal correction

TV-01 and TV-02 are closed for their reported reproductions. The revised model retains the failure tail and checkpoint composition at 80-digit Decimal precision, uses small-argument series to avoid cancellation, and compares replica-selection targets in Decimal. Re-ran the independent reproductions: two-replica lease risk is 1e-100 and required multiplicity is 3; the exact 0.1 single-cell boundary accepts one replica. All 28 model tests pass. An additional independent sweep of 99 one-cell, 27-interval cases (failure probabilities 0.01 through 0.99) matches a separate 100-digit direct-complement calculation within 1e-15 relative tolerance. Current documentation checker passes with 35 Markdown files and 168 local links.

Confirmed the chapter 05 product now explicitly assumes independent intervals. Chapter 10 defines B as protocol-accounted quantity. The surrender example describes near-zero released capacity, the numerical takeaway carries its storage-only scope, and chapter 01 no longer privileges arbitrary granularity as a prerequisite. These formerly outstanding wording dispositions are closed.

One P3 numerical-policy consistency issue was sent to the coordinator: the CLI still rounds the computed risk to float before its target comparison, whereas minimum_replicas compares Decimal. With one cell/threshold/replica, q=0.02, duration=27, repair_interval=1, and p_max=0.4204324735203474, exact risk is 0.420432473520347409079056448611586728046952078196604928. The replica API correctly rejects one; the CLI reports true after rounding to the target. This affects a rounding-scale boundary, not the repaired material underflow case. Use the same Decimal decision in CLI and convert only displayed probabilities to float. No new material technical error was established by this follow-up.

### Final CLI closure

Confirmed the CLI now compares the Decimal failure and Decimal target within the same 80-digit context and converts probabilities to float only for display. Independently executed the q=0.02, 27-interval boundary reproduction: meets_target_under_null_model is now false, consistent with minimum_replicas. All 29 model tests pass, including the CLI regression. The P3 consistency issue is closed. No actionable technical findings remain from this bounded verification; finite-precision arithmetic and the explicitly conditional custody model remain limitations rather than a security proof.
