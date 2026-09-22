# Fusion Chart Historical Provenance Audit R1 — Batch 12EN

## GK02538《大統曆註》× 1580《庚辰年大統曆》× 1604《甲辰大統曆》：定年印曆字三方字形变异与断代防火墙

Status: **SOURCE-HASH-BOUND 正/月/大 THREE-WAY CORPUS CLOSED / DATED INRYEOKJA CATEGORY-LEVEL FORM VARIATION DIRECTLY OBSERVED / 1604 MEDIUM SIZE CLASS NOT INDEPENDENTLY CLOSED / VISUAL NEAREST-NEIGHBOR DATING FORBIDDEN / GK02538 SUBTYPE, CASTING GENERATION & IMPRESSION YEAR UNRESOLVED / NO RUNTIME CHANGE**

## 1. Purpose

12EM established a reproducible nominal-scale `正/月/大` comparison between the dated 1580 Gyeongjin control and GK02538. The remaining risk was methodological: a single dated comparator could tempt a false nearest-neighbor conclusion.

12EN adds the already catalogued 1604 Ryu Gabjin calendar as a second dated Gwansanggam/Inryeokja physical control.

## 2. Probe artifact

GitHub Actions run `35673722058`, artifact `10672460495`:

```text
gk02538-dated-inryeokja-three-way-glyphs-r1
sha256:4ba5393b22292b04b1488a4cc710ed8b20495952d1bc24b92673dc3a8f2c4839
```

The probe completed successfully. It used no OCR, automatic similarity score, or automatic type/casting classifier.

## 3. Three exact source controls

```text
1580 庚辰年大統曆 tail
1748×2048
SHA256 306b8f03949850c0cedd9575263208ccbd9dc8e6465165b13406ef1918788590

1604 柳成龍 甲辰大統曆
1002×1055
SHA256 05a59824cfb8a836e2c86168f1610417f115a372f50af4c0f6613b8cde864a3b

GK02538 0001/002a
1186×2000
SHA256 8458f8a0fd58f23f91139d7d489077472fd7fddb449d9635f6f29df5e2a9b461
```

The shared manual glyph set is `正 / 月 / 大`.

## 4. 1604 size-class boundary

The 1604 object is independently catalogued in the official 1594–1606 Ryu calendar series as an iron 印曆字 calendar. In the direct image, the selected `正/月/大` occur in a visibly larger monthly-heading class than the dense body text.

However, the official page record says `行字數不定`, and there is no object-specific caliper measurement tying these exact glyphs to the institutional `1.2×0.8 cm` medium sort.

Therefore:

```text
1604 broad Inryeokja object identity       CLOSED
1604 larger heading class                  DIRECTLY VISIBLE
1604 exact medium-size binding             NOT INDEPENDENTLY CLOSED
```

Its local-pitch normalization is used as a display control, not as proof of physical type-body equality.

## 5. Direct triad review

The probe fixes all nine source crops and normalizes each object's local vertical pitch to a common display pitch. Direct human review of the resulting triads shows:

```text
1580 vs 1604: 正/月/大 all visibly non-identical   YES
1580 vs GK:   正/月/大 all visibly non-identical   YES
1604 vs GK:   正/月/大 all visibly non-identical   YES
```

The key result is the first line: **two dated objects already accepted inside the broad Gwansanggam/Inryeokja calendar category do not share one invariant shared-glyph form.**

That directly demonstrates category-level form variation.

## 6. What this does — and does not — prove

12EN strengthens the existing firewall:

- generic `觀象監活字 / 印曆字` is not a typographically homogeneous single casting;
- a visual nearest-neighbor match or mismatch is not, by itself, an exact casting-generation operator;
- a visual nearest-neighbor match or mismatch is not, by itself, an exact impression-date operator;
- 1580 and 1604 straddle the Imjin-War period and must not be silently treated as the same casting generation.

It does **not** identify GK02538's subtype, casting generation, or exact surviving-copy impression year.

## 7. Project consequence

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

1. bind the 1604 heading to a physical size class if an object-specific measurement or bibliography can be recovered;
2. recover Kim Sang-Ho 1987 full text or equivalent object-level subtype/casting diagnostics;
3. continue the independent pre-1578 Rainwater + Dahan exact-fingerprint / threshold-operator search.

Research record: `docs/research/ZIWEI-KYUDB-GK02538-DATED-INRYEOKJA-THREE-WAY-FORM-VARIATION-FIREWALL-R1.json`.
