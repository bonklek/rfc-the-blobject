# What remains to be proven?

## 22. Open questions

The next round of work should try to disprove the proposal rather than add more features. Five questions take priority:

1. Can logical expiry release physical resources under current 1D PeerDAS?
2. If Ethereum adopts cross-row 2D coding, can hot redundancy be dropped without weakening fresh DA?
3. Can cold custody survive realistic correlated failure and repair conditions?
4. What serving horizons do major rollups actually require for trustless recovery?
5. Do a few maturity classes capture most of the benefit of continuous durations?

The detailed questions below unpack those blockers and the secondary design choices around them.

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

For a future 2D design, the hot/cold kill questions are:

- Does a concrete FullDAS design require its second-dimensional coded representation to persist through the entire historical serving window, or only through fresh dispersal/sampling/availability amplification?
- Can the independently committed horizontal blob row remain a sufficient authenticated reconstruction object after cross-row redundancy is dropped?
- Is row-local cold repair cheap and robust enough under realistic churn to maintain long leases without preserving the rich 2D code?

Secondary questions include:

- Which `T_hot` candidate—local acceptance plus delay, a network availability signal, or finality—satisfies the fresh-DA security model?
- Can the hot representation be dropped before ordinary finality?
- What minimum common hot interval is needed?
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
- What are the exact reorg semantics for the expiry ring and active resource counters?
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

An implementation EIP should wait until these questions have been simulated or prototyped against a concrete DAS representation.

---
