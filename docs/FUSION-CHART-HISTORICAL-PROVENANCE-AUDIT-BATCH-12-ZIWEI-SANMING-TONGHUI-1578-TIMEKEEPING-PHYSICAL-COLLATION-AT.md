# Fusion Chart Historical Provenance Audit R1 — Batch 12AT

## 1578《三命通會》时刻原刻物理校勘、子时换日语义与恶劣天气时辰辨定边界

Status: **NCL 1578 PHYSICAL LOCATOR CORRECTED / 《論日刻》《論時刻》《論曰》 DIRECTLY COLLATED / 為昨日—屬今日 RECENSION GLYPHS PRESERVED / GENERIC HALF-ZI DATE ATTRIBUTION CONFIRMED / FULLBOOK HAI-BRANCH RECLASSIFICATION NOT PROVED / CLOUDY-RAIN SPECIFIC CLOCK INPUT STILL UNRESOLVED / NO GENEALOGY CLAIM / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

## 1. Question

Batch 12AS established in the 1613 physical 《圖書編》 witness:

```text
若子時則上半時在夜半前屬昨日
下半時在夜半後屬今日
```

It also showed actual clepsydra material, but did not close the Fullbook-specific mechanics:

```text
上五刻屬昨夜亥時
下五刻屬今日子時
陰雨之際必須羅經以定真確時候
```

Batch 12AT therefore asks whether a **chronologically earlier physical mantic witness**, the 1578 edition of Wan Minying's 《三命通會》, can directly establish:

1. the half-Zi previous/current-day relation;
2. the associated ke/clepsydra timekeeping system;
3. birth-time uncertainty around midnight and the Zi–Hai boundary; and
4. whether weather language plus timekeeping material is enough to close the Fullbook cloudy/rain acquisition chain.

The answer is:

```text
1 = YES, direct physical attestation
2 = YES, direct physical attestation
3 = YES, direct physical attestation
4 = NO, specific acquisition instrument/input remains unstated
```

## 2. Scope firewall

```text
S00_S19_INERRANT_AUTHORITY=false
MODERN_SOFTWARE_HISTORICAL_AUTHORITY=false
OCR_USED_FOR_GLYPH_CLAIMS=false
WRONG_LOCATOR_NEGATIVE_INFERENCE=false
RECENSION_GLYPH_NORMALIZATION=false
CHRONOLOGY_ALONE_PROVES_TEXTUAL_GENEALOGY=false
SANMING_1578_TEXTUAL_INDEPENDENCE_FROM_TUSHUBIAN_1613=UNRESOLVED
BORROWING_DIRECTION=UNRESOLVED
GENERIC_DATE_ATTRIBUTION_EQUATED_TO_HAI_BRANCH_RECLASSIFICATION=false
CLEPSYDRA_SILENTLY_INSERTED_INTO_FULLBOOK_CLOUDY_RAIN_SENTENCE=false
FULLBOOK_INCLEMENT_CLOCK_INPUT_CLOSED=false
RUNTIME_STANDARD_SELECTED=false
CANDIDATE_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

## 3. Locator correction: Commons suffix is a scan split, not a juan number

### 3.1 R1/R2 mistake

The first two Batch 12AT probes used:

```text
File:NCL-06589 2 三命通會.pdf
```

and inspected physical PDF pp34–44.

No target `論時刻` passage appeared there. That observation **must not** be converted into a content negative, because the locator premise was wrong.

The Commons/NCL object is split into two scan files. The filename suffix `1` / `2` identifies the **scan-file segment**, not `卷一` / `卷二`.

Therefore:

```text
NCL-06589 2 != 卷二
R1/R2 = LOCATOR MISS ONLY
R1/R2 CONTENT-NEGATIVE AUTHORITY = NONE
```

This is recorded as a forward-only research correction, not hidden or rewritten away.

### 3.2 Corrected source object

Controlling physical source:

```text
WORK=三命通會
AUTHOR=萬民英
EDITION=明萬曆六年（1578）刻本
COMMONS_FILE=File:NCL-06589 1 三命通會.pdf
SOURCE_SHA1=c222bc54815d8e5cef15338c03b9fc11d540f41a
SOURCE_SIZE=101956385
PDF_SHA256=3de5c45efb1919965afae00a3c97121054aaabd0f38f9fd5ab8f0a28bb8e36dd
PDF_PAGE_COUNT=1000
```

R3 broad direct contact review mapped the second physical book approximately to PDF pp101–188. R4 then rendered that bounded object at readable scale. R5 locked the four decisive PDF pages at high resolution with no OCR.

## 4. Machine evidence chain

### 4.1 Wrong-locator controls retained

```text
R1_RUN=34544127031
R1_ARTIFACT=10178374158
R1_DIGEST=sha256:9cb08047fbe368465284ba88f03c2169a41354047d499d76fc734b3df757a69e

R2_RUN=34544308980
R2_ARTIFACT=10178440876
R2_DIGEST=sha256:e0ca8f75d8347465996851791a145f5b55038bee584e6aca3b99886765ba38cc
```

These are provenance for the locator correction only.

### 4.2 Corrected main-file mapping

```text
R3_RUN=34544892575
R3_ARTIFACT=10178643326
R3_DIGEST=sha256:f988ca9612b73129dba1786c21370d3244fba1143a26eaebbe59fc5104a8e4e7
```

R3 establishes the 1000-page main-file object and the physical-book boundary.

### 4.3 Readable juan-2 physical-book review

```text
R4_RUN=34545147295
R4_ARTIFACT=10178733130
R4_DIGEST=sha256:572cb4798f8b929c0d440cfb7e022f821d7ddb0fceb89fa5a67cf5462d4d4363
```

R4 narrows the target to the physical sequence containing `論日刻` / `論時刻` / following timing tables and `論曰`.

### 4.4 R5 target glyph lock

```text
R5_RUN=34545625767
R5_ARTIFACT=10178894706
R5_DIGEST=sha256:c4bf633e6a0f5e6c6ac1e4a79fe0e30ece4b597f779dc8bf747b7633d67c623f
```

Page-image hashes:

```text
PDF p132 = e664ec52aecc62b0ce292ca983c8930b77f904a6d8b4be2d38d8bf829d03ab11
PDF p133 = 937f36bd7238f89b82ec788e621f42631087b0de011923f845c38912ff59656d
PDF p136 = edc04e619928615b97bf798360834ca9b952629a26907c2ce329ebeec7f2b90f
PDF p137 = 418fc7bac1654a4ab4baafba6f8fe865e373d49d25521fd7470e7db8f26f7eeb
```

All glyph conclusions below come from direct visual review of these physical page renders, **not OCR**.

## 5. Direct physical collation

### 5.1 PDF p132 — 《論日刻》: clepsydra and hundred-ke day

The left physical leaf directly carries the heading:

```text
論日刻
```

and reads, in the relevant sequence:

```text
夫日一晝一夜十二時當均分於一日
故上智設銅壺貯水漏下壺箭……
一日之中有百刻之候也
```

Mechanical content:

```text
one day/night -> twelve double-hours
copper vessel + stored water + leakage -> timekeeping apparatus
one day -> hundred ke
```

Thus, in this exact 1578 mantic text, `刻` is not merely an abstract subdivision. The passage directly explains it through a water-clepsydra mechanism.

### 5.2 PDF p133 — 《論時刻》: half-Zi before/after midnight

The physical leaf directly carries:

```text
論時刻
```

and states the hundred-ke / twelve-shi subdivision, including eight large ke and two small ke per shi.

The decisive Zi-hour locus is physically read as:

```text
若子時則上半時在夜半前為昨日
下半時在夜半後屬今日
```

This Batch deliberately preserves the physical glyph asymmetry:

```text
1578 三命通會 = 為昨日 / 屬今日
```

It is **not normalized** into `屬昨日 / 屬今日` merely because later received texts or another recension use `屬` in both halves.

Mechanical reading:

```text
upper half Zi -> before midnight -> previous-day attribution
lower half Zi -> after midnight -> current-day attribution
```

What it does **not** say:

```text
upper half Zi -> Hai branch
```

`昨日` is a date attribution. It is not automatically equivalent to `昨夜亥時`.

### 5.3 PDF pp136–137 — 《論曰》: birth-time precision and Zi–Hai ambiguity

At the bottom sequence of p136 the physical text begins:

```text
論曰看命之法以時為低昂時有八刻初正之氣不同……
```

The continuation on p137 directly reads the critical passage:

```text
況夜半不分其日頓差子亥中間厥時難定
除初初正四刻餘六刻之間或陰晴倏忽寒煖迥別
人之生時果得其當也耶
余姑就授時曆分之要在智者密察而詳問之庶無悞矣
```

This is a high-value mantic operational witness because it places the following items in one continuous birth-time discussion:

```text
命理判断 depends on exact 時
初 / 正 subdivisions have different qi
夜半不分其日 -> day attribution can be badly wrong
子亥中間 -> difficult boundary
six non-anchor ke -> timing uncertainty remains
陰晴倏忽 / 寒煖迥別 -> environmental variability explicitly matters
授時曆 -> calendrical/time division reference
密察而詳問 -> close examination + detailed inquiry
```

The text therefore directly proves that the Zi–Hai / midnight issue was treated as a practical birth-time determination problem, not only an abstract calendrical note.

## 6. Philological comparison with Batch 12AS 《圖書編》 1613

Batch 12AS's 1613 physical witness reads:

```text
若子時則上半時在夜半前屬昨日
下半時在夜半後屬今日
```

Batch 12AT's 1578 physical witness reads:

```text
若子時則上半時在夜半前為昨日
下半時在夜半後屬今日
```

The functional orientation is the same:

```text
upper half -> previous day
lower half -> current day
```

But the glyphs are not identical. The direct 1578 witness has `為昨日`; the direct 1613 witness has `屬昨日`.

This difference is useful for recension control. It also proves why received-text normalization cannot be allowed to overwrite physical evidence.

However, chronology alone does not answer textual genealogy. Therefore:

```text
1578 SANMING -> 1613 TUSHUBIAN borrowing = NOT PROVED
1613 TUSHUBIAN -> 1578 SANMING borrowing = chronologically impossible for this edition, but later textual transmission remains a separate recension question
COMMON EARLIER SOURCE = POSSIBLE, NOT PROVED
TEXTUAL_INDEPENDENCE = UNRESOLVED
INDEPENDENT_VOTE_COUNT = NOT AUTHORIZED
```

The project may say the 1578 physical witness is **earlier**. It may not silently promote it to an independent textual tradition without stemmatic evidence.

## 7. Relationship to Fullbook late-Zi mechanics

### 7.1 What Batch 12AT strengthens

Batch 12AT now gives direct 1578 physical support for:

```text
A. midnight is the operative boundary inside Zi hour
B. the upper half before midnight belongs to the previous-day side
C. the lower half after midnight belongs to the current-day side
D. ke-level subdivisions are operationally significant in mantic birth-time work
E. Zi–Hai boundary time is explicitly described as difficult to determine
F. clepsydra timing is explicitly described in the same physical book
G. environmental conditions such as 陰晴 / 寒煖 are explicitly named in the birth-time caution
```

This materially improves historical provenance around the generic late-Zi problem.

### 7.2 What remains unproved

The Fullbook rule adds a stronger mechanical transformation:

```text
上五刻 -> 昨夜亥時
```

Batch 12AT only directly supplies:

```text
上半時 -> 夜半前 -> 昨日
```

That is not enough to rewrite the branch from Zi to Hai.

Therefore:

```text
GENERIC_PREVIOUS_DAY_ORIENTATION = SUPPORTED
FULLBOOK_HAI_BRANCH_RECLASSIFICATION = STILL SOURCE-SPECIFIC / NOT DERIVED FROM SANMING 1578
```

## 8. Cloudy/rain acquisition chain remains open

A tempting but invalid synthesis would be:

```text
三命通會 has 銅壺漏水
三命通會 birth-time caution has 陰晴
therefore 陰雨時 must use clepsydra
```

That inference is prohibited.

The 1578 text demonstrates both concepts in the same book, but the reviewed pages do **not** directly say:

```text
when cloudy/raining -> use clepsydra to obtain current birth time
```

Nor do they say:

```text
when cloudy/raining -> use luopan/compass alone as the clock input
```

The Fullbook sentence's exact acquisition mechanics therefore remain unresolved.

The evidence chain is currently:

```text
1578 三命通會:
  clepsydra = explicit timekeeping mechanism
  birth-time precision = explicit mantic concern
  Zi-Hai boundary = explicitly difficult
  weather variability = explicitly mentioned
  specific inclement-weather replacement input = absent from reviewed direct passage

1613 圖書編:
  clepsydra / astronomical calibration = explicit
  half-Zi date orientation = explicit
  Fullbook cloudy/rain input chain = not closed

Fullbook witness:
  cloudy/rain + 羅經 sentence = direct
  how 羅經 yields the required current clock-time value = still mechanically incomplete
```

No cross-source compositing may silently fill the missing edge.

## 9. Impact on HPA-ZDATE-006

Before Batch 12AT:

```text
HPA-ZDATE-006 = MISSING_FROM_PRODUCT
```

After Batch 12AT:

```text
HPA-ZDATE-006 = MISSING_FROM_PRODUCT
```

Reason:

- historical provenance of the generic half-Zi date split is stronger;
- the exact 1578 physical mantic witness is now locked;
- a recension glyph difference has been identified and preserved;
- but Fullbook-specific `upper five ke -> previous-night Hai branch` still cannot be generalized from this evidence;
- and the Fullbook cloudy/rain current-time acquisition chain remains incomplete.

So Batch 12AT is a **provenance refinement**, not a runtime-rule promotion.

## 10. Product / algorithm decision

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
FUSION_CHART_HISTORICAL_PROVENANCE_AUDIT_R1=IN_PROGRESS
HPA_ZDATE_006=MISSING_FROM_PRODUCT
RUNTIME_STANDARD_SELECTED=false
CANDIDATE_SELECTED=false
CANDIDATE_COLLAPSED=false
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
PREDICTION_AI_INTERPRETATION=CURRENTLY_OUT_OF_SCOPE
```

No deterministic chart code is reopened by this batch.

## 11. Counts

Batch 12AT does not add a new audit-matrix row and does not resolve an existing missing candidate into product runtime.

```text
ROW_COUNT=198
AUDITED_ROW_COUNT=166
MISSING_FROM_PRODUCT=10
IDENTIFIED_MISSING_CANDIDATES=14
CONFIRMED_PROVENANCE_DEFECTS=11
REPAIRED_PROVENANCE_DEFECTS=11
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

## 12. Durable research artifact

Machine-readable record:

```text
docs/research/ZIWEI-SANMING-TONGHUI-1578-TIMEKEEPING-PHYSICAL-COLLATION-R1.json
```

It preserves:

- the R1/R2 locator error and fail-closed interpretation;
- corrected NCL source identity and hashes;
- R3/R4/R5 run/artifact/digest chain;
- decisive page hashes;
- direct physical transcription;
- the `為昨日 / 屬今日` recension reading;
- the distinction between date attribution and Hai-branch reclassification;
- the unresolved genealogy and inclement-weather acquisition edge;
- no-runtime/no-collapse/no-reopen guards.

## 13. Next research gate

Do **not** repeat the now-closed NCL 1578 locator search.

The next chart-affecting gate remains narrower:

1. find a direct Fullbook-line or demonstrably same-rule-family physical witness that explicitly links `陰雨` / unavailable solar-stellar observation to a **specific time-acquisition input or instrument**;
2. seek a physical witness whose wording explicitly bridges `上半子 / 上五刻` to `昨夜亥時`, rather than merely `昨日`;
3. keep edition/recension genealogy separate from mechanical similarity;
4. preserve every unresolved candidate until source-scoped mechanics justify promotion.

The 1578 《三命通會》 route itself is now adequately physically locked for this question.
