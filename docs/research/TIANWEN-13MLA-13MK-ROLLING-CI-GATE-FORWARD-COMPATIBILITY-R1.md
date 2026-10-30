# 天问 13MLA｜13MK 历史原图测试的滚动版本兼容修复

当前提交 `ae4081505eb90f559ec719d19ca9cad5f0ba2dac` 的 GitHub Actions 原版 13ML 研究门禁、遗漏台账连续性门禁已 **success**。唯一已观察到的历史 source gate 失败是 [13MK 验证器 run 41146446400](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/41146446400) 的 `assert schema_version == ... == "1.973.0"`，而当前语义状态已经合法递增至 `1.974.0`。

13MK 证据本身是历史固定批次，但状态交接文件是滚动的。故以向后兼容方式修正 **脚本，不回写历史研究 JSON 和旧台账快照**：

1. 当前状态版本必须与遗漏台账版本相等，且 **不早于 1.973.0**；历史 13MK 状态证据保留在不可更改的 checkpoint `OMISSIONS-13MK-G893-001A-ORIGINAL-REACQUISITION-20261031`。
2. 13MK 研究焦点必须出现在完整 append-only focus 历史中，而不必永远是末尾唯一最新焦点。
3. 最新研究前缀仍要与当前焦点最后一项严格一致，最后 checkpoint 仍须匹配当前状态版本。
4. 保持 G893 原图三页哈希、001a 少字、002b 十六日、跨原本六项 0/6、未结 P0、产品 CLOSED 等源级检查不变。

此笔属于 **CI 形式契约修复**，不增加研究判断、不更新 `PROJECT-CURRENT-STATE-R1.json` 或遗漏台账版本，不新增物理见证与传承边；今后出现 1.975、1.976 等合法连续版本也不应导致旧 13MK 研究验证器重新失败。
