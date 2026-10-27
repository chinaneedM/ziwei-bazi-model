# Fusion Chart Historical Provenance Audit R1 — Batch 12A

## Ziwei 《紫微斗數全書》南陽堂本晚子時影印校勘

Status: **DIRECT FACSIMILE COLLATION COMPLETE / NEW SOURCE-SCOPED CANDIDATE IDENTIFIED / NO ALGORITHM REOPEN**

A public indexed seven-juan PDF was acquired by the research-only GitHub workflow without authentication, OCR or identifier brute force.

- acquisition run: `34116332295`
- artifact: `10016416872`
- PDF SHA-256: `32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7`
- PDF pages: `527`
- 卷五 begins at zero-based page `312`; 卷六 at `382`
- machine evidence: `docs/research/ZIWEI-QUANSHU-NANYANGTANG-LATE-ZI-DIRECT-COLLATION-R1.json`

The reviewed title surface directly shows `紫微斗數全書`, `陳希夷先生著` and `南陽堂梓`. The exact print year is not closed by the reviewed surfaces.

## Direct reading

PDF page 320 (one-based), 卷五, directly shows `論人生時要審的確` and:

`如人生子亥二時最難定凖要仔細推詳`

`如子時有十刻上五刻屬昨夜亥時下五刻屬今日子時`

`如天氣陰雨之際必須羅經以定真確時候若差訛則命不凖矣`

PDF page 321 begins `論命先貧後富`, so the target section is bounded on page 320.

## S01 attribution

S01 attributes `子時乃一日之始，當從新日計。` to 《紫微斗數全書》. That exact sentence is **not observed on the directly reviewed target-section page**. This is not a whole-volume negative-search claim.

The direct Fullbook witness instead preserves a distinct ten-ke split rule. Therefore `PROV-DEFECT-005` remains quarantined and the page cannot be rewritten into a simple `ZI_START_23` rollover rule.

## New candidate family

Current `NatalStructureGenerator._hour_branch_index()` maps local apparent-solar `23:00..00:59` uniformly to 子. Existing `MIDNIGHT` / `ZI_START_23` profiles change date handling only; they cannot represent a source-scoped half-Zi reclassification to 亥.

New row:

`HPA-ZDATE-006 = MISSING_FROM_PRODUCT`

Candidate:

`NANYANGTANG-FULLBOOK-ZI-TEN-KE-HAI-SPLIT-R1`

Before productization, further work must independently close the historical meaning/orientation of `上五刻 / 下五刻`, modern-clock mapping, branch/date composition, additional Fullbook editions, and exact Nanyangtang print dating.

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
HISTORICAL_CANDIDATE_EXTENSIONS=6
HISTORICAL_CANDIDATE_REGISTRIES=3
HISTORICAL_CANDIDATE_RUNTIME_RESOLVERS=3
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

The deterministic fusion-chart product remains CLOSED.
