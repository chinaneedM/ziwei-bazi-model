# Historical Provenance Audit — Batch 12GJ

## 1. Batch identity

- Batch: `BATCH-12-ZIWEI-GU-TINGLONG-DIARY-P593-P595-PAGE-CALIBRATION-AND-JAN6-FALSE-LEAD-FIREWALL-GJ`
- Prior batch: `BATCH-12-ZIWEI-DENG-ZHICHENG-DIARY-VOL5-TOYO-BUNKO-FIRST-PARTY-HOLDING-AND-COPY-SERVICE-BOUNDARY-GI`
- Scope: page-citation calibration for the unresolved 1950-01-06 Gu Tinglong diary entry.
- This is a provenance/locator firewall batch only.

## 2. Page 593 citation

The official public HTML for Wang Shiwei's 2025 *Library Journal* article
`古籍版本目录学界的“南顾北赵”——纪念赵万里先生诞辰120周年`
directly exposes reference [40] as:

`顾廷龙,李军,师元光. 顾廷龙日记[M]. 北京:中华书局,2022:593.`

The public HTML surface exposes the abstract and reference list, but not the in-text
citation context for reference [40]. Therefore the project can close only the
existence of a p.593 citation. It cannot bind p.593 to 1950-01-06.

## 3. Page 595 chronology control

A Peking University-hosted academic PDF by Chen Ming is publicly indexed with text
that explicitly associates 1951-12-25 with the Gu diary phrase
`得一良寄乃翁《六十纪念集》`, with its footnote locating that entry at
`《顾廷龙日记》第595页`.

The direct PDF fetch timed out in the reviewed public browser route, so this batch
records that observation only as search-index text from the PKU-hosted academic PDF.
No direct PDF-page screenshot and no direct 2022 diary page 595 were reviewed.

This control is sufficient to reject a shortcut that treats a bare p.593 citation
as proof of the 1950-01-06 target page. It is **not** sufficient to identify the
exact event on p.593.

## 4. Existing 1950 sample boundary

The public reproduction of Li Jun's editorial preface exposes sample imagery
captioned `1950年1月1日、2日、3日、4日日记`.

That sample does not include 1950-01-06 and supplies no Jan-6 page number.

## 5. Adjudication

Accordingly:

- p.593 citation existence = `CLOSED_AT_LIBRARY_JOURNAL_REFERENCE_LIST_LEVEL`;
- p.593 event/date = `UNRESOLVED`;
- p.595 / 1951-12-25 = `SEARCH_INDEX_TEXT_CONTROL`;
- p.593 → 1950-01-06 = **not authorized**;
- exact 1950-01-06 published page = `UNRESOLVED`;
- direct 1950-01-06 published text = `NOT_REVIEWED`;
- direct manuscript text = `NOT_REVIEWED`.

No page-number interpolation is permitted.

## 6. Product / genealogy consequence

This batch adds no transmission node or edge and does not bind historical catalog
nos. `3482/3483` or current `03482/03483` to any acquisition event.

`ACQUISITION_EDGE_AUTHORIZED=false`;
`SAME_OBJECT_EDGE_AUTHORIZED=false`;
`RUNTIME_RULE_CHANGE=false`;
`ALGORITHM_REOPEN=false`;
`CANDIDATE_COLLAPSE=false`.

Matrix row/audited/missing counts remain **198 / 166 / 10**.
Provenance defects remain **14 / 14 repaired**.
Chart algorithm defects remain **0**.
`DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED`.

Machine evidence:
`docs/research/ZIWEI-GU-TINGLONG-DIARY-P593-P595-PAGE-CALIBRATION-JAN6-FIREWALL-R1.json`.
