# ZiWei Bureau Metadata Workbench R1

Status: PRODUCTIZED READ-ONLY PRESENTATION

## Scope

This milestone exposes two deterministic Zi Wei natal fields that were already released inside `NatalStructureState.bureau` but were not visible in the unified Workbench:

- `life_palace_ganzhi` → **命宫干支**
- `nayin_name` → **局纳音**

The existing **五行局** display remains unchanged and continues to use `bureau.element` plus `bureau.number`.

## Product boundary

`ziwei_basic_info_assets.py` reads these values directly from the exact successful `/api/resolve` response at `combined_resolution.ziwei_bundle.candidate.chart.structure.bureau`. The browser does not regenerate a natal chart, derive a Life-Palace stem, perform a Nayin lookup, or mutate Zi Wei selectors/SVG state.

This is presentation closure only. It does not change:

- `FiveElementBureau` calculation;
- natal fact/computation hashes;
- source refs or algorithm versions;
- candidate selection semantics;
- any auspiciousness, strength, prediction, or doctrinal interpretation.

## Regression contract

`tests/test_combined_workbench_ziwei_basic_info_r1.py` verifies that a real combined resolution contains non-empty `life_palace_ganzhi` and `nayin_name`, that the Workbench consumes those exact released fields, and that no browser-side natal/Nayin recomputation dependency is introduced.
