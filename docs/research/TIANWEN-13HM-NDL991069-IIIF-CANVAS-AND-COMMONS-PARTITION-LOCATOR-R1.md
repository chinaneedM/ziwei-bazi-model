# 天問 13HM — NDL991069 的第一方 IIIF 與四份高分辨率 Commons 分件對照

本批把已由 13CO 知道的 **1909 年《高麗史》第2冊** 從單純書目線索轉為**可執行的來源原圖取證路線**，但仍未宣稱讀到卷52的 D14/D16 原字。

日本國立國會圖書館 [原生第2冊書目](https://ndlsearch.ndl.go.jp/books/R100000039-I991069) 明確載 ISBN 以外的固定識別 PID `991069`、JPNO `50001638`、刊行年 1909、志卷47–87（含作品卷52）、公開範圍 `インターネット公開`、影像格式 `image/jp2`，並**在來源頁直接發出** IIIF manifest：`https://dl.ndl.go.jp/api/iiif/991069/manifest.json`。因而不需猜測非公開 item token。

Commons [《高麗史》分類索引](https://commons.wikimedia.org/wiki/Category:%E9%AB%98%E9%BA%97%E5%8F%B2) 確實列出同 PID 的四份高分辨率 PDF：`NDL991069 高麗史 第2 part1–4`，分別 **100、100、100、95 數字頁**，總共 **395** 個數字頁，標稱解析度 **5893 × 4597**。這是**同一 NDL 數字物件的分段副本**，不是四個古籍實物或四票歷史數字。

區分：
- **已成立：** 官方 PID、書目涵蓋卷52、公開 IIIF manifest URL、四份 Commons 分段公開目錄和分段頁數。
- **仍未成立：** manifest 本次成功取回、目錄頁/第52卷真實 canvas 索引、與 D14/D16 的圖像像素及 SHA、1909 NDL 本與中國國圖 `NLC416` 同印/異印關係、臺灣 NCL03130 旧钞/補钞卷52層次、任何新數值字形投票。
- **傳承分層：** 1909 日本近代重印只能作 received printed witness；不得當1451古本、不得改寫 Waseda/NAJ 早期校讀，也不得把其讀法代填 NCL03130 原葉。

為此新增 `scripts/probe-tianwen-13hm-ndl991069-iiif.py` 和 GitHub Actions，可只取第一方 source-emitted manifest、記錄 SHA256、canvas 數及可能由目錄標籤明示的卷52位置。沒有可核實的目錄標籤即保留 UNKNOWN，**不得猜測頁次或用 OCR-only 直接裁決**。每次 Actions 的回應作為可重複的 artifact；HTTP 阻擋亦只記訪問邊界，不是不存在原圖。

本批矩陣 222/222、source 761、譜圖 252/238、OPEN 11、chart CLOSED；0 算法重開/候選坍縮。後續直接從 exact-HEAD 13HM artifact 查核原圖 canvas，不再重複泛搜 NDL 書名。機器記錄：`docs/research/TIANWEN-13HM-NDL991069-IIIF-CANVAS-AND-COMMONS-PARTITION-LOCATOR-R1.json`。
