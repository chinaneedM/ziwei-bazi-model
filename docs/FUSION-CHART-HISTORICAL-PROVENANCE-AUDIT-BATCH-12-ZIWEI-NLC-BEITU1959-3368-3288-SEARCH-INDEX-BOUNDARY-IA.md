# Fusion Chart Historical Provenance Audit R1 — Batch 12IA

## 3368→3288 检索能力边界：NLC 现行 ANY 检索不索引已知 905s；Google Books“三二八八”命中经直接扫描复核均为假阳性

Status: **NLC NUMERIC SEARCH NOT A VALID 905s EXISTENCE TEST / KNOWN-POSITIVE 03288 AND 08643 BOTH NO-MATCH / 03368 NO-MATCH HAS ZERO ABSENCE VALUE / GOOGLE BOOKS NUMBER SEARCH = NAVIGATION ONLY / PP34·PP36·PP60 FALSE POSITIVE LOCATORS / EXACT CAUSE STILL UNRESOLVED / ZERO PRODUCT CHANGE**

## 1. NLC current-search calibration

IA-r1 returned no match for 3368, 03368 and SBYL:03368. The only title+3368 result was an unrelated modern 科技文献索引 record whose title contains the numeric range 2222-3368.

IA-r2 then tested the same ANY-search endpoint with two known-positive current 905s values already closed from direct current detail records:

- FID070 target: 03288
- adjacent Liu Shugang copy: 08643

Both also returned no matching result. Therefore the endpoint is not a valid 905s existence test, and a no-result for 03368 is not absence evidence.

## 2. Google Books within-volume index boundary

For Google Books volume 8HUnrRREKsoC, SearchWithinVolume2 returned:

- 三三六八 → PP38, PP46, PP69
- 三二八八 → PP34, PP36, PP60
- title + 三三六八 → PP61, PP64
- title + 三二八八 → PP61, PP64

The two conflicting context queries returning the same PP61/PP64 tokens demonstrates non-exact/noisy matching. Google Books is therefore used only as a navigation locator.

## 3. Direct review of all 三二八八 locator candidates

The already-closed target context provides the same-volume navigation calibration PP64 → direct 1959 PDF56. The three 三二八八 candidate tokens were therefore checked on the hash-bound 1959 scan:

| Google token | Direct PDF page | Render SHA256 | Exact 三二八八 / 3288 observed |
|---|---:|---|---|
| PP34 | 26 | 8765afd36b8347470201696d52002f51cb120d1a5f7369c3a64fec9e0de21332 | No |
| PP36 | 28 | 8e0494babfdc94a7e8230529d04e0a487a6b2c825e5997e7dc92e0d4c251d9e7 | No |
| PP60 | 52 | 6cdc7652422601d5bfaf6ef98df6f9b878c4233190e0a1be06760e09203864cf | No |

Review method: manual visual review of the hash-bound 1959 scan; project OCR was not used.

All three machine-locator hits are closed as false positives. This does not prove that 3288 never appears elsewhere in the entire 1959 catalog.

## 4. Adjudication

The HZ result remains controlling: the observed change is target-specific within the shared local neighborhood, but scope is not cause.

Still unresolved are whether 1959 3368 was itself an error, whether 1987 made a target-specific correction, whether the target was specifically reassigned during recompilation, or whether another preparation change occurred.

## 5. Audit controls

- IA-r1: run 36334400075 / job 108662362799 / artifact 10936492350
- IA-r2: run 36334535925 / job 108662747067 / artifact 10936103311
- IA-r3: run 36334790433 / job 108663460114 / artifact 10936499347
- 1959 source PDF SHA256: 3f7eb1d2ab0057f4524eee2fb3dd3ca08561257302ffed32fe1960188184452f

## 6. Project boundary

No deterministic chart rule, Matrix row, candidate, transmission edge or provenance-defect count changes. Accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 16 of 16 provenance defects repaired / zero chart-algorithm defects, reopens or candidate collapses.

## 7. Highest next gate

The search shortcuts are exhausted. The highest gate is documentary: recover a target-specific catalog card, correction slip, catalog-preparation note, accession register or explicit 1959→1987 crosswalk naming 3368 and/or 3288. Zhang Lijuan 2018 full text, exact Qu donation/accession record and 2017 facsimile base-copy binding remain parallel gates.

Research record: `docs/research/ZIWEI-NLC-BEITU1959-3368-3288-SEARCH-INDEX-BOUNDARY-R1.json`.
