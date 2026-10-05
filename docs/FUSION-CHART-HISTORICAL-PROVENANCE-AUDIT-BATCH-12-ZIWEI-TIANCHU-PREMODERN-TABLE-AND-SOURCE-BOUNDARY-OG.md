# Historical Provenance Audit — Batch 12OG

## Scope

Batch ID: `BATCH-12-ZIWEI-TIANCHU-PREMODERN-TABLE-AND-SOURCE-BOUNDARY-OG`

Target: `HPA-ZMINOR-007` — TianChu heavenly-stem table.

The old Matrix treated TianChu as a two-table dispute: the production/Wenmo-compatible table versus a “Fullbook variant table pending extraction”. 12OG tests both sides instead of preserving that label indefinitely.

## Premodern table witness

`EXT-WIKISOURCE-XINGXUE-DACHENG-TIANCHU` is the received Siku transcription of Ming Wan Minying's `星學大成`, juan 1, heading `論天厨`.

The verse reads:

`甲乙巳午丙在子，丁戊己午己申儲，庚落寅中辛尋午，壬厨居酉癸居猪。`

Its accompanying gloss identifies TianChu as `食神祿` and explains the first cases mechanically through the eaten stem's Lu position.

Parsed by heavenly stem:

| Stem | Premodern TianChu | Current runtime |
| --- | --- | --- |
| 甲 | 巳 | 巳 |
| 乙 | 午 | 午 |
| 丙 | 子 | 子 |
| 丁 | 巳 | 巳 |
| 戊 | 午 | 午 |
| 己 | 申 | 申 |
| 庚 | 寅 | 寅 |
| 辛 | 午 | 午 |
| 壬 | 酉 | 酉 |
| 癸 | 亥 | 亥 |

Result: **10/10 exact match**.

A modern received transcription of `張果星宗` preserves the same verse and `食神祿` explanation. The repository already has a strong 1594 ZhangGuo physical-edition control, but the TianChu target leaf of that physical witness was not directly collated here; it therefore adds lineage context, not an independent target-text vote.

## Source-domain boundary

`星學大成` is not itself a Ziwei-specific placement manual. Its TianChu witness proves that the current table is not merely a modern Wenmo/Zhongzhou invention: the same star name, same birth-year heavenly-stem input dimension and same ten coordinates are present in a premodern astrological rule tradition.

What remains open is the exact route by which this table entered later Ziwei practice.

This distinction follows the existing project precedent for rules such as standalone Feilian: geometry can be historically closed while adoption genealogy remains open.

## Audit of the alleged Fullbook competing table

The old normalized route `S01:ZZZA-PR-023` says the current table is “与全书异表”.

12OG found no corresponding TianChu atom in the frozen `ZZQS-*` canonical Fullbook extraction, and no quoted/located Fullbook TianChu table is bound in the current Matrix or external-source registry.

Therefore the old “Fullbook variant” is not a valid preserved candidate yet. A candidate requires at minimum a quoted rule, locator and source/edition binding.

This is a bounded evidence conclusion, not a claim that no Fullbook recension anywhere can contain TianChu material. If such a witness is later found, it may be registered forward-only.

## Adjudication

**PROV-DEFECT-043** is repaired forward-only.

`HPA-ZMINOR-007` changes:

`DISPUTED_MULTIPLE_CANDIDATES -> HISTORICALLY_SUPPORTED`

for the placement geometry:

`甲巳、乙午、丙子、丁巳、戊午、己申、庚寅、辛午、壬酉、癸亥`.

The specific Ziwei adoption path remains unresolved. The unbound Fullbook variant is removed from the live competing-method list rather than materialized as a phantom candidate.

No runtime, production default or chart algorithm changes.

## Result

- Matrix: **222 / 222 audited**
- HISTORICALLY_SUPPORTED: **99**
- DISPUTED_MULTIPLE_CANDIDATES: **27**
- SOURCE_INSUFFICIENT: **11**
- current MISSING_FROM_PRODUCT: **10**
- provenance defects: **43 / 43 repaired**
- historical candidate extensions: **8**
- algorithm reopens: **0**

## Next

**12OH — re-rank the remaining active DISPUTED_MULTIPLE_CANDIDATES queue after TianShou/TianChu closure.**

Research record: `docs/research/ZIWEI-TIANCHU-PREMODERN-TABLE-AND-SOURCE-BOUNDARY-R1.json`.
