# Bazi Chart Engine V1 Foundation

Status: release candidate on the Bazi Foundation development branch.

## Purpose

This layer is the first independently runnable, typed and auditable Bazi chart-generation slice. It consumes the shared Time/Calendar Foundation and materializes deterministic natal facts only.

It is not a strength calculator, pattern classifier, useful-god engine, prediction runtime, ShenSha engine or Dayun runtime.

## Authority boundary

- Git `main` remains the dynamic repository authority after release.
- `sources/canonical/` is not modified by this Foundation work.
- S11 and S14 are provenance identities for generated Bazi knowledge facts; their prediction-library role does not make an external software package or UI canonical authority.
- External products such as Wenzhen are compatibility witnesses only.

## Public vertical path

```text
BirthInput
  -> TimeCalendarFoundation.resolve_bazi()
  -> BaziChartFoundation.resolve_typed()
  -> BaziChartCandidate
  -> BaziNatalState
  -> IntegrityReport
  -> FactHash / ComputationHash
```

`BaziChartFoundation.resolve()` exposes the stable JSON envelope defined by `schemas/bazi-chart-foundation-v1.schema.json`.

## Bazi-only Time/Calendar projection

The existing combined `TimeCalendarFoundation.resolve()` is preserved unchanged. Bazi V1 adds a Bazi-only projection so Bazi charting does not depend on Ziwei-only Chinese-calendar calculations or Ziwei policy fields.

The Bazi projection reuses, rather than duplicates:

- `CivilTimeResolver`
- `SolarTimeEngine`
- `SolarTermEngine`
- `BaziTimeResolver`

It returns every legal sampled time branch and preserves previous/next Jie boundaries for later Jiaoyun work.

This also avoids making Bazi natal chart generation depend on the modern Chinese-calendar adapter's 1901-2100 range. The Solar Term engine has its own range and capability boundary; edge years remain subject to dedicated boundary certification.

## Frozen Natal fact types

### Four pillars and entity instances

Each pillar carries a legal 60-Jiazi identity. A stem character plus an arbitrary branch character is not accepted as a valid pillar merely because both characters are individually legal.

Visible stems and branches have position-scoped instance IDs such as:

```text
YEAR.STEM
YEAR.BRANCH
MONTH.STEM
MONTH.BRANCH
DAY.STEM
DAY.BRANCH
HOUR.STEM
HOUR.BRANCH
```

Repeated branch characters remain distinct instances.

### Hidden-stem membership

Hidden stems are materialized as membership facts under an explicit rule set. Registry order is retained for lineage/display compatibility but is not part of Natal Fact identity and is not interpreted as root strength.

### Ten Gods

Every visible stem and every hidden stem receives one deterministic Ten-God semantic binding relative to the Day Master.

Stable semantic IDs are separated from display labels.

### Hidden-stem exposure

An exact hidden stem that also appears as a visible stem produces an explicit `HiddenStemExposureLink`. Exposure is a fact; it does not imply pattern formation, useful-god selection or strength.

### Stem-branch affinity

The Foundation records neutral affinity facts between every visible stem and every branch. These identify exact hidden-stem matches and same-element hidden-stem matches.

They deliberately do not claim `ROOT`, `MAIN_ROOT`, `MIDDLE_ROOT`, `RESIDUAL_ROOT` or any strength value.

### Raw relations

V1 raw relations are occurrence facts only. The initial default registry includes:

- Five Stem Combinations, with a nominal transformation element but no claim of successful transformation
- Six Harmonies
- Six Clashes
- complete Three-Combination trines
- Zi-Mao punishment
- directed Yin-Si-Shen and Chou-Xu-Wei punishment cycles
- self-punishment for Chen/Wu/You/Hai when distinct branch instances repeat

V1 deliberately does not make Harm, Break, partial-trine, directional-triad, hidden-combination or transformation-success claims part of the default Foundation relation registry. Those require separately versioned rule-set certification.

## Explicit exclusions from `BaziNatalState`

The following are prohibited from the Natal Foundation contract:

- strong / weak body conclusions
- seasonal strength scores
- pattern / structure selection
- useful god, favorable or unfavorable elements
- root strength grades
- successful combination transformation
- relation cancellation / suppression / reactivation
- Jiaoyun and Dayun
- annual/monthly dynamic overlays
- fetal origin, life palace, body palace
- NaYin, Twelve Growth, XunKong and ShenSha
- event or life-outcome prediction

These are downstream structural, temporal, optional-annotation or interpretation layers.

## Temporal seeds and candidate grouping

Bazi differs from Ziwei candidate deduplication in one important way.

Two legal time branches can generate the same natal chart while preserving different birth instants. Since the later Jiaoyun boundary depends on the birth-to-Jie interval, Bazi cannot discard those time branches after natal deduplication.

Therefore one `BaziChartCandidate` may contain:

```text
one BaziNatalState
one Natal FactHash
multiple BaziTemporalSeed values
```

Temporal seeds contain the source Time/Calendar branch index, sampled wall time, UTC birth instant, local apparent solar datetime, previous/next Jie instants and uncertainty lineage. They are not part of Natal FactHash.

## Integrity and hashes

`validate_natal_state()` replays the deterministic generators and checks:

- four ordered pillars
- legal 60-Jiazi identities
- unique visible stem and branch instances
- Day Master binding
- hidden-stem membership
- complete Ten-God bindings
- exposure replay
- 4 x 4 neutral stem-branch affinity coverage
- raw relation replay and participant validity
- relation arity/orientation
- source provenance
- algorithm identity/version

`BaziNatalFactHash` represents deterministic natal facts only.

`BaziNatalComputationHash` additionally binds the resolved calculation profile, algorithm versions, rule-set lineage, source identities and hidden-stem registry order.

Changing display/registry ordering without changing membership must not change Natal FactHash, but it may change ComputationHash.

## Historical-time compatibility discriminator

The Wenzhen A1 screenshot used:

```text
Male
Beijing
1990-06-15 12:00 civil time
```

Wenzhen displayed:

```text
庚午 壬午 辛亥 甲午
```

The authoritative Time/Calendar Foundation uses the IANA `Asia/Shanghai` historical timeline. China was observing summer time for this fixture, so historical civil offset and true-solar conversion yield:

```text
庚午 壬午 辛亥 癸巳
```

A fixed UTC+08:00 compatibility clock reproduces the Wenzhen `甲午` hour while the first three pillars remain identical.

This is classified as a historical-time compatibility difference, not a Bazi engine defect. The Foundation must not erase historical timezone/DST facts merely to imitate an external application.

## Validation matrix

Current release-candidate tests include:

- exactly 60 legal identities among all 120 stem x branch pairs
- complete 10 x 10 Ten-God matrix
- hidden-stem membership and Ten-God replay
- explicit exposure links
- 16 visible-stem x branch affinity facts
- repeated branch instance preservation
- directed punishment orientation
- complete trine vs partial-trine boundary
- same natal chart with multiple preserved temporal seeds
- deterministic Natal hashes
- hidden-stem order excluded from Natal FactHash
- Bazi-only Time/Calendar projection without Ziwei calendar evaluation
- historical `Asia/Shanghai` vs fixed UTC+8 Wenzhen compatibility discriminator
- repository `fortune-train verify`
- full unittest suite

## Next layers

The next implementation layer after Foundation release is not ShenSha or prediction. It is separately scoped work:

1. Bazi Structural Runtime: relation composition / suppression / reactivation and profile-specific root resolution.
2. Bazi Temporal Runtime: direction, Jie anchor, Jiaoyun conversion profiles, Pre-Dayun, Dayun frames, Annual/Monthly axes and temporal intersections.
3. Optional derived coordinates and annotations.
4. Bazi Application / ViewModel.
5. Only after both applications are stable: unified Ziwei + Bazi application shell.
