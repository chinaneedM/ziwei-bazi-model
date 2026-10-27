# Fusion Chart Historical Provenance Audit R1 — Batch 12NY

## HPA-ZMINOR-020 standalone 蜚廉：历史几何与身份碰撞收束

Status: **HISTORICALLY_SUPPORTED FOR STANDALONE YEAR-BRANCH GEOMETRY / ZIWEI ADOPTION PATH UNRESOLVED / BOSHI IDENTITY SEPARATED / NO ALGORITHM REOPEN**

本批重审 `HPA-ZMINOR-020`。当前 `STAR.FEILIAN` 使用固定生年支表：子→申、丑→酉、寅→戌、卯→巳、辰→午、巳→未、午→寅、未→卯、申→辰、酉→亥、戌→子、亥→丑。此前 Batch 07C 只能确认这是稳定的现代运行时表，尚未建立合格的前现代来源。

本批找到并交叉核对了前现代岁神/历法传统。元曹震圭《历事明原》的公开转录在飞廉条中引《神枢经》释义，并明确以《广圣历》列出上述十二支表；康熙五十二年（1713）《御定星历考原》卷二再次以《广圣历》名义重录完全相同的十二值；乾隆朝《钦定协纪辨方书》卷三又重录同表，并进一步用三合生、旺、墓次序解释其逆历机制，同时说明“岁名飞廉、月名大煞”的时间层命名。

因此 `FEILIAN_BY_BRANCH` 的十二支坐标现在取得 **12/12 前现代历史几何支持**。这足以把本行从 `SOURCE_INSUFFICIENT` 升级为 `HISTORICALLY_SUPPORTED`，但支持范围严格限定为：standalone 飞/蜚廉作为岁神/年支神煞的坐标几何及年支输入。

谱系仍保留一个重要缺口。《历事明原》《星历考原》都明确引用《广圣历》，而《宋史·艺文志》著录苗锐《新删定广圣历》二卷；但当前没有直接审读该被引《广圣历》传本，也未证明《历事明原》所引文本与《宋史》著录条目是同一具体 recension。因此只能登记“引用链存在”，不能把宋代书目记录直接当成已审读规则原文。

同时，standalone `STAR.FEILIAN` 与 `RING.BOSHI12.FEILIAN` 必须继续分离。后者属于博士十二神：以禄存为起点，飞/蜚廉为第 7 个成员。由于序数 6 在十二宫上顺逆都落于禄存对宫，其坐标本质由年干→禄存决定，而 standalone 则由生年支固定表决定。六十甲子中仅甲子、乙丑、庚午、辛未四例同宫；这四个坐标偶合不能形成身份合并。

紫微《捷览》《全书》直接证明博士十二神中的飞/蜚廉成员及禄存起法，但当前仍没有合格证据证明 standalone 岁神飞廉何时、经何流派进入紫微体系。因此“历史几何已闭合”与“紫微采用谱系未闭合”同时成立。

本批不修改 `minor_stars.py`、`rings.py`、profile、rule-set/version、算法、fact/computation hash 或候选选择；不产生算法 reopen。Matrix 仍为 220/220 audited、10 current missing；provenance defects 40/40；chart algorithm defects/reopens/candidate collapses 0。

下一门：**12NZ — HPA-ZMINOR-023 月解 / month 解神 provenance**，重点继续隔离月表与年解/解神同名对象。

Research: `docs/research/ZIWEI-STANDALONE-FEILIAN-HISTORICAL-IDENTITY-CLOSURE-R1.json`
Evidence: `docs/research/evidence/batch-12ny/ziwei-standalone-feilian-historical-identity-evidence.json`
