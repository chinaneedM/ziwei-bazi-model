# Fusion Chart Historical Provenance Audit R1 — Batch 12KE

## 国家图书馆文津赵万里《永樂大典展覽的意義》文章级命中

Status: **TRADITIONAL TITLE = 1 HIT / SIMPLIFIED TITLE = 0 / SAME RECORD UNDER AUTHOR+TITLE / 1951 JOURNAL ARTICLE / PP.221-233 / 13 PAGES / FULLTEXT FACET PRESENT / SOURCE-EMITTED DOCID CLOSED / DIRECT ARTICLE TEXT NOT YET REVIEWED / CARRIER LABEL TENSION PRESERVED / ZERO PRODUCT IMPACT**

### 1. 目标

12KD 已证明 2004《文汇报》13-DVD 的匿名 `uri/directLink` 为空，因此不再围绕该路线反复尝试。12KE 转回最直接文本目标：只使用 12JX 从国家图书馆第一方脚本恢复的文津 GET 合同，检索赵万里 1951 年《永乐大典展览的意义》。

### 2. 字符形态决定当前索引命中

正控“史记”仍返回约 67,000 条，说明本次文津结果面有效。

目标检索出现明确差异：

- `永乐大典展览的意义` → 0；
- `永樂大典展覽的意義` → **1**；
- `赵万里 永乐大典展览的意义` → 0；
- `趙萬里 永樂大典展覽的意義` → **1**；
- 简体题名 + 副题组合 → 0。

因此简体 0 命中只能解释为**当前索引字符/检索形态边界**，绝不能作为文章不存在的负证据。

### 3. 唯一命中记录

繁体题名结果页直接显示：

```text
永樂大典展覽的意義——一九五一...
文献类型：期刊论文
著者：趙萬里
出版年份：1951
来源：文物,1951年第9期221-233,共13页
来源数据库：
  国家哲学社会科学文献中心中文期刊论文
  维普中文科技期刊数据库
全文：可提供全文
```

结果页还直接 source-emit：

```text
docId = 149819805017800696
dataSource = sky,wpqk
detail path = /search/showDocDetails?
```

繁体“作者 + 题名”查询返回同一个 record，因此 item-level 身份不是模糊的宽题名偶合。

### 4. “文物”与“文物参考资料”不得静默合并

12JK 的国家图书馆官方现代综述明确著录载体为《文物参考资料》1951年第9期 pp.221–233；12KE 当前文津联邦记录的“来源”则显示为“文物,1951年第9期221-233”。

两者页码、年份、期号和作者/题名高度对应，但本项目不依靠相似度自动归一化题名。当前状态：

```text
WENJIN CURRENT SOURCE LABEL = 文物
NLC REVIEW BIBLIOGRAPHIC LABEL = 文物参考资料
RELATION = PENDING FIRST-PARTY DETAIL / CROSSWALK
```

这可能是数据库规范化题名，也可能涉及刊名沿革或索引约定；必须由详情或独立书目交叉证据关闭。

### 5. “可提供全文”不等于已经取得全文

结果筛选面显示“可提供全文”，但 12KE 没有点击在线阅读、没有进入来源数据库、没有登录，也没有审读 1951 原页。因此：

```text
DIRECT_1951_ARTICLE_TEXT = NOT_REVIEWED
```

### 6. 控制证据

- workflow: `.github/workflows/probe-batch-12ke-nlc-wenjin-yongle-article-title-search.yml`
- exact head: `3f3de8e7d7c29e4bcf3789686e2c586bb8774c4e`
- run / job / artifact: `36855360257 / 110346462680 / 11157847229`
- artifact digest: `sha256:9c68b9933d57cc358d6cfbe413085fbed864118f12f7ccab76b3d4ac09f279a6`

### 7. 项目影响与下一门

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission Graph 暂不加边。

下一门 12KF 只沿结果页直接发出的 `149819805017800696 / sky,wpqk` 读取匿名详情，重点检查：

1. 完整题名/副题与载体字段；
2. “文物”与“文物参考资料”的题名关系是否能在第一方详情关闭；
3. 是否 source-emit 具体全文 URI / directLink；
4. 若全文需要登录或第三方服务，则只记录边界，不绕过。

Research record: `docs/research/ZIWEI-NLC-WENJIN-ZHAO-YONGLE-ARTICLE-TITLE-SEARCH-R1.json`.
