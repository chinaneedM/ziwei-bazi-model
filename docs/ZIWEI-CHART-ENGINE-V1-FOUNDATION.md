# Ziwei Chart Engine V1 Foundation

## Status and scope

This document began as the first Ziwei chart-generation layer above the shared
Time/Calendar Foundation R1. The foundation core remains stable while the
implementation has grown upward through operational content, typed rings and a
reusable transformation runtime.

The chart layer consumes resolved civil/solar/calendar facts; it does not
duplicate timezone, astronomy, Chinese-calendar or Bazi logic.

Implemented:

- typed Z12 addresses and natal designation bindings;
- Ziwei natal-month coordinate handling under explicit profile policy;
- Life and Body placement, twelve-palace rebasing and address stems;
- Life-palace Ganzhi -> NaYin -> Five Element Bureau;
- Ziwei anchor, Tianfu reflection and all fourteen main-star placements;
- profile-bound core auxiliaries, including a separate Wenmo Fire/Bell family;
- dependency-bound 三台/八座 and 恩光/天贵;
- a 35-entity Wenmo operational minor-star content pack;
- typed `RoleBinding` facts for 命主/身主, separate from physical placements;
- typed `RingInstance` / `RingMemberBinding` state for 长生、岁前、将前、博士;
- typed `TransformationActivation` facts using S08's current 40-assignment table;
- a reusable transformation generator whose context is explicit, so future
  palace-stem, Daxian, annual and monthly layers can reuse one mechanism without
  moving physical stars;
- a single immutable resolved calculation-profile snapshot binding exact
  Time/Calendar, auxiliary, minor-star, transformation, ring and role identities;
- typed provenance, machine-readable schema and fail-closed diagnostics.

Still outside the current implementation slice:

- unresolved operational content such as 天寿 and the 天伤/天使 profile split;
- a complete operational Dignity registry;
- Daxian, Annual and Minor Limit temporal frames;
- integrity/hash completion;
- renderer/UI;
- general ChartDiff automation beyond frozen Wenmo fixtures;
- interpretation or prediction.

## Fact-type boundaries

The implementation lives in `src/fortune_training/ziwei_chart/` and consumes
`src/fortune_training/calendar_foundation/`.

```text
Placement
  = one physical entity occupies one Z12 address

TransformationActivation
  = one causal stem/layer activates 禄/权/科/忌 on an existing physical entity;
    the activation references the entity's immutable address and never moves it

RoleBinding
  = an existing entity is designated for a role such as 命主/身主

RingInstance / RingMemberBinding
  = cyclic ring state; same-label ring members are not physical Placement facts

DesignationBinding
  = a palace designation such as 命/兄弟/夫妻 is bound to an address
```

These objects are intentionally not interchangeable. In particular, physical
华盖 and 将前华盖, or physical 大耗 and 博士环大耗, may coexist without entity
collapse.

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
-> dependency-bound placements
-> operational minor-star placements when explicitly enabled
-> TransformationActivation overlay when explicitly enabled
-> Ring state when explicitly enabled
-> RoleBinding state when explicitly enabled
-> immutable NatalChartState
```

There is no runtime fallback to an unnamed modern default. Every optional
content family is either fully bound by the resolved profile or disabled.

## Canonical and compatibility authority

Canonical-backed deterministic rules remain bound to Git `main` sources without
modifying them. Important S01 routes include:

- `ZZZA-PR-008` Life/Body;
- `ZZZA-PR-009` twelve-palace order;
- `ZZZA-PR-010` address stems;
- `ZZZA-PR-011` NaYin -> Five Element Bureau;
- `ZZZA-PR-012` Ziwei placement;
- `ZZZA-PR-013` Tianfu placement;
- `ZZZA-PR-014` / `ZZZA-PR-015` fourteen-main-star geometry;
- `ZZZA-PR-052` 三台/八座;
- `ZZZA-PR-053` 恩光/天贵;
- `ZZZA-PR-054` 命主;
- `ZZZA-PR-055` 身主;
- `ZZZA-PR-057` through `ZZZA-PR-060` the four current ring families.

S08's explicit `唯一运行四化表` supplies the current 10-stem / 40-assignment
transformation registry. The runtime preserves all assignment identities and 39
mechanism identities rather than flattening them into display strings.

Wenmo fixtures are explicitly tagged
`EXTERNAL_COMPATIBILITY_ORACLE_NOT_CANONICAL_AUTHORITY`. They may establish an
operational profile or expose an engine defect, but they never silently replace
Git canonical semantics.

The 2001-12-15 辛巳 fixture now externally checks, among other things:

- Fire/Bell for the 巳酉丑 trine class;
- 三台、八座、恩光、天贵;
- 命主破军 / 身主天机;
- 35 operational minor-star placements;
- all four rings and 48 ring members;
- natal 辛四化: 巨门禄、太阳权、文曲科、文昌忌.

## Dignity release blocker

Dignity remains an operational-content blocker, not an architecture blocker.
S05 defines brightness semantics and S06 contains many historical brightness
predicates, but the current Git canonical corpus does not expose one complete
deterministic seven-grade operational matrix matching every required
entity/address cell. The engine therefore must not infer missing cells from
absence or from one Wenmo chart. GitHub issue #180 tracks explicit registry
closure and optimized compatibility calibration.

## Validation

Regression coverage includes:

- all 12 natal months x 12 birth-hour branches for Life/Body geometry;
- all 150 canonical Ziwei-anchor cells;
- Tianfu reflection and fourteen-main-star covariance;
- exhaustive core auxiliary, Fire/Bell and operational minor-star domains;
- all 60 valid sexagenary Xunkong pairs;
- canonical dependency-star examples;
- role-profile discrimination and fail-closed ambiguities;
- all five Changsheng anchors, all TaiSui/Jiangqian branch domains and Boshi
  Lucun dependency;
- exact four-ring / 48-member Wenmo regression;
- all 10 transformation stems x four ordered assignments;
- exactly 40 transformation assignments and 39 mechanism identities;
- missing/duplicate transformation-target fail-closed behavior;
- proof that transformation contexts reuse physical coordinates without moving
  target stars;
- external Wenmo regression fixtures including the 2001 辛巳 chart.

Run the full repository checks with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
fortune-train verify
```

## Release boundary

Passing these stages still does **not** mean Ziwei Chart Engine V1 is complete.
The remaining V1 work is primarily temporal frames, Dignity/content closure,
integrity/hash finalization, renderer separation and wider operational
compatibility regression.
