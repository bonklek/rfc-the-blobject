# Candidate operator-market kill questions

These entries are issue-ready local research tracking. They have **not** been opened on GitHub. Each is phrased as a way to falsify or materially narrow the expanded operator architecture.

## KQ-4: Does repeated procurement remain stable under strategic supply withholding?

**Claim at risk:** bounded posted prices can recruit qualified write and retention capacity without creating an easily manipulated feedback loop.

**Kill condition:** under plausible ownership concentration, suppliers can profitably withhold capacity, induce a shortage update, and earn enough at later prices to dominate honest participation or cause persistent oscillation. The comparison should include sealed-bid uniform-price and pay-as-bid reverse procurement under the same actors and shocks.

**Evidence needed:** calibrated supply elasticities; qualification and exit lags; multi-epoch simulations; coalition size and profitability; sensitivity to `kappa`, step bounds, ceilings, reserve margins, and safe-target reduction.

**Starting artifact:** [illustrative controller and mechanism comparison](appendices/illustrative-operator-economics.md).

## KQ-5: Do fractional pools create independent supply or only Sybil capacity?

**Claim at risk:** dividing duties into small assignments broadens the credible operator set and failure-domain diversity.

**Kill condition:** a large claimed contributor population collapses to too few common administrative, hosting, network, geographic, funding, or software failure domains to meet the reconstruction and repair target. Identity count alone is not evidence of independence.

**Evidence needed:** a privacy-compatible qualification design; concentration metrics resistant to cheap identity splitting; correlated-failure traces; pool accountability and bond structure; handoff and mass-exit experiments; minimum independently controlled operator population.

**Starting section:** [fractional operation and market-power defenses](docs/11-how-do-hardware-and-da-operator-markets-scale.md#5-adaptive-posted-procurement-prices).

## KQ-6: Is the service qualification envelope physically attainable?

**Claim at risk:** qualified operators can safely sustain the write, serving, repair, and retention duties at the target throughput and allowed per-node fraction.

**Kill condition:** measured write amplification, endurance, network service, repair traffic, or qualification overhead makes the target unattainable on the intended hardware population, or forces a per-node write fraction that recreates a specialized central operator set.

**Evidence needed:** client traces for physical/logical write ratio, sustained and burst bandwidth, read/repair load, device wear, replacement time, safe per-node assignment fraction, and qualification false-positive/false-negative rates across candidate hardware tiers.

**Starting section:** [research and deployment sequence](docs/11-how-do-hardware-and-da-operator-markets-scale.md#7-research-and-deployment-sequence).
