# Fusion Chart Historical Provenance & School Audit R1

## Batch 11K - Ogawa 1673 Native Evidence Package and Independent Holding

Status: **COMPLETE FOR NATIVE EVIDENCE PACKAGE + D16 STRUCTURAL ADJUDICATION + BIBLIOGRAPHIC CORROBORATION; THREE LUNAR DIPLOMATIC READINGS REMAIN OPEN**

Batch ID: `BATCH-11-BAZI-OGAWA-1673-NATIVE-EVIDENCE-K`

This batch closes a narrow provenance/access and structural milestone around the Japanese received witness `EXT-NDL-OGAWA-SHOUSHI-LICHENG-1673`. It does **not** close the unresolved L8/L101/L132 split-vertical glyph-group readings and it does not authorize any chart/runtime change.

## 1. Exact remote evidence packages

At exact source commit `f90477b4247f6c7bfc70f58f68082c0638947cf5`, workflow `research-ndl-ogawa-shoushi-licheng-target-pages` run `33977235461` completed successfully and emitted artifact `9972676923`:

- artifact name: `ndl-ogawa-target-pages-f90477b4247f6c7bfc70f58f68082c0638947cf5`
- artifact size: `29,096,181` bytes
- artifact digest: `sha256:81c99a8952dfbabf80c9d2cb9e95093b06aca734bf9a7d19e1c70d3ec567e216`
- requested native canvas width: `7392px`
- localized pages: initial solar D16 context, lunar structural header, L8, L101, L114 and L132 pages
- OCR: **not used**

Direct inspection showed that the initial D16 locator page R0000004 printed the day-16 derived columns but not the target difference column. The probe was therefore corrected forward-only rather than forcing a value.

At exact source commit `f5b1b362a3fcb5816da9231b2eb43824d50b8c6e`, run `33978788314` emitted the revised native package `9973124845`:

- artifact digest: `sha256:1e259e9ba7c8c6393b8b9d9674981022e23f27bda7823868714e2320189232f8`
- artifact size: `33,763,589` bytes
- requested width: `7392px`
- added R0000003, the printed opening of `太陽盈縮立成`, while retaining R0000004 as the D16 continuation context.

Workflow success proves only that the page package was emitted. `FETCH_SUCCESS != DIPLOMATIC_READING` remains an explicit evidence firewall.

## 2. D16 structural adjudication

R0000003 directly shows the opening and printed field structure of `太陽盈縮立成`; R0000004 is its continuation containing day 16. Native-resolution visual inspection binds the visible solar schema as:

- `積日`
- `盈縮積度`
- `盈縮加分`

The active cross-edition control `VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE` is a separate day-difference/message-difference type field. No independent `日差` / `消息分`-type column is printed in this Ogawa solar table opening or its day-16 continuation.

Therefore:

`OGAWA_1673_D16_DIFFERENCE = FIELD_STRUCTURALLY_NOT_DIRECTLY_COMPARABLE`

It is **forbidden** to infer either `5.1362` or `5.2362` from the neighboring derived columns, an arithmetic sequence, Goryeosa, or Ming 1569. This closes D16 for this witness as a structural non-comparability result, not as a numeric reading.

## 3. NDL bibliographic identity

NDL Search independently exposes the 1673 bibliographic identity for the work:

- title: `大元授時暦經立成 6巻`
- creator: `小川正意新勘`
- publisher: `田原仁左衛門`
- date: `寛文13 [1673]`
- NDL Search record: `https://ndlsearch.ndl.go.jp/books/R100000136-I1970023484922964747`

This is bibliographic authority for edition/work identity, not target-glyph authority.

## 4. Independent same-year holding: Kyushu University

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

## 5. Lunar evidence boundaries retained

The direct reading is now reconfirmed at native resolution:

- L114: `九日三四八九` -> normalized `9日3489`, HIGH confidence.

Direct native inspection has also reached the exact L8, L101 and L132 columns. Their target cells use split vertical place-group typography. The individual printed groups are visible, but their diplomatic serialization/place semantics are not yet sufficiently established to authorize normalized target values. They remain deliberately open rather than being back-filled from another edition or a calculated sequence.

L124 remains explicitly non-comparable in the inspected Ogawa volume-2 structure: the prior R0000019 overbinding is rejected, and absence of a separately identified 行度 field cannot be converted into numeric zero, equality, or a transmission variant.

## 6. Philological implications

The independent Kyushu holding is valuable precisely because it can separate four questions that must not be collapsed:

1. **edition/work identity** — already bibliographically corroborated;
2. **same-edition physical surface agreement** — requires direct image collation;
3. **table-schema agreement** — especially whether the same D16 difference and L124 行度 fields are absent;
4. **earlier transmission genealogy** — still requires G893/Ming/Korean evidence and cannot be inferred from a 1673 Japanese witness.

Accordingly:

`SAME_YEAR_SAME_WORK_HOLDING != SAME_PHYSICAL_COPY`

`SAME_EDITION_IMAGE_AGREEMENT != EARLY_TRANSMISSION_AUTHORITY`

`NATIVE_IMAGE_FETCH != TARGET_VALUE`

`ABSENT_FIELD != INFERRED_NUMERIC_VALUE`

## 7. Runtime consequence

None.

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

## 8. Next work

1. establish the Ogawa split-vertical place-group typography from internal controls and complete no-OCR diplomatic transcription for L8/L101/L132;
2. bind equivalent pages in the Kyushu University IIIF copy by printed headings rather than scan offsets;
3. test whether the independent 1673 copy confirms the same solar D16 structural omission and L124 non-comparability;
4. only after direct surface collation, compare Ogawa 1673 against Goryeosa/CADAL/KRDB, G893 and Ming 1569 without collapsing source rank or chronology.
