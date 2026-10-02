// bft live face: minutes and seconds that tick from the last block. Mirrors py bft/live.py.
// A DISPLAY CONVENTION, not the standard: the canonical stamp stays height-only (HH:MM in 10s).
// The date, hour and 10-minute step come from the HEIGHT alone. The wall clock only measures the
// seconds since this block ARRIVED (when our node first saw it); it never makes a date.
//   elapsed >= 600 holds at step+9:59 ("straining"), never rolling into the next step until a real block lands.
//   now before arrival (clock skew) reads as 0. No arrival or no clock: no seconds, dashes: "16:1-:--".

import * as core from "./core.js";

export const HOLD_AT = 600;

                           
                 
               
                      
                        
                        
                         
                   
                 
                  
                     
 

const num = (x         )              => typeof x === "number" && Number.isFinite(x);
const p2 = (n        )         => String(n).padStart(2, "0");

export function liveFace(height         , arrivedAt         , now         , estimated = false)           {
  if (!core.isHeight(height)) {
    return { known: false, text: "----.--.-- --:--:-- " + core.MARKER, hour: null, minute: null, second: null,
      elapsed: null, holding: false, lateBy: 0, skewed: false, estimated };
  }
  const f = core.fields(height);
  const d = core.date(height), hh = p2(f.hour);
  if (!num(arrivedAt) || !num(now)) {
    return { known: true, text: d + " " + hh + ":" + f.minute / 10 + "-:-- " + core.MARKER, hour: f.hour, minute: null,
      second: null, elapsed: null, holding: false, lateBy: 0, skewed: false, estimated };
  }
  const raw = Math.floor(now - arrivedAt);
  const skewed = raw < 0;
  const e = Math.max(0, raw);
  const holding = e >= HOLD_AT;
  const shown = holding ? HOLD_AT - 1 : e;
  const minute = f.minute + Math.floor(shown / 60), second = shown % 60;
  return { known: true, text: d + " " + hh + ":" + p2(minute) + ":" + p2(second) + " " + core.MARKER, hour: f.hour,
    minute, second, elapsed: e, holding, lateBy: holding ? e - HOLD_AT : 0, skewed, estimated };
}
