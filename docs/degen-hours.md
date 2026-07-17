# Day 0 & the Degen Hours — the appointed window

*Decision paper · double-checked numbers · **PROPOSAL — awaiting Pac's key-signed
sign-off.** Nothing below is canon until he blesses it.*

## The two moments that make the window

Bitcoin turns 18 on the sun's calendar on **3 Jan 2027** (genesis: 2009-01-03 18:15:05 UTC).
The new moon nearest that birthday is **7 Jan 2027 ~20:24 UTC**. Pac's call (0018.04.17 a₿):
**Day 0 = the new moon that starts the new calendar.** Today's refinement: the span between the
solar birthday and the lunar birth **is itself the thing** — the old year done, the new one not
yet lit. **The Degen Hours.**

## The verified numbers

All height estimates use the pupil's honest anchor (block 957,877 @ 2026-07-13 16:13:46 UTC) and
wear the `~` — the real chain will drift; **the appointed heights are exact, their wall-clock
arrival is not.**

| Moment | Wall clock (est.) | ~Height @600s/blk | @590s/blk | Nearest bitcoin-midnights |
|---|---|---|---|---|
| Sol birthday opens | 2027-01-03 00:00 UTC | ~982,836 | ~983,259 | 982,800 · 982,944 |
| **The exact anniversary** | 2027-01-03 18:15:05 UTC | **~982,945** | ~983,370 | **982,944** · 983,088 |
| **The new moon** | 2027-01-07 ~20:24 UTC | **~983,534** | ~983,969 | 983,520 · **983,664** |

Three things worth Pac's eye:

1. **The appointed Day-0 height 983,664 checks out.** It sits inside the new moon's plausibility
   band (it corresponds to ~597 s/block — real blocks have averaged slightly under 600). It is a
   true bitcoin-midnight (983,664 = 144 × 6,831 → `00:00`), and it is **the first midnight whose
   BFT moon face reads 🌑 New** (at 983,520 the face still reads Waning Crescent). Date:
   `0018.10.28 a₿`.
2. **The exact 18th-anniversary moment lands ~1 block after midnight 982,944** (`0018.10.23
   00:00 a₿`, ~2027-01-03 18:05 UTC at the 600s model). The chain practically hands us the
   opening bell.
3. **983,664 is D28 — the last day of month 10 — not a month-start.** The moon completes on D28,
   and the *next* midnight, **983,808, opens M11·D01** — the "months begin on the new moon"
   purist reading. If Day 0 must *open* a month, that is the candidate.

## The proposed Degen Hours (chain-exact)

> **Degen Hours = blocks 982,944 → 983,664.**
> From the midnight of bitcoin's exact 18th anniversary to the appointed new-moon midnight:
> **exactly 720 blocks = 5 BFT days = 120 block-hours** of liminal time.
> Bitcoin is already 18 on the sun's clock; the new calendar hasn't been born on the moon's.
> The hours in between belong to the degenz.

Defined in blocks, the window needs no wall clock and cannot drift: it opens when block 982,944
is mined and closes when 983,664 breaks the balloons loose. (The *dates* 3–7 Jan are the
estimate; the *blocks* are the appointment.)

## The Hallows resonance (Pac's spark, 0018.04.20)

Day 0 — `0018.10.28 a₿` — is **the last day of the tenth month**: structurally, the new
calendar's own **All Hallows' Eve**. And the chain already blessed that night once —
**Satoshi published the whitepaper on 31 October 2008** (`2008.31.10 b₿`), actual All
Hallows' Eve on the old calendar. So the new calendar is born on its own Halloween, under a
**dark moon**, echoing the night the whitepaper dropped — and the next midnight opens
`M11·D01`, the hallows' *day*: a new month, on a new moon, on the other side of the veil.
The Degen Hours end where the whitepaper began. Lore, free of charge, from the math.

## For Pac to bless (pick one per line)

| Decision | Option A (as coded today) | Option B |
|---|---|---|
| Day-0 height | **983,664** — first New-moon midnight, `0018.10.28 a₿` (pupil's `GO_TARGET_HEIGHT`) | 983,808 — month-start new moon, `0018.11.01 a₿` |
| Degen Hours open | **982,944** — the anniversary midnight | 982,800 — midnight opening the sol birthday itself |
| During the window | pupil counts down as today | a visible DEGEN HOURS state on the clock (ember breath, ghost-side styling) |

If any choice changes `GO_TARGET_HEIGHT`, the pupil study and the DW countdown brief
(`dw-countdown-clock-moodboard.md`) update together — one constant, every surface.

*Numbers computed from the library and the pupil's anchor; the new-moon timestamp
(2027-01-07 20:24 UTC) is astronomy, verified against public ephemeris sources — see the
verification report. Wonder, not finance.*
