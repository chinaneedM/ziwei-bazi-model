# Batch 12CZ — 《宋史》卷76皇祐漏刻：黃道閾值 → 改箭整刻離散化物理閉合

## Status

```text
SONGSHI_V76_SOURCE_BOUND_PHYSICAL_SEQUENCE=152/152_ACQUIRED
HUANGYOU_LOUKE_HEADING=DIRECT_PHYSICAL
HUNDRED_KE_DAY=DIRECT_PHYSICAL
ONE_KE_ONE_ARROW_LAYER=DIRECT_PHYSICAL
HUANGDAO_THRESHOLD_TO_ARROW_CHANGE=DIRECT_PHYSICAL
HUANGYOU_THRESHOLD=2_DEG_40_FEN
HUANGYOU_SUMMER_CAP=60/40
HISTORICAL_POST_COMPUTATION_DISCRETIZATION_FAMILY=CLOSED
EXACT_SANMING_REDUCTION_RULE=UNRESOLVED
HUANGYOU_AS_UNCHANGED_SANMING_PARENT=DISPROVED
HPA_ZDATE_006=MISSING_FROM_PRODUCT
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
```

## 1. Why this follows Batch 12CX and 12CY

Batch 12CX directly proved that the reviewed Shoushi day/night conversion retains sub-ke remainder as `分` and describes the result as `晝刻及分秒`. Therefore Sanming's displayed whole-ke ladder requires a distinct downstream reduction/binning/table-abstraction layer.

Batch 12CY then showed that the old Huqian integer-arrow family is not the unchanged Sanming parent: its Dahan/Yushui change-day fingerprint and 60/40 summer cap differ from the exact 1578 target.

The next question is therefore narrower:

> Did historical Chinese timekeeping actually use an explicit rule that converts a finer astronomical quantity into discrete integer-ke arrow changes, or is such a layer merely a modern reconstruction?

Batch 12CZ closes that question positively, while preserving the firewall that the exact Sanming threshold remains unknown.

## 2. Exact source-bound physical acquisition

A new GitHub Actions evidence gate acquired the complete public CADAL object:

```text
SOURCE=CADAL06060932 宋史·卷七十六~卷七十七
RUN=35334800072
ARTIFACT=10543435082
ARTIFACT_DIGEST=sha256:c2c7b13866062e49c241f66652ef3f4dadc0393877189dbf636b4aec3b79ad1b
SOURCE_DJVU_SHA256=f98aa642f30220a3a84406ca3f4739a519f765caafdd1a8ef103da080cacf132
PAGES=152
OCR_USED_FOR_FINAL_GLYPH_CLAIMS=false
```

The DjVu text layer returned zero target-term hits. That result is treated only as a failed locator and has **no negative textual authority**. The target was located and read directly on physical renders.

Chronology firewall:

```text
北宋皇祐制度 / 元代《宋史》記錄層
  !=
current Qinding Siku received-recension physical scan date
```

The current facsimile proves the received wording and table as preserved in that physical recension. It does not make the scanned exemplar a Northern-Song physical copy.

## 3. Direct physical readings

### render 009

SHA-256:

```text
34d182f86af9ad229e40cd94da037d023f70b05db9dfceb58a95abe4226c546f
```

Direct heading:

```text
皇祐漏刻
```

### render 010

SHA-256:

```text
00f5013166a08a11f10d4957e614b6265c95de2495311f5bb5acd9f8d04679e9
```

The physical text directly preserves the operating frame:

```text
分百刻於晝夜
冬至晝漏四十刻 / 夜漏六十刻
夏至晝漏六十刻 / 夜漏四十刻
春秋二分晝夜各五十刻
...
冬至夏至之間晝夜長短凡差二十刻
每差一刻...
```

### render 011 — decisive reduction rule

SHA-256:

```text
a8f9c0e466631bb4f550ccb03b222a468444d3fa3d2c036c15252d3c71834280
```

The continuation directly reads:

```text
刻別為一箭
冬至互起其首
凡有四十一箭
...
凡黃道升降差二度四十分
則隨曆增減改箭
```

The same page also preserves fractional clock-boundary language:

```text
每時初行一刻
至四刻六分之一為時正
終八刻六分之二則交次時
```

Therefore this is not a simplistic integer-only cosmology. A finer astronomical/calendar argument is explicitly connected to discrete arrow changes, while sub-ke fractions still exist in the clock-coordinate layer.

### render 014

SHA-256:

```text
2662f74e20d96bf10d3ded381d6ef27a34798cc4d20285d0b1bf74446f936df0
```

The physical table directly preserves:

```text
夏至 晝六十刻 / 夜四十刻
```

## 4. What this closes mechanically

The historical architecture is explicit:

```text
finer astronomical/calendar quantity:
  黃道升降差
        ↓ threshold
  2度40分
        ↓
discrete operational state change:
  增減改箭
        ↓
one-ke arrow/bin family
```

This is the critical new closure.

After Batch 12CX it was already mechanically necessary that some layer existed after precise Shoushi-style fractional computation if Sanming was to display whole-ke bins. Batch 12CZ now proves that **threshold-driven integer arrow discretization is itself an attested historical operational form**.

What is closed:

```text
HISTORICAL_THRESHOLD_TO_INTEGER_ARROW_DISCRETIZATION_FAMILY=YES
```

What is not closed:

```text
SANMING_USED_HUANGYOU_2DEG40FEN_THRESHOLD=NO_PROOF
SANMING_EXACT_THRESHOLD=UNRESOLVED
SANMING_EXACT_CHANGE_DAY_REPLAY=UNRESOLVED
NEAREST_INTEGER_ROUNDING_AS_HISTORICAL_RULE=NOT_PROVED
```

## 5. Earlier received control: 《隋書》卷19

The already registered `EXT-WIKISOURCE-SUI-SHU-V19-LOUKE-SEASONAL-LENGTH` preserves a deeper historical control. Its received text records the Han Yongyuan-14 / 102 CE debate over fixed nine-day changes and states a solar/ecliptic-distance rule in which each `二度四分` changes one ke, with forty-eight arrows.

This is significant because the threshold→arrow architecture is therefore not isolated to the Huangyou account. But Batch 12CZ does **not** have a Han physical copy and does not infer a direct Han → Huangyou → Sanming chain.

The Sui witness is used only as:

```text
DEEPER_HISTORICAL_TEXTUAL_CONTROL_FOR_RULE_ARCHITECTURE
```

not as direct physical ancestry.

## 6. Comparison with 1578 Sanming

The exact physical Sanming target remains different:

```text
Huangyou:
  summer solstice = 60/40
  equinoctial framework = 50/50
  explicit threshold = 黃道升降差2度40分

Sanming 1578:
  summer solstice = 59/41
  spring equinox display = 51/49
  distinctive Dahan/Yushui change-day fingerprint
  exact reduction threshold = unknown
```

Thus:

```text
Huangyou threshold rule = historical mechanism precedent
Huangyou threshold rule != unchanged direct Sanming rule
```

The evidence strengthens the **type of missing layer**, not a specific parent-child claim.

## 7. Updated composite reconstruction

The safe current model is now:

```text
Shoushi / precise daily astronomy:
  fractions retained
        ↓
historically attested rule class:
  astronomical threshold -> arrow/bin change
        ↓
Ming Nanjing / Datong regional numerical layer:
  C-II-N + 59-ke locality regime
        ↓
still-unresolved exact threshold / change-day recomposition
        ↓
1578 Sanming:
  42..59 whole-ke seasonal display
  + distinctive intra-term transitions
```

This is materially narrower than before 12CX–12CZ: the missing link is no longer an unspecified generic "rounding". It is a historically specific **selection/threshold/reduction rule** whose Nanjing-calibrated parameters and Sanming change-day fingerprint remain to be identified.

## 8. Product adjudication

No deterministic chart rule is changed.

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

No runtime candidate, winner or candidate collapse is authorized.

## 9. Next gate

The search target is now more precise:

1. a securely pre-1578 Chinese Nanjing/Datong rule that maps a fine astronomical/daylength argument to integer arrow/ke states;
2. preferably a rule whose parameters yield the **59-ke summer cap** and can replay the exact Sanming Dahan/Yushui change days;
3. an independent Chinese physical C-II-N carrier to separate Chinese origin from Joseon transmission.

Research record: `docs/research/ZIWEI-SONGSHI-HUANGYOU-ARROW-THRESHOLD-DISCRETIZATION-R1.json`.
