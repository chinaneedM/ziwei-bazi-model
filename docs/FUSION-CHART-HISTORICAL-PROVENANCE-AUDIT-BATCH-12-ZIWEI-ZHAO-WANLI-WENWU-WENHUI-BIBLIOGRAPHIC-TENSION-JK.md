# Fusion Chart Historical Provenance Audit R1 — Batch 12JK

## 国图官方综述《文物参考资料》书目控制与 1951-08-18 上海《文汇报》线索张力

Status: **NLC OFFICIAL PDF CLOSED / WENWU 1951 NO.9 PP.221–233 BIBLIOGRAPHIC BUNDLE CLOSED / WENHUI OMISSION NON-NEGATIVE / AUG-18 WENHUI LEAD UNVERIFIED / FIRST PUBLICATION UNRESOLVED / TRANSMISSION RELATION UNRESOLVED / ZERO PRODUCT IMPACT**

### 1. 目标

12JJ 已关闭上海社科院 1951 整年上海《文汇报》实体馆藏路线，但 1951-08-18 刊载说仍只是二手线索。

12JK 检查国家图书馆官网公开的刘鹏《清末以来（1908—2021）〈永乐大典〉研究综述》PDF，确定它对赵万里该文的现代机构书目著录能关闭到什么程度，以及它是否足以否定《文汇报》线索。

### 2. 官方 PDF

对象：

```text
https://www.nlc.cn/upload/attachments/2025-04-08/753b026e.pdf
```

控制性探针取得：

- HTTP 200 / application/pdf
- 755,701 bytes
- 17 pages
- SHA-256 `08bf6adcf9a2d200128a80b26156f9de06731094426a116c44ae02386822af20`
- text layer 可直接提取
- OCR_USED=false

### 3. PDF 第5页 / 印刷页10

无 OCR 文本层直接闭合：

- 赵万里；
- 《永乐大典展览的意义》；
- 副题“一九五一年八月北京图书馆举办”；
- 《文物参考资料》；
- 1951年第9期；
- 第221—233页。

因此：

```text
WENWU_1951_NO9_PP221_233
= CLOSED_AT_OFFICIAL_MODERN_SCHOLARLY_BIBLIOGRAPHIC_LEVEL
```

但它仍不是 1951 原期正文；pp.221–233 继续 NOT_REVIEWED。

### 4. 与《文汇报》线索的张力

该综述目标页没有“文汇报”，也没有“8月18日”。

这只能说明**这份现代综述在列举代表作时选择了《文物参考资料》这一载体**，不能证明 1951-08-18 上海《文汇报》没有先刊、摘载或另版。

所以禁止：

```text
NLC review omits Wenhui
=> Wenhui publication impossible
```

同样禁止：

```text
secondary chronology says Wenhui 8/18
=> Wenwu must be a reprint
```

### 5. 控制性探针

- workflow: `.github/workflows/probe-batch-12jk-nlc-review-wenwu-wenhui-bibliographic-tension.yml`
- exact probe head: `a57d0cba8916d3c79ad66ea28705e9572778cfaf`
- run: `36829969296`
- job: `110264093618`
- artifact: `11147240797`
- artifact digest: `sha256:4c19f7cff9fdec4c2e24b8fef12578345ba8c195cc3594810924311a2a215c60`

### 6. 当前裁决

```text
Wenwu issue-9 carrier
  = HIGH_CONFIDENCE_MODERN_INSTITUTIONAL_BIBLIOGRAPHIC_CONTROL

Direct Wenwu pp.221-233
  = NOT_REVIEWED

Shanghai Wenhui 1951-08-18
  = SECONDARY_LEAD_UNVERIFIED_BY_PRIMARY_PAGE

Direct Wenhui 1951-08-18
  = NOT_REVIEWED

FIRST_PUBLICATION_STATUS
  = UNRESOLVED

WENHUI_TO_WENWU_RELATIONSHIP
  = UNRESOLVED
```

### 7. 传承影响

本批次不添加强制传播边，只新增未决问题：

- 8月18日《文汇报》是否确有该文；
- 若两载体均存在，是全文重刊、节本、修订稿还是同题异文；
- 哪一个是首刊。

`TRANSMISSION_IMPACT=UNRESOLVED_QUESTION_ONLY`。Transmission Graph 暂不修改，避免把尚未审读的两个对象强连成直接传播关系。

### 8. 项目影响

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；chart algorithm defects 0；algorithm reopen 0；candidate collapse 0。无 runtime 或产品变化。

### 9. 下一门

现在最有信息增益的动作不是继续找现代转述，而是取得两个原始对象之一：

1. 上海《文汇报》1951-08-18 原页；
2. 《文物参考资料》1951年第9期 pp.221–233。

任一直接文本出现后，即可开始全文/段落级校勘，并判断是否存在先刊—重刊或改写关系。2011《赵万里文集》第1卷 p.197 仍保持并行最高门。

Research record: `docs/research/ZIWEI-ZHAO-WANLI-WENWU-WENHUI-BIBLIOGRAPHIC-TENSION-R1.json`.
