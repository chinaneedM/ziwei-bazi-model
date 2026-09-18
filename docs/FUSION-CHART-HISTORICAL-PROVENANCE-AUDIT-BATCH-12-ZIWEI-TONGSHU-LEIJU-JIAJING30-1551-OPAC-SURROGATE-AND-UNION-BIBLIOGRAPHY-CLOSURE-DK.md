# Batch 12DK — 嘉靖三十年（1551）《通書類聚尅擇大全》OPAC、公開替代本、縮微目錄與聯合書目路線閉合

## Status

```text
TARGET=通書類聚尅擇大全
NLC_OPAC_DOC_NUMBER=001790345
NLC_INTERNAL_ID=411999023866
CALL_NUMBER=14202
HOLDING=南区善本阅览室
PUBLIC_COMMONS_TARGET_SURROGATE=NOT_FOUND_IN_REVIEWED_SEARCH_INDEX
PUBLIC_IA_IDENTIFIER_SURROGATE=NOT_FOUND
OLCC_B1MICU_ANONYMOUS_QUERY=AUTHENTICATION_BLOCKED
GOOGLE_BOOKS_MICROFORM_CATALOG_SEARCHABLE=false
CURRENT_CENSUS_SECOND_HOLDING=NOT_FOUND_IN_REVIEWED_VARIANTS
UNION_BIBLIOGRAPHY_FUZZY_SET=48/48_PAGES_576/576_RECORDS_VALIDATED
UNION_TARGET_OR_VARIANT_COPY=0
DIRECT_JUAN16_19_PAGE=NOT_OBTAINED
TARGET_FINGERPRINT=UNRESOLVED
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NO
```

## 1. Why this follows 12DJ

12DJ closed the 1551 physical holding and the NLC Digital Ancient Books public-index boundary, but intentionally left open whether another NLC route, microform record, public surrogate, or second institutional copy could expose the surviving juan 16–19.

12DK follows those access and holding routes to their current evidence boundary. It is **not** a target-table collation batch: no body-text page from juan 16–19 has yet been acquired.

## 2. NLC OPAC strengthens physical-copy identity

The NLC OPAC title record directly binds:

```text
TITLE=通書類聚尅擇大全 [善本] : □□卷
FORMAT=活字印本, 銅活字
IMPRINT=芝城, 明嘉靖30年[1551]
EXTENT=1冊
DOC_NUMBER=001790345
INTERNAL_ID=411999023866
CALL_NUMBER=14202
SUBLIBRARY=南区善本阅览室
```

The source-generated session-bearing `item-global` link was followed successfully. The item page directly prints:

```text
14202\南区善本阅览室
```

and its client-side rare-book handling rule converts the generic unavailable message for South Rare Books holdings into:

```text
请到总馆南区善本阅览室办理相关阅览手续。
```

The page also contains a **generic** service note saying a preservation copy is provided only when no circulation/reading/base copy or other-format holding such as electronic or microform exists. That service rule does **not** prove this specific title has an electronic or microform copy.

Evidence:

```text
RUN=35375192286
ARTIFACT=10560310067
DIGEST=sha256:7e38443823690329ea4a8d05fdeeb1d35f40ad74238260e9c5e43f46ffd0308f
```

## 3. Public surrogate discovery

A second workflow followed the live OPAC session item route and queried public surrogate indexes with the internal object identity:

```text
411999023866
NLC892-411999023866
通書類聚尅擇大全
通書類聚抉擇大全
通书类聚克择大全
```

Wikimedia Commons returned zero for all five source-search queries.

Internet Archive returned zero for both identifier queries. Title searches returned unrelated newspapers/other objects rather than a matching book object. The title route is therefore discovery-only, not a world-wide negative.

```text
RUN=35375499098
ARTIFACT=10559648198
DIGEST=sha256:f23451fc509c109db84fbe670ba07f8c48295f1763f11e76e144189de22af7ee
```

No public direct-page surrogate was found in these reviewed routes.

## 4. OLCC microform logical database: authentication boundary

The National Library Union Cataloging Center exposes the UTF-8 microform logical database `B1MICU` over Z39.50.

The target accepted a protocol connection, but anonymous search attempts ended with:

```text
Access-control failure
Aleph error. Service: C9902. Code: 1.
User name Z39 does not exist.
```

Some client output displayed `Number of hits: 0` before the access-control failure. Those numbers are explicitly **invalid as content-negative evidence** because the search was not authorized.

```text
RUN=35376261851
ARTIFACT=10560661850
DIGEST=sha256:519a21db7bf1e03269b53d2a64e6b7f94fbbe2f8e9c6f67b7da1688c6e5ca044
```

Therefore:

```text
MICROFORM_CATALOG_TARGET_PRESENCE=UNRESOLVED
ANONYMOUS_Z3950_ROUTE=AUTHENTICATION_BLOCKED
```

## 5. Published 2015 microform union catalog control

Google Books exposes a record for the 2015 `《全国公共图书馆缩微文献联合目录·古籍编》` volume route, including known volume id `K1wpxAEACAAJ`.

All tested SearchWithinVolume2 queries returned:

```text
searchable=false
```

Therefore zero result arrays have no negative authority.

```text
RUN=35376706700
ARTIFACT=10559549808
DIGEST=sha256:fe58f6abadb991f9a9d7ac064145b7e1667436ca2a0b2589e7deb9ad65dd3ba2
```

The microform question remains open to authenticated OLCC access, a searchable copy of the union catalog, or direct NLC service confirmation.

## 6. National Ancient Books Census broad-variant control

Controlled broad searches were run against the current public census database.

Direct source HTML gives:

```text
QUERY=通書類聚
RETURNED=1
TARGET=110000-0101-0013797 / 14202 / 國家圖書館

QUERY=通书类聚
RETURNED=1
SAME_TARGET=true

QUERY=芝城銅活字
RETURNED=2
  110000-0101-0004638 / 墨子十五卷 / 1552芝城銅活字藍印本 / 國家圖書館
  110000-0101-0013797 / 通書類聚尅擇大全 / 1551芝城銅活字印本 / 國家圖書館

QUERY=姚奎
RETURNED=0

QUERY=王以寧
RETURNED=1
TARGET=false
RETURNED_TITLE=西臺疏草...（明）王以寧撰
HOLDER=浙江圖書館
```

Evidence:

```text
RUN=35376977033
ARTIFACT=10561285274
DIGEST=sha256:50763fdee7b299228182e6b80ac9179d0cb893d73fd32c8f95c7e9cd3e05c162
```

Thus the reviewed current census variants do not directly support a second target copy at Fujian Provincial Library. A historical holding, transferred copy, differently catalogued object, or non-census copy remains possible; the secondary Fujian-holding statement is not promoted to current-holding fact.

## 7. Chinese Ancient Books Union Bibliography: exact and exhaustive fuzzy closure

Resource index `0019` exact-title queries returned zero for:

```text
通書類聚尅擇大全
通書類聚尅擇大全□□卷
通書類聚抉擇大全
通书类聚克择大全
```

The broad source query:

```text
title LIKE 通書類聚
```

returned:

```text
TOTAL=576
PAGE_SIZE=12
PAGES=48
```

Evidence was not accepted until all 48 pages were physically retrieved and validated.

Initial acquisition:

```text
RUN=35377985520
ARTIFACT=10560996782
DIGEST=sha256:a8a5b3a46d03766382c0c9624874e02225829b04cd6a966e3ce6931f2306e68b
VALIDATED_PAGES=15
TIMED_OUT_PAGES=33
```

Bounded retry:

```text
RUN=35379079830
ARTIFACT=10560957890
DIGEST=sha256:93b2f5dfde12d5b333fa5ceaf64a5cdf260ea514253727c70fb80d94e3f1331e
RECOVERED=32/33
STILL_MISSING=PAGE_38
```

Final page:

```text
RUN=35379372970
ARTIFACT=10561901955
DIGEST=sha256:6e14984cb189c17f6b8aa9f326e47026aa9ede6a5dc7894e016a07aa6f9c54a5
PAGE_38_VALID=true
ATTEMPTS_REQUIRED=1
```

Merged and de-duplicated result:

```text
VALIDATED_PAGES=48/48
UNIQUE_RECORDS=576/576
CONTIGUOUS 通書類聚/通书类聚 TITLE HITS=0
尅擇/克擇/抉擇 TERM HITS=0
姚奎 HITS=0
王以寧/王以宁 HITS=0
芝城 HITS=0
ROMANIZED TARGET TITLE HITS=0
ROMANIZED YAO KUI HITS=0
ROMANIZED WANG YINING HITS=0
```

Only one exact 1551 / Jiajing-30 record occurs in the 576 rows:

```text
IDENTIFIER=NJPX96-B51
TITLE=新刊批點古文類抄 / 新刊古文類抄
DATE=明嘉靖辛亥 [30年, 1551]
TARGET=false
```

Therefore this complete indexed fuzzy result set contains no target or independent copy.

This is a search-scope negative only; it cannot prove no uncatalogued/private/historical copy exists.

## 8. Genealogy consequence

12DK strengthens only the provenance/access metadata of:

```text
PHYSICAL-COPY-TONGSHU-LEIJU-NLC-JIAJING30-1551-V16-19
```

It adds no positive textual or numeric transmission edge.

The existing unresolved firewalls remain:

```text
1551_TONGSHU_LEIJU DIRECT_TARGET_FINGERPRINT_ATTESTATION SANMING_1578 = UNRESOLVED
1551_TONGSHU_LEIJU DIRECT_TARGET_FINGERPRINT_ATTESTATION YUELING_1589 = UNRESOLVED
```

No target page means no table-family vote.

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

1. do not repeat the now-closed Commons/IA identifier route, NLC Digital Ancient Books exact-title/sbnumber route, or the complete 576-record Union Bibliography fuzzy result set unless those indexes change;
2. resolve `B1MICU` only through authorized catalog access, a searchable/physical copy of the 2015 microform union catalog, or direct NLC service confirmation;
3. prioritize lawful South Rare Books Reading Room / reproduction-service access to call no. `14202`, or locate an independently accessible physical/reproduction copy outside the reviewed current NLC public indexes;
4. continue in parallel the pre-1578 exact-fingerprint Tongshu/almanac search, Chinese Nanjing/Datong 59/41 carrier search, and exact whole-ke threshold/selection-rule reconstruction.

Research record: `docs/research/ZIWEI-TONGSHU-LEIJU-JIAJING30-1551-OPAC-SURROGATE-AND-UNION-BIBLIOGRAPHY-CLOSURE-R1.json`.
