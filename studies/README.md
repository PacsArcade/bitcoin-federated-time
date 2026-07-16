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
  block-timed phase, with the BFT hands on top and the difficulty LEVEL below.
- **The thesis, in PAC-MAN** — every block, bitcoin eats the world's fiat: mempool dots ring each
  clock, Pac laps the ring as the block ages, and the gold reward coin at 12 o'clock (the only
  gold — gold is money, and the reward *is* money) gets eaten at every block-break.
- **The flip side** — tap a clock to flip it: the Day-0 countdown, split-flap style, counting
  down to the appointed block. At zero: balloons, and THANK YOU, SATOSHI.

It reads the live tip from mempool.space when the network allows, and falls back to an honest,
`~`-marked anchor estimate offline. **Every number on the face is translated, with formulas, in
[`docs/pupil-clock-grid.md`](../docs/pupil-clock-grid.md).** The Day-0 target and the Degen Hours
window are specified (pending sign-off) in [`docs/degen-hours.md`](../docs/degen-hours.md).

## [`bitcoin-birthday.html`](bitcoin-birthday.html) — THE BITCOIN BIRTHDAY

Enter any old-calendar birthday and read it back in bitcoin time: your ~birth block, your
`hh:mm` birth beat, your block-timed moon, your **month sign** (the 13 astronomical signs,
Ophiuchus seated), your **year animal** (the 13 animals, the Astronomical Cat welcomed home) —
and **the mirror**: the same distance on the other side of genesis, so every birthday gets both
its `a₿` and `b₿` reading, in old time and bitcoin time.

Runs entirely in the browser. Nothing you type leaves your device — no keys, no data.

---

*Estimates wear the `~`; the chain vouches only for real heights. Signs and moons are wonder,
not finance.*
