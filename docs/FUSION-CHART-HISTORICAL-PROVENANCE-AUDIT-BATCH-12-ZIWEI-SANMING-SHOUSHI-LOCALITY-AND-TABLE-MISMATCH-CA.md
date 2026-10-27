# Fusion Chart Historical Provenance Audit R1 — Batch 12CA

## 《三命通會》“授時曆分之”的地域边界与表谱错配：九服地方算法、地中 40/60、燕都 62/38

Status: **YUANSHI SHOUSHI METHOD DIRECTLY SUPPORTS REGIONAL LOCALITY CALIBRATION / NINE-REGION DAY-NIGHT KE DEPEND ON LOCAL POLE ALTITUDE AND MAY BE CALIBRATED BY INSTRUMENT OR WATER CLOCK / MING TECHNICAL TRANSMISSION EXPLICITLY DISTINGUISHES DIZHONG 40/60 FROM YANDU SHOUSHI 62/38 / SANMING TONGHUI DISPLAYED MANTIC TABLE IS NOT THE EXACT YANDU 62/38 TABLE / TIANYIGE MING-PRINT HUQIANJING PHYSICALLY CONFIRMS A BROADER 40/60 SEASONAL LEAK-ARROW TRADITION / NO DIRECT HUQIANJING→SANMING GENEALOGY CLAIM / SANMING SELECTED LOCALITY OR TABLE GENEALOGY STILL UNRESOLVED / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

## 1. Why this batch follows 12BZ

Batch 12BZ closed a primary Ming mantic bridge from difficult natal birth-time adjudication to `授時曆分之`. The remaining question is whether that phrase licenses a unique modern time coordinate or a specific Dadu/Beijing standard.

The answer is no: the Shoushi method itself is explicitly regional, while Wan Minying's displayed table is not the exact Yandu Shoushi table.

## 2. 《元史·授時曆經》: locality is native to the system

《元史》卷55 directly states that the `九服` day/night ke and central-star rates are to be computed according to the local pole altitude. It then gives `求九服所在漏刻`: each place may use instrument observation or a water clock to establish its own solstitial night-ke value, from which the daily values are derived.

Therefore:

- Shoushi is not intrinsically a single location-free table;
- nor is it intrinsically only a Dadu table at the method level;
- regional realization is explicitly part of the received computational framework.

This closes **calendar-system locality capability**, but does not prove Wan Minying recalculated a natal chart for the birthplace.

## 3. Historical distinction: 地中 40/60 versus 燕都 62/38

唐順之《稗編》卷54, transmitting a discussion attributed to 馬端臨, explicitly contrasts:

```text
蔡氏據地中而言：長極六十，短止四十。
授時曆據今燕都而言：長極六十二，短極三十八。
```

This is decisive as a comparative control: differing solstitial ke values can encode differing geographic standards rather than a mere textual error.

It does not by itself establish which table Wan Minying used.

## 4. The Sanming table is not exact Yandu Shoushi

The Ming physical/received 《三命通會》 `論時刻` table includes values such as 小寒 42/58, 立春 45/55, 雨水 47/53 and 48/52, and 夏至 59/41. Its displayed structure therefore does not equal the historical Yandu Shoushi 62/38 extreme table.

Consequently, the phrase `余姑就授時曆分之` must not be normalized into:

```text
use the exact Dadu/Beijing Shoushi day-night table
```

and it certainly does not authorize a modern Beijing longitude/latitude runtime default.

## 5. Tianyige Ming physical 《虎鈐經》 control

To test whether 40/60-style seasonal tables belong to a wider historical timekeeping tradition, a Tianyige Ming-print physical copy of the Song work 《虎鈐經》 was rendered and reviewed without OCR.

- workflow run `34832306143`
- artifact `10342711240`
- artifact digest `sha256:87bd11223e5fdbfe1ec79b2bc4e2a7577fbe459559e0386287c96f3074f2f27d`
- source PDF SHA-256 `52ea8f81c8cd6ccc1000db4bb15a07b18b5e2196966a3ebdcf740bc423686dfc`
- PDF p74 render SHA-256 `a86cade9b99ed1b5cc943370e4b66e914d7968bc08943225bb99530fb15721ab`
- PDF p76 render SHA-256 `2136201c372c0f8ea51dce46c1babcfc135758a98c775afa52c09c39fc8d5534`

PDF p74 directly reads `傳箭第七十六`, the hundred-ke day, and winter-solstice first-arrow `晝四十刻 / 夜六十刻`. PDF p76 reaches the summer-solstice reversal `晝六十刻 / 夜四十刻`.

This physically establishes a broader premodern 40/60 seasonal leak-arrow family. It does **not** prove that 《三命通會》 copied 《虎鈐經》, and no genealogy vote is added.

## 6. Product adjudication

For `HPA-ZDATE-006`:

- `授時曆` regional/locality capability: **closed**;
- Wan Minying actual birthplace localization: **not proved**;
- Sanming table = exact Yandu Shoushi table: **rejected**;
- Dadu/Beijing runtime binding: **not authorized**;
- exact Sanming seasonal-table genealogy: **open**;
- upper-Zi → Hai mechanical vote: **0**;
- runtime candidate: **none**;
- `HPA-ZDATE-006`: remains `MISSING_FROM_PRODUCT`.

## 7. Next gate

Trace the **exact pre-1578 provenance** of the Sanming seasonal table using distinctive multi-point strings rather than the generic 40/60 endpoints. Priority targets are pre-1578 medical `運氣`, almanac/tongshu and calendrical manuals. A later matching table can be used as transmission evidence, never as an ancestor merely because it matches.

Research record: `docs/research/ZIWEI-SANMING-SHOUSHI-LOCALITY-AND-TABLE-MISMATCH-R1.json`.
