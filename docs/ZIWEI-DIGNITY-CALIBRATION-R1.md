# Ziwei Operational Dignity Calibration R1

## Authority boundary

This calibration is for operational compatibility only.

```text
AUTHORITY = EXTERNAL_COMPATIBILITY_ORACLE_NOT_CANONICAL_AUTHORITY
TARGET = Wenmo Tianji 2.5.9 / API 1.1.2 / star code C5VUC / default settings
```

It must not modify or silently overwrite `sources/canonical/` historical claims.
GitHub issue #180 remains the source-governance/release blocker for a complete
Operational Dignity Registry.

## Existing six-sample audit

Six user-provided Wenmo text exports were mechanically normalized as
`entity × Z12 address -> displayed dignity state`.

Observed unique cells:

```text
TOTAL = 267
GRADE(庙/旺/得/利/平/不/陷) = 231
EXPLICIT_NO_DISPLAY = 36
CONFLICT = 0
```

`EXPLICIT_NO_DISPLAY` is a real compatibility observation, not an alias for
`平`, `不` or an unobserved/missing registry cell. Across the six samples there
was no entity/address pair that alternated between a grade and no display.

## Main-star coverage

All fourteen main stars are graded in every sample. Existing samples cover five
unique Ziwei-anchor configurations:

```text
丑 / 卯 / 午 / 戌 / 亥
```

Therefore current main-star coverage is exactly:

```text
14 × 5 = 70 / 168 cells
```

The only missing Ziwei anchors are:

```text
子 / 寅 / 辰 / 巳 / 未 / 申 / 酉
```

Because the fourteen-star geometry is deterministic relative to the Ziwei
anchor, observing those seven remaining anchor configurations closes every
main-star × address cell exactly once.

## Optimized seven-chart closure pack

Reuse the already calibrated 2001 辛巳、冬月、午时、金四局 family and vary only
lunar birth day. This preserves year/month/hour structural inputs while moving
the Ziwei anchor through the seven missing configurations.

All inputs use:

```text
Sex = male
Birth place = Beijing
Clock time = 12:00
Wenmo settings = default
```

| Gregorian date | Lunar day | Expected Ziwei anchor |
|---|---:|---|
| 2001-12-16 | 2 | 辰 |
| 2001-12-18 | 4 | 寅 |
| 2001-12-19 | 5 | 子 |
| 2001-12-20 | 6 | 巳 |
| 2001-12-28 | 14 | 未 |
| 2002-01-01 | 18 | 申 |
| 2002-01-05 | 22 | 酉 |

The user only needs to return Wenmo full text exports; screenshots/settings are
not required unless an output anomaly appears.

## After the seven-chart pack

1. Close and regression-test the complete Wenmo 14 × 12 main-star Dignity matrix.
2. Keep grade cells and explicit no-display cells distinct.
3. Compute auxiliary/minor-star coverage from all observations.
4. Use generator-aware set-cover selection for the smallest additional test pack
   needed by year-stem, year-branch, month and hour dependent entities.
5. Do not request random bulk charts when a discriminator/coverage-targeted chart
   can close multiple missing cells.
6. Only after the operational registry is complete may it be bound as a required
   production Dignity Profile; historical/canonical status remains separately governed.
