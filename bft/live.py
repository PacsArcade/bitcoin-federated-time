"""
bft.live -- the LIVE FACE: minutes and seconds that tick from the last block.

A DISPLAY CONVENTION, not the standard. The canonical stamp stays height-only ('HH:MM' in steps of 10).
The date and the hour and the 10-minute step still come from the HEIGHT alone. The wall clock is used for
exactly one thing: measuring seconds since this block ARRIVED (when our node first saw it). The law "never read a
wall clock to make a date" is untouched, because no date or step is ever derived from `now`.

    live_face(height, arrived_at, now)  ->  {known, text, hour, minute, second, elapsed, holding, lateBy, skewed, estimated}

  * elapsed = floor(now - arrived_at), clamped at 0. A clock that runs backwards (now < arrived) reads as 0 and sets skewed.
  * minute = step + floor(elapsed / 60), second = elapsed % 60, for elapsed 0..599 (00:00 to 09:59 into the step).
  * At elapsed >= 600 the face HOLDS at step + 9 : 59 ("straining", holding=True, lateBy = elapsed - 600). It never
    rolls into the next step. Only a real block (a new height) moves it, and it snaps to the new step at :00.
  * No arrival time (or a non-finite clock): no seconds are invented. The unknown digits are dashes: '18:2-:--'.
    Chosen over showing the bare 10-minute stamp because '18:20' on a face with a seconds slot reads as an exact
    18:20:00, which is a claim we cannot back; dashes say exactly what is known (the step) and nothing more.
  * `estimated` is passed through for callers whose arrival time is a stand-in (an inscription's cold load).
"""

from __future__ import annotations

import math
from typing import Any, Dict, Optional

from . import core

HOLD_AT = 600  # seconds in one 10-minute step


def _num(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def live_face(height: Any, arrived_at: Any, now: Any, estimated: bool = False) -> Dict[str, Any]:
    if not core.is_height(height):
        return {"known": False, "text": "----.--.-- --:--:-- " + core.MARKER, "hour": None, "minute": None,
                "second": None, "elapsed": None, "holding": False, "lateBy": 0, "skewed": False,
                "estimated": bool(estimated)}
    f = core.fields(height)
    d = core.date(height)
    hh = "%02d" % f["hour"]
    if not (_num(arrived_at) and _num(now)):
        step = f["minute"] // 10
        return {"known": True, "text": "%s %s:%d-:-- %s" % (d, hh, step, core.MARKER), "hour": f["hour"],
                "minute": None, "second": None, "elapsed": None, "holding": False, "lateBy": 0,
                "skewed": False, "estimated": bool(estimated)}
    raw = math.floor(now - arrived_at)
    skewed = raw < 0
    e = max(0, raw)
    holding = e >= HOLD_AT
    shown = HOLD_AT - 1 if holding else e
    minute = f["minute"] + shown // 60
    second = shown % 60
    return {"known": True, "text": "%s %s:%02d:%02d %s" % (d, hh, minute, second, core.MARKER), "hour": f["hour"],
            "minute": minute, "second": second, "elapsed": e, "holding": holding,
            "lateBy": e - HOLD_AT if holding else 0, "skewed": skewed, "estimated": bool(estimated)}
