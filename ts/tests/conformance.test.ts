import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { run } from "../src/conformance.ts";
import * as bft from "../src/index.ts";

const vectors = JSON.parse(readFileSync(new URL("../../vectors/vectors.json", import.meta.url), "utf8"));

test("all canonical vectors pass", () => {
  assert.deepEqual(run(vectors), []);
});

test("42+ forward vectors, 8+ inverse, 6+ invalid", () => {
  assert.ok(vectors.forward.length >= 42 && vectors.inverse.length >= 8 && vectors.invalid.length >= 6);
});

test("strict and display", () => {
  assert.equal(bft.stamp(969505), "0018.07.13 16:10 a₿");
  assert.equal(bft.stamp(0), "0000.01.01 00:00 a₿");
  assert.equal(bft.date(52416 * 10000), "10000.01.01");
  for (const bad of [null, undefined, -1, 1.5, "969505", true, NaN, Infinity, 2 ** 53]) {
    assert.throws(() => bft.stamp(bad), RangeError);
    assert.equal(bft.face(bad), "----.--.-- --:-- a₿");
  }
});

test("ladder matches brute force", () => {
  const sizes = { block: 1, hour: 6, day: 144, week: 1008, retune: 2016, month: 4032, year: 52416, halving: 210000, cycle: 1260000 };
  let seed = 12345;
  const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) % 6_000_000;
  const hs = [0, 1, 5, 6, 143, 144, 2015, 2016, 4032, 52416, 209999, 210000, 969505, 1260000];
  for (let i = 0; i < 500; i++) hs.push(rnd());
  for (const h of hs) {
    const by = Object.fromEntries(bft.ladder(h).map((r) => [r.unit, r]));
    for (const [u, s] of Object.entries(sizes)) {
      const r = by[u], lo = Math.floor(h / s) * s;
      assert.deepEqual([r.start, r.end, r.position, r.remaining], [lo, lo + s - 1, h - lo + 1, lo + s - 1 - h]);
      const rr = bft.unitRange(u as bft.UnitKey, r.index);
      assert.ok(rr.start <= h && h <= rr.end && rr.end - rr.start + 1 === s);
      if (r.parent) {
        const p = by[r.parent.unit];
        assert.equal(r.parent.of * s, p.size);
        assert.equal(r.parent.n, (r.start - p.start) / s + 1);
      }
    }
  }
});

test("inverse round trip, no day 29, no month 14", () => {
  for (let h = 0; h < 6_000_000; h += 997) {
    const f = bft.fields(h);
    assert.ok(f.day >= 1 && f.day <= 28 && f.month >= 1 && f.month <= 13);
    assert.equal(bft.inverse(f.year, f.month, f.day, f.hour, f.minute), h);
  }
  assert.throws(() => bft.inverse(18, 14, 1));
  assert.throws(() => bft.inverse(18, 1, 29));
});

test("stamp items, templates, json", () => {
  assert.equal(bft.stamp(969505, { include: ["epoch"] }), "0018.07.13 16:10 a₿ | epoch 480");
  assert.equal(bft.stamp(969505, { template: "{date}T{time}" }), "0018.07.13T16:10");
  assert.ok(bft.stamp(969505, { include: ["moon"], at: 1790856000 }).endsWith("moon 🌖 Waning Gibbous"));
  assert.ok(bft.stamp(969505, { include: ["moon"] }).endsWith("moon --"));
  assert.throws(() => bft.stamp(969505, { include: ["nonsense"] }));
  assert.throws(() => bft.stamp(969505, { template: "{nonsense}" }));
  const rec = JSON.parse(bft.stamp(969505, { json: true }));
  assert.equal(rec.values.date, "0018.07.13");
  assert.equal(rec.ladder.length, 9);
  assert.equal(bft.face(null, { include: ["epoch"] }), "----.--.-- --:-- a₿ | epoch --");
});

test("json bytes equal python's (the cross-language referee)", () => {
  // value printed by: python3 -c "import bft;print(bft.stamp(969505,as_json=True))"
  const expected = readFileSync(new URL("../../vectors/json-969505.txt", import.meta.url), "utf8").trim();
  assert.equal(bft.stamp(969505, { json: true }), expected);
});

test("tip: beacon, then mempool, then dashes", async () => {
  const f = (t: Record<string, number>) => async (u: string) => t[u] ?? null;
  const B = bft.BEACON_URL, M = bft.MEMPOOL_URL;
  assert.deepEqual((await bft.tip(f({ [B]: 969506, [M]: 969506 }))).source, "beacon");
  const gap = await bft.tip(f({ [B]: 969500, [M]: 969506 }));
  assert.ok(gap.height === 969500 && gap.note.includes("GAP"));
  assert.equal((await bft.tip(f({ [M]: 969506 }))).source, "mempool");
  assert.equal((await bft.tip(f({}))).height, null);
});
