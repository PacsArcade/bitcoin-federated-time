# The Bitcoin Holidays — the chain's own feast days

*Every value below was computed from this package (`bft.holidays`) — the house precision
rule. Storied research: the DW desk's chain-verified table (commissioned 0018.04.15 a₿);
this doc recomputes every BFT label through the library. Try it live:
`python -m bft` prints today's feast days and what's coming up.*

## The storied days (one-time history, block-anchored)

**Exact** = the event IS a block. **~** = an old-calendar date bridged onto the chain.

| Block | BFT date | | Holiday | The story, one line |
|---|---|---|---|---|
| 0 | `0000.01.01 a₿` | exact | **Genesis Block Day** | Block 0, the Times headline folded inside — the clock starts. |
| 78 | `0000.01.01 a₿` | ~ | **Running Bitcoin Day** | Hal Finney, out loud: "Running bitcoin" — the first believer shares day one with genesis. |
| 57,043 | `0001.02.05 a₿` | exact | **Bitcoin Pizza Day** | 10,000 BTC for two pizzas — the first real-world purchase. |
| 97,230 | `0001.12.04 a₿` | ~ | **Satoshi Vanishing Day** | The last post, then quiet — the chain keeps going without him. |
| 210,000 | `0004.01.03 a₿` | exact | **The First Halving** | 50 → 25. The schedule holds. |
| 275,603 | `0005.04.10 a₿` | ~ | **HODL Day** | "I AM HODLING" — a typo becomes a creed. |
| 420,000 | `0008.01.05 a₿` | exact | **The Second Halving** | 25 → 12.5. The schedule holds. |
| 478,479 | `0009.02.19 a₿` | ~ | **Bitcoin Independence Day** | BIP-148: users, not miners, enforce the rules. |
| 481,824 | `0009.03.15 a₿` | exact | **SegWit Day** | Malleability fixed; Lightning unlocked. |
| 630,000 | `0012.01.08 a₿` | exact | **The Third Halving** | 12.5 → 6.25 — the schedule holds, even mid-pandemic. |
| 709,632 | `0013.08.01 a₿` | exact | **Taproot Day** | Schnorr lands — at 176 × 4,032, exactly on a BFT month boundary. |
| 840,000 | `0016.01.10 a₿` | exact | **The Fourth Halving** | 6.25 → 3.125 — mined on 4/20, because of course it was. |
| 1,050,000 | `0020.01.12 a₿` | exact | **The Fifth Halving** (next) | 3.125 → 1.5625 — the block is fixed; only the wall-clock date drifts. |

**Before the light (b₿):** **Whitepaper Day** — 31 Oct 2008, All Hallows' Eve —
computes to `0000.03.09 b₿` (~height −9,217). **Satoshi's chosen birthday** — 5 Apr 1975,
lore-grade — computes to `0033.12.08 b₿`. *(An earlier research draft composed these two
labels differently; the values here come straight from `bft.format_date()` — compute, don't
copy.)*

Every halving so far — and the next — lands in **month 1**, sliding ~2⅓ days later each
epoch (D03 · D05 · D08 · D10 · D12 …): the BFT year opens with halving season every fourth
year until the 12th halving (block 2,520,000, ~2056) finally rolls into month 2.

## The recurring feast days (the calendar throws these forever)

| Day | Holiday | Why |
|---|---|---|
| `M01·D01` | **New Year** | Every year opens on the **calendar's** new moon — 52,416 blocks, no exceptions. The sky agreed once, at Day 0 (a real new moon, ~7 Jan 2027), then drifts ~9.6 days of phase a year; the calendar's moon keeps the feast. |
| `M10·D28` | **The Hallows** | The last day of the tenth month: the new calendar's All Hallows' Eve, honoring the whitepaper's 31 Oct 2008. In year 0018 this is **Day 0** — block 983,664 opens it. |
| `M13·D01` | **Sol's Seat opens** | The thirteenth month begins; every day of it is a whisper day. |
| `M13·D13` | **The Thirteenth of the Thirteenth** | The loudest whisper of the year. |
| `M13·D28` | **Year's End** | The 364th day; the year completes with the calendar's moon. |
| every D13 · all of M13 | **Whisper days** (rhythm) | The thirteens — the clock may speak (`bft.lore.whisper`). |
| every 210,000 blocks | **Halving Day** | Epic sats are minted; the subsidy halves. |
| every 1,260,000 blocks | **The Conjunction** | Halving meets retarget: the ~24-year hour ticks; a legendary sat is born. First: ~2032. |
| every 13th year | **A Year of the Cat** | The whole year belongs to the Astronomical Cat (AB 11, 24, 37…). |

Holiday **names are offered, not baked** — the arcade blesses names the way it blesses month
names: by decision, not by code. The **heights** are the canon. *(Considered and left off,
per the desk: difficulty re-tunes — every 2,016 blocks is rhythm, not holiday.)*

## Use it

```python
from bft import holidays
holidays.holidays_at(840_000)          # what made this day a feast day (if anything)
holidays.next_holidays(958_346, 5)     # the next five, with day-start heights + dates
holidays.year_calendar(18)             # the printable calendar of one BFT year
```

```bash
python -m bft            # the clock ~now, today's feast days, and what's coming up
python -m bft 840000     # any block's whole story
```

*Wonder, not finance. Estimates wear the ~; the chain vouches only for heights.*
