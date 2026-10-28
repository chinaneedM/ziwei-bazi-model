# 天问13IY｜Git父提交异常状态文件的前向恢复证据

## 不得把异常提交的三个文本文件作为研究事实源

- 最后已核验的健康前置 HEAD：`78e0a7ac59bdb7a007b4ceb4d8c0a15d32a892ad`，state/ledger=1.903.0，来源注册合计761。
- 13IY 初次历史记录提交 `3ae9c7996bb4b29803f55b1203e9a151ca815694` 中，`docs/PROJECT-CURRENT-STATE-R1.json`、`docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json` 和来源扩展 manifest 被工具端序列化错误写成字面量 `undefined\\n`；不可当作有效 JSON 或新研究判断。这是**文件写回缺陷**，不是原史料版本冲突，不是算法缺陷。
- 补救 HEAD `947af6e81bd2cd84ec3657ec7dbe37a6280d50fd` 以经过解析的健康前置远端三份文件重建，严格追加13IY源证据、状态1.904.0、来源总量763及风险历史；重读三份文件均为有效 JSON。全量前向对比证实旧2625研究焦点保留、其他10项风险原样保留、TW-OPEN-0005历史前缀保留、历史checkpoint前缀保留、旧65来源分片哈希全部保持不变、排盘不变量未变。
- 在修复HEAD上执行 `scripts/verify-research-omission-risk-ledger-r1.py --check-parent` 会因为它的**直接父提交**是无效JSON而抛JSONDecodeError。这是历史工具写回问题的预期父链污染，绝非史料门禁真实失效；不修改检验器、不降级forward-only要求。后继提交以有效947af6e8为直接父提交后，该同一标准校验应自行恢复。
- 本提交同时将 66 分片的 source-extension manifest schema_version 从1.65.0更新为1.66.0（仅元数据版本同步）；不改变来源计数、风险研判、算法及传承谱结论。

凡后续考证、状态读取、Actions核验应以**实时远端HEAD**为准，不得引用坏提交作为有效状态。13IY官方原文取证直接证据仍以 GitHub Actions 40631928662 / artifact 12791554120 和官方 KHS 原文SHA为准。
