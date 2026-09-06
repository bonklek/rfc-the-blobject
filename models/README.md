# Models

These dependency-free Python programs turn the RFC's null models into reproducible experiments. They are not Ethereum parameter recommendations or security proofs.

## Active stock and expiry

`stock.py` is an abstract companion to §4.1. It scans a dictionary of leases to model capacity rejection, elapsed slot-based expiry, delayed reclamation, and snapshot restoration. Its `retained_bytes` counter corresponds to `obligated_bytes` in the sketch. Synthetic caller-supplied sizes and local ordinal identities support experiments; they do not implement fixed-blob admission or canonical fork identity. Snapshot restoration tests accounting, not recovery of pruned data. No ring-buffer or storage-engine performance claim is made.

```powershell
python models/stock.py frontier --capacity-tib 64 --durations-epochs 256 512 1024 2048 4096
```

## Pricing hypotheses

`pricing.py` compares plain byte-epoch accounting, a convex duration premium, quantized maturities, expected-scarcity pricing, and an auction reserve-price proxy. Duration inputs are epochs.

```powershell
python models/pricing.py --size 131072 --duration-epochs 4096 --utilization 0.75
```

The output is useful only for relative comparisons under shared arbitrary units.

`pricing.py` uses fixed RFC example maturities by default. The reference
duration, maturity set, and expected utilization at expiry are explicit CLI
inputs rather than values derived from the quoted request.

## Normalized spot-allocation scenarios

`spot_simulation.py` combines immediate-start active-stock accounting with the
RFC's pricing hypotheses. It uses synthetic capacity and fee units to compare
steady demand, long-lease front-loading, correlated maximum-duration demand,
adversarial occupation, maturity fragmentation, and an expiry cliff.

```powershell
python models/spot_simulation.py
python models/spot_simulation.py --output-dir models/output
python models/render_charts.py
```

The output reports admission, rejection, charge coverage against an ex-post
scarcity benchmark, peak occupancy, stranded lane capacity, and peak expiry.
It is a falsification aid, not a demand forecast or parameter recommendation.
The chart command renders SVG comparisons of rejection rates, ex-post charge
coverage, and active-stock paths without adding runtime dependencies.

The scenario runner holds arrivals fixed. As a result, term-premium pricing
changes charges but not admission; modeling a demand response would require an
explicit willingness-to-pay hypothesis. The maturity-lane null model divides
capacity equally and does not allow capacity to float between lanes, making it
an intentionally severe fragmentation test. Charge coverage compares the
upfront quote with a diagnostic ex-post utilization-price path, not with a
measured social or operator cost.

## Operator-service procurement

`procurement.py` implements the non-normative bounded posted-price controller from the operator-economics appendix. It raises or lowers an illustrative service price from the gap between target and qualified supply, subject to a per-update step bound and absolute floor and ceiling.

The model does not determine whether announced capacity is real, independent, or strategically withheld. It exists to make those controller dynamics reproducible.

## Cold-custody survivability

`cold_custody.py` evaluates the independent-failure checkpoint model from §17.4.

```powershell
python models/cold_custody.py `
  --cells 128 `
  --threshold 64 `
  --custodians 10000 `
  --replicas 2 `
  --failure-probability 0.1 `
  --duration-epochs 4096 `
  --repair-interval-epochs 8 `
  --p-max 0.000001
```

Correlated failures, adaptive adversaries, network partitions, non-serving online nodes, and repair failure are deliberately outside this null model. A result that passes here is not sufficient evidence for protocol safety.

The output names the independent-cell-loss, independent-interval, and full-repair assumptions. `meets_target_under_null_model` compares the directly computed failure tail with the target; rounded survival near one must not be used for that decision. The former `meets_target` output name has been replaced to make this scope explicit. The calculation retains interval risks in an 80-digit Decimal context through checkpoint composition, then converts public probability outputs to floats. Final probabilities below float range may display as zero; replica selection compares the Decimal risk directly. Finite numerical precision and the statistical assumptions still limit this research calculator.

For example, two cells held by one custodian fail together when that custodian fails. At failure probability 0.1 and reconstruction threshold one, their actual survival is 0.9; independent-cell arithmetic gives 0.99. The population argument only checks replica feasibility and does not simulate assignment overlap.

The scenario API rejects observation horizons that end before an arrival's full billed lease expiry, so its admission totals and ex-post charge coverage cannot silently include unobserved service.

## Published outputs

- [Rejection rates](output/rejection-rate.svg), [charge coverage](output/charge-coverage.svg), and [occupancy paths](output/stress-occupancy.svg).
- [Scenario summary](output/spot-summary.csv) and [time series](output/spot-timeseries.csv).

See the [artifact map](../docs/document-map.md) and [regeneration guide](../CONTRIBUTING.md#generated-artifacts-and-checks). These charts use fixed synthetic arrivals, equal non-borrowing maturity lanes, and a diagnostic utilization-price benchmark; they are not measured cost or demand evidence.

## Tests

```powershell
python -m unittest discover -s models -p "test_*.py"
```
