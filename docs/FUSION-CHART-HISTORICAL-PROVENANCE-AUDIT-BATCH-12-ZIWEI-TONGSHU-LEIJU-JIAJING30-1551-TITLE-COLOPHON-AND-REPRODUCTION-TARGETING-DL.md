# Batch 12DL — 嘉靖三十年（1551）《通書類聚尅擇大全》題署、卷十六刊記定位與複製目標收窄

## Status

```text
BATCH_ID=BATCH-12-ZIWEI-TONGSHU-LEIJU-JIAJING30-1551-TITLE-COLOPHON-AND-REPRODUCTION-TARGETING-DL
PRIOR_BATCH=...-DK
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
HPA_ZDATE_006=MISSING_FROM_PRODUCT
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
```

## 1. Why this follows 12DK

12DK 已把公開 OPAC、數字古籍索引、Commons/IA、匿名 B1MICU 與 576 條聯合書目路線收口，但仍沒有取得 NLC 索書號 `14202` 的卷十六至十九頁圖。

本批次只處理兩個問題：

1. 是否能把「整冊盲查」收窄成可向館方提出的精確複製目標；
2. 新檢出的相同數表是否真是獨立來源，而非後世轉抄。

## 2. 2025《圖書館雜誌》版本學定位

《圖書館雜誌》官方文章頁直接確認：

- 沈凱文：〈國家圖書館藏明活字本《墨子》考論〉；
- 2025 年，第 44 卷（總 409 期），136–144；
- 正式文章頁與出版社 PDF 路線均存在。

出版社 PDF 在當前研究環境中以 `application/octet-stream` 返回，無法作 PDF 頁面截圖。因此本批次**不把搜索索引中暴露的正文片段冒充直接 PDF/實物目驗**。

搜索索引中的出版社正文片段提供兩個高價值的**二級定位控制**：

- 1551《通書類聚尅擇大全》題署把姚奎記為纂輯、王以寧記為校刊；
- 注釋把「嘉靖三十年芝城活字印行」刊記精確定位到**卷十六末**，並引張秀民《中國印刷史》（2006：569）。

這一層的權限只到「複製請求定位」，不能替代 1551 實物頁。

## 3. Why juan 16 matters operationally

12DJ/12DK 已經以國家圖書館一手書目綁定現存範圍：

```text
CALL_NO=14202
SURVIVING_SCOPE=卷十六至十九
```

而本批次二級版本學定位把刊記落在：

```text
卷十六末
```

因此第一次合法複製/閱覽請求不再需要泛稱「請查卷16–19」，而可以優先要求：

1. 卷十六末若干葉，核驗刊記、版式與實物身份；
2. 卷十六至十九目錄/篇題中與晝夜百刻、四時節氣、日出入、漏刻/銅壺相近的葉；
3. 若命中表格，直接核驗 `大寒 43/57 -> 十三後 44/56`、`雨水 47/53 -> 後四日 48/52` 與 `夏至 59/41`。

這只是提高複製命中率；本批次仍然：

```text
DIRECT_1551_PAGE_OBTAINED=false
TARGET_TABLE_PAGE_OBTAINED=false
EXACT_FINGERPRINT_TESTED_ON_1551_COPY=false
```

## 4. Printing-shop inference firewall

沈文認為 1551《通書類聚》與 1552 芝城活字《墨子》的字體、版式支持同一副活字/同一書坊來源。

天問只把這一點記為：

```text
PRINTING_PROVENANCE=SCHOLARLY_INFERENCE
SAME_PRINTING_SHOP != SAME_TEXTUAL_LINEAGE
SAME_PRINTING_SHOP != SAME_TABLE_LINEAGE
NUMERIC_ANCESTRY_VOTE=0
```

不得把印刷工藝同源偷換成術數數表傳承同源。

## 5. 《古今圖書集成》同數表不是新一票

新檢出的《欽定古今圖書集成·藝術典》卷597 公開轉錄確實顯示同一高信息量數字：

- 大寒 43/57，後十三日 44/56；
- 雨水 47/53，後四日 48/52。

但同一頁面在卷目與正文入口明確標成：

```text
星命部彙考三十三
三命通會五
```

因此它是後世類書在《三命通會》名下收錄該材料，不能作為：

- 獨立的 pre-1578 來源；
- 第二個實物數表見證；
- Sanming/Yueling 共同祖本的新增票數。

```text
INDEPENDENT_FINGERPRINT_WITNESS_INCREMENT=0
```

## 6. Genealogy consequence

本批次只加強既有節點：

```text
PHYSICAL-COPY-TONGSHU-LEIJU-NLC-JIAJING30-1551-V16-19
```

不新增正向傳承邊，不改變兩條既有未決防火牆：

```text
1551_TONGSHU_LEIJU DIRECT_TARGET_FINGERPRINT_ATTESTATION SANMING_1578 = UNRESOLVED
1551_TONGSHU_LEIJU DIRECT_TARGET_FINGERPRINT_ATTESTATION YUELING_1589 = UNRESOLVED
```

對 `TG-H0001` 的影響僅為：複製目標更精確，且一條後世假獨立見證已去重；**zero textual/numeric vote**。

## 7. Product adjudication

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
HPA_ZDATE_006=MISSING_FROM_PRODUCT
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=12
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=12
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 8. Next gate

1. 向 NLC 南區善本閱覽室/複製服務以 `14202` 為唯一實物標識，第一批優先請求**卷十六末**及相鄰葉；
2. 同批要求卷16–19中晝夜百刻/四時節氣/日出入/漏刻或銅壺相關目錄與目標葉；
3. 在未取得實物頁前，不把姚奎/王以寧題署、卷十六刊記或同書坊推論升格為物理頁權威；
4. 並行繼續 exact-fingerprint pre-1578 Tongshu、Nanjing/Datong 59/41 carrier、whole-ke threshold/selection-rule 三條搜索。

Research record: `docs/research/ZIWEI-TONGSHU-LEIJU-JIAJING30-1551-TITLE-COLOPHON-AND-REPRODUCTION-TARGETING-R1.json`.
