// bft core: the frozen spec core (spec/BFT-SPEC.md). Pure integer math, no network, no clock.
// A height in, a reading out. Strict API throws on a non-height; face() returns the dash faces.
// Must stay byte-for-byte equivalent to py bft/core.py: both run vectors/vectors.json.

export const MARKER = "a₿"; // a₿
export const BLOCKS_PER_HOUR = 6;
export const BLOCKS_PER_DAY = 144;
export const DAYS_PER_WEEK = 7;
export const BLOCKS_PER_WEEK = 1008;
export const DAYS_PER_MONTH = 28;
export const MONTHS_PER_YEAR = 13;
export const DAYS_PER_YEAR = 364;
export const BLOCKS_PER_MONTH = 4032;
export const BLOCKS_PER_YEAR = 52416;
export const DIFFICULTY_EPOCH_BLOCKS = 2016; // a "retune"
export const HALVING_EPOCH_BLOCKS = 210000;
export const CYCLE_BLOCKS = 1260000;

export const DASH_DATE = "----.--.--";
export const DASH_TIME = "--:--";
export const DASH_STAMP = DASH_DATE + " " + DASH_TIME + " " + MARKER;
export const DASH_DATE_STAMP = DASH_DATE + " " + MARKER;

                         
                 
               
                
              
                    
                      
               
               
                 
                    
 

const pad = (n        , w        )         => String(n).padStart(w, "0");

/** True only for a real non-negative safe integer. Strings, floats, NaN, null are not heights. */
export function isHeight(h         )              {
  return typeof h === "number" && Number.isSafeInteger(h) && h >= 0;
}

/** Strict gate: returns h or throws RangeError. Nothing is coerced. */
export function check(h         )         {
  if (!isHeight(h)) throw new RangeError("not a height: " + String(h) + " (a height is a non-negative safe integer)");
  return h;
}

export function fields(h        )         {
  check(h);
  const dayIndex = Math.floor(h / BLOCKS_PER_DAY);
  const beat = h % BLOCKS_PER_DAY;
  const doy = dayIndex % DAYS_PER_YEAR;
  return {
    height: h,
    year: Math.floor(dayIndex / DAYS_PER_YEAR),
    month: Math.floor(doy / DAYS_PER_MONTH) + 1,
    day: (doy % DAYS_PER_MONTH) + 1,
    dayOfYear: doy + 1,
    weekOfMonth: Math.floor((doy % DAYS_PER_MONTH) / DAYS_PER_WEEK) + 1,
    beat,
    hour: Math.floor(beat / BLOCKS_PER_HOUR),
    minute: (beat % BLOCKS_PER_HOUR) * 10,
    diffEpoch: Math.floor(h / DIFFICULTY_EPOCH_BLOCKS),
  };
}

export function date(h        )         {
  const f = fields(h);
  return pad(f.year, 4) + "." + pad(f.month, 2) + "." + pad(f.day, 2);
}

export function time(h        )         {
  const f = fields(h);
  return pad(f.hour, 2) + ":" + pad(f.minute, 2);
}

/** The canonical stamp: "YYYY.MM.DD HH:MM a₿", or date only "YYYY.MM.DD a₿". Strict. */
export function stampCore(h        , withTime = true)         {
  return withTime ? date(h) + " " + time(h) + " " + MARKER : date(h) + " " + MARKER;
}

/** Display variant: a real height renders, anything else is the dash face. Never throws. */
export function faceCore(h         , withTime = true)         {
  if (!isHeight(h)) return withTime ? DASH_STAMP : DASH_DATE_STAMP;
  return stampCore(h, withTime);
}

function inRange(name        , v         , lo        , hi        )         {
  if (typeof v !== "number" || !Number.isSafeInteger(v) || v < lo || v > hi) {
    throw new RangeError(name + " out of range: " + String(v));
  }
  return v;
}

/** First block of a BFT moment, exact. Defaults to the start of the month/day/hour given. */
export function inverse(year        , month = 1, day = 1, hour = 0, minute = 0)         {
  inRange("year", year, 0, Number.MAX_SAFE_INTEGER);
  inRange("month", month, 1, MONTHS_PER_YEAR);
  inRange("day", day, 1, DAYS_PER_MONTH);
  inRange("hour", hour, 0, 23);
  inRange("minute", minute, 0, 50);
  if (minute % 10) throw new RangeError("minute must be a multiple of 10: " + minute);
  return check(
    year * BLOCKS_PER_YEAR + (month - 1) * BLOCKS_PER_MONTH + (day - 1) * BLOCKS_PER_DAY +
      hour * BLOCKS_PER_HOUR + minute / 10,
  );
}
