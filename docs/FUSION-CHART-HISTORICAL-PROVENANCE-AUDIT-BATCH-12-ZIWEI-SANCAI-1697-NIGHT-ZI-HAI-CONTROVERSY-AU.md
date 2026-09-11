# Fusion Chart Historical Provenance Audit R1 — Batch 12AU

## 1697《三才發秘》夜子作亥歷史實踐、作者反駁與 Fullbook 上五刻屬亥規則的爭議譜系

Status: **HARVARD-YENCHING 1697 PHYSICAL WITNESS DIRECTLY COLLATED / 夜子作亥 HISTORICAL SHUSHU PRACTICE DIRECTLY ATTESTED / PRACTICE EXPLICITLY REJECTED BY AUTHOR / SAME-PROBLEM CONTROVERSY CONFIRMED / FULLBOOK TEXTUAL GENEALOGY UNRESOLVED / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / CLOUDY-RAIN INPUT STILL OPEN / NO ALGORITHM REOPEN**

## 1. Question

Batch 12AT physically established that the 1578《三命通會》 gives the generic midnight split:

```text
upper half Zi -> before midnight -> previous-day attribution
lower half Zi -> after midnight -> current-day attribution
```

but does **not** say that upper-half Zi becomes the Hai branch.

The Fullbook physical witness is stronger:

```text
子時有十刻
上五刻屬昨夜亥時
下五刻屬今日子時
```

The next narrow question is therefore historical rather than computational:

> Is `夜子 / 上半子 -> 亥` a demonstrably historical shushu practice, or is the Fullbook sentence an isolated wording that cannot yet be connected to a wider rule controversy?

Batch 12AU answers:

```text
HISTORICAL_PRACTICE_ATTESTED = YES
AUTHOR_ENDORSES_PRACTICE = NO
PRACTICE_WAS_CONTROVERSIAL = YES
FULLBOOK_GENEALOGY_PROVED = NO
RUNTIME_WINNER_JUSTIFIED = NO
```

## 2. Scope firewall

```text
S00_S19_INERRANT_AUTHORITY=false
OCR_USED_FOR_DECISIVE_GLYPH_CLAIMS=false
MODERN_TRANSCRIPTION_GLYPH_AUTHORITY=false
REPORTED_PRACTICE_EQUALS_AUTHOR_ENDORSEMENT=false
MECHANICAL_SIMILARITY_PROVES_GENEALOGY=false
SANCAI_EIGHT_KE_EQUALS_FULLBOOK_TEN_NAMED_POSITIONS=false
FULLBOOK_RULE_GENERALIZED_TO_ALL_SCHOOLS=false
RUNTIME_STANDARD_SELECTED=false
CANDIDATE_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

## 3. Source identity

The controlling physical object is Harvard-Yenching Library's scan:

```text
WORK=三才發秘
AUTHOR=陳雯
SECTION=天部卷二《原甲子日有兩子時》
COMMONS_FILE=File:Harvard drs 52822721 三才發秘天部二卷 v.3.pdf
COMMONS_SHA1=58b1b92aee55c190092e09c89b61993b4ca1ba40
PDF_SHA256=3c226eb8b1d70568e0ce6c5df7f4f4eae8c6ad35b44f6ed6ec47d78261786a11
PDF_PAGE_COUNT=76
```

Commons/Harvard metadata identifies the work as Chen Wen's《三才發秘》, Harvard-Yenching holding, with publication/imprint date 1697 inferred from the preface and with `德星堂寶翰樓藏版` in the authority metadata.

The received self-preface ends:

```text
康熙三十六年，歲次丁丑……
新安後學陳雯耕山氏識
```

That bibliographic material identifies the edition context. It is not used instead of the physical target pages for glyph claims.

## 4. Acquisition and locator correction

### 4.1 R1 broad window

The first physical acquisition correctly resolved the Harvard PDF but used a rough CText OCR-block-to-PDF-page estimate and rendered pp33–42.

```text
R1_RUN=34558586685
R1_ARTIFACT=10183491031
R1_DIGEST=sha256:3029f9747b3ac4e2f6bc062de4e631cbf877ee1825427008c76fdfd53bb40b9e
```

That physical window lies later in the volume. It is retained only as locator history:

```text
R1_TARGET_PAGE_HIT=false
R1_CONTENT_NEGATIVE_AUTHORITY=NONE
```

A locator miss is not textual absence.

### 4.2 Direct visual remapping

The physical chapter sequence was then reviewed forward from the preceding section. The target begins on PDF p16 and continues on p17.

No OCR was used to read the decisive glyphs.

### 4.3 R2 exact target lock

R2 rendered the exact pages at 400 dpi:

```text
R2_RUN=34559011255
R2_ARTIFACT=10183637134
R2_DIGEST=sha256:9df6312b4424a42243f4834e56252e07e087af4c8d56a9a3720479372da4af8a
OCR_USED=false
PDF_P16_SHA256=313e7196e348aaa7801042c528095c795aa2b3e8bce581b56c6a8da702bdaa6b
PDF_P17_SHA256=3fafcd95d7e60d7d1fcf350aecc35bdda5697b4fd9827d1555eeb8d516c998f7
```

## 5. Direct physical collation

### 5.1 PDF p16 — `原甲子日有兩子時`

The physical heading reads:

```text
原甲子日有兩子時
```

The decisive sequence states:

```text
子居正北之位前半子還屬陰原為昨日之辰
```

and then:

```text
至交正子方一陽生始為今日之辰
```

The same physical leaf later states the ke split:

```text
至於子時八刻前四刻為昨日辰後四刻為今日辰
```

Mechanical reading:

```text
pre-Zi-zheng half -> previous-day side
post-Zi-zheng half -> current-day side
Zi is internally divided at Zi-zheng
```

This agrees in orientation with the generic midnight split already physically established in 1578《三命通會》 and 1613《圖書編》.

But the source uses an **eight-ke / four-plus-four** presentation. It is not normalized into the Fullbook's `十刻 / 上五刻 / 下五刻` wording.

### 5.2 PDF p17 — direct attestation of `夜子作亥`

After listing the day-stem treatment of 正子 and 夜子, the physical page directly reads:

```text
今人不知此理
往往以夜子作亥
用于尅擇祿命
豈能協于天地之真機乎
```

This is the decisive new historical evidence.

It proves that, within the source's own contemporary polemical horizon, practitioners were in fact treating `夜子` as `亥`, and doing so in precisely the domains relevant to deterministic calendar/fate practice:

```text
尅擇
祿命
```

However, the rhetorical question shows that Chen Wen **rejects** that practice.

Therefore the correct evidentiary statement is:

```text
NIGHT_ZI_AS_HAI_PRACTICE_HISTORICALLY_ATTESTED=true
SANCAI_AUTHOR_ENDORSES_NIGHT_ZI_AS_HAI=false
CONTEMPORARY_RULE_CONTROVERSY_ATTESTED=true
```

The incorrect statement would be:

```text
三才發秘 teaches night Zi should be Hai
```

It does not.

## 6. Why this materially changes the Fullbook provenance picture

Before Batch 12AU, direct evidence looked like this:

```text
1578 三命通會:
  upper-half Zi -> previous day
  no direct Hai reclassification

1613 圖書編:
  upper-half Zi -> previous day
  no direct Hai reclassification

Fullbook:
  upper five positions -> previous-night Hai branch
```

The Fullbook's Hai step was therefore directly attested in the Fullbook line but not yet shown to belong to a wider historical shushu controversy.

After Batch 12AU:

```text
1697 三才發秘:
  authorial rule -> pre-Zi-zheng half remains previous-day-side night Zi
  reported practitioner rule -> 夜子作亥
  application domain -> 尅擇 / 祿命
  authorial judgment -> rejects 夜子作亥
```

This changes the historical classification from:

```text
FULLBOOK_HAI_RECLASSIFICATION = DIRECTLY_ATTESTED_BUT_HISTORICALLY_ISOLATED
```

to:

```text
FULLBOOK_HAI_RECLASSIFICATION = DIRECTLY_ATTESTED_AND_HAS_A_HISTORICALLY_ATTESTED_SAME_PROBLEM_SHUSHU_ANALOGUE / CONTROVERSY
```

That is a substantial provenance advance.

It means the Fullbook's rule must not be dismissed as a modern misunderstanding merely because 1578《三命通會》 and 1613《圖書編》 stop at previous-day attribution.

## 7. What Batch 12AU still does not prove

### 7.1 No direct textual genealogy

The physical similarity does not establish:

```text
Fullbook -> 三才發秘
三才發秘 -> Fullbook
common textual ancestor
same school lineage
```

Those are stemmatic questions and remain open.

### 7.2 No exact mechanical identity

The Fullbook says:

```text
子時有十刻
上五刻屬昨夜亥時
下五刻屬今日子時
```

The 1697 source says:

```text
子時八刻
前四刻為昨日辰
後四刻為今日辰
```

and separately reports that some practitioners `以夜子作亥`.

Those facts are highly relevant but not mechanically identical wording. The project may not silently rewrite one into the other.

### 7.3 No authorial vote for Hai

Chen Wen is evidence **for the existence of the dispute**, not a positive vote for Hai reclassification.

Evidence weighting therefore must distinguish:

```text
practice existence vote = positive
practice correctness vote from Chen Wen = negative
Fullbook textual rule vote = positive within Fullbook line
```

A simple source-count majority would be philologically wrong.

## 8. Candidate-policy consequence

This is exactly the class of evidence for which the project's candidate-preservation policy exists.

The historical record now directly contains competing operations:

```text
A. upper/night Zi retained as Zi but assigned to previous-day side
B. night Zi reclassified as Hai
```

The second operation is not hypothetical; it is historically attested. The first is also historically attested and explicitly defended by Chen Wen.

Therefore:

```text
DISPUTED_METHOD=TRUE
PRESERVE_SEPARATE_CANDIDATES=YES
SELECT_WINNER=NO
COLLAPSE_CANDIDATES=NO
```

This batch does not create a new candidate family because HPA-ZDATE-006 already represents the unresolved Fullbook late-Zi branch transformation. It refines that candidate's historical provenance.

## 9. Relationship to the cloudy/rain Fullbook sentence

Batch 12AU does not close the separate sentence:

```text
如天氣陰雨之際必須羅經以定真確時候
```

The current open chain remains:

```text
cloud/rain
-> Fullbook says 羅經
-> orientation/time-sector semantics partly understood
-> exact current-time acquisition input/mechanism still missing
```

No evidence from《三才發秘》 p16–17 supplies that missing edge.

Therefore the two subproblems must remain separate:

```text
upper-half/night-Zi branch controversy = materially advanced
inclement-weather current-time acquisition = unresolved
```

## 10. Effect on HPA-ZDATE-006

Before Batch 12AU:

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
```

After Batch 12AU:

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
```

But its historical status is refined:

```text
NIGHT_ZI_TO_HAI_HISTORICAL_PRACTICE=PHYSICALLY_ATTESTED
HISTORICAL_CONTROVERSY=PHYSICALLY_ATTESTED
FULLBOOK_HAI_RULE_IS_MODERN_INVENTION=DISPROVED_AS_A_GENERAL_CHARACTERIZATION
FULLBOOK_EXACT_GENEALOGY=UNRESOLVED
RUNTIME_WINNER=UNRESOLVED
```

The deterministic runtime remains unchanged because historical existence is not the same thing as adjudicated runtime priority.

## 11. Product / algorithm decision

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

No deterministic chart code is reopened.

## 12. Accounting

```text
ROW_COUNT=198
AUDITED_ROW_COUNT=166
MISSING_FROM_PRODUCT=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_PROVENANCE_DEFECTS=11
REPAIRED_PROVENANCE_DEFECTS=11
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

No matrix-row count changes are justified by this provenance refinement.

## 13. Durable research artifact

Machine-readable evidence:

```text
docs/research/ZIWEI-SANCAI-1697-NIGHT-ZI-HAI-CONTROVERSY-R1.json
```

It records:

- Harvard/Commons source identity;
- R1 locator miss without negative inference;
- R2 p16–17 physical target lock;
- PDF and page-image hashes;
- direct no-OCR glyph sequences;
- authorial rejection versus historical-practice attestation;
- comparison with the Fullbook;
- no-genealogy/no-runtime/no-collapse/no-reopen guards.

## 14. Next research gate

Do not repeat this Harvard p16–17 acquisition.

The next useful work is now two parallel lines:

1. search earlier or independent physical witnesses for `夜子作亥`, `夜子屬亥`, `上半子作亥`, or mechanically equivalent wording, to establish chronology and textual/school genealogy of the disputed operation;
2. continue independently searching for the missing Fullbook cloudy/rain **current-time acquisition mechanism**, because the 1697 witness does not close that problem.

Until those gates are resolved, the project must preserve both historically attested late-Zi operations rather than force a single winner.
