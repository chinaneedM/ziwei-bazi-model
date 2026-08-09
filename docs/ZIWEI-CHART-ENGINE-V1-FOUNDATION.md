# Ziwei Chart Engine V1 Foundation

## Status and scope

The shared Time/Calendar Foundation and the Ziwei foundation core are stable.
The implementation now extends through natal placements, operational content,
typed roles/rings/transformations and a separate temporal-frame runtime.

Implemented:

- Time/Calendar consumption without duplicating civil-time, astronomy or Chinese-calendar logic;
- typed Z12, Life/Body, twelve-palace designations, address stems and Five Element Bureau;
- Ziwei anchor, Tianfu reflection and all fourteen main stars;
- profile-bound core auxiliaries and a separate Wenmo Fire/Bell family;
- dependency-bound 三台/八座、恩光/天贵;
- a 35-entity Wenmo operational minor-star content pack;
- typed `RoleBinding` for 命主/身主;
- typed `RingInstance` / `RingMemberBinding` for 长生、岁前、将前、博士;
- typed `TransformationActivation` using S08's 10-stem / 40-assignment runtime table;
- standalone `ZiweiTemporalEngine` with typed Daxian, Annual and Minor Limit frames;
- Daxian and Annual reuse the same transformation generator without moving natal stars;
- immutable resolved profile bindings for Time/Calendar, auxiliary, minor-star,
  transformation, temporal, ring and role rule identities/versions;
- machine-readable schemas, provenance and fail-closed diagnostics.

Still outside the current implementation slice:

- unresolved operational content such as 天寿 and the 天伤/天使 profile split;
- a complete operational Dignity registry (tracked by GitHub issue #180);
- temporal extensions beyond current Daxian/Annual/Minor-Limit scope, such as a
  separately typed 斗君/月 frame runtime if promoted into V1;
- integrity/hash finalization;
- renderer/UI;
- general ChartDiff automation beyond frozen Wenmo fixtures;
- interpretation or prediction.

## Fact-type boundaries

```text
Placement
  = one physical entity occupies one Z12 address

TransformationActivation
  = one causal stem/layer activates 禄/权/科/忌 on an existing physical entity;
    it references the immutable target address and never moves the star

RoleBinding
  = an existing entity is designated as 命主/身主

RingInstance / RingMemberBinding
  = cyclic ring state, not physical star placement

DaxianFrame / AnnualFrame / MinorLimitFrame
  = dynamic reference frames over the natal chart, not regenerated natal charts

DesignationBinding
  = a palace designation bound to an address inside one declared frame
```

Same-label objects remain distinct across layers. Physical 华盖 is not the
将前-ring 华盖; Annual Life at a branch does not move the natal stars at that
branch; a Daxian/Annual 四化 activation does not relocate its target entity.

## Deterministic vertical path

```text
BirthInput
-> TimeCalendarFoundation
-> profile-bound Ziwei birth coordinates
-> immutable NatalChartState
   -> physical placements
   -> natal TransformationActivation overlay
   -> Ring state
   -> RoleBinding state

NatalChartState + absolute Ziwei birth year + Sex + resolved profile
-> ZiweiTemporalEngine
   -> DaxianFrame[]
   -> AnnualFrame[]
   -> MinorLimitFrame[]
```

Temporal state is deliberately separate from `NatalChartState`.

## Canonical and compatibility authority

Key S01 source routes include `ZZZA-PR-008` through `ZZZA-PR-015` for natal
structure/main stars, `ZZZA-PR-052`/`053` for dependency stars,
`ZZZA-PR-054`/`055` for roles, and `ZZZA-PR-057` through `060` for the current
ring families.

S08's explicit `唯一运行四化表` supplies the transformation registry. One
`TransformationGenerator` is reused for natal, Daxian and Annual contexts by
changing the declared causal `source_layer`, `source_stem` and `context_id`.

S10's current dynamic-coordinate supplement supplies the implemented temporal
geometry:

- Five Element Bureau number = first Daxian nominal age;
- 阳男阴女 forward / 阴男阳女 reverse Daxian movement;
- every ten years advances one Daxian address;
- Annual TaiSui branch is Annual Life;
- Annual 四化 uses the annual heavenly stem, not the natal stem of the Annual Life address;
- Minor Limit age-one anchor is selected by the birth-year trine group and then
  moves male-forward / female-reverse, independent of year-stem yin/yang.

Wenmo fixtures remain explicitly
`EXTERNAL_COMPATIBILITY_ORACLE_NOT_CANONICAL_AUTHORITY`.

The 2001-12-15 辛巳 fixture now externally checks:

- Fire/Bell, dependency stars, roles and 35 operational minor stars;
- all four rings / 48 ring members;
- natal 辛四化;
- all 12 Daxian active palace Ganzhi and age/year ranges;
- Annual TaiSui/active-palace coordinates across Daxian boundaries;
- Minor Limit ages 1-12.

## Dignity release blocker

Dignity remains an operational-content blocker, not an architecture blocker.
S05 defines brightness semantics and S06 contains many historical predicates,
but current Git canonical sources do not expose one complete deterministic
seven-grade operational matrix for every required entity/address cell. Missing
cells must not be inferred from absence or from one external chart. Issue #180
tracks explicit registry closure and optimized Wenmo calibration.

## Validation

Regression coverage now includes:

- all 12 natal months x 12 birth hours for Life/Body;
- all 150 canonical Ziwei-anchor cells;
- Tianfu reflection and main-star covariance;
- exhaustive core auxiliary, Fire/Bell and minor-star domains;
- all 60 valid sexagenary Xunkong pairs;
- dependency-star, role and ring profile checks;
- all 10 transformation stems x four ordered assignments, 40 assignments / 39 mechanisms;
- transformation missing/duplicate-target fail-closed behavior;
- all five first-Daxian age values and the full yin/yang x sex direction matrix;
- exact 12-Daxian Wenmo regression for the 2001 金四局 阴男 chart;
- Annual samples proving year-stem 四化 is separate from Annual-Life palace stem;
- Minor Limit male/female direction rules and exact age 1-12 Wenmo regression;
- pre-first-Daxian Annual frames preserved with no invented Daxian parent.

Run the full repository checks with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
fortune-train verify
```

## Release boundary

Passing these stages still does **not** mean Ziwei Chart Engine V1 is complete.
The main remaining V1 gates are Dignity/content closure, integrity/hash
finalization, renderer separation and wider operational compatibility regression.
