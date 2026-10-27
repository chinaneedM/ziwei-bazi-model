# 天问 13AJ exact-HEAD CI 恢复｜历史快照不可约束未来合法增长

## 被记录的失败

13AJ 提交 `664503907edadcc7896e4a59496f693616f9bd2c` 对应 `clean-training-system` GitHub Actions [39337922507](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/39337922507) 在 `UTokyo 13AI Agawa catalog editorial supplement and OPAC nonpromotion gate` 失败；GitHub job `118351968513` 指示脚本 `scripts/verify-agawa-catalog-editorial-bridge-13ai.py` 的历史快照 `b["external_sources_remain"]==746` 同时强制活跃来源总量等于746。13AJ 正常新增一条第一方数字馆藏来源，实时来源总量变成747。**这是历史验证脚本错误，非史料缺陷，也非证据回退。**

除这一失败以外，13AJ 同一 HEAD 上其余 173 个 Actions 均成功；原13AI HEAD `75b97cd3a41426885b26c382718cbd0174d40492` 的 174 个 Actions 已全部成功。失败日志与历史状态文件保留，不修改先前 13AI、13AJ 的证据快照。

## 修复范围

- **保留批次历史常量**：13AI 来源登记时 746、13AJ 时 747，来源分片、物理原件身份与历史校验结论不回写；
- **检查活跃仓库的单调扩展**：当前来源数需不小于对应批次的来源快照基线；真实活跃来源总数仍由 Source Registry、Manifest 与 PROJECT-CURRENT-STATE 的同期一致性门核验；
- **检查旧历史事件存在**：13AI / 13AJ 原始证据、研究焦点和遗漏账本 checkpoint 应持续存在，不能要求自己永远是焦点数组的末条；
- **检查最新焦点同步**：账本 latest prefix 必须匹配当前 current_focus 的末条，不得硬编码为历史批次号；
- 保持排盘产品 CLOSED、已确认算法缺陷0、算法重开0、跨原件数值票新增0，11 个遗漏项的状态不变。

该提交只修订验证代码及其测试，不改变研究语义状态；`PROJECT-CURRENT-STATE-R1.json` 版本继续为 `1.695.0`，不虚增考据批次或来源。需要重新核查修复 HEAD 的全量 Actions。

## 同轮补充：不可将 11 个已登记问题写成永久上限

审计继续发现 13AI 与 13AJ 的验证器原先亦直接写死 `len(issues)==11`、所有问题状态必须永远 OPEN/BLOCKED 和 `TW-OPEN-0005` 永远 P0/OPEN。未来依据原书证据合法登记新问题、调整优先级或用 append-only 事件结案时，旧验证器不应误报。改为 **初始 TW-OPEN-0001 至 0011 的 ID 均仍存在、允许总数增加**，并由正式的 omission continuity gate 验证增删/状态转换的凭证和一致性。这里不实际增加或关闭任何问题。
