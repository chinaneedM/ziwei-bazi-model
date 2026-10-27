# Fusion Chart ZiWei Full Daxian Sequence Presentation R1

## Status

R1 presentation closure for the already-released Zi Wei Daxian frame sequence.

This milestone does **not** add or change a Daxian calculation rule. It exposes the validated `ZiweiTemporalState.daxian_frames` contract in the unified Workbench as a read-only sequence.

## Released source contract

The runtime source remains `src/fortune_training/ziwei_chart/temporal.py`:

- `ZiweiTemporalState.daxian_frames`
- `DaxianFrame.frame_id`
- `DaxianFrame.index`
- `DaxianFrame.nominal_age_start`
- `DaxianFrame.nominal_age_end`
- `DaxianFrame.absolute_year_start`
- `DaxianFrame.absolute_year_end`
- `DaxianFrame.active_address`
- `DaxianFrame.active_palace_ganzhi`

Existing runtime lineage is unchanged:

- temporal algorithm: `ZIWEI-TEMPORAL-FRAMES-V1`
- temporal rule set: `S10_CURRENT_TEMPORAL_R1`
- Daxian source reference: `S10:中州派动态坐标生成补充:大限`

The existing engine remains the sole owner of direction, first nominal age, palace stepping, age ranges, Gregorian-year ranges and palace Ganzhi generation.

## Workbench contract

`src/fortune_training/combined_chart_application/ziwei_basic_info_assets.py` reads only `combined_resolution.ziwei_bundle.temporal_state.daxian_frames` from a successful `/api/resolve` response.

The presentation validates each released row before rendering. A valid sequence requires:

- a non-empty frame array;
- non-empty `frame_id` values;
- integer `index`, nominal-age bounds and Gregorian-year bounds;
- a valid released `active_address.index` and non-empty `active_address.branch`;
- a non-empty released `active_palace_ganzhi`;
- non-reversed age/year ranges;
- unique `frame_id` and unique `index` values.

If any row fails this identity/shape validation, the entire full-sequence section is hidden. The browser does not repair, infer, sort, step or regenerate missing Daxian values.

The visible row is therefore only a formatting projection of released values:

`frame_id · nominal-age range · Gregorian-year range · active palace Ganzhi/branch`

The DOM also retains released frame/index/address-index identities as data attributes for presentation identity only.

## Separation from existing parity fields

`ZIWEI_DAXIAN_SEQUENCE_METADATA` remains the independent field for:

- Daxian direction;
- first Daxian nominal age.

`ZIWEI_SELECTED_DAXIAN_FRAME_SUMMARY` remains the independent field for the currently selected Daxian frame rendered by the server-side SVG.

This R1 adds `ZIWEI_DAXIAN_SEQUENCE_FRAMES` for the **complete released Daxian frame list**. It does not replace or broaden either existing parity row.

Dynamic designation overlays, Four-Transformation activations and temporal auxiliary/candidate surfaces carried by individual `DaxianFrame` rows remain governed by their already-existing parity contracts. They are not duplicated in this basic sequence list.

## Deterministic boundary

The browser explicitly does not implement the engine expressions that generate Daxian frames, including:

- Life-Palace stepping by Daxian direction;
- bureau-number-derived first age;
- ten-year interval construction;
- Gregorian-year conversion from Zi Wei birth year and nominal age;
- palace stem/Ganzhi derivation.

Focused tests inspect the released service payload and assert that the Workbench source consumes the released fields while excluding the core generation expressions.

## Smoke receipt

`combined-workbench-smoke.py` now verifies the released sequence count, required frame identity fields, range shape and uniqueness. It records `ziwei_daxian_sequence_count` in the smoke receipt.

The smoke check does not duplicate any Daxian astrology arithmetic.
