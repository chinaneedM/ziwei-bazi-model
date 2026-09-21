# Fusion Chart Historical Provenance Audit R1 — Batch 12EH

## GK02538《大統曆註》：定年印曆字实物对照集与觀象監活字子型防火墙

Status: **DATED 1580 + 1604 INRYEOKJA PHYSICAL COMPARATORS ACQUIRED / ANNUAL-CALENDAR LAYOUT ≠ COPY-DATING OPERATOR FOR DATONGLIZHU / GENERIC 觀象監活字 SUBTYPE STILL AMBIGUOUS / NO CASTING-GENERATION IDENTITY / GK02538 IMPRESSION YEAR UNRESOLVED / NO RUNTIME CHANGE**

## 1. Why this batch

12EG proved that `觀象監活字` is not a unique one-time casting label and that an old internal imprint can survive inside a later physical reprint.

The next gate was therefore copy-specific comparison against dated Gwansanggam / 印曆字 objects.

12EH builds that comparison set directly.

## 2. Direct dated image corpus

GitHub Actions run `35551350656`, artifact `10618158169`:

```text
aks-inryeokja-dated-physical-comparators-r1
sha256:684d87c4c28c1ac89e4670e255dbee4f5c80657de42588e9f65081adeedbeeac
```

recovered all target images without OCR authority.

### 2.1 庚辰年大統曆 — 1580 usage-year control

Two full-size public physical images credited to the Korea Heritage Administration were acquired:

```text
卷首  1762×2048
SHA256 34dcbde6f5b79629df507498e1c22baa09db8f6ac74368b80f3819d82e61de2e

卷末  1748×2048
SHA256 306b8f03949850c0cedd9575263208ccbd9dc8e6465165b13406ef1918788590
```

The object is the 1580-use `庚辰年大統曆`. Specialist sources place printing in 1579; the Heritage detailed record itself describes 1579 as an inference from the ordinary prior-winter issue cycle. Therefore 12EH does not convert the photograph into an independent “1579 imprint statement”.

### 2.2 柳成龍大統曆甲辰 — 1604 direct dated control

The Academy of Korean Studies original media image was acquired directly:

```text
1002×1055
SHA256 05a59824cfb8a836e2c86168f1610417f115a372f50af4c0f6613b8cde864a3b
```

The image visibly carries the calendar heading:

```text
大明萬曆三十二年歲次甲辰大統曆
```

and therefore provides a direct post-Imjin dated Gwansanggam/Inryeokja physical control.

## 3. GK02538 controls in the same artifact

The comparison artifact re-acquired the exact GK02538 pages already bound in 12EE–12EF:

```text
0001/002a 8458f8a0fd58f23f91139d7d489077472fd7fddb449d9635f6f29df5e2a9b461
0001/002b 44d3b37b9ddf8d67da153a4a7143837b1d9b066379f657c38a0ab0a8298a95a1
0004/057a 6adda63e4c6c84aea1230e2c2925faeecac5069b2779018e725986c2adbc97ef
0004/057b 9bf50977f2ab0cbe21b326bd4ec1eaa20493dc93a47917ee291695f8df90232b
```

Current first-party catalog identity remains:

```text
edition     觀象監活字
year        刊年未詳
layout      四周雙邊; 半葉匡郭 25.3×17.5cm; 9行21字; 注雙行;
            上下花紋魚尾; 34.7×22.5cm
```

## 4. What direct visual comparison can safely say

The dated 1580/1604 controls use an annual-calendar-specific page architecture: dense calendrical grids, chained recurring calendar expressions, mixed type sizes and calendar title blocks.

GK02538 is a 12-juan calendrical commentary with a book-text/table architecture.

Therefore:

```text
annual-calendar page layout == GK02538 copy-identical layout control    FALSE
layout difference == different institutional type family               NOT PROVED
visual resemblance == exact copy date                                  FALSE
```

This is a methodological narrowing, not a failed comparison.

The correct next comparison must work at **shared-glyph / type-form / casting-generation** level, not page-layout level.

## 5. Specialist subtype firewall

Kim Sang-Ho's 1987 bibliographic study `관상감활자고`, indexed by RISS, explicitly warns that multiple distinct printing types were often catalogued under the single name “Kwansanggam Type”, causing erroneous catalogue notes.

Its indexed abstract proposes four functional categories:

```text
Daetongryokja
Naeyongsamsoja
Myongsiryokja
Chiljongryokja
```

12EH uses this only as a **secondary specialist taxonomy control**.

It does **not** assign GK02538 to one of those four types without direct object-level evidence.

## 6. Dated series control

The official Ryu Seong-ryong bibliography supplies a useful chronological series:

```text
1594 甲午 = woodblock control
1596 丙申 = iron Inryeokja
1597 丁酉 = iron Inryeokja
1604 甲辰 = iron Inryeokja
1606 丙午 = iron Inryeokja
```

with common calendar layout:

```text
四周單邊; 行字數不定; 註雙行; 黑口; 上下內向三葉花紋魚尾
```

This strengthens the dated institutional comparison corpus but still does not identify GK02538's exact casting generation.

## 7. Chronology consequence

The safe chronology state is now:

```text
dated Gwansanggam/Inryeokja comparator corpus   YES
GK02538 generic catalog type                    觀象監活字
GK02538 exact subtype                           UNRESOLVED
GK02538 casting generation                      UNRESOLVED
GK02538 exact impression year                   UNRESOLVED
secure pre-1578 GK02538 physical impression     FALSE
```

No 1434, 1442, 1579, 1580 or 1604 shortcut is authorized.

## 8. Product consequence

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

## 9. Next gate

1. build scale-preserving shared-glyph controls between GK02538 and dated 印曆字 objects;
2. recover the 1987 specialist study or equivalent authoritative type study far enough to test object-specific subtype criteria;
3. continue the exact pre-1578 Rainwater + Dahan fingerprint and threshold-to-whole-ke operator searches.

Research record: `docs/research/ZIWEI-KYUDB-GK02538-DATED-INRYEOKJA-PHYSICAL-COMPARATOR-AND-SUBTYPE-FIREWALL-R1.json`.
