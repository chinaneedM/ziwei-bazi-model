# Batch 12DD — 1589《月令通攷》“通書”来源标签与指纹材料范围物理校勘

## Status

```text
YUELING_1589_TARGET_NEIGHBORHOODS=DIRECT_PHYSICAL
YUSHUI_P27_TONGSHU_SOURCE_LABEL=DIRECT_PHYSICAL
DAHAN_P802_TONGSHU_SOURCE_LABEL=DIRECT_PHYSICAL
GENERIC_TONGSHU_SOURCE_FAMILY=PHYSICALLY_BOUND
EXACT_TONGSHU_TITLE_EDITION=UNRESOLVED
PRE1578_CITED_TONGSHU_DATE=UNRESOLVED
SANMING_TO_YUELING_DIRECT_COPY=UNPROVED
PRE1578_COMMON_SOURCE=UNPROVED
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
```

## 1. Question carried forward from Batch 12DA

Batch 12DA established that the 1589 Wang Daozeng edition of `《月令通攷》` physically preserves both high-information fingerprints also found in the exact 1578 `《三命通會》`:

- 大寒 43/57 -> `十三後` -> 44/56;
- 雨水 47/53 -> `後四日` -> 48/52.

But 12DA deliberately did **not** bind the target loci to a named source. It only noted that elsewhere the compilation cites `通書`.

12DD therefore asks a narrower philological/layout question:

> Does the physical 1589 target material itself carry a source-name label, and what bibliographic scope does that label authorize?

## 2. Controlled acquisition

```text
SOURCE=NCL-03165 月令通攷
EDITION=明萬曆十七年(1589)王道增臨海刊本
SOURCE_PDF_SHA256=bc95f32afb2bfe52b69ea4fb249481f6deee49d33b7b51f37f39ae9b383516a4
WORKFLOW_RUN=35347370998
ARTIFACT_ID=10547561713
ARTIFACT_DIGEST=sha256:e0144a547791283bccf0e3ea05765565bdaea0701022fc936b5c6d301e0cd702
YUSHUI_WINDOW=p24-p30
DAHAN_WINDOW=p799-p805
RENDER_DPI=330
OCR_USED_FOR_FINAL_GLYPH_CLAIMS=false
```

## 3. p27 — 雨水 block and source-label typography

```text
PAGE_SHA256=ec9b5aeb747c6a6a14a80923a1e1f0f4a56c8feb2db0ef303147b0b710638513
```

The target block physically preserves the already-controlled sequence:

```text
雨水日日在危九度
晝四十七刻夜五十三刻
後四日
晝四十八刻夜五十二刻
```

At the end/boundary of that block, before the solar-term diagram material, the page directly prints the small vertical source name:

```text
通書
```

The following diagram captions identify the solar-term day/night diagrams, including:

```text
立春正月節日出入并晝夜長短之圖
雨水正月中日出入并晝夜長短之圖
```

Crucially, this page supplies an internal typographic control: an earlier phenology quotation ends with the same kind of small source-name treatment `汲冢周書`. Therefore the small `通書` is not treated as ordinary running text or a modern transcription insertion; it belongs to the compilation's source-attribution apparatus at this block boundary.

## 4. p802 — 大寒 block independently repeats the same structure

```text
PAGE_SHA256=ab6aeac3f163bd732cf92bc8639daee2a40c95b2671dad69c6653119d29f417e
```

The target block physically preserves:

```text
小寒日日在斗十二度
大寒日日在牛初度
晝四十三刻夜五十七刻
十三後晝四十四刻夜五十六刻
```

Again, the small vertical source label at the end/boundary of the block is:

```text
通書
```

and it is immediately followed by the Xiaohan/Dahan day/night diagram material:

```text
小寒十二月節日出入并晝夜長短之圖
大寒十二月中日出入并晝夜長短之圖
```

The January and December loci therefore independently reproduce the same source-label architecture.

## 5. What “通書” now proves — and what it does not

The source-layer adjudication can now be strengthened from:

```text
COMMON_TONGSHU_SUBSTRATE=PLAUSIBLE
```

to:

```text
YUELING_1589_TARGET_MATERIAL_GENERIC_TONGSHU_SOURCE_LABEL=PHYSICALLY_BOUND
```

But `通書` is a generic source label here. It does **not** by itself prove:

```text
通書 = 熊宗立《類編曆法通書大全》
通書 = 1455《四時氣候集解》所引通書
通書 = one single invariant table family
通書 physical source date < 1578
通書 -> Sanming direct copying
```

This firewall matters because the already reviewed 1455 coarse Tongshu branch has summer-solstice 60/40, whereas exact Sanming 1578 has 59/41. A shared generic source label cannot erase a direct numeric mismatch between distinct Tongshu branches.

## 6. Transmission consequence

The best-supported model is now narrower:

```text
1589 Yueling exact fingerprint
        |
        | explicit physical source label
        v
generic 通書 source family
        |
        | exact title / recension / date unresolved
        ?
possible earlier carrier shared with or antecedent to Sanming
```

Because Yueling 1589 postdates Sanming 1578 by eleven years, chronology still permits multiple directions:

- a Tongshu source older than both;
- an intermediate Tongshu recension formed after 1578;
- Sanming-derived material entering a Tongshu/Yueling transmission line;
- parallel inheritance from another calendar/almanac source.

Therefore no direct ancestor edge into Sanming is promoted.

## 7. Search-space reduction

The next documentary search is no longer “any calendar text with similar numbers.” It should prioritize **pre-1578 Tongshu/almanac recensions** and their upstream compilation lines, while preserving branch separation.

High-value targets include:

1. pre-1578 `通書` witnesses carrying both `大寒十三後` and `雨水後四日`;
2. the upstream relationships among 熊宗立-family `通書大全`, earlier `通書` compilations, and Nanjing/Datong day-length materials;
3. a source that combines the exact 59/41 cap with the exact change-day fingerprint;
4. the historical reduction/threshold rule that can generate that table from a finer daily numerical substrate.

## 8. Product adjudication

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
HPA_ZDATE_006=MISSING_FROM_PRODUCT
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=12
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=12
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

No runtime candidate is selected or collapsed.

Research record: `docs/research/ZIWEI-YUELING-TONGKAO-1589-TONGSHU-SOURCE-LABEL-SCOPE-R1.json`.
