# 紫微＋八字共享时间凭证 R1

## 目标

联合排盘不再只证明“两个子系统收到同一个 `BirthInput`”，而是生成一份可复验的共享时间凭证。凭证把同一次输入解析得到的时区、UTC、真太阳时、节气、历法坐标、四柱时间结果及候选分支绑定到统一哈希，并建立每个时间分支到紫微、八字候选的联动关系。

本层只处理确定性排盘事实和明确选择的规则，不包含强弱、格局、用神、喜忌、预测、评分或断语。

## 不合并两门术数的换日规则

“共享时间底座”不等于“强制采用相同换日法”。当前生产配置明确保留两条独立规则链：

- 紫微：`ziwei_day_boundary_policy=ZI_START_23`，并单独记录历法日期和闰月规则；
- 八字：`bazi_day_boundary_policy=MIDNIGHT`，晚子时采用 `CLASSICAL_CONTINUOUS`；
- 共同事实：出生地、经纬度、IANA 时区、DST/fold、UTC 时刻、地方平太阳时、地方视太阳时和节气时刻。

两边的规则选择并列写入 `selected_policies.ziwei` 与 `selected_policies.bazi`，任何一方不得覆盖另一方。共享层只要求政策注册表版本和民用歧义时间选择一致，以保证同一个墙上时间产生同一组物理时刻候选。

## 凭证结构

`shared_time_credential` 包含：

- 输入区间与未解析民用时间样本；
- 每个合法时间分支的 UTC、offset、fold、真太阳时；
- 民用日期和真太阳日期分别对应的农历事实；
- 紫微有效农历日期；
- 按八字自身规则生成的四柱、有效日和晚子时日干来源；
- 当前节与下一节的 UTC 时刻；
- 分支 `realization_hash`、总体 `fact_hash` 和绑定共享时间 policy snapshot / realization 的 `computation_hash`。

`candidate_lineage` 以 `source_time_branch_index` 为唯一联动坐标，记录同一物理时间分支对应的紫微本命事实哈希及八字应用候选 ID，并生成独立 `lineage_hash`。

## 哈希与 provenance 分层边界

`shared_time_credential` 的哈希边界是共享时间层，不是整个联合盘的全部算法版本：

- `realization_hash` 绑定单个合法物理时间分支的共享时间/历法事实；
- `fact_hash` 绑定出生输入、两子系统时间解析状态、输入不确定区间、各 realization hash 与未解析样本；
- `computation_hash` 直接绑定 credential schema、`fact_hash`、policy registry version、`selected_policies` 与 realizations；
- 它**不直接包含每个子系统的全部 algorithm ID/version**。

完整联合 provenance 由更高一层 `ZIWEI-BAZI-COMBINED-MANIFEST-V1` 补全：manifest 绑定 combined profile 的 algorithm ID/version、紫微/八字各 profile ID/version、完整 shared credential、candidate lineage，以及两个子系统的 bundle hash。子系统内部的算法与规则 lineage 继续由各自 bundle/hash 合约负责。

`SHARED_TIME_CREDENTIAL_HASH_SCOPE=SHARED_FACTS_PLUS_POLICY_SNAPSHOT`

`FULL_COMBINED_PROVENANCE_SCOPE=MANIFEST_PLUS_SUBSYSTEM_BUNDLES`

因此“共享时间”只统一可共同验证的物理事实与必要政策契约，不把紫微与八字的独立规则链压成一个统一命理规则。

## 完整性门禁

联合结果验证会失败关闭以下情况：

1. 凭证 Schema、分支序号、分支哈希、事实哈希或计算哈希被修改；
2. 凭证中的注册表版本或两套独立规则快照与运行配置不一致；
3. 紫微候选引用不存在的共享时间分支；
4. 八字应用中的墙上时间、UTC、fold 或真太阳时与共享分支不一致；
5. 候选联动表与两个子系统的实际候选集合不一致。

联合导出清单 Schema 仍为 `ZIWEI-BAZI-COMBINED-MANIFEST-V1`，新增的共享凭证和候选联动字段是必填项；旧清单不能冒充本轮之后的新联合结果。
