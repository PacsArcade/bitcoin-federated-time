"""
bft.sky — the moon and the thirteen animals ride the block calendar for free.

There is **one moon**, and it's the sky's — the real ~29.53-day synodic lunation, computed from
wall time (see `moon_phase()` below). The 28-day BFT month is a block count, a rhythm the
network keeps on its own, and it never wears the moon's name: no day-of-month formula stands in
for the sky. *(Ruling 0018.07.02, the Admiral: "we only have one moon. and we can see it
outside." This module used to also serve a second, block-timed "calendar's moon" — a pure
function of the day-of-month — asserted here as fact; that doctrine is retired. See
`docs/the-two-moons.md` for the retired doctrine, kept as history.)*

Each year carries one of **thirteen** animal signs: the traditional twelve, plus the **Cat** as the 13th
— the famous "left-out" sign of the Great Race (the rat tricked it out of the race) and a real sign
in the Vietnamese zodiac. We seat it thirteenth to match the 13-month year and Ophiuchus, the 13th
zodiac sign. Twelve you were given; the thirteenth was left out — a small door this library keeps
open on purpose. (See bft.lore.)

Signs are wonder, never finance — the same house rule as the rest of BFT.
"""

from __future__ import annotations

import math
from typing import Any, Optional

from . import from_height, DAYS_PER_MONTH, GENESIS_UNIX

# 8 phases across one synodic lunation of the sky's moon — not tied to the BFT month.
MOON_PHASES = [
    ("🌑", "New"), ("🌒", "Waxing Crescent"), ("🌓", "First Quarter"), ("🌔", "Waxing Gibbous"),
    ("🌕", "Full"), ("🌖", "Waning Gibbous"), ("🌗", "Last Quarter"), ("🌘", "Waning Crescent"),
]

# 13 animals — the twelve, plus the Astronomical Cat crowned 13th. BFT year 0 (2009) = Ox.
YEAR_ANIMALS = [
    ("🐀", "Rat"), ("🐂", "Ox"), ("🐅", "Tiger"), ("🐇", "Rabbit"), ("🐉", "Dragon"), ("🐍", "Snake"),
    ("🐎", "Horse"), ("🐐", "Goat"), ("🐒", "Monkey"), ("🐓", "Rooster"), ("🐕", "Dog"), ("🐖", "Pig"),
    ("🐈", "Astronomical Cat"),
]


# THE SKY'S MOON (ruling 0018.05.18): the real ~29.53-day synodic lunation from a
# known new-moon epoch — the 28-day month is our RHYTHM; the moon keeps her own.
SYNODIC_DAYS = 29.530588853
NEW_MOON_EPOCH_S = 947182440  # 2000-01-06 18:14 UTC


def moon_phase(height: Optional[int], at_ts: Optional[float] = None) -> dict[str, Any]:
    """THE SKY'S MOON — the real synodic phase (~29.53 days) anchored to the known
    new moon of 2000-01-06 18:14 UTC. `at_ts` (unix seconds) is the wall instant this
    height belongs to; callers with a LIVE tip should pass time.time() — the default
    genesis-average estimate (height × 600s) is deterministic but runs months ahead of
    the sky after years of fast blocks. Day 0 of the lunation = 🌑 new, ~day 15 of the
    lunation = 🌕 full. Returns
    {known, index 0..7, emoji, name, illumination 0..1, day}."""
    d = from_height(height)
    if not d.get("known") or d.get("epoch") == "BB":
        return {"known": False}
    ts = at_ts if at_ts is not None else GENESIS_UNIX + (height or 0) * 600
    age_days = ((ts - NEW_MOON_EPOCH_S) / 86400.0) % SYNODIC_DAYS
    frac = age_days / SYNODIC_DAYS                          # 0..1 through the lunation
    index = round(frac * 8) % 8
    emoji, name = MOON_PHASES[index]
    return {"known": True, "index": index, "emoji": emoji, "name": name,
            "illumination": round((1 - math.cos(2 * math.pi * frac)) / 2, 3),
            "day": int(age_days) + 1}


def year_animal(height: Optional[int]) -> dict[str, Any]:
    """The 13-animal sign for the BFT year (the twelve + the Cat). AB 0 (2009) = 🐂 Ox;
    AB 11 = 🐈 the Astronomical Cat; it wraps every 13 years."""
    d = from_height(height)
    if not d.get("known") or d.get("epoch") == "BB":
        return {"known": False}
    emoji, name = YEAR_ANIMALS[(d["year"] + 1) % 13]      # +1 so AB 0 lands on Ox; 13th = the Cat
    return {"known": True, "year": d["year"], "emoji": emoji, "name": name,
            "is_the_thirteenth": name == "Astronomical Cat"}
