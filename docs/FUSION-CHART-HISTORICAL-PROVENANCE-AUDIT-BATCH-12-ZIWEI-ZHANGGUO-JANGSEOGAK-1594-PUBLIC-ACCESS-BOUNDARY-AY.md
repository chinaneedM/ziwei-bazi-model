# Fusion Chart Historical Provenance Audit R1 — Batch 12AY

## 《张果星宗大全》藏书阁万历二十二年本公开访问边界审计

Status: **JANGSEOGAK 1594 HOLDING CATALOG IDENTITY CONFIRMED / SECOND UNDATED HOLDING CONFIRMED / ADJACENT MF-PDF CONTROL VERIFIED / 15 OBJECT-SPECIFIC TARGET PDF ROUTES RETURN 404 HTML / TARGET LEAF NOT OBTAINED / ACCESS FAILURE IS NOT TEXTUAL ABSENCE / ZERO TEXT OR HAI-GLYPH VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Why this batch exists

Batch 12AW established a direct 1594 physical witness for the Zhangguo passage and Batch 12AX showed that a later Hirayama recension differs at the reviewed boundary. The highest-value next question was therefore whether an independent 1594 holding could provide a second physical target-leaf collation.

Jangseogak exposes two catalog records for 《新編評註通玄先生張果星宗大全》. AY binds those holdings and then tests the public image/MF-PDF topology without converting an access failure into a textual negative.

## 2. Jangseogak holdings

### 2.1 Dated 1594 holding

```text
data_id=LIB_169178
display_call_number=PC9A-20
detail_call_number=C9A-20
mf_number=MF16/1453-1454
title=新編評註通玄先生張果星宗大全
catalog_date=萬曆22(1594)
edition_type=中國木板本
extent=10卷10冊:圖, 四周雙邊, 上黑魚尾;25.7 × 15.5cm
```

Official public record:

```text
https://jsg.aks.ac.kr/dir/view?dataId=LIB_169178
```

The public directory exposes bibliography / electronic-library / XML linkage, but no image link and no MF-PDF link for this object.

### 2.2 Second undated holding

```text
data_id=LIB_169177
display_call_number=PC9A-20A
detail_call_number=C9A-20A
mf_number=MF35/8437
title=新編評註通玄先生張果星宗大全
catalog_date=[刊年未詳]
edition_type=中國木板本
extent=10卷5冊:圖, 四周雙邊, 上黑魚尾;25.3 × 15.4cm
```

Official public record:

```text
https://jsg.aks.ac.kr/dir/view?dataId=LIB_169177
```

This holding is a separate access/recension control. Its unresolved catalog date must not be promoted to 1594 or to an early witness by inference.

## 3. Public-route positive control

The same Jangseogak directory visibly distinguishes items with digitized/MF-PDF access. Adjacent record `PC9A-23 / LIB_169174`, 《紫微斗數補遺》, exposes an MF-PDF link whose first book is a real public PDF:

```text
https://jsg.aks.ac.kr/data/serviceFiles/pdf/PC9A-23_001.pdf
```

This proves that the route pattern

```text
/data/serviceFiles/pdf/{display_call_number}_{book}.pdf
```

is genuine for at least a Jangseogak object that advertises MF-PDF access. It does **not** prove that every Jangseogak holding is digitized or publicly downloadable.

## 4. Object-specific target probe

GitHub Actions run and artifact:

```text
workflow_run_id=34593669934
artifact_id=10260891530
artifact_digest=sha256:10d7ee063b017464143f05dc9740903b40090ce65d782b1576c81fa9675b27fc
```

Routes tested:

```text
PC9A-20_001.pdf ... PC9A-20_010.pdf
PC9A-20A_001.pdf ... PC9A-20A_005.pdf
```

All 15 responses were:

```text
HTTP 404
Content-Type: text/html
response_bytes=1259
prefix_hex=3c21444f43545950  # <!DOCTYP
PDF magic=false
```

No live target PDF route and no rendered target book were obtained.

## 5. Scope discipline

The result authorizes only the following statement:

```text
THE_REVIEWED_PUBLIC_JANGSEOGAK_IMAGE_MF_PDF_ROUTE_DOES_NOT_EXPOSE_THE_TARGET_BOOK_BYTES
```

It does **not** authorize any of these statements:

```text
TARGET_PASSAGE_ABSENT=false_to_claim
WHOLE_HOLDING_NEGATIVE=false_to_claim
NO_INTERNAL_DIGITIZATION=false_to_claim
NO_REPRODUCTION_POSSIBLE=false_to_claim
```

Catalog identity and access topology are evidence; failure to retrieve target bytes is not text criticism.

## 6. Philological and witness accounting

Because no target leaf was obtained, AY performs no glyph adjudication and supplies no same-edition stability vote.

```text
PUBLIC_TARGET_LEAF_OBTAINED=false
DIRECT_GLYPH_COLLATION_AUTHORIZED=false
WHOLE_HOLDING_TEXT_NEGATIVE_AUTHORIZED=false
SAME_EDITION_TEXT_STABILITY_VOTE_INCREMENT=0
INDEPENDENT_TARGET_TEXT_WITNESS_INCREMENT=0
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
```

The 1594 AW physical leaf remains the controlling positive witness for its own wording. AY neither strengthens nor weakens the missing mechanical bridge `upper/night Zi -> Hai branch`.

## 7. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_CANDIDATE_FAMILY=false
RUNTIME_WINNER_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

No current runtime behavior changes are authorized.

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

## 9. External-action boundary

Jangseogak's public pages expose an institutional image-use/contact route. Requesting target-page imaging or reproduction is an external institutional action.

```text
REQUEST_SUBMITTED=false
USER_AUTHORIZATION_REQUIRED=true
```

No request is submitted in this batch. A future request may be made only with explicit user authorization and whatever request identity/contact data the institution requires.

## 10. Durable artifact

```text
docs/research/ZIWEI-ZHANGGUO-JANGSEOGAK-PUBLIC-ACCESS-BOUNDARY-R1.json
```

## 11. Next gate

1. Seek another publicly readable 1594, same-edition, or clearly near-edition physical witness and directly collate the target leaf.
2. Keep the Jangseogak institutional request route available but dormant until explicit authorization.
3. Continue searching for an independent historical witness that explicitly supplies the missing `upper/night Zi -> Hai branch` bridge; do not infer it from day-stem/day-date ownership language alone.
