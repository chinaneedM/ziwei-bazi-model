# Fusion Chart Historical Provenance Audit R1 — Batch 12CC

## 1569周相《大明大統曆法》实体卷范围与《三命通會》节气刻数指纹核验

Status: **1569 ZHOU-XIANG DATONG PHYSICAL METHOD WITNESS DIRECTLY REVIEWED / ALL 45 RENDERED PAGES OF THE PUBLIC VOL6 OBJECT VISUALLY COLLATED WITHOUT OCR / REVIEWED OBJECT DOES NOT DIRECTLY EXPOSE SANMING 42/58...59/41 SEASONAL DAY-NIGHT TABLE / VOLUME-SCOPED NONATTESTATION ONLY / GLOBAL DATONG ABSENCE FORBIDDEN / EXACT SANMING TABLE PROVENANCE STILL OPEN / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO HAI VOTE / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

## 1. Why this batch follows 12CB

Batch 12CB physically established that the 1533 Chengqiao-print 《運氣易覽》 carries an earlier 50/50 and 60/40 seasonal-extrema tradition, but not the exact multi-point sequence displayed by the 1578 《三命通會》 witness.

A natural next candidate is Zhou Xiang's 1569 《大明大統曆法》: it is pre-1578, belongs to the Ming Datong calendrical horizon, and therefore must be checked directly rather than inferred from later descriptions of Ming day/night standards.

## 2. Physical witness and machine evidence

A dedicated workflow downloaded and rendered the entire public volume without OCR.

```text
WORKFLOW_RUN=34860488890
ARTIFACT=10354907760
ARTIFACT_DIGEST=sha256:55dce049de5bf8ede84b0f2bae89dc4733617136033e6f6f8700964b7c8e981b
SOURCE_PDF_SHA256=4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c
PAGE_COUNT=45
OCR_USED_FOR_GLYPH_CLAIMS=false
RENDER_TRIGGER_COMMIT=35f401a92e0d23f1292301b9372fea6546eab71b
EXACT_HEAD_CI_RUN=34860488925
```

The render workflow and the normal CI both passed on the same triggering HEAD. This provides a reproducible evidence object and closes the acquisition layer for this particular public volume.

## 3. Direct physical scope review

The full 45-page object was reviewed through full-volume contact sheets and targeted full-page renders.

Key controls include:

- PDF p1: title/cover `大明大統曆法`;
- PDF p2: `曆原` and calendrical exposition;
- PDF p14: `推盈縮曆初末限分法`, with adjacent `太陽冬至前後立成卷第二`; its table is solar-anomaly/calculation material rather than a day/night-ke table;
- later pages continue calendar arithmetic, lunar-motion/遲疾, eclipse and related computational tables;
- PDF p42 is likewise calculation/date-grid material, not the target seasonal day/night table.

Across the reviewed object, the distinctive Sanming fingerprint was not directly observed:

```text
小寒 42/58
立春 45/55
雨水 47/53 -> 48/52
春秋分 near/equal 50/50
夏至 59/41
```

## 4. The negative is strictly volume scoped

This batch does **not** authorize:

```text
reviewed 45-page object lacks the target table
  -> no Ming Datong text ever contained such a table
```

That inference is invalid. The Datong tradition includes multiple books, recensions, official almanacs, separately transmitted calculation tables and locality-sensitive material. This batch only establishes:

```text
THIS_PUBLIC_1569_VOL6_OBJECT -> exact Sanming multipoint table NOT OBSERVED
```

Therefore the 1569 object remains a strong primary Ming Datong **method witness**, but it is not yet a direct table-genealogy witness for the Sanming sequence.

## 5. Consequence for the 59/41 hypothesis

Later Ming/received explanatory material makes the Datong 59/41 and Nanjing-locality layer an important research lead. However, chronology and source scope matter:

- later explanation cannot be promoted into pre-1578 direct proof;
- the reviewed 1569 object does not itself close that table;
- a genuine ancestor claim still requires a pre-1578 direct table witness, a demonstrably generative calculation, or an edition-scoped textual bridge.

A composite transmission remains plausible but unproved:

```text
older hundred-ke / midnight prose
  + older seasonal leak-arrow tables
  + Ming locality/calendar adaptation
  -> Sanming displayed table
```

Plausibility is not genealogy.

## 6. Product adjudication

For `HPA-ZDATE-006`:

- 1569 Zhou-Xiang Datong primary method witness: **directly reviewed**;
- exact Sanming multi-point table in this reviewed object: **not observed**;
- global Datong absence: **not authorized**;
- exact Sanming table ancestry/locality: **open**;
- upper-Zi -> Hai mechanical vote: **0**;
- new runtime candidate: **none**;
- runtime winner: **none**;
- candidate collapse: **none**;
- algorithm reopen: **no**;
- `HPA-ZDATE-006`: remains `MISSING_FROM_PRODUCT`.

## 7. Next gate

The search now moves one layer deeper: reconstruct the **pre-Ming/Song-Yuan seasonal leak-clock lineages** and compare their whole sequence against Sanming, not just 40/60 endpoints. Priority controls are Zhao Youqin's 《革象新書》 hundred-ke/midnight prose, the Song-work 《虎鈐經·傳箭》 stepwise arrow sequence, and the Yuan/Song-Luzhen 《類編曆法通書大全》 24-qi day/night table. In parallel, continue looking for a pre-1578 Ming Datong/Nanjing witness that directly carries the 59/41 layer.

Research record: `docs/research/ZIWEI-DATONG-1569-VOL6-TABLE-FINGERPRINT-R1.json`.
