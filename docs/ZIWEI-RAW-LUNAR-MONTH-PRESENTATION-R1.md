# ZiWei Raw Lunar Month Workbench Presentation R1

## Scope

This milestone closes a presentation-only gap for the already released Zi Wei natal structure field `NatalStructureState.raw_lunar_month`.

It does not add or change any lunar-calendar conversion, Zi Wei day-boundary rule, Ba Zi day-boundary rule, temporal selector, transformation rule, auxiliary-star rule, auspiciousness, strength, interpretation, or prediction behavior.

## Released source contract

The backend already publishes both:

- `raw_lunar_month`
- `natal_month_coordinate`

inside the exact released `NatalStructureState` carried by `combined_resolution.ziwei_bundle.candidate.chart.structure`.

These fields are deliberately kept distinct. The Workbench already renders `natal_month_coordinate` as `农历月坐标`; this milestone additionally renders `raw_lunar_month` as `原始农历月`.

The browser does not derive one from the other and does not perform lunar-calendar conversion.

## Workbench presentation

`src/fortune_training/combined_chart_application/ziwei_raw_lunar_month_assets.py` is an additive read-only asset. After a successful `/api/resolve`, it:

1. reads only `combined_resolution.ziwei_bundle.candidate.chart.structure.raw_lunar_month`;
2. requires the released value to be an integer in `[1, 12]`;
3. appends one `原始农历月` item to the existing Zi Wei basic-information grid;
4. removes the item before the next submit;
5. performs no fallback calculation if the released value is absent or malformed.

`workbench_local_app.py` publishes the asset through loopback HTTP. No new backend endpoint or schema is introduced.

## Safety boundaries

- Zi Wei and Ba Zi time/day-boundary policies remain independent.
- No leap-month policy is inferred from `raw_lunar_month`.
- `raw_lunar_month` is not treated as a substitute for `natal_month_coordinate`.
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
- `python scripts/combined-workbench-http-smoke.py`
