# Batch 12CQ — 楊瓚《閑中錄》北京晝夜精密計算物理校勘與《三命通會》父本捷徑排除

## Status

```text
YANGZAN_XIANZHONGLU_BEIJING_PRECISION_PHYSICAL_LAYER=CLOSED
YANGZAN_DIRECT_SANMING_59_41_PARENT=DISPROVED_BY_DIRECT_NUMERIC_ANCHOR_MISMATCH
SECURE_PRE1578_PHYSICAL_COPY_STATUS=NOT_ESTABLISHED
PRE1578_EXACT_PARENT=UNRESOLVED
PRE1578_SAME_CHANGE_DAY_FINGERPRINT=UNRESOLVED
EXACT_HISTORICAL_QUANTIZATION_RULE=UNRESOLVED
OCR_GLYPH_AUTHORITY=false
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
CANDIDATE_COLLAPSE=NONE
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 1. Why this batch exists

Batch 12CP physically closed the 1578 NCL-06589-1 《三命通會》 seasonal day/night-ke target and fixed its summer-solstice anchor at 59/41, while leaving the pre-1578 direct parent, same change-day fingerprint and exact quantization rule unresolved. The next-state gate explicitly named the Yang Zan route, but that route could not be used genealogically until the exact object, target pages and numerical mechanism were bound to a physical witness.

This batch closes that Yang Zan route at physical-page level and, more importantly, determines what it **does not** prove.

## 2. Exact source binding and date firewall

The public Shidian object identifies:

```text
BOOK_ID=NGJ89241199901864074070
TITLE=閑中錄前集
AUTHOR=楊瓚
RESPONSIBILITY=撰
PROVIDER_DYNASTY=明
PROVIDER_EDITION=明抄本
IMAGE_SOURCE=國家圖書館
CLASSIFICATION=子部 / 天文算法类 / 推步之属
CHAPTER=閑中錄前集正文
CHAPTER_PAGES=6..123
```

The date layers are deliberately separated:

```text
work composition date = unresolved in this batch
edition/impression date = not supplied as a dated print
physical-copy date = Ming manuscript per provider metadata; exact copying date unresolved
digital surrogate = modern Shidian route bound to National Library of China images
```

Therefore this batch does **not** call the surviving manuscript a securely pre-1578 physical copy, and does not identify a biographical Yang Zan merely from name coincidence.

## 3. Physical acquisition gate

The final browser-SDK gate is:

```text
R7_COMMIT=df34d24bc7d8d90b7cd5c35c8317f764aa1a5f59
WORKFLOW_RUN=35088687110
ARTIFACT=10442714003
ARTIFACT_DIGEST=sha256:d09d3327fc14d5453f9819e292b8ea610271015bcadf7d407d37a4c15ed75289
```

The route executes the site's own public reader chain in a real browser:

`page -> byted_psdk.getPtokenStatus -> pages/v3 -> byted_psdk.decrypt -> physical image`

The first request returned transient `40001`; after a fresh page/token cycle the second request returned `errorCode=0` and 37 pages. The gate is hard-failed unless all four requested physical pages 115–118 are downloaded. Thus the successful run cannot be satisfied by an empty API response.

| page | pageId | bytes | SHA-256 |
|---|---|---:|---|
| 115 | 7575481384166735924 | 2,090,880 | `b1dad12caa26bed26acb3c25455431b5fd6ce30ee891992cab08bd7968820193` |
| 116 | 7575481384166752308 | 2,187,078 | `fffe74fa40f80e3c98935d6463f880a3e0205f10f5fbb121f94d8770cd4118e5` |
| 117 | 7575481384166768692 | 2,117,052 | `1c39cdbf44e284ce53c5517e04794e3a17c286b27d730d7085452536c772683d` |
| 118 | 7575481384166785076 | 2,514,643 | `7c2a6989270d39837ab65656c8aeaf65a7ec816d3e0fd9c365fb53b7a9371611` |

Machine text was used only to locate the passage. All glyph and number claims below come from direct visual review of these images; OCR has no final authority.

## 4. Direct physical collation

### 4.1 p115 — locality and measured-difference layer

The page directly shows the heading `步中星` and `北京北極出地四十度`. The surrounding prose explicitly treats north/south location as mechanically relevant to polar elevation and sunrise timing, and scopes the following values to measured Beijing conditions.

The decisive numerical/mechanical lines directly include:

```text
内外差并晝夜差俱係新儀測定每日所差的數
晝夜總差五百九十二分〇四秒
```

This is not a free-standing fortune-telling mnemonic. It is a locality-bound astronomical/timekeeping computation.

### 4.2 p116 — solstitial extrema and dawn/dusk constant

The physical page directly prints:

```text
冬至晝夏至夜三千八百一十五分九十二秒
夏至晝冬至夜六千一百八十四分〇八秒
昏明分二百五十分
```

The same locus explains sunset-to-dusk and dawn-to-sunrise as approximately two and a half ke each.

### 4.3 p117 — half-values and daily recurrence

The physical page directly gives the half-values:

```text
冬晝夏夜半周一千九百〇七分九十六秒
夏晝冬夜半周三千〇九十二分〇四秒
```

It also explicitly instructs cumulative subtraction/addition of the internal/external and day/night differences to derive successive daily values. This is therefore a continuous precision computation layer rather than a 24-term integer display table.

### 4.4 p118 — passage boundary

p118 opens a new heading, `超神接氣論`. It functions here as a physical boundary control: the relevant `步中星` numerical mechanism is contained on pp115–117 rather than silently extended into the following topic.

## 5. Exact mechanical replay

The p115 total day/night difference is `592.04` fen. Taking the 10,000-fen day midpoint `5000`:

```text
5000 - 2 × 592.04 = 3815.92
5000 + 2 × 592.04 = 6184.08
```

These exactly reproduce p116. Halving them gives:

```text
3815.92 / 2 = 1907.96
6184.08 / 2 = 3092.04
```

which exactly reproduces p117.

Under the 10,000-fen = 100-ke coordinate, the solstitial extreme is therefore approximately:

```text
short side = 38.1592 ke
long side  = 61.8408 ke
```

By contrast, the exact 1578 《三命通會》 physical target closed in Batch 12CP is:

```text
夏至 -> 晝59 / 夜41
```

The two numerical fingerprints are not identical. Ordinary integer rounding of the Yang Zan values would be about 62/38, not 59/41.

## 6. Genealogical adjudication

The safe result is narrow but strong:

```text
Yang Zan physical witness ATTESTS a Beijing precision day/night computation layer.
It does NOT supply the Sanming 59/41 solstitial anchor.
It therefore cannot be promoted as Sanming's direct numeric parent merely because both discuss day/night length.
```

This is a `DISPROVES_LINEAGE_SHORTCUT` result, not a claim that the two works have no broader calendrical relationship. Same subject matter and possible shared technical background remain distinct from direct table parentage.

The unresolved Sanming ancestry questions remain:

1. which securely pre-1578 witness combines the Nanjing 59/41 cap with Sanming-like intermediate anchors;
2. which witness reproduces the Sanming intra-term change-day fingerprint;
3. what exact historical selection/quantization rule generated the displayed integer ladder.

## 7. Transmission impact

```text
nodes added/strengthened:
  - Shidian/National Library of China Ming-manuscript physical witness of Yang Zan 閑中錄前集
  - Yang Zan 北京晝夜精密計算 mechanical-rule node

edge supported:
  - physical manuscript ATTESTS Beijing precision rule

shortcut rejected:
  - Yang Zan Beijing precision rule -> Sanming 1578 direct numeric parent
    rejected because 61.8408/38.1592 != 59/41

not asserted:
  - exact work-composition date
  - securely pre-1578 surviving physical-copy date
  - direct copying between Yang Zan and Wan Minying
  - complete single-tree lineage
```

## 8. Product adjudication

This batch supplies no new chart-runtime rule and does not touch the Fullbook late-Zi issue:

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
RUNTIME_CHANGE=NONE
NEW_RUNTIME_CANDIDATE=false
ALGORITHM_REOPEN=NONE
CANDIDATE_COLLAPSE=NONE
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Audit accounting remains:

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
CUMULATIVE_IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
PROVENANCE_METADATA_DEFECTS=12/12_REPAIRED
```

## 9. Next gate

The Yang Zan route has now done its job: it narrows rather than closes the Sanming parent search. Priority returns to the Nanjing/Datong branch:

1. obtain direct `大統曆通軌 / 大統曆日通軌` morning-evening table cells, accepting that sunrise/sunset/half-day may be mechanically implicit in `晨昏分`;
2. continue securely pre-1578 annual Datong almanac/table searches for the Nanjing 59/41 cap plus the Sanming intermediate/change-day fingerprint;
3. test any candidate against the exact 1578 pp134–136 physical target rather than extrema alone;
4. keep exact parentage and quantization unresolved until a page-level witness reproduces the necessary fingerprint.

Research record:

`docs/research/ZIWEI-YANGZAN-XIANZHONGLU-BEIJING-PRECISION-PHYSICAL-COLLATION-R1.json`
