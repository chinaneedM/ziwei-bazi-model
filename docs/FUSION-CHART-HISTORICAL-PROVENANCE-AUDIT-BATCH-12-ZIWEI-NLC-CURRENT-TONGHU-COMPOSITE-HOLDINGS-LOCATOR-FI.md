# Fusion Chart Historical Provenance Audit R1 — Batch 12FI

## 國家圖書館 current meta：《銅壺漏箭制度》SYS/UID/905 館藏定位與 03482/03483 當前成對閉合

Status: **CURRENT NLC TONGHU ORIGINAL RECORD CLOSED / SYS 001775082 + UID UCS01003828992 CLOSED / CURRENT LOCAL HOLDINGS LOCATOR NLC:SBYL:03482 CLOSED / CURRENT 03482+03483 COMPOSITE LOCATOR PAIR CLOSED AT CATALOG-AND-LOCAL-HOLDINGS LEVEL / TONGHU MICROFILM 455 LINK + SEPARATE-PHOTO 00O003571 CONTROL CLOSED / PUBLIC BARCODE NOT EXPOSED / ACQUISITION ROUTE UNRESOLVED / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Question

Batch 12FH closed the current Zhunzhai rare-book locator as `SYS 001775083 / UID UCS01003828993 / NLC:SBYL:03483`. The next gate was whether the bound companion `銅壺漏箭制度` is separately represented in current NLC metadata and whether its local holdings field carries the expected `03482` component.

## 2. Controlling current-NLC evidence

The browser-native current-meta title probe and item-detail fetch completed successfully:

```text
RUN      = 36021477176
ARTIFACT = 10817116307
DIGEST   = sha256:a46e8a86b8ba020cbbaeaa179dd9ed64410b2ea77e820dd2620ec2ee4b147774
OCR_USED = false
```

Exact simplified-title search returns two microfilm records; a loose title search additionally returns the original rare-book record. The target original is:

```text
SYS = 001775082
UID = UCS01003828992
WDT = 善本
YEA = 1823
PUB = 黃氏士禮居
PAG = 1冊
TIT includes = 銅壺漏箭制度 ; 准齋心製几漏圖式
holding = 国家图书馆
```

The item API directly returns:

```text
905a = NLC
905q = SBYL
905s = 03482
3165 = NLC:SBYL:03482
852a = A100000NLC
```

Using the same 905/SBYL semantic controls already gated in 12FH, the current Tonghu local holdings locator is therefore closed as `NLC:SBYL:03482`. No public barcode is exposed.

## 3. Current composite pair

Batch 12FH and 12FI now give the current pair:

```text
銅壺漏箭制度    SYS 001775082 / UID UCS01003828992 / NLC:SBYL:03482
準齋心製几漏圖式 SYS 001775083 / UID UCS01003828993 / NLC:SBYL:03483
```

This is directly concordant with the 1959 historical catalog numbers 3482/3483 and the legacy OPAC `原文献03482/03483为一册` statement. The numeric continuity is closed, while semantic layers remain separate: historical catalog number != current SYS/UID != current local call-number component != barcode.

## 4. Microfilm symmetry and separate-photo references

The current Tonghu microfilm records include `SYS 002597933 / UID UCS01003581457` and `SYS 002146415 / UID UCS01003553255`. Their first-party 455 original-source note states:

```text
原文献03482铜壶漏箭制度、03483准斋心制几漏图式为一册，准斋心制几漏图式另拍在00O003571
```

The same record family emits raw `455$1 = 001411999008600`, which is parsed by the already-gated UNIMARC rule as embedded tag `001` + linked record-control identifier `411999008600`.

Together with the Zhunzhai microfilm record from 12FH:

```text
Zhunzhai microfilm: raw 455$1 001411999008601 -> embedded 001 + 411999008601; 铜壶另拍在00O003570
Tonghu microfilm:   raw 455$1 001411999008600 -> embedded 001 + 411999008600; 准斋另拍在00O003571
```

Thus the referents of the two `另拍在` values are title-specific and symmetrical. Their exact identifier class/current SYS mapping is still not proved. They remain separate-photo references, not call numbers or barcodes.

## 5. Bounded SYS-neighborhood control

A separate bounded `001775076..001775090` SYS-neighborhood run succeeded overall (run `36021672675`, artifact `10816842828`, digest `sha256:6556ffd58367b3ff4ebcddd439b6caeb832a216ee98a837683ca5d94662432ae`), but requests for `001775082/83` timed out in that specific pass. The timeout has zero negative content authority; the direct title/item API evidence above remains controlling.

## 6. Bibliographic-metadata firewall

The current Tonghu record carries author/title-link metadata that may reflect the bound companion/received cataloging state. Batch 12FI uses the record only for current object-family identity and holdings fields. It does not use the current catalog author string to redetermine the historical authorship/date of either work.

## 7. Acquisition and object-identity firewall

Current paired locators materially strengthen the identification of the reviewed NLC Huang Shiliju composite object. They still do not identify the legal/acquisition event by which the Tieqin copy entered Beijing Library/NLC, and they do not erase Huang's `原書舊鈔 / 錄副` multi-copy firewall. Target-specific sale/donation route remains `UNRESOLVED`; no historical `SAME_OBJECT` collapse is authorized.

## 8. Product firewall

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
MISSING_FROM_PRODUCT=10
PROVENANCE_DEFECTS=13/13_REPAIRED
CONFIRMED_CHART_ALGORITHM_DEFECTS=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
DIRECT_SANMING_PARENT_VOTE_INCREMENT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 9. Next gate

1. map `00O003570` and `00O003571` to any first-party current microfilm/photo-service identifiers without inferring from sequence alone;
2. test `411999008600/411999008601` as linked record-control identifiers through first-party catalog routes; current SYS nonreturn/timeout is not a negative physical-record conclusion;
3. continue target-specific Qu-family sale/donation/transfer/accession research;
4. keep the pre-1578 Zhunzhai rule line and independent Sanming/Yueling Dahan–Rainwater + Nanjing-59 lines active.

Research record: `docs/research/ZIWEI-NLC-CURRENT-TONGHU-COMPOSITE-HOLDINGS-LOCATOR-R1.json`.
