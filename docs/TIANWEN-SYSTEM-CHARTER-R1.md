# 天问（TIANWEN）系统宪章 R1

## 0. 身份

```text
SYSTEM_UMBRELLA_NAME_ZH=天问
SYSTEM_UMBRELLA_NAME_EN=TIANWEN
WORKING_MOTTO=天以命运问人，人以命理问天。
TIANWEN_SYSTEM_CHARTER_R1=ACTIVE
```

“天问”不是某一版桌面软件的临时产品名，而是本项目长期研究与工程体系的总名。

名称表达两层方向：

- **天以命运问人**：人的出生时间、环境、际遇与生命历程构成一个有待理解的问题；
- **人以命理问天**：人通过历法、干支、星曜、阴阳五行及历代术数知识，尝试理解其中是否存在可描述、可检验的秩序。

“问”比“答”更重要。天问不把任何一本古籍、某个流派、现代软件、当前模型或当前仓库结论视为不可质疑的最终答案。

## 1. 长期使命

建立一套能够长期演化的紫微斗数与四柱八字知识基础设施，使下列问题可以分别回答、彼此追溯：

1. **怎么算**：确定性排盘的机械规则是什么；
2. **为什么这样算**：规则有哪些历史、文本、历法、术语与流派依据；
3. **怎样传到今天**：文本、版本、人物、地域、流派和规则如何传承、分叉、汇流、讹变；
4. **将来如何检验**：在独立阶段中评估这些规则是否具有现实解释力或预测价值。

当前阶段只执行前 3 项中的已授权范围。第 4 项属于未来独立阶段，**不因本宪章的建立而进入当前开发范围**。

## 2. 四层体系

### A. 天问·排盘 — Deterministic Charting

目标是生成可复现、可测试的紫微斗数 + 四柱八字确定性排盘。

当前状态：

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

历史研究不能仅因“发现另一种古法”就重开现有算法。只有满足仓库既有 algorithm-reopen gate 的真实、可复现、作用域明确的实现缺陷才可局部重开。

### B. 天问·源流 — Historical Provenance & Philology

目标是回答规则、术语、文本和版本的历史依据，并进行考据、校勘与训诂。

当前主要阶段：

```text
FUSION_CHART_HISTORICAL_PROVENANCE_AND_SCHOOL_AUDIT_R1=IN_PROGRESS
```

必须遵守 `docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md`。

### C. 天问·传承谱 — Transmission Genealogy

目标是把历史审计产生的离散结论连接成可持续修订的传承图谱：

```text
text / edition / physical copy / passage
rule / term / school / person / region / institution
                ↓
        evidence-scoped graph
```

传承关系不是预设的单一师承树，而是允许多源汇流、平行并存、地域改造、版本分叉、术语变迁和传播错误的**有证据图谱**。

当前状态：

```text
TIANWEN_TRANSMISSION_GENEALOGY_R1=ACTIVE_INCREMENTAL
```

既往研究批次逐步回填；从本协议生效后的新历史批次开始，凡材料足以影响谱系，都应显式记录 `transmission_impact`。

### D. 天问·命理模型 — Future Empirical / Predictive Layer

未来可在排盘、历史谱系和独立数据治理成熟之后，再研究解释、经验检验与预测模型。

当前状态：

```text
PREDICTION_AI_INTERPRETATION=CURRENTLY_OUT_OF_SCOPE
```

本层不得反向污染当前历史证据裁决：预测效果不能把无出处规则自动改写成“古法”，历史权威也不能替代未来的经验验证。

## 3. 天问的认识论原则

### 3.1 没有因文件名、年代或名气而天然正确的来源

禁止以下推理：

```text
S00-S19 写了，所以一定正确。
古籍写了，所以一定唯一正确。
现代软件这样排，所以古代一定这样排。
当前 AI 这样判断，所以证据已经闭合。
```

证据必须按来源、版本、物理对象、文本位置、时代、流派和机械规则作用域裁决。

### 3.2 结论必须可追溯

重要结论应尽量能追溯到：

```text
implementation / question
→ exact mechanical rule
→ passage / table / artifact
→ work
→ edition
→ physical/digital witness
→ provenance and date scope
→ competing witnesses
→ adjudication
```

### 3.3 不把不确定性伪装成确定性

证据不足时允许并要求保存：

- 未决；
- 流派限定；
- 版本限定；
- 候选方法；
- 共同祖源假说；
- 平行发展；
- 无法确认的直接传承边。

“暂时不知道”是可审计状态，不是研究失败。

### 3.4 同时防止虚假等价

保留候选不等于所有说法永远平权。若物理原件、独立同代证据、机械重放和文本关系已足以证明某读法为转录错误、误刊或后世误解，应按证据降级，并保留裁决过程。

## 4. 传承史的四个日期必须分开

任何重要古籍对象，应尽可能分离：

1. `work_composition_date` — 作品形成/编纂时代；
2. `edition_impression_date` — 某版刻印、刊行或抄成时代；
3. `physical_copy_date` — 当前实际审读的物理副本年代；
4. `digital_surrogate_date` — 数字化、影印、缩微或现代再版形成时间。

内部序跋写有早期年代，**不自动等于当前物理副本就是那个年代**。

此原则由 Batch 12CH 的 `NCL-03164《四時氣候集解》舊鈔本` 范围校正作为首个明确工程案例。

## 5. 传承史必须是图，不是预设家谱

天问允许一个后世规则同时拥有多个上游层：

```text
A：文字/训诂传统 ─┐
B：数表/算法传统 ─┼→ D：后世综合规则
C：地域/历法标准 ─┘
```

因此：

- 相同文字未必证明直接抄袭；
- 相同数字未必证明同一数表；
- 相同书名未必是同一版本或同一物理对象；
- 同时存在未必互相传承；
- 后世明确记载不能无条件倒推为更早时代的事实。

## 6. 可持续升级而非静态定稿

天问的目标不是一次性写出“最终答案”，而是建立版本化证据系统。

当未来出现：

- 新开放的珍本影像；
- 新目录、档案或出土材料；
- 更可靠的版本学研究；
- 更强的图像、文本、计算或模型能力；

系统应能够重新审计旧判断，并以 forward-only 方式记录：

```text
旧判断
→ 新证据
→ 受挑战点
→ 新裁决
→ 改变原因
→ 旧状态保留为历史
```

不得静默重写过去。

## 7. 面向未来著述

未来的《紫微斗数源流考》《四柱命理源流考》或更大的《中国命理术数传承史》，应当是证据图谱和审计记录的**可读派生物**，而不是先写叙事、再寻找材料证明叙事。

换言之：

```text
证据 → 图谱 → 裁决 → 叙事
```

而不是：

```text
预设故事 → 选择性取证
```

## 8. 当前工程边界

本宪章建立后：

- 不改变已经 CLOSED 的确定性排盘产品状态；
- 不自动新增任何预测、断语或 AI 解盘功能；
- 不因“天问”品牌化而降低现有证据门槛；
- 不要求一次性回填全部既往批次；
- 要求以后研究尽量同时服务于排盘正确性、历史考据和传承谱系三层。

相关协议：

- `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`
- `docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md`
- `docs/TRANSMISSION-GENEALOGY-PROTOCOL-R1.md`
- `docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json`
