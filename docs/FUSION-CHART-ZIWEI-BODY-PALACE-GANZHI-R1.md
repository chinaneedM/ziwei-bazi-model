# ZiWei Body-Palace Ganzhi Workbench Closure R1

## Scope

This milestone closes one deterministic presentation gap only: the unified Workbench now shows the natal Body-Palace Ganzhi (`身宫干支`).

It does **not** add a new Zi Wei calculation rule, select a disputed method, or perform any browser-side calendar/fortune derivation.

## Canonical released data

The existing released natal contract already contains both inputs required for an identity-only projection:

- `NatalStructureState.body_address` identifies the Body Palace by canonical `index` and `branch`.
- `NatalStructureState.address_attributes` contains the released palace stem for each canonical address.

The Workbench therefore performs a strict read-only identity join:

1. require a valid Body-Palace `index` and `branch`;
2. match `address_attributes` on both `index` and `branch`;
3. require exactly one matching released row with a non-empty `stem`;
4. render `stem + branch` as `身宫干支`;
5. render `-` when the released identity is missing, malformed, or non-unique.

No stem is synthesized in the browser.

## Product evidence

- Presentation: `src/fortune_training/combined_chart_application/ziwei_basic_info_assets.py`
- Released model: `src/fortune_training/ziwei_chart/models.py`
- Regression: `tests/test_combined_workbench_ziwei_body_palace_ganzhi_r1.py`

The existing Field Parity row `ZIWEI_LIFE_BODY_PALACE_BRANCHES` remains intentionally scoped to palace branches. This milestone records the additional Body-Palace Ganzhi visibility without changing natal engine semantics.
