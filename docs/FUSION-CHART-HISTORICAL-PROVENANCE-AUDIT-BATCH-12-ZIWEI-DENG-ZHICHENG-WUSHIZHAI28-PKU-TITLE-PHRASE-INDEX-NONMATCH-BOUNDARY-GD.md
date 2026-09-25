# Historical Provenance Audit — Batch 12GD

## 1. Batch identity

- Batch: `BATCH-12-ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-PKU-TITLE-PHRASE-INDEX-NONMATCH-BOUNDARY-GD`
- Prior batch: `BATCH-12-ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-PKU-STABLE-DETAIL-ARTICLEFILE-BOUNDARY-GC`
- Scope: current PKU search-index behavior for known derivative 1950-01-29 phrases under a source-emitted two-condition query constrained to the 《五石斋文史札记》 series.
- This is an index-coverage/access-semantics batch only. It does not establish primary article wording and does not reopen deterministic chart algorithms.

## 2. Question

Can the current PKU search backend reproduce known derivative phrases inside the target installment, and if it does not, what evidentiary meaning is permitted?

## 3. Why the first broad probe was insufficient

The first GD probe queried five phrases as broad All-fields searches:

- `四千万人民券`
- `十二箱`
- `以归公`
- `一月二十九日`
- `铁琴铜剑楼`

Those searches had total result counts ranging from 1,183 to 44,898, while only the top 100 results were retrieved. Target article `286663046` did not appear in those top-100 sets.

That is **not** target-specific negative evidence and is not used for textual adjudication.

## 4. Source-emitted two-condition query

The PKU advanced-search page itself accepts multiple conditions and emits the corresponding `queryItem` array. The scoped probe therefore:

1. GETs the public advanced-search URL with:
   - Title = `五石斋文史札记`;
   - All fields = tested term;
   - boolean relation = AND.
2. Parses the exact `queryItem` array emitted by PKU.
3. Calls `POST /Search/SearchArticleByElasticsearch` only if the page itself emitted both conditions.
4. Uses 100/Page, matching the current UI.
5. Never guesses an article ID or backend operator.

## 5. Positive control

The positive control uses:

- Title = `五石斋文史札记`
- All fields = `邓之诚`
- AND

PKU source-emits exactly two query items. The backend returns **37** records, matching the full current series result count established in GC, and includes target article **286663046** exactly once.

The returned target row remains:

- 《五石斋文史札记》(二十八)
- 中国典籍与文化
- 2008 (03)
- pp.121–129
- `hasFullText=true`
- `isFileExist=false`
- `fulltextFId=null`

Therefore the two-condition mechanism is demonstrated to be operational for the target series.

## 6. Tested derivative phrases

Using the same source-emitted two-condition mechanism:

| Phrase | Series results | Target 286663046 |
|---|---:|---:|
| 四千万人民券 | 0 | 0 |
| 十二箱 | 9 | 0 |
| 以归公 | 4 | 0 |
| 一月二十九日 | 20 | 0 |
| 铁琴铜剑楼 | 1 | 0 |

Thus all five tested phrases are:

`CURRENT_SEARCH_INDEX_NONMATCH_UNDER_TESTED_TITLE_SCOPED_QUERY`.

## 7. What this does **not** prove

The result is **not** a negative collation of the 2008 article.

Reasons:

- the target's current PKU abstract field is empty;
- GC established `isFileExist=false`;
- GC established `fulltextFId=null`;
- the source-emitted ArticleFile action currently returns `文件不存在`;
- the project has not demonstrated that PKU's All-fields search indexes the complete article body for this target.

Therefore:

- index nonmatch ≠ phrase absent from article;
- index nonmatch ≠ phrase absent from journal page;
- index nonmatch ≠ contradiction of the 2012 derivative quotation;
- index nonmatch ≠ handwriting authority.

This batch closes only the **current PKU index-route usefulness boundary** for these five derivative phrases.

## 8. Authority firewall

The following rules are now explicit:

- positive control is required before interpreting scoped nonmatch;
- broad top-100 nonmatch is not negative evidence;
- scoped index nonmatch ≠ article-text absence;
- search-index match/highlight ≠ primary page glyph;
- empty abstract ≠ empty article;
- pp.121–129 ≠ exact 1950-01-29 page;
- journal pagination ≠ 2007 facsimile pagination;
- no date-to-page interpolation.

No authentication/paywall bypass, ID enumeration, account action, purchase or fee occurred.

## 9. Target status

Unchanged primary target status:

- article ID: `286663046`;
- article range: **121–129**;
- stable detail route: closed;
- current PKU ArticleFile: source-emitted route returns file not found;
- known derivative phrase index status: **CURRENT_SEARCH_INDEX_NONMATCH_UNDER_TESTED_TITLE_SCOPED_QUERY**;
- 1950-01-29 exact journal page: **UNRESOLVED**;
- primary journal text: **NOT_REVIEWED**;
- 2007 facsimile exact page/leaf: **UNRESOLVED**;
- handwriting: **NOT_DIRECTLY_COLLATED**.

## 10. Research runs

- Broad control run `36096798823`; artifact `10847607831`; digest `sha256:44e6617b58ec2105367639db6f279f8c4c45a8c0bf80a6ae6d06e512b7b36cb7`.
- Scoped two-condition run `36097046685`; artifact `10846993957`; digest `sha256:f8f353ac63def02584f394e668bb47d5faa0e438b4ec02158048b9342507d3a4`.

## 11. Product / genealogy consequence

No transmission node or edge is added.

`NODES_ADDED=0`; `EDGES_ADDED=0`; `ACQUISITION_EDGE_AUTHORIZED=false`; `SAME_OBJECT_EDGE_AUTHORIZED=false`; `RUNTIME_RULE_CHANGE=false`; `ALGORITHM_REOPEN=false`; `CANDIDATE_COLLAPSE=false`.

Matrix row/audited/missing counts remain **198 / 166 / 10**. Provenance defects remain **14 / 14 repaired**. Chart algorithm defects remain **0**. `DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED`.

## 12. Highest next gate

1. Stop treating PKU phrase-index searches as a route to primary negative proof; prioritize source-emitted primary page/fulltext objects or independent exact page citations.
2. Seek an exact scholarly/primary citation that binds the 1950-01-29 entry to one page inside pp.121–129 without interpolation.
3. Continue exact 2007 facsimile volume-5 page/leaf discovery and direct handwriting collation.
4. Search directly reviewed target/adjacent primary or facsimile pages for `铜壶漏箭制度`, `准斋心制几漏图式`, `3482/3483`, `03482/03483`, the 1823 士礼居 fingerprint or another stable identifier.
5. Continue Gu Tinglong 1950-01-06, NLC [23]/[24], Ji Shuying chapter 9 and Gao Xizeng annotated-catalog routes in parallel.

Machine evidence: `docs/research/ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-PKU-TITLE-PHRASE-INDEX-NONMATCH-BOUNDARY-R1.json`.
