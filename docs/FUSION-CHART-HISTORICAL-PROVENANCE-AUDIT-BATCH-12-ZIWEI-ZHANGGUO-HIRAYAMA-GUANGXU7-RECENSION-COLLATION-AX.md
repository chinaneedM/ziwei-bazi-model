# Fusion Chart Historical Provenance Audit R1 — Batch 12AX

## 《張果星宗大全》平山文庫光緒7序本卷7–8异本边界校勘与错误卷次纠正

Status: **TOHOKU HIRAYAMA MA/591 VOLUME ROUTE CORRECTED / GUANGXU-7-PREFACE V7–8 DIRECTLY REVIEWED / FEMALE-SECTION BOUNDARY LOCATED / 1594 NIGHT-ZI + ZI-HAI PASSAGE NOT OBSERVED ON THE IMMEDIATE PRECEDING REVIEWED LEAF / WRONG V5–6 NEGATIVE ROUTE QUARANTINED / RECENSION CONTROL ONLY / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Why this batch exists

Batch 12AW directly collated the Wanli-22 / 1594 NIJL-Tohoku physical witness at canvas 195. It established two facts: the main text discusses birth-time 子/亥 reciprocal misidentification, and the upper annotation records a 七政曆 night-Zi upper/lower four-ke division. AW deliberately did **not** convert those statements into an upper-Zi→Hai rule.

A follow-up automated locator initially opened Tohoku Hirayama record `10020000001143`, volume 5–6. That route was bibliographically real but mechanically wrong for the AW target proposition. AX corrects that route and prevents its OCR/non-hit results from becoming false negative textual evidence.

## 2. Correct Tohoku recension control

```text
record_id=10020000001144
title=新編評註通玄先生張果星宗大全
creator=陸位輯校
volume=卷之7-8
catalog_date=光緒7序
call_number=MA/591
former_owner=平山諦
image_count=89
```

This is a **later recension control**, not an earlier witness than 1594. The catalog label is 光緒7序; it must not be misdescribed as 正德 or Wanli.

## 3. Route correction

The earlier exploratory route `10020000001143 / 卷之5-6 / 正徳5` is retained only as acquisition provenance. Its OCR candidates and misses are **not** evidence that the AW target wording is absent from 《張果星宗大全》 or from volume 8.

```text
WRONG_VOLUME_NEGATIVE_EVIDENCE_AUTHORIZED=false
CORRECT_TARGET_VOLUME=7-8
```

## 4. Direct no-OCR visual boundary collation

The visual pack came from GitHub Actions run `34591234105`, artifact `10195723595`, digest:

```text
sha256:006af2fe24153f8b8d44fa5e05981a350fb17343aa9212868c514c80e71a843a
```

### 4.1 Image 57 — female-section anchor

Direct review securely shows:

```text
此段專命婦人之命
婦人以身福為重官星可作夫元
```

This locates the female-destiny boundary without OCR. Reviewed image SHA-256:

```text
3c4e174d21cab9722c39482b1ce1233eaeb476458f15c0b8c90fb3627b40f26c
```

### 4.2 Image 56 — immediate predecessor

The immediately preceding image was directly reviewed. It does **not** show either AW target component:

```text
人命多有生時不定，以子為亥，亥為子……
七政曆所載，有夜子時之分，有上四刻下四刻之法……
```

Reviewed image SHA-256:

```text
f0c93d6a4a4a475008cf130edc2772a0cec5b99ee6b209bdf768070fd6ee88a7
```

This is a leaf-scoped direct observation, **not** a whole-volume negative-search claim.

## 5. OCR locator control

Corrected full-volume locator run `34591055695` downloaded all 89 images. OCR was locator-only and returned `生時` hits at pages 25, 42, 47 and 84; it did not directly locate the AW target phrases. Its local evidence commit failed to push only because the remote branch advanced concurrently.

```text
OCR_ROLE=LOCATOR_ONLY_NOT_GLYPH_AUTHORITY
WHOLE_VOLUME_NEGATIVE_FROM_OCR=false
```

## 6. Philological adjudication

```text
1594 physical witness:
  target 子/亥 uncertainty wording = directly attested
  night-Zi upper/lower four-ke annotation = directly attested

Hirayama 光緒7序 volume 7-8:
  female-destiny boundary = directly located
  immediate preceding reviewed leaf = target passage not observed
```

This supports a **recensional difference/omission at the reviewed boundary**. It does not prove which layer authored or removed the passage, and it does not authorize an interpolation theory. The 1594 wording therefore cannot be mechanically assumed across later 《張果星宗大全》 recensions.

## 7. Effect on HPA-ZDATE-006

Nothing here supplies the missing mechanical bridge `upper/night Zi -> Hai branch`.

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_CANDIDATE_FAMILY=false
INDEPENDENT_TARGET_TEXT_WITNESS_INCREMENT=0
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
RUNTIME_WINNER_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

The 1594 AW page remains the controlling physical authority for its own wording. The later Hirayama recension is a transmission/stability control, not a second positive vote.

## 8. Accounting

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

No Historical Audit Matrix count changes are authorized.

## 9. Durable artifacts

```text
docs/research/ZIWEI-ZHANGGUO-HIRAYAMA-GUANGXU7-RECENSION-COLLATION-R1.json
docs/research/ZIWEI-TOHOKU-HIRAYAMA-MA591-V5-6-LOCATOR-R1.json  # retained but route-quarantined
```

## 10. Next gate

1. Directly read a Jangseogak 1594 target leaf or another independently bound 1594 copy to test same-edition stability.
2. Seek an earlier/independent witness explicitly stating the missing `upper/night Zi -> Hai branch` bridge.
3. Do not inflate evidence by repeatedly OCR-mining the same Hirayama recension unless a new mechanically material passage appears.
