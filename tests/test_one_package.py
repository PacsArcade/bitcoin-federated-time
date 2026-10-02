"""One-package tests: spec core, ladder, stamp, beacon, CLI, and the canonical vectors.
Pure stdlib. Run:  python tests/test_one_package.py   (or pytest)."""
import json
import os
import random
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
import bft  # noqa: E402
from bft import core, steps, stamping, beacon, conformance  # noqa: E402

VECTORS = os.path.join(ROOT, "vectors", "vectors.json")


def raises(fn, *a, **k):
    try:
        fn(*a, **k)
    except ValueError:
        return True
    return False


def test_all_vectors_pass():
    assert conformance.run(VECTORS) == []


def test_vector_counts():
    v = json.load(open(VECTORS, encoding="utf-8"))
    assert len(v["forward"]) >= 42 and len(v["inverse"]) >= 8 and len(v["invalid"]) >= 6


def test_core_strict_and_dashes():
    assert bft.stamp(969505) == "0018.07.13 16:10 a₿"
    assert bft.stamp(0) == "0000.01.01 00:00 a₿"                      # block 0 is valid
    assert bft.stamp(5241600) == "0100.01.01 00:00 a₿"                # 4-digit year
    assert core.date(52416 * 10000) == "10000.01.01"                  # never truncated
    for bad in (None, -1, 1.5, "969505", True, float("nan"), float("inf"), 2 ** 53):
        assert raises(bft.stamp, bad), bad
        assert bft.face(bad) == "----.--.-- --:-- a₿", bad
    assert bft.face(969505, date_only=True) == "0018.07.13 a₿"
    # no day 29, no month 14, ever
    for h in random.Random(1).sample(range(0, 6_000_000), 3000):
        f = core.fields(h)
        assert 1 <= f["day"] <= 28 and 1 <= f["month"] <= 13


def test_inverse_roundtrip():
    rng = random.Random(2)
    for _ in range(2000):
        h = rng.randrange(0, 6_000_000)
        f = core.fields(h)
        first = core.inverse(f["year"], f["month"], f["day"], f["hour"], f["minute"])
        assert first == h                                             # exact to the block
        assert core.inverse(f["year"], f["month"], f["day"]) == h - f["beat"]
    assert raises(core.inverse, 18, 14, 1) and raises(core.inverse, 18, 1, 29)
    assert raises(core.inverse, 18, 1, 1, 0, 5)


def test_ladder_matches_brute_force():
    """Independent re-derivation: every unit tiles the chain and nests as claimed."""
    sizes = {"block": 1, "hour": 6, "day": 144, "week": 1008, "retune": 2016, "month": 4032,
             "year": 52416, "halving": 210000, "cycle": 1260000}
    rng = random.Random(3)
    heights = [0, 1, 5, 6, 143, 144, 2015, 2016, 4031, 4032, 52415, 52416, 209999, 210000,
               969505, 1259999, 1260000] + [rng.randrange(0, 6_000_000) for _ in range(500)]
    for h in heights:
        lad = bft.ladder(h)
        assert [r["unit"] for r in lad] == list(sizes)
        by = {r["unit"]: r for r in lad}
        for u, s in sizes.items():
            r = by[u]
            lo = (h // s) * s
            assert (r["start"], r["end"], r["size"]) == (lo, lo + s - 1, s)
            assert r["position"] == h - lo + 1 and r["remaining"] == lo + s - 1 - h
            rr = steps.unit_range(u, r["index"])
            assert rr["start"] <= h <= rr["end"] and rr["end"] - rr["start"] + 1 == s
            if r["parent"]:
                p = by[r["parent"]["unit"]]
                assert r["parent"]["of"] * s == p["size"]
                assert r["parent"]["n"] == (r["start"] - p["start"]) // s + 1
    # the halving era does not divide a year: say so, in numbers
    assert 210000 % 52416 != 0 and 2016 * 26 == 52416 and 4032 * 13 == 52416


def test_ladder_named_cases():
    r = {x["unit"]: x for x in bft.ladder(969505)}
    assert (r["hour"]["position"], r["day"]["position"]) == (2, 98)
    assert r["retune"]["index"] == 480 and r["retune"]["untilNext"] == 191
    assert steps.unit_range("day", 6732)["start"] == 969408
    assert steps.date_range(18, 7)["start"] == 967680 and steps.date_range(18, 7)["end"] == 971711
    assert steps.date_range(18)["size"] == 52416
    assert raises(steps.unit_range, "fortnight", 1) and raises(bft.ladder, None)


def test_stamp_items_and_templates():
    assert bft.stamp(969505, include=["epoch"]) == "0018.07.13 16:10 a₿ | epoch 480"
    assert bft.stamp(969505, template="{date}T{time}") == "0018.07.13T16:10"
    assert "moon 🌖 Waning Gibbous" in bft.stamp(969505, include=["moon"], at=1790856000)
    assert bft.stamp(969505, include=["moon"]).endswith("moon --")     # no wall instant, no moon
    assert raises(bft.stamp, 969505, include=["nonsense"])
    assert raises(bft.stamp, 969505, template="{nonsense}")
    rec = json.loads(bft.stamp(969505, as_json=True))
    assert rec["known"] and rec["values"]["date"] == "0018.07.13" and len(rec["ladder"]) == 9
    dead = json.loads(bft.face(None, as_json=True))
    assert dead["known"] is False and dead["values"]["stamp"] == "----.--.-- --:-- a₿"
    assert bft.face(None, include=["epoch"]) == "----.--.-- --:-- a₿ | epoch --"


def test_tip_beacon_then_mempool_then_dashes():
    def f(table):
        return lambda url: table.get(url)
    both = beacon.tip(f({beacon.BEACON_URL: 969506, beacon.MEMPOOL_URL: 969506}))
    assert both["height"] == 969506 and both["source"] == "beacon" and both["gap"] == 0
    gap = beacon.tip(f({beacon.BEACON_URL: 969500, beacon.MEMPOOL_URL: 969506}))
    assert gap["height"] == 969500 and "GAP" in gap["note"]            # the house beacon is the reading
    only = beacon.tip(f({beacon.MEMPOOL_URL: 969506}))
    assert only["height"] == 969506 and only["source"] == "mempool"
    none = beacon.tip(f({}))
    assert none["height"] is None and bft.face(none["height"]) == "----.--.-- --:-- a₿"


def run_cli(*args):
    p = subprocess.run([sys.executable, "-m", "bft.cli"] + list(args), cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout.strip()


def test_cli():
    assert run_cli("stamp", "969505") == (0, "0018.07.13 16:10 a₿")
    assert run_cli("stamp", "969505", "--with", "epoch,retune")[1] == \
        "0018.07.13 16:10 a₿ | epoch 480 | retune 1826/2016"
    assert run_cli("stamp", "969505", "--fmt", "{date}")[1] == "0018.07.13"
    assert run_cli("stamp", "nope", "--strict") == (2, "----.--.-- --:-- a₿")
    assert json.loads(run_cli("stamp", "969505", "--json")[1])["height"] == 969505
    assert run_cli("ladder", "969505")[1].startswith("block 969,505  =  0018.07.13 16:10 a₿")
    assert "(6 blocks)" in run_cli("range", "0018.07.13T16")[1]
    assert run_cli("verify")[0] == 0


def test_python_and_typescript_clis_agree():
    """Same command, same bytes, both languages (skipped when node is absent)."""
    import shutil
    node = shutil.which("node")
    if not node:
        print("skip: no node")
        return
    cases = [["stamp", "969505"], ["stamp", "0"], ["stamp", "5241600", "--date-only"],
             ["stamp", "969505", "--with", "epoch,retune,retuneleft,halving,halvingpos,subsidy,animal,cycle"],
             ["stamp", "969505", "--with", "moon", "--at", "1790856000"],
             ["stamp", "969505", "--fmt", "{year}/{month}/{day} w{weekofyear} {heightc}"],
             ["stamp", "969505", "--json"], ["stamp", "969505", "--with", "ladder"],
             ["stamp", "garbage"], ["ladder", "969505"], ["ladder", "0", "--json"],
             ["range", "day", "6732"], ["range", "0018.07"], ["range", "0018.07.13T16"], ["range", "cycle", "3"]]
    for c in cases:
        py = run_cli(*c)
        p = subprocess.run([node, os.path.join(ROOT, "ts", "bin", "bft.mjs")] + c, capture_output=True,
                           text=True, encoding="utf-8")
        assert (p.returncode, p.stdout.strip()) == py, (c, py, p.stdout.strip(), p.stderr)


if __name__ == "__main__":
    n = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            n += 1
            print("ok", name)
    print("%d one-package tests passed" % n)
