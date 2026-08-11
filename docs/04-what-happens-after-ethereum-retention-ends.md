# What happens after Ethereum retention ends?

## 14. Retention-extension markets above Ethereum DA

Variable retention does not imply that Ethereum itself must provide every useful retention horizon. Exposing time as an explicit resource creates a clean boundary around which downstream providers can compete.

The base protocol provides the common required-serving window:

> A committed object was reconstructably available under Ethereum’s DA security assumptions, and the relevant protocol participants remain obligated to retain and serve sufficient custody data for reconstruction until expiration.

Any third party can retrieve the object during that window and offer an additional availability promise over the same commitment. Ethereum therefore acts as a **wholesale availability and integrity layer**; downstream systems can sell **retail persistence** with different trust, latency, durability, and jurisdictional properties.

Possible products include:

- an additional six hours of availability;
- seven days of low-latency retrieval;
- long-term archival storage;
- geographically or jurisdictionally diversified replication;
- retention until a designated event or acknowledgement;
- permanent or effectively permanent mirroring.

The original publisher need not upload the same bytes independently to every provider. Multiple providers can ingest them from the common Ethereum publication event and verify them against the same commitment or versioned hash.

### 14.1 Decentralized retention extensions

A decentralized retention layer can monitor Ethereum DA, retrieve objects before expiry, retain them longer, and receive payment for demonstrating possession or service.

EthStorage provides concrete adjacent evidence for this architecture: its documented storage providers download data associated with Ethereum DA and submit storage proofs to an L1 contract for rewards. Filecoin supplies a more general storage-market precedent in which deals have explicit durations and providers continuously prove storage over the deal lifetime. Neither system implements the base-protocol variable-retention mechanism proposed here, but both show that **timed persistence can be separated from initial publication**.

An Ethereum-settled adapter could similarly purchase external storage for an Ethereum-committed object without requiring that the storage network itself become an Ethereum rollup.

### 14.2 Centralized retention and pinning

A centralized provider can offer the same interface with a different trust model:

> I will retain any qualifying Ethereum-published object for `x` per byte-hour for up to `R`.

Ethereum supplies the integrity anchor and initial retrieval opportunity. The provider is trusted only for extending availability. Multiple providers can ingest the same object independently.

### 14.3 Worked construction, not base protocol: receipt-terminated retention

A more application-specific consequence is that downstream retention need not terminate at a fixed clock time. A provider could retain ciphertext until a recipient or other condition proves that persistence is no longer needed, subject to a prepaid maximum duration or spend.

This **RetentionNote** construction is useful because it demonstrates the expressiveness of a timed-availability market: the downstream guarantee can be state-contingent rather than merely “seven more days.” It is **not a required component of variable-retention Ethereum DA**, and the messaging-specific acknowledgement and mailbox mechanics are moved to Appendix A so that the base paper does not silently become an application-design proposal.

### 14.4 Composable chains of guarantees

An object can move through a chain such as:

```text
Ethereum: short protocol serving window
      |
      v
specialized cache: hours / until acknowledgement
      |
      v
decentralized retention market: weeks
      |
      v
Filecoin / archive / swarm: long-term persistence
```

Each stage can inherit the same content commitment while adding a new availability promise. The stages need not share a trust model.

This is particularly useful for censorship-resistant dissemination **after inclusion**. Ethereum need not bear the cost of permanent storage merely to provide a credible replication window from which independent persistence systems can acquire the object.

These services are architectural consequences and evidence of composability, not prerequisites for the base mechanism.

---

## 15. Throughput-retention frontier

The relationship between throughput and retention is simple in first approximation.

If the DA system can safely support:

```text
S
```

bytes of logically retained data, then the throughput at which every byte can receive retention `T` scales approximately as:

```text
R_max
≈
(S) / (T).
```

Equivalently:

```text
T_sustainable
∝
(S) / (R).
```

This is not intended as a complete FullDAS capacity model.

Coding overhead, replication, repair, validator heterogeneity, custody topology, sampling, networking overhead, and provider churn complicate the mapping from logical retained data to physical node resources.

For purposes of the toy model, we collapse these factors into an effective logical capacity parameter `S`. A deployable implementation would need to derive `S` from the actual DAS architecture.

The purpose of the model is to expose the basic tradeoff.

At low throughput, nearly all data may afford multi-week retention.

As throughput rises by one or two orders of magnitude, long retention becomes scarce while shorter retention can remain abundant.

At sufficiently high throughput, this is not necessarily a failure state.

It may be the expected market allocation.

---

## 16. Illustrative active-stock model

The argumentative core uses only the relationship `R≈S/T`. It does not assume a numerical value for `S`, which must ultimately be derived from a concrete custody topology and the resource-vector treatment in §6.

The former 64 TiB example is retained in [Illustrative numerics](../appendices/illustrative-numerics.md) as a reproducible geometry check, not as evidence for an Ethereum parameter.

---
