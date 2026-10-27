# Batch 12DG — 《續修四庫全書》1061–1062冊《陰陽寶鑒》前五後五再現與卷界閉合

## Status

```text
SOURCE=續修四庫全書第1061-1062冊
TARGET_WORK=新刊陰陽寶鑒克擇通書前集五卷後集五卷
FRONT_VOLUME5_DIRECTLY_BOUND=YES_AT_XUXIU_REPRODUCTION_SCOPE
BACK_COLLECTION_BOUNDARY_DIRECTLY_BOUND=YES
NEXT_WORK_START=1062_P210_類編曆法通書大全序
SANMING_YUELING_TARGET_CANDIDATE=NOT_OBSERVED_AT_STRUCTURAL_LOCATOR_SCOPE
SAME_PHYSICAL_COPY_AS_BATCH12DF=UNPROVED
EXACT_EDITION_DATE=UNRESOLVED_XUXIU_YUAN_LABEL_VS_CURRENT_UNION_CATALOG_EARLY_MING
WHOLE_WORK_TEXTUAL_NEGATIVE=FORBIDDEN
HPA_ZDATE_006=MISSING_FROM_PRODUCT
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NO
```

Batch 12DF 的剩余高价值门不是再次扫描其已公开的卷1–4，而是找到缺失卷五或完整异本。本批沿着状态文件之后已经提交到远端的三条《續修四庫全書》探测 workflow 完成该门的直接审查。

## 1. Source and acquisition chain

本批使用《續修四庫全書》第1061、1062冊公开 PDF。两册在本次所有 workflow 中字节哈希稳定一致：

- 1061: `618a31924e05cbb8e8c5b49bfc0da2d7c7fb64526c6719175d685088cef29d83`，846页；
- 1062: `f601dcab3bec1ac5cb958790c404c0e5a2ac3f3d6e2b6464352096fce48024e6`，687页。

机器取证链：

- complete locator: run `35354199385` / artifact `10551495381`；
- anchored target range: run `35354510398` / artifact `10551870858`；
- 320-dpi boundary lock: run `35355620739` / artifact `10551353927`。

文本层仅作 locator，最终卷名、边界和字形结论均来自直接图像核读，不使用 OCR 代替原页。

## 2. Front volume 5 is directly recovered

1061 PDF p800（SHA-256 `a2647361c71fc54a3ff021c664c14baa88dba25be3a9b8b9eef738516a1f078c`）左栏直接可读：

> 新刊陰陽寶鑒尅擇通書　前集卷五

因此 12DF 所称“当前独立数字对象缺卷五”不能再被外推为“此书卷五不可见”。更精确的结论是：

```text
BATCH12DF_STANDALONE_OBJECT_VOLUME5=MISSING
XUXIU_REPRODUCTION_FRONT_VOLUME5=RECOVERED
SAME_PHYSICAL_COPY=UNPROVED
```

1061 p810、p820、p825 继续处于前集卷五内容面；p830–p831 已明显残损，因此残损区域不承担任何内容缺失的否定证明。

## 3. Back collection and work boundary

1062 的高分辨率页把后集卷序与书末边界直接锁住：

| PDF page | SHA-256 | direct reading / role |
| --- | --- | --- |
| p66 | `7c5ca76e4bf90797d72ac88e6c7bc9a3b09a0d06ebb0469727bfdbd4ad6386e7` | 后集卷二 |
| p119 | `057e3ca838bd4f0240780633b49342a3d704c1cf9f153f932de730075529bec9` | 卷之三 title leaf |
| p167 | `c14589dd55f5584a4d680b8942cfd0c0bc1e8aca53eb4943c40962b07c490dc0` | 卷之四 title leaf |
| p208 | `0a052c82ed6123a4bdb86be76d7c014dd3cc15dd786c3052aae8df6251c4292d` | 后集卷五 |
| p209 | `ce4d396a72f7a676c1a36b6ce3a2e6e3b493202feb5ac2dd59c58f6b0cb0dc65` | blank separator |
| p210 | `9557e9eab3683360695b8f8a35a2a53926340c7078ec4b799b7b052bdbe4557d` | 《類編曆法通書大全序》 begins |

这使《陰陽寶鑒》在 1062 中的末界不再依赖目录推断：p208 仍是后集卷五，p209 分隔，p210 已进入下一部书。

## 4. Target-fingerprint structural review

直接审查了目标承载区的连续 contact sheets（1061 p721–846；1062 p1–240），并用 320-dpi 页锁定卷界。目标仍然是寻找与 1578《三命通會》/1589《月令通攷》同类的：

- 二十四节气/日期段 + 昼夜刻数表；
- 百刻制季节性整数阶梯；
- `大寒 43/57 -> 十三後 -> 44/56`；
- `雨水 47/53 -> 後四日 -> 48/52`。

结果：

```text
CANDIDATE_SOLAR_TERM_DAYNIGHT_TABLE_LEAF=NOT_OBSERVED
CANDIDATE_HUNDRED_KE_TARGET_LEAF=NOT_OBSERVED
CANDIDATE_SANMING_YUELING_FINGERPRINT_LEAF=NOT_OBSERVED
NEGATIVE_AUTHORITY=STRUCTURAL_LOCATOR_ONLY
WHOLE_WORK_TEXTUAL_ABSENCE=NOT_PROVED
```

这比 12DF 强，因为“缺卷五”本身在《續修四庫》再现范围内已经闭合；但仍不能把低/中分辨率结构审查升级成逐字全文否定，尤其不能让残损页承担负证据。

## 5. Date and copy-identity firewall

当前存在两套不应静默合并的目录性描述：

- 《續修四庫》探测链记录该收录对象为“國家圖書館藏元刻本”；
- 12DF 当前联合目录对象著录为“明初（1368～1424）刻本”。

本批不以相同书名、同一馆藏机构名称或现代再现位置推断二者必为同一物理本，也不裁定“元刻本”与“明初刻本”哪一项最终正确。

```text
SAME_PHYSICAL_COPY_AS_DF_OBJECT=UNPROVED
SAME_RECENSION_AS_DF_OBJECT=UNPROVED
EXACT_UNDERLYING_IMPRESSION_DATE=UNRESOLVED
```

## 6. Transmission impact

新增图谱节点 `DIGITAL-SURROGATE-XUXIU-1061-1062-YINYANG-BAOJIAN`，把《續修四庫》1061–1062 的现代数字再现与 12DF 的当前 NLC 卷1–4数字对象分开保存。

两条关系继续 fail-closed：

1. 与 12DF 物理本是否同本：`UNRESOLVED`；
2. 是否直接见证《月令通攷》所引通书目标指纹：`UNRESOLVED`。

因此 generic `通書` 的精确书名/版本仍未解决；本批只是关闭一个高价值“缺卷五/完整再现”搜索门，而不是把《陰陽寶鑒》提升为三命表的祖本。

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

无新 runtime candidate、无 winner、无 candidate collapse、无 algorithm reopen。

## 8. Next gate

下一优先级不再是重复扫描这组《續修四庫》卷界，而是：

1. 继续寻找 **1578 之前**、能同时直接保存 `大寒十三後` 与 `雨水後四日` 两个高信息指纹的通书/历书异本；
2. 继续独立寻找中国本土 C-II-N / 南京大统 59/41 数值载体；
3. 寻找能把连续日值转换为三命/月令整数换档日的历史 threshold / selection / quantization 规则。

Research record: `docs/research/ZIWEI-XUXIU-YINYANG-BAOJIAN-COMPLETE-REPRODUCTION-R1.json`.
