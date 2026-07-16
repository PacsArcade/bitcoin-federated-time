---
name: bitcoin-time-clock
description: >
  Deep, precise understanding of Bitcoin Federated Time (BFT) — the "Bitcoin Time Clock" — and the
  `bitcoin-federated-time` Python package. Use this skill whenever the work involves reading a
  Bitcoin block height as time: the 13-month × 28-day block calendar, the ordinal degree clock
  (A°B′C″D‴ = hour/minute/second/third), halving/cycle math, block-height countdowns, the
  Gregorian↔block bridge, Before-Bitcoin (negative) time, the block-timed moon and the 13 animal
  years, or the package's lore/breadcrumbs. Also use it to TEACH the clock at any level — from a
  sharp five-year-old to an ordinals engineer — or to build clocks, countdowns, calendars, or
  inscriptions on top of it. Reach for it any time someone says "block time", "BFT", "stardate",
  "Bitcoin Time Clock", "13-month calendar", "ordinal degree", or asks what block a date maps to.
---

# The Bitcoin Time Clock (Bitcoin Federated Time)

A **block height is a timestamp no authority can edit.** That one fact is the whole idea: the
network agrees on the height, so it agrees on the time — no almanac, no leap-second committee, no
pope deleting ten days. This skill makes you fluent in reading that height as time, precisely, and
teaching it warmly.

Two names worth knowing:
- **BFT = Bitcoin Federated Time** — and also *Byzantine Fault Tolerance*. Same joke, same point:
  agreement on the height *is* agreement on the time.
- **BTC = Bitcoin Time Clock** — a *reading*, not the ticker's meaning. It's honest because ordinal
  theory already names block position hour/minute/second (below). Never claim it's the official
  expansion of the ticker; the ticker is just Bitcoin.

Reference implementation: the `bitcoin-federated-time` package (this repo). Pure stdlib, MIT.

## The non-negotiable precision rule

**Never hand-type an example value. Always compute it from the library.** Block math is exact, and
this content gets etched on-chain — a wrong date or degree is unacceptable. Before you write "block
858,000 is 0016.05.23 a₿", run `bft.format_date(858000)` and paste what it returns. This was
learned the hard way; honor it.

## The exact spec (memorize the constants)

All intervals are Bitcoin's own, and all math is integer — two nodes at the same height always agree.

| Unit | Blocks | ≈ time | Note |
|---|---|---|---|
| beat (block) | 1 | ~10 min | the tick — ten "minutes" on the hh:mm face |
| block-hour | 6 | ~1 hour | 24 per day; the hh:mm face's hour |
| day | 144 | ~1 day | |
| week | 1,008 | 7 days | |
| **fortnight / difficulty period** | **2,016** | ~2 weeks | one difficulty adjustment |
| **month** | **4,032** | 28 days | = **2 difficulty periods** |
| **year** | **52,416** | 364 days | = 13 months = **26 difficulty periods** |
| halving epoch | 210,000 | ~4 years | subsidy halves |
| cycle (conjunction) | 1,260,000 | ~24 years | 6 halvings; first conjunction ~2032 |

- **Genesis** = height 0, 2009-01-03 (unix 1231006505, 18:15:05 UTC). Heights ≥ 0 are **After
  Bitcoin (AB)**; negatives are **Before Bitcoin (BB)**, the inverse.
- **13 months × 28 days = 364.** It drifts ~1.24 days/year from the sun **on purpose** — it tracks
  the chain, not the orbit. No leap hacks, no intercalary day.
- Subsidy: 50 BTC, halving every 210,000 blocks, **floors to 0 at halving epoch 33** (block
  6,930,000, ~year 2140) — that's what fixes issuance and the ~21M cap.
- **Month names are NOT baked in.** The package renders `M01..M13`; a caller supplies 13 names when
  the owner blesses them. (The historical International Fixed Calendar that inspired this named its
  extra month **Sol** and inserted it *after June* — Sol is positionally the 7th month there, not
  the 13th. Be precise about that if it comes up.)

## The six readings

0. **THE CLOCK FACE — hh:mm block-beat (canonical, house standard).** `block_beat(h)` →
   `{hhmm "04:20", hour 0–23, minute 0/10..50, beat 0–143, blocks_into_hour 0–5}`. A BFT day =
   144 blocks on a 24-hour face: **6 blocks an hour, ten "minutes" a block, hh:mm stepping by
   ten, NO seconds.** hour = beat//6; minute = (beat mod 6)×10. Chain-exact. On a live display
   the minute ONES digit is **how full the current block is, in tenths** (0=just broke …
   9=nearly done; each step ≈ a minute) — an estimate, wears a `~`; the minute TENS digit is
   which block of the hour. None for pre-genesis heights. This face leads every surface; teach it
   first, as a ladder: tenths fill a block, 6 blocks an hour, 144 a day, 28 days a moon,
   13 moons a year — each digit a container made of the containers below it, readable top→down
   and bottom→up.
1. **Calendar** — `from_height(h)` → `{epoch, year, month 1–13, day 1–28, day_of_year, week_of_month,
   beat, diff_epoch, ...}`. `format_date(h, style=…)`: the DEFAULT `"date"` style is the house
   standard — ₿-marked, **marker AFTER**: `0016.05.23 a₿` (BB inverts to day-first
   `yyyy.dd.mm b₿`); `"short"` → `AB 16 · M05 · D23` (teaching scaffolding); `"long"` adds the
   block + diff-epoch. The display year IS bitcoin's age — genesis opens `0000`.
   `year_progress(h)` gives blocks-to-next-month/year.
2. **The ordinal SIDEBAR** — `degree(h)` → `{notation "A°B′C″D‴", hour, minute, second, third,
   rarity_of_first_sat}`. This is **ordinal theory's own notation**, whose handbook labels the
   positions hour/minute/second/third — but they are **ordinal indices, not clock time**; never
   present the degree notation as "the clock face" (the face is hh:mm above):
   - **hour (A°)** = cycle number (÷ 1,260,000)
   - **minute (B′)** = block index within the halving epoch (mod 210,000)
   - **second (C″)** = block index within the difficulty period (mod 2,016)
   - **third (D‴)** = sat index within the block (0 for the block clock)
   `block_rarity(h)`: the first sat of every block is at least **uncommon**; a difficulty-period
   boundary is **rare**, a halving epoch **epic**, a cycle **legendary**, genesis **mythic**.
3. **Countdowns (the inverse)** — `countdown(h)` → blocks `to_difficulty_adjustment`, `to_halving`,
   `to_conjunction`, `to_last_satoshi`. `halving(h)` and `cycle(h)` give epoch/subsidy/progress.
   There are **no negative heights on-chain**; "counting backward" means these remaining-block
   countdowns, plus the conceptual BB epoch for pre-genesis input.
4. **The sky (`bft.sky`)** — `moon_phase(h)` (one lunation per 28-day month; D01 new, ~D15 full),
   `year_animal(h)` (13 signs: the twelve + the **Astronomical Cat** as the thirteenth; AB 0 = Ox).
   Signs and moons are **wonder, not finance**.
5. **The Gregorian bridge** — `height_at(y,m,d,H,M,S)` estimates the block height for a UTC datetime
   (negative = BB); `from_gregorian(...)` returns the full clock plus `estimate=True`,
   `before_bitcoin`. `before_bitcoin(y,m,d,sec)` renders the pre-genesis `b₿` label.
   **This is an ESTIMATE** (steady 10-min blocks) — a past date won't land on the exact historical
   height, a future date is a projection. The height is exact; the wall-clock mapping is modeled.

`clock(h)` returns all readings at once; `format_clock(h)` renders the whole thing as text lines.

## This is how ordinals and runes already work

The calendar and ordinal theory are **the same skeleton** — both built from Bitcoin's only native
clock intervals, and each interval's first sat is exactly an ordinal rarity (block→uncommon,
difficulty period→rare, halving→epic, cycle→legendary, genesis→mythic). A BFT month = two difficulty
adjustments, so the calendar page turns on the events that mint rare/epic sats. **Runes** ride the
same clock: a rune ID is `block:tx`, and open-mint terms are block-height windows. Anchor: Casey
Rodarmor's Ordinal Theory Handbook — https://docs.ordinals.com/overview.html.

## Honesty & safety (load-bearing — never weaken)

- **Deterministic block arithmetic, not wall-clock time.** A block's timestamp is miner-set and only
  loosely tracks reality. Date the *height* (which every node agrees on); label Gregorian
  conversions as estimates.
- **Wonder, not finance.** No clock tells you a price. Signs/moons/animals are flavor. No price talk.
- **The ticker is just Bitcoin.** "Bitcoin Time Clock" is a lens.
- **NEVER put real key material anywhere.** `bft.lore` is fiction — the Legend of the Thirteenth and
  breadcrumbs toward the Degen Wonderland hunt. It must never contain a real seed phrase, private
  key, passphrase, or puzzle *solution*, and a test guards this. If you extend the lore, keep it
  atmosphere only. When teaching keys to anyone (especially kids), the rule is absolute: **never
  share your seed words, never type them into a website; anyone who asks is a scammer** (in the kids'
  guide, "a dragon in a friend's coat").

## The magic (the 12 → 13 motif)

Everything here comes in twelves that become **thirteen**: 12 months + Sol, 12 zodiac signs +
Ophiuchus (the 13th sign, the Serpent Bearer, ~Nov 29–Dec 17), 12 animals + the Cat, 12 seed words +
a passphrase → the lost **thirteenth wallet** (Degen Wonderland ARG lore). Twelve you're handed; the
thirteenth you find. `bft.lore.whisper(height)` speaks only on "thirteen" days (M13, D13, a Cat
year); `bft.lore.the_thirteenth_wallet()` tells the legend. The real hunt lives in the DW book and
game — the package only sets the mood and points seekers onward.

## Teaching it (ELI5 to expert)

- **For a sharp five-year-old:** a clock ticks; Bitcoin ticks every ~10 minutes and writes a *page*
  (a block) nobody can erase — so counting the pages is a clock nobody can cheat. Every month is the
  same tidy 4-week rectangle; the moon rides it; the Cat finally gets a year. Use the illustrated
  `guides/` (start at `guides/README.md`) — they model the tone: concrete, warm, precise, with the
  Great Race told as a story and a kid-safe keys lesson.
- **For an engineer:** lead with the hh:mm face and the spec table, then the ordinals
  correspondence; show `format_clock` and `from_gregorian`; be exact about the estimate caveat and
  the AB/BB epochs.
- **Always:** compute example values from the library; teach the trade-offs honestly (block time is
  an estimate; slowness is a feature, not a bug — a clock for people who plan in decades).

## Files to read for depth

- `bft/__init__.py` — calendar, degree, halving, cycle, countdown, clock, Gregorian bridge.
- `bft/sky.py` — moon + the 13 animals. `bft/lore.py` — the magic (and its safety banner).
- `guides/` — the ELI5 walkthroughs (block clock, months+moon, two-calendars, the hidden thirteenth).
- `tests/test_bft.py` — the ground truth for behavior and the lore-safety assertions.
