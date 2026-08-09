# Ziwei Chart Engine V1 Foundation

## Status and scope

This phase is the first Ziwei chart-generation layer above the shared
Time/Calendar Foundation R1. It consumes resolved civil/solar/calendar facts;
it does not duplicate timezone, astronomy, Chinese-calendar or Bazi logic.

Implemented in this slice:

- typed Z12 addresses and natal designation bindings;
- Ziwei natal-month coordinate handling under an explicit leap-month policy;
- Life and Body placement from natal month and apparent-solar birth hour;
- twelve-palace designation rebasing from Life;
- address stems by the Five Tigers rule;
- Life-palace Ganzhi -> NaYin -> Five Element Bureau;
- Ziwei anchor from lunar birth day and bureau;
- Tianfu reflection from the Ziwei anchor;
- all fourteen main-star placements;
- a single immutable resolved calculation-profile snapshot binding the
  Time/Calendar policy registry and chart algorithm versions;
- typed generation trace for natal structure;
- fail-closed propagation when Time/Calendar cannot resolve a chart candidate.

Not implemented in this slice:

- auxiliary stars;
- dignity annotations;
- transformations;
- Longsheng/Doctor rings;
- Daxian, Annual and Minor Limit frames;
- renderer/UI;
- operational compatibility with any third-party software;
- interpretation or prediction.

## Repository architecture

The implementation lives in `src/fortune_training/ziwei_chart/` and consumes
`src/fortune_training/calendar_foundation/`.

The chart layer never modifies `sources/canonical/`, `model-learning/`, training
state or prediction access controls.

## Deterministic vertical path

```text
BirthInput
-> TimeCalendarFoundation
-> effective Ziwei lunar date + local apparent solar datetime
-> natal month coordinate + birth-hour Z12 coordinate
-> Life / Body
-> twelve designations + address stems
-> Life Palace Ganzhi
-> NaYin
-> Five Element Bureau
-> Ziwei anchor
-> Tianfu reflection
-> fourteen main-star placements
```

A chart run requires a `ResolvedZiweiCalculationProfile`. Profile identity,
Time/Calendar policy registry version, selected Time/Calendar policies and chart
algorithm versions are bound before generation. There is no runtime fallback to
an unnamed default.

## Canonical source binding

The current deterministic core is regression-bound to the frozen Git `main`
canonical source without changing it. Relevant S01 charting material includes:

- `ZZZA-PR-008` Life/Body placement;
- `ZZZA-PR-009` twelve-palace order;
- `ZZZA-PR-010` Five Tigers address stems;
- `ZZZA-PR-011` Life-palace NaYin -> Five Element Bureau;
- `ZZZA-PR-012` Ziwei placement;
- `ZZZA-PR-013` Tianfu placement;
- `ZZZA-PR-014` Ziwei system offsets;
- `ZZZA-PR-015` Tianfu system offsets.

`tests/fixtures/ziwei-main-star-anchor-r1.json` is a test transcription of the
S01 `T11R00-T11R30` 30x5 Ziwei placement table. The production algorithm is the
formula implementation; the fixture is the frozen Golden oracle. The test suite
requires all 150 cells to match.

## Validation

`tests/test_ziwei_chart_foundation.py` currently checks:

- all 12 natal months x 12 birth-hour branches for Life/Body geometry;
- Zi-hour `Life == Body == MonthAnchor`;
- the source example chain `甲年 + Life寅 -> 丙寅 -> 炉中火 -> 火六局`;
- leap-month policy scope without mutating the raw lunar month;
- all 150 cells of the canonical Ziwei anchor table;
- Tianfu reflection for all 12 Ziwei anchors;
- fourteen-main-star half-turn covariance;
- an end-to-end Beijing smoke chart;
- fail-closed calculation-profile registry-version mismatch.

Run the full repository checks with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
fortune-train verify
```

Generate the current machine-readable smoke example with:

```bash
PYTHONPATH=src python scripts/ziwei-chart-example.py
```

The smoke input is deliberately away from major time boundaries:

- male;
- 1994-05-17 14:30 reported civil time;
- Beijing, China;
- latitude 39.9042, longitude 116.4074;
- IANA zone `Asia/Shanghai`.

## Release boundary

Passing this foundation does **not** mean Ziwei Chart Engine V1 is complete.
It establishes only the first independently runnable vertical slice. The next
implementation stages add profile-bound auxiliary placements, annotations,
transformations, rings and temporal frames, followed by renderer separation and
third-party compatibility `ChartDiff` validation.
