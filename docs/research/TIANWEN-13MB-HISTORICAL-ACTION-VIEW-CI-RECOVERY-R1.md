# 天问 13MB｜历史风险字段前向校验兼容修复

## 问题来源（非古籍证据结论）

基于远端 HEAD `3310be4c854aa9746d9e0809cedcb7de6b075daf`、Actions 272 项的批次验收：247 成功、25 失败。多处早期验证脚本不当地继续要求 **实时** `TW-OPEN-0005.next_action` 包含 `13EC`、`13LN`、`13LQ` 等旧研究措辞及跨领域数字标签。风险台账应始终只有**当前**待办；旧研究要从 `history[*].previous_next_action` 及 `history[*].revision_id` 读取，不能倒退 `13MA CURRENT ACTION`。

## 修复策略

新增 `scripts/_tianwen_historical_action_r1.py` 的只读 `historical_action_view(issue)`：将实时 `next_action` 放首位，并且只从现存的前向追加历史快照及有对应 `revision_id` 的批次还原旧措辞。此文本只能用于旧批次 CI 回放，不可写回实时字段、来源注册、Matrix、传承谱或产品算法。

历史验收脚本改从该只读视图核对过去已被记录的关键字，持续由现存 `issue.status`、`source_refs`、`revision_id`、`current_focus` 和 current-prefix 门禁确保仍符合前向追加契约。新单元测试检查：最新动作优先、旧批次确实有证据可追溯、未出现的批次不可凭空生成、实时字段不被修改。该修复不改变历史断言的正确性和来源证据等级。

## 科学与项目边界

**没有新古籍原叶证据、没有数值裁决、没有版刻或印次结论**。当前实际研究边界仍为 13MA：BSB `bsb11166691` 官方清单1910个canvas，40幅900px衍生图。卷三十五原叶与 G893 六组原数值裁决未闭合。

因此 `PROJECT-CURRENT-STATE-R1.json` 仍为 `1.965.0`，遗漏风险台账仍为11项，研究来源765，Matrix222/222，传承谱252节点/238边，`DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED`，算法重开0。

CI 结果必须以本修复提交**准确 HEAD** 的重新执行结果为准，不引用旧成功记录。
