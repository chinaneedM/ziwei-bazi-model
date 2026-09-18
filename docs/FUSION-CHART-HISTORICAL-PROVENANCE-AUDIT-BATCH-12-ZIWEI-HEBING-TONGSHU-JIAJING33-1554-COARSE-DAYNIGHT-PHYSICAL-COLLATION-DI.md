# Batch 12DI — 嘉靖三十三年（1554）《新刊類編陰陽選擇合併通書大全》卷十七晝夜百刻粗表直接校勘

## Status

```text
SOURCE=Library of Congress LCCN 2012402919
TITLE=新刊類編陰陽選擇合併通書大全十七卷
EDITION=明嘉靖三十三年書林余氏自新齋刻本
DATE=1554
TARGET_JUAN=17
TARGET_HEADING=選時寶鏡局
TABLE=銅壺晝夜百刻圖式
DAHAN_1554=41/59
YUSHUI_1554=45/55
XIAZHI_1554=60/40
SANMING_1578_DAHAN=43/57 -> 十三後日 -> 44/56
SANMING_1578_YUSHUI=47/53 -> 後四日 -> 48/52
SANMING_1578_XIAZHI=59/41
PRE1578_COARSE_TONGSHU_BRANCH=CONFIRMED
UNCHANGED_EXACT_TARGET_IDENTITY=DISPROVED
HPA_ZDATE_006=MISSING_FROM_PRODUCT
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NO
```

## 1. Why this follows 12DH

12DH closed the 1551 chronology of the competing fine `38↔62` branch. The remaining high-value search was not another copy of that same table, but a **different securely pre-1578 Tongshu/almanac physical witness**.

LOC LCCN `2012402919` is such a witness: `《新刊類編陰陽選擇合併通書大全》十七卷`, catalogued as a Ming Jiajing-33 / 1554 Zixinzhai print. Volume 10 contains Juan 17.

## 2. Bibliographic binding

The preserved LOC item JSON from run `35361144052` records:

```text
CREATED_PUBLISHED=[China] : Zi xin zhai, Ming Jiajing 33 nian [1554]
DATE=1554
NOTE=明嘉靖三十三年書林余氏自新齋刻本
COLOPHON_NOTE=龍飛嘉靖甲寅歲（33年，1554）冬月書林余氏自新齋刊行
EXTENT=10 volumes : illustrations
VOLUME_10=卷17
JUAN_17_RESOURCE_COUNT=61
```

This is a catalog-bound and source-route-bound pre-1578 physical object, not a later reprint inferred from title similarity.

## 3. Acquisition chain

Route discovery:

```text
RUN=35361144052
ARTIFACT=10553899912
DIGEST=sha256:43f86d58849983c03958f96803858acd1862f17c8fb7ef87ae9575a189810d07
```

A first high-resolution attempt (`35361531424`) failed before image acquisition because the live LOC item JSON endpoint returned repeated HTTP 503. That failure carries no content-negative authority.

The corrected source lock reused the already preserved resource IDs and downloaded LOC storage-service JP2 files directly:

```text
RUN=35362394560
ARTIFACT=10555656579
DIGEST=sha256:416a37750923c451a269524c2222ddc784e64b424b34257f9894b78f7578182a
SOURCE_FORMAT=JP2
REVIEW_DERIVATIVE=PNG
OPENING_RESOURCES_LOCKED=12
OCR_USED_FOR_GLYPH_CLAIMS=false
```

## 4. Direct section binding

Juan-17 resource 2 (`00001a`):

```text
JP2_SHA256=67d5f5761a16074dd39a588eee74a23d8797514e39cce56cd895edabc2016676
DIRECT_HEADING=選時寶鏡局
```

Juan-17 resource 3 (`01b02a`):

```text
JP2_SHA256=20dd6e975228a7e352e2762f939aeea1847c1d1d8b6729aaf3c8d69394b7b08d
DIRECT_TEXT=銅壺晝夜百刻圖式
DIRECT_DIAGRAM_TITLE=銅壺晝夜百刻之圖
```

Thus the following solar-term pages are physically bound to the intended hundred-ke day/night table, not inferred from OCR or adjacent unrelated material.

## 5. Direct numerical readings

### Rain Water

Juan-17 resource 4 / leaf `02b03a`:

```text
JP2_SHA256=e2314b210ab98267b87bd39dc5bff9e94199720efdaacb3657123405082f6c14
雨水 正月中
晝四十五刻
夜五十五刻
```

### Summer Solstice

The same source page directly gives:

```text
夏至 五月中
晝六十刻
夜四十刻
```

### Great Cold

Juan-17 resource 5 / leaf `03b04a`:

```text
JP2_SHA256=3085244d2b61b247ad53a2ee526af1732ddd9e4db97dc70df27f90e35a565d32
大寒 十二月中
晝四十一刻
夜五十九刻
```

## 6. Table-family adjudication

The 1554 table is directly compatible with the already established coarse Tongshu family:

```text
DAHAN=41/59
YUSHUI=45/55
XIAZHI=60/40
FAMILY=TABLE-FAMILY-TONGSHU-COARSE-40-60
```

This materially strengthens the historical conclusion that a coarse 40↔60 seasonal table branch remained in active Tongshu transmission immediately before Sanming 1578.

It does **not** prove a direct copy edge from the 1455 witness or same physical-copy identity with any other Tongshu object.

## 7. Exact target comparison

1554 Hebing Tongshu:

```text
大寒 41/59
雨水 45/55
夏至 60/40
```

1578 Sanming:

```text
大寒 43/57 -> 十三後日 -> 44/56
雨水 47/53 -> 後四日 -> 48/52
夏至 59/41
```

1589 Yueling target:

```text
大寒 43/57 -> 十三後 -> 44/56
雨水 47/53 -> 後四日 -> 48/52
SOURCE_LABEL=通書
```

Therefore the 1554 object is directly excluded as the unchanged exact table behind either target.

## 8. Genealogy consequence

This batch adds a new physical-copy node and confirms:

```text
1554_HEBING_TONGSHU ATTESTS TABLE-FAMILY-TONGSHU-COARSE-40-60
```

while fail-closing:

```text
1554_HEBING_TONGSHU DIRECT_UNCHANGED_TABLE_IDENTITY_WITH SANMING_1578 = DISPROVED
1554_HEBING_TONGSHU DIRECT_UNCHANGED_TABLE_IDENTITY_WITH YUELING_1589_TARGET = DISPROVED
```

The generic `通書` label in Yueling remains bibliographically unresolved.

## 9. Product adjudication

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
HPA_ZDATE_006=MISSING_FROM_PRODUCT
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=12
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=12
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

No runtime candidate, winner, collapse, or algorithm reopen is authorized.

## 10. Next gate

Search pressure is narrower again:

1. locate a **different pre-1578 Tongshu/almanac recension** that physically carries both exact target fingerprints;
2. locate a Chinese pre-1578 Nanjing/Datong witness that directly prints or generates the `59/41` layer;
3. close the historical whole-ke threshold/selection/quantization rule between the daily precision layer and the Sanming/Yueling change-day display.

Research record: `docs/research/ZIWEI-HEBING-TONGSHU-JIAJING33-1554-COARSE-DAYNIGHT-PHYSICAL-COLLATION-R1.json`.
