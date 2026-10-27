# Ziwei Dependency / Minor Dignity R3

## Purpose

This stage closes operational Dignity for every physical star currently emitted by
Ziwei Chart Engine V1 without promoting external software to canonical authority.

Runtime identity:

```text
OPERATIONAL-ZIWEI-DIGNITY-R3
```

R3 extends, rather than replaces, the existing backward-compatible Dignity rule sets:

```text
R1 = 14 main stars
R2 = R1 + 14 core auxiliaries
R3 = R2 + 4 dependency stars + 35 operational minor stars
```

## Reachable-domain closure

The dependency/minor denominator is derived from the active Placement Generators,
not from an artificial entity × 12 rectangle.

```text
dependency entities = 4
minor entities = 35
dependency/minor entities = 39
reachable cells = 379
GRADED = 290
UNRATED = 89
conflicts = 0
```

Combined full R3 runtime scope:

```text
main stars = 168 cells
core auxiliaries = 134 cells
dependency/minor = 379 cells
TOTAL = 681 cells

runtime entities = 67
GRADED = 589
UNRATED = 92
```

Impossible entity/address pairs are absent rather than represented as missing data.

## UNRATED semantics

`UNRATED` remains a first-class `DignityAnnotation` state with `grade=null`.
It is not 平, not 不, and not missing calibration evidence.

The 89 dependency/minor UNRATED cells are the complete reachable domains of exactly
ten operational entities:

```text
天厨 7
劫煞 4
蜚廉 12
龙德 12
月德 12
台辅 12
封诰 12
天巫 4
天月 8
阴煞 6
TOTAL 89
```

R3 reuses the existing Integrity, FactHash, ComputationHash and ViewModel semantics;
no ChartState schema change is required.

## Calibration evidence

The closed calibration fixture contains 21 Wenmo default text exports:

```text
Wenmo Tianji 2.5.9
API 1.1.2
star code C5VUC
```

Authority remains:

```text
EXTERNAL_COMPATIBILITY_ORACLE_NOT_CANONICAL_AUTHORITY
```

The external application is retained only as compatibility provenance. It does not
define runtime identity, ChartState, public field names, renderer layout, product UI
or historical-source truth.

The normalized 379-cell matrix is frozen by:

```text
SHA256 = 3eb9f9c5d7d359707293d566cfe69035fa84d0d3d0a55b18e35eb654ea321ab5
```

No `sources/canonical/` file is modified by this release.

## Profile binding

R3 fails closed unless both compatible physical-placement families are active:

```text
WENMO_DEFAULT_CORE_AUX_R1
WENMO_DEFAULT_MINOR_R1
```

This prevents a Dignity table calibrated over one placement geometry from being
silently attached to another profile.

R1 and R2 remain selectable and backward compatible.

## Validation

R3 regression checks:

- fixture and runtime registry are byte-semantic equivalents after compact-row expansion;
- the normalized matrix SHA is fixed;
- registry summary is exactly 67 entities / 681 cells / 589 graded / 92 unrated;
- dependency/minor state totals are exactly 39 entities / 379 cells / 290 graded / 89 unrated;
- the ten all-UNRATED entity domains match their Generator-reachable domains exactly;
- active stem, sexagenary-xun, year-branch, life-address, hour, month and dependency
  generator inputs re-derive exactly the same 379-cell reachable set;
- one compatible synthetic chart materializes exactly 67 Dignity annotations;
- profile validation rejects R3 without compatible core-auxiliary or minor-star bindings.

## Release boundary

This closes Dignity for the **currently implemented physical-star inventory** of
Ziwei Chart Engine V1. It does not automatically promote unresolved physical content
such as 天寿 or the 天伤/天使 profile split into V1.

If new physical entities are later promoted into the engine, their Placement domain
and Dignity governance must be closed explicitly; R3 must not silently assign them a
state by analogy.
