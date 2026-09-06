# How do hardware and DA operator markets scale?

## Short answer

The active-stock model limits how much logical retention Ethereum may admit. It leaves the supply side unanswered: who installs the hardware, how a large custody duty can be divided among small operators, and how those operators are paid for writes, serving, repair, and retained byte-time.

This chapter examines four parts of that supply side:

1. model per-node writes separately from resident storage;
2. place data on hardware suited to its remaining lifetime;
3. decompose large logical custody duties across fractional operators;
4. separate the scarcity burn from posted service payments for qualified capacity.

Every implementation must account for writes, placement, and assignment granularity. Fractional pools and separate service payments are optional responses to those constraints; a base experiment can retain the existing custody population. These extensions become relevant only if a proposed throughput target exceeds the hardware envelope of ordinary validator duties.

---

## 1. Stock and churn are different hardware constraints

Let:

- `R` be the logical ingress rate;
- `rho` be the physical write expansion from coding and replication;
- `f` be the fraction of that expanded stream assigned to one node;
- `alpha` be local write amplification, including staging, compaction, repair, and metadata;
- `T` be the required-serving duration.

A first-order per-node write-rate model is:

```text
W_local ≈ alpha · f · rho · R.
```

The corresponding resident stock is:

```text
S_local ≈ f · rho · R · T.
```

Together, these equations reveal a limit that the aggregate frontier `R≈S/T` hides:

> **Shortening retention reduces resident stock, but it does not reduce the steady write stream created by the same ingress rate.**

Nor does it reduce live network traffic. The [backbone-scale appendix](../appendices/backbone-scale-limits.md) adds the corresponding `N · b ≳ e · q · R` conservation bound, shrinking-custody-fraction examples, and object/proof-count stress tests.

A live set can fit on a device even while the write stream wears that device out. The `K_IO` component of `K_safe_vector` can bind before `K_storage`; it is not a secondary implementation detail.

### Illustrative endurance check

Suppose, only for scale:

```text
R     = 1 GiB/s
rho   = 2
f     = 1/64
alpha = 2
```

Then:

```text
W_local ≈ 0.0625 GiB/s
        ≈ 5,400 GiB/day
        ≈ 5.8 TB/day
        ≈ 2.1 PB/year.
```

With an 8-epoch serving horizon—about 51.2 minutes—the steady resident set is only:

```text
S_local ≈ 96 GiB.
```

The capacity requirement looks modest; the endurance requirement does not. A 3.84 TB SSD rated for one full drive write per day would have a nominal workload budget of 3.84 TB/day, below this example's 5.8 TB/day. Shortening the horizon below 8 epochs would reduce `S_local` again while leaving the 5.8 TB/day write stream approximately unchanged.

This is an illustrative stress calculation, not an Ethereum target or a recommendation for a particular device. A real model must measure `rho`, `f`, and especially `alpha` from the selected coding, client, filesystem, repair policy, and failure process. It must also include burst writes, read amplification, thermal throttling, device replacement, and correlated wear.

---

## 2. Expiry is physical scheduling metadata

Once remaining lifetime is explicit, a storage scheduler can treat it as more than fee metadata.

| Remaining lifetime | Candidate placement | Dominant concern |
|---|---|---|
| 1–8 epochs (~6.4–51.2 minutes) | DRAM or a bounded circular-memory/disk buffer | latency and sustained overwrite rate |
| 8–64 epochs (~51.2 minutes–6.83 hours) | high-endurance NVMe | write endurance and rapid repair |
| 64–1,024 epochs (~6.83 hours–4.55 days) | general SSD tiers | balanced endurance, capacity, and serving |
| 2,048–4,096 epochs (~9.10–18.20 days) | capacity-oriented SSD or sequential HDD tiers | capacity, handoff, and slower repair |
| Archive | downstream retention networks | durable proofs, retrieval, and renewal |

The table describes workload classes, not normative hardware. Operators may implement several classes on one device or use a different medium where measurements justify it.

Remaining lifetime can inform:

- whether a cell should be copied to a colder tier at all;
- whether repairing it costs more than the value of its remaining service;
- how much overlap is required during a custody handoff;
- which devices receive new writes so wear remains balanced;
- how much spare capacity each tier must maintain;
- whether repair should be eager, batched, or allowed to wait for a scheduled expiry.

Repair policy must still satisfy the lease's survivability target. “Near expiry” cannot be a license to drop the object early. The useful optimization is to choose the cheapest schedule that preserves the target probability through the declared end of service.

A lifecycle-aware physical path can then look like:

```text
fresh bytes
    -> hot dispersal and sampling buffer
    -> duration-matched custody tier
    -> optional downstream archive handoff
    -> expiry of the protocol duty and physical reclamation
```

The path also provides a concrete reason to expose absolute expiry to custody software: it becomes an input to placement, repair, wear balancing, and exit planning.

---

## 3. Fractional DA pools

A large logical custody obligation need not imply one equally large physical operator.

For example:

```text
4 TB logical pool obligation
    -> 8 × 500 GB contributor allocations
```

This arithmetic intentionally omits replication, coding expansion, and spare capacity, all of which increase the physical requirement. The point is that the duty can be divided. A pool can present one accountable service boundary while routing independently verifiable cells across many smaller contributors.

EthStorage provides concrete, though non-equivalent, implementation precedent for this assignment scale. Its pinned [storage-contract deployment template](https://github.com/ethstorage/storage-contracts-v1/blob/513ec70e23a15db828dbd99f03714aada3484ce3/.env.template) configures `SHARD_SIZE_BITS=39`, approximately 512 GiB, and its [provider guide](https://github.com/ethstorage/ethstorage-doc/blob/8ba215431220c1bc8518833a91a5f35c334d513e/storage-provider-guide/tutorials.md) calls for at least 550 GB of free storage for one data shard, with 8 GB RAM; NVMe is recommended for full sampling speed. That does not establish that eight such machines can safely implement a 4 TB Ethereum DA pool: EthStorage has different proofs, reads, networking, replication, repair, and trust boundaries. It does show that a protocol-accounted storage responsibility can be divided into independently operated shards near the illustrative 500 GB contributor size rather than requiring every provider to hold the whole logical dataset.

The closest analogy is a fractional staking pool, but the duty is more operationally demanding. A DA pool must continuously:

- qualify contributor hardware and network service;
- assign authenticated cells pseudorandomly;
- maintain replica and failure-domain diversity;
- reserve hot and cold spare capacity;
- measure serving, write, and repair performance;
- rebalance device wear rather than only byte occupancy;
- overlap assignments during joins and delayed exits;
- reconstruct and repair data when contributors fail;
- attribute rewards and losses without trusting self-reported capacity.

The pool must not become a new trusted custodian. Assignments should be derivable or auditable, cells should remain verifiable against the original commitment, and no coordinator should be able to satisfy a service check with capacity that was merely pledged on paper. Pool-level bonds or penalties may align operators, but they do not prove that the underlying contributors are independent.

Nor does a cheap identity make the duty enforceable. A NodeID can identify an assignment without giving the protocol anything durable to penalize. A strong retention service needs a bonded or otherwise accountable, Sybil-resistant party at the protocol-visible boundary. If a pool carries that accountability for its contributors, its bond and internal controls must survive repair, reassignment, and handoff rather than ending when a contributor disappears.

### Native and pooled variants

Two deployment forms should be distinguished:

1. **Protocol-visible contributors.** Ethereum assigns and measures fractional duties directly. This provides the cleanest concentration data but expands consensus and networking complexity.
2. **Protocol-visible pools.** Ethereum sees a smaller number of accountable pools, which internally divide duties. This is easier to integrate but can hide common ownership, correlated hardware, and coordinator failure.

A hybrid could require pools to commit to contributor and failure-domain metadata without placing every scheduling decision in consensus. That metadata is still vulnerable to Sybil identities and false independence claims. Concentration measurement must therefore be treated as evidence with uncertainty, not a solved decentralization oracle.

### Handoffs and exits

Instant exit is incompatible with retained-serving obligations. A contributor or pool that stops accepting new work should remain responsible for existing assignments until one of the following occurs:

- the cells expire;
- an authenticated replacement accepts them after an overlap period;
- the pool reconstructs and reassigns them under a protocol-recognized handoff.

Multi-epoch capacity commitments and delayed exits make procurement more predictable and reduce the ability to withdraw capacity immediately after a price change. Accountability must overlap the data transfer: the outgoing party cannot shed its obligation before the replacement has accepted and demonstrated custody, and the incoming party must be identifiable and punishable for later non-service. These rules create operational lock-in, so commitment length should be derived from repair and replacement time rather than used as an arbitrary economic penalty.

---

## 4. Separate scarcity from hardware service

### Current Ethereum baseline

Current PeerDAS specifies custody, sampling, and serving duties, but [EIP-7594](https://eips.ethereum.org/EIPS/eip-7594) does not define a distinct per-byte DA-service payment to the participant performing each duty. Validator economics compensate the validator role as a whole; non-validator nodes do not acquire a `q_write` or `q_retention` claim merely by serving data. [EIP-4844](https://eips.ethereum.org/EIPS/eip-4844)'s blob base fee is deducted and burned rather than paid to DA custodians.

| Current duty or payment | Separate DA-service reward? |
|---|---:|
| PeerDAS custody | No |
| Sampling | No |
| Serving assigned cells or columns | No |
| Voluntary extra custody | No |
| Blob base fee | Burned, not paid to providers |

The operator payment below is therefore a new candidate mechanism, not a redirection already implicit in PeerDAS. Introducing it would require a positive case that specialized service procurement improves safety or credible supply enough to justify its expenditure, qualification, and capture risks.

The base RFC treats ingress and retention fees primarily as admission charges. If Ethereum additionally procures operator hardware, one candidate decomposition is:

```text
F_DA
=
F_scarcity_burn
+
q_write · B
+
q_retention · B · T.
```

Here:

- `F_scarcity_burn` rises with demand and rations protocol capacity;
- `q_write · B` pays for measured hot-path writes, dispersal, and related flow work;
- `q_retention · B · T` pays for the admitted retained byte-time obligation.

The units must be defined over the physical accounting basis selected by the protocol. If `B` is logical bytes, the posted rates must incorporate expected coding, replication, repair, and service overhead. If physical duty units are used instead, the conversion from logical service to duty units must be deterministic and auditable.

This **hybrid fee** is not a relabeling of the present blob base fee. Burning the scarcity component keeps the capacity controller from promising whatever price suppliers demand. The service component recognizes that a deliberately expanded hardware role differs from an ordinary validator duty funded implicitly through issuance and transaction fees.

### Payment requires qualified service

Capacity announcements alone should not earn rewards. Service payment should depend on an operator remaining qualified and accepting assignments, with some combination of:

- admission benchmarks for sustained writes, reads, and network service;
- observed availability and repair telemetry;
- randomized retrieval or custody challenges where safe;
- assignment receipts and handoff records;
- delayed settlement or clawback for provable non-service;
- conservative treatment of ambiguous network failures.

None of these measurements by itself proves continuous retrievability. Challenge systems also create location leakage, adaptive-targeting, false-positive, and correlated-slashing risks. The enforcement levels in §2.2 therefore remain applicable: posted service rewards do not automatically turn protocol-required service into a cryptographic proof of service.

The mechanism must also specify how rewards interact with validator issuance, pool fees, repair reserves, and penalties. Otherwise the same duty can be overpaid, or repair can become an unfunded externality.

---

## 5. Adaptive posted procurement prices

One procurement option is a posted price that adjusts periodically. Operators would not compete in a latency race or a repeated uniform-price reverse auction.

At each procurement epoch, the protocol observes qualified capacity committed for future service and updates:

```text
q_write
q_retention
```

toward target reserve margins. Conceptually:

```text
qualified supply below target reserve
    -> raise the relevant posted price within a bounded step

qualified supply above target reserve
    -> lower the relevant posted price within a bounded step
```

Separate signals are necessary because the hot write tier and cold retention tier can clear at different prices. A single rate can overpay cheap capacity while failing to recruit endurance and networking.

Posted prices offer several advantages:

- small operators need not run low-latency bidding infrastructure;
- the marginal accepted operator does not set one clearing price for all supply;
- capacity can commit for multiple epochs instead of appearing only when prices spike;
- bounded adjustments make revenue and protocol expenditure less discontinuous.

They do not eliminate manipulation. Operators can withhold supply, split identities, coordinate exits, or create the appearance of independent capacity. The mechanism therefore needs defenses at the market-structure layer.

### Market-power defenses

Candidate controls include:

- **multi-epoch commitments:** accepted capacity remains available across several procurement epochs;
- **delayed exits:** withdrawal is announced early enough to repair and replace live assignments;
- **bounded price changes:** neither a transient shortage nor one manipulated report causes an unbounded step;
- **pseudorandom assignments:** operators cannot select only cheap-to-serve objects or collude on predictable cells;
- **service-price ceilings:** the protocol publishes the maximum rate it will pay for each duty class;
- **safe-target reduction:** if qualified supply is insufficient at the ceiling, lower the safe DA target rather than capitalize cartel rents;
- **concentration monitoring:** track pool share, shared control, client and hosting diversity, geographic and network correlation, and the fraction of assignments that can fail together.

One constraint overrides the procurement design:

> **Procurement prices may recruit capacity, but they must never substitute for a physically supportable DA target.**

If the market cannot supply the target within the ceiling and reserve requirements, the safe response is less protocol capacity. The target can rise again only after qualified supply and measured performance recover.

### A controller, not an oracle

The observed supply signal will be delayed and noisy. A deployable controller needs:

- a qualification lag so temporary capacity cannot move the price immediately;
- separate entry and exit reserves;
- smoothing or hysteresis to prevent oscillation;
- explicit treatment of pledged, assigned, degraded, and spare capacity;
- limits on how much one administrative domain can count toward the safety target;
- public data sufficient to reproduce every price update.

No specific controller is proposed here. Simulation should compare posted-price control with reverse auctions, fixed subsidies, and ordinary validator-funded duties under honest entry, correlated failures, supply withholding, Sybil pooling, and demand shocks.

One non-normative controller is developed in the [illustrative operator-economics appendix](../appendices/illustrative-operator-economics.md):

```text
q_(k+1) = q_k * [1 + kappa * (C*_k - C_k) / C*_k],
```

with bounded multiplicative movement plus an absolute floor and ceiling. It exists to make convergence and withholding attacks simulatable, not to select an update rule. The appendix also compares posted prices with sealed-bid uniform-price and pay-as-bid reverse procurement. In a repeated uniform-price auction, a marginal accepted bid can set the payment for all accepted supply, so coordinated withholding and strategic bidding remain first-order concerns.

---

## 6. End-to-end operator architecture

The pieces compose as follows:

```text
application demand
    -> scarcity-priced admission
    -> AOT or JIT dispersal duty
    -> hot write-tier assignment
    -> publication-time DAS
    -> duration-aware cold assignment
    -> serving, repair, and handoff
    -> expiry or downstream archive

qualified operator supply
    -> multi-epoch commitment
    -> posted q_write / q_retention / q_history
    -> pseudorandom fractional assignments
    -> measured service and delayed settlement
```

This connects the logical retained-stock market to actual devices. It also shows exactly what variable retention can and cannot buy:

- it can lower resident stock and avoid unnecessary cold-tier writes;
- it can make repair and handoff aware of remaining service value;
- it cannot eliminate initial propagation, coding, or hot writes;
- it cannot manufacture independent operators merely by paying more;
- it cannot safely exceed the measured hardware envelope.

The third rate applies only when a lifecycle includes a sparse history tail. Rather than charging `q_retention * B * infinity`, the protocol can settle `q_history,node * f_tail,node * B * Δt` for one qualifying node's local duty in each service interval. Aggregate payment and security depend on the full custody profile and overlapping assignments; a local sampling fraction is not the system's retained fraction. Long-run custodians remain subject to continuing qualification, repair, and handoff. Protocol-generated L1 history needs an explicit funding channel because there may be no user blob payer. The [Lean lifecycle chapter](10-how-does-lean-ethereum-change-the-proposal.md#6-how-does-lifecycle-pricing-change) develops this distinction.

### 6.1 Illustrative operator-market scenarios

The following scenarios show scaling relationships rather than forecast costs.

The [illustrative operator-economics appendix](../appendices/illustrative-operator-economics.md) also applies deliberately arbitrary dollar rates to a dated 14-blob target, 32 MiB/slot, and 1 GiB/s. It is a dimensional sanity check, not a price recommendation or forecast.

**Fractional capacity.** Suppose 10,000 contributors each commit 256 GB. Gross pledged capacity is 2.56 PB. If the duty requires `rho=2` physical bytes per logical byte and the pool reserves spare capacity equal to 20% of its assigned physical capacity, the maximum first-order logical obligation is:

```text
2.56 PB / (2 · 1.20) ≈ 1.07 PB.
```

Common ownership or one hosting domain could make the 10,000 identities far less valuable than 10,000 independent failure domains. The arithmetic establishes capacity, not decentralization.

**Write-heavy versus retention-heavy payment.** Define the service-price crossover:

```text
T_star = q_write / q_retention.
```

Then one object's service payment can be written:

```text
q_write · B · (1 + T / T_star).
```

If, purely for comparison, `T_star=256 epochs`—about 1.14 days—the normalized service payment is:

| Required-serving duration | Payment relative to `q_write · B` |
|---:|---:|
| 8 epochs (~51.2 minutes) | 1.03125× |
| 256 epochs (~1.14 days) | 2× |
| 4,096 epochs (~18.20 days) | 17× |

All three objects pay the same write component per byte. The retention component changes with duration. Changing `T_star` changes the numbers and reveals whether the procured market is dominated by hot-path work or retained capacity.

**Supply shortage.** Suppose the protocol target requires 1 PB of qualified cold duty plus a 20% reserve, but only 800 TB remains qualified at the maximum posted service price. The safe response is not to record 1.2 PB of capacity or raise the price without bound. Admission must fall to the capacity supportable by the 800 TB supply after repair and reserve margins. This reduces new commitments only. Outstanding leases still require their admitted service: funded replacement capacity, repair reserves, enforceable exit notice, and an emergency shortfall policy must cover them. If those mechanisms cannot preserve the service, it is a service failure, not a safe retroactive reduction of the promised obligation.

---

## 7. Research and deployment sequence

A conservative sequence is:

1. measure present PeerDAS client write amplification and per-custody-group service cost;
2. publish workload traces for hot writes, resident stock, requests, repair, and expiry;
3. prototype duration-aware placement without changing consensus rewards;
4. test fractional pools with auditable cell assignment and explicit failure domains;
5. simulate posted-price controllers and supply-withholding attacks;
6. introduce service rewards only after the duty, qualification rule, and non-service evidence are defined;
7. raise the DA target only after qualified supply exists at or below the service-price ceiling.

The operator market should be judged against two baselines: ordinary validator custody with no separate provider payment, and a simpler small set of protocol-defined operator classes. Fractionalization and adaptive procurement are justified only if they expand credible independent supply enough to offset their coordination, measurement, and capture risks.

---

## 8. Open questions

### Physical accounting

- What are measured values of `alpha`, `rho`, and `f` for candidate PeerDAS and FullDAS paths?
- Which resource binds first for each duration class: network, writes, capacity, serving, repair, or compute?
- How should device wear and replacement reserves enter the physical safety envelope?

### Fractional operation

- What is the smallest independently verifiable assignment unit?
- Can pools prove contributor diversity without exposing operators to targeted attacks?
- What overlap and spare fraction keeps handoffs safe under correlated exits?
- Who pays for reconstruction when a contributor fails?

### Procurement

- Which observable supply measure is costly enough to fake but cheap enough for small operators to provide?
- How quickly may `q_write` and `q_retention` adjust without oscillation or easy withholding attacks?
- If canonical data receives a recurring `q_history` service, who funds it and what event may end or reassign that obligation?
- What price ceiling and concentration limit should force a reduction in the DA target?
- Can pool or hosting concentration be measured robustly in the presence of Sybil identities?

### Enforcement

- Which failures justify withholding rewards, and which are indistinguishable from network partitions?
- Can randomized service checks avoid leaking stable custody assignments?
- Should rewards settle continuously, after the service window, or through a repair reserve?

Until these questions have measured answers, the equations in this chapter are a procurement research program rather than a protocol parameter proposal.

[Project overview](../README.md) · [Document map](document-map.md) · [Previous in core argument](02-is-variable-retention-safe-for-rollups.md) · [Next in core argument](07-what-is-the-prior-art-and-novelty.md)
