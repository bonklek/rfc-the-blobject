# Focused Wikipethia research pass

Date: 2026-09-06. Scope: additional prior art for selectable blob retention, historical retrieval/repair, and custody enforcement. Only public concept queries were sent. No draft upload, installation, corpus download, or source-code execution occurred. Only this report was written.

## Depth decision and repository assessment

The [Wikipethia repository](https://github.com/JossDuff/wikipethia) is useful as a targeted retrieval layer: its hybrid lexical/semantic search returns dated documents, stable corpus IDs, source tiers, and original URLs; thread context and paginated full documents help recover objections missed by snippets. Its README offers a hosted read-only endpoint, avoiding the roughly 1.5 GB local setup and multi-hour initial sync. Using the hosted corpus for this audit was proportionate. There is no reason to install or build it to complete this pass.

The hosted server reported 57,778 documents from ten sources, including 20,272 ethresear.ch and 33,729 Ethereum Magicians documents, with claimed coverage from 2017 to present. It did not supply an exact last-sync timestamp or immutable corpus snapshot identifier. Treat these as the server's coverage description, not an independently audited completeness claim. Search rankings included weak lexical matches; a top result is not proof of relevance. Research and process tiers are not deployed protocol authority.

This pass ran ten searches (five results each), one similar-document expansion, and context/full-thread retrieval for promising sources. Complete paginated bodies were read for RowDAS and Variants of Mempool Tickets. Original canonical sources were opened independently for the recommendations below. The result warrants a few precise reference additions, not an unlimited literature review.

## Concrete additions and corrections

### W-01 — P2, high confidence: Add RowDAS to the 1D compatibility boundary

Locations: `docs/05-can-this-work-with-peerdas-and-fulldas.md` after the 8136/partial-reconstruction discussion; `docs/07-what-is-the-prior-art-and-novelty.md` §21.6; REFERENCES.md.

[Draft EIP-8371: RowDAS](https://eips.ethereum.org/EIPS/eip-8371), created August 5, 2026, is directly relevant omitted prior art. It distributes reconstruction over row topics using cell deltas, retaining row-only encoding. Row subscription creates no custody obligation. Its individual-blob retrieval extension explicitly remains future work and requires cell-granular requests plus a row-serving retention window.

Suggested addition: “Draft RowDAS further develops row-level reconstruction without adding a second coding dimension. It does not define historical retrieval or row custody; its proposed retrieval extension still needs cell-granular requests and an explicit serving window. It therefore supports the 1D research direction while leaving the heterogeneous-expiry interface unresolved.”

Support status: canonical draft verified, not implementation adoption. This strengthens the existing qualification; it does not remove a prototype gate. The draft's creation predates the RFC cutoff, but this review did not establish that every currently visible section existed then. Date the new check separately.

### W-02 — P2, high confidence: Broaden historical custody provenance beyond bombs

Locations: `docs/07-what-is-the-prior-art-and-novelty.md` §21.9; REFERENCES.md; optional link from enforcement discussion in chapter 00.

Vitalik Buterin's [2018 custody proposal](https://ethresear.ch/t/extending-skin-in-the-game-of-notarization-with-proofs-of-custody/1639/1) combines altered-data commitments with later challenges. Justin Drake's [reply 4](https://ethresear.ch/t/extending-skin-in-the-game-of-notarization-with-proofs-of-custody/1639/4) extends claims to the notary's entire retained “storeback,” so successive votes cover data across time and shards. This is closer precedent for obligations over retained history than the cited acquisition-bomb explanations alone.

Suggested addition: “Earlier custody research also proposed extending repeated custody claims across a notary's retained history. This anticipates accountability over a storage interval, but does not supply this RFC's permissionless delivery, repair, reassignment, or heterogeneous-expiry mechanism.”

Support status: historical research and author reply, independently checked in thread context. Preserve the existing statement that a momentary custody result does not by itself establish continuous service; avoid implying that all historical proposals concerned only initial acquisition.

### W-03 — P2, high confidence: Anchor mass-slashing references in the specific construction and reply

Locations: enforcement research questions in chapter 05 and chapter 07 §21.9.

Justin Drake's [2020 mass-slashable unavailability proposal](https://ethresear.ch/t/mass-slashable-unavailability-faults/8129/1) combines deterministic sampling with custody bits. Dankrad Feist's [reply 4](https://ethresear.ch/t/mass-slashable-unavailability-faults/8129/4) explains that the 0.001-bit modification deters lazy sampling but does not ensure a large slashable validator fraction upon a DA fault.

Correction: when mentioning mass-slashable faults as an optional extension, cite the construction and preserve the difference between its aggregate-slashing claim and the modified deterrence mechanism. Neither is a proof of continued historical service. No recommendation to implement either follows.

Support status: original and replies verified. The RFC already treats this as optional research, so a concise reference addition is enough.

### W-04 — P3, high confidence: Distinguish mempool leases from retention leases

Location: chapter 07 §21.5, optional one-sentence prior-art comparison.

Julian's [Variants of Mempool Tickets](https://ethresear.ch/t/variants-of-mempool-tickets/23338/1), October 23, 2025, proposes persistent sender permissions allocated by stake or LIFO rules, alongside expiring tickets. Replies discuss liquidity, exclusion, and mixing access mechanisms. These “leases” govern the right to propagate, not purchaser-selected historical serving of an included object.

Suggested sentence: “Mempool-lease research concerns reusable propagation permissions; the retention lease here governs the lifetime of an already admitted object's serving obligation.”

Support status: full source and reply context checked. This is a useful terminological boundary, not closer complete prior art that defeats the narrow composition claim.

## Query and disposition ledger

Each query searched all indexed sources, limit five. IDs identify corpus hits; source titles link where promoted into a recommendation above. Unpromoted hits were discovery leads, not verified evidence for new RFC claims.

| # | Query | Main hits and disposition |
|---|---|---|
| 1 | `user selected blob retention duration byte time pricing` | Dynamic Blob Sizing (`ethresearch/post/53106`), Blob Aggregation (`52608`), fee-market posts. Different size/ingress dimensions; no direct selectable-retention match. |
| 2 | `variable retention blob expiry lease` | Mempool Tickets (`56728`) promoted to W-04. EIP-8252 concerns execution reorg state, not DA serving. |
| 3 | `data availability configurable retention period storage rent` | EthStorage (`36368`), StorageBeat (`53980`), state rent (`11830`), EIP-8125. Existing downstream/state distinctions; StorageBeat remains a possible later evaluation-framework source, not verified here. |
| 4 | `PeerDAS historical cell sparse storage expiry` | EIP-8371 promoted to W-01. EIP-8070 and 2D-headliner discussion (`ethmagicians/post/66932`) are adjacent; no need to infer adopted 2D architecture. |
| 5 | `data column historical retrieval repair pruning` | EIP-8371 promoted. LossyDAS (`46511`), PANDAS (`49954`), and rsmt2d (`5392`) concern coding/recovery; not investigated as expiry implementations. |
| 6 | `blob retention shorter than 18 days historical availability` | Blob Analysis (`57877`, `59477`), CL Call 99, mempool measurements. No direct purchaser-selected horizon proposal. No performance numbers imported. |
| 7 | `proof custody continuous storage retrieval service withholding` | Storeback reply (`5506`) promoted to W-02; mass-slashing (`22962`) promoted to W-03. Custody roots (`19805`) and locality (`14941`) left as further leads. |
| 8 | `proof of custody sampling historical data incentives` | Mass-slashing original/reply (`22962`, `22982`), 0.001-bit (`20990`), FullDAS (`47912`), path-to-Danksharding (`44459`). Confirmed need to distinguish enforcement claims. |
| 9 | `retention byte time pricing blob expiry user chosen` | EIP-7999, EIP-4844, Blocks Are Dead (`59441`), pricing replies. No direct heterogeneous serving-duration mechanism found. |
| 10 | `mempool leases storage duration tickets` | Mempool Tickets original/reply (`56728`, `56760`), Blob Streaming (`58659`), EIP-8256, Execution Tickets (`44229`). W-04; different resource right. |

Similar-document expansion from `ethresearch/post/56728` returned EIP-4844, thread replies, EL meeting 185 and LUCID encrypted-mempool material. It supplied no additional direct retention mechanism. This negative retrieval result is not a novelty proof.

## Coverage and stopping point

No source found in this bounded pass specifies the complete purchaser-selected, byte-time-accounted Ethereum DA serving composition. That permits retaining the dated “not aware” language; it does not establish invention or exhaustive novelty. Unindexed papers, other DA ecosystems, private discussions, missed synonyms, stale snapshots, and ranking truncation remain gaps.

For the current revision, add W-01 and W-02, and concise W-03/W-04 provenance where it improves the reader's distinctions. Further broad searching would be less useful than the already identified representation prototype and application recovery timelines. Revisit the corpus when those experiments produce a concrete question or a proposed wire interface to compare.
