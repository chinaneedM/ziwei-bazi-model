# Fusion Chart Historical Provenance Audit R1 — Batch 12LI

## 全国报刊索引：公开活动页 inline / form 合同穷尽

Status: **ACTIVITY HTTP 200 / 0 FORMS / 0 ONCLICK / 2 INLINE SCRIPTS / 0 INLINE ROUTES / NO QUERY / ZERO PRODUCT IMPACT**

12LH 已证明活动页直接发出的六个外链脚本不能闭合 CNBKSY 业务检索路由。12LI 因而只回到同一个已匿名 HTTP 200 的第一方活动 HTML，检查页面自身是否还有 form/action、onclick 或 inline-script 合同。

控制 run `36880399113` / job `110430406848` 在 exact head `2346585319ea83902ea0c78fdeeb3ea3d2279b2a` 上成功。活动页本次返回 HTTP 200 / `text/html;charset=UTF-8` / `server: ESA`，17232 bytes，SHA-256 `99d70e27f16ac5c32798a7947e5fbadb1f2a7494ee55e208e6736d9841ed2f09`。

静态页面结构为：

- form：0；
- onclick handler：0；
- inline script：2；
- inline script route literal：0；
- configured search/query/find/navigation/AJAX/submit signal：0；
- href 仍只有 `/home`、`/signUp`、`/login` 与联系邮箱。

因此活动页这条公开分支在当前静态可见表面上已穷尽，但只能作如下有限裁决：

```text
ACTIVITY_PAGE_STATIC_SEARCH_CONTRACT = NOT_OBSERVED
ACTIVITY_PAGE_CONFIGURED_STATIC_SURFACE = EXHAUSTED
SITE_WIDE_SEARCH_ABSENCE = NOT_AUTHORIZED
TARGET_QUERY = NOT_SUBMITTED
```

公开搜索引擎另行索引到当前第一方 CNBKSY 新闻页 `/portal/newsCategoryBrowse/newsContent?id=202`。该页面公开描述数据库具有题名、作者、刊名、分类号、年份及期号检索能力，并发出“信息动态”等站内导航。下一门 12LJ 只把这个公开索引到的第一方 URL 用作 route-discovery 起点，跟随页面自己发出的“信息动态”导航并静态读取其 form/action/field/script 合同；不得把“站点新闻检索”混同于“历史报纸数据库检索”。

控制证据：workflow `.github/workflows/probe-batch-12li-cnbksy-public-activity-inline-contract.yml`; run/job/artifact `36880399113 / 110430406848 / 11170582729`; artifact digest `sha256:7b16b2890d5015ba8259546c972ce8c1bdd10c6709aa3b3c5dfdac0170a419e6`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-PUBLIC-ACTIVITY-INLINE-CONTRACT-R1.json`.
