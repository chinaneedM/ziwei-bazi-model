# ZiWei Full Minor Limit Sequence Presentation + Selection R1

## Scope

This milestone closes the released-core-to-Workbench presentation gap for the Zi Wei Minor-Limit sequence. It does not add or change any Minor-Limit, Daxian, annual, monthly, transformation, auxiliary-star, calendar, or time rule.

The Workbench exposes the complete released `ZiweiTemporalState.minor_limit_frames` sequence in a bounded scrollable list and lets a user copy a released nominal age into the existing `ziwei_minor_limit_age` selector by clicking a row.

Prediction, auspiciousness, strength, doctrinal arbitration, and interpretation remain out of scope.

## Released source contract

The browser consumes `ApplicationChartBundle.temporal_state.minor_limit_frames` only. Each accepted released row must already carry these identities:

- `frame_id`
- `nominal_age`
- `active_address.index`
- `active_address.branch`
- `source_refs`

The Workbench preserves source order, rejects duplicate `frame_id` or `nominal_age`, requires non-empty released source references, and hides the sequence if any row is malformed. It does not sort, repair, infer, or synthesize missing Minor-Limit facts.

## Runtime lineage

The existing engine remains authoritative:

- temporal algorithm: `ZIWEI-TEMPORAL-FRAMES-V1@1.6.0`
- temporal rule set: `S10_CURRENT_TEMPORAL_R1@1.6.0`
- Minor-Limit source: `S10:中州派动态坐标生成补充:小限`

`ZiweiTemporalEngine.generate` already emits `minor_limit_frames` for every nominal age in the generated temporal range. `ZiweiChartService` owns that temporal range and the selected Minor-Limit age. The browser does not reproduce the birth-year-branch start mapping, sex direction, palace stepping, or frame-id construction.

The released Minor-Limit frame does not contain Daxian direction, a Minor-Limit direction field, start-address metadata, step count, or active-palace Ganzhi. The Workbench therefore does not synthesize any of them.

## Workbench presentation

`src/fortune_training/combined_chart_application/ziwei_basic_info_assets.py` adds:

- `minorLimitSequence(temporalState)` — strict copy projection from released `minor_limit_frames`;
- `renderMinorLimitSequence(temporalState, selectedMinorLimit)` — bounded read-only list rendering plus exact selected-row identity marking;
- `fillMinorLimitTarget(nominalAge)` — copies only a validated released integer nominal age into the existing `#ziwei-minor-limit-age` input.

A rendered row shows only released frame identity, nominal age, active branch, and source references. When the released selected-temporal summary contains a Minor-Limit row, selection highlighting requires both its released `frame_id` and released `nominal_age` to match the list row.

Clicking a row:

1. copies the released `nominal_age` to the existing Minor-Limit age selector;
2. emits normal `input` and `change` events;
3. focuses that selector;
4. does **not** construct `MINOR:age=<n>` in JavaScript;
5. does **not** change Daxian or annual selectors;
6. does **not** auto-submit the form.

A subsequent normal resolve remains the only operation that asks the server to select that Minor-Limit target.

## Separation from existing parity rows

The full Minor-Limit sequence is distinct from `ZIWEI_SELECTED_MINOR_LIMIT_FRAME_SUMMARY`, which exposes only the currently selected Minor-Limit frame in the released view/SVG. It is also independent from Daxian direction/first-age metadata and must never reuse `daxian_direction` as a Minor-Limit direction.

The existing Zi Wei JSON export already preserves the canonical temporal state, including released `minor_limit_frames` and their source references. This milestone adds no parallel export calculation.

## Verification

Focused test: `tests/test_combined_workbench_ziwei_minor_limit_sequence_r1.py`.

Milestone closure requires same-SHA PASS for:

- `fortune-train verify`
- full `unittest` discovery
- `combined-workbench-smoke`
