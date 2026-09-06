# Fusion Chart Historical Provenance & School Audit R1

## Batch 11N - Joseon 1444 Chiljeongsan Independent Table-Witness Routes

Status: **COMPLETE FOR WITNESS IDENTITY / TABLE-FAMILY / ORIGINAL-IMAGE ROUTE LOCALIZATION; TARGET GLYPHS PENDING**

Batch ID: `BATCH-11-BAZI-JOSEON-1444-CHILJEONGSAN-WITNESS-ROUTES-N`

This batch adds two independent early-Joseon comparison routes without
substituting either route for Kyujanggak G893.

The machine-readable route ledger is:

`docs/research/JOSEON-1444-CHILJEONGSAN-EARLY-TABLE-WITNESS-ROUTES-R1.json`

No target numeric value is entered in this batch.

## 1. Kyujanggak G894 is a separate 1444 official computational print

Kyujanggak's National Important Science/Technology Materials listing directly
identifies:

- `七政算內篇`;
- call number `奎貴894-v.1-3`;
- authors `李純之, 金淡(朝鮮) 受命編`;
- `甲寅字`;
- publication year `1444`;
- original-image and original-text services.

The catalog image surface additionally exposes book code `GK00894_00`.

This is a particularly valuable early-Joseon numerical-table witness because
the provider itself gives 1444 for this object. But it is **not**
`授時曆立成 奎貴893`.

Therefore:

```text
G894_AS_G893=FORBIDDEN
ADJACENT_CALL_NUMBER_AS_SHARED_COPY_GENEALOGY=FORBIDDEN
```

The adjacency `893 / 894` is a catalog fact, not a genealogy argument.

## 2. Sejong Sillok volume 156 independently localizes the same table families

The National Institute of Korean History official Sillok service directly
binds the solar and lunar table families in `世宗實錄 卷156`.

Solar:

- article: `wda_50016011`;
- table: `太陽冬至前後二象盈初縮末限`;
- Taebaeksan copy location: `60冊 156卷 6張 A面`;
- National History reprint location: `6冊 3面`.

Lunar:

- article: `wda_50016016`;
- table: `太陰限數遲疾度`;
- Taebaeksan copy location: `60冊 156卷 13張 A面`;
- National History reprint location: `6冊 7面`.

The official service exposes an original-image viewer backed by the Taebaeksan
Sillok image layer. Exact target image identifiers and target cells have not
yet been read.

Consequently:

```text
SILLOK_ARTICLE_IMAGE_PRESENCE_AS_NUMERIC_READING=FORBIDDEN
SILLOK_TABLE_AS_1444_G894_IDENTICAL_GLYPH_SURFACE=FORBIDDEN
```

## 3. Why these routes matter

The active cross-edition problem currently contains:

- Ming 1569 edition-scoped primary readings;
- Goryeosa received surfaces;
- G893 early Korean Shoushi-licheng physical witness, with target pages still
  pending;
- Ogawa 1673 Japanese received witnesses.

G894 and the Sejong Sillok create an additional **mid-15th-century Joseon
computational transmission control**.

After exact target-cell reading, they can test whether disputed surfaces were
already present, corrected, normalized or reorganized in official Joseon
computational practice.

They cannot answer that question merely by existing.

## 4. Six controls remain fail-closed

For both G894 and the Sillok route, these controls remain pending direct image
reading:

1. `VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE`;
2. `VAR-NUM-LUNAR-L8-LOSSGAIN`;
3. `NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING`;
4. `VAR-NUM-LUNAR-L114-DAYRATE`;
5. `VAR-NUM-LUNAR-L124-JI-XINGDU`;
6. `VAR-NUM-LUNAR-L132-LOSSGAIN`.

No Ming/Goryeosa/Ogawa value is copied into these witnesses.

## 5. Chronology boundary

Official modern historical synthesis places completion of the Naepyeon in
1442 and publication in 1444. Kyujanggak independently catalogs G894 as 1444.

This does **not** date every later physical Sillok copy to 1444.

Therefore:

`COMPOSITION_OR_PUBLICATION_YEAR_AS_SURVIVING_SILLOK_COPY_DATE=FORBIDDEN`

Likewise, G894's provider-dated 1444 does not close G893's separate
1434-versus-1444 copy-date conflict.

## 6. Authority and transmission boundary

Evidence weighting remains source-type aware:

- G894: independent official computational print witness;
- Sillok: official received-record table witness with physical leaf
  localization;
- G893: separate Shoushi-licheng physical witness;
- Goryeosa: separate received historiographic tradition;
- Ming 1569: edition-scoped primary reference for the current ledger.

Source count is not adjudication.

`SOURCE_COUNT_AS_VARIANT_ADJUDICATION=FORBIDDEN`

## 7. Runtime consequence

None.

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

## 8. Next work

1. extract the exact Sillok original-image viewer identifiers for
   `wda_50016011` and `wda_50016016`;
2. render/read the relevant target cells without OCR;
3. bind G894's exact solar/lunar target folios through Kyujanggak's
   original-image service;
4. compare G894, Sillok, G893 and Goryeosa only after independent target-cell
   readings exist;
5. preserve G893 as an unresolved but required independent physical witness;
   G894 or Sillok may not substitute for it.
