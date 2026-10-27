# Shared Ziwei Target Projection Productization R1 (R1.10)

## Scope

R1.10 productizes the existing `SharedZiweiSelectorProjectionService` inside the released local combined target-flow path. It does **not** create another Ziwei temporal engine and does not change the released Ziwei application bundle, BaZi application-flow bundle, BaZi temporal ShenSha sidecar, or combined target-flow binding hashes.

The public `/api/resolve-flow` response now carries an additive `shared_ziwei_selector_projection` object. The existing `/api/shared-ziwei-projection` workflow remains the explicit UI/application path for writing a chosen projection candidate into Ziwei selectors.

## Shared target-coordinate lineage

The combined target-flow service already resolves the target coordinate for BaZi. The local product adapter deterministically replays that same target-coordinate foundation from the exact `TargetTemporalInput` and resolved profile, then requires its fact and computation hashes to match the hashes embedded in `bazi_target_flow_bundle`.

If either hash differs, the unified endpoint fails closed with `LOCAL_APP_SHARED_ZIWEI_TARGET_COORDINATE_MISMATCH`. The Ziwei projection therefore cannot silently use a caller-invented or independently drifted target coordinate.

Each Ziwei projection candidate retains:

- `source_target_candidate_index`
- `source_target_candidate_id`
- sample index and reported local datetime
- UTC instant and DST `fold`
- the exact Ziwei application bundle and temporal hashes
- the exact shared target-coordinate fact/computation hashes

DST folds and other coordinate ambiguity remain explicit candidates.

## Ziwei temporal semantics

No doctrinal arbitration is added in R1.10.

- Flow day remains a source-bound text rule (`S10-FLOW-MONTH-FIRST-DAY-FORWARD-R1`, including `S10:ZZTERM-P-0274` lineage).
- Flow hour remains `CANDIDATES_PRESERVED_NO_SELECTED_FRAME`.
- Hour method candidates retain `CASE_METHOD_ONLY_NOT_GLOBAL_RULE`.
- The Zhongzhou/Luoyang mean-solar-time and local-apparent-solar-time methods remain parallel candidates.
- No hourly winner is auto-selected.
- Leap lunar month handling remains fail-closed rather than fabricating a regular month frame.
- No auspiciousness, strength, judgment, prediction, or interpretation semantics are introduced.

The existing Workbench shared-apply panel remains the user-facing explicit Ziwei application workflow and already states these neutral semantics. The unified target-flow response is read-only product data and does not mutate Ziwei selectors or SVG state.

## Full replay gate

Both public Ziwei target-projection paths execute the same full replay gate before returning projection data:

- `/api/resolve-flow`
- `/api/shared-ziwei-projection`

Each path calls `validate_shared_ziwei_selector_full_replay(...)` against the exact released Ziwei application bundle, resolved shared target coordinate, resolved target profile, and generated projection. A dataclass mismatch between the original result and an independent service replay fails closed with `LOCAL_APP_SHARED_ZIWEI_FULL_REPLAY_FAILED`.

The standalone endpoint therefore cannot return a projection that has not passed the same deterministic replay requirement as the unified target-flow endpoint. Its successful response envelope and projection serialization remain unchanged.

This sits on top of the existing structural integrity checks, candidate hashes, projection fact/computation hashes, and exact source-lineage replay in `shared_time_integrity.py`.

## Strict response contract

`schemas/combined-local-target-flow-response-r1.schema.json` now requires the additive `shared_ziwei_selector_projection` envelope and rejects unknown fields at that envelope level. The standalone `shared-ziwei-selector-projection-r1.schema.json` remains the authoritative strict schema for the full projection payload.

Regression coverage verifies:

1. exact Ziwei application bundle binding;
2. exact BaZi/shared target-coordinate hash binding;
3. candidate ID equivalence across BaZi and Ziwei target projections;
4. deterministic daily rule lineage;
5. preservation of both hourly case-method candidates with no selected hour;
6. DST fold candidate preservation;
7. fail-closed full replay on the unified endpoint;
8. rejection of injected prediction fields by the unified response schema;
9. fail-closed full replay on the standalone `/api/shared-ziwei-projection` endpoint while retaining the pre-existing successful response contract.

## Compatibility boundary

R1.10 is additive. It does not alter:

- `ZIWEI-BAZI-COMBINED-TARGET-FLOW-RESOLUTION-R1` hashes;
- `BAZI-APPLICATION-FLOW-RESOLUTION-R1`;
- `BAZI-TEMPORAL-SHENSHA-PROJECTION-SIDECAR-R1`;
- Ziwei application bundle hashes or selector semantics;
- the legacy `/api/resolve` response.

No main-branch merge or release is part of this milestone.
