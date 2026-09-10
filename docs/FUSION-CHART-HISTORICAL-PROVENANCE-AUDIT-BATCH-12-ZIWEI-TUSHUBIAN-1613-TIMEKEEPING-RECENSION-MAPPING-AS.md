# Fusion Chart Historical Provenance Audit R1 — Batch 12AS

## 1613《圖書編》时令/刻漏物理卷次纠正与子时计时技术桥接

Status: **HARVARD 1613 PHYSICAL VOLUME MAPPING CORRECTED / V32 DIRECTLY BINDS 卷二十二《時令總敘》 / DIRECT 刻漏 + MIDNIGHT-SPLIT GLYPHS COLLATED / CROSS-RECENSION JUAN-NUMBER CONFLATION REJECTED / FULLBOOK CLOUDY-RAIN CLOCK INPUT STILL UNRESOLVED / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

## 1. Question

Batches 12AJ–12AR left one operational hole in the received Fullbook sentence:

> `陰雨之際必須羅經以定真確時候`

The direct Fullbook page is real, but a magnetic compass is not by itself a clock. Earlier Ming technical controls distinguish compass orientation from the actual day/night or inclement-weather time source.

Batch 12AS therefore asked two narrower questions:

1. can Zhang Huang's Ming technical/encyclopedic timekeeping material supply an independent early witness for Zi-hour division, clepsydra use and astronomical calibration; and
2. can that evidence legitimately close the Fullbook cloudy/rain current-time acquisition step?

The answer is **yes** to the first and **no** to the second.

A third issue emerged during acquisition: the target `juan` number is **not stable across the digital recensions encountered**. That locator defect had to be corrected before rule-text collation.

## 2. Scope firewall

```text
S00_S19_INERRANT_AUTHORITY=false
MODERN_SOFTWARE_HISTORICAL_AUTHORITY=false
OCR_USED_FOR_GLYPH_CLAIMS=false
CROSS_RECENSION_JUAN_NUMBER_EQUIVALENCE_ASSUMED=false
TUSHUBIAN_GENERIC_MIDNIGHT_SPLIT_EQUATED_TO_FULLBOOK_HAI_RECLASSIFICATION=false
TUSHUBIAN_CLEPSYDRA_SILENTLY_INSERTED_INTO_FULLBOOK_SENTENCE=false
FULLBOOK_INCLEMENT_CLOCK_INPUT_CLOSED=false
RUNTIME_STANDARD_SELECTED=false
CANDIDATE_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

## 3. Acquisition history and locator correction

### 3.1 R5/R6 — text-layer route fails closed

Harvard `圖書編 v.38.pdf` was first acquired as a possible internal `卷二十八` target. The PDF has no useful text layer for target-term location. The resulting zero keyword hits were correctly treated as **locator failure**, not textual absence.

### 3.2 R7–R10 — direct v.38 visual mapping

Visual contact sheets and targeted page renders established:

- Harvard physical `v.38` PDF p3 begins `圖書編卷之二十八`;
- internal `卷二十八` spans the physical object through PDF p33;
- PDF p34 begins `圖書編卷之二十九`;
- the reviewed internal `卷二十八` is the 天地/象纬-geographical sequence, not the required `時令/刻漏` target.

R10 controlling machine evidence:

```text
WORKFLOW_RUN=34542834591
ARTIFACT=10177906841
ARTIFACT_DIGEST=sha256:47e581a0406c66a4361e8d91fe25123d896179fce7817cb7a04dec337c0e5714
V38_PDF_SHA256=5bc02aef7421ea9f6be18fd5ab0e8a9289507b117e3e881ac488d50f5c84d886
```

This directly disproved the working assumption that “a digital `卷二十八` timekeeping transcription” could be mapped to Harvard `v.38` merely by equal juan number.

### 3.3 Received-text controls reveal recension numbering tension

The Siku received-text route places `時令總敘` in **卷二十二**. A separate Shidian digital surface headed `古今圖書編 / 圖書全編卷二十八` presents substantially the same `時令—百刻—刻漏` sequence under **卷二十八**.

The proper philological/edition rule is therefore:

```text
same or near-identical passage != same juan number across recensions
juan number is edition scoped
content identity requires textual collation
physical locator requires edition-specific mapping
```

The Shidian surface remains a navigation/transcription witness, not glyph authority for the Harvard object.

## 4. R11 — Harvard v.32 directly closes the physical locator

R11 resolved:

```text
COMMONS_FILE=File:Harvard drs 428499316 圖書編 v.32.pdf
PDF_SHA256=44512e7ca354ff94a87c7c5c84ddea61ba46812371707c2c4ecaf2a2d47f83ba
PAGE_COUNT=69
WORKFLOW_RUN=34543115889
ARTIFACT=10178011062
ARTIFACT_DIGEST=sha256:75fa4744df5f476218d6fd6f1645dfd6bc31d11d84346602f4334f285c829da8
```

Direct visual review of **PDF p3** reads:

```text
圖書編卷之二十二
時令總敘
```

This is the decisive correction:

```text
HARVARD_PHYSICAL_V32 -> INTERNAL_JUAN_22 -> 時令總敘 / 刻漏 MATERIAL
HARVARD_PHYSICAL_V38 -> INTERNAL_JUAN_28 -> NOT_THE_TIMEKEEPING_TARGET
```

The Harvard-Yenching Commons series describes the work as Zhang Huang's 127-juan `圖書編`, blockprint, published by Tu Jingyuan et al. in Ming Wanli 41 (1613). Independent National Central Library bibliographic records likewise bind 1613 Tu Jingyuan printings with 127 juan and 10 lines × 22 characters, providing edition-level corroboration without being counted as a second target-page textual vote in this batch.

## 5. R12 — direct physical glyph collation

R12 rendered Harvard v.32 PDF pp35–45 at high resolution with no OCR.

```text
WORKFLOW_RUN=34543260640
ARTIFACT=10178062853
ARTIFACT_DIGEST=sha256:1f30fd73e7958748f3c2b4740b62cace6a33e7f43059016b2772558a5f91ba77
```

### 5.1 p37 — physical clepsydra diagrams

The scan directly shows headings:

```text
古漏圖
今漏圖
```

This binds the surrounding discussion to actual clepsydra instrument forms rather than a purely metaphorical use of `漏`.

### 5.2 p38 — generic midnight previous/current-day split

The physical page directly reads:

```text
若子時則上半時在夜半前屬昨日
下半時在夜半後屬今日
亦猶冬至得十一月中氣一陽來復為天道之初耳
```

The same page discusses division of the hundred ke across the twelve double-hours and rejects the popular simplification that Zi/Wu/Mao/You each simply have nine ke.

Mechanical reading:

```text
upper-half Zi -> before midnight -> previous day
lower-half Zi -> after midnight -> current day
```

This is an independent Ming timekeeping witness for the **orientation of the midnight split**.

It is **not** mechanically identical to the received Fullbook rule:

```text
upper five ke -> previous-night Hai branch
lower five ke -> current-day Zi branch
```

`屬昨日` is a date attribution. `屬昨夜亥時` is a branch reclassification. The extra `亥時` mechanics may not be supplied by normalization.

### 5.3 p39 — `刻漏總論`

The physical scan has the heading:

```text
刻漏總論
```

and directly states:

```text
於是先王刻箭沃漏以揆之
故隋志曰黃帝創觀漏水制器取則以分晝夜
```

For this source, clepsydra is explicitly a day/night time-measurement instrument.

### 5.4 p41 — clock readings are calibrated against celestial motion

The physical scan directly reads:

```text
使挈壺氏專掌時刻
與儀象互相參考
以合天星行度為正
所以驗天數與天運為不差
則寒暑之氣候自正也
```

This is especially important mechanically. The water-clock/timekeeper layer is not treated as an autonomous astronomical truth source. Its readings are cross-checked with astronomical instruments and celestial motion.

That is consistent with the earlier Ming technical control in Batch 12AJ:

```text
day -> solar observation / sundial family
night -> stellar observation family
orientation -> compass
inclement conditions -> water-clock fallback
ultimate reference -> celestial motion
```

But consistency is not source identity.

### 5.5 p42 — finer solar-time structure

The page further states:

```text
且世人止知十二時耳
孰知一晝一夜而太陽之所臨有二十四時乎
```

The surrounding page discusses sunrise/sunset and twilight geometry. This reinforces that `時` in the chapter is embedded in observational solar/astronomical structure, not merely a modern fixed-clock label.

## 6. Bibliographic control

Independent public bibliographic witnesses were checked for edition context.

National Central Library records identify `圖書編` by Zhang Huang as:

- Ming Wanli guichou / Wanli 41 (1613);
- Tu Jingyuan et al. printing;
- 127 juan;
- 10 lines × 22 characters;
- one record as the 1613 print, another as a 1613 print / 1623 Yue Yuansheng impression lineage.

These records corroborate the edition family and physical format. This batch does **not** claim that the NCL copies' target pages were visually collated or that they are independent textual-stemma votes.

## 7. Philological adjudication

The evidence supports the following distinctions.

### 7.1 `屬昨日` vs `屬昨夜亥時`

They share a midnight-orientation dimension but not complete mechanics.

```text
TUSHUBIAN: upper-half Zi belongs to previous day
FULLBOOK: upper-five Zi is reclassified as previous-night Hai hour
```

Therefore:

```text
PARTIAL_MECHANICAL_OVERLAP != SAME_RULE
```

### 7.2 `漏` as a clock vs Fullbook `羅經`

`圖書編` directly establishes that clepsydra is a genuine time-measurement system and that timekeeper readings can be calibrated against astronomical motion.

It does **not** say:

```text
when a Ziwei birth occurs in cloudy/rainy weather, use this clepsydra together with a compass
```

Nor does the reviewed target sequence provide a direct Fullbook-specific `陰雨` clause.

Accordingly the following inference remains forbidden:

```text
Fullbook says 羅經 + Tushu Bian knows 刻漏
=> Fullbook 羅經 sentence secretly means 羅經+刻漏
```

That would be evidence invention, not 训诂.

### 7.3 `juan 28` is not a portable locator

The mismatch between the Harvard/Siku line and the alternate digital numbering is itself a provenance lesson:

```text
卷號 is recension-scoped metadata
章節文字 + sequence + physical title leaf are stronger identity keys
```

Future research locators must bind `edition/object -> physical volume -> internal juan -> section`, rather than search by bare juan number.

## 8. HPA-ZDATE-006 effect

No chart-affecting state changes.

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_SOURCE_SCOPED_TIMEKEEPING_WITNESS=1
GENERIC_MIDNIGHT_SPLIT_ORIENTATION=STRONGLY_CORROBORATED_BY_1613_DIRECT_PHYSICAL_WITNESS
FULLBOOK_HAI_BRANCH_RECLASSIFICATION_CROSS_SOURCE_EQUIVALENCE=NOT_PROVEN
FULLBOOK_INCLEMENT_CURRENT_TIME_ACQUISITION=UNRESOLVED
RUNTIME_TIME_STANDARD_SELECTED=false
CANDIDATE_SELECTION=NO
CANDIDATE_COLLAPSE=0
CHART_ALGORITHM_DEFECT=0
ALGORITHM_REOPEN=0
MATRIX=198/166
CURRENT_MISSING_FROM_PRODUCT=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
PROVENANCE_DEFECTS=11_CONFIRMED/11_REPAIRED
```

This batch is a **source locator / edition mapping repair and technical-context strengthening**, not an implementation defect.

## 9. Next gate

Batch 12AS removes one major ambiguity: early Ming/Qing-era timekeeping discussion can be physically grounded without treating `羅經` as a clock, and the generic midnight split is independently witnessed in a 1613 physical print.

The remaining chart-affecting gate is narrower than before:

1. find a Fullbook-line, early Ziwei, or demonstrably relevant contemporary operational witness that explicitly connects **cloudy/rainy birth-time acquisition** to the actual timekeeping instrument/input;
2. continue independent physical collation where it can distinguish `屬昨日` from `屬昨夜亥時`, rather than merely accumulating identical secondary transcriptions;
3. do not select civil, local-mean-solar, apparent-solar, compass-only or clepsydra-composed runtime coordinates until a source-scoped mechanical chain is complete.

Machine evidence:

`docs/research/ZIWEI-TUSHUBIAN-1613-TIMEKEEPING-RECENSION-MAPPING-R1.json`
