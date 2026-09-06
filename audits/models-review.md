# Models and economics specialist review

Date: 2026-09-06. Read-only review except this report. Locations describe the reviewed working tree; the coordinator is editing concurrently. Severity follows the argument skill: P1 material defect, P2 support/consistency defect, P3 expression. No finding invalidates the proposal's logical byte-time thesis.

## Coverage and argument

Read the local argument skill, Blobject rubric, initial audit/approved programme, all seven executable model/support modules and both test modules, model README, numerical and operator-economics appendices, backbone appendix, relevant capacity/pricing, cold-custody and hardware/operator chapters. Inspected mathematical claims in the lifecycle and surrender extensions and the retention-note economic roles. This is not external-source verification, hardware measurement, incentive equilibrium analysis, or full cryptographic review of the private/ephemeral appendices.

The defensible argument is: durations change logical stock at fixed admissions; capacity accounting can bound that stock; physical savings and qualified supply require additional measurements; prices and service payments are hypotheses. The strongest economic objection is that fixed-arrival simulations cannot establish behavioral improvement or net welfare. The repository already states that limitation clearly, so it is not a fresh defect.

## Findings

### MOD-01 — P1: Tail cancellation makes custody risk targets wrong

**Location:** `models/cold_custody.py:27-34,83,114-115`.

**Evidence:** The implementation forms survival near one, raises it to a power, then subtracts from one. Running the existing functions with `cells=1, reconstruction_threshold=1, custodian_population=10, failure_probability=1e-10, duration=1, repair_interval=1, p_max=1e-25` returns `minimum_replicas=2`. The exact interval loss is `q**replicas`: two replicas lose with probability `1e-20`, exceeding the target; three give `1e-30`, meeting it. For two replicas the current output is survival 1.0 and failure 0.0. Conversely, the README example (128 cells, threshold 64, q=.1, replicas 2, 512 intervals) reports failure `5.115907697472721e-13`, whereas summing the failure tail with 100-digit Decimal arithmetic gives approximately `6.4727168e-91`.

**Consequence:** Both false target passes and severe overestimation of tiny risk are possible inside the stated null model; this is a numerical bug beyond the model's acknowledged applicability limits.

**Correction:** Compute interval failure directly as the binomial upper loss tail and compare failure to `p_max`. Compose interval loss with `-expm1(N*log1p(-p_interval))`; ensure the tail method is stable near both endpoints and avoids large-combination overflow. Preserve existing survival API if needed, but never derive target decisions from rounded near-one survival. Add the exact one-cell test and a high-precision reference tail case.

**Confidence/support:** High, directly reproduced and independently checked by elementary exact probabilities and Decimal arithmetic.

### MOD-02 — P2: Output and “conservative” label omit independent cell/checkpoint assumptions

**Location:** `models/cold_custody.py:1,22-34,112-115`; `models/README.md` cold-custody section; `docs/05-can-this-work-with-peerdas-and-fulldas.md:264-294`.

**Evidence:** Two cells, threshold one, one custodian, one replica, q=.1, one interval returns survival `.9900000000000001`. A sole custodian holding both cells yields survival .9. Independent failures of custodians do not establish independence of cells whose holders overlap. The chapter already acknowledges assignment overlap, but the CLI emits an unqualified `meets_target`, and the expression is still called a “conservative checkpoint approximation.” Independence across intervals and complete successful repair are also premises of the product.

**Consequence:** A researcher can interpret a numerical pass as a bound for an impossible independent assignment, while “conservative” suggests a justified direction of error. Neither follows from the supplied population bound.

**Correction:** Attach independent cell-loss, independent intervals and successful repair assumptions to CLI output and README. Rename the target result as conditional/null-model feasibility. Remove general “conservative”; explain that rounding a partial final interval up is conservative only within the explicit independent, full-repair model. Add the shared-custodian counterexample without pretending the null model is assignment-aware.

**Confidence/support:** High. The limitation itself is acknowledged; the actionable residual defect is output labeling and unsupported bound language, not the abstract binomial formula.

### MOD-03 — P2: Explicit simulation horizon overcounts admission and censors coverage

**Location:** `models/spot_simulation.py:105-112,124,198-203`.

**Evidence:** `simulate('trunc', [Arrival(0,1,10), Arrival(5,1,1)], Mechanism('s','byte_time',capacity=100), horizon=0)` reports requested=2, admitted=2, charge=10, coverage=9.9. Only the first arrival was processed, and only one epoch of its ten-epoch scarcity path was accumulated. With horizon=10 the same input gives charge≈11.0101 and coverage≈.989074. A full-length single lease similarly makes the upward coverage artifact transparent.

**Consequence:** The exposed horizon option can declare future requests admitted and create apparent quote coverage from an incomplete ex-post denominator. Current generated scenarios run through all their expiries and are not affected. The default horizon also assumes all durations are bounded by `max(maturities)` even for shared-capacity mechanisms that do not enforce that bound.

**Correction:** Either reject horizons that do not cover all arrivals and lease expiries (and derive the default from actual billed durations), or explicitly report processed/admitted requests and censored active leases with coverage unavailable/incomplete. Add one future-arrival and one incomplete-lease regression case.

**Confidence/support:** High, directly reproduced. Scope is reusable simulation API, not the published default results.

### MOD-04 — P3: Reserve denominator is ambiguous

**Location:** `docs/11-how-do-hardware-and-da-operator-markets-scale.md:336-340`.

**Evidence:** “reserves 20% physical spare capacity” accompanies `2.56 PB/(2*1.20)≈1.07 PB`. This reserves one-sixth of gross physical capacity, which is 20% of assigned capacity. Reserving 20% of gross gives `2.56*.8/2=1.024 PB`.

**Consequence/correction:** The formula is valid under a spare-to-assigned ratio; name that denominator explicitly rather than changing the number absent an author choice.

**Confidence/support:** High arithmetic; medium significance. This is wording ambiguity, not a demonstrated false formula.

## Validated results and limitations that need no new finding

- Ran `python -m unittest discover -s models -p "test_*.py"`: all 21 tests pass. Existing tests do not exercise MOD-01 or MOD-03.
- Regenerated both scenario CSVs and all three scenario SVGs in an OS temporary directory; all five equal checked-in files after newline normalization. Byte inequality is solely line-ending variation, not stale content. No checked-in outputs were changed.
- Recomputed operator payment rows using exact epoch duration: totals 5.991234375, 109.554, 42068.736 dollars/day; annual totals 2186.800546875, 39987.21, 15355088.64. Published rounding is correct, including the first row's separately rounded components.
- Verified 64 TiB stock frontiers, two-thirds targets, epoch/day/hour conversions, hardware write and resident-stock arithmetic, network multiplier examples, object/cell-proof counts, and normalized payment ratios. No arithmetic defects found there.
- Stock is an abstract dictionary model, not an epoch ring or canonical protocol adapter. The coordinator's already-visible README and chapter corrections accurately delimit it. No request to replace it with a ring.
- Procurement equation and tests match the stated bounded update. No stability or market-equilibrium proof is claimed. Floors/ceilings can saturate the response; “raises under shortage” should be understood as conditional on nonzero price/gain and no ceiling. Zero price with a zero floor is an absorbing state; this is a controller initialization caveat, not a central proposal defect.
- Equal maturity lanes intentionally strand capacity, demand is fixed, and the ex-post scarcity benchmark is not operator/social cost. Those qualifications are explicit. At saturation the benchmark uses an arbitrary utilization clamp of .999999; future comparative sensitivity work should vary that clamp, but current outputs do not claim calibrated welfare or profit.
- Pricing functions are illustrative and accept some economically nonsensical direct-call inputs (e.g. negative size). Input hardening could improve the experiment interface; it does not undermine published positive-input examples and is not prioritized over the actual risk calculation.

## Revision order and residual uncertainty

Fix MOD-01, then MOD-02, then MOD-03; clarify MOD-04 with a minimal wording change. Repeat the focused tests and isolated regeneration. The empirical questions remain demand elasticity, recovery-safe horizons, physical expansion/amplification, assignment-aware survival, qualified supply and withholding behavior. Passing these toy models supplies no answer to those questions.
