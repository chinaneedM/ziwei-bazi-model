# Fusion Chart Historical Provenance Audit R1 — Batch 12GV

## 《百川归海，蔚为大观》p.335 跨正式出版物引文页锚

Status: **DPM 2010 PRINTED P.60 DIRECTLY REVIEWED / WENJI P.335 CITATION CLOSED / TAIWAN NCL 2015 PRINTED P.96 + BIBLIOGRAPHY P.102 DIRECTLY REVIEWED / AUTHOR-YEAR CITATION MAPS THE SAME JI STATEMENT TO BAICHUAN / P.335 BOUND TO BAICHUAN AT HIGH-CONFIDENCE CROSS-PUBLICATION CITATION LAYER / ORIGINAL 2004 P.335 NOT REVIEWED / ARTICLE START-END STILL UNRESOLVED / ZERO RUNTIME, MATRIX, GENEALOGY OR TARGET-TRANSFER CHANGE**

## 1. Why this is a real increment

Batches 12GS and 12GT established only structure: `《百川归海，蔚为大观》` is TOC item 74, but its exact pages could not be inferred from total extent.

Batch 12GV closes the first concrete numbered page anchor **inside** that article through two independent formal publications.

## 2. Palace Museum Journal 2010 control

Liu Qiang's official Palace Museum Journal page, printed p.60, directly shows Ji Shuying's statement about better-known Song editions in the Tianlu Linlang Hou-bian being transferred to Beijing Library.

Footnote 6 directly gives:

```text
冀淑英：《冀淑英文集》页335，北京图书馆出版社，2004年。
```

Therefore the statement is explicitly anchored to **Wenji p.335**.

This DPM footnote does not itself name the component article.

## 3. Taiwan National Central Library 2015 control

The 2015 `《國家圖書館館刊》` article `《臺灣現藏〈天祿琳琅〉遺書考述》` directly reproduces the same Ji statement on printed p.96 and attributes it to:

```text
冀淑英（2004）
```

The same article's printed p.102 bibliography expands that author-year item as:

```text
冀淑英（2004）。百川歸海，蔚為大觀。在冀淑英文集。
北京市：北京圖書館出版社。
```

Thus the article-level identity is explicit in the reference system of the independent 2015 publication.

## 4. Cross-publication adjudication

The evidence chain is:

```text
same Ji statement
  -> DPM 2010 footnote
     -> 《冀淑英文集》 p.335

same Ji statement
  -> Taiwan NCL 2015 author-year citation
     -> 冀淑英（2004）
     -> bibliography: 《百川归海，蔚为大观》
        in 《冀淑英文集》
```

Therefore:

```text
BAICHUAN_CONTAINS_WENJI_P335
  = HIGH_CONFIDENCE_CROSS_PUBLICATION_CITATION_BRIDGE

DIRECT_2004_P335_REVIEWED
  = false

P335_IS_ARTICLE_START
  = UNRESOLVED

P335_IS_ARTICLE_END
  = UNRESOLVED

BAICHUAN_EXACT_PAGE_RANGE
  = UNRESOLVED

PAGE_INTERPOLATION_FROM_P335
  = NOT_AUTHORIZED
```

The project still does not pretend that a citation bridge equals direct physical-page collation.

## 5. Relation to prior batches

- 12GP: formal Baichuan article identity remains closed.
- 12GS: TOC item 74 remains closed.
- 12GT: institutional 435-page extent and anti-interpolation firewall remain in force.
- 12GR: pp.383–385 remain an unauthorized Baichuan shortcut in Liu's Chen Qinghua citation context.

The new fact is narrower and stronger: **p.335 is a concrete page anchor within Baichuan at cross-publication citation level.**

## 6. Target-volume firewall

The p.335 statement concerns Tianlu Linlang collection transfer generally. It does not name:

- `《铜壶漏箭制度》`;
- `《准斋心制几漏图式》`;
- 3482 / 3483;
- 03482 / 03483.

No target purchase/donation route is selected.

## 7. Product / genealogy consequence

```text
NODES_ADDED=0
EDGES_ADDED=0
DIRECT_COPY_EDGE_AUTHORIZED=false
SAME_OBJECT_EDGE_AUTHORIZED=false
ACQUISITION_EDGE_AUTHORIZED=false
RUNTIME_RULE_CHANGE=false
ALGORITHM_REOPEN=false
CANDIDATE_COLLAPSE=false
MATRIX_COUNT_CHANGE=false
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Accounting remains `198 / 166 / 10`, provenance defects `14 / 14 repaired`, chart algorithm defects `0`.

## 8. Highest next gate

1. Search scholarly citations for additional explicit Baichuan page numbers bracketing p.335.
2. Directly inspect the 2004 volume p.335 and neighboring pages; determine item-74 start/end only from direct page evidence.
3. Continue final `《編后記》`, 2009 postscript, and 2010 `《〈冀淑英文集〉补遣》` discovery.
4. Continue direct 1997 `《北京图书馆馆史资料汇编（二）：1949—1966》` pp.446—449 collation.

Research record: `docs/research/ZIWEI-JI-SHUYING-BAICHUAN-P335-CROSS-PUBLICATION-CITATION-BRIDGE-R1.json`.
