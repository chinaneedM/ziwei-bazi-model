# Fusion Chart Historical Provenance Audit R1 — Batch 12AO

## 1581《紫微斗數捷覽》完整公開錄文面與《全書》陰雨—羅經條款的早期傳承邊界

Status: **ALL FIVE SOURCE-EMITTED JIELAN PAGINATION PAGES REVIEWED / 246 CHAPTERS + 67,533 CHAR PUBLIC TRANSCRIPTION SURFACE / INCLEMENT-LUOJING TERMS NOT ATTESTED / BIRTH-TIME MATERIAL POSITIVE CONTROL PRESENT / NO PHYSICAL-BOOK NEGATIVE / NO INTERPOLATION CLAIM / FULLBOOK CLAUSE REMAINS SOURCE-SCOPED / INCLEMENT CLOCK INPUT UNRESOLVED / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

## 1. Question

After Batch 12AN established that a 24-mountain ring can carry time-sector coordinates while still requiring an external solar/astronomical anchor, the unresolved question remains:

> Is the Fullbook sentence `陰雨之際必須羅經以定真確時候` already visible in the earliest extant 1581 Ziwei print tradition, and does any early Ziwei surface explain the missing cloudy/rainy current-time input?

Batch 12AO answers the first question at the **complete current public transcription-surface level**, but not at physical-glyph level. It does not close the second question.

## 2. 1581 Jielan route

Registry identity for `EXT-ZIWEI-JIELAN-1581` remains:

- 《新刻纂集紫微斗數捷覽》
- 明萬曆九年（1581）
- 金陵書坊王氏洛川刊本
- bibliographic identity independently linked to Shanghai Library instance `子4051`.

The Tianji public transcription declares:

- 246 chapters
- 67,533 characters
- five pagination pages.

Batch 12AO did not guess `?p=` values. It started from the book root and followed only same-book pagination URLs literally emitted by already fetched pages. After URL fragments were canonicalized, the source-emitted traversal fetched exactly pages 1–5, each once.

Controlling run:

```text
WORKFLOW_RUN=34341036879
ARTIFACT=10099727992
ARTIFACT_ZIP_SHA256=75cf90fcfbdf4df9728dfec0bbc5c7d69c23e40922001a78e4421beeef3cb7fd
```

Page hashes:

```text
p1 9f2d56bbf53d85abc39f4c4f8dbdba1af56fb7933f01cbf0b848b429a8c7379b
p2 4ebf043f37574c79ec6c5d686adac9517cc2ecaf81780c23dbef45f8c5feedad
p3 d3b54153e565510eaa76ff3b45cbbeeb72eda6395c532c59539a69610b9b532a
p4 834bd43f852962b62fd82ae7846e73fbaa833f9f86977caee9b899287e9cd5ac
p5 d61947e2ddb40efd8bdca66fbed902562634b9c4da77e33522f07db052389471
```

## 3. Positive control and negative result

The public Jielan transcription is not devoid of birth-time material. It positively contains chapter labels corresponding to `定小儿生时` / `生时成形论`.

Across all five pages, however, the following terms are not attested in either configured traditional/simplified variants where applicable:

- `論人生時要審的確`
- `人生子亥二時`
- `子時有十刻`
- `陰雨`
- `羅經`
- `真確時候`
- `行漏`
- `壺漏`
- `指南針`

This supports a real **current public transcription-surface nonattestation** in the early 1581 Jielan tradition.

It does **not** authorize a whole-physical-book negative, because the 1581 facsimile target pages were not directly reviewed in this batch.

## 4. Fullbook control

Wikisource卷三 directly exposes the received Fullbook section `論人生時要審的確` and the configured terms `人生子亥二時`, `子時有十刻`, `陰雨`, `羅經`, `真確時候`.

More importantly, prior batches already bind the corresponding Fullbook clause to direct Nanyangtang and Guangyi physical facsimile routes. Therefore 12AO does not treat the received digital text as the sole authority for the Fullbook reading.

## 5. Ming technical control remains unchanged

The same AO cross-surface probe also re-hit the already controlled Ming calendar-bureau technical text in 《新法算書》:

- `晨昏陰雨`
- `行漏`
- `壺漏`
- `羅經`
- `指南針`

Its previously established mechanical division remains controlling for technical semantics:

```text
day -> sundial
night -> star dial
meridian/orientation -> compass
cloudy/rainy -> clepsydra / running water clock
```

This does not prove that the Fullbook sentence secretly meant `行漏`; it merely shows that a contemporaneous technical system did **not** use the magnetic compass itself as the inclement-weather clock input.

## 6. Philological adjudication

The evidence now supports four separate statements:

1. The Fullbook inclement-Luojing clause is directly real in reviewed Fullbook physical routes.
2. The same clause/terminology is absent from the complete current Tianji public transcription surface of the 1581 Jielan.
3. That absence is an early Ziwei transmission-variant dimension, not proof of interpolation, corruption, or authorial chronology.
4. The missing mechanical step — how a Fullbook practitioner obtained **current time under cloud/rain** — remains unobserved.

Accordingly, the following are still forbidden:

- silently inserting `行漏` into the Fullbook sentence;
- declaring the Fullbook clause an interpolation from the Jielan transcription non-hit;
- declaring the 1581 physical print itself negative without direct facsimile review;
- selecting civil, mean-solar, true-solar, or apparent-solar runtime;
- collapsing a candidate or reopening deterministic chart algorithms.

## 7. HPA-ZDATE-006 effect

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
RUNTIME_TIME_STANDARD_BINDING=EARLY_1581_JIELAN_COMPLETE_PUBLIC_TRANSCRIPTION_NONATTESTATION_CONFIRMED_FULLBOOK_INCLEMENT_LUOJING_CLAUSE_REMAINS_SOURCE_SCOPED_AND_CLOCK_INPUT_UNRESOLVED
NEW_FULLBOOK_TEXTUAL_WITNESS=0
NEW_HAI_GLYPH_WITNESS=0
NEW_EARLY_ZIWEI_TRANSCRIPTION_VARIANT_DIMENSION=1
NEW_DIRECT_PHYSICAL_WITNESS=0
CANDIDATE_SELECTION=NO
CANDIDATE_COLLAPSE=0
ALGORITHM_REOPEN=NO
```

Accounting remains 198 rows / 166 audited / 10 current MISSING_FROM_PRODUCT / 14 cumulative missing candidate families / provenance defects 10 confirmed and 10 repaired / algorithm defect-reopen-collapse all zero.

## 8. Next gate

Two evidence routes now have priority:

1. obtain direct physical target-section review of the 1581 Jielan, so the transcription-surface nonattestation can be tested against the actual print;
2. continue searching Fullbook-line or sufficiently early independent Ziwei witnesses for an explicit cloudy/rainy **current-time acquisition mechanism**.

Until one of those routes produces stronger evidence, the Fullbook operational chain remains fail-closed.

Machine evidence: `docs/research/ZIWEI-JIELAN-INCLEMENT-TIME-ACQUISITION-R1.json`.
