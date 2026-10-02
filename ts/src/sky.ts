// bft sky extension: the sky's moon (real synodic phase, from wall time) and the thirteen animals.
// Mirrors py bft/sky.py. Optional: the core never imports this.

import * as core from "./core.ts";

export const MOON_PHASES: Array<[string, string]> = [
  ["\u{1F311}", "New"], ["\u{1F312}", "Waxing Crescent"], ["\u{1F313}", "First Quarter"], ["\u{1F314}", "Waxing Gibbous"],
  ["\u{1F315}", "Full"], ["\u{1F316}", "Waning Gibbous"], ["\u{1F317}", "Last Quarter"], ["\u{1F318}", "Waning Crescent"],
];
export const YEAR_ANIMALS: Array<[string, string]> = [
  ["\u{1F400}", "Rat"], ["\u{1F402}", "Ox"], ["\u{1F405}", "Tiger"], ["\u{1F407}", "Rabbit"], ["\u{1F409}", "Dragon"],
  ["\u{1F40D}", "Snake"], ["\u{1F40E}", "Horse"], ["\u{1F410}", "Goat"], ["\u{1F412}", "Monkey"], ["\u{1F413}", "Rooster"],
  ["\u{1F415}", "Dog"], ["\u{1F416}", "Pig"], ["\u{1F408}", "Astronomical Cat"],
];
const SYNODIC_DAYS = 29.530588853;
const NEW_MOON_EPOCH_S = 947182440; // 2000-01-06 18:14 UTC

/** The sky's moon at wall instant `atTs` (unix seconds). The core never reads a clock: pass it in. */
export function moonPhase(atTs: number): { index: number; emoji: string; name: string; illumination: number } {
  const raw = (atTs - NEW_MOON_EPOCH_S) / 86400;
  const age = ((raw % SYNODIC_DAYS) + SYNODIC_DAYS) % SYNODIC_DAYS;
  const frac = age / SYNODIC_DAYS;
  const index = Math.round(frac * 8) % 8;
  const [emoji, name] = MOON_PHASES[index];
  return { index, emoji, name, illumination: Math.round(((1 - Math.cos(2 * Math.PI * frac)) / 2) * 1000) / 1000 };
}

/** The 13-animal sign for the BFT year (the twelve plus the Cat). Year 0 = Ox. */
export function yearAnimal(h: number): { emoji: string; name: string } {
  const [emoji, name] = YEAR_ANIMALS[(core.fields(h).year + 1) % 13];
  return { emoji, name };
}
