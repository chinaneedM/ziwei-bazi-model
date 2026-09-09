# Fusion Chart Historical Provenance Audit R1 — Batch 12AJ

## Fullbook 「羅經以定真確時候」訓詁與歷史計時技術審計

Status: **TWO FULLBOOK PHYSICAL EDITIONS AGREE ON 羅經 SENTENCE / 羅經 DIRECTIONAL-INSTRUMENT SEMANTICS CLOSED / STANDALONE CLOCK EQUIVALENCE REJECTED / TRUE-SOLAR RUNTIME INFERENCE FORBIDDEN / HPA-ZDATE-006 REMAINS OPEN**

## 1. Why this batch exists

Batch 12AI narrowed the generic historical clock family toward local observational astronomical time but deliberately did not select a Ziwei natal runtime winner.

The directly reviewed Fullbook target section contains a stronger source-internal sentence:

```text
如天氣陰雨之際必須羅經以定真確時候若差訛則命不凖矣
```

Batch 12AJ asks what `羅經` mechanically means in its historical technical environment and whether this sentence authorizes a modern “true/apparent solar time” runtime interpretation.

## 2. Direct Fullbook physical-edition agreement

No OCR is used.

### Nanyangtang

Direct Nanyangtang facsimile, PDF p320 / 卷五 / 《論人生時要審的確》:

```text
如人生子亥二時最難定凖要仔細推詳
如子時有十刻上五刻屬昨夜亥時下五刻屬今日子時
如天氣陰雨之際必須羅經以定真確時候若差訛則命不凖矣
```

### Shanghai Guangyi / Yulgok

Direct re-review of image `B005_01_B00320_003_003`, SHA-256
`2d1fc5ce8459d3696166b0471b2075fee247ede94b73eb833d435fe54ee847e0`, shows the same three-line passage in 卷三.

Therefore:

```text
FULLBOOK_LUOJING_SENTENCE_STABILITY_ACROSS_NANYANGTANG_AND_GUANGYI=CONFIRMED
NEW_WITNESS_INCREMENT=0
```

The zero increment avoids double-counting physical copies already counted in earlier target-text batches.

## 3. Contemporary Ming astronomical control

Machine probe run `34324043522` / artifact `10093089382` binds the 《皇明經世文編》卷四百九十三 `制器測晷` passage.

Its instrument separation is explicit:

- `日晷` determines daytime time;
- `星晷` determines nighttime time;
- `正線羅經` determines `子午` direction;
- during dawn/dusk/cloud/rain, `行漏` supplements what the two dials cannot do;
- the clepsydra itself is not the root of time determination; the root must be calibrated against celestial motion;
- ordinary compass north-south is not automatically the true meridian;
- exclusive use of a compass can create indeterminate ke/fen timing error and tends to be early relative to the true time.

This is a contemporary technical control, not Ziwei doctrine.

## 4. Contemporary Ming Luojing control inside shushu literature

Xu Zhimo's Ming `《新鐫徐氏家藏羅經頂門針》` directly discusses:

- magnetism and the needle;
- the needle's directional behavior;
- the phrase `此針之所以必指南也`;
- the broader `羅經` device as a directional / geomantic instrument.

This independently closes the philological point that `羅經` belongs to the magnetic-compass / orientation instrument family. It is not a clock specification.

## 5. Adjudication

The following normalization is now forbidden:

```text
羅經以定真確時候
    != 羅經本身就是計時器
    != 原文直接指定真太陽時
    != 原文直接指定 local apparent solar time runtime
```

The strongest defensible statement is:

```text
羅經 = magnetic compass / orientation instrument family
Fullbook 羅經 sentence = source-scoped practice statement or shorthand
exact operational composition = unresolved
```

There is a real technical tension: the Fullbook says to use `羅經` under cloudy/rainy conditions to determine accurate time, whereas contemporary astronomical instrumentation assigns `羅經` to meridian orientation and `行漏` to inclement-weather time continuation, while warning that exclusive compass use can induce timing error.

That tension must be preserved rather than harmonized by assumption.

## 6. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
RUNTIME_TIME_STANDARD_BINDING=PARTIALLY_NARROWED_WITH_FULLBOOK_INSTRUMENT_SEMANTIC_TENSION_NOT_CLOSED
LUOJING_MEANS_TRUE_SOLAR_TIME=NO
LOCAL_APPARENT_SOLAR_RUNTIME_WINNER=NOT_SELECTED
NEW_CANDIDATE=NO
CANDIDATE_COLLAPSE=0
ALGORITHM_REOPEN=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
```

The deterministic product remains CLOSED.

## 7. Accounting

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
PROVENANCE_METADATA_DEFECTS=10_CONFIRMED_10_REPAIRED
CHART_ALGORITHM_DEFECTS=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

## 8. Next gate

The next high-value gate is not another generic modern “true solar time” article. It is a source-scoped historical bridge explaining how Ziwei/Fullbook practitioners operationalized `羅經以定真確時候`, especially in cloudy/rainy or nighttime natal timing.

Machine evidence: `docs/research/ZIWEI-FULLBOOK-LUOJING-TIMEKEEPING-SEMANTICS-R1.json`.
