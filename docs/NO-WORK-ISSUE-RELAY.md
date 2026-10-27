# GitHub Issue 自动训练通道 V3

该通道供Work额度不可用时使用。Chat完成当前案例预测与揭盲复盘，GitHub Actions负责预检、冻结、加密答案评分、学习发布、维护检查和状态切换。

## 操作

1. 新开Chat，发送`docs/CHAT-WORK-RUNBOOK.md`中的固定预测口令。
2. Chat完成`PREDICTION-WORKBOOK-V2`并冻结。
3. 揭盲后让Chat生成完整`TRAINING-ISSUE-PACKET-V3`。
4. 打开仓库“无 Work 训练提交单”，正文框`Ctrl+A`后粘贴整份JSON并提交。

不要手工拼装Schema、哈希、证据或重复结构。控制器会在启动轮次前验证完整推理；不合格提交不会消费当前案例。

## V3边界

提交保留完整：

- 选项前全案模型；
- 同案跨题一致性；
- 紫微与八字独立封卷；
- 具体证据账本和证据家族；
- 全选项矩阵和全部必要配对；
- 真实反转测试；
- 分解置信度；
- 决定性规则反事实消融；
- 复训定向修复声明。

失败时增加`learning_release_id`和`MODEL-LEARNING-CORRECTION-V3`。修正包含根因、修正类型、通用陈述、适用条件、限制、预期效果、能力上限、来源依据和理由。只有`NEW_GENERAL_RULE`可以带新规则；其他修正的`rules`为空。

## 自动执行

- 只接受仓库所有者创建的训练Issue；
- 无效Schema在启动轮次前拒绝；
- 冻结后才可访问加密答案；
- 不保存逐题答案映射；
- 首次盲测与间隔复训统计隔离；
- 阶段验证与最终留出不得创建规则；
- 失败可发布非规则型模型思路；
- 题型低样本只报告`INSUFFICIENT_SAMPLE`，不调参、不重排；
- 不修改`sources/canonical/`；
- 全套验证通过后才提交`main`。

Issue失败时仓库不会提交半成品。根据不含答案的Actions错误修正完整V3包，再新建Issue。
