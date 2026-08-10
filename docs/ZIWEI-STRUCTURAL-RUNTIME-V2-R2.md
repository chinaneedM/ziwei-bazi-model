# Ziwei Structural Runtime V2-R2

## Status

```text
RUNTIME_ID=ZIWEI-STRUCTURAL-RUNTIME-V2-R2
RUNTIME_VERSION=1.0.0
STATUS=IMPLEMENTATION_CANDIDATE
UPSTREAM_STRUCTURAL_RELEASE=ZIWEI-STRUCTURAL-RUNTIME-V2-R1@1.0.0
UPSTREAM_NATAL_RELEASE=ZIWEI-CHART-ENGINE-V1@1.0.0
ISSUE=#195
CANONICAL_SEMANTIC_BLOCKER=#194
```

V2-R2 is a separately versioned relative-palace coordinate layer after the active
neutral Structural Runtime V2-R1. It does not modify frozen V1 Natal state or active
V2-R1 StructuralState, profiles, schemas or hashes.

## Why R2 is a frame layer rather than a named-relation layer

The current Git source audit closed the mechanical access path for large canonical
sources through `sources/canonical-runtime/`, a lossless read view of canonical source
bytes. The audit found both useful structural source material and an internal retained
S04 inconsistency in Sanfang/Sizheng rows 07-12. Issue #194 owns that source correction.

R2 therefore publishes a more primitive coordinate transform that does not depend on
choosing between conflicting named semantic rows. Traditional terms are downstream
selectors over this substrate and remain disabled here.

## Relative-palace frame algebra

The frozen V1 palace designation order is:

```text
1  LIFE / 命
2  SIBLINGS / 兄弟
3  SPOUSE / 夫妻
4  CHILDREN / 子女
5  WEALTH / 财帛
6  HEALTH / 疾厄
7  TRAVEL / 迁移
8  SERVANTS_FRIENDS / 奴仆
9  CAREER / 官禄
10 PROPERTY / 田宅
11 FORTUNE / 福德
12 PARENTS / 父母
```

For every natal palace designation, R2 temporarily treats that palace as relative
ordinal 1 and rotates the same frozen V1 role order through all 12 ordinals.

For origin designation index `i` and zero-based relative role offset `j`:

```text
target_designation_index = (i + j) mod 12
relative_ordinal = j + 1
target_address = upstream V1 designation address for target_designation_index
clockwise_offset = (target_address - origin_address) mod 12
```

Because frozen V1 places designation offset `j` at `address(life - j)`, the resulting
physical Z12 geometry is:

```text
clockwise_offset = (-j) mod 12
```

The compiler emits exactly 12 x 12 = 144 `RelativePalaceRoleFact` rows.

## Fact contract

Each fact contains:

- origin natal palace designation id;
- origin physical Address copied from upstream V1;
- relative ordinal `1..12`;
- relative role designation id from the frozen V1 role order;
- target natal palace designation id;
- target physical Address copied from upstream V1;
- clockwise Z12 offset from origin to target.

R2 never independently invents target addresses. Integrity validation requires every
origin and target address to match the supplied V1 `designation_bindings`, and every
resulting address edge to exist in the supplied R1 144-fact neutral topology.

## Geometry-only ordinal landmarks

Under the frozen V1 direction convention:

```text
relative ordinal 1 -> clockwise offset +0
relative ordinal 5 -> clockwise offset +8
relative ordinal 6 -> clockwise offset +7
relative ordinal 7 -> clockwise offset +6
relative ordinal 9 -> clockwise offset +4
```

These are geometry-only facts in V2-R2. This release does **not** attach traditional
labels such as 三方、对宫、气数位 or 一六共宗 to those ordinals.

## Independent profile

`ResolvedRelativePalaceFrameProfile` binds:

```text
R2 profile              ZIWEI-STRUCTURAL-RUNTIME-V2-R2@1.0.0
upstream Natal          ZIWEI-CHART-ENGINE-V1@1.0.0
upstream Structural R1  ZIWEI-STRUCTURAL-RUNTIME-V2-R1@1.0.0
frame algorithm         ZIWEI-RELATIVE-PALACE-FRAME@1.0.0
semantic rule set       disabled
```

Any named structural semantic rule-set binding fails closed in R2.

## Typed handoff and cross-chart gate

The public path is:

```text
validated NatalChartState + V1 HashBundle
+ validated StructuralState(V2-R1)
+ ResolvedRelativePalaceFrameProfile
-> ZiweiRelativePalaceFrameRuntime.generate(...)
-> RelativePalaceFrameState
```

A `ZiweiChartCandidate` may be handed off with `generate_from_candidate(...)`.

The runtime verifies that the supplied R1 StructuralState is explicitly bound to the
same V1 FactHash and ComputationHash as the supplied Natal computation. Mixing an R1
state from one chart with a Natal candidate from another chart fails closed.

## State and hash contract

`RelativePalaceFrameState` contains:

- upstream R1 Structural FactHash;
- upstream R1 Structural ComputationHash;
- resolved R2 profile;
- 144 canonical relative-frame facts;
- R2 IntegrityReport;
- R2 FactHash / ComputationHash;
- independent schema id `ZIWEI-RELATIVE-PALACE-FRAME-STATE-V2-R2`.

### R2 FactHash

Commits to:

```text
upstream R1 Structural FactHash
+ canonical 144 RelativePalaceRoleFact rows
```

### R2 ComputationHash

Additionally commits to:

```text
R2 FactHash
+ upstream R1 Structural ComputationHash
+ resolved R2 profile
+ R2 integrity/hash algorithm identity
```

Changing only upstream computation lineage, R2 profile version or frame-algorithm
version leaves the fact projection unchanged but changes ComputationHash.

## Integrity invariants

R2 enforces at least:

1. exactly 12 frozen origin designations;
2. exactly 144 facts;
3. exact canonical origin-order x ordinal-order serialization;
4. unique `(origin_designation_id, relative_ordinal)` keys;
5. every origin covers ordinals `1..12` exactly once;
6. every origin resolves all 12 natal palace targets exactly once;
7. role designation matches the relative ordinal;
8. target designation matches the rotational formula;
9. origin and target Addresses exactly match upstream V1 designation bindings;
10. offset matches the supplied addresses;
11. offset matches frozen V1 rotational geometry;
12. every relative-frame edge exists in upstream R1 neutral topology;
13. upstream R1 state passes its own integrity validation;
14. upstream V1/R1 profile identities match R2 bindings;
15. final state is bound to the exact supplied R1 hashes;
16. stored R2 hashes reproduce from canonical projections.

## Schema

Runtime JSON is independently validated by:

```text
schemas/ziwei-relative-palace-frame-v2-r2.schema.json
```

No V1 or R1 schema is expanded.

## Current source-closure map for later slices

The source audit established the following downstream boundaries:

- **Opposition / Sanfang-Sizheng / Qishu**: S04 contains explicit mappings, but named
  Sanfang/Sizheng activation is blocked by Issue #194 until its internal rows 07-12 are
  corrected through current higher-precedence canonical governance without mutating the
  retained historical payload.
- **Borrow-star projection**: current S06 contains a mechanical, opposite-only,
  non-recursive, fail-closed borrow closure algorithm. This belongs in a later
  Structural View / Projection slice because it projects physical stars for structural
  reading and must not mutate Base Chart placements.
- **夹宫**: no current mechanically closed active algorithm was established during this
  audit, so no rule is inferred from memory.

## Explicit non-goals

V2-R2 does not activate:

- 三方 / 三方四正;
- 对宫;
- 气数位;
- 一六共宗;
- 夹宫;
- 借星 / 借照;
- motif/configuration semantics;
- auspicious/inauspicious meaning;
- interpretation, scoring or prediction.

## Activation gate

Before V2-R2 is marked active, the merge-candidate branch must pass repository
bootstrap, `fortune-train verify`, the full unittest suite, the new exhaustive R2
algebra/integrity/hash/schema/cross-chart regressions, and a branch-to-main audit
showing no unintended V1 or V2-R1 changes.
