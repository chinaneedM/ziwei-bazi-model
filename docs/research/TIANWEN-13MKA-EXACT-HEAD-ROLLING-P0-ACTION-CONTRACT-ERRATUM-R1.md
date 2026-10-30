# 天问 13MKA｜13MK 既有 CI 当前行动前缀契约前向更正

在新提交 `f8103cbe185f9bab341b7173ff102d0800ec2ab0` 的 exact-HEAD GitHub Actions 中，13MK 专项校验已通过（run 41145097995），但多个既有守卫测试失败。代表性失败：

- 13KD run 41145097449：`issue["next_action"].startswith(latest_prefix+" CURRENT ACTION:")`；
- 13KX run 41145097676：`ValueError: rolling issue`；
- 13LI run 41145097660 与 13LG run 41145101271：同一字符串契约未满足。

根因为 13MK 的实际 `next_action` 使用了 `13MK CURRENT:`，而旧校验器所坚持的仓库契约是 `13MK CURRENT ACTION:`。仅补入 `ACTION` 以匹配已存在的消费者契约，**不改变研究对象、目标原字、数据裁决、数值、问题优先级和下一研究方向**。

研究遗漏 issue `TW-OPEN-0005` 的旧行动字符串不被抹去，原字符串保存在本次追加的 `ISSUE_REVISION.previous_next_action`，附本次更正证据。13MK 仍是同一个研究里程碑，故不人为新增研究批次、也不伪增 `schema_version` 或当前阶段快照，只修正格式兼容并留下独立审计痕迹。

原始 13MK source artifact、三个 G893 JPEG 页 SHA-256、1569 PDF、`001a` 的「少」字原印、002b 十六日布局、六控跨书裁决 0/6 的结论完全保留。排盘 `CLOSED`、算法重开 0。

13MK 专项校验的原脚本通过检测 revision ID 是否存在于 append-only `history` 来确认研究批次，而非将其强制指定为末一条记录，以允许该正当后续 CI 修正。
