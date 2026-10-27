# Batch 12CY — 《虎鈐經·傳箭》換檔日指紋 × 1578《三命通會》直接比較

## Status

```text
HUQIAN_PRE1578_INTEGER_STEP_CHANGE_DAY_FAMILY=CONFIRMED
HUQIAN_DECISIVE_CHANGE_DAYS_CROSS_RECENSION_STABLE=CONFIRMED
HUQIAN_EXACT_CHANGE_DAY_FINGERPRINT_EQUALS_SANMING_1578=FALSE
DIRECT_UNCHANGED_HUQIAN_TABLE_PARENT_SHORTCUT=DISPROVED
HUQIAN_STRUCTURAL_ANCESTRY_CANDIDATE=RETAINED
SANMING_POST_CONVERSION_REDUCTION_LAYER=STILL_UNRESOLVED
HPA_ZDATE_006=MISSING_FROM_PRODUCT
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
```

## 1. Why this follows Batch 12CX

Batch 12CX directly established that the reviewed `《元史·授時曆》` day/night conversion retains sub-ke remainders as `分` and describes the result as `晝刻及分秒`. Therefore the 1578 `《三命通會》` whole-ke seasonal display cannot be explained by simply discarding the remainder inside that reviewed Shoushi conversion step.

The next gate is downstream integer reduction/change-day logic. `《虎鈐經·傳箭》` is unusually valuable because it does not merely print 40/60-style integer pairs: it explicitly states *when* the arrow is changed inside a solar term.

Batch 12CJ already proved the core Huqian arrow family is stable across a Tianyige Ming print and a later Siku-recension physical witness. This batch reuses those archived physical artifacts and asks a narrower question: do its **change days** reproduce the distinctive 1578 Sanming fingerprint?

## 2. Reused physical witnesses; no new OCR authority

### Tianyige Ming print

Prior acquisition:

```text
RUN=34832306143
ARTIFACT=10342711240
SOURCE=EXT-TIANYIGE-HUQIANJING-MING-CHUANJIAN
OCR_USED_FOR_GLYPH_CLAIMS=false
```

Directly re-reviewed pages:

```text
p74 sha256=a86cade9b99ed1b5cc943370e4b66e914d7968bc08943225bb99530fb15721ab
p75 sha256=cc7546f4d93b85fb0327e30cead9c994ae017d81dc2f1dd1b86e994babb3cf83
```

### CADAL / Siku-recension witness

Prior acquisition:

```text
RUN=34933201296
ARTIFACT=10382093979
SOURCE=EXT-CADAL-HUQIANJING-SIKU-CHUANJIAN
OCR_USED_FOR_GLYPH_CLAIMS=false
```

Directly re-reviewed pages:

```text
p15 sha256=b6381ac14f6479163b2c2a10ac59b2c6f773aac44c613818eab950ff50402883
p16 sha256=e1fcd26c6d2749c0d627204c00fda4a3cdcb90525095b6cb380bb6642d61b0ef
```

The two surviving witnesses are not treated as two votes for direct Sanming ancestry. Their value here is narrower: they independently preserve the decisive Huqian change-day wording, making a late Siku-only corruption explanation substantially less plausible for these loci.

## 3. Direct Huqian change-day fingerprint

Across the reviewed physical witnesses the mechanically relevant sequence is stable:

```text
大寒後三日改第五箭 -> 晝44 / 夜56

雨水初日改第八箭 -> 晝47 / 夜53
後第九日改第九箭 -> 晝48 / 夜52
```

The CADAL/Siku physical pages additionally preserve the nearby controls:

```text
驚蟄後三日改第十箭 -> 49/51
春分前三日改第十一箭 -> 50/50
後六日改第十二箭 -> 51/49
```

These readings strengthen Batch 12CJ's conclusion that Huqian is an operational integer-step/change-day system, not merely a list of seasonal extrema.

## 4. Exact 1578 Sanming target

Batch 12CP already fixed the 1578 NCL-06589-1 physical target at pp134–136. The relevant loci are:

```text
大寒 -> 43/57
physical sequence 十三後日 -> 44/56

雨水 -> 47/53
後四日 -> 48/52

驚蟄 -> 49/51
春分 -> 51/49
夏至 -> 59/41
```

Philological firewall:

```text
1578 physical 十三後日 is preserved literally.
It is not silently normalized into 後三日, 十三日後, or any modernized threshold.
```

## 5. Fingerprint comparison

| locus | Huqian physical rule | Sanming 1578 physical rule | result |
|---|---|---|---|
| change to 44/56 around 大寒 | 大寒後三日 | literal 十三後日 after 大寒 43/57 | mismatch |
| 雨水 47/53 -> 48/52 | 雨水初日 47/53; 後第九日 48/52 | 雨水 47/53; 後四日 48/52 | mismatch |
| 春分 neighborhood | 春分前三日 50/50; 後六日 51/49 | 春分 51/49 | anchor mismatch |
| summer cap | 夏至前三日 60/40 | 夏至 59/41 | extreme + anchor mismatch |

This is stronger than the earlier observation that the two tables have different solstitial extrema. The **internal transition fingerprint itself** is different.

## 6. Historical adjudication

The evidence now supports all of the following simultaneously:

```text
A. Pre-1578 integer one-ke seasonal stepping is old and operationally explicit.
B. Intra-term change-day instructions are also old, not a Sanming invention.
C. Huqian's reviewed change-day schedule is stable across a Ming print and a Siku-recension witness.
D. That stable Huqian schedule is NOT the exact 1578 Sanming schedule.
```

Therefore the shortcut

```text
Huqian Chuanjian table
  -> verbatim/direct unchanged mechanical parent
  -> Sanming 1578 seasonal table
```

is disproved.

This does **not** disprove broader ancestry. The safe model remains composite:

```text
older integer-arrow / seasonal-step operational family
  + Ming Nanjing/Datong regional numerical calibration
  + unresolved downstream reduction / change-day recomposition
  -> 1578 Sanming displayed integer ladder
```

Huqian therefore remains a strong structural-ancestry candidate, but the missing historical object is now more narrowly defined: a source or rule that modifies/recalibrates the older change-day ladder into the Sanming fingerprint.

## 7. Transmission impact

Strengthened:

- `RULE-FAMILY-HUQIANJING-CHUANJIAN-20ARROW-40-60`
- the evidence scope of `TG-E0009` / `TG-E0010`
- `TG-E0011` as **structural**, not exact-table ancestry

New explicit non-edge:

```text
RULE-FAMILY-HUQIANJING-CHUANJIAN-20ARROW-40-60
  DIRECT_CHANGE_DAY_TABLE_PARENT_OF
TABLE-SANMING-1578-DAYNIGHT-KE
  = DISPROVED as unchanged table identity
```

No direct-copy direction from the Tianyige or Siku physical copy into Wan Minying is inferred.

## 8. Product adjudication

This is provenance/genealogy work only.

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

No runtime candidate, winner, candidate collapse, or algorithm reopen is authorized.

## 9. Next gate

The search should now target a narrower class of pre-1578 Chinese evidence:

1. a Huqian-like integer step/change-day table already recalibrated to a **59-ke Nanjing/Datong cap**;
2. a rule that transforms precise C-II-N daily values into the exact Sanming thresholds, especially the literal `大寒 十三後日` locus and `雨水 後四日`;
3. an independent Chinese physical C-II-N carrier, so Chinese origin and Joseon transmission remain distinct.

Research record: `docs/research/ZIWEI-HUQIANJING-CHANGE-DAY-FINGERPRINT-SANMING-COMPARISON-R1.json`.
