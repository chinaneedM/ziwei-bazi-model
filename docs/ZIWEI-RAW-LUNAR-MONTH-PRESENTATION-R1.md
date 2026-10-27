# ZiWei Natal Month Coordinates Workbench Presentation R1

## Scope

This milestone closes presentation-only gaps for already released Zi Wei natal structure fields carried by `combined_resolution.ziwei_bundle.candidate.chart.structure`:

- `raw_lunar_month`
- `natal_month_coordinate`
- `month_anchor`

It does not add or change lunar-calendar conversion, Zi Wei day-boundary rules, Ba Zi day-boundary rules, leap-month policy, temporal selectors, transformation rules, auxiliary-star rules, auspiciousness, strength, interpretation, or prediction behavior.

## Released source contract

`NatalStructureState.raw_lunar_month`, `NatalStructureState.natal_month_coordinate`, and `NatalStructureState.month_anchor` are backend-released values.

`month_anchor` is the released `Address` used by `ZIWEI-NATAL-STRUCTURE-V1` when placing Life and Body palaces. The canonical generation trace records the `place_life_and_body` step against `S01:ZZZA-PR-008`. The Workbench must therefore copy the released anchor; it must not reconstruct it from month or hour inputs.

The fields remain distinct:

- `raw_lunar_month`: raw effective lunar month supplied to natal structure generation;
- `natal_month_coordinate`: month coordinate after the configured Zi Wei life/body leap-month policy;
- `month_anchor`: released earthly-branch address from which Life/Body placement proceeds.

## Workbench presentation

`src/fortune_training/combined_chart_application/ziwei_raw_lunar_month_assets.py` remains the compatibility asset and route name, but now acts as a small read-only natal-coordinate projection. After a successful `/api/resolve`, it:

1. reads `structure.raw_lunar_month` and, when valid, appends `原始农历月`;
2. reads `structure.month_anchor` and, when its released `Address` shape is valid, appends `命身月锚`;
3. appends both items to the existing Zi Wei basic-information grid;
4. removes prior projected items before re-rendering and before the next submit;
5. performs no fallback calculation if either released value is absent or malformed.

The existing basic-info asset continues to render `natal_month_coordinate` as `农历月坐标`. No new backend endpoint or schema is introduced, and the existing loopback route `/ziwei-raw-lunar-month.js` is preserved.

## Safety boundaries

- Zi Wei and Ba Zi time/day-boundary policies remain independent.
- No leap-month policy is inferred from any browser-visible coordinate.
- The browser does not derive `month_anchor` from `raw_lunar_month` or `natal_month_coordinate`.
- The browser does not derive Life or Body palace from `month_anchor`.
- `ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION` remains `NOT_YET_FORMALIZED`.
- `ZIWEI_TARGET_HOURLY_CANDIDATES` remains `DISPUTED_CANDIDATE_ONLY`.
- No prediction or doctrinal winner is introduced.

## Verification

Focused test:

`tests/test_combined_workbench_ziwei_raw_lunar_month_r1.py`

Closure requires same-SHA PASS for:

- `fortune-train verify`
- full `python -m unittest discover -s tests -v`
- `python scripts/combined-workbench-smoke.py`
