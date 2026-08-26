# 八字运限神煞目标匹配投影 R1

## 1. 目的

问真类排盘会在原局之外展示大运、流年等时间层的神煞。当前仓库已经有来源绑定的原局神煞事实注册表，也已经有 `原局 → 大运 → 小运候选 → 流年 → 流月 → 流日 → 流时` 的统一时间链。

R1 增加一层**目标身份匹配投影**，用于回答一个严格有限的问题：

> 某个已经解析出的动态干支，是否命中了某个原局神煞候选已经登记的 `target_values`？

它不回答：

- 古籍是否明确允许把该神煞用于大运、流年、流月、流日或流时；
- 哪个流派的岁运神煞口径正确；
- 命中后的吉凶、强弱、事件或应期；
- 多个候选锚点中哪一个应该胜出。

因此本投影的固定策略是：

`ENGINEERING_TARGET_MATCH_NOT_CLASSICAL_TEMPORAL_APPLICABILITY`

所有命中项统一保存：

`temporal_applicability_status = NOT_CLASSICALLY_ARBITRATED`

该状态必须在后续历史考证/流派裁决阶段之前保持不变。

## 2. 来源边界

投影不建立第二套神煞表。唯一规则输入是当前原局 `BAZI-CLASSICAL-SHENSHA-FACTS-R1` 候选集合：

- 锚点、目标类型、目标值、匹配范围、来源坐标全部从原局候选读取；
- 原局 `DAY_STEM / YEAR_STEM / DAY_BRANCH / YEAR_BRANCH / YEAR_GANZHI / DAY_GANZHI` 等候选身份保持独立；
- `CANDIDATE_NOT_ARBITRATED` 不得在投影时合并或选胜；
- 来源坐标继续引用原局候选的 S0–S19 锚点；
- 本层增加的只是工程投影算法身份，不冒充新的古籍安法来源。

问真等商业软件只提供“存在运限神煞显示需求”的兼容性证据，不构成规则权威。

## 3. 可投影目标

R1 只允许单一动态干支可以机械比较的三种 `target_kind`：

- `STEM`：比较动态干支的天干；
- `BRANCH`：比较动态干支的地支；
- `GANZHI`：比较完整动态干支。

原局候选若为 `match_scope = ALL_PILLARS`，R1 可以在下列时间层进行 target-match：

- 大运；
- 小运候选；
- 流年；
- 流月；
- 流日；
- 流时。

这仍然只是“目标值匹配”，不是对古籍岁运适用性的裁决。

## 4. 原文落柱限制必须保留

原局候选若明确为 `match_scope = ONLY_DAY`，R1 只允许投影到 `DAILY` 层。

例如：

- 月德的原局规则明确验日干，因此不能因为某步大运或某个流年天干恰好相同，就把该 `ONLY_DAY` 候选投影成大运/月德或流年/月德；
- 天赦以季节定目标日柱，因此 `GANZHI + ONLY_DAY` 也只允许与流日干支进行 target-match；
- 月德合同时保存 `ONLY_DAY` 与 `ALL_PILLARS` 两个原局候选；两个候选在投影层仍保持独立，前者只检查流日，后者可进入一般动态 target-match。

该限制是来源范围的保守继承，不代表已经证明“流日一定适用此神煞”。

## 5. 结构型规则禁止退化为单干支匹配

以下当前原局候选不会进入 R1 单目标投影：

- `SANQI / 三奇贵人`：`STEM_SEQUENCE`，要求连续三柱顺序；
- `JIALU / 夹禄`：`BRANCH_PAIR`，要求两支同时出现；
- `YUANCHENG / 垣城`：`HOUR_BRANCH_LONGSHENG_LIUHE_YIMA`，要求日干长生、实际时支、日支驿马与六合共同成立。

它们会进入 `excluded_source_candidates`，并保留明确排除原因。不得为了在运限栏显示名称而把结构条件降格为单个天干或地支命中。

如果未来需要动态结构投影，必须建立独立的多层结构模型和来源审计，不能复用本 R1 单目标算法。

## 6. 时间层与候选保持

R1 与现有统一时间链保持同构：

`DAYUN → XIAOYUN candidates → ANNUAL → MONTHLY → DAILY → HOURLY`

- 大运前状态显式记为 `PRE_DAYUN_NO_GANZHI_PROJECTION`；
- 两套小运方法各自保持 `profile_id / direction / active_frame`，不得合并；
- 目标时间不存在合法干支时不制造神煞结果；
- 每一层只保存匹配事实，不保存吉凶词。

## 7. 完整性

投影保存独立 `fact_hash` 与 `computation_hash`：

- fact hash 锁定来源候选身份、目标值、层级匹配和排除状态；
- computation hash 另外锁定来源坐标和算法身份；
- replay 必须能够从同一原局神煞候选集合与同一时间层干支重新生成完全相同的投影。

任何对匹配值、候选身份、范围或排除状态的静默修改都应导致 replay 失败。

## 8. 阶段状态

R1.7 只发布内部 target-match 内核与专项回归，不立即修改联合 timeline/schema/UI。

R1.7 全量门禁通过后，下一阶段 R1.8 才允许把该 sidecar 接入：

1. `BAZI-UNIFIED-TARGET-TIMELINE-R1`；
2. application flow full replay；
3. JSON Schema；
4. combined read-only workbench。

在 R1.8 之前，现有公开融合盘契约保持不变。
