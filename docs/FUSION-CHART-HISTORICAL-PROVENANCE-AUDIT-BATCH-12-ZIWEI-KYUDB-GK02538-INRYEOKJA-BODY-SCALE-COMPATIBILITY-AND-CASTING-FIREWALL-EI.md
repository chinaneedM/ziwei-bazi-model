# Fusion Chart Historical Provenance Audit R1 — Batch 12EI

## GK02538《大統曆註》：印曆字中号字身尺度相容性与铸字同一性防火墙

Status: **OFFICIAL 印曆字 MEDIUM TYPE = 1.2×0.8 CM / GK02538 NOMINAL 21-CHAR VERTICAL SLOT = 1.2047619 CM / SCALE COMPATIBILITY SUPPORTED / DIRECT GLYPH-BODY OR CASTING IDENTITY NOT CLOSED / EXACT IMPRESSION YEAR UNRESOLVED / NO RUNTIME CHANGE**

## 1. Why this batch

12EH built a direct dated 印曆字 comparison corpus, but correctly rejected page-layout resemblance as a dating operator.

The next question is narrower:

> Can the surviving bibliographic dimensions be converted into a physical-scale control before any shared-glyph/type-form claim is attempted?

12EI answers **yes at the nominal body-slot level, no at casting-identity level**.

## 2. Official 印曆字 type-body control

Korea Heritage Service / 国家遗产门户 publishes a metal-type chronology entry for `인력자(印曆字)` / `관상감(서운관) 철활자`:

```text
historical scope   16세기
material           무쇠
medium type        1.2 × 0.8 cm
small type         0.5 × 0.4 cm
imprints           大統曆 · 各種曆書 等
```

Source ID:

```text
EXT-HERITAGE-INRYEOKJA-TYPE-BODY-DIMENSION-CONTROL
https://www.heritage.go.kr/heri/html/HtmlPage.do?pg=%2Fhwalja%2Fhwalja01_01.jsp
```

The same institutional page says the exact casting date is not known and treats pre-Imjin use as an inference from historical evidence. Therefore the dimension table is a **type-category physical-scale control**, not a copy-specific impression date.

## 3. GK02538 nominal scale replay

Kyujanggak's first-party catalog metadata for GK02538 remains:

```text
edition       觀象監活字
year          刊年未詳
half frame    25.3 × 17.5 cm
layout        9行21字; 注雙行
leaf          34.7 × 22.5 cm
```

For a standard 21-character body line, the nominal vertical slot is:

```text
25.3 cm / 21 = 1.2047619 cm
```

Against the official medium 印曆字 height:

```text
official medium height    1.2000000 cm
GK02538 nominal slot      1.2047619 cm
absolute difference       0.0047619 cm
relative difference       0.397 %
```

This is a strong **physical-scale compatibility** result.

It is not a direct measurement of the inked glyph or metal sort. Frame margins, impression distortion, paper deformation and layout practice remain distinct variables.

Therefore:

```text
GK02538 nominal body scale compatible with medium 印曆字     SUPPORTED
GK02538 glyph body directly measured                         FALSE
same matrix / same casting generation                        NOT PROVED
exact copy date from scale                                    FORBIDDEN
```

## 4. Why the 1604 object does not close casting identity

The official Ryu Seong-ryong 1604 甲辰 calendar record gives:

```text
half frame     28.5 × 16.2 cm
line count     行字數不定
annotation     註雙行
```

The direct physical image also visibly mixes large title type, body type, smaller calendrical type and manuscript annotations.

Because the line/character count is explicitly variable, there is no lawful analogue of `frame height / fixed body-character count` for that annual-calendar page.

The current direct-image corpus does contain common characters such as `大 / 正 / 月 / 日 / 立 / 春 / 雨 / 水`, but candidate occurrences are not yet bound to the same nominal type-size class across objects.

Thus shared-glyph form identity receives **zero vote** in 12EI.

## 5. Chronology consequence

```text
official 印曆字 body-size control                CLOSED
GK02538 medium-type scale compatibility          SUPPORTED_NOMINAL_VERTICAL_ONLY
GK02538 specific subtype                         UNRESOLVED
GK02538 casting generation                       UNRESOLVED
GK02538 exact impression year                    UNRESOLVED
secure pre-1578 GK02538 physical impression      FALSE
```

The result narrows the typographic search without collapsing chronology.

## 6. Transmission consequence

The physical-copy node is strengthened with a new scale attribute, but no new direct lineage edge is created.

Explicitly unproved:

```text
scale compatibility -> same casting generation
scale compatibility -> exact impression date
scale compatibility -> Sanming/Yueling parentage
```

Exact Sanming-parent vote increment remains **0**.

## 7. Product consequence

No deterministic chart algorithm changes.

```text
Matrix rows                 198
Audited rows                166
MISSING_FROM_PRODUCT         10
Provenance defects          12 / 12 repaired
Chart algorithm defects      0
Algorithm reopen             0
Candidate collapse           0
DETERMINISTIC PRODUCT        CLOSED
```

## 8. Next gate

1. recover high-resolution, **size-class-bound** shared glyphs from dated 16th-century 印曆字 impressions;
2. normalize them by source-bound physical scale before comparing stroke/type-form details;
3. recover the full 1987 specialist study or another authoritative study with object-specific subtype criteria;
4. continue the separate pre-1578 Rainwater + Dahan fingerprint / threshold-to-whole-ke search.

Research record: `docs/research/ZIWEI-KYUDB-GK02538-INRYEOKJA-BODY-SCALE-COMPATIBILITY-AND-CASTING-FIREWALL-R1.json`.
