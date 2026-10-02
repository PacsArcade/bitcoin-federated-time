"""
bft.stamping -- the stamp, with options that can pull ANY item.

    stamp(h)                                  '0018.07.13 16:10 a₿'            (strict: throws on a non-height)
    face(h)                                   same, but a non-height gives '----.--.-- --:-- a₿'
    stamp(h, include=['epoch', 'moon'])       '0018.07.13 16:10 a₿ | epoch 481 | moon Waning Gibbous'
    stamp(h, template='{date} {time} {marker} #{heightc}')
    stamp(h, as_json=True)                    full record as JSON

Order never moves: the marker always follows the date and time. Extra items come after, each
separated by ' | '. The first segment is the template (default '{date} {time} {marker}').

Tokens (usable in a template as {name}, or pulled with include=[name, ...]):
  date time marker stamp datestamp        the canonical pieces
  height heightc                          123456 / 123,456
  year month day hour minute beat         the fields (zero padded as shown on the face)
  dayofyear week weekofyear               1..364, week of month 1..4, week of year 1..52
  epoch                                   retune number (height // 2016)
  retune retuneleft                       position '1121/2016', blocks left in this retune
  halving halvingpos halvingleft          era number, '12345/210000', blocks left in the era
  cycle subsidy                           cycle number, block subsidy in BTC
  animal                                  the year's animal sign (sky extension)
  moon                                    the sky's moon; needs at=<unix seconds>, else '--'
  ladder                                  the one-line step ladder
  json                                    (include only) the whole record as JSON

The moon is the sky's, from wall time (bft.sky). The core never reads a clock, so a stamp of a
past height has no moon unless the caller supplies `at`.
"""

from __future__ import annotations

import json as _json
import re
from typing import Any, Dict, Iterable, List, Optional

from . import core, steps as _ladder

DEFAULT_TEMPLATE = "{date} {time} {marker}"
DATE_ONLY_TEMPLATE = "{date} {marker}"
SEPARATOR = " | "

TOKENS = [
    "date", "time", "marker", "stamp", "datestamp", "height", "heightc",
    "year", "month", "day", "hour", "minute", "beat", "dayofyear", "week", "weekofyear",
    "epoch", "retune", "retuneleft", "halving", "halvingpos", "halvingleft",
    "cycle", "subsidy", "animal", "moon", "ladder", "json",
]
_TOKEN_RE = re.compile(r"\{([a-z]+)\}")
_INITIAL_SUBSIDY_SATS = 5_000_000_000


def _fmt_btc(sats: int) -> str:
    whole, frac = divmod(sats, 100_000_000)
    s = str(whole)
    if frac:
        s += "." + ("%08d" % frac).rstrip("0")
    return s


def _sky_tokens(h: int, at: Optional[float]) -> Dict[str, str]:
    from . import sky
    animal = sky.year_animal(h)
    out = {"animal": (animal["emoji"] + " " + animal["name"]) if animal.get("known") else "--"}
    if at is None:
        out["moon"] = "--"
    else:
        m = sky.moon_phase(h, at)
        out["moon"] = (m["emoji"] + " " + m["name"]) if m.get("known") else "--"
    return out


def values(h: int, at: Optional[float] = None) -> Dict[str, str]:
    """Every token for a real height (strict)."""
    f = core.fields(h)
    d, t = core.date(h), core.time(h)
    pos = h % core.DIFFICULTY_EPOCH_BLOCKS
    era_pos = h % core.HALVING_EPOCH_BLOCKS
    era = h // core.HALVING_EPOCH_BLOCKS
    sats = _INITIAL_SUBSIDY_SATS // (2 ** era) if era < 64 else 0
    v = {
        "date": d, "time": t, "marker": core.MARKER,
        "stamp": "%s %s %s" % (d, t, core.MARKER), "datestamp": "%s %s" % (d, core.MARKER),
        "height": str(h), "heightc": format(h, ","),
        "year": "%04d" % f["year"], "month": "%02d" % f["month"], "day": "%02d" % f["day"],
        "hour": "%02d" % f["hour"], "minute": "%02d" % f["minute"], "beat": str(f["beat"]),
        "dayofyear": str(f["dayOfYear"]), "week": str(f["weekOfMonth"]),
        "weekofyear": str((f["dayOfYear"] - 1) // core.DAYS_PER_WEEK + 1),
        "epoch": str(f["diffEpoch"]),
        "retune": "%d/%d" % (pos + 1, core.DIFFICULTY_EPOCH_BLOCKS),
        "retuneleft": str(core.DIFFICULTY_EPOCH_BLOCKS - 1 - pos),
        "halving": str(era), "halvingpos": "%d/%d" % (era_pos + 1, core.HALVING_EPOCH_BLOCKS),
        "halvingleft": str(core.HALVING_EPOCH_BLOCKS - 1 - era_pos),
        "cycle": str(h // core.CYCLE_BLOCKS), "subsidy": _fmt_btc(sats),
        "ladder": _ladder.ladder_line(h),
    }
    v.update(_sky_tokens(h, at))
    return v


def _dash_values() -> Dict[str, str]:
    v = {name: "--" for name in TOKENS}
    v.update({"date": core.DASH_DATE, "time": core.DASH_TIME, "marker": core.MARKER,
              "stamp": core.DASH_STAMP, "datestamp": core.DASH_DATE_STAMP})
    return v


def record(h: Any, at: Optional[float] = None) -> Dict[str, Any]:
    """The whole record: every token plus the full ladder. Dashes for a non-height."""
    if not core.is_height(h):
        return {"height": None, "known": False, "values": _dash_values(), "ladder": None}
    return {"height": h, "known": True, "values": values(h, at), "ladder": _ladder.ladder(h)}


def _render(h: Any, include: Iterable[str], template: Optional[str], date_only: bool,
            at: Optional[float]) -> str:
    vals = values(h, at) if core.is_height(h) else _dash_values()
    tpl = template if template is not None else (DATE_ONLY_TEMPLATE if date_only else DEFAULT_TEMPLATE)
    for name in _TOKEN_RE.findall(tpl):
        if name not in TOKENS or name == "json":
            raise ValueError("unknown token {%s}" % name)
    out = _TOKEN_RE.sub(lambda m: vals[m.group(1)], tpl)
    segs: List[str] = [out]
    for name in include:
        if name not in TOKENS:
            raise ValueError("unknown item %r (one of %s)" % (name, ", ".join(TOKENS)))
        if name == "json":
            raise ValueError("'json' is a mode, not an item: use as_json=True")
        if name in ("ladder",):
            segs.append(vals[name])
        elif name in ("stamp", "datestamp", "date", "time", "marker"):
            segs.append(vals[name])
        else:
            segs.append("%s %s" % (name, vals[name]))
    return SEPARATOR.join(segs)


def stamp(height: Any, include: Iterable[str] = (), template: Optional[str] = None,
          date_only: bool = False, at: Optional[float] = None, as_json: bool = False) -> str:
    """Strict stamp: throws ValueError on a non-height."""
    core.check(height)
    return _out(height, include, template, date_only, at, as_json)


def face(height: Any, include: Iterable[str] = (), template: Optional[str] = None,
         date_only: bool = False, at: Optional[float] = None, as_json: bool = False) -> str:
    """Display stamp: a non-height gives the dash face. Never throws on the height."""
    return _out(height, include, template, date_only, at, as_json)


def _out(height, include, template, date_only, at, as_json) -> str:
    if as_json:
        rec = record(height, at)
        rec["stamp"] = _render(height, include, template, date_only, at)
        return _json.dumps(rec, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return _render(height, include, template, date_only, at)
