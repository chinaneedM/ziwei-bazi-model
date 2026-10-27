# Ziwei Chart Engine V1 Foundation

## Status and scope

Ziwei Chart Engine V1 is frozen at the deterministic release profile
`ZIWEI-CHART-ENGINE-V1@1.0.0`, built on Time/Calendar Foundation `PHASE-01-R1`.
The implementation extends through natal placements, typed static annotations,
operational content, roles/rings/transformations, temporal frames, fail-closed
integrity/hash validation, a renderer-neutral ViewModel boundary, and a public typed
end-to-end handoff. The corresponding release contract is documented in
`docs/ZIWEI-CHART-ENGINE-V1-RELEASE.md`.

Implemented:

- Time/Calendar consumption without duplicating civil-time, astronomy or Chinese-calendar logic;
- one frozen operational calculation profile with immutable component identities and versions;
- public `resolve_typed()` handoff preserving validated `NatalChartState`, effective Ziwei birth year, sex, branch lineage, IntegrityReport and HashBundle;
- typed Z12, Life/Body, twelve-palace designations, address stems and Five Element Bureau;
- Ziwei anchor, Tianfu reflection and all fourteen main stars;
- profile-bound core auxiliaries and a separate compatibility Fire/Bell family;
- dependency-bound 三台/八座、恩光/天贵;
- a profile-versioned operational minor-star family: legacy R3 v1.0.0 emits 35 entities, while R4/V1 v2.0.0 adds 天寿、天伤、天使 for 38 operational minor entities;
- typed `DignityAnnotation` with complete project-owned operational coverage for every generator-reachable cell in the current 70-entity physical inventory;
- main-star Dignity: 14 entities × 12 addresses = 168/168 `GRADED` cells;
- core-auxiliary Dignity: 134 generator-reachable cells = 131 `GRADED` + 3 `UNRATED`;
- dependency/minor R3 Dignity: 39 entities / 379 generator-reachable cells = 290 `GRADED` + 89 `UNRATED`;
- R4 天寿/天伤/天使 Dignity: 36/36 generator-reachable cells, all `GRADED`, zero observed conflicts;
- full V1 Dignity scope: 70 physical entities / 717 reachable cells / 625 `GRADED` / 92 `UNRATED`;
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
- machine-readable chart, temporal and view schemas validated against real emitted runtime payloads in CI.

Explicitly post-V1 unless promoted by a new release/profile version:

- temporal extensions beyond current Daxian/Annual/Minor-Limit and annual 斗君 scope, including separately typed month/day/hour frame families;
- graphical renderer / UI;
- general ChartDiff automation beyond frozen compatibility fixtures;
- wider compatibility research for additional physical entities not in the V1 inventory;
- interpretation or prediction;
- Structural Runtime V2 and the later Query/Evidence/Warrant/Reality/Possible-Worlds runtime.

The former V1 blockers for dependency/minor Dignity, 天寿 placement, the Wenmo-default
天伤/天使 profile discriminator, typed runtime composition and published-schema drift
are closed. Historical alternative source families remain preserved rather than
overwritten.

## Fact-type boundaries

```text
Placement
  = one physical entity occupies one Z12 address

DignityAnnotation
  = a typed static state attached to an existing entity/address under an explicit scale/rule set;
    status is GRADED or UNRATED; it does not rename or move the physical entity

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
-> frozen ZIWEI-CHART-ENGINE-V1 calculation profile
-> ZiweiChartFoundation.resolve_typed()
-> ZiweiChartCandidate
   -> effective absolute Ziwei birth year + Sex + branch lineage
   -> immutable NatalChartState
      -> physical placements
      -> static DignityAnnotation state
      -> natal TransformationActivation overlay
      -> Ring state
      -> RoleBinding state
   -> IntegrityReport
   -> FactHash / ComputationHash

ZiweiChartCandidate.temporal_context()
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

The stable JSON `resolve()` API remains available and serializes the same typed
resolution envelope after validation. Temporal state is deliberately separate from
`NatalChartState`. Renderers are deliberately downstream from `ChartViewModel` and
never receive mutable access to canonical state. A graphical square chart, circular
chart and plain-text view may therefore consume the same ViewModel without requiring
a second canonical state.

## Integrity and hash semantics

Generated state is not returned as resolved merely because all generators ran.
It must also pass typed integrity checks covering structure topology, unique
physical entity identity, annotation-target/address consistency, provenance,
transformation-target immutability, ring cardinality/topology and temporal-frame
invariants. Invalid generated state fails closed.

Three hash layers are deliberately distinct:

```text
FactHash
  = canonical generated facts only, including dignity status/grade annotations

ComputationHash
  = FactHash + resolved profile + algorithm/generator versions + provenance lineage

ViewHash
  = source hashes + PresentationProfile + selected temporal projection + ViewProjection version
```

Changing a dignity status or grade therefore changes `FactHash`; changing only
the evidence lineage for the same state preserves `FactHash` but changes
`ComputationHash`. Showing or hiding dignity in a presentation changes `ViewHash` only.

`UNRATED` is a first-class operational state with `grade=null`; it is not an
alias for 平, 不 or missing evidence. Integrity rejects `UNRATED` carrying a grade
and rejects `GRADED` without a valid seven-grade value.

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
structure/main stars, `ZZZA-PR-042` for 天寿, `ZZZA-PR-052`/`053` for dependency
stars, `ZZZA-PR-054`/`055` for roles, and `ZZZA-PR-057` through `060` for the
current ring families.

For 天伤/天使, the source corpus deliberately preserves more than one family:

- `ZZQS-A-1855` records the fixed traditional placement: 天伤在交友/奴仆，天使在疾厄;
- `ZZZA-PR-051` records a yin/yang-sex swap family.

The V1 operational profile selects the fixed Wenmo-compatible family because the
1975-05-20 yin-year male discriminator still displays 天伤 in 交友 and 天使 in 疾厄.
The alternate family remains source knowledge and is not deleted or rewritten.

S08's explicit `唯一运行四化表` supplies the transformation registry. One
`TransformationGenerator` is reused for natal, Daxian and Annual contexts by
changing the declared causal `source_layer`, `source_stem` and `context_id`.

S10's current dynamic-coordinate supplement supplies the V1 temporal geometry:

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

## Operational content versioning

R3 remains an immutable replay target:

```text
WENMO_DEFAULT_MINOR_R1 v1.0.0
OPERATIONAL-ZIWEI-DIGNITY-R3 v3.0.0
67 physical entities
681 reachable Dignity cells
589 GRADED
92 UNRATED
```

R4/V1 extends the same minor-rule-set family without changing R3:

```text
WENMO_DEFAULT_MINOR_R1 v2.0.0
OPERATIONAL-ZIWEI-DIGNITY-R4 v4.0.0
70 physical entities
717 reachable Dignity cells
625 GRADED
92 UNRATED
```

Profile validation binds R3 specifically to minor v1.0.0 and V1/R4 specifically to
minor v2.0.0. This prevents a newer physical inventory from silently changing an
already frozen R3 computation snapshot.

TianShou uses the operational Body-basis formula selected by source route
`ZZZA-PR-042` and the 1992-06-10 discriminator:

```text
TianShou = BodyAddress + BirthYearBranchIndex (mod 12)
```

The V1 TianShang/TianShi formulas are:

```text
TianShang = Life + 5 = 交友
TianShi   = Life + 7 = 疾厄
```

## Dignity calibration and release boundary

The dedicated main-star calibration pack covers all 12 Ziwei anchors and therefore
all 168 unique main-star/address cells with zero observed conflicts.

The core-auxiliary calibration pack closes exactly all 134 addresses reachable by
the bound core-auxiliary Generator. It yields 131 `GRADED` cells plus three explicit
`UNRATED` cells with zero observed conflicts.

R3 closes the four dependency stars plus 35 legacy operational minor stars over
exactly 379 generator-reachable cells: 290 `GRADED` + 89 `UNRATED`, with zero
observed conflicts. Impossible entity/address pairs are not invented.

R4/V1 adds 天寿、天伤、天使. The prior 21 calibration exports already covered 32/36
of their cells; two deliberately selected closure exports supply the four missing
cells:

```text
2012-09-25 00:30 -> Life=酉 -> 天伤@寅=平, 天使@辰=陷
2006-04-07 00:30 -> Life=辰 -> 天伤@酉=平, 天使@亥=旺
```

The resulting three-row matrix is 36/36 `GRADED`, zero `UNRATED`, zero observed
conflicts. Its added-row SHA256 is:

```text
5bac16b2f13d240f3adc7846a8aa45ce58f1c9bb2b89c6f7a450aef606b40e23
```

For the frozen 70-entity V1 physical inventory, Dignity is no longer a coverage
blocker. Any future physical entity promoted into a later release must independently
satisfy the same generator-reachable-domain closure rule before it can join a
complete Dignity profile.

## Validation

Regression coverage includes:

- all 12 natal months × 12 birth hours for Life/Body;
- all 150 canonical Ziwei-anchor cells;
- Tianfu reflection and main-star covariance;
- all 12 Ziwei-anchor configurations × 14 main stars = 168 operational main-star Dignity cells;
- all 134 generator-reachable core-auxiliary Dignity cells;
- exactly 131 graded + 3 unrated core-auxiliary states, with no invented unreachable cells;
- exact R3 dependency/minor generator-domain equality over 379 reachable cells;
- exactly 290 graded + 89 unrated R3 dependency/minor states;
- exact V1 TianShou/TianShang/TianShi generator-domain equality over 36 reachable cells;
- exact 36 graded + 0 unrated V1 added states and frozen matrix SHA256;
- full V1 registry summary: 70 entities / 717 cells / 625 graded / 92 unrated;
- R3 legacy-profile replay and V1 minor-version mismatch rejection;
- frozen `ZIWEI-CHART-ENGINE-V1@1.0.0` profile binding;
- public `resolve_typed()` materialization of one complete 70-entity / 70-annotation chart;
- typed time-uncertainty deduplication while preserving branch lineage;
- dignity as immutable annotation rather than placement mutation;
- dignity target/address and status/grade integrity failures;
- dignity fact vs provenance hash-layer discrimination;
- presentation show/hide dignity without canonical-state mutation;
- exhaustive core auxiliary, Fire/Bell and minor-star domains;
- all 60 valid sexagenary Xunkong pairs;
- dependency-star, role and ring profile checks;
- all 10 transformation stems × four ordered assignments, 40 assignments / 39 mechanisms;
- transformation missing/duplicate-target fail-closed behavior;
- all five first-Daxian age values and the full yin/yang × sex direction matrix;
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
- full public BirthInput -> Natal -> Temporal -> View -> Renderer smoke with no private calls;
- real emitted chart JSON validated against `ziwei-chart-foundation-v1.schema.json`;
- real emitted temporal JSON validated against `ziwei-temporal-state-v1.schema.json`;
- real emitted ViewModel JSON validated against `ziwei-chart-view-v1.schema.json`;
- plain-text rendering from renderer-neutral ViewModel only.

Run the full repository checks with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
fortune-train verify
```

## Frozen V1 release boundary

Ziwei Chart Engine V1 is frozen around the current deterministic calculation profile,
70-entity physical inventory, current Daxian/Annual/Minor-Limit temporal runtime,
Integrity/Hash contracts and published chart/temporal/view schemas.

Future work does not reopen V1 merely because more traditional content exists.
A new release/profile version is required when a change alters deterministic chart
facts, Generator behavior, calculation-profile identity, Canonical Fact boundaries,
Integrity/Hash semantics, or the published V1 API/schema contract. Graphical UI,
interpretation/prediction, Structural Runtime V2, non-promoted historical variants,
and additional temporal families remain downstream until that threshold is met.
