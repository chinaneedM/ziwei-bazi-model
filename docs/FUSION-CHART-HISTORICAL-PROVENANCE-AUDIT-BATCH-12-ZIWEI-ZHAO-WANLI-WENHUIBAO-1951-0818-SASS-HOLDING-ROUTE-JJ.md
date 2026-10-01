# Fusion Chart Historical Provenance Audit R1 — Batch 12JJ

## 1951-08-18 上海《文汇报》刊载线索、上海社科院整年实体馆藏与同名报纸防混淆

Status: **SASS 1951 SHANGHAI WENHUI FULL-YEAR HOLDING CLOSED / SHANGHAI-HONG KONG TITLE DISAMBIGUATED / 1951 ARTICLE IDENTITY INSTITUTIONALLY CORROBORATED / AUG-18 WENHUI PUBLICATION SECONDARY LEAD ONLY / NO TARGET NEWSPAPER PAGE / WENHUI↔WENWU RELATION UNRESOLVED / ZERO PRODUCT IMPACT**

### 1. 目标

12JI 后最高门仍是 2011《赵万里文集》第1卷 p.197。新检索同时出现一条同年原始报刊线索：公开年谱类页面称赵万里《〈永乐大典〉展览的意义》载于 1951-08-18 上海《文汇报》。

12JJ 不把该说法直接当成首刊事实，而是分别审计：

1. 1951 上海《文汇报》是否存在可追溯的一手馆藏路线；
2. “上海《文汇报》”是否可能和香港同名报纸混淆；
3. 1951 文章身份是否有独立机构回顾佐证；
4. 是否真正审读到 1951-08-18 报纸原页；
5. 与《文物参考资料》第2卷第9期 pp.221–233 的关系是否能够关闭。

### 2. 上海社科院第一方旧报纸馆藏

上海社会科学院图书馆公开“纸媒目录”HTTP 200。UTF-8 校准后，页面直接列出：

- 上海《文汇报》：1951年1－12月；
- 《文汇报(香港)》：1951年1－3月。

因此可以关闭：

```text
Shanghai Wenhui 1951 full-year physical holding route = CLOSED
Shanghai Wenhui != Hong Kong Wenhui at this catalog level
```

但该目录没有 1951-08-18 版面图像、版次、文章题名或正文，所以“整年馆藏”不能升级成“目标文章已见”。

### 3. 清华机构回顾控制

清华校友网公开文章可直接检出赵万里、1951、《〈永乐大典〉展览的意义》及展览语境。它独立支持“1951 年赵万里主持展览并撰写该文”。

该页面没有“8月18日”，也没有“文汇报”。因此它只能关闭文章身份/历史背景的现代机构回顾层，不能关闭刊载日期或报纸身份。

### 4. 1951-08-18 上海《文汇报》二手线索

公开 Web 检索可发现年谱类页面声称：

```text
作《〈永乐大典〉展览的意义》，载8月18日上海《文汇报》
```

控制性 runner 对该页面 HTTPS 路线出现 connection reset，HTTP 路线出现 connect timeout；没有关闭直接页面对象。项目未关闭 TLS 校验、未绕过访问控制，也没有把搜索索引文本升级成第一方报纸证据。

当前裁决：

```text
1951-08-18 Shanghai Wenhui publication
= SECONDARY_LEAD_UNVERIFIED_BY_PRIMARY_PAGE
```

### 5. 控制性探针

- workflow: `.github/workflows/probe-batch-12jj-zhao-wenhui-1951-sass-holding.yml`
- exact probe head: `0aeae73c97d08bab01d1f1d80646d6c9c6d2e279`
- run: `36828765852`
- job: `110260317546`
- artifact: `11146151782`
- artifact digest: `sha256:c922718224ac493d59328c98e49fd99f1a181158e6855e13a982736106578f61`

SASS response SHA-256: `6ddba5f0bc79d73e265dbf0c1df8ca0a3715ed696f0d9f723f17f69faabea6e1`.

Tsinghua response SHA-256: `0904dec98fdfe12663cafe57e5c142538b41708a0691c69cde9ff934be445c0a`.

### 6. 证据防火墙

```text
physical yearly holding != target article presence
same-year article identity != publication venue/date
secondary chronology != primary newspaper page
same article title across newspaper/periodical != proven textual identity
publication-date claim != direct text review
Shanghai Wenhui != Hong Kong Wenhui
runner transport failure != negative content evidence
modern institutional retrospective != original 1951 text
```

### 7. 与《文物参考资料》的关系

当前仍不知道上海《文汇报》版本若存在，究竟是：

- 首刊后转载至《文物参考资料》；
- 报刊摘载/节本；
- 同题不同修订稿；
- 书目年谱误记；
- 或其他传播关系。

在直接取得至少一方页级文本并进行机械校勘之前：

```text
WENHUI_TO_WENWU_ISSUE9_RELATIONSHIP=UNRESOLVED
FIRST_PUBLICATION_STATUS=UNRESOLVED
```

### 8. 项目影响

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；chart algorithm defects 0；reopen 0；candidate collapse 0。无 runtime、产品或 transmission graph 修改；`TRANSMISSION_IMPACT=NONE`。

### 9. 下一门

新增一条并行高价值路线：直接取得并审读上海《文汇报》1951-08-18 原版或合法页级替代物。只有届时才能判断 8 月 18 日刊载与《文物参考资料》第9期 pp.221–233 的先后、同文/异文关系。

与此同时继续最高门：2011《赵万里文集》第1卷 p.197，以及 1951《文物参考资料》第9期 pp.221–233 的直接页级恢复。

Research record: `docs/research/ZIWEI-ZHAO-WANLI-WENHUIBAO-1951-0818-SASS-HOLDING-ROUTE-R1.json`.
