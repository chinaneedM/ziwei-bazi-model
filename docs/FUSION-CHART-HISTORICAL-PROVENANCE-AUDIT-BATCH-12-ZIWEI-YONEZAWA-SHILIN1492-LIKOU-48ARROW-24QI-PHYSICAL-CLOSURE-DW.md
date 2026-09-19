# Fusion Chart Historical Provenance Audit R1 — Batch 12DW

## 米沢弘治五年《事林廣記》：1492 實體本 48 箭 / 24 氣漏刻機制閉合

Status: **SECURE PRE-1578 PHYSICAL PRINT WITNESS CLOSED / 48 ARROWS + TWO ARROWS PER QI + 24-QI + 2.5-FEN-PER-QI + WINTER-INCREASE/SUMMER-DECREASE DIRECTLY VISIBLE / SAME 1492 COPY RETAINS 40↔60 COARSE EXTREMA / 59↔41 NANJING ENDPOINT NOT PRESENT AT REVIEWED LOCUS / EXACT WITHIN-QI CHANGE-DAY RULE UNRESOLVED / EXACT 大寒十三後・雨水後四日 FINGERPRINT UNRESOLVED / ZERO DIRECT SANMING-PARENT VOTE / NO RUNTIME CHANGE / NO ALGORITHM REOPEN**

## 1. Why this batch

Batch 12DV closed a calendar/solar-term-to-discrete-arrow selection mechanism in a reviewed Qing 1823 physical recension. The remaining chronology gate was a securely pre-1578 physical carrier.

The Yonezawa first-party catalog supplies such a carrier:

```text
米沢善本60
管理番号 AA060001
《群書類要事林廣記》十二卷
刊本　詹氏進徳精舎刊本
弘治5年（1492）刊
12巻・12冊 / 375丁
```

This batch asks only what the 1492 object itself visibly attests.

## 2. First-party route and physical acquisition

```text
ROUTE_PROBE_RUN=35439896355
ROUTE_PROBE_ARTIFACT=10583615625
ROUTE_PROBE_DIGEST=sha256:48daba78184a60b8e7f3afda80b3789ad8614879efcb24e781bbc3ad89c419d7

PHYSICAL_PAGE_RUN=35440299002
PHYSICAL_PAGE_JOB=105889826159
PHYSICAL_PAGE_ARTIFACT=10583821131
PHYSICAL_PAGE_DIGEST=sha256:126b756814bfb1dbde6cd536b2a45398f746e8b0f82231801557ec9e4fb54782
ACQUIRED_PAGE_COUNT=48
OCR_LOCATOR_HITS=0
OCR_USED_FOR_FINAL_GLYPH_NUMERIC_OR_MECHANISM_CLAIMS=false
```

OCR failed as a locator and is not evidence. Final readings below are direct visual readings of source-bound first-party JPEGs.

## 3. AA060001_015 — direct 100-ke / 40↔60 control

```text
URL=https://www.library.yonezawa.yamagata.jp/dg/data/AA060/001/AA060001_015.jpg
SHA256=ebbf7717500d3ef2dd07b77f1f44bcaed235c321bf68ff9d89c500bf26f31d3a

古制蓮漏之圖
刻漏制
成周挈壺氏以百刻分晝夜
冬至晝四十刻夜六十刻
夏至晝六十刻夜四十刻
春秋二分晝夜各五十刻
```

Thus this exact 1492 print securely carries the hundred-ke framework and coarse 40↔60 solstitial control.

## 4. AA060001_016 — decisive 48-arrow / 24-qi mechanism

```text
URL=https://www.library.yonezawa.yamagata.jp/dg/data/AA060/001/AA060001_016.jpg
SHA256=96c1ba3aa77df00739194ce04f5fd351521a7001591d125297e0df840786dc52

今制蓮漏之圖
宋朝所用之制亦如於唐而其法以晝夜百刻
分十二時每時有八刻二十分每刻六十分
箭四十八
二箭當一氣
二十四氣大凡每氣差二分半
冬至後行盈夏至後行縮
```

The narrow mechanism claim is physically closed by 1492:

```text
100-ke clepsydra
  + 48 discrete arrows
  + 2 arrows per qi
  + 24 qi
  + 2.5 fen difference per qi
  + increase after winter solstice / decrease after summer solstice
```

This binds a finite arrow apparatus directly to the 24-qi cycle.

## 5. Scope firewall

Closed:

```text
secure pre-1578 physical arrow/qi carrier = YES
48-arrow architecture = YES
two arrows per qi = YES
24-qi cycle = YES
per-qi 2.5-fen differential = YES
winter/summer directional reversal = YES
```

Still unresolved:

```text
exact within-qi change-day selector
Nanjing 59-ke endpoint binding
exact 大寒十三後 / 雨水後四日 fingerprint
direct Sanming parent
```

The same 1492 object directly gives 40/60 rather than 59/41 at the reviewed coarse solstitial locus. Therefore unchanged numeric identity with the 1578 Sanming target is disproved.

## 6. Relation to Batch 12DV

Do not collapse the two parameterizations:

```text
1492 事林廣記:
48 arrows / 2 arrows per qi / 24 qi / 2.5 fen per qi / 40↔60 coarse control

1823 reviewed 準齋 recension:
25 arrows / 日曆節候 selection / first-to-25th 38↔62
```

Together they establish the historical reality of seasonal discrete leak-clock arrow mechanisms while preserving their numeric and transmission differences.

## 7. Transmission consequence

```text
PHYSICAL-COPY-YONEZAWA-SHILIN-AA060-HONGZHI5-1492
RULE-FAMILY-SHILIN-48ARROW-24QI-40-60
TG-E0074  physical 1492 copy -> ATTESTS -> 48-arrow/24-qi rule family
TG-E0075  rule family -> STRUCTURAL_MECHANISM_CANDIDATE_FOR -> 1578 Sanming table
```

TG-E0075 is mechanism-class evidence only. Direct unchanged numeric-table identity is recorded as disproved, and the Sanming composite hypothesis receives zero exact-parent vote.

## 8. Product firewall

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
MISSING_FROM_PRODUCT=10
PROVENANCE_DEFECTS=12/12_REPAIRED
CONFIRMED_CHART_ALGORITHM_DEFECTS=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
DETERMINISTIC_PRODUCT=CLOSED
```

## 9. Next gate

Find the pre-1578 Chinese binding/recomposition layer that connects the already attested seasonal discrete-arrow / whole-ke architecture to the official Nanjing 59-ke endpoint, while separately pursuing the exact `大寒十三後 / 雨水後四日` change-day fingerprint.

The 1492 witness closes the chronology of the arrow/qi architecture; it does **not** solve the 59-ke numerical recomposition.
