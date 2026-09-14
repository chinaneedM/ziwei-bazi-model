# Fusion Chart Historical Provenance Audit R1 — Batch 12CD

## 《革象新書》百刻文本祖型 + 《虎鈐經》傳箭數列：1578《三命通會》時刻材料的複合傳承模型

Status: **RECEIVED YUAN-WORK GEXIANG FACSIMILE PHYSICALLY CONFIRMS A NEAR-VERBATIM HUNDRED-KE / HALF-ZI TEXTUAL ANTECEDENT / SONG-WORK HUQIANJING MING-PRINT PHYSICALLY CONFIRMS THE OLDER 40↔60 ONE-KE STEP LADDER / SANMING SHARES BOTH STRUCTURES BUT IS NOT AN EXACT COPY OF EITHER / COMPOSITE ANCESTRY MODEL MATERIALLY STRENGTHENED / EXACT 59/41 MING TABLE PARENT STILL OPEN / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO HAI VOTE / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

## 1. Why this batch follows 12CC

Batch 12CC ruled out a shortcut: the reviewed 1569 Zhou-Xiang Datong volume does not itself expose the Sanming 42/58...59/41 table. The next task is therefore structural: separate the **prose lineage** from the **numeric ladder lineage** before looking for the Ming adaptation that joined them.

## 2. 《革象新書》 physical collation

A dedicated workflow rendered all 202 pages of CADAL06054852 without OCR.

```text
RUN=34863878875
ARTIFACT=10356238369
DIGEST=sha256:1b6f1c2f665b97794022a02e75cc85eb5cfb72501dfb8063acc2fc11464a7dbe
DJVU_SHA256=e6199e9a7e9381adec1d9b4f418a2fd6321add6bf72f6fb28add6ab379b8dbd4
PDF_SHA256=9a8e15384a3d2898f2fc28747c6dd847dad587190fe67a2ac5b019edfb042bbb
P78_SHA256=55fa822b1b809f519d79df36701191c95d2c9873fcd52a7035d33501bdb2e1ba
P79_SHA256=f8baf1814afe70728f537a7bea865e5d8a5589cbd8e8ebb9992e9df6988d24ca
P80_SHA256=3c74fc0d59ff735ec089ccda777784f05900d3c1e19d97abc9b4f9f68904409b
EXACT_HEAD_CI_RUN=34863878945
OCR_USED_FOR_GLYPH_CLAIMS=false
```

Scope firewall: 《革象新書》 is a Yuan work by Zhao Youqin, but this physical object is a **later received facsimile transmission**. It is not called a surviving Yuan print.

PDF p78 directly carries `時分百刻` and reads the hundred-ke system, including:

```text
晝夜十二時均分為百刻
一時有八大刻二小刻
...
子時之上一半在夜半前屬昨日
下一半在夜半後屬今日
```

p79 continues the same discussion into the old-calendar two-small-ke arrangement and rejects the popular `子午卯酉各九刻` claim, then opens `晝夜短長`. p79-80 further explains that spring/autumn day-night change is faster and solstitial change slower.

## 3. Near-verbatim relation to 1578《三命通會》

Batch 12AT physically locked the 1578 NCL Sanming p133 passage. The architecture is overwhelmingly the same: twelve shi / hundred ke, eight large + two small ke, 96 large + 24 small with six small equaling one large, upper/lower half labels, midnight half-Zi date orientation, the old-calendar small-ke note, and the rejection of the `子午卯酉九刻` folk rule.

One valuable recension difference is preserved rather than normalized:

```text
received Gexiang facsimile: 屬昨日 / 屬今日
1578 Sanming physical:      為昨日 / 屬今日
```

This establishes a strong **earlier-work textual antecedent / common-text lineage** for the Sanming prose. It does not by itself prove direct copying direction or exclude an earlier common source.

## 4. 《虎鈐經·傳箭》 supplies the older numeric ladder family

The Tianyige Ming-print physical witness of the Song work was already rendered without OCR in Batch 12CA. Re-reading pp74-76 as a whole sequence shows why endpoint-only comparison was insufficient.

The table runs by one-ke steps from winter `40/60` toward summer `60/40`, and it directly contains many of the same numeric pairs later displayed by Sanming, including:

```text
小寒 42/58
立春 45/55
雨水 47/53
later 48/52
...
55/45
56/44
58/42
59/41
```

The similarity is structural, not identity. Huqianjing changes arrows on its own day offsets and reaches `60/40` at the summer-solstice arrow. Sanming changes solar-term/date anchoring and displays `59/41` at 夏至.

Therefore the correct statement is:

```text
Sanming numeric table belongs to the older stepwise leak-arrow family
!= Sanming copied the Huqianjing table unchanged
```

## 5. Composite transmission model

The evidence now supports a substantially narrower model:

```text
Gexiang-like hundred-ke / half-Zi prose lineage
  + older 40↔60 seasonal leak-arrow numeric ladder
  + Ming calendrical/locality/astronomical adaptation
  -> Sanming 1578 displayed timekeeping material
```

This is no longer a loose thematic analogy. Two different structural layers now have concrete antecedents. What remains open is the **Ming adaptation layer**, especially the direct pre-1578 source that turns the old solstitial 60/40 family into Sanming's displayed 59/41 cap and fixes its term/date anchors.

## 6. Product adjudication

For `HPA-ZDATE-006`:

- generic half-Zi / hundred-ke textual ancestry: **materially strengthened**;
- older stepwise seasonal numeric family: **materially strengthened**;
- exact Sanming = Gexiang: **no**;
- exact Sanming = Huqianjing: **no**;
- direct borrowing direction: **not proved**;
- exact pre-1578 59/41 Ming parent: **open**;
- upper-Zi -> Hai branch vote: **0**;
- runtime candidate/winner/collapse: **none**;
- algorithm reopen: **no**;
- `HPA-ZDATE-006`: remains `MISSING_FROM_PRODUCT`.

## 7. Next gate

Stop searching only for isolated numbers. Search for a pre-1578 Ming/Nanjing witness that combines the **same one-ke ladder** with the **59/41 solstitial cap and Sanming-like solar-term anchoring**. Priority targets are Datong almanac appendices, official leak-clock/day-night tables, local Nanjing calendrical tables, and pre-1578 tongshu/medical-yunqi compilations.

Research record: `docs/research/ZIWEI-GEXIANG-HUQIAN-COMPOSITE-TIMEKEEPING-ANCESTRY-R1.json`.
