# Fusion Chart Historical Provenance Audit R1 — Batch 12FN

## 林振岳《序》与高熙曾批校《铁琴铜剑楼藏书目录》：现代证据作者归属修正

Status: **DIRECT MODERN ASSERTION AUTHOR = LIN ZHENYUE / UNDERLYING VOLUME COMPILERS = TANG ZHIBO + ZHAO YINGJIE / REPOST PLATFORM != ORIGINAL AUTHORITY / GAO ANNOTATED-CATALOG EXISTENCE ATTESTATION PRESERVED / CURRENT HOLDING + 3482/3483 ANNOTATION + TARGET TRANSACTION MODE STILL UNRESOLVED / ZERO GENEALOGY OR RUNTIME CHANGE**

## 1. Why this correction is required

Batch 12FL and Batch 12FM used a public repost of the 2026 volume:

```text
汤志波、赵颖洁编
《中国分省公藏古籍书目总录（1949—2024）》
上海辞书出版社，2026
ISBN 9787532664252
```

The underlying historical claim remains usable, but the direct authorship layer had been described too generically as a Tang/Zhao bibliographic-survey discussion.

Direct review of the public text shows a stricter structure:

```text
书名 / 编者：汤志波、赵颖洁
序
林振岳
...
高熙曾先生留有一部批校本《铁琴铜剑楼藏书目录》...
...
二〇二五年十月三十日
于东京大学东洋文化研究所
```

Therefore the target sentence belongs to **Lin Zhenyue's signed preface**, not to a separately signed passage by the volume compilers.

Public control:

```text
https://www.sohu.com/a/1011488146_121124384
```

## 2. Canonical source-layer model

12FN separates three layers that must not be collapsed:

```text
UNDERLYING_VOLUME
  compilers = 汤志波、赵颖洁

SIGNED_PREFACE
  author = 林振岳
  dated = 2025-10-30
  place = 东京大学东洋文化研究所

PUBLIC_REPOST
  carrier = 搜狐 / 海交史等公开转载
```

The statement used by this project — Qu collection transfer catalog semantics and Gao Xizeng's annotated Tieqin catalog — is directly authored at the **SIGNED_PREFACE** layer.

## 3. Author identity and research-fit control

Shanghai Jiao Tong University's official faculty page identifies Lin Zhenyue as a scholar in:

- Chinese classical bibliography;
- editions and catalog studies;
- book history;
- modern-person studies;
- Ming-Qing catalogs and collection history.

Official profile:

```text
https://shss.sjtu.edu.cn/Web/FacultyDetail/265
```

This does not make the statement self-proving. It closes only the modern author identity and supplies a legitimate scholarly discovery route for the statement's underlying source basis.

## 4. Repository repair

The prior registry source id:

```text
EXT-TANG-ZHAO-2026-QU-TRANSFER-CATALOG-SEMANTICS-GAO-ANNOTATED-CATALOG-LEAD
```

is retained as a historical attribution alias, but is now deprecated for direct authorship.

Canonical source:

```text
EXT-LIN-ZHENYUE-2025-PREFACE-QU-TRANSFER-GAO-ANNOTATED-CATALOG
```

Batch 12FL and Batch 12FM machine evidence are repaired to preserve:

```text
direct statement author = 林振岳
underlying volume compilers = 汤志波 / 赵颖洁
repost platform = carrier only
```

No historical-object conclusion is withdrawn.

## 5. What remains closed and what remains open

Still closed:

```text
GAO_ANNOTATED_TIEQIN_CATALOG_EXISTENCE
  = ATTESTED_BY_LIN_ZHENYUE_PREFACE

QU_TO_BEITU_COLLECTION_LEVEL_MIXED_TRANSFER
  = unchanged from Batch 12FL
```

Still open:

```text
GAO_ANNOTATED_CATALOG_CURRENT_HOLDING = UNRESOLVED
GAO_ANNOTATED_CATALOG_SHELFMARK       = UNRESOLVED
GAO_ANNOTATED_CATALOG_PUBLIC_SURROGATE= UNRESOLVED
TARGET_3482_3483_ANNOTATION           = NOT_REVIEWED
TARGET_TRANSACTION_MODE               = UNRESOLVED
```

12FN therefore changes the **provenance of the modern claim**, not the provenance of the 1823 bound volume.

## 6. Search boundary after authorship correction

Targeted searches for combinations of:

- 林振岳 + 高熙曾;
- 林振岳 + 铁琴铜剑楼;
- 林振岳 + 瞿氏藏书;
- 高熙曾 + 批校目录;

did not expose a second public source naming Lin's underlying evidence, current holder, shelfmark, or a target 3482/3483 annotation.

This is a bounded web-search result only:

```text
NO_SECOND_PUBLIC_SOURCE_LOCATED
!=
NO_SOURCE_EXISTS
!=
PRIVATE_SOURCE
!=
LOST
```

## 7. Product / genealogy consequence

```text
NODES_ADDED=0
EDGES_ADDED=0
ACQUISITION_EDGE_AUTHORIZED=false
SAME_OBJECT_EDGE_AUTHORIZED=false
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

The 12FN repair is repository evidence-source metadata normalization and does not increment the product/historical-row provenance-defect counter.

## 8. Highest next gate

1. Recover Lin Zhenyue's source basis for the Gao annotated-catalog statement: citation, personally inspected copy, colleague-owned material, unpublished catalog record, or archival reference.
2. Treat Tang Zhibo and Zhao Yingjie as the underlying-volume compilers unless a separate signed statement by them is recovered.
3. Keep Qin Junze 2020, Zhao Lintao, Gao-family manuscripts, and NLC historical work papers as secondary discovery routes.
4. Do not select current custody or target donation/sale route without direct or near-direct evidence.

Research record: `docs/research/ZIWEI-LIN-ZHENYUE-PREFACE-GAO-ANNOTATED-CATALOG-SOURCE-ATTRIBUTION-R1.json`.
