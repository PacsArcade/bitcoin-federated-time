"""The Bitcoin Time Clock in your terminal.

    python -m bft                      # the clock ~now (wall-clock estimate, 10 min a block)
    python -m bft 958346               # the clock at a height (chain-exact)
    python -m bft 1983-06-13           # a birthday (UTC; ~estimated height; b₿ before genesis)
    python -m bft 2027-01-07 20:24     # any old-calendar moment
"""

from __future__ import annotations

import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")   # Windows consoles vs ₿ ° ′ ″

import bft
from bft import holidays


def main(argv: list[str]) -> int:
    arg = " ".join(argv[1:]).strip() or None
    if arg in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    if arg is None:
        import time
        t = time.gmtime()
        h = bft.height_at(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
        print("(no height given — ~estimated from the wall clock at 10 min a block; "
              "feed a real tip height for on-chain truth)")
    elif re.fullmatch(r"-?\d[\d,_]*", arg):
        h = int(arg.replace(",", "").replace("_", ""))
    else:
        m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{1,2}):(\d{2}))?", arg)
        if not m:
            print(__doc__.strip())
            return 2
        y, mo, dd = int(m.group(1)), int(m.group(2)), int(m.group(3))
        hh, mm = int(m.group(4) or 12), int(m.group(5) or 0)
        h = bft.height_at(y, mo, dd, hh, mm)
        print(f"(~estimated height for {arg} UTC at a steady 10-minute block)")
    print("\n".join(bft.format_clock(h)))
    today = holidays.holidays_at(h)
    if today:
        print("  Today:            " + "  ·  ".join(t["name"] for t in today))
    coming = holidays.next_holidays(h, count=3)
    if coming:
        print("  Coming up:        " + "  ·  ".join(f"{c['name']} ({c['date']})" for c in coming))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
