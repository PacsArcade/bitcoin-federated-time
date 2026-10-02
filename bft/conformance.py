"""bft.conformance -- run vectors/vectors.json against this Python build. Returns a list of failures."""

from __future__ import annotations

import json
from typing import Any, List

from . import core, steps, stamping, live


def _raises(fn, *a, **k) -> bool:
    try:
        fn(*a, **k)
    except (ValueError, TypeError):
        return True
    return False


def _invalid_value(v: Any) -> Any:
    """vectors.json writes non-JSON inputs as strings: map the labels back to Python values."""
    table = {"NaN": float("nan"), "Infinity": float("inf"), "-Infinity": float("-inf")}
    return table.get(v, v) if isinstance(v, str) and v in table else v


def run(path: str) -> List[str]:
    v = json.load(open(path, encoding="utf-8"))
    fails: List[str] = []
    mine = {"BLOCKS_PER_BEAT": 1, "BLOCKS_PER_HOUR": core.BLOCKS_PER_HOUR,
            "BLOCKS_PER_DAY": core.BLOCKS_PER_DAY, "BLOCKS_PER_WEEK": core.BLOCKS_PER_WEEK,
            "BLOCKS_PER_MONTH": core.BLOCKS_PER_MONTH, "BLOCKS_PER_YEAR": core.BLOCKS_PER_YEAR,
            "DAYS_PER_MONTH": core.DAYS_PER_MONTH, "MONTHS_PER_YEAR": core.MONTHS_PER_YEAR,
            "DAYS_PER_YEAR": core.DAYS_PER_YEAR,
            "DIFFICULTY_EPOCH_BLOCKS": core.DIFFICULTY_EPOCH_BLOCKS,
            "HALVING_EPOCH_BLOCKS": core.HALVING_EPOCH_BLOCKS,
            "GENESIS_UNIX": 1231006505, "SECONDS_PER_BLOCK": 600}
    for k, want in v["constants"].items():
        if mine.get(k) != want:
            fails.append("constant %s: %r != %r" % (k, mine.get(k), want))
    for row in v["forward"]:
        h = row["height"]
        f = core.fields(h)
        for key in ("year", "month", "day", "dayOfYear", "weekOfMonth", "beat", "hour", "minute", "diffEpoch"):
            if f[key] != row[key]:
                fails.append("forward %d %s: %r != %r" % (h, key, f[key], row[key]))
        for key, got in (("date", core.date(h)), ("time", core.time(h)),
                         ("stamp", core.stamp_core(h, False)), ("stampTime", core.stamp_core(h, True))):
            if got != row[key]:
                fails.append("forward %d %s: %r != %r" % (h, key, got, row[key]))
    for row in v["inverse"]:
        got = core.inverse(row["year"], row["month"], row["day"])
        if got != row["firstHeight"]:
            fails.append("inverse %r: %r" % (row, got))
    for row in v["invalid"]:
        x = _invalid_value(row["input"])
        if not _raises(core.check, x):
            fails.append("invalid %r should be rejected" % (row["input"],))
        if core.face_core(x) != core.DASH_STAMP:
            fails.append("invalid %r display should be the dash face" % (row["input"],))
        if not _raises(stamping.stamp, x):
            fails.append("invalid %r strict stamp should throw" % (row["input"],))
        if stamping.face(x) != core.DASH_STAMP:
            fails.append("invalid %r face() should be dashes" % (row["input"],))
    for row in v.get("ladder", []):
        if steps.ladder(row["height"]) != row["rungs"]:
            fails.append("ladder %d differs" % row["height"])
        if steps.ladder_line(row["height"]) != row["line"]:
            fails.append("ladder_line %d: %r" % (row["height"], steps.ladder_line(row["height"])))
    for row in v.get("ranges", []):
        got = steps.unit_range(row["unit"], row["index"])
        for key in ("start", "end", "size"):
            if got[key] != row[key]:
                fails.append("range %s %d %s: %r != %r" % (row["unit"], row["index"], key, got[key], row[key]))
    for row in v.get("dateRanges", []):
        got = steps.date_range(*row["args"])
        for key in ("start", "end", "size", "unit"):
            if got[key] != row[key]:
                fails.append("dateRange %r %s: %r != %r" % (row["args"], key, got[key], row[key]))
    for row in v.get("stamps", []):
        got = stamping.stamp(row["height"], include=row.get("include", []), template=row.get("template"),
                             date_only=row.get("dateOnly", False), at=row.get("at"))
        if got != row["expected"]:
            fails.append("stamp %r: %r != %r" % (row, got, row["expected"]))
    for row in v.get("live", []):
        got = live.live_face(row["height"], row["arrivedAt"], row["now"], row["estimated"])
        if got != row["expected"]:
            fails.append("live %s: %r != %r" % (row["name"], got, row["expected"]))
    return fails
