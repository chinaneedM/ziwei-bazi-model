# Fusion Chart Historical Provenance Audit R1 — Batch 12H

## Japan Ming Fullbook archive + formal facsimile routes

Status: **MING FULLBOOK ARCHIVE IDENTITY CLOSED / FORMAL FACSIMILE ROUTE CLOSED / TARGET PAGE NOT OBSERVED / TOYO QUANJI PROVENANCE DISCREPANCY PRESERVED / NO ALGORITHM REOPEN**

Batch 12H moves the late-Zi collation away from generic modern scans and binds a high-quality Japanese archival/facsimile route for a Ming 《紫微斗數全書》 witness.

## 1. National Archives of Japan Ming Fullbook object

The National Archives of Japan public search/viewer index binds:

- title: `新鋟希夷陳先生紫微斗数全書`;
- call number: `子０６０－０００１`;
- former owner: `紅葉山文庫`;
- people: `陳搏（宋） / 潘希尹（明）`;
- bibliographic label: `刊本:明:::`;
- quantity: `2冊`;
- access class: `公開`.

The first item is independently indexed as item `4468520`, `新鋟希夷陳先生紫微斗数全書１`, volume `0001`, also `公開`, with a content-download interface and JP2 image content.

This closes the archive/digital-object identity. It does **not** read the late-Zi target page.

## 2. GitHub-runner access boundary

Research run `34134081787` / artifact `10023248966` followed only officially documented `file/item .json/.ttl/.rdf` and known `/img/[ID]` routes.

All nine seed routes returned HTTP 403 with 919-byte responses from the GitHub runner. No adjacent item ID, page number, image identifier or manifest ID was guessed.

Therefore:

```text
NAJ_GITHUB_RUNNER_ROUTE=CURRENTLY_BLOCKED_403
ARCHIVE_OBJECT_ABSENT=NO
DIGITAL_IMAGES_ABSENT=NO
TARGET_PAGE_ABSENT=NO
```

The official public search index remains positive for the archive/digital object.

## 3. Formal facsimile publication route

山东大学国际汉学研究中心 / 全球汉籍合璧工程 directly lists the work in `《子海珍本编·日本卷》第一辑`:

```text
《新鋟希夷陳先生紫微斗數全書》七卷，
（宋）陳摶撰，（明）潘希尹補。
據内閣文庫藏明刊本影印。
```

Research run `34134328002` / artifact `10023353526` captured both official SDU surfaces with HTTP 200.

This is a formal facsimile route to the same Naikaku/National-Archives Ming witness family. The exact subvolume within the 15-volume `《子海珍本編·海外卷·日本：內閣文庫》` set is not yet bound.

## 4. Scholarly genealogy

Chen Zhaoyin's peer-reviewed NCKU paper was directly retrieved as a 2,105,566-byte PDF, SHA-256 `17d0089c3328253230cb2f110ac40527abe41fbb97183483215a5e633e5b2e2e`.

Direct visual review of printed pp.60–61, without OCR, shows the edition table:

- the Japan National Archives Fullbook row carries `書林棲和堂葉梓行、南陽堂較梓`, former `紅葉山文庫`, now National Archives of Japan;
- the separate Quanji row carries `金陵益軒唐謙梓` and notes acquisition by Toyo Bunko in June 1942;
- the paper then organizes circulated Fullbook versions around two publishing-origin families, Jianyang Qihetang/Nanyangtang and Jinling Yixuan Tang Qian.

This is modern scholarly genealogy, not target-glyph authority.

## 5. Toyo Bunko official-catalog discrepancy

Toyo Bunko's public Hanji database directly returns call mark `VII-3-157` with:

- `新刊希夷陳先生紫微斗數全集不分卷` — `鈔本`;
- `新刊希夷陳先生紫微斗數全集` — `寫本`.

That does not match a simplistic claim that the current catalog object is itself the printed `金陵益軒唐謙梓` witness named in the NCKU genealogy table.

Batch 12H therefore preserves:

```text
TOYO_CURRENT_CATALOG_OBJECT=MANUSCRIPT/COPY_LABEL
NCKU_PRINT_GENEALOGY=JINLING_YIXUAN_TANG_QIAN
EXACT_PROVENANCE_BRIDGE=UNRESOLVED
CONFLATION=FORBIDDEN
```

## 6. Effect on HPA-ZDATE-006

The Japan route substantially improves the edition horizon, but still does not expose the target `亥時` glyph.

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
JAPAN_MING_FULLBOOK_IDENTITY=CLOSED_AT_ARCHIVE_AND_FORMAL_FACSIMILE_ROUTE_LEVEL
JAPAN_TARGET_PAGE=NOT_OBSERVED
HAI_GLYPH_STABILITY_ACROSS_PHYSICAL_EDITIONS=UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES
RUNTIME_TIME_STANDARD_BINDING=UNRESOLVED
NEW_CANDIDATE=NO
ALGORITHM_REOPEN=NO
```

Next acquisition gate: identify the exact `子海珍本編·海外卷·日本：內閣文庫` subvolume containing this Fullbook or obtain an official National Archives image/download session outside the blocked runner, then bind exact facsimile page/leaf and directly read the late-Zi target.

## 7. Accounting

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

Machine evidence: `docs/research/ZIWEI-JAPAN-MING-FULLBOOK-FACSIMILE-ROUTES-R1.json`.

The deterministic fusion-chart product remains CLOSED.
