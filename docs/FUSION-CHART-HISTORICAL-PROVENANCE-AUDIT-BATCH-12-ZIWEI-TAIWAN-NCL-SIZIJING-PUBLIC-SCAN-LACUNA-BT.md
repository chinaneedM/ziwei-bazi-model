# Fusion Chart Historical Provenance Audit R1 — Batch 12BT

## 臺灣國圖 15275-0058《四字經》公開掃描缺頁控制：目錄列「唐明皇論」，可見正文由「甲甲」起

Status: **TAIWAN-NCL MING-WANLI SIZIJING 21-PAGE PUBLIC SCAN DIRECTLY REVIEWED WITHOUT OCR / P01 TOC DIRECTLY LISTS 唐明皇論 BEFORE 甲甲 / P03 DIRECTLY READS 四字經目錄終 / P04 VISIBLE BODY OPENS 四字經 THEN 甲甲, WITH NO EXPOSED 唐明皇論 BODY LEAF / P21 CONTINUES THROUGH 癸癸 MATERIAL / PUBLIC-SCAN TARGET-LEAF LACUNA CONFIRMED / PHYSICAL-HOLDING LACUNA NOT PROVED / YIMEN-TAIWAN INTERNAL-UNIT CORRESPONDENCE STRENGTHENED / SAME IMPRESSION OR DISBOUND IDENTITY NOT PROVED / TARGET VARIANT GLYPHS NOT OBSERVED IN TAIWAN SCAN / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI-BRANCH MECHANICAL VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope and exact evidence chain

Batch 12BS directly adjudicated the 1597 《夷門廣牘》 side of the 《四字經》 opening variants as `唐明皇論 / 古人云 / 天陰雨落難定 / 亥子丑寅`. Its next gate was to collate the independent Taiwan National Central Library single-title object 15275-0058.

The full public 21-page PDF derivative was therefore downloaded and rendered without OCR:

- source: `NCL-15275-0058_四字經.pdf`, Wikimedia Commons derivative sourced to Taiwan National Central Library;
- source PDF SHA-256: `e99bee3b210d9b078b11778f2e504277c821520ba16677b917a4a434661dbe02`;
- page count: `21`;
- renderer commit/tree: `46c4a4493d92b7697f78163f582402fbc02691d7` / `7744f048e0dd532a3d41209868660a46b28433d9`;
- successful GitHub Actions run: `34825456673`;
- artifact: `10340620803`, digest `sha256:5448669de7e40c697a6a80007941514467cdb4dfb1880ac726fcf4f97ce32ffc`;
- final judgments below are direct visual readings of the rendered physical scan, not OCR output.

## 2. Page 1: the internal unit is explicitly in the Taiwan witness

Page 1 (`5545620326b950aca74c508394971f063177c819ddc2f3ac7b513949fd2188f8`) directly reads the heading `四字經目錄`. The first listed internal unit is `唐明皇論`, followed by `甲甲` and the stem-pair sequence.

This is a material advance over the earlier catalog-only relationship: the Taiwan witness itself, not a modern OCR layer, directly identifies `唐明皇論` as part of its 《四字經》 contents. The 1597 Yimen witness physically uses the same heading over the opening prose unit.

## 3. Pages 3–4: public derivative skips from catalogue end to 甲甲 body

Page 3 (`2a1fface07816bc46764da1be57b8e0d10f75c18fea3096d6678a2bebbf922cc`) directly reads:

```text
四字經目錄終
```

The very next public PDF page, page 4 (`8ae30532d8d0bfc64886ff88e44ac9ed84af7537cb7d5b5496a62c213f2cd794`), directly opens:

```text
四字經
甲甲
...
甲乙
...
```

No `唐明皇論` prose body is exposed between the catalogue ending and the visible `甲甲` body. Review of the remaining public pages continues the stem-pair material; page 21 (`2921471d1ee787ce7d250225bfd2218ad57be740a0d914729b71c35a7388956c`) is already in `癸癸` material.

The admissible conclusion is therefore **public-scan lacuna**, not physical-book absence:

```text
TAIWAN_PUBLIC_21_PAGE_DERIVATIVE_DOES_NOT_EXPOSE_TANG_MINGHUANG_LUN_BODY_LEAF
PHYSICAL_HOLDING_LACUNA_NOT_PROVED
```

The missing unit could reflect digitization selection, a missing leaf in the digitized object, or another physical-history condition. This batch does not choose among those explanations.

## 4. Edition/transmission effect

Taiwan 15275-0058 and the 1597 NLC/Yimen witness now have a stronger internal structural bridge:

- both are titled 《四字經》;
- the Taiwan physical scan's own TOC lists `唐明皇論` as the first internal unit;
- the Yimen physical scan preserves `唐明皇論` as the prose heading before the stem-pair body.

This strengthens common transmission/edition-family correspondence, but it still does **not** prove that the two objects are the same impression, that Taiwan 15275-0058 was disbound from a Yimen-Guangdu volume, or that every target glyph is identical.

Because the Taiwan public derivative does not expose the `唐明皇論` body leaf, it contributes **zero** direct Taiwan glyph votes for `古人/古經`, `雨落/雨露`, or `亥子丑寅/子丑寅亥`.

## 5. Effect on HPA-ZDATE-006

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`;
- Taiwan public-scan direct target-body glyph witness increment: `0`;
- Taiwan physical TOC `唐明皇論` structural witness: `+1`;
- Hai-branch mechanical vote increment: `0`;
- Fullbook cloudy/rain current-time acquisition mechanism closed: `false`;
- runtime winner selected: `false`;
- candidate collapsed: `false`;
- algorithm reopen authorized: `false`.

Global accounting remains `198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families`; provenance defects remain `11/11`; chart algorithm defect/reopen/collapse remain `0/0/0`.

## 6. Next gate

1. Search for another first-party or derivative image route for Taiwan NCL 15275-0058 that exposes the omitted `唐明皇論` body leaf; do not infer its glyphs from the TOC.
2. Directly collate the Yongle-Dadian target physical leaf for `古經/古人`, `雨露/雨落`, and hour ordering if an admissible image route is available.
3. Continue the separate Fullbook-line operational-current-time question; neither the Taiwan TOC nor its public-scan lacuna supplies a clock-recovery method.

Research record: `docs/research/ZIWEI-TAIWAN-NCL-SIZIJING-PUBLIC-SCAN-LACUNA-R1.json`.
