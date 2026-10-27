# Fusion Chart Historical Provenance Audit R1 — Batch 12IB

## 1959《北京图书馆善本书目》八册跨卷 3288 定位：公开扫描全量路由闭合，但机器检索正样本校准失败，零命中不得作阴性证据

Status: **EIGHT PUBLIC VOLUMES MAPPED / R5 ALL-VOLUME ZERO CANDIDATES OBSERVED / KNOWN-POSITIVE 3368 AND NEIGHBOR CONTROLS NOT RECALLED / EMBEDDED TEXT LAYER ABSENT ON POSITIVE PAGES / 48-VARIANT AND 64-VARIANT OCR CALIBRATIONS BOTH ZERO-POSITIVE / WHOLE-CATALOG ABSENCE INFERENCE FORBIDDEN / 3368→3288 CAUSE STILL UNRESOLVED / ZERO PRODUCT CHANGE**

## 1. Why Batch 12IB exists

Batch 12IA closed the current NLC numeric-search and Google Books index shortcuts as non-authoritative navigation layers. It did **not** prove that 3288 is absent from the complete 1959 catalog.

12IB therefore tested the stronger public-scan route: the complete eight-volume 1959 《北京图书馆善本书目》 set exposed by Wikimedia Commons, SSID 12335507–12335514.

The goal was deliberately narrow: determine whether a machine locator could be calibrated against already-known positive catalog numbers strongly enough to make cross-volume navigation useful. OCR was never authorized as historical textual authority.

## 2. Complete public scan map

The provider exposes all eight volumes. The route-map workflow bound the public files to the following Commons SHA-1 values:

| volume | SSID | pages | Commons SHA-1 |
|---|---:|---:|---|
| 1 | 12335507 | 104 | 3ff9c94a69a5b5b799d65fba4a6d00fc2daecc97 |
| 2 | 12335508 | 127 | 0aa66bca2fa78068712d28361d53dbe8a52d5590 |
| 3 | 12335509 | 118 | 92f14b7818d4b8d01ca01d1d659fdfaf0a89b4a6 |
| 4 | 12335510 | 163 | d400c10df649f2ff2ca85cedcc87c18128531c90 |
| 5 | 12335511 | 154 | 1e4a7f26eb4d825a73e0cdc746adba71faab3579 |
| 6 | 12335512 | 139 | f981a9257737fa3dc136a5eb36b3616c60cdeefc |
| 7 | 12335513 | 164 | 64edc5f16e1a24f610b52306b4f607124cbbe97a |
| 8 | 12335514 | 193 | e34d425ab6794e197d0ddf84b13e5a1b57d0912a |

Route-map control: run `36363002709`, artifact `10946168006`, digest `sha256:13b1be326f15cf042e1ba93b9037f18d8bcf691fc64f58d0700a5d69009a3f7b`.

This closes **public scan availability**, not searchable text quality.

## 3. Full eight-volume locator result and its fatal calibration problem

The r5 workflow (run `36503637232`) completed all eight volumes and returned candidate count `0` for every volume.

That output cannot be promoted to a negative catalog conclusion because the same locator failed its positive control on volume 1:

- PDF55 already has directly visually closed catalog-number controls from Batch 12HZ;
- PDF56 already directly prints the target's 1959 book number `三三六八 = 3368`;
- r5 recognized **none** of the configured positive controls on either page.

Therefore:

```text
R5_ALL_VOLUMES_CANDIDATE_COUNT_ZERO = OBSERVED
R5_KNOWN_POSITIVE_CALIBRATION = FAILED
R5_ZERO_RESULT_ABSENCE_VALUE = ZERO
```

The eight r5 artifacts remain retained as method evidence, not bibliographic negative evidence.

## 4. Independent calibration attempts

### 4.1 Embedded PDF text layer

Run `36504285825` / artifact `11007166228` tested `pdftotext` and font presence on known-positive pages 55–56.

Both raw and layout extraction produced only two form-feed bytes, zero non-whitespace characters, and no font listing. Thus the scan has no usable embedded text layer on the positive controls.

This is an access/searchability fact only. It says nothing about whether 3288 is printed elsewhere.

### 4.2 Conventional OCR calibration

Run `36504215889` / artifact `11006222559` tested 48 focused rendering/crop/rotation/page-segmentation variants against the known-positive pages.

Result:

```text
positive variants = 0
3368 positive calibration = FAIL
page55 neighbor-control calibration = FAIL
```

### 4.3 Native Traditional-Chinese vertical OCR calibration

Run `36504602447` / artifact `11006183498` tested 64 variants with `tessdata_best/chi_tra_vert`.

Result:

```text
positive variants = 0
3368 positive calibration = FAIL
page55 neighbor-control calibration = FAIL
```

The workflow's GitHub conclusion is `success` because the script executed and uploaded its artifact. Its **research calibration result is false**. Workflow completion and evidentiary success are explicitly separated.

Earlier r2/r3 whole-volume attempts either failed or timed out and produced no stronger evidence.

## 5. Adjudication

Batch 12IB closes the present machine-locator route as follows:

```text
complete public eight-volume route
= CLOSED

embedded text navigation on known-positive pages
= CLOSED_NO_TEXT_LAYER

tested OCR locator family
= FAILED_KNOWN_POSITIVE_RECALL

all-volume zero candidates
= UNCALIBRATED_NON_EVIDENTIARY

3288 absent from complete 1959 catalog
= NOT PROVED

3288 present elsewhere in complete 1959 catalog
= NOT PROVED

3368 -> 3288 causal mechanism
= UNRESOLVED
```

Batch 12HZ remains controlling for scope: the number change is isolated to the target within the directly shared local neighborhood. Batch 12IA remains controlling for search-index limitations.

A future machine-search method must first pass the direct 3368/neighbor positive calibration before any whole-catalog zero result can even be considered for navigation confidence. OCR itself still cannot become historical textual authority.

## 6. Highest next gate

The productive next gate is documentary, not another uncalibrated whole-catalog OCR sweep:

1. target-specific Beijing Library/NLC catalog card, correction slip, preparation note, accession register or explicit crosswalk naming `3368` and/or `3288`;
2. Zhang Lijuan's 2018 article `国图藏元刻十行本《附释音春秋左传注疏》` for object-level identifiers and version notes;
3. exact Qu-family donation/accession record tied to the title/book number/object;
4. only if a materially new recognition method appears, re-open machine navigation after known-positive calibration passes.

## 7. Project boundary

No chart rule, candidate, Matrix row, provenance-defect count or transmission topology changes.

```text
Matrix rows = 198
audited rows = 166
MISSING_FROM_PRODUCT = 10
provenance defects = 16 / 16 repaired
chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```

Research record: `docs/research/ZIWEI-BEITU1959-CROSSVOLUME-3288-LOCATOR-CALIBRATION-BOUNDARY-R1.json`.
