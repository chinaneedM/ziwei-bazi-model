# Fusion Chart Historical Provenance Audit R1 — Batch 12GN

## 《北京图书馆馆史资料汇编（二）》pp.446—449：国图官方引文桥接与东京都立馆藏访问路线

Status: **NLC-HOSTED 2024 SCHOLARLY CITATION BINDS PP.446—449 TO A TIEQIN-TRANSFER BEIJING-LIBRARY INTAKE QUOTATION / TOKYO METROPOLITAN PUBLIC CATALOG CLOSES A PHYSICAL UPPER-VOLUME HOLDING ROUTE / DIRECT PP.446—449 IMAGES OR FULL TEXT NOT REVIEWED / INTERNAL DOCUMENT TITLE + EXACT TARGET 3482/3483 STATUS UNRESOLVED / ZERO GENEALOGY OR RUNTIME CHANGE**

## 1. Why this batch is an actual increment

Batch 12FP identified `《北京图书馆馆史资料汇编（二）：1946—1966》` pp.446—449 as a high-priority direct-source target, but the project had not bound those pages to a specific quotation from an authoritative public surface.

A 2024 article hosted by the National Library of China / 中国古籍保护网 now supplies that missing citation bridge. In its discussion of the early PRC Tieqin Tongjian Lou transfer, the article first states that, after Zheng Zhenduo's mobilization, Qu-family rare books were transferred to the government, citing Liu Chenggan's diary as reference [22]. It then quotes:

```text
这些善本入藏本馆，本馆中文书藏地位将益形重要，可为全国之冠
```

and places reference [23] immediately after that quotation:

```text
北京图书馆馆史资料汇编(二)编辑委员会.
北京图书馆馆史资料汇编二：1946—1966.
北京：北京图书馆出版社，1997：446—449.
```

Therefore the repository can now close a **modern NLC-hosted citation-layer binding** between the Tieqin intake discussion / quoted Beijing-Library voice and the pp.446—449 range.

This is not direct collation of pp.446—449.

## 2. Source-layer separation

The evidence layers are kept distinct:

```text
NLC_HOSTED_2024_ARTICLE
  authors = 蔡成普 / 李静
  role    = modern scholarly citation bridge

REFERENCE_22
  source  = 刘承幹《求恕斋日记16》pp.321—322
  role    = supports the article's preceding "让归政府" sentence

REFERENCE_23
  source  = 《北京图书馆馆史资料汇编（二）：1946—1966》pp.446—449
  role    = cited immediately after the quoted Beijing-Library intake assessment

DIRECT_1997_PAGES
  project review = NOT YET PERFORMED
```

The project must not collapse [22] and [23], or promote the modern article into the direct 1997 page text.

## 3. What the NLC-hosted article closes

Closed at the **modern institutional scholarly citation** layer:

- the 2024 article is hosted by the National Library of China / 中国古籍保护网;
- its section 3.1 discusses Zheng Zhenduo's mobilization of the Changshu Qu family / Tieqin Tongjian Lou transfer;
- the Beijing-Library intake quotation above is directly followed by reference [23];
- reference [23] identifies the exact 1997 work and pp.446—449.

Adjudication:

```text
PP446_449_TIEQIN_CONTEXT_CITATION_BRIDGE
  = CLOSED_AT_NLC_HOSTED_MODERN_SCHOLARLY_LAYER

PP446_449_DIRECT_PAGE_COLLATION
  = NOT_REVIEWED
```

## 4. Tokyo Metropolitan lawful physical-holding route

Tokyo Metropolitan Library's public Digital BookShelf exposes the exact upper volume:

```text
北京图书馆馆史资料汇编(二) : 上册
北京图书馆馆史资料汇编(二)编辑委员会编
北京圖書館出版社
1997.8
displayed shelf sequence: 0161 / 1 / 2-1
```

The same public shelf browser also exposes the lower volume at `0161 / 1 / 2-2`.

This closes a concrete physical-holding discovery route for the upper volume that contains pp.446—449. The public shelf browser does not expose those page images.

The project has not submitted a copying request, incurred a fee, or claimed user-specific eligibility.

## 5. Target-volume firewall

The target remains the single 1823 Huang Pilie/Shiliju bound manuscript containing:

- `《铜壶漏箭制度》` — historical catalog no. 3482;
- `《准斋心制几漏图式》` — historical catalog no. 3483;
- current public identifiers 03482 / 03483 in the already audited NLC route.

Neither the 2024 NLC-hosted article nor the Tokyo shelf browser names those titles or identifiers.

Direct pp.446—449 remain unreviewed. Therefore:

```text
TARGET_3482_3483_NAMED_IN_DIRECT_PP446_449
  = UNRESOLVED_NOT_REVIEWED

TARGET_SPECIFIC_PURCHASE_ROUTE_SELECTED
  = false

TARGET_SPECIFIC_DONATION_ROUTE_SELECTED
  = false
```

The existing firewall remains active:

```text
MISSING_瞿捐 != SALE
COLLECTION_LEVEL_PURCHASE != TARGET_PURCHASE
COLLECTION_LEVEL_DONATION != TARGET_DONATION
MODERN_CITATION_BRIDGE != DIRECT_1997_PAGE_TEXT
```

## 6. Relation to Batch 12GM

Targeted public searches for Lin Zhenyue's 2024 report title and variants still did not recover an abstract, slides, handout, proceedings text, report body, or source list.

12GN therefore does **not** claim that the 1997 pp.446—449 were Lin's "new materials", and does not claim that the report used Gao Xizeng's annotated Tieqin catalog.

It advances a parallel high-priority direct-record route while preserving 12GM's source-basis uncertainty.

## 7. Product / genealogy consequence

```text
NODES_ADDED=0
EDGES_ADDED=0
ACQUISITION_EDGE_AUTHORIZED=false
SAME_OBJECT_EDGE_AUTHORIZED=false
DIRECT_SANMING_PARENT_VOTE_INCREMENT=0
MATRIX_ROW_COUNT_CHANGE=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Accounting remains:

```text
Matrix rows / audited / missing = 198 / 166 / 10
provenance defects repaired     = 14 / 14
chart algorithm defects         = 0
```

## 8. Highest next gate

1. Lawfully obtain or inspect the exact `《北京图书馆馆史资料汇编（二）》上册` pp.446—449, using NLC, Tokyo Metropolitan Library, or another legitimate holding.
2. Directly identify the internal document(s) reproduced on those pages: title, date, issuing office/person, quotation boundaries, transfer terms, batch counts, and any accession/catalog identifiers.
3. Search every directly reviewed line for `铜壶漏箭制度`, `准斋心制几漏图式`, 3482/3483, 03482/03483, or the 1823 Huang/Shiliju one-volume fingerprint.
4. Keep Lin Zhenyue 2024 report-source recovery, Ji Shuying chapter 9, Song Yunbin 1950-02-11, and Deng Zhicheng 1950-01-29 active in parallel.
5. Do not select purchase/sale versus donation for the target bound volume without direct or near-direct item-level evidence.

Research record: `docs/research/ZIWEI-NLC-PP446-449-TIEQIN-CITATION-BRIDGE-AND-TOKYO-HOLDING-R1.json`.
