# Fusion Chart Historical Provenance Audit R1 — Batch 12JD

## 郑振铎《关于〈永乐大典〉》1951-08-13 / 1951-08-31 出版日期冲突

Status: NLC 2019 OFFICIAL REPRINT REPORTS 1951-08-13 / NLC 2025 OFFICIAL PDF REPORTS 1951-08-31 / PUBLIC DAILY TRANSCRIPTION PLACES TARGET ARTICLE ON 1951-08-13 PAGE 3 / SOURCE-EMITTED 1951-08-31 DAILY PAGE DOES NOT CONTAIN TARGET TITLE OR ZHENG / 1951-08-13 ADOPTED AS HIGH-CONFIDENCE CONTROLLING DATE / 1951-08-31 QUARANTINED PENDING OFFICIAL NEWSPAPER SCAN / ZERO PRODUCT OR MATRIX CHANGE

### 1. Why this batch exists

国家图书馆 2025 年《清末以来（1908—2021）〈永乐大典〉研究综述》是项目现有赵万里 1951 目标篇的重要第一方书目定位来源。该 PDF 同时把郑振铎《关于永乐大典》记为 1951年8月31日《人民日报》。

国家图书馆中国古籍保护网 2019 年公开全文转载同文时，则明确标为 1951-08-13，并注明转载自《人民日报》。12JD 专门裁决这个日期冲突，禁止静默归一化。

### 2. Reproducible probe

Probe workflow: .github/workflows/probe-batch-12jd-zheng-yongle-date-conflict.yml

- exact probe head: e254e3b30eeaa0eed352055dee2c8bb67dbd69e4
- workflow run: 36759879758
- artifact: 11118018737
- artifact digest: sha256:27cbf81f6a2a68128afa7f7bb935532085d85f16c846cbea0d3edbed6fc4ac7d

Probe 仅匿名 GET，并解析 NLC 官方 PDF 自带文本层。没有 OCR、登录、付款、猜测 8月31日 URL 或绕过访问控制。

### 3. NLC 2019 official reprint

URL: https://www.nlc.cn/pcab/zx/xw/20190815_180607.shtml

直接观察到：题名“郑振铎：关于《永乐大典》”、转载自《人民日报》、日期 1951-08-13，以及苏联列宁格勒大学归还十一册、商务印书馆捐赠二十一册等正文控制点。

### 4. NLC 2025 official PDF conflict

URL: https://www.nlc.cn/upload/attachments/2025-04-08/753b026e.pdf

- bytes: 755701
- SHA-256: 08bf6adcf9a2d200128a80b26156f9de06731094426a116c44ae02386822af20
- OCR used: false
- PDF 文本层直接显示：郑振铎《关于永乐大典》，1951年8月31日《人民日报》。
- 同一 PDF 继续正确提供赵万里目标篇《文物参考资料》1951年第9期、第221—233页的书目定位。

因此 8/31 是真实存在于 NLC 2025 正文中的冲突值，不是搜索引擎摘要错误。

### 5. Public daily-transcription control

逐日报纸公开转录不是《人民日报》官方原版影像，只作为独立对照。探针从 1951-08-13 页面自身发出的“当月目录”继续到目录自身发出的 1951-08-31 页面，没有合成或猜测 8/31 URL。

1951-08-13 页面：目标题名存在；第3版存在；展览编辑按说明写明八月十三日举行；正文中的苏联十一册和商务二十一册控制点均存在。

1951-08-31 页面：日期身份存在；目标题名不存在；郑振铎字样不存在；展览说明字样不存在。

### 6. Adjudication

当前项目控制：郑振铎《关于〈永乐大典〉》的控制出版日期为 1951-08-13，置信度 HIGH。NLC 2025 的 1951-08-31 保留为 BIBLIOGRAPHIC_DATE_CONFLICT_QUARANTINED_PENDING_OFFICIAL_NEWSPAPER_SCAN。

这不是宣称 8/31 在物理报纸上绝对不可能存在。最终影像级裁决仍需权威/原始《人民日报》1951-08-13 与 1951-08-31 页面。

### 7. Scope firewall

12JD 不证明郑振铎文章与赵万里《〈永乐大典〉展览的意义》为同文，也不允许以郑文替代赵文直接页。

- 2011《赵万里文集》第1卷 p.197：NOT_REVIEWED
- 1951《文物参考资料》第9期 pp.221–233：NOT_REVIEWED
- 1997《北京图书馆馆史资料汇编（二）》pp.446–449：NOT_REVIEWED

### 8. Project consequence

- Matrix: 198 rows / 166 audited
- MISSING_FROM_PRODUCT: 10
- existing confirmed project provenance metadata defects: 17 / 17 repaired
- new provenance-defect count change: 0
- chart algorithm defects: 0
- algorithm reopen: 0
- candidate collapse: 0
- transmission graph change: none
- runtime/product change: none

### 9. Next gate

1. 继续直接合法恢复 2011《赵万里文集》第1卷 p.197。
2. 继续恢复 1951《文物参考资料》第9期 pp.221–233。
3. 继续恢复 1997《北京图书馆馆史资料汇编（二）》pp.446–449。
4. 若权威/原始《人民日报》影像公开，再进行 8/13 与 8/31 最终影像级裁决。

Research record: docs/research/ZIWEI-ZHENG-YONGLE-1951-0813-0831-PUBLICATION-DATE-CONFLICT-R1.json.
