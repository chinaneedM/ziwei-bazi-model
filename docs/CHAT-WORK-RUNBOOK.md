# 日常训练操作单：Chat＋Work

## 开始当前案例下一轮

新开Chat并发送：

> 开始当前案例下一轮。只读取公共仓库main最新`chat-input/current.json`以及项目内与其manifest匹配的S00–S19只读镜像，禁止读取旧预测、评分、复盘、learning-ledger、答案或密钥。先确认`prediction_allowed=true`。在看选项和比较选项之前，先建立并冻结全案共享的`blind_chart_model`；随后逐题完成语义原子化、紫微独立封卷、八字独立封卷、双轨裁决、具体证据账本、全选项矩阵与全部必要配对、Top1真实反转测试、置信度分解、规则反事实消融和跨题一致性检查。证据不设数量配额；`max_applied_rules_per_question`只限制model-learning规则，不限制S00–S19证据。输出完整`PREDICTION-WORKBOOK-V2`并创建唯一`CHAT-WORK-PREDICTION-HANDOFF-V2` Issue；不得读取或写入答案。完成后停止，等待我切换Work。

## Work闭环

切换Work并发送：

> 冻结、评分；若未达标则先分类根因，再选择可推广的执行、测量、校准、权重、范围、合并、退休、测试、假设或新规则修正，落库并加入间隔复训队列；只有确认缺少可推广知识时才用NEW_GENERAL_RULE。发布后进入下一新案例。不得修改S00–S19，不得消费未通过完整性预检的案例。

Work读取唯一交接Issue，核对全部绑定并预检完整推理。评分必须晚于冻结；PASS不生成修正，FAIL使用`MODEL-LEARNING-CORRECTION-V3`。复训继续从零推理，但不计首次盲测、独立规则证据或阶段门。

## 维护

系统每25道首次盲测题做短维护、每100道做中期维护，并检查推理退化、置信失真、规则治理、复训根因修复和题型分布。低样本主题只观察，不改变案例顺序、通过标准或模型权重。

用户不需要运行Git、gh、Python或终端命令，也不需要手工填写哈希或复杂Schema。
