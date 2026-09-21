# work-claim — task-359 (BFT · one-moon correction, Lane A — the source of truth)

Lane: home crew (Number One sonnet sub-agent). Base = `bitcoin-federated-time` main
**80da35f8a530564fb8dd898e3f927b5df7c6b88f** ("the sky's moon — real synodic phase from the
2000-01-06 epoch (ruling 0018.05.18)"). Branch `feat/task-359-one-moon`. Worktree cut by
Number One at `~/dev/worktrees/task-359`. No ports (static package, no dev server). Brief:
`~/dev/home/inbox/TASK-359-bft-one-moon-lane-a.md`. RULED by Number One at verify, block
967,918.

**The Admiral's ruling (0018.07.02): "we only have one moon. and we can see it outside."**
The 28-day BFT month is a block count and never wears the moon's name. The moon is the
sky's, from wall time, labeled. This lane is the SOURCE OF TRUTH: later lanes (B mirrors,
C frens.earth, D onecocreation, E pacsarcade, F prose) copy this lane's corrected wording
and run its lint scripts.

`bft/sky.py`'s module docstring asserted a retired doctrine — "TWO moons," a block-timed
"calendar's moon" tied to day-of-month (D01 = new, D15 = full) — while its own `moon_phase()`
function already computed the sky's real synodic phase (ruling 0018.05.18). The docstring
was self-contradictory. This lane rewrites every surface (code prose, tests, docs, guides,
the two in-lane studies) that asserted the retired doctrine as fact, without changing any
function's logic, and ships two fleet-reusable lint scripts so lanes B–E can hold the same
line.

## OWNS (after the RULED exclusions)

- `bft/sky.py` (module docstring only — `moon_phase()`'s logic untouched)
- `bft/holidays.py` (feast-day names/stories: "New Year" — no longer "the new-moon new
  year"; "Year's End" no longer "completes with the moon")
- `bft/lore.py` (one whisper line rewritten — no logic change)
- `tests/test_bft.py` (`test_sky_moon_and_animals` lines 102–103 rewritten to the sky's
  actual computed phase; `test_holidays` line 126's string literal follows `holidays.py`)
- `README.md` (the "sky comes free" section, the display-standard "bitcoin's age" line, the
  drift line, the guide cross-references, the spark section)
- `CHANGELOG.md` (NEW dated entry only — additive, history untouched)
- `docs/the-two-moons.md` (REWRITTEN AS HISTORY — past-tense framing banner, body kept)
- `docs/degen-hours.md` (correction banner — the Day-0/new-moon proposal was never signed
  off and is now superseded by the one-moon ruling; body kept as design history)
- `docs/the-thirteen-seats.md` (the two-part drift line; the Day-0/moon cross-reference)
- `docs/bitcoin-holidays.md` (the New Year / Year's End rows; the Day-0 cross-reference)
- `docs/pupil-clock-grid.md` ("13 moons" → "13 months"; the bitcoin's-age line; two rows
  describing the still-uncorrected pupil study's calendar-moon feature, flagged pending)
- `guides/1-a-clock-made-of-blocks.md` (the ladder line: months not moons, block-years not
  age)
- `guides/2-the-months-and-the-moon.md` (RETITLED heading; "The moon comes free" section and
  the new-year line rewritten to one moon, the sky's)
- `guides/3-the-two-calendars.md`, `guides/4-the-hidden-thirteenth.md`, `guides/README.md`
  (cross-reference text only)
- `studies/index.html`, `studies/README.md` (words only — both non-dirty, in-lane; the two
  dirty studies are READ-ONLY, see below)
- `scripts/lint-one-moon.sh`, `scripts/one-moon-allowlist.txt` (NEW)
- `scripts/lint-finding1.sh`, `scripts/finding1-allowlist.txt` (NEW)
- `work-claims/task-359.md` (this file, first commit)

## READ-ONLY / out of this lane (the RULED exclusions)

- `studies/bitcoin-birthday.html`, `studies/clock-study-pupil.html` — the live clone carries
  someone's uncommitted edits to these; a worktree cut from `80da35f` doesn't contain them,
  and editing them here would collide. Follow-up pass once their owner commits.
- `docs/keep-time-simple.md` — untracked in the live clone, postdates every prior sweep;
  not in this worktree at all (git worktrees only carry committed history).
- `.claude/skills/bitcoin-time-clock/SKILL.md` — this repo's bundled copy stays Lane B's
  (T-360 mirrors from the canonical skill); read-only here so the two lanes don't both
  write it.
- `build/lib/bft/*`, `bitcoin_federated_time.egg-info/PKG-INFO` — generated output; no
  Python build toolchain (`pip`/`setuptools`/`build`) available in this sandbox, so neither
  regenerated nor hand-edited. Named exception, not a silent skip.

## Also out of scope (discovered at pickup, not in the brief's exclusion list)

- `DW-PRESS-REVIEW.md`, `DW-PRESS-VERBIAGE-REVIEW.md` — the brief asked for a one-line
  correction note at the top of each, but both files are `.gitignore`d at the repo root
  ("never ship these — Pac's ruling") and exist only in the live clone as untracked local
  files. They are not present in this git worktree, and creating them here would mean
  committing files the repo's own ruling says never to ship, plus this lane never touches
  the live clone. Flagged for the Admiral / a lane with live-clone access, not actioned.

## Never-delete law

Nothing removed. `docs/the-two-moons.md` gets a banner + past-tense framing, body kept
verbatim. `docs/degen-hours.md` gets a banner, body kept. `CHANGELOG.md`'s 0.2.0/0.3.0
entries untouched. `build/lib/` and the egg-info are neither regenerated nor deleted — that
choice is the Admiral's hand only.

## Gate

`python3 tests/test_bft.py` (the CI command, stdlib only) + `scripts/lint-one-moon.sh .` +
`scripts/lint-finding1.sh .`, run from the worktree root.
