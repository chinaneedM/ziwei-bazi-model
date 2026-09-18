# Batch 12DE — 明刻《類編曆法通書大全》38/62細表 × 《三命通會》/《月令通攷》目標指紋直接排除

## Status

```text
SOURCE=NLC892-411999018604-67969 類編曆法通書大全 第1冊
TABLE=四時加減晝夜節氣
PHYSICAL_MING_PRINT=YES
EXACT_IMPRESSION_YEAR=UNRESOLVED_1368_1644
P24_TARGET_COLLATION=DIRECT_360DPI_NO_OCR
DAHAN_FINE_TABLE=40/60 -> 41/59
YUSHUI_FINE_TABLE=45/55_AT_TERM_THROUGH_POST_DAY5
SANMING_YUELING_DAHAN=43/57 -> 十三後 -> 44/56
SANMING_YUELING_YUSHUI=47/53 -> 後四日 -> 48/52
UNCHANGED_EXACT_PARENT=DISPROVED
GENERIC_TONGSHU_IDENTITY_COLLAPSE=FORBIDDEN
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
```

## 1. Why this follows 12DD

12DD physically bound the 1589 `《月令通攷》` target fingerprint material to a small-font source label `通書`, but deliberately left the cited Tongshu title/recension/date unresolved.

The highest-value next test is therefore not “does another book call itself 通書?” but:

> Does a directly reviewed Tongshu-family physical table actually carry the same high-information Dahan/Yushui fingerprint?

Batch 12DE revisits the fine `四時加減晝夜節氣` table already identified in 12CE and locks its target rows at 360 dpi.

## 2. Controlled physical object

```text
SOURCE_ID=EXT-NLC-LEIBIAN-LIFA-TONGSHU-MING-VOL1
TITLE=類編曆法通書大全 第1冊
CATALOG_SCOPE=刻本；明[1368-1644]
EXACT_IMPRESSION_YEAR=UNRESOLVED
PDF_PAGES=95
SOURCE_SHA256=50a308f8adbfd7010b398cc68bc64dc66f7c1dbdcfe6470029e04aacd22e6419
RUN=35349106287
ARTIFACT=10548946354
ARTIFACT_DIGEST=sha256:308b16283270f5f110dc962c39761f03e42f4266e4548b8e07033d955f957ca2
RENDER_DPI=360
OCR_USED_FOR_FINAL_GLYPH_CLAIMS=false
```

Target page hashes:

```text
p23 e087452ab8421f22dcf52cbf255d8e10e44d480f4b2f6680f72b98dd24d07903
p24 2316baee2c40b9ffcb9add014dedab78aebb2914ffbfdd87cd96492fe5d7a154
p25 83583c1bb382f3fd0bfc940513e0ab85d0a38209a6815f34212100fe0974ac05
p26 7dea0f5a42937ee2cffa547b1a8374b06795a3c1b8f797f03d34847bf41aef4a
```

## 3. Direct p24 fine-table readings

The physical leaf directly heads the table:

```text
四時加減晝夜節氣
```

The securely readable post-winter-solstice target ranges include:

```text
冬至節日連小寒後四日同 -> 晝38 / 夜62

大寒節日至後六日       -> 晝40 / 夜60
大寒後七日至後十三日   -> 晝41 / 夜59
立春前一日至後三日     -> 晝42 / 夜58
立春後四日至後九日     -> 晝43 / 夜57
立春後十日至後十四日   -> 晝44 / 夜56
雨水節日至後五日       -> 晝45 / 夜55
```

The table physically pairs these post-winter ranges with corresponding autumn/pre-winter ranges under the same ke cells. This batch promotes only the target post-winter readings required for the Sanming/Yueling comparison.

p25 continues the same one-ke ladder. Because p24 already disproves unchanged exact-table identity, no uncertain p25 Rain-Water follow-on wording is promoted merely to force a complete transcription.

## 4. Exact target comparison

### 1578 Sanming direct physical target

```text
大寒 43/57 -> 十三後日 -> 44/56
雨水 47/53 -> 後四日   -> 48/52
```

### 1589 Yueling direct physical homolog

```text
大寒 43/57 -> 十三後 -> 44/56
雨水 47/53 -> 後四日 -> 48/52
SOURCE_LABEL=通書
```

### Ming Leibian fine 38/62 branch

```text
大寒節日~後六日 = 40/60
大寒後七~十三日 = 41/59
雨水節日~後五日 = 45/55
```

The mismatch is therefore not a minor wording difference or a one-day boundary shift. **The term-anchor numerical states themselves differ.**

## 5. Stemma adjudication

The following shortcut is now directly disproved:

```text
1589 Yueling says 通書
        ->
therefore its exact 43/57, 44/56, 47/53, 48/52 fingerprint
must be this physically reviewed Leibian fine 38/62 table
```

Safe result:

```text
LEIBIAN_FINE_38_62_UNCHANGED_EXACT_PARENT_OF_SANMING=DISPROVED
LEIBIAN_FINE_38_62_UNCHANGED_IDENTITY_WITH_YUELING_CITED_TONGSHU=DISPROVED_AS_NUMERIC_TABLE_IDENTITY
BROADER_TONGSHU_STRUCTURE_OR_RECOMPOSITION_ANCESTRY=POSSIBLE
```

This complements 12CH, which already showed that a different pre-1578 coarse Tongshu branch has Xiazhi 60/40 rather than Sanming 59/41. “通書” is a source-family label, not a license to flatten historically distinct tables into one invariant numerical tradition.

## 6. Chronology firewall

The NLC object is bibliographically Ming `[1368-1644]`, but its exact impression year is unresolved. Therefore Batch 12DE does not claim this physical copy predates Sanming 1578.

The numeric mismatch is independent of that chronology issue: even if an earlier recension of this exact 38/62 table family existed, the physically reviewed table is not the unchanged Sanming/Yueling exact target.

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

No runtime candidate is created, selected, or collapsed.

## 8. Next gate

Search pressure is now narrower:

1. pre-1578 `通書` / almanac recensions carrying **both** exact fingerprints;
2. a pre-1578 Nanjing/Datong table-level **59/41** carrier;
3. the historically attested reduction/threshold rule mapping C-II-N daily precision to the Sanming/Yueling whole-ke display.

Research record: `docs/research/ZIWEI-LEIBIAN-MING-FINE-TABLE-SANMING-TARGET-MISMATCH-R1.json`.
