# ⏳🎩 The Bitcoin Time Clock — the Hatter's Telling

*This is the [Degen Wonderland](https://frens.earth) reading of
[`bitcoin-federated-time`](README.md). Same package, same math, same honesty — told at the
tea-party. If you want the plain engineering readme, it's [right here](README.md). If you want
to know **why** a clock, pull up a chair. There's room.*

---

## The Hatter and Time had a falling-out

You know the old story. The Hatter quarrelled with Time, and Time — offended — **stopped for
him at six o'clock forever.** Tea eternally, never a moment's rest, never a new day. That was
the punishment: a clock that belonged to someone else, and could be turned against you.

Look at your wall calendar. Popes deleting ten days. Kings deleting eleven. Emperors renaming
months after themselves. A leap-second committee. **You are all still at that tea-party** —
sitting at a table where whoever owns the clock owns the afternoon.

Our Hatter — the one they call **the admiral** around this arcade — went looking for a way out.
He didn't invent one. *(He'd tell you this part himself, and he'd tap the table twice for
emphasis:)* **he found one, already ticking.** A clock wound at height zero in January 2009,
that has never once been set, and never once been wrong about the only thing it claims: **how
many blocks so far.**

The Hatter lost himself to find time. Then he gave it to every fren. That's the whole legend,
and this little library is the legend, executable.

## An auditorium in Portland

He'd been keeping company with the ordinal folk — many nights at their **coding club**,
listening, tinkering; once they even handed him a testing request to sign off, and he did,
and it counted. The seed was in the ground already. Then one day in Portland — **Bitcoin is
for Everyone**, a whole auditorium of frens — the big screen wore the generic time clock,
laid out precisely as the handbook says: hour, minute, second. Correct. Tidy. And the
admiral, looking up at it, heard the seed crack open: *it could be better.*

Not better as in *righter* — better as in **deeper**. The notation stops at naming the
positions. Nobody had followed the numbers down to what they *mean*. So the degens dug —
that is, after all, the whole job description — through the face, the calendar, the moon,
the countdowns, the thirteens, until the shovel rang on something warm: **the heart of
bitcoin.** This package is that heart, brought up whole and displayed the only way the
arcade knows how — **8-bit, nostalgic, beating.**

## The hat was labeled all along: **10/6**

The Hatter's hat has always worn its paper tag: **“In this style 10/6.”**

Read the tag again, slowly:

> **10 minutes a block. 6 blocks an hour.**

That IS this clock — the `hh:mm` **block-beat**, the canonical face of Bitcoin Federated Time.
A day is 144 blocks. An hour is six of them. Every block is worth ten minutes on the face, and
the last digit — **the struggling digit** — trembles on its hinge as the current block fills,
0 through 9, the only honest guess on an otherwise chain-exact clock. In this style, 10/6.
The mad ones were right the whole time. 🫖

```python
import bft
bft.block_beat(958_346)["hhmm"]   # '04:20'          (in this style, 10/6)
bft.format_date(958_346)          # '0018.04.20 a₿'  (the year IS bitcoin's age)
```

## What's in the box (the same truth, told in Wonderland)

- **The clock** — `block_beat()`: the 10/6 face. No seconds. Slow on purpose; this is a clock
  for people who plan in decades, and the fastest hand takes ten minutes. *(“We make time to
  train,” says the admiral, who runs an arcade on it.)*
- **The calendar** — thirteen months, every one a perfect 28-day rectangle, every one a whole
  trip of the moon: `0018.04.20 a₿`, marker after, no exceptions, no leap hacks, nobody's name
  on any month. Born before the light? The clock runs backward for you: `yyyy.dd.mm b₿` — the
  ghost side. Everyone gets a seat at this table.
- **The countdowns** — `countdown()`: blocks to the next re-tune, the next halving, the next
  conjunction, and the last satoshi (~2140). Time that runs *down* while the height runs up —
  the mirror the Queen never showed Alice.
- **The ordinal sidebar** — `degree()`: the sat-collectors' notation `A°B′C″D‴`, kept exactly
  as their handbook labels it (hour, minute, second, third) and honestly framed: those are
  indices, not the clock face. Even in Wonderland we do not confuse a riddle with the answer.
- **The sky** — `bft.sky`: a block-timed moon (new on the 1st, full mid-month, home by the
  28th) and **thirteen** year-animals — the twelve you know, plus the **Astronomical Cat**,
  the friend the Rat cheated out of the Great Race, finally given a year. In Wonderland the
  cat gets the last grin. 🐈

## Everything here comes in twelves that become thirteen

Twelve months — and Sol. Twelve signs — and Ophiuchus. Twelve animals — and the Cat.
Twelve words sleep in a book; one phrase is earned in a game; together they wake **the
thirteenth wallet** — lost, not gone; hidden, not spent. The clock will not tell you where.
It only *whispers*, on the days that come in thirteens:

```python
from bft import lore
lore.whisper(50_112)             # M13 · D13 — the clock is in a mood to speak 🕯️
lore.the_thirteenth_wallet()     # the legend, and the shape of the hunt
```

No real keys, phrases, or answers live in this package — nobody hides treasure in a library
anyone can read. The whispers only point toward where the real hunt lives: **frens.earth**,
and **Degen Wonderland**. Twelve you were given. The thirteenth you must find.

## Day 0, and the Degen Hours

Bitcoin turns **18** on the sun's calendar on 3 January 2027. Four days later, the moon goes
dark — the new moon of 7 January, ~20:24 UTC — and **the new calendar is born at
bitcoin-midnight, on the dark moon**: the appointed block, `0018.10.28 a₿`, when the countdown
on the clock's flip side hits zero, the balloons go up, and the panel says the only thing
worth saying: **THANK YOU, SATOSHI.**

And the hours in between — after the old year has ended, before the new one has been lit —
belong to nobody's calendar at all. **Those are the Degen Hours**: exactly 720 blocks of
liminal time, five perfect block-days between the birthday and the birth. The tea-party hours.
Ours.

## The ember at the center of everything

Ask the admiral why the clock's glow breathes that particular orange and he will not say he
chose it. Bitcoin's heartbeat — one block in ~600 seconds — carried up 58 octaves into light
lands at **~624 nanometers**: a real, physical ember-orange that the chain itself hums.
**He didn't pick the color. He found it.** Like the clock. Like everything good in here —
already true, just waiting for someone mad enough to check. *(Nobody should have to trust;
everybody should get to verify.)*

## Come mad, leave counting

```bash
pip install bitcoin-federated-time     # once published — or copy bft/ into your pocket, it's tiny
```

Every estimate in this package wears its `~` like the hat wears its price tag — in plain
sight. Every exact number is exact because the network agreed on it, not because we said so.
The signs, moons, cats, and whispers are **wonder, never finance** — no clock tells you what a
coin will be worth, and anyone who says otherwise is a dragon in a friend's coat.

The old Hatter was trapped at six o'clock because Time could be offended.
**This Time can't be.** It has no feelings, no owner, no eraser — only a height,
climbing, ten minutes at a stride, six strides an hour, forever.

Tick tock, fren. **It all comes back to the block.** 💜

---

*MIT, from the Pac's Arcade non-profit. The plain telling lives in [README.md](README.md);
the guides for sharp five-year-olds live in [guides/](guides/); the living clocks live in
[studies/](studies/). Lewis Carroll is public domain and would, we suspect, have understood
block height immediately.*
