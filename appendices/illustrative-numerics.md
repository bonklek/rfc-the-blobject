# Appendix: What do illustrative retention frontiers look like?

The capacity in this appendix is hypothetical. The calculations show the geometry of `R≈S/T`; they do not estimate a safe Ethereum parameter.

For the longest row, it uses the current mainnet Fulu minimum serving range of 4,096 epochs. At 32 slots per epoch and 12 seconds per slot, that is 1,572,864 seconds, or approximately 18.2 days. Current clients are required to serve at least that range and may serve longer. In the conservative variable-retention proposal, this existing fixed requirement becomes the candidate `T_max`; it is not the proposed `T_min` and is not a pruning deadline.

Suppose a future DAS network can support:

```text
S = 64 TiB
```

of effective logical active retention. If every byte receives the same horizon `T`, the hard steady-state throughput frontier is `S/T`:

| Required-serving duration | Approximate wall-clock time | Hard frontier |
|---:|---:|---:|
| 256 epochs | 1.14 days | 683 MiB/s |
| 512 epochs | 2.28 days | 341 MiB/s |
| 1,024 epochs | 4.55 days | 171 MiB/s |
| 2,048 epochs | 9.10 days | 85.3 MiB/s |
| 4,096 epochs | 18.20 days | 42.7 MiB/s |

If an operating target were set at two-thirds of that hypothetical envelope, the target frontiers would be:

| Required-serving duration | Approximate wall-clock time | Two-thirds target |
|---:|---:|---:|
| 256 epochs | 1.14 days | 455 MiB/s |
| 512 epochs | 2.28 days | 228 MiB/s |
| 1,024 epochs | 4.55 days | 114 MiB/s |
| 2,048 epochs | 9.10 days | 56.9 MiB/s |
| 4,096 epochs | 18.20 days | 28.4 MiB/s |

The calculation establishes one relationship:

> **The same retained-stock envelope supports radically different ingress rates depending on how much protocol-required byte-time applications purchase.**

`H_min` would reduce the general-purpose pool by an explicitly chosen amount. As §6 explains, that protects a short-duration resource lane against pre-consumption by long leases; it does not prevent an attacker from flooding the short lane itself. Future-starting reservations would additionally be bounded by the forward envelope introduced in §10.

Run the stock model for equivalent calculations:

```powershell
python models/stock.py frontier --capacity-tib 64 --durations-epochs 256 512 1024 2048 4096
```
