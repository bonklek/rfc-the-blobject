# What does a generalized Ethereum data plane enable?

## 18. High-throughput ephemeral DA

Ephemeral retention does not eliminate the live bandwidth constraint.

Gigabytes per second still have to propagate through, be processed by, and be made reconstructably available across a distributed system.

Nor should extremely high throughput be implemented by simply multiplying the number of present 128 KiB blob objects into hundreds of thousands or millions per slot.

A high-throughput architecture would likely require:

- larger coded DA frames;
- extensive multiplexing;
- ahead-of-time or continuous propagation;
- increasingly fine distributed custody;
- efficient repair;
- batch or aggregate proof verification;
- consensus periodically certifying availability over a continuous data plane;
- markets for ingress;
- explicit accounting for custody through time.

Applications could still submit small logical messages or objects. The underlying transport would batch them into much larger DA structures.

Variable retention is deliberately orthogonal to this transport evolution.

Its purpose is to ensure that increases in real-time throughput do not automatically create proportionate increases in long-term mandatory storage.

At one gigabyte per second, for example, a one-minute raw logical retention window corresponds to roughly 60 GB of currently live data.

An eighteen-day window corresponds to roughly 1.5 PB.

The bandwidth is identical.

The storage obligation is not.

This distinction becomes increasingly consequential as Ethereum DA moves from megabytes per second toward hundreds of megabytes or gigabytes per second.

---

## 19. Application space

A generalized Ethereum availability market could serve applications with very different temporal requirements.

Examples include:

- rollup DA;
- proof and witness distribution;
- private messaging;
- public authenticated messaging;
- live media;
- broadcast;
- social feeds;
- games;
- oracle and event data;
- agent coordination;
- censorship-resistant publication;
- decentralized-storage bootstrap;
- software distribution;
- arbitrary application data.

These should not become protocol-defined categories.

Their differences emerge from choices over:

```text
B, T, R
```

and any privacy or routing layers above Ethereum.

A live-media segment may purchase minutes.

A message may purchase enough time for recipient relays to observe it.

A storage bootstrap object may purchase enough time for a persistent P2P network to acquire it.

A rollup may purchase days.

The common primitive is not “a rollup blob.”

It is:

> **market-priced, consensus-secured availability over committed bytes.**

---

## 20. Why the scope matters

The speculative claim is not that Ethereum should directly replace BitTorrent, Tor, Filecoin, messaging protocols, CDNs, or the Internet.

The emerging division of labor is different.

Ethereum can supply:

- economic scarcity;
- settlement;
- authenticated commitments;
- admission control;
- censorship-resistant publication;
- distributed availability;
- and eventually markets for those resources through time.

Specialized systems can supply:

- routing;
- privacy;
- discovery;
- indexing;
- long-term persistence;
- retransmission;
- application semantics.

In this architecture, Ethereum functions increasingly as a **permissionless economic control plane and availability substrate**.

A user purchases a scarce network resource.

Authenticated bytes enter a globally shared data plane.

Ethereum’s DAS guarantees reconstructability for a chosen period.

Other systems take over whatever happens afterward.

The provocative possibility is that Ethereum’s rollup-oriented DA roadmap may be assembling much of the infrastructure required for a more general economically secured network substrate without that having been its original design objective.

Variable retention matters because it removes a temporal assumption inherited from the rollup use case.

Once data need not automatically purchase the same multi-day retention package, the range of economically sensible applications expands dramatically.

---
