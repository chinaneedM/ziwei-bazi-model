# Fusion Chart Historical Provenance Audit R1 — Batch 12FM

## 高熙曾批校《鐵琴銅劍樓藏書目錄》現藏／訪問邊界

Status: **ANNOTATED TIEQIN CATALOG EXISTENCE ATTESTED BY 2026 BIBLIOGRAPHIC SURVEY / BROADER GAO MANUSCRIPT SURVIVAL CLOSED AT MODERN EDITORIAL-CHAIN LEVEL / EXACT HOLDING + SHELFMARK + PUBLIC SURROGATE UNRESOLVED / TARGET 3482-3483 ANNOTATION NOT REVIEWED / ZERO ACQUISITION-ROUTE SELECTION / ZERO GENEALOGY OR RUNTIME CHANGE**

## 1. Question

Batch 12FL closed only the collection-level fact that the Qu-family Tieqin Tongjian Lou transfer into Beijing Library used both donation and priced acquisition/sale mechanisms. It deliberately left the target bound volume's exact route unresolved.

The best next source lead was the reported Gao Xizeng annotated copy of 《鐵琴銅劍樓藏書目錄》.

12FM asks:

> Can the present holder, shelfmark, lawful public surrogate, or the target 3482/3483 annotations of that exact annotated catalog now be closed?

Answer: **No.**

What can be closed is narrower but useful: modern bibliographic literature attests the annotated catalog's existence and research value; independent modern publication evidence shows that other Gao Xizeng manuscripts survived into a family/editor/academic research chain. The exact annotated Tieqin catalog is not yet bound to any present institution or private holder.

## 2. Existence attestation

A 2026 publication discussion for Tang Zhibo and Zhao Yingjie's 《中國分省公藏古籍書目總錄（1949—2024）》 states that Gao Xizeng accompanied Zhao Wanli in collecting Qu-family books and left an annotated 《鐵琴銅劍樓藏書目錄》 with detailed annotations on books he handled.

Public discussion:

```text
https://www.sohu.com/a/1011488146_121124384
```

Underlying work:

```text
湯志波、趙穎潔編
《中國分省公藏古籍書目總錄（1949—2024）》
上海辭書出版社，2026
ISBN 9787532664252
```

This closes only:

```text
GAO_ANNOTATED_TIEQIN_CATALOG_EXISTENCE
  = ATTESTED_BY_2026_BIBLIOGRAPHIC_SURVEY_DISCUSSION

GAO_ANNOTATION_CONTENT_SCOPE
  = BOOKS_HANDLED_DURING_QU_COLLECTION_WORK
```

The public discussion does not name the current holder, shelfmark, reproduction, or the target 3482/3483 annotation.

## 3. Independent evidence that Gao manuscript materials survived

### 3.1 《高熙曾學術文存》

Zhao Lintao's 2022 edited volume 《高熙曾學術文存：中國古代文學經典講義》 states that some included materials were organized from Gao manuscripts. The first preface is by Gao's daughter Gao Tingting and records Gao's 1950 move into Beijing Library rare-books work under Zhao Wanli, where he left many valuable records.

Bibliographic / preview controls:

```text
https://search.megbook.com.hk/mall/detail.jsp?proID=3791857
https://www.airitibooks.com/Publication/Details?publicationID=P20240308094
```

This authorizes:

```text
BROADER_GAO_MANUSCRIPT_SURVIVAL
  = CLOSED_AT_MODERN_EDITORIAL_CHAIN_LEVEL
```

It does **not** authorize:

```text
TARGET_TIEQIN_CATALOG_IN_FAMILY_CUSTODY = false / not proved
TARGET_TIEQIN_CATALOG_AT_HEBEI_UNIVERSITY = false / not proved
TARGET_TIEQIN_CATALOG_AT_NLC = false / not proved
```

### 3.2 Gao bibliographical manuscript research chain

The 2020 《燕趙文化研究（第3輯）》 table of contents includes:

```text
秦俊澤《高熙曾〈版本瑣記遺稿〉整理與研究》
```

Bibliographic control:

```text
https://www.megbook.com.tw/mall/detail.jsp?proID=3559785
```

This closes the existence of a modern research/publication chain for another Gao bibliographical manuscript. It does not establish the custody of the annotated Tieqin catalog.

## 4. Current institutional discovery path

Official Hebei University pages place Zhao Lintao within the university's current institutional research/administrative network. This makes the Gao-family/editorial chain a concrete discovery path rather than a speculative name search.

Controls:

```text
https://manage.hbu.edu.cn/jgsz/gltd.htm
https://www.hbu.edu.cn/info/1094/22368.htm
```

But institutional affiliation is not custody evidence.

Therefore:

```text
HEBEI_UNIVERSITY_EDITORIAL_CONNECTION
  !=
HEBEI_UNIVERSITY_HOLDING
```

Likewise Gao's former Beijing Library employment is not proof that the annotated copy stayed at NLC.

## 5. Reviewed public-search boundary

12FM searched the currently accessible indexed web surface for:

- exact title + Gao Xizeng;
- NLC-indexed references;
- Hebei University domain traces;
- Qin Junze's 《版本瑣記遺稿》 research;
- Zhao Lintao + Gao manuscript relationships.

No reviewed public result supplied:

```text
EXACT_CURRENT_HOLDER
EXACT_SHELFMARK
LAWFUL_PUBLIC_DIGITAL_SURROGATE
TARGET_3482_3483_ANNOTATION
```

This is a bounded negative only:

```text
NOT_LOCATED_ON_REVIEWED_PUBLIC_WEB_INDEXES
!=
LOST
!=
NONEXISTENT
!=
PRIVATE_CUSTODY
```

## 6. Adjudication

```text
GAO_ANNOTATED_TIEQIN_CATALOG_EXISTENCE
  = ATTESTED_BY_2026_BIBLIOGRAPHIC_SURVEY_DISCUSSION

BROADER_GAO_MANUSCRIPT_SURVIVAL
  = CLOSED_AT_MODERN_EDITORIAL_CHAIN_LEVEL

GAO_BIBLIOGRAPHICAL_MANUSCRIPT_RESEARCH_CHAIN
  = CLOSED_FOR_OTHER_VERSION_NOTES_MANUSCRIPT_PUBLICATION

TARGET_ANNOTATED_TIEQIN_CATALOG_CURRENT_HOLDING
  = UNRESOLVED

TARGET_ANNOTATED_TIEQIN_CATALOG_SHELFMARK
  = UNRESOLVED

TARGET_ANNOTATED_TIEQIN_CATALOG_PUBLIC_SURROGATE
  = UNRESOLVED

TARGET_3482_3483_ANNOTATION
  = NOT_REVIEWED

TARGET_TRANSACTION_MODE
  = UNRESOLVED
```

Custody selection remains all false:

```text
FAMILY_CUSTODY_SELECTED=false
HEBEI_UNIVERSITY_CUSTODY_SELECTED=false
NLC_CUSTODY_SELECTED=false
OTHER_CUSTODY_SELECTED=false
```

## 7. Firewalls

Do not make any of these substitutions:

```text
SURVIVING_OTHER_GAO_MANUSCRIPTS
  != SAME_CUSTODY_AS_TARGET_CATALOG

HEBEI_UNIVERSITY_EDITORIAL_CONNECTION
  != HEBEI_UNIVERSITY_HOLDING

GAO_BEIJING_LIBRARY_EMPLOYMENT
  != NLC_HOLDING

NO_PUBLIC_HOLDING_RECORD_FOUND
  != LOST
```

No donation/sale/purchase route is selected.

## 8. Transmission and product consequence

12FM is an access/provenance-discovery boundary only.

```text
NODES_ADDED=0
EDGES_ADDED=0
ACQUISITION_EDGE_AUTHORIZED=false
SAME_OBJECT_EDGE_AUTHORIZED=false
DIRECT_SANMING_PARENT_VOTE_INCREMENT=0
PRE1578_ZHUNZHAI_RULE_WITNESS_INCREMENT=0
MATRIX_ROW_COUNT_CHANGE=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Accounting remains:

```text
Matrix rows / audited / missing = 198 / 166 / 10
provenance defects repaired     = 13 / 13
chart algorithm defects         = 0
```

## 9. Next gate

Prioritized discovery path:

1. recover the source/citation context behind Tang/Zhao's 2026 statement about Gao's annotated Tieqin catalog, ideally identifying present holder or reproduction;
2. inspect Qin Junze's 2020 《高熙曾〈版本瑣記遺稿〉整理與研究》 for explicit manuscript-provenance/custody notes;
3. trace the Gao-family / Zhao Lintao editorial-manuscript chain only as a discovery path, never as a custody inference;
4. search NLC ancient-books / historical acquisition work papers for the Gao annotated catalog or target-level transaction annotations;
5. do not select a target donation/sale route until catalog nos. 3482/3483 or the bound volume is tied to direct or near-direct transaction evidence;
6. keep Batch 12FK's public pre-permission access boundary unchanged.

Research record: `docs/research/ZIWEI-GAO-XIZENG-ANNOTATED-TIEQIN-CATALOG-HOLDING-AND-ACCESS-BOUNDARY-R1.json`.
