# Appendix: How could RetentionNotes work?

This appendix preserves the detailed application-level construction because it demonstrates what composable retention can enable. It is deliberately separated from the base mechanism.

## A.1 Receipt-terminated retention note

A downstream storage obligation can terminate when the intended recipient proves that the object has been retrieved.

A publisher creates a `RetentionNote` containing at least:

```text
data commitment H
retention policy
maximum expiry
prepaid retention balance
acknowledgement condition
```

While the note remains unspent, a provider retains the corresponding ciphertext and earns fees according to elapsed byte-time. When the acknowledgement condition is satisfied, the note is spent, accrued fees are released, unused prepaid balance can be refunded, and the provider may prune the data.

If no acknowledgement arrives, the lease continues until either:

- the prepaid balance is exhausted; or
- a hard maximum expiration is reached.

Downstream retention is then metered rather than purchased for one fixed duration. This may suit private messaging, asynchronous agent communication, or any application whose sender values reliable retrieval but not persistence after receipt.

The economic roles remain distinct:

- **sender escrow** pays for actual byte-time retained;
- **provider collateral or proof obligations** back the provider’s promise to retain and serve the object.

The first can decay continuously with time. The second can be slashed, withheld, or fail to earn payment if continued possession or service cannot be demonstrated.

## A.2 Private acknowledgement without a public receipt graph

A recipient acknowledgement need not reveal the recipient’s Ethereum identity.

The sender can choose a random secret `r`, place `r` inside the recipient-encrypted payload, and publish only:

```text
c_ack = H(r)
```

in the retention note.

After retrieving and decrypting the message, the recipient learns `r` and can reveal it directly or through a relay. The retention contract checks:

```text
H(r) = c_ack
```

and marks the note spent.

The public system learns only that someone possessing the acknowledgement secret terminated the retention obligation. It need not learn the recipient’s long-term wallet, messaging identity, or account.

The construction cannot force an honest acknowledgement. A recipient may retrieve the data and refuse to reveal `r`, so the sender still needs a maximum duration or spend. Incentives for timely acknowledgement would require a separate mechanism.

## A.3 Spam and mailbox admission

Sender-funded retention makes bulk storage spam costly but does not solve recipient attention costs or scanning overhead.

A messaging system above the retention market can use separate mailbox-admission policies, including:

- capabilities issued to known contacts;
- anonymous group membership or RLN/Semaphore-style rate limits;
- higher-cost postage for unsolicited senders;
- per-sender or per-group quotas;
- reply capabilities created by an existing conversation;
- public inboxes accepting messages above a specified economic threshold.

The storage provider need not understand the recipient’s social identity. It only needs to enforce the retention contract for an authorized committed object.

This keeps economic anti-spam, recipient privacy, and storage economics separable.
