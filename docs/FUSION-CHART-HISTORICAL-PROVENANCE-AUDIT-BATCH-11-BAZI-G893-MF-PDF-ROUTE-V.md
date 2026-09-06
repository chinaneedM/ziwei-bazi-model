# Fusion Chart Historical Provenance & School Audit R1

## Batch 11V - G893 Microfilm PDF Route Closure

Status: **COMPLETE FOR CURRENT M/F PDF ACCESS ROUTE; SIX TARGET VALUES REMAIN FAIL-CLOSED**

Batch ID: `BATCH-11-BAZI-G893-MF-PDF-ROUTE-V`

Machine-readable evidence:

- `docs/research/KYUJANGGAK-G893-MF-PDF-ROUTE-R1.json`

This batch does not revisit the Batch 11U catalog-item identity closure and does not inspect a G893 computational target page. It closes one distinct digital-access route so future sessions do not repeatedly infer a downloadable PDF from the provider's M/F UI.

## 1. Why this route is distinct

The existing G893 renderer route is known to reset on equivalent GitHub-hosted Ubuntu, macOS and Windows probes. The M/F PDF route is a different provider interface:

- PDF-list endpoint: `POST /ajax/book/mfPdfList.do`;
- direct-PDF endpoint shape: `/book/mfPdf.do?book_cd={book_cd}&vol_no={vol_no}`.

The route shape is documented independently by the public `deweizhu/bookget` Kyujanggak adapter and `open-guji/bookget-py` Kyujanggak technical documentation. This batch therefore does not violate the prior prohibition against repeating equivalent hosted-runner renderer probes.

## 2. The M/F PDF list endpoint is reachable and returns the correct G893 object

Run `34044864073` / job `101518006693` completed successfully and the provider returned HTTP 200 JSON for `GK00893_00`.

The returned volume metadata directly included:

- `CALL_NUM = 奎貴893`;
- `ORI_TIT = 授時曆立成`;
- `BOOK_CD = GK00893_00`;
- `ITEM_CD = SIC`;
- `VOL_NO = 0001`;
- `TOTAL_CNT = 1`;
- `REL_MAIN_IMG = GK00893_00IH_0001_000a.jpg`;
- `REL_ADD_IMG = GK00893_00IH_0001_004b.jpg`.

This reconfirms object metadata only. It does not bind a target folio.

## 3. The server explicitly does not expose a current PDF directory

The same list response states:

```text
RESULT = ERROR - DIR NOT EXIST
```

and no volume entry carries `IS_PDF = Y`; the observed value is null.

Because the public adapter constructs `mfPdf.do` URLs only for entries whose `IS_PDF` is exactly `Y`, the response does not authorize treating the UI's `M/F PDF 보기` marker as proof of an available PDF.

## 4. Direct mfPdf.do control also returns no PDF object

A second probe, run `34044991699` / job `101518359210`, directly requested:

```text
https://kyudb.snu.ac.kr/book/mfPdf.do?book_cd=GK00893_00&vol_no=0001
```

The transport returned HTTP 200, but the body did not begin with the PDF magic `%PDF-`.

Machine result:

```text
mf_pdf_direct_transport_success = true
mf_pdf_direct_pdf_magic = false
direct_pdf_returned = false
route_status = NO_DIRECT_PDF_OBJECT_OBSERVED
```

Therefore:

```text
G893_CURRENT_MF_PDF_ROUTE = CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED
```

This conclusion is about the current online route only.

## 5. What this does not prove

The provider catalog still records microfilm number `M/F73-102-37-A`. Therefore `ERROR - DIR NOT EXIST` must **not** be converted into any claim that no physical microfilm or institutional reproduction exists.

The following inferences remain forbidden:

```text
MF_PDF_UI_MARKER_AS_DOWNLOADABLE_PDF_PROOF=FORBIDDEN
MICROFILM_CATALOG_NUMBER_AS_ONLINE_PDF_PRESENCE=FORBIDDEN
ERROR_DIR_NOT_EXIST_AS_PHYSICAL_MICROFILM_ABSENCE=FORBIDDEN
THUMBNAIL_FILENAME_AS_TARGET_FOLIO_BINDING=FORBIDDEN
TECHNICAL_ENDPOINT_SUCCESS_AS_TARGET_GLYPH_AUTHORITY=FORBIDDEN
```

## 6. Relation to Batch 11U

Batch 11U remains controlling for catalog-item identity:

```text
CATALOG_ITEM_CONTINUITY_TO_CURRENT_奎貴893=RESOLVED
EXACT_ITEM_CONTINUITY_TO_CURRENT_GK00893_00=RESOLVED_AT_CATALOG_IDENTIFIER_LEVEL
```

Batch 11V changes none of that. It only removes a false digital shortcut.

## 7. Six target controls remain pending

No G893 target page was obtained. The following remain `PENDING_DIRECT_TARGET_PAGE`:

1. `VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE`;
2. `VAR-NUM-LUNAR-L8-LOSSGAIN`;
3. `NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING`;
4. `VAR-NUM-LUNAR-L114-DAYRATE`;
5. `VAR-NUM-LUNAR-L124-JI-XINGDU`;
6. `VAR-NUM-LUNAR-L132-LOSSGAIN`.

No value is imported from Goryeosa, Ming editions, Ogawa, G894, Sillok or Kang-Bo.

## 8. Runtime and audit-count consequence

None.

```text
HISTORICAL_PROVENANCE_ROW_COUNT=197
AUDITED_ROW_COUNT=165
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

## 9. Next work

The next useful work is no longer an equivalent hosted-renderer retry or another speculative `mfPdf.do` request.

Priority is:

1. search public scholarly reproductions and legitimate mirrors for pages visibly carrying the exact target table headings and rows;
2. if public target pages remain unavailable, use the official Kyujanggak reproduction/consultation route for `授時曆立成 / 奎貴893 / GK00893_00 / M/F73-102-37-A`;
3. bind solar D16 only from a surface visibly containing `十六日` under the correct solar table schema;
4. bind lunar L8/L101/L114/L124/L132 only from surfaces whose table headings, limit numbers and field identity are directly visible;
5. keep all six values fail-closed until those direct surfaces are obtained.
