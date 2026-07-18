# Changelog

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
