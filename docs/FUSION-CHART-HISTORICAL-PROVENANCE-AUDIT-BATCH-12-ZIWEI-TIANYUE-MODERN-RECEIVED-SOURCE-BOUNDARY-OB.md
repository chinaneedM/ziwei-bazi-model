# Fusion Chart Historical Provenance Audit R1 — Batch 12OB

## HPA-ZMINOR-025 天月：现代接收表确认与前现代来源边界

Status: **SOURCE_INSUFFICIENT RETAINED / MODERN RECEIVED TABLE STABLE / PREMODERN ZIWEI WITNESS UNRESOLVED / NO ALGORITHM REOPEN**

当前 `STAR.TIANYUE_MOON` 使用十二月表：一戌二巳三辰、四寅五未六卯、七亥八未九寅、十午十一戌十二寅。

公开现代紫微资料稳定重复同一口诀；现代开源实现也使用同一十二值，但明确把出处标为“古籍待考、后世悬曜增补”。这足以确认现代接收传统的一致性，却不能反向证明明清紫微刻本已经存在同表。

同时必须排除跨系统近名对象。《三命通会》中的天德、月德、天月德合属于另一套日课/神煞语义和输入维度，不能因“天月”字面邻近而并入 `STAR.TIANYUE_MOON`。

本批没有取得合格的前现代紫微专属十二值见证，因此 `HPA-ZMINOR-025` 继续保持 `SOURCE_INSUFFICIENT`。这里的“未找到”仅限本批已审阅的公开检索面，不宣称历史上绝不存在更早见证。

不修改 runtime、profile、rule-set/version、hash、候选或默认值，不产生 algorithm reopen。Matrix 220/220 audited、10 current missing；provenance defects 40/40；HISTORICALLY_SUPPORTED 96 / SOURCE_INSUFFICIENT 9。

下一门：**12OC — HPA-ZMINOR-026 阴煞 lunar-month six-value cycle**。

Research: `docs/research/ZIWEI-TIANYUE-MODERN-RECEIVED-SOURCE-BOUNDARY-R1.json`
Evidence: `docs/research/evidence/batch-12ob/ziwei-tianyue-modern-received-source-boundary-evidence.json`
