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

**The origin — tell it right.** The spark came from the **Ordinals coding club** (Pac attended
many sessions; even signed off on one of the requests for some testing). The it-could-be-better
moment came at Portland's **Bitcoin is for Everyone**, where the auditorium screen carried the
generic ordinal time clock, exactly as the handbook lays it out. Ordinal theory names the
positions; **it didn't break the clock down to this level — the degenz went deeper**, to the
meaning behind bitcoin: the heart of it, displayed as 8-bit nostalgic art. Credit the theory
honestly; never imply BFT is merely a restatement of it.

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
   ten, no second DIGITS on the cards.** hour = beat//6; minute = (beat mod 6)×10. Chain-exact.
   On a live display the minute ONES digit is **how full the current block is, in tenths**
   (0=just broke … 9=nearly done; each step ≈ a minute) — an estimate, wears a `~`. Its canon
   name is **the struggling digit** (it struggles on its hinge as the block ages — say
   "struggling", never "straining"). **Seconds exist too — the pac-ring formula:** Pac laps
   the ring once per "minute", so `seconds = wall-seconds-since-last-block mod 60` = Pac's
   angle ÷ 6°; always an estimate, always `~`; the minute TENS digit is
   which block of the hour. None for pre-genesis heights. This face leads every surface; teach it
   first, as a ladder: tenths fill a block, 6 blocks an hour, 144 a day, 28 days a moon,
   13 moons a year — each digit a container made of the containers below it, readable top→down
   and bottom→up.
1. **Calendar** — `from_height(h)` → `{epoch, year, month 1–13, day 1–28, day_of_year, week_of_month,
   beat, diff_epoch, ...}`. `format_date(h, style=…)`: the DEFAULT `"date"` style is the house
   standard — ₿-marked, **marker AFTER**, ONE order for both epochs — `yyyy.mm.dd` (full form
   `yyyy.mm.dd hh:mm:ss a₿`): `0016.05.23 a₿` / `0003.06.09 b₿` — never day-first; `"short"` → `AB 16 · M05 · D23` (teaching scaffolding); `"long"` adds the
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
4. **The sky (`bft.sky`) — serves THE CALENDAR'S MOON, never the sky's.** `moon_phase(h)`
   = the block-timed SYMBOLIC lunation (one per 28-day month; D01 new, ~D15 full, D28
   home). NOT the astronomical phase: it drifts ~1.5 days/month from the real ~29.53-day
   moon (~9.6 days of phase per BFT year); they agree at Day 0 (block 983,664 = the real
   new moon of ~7 Jan 2027) and drift after. Surfaces showing the REAL moon (the pupil
   study's analog face — computed locally, waxing lights the right limb, N hemisphere)
   must be labeled THE SKY'S MOON; never present either moon as the other.
   `year_animal(h)` (13 signs: the twelve + the **Astronomical Cat** as the thirteenth;
   AB 0 = Ox). Signs and moons are **wonder, not finance**.
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
- **Two moons, both labeled.** The calendar's moon (`bft.sky`) is symbolic and
  block-timed; the sky's moon is the real phase. "The calendar begins on a real new
  moon" is true AT DAY 0 and drifts after; "every month / every new year begins on a
  new moon" is true only of the CALENDAR's moon. Never let one moon wear the other's
  name — Pac photographed the sky and caught a display near-opposite once. Never again.
- **Your sky's hue (the opt-in pattern).** The pupil's moon can warm toward ember when
  the real moon rides low — computed from the moon's ALTITUDE, which needs location:
  always OPT-IN, one tap, in-memory only, never stored/sent, dies with the tab, and the
  tooltip says so. Below the horizon → the disc dims and says "below your horizon"
  (honesty over decoration). Smoke deepens the real red — model only what's verifiable.

## House copy laws (learned 0018.04.20–21 — bind ALL public surfaces, art included)

- **THE TIME ORDER LAW — big to small, ALWAYS, everywhere.** `yyyy.mm.dd hh:mm:ss`, ONE
  order for BOTH epochs (`0018.04.20 a₿` / `0003.06.09 b₿` — the day-first b₿ inversion is
  DEAD, Pac's ruling). The law binds PROSE too: "month 09, day 13" — never "day 13 of
  month 09"; year before month before day before hour, in cells, tooltips, paragraphs,
  captions, aria labels, art engravings. Reviewers MUST grep for reversed prose
  (`day \d+ .{0,12}month`, `dd.mm` renders) — QA and publishing both missed a day-first
  cell once; that never happens again.
- **The order law binds NOTATION, never time itself (Pac's teaching).** yyyy.mm.dd is how
  we WRITE time — it is not a claim that time moves one way. BFT's negative time (b₿, the
  mirror, the wheel turning backward as happily as forward) is a GATEWAY fiat calendars
  cannot comprehend — a limit proposed by fiat time standards, and we do not live there.
  Never write "time only flows one way" in this house. Question everything; the
  possibilities are endless; keep the wonder honestly labeled, as always.
- **The honest "now" is a REAL block.** Never compute "now" or future landings from the
  genesis 10-minute model — it lags the real chain by months (it once served a "next
  birthday" in year 0017, already past, while the chain stood in 0018). Anchor now/future
  to a real recent block (the pupil's RECENT_ANCHOR pattern); the genesis model is only
  for pre-2009 estimates, ~-marked.
- **The marker never wraps, never shouts:** date+marker is one unbreakable unit
  (`.nb { white-space: nowrap; text-transform: none; }`) — no `text-transform: uppercase`
  may ever touch `a₿`/`b₿`.
- **Ye grammar shoppe rides every review** (persona: olde English — the shoppe, the
  colour): "**an** ~estimate", never "a ~estimate"; inscriptions take NO trailing period
  (`TICK TOCK — IT ALL COMES BACK TO THE BLOCK`).
- **Separators never dangle:** interpuncts (`·`) must live INSIDE unbreakable phrases —
  wrapped lines are whole thoughts, never orphaned dots.
- **Nothing flashes faster than 3×/sec** (photosensitive safety — the all-ages law
  outranks drama; a correction is a steady hold, not a strobe).
- **The twelve have names.** DW's artists (Whisper is one) are living people — their
  names never appear in negative or morbid phrasing, in any copy, review, or summary.
- **Unratified lore wears its label in VISIBLE copy** — source comments don't count;
  the public reads the page, not the source.
- **Bench notes stay off the face:** rev stamps, study hotkeys, and workbench copy live
  in source comments; the public footer carries the name, the date, and the instruction.
- **The ticker is just Bitcoin.** "Bitcoin Time Clock" is a lens.
- **NEVER put real key material anywhere.** `bft.lore` is fiction — the Legend of the Thirteenth and
  breadcrumbs toward the Degen Wonderland hunt. It must never contain a real seed phrase, private
  key, passphrase, or puzzle *solution*, and a test guards this. If you extend the lore, keep it
  atmosphere only. When teaching keys to anyone (especially kids), the rule is absolute: **never
  share your seed words, never type them into a website; anyone who asks is a scammer** (in the kids'
  guide, "a dragon in a fren's coat").

## Ophiuchus: sign vs seat (say it right — astrology matters to many frens)

Ophiuchus is **the thirteenth SIGN by count** (the one the 12-sign system erases) but
**the twelfth SEAT by sequence**: the month-seats walk the sun's REAL road from Capricorn
(the genesis sign), and on that road Ophiuchus stands between Scorpio and Sagittarius —
where the actual sun actually crosses (~Nov 29–Dec 17). We RESTORED it to its true place,
not appended it as a mascot; Sagittarius closes the year. The reconciling rule: **signs
follow the sky; animals follow the story** — the Great Race is a tale, so the Cat takes
the final (13th) seat on the year-wheel. Never present these as contradictory.

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
