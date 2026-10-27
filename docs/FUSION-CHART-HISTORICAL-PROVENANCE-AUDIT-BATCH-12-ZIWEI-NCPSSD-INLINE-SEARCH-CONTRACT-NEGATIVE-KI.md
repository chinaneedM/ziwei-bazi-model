# Fusion Chart Historical Provenance Audit R1 — Batch 12KI

## NCPSsd 首页内联搜索合同：目标函数未发现

Status: **HOME OBJECT REPLAYED / 6 INLINE SCRIPT BLOCKS / BASICSEARCH NOT INLINE / ADVANCEDSEARCH NOT INLINE / SEARCH_TEXT NOT INLINE / HIDESEARCH INLINE ONLY / KH INLINE HYPOTHESIS REFUTED / EXECUTABLE CONTRACT STILL UNRESOLVED / NO QUERY / ZERO PRODUCT IMPACT**

12KH 观察到 `Basicsearch()` 等 onclick 控件，但尚未定位函数定义。12KI 对同一首页对象的所有无 `src` 内联 script 做 brace-aware 函数抽取。

结果：`Basicsearch / AdvancedSearch / Search_text / qkSearchCondition / Search_GJ / waiwen_search` 全部未发现；只有 `hideSearch()` 被直接定义，SHA-256 `ccbcf39d89619b7b01640f38ef8df9cb86294994b6378cb6fb41a9bc6258df75`。

因此 KH 的“相关搜索逻辑很可能内联”只是工作假设，现已被直接源码检查推翻。当前仍不能猜 endpoint 或参数。

控制证据：workflow `.github/workflows/probe-batch-12ki-ncpssd-inline-search-contract.yml`；exact head `5a95c334f1147070f66bd175f4dca4547fe7d111`；run/job/artifact `36858551261 / 110356811675 / 11159996909`；artifact digest `sha256:2e5d7a674f5028a07334526e3d3cb6e9c4e78f88ef8e8d67839690eee444b0d5`。

Matrix 继续 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。

下一门 12KJ 枚举首页真正发出的全部 `<script src>`，不再限制 host；只沿这些 source-emitted 脚本寻找目标函数定义。查询仍不得执行。

Research record: `docs/research/ZIWEI-NCPSSD-INLINE-SEARCH-CONTRACT-NEGATIVE-R1.json`.
