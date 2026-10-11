# 天问 12SJ — 12SI exact-HEAD CI 旧批次来源计数回归修复

## 问题证据

12SI commit `7305ca353092d36162be3404fc25819465b1c507` 的 clean-training-system Actions run [38155947594](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/38155947594) 完成 Full unittest **2539 tests、2 failures**，其余 117 个 exact-HEAD checks success。两个失败只是旧批次测试把当前来源注册表总数固定到历史 12QF 时刻的 `647+7=654`：

- `test_ming_datong_yehuobian_12qe_cadal_direct_target_r1.py::test_extension_is_digest_bound_and_never_reopens_algorithm`：现值655 ≠ 旧硬编码654。
- `test_ming_datong_yehuobian_12qf_cadal_preface_date_r1.py::test_source_extension_and_product_gate`：现值8 ≠ 旧硬编码7。

## 修复原则

保留历史 12QE/12QF 原始来源影像、实际目标页、数字读数、SHA256 以及不可重开算法的独立判定。只将**全局、可增长的来源注册表合并计数**改成 forward-only 门禁：

```text
root_source_count = 647 (unchanged)
extension_source_count >= checkpoint floor (12QE/12QF:7, 12SI:8)
combined_source_count = root_source_count + extension_source_count
state.current_extension_count = manifest.extension_source_count
state.current_total_count = manifest.combined_source_count
checkpoint shard path and per-shard count remain present
```

12SI 自身回归测试也由“永远恰为8／655”同步调整为保留下限、总数和当前 state/manifest 相等。以后新增合法分片时不再误报历史目标页证据失败；任意来源总数不同步、删除已确认分片或更改原始直接页证据仍由各自回归与 `verify-historical-source-registry-extensions-r1.py` 拒绝。

这只是测试生命周期修复，**不是**新的正式 Matrix 历史批次；不改变 `PROJECT-CURRENT-STATE-R1.json`，也不增加来源、考据判定或排盘算法变动。补丁推送后仍须等待新 HEAD 完整 CI 通过才能宣布闭合。
