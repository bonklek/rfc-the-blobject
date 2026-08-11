# Is variable retention safe for rollups?

## 8. Security-critical applications and conditional graceful degradation

Variable retention is safe for a rollup only when the chosen window covers that rollup's recovery assumptions, or when another system has accepted the archival obligation before Ethereum's window closes.

At present, an application effectively purchases:

```text
immediate DA bandwidth
+
fixed protocol serving horizon.
```

Variable retention exposes a second control variable. An L2 may prefer a horizon `T_preferred` while treating a shorter horizon `T_application-min` (called `T_security-min` in some application discussions) as its hard floor. Under retention congestion it can shorten the former while bidding aggressively for ingress.

That option exists only if the application's security model actually permits it.

The payer and the users exposed to failure need not be the same actor. A sequencer may buy the lease while challengers, bridge users, or future node operators bear the cost of an undersized window. If an application publishes a machine-readable minimum, admission can require `T_selected >= T_application-min`. Without such a declaration, a sequencer choosing less retention than the application's user-facing security model needs is exercising delegated trust, not obtaining a protocol endorsement that the shorter horizon is safe.

For optimistic rollups, challenge windows are currently on the order of a week: OP Mainnet documents a seven-day challenge window (about 1,575 Ethereum epochs at current timing), while Arbitrum BoLD uses a default 6.4-day challenge period (about 1,440 Ethereum epochs). Retaining L2 input data on Ethereum for less than the challenge window does not automatically make the rollup insecure, but it changes what an honest challenger can assume. A party that comes online late may no longer be able to recover all relevant input data from Ethereum alone. Safety then depends on at least one honest watcher, archive, state-distribution system, or equivalent handoff having acquired the data during the shorter window. If a power-of-two maturity must cover either window without another assumption, the next class is 2,048 epochs—about 9.10 days.

`T_application-min` is not automatically equal to the challenge period. Still, shortening below that period can add a new assumption: some honest retriever or archive must acquire the data before Ethereum stops serving it.

Validity-proof systems can have a different lower bound because execution validity may be established quickly, but historical input data can still matter for state reconstruction, escape, proving continuity, and permissionless new-node sync. Fast proving does not by itself make retained data irrelevant.

The claim is:

> **Variable retention enables graceful degradation where the application’s proving, recovery, and archival architecture provides genuine retention elasticity.**

Conceptually:

```text
T_preferred
→
T_application-min
→
no further safe shortening.
```

At that boundary the application must compete for retention as well as ingress. Variable retention does not abolish the underlying security requirement.

This gives rollups a concrete incentive to prove rapidly, distribute state robustly, maintain several independent archives, and provide escape mechanisms. Those capabilities reduce their dependence on scarce Ethereum byte-time during stress.

---

## 9. Market feedback and failure modes

Variable retention can create a stabilizing response: as retained stock becomes expensive, applications with elastic demand shorten leases, causing data to expire sooner and releasing capacity faster than under a universal fixed horizon.

Schematically:

```text
high retained-stock utilization
→
higher byte-time price
→
shorter elastic leases
→
faster expiry
→
lower active stock.
```

This feedback may help, but it does not guarantee stability.

Several countervailing behaviors require simulation:

- users may front-load long prepaid leases when prices are temporarily low;
- correlated applications may all seek the maximum protocol-required retention during the same crisis;
- a wealthy attacker may intentionally occupy the general-retention pool;
- quantized classes may fragment otherwise usable capacity;
- renewal mechanisms may create synchronized expiry cliffs;
- storage savings may be offset by physical fragmentation from heterogeneous expiry.

The mechanisms have different jobs:

- **hard active-stock bounds** protect physical safety;
- **reserved headroom** prevents long leases from pre-consuming a short-duration lane, but does not prevent that lane itself from being flooded;
- **fees** allocate the remaining byte-time economically;
- **application security minima** determine how much demand can actually respond to price.

---
