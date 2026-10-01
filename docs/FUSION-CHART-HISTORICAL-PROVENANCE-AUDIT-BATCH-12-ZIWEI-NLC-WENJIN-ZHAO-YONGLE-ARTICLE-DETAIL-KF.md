# Fusion Chart Historical Provenance Audit R1 — Batch 12KF

## 国家图书馆文津赵万里《永樂大典展覽的意義》详情与 NCPSsd source-emitted 路由

Status: **ANONYMOUS DETAIL HTTP200 / COMPLETE TITLE CLOSED / ZHAO WANLI CLOSED / 1951 NO.9 PP.221-233 CLOSED AT CURRENT FEDERATED METADATA LEVEL / ABSTRACT PRESENT / SOURCE LABEL = 文物 / NLC REVIEW LABEL = 文物参考资料 TENSION PRESERVED / NCPSsd URI SOURCE-EMITTED / DIRECTLINK EMPTY / WENJIN LOGIN REQUIRED / PRIMARY 1951 PAGES NOT REVIEWED / ZERO PRODUCT IMPACT**

### 1. 目标

12KE 已通过繁体题名唯一命中恢复 source-emitted `docId=149819805017800696 / dataSource=sky,wpqk`。12KF 只沿该控件匿名读取详情，不登录、不 POST、不猜 provider identifier。

### 2. 详情页直接闭合的文章级元数据

匿名详情返回 HTTP 200 / 30,605 bytes / SHA-256 `3ba53f14f4c21b2c6ba5ae6a1cf4be106e645c3da61d4d3ae4a3a4c068473d23`。

页面直接显示：

- 完整题名：**《永樂大典展覽的意義——一九五一年八月北京圖書舘舉辦》**；
- 责任者：**趙萬里**；
- 文献类型：期刊论文；
- 期刊名称：**文物**；
- 来源：**文物,1951年第9期221-233,共13页**；
- 期：9；卷：0；
- 语种：Chinese 汉语；
- 中图分类：K87；
- 中文摘要存在；
- 来源数据库：国家哲学社会科学文献中心中文期刊论文 / 维普中文科技期刊数据库。

这比 12KE 的结果列表更强，但仍是**当前联邦数据库元数据/摘要**，不是 1951 原期页影或原页正文。

### 3. “文物”与“文物参考资料”继续分离

12JK 的国家图书馆官方现代综述著录同一作者、同一题名、同一 1951 年第9期、同一 pp.221–233，但载体名写作《文物参考资料》；12KF 的当前文津详情仍明确写“文物”。

因此当前只能保留：

```text
WENJIN DETAIL LABEL = 文物
NLC REVIEW LABEL = 文物参考资料
YEAR / ISSUE / PAGES = 1951 / 9 / 221-233
RELATION = UNRESOLVED PENDING EXPLICIT CROSSWALK
```

不得依靠相似度静默改名或合并。

### 4. source-emitted NCPSsd 路由

详情页直接发出一个具体 `uri`，指向国家哲学社会科学文献中心的 `CooperationUser.aspx` 路由，并在其 `UrlReferrer` 中携带 articleinfo 目标。该 URI 来自页面本身，不是项目猜测。

同时：

```text
directLink = ''
isUserLogin = false
isInnerIP = false
isVpnLink = false
isSamlLink = false
```

文津页面明确提示“未登录情况下不能使用在线阅读功能，请您先登录”。因此 KF 不点击文津在线阅读，也不跟随外部 URI；只把它登记为下一门可校准的 source-emitted 公共 GET 路线。

### 5. 控制证据

- workflow: `.github/workflows/probe-batch-12kf-nlc-wenjin-zhao-yongle-article-detail.yml`
- exact head: `97883e2c6ce58b3a5bcbbfbbd6dcea3a403646ad`
- run / job / artifact: `36855851382 / 110348023825 / 11159156947`
- artifact digest: `sha256:c1f0e4ef6f7a5c7a9a7805be79e265447a0b8251e788e6e49d301d92bfdf02d4`

### 6. 项目影响与下一门

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission Graph 不加边。

下一门 **12KG** 只对 12KF 页面明确发出的 NCPSsd `CooperationUser.aspx` URI 做匿名 GET，并只接受其真实 HTTP 重定向链。若落到公开文章页，再检查它是否公开发出原文/PDF；若落到登录/授权边界，则立即收口，不绕过。

同时继续上海《文汇报》1951-08-18 与 2011《赵万里文集》第1卷 p.197 的直接恢复。

Research record: `docs/research/ZIWEI-NLC-WENJIN-ZHAO-YONGLE-ARTICLE-DETAIL-R1.json`.
