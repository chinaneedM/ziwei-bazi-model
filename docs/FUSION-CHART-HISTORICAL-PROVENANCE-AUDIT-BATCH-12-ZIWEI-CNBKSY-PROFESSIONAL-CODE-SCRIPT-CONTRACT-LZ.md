# Fusion Chart Historical Provenance Audit R1 — Batch 12LZ

## 全国报刊索引：专业检索字段代码脚本复核与入口绑定

Status: **SUBSTRING FALSE POSITIVES REPAIRED / EXACT FIELD-CODE HITS = 0 / PROFESSIONAL ROUTE SOURCE-CLOSED / NO ROUTE INVOKED / NO QUERY / ZERO PRODUCT IMPACT**

首轮 12LZ run `37020017898` / job `110880618487` / artifact `11232333861` 报告 2528 个 `PTI/NATI/ADPR` 等命中，但这些短码使用 substring 搜索，实际大量撞入 vendor/minified library 的普通字符序列。对 artifact 做严格词法边界复核后，专业字段代码精确命中为 **0**；因此首轮 run 明确 superseded，不得据其声称脚本含有专业字段代码。

修复 run `37021258360` / job `110884629398` / artifact `11233850753` 在 exact head `f5430c69cc5f56822e2ac02ed5f50ccdb9c95c1f` 上改用 exact lexical boundary。39 个同域 source-emitted scripts 中，五个第一方应用脚本 `productTree.js / app4O.js / common.js / sdUtils.js / promptMsg.js` 均无 `JTI/PTI/ADTI/FXJG/NATI/TSCT/ADPB/ADPR` 精确命中，也未暴露新的 search route literal。由此只能说**当前已加载脚本表面没有专业检索 request builder**，不能推断后端不存在。

更重要的是，两个公开第一方页面都直接输出同一组带标签导航：`普通检索=/search`、`高级检索=/search/advance`、`专业检索=/search/special`、`图片检索=/search/pic/`。因此 `/search/special` 已经是 source-emitted route，不需要猜 endpoint。

12LZ 全程只读公开 HTML/JS；没有调用 `/search/special`，没有提交赵万里、文汇报或任何目标词，也没有登录、注册或绕过 ESA。下一门 12MA 只允许对这个 source-emitted 专业检索页面做一次无查询匿名 GET，并静态盘点返回面；若遇 ESA/browser challenge，必须原样记录，禁止绕过。

控制证据：workflow `.github/workflows/probe-batch-12lz-cnbksy-professional-code-script-contract.yml`; repaired run/job/artifact `37021258360 / 110884629398 / 11233850753`; artifact digest `sha256:086b1aedc1240dc1dff69380de92b2f0bfabdad4d4eb37e03223e3a20b8cad60`.

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-PROFESSIONAL-CODE-SCRIPT-CONTRACT-R1.json`.
