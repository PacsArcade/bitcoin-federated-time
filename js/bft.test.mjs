// The inscription build against vectors/vectors.json. Run: node --test js/
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const src = readFileSync(new URL("./bft.js", import.meta.url), "utf8");
const bft = vm.runInNewContext(src + "\n;bft", { RangeError, Number, String, Math });
const v = JSON.parse(readFileSync(new URL("../vectors/vectors.json", import.meta.url), "utf8"));

test("file is inscription-sized and dependency free", () => {
  assert.ok(Buffer.byteLength(src) < 400, "bytes: " + Buffer.byteLength(src));
  assert.ok(!/fetch|Date|import|require/.test(src));
});

test("every forward vector: date and time stamp", () => {
  assert.ok(v.forward.length >= 42);
  for (const r of v.forward) assert.equal(bft(r.height), r.stampTime, "height " + r.height);
});

test("every invalid input throws", () => {
  for (const r of v.invalid) {
    const x = r.input === "NaN" ? NaN : r.input === "Infinity" ? Infinity : r.input === "-Infinity" ? -Infinity : r.input;
    assert.throws(() => bft(x), RangeError, JSON.stringify(r.input));
  }
});

test("inverse vectors land on midnight of that day", () => {
  for (const r of v.inverse) assert.equal(bft(r.firstHeight), String(r.year).padStart(4, "0") + "." + String(r.month).padStart(2, "0") + "." + String(r.day).padStart(2, "0") + " 00:00 a₿");
});
