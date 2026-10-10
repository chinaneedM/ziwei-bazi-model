# 天问历史考据 12QB — 上海 GJ2312912 连续页图索引

**结论：完成311张连续原页图及27份联络表的可复现采集，仍未完成目标篇章的逐页视觉校勘。** 不得把图像采集等同于已读完311页，更不得声称全书没有〈改造漏刻〉。

## 图像来源与可复核窗口

- GitHub Actions: https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/38042316379（两个分件任务均 success），无OCR。
- 分件2 PDF第350—550页，即原文件全套第900—1100页；201张逐页JPEG、17张联络表；artifact ID 11665913148。
- 分件3 PDF第1—110页，即原文件全套第1101—1210页；110张逐页JPEG、10张联络表；artifact ID 11665464139。
- 原始PDF SHA-256在12QA记录中已经确认；本批重下载时强制哈希相符。每个 artifact 保留 dense-source-page-index.json，逐图附完整 SHA-256和源页码。公开workflow可按同一源复跑。

## 历史判读边界

新取得的图像是影像资源和连续页码证据，尚未逐页确认篇名、版心原叶码及「官漏／宫漏」的实际原字。人工仅查看部分联络表和此前间隔采样单页；图像数量不代表已校读文字的页数。

Commons将这套影像标为上海图书馆来源，原文件名含GJ2312912，但馆藏正式实物ID、版本年代、实物抄成年代仍未一一绑定；其它目录中的「清初抄本」不能按同名或同馆直接合并。

## 工程裁决和下一步

历史审计矩阵222/222；来源元数据缺陷修复45/45；真实排盘算法缺陷0。MD-G03维持OPEN_BLOCKING_GENERAL_ADAPTER，HPA-DAYUN-CAL-002维持MISSING_FROM_PRODUCT；确定性产品仍CLOSED。无谱系新直接边，无运行时改动。

下一步继续从联系表筛选可疑章题页并调阅原尺寸图，确立〈改造漏刻〉原页及「官漏／宫漏」字形，再与1827刊本、旧二十卷抄本做独立校勘。

机器证据：docs/research/MING-DATONG-YEHUOBIAN-12QB-SHLIB-GJ2312912-DENSE-PAGE-INDEX-R1.json
