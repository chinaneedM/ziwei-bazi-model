# Fusion Chart Historical Provenance Audit R1 — Batch 12AF

## Shanghai Guangyi / Yulgok institutional direct late-Zi collation

Status: **YULGOK INSTITUTIONAL FOUR-BOOK COPY BOUND / SHANGHAI GUANGYI IMPRINT DIRECTLY OBSERVED / TARGET LEAF DIRECTLY OBSERVED / 昨夜亥時 CONFIRMED IN SECOND FULLBOOK PHYSICAL EDITION / STEMMATIC INDEPENDENCE NOT CLAIMED / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12AF closes the exact evidence gate left open by Batches 12I, 12J and 12AE: a directly readable `《論人生時要審的確》` target leaf from another physically bound Fullbook publisher edition rather than another mirror, catalog entry or modern transcription.

No OCR, login, identifier enumeration, purchase or access-control bypass was used.

## 2. Yulgok first-party four-book identity

The public Yulgok record identifies `新鑴希夷陳先生紫薇斗數全書` as a four-book lithographic holding. The public viewer tree itself directly lists the four exact item IDs:

```text
B005_01_B00320_001  新鑴希夷陳先生紫薇斗數全書 1
B005_01_B00320_002  新鑴希夷陳先生紫薇斗數全書 2
B005_01_B00320_003  新鑴希夷陳先生紫薇斗數全書 3
B005_01_B00320_004  新鑴希夷陳先生紫薇斗數全書 4
```

The viewer source itself embeds `imgItems` and defines the public preview-image path. Across the four viewers the manifests contain `7 + 4 + 4 + 4 = 19` representative images, all of which were fetched. This is not a claim that every leaf is publicly digitized.

## 3. Direct Guangyi imprint

Yulgok image `B005_01_B00320_001_004` (SHA-256 `2a714616b5d4a33642003658516fc7d109b1f33a13892ff93604f07ab38ddf67`) directly reads without OCR:

```text
陳希夷先生著
紫薇斗數全書
上海廣益書局印行
```

This binds the exact institutional B00320 holding to a Shanghai Guangyi physical Fullbook copy.

## 4. Direct target leaf

Yulgok image `B005_01_B00320_003_003` (SHA-256 `2d1fc5ce8459d3696166b0471b2075fee247ede94b73eb833d435fe54ee847e0`) directly exposes `紫薇斗數全書`, `卷三`, heading `論人生時要審的確`, and the decisive clause:

```text
如子時有十刻上五刻屬昨夜亥時下五刻屬今日子時
```

The exact physical glyphs therefore include both `昨夜亥時` and `今日子時` in this Guangyi copy.

## 5. Cross-edition adjudication

Batch 12A's direct Nanyangtang seven-juan facsimile reads the same decisive clause on its 卷五 target leaf. Batch 12AF now establishes the same reading in a Shanghai Guangyi physical edition whose target is visible in 卷三.

Therefore:

```text
NANYANGTANG_GUANGYI_DIRECT_PHYSICAL_HAI_AGREEMENT=RESOLVED
WITHIN_FULLBOOK_HAI_GLYPH_STABILITY=CONFIRMED_ACROSS_NANYANGTANG_AND_GUANGYI_DIRECT_PHYSICAL_EDITIONS
GLOBAL_ALL_FULLBOOK_EDITION_HAI_STABILITY=NOT_CLAIMED
STEMMATIC_INDEPENDENCE=NOT_CLAIMED
```

This is physical-edition corroboration, not proof of fully independent stemmatic descent. The Korea Springgang manuscript's directly observed non-Hai `昨夜 / 今夜` wording remains a broader Ziwei transmission variant and is not silently normalized away.

## 6. HPA-ZDATE-006 effect

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
DIRECT_FULLBOOK_PHYSICAL_TARGET_TEXT_WITNESS_INCREMENT=1
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=1
STEMMATICALLY_INDEPENDENT_BRANCH_INCREMENT=0
RUNTIME_TIME_STANDARD_BINDING=UNRESOLVED
NEW_CANDIDATE_FAMILY=NO
CANDIDATE_SELECTION=NO
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
```

The new evidence materially strengthens the source-scoped Fullbook candidate but does not decide whether a future runtime implementation must bind the historical half-Zi rule to civil time, mean solar time or apparent solar time. The deterministic fusion-chart product remains CLOSED.

## 7. Next gate

Further Fullbook work should broaden genuinely distinct target-leaf coverage (Huiwentang, Jinzhang, Wenguang/Dunhuatang/Jishutang, Jingshutang/Jingluntang, Wenchengtang or equivalent). Separately, productization still requires a source-closed runtime time-standard binding.

## 8. Machine evidence

`docs/research/ZIWEI-GUANGYI-YULGOK-DIRECT-LATE-ZI-COLLATION-R1.json`

## 9. Closure execution binding

Pending fail-closed closure workflow and exact-HEAD CI.
