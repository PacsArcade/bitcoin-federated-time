# 2. The thirteen months and the moon

## Every month is the same shape

The calendar on your wall is **messy**: 12 months, all different sizes. September has 30 days, July
has 31, and poor February gets 28 (or 29 when it feels like it). Nobody can remember which is which.

Bitcoin time is **tidy**. Every month is the **exact same shape** — 4 weeks, 28 days, a perfect
little rectangle:

```
   ┌──────────────────────┐
   │  1  2  3  4  5  6  7 │
   │  8  9 10 11 12 13 14 │
   │ 15 16 17 18 19 20 21 │
   │ 22 23 24 25 26 27 28 │
   └──────────────────────┘
     4 weeks · 28 days · no messy 30s or 31s
```

Now stack **thirteen** of those identical months. Thirteen × 28 = **364 days** — one day short of a
sun-year, and it slowly drifts away from the sun a day or so each year. **That's allowed.** Bitcoin
keeps time by *its own heartbeat*, not by the sky. (Fun fact: one month = exactly **two** of
Bitcoin's "difficulty adjustments" — the calendar page turns on the same beat the network re-tunes
itself.)

### Wait — thirteen months?

Yes! One more than you're used to. For now the library just numbers them **M01 to M13** — the
*names* are still waiting to be chosen. The old 13-month calendar that inspired this one *did* name
them, though: it kept the twelve you know and slipped a brand-new month, called **Sol**, in right
after June —

```
   … May · June · [ Sol ] · July · August …
                    ▲ the new one
```

— so its year had a thirteenth month tucked in the middle. That's where our extra month comes from.

## The moon comes free

Here's the loveliest part. A **28-day month is almost exactly one trip of the moon** —
the real moon takes about a day and a half longer. So this calendar keeps **its own
moon**: the same picture, every month, and nobody has to wind it:

```
   D01   🌑  new moon      · the month begins
   D08   🌓  first quarter
   D15   🌕  FULL moon     · the middle of the month
   D22   🌗  last quarter
   D28   🌑  new again     · the month ends
```

That means there are **two moons**, and both are telling the truth. The **sky's moon**
is the real one over your head — go outside any night and check it. The **calendar's
moon** is this one — a drawing that keeps perfect calendar time and slowly drifts away
from the sky, about a day and a half each month. They shook hands once, on Day 0: the
whole calendar *begins* on a real new moon. After that, the drawing keeps its own beat.
*(Grown-up version of this story, with the drift math and the Day-0 appointment:
[the two moons](../docs/the-two-moons.md).)*

Because every month *starts* on the calendar's new moon, **every new year starts on a
new moon too — the calendar's** — just like the old Asian calendars, falling right out
of the block math with nothing bolted on.

## And every year has an animal — even the one who was left out

Each year gets an animal sign. Most people know **twelve**: Rat, Ox, Tiger, Rabbit, Dragon, Snake,
Horse, Goat, Monkey, Rooster, Dog, Pig. But do you know *why* there are only twelve — and why
there's no Cat? Here's the story. 🐈

> **The Great Race.** Long ago — so the story goes — the Jade Emperor, the emperor of the whole
> sky, called every animal to a **race across a wide, cold river**. "The first twelve to reach the
> far bank," he said, "will each have a year named after them. Forever."
>
> The **Cat** and the **Rat** were best frens, and both were small — far too small to swim such a
> river. So they made a plan together: they would cross on the back of the kind, strong **Ox**, who
> didn't see well and didn't mind carrying passengers.
>
> Halfway across, the Rat did the thing the Cat never forgot: it **pushed its fren into the
> water** and rode on alone. And just as the Ox waded up the far bank in first place, the Rat
> leapt over its nose and landed on the shore **first of all**. That is why the Rat's year comes
> first, and the patient Ox's comes second.
>
> The Cat pulled itself out of the river, soaked and shivering, long after the twelfth place was
> taken. There was no year for the Cat. And that — the story says — is why there is **no Cat among
> the twelve**, why cats have never forgiven rats, and why every cat you've ever met hates
> getting wet.

*(Families tell it a little differently across Asia — and in Vietnam's calendar the Cat **did**
get a year, where the Rabbit's would be. The Cat was never left out everywhere.)*

In *this* clock — the one with a thirteenth of everything — we finally do the kind thing. We save
the Cat a seat. The **13th year is the Astronomical Cat**: the fren who was left out, welcomed
home at last.

```python
import bft
bft.moon_phase(920000)     # 🌒 Waxing Crescent
bft.year_animal(920000)    # 🐍 Snake
```

The moon and the animals here are for **wonder, not money** — and if you want *tonight's*
real moon, the sky shows it for free — no clock tells you what a coin will be worth. But
keep an eye on that thirteenth. It keeps coming up… →

**Next:** [the two calendars →](3-the-two-calendars.md)
