# 天问 12SQ — 12SO / 12SN 延展来源计数的增量 CI 回归修复

## 原因与证据

在远端 `c9fb70baef7122f5bdd1adc49e02703794fbdf09`，GitHub Actions [clean-training-system run 38162026311](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/38162026311) 的 **Full unittest** 实际失败：`test_yehuobian_tokyo_ioc_reproduction_12sn.Tokyo12SNReproductionServiceScope.test_shard_and_manifest_forward_only` 断言 `extension_source_count == 10`，而合法新增12SO机构数字化历史来源后为11。记录显示 `Ran 2554 tests in 776.010s`，仅一处 FAIL，预先的 `Verify` 步骤成功。

这证明故障在**测试把过去某次快照当作不可变全局计数**，并不证明根表、追加来源或确定性排盘出错。此前12SN曾固定`combined_source_count=657`和state对应字段；12SO自身测试也固定11/658，若未来新增12ST会再次触发相同错误。

## 允许演进，不放松验证

改动 `tests/test_yehuobian_tokyo_ioc_reproduction_12sn.py` 和 `tests/test_yehuobian_tokyo_2005_digitization_and_print_fingerprint_12so.py`：

- 必须包含**分别指定、唯一存在的12SN/12SO分片**，每片 `source_count=1`；原来源`source_id`及`physical_glyph_authority=False`等前置断言仍保持。
- 保留创建时的单向最低门禁（12SN ≥10，12SO ≥11），但不把后续扩充视为错误。
- `extension_source_count == sum(shard.source_count)`、`combined_source_count == root_source_count + extension_source_count`、state里的两个注册表计数分别等于manifest；禁止重复分片路径。这与现行 `scripts/verify-historical-source-registry-extensions-r1.py` 的原始文件SHA、来源ID唯一性、schema、图像字形准入验证形成相互独立的层级。
- 正式批次数量也只保留当时已完成批次的下限487，不能把补充批次的`latest_batch_doc`永久锁定在12QD，因为后续合法正式审计会替换指针。

新增模拟未来来源合法加入，以及计数漂移/重复路径的独立回归测试；不需要新增真实registry shard，不改源注册或传承谱。

## 保持

12SP四件藏本原叶取证队列仍为未获得原页、未发送申请与零独立字形票。Matrix 222/222，元数据修复45/45，来源647根+11扩展=658，传承谱248节点235边，正式批次487，latest12QD，排盘R1 CLOSED、零算法重开、12QE/MD-G03仍开放。只有本次新HEAD的 exact-head GitHub Actions 全绿才应宣布完整CI通过。
