# Fusion Chart Historical Provenance Audit R1 — Batch 12MK

## 身宫干支：继承已审计规则的纯投影与异常身份回退修正

Status: **HPA-ZIWEI-013 AUDITED / INHERITED HISTORICAL RULE SCOPE / UI IDENTITY GUARD REPAIRED / CHART ALGORITHM UNCHANGED**

身宫干支展示是 `body_address` 与 `address_attributes` 按 `index + branch` 唯一联接后的 `stem + branch`，不是新增安身或起宫干公式。

| 输入 | 已审计来源 | 当前作用域 |
| --- | --- | --- |
| `body_address` | HPA-ZIWEI-002，Batch 06；received Fullbook `ZZQS-A-1744` | 生月上起子时，顺至生时安身；上游闰月/时间方案仍独立 |
| `address_attributes.stem` | HPA-ZIWEI-004，Batch 06；`ZZQS-A-1755..1756` | 五寅起宫干，读取已经生成的该宫宫干 |
| 展示联接 | 现代 Workbench `palaceGanzhi` | 不计算历法、身宫或宫干，不选历史候选 |

因此 HPA-ZIWEI-013 从 `IMPLEMENTATION_REVIEW_REQUIRED` 转为 `HISTORICALLY_SUPPORTED`，严格限定为继承两个父规则的历史作用域。不是声称古籍独立规定了现代“身宫干支显示字段”；没有新增古籍见证、精确刊年或流派胜出结论。原行完整保存在研究记录的 `prior_row`。

### 实际发现与修复

旧函数先过滤空宫干，再判断唯一性。若同一地址有一条有效宫干及一条空宫干，重复身份被掩盖，仍显示丙寅。`address_attributes={}` 会抛 TypeError；范围外整数地址若有匹配行也能显示。这不符合既有“缺失、畸形或非唯一身份显示 -”的产品契约。

仅调整展示层：先校验列表和 0..11 索引，按地址身份收集全部行，确认恰一条后再校验宫干。重复身份、错误容器、越界地址均回退 `-`。不增加宫干注册表或浏览器排盘公式。此问题登记为 `UI-BODY-GANZHI-IDENTITY-GUARD-001`，不计入历史来源元数据缺陷或排盘算法缺陷。

### 执行验证

实际执行 JavaScript，覆盖十个年干 × 十二生月 × 十二时支，共 1440 组；将宫位列表倒序后仍按身份正确读取，修正前后正常输出全部一致。另执行 14 个异常/错配/重复身份控制，包含空宫干重复记录的两种顺序。正常宫位不依赖列表下标。

现有展示/数据测试补入两个实际 JS 回归；相关三组共 19 项测试通过（5 + 3 + 11），无跳过。独立 before/after 采集保存于 `docs/research/evidence/batch-12mk/projection-replay.json`；上游 natal/models/registries 与 S01 文件摘要确认未改动。

Matrix 为 198 项、已审 167 项、缺失产品候选仍 10；来源缺陷 17/17；算法缺陷、算法重开、候选折叠仍 0。排盘 CLOSED，`TRANSMISSION_IMPACT=NONE`。

本批首次给已有 supplemental chronology 增加规则行裁决。`supplemental_rule_audit_batches` 单独登记这一行效应，保留原有主批次前缀与完整续接顺序，避免把以前的访问批次重写为规则裁决。

下一门 12ML：HPA-BAZI-FLOW-002，动态十神是否纯粹复用已审计本命十神映射，并保持日主锚点和事实边界。原刊恢复分支继续暂停为访问未决，等待实质新机制。

研究记录：`docs/research/ZIWEI-BODY-PALACE-GANZHI-PROJECTION-AUDIT-R1.json`。
