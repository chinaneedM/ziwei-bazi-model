# 日常训练操作单：Chat＋Work

## 开始当前案例下一轮

新开Chat并发送：

> 开始当前案例下一轮。任何仓库检索前，唯一允许的首次读取是公共仓库main最新`chat-input/prediction-access-contract.json`；立即执行其中的默认拒绝契约，契约未执行前不得读取状态、当前案例、模型或配置。随后按`startup_sequence`读取`training/state.json`与`chat-input/current.json`，确认内嵌契约与启动契约完全一致，再按动态白名单读取当前绑定的`chat-input/runtime-model.json`、`sources/canonical/`、当前发布实际引用的`model-learning/`文件及必要配置。预测阶段只可使用GitHub单文件读取；硬性禁止File Library、附件、历史上传、Personal Context、跨对话记忆、仓库搜索、提交/历史/差异/目录枚举、旧预测、旧揭盲、旧诊断、learning-ledger、答案或密钥。任一违规立即停止且不得冻结或评分。先确认`prediction_allowed=true`并核对运行模型哈希；绑定通过后读取一次编译运行模型并输出`BINDING_VERIFIED`检查点。在看选项和比较选项之前，先建立并冻结全案共享的`blind_chart_model`、紫微静态结构、八字静态结构、必要时间事实与共享证据注册表；随后逐题投影，完成语义原子化、紫微独立封卷、八字独立封卷、双轨裁决、具体证据账本、全选项矩阵与全部必要配对、Top1真实反转测试、置信度分解、规则反事实消融和跨题一致性检查。证据不设数量配额；`max_applied_rules_per_question`只限制model-learning规则，不限制S00–S19证据。先使用题级路由与知识卡精确锚点；若任何竞争项仍有未闭合区别原子、直接反证未查、双轨或时间终点未闭合，或未读声明来源仍可能改变排序，必须渐进扩大检索。严格按`chat_work_handoff_contract`与冻结前才读取的`prediction_row_template_ref`输出完整`PREDICTION-WORKBOOK-V2`，不得使用近义自定义字段。完整预测冻结且binding与访问收据验证通过后，转换为`POST_PREDICTION_HANDOFF`，只允许一次`GITHUB_CREATE_ISSUE`创建唯一交接；完整归一化与机器预检由GitHub controller执行，Chat和用户均无需`gh`、clone、Python或终端。压缩时不得删结构、实质证据或改变Top1/Top2；不得读取或写入答案。完成后停止，等待我切换Work。

创建交接前必须把`handoff_payload_template.prediction_access_execution_receipt`原样保留在交接顶层。该收据绑定契约哈希、唯一首读路径、空的契约前读取列表及状态→当前输入的后续顺序；缺失、改写或顺序不符时预检必须失败，且不得启动、冻结或评分。

预测过程中约每15–20秒输出一次简短可恢复检查点，依次覆盖绑定、共享盘面、
每题分析、跨题复核和正式交接。检查点只记录当前绑定、已完成阶段、共享证据ID及
未决项，不创建第二张Issue，也不代表已经最终冻结。连接中断后先重验`main`绑定与哈希，
绑定未变时复用已显示的阶段摘要，只重跑未决阶段和最终一致性；不得把中断的内部推理
假定为已完成冻结。

若开始后发现任何白名单违规，立即丢弃所有推理方向，不创建预测交接单。读取了答案、旧预测
或其他案例污染对象时，控制器登记`PRE-FREEZE_CONTAMINATED_NOT_EXECUTED`并隔离案例；
仅发生契约启动顺序违规且未泄露答案时，控制器登记同一状态但只作废当前轮次，为同一案例生成
下一干净轮次与无答案输入包。

## Work闭环

切换Work并发送：

> 冻结、评分；若未达标则先分类根因，再选择可推广的执行、测量、校准、权重、范围、合并、退休、测试、假设或新规则修正，落库并加入间隔复训队列；只有确认缺少可推广知识时才用NEW_GENERAL_RULE。发布后进入下一新案例。不得修改S00–S19，不得消费未通过完整性预检的案例。

Work读取唯一交接Issue，核对全部绑定并预检完整推理。评分必须晚于冻结；PASS不生成修正，FAIL使用`MODEL-LEARNING-CORRECTION-V3`。复训继续从零推理，但不计首次盲测、独立规则证据或阶段门。

Work开始时由系统运行`scripts/bootstrap-work-env.sh`，自动补齐稀疏检出所需目录并在
`gh`缺失时安装固定版本、校验下载哈希。binary/auth能力分离及connector-first路由见
`docs/WORK-GITHUB-ACCESS-R2.md`；connector已覆盖任务时，本地`gh`未认证不是环境失败。
该环境初始化不得要求用户执行命令。

若交接Schema或长度预检失败，必须在读取答案前停止。Schema修复只允许把已冻结内容机械映射
到精确字段或压缩重复措辞，严禁改变Top1、Top2或借答案重新推理。

## 维护

系统每25道首次盲测题做短维护、每100道做中期维护，并检查推理退化、置信失真、规则治理、复训根因修复、题型分布以及Chat运行包字符数、工具读取量、检查点间隔和交接正文长度。低样本主题只观察，不改变案例顺序、通过标准或模型权重。任何性能优化若删减紫微、八字、岁运、现实终点、全选项比较或反证主题，验证必须失败。

用户不需要运行Git、gh、Python或终端命令，也不需要手工填写哈希或复杂Schema。
