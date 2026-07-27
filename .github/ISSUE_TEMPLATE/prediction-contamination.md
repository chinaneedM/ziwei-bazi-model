---
name: 预测上下文污染隔离
about: 在冻结前隔离受污染案例，不计分并自动切换到下一案例
title: "[PREDICTION CONTAMINATION] "
assignees: ""
---

仅限仓库所有者提交。正文只能包含下列四字段 JSON；不得包含答案、预测方向、评分或复盘内容。`round_id` 与 `case_id` 必须仍与当前 `READY_FOR_ROUND` 状态一致。

```json
{
  "schema": "PREDICTION-CONTAMINATION-REPORT-V1",
  "round_id": "FORMAL-ROUND-000",
  "case_id": "CASE-000",
  "reason": "PREDICTION_CONTEXT_ALLOWLIST_VIOLATION"
}
```
