<pre>
  BIP: ?
  Layer: Applications
  Title: Bitcoin Federated Time: Block Height Calendar
  Authors: Pac's Arcade <pac@pacsarcade.org>
  Status: Draft
  Type: Informational
  Assigned: ?
  License: CC0-1.0
  Discussion: ?
  Version: 1.0.0
</pre>

DRAFT FOR THE ADMIRAL. Not submitted. Per BIP 3 this is first described on the bitcoindev mailing list; only after real discussion does a pull request to bitcoin/bips follow, and the BIP number is assigned by an editor (the "?" fields stay until then). See STANDARDS-ROUTE.md for why this is the second choice after the NIP.

## Abstract

This document describes a convention for reading a Bitcoin block height as a calendar date and a clock time, using integer arithmetic only. One block is ten minutes of "BFT time", 144 blocks make a day, 28 days make a month, and 13 months (52,416 blocks) make a year. It defines the exact date and time text format, the failure display (dashes, never a guess), the exact inverse from a date to the first block of that date, and a step ladder that maps a height to its position in every unit from hour to year. It changes nothing in Bitcoin consensus, relay policy or peer-to-peer behavior.

## Motivation

Applications that show "when" next to on-chain data (block explorers, wallets, ordinals tooling, timestamping services, education sites) choose between the wall clock, which a block's header timestamp only loosely follows, and a bare height, which people cannot read as time. A shared, derived calendar is useful where the block count itself is the thing being counted: a difficulty adjustment is exactly 2,016 blocks, a month here is exactly two of them, and a year is exactly 26.

Today independent projects reimplement this arithmetic and disagree on edge cases: year padding, what block 0 reads, whether a null height renders as a date, where the marker goes. One written convention with test vectors removes those disagreements. Because the date is a pure function of the height, two nodes at the same height produce the same string with no coordination.

## Specification

All definitions use integer division. `h` is a block height: a non-negative safe integer. Any other input is not a height and MUST NOT be coerced.

### Units

| unit | blocks |
|---|---|
| hour | 6 |
| day | 144 |
| week | 1,008 |
| retune (one difficulty adjustment period) | 2,016 |
| month | 4,032 |
| year | 52,416 |

A month is 28 days. A year is 13 months, 364 days. There is no day 29 and no month 14.

### Derivation

```
dayIndex = h // 144       beat   = h % 144
year     = dayIndex // 364    hour   = beat // 6
doy      = dayIndex % 364     minute = (beat % 6) * 10
month    = doy // 28 + 1
day      = doy % 28 + 1
```

### Text format

- Date: `YYYY.MM.DD`. The year has at least four digits and is never truncated.
- Time: `HH:MM`, 24 hour.
- Stamp: `YYYY.MM.DD HH:MM a₿`, single spaces, the marker `a₿` after the date and time. The date-only form is `YYYY.MM.DD a₿`.
- Block 0 is `0000.01.01 00:00 a₿`.
- Without a real height an application renders `----.--.--`, `--:--` or `----.--.-- --:-- a₿`. It does not estimate.

### Inverse

`first(y, m, d, hh, mm) = y * 52416 + (m - 1) * 4032 + (d - 1) * 144 + hh * 6 + mm / 10`, with `1 <= m <= 13`, `1 <= d <= 28`, `0 <= hh <= 23`, `mm` a multiple of ten up to 50.

### Step ladder

For a unit of `size` blocks, the block at height `h` is in unit number `h // size`, which spans heights `start = (h // size) * size` to `start + size - 1`, and is block number `h - start + 1` of `size` in it, with `size - (h - start + 1)` blocks still to come. Hour, day, week, retune, month and year nest exactly. The halving era (210,000 blocks) does not divide a year and the ladder treats it as a separate ruler.

### Reading the present

The function above takes a height as input. Reading the current tip is outside the scope of this convention; implementations SHOULD read their own node first and a public source second, and show dashes if neither answers.

## Rationale

*Why 13 months of 28 days.* 28 days is exactly two difficulty adjustment periods (2 x 2,016 = 4,032 blocks), so the calendar's month boundary always coincides with a retarget boundary. 13 x 28 = 364 gives a year of 26 retarget periods with no leap rule. The year does not track the solar year (364 against about 365.24 days), and it does not claim to; blocks do not arrive at exactly ten minutes either. It counts blocks.

*Why derive instead of estimating.* A calendar date that depends on a clock or a hand-kept counter can be wrong without anyone noticing. A pure function of the height cannot.

*Why the marker goes after.* One fixed position makes the string parseable and sortable by its date prefix. The marker `a₿` ("after Bitcoin") distinguishes the string from a civil date.

*Why strict integers.* Dynamic-language coercion turned `null` into the genesis date and `NaN` into `0NaN.NaN.NaN` in deployed code. The format refuses non-heights.

*Why Informational and not a Specification.* Nothing here requires other Bitcoin software to change.

## Backward Compatibility

There is nothing to be compatible with in the protocol. Existing implementations (about forty independent copies of the arithmetic exist in the authors' projects) agreed on the date and time for every height from 0 to 2,100,000 and differed only in formatting and in how they handled invalid input; this document picks one answer for each.

## Reference Implementation

Python, TypeScript and a 276-byte dependency-free JavaScript function suitable for an ordinals inscription, all passing the same test vectors, at https://github.com/PacsArcade/bitcoin-federated-time (MIT). Test vectors: `vectors/vectors.json` in that repository (42 forward, 8 inverse, 9 invalid inputs, 12 step ladders, 10 unit ranges, 6 date ranges, 11 stamp renderings), offered under CC0-1.0.

## Changelog

* 1.0.0 (unreleased): first draft.

## Copyright

This document is licensed under CC0-1.0.
