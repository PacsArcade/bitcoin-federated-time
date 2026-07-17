# The Pupil Clock — every number, translated

*The exact math behind every number on the pupil clock study (`studies/clock-study-pupil.html`).
One height in, every reading out. Nothing on the face is decoration: every mark maps to a chain
fact, and every estimate wears a `~`.*

**The worked example below uses one block all the way through: height `958,346` —
`0018.04.20 a₿ · 04:20` (the degen beat).** Verify any cell yourself:
`python -c "import bft; print('\n'.join(bft.format_clock(958_346)))"`

---

## The ladder — how to read the whole clock with no concept of time

Every digit on the face is a **container made of the containers below it**. Read it either
direction; it has to make sense both ways.

**Top → down (big to small): what is each thing made of?**

```
0 0 1 8 . 0 4 . 2 0     0 4 : 2 7
└──┬──┘   └┬┘   └┬┘     └┬┘  │ └─ ONES of minutes — how FULL the current block is:
   │       │     │       │   │     0=empty … 9=nearly full (each step ≈ a minute) · the ~guess
   │       │     │       │   └─── TENS of minutes — which block of this hour (0–5),
   │       │     │       │         each block worth ten minutes
   │       │     │       └─────── HOUR (00–23) — six blocks each
   │       │     └─────────────── DAY (01–28) — 144 blocks, 24 hours
   │       └───────────────────── MONTH (01–13) — 28 days, one whole moon
   └───────────────────────────── YEAR — 13 moons · the year IS bitcoin's age (genesis = 0000)
```

**Bottom → up (small to big): watch time grow.**

1. Watch the very last digit. The block is **filling like a glass** — `0, 1, 2 … 9`. It's the
   only guess on the whole clock (the chain hasn't written the page yet), so it wears the `~`.
2. The glass fills — **the block breaks!** The ones snaps to `0`, and the minute-tens clicks
   up one: one more block done this hour.
3. **Six blocks** → the hour turns. `04:50` becomes `05:00`.
4. **144 blocks** → the day turns: `0018.04.20` becomes `0018.04.21`.
5. **28 days** → the moon comes back to new → the month turns.
6. **13 moons** → the year turns, and bitcoin has a birthday. 🎂

So `04:27` says, exactly: *hour 4 · block 2 of that hour · and the current block is ~7/10
full.* Nothing on the face means anything else.

---

## How one height becomes everything (the spine)

| Step | Formula | At 958,346 |
|---|---|---|
| days since genesis | `height // 144` | 6,655 |
| **beat** (block of the day) | `height mod 144` | **26** |
| year | `days // 364` | **18** |
| day of the year | `days mod 364` | 103 |
| month | `day_of_year // 28 + 1` | **4** |
| day | `day_of_year mod 28 + 1` | **20** |

All integer math. Two nodes at the same height always agree on every row.

---

## The square clock (the flip / split-flap face)

| What you see | What it is | Exact formula | At 958,346 | Truth |
|---|---|---|---|---|
| `04` — the hour cards | The block-hour (0–23). Six blocks each. | `beat // 6` | `26 // 6 = 4` | chain-exact |
| `2_` — the minute TENS card | Which block of this hour (0–5), worth ten minutes each | `beat mod 6` → shows `(beat mod 6)` as the tens digit | `26 mod 6 = 2` → `:2_` | chain-exact |
| `_0→9` — the minute ONES card (**the struggling digit**) | **How FULL the current block is**, in tenths: `0` = just broke, `7` = ~70% full, `9` = nearly done (each step ≈ a minute) | `floor(min(age/600, 0.999) × 10)` where `age` = seconds since the last block | `0` at block-break → `9` late | **~ estimate** (wears the `~`) |
| `~N% of the way to the next block` | The same live progress, in percent | `round(age / 600 × 100)` | 0–99% | **~ estimate** |
| `0018.04.20 a₿` — the dateline | The BFT date, marker after; the year IS bitcoin's age | spine table above, rendered `yyyy.mm.dd a₿` | `0018.04.20 a₿` | chain-exact |
| `OLD CAL · 16 JUL 2026` — under the dateline | The same moment on the Gregorian calendar, side by side — watch the two drift | the tip block is *now*, so its old-calendar reading is the wall date | `16 JUL 2026` | wall-clock fact |
| `958,346` — HEIGHT | The chain tip (the time itself) | mempool.space `blocks/tip/height`; offline → `anchor.h + (now − anchor.t)/600s` | `958,346` | LIVE, or **~** when estimated |
| `N payments waiting` | The mempool count | mempool.space `/api/mempool` count | live only | LIVE |
| `next block ~N% full` | How full the next block template is | mempool vsize vs ~1 MvB, capped at 100% | live only | LIVE / **~** |
| The PAC ring | **Pac laps the ring TEN times per block — his lap counter IS the struggling digit.** Dots = waiting payments; the board refills every lap | lap = `floor(age/600 × 10)` (0–9) · Pac's angle = `frac(age/600 × 10) × 360°` clockwise from 12 | — | **~** (the lap), dots = LIVE |
| The seconds (read them off Pac) | **Pac IS the seconds hand** — one lap per "minute", so his position is the seconds | **the pac-ring formula:** `seconds = age mod 60` = Pac's angle ÷ 6° | — | **~ estimate** |
| The prize at 12 o'clock | **The fruit ladder** — one prize per lap: 🍒 🍓 🍊 🥨 🍎 🍈 👾 🔔 🗝️ (classic arcade points in the tooltips; the Key ninth — it unlocks the tenth lap). **The tenth lap's prize is the ₿**, eaten at the block-break BANG. A long block parks Pac at 12, waiting beside it | prize = `FRUITS[lap]` for laps 0–8; the ₿ coin for lap 9 | — | chain-timed art |

### The flip-card back — the Day-0 countdown

| What you see | What it is | Exact formula | Truth |
|---|---|---|---|
| `block 983,664` — the target | The appointed Day-0 height (see `docs/degen-hours.md` — under review) | constant `GO_TARGET_HEIGHT` | appointed |
| `N blocks to go` | Blocks between the tip and Day 0 | `983,664 − height` (floored at 0) | chain-exact given the height |
| `DDD:HH:MM:SS` | The same distance as wall time | `blocks_to_go × 600 s`, ticking down against a fixed anchor, re-anchored when the chain moves | **~ estimate** |
| The Day-0 surprise | Fires once, when blocks-to-go hits 0 — no spoilers here; be there (or dig in the source, if you must) | `height ≥ 983,664` | chain-exact |

---

## The circle clock (the analog / moon face)

| What you see | What it is | Exact formula | At 958,346 | Truth |
|---|---|---|---|---|
| The hour hand (calm) | The block-hour on a 12-hour face, stepping 5° per block | `(hour mod 12) × 30° + (beat mod 6) × 5°` | `4×30 + 2×5 = 130°` | chain-exact |
| The minute hand (struggles) | The ten-minute beats plus live progress in this block | `((beat mod 6) + sub) / 6 × 360°`, `sub = age/600` | `(2+sub)/6 × 360 = 120°→180°` | **~** (the `sub` part) |
| The lit hour tick | Which of the 12 marks is "now" | `(beat // 6) mod 12` | `4` | chain-exact |
| The 8-bit moon face + name | The block-timed moon: one lunation per 28-day month | `round((day−1)/28 × 8) mod 8` → 8 phases; D01 new · ~D15 full | day 20 → index 5 → 🌖 Waning Gibbous | chain-exact |
| `LEVEL 475` | The arcade level = difficulty epoch | `height // 2016` | `475` | chain-exact |
| `re-tunes in N blocks` | Blocks left in this difficulty period | `2016 − (height mod 2016)` (or the API's remaining, when live) | `1,270` | chain-exact / LIVE |
| `▲ / ▼` beside LEVEL | Estimated difficulty change direction at the next re-tune | mempool.space `difficultyChange` sign | live only | LIVE **~** |
| ₿ coin at 12 + fiat ghosts on 1–11 | The thesis, not a number: every block, bitcoin eats the world's fiat; the reward coin is the only gold | eat-loop rides the block-break events | — | art (block-timed) |

---

## The offline anchor (how the clock guesses with no network)

Blocks have come faster than 10 minutes over bitcoin's life, so anchoring an estimate at genesis
lands a whole year low. The pupil anchors at a recent known block instead:

```
RECENT_ANCHOR = block 957,877 at 2026-07-13 16:13:46 UTC
estimated height = 957,877 + (now − anchor) / 600 s      ← always wears the ~
```

Bump the anchor to a fresh `(height, timestamp)` pair periodically; the whole estimate column
above inherits its honesty from this one line.

---

## Reading the same block everywhere (cross-check)

Block **958,346**, every surface, one truth:

```
Clock (hh:mm):    04:20                     hour 4 · block 2 of the hour · live digit climbing
Date (BFT):       0018.04.20 a₿             year 18 = bitcoin's age · month 4 · day 20
Level:            475 · re-tunes in 1,270    958,346 // 2016 · 2016 − 746
Moon:             🌖 Waning Gibbous          day 20 of the 28-day lunation
Halving epoch:    4 · subsidy 3.125 BTC     958,346 // 210,000 · 50 / 2⁴
Day-0 distance:   25,318 blocks             983,664 − 958,346   (≈ 175.8 days at 10 min)
Ordinal sidebar:  0°118346′746″0‴           cycle 0 · block 118,346 of the epoch · block 746 of the period
```

*Every number above was computed, not typed — recompute any of them with the library before you
reuse them. That's the house precision rule.*
