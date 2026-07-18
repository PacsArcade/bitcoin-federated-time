# Bitcoin Federated Time (BFT)

> *Prefer your time with tea? There is a second telling of this clock — the Hatter's, down in
> [Degen Wonderland](https://github.com/DegenWonderland). Same math, more madness. Follow the
> white rabbit.* 🎩🐇

**A block height is a timestamp no authority can edit.** This is a tiny, dependency-free Python
library that reads a Bitcoin block height as time — three honest ways, plus one sidebar:

1. **The clock** — the `hh:mm` **block-beat**: a BFT day is 144 blocks on a 24-hour face,
   6 blocks an hour, ten "minutes" a block — and yes, **seconds**: they ride the Pac ring.
   **`seconds = time since the last block, mod 60`** — Pac laps once a minute, so his angle
   ÷ 6° *is* the seconds hand (a live `~`estimate, like all sub-block time). The face people
   read.
2. **A calendar** — 13 perfect 28-day months, counted purely in blocks: `0018.04.20 a₿`.
3. **The countdowns** — the *inverse* of the block count: blocks remaining to the next difficulty
   retarget, the next halving, the next cycle, and the last satoshi (~year 2140).
4. *(sidebar)* **The ordinal degree notation** `A°B′C″D‴`, which ordinal theory labels
   hour/minute/second/third — real sat-collector lore, honestly framed as indices, not clock time.

And a bridge from the calendar you were handed: **enter any Gregorian date and time and get it back
in Bitcoin time** — with dates before the 2009 genesis block winding the clock backward into
*Before Bitcoin*.

> **BFT** also reads as *Byzantine Fault Tolerance* — which is the point. The network agrees on the
> height, so it agrees on the time. No almanac, no leap-second committee, no pope deleting ten days.
> The longest chain is the clock.

## The hidden reading of "BTC" → **Bitcoin Time Clock**

The ticker is, and only is, Bitcoin. But every block is a tick, and the chain keeps a steadier
count than any wall clock — so we gave the count a face. Call it the **Bitcoin Time Clock** if you
like; that's a lens, not a claim about the ticker.

## Install

Zero dependencies, Python 3.9+.

```bash
pip install bitcoin-federated-time      # once published
# or vendor it right now: copy the bft/ folder into your project
```

## Quick start

```bash
python -m bft 958346     # the whole clock in your terminal — plus today's feast days
python -m bft 1983-06-13 # a birthday (b₿ before genesis)
```

```python
import bft

bft.block_beat(958_346)["hhmm"]  # '04:20'                (the canonical hh:mm face)
bft.format_date(958_346)         # '0018.04.20 a₿'        (the ₿-marked bitcoin date)
bft.halving(958_346)             # {'epoch': 4, 'subsidy_btc': 3.125, 'blocks_to_next_halving': 91654}
bft.countdown(958_346)           # {'to_halving': 91654, 'to_last_satoshi': 5971654, ...}
bft.holidays.next_holidays(958_346, 3)   # the chain's coming feast days (docs/bitcoin-holidays.md)

print("\n".join(bft.format_clock(958_346)))
# Bitcoin Time Clock — block 958,346
#   Clock (hh:mm):    04:20   (beat 26/144 · 6 blocks an hour · ten minutes a block)
#   Date (BFT):       0018.04.20 a₿   (AB 18 · M04 · D20)
#   Level:            475  ·  re-tunes in 1,270 blocks
#   Halving epoch:    4  ·  subsidy 3.125 BTC  ·  56.4% through
#   Cycle:            0  ·  76.1% through  ·  301,654 blocks to the next conjunction
#   Counting down:    1,270 → retarget  ·  91,654 → halving  ·  5,971,654 → the last sat
#   Ordinal sidebar:  0°118346′746″0‴   (degree notation, for the sat collectors — ordinal
#                     indices, not clock time; first sat: uncommon)
```

### Your birthday in Bitcoin time

```python
bft.from_gregorian(1995, 6, 15, 12, 0)   # a Gregorian UTC birthday → the full clock
# {'height': -712982, 'before_bitcoin': True, 'estimate': True, 'calendar': {...}}
bft.format_date(bft.height_at(1995, 6, 15))   # '0013.08.24 b₿'  — before genesis, same format
bft.format_date(bft.height_at(2015, 7, 20))   # '0006.08.09 a₿'
```

Born before 2009-01-03? Your height is **negative** and the clock runs in reverse — *Before
Bitcoin*. Born after? You get an `a₿` date and your place on the clock. It's an **estimate**
(see honesty notes) — the model dates you at a steady 10-minute block.

## The readings

### 1. The clock — `hh:mm` block-beat

The canonical face. All of it is chain-exact — two nodes at the same height show the same time:

| Piece | Formula | Range |
|---|---|---|
| beat | `height mod 144` | 0–143 (the block within the BFT day) |
| **hh** | `beat // 6` | 0–23 (the block-hour) |
| **mm** | `(beat mod 6) × 10` | 00, 10, 20, 30, 40, 50 |
| *ones of minutes* | `floor(block-age / 60)`, capped at 9 | how full the current block is, in tenths — **~** |
| *seconds* | **the Pac-ring formula:** `block-age mod 60` — Pac laps once a "minute", so his angle ÷ 6° IS the seconds hand | 0–59 — **~** |

Six blocks an hour, ten minutes a block, **no second digits on the cards** — the chain-exact
face is calm on purpose (see "the long view"). The live column is honest about being a guess:
the minute-ones digit is the current block filling in tenths, and the seconds are read off the
ring — both estimated from wall time since the last block, both wearing the `~`, because the
chain hasn't vouched for that page yet.

### 2. The calendar

- **Epoch:** the genesis block (height 0, 2009-01-03) starts the clock. Heights ≥ 0 are **After
  Bitcoin (a₿)**; negatives are **Before Bitcoin (b₿)**, the inverse.
- **The date:** `yyyy.mm.dd a₿`, marker after, year zero-padded to four — **the display year is
  bitcoin's age** (genesis opens `0000`). Before Bitcoin reads identically: `yyyy.mm.dd b₿` — one order, both epochs.
- **Units:** day = 144 blocks · week = 1,008 · **fortnight = 2,016 (one difficulty period)** ·
  **month = 4,032 (two difficulty periods) = 28 days** · **year = 52,416 (26 periods) = 364 days**.
- **13 months of 28 days = 364 days.** No leap hacks, no intercalary day. It drifts ~1.24 days/year
  against the sun — **on purpose**. It tracks the chain's heartbeat, not the earth's orbit.
- **Month names aren't baked in.** Pass `format_date(h, month_names=[...13...], style="short")` for
  your own; otherwise the short style renders `M01..M13`. (The naming of the 13 moons is a
  decision the arcade makes by vote, not a constant in a library.)

### 3. The countdowns (the inverse)

There are **no negative block heights on-chain** — the chain starts at genesis. So "counting
backward" in Bitcoin means the *remaining-block countdowns*: `countdown(h)` gives blocks to the
next retarget, the next halving, the next cycle, and the last satoshi. The forward count (height,
sats rising toward ~2.1 quadrillion) and the down count (subsidy shrinking toward zero, the 21M cap
approaching) are mirror images of one schedule. Negative *inputs* are the conceptual inverse:
`from_height(-h)` renders the **b₿** epoch.

### 4. The ordinal sidebar — for the sat collectors

Bitcoin's degree notation `A°B′C″D‴`, straight from ordinal theory, labels the four positions
**hour, minute, second, third** — that's [in the handbook](https://docs.ordinals.com/overview.html),
not our invention. They are **ordinal indices, not clock time**:

| Position | Ordinal name | Is | Ticks every |
|---|---|---|---|
| `A°` | **hour** | cycle number | 1,260,000 blocks (~24 years) |
| `B′` | **minute** | block index in the halving epoch | 210,000 blocks (~4 years) |
| `C″` | **second** | block index in the difficulty period | 2,016 blocks (~2 weeks) |
| `D‴` | **third** | sat index in the block | each sat |

## This is how ordinals and runes already work

The calendar and ordinal theory are **the same skeleton**, because both are built from Bitcoin's
only native clock intervals — and each interval's first satoshi is exactly an ordinal rarity:

| Interval | Blocks | Degree | BFT unit | First-sat rarity |
|---|---|---|---|---|
| block | 1 | third ‴ | the tick | uncommon |
| difficulty period | 2,016 | second ″ | 1 fortnight | rare |
| halving epoch | 210,000 | minute ′ | ~4 years | epic |
| cycle | 1,260,000 | hour ° | ~24 years | legendary |
| genesis | — | `0°0′0″0‴` | `0000.01.01 a₿` | mythic |

A BFT **month is exactly two difficulty adjustments**, so the calendar's page turns on the very
events that mint rare and epic sats. **Runes** ride the same clock — a rune ID is literally
`block:tx`, and open-mint terms are block-height windows. If you're numbering sats or etching runes,
you're already telling Bitcoin time; this library reads it back to you.

## The sky comes free (`bft.sky`)

There are two moons in this house, and both are honest because we label them. **The
calendar's moon** lives here: a 28-day month is *almost* one trip of the real moon
(~29.53 days), so BFT keeps a block-timed, symbolic lunation — D01 new, D15 full, D28
home — that drifts from the sky ~1.5 days a month **on purpose**, the same way the
364-day year drifts from the sun. **The sky's moon** is the one over your head; ask the
sky, not this module. They agree at Day 0 — the calendar begins on a **real** new moon
(block 983,664, ~7 Jan 2027) — and part ways after, ~9.6 days of phase per BFT year.

So every BFT month begins on a *calendar* new moon, and every BFT new year is a
new-moon new year **on the calendar's moon** — true by construction, checkable by
anyone. Each year also carries one of **thirteen** animal signs: the traditional
twelve, plus the **Astronomical Cat** as the thirteenth (the sign left out of the
Great Race).

```python
import bft
bft.moon_phase(920_000)          # {'emoji': '🌒', 'name': 'Waxing Crescent', ...}
bft.year_animal(920_000)         # {'emoji': '🐍', 'name': 'Snake', ...}
bft.format_date(858_000)         # '0016.05.23 a₿'  — the ₿-marked bitcoin date
```

Signs and moons are for wonder, not finance — and the calendar's moon never pretends to
be the sky's. Same house rule as the rest of BFT.

## Little guides & studies

The [`guides/`](guides/) folder has short, illustrated, ELI5 walkthroughs — written so a sharp
five-year-old can follow and a grown-up still learns something: the block clock, the thirteen months
and the moon, the two calendars side by side, and a kid-safe lesson on never sharing your keys.

The [`studies/`](studies/) folder holds the living clock studies — the flagship **pupil clock**
(two clocks, one time, PAC-MAN eats the mempool) and the **bitcoin birthday** converter — plus
[`docs/`](docs/) with the exact math grid behind every number on the clock face.

## The long view — "the longer-living time"

A quiet idea this project is built around: Bitcoin rewards patience, and measuring your life in
blocks nudges you toward a longer view. Ten minutes is a long time to a day-trader and no time at
all to a forest. As we learn to think in halvings and cycles — and as we look out for our frens
across long horizons instead of the next candle — a **block can become the new second**: the shared,
unhurried heartbeat of people who plan in decades. That's the "longer-living time." It's a
philosophy, not a physics claim — but it's why the fastest hand on this clock is a ten-minute beat,
and why the network only re-tunes itself once a fortnight. Slow is the feature.

## Honesty notes (please keep these if you fork)

- This is **deterministic block arithmetic**, not wall-clock time. A block's timestamp is miner-set
  and only loosely tracks real time. `height_at()` dates a moment at a *steady* 10-minute block, so a
  past date won't land on the exact height it historically did (real blocks came a bit faster), and a
  future date is a projection. What's exact is the math; what every node agrees on is the height — use
  a real tip when you need on-chain truth.
- The 21-million cap and the ~10-minute target are implementation constants, not lines in the Bitcoin
  whitepaper. The subsidy schedule (50 BTC, halving every 210,000 blocks, flooring to 0 at epoch 33
  near block 6,930,000) is what fixes issuance at ~2140.
- "Bitcoin Time Clock" is a *reading*, not the meaning of the ticker.

## The spark — where this came from

This project was born around the **Ordinals coding club**. Pac sat in on many of those
sessions — even got to sign off on one of the requests for some testing — and the idea took
root there. Then, at Portland's **Bitcoin is for Everyone**, the auditorium screen carried the
generic time clock laid out exactly as ordinal theory describes it: hour, minute, second,
straight from the handbook. Watching it, one thing was plain: **it could be better.** Not
wrong — just not deep enough. The notation names the positions; it doesn't take you down to
the *meaning*.

So we went deeper — we're degenz; that's the job. Ordinal theory didn't break the clock down
to this level. We kept digging until the `hh:mm` face, the 13-month calendar, the block-timed
moon, the countdowns, and the lore all fell out of the **same block math** — until we hit
**the heart of bitcoin**. And we display it the way the arcade remembers everything worth
keeping: **8-bit, nostalgic, alive.**

## Prior art & credit

- **Ordinal theory** and degree notation: Casey Rodarmor, who created it; raphjaph and the
  `ord` maintainers and contributors who carry it; and the community's
  [Ordinal Theory Handbook](https://docs.ordinals.com/overview.html). The
  hour/minute/second/third labels are theirs; this library keeps them, honestly labeled, as
  the sidebar — and digs on past them.
- Block-time calculators and hardware **block clocks** exist, and the generic ordinal time
  clock has graced conference screens. What didn't exist, as far as we found, is a small
  **library + spec** unifying an `hh:mm` block-beat face, a block-native 13-month calendar,
  the halving/countdown math, and a Gregorian bridge — so here it is, for anyone to use.

## License

MIT. Built by the Pac's Arcade non-profit — *nobody should have to trust; everybody should get to
verify.* Contributions welcome.
