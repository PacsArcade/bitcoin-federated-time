# Bitcoin Federated Time (BFT)

**A block height is a timestamp no authority can edit.** This is a tiny, dependency-free Python
library that reads a Bitcoin block height as time — three honest ways:

1. **A calendar** — 13 perfect 28-day months, counted purely in blocks.
2. **The ordinal clock** — Bitcoin's own degree notation `A°B′C″D‴`, which ordinal theory already
   reads as **hour° / minute′ / second″ / third‴**. Bitcoin has been keeping time all along.
3. **The countdowns** — the *inverse* of the block count: blocks remaining to the next difficulty
   retarget, the next halving, the next cycle, and the last satoshi (~year 2140).

And a bridge from the calendar you were handed: **enter any Gregorian date and time and get it back
in Bitcoin time** — with dates before the 2009 genesis block winding the clock backward into
*Before Bitcoin*.

> **BFT** also reads as *Byzantine Fault Tolerance* — which is the point. The network agrees on the
> height, so it agrees on the time. No almanac, no leap-second committee, no pope deleting ten days.
> The longest chain is the clock.

## The hidden reading of "BTC" → **Bitcoin Time Clock**

The ticker is, and only is, Bitcoin. But ordinal theory labels the four positions of its degree
notation **hour, minute, second, third** — that's [in the handbook](https://docs.ordinals.com/overview.html),
not our invention. Read that way, every block is a tick and the chain is a clock. We just gave it a
face. Call it the **Bitcoin Time Clock** if you like; that's a lens, not a claim about the ticker.

## Install

Zero dependencies, Python 3.9+.

```bash
pip install bitcoin-federated-time      # once published
# or vendor it right now: copy the bft/ folder into your project
```

## Quick start

```python
import bft

bft.format_date(920_986)        # 'AB 17 · M08 · D12'   (the 13-month block calendar)
bft.degree(920_986)             # {'notation': '0°80986′1690″0‴', 'hour': 0, 'minute': 80986, ...}
bft.halving(920_986)            # {'epoch': 4, 'subsidy_btc': 3.125, 'blocks_to_next_halving': 129014}
bft.countdown(920_986)          # {'to_halving': 129014, 'to_last_satoshi': 6009014, ...}

print("\n".join(bft.format_clock(920_986)))
# Bitcoin Time Clock — block 920,986
#   Calendar (BFT):   AB 17 · M08 · D12
#   Ordinal degree:   0°80986′1690″0‴   (hour°minute′second″third‴; first sat: uncommon)
#   Halving epoch:    4  ·  subsidy 3.125 BTC  ·  38.6% through
#   Cycle (hour):     0  ·  73.1% to the next conjunction
#   Counting down:    326 → retarget  ·  129,014 → halving  ·  6,009,014 → the last sat
```

### Your birthday in Bitcoin time

```python
bft.from_gregorian(1995, 6, 15, 12, 0)   # a Gregorian UTC birthday → the full clock
# {'height': -712982, 'before_bitcoin': True, 'estimate': True, 'calendar': {...}}
bft.format_date(bft.height_at(1995, 6, 15))   # 'BB 13 · M08 · D24'  — before genesis, inverted
bft.format_date(bft.height_at(2015, 7, 20))   # 'AB 6 · M08 · D09'
```

Born before 2009-01-03? Your height is **negative** and the clock runs in reverse — *Before
Bitcoin*. Born after? You get an AB date and your place on the ordinal clock. It's an **estimate**
(see honesty notes) — the model dates you at a steady 10-minute block.

## The three readings

### 1. The calendar

- **Epoch:** the genesis block (height 0, 2009-01-03) starts the clock. Heights ≥ 0 are **After
  Bitcoin (AB)**; negatives are **Before Bitcoin (BB)**, the inverse.
- **Units:** day = 144 blocks · week = 1,008 · **fortnight = 2,016 (one difficulty period)** ·
  **month = 4,032 (two difficulty periods) = 28 days** · **year = 52,416 (26 periods) = 364 days**.
- **13 months of 28 days = 364 days.** No leap hacks, no intercalary day. It drifts ~1.24 days/year
  against the sun — **on purpose**. It tracks the chain's heartbeat, not the earth's orbit.
- **Month names aren't baked in.** Pass `format_date(h, month_names=[...13...])` for your own;
  otherwise it renders `M01..M13`.

### 2. The ordinal clock (hour · minute · second · third)

Bitcoin's degree notation `A°B′C″D‴`, straight from ordinal theory — the clock it always had:

| Position | Name | Is | Ticks every |
|---|---|---|---|
| `A°` | **hour** | cycle number | 1,260,000 blocks (~24 years) |
| `B′` | **minute** | block index in the halving epoch | 210,000 blocks (~4 years) |
| `C″` | **second** | block index in the difficulty period | 2,016 blocks (~2 weeks) |
| `D‴` | **third** | sat index in the block | each sat |

### 3. The countdowns (the inverse)

There are **no negative block heights on-chain** — the chain starts at genesis. So "counting
backward" in Bitcoin means the *remaining-block countdowns*: `countdown(h)` gives blocks to the
next retarget, the next halving, the next cycle, and the last satoshi. The forward count (height,
sats rising toward 2.1 quadrillion) and the down count (subsidy shrinking toward zero, the 21M cap
approaching) are mirror images of one schedule. Negative *inputs* are the conceptual inverse:
`from_height(-h)` renders the **BB** epoch.

## This is how ordinals and runes already work

The calendar and ordinal theory are **the same skeleton**, because both are built from Bitcoin's
only native clock intervals — and each interval's first satoshi is exactly an ordinal rarity:

| Interval | Blocks | Degree | BFT unit | First-sat rarity |
|---|---|---|---|---|
| block | 1 | third ‴ | the tick | uncommon |
| difficulty period | 2,016 | second ″ | 1 fortnight | rare |
| halving epoch | 210,000 | minute ′ | ~4 years | epic |
| cycle | 1,260,000 | hour ° | ~24 years | legendary |
| genesis | — | `0°0′0″0‴` | AB 0·M01·D01 | mythic |

A BFT **month is exactly two difficulty adjustments**, so the calendar's page turns on the very
events that mint rare and epic sats. **Runes** ride the same clock — a rune ID is literally
`block:tx`, and open-mint terms are block-height windows. If you're numbering sats or etching runes,
you're already telling Bitcoin time; this library reads it back to you.

## The sky comes free (`bft.sky`)

A 28-day month is one whole trip of the moon, so the moon rides the calendar for nothing — and
because every month begins on a new moon, every BFT new year is a new-moon new year. Each year also
carries one of **thirteen** animal signs: the traditional twelve, plus the **Astronomical Cat** as
the thirteenth (the sign left out of the Great Race).

```python
import bft
bft.moon_phase(920_000)          # {'emoji': '🌒', 'name': 'Waxing Crescent', ...}
bft.year_animal(920_000)         # {'emoji': '🐍', 'name': 'Snake', ...}
bft.format_date(858_000, style="date")   # 'a₿ 0016.05.23'  — the ₿-marked bitcoin date
```

Signs and moons are for wonder, not finance — the same house rule as the rest of BFT.

## Little guides

The [`guides/`](guides/) folder has short, illustrated, ELI5 walkthroughs — written so a sharp
five-year-old can follow and a grown-up still learns something: the block clock, the thirteen months
and the moon, the two calendars side by side, and a kid-safe lesson on never sharing your keys.

## The long view — "the longer-living time"

A quiet idea this project is built around: Bitcoin rewards patience, and measuring your life in
blocks nudges you toward a longer view. Ten minutes is a long time to a day-trader and no time at
all to a forest. As we learn to think in halvings and cycles — and as we look out for our frens
across long horizons instead of the next candle — a **block can become the new second**: the shared,
unhurried heartbeat of people who plan in decades. That's the "longer-living time." It's a
philosophy, not a physics claim — but it's why the clock's fastest visible hand still takes two weeks
to come around. Slow is the feature.

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

## Prior art & credit

- **Ordinal theory** and degree notation: Casey Rodarmor, the
  [Ordinal Theory Handbook](https://docs.ordinals.com/overview.html). The hour/minute/second/third
  clock reading is theirs; this library surfaces it beside a calendar.
- Block-time calculators and hardware **block clocks** exist. What didn't, as far as we found, is a
  small **library + spec** unifying a block-native 13-month calendar, the ordinal degree clock, the
  halving/countdown math, and a Gregorian bridge — so here it is, for anyone to use.

## License

MIT. Built by the Pac's Arcade non-profit — *nobody should have to trust; everybody should get to
verify.* Contributions welcome.
