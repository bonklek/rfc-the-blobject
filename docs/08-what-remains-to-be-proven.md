# What remains to be proven?

## 22. Open questions

The next round of work should test whether selectable native retention is worth implementing. The tests below have three scopes: a **proposal kill** rejects purchaser-selected serving duration, a **branch kill** rejects one representation or duration granularity while leaving alternatives available, and a **deployment gate** must be satisfied before an implementation can safely ship.

1. Can logical expiry release physical resources under current 1D PeerDAS?
2. If Ethereum adopts cross-row 2D coding, can hot redundancy be dropped without weakening fresh DA?
3. Can cold custody survive realistic correlated failure and repair conditions?
4. What serving durations do rollups, provers, and other applications actually require for trustless recovery or completion?
5. Do a few maturity classes capture most of the benefit of continuous durations?

The detailed questions below unpack those blockers and the secondary design choices around them.

### Workload evidence plan

No row below has a validated safe short native duration or a measured cost advantage in this repository. The examples define evidence to collect, not parameters to deploy.

The first application experiments are scoped to [Blobcast and BlobMail](../audits/application-use-case-review.md): stream acquisition and archive handoff for the first, offline delivery and expiry recovery for the second. Their inspected implementations support experiment design; workload measurements remain outstanding. The broader workload table below records future research questions, not additional case studies selected for this round.

| Workload and affected actor | Recovery timeline to measure | Comparison and likely constraints |
|---|---|---|
| Optimistic rollup: sequencer pays; challengers and users rely on data | Blob inclusion, assertion time, late challenger acquisition, replay/proving, dispute deadlines; identify who retains copies and when | Full current service versus shorter native service with an explicit archive/watcher assumption; serving and recovery may bind |
| Validity rollup: provers, users, and new nodes | Input acquisition, state reconstruction, proof completion, escape and new-node sync | Short proving latency alone is insufficient; compare durable state distribution and archive alternatives |
| Proof over temporary input: prover and result consumer | Acquire a recoverable witness before expiry; retain it through proof, retries, and required settlement | Local witness retention or external storage can separate native acquisition time from completion; ingress, computation, and recovery may bind |
| Media or interactive stream: publisher and listeners | Initial delivery, late joins, retransmission, rebuffering, and replication deadlines | Compare existing P2P/CDN delivery; network and writes may dominate retention |
| Encrypted asynchronous message: sender, recipient, and provider | Offline-recipient delay, mailbox discovery, retrieval, cancellation authority, and lost-key recovery | Compare application storage; recipient timing and privacy may dominate nominal short message lifetime |
| Persistent-object bootstrap: publisher and mirrors | Verified acquisition by independent mirrors before native expiry; recovery if handoff fails | Compare direct archive publication; handoff traffic and persistence qualification may erase savings |

For each candidate, measure byte volume, duration distribution, willingness to pay, failure/retry behavior, and the resource that actually binds. Compare unchanged service, a small duration menu, and arbitrary epoch choices using the same trace and safety requirements. Record net reclaimed storage, request/repair bandwidth, metadata, writes, and time to reusable capacity. Set the minimum useful improvement and tolerated failure criteria before evaluating a result; do not select them after seeing the winner.

### 22.0 Proposal-level kill criteria

Selectable retention should be abandoned or narrowed if either of these conditions holds:

1. **1D physical-value kill.** Under representative expiry, request, churn, and repair workloads, sparse historical serving on current or near-current PeerDAS does not release enough physical resources to justify its metadata, request, repair, and reclamation costs.
2. **Demand kill.** Realistic applications cannot safely use materially shorter horizons than the current fixed window, so variable duration creates no meaningful allocation advantage beyond its logical accounting result.

**Granularity branch kill:** if two or three fixed maturity classes capture nearly all measured value at substantially lower implementation and security complexity, prefer that menu to arbitrary epoch choices. This outcome supports a simpler form of variable retention; it does not refute purchaser-selected duration.

The FullDAS parity-lifetime and cold-row survivability questions in §22.3 are branch kills: failure rejects the hot-2D/cold-1D design, not the entire proposal. Upgrade, repair, handoff, observability, and recovery requirements are deployment gates unless the proposal relies on one of them for a claimed security property.

### 22.1 Physical capacity and pricing

- Which component of `K_safe_vector=(K_storage,K_serve,K_repair,K_IO)` binds under each workload?
- What node-resource percentile should define the protocol envelope?
- How large must `H_min` be to preserve a meaningful short-duration lane under bursts, and how can ingress policy prevent that lane itself from being flooded?
- Does a simple active-stock base fee plus byte-time charge allocate capacity adequately, or does it systematically underprice long leases purchased during quiet periods?
- Should long required-serving leases pay a duration risk premium even without future-starting reservations?
- Can an attacker cheaply cycle short leases to manipulate the retention base fee?
- What are the measured per-node write fraction, physical expansion, and local write amplification for each candidate custody architecture?
- At what throughput does SSD endurance or hot-tier bandwidth bind before resident storage?
- If hardware providers are paid separately, can posted `q_write` and `q_retention` rates recruit qualified supply without oscillation, Sybil pooling, or strategic withholding?
- What service-price ceiling and concentration threshold should force the safe DA target downward?

### 22.1.1 Fractional operator pools

- What is the smallest independently verifiable cell assignment that a fractional contributor can serve?
- Can one logical duty be divided among small contributors without making the pool coordinator a trusted custody or repair bottleneck?
- How much spare capacity and handoff overlap is required for delayed exits?
- Can ownership, hosting, network, client, and geographic concentration be measured well enough to inform a safety bound?
- How should rewards fund repair and device replacement without double-paying existing validator duties?

### 22.2 Simpler-design challenge

- Do two or three maturity classes capture most of the allocative benefit?
- Can unused capacity safely float across maturity lanes without recreating heterogeneous physical expiry?
- Do renewable short leases provide enough continuity for non-rollup applications?
- At what point does continuous `T` outperform quantized classes after implementation overhead is included?

### 22.3 Heterogeneous expiry under PeerDAS/FullDAS

The highest-priority implementation questions split by representation. For 1D PeerDAS:

- Can EIP-8136-style cell transport be adapted to sparse historical requests without reconstructing complete sidecars?
- What row-topic or discovery mechanism lets independent nodes contribute to partial reconstruction?
- How are per-cell expiry, custody assignment, and repair indexes represented?
- Can the request path meet a versioned service profile's deadlines, rate limits, retry rules, and reconstruction-fanout assumptions under adversarial load?
- How large can reclamation lag and scheduled expiry bursts become before physical capacity credit must stop?

For a future 2D design, the hot/cold kill questions are:

- Does a concrete FullDAS design require its second-dimensional coded representation to persist through the entire historical serving window, or only through fresh dispersal/sampling/availability amplification?
- Can the independently committed horizontal blob row remain a sufficient authenticated reconstruction object after cross-row redundancy is dropped?
- Before shared parity is discarded, can every still-live object demonstrate independently authenticated custody above its reconstruction threshold plus a justified churn and repair margin?
- Is row-local cold repair cheap and robust enough under realistic churn to maintain long leases without preserving the rich 2D code?

Secondary questions include:

- Which `T_hot` candidate—local acceptance plus delay, a network availability signal, or finality—satisfies the fresh-DA security model?
- Can the hot representation be dropped before ordinary finality?
- What minimum common hot interval is needed?
- Can an illustrative 8-epoch lease satisfy publication-time DAS, L1 restart, sync, backfill, reassignment, and ordinary fork-recovery requirements, or must `T_protocol-min` be longer?
- If unresolved fork or finality duties extend beyond a purchased duration, how are those bytes bounded, admitted, and paid for without turning a prepaid lease into an unknown-duration obligation?
- Can current PeerDAS cells be served sparsely after neighboring blob cells expire without reconstructing a dense `DataColumnSidecar`?
- What cold request/proof interface identifies a surviving cell against the original blob commitment?
- How are cold cells assigned, replicated, challenged, repaired, and handed off?
- How should repair policy depend on remaining lease time?
- What is the measured ratio `γ_hot/γ_cold` under a concrete code?
- When does maturity-aware physical framing remain useful even if the hot/cold transition works?
- If the hot/cold design fails, how many maturity-aligned coding domains capture most of the benefit without excessive fragmentation?


### 22.4 L2 security minima

- For each major optimistic rollup, what data must remain independently retrievable throughout the fault-challenge window for a previously offline challenger to participate trustlessly?
- What additional assumption appears if Ethereum serving expires before that window?
- For validity rollups, what historical data remains necessary for state reconstruction, escape, and permissionless node bootstrap after proof generation?
- How much of present blob retention is actually security-critical versus operational convenience?
- Under realistic minima, how much budget elasticity remains during a DA attack?
- For temporary computation and proving workloads, what duration covers retrieval, computation or proving, result settlement, retries, and correlated-failure margin?

### 22.5 Future-starting commitments

- How should `H_uncertainty(τ)` scale with lookahead?
- What maximum reservation horizon is compatible with credible hardware-capacity forecasts?
- Can non-refundable future rights still be weaponized as economic denial?
- When and how should unexercised capacity return to a spot/JIT lane?
- How should transferable rights interact with owner-based mempool allowance and late-bound operational keys?

### 22.6 Availability semantics and post-expiry proof

- Is level-1 protocol-required serving sufficient for the base experiment, or must continued service be probabilistically monitored?
- What evidence would justify level-3 cryptoeconomic penalties without creating mass-slashing or false-positive risk?
- Can a Sybil-resistant, economically accountable custody mechanism demonstrate continued possession and service across heterogeneous lease durations, repair, reassignment, and handoff?
- Can a client deterministically compute its live duties from canonical `DataObjectMeta` without arbitrary EL-state access?
- Can a live lease retain its admitted `service_profile_id` semantics across client and protocol upgrades?
- What are the recovery semantics for canonical lease identity, slot-based expiry, and active resource counters under reorgs or extraordinary rollback?
- Can custody reassignment preserve a live obligation until the replacement has accepted and demonstrated custody?
- What minimal integrity anchor should remain after payload expiry?
- Can a later observer prove historical availability, or only authenticate a copy that survived elsewhere?

### 22.7 Persistence handoff and downstream markets

- What minimum base window is sufficient for plural independent storage systems to ingest an object?
- What standardized commitment/handoff interface would allow EthStorage-like, Filecoin-like, centralized, and P2P providers to compete over the same object?
- Which downstream guarantees require proof of possession versus proof of retrievability or service?

### 22.8 Backbone-scale limits and ephemeral proofs

- For a proposed global rate, do `N · b`, coding expansion, replication, sender uplink, repair, and burst headroom fit one topology-aware network model?
- At what rate does shrinking the custody fraction stop preserving the intended independent operator population?
- What frame, manifest, commitment, and proof aggregation should replace the current 128 KiB object control surface at very high throughput?
- What durable evidence can a late node verify after historical DAS sampling can no longer be repeated?
- Can an application bind a proof of `f(D)=y` to the exact Ethereum commitment and finish proving before `D` expires?
- How should clients distinguish inclusion, publication-time availability, interval service, a surviving copy, and a proved computation?

### 22.9 Private AOT activation

- Can shielded capacity ownership activate a public ephemeral key without linking payer and publication through timing or denomination?
- Can peers reject unknown publication keys before doing expensive zero-knowledge or blob-proof verification?
- What canonical state and reorg rules track active keys, nullifiers, and remaining byte allowances?
- How many activations must be pooled or batched to provide a meaningful anonymity set?
- Does a generic shielded future-capacity market make a separate private-ticket mechanism unnecessary?

### 22.10 Optional active-lease surrender

- Can time-dependent safe reclaim credit `κ_X(L,τ)` be derived conservatively from consensus-visible representation state rather than client-specific compaction, garbage collection, or repair debt?
- What overlap reserve lets a replacement clear ingress and hot DAS while the surrendered cold obligation remains physically live?
- Which leases expose surrender authority, and how are application beneficiaries protected from payer- or sequencer-directed early termination?
- Does reclaim-and-return capture most of the value without creating transferable residual future-capacity rights?
- When do coding-cohort complementarities make reclaim credit non-additive or too illiquid to justify protocol integration?

A base implementation EIP needs evidence for the selected representation, exact serving boundaries, protocol and application floors, physical admission, and recovery behavior. Futures, private activation, specialized procurement, and early surrender need their own evidence only if those extensions are proposed. They are not prerequisites for the immediate-start experiment.

---

[Project overview](../README.md) · [Document map](document-map.md) · [Previous in core argument](07-what-is-the-prior-art-and-novelty.md) · [Next in core argument](09-what-is-the-conclusion.md)
