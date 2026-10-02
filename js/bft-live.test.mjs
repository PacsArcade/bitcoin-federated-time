// The inscription live face against vectors/vectors.json (live section), plus the watcher with a fake clock and fetch.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const src = readFileSync(new URL("./bft-live.js", import.meta.url), "utf8");
const ctx = vm.runInNewContext(src + "\n;({bftLive,bftWatch})", { Number, String, Math, isFinite, JSON, Promise, setInterval: () => 0 });
const { bftLive, bftWatch } = ctx;
const v = JSON.parse(readFileSync(new URL("../vectors/vectors.json", import.meta.url), "utf8"));
const plain = (o) => JSON.parse(JSON.stringify(o));

test("every live vector", () => {
  assert.ok(v.live.length >= 15);
  for (const r of v.live) assert.deepEqual(plain(bftLive(r.height, r.arrivedAt, r.now, r.estimated)), r.expected, r.name);
});

test("watcher: cold load is estimated and clamped, a change is first-seen, never the header otherwise", async () => {
  let t = 10_000, height = "969505", headerTime = 10_000 - 4000; // header says 4000 s old: clamp to 599
  const fetchFake = async (u) => u === "/r/blockheight"
    ? { text: async () => height }
    : { json: async () => ({ timestamp: headerTime }) };
  const out = [];
  const w = bftWatch((f, h) => out.push([h, f]), { fetch: fetchFake, now: () => t, manual: true });
  await w.poll(); w.draw();
  assert.equal(out[0][1].elapsed, 599);
  assert.equal(out[0][1].estimated, true);
  assert.equal(out[0][1].holding, false);
  t += 30; w.draw();
  assert.equal(out[1][1].elapsed, 629); // 599 + 30: the clamp was an estimate, now it is late and holds
  assert.equal(out[1][1].holding, true);
  t += 5; height = "969506"; await w.poll(); w.draw();           // a real change: arrival = the moment seen
  assert.equal(out[2][0], 969506);
  assert.equal(out[2][1].elapsed, 0);
  assert.equal(out[2][1].estimated, false);
  t += 75; w.draw();
  assert.equal(out[3][1].text, "0018.07.13 16:21:15 a₿"); // 969506 = 16:20 step, 75 s in
  assert.equal(out[3][1].holding, false);
});

test("watcher: no header and no change: dashes, never invented", async () => {
  const fetchFake = async (u) => { if (u === "/r/blockheight") return { text: async () => "969505" }; throw new Error("blocked"); };
  const out = [];
  const w = bftWatch((f) => out.push(f), { fetch: fetchFake, now: () => 1, manual: true });
  await w.poll(); w.draw();
  assert.equal(out[0].second, null);
  assert.ok(out[0].text.endsWith("16:1-:-- a₿"));
});

test("file is dependency free", () => assert.ok(!/require|import\(|eval/.test(src)));
