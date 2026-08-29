# Fusion Chart ZiWei Daxian Sequence Selection R1

## Status

R1 Workbench interaction closure for the already-released Zi Wei Daxian sequence.

This milestone adds no astrology rule and no new deterministic field. It only lets a user copy an already-released `daxian_frames[].frame_id` into the Workbench's existing optional `ziwei_daxian_frame_id` target input by clicking the corresponding displayed Daxian row.

## Released identity source

The identity source remains the validated temporal bundle:

- `ZiweiTemporalState.daxian_frames`
- `DaxianFrame.frame_id`

The browser does not construct a frame ID from `index`, age, year, palace, direction or any other field. The temporal engine remains the sole owner of Daxian frame generation and identity.

## Workbench interaction contract

`src/fortune_training/combined_chart_application/ziwei_basic_info_assets.py` continues to validate the complete released Daxian sequence before rendering it.

For every valid rendered row:

1. the row is a `button` with `type="button"`;
2. its click handler passes the copied released `row.frameId` to `fillDaxianTarget`;
3. `fillDaxianTarget` writes that exact string into the existing `ziwei-daxian-frame-id` input;
4. normal bubbling `input` and `change` events are dispatched;
5. focus moves to the target input so the user can inspect or edit the selection.

The click does **not** submit the form. The existing `chart-form` submit path remains the only path that requests a new combined resolution.

## Deterministic boundary

The browser must not:

- synthesize `DAXIAN:index=N` from a numeric index;
- concatenate a Daxian ID prefix with any browser-computed value;
- derive Daxian direction, start age, age/year intervals, palace stepping or palace Ganzhi;
- repair, sort or select from malformed/duplicate released frame rows;
- auto-submit after a click;
- choose a doctrinal winner or infer predictive meaning.

Malformed or duplicate released Daxian sequence identity continues to fail closed at the existing `daxianSequence` validation boundary, so no selectable row is produced from invalid input.

## Field parity receipt

No new Field Parity Matrix row is introduced because this milestone does not release a new deterministic field. The existing `ZIWEI_DAXIAN_SEQUENCE_FRAMES` row remains the canonical parity record for the complete Daxian sequence.

The distinction is intentional:

- `ZIWEI_DAXIAN_SEQUENCE_FRAMES` records the released/rendered deterministic data field;
- this R1 records a Workbench affordance that passes an existing released `frame_id` into an existing target selector input.

`ZIWEI_SELECTED_DAXIAN_FRAME_SUMMARY` remains independently responsible for displaying the server-selected Daxian frame after the user submits a target selection.

## Verification

Focused tests verify:

- the 1994-05-17 14:30 Beijing fixture releases the expected unique Daxian frame identities;
- the existing Workbench target input is present;
- the sequence uses non-submitting buttons;
- click handling copies `row.frameId` exactly;
- browser source contains no Daxian frame-ID construction and no auto-submit path;
- Field Parity remains represented by the existing full-sequence row rather than a pseudo-field for UI selection.

Milestone closure requires the exact implementation SHA to pass `fortune-train verify`, the full unittest suite and `combined-workbench-smoke`.
