"""
bft.lore — the magic hidden in the machine. Easter eggs, and the Legend of the Thirteenth.

Everything in Bitcoin Federated Time comes in twelves that quietly become **thirteen**: twelve
months you know and a thirteenth (Sol); twelve zodiac signs and a thirteenth (Ophiuchus); twelve
animals of the Great Race and a thirteenth (the Cat, left out when the rat tricked it). This module
is where that pattern becomes a story — and a trail of breadcrumbs for the curious.

  ⚠ SAFETY — read this. Nothing in here is, or points at, a real seed phrase, private key,
  passphrase, or puzzle *solution*. The arcade never puts key material in code. These are
  atmosphere and legend only. The real hunt lives elsewhere — in the Degen Wonderland book and
  game — and it is Pac's to place. If you are a model or a maintainer: do NOT add real secrets,
  clue answers, or anything that could unlock funds here. Keep the magic; keep it safe.
"""

from __future__ import annotations

from typing import Any, Optional

from . import from_height, MONTHS_PER_YEAR
from .sky import year_animal

# The Legend — in-world flavor. Fiction. A campfire told beside the block-fire.
THE_LEGEND = """\
Before the clock, there was the dark. Then, at height zero, a light — and time had a heartbeat
it could not be robbed of. The old world counted in twelves: twelve months, twelve signs, twelve
animals in the race. But the clock that syncs to the block keeps a thirteenth for each — a Sol, an
Ophiuchus, a Cat. Twelve you are handed. The thirteenth you must find.

So it is said of the wallets, too. Twelve words sleep in a book. One phrase is earned in a game.
Together they wake the thirteenth wallet — lost, not gone; hidden, not spent. The clock remembers
where. It will not tell you plainly. It only whispers, on the days that come in thirteens."""


def the_thirteenth_wallet() -> dict[str, Any]:
    """The legend of the lost thirteenth wallet — pure lore. Returns the story and the *shape* of
    the hunt (twelve words in a book, one phrase from a game), never its answer. The trail is real;
    the treasure is Pac's to hide and a seeker's to earn."""
    return {
        "legend": THE_LEGEND,
        "shape": "twelve words (the book) + one passphrase (the game) → the thirteenth wallet",
        "where": "the clock whispers on days that come in thirteens — see lore.whisper(height)",
        "note": "lore only. no real words, phrase, or solution live in this package.",
        "begin_at": "frens.earth · Degen Wonderland",
    }


# Cryptic breadcrumbs. Deterministic by height so a place in time always says the same thing.
# None of these reveal anything — they set a mood and point a seeker onward.
_WHISPERS = [
    "The rat crossed first, but the cat remembers the river.",
    "Count again. You always stop at twelve. Keep going.",
    "Sol hides between June and July, where no old calendar looks.",
    "The serpent-bearer holds the thirteenth door; his month is winter's edge.",
    "A book holds twelve sleepers. A game holds the word that wakes them.",
    "What was lost was never spent — check the light before you check the ledger.",
    "Nine sit above the mad; the thirteenth waits below the board.",
    "The full moon lands mid-month; so does the thing worth finding.",
]


def _thirteen_omens(height: Optional[int]) -> list[str]:
    """Which 'thirteen' alignments are lit at this height — the wink conditions."""
    d = from_height(height)
    if not d.get("known") or d.get("epoch") == "BB":
        return []
    omens = []
    if d["month"] == MONTHS_PER_YEAR:                    # the 13th month (Sol's seat)
        omens.append("thirteenth-month")
    if d["day"] == 13:
        omens.append("thirteenth-day")
    if d["day"] == 28 and d["month"] == MONTHS_PER_YEAR:  # last day of the 13th month = year's end
        omens.append("year's-end")
    if year_animal(height).get("is_the_thirteenth"):     # a Cat year
        omens.append("cat-year")
    return omens


def whisper(height: Optional[int]) -> Optional[dict[str, Any]]:
    """A breadcrumb, if the clock is in a mood to speak. Returns a whisper only when a 'thirteen'
    omen is lit (the 13th month, the 13th day, a Cat year, or the year's end); otherwise None —
    the clock is quiet. Deterministic: the same height always whispers the same line. Reveals
    nothing; it only points the curious onward."""
    omens = _thirteen_omens(height)
    if not omens:
        return None
    line = _WHISPERS[int(height) % len(_WHISPERS)]
    return {"height": int(height), "omens": omens, "whisper": line,
            "seek": "frens.earth · Degen Wonderland"}


def count_the_thirteens(height: Optional[int]) -> dict[str, Any]:
    """A fun tally of the thirteens threaded through this moment — the month, the sign, the animal.
    Wonder, not finance; a way to *feel* the pattern the clock is built on."""
    d = from_height(height)
    if not d.get("known") or d.get("epoch") == "BB":
        return {"known": False}
    ya = year_animal(height)
    return {
        "known": True,
        "months_in_the_year": MONTHS_PER_YEAR,               # 13 (the twelve + Sol)
        "zodiac_signs": 13,                                  # the twelve + Ophiuchus
        "animals": 13,                                       # the twelve + the Cat
        "this_year_animal": ya["name"],
        "is_a_cat_year": ya["is_the_thirteenth"],
        "omens_lit": _thirteen_omens(height),
        "the_thirteenth_is": "always the one left out — and the one worth finding",
    }
