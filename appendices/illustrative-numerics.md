# Appendix: What do illustrative retention frontiers look like?

This appendix deliberately uses a hypothetical capacity. It demonstrates the geometry of `R≈S/T`; it does not estimate a safe Ethereum parameter.

Suppose a future DAS network can support:

```text
S = 64 TiB
```

of effective logical active retention. If every byte receives the same horizon `T`, the hard steady-state throughput frontier is `S/T`:

| Required-serving duration | Hard frontier |
|---|---:|
| 1 hour | 18.2 GiB/s |
| 1 day | 777 MiB/s |
| 7 days | 111 MiB/s |
| 14 days | 55.5 MiB/s |

If an operating target were set at two-thirds of that hypothetical envelope, the target frontiers would be:

| Required-serving duration | Two-thirds target |
|---|---:|
| 1 hour | 12.1 GiB/s |
| 1 day | 518 MiB/s |
| 7 days | 74.0 MiB/s |
| 14 days | 37.0 MiB/s |

The point is only:

> **The same retained-stock envelope supports radically different ingress rates depending on how much protocol-required byte-time applications purchase.**

`H_min` would reduce the general-purpose pool by an explicitly chosen amount. As §6 explains, that protects a short-duration resource lane against pre-consumption by long leases; it does not prevent an attacker from flooding the short lane itself. Future-starting reservations would additionally be bounded by the forward envelope introduced in §10.

Run the stock model for equivalent calculations:

```powershell
python models/stock.py frontier --capacity-tib 64 --durations-hours 1 24 168 336
```
