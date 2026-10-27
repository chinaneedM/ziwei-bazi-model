# Fusion Chart Historical Provenance & School Audit R1

## Batch 11X - G893 Official Kyujanggak Reproduction Route

Status: **COMPLETE FOR OFFICIAL APPLICATION-ROUTE BINDING; NO REQUEST SUBMITTED AND SIX TARGET VALUES REMAIN FAIL-CLOSED**

Batch ID: `BATCH-11-BAZI-G893-OFFICIAL-REPRODUCTION-ROUTE-X`

Machine-readable evidence:

- `docs/research/KYUJANGGAK-G893-OFFICIAL-REPRODUCTION-ROUTE-R1.json`

This batch closes a practical acquisition question left after Batch 11V. Batch 11V proved that no downloadable G893 M/F PDF object is currently exposed through the tested online PDF route. Batch 11X separately establishes that the holding institution itself provides an official reproduction workflow capable of publishing microfilm scan PDFs after an approved request.

No institutional request is submitted in this batch.

## 1. The G893 object itself exposes a reproduction-request route

The official provider record directly identifies `授時曆立成 / 奎貴893 / GK00893_00 / 1冊(102張) / 甲寅字 / M/F73-102-37-A` and visibly exposes `열람복제 신청` / `방문 열람 자료 복제` controls.

Therefore the acquisition route is object-specific, not a generic suggestion to contact a library.

## 2. Official reproduction policy explicitly covers homepage publication

The Kyujanggak original-text service notice states that materials already public on the homepage may be used with source attribution; materials not public may be requested for reproduction; original-image reproduction is uploaded as a high-resolution edited old-document image; microfilm reproduction is uploaded as a scanned PDF; the procedure is homepage → material search → reproduction request → approval email; and normal processing is within two weeks unless delayed.

The notice gives 02-880-5316 for original-image reproduction and 02-880-5317 for microfilm reproduction.

## 3. Non-member workflow confirms the post-2024 delivery model

The public non-member reproduction-cart surface records a service change effective `2024-02-01`:

```text
postal paper-copy service
→ microfilm scan PDF file published on the homepage
```

The cart tracks call number, title, book count, M/F, source-text/image availability and selection state.

This does not establish whether G893 would be fulfilled as a complete one-volume scan or selected pages.

## 4. Relation to Batch 11V

There is no contradiction:

```text
Batch 11V:
CURRENT_PREEXISTING_MF_PDF_OBJECT =
CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED

Batch 11X:
FUTURE_OFFICIAL_REPRODUCTION_WORKFLOW =
DIRECTLY_CONFIRMED_REQUEST_NOT_SUBMITTED
```

An institutional workflow that creates and publishes a scan after approval is different from a PDF object already existing at `mfPdf.do`.

## 5. Strict unresolved boundaries

This batch does not establish approval, guaranteed two-week delivery, free service, whole-volume versus selected-page scope, future URL/file name, scan quality, target folio, or target glyph.

```text
G893_REPRODUCTION_REQUEST_SUBMITTED=false
G893_REPRODUCTION_APPROVED=false
G893_FULFILLMENT_SCOPE=UNRESOLVED
G893_FEE_STATUS=UNKNOWN_DO_NOT_INFER_FREE
```

## 6. Six numerical controls remain pending

All six controls remain `PENDING_DIRECT_TARGET_PAGE`. No service-policy statement is target-glyph evidence.

## 7. Runtime and audit-count consequence

```text
HISTORICAL_PROVENANCE_ROW_COUNT=197
AUDITED_ROW_COUNT=165
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

## 8. Next work

1. retain the official reproduction workflow as the highest-confidence G893 acquisition route;
2. do not submit an institutional request without explicit user authorization and required contact details;
3. continue parallel public-target-page and legitimate scholarly-fulltext searches;
4. after any future fulfillment, bind provider URL, file digest, page identity, table heading, target row and visible glyph before numeric adjudication;
5. keep all six controls fail-closed until direct surfaces are obtained.
