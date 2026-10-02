// Run vectors/vectors.json against this TypeScript build. Returns a list of failures.
import * as core from "./core.ts";
import * as steps from "./steps.ts";
import * as stamping from "./stamp.ts";
import { liveFace } from "./live.ts";

function throws(fn: () => unknown): boolean {
  try { fn(); } catch { return true; }
  return false;
}

// vectors.json writes non-JSON numbers as strings
function invalidValue(v: unknown): unknown {
  if (v === "NaN") return NaN;
  if (v === "Infinity") return Infinity;
  if (v === "-Infinity") return -Infinity;
  return v;
}

function same(a: unknown, b: unknown): boolean {
  return JSON.stringify(a) === JSON.stringify(b);
}

export function run(v: any): string[] {
  const fails: string[] = [];
  const mine: Record<string, number> = {
    BLOCKS_PER_BEAT: 1, BLOCKS_PER_HOUR: core.BLOCKS_PER_HOUR, BLOCKS_PER_DAY: core.BLOCKS_PER_DAY,
    BLOCKS_PER_WEEK: core.BLOCKS_PER_WEEK, BLOCKS_PER_MONTH: core.BLOCKS_PER_MONTH, BLOCKS_PER_YEAR: core.BLOCKS_PER_YEAR,
    DAYS_PER_MONTH: core.DAYS_PER_MONTH, MONTHS_PER_YEAR: core.MONTHS_PER_YEAR, DAYS_PER_YEAR: core.DAYS_PER_YEAR,
    DIFFICULTY_EPOCH_BLOCKS: core.DIFFICULTY_EPOCH_BLOCKS, HALVING_EPOCH_BLOCKS: core.HALVING_EPOCH_BLOCKS,
    GENESIS_UNIX: 1231006505, SECONDS_PER_BLOCK: 600,
  };
  for (const [k, want] of Object.entries(v.constants)) if (mine[k] !== want) fails.push("constant " + k);
  for (const row of v.forward) {
    const h = row.height;
    const f = core.fields(h) as unknown as Record<string, number>;
    for (const key of ["year", "month", "day", "dayOfYear", "weekOfMonth", "beat", "hour", "minute", "diffEpoch"]) {
      if (f[key] !== row[key]) fails.push("forward " + h + " " + key + ": " + f[key] + " != " + row[key]);
    }
    const got: Array<[string, string]> = [["date", core.date(h)], ["time", core.time(h)],
      ["stamp", core.stampCore(h, false)], ["stampTime", core.stampCore(h, true)]];
    for (const [key, val] of got) if (val !== row[key]) fails.push("forward " + h + " " + key + ": " + val + " != " + row[key]);
  }
  for (const row of v.inverse) {
    const got = core.inverse(row.year, row.month, row.day);
    if (got !== row.firstHeight) fails.push("inverse " + JSON.stringify(row) + ": " + got);
  }
  for (const row of v.invalid) {
    const x = invalidValue(row.input);
    if (!throws(() => core.check(x))) fails.push("invalid " + JSON.stringify(row.input) + " should be rejected");
    if (core.faceCore(x) !== core.DASH_STAMP) fails.push("invalid " + JSON.stringify(row.input) + " display should be dashes");
    if (!throws(() => stamping.stamp(x))) fails.push("invalid " + JSON.stringify(row.input) + " strict stamp should throw");
    if (stamping.face(x) !== core.DASH_STAMP) fails.push("invalid " + JSON.stringify(row.input) + " face() should be dashes");
  }
  for (const row of v.ladder ?? []) {
    if (!same(steps.ladder(row.height), row.rungs)) fails.push("ladder " + row.height + " differs");
    if (steps.ladderLine(row.height) !== row.line) fails.push("ladderLine " + row.height);
  }
  for (const row of v.ranges ?? []) {
    const got = steps.unitRange(row.unit, row.index) as unknown as Record<string, number>;
    for (const key of ["start", "end", "size"]) if (got[key] !== row[key]) fails.push("range " + row.unit + " " + row.index + " " + key);
  }
  for (const row of v.dateRanges ?? []) {
    const got = steps.dateRange(...(row.args as [number, number?, number?, number?])) as unknown as Record<string, unknown>;
    for (const key of ["unit", "start", "end", "size"]) if (got[key] !== row[key]) fails.push("dateRange " + JSON.stringify(row.args) + " " + key);
  }
  for (const row of v.stamps ?? []) {
    const got = stamping.stamp(row.height, { include: row.include ?? [], template: row.template ?? null, dateOnly: row.dateOnly ?? false, at: row.at ?? null });
    if (got !== row.expected) fails.push("stamp " + JSON.stringify(row) + ": " + got);
  }
  for (const row of v.live ?? []) {
    const got = liveFace(row.height, row.arrivedAt, row.now, row.estimated);
    if (!same(got, row.expected)) fails.push("live " + row.name + ": " + JSON.stringify(got));
  }
  return fails;
}
