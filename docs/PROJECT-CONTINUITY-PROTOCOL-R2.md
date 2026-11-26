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

## 5. R2.1：复用现有CI作精确全库查询（2026-11-26）

R2首版真实CI中全库控制检索与其余5项测试合计0.143秒；连接器单次32片读取亦已超调用限制。因此优先采用已存在的检查点与CI计算，不另建索引数据库、重复语料包或新workflow。对需要全库字面查重的研究，在**原本就需要提交的研究检查点**同一原子提交添加或替换 `docs/PROJECT-REGISTRY-QUERY-R2.json`（schema、query_id、当前checkpoint_id、registry manifest blob SHA、明确异文/编号terms、limit≤20），保持研究语义未结项。现有 `verify-research-omission-continuity` 调用 `request`，在真实checkout中重跑R1完整来源门禁并逐字搜索所有根及分片。禁止为查询任意外部命令、网络地址或路径；请求仅为固定字段的字面字符串。
 
领取结果：读取精确提交的成功workflow/job日志，在工具层只提取 query_id 对应JSON一行，核验 checkpoint_id、request_blob_sha、registry_manifest_blob_sha、全库files/records、per_term_matching_files、scope、status=PASS、truncated。不得把NO_REQUEST、STALE_CHECKPOINT、失败、排队或缺失输出当作零命中；活动请求manifest变更必须修正后再执行。旧请求不属当前checkpoint时明确跳过，无须删除历史提交。若truncated=true，不作完整候选判定，按需要补读匹配路径或细分查询。语义近似、异体字、同本/版本/物件/替身仍由研究者判断，不升级为原页证据。
 
结果若已满足且manifest/request/checkpoint/验证程序均未改变，可复用相应已验证结果作候选来源；新HEAD接受仍按R1/R2验收门禁，发生源登记变更立即失效。此方案利用现有阶段检查点，不增加用户操作；无需检查点或CI不可用时仍用本地全库命令/连接器小批扫描，不为了查询制造无意义提交或等待空转。试点15DN请求覆盖此前明确的八个查重词并补三个书名异体组合，保留TW-OPEN-0032，未据查询自行准入来源或改变历史状态。

## 6. R2.1 真实恢复复核与查询结果保全（2026-11-26）

在新的 Chat 会话以原 R1 启动语恢复成功：HEAD `b2782a5cc4d43de51e52f8adc53222371c00368c`、tree `51aebbc1a520b1b699f22733025d2930fb8d06c3`，六个恢复视图绑定与真实 docs tree 逐一吻合；[精确HEAD连续性CI](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45765999635)通过，视图5108 UTF-8字节、全部五项P0保留、62项原遗漏风险测试及7项R2测试通过。复核时21项Actions中20成功、clean-training-system仍运行；不得记为全通过。常规 fetch_file 对大current-state返回空正文，证明不可将其当作已读；R2验证视图/必要时权威blob回退仍是正确路径。

查询日志有保留期限，不应成为唯一长期研究交接：已验证的字面查询结果应以最小记录附入现有对应检查点或后续正式批次，保留 exact-HEAD、run/job、request/manifest/验证程序blob、checkpoint、范围、逐词统计与截断标志。恢复时优先读该记录、验证当前绑定及适用门禁；有冲突、绑定变化或缺少可信验证时回到原日志/重算。不得新建第二查询数据库；不重复粘贴日志全文。15DN 的真实结果已追加于原检查点；旧段落为当时尚未完成的记录，不能忽略其后追加的验证。此次仅保存基础设施执行证据，不宣告研究批次完成、不准入来源、不修改历史语义状态或关闭风险。下一次研究单元在完成语义去重和证据准入裁决后按R1/R2原子更新权威状态与派生视图。

原启动语继续永久作为兼容入口；后续协议升级由 R1 指向当前生效协议，无需用户反复更换启动语。首次真实会话验证不等于已证明多轮上下文寿命提升，仍需后续有效工作单元对照。

## 7. 用户续接信号与上下文反馈（2026-11-26，用户明确确认）

默认解释：用户发送完整固定启动语表示上一大对话遇到上下文限制、开启新的大对话；发送「继续」表示当前大对话内进入下一小轮。用户明确表示主动换对话、切换任务、正常结束或其他原因时，以其说明为准。启动语是用户行为代理信号，不是平台遥测；不得宣称能直接观测实际上下文窗口、剩余token、截止时刻或上一轮未保存思考。无法看到前一会话完整记录时，不虚构精确轮数、耗时或消耗量，标记UNKNOWN。

用户提供的历史基线：早期每大对话约5–7个小轮、典型小轮约20分钟；近期约2个小轮、小轮不足5分钟。均为用户回顾性描述，不是平台测量。R2.1从2026-11-26试用，不以单次结果宣告长期收益。

每次实际续接时以已有记录核查可观察的工作单元完成量、远端检查点完整性、工具返回字符量、重复调用、恢复成本及可能的上下文浪费；能够可靠关联时才比较同一大对话内小轮次数。优先记载异常、可操作修复及阶段性实测，不新建逐轮日志、数据库、自动化或额外用户操作。完整启动语依旧兼容；不要求用户另报何时触发限制。每次会话以研究质量及有效成果为主，不用固定耗时或轮数填充任务。

实施层规则：工具输出一律先构造明确字段白名单，再限制长度，尤其禁止直接输出整个 research_execution_strategy、breadth_first_progress、current_focus历史或checkpoint_log。长正文仅在具体证据审查时分段读取；先统计并报告所需字段，保留完整原始权威数据和必要审计。15DN曾出现一次工具投影误将完整历史进度字段输出（工具报告截断），此为明确的执行缺陷，后续避免；不能把工具截断当作原始文件已完整呈现。不得因压缩而削弱来源、P0、forward-only或CI门禁。
