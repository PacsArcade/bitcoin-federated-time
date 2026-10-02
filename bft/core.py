"""
bft.core -- the frozen core of Bitcoin Federated Time (spec: spec/BFT-SPEC.md).

Pure integer math, standard library only, no network, no clock. A height in, a reading out.
This file changes only with a spec version. Every language build (Python here, TypeScript in
ts/, the inscription file in js/bft.js) must pass vectors/vectors.json exactly.

Rules in one breath (the spec has the long form):
  * a height is a non-negative safe integer; nothing else is a height, nothing is coerced.
  * 1 block = 10 BFT minutes; 6 = hour; 144 = day; 28 days (4,032) = month;
    13 months (364 days, 52,416 blocks) = year. No day 29, no month 14.
  * stamp = "YYYY.MM.DD HH:MM a₿": year at least 4 digits, never truncated, marker AFTER.
  * strict API throws on a non-height; display API (face) returns the dash faces.
"""

from __future__ import annotations

from typing import Any, Dict

MARKER = "a₿"
MAX_SAFE_INTEGER = 2 ** 53 - 1

BLOCKS_PER_HOUR = 6
BLOCKS_PER_DAY = 144
DAYS_PER_WEEK = 7
BLOCKS_PER_WEEK = 1008
DAYS_PER_MONTH = 28
MONTHS_PER_YEAR = 13
DAYS_PER_YEAR = 364
BLOCKS_PER_MONTH = 4032
BLOCKS_PER_YEAR = 52416
DIFFICULTY_EPOCH_BLOCKS = 2016        # "retune"
HALVING_EPOCH_BLOCKS = 210000
CYCLE_BLOCKS = 1260000

DASH_DATE = "----.--.--"
DASH_TIME = "--:--"
DASH_STAMP = DASH_DATE + " " + DASH_TIME + " " + MARKER
DASH_DATE_STAMP = DASH_DATE + " " + MARKER


def is_height(h: Any) -> bool:
    """True only for a real non-negative safe integer. bool, float, str, None are not heights."""
    return (isinstance(h, int) and not isinstance(h, bool) and 0 <= h <= MAX_SAFE_INTEGER)


def check(h: Any) -> int:
    """Strict gate. Returns h or raises ValueError. Nothing is coerced."""
    if not is_height(h):
        raise ValueError("not a height: %r (a height is a non-negative safe integer)" % (h,))
    return h


def fields(h: int) -> Dict[str, int]:
    """The calendar reading of a height. Strict."""
    check(h)
    day_index = h // BLOCKS_PER_DAY
    beat = h % BLOCKS_PER_DAY
    doy = day_index % DAYS_PER_YEAR
    return {
        "height": h,
        "year": day_index // DAYS_PER_YEAR,
        "month": doy // DAYS_PER_MONTH + 1,
        "day": doy % DAYS_PER_MONTH + 1,
        "dayOfYear": doy + 1,
        "weekOfMonth": (doy % DAYS_PER_MONTH) // DAYS_PER_WEEK + 1,
        "beat": beat,
        "hour": beat // BLOCKS_PER_HOUR,
        "minute": (beat % BLOCKS_PER_HOUR) * 10,
        "diffEpoch": h // DIFFICULTY_EPOCH_BLOCKS,
    }


def date(h: int) -> str:
    f = fields(h)
    return "%04d.%02d.%02d" % (f["year"], f["month"], f["day"])


def time(h: int) -> str:
    f = fields(h)
    return "%02d:%02d" % (f["hour"], f["minute"])


def stamp_core(h: int, with_time: bool = True) -> str:
    """The canonical stamp. 'YYYY.MM.DD HH:MM a₿' or, date only, 'YYYY.MM.DD a₿'."""
    return (date(h) + " " + time(h) + " " + MARKER) if with_time else (date(h) + " " + MARKER)


def face_core(h: Any, with_time: bool = True) -> str:
    """Display variant: a real height renders, anything else is the dash face. Never throws."""
    if not is_height(h):
        return DASH_STAMP if with_time else DASH_DATE_STAMP
    return stamp_core(h, with_time)


def inverse(year: int, month: int = 1, day: int = 1, hour: int = 0, minute: int = 0) -> int:
    """First block of a BFT moment, exact. Defaults to the start of the month/day/hour given."""
    for name, v, lo, hi in (("year", year, 0, MAX_SAFE_INTEGER), ("month", month, 1, MONTHS_PER_YEAR),
                            ("day", day, 1, DAYS_PER_MONTH), ("hour", hour, 0, 23),
                            ("minute", minute, 0, 50)):
        if not (isinstance(v, int) and not isinstance(v, bool) and lo <= v <= hi):
            raise ValueError("%s out of range: %r" % (name, v))
    if minute % 10:
        raise ValueError("minute must be a multiple of 10: %r" % (minute,))
    h = (year * BLOCKS_PER_YEAR + (month - 1) * BLOCKS_PER_MONTH + (day - 1) * BLOCKS_PER_DAY
         + hour * BLOCKS_PER_HOUR + minute // 10)
    return check(h)
