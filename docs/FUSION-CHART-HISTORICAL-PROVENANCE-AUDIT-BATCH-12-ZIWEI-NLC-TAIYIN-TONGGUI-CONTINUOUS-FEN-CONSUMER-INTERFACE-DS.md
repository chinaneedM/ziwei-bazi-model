# Fusion Chart Historical Provenance Audit R1 — Batch 12DS

## 國圖成化《太陰通軌》晨昏分局部消費接口：全分直用與整刻層排除

Status: **DIRECT P12–P24 INTERFACE REVIEW CLOSED / 晨分與昏分「全錄」並以「全分為法」直接參與月行計算 / C-II-N FRACTIONAL SUBSTRATE IS CONSUMED WITHOUT AN ATTESTED WHOLE-KE PRE-REDUCTION AT THIS LOCAL INTERFACE / NO FLOOR-NEAREST-CEILING-CHANGE-ARROW-59KE BINDING INSTRUCTION OBSERVED IN REVIEWED SCOPE / OBJECT-SCOPED NONATTESTATION ONLY / ZERO EXACT SANMING-PARENT VOTE / NO RUNTIME CHANGE / NO ALGORITHM REOPEN**

## 1. Why this batch

12DR closed the Chinese pre-1578 physical carrier of the C-II-N `晨分/昏分` table in NLC object `411999012050《太陰通軌》`.

The next question is no longer merely whether the table exists, but **how this manuscript actually consumes those values**:

```text
continuous 晨分 / 昏分
    -> ?
whole-ke day/night display
```

12DS reviews the directly adjacent calculation interface, not just the numerical table.

## 2. Evidence scope

Physical source:

```text
NLC object 411999012050
《太陰通軌》
volume 2
reviewed PDF pages 12–24
```

Final glyph/mechanism claims are based on direct image review. OCR is not used as final authority.

The reviewed range deliberately includes:

- the morning-consumption method before the table;
- the evening-consumption method before the table;
- the `冬夏二至日出晨昏分立成鈐` itself;
- the first method immediately following the table.

This is sufficient to adjudicate the **local interface around the table**. It is not used as a whole-work negative.

## 3. Morning side: the fractional value is explicitly copied in full

Volume 2 PDF p12 directly heads:

```text
推第十格晨入轉日并晨分及晨轉度分法
```

The physical manuscript then states:

```text
晨分者就將元加之晨分全錄於晨日同格為各推得之晨分也
```

and immediately uses it as:

```text
晨轉度分者置各第八格推得遲疾轉定度全分
以其本格推得晨分全分為法
```

The important mechanism is positive, not merely an absence:

```text
晨分 -> 全錄
晨分全分 -> directly used as the calculation basis
```

No intervening whole-ke conversion is written in this local interface.

Physical control:

```text
vol2-12.jpg
sha256=7af238834a551e79f45133f4e683b5d6cde27d75d51562a9e0e983e812ea3bd7
```

## 4. Evening side: the same full-fraction logic is symmetric

Volume 2 PDF p14 directly heads:

```text
推第十二格昏入轉日并昏分及昏轉度分法
```

The evening branch states:

```text
昏分者就將元加之昏分全錄於昏日同格為各推得昏分也
```

and then:

```text
昏轉度分者亦置其第八格推得遲疾轉定度全分
以其本格推得昏分全分為法
```

So both sides preserve the same interface:

```text
晨分/昏分 fractional value
    -> copy full value
    -> consume full value in lunar turn-degree computation
```

Physical control:

```text
vol2-14.jpg
sha256=0bbed80c9f1bce507c7b472cdf6a4f45971f47d6450105cda130220ce326e4c2
```

## 5. Table and post-table boundary

Volume 2 p15 starts the directly reviewed table:

```text
冬夏二至日出晨昏分立成鈐
```

Its initial winter pair remains:

```text
晨分 2681.70
昏分 7318.30
```

These are fractional `分` values, not displayed whole `刻`.

The continuous table continues through the reviewed p15–p24 range. On p24, immediately after the table, the manuscript resumes:

```text
推第十四格相距度分并轉積度分法
```

That is again a lunar relative-distance / turn-accumulation calculation. No inserted whole-ke conversion step is physically observed between the `晨昏分` table and the surrounding consumer calculations.

Physical controls:

```text
vol2-15.jpg sha256=5fe45f2483dd7f5a4e92506845cec74bd72901dae3f62e59de24fd1ef7b4016b
vol2-24.jpg sha256=6cfdbc58a0c0f98300c8b76a7ea2b446a22e23a3a42e87b52b750dd3a50e4c1d
```

## 6. Mechanism adjudication

For the directly reviewed p12–p24 interface:

```text
晨分 full fractional value copied directly       = YES
昏分 full fractional value copied directly       = YES
fractional values consumed in lunar computation  = YES

whole-ke rounding instruction                     = NOT ATTESTED
floor instruction                                 = NOT ATTESTED
nearest-integer instruction                       = NOT ATTESTED
ceiling instruction                               = NOT ATTESTED
改箭 / clepsydra-arrow selection                  = NOT ATTESTED
explicit Nanjing 59-ke endpoint binding           = NOT ATTESTED
Sanming/Yueling exact change-day fingerprint      = NOT ATTESTED
```

This is an **object-scoped local-interface result** only.

It does not prove those rules never occur elsewhere in `大統曆法通軌`, Tongshu/almanac literature or institutional clepsydra practice.

## 7. Consequence for the 12DQ composite model

12DQ already showed that one global constant fractional threshold cannot map the C-II-N interior and the 59-ke endpoint simultaneously.

12DS now adds a separate positive constraint:

> At this Chinese pre-1578 Taiyin calculation interface, the continuous `晨分/昏分` are retained and consumed as full fractional values.

Therefore the missing Sanming whole-ke layer should not be silently inserted into this exact local calculation step.

The remaining historical possibilities are narrower:

```text
continuous C-II-N substrate
    -> local Taiyin consumer keeps full fractions
    -> [missing layer elsewhere]
       - Tongshu/almanac table recomposition
       - clepsydra / 改箭 institutional selection
       - another Datong/Tonggui section
       - editorial selection/recomposition
    -> whole-ke 42..59 display
```

No winner is selected.

## 8. Locator-only received transcription control

The modern transcription surface for the same object was used only as a locator/reading aid. Searches for:

```text
刻 / 百刻 / 漏 / 箭 / 晝夜 / 半晝
```

returned no match in the reviewed search surface.

This contributes **zero independent negative authority**. The 12DS conclusion rests on direct physical scope and the positive `全錄 / 全分為法` wording.

## 9. Product adjudication

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
HPA-ZDATE-006=MISSING_FROM_PRODUCT
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=12
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=12
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

No runtime candidate, no winner and no algorithm reopen.

## 10. Next gate

The missing whole-ke layer is now more tightly localized outside this p12–p24 Taiyin consumer interface:

1. search other Chinese pre-1578 Datong/Tonggui material for explicit whole-ke reduction / binning / `改箭` / endpoint-binding instructions;
2. prioritize Tongshu/almanac and clepsydra sources that can connect C-II-N to the Nanjing 59-ke institutional endpoint;
3. continue exact `大寒十三後 / 雨水後四日` fingerprint search;
4. locate and physically collate the separately reported NLC three-juan `《大統曆法通軌》`.

Research record: `docs/research/ZIWEI-NLC-TAIYIN-TONGGUI-CONTINUOUS-FEN-CONSUMER-INTERFACE-R1.json`.
