# Formal blind-track workflow for new cases

This workflow applies only to new unrevealed cases. It must not be used to retroactively claim that an older prediction was sealed before option exposure.

## Phase 1: pre-option blind model

Create one independent candidate per track using schema `BLIND-TRACK-MODEL-V1`.

Required attestations:

- `phase` is `PRE_OPTION`;
- `option_visibility` is `false`;
- `other_track_visibility` is `false`;
- `answer_access_performed` is `false`;
- the Ziwei parent chain uses S05-S10 plus allowed shared libraries;
- the Bazi parent chain uses S11-S16 plus allowed shared libraries;
- the blind model body contains no question IDs, option IDs, TOP1/TOP2, pairwise rows, direction matrices, compound coverage, or formal exact assertions.

Seal each track before option projection:

```bash
fortune-v1 blind-track-seal \
  --candidate work/CASE-NEW-001-ziwei-blind.json \
  --frozen-root frozen/blind-tracks

fortune-v1 blind-track-seal \
  --candidate work/CASE-NEW-001-bazi-blind.json \
  --frozen-root frozen/blind-tracks
```

The command writes an immutable blind model, a machine validation receipt, and a real `blind_model_hash` derived from canonical JSON bytes.

## Phase 2: local option adjudication

After the blind model is sealed, each track may receive the option atoms. Each track must adjudicate independently and write a `TRACK-LOCAL-ADJUDICATION-V1` object containing:

- the exact `blind_model_hash` from its phase-1 receipt;
- one question ID;
- one track ID;
- an S18 local adjudication object ID;
- parent object IDs for coverage, direction, compound coverage, and pairwise adjudication;
- `answer_access_performed=false`;
- `other_track_visibility=false`.

Create the local seal:

```bash
fortune-v1 local-track-seal \
  --adjudication work/CASE-NEW-001-Q1-ziwei-adjudication.json \
  --blind-receipt frozen/blind-tracks/BLIND-.../blind-track-seal-receipt.json \
  --output work/CASE-NEW-001-Q1-ziwei-local-seal.json
```

The resulting object contains every field required by the formal prediction validator:

- `seal_id`;
- `canonical_hash`;
- `body_hash`;
- `machine_validation_report_id`;
- `validation_status=PASS`;
- `s18_local_adjudication_object_id`;
- `parent_object_ids`.

## Phase 3: fusion and formal run

Only after both independent local seals pass may S03 read them. The final `PREDICTION-RUN-V1` must reference the real blind model hashes and local seal objects. Formal freezing is performed only by the existing `fortune-v1 freeze` command after the complete run passes `validate_prediction_run`.

## Fail-closed rules

- A missing pre-option seal cannot be replaced by a retrospective hash.
- A track cannot use the other track's parent libraries.
- The same blind seal ID cannot be overwritten.
- Answer-bearing content is rejected.
- If one track is invalid, S03 formal fusion is not performed.
- Historical cases that lack valid pre-option seals remain relative replay records only.
