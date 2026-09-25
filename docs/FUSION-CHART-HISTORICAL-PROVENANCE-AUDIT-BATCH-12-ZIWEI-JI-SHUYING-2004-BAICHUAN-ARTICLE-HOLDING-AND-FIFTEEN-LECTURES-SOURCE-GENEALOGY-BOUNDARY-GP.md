# Fusion Chart Historical Provenance Audit R1 — Batch 12GP

## 冀淑英 2004《百川归海，蔚为大观》：正式篇章、实体馆藏与 2009《十五讲》来源谱系边界

Status: **2004 ARTICLE IDENTITY CLOSED BY TWO INDEPENDENT LIBRARY/INSTITUTIONAL PUBLICATIONS / TOKYO PHYSICAL HOLDING ROUTE FOR 《冀淑英文集》 CLOSED / 2009 《十五讲》 BIBLIOGRAPHIC IDENTITY ALREADY CLOSED / DIRECT 2004 ARTICLE TEXT + PAGE RANGE NOT REVIEWED / 2009↔2004 DERIVATION REMAINS SECONDARY-REPORTED PENDING DIRECT POSTSCRIPT/EDITOR-NOTE COLLATION / TARGET 3482/3483 TRANSFER MODE UNRESOLVED / ZERO RUNTIME OR GENEALOGY EDGE CHANGE**

## 1. Why this route matters

Batch 12FP/12GL established the 2009 book `《冀淑英古籍善本十五讲》` and its ninth lecture `《铁琴铜剑楼藏书的收购入藏》`, but full chapter 9 has not been directly reviewed.

A distinct earlier textual route is now closed at bibliographic level:

```text
冀淑英：
《百川归海，蔚为大观》
收于《冀淑英文集》
北京图书馆出版社，2004
```

This earlier article is independently cited by both a National Library of China publication and a Taiwan National Central Library journal article. Separately, Tokyo Metropolitan Library exposes a physical 2004 `《冀淑英文集》` holding.

This creates a lawful earlier-source acquisition route without claiming that the 2009 chapter is textually identical to the 2004 article.

## 2. National Library of China publication control

A National Library of China-hosted public PDF on Haiyuan Pavilion holdings lists in its bibliography:

```text
冀淑英：百川归海，蔚为大观。
见：冀淑英文集。
北京：北京图书馆出版社，2004。
```

The project directly reviewed the bibliography page image; no OCR-only authority is used for the title.

This closes:

```text
BAICHUAN_ARTICLE_EXISTS_IN_2004_WENJI = CLOSED
```

It does **not** close the article's page range or the text of its Tieqin section.

## 3. Taiwan National Central Library independent control

A 2015 article in `《国家图书馆馆刊》` independently includes in its references:

```text
冀淑英（2004）。
百川归海，蔚为大观。
在冀淑英文集。
北京市：北京图书馆出版社。
```

The project directly reviewed the bibliography page image.

This is independent modern bibliographic corroboration, not a second physical copy of the 2004 article and not target-text authority.

## 4. Tokyo Metropolitan physical holding route

Tokyo Metropolitan Library's public Digital BookShelf exposes:

```text
冀淑英文集 /
[冀淑英著].
北京圖書館出版社
2004.9
displayed shelf sequence: 022.0 / 6001 / 2004
```

CiNii Books independently lists `《冀淑英文集》` as a 2004.9 Beijing Library Press title available at multiple Japanese libraries.

The project has not obtained a copy, submitted a copying request, incurred a fee, or transmitted user identity data.

## 5. Relation to the 2009 Fifteen Lectures

The 2009 work identity remains controlled by the existing NDL source:

```text
《冀淑英古籍善本十五讲》
冀淑英著；李文洁插图
国家图书馆出版社
2009.7
```

A modern secondary Shuge discussion states that, according to the 2009 book's postscript and the 2004 collection's editor note, `《百川归海，蔚为大观》` was an audio/lecture transcript and the Fifteen Lectures was an illustrated expanded form of that text.

That is a **discovery locator only**. The project has not directly reviewed:

- the 2009 postscript;
- the 2004 collection editor note;
- the complete 2004 article;
- a page-by-page 2004→2009 textual collation.

Therefore:

```text
2009_DERIVED_FROM_2004_BAICHUAN
  = SECONDARY_REPORTED_NOT_DIRECTLY_CLOSED

CHAPTER9_EXACT_CORRESPONDENCE_TO_2004_SECTION
  = UNRESOLVED

DIRECT_COPY_OR_SAME_TEXT_EDGE
  = NOT_AUTHORIZED
```

## 6. Target-volume firewall

No reviewed source in this batch directly names:

- `《铜壶漏箭制度》`;
- `《准斋心制几漏图式》`;
- 3482 / 3483;
- 03482 / 03483;
- the 1823 Huang Pilie / Shiliju one-volume fingerprint.

The existence of an earlier Ji Shuying lecture/article route does not select the target's acquisition mode.

```text
TARGET_PURCHASE_SELECTED=false
TARGET_DONATION_SELECTED=false
FINAL_TRANSFER_PATH=UNRESOLVED
```

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

1. Obtain or inspect the 2004 `《冀淑英文集》` and directly locate `《百川归海，蔚为大观》`: exact page range, editor note and Tieqin subsection.
2. Directly review the 2009 `《十五讲》` postscript and compare its source statement with the 2004 collection editor note.
3. If the source genealogy closes, collate the 2004 Tieqin subsection against 2009 chapter 9 and record additions/omissions rather than presuming textual identity.
4. Search the direct 2004/2009 text for the target titles, 3482/3483, 03482/03483 and the 1823 bound-volume fingerprint.
5. Continue the higher-priority direct `《北京图书馆馆史资料汇编（二）：1949—1966》` pp.446—449 route in parallel.

Research record: `docs/research/ZIWEI-JI-SHUYING-2004-BAICHUAN-ARTICLE-HOLDING-AND-FIFTEEN-LECTURES-SOURCE-GENEALOGY-BOUNDARY-R1.json`.
