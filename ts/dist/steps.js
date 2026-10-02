// bft steps: the step ladder. From a block height to ANY time unit, and back.
//   block 1 -> hour 6 -> day 144 -> week 1,008 -> retune 2,016 -> month 4,032 -> year 52,416
//   halving era 210,000 -> cycle 1,260,000
// Week, retune, month, year nest exactly (2 weeks = retune, 2 retunes = month, 13 months = year).
// The halving era does not divide a year (about 4.006 years): its own ruler. 6 eras = 1 cycle.
// Mirrors py bft/steps.py; vectors/vectors.json is the referee.

import * as core from "./core.js";
import { check } from "./core.js";

                                                                                                            

                          
               
                
               
                         
 

export const UNITS            = [
  { key: "block", label: "Block", size: 1, parent: "hour" },
  { key: "hour", label: "Hour", size: core.BLOCKS_PER_HOUR, parent: "day" },
  { key: "day", label: "Day", size: core.BLOCKS_PER_DAY, parent: "week" },
  { key: "week", label: "Week", size: core.BLOCKS_PER_WEEK, parent: "retune" },
  { key: "retune", label: "Retune", size: core.DIFFICULTY_EPOCH_BLOCKS, parent: "month" },
  { key: "month", label: "Month", size: core.BLOCKS_PER_MONTH, parent: "year" },
  { key: "year", label: "Year", size: core.BLOCKS_PER_YEAR, parent: null },
  { key: "halving", label: "Halving era", size: core.HALVING_EPOCH_BLOCKS, parent: "cycle" },
  { key: "cycle", label: "Cycle", size: core.CYCLE_BLOCKS, parent: null },
];
export const UNIT_KEYS            = UNITS.map((u) => u.key);

                       
                
                
               
                                                             
               
                
              
                                                                       
             
                                                             
                                                        
              
                                                          
 

                        
                
                 
                 
               
                
              
                
               
 

function def(key        )          {
  const d = UNITS.find((u) => u.key === key);
  if (!d) throw new RangeError("unknown unit " + JSON.stringify(key) + " (one of " + UNIT_KEYS.join(", ") + ")");
  return d;
}

const p = (n        , w        )         => String(n).padStart(w, "0");
const commas = (n        )         => n.toLocaleString("en-US");

function nameOf(key         , h        , index        )         {
  const f = core.fields(h);
  switch (key) {
    case "block": return "block " + h;
    case "hour": return p(f.hour, 2) + ":00 on " + core.date(h);
    case "day": return core.date(h);
    case "week": return "week " + f.weekOfMonth + " of month " + p(f.month, 2) + ", year " + p(f.year, 4);
    case "retune": return "retune " + index;
    case "month": return p(f.year, 4) + "." + p(f.month, 2);
    case "year": return p(f.year, 4);
    case "halving": return "halving era " + index;
    default: return "cycle " + index;
  }
}

/** One rung of the ladder for height h. */
export function rung(key         , h        )       {
  check(h);
  const d = def(key);
  const index = Math.floor(h / d.size);
  const start = index * d.size;
  const end = start + d.size - 1;
  let parent                 = null;
  if (d.parent) {
    const ratio = def(d.parent).size / d.size;
    parent = { unit: d.parent, n: (index % ratio) + 1, of: ratio };
  }
  return {
    unit: d.key, label: d.label, size: d.size, index, name: nameOf(d.key, h, index),
    start, end, position: h - start + 1, of: d.size, remaining: end - h, untilNext: end + 1 - h,
    pct: Math.floor((20000 * (h - start + 1) + d.size) / (2 * d.size)) / 100, parent,
  };
}

/** Every unit at once, smallest to largest. */
export function ladder(h        )         {
  check(h);
  return UNIT_KEYS.map((k) => rung(k, h));
}

/** "2 of 6 in hour | 98 of 144 in day | ..." for every unit above the block. */
export function ladderLine(h        )         {
  return ladder(h).slice(1).map((r) => commas(r.position) + " of " + commas(r.of) + " in " + r.unit).join(" | ");
}

/** Which unit number (0-based from genesis) the height is in. */
export function unitAt(unit         , h        )         {
  return Math.floor(check(h) / def(unit).size);
}

/** The way back down: the first and last height of the n-th unit (0-based). */
export function unitRange(unit         , index        )        {
  const d = def(unit);
  if (typeof index !== "number" || !Number.isSafeInteger(index) || index < 0) {
    throw new RangeError("unit index must be a non-negative integer: " + String(index));
  }
  const start = index * d.size;
  const end = start + d.size - 1;
  check(end);
  return { unit, label: d.label, index, size: d.size, start, end, first: core.stampCore(start), last: core.stampCore(end) };
}

/** Height range of a calendar slot: year; year+month; year+month+day; or all four (hour). */
export function dateRange(year        , month                , day                , hour                )        {
  let unit         , size        , start        ;
  if (month == null) { unit = "year"; size = core.BLOCKS_PER_YEAR; start = core.inverse(year); }
  else if (day == null) { unit = "month"; size = core.BLOCKS_PER_MONTH; start = core.inverse(year, month); }
  else if (hour == null) { unit = "day"; size = core.BLOCKS_PER_DAY; start = core.inverse(year, month, day); }
  else { unit = "hour"; size = core.BLOCKS_PER_HOUR; start = core.inverse(year, month, day, hour); }
  const end = start + size - 1;
  return { unit, size, start, end, first: core.stampCore(start), last: core.stampCore(end) };
}
