# The clock studies

Living, self-contained HTML studies of the Bitcoin Time Clock. Open them straight in a browser —
no build, no server, no dependencies.

## [`clock-study-pupil.html`](clock-study-pupil.html) — THE CLOCK (the pupil)

The flagship study: **two clocks, side by side, reading the same Bitcoin Federated Time.**

- **The square clock** — a retro split-flap face showing the `hh:mm` block-beat. Only **the
  struggling digit** — the minute-ones card, how full the current block is — trembles on its
  hinge as the block ages (it's the one honest guess on the face, and it wears a `~`);
  everything else is chain-exact and calm.
- **The circle clock** — an analog face that *is* a full-size 8-bit pixel moon at the current
  SKY's real phase — computed in your browser, correct lit limb, check it against your window — with the BFT hands on top and the live height + arcade LEVEL below. (The calendar's symbolic block-moon rides the birthday page, labeled as the calendar's.)
- **The thesis, in PAC-MAN** — every block, bitcoin eats the world's fiat: mempool dots ring each
  clock and **Pac laps the ring ten times per block — his lap counter IS the struggling digit.**
  Each lap's prize waits at 12 o'clock: the classic **fruit ladder** (🍒 🍓 🍊 🥨 🍎 🍈 👾 🔔 🗝️ —
  the Key ninth, because it unlocks the tenth lap), and the tenth lap's prize is the gold ₿
  itself (the only gold — gold is money, and the reward *is* money), eaten at every block-break.
- **The flip side** — tap a clock to flip it: the Day-0 countdown, split-flap style, counting
  down to the appointed block. At zero: a surprise the arcade has been saving. Be there.

It reads the live tip from mempool.space when the network allows, and falls back to an honest,
`~`-marked anchor estimate offline. **Every number on the face is translated, with formulas, in
[`docs/pupil-clock-grid.md`](../docs/pupil-clock-grid.md).** The Day-0 target and the Degen Hours
window are specified (pending sign-off) in [`docs/degen-hours.md`](../docs/degen-hours.md).

## [`bitcoin-birthday.html`](bitcoin-birthday.html) — THE BITCOIN BIRTHDAY

Enter any old-calendar birthday and read it back in bitcoin time: your ~birth block, your
`hh:mm` birth beat, your block-timed moon, your **month sign** (the 13 astronomical signs,
Ophiuchus seated), your **year animal** (the 13 animals, the Astronomical Cat welcomed home) —
plus **the returns** (what it was on the old calendar, and the next three times your bitcoin
birthday comes around, each with its ≈ old-calendar landing — it walks ~1¼ days up the old
year every year, because it's the old calendar that drifts) — and **the mirror**: the same
distance on the other side of genesis, so every birthday gets both its `a₿` and `b₿` reading,
in old time and bitcoin time.

Runs entirely in the browser. Nothing you type leaves your device — no keys, no data.

---

*Estimates wear the `~`; the chain vouches only for real heights. Signs and moons are wonder,
not finance.*
