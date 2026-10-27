# Fusion Chart Historical Provenance Audit R1 — Batch 12B

## Ziwei late-Zi ten-ke timekeeping / 训诂 closure

Status: **GENERIC TIMEKEEPING ORIENTATION CLOSED / ZIWEI RUNTIME TIME-STANDARD BINDING OPEN / NO ALGORITHM REOPEN**

Batch 12A established the direct Ziwei witness: Nanyangtang Fullbook PDF p.320 reads `如子時有十刻上五刻屬昨夜亥時下五刻屬今日子時`. Batch 12B asks a narrower philological question: what do `十刻 / 上五刻 / 下五刻` mean in the historical timekeeping coordinate?

## 1. Ming timekeeping control

《三命通会》卷二《论时刻》 states that a shichen has eight large and two small ke, arranged into upper and lower halves. It explicitly says Zi's upper half is before midnight and belongs to the previous day, while the lower half is after midnight and belongs to the current day.

This is used only as a **generic Ming timekeeping semantic control**. It is not imported as Ziwei doctrine.

## 2. Ten-ke is not ten equal duration slices

顾炎武《日知录·百刻》 independently explains the apparent ten-ke-per-shichen naming: the day still totals 100 ke because the scheme mixes large and small ke. Therefore Fullbook's `十刻` must not be naively modeled as ten equal 12-minute slices.

The relevant mechanical reading is two equal **half-shichen** spans, each represented by four large plus one small named ke position.

## 3. Modern coordinate translation

The National Astronomical Observatory of Japan calendar-history reference gives the fixed-hour coordinate:

- one shichen = two modern hours;
- Zi ≈ 23:00–01:00;
- Zi-zheng = the middle of Zi ≈ midnight.

Therefore, **as a modern coordinate translation only**:

- upper half Zi ≈ 23:00–24:00;
- lower half Zi ≈ 00:00–01:00.

This translation does not select the Ziwei runtime clock. The source does not yet tell us whether the candidate must be evaluated in civil standard time, local mean solar time, local apparent solar time, or another source-scoped historical clock realization.

## 4. Received transcription controls

- Shidian reproduces `上五刻 / 下五刻`, agreeing with the direct Nanyangtang facsimile at the critical wording.
- Wikisource renders `上午刻 / 下午刻`; it also places the section in 卷三 rather than the Nanyangtang seven-juan scan's 卷五.

The direct facsimile remains glyph authority. These digital texts are controls for transmission/transcription, not independent physical editions.

## 5. Current candidate status

`HPA-ZDATE-006` remains:

`MISSING_FROM_PRODUCT`

The generic upper/lower-half orientation is no longer a blocker, but these remain open:

1. additional physical Fullbook edition collation;
2. whether `亥時` is stable across physical witnesses or a transmission defect;
3. the exact Ziwei runtime time-standard binding;
4. composition with chart-date attribution;
5. no winner selection until the above are source-closed.

Counts are unchanged:

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

The deterministic fusion-chart product remains CLOSED.
