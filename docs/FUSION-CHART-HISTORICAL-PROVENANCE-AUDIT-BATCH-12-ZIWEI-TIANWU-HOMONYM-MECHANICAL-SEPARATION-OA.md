# Fusion Chart Historical Provenance Audit R1 — Batch 12OA

## HPA-ZMINOR-024 天巫：同名古典规则的机械排除与来源域隔离

Status: **SOURCE_INSUFFICIENT RETAINED / PREMODERN HOMONYM MECHANICALLY REJECTED AS CURRENT ZIWEI TABLE ANCESTRY / NO ALGORITHM REOPEN**

当前 `STAR.TIANWU` 为四马地循环：正五九月巳、二六十月申、三七十一月寅、四八十二月亥。

《历事明原》与《御定星历考原》保存同名天巫“常居月建前二辰”；《星历考原》同章福德例证把“前二辰”明确为月建顺推两支。《钦定协纪辨方书》卷四又把天巫置于建除十二神“满”的择日语境。

机械复算：

```text
月建：寅 卯 辰 巳 午 未 申 酉 戌 亥 子 丑
古典：辰 巳 午 未 申 酉 戌 亥 子 丑 寅 卯
现行：巳 申 寅 亥 巳 申 寅 亥 巳 申 寅 亥
```

仅八月（亥）与十一月（寅）2/12 偶合，10/12 不同。因此前现代历法/择日天巫被明确排除为现行紫微四马地月表的直接机械来源；同名与少数同宫不能建立身份或传承。

`HPA-ZMINOR-024` 继续保持 `SOURCE_INSUFFICIENT`：古典天巫本身有历史见证，但当前紫微 `巳申寅亥` 表仍缺合格的前现代紫微专属见证。

本批不改 runtime、profile、rule-set、hash、候选或默认值，不产生 algorithm reopen。Matrix 220/220 audited、10 current missing；provenance defects 40/40；HISTORICALLY_SUPPORTED 96 / SOURCE_INSUFFICIENT 9。

下一门：**12OB — HPA-ZMINOR-025 天月 lunar-month twelve-value table**，继续隔离天月德、天月德合等跨系统同名/近名对象。

Research: `docs/research/ZIWEI-TIANWU-HOMONYM-MECHANICAL-SEPARATION-R1.json`
Evidence: `docs/research/evidence/batch-12oa/ziwei-tianwu-homonym-mechanical-evidence.json`
