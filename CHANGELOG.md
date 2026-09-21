# Changelog

## Unreleased — the one-moon correction (task-359, Lane A)

*Corrected `0018.07.02 a₿`, block 967,918 — the Admiral's ruling: "we only have one moon.
and we can see it outside." The 28-day BFT month is a block count and never wears the
moon's name; the moon is the sky's, computed from wall time against the real ~29.53-day
synodic lunation, labeled.*

- **`bft/sky.py`'s module docstring was self-contradictory** — it claimed "TWO moons" and a
  block-timed "calendar's moon" tied to day-of-month (D01 = new, D15 = full), while its own
  `moon_phase()` already computed the sky's real synodic phase (ruling 0018.05.18).
  Rewrote the docstring; `moon_phase()`'s logic is untouched.
- **`bft.holidays`** — "New Year (the new-moon new year)" is now just "New Year" (the year
  turns over on a block count, never a moon); "Year's End"'s story no longer claims the
  year "completes with the moon."
- **`bft.lore`** — one whisper line asserted the retired doctrine as flavor text; reworded,
  no change to the deterministic height-based selection.
- **Tests, docs, guides, and this package's own bundled study index/readme** corrected to
  match — no surface asserts a BFT month or new year is tied to a moon phase.
- **Finding 1 (block-years, not age):** the display year counts bitcoin's block-years, not
  "how old bitcoin is" or "bitcoin's age" — corrected in `README.md`, `docs/pupil-clock-grid.md`,
  and `docs/the-thirteen-seats.md`, both corrected. The 364-vs-365.24 solar drift is now stated with its two parts (the designed ~1.24 days/year, and the separately-measured faster-than-600s block average) instead of one flattened number.
- `docs/the-two-moons.md` kept as history (past-tense framing banner; body unchanged).
  `docs/degen-hours.md` banner-marked as a superseded proposal (it was never signed off).
- **NEW:** `scripts/lint-one-moon.sh` and `scripts/lint-finding1.sh` — fleet-reusable greps,
  each taking a path argument, for lanes B–E to run as their own exit check.
- **Not in this lane** (see `work-claims/task-359.md`): the two in-flight studies
  (`studies/bitcoin-birthday.html`, `studies/clock-study-pupil.html`), `docs/keep-time-simple.md`,
  this repo's bundled `.claude/skills/bitcoin-time-clock/SKILL.md` (Lane B's), and the
  generated `build/lib/` + `egg-info/PKG-INFO` (no Python build toolchain available; neither
  regenerated nor hand-edited).

## 0.3.0 — the house clock canon

*Published `0018.04.20 a₿` — during block ~958,336, `02:40` on the face — signed by Pac's
key and shipped on the 420 day itself. Happy 420. 🍒🗝️₿*

- **`block_beat()`** — the canonical `hh:mm` block-beat face (6 blocks an hour, ten minutes a
  block; no second digits — the seconds read off the Pac ring, `block-age mod 60`, always `~`)
  now leads every surface; the ordinal degree notation stays as an honestly-labeled sidebar
  for the sat collectors.
- **Marker after, everywhere:** `format_date()` defaults to the house style — `0018.04.20 a₿`,
  pre-genesis the same order, `0025.09.13 b₿`.
- **`bft.holidays`** — the chain's feast days: the storied table (genesis → the fifth
  halving), the recurring calendar (New Year, the Hallows, Sol's Seat, Year's End, whisper
  days, Halving Day, the Conjunction, Cat years), `holidays_at` / `next_holidays` /
  `year_calendar`.
- **`python -m bft`** — the whole clock in a terminal: a height, an old-calendar date, or
  ~now; prints today's feast days and what's coming up.
- **Studies aboard:** `studies/clock-study-pupil.html` (the flagship two-clock study — ten
  Pac-laps per block, the fruit ladder, the Day-0 countdown) and
  `studies/bitcoin-birthday.html` (birthdays in bitcoin time: signs old & new, the mirror,
  the returns).
- **Docs:** `docs/pupil-clock-grid.md` (every number on the clock, translated),
  `docs/degen-hours.md` (the Day-0 window, proposal), `docs/bitcoin-holidays.md`.
- **Two readmes:** the plain telling and the Hatter's (`README-DW.md`).
- **Fixes:** the cycle line said "% to the next conjunction" for a % *through* value; the test
  demo crashed on legacy Windows consoles; guides taught the degree notation as "the clock
  face" (it never was).

## 0.2.0

- Initial package: the 13×28 block calendar, ordinal degree notation, halving/cycle math,
  countdowns, the Gregorian bridge, `bft.sky` (block-timed moon + the 13 animals),
  `bft.lore` (the thirteens; no key material, ever), guides, tests.
