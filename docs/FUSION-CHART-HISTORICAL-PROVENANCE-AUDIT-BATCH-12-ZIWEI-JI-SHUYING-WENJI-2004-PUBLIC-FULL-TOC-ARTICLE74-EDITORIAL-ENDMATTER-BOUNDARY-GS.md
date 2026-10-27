# Fusion Chart Historical Provenance Audit R1 — Batch 12GS

## 2004《冀淑英文集》公开完整目录：第74篇《百川归海，蔚为大观》结构定位与“编后记”边界

Status: **PUBLIC FULL TOC DIRECTLY REVIEWED / BAICHUAN CLOSED AS TOC ITEM 74 / TARGET NARROWED TO CLOSING MAIN-TEXT BLOCK / FINAL 編后記 LABEL EXPOSED / EXACT ARTICLE PAGES AND BODY NOT REVIEWED / 編后記 ≠ SECONDARY-REPORTED 编者注 UNLESS DIRECTLY PROVED / ZERO RUNTIME, MATRIX, GENEALOGY OR TARGET-TRANSFER CHANGE**

## 1. Why this batch matters

Batch 12GP closed the formal 2004 article identity but did not know where the article sat inside the volume. Batch 12GR then removed pp.383—385 as an unauthorized shortcut. The next lawful step is therefore to narrow the article structurally without inventing page numbers.

A public 書虫精品 / 芸香閣叢書 catalog surface exposes a complete contents sequence for the 2004 volume.

## 2. Directly reviewed public TOC surface

The page displays the volume as:

```text
冀淑英 著
北京図書館
2004年9月
p456/32開/精装
ISBN7-5013-2461-1
```

These are preserved as literal retail-catalog metadata, not silently promoted to canonical pagination.

The complete TOC then places the target at:

```text
七十三  宋元明清版本…概况
七十四  百川歸海 蔚爲大…
七十五  中国古代目録学簡述
附録
  一  冀淑英…復王紹曾書
  二  冀淑英…復陳先行的信
  三  冀淑英致沈津信
編后記
```

The public page has mojibake in several glyphs. The exact normalized target title `《百川归海，蔚为大观》` is not reconstructed from mojibake alone; it is bound to the institutional title identity already closed in Batch 12GP.

## 3. What is now closed

```text
BAICHUAN_TOC_ORDINAL
  = 74

BAICHUAN_STRUCTURAL_POSITION
  = CLOSING_MAIN_TEXT_BLOCK
  = AFTER_ITEM_73
  = BEFORE_ITEM_75
  = BEFORE_APPENDIX_AND_FINAL_編后記

FINAL_EDITORIAL_ENDMATTER_LABEL
  = 編后記
  = CLOSED_AT_TOC_LABEL_LAYER
```

This materially narrows where direct physical/digital collation must start.

## 4. What remains unresolved

The surface does **not** expose:

- item 74 start page;
- item 74 end page;
- any direct item 74 text;
- page number or text of `編后記`;
- evidence that `編后記` is the same textual object as the secondary-reported `编者注`;
- the 2009 `《十五讲》` postscript.

Therefore:

```text
BAICHUAN_EXACT_PAGE_RANGE
  = UNRESOLVED

DIRECT_2004_BAICHUAN_TEXT
  = NOT_REVIEWED

DIRECT_2004_EDITOR_NOTE
  = NOT_REVIEWED

DIRECT_FINAL_編后記_TEXT
  = NOT_REVIEWED

編后記_EQUALS_SECONDARY_REPORTED_编者注
  = NOT_PROVED

PAGE_INTERPOLATION_FROM_ORDINAL_OR_P456
  = NOT_AUTHORIZED
```

## 5. Relation to 12GP / 12GQ / 12GR

- 12GP article identity and physical-holding route remain valid.
- 12GQ 2010 `《〈冀淑英文集〉补遣》` still lacks author/pages/body.
- 12GR correctly blocks pp.383—385 as a Baichuan shortcut.
- 12GS replaces that false shortcut with a lawful structural locator: **TOC item 74**, but still no page interpolation.

The 2004→2009 derivation status remains:

```text
SECONDARY_REPORTED_NOT_DIRECTLY_CLOSED
```

No direct-copy or same-text edge is authorized.

## 6. Target-volume firewall

Nothing newly reviewed in this batch directly binds:

- `《铜壶漏箭制度》`;
- `《准斋心制几漏图式》`;
- 3482 / 3483;
- 03482 / 03483;
- the 1823 Huang Pilie / Shiliju one-volume fingerprint.

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

1. Lawfully inspect the 2004 volume around **TOC item 74** and recover exact start/end pages and full `《百川归海，蔚为大观》` text.
2. Directly inspect the final `《編后記》`; only then determine whether it contains or corresponds to the secondary-reported `编者注`.
3. Directly inspect the 2009 `《十五讲》` postscript, then collate the 2004 Tieqin subsection against 2009 chapter 9.
4. Continue direct 2010 `《〈冀淑英文集〉补遣》` recovery and direct 1997 `《北京图书馆馆史资料汇编（二）：1949—1966》` pp.446—449 collation in parallel.

Research record: `docs/research/ZIWEI-JI-SHUYING-WENJI-2004-PUBLIC-FULL-TOC-ARTICLE74-EDITORIAL-ENDMATTER-BOUNDARY-R1.json`.
