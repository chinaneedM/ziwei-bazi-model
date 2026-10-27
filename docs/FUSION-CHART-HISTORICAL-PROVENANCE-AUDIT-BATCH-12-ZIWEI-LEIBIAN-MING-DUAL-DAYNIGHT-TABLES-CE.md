# Fusion Chart Historical Provenance Audit R1 — Batch 12CE

## 明刻《類編曆法通書大全》同卷雙表：40/60 銅壺二十四氣表與 38/62《四時加減晝夜節氣》並存

Status: **INDEPENDENT MING-PRINT PHYSICAL COPY DIRECTLY CONFIRMS TWO DIFFERENT DAY/NIGHT-KE TABLE FAMILIES IN THE SAME VOLUME / COARSE 24-QI COPPER-POT FAMILY REACHES 60/40 AND CONTAINS 59/41 ADJACENT ROWS / FINE FOUR-SEASONS TABLE REACHES 62/38 / SANMING 59/41 AT SUMMER SOLSTICE EQUALS NEITHER TABLE EXACTLY / LATER 1600 XING-YUNLU CONTROL EXPLICITLY EXPLAINS NANJING DATONG 59/41 VS YANDU SHOUSHI 62/38 / EXACT PRE-1578 SANMING TABLE PARENT STILL OPEN / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO HAI VOTE / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

## 1. Why this follows 12CD

Batch 12CD separated the older hundred-ke prose lineage from the older 40↔60 stepwise leak-arrow numeric lineage. The unresolved layer was Ming adaptation: how can a mantic text say `授時曆分之` yet display a table that is not the literal Yandu Shoushi 62/38 table?

The decisive new evidence is that a single Ming-print calendrical/almanac volume physically preserves **more than one day/night-ke convention**.

## 2. Independent Ming-print physical witness

Controlling public object:

```text
TITLE=類編曆法通書大全 第1冊
METADATA_AUTHOR=〔元〕宋魯珍通書
EDITION=刻本
PUBLICATION=明[1368-1644]
PAGE_COUNT=95
EXACT_IMPRESSION_YEAR=UNRESOLVED
```

Evidence chain:

```text
RUN=34866426888
JOB=104051295890
ARTIFACT=10357132602
ARTIFACT_DIGEST=sha256:8dcf2e8e7ffeb987c3c2016545b3d252ed2d0e7ab118bcd240c0b28bafcdc098
SOURCE_PDF_SHA256=50a308f8adbfd7010b398cc68bc64dc66f7c1dbdcfe6470029e04aacd22e6419
P20_SHA256=15325745229581c336e407d0eb405a8ef75c6d3bcf28117209f51f0484af7ce4
P21_SHA256=a348fb2e6c4b06323bcdbc6851aa7f09ca72a76e8ab2d9e08bd50eabf79c3bbe
P24_SHA256=0e94adaf05c5082b680ab210d2bf7703a5c184fe1217aa35b0ee96606870329f
P25_SHA256=f4305f0f8b7e766dd0f31cb4d78ecb15154e6db1820975335bd53ddda109130f
OCR_USED_FOR_GLYPH_CLAIMS=false
```

The earlier run `34866248129` successfully downloaded the same source and rendered all 95 pages, but its contact-sheet step failed because of a page-filename padding bug. It has **no content-negative authority**. The corrected workflow run above succeeded and produced the durable artifact.

## 3. First physical table: coarse 24-qi copper-pot family

PDF pp20-21 directly show the seasonal rows. Secure examples include:

```text
立夏 57/43
小滿 59/41
芒種 60/40
夏至 60/40
小暑 60/40
大暑 59/41
立秋 57/43
處暑 55/45
```

The full received family is the older 40/60-style copper-pot table. Crucially, it contains `59/41`, but **not at the same solar-term anchor as Sanming**: this physical table prints `夏至 60/40`, whereas the 1578 Sanming display prints `夏至 59/41`.

Therefore:

```text
shared number 59/41 != exact table identity
```

## 4. Second physical table: fine 38/62 ladder

On PDF p24 the left leaf directly opens:

```text
四時加減晝夜節氣
```

and begins the winter ladder at `38/62`, then `39/61`, `40/60`, `41/59`, `42/58` and onward. PDF p25 continues the one-ke progression and reaches the summer range culminating at `62/38`.

This is structurally Yandu/Shoushi-like, but it is likewise **not** Sanming's displayed summer-solstice `59/41` table.

## 5. The key historical result is coexistence, not one winning table

The same Ming-print physical volume therefore preserves at least:

```text
A. coarse 24-qi copper-pot 40/60 family
B. fine 四時加減 38/62 family
```

That directly falsifies an overly simple historical normalization:

```text
'mentions Shoushi/calendar division' -> must mean one unique literal 62/38 table everywhere
```

Premodern calendrical/almanac transmission could carry multiple day/night-ke schemes side by side. A mantic author could inherit prose, numerical ladders, locality conventions and term anchors from different layers.

## 6. Later Ming explanatory control: Nanjing 59/41

邢雲路《古今律曆考》卷47 explicitly contrasts two geographic standards:

```text
Yandu / Shoushi:  夏至晝 62 / 夜 38
early-Ming Nanjing Datong: 夏至晝 59 / 夜 41
```

The work is securely represented by a Wanli-28 (1600) print, so it is **later than the 1578 Sanming witness**. It cannot be used as Sanming's ancestor. Its value is explanatory: it proves that the Ming technical tradition itself understood `59/41` as a Nanjing-calibrated Datong layer distinct from Yandu `62/38`.

This materially strengthens—but does not close—the hypothesis that Sanming's `59/41` belongs to a Ming locality-adaptation layer rather than the literal Yandu Shoushi table.

## 7. Chronology firewall

The NLC Leibian object is catalogued only as Ming `[1368-1644]`. Therefore this batch may say:

```text
Ming-print transmission physically preserves both table families.
```

It may **not** say:

```text
this exact physical impression definitely predates 1578;
therefore Sanming copied this exact book.
```

That ancestor claim remains open until an edition securely dated before 1578, or another direct pre-1578 Ming/Nanjing table, is locked.

## 8. Product adjudication

For `HPA-ZDATE-006`:

- Ming-print dual-table coexistence: **physically attested**;
- one-literal-Shoushi-table assumption: **rejected**;
- Sanming = coarse Leibian table: **no**;
- Sanming = fine 38/62 table: **no**;
- Nanjing 59/41 explanatory layer: **strongly supported by later Ming technical testimony**;
- exact pre-1578 table parent: **open**;
- upper-Zi -> Hai vote: **0**;
- runtime candidate/winner/collapse: **none**;
- algorithm reopen: **no**;
- `HPA-ZDATE-006`: remains `MISSING_FROM_PRODUCT`.

## 9. Next gate

Search specifically for a **securely pre-1578 Ming/Nanjing physical or edition-scoped witness** that prints or generates `夏至 59/41` and ideally carries Sanming-like intermediate solar-term anchors. Priority: early Datong almanacs, Nanjing official clepsydra/day-night tables, pre-1578 tongshu recensions, and calendrical appendices. Only then can the adaptation layer move from explanatory model to chronological genealogy.

Research record: `docs/research/ZIWEI-LEIBIAN-MING-DUAL-DAYNIGHT-TABLES-R1.json`.
