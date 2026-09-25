# Fusion Chart Historical Provenance Audit R1 — Batch 12GT

## 2004《冀淑英文集》机构书目页数校准与零售 `p456` 推页防火墙

Status: **CINII EXACT RECORD DIRECTLY REVIEWED / STANFORD SEARCHWORKS INDEPENDENT INSTITUTIONAL CONTROL / BOTH CONVERGE ON 435-PAGE NUMBERED MAIN SEQUENCE / PRELIMINARY-MATTER DESCRIPTION DIFFERS / RETAIL p456 REJECTED FOR PAGE INFERENCE / ITEM 74 EXACT PAGES STILL UNRESOLVED / ZERO RUNTIME, MATRIX, GENEALOGY OR TARGET-TRANSFER CHANGE**

## 1. Why this batch is necessary

Batch 12GS closed `《百川归海，蔚为大观》` as TOC item 74 but deliberately refused to infer its pages. The same retail page that exposed the complete TOC also printed `p456`. Before any later researcher is tempted to reverse-estimate item 74 from that number, the physical-extent metadata must be checked against institutional catalogs.

## 2. CiNii exact-record control

NII/CiNii Books record `BA71484545` directly identifies:

```text
冀淑英文集
[冀淑英著]
北京圖書館出版社, 2004.9
ISBN 7501324611
ページ数/冊数: 4, 435p
大きさ: 22cm
所蔵館: 11館
```

This is a union-catalog bibliographic record for the exact edition, not a retail description.

## 3. Stanford independent control

Stanford University Libraries SearchWorks independently exposes the same title under catkey `6318452` and records:

```text
4, 10, 435 p. : ill. (some col.) ; 22 cm
```

The reviewed web route timed out when opening the full SearchWorks record, so this batch treats the indexed institutional catalog result as the reviewed Stanford layer and does not claim more than that result exposes.

## 4. Extent adjudication

The three source layers are preserved literally:

```text
CiNii institutional union catalog
  = 4, 435p

Stanford institutional catalog
  = 4, 10, 435 p.

Frelax retail catalog / GS
  = p456/32開/精装
```

The two institutional records converge on a **435-page numbered main sequence** but differ in their description of preliminary matter. That preliminary difference is retained rather than normalized away.

Therefore:

```text
RETAIL_P456_AS_CANONICAL_PAGINATION
  = REJECTED_FOR_PAGE_INFERENCE

RETAIL_P456_MEANING
  = UNRESOLVED_DO_NOT_NORMALIZE

BAICHUAN_ITEM_74_EXACT_PAGE_RANGE
  = UNRESOLVED

PAGE_INTERPOLATION_FROM_74_OF_75_OR_TOTAL_EXTENT
  = NOT_AUTHORIZED
```

This is a bibliographic-control improvement, not direct page collation.

## 5. Source-genealogy and target-volume consequence

Nothing in these extent records exposes the text of item 74, `編后記`, the 2009 postscript, or the target `《铜壶漏箭制度》 / 《准斋心制几漏图式》` identifiers.

The 2004→2009 derivation remains:

```text
SECONDARY_REPORTED_NOT_DIRECTLY_CLOSED
```

No target purchase/donation route is selected.

## 6. Product / genealogy consequence

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

## 7. Highest next gate

1. Directly inspect the 2004 physical/digital volume around TOC item 74 and recover the exact pages and complete text.
2. Directly inspect final `《編后記》` and the 2009 `《十五讲》` postscript.
3. Recover the 2010 `《〈冀淑英文集〉补遣》` author/pages/body.
4. Continue direct 1997 `《北京图书馆馆史资料汇编（二）：1949—1966》` pp.446—449 collation.

Research record: `docs/research/ZIWEI-JI-SHUYING-WENJI-2004-INSTITUTIONAL-PAGINATION-AND-RETAIL-P456-FIREWALL-R1.json`.
