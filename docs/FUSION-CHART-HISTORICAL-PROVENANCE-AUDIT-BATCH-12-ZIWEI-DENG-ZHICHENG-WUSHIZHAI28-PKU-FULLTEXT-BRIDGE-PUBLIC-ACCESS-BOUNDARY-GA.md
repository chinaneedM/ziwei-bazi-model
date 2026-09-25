# Fusion Chart Historical Provenance Audit R1 — Batch 12GA

## 《五石斋文史札记（二十八）》：北大官方全文桥五路当前公开访问边界

Status: **PKU OFFICIAL ISSUE FULLTEXT BRIDGE DIRECTLY REVIEWED / 5 OUTBOUND ROUTES ADJUDICATED AS CURRENT ACCESS BOUNDARIES / TARGET PRIMARY TEXT NOT OBTAINED / PP.121–129 RANGE PRESERVED / JAN-29 EXACT PAGE UNRESOLVED / ZERO DEFECT OR RUNTIME CHANGE**

## 1. Trigger

Batch 12FZ closed the article's first-party indexed bibliographic range as **121–129** and repaired the incompatible FY p120 secondary anchor. The highest remaining journal-side gate is not another page-number estimate; it is acquisition of the actual primary article pages or a source-emitted fulltext object.

The official Peking University 2008 Issue 03 page exposes five outbound **Fulltext link** routes. Batch 12GA tests those routes without logging in, bypassing access controls, purchasing content, or guessing article identifiers.

## 2. Official bridge

The first-party PKU issue object remains:

- journal: 《中国典籍与文化》
- year / issue: 2008 / 03
- `jid=94408`
- `viid=12482306`

The issue page visibly exposes five outbound labels:

1. Official website
2. National social sciences database
3. 知网
4. 万方
5. 维普

The presence of those links is **not** itself evidence that the target article bytes were retrieved.

## 3. Current public route observations

### 3.1 凤凰出版社

The publisher route currently lands on the generic 凤凰出版社 homepage. No source-emitted target article object or target text is present on the reviewed surface.

This is an access/navigation boundary only. It does not prove the publisher has no archive.

### 3.2 国家哲学社会科学文献中心 / NSSD

The exact legacy journal route emitted by PKU currently returns HTTP 404 in the reviewed public environment.

This does not prove target-content absence at NSSD; it proves only that this legacy route no longer directly resolves.

### 3.3 中国知网 / CNKI

The PKU-emitted journal-navigation route currently returns an HTTP 502 fetch boundary in the reviewed environment.

No target article text was obtained. No content-negative claim is authorized.

### 3.4 万方

The PKU route redirects to the current Wanfang magazine surface and presents a JavaScript/account-oriented shell. The reviewed static surface does not emit the target article text.

No login or institutional-account action was attempted.

### 3.5 维普

The PKU-emitted CQVIP journal-summary route currently returns HTTP 412 Precondition Failed in the reviewed environment.

No bypass was attempted and no content-negative inference is authorized.

## 4. PKU target-detail control

The prior PKU search index emitted the exact target title and pp.121–129. A candidate detail URL surfaced through search indexing, but direct opening currently misroutes to another Peking University journal.

Therefore:

`FIRST_PARTY_INDEX_RANGE_121_129=VALID`

`STABLE_TARGET_DETAIL_ROUTE=NOT_OBSERVED`

`TARGET_DOWNLOAD_OBJECT_SOURCE_EMITTED=false`

`TARGET_PRIMARY_TEXT_SOURCE_EMITTED=false`

No `aid` enumeration or guessed-ID probing was performed.

## 5. Authority firewall

The following equivalences are explicitly forbidden:

- Fulltext-link presence ≠ target fulltext retrieval.
- HTTP 404/412/502 ≠ provider content absence.
- JavaScript/login shell ≠ provider content absence.
- Generic publisher homepage ≠ no archive.
- First-party 121–129 metadata ≠ direct page glyphs.
- 121–129 article range ≠ proof that the 1950-01-29 entry is present.
- article range ≠ exact Jan-29 page.
- journal pagination ≠ 2007 facsimile pagination.

No authentication bypass, paywall bypass, guessed article-ID enumeration, provider-account action, purchase, or fee occurred.

## 6. Target status

The article range remains **121–129** at the first-party PKU indexed-metadata layer.

Still unresolved:

- whether the 1950-01-29 diary entry is present in the serial article;
- its exact journal page;
- the primary journal wording;
- the 2007 facsimile volume-5 page/leaf;
- the direct handwriting collation;
- whether the target 1823 《铜壶漏箭制度》 / 《准斋心制几漏图式》 object belonged to the reported twelve-box purchase.

## 7. Product / genealogy consequence

This is an access-boundary batch only.

`NODES_ADDED=0`; `EDGES_ADDED=0`; `ACQUISITION_EDGE_AUTHORIZED=false`; `SAME_OBJECT_EDGE_AUTHORIZED=false`; `RUNTIME_RULE_CHANGE=false`; `ALGORITHM_REOPEN=false`; `CANDIDATE_COLLAPSE=false`.

Matrix row/audited/missing counts remain **198 / 166 / 10**. Provenance defects remain **14 / 14**. Chart algorithm defects remain **0**. `DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED`.

## 8. Highest next gate

1. Continue lawful discovery for a source-emitted primary fulltext/page object for pp.121–129, prioritizing stable first-party/provider article records over guessed identifiers.
2. Search exact 1950-01-29 quotations that explicitly cite the 2008 serial page, while preserving derivative-vs-primary authority.
3. If primary pages are obtained, directly collate pp.121–129 and bind Jan-29 to its exact journal page without interpolation.
4. Resolve the exact 2007 facsimile volume-5 page/leaf and directly collate handwriting.
5. Search target/adjacent pages for 《铜壶漏箭制度》, 《准斋心制几漏图式》, 3482/3483, 03482/03483, the 1823 士礼居 fingerprint, or another stable item identifier.
6. Continue Gu Tinglong 1950-01-06, NLC [23]/[24], Ji Shuying chapter 9 and Gao Xizeng annotated-catalog routes in parallel.

Machine evidence: `docs/research/ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-PKU-FULLTEXT-BRIDGE-PUBLIC-ACCESS-BOUNDARY-R1.json`.
