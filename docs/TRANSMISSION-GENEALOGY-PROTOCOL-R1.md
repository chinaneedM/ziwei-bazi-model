# 天问 Transmission Genealogy Protocol R1

## Status

```text
TIANWEN_TRANSMISSION_GENEALOGY_R1=ACTIVE_INCREMENTAL
GENEALOGY_MODEL=EVIDENCE_SCOPED_GRAPH_NOT_SINGLE_TREE
HISTORICAL_BACKFILL=INCREMENTAL
FUTURE_BATCH_TRANSMISSION_IMPACT=REQUIRED_WHEN_MATERIAL
```

## 1. Purpose

本协议把考据、训诂和版本校勘过程中已经产生的“传承信息”从叙述性备注提升为可持续维护的正式研究对象。

它回答的不是单纯的“某规则是否有古籍依据”，而是：

- 该规则、词语、数表或技术观念目前最早能追到哪里；
- 哪些版本真正保存了它；
- 哪些后世文本继承、改写、重命名或误传了它；
- 不同地域、历法、流派和技术传统是否形成分叉；
- 一个后世规则是否由多个上游知识层汇流而成；
- 哪些看似传承的关系其实只有结构相似，不能证明直接承袭。

## 2. 图谱而非家谱树

默认模型是有向、多类型、带证据作用域的图。

允许：

- 一个节点有多个上游来源；
- 同时代平行规则并存；
- 一个规则的文字来自 A、算法来自 B、地域校准来自 C；
- 后世重新组合早期材料；
- 同一书名形成多个不等价版本分支；
- 抄本、刻本、影印本、数字对象分别建模。

禁止为了叙事简洁把复杂关系强制压成 `A → B → C`。

## 3. 标准节点类型

图谱至少支持以下节点类型：

- `TEXT_WORK`：作品层，如《四時氣候集解》；
- `EDITION`：具体版本/刊本/抄本系统；
- `PHYSICAL_COPY`：可识别的馆藏、拍卖或私人实物；
- `DIGITAL_SURROGATE`：扫描、缩微、影印、数字对象；
- `PASSAGE`：具体篇章、页、段、表；
- `RULE_FAMILY`：机械规则家族；
- `MECHANICAL_RULE`：足够精确可重放的单一规则；
- `TERM_CONCEPT`：术语及其历史技术义；
- `REGIONAL_STANDARD`：地域性的历法、计时、观测或技术标准；
- `SCHOOL`：可证的流派/传承群体；
- `PERSON`：作者、编者、校者、传人、研究者；
- `INSTITUTION`：钦天监、书坊、藏书机构等；
- `OPERATIONAL_ARTIFACT`：历表、漏箭、历书、仪器记录等可执行技术材料。

节点类型可以扩展，但新增类型必须有清晰语义，不能以模糊标签代替已有类型。

## 4. 四层年代防火墙

对文本与版本对象，必须尽量分别记录：

```text
work_composition_date
edition_impression_date
physical_copy_date
digital_surrogate_date
```

还可记录：

```text
preface_date
postface_date
catalog_assigned_date
acquisition_date
```

但这些辅助日期不得静默替代四层主日期。

特别禁止：

```text
早期序跋日期 -> 当前物理抄本一定同年
作品形成于某朝 -> 当前扫描对象一定是该朝实物
现代影印标题写“明版” -> 未经书目/物理证据即视为精确刊年
```

## 5. 标准关系类型

### 5.1 强事实关系

- `ATTESTS`：对象直接见证某规则/文字/数表；
- `EDITION_OF`：版本属于某作品；
- `PHYSICAL_COPY_OF_EDITION`：实物被可靠绑定到某版本；
- `DIGITAL_SURROGATE_OF`：数字对象对应某物理对象/版本；
- `EXPLICITLY_CITES`：文本明确引用另一文本/作者/制度；
- `TRANSMITS_RULE`：后见证可明确证明保存同一机械规则；
- `RECENSION_VARIANT_OF`：可证的版本/异文关系；
- `TERMINOLOGY_NORMALIZES_TO`：训诂后证明是同一机械概念的不同术语。

### 5.2 解释性/候选关系

- `TEXTUAL_ANCESTRY_CANDIDATE_FOR`；
- `STRUCTURAL_ANCESTRY_CANDIDATE_FOR`；
- `SHARED_COMMON_ANCESTOR_CANDIDATE`；
- `REGIONAL_ADAPTATION_CANDIDATE_FOR`；
- `SCHOOL_REINTERPRETATION_CANDIDATE_FOR`；
- `SYNTHESIS_COMPONENT_CANDIDATE_FOR`。

这些关系必须携带 `status` 与 `confidence`，不能渲染成已证实直传。

### 5.3 并存/反证关系

- `PARALLEL_COEXISTS_WITH`：同一时代或相近环境中并存但无直接传承结论；
- `CONTRADICTS`：机械规则或文字实质冲突；
- `DISPROVES_LINEAGE_SHORTCUT`：证据足以否定某个过度简化的传承推断；
- `TRANSMISSION_ERROR_OF`：有足够证据证明转录、刻印、OCR、目录或后世理解错误。

## 6. 关系状态与置信度

`status` 至少允许：

- `CONFIRMED`
- `HIGH_CONFIDENCE`
- `PROBABLE`
- `POSSIBLE`
- `UNRESOLVED`
- `DISPROVED`

`confidence` 与 `status` 分开保存，可使用项目既有 HIGH / MEDIUM_HIGH / MEDIUM / LOW 等体系。

每条关系还必须说明主要证据类别，例如：

- `DIRECT_PHYSICAL_TEXT`
- `DIRECT_BIBLIOGRAPHIC_BINDING`
- `CONTEMPORARY_OPERATIONAL_ARTIFACT`
- `RECEIVED_TEXT`
- `SECONDARY_SCHOLARSHIP`
- `MECHANICAL_REPLAY`
- `COMPOSITE_EVIDENCE`

不得仅靠“来源数量多”提升关系强度；仍按研究权威政策进行证据加权。

## 7. 八条反过度推断规则

1. **相同文字 ≠ 已证明直接抄袭。** 可能存在共同祖本。
2. **相同数字 ≠ 同一数表。** 必须比较锚点、顺序、步长、单位和使用情境。
3. **相同书名 ≠ 同一版本/实物。** 必须区分 edition/copy。
4. **序跋年代 ≠ 当前物理副本年代。** 除非另有版本/实物绑定。
5. **目录记录 ≠ 页内文字。** 目录强于身份，不能替代规则字形核读。
6. **OCR/转录 ≠ 物理字形。** 字形争议优先物理影像。
7. **后世同法 ≠ 证明早期已有。** 后见证只能证明其自身时代及可合理追溯范围。
8. **并存 ≠ 承袭。** 两种方法同朝同时出现，反而可能证明多层传统并存。

## 8. 复合传承

如果一个后世规则明显由多个独立层构成，应使用多个入边，而不是挑一个“祖先”。

例如当前时间刻制研究允许这样的候选模型：

```text
早期 40↔60 漏刻/通书数表家族 ─┐
南京/大统地方数值标准 ─────────┼→ 1578 三命通会显示表
更早百刻与时刻文本传统 ────────┘
```

只有当文本依赖关系被直接证实时，才升级成更强的 direct-dependence 关系。

## 9. 每批研究的 transmission_impact 契约

从本协议激活以后，只要研究结果对传承关系有实质影响，批次研究 JSON 应记录：

```json
{
  "transmission_impact": {
    "nodes_added_or_strengthened": [],
    "edges_supported": [],
    "edges_revised": [],
    "edges_rejected_or_unproved": [],
    "unresolved_lineage_questions": []
  }
}
```

旧批次允许逐步回填，不要求一次性重写全部历史。

若某一批只有产品实现或访问边界、完全不影响传承，可明确写：

```text
TRANSMISSION_IMPACT=NONE
```

而不是虚构关系。

## 10. Forward-only 修订

传承图谱中的关系允许被新证据升级、降级或否定，但不得静默覆盖。

重要修改应保留：

- prior status；
- new status；
- triggering evidence；
- adjudication reason；
- batch/date；
- 是否影响排盘算法。

传承关系的改变默认**不自动影响排盘算法**。算法仍受现有 reopen gate 控制。

## 11. 与考据 Matrix 的关系

Historical Provenance Matrix 仍是“规则审计”的事实主表；Transmission Genealogy Graph 是“规则及其载体如何历史连接”的关系层。

二者关系：

```text
Matrix = rule-centric audit ledger
Graph  = lineage-centric evidence network
```

它们应互相引用，但不能互相替代。

## 12. 与未来出版的关系

未来源流史写作应从图谱派生：

- 按时代生成 chronology；
- 按规则生成 lineage；
- 按书籍生成 recension history；
- 按地域生成 transmission map；
- 按术语生成 philological evolution；
- 按争议生成 competing-method history。

出版文本必须能够回指图谱节点、关系及证据，不得把叙事性推测升级成事实。

## 13. 当前种子批次

Batch 12CH 是 R1 的首个显式 `transmission_impact` 种子：

- 1455《四時氣候集解》景泰六年胡廷璨刻本直接见证粗粒度 `40↔60` 通书表；
- 1447 南京 59 刻官方标准与 1455 夏至 60/40 通书表被证明可以并存；
- 因而否定“同朝只存在一种表”“出现 59/41 就等于三命通会直祖”的简化路线；
- 对 1578《三命通会》的关系仍是复合祖源候选，而非直接抄传定论。

机器图谱：`docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json`。
