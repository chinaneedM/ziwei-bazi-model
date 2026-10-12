# 12UJ — CI 前向修复：历史快照计数不等于当前注册总数

首次 12UJ 提交 `8b5ad522af0f82dd112f874f5eaec03ea7917f3b` 后，针对该 HEAD 的 [Actions 38244147621](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/38244147621) 检测失败。来源登记验证 PASS：根647、扩展39、共686；项目连续性 PASS：Matrix 222/222、缺陷修复45/45、正式批次487。

故障只发生于旧 12UI 回归测试：其对**当前** registry 的 `combined_source_count` 固定断言683，但在后续 12UJ 正确新增3个来源后当前总数已是686。该断言把 12UI 的**历史批次完成时快照**误用于所有后续 HEAD，属于测试设计缺陷，不是研究来源账本或历史见证被篡改。

修复：保留 12UI 原始机器证据中的 `accounting.source_count_after=683`，但旧测试核查**当前**计数应直接与当前状态 JSON 及统一 registry verifier 对齐，并要求当前计数不得低于原批次历史快照。同步修复新 12UJ 测试对686/39的硬编码，以防后续来源增补重复触发失败。该操作只改测试与本前瞻说明，不改旧证据、来源、图谱、状态、算法或当前阶段。

期待核验：`verify-historical-source-registry-extensions-r1.py`、`verify-project-continuity-state-r1.py`、12UI和12UJ两个专属单元测试组在新 exact HEAD 通过；旧失败 Actions 作为可审计历史保留。
