# Historical Provenance Audit — Batch 12GC

## 1. Batch identity

- Batch: `BATCH-12-ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-PKU-STABLE-DETAIL-ARTICLEFILE-BOUNDARY-GC`
- Prior batch: `BATCH-12-ZIWEI-DENG-ZHICHENG-DIARY-2007-NLCPRESS-ITEM-DOWNLOAD-SURFACE-BOUNDARY-GB`
- Scope: current first-party PKU search backend → exact article identity → stable detail route → source-emitted ArticleFile boundary for 《五石斋文史札记》(二十八).
- This batch changes provenance/access certainty only. It does not reopen deterministic chart algorithms.

## 2. Question

Can the current official PKU platform close a stable article identity/detail route for 《五石斋文史札记》(二十八), and does the detail page's own ArticleFile action expose the primary article file/text?

## 3. Official search contract recovered from the page itself

The current PKU search page source directly emits:

- backend: `POST /Search/SearchArticleByElasticsearch`;
- anti-forgery token in the page;
- Title-field query object;
- current pagination call shape `pageSize/pageIndex/sortType/sortField/queryItem`;
- UI page-size choices 10 / 20 / 50 / **100**;
- result detail template `/article/info?aid={{item.id}}`.

No article ID was guessed or enumerated.

The source-defined Title query for `五石斋文史札记`, using 100/Page, returns **37** records in one page and exactly one installment-28 record.

## 4. Target article identity

The official backend currently returns:

- article ID: **286663046**;
- title: `《五石斋文史札记》(二十八)`;
- authors: 邓之诚 / 邓瑞;
- journal: 《中国典籍与文化》;
- year / issue: **2008 (03)**;
- volumeIssueId: **12482306**;
- pages: **121–129**;
- classification: K825.4;
- journalId: 94408;
- ISSN: 1004-3241.

The row also emits:

- `hasFullText=true`;
- `isFileExist=false`;
- `fulltextFId=null`;
- journal / issue / article shelf flags = true.

This current backend result independently re-closes the earlier FZ page-range metadata and, crucially, supplies the exact current article ID.

## 5. Stable detail route

Following only the ID returned by the official backend:

`https://ccj.pku.edu.cn/article/info?aid=286663046`

returns HTTP 200 and directly displays:

- exact title;
- 2008 (03);
- pp.121–129;
- authors and citation metadata.

Therefore:

`STABLE_TARGET_DETAIL_ROUTE=CLOSED_CURRENT_FIRST_PARTY_DETAIL_ROUTE`.

The page source also emits `mag-articleid="77845"`, but this secondary component identifier is not used to infer or enumerate another file route.

The rendered HTML contains a body template surface, but no directly rendered target journal body text was observed in this batch.

## 6. Source-emitted ArticleFile control

The target detail page itself hard-codes this download action:

`/Article/DownLoad?id=286663046&&type=ArticleFile`

This route was followed exactly as emitted. No login, guessed parameter, ID enumeration or bypass was used.

Observed response:

- HTTP 200;
- content type `application/json; charset=utf-8`;
- 114 bytes;
- SHA-256 `70e6fc2a80ba2a231907d056ee834355c3ef458e9165cf7adb3f81fdc1e6fe6b`;
- not PDF / not ZIP;
- JSON reports `succeeded=false`;
- error: **`文件不存在`**.

Therefore:

`CURRENT_PKU_ARTICLEFILE=SOURCE_EMITTED_ROUTE_RETURNS_FILE_NOT_FOUND`.

This is a current route/file-state conclusion only. It does not prove that no file ever existed historically and does not prove absence at CNKI, Wanfang, CQVIP, NSSD or another provider.

## 7. Authority firewall

The following equivalences are now explicitly forbidden:

- `hasFullText=true` ≠ currently retrievable article file;
- “Fulltext” label ≠ primary journal text reviewed;
- stable detail page ≠ page-image/glyph authority;
- `文件不存在` at PKU ArticleFile ≠ provider-wide content absence;
- current ArticleFile absence ≠ historical nonexistence;
- article pp.121–129 ≠ exact 1950-01-29 page;
- journal pagination ≠ 2007 facsimile pagination;
- date order ≠ permission to interpolate page number.

No authentication/paywall bypass, account action, purchase, fee, article-ID guessing or ID enumeration occurred.

## 8. Target status

Closed in this batch:

- article identity: **CLOSED_CURRENT_FIRST_PARTY_SEARCH_BACKEND**;
- article ID: **286663046**;
- article range: **121–129**;
- stable detail route: **CLOSED_CURRENT_FIRST_PARTY_DETAIL_ROUTE**;
- current PKU ArticleFile route: **FILE NOT FOUND**.

Still unresolved:

- whether 1950-01-29 is directly present in the serial text;
- exact journal page of 1950-01-29;
- primary journal wording;
- 2007 facsimile volume-5 exact page/leaf;
- handwriting;
- target 3482/3483 item-level transaction membership.

## 9. Product / genealogy consequence

No transmission node or edge is added.

`NODES_ADDED=0`; `EDGES_ADDED=0`; `ACQUISITION_EDGE_AUTHORIZED=false`; `SAME_OBJECT_EDGE_AUTHORIZED=false`; `RUNTIME_RULE_CHANGE=false`; `ALGORITHM_REOPEN=false`; `CANDIDATE_COLLAPSE=false`.

Matrix row/audited/missing counts remain **198 / 166 / 10**. Provenance defects remain **14 / 14 repaired**. Chart algorithm defects remain **0**. `DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED`.

## 10. Research runs

- Run `36095744082`: source-emitted PKU route/script discovery; artifact `10847102165`, digest `sha256:f39c0cb7aa7d8b834957f20353f7657114e7f5b173a7d639c5b10a8467221d3f`.
- Run `36096215694`: 37-record Title result set + exact installment-28 ID binding; artifact `10847970466`, digest `sha256:6c6c62b50525e9439daa7f00cec0e393b8f55c22bce0ba2bddb056f4c9f348b5`.
- Run `36096368404`: exact detail + source-emitted ArticleFile control; artifact `10847906395`, digest `sha256:d492143ae58fe67255ac87d6c3383aac75b23f4ae5c291bd13a7b4a523527c29`.

## 11. Highest next gate

1. Keep `aid=286663046` as stable PKU metadata identity and continue lawful primary/fulltext-page discovery through source-emitted PKU/provider routes; do not treat the current ArticleFile error as provider-wide absence.
2. Search exact 1950-01-29 quotations/citations that bind the entry to a specific journal page within pp.121–129; no interpolation.
3. Continue exact 2007 facsimile volume-5 page/leaf discovery and directly collate handwriting if obtained.
4. Search directly reviewed target/adjacent primary or facsimile pages for `铜壶漏箭制度`, `准斋心制几漏图式`, `3482/3483`, `03482/03483`, the 1823 士礼居 fingerprint or another stable identifier.
5. Continue Gu Tinglong 1950-01-06, NLC [23]/[24], Ji Shuying chapter 9 and Gao Xizeng annotated-catalog routes in parallel.

Machine evidence: `docs/research/ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-PKU-STABLE-DETAIL-ARTICLEFILE-BOUNDARY-R1.json`.
