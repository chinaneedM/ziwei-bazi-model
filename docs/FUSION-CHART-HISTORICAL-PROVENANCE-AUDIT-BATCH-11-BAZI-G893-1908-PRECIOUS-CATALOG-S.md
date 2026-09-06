# Fusion Chart Historical Provenance & School Audit R1

## Batch 11S - G893 and the 1908 Kyujanggak Precious-Book Catalog

Status: **COMPLETE FOR DIRECT NO-OCR TITLE-PRESENCE REVIEW; NEGATIVE CATALOG WITNESS ONLY**

Batch ID: `BATCH-11-BAZI-G893-1908-PRECIOUS-CATALOG-S`

Machine-readable evidence:

- `docs/research/KYUJANGGAK-G893-PREWAR-COLLECTION-CONTINUITY-R1.json`
- `docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json`

This batch tests one narrow provenance question opened by Batch 11R:
whether the title `授時曆立成` is visibly present in the surviving 1908
`貴重圖書目錄`.

It does not inspect any G893 target table and has no runtime effect.

## 1. The 1908 catalog was directly bound to its official digital object

The live Kyujanggak provider exposes the 1908 `貴重圖書目錄` as:

- call number: `古016.09-G995`;
- `BOOK_CD=GR35006_00`;
- `ITEM_CD=BBG`;
- extent: `1冊(13張)`.

The official front-end JavaScript itself defines:

```text
fn_mfPdf(book_cd, vol_no)
    -> /book/mfPdf.do?book_cd=<BOOK_CD>&vol_no=<VOL_NO>
```

The project therefore used the provider-derived route:

```text
/book/mfPdf.do?book_cd=GR35006_00&vol_no=0001
```

and received the original PDF directly.

Direct PDF evidence:

- workflow run: `34031551270`;
- head SHA: `3ab11fe651c2f24ae0515eb8d278de84ca9ce3e0`;
- artifact: `9988774086`;
- bytes: `1,746,005`;
- SHA-256:
  `b4b7b14229a82f3f5da12dc069cf8943b1d4c1ff7ca0aa87e85eb3e5d2b06328`;
- rendered scan pages: `17`;
- OCR used: **false**.

No guessed PDF URL, guessed book code, OCR transcription or filename-based folio
inference was used.

## 2. The complete 子部 range was visually bounded and reviewed

The rendered PDF was reviewed directly.

The visual section boundaries are:

- PDF page 9, left half: `子部` begins;
- PDF page 12, left half: `集部` begins.

Therefore the complete visually bounded `子部` material lies within the span
from PDF page 9 left half through PDF page 12 right-side material immediately
preceding the `集部` transition.

Within that complete child-section range, direct visual review found no visible:

- `授時曆立成`; or
- shortened `授時曆`.

The machine result is therefore:

```text
1908_PRECIOUS_CATALOG_授時曆立成_VISIBLE=FALSE
1908_PRECIOUS_CATALOG_授時曆_VISIBLE=FALSE
REVIEW_MODE=DIRECT_RENDERED_PAGE_VISUAL_REVIEW_NO_OCR
```

## 3. This is negative catalog evidence, not physical-absence evidence

The correct conclusion is only:

> this surviving 1908 precious-book catalog does not visibly list the target
> title in its complete 子部 range.

It does **not** establish any of the following:

- that the physical G893 object was absent from the Kyujanggak collection in
  1908;
- that the object had not yet entered the collection;
- that the modern `奎貴893` precious-book designation did not yet exist in
  another administrative form;
- that the Rufus 1936 Wang-Xun `授時曆立成` was a different copy;
- that the current G893 copy was created, rebound or recataloged after 1908.

Therefore:

```text
NEGATIVE_CATALOG_ENTRY_AS_PHYSICAL_ABSENCE=FORBIDDEN
CURRENT_PRECIOUS_STATUS_BACKPROJECTION_TO_1908=FORBIDDEN
NEGATIVE_CATALOG_ENTRY_AS_EXACT_ITEM_IDENTITY=FORBIDDEN
NEGATIVE_CATALOG_ENTRY_AS_PRINT_YEAR_EVIDENCE=FORBIDDEN
```

## 4. The prewar continuity problem is narrowed, not solved

The currently supported chronology is now:

1. 1908 `貴重圖書目錄`: target title not visibly listed in the complete
   `子部` range;
2. 1928-1930: official SNU history records transfer of the Kyujanggak
   collection to Keijo Imperial University;
3. 1936: Rufus directly reports an undated `授時曆立成` credited to Wang Xun
   in the Keijo University Library;
4. 1946: official SNU history records custody of the former Keijo Kyujanggak
   collection passing to SNU without change in volume count or place of
   preservation;
5. current provider: `奎貴893 / GK00893_00`, Wang-Xun-attributed, 102 leaves.

This creates a useful negative/positive bracket, but exact individual-copy
continuity remains:

```text
EXACT_ITEM_CONTINUITY_TO_CURRENT_GK00893_00=UNRESOLVED
```

The next high-value control is the 1912 catalog, followed by direct reading of
the 1930 numeric-order catalog entry.

## 5. Six G893 target controls remain fail-closed

No target-page value is added:

1. `VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE`;
2. `VAR-NUM-LUNAR-L8-LOSSGAIN`;
3. `NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING`;
4. `VAR-NUM-LUNAR-L114-DAYRATE`;
5. `VAR-NUM-LUNAR-L124-JI-XINGDU`;
6. `VAR-NUM-LUNAR-L132-LOSSGAIN`.

All remain `PENDING_DIRECT_TARGET_PAGE`.

## 6. Runtime and audit-count consequence

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

## 7. Next work

1. directly review the 1912 Kyujanggak catalog for `授時曆立成` or a
   copy-specific identifier;
2. directly read the 1930 `奎章閣圖書番號順目錄` entry and bind any old
   identifier to current `奎貴893`;
3. inspect 1920 and 1940 catalog controls;
4. continue searching prewar copy-specific physical or microfilm metadata;
5. continue G893 target-page acquisition independently.
