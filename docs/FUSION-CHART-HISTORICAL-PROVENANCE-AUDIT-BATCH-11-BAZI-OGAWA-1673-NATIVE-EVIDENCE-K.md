# Fusion Chart Historical Provenance & School Audit R1

## Batch 11K - Ogawa 1673 Native Evidence Package and Independent Holding

Status: **COMPLETE FOR NATIVE EVIDENCE PACKAGE + BIBLIOGRAPHIC CORROBORATION; FOUR TARGET DIPLOMATIC READINGS REMAIN OPEN**

Batch ID: `BATCH-11-BAZI-OGAWA-1673-NATIVE-EVIDENCE-K`

This batch closes a narrow provenance/access milestone around the Japanese received witness `EXT-NDL-OGAWA-SHOUSHI-LICHENG-1673`. It does **not** close the unresolved D16/L8/L101/L132 glyph readings and it does not authorize any chart/runtime change.

## 1. Exact remote evidence package

At exact source commit `f90477b4247f6c7bfc70f58f68082c0638947cf5`, workflow `research-ndl-ogawa-shoushi-licheng-target-pages` run `33977235461` completed successfully and emitted artifact `9972676923`:

- artifact name: `ndl-ogawa-target-pages-f90477b4247f6c7bfc70f58f68082c0638947cf5`
- artifact size: `29,096,181` bytes
- artifact digest: `sha256:81c99a8952dfbabf80c9d2cb9e95093b06aca734bf9a7d19e1c70d3ec567e216`
- requested native canvas width: `7392px`
- localized pages: solar D16 page, lunar structural header, L8, L101, L114 and L132 pages
- OCR: **not used**

The workflow success proves that the high-resolution page package was emitted. It does **not** itself prove any target numeral. `FETCH_SUCCESS != DIPLOMATIC_READING` remains an explicit evidence firewall.

## 2. NDL bibliographic identity

NDL Search independently exposes the 1673 bibliographic identity for the work:

- title: `大元授時暦經立成 6巻`
- creator: `小川正意新勘`
- publisher: `田原仁左衛門`
- date: `寛文13 [1673]`
- NDL Search record: `https://ndlsearch.ndl.go.jp/books/R100000136-I1970023484922964747`

This is bibliographic authority for edition/work identity, not target-glyph authority.

## 3. Independent same-year holding: Kyushu University

NDL Search also exposes an independent public digital holding at Kyushu University:

- title container: `大元授時暦經 巻上下, 巻1-6`
- creator: `小川, 正意`
- publisher: `田原二左衛門`
- date: `寛文13年` / 1673
- note: bound with `大元授時暦經立成 6巻`
- collection: `九州大学附属図書館・九大コレクション貴重資料`
- public access: Internet public / Public Domain
- IIIF manifest: `https://catalog.lib.kyushu-u.ac.jp/image/manifest/1/820/6631038.json`
- NDL Search record: `https://ndlsearch.ndl.go.jp/books/R100000092-I2324_6631038`

This creates an independent same-year, same-work image-collation route. No NDL-to-Kyushu scan offset is assumed. Each target must be rebound by printed title/table/limit headings before any same-edition comparison.

## 4. Evidence boundaries retained

The pre-existing direct reading remains:

- L114: `九日三四八九` -> normalized `9日3489`, HIGH confidence.

Still unresolved from the NDL native package until human/direct visual transcription binds the exact field column:

- D16 difference;
- L8 損益;
- L101 positional grouping;
- L132 損益 compact surface.

L124 remains explicitly non-comparable in the inspected Ogawa volume-2 structure: the prior R0000019 overbinding is rejected, and absence of a separate identified 行度 field cannot be converted into numeric zero, equality, or a transmission variant.

## 5. Philological implications

The independent Kyushu holding is valuable precisely because it can separate three different questions that must not be collapsed:

1. **edition/work identity** — already bibliographically corroborated;
2. **same-edition physical surface agreement** — requires direct image collation;
3. **earlier transmission genealogy** — still requires G893/Ming/Korean evidence and cannot be inferred from a 1673 Japanese witness.

Accordingly:

`SAME_YEAR_SAME_WORK_HOLDING != SAME_PHYSICAL_COPY`

`SAME_EDITION_IMAGE_AGREEMENT != EARLY_TRANSMISSION_AUTHORITY`

`NATIVE_IMAGE_FETCH != TARGET_VALUE`

## 6. Runtime consequence

None.

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

## 7. Next work

1. inspect artifact `9972676923` directly and complete no-OCR diplomatic transcription for D16/L8/L101/L132;
2. bind the equivalent pages in the Kyushu University IIIF copy by printed headings rather than scan offsets;
3. determine whether the Kyushu copy confirms the same structural absence/non-comparability for the L124 field;
4. only after direct surface collation, compare Ogawa 1673 against Goryeosa/CADAL/KRDB, G893 and Ming 1569 without collapsing source rank or chronology.
