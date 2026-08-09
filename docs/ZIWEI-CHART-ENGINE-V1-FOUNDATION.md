# Ziwei Chart Engine V1 Foundation

## Status and scope

The shared Time/Calendar Foundation and the Ziwei foundation core are stable.
The implementation now extends through natal placements, typed static annotations,
operational content, roles/rings/transformations, temporal frames, fail-closed
integrity/hash validation and a presentation-only ViewModel boundary.

Implemented:

- Time/Calendar consumption without duplicating civil-time, astronomy or Chinese-calendar logic;
- typed Z12, Life/Body, twelve-palace designations, address stems and Five Element Bureau;
- Ziwei anchor, Tianfu reflection and all fourteen main stars;
- profile-bound core auxiliaries and a separate compatibility Fire/Bell family;
- dependency-bound 三台/八座、恩光/天贵;
- a 35-entity operational minor-star content pack calibrated against external fixtures;
- typed `DignityAnnotation` with a complete project-owned 14-main-star × 12-address operational registry;
- typed `RoleBinding` for 命主/身主;
- typed `RingInstance` / `RingMemberBinding` for 长生、岁前、将前、博士;
- typed `TransformationActivation` using S08's 10-stem / 40-assignment runtime table;
- standalone `ZiweiTemporalEngine` with typed Daxian, Annual and Minor Limit frames;
- Daxian and Annual reuse the same transformation generator without moving natal stars;
- immutable resolved profile bindings for Time/Calendar, auxiliary, minor-star,
  dignity, transformation, temporal, ring and role rule identities/versions;
- fail-closed natal and temporal integrity validation;
- separate deterministic `FactHash` and `ComputationHash` semantics;
- typed `PresentationProfile`, renderer-neutral `ChartViewModel` and `ViewHash`;
- a pure plain-text renderer that consumes only `ChartViewModel`;
- machine-readable schemas, provenance and diagnostics.

Still outside the current implementation slice:

- unresolved operational content such as 天寿 and the 天伤/天使 profile split;
- auxiliary/minor-star Dignity closure, including explicit no-display semantics, tracked by GitHub issue #180;
- temporal extensions beyond current Daxian/Annual/Minor-Limit scope, such as a
  separately typed 斗君/月 frame runtime if promoted into V1;
- graphical renderer / UI;
- general ChartDiff automation beyond frozen compatibility fixtures;
- interpretation or prediction.

## Fact-type boundaries

```text
Placement
  = one physical entity occupies one Z12 address

DignityAnnotation
  = a typed static state attached to an existing entity/address under an explicit scale/rule set;
    it does not rename or move the physical entity

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

ChartViewModel
  = renderer-neutral presentation projection only; it cannot write back into canonical or temporal state
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
   -> static DignityAnnotation state
   -> natal TransformationActivation overlay
   -> Ring state
   -> RoleBinding state
   -> IntegrityReport
   -> FactHash / ComputationHash

NatalChartState + absolute Ziwei birth year + Sex + resolved profile
-> ZiweiTemporalEngine
   -> DaxianFrame[]
   -> AnnualFrame[]
   -> MinorLimitFrame[]
   -> IntegrityReport
   -> FactHash / ComputationHash

validated NatalChartState (+ optional validated TemporalState)
+ HashBundle
+ PresentationProfile
-> ZiweiViewProjectionCompiler
-> immutable renderer-neutral ChartViewModel
-> ViewHash
-> any compatible Renderer
```

Temporal state is deliberately separate from `NatalChartState`. Renderers are
deliberately downstream from `ChartViewModel` and never receive mutable access
to canonical state. A graphical square chart, circular chart and plain-text view
may therefore consume the same ViewModel without requiring a second canonical state.

## Integrity and hash semantics

Generated state is not returned as resolved merely because all generators ran.
It must also pass typed integrity checks covering structure topology, unique
physical entity identity, annotation-target/address consistency, provenance,
transformation-target immutability, ring cardinality/topology and temporal-frame
invariants. Invalid generated state fails closed.

Three hash layers are deliberately distinct:

```text
FactHash
  = canonical generated facts only, including typed static annotations such as dignity grades

ComputationHash
  = FactHash + resolved profile + algorithm/generator versions + provenance lineage

ViewHash
  = source hashes + PresentationProfile + selected temporal projection + ViewProjection version
```

Changing a dignity grade therefore changes `FactHash`; changing only the evidence
lineage for the same grade preserves `FactHash` but changes `ComputationHash`.
Showing or hiding dignity in a presentation changes `ViewHash` only.

Display-label, palace-label, address-order or visibility changes are presentation
changes only: they may change `ViewHash`, but they cannot rewrite `FactHash` or
`ComputationHash`. Renderer-specific layout/pixel output is deliberately not part
of the renderer-neutral ViewHash; a future renderer-specific `RenderHash` may be
added downstream if required.

The View compiler re-validates its natal source; temporal projection additionally
requires the explicit `TemporalNatalContext` used to validate that temporal state,
rather than reconstructing hidden inputs.

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

External software fixtures remain explicitly
`EXTERNAL_COMPATIBILITY_ORACLE_NOT_CANONICAL_AUTHORITY`.
They can calibrate or discriminate an operational rule set, but they do not define
ChartState, API field names, renderer layout, product UI, or historical-source truth.

The 2001-12-15 辛巳 fixture externally checks:

- Fire/Bell, dependency stars, roles and 35 operational minor stars;
- all four rings / 48 ring members;
- natal 辛四化;
- all 12 Daxian active palace Ganzhi and age/year ranges;
- Annual TaiSui/active-palace coordinates across Daxian boundaries;
- Minor Limit ages 1-12.

The dedicated main-star dignity calibration pack covers all 12 Ziwei anchors and
therefore all 168 unique main-star/address cells with zero observed conflicts.
The runtime identity is the project-owned `OPERATIONAL-ZIWEI-MAIN-STAR-DIGNITY-R1`;
the external software name exists only in calibration provenance/fixtures.

## Dignity release boundary

Dignity remains an operational-content blocker only for entities whose registry
is still incomplete; it is no longer a blocker for the fourteen main stars.

S05 defines brightness semantics and S06 contains historical predicates, but the
current Git canonical sources do not expose one complete deterministic seven-grade
operational matrix for every required auxiliary/minor entity/address cell. Those
missing cells must not be inferred from absence or from one external chart.
Issue #180 tracks auxiliary/minor-star registry closure and explicit no-display semantics.

## Validation

Regression coverage now includes:

- all 12 natal months x 12 birth hours for Life/Body;
- all 150 canonical Ziwei-anchor cells;
- Tianfu reflection and main-star covariance;
- all 12 Ziwei-anchor configurations × 14 main stars = 168 operational main-star dignity cells;
- dignity as immutable annotation rather than placement mutation;
- dignity target/address integrity failure;
- dignity grade vs provenance hash-layer discrimination;
- presentation show/hide dignity without canonical-state mutation;
- exhaustive core auxiliary, Fire/Bell and minor-star domains;
- all 60 valid sexagenary Xunkong pairs;
- dependency-star, role and ring profile checks;
- all 10 transformation stems x four ordered assignments, 40 assignments / 39 mechanisms;
- transformation missing/duplicate-target fail-closed behavior;
- all five first-Daxian age values and the full yin/yang x sex direction matrix;
- exact 12-Daxian external regression for the 2001 金四局 阴男 chart;
- Annual samples proving year-stem 四化 is separate from Annual-Life palace stem;
- Minor Limit male/female direction rules and exact age 1-12 external regression;
- pre-first-Daxian Annual frames preserved with no invented Daxian parent;
- natal and temporal integrity success/failure cases;
- deterministic 64-hex fact/computation hashes;
- display/provenance/profile/fact mutation tests proving the intended canonical hash semantics;
- injected invalid generated state proving the public chart engine fails closed before return;
- deterministic ViewModel/ViewHash generation;
- lexeme and address-order presentation changes without canonical-state mutation;
- explicit temporal-context requirement at the View projection boundary;
- plain-text rendering from renderer-neutral ViewModel only.

Run the full repository checks with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
fortune-train verify
```

## Release boundary

Passing these stages still does **not** mean Ziwei Chart Engine V1 is complete.
The main remaining V1 gates are auxiliary/minor Dignity/content closure and wider
operational compatibility regression. Graphical UI can remain post-core because
the renderer boundary is now explicit and presentation-only.
