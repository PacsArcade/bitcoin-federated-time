# Bitcoin Federated Time (BFT): specification

Version 1.0.0-draft. Status: draft for adoption by the Pac's Arcade fleet. Canonical home: `PacsArcade/bitcoin-federated-time`.
Referee: `vectors/vectors.json` (v2). Where this page and the vectors disagree, the vectors win and this page gets fixed.

The key words MUST, MUST NOT, SHOULD and MAY are used as in RFC 2119.

## 1. The idea in one breath

A Bitcoin block height is a clock nobody can edit. BFT reads it as a calendar: 10 BFT minutes per block, 6 blocks an hour, 144 blocks a day, 28 days a month, 13 months a year. The date is a measurement of the height. It is never an estimate, never a count kept by hand, and never read from a wall clock.

## 2. Heights

1. A height is a non-negative safe integer (0 to 2^53 - 1).
2. Anything else (null, NaN, Infinity, a negative number, a fraction, a string, a boolean) is not a height. Implementations MUST NOT coerce it. `"969505"` is not a height: parse it upstream.
3. Block 0 is a valid height and reads `0000.01.01 00:00 a₿`.
4. The strict API (`stamp`, `fields`, `date`, `time`, `inverse`) MUST throw on a non-height. The display API (`face`) MUST return the dash faces of section 6 and MUST NOT throw because of the height.

## 3. Constants

| name | blocks |
|---|---|
| hour | 6 |
| day | 144 |
| week (7 days) | 1,008 |
| retune (one difficulty adjustment) | 2,016 |
| month (28 days) | 4,032 |
| year (13 months, 364 days) | 52,416 |
| halving era | 210,000 |
| cycle (6 halving eras) | 1,260,000 |

A month is exactly 2 retunes and a year is exactly 26. There is no day 29 and no month 14, ever.

## 4. Derivation

```
dayIndex = floor(h / 144)         beat   = h mod 144
year     = floor(dayIndex / 364)  hour   = floor(beat / 6)
doy      = dayIndex mod 364       minute = (beat mod 6) * 10
month    = floor(doy / 28) + 1    day    = (doy mod 28) + 1
```

All arithmetic is on integers. Two nodes at the same height MUST agree to the character.

## 5. Format

- Date: `YYYY.MM.DD`. The year has at least 4 digits and is never truncated (`0100` at height 5,241,600; year 10000 stays five digits).
- Time: `HH:MM`, 24 hours, no am/pm.
- Stamp: `YYYY.MM.DD HH:MM a₿`. Single spaces. The marker `a₿` goes AFTER the date and time, always.
- Date-only stamp: `YYYY.MM.DD a₿`.
- A middle dot between date and time, and a marker before the date, are not BFT.

## 6. Dash faces

Real value or dashes, nothing in between: `----.--.--`, `--:--`, `----.--.-- --:-- a₿`, `----.--.-- a₿`. A surface that does not have a real height MUST show these. It MUST NOT show a guess, a hand-typed height, or a date derived from a civil clock.

## 7. Inverse

The first block of a BFT moment is exact:

```
first(y, m, d, hh, mm) = y * 52416 + (m - 1) * 4032 + (d - 1) * 144 + hh * 6 + mm / 10
```

with `1 <= m <= 13`, `1 <= d <= 28`, `0 <= hh <= 23`, `mm` in {0, 10, ..., 50}. Anything outside MUST throw. A civil (Gregorian) date to a height is a different thing: it is an estimate, it is labelled as one, and it lives in the optional extension (section 11).

## 8. The step ladder

Every height lies in exactly one slot of every unit. For a unit of `size` blocks:

```
index     = floor(h / size)          (which one, counted from block 0)
start     = index * size             end = start + size - 1
position  = h - start + 1            (this block is the n-th of size)
remaining = end - h                  untilNext = end + 1 - h
```

Units, small to large: block 1, hour 6, day 144, week 1,008, retune 2,016, month 4,032, year 52,416, halving 210,000, cycle 1,260,000. Block, hour, day, week, retune, month and year nest exactly (ratios 6, 24, 7, 2, 2, 13). The halving era does not divide a year (210,000 / 52,416 = 4.006) and is its own ruler; 6 eras make a cycle. `ladder(h)` returns every unit; `ladderLine(h)` returns `2 of 6 in hour | 98 of 144 in day | ...`; `unitRange(unit, index)` and `dateRange(y, m?, d?, hh?)` go the other way, from a unit to its first and last height. `pct` is `floor((20000 * position + size) / (2 * size)) / 100` (half-up, integer math).

## 9. The stamp with options

`stamp(h, options)` builds the canonical stamp and MAY append more items, each after ` | `. The canonical part always comes first and its order never changes. Options: a `template` using `{token}` placeholders, an `include` list of tokens, `dateOnly`, `at` (unix seconds, for the sky), and `json`. Tokens: date, time, marker, stamp, datestamp, height, heightc, year, month, day, hour, minute, beat, dayofyear, week, weekofyear, epoch (retune number), retune, retuneleft, halving, halvingpos, halvingleft, cycle, subsidy, animal, ladder, and the sky token (needs `at`). An unknown token MUST throw in the strict API. This section is a convention for tooling; the canonical stamp (section 5) is the standard.

## 10. Reading "now"

The library never reads a clock to make a date. The tip is read by a separate, optional function: the house beacon (`https://time.pacsarcade.org/height`) first, `https://mempool.space/api/blocks/tip/height` to verify, else dashes. A beacon and public gap of 2 or more blocks MUST be reported. A public height stands in only when the beacon is unreachable, and the output says so. A tip is never cached.

## 11. Extensions (optional, versioned apart, never part of core)

- Sky: the sky's own moon (real synodic phase from wall time) and the thirteen year animals. It never changes a calendar boundary.
- Gregorian bridge and anchors: one table of historical height-and-time anchors, optional, used only for labelled estimates, never rendered as "now".
- Pre-genesis (BB): negative heights, marker `b₿`, same field order. Out of core.
- Ordinal degree notation, halving and countdown helpers, lore.

## 12. Conformance

An implementation conforms if it passes every section of `vectors/vectors.json`: 42 forward vectors, 8 inverse, 9 invalid inputs, 12 ladder, 10 unit ranges, 6 date ranges, 11 stamps. Builds today: Python (`bft/`), TypeScript (`ts/`), and the inscription file (`js/bft.js`, strict, no network, no clock).

## 13. Versioning

Core changes only with a spec version. Extensions version separately. Any consumer SHOULD print the spec version it implements next to its vector self-test.
