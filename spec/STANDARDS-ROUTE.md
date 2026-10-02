# How BFT gets formally recognized: the route

Researched at block 969,505 (0018.07.13 a₿) from the primary documents linked below. Nothing has been posted or submitted anywhere. The Admiral submits.

## Verdict

1. **Best fit now: a NIP** for the optional `["bft", stamp, height]` tag. Low bar, no mailing list, the shape already ships in meetkit. Draft: `nip-bft-tag.md`.
2. **Second: an Informational BIP**, but only after the NIP has real implementations, and expect a scope argument. A calendar convention is not protocol, so it is borderline. Draft: `bip-bft-calendar.md`. Open it as a conversation on the mailing list first; do not open a pull request cold.
3. **Third, cheap and parallel: an ordinals inscription convention**, no process needed: inscribe `js/bft.js` once and let other inscriptions import it. Draft: `ORDINALS-CONVENTION.md`.
4. **Always: the repo is canonical.** `spec/BFT-SPEC.md` plus `vectors/vectors.json` in `PacsArcade/bitcoin-federated-time`. Every other route points here. A standard people can run beats a number.

## The BIP route, in detail

**Current rules are BIP 3, not BIP 2.** The bitcoin/bips README says it now uses BIP 3 (Updated BIP Process), and BIP 3's own preamble reads Status: Deployed (assigned 2025-01-09). BIP 3 replaces BIP 2: it drops the "Standards Track" type for three types (Specification, Informational, Process), collapses nine statuses into four (Draft, Complete, Deployed, Closed), and abolishes the comment system. Sources: [BIP 3](https://github.com/bitcoin/bips/blob/master/bip-0003.md), [BIP 2](https://github.com/bitcoin/bips/blob/master/bip-0002.mediawiki), [repo README](https://github.com/bitcoin/bips/blob/master/README.mediawiki).

**Order of events.**
1. Describe the idea to bitcoindev@googlegroups.com first, "to gather feedback" (README). Archived at [gnusha.org/pi/bitcoindev](https://gnusha.org/pi/bitcoindev/). The BIP 3 discussion itself happened there ([thread](https://gnusha.org/pi/bitcoindev/458a5831-a1a2-4c21-ab61-dccd00ed5219@murch.one/t)).
2. Open a pull request only "when substantial progress on the draft has been made." Use a filename like `bip-bft-calendar.md` (Markdown or MediaWiki are both allowed). Auxiliary files go in a `bip-XXXX/` folder (our vectors would go there).
3. Authors do not assign their own number. An editor assigns one after the proposal (1) follows the formatting rules, (2) is on-topic, and (3) "materially progressed beyond the ideation phase" through public discussion from diverse contributors.

**Required preamble** (from BIP 3): BIP, Title (50 characters or fewer), Authors, Status, Type, Assigned, License (an SPDX expression), plus optional Layer, Deputies, Discussion, Version, Requires, Replaces. Required sections: Abstract, Copyright, Motivation; also Specification, Rationale, Backward Compatibility, Reference Implementation, Changelog where they apply. Our draft is built to that shape.

**What editors accept and reject.** They check on-topic, format, license, motivation, a sufficient specification, and general interest. They do not judge adoption likelihood. They decline duplicates, format violations, unfocused scope, thin motivation, unaddressed backward compatibility, unclear specs. The README says editors are "expected to be liberal with publishing BIPs", but controversial proposals are closed by default.

**Is a calendar convention in scope?** Honest answer: borderline, leaning yes for Informational. BIP 3 limits the repository to BIPs that do not oppose Bitcoin as peer-to-peer electronic cash, concerning "the Bitcoin protocol, peer-to-peer network, and client software". A block-height calendar touches none of consensus, relay or wallet behavior. In its favor: the Layer value `Applications` exists, and the README lists application-level Informational BIPs (BIP 21 URI scheme, BIP 39 mnemonics, BIP 69, BIP 85). Against: those are tied to how wallets and software interoperate; "how to print a date" is a thinner link. We could not find a published precedent of a time or calendar BIP. We did not test the editors' reaction. Treat this as the editors' call.

**Informational vs Specification.** Specification needs a reference implementation and test vectors before Complete; we have both, but it implies other software should change. Informational fits: nothing is required of anyone. Complete means the author recommends adoption; Deployed needs evidence of active use, which is why running code in several projects first helps.

## The NIP route

Process ([nips README](https://github.com/nostr-protocol/nips/blob/master/README.md)): open a pull request to nostr-protocol/nips. Rules: fully implemented in at least two clients and one relay "when applicable"; "should make sense"; "optional and backwards-compatible"; "no more than one way of doing the same thing". Our tag is optional and ignorable, so it is backwards-compatible by construction. A relay is not needed because relays do not process it.

Things the draft handles: [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md) expects relays to index only single-letter tags, so `bft` cannot be filtered on directly. The draft says to add `["t","bft"]` ([NIP-24](https://github.com/nostr-protocol/nips/blob/master/24.md)) or a [NIP-32](https://github.com/nostr-protocol/nips/blob/master/32.md) label in a reverse-domain namespace to make events findable. The existing `["bft", stamp, height]` shape from meetkit is kept, with one optional fourth field.

Before submitting: two clients should emit and display it (meetkit is one; Lumen or the arcade site can be the second). Check for an overlapping NIP first (the "one way" rule); NIP-52 calendar events use unix `start`/`end`, so we describe BFT as an add-on there.

## The ordinals route

No formal standards process was found for ordinals conventions; the ord docs describe behavior, and conventions spread by use. The relevant primitive is recursion: [recursive endpoints](https://docs.ordinals.com/inscriptions/recursion.html) are whitelisted, with a backwards-compatibility promise (not removed, fields not renamed). `/r/blockheight` gives the latest height; `/content/<INSCRIPTION_ID>` lets one inscription load another. So the convention is: inscribe `js/bft.js` once, publish its inscription id in this repo, and let others import it. See `ORDINALS-CONVENTION.md`. The 5-line function is pure, so it survives any ord version change except the endpoint names, which carry the stability promise.

## What we could not verify

- Whether bitcoindev will see a calendar convention as on-topic (no published precedent found; no list reaction tested).
- That `/r/blockheight` returns a bare number on the exact `ord` version the Admiral inscribes against (the docs list it; test on the target server).
- Whether a NIP already covers a block-height tag (a search of the repo README did not show one; search the PR list before submitting).

## Suggested order for the Admiral

1. Merge this lane; cut the repo release; make the spec URL the one link everyone cites.
2. Get a second client emitting the tag, then open the NIP pull request.
3. Decide on the inscription (it costs sats; the draft convention is ready).
4. Post a short feeler to bitcoindev with the Abstract, link the repo, ask "is this on-topic as Informational?". Only on a yes, open the pull request.
