# Fusion Chart Historical Provenance Audit R1 — Batch 12LT

## 全国报刊索引：“使用帮助”根正文动态闭合

Status: **ROOT HELP CONTENT HTTP 200 / GENERIC SUPPORT TEXT ONLY / ZERO SEARCH-FIELD SEMANTICS / NO LINK FOLLOW / NO QUERY / ZERO PRODUCT IMPACT**

控制 run `36892057259` / job `110469837665` / artifact `11177147183` 在 exact head `c240d0564fa06838ac666ed20502be4f1cd16839` 上只复现页面活动 `init()`：`POST /portal/footCategory/findNews?id=61` + 空对象。同一匿名 session 的 `_csrf` 仅进入请求 query，未记录其值，也没有使用动态 tree ID payload。

响应为 HTTP 200 `application/json;charset=UTF-8`，3831 bytes，SHA-256 `9d3e42888751ff998e76508b2325962ab1ffa7101f6721e85c1f21e5c5734ca6`。JSON `title=使用帮助`；`content` 长 591、SHA-256 `55be4b4fb7cc3bd728c733690ebe55778252ff5ae07cdfad93e39dd6a7fab35f`；去 HTML 后可见正文仅 131 字符，内容是浏览器兼容与客服联系信息。

`普通检索 / 高级检索 / 专业检索 / 图片检索 / 题名 / 作者 / 刊名 / 分类号 / 年份 / 期号 / 检索词 / 关键词 / 全文 / 逻辑 / 布尔` 在动态根正文中仍全部为 0。故不能把根“使用帮助”当成字段级检索手册。

正文中只抽出一个 source-emitted href-like literal `http://service@cnbksy.com`。该值按原样保存，不跟随、不纠正、不推定为有效 Web URL；页面可见文本另写 `E-mail: service@cnbksy.com`，二者保持层次分离。

下一门 12LU 使用 12LS 已闭合的第一方节点 `161 用户手册下载`，按活动 `zTreeOnClick` 契约只执行 `POST /portal/footCategory/findNews` + form payload `id=161`，盘点返回标题/正文及链接但不跟随。不得猜其他 ID，不提交任何目标检索词。

控制证据：workflow `.github/workflows/probe-batch-12lt-cnbksy-help-root-content-contract.yml`; run/job/artifact `36892057259 / 110469837665 / 11177147183`; artifact digest `sha256:336b0c50b25c43a40f1e9eef3a966b6df1987e9a03c1b209dc32b0c5542ed0a0`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-HELP-ROOT-CONTENT-CONTRACT-R1.json`.
