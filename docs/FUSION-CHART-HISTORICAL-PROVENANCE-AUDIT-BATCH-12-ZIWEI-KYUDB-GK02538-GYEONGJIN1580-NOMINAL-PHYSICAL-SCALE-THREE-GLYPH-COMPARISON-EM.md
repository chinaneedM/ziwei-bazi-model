# Fusion Chart Historical Provenance Audit R1 — Batch 12EM

## GK02538《大統曆註》× 1580《庚辰年大統曆》：中字号三字名义物理尺度归一化与铸造代判定防火墙

Status: **SOURCE-HASH-BOUND 正/月/大 CORPUS CLOSED / NOMINAL MEDIUM VERTICAL-PITCH NORMALIZATION CLOSED / THREE-GLYPH FORM DIVERGENCE OBSERVED / CASTING-GENERATION VERDICT NOT AUTHORIZED / GK02538 SUBTYPE & IMPRESSION YEAR UNRESOLVED / NO RUNTIME CHANGE**

## 1. Why this batch

12EK closed reproducible source-bound `正/月` crops. 12EL then bound the 1580 targets to the medium 印曆字 class and paired that result with GK02538's prior nominal medium-scale compatibility.

The next gate was therefore not another whole-page comparison. It was a reproducible **multi-glyph, same-nominal-size-class, scale-normalized corpus**.

12EM closes that evidence layer only.

## 2. Probe artifact

GitHub Actions run `35673107826`, artifact `10671577720`:

```text
gk02538-gyeongjin1580-medium-normalized-glyphs-r1
sha256:f75b65bded16d00d3a80b41bb00174c5d75b8e143c82f19455d997c6fa66a60f
```

The run completed successfully with no OCR, automatic glyph matching, similarity score, or automatic type-family/casting classification.

## 3. Source controls and third shared glyph

The probe hard-fails unless the exact source bytes remain unchanged:

```text
1580 Gyeongjin tail
1748×2048
SHA256 306b8f03949850c0cedd9575263208ccbd9dc8e6465165b13406ef1918788590

GK02538 0001/002a
1186×2000
SHA256 8458f8a0fd58f23f91139d7d489077472fd7fddb449d9635f6f29df5e2a9b461
```

12EM retains the 12EK `正/月` locators and adds a third manually verified shared glyph, `大`:

```text
1580 大  [698,675,754,735]
crop SHA256 bee7598f99a39e1cf8aecda68acde4797006ba7ef3e8051d45c812bca724a54e

GK 大    [1020,310,1080,370]
crop SHA256 fa1e315a09b4b3b970e67105b3cb98004e6f331484437162e51f403607f893f4
```

The 1580 `大` is in the same medium heading column as `正/月`. The GK `大` is in the `大統曆註` title column and visually occupies the same page-level body class as the medium-compatible heading type.

## 4. Nominal physical-scale normalization

The institutional medium 印曆字 height remains `1.2 cm`.

The source images independently supply their local vertical pitch anchors:

```text
1580 正→月→大 median pitch     55.0 px
GK02538 正→月 pitch           55.5 px
target normalized pitch       240 px
target nominal density        200 px/cm
```

The probe applies isotropic scaling only:

```text
1580 scale factor     4.363636...
GK02538 scale factor  4.324324...
```

This removes the small source-scale difference while preserving each photographed glyph's aspect ratio.

It is explicitly **not** a direct caliper measurement and does not rectify all photographic perspective.

## 5. Direct three-glyph review

After nominal vertical-pitch normalization, direct human review of `正/月/大` finds that all three pairs remain visibly non-identical in form.

The important adjudication is the scope of that observation:

```text
three-glyph normalized corpus closed                 YES
all three pairs visibly non-identical                 YES
automatic similarity/classification used             NO
exact same printing-face identity supported           NO
different casting generation proved                   NO
GK02538 subtype identified                            NO
GK02538 exact impression year identified              NO
```

The divergence is therefore a **descriptive multi-glyph form signal**, not a casting-generation verdict.

## 6. Why the firewall remains necessary

The Academy of Korean Studies specialist entry on 印曆字/觀象監活字 independently states that the type was repeatedly recast, that different iron-type forms existed, that wooden sorts were mixed in, and that impressions are diverse.

Therefore even a stable three-glyph visual difference cannot by itself tell us whether the two objects represent:

- different casting generations inside the same institutional type family;
- different individual sorts within a broader recurring type category;
- mixed iron/wood substitution;
- or image/printing deformation.

The full object-level diagnostic criteria from Kim Sang-Ho 1987 remain unrecovered; the RISS abstract supplies the four-category taxonomy but not enough object-specific tests to assign GK02538.

## 7. Chronology / product consequence

GK02538's exact subtype, casting generation and surviving-copy impression year remain unresolved. Secure pre-1578 GK02538 physical impression remains false. Exact Sanming-parent vote increment remains 0.

```text
Matrix rows                  198
Audited rows                 166
MISSING_FROM_PRODUCT          10
Provenance defects          12/12 repaired
Chart algorithm defects        0
Algorithm reopen               0
Candidate collapse             0
DETERMINISTIC PRODUCT        CLOSED
```

## 8. Next gate

1. obtain direct physical/perspective calibration or a second dated medium-class comparator that permits stronger diagnostic type-form comparison;
2. recover Kim Sang-Ho 1987 full text or equivalent authoritative object-level subtype/casting criteria and test GK02538 against them;
3. continue the independent pre-1578 Rainwater + Dahan exact-fingerprint / threshold-operator search.

Research record: `docs/research/ZIWEI-KYUDB-GK02538-GYEONGJIN1580-NOMINAL-PHYSICAL-SCALE-THREE-GLYPH-COMPARISON-R1.json`.
