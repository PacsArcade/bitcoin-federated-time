"""
bft -- the command line.

    bft stamp [HEIGHT] [--with a,b,c] [--fmt TEMPLATE] [--date-only] [--json] [--at UNIX] [--source] [--strict]
    bft ladder [HEIGHT] [--json]
    bft range UNIT INDEX          first and last block of the n-th hour/day/week/retune/month/year/halving/cycle
    bft range DATE                a calendar slot: 0018 | 0018.07 | 0018.07.13 | 0018.07.13T16
    bft tip                       the beacon, mempool.space to verify
    bft verify [VECTORS.json]     run the canonical vectors against this build
    bft items                     list every item / token

No HEIGHT means: read the tip (house beacon first, mempool.space to verify, else dashes).
A bad height never becomes a date: it prints the dash face (and exits 2 with --strict).
"""

from __future__ import annotations

import json
import os
import sys
import time as _time
from typing import List, Optional

import bft
from bft import core, steps, stamping, beacon


def _parse_height(s: str) -> Optional[int]:
    s = s.replace(",", "").replace("_", "")
    return int(s) if s.isdigit() else None


def _split_opts(argv: List[str]):
    pos, o = [], {"with": [], "fmt": None, "date_only": False, "json": False, "at": None,
                  "source": False, "strict": False}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--with":
            i += 1
            o["with"] += [x for x in argv[i].split(",") if x]
        elif a == "--fmt":
            i += 1
            o["fmt"] = argv[i]
        elif a == "--at":
            i += 1
            o["at"] = float(argv[i])
        elif a == "--date-only":
            o["date_only"] = True
        elif a == "--json":
            o["json"] = True
        elif a == "--source":
            o["source"] = True
        elif a == "--strict":
            o["strict"] = True
        elif a.startswith("--"):
            raise ValueError("unknown flag %s" % a)
        else:
            pos.append(a)
        i += 1
    return pos, o


def _height_arg(pos, o):
    """Returns (height or None, tip info or None)."""
    if pos:
        h = _parse_height(pos[0])
        return h, None
    info = beacon.tip()
    return info["height"], info


def cmd_stamp(argv):
    pos, o = _split_opts(argv)
    h, info = _height_arg(pos, o)
    at = o["at"]
    live = info is not None and h is not None
    wants_moon = "moon" in o["with"] or "{moon}" in (o["fmt"] or "")
    if at is None and live and wants_moon:
        at = _time.time()                       # a live tip: now is the real wall instant
    out = stamping.face(h, include=o["with"], template=o["fmt"], date_only=o["date_only"],
                        at=at, as_json=o["json"])
    print(out)
    if o["source"] and info is not None:
        print("source: %s | %s" % (info["source"] or "none", info["note"]), file=sys.stderr)
    if o["strict"] and h is None:
        return 2
    return 0


def cmd_ladder(argv):
    pos, o = _split_opts(argv)
    h, info = _height_arg(pos, o)
    if h is None:
        print(core.DASH_STAMP)
        return 2 if o["strict"] else 0
    lad = steps.ladder(h)
    if o["json"]:
        print(json.dumps(lad, ensure_ascii=False, separators=(",", ":")))
        return 0
    print("block %s  =  %s" % (format(h, ","), core.stamp_core(h)))
    W = (14, 20, 12, 12, 12)
    print("unit".ljust(12) + "".join(" " + t.rjust(w) for t, w in zip(
        ("n-th (0-based)", "this block is", "left after", "start", "end"), W)))
    for r in lad:
        cells = (format(r["index"], ","), "%s of %s" % (format(r["position"], ","), format(r["of"], ",")),
                 format(r["remaining"], ","), format(r["start"], ","), format(r["end"], ","))
        print(r["unit"].ljust(12) + "".join(" " + c.rjust(w) for c, w in zip(cells, W)))
    return 0


def cmd_range(argv):
    pos, o = _split_opts(argv)
    if len(pos) == 2 and pos[0] in steps.UNIT_KEYS:
        r = steps.unit_range(pos[0], int(pos[1]))
    elif len(pos) == 1:
        s = pos[0]
        hour = None
        if "T" in s:
            s, hh = s.split("T")
            hour = int(hh)
        parts = [int(x) for x in s.split(".")]
        parts += [None] * (3 - len(parts))
        r = steps.date_range(parts[0], parts[1], parts[2], hour)
    else:
        print(__doc__.strip())
        return 2
    print(json.dumps(r, ensure_ascii=False) if o["json"] else
          "%s: blocks %s to %s (%s blocks)  %s  to  %s" % (
              r["unit"], format(r["start"], ","), format(r["end"], ","), format(r["size"], ","),
              r["first"], r["last"]))
    return 0


def cmd_tip(argv):
    info = beacon.tip()
    print(json.dumps(info, separators=(",", ":")))
    return 0 if info["height"] is not None else 2


def cmd_items(argv):
    print("items / tokens: " + " ".join(stamping.TOKENS))
    print("units: " + " ".join(steps.UNIT_KEYS))
    return 0


def cmd_verify(argv):
    path = argv[0] if argv else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                             "vectors", "vectors.json")
    from . import conformance
    fails = conformance.run(path)
    for f in fails:
        print("FAIL " + f)
    print("%s: %d failure(s)" % (path, len(fails)))
    return 1 if fails else 0


COMMANDS = {"stamp": cmd_stamp, "ladder": cmd_ladder, "range": cmd_range, "tip": cmd_tip,
            "items": cmd_items, "verify": cmd_verify}


def main(argv: Optional[List[str]] = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    cmd = COMMANDS.get(argv[0])
    if cmd is None:
        print("unknown command %r\n" % argv[0] + __doc__.strip(), file=sys.stderr)
        return 2
    try:
        return cmd(argv[1:])
    except (ValueError, IndexError) as e:
        print("bft: %s" % e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
