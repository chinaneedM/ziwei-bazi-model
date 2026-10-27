# Fusion Chart Historical Provenance Audit R1 — Batch 12BS

## 1597《夷門廣牘》本《四字經》直接字形校勘：`唐明皇論`、`古人云`、`雨落`、`亥子丑寅`

Status: **DIRECT NO-OCR MING-PRINT GLYPH COLLATION COMPLETE FOR THE YIMEN-GUANGDU SIZIJING OPENING / P28 DIRECTLY PRINTS 四字經, 唐德行禪師著, 明周履靖校正, 唐明皇論 / P29 DIRECTLY PRINTS 古人云 AND 天陰雨落難定 AND THE CONTIGUOUS HOUR ORDER 亥子丑寅 / BATCH-12BR YIMEN-SIDE OCR VARIANTS PHYSICALLY ADJUDICATED / YONGLE-DADIAN READINGS REMAIN A SEPARATE RECENSION WITNESS / TAIWAN-NCL EDITION IDENTITY STILL UNRESOLVED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI-BRANCH MECHANICAL VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope and evidence chain

Batch 12BR proved an independent Ming-print 《四字經》 transmission and isolated three exact variants that could not be trusted from CText automatic OCR alone. The next gate was direct, no-OCR collation of the 1597 《夷門廣牘》 physical scan.

Reproducible evidence chain:

- source object: Wikimedia Commons `明刻本夷門廣牘26.djvu`, already bound to the NLC-sourced 1597 《夷門廣牘》 route;
- source DjVu SHA-256: `30ffe1ae111fc72d816cb9d2a507bb051b0b67a3eb6be0e80497f02ff4c853e2`;
- renderer commit/tree: `8e087490a48c42303c61cfe50840e3568624653a` / `415c67fccddfad0a5f44307b139db8639d6a89bf`;
- successful exact-HEAD renderer run: `34824084899`;
- artifact: `10339620251`, digest `sha256:8e728d108f3e4f0b828e7fe6de3e8bc2ac53ae7cc41fec45c2c60fb5f58c5904`;
- rendering used `ddjvu` and Pillow; no OCR was used for final glyph judgment.

## 2. Page 28: title, responsibility and heading

Direct review of p28 (`9a96a2f82313a74d24472d33a789258757ee2dbb5d8f470e94d1c7913d31f64a`) reads:

```text
四字經
唐德行禪師著
明周履靖校正
唐明皇論
```

This physically closes the Yimen-side heading as `唐明皇論` and confirms the printed responsibility/correction lines. It does not authenticate a Tang composition date merely from `唐德行禪師著`.

## 3. Page 29: three Batch-12BR variants

Direct review of p29 (`4ee4441255716dda76ac0a04eb8aa6460feb3f213526667a451a08bcd1038246`) resolves the Yimen-side readings:

| Variant question | 1597 Yimen physical reading | Result |
| --- | --- | --- |
| `古經云` vs `古人云` | `古人云` | YIMEN SIDE DIRECTLY ADJUDICATED |
| `天陰雨露時難定` vs `天陰雨落難定` | `天陰雨落難定` | YIMEN SIDE DIRECTLY ADJUDICATED |
| `子丑寅亥` vs `亥子丑寅` | contiguous sequence `亥子丑寅` | YIMEN SIDE DIRECTLY ADJUDICATED |

The same page visibly continues `便是神仙也有差別`. This batch intentionally avoids a diplomatic transcription of every surrounding glyph because only the three listed variant loci are material to this gate.

## 4. Philological effect

These three differences are no longer merely automatic-OCR artifacts on the Yimen side. The 1597 physical print itself supports `古人云 / 雨落 / 亥子丑寅`.

The opposite conclusion is **not** authorized: Batch 12BS does not call the Yongle-Dadian `古經云 / 雨露 / 子丑寅亥` readings errors. They remain a separate transmission/recension witness until their own physical-glyph chain is adjudicated. The current classification is:

```text
SAME_SIZIJING_TEXT_FAMILY_AT_LONG_SEQUENCE_LEVEL
+ REAL_RECENSION_VARIATION_NOW_PHYSICALLY_CONFIRMED_ON_YIMEN_SIDE
+ NO_STEMMATIC_WINNER_SELECTED
```

Taiwan NCL 15275-0058 is still not proved to be the same impression, a disbound/extracted copy, or an independent edition relative to the NLC/Yimen object.

## 5. Effect on HPA-ZDATE-006

The literal `亥` here belongs to the difficult-hour list `亥子丑寅`; it is not an instruction to reclassify upper-half Zi as Hai. Likewise `天陰雨落難定` states time-determination difficulty under inclement weather but gives no complete operational time-acquisition procedure.

Therefore:

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`;
- direct 1597 Sizijing target-leaf glyph witness increment: `+1` at the textual-variant layer;
- HPA-ZDATE-006 Hai-branch mechanical vote increment: `0`;
- Fullbook cloudy/rain current-time acquisition mechanism closed: `false`;
- runtime winner selected: `false`;
- candidate collapsed: `false`;
- algorithm reopen authorized: `false`.

Global accounting remains `198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families`; provenance defects remain `11/11`; chart algorithm defect/reopen/collapse remain `0/0/0`.

## 6. Next gate

1. Directly collate the Taiwan NCL 15275-0058 《四字經》 opening leaf for the same heading and three variant loci, to test edition/impression identity with physical glyphs.
2. If accessible, directly collate the Yongle-Dadian physical target leaf for the same loci rather than treating its transcription as final glyph authority.
3. Separately continue the Fullbook-line cloudy/rain operational-current-time acquisition chain; the Sizijing sentence remains an uncertainty statement rather than a complete clock-recovery method.

Research record: `docs/research/ZIWEI-YIMEN-1597-SIZIJING-DIRECT-GLYPH-COLLATION-R1.json`.
