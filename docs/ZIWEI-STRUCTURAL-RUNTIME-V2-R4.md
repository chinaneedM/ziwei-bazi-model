# Ziwei Structural Runtime V2-R4

## Status

```text
RUNTIME_ID=ZIWEI-STRUCTURAL-RUNTIME-V2-R4
RUNTIME_VERSION=1.0.0
STATUS=ACTIVE_V2_R4
ACTIVATION_CONDITION=MERGED_TO_MAIN
UPSTREAM_FRAME_RELEASE=ZIWEI-STRUCTURAL-RUNTIME-V2-R2@1.0.0
CANONICAL_SOURCE=S04
CANONICAL_SOURCE_SHA256=f7720ee4a11ce36155007cc3846620bcebdeaf5d98447c4abe427b37348e6c4f
SEMANTIC_RULE_SET=S04-SANFANG-SIZHENG-CORRECTION-R1@1.0.0
ISSUE=#200
PR=#201
```

PR #201 is the activation change set. The status above is effective only when this
document is present on `main`.

V2-R4 is the first named Structural Runtime semantic layer. It binds the already-active
V2-R2 relative-palace geometry to current-Git S04 semantics after the #194 canonical
correction. It does not modify V1, R1, R2 or R3 contracts.

## Activated semantics

R4 activates only:

- 对宫 / opposition;
- 三方 / trine group;
- 三方四正 / origin-centered structural frame.

The source-bound invariant is:

```text
OPPOSITION = shift(source, +6)
TRINE_SET = {shift(source, +4), shift(source, +8)}
SANFANG_SIZHENG = {source} union TRINE_SET union {OPPOSITION}
```

No interpretive weight, auspicious/inauspicious meaning, motif, prediction, 气数位,
一六共宗 or 夹宫 semantics are introduced.

## Why R4 is separate from R2

R2 is frozen as an interpretation-free coordinate frame and explicitly rejects named
semantic rule-set bindings. R4 therefore consumes validated R2 state and owns semantic
source lineage independently.

R3 borrow projection remains separately active. R4 does not require R3 because named
Sanfang/Sizheng identity is a relation over the physical/relative geometry itself.
Applications may compose R3 projection and R4 named relation views downstream without
mutating either layer.

## Canonical semantic identity

R4 avoids materializing every directed relation as independent evidence. It emits:

```text
6  OppositionAxisFact
4  TrineGroupFact
12 SanfangSizhengFrameFact
--------------------------
22 canonical semantic facts
```

### OppositionAxisFact

A physical opposition is stored once as an unordered canonical two-palace axis. Both
query directions reference the same `axis_key`.

### TrineGroupFact

A three-palace `{0,+4,+8}` orbit is stored once. All three palace perspectives reference
the same `group_key`.

### SanfangSizhengFrameFact

Each of the 12 natal palace designations receives one query-facing frame containing:

- origin palace/address;
- canonical trine-group key;
- the `+4` and `+8` trine partners;
- canonical opposition-axis key;
- the `+6` opposition target.

The frame is not an additional independent structural cause. The axis/group keys expose
shared physical semantic identity for downstream evidence deduplication.

## Source binding

`ResolvedNamedStructuralSemanticProfile` binds:

```text
R4 profile                    ZIWEI-STRUCTURAL-RUNTIME-V2-R4@1.0.0
upstream R2                   ZIWEI-STRUCTURAL-RUNTIME-V2-R2@1.0.0
semantic compiler             ZIWEI-NAMED-SANFANG-SIZHENG@1.0.0
canonical source              S04
canonical source SHA256       f7720ee4a11ce36155007cc3846620bcebdeaf5d98447c4abe427b37348e6c4f
canonical manifest object     da7b511bb5734c09febccbe0ed54170490c27a6c0249df79e87c496f10d3e5e6
semantic rule set             S04-SANFANG-SIZHENG-CORRECTION-R1@1.0.0
```

Unsupported source, manifest, algorithm, rule-set or profile identities fail closed.
Regression verifies these constants against current `sources/canonical-manifest.json`,
`config/source-policy.json`, and the active S04 runtime segment.

## Typed handoff

```text
validated RelativePalaceFrameState(V2-R2)
+ ResolvedNamedStructuralSemanticProfile
-> ZiweiNamedStructuralSemanticRuntime.generate(...)
-> NamedStructuralSemanticState(V2-R4)
```

R4 requires R2 to retain its disabled semantic fields. A mutated R2 semantic profile is
rejected because named semantics belong exclusively to R4.

Before semantic compilation, R4 also re-validates R2 self-consistency without changing
R2: it validates the frozen R2 profile, verifies R2 integrity-algorithm identity, and
recomputes the R2 hash bundle from the stored upstream lineage and all 144 frame facts.
A stale `PASS` flag and stale hashes therefore cannot hide a tampered R2 fact, including
facts at offsets that R4 itself does not use.

## Hash contract

R4 FactHash commits to:

```text
upstream R2 FactHash
+ canonical 6 OppositionAxis facts
+ canonical 4 TrineGroup facts
+ canonical 12 SanfangSizhengFrame facts
```

R4 ComputationHash additionally commits to:

```text
upstream R2 ComputationHash
+ resolved R4 profile
+ canonical S04 / manifest / rule-set lineage
+ R4 integrity/hash algorithm identity
```

Therefore a source/profile lineage change that preserves the same semantic fact
projection preserves FactHash but changes ComputationHash.

## Integrity gate

R4 validates at least:

1. R2 profile is valid and compatible with the R4 binding;
2. R2 integrity status and integrity-algorithm identity match the frozen R2 release;
3. all 144 R2 facts plus stored upstream lineage reproduce the stored R2 hashes;
4. R2 remains interpretation-free;
5. exactly 6 opposition axes covering all 12 designations once;
6. every axis is a reciprocal physical `+6` relation;
7. exactly 4 trine groups covering all 12 designations once;
8. every group is the exact `{0,+4,+8}` orbit from R2;
9. exactly 12 Sanfang/Sizheng frames, one per designation;
10. frame trines are exact `+4/+8` R2 targets;
11. frame opposition is exact `+6` R2 target;
12. every frame references the correct canonical group and axis;
13. each frame contains exactly four unique palace identities;
14. state binds the exact supplied R2 FactHash and ComputationHash;
15. stored R4 hashes reproduce from canonical projections.

## Schema

Independent runtime JSON schema:

```text
schemas/ziwei-named-structural-semantics-v2-r4.schema.json
```

No earlier schema is expanded.

## Explicit non-goals

V2-R4 does not activate:

- 气数位;
- 一六共宗;
- 夹宫;
- additional borrow rules;
- dignity reinterpretation;
- motif/configuration semantics;
- evidence weights;
- auspicious/inauspicious scoring;
- natural-language fortune interpretation;
- prediction.

## Release validation gate

PR #201 must pass on its final merge-candidate head:

- current-main base and `behind=0`;
- only R4/schema/test/doc additions;
- source binding matches current Git #194 correction;
- exhaustive 6-axis / 4-group / 12-frame invariants;
- corrected S04 rows 07-12 materialize exactly;
- deterministic hash ordering;
- source/profile lineage separation between FactHash and ComputationHash;
- axis/group/frame tamper rejection;
- cross-R2 composition rejection;
- stale-PASS/stale-hash R2 tamper rejection;
- R2 integrity-algorithm lineage rejection;
- JSON Schema validation;
- repository bootstrap PASS;
- `fortune-train verify` PASS;
- full unittest PASS.

No named structural semantics are active merely because this file exists on a feature
branch. V2-R4 becomes active only when the final validated PR #201 head is merged to
`main`.
