# Appendix: How could private AOT authorization remain cheap to validate?

This privacy-research branch sits outside the base proposal. It asks whether a user can pay privately for future DA propagation while still giving gossip peers a cheap, canonical authorization check.

The core constraint is asymmetric:

- authorization should not reveal a durable payer-to-publication link;
- peers must reject unauthorized high-bandwidth traffic before expensive proof, coding, or storage work.

[Waku RLN](https://docs.waku.org/learn/concepts/protocols/) is relevant precedent for anonymous, economically constrained P2P publication. Blob-scale DA adds a stricter resource boundary: an invalid authorization can precede hundreds of kilobytes or more of offered data and expensive cell-proof processing.

This note is a construction sketch, not a recommendation to modify EIP-8256.

---

## D.1 Why AOT tickets are an anti-DoS capability

Ordinary public mempool propagation often has a free-option shape:

```text
advertise candidate traffic
        |
        v
network validates, stores, and relays it
        |
        v
transaction may never land
```

The network spends resources before final inclusion is certain. Fee checks and replacement rules constrain abuse, but the candidate can still consume bandwidth and memory while pending.

The AOT model reverses the order:

```text
PAY FIRST
    -> receive one bounded future propagation capability
    -> bytes may enter the special gossip path
```

Draft [EIP-8256](https://eips.ethereum.org/EIPS/eip-8256) makes ticket ownership a prerequisite for propagation, creating a globally agreed bounded set of eligible senders. Honest use and capacity griefing both pay in advance. This is more than a reservation receipt: it is a **prepaid capability to consume a bounded unit of Ethereum DA-network bandwidth**.

Privacy must preserve that property.

### Exact baseline mechanics in the present draft

Three details matter when comparing the construction below with EIP-8256 itself:

1. A ticket for target slot `T` is bought specifically in slot `T - TICKET_LOOKAHEAD`. Equivalently, a purchase in slot `s` derives `target_slot = s + TICKET_LOOKAHEAD`; the purchaser does not freely choose an arbitrary target from a forward curve.
2. Gossip does **not** consume the ticket through an on-chain `spent` bit. The ticket payment and reserved capacity are recorded at purchase, while the later AOT sidecar is a networking object.
3. Replay or equivocation is bounded on the networking path: AOT gossip accepts only the first valid sidecar for each `(ticket_id, column_index)`, after checking the target window, registered BLS key, proof, and subnet.

The nullifier and canonical activation state proposed later are therefore changes required by shielded ownership, not descriptions of how the present public-ticket draft accounts for gossip use. They should preserve its cheap first-valid-message rule rather than replacing every sidecar with an on-chain consumption transition.

---

## D.2 Naive private proof at gossip time

A first construction is:

1. the user acquires a private capacity credit;
2. for each AOT publication, the user sends peers a zero-knowledge proof of an unspent valid credit;
3. the proof reveals a slot-specific nullifier but no payer identity;
4. peers verify the proof and reject duplicate nullifiers.

Conceptually:

```text
private credit
    + target slot
    + fresh publication key
    -> ZK authorization + nullifier
    -> gossip peers
```

The construction can hide the payer-to-key link, but it moves expensive work to the network edge. An attacker can stream syntactically plausible but cryptographically invalid proofs from unknown identities. Every peer must verify the proof before learning that the sender has no capacity.

Additional problems appear:

- peers may disagree about observed nullifiers;
- gossip-local spent state has awkward reorg semantics;
- proof verification sits in front of cheap reputation and allowlist checks;
- verification cost multiplies across peers;
- invalid proof traffic can be much cheaper for the sender than for the network.

RLN systems are specifically engineered around proof cost and rate-limiting semantics. A generalized DA path should not assume that attaching an arbitrary SNARK to every large candidate object is automatically DoS-safe.

---

## D.3 Canonical private activation, public ephemeral key

A cleaner construction moves the expensive privacy proof into canonical state before gossip begins.

```text
private capacity credit
        |
        v
on-chain ZK activation
        |
        +-- spends slot/capacity nullifier
        +-- registers ephemeral BLS/publication key
        +-- fixes target slot and byte allowance
        |
        v
canonical active-key allowlist
        |
        v
ordinary signed AOT gossip
```

The activation transaction proves approximately:

```text
I own one unspent eligible private credit
and authorize ephemeral key K
for capacity B in target slot s.
```

It reveals:

- the operational key `K`;
- the target slot or window `s`;
- the capacity class `B`;
- a nullifier preventing reuse.

It need not reveal the original payer or the path by which the private credit changed hands.

### Peer fast path

Consensus clients derive a canonical map such as:

```text
active_aot[activation_id] = (domain, K, slot, max_bytes, object_index_range, ticket_class)
```

On receiving candidate AOT traffic, a peer performs:

1. a lookup for the activation and its authorized key `K`;
2. an immediate drop if `K` is absent, early, late, or out of allowance;
3. a normal signature check for known `K`;
4. byte/cell/proof validation only after authorization succeeds;
5. bounded peer-local quota and first-valid-message accounting for accepted objects.

Canonical state fixes the maximum authorization; it does not record every peer's accepted gossip. Peers need local caches keyed by activation, object index, and column (or another precisely specified resource unit), with signed binding to the object and target. Two peers may see different valid messages first. Equivocation, concurrent objects, cache retention, and total resource bounds remain design questions; canonical activation alone does not solve them.

Unknown identities therefore fail before a zero-knowledge proof or blob proof is verified. The private proof is attached to one canonical activation transaction; chain validators still perform the required verification. Ordinary gossip authorization need not repeat that privacy proof per sidecar.

### Reorg behavior

Because the allowlist is derived from canonical chain state, reorgs have defined behavior:

- an activation removed by a reorg removes `K` from the active map;
- a restored private credit or nullifier follows the shielded system's reorg rules;
- peers refresh canonical authorization and reconcile local quotas and replay caches under an explicit reorg policy; consumed bandwidth cannot be rolled back;
- objects propagated under the orphaned activation may remain in local caches but lose canonical eligibility.

Reorgs can still waste bandwidth, but peers no longer invent incompatible gossip-local ownership histories.

---

## D.4 Relationship to EIP-8256 settlement

The present EIP-8256 draft has two authorization surfaces:

- an execution-layer allowance derived from ticket `owner`;
- a consensus-layer BLS key bound into the ticket for AOT propagation.

A private activation design needs an explicit indirection. The shielded or pooled financial right would settle into a public operational record near delivery:

```text
private/fungible ownership
        -> activation
        -> public slot-specific operational key
```

The execution-layer allowance must recognize that operational record instead of requiring a transparent permanent owner path. The consensus layer can continue using a cheap public key for AOT signatures.

This separation also supports ordinary delegation and key rotation. Privacy is not the only reason to avoid binding a hot delivery key when a long-lived financial position is first purchased.

---

## D.5 The anonymity-set problem

Shielded ownership does not guarantee useful anonymity at activation.

If only one private user activates exactly 40 MiB for slot `s`, observers can correlate:

- credit acquisition timing;
- activation timing and capacity;
- the ephemeral key;
- row propagation timing;
- the eventual application transaction.

The proof may hide the formal ownership edge while the resource pattern identifies the user.

Mitigations include:

- common capacity and maturity classes;
- activation windows rather than exact user-selected instants;
- batched activation of many operational keys;
- delayed or randomized settlement within a bounded window;
- padding and cover publications;
- pooled purchases that aggregate many applications;
- long-lived private DA capacity from which users draw standardized units.

The last option creates a stronger anonymity set but also a pool coordinator, inventory, and solvency problem. The pool must not oversell future capacity or learn the complete payer-to-publication mapping.

There is also a liquidity feedback loop. If a privacy-only class attracts a fraction `p` of otherwise comparable DA demand, its candidate anonymity set is bounded above by roughly:

```text
A_private <= p * A_total
```

before timing, denomination, capacity, and application fingerprints reduce it further. A privacy surcharge or separate-market friction can lower `p`; the smaller resulting anonymity set makes the privacy product less useful, which can lower participation again. Fixed proof, coordination, and inventory costs may then be spread across fewer users and raise the surcharge further.

```text
privacy surcharge / fragmented liquidity
    -> lower participation
    -> smaller anonymity set
    -> lower privacy value and higher per-user overhead
    -> still lower participation
```

This bootstrap problem is a reason to prefer a large generic capacity market with pooled or shielded ownership over a thin privacy-branded ticket class. The formula is an upper-bound intuition, not an anonymity guarantee: correlated timing can make effective anonymity much smaller than the number of participants.

---

## D.6 A separate private-ticket market may be unnecessary

Once future DA capacity is already represented as transferable or pooled rights, privacy may belong in the general settlement layer rather than in a special “private AOT” product.

One architecture is:

```text
ordinary future DA capacity
    -> pooled or shielded ownership domain
    -> private transfer/aggregation
    -> late public activation of an operational key
```

This reuses the same scarce capacity and forward-safety accounting. It avoids fragmenting liquidity and capacity into public and private ticket markets.

The private system still needs to hide denomination and timing well enough to provide an anonymity set. But the protocol primitive can remain a generic late-bound delivery authorization rather than a privacy-specific DA class.

---

## D.7 Threat model and failure modes

The construction must address at least:

- **activation spam:** on-chain proof verification and state growth must be fee-bounded;
- **invalid gossip:** unknown keys must fail before expensive payload validation;
- **key theft:** possession of `K` may permit spending the activated bandwidth capability;
- **front-running:** the activation proof must bind `K`, slot, chain, and capacity so it cannot be redirected;
- **nullifier replay:** activation must be unique within each canonical history, with explicit orphan/reactivation and local replay-cache rules;
- **unused capacity:** non-refundable activation prevents a private free option but wastes reserved bandwidth;
- **traffic analysis:** timing, size, peer origin, and application inclusion can undo cryptographic unlinkability;
- **pool insolvency:** pooled private capacity must not issue more activation rights than it owns;
- **small anonymity sets:** private mode may be formally correct but practically identifying;
- **censorship:** a paid ticket or activation authorizes propagation but does not automatically guarantee transaction inclusion.

Network privacy remains separate. An activated pseudonym sent directly from the user's IP leaks first-hop origin even if payment is perfectly shielded. Mix/onion ingress or an unlinkable relay is still required for that edge.

---

## D.8 Questions for a real design

- Which shielded asset represents the capacity credit, and how is future-slot solvency proved?
- Can activation proofs be batched without making one aggregator a censorship point?
- What is the cheapest canonical commitment to active keys and remaining allowances?
- How does a peer account for concurrent partial objects without race conditions?
- Can one activation authorize several rows without creating replacement or equivocation attacks?
- What minimum batch size provides a meaningful payer anonymity set?
- How are late-bound keys reconciled with EL mempool allowance and builder interfaces?
- Can activation happen early enough for AOT propagation while remaining late enough to reduce timing linkage?
- When is generic shielded settlement sufficient, making a separate private-ticket mechanism unnecessary?

The result is not a finalized anonymous ticket. It is a validation boundary:

> **perform expensive private authorization once in canonical state, then give the P2P network a bounded public capability it can reject cheaply.**

[Project overview](../README.md) · [Document map](../docs/document-map.md)
