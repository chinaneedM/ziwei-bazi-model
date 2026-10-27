# Fusion Chart Historical Provenance Audit R1 — Batch 12GU

## 《文津学志》第三辑：日本三馆实体馆藏定位与匿名 OPAC 访问边界

Status: **VOLUME-3 PHYSICAL HOLDINGS CLOSED FOR THREE JAPANESE UNIVERSITY LIBRARY COPIES AT CINII LAYER / VOLUME-SPECIFIC CALL NUMBERS AND ITEM IDENTIFIERS EXPOSED / KYOTO AND UTOKYO OPAC LINKS RETURN HTTP 403 IN REVIEWED ANONYMOUS TOOL ROUTE / ARTICLE AUTHOR, PAGES AND BODY STILL UNRESOLVED / NO LOGIN, REQUEST, IDENTITY OR FEE / ZERO RUNTIME, MATRIX, GENEALOGY OR TARGET-TRANSFER CHANGE**

## 1. Why this batch matters

Batch 12GQ proved the formal existence of `《〈冀淑英文集〉补遣》` in the 2010 `《文津学志》第三辑`, but only at TOC/ISBN level. The next useful step is to identify exact physical copies that could support lawful direct collation, without pretending that a holding record is already article text.

## 2. CiNii/NII exact serial and volume control

The directly reviewed CiNii Books record `BA65589403` lists `第3輯` and binds the volume series to ISBN `9787501340859`.

The same record exposes three exact third-volume holdings relevant to direct collation:

```text
京都大学 人文科学研究所 図書室 / 人情セ
  第3輯
  020.22||Ko/43||3
  200035254509

京都大学 文学研究科 図書館 / 東洋史
  第3輯
  FXIIb||B||7
  200019220216

東京大学 大学院人文社会系研究科・文学部 図書室 / 中国思想
  第3輯
  3号館B37:Guo:3
  4818863757
```

These are volume-specific institutional holding identifiers. They do not reveal the supplement article pages.

## 3. OPAC route check

Following the CiNii OPAC links in the reviewed anonymous web route produced:

```text
Kyoto KULINE openurl route
  = HTTP 403 in reviewed anonymous tool route

University of Tokyo OPAC openurl route
  = HTTP 403 in reviewed anonymous tool route
```

Critical boundary:

```text
CRAWLER_OR_TOOL_HTTP_403
  != proof that ordinary human catalog access is forbidden
  != proof that on-site access is forbidden
  != proof that reference/copy service is unavailable
```

No login, library account, email, reference request, copy order, user identity or fee was used.

## 4. What is and is not closed

```text
EXACT_JAPAN_VOLUME3_PHYSICAL_HOLDING_ROUTES
  = CLOSED_FOR_THREE_INSTITUTIONAL_COPIES_AT_CINII_LAYER

SUPPLEMENT_ARTICLE_FORMAL_EXISTENCE
  = remains CLOSED_AT_PUBLISHED_TOC_LEVEL from 12GQ

SUPPLEMENT_ARTICLE_AUTHOR
  = UNRESOLVED

SUPPLEMENT_ARTICLE_PAGE_RANGE
  = UNRESOLVED

SUPPLEMENT_ARTICLE_BODY
  = NOT_REVIEWED
```

Multiple physical holdings are **not** multiple textual votes until their relevant pages are actually collated.

## 5. External-action firewall

The project has not contacted any library and has not transmitted user-specific information.

If public discovery remains exhausted, a reference or reproduction request to Kyoto University or the University of Tokyo is an explicit user-authorized external-action boundary and must not be initiated automatically.

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

1. Continue public article-level discovery for `《〈冀淑英文集〉补遣》`: author, exact pages, body or lawful digital surrogate.
2. If public routes are genuinely exhausted, treat a Kyoto/Tokyo reference or copy inquiry as an explicit user-authorized action; do not submit automatically.
3. Continue direct 2004 item 74 / final `《編后記》` and 2009 postscript discovery.
4. Continue direct 1997 `《北京图书馆馆史资料汇编（二）：1949—1966》` pp.446—449 collation.

Research record: `docs/research/ZIWEI-WENJIN-XUEZHI-V3-JAPAN-PHYSICAL-HOLDINGS-AND-OPAC-ACCESS-BOUNDARY-R1.json`.
