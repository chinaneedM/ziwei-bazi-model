# Fusion Chart Historical Provenance Audit R1 — Batch 12HS

## FID070 当前 905 定位闭环与 1987 书号 3288 前向纠错

Status: **CURRENT NLC TARGET = UID `UCS01003868188` / SYS `002838237` / 905 `NLC : SBYL : 03288`; 1987 DIRECT VISUAL BOOK NUMBER IS `三二八八 = 3288`, NOT 3388; PRIOR 3388 IS FORWARD-CORRECTED AS PROV-DEFECT-015; 1959 `3368` → 1987 `3288` MECHANISM REMAINS UNRESOLVED; ZERO PRODUCT/RUNTIME CHANGE**

## 1. Why this batch exists

Batch 12HR recovered the current 32冊 NLC record at search-result level but deliberately left 905s unresolved.

A focused two-record probe then returned HTTP 200 on the first attempt for both the target and the immediately useful same-title control. More importantly, the target current 905s forced a reinspection of the 1987 catalog number. Magnified direct visual collation shows that the second digit had previously been misread.

This batch records the correction **forward-only**. Earlier HN–HR artifacts are not rewritten; their `3388` reading remains auditable as the prior project state and is superseded here.

## 2. Current NLC target detail

Controlling probe:

```text
workflow run  = 36319489516
job           = 108620434290
artifact      = 10932075967
artifact SHA  = 7fffceaac4ab10128ca638bfb79924649056663520c8bef217f332ff3d2b757d
HEAD          = 15ebf1c8769d8a096c673cbbecbd70336ca30d49
tree          = 88062838265b4b6efcffcb23b7a7513cd223e699
```

Target response:

```text
UID   UCS01003868188
SYS   002838237
001   003868188
题名  附釋音春秋左傳註疏 六十卷
类型  善本 / 刻本
年代  元[1271-1368]
册数  32冊

852a  A100000NLC
905a  NLC
905q  SBYL
905s  03288
910n  002838237
910l  NLC01
```

Following the already established 12FH/12FI field semantics, the current local holdings locator is therefore closed at:

```text
NLC : SBYL : 03288
```

This is a local holdings/call-number layer. It is not a barcode, accession/login number, SYS, UID or FID.

## 3. The 1987 number is 3288, not 3388

The same hash-bound 1987 scan used in Batch 12HN was re-inspected directly, without OCR:

```text
PDF SHA-256 = 9cb2ab3ff5d00fda316a9f0430096ca2a5e68fcd53609a878c0ed9d08a26d3ab
PDF page    = 104
printed page= 92
render SHA  = 04c1c3a8a33aaa3b401db2fd6ddcc77455a94098f01cc178a284ea8b2f42b6ce
```

Under the exact `元刻明修本 / 三十二冊` target column the four Chinese numerals are visibly:

```text
三
二
八
八
```

Therefore:

```text
1987 书号 = 3288
prior project reading 3388 = WRONG
```

This is **PROV-DEFECT-015**, an internal direct-visual transcription error. It is found and repaired in the same batch.

## 4. Same-page control independently validates the leading-zero current form

The neighboring Liu Shugang same-title record supplies a direct control.

1987 catalog:

```text
附釋音春秋左傳註疏六十卷
劉叔剛刻本 / 存二十九卷一至二十九 / 十五冊
书号 8643
```

Current NLC detail:

```text
UID  UCS01003868187
SYS  002838236
3165 NLC:SBYL:08643
905a NLC
905q SBYL
905s 08643
```

Thus, in the same title neighborhood:

```text
8643 -> 08643
3288 -> 03288
```

The target mapping is no longer a speculative zero-padding hypothesis. It is directly closed by the current target 905s and independently controlled by the adjacent record.

This does **not** license blind zero-padding of arbitrary catalog numbers elsewhere.

## 5. 1959 → 1987 is still not a simple arithmetic renumbering

The 1959 target remains directly read as:

```text
瞿捐
元刻明修本
三十二冊
printed number 3368
```

On the same 1959 page, the adjacent `春秋左傳註疏六十卷` record is numbered `10010`.

On the 1987 target page, that same adjacent title remains `10010`, while the target is `3288`.

Therefore:

```text
blanket local arithmetic offset = DISPROVEN
3368 -> 3288 exact mechanism = UNRESOLVED
```

Possible mechanisms—catalog correction, target-specific reassignment, 1959 printing/catalog error, or another preparation change—remain candidates only. None is selected without direct catalog-preparation evidence.

## 6. Identifier firewall after correction

```text
1959 printed catalog number = 3368
1987 book number            = 3288
current 905s                = 03288
current SYS                 = 002838237
current UID                 = UCS01003868188
digital FID                 = 412004000070
```

The prior `3388` reading is superseded. The prior `03388` search hypothesis is rejected by the direct current `905s=03288` response.

## 7. Remaining catalog-description tension

The 1987 target describes `十行十七字 / 小字雙行二十三字`; the current NLC detail returns `10行16字，小字雙行23字，白口，左右雙邊`.

This 17-vs-16 difference is retained as a catalog-description tension. It does not override the direct 3288↔03288 identifier bridge and does not authorize a second provenance defect without stronger adjudication.

## 8. Accounting and product consequence

This repair changes provenance metadata accounting only:

```text
Matrix rows = 198
audited rows = 166
MISSING_FROM_PRODUCT = 10
provenance defects = 15 / 15 repaired
confirmed chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```

No deterministic chart rule, runtime candidate, Matrix row, or transmission-genealogy topology changes.

## 9. Next gate

1. recover direct catalog-preparation/correction/succession evidence for `3368 (1959) -> 3288 (1987/current 905)`;
2. recover the exact Qu donation/accession batch and date for this object;
3. continue Zhang Lijuan 2018 full-text retrieval;
4. separately investigate the 17-vs-16 format-description tension.
