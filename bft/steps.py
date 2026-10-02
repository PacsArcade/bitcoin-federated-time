"""
bft.steps -- the step ladder: from a block height to ANY time unit, and back.

One block is one rung. Every unit above it is a fixed run of blocks, so a height lands in
exactly one slot of every unit, always:

    block 1 -> hour 6 -> day 144 -> week 1,008 -> retune 2,016 -> month 4,032 -> year 52,416
    halving era 210,000 -> cycle 1,260,000

(retune = one difficulty adjustment. Week, retune, month and year nest exactly: 2 weeks make
a retune, 2 retunes make a month, 13 months make a year. The halving era does NOT divide a
year evenly (it is about 4.006 years), so it is its own ruler; 6 eras make a cycle.)

    ladder(h)               every unit: index, position inside, blocks left, start/end heights
    ladder_line(h)          one line: "2 of 6 in hour | 98 of 144 in day | ..."
    unit_range(unit, n)     the height range of the n-th unit (the way back down)
    date_range(y, m, d, h)  the height range of a calendar slot (year / month / day / hour)
    unit_at(unit, h)        which unit number a height is in

Pure integer math on top of bft.core. Strict: a non-height raises ValueError.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from . import core
from .core import check

# (key, label, blocks, parent key if it nests exactly else None)
UNITS = [
    ("block", "Block", 1, "hour"),
    ("hour", "Hour", core.BLOCKS_PER_HOUR, "day"),
    ("day", "Day", core.BLOCKS_PER_DAY, "week"),
    ("week", "Week", core.BLOCKS_PER_WEEK, "retune"),
    ("retune", "Retune", core.DIFFICULTY_EPOCH_BLOCKS, "month"),
    ("month", "Month", core.BLOCKS_PER_MONTH, "year"),
    ("year", "Year", core.BLOCKS_PER_YEAR, None),
    ("halving", "Halving era", core.HALVING_EPOCH_BLOCKS, "cycle"),
    ("cycle", "Cycle", core.CYCLE_BLOCKS, None),
]
UNIT_KEYS = [u[0] for u in UNITS]
_BY_KEY = {u[0]: u for u in UNITS}
SIZES = {u[0]: u[2] for u in UNITS}


def _unit(key: str):
    if key not in _BY_KEY:
        raise ValueError("unknown unit %r (one of %s)" % (key, ", ".join(UNIT_KEYS)))
    return _BY_KEY[key]


def _label(key: str, h: int, index: int) -> str:
    f = core.fields(h)
    if key == "block":
        return "block %d" % h
    if key == "hour":
        return "%02d:00 on %s" % (f["hour"], core.date(h))
    if key == "day":
        return core.date(h)
    if key == "week":
        return "week %d of month %02d, year %04d" % (f["weekOfMonth"], f["month"], f["year"])
    if key == "retune":
        return "retune %d" % index
    if key == "month":
        return "%04d.%02d" % (f["year"], f["month"])
    if key == "year":
        return "%04d" % f["year"]
    if key == "halving":
        return "halving era %d" % index
    return "cycle %d" % index


def _pct(position: int, size: int):
    """Percent through the unit, 2 decimals, half-up in integer math (same in every language);
    whole numbers come back as ints so JSON matches JavaScript byte for byte."""
    hundredths = (20000 * position + size) // (2 * size)
    return hundredths // 100 if hundredths % 100 == 0 else hundredths / 100


def rung(key: str, h: int) -> Dict[str, Any]:
    """One rung of the ladder for height h."""
    check(h)
    _, label, size, parent = _unit(key)
    index = h // size
    start = index * size
    end = start + size - 1
    out = {
        "unit": key, "label": label, "size": size,
        "index": index,                       # which one, counted from block 0 (0-based)
        "name": _label(key, h, index),
        "start": start, "end": end,
        "position": h - start + 1,            # this block is the n-th of `size` in it (1-based)
        "of": size,
        "remaining": end - h,                 # blocks still to come inside this unit
        "untilNext": end + 1 - h,             # blocks until the next one starts (this block counts as 1 away)
        "pct": _pct(h - start + 1, size),
        "parent": None,
    }
    if parent:
        ratio = _BY_KEY[parent][2] // size
        out["parent"] = {"unit": parent, "n": index % ratio + 1, "of": ratio}
    return out


def ladder(h: int) -> List[Dict[str, Any]]:
    """Every unit at once, smallest to largest."""
    check(h)
    return [rung(k, h) for k in UNIT_KEYS]


def ladder_line(h: int) -> str:
    """'2 of 6 in hour | 98 of 144 in day | ...' for every unit above the block."""
    parts = []
    for r in ladder(h)[1:]:
        parts.append("%s of %s in %s" % (format(r["position"], ","), format(r["of"], ","), r["unit"]))
    return " | ".join(parts)


def unit_at(unit: str, h: int) -> int:
    """Which unit number (0-based from genesis) the height is in."""
    return check(h) // _unit(unit)[2]


def unit_range(unit: str, index: int) -> Dict[str, Any]:
    """The way back down: the first and last height of the n-th unit (0-based)."""
    _, label, size, _p = _unit(unit)
    if not (isinstance(index, int) and not isinstance(index, bool) and index >= 0):
        raise ValueError("unit index must be a non-negative integer: %r" % (index,))
    start = index * size
    end = start + size - 1
    check(end)
    return {"unit": unit, "label": label, "index": index, "size": size, "start": start, "end": end,
            "first": core.stamp_core(start), "last": core.stamp_core(end)}


def date_range(year: int, month: Optional[int] = None, day: Optional[int] = None,
               hour: Optional[int] = None) -> Dict[str, Any]:
    """Height range of a calendar slot. Give year; or year+month; or year+month+day; or all four."""
    if month is None:
        unit, size = "year", core.BLOCKS_PER_YEAR
        start = core.inverse(year)
    elif day is None:
        unit, size = "month", core.BLOCKS_PER_MONTH
        start = core.inverse(year, month)
    elif hour is None:
        unit, size = "day", core.BLOCKS_PER_DAY
        start = core.inverse(year, month, day)
    else:
        unit, size = "hour", core.BLOCKS_PER_HOUR
        start = core.inverse(year, month, day, hour)
    end = start + size - 1
    return {"unit": unit, "size": size, "start": start, "end": end,
            "first": core.stamp_core(start), "last": core.stamp_core(end)}
