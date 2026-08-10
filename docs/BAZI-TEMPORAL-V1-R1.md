# Bazi Temporal V1 R1 — Dayun Schedule

Status: release candidate.

## Scope

This runtime consumes one validated `BaziChartCandidate` and its preserved `BaziTemporalSeed` values. R1 resolves Dayun direction, Jie anchor, symbolic luck age, one explicit calendar-realization profile, Pre-Dayun, and a sequence of ten-year Dayun frames.

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

## External compatibility

The Wenzhen A1 fixture already confirms the Dayun **direction and pillar sequence** for the fixed-UTC+8 compatibility chart, while also exposing a historical China DST difference in the natal hour. That difference does not alter the A1 month pillar, so both the authoritative historical-time chart and Wenzhen compatibility chart produce the same Dayun Ganzhi sequence.

The next external discriminator is A7. It is designed specifically to determine how Wenzhen realizes the symbolic luck age into a civil transition date. The result will inform a separate Wenzhen compatibility profile; it will not rewrite this engineering profile or shared calendar truth.

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
- no changes to canonical sources, model-learning, training state, prediction controls, or Ziwei runtime
