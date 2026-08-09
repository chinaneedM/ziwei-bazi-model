# Ziwei Chart Engine V1 Foundation

## Status and scope

This document began as the first Ziwei chart-generation layer above the shared
Time/Calendar Foundation R1. The foundation core remains stable, while the
implementation has now grown upward through profile-bound core auxiliaries,
dependency-bound stars, external Wenmo compatibility discriminators and typed
Mingzhu/Shenzhu role bindings.

The chart layer consumes resolved civil/solar/calendar facts; it does not
duplicate timezone, astronomy, Chinese-calendar or Bazi logic.

Implemented:

- typed Z12 addresses and natal designation bindings;
- Ziwei natal-month coordinate handling under an explicit leap-month policy;
- Life and Body placement from natal month and apparent-solar birth hour;
- twelve-palace designation rebasing from Life;
- address stems by the Five Tigers rule;
- Life-palace Ganzhi -> NaYin -> Five Element Bureau;
- Ziwei anchor, Tianfu reflection and all fourteen main-star placements;
- profile-bound 文昌/文曲、左辅/右弼、天魁/天钺、天马、禄存/擎羊/陀罗、地空/地劫;
- Wenmo operational Fire/Bell compatibility as a separate rule family;
- dependency-bound 三台/八座 from 左辅/右弼 + lunar day;
- dependency-bound 恩光/天贵 from 文昌/文曲 + lunar day;
- typed `RoleBinding` facts for 命主/身主, separate from physical placements;
- a single immutable resolved calculation-profile snapshot binding exact
  Time/Calendar, auxiliary and role rule identities/versions before generation;
- typed generation/source provenance and machine-readable output schema;
- fail-closed propagation for unresolved time, profile, auxiliary or role cells.

Still outside the current implementation slice:

- the remaining reference/operational minor-star content pack;
- dignity annotations;
- transformations;
- Longsheng/Doctor and other rings;
- Daxian, Annual and Minor Limit frames;
- renderer/UI;
- general ChartDiff automation beyond the current frozen Wenmo fixtures;
- interpretation or prediction.

## Repository architecture

The implementation lives in `src/fortune_training/ziwei_chart/` and consumes
`src/fortune_training/calendar_foundation/`.

The chart layer never modifies `sources/canonical/`, `model-learning/`, training
state or prediction access controls.

The key fact-type separation is:

```text
Placement
  = an entity physically occupies one Z12 address

RoleBinding
  = an existing entity is designated for a role such as 命主/身主

DesignationBinding
  = a palace designation such as 命/兄弟/夫妻 is bound to an address
```

These objects are intentionally not interchangeable.

## Deterministic vertical path

```text
BirthInput
-> TimeCalendarFoundation
-> raw/effective calendar facts + local apparent solar datetime
-> profile-bound Ziwei chart coordinates
-> Life / Body
-> twelve designations + address stems
-> Life Palace Ganzhi -> NaYin -> Five Element Bureau
-> Ziwei anchor -> Tianfu reflection -> fourteen main stars
-> profile-bound core auxiliary placements
-> dependency-bound placements (三台/八座/恩光/天贵)
-> profile-bound role bindings (命主/身主)
-> immutable NatalChartState
```

A chart run requires a `ResolvedZiweiCalculationProfile`. Profile identity,
Time/Calendar policy registry version, selected policies, auxiliary rule set,
role rule set and algorithm versions are bound before generation. There is no
runtime fallback to an unnamed modern default.

## Canonical and compatibility authority

The deterministic canonical-bound portions are regression-bound to the frozen
Git `main` sources without changing them. Important S01 routes include:

- `ZZZA-PR-008` Life/Body placement;
- `ZZZA-PR-009` twelve-palace order;
- `ZZZA-PR-010` Five Tigers address stems;
- `ZZZA-PR-011` Life-palace NaYin -> Five Element Bureau;
- `ZZZA-PR-012` Ziwei placement;
- `ZZZA-PR-013` Tianfu placement;
- `ZZZA-PR-014` / `ZZZA-PR-015` fourteen-main-star relative geometry;
- `ZZZA-PR-052` 三台/八座;
- `ZZZA-PR-053` 恩光/天贵;
- `ZZZA-PR-054` 命主 table and source conflict note;
- `ZZZA-PR-055` 身主 table and source-field conflict note.

`tests/fixtures/ziwei-main-star-anchor-r1.json` is a test transcription of the
S01 30x5 Ziwei placement table; all 150 cells must match.

Wenmo fixtures are explicitly tagged
`EXTERNAL_COMPATIBILITY_ORACLE_NOT_CANONICAL_AUTHORITY`. They may establish an
operational compatibility profile or expose an engine defect, but they never
silently replace Git canonical source semantics.

Examples already encoded:

- Wenmo leap-month midpoint behavior is separate from raw lunar identity;
- Wenmo late-Zi rollover is a Ziwei calculation-profile policy, not a rewrite of
  physical/civil time;
- Wenmo 辛-year Kui/Yue ordering coexists with the strict QS ordering;
- historical China DST is preserved even where Wenmo appears to use fixed UTC+8;
- Wenmo Fire/Bell is a separately named operational rule family;
- the 2001-12-15 Wenmo fixture validates 命宫午 -> 命主破军 and
  birth-year巳 -> 身主天机 without collapsing those two coordinate bases.

## Validation

Current regression coverage includes:

- all 12 natal months x 12 birth-hour branches for Life/Body geometry;
- all 150 canonical Ziwei-anchor cells;
- Tianfu reflection and fourteen-main-star covariance;
- exhaustive small-domain core auxiliary tests;
- profile discrimination for leap month, late Zi and 辛-year Kui/Yue;
- four Fire/Bell year-trine classes and all-hour translation properties;
- canonical 三台/八座 and 恩光/天贵 source examples;
- all 12 命主 Life-palace branch cells;
- strict QS 子/午身主 ambiguity fail-closed behavior;
- Wenmo operational role compatibility;
- external Wenmo end-to-end fixtures including the 2001 辛巳 chart.

Run the full repository checks with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
fortune-train verify
```

Generate the original machine-readable foundation smoke example with:

```bash
PYTHONPATH=src python scripts/ziwei-chart-example.py
```

## Release boundary

Passing these stages still does **not** mean Ziwei Chart Engine V1 is complete.
The remaining V1 work includes the reference/operational content pack, dignity,
transformations, ring generators, temporal frames, integrity/hash completion,
renderer separation and wider operational compatibility regression.
