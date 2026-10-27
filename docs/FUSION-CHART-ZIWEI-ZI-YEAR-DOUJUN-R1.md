# ZiWei 子年斗君 Workbench Presentation Closure R1

## Scope

This milestone closes one deterministic presentation gap only: the unified Workbench shows the natal-reference `子年斗君` branch by consuming already released annual Doujun frames.

It does **not** add a new Doujun formula, rerun the formula in the browser, select a disputed method, or interpret the coordinate.

## Canonical rule lineage

The released temporal engine already implements the classical Doujun rule:

- `S01:ZZQS-A-1935`: 流年太岁宫起正月，逆至本生月，再从本生月起子，顺数至本生时安斗君；
- `S10:ZZZA-A-1127` / `S10:ZZZA-A-1128`: normalized temporal-source closure used by the current runtime;
- released rule id: `S10-SUIJIAN-REVERSE-BIRTH-MONTH-FORWARD-BIRTH-HOUR-R1`.

`ZiweiTemporalState.annual_frames` already contains `year_branch`, `doujun_address`, and `doujun_rule_id` for every generated annual frame. With the default application range there are multiple `子`-year frames, and the same natal month/hour inputs make their released Doujun address identical.

## Presentation rule

The Workbench performs a strict read-only identity check:

1. select released annual frames whose `year_branch == 子`;
2. require at least one such frame;
3. require every selected frame to carry a valid `doujun_address.index` and `doujun_address.branch`;
4. require all selected frames to agree on the exact address identity;
5. render the released branch as `子年斗君`;
6. render `-` when the released data is absent, malformed, or inconsistent.

No birth-month counting, birth-hour counting, branch arithmetic, or Doujun rule id is implemented in browser code.

## Compatibility evidence

`docs/WENMO-CHARTDIFF-001.md` records the 1994-05-17 14:30 Beijing compatibility fixture as `子年斗君=辰`. The existing released temporal state reproduces `辰`; this milestone only makes that already-released deterministic fact visible in the basic-information panel.

## Important identity boundary

`子年斗君` here is the standard annual Doujun coordinate evaluated for a `子` annual branch. It is **not** the S01 normalized primitive `ZZZA-PR-056|ZI-DOU|子斗`, which is explicitly source-candidate-only and must remain separately governed rather than silently merged into Doujun.

## Product evidence

- Released engine: `src/fortune_training/ziwei_chart/temporal.py`
- Released bundle: `src/fortune_training/ziwei_application/models.py`
- Presentation: `src/fortune_training/combined_chart_application/ziwei_basic_info_assets.py`
- Regression: `tests/test_combined_workbench_ziwei_zi_year_doujun_r1.py`
