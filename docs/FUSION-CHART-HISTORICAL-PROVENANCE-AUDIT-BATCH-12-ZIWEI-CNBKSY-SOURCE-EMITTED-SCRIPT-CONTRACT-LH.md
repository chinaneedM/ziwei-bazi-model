# Fusion Chart Historical Provenance Audit R1 — Batch 12LH

## 全国报刊索引：公开活动页 source-emitted 脚本合同审计

Status: **6/6 SCRIPTS HTTP 200 / NO BUSINESS SEARCH ROUTE LITERAL / THIRD-PARTY TOKEN NOISE EXCLUDED / NO ROUTE FOLLOWED / NO QUERY / ZERO PRODUCT IMPACT**

12LG 从匿名公开活动页获得六个明确 source-emitted script src。12LH 只读取这六个脚本本身；不猜 endpoint、不执行脚本中可能出现的路由、不登录、不注册，也不提交赵万里 / 文汇报目标查询。

控制 run `36879836981` / job `110428492239` 在 exact head `0ca02033ec670e021f212b69d0e452c217ea2c81` 上成功，六个脚本均为 HTTP 200：

- ESA 动态前置脚本：175000 bytes，SHA-256 `8e0c8b90…`；
- jQuery 3.1.1：277414 bytes，SHA-256 `9048fea1…`；
- jQuery 1.11.1：95790 bytes，SHA-256 `91222f96…`；
- Bootstrap：37051 bytes，SHA-256 `36460e49…`；
- PDF.js：421183 bytes，SHA-256 `deb1fd79…`；
- CNBKSY `common.js?version=V20241206`：4273 bytes，SHA-256 `3d7d6379…`。

Configured route-literal inventory 对六个脚本均未观察到 search/query/find/index/newspaper/resource/portal 等业务检索路径。jQuery、Bootstrap、PDF.js 内出现的 `query` / `find` / `search` 是库实现语义，不能计作《全国报刊索引》检索合同。ESA 动态脚本也没有命中配置的检索信号；`common.js` 仅观察到 `logout` 函数及通用 AJAX / `Array.indexOf(searchElement)` 语义，没有公开报纸检索路由。

因此：

```text
SOURCE_EMITTED_SCRIPT_FETCH = 6_OF_6_HTTP_200
PUBLIC_NEWSPAPER_SEARCH_ROUTE_LITERAL = NOT_OBSERVED
THIRD_PARTY_QUERY_FIND_SEARCH_TOKENS = NON_BUSINESS_NOISE
SEARCH_CONTRACT = NOT_YET_CLOSED
TARGET_QUERY = NOT_SUBMITTED
```

这不是“站点没有检索接口”的负面证明，只说明 **12LG 页面直接发出的六个外链脚本** 没有闭合检索合同。

下一门 12LI 回到已经匿名 HTTP 200 的活动 HTML，只解析 inline script、form/action、字段名、onclick handler 和 route literal；仍然发现而不执行。

控制证据：workflow `.github/workflows/probe-batch-12lh-cnbksy-source-emitted-script-contract.yml`; run/job/artifact `36879836981 / 110428492239 / 11170592063`; artifact digest `sha256:2f30de9a909488452724ba671e03b8b8033497fac9c393bfe3b9999a8f2431bb`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-SOURCE-EMITTED-SCRIPT-CONTRACT-R1.json`.
