# The Hatter: Degen Wonderland's time keeper (draft)

DRAFT. No key created, nothing inscribed, nothing published. Every step below that touches a key, a relay or a mint is the Admiral's.

## Why the Hatter

From the Degen Wonderland lore (`briefings/degen-wonderland-lore.md`): "Bitcoin time is the only constant we can trust in Degen Wonderland. It's tied to the block. The source of truth in a world full of lies." And: "The Hatter lost himself to find time", the madman who went so far out of the calendar he was handed that he came back holding a truer clock.

In Carroll's tea party the Hatter quarrelled with Time and it has been six o'clock ever since. Ours made peace the other way round: he lets the block set the hour. The live face (BFT-SPEC section 14) even has his moment built in: if the next block is late the face does not run on, it holds at 9:59, straining, until a real block lands. "It is always almost time, until the block says so."

The Hatter is a character account with a disclosed role (the keeper of time for Degen Wonderland), the way Lumen is a disclosed AI. It is not Pac's own key and does not speak as Pac.

## Part 1: the DW clock inscription carries the live face by itself

The DW clock ordinal can show the ticking face with nothing else: `js/bft-live.js` is self-contained (about 2 KB). It reads the height from `/r/blockheight`, and the moment it SEES the height change is its arrival time (viewer first-seen). On a cold load it reads the header time from `/r/blockinfo/<height>`, clamps the age into 0 to 599 seconds, and marks the face `estimated` until the first real change. See BFT-SPEC sections 14 and 15b.

### What an inscription can and cannot do

| can | cannot |
|---|---|
| carry pure code, forever, with no host | make outbound requests: ord's default content security policy keeps the page to its own origin (verify on the target `ord` version) |
| read the same-origin recursive endpoints (`/r/blockheight`, `/r/blockinfo/<h>`, `/content/<id>`) | open a websocket to a relay, so it cannot listen to the Hatter's signed events |
| tick, hold at 9:59, and snap on a new height | know when OUR node saw the block: only when THIS viewer's page saw it |
| import a shared library by id (`/content/<id>`) | hold a secret or a signing key: everything in it is public |
| | run a server or a timer while nobody has it open |
| | change after minting: a fix is a new inscription |
| | agree with other viewers to the second: two viewers see the same block at different moments (poll interval of 5 s, tab sleeping, load time) |

So the inscription is honest and self-sufficient, and its seconds are "since I saw it". That is enough for a living clock face; it is not a shared, signed arrival time.

## Part 2: the off-chain Hatter, a nostr key under Degen Wonderland

For sites that can fetch (every ordinary web page), the shared arrival time is better: one number, from our node, signed, the same for everyone.

### The keeper

A small daemon on the ship, fed by the block watcher that already records `first_seen` per block (`block_caller.py`, served at `/api/block-calls`, field `first_seen`). When a new block lands it signs and publishes one event as the Hatter's key. The Hatter's key is its own key under the Degen Wonderland organization: not Pac's, not Lumen's, not the house key. Where the secret lives (a `0600` file on the ship, or a NIP-46 remote signer) and which relays (the house relay first, a public relay or two for reach) are the Admiral's calls. An identity the sites can check: a NIP-05 name for the Hatter on a Degen Wonderland domain (domain: the Admiral's), and the DW organization account follows or labels the Hatter's npub (NIP-32) so a reader can tell the real Hatter from a copycat.

### The event (proposal)

One addressable event, replaced on every block, so "the latest" is one cheap query; kind number to be chosen on submission from the addressable range (30000 to 39999).

```json
{
  "kind": "<addressable, TBD>",
  "created_at": 1790900003,
  "content": "Block 969,520 is in. It is 0018.07.13 16:20 a₿. Not a second late.",
  "tags": [
    ["d", "tip"],
    ["bft", "0018.07.13 16:20 a₿", "969520", "node"],
    ["first_seen", "1790900001"],
    ["hash", "<block hash, hex>"],
    ["t", "bft"]
  ]
}
```

- `["bft", stamp, height, source]` is the tag from `nip-bft-tag.md`. Here the optional fourth field says the height came from our own node.
- `first_seen` is unix seconds: when our node first saw this hash. A site computes the live face as `liveFace(height, first_seen, its own clock)`.
- `hash` lets a reader catch a reorg: a new hash at the same height is a new event with a new `first_seen`.
- `d`=`tip` makes the event addressable; `t`=`bft` makes the family findable (multi-letter tags are not indexed by relays).
- Optional per-block history: the same event as a regular (non-replaceable) kind, if anyone wants an archive. Not needed for ticking.

### Rules for sites that listen

1. Recompute the stamp from the height; if the tag disagrees, ignore the event (NIP draft rule).
2. Check the signer is the Hatter's pinned npub.
3. A claim is not proof: compare the height with your own node when you have one. A gap of a few blocks is normal; 2 or more is said out loud.
4. The seconds are only as good as the viewer's clock. A clock behind the arrival reads 0 and is marked skewed (section 14); a clock far ahead shows "holding" early. A site MAY offset by the difference between the event's `created_at` and its own receive time.
5. No Hatter event, or a stale one: show the step with dashes (`16:2-:--`), not a guess.

### What it does not fix

It is signed by a key, not by the chain. It proves "the Hatter says our node saw this hash at T", not that T is true. For the date itself nothing changes: the height decides, always.

## The two parts together

| surface | arrival time | looks like |
|---|---|---|
| the DW clock inscription | its own viewer's first-seen (cold load: clamped header estimate, marked) | `0018.07.13 16:14:32 a₿`, holds at `16:19:59` |
| a DW website or app | the Hatter's signed `first_seen` | the same face, same seconds for everyone |
| anything with no source | none | `0018.07.13 16:1-:-- a₿` |

## Steps for the Admiral (nothing here has been done)

1. Decide the Hatter's name and the DW domain for its NIP-05.
2. Generate the Hatter's key yourself (never in a chat), choose where the secret lives.
3. Choose the relays; pick the kind number when the NIP is submitted.
4. Restart the lumen mock server so `/api/block-calls` serves `first_seen` (the watcher change is written, the running process is old code).
5. Inscribe the DW clock with `js/bft-live.js` once a target `ord` version has been checked for `/r/blockheight` and `/r/blockinfo`.
