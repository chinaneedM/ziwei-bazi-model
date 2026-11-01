# 天问13NJ｜13NI 来源正式登记过早：保留研究，纠正统计与 CI

13NI 的**新发现《明史稿》NA03560 卷29电子文本**依然可作为待核实目标；12YM/12YN 两件已封存原印读数仍成立。错误在于：将尚未完成物理原页绑定的这条数字文本当作新的**正式来源总量**，使正式总量由 765 被动升为 766；新 shard 的校验状态也不在既有枚举中。精确 HEAD `c5a83ccb` 的来源注册表校验因此失败；若继续改写大批旧验收脚本中的 765 常量，会制造与此次文本线索不相称的工程复杂性。

**前向纠误，不删除证据**：

1. 保留 `docs/research/TIANWEN-13NI-MINGSHI-DRAFT-AND-TWO-ORIGINAL-REPLAY-R1.json`、其 Markdown，以及 `docs/research/TIANWEN-13NI-MINGSHIGAO-RECEIVED-SOURCE-SHARD-R1.json` 的全部原始内容，作为历史已提交且可重放的电子来源线索。不得再将其内暂记的 766 当作有效总量。
2. 从**正式启用的** extension manifest 列表撤销 13NI 此唯一新 shard 的登记，附上本纠误、旧提交号和撤回原因。保留旧源 ID 及文件不复用、不抹掉；这不等于否定《明史稿》电子收本的 4.9386 文本发现。
3. 实际启用来源总数回到 **647+118=765**，同时更新状态／遗漏账本版本和校验；不修改既有源文件、图谱、排盘、无关验收脚本。

本次没有新增《明史稿》原稿像素核读、没有为该数字文本建立独立明代或清代物理证据票。G893原刻“少”的位置与后续日差精度、NAAJ `子051-0003` 第六册物理对象仍未闭合。问题 TW-OPEN-0005=P0 OPEN，历史最终0/6，产品 CLOSED、算法重开0。

机器纠误：`docs/research/TIANWEN-13NJ-13NI-DIGITAL-LOCATOR-REGISTRY-CORRECTION-R1.json`。
