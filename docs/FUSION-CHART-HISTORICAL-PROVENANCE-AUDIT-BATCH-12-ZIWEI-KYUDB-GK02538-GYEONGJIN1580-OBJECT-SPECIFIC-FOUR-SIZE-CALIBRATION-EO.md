# Fusion Chart Historical Provenance Audit R1 — Batch 12EO

## 1580《庚辰年大統曆》对象级四级活字尺寸校准：修正“通用中字”表述，保留 1.2 cm 纵向桥梁

Status: **OBJECT-SPECIFIC FOUR-SIZE TYPOGRAPHY RECOVERED / 正·月 MONTH-HEADING SIZE ≈ 1.4×1.2 CM / PRIOR GENERIC 1.2×0.8 TWO-DIMENSIONAL TARGET IDENTITY SUPERSEDED / 1.2 CM VERTICAL NORMALIZATION STRENGTHENED / GK02538 WIDTH, SUBTYPE, CASTING & IMPRESSION YEAR UNRESOLVED / NO RUNTIME CHANGE**

## 1. Why this is a correction batch

12EL used the institutional generic 印曆字 reference (`medium 1.2×0.8 cm / small 0.5×0.4 cm`) to bind the 1580 `正/月` heading to a nominal medium class.

A stronger object-specific source is now available: 김종태, 「경진년 대통력(庚辰年大統曆) 소고(小考)」, *생활문물연구* 7, National Folk Museum of Korea, 2002.

The paper directly measures the 1580 object itself.

## 2. Direct object-specific measurements

On printed p.82, the study states that the 1580 calendar used four approximate type-size classes:

```text
year-spirit map + month-name/month-stem-branch letters   1.4 × 1.2 cm
year-white/month-white                                  1.0 × 0.9 cm
explanation + calendar-annotation text                  0.7 × 0.6 cm
small calendar-annotation text                          0.3 × 0.3 cm
```

The same page also documents chained-type practice for repeated calendrical phrases.

## 3. Binding to the 12EK/12EM shared glyphs

The source-fixed 1580 comparison column is `正/月/大`.

`正月` is the month name, so `正` and `月` bind directly to the paper's month-name heading class:

```text
正  ≈ 1.4 cm wide × 1.2 cm high
月  ≈ 1.4 cm wide × 1.2 cm high
```

`大` is visibly in the same monthly heading column, but the measurement sentence does not explicitly enumerate the month-size marker. Therefore no exact `1.4×1.2` assignment is made to `大` from text alone.

## 4. What changes from 12EL

The raw 12EL evidence is not retracted. Its generic medium-class inference is simply no longer the controlling target description.

Current controlling statement:

```text
1580 正/月:
  object-specific month-name heading ≈ 1.4W × 1.2H cm

generic institutional medium reference:
  1.2 × 0.8 cm

exact two-dimensional identity between these descriptions:
  NOT PROVEN
```

This resolves an important ambiguity between a generic type-category table and the actual measured 1580 printed object.

## 5. Why the 12EM vertical normalization survives

GK02538 catalog geometry gives:

```text
25.3 cm frame height / 21 character slots
= 1.204761905 cm nominal vertical pitch
```

The 1580 object-specific month-name heading height is approximately `1.2 cm`.

Relative difference:

```text
0.396825%
```

So the **vertical** scale bridge used in 12EM remains valid and is now supported by an object-specific 1580 measurement rather than only a generic type table.

What remains unproved is horizontal/body-width equivalence.

## 6. Current gate status

```text
1580 正/月 object-specific physical height       CLOSED ≈ 1.2 cm
1580 正/月 object-specific width                 CLOSED ≈ 1.4 cm
1580 大 exact textual size assignment            NOT CLOSED
GK02538 nominal vertical slot compatibility      SUPPORTED
GK02538 direct glyph-width/body calibration      NOT CLOSED
same-size shared-glyph gate                      CLOSED VERTICAL-ONLY
full physical-scale form comparison              NOT CLOSED
shared casting generation                        NOT CLOSED
GK02538 exact impression year                    NOT CLOSED
```

## 7. Project consequence

No Matrix/product count or deterministic chart behavior changes:

```text
Matrix rows                  198
Audited rows                 166
MISSING_FROM_PRODUCT          10
Provenance defects          12/12 repaired
Chart algorithm defects        0
Algorithm reopen               0
Candidate collapse             0
Direct Sanming-parent vote      0
DETERMINISTIC PRODUCT        CLOSED
```

## 8. Next gate

1. seek calibrated GK02538 glyph-width/body measurements;
2. seek object-specific 1604 type-size measurements;
3. recover Kim Sang-Ho 1987 full text or equivalent subtype diagnostics and continue the independent pre-1578 Rainwater + Dahan fingerprint search.

Research record: `docs/research/ZIWEI-KYUDB-GK02538-GYEONGJIN1580-OBJECT-SPECIFIC-FOUR-SIZE-CALIBRATION-R1.json`.
