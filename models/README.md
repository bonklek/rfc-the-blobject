# Models

These dependency-free Python programs turn the RFC's null models into reproducible experiments. They are not Ethereum parameter recommendations or security proofs.

## Active stock and expiry

`stock.py` implements the non-normative epoch ring from §4.1, including capacity rejection, expiry, snapshots, and reorg restoration.

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

## Tests

```powershell
python -m unittest discover -s models -p "test_*.py"
```
