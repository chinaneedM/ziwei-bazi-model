# Batch 12DN — 大統 C-II-N 整刻跨越校讀與 1616/1624 年 59/41 階梯後出同源控制

## Status

`COMPLETED_RESEARCH_BATCH / FORWARD_ONLY_CORRECTION / POST1578_HOMOLOGY_CONTROL`

This batch follows the parallel gate left open by 12DM. It does **not** submit any NLC reproduction request and does not reopen the deterministic chart product.

## 1. Why this batch

Batch 12CG had already shown that the Nanjing/Datong C-II-N daily sunrise/sunset table spans the numerical range needed by the 1578 Sanming 59/41 ladder, but its selected cells were explicitly `DIRECT_VISUAL_APPROX` and the historical whole-ke selection rule remained unresolved.

A renewed no-OCR review of the already archived NCL-06267 page renders exposed one exact-indexing defect in that exploratory replay and a stronger mechanical clue: the daily half-day curve crosses whole daylight-ke boundaries at the same scale as a coherent later 59/41 stepped table preserved in 1616 《朱翼》 and 1624 《類經圖翼》.

## 2. Direct C-II-N re-collation: Batch 12CG day-67 correction

The source remains workflow `34869676923`, artifact `10358685142`, NCL-06267. OCR is not used for the corrected numerical cells.

Direct page-06 column alignment reads:

```text
六十六日 半晝分 = 二千三百四八七三 = 2348.73
六十七日 半晝分 = [承前二千三百]五五三七 = 2355.37
```

Using `full daylight ke = 2 * half-day fen / 100`:

```text
day 66 = 46.9746 ke
day 67 = 47.1074 ke
day 73 = 47.9052 ke
day 74 = 48.0380 ke
```

Thus 47 ke is crossed between days 66/67 and 48 ke between days 73/74. Page 05 independently keeps day 59 at `2302.41 -> 46.0482 ke`.

Batch 12CG's `day67=2348.62` was explicitly `DIRECT_VISUAL_APPROX`. 12DN therefore records it as `SUPERSEDED_FOR_EXACT_DAY_INDEXING_ONLY`; the old batch is not rewritten and the broad C-II-N/Nanjing range conclusion is unchanged.

## 3. 1616 《朱翼》: postdated control

Bibliographic control places 江旭奇《朱翼》十二卷 in a 明萬曆四十四年（1616）刻本. The source-linked CADAL/Shidian transcription preserves a 59/41-cap stepped day/night table family. The transcription is used as mechanical/locator evidence, not direct glyph authority.

Chronology is decisive: 1616 is later than Sanming 1578, so it cannot be a direct ancestor of the 1578 physical table.

## 4. 1624 《類經圖翼》: cleaner stepped recension

Bibliographic controls bind 張介賓《類經圖翼》 to the 天啟四年（1624） edition family. The received `四季日躔宿度晝夜長短刻數` table includes:

```text
冬至 41/59
小寒後六日 42/58
大寒後四日 43/57
大寒後十三日 44/56
立春後六日 45/55
立春後十三日 46/54
雨水後六日 47/53
雨水後十三日 48/52
驚蟄後六日 49/51
夏至 59/41
```

This is a coherent later 59/41 stepped branch. It does **not** prove that the 1624 recension is older, more original, or copied from the same exemplar as Sanming/Yueling.

## 5. Mechanical consequence

The direct C-II-N correction exposes exact adjacent-day crossings `46.9746 -> 47.1074` and `47.9052 -> 48.0380`. These materially strengthen a two-layer model:

```text
continuous Nanjing/Datong daily numerical substrate
+
whole-ke selection / transition-day layer
```

12DN does **not** promote a global `floor()` or `round()` rule. The C-II-N summer extremum remains below exact 59.0 ke while received tables display 59/41, so a single universal fraction-discard rule would overclaim the evidence.

## 6. Genealogy consequence

12DN adds a postdated stepped-table family and two postdated textual attestations. It strengthens only a structural-mechanism candidate from C-II-N to that later family. Chronology explicitly blocks both later works from direct ancestry into Sanming 1578.

```text
PRE1578_EXACT_PARENT = UNRESOLVED
SANMING_YUELING_DAHAN_YUSHUI_FINGERPRINT_PARENT = UNRESOLVED
CII_N_TO_WHOLE_KE_MECHANICAL_BRIDGE = STRENGTHENED_NOT_CLOSED
```

No postdated witness receives a pre-1578 ancestry vote.

## 7. Product adjudication

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=12
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=12
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

No runtime candidate, winner, collapse or chart-algorithm reopen is authorized.

## 8. Next gate

1. search securely pre-1578 Chinese witnesses for the coherent 59/41 stepped pattern, especially `立春/雨水 +6/+13` transitions;
2. continue direct C-II-N page re-collation around earlier integer crossings and the summer extremum, looking for a historically defensible selection rule rather than fitting a modern rounding function;
3. keep the exact Sanming/Yueling `大寒十三後 / 雨水後四日` branch separate until a pre-1578 carrier or explicit editorial/reduction rule closes it;
4. continue the NLC call-14202 reproduction route in parallel under the Batch 12DM external-action firewall.

Research record: `docs/research/ZIWEI-DATONG-CIIN-INTEGER-CROSSING-AND-POST1578-59-41-LADDER-R1.json`.
