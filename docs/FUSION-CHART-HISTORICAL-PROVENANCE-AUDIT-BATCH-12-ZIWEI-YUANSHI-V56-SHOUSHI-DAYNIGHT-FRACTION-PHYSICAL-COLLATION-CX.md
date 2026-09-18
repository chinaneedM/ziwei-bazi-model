# Batch 12CX — 《元史》卷56授時曆晝夜刻分秒規則實物定位：精細換算不丟餘數

## Status

```text
YUANSHI_V56_FRACTION_RULE_FACSIMILE_LOCATOR=CLOSED
REVIEWED_RECENSION=QING_SIKU_RECEIVED_RECENSION
PRE1578_PHYSICAL_WITNESS=false
RECEIVED_SHOUSHI_DAYNIGHT_CONVERSION_RETAINS_SUBKE_REMAINDER=true
SIMPLE_REMAINDER_DISCARD_AT_SHOUSHI_CONVERSION=DISPROVED_FOR_REVIEWED_RECEIVED_RECENSION
SANMING_INTEGER_DISPLAY_REQUIRES_SEPARATE_OR_DOWNSTREAM_REDUCTION_LAYER=true
EXACT_SANMING_QUANTIZATION_CHANGE_DAY_RULE=UNRESOLVED
DIRECT_SANMING_PARENT=UNRESOLVED
HPA_ZDATE_006=MISSING_FROM_PRODUCT
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
```

## 1. Trigger

Batch 12CW closed the raw `授時曆立成` Beijing/Yandu Type-II numerical branch and showed that its summer value `61.8408` ke cannot be equated with the 1578 `《三命通會》` summer-solstice display `59/41`.

That left the highest-value bottleneck at the **reduction layer**: when precise daily `晨昏 / 日出入 / 半晝` values are converted into day/night ke, does the Shoushi procedure itself discard the fractional remainder, or is the whole-ke display created later?

The already-committed exact-head workflow now provides a complete 156-page facsimile surface for `《元史》卷五十五~卷五十六`, allowing that question to be answered directly at the reviewed recension layer.

## 2. Source and date firewall

Acquisition:

```text
WORKFLOW_RUN=35326506325
WORKFLOW_JOB=105540679987
ARTIFACT=10539204266
ARTIFACT_NAME=yuanshi-v55-56-daynight-fraction-rule
ARTIFACT_DIGEST=sha256:4f2ec714855b2d8f99887088c7ccc508bd49318fc9843a33b95b82c9ea386914
SOURCE_DJVU_SHA256=6abcfe75ea823aa5a5548fe51a889256ae55949592b7ebe7739c42958beb96db
RENDERED_PAGES=156/156
OCR_USED_FOR_FINAL_GLYPH_CLAIMS=false
```

The reviewed object is `CADAL06056892 元史·卷五十五~卷五十六`, and the facsimile visibly belongs to the `欽定四庫全書` received-recension presentation.

The following dates/levels must remain separate:

```text
Yuan Shoushi technical rule layer
!= Yuan-shi work-text compilation layer
!= Qing Qinding Siku Quanshu received-recension layer
!= exact physical exemplar/impression underlying the CADAL scan
!= modern CADAL/Wikimedia digital-surrogate layer
```

Therefore this batch **does not** call the reviewed scan a pre-1578 physical witness. It is direct facsimile evidence for a later received recension of an earlier rule text.

## 3. Direct facsimile page 123: target procedure begins

Rendered page `123.jpg`:

```text
SHA256=f37742072ae4e70e9e948060a7a1ab2d27914fd7eee4529ecb3d4e9c7c10cd87
```

Direct no-OCR review visibly reads the section heading:

```text
求每日日出入晨昏半晝分
```

and then:

```text
求日出入辰刻
```

This establishes the immediate procedural context for the following page.

## 4. Direct facsimile page 124: remainder is retained

Rendered page `124.jpg`:

```text
SHA256=3277b5fed27a758b75de6c2ba2573c34571393827273302c6f9d56f6ebde6f0d
```

The continuation of the sunrise/sunset conversion visibly includes:

```text
除之為刻不滿為分命子正算外即得所求
```

The next heading is:

```text
求晝夜刻
```

and the rule visibly reads:

```text
置日出分十二乘之刻法而一為刻不滿為分即為夜刻覆減一百餘為晝刻及分秒
```

The critical mechanical facts are therefore direct:

1. an incomplete quotient is retained as `分`;
2. the day/night result is explicitly described at `刻及分秒` resolution;
3. this reviewed Shoushi conversion layer is **not** a simple whole-ke remainder-discard operation.

## 5. Consequence for the 1578 Sanming reduction problem

The evidence now rejects one shortcut:

```text
precise Shoushi daily value
  -> apply received Yuan-shi day/night conversion
  -> discard all sub-ke remainder at that same conversion step
  -> directly obtain Sanming whole-ke display
```

That shortcut is incompatible with the reviewed rule, because the rule explicitly preserves the remainder.

The mechanically admissible model is narrower:

```text
precise daily astronomical/timekeeping value
  -> Shoushi-style conversion retaining ke + fractional resolution
  -> [separate/downstream integer selection, binning, table abstraction or editorial reduction]
  -> 1578 Sanming displayed whole-ke ladder
```

The bracketed layer is **required as a mechanical inference**, but this batch does not identify its historical author, source, threshold, change-day convention or exact textual carrier.

In particular, the following remain open:

- why the 1578 physical table changes `大寒 43/57` after the printed `十三後日` instruction;
- why `雨水 47/53` changes after `後四日`;
- the exact rule converting the Nanjing Datong C-II-N daily curve into the Sanming displayed integers;
- direct parentage into Wan Minying's table.

## 6. Transmission impact

New graph nodes:

- `DIGITAL-SURROGATE-CADAL06056892-YUANSHI-V55-56-SIKU`;
- `RULE-YUANSHI-V56-SHOUSHI-DAYNIGHT-FRACTION-RETENTION`.

New graph results:

- the CADAL/Siku surrogate **ATTESTS** the received Shoushi fraction-retention rule;
- that rule **DISPROVES_LINEAGE_SHORTCUT** to a same-step whole-ke truncation explanation for the 1578 Sanming display.

This strengthens the existing composite-transmission hypothesis while keeping the missing reduction layer explicit.

No claim is made that the reviewed Siku physical recension is itself an ancestor of the 1578 print.

## 7. Product adjudication

This is a provenance / philology / transmission-layer refinement only.

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
HPA_ZDATE_006=MISSING_FROM_PRODUCT
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

No deterministic chart code or runtime profile changes.

## 8. Next gate

1. find a securely pre-1578 **Chinese** witness that explicitly performs or states the post-conversion whole-ke reduction/binning/change-day rule;
2. mechanically replay any such rule against the exact 1578 `大寒十三後日` and `雨水後四日` transitions using the Nanjing Datong C-II-N daily curve;
3. continue the independent Chinese physical C-II-N witness search so Chinese origin and Joseon transmission remain distinguished;
4. separately close the six older G893 page-specific controls from the complete G893 image sequence, without contaminating the Sanming reduction question.

Research record: `docs/research/ZIWEI-YUANSHI-V56-SHOUSHI-DAYNIGHT-FRACTION-PHYSICAL-COLLATION-R1.json`
