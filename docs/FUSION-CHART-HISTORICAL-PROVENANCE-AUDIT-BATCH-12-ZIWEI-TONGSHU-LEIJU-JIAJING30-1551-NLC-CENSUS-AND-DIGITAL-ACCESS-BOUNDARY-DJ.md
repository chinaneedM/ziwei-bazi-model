# Batch 12DJ — 嘉靖三十年（1551）《通書類聚尅擇大全》國圖普查館藏閉合與公開數字路線邊界

## Status

```text
CENSUS_ID=110000-0101-0013797
CALL_NUMBER=14202
TITLE=通書類聚尅擇大全□□卷
EDITION=明嘉靖三十年（1551）芝城銅活字印本
HOLDER=國家圖書館
PHYSICAL_QUANTITY=1册
SURVIVING_SCOPE=存四卷（十六至十九）
PRE1578_PHYSICAL_HOLDING_IDENTITY=CATALOG_BOUND
NLC_DIGITAL_ANCIENT_BOOKS_EXACT_TITLE_HIT=0
NLC_DIGITAL_ANCIENT_BOOKS_SBNUMBER_14202_HIT=0
PUBLIC_DIGITAL_INDEX_ROUTE=CLOSED_NO_TARGET_RECORD_OBSERVED
PHYSICAL_COPY_DIGITIZATION_STATUS=UNRESOLVED
DIRECT_TARGET_PAGE_OBTAINED=NO
TARGET_FINGERPRINT_ADJUDICATION=UNRESOLVED
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NO
```

## 1. Why this follows 12DI

12DI excluded another securely pre-1578 Tongshu branch: the 1554 LOC `《新刊類編陰陽選擇合併通書大全》` preserves the ordinary coarse 40/60 family rather than the exact 1578 Sanming / 1589 Yueling fingerprint.

The next high-value question was therefore not another re-read of the same branch, but whether a **different pre-1578 Tongshu title** could be tied to a surviving physical copy and then opened for direct page-level testing.

A live remote work unit had already located a 1551 bibliography entry. Batch 12DJ closes that bibliographic identity and access boundary without converting catalog metadata into a textual claim.

## 2. 《中國古籍善本書目》 direct catalog control

The source-bound high-resolution catalog workflow fixes:

```text
SOURCE=中國古籍善本書目 子部 三
SOURCE_PDF_SHA256=e562a7af9c9aac5daf641172110133f8f203cebeb1ebcd1bad4fd515979cf2ab
PDF_PAGE=48
CATALOG_ITEM=四五〇 / 450
DIRECT_PAGE_SHA256=1c1a05e8db798c6c8b6995d0629c30934f17a0463ae96a87b8cedb2951ae07d4
EDITION=明嘉靖三十年芝城銅活字印本
SURVIVING_SCOPE=十六至十九
OCR_USED=false
```

Workflow:

```text
RUN=35370570700
ARTIFACT=10558651831
DIGEST=sha256:80ec57b1d53533471f9990ecae67dfe2a3d1c5a1e5be598eff2871ad6d003814
```

This corrects the exploratory locator error that had temporarily called the target item 451. The target is item **450**; item 451 belongs to the following bibliography entry. Because that mistake was never promoted into the formal Matrix/Registry/Graph, the formal provenance-defect counter remains unchanged.

## 3. National Ancient Books Census direct holding record

The official `全國古籍普查登記基本數據庫` source HTML returned one exact traditional-title record. Direct fields are:

```text
普查編號=110000-0101-0013797
索書號=14202
題名=通書類聚尅擇大全□□卷
版本=明嘉靖三十年（1551）芝城銅活字印本
册（件）数=1册
单位=國家圖書館
存卷=存四卷（十六至十九）
```

Workflow:

```text
RUN=35371456818
ARTIFACT=10558264237
DIGEST=sha256:a134e16ee70a029540b936d1064db1634137045acc8bf9c217c5d3d22bc08ab9
```

Therefore the project now has a first-party national-census binding for a distinct pre-1578 Tongshu physical holding.

This closes **physical holding identity**, not body text. No leaf from juan 16-19 has yet been directly acquired in this batch.

## 4. NLC Digital Ancient Books advanced-search contract

The current NLC advanced-search page exposes the Digital Ancient Books resource as:

```text
RESOURCE_INDEX=0003
ENDPOINT=/advanceSearch/gujiSearch/data
FIELDS:
  title=标题
  author=责任者
  publish_unit=出版者
  publish_time=出版发行项
  sbnumber=善本书号
MATCH:
  must=精确
  like=模糊
```

This makes identifier-level access testing possible without relying on generic web search snippets.

## 5. Exact-title checks

Controlled exact queries returned:

```text
title must 通書類聚尅擇大全       -> total=0
title must 通書類聚尅擇大全□□卷 -> total=0
title must 通书类聚克择大全       -> total=0
```

Workflow:

```text
RUN=35372409456
ARTIFACT=10558009027
DIGEST=sha256:f237b420df568069173108c4113ad9ab6ee0c2292614319c6dcd8e7715cb6b0c
```

The fuzzy title endpoint is intentionally **not** used as negative evidence: it tokenizes the query and returns thousands of unrelated records.

## 6. Compound controls and a live positive control

The field-level compound workflow confirms that the Digital Ancient Books index is live and can return a 1551 Tongshu record under controlled fields.

For example:

```text
publish_time must 明嘉靖30年[1551]
AND title like 大全
-> total=2
```

One returned record is the already audited 1551 Leibian object:

```text
TITLE=類編曆法通書大全
IDENTIFIER=411999026677
SBNUMBER=15897
PUBLISH_TIME=明嘉靖30年[1551]
```

Thus the target's non-return cannot be attributed to a globally broken resource index.

Workflow:

```text
RUN=35373080523
ARTIFACT=10558119833
DIGEST=sha256:1c511b60c4f6c548f9e6ffb7a193a54ec85bde93f65e41bae6889120e8865238
```

Broad fuzzy author/publisher results are not promoted into identity claims.

## 7. Strong identifier-level check: 14202

Because the advanced-search contract exposes `sbnumber=善本书号`, the NLC holding number `14202` was tested directly:

```text
sbnumber must 14202                                      -> total=0
sbnumber must 14202 AND publish_time must 明嘉靖30年[1551] -> total=0
sbnumber must 14202 AND title like 通書                   -> total=0
```

Workflow:

```text
RUN=35373229704
ARTIFACT=10559121597
DIGEST=sha256:59e814eaa0f522bca7b1cda797ec3b6b0ac4defc74d26cebcf6949da8ebd67b4
```

This is strong enough to close the **current public Digital Ancient Books index route** for the exact copy.

It is **not** strong enough to claim any of the following:

```text
THE_PHYSICAL_COPY_IS_NOT_DIGITIZED
NO_READER_TERMINAL_OR_INTERNAL_IMAGE_EXISTS
NO_REPRODUCTION_OR_MICROFILM_ROUTE_EXISTS
NO_OTHER_PUBLIC_SURROGATE_EXISTS
THE_TARGET_TABLE_IS_ABSENT
```

All remain unresolved unless separately evidenced.

## 8. Target-table and genealogy consequence

At present:

```text
1551_TONGSHU_LEIJU_PHYSICAL_HOLDING=CONFIRMED_AT_CENSUS_CATALOG_LEVEL
JUAN_16_19_DIRECT_PAGE_COLLATION=NOT_YET_OBTAINED
TABLE_FAMILY=UNRESOLVED
SANMING_EXACT_FINGERPRINT_TEST=NOT_PERFORMED
YUELING_GENERIC_TONGSHU_IDENTITY=UNRESOLVED
```

The genealogy graph therefore gains a physical-copy node, but **no positive table-transmission edge**.

The following remain explicitly unresolved:

```text
1551_TONGSHU_LEIJU DIRECT_TARGET_FINGERPRINT_ATTESTATION SANMING_1578
1551_TONGSHU_LEIJU DIRECT_TARGET_FINGERPRINT_ATTESTATION YUELING_1589
```

Same title family, suitable chronology and surviving physical copy do not prove textual identity or lineage.

## 9. Product adjudication

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
HPA_ZDATE_006=MISSING_FROM_PRODUCT
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=12
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=12
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

No runtime candidate, winner, collapse, or algorithm reopen is authorized.

## 10. Next gate

Priority is now more concrete:

1. obtain a lawful direct image/reproduction/reader-access route for NLC census `110000-0101-0013797`, call no. `14202`, juan 16-19;
2. directly locate any seasonal day/night-ke or change-day table before judging the 1551 copy against the Sanming/Yueling fingerprint;
3. if this physical-copy route remains inaccessible, search independent copies/recensions of `《通書類聚尅擇大全》` rather than treating the current public-index non-return as textual evidence;
4. continue in parallel the Chinese pre-1578 Nanjing/Datong 59/41 carrier and whole-ke threshold/selection-rule searches.

Research record: `docs/research/ZIWEI-TONGSHU-LEIJU-JIAJING30-1551-NLC-CENSUS-AND-DIGITAL-ACCESS-BOUNDARY-R1.json`.
