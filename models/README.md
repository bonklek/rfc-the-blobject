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
