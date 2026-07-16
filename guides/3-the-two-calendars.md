# 3. The two calendars

You have two clocks now. One you were handed. One you can verify yourself. Let's put them
side by side.

|  | The old calendar *(sun & kings)* | The block clock *(Bitcoin time)* |
|---|---|---|
| **who decides?** | popes, kings, governments | nobody — the whole network agrees |
| **the months** | 12, all different sizes | 13, every one exactly 28 days |
| **the tick** | the spinning earth (wobbly) | one block, ~10 min (steady) |
| **needs fixing?** | yes — leap years, patches | no — it just counts up |
| **can it change?** | **YES. it has.** | **NO. it can't.** |

## "It has" — the scary part

The old calendar really was changed by whoever was in charge:

- In **1582**, a pope **deleted ten days**. If you went to sleep on October 4th, you woke up on
  October 15th. The days in between simply… never happened. *(True. Look it up.)*
- In **1752**, Britain deleted **eleven** more.
- Long ago, Roman emperors renamed months after **themselves** (that's why we have *July* for
  Julius and *August* for Augustus).

Nobody asked. They just changed time.

## Why the block clock can't be fooled

The block clock is only ever "how many pages so far?" — and **nobody owns an eraser**. To change
the count, you'd have to re-write every page after it, faster than the whole world writes new ones.
That's not *hard*; it's practically **impossible**, on purpose. So the number is safe, and the
clock is honest.

```
   old calendar:   a story someone can rewrite.
   block clock:    a fact everyone can check.
```

That's the difference, and it's the reason this little library exists: to read the **honest** clock
in friendly, human ways — a date, a moon, a birthday, a countdown.

## Slow on purpose

One more thing you might have noticed: the block clock is **slow**. Its fastest tick takes **ten
whole minutes**, and the network only re-tunes itself once every **two weeks**. That's not a bug.
It's a clock for people who plan in years and decades — who look after each other for a long, long
time. When you start measuring your life in blocks, ten minutes stops feeling long, and a hurried
world slows down a little. **Slow is the feature.**

**Next:** [the hidden thirteenth →](4-the-hidden-thirteenth.md)
