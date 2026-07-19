# Chat / Work 日常训练操作单

## 一、第一次准备答案

这一步只做一次。把每个案例的官方答案明文留在仓库外，由 Work 执行：

```bash
fortune-train keygen
FORTUNE_ANSWER_KEY='保存好的密钥' fortune-train encrypt-answer DEV-EXAMPLE-001 /tmp/DEV-EXAMPLE-001.answers.json
```

对 5 个案例依次生成加密答案并提交公共仓库。明文答案与密钥绝不提交。

## 二、一次性的项目整理

1. 原项目 S00–S19 不要整套删除；它们保留为只读镜像。
2. 当前两个 S02 中移除或停用 `(8)`，保留 `(9)`。
3. 打开“算命”项目的项目指令，全部选中旧 R16/R17 内容，用 `docs/PROJECT-MAIN-PROMPT-R1.txt` 完整替换。不要追加在旧内容后面。

这三个动作中，仓库侧规则和新提示词由系统维护；ChatGPT 项目文件与项目指令的界面操作只能由用户做一次。

## 三、在 Chat 中开始一轮

把下面这段直接发给 Chat：

> 开始当前案例下一轮。只直接读取安全启动包 `https://raw.githubusercontent.com/chinaneedM/ziwei-bazi-model/main/chat-input/current.json`，不得搜索 GitHub 仓库、代码、提交、历史或目录，不得读取其他 Git 文件。若启动包中 `prediction_allowed=true`，使用其中内嵌的当前无答案案例和当前 model-learning，并结合项目 S00–S19 只读镜像，从零完成 `recommended_round_id` 的预测；不得读取旧预测、评分、复盘或答案。完成后冻结输出并停止，等待我揭盲。本项目固定使用 Chat＋GitHub Issue 通道，不切换 Work。

Chat 完成预测后，在同一对话发送：

> 现在揭盲：答案字母串。请使用刚才冻结的预测评分和复盘，并生成可整份粘贴到“无 Work 训练提交单”的 `TRAINING-ISSUE-PACKET-V1` JSON。JSON 不得包含正确答案或密钥。

用户复制整份 JSON 到“无 Work 训练提交单”；GitHub 自动冻结、复核加密答案、更新状态和模型。用户不需要输入 Git、`gh` 或 Python 命令。

## 四、达标时

- 若连续达标次数是 1 或 2：仍训练同一案例，再开新轮次。
- 若连续达标次数是 3：当前案例完成，自动进入下一案例。

## 五、未达标时

未达标时不需要再切回 Chat 单独做一次交接。上一步的 Work 操作应在同一事务内完成深度复盘和落库。复盘需区分输入识别、取象、结构、应期、现实语义、双体系裁决、选项比较和执行遗漏；只允许产出可推广的模型思路、知识运用方法、执行步骤或待验证假设。若修正含案例专属答案映射，控制器会拒绝。

## 六、为什么不能全在 Chat 自动落库

Chat 可以完成命理推理，但当前产品边界下，纯 Chat 不能可靠地提交 Git 修改。安装 `gh` 也不会让 Chat 获得仓库写入身份；`gh` 只是某些命令行环境中的客户端。为了省额度，每轮预测都在 Chat 完成，之后只切一次 Work，把创建轮次、冻结、评分和必要的复盘落库合并为一笔事务。

如果 Work 用量暂时完全不可用，仍可另建“GitHub Issue + 自动工作流”入口：用户把 Chat 生成的结构化修正粘贴一次，GitHub 自动校验并提交。这不会消耗 Work，但仍需要一次人工粘贴，无法做到纯 Chat 零操作写 Git。没有 Work、API 或外部自动化身份时，公开仓库不可能接受匿名写入。

该入口的实际文件、固定 JSON 格式和逐步操作见 `docs/NO-WORK-ISSUE-RELAY.md`。它每轮只需创建一张 Issue：用户复制 Chat 输出的整份 JSON，在 Issue 正文中全选粘贴并提交，不需要寻找占位符或保留标记。Issue 不含正确答案；GitHub 使用加密答案和 Actions Secret 自行复核评分。首次必须完成一次加密答案与 `FORTUNE_ANSWER_KEY` 设置。

## 七、用户只需要说什么

日常无需使用 `gh`、Git 或 Python 命令。用户只需说：

> 开始当前案例下一轮。

或：

> 本轮已揭盲，请复盘并把通用修正落库后继续同一案例。

系统不得因为“测试通过”“文件齐全”或“训练次数够多”而宣布案例完成。唯一完成条件是当前案例连续 3 轮达到规定准确率。
