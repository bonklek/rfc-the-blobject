# How are capacity and pricing managed?

## 4. Flow and active retained stock

For the narrow spot-start mechanism, two quantities are initially sufficient.

Let `R_t` denote new data entering Ethereum DA around time `t`. This is the **flow** resource: propagation, coding, sampling, and real-time processing.

Let `S_t` denote the total logical data currently under an unexpired protocol serving obligation. This is the **active retained stock**.

If an object of size `B` is admitted at time `t` with duration `T`, it immediately increases active stock by `B` and remains in `S` until `t+T`. The protocol therefore faces two independently scarce resources:

```text
R_t ≤ R_max
```

and

```text
S_t ≤ K_safe,
```

where `K_safe` is the largest logical retained-data obligation the custody architecture is provisioned to serve safely.

This is the first major simplification produced by adversarial review. For leases that begin at admission, a separate forward hard-cap curve is not required for storage safety.

To see why, let `S_t(τ)` denote retained obligations that will still be alive at horizon `t+τ`, considering only leases already admitted at `t`. Because those leases can expire but no already-admitted lease begins later,

```text
S_t(τ) ≤ S_t(0) = S_t
     ∀ τ ≥ 0.
```

A new immediate lease of size `B` adds `B` for horizons `0≤τ≤ T`. Therefore, if

```text
S_t + B ≤ K_safe,
```

then the already-contracted retained stock cannot exceed `K_safe` at any later horizon merely because time passes.

Long leases can still crowd out later users, but they do so by occupying capacity **now**, not by secretly reserving a future stock that is invisible to the current cap. That is an allocation and liveness problem, not a hidden physical-safety problem.

---

## 5. Pricing guaranteed byte-time

The fee decomposition remains:

```text
F(B,T)
=
F_ingress(B;R_t)
+
F_ret(B,T;S_t).
```

Ingress prices the immediate flow burden. Retention prices a guaranteed amount of **byte-time**.

The simplest spot-start benchmark is:

```text
F_ret(B,T;S_t)
=
B · T · p_ret(u_t),

u_t = S_t / K_target,
```

with a marginal byte-time price that rises as active retained stock approaches its sustainable target. A deployable fee mechanism may need a duration premium, discrete maturity classes, or a more sophisticated base-fee update rule; the equation is a benchmark, not a final mechanism.

A hot/cold physical implementation refines this decomposition without changing the logical API. Every object incurs the common cost of fresh dispersal, coding, sampling, and whatever mandatory hot redundancy the DAS design requires. Only the post-transition obligation scales with the purchaser's longer retention choice. Schematically, for total service horizon `T≥ T_hot`,

```text
F(B,T)
≈
F_hot_DA(B;R_t)
+
F_cold(B,T-T_hot;S_t).
```

In a crude linear approximation,

```text
F(B,T)
≈
B · c_hot
+
B · (T - T_hot) · c_cold,
```

where the coefficients summarize physically different workloads rather than proposed constants. The paper should not assume that `c_hot` or `c_cold` is literally linear, nor assert a coding-overhead ratio before a concrete FullDAS design is fixed. The important point is that shortening retention cannot remove the initial hot-path cost; it can remove the continuing cold custody obligation.

This is intentionally less ambitious than pricing every point on a forward curve. The hard cap supplies safety. The fee market supplies economic allocation below that cap.

A prepaid fixed-duration lease has one important security property: once accepted, its serving horizon is not contingent on later fee increases. A “rent that must continuously be topped up” is simpler in some respects but changes the service semantics. Under future congestion or censorship, a rollup could lose retention before its promised security horizon. Continuous rent is therefore better understood as an application-layer or best-effort service unless the entire maximum obligation is prepaid or otherwise guaranteed at admission.

The retention fee should initially be understood as a **scarcity/admission charge on protocol byte-time**, not automatically as compensation to individual custodians. Ethereum can burn the fee while separately enforcing custody duties, just as blob fees need not be direct provider payments. A provider-reward system is a different mechanism.

### 5.1 What pricing cannot solve

No fee curve guarantees access against a sufficiently wealthy adversary willing to purchase the scarce resource. A high price makes hoarding expensive; it does not create capacity.

This distinction matters because the old forward-curve presentation implicitly asked pricing to do three jobs at once:

1. reflect byte-time scarcity;
2. enforce a physical safety bound;
3. preserve near-term capacity against strategic long leases.

The active-stock cap solves the second. A separately derived reserve can address the third. Pricing can then focus on allocation.

---

## 6. Deriving physical capacity and liveness headroom

The protocol should not begin with an arbitrary `C(τ)`. It should begin with a physical resource envelope.

Let `K_safe` denote the maximum logical retained stock compatible with the chosen node-resource target under the actual custody topology. In a concrete DAS design, deriving `K_safe` requires at least:

- erasure-coding expansion;
- the fraction of columns, rows, or cells each node class must custody;
- validator balance-dependent custody requirements;
- repair and re-replication overhead;
- serving bandwidth for historical requests;
- metadata and proof overhead;
- hardware targets and safety margin;
- heterogeneity across clients and node operators.

The protocol still makes a normative choice about what hardware envelope it wants to support, just as it does when choosing blob throughput. But the retained-stock ceiling should be **derived from that envelope**, rather than introduced as an independent market parameter.

The hot/cold design makes that derivation more physical. Let `γ_hot` denote the effective local storage expansion of the transient availability-establishment representation and `γ_cold` the effective local expansion of the sparse retained representation under a chosen custody topology. At throughput `R`, a first-order hot working set is on the order of

```text
M_hot
~
γ_hot · R · T_hot,
```

while the cold resident set is approximately

```text
M_cold
~
γ_cold · S_t.
```

If `M_budget` is the protocol's chosen local storage envelope, then a cold-stock limit should be derived only after reserving the hot working set, repair slack, metadata, and churn margin. Schematically:

```text
K_safe ≲ (M_budget - M_hot - M_repair - M_metadata) / γ_cold.
```

This is not yet a parameter proposal. It is a more useful research target than an abstract capacity percentage because every term can eventually be measured against a concrete custody and coding design. It also exposes a hardware asymmetry: the hot tier is dominated by write bandwidth, networking, coding, verification, and rapid repair, while the cold tier is dominated by capacity, historical serving, expiry bookkeeping, and slower reconstruct-and-repair.

A second quantity is then needed if Ethereum wants to guarantee that long leases cannot consume every byte of capacity required by urgent short-lived traffic.

Suppose the protocol wants to preserve the ability to admit at least `r_reserve` bytes per unit time of minimum-retention traffic, where every such byte must remain served for at least `T_min`. A first-order steady-state reserve is:

```text
H_min ≈ r_reserve · T_min.
```

Ordinary longer leases would therefore be limited to approximately:

```text
K_general
=
K_safe - H_min,
```

while the reserved region remains available to the protocol-defined spot/JIT lane.

This is not offered as a finished parameterization. Bursts, repair slack, node churn, and changing ingress limits require additional margins. Its value is conceptual: **headroom can be tied to an explicit liveness objective instead of percentages chosen by maturity.**

There is already an adjacent Ethereum design pattern. The draft Blob Streaming EIP separates AOT from JIT capacity and includes `JIT_RESERVED`, a minimum capacity that AOT reservations cannot consume. A retention reserve would apply the same principle to stock rather than flow.

---

## 7. Competing physical implementations and deployment fallbacks

Adversarial review still suggests that arbitrary continuous `T` should remain the **service abstraction**, but it no longer implies that maturity quantization is the preferred long-run physical design.

There are two qualitatively different ways to make heterogeneous expiry tractable.

### 7.1 Maturity-aligned physical classes

The conservative implementation is to round requested durations into a small number of physical maturities—for example, minutes, hours, days, and the current full horizon—and pack only similar maturities into the same persistent coding domain.

This has substantial advantages:

- simple expiry accounting;
- maturity-homogeneous packing;
- bounded metadata;
- predictable repair horizons;
- easier pricing and simulation;
- compatibility with physical representations that cannot become sparse.

Its cost is fragmentation. Capacity can be idle in one maturity class while another is congested, and users lose some allocative precision. A binary version—one ephemeral lane plus one full-retention lane—is the simplest possible experiment.

### 7.2 Renewable short leases

Ethereum could sell only a short base horizon and permit extensions before expiry.

This avoids long guaranteed commitments and makes current stock easy to price. But it does **not** reproduce a prepaid long guarantee. A rollup that must renew under future congestion is exposed precisely when it most values continuity. If renewal capacity is guaranteed in advance, the design has recreated a future retention commitment under another name.

Renewal is therefore attractive for elastic applications, not a full substitute for guaranteed maturity.

### 7.3 Continuously metered rent

A prepaid balance could decay with byte-time until the payer tops it up or a maximum expiry is reached. This is elegant for downstream storage services and receipt-terminated retention, but weakens the base protocol guarantee if the service can terminate merely because future prices rise.

### 7.4 Hot availability representation → cold independently expiring custody

The more ambitious implementation is to let the **physical representation change after fresh availability has been established**.

The logical object remains the same committed blob and the application still chooses its serving horizon. Under the hood, however, the network first uses the dense redundancy and repair structure optimized for fast DAS. Once a protocol-recognizable hot phase ends, it discards representation components needed only for fresh availability amplification and keeps an independently reconstructable, independently expiring representation for historical serving.

For a two-dimensional FullDAS-style code, the working design is:

```text
hot dense 2D availability coding
→
cold sparse row-local custody
```

Under current PeerDAS, which does not add the same cross-row second-dimensional parity, the analogous transition is mainly from dense block-wide column-sidecar packaging to sparse cell-level historical serving.

This design family is developed in §17. If it works, it preserves continuous logical lease choice without forcing long-lived and short-lived blobs into separate hot coding domains. If it fails because the richer codeword must remain intact for the entire serving horizon, maturity classes become the natural fallback.

### 7.5 Full variable retention

Arbitrary `T` still maximizes allocative expressiveness and keeps the logical API clean. The physical question is now sharper:

> **Can Ethereum preserve one highly redundant representation only as long as it is needed for fresh availability, then move still-live objects into an independently expirable serving representation without changing their commitments?**

The paper therefore treats **continuous variable retention as the semantic target, hot/cold representation transition as the leading compatibility hypothesis, and maturity-aligned classes as the conservative fallback**.

---
