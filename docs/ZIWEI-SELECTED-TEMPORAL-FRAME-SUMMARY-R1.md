# Zi Wei Selected Temporal Frame Summary R1

## Scope

This milestone closes a deterministic presentation gap in the Zi Wei application surface. The temporal engine already releases selected Daxian, Annual, Monthly and Minor-Limit frame facts, while the released `ChartViewModel` previously exposed only their frame IDs plus palace overlays. The Workbench therefore lacked a compact, human-readable summary of the exact selected temporal coordinates.

No temporal rule is added or changed here. Prediction, strength, auspiciousness, transformation-success judgments and doctrinal arbitration remain out of scope.

## Release boundary

`ZiweiViewProjectionCompiler` remains the release boundary. After the existing selectors resolve the exact `DaxianFrame`, `AnnualFrame`, `MonthlyFrame` and `MinorLimitFrame`, the compiler copy-projects canonical fields into `ViewSelectedTemporalFrameSummary` and stores it on `ChartViewModel`.

Because `ChartViewModel` is serialized into the normal view payload, the summary is included in `view_hash`, application export and bundle replay validation. A stored summary that no longer reproduces from the selected canonical frames therefore fails closed through the existing `APPLICATION_VIEW_REPLAY_MISMATCH` boundary.

The SVG renderer consumes only `view.selected_temporal_frame_summary`. The combined local Workbench continues to inject the server-produced `ziwei_svg` directly; it does not read `temporal_state` or run a second selector/calculation path in JavaScript.

## Released summary fields

### Selected Daxian

- `frame_id`
- `index`
- `nominal_age_start`
- `nominal_age_end`
- `absolute_year_start`
- `absolute_year_end`
- `active_address_index`
- `active_branch`
- `active_palace_ganzhi`

### Selected Annual frame

- `frame_id`
- `absolute_year`
- `nominal_age`
- `year_stem`
- `year_branch`
- `active_address_index`
- `active_branch`
- `active_palace_ganzhi`

### Selected Monthly frame

- `frame_id`
- `absolute_year`
- `lunar_month`
- `month_stem`
- `month_branch`
- `month_ganzhi`
- `active_address_index`
- `active_branch`
- `calendar_scope`
- `leap_month_policy_status`

`MonthlyFrame` does not release `active_palace_ganzhi`, `year_stem` or `year_branch`. R1 therefore does not synthesize those fields by joining other frames.

### Selected Minor Limit

- `frame_id`
- `nominal_age`
- `active_address_index`
- `active_branch`

`MinorLimitFrame` does not release a direction, start address or step count. R1 therefore does not borrow `daxian_direction` or invent any Minor-Limit direction metadata.

## Presentation

SVG renderer `1.3.0` adds a compact chart-center summary for the selected frames. It performs string formatting only. `show_temporal=False` suppresses the new summary together with the existing temporal presentation layer.

The existing `ZIWEI-CHART-VIEW-MODEL-V1` schema identity is retained because this is an additive release-field extension rather than a semantic replacement of the view model. The strict JSON schema is updated so the new summary and all four type-specific field contracts remain validated under `additionalProperties: false`.

## Governance

The Fusion Chart Field Parity Matrix registers the four selected-frame summaries as `ALREADY_VISIBLE` only after the released view, strict schema and server SVG surface exist together. The implementation does not modify `ziwei_chart/temporal.py`.

Closure requires focused tests plus the standard same-HEAD GitHub Actions gates:

- fortune-train verify
- full unittest
- combined-workbench-smoke
