"""
bft.sky — the moon and the thirteen animals ride the block calendar for free.

The 28-day BFT month is one whole moon. Because the phase is a pure function of the day-of-month,
the moon is *block-timed* like everything else: it drifts from the ~29.53-day astronomical moon on
purpose, the same way the 364-day year drifts from the sun. The chain is still the clock.

And because every month begins on **D01, a new moon**, every BFT new year (M01·D01) is a new-moon,
Asian-calendar-style new year — the shape falls out of the block math with nothing bolted on. Each
year carries one of **thirteen** animal signs: the traditional twelve, plus the **Cat** as the 13th
— the famous "left-out" sign of the Great Race (the rat tricked it out of the race) and a real sign
in the Vietnamese zodiac. We seat it thirteenth to match the 13-month year and Ophiuchus, the 13th
zodiac sign. Twelve you were given; the thirteenth was left out — a small door this library keeps
open on purpose. (See bft.lore.)

Signs are wonder, never finance — the same house rule as the rest of BFT.
"""

from __future__ import annotations

from typing import Any, Optional

from . import from_height, DAYS_PER_MONTH

# 8 phases, one lunation per month.
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


def moon_phase(height: Optional[int]) -> dict[str, Any]:
    """The BFT moon — one synodic cycle per BFT month, a pure function of the day-of-month.
    D01 = 🌑 new, ~D15 = 🌕 full, back to new by D28. Returns
    {known, index 0..7, emoji, name, illumination 0..1, day}."""
    d = from_height(height)
    if not d.get("known") or d.get("epoch") == "BB":
        return {"known": False}
    frac = (d["day"] - 1) / DAYS_PER_MONTH                 # 0..1 through the lunation
    index = round(frac * 8) % 8
    emoji, name = MOON_PHASES[index]
    return {"known": True, "index": index, "emoji": emoji, "name": name,
            "illumination": round(1 - abs(1 - 2 * frac), 3), "day": d["day"]}


def year_animal(height: Optional[int]) -> dict[str, Any]:
    """The 13-animal sign for the BFT year (the twelve + the Cat). AB 0 (2009) = 🐂 Ox;
    AB 11 = 🐈 the Astronomical Cat; it wraps every 13 years."""
    d = from_height(height)
    if not d.get("known") or d.get("epoch") == "BB":
        return {"known": False}
    emoji, name = YEAR_ANIMALS[(d["year"] + 1) % 13]      # +1 so AB 0 lands on Ox; 13th = the Cat
    return {"known": True, "year": d["year"], "emoji": emoji, "name": name,
            "is_the_thirteenth": name == "Astronomical Cat"}
