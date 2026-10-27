# Fusion Chart Historical Provenance Audit R1 — Batch 12HX

## FID070 第二条 17 字正文行 + GB/T 行款语义：PROV-DEFECT-016 闭合

Status: **TWO DIRECT PHYSICAL 17-CHAR FULL MAIN-TEXT LINES / GB/T FULL-LINE SEMANTICS CLOSED / CURRENT NLC RAW 16 PRESERVED BUT ADJUDICATED AS METADATA DEFECT / PROV-DEFECT-016 REPAIRED FORWARD-ONLY / ZERO CHART-ALGORITHM CHANGE**

## 1. Second independent physical sample

FID070 第1册 PDF p16 右叶一整列正文大字直接读作：

策書成文考其真偽而志其典禮上以遵周

逐字计数为 17。该列为正文大字，不含双行注文，不使用 OCR。

与 Batch 12HW 的 p12 样本“周禮有史官掌邦國四方之事達四方之志”相互独立；两条位于不同 PDF 页，均为 17 个正文大字。

## 2. Cataloging semantics

GB/T 3792.7—2008《古籍著录规则》8.7.1.4(b) 明确规定：每半叶行数按满半叶行数计算；每行字数按满行字数计算。

该标准说明其主要用于汉语文古籍著录、适用于国家书目及各类型目录，主要起草单位包括中国国家图书馆。

因此“行十六字/行十七字”的裁决对象不是平均值或随意抽样值，而是满行字数。

## 3. Defect closure

现行国图原始元数据仍保留为：10行16字，小字雙行23字，白口，左右雙邊。

但同一 FID070 实物已经在两个不同页位直接出现完整 17 字正文行；铁琴历史目录、1987 北图目录、2017 上海古籍影印出版说明也一致记 17/23。

在 GB/T 满行计数字段语义下，现行 16 字值与直接实物证据冲突。因此登记 PROV-DEFECT-016：CURRENT_PROVIDER_FORMAT_NOTE_MAIN_TEXT_FULL_LINE_CHARACTER_COUNT_ERROR。

修复采用 forward-only：不篡改供应方原始值，而在项目考据层将该实物的正文满行值裁决为 17；小字双行 23 保持不变。

## 4. Product boundary

本缺陷属于历史来源/目录元数据，不属于排盘算法缺陷。紫微/八字确定性排盘 R1 保持 CLOSED；算法重开、候选折叠、运行时规则变化均为 0。

## 5. Accounting

Matrix rows 198；audited rows 166；MISSING_FROM_PRODUCT 10；provenance defects 16/16 repaired；chart algorithm defects 0；algorithm reopen 0；candidate collapse 0。

## 6. Next gate

1. 继续追 1959 书号 3368 → 1987 书号 3288 的对象级卡片/修订单/编目准备记录。
2. 解决 FID070 瞿氏捐赠/入藏的精确批次与日期。
3. 继续取得张丽娟 2018 全文。
4. 继续闭合 2017 上海古籍影印本的具体底本身份。
