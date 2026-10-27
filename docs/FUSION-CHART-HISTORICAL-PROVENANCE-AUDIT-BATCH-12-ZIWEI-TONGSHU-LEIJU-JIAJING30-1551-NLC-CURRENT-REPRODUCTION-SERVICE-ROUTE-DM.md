# Batch 12DM — NLC 1551《通書類聚尅擇大全》現行合法複製/替代介質服務路線

## Status

```text
BATCH_ID=BATCH-12-ZIWEI-TONGSHU-LEIJU-JIAJING30-1551-NLC-CURRENT-REPRODUCTION-SERVICE-ROUTE-DM
TARGET_CALL_NO=14202
REQUEST_SUBMITTED=false
PROVIDER_ACCEPTANCE=false
DIRECT_PAGE_OBTAINED=false
NUMERIC_ANCESTRY_VOTE=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 1. Purpose

12DL 已把第一次複製目標收窄到**卷十六末刊記 + 卷16–19目標表頁**。12DM 不再重複公開索引搜索，而是回答：目前國圖有哪些一手、合法、可操作的獲取渠道？

## 2. Current first-party service routes

### A. 善本特藏閱覽室

國圖當前館區服務頁列明：

- 善本特藏文獻：閉架閱覽與諮詢；
- 若已有縮微、數字資源或影印本，原則上不提供原件；
- 現行服務點：總館南區二層 G220；
- 現行頁面列電話：010-88545344。

這使「先問替代介質，再碰原件」成為本項目的首選順序。

### B. 文獻提供中心

國圖一手服務頁明列可提供：

```text
檢索 / 復印 / 膠片還原 / 掃描 / 拍照 / 刻錄 / 打印 / 裝訂
```

並公開：

- 網上系統；
- E-MAIL；
- 電話；
- 傳真；
- 到館委託。

現行公開聯繫控制：

```text
TEL 010-88545533
E-MAIL wxtgzx@nlc.cn
```

但這只是一般服務能力；**不等於**館方已同意複製善本 `14202`。

### C. 全國圖書館文獻縮微複製中心

國圖縮微中心當前頁面明確說明，其文獻諮詢/提供長期面向包括普通讀者，提供縮微、數字和紙本文獻；亦有縮微膠片數字化還原能力。

這條路尤其重要，因為 12DK 的 B1MICU 只證明了「外部微縮聯合目錄匿名檢索受阻」，**沒有證明國圖本身不存在膠卷**。

## 3. Request payload frozen for future authorized submission

```text
書名：通書類聚尅擇大全
版本：明嘉靖三十年（1551）芝城活字印本
索書號：14202
普查編號：110000-0101-0013797
OPAC doc：001790345
OPAC internal id：411999023866
存卷：十六至十九
```

第一批請求順序：

1. 卷十六末刊記頁，盡量帶前後各 1–2 葉；
2. 卷16–19各卷卷首、目錄、篇題頁；
3. 優先定位「晝夜百刻 / 四時節氣 / 日出入 / 漏刻 / 銅壺」相關欄目；
4. 若命中數表，要求包含大寒、雨水、夏至的完整頁及相鄰頁。

同時向館方明問：

- 是否已有縮微膠卷、數字影像、影印本；
- 若有，優先提供替代介質；
- 若無，善本閱覽/複製需要何種證件、介紹信、申請與費用；
- 能否先由館員定位卷十六末刊記與目標欄目葉碼。

## 4. Authorization boundary

本批次**沒有**替任何人提交申請，也沒有使用任何個人身份、讀者卡或支付資料。

```text
REQUEST_SUBMITTED=false
ACCEPTANCE_OBTAINED=false
PRICE_QUOTE=false
MICROFILM_FOR_TARGET_CONFIRMED=false
DIRECT_PAGE_OBTAINED=false
```

真正提交屬於外部服務交互，可能需要身份、登入、館方審批或付款；只有在取得相應授權後才能執行。

## 5. Genealogy and product firewalls

本批次只改「如何取得證據」，不改「證據內容」：

```text
TEXTUAL_VOTE_INCREMENT=0
NUMERIC_VOTE_INCREMENT=0
1551_TONGSHU_LEIJU -> SANMING_1578 DIRECT_TARGET_FINGERPRINT = UNRESOLVED
1551_TONGSHU_LEIJU -> YUELING_1589 DIRECT_TARGET_FINGERPRINT = UNRESOLVED
HPA_ZDATE_006=MISSING_FROM_PRODUCT
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
```

## 6. Parallel next gate

外部申請尚未提交/等待期間，研究不中斷：

1. pre-1578 exact-fingerprint Tongshu/almanac carrier；
2. Chinese Nanjing/Datong 59/41 physical carrier；
3. exact whole-ke threshold/selection rule。

Research record: `docs/research/ZIWEI-TONGSHU-LEIJU-JIAJING30-1551-NLC-CURRENT-REPRODUCTION-SERVICE-ROUTE-R1.json`.
