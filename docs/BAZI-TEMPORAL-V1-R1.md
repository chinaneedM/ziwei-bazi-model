# Bazi Temporal V1 R1 — Dayun Schedule

Status: release candidate.

## Scope

This runtime consumes one validated `BaziChartCandidate` and its preserved `BaziTemporalSeed` values. R1 resolves Dayun direction, Jie anchor, symbolic luck age, explicit calendar-realization profiles, Pre-Dayun, and a sequence of ten-year Dayun frames.

It does **not** implement Annual/Monthly axes, dynamic relation composition, strength, pattern, useful-god selection, ShenSha, derived coordinates, event prediction, or UI.

## Inputs

```text
BaziChartCandidate
+ BaziSex (MALE/FEMALE)
+ ResolvedBaziTemporalProfile
+ requested Dayun frame count
```

Sex is a temporal projection input. It does not mutate `BaziNatalState` or its FactHash.

## Direction

R1 uses the resolved natal **year stem** polarity and sex:

```text
Yang male / Yin female -> FORWARD
Yin male / Yang female -> REVERSE
```

The direction rule carries canonical source identity `S15`.

## Jie anchor

```text
FORWARD -> next JIE
REVERSE -> previous JIE
```

The birth instant and Jie instants are compared on the UTC instant axis preserved by the Bazi Foundation TemporalSeed.

A birth instant exactly equal to a Jie boundary fails closed in R1 (`EXACT_JIE_TIE_UNRESOLVED`). The shared Time/Calendar comparison convention is not silently promoted into a classical Dayun tie rule.

## Symbolic luck age

R1 preserves the traditional proportional model on an explicit symbolic scale:

```text
3 physical days -> 1 symbolic year
1 physical day  -> 4 symbolic months
1 traditional shichen -> 10 symbolic days
```

Internally this is represented as an exact `x120` duration transform and then normalized using a 360-day symbolic year / 30-day symbolic month. This representation does not by itself choose a historical calendar-realization method.

## Operational calendar realization

The first executable profile is:

```text
MODERN_CONTINUOUS_RATIO_120X
source_class = ENGINEERING_INTERPOLATION
```

It maps the exact UTC birth-to-Jie interval continuously onto the transition axis and therefore can preserve minute/second uncertainty.

This profile is intentionally **not** named or documented as the unique classical Jiaoyun truth. The research phase identified competing realization families, including lunisolar correction and anniversary-plus-remainder methods. Those remain separate profiles pending reproducible fixtures and external compatibility discrimination.

## Dayun frames

The first Dayun pillar is the natal month pillar moved one legal 60-Jiazi step in the resolved direction; later frames continue along the same sexagenary direction.

R1 materializes:

```text
PRE_DAYUN [birth, first_transition)
DAYUN-01  [first_transition, +10y)
DAYUN-02  [+10y, +20y)
...
```

The operational ten-year boundary rule is explicitly versioned as a proleptic-Gregorian UTC anniversary rule. It is a temporal implementation choice, not an interpretation rule about the relative importance of stems and branches within a ten-year frame.

## Multiple TemporalSeeds

Bazi Foundation can group multiple legal birth-time branches into one Natal candidate when all natal facts are identical. Dayun R1 replays every TemporalSeed separately.

If those seeds produce different Jiaoyun boundaries, the result is `MULTI_CANDIDATE`; the engine never collapses them merely because Natal FactHash is shared.

## Hash boundary

`TemporalFactHash` includes the resolved Dayun facts:

- upstream Natal FactHash
- direction
- anchor identity and UTC instant
- birth UTC instant
- raw interval
- symbolic luck age
- first transition
- Pre-Dayun boundary
- Dayun Ganzhi and exact frame boundaries

TemporalSeed IDs are lineage, not fact identity. Time instants are normalized to canonical UTC ISO microsecond strings before hashing.

`TemporalComputationHash` additionally binds the resolved Temporal Profile and rule/source lineage.

## Wenzhen China compatibility profile

The A7--A11 external differential fixtures add a second, explicitly isolated profile:

```text
BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1
source_class = THIRD_PARTY_COMPATIBILITY_WITNESS
```

It does not replace the continuous profile and is not shared calendar truth. Its observed behavior is:

```text
direction       = year-stem polarity x sex
FORWARD anchor  = next Jie
REVERSE anchor  = previous Jie
interval        = birth local-apparent-solar clock vs Jie China-standard clock
symbolic ratio  = exact x120 / three days one year
realization     = combined (year * 12 + month) calendar-month displacement,
                  then day and sub-day residual
```

The interval is intentionally asymmetric: the birth endpoint uses the birthplace's apparent-solar wall clock, while the Jie endpoint uses a fixed UTC+8 China-standard wall clock. A7--A10 show that moving the same reported birth from Beijing to Kashgar changes the symbolic age, and reversing Dayun direction mirrors that change.

A11 is the leap-day discriminator. For the observed `1y8m3d7h`, the model first applies one combined 20-month displacement to 2024-02-29, reaching 2025-10-29, and only then adds three days and seven hours. Applying `+1 year` first and clamping to 2025-02-28 would incorrectly produce the prior civil date.

Wenzhen exposes symbolic age at year/month/day/hour precision. The captured UI does not independently certify the realized transition minute or second. Engine microseconds remain deterministic for replay and frame continuity, but provenance is capped with `PRECISION_CEILING:WENZHEN_UI_HOUR_ONLY`; they must not be described as exact Wenzhen truth.

The fixture file `tests/fixtures/bazi-dayun-wenzhen-compatibility-r1.json` preserves the third-party observations separately from the calculation profile. The current mixed-clock model reproduces every certified year/month/day component and the observed hour within the explicit unresolved subminute/location-coordinate envelope. This envelope is regression metadata, not permission to rewrite an observed UI value.

## External compatibility

The Wenzhen A1 fixture already confirms the Dayun **direction and pillar sequence** for the fixed-UTC+8 compatibility chart, while also exposing a historical China DST difference in the natal hour. That difference does not alter the A1 month pillar, so both the authoritative historical-time chart and Wenzhen compatibility chart produce the same Dayun Ganzhi sequence.

A7--A11 now bind the separate Wenzhen China compatibility profile described above. They do not rewrite the engineering profile or shared Time/Calendar truth. Remaining boundary work includes exact-Jie UI behavior, overseas timezones, historical China DST, and independently observable transition minute/second precision.

## Release gates

R1 release requires:

- direction replay for both sexes
- correct month-pillar +/-1 Dayun sequence
- exact raw Jie interval replay
- 3d12h synthetic fixture -> symbolic 1y2m
- explicit continuous +420d realization for that synthetic fixture
- exact-Jie fail closed
- Pre-Dayun / Dayun continuity
- same Natal + different TemporalSeed transitions -> multi-candidate
- deterministic FactHash / ComputationHash
- typed and machine-readable public contracts
- repository `fortune-train verify` PASS
- full unittest suite PASS
- A7--A10 birthplace/direction mirror regression PASS
- A11 combined calendar-month leap-day regression PASS
- Wenzhen provenance, integrity, schema and hash-boundary regression PASS
- no changes to canonical sources, model-learning, training state, prediction controls, or Ziwei runtime
