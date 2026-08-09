# Ziwei Core Auxiliary Dignity R2

## Purpose

This stage closes operational dignity for the fourteen core auxiliary entities
without treating external software as product or historical authority.

Runtime identity:

```text
OPERATIONAL-ZIWEI-DIGNITY-R2
```

External calibration identity:

```text
EXTERNAL_COMPATIBILITY_ORACLE_NOT_CANONICAL_AUTHORITY
Wenmo Tianji 2.5.9 / API 1.1.2 / star code C5VUC / default settings
```

The software name exists in fixture/provenance only. It does not define our
ChartState, API names, renderer layout, UI, entity ontology or canonical source truth.

## Reachable-domain rule

Dignity completeness is measured over the output domain of the bound Placement
Generator, not over an artificial entity × 12 rectangle.

For the fourteen operational core auxiliaries:

```text
full-Z12 entities (8 × 12) = 96
天魁 reachable = 5
天钺 reachable = 5
天马 reachable = 4
禄存 reachable = 8
擎羊 reachable = 8
陀罗 reachable = 8
TOTAL = 134
```

The complete external observation set covers all 134 reachable cells with zero
conflicts. No impossible entity/address cell is created merely to make a table rectangular.

## State semantics

Dignity is a typed `DignityAnnotation`, never a mutation of `Placement`.

```text
GRADED
  grade ∈ {庙, 旺, 得, 利, 平, 不, 陷}

UNRATED
  grade = null
```

`UNRATED` is not 平, not 不, and not missing evidence. It records an explicit
operational state for which the calibrated output provides no seven-grade value.
Current R2 contains exactly three such reachable cells:

```text
STAR.TIANKUI@寅
STAR.TIANYUE@午
STAR.DIJIE@亥
```

Core auxiliary totals:

```text
reachable = 134
GRADED = 131
UNRATED = 3
conflicts = 0
```

Combined with the already closed fourteen-main-star matrix:

```text
runtime entities = 28
runtime cells = 168 + 134 = 302
GRADED = 168 + 131 = 299
UNRATED = 3
```

## Profile binding

R2 fails closed unless it is paired with the compatible operational core-auxiliary
placement profile. This prevents one profile's placement geometry from silently
receiving another profile's dignity registry.

The existing main-star-only R1 remains available for backward compatibility.

## Hash and view semantics

`status` and `grade` are canonical static annotation facts and therefore belong in
`FactHash`. Evidence/provenance identity belongs in `ComputationHash` lineage.
Presentation visibility remains downstream:

```text
change status/grade -> FactHash changes
change evidence only -> FactHash stable, ComputationHash changes
show/hide dignity -> source hashes stable, ViewHash changes
```

Renderer-neutral `ViewPlacement` exposes both `dignity_status` and
`dignity_grade`. A renderer may choose how to display `UNRATED`; it cannot rewrite
the source annotation.

## Validation

The regression suite derives the reachable set from the actual operational
Auxiliary Generator by varying hour, month, year stem, year branch and Fire/Bell
branch-hour inputs. The derived set must equal the registry set exactly at 134 cells.

The suite also checks:

- calibration fixture = runtime registry;
- exactly 131 graded + 3 unrated core-aux cells;
- R2 materializes 28 main/core-aux annotations on a compatible chart;
- incoherent `UNRATED + grade` fails integrity;
- status changes alter FactHash;
- ViewModel preserves `UNRATED` without inventing a grade;
- R2 profile binding fails closed when compatible core auxiliaries are absent.

## Source-governance boundary

This PR does not modify `sources/canonical/`. The current operational table can be
rebound to stronger canonical provenance later if Git canonical source governance
closes the relevant historical tables. Such a provenance upgrade must not require
changing the typed ChartState interface.
