# Is variable retention safe for rollups?

## 8. Security-critical applications and conditional graceful degradation

Variable retention creates a potential resilience property for rollups and other security-critical DA users, but adversarial review narrows the claim.

At present, an application effectively purchases:

```text
immediate DA bandwidth
+
fixed protocol serving horizon.
```

Variable retention exposes a second control variable. An L2 may have a preferred horizon `T_preferred` and a shorter horizon `T_security-min`. Under retention congestion it can shorten the former while bidding aggressively for ingress.

The benefit is real only if the application’s security model actually admits such elasticity.

For optimistic rollups, challenge windows are currently on the order of a week: OP Mainnet documents a seven-day challenge window, while Arbitrum BoLD uses a default 6.4-day challenge period. Retaining L2 input data on Ethereum for less than the challenge window does not automatically make the rollup insecure, but it changes what an honest challenger can assume. A party that comes online late may no longer be able to recover all relevant input data from Ethereum alone. Safety then depends on at least one honest watcher, archive, state-distribution system, or equivalent handoff having acquired the data during the shorter window.

Thus `T_security-min` is not simply “the challenge period,” but shortening below that period can add a new online-retriever or archival assumption.

Validity-proof systems can have a different lower bound because execution validity may be established quickly, but historical input data can still matter for state reconstruction, escape, proving continuity, and permissionless new-node sync. Fast proving does not by itself make retained data irrelevant.

The defensible claim is therefore:

> **Variable retention enables graceful degradation where the application’s proving, recovery, and archival architecture provides genuine retention elasticity.**

Conceptually:

```text
T_preferred
→
T_security-min
→
no further safe shortening.
```

At that boundary the application must compete for retention as well as ingress. Variable retention does not abolish the underlying security requirement.

This still creates an architectural incentive. Rollups that can prove rapidly, distribute state robustly, maintain plural independent archives, or provide escape mechanisms can convert those capabilities into lower dependence on scarce Ethereum byte-time during stress.

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

But this is not an automatic stability theorem.

Several countervailing behaviors require simulation:

- users may front-load long prepaid leases when prices are temporarily low;
- correlated applications may all seek maximum retention during the same crisis;
- a wealthy attacker may intentionally occupy the general-retention pool;
- quantized classes may fragment otherwise usable capacity;
- renewal mechanisms may create synchronized expiry cliffs;
- storage savings may be offset by physical fragmentation from heterogeneous expiry.

The key separation after adversarial review is:

- **hard active-stock bounds** protect physical safety;
- **reserved headroom** protects a chosen minimum-liveness lane;
- **fees** allocate the remaining byte-time economically;
- **application security minima** determine how much demand can actually respond to price.

---
