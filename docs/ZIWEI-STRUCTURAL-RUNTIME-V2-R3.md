# Ziwei Structural Runtime V2-R3

## Status

```text
RUNTIME_ID=ZIWEI-STRUCTURAL-RUNTIME-V2-R3
RUNTIME_VERSION=1.0.0
STATUS=ACTIVE_V2_R3
UPSTREAM_R2=ZIWEI-STRUCTURAL-RUNTIME-V2-R2@1.0.0
UPSTREAM_R1=ZIWEI-STRUCTURAL-RUNTIME-V2-R1@1.0.0
UPSTREAM_NATAL=ZIWEI-CHART-ENGINE-V1@1.0.0
ISSUE=#197
ACTIVATION_PR=#198
S04_SEMANTIC_BLOCKER=#194
```

V2-R3 is a Structural View / borrow-projection layer. It does not mutate V1 natal
placements, R1 neutral topology or R2 relative-palace frames, and it does not activate
named S04 Sanfang/Sizheng semantics.

## Current source contract

Current Git S06 supplies the active borrow-closure rules used by this runtime:

- a member palace is borrow-eligible only when it contains no fourteen principal stars;
- auxiliary, assistant, malefic and miscellaneous physical stars do not make the palace non-empty;
- borrowing reads the physical opposite only;
- a successful borrow projects all physical stars from that opposite, not only principal stars;
- applicable transformation activations at the physical source are projected as overlays;
- borrowed content is an interpretation/structural projection, not physical relocation;
- projection depth is one; recursive borrowing is forbidden;
- if the physical opposite also contains no principal star, status is
  `BORROW_SOURCE_EMPTY_OR_UNKNOWN`;
- a borrowed projection has `ZERO_SECOND_CONTRIBUTION=true`;
- member geometry is the physical set `{0,4,6,8}`.

The current source route does not mechanically close which of `+4/+8` should be called
left/right 合宫. R3 therefore treats them as an unordered semantic pair and stores only
their neutral offsets.

## State boundary

R3 introduces an independent `BorrowProjectionState` with:

- upstream R2 FactHash / ComputationHash binding;
- independent R3 profile;
- explicit `time_layer`;
- exactly 48 `BorrowClosureMemberFact` rows (12 evaluation origins x four member offsets);
- R3 IntegrityReport;
- independent FactHash / ComputationHash;
- independent JSON schema.

No upstream state object gains a field and no upstream hash changes.

## Projection model

For every evaluation origin, R3 selects the four R2 facts whose physical clockwise
offsets are exactly:

```text
0, 4, 6, 8
```

For each target:

```text
if target contains a principal star:
    DIRECT_PHYSICAL
    projected placements = all physical Placement objects at target

else:
    source = physical opposite(target)
    if source contains a principal star:
        BORROWED_DIRECT
        projected placements = all physical Placement objects at source
        projected transformations = all TransformationActivation objects at source
        ZERO_SECOND_CONTRIBUTION = true
    else:
        BORROW_SOURCE_EMPTY_OR_UNKNOWN
        no recursive projection
```

`Placement` objects are referenced directly from immutable V1 state. R3 does not create
new physical placements. `TransformationActivation` objects are likewise references to
the natal overlay. `RoleBinding`, ring objects and Dignity annotations are not treated as
borrowed stars. Dignity remains attached to the original physical entity/address and can
be joined downstream if a view requires it.

## Main-star emptiness

The emptiness predicate uses exactly the fourteen physical entity identities published by
the frozen V1 main-star placement generator (`ZIWEI_GROUP` + `TIANFU_GROUP`, 6 + 8 = 14).
It deliberately does not depend on the downstream Dignity registry. Presence of non-main
physical stars does not block borrowing.

## Physical deduplication key

`STRUCTURE_PHYSICAL_KEY` is independent of the evaluation view. It commits to:

- time layer;
- target raw address;
- physical source address;
- closure status;
- projected physical entity identities;
- projected transformation identities.

Therefore the same physical borrow/direct fact reached through multiple evaluation views
shares one key and cannot become multiple independent base contributions downstream.

## Time-layer boundary

The data model is explicitly time-layered because S06 defines the source contract over
natal or dynamic physical charts. R3 v1.0.0 activates only:

```text
NATAL
```

Unsupported dynamic layers fail closed. Later temporal integration may supply Daxian or
Annual transformation overlays without moving natal physical placements.

## Hash contract

R3 FactHash commits to:

```text
upstream R2 FactHash
+ time layer
+ canonical 48 member facts
+ projected entity identity / original physical coordinates
+ projected transformation identity
+ structure physical keys
```

R3 ComputationHash additionally commits to:

```text
R3 FactHash
+ upstream R2 ComputationHash
+ resolved R3 profile
+ S06 borrow source refs
+ R3 integrity/hash algorithm identity
```

Upstream V1/R1/R2 hashes remain unchanged.

## Explicit non-goals

R3 does not activate:

- named 三方 or 三方四正 semantics;
- the blocked S04 rows governed by #194;
- left/right 合宫 labels;
- pair-star strength ranking;
- motif/configuration interpretation;
- auspicious/inauspicious scoring;
- prediction;
- recursive borrowing;
- physical relocation of stars;
- dynamic temporal borrowing beyond `NATAL`.

## Release validation

The activation gate requires:

- exact 12 x 4 = 48 member coverage;
- `{0,4,6,8}` member geometry for every origin;
- physical-generator-derived fourteen-main-star identity;
- principal-star-only emptiness tests;
- auxiliary-only target borrow eligibility;
- exact all-Placement source projection;
- natal transformation overlay projection;
- direct vs borrowed vs double-empty fail-closed behavior;
- one-step recursion boundary;
- stable physical deduplication keys;
- deterministic hashes and replay;
- cross-chart binding rejection;
- tamper tests;
- JSON Schema validation;
- repository bootstrap, `fortune-train verify` and full unittest.
