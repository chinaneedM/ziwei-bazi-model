# 项目连续性与上下文治理 R2（天问试点）

2026-11-26 用户授权。R2 只改变取数、检索、恢复和验证的实现，不改变 R1 的史料权威、原页证据、未决事项、排盘 CLOSED、双体系独立、零付费/免账号、远端唯一事实源及 forward-only 约束。现阶段为可回退试点，不声称已提高实际 Chat 上下文容量。先验收天问，再分别适配石器时代、大六壬。

## 1. 新对话/继续：有限输出、完整验证

1. 每次新对话从真实远端分支读取 HEAD/tree，最近提交和相关PR、精确HEAD Actions（分页）。工具层仅输出 SHA、最新提交摘要、所需路径/Blob SHA、计数、失败或未完成项；禁止把完整 API 响应、整个树、历史焦点/检查点数组或所有 workflow 文件名送进模型。相同对话同一已核HEAD的不可变blob不重复展开；HEAD变化仅核对变化对象及依赖。
2. 读取本协议及R1 governing policies、宪章、研究权威、图谱与广度路线；以相关段落为主，保留全部适用约束。若新政策、冲突或不明依赖出现，展开核实。
3. 读取 `docs/PROJECT-RECOVERY-VIEW-R2.json`。这是**纯派生视图，不是第二状态数据库**。必须逐项将 bindings 与精确HEAD树中六个真实路径的blob SHA比对，检查 schema、authority、预算、全部P0条目数、当前任务和两个最新批次/检查点。只有 exact-HEAD `verify-research-omission-continuity` 成功（含R2 verifier），且其余必须门禁无已知失败或未完成阻塞时，才允许以此代替六个大型文件的例行全量解析；不将其它CI或前一HEAD的成功当作当前成功。没有成功检查、绑定不符、缺字段、预算超限或不一致时，回退R1：直接读取相应权威blob，在工具层完整解析，精确投影必要字段。所有P0保持可核阅，若超过单页预算分批，绝不悄悄裁减。没有完整读取就不能声称完成。
4. 根据 focus、next_deliverable、latest_matrix_batch、latest_breadth_batch、checkpoint.evidence_refs 打开当前相关文件。focus.truncated=true 时必须取权威current_focus指定项完整正文。只在任务实际需要或冲突时读取历史文件。R1当前源/图/Matrix/遗漏审计及全量来源查重门禁仍有效；无新研究证据不得改变语义状态。
5. 每次工作单元以原子提交保存结果、状态、风险、下一步；不依赖会话结束摘要。写入前重查远端，非破坏性 lease。六个权威输入任一变化，必须同一提交重新生成恢复视图，不用将新HEAD写入文件。运行脚本 `python scripts/project-context-r2.py build`，随后 `verify`。Chat connector-only 时使用下方等价投影合同生成，再由CI严格复验。
6. 工具输出常规目标每次≤3000字符、恢复视图≤12000 UTF-8字节。只在具体证据、异常、代码审查需要时扩大，明确原因；不能因预算拒绝必要的历史核实。分页输出只返回必要条目，绝不把截断/缺页当作完整。每轮记录有效成果而非以固定分钟/次数作为完成标准。上下文余量不可直接测量，采用输出字符数、重复调用数、完成工作单元作为代理指标。

## 2. 查重执行基线（完整索引尚未构建）

`python scripts/project-context-r2.py search "题名" "馆藏号" --limit 20`：在真实checkout内复用R1全库source verifier，随后遍历根及全部分片的实际字节、校验hash/计数，搜索原始JSON或解码后的单个字符串/键；输出完整匹配数、有限路径、分片hash和截断标志。精确字面检索≠语义消歧/版本同一。必须显式提供繁简异文、别名、编号；匹配后读原记录判断作品/版本/物件/数字替身。不可用局部未命中声称全库无重复。

Chat connector-only 无本地checkout时，用 `functions.exec` 工具层逐批读取精确manifest中的blob，分组约8–16片（实际工具限制优先），在每批中校验schema/count、原始JSON和递归字符串检索、累计已扫描编号、匹配路径、缺失/失败项和总数。工具层只输出少量计数与命中；完整232片当作一个调用已实测超出单次工具调用限制。根647条单独核查；不得凭文件清单判正文无命中。完整查重未完成须保持检查点OPEN。后续评估可校验、按blob增量更新的查询索引/分包；不提前加入复杂Bloom算法、全量重复数据库、额外CI工作流或未经证实的检索结果。优先在同一工具中一次扫描同时检查多个候选来源。

## 3. Chat端生成恢复视图（无checkout时）

从新提交拟纳入的六个权威输入原始JSON及实际blob SHA派生；以scripts/project-context-r2.py::project为精确合同。生成过程保留六个path→SHA绑定，状态schema_version/current_stage/invariants，Matrix行数和audited IDs数，根sources/manifest统计，graph nodes/edges，ledger open/P0（排除RESOLVED_WITH_EVIDENCE），research_execution_strategy.phase/next_deliverable/latest_breadth_batch_doc，historical_audit.latest_batch_doc，ledger最后checkpoint.id/evidence_refs，以及最后current_focus的零基索引、最多1600 Unicode codepoint的text、truncated布尔。全部P0包含id/title/status/next_action。字段名以现存视图为准，不复制完整历史对象。不修改权威状态来适配视图；生成blob和所有权威变更在一次tree/commit中发布；CI对六个原始文件重算并逐字段比对。生成或预算失败时不得伪造视图，改用R1恢复并修复门禁后继续。

## 4. 试点验收与复盘

基线HEAD 3a36af6bab030623c543a64bdfd30327cb78baa2。六个权威JSON工具返回合计7,609,276字符，派生视图4,594字符（99.94%字符量缩减；非实际token/总启动成本）。232分片，1286来源，32开放风险（P0五项），Matrix222/222，图468/375；15DN provisional仍为当前研究任务。不改变语义状态，原资料不删除。原先单次操作枚举1096个workflow或大量文件名会产生不必要返回，后续仅取相关统计/异常。当前直接git checkout因DNS不可用；真实数据上的Python测试由远端CI执行，未通过前保持试点，不使用快路径。后续用真实新会话对照启动输出、调用数、时长和有效完成量，检验索引方案及大量历史workflow触发成本；先统计触发条件和保留功能，不擅自停用旧门禁。确认稳定收益后才向另外两个项目推广。禁止承诺固定对话容量或固定运行时间。
