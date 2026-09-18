# Batch 12DH — 嘉靖三十年（1551）《類編曆法通書大全》38/62細表前1578年代閉合

## Status

```text
SOURCE=NLC892-411999026677-72517 類編曆法通書大全 第1冊
EDITION=刻本 遞修本
PUBLICATION_DATE=劉釪明嘉靖30年[1551]
GOOD_BOOK_NUMBER=15897
PRE1578_BIBLIOGRAPHIC_BINDING=YES
P20_TARGET=四時加減晝夜節氣
DAHAN_1551=40/60 -> 41/59
YUSHUI_1551=45/55
SANMING_YUELING_DAHAN=43/57 -> 十三後 -> 44/56
SANMING_YUELING_YUSHUI=47/53 -> 後四日 -> 48/52
FINE_38_62_BRANCH_PRE1578_EXISTENCE=CLOSED
UNCHANGED_EXACT_TARGET_IDENTITY=DISPROVED
HPA_ZDATE_006=MISSING_FROM_PRODUCT
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NO
```

## 1. Result

Batch 12DE had already physically excluded the fine `38↔62` branch as the unchanged exact Sanming/Yueling table, but its reviewed NLC copy was only dated to Ming `[1368-1644]`. Batch 12DH closes the remaining chronology question using NLC set `411999026677`.

The public NLC-derived file record binds this object as `刻本 遞修本`, `劉釪明嘉靖30年[1551]`, `存28卷：1～28`, 善本書號 `15897`. This date is used at bibliographic-object scope; no unread internal colophon is promoted as direct glyph evidence.

## 2. Evidence chain

```text
SOURCE_SHA256=22811dd2b2291ed4a94a63b51665c24785a4c1795637a4a89b05f979208d76f2
PDF_PAGES=70
LOCATOR_RUN=35358583198
LOCATOR_ARTIFACT=10554020325
LOCATOR_DIGEST=sha256:b557c123d8f67ee4a66b8ccf9e27c4d6fb60795459e993dfd9d927a8cfb110a1
HIGHRES_RUN=35359354362
HIGHRES_ARTIFACT=10554051966
HIGHRES_DIGEST=sha256:3c13f48b0df8b82989e765bfa8bd32f0bcf3e489838985ac75d6d7fb6cc47fb4
OCR_USED_FOR_FINAL_GLYPH_CLAIMS=false
```

p14 (`6d5d5de...`) directly reads `類編曆法通書大全總目` and `類編曆法通書大全卷之一`, binding the physical target volume to the work.

## 3. Direct p20 collation

p20 SHA-256:

`ac71e579493ff892476c1534aabd3b53cb26d64f185d6bb12a837476ba3f6fa9`

The heading is directly readable as:

```text
四時加減晝夜節氣
```

Secure target rows include:

```text
冬至節日連小寒後四日同 -> 晝38 / 夜62
大寒節日至後六日       -> 晝40 / 夜60
大寒後七日至後十三日   -> 晝41 / 夜59
立春前一日至後三日     -> 晝42 / 夜58
立春後四日至後九日     -> 晝43 / 夜57
立春後十日至後十四日   -> 晝44 / 夜56
雨水節日至後五日       -> 晝45 / 夜55
```

This is the same fine one-ke `38↔62` table family characterized in 12CE/12DE.

## 4. Chronology adjudication

Before 12DH:

```text
MING_PHYSICAL_ATTESTATION=YES
EXACT_IMPRESSION_YEAR=UNRESOLVED
SECURE_PRE1578_ATTESTATION=OPEN
```

After 12DH:

```text
FINE_38_62_BRANCH_PRE1578_ATTESTATION=YES_AT_NLC_1551_BIBLIOGRAPHIC_OBJECT_SCOPE
```

A numerically different Tongshu day/night-ke branch therefore demonstrably existed before the 1578 Sanming print.

## 5. Exact target mismatch

1551 Leibian:

```text
大寒 40/60 -> 41/59
雨水 45/55
```

1578 Sanming / 1589 Yueling:

```text
大寒 43/57 -> 十三後 -> 44/56
雨水 47/53 -> 後四日 -> 48/52
```

So the chronology closes for a **competing branch**, not for the target parent:

```text
PRE1578_EXISTENCE_OF_FINE_38_62_BRANCH=CONFIRMED
UNCHANGED_EXACT_PARENT_OF_SANMING=DISPROVED
UNCHANGED_EXACT_IDENTITY_WITH_YUELING_CITED_TONGSHU=DISPROVED
```

## 6. Copy firewall

The 1551 object is not silently equated with NLC892-411999018604-67969 used in 12CE/12DE.

```text
SHARED_FINE_TABLE_FAMILY=SUPPORTED
SAME_PHYSICAL_COPY=UNPROVED
DIRECT_COPY_RELATION=UNPROVED
```

## 7. Product adjudication

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

## 8. Next gate

The 38/62 fine branch no longer needs chronology chasing. Priority remains:

1. a distinct pre-1578 Tongshu/almanac witness carrying both exact Sanming/Yueling fingerprints;
2. a Chinese pre-1578 Nanjing/Datong carrier directly printing or generating the `59/41` layer;
3. the historical threshold/selection/quantization rule that produces the whole-ke change-day fingerprint.

Research record: `docs/research/ZIWEI-LEIBIAN-JIAJING30-1551-PRE1578-FINE-TABLE-CHRONOLOGY-R1.json`.
