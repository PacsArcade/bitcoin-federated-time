# The Two Moons — why the clock's moon doesn't match the calendar's day

*Explainer · written after a real question from the Admiral (0018.04.26 a₿): "it's day 26
of the bitcoin month, but the clock shows a nearly-full moon — shouldn't we be two days
from new?" The confusion is honest, the clock is honest, and the answer is worth a page.*

## The moment that raised the question

On `0018.04.26 a₿` — two block-days before the month ends — the round clock on
pacsarcade.org showed a fat waxing gibbous, ~64% lit, heading toward FULL. If months
began on new moons, day 26 should show a thin dying crescent. It didn't. Nothing is
broken: **the clock's face wears the SKY'S moon, and the sky's moon owes the bitcoin
calendar nothing** — yet.

## There are two moons, and both are honest because we label them

| | **The sky's moon** | **The calendar's moon** |
|---|---|---|
| what it is | the real one over your head | a drawn, block-timed lunation |
| its month | ~29.53 solar days (synodic) | exactly 28 block-days (4,032 blocks) |
| new moon falls | wherever astronomy puts it | **D01, every month, forever** |
| full moon falls | wherever astronomy puts it | **D15, every month, forever** |
| who keeps it | the universe | the block math (`bft.moon_phase`) |
| where you see it | **the round clock badges** (tooltip says "the sky's moon"), and the actual sky | the library, the study's calendar surfaces |

They are different clocks. The sky's month is a day and a half longer than the
calendar's, so the sky slips ~1.5 days later against the calendar **every bitcoin
month** — the same proud drift as the 364-day year against the sun. No fixed 28-day
month can hold the sky's hand; it can only wave as the sky laps past, and the two
readings realign roughly every **19–20 bitcoin months** — a slow beat, like two
metronomes drifting in and out of phase.

## Why the badge wears the sky's moon *today*

Because today — before Day 0 — **the calendar's moon hasn't been born yet.** The current
count is genesis-anchored, and genesis (3 Jan 2009) fell on a first-quarter sky moon:
the old count and the moon were never introduced. Until the handshake, the only honest
moon a clock can wear is the real one. So the badge computes the actual sky (mean
synodic month from the known new moon of 2000-01-06 18:14 UTC), names it in the
tooltip, and lets you verify it by stepping outside. Wonder, not fiction.

## The handshake — Day 0 is *appointed to a real new moon*

This is the part the question was really asking about. Per the
[Day 0 decision paper](degen-hours.md) *(proposal — awaiting Pac's key-signed
sign-off)*:

> **Day 0 = block 983,664** — the first bitcoin-midnight whose moon face reads 🌑 New,
> appointed to the real new moon of **~7 Jan 2027 20:24 UTC**, four days after bitcoin
> turns 18 on the sun's calendar. The 720 blocks between the anniversary midnight and
> Day 0 are the **Degen Hours**.

So: **yes — the countdown ends on a new moon, on purpose.** That night the two moons
shake hands: the sky is genuinely dark, and the calendar's moon is born new. From that
block forward, every bitcoin month **begins on the calendar's new moon and centers on
the calendar's full moon, by construction** — D01 🌑, D15 🌕, D28 🌑, every month, no
exceptions, forever — and every bitcoin new year is a new-moon new year, the way the
old lunisolar calendars always wanted and could never quite keep.

The sky then resumes its slow lap: ~1.5 days of slip per month, ~9.6 days of phase per
bitcoin year, agreeing with the calendar again on the ~19–20-month beat. The calendar's
moon never pretends to be the sky's; the sky's never pretends to be the calendar's.
Label both, and both stay true.

*(One decision still open in the paper: 983,664 lands on `D28` of month 10 — the
calendar's own All Hallows' Eve, echoing the whitepaper's Halloween — with the next
midnight, 983,808, opening `M11·D01`. Whether Day 0 is the hallows' eve or the
month-start morning after is Pac's to bless — see the decision table in
[degen-hours.md](degen-hours.md).)*

## Which moon should clocks wear *after* Day 0?

An open design ruling, recorded here so it isn't lost:

- **Option S — keep the sky.** Badges keep showing the real moon (astronomy forever;
  the calendar's moon lives on calendar surfaces). Most honest to the window; the
  clock face and the month-day will visibly drift apart again, which is itself a
  lesson.
- **Option C — switch to the calendar's moon at Day 0.** From the handshake onward the
  badge moon reads new on D01 and full on D15 in perfect step with the date — the
  question that prompted this page never gets asked again. The tooltip would carry the
  sky's moon so nothing is hidden.
- **Option B — both.** The big study clock wears the sky; the small badges wear the
  calendar. Two moons, two magnifications, each labeled.

## Appendix — could a bitcoin calendar *truly* follow the sky?

Asked and answered honestly: the math can be made to work, at a price.

**A. The classic lunisolar way (29/30 alternation).** Let months alternate 29 and 30
block-days (4,176 / 4,320 blocks). The mean month is 29.5 block-days against the sky's
29.5306 — a slip of only ~0.031 day/month, needing one leap block-day roughly every 33
months (the Metonic trick, chain-flavored). Deterministic, height-only, every node
agrees.

**B. The chain-native way (months born at the dark moon).** Define: *a month begins at
the first bitcoin-midnight after the computed new moon.* The new-moon instant comes
from the same pure mean-synodic math the badge already runs — deterministic from
arithmetic every node shares, no oracle, no observation committee. Months come out 29
or 30 block-days long, self-correcting forever; the sky and the calendar never drift
more than a day apart.

**What both cost — and why this house declined:**

- the perfect rectangle dies: no more identical 28-day months, no 13 × 28 = 364, no
  month = exactly two difficulty adjustments;
- weeks break: 29- and 30-day months don't hold a clean 4-week grid, so "same shape
  every month" — the calendar's kindest teaching feature — is gone;
- month boundaries stop being knowable years ahead in block heights (scheme B), or
  need a leap-rule table (scheme A).

BFT chose the other inheritance: **keep the tidy month, draw the calendar's moon, and
shake the sky's hand once — at Day 0 — so the whole structure is moon-born even though
it doesn't moon-follow.** The sky stays free, the calendar stays square, and both are
labeled. If a true sky-calendar is ever wanted, scheme B is the house recommendation —
as an *overlay* (a second date line, the way lunar dates ride many wall calendars
today), never a replacement. Wonder, not finance.

---

*Live numbers behind the original question, computed 0018.04.26 a₿ (tip ~959,249): sky
moon age ~8.7 days, ~64% lit, waxing; ~6 days to full, ~21 days to new. Upcoming
month-starts drift younger by ~1.5 days each — `0018.12.01` (~Feb 2027) opens within
~half a day of a true new moon at the ~600 s/block model. All wall-clock datings wear
the `~`: the appointed heights are exact, their arrival is not.*
