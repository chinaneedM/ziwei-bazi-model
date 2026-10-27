# Ziwei Structural Runtime V2-R1

## Status

```text
RUNTIME_ID=ZIWEI-STRUCTURAL-RUNTIME-V2-R1
RUNTIME_VERSION=1.0.0
STATUS=ACTIVE_V2_R1
UPSTREAM_NATAL_RELEASE=ZIWEI-CHART-ENGINE-V1@1.0.0
ISSUE=#192
PR=#193
```

PR #193 is the activation change set for this runtime. When this document is present
on `main`, the neutral Structural Runtime V2-R1 contract described below is active.

This runtime is a separately versioned layer after the frozen Ziwei Chart Engine V1.
It does not redefine V1 NatalChartState, V1 calculation profiles, V1 hashes, V1
schemas, temporal output, view output, interpretation, or prediction.

## R1 boundary

R1 implements only the mathematically neutral Z12 topology. The canonical relation
space is the complete 12 x 12 matrix of ordered address pairs. Each fact contains:

```text
source Address
target Address
clockwise_offset in [0, 11]
```

The canonical order is source index 0..11, then target index 0..11. This produces
exactly 144 facts.

The runtime deliberately does not attach traditional names or behavioral meaning to
any offset. In particular, R1 does not encode 三方四正、对宫、夹宫、空宫借星、
气数位、一六共宗、motif/configuration semantics, auspicious/inauspicious meaning,
or prediction rules. Those require later current-Git canonical and profile closure.

## Independent profile

`ResolvedZiweiStructuralProfile` is independent of
`ResolvedZiweiCalculationProfile`. R1 binds:

```text
structural profile        ZIWEI-STRUCTURAL-RUNTIME-V2-R1@1.0.0
upstream natal profile    ZIWEI-CHART-ENGINE-V1@1.0.0
topology algorithm        NEUTRAL-Z12-TOPOLOGY@1.0.0
semantic rule set         disabled
```

Named semantic bindings are fail-closed in R1.

## Typed handoff

The public handoff is:

```text
validated NatalChartState
+ V1 HashBundle
+ ResolvedZiweiStructuralProfile
-> ZiweiStructuralRuntime.generate(...)
-> StructuralState
```

A `ZiweiChartCandidate` can be handed off directly with
`generate_from_candidate(...)`.

Structural generation re-validates the upstream NatalChartState, verifies that its
profile identity matches the frozen structural-profile binding, generates the neutral
144-fact matrix, runs structural integrity validation, computes structural hashes, and
then validates the completed StructuralState.

## StructuralState

`StructuralState` contains:

- upstream Natal FactHash;
- upstream Natal ComputationHash;
- resolved structural profile;
- 144 canonical AddressOffsetFact rows;
- structural IntegrityReport;
- structural HashBundle;
- independent schema identity `ZIWEI-STRUCTURAL-STATE-V2-R1`.

It is not added as a field to `NatalChartState`.

## Hash semantics

Structural hashing preserves the V1 two-layer distinction.

### Structural FactHash

The structural FactHash commits to:

```text
upstream Natal FactHash
+ canonical neutral topology facts
```

Therefore the same neutral topology attached to a different Natal canonical fact
identity produces a different Structural FactHash.

### Structural ComputationHash

The Structural ComputationHash commits to:

```text
Structural FactHash
+ upstream Natal ComputationHash
+ resolved structural profile
+ structural integrity/hash algorithm identity
```

Changing only upstream computation lineage or the structural profile leaves the
structural fact projection unchanged but changes Structural ComputationHash.

## Integrity invariants

R1 enforces:

1. exactly 144 topology facts;
2. exactly 144 unique ordered source/target pairs;
3. all 12 source addresses present;
4. all 12 target addresses present;
5. every source targets every Z12 address exactly once;
6. canonical Address index/branch identity;
7. `clockwise_offset == (target - source) mod 12`;
8. self offset equals zero;
9. canonical source-major/target-minor ordering;
10. valid upstream SHA-256 identities;
11. exact supported structural profile binding;
12. stored Structural FactHash and ComputationHash reproduce from canonical projections.

Algebra tests additionally exhaustively verify shift closure, inverse shift, offset
consistency and the pure geometric +6 involution without assigning it a traditional
semantic label. Hash-lineage tests explicitly verify both structural-profile and
topology-algorithm version changes affect ComputationHash while leaving the fact
projection unchanged.

## Schema

Runtime JSON is independently validated by:

```text
schemas/ziwei-structural-state-v2-r1.schema.json
```

The frozen V1 chart, temporal and view schemas are not expanded.

## Validation

Activation requires the repository's existing bootstrap/verify/full-unittest checks
plus the new exhaustive structural and schema tests to pass on the PR merge candidate.
PR #193 satisfies this gate before merge. Any future failure must be fixed within the
separate V2 layer unless it proves a genuine upstream V1 defect; V1 must not be
casually reopened to accommodate Structural Runtime implementation.
