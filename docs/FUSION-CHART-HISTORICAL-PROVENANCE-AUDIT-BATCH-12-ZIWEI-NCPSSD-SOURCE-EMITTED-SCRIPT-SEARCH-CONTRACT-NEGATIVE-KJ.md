# Fusion Chart Historical Provenance Audit R1 — Batch 12KJ

## NCPSsd 首页 source-emitted 外部脚本：搜索函数仍未发现

Status: **13 SOURCE-EMITTED EXTERNAL SCRIPTS / ALL HTTP200 / SIX TARGET FUNCTIONS ABSENT / 12KI+12KJ COVER INLINE+EXTERNAL SCRIPT CLASSES / EXECUTABLE SEARCH CONTRACT UNRESOLVED / NO QUERY / ZERO PRODUCT IMPACT**

12KI 已检查当前 NCPSsd 首页全部 6 个无 src 内联 script；12KJ 再按首页真实 script src 清单逐个读取 13 个外部脚本。当前首页对象仍为 HTTPS 200、198,008 bytes、SHA-256 `19823cf7d2d3a89bd3f86081b113f779507ebe45acb86273fd961b537b056544`。

13 个外部脚本全部成功读取，但 `Basicsearch / AdvancedSearch / Search_text / qkSearchCondition / Search_GJ / waiwen_search` 六个目标函数名全部未出现。与 12KI 合并后：

```text
INLINE SCRIPTS       = 6  / TARGET DEFINITIONS 0
EXTERNAL SCRIPT SRCS = 13 / TARGET NAME HITS 0
```

首页 UI 仍真实存在 `text_search`、`select_type=TS`、`hidSearchType=0`、`hidSearchValue=0` 与 `onclick="Basicsearch()"`，但函数调用本身不构成 endpoint/参数合同。已观察到的 `POST /searchHandler/getautocomplete` 只属于自动补全，禁止把它升级为正式结果检索 endpoint。

控制证据：workflow `.github/workflows/probe-batch-12kj-ncpssd-source-emitted-script-search-contract.yml`；exact head `4dd1b138bb1f26b3cf5fc908dd34ee44ed1ee8c6`；run/job/artifact `36859077093 / 110358543477 / 11160726318`；artifact digest `sha256:781f93317cfc4e8a44e804cac08f8dc13a1f945be9c40dd12ffeb29091faa65b`。

下一门 12KL 只枚举同一首页源码中已经写出的 route literal、AJAX url、location/window.open 导航表达式以及搜索控件附近路径常量；本批不请求任何候选路由、不提交查询。

Matrix 继续 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission Graph 不变。

Research record: `docs/research/ZIWEI-NCPSSD-SOURCE-EMITTED-SCRIPT-SEARCH-CONTRACT-NEGATIVE-R1.json`.
