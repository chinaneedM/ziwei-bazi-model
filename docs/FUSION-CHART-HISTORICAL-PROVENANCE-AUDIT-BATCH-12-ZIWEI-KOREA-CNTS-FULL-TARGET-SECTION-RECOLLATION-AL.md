# Fusion Chart Historical Provenance Audit R1 — Batch 12AL

## Korea CNTS 《紫微斗數方書》 full target-section re-collation

Status: **DIRECT NO-OCR ADJACENT-PAGE RECOLLATION / KOREA TARGET LOCATION LACKS BOTH FULLBOOK EXPLICIT 亥 RECLASSIFICATION AND THE FOLLOWING 陰雨—羅經 CLAUSE / BROADER TRANSMISSION VARIANT CONFIRMED / NO FULLBOOK INTERPOLATION CLAIM / NO ALGORITHM REOPEN**

## 1. Why this re-collation was required

Batch 12Z directly established the Korean manuscript reading:

```text
命有稱兩時者可詳之子有十刻上五刻屬昨夜下五刻屬今夜
```

but the earlier evidence artifact deliberately made no whole-page or adjacent-page claim about the Fullbook's following sentence:

```text
如天氣陰雨之際必須羅經以定真確時候若差訛則命不凖矣
```

Batch 12AL therefore reopens **only the physical target-section collation**, using the already-bound 153-page manuscript scan and no OCR.

## 2. Physical source identity

The object is the same institution-bound physical manuscript already controlled in Batch 12Z:

- title: `紫微斗數方書`
- edition: `筆寫本`
- catalog author: `編者未詳`
- CNTS: `CNTS-00047996572`
- PDF SHA-256: `b21bbf3e2c7cdada4153f847ff9f359dbb29e71998e1f931417d108b571b23c3`
- 153 pages
- exact copying date: unresolved

Inherited acquisition:

```text
WORKFLOW_RUN=34247945308
ARTIFACT=10064784871
ARTIFACT_ZIP_SHA256=64b1729df1523991a4ac764e8a4672cf7b6edeb41f94b56a47da49d5b17a6f95
```

No new physical witness is counted.

## 3. Direct p125–126 re-collation

### p125

The rightmost target column directly reads:

```text
命有稱兩時者可詳之子有十刻上五刻屬昨夜下五刻屬今夜
```

Direct visual findings:

- no explicit `亥` glyph in the target span;
- no explicit current-`子` glyph after `今夜`;
- the immediately adjacent next textual column switches to a different `交限十年...` topic;
- the Fullbook `陰雨—羅經` sentence is not present after the target passage on the remaining target-location surface of p125.

Artifact-member JPEG SHA-256:

`6a09e465608f68af92190a85039de9e2031f50fc0b7cc167d722978960847023`

### p126

p126 is already a different limit-period discussion surface. It does not continue the p125 birth-hour target passage and does not supply the Fullbook `陰雨—羅經` sentence.

Artifact-member JPEG SHA-256:

`855361ffc06ee1cd6fe4ca25ef733d2c5102f583c8fa2d4425b1b49004644cb4`

This negative claim is **target-location / adjacent-page scoped only**. No whole-manuscript negative claim is made.

## 4. Cross-transmission result

Two directly reviewed Fullbook physical publisher-edition routes agree:

```text
上五刻屬昨夜亥時
下五刻屬今日子時
如天氣陰雨之際必須羅經以定真確時候...
```

The Korean manuscript instead has:

```text
上五刻屬昨夜
下五刻屬今夜
[then changes topic]
```

Therefore:

```text
EXPLICIT_HAI_RECLASSIFICATION_UNIVERSAL_ACROSS_BROADER_ZIWEI_TRANSMISSION=NO
FULLBOOK_LUOJING_CLAUSE_UNIVERSAL_ACROSS_BROADER_ZIWEI_TRANSMISSION=NO
WITHIN_REVIEWED_FULLBOOK_PHYSICAL_ROUTES_LUOJING_CLAUSE_STABILITY=YES
```

## 5. What this does not authorize

Batch 12AL does **not** authorize any of the following:

- claiming the Fullbook `羅經` sentence is a later interpolation;
- claiming the Korean manuscript is defective because it lacks the Fullbook clause;
- silently normalizing either source into the other;
- selecting one universal Ziwei late-Zi rule;
- selecting civil / mean / apparent-solar runtime time;
- reopening the deterministic chart algorithm.

The copy date and deeper stemma of the Korean manuscript remain unresolved.

## 6. HPA-ZDATE-006 effect

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
RUNTIME_TIME_STANDARD_BINDING=BROADER_ZIWEI_TRANSMISSION_VARIANT_CONFIRMED_FULLBOOK_OPERATIONAL_PROCEDURE_REMAINS_SOURCE_SCOPED_AND_RUNTIME_UNRESOLVED
NEW_PHYSICAL_WITNESS=0
NEW_TARGET_SECTION_CLAUSE_VARIANT_DIMENSION=1
NEW_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CANDIDATE_COLLAPSE=0
ALGORITHM_REOPEN=NO
```

## 7. Next gate

The next high-value gate is now even narrower: obtain a **Fullbook-line or sufficiently early related witness that explains the operational meaning of its own `羅經以定真確時候` clause**. Broader Ziwei transmission cannot be assumed to contain that clause at all.

Machine evidence: `docs/research/ZIWEI-KOREA-CNTS-FULL-TARGET-SECTION-RECOLLATION-R1.json`.
