# Ziwei Structural Runtime V2-R5

## Status

```text
RUNTIME_ID=ZIWEI-STRUCTURAL-RUNTIME-V2-R5
RUNTIME_VERSION=1.0.0
STATUS=ACTIVE_V2_R5
ACTIVATION_CONDITION=MERGED_TO_MAIN
UPSTREAM_R3=ZIWEI-STRUCTURAL-RUNTIME-V2-R3@1.0.0
UPSTREAM_R4=ZIWEI-STRUCTURAL-RUNTIME-V2-R4@1.0.0
ISSUE=#202
PR=#203
```

The status above is effective only when this document is present on `main`. A feature-branch copy is not an active release.

V2-R5 is a pure composition layer joining the active R3 borrow-projection state with the active R4 named Sanfang/Sizheng semantic state. It introduces no new physical placement, geometry, borrowing rule, named semantic rule, interpretation, scoring, or prediction meaning.

## Composition contract

For every natal evaluation origin R5 exposes exactly four ordered member roles:

```text
SELF            = +0
TRINE_PLUS_4    = +4
OPPOSITION      = +6
TRINE_PLUS_8    = +8
```

The member target and borrow closure come from R3. The trine-group and opposition-axis identities come from R4.

Expected query-facing materialization:

```text
12 ResolvedSanfangSizhengFrameFact
48 ResolvedStructuralMemberRef
```

These records are view/composition metadata and are not 60 new evidence causes.

## No duplicated physical payload

R5 does not copy R3 `projected_placements` or `projected_transformations`. A member reference carries the deterministic R3 lookup identity plus the existing `structure_physical_key`. Applications dereference R3 when physical payload is required.

`physical_source_address` is derived without a second borrow pass:

```text
DIRECT_PHYSICAL                 -> target_raw_address
BORROWED_DIRECT                 -> borrowed_from_raw_address
BORROW_SOURCE_EMPTY_OR_UNKNOWN  -> null
```

## Evidence identity

R5 preserves two independent upstream deduplication domains:

- R3 `structure_physical_key` remains the physical-resolution identity;
- R4 `axis_key` and `group_key` remain named semantic identities.

The R5 frame itself is not an additional independent evidence cause.

## Cross-binding gate

R3 and R4 must descend from the exact same R2 state:

```text
R3.upstream_relative_frame_fact_hash
== R4.upstream_r2_fact_hash

R3.upstream_relative_frame_computation_hash
== R4.upstream_r2_computation_hash
```

R5 also requires frozen R3/R4 profile identities, canonical PASS integrity algorithm identities, reproducible upstream state hashes, and the active R3 `NATAL` time layer. Cross-chart, cross-R2, stale-hash, tampered-upstream, or unsupported dynamic composition fails closed.

## Hash contract

R5 FactHash commits to:

- upstream R3 FactHash;
- upstream R4 FactHash;
- time layer;
- canonical 12 resolved frames / 48 member references;
- referenced physical/semantic identities and composition coordinates.

R5 ComputationHash additionally commits to:

- upstream R3 ComputationHash;
- upstream R4 ComputationHash;
- resolved R5 profile;
- R5 composition/integrity/hash algorithm identity.

Canonical source authority is inherited through the validated R3/R4 computation lineage; R5 does not duplicate S04/S06 source bindings.

## Release integrity gate

Before composition, R5 replays both upstream state hash bundles from their stored facts, profiles, and lineage, and checks the frozen R3/R4 integrity algorithm identities. Therefore stale `PASS` reports and stale hashes cannot hide tampered R3 member facts or tampered R4 semantic facts.

The merge-candidate gate requires:

- current-main base and `behind=0`;
- only R5/schema/test/doc additions;
- bootstrap PASS;
- `fortune-train verify` PASS;
- full unittest PASS;
- R3/R4 stale-PASS/hash tamper rejection;
- cross-R3/R4 R2 lineage rejection;
- deterministic composition/hash ordering;
- JSON Schema validation.

## Explicit non-goals

V2-R5 does not activate:

- 气数位;
- 一六共宗;
- 夹宫;
- left/right 合宫 naming;
- pair-strength ranking;
- motif/configuration semantics;
- dynamic borrowing beyond NATAL;
- auspicious/inauspicious scoring;
- interpretation or prediction.

## Foundation Exit role

R5 is the final mandatory Structural Runtime slice in the current Foundation Exit Gate. After activation, the next task is a vertical Foundation Exit Audit over:

```text
BirthInput
-> Ziwei Chart Engine V1
-> Temporal Runtime
-> Structural R1/R2/R3/R4/R5
-> deterministic serialization/application handoff
```

气数位 may be added only as a small directed-semantic identity closure if the Exit Audit shows it materially improves application handoff. It must not reopen broad Foundation expansion.
