# Ziwei Operational Dignity Calibration R1

## Purpose and authority boundary

The runtime object is the project's own vendor-neutral operational registry:

```text
RULE_SET = OPERATIONAL-ZIWEI-MAIN-STAR-DIGNITY-R1
SCALE = ZIWEI-SEVEN-GRADE-DIGNITY-R1
```

External software is calibration evidence only:

```text
CALIBRATION_AUTHORITY = EXTERNAL_COMPATIBILITY_ORACLE_NOT_CANONICAL_AUTHORITY
CALIBRATION_TARGET = Wenmo Tianji 2.5.9 / API 1.1.2 / star code C5VUC / default settings
```

The external target does not define ChartState, field names, renderer layout, lexemes, UI, or canonical historical truth. It must not modify or silently overwrite `sources/canonical/` claims.

## Initial six-sample audit

The first six user-provided text exports were normalized as:

```text
entity × Z12 address -> displayed dignity observation
```

They produced:

```text
TOTAL UNIQUE OBSERVED CELLS = 267
GRADE(庙/旺/得/利/平/不/陷) = 231
EXPLICIT_NO_DISPLAY = 36
CONFLICT = 0
```

`EXPLICIT_NO_DISPLAY` is a real compatibility observation, not an alias for `平`, `不`, or an unobserved registry cell. The operational main-star registry in this phase uses only explicit seven-grade observations; auxiliary/minor-star no-display semantics remain a separate future content problem.

## Main-star 168-cell closure

The initial samples covered Ziwei anchors:

```text
丑 / 卯 / 午 / 戌 / 亥
```

Seven optimized additional charts were then selected to cover the remaining anchors while keeping year/month/hour inputs as stable as possible:

| Gregorian date | Lunar day | Ziwei anchor |
|---|---:|---|
| 2001-12-16 | 2 | 辰 |
| 2001-12-18 | 4 | 寅 |
| 2001-12-19 | 5 | 子 |
| 2001-12-20 | 6 | 巳 |
| 2001-12-28 | 14 | 未 |
| 2002-01-01 | 18 | 申 |
| 2002-01-05 | 22 | 酉 |

Final main-star observation result:

```text
12 Ziwei anchors × 14 main stars = 168 observations
unique (main-star entity, Z12 address) cells = 168
conflicting cells = 0
```

The normalized external evidence is stored in `tests/fixtures/wenmo-main-star-dignity-r1.json`. That fixture remains explicitly vendor/source specific. The runtime registry generated from it is vendor-neutral.

## Runtime representation

Dignity is a typed `DignityAnnotation`, not part of a star-name string and not a mutation of `Placement`:

```text
Placement
  entity_id
  address

DignityAnnotation
  target_entity_id
  target_address
  grade
  scale_id/version
  rule_set_id/version
  generator_id/version
  source_refs
```

Therefore:

- changing a dignity grade changes canonical facts and `FactHash`;
- changing only calibration/provenance lineage preserves `FactHash` but changes `ComputationHash`;
- hiding/showing dignity is presentation-only and changes `ViewHash`, not the canonical chart;
- a renderer may display `紫微[旺]`, split the grade into another column, use icons, or omit it entirely without changing the calculation model.

## Release status after R1

The fourteen main stars now have a complete operational 14 × 12 registry.

This does **not** mean the whole Operational Dignity Registry is complete. Auxiliary and minor-star coverage remains partial, including explicit no-display cells. GitHub issue #180 remains the content/release blocker for closing those additional entities.

Next steps:

1. regression-test all 168 main-star cells;
2. bind the main-star registry through the immutable calculation profile;
3. include annotations in Integrity / FactHash / ComputationHash;
4. expose dignity through the renderer-neutral ViewModel;
5. compute auxiliary/minor-star coverage from all available observations;
6. use generator-aware set cover to request only the smallest additional external test pack;
7. keep historical/canonical source research separately governed.
