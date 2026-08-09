# WENMO CHARTDIFF 001

Status: external compatibility calibration, not canonical-source authority.

## Input

- software: 文墨天机专业版 2.5.9 / API 1.1.2
- user-confirmed setting state: all defaults
- sex: male
- civil birth time: 1994-05-17 14:30
- place: Beijing
- longitude shown by Wenmo: 116.400E
- Wenmo displayed true-solar time: 1994-05-17 14:19
- Wenmo lunar coordinate: 甲戌年四月初七未时

The fixture intentionally omits the displayed personal name. It stores only the reusable test coordinates and chart facts.

## Layered result

### Common deterministic scope: MATCH

Current engine and Wenmo agree on all fields implemented in the shared comparison scope:

1. true-solar minute: 14:19;
2. lunar coordinate: 甲戌 year, lunar month 4, day 7, non-leap, 未 hour;
3. Life palace: 戌;
4. Body palace: 子;
5. all twelve functional-palace addresses;
6. all twelve address stems / palace Ganzhi;
7. Five-Element Bureau: 火六局, Life palace 甲戌;
8. all fourteen main-star addresses;
9. 文昌/文曲;
10. 左辅/右弼;
11. 天魁/天钺 for this 甲-year fixture;
12. 天马;
13. 禄存/擎羊/陀罗;
14. the hour-derived 地空/地劫 pair.

The current common-scope placement regression therefore compares exactly 26 generated placement entities.

## Entity correction discovered by the diff

The strict QS e-witness uses the historical label `天空` in the paired hour rule with 地劫. The repository primitive `ZZZA-PR-018` and Wenmo both identify the corresponding modern normalized entity as 地空, while Wenmo separately places another small-star 天空 in 亥.

Keeping the generated entity as `AUX.HOUR_VOID / 天空` would collapse two distinct entities. CHARTDIFF-001 therefore normalizes the paired hour entity to:

- entity id: `STAR.DIKONG`
- display name: `地空`
- source refs: retain the QS e-witness plus the project primitive, so the historical alias remains auditable.

The separate 天空 entity is not yet implemented and must receive its own identity/generator later.

## Confirmed profile / scope differences, not bugs

The following Wenmo outputs are deliberately outside the current engine slice and are stored only as future compatibility observations:

- 命主=禄存;
- 身主=文昌;
- 子年斗君=辰;
- natal 火星=申;
- natal 铃星=戌;
- separate small-star 天空=亥;
- dignity labels;
- natal transformations and self-transformations;
- 长生十二神 and 太岁煞禄;
- Daxian / annual / minor-limit frames;
- remaining auxiliary and miscellaneous stars.

In particular, 火铃 must not be copied from Wenmo into the strict QS rule set. The current canonical QS witness and modern/Wenmo behavior are not the same rule family. This remains a Profile Discrimination task.

## Daxian observation reserved for Temporal V1

Wenmo default output for this fixture begins:

- 6-15 virtual age: 甲戌 / Life palace;
- 16-25: 乙亥;
- 26-35: 丙子;
- 36-45: 丁丑.

This is recorded as an external future regression target only; the current chart foundation does not yet claim Daxian support.

## Engineering rule established

External software comparison is used in three passes:

1. shared deterministic facts: exact comparison and regression fixture;
2. known profile-dependent facts: classify and defer to explicit Profile rules;
3. unsupported content: record as future coverage, never silently copy into current algorithms.

A Wenmo mismatch is therefore not automatically an engine bug, and a Wenmo match is not canonical proof. Git canonical sources remain the source authority; compatibility fixtures are independent operational oracles.
