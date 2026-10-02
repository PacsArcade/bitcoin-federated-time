// bft stamp: the stamp, with options that can pull ANY item. Mirrors py bft/stamping.py.
//   stamp(h)                                      "0018.07.13 16:10 a₿"       (strict: throws on a non-height)
//   face(h)                                       same, but a non-height gives "----.--.-- --:-- a₿"
//   stamp(h, { include: ["epoch", "moon"], at })  "0018.07.13 16:10 a₿ | epoch 480 | moon 🌖 Waning Gibbous"
//   stamp(h, { template: "{date} {time} {marker} #{heightc}" })
//   stamp(h, { json: true })                      the whole record as JSON
// The marker always follows the date and time. Extras come after, separated by " | ".
// Tokens: date time marker stamp datestamp height heightc year month day hour minute beat dayofyear
//   week weekofyear epoch retune retuneleft halving halvingpos halvingleft cycle subsidy animal moon ladder
//   json (mode only). The moon needs `at` (unix seconds, the real wall instant) or it prints "--".

import * as core from "./core.js";
import * as steps from "./steps.js";
import * as sky from "./sky.js";

export const DEFAULT_TEMPLATE = "{date} {time} {marker}";
export const DATE_ONLY_TEMPLATE = "{date} {marker}";
export const SEPARATOR = " | ";

export const TOKENS = [
  "date", "time", "marker", "stamp", "datestamp", "height", "heightc",
  "year", "month", "day", "hour", "minute", "beat", "dayofyear", "week", "weekofyear",
  "epoch", "retune", "retuneleft", "halving", "halvingpos", "halvingleft",
  "cycle", "subsidy", "animal", "moon", "ladder", "json",
];
const INITIAL_SUBSIDY_SATS = 5_000_000_000;

                               
                     
                           
                     
                                                   
                 
 

const pad = (n        , w        )         => String(n).padStart(w, "0");
const commas = (n        )         => n.toLocaleString("en-US");

function fmtBtc(sats        )         {
  const whole = Math.floor(sats / 100_000_000);
  const frac = sats % 100_000_000;
  return frac ? whole + "." + pad(frac, 8).replace(/0+$/, "") : String(whole);
}

export function values(h        , at                )                         {
  const f = core.fields(h);
  const d = core.date(h), t = core.time(h);
  const pos = h % core.DIFFICULTY_EPOCH_BLOCKS;
  const eraPos = h % core.HALVING_EPOCH_BLOCKS;
  const era = Math.floor(h / core.HALVING_EPOCH_BLOCKS);
  const sats = era < 64 ? Math.floor(INITIAL_SUBSIDY_SATS / 2 ** era) : 0;
  const animal = sky.yearAnimal(h);
  const moon = at == null ? "--" : (() => { const m = sky.moonPhase(at); return m.emoji + " " + m.name; })();
  return {
    date: d, time: t, marker: core.MARKER,
    stamp: d + " " + t + " " + core.MARKER, datestamp: d + " " + core.MARKER,
    height: String(h), heightc: commas(h),
    year: pad(f.year, 4), month: pad(f.month, 2), day: pad(f.day, 2),
    hour: pad(f.hour, 2), minute: pad(f.minute, 2), beat: String(f.beat),
    dayofyear: String(f.dayOfYear), week: String(f.weekOfMonth),
    weekofyear: String(Math.floor((f.dayOfYear - 1) / core.DAYS_PER_WEEK) + 1),
    epoch: String(f.diffEpoch),
    retune: pos + 1 + "/" + core.DIFFICULTY_EPOCH_BLOCKS,
    retuneleft: String(core.DIFFICULTY_EPOCH_BLOCKS - 1 - pos),
    halving: String(era), halvingpos: eraPos + 1 + "/" + core.HALVING_EPOCH_BLOCKS,
    halvingleft: String(core.HALVING_EPOCH_BLOCKS - 1 - eraPos),
    cycle: String(Math.floor(h / core.CYCLE_BLOCKS)), subsidy: fmtBtc(sats),
    ladder: steps.ladderLine(h),
    animal: animal.emoji + " " + animal.name, moon,
  };
}

function dashValues()                         {
  const v                         = {};
  for (const n of TOKENS) v[n] = "--";
  return Object.assign(v, {
    date: core.DASH_DATE, time: core.DASH_TIME, marker: core.MARKER,
    stamp: core.DASH_STAMP, datestamp: core.DASH_DATE_STAMP,
  });
}

/** The whole record: every token plus the full ladder. Dashes for a non-height. */
export function record(h         , at                ) {
  if (!core.isHeight(h)) return { height: null, known: false, values: dashValues(), ladder: null };
  return { height: h, known: true, values: values(h, at), ladder: steps.ladder(h) };
}

function sortKeys(x         )          {
  if (Array.isArray(x)) return x.map(sortKeys);
  if (x && typeof x === "object") {
    const o                          = {};
    for (const k of Object.keys(x          ).sort()) o[k] = sortKeys((x                           )[k]);
    return o;
  }
  return x;
}

function render(h         , o              )         {
  const vals = core.isHeight(h) ? values(h, o.at) : dashValues();
  const tpl = o.template != null ? o.template : o.dateOnly ? DATE_ONLY_TEMPLATE : DEFAULT_TEMPLATE;
  for (const m of tpl.matchAll(/\{([a-z]+)\}/g)) {
    if (!TOKENS.includes(m[1]) || m[1] === "json") throw new RangeError("unknown token {" + m[1] + "}");
  }
  const segs = [tpl.replace(/\{([a-z]+)\}/g, (_m, n        ) => vals[n])];
  for (const name of o.include ?? []) {
    if (!TOKENS.includes(name)) throw new RangeError("unknown item " + JSON.stringify(name) + " (one of " + TOKENS.join(", ") + ")");
    if (name === "json") throw new RangeError("'json' is a mode, not an item: use { json: true }");
    segs.push(["ladder", "stamp", "datestamp", "date", "time", "marker"].includes(name) ? vals[name] : name + " " + vals[name]);
  }
  return segs.join(SEPARATOR);
}

function out(h         , o              )         {
  if (o.json) {
    const rec = { ...record(h, o.at), stamp: render(h, o) };
    // same bytes as python json.dumps(sort_keys, ensure_ascii=False, separators=(",", ":"))
    return JSON.stringify(sortKeys(rec));
  }
  return render(h, o);
}

/** Strict stamp: throws RangeError on a non-height. */
export function stamp(height         , o               = {})         {
  core.check(height);
  return out(height, o);
}

/** Display stamp: a non-height gives the dash face. */
export function face(height         , o               = {})         {
  return out(height, o);
}
