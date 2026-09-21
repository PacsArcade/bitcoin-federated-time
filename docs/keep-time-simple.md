# Keep time simple — the one way this house shows a block as a clock

Written 0018.06.24 a₿ (block 966,979) by Number One, on the Admiral's order from the Arcade Relaunch review:
*"in the repo we shouldn't be reimagining how to express time over and over again … make sure we send any info back
to the bft repo on how to keep things simple."* This note is the memory. Read it before drawing any clock, tile,
infographic or sentence that shows Bitcoin time.

## The face (already built — reuse it)

- **Canonical math:** `bft.block_beat(height)` in this repo. `beat = height mod 144` · `hour = beat // 6` ·
  `minute tens = beat mod 6` (×10). Chain-exact; two nodes at one height show one face.
- **The live digits:** minute **ones** = tenths of the way through the current block (`block age ÷ 600 s`, ×10);
  **seconds** = seconds since the last block, mod 60 (one Pac lap per minute; his angle ÷ 6° is the seconds hand).
  Both are honest `~` estimates and are drawn as such (the ones digit trembles; the ring carries the `~`).
- **The picture:** THE LIVING CLOCK = `studies/clock-study-pupil.html`, ported whole as
  `pacsarcade-org/src/components/time/living-clock-engine.ts` (+ `LivingClock.tsx`, the `StripClock` for headers,
  `MoonClock` for the round badge). No new drawing of the face. A page that needs a clock **mounts one of these**.
- **Dash law:** a real value or a dash-face (`--:--`, `----.--.--`). Estimates ride on a real anchor or not at all.

## How to explain it in one breath (the words, so we stop rewriting them)

1. **1 block ≈ 10 minutes.**
2. **6 blocks an hour, 144 a day** — a 24-hour face you already know how to read.
3. **hh** is the block-hour; **mm** tens is which of the hour's six blocks; the **ones** digit is how far through this
   block we are (~); **seconds** are the time since the last block, mod 60 (~).
4. **28 days a month, 13 months a year** (4,032 / 52,416 blocks). Year 0 began at genesis.
5. The **beat** (block-of-the-day, 0–143) is the engine's own word for "where we are in the day". Show it under the
   day, never above the face; a first-time reader needs hh:mm, not the beat.

## What NOT to do (scar tissue, 0018.06.24)

- Don't build a "block → beat → day → month" ladder as the front-page picture: it explained the beat before the face
  and dropped the ones column and the seconds. The Admiral: "the clock goes more than the 10 min increments … you're
  missing the 1's column … we need to show time simply."
- Don't paraphrase the math per page. Link the paper (pacsarcade.github.io/bitcoin-federated-time) and the guides
  (`guides/1-a-clock-made-of-blocks.md`).
- Don't stamp a date without a real tip height (`skills/bft`).
