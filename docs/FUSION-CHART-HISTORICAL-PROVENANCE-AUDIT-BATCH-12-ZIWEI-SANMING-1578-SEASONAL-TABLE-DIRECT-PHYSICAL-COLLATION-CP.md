# Batch 12CP — 1578《三命通會》季节晝夜刻表原刻物理闭合

## Status

```text
1578_SANMING_SEASONAL_TARGET_TABLE_PHYSICAL_LAYER=CLOSED
OCR_GLYPH_AUTHORITY=false
SUMMER_SOLSTICE_59_41=DIRECT_PHYSICAL_ATTESTATION
SELECTED_INTRA_TERM_STEPS=DIRECT_PHYSICAL_ATTESTATION
PRE1578_EXACT_PARENT=UNRESOLVED
PRE1578_SAME_CHANGE_DAY_FINGERPRINT=UNRESOLVED
EXACT_HISTORICAL_QUANTIZATION_RULE=UNRESOLVED
SUKU_RECEIVED_TEXT_NOT_EXACT_1578_SURROGATE=true
HPA_ZDATE_006=MISSING_FROM_PRODUCT
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
```

## 1. Why this batch exists

Batch 12CO corrected the KOSTMA `DIC_A3_000150` attribution and therefore reopened one part of the pre-1578 Datong day/night-table bridge. At the same time, the current ancestry work still depended on a distinction that had not been made explicit enough:

1. what the **1578 target table itself physically says**; versus
2. what earlier numerical/table tradition generated it.

Batch 12AT had already bound the exact NCL 1578 physical object and directly collated `論日刻` / `論時刻` / the birth-time caution, but its decisive seasonal-table pages were not the focus. Batch 12CG then reconstructed a plausible numerical substrate from `大統日出分`, and Batch 12CI established a separate earlier precision/coarse structural ancestry candidate. Those batches intentionally left exact parentage, change-day ancestry and quantization open.

Before continuing that ancestry search, this batch closes the target side at physical-page level.

## 2. Exact physical source and machine gate

The source is the same exact 1578 object already controlled in Batch 12AT:

```text
WORK=三命通會
AUTHOR=萬民英
EDITION=明萬曆戊寅（六年，1578）刊本
SOURCE_ID=NCL-06589-1
PDF_SHA256=3de5c45efb1919965afae00a3c97121054aaabd0f38f9fd5ab8f0a28bb8e36dd
```

A new targeted physical gate was added because the previous coarse locator began its rendered candidate window at PDF p135 while the critical winter/spring ladder already begins on p134.

```text
WORKFLOW_RUN=35074754104
ARTIFACT=10437955655
ARTIFACT_DIGEST=sha256:bcb11ee8e8fe384d36fccd9439a6942391ea0cef296ef134378334ec41cfc638
OCR_USED_FOR_LOCALIZATION_IN_THIS_GATE=false
OCR_USED_FOR_GLYPH_CLAIMS=false
```

The targeted gate renders only the exact physical leaves p134–136 at 220 dpi and binds them by SHA-256:

```text
p134 = 0baaa3ec9f615a7f867c4cea2770d423d92485d8127417b2c7bb0cc7898635aa
p135 = 622dfb58c615e7eec1553d0f667934c35768fa822a4e3dd9f1bfa4844b72bca0
p136 = abe0e129ace60f8cf29395f1f086972b17da8383ca20c3ab8323d3fd5ff42c59
```

Machine locator:

`docs/research/SANMING-TONGHUI-1578-SEASONAL-TABLE-PHYSICAL-LOCATOR-R1.json`

All textual conclusions below come from direct visual review of those physical renders. OCR is not used as final glyph evidence.

## 3. Direct physical table: p134

The physical leaf directly fixes the winter-to-spring ladder. The mechanically relevant day/night-ke values are:

| locus | direct physical value |
|---|---|
| 小寒 | 晝四十二刻 / 夜五十八刻 |
| 大寒 | 晝四十三刻 / 夜五十七刻 |
| 大寒后续 | physical sequence `十三後日` followed by 晝四十四刻 / 夜五十六刻 |
| 立春 | 晝四十五刻 / 夜五十五刻 |
| 雨水 | 晝四十七刻 / 夜五十三刻 |
| 雨水后续 | `後四日` followed by 晝四十八刻 / 夜五十二刻 |
| 驚蟄 | 晝四十九刻 / 夜五十一刻 |
| 春分 | 晝五十一刻 / 夜四十九刻 |

Two philological firewalls are important.

First, the physical sequence around the Dahan transition is preserved as printed: `十三後日`. This batch does **not** silently rewrite the order into a modernized instruction merely to make the threshold easier to state.

Second, the table is not a simple list of one fixed integer pair per solar term. It contains intra-term timing instructions and explicit secondary integer states. Therefore any proposed ancestor must reproduce more than just the extrema `59/41` and `42/58`; the change structure matters.

## 4. Direct physical table: p135

The spring-to-summer and early-autumn leaf continues:

| locus | direct physical value |
|---|---|
| 清明 | 53 / 47 |
| 穀雨 | 55 / 45 |
| 立夏 | 56 / 44 |
| 小滿 | 58 / 42 |
| 夏至 | 59 / 41 |
| 小暑 | 58 / 42 |
| 大暑 | 57 / 43 |
| 立秋 | 56 / 44 |

For `芒種`, the physical locus states `其晝夜本無節`. This batch does not infer an explicit day/night pair from adjacent entries when the leaf itself does not print one there.

The summer-solstice endpoint is therefore no longer merely a received-text or reconstructed target value in the current ancestry work:

```text
1578 三命通會 physical p135
夏至 -> 晝五十九刻 / 夜四十一刻
```

This is the exact target against which earlier Nanjing/Datong witnesses must be compared.

## 5. Direct physical table: p136

The later-year sequence directly shows:

| locus | direct physical value |
|---|---|
| 處暑 | 54 / 46 |
| 白露 | 52 / 48 |
| 秋分 | 50 / 50 |
| 寒露 | 48 / 52 |
| 霜降 | 46 / 54 |
| 立冬 | 44 / 56 |
| 小雪 | 42 / 58 |

This confirms that the 1578 display is not merely a symmetric `40↔60` coarse table. Its extrema, intermediate integers and intra-term transitions are a distinct target fingerprint requiring its own ancestry reconstruction.

## 6. Received-text control: numerical stability does not imply exact recension identity

The repository already registers `EXT-CTEXT-SMTHE-SIKU-V2` as a received Siku control. Its day/night-ke ladder broadly agrees with the 1578 physical target, but the physical p134 also exposes multiple astronomical-position wording differences.

Examples from direct 1578 physical review versus the received Siku control include:

```text
冬至:
  1578 physical -> 今在箕六度
  Siku received -> 今在箕三度

立春:
  1578 physical -> 日在虛二度
  Siku received -> 日在危三度今在女六度

雨水:
  1578 physical -> 日在危九度
  Siku received -> 日在危六度今在尾初度

驚蟄:
  1578 physical -> 日在室八度
  Siku received -> 日在空八度今在危十五度
```

The safe conclusion is deliberately narrow:

```text
Siku received text can corroborate parts of the ke ladder.
Siku received text is NOT an exact surrogate for the 1578 physical wording.
```

This does not by itself prove a complete stemma, identify the direction of alteration, or turn the astronomical-position differences into a different timekeeping algorithm. It only blocks the invalid shortcut of using the later received transcription as though every target glyph were identical to the 1578 impression.

## 7. Relationship to the existing numerical ancestry chain

### 7.1 Batch 12CG remains valid but scoped

Batch 12CG directly bound `NCL-06267 大統日出分` to a 1380s Nanjing daily table family and showed that the daily half-day curve mechanically spans the Sanming integer range. It also preserved an older intra-term integer-bin tradition.

Batch 12CP strengthens the **target side** of that comparison. It does not prove:

```text
NCL-06267 -> 三命通會 direct copying
nearest-integer rounding -> Wan Minying's rule
exact Sanming transition days -> recovered from the daily table
```

### 7.2 Batch 12CI remains a structural-ancestry candidate, not a generator of Sanming

Batch 12CI showed a 24/24 quantization compatibility between the recorded 1010 Han Xianfu precision table and a separate Ming coarse `40↔60` family, while rejecting ordinary modern 0.5 rounding for that coarse table.

The direct 1578 Sanming physical table still contains a different fingerprint. Therefore no newly closed p134–136 glyph authorizes collapsing the two table families.

### 7.3 Batch 12CO remains the current warning against metadata shortcutting

Batch 12CO proved that `DIC_A3_000150 / 大統曆日通軌` had been over-described by the prior batch and repaired the source-emitted Kyujanggak identifier to `GK12437_00`. The pre-1578 Datong-line day/night table must therefore still be established from page-level cells or an explicit table field, not from a generic catalog description.

## 8. New external search signal after 12CO

A fresh search of the received `《明史·曆志》` route confirms a useful mechanical locator statement for `大統曆通軌`: its `晨昏分` layer can generate the other quantities by formula — add 250 fen to dawn for sunrise; derive dusk from the 10,000-fen day; subtract 250 for sunset; subtract another 5,000 for half-daylight. The same received passage explicitly says that only `晨昏分` need be listed because sunrise/sunset/half-daylight are thereby determined.

This is useful for the next search because a pre-1578 source does **not** need to carry a literal heading `晝夜刻分表` to contain the required numerical substrate. But this batch does not promote the received Ming-history prose into an observed physical `大統曆通軌` table cell. Direct page-level witness remains the gate.

## 9. Transmission impact

```text
nodes strengthened:
  - NCL-06589-1 1578 physical witness, seasonal passage pp134-136
  - 1578 Sanming seasonal integer-ke target artifact

edge supported:
  - 1578 physical copy ATTESTS the seasonal integer-ke ladder

edges not upgraded:
  - NCL-06267 Datong daily table -> Sanming direct transmission
  - Song precision / Ming coarse table -> Sanming direct transmission
  - Siku received wording -> exact 1578 recension identity
```

No direct lineage winner is selected. The graph model remains composite and evidence-scoped.

## 10. Product adjudication

Nothing in this batch supplies the Fullbook-specific transformation:

```text
上五刻 -> 昨夜亥時
```

Therefore:

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
UPPER_ZI_TO_HAI_VOTE_INCREMENT=0
NEW_RUNTIME_CANDIDATE=false
RUNTIME_WINNER=false
CANDIDATE_COLLAPSE=false
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Audit accounting remains:

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
CUMULATIVE_IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
PROVENANCE_METADATA_DEFECTS=12/12_REPAIRED
CHART_ALGORITHM_DEFECTS=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
```

## 11. Next gate

The next research priority remains ancestry rather than target reconstruction:

1. continue direct `大統曆通軌 / 大統曆日通軌` `晨昏立成` witness search, now allowing for the possibility that `日出 / 日入 / 半晝` are mechanically implicit in `晨昏分` rather than separately titled;
2. continue pre-1578 annual Datong almanac and related table searches for both the Nanjing `59/41` cap and the Sanming intra-term change fingerprint;
3. audit the Yang Zan / related route already named in current state, with exact title/person/object binding before using it;
4. keep the Fullbook `上五刻 -> 昨夜亥時` lineage independent from this seasonal-table ancestry work.

Research record:

`docs/research/ZIWEI-SANMING-1578-SEASONAL-TABLE-DIRECT-PHYSICAL-COLLATION-R1.json`
