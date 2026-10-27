# 天问 12RR｜12RL–12RP 的历史研究父批次与阶段字段验证器修正

- 精确失败基线：`6378b9f89b6f635e960e2be82fe69ae49e894b5e`；Actions [38138635589](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/38138635589)，`clean-training-system` 完整单测 `2377 tests, errors=5`。
- 错误模块：12RL、12RM、12RN、12RO、12RP 的正向证据验证器。原验证器错误表达 `stage == parent_open_batch == "12QE_OPEN"`，或将左右字段颠倒，导致仓库中合法的 `parent_open_batch="12QE"; stage="12QE_OPEN"` 被误拒。
- 本修复只调整五处**验证器谓词**，独立确认上述两个字段，绝不改动任何来源影像、字形、图谱、算法、研究记录、现有哈希或计算规则。
- 增补 `tests/test_ming_datong_yehuobian_f3_parent_batch_scope_12rr.py`：五个真实记录正向校验，以及各记录分别篡改 parent 和 stage 必须拒绝，防止未来回归成两个字段假相等。
- 沿用同一国图馆藏和 12QE_OPEN 的证据域；`12QE` 的研究问题保持开放，`MD-G03` 尚未闭合，`HPA-DAYUN-CAL-002` 仍然 `MISSING_FROM_PRODUCT`。
- Matrix 222/222，元数据修复45/45，外部来源647+7=654。ChartR1 CLOSED，零算法重开、零候选坍缩。**本批只修 CI，不制造新古籍结论。**
