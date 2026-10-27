# Fusion Chart Historical Provenance Audit R1 — Batch 12FL

## 瞿氏鐵琴銅劍樓 → 北京圖書館混合轉移機制與《銅壺／準齋》目標冊入藏邊界

Status: **QU→BEITU COLLECTION-LEVEL MIXED DONATION + PRICED ACQUISITION/SALE CLOSED / TONGHU-ZHUNZHAI TARGET VOLUME EXACT TRANSACTION ROUTE UNRESOLVED / 1959 TARGET ENTRIES NOT MARKED 瞿捐 / ABSENCE DOES NOT SELECT SALE / GAO XIZENG ANNOTATED CATALOG IDENTIFIED AS NEXT TARGET BUT NOT DIRECTLY REVIEWED / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Question

Batch 12FG established that the 1959 《北京圖書館善本書目》 directly records the target bound volume as:

```text
銅壺漏箭制度       3482
準齋心製几漏圖式   3483
清道光三年黃氏士禮居抄本
合一冊
```

and that neither target entry carries the explicit same-catalog provenance notation `瞿捐`.

Batch 12FK then closed the current public NLC digital-object shell but deliberately left the historical acquisition route unresolved.

12FL asks a narrower provenance question:

> Can currently accessible evidence select the exact route by which this Qu-family volume entered Beijing Library/NLC — donation, sale/priced acquisition, or another transfer?

Answer: **No.**

The collection-level Qu→Beijing Library transfer mechanism is now closed as mixed donation plus priced acquisition/sale. The target volume's exact transaction route remains `UNRESOLVED`.

## 2. Institutional collection-level evidence

### 2.1 NLC / China Ancient Books Protection Network retrospective

The National Library of China-hosted retrospective on Zhao Wanli states that in the early 1950s the Qu family selected books from the Shanghai-held Tieqin Tongjian Lou collection and transferred them to Beijing Library through a mixed `半賣半送` process. It separately reports more than 500 titles across three transfer batches and another 246 donated titles.

The same institutional retrospective cites contemporary recollection that Zhao Wanli purchased Tieqin Tongjian Lou books and that a per-volume price was negotiated.

Source:

```text
https://www.nlc.cn/pcab/zy/pxjz/20181227_174775.shtml
```

This closes:

```text
QU_TO_BEITU_TRANSFER_PROGRAM_HAS_DONATION_COMPONENT = true
QU_TO_BEITU_TRANSFER_PROGRAM_HAS_PRICED_SALE_OR_ACQUISITION_COMPONENT = true
COLLECTION_LEVEL_TRANSFER_MODE = MIXED
```

It does **not** name the target Tonghu/Zhunzhai volume as belonging to either component.

### 2.2 2024 NLC-hosted Zheng Zhenduo study

The 2024 NLC-hosted study by Cai Chengpu (National Library of China) and Li Jing (National Museum of China) reconstructs the same transfer program from historical records.

For the Qu family it records:

1. late-1949 mobilization to transfer Tieqin Tongjian Lou books into public custody;
2. early transfer of part of the rare-book collection;
3. Zheng Zhenduo's January 1950 request that the remaining collection later be `陸續價購歸公` by agreement;
4. additional Qu-family donation activity in 1950, 1953 and 1954.

Source:

```text
https://www.nlc.cn/pcab/zx/xw/20240701_2640245.shtml
```

The article points to archival/history materials that become direct next targets:

```text
《北京圖書館館史資料彙編二：1946—1966》 pp.446–449
陳福康《鄭振鐸年譜》 pp.1397–1398
仲偉行等《鐵琴銅劍樓研究文獻集》 pp.263–264
李致忠《中國國家圖書館館史資料長編：1909—2008》 pp.417–418
```

Again, these collection-level records do not yet bind catalog no. 3482/3483 to a specific transaction.

## 3. Target-specific negative controls

### 3.1 Direct 1959 catalog

Batch 12FG directly established:

```text
same catalog uses 瞿捐 on other entries              = true
3482 target entry carries 瞿捐                       = false
3483 target entry carries 瞿捐                       = false
1959 catalog directly attests target Qu donation     = false
```

This is real but bounded negative evidence.

It authorizes only:

```text
TARGET_QU_DONATION_MARK_IN_1959_ENTRY = ABSENT
```

It does **not** authorize:

```text
TARGET_WAS_NOT_DONATED = false / not proved
TARGET_WAS_SOLD        = false / not proved
```

### 3.2 Wang Xiaohu target-volume study

Wang Xiaohu's study identifies the NLC Tonghu and Zhunzhai as the same bound 1823 Huang Pilie/Shiliju manuscript volume carrying Tieqin Tongjian Lou provenance. It further states that the author did not locate these two works in the consulted 《瞿氏藏書捐贈北京圖書館書目》 and therefore left their exact route into NLC for further investigation.

Source:

```text
https://www.sohu.com/a/210477956_488626
```

This is an independent target-specific negative control, but it remains non-exhaustive:

```text
NOT_FOUND_IN_ONE_CONSULTED_DONATION_LIST != PROVED_SALE
NOT_FOUND_IN_ONE_CONSULTED_DONATION_LIST != PROVED_NON_DONATION
```

## 4. Why missing 瞿捐 cannot be converted into a sale verdict

A 2026 bibliographic survey discussion of post-1949 public ancient-book catalogs explicitly distinguishes the two catalog conventions:

```text
Qu-donated items may be marked 瞿捐
Qu books sold to Beijing Library were not marked as sale entries in the 1959 catalog
```

Discovery source:

```text
湯志波、趙穎潔《中國分省公藏古籍書目總錄（1949—2024）》
上海辭書出版社，2026
public discussion:
https://www.haijiaoshi.com/archives/14918
```

Therefore an unmarked target entry is compatible with more than one historical path.

The correct inference is:

```text
MISSING_QU_DONATION_MARK_NARROWS_CATALOG_NOTATION
!=
SALE_SELECTED
```

## 5. Gao Xizeng annotated-catalog lead

The same 2026 bibliographic discussion reports a more important source lead:

> Gao Xizeng, who assisted Zhao Wanli in collecting books from the Qu family, left an annotated copy of 《鐵琴銅劍樓藏書目錄》 containing detailed annotations on books he handled.

12FL treats this only as a **discovery lead**.

The project has not yet directly reviewed that annotated copy, a facsimile, or an authoritative full collation. Therefore:

```text
GAO_ANNOTATED_CATALOG_EXISTENCE_LEAD = IDENTIFIED
DIRECT_PROJECT_REVIEW                = false
CURRENT_HOLDING_OR_SURROGATE         = NOT_CLOSED
TARGET_3482_3483_ANNOTATION          = NOT_REVIEWED
TARGET_TRANSACTION_MODE              = UNRESOLVED
```

This source is now higher priority than further inference from catalog silence.

## 6. Adjudication

```text
QU_TO_BEITU_COLLECTION_LEVEL_TRANSFER_PROGRAM
  = CLOSED_AS_MIXED_DONATION_AND_PRICED_ACQUISITION_OR_SALE

TARGET_VOLUME_QU_PROVENANCE_BEFORE_BEITU
  = CLOSED

TARGET_1959_QU_DONATION_MARK
  = ABSENT_ON_DIRECT_TARGET_ENTRIES

TARGET_SPECIFIC_DONATION_ROUTE_SELECTED
  = false

TARGET_SPECIFIC_SALE_OR_PURCHASE_ROUTE_SELECTED
  = false

TARGET_SPECIFIC_OTHER_TRANSFER_ROUTE_SELECTED
  = false

FINAL_NLC_ACQUISITION_TRANSFER_PATH
  = UNRESOLVED
```

No source-count voting is used. Collection-level history cannot substitute for an item-level transaction record.

## 7. Transmission and product consequence

12FL changes no textual lineage and creates no genealogy topology.

```text
NODES_ADDED=0
EDGES_ADDED=0
SAME_OBJECT_EDGE_AUTHORIZED=false
ACQUISITION_EDGE_AUTHORIZED=false
DIRECT_SANMING_PARENT_VOTE_INCREMENT=0
MATRIX_ROW_COUNT_CHANGE=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Accounting remains:

```text
Matrix rows / audited / missing = 198 / 166 / 10
provenance defects repaired     = 13 / 13
chart algorithm defects         = 0
```

## 8. Next gate

Highest priority:

1. locate and directly inspect Gao Xizeng's annotated 《鐵琴銅劍樓藏書目錄》 or an authoritative reproduction/collation;
2. test the Tonghu/Zhunzhai target entry or bound-volume identity for an item-level sale/donation/handling annotation;
3. inspect the Qu-family transaction material cited in NLC institutional history, especially 《北京圖書館館史資料彙編二：1946—1966》 pp.446–449 and any accession/transfer lists;
4. do not infer sale from the absence of `瞿捐` or from nonlocation in one donation list;
5. keep the 12FK NLC page-count/full-manifest access boundary unchanged;
6. continue pre-1578 Zhunzhai and independent Sanming/Yueling Dahan–Rainwater + Nanjing-59 lines in parallel.

Research record: `docs/research/ZIWEI-QU-NLC-MIXED-TRANSFER-AND-TARGET-ACQUISITION-BOUNDARY-R1.json`.
