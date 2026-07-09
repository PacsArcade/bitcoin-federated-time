"""Tests for bitcoin-federated-time. Pure stdlib; run with:  python -m pytest  (or python tests/test_bft.py)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import bft  # noqa: E402


def test_calendar_boundaries():
    assert bft.from_height(0)["label"] == "AB 0 · M01 · D01"
    assert bft.from_height(bft.BLOCKS_PER_MONTH)["month"] == 2
    assert bft.from_height(bft.BLOCKS_PER_MONTH)["day"] == 1
    assert bft.from_height(bft.BLOCKS_PER_YEAR)["year"] == 1
    assert bft.from_height(bft.BLOCKS_PER_YEAR - bft.BLOCKS_PER_DAY)["day_of_year"] == 364


def test_month_is_two_difficulty_epochs():
    assert bft.BLOCKS_PER_MONTH == 2 * bft.DIFFICULTY_EPOCH_BLOCKS
    assert bft.BLOCKS_PER_YEAR == 26 * bft.DIFFICULTY_EPOCH_BLOCKS


def test_before_bitcoin_is_the_inverse():
    d = bft.from_height(-4032)
    assert d["epoch"] == "BB"
    assert d["blocks_before_genesis"] == 4032
    assert bft.degree(-1) is None          # no sats before genesis


def test_degree_notation():
    # genesis: cycle 0, minute 0, second 0, third 0, and the mythic sat
    g = bft.degree(0)
    assert g["notation"] == "0°0′0″0‴"
    assert g["rarity_of_first_sat"] == "mythic"
    # a block partway in
    d = bft.degree(210_000)                # first block of halving epoch 1 -> epic first sat
    assert d["hour"] == 0 and d["minute"] == 0
    assert d["rarity_of_first_sat"] == "epic"
    assert bft.degree(2_016)["rarity_of_first_sat"] == "rare"
    assert bft.degree(1_260_000)["rarity_of_first_sat"] == "legendary"
    assert bft.degree(1)["rarity_of_first_sat"] == "uncommon"


def test_halving_subsidy():
    assert bft.halving(0)["subsidy_btc"] == 50.0
    assert bft.halving(210_000)["subsidy_btc"] == 25.0
    assert bft.halving(840_000)["subsidy_btc"] == 3.125     # the 2024 halving epoch
    assert bft.halving(0)["blocks_to_next_halving"] == 210_000


def test_countdown_inverse():
    cd = bft.countdown(0)
    assert cd["to_halving"] == 210_000
    assert cd["to_difficulty_adjustment"] == 2_016
    assert cd["to_last_satoshi"] == bft.LAST_SUBSIDY_BLOCK
    # near the end, the countdown floors at zero, never negative
    assert bft.countdown(bft.LAST_SUBSIDY_BLOCK + 5)["to_last_satoshi"] == 0


def test_cycle_conjunction():
    assert bft.cycle(0)["cycle"] == 0
    assert bft.cycle(1_260_000)["cycle"] == 1
    assert bft.CYCLE_BLOCKS == 6 * bft.HALVING_EPOCH_BLOCKS


def test_gregorian_bridge():
    assert bft.height_at(2009, 1, 3, 18, 15, 5) == 0        # the genesis moment -> block 0
    assert bft.height_at(2008, 1, 1) < 0                    # before bitcoin -> negative
    r = bft.from_gregorian(2015, 7, 20, 9, 30)
    assert r["estimate"] is True and r["before_bitcoin"] is False
    assert r["calendar"]["epoch"] == "AB"
    b = bft.from_gregorian(1990, 5, 15)                     # pre-genesis birthday -> BB inverse
    assert b["before_bitcoin"] is True
    assert b["calendar"]["epoch"] == "BB"
    assert bft.format_date(b["height"]).startswith("BB ")
    assert bft.degree(b["height"]) is None                 # no ordinal clock before genesis


def test_bitcoin_date_style():
    assert bft.format_date(0, style="date") == "a₿ 0000.01.01"
    assert bft.format_date(858_000, style="date") == "a₿ 0016.05.23"     # matches AB 16 · M05 · D23
    assert bft.before_bitcoin(2008, 10, 31) == "b₿ 2008.31.10"           # day-first inverse
    assert bft.format_date(bft.height_at(2008, 10, 31), style="date").startswith("b₿ ")


def test_sky_moon_and_animals():
    assert bft.moon_phase(0)["name"] == "New"                            # D01 = new moon
    assert bft.moon_phase(14 * bft.BLOCKS_PER_DAY)["name"] == "Full"     # ~mid-month = full
    assert bft.year_animal(0)["name"] == "Ox"                            # AB 0 (2009) = Ox
    assert bft.year_animal(11 * bft.BLOCKS_PER_YEAR)["is_the_thirteenth"] is True   # Cat
    assert bft.year_animal(12 * bft.BLOCKS_PER_YEAR)["name"] == "Rat"    # wraps after the Cat


def test_lore_is_magic_not_leakage():
    from bft import lore
    th = 12 * bft.BLOCKS_PER_MONTH + 12 * bft.BLOCKS_PER_DAY             # M13 · D13
    w = lore.whisper(th)
    assert w and "thirteenth-month" in w["omens"] and "thirteenth-day" in w["omens"]
    assert lore.whisper(858_000) is None                                # a quiet, ordinary day
    assert lore.whisper(th) == lore.whisper(th)                         # deterministic
    tw = lore.the_thirteenth_wallet()
    assert "book" in tw["shape"] and "game" in tw["shape"]
    assert "no real" in tw["note"].lower()                              # it disclaims itself


def test_clock_smoke():
    lines = bft.format_clock(858_000)
    assert any("Ordinal degree" in ln for ln in lines)
    assert any("Counting down" in ln for ln in lines)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  ok  {fn.__name__}")
    print(f"\n{len(fns)} tests passed")
    print("\n--- demo ---")
    for h in (0, 210_000, 840_000, 858_000, 1_260_000):
        print("\n".join(bft.format_clock(h)))
        print()
