# Fusion Chart Historical Provenance Audit R1 — Batch 12CB

## 1533《運氣易覽》季节刻漏实体校勘：50/50、60/40 传统与《三命通會》精确表谱不等同

Status: **1533 CHENGQIAO-PRINT YUNQI YILAN PHYSICALLY CONFIRMS PRE-1578 MEDICAL-YUNQI 50/50 EQUINOX AND 60/40 SOLSTICE EXTREMA / REVIEWED 論四時氣候 LOCUS IS NOT THE EXACT SANMING MULTI-POINT TABLE / DIRECT YUNQI-YILAN→SANMING GENEALOGY NOT PROVED / BROADER SHARED SEASONAL TIMEKEEPING TRADITION REMAINS POSSIBLE / EXACT SANMING TABLE PROVENANCE STILL OPEN / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO HAI VOTE / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

## 1. Why this batch follows 12CA

Batch 12CA rejected the shortcut that Wan Minying's displayed table is simply the exact Yandu Shoushi 62/38 table. Its next gate was to trace the precise pre-1578 ancestry of the distinctive Sanming sequence rather than stop at generic 40/60 endpoints.

A high-value pre-1578 candidate is Wang Ji's medical-yunqi work 《運氣易覽》, surviving here in a facsimile identified as the Ming Jiajing 12 (1533) Chengqiao print.

## 2. Physical witness and machine evidence

The full source is 《續修四庫全書》第983冊, which reproduces the 1533 Chengqiao-print 《運氣易覽》. A dedicated no-OCR workflow rendered the relevant physical page.

```text
WORKFLOW_RUN=34859366584
ARTIFACT=10354496404
ARTIFACT_DIGEST=sha256:65f611f28d8989ae4d2dc7d25e4ee2ed6e4075b065d8ee36db2bda090a2aff0a
SOURCE_PDF_SHA256=a1b0bcba30eaccacd7860d6444e7e7811d98b3fc3649b5cfcd7657edb31e0b0c
TARGET_PDF_PAGE=8
TARGET_PAGE_SHA256=fcb0597a86bfaeead333ce610ec20114e119680f2583dffa2259dca3e83dadc6
OCR_USED_FOR_GLYPH_CLAIMS=false
```

PDF p8 directly carries the heading `論四時氣候`.

## 3. Direct physical readings

No OCR is used for the glyph claims below. The physical page directly reads:

```text
晝夜分五十刻亦陰陽之中分
夏至日長不過六十刻陽至此而極
冬至日短不過四十刻陰至此而極
```

Therefore a medical `運氣` source printed in 1533 unquestionably transmits the broad seasonal structure:

```text
equinox -> day/night midpoint at 50/50
summer-solstice day length -> not beyond 60 ke
winter-solstice day length -> not beyond 40 ke
```

This predates the 1578 Sanming physical witness and materially strengthens the pre-Sanming history of the 40/60 family.

## 4. It is not the exact Sanming numeric table

The decisive distinction is **table identity**, not thematic similarity.

The reviewed 《運氣易覽·論四時氣候》 locus gives extrema/bounds. It does not itself print the distinctive Sanming multi-point table such as:

```text
小寒 42/58
立春 45/55
雨水 47/53 -> 48/52
春秋分 near/equal 50/50
夏至 59/41
```

In particular, `夏至日長不過六十刻` is a bound/extreme statement; it is not the same numeric row as Sanming's displayed `59/41`.

Hence the following inference is forbidden:

```text
1533 Yunqi Yilan contains the exact Sanming table
  -> therefore Sanming copied this table from Yunqi Yilan
```

The evidence supports a **broader shared seasonal-timekeeping tradition**, not direct textual genealogy or exact numeric-table equivalence.

## 5. Philological consequence

This result is useful precisely because it separates three layers that would otherwise be conflated:

1. general hundred-ke seasonal extrema (`40/60`, `50/50`);
2. an interpolated or conventionally rounded multi-point seasonal table;
3. a locality-specific official-calendar table such as Yandu Shoushi `38/62`.

The 1533 medical witness closes layer 1 before Sanming. It does not identify layer 2's exact ancestor or location, and it does not convert layer 3 into Sanming's table.

## 6. Product adjudication

For `HPA-ZDATE-006`:

- pre-1578 medical-yunqi 50/50 and 60/40 tradition: **physically attested**;
- exact Yunqi Yilan = Sanming multi-point table: **rejected**;
- direct Yunqi Yilan -> Sanming genealogy: **not proved**;
- exact Sanming table provenance/locality: **open**;
- upper-Zi -> Hai mechanical vote: **0**;
- new runtime candidate: **none**;
- runtime winner: **none**;
- algorithm reopen: **no**;
- `HPA-ZDATE-006`: remains `MISSING_FROM_PRODUCT`.

## 7. Next gate

Search the exact multi-point fingerprint, not merely the endpoints. Priority strings include combinations of `小寒 42/58`, `立春 45/55`, `雨水 47/53 -> 48/52`, and `夏至 59/41` in pre-1578 calendrical, leak-clock, almanac, medical-yunqi and mantic sources. Later exact matches may establish downstream transmission or a shared ancestor, but by chronology cannot be promoted into an ancestor of the 1578 witness.

Research record: `docs/research/ZIWEI-YUNQI-YILAN-1533-SEASONAL-EXTREMA-R1.json`.
