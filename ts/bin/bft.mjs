#!/usr/bin/env node
// bft: the command line (TypeScript build). Same commands, same output as `python -m bft.cli`.
//   bft stamp [HEIGHT] [--with a,b,c] [--fmt TEMPLATE] [--date-only] [--json] [--at UNIX] [--source] [--strict]
//   bft ladder [HEIGHT] [--json]
//   bft range UNIT INDEX | DATE      (DATE = 0018 | 0018.07 | 0018.07.13 | 0018.07.13T16)
//   bft tip | bft verify [VECTORS.json] | bft items
// No HEIGHT: read the tip (house beacon first, mempool.space to verify, else dashes).
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import * as bft from "../dist/index.js";
import { run } from "../dist/conformance.js";

const USAGE = readFileSync(fileURLToPath(import.meta.url), "utf8").split("\n").slice(1, 8).map((l) => l.replace(/^\/\/ ?/, "")).join("\n");

function parse(argv) {
  const pos = [], o = { with: [], fmt: null, dateOnly: false, json: false, at: null, source: false, strict: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--with") o.with.push(...argv[++i].split(",").filter(Boolean));
    else if (a === "--fmt") o.fmt = argv[++i];
    else if (a === "--at") o.at = Number(argv[++i]);
    else if (a === "--date-only") o.dateOnly = true;
    else if (a === "--json") o.json = true;
    else if (a === "--source") o.source = true;
    else if (a === "--strict") o.strict = true;
    else if (a.startsWith("--")) throw new RangeError("unknown flag " + a);
    else pos.push(a);
  }
  return [pos, o];
}

async function heightArg(pos) {
  if (pos.length) {
    const s = pos[0].replace(/[,_]/g, "");
    return [/^\d+$/.test(s) ? Number(s) : null, null];
  }
  const info = await bft.tip();
  return [info.height, info];
}

const commas = (n) => n.toLocaleString("en-US");

async function main(argv) {
  const [cmd, ...rest] = argv;
  if (!cmd || cmd === "-h" || cmd === "--help") { console.log(USAGE); return 0; }
  const [pos, o] = parse(rest);
  if (cmd === "stamp") {
    const [h, info] = await heightArg(pos);
    let at = o.at;
    if (at == null && info && h !== null && (o.with.includes("moon") || (o.fmt ?? "").includes("{moon}"))) at = Date.now() / 1000;
    console.log(bft.face(h, { include: o.with, template: o.fmt, dateOnly: o.dateOnly, at, json: o.json }));
    if (o.source && info) console.error("source: " + (info.source ?? "none") + " | " + info.note);
    return o.strict && h === null ? 2 : 0;
  }
  if (cmd === "ladder") {
    const [h] = await heightArg(pos);
    if (h === null) { console.log(bft.DASH_STAMP); return o.strict ? 2 : 0; }
    const lad = bft.ladder(h);
    if (o.json) { console.log(JSON.stringify(lad)); return 0; }
    console.log("block " + commas(h) + "  =  " + bft.stampCore(h));
    const W = [14, 20, 12, 12, 12];
    console.log("unit".padEnd(12) + ["n-th (0-based)", "this block is", "left after", "start", "end"].map((t, i) => " " + t.padStart(W[i])).join(""));
    for (const r of lad) {
      const cells = [commas(r.index), commas(r.position) + " of " + commas(r.of), commas(r.remaining), commas(r.start), commas(r.end)];
      console.log(r.unit.padEnd(12) + cells.map((c, i) => " " + c.padStart(W[i])).join(""));
    }
    return 0;
  }
  if (cmd === "range") {
    let r;
    if (pos.length === 2 && bft.UNIT_KEYS.includes(pos[0])) r = bft.unitRange(pos[0], Number(pos[1]));
    else if (pos.length === 1) {
      let [s, hh] = pos[0].split("T");
      const parts = s.split(".").map(Number);
      while (parts.length < 3) parts.push(null);
      r = bft.dateRange(parts[0], parts[1], parts[2], hh === undefined ? null : Number(hh));
    } else { console.log(USAGE); return 2; }
    console.log(o.json ? JSON.stringify(r) : r.unit + ": blocks " + commas(r.start) + " to " + commas(r.end) + " (" + commas(r.size) + " blocks)  " + r.first + "  to  " + r.last);
    return 0;
  }
  if (cmd === "tip") { const t = await bft.tip(); console.log(JSON.stringify(t)); return t.height === null ? 2 : 0; }
  if (cmd === "items") { console.log("items / tokens: " + bft.TOKENS.join(" ")); console.log("units: " + bft.UNIT_KEYS.join(" ")); return 0; }
  if (cmd === "verify") {
    const path = pos[0] ?? join(dirname(fileURLToPath(import.meta.url)), "..", "..", "vectors", "vectors.json");
    const fails = run(JSON.parse(readFileSync(path, "utf8")));
    for (const f of fails) console.log("FAIL " + f);
    console.log(path + ": " + fails.length + " failure(s)");
    return fails.length ? 1 : 0;
  }
  console.error("unknown command " + JSON.stringify(cmd) + "\n" + USAGE);
  return 2;
}

main(process.argv.slice(2)).then((c) => { process.exitCode = c; }, (e) => { console.error("bft: " + e.message); process.exitCode = 2; });
