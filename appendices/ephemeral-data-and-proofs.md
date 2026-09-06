# Appendix: What can be proven after ephemeral data expires?

Variable retention makes a distinction that fixed-duration DA can leave implicit: some claims survive the bytes, while others cannot be recreated after the serving window closes.

The sections below separate those claims and develop one application pattern:

> **use large temporary data to produce small permanent knowledge while the data is still available.**

It does not add a historical availability certificate to the base proposal.

---

## C.1 Four different claims

For an object `D`, commitment `C(D)`, and computation `f(D)=y`, at least four claims are possible.

| Claim | Possible surviving evidence | What the evidence does not establish |
|---|---|---|
| The committed object existed in a publication | canonical inclusion of `C(D)` | that the bytes were made available, retained, or still exist |
| The object was available at publication time | block acceptance under the contemporaneous DAS protocol; possibly an explicit attestation | that a late node can repeat the original sampling, or that service continued afterward |
| The object contained particular bytes | a surviving copy plus commitment verification, or a valid opening for revealed positions | unrevealed contents, or historical availability of the whole object |
| A computation over the object returned `y` | a proof `pi` whose public statement binds `C(D)`, `f`, and `y` | continuous service, later retrievability, or correctness outside the proved circuit |

Conflating these claims creates two common errors.

First, a commitment is an integrity anchor, not storage. It authenticates bytes that someone still possesses; it does not regenerate bytes that everyone discarded.

Second, a valid proof about committed data is not automatically a proof that Ethereum's custody population served that data throughout its declared horizon.

---

## C.2 The late-node problem

A node online during publication can sample the live DAS network and use the responses in its block-acceptance decision. A node arriving after all protocol and voluntary copies disappear cannot replay that interaction.

The late node may still verify:

- that `C(D)` appeared in canonical consensus;
- that contemporaneous validators accepted the containing block under the protocol rules;
- any durable aggregate attestation or proof committed at publication;
- a later proof whose public inputs bind to `C(D)`.

It cannot issue fresh historical sample requests to vanished bytes. A hypothetical **publication-time DA certificate** would therefore have certificate semantics:

> a specified population attested, sampled, or proved a condition at the time, under the stated cryptographic and adversarial assumptions.

It would not make availability replayable. Nor would it show that the object remained served for every moment until expiry.

Three certificate families should be kept distinct:

1. **Publication certificate.** Evidence that a threshold of contemporaneous checks accepted fresh availability.
2. **Interval service evidence.** Periodic custody or retrieval challenges during `[t,t+T]`, with gaps and sampling error made explicit.
3. **Surviving-copy proof.** Evidence that a particular copy or opening exists when the proof is made.

Only the second even attempts to speak about the retention interval, and discrete checks still do not prove continuous service between them.

---

## C.3 Ephemeral data to permanent knowledge

Suppose an application needs a large object only long enough to compute and prove a durable fact.

```text
large transient D
      |
      v
while D exists, prove f(D)=y
      |
      v
D expires
      |
      v
retain C(D), y, pi
```

The permanent statement is approximately:

```text
pi proves:
    exists D such that
        Commit(D) = C
        and
        f(D) = y
```

After expiry, a verifier needs only:

- the commitment `C` anchored by Ethereum;
- the result `y`;
- the computation identifier or verification key for `f`;
- the proof `pi`.

The verifier no longer needs `D`, provided the proof system is sound and the circuit binds the same commitment scheme and encoding used by the published object.

DA then acts as a temporary proving workspace. The data plane carries the large witness long enough for independent provers to acquire it, while the chain or application retains a compact fact.

### Candidate uses

Examples include:

- proving that a large batch produced a particular state transition;
- computing an authenticated aggregate over a transient dataset;
- proving that media or a document satisfied a machine-checkable property at publication;
- deriving a compact index, accumulator, or model output from a large witness;
- proving a redacted statement without retaining the full source in the base protocol.

These examples require application-specific circuits and disclosure policies. A proof of a classifier result, for example, proves only the encoded classifier and inputs; it does not establish that the classifier is socially or scientifically valid.

---

## C.4 Proving-window requirements

The pattern works only if at least one qualified prover obtains `D` and finishes before every usable copy expires.

Let:

- `T_service` be Ethereum's required-serving window;
- `T_fetch` be worst-case acquisition time;
- `T_prove` be proof-generation time;
- `T_settle` be time to publish the proof or satisfy whatever settlement condition the application requires;
- `H` be reorg, retry, and failure headroom.

A sufficient budget for a workflow that requires completion inside Ethereum's serving window is:

```text
T_service
>
T_fetch + T_prove + T_settle + H.
```

A workflow may instead acquire and durably retain a witness before native expiry, then prove and settle afterward. In that case native service must cover acquisition and its retries, while local or external copies must remain recoverable through completion. That changes the recovery and redundancy assumptions; the inequality above is not a necessary native-retention floor for every workflow.

`T_settle` may be only proof publication for one application and confirmation or finality for another. It is an application requirement, not a reason to make every Ethereum lease finality-dependent. Parallel provers can reduce correlated failure only if their failure domains are sufficiently independent, and they increase retrieval traffic. A downstream retention provider can extend the proving window, but then the application relies on that provider's service rather than Ethereum's expired obligation.

The proof should be published before the last trusted copy disappears. Otherwise a proof-generation failure is unrecoverable even though `C(D)` remains permanently visible.

---

## C.5 Binding and encoding hazards

The public statement must bind exactly the object Ethereum committed to.

Important questions include:

- Does the circuit recompute the KZG, hash, Merkle, or future post-quantum commitment correctly?
- Is `D` the logical payload, the padded blob, a segment, or the erasure-coded representation?
- Are padding, compression dictionaries, field-element encoding, and segment boundaries unambiguous?
- Does the proof bind an application and chain domain so it cannot be replayed elsewhere?
- If a decoder is used, is its version or code hash part of the statement?
- Can a later commitment migration preserve the old verification statement?

A proof over decoded bytes and a commitment over encoded field elements need a deterministic bridge. “Same human-readable data” is not enough.

---

## C.6 Availability evidence is still separate

Even a perfect proof:

```text
pi: f(D)=y for Commit(D)=C
```

does not show that arbitrary observers could retrieve `D` during the service window. A single colluding publisher and prover could create it without broad dissemination unless block acceptance or another certificate separately establishes publication-time availability.

A durable record may need several independent pieces:

```text
C(D)              integrity anchor
A_pub              contemporaneous publication evidence
y, pi              permanent proved fact
A_interval[]       optional sampled service evidence
```

Each field answers a different question. Applications should state which one their security model needs rather than call the bundle simply “proof of availability.”

---

## C.7 Privacy and deletion limits

Expiry is not guaranteed deletion. Any sampler, prover, archive, or adversary that received `D` may keep it.

The ephemeral proving pattern supports:

- ending Ethereum's serving duty;
- reducing expected widespread persistence;
- minimizing the permanent public record;
- retaining a selective proved fact instead of the complete source.

It does not support a right-to-be-forgotten guarantee. If confidentiality matters, `D` should be encrypted before publication and the proof system should operate over the intended plaintext/ciphertext relation. Key destruction can prevent future decryption under additional assumptions, but cannot erase plaintext copies already obtained by authorized or compromised parties.

Proof outputs themselves can leak information. The choice of `y`, circuit, proving time, and public inputs needs the same application-privacy analysis as the original data.

---

## C.8 Research questions

- What is the minimal publication certificate a late node can verify without pretending to replay historical DAS?
- Can current validator attestations be composed into a useful certificate, or is a new aggregate object required?
- How should a proof bind a logical data segment across future commitment and transport changes?
- What serving horizon makes independent proof generation realistic under worst-case congestion?
- Can proof markets recruit multiple independent provers without revealing sensitive access patterns?
- Which interval-service challenge schemes provide useful evidence without targeted-custodian leakage or mass-slashing risk?
- How should clients display the difference between “commitment included,” “available when published,” “served until expiry `e`,” and “computation proved”?

The durable opportunity is real, but narrow:

> **Ethereum can preserve small, verifiable knowledge derived from large temporary information; it cannot retrospectively recreate the information or rerun the network interaction that made it available.**

[Project overview](../README.md) · [Document map](../docs/document-map.md)
