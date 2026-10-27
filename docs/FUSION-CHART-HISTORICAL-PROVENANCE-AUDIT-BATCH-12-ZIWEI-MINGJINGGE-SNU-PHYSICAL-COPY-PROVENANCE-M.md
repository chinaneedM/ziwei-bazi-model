# Fusion Chart Historical Provenance Audit R1 — Batch 12M

## 1870 Mingjingge Quanji: SNU Ilsa physical-copy provenance, volume-4 scan route, mirror dedup, and Hanyang independent-holding locator

Status: **SNU PHYSICAL-COPY / VOLUME-4 DIGITIZATION LINEAGE BOUND / FIVE-XIONG-SHEN TARGET PAGE NOT OBTAINED / MIRROR DOUBLE-COUNT FORBIDDEN / HANYANG INDEPENDENT HOLDING LOCATED / NO ALGORITHM REOPEN**

Batch 12M moves the `《飛星策天紫微斗數全集》` late-Zi route from modern received transcription to a specific 1870 Mingjingge physical-copy/digitization lineage, while deliberately stopping short of a target-text claim.

## 1. SNU Ilsa copy and 1870 Mingjingge imprint

Public high-resolution images expose the call-number family `一簑古 523.5 J562b v.1-6`.

Direct no-OCR review of the v.1 controls shows:

- cover label: `523.5 / J562b / V.1`;
- title/imprint surface: `同治九年新鐫`;
- visible title surface: `飛星紫微斗數`;
- `陳希夷先生著`;
- `羊城明經閣板`.

This directly closes edition/imprint identity at the visible-image level without expanding small or obscured glyphs beyond what can actually be read.

## 2. SNU volume 4 is directly bound

The unauthenticated Pduola public preview exposes five book-page images carrying Seoul National University Kyujanggak Korean Studies Institute branding.

Direct review gives:

```text
0001 = physical cover / 斗數 四 / 523.5 J562b V.4
0002 = volume-four opening material; 太微賦總括 visible
0003 = early volume-four text
0004 = early volume-four text
0005 = early volume-four text
```

The target `五凶神` heading and the late-Zi line are **not** present in these five public pages.

The full Pduola file is paywalled. No purchase or restricted full-file download was attempted.

## 3. Mirror deduplication

The following public routes are governed as one SNU/Kyujanggak digitization lineage unless a distinct physical-copy bridge is later proven:

- Pduola v.4 public preview;
- Shenjige call-number images;
- Scribd pages indexed with `서울대학교 규장각한국학연구원` / `飛星策天紫微斗數全集`.

Therefore:

```text
MIRROR_HOST_COUNT != PHYSICAL_WITNESS_COUNT
SAME_SNU_DIGITIZATION_LINEAGE_INDEPENDENT_VOTES=0
```

This applies the Batch 12I rule `DO_NOT_DOUBLE_COUNT_SAME_PHYSICAL_COPY_OR_DIGITIZATION_LINEAGE`.

## 4. Scribd public-preview boundary

Search-engine indexing exposes SNU/Kyujanggak page labels from 0001 through 0035, but a direct unauthenticated browser run reaches only a `Client Challenge` CAPTCHA.

No CAPTCHA bypass was attempted.

Accordingly, indexed page labels are provenance/access evidence only; they are not a substitute for direct visual target-page review.

## 5. Official Kyujanggak execution boundary

The official public Kyujanggak catalog service remains a high-priority route. A GitHub-runner probe to the public old-book list failed during TLS handshake with `Connection reset by peer`, before any search submission.

This is classified only as:

`EXECUTION_ENVIRONMENT_ACCESS_BOUNDARY`

It is **not** evidence that the record or image object is absent.

No `book_cd` guessing, hidden endpoint enumeration, authentication, or token reuse was attempted.

## 6. Separate Hanyang University holding

The Academy of Korean Studies Sillokwiki bibliography independently records:

- `新刻合倂十八飛星策天紫微斗數全集`;
- 6卷6冊;
- 木板本;
- 1870 / 同治九年;
- 明經閣;
- holding: 漢陽大學校圖書館.

This is potentially a second physical copy and therefore materially more valuable than another SNU mirror. However, no Hanyang target page has yet been directly observed, so it contributes no target-text or glyph vote in this batch.

## 7. Philological boundary

The currently received Quanji text says:

`子有十刻，上五刻屬昨夜，下五刻屬今夜子`.

The directly reviewed Nanyangtang Fullbook says:

`上五刻屬昨夜亥時、下五刻屬今日子時`.

These are parallel but not mechanically identical: the Quanji received text does not explicitly name the upper half as `亥時`.

A direct physical `五凶神` page is therefore required before any cross-work rule identity is formalized.

## 8. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
SNU_V4_PHYSICAL_SCAN_ROUTE=BOUND_PUBLIC_PAGES_0001_0005
SNU_FIVE_XIONG_SHEN_TARGET_PAGE=PENDING_DIRECT_PAGE
HANYANG_TARGET_PAGE=PENDING_DIRECT_PAGE
DIRECT_INDEPENDENT_HAI_GLYPH_WITNESS_COUNT_ADDED=0
CROSS_MIRROR_VOTE_COUNT=0
NEW_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
```

Next gate: direct `五凶神` target page from SNU Ilsa v.4 or the independent Hanyang copy.

## 9. Accounting

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

Machine evidence: `docs/research/ZIWEI-MINGJINGGE-SNU-PHYSICAL-COPY-PROVENANCE-R1.json`.

The deterministic fusion-chart product remains CLOSED.
