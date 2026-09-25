# Fusion Chart Historical Provenance Audit R1 — Batch 12GQ

## 2010《文津学志》第三辑《〈冀淑英文集〉补遣》：正式篇章发现与正文未审边界

Status: **SUPPLEMENT ARTICLE FORMAL EXISTENCE CLOSED AT PUBLISHED TOC LEVEL / VOLUME IDENTITY CLOSED BY COMMERCIAL BIBLIOGRAPHIC OBJECT + CINII UNION-CATALOG CONTROL / ARTICLE AUTHOR + PAGE RANGE + BODY NOT RECOVERED / RELATION TO 《百川归海，蔚为大观》, 2004 EDITOR NOTE, OR 2009 《十五讲》 REMAINS UNRESOLVED / NO TEXTUAL-GENEALOGY EDGE / ZERO RUNTIME OR MATRIX CHANGE**

## 1. Why this is a material increment

Batch 12GP established that 冀淑英's `《百川归海，蔚为大观》` was formally published in the 2004 `《冀淑英文集》`, while the claimed 2004→2009 source genealogy remained only secondarily reported because neither the 2004 editor note nor the 2009 `《十五讲》` postscript had been directly reviewed.

A later formal corrective route now exists:

```text
《文津学志》第三辑
栏目：文献整理与版本研究
篇名：《〈冀淑英文集〉补遣》
出版年：2010
ISBN：9787501340859
```

The title itself shows that a published supplement/corrigendum-style article concerning `《冀淑英文集》` exists. This is a high-value discovery target because it postdates both the 2004 collection and the 2009 Fifteen Lectures.

The project has **not** recovered the article body, author, exact page span, abstract or notes. Therefore no content claim is inferred from the word `补遣`.

## 2. Sanmin published TOC control

Sanmin's public bibliographic/product page for `《文津学志 第三辑》` exposes:

- ISBN13: `9787501340859`;
- editor/compiled responsibility: `国家图书馆善本特藏部 编著`;
- publication date: `2010/05/25`;
- physical extent: `343页`;
- publisher string on that surface: `北京圖書館出版社`;
- TOC section: `文献整理与版本研究`;
- exact listed article title: `《冀淑英文集》補遣`.

This closes the article's **formal existence in the published table of contents**, not its author or content.

## 3. CiNii serial / ISBN control

CiNii Books serial record `BA65589403` for `《文津学誌》` independently exposes the series identity and includes ISBN `9787501340859` among the volume ISBNs. The record notes that volumes 3–12 use `国家图书馆出版社` as publisher.

The difference between the Sanmin publisher string and the CiNii publisher note is retained as source-layer metadata and is not silently normalized in this batch. It does not affect identification of the volume through the exact ISBN.

## 4. What is and is not closed

Closed:

```text
WENJIN_XUEZHI_V3_OBJECT
  = CLOSED_BY_ISBN_AND_SERIAL_CONTROLS

SUPPLEMENT_ARTICLE_FORMAL_EXISTENCE
  = CLOSED_AT_PUBLISHED_TOC_LEVEL

SUPPLEMENT_ARTICLE_EXACT_TITLE
  = 《冀淑英文集》补遣
```

Not closed:

```text
SUPPLEMENT_ARTICLE_AUTHOR
  = UNRESOLVED

SUPPLEMENT_ARTICLE_PAGE_RANGE
  = UNRESOLVED

SUPPLEMENT_ARTICLE_BODY
  = NOT_REVIEWED

MENTIONS_百川归海蔚为大观
  = UNRESOLVED

MENTIONS_2004_EDITOR_NOTE
  = UNRESOLVED

MENTIONS_2009_十五讲_OR_POSTSCRIPT
  = UNRESOLVED

CHANGES_2004_TO_2009_DERIVATION_ADJUDICATION
  = false
```

No inference is made that `补遣` means correction of the specific article `《百川归海，蔚为大观》`, or that it discusses the Tieqin acquisition narrative at all.

## 5. Relation to Batch 12GP

Batch 12GP remains unchanged:

- 2004 `《百川归海，蔚为大观》` formal article identity is closed;
- direct 2004 article text/page range is not reviewed;
- direct 2004 editor note is not reviewed;
- direct 2009 postscript is not reviewed;
- 2009 derivation from the 2004 article remains `SECONDARY_REPORTED_NOT_DIRECTLY_CLOSED`.

12GQ adds a new formal published object to inspect. It does not authorize a direct-copy or same-text edge.

## 6. Target-volume firewall

Nothing reviewed in this batch names or binds:

- `《铜壶漏箭制度》`;
- `《准斋心制几漏图式》`;
- 3482 / 3483;
- 03482 / 03483;
- the 1823 Huang Pilie / Shiliju one-volume fingerprint.

Therefore no target purchase, donation or other transfer route is selected.

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

1. Obtain or directly inspect `《文津学志》第三辑` `《〈冀淑英文集〉补遣》` and recover author, exact start/end pages, full text and footnotes.
2. Search the direct article for `百川归海`, `蔚为大观`, `录音`, `讲稿`, `授课`, `十五讲`, `后记`, `编者注`, `陈红彦`, `徐蜀`, `李文洁`.
3. Directly inspect the 2004 `《冀淑英文集》` editor note and the 2009 `《冀淑英古籍善本十五讲》` postscript; only then adjudicate the 2004→2009 textual genealogy.
4. Continue the parallel highest-priority archival route: direct `《北京图书馆馆史资料汇编（二）：1949—1966》` pp.446—449 collation.

Research record: `docs/research/ZIWEI-JI-SHUYING-WENJI-2010-SUPPLEMENT-ARTICLE-DISCOVERY-BOUNDARY-R1.json`.
