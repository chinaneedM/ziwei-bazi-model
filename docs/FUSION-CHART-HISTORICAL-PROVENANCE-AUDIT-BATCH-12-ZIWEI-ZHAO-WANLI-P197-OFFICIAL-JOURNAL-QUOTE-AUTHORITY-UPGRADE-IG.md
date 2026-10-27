# Fusion Chart Historical Provenance Audit R1 — Batch 12IG

## 浙江图书馆官方期刊全文：赵万里 p.197 引文桥权威升级，1951 原刊与 FID070 同物关系继续封锁

Status: **ZHEJIANG LIBRARY OFFICIAL JOURNAL PDF RECOVERED / PDF SHA256 BOUND / DIRECT TEXT LAYER NO OCR / QU DONOR QUOTE BOUND TO PDF PAGE 92 / [2]197 DIRECTLY SEEN / 2026 QUOTATION BRIDGE AUTHORITY UPGRADED / 2011 P197 NOT DIRECTLY REVIEWED / 1951 ORIGINAL NOT DIRECTLY REVIEWED / SONG-PRINT MEMBER NOT COLLAPSED TO FID070 / ZERO PRODUCT CHANGE**

## 1. Why Batch 12IG exists

此前 Batch 12HF / 12HJ / 12HY 已通过公开转载建立赵万里 1951 捐赠段落的引文桥，但该桥的现代承载层仍是公开转载页面。

12IG 将这条桥升级到**浙江图书馆官方《图书馆研究与工作》期刊全文对象**：直接取得 2026 年第4期官方 PDF，并在无需 OCR 的文本层中绑定目标引文所在 PDF 页。

升级的是现代引文承载物的权威级别，不是把 2026 文章改写成 1951 原刊，也不是把参考文献页码视作已直读 2011 原页。

## 2. Official journal object

官方期刊页：`https://bjb.zjlib.cn/CN/Y2026/V0/I4/2`

官方 PDF：`https://bjb.zjlib.cn/CN/PDF/1737`

对象控制：

```text
provider = 浙江图书馆《图书馆研究与工作》编辑部
issue = 2026年第4期
article = 肖玲《赵万里与古籍保护》
article printed start page = 89
PDF pages = 96
PDF bytes = 3023670
PDF SHA-256 = 2e0b9c1d59ccc95523b48144964cb8f528161c3b9201cb28da0cee41de9cd776
OCR used = false
```

整卷下载与页级复核由两个独立 probe 完成。页级 probe run `36601170241` / artifact `11049695243`，artifact digest `sha256:9cf113f42d13607dbf157d09157cabfbf0a9fc128ab311db50e09c23bbd929e7`。

## 3. Direct page-level control

页级 probe 在 **PDF 第92页** 同页闭合以下 token：

- `瞿济苍`；
- `凤起`；
- `旭初`；
- `捐赠`；
- `宋刻`；
- 题名因 PDF 双栏文本顺序被拆为 `春秋左` + `传注疏`；
- `六十二种`；
- 引注 `[2]197`。

因此本批允许写成：浙江图书馆官方期刊 PDF 的直接文本层，确实复现了肖玲对赵万里捐赠段落的引文，并把该段引至参考文献 `[2]` 的第197页。

但本批**不存储整段引文全文作为项目权威正文**；仅保留可复核 token、页码、对象哈希和引用链。

## 4. Citation chain

同一官方 PDF 的参考文献 `[2]` 为：

`冀淑英、张志清、刘波《赵万里文集：第一卷》，国家图书馆出版社，2011`。

所以当前证据链为：

```text
2026 浙江图书馆官方期刊 PDF
    ↓ direct reviewed quotation + [2]197
2011 《赵万里文集：第一卷》 p.197
    ↓ still pending direct page review
赵万里 1951 《〈永乐大典〉展览的意义》
    ↓ still pending direct original-page review
《文物参考资料》1951年第9期 pp.221–233
```

不能把 citation page number 当作 direct page review。

## 5. Object-identity firewall

官方 2026 引文显示捐赠成员为`宋刻《春秋左传注疏》`。而项目当前 FID070 对象经过实物/版本研究后控制为`元刻元印十行本`，此前旧编目曾作`元刻明修本`。

因此：

```text
quoted 宋刻《春秋左传注疏》 == FID070
= NOT PROVED

same-object collapse
= FORBIDDEN

FID070 exact Qu donation batch
= UNRESOLVED

FID070 exact Qu donation date
= UNRESOLVED

3368 -> 3288 causal mechanism
= UNRESOLVED
```

题名相同不能跨版本、跨对象直接合并。

## 6. Relation to prior batches

- 12HJ 的“62 种 + 一个明确成员”引文桥继续有效；
- 12HY 的 FID070 年代/对象同一性防火墙继续有效；
- 12IF 的 Cambridge 1951 原刊馆藏路线继续有效；
- 12IG 只把 12HJ/12HY 使用的现代引文承载层升级为**官方期刊直接全文**。

没有新增历史交易事实，没有改变 62 / 52 / 42 等不同统计层的既有不归一化原则。

## 7. Lawful next route to the original page

1951 原刊目标已经有精确定位：`《文物参考资料》1951年第9期 / 卷2 / pp.221–233`，并已有 NDL 原刊合订卷 `Z8-AC150 / 2(7)-2(12) 1951` 与 Cambridge `FB.252:14 / 卷2i-xii` 等实体路线。

下一步应优先取得**直接页面**，而不是继续堆馆藏数量。NDL 官方远隔复制服务在已知刊名、卷期、篇名或页码时允许注册用户提出有偿复制申请；但具体对象能否在线提交、交付形态及费用必须在登录后确认。本项目目前未登录、未提交、未付费。

任何复制申请属于账户/费用外部动作，未经用户明确授权不执行。

## 8. Project accounting

```text
Matrix rows = 198
audited rows = 166
MISSING_FROM_PRODUCT = 10
provenance defects = 17 / 17 repaired
chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```

本批不改变确定性排盘规则、候选、Matrix 行数、传承图拓扑或 provenance-defect 计数。

Research record: `docs/research/ZIWEI-ZHAO-WANLI-P197-OFFICIAL-JOURNAL-QUOTE-AUTHORITY-UPGRADE-R1.json`.
