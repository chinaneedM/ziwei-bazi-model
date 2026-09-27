# Fusion Chart Historical Provenance Audit R1 — Batch 12HP

## 1959《北京图书馆善本书目》“瞿捐”：FID 412004000070 / 铁琴铜剑楼元印十行本对象身份闭合

Status: **1959 DIRECT SCAN = EXACT TITLE + 元刻明修本 + 三十二冊 + 瞿捐 / NLC CATALOG METHOD CONFIRMS DONOR-SURNAME SEMANTICS / NLC HISTORY CONFIRMS QU-FAMILY TIEQIN DONATION TO NATIONAL LIBRARY / FID070 ↔ ZHANG TIEQIN PHYSICAL COPY HIGH-CONFIDENCE CLOSED AT MULTILAYER CATALOG-DONOR-PROVENANCE-FORMAT LEVEL / CURRENT SYS-UID-905S AND 1959→1987 NUMBER SUCCESSION STILL UNRESOLVED / ZERO PRODUCT OR MATRIX CHANGE**

## 1. Why this batch changes the object-identity status

12HO directly saw provenance-seal traces on FID070 but could not read the seal text. It therefore correctly retained:

```text
FID070 == Zhang Tieqin physical copy
= STRONGLY_COMPATIBLE_NOT_PROVED
```

12HP takes a different route: not seal-shape inference, but an institutional historical catalog that directly prints the donor surname on the exact old-catalog object.

## 2. 1959 direct visual target

Source:

```text
《北京图书馆善本书目》 第1册
北京图书馆
1959
public scan: Wikimedia Commons

PDF SHA256
3f7eb1d2ab0057f4524eee2fb3dd3ca08561257302ffed32fe1960188184452f

PDF pages = 104
target = PDF page 56
target render SHA256
39f4348a6d0c3edbf353452251a5037ab9d3b0c88a35533940051382ca689835
```

The page was reviewed directly from the hash-bound scan. OCR was not used for the adjudication.

The target column reads:

```text
附釋音春秋左傳註疏六十卷
晉杜預
唐孔穎達撰
唐陸德明釋文

元刻明修本
三十二冊
瞿捐
```

The number printed below the same column is:

```text
三三六八
= 3368
```

Google Books volume `8HUnrRREKsoC` / `PP64` was used only as a navigation locator. The textual authority is the direct 1959 scan.

Probe:

```text
run      = 36313051367
artifact = 10929183632
zip sha256 =
6701b3ac7dcbeb160b48e2d33b2048cb185c1cecf7b8b3ffefdcc57cb240e908
OCR_USED = false
```

## 3. What “瞿捐” means in this catalog

A National Library of China / China Ancient Books Protection catalog-history article states that the 1959 `《北京图书馆善本书目》` continued the source-annotation tradition and:

```text
于每部书后详注捐书人姓氏
```

with the purpose/effect of clarifying the provenance of NLC rare books.

Therefore the target's:

```text
瞿捐
```

is not treated as a guessed ownership seal or OCR fragment. It is the catalog's **Qu-surname donation/source notation**.

Source:

```text
https://www.nlc.cn/pcab/ztzl/tsgb/2020/202210/P020221017510797685830.pdf
```

## 4. The Qu donation is independently tied to Tieqin Tongjian Lou

The NLC / China Ancient Books Protection history page states that fifth-generation owners:

```text
瞿济苍
瞿旭初
瞿凤起
```

donated/transferred more than 700 rare-book works from **铁琴铜剑楼** to the National Library.

Source:

```text
https://www.nlc.cn/pcab/zx/xw/20200414_191069.shtml
```

The project's previously registered NLC retrospective also records the early-1950s Qu/Tieqin books entering Beijing Library through mixed donation/sale batches.

Thus:

```text
1959 exact target + 瞿捐
      ↓
Qu-family donation provenance
      ↓
Tieqin Tongjian Lou → National Library
```

is now institutionally supported.

## 5. Why this identifies FID070 rather than merely another same-title copy

The donor bridge is combined with five independent layers already closed in HK–HO.

### A. Historical Tieqin catalog

```text
附释音春秋左传注疏六十卷
旧藏黄氏百宋一廛
十行十七字
小字双行二十三字
```

### B. 1987 Beijing Library catalog

```text
附釋音春秋左傳註疏六十卷
元刻明修本
三十二冊
十行十七字
小字雙行二十三字
书号 3388
```

### C. 1985 NLC microfilm original-control layer

```text
455$1 original control = 001412004000070
元[1271-1368]
明[1368-1644]重修
善本 / 刻本
32册
```

### D. NLC-backed digital object

```text
FID = 412004000070
32 digital books
卷首 / 卷1 → 卷60
```

### E. Zhang Lijuan's NLC physical research

The official NOPSS report identifies an NLC-held:

```text
铁琴铜剑楼旧藏
十行本
旧著录：元刻明修本
实物审定：元刻元印十行本
```

12HP therefore has not only title similarity, but donor provenance + old classification + extent + line format + holder + digital/microfilm original-control convergence.

Adjudication:

```text
FID070 == Zhang Lijuan's Tieqin-Yuan physical copy
= HIGH_CONFIDENCE_CLOSED_AT_MULTILAYER_HISTORICAL_CATALOG_DONOR_PROVENANCE_AND_FORMAT_LEVEL

SAME_PHYSICAL_OBJECT_IDENTITY_AUTHORIZED=true
```

This forward-revises 12HO. HO itself is not rewritten and remains an auditable record of the earlier evidence state.

## 6. What is still unresolved

The identity closure does **not** make the following identifiers interchangeable:

```text
1959 printed bottom number = 3368
1987 book number           = 3388
digital FID                = 412004000070
current SYS                = UNRESOLVED
current UID                = UNRESOLVED
current 905s               = UNRESOLVED
current shelfmark          = UNRESOLVED
```

No direct 1959→1987 renumbering record has been recovered.

Therefore:

```text
3368 == 3388 as identifier
= FALSE / NOT CLAIMED

3368 -> 3388 renumbering mechanism
= UNRESOLVED

3388 -> 03388 zero padding
= FORBIDDEN
```

The faded physical seal on FID070 book1 page2 also remains unreadable. 12HP no longer needs to guess that seal to establish the object's Qu/Tieqin provenance.

## 7. HJ / Zhao 1951 firewall

The newly closed Qu/Tieqin identity does not automatically identify Zhao Wanli's 1951 named:

```text
宋刻《春秋左传注疏》
```

The historical Tieqin catalog contains layered Song-carving / Yuan-impression language, while Zhao's contemporaneous phrase lacks a stable accession/shelfmark bridge.

Therefore:

```text
HJ MEMBER == FID070
= UNRESOLVED
```

A contemporaneous acquisition/object crosswalk is still required.

## 8. Target-volume and product firewalls

12HP does not name or alter the acquisition route of:

- `《铜壶漏箭制度》`;
- `《准斋心制几漏图式》`;
- historical `3482 / 3483`.

No purchase/donation/Ding route is selected for those target works.

```text
MATRIX_COUNT_CHANGE=false
RUNTIME_RULE_CHANGE=false
ALGORITHM_REOPEN=false
CANDIDATE_COLLAPSE=false
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Accounting remains:

```text
Matrix rows = 198
audited rows = 166
MISSING_FROM_PRODUCT = 10
provenance metadata defects = 14 / 14 repaired
confirmed chart algorithm defects = 0
```

## 9. Highest next gate

1. determine the exact Qu donation/purchase batch and accession date for this now-identified object from 1950–1954 transfer/accession records;
2. recover the current NLC `SYS / UID / 905s / shelfmark`;
3. explain the 1959 printed number `3368` versus the 1987 book number `3388` only through a direct catalog-renumbering/crosswalk source;
4. continue Zhang 2018 full-text retrieval for explicit identifiers and physical details;
5. keep Zhao 1951 and target 3482/3483 acquisition-object mappings separately evidence-gated.

Research record: `docs/research/ZIWEI-BEITU1959-ZUOZHUAN-QU-DONATION-FID070-TIEQIN-IDENTITY-CLOSURE-R1.json`.
