# Fusion Chart Historical Provenance Audit R1 — Batch 12HT

## 1959/1987 同属“书号”与 3368 → 3288 重编环境边界

Status: **1959 `3368` = DIRECT BOOK NUMBER / 1987 `3288` = DIRECT BOOK NUMBER / 1987 CATALOG IS A BROADER 1910–1986 RECOMPILATION THAT EXPLICITLY CORRECTED SOME EARLIER CATALOGING ERRORS / BLANKET ARITHMETIC RENUMBERING DISPROVEN / EXACT TARGET-SPECIFIC 3368→3288 MECHANISM STILL UNRESOLVED / ZERO PRODUCT OR MATRIX CHANGE**

## 1. Why this batch exists

Batch 12HS closed the corrected chain:

```text
1987 书号 3288
→ current 905s 03288
→ SYS 002838237 / UID UCS01003868188
→ FID 412004000070
```

The remaining historical question is why the 1959 catalog gives the same physical object `3368`.

Until now the project often described the 1959 value conservatively as a “printed number”. Direct review of the 1959 catalog's own 编例 now permits a stronger semantic statement: **3368 itself is also a 书号**.

## 2. 1959 catalog semantics: 3368 is a 书号

Hash-bound 1959 scan:

```text
PDF SHA-256 = 3f7eb1d2ab0057f4524eee2fb3dd3ca08561257302ffed32fe1960188184452f
OCR_USED    = false
```

The 1959 编例 states directly:

> 书名下方均著书号，以便检索。

Therefore the target's directly reviewed `3368` is not merely an unexplained bottom-of-column number. It is:

```text
1959 target 3368 = BOOK NUMBER
```

The same 编例 also shows that this 1959 catalog is not a complete historical inventory of every holding since the library's founding. Its principal scope is the first decade's newly acquired books after 1949, with 1937–1948 acquisitions also included.

Target remains:

```text
附釋音春秋左傳註疏六十卷
元刻明修本
三十二冊
瞿捐
书号 3368
```

## 3. 1987 catalog semantics and recompilation context

The 1987 catalog's own 前言 states that after the 1959 catalog, holdings continued to grow; after the 1980 national rare-book catalog work and further acquisitions, Beijing Library began compiling the new catalog in 1986.

Most importantly, the foreword explicitly says the new catalog:

> 纠正了一些以往著录的失误

The 1987 编例 then defines its much broader scope as rare books acquired from the library's establishment in 1910 through 1986, and again explicitly defines the number below each title as 书号.

Thus:

```text
1987 corrected target 3288 = BOOK NUMBER
1987 catalog = fresh/broader recompilation environment
generic prior-catalog correction activity = directly attested
```

This does **not** prove that the target's 3368→3288 change was specifically one of those corrected errors.

## 4. Why a blanket renumbering formula is ruled out

Batch 12HS already provides a same-neighborhood control:

```text
target:
1959 3368 → 1987 3288

adjacent 春秋左傳註疏六十卷:
1959 10010 → 1987 10010
```

Therefore:

```text
blanket/global/local arithmetic offset = DISPROVEN
```

The target changes by -80 while the adjacent shared record does not change at all.

No rule such as “subtract 80”, insertion shift, page shift, or automatic resequencing is authorized.

## 5. What can now be concluded

The evidence closes the following narrower interpretation:

```text
3368 and 3288 are both historical catalog BOOK NUMBERS.
The 1987 book number arose in a documented broader recompilation/correction environment.
The target-specific change is real and object-specific relative to the stable adjacent control.
The exact mechanism that changed 3368 to 3288 remains unresolved.
```

Candidates remain open:

- target-specific reassignment during recompilation;
- a 1959 target book-number catalog/printing error later corrected;
- a 1987 target-specific catalog correction;
- another catalog-preparation change not yet recovered.

None is selected without an object-specific correction slip, catalog card, accession register, or equivalent direct record.

## 6. Identifier firewall

Current controlling layers are:

```text
1959 book number = 3368
1987 book number = 3288
current 905s     = 03288
current SYS      = 002838237
current UID      = UCS01003868188
digital FID      = 412004000070
```

The superseded `3388/03388` project reading remains historical audit trail only and must not re-enter current reasoning.

## 7. Product and accounting consequence

No deterministic chart rule, runtime candidate, Matrix row, or transmission-genealogy topology changes.

```text
Matrix rows = 198
audited rows = 166
MISSING_FROM_PRODUCT = 10
provenance defects = 15 / 15 repaired
confirmed chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```

This batch introduces no new provenance defect; it improves semantic classification and narrows the unresolved historical mechanism.

## 8. Next gate

1. find an object-specific catalog card/correction slip/accession or preparation record explicitly bridging `3368 → 3288`;
2. resolve the exact Qu donation/accession batch and date for FID070;
3. continue Zhang Lijuan 2018 full-text retrieval;
4. separately adjudicate the exact-copy `17字 vs 16字` format-description tension.
