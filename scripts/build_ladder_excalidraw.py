#!/usr/bin/env python3
"""Regenerate docs/bft-ladder.excalidraw: the step ladder, drawn.  Run: python3 scripts/build_ladder_excalidraw.py

Excalidraw's dark theme is an invert filter, so every color is pre-inverted (dark first) the same
way the house build.py does it (apps/wanderpac/design/excalidraw/build.py): the palette below is
what you SEE in dark mode. Opened in light mode the file looks inverted; that is the house trade.
Deterministic: fixed seeds and timestamp, standard library only.
"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import bft  # noqa: E402

# ---- house dark-first color transform (copied from the wanderpac build.py) -------------------
_HUE180 = [[-0.574, 1.430, 0.144], [0.426, 0.430, 0.144], [0.426, 1.430, -0.856]]


def _inv3(m):
    a, b, c = m[0]; d, e, f = m[1]; g, h, i = m[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    return [[(e * i - f * h) / det, (c * h - b * i) / det, (b * f - c * e) / det],
            [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det],
            [(d * h - e * g) / det, (b * g - a * h) / det, (a * e - b * d) / det]]


_INV = _inv3(_HUE180)


def dark_first(hex_color):
    if not (isinstance(hex_color, str) and len(hex_color) == 7 and hex_color[0] == "#"):
        return hex_color
    t = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    v = [sum(_INV[i][j] * t[j] for j in range(3)) for i in range(3)]
    f = [(0.93 - x) / 0.86 for x in v]
    return "#" + "".join("%02X" % round(255 * min(1, max(0, x))) for x in f)


BG, PANEL, TEXT, MUTED, LINE = "#0B0D12", "#131722", "#E8ECF4", "#A9B3C7", "#46506A"
COL = {"block": "#FFB347", "hour": "#7DD3FC", "day": "#86EFAC", "week": "#C4B5FD", "retune": "#F9A8D4",
       "month": "#FDE68A", "year": "#FCA5A5", "halving": "#93C5FD", "cycle": "#D8B4FE"}
FIXED_TS = 1790856000000
rng = random.Random("bft-ladder")
els = []


def _base(t, x, y, w, h, stroke, bg_color="transparent"):
    return {"id": "e%04d" % (len(els) + 1), "type": t, "x": x, "y": y, "width": w, "height": h, "angle": 0,
            "strokeColor": dark_first(stroke), "backgroundColor": dark_first(bg_color), "fillStyle": "solid",
            "strokeWidth": 2, "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [],
            "frameId": None, "index": "a%04d" % (len(els) + 1), "roundness": None, "strokeSharpness": "sharp",
            "seed": rng.randint(1, 2 ** 31), "version": 1, "versionNonce": rng.randint(1, 2 ** 31),
            "isDeleted": False, "boundElements": None, "updated": FIXED_TS, "link": None, "locked": False}


def rect(x, y, w, h, stroke, fill="transparent", rounded=True):
    e = _base("rectangle", x, y, w, h, stroke, fill)
    if rounded:
        e["roundness"] = {"type": 3}
    els.append(e)


def text(x, y, s, size=16, color=TEXT, align="left", w=None):
    lines = s.split("\n")
    width = w or max(len(l) for l in lines) * size * 0.58
    height = len(lines) * size * 1.25
    e = _base("text", x, y, width, height, color)
    e.update({"strokeWidth": 1, "text": s, "originalText": s, "fontSize": size, "fontFamily": 2,
              "textAlign": align, "verticalAlign": "top", "containerId": None, "autoResize": True,
              "lineHeight": 1.25, "baseline": round(height - 0.3 * size)})
    els.append(e)


def arrow(x, y, dx, dy, color=MUTED):
    e = _base("arrow", x, y, abs(dx) or 1, abs(dy) or 1, color)
    e.update({"points": [[0, 0], [dx, dy]], "lastCommittedPoint": None, "startBinding": None,
              "endBinding": None, "startArrowhead": None, "endArrowhead": "arrow"})
    els.append(e)


def centered(cx, y, s, size=16, color=TEXT):
    w = max(len(l) for l in s.split("\n")) * size * 0.58
    text(cx - w / 2, y, s, size, color, "center", w)


H = 969505
lad = {r["unit"]: r for r in bft.ladder(H)}

# canvas background panel
rect(0, 0, 1700, 980, LINE, BG, rounded=False)
text(40, 28, "The BFT step ladder", 34, TEXT)
text(40, 76, "One block is one rung. Every unit above it is a fixed run of blocks. From any height you can read every unit, and from any unit you can read its heights.", 17, MUTED)

# the staircase: seven nested units, each step taller than the last
CH = [("block", "Block", 1, "10 minutes"), ("hour", "Hour", 6, "1 hour"), ("day", "Day", 144, "24 hours"),
      ("week", "Week", 1008, "7 days"), ("retune", "Retune", 2016, "14 days"),
      ("month", "Month", 4032, "28 days"), ("year", "Year", 52416, "364 days, 13 months")]
RATIOS = ["x6", "x24", "x7", "x2", "x2", "x13"]
x0, base_y, step_w, gap = 40, 640, 190, 36
for i, (k, label, size, dur) in enumerate(CH):
    x = x0 + i * (step_w + gap)
    h = 90 + i * 62
    y = base_y - h
    rect(x, y, step_w, h, COL[k], PANEL)
    centered(x + step_w / 2, y + 12, label, 22, COL[k])
    centered(x + step_w / 2, y + 44, ("{:,} block" + ("" if size == 1 else "s")).format(size), 17, TEXT)
    centered(x + step_w / 2, y + 68, dur, 13, MUTED)
    r = lad[k]
    if h >= 140:
        centered(x + step_w / 2, y + h - 52, "this block is\n%s of %s" % ("{:,}".format(r["position"]), "{:,}".format(r["of"])), 15, COL[k])
    else:
        centered(x + step_w / 2, base_y + 10, "this block is %s of %s" % ("{:,}".format(r["position"]), "{:,}".format(r["of"])), 13, COL[k])
    if i < len(RATIOS):
        arrow(x + step_w + 4, base_y - h - 4 + 20, gap - 8, 0, MUTED)
        centered(x + step_w + gap / 2, base_y - h - 28 + 20, RATIOS[i], 15, TEXT)

# the other direction, said once
text(40, 700, "Down the ladder: first block of a unit = number x size.   Day 6,732 starts at 6,732 x 144 = 969,408 and ends at 969,551.", 17, TEXT)
text(40, 730, "Up the ladder: unit number = height // size.   969,505 // 144 = 6,732, so it is day 6,732 (0018.07.13).", 17, TEXT)
text(40, 760, "Exact calendar inverse:  first block of (year, month, day) = year x 52,416 + (month-1) x 4,032 + (day-1) x 144.", 17, TEXT)

# the side branch: halving era and cycle do not nest in the year
bx = 40
by = 810
rect(bx, by, 760, 140, COL["halving"], PANEL)
text(bx + 18, by + 12, "Halving era: 210,000 blocks (about 4 years)", 20, COL["halving"])
text(bx + 18, by + 44, "210,000 / 52,416 = 4.006 years. It does not divide a year evenly, so it is its own ruler.", 15, TEXT)
text(bx + 18, by + 70, "6 halving eras = 1 cycle = 1,260,000 blocks (about 24 years).", 15, TEXT)
text(bx + 18, by + 96, "This block: %s of 210,000 in era %d.   %s of 1,260,000 in cycle %d." % (
    "{:,}".format(lad["halving"]["position"]), lad["halving"]["index"],
    "{:,}".format(lad["cycle"]["position"]), lad["cycle"]["index"]), 15, COL["cycle"])

# the worked example
ex = 860
rect(ex, by, 800, 140, COL["block"], PANEL)
text(ex + 18, by + 12, "Example: block 969,505  =  %s" % bft.stamp(H), 20, COL["block"])
text(ex + 18, by + 44, "2 of 6 in its hour  |  98 of 144 in its day  |  818 of 1,008 in its week", 15, TEXT)
text(ex + 18, by + 70, "1,826 of 2,016 in its retune  |  1,826 of 4,032 in its month", 15, TEXT)
text(ex + 18, by + 96, "26,018 of 52,416 in its year (0018)  |  190 blocks until the next retune", 15, TEXT)

doc = {"type": "excalidraw", "version": 2, "source": "bitcoin-federated-time/scripts/build_ladder_excalidraw.py",
       "elements": els,
       "appState": {"viewBackgroundColor": dark_first(BG), "gridSize": None, "theme": "dark"}, "files": {}}
out = os.path.join(os.path.dirname(HERE), "docs", "bft-ladder.excalidraw")
json.dump(doc, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(out, "a").write("\n")
print("wrote", out, len(els), "elements")
