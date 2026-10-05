# Fusion Chart Historical Provenance Audit R1 — Batch 12NX

## HPA-ZIWEI-026 将前十二神：来源与时层收束

Status: **SOURCE_INSUFFICIENT RETAINED / NATAL-ANNUAL TEMPORAL LAYERS SEPARATED / NO ALGORITHM REOPEN**

本批继续 `HPA-ZIWEI-026`。当前 `RING.JIANGQIAN12` 的十二成员、三合旺支锚点和顺行几何不变；production 仍由 `ZiweiChartFoundation` 把 `structure.ziwei_birth_year_branch` 送入 `WenmoDefaultRingGenerator.jiangqian()`，因此当前产品事实是明确的 **NATAL / 生年支层**。

证据层需要把“规则几何”与“时间层”拆开。1581《新刻纂集紫微斗数捷览》公开转录的卷一第 58 章题为《定流年太岁所值凶星图》，其中直接按年支三合列出驿马位置。这证明早期紫微文本确有**流年太岁层的同族三合神煞运用**；但该章当前公开文字并没有给出完整的“将星→攀鞍→岁驿→…→亡神”十二成员连续表，因此不能把它升级成 1581 完整将前十二神表。

王亭之现代中州派 received manual 的第 40 条则完整保存 `将星三合起旺地，攀鞍岁驿息神方，华盖劫灾天三煞，指背咸池月煞亡`，标题只写“年支”。现代派生规则面同时可见完全相同几何的“安生年将前十二星”和“安流年将前诸星表”。因此本批裁决：**本命与流年不是互斥胜者，而是同一三合几何在不同 year-branch context 上的独立时间层应用**。不能因为存在流年表，就把当前本命 ring 改成流年；也不能因为当前 runtime 使用生年，就否认年运层。

`HPA-ZIWEI-026` 继续 `SOURCE_INSUFFICIENT`，缺口被收窄为：尚未取得版次绑定、可直接审读的早期完整十二成员将前表及其明确时层说明。S01 normalization、现代中州派 manual、现代网站或软件均不能倒推成明代完整规则的唯一权威。

本批没有确认新的 provenance metadata defect：12MV 已经明确写过 annual-target presentation 必须单独 sourcing/implementation。12NX 只是把“候选方法”表述进一步校正为“不同时间层应用”，所以 provenance 仍为 **40/40**。

不修改 `rings.py` / `engine.py`、rule-set/version、算法版本、fact/computation hash、候选选择或默认 profile；不新增流年 ring product surface。Matrix 220/220 audited、10 current missing；chart algorithm defects / reopens / candidate collapses 均为 0。`transmission_impact=NONE`。

下一门：**12NY — HPA-ZMINOR-020 standalone Feilian identity collision**，重点保持博士环“飞廉”、年支“蜚廉”及同坐标事实的身份隔离。

Research: `docs/research/ZIWEI-JIANGQIAN-TEMPORAL-SOURCE-SCOPE-CLOSURE-R1.json`  
Evidence: `docs/research/evidence/batch-12nx/ziwei-jiangqian-temporal-source-scope-evidence.json`
