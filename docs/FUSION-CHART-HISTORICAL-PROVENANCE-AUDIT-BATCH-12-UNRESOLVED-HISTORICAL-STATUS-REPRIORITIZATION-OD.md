# Fusion Chart Historical Provenance Audit R1 — Batch 12OD

## unresolved historical-status queue：月系 023–026 后重排

Status: **PRIORITY REASSESSMENT COMPLETE / NO STATUS CHANGE / NO ALGORITHM REOPEN**

完成 12NZ–12OC 后，当前 unresolved inventory 为：30 `DISPUTED_MULTIPLE_CANDIDATES`、9 `SOURCE_INSUFFICIENT`、1 `NOT_YET_FORMALIZED`。

剩余 SOURCE_INSUFFICIENT/NOT_YET_FORMALIZED 行的边际风险已经下降：HPA-ZIWEI-008/011 是已拆分父行；HPA-ZMINOR-024/025/026 刚完成来源边界；HPA-BAZI-015 与 HPA-BHIDDEN-002 只是非语义显示顺序；HPA-ZT-016 明确未实现；HPA-ZIWEI-023 与 HPA-ZIWEI-026 已分别做过 NW/NX 深审。

因此下一阶段转回 disputed candidate 队列，优先处理“生产已选择一个具体方法，但历史上存在明确竞争家族、且竞争方法尚未形成完整可回放候选”的对象。

第一优先选定 **HPA-ZMINOR-022 月德**：当前 `STAR.YUEDE` 采用子年巳宫起顺行；received Fullbook 存在子起竞争家族，而且 temporal scope 仍需拆开。该问题既直接影响生产星位，又比晚子时整套时间坐标争议更紧凑，适合先完成 source-scoped candidate closure。

第二梯队为 HPA-ZMINOR-008 天寿 Body/Life basis、HPA-ZMINOR-007 天厨 competing tables；再往后才是更宽的 core-aux / roles / TaiSui label families 与已经长期保留候选的时间边界争议。

本批不改 Matrix status、runtime、默认值、候选选择或算法；只重排工作队列。

下一门：**12OE — HPA-ZMINOR-022 月德：巳起 vs 子起历史家族 + natal/flow 时层候选化。**

Research: `docs/research/HISTORICAL-UNRESOLVED-STATUS-REPRIORITIZATION-OD-R1.json`
