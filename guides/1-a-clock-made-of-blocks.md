# 1. A clock made of blocks

## The tick

Every clock has a **tick**. A wall clock ticks every second. Bitcoin ticks every **~10 minutes** —
and each tick makes a **block**: a page in a book the whole world shares.

```
   ┌─────┐   ┌─────┐   ┌─────┐
   │block│──▶│block│──▶│block│──▶ …
   └─────┘   └─────┘   └─────┘
   a new page every ~10 min — and no eraser exists.
```

## The number that is the time

You don't ask Bitcoin "what o'clock is it?" You ask "**how many pages so far?**" That number is
the **block height**. Right now it's around **958,000**. Tomorrow it's a little bigger. It only ever
goes **up**, and no king, bank, or wizard can turn it back.

> A wall clock can be set wrong. This clock cannot. That is the whole point.

## Reading the clock face

The face reads **hh:mm**, just like the clock you already know — but every digit is a little
container made of the containers below it:

```
        0 4 : 2 7
        │ │   │ └─ how FULL this block is: 0=empty … 9=nearly full · the honest ~guess
        │ │   └─── which block of this hour (0–5) — each block worth ten minutes
        └─┴─────── the block-hour (00–23) — six blocks each
```

A BFT **day is 144 blocks**: 24 block-hours of 6 blocks each. So `04:27` says, exactly: *hour 4,
block 2 of that hour, and the current block is about 7/10 full.* The last digit is a glass of
water slowly filling — the only guess on the whole face (the chain hasn't written that page yet,
so it wears a `~`). When the block breaks: **snap** — the glass empties to 0 and the tens clicks
up one block.

Read it back UP the ladder and you've explained time itself: blocks fill by tenths → ten filled
tenths make a block → six blocks make an hour → 144 make a day → 28 days make a moon → 13 moons
make a year, and the year is just bitcoin's age. Every big thing is made of the small thing
below it. That's all a clock has ever been.

No seconds. The fastest hand on this clock takes ten minutes — on purpose. This is a clock for
people who think in years. (More on *why slow is good* in guide 3.)

## For the sat collectors (a sidebar)

People who collect satoshis have their own notation for a block — it looks like this: `0°118346′746″`.
Those little marks are **ordinal degrees**, and their handbook calls the positions hour, minute, and
second — but they're really **indices** (which ~24-year cycle, which block since the halving, which
block of the two-week retune), not a clock face. Fun lore, worth knowing — the everyday time is the
`hh:mm` above.

## Try it

```python
import bft
bft.block_beat(958_346)["hhmm"]   # '04:20'
bft.format_date(958_346)          # '0018.04.20 a₿'
print("\n".join(bft.format_clock(958_346)))
```

**Next:** [the thirteen months and the moon →](2-the-months-and-the-moon.md)
