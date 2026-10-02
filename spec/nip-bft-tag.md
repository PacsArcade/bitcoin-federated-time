NIP-XX
======

BFT tag: a block height and its Federated Time date
---------------------------------------------------

`draft` `optional`

DRAFT FOR THE ADMIRAL. Not submitted. The number is assigned in the pull request to nostr-protocol/nips.

This NIP defines one optional tag, `bft`, that an event author MAY add to any event to say which Bitcoin block height the event was made at, together with the Bitcoin Federated Time (BFT) stamp for that height. BFT is a calendar derived from a block height with integer arithmetic only: 144 blocks a day, 28 days a month, 13 months a year. The full rules and test vectors are in https://github.com/PacsArcade/bitcoin-federated-time (`spec/BFT-SPEC.md`, `vectors/vectors.json`).

## The tag

```json
["bft", "0018.07.13 16:10 a₿", "969505"]
```

| position | value |
|---|---|
| 0 | `"bft"` |
| 1 | the BFT stamp: `YYYY.MM.DD HH:MM a₿` (year at least four digits, marker after) |
| 2 | the block height as a base-10 string of digits, no separators |
| 3 | OPTIONAL: where the height was read, one of `beacon`, `node`, `public` |

A client or relay MAY ignore this tag. An event without it is a complete event.

## Verification

The stamp is a pure function of the height. A reader that cares MUST recompute the stamp from field 2 and treat the tag as invalid if the strings differ. Field 2 has to be a non-negative integer with no leading zeros (except `0`); anything else makes the tag invalid.

The tag is a claim, not a proof. It says "the author saw this height", the way `created_at` says "the author's clock read this". A reader that wants to check the claim compares the height with the chain, and can compare it with `created_at` for plausibility (blocks arrive about every ten minutes, but the spread is wide). A client SHOULD NOT reject an event because the height is behind or ahead of its own view of the tip by a few blocks.

## Dashes

An author with no height MUST omit the tag. It MUST NOT write a guessed height or a placeholder stamp.

## Relation to other NIPs

* Not a replacement for `created_at` (NIP-01). BFT is a second, optional reading of time.
* NIP-52 calendar events keep `start`/`end` in unix seconds. An application MAY add a `bft` tag describing the start; the calendar semantics stay in NIP-52.
* Multi-letter tags are not indexed by relays (NIP-01 expects only single-letter tags to be). To find events by BFT, a client SHOULD add `["t", "bft"]` (NIP-24) or use a NIP-32 label in a namespace such as `org.pacsarcade.bft`, and filter by that.

## Example

```json
{
  "kind": 1,
  "created_at": 1790856000,
  "content": "gm",
  "tags": [["bft", "0018.07.13 16:10 a₿", "969505", "beacon"], ["t", "bft"]]
}
```

## Implementations

(To be filled before submission. NIPs are expected to be implemented in at least two clients and one relay where applicable; for this tag a relay is not needed. Candidates: meetkit (the meetup kit already emits `["bft", stamp, height]`), Lumen, the Pac's Arcade site.)
