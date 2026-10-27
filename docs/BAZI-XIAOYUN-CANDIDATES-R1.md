# 八字小运古法候选 R1

## 范围

本轮只生成虚岁对应的小运干支坐标，不评价吉凶、强弱或应事。小运结果写入八字候选视图及其哈希。

## 两套来源口径

仓库古籍资料明确并存两种起法，当前不作无依据裁决：

| profile | 起法 | 来源 |
| --- | --- | --- |
| `SMTH-HOUR-PILLAR-YEAR-YINYANG-DIRECTION-R1` | 从出生时柱按顺逆走下一位为一岁；阳年男、阴年女顺，阴年男、阳年女逆 | `S12:SMTH-SEG-01200`、`S12:YHZP-USR-S03778` |
| `SMTH-MALE-BINGYIN-FEMALE-RENSHEN-R1` | 男命一岁丙寅顺行；女命一岁壬申逆行 | `S12:SMTH-SEG-01199` |

汇总状态固定为 `UNRESOLVED_CLASSICAL_ALTERNATIVES`，每套 profile 均为 `CANDIDATE_NOT_ARBITRATED`。这表示软件忠实列出古法差异，而不是把其中一套伪装成唯一答案。

## 语义隔离与回归

所有年岁标记 `ANNUAL_COORDINATE_ONLY_NO_INTERPRETATION`。测试覆盖来源算例、四种年干阴阳／性别顺逆组合、两套固定起点、六十甲子闭合、非法输入闭锁，以及应用候选视图中的双 profile 保留。
