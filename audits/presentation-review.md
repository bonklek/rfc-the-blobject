# Filesystem and presentation review

Date: 2026-09-06. Read-only specialist pass; existing source and published artifacts unchanged. Coordinator revisions were already in progress, so anchors describe the inspected working tree and may move.

## Coverage and method

Read the initial audit, local argument skill and project rubric, README, CONTRIBUTING, model README, validator, both figure generators, new check-docs/check-generated tools, research-tracker scope, all document/appendix heading and navigation structure, figure embeds/captions, tracked inventory, and all eight SVG sources. Rendered all eight SVGs at native dimensions through installed CairoSVG, then visually inspected every PNG. Evidence is under `audits/visual-qa/`, with the SVG basename preserved. Ran `python tools/check-docs.py`: 27 Markdown files, 78 local links, chapter inventory 00–11 passed at inspection time. Did not duplicate coordinator's generated-output/model verification.

The argument skeleton remains: selected service duration → logical byte-time reduction with fixed ingress → representation-dependent physical feasibility → application recovery constraints → experiments. These figures should explain that dependency without implying measured demand, physical throughput gains, or settled minimum durations.

## Actionable findings

### PRES-1 — P2: Figure 2 turns a conditional maturity range into an exclusion

**Location:** `tools/render-rfc-figures.py:197–203`; `docs/assets/figures/figure-02-term-structure.svg:16–20`; caption at `docs/01-how-are-capacity-and-pricing-managed.md:196`.

**Evidence:** orange region below 256 epochs says “below here: not independently selectable,” while the mechanism at chapter 01 §7.1 permits 1, 8, and 64 epochs if `T_hot` permits. The footer saying `T_min` is unsettled does not resolve the prominent contrary label. The subtitle promises “null and convex-duration benchmarks,” but the generator draws only the convex curve. The Markdown alt text also says a jump at T=0, while the plotted log axis starts at 1.

**Consequence:** the visual implies a settled lower boundary and comparison it does not supply.

**Fix:** label the region “shorter classes conditional on T_hot”; call 256 an illustrative class boundary, remove the nonexistent null-curve promise, and describe the ingress marker as admission charge at the left plot edge. Move the boundary label a few pixels away from the horizontal 20,000 grid line.

**Confidence/support:** high; direct text/source and rendered evidence. This is a terminology/support defect, not a critique of the model formula.

### PRES-2 — P3: Figure 1 clips its left vertical axis label

**Location:** `tools/render-rfc-figures.py:88,144`; `docs/assets/figures/figure-01-throughput-retention-frontier.svg` (left rotated axis text).

**Evidence:** first panel starts at x=44 and axis text is centered at x=9; native rendering cuts the left of “Sustainable ingress (MiB/s)” against the canvas edge. The right panel's caption is intact. See `audits/visual-qa/figure-01-throughput-retention-frontier.png`.

**Fix:** increase left margin or move the first rotated label right with sufficient clearance from ticks; preferably label throughput “storage-only ingress bound” so the standalone figure retains the logical-capacity qualification already present in its prose caption. Current formula and plotted units agree; the two-thirds line is represented correctly on each scale.

**Confidence/support:** high for native CairoSVG clipping, medium for precise browser extent because browser cross-check was unavailable.

### PRES-3 — P3: Figure 5 erases its phase background bands

**Location:** `tools/render-rfc-figures.py:44,296–299`; `docs/assets/figures/figure-05-application-lifecycle.svg` (frame after phase rectangles).

**Evidence:** the phase-colored rectangles are followed by `<rect class="frame" ... fill="none"/>`, but `.frame{fill:#fff}` takes precedence over the SVG presentation attribute. The frame paints white over all phase bands. The native PNG shows a white plot despite three background rectangles in the source.

**Consequence:** hot/cold/overlap labels lose their background regions; row bars and dashed external continuations still communicate the main idea, so this is not a mechanism validity defect.

**Fix:** use an outline-only class or inline style `fill:none` for this frame. Keep “conceptual lifecycle” and illustrative-application qualification; the row lengths are not measurements and should not gain numeric implied durations.

**Confidence/support:** high; deterministic CSS precedence plus rendering.

### PRES-4 — P3: Contributor workflow lacks regeneration and review instructions

**Location:** `CONTRIBUTING.md:21`; `models/README.md:34–46`; `tools/render-rfc-figures.py:11–12`.

**Evidence:** contribution instructions ask for model tests specifically in `models/test_models.py`, although procurement tests have their own file. No contributor instructions identify the five generated docs SVGs, the three model SVGs/two CSVs, their source generators, or required validator command. Model README names regeneration commands but does not link to the three produced plots. The newly added checks detect staleness but do not tell a contributor how to repair it.

**Fix:** add one small generated-artifact table and commands to CONTRIBUTING or model README; require tests under `models/test_*.py`; instruct editing generators rather than SVG outputs and inspecting rendered changes after validation. Include prerequisites Python and PowerShell/rg for the wrapper. Retain both output directories: they separate explanatory figures from experimental results coherently.

**Confidence/support:** high; repository inspection. Accounted for new `check-docs.py` and `check-generated.py`; no duplicate request to implement them.

### PRES-5 — P2: Model figures lose the fixed-arrival and artificial-lane assumptions when viewed alone

**Location:** `models/render_charts.py:35–47,204–224`; `models/output/charge-coverage.svg`; `models/output/rejection-rate.svg`.

**Evidence:** visual titles/legends do not say arrivals are fixed or lanes have fixed equal capacity and cannot borrow. `_svg_start` stores description only in `<desc>`, not as visible text. Charge coverage does explicitly name the ex-post scarcity benchmark on its axis, but omits that it is a diagnostic rather than measured service cost. README states these qualifications clearly.

**Consequence:** an exported chart may be read as evidence that duration classes generally reject more traffic, or that term pricing covers economic cost. The plots are correct for their declared model; the defect is assumption portability.

**Fix:** use the substantial spare bottom space on bar figures for a visible footer: fixed synthetic arrivals; lanes fixed/equal/no borrowing; benchmark diagnostic, not operator cost. Add links to outputs from model README so their source context travels with normal navigation.

**Confidence/support:** high; direct rendered and source evidence. Not a new criticism of acknowledged null-model limitations.

## Navigation and minimal organization plan

The existing docs/appendices/models/tools split is sensible and needs no relocation. All 12 chapters and seven appendices have stable filenames; preserve them and the legacy section anchors. The inspected chapters have no consistent home/previous/next navigation, making the argument-first README path difficult to follow after entering a file. Coordinator already owns README restructuring: complete it with compact core-path links on each core chapter and a return-to-roadmap link on optional branches. Figure numbering skips 4, but no broken Figure 4 reference was found; explain legacy numbering in an asset manifest rather than renumbering cited figures. RESEARCH_TRACKING's heading already accurately scopes operator-market questions; descriptive link text is sufficient without a rename.

The local rubric is ignored through `.agents/`; contributor-visible guidance should summarize its key epistemic distinctions in CONTRIBUTING or an editorial guide instead of exposing local agent infrastructure. Public citation/license files are present. No filename/anchor migration is recommended.

## Figure-by-figure disposition

| Figure | Native visual result | Semantic/units check |
|---|---|---|
| 01 frontier | Left axis cropping (PRES-2); otherwise legible | MiB/s and days agree with S/T; first-order storage bound needs standalone qualification |
| 02 fee | Boundary label touches grid; no gross cropping | Conditional maturity conflict, absent null curve, inaccurate alt-text origin (PRES-1) |
| 03 fixed tail | Clean, readable, no clipping | Explicit logical-byte-time limitation; illustrative days and 4096-epoch endpoint consistent to displayed precision |
| 05 application lifecycle | Background bands hidden (PRES-3) | Conceptual axis; application durations illustrative and not protocol categories |
| 06 storage admission | CairoSVG subscript layout mangles formula and lacks ≲ glyph | Source formula and physical/logical units sensible; rendering portability remains unverified |
| charge coverage | Clean labels and bars | Diagnostic ratio axis explicit; add visible assumptions (PRES-5) |
| rejection rate | Clean labels and bars including zeroes | Percentage axis coherent; add fixed-arrival/equal-lane caveat (PRES-5) |
| stress occupancy | Three readable panels; orange dashes expose blue line under overlap | Normalized capacity units and epoch axes explicit; matching shared/term paths agree with fixed arrivals |

## Limitations and remaining verification

All eight images were visually inspected with CairoSVG only, not in GitHub Markdown or on narrow viewports. Browser inspection of a local SVG was rejected by the browser URL security policy; no workaround was attempted. Accordingly the Figure 6 subscript/≲ artifact is recorded as a CairoSVG export limitation, not a proven source defect in browser rendering. If PDF/export support is intended, use portable explicit subscript positioning and a font with the required glyph, or verify an alternate permitted renderer. The final coordinator should rerender corrected figures and inspect them once more. This pass did not verify external sources, screen-reader behavior, real client performance, or all prose semantics, which belong to other audit passes.

## Final verification pass

Rerendered and visually inspected all eight current published SVGs after coordinator corrections. Final native PNGs are under `audits/visual-qa/final/` with the original basenames. Figure 1 now has complete axis labels and accurately says “Storage-only ingress bound.” Figure 2 now calls 256 an illustrative boundary, explicitly leaves floors unresolved, promises only its actual convex benchmark, and avoids the grid-line collision. Figure 5 now displays the hot/cold/overlap backgrounds. Both model bar figures now display fixed-arrival/equal-nonborrowing-lane and diagnostic-cost assumptions in readable footers. Figures 3 and stress occupancy remain clean. Thus PRES-1, PRES-2, PRES-3, and PRES-5's visible corrections pass native-render inspection. CONTRIBUTING now supplies the output-source table, regeneration commands, prerequisites, general test pattern, and semantic/visual review requirements, resolving PRES-4 by text inspection.

Figure 6 still exhibits CairoSVG subscript/glyph problems. A temporary proof-of-fix at `audits/visual-qa/final/figure-06-portable-preview.svg` and `.png` has been rendered and visually inspected: replacing baseline-shift subscript tspans with literal underscore variable names fixes every label and leaves the numerator within its fraction rule; replacing unsupported ≲ with ≤ renders successfully when the subtitle explicitly identifies the formula as an approximate research bound. This is a recommendation to the coordinator, not an edit to published source or output. The temporary portable-preview.py records the first intermediate variant; the final preview SVG uses ≤ and the approximation subtitle.

No browser/local-HTTP workaround was attempted because the prior browser denial expressly prohibited achieving the same blocked action indirectly. README received source-level inspection only, not browser Markdown-layout verification. Final PNG evidence establishes native CairoSVG output quality, not responsive or GitHub-browser rendering behavior.

### Figure 6 closure

After the coordinator applied the portable-label correction to the generator and regenerated the published SVG, rerendered the actual `docs/assets/figures/figure-06-storage-admission-model.svg` into `audits/visual-qa/final/figure-06-storage-admission-model.png` and inspected it directly. All variable labels, the full numerator/denominator, inequality glyph, and approximate-bound subtitle are legible without overlap or clipping. The earlier native PNG under `audits/visual-qa/` retains the before evidence. Figure 6's CairoSVG portability issue is now closed. Together with the seven other final PNGs inspected in the preceding pass, all eight published figures pass this native-render visual QA. Browser/responsive and screen-reader limitations remain as documented; no known unaddressed defect remains within this presentation pass's scope.
