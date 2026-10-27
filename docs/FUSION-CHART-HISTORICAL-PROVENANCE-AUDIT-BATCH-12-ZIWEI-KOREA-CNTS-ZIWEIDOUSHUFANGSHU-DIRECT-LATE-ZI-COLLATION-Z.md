# Fusion Chart Historical Provenance Audit R1 — Batch 12Z

## Korea National Library CNTS-00047996572 《紫微斗數方書》 / 《秘傳紫微》春岡藏 direct late-Zi collation

Status: **INSTITUTION-BOUND PHYSICAL MANUSCRIPT TARGET PASSAGE DIRECTLY COLLATE​D / 五神 AND 五凶神 COEXIST IN SAME PASSAGE / TEN-KE PREVIOUS-NIGHT CURRENT-NIGHT WORDING DIRECTLY OBSERVED / EXPLICIT 亥 ABSENT FROM EXACT TARGET SPAN / NANYANGTANG 亥時 NOT UNIVERSAL ACROSS BROADER RECEIVED TRANSMISSION / NO ALGORITHM EFFECT**

### 1. Post-12Y public sample controls

Run `34246929528` / artifact `10064408521` probed only source-emitted public images. Direct no-OCR review found:

- Gujiwu 67626: nine Dayuan images, limited to modern cover/front matter/contents; no target passage.
- 2book Jiwen: genuine old-print facsimile spreads are directly visible, but none contains `五凶神` or `子有十刻`.
- Guoxuezhan: retrieved images are UI/logo/QR-type assets rather than target book pages.
- A later “free Quark” locator resolves to the already-controlled SNU share `3b7b731e41f2`; it is the same SNU digitization lineage and is not an independent witness.

These controls add zero target-text votes.

### 2. New physical manuscript witness

A substantially stronger route was then located: National Digital Library of Korea / National Library of Korea object:

```text
CNTS-00047996572
master_bib_no=21581878
UCI=G701:B-00047996572
KOL200100663
catalog title=紫微斗數方書
edition=筆寫本
extent=2卷1冊; 34.2 x 23.3 cm
```

The institution-bound public-domain mechanical scan is mirrored on Wikimedia Commons. Its source metadata links back to the Korean national-library object. The public file is 153 pages.

Exact acquisition:

- run `34247945308`
- workflow head `b6343215b0aa8c6f16e3a1a1d95ccfbdcd3df89d`
- artifact `10064784871`
- artifact ZIP SHA-256 `64b1729df1523991a4ac764e8a4672cf7b6edeb41f94b56a47da49d5b17a6f95`
- source PDF: 75,687,209 bytes
- source PDF SHA-256 `b21bbf3e2c7cdada4153f847ff9f359dbb29e71998e1f931417d108b571b23c3`
- page count: 153

No authentication, purchase, identifier guessing, access-control bypass or OCR was used.

### 3. Physical identity

Direct visual review of PDF page 1 reads:

```text
秘傳紫微
春岡藏
```

This directly bridges the physical object to the received “春岡藏本 / 秘傳紫微” naming layer. The Korean catalog metadata separately identifies the object as `紫微斗數方書`, `筆寫本`, with keywords including `비전자미` and `춘강장`.

The exact copying date remains unresolved and is not inferred from later editions or secondary descriptions.

### 4. Direct target passage: PDF p124

The source scan itself, reviewed visually without OCR, directly contains:

```text
五神天殤天使奏書直符將軍
凡五凶神不可重犯惡殺不可合湊更加歲限合死若流年二限凡一二位者只作災重凡論人
```

This closes the prior philological ambiguity.

`五神` and `五凶神` are **not competing transcriptions of one heading on this physical page**. They occur sequentially in the same passage:

- `五神` introduces the five named spirits;
- the following prose calls the set `五凶神`.

Therefore:

```text
五神_TO_五凶神_SILENT_ONE_CHARACTER_CORRECTION=FORBIDDEN
RELATION=SAME_FIVE_ENTITY_SET_DIFFERENT_PHRASE_ROLES_IN_SAME_PHYSICAL_PASSAGE
```

This does not prove that Dayuan's unseen underlying page is identical to this manuscript, but it eliminates the assumption that a directory surface `五神` must simply be a dropped `凶`.

### 5. Direct late-Zi wording: PDF p125

The next physical page directly reads:

```text
命有稱兩時者可詳之子有十刻上五刻屬昨夜下五刻屬今夜
```

The exact target span contains:

```text
亥 = NOT OBSERVED
今夜子 = NOT OBSERVED
```

This is no longer a conclusion based on a modern transcription. It is direct manuscript glyph evidence.

### 6. Conflict adjudication

The two physical witness surfaces are now materially different:

**Nanyangtang Fullbook physical facsimile**

```text
子時有十刻上五刻屬昨夜亥時下五刻屬今日子時
```

**Korea Springgang manuscript**

```text
子有十刻上五刻屬昨夜下五刻屬今夜
```

The Korean manuscript directly supports the previous-night/current-night ten-ke division but does **not** perform the explicit upper-half `亥時` branch reclassification present in the Nanyangtang Fullbook.

The correct adjudication is therefore not source-count voting and not candidate collapse:

```text
EXPLICIT_HAI_RECLASSIFICATION_NOT_UNIVERSAL_ACROSS_BROADER_RECEIVED_TRANSMISSION
NANYANGTANG_HAI_METHOD=SOURCE_SCOPED
KOREA_SPRINGGANG_PREVIOUS_CURRENT_NIGHT_SURFACE=DIRECT_PHYSICAL_WITNESS
WITHIN_FULLBOOK_FAMILY_HAI_STABILITY=STILL_UNRESOLVED
```

Deep stemmatic genealogy between the Korean manuscript and Fullbook/Quanji printed traditions remains unresolved.

### 7. Product effect

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
DIRECT_PHYSICAL_TARGET_TEXT_WITNESS_INCREMENT=1
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
NEW_MISSING_CANDIDATE_FAMILY=NO
NEW_CHART_RULE_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
```

The deterministic product remains CLOSED.

The next high-value gate is a direct target page from another **Fullbook** physical edition (Dunhuatang, Jishutang, Jingluntang, Wenchengtang or an equivalent independently bound witness), followed separately by a source-justified runtime time-standard binding before any product implementation decision.
