# Illustrative operator economics and procurement control

This appendix makes the operator-market arithmetic executable enough to criticize. Every dollar rate below is arbitrary. The examples are **not parameter recommendations, cost estimates, forecasts, or claims about a sustainable Ethereum market**. They answer only how a stated service-price schedule scales with admitted bytes and duration.

## A deliberately artificial calibration

Assume:

```text
q_write     = $0.05 / GiB
q_retention = $0.001 / GiB-hour
T           = 4,096 epochs = 436.9067 hours
```

For `B_day` GiB admitted per day, the illustrative daily service payment is:

```text
P_day = q_write * B_day + q_retention * B_day * T.
```

The first term pays once for admitted write/flow work. The second values the full byte-time obligation created by one day's admissions; it is not the cash balance of a mature system on one particular day.

| Workload | Admitted data/day | Write component/day | Full-horizon retention component/day | Total/day | Annualized total |
|---|---:|---:|---:|---:|---:|
| 14 blobs/slot, 128 KiB/blob, 12 s slots | 12.3047 GiB | $0.62 | $5.38 | $5.99 | $2,186.80 |
| 32 MiB/slot | 225 GiB | $11.25 | $98.30 | $109.55 | $39,987.21 |
| 1 GiB/s | 86,400 GiB | $4,320.00 | $37,748.74 | $42,068.74 | $15,355,088.64 |

The first row uses the 14-blob target introduced by [EIP-8135's BPO2 schedule](https://eips.ethereum.org/EIPS/eip-8135). It is a dated baseline, not a claim that the target will remain 14. Binary GiB and MiB units are used throughout.

Under this invented schedule, explicit DA service rewards are economically small at the first workload and material only at much higher throughput. That result is mechanically caused by the assumed rates and volumes. It does not establish that the rates cover hardware, networking, repair, capital, risk, or profit at any row.

Shorter service windows change only the retention column. A one-hour object pays `$0.001/GiB` for retention instead of approximately `$0.4369/GiB` at 4,096 epochs, while its write component remains `$0.05/GiB`.

## An illustrative posted-price controller

The operator-market chapter intentionally does not select a controller. One toy update for simulation is:

```text
q_(k+1) = q_k * [1 + kappa * (C*_k - C_k) / C*_k]
```

where `C*_k` is target qualified supply and `C_k` is observed qualified supply. The executable model bounds the multiplicative change to `1 +/- max_step` and then applies an absolute price floor and ceiling. The controller therefore raises price under a measured shortage, lowers it under measured surplus, and cannot jump without bound in one epoch.

This is a feedback rule, not an oracle. It does not determine whether announced capacity is real, independent, correctly measured, or strategically withheld. Qualification lags, smoothing, reserves, delayed exits, and concentration limits remain separate requirements.

The model is in [`models/procurement.py`](../models/procurement.py), with focused tests in [`models/test_procurement.py`](../models/test_procurement.py).

## Posted prices versus reverse procurement

| Mechanism | Useful property | Principal risk in repeated procurement |
|---|---|---|
| Bounded posted-price controller | Predictable participation; no latency race; marginal supplier does not set one clearing price for all | Suppliers can withhold qualified capacity to move the observed shortage and later posted price |
| Sealed-bid uniform-price reverse auction | Discovers a supply curve without publishing the next price first | The marginal accepted bid sets payment for all accepted supply, inviting strategic bidding or coordinated withholding |
| Sealed-bid pay-as-bid reverse auction | Limits a single uniform clearing-price transfer | Rewards bid shading and information advantages; similar operators can receive different prices for the same duty |

Sealed bids hide individual offers before a round closes; they do not make a repeated market manipulation-proof. Posted prices likewise remove one auction-game surface without removing supplier market power. Simulations should compare the mechanisms under common ownership, Sybil identities, correlated failures, capacity withholding, demand shocks, and costly service qualification.

No mechanism should pay through a physical safety limit. If qualified supply remains below the required reserve at the service-price ceiling, the DA target must fall.
