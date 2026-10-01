# Fusion Chart Historical Provenance Audit R1 — Batch 12JI

## 国家图书馆出版社《赵万里传》编辑团队背景桥与 p.197 同号防误认

Status: **FIRST-PARTY PRODUCT CLOSED / EDITORIAL-TEAM RELATION CLOSED / BIOGRAPHY TOC 197 DISAMBIGUATED / PUBLIC BOOKTEXT BOUNDED / TARGET QUOTE TOKENS NOT OBSERVED / DIRECT 2011 P197 NOT REVIEWED / ZERO PRODUCT IMPACT**

### 1. 目标

12JH 后最高门仍是 2011《赵万里文集》第1卷 p.197 的合法直接页级恢复。12JI 检查国家图书馆出版社公开的刘波《赵万里传》Product 11443：它是否能直接恢复目标页，或至少提供可严格限定的编辑团队背景与出处线索。

### 2. 第一方对象与目录

出版社公开页直接绑定《赵万里传》、刘波、ISBN 9787501371655、出版时间 2021-07-30，并公开 Booktext postback。页面目录显示：

- “弢翁挚友 / 197”；
- “劝导藏家捐赠图书 / 255”；
- “大举购入善本古籍 / 258”。

因此页面中的数字 197 属于《赵万里传》自身目录，不能与 2011《赵万里文集》第1卷 p.197 合并。

出版社页面后记同时明确刘波 2010 年加入《赵万里文集》编辑团队。该事实只关闭现代编辑团队关系，不等于审读过当前目标页。

### 3. 控制性探针

- workflow: `.github/workflows/probe-batch-12ji-zhao-wanli-zhuan-nlcpress-editorial-bridge.yml`
- exact probe head: `38a9ab8cd86febb6b69bd1999586149f9d02d833`
- run: `36824880534`
- job: `110248229760`
- artifact: `11144523100`
- artifact digest: `sha256:a734134d74bbe1de922954f1b4f0977168827ce3320a03ee2ae45e3db69cf885`

source-emitted Booktext 返回 HTTP 200、6,496 bytes、GB18030、3,682 normalized chars，正文 SHA-256 为 `3da910b9bd88ef8fe6fe3318c814faeda10e2283b12e038760b0b523aa4a4312`。探针不保存、不输出原始正文。

### 4. 目标词校准

Booktext 可见产品/作者/编辑团队/目录标志，但配置的瞿济苍、瞿凤起、瞿旭初、六十二种、《春秋左传注疏》、丁惠康、《东家杂记》《太平乐府》、《文物参考资料》与 1951 等目标词均未出现。

此结论只适用于当前公开 Booktext payload；不得外推为实体《赵万里传》全文不存在这些内容。

### 5. 裁决与证据防火墙

- Product 11443 identity: CLOSED
- 刘波参与《赵万里文集》编辑团队：CLOSED_AT_FIRST_PARTY_MODERN_RETROSPECTIVE_LEVEL
- 《赵万里传》“197”：UNRELATED_BIOGRAPHY_TOC_PAGE_NUMBER
- 传记 p.255 / p.258 章节标题：CLOSED
- 传记 p.255 / p.258 正文：NOT_REVIEWED
- direct 2011 Wenji p.197：NOT_REVIEWED
- direct 1951 pp.221–233：NOT_REVIEWED

必须保持：

```text
same page number != same page object
editor participation != direct target-page review
chapter heading != chapter body
modern retrospective != 1951 primary text
public payload absence != physical-book absence
```

### 6. 项目影响

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；chart algorithm defects 0；reopen 0；candidate collapse 0。无 runtime、产品或 transmission graph 修改；`TRANSMISSION_IMPACT=NONE`。

### 7. 下一门

最高门不变：继续新的合法 2011《赵万里文集》第1卷 p.197 页级路线；并行继续 1951 pp.221–233 与 1997 pp.446–449。若未来出现《赵万里传》p.255–258 的合法页级对象，只能先作为现代回顾/引文桥，除非它能明确回指并校验原始对象。

Research record: `docs/research/ZIWEI-ZHAO-WANLI-ZHUAN-NLCPRESS-EDITORIAL-BRIDGE-R1.json`.
