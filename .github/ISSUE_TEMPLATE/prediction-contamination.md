---
name: 预测上下文污染处置
about: 在冻结前作废污染轮次；仅在案例材料或答案污染时隔离案例
title: "[PREDICTION CONTAMINATION] "
assignees: ""
---

仅限仓库所有者提交。正文不得包含答案、预测方向、评分或复盘内容。

- 仅启动顺序违规、未读取案例或答案：使用下列 JSON，并保留 CASE 的严格首次盲测资格。
- 已读取答案、旧预测或其他案例污染对象：把 `round_id` 改为显式当前轮次，并把
  `reason` 改为 `PREDICTION_CONTEXT_ALLOWLIST_VIOLATION`；控制器才会隔离案例。

```json
{
  "schema": "PREDICTION-CONTAMINATION-REPORT-V1",
  "round_id": "RESOLVE_FROM_MAIN_CURRENT_ACTIVE_ROUND",
  "case_id": "CASE-000",
  "reason": "PREDICTION_ACCESS_CONTRACT_NOT_EXECUTED_BEFORE_REPOSITORY_READ"
}
```
