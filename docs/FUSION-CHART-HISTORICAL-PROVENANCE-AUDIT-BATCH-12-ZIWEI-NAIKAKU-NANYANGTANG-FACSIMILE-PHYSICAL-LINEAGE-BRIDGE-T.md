# Fusion Chart Historical Provenance Audit R1 — Batch 12T

## Naikaku / National Archives Nanyangtang facsimile physical-lineage bridge

Status: **BATCH 12A DIRECT FACSIMILE ↔ NAIKAKU / NATIONAL ARCHIVES MING FULLBOOK HIGH-CONFIDENCE LINEAGE CONVERGENCE / OLD REGISTRATION CROSSWALK NOT EXPLICITLY CLOSED / DEDUP ONLY / ZERO NEW TEXTUAL-GLYPH VOTES / NO ALGORITHM REOPEN**

Batch 12T revisits an unresolved bridge left between Batch 12A and Batch 12H. It does not discover a second late-Zi witness. It improves the provenance of the already-collated Batch 12A facsimile and prevents double counting.

### 1. Batch 12A physical marks, re-read directly without OCR

The controlling Batch 12A PDF remains SHA-256 `32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7`, 527 pages, artifact `10016416872`.

Its first page visibly carries:

- cover title `紫微斗數全書 上`;
- old shelf/registration label columns `漢 / 子六十 / 一五八五六 / 全二`.

The second page visibly carries `陳希夷先生著 / 紫微斗數全書 / 南陽堂較梓`.

The already-reviewed target page remains PDF p.320, 卷五《論人生時要審的確》, where the direct facsimile visibly reads `如子時有十刻上五刻屬昨夜亥時下五刻屬今日子時`.

### 2. First-party National Archives object

The National Archives of Japan public index binds `新鋟希夷陳先生紫微斗数全書` to `子０６０－０００１`, former owner `紅葉山文庫`, `刊本:明:::`, quantity `2冊`, with public digital object `file/1078787` and first item `4468520`. Its official 2019 digitization target list independently lists `子060-0001 新鍥希夷陳先生紫微斗数全書`.

Batch 12H had already closed this official archive/digital-object identity, but could not observe the target page.

### 3. Provenance convergence and ceiling

The physical/codicological fields now converge strongly: Ming Fullbook title family, Nanyangtang imprint, `子六十` ↔ `子060` class, two-volume total, and the Naikaku/Red-Leaves/National-Archives holding genealogy also preserved by the formal SDU facsimile route and NCKU edition study.

This supports `HIGH_CONFIDENCE_SAME_NAIKAKU_NATIONAL_ARCHIVES_MING_FULLBOOK_LINEAGE` for the Batch 12A mirror.

However, no reviewed first-party catalog surface explicitly states that legacy registration number `漢15856` was migrated to current call `子060-0001`. Therefore Batch 12T does **not** claim a formally closed old-number crosswalk, and it does not rewrite the mirror p.320 image as a first-party National Archives viewer capture.

### 4. Runner access boundary

Recheck run `34224240506` / artifact `10054995877` followed only the already known first-party `/file/1078787`, `/item/4468520`, and `/img/4468520` routes. All three returned a 919-byte CloudFront `ERROR: The request could not be satisfied` page in the GitHub runner. This is a CDN/runner boundary only.

### 5. Dedup and rule effect

```text
BATCH12A_MIRROR_AND_NAJ_ROUTE_INDEPENDENT_WITNESSES=NO
DIRECT_INDEPENDENT_HAI_GLYPH_WITNESS_ADDED=0
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_CHART_RULE_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
```

The deterministic product remains CLOSED. The next gate is either an explicit first-party legacy-number crosswalk / official NAJ target-page capture, or a genuinely independent directly readable `五凶神` physical witness.

Machine evidence: `docs/research/ZIWEI-NAIKAKU-NANYANGTANG-FACSIMILE-PHYSICAL-LINEAGE-BRIDGE-R1.json`.
