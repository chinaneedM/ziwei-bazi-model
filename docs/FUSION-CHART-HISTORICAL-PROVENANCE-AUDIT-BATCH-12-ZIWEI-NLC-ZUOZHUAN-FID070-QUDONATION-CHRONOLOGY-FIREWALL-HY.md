# Fusion Chart Historical Provenance Audit R1 — Batch 12HY

## FID070 “瞿捐”入藏年代防火墙：捐赠属性闭合，精确批次/日期仍未闭合

Status: **1959 EXACT TARGET “瞿捐” = DIRECT QU-SURNAME DONATION PROVENANCE / COLLECTION-LEVEL 1950·1953·1954 DONATION YEARS DO NOT BIND TARGET / SECONDARY 1950-01-07·1950-03·1953-03 BATCH DATES DO NOT BIND TARGET / 1951 宋刻《春秋左传注疏》 REMAINS CANDIDATE BRIDGE NOT SAME-OBJECT PROOF / 3368→3288 MECHANISM STILL UNRESOLVED / ZERO PRODUCT CHANGE**

## 1. Exact target layer

Batch 12HP already directly reviewed the 1959 《北京图书馆善本书目》 target entry without OCR:

```text
附釋音春秋左傳註疏六十卷
元刻明修本
三十二冊
瞿捐
书号 3368
```

The catalog-method control establishes that the surname notation after a book records donation/source provenance. Therefore the target's Qu-family donation provenance is direct target-level evidence, not an inference from later collection history.

What it does **not** print is a donation year, batch number or exact accession date.

## 2. Collection-level chronology cannot be collapsed onto FID070

The NLC-hosted 2024 study records Qu-family donation activity in 1950, 1953 and 1954. It also explicitly does not enumerate the exact dates and contents needed to bind this object.

Separately, later recounting derived from Ji Shuying chapter 9 reports events at 1950-01-07, 1950-03 and 1953-03. Those dates are retained as secondary batch chronology pending direct chapter/accession-ledger collation.

Neither layer names FID 412004000070 or book no.3368. Therefore no exact target year/date is selected from them.

## 3. 1951 named-member bridge remains a candidate, not a shortcut

A 1951 Zhao Wanli quotation bridge says that Qu Jicang, Qu Fengqi and Qu Xuchu donated 62 titles and names a `宋刻《春秋左传注疏》` as one example.

That is highly relevant, but it is not yet an object identifier. The present target was historically cataloged `元刻明修本` and later physically re-adjudicated as `元刻元印十行本`. Until a stable accession/book-number/object bridge equates the 1951 wording with FID070, the project preserves:

```text
1951 named 宋刻《春秋左传注疏》
== FID070
UNRESOLVED
```

The 1951 line therefore cannot be used to manufacture an exact FID070 transfer date.

## 4. 3368 → 3288 remains the first unresolved gate

Current identifier layers remain:

```text
1959 book number = 3368
1987 book number = 3288
current 905s     = 03288
current SYS      = 002838237
current UID      = UCS01003868188
digital FID      = 412004000070
```

Targeted public searching in this batch did not recover an object-level catalog card, correction slip or preparation record explaining `3368 → 3288`.

That negative search result is **not** absence evidence. The exact mechanism remains unresolved.

The current NLC MARC `801c` values are catalog/record metadata and are not promoted to acquisition dates without field-specific acquisition evidence.

## 5. Adjudication

```text
FID070 Qu-donation provenance            = CLOSED at direct 1959 target-entry level
exact Qu donation year                   = UNRESOLVED
exact Qu donation batch                  = UNRESOLVED
exact Qu donation/accession date         = UNRESOLVED
1951 宋刻《春秋左传注疏》 == FID070        = UNRESOLVED
1959 3368 -> 1987 3288 exact mechanism   = UNRESOLVED
```

The official 1950/1953/1954 years are not treated as an exhaustive target candidate set, and the secondary exact dates are not promoted to target dates.

## 6. Product boundary and accounting

No deterministic chart rule, runtime candidate, Matrix row, transmission topology or algorithm gate changes.

```text
Matrix rows = 198
audited rows = 166
MISSING_FROM_PRODUCT = 10
provenance defects = 16 / 16 repaired
chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```

## 7. Next gate

1. recover an object-specific card/correction slip/catalog-preparation record for `3368 → 3288`;
2. recover a Qu donation/accession ledger or list explicitly binding this title, `3368`, FID070 or another stable object fingerprint to a precise batch/date;
3. continue Zhang Lijuan 2018 full-text retrieval;
4. continue exact source-copy binding for the 2017 Shanghai Ancient Books facsimile.

Research record: `docs/research/ZIWEI-NLC-ZUOZHUAN-FID070-QUDONATION-CHRONOLOGY-FIREWALL-R1.json`.
