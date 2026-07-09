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
the **block height**. Right now it's around **920,000**. Tomorrow it's a little bigger. It only ever
goes **up**, and no king, bank, or wizard can turn it back.

> A wall clock can be set wrong. This clock cannot. That is the whole point.

## Reading the clock face

Here's a neat secret people who collect satoshis already know: you can slice the block number into
**hour, minute, second** — a real clock face — like this:

```
   0° 80000′ 704″
   │    │    └─ second: a block in the last 2 weeks
   │    └────── minute: a block since the halving
   └─────────── hour:   which ~24-year cycle
```

The fast hand ("second") comes all the way around every **two weeks**. Slow is on purpose. This is
a clock for people who think in years, not seconds. (More on *why slow is good* in guide 4.)

## Try it

```python
import bft
bft.format_date(920000)       # 'AB 17 · M08 · D05'
print("\n".join(bft.format_clock(920000)))
```

**Next:** [the thirteen months and the moon →](2-the-months-and-the-moon.md)
