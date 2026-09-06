# Fusion Chart Historical Provenance & School Audit R1

## Batch 11L - Ogawa 1673 Kyushu Independent Holding Collation

Status: **COMPLETE FOR CURRENT KYUSHU DIRECT-IMAGE CONTROLS; EARLY TRANSMISSION CAUSE AND G893 TARGETS REMAIN OPEN**

Batch ID: `BATCH-11-BAZI-OGAWA-1673-KYUSHU-COLLATION-L`

This batch converts the Kyushu University 1673 Ogawa holding from a bibliographic
route into a directly bound no-OCR image witness. It also repairs an over-broad
field assumption discovered during target-page localization. It does **not**
reopen any chart algorithm or historical-calendar runtime.

## 1. Exact reproducible evidence package

At exact source commit `8cd6d20dda9c7038daac3db884c3c1ea6b86c6f9`,
workflow `research-kyushu-ogawa-shoushi-licheng-target-pages` run
`34010515542` completed successfully and emitted artifact `9982311056`:

- artifact:
  `kyushu-ogawa-target-pages-8cd6d20dda9c7038daac3db884c3c1ea6b86c6f9`
- digest:
  `sha256:bf85126c4d4a16ad4be17e28b089d921b8f7f1b986bf4bd2f480b4a308bb5944`
- artifact size: 32,778,514 bytes
- fetched native page size: 6592 x 4672
- OCR: **not used**
- cross-copy fixed offset: **not used**
- target binding: printed table title, field identity and printed limit headings.

The exact machine-readable human-reading ledger is
`docs/research/KYUSHU-OGAWA-1673-SHOUSHI-LICHENG-DIRECT-COLLATION-R1.json`.

Workflow success only proves that images were emitted. The direct conclusions
below were recorded only after page-level visual inspection.

## 2. D16: independent structural replication

Canvases 40-41 directly bind the Kyushu copy's `太陽盈縮立成` opening and
day-16 continuation.

The independent 1673 holding repeats the Ogawa structural result already seen
in the NDL copy: the active cross-edition D16 difference/message-difference
control is not printed as a separate field in this table schema.

Therefore:

`KYUSHU_OGAWA_D16_DIFFERENCE = FIELD_STRUCTURALLY_NOT_DIRECTLY_COMPARABLE`

Neither `5.1362` nor `5.2362` may be inferred from neighboring columns.

This is independent same-year structural corroboration, not a numeric vote.

## 3. Chiji table: same-copy typography controls

Canvas 50 directly exposes the table schema:

- `限數`
- `遲疾曆日率`
- `損益分`
- `遲疾積`

The new workflow deliberately adds three same-copy symmetry controls:

- L8 target (canvas 51) <-> L159 control (canvas 58);
- L132 target (canvas 57) <-> L35 control (canvas 52);
- L101 target (canvas 55) <-> L67 control (canvas 54).

Direct inspection gives three separate philological results.

### 3.1 L8 / L159

After the expected `益` versus `損` sign reversal, the numeric glyph layout
is physically identical in the Kyushu copy.

This establishes a same-copy positional control for L8 without importing a
linear transcription from Goryeosa or Ming 1569.

The photograph alone is **not** used to force either
`10.561775` or `10.5601775`.

### 3.2 L35 / L132

After the expected sign reversal, the numeric glyph layout is likewise
physically identical in the Kyushu Ogawa copy.

This matters because the Goryeosa received facsimile has a visible
L35/L132 compact-zero contrast. The Kyushu result proves that the Goryeosa
surface practice must remain copy/source scoped rather than being universalized
as the meaning of the mechanical value.

Again, no linear decimal string is invented from the photograph.

### 3.3 L67 / L101

The same-copy symmetric accumulated-value positions preserve visibly different
zero/place-group surfaces.

This independently reinforces the project's philological rule:

`SURFACE_STRING_INEQUALITY != MECHANICAL_INEQUALITY`

The result supports positional interpretation, but the normalized decimal is
not rederived from the photograph alone.

## 4. L114: direct same-year confirmation

Canvas 56 directly reads:

`九日三四八九`

Normalized:

`9日3489`

This agrees with:

- the NDL Ogawa 1673 native image;
- Ming 1569;
- the KRDB underlying image;
- CADAL Goryeosa received facsimile;
- Wikisource / KRDB normalized rendering.

It further isolates KRDB types=o `九日二四八九` as a database transcription
error rather than a physical transmission variant.

## 5. L124: critical field-identity correction

The prior target-page probe correctly noticed that canvases 68-70 belong to a
different table family than the Chiji pages, but the first L124 binding was
still too strong because it described canvas 70 as if it directly printed the
same raw `疾曆行度` field as Ming 1569.

Direct header inspection now binds the Kyushu table as:

- table title: `遲疾限行度`
- fields: `疾曆限行度` and `遲曆限行度`.

Its numeric layer is not the Ming raw 1e-4-degree `疾曆行度 / 遲曆行度`
layer. The initial-limit printed values normalize to:

- 疾: `0.0679314`
- 遲: `0.0832064`

These exactly match the Ming 1569 reciprocal shortcut layer:

- `疾曆捷法 = 0.0679314`
- `遲曆捷法 = 0.0832064`.

At L124 the Kyushu table directly preserves the derived pair:

- 疾: `0.0797587`
- 遲: `0.0704164`.

Those are exactly the Ming-derived shortcut values associated with:

- Ming raw 疾 / project `ji_xingdu`: `1.0281`
- Ming raw 遲 / project `chi_xingdu`: `1.1645`.

By contrast, the received Goryeosa raw variant `1.0821` would produce the
seven-place truncated derived control `0.0757785`, which is not the printed
Kyushu L124 疾 value.

The correct classification is therefore:

`MECHANICALLY_LINKED_DERIVED_CONTROL_SUPPORTS_MING_1_0281_LINEAGE_NOT_DIRECT_RAW_GLYPH`

This is stronger than simple non-comparability, but weaker than a direct raw
`一度〇二八一` image reading. That distinction is mandatory.

## 6. Provenance implications

The two 1673 Ogawa holdings now contribute different but compatible evidence:

- NDL: native direct D16 structural result and L114 direct reading;
- Kyushu: independent D16 structural corroboration, L114 direct reading,
  same-copy split-place controls, and the L124 reciprocal-layer lineage control.

The Kyushu result also proves that the NDL observation "no separate L124 table
identified in the inspected volume sequence" cannot be generalized to all
1673 Ogawa physical holdings. It was a holding/sequence-scoped observation.

Catalog spelling `田原仁左衛門` versus `田原二左衛門` is retained as a
bibliographic surface difference and is not used by itself to infer a distinct
edition genealogy.

## 7. Runtime consequence

None.

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

No historical-calendar adapter is activated and no Bazi/Ziwei chart rule is
changed.

## 8. Next work

1. bind the six target controls in the early Kyujanggak G893 physical witness
   when a non-blocked image path becomes available;
2. keep the L124 Kyushu evidence explicitly typed as a derived/reciprocal
   control rather than a direct raw-xingdu glyph;
3. continue transmission-genealogy adjudication across Ming 1569, Goryeosa,
   G893, NDL Ogawa and Kyushu Ogawa;
4. do not force linear serialization of split-place Ogawa cells where
   same-copy relative identity is sufficient for the current philological
   conclusion.
