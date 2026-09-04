# S08 自化确定性运行审计 R1

## 结论

当前 S08 已明确自化与向心化是独立的四化对象，并明确其数据字段；但当前可引用材料没有给出一套可以从盘面唯一重放的“离心 / 向心”方向判定公式或完整表。因此本轮不新增自化运行时。

这不是否定自化，而是区分两件事：资料已经定义了“自化对象是什么”，尚未闭合“方向怎样机械计算”。参考软件中的箭头或显示结果不能代替来源规则。

## 已确认事实

S08 明确列出：

```text
SELF_TRANSFORMATION_DIRECTION_ENUM=OUTWARD_DISSIPATION|INWARD_RECEPTION
SELF_TRANSFORMATION_KIND_ENUM=SELF_LU|SELF_QUAN|SELF_KE|SELF_JI|OPPOSITE_LU|OPPOSITE_QUAN|OPPOSITE_KE|OPPOSITE_JI
```

并要求自化同时保存：原始宫位、宫干、受化星、化曜、方向、对宫、时间层。

S08 的十干四化表可以确定“某天干使哪颗星化禄 / 权 / 科 / 忌”，并明确适用于生年、一般宫干、主题宫干、大限、流年与流月四化。现有 `TransformationGenerator` 已承担这一类确定性分配。

但是该十干表本身不能唯一回答：

- 什么条件把一次宫干四化归为 `SELF_*`；
- 什么条件把它归为 `OPPOSITE_*`；
- 什么盘面事实决定 `OUTWARD_DISSIPATION`；
- 什么盘面事实决定 `INWARD_RECEPTION`。

## 来源章节审计

S08 运行时给出的原始来源统计为：

```text
SOURCE_CHAPTER_COUNT=45
SOURCE_GENERAL_CHAPTER_COUNT=5
SOURCE_TRANSFORMATION_CHAPTER_COUNT=40
```

章节注册表由通论与具体十干四化章节组成，末端仍是诸如 `武曲化忌 (壬干)`、`贪狼化忌 (癸干)` 的分配/机制章节。当前没有独立登记一个提供离心 / 向心宫位判定公式、方向表或完整触发矩阵的来源章节。

因此不能因为上层 Schema 已登记自化字段，就自行补出方向算法。

## 语义边界

S08 对离心与向心的文字说明用于界定对象含义：离心表示向外释放，向心表示承接回流。这类文字不是宫位计算公式。尤其不能未经来源支持，自行写出“本宫命中即离心”或“对宫命中即向心”等规则。

同样，文墨天机的显示只作为兼容性观察，不作为默认运行规则来源。

## 允许实现的门槛

后续只有在资料同时提供以下内容后，才开启自化运行时：

1. 明确的输入集合：原宫、对宫、宫干、物理星曜、四化类型；
2. 可机械重放的 `SELF_* / OPPOSITE_*` 命中公式或完整表；
3. 可机械重放的离心 / 向心方向公式或完整表；
4. 明确适用的时间层，不能从原局规则自动外推到流日、流时；
5. 稳定来源锚点；不同流派必须分别成为 method candidate；
6. 原宫、对宫、宫干、化曜、方向与时间层全部进入哈希、完整性与重放校验。

## 当前状态

本轮不改动已经发布的生年、大限、流年、流月四化，也不把解释性语义加入排盘结果。

`config/fusion-field-parity-r1.json` 中 `ZIWEI_SELF_TRANSFORMATION` 继续保持 `DETERMINISTIC_RUNTIME_MISSING`，下一步仅检索闭合的方向触发来源。
