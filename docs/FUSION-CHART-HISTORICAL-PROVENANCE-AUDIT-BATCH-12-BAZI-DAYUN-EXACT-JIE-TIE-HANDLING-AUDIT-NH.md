# Fusion Chart Historical Provenance Audit R1 — Batch 12NH

## HPA-DAYUN-007 Exact-Jie tie handling：交节等号语义、训诂边界与 fail-closed 审计

Status: **MODERN FAIL-CLOSED POLICY / HISTORICAL EQUALITY UNRESOLVED / ONE PROVENANCE DEFECT REPAIRED / NO ALGORITHM REOPEN**

本批审计 `HPA-DAYUN-007`：当出生 UTC 瞬间恰好等于已解析的前一节气瞬间时，大运起运计算应如何处理。

### 1. 当前实现

两个已发布 Bazi temporal profile 都固定：

`exact_jie_tie_policy=FAIL_CLOSED`

运行时在：

`birth_utc == previous_jie_utc`

时返回失败诊断：

`EXACT_JIE_TIE_UNRESOLVED`

这不是古法结论，而是项目对未闭合边界条件的现代治理策略。

### 2. 历史文本真正说了什么

当前已绑定的宋《五行精纪》卷三十三与明《三命通会》卷二《论大运》都采用同一类严格前后措辞：

- 顺行：以“生日后未来节气”计；
- 逆行：以“生日前过去节气”计。

这两组措辞清楚支持“向后数到未来节 / 向前数到过去节”的方向结构，却没有写出出生瞬间**恰等于**节气瞬间时的等号归属，也没有规定零间隔是否立即起运。

因此不能从“后 / 前、未来 / 过去”自动补出 `>=`、`<=` 或“等号归新月令”等现代程序规则。

### 3. 训诂裁决

本批把三个层次分开：

1. `生日后 / 生日前`：文本中的严格相对位置语言；
2. `未来节气 / 过去节气`：顺逆方向所选的节气；
3. exact equality：现代高精度天文时刻下才会被程序显式触发的边界判定。

当前来源足以说明“等号没有被这些已绑定文本闭合”，但不足以证明历史上从未存在任何处理规则。因此：

- 不宣称“古人规定 fail-closed”；
- 不宣称“等于节气一定算下一节”；
- 不宣称“等于节气一定算上一节”；
- 不制造两个没有历史见证的伪候选。

### 4. PROV-DEFECT-029

Matrix 此前将该行的 `historical_period` 写成 `MODERN_STANDARD`，且 `current_profile` 仅写成模糊的 `BAZI temporal profiles`。

这容易把项目自己的防御性边界策略误读为某种现代行业标准。

确认：

`PROV-DEFECT-029=HPA_DAYUN_007_MODERN_STANDARD_LABEL_AND_VAGUE_PROFILE_SCOPE_OVERSTATED_THE_PROJECT_FAIL_CLOSED_POLICY`

修复后：

- 历史/时代作用域明确为现代项目 fail-closed boundary policy；
- profile 精确绑定到 continuous 与 Wenzhen compatibility 两个 released profile；
- 宋、明大运文本只作为“严格前后措辞但未闭合等号”的历史语义控制。

### 5. 结论

`HPA-DAYUN-007=MODERN_COMPATIBILITY_ONLY`。

保留 `FAIL_CLOSED` 是正确的当前工程决策，因为它拒绝把未证实的等号约定伪装成古法。只有未来出现来源明确、作用域明确且机械可重放的等号规则时，才允许新增 source-scoped candidate；现有算法不因此重开。

Matrix rows **220**；audited **211→212**；missing-product rows **10**。Provenance defects **28→29 confirmed / 28→29 repaired**；chart algorithm defects / reopens / candidate collapses 均为 **0**。

### 6. Transmission impact

`transmission_impact=NONE`。本批只收紧文本语义与现代边界治理，没有建立新的文本、版本、人物或流派传承边。

下一门 **12NI：HPA-ZT-016 Self/inward transformation direction**。

研究记录：`docs/research/BAZI-DAYUN-EXACT-JIE-TIE-HANDLING-AUDIT-R1.json`。  
证据记录：`docs/research/evidence/batch-12nh/dayun-exact-jie-tie-handling.json`。
