# ZiWei Full Annual Sequence Presentation + Selection R1

## Scope

This milestone closes a released-core-to-Workbench presentation gap for the Zi Wei annual sequence. It does not add or change any annual, Doujun, Daxian, transformation, auxiliary-star, calendar, or time rule.

The Workbench now exposes the complete released `ZiweiTemporalState.annual_frames` sequence in a bounded scrollable list and lets a user copy a released annual year into the existing `ziwei_annual_year` selector by clicking a row.

Prediction, auspiciousness, strength, doctrinal arbitration, and interpretation remain out of scope.

## Released source contract

The browser consumes `ApplicationChartBundle.temporal_state.annual_frames` only. Each accepted `AnnualFrame` must already carry these released identities:

- `frame_id`
- `absolute_year`
- `nominal_age`
- `year_stem`
- `year_branch`
- `active_address.index`
- `active_address.branch`
- `active_palace_ganzhi`
- `doujun_address.index`
- `doujun_address.branch`
- `doujun_rule_id`
- `parent_daxian_frame_id` (`null` before the first Daxian is allowed)

The Workbench preserves source order, rejects duplicate `frame_id` or `absolute_year`, and hides the sequence if any row is malformed. It does not sort, repair, infer, or synthesize missing annual facts.

## Runtime lineage

The existing engine remains authoritative:

- temporal algorithm: `ZIWEI-TEMPORAL-FRAMES-V1@1.6.0`
- temporal rule set: `S10_CURRENT_TEMPORAL_R1@1.6.0`
- annual source: `S10:中州派动态坐标生成补充:流年太岁与斗君`
- standard Doujun sources: `S01:ZZQS-A-1935`, `S10:ZZZA-A-1127`, `S10:ZZZA-A-1128`
- standard Doujun rule: `S10-SUIJIAN-REVERSE-BIRTH-MONTH-FORWARD-BIRTH-HOUR-R1`

`ZiweiChartService` owns temporal-range expansion and calls `ZiweiTemporalEngine.generate`. The browser does not reproduce annual nominal-age arithmetic, sexagenary-year lookup, annual palace placement, parent-Daxian binding, Doujun calculation, or annual frame-id construction.

## Workbench presentation

`src/fortune_training/combined_chart_application/ziwei_basic_info_assets.py` adds:

- `annualSequence(temporalState)` — strict copy projection from released `annual_frames`;
- `renderAnnualSequence(temporalState)` — bounded read-only list rendering;
- `fillAnnualTarget(absoluteYear)` — copies only a validated released integer year into the existing `#ziwei-annual-year` input.

A rendered row shows released frame identity, released year Ganzhi components, nominal age, active palace Ganzhi/branch, and Doujun branch. Long sequences are constrained by a scroll container rather than expanding the whole Workbench page.

Clicking a row:

1. copies the released `absolute_year` to the existing annual-year scalar selector;
2. emits normal `input` and `change` events;
3. focuses that selector;
4. does **not** construct `ANNUAL:<year>` in JavaScript;
5. does **not** change `ziwei_daxian_frame_id`;
6. does **not** auto-submit the form.

A subsequent normal resolve remains the only operation that asks the server to select that annual target and, when applicable, generate its monthly frames.

## Separation from existing parity rows

`ZIWEI_ANNUAL_SEQUENCE_FRAMES` is distinct from:

- `ZIWEI_SELECTED_ANNUAL_FRAME_SUMMARY` — only the currently selected AnnualFrame summary;
- `ZIWEI_DOUJUN_PALACE` — selected annual Doujun marker on the board;
- `ZIWEI_ZI_YEAR_DOUJUN_BRANCH` — standard 子-year Doujun compatibility/basic-info projection;
- `ZIWEI_TEMPORAL_DESIGNATIONS`, `ZIWEI_TEMPORAL_TRANSFORMATION_BADGES`, and `ZIWEI_TEMPORAL_AUXILIARIES` — selected temporal overlays;
- candidate-only temporal auxiliary methods, which remain unranked and unselected.

Monthly sequence presentation is intentionally not conflated with this milestone. The current application contract generates `monthly_frames` only for explicitly requested annual years, and leap-month semantics remain `UNRESOLVED_NOT_GENERATED` under the released temporal contract.

## Verification

Focused test: `tests/test_combined_workbench_ziwei_annual_sequence_r1.py`.

The combined Workbench smoke validates the released annual sequence shape, unique frame/year identity, valid parent-Daxian references, and reports `ziwei_annual_sequence_count` without recreating annual formulas.

Milestone closure still requires same-SHA PASS for:

- `fortune-train verify`
- full `unittest` discovery
- `combined-workbench-smoke`
