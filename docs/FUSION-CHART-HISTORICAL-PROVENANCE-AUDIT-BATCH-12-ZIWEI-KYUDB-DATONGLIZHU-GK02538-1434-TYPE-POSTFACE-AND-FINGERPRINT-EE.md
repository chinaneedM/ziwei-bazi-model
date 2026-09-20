# Fusion Chart Historical Provenance Audit R1 — Batch 12EE

## 奎章閣 GK02538_00《大統曆註》：1434 金鑌鑄字跋、活字異本與雨水/大寒指紋再校

Status: **DIRECT KYUDB PHYSICAL RECENSION / DISTINCT 觀象監活字 COPY CLOSED / 1434 KIM BIN TYPE-CASTING + START-OF-PRINTING POSTFACE DIRECTLY RECOVERED / CURRENT IMPRESSION YEAR STILL 刊年未詳 / RAINWATER AND DAHAN EXACT SANMING FINGERPRINTS MISMATCH / ZERO EXACT SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12ED directly collated GK02426_00 and found a Korean Datonglizhu recension with the same threshold + whole-ke architecture, a Dahan single-day `後十三日 -> 44/56` convergence, but a mismatching Rainwater branch. Its chronology remained unresolved because the previously reported 1434 Kim Bin postface was not directly recovered.

The live Kyujanggak catalog also exposes a **different** object:

- `GK02538_00`
- `奎2538-v.1-4`
- `觀象監活字`
- `12卷 4冊`
- `刊年未詳`
- `9行21字`
- `M/F83-16-89-D`

This batch directly reviews that object and its attached postfaces.

## 2. Acquisition / route correction

The old record is not on the `SIC` image family used by GK02426. The current catalog source emits:

```text
item_cd=CSP
book_cd=GK02538_00
image filename family = GK02538_00_IL_{vol}_{page}.jpg
```

After binding to that first-party route, run `35516795637` recovered all 38 requested target pages with zero failures.

Artifact:

```text
ID=10606724326
DIGEST=sha256:407a937f452431c1adcd6fb46c10b4446bf2e3e08b1f2e1bc727b9683fb59349
```

No OCR is used for final glyph, numeric, chronology or lineage claims.

## 3. Rainwater direct collation

Volume 1 p002a:

```text
大統曆註卷第一
立春正月節
冬至餘三十四刻四十五分已上為退
雨水正月中
```

SHA-256: `8458f8a0fd58f23f91139d7d489077472fd7fddb449d9635f6f29df5e2a9b461`

Volume 1 p002b directly preserves:

```text
後五六日  晝四十七刻 夜五十三刻
後十三四日 晝四十八刻 夜五十二刻
```

SHA-256: `44d3b37b9ddf8d67da153a4a7143837b1d9b066379f657c38a0ab0a8298a95a1`

The 1578 Sanming/Yueling target is:

```text
雨水 47/53
後四日 48/52
```

Therefore the GK02538 Rainwater branch is a decisive mismatch.

## 4. Dahan direct collation

Volume 4 p038a directly binds the locus:

```text
大統曆註卷第十二
小寒十二月節
大寒十二月中
```

SHA-256: `a2ef9d9612b2a5b19acc4314eac579e390dc2edd3106c162ddd058fe3634db9d`

Volume 4 p038b directly preserves:

```text
後十三四日 晝四十四刻 夜五十六刻
冬至餘五十六刻三十分已上為退
```

SHA-256: `1952fe334709737751f5a29831a261cbf7eb7219b0ef2a9f6c15c9b01649fb38`

This differs from:

- GK02426: `後十三日 -> 44/56`
- Sanming 1578: literal `十三後日` before `44/56`

So GK02538 shows a nearby day-13/14 band, but **not** the exact target fingerprint.

## 5. Direct terminal chronology evidence

p055b directly reads:

```text
大統曆註卷第十二終
```

The attached printing/type postface then becomes physically visible.

p057a:

```text
宣德九年秋七月
殿下謂知申樞院事臣李蕆曰
更用大字本重鑄之亦佳也
```

p057b:

```text
所鑄至三十有餘萬字
越九月初九日始用以印書
一日所印可至四十餘紙
宣德九年九月日
臣金鑌拜手稽首敬跋
```

Thus the object directly preserves a 1434 statement about recasting large type and beginning to print books with it on the ninth day of the ninth month.

### Chronology firewall

This closes:

```text
1434 TYPE-CASTING / START-OF-PRINTING EVENT STATEMENT = DIRECT
```

It does **not** close:

```text
SURVIVING GK02538 COPY IMPRESSED IN 1434 = NOT PROVED
EVERY CALENDAR RULE COMPOSED IN 1434 = NOT PROVED
SECURE PRE-1578 PHYSICAL IMPRESSION = NOT YET PROVED
```

The same p057b also visibly carries `正統七年十二月日` at the far left. Its exact referent is not adjudicated in this batch and therefore is not silently normalized into a copy date.

## 6. Recensional consequence

GK02538 and GK02426 are distinct first-party catalogued physical routes. They share the Datonglizhu threshold + whole-ke architecture but differ at high-information loci.

The evidence supports:

```text
BRANCHING / RECOMPOSED DATONGLIZHU RECENSION FAMILY
```

It does not support:

```text
GK02538 = GK02426 unchanged text state
GK02538 = direct unchanged parent of Sanming 1578
1434 postface date = automatic surviving-copy impression date
```

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

The next highest-value work is now:

1. date the **surviving GK02538 impression itself** using copy/type/bibliographic evidence without transferring the 1434 postface date;
2. keep searching for a securely pre-1578 witness that combines the exact `雨水 -> 後四日` and `大寒 十三後日` target fingerprint;
3. find an explicit operator connecting `冬至餘…已上為退` state thresholds to the whole-ke schedule.

Research record: `docs/research/ZIWEI-KYUDB-DATONGLIZHU-GK02538-1434-TYPE-POSTFACE-AND-FINGERPRINT-R1.json`
