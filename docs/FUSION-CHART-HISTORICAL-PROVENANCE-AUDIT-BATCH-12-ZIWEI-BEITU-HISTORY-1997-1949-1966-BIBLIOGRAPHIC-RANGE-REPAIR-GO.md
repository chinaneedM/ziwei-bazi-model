# Fusion Chart Historical Provenance Audit R1 — Batch 12GO

## 《北京图书馆馆史资料汇编（二）》1997 书目范围修正：1949—1966，而非 1946—1966

Status: **CANONICAL 1997 BIBLIOGRAPHIC IDENTITY = 1949—1966 / GOOGLE BOOKS ISBN 7501314195 + NLC OWN 2023 PUBLICATION CONVERGE / CAI-LI 2024 REFERENCE [23] RETAINS OBSERVED 1946—1966 AS CITATION-LAYER VARIANT / HIGH-CONFIDENCE TYPO CLASSIFICATION / PP.446—449 CITATION BRIDGE PRESERVED / DIRECT PAGES STILL NOT REVIEWED / ZERO RUNTIME OR GENEALOGY CHANGE**

## 1. Why this repair is required

Batch 12GN correctly transcribed what the National Library of China-hosted 2024 Cai Chengpu / Li Jing article prints in reference [23]:

```text
北京图书馆馆史资料汇编二：1946—1966
北京图书馆出版社，1997：446—449
```

That is an observation about the **2024 citation layer**. It must not automatically become the canonical title/range identity of the 1997 book.

Independent bibliographic and NLC-internal publication evidence now converge on:

```text
北京图书馆馆史资料汇编（二）：1949—1966
```

Therefore the repository must preserve both facts without collapsing them:

```text
2024_CAILI_REFERENCE_OBSERVED_RANGE = 1946—1966
1997_CANONICAL_BIBLIOGRAPHIC_RANGE = 1949—1966
```

## 2. Google Books bibliographic object

Google Books volume `BZ0M0gEACAAJ` exposes:

- title: `北京图书馆馆史资料汇编: 1949-1966, Volume 2`;
- contributor: `北京图书馆. 馆史资料汇编(二)编辑委员会`;
- publisher: `北京图书馆出版社`;
- year: `1997`;
- ISBN: `7501314195` / `9787501314195`;
- length: `1811 pages`.

This is a bibliographic object, not a direct page image of pp.446—449.

## 3. National Library of China internal publication control

The National Library of China-hosted PDF `《文津流觞》2023年第4期` contains Ma Tao's article `《王重民与鼎新之际的国家图书馆》`.

On the printed p.22 footnote, the citation visibly reads:

```text
北京图书馆馆史资料汇编（二）编辑委员会：
《北京图书馆馆史资料汇编（二）（1949—1966）》，
北京图书馆出版社，1997年，第606页。
```

This is especially important because it is an NLC-hosted publication independently using the 1949—1966 range for the same compilation/editor/publisher/year identity.

## 4. Adjudication of the 1946 / 1949 conflict

The evidence pattern is:

```text
CAI_LI_2024_NLC_HOSTED_REFERENCE_23
  range = 1946—1966

GOOGLE_BOOKS_1997_BIBLIOGRAPHIC_OBJECT
  range = 1949—1966
  ISBN  = 7501314195

NLC_WENJIN_2023_PUBLICATION
  range = 1949—1966
  same editor / publisher / year family
```

Adjudication:

```text
CANONICAL_1997_RANGE
  = 1949—1966

CAI_LI_2024_1946_RANGE
  = BIBLIOGRAPHIC_DATE_RANGE_VARIANT_HIGH_CONFIDENCE_TYPO

SILENT_NORMALIZATION
  = FORBIDDEN
```

The project retains the 2024 article's literal `1946—1966` in its source-layer record, but all canonical identification of the 1997 work must use `1949—1966`.

## 5. Effect on Batch 12GN

The repair does **not** invalidate 12GN's principal citation bridge.

Reference [23] still binds:

- the same editor identity;
- the same Beijing Library Press;
- the same 1997 publication;
- the same cited pp.446—449;
- immediately after the quoted Beijing-Library intake assessment.

Thus:

```text
PP446_449_CITATION_BRIDGE
  = PRESERVED

DIRECT_PP446_449_COLLATION
  = NOT_REVIEWED

EXACT_INTERNAL_DOCUMENT_IDENTITY
  = UNRESOLVED
```

Only the canonical date-range metadata is repaired.

## 6. Counter policy

This is an evidence-source bibliographic normalization analogous to the authorship-layer repair in Batch 12FN.

It does not alter a Historical Audit Matrix row, deterministic rule, historical-object acquisition conclusion, or product provenance counter.

Therefore:

```text
PROVENANCE_DEFECT_COUNTER_INCREMENT = 0
PROVENANCE_DEFECT_ACCOUNTING = 14 / 14 repaired
```

## 7. Product / genealogy consequence

```text
NODES_ADDED=0
EDGES_ADDED=0
ACQUISITION_EDGE_AUTHORIZED=false
SAME_OBJECT_EDGE_AUTHORIZED=false
RUNTIME_RULE_CHANGE=false
ALGORITHM_REOPEN=false
CANDIDATE_COLLAPSE=false
MATRIX_COUNT_CHANGE=false
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Accounting remains `198 / 166 / 10`, provenance defects `14 / 14 repaired`, chart algorithm defects `0`.

## 8. Highest next gate

1. Continue direct lawful acquisition/inspection of `《北京图书馆馆史资料汇编（二）：1949—1966》上册` pp.446—449.
2. On direct review, identify the reproduced internal document title/date/office, exact quotation boundaries, batch counts, prices, and identifiers.
3. Search every line for `铜壶漏箭制度`, `准斋心制几漏图式`, 3482/3483, 03482/03483 and the 1823 Huang/Shiliju one-volume fingerprint.
4. Preserve the Cai/Li 2024 `1946—1966` string only as an observed citation-layer variant, never as canonical edition identity.
5. Keep Lin Zhenyue 2024 report-source recovery, Ji Shuying chapter 9, Song Yunbin 1950-02-11 and Deng Zhicheng 1950-01-29 active in parallel.

Research record: `docs/research/ZIWEI-BEITU-HISTORY-1997-1949-1966-BIBLIOGRAPHIC-RANGE-REPAIR-R1.json`.
