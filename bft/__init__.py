"""
Bitcoin Federated Time (BFT) — the clock that syncs to the block, not the sun.

A block height is a timestamp no authority can edit. This library turns a Bitcoin block
height into three honest readings of time, plus one sidebar:

  1. THE CLOCK — the hh:mm block-beat, the canonical face. A BFT day is 144 blocks on a
     24-hour face: 6 blocks an hour, ten "minutes" a block, no seconds. `block_beat()`.
  2. A CALENDAR — 13 perfect 28-day months, counted purely in blocks (the "Federated Time"
     calendar). A month is exactly two difficulty adjustments; a year is 26. Dates render
     ₿-marked, marker after: `0018.04.20 a₿` (pre-genesis inverts day-first: `b₿`-marked).
  3. The COUNTDOWNS — the inverse of the block count: blocks remaining to the next difficulty
     adjustment, the next halving, the next cycle conjunction, and the last satoshi (~2140).
  ·  THE ORDINAL SIDEBAR — Bitcoin's degree notation A°B′C″D‴, which ordinal theory labels
     hour/minute/second/third. Real lore, honestly labeled: those are ordinal INDICES
     (block-in-halving-epoch, block-in-difficulty-period), not clock time. `degree()`.

"BFT" reads as Byzantine Fault Tolerance too, which is the whole point: the network agrees on
the height, so the network agrees on the time. And "BTC" gets a second reading here —
**Bitcoin Time Clock**. (That's our lens, not an official expansion — the ticker is still just
Bitcoin. But ordinal theory's hour/minute/second naming is real, and it means the chain has a
clock built in.)

Pure standard library. No dependencies. Offline-first. MIT licensed.
"""

from __future__ import annotations

from typing import Any, Optional

__version__ = "0.3.0"

# --- Bitcoin's own intervals (exact, protocol-defined) -----------------------
DIFFICULTY_EPOCH_BLOCKS = 2_016          # one difficulty adjustment (~2 weeks)
HALVING_EPOCH_BLOCKS = 210_000           # one halving epoch (~4 years)
CYCLE_BLOCKS = 6 * HALVING_EPOCH_BLOCKS  # 1,260,000 — halving+difficulty conjunction (~24y)
INITIAL_SUBSIDY_SATS = 5_000_000_000     # 50 BTC, the genesis block subsidy
SUBSIDY_ZERO_HALVING = 33                # subsidy floors to 0 at halving epoch 33
LAST_SUBSIDY_BLOCK = SUBSIDY_ZERO_HALVING * HALVING_EPOCH_BLOCKS  # 6,930,000 (~year 2140)
GENESIS_ISO = "2009-01-03"               # block 0 — the clock starts
GENESIS_UNIX = 1_231_006_505             # genesis block timestamp, 2009-01-03 18:15:05 UTC
SECONDS_PER_BLOCK = 600                  # the 10-minute target — the model's tick rate

# --- the Federated Time calendar (block-native, 13x28) -----------------------
BLOCKS_PER_DAY = 144
BLOCKS_PER_HOUR = 6                                       # 24 block-hours a day, 10 min a block
DAYS_PER_WEEK = 7
DAYS_PER_MONTH = 28
MONTHS_PER_YEAR = 13
BLOCKS_PER_WEEK = BLOCKS_PER_DAY * DAYS_PER_WEEK          # 1,008
BLOCKS_PER_MONTH = BLOCKS_PER_DAY * DAYS_PER_MONTH        # 4,032  (= 2 difficulty epochs)
DAYS_PER_YEAR = DAYS_PER_MONTH * MONTHS_PER_YEAR          # 364
BLOCKS_PER_YEAR = BLOCKS_PER_DAY * DAYS_PER_YEAR          # 52,416 (= 26 difficulty epochs)


# ============================================================================ #
# 0. The clock face — hh:mm block-beat (the canonical, house-standard reading)
# ============================================================================ #
def block_beat(height: Optional[int]) -> Optional[dict[str, Any]]:
    """The canonical BFT clock face: **hh:mm block-beat**. A BFT day = 144 blocks on a
    24-hour face — 6 blocks an hour, ten "minutes" a block, `hh:mm` stepping by ten,
    **no seconds**. Chain-exact: two nodes at the same height show the same face.

        beat   = height mod 144      → 0..143  (the block within the BFT day)
        hour   = beat // 6           → 0..23   (the block-hour)
        minute = (beat mod 6) * 10   → 0,10..50 (which ten-minute beat of the hour)

    Returns None for heights before genesis (no blocks tick there — see the BB inverse).
    """
    if height is None or int(height) < 0:
        return None
    beat = int(height) % BLOCKS_PER_DAY
    hour = beat // BLOCKS_PER_HOUR
    minute = (beat % BLOCKS_PER_HOUR) * 10
    return {"hhmm": f"{hour:02d}:{minute:02d}", "hour": hour, "minute": minute,
            "beat": beat, "blocks_into_hour": beat % BLOCKS_PER_HOUR}


# ============================================================================ #
# 1. The calendar
# ============================================================================ #
def from_height(height: Optional[int]) -> dict[str, Any]:
    """Decompose a block height into a Bitcoin Federated Time date.

    All integer block math, so two nodes at the same height agree on the date. Heights >= 0 are
    **After Bitcoin (AB)**; negative heights render as **Before Bitcoin (BB)** — the inverse
    count, |height| blocks before genesis. Unknown height (None) returns {"known": False}.
    """
    if height is None:
        return {"known": False, "height": None}
    h = int(height)
    if h < 0:                                       # inverse: before the genesis block
        before = -h                                 # magnitude, decomposed the same way, counting back
        doe = before // BLOCKS_PER_DAY
        by = doe // DAYS_PER_YEAR
        doy = doe % DAYS_PER_YEAR
        mi = doy // DAYS_PER_MONTH
        dom = doy % DAYS_PER_MONTH
        return {"known": True, "height": h, "epoch": "BB",
                "blocks_before_genesis": before,
                "year": by, "month": mi + 1, "day": dom + 1, "month_index": mi,
                "label": f"BB {by} · M{mi + 1:02d} · D{dom + 1:02d}",
                "note": "Before Bitcoin: the clock runs in reverse here — time the chain cannot vouch for"}

    day_of_epoch = h // BLOCKS_PER_DAY
    block_of_day = h % BLOCKS_PER_DAY
    year_index = day_of_epoch // DAYS_PER_YEAR
    day_of_year = day_of_epoch % DAYS_PER_YEAR
    month_index = day_of_year // DAYS_PER_MONTH
    day_of_month = day_of_year % DAYS_PER_MONTH
    return {
        "known": True, "height": h, "epoch": "AB",
        "year": year_index, "month": month_index + 1, "day": day_of_month + 1,
        "month_index": month_index, "day_of_year": day_of_year + 1,
        "week_of_month": (day_of_month // DAYS_PER_WEEK) + 1,
        "beat": block_of_day, "day_progress": round(100 * block_of_day / BLOCKS_PER_DAY, 1),
        "diff_epoch": h // DIFFICULTY_EPOCH_BLOCKS,
        "label": f"AB {year_index} · M{month_index + 1:02d} · D{day_of_month + 1:02d}",
    }


def format_date(height: Optional[int], month_names: Optional[list[str]] = None,
                style: str = "date") -> str:
    """Render the calendar date. The default (house-standard) style is 'date' — the ₿-marked
    bitcoin date, marker AFTER: '0018.04.20 a₿'. `month_names` (13) supplies blessed month
    lore in the 'short'/'long' styles when set, else 'M01'..'M13'.
    style: 'date' -> '0018.04.20 a₿'; 'short' -> 'AB 18 · M04 · D20'; 'long' adds
    block + diff-epoch."""
    d = from_height(height)
    if not d.get("known"):
        return "BFT —"
    if style == "date":
        # the ₿-marked bitcoin date — unmistakably a *bitcoin* date, year zero-padded to 4,
        # marker AFTER the date (house standard, per bft-display). The display year IS
        # bitcoin's age: genesis opens 0000. After Bitcoin is month-first (yyyy.mm.dd a₿);
        # Before Bitcoin inverts to day-first (yyyy.dd.mm b₿).
        if d["epoch"] == "BB":
            return f"{d['year']:04d}.{d['day']:02d}.{d['month']:02d} b₿"
        return f"{d['year']:04d}.{d['month']:02d}.{d['day']:02d} a₿"
    if d["epoch"] == "BB":
        bi = d.get("month_index", 0)
        bmonth = (str(month_names[bi]) if month_names and len(month_names) >= MONTHS_PER_YEAR
                  and month_names[bi] else f"M{d['month']:02d}")
        return f"BB {d['year']} · {bmonth} · D{d['day']:02d}"
    mi = d["month_index"]
    month = (str(month_names[mi]) if month_names and len(month_names) >= MONTHS_PER_YEAR
             and month_names[mi] else f"M{d['month']:02d}")
    short = f"{d['epoch']} {d['year']} · {month} · D{d['day']:02d}"
    return f"{short}  (block {d['height']:,} · diff-epoch {d['diff_epoch']})" if style == "long" else short


def year_progress(height: Optional[int]) -> dict[str, Any]:
    """How far through the current BFT year, with the block distances to the next month/year."""
    d = from_height(height)
    if not d.get("known") or d["epoch"] == "BB":
        return {"known": False}
    return {
        "known": True, "year": d["year"], "month": d["month"], "day_of_year": d["day_of_year"],
        "year_pct": round(100 * d["day_of_year"] / DAYS_PER_YEAR, 1),
        "blocks_to_next_month": BLOCKS_PER_MONTH - (d["height"] % BLOCKS_PER_MONTH),
        "blocks_to_next_year": BLOCKS_PER_YEAR - (d["height"] % BLOCKS_PER_YEAR),
    }


def height_at(year: int, month: int, day: int,
              hour: int = 0, minute: int = 0, second: int = 0) -> int:
    """Estimate the block height for a Gregorian UTC date/time — the bridge from the calendar you
    were handed to Bitcoin time. Model: (seconds since genesis) / 600. Dates before the genesis
    block (2009-01-03 18:15:05 UTC) return a **negative** height — the Before-Bitcoin (BB) inverse.

    This is an ESTIMATE, deliberately. Real blocks don't arrive exactly every 10 minutes, so a
    past date won't land on the exact height it historically did, and a future date is a
    projection at the target rate. What's exact is the arithmetic, not the wall clock — feed a
    real tip height to the other functions when you need on-chain truth.
    """
    import calendar as _cal
    unix = _cal.timegm((int(year), int(month), int(day),
                        int(hour), int(minute), int(second), 0, 0, 0))  # UTC, any year
    return round((unix - GENESIS_UNIX) / SECONDS_PER_BLOCK)


def from_gregorian(year: int, month: int, day: int,
                   hour: int = 0, minute: int = 0, second: int = 0) -> dict[str, Any]:
    """A Gregorian birthday (or any UTC moment) rendered in Bitcoin Federated Time. Returns the
    estimated block height plus the full clock; `estimate=True` is a standing reminder the height
    is modeled, not looked up. Pre-genesis input comes back as the BB inverse."""
    h = height_at(year, month, day, hour, minute, second)
    reading = clock(h)
    reading["estimate"] = True
    reading["before_bitcoin"] = h < 0
    return reading


def before_bitcoin(year: int, month: int, day: int, second: Optional[int] = None) -> str:
    """Wall-clock label for a date *before* genesis: 'yyyy.dd.mm[.ss] b₿' — day-first, the mirror
    of the After-Bitcoin 'yyyy.mm.dd a₿' (marker after, house standard). On-chain heights are
    never negative, so this is only for pre-genesis / negative-time references (the grey side of
    the clock, before the light)."""
    base = f"{year:04d}.{day:02d}.{month:02d}"
    return f"{base} b₿" if second is None else f"{base}.{second:02d} b₿"


# ============================================================================ #
# 2. The ordinal sidebar — Bitcoin's built-in degree notation
# ============================================================================ #
def degree(height: Optional[int]) -> Optional[dict[str, Any]]:
    """THE ORDINAL SIDEBAR — Bitcoin's degree notation A°B′C″D‴ for the FIRST sat of the
    block, which ordinal theory labels hour°/minute′/second″/third‴. Real ordinal-theory
    lore, honestly framed: these are ordinal INDICES, not clock time — the clock face
    people read is `block_beat()` (hh:mm). For the sat collectors:

        A (hour)   = cycle number                         (every 1,260,000 blocks)
        B (minute) = index of block within the halving epoch (0..209,999)
        C (second) = index of block within the difficulty period (0..2,015)
        D (third)  = index of sat within the block (0 = the block's first sat)

    Returns None for heights before genesis (no sats exist there). See ordinal theory:
    https://docs.ordinals.com/overview.html
    """
    if height is None or height < 0:
        return None
    h = int(height)
    hour = h // CYCLE_BLOCKS
    minute = h % HALVING_EPOCH_BLOCKS
    second = h % DIFFICULTY_EPOCH_BLOCKS
    third = 0                                    # the block-clock ticks on each block's first sat
    return {
        "notation": f"{hour}°{minute}′{second}″{third}‴",
        "hour": hour, "minute": minute, "second": second, "third": third,
        "reading": "hour°minute′second″third‴",
        "rarity_of_first_sat": block_rarity(h),
    }


def block_rarity(height: int) -> str:
    """Ordinal rarity of the block's FIRST sat — the calendar tick's collectible echo.
    Every block's first sat is at least 'uncommon'; the boundaries that make BFT's units
    (difficulty period, halving epoch, cycle, genesis) are exactly the rare/epic/legendary/mythic
    sats. The calendar and the collectible are the same skeleton."""
    h = int(height)
    if h == 0:
        return "mythic"                          # the genesis sat
    if h % CYCLE_BLOCKS == 0:
        return "legendary"                       # first sat of a cycle
    if h % HALVING_EPOCH_BLOCKS == 0:
        return "epic"                            # first sat of a halving epoch
    if h % DIFFICULTY_EPOCH_BLOCKS == 0:
        return "rare"                            # first sat of a difficulty period
    return "uncommon"                            # first sat of any block


# ============================================================================ #
# 3. Halvings, cycles, and the inverse (countdown) view
# ============================================================================ #
def halving(height: Optional[int]) -> Optional[dict[str, Any]]:
    """Halving-epoch context + the block subsidy at this height, with the inverse count to the
    next halving (blocks remaining)."""
    if height is None or height < 0:
        return None
    h = int(height)
    epoch = h // HALVING_EPOCH_BLOCKS
    into = h % HALVING_EPOCH_BLOCKS
    subsidy = INITIAL_SUBSIDY_SATS >> epoch if epoch < 64 else 0
    return {
        "epoch": epoch, "blocks_into_epoch": into,
        "blocks_to_next_halving": HALVING_EPOCH_BLOCKS - into,   # the inverse / countdown
        "epoch_pct": round(100 * into / HALVING_EPOCH_BLOCKS, 1),
        "subsidy_sats": subsidy, "subsidy_btc": subsidy / 1e8,
    }


def cycle(height: Optional[int]) -> Optional[dict[str, Any]]:
    """Cycle (conjunction) context — the 1,260,000-block 'hour' of the ordinal degree notation,
    with the inverse count to the next conjunction (~24-year rhythm; first conjunction ~2032)."""
    if height is None or height < 0:
        return None
    h = int(height)
    into = h % CYCLE_BLOCKS
    return {
        "cycle": h // CYCLE_BLOCKS, "blocks_into_cycle": into,
        "blocks_to_next_conjunction": CYCLE_BLOCKS - into,      # the inverse / countdown
        "cycle_pct": round(100 * into / CYCLE_BLOCKS, 1),
    }


def countdown(height: Optional[int]) -> Optional[dict[str, Any]]:
    """The inverse of the block clock — everything that counts DOWN. There are no negative block
    heights on-chain (the chain starts at genesis), so 'counting backward' in Bitcoin means these
    remaining-block countdowns, plus the conceptual Before-Bitcoin epoch for pre-genesis time."""
    if height is None or height < 0:
        return None
    h = int(height)
    return {
        "to_difficulty_adjustment": DIFFICULTY_EPOCH_BLOCKS - h % DIFFICULTY_EPOCH_BLOCKS,
        "to_halving": HALVING_EPOCH_BLOCKS - h % HALVING_EPOCH_BLOCKS,
        "to_conjunction": CYCLE_BLOCKS - h % CYCLE_BLOCKS,
        "to_last_satoshi": max(0, LAST_SUBSIDY_BLOCK - h),      # ~year 2140, when issuance ends
    }


# ============================================================================ #
# The whole clock, one call
# ============================================================================ #
def clock(height: Optional[int]) -> dict[str, Any]:
    """Every reading of the block at `height`: the hh:mm face, calendar, halving, cycle,
    countdown — and the ordinal-degree sidebar."""
    return {
        "height": height,
        "beat": block_beat(height),
        "calendar": from_height(height),
        "degree": degree(height),
        "halving": halving(height),
        "cycle": cycle(height),
        "countdown": countdown(height),
    }


def format_clock(height: Optional[int], month_names: Optional[list[str]] = None) -> list[str]:
    """Human-readable multi-line render of the full clock. The hh:mm block-beat face leads
    (the canonical reading); the ordinal degree notation rides along as a labeled sidebar."""
    d = from_height(height)
    if not d.get("known"):
        return ["BFT — unknown height"]
    if d["epoch"] == "BB":
        return [format_date(height), "(no clock before genesis — the chain vouches for nothing here)"]
    bb, deg = block_beat(height), degree(height)
    hv, cy, cd = halving(height), cycle(height), countdown(height)
    return [
        f"Bitcoin Time Clock — block {int(height):,}",
        f"  Clock (hh:mm):    {bb['hhmm']}   (beat {bb['beat']}/144 · 6 blocks an hour · ten minutes a block)",
        f"  Date (BFT):       {format_date(height)}   ({format_date(height, month_names, style='short')})",
        f"  Level:            {d['diff_epoch']}  ·  re-tunes in {cd['to_difficulty_adjustment']:,} blocks",
        f"  Halving epoch:    {hv['epoch']}  ·  subsidy {hv['subsidy_btc']:g} BTC  ·  {hv['epoch_pct']}% through",
        f"  Cycle:            {cy['cycle']}  ·  {cy['cycle_pct']}% through  ·  "
        f"{cy['blocks_to_next_conjunction']:,} blocks to the next conjunction",
        f"  Counting down:    {cd['to_difficulty_adjustment']:,} → retarget  ·  "
        f"{cd['to_halving']:,} → halving  ·  {cd['to_last_satoshi']:,} → the last sat",
        f"  Ordinal sidebar:  {deg['notation']}   (degree notation, for the sat collectors — "
        f"ordinal indices, not clock time; first sat: {deg['rarity_of_first_sat']})",
    ]


# --- the sky, the magic, and the feast days (imported last — the core above comes first) ------
from .sky import moon_phase, year_animal, MOON_PHASES, YEAR_ANIMALS  # noqa: E402,F401
from . import lore  # noqa: E402,F401
from . import holidays  # noqa: E402,F401
