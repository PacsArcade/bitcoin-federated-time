"""
bft.holidays — the chain's own feast days, computed from the block height.

Two kinds of holiday, both block-honest:

  * THE STORIED DAYS — one-time history, anchored to real heights (the genesis block, the
    halvings, SegWit, Taproot, the pizza). Block-native anchors are EXACT; days reached by
    bridging an old-calendar date are marked approximate (the ~ rule).
  * THE RECURRING DAYS — days the calendar itself throws, forever: the new-moon New Year,
    Halving Day every 210,000 blocks, the Conjunction every 1,260,000, the Hallows (the last
    day of the tenth month — the new calendar's All Hallows' Eve, honoring the whitepaper's
    31 Oct 2008), the whisper days (the thirteens), Year's End, and the Cat years.

Names are offered, not baked: the arcade blesses holiday names the way it blesses month
names — by decision, not by code. The HEIGHTS are the canon. Wonder, not finance.
"""

from __future__ import annotations

from typing import Any, Optional

from . import (BLOCKS_PER_DAY, BLOCKS_PER_MONTH, BLOCKS_PER_YEAR, CYCLE_BLOCKS,
               DAYS_PER_MONTH, HALVING_EPOCH_BLOCKS, MONTHS_PER_YEAR, format_date,
               from_height)
from .sky import year_animal

# --- the storied days (height, name, one-line story, exact?) -----------------
# Exact = the event IS a block (block-native). Approximate (~) = an old-calendar date
# bridged onto the chain. Research: the DW desk's chain-verified table (0018.04.15).
STORIED: list[dict[str, Any]] = [
    {"height": 0,         "name": "Genesis Block Day",       "exact": True,
     "story": "Block 0, the Times headline folded inside — the clock starts."},
    {"height": 78,        "name": "Running Bitcoin Day",     "exact": False,
     "story": "Hal Finney, out loud: 'Running bitcoin' — the first believer."},
    {"height": 57_043,    "name": "Bitcoin Pizza Day",       "exact": True,
     "story": "10,000 BTC for two pizzas — the first real-world purchase."},
    {"height": 97_230,    "name": "Satoshi Vanishing Day",   "exact": False,
     "story": "The last post, then quiet — the chain keeps going without him."},
    {"height": 210_000,   "name": "The First Halving",       "exact": True,
     "story": "50 → 25. The schedule holds."},
    {"height": 275_603,   "name": "HODL Day",                "exact": False,
     "story": "'I AM HODLING' — a typo becomes a creed."},
    {"height": 420_000,   "name": "The Second Halving",      "exact": True,
     "story": "25 → 12.5. The schedule holds."},
    {"height": 478_479,   "name": "Bitcoin Independence Day","exact": False,
     "story": "BIP-148: users, not miners, enforce the rules."},
    {"height": 481_824,   "name": "SegWit Day",              "exact": True,
     "story": "Malleability fixed; Lightning unlocked."},
    {"height": 630_000,   "name": "The Third Halving",       "exact": True,
     "story": "12.5 → 6.25 — the schedule holds, even mid-pandemic."},
    {"height": 709_632,   "name": "Taproot Day",             "exact": True,
     "story": "Schnorr lands — at 176 × 4,032, exactly on a BFT month boundary."},
    {"height": 840_000,   "name": "The Fourth Halving",      "exact": True,
     "story": "6.25 → 3.125 — mined on 4/20, because of course it was."},
    {"height": 1_050_000, "name": "The Fifth Halving",       "exact": True,
     "story": "3.125 → 1.5625 — already on the books; the block is fixed, the date drifts."},
]


def _day_index(height: int) -> int:
    return int(height) // BLOCKS_PER_DAY


def _recurring_for_day(d: dict[str, Any]) -> list[dict[str, Any]]:
    """The calendar's own feast days for one decomposed AB date (day-level)."""
    out: list[dict[str, Any]] = []
    month, day, year = d["month"], d["day"], d["year"]
    if month == 1 and day == 1:
        out.append({"name": "New Year (the new-moon new year)", "kind": "recurring",
                    "story": "M01·D01 — a new year opens on a new moon, every 52,416 blocks."})
    if month == 10 and day == DAYS_PER_MONTH:
        out.append({"name": "The Hallows", "kind": "recurring",
                    "story": "The last day of the tenth month — the new calendar's All "
                             "Hallows' Eve, honoring the whitepaper's 31 Oct 2008."})
    if month == MONTHS_PER_YEAR and day == DAYS_PER_MONTH:
        out.append({"name": "Year's End", "kind": "recurring",
                    "story": "M13·D28, the 364th day — the year completes with the moon."})
    if day == 13 or month == MONTHS_PER_YEAR:
        out.append({"name": "A Whisper Day", "kind": "recurring",
                    "story": "A thirteen is lit — the clock may be in a mood to speak "
                             "(see bft.lore.whisper)."})
    ya = year_animal(year * BLOCKS_PER_YEAR)
    if ya.get("is_the_thirteenth"):
        out.append({"name": "A Year of the Cat", "kind": "recurring",
                    "story": f"AB {year} belongs to the Astronomical Cat — the thirteenth, "
                             "welcomed home."})
    return out


def holidays_at(height: Optional[int]) -> list[dict[str, Any]]:
    """Every holiday whose DAY contains this height (storied + recurring + the schedule
    boundaries). Empty list on ordinary days — most days are ordinary; that's what makes
    a holiday one."""
    d = from_height(height)
    if not d.get("known") or d.get("epoch") == "BB":
        return []
    h = int(height)
    di = _day_index(h)
    out: list[dict[str, Any]] = []
    for s in STORIED:
        if _day_index(s["height"]) == di:
            out.append({**s, "kind": "storied",
                        "date": format_date(s["height"]),
                        "approx": not s["exact"]})
    day_start = di * BLOCKS_PER_DAY
    if di != 0:                                  # genesis owns its own day — epoch 0 is a birth, not a halving
        if (day_start // HALVING_EPOCH_BLOCKS) != ((day_start + BLOCKS_PER_DAY - 1) // HALVING_EPOCH_BLOCKS) or \
           day_start % HALVING_EPOCH_BLOCKS == 0:
            out.append({"name": "Halving Day", "kind": "schedule",
                        "story": "A halving boundary falls inside this day — epic sats are minted."})
        if (day_start // CYCLE_BLOCKS) != ((day_start + BLOCKS_PER_DAY - 1) // CYCLE_BLOCKS) or \
           day_start % CYCLE_BLOCKS == 0:
            out.append({"name": "The Conjunction", "kind": "schedule",
                        "story": "Halving meets retarget — the ~24-year hour hand ticks; a "
                                 "legendary sat is born."})
    out.extend(_recurring_for_day(d))
    return out


def next_holidays(height: Optional[int], count: int = 8,
                  max_days: int = 2 * 364) -> list[dict[str, Any]]:
    """The upcoming feast days: scans forward day by day (up to `max_days`) and returns the
    next `count` holidays with their day-start heights, dates, and stories. Whisper days are
    frequent by design (they're the breadcrumb rhythm) — they count, but they don't crowd out
    the rarer days because each day reports all of its holidays at once."""
    if height is None or int(height) < 0:
        return []
    start = _day_index(int(height)) + 1
    found: list[dict[str, Any]] = []
    for di in range(start, start + max_days):
        day_h = di * BLOCKS_PER_DAY
        todays = holidays_at(day_h)
        for t in todays:
            found.append({**t, "day_start_height": day_h, "date": format_date(day_h)})
        if len(found) >= count:
            break
    return found[:count]


def year_calendar(year: int) -> list[dict[str, Any]]:
    """The fixed feast days of one AB year, in order — the printable holiday calendar.
    (Whisper days are listed once as a rhythm, not 41 times as rows.)"""
    y = int(year)
    base = y * BLOCKS_PER_YEAR
    rows: list[dict[str, Any]] = []

    def _add(day_offset_blocks: int, name: str, story: str) -> None:
        h = base + day_offset_blocks
        rows.append({"name": name, "height": h, "date": format_date(h), "story": story})

    _add(0, "New Year (the new-moon new year)", "M01·D01 — the year opens on a new moon.")
    _add(9 * BLOCKS_PER_MONTH + 27 * BLOCKS_PER_DAY, "The Hallows",
         "M10·D28 — the new calendar's All Hallows' Eve (the whitepaper's night).")
    _add(12 * BLOCKS_PER_MONTH, "Sol's Seat opens",
         "M13·D01 — the thirteenth month begins; every day of it is a whisper day.")
    _add(12 * BLOCKS_PER_MONTH + 12 * BLOCKS_PER_DAY, "The Thirteenth of the Thirteenth",
         "M13·D13 — the loudest whisper of the year.")
    _add(13 * BLOCKS_PER_MONTH - BLOCKS_PER_DAY, "Year's End",
         "M13·D28 — the 364th day; the year completes with the moon.")
    for s in STORIED:
        if base <= s["height"] < base + BLOCKS_PER_YEAR:
            rows.append({"name": s["name"], "height": s["height"],
                         "date": format_date(s["height"]), "story": s["story"],
                         "approx": not s["exact"]})
    ya = year_animal(base)
    if ya.get("is_the_thirteenth"):
        rows.append({"name": "A Year of the Cat (all year)", "height": base,
                     "date": format_date(base),
                     "story": "The whole year belongs to the thirteenth animal."})
    rows.sort(key=lambda r: r["height"])
    rows.append({"name": "Whisper days (rhythm)", "height": base,
                 "date": f"every D13, and all of M{MONTHS_PER_YEAR}",
                 "story": "The thirteens — the clock may speak (bft.lore.whisper)."})
    return rows
