# Application use-case review

Reviewed September 6, 2026. This follow-up examines two public application repositories as evidence for the Blobject. It is source reconnaissance, not a security audit or an independently rerun deployment test.

## Inclusion decision

The selected scope is **Blobcast and BlobMail as the two experimental case studies**. Start with Blobcast's acquisition and archive-handoff experiment, then test BlobMail's offline delivery and expiry recovery. Neither supports a numerical application retention minimum, a demand estimate, or a claim of physical savings. Both share an author with this proposal, so they do not establish independent adoption.

Public snapshots inspected:

- [Blobcast / Radio Free Ethereum](https://github.com/bonklek/poc-blobcast/tree/8d4924edaf7ecad2ddaccb2bd52df08ff24284e3).
- [BlobMail](https://github.com/bonklek/poc-blobmail/tree/939b1d8a5dc2f9ca230a2a7e9d301923033d877b).

Local checkouts discovered during reconnaissance were older than these public snapshots. Their older descriptions should not determine the public applications' present maturity. Other private and local projects are outside this public evidence record.

## Blobcast: acquisition and archive handoff

The [README](https://github.com/bonklek/poc-blobcast/blob/8d4924edaf7ecad2ddaccb2bd52df08ff24284e3/README.md) documents a Station contract, media publisher, browser tuner, verified local caching, and archive retrieval. It also describes provider and cross-layer verification limitations. The [availability module](https://github.com/bonklek/poc-blobcast/blob/8d4924edaf7ecad2ddaccb2bd52df08ff24284e3/packages/protocol/availability.mjs) compares inclusion plus a configured serving window against season end plus a safety margin. Its Ethereum helper fixes a 4,096-epoch profile. That application arithmetic must not be mistaken for a specification of exact consensus request boundaries or configurable native leases.

The useful lifecycle is publication → verified acquisition → playback/retries → optional archive or scheduled replay. A short media segment does not imply a short required serving window: late joins, prepublication, repeat programming, and archive failures can extend the requirement.

First experiment:

1. Record one bounded stream's segment sizes, publication times, viewer acquisition times, late joins, retries, and replay requests.
2. Replay that same trace through an application test harness with simulated fixed, menu-based, and arbitrary serving deadlines. Keep publication volume and required playback behavior constant.
3. Independently disable native retrieval, browser cache, and archive sources. Record the verified source of every successful acquisition; a surviving cache must not conceal failed native service.
4. Measure playback failures, join delay, handoff completion, bytes stored over time, and network traffic. Label fallback programming separately from successful delivery of the requested segment.

This is the best first candidate for measuring how an application's acquisition deadline differs from its later use of already acquired data. Application tests alone cannot establish PeerDAS resource reclamation or Ethereum's minimum safe serving window.

## BlobMail: offline delivery and expiry recovery

The [README](https://github.com/bonklek/poc-blobmail/blob/939b1d8a5dc2f9ca230a2a7e9d301923033d877b/README.md) describes a standalone Sepolia messaging MVP with browser identities, encrypted text, batch publication, event discovery, and KZG verification. The [August 12 acceptance record](https://github.com/bonklek/poc-blobmail/blob/939b1d8a5dc2f9ca230a2a7e9d301923033d877b/reports/sepolia-mvp-live-acceptance.json) reports one included blob transaction, a reconstructed 664-byte batch containing one entry, a matching recipient, and rejection by an unrelated recipient. This is checked-in evidence inspected here; the live transaction and receiver were not independently replayed in this review. One lightly filled testnet blob is not evidence of efficient batching or market demand.

The useful lifecycle is publication → recipient offline interval → event discovery → authenticated batch acquisition → local decryption and durable inbox storage. It has no delivery or read receipt. Sender-observed inclusion cannot establish that the recipient has a recoverable copy.

The [receiver](https://github.com/bonklek/poc-blobmail/blob/939b1d8a5dc2f9ca230a2a7e9d301923033d877b/src/mailbox/receiver.js) returns a new cursor only after processing the refresh successfully. A segment replay failure aborts the refresh. The [receiver tests](https://github.com/bonklek/poc-blobmail/blob/939b1d8a5dc2f9ca230a2a7e9d301923033d877b/test/mailbox-receiver.test.mjs) cover non-advancement on verification failure; they do not establish recovery after genuine expiry.

First experiment: vary recipient absence, provider failure, batch age, and backup availability; place an unavailable old declaration before fresh mail. Determine whether recovery preserves both explicit loss reporting and progress. Do not silently skip unverifiable data and count the run as successful delivery. Measure time to acquisition, catch-up requests, delivery failures, and how much a relay or archive must retain. If short native service requires an always-online relay, include its cost and trust assumptions in the comparison.

## What would count as progress?

These cases can address the request for real workflows and falsifiable application tests now. They still need measured traces, explicit recovery guarantees, and independent users or operators before supporting demand claims. Compare ordinary authenticated distribution or application storage as well as fixed-retention Ethereum service. Keep economic willingness to pay separate from testnet transaction costs.

Use the resulting traces as inputs to the [physical-resource and workload evaluation](../docs/08-what-remains-to-be-proven.md#workload-evidence-plan). Report application delivery results separately from protocol safety and physical storage savings. Prefer a small duration menu if it captures the useful effect; these applications do not by themselves justify arbitrary epoch choices.
