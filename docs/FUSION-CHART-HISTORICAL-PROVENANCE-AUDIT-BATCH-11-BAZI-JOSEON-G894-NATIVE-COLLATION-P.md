# Fusion Chart Historical Provenance & School Audit R1

## Batch 11P - Joseon G894 Native Table Collation and Field Bridge

Status: **COMPLETE FOR FIVE LUNAR CONTROLS; SOLAR D16 STRUCTURALLY NON-COMPARABLE**

Batch ID: `BATCH-11-BAZI-JOSEON-G894-NATIVE-COLLATION-P`

Machine-readable evidence:

- `docs/research/KYUJANGGAK-G894-DIRECT-TARGET-PAGE-BINDING-R1.json`
- `docs/research/KYUJANGGAK-G894-LUNAR-FIELD-SEMANTIC-BRIDGE-R1.json`

This batch upgrades Kyujanggak `七政算內篇 奎貴894-v.1-3` from a
provider-dated 1444 object route to exact renderer-bound page localization,
direct no-OCR native-image reading and an edition-scoped field-semantic bridge
based on G894's own method prose.

It does **not** substitute G894 for G893 or for the Sejong Sillok physical
transmission layer.

## 1. Reproducible Kyujanggak digital-object chain

The official Kyujanggak service directly returned:

- `BOOK_CD=GK00894_00`;
- `ITEM_CD=GJB`;
- three provider volumes `0001 / 0002 / 0003`;
- renderer-returned page IDs and exact `imgFileNm` paths.

Object-access workflow `34021927880` at
`c2bc80e2b9b5aed593799109c46baa8fd8992741` uploaded artifact
`9985782432`.

Direct visual sampler workflow `34022309182` localized the active table
ranges. Target-page workflow `34022550834` then fetched the exact target
pages through the renderer-returned image paths. Finally, method-closure
workflow `34024508098` at
`af93758c7c167b89e302cbc6e3560e6923ee0a6b` uploaded artifact
`9986629487` (digest
`sha256:5d53684ea507a3f2c7e576cf045356ac3a909c4319defc1c4ce1014ad903f540`)
and directly bound the table-end / post-table method page `041b`.

No filename sequence is treated as page evidence.

## 2. G894's own six-column lunar schema

Native page `0001-018a` directly prints the table
`大陰限數遲疾度` with six fields:

1. `限數`
2. `遲疾曆日率`
3. `損益分`
4. `遲疾度`
5. `疾曆限行度`
6. `遲曆限行度`

This corrects an in-progress evidence-artifact transcription that had
temporarily written `遲疾益分` and omitted `遲疾度`. The correction occurs
before Batch 11P closure and is not a chart-algorithm defect.

## 3. Direct method-prose bridge

Page `018a` directly defines how the current `疾曆 / 遲曆` half and
`限數` are derived.

Page `041b`, under `求遲疾差`, directly states the stable computational core:

`置遲疾曆日及分秒以遲疾曆日率減之以其下損益分乘之如八百二十而一益加損減其下遲疾度即遲疾差`

Therefore:

- `遲疾曆日率` is the within-limit day-rate anchor;
- `損益分` is the interpolation increment;
- `遲疾度` is the row base correction.

The same page, under `求加減差`, directly states the stable core:

`視經朔弦望盈縮差與遲疾差同名相從異名相消以八百二十乘之以所入遲疾限下行度除之即為加減差`

Therefore the current-half `疾曆限行度 / 遲曆限行度` is the denominator
used by the lunar correction path. This closes field identity by G894's own
method text rather than by similar names alone.

## 4. Five direct lunar readings

| Control | G894 native page | Direct surface | Normalized | Cell-level result |
| --- | --- | --- | --- | --- |
| L8 `損益分` | `0001-019b` | `益一十〇分五六〇一七七五` | 10.5601775 | agrees with Sillok / Goryeosa received branch, not Ming 1569 10.561775 |
| L101 `遲疾度` | `0001-032a` | `五度二十〇四八一一二五` | 5.20481125 | same mechanical value as the normalization bridge, with explicit positional zero |
| L114 `遲疾曆日率` | `0001-034a` | `九日三四八九` | 9日3489 | agrees with Ming, Sillok and direct Goryeosa images; reinforces KRDB-o 2489 as transcription error |
| L124 `疾曆限行度` | `0001-035a` | `疾一度〇二八一` | 1.0281 | agrees with Ming 1569 and Sillok; differs from Goryeosa received 1.0821 |
| L132 `損益分` | `0001-036b` | `損七分八八六〇七五` | 7.886075 | preserves explicit zero, unlike the compact Goryeosa received L132 surface |

All five readings are direct human visual readings of provider-native images.
OCR was not used.

## 5. Solar D16 is structurally non-comparable

G894 native pages `009a/009b` directly show the winter solar table through
day 16. The visible schema is:

- `積日`
- `盈縮加分`
- `盈縮積`

The active control `VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE` targets the
second difference/message-difference numeric field that is independently
present in the compared Shoushi/Goryeosa lineage. G894 does not print that
field in this table.

Therefore:

```text
G894_SOLAR_D16_TARGET_FIELD=STRUCTURALLY_ABSENT
G894_SOLAR_D16_NUMERIC_VALUE=NONE
NEIGHBORING_COLUMN_SUBSTITUTION=FORBIDDEN
```

Absence is not converted into zero, blank, or an inferred value.

## 6. Transmission consequence: cell-level lineage, not copy blocs

G894 is internally mixed relative to the previously observed variants:

- L8 agrees with the Goryeosa/Sillok value branch.
- L124 agrees with Ming 1569/Sillok at 1.0281.
- L101 and L132 preserve explicit positional zeros.
- D16 is structurally non-comparable rather than numerically aligned.

Accordingly:

```text
WHOLE_COPY_VARIANT_INHERITANCE=FORBIDDEN
SOURCE_COUNT_AS_VARIANT_ADJUDICATION=FORBIDDEN
CELL_LEVEL_MECHANICAL_FIELD_MAPPING=REQUIRED
```

This also demonstrates why the project's philology rule must precede
mechanical rule identity.

## 7. G893 remains required and independent

G894 is a 1444 `七政算內篇` object. It is not
`授時曆立成 奎貴893`. The neighboring call numbers do not establish copy
genealogy, and neither G894 nor Sillok values are transferred into G893.

All six G893 direct target readings therefore remain open.

## 8. Runtime consequence

None.

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

## 9. Next work

1. continue direct G893 target-page acquisition without substituting G894 or
   Sillok;
2. continue Sillok solar D16 continuation-image research independently;
3. expand the cell-level transmission graph only with independently mapped
   fields and directly read surfaces;
4. continue open historical-calendar adapter work separately; Batch 11P has no
   runtime-selection effect.
