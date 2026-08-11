# What remains to be proven?

## 22. Open questions and adversarial research agenda

The next work should be falsification-oriented rather than additive.

### 22.1 Physical capacity and pricing

- How should `K_safe` be derived from custody groups, erasure coding, local storage budgets, serving bandwidth, and repair overhead?
- What node-resource percentile should define the protocol envelope?
- How large must `H_min` be to preserve a meaningful minimum ingress lane under bursts rather than steady state?
- Does a simple active-stock base fee plus byte-time charge allocate capacity adequately, or does it systematically underprice long leases purchased during quiet periods?
- Should guaranteed long leases pay a duration risk premium even without future-starting reservations?
- Can an attacker cheaply cycle short leases to manipulate the retention base fee?

### 22.2 Simpler-design challenge

- Do two or three maturity classes capture most of the allocative benefit?
- Can unused capacity safely float across maturity lanes without recreating heterogeneous physical expiry?
- Do renewable short leases provide enough continuity for non-rollup applications?
- At what point does continuous `T` outperform quantized classes after implementation overhead is included?

### 22.3 Heterogeneous expiry under PeerDAS/FullDAS

The highest-priority implementation questions are now the hot/cold kill questions:

- Does a concrete FullDAS design require its second-dimensional coded representation to persist through the entire historical serving window, or only through fresh dispersal/sampling/availability amplification?
- Can the independently committed horizontal blob row remain a sufficient authenticated reconstruction object after cross-row redundancy is dropped?
- Is row-local cold repair cheap and robust enough under realistic churn to maintain long leases without preserving the rich 2D code?

Secondary questions include:

- What exact event ends the mandatory hot phase `T_hot`?
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

- Is the base service a point-in-time availability event plus a timed serving obligation, or should continued service itself be attestable?
- What enforcement makes heterogeneous serving duties credible?
- What minimal integrity anchor should remain after payload expiry?
- Can a later observer prove historical availability, or only authenticate a copy that survived elsewhere?

### 22.7 Persistence handoff and downstream markets

- What minimum base window is sufficient for plural independent storage systems to ingest an object?
- What standardized commitment/handoff interface would allow EthStorage-like, Filecoin-like, centralized, and P2P providers to compete over the same object?
- Which downstream guarantees require proof of possession versus proof of retrievability or service?

The paper should not advance to an implementation EIP until these questions are simulated or prototyped against a concrete DAS representation.

---
