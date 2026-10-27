# Batch 12DO — 大統 C-II-N 42–48 整刻跨越閉合 × 《太乙統宗寶鑑》逐日日出差分機制控制

## Status

```text
CII_N_42_TO_48_EXACT_CROSSINGS=CLOSED
INTERIOR_THRESHOLD_BEHAVIOR=CONSISTENT_WITH_FRACTION_DISCARD
UNIVERSAL_FLOOR_RULE=NOT_PROVED
SUMMER_59_ENDPOINT=REQUIRES_SEPARATE_HANDLING
BATCH12CG_DAY43_INDEX=FORWARD_ONLY_CORRECTED
TAIYI_DAILY_SUNRISE_INTERPOLATION=DIRECTLY_ATTESTED_IN_XUXIU_MING_MANUSCRIPT_REPRODUCTION
TAIYI_CALENDAR_LAYER_PRE1578_PHYSICAL_DATE=UNRESOLVED
SANMING_YUELING_EXACT_FINGERPRINT=UNRESOLVED_SEPARATE_BRANCH
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NO
```

## 1. Why this batch

12DN 已把 C-II-N 的 47、48 刻跨越锁定在 66/67、73/74 日之间，但 42–46 仍来自 12CG 的探索性 `DIRECT_VISUAL_APPROX` 点。12DO 回到同一 NCL-06267 物理归档页，逐列重校早段跨越；同时审查并行工作刚取得的《續修四庫全書》1061《太乙統宗寶鑑》明抄本再现，用它检验“节气初值 + 逐日差分”是否属于历史上真实存在的日出生成机制。

## 2. C-II-N 42–48 整刻跨越

来源仍是 workflow `34869676923` / artifact `10358685142` / NCL-06267。最终数字均来自直接页图核读，不以 OCR 为字形或数值权威。

| 整刻 | 下界日 / 昼刻 | 上界日 / 昼刻 | 首个越过整数的日 |
| --- | --- | --- | --- |
| 42 | d20 = 41.9706 | d21 = 42.0326 | 21 |
| 43 | d33 = 42.9878 | d34 = 43.0842 | 34 |
| 44 | d42 = 43.9328 | d43 = 44.0474 | 43 |
| 45 | d50 = 44.8912 | d51 = 45.0164 | 51 |
| 46 | d58 = 45.9132 | d59 = 46.0482 | 59 |
| 47 | d66 = 46.9746 | d67 = 47.1074 | 67 |
| 48 | d73 = 47.9052 | d74 = 48.0380 | 74 |

这形成连续的首跨日序列：

```text
42→d21, 43→d34, 44→d43, 45→d51, 46→d59, 47→d67, 48→d74
```

## 3. 第二个 12CG 精确索引修正

12CG 曾把 `2208.19` 记作 day43，且明确标为 `DIRECT_VISUAL_APPROX`。本批直接列对齐表明：

```text
day43 = 2202.37 -> 44.0474 ke
day44 = 2208.19 -> 44.1638 ke
```

因此旧记录仅在“精确日序索引”意义上被 `SUPERSEDED_FOR_EXACT_DAY_INDEXING_ONLY`；12CG 文件不回写，其“C-II-N 连续曲线覆盖三命整数梯级”的宏观结论不变。12DN 对 day66/day67 的前向修正也继续有效。

## 4. 内部阈值机制：证据增强，但不能外推成全域 floor()

42–48 的每一个直接复核跨越都具有同一形态：前一日小于目标整数，后一日越过该整数。对这一个内部区间而言，“连续值达到下一整数后换档”的截去小数/阈值模型与实物数据完全一致。

但夏至端点仍是硬性防火墙：

```text
C-II-N day182 half-day = 2931.66
full daylight = 58.6332 ke
received whole-ke endpoint = 59/41
```

若把内部规律直接写成全域 `floor()`，夏至会得到 58，而不是 59。因此本批只允许：

```text
INTERIOR_42_48_FRACTION_DISCARD_COMPATIBILITY = STRONG
UNIVERSAL_FLOOR_OR_TRUNCATION_RULE = NOT_PROVED
ENDPOINT_ANCHOR/CAP/RECOMPOSITION = STILL_REQUIRED
```

这同时让 1624《類經圖翼》的“干净 +6/+13”59/41 阶梯获得更强的机械解释，却不把它反投为 1578 的祖本。

## 5. 《太乙統宗寶鑑》：独立逐日日出差分机制

live HEAD 新增 workflow `audit-xuxiu1061-taiyi-daily-sunrise-mechanism`，run `35387139084` 成功，artifact `10564496303`，源 PDF SHA-256 为：

```text
618a31924e05cbb8e8c5b49bfc0da2d7c7fb64526c6719175d685088cef29d83
```

直接页图审查锁定：

- p376：序文自署大德七年癸卯（1303）；
- p385：卷一天文表，表题可直接识别为“二十四氣初日損益朓朒及日出分”；
- p386：直接见“求每日日出分術”，其机械核心是把“差分秒”逐日累加/减到各气初日日出分，从而生成逐日日出分。

这证明一种“节气初值 + 日差累积 -> 每日太阳时值”的离散生成机制在该传本中是真实存在的，不是我们为了拟合 C-II-N 临时发明的现代算法。

## 6. 年代防火墙与《庚午元曆》控制

这里必须区分三种年代：

1. 《太乙統宗寶鑑》序文自署 1303；
2. 《續修四庫》所影对象著录为明抄本；
3. 卷一具体历法层是否在 1303 原始文本中已经以完全相同形态存在，当前物理证据仍未单独闭合。

因此：

```text
WORK_SELF_PREFACE_1303 = DIRECTLY_VISIBLE
REVIEWED_COPY = MING_MANUSCRIPT_REPRODUCTION
CALENDAR_LAYER_PHYSICALLY_PROVED_PRE1578 = NO
DIRECT_ANCESTOR_OF_CII_N = NO
DIRECT_ANCESTOR_OF_SANMING_1578 = NO
```

鲁楠、叶杰、李刚 2025 年校勘研究把该表与 1216《庚午元曆》进行系统比较，指出日出分按各气初值与逐日差分生成；《庚午元曆》传本文本本身也保存“求每日日出入晨昏半晝分”的逐日差分算法。二者提供的是历史算法类控制，而不是对 C-II-N 或《三命通會》的直接谱系证明。

## 7. 对 1624 干净阶梯与 1578/1589 异常指纹的分流

12DO 使两条支路的差异更清楚：

```text
C-II-N continuous daily curve
  -> interior 42–48 integer thresholds
  -> mechanically compatible with clean +6/+13 stepped family

Sanming 1578 / Yueling 1589
  -> 大寒十三後
  -> 雨水後四日
  -> still needs separate editorial/reduction/recomposition explanation
```

尤其“雨水後四日 -> 48/52”不能被本批的干净阈值模型解释成“雨水後十三日”的同一规则，因此禁止合并。

## 8. Genealogy consequence

新增节点：

- `PHYSICAL-COPY-TAIYI-TONGZONG-XUXIU-MING-MANUSCRIPT`
- `PASSAGE-TAIYI-JUAN1-DAILY-SUNRISE-INTERPOLATION`

新增关系：

- `TG-E0055`: reviewed Ming-manuscript reproduction attests the daily-sunrise passage；
- `TG-E0056`: Taiyi daily-interpolation passage is a POSSIBLE structural-mechanism control for the C-II-N daily table, not direct ancestry.

`TG-E0054` 保持 `PROBABLE`，但其证据由 47–48 两个跨越扩展为 42–48 七个连续整刻跨越。其强度只提升到“内部阈值机制”范围；夏至端点和 Sanming/Yueling 特殊换档日继续阻止全域闭合。

## 9. Product adjudication

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=12
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=12
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

没有新 runtime candidate、没有 winner、没有 candidate collapse，也不重新打开排盘算法。

## 10. Next gate

下一步应继续：

1. 直接重校 C-II-N 49–58 刻跨越，并显式重放节气真实长度/积日偏移，检验 1624 干净阶梯的 +6/+13 标注；
2. 优先寻找 1578 前中国本土、能直接保存 C-II-N 数值表或说明整刻换档规则的物理/近物理证据；
3. 继续把 Sanming/Yueling “大寒十三後 / 雨水後四日”作为独立异常支路追源；
4. NLC call 14202 复制服务路线继续并行，但本批仍不提交需要用户身份、费用或馆方授权的外部请求。

Research record: `docs/research/ZIWEI-DATONG-CIIN-42-48-CROSSING-AND-TAIYI-DAILY-INTERPOLATION-R1.json`.
