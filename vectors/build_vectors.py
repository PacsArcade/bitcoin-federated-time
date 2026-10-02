#!/usr/bin/env python3
"""Regenerate the v2 additions to vectors.json (ladder, ranges, dateRanges, stamps, extra invalid).

The v1 sections (forward, inverse, invalid, constants) come from the block 969,505 audit and are
kept byte-for-byte; this script only adds sections computed by the Python reference, and
tests/test_ladder.py re-derives them independently (brute-force tiling), so they are not
circular. Run:  python3 vectors/build_vectors.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import bft  # noqa: E402

PATH = os.path.join(HERE, "vectors.json")
v = json.load(open(PATH, encoding="utf-8"))
v["version"] = 2
v["generatedAt"] = ("v1 from the block 969,505 audit (bft.from_height + block_beat, cross-checked against "
                    "onecocreation bft.ts); v2 adds ladder/ranges/dateRanges/stamps from bft.steps and bft.stamping, "
                    "re-derived independently in tests/test_ladder.py")

have = [json.dumps(r["input"]) for r in v["invalid"]]
for extra, note in ((True, "bool is not a height"), ("Infinity", "not finite"),
                    ("-Infinity", "not finite")):
    if json.dumps(extra) not in have:
        v["invalid"].append({"input": extra, "display": "----.--.--", "strict": "throw", "note": note})

v["ladder"] = [{"height": h, "line": bft.ladder_line(h), "rungs": bft.ladder(h)}
               for h in (0, 5, 143, 144, 1007, 2016, 52415, 52416, 210000, 969505, 1260000, 5241600)]
v["ranges"] = [{"unit": u, "index": i, **{k: bft.unit_range(u, i)[k] for k in ("start", "end", "size")}}
               for u, i in (("block", 7), ("hour", 0), ("hour", 161584), ("day", 6732), ("week", 961),
                            ("retune", 480), ("month", 240), ("year", 18), ("halving", 4), ("cycle", 0))]
v["dateRanges"] = [{"args": a, **{k: bft.date_range(*a)[k] for k in ("unit", "start", "end", "size")}}
                   for a in ([18], [18, 7], [18, 7, 13], [18, 7, 13, 16], [0, 1, 1, 0], [100, 1, 1])]
AT = 1790856000  # 2026-10-01T12:00:00Z, the sky's moon is waning gibbous
stamp_cases = [
    {"height": 969505},
    {"height": 969505, "dateOnly": True},
    {"height": 0},
    {"height": 5241600},
    {"height": 969505, "include": ["epoch", "retune", "halvingpos", "subsidy", "animal"]},
    {"height": 969505, "include": ["moon"], "at": AT},
    {"height": 969505, "include": ["moon"]},
    {"height": 969505, "include": ["ladder"]},
    {"height": 969505, "template": "{date} {time} {marker} #{heightc}"},
    {"height": 969505, "template": "{year}/{month}/{day} w{weekofyear} d{dayofyear} {stamp}"},
    {"height": 983664, "template": "{datestamp} retune-left {retuneleft} halving {halving} cycle {cycle}"},
]
v["stamps"] = [{**c, "expected": bft.stamp(c["height"], include=c.get("include", []), template=c.get("template"),
                                           date_only=c.get("dateOnly", False), at=c.get("at"))}
               for c in stamp_cases]
A = 1790900000
live_cases = [
    ("normal, 4:32 into the step", 969505, A, A + 272, False),
    ("just landed", 969505, A, A, False),
    ("exactly 9:59 still live", 969505, A, A + 599, False),
    ("10:00 holds at 9:59", 969505, A, A + 600, False),
    ("late hold, 15 minutes over", 969505, A, A + 1500, False),
    ("step 50 at 9:59 stays in the hour", 969509, A, A + 599, False),
    ("step 50 held", 969509, A, A + 5000, False),
    ("clock skew: now before arrival reads 0", 969505, A, A - 30, False),
    ("fractional seconds floor", 969505, A, A + 61.9, False),
    ("missing arrival: no seconds", 969505, None, A, False),
    ("missing clock: no seconds", 969505, A, None, False),
    ("estimated arrival passes through", 969505, A, A + 100, True),
    ("block 0", 0, A, A + 5, False),
    ("not a height", None, A, A + 5, False),
    ("not a height (negative)", -1, A, A + 5, False),
]
v["live"] = [{"name": n, "height": h, "arrivedAt": a, "now": nw, "estimated": est,
              "expected": bft.live_face(h, a, nw, est)} for n, h, a, nw, est in live_cases]
v["liveRules"] = {"hold": "elapsed >= 600 holds at step+9:59; lateBy = elapsed-600", "skew": "now < arrivedAt reads 0, skewed=true",
                  "missing": "no arrival or no clock: HH:M-:-- (dashes for the unknown digits)",
                  "scope": "display convention, not the standard; the canonical stamp stays height-only"}
json.dump(v, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(PATH, "a").write("\n")
print("vectors v2:", len(v["forward"]), "forward,", len(v["inverse"]), "inverse,", len(v["invalid"]), "invalid,",
      len(v["ladder"]), "ladder,", len(v["ranges"]), "ranges,", len(v["dateRanges"]), "dateRanges,",
      len(v["stamps"]), "stamps")
